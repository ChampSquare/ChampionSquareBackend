import itertools
from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Quiz = get_model('quiz', 'quiz')

class QuizTable(DashboardTable):
    counter = Column(
        verbose_name=_("Sr."),
        empty_values=(),
        orderable=False
    )
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('name'))

    category = Column(
        verbose_name=_('Category'),
        orderable=False, accessor=('category'))

    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/quiz/quiz_row_actions.html',
        orderable=False)

    icon = "sitemap"

    class Meta(DashboardTable.Meta):
        model = Quiz
        fields = ()
        sequence = ('counter', 'name', 'category', 'actions')

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)
