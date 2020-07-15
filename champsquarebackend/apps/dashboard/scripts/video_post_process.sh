#!/bin/bash

# video_post_process.sh

# Declare the binary path of the converter
januspprec_binary=~/workbench/janus/bin/janus-pp-rec

# Contains the prefix of the recording session of janus e.g
session_prefix="$1"

# Create temporary files that will store the individual tracks (audio and video)
tmp_video=~/workbench/ChampSquare/ChampionSquareBackend/video_recordings/mjr-$RANDOM.mp4
tmp_audio=~/workbench/ChampSquare/ChampionSquareBackend/video_recordings/mjr-$RANDOM.opus

echo "Converting mjr files to individual tracks ..."
$januspprec_binary $session_prefix-video.mjr $tmp_video
$januspprec_binary $session_prefix-audio.mjr $tmp_audio

echo "Merging audio track with video ..."

# ffmpeg -i $tmp_audio -i $tmp_video  -c:v copy -c:a opus -strict experimental $session_prefix

echo "Done !"
exit 0