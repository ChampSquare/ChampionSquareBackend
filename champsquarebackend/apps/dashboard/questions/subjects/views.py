from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.contrib import messages
from django.urls import reverse

from champsquarebackend.core.loading import get_classes, get_model

(SubjectForm, TopicForm) = get_classes('dashboard.questions.subjects.forms',
                                       ('SubjectForm', 'TopicForm'))
Subject = get_model('question', 'subject')

def filter_subjects(queryset, user):
    """
        Restrict the queryset to questions the given user has access to.
        A staff user has access to all questions.
    """
    if user.is_staff:
        return queryset
    return None


class SubjectCreateUpdateView(generic.UpdateView):
    """
        Dashboard view that can be used to create and update
        subjects (similar to questions). It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new subject.
        - when editing an existing question, this view is called with
        subject's primary key.
    """
    template_name = 'champsquarebackend/dashboard/questions/subjects/subject_create_update.html'
    model = Subject
    context_object_name = 'subject'

    form_class = SubjectForm

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
            subject = super().get_object(queryset)
            return subject

    def get_queryset(self):
        """
            filter questions that the user doesn't have permission to update
        """
        return filter_subjects(Subject.objects.all(), self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()

        # edit : add context data in here

        return ctx

    def get_page_title(self):
        if self.creating:
            return _('Create new Subject')
        else:
            return _('Edit Subject')

    def get_success_url(self):
        """
            return a success message and redirects to given url
        """
        msg = _("Added subject '%s'") % self.object.__str__()
        messages.success(self.request, msg)

        return reverse('dashboard:questions-list')
