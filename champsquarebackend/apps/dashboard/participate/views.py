from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView

from django_tables2 import SingleTableMixin, SingleTableView


from champsquarebackend.core.loading import get_model, get_class
from champsquarebackend.views.generic import BulkEditMixin
from champsquarebackend.core.compat import get_user_model

Quiz = get_model('quiz', 'quiz')
Participate = get_model('participate', 'participate')
ParticipateTable = get_class('dashboard.participate.tables', 'ParticipateTable')
NewUserForm = get_class('dashboard.participate.forms', 'NewUserForm')

User = get_user_model()


class ParticipateListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/participate/participate_list.html'
    table_class = ParticipateTable
    context_table_name = 'participants'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_caption(self):
        return _('Participants')

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
        queryset = Participate.objects.filter(quiz=self.kwargs.get('pk'))
        return queryset

class QuizParticipantCreateView(CreateView):
    model = User
    template_name = 'champsquarebackend/dashboard/participate/participate_user_form.html'
    form_class = NewUserForm

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            Quiz, pk=kwargs.get('quiz_pk', None))
        return super().dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['quiz'] = self.quiz
        ctx['title'] = _('Create user')
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['quiz'] = self.quiz
        return kwargs

    def get_success_url(self):
        name = self.object.get_full_name() or self.object.email
        messages.success(self.request,
                         _("User '%s' was created successfully.") % name)
        return reverse('dashboard:quiz-participant-list', kwargs={'pk': self.kwargs['quiz_pk'] })
