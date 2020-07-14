import itertools

from django.utils.translation import ngettext_lazy
from django.utils.translation import gettext_lazy as _
from django_tables2 import Table, Column


class DashboardTable(Table):
    caption = ngettext_lazy('%d Row', '%d Rows')
    counter = Column(
        verbose_name=_("Sr."),
        empty_values=(),
        orderable=False
    )

    def get_caption_display(self):
        # Allow overriding the caption with an arbitrary string that we cannot
        # interpolate the number of rows in
        try:
            return self.caption % self.paginator.count
        except TypeError:
            pass
        return self.caption

    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)

    class Meta:
        template_name = 'champsquarebackend/dashboard/table.html'
        attrs = {'class': 'table table-striped table-bordered'}
