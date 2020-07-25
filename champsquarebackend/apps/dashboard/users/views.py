from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DeleteView, DetailView, FormView, ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView

from champsquarebackend.core.compat import get_user_model
from champsquarebackend.core.loading import get_class, get_classes, get_model
from champsquarebackend.views.generic import BulkEditMixin
from champsquarebackend.apps.user.utils import normalise_email


UserSearchForm, UserForm = get_classes('dashboard.users.forms', ['UserSearchForm', 'UserForm'])
PasswordResetForm = get_class('user.forms', 'PasswordResetForm')
UserTable, AddUserTable = get_classes('dashboard.users.tables', ['UserTable', 'AddUserTable'])
User = get_user_model()
Quiz = get_model('quiz', 'quiz')


class UserListView(BulkEditMixin, FormMixin, SingleTableView):
    template_name = 'champsquarebackend/dashboard/users/index.html'
    model = User
    actions = ('make_active', 'make_inactive', )
    form_class = UserSearchForm
    table_class = UserTable
    context_table_name = 'users'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)

    def get_table_pagination(self, table):
        return dict(per_page=settings.SETTINGS_DASHBOARD_ITEMS_PER_PAGE)

    def get_form_kwargs(self):
        """
        Only bind search form if it was submitted.
        """
        kwargs = super().get_form_kwargs()

        if 'search' in self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })

        return kwargs

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-date_joined')
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All users'),
            'email_filter': '',
            'name_filter': '',
        }
        if self.form.is_valid():
            return self.apply_search_filters(queryset, self.form.cleaned_data)
        else:
            return queryset

    def apply_search_filters(self, queryset, data):
        """
        Function is split out to allow customisation with little boilerplate.
        """
        if data['email']:
            email = normalise_email(data['email'])
            queryset = queryset.filter(email__istartswith=email)
            self.desc_ctx['email_filter'] \
                = _(" with email matching '%s'") % email
        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            # always true filter
            condition = Q()
            for part in parts:
                condition &= Q(first_name__icontains=part) \
                    | Q(last_name__icontains=part)
            queryset = queryset.filter(condition).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with name matching '%s'") % data['name']

        return queryset

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.desc_template % self.desc_ctx
        return table

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def make_inactive(self, request, users):
        return self._change_users_active_status(users, False)

    def make_active(self, request, users):
        return self._change_users_active_status(users, True)

    def _change_users_active_status(self, users, value):
        for user in users:
            if not user.is_superuser:
                user.is_active = value
                user.save()
        messages.info(self.request, _("Users' status successfully changed"))
        return redirect('dashboard:users-index')

class UserCreateUpdateView(UpdateView):
    model = User
    template_name = 'champsquarebackend/dashboard/users/user_form.html'
    form_class = UserForm
    context_object_name = 'user'
    creating = None

    def get_object(self, queryset=None):
        """
            This parts allows generic.UpdateView to handle creating
            questions as well. The only distinction between an UpdateView
            and a CreateView is that self.object is None. We emulate this behavior.
        """
        self.creating = 'pk' not in self.kwargs
        if self.creating:
            return None #success
        else:
            user = get_object_or_404(User, pk=self.kwargs['pk'])
            return user

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()
        return ctx
    
    def get_page_title(self):
        if self.creating:
            return _('Create new User')
        else:
            return _('Update user %s') % self.object.email

    def get_success_url(self):
        if self.creating:
            msg = _("Created user '%s'") % self.object.__str__()
        else:
            msg = _("Updated user '%s'") % self.object.__str__()
        messages.success(self.request, msg)
        return reverse('dashboard:users-index')


class AddUserToQuizView(UserListView):
    template_name = 'champsquarebackend/dashboard/users/add_user.html'
    model = User
    table_class = AddUserTable
    actions = ('add_to_test',)
    

    def get_queryset(self):
        # only fetch users which are not included in the quiz users list
        queryset = self.model.objects.exclude(
            id__in=self._get_quiz().users.values_list('id', flat=True))
        
        return self.apply_search(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['quiz_id'] = self.kwargs['pk']
        return context

    def _get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return self._quiz


    def add_to_test(self, request, users):
        quiz = self._get_quiz()
        quiz.users.add(*users)
        messages.info(self.request, _("Successfully added users to quiz"))
        return redirect(reverse('dashboard:quiz-add-user', kwargs={'pk': self._get_quiz().id}))

class UserDetailView(DetailView):
    template_name = 'champsquarebackend/dashboard/users/detail.html'
    model = User
    context_object_name = 'user'


class PasswordResetView(SingleObjectMixin, FormView):
    form_class = PasswordResetForm
    http_method_names = ['post']
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = {'email': self.object.email}
        return kwargs

    def form_valid(self, form):
        # The PasswordResetForm's save method sends the reset email
        form.save(request=self.request)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(
            self.request, _("A password reset email has been sent"))
        return reverse(
            'dashboard:user-detail', kwargs={'pk': self.object.id}
        )

