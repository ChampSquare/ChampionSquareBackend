from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.conf import settings

from django_tables2 import SingleTableMixin, SingleTableView

from champsquarebackend.apps.quiz.models import Question
from .forms import AddQuestionForm, AddSubjectForm, AddTopicForm, QuestionTypeSelectionForm
from .tables import QuestionTable

# Create your views here.

def filter_questions(queryset, user):
    """
        Restrict the queryset to questions the given user has access to.
        A staff user has access to all questions.
    """
    if user.is_staff:
        return queryset

class QuestionListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'dashboard/question/question_list.html'
    question_type_selection_form = QuestionTypeSelectionForm
    table_class = QuestionTable
    context_table_name = 'questions'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['question_type_selection_form'] = self.question_type_selection_form
        return ctx

    def get_caption(self):
        return _('Questions')

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = self.get_caption()
        return table

    def get_table_pagination(self, table):
        return dict(per_page=5)

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
    template_name = 'dashboard/question/question_create_update.html'
    model = Question
    context_object_name = 'question'

    form_class = AddQuestionForm

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

    def process_all_forms(self, form):
        """
        short-circuits the regular logic to have one place 
        to have our logic to check all forms
        """



    
    


question_list_view = QuestionListView.as_view()

