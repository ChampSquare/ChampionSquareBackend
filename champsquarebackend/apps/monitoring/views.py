from django.views.generic import  DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from champsquarebackend.core.loading import get_model, get_class

AnswerPaper = get_model('quiz', 'AnswerPaper')
VideoRecord = get_model('monitoring', 'VideoRecord')


class SaveVideoRecordView(DetailView):
    """
        save video record details
    """
    def get(self, request, *args, **kwargs):
        answer_paper_id = request.GET.get('paper_id', None)
        video_record_type = request.GET.get('video_record_type', None)
        record_id = request.GET.get('record_id', None)
        answer_paper = AnswerPaper.objects.get(id=answer_paper_id)
        name = answer_paper.participant.user.email
        file_name = VideoRecord.create_mjr_video_file_name(record_id, video_record_type)

        video_record = VideoRecord(answerpaper=answer_paper, name=name,
                                   type=video_record_type,
                                   record_id=record_id, file_name=file_name)
        video_record.save()
        video_record.create_record_file()
        if video_record_type == 'webcam':
            answer_paper.set_status('webcam_permssion_granted')
        elif video_record_type == 'screen':
            answer_paper.set_status('screen_sharing_permission_granted')
        date = {
            'success': True
        }
        return JsonResponse(date)
