# Issue #0009: Flatland page in brand v5: screenshot hero, brand at the bottom, demos re-recorded, recording kit

**Type:** ready. **Category:** product feature.
**Depends on:** #0008.
**Blocks:** none.
**Touches:** `site/index.html` (home card, Blender tools section, Flatland page), `site/img/` (11 `fl-demo-*.gif`; `flatland-workspace-v5.jpg` and `flatland-banner-v5.svg` added; `flatland-brand-guide.png` replaced; `flatland-banner.svg`, `flatland-cube-v3.svg` and `flatland-workspace-v3.jpg` removed), `tools/flatland-demos/` (new), `BUILDLOG.md` (one line, at commit), this file.

## User story
As a visitor reading about Flatland on trevorhumble.com, I need the site in the brand Trevor settled on (kit
v5: Ink, Paper and Scarlet Ibis #E05450) with Flatland itself as the first thing I see, so that the page
shows the tool and its real brand. As Trevor, I need a scenes file and a guide to record the demos myself,
and the automated recorder kept for quick re-renders.

## Source
Owner direction, 2026-11-15 and 2026-11-16, reviewed round by round on a private preview: hero back to a
Blender screenshot of his banner file; brand section at the bottom of the Flatland page; both home-page
Flatland images replaced; demos re-recorded with real logo SVGs and human-like cursor motion; then a
one-file, scene-per-demo template for recording by hand, rebuilt in brand kit v5. The owner approved
pushing this version on 2026-11-16 ("close enough"); hand-recorded GIFs in v5 follow in a later change.

## Acceptance criteria
1. **Given** the Flatland page and the home page's Blender tools section, **When** they load, **Then** both show `img/flatland-workspace-v5.jpg` (1680 by 952, `data-zoom`), a screenshot of the banner file open in Blender with the Flatland panel, whose background is #E05450.
2. **Given** the home page's Flatland card, **When** it loads, **Then** it shows `img/flatland-banner-v5.svg`, byte-identical to brand kit v5's `banner/flatland-banner.svg`, on an #E05450 background.
3. **Given** `site/img/`, **When** listed, **Then** `flatland-banner.svg`, `flatland-cube-v3.svg`, `flatland-workspace-v3.jpg` and any `-v4` image are absent.
4. **Given** the Flatland page, **When** it is read, **Then** the Brand section is its last section and shows kit v5's `brand-guide.png` scaled to 2000 px wide, with alt text naming Scarlet Ibis.
5. **Given** the 11 demo GIFs, **When** they are viewed, **Then** each is 800 by 467, uses only Ink, Paper and Scarlet Ibis (the v4 value, #DA5B47, until the hand recordings replace them), shows a standard arrow cursor, and the Bevel, Mirror editing and Export demos show the kit's logo shapes. Each GIF's alt text and caption describe what it shows.
6. **Given** `tools/flatland-demos/`, **When** it is read, **Then** `README.md`, `RECORDING.md`, `HUMAN-MOTION.md`, `build_scenes.py` and `flatland-demo-scenes.blend` exist; the .blend holds 11 scenes named `01 Shapes and pen` to `11 Export` with the accent #E05450; no file holds a path to a session scratch folder; generated output is gitignored.
7. **Given** the repo root, **When** `python tools/check_site_assets.py` runs, **Then** it reports `missing 0, unreferenced 0`; `python tools/test_check_site_assets.py` ends with `site asset tests passed`; `site/index.html` keeps CRLF line endings and has no em dash.
