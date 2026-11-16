# Recording the Flatland demos by hand

**As the person recording the Flatland demo GIFs, I need every scene set up and a known way to capture and
convert, so a take is just the action itself and every GIF comes out the same size and quality.**

## The scenes file

`flatland-demo-scenes.blend` holds one scene per demo, in page order: 01 Shapes and pen to 11 Export. Pick a
scene from the scene menu at the top right of Blender. Every scene uses the same Paper page and framing, so
nothing moves when you switch. This guide is also inside the file as the text block `RECORDING NOTES`.

Before the first take in a session:

1. Install and enable Flatland (Blender 5.2 or later).
2. Click the Flatland tab in the sidebar (N). Blender does not save which tab is open.
3. Leave the colour view at Raw (Flatland's neutral view; the file sets it).
4. Turn tooltips off (Edit > Preferences > Interface > Tooltips), so none pop up mid-take.

Never save over the template while recording. Use File > Save As if you want to keep a take's end state.

## Changing the colours

The palette lives at the top of `build_scenes.py` (`ink`, `paper`, `accent`). Change the hex values and
rebuild:

```bash
blender --python build_scenes.py -- --logos <brand kit>/logo --fonts <brand kit>/fonts --out flatland-demo-scenes.blend --quit
```

Every scene is rebuilt from scratch with the new colours. The house shapes are the brand kit's own logo SVGs.

## What to record with

**OBS Studio** (free) for the capture, then the conversion below for the GIF. This keeps every GIF at the
same size, frame rate and colour handling.

- Source: Window Capture of Blender, with Capture Cursor on. Window Capture records only that window, so
  notifications and the desktop stay out ([Castr](https://castr.com/blog/obs-screen-recording/)).
- Crop the source to the 3D view (Alt-drag the source's edges in OBS) so the canvas is close to 1600 by 934,
  twice the GIF size.
- Settings > Output > Recording: format MKV (a crash cannot corrupt it, and OBS can remux it to MP4),
  rate control CQP at about 18 ([Compresto](https://compresto.app/blog/obs-recording-settings)).
- Settings > Video: 60 fps. Software is usually fine at 30, but the cursor is the star here, and 60 keeps
  it smooth before the GIF drops to 12.
- Windows display scaling at 100% for the Blender monitor, so the UI is crisp.

**ScreenToGif** (free, Windows) is the simpler choice if you would rather trim and export in one app: it
records a region straight to frames, lets you delete or retime frames, and exports an optimised GIF
([AlternativeTo](https://alternativeto.net/software/screentogif/about)). Its GIFs will not match the others'
palette and size exactly unless you set them to 800 by 467 at 12 fps.

## Turning a recording into a GIF

Send the MKV and it can be converted here, or run it yourself with ffmpeg (`winget install ffmpeg`). This is
the two-pass palette method: build a palette from the clip, then encode against it
([Mux](https://www.mux.com/articles/create-gifs-from-video-clips-with-ffmpeg)). The demos play back 1.5 times
faster than they were performed; drop `setpts=PTS/1.5,` to keep real time.

```powershell
ffmpeg -i take.mkv -vf "setpts=PTS/1.5,fps=12,scale=800:467:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle" fl-demo-NAME.gif
```

For the Gradient demo use `max_colors=256:stats_mode=full` and `dither=bayer:bayer_scale=3`, or the gradient
bands. Name each file as the page expects: `fl-demo-draw`, `-type`, `-gradient`, `-stroke`, `-layers`,
`-clip`, `-shape-builder`, `-pathfinder`, `-bevel`, `-mirror`, `-export`.

## How to move

`HUMAN-MOTION.md` has the research. For a hand that already moves like a hand, the reminders are about
pacing: pause about half a second after each result so a viewer can take it in, let repeats get a little
quicker, and keep each take to about 8 to 15 seconds after the 1.5 times speed-up.

## The takes

**01 Shapes and pen.** Shape tools from the toolbar flyout: drag a rectangle, a circle (Shift for even), a
star and a hexagon across the top half. Set each one's colour if you like (new shapes start Ink). Then the
Pen: click, then click-drag a few points into an uneven wave along the bottom, and Tab out.

**02 Type.** Text tool, click on the page, Tab, delete "Text", type "Flatland", Tab. Open the font list,
search "grav", pick Gravitas One. Then small caps, spacing 1.2 and slant 0.2.

**03 Gradient.** Switch the viewport to Material Preview first (Z, or the header) and let it settle. Open
the fill's settings, choose linear (the Ink, Paper, Accent stops are already set), turn it by its end
handle, slide the middle stop, then choose radial.

**04 Strokes.** Open the stroke's settings. Width 0.18, round corners, round caps. Tab, click the left peak,
Alt S and pull out (it swells there), A, Alt S and pull a little (the whole stroke grows), then Ctrl Z four
times (each selection is an undo step too) and Tab. Tick Dashed Line, dash 0.35, gap 0.25, Shift-drag Phase
so the dashes travel, then dash 0 for dots.

**05 Layers.** Drag the Square row to the top of the layer list (the square comes to the front). Click the
Sun, Shift-click the Star, press the new group button, double-click the group and name it "Sky".

**06 Clipping paths.** With Window selected, Make Clipping Path, Crops: Stripes. Then G and move the window
up, down and across so the stripes slide inside it.

**07 Shape Builder.** A to select all three circles, the Shape Builder tool, drag through the pieces to
merge, Enter.

**08 Pathfinder.** Four pairs, left to right: select a pair (click, Shift-click; vary the order, box-select
one), then Add, Subtract, Intersect, Exclude in turn.

**09 Bevel.** Start with the cursor on the paper to the right of the house, so the pull line shows on the
white. Tab, A, Ctrl B, pull out and back to taste, click, Tab.

**10 Mirror editing.** Tab, Alt A, turn on Mirror X in the header. Click the right eave and G it out, then
a foot, then the peak (it stays on the middle line). Tab.

**11 Export.** Click the globe beside Export to preview in a browser. Record the browser part separately with
the browser in full screen (F11), zoomed in on the artwork, and select the word "Flatland" to show it is
real text. Crop out any browser chrome before converting.
