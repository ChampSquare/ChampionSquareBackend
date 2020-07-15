from subprocess import Popen, PIPE, STDOUT

from django.conf import settings

def post_process_video(file_name):
    video_rec_dir = str(settings.ROOT_DIR)+ settings.SETTINGS_VIDEO_RECORD_FOLDER_NAME
    
    command = ["bash",
               "champsquarebackend/apps/dashboard/scripts/video_post_process.sh",
               video_rec_dir+file_name,
               ]
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        output = process.stdout.read()
        exitstatus = process.poll()
        if (exitstatus==0):
            return {"status": "Success", "output":str(output)}
        else:
            return {"status": "Failed", "output":str(output)}
    except Exception as e:
        return {"status": "failed", "output":str(e)}