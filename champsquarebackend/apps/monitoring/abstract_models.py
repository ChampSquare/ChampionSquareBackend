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
    participant = models.ForeignKey('participate.Participant',
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
        return self.get_file_syntax()+".nfo"

    @classmethod
    def create_file_name_syntax(cls, record_id, video_type):
        return '{0}-{1}'.format(record_id, video_type)

    @classmethod
    def create_mjr_video_file_name(cls, record_id, video_type):
        return '{0}-video.mjr'.format(cls.create_file_name_syntax(record_id, video_type))

    @classmethod
    def create_mjr_audio_file_name(cls, record_id, video_type):
        return '{0}-audio.mjr'.format(cls.create_file_name_syntax(record_id, video_type))

    def get_file_syntax(self):
        return self.create_file_name_syntax(self.record_id, self.type)

    def get_mjr_audio_file_name(self):
        return self.create_mjr_audio_file_name(self.record_id, self.type)
    
    def get_mjr_video_file_name(self):
        return self.create_mjr_video_file_name(self.record_id, self.type)

    def create_processed_video_file_name(self):
        return '{0}.webm'.format(self.get_file_syntax())

    def get_processed_video_file_path(self):
        return settings.VIDEO_URL + self.create_processed_video_file_name()

    def create_processed_audio_file_name(self):
        return '{0}.opus'.format(self.get_file_syntax())

    def get_video_dir(self):
        return str(settings.ROOT_DIR)+ settings.SETTINGS_VIDEO_RECORD_FOLDER_NAME

    def create_record_file(self):
        file_name = self.get_info_file_name()
        video_rec_dir = self.get_video_dir()
        # todo : check whether dir exists or not
        # create first if it doesn't exist
        with open(video_rec_dir+file_name, 'w') as f:
            video_file_info = File(f)
            video_file_name = self.get_mjr_video_file_name()
            if self.type == 'webcam':
                audio_file_name = self.get_mjr_audio_file_name()
                video_file_info.write("[{0}]\nname = {1}-{3}\ndate = {2}\naudio = {5}\nvideo = {4}"
                                 .format(self.record_id, self.name, self.type, self.created_at, video_file_name, audio_file_name))
            else:
                video_file_info.write("[{0}]\n name = {1}-{3}\ndate = {2}\n video = {4}"
                                 .format(self.record_id, self.name, self.created_at, self.type, video_file_name))


    def delete_raw_files(self):
        # get video directory
        video_dir = self.get_video_dir()
        # each video has corresponding info file
        info_file = self.get_info_file_name()
        # get the video file name
        video_file = self.get_mjr_video_file_name()
        # delete info file
        self._delete_file(video_dir+info_file)
        #delete video file
        self._delete_file(video_dir+video_file)

        if self.type == 'webcam':
            # if type is webcam, there should be an audio file as well
            audio_file = self.get_mjr_audio_file_name()
            self._delete_file(video_file+audio_file)

    def _delete_file(self, filename):
        #first check for file existence
        if os.path.isfile(filename):
            os.remove(filename)
