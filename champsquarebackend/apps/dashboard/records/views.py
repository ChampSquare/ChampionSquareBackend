from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.views.generic import DeleteView, DetailView
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from django_tables2 import SingleTableMixin, SingleTableView
from celery import current_app


from champsquarebackend.core.loading import get_model, get_class
from champsquarebackend.views.generic import BulkEditMixin
from champsquarebackend.apps.dashboard.records.tasks import process_video

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


class ProcessVideoView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        task = process_video.delay(video_record_id=self.kwargs['pk'])
        
        context['task_id'] = task.id
        context['task_status'] = task.status

        return JsonResponse(context)

        # return render(self.request, 'champsquarebackend/dashboard/records/video_process.html', context)


        # return HttpResponseRedirect(reverse('dashboard:video-list')+'?task_id=%s&task_status=%s' % (task.id, task.status))
        
        # if response:
        #     video_record.is_processed = response
        #     video_record.file_name = video_record.create_processed_video_file_name()
        #     video_record.save()
        #     messages.info(self.request, _('Successfully converted video'))
        # else:
        #     messages.error(self.request, _('Failed to convert the video'))
        # return HttpResponseRedirect(reverse('dashboard:video-list'))

class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()
            response, video_id = task.get()
            if response:
                video_record = VideoRecord.objects.get(id=video_id)
                video_record.is_processed = True
                video_record.save()
        return JsonResponse(response_data)

