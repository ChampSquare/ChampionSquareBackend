#!/bin/bash

# file name, don't forget to update file name in defaults.py
# if you change file name
# janus_post_process.sh

# Declare the binary path of the converter
januspprec_binary=~/janus10/bin/janus-pp-rec

# Contains the prefix of the recording session of janus e.g
input_file="$1"
output_file="$2"

# check video file exists or not
# quit if doesn't
if [ ! -f $input_file ]; then
    echo "Input file not found!"
    exit 1
fi

# Create temporary files that will store the individual tracks (audio and video)

echo "Converting mjr files to individual tracks ..."
$januspprec_binary $input_file $output_file

# finally check whether output file exists or not
# exit 1 -> if file doesn't exist -> Failed
if [ ! -f $output_file ]; then
    echo "Failed"
    exit 1
fi
echo "Done !"
exit 0