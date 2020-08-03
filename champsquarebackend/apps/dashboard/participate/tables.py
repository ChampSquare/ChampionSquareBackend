from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Participant = get_model('participate', 'participant')


class ParticipantTable(DashboardTable):
    check = TemplateColumn(
        template_name='champsquarebackend/dashboard/participate/participant_row_checkbox.html',
        verbose_name=' ', orderable=False)
    
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='champsquarebackend/dashboard/participate/participant_row_user.html',
        orderable=False
    )

    attempt = Column(
        verbose_name=_('Attempted?'),
        orderable=False, accessor=('has_taken_quiz')
    )

    start_time = Column(
        verbose_name=_('Start Time'),
        orderable=True, accessor=('start_date_time')
    )

    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/participate/participant_row_actions.html',
        orderable=False)

    icon = "group"

    class Meta(DashboardTable.Meta):
        template_name = 'champsquarebackend/dashboard/participate/participant_table.html'