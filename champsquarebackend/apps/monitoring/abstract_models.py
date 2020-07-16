import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.files import File


# from taggit.managers import TaggableManager

from champsquarebackend.models.models import TimestampedModel, ModelWithMetadata
# Create your models here.


class AbstractVideoRecord(ModelWithMetadata, TimestampedModel):
    participant = models.ForeignKey('participate.Participate',
                                       related_name='videos',
                                       on_delete=models.PROTECT,
                                       verbose_name=_('Participant'))
    name = models.CharField(max_length=50)

    RECORD_TYPE = (
        ('webcam', 'Webcam'),
        ('screen', 'Screen Recording')
    )

    type = models.CharField(_('Video Type'), max_length=20, choices=RECORD_TYPE)
    record_id = models.CharField(max_length=50, null=True, blank=True)
    file_name = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(_('Url of video'), blank=True, null=True)
    is_processed = models.BooleanField(_('Is video file processed?'), default=False)

    class Meta:
        abstract = True
        app_label = 'monitoring'
        verbose_name = _('Video Record')
        verbose_name_plural = _('Video Records')
        ordering = ['-created_at']

    def __str__(self):
        return "{0}, type: {1}".format(self.name, self.type)

    def get_info_file_name(self):
        return self.record_id+"_"+self.type+".nfo"

    def get_video_dir(self):
        return str(settings.ROOT_DIR)+ settings.SETTINGS_VIDEO_RECORD_FOLDER_NAME

    def create_record_file(self):
        file_name = self.get_info_file_name()

        video_rec_dir = self.get_video_dir()
        # todo : check whether dir exists or not
        # create first if it doesn't exist
        with open(video_rec_dir+file_name, 'w') as f:
            video_file = File(f)
            if self.type == 'webcam':
                video_file.write("[{0}]\n name = {1}-{4}\ndate = {2}\naudio = {3}_{4}-audio.mjr\nvideo = {3}_{4}-video.mjr"
                                 .format(self.record_id, self.name, self.created_at, self.file_name, self.type))
            else:
                video_file.write("[{0}]\n name = {1}-{3}\ndate = {2}\n video = {0}_{3}-video.mjr"
                                 .format(self.record_id, self.name, self.created_at, self.type))


    def delete_raw_files(self):
        # get video directory
        video_dir = self.get_video_dir()
        # each video has corresponding info file
        info_file = self.get_info_file_name()
        # get the video file name
        video_file = "{0}_{1}-video.mjr".format(self.record_id, self.type)
        # delete info file
        self._delete_file(video_dir+info_file)
        #delete video file
        self._delete_file(video_dir+video_file)

        if self.type == 'webcam':
            # if type is webcam, there should be an audio file as well
            audio_file = "{0}_{1}-audio.mjr".format(self.file_name, self.type)
            self._delete_file(video_file+audio_file)

    def _delete_file(self, filename):
        #first check for file existence
        if os.path.isfile(filename):
            os.remove(filename)
