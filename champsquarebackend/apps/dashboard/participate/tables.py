from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Participate = get_model('participate', 'participate')


class ParticipateTable(DashboardTable):
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('full_name')
    )

    attempt = Column(
        verbose_name=_('Attempted?'),
        orderable=True, accessor=('has_taken_quiz')
    )

    start_time = Column(
        verbose_name=_('Start Time'),
        orderable=False, accessor=('get_start_time')
    )

    end_time = Column(
        verbose_name=_('End Time'),
        orderable=False, accessor=('get_end_time')
    )

    # marks = TemplateColumn(
    #     verbose_name=_('Marks Obtained'),
    #     template_name='champsquarebackend/dashboard/participate/participate_row_marks.html',
    #     orderable=False)

    # actions = TemplateColumn(
    #     verbose_name=_('Actions'),
    #     template_name='champsquarebackend/dashboard/participate/participate_row_actions.html',
    #     orderable=False)

    icon = "group"

    class Meta(DashboardTable.Meta):
        model = Participate
        fields = ()
        # sequence = ('counter', 'name', 'status', 'marks', 'start_time', 'actions')