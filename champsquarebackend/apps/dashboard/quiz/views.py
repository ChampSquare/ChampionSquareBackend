import json

from django.utils.translation import gettext_lazy as _
from django.views.generic import  UpdateView, DetailView
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.db.models import Q

from django_tables2 import SingleTableMixin, SingleTableView

from champsquarebackend.core.loading import get_classes, get_model, get_class
from champsquarebackend.core.compat import get_user_model
from champsquarebackend.views.generic import BulkEditMixin
from champsquarebackend.apps.user.utils import normalise_email

User = get_user_model()
Category = get_model('quiz', 'category')
Quiz = get_model('quiz', 'quiz')
QuestionPaper = get_model('quiz', 'questionpaper')
Question = get_model('question', 'question')
AnswerPaper = get_model('quiz', 'answerpaper')
Participant = get_model('participate', 'participate')

CategoryForm, QuizForm, QuestionPaperForm \
    = get_classes('dashboard.quiz.forms', ['CategoryForm', 'QuizForm', 'QuestionPaperForm'])
UserSearchForm = get_class('dashboard.users.forms', 'UserSearchForm')

QuizTable, UserTable, ParticipantTable = get_classes('dashboard.quiz.tables',
                                                     ('QuizTable', 'UserTable', 'ParticipantTable'))



# Create your views here.

class QuizListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/quiz/quiz_list.html'
    table_class = QuizTable
    context_table_name = 'quizzes'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_caption(self):
        return _('Quizzes')

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.get_caption()
        return table

    def get_table_pagination(self, table):
        return dict(per_page=settings.SETTINGS_DASHBOARD_ITEMS_PER_PAGE)

    def get_queryset(self):
        """
            Build the queryset for this list
        """
        queryset = Quiz.objects.all()
        return queryset  

class CategoryCreateUpdateView(UpdateView):
    """
        Dashboard view that can be used to create and update
        Category (similar to questions). It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new subject.
        - when editing an existing question, this view is called with
        subject's primary key.
    """
    template_name = 'champsquarebackend/dashboard/quiz/category_create_update.html'
    model = Category
    context_object_name = 'category'
    form_class = CategoryForm
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
            category = get_object_or_404(Category, pk=self.kwargs['pk'])
            return category

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()

        # edit : add context data in here

        return ctx

    def get_page_title(self):
        if self.creating:
            return _('Create new category')
        else:
            return _('update category %s') % self.object.name

    def get_success_url(self):
        """
            return a success message and redirects to given url
        """
        msg = _("Added category '%s'") % self.object.__str__()
        messages.success(self.request, msg)

        return reverse('dashboard:quiz-list')

class QuizCreateUpdateView(UpdateView):
    """
        Dashboard view that can be used to create and update
        Category (similar to questions). It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new subject.
        - when editing an existing question, this view is called with
        subject's primary key.
    """
    template_name = 'champsquarebackend/dashboard/quiz/quiz_create_update.html'
    model = Quiz
    context_object_name = 'quiz'
    form_class = QuizForm
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
            quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
            return quiz

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()

        # edit : add context data in here

        return ctx

    def get_page_title(self):
        if self.creating:
            return _('Create new quiz')
        else:
            return _('Update quiz %s') % self.object.name

    def get_success_url(self):
        """
            return a success message and redirects to given url
        """
        if self.creating:
            msg = _("Added quiz '%s'") % self.object.__str__()
        else:
            msg = _("Updated quiz '%s'") % self.object.__str__()
        messages.success(self.request, msg)

        return reverse('dashboard:quiz-list')


