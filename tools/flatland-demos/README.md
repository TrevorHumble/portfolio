# Flatland demo recorder

**Recording by hand?** Open `flatland-demo-scenes.blend` (one scene per demo, ready to record) and follow
`RECORDING.md`. `build_scenes.py` rebuilds that file, for instance after a colour change.

Records the Flatland demo GIFs on the portfolio's Flatland page (`site/img/fl-demo-*.gif`) by driving a
real Blender window: Blender runs on a virtual display, `xdotool` moves the mouse and types, and `ffmpeg`
records the screen. Each `demo_*.py` is one GIF.

## Setup (Linux)

1. Install `xvfb`, `xdotool`, `ffmpeg`, `imagemagick`, Node with Playwright (for the Export demo's browser
   half), and Blender 5.2 or later.
2. Build Flatland from `TrevorHumble/flatland` (`python3 tools/build_addon.py`), copy the built package, and
   on a software-rendered display (Xvfb, Mesa) run `python3 patch_flatland_for_xvfb.py <copy>/flatland`
   before installing the copy (`blender --command extension install-file -r user_default -e <zip>`). The
   patch file says why. On a machine with a real GPU, skip it.
3. Copy the brand kit's `fonts/*.ttf` into `~/.local/share/fonts` and run `fc-cache -f`, so the Type demo
   finds Gravitas One.
4. Start the display and set the paths:

```bash
Xvfb :99 -screen 0 1600x1012x24 &
```

```bash
export DISPLAY=:99 BLENDER=/path/to/blender FLATLAND_LOGO_DIR=/path/to/flatland-brand-v5/logo FLATLAND_FONT_DIR=/path/to/flatland-brand-v5/fonts
```

## Run

```bash
./run_all.sh
```

Or name demos: `./run_all.sh stroke layers`. GIFs land in `final/` with a contact sheet per demo. Each demo
restarts Blender, so one bad take cannot spoil the next.

## Things to know

- The system cursor is hidden while recording; `cursor.py` draws a standard arrow at every logged mouse
  position afterwards, since Xvfb only offers the X11 'X'.
- Cursor motion follows `HUMAN-MOTION.md`: why moves curve, ease and overshoot the way they do, with sources.
- Click positions are fixed pixels for a 1600x1012 window with Blender's default theme. A Flatland panel
  change can move a button; when a take goes wrong, check its contact sheet first.
- Colors are Ink, Paper and Scarlet Ibis from brand kit v5 (`setup.py`). The house shapes are the kit's
  own logo SVGs, imported as plain Blender curves (`import_logo` in `setup.py`).
- The Gradient demo uses Material Preview, so its first run waits for Blender to compile shaders.
- The Layers demo stops before bringing a group forward: with Flatland 0.2.0 a group brought forward in
  the layer list drops back behind on the next deselect.
