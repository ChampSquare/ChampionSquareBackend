#!/bin/bash

# video_post_process.sh

# Declare the binary path of the converter
januspprec_binary=~/workbench/janus/bin/janus-pp-rec

# Contains the prefix of the recording session of janus e.g
session_prefix="$1"
video_type = "$2"

# Create temporary files that will store the individual tracks (audio and video)
tmp_video=~/workbench/ChampSquare/ChampionSquareBackend/video_recordings/mjr-$RANDOM.webm

echo "Converting mjr files to individual tracks ..."
$januspprec_binary $session_prefix-video.mjr $tmp_video

tmp_audio=~/workbench/ChampSquare/ChampionSquareBackend/video_recordings/mjr-$RANDOM.opus
$januspprec_binary $session_prefix-audio.mjr $tmp_audio
ffmpeg -i $tmp_audio -i $tmp_video  -c:v copy -c:a opus -strict experimental $session_prefix

echo "Merging audio track with video ..."


echo "Done !"
exit 0