class QuestionPaperCreateUpdateView(UpdateView):
    """
        Dashboard view that can be used to create and update
        Category (similar to questions). It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new subject.
        - when editing an existing question, this view is called with
        subject's primary key.
    """
    template_name = 'champsquarebackend/dashboard/quiz/questionpaper_create_update.html'
    model = QuestionPaper
    context_object_name = 'questionpaper'
    form_class = QuestionPaperForm
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
            quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
            return quiz

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()
        ctx['questions'] = Question.objects.all()
        
        if self.object.questionpaper:
            ctx['questions_in_questionpaper'] = self.object.questionpaper.questions.all()
            ctx['questions'] = Question.objects.exclude(
            id__in=self.object.questionpaper.questions.values_list('id', flat=True))

        # edit : add context data in here

        return ctx


    def get_page_title(self):
        if self.creating:
            return _('Create new questionpaper')
        else:
            return _('Update questionpaper ')

    def form_valid(self, form):
        action = self.request.POST.get('action')

        if action == "add-questions":
            question_ids = self.request.POST.getlist('questions', None)
            questions_to_add = Question.objects.filter(id__in=question_ids)
            questionpaper = self.object.questionpaper
            if questionpaper:
                questionpaper.questions.add(*questions_to_add)
                self.object.set_marks(questionpaper.calculate_marks())
                
            else:
                questionpaper = QuestionPaper.objects.create()
                questionpaper.questions.add(*questions_to_add)
                self.object.questionpaper = questionpaper
                self.object.set_marks(questionpaper.calculate_marks())
            
            
            messages.success(self.request, _('Successfully added chosen questions'))
            return HttpResponseRedirect(reverse('dashboard:quiz-questionpaper-update', kwargs={'pk': self.object.id}))
            
        elif action == 'remove-questions':
            question_ids = self.request.POST.getlist('added-questions', None)
            questions_to_remove = self.object.questionpaper.questions.filter(id__in=question_ids)
            self.object.questionpaper.questions.remove(*questions_to_remove)
            messages.success(self.request, _('Successfully removed chosen questions'))

        else:
            form.save()
            messages.success(self.request, "Form saved successfully")
            return HttpResponseRedirect(self.get_success_url())
            

    def get_success_url(self):
        """
            return a success message and redirects to given url
        """
        if self.creating:
            msg = _("Added quiz '%s'") % self.object.__str__()
        else:
            msg = _("Updated quiz '%s'") % self.object.__str__()
        messages.success(self.request, msg)

        return reverse('dashboard:quiz-list')


class AnswerPaperDetailView(DetailView):
    """ View to show answerpaper """
    model = AnswerPaper
    context_object_name = 'answerpaper'
    template_name = 'champsquarebackend/dashboard/quiz/answerpaper_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AnswerPaper, id=self.kwargs['pk'])


class AddUserView(BulkEditMixin, FormMixin, SingleTableView):
    template_name = 'champsquarebackend/dashboard/quiz/add_user.html'
    model = User
    actions = ('add_to_test',)
    form_class = UserSearchForm
    table_class = UserTable
    context_table_name = 'users'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)

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
        queryset = self.model.objects.exclude(
            id__in=self._get_quiz().users.values_list('id', flat=True))
        
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All Users (excludes quiz users)'),
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
        context['quiz_id'] = self.kwargs['pk']
        return context

    def _get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        return self._quiz


    def add_to_test(self, request, users):
        quiz = self._get_quiz()
        quiz.users.add(*users)
        messages.info(self.request, _("Successfully added users to quiz"))
        return redirect(reverse('dashboard:quiz-add-user', kwargs={'pk': self._get_quiz().id}))

class QuizParticipantView(AddUserView):
    template_name = 'champsquarebackend/dashboard/quiz/participants.html'
    model = Participant
    actions = ('remove_from_test', 'send_test_link',)
    form_class = UserSearchForm
    table_class = ParticipantTable
    context_table_name = 'participants'
    desc_template = _('%(main_filter)s %(email_filter)s %(name_filter)s')
    description = ''

    def get_queryset(self):
        queryset = self._get_quiz().participants.all()
        
        return self.apply_search(queryset)

    def apply_search(self, queryset):
        # Set initial queryset description, used for template context
        self.desc_ctx = {
            'main_filter': _('All Participants'),
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
            queryset = queryset.filter(user__email__istartswith=email)
            self.desc_ctx['email_filter'] \
                = _(" with email matching '%s'") % email
        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            # always true filter
            condition = Q()
            for part in parts:
                condition &= Q(user__first_name__icontains=part) \
                    | Q(user__last_name__icontains=part)
            queryset = queryset.filter(condition).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with name matching '%s'") % data['name']

        return queryset

    def remove_from_test(self, request, participates):
        # always delete via this way as it checks whether object exist or not first
        participant_to_delete = Participant.objects \
            .filter(id__in=list(map(lambda participant: participant.id, participates)))
        participant_to_delete.delete()
        messages.info(self.request, _("Successfully removed participant from list"))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))

    def send_test_link(self, request, participates):
        messages.info(self.request, _("Method hasn't be implemented"))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))