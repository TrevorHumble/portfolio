#!/bin/bash
# Records every demo and writes the GIFs to $OUT. Usage: run_all.sh [demo ...]
H=$(cd "$(dirname "$0")" && pwd); OUT=${OUT:-$H/final}; mkdir -p "$OUT" "$H/rec"
cd "$H"
demos=${@:-"draw type gradient stroke layers clip builder pathfinder bevel mirror export"}
for d in $demos; do
  echo "== $d"
  python3 demo_$d.py > "rec/$d.log" 2>&1 || { echo "FAILED $d"; tail -5 "rec/$d.log"; continue; }
  case $d in
    builder) name=shape-builder; src=rec/shape-builder.mkv ;;
    *) name=$d; src=rec/$d.mkv ;;
  esac
  python3 cursor.py "$src" "${src%.mkv}.trace.json" "rec/${d}_c.mkv" >/dev/null && src="rec/${d}_c.mkv"
  if [ "$d" = export ]; then
    html=$(grep -o '/[^ ]*flatland-preview-[0-9a-f]*\.html' "rec/$d.log" | tail -1)
    mkdir -p web; cp "$html" web/preview.html; python3 fix_preview.py web/preview.html
    rm -rf web/frames ex; node browser_part.js "$H/web" "$H/web/frames" >/dev/null
    mkdir ex; ffmpeg -v error -i "$src" -vf "setpts=PTS/1.5,fps=12" ex/a%04d.png
    i=$(ls ex | wc -l); for f in web/frames/*.png; do i=$((i+1)); cp "$f" ex/a$(printf %04d $i).png; done
    ffmpeg -v error -y -framerate 12 -i ex/a%04d.png -c:v libx264rgb -crf 0 -preset ultrafast rec/export_f.mkv
    ./gif.sh rec/export_f.mkv "$OUT/fl-demo-export.gif" 12
  else
    ffmpeg -v error -y -i "$src" -vf "setpts=PTS/1.5" -c:v libx264rgb -crf 0 -preset ultrafast "rec/${d}_f.mkv"
    if [ "$d" = gradient ]; then ./gifhq.sh "rec/${d}_f.mkv" "$OUT/fl-demo-$name.gif" 12; else ./gif.sh "rec/${d}_f.mkv" "$OUT/fl-demo-$name.gif" 12; fi
  fi
  ./sheet.sh "$OUT/fl-demo-$name.gif" "$OUT/sheet-$name.png" 8 >/dev/null
done
echo ALLDONE
