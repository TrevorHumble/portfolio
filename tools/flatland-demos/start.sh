#!/bin/bash
# (Re)starts Blender on the virtual display with the command poller (boot.py) loaded.
# Needs: BLENDER (path to Blender 5.2+), FLATLAND_LOGO_DIR (brand kit logo/), FLATLAND_FONT_DIR
# (brand kit fonts/), and an X display at $DISPLAY sized 1600x1012 (see README.md).
H=$(cd "$(dirname "$0")" && pwd)
: "${BLENDER:?set BLENDER to the Blender executable}"
export DISPLAY=${DISPLAY:-:99} XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/xdg}
mkdir -p "$XDG_RUNTIME_DIR"; chmod 700 "$XDG_RUNTIME_DIR"
# a virtual display that died (a machine restart kills it) is started again here
if ! xdotool getmouselocation >/dev/null 2>&1; then
  rm -f "/tmp/.X${DISPLAY#:}-lock" "/tmp/.X11-unix/X${DISPLAY#:}"
  (setsid Xvfb "$DISPLAY" -screen 0 1600x1012x24 >/dev/null 2>&1 &)
  sleep 2
fi
pkill -f "$BLENDER" ; sleep 1
rm -f "$H/ready"
HDIR="$H" "$BLENDER" --window-geometry 0 0 1600 1012 --python "$H/boot.py" > "$H/bl.log" 2>&1 &
for i in $(seq 1 60); do sleep 1; [ -f "$H/ready" ] && break; done
