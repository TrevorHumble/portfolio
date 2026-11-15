# Issue #0008: Flatland page: new demos, store banner and brand guide

**Type:** ready. **Category:** product feature.
**Depends on:** #0007.
**Blocks:** none.
**Touches:** `site/index.html` (Flatland page and the Blender tools Features grid), `site/img/` (11 `fl-demo-*.gif`, `flatland-banner.svg`, `flatland-brand-guide.png`), `BUILDLOG.md` (one line, at commit), this file.

## User story
As a visitor reading about Flatland on trevorhumble.com, I need the demos to show the add-on as it is today
(Blender 5.2, the current panel, the brand colors) and the page to carry the brand Trevor designed, so that
what I see is what I would get.

## Source
Owner request, 2026-11-15: re-record every GIF in the current panel and brand colors, add demos for the new
features (dashed strokes, layers, clipping paths, mirror editing, bevel on any curve, live text), replace the
hero with the store banner (the actual SVG from brand kit v3, `banner/flatland-banner.svg`), and show the
brand guide (`brand-guide.png`) on the page. The GIFs were recorded in Blender 5.2.4 with Flatland 0.2.0
(`TrevorHumble/flatland` at `462b7a1`).

## Acceptance criteria
1. **Given** the Flatland page, **When** it loads, **Then** its top image is `img/flatland-banner.svg`, byte-identical to the brand kit's `banner/flatland-banner.svg`.
2. **Given** the Demos grid, **When** it is read, **Then** it has 11 figures in this order: Shapes and pen, Type, Gradients, Strokes, Layers, Clipping paths, Shape Builder, Pathfinder, Bevel, Mirror editing, Export; each image is an 800 by 467 GIF in `site/img/` and each has alt text and a caption that describe what the GIF shows.
3. **Given** the Flatland page, **When** it is read, **Then** a Brand section between Demos and Planned features shows `img/flatland-brand-guide.png` (the brand kit's `brand-guide.png`, scaled to 2000 px wide) with alt text.
4. **Given** the Planned features lists, **When** they are read, **Then** they no longer list clipping masks, dashed and dotted strokes, mirror editing, bevel on any curve, live text in SVG, layers and groups, or text as editable curves (Convert to Curves ships); arrowheads, snapping, real text in PDF and artboards stay listed as planned.
5. **Given** the Features grid in the Blender tools section, **When** it is read, **Then** it keeps every item it had (Bevel corners becomes Bevel on any curve) and adds Layers and groups, Mirror editing, Clipping paths, Dashed strokes and Live text.
6. **Given** `site/index.html`, **When** searched, **Then** it contains no em dash.
7. **Given** the repo root, **When** `python tools/check_site_assets.py` runs, **Then** it reports `missing 0, unreferenced 0`, and `python tools/test_check_site_assets.py` ends with `site asset tests passed`.
8. **Given** the page at 1280 px and 390 px wide, **When** it loads, **Then** it raises no page error and has no horizontal scroll.

## Out of scope
The Blender tools section's workspace screenshot and the home card image stay as they are.
