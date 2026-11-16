#!/bin/bash
# sheet.sh in.gif out.png [n]  -> tile of n evenly spaced frames
in=$1; out=$2; n=${3:-8}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
ffmpeg -v error -y -i "$in" -vf "fps=$n/$d,scale=400:-1,tile=2x$(( (n+1)/2 ))" -frames:v 1 "$out"
echo "dur=$d"
