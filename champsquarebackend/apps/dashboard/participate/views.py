from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from django.db.models import Q



from django_tables2 import SingleTableView

from champsquarebackend.apps.user.utils import normalise_email
from champsquarebackend.core.loading import get_model, get_class
from champsquarebackend.core.compat import get_user_model

Quiz = get_model('quiz', 'quiz')
Participant = get_model('participate', 'participant')
ParticipantTable = get_class('dashboard.participate.tables', 'ParticipantTable')
NewUserForm = get_class('dashboard.participate.forms', 'NewUserForm')
UserListView = get_class('dashboard.users.views', 'UserListView')

User = get_user_model()


class ParticipantListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/participate/participant_list.html'
    table_class = ParticipantTable
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
        queryset = get_object_or_404(Participant, quiz=self.kwargs.get('pk'))
        return queryset


class QuizParticipantListView(UserListView):
    template_name = 'champsquarebackend/dashboard/participate/participants.html'
    model = Participant
    actions = ('remove_from_test', 'send_test_link',)
    table_class = ParticipantTable
    context_table_name = 'participants'


    def get_queryset(self):
        queryset = self._get_quiz().participants.all()
        
        return self.apply_search(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['quiz_id'] = self.kwargs['pk']
        return context

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

    def _get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return self._quiz

    def remove_from_test(self, request, participants):
        # always delete via this way as it checks whether object exist or not first
        # participant_to_delete = Participant.objects \
            # .filter(id__in=list(map(lambda participant: participant.id, participants)))
        participant_to_delete = Participant.objects \
            .filter(id__in=[participant.id for participant in participants])
        participant_to_delete.delete()
        messages.info(self.request, _("Successfully removed participant from list"))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))

    def send_test_link(self, request, participants):
        messages.info(self.request, _("Method hasn't be implemented"))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))


class QuizParticipantCreateView(CreateView):
    model = User
    template_name = 'champsquarebackend/dashboard/participate/participant_form.html'
    form_class = NewUserForm

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(
            Quiz, pk=kwargs.get('pk', None))
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
        return reverse('dashboard:quiz-participant-list', kwargs={'pk': self.kwargs['pk']})




class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'champsquarebackend/dashboard/participate/detail.html'
    context_object_name = 'participant'
