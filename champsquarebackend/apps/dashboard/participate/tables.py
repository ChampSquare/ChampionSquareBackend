from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Participant = get_model('participate', 'participant')


class ParticipantTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/participate/participant_row_checkbox.html',
        verbose_name=' ', orderable=False)
    
    name = Column(
        verbose_name=_('Name'),
        orderable=False, accessor=('full_name')
    )

    attempt = Column(
        verbose_name=_('Attempted?'),
        orderable=False, accessor=('has_taken_quiz')
    )

    start_time = Column(
        verbose_name=_('Start Time'),
        orderable=True, accessor=('start_date_time')
    )

    end_time = Column(
        verbose_name=_('End Time'),
        orderable=False, accessor=('end_date_time')
    )

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/participate/participant_table.html'