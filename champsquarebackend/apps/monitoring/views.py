from django.views.generic import  DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

from champsquarebackend.core.loading import get_model, get_class

AnswerPaper = get_model('quiz', 'AnswerPaper')
VideoRecord = get_model('monitoring', 'VideoRecord')


class SaveVideoRecordView(DetailView):
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
        date = {
            'success': True
        }
        return JsonResponse(date)
