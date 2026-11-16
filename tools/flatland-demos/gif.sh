#!/bin/bash
# gif.sh in.mkv out.gif [fps] [trim_start] [end_hold_s]
in=$1; out=$2; fps=${3:-12}; ss=${4:-0}
ffmpeg -v error -y -ss $ss -i "$in" -vf "fps=$fps,scale=800:467:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff:reserve_transparent=0[p];[b][p]paletteuse=dither=none:diff_mode=rectangle" "$out"
ls -la "$out" | awk '{print $5}'
