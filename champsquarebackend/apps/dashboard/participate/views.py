from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_tables2 import SingleTableMixin, SingleTableView


from champsquarebackend.core.loading import get_model, get_class
from champsquarebackend.views.generic import BulkEditMixin

Participate = get_model('participate', 'participate')
ParticipateTable = get_class('dashboard.participate.tables', 'ParticipateTable')

class ParticipateListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/participate/participate_list.html'
    table_class = ParticipateTable
    context_table_name = 'participants'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_caption(self):
        return _('Participants')

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
        queryset = Participate.objects.filter(quiz=self.kwargs.get('pk'))
        return queryset
