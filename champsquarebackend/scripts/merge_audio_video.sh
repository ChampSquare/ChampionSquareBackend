#!/bin/bash

# file name, don't forget to update file name in defaults.py
# if you change file name
# merge_audio_video.sh


video_file="$1"
audio_file="$2"
output_file="$3"

# check video file exists or not
# quit if doesn't
if [ ! -f $video_file ]; then
    echo "Video input file not found!"
    exit 1
fi

# check audio file exists or not
# quit if doesn't
if [ ! -f $audio_file ]; then
    echo "audio input file not found!"
    exit 1
fi

# Create temporary files that will store the individual tracks (audio and video)

echo "Merging audio and video files ..."
ffmpeg -i $audio_file -i $video_file  -c:v copy -c:a opus -strict experimental $output_file -y

# finally check whether output file exists or not
# exit 1 -> if file doesn't exist -> Failed
if [ ! -f $output_file ]; then
    echo "Failed"
    exit 1
fi
# delete input files
rm $audio_file
rm $video_file
echo "Done !"
exit 0