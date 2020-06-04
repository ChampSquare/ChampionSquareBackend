from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn

from champsquarebackend.dashboard.tables import DashboardTable
from champsquarebackend.quiz.models import Question

class QuestionTable(DashboardTable):
    description = TemplateColumn(
        verbose_name=_('Description'),
        template_name='dashboard/question/question_row_description.html',
        orderable=False)
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='dashboard/question/question_row_actions.html',
        orderable=False)

    class Meta(DashboardTable.Meta):
        model = Question
        fields = ('subject', 'question_type')
        sequence = ('description', 'subject', 'question_type', 'actions')
