from django.utils.translation import gettext_lazy as _

from django_tables2 import TemplateColumn, A, Column

from champsquarebackend.core.loading import get_model, get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
VideoRecord = get_model('monitoring', 'videorecord')


class VideoRecordTable(DashboardTable):
    id = TemplateColumn(
        verbose_name=_('Id'),
        template_name='champsquarebackend/dashboard/records/videos_row_id.html',
        orderable=False
    )

    user = TemplateColumn(
        verbose_name=_('User'),
        template_name='champsquarebackend/dashboard/records/videos_row_user.html',
        orderable=False
    )

    type = Column(
        verbose_name=_('Type'),
        orderable=True, accessor=('type')
    )

    start_time = Column(
        verbose_name=_('Start Time'),
        orderable=True, accessor=('created_at')
    )

    is_processed = Column(
        verbose_name=_('Is Processed?'),
        orderable=True, accessor=('is_processed'))

    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='champsquarebackend/dashboard/records/videos_row_actions.html',
        orderable=False)

    icon = "group"

    class Meta(DashboardTable.Meta):
        model = VideoRecord
        fields = ()
        sequence = ('counter', 'id', 'user', 'type', 'start_time', 'is_processed', 'actions')
