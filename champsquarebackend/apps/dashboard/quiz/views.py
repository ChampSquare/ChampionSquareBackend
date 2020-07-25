import json

from django.utils.translation import gettext_lazy as _
from django.views.generic import  UpdateView, DetailView, FormView
from django.conf import settings
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.db.models import Q

from django_tables2 import SingleTableMixin, SingleTableView

from champsquarebackend.core.loading import get_classes, get_model, get_class
from champsquarebackend.core.compat import get_user_model
from champsquarebackend.views.generic import BulkEditMixin

User = get_user_model()
Category = get_model('quiz', 'category')
Quiz = get_model('quiz', 'quiz')
QuestionPaper = get_model('quiz', 'questionpaper')
Question = get_model('question', 'question')
AnswerPaper = get_model('quiz', 'answerpaper')
Participant = get_model('participate', 'participant')

QuizCreateSessionMixin = get_class('dashboard.quiz.mixins', 'QuizCreateSessionMixin')

CategoryForm, QuizForm, QuizMetaForm, QuestionPaperForm \
    = get_classes('dashboard.quiz.forms', ['CategoryForm', 'QuizForm', 'QuizMetaForm', 'QuestionPaperForm'])

QuizTable = get_class('dashboard.quiz.tables','QuizTable')



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


class QuizMetaCreateView(QuizCreateSessionMixin, FormView):
    template_name = 'champsquarebackend/dashboard/quiz/quiz_meta_create.html'
    form_class = QuizMetaForm
    success_url = reverse_lazy('dashboard:quiz-list')
    pre_conditions = ['check_category_exists']
    skip_conditions = []



