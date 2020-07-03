from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse

from django_tables2 import SingleTableMixin, SingleTableView


from champsquarebackend.core.loading import get_classes, get_model, get_class


QuestionForm = get_class('dashboard.questions.forms',
                         'QuestionForm')
Question = get_model('question', 'question')
Subject = get_model('question', 'subject')
QuestionTable = get_class('dashboard.questions.tables',
                          'QuestionTable')

# Create your views here.



def filter_questions(queryset, user):
    """
        Restrict the queryset to questions the given user has access to.
        A staff user has access to all questions.
    """
    if user.is_staff:
        return queryset
    return None

class QuestionListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/questions/question_list.html'
    table_class = QuestionTable
    context_table_name = 'questions'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_caption(self):
        return _('Questions')

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
        queryset = Question.objects.all()
        return queryset     

class QuestionCreateUpdateView(generic.UpdateView):
    """
        Dashboard view that can be used to create and update
        questions. It can be used in two different ways,
        each of them with unique URL pattern:
        - when creating a new question, this view can be called
        with desired question type.
        - when editing an existing question, this view is called with
        question's primary key.
    """
    template_name = 'champsquarebackend/dashboard/questions/question_create_update.html'
    model = Question
    context_object_name = 'question'

    form_class = QuestionForm

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
            question = super().get_object(queryset)
            # self.question_type = question.question_type
            return question

    def get_queryset(self):
        """
            filter questions that the user doesn't have permission to update
        """
        return filter_questions(Question.objects.all(), self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.get_page_title()

        # edit : add context data in here

        return ctx

    def get_page_title(self):
        if self.creating:
            return _('Create new Question')
        else:
            return _('Edit Question')

    def get_url_with_querystring(self, url):
        url_parts = [url]
        if self.request.GET.urlencode():
            url_parts += [self.request.GET.urlencode()]
        return "?".join(url_parts)

    def get_success_url(self):
        """
            Renders a success message and redirects depending on the button
            - Standard case is pressing "Save"; redirects to the question list
            - when "Save and continue" is pressed; we stay on the same page
            - When "Save and Add Another" is pressed it, redirects to a new question
              creation page.
        """
        msg = _("Successfully added question '%s'") % self.object.__str__()
        messages.success(self.request, msg, extra_tags="safe noicon")

        action = self.request.POST.get('action')
        if action == 'continue':
            # stay on same editing page
            return reverse(
                'dashboard:question-update', kwargs={"pk": self.object.id}
            )
        elif action == 'create-another-question':
            # render  a new form to add question
            return reverse(
                'dashboard:question-create', kwargs={}
            )
        else:
            # go back to question list
            return reverse('dashboard:questions-list', kwargs={})
        