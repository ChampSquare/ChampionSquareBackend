import json

from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, UpdateView
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


from django_tables2 import SingleTableMixin, SingleTableView


from champsquarebackend.core.loading import get_classes, get_model, get_class


CategoryForm, QuizMetaForm, QuestionPaperForm, QuizRestrictionsForm \
    = get_classes('dashboard.quiz.forms', ['CategoryForm', 'QuizMetaForm',
                    'QuestionPaperForm', 'QuizRestrictionsForm'])
Category = get_model('quiz', 'category')
Quiz = get_model('quiz', 'quiz')
QuizForm = get_class('dashboard.quiz.forms', 'QuizForm')
QuizTable = get_class('dashboard.quiz.tables', 'QuizTable')

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

class QuizWizardStepView(FormView):
    wizard_name = 'quiz_wizard'
    form_class = None
    step_name = None
    update = False
    url_name = None

    # Keep a reference to previous view class to allow checks to be made on
    # whether prior steps have been completed
    previous_view = None

    def dispatch(self, request, *args, **kwargs):
        if self.update:
            self.quiz = get_object_or_404(Quiz, id=kwargs['pk'])
        if not self.is_previous_step_complete(request):
            messages.warning(
                request, _("%s step not complete") % (
                    self.previous_view.step_name.title(),))
            return HttpResponseRedirect(self.get_back_url())
        return super().dispatch(request, *args, **kwargs)

    def is_previous_step_complete(self, request):
        if not self.previous_view:
            return True
        return self.previous_view.is_valid(self, request)

    def _key(self, step_name=None, is_object=False):
        key = step_name if step_name else self.step_name
        if self.update:
            key += str(self.quiz.id)
        if is_object:
            key += '_obj'
        return key

    def _store_form_kwargs(self, form):
        session_data = self.request.session.setdefault(self.wizard_name, {})

        # Adjust kwargs to avoid trying to save the category instance
        form_data = form.cleaned_data.copy()
        category = form_data.get('category', None)
        questions = form_data.get('questions', None)
        if category is not None:
            form_data['category'] = category.id
        question_list = []
        if questions is not None:
            for question in questions:
                question_list.append(question.id)
            form_data['questions'] = question_list
        form_kwargs = {'data': form_data}
        json_data = json.dumps(form_kwargs, cls=DjangoJSONEncoder)

        session_data[self._key()] = json_data
        self.request.session.save()

    def _fetch_form_kwargs(self, step_name=None):
        if not step_name:
            step_name = self.step_name
        session_data = self.request.session.setdefault(self.wizard_name, {})
        json_data = session_data.get(self._key(step_name), None)
        if json_data:
            return json.loads(json_data)

        return {}

    def _store_object(self, form):
        session_data = self.request.session.setdefault(self.wizard_name, {})

        # We don't store the object instance as that is not JSON serialisable.
        # Instead, we save an alternative form
        instance = form.save(commit=False)
        json_qs = serializers.serialize('json', [instance])

        session_data[self._key(is_object=True)] = json_qs
        self.request.session.save()

    def _fetch_object(self, step_name, request=None):
        if request is None:
            request = self.request
        session_data = request.session.setdefault(self.wizard_name, {})
        json_qs = session_data.get(self._key(step_name, is_object=True), None)
        if json_qs:
            # Recreate model instance from passed data
            deserialised_obj = list(serializers.deserialize('json', json_qs))
            return deserialised_obj[0].object

    def _fetch_session_quiz(self):
        """
        Return the quiz instance loaded with the data stored in the
        session.  When updating an quiz, the updated fields are used with the
        existing quiz data.
        """
        quiz = self._fetch_object('metadata')
        if quiz is None and self.update:
            quiz = self.quiz
        return quiz

    def _flush_session(self):
        self.request.session[self.wizard_name] = {}
        self.request.session.save()

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = {}
        if self.update:
            form_kwargs['instance'] = self.get_instance()
        session_kwargs = self._fetch_form_kwargs()
        form_kwargs.update(session_kwargs)
        parent_kwargs = super().get_form_kwargs(
            *args, **kwargs)
        form_kwargs.update(parent_kwargs)
        return form_kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.update:
            ctx['quiz'] = self.quiz
        ctx['session_quiz'] = self._fetch_session_quiz()
        ctx['title'] = self.get_title()
        return ctx

    def get_back_url(self):
        if not self.previous_view:
            return None
        if self.update:
            return reverse(self.previous_view.url_name,
                           kwargs={'pk': self.kwargs['pk']})
        return reverse(self.previous_view.url_name)

    def get_title(self):
        return self.step_name.title()

    def form_valid(self, form):
        self._store_form_kwargs(form)
        self._store_object(form)

        if self.update and 'save' in form.data:
            # Save changes to this quiz when updating and pressed save button
            return self.save_quiz(self.quiz)
        else:
            # Proceed to next page
            return super().form_valid(form)

    def save_quiz(self, quiz):
        # We update the quiz with the name/description from step 1
        session_quiz = self._fetch_session_quiz()
        quiz.name = session_quiz.name
        quiz.description = session_quiz.description

        # Save the related models, then save the quiz.
        # Note than you can save already on the first page of the wizard,
        # so le'ts check if the benefit and condition exist
        question_paper = self._fetch_object('question_paper')
        if question_paper:
            question_paper.save()
            quiz.question_paper = question_paper

        quiz.save()

        self._flush_session()

        if self.update:
            msg = _("quiz '%s' updated") % quiz.name
        else:
            msg = _("quiz '%s' created!") % quiz.name
        messages.success(self.request, msg)

        return HttpResponseRedirect(reverse(
            'dashboard:quiz-detail', kwargs={'pk': quiz.pk}))

    def get_success_url(self):
        if self.update:
            return reverse(self.success_url_name,
                           kwargs={'pk': self.kwargs['pk']})
        return reverse(self.success_url_name)

    @classmethod
    def is_valid(cls, current_view, request):
        if current_view.update:
            return True
        return current_view._fetch_object(cls.step_name, request) is not None


class QuizMetaDataCreateUpdateView(QuizWizardStepView):
    step_name = 'metadata'
    form_class = QuizMetaForm
    template_name = 'champsquarebackend/dashboard/quiz/quiz_metadata_form.html'
    url_name = 'dashboard:quiz-metadata'
    success_url_name = 'dashboard:quiz-questionpaper'

    def get_instance(self):
        return self.quiz

    def get_title(self):
        return _("Quiz Detail")

class QuizQuestionPaperCreateUpdateView(QuizWizardStepView):
    step_name = 'questionpaper'
    form_class = QuestionPaperForm
    template_name = 'champsquarebackend/dashboard/quiz/quiz_questionpaper_form.html'
    previous_view = QuizMetaDataCreateUpdateView
    url_name = 'dashboard:quiz-questionpaper'
    success_url = 'dashboard:quiz-restrictions'

    def get_instance(self):
        return self.quiz.questionpaper

    def get_title(self):
        return _("Question Paper")


class QuizRestrictionscreateUpdateView(QuizWizardStepView):
    step_name = 'restrictions'
    form_class = QuizRestrictionsForm
    template_name = 'champsquarebackend/dashboard/quiz/quiz_restrictions_form.html'
    previous_view = QuizQuestionPaperCreateUpdateView
    url_name = 'dashboard:quiz-restrictions'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        return self.save_quiz(quiz)

    def get_instance(self):
        return self.quiz

    def get_title(self):
        return _("Restrictions")



    