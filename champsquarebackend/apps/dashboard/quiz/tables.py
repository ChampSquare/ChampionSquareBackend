from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column, LinkColumn

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Quiz = get_model('quiz', 'quiz')

class QuizTable(DashboardTable):
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('name'))

    category = Column(
        verbose_name=_('Category'),
        orderable=False, accessor=('category'))

    total_marks = Column(
        verbose_name=_('Marks'),
        orderable=False, accessor=('total_marks'))

    questions = TemplateColumn(
        verbose_name=_('Questions'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_questions.html',
        orderable=False)

    users = TemplateColumn(
        verbose_name=_('Users'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_users.html',
        orderable=False)

    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = Quiz
        fields = ()
        sequence = ('counter', 'name', 'questions', 'total_marks', 'users', 'category', 'actions')

