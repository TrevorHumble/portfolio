#!/bin/bash
in=$1; out=$2; fps=${3:-12}
ffmpeg -v error -y -i "$in" -vf "fps=$fps,scale=800:467:flags=lanczos,split[a][b];[a]palettegen=max_colors=256:stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle" "$out"
ls -la "$out" | awk '{print $5}'
