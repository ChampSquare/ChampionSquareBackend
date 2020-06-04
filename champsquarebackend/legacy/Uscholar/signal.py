from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import VideoRecord

@receiver(post_save, sender=VideoRecord)
def save_video_record_file(sender, instance, **kwargs):
    instance.create_record_file()

post_save.connect(save_video_record_file, sender=VideoRecord)
