from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.generic import DeleteView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from django_tables2 import SingleTableMixin, SingleTableView


from champsquarebackend.core.loading import get_model, get_class
from champsquarebackend.views.generic import BulkEditMixin

VideoRecord = get_model('monitoring', 'videorecord')
VideoRecordTable = get_class('dashboard.records.tables', 'VideoRecordTable')

class VideoListView(SingleTableView):
    """
        Dashboard view of question list.
    """

    template_name = 'champsquarebackend/dashboard/records/videos_list.html'
    table_class = VideoRecordTable
    context_table_name = 'videos'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_caption(self):
        return _('All Videos')

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
        queryset = VideoRecord.objects.all()
        return queryset


class VideoDeleteView(DeleteView):
    """
    Dashboard view to delete a video.
    Supports the permission-based dashboard.
    """
    template_name = 'champsquarebackend/dashboard/records/video_delete.html'
    model = VideoRecord

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['title'] = _("Are you sure want to delete the video?" )
        return ctx

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_processed:
            self.object.delete_raw_files()
        self.object.delete()
        # delete respective video files
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        messages.info(self.request, _('Successfully deleted video'))
        return reverse('dashboard:video-list')
