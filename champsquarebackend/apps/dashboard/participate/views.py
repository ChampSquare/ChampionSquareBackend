from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import ProtectedError

from django_tables2 import SingleTableView

from champsquarebackend.core.loading import get_model, get_class, get_classes
from champsquarebackend.core.compat import get_user_model

Quiz = get_model('quiz', 'quiz')
Participant = get_model('participate', 'participant')
ParticipantTable = get_class('dashboard.participate.tables', 'ParticipantTable')
ParticipantForm = get_class('dashboard.participate.forms', 'ParticipantForm')
UserListView = get_class('dashboard.users.views', 'UserListView')

ParticipantDispatcher = get_class('dashboard.participate.utils', 'ParticipantDispatcher')


User = get_user_model()


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
        try:
            participant_to_delete.delete()
            messages.success(self.request, _("Successfully removed participant from list"))
        except ProtectedError:
            messages.error(self.request, _('Can\'t delete protected user'))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))

    def send_test_link(self, request, participants):
        site = get_current_site(request)
        response = None
        for participant in participants:
            ctx = {
                'site': site,
                'start_date_time': participant.start_date_time,
                'video_monitoring_enabled': participant.video_monitoring_enabled,
                'duration': participant.duration,
                'quiz_link': participant.get_absolute_url()
            }
            response = ParticipantDispatcher().send_quiz_link_email_for_user(participant, ctx)

        messages.info(self.request, _(response))
        return redirect(reverse('dashboard:quiz-participant-list', kwargs={'pk': self._get_quiz().id}))


class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'champsquarebackend/dashboard/participate/detail.html'
    context_object_name = 'participant'


class ParticipantCreateUpdateView(UpdateView):
    """
        Dashboard view that can be used to create and update
        Category (similar to questions). It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new subject.
        - when editing an existing question, this view is called with
        subject's primary key.
    """
    template_name = 'champsquarebackend/dashboard/participate/participant_create_update.html'
    model = Participant
    context_object_name = 'participant'
    form_class = ParticipantForm
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
            participant = get_object_or_404(Participant, pk=self.kwargs['pk'])
            return participant

    def get_quiz(self):
        if not hasattr(self, '_quiz'):
            self._quiz = get_object_or_404(Quiz, pk=self.kwargs['quiz_pk'])
        return self._quiz

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()
        ctx['quiz_pk'] = self.get_quiz().id

        # edit : add context data in here

        return ctx

    def get_page_title(self):
        if self.creating:
            return _('Create new Participant')
        else:
            return _('Update Participant %s') % self.object.full_name

    def get_success_url(self):
        """
            return a success message and redirects to given url
        """
        if self.creating:
            msg = _("Added participant '%s'") % self.object.__str__()
        else:
            msg = _("Updated quiz '%s'") % self.object.__str__()
        messages.success(self.request, msg)

        return reverse('dashboard:quiz-participant-list', kwargs={'pk': self.kwargs['quiz_pk']})
