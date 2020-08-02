from django.conf import settings

from champsquarebackend.core.utils import run_bash_script
from champsquarebackend.core.loading import get_model

VideoRecord = get_model('monitoring', 'VideoRecord')

def janus_post_process_file(input_file, output_file):
    """
        python function wrapper of janus post process script
    """
    command = ["bash",
               settings.SETTINGS_JANUS_POST_PROCESS_SCRIPT,
               input_file,
               output_file
               ]
    output = run_bash_script(command)
    if 'Success' in output.get('status'):
        return True
    return False

def merge_audio_video(input_video_file, input_audio_file, output_file):
    """
        python functional wrapper of video-audio merge bash script
        which uses ffmpeg internally
    """
    command = ["bash",
               settings.SETTINGS_AUDIO_VIDEO_MERGE_SCRIPT,
               input_video_file,
               input_audio_file,
               output_file
               ]
    output = run_bash_script(command)
    if 'Success' in output.get('status'):
        return True
    return False

def post_process_video(video_record_id):
    """
        post processes janus mjr file to convert to webm
        
        video of type "webcam" has separate audio and video files
        which requires to convert both of them to convert to webm and
        opus format resp. and then merge them together

        video of type "screen" doesn't need merging as it has only video file

        args: video_record - instance of `champsquarebackend.apps.monitoring.VideoRecord`
    """
    video_record = VideoRecord.objects.get(id=video_record_id)
    if video_record is None:
        return False
    video_type = video_record.type
    video_media_root = settings.VIDEO_ROOT
    input_video_file = video_record.get_video_dir() + video_record.get_mjr_video_file_name()
    output_file = video_record.create_processed_video_file_name()
    output_video_file = video_record.get_video_dir() + output_file

    if video_type == 'screen':
        # this will create output file in media video directory
        output_video_file = video_media_root + output_file
        
    response = janus_post_process_file(input_video_file, output_video_file)
    
    if video_type == 'webcam' and response:
        input_audio_file = video_record.get_video_dir() + video_record.get_mjr_audio_file_name()
        output_audio_file = video_record.get_video_dir() + video_record.create_processed_audio_file_name()
        response = janus_post_process_file(input_audio_file, output_audio_file)
        # now merge video and audio files
        if response:
            response = merge_audio_video(output_video_file, output_audio_file, video_media_root+output_file)
    
    return response, video_record_id
