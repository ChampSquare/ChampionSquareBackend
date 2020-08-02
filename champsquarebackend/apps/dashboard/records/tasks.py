from celery import shared_task

from champsquarebackend.apps.dashboard.records.utils import post_process_video

@shared_task
def process_video(video_record_id):
    pass
    #return post_process_video(video_record_id)
