import itertools
from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Question = get_model('question', 'question')

class QuestionTable(DashboardTable):
    counter = Column(
        verbose_name=_("Sr."),
        empty_values=(),
        orderable=False
    )
    description = TemplateColumn(
        verbose_name=_('Description'),
        template_name='champsquarebackend/dashboard/questions/question_row_description.html',
        orderable=False, accessor=A('description'))
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/questions/question_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = Question
        fields = ('subject', 'question_type')
        sequence = ('counter', 'description', 'subject', 'question_type', 'actions')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)
