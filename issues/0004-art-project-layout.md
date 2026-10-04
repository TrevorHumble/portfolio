# Issue #0004: Video hero with a picture column, and masonry pictures, on art project pages

**Type:** ready. **Category:** product feature.
**Depends on:** #0003.
**Blocks:** none.
**Touches:** `site/index.html` only in: the `/* Art pages */` CSS block; one `.art-about .lede` selector added to the existing `.fl-head .lede` rule (so the two share one declaration); the `renderProject` function; one added line in `route()`; and new helper functions, one `var shownProject = null` and one `window` `resize` listener (registered once at load), all placed beside `renderProject` inside the same page-script function. Also `issues/0004-art-project-layout.md` (this file) and `BUILDLOG.md` (one line).

## User story
As a visitor to the portfolio (a hiring manager or collaborator) opening an art project, I need the video
up front with its pictures beside it, and picture-only projects laid out compactly, so that I can see the
work without scrolling through one long ragged column.

## Background
Today `renderProject` in `site/index.html` puts every video and every picture into one `.art-pics`
column, left-aligned, each picture at its own width (the Digital page is about 8,500px tall at 1440px wide).
The owner approved this layout on 2026-10-04 from mockups:

- **Projects with at least one playable video** (`vids = p.videos.filter(function (v) { return embedUrl(v); })` is non-empty): the header stays as it is (back link,
  Type/Pictures bar, title, description, tools). Under it, a **hero**: the video large on the left and a
  narrow **picture column** on the right. The column holds only pictures (never videos, never play
  icons). Its control bar is "style 2": a 2px top rule; the label `Pictures`; a counter like `01/06`; and
  two small square outlined buttons (up and down chevrons) at the right end. There is no bottom bar.
  Clicking a picture opens the existing zoom dialog. A project with more than one video gets a row of clip
  buttons under the video (`Clips 01 02 03 ...`); clicking one loads that clip into the one player.
- **Projects with no playable video** (`vids` empty): pictures in a masonry layout (equal-width columns, each picture at its full
  shape, each placed in the currently shortest column, in data order). Pictures sit in the page column by
  column, so keyboard and screen-reader order follows the columns (for Digital: 1, 5, 8, 2, ...); this is
  accepted. The picture counter reads `NN/NN` whenever the column is scrolled to its end, so it can jump
  from, say, `03/06` to `06/06`; this is accepted.

- **Phones (below 900px), approved 2026-10-04 from a phone mockup:** on video projects the video (and its
  clip buttons) sits right under the title, above the description and tools, so it is visible without
  scrolling a full screen; the picture column becomes a sideways-swiping row under it, with no up/down
  buttons, and its bar reads `Pictures` followed by the plain picture count (e.g. `Pictures 6`). On
  desktop (900px and wider) the description and tools stay above the video, as sketched.

Out of scope: the home page, the Design index page (`#art-all`), the `art-data` JSON, images, and any
other page.

## Acceptance criteria
All browser checks use Chromium driven by Playwright, against `site/` served with
`python3 -m http.server` from inside `site/`, after waiting 1500 ms for the page to settle. "Desktop" is a
1440x900 viewport; "phone" is 390x844. `kQY4zn` is Unproduced Music Video (6 videos, 6 pictures),
`DAnGqo` is Liminal Fields (1 video, 4 pictures), `kQ5ZDn` is Digital (0 videos, 10 pictures),
`zPkN3Q` is Realistic Pignite (0 videos, 4 pictures).

1. **Given** the repo after this change, **When** `python tools/check_site_assets.py` is run from the repo
   root, **Then** its last line is exactly `referenced 134, missing 0, unreferenced 0` and it exits `0`;
   and `python tools/test_check_site_assets.py` ends with `site asset tests passed` and exits `0`.
2. **Given** desktop at `#art-kQY4zn`, **When** the page is read, **Then** `#art-view` contains exactly one
   `iframe`, inside `.art-stage`, whose `src` contains `player.vimeo.com/video/952888961`; `.art-side`
   contains exactly 6 `img[data-zoom]` and no `iframe`; `.art-side .art-count` text is `01/06`; the
   `.art-up` button is `disabled` and the `.art-down` button is not; the `.art-clips button` texts are
   `01` to `06` in order, the `01` button has `aria-pressed="true"` and the other five `aria-pressed="false"`.
3. **Given** desktop at `#art-kQY4zn`, **When** the `.art-clips button` whose text is `03` is clicked,
   **Then** there is still exactly one `iframe` in `#art-view`, its `src` contains
   `player.vimeo.com/video/952923739`, and that button has `aria-pressed="true"` while the other five have
   `aria-pressed="false"`, and the iframe `title` is `Unproduced Music Video, clip 3`.
4. **Given** desktop at `#art-kQY4zn`, **When** `.art-down` is clicked and 1000 ms pass, **Then**
   `.art-side-list` has `scrollTop > 0`, `.art-up` is not `disabled`, and `.art-count` text is `02/06`;
   and when `.art-down` is then clicked (waiting 1000 ms each time) until it is `disabled`, `.art-count`
   text is `06/06`.
5. **Given** desktop at `#art-kQY4zn`, **When** bounding boxes are read, **Then** `.art-side` is 240px wide
   (within 1px), its top equals the `.art-stage .vid` top and its bottom equals the `.art-stage .vid`
   bottom (each within 1px), and its left edge is to the right of the `.vid` right edge.
6. **Given** desktop at `#art-DAnGqo`, **When** the page is read, **Then** there is no `.art-clips` element,
   there is exactly one `iframe` (its `src` contains `youtube-nocookie.com/embed/Qlhx3Ls0iuk`), and
   `.art-side` contains exactly 4 `img[data-zoom]`.
7. **Given** desktop at `#art-kQ5ZDn`, **When** the page is read, **Then** there is no `iframe` and no
   `.art-side`; `.art-pics` contains exactly 10 `img[data-zoom]`; their rendered widths are all equal
   (within 1px); and their left edges take exactly 3 distinct values (rounded to whole px).
8. **Given** desktop at `#art-zPkN3Q`, **When** the page is read, **Then** the 4 `.art-pics img` left
   edges take exactly 2 distinct values.
9. **Given** desktop at `#art-kQ5ZDn`, **When** the `.art-pics` figures are read in DOM order per column,
   **Then** reconstructing the placement (each picture `k`, in data order, goes to the column whose summed
   `h/w` ratio so far is smallest, ties to the leftmost) gives exactly the column each picture is
   rendered in: left to right, the columns hold pictures `1, 5, 8` | `2, 6, 10` | `3, 4, 7, 9`.
10. **Given** phone at `#art-kQY4zn`, **When** bounding boxes are read, **Then** the `.art-side` top is at or
    below the `.art-stage .vid` bottom, `.art-side-list` has `scrollWidth > clientWidth`, and `.art-up`
    and `.art-down` are not displayed (`offsetParent === null`), and the first `.art-side-list figure` rendered width equals
    0.62 x `.art-side-list` `clientWidth` (within 1px), and `.art-count` is displayed with text `6`.
11. **Given** desktop at `#art-kQY4zn`, **When** the first `.art-side img` is clicked, **Then** `dialog#zoom`
    has the `open` attribute and `#zoom-img` `src` ends with `img/art/kQY4zn-1.jpg`.
12. **Given** desktop, **When** `/` is loaded with `page.goto` and then each of the 16 project pages is
    loaded in turn with `page.goto` of `/#art-<id>` (every `id` in `art-data`), **Then** no `console`
    message of type `error` and no `pageerror` is recorded, except failed loads of `youtube-nocookie.com`,
    `vimeo.com`, `fonts.googleapis.com` or `fonts.gstatic.com` resources and the `favicon.ico` 404 from
    `http.server` (the test sandbox cannot reach those hosts, and the unchanged page logs the same).
13. **Given** desktop at `#art-kQ5ZDn`, **When** the viewport is resized to 800x900 and 500 ms pass,
    **Then** `.art-pics .col` count is 2; **When** it is then resized to 500x900 and 500 ms pass, **Then**
    it is 1; **When** the page then navigates to `#art-kQY4zn`, is resized back to 1440x900 and 500 ms
    pass, **Then** there is no `.art-pics` element, exactly one `iframe`, `.art-down` is not `disabled`, `.art-up` is
    `disabled`, and `.art-count` text is `01/06`.
14. **Given** desktop at `#art-8bJnLQ` (Pokemon: Freedom and Revolution, 1 video, 3 pictures), **When** the
    viewport is resized to 1000x900 and 500 ms pass, **Then** `.art-down` is not `disabled` and `.art-count`
    text is `01/03`; **When** it is then resized back to 1440x900 and 500 ms pass, **Then** `.art-down` is
    `disabled` and `.art-count` text is `03/03`.
15. **Given** phone at `#art-kQY4zn`, **When** bounding boxes are read, **Then** the `.art-title` bottom is
    at or above the `.art-stage .vid` top, and the `.art-stage .vid` bottom is at or above the `#art-view .lede` top.
16. **Given** desktop at `#art-kQY4zn`, **When** bounding boxes are read, **Then** the `#art-view .lede`
    bottom is at or above the `.art-stage .vid` top.
17. **Given** desktop at `#art-kQY4zn`, **When** `history.length` is read, then the `.art-clips button` with
    text `03` and then the one with text `05` are clicked (500 ms after each), **Then** `history.length`
    equals the value read before the clicks, and `.art-stage iframe` count is 1.

## Implementation plan
1. In `site/index.html`, inside the `/* Art pages */` CSS block, replace the three `.art-pics` rules with
   masonry rules: `.art-pics { display: flex; gap: clamp(12px, 1.6vw, 18px); align-items: flex-start; }`,
   `.art-pics .col { flex: 1 1 0; min-width: 0; display: grid; gap: clamp(12px, 1.6vw, 18px); }`,
   `.art-pics figure { margin: 0; }`, `.art-pics img { display: block; width: 100%; height: auto;
   border-radius: 4px; background: var(--surface); }`. Keep the existing `.vid` rules.
2. Add hero CSS in the same block, using the page's existing tokens (`--ink`, `--ink-2`, `--mono`,
   `--surface`):
   - `.art-hero` is a grid: one column with `row-gap: 12px` below 900px (so the clip row does not touch the
     picture bar); at `min-width: 900px`, `row-gap: 0; column-gap: 14px; align-items: start`, and only a
     hero that has a picture column (`hero()` adds the class `has-side` when it renders the aside) gets
     `grid-template-columns: minmax(0, 1fr) 240px`, so a video project without pictures keeps a full-width
     video.
   - `.art-side` at 900px+: `position: relative; align-self: stretch; grid-column: 2; grid-row: 1`, with an
     inner `.art-side-in` that is `position: absolute; inset: 0; display: flex; flex-direction: column`,
     so the column is exactly as tall as the video and never taller. Below 900px `.art-side-in` is static.
   - `.art-bar`: `display: flex; align-items: center; gap: 10px; height: 34px; border-top: 2px solid
     var(--ink); margin-bottom: 8px; font: 500 0.7rem/1 var(--mono); letter-spacing: 0.1em;
     text-transform: uppercase`. `.art-count` is `color: var(--ink-2)`. A spacer `.art-bar .sp { flex: 1 }` pushes the buttons right.
   - `.art-up`, `.art-down`: 26x26px, `border: 1px solid var(--ink); border-radius: 2px; background:
     transparent; color: var(--ink); display: grid; place-items: center; cursor: pointer; padding: 0`;
     `:disabled` is `opacity: 0.25; cursor: default`. Each holds an inline SVG chevron (16x16, stroke
     `currentColor`, stroke-width 2). Below 900px both buttons are `display: none` (`.art-count` stays visible).
   - `.art-side-list` at 900px+: `flex: 1; min-height: 0; overflow-y: auto; display: flex;
     flex-direction: column; gap: 10px; scrollbar-width: none` (plus `::-webkit-scrollbar { display:
     none }`). Below 900px: `display: flex; flex-direction: row; gap: 10px; overflow-x: auto; scroll-snap-type: x mandatory`, items
     `flex: 0 0 62%; scroll-snap-align: start`.
   - `.art-side-list figure { margin: 0 }`; at 900px+ add `.art-side-list figure { flex: none }`; below 900px
     the figures take `flex: 0 0 62%` (the 62% rule must win below 900px); `.art-side-list img { display: block; width: 100%;
     aspect-ratio: 16 / 9; object-fit: cover; border-radius: 3px; background: var(--surface) }`.
   - `.art-clips` (left column, under the video): `display: flex; gap: 18px; align-items: center;
     margin-top: 10px; font: 500 0.7rem/1 var(--mono); letter-spacing: 0.1em; text-transform: uppercase`.
     Its label is `color: var(--ink-2)`; its buttons are `background: none; border: 0; border-bottom: 2px
     solid transparent; padding: 6px 0; color: var(--ink-2); font: inherit; cursor: pointer`, and
     `[aria-pressed="true"]` is `color: var(--ink); border-bottom-color: var(--ink)`. At 900px+ it sits in
     `grid-column: 1; grid-row: 2`.
   - `.art-hero` gets `margin-top: 8px`; `.art-stage { min-width: 0 }`; `.art-stage .vid { margin: 0 }`
     (the page has no global `figure` margin reset, and the browser default would shrink the video).
3. In `renderProject`, keep the header markup as now for projects with no playable video. Build the pictures as `figure > img[data-zoom]` with
   the same `src`, `alt`, `width`, `height` and lazy-loading rule as today.
   - Compute `vids = playable(p)`; every clip index, clip
     count and clip button below refers to `vids`, not `p.videos`.
   - **When `vids` is non-empty**, split the header: `<div class="art-top">` holds (a) `<header class="fl-head
     art-head">` with only the Type/Pictures bar and the `h1.art-title`, (b) `<div class="art-about">` with
     the `p.lede` and the tools block exactly as rendered today, and (c) the hero below. CSS (in step 2's
     block): `.art-top { display: flex; flex-direction: column }`, `.art-top > .art-head { padding-bottom:
     14px }`, `.art-about { display: grid; gap: 14px; padding-bottom: clamp(24px, 4vw, 40px) }`; below
     900px `.art-top > .art-hero { order: 1; margin-bottom: clamp(24px, 4vw, 40px) }` and `.art-top >
     .art-about { order: 2 }`; at 900px+ DOM order applies (header, about, hero). The hero is:
     `<div class="art-hero">` containing `<div class="art-stage">` + one `figure.vid` with one `iframe` for
     `vids[0]` (same attributes as today) + `</div>`, then, only if `vids.length >= 2`, `<div class="art-clips"
     role="group" aria-label="Clips"><span>Clips</span>` plus one `<button type="button">` per clip
     labelled with its two-digit number (`01`, `02`, ...), with `aria-pressed="true"` on `01` and
     `aria-pressed="false"` on the rest, then `</div>`, then
     `<aside class="art-side" aria-label="Pictures"><div class="art-side-in"><div class="art-bar"><span>
     Pictures</span><span class="art-count"></span><span class="sp"></span><button type="button"
     class="art-up" aria-label="Previous pictures">…</button><button type="button"
     class="art-down" aria-label="Next pictures">…</button></div><div class="art-side-list">` + the
     picture figures + `</div></div></aside></div>`. If `p.imgs` is empty, omit the `aside` entirely. The
     counter text and both buttons' `disabled` states are set only by the picture-column update function,
     which runs synchronously at the end of the render, so the markup carries no initial values for them.
     Each clip button carries its own `data-src` (its embed URL) and `data-title` (its iframe title), and
     the click handler reads those attributes rather than looking the clip up by position. NN is the picture count, two-digit. Do not render an
     `.art-pics` block for these projects.
   - Clip buttons: on click, replace the iframe element with a fresh copy (`var n = ifr.cloneNode();
     n.src = embedUrl(vids[k]); n.title = <same name rule as today, using vids.length>; ifr.replaceWith(n);
     ifr = n;`). Never assign `src` on the existing iframe, because that pushes a browser-history entry and
     hijacks the Back button. Then set `aria-pressed="true"` on the clicked button and
     `aria-pressed="false"` on every other clip button.
   - Shared helpers beside `renderProject` (so nothing is written twice): `playable(p)` returns
     `p.videos.filter(function (v) { return embedUrl(v); })`; `pad(n)` returns the two-digit string;
     `picFig(p, im, k)` returns one picture's `figure > img[data-zoom]` markup (used by both the picture
     column and the masonry helper).
   - Picture column: put the update logic in a function beside `renderProject` that reads the current
     `.art-side-list` from `artView` and returns at once when there is none. `step` = first figure's `offsetHeight` + the list's computed `row-gap` (read with `getComputedStyle`, never restated in JS), recomputed on every call. `.art-down` / `.art-up` call
     `list.scrollBy({ top: ±step, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" })`. On the list's `scroll` event (and once after
     render): when the up/down buttons are not displayed (`.art-down` `offsetParent === null`, i.e. the phone layout the
     CSS chose; the 900px breakpoint is never restated in JS) set `.art-count` to the plain picture count
     (e.g. `6`) and stop; otherwise disable `.art-up` when `scrollTop <= 1`, disable `.art-down` when
     `scrollTop + clientHeight >= scrollHeight - 1`, and set `.art-count` to `NN/NN` when `.art-down` is
     disabled, otherwise to the two-digit `Math.round(list.scrollTop / step) + 1` (capped at NN) + `/NN`.
   - **When `vids` is empty**, render `<div class="art-pics">` holding N `<div class="col">`
     elements, N = `colCount(p)`: 1 when `window.innerWidth < 600` or the project has 1 picture; else 2 when
     the project has 2-4 pictures or `window.innerWidth < 900`; else 3. Both the masonry helper and the
     `resize` listener call `colCount(p)`; the rule exists in that one function only. Place pictures in data order, each into the column whose summed
     `h / w` is smallest so far (ties go to the leftmost). Put this in a helper beside `renderProject`
     that returns the `.art-pics` HTML for a project.
   - At the start of `renderProject`, set `shownProject = p`. In `route()`, set `shownProject = null` when
     the view is not `project` (one added line). Once at load, outside `renderProject`, register one
     `window` `resize` listener that acts on what is rendered, never re-deciding the layout rule: when
     `shownProject` is set it calls the picture-column update function (a no-op without a picture column),
     and if an `.art-pics` element exists and `colCount(shownProject)` differs from its number of columns,
     replaces it with the masonry helper's output and calls `arm(artView)`. (This supersedes the
     `playable`-based branching described next.) When `shownProject` is set: if `playable(shownProject)` is empty, compute
     `colCount(shownProject)` and, only if it differs from the number of `.art-pics .col` elements,
     replace the `.art-pics` element's `outerHTML` with the masonry helper's output and call
     `arm(artView)`. If `playable(shownProject)` is non-empty, call the picture-column update function
     (button `disabled` states and `.art-count`). No `resize` or `matchMedia` listener is added inside `renderProject`; the clip, up/down
     and list `scroll` listeners are attached to the freshly rendered elements inside `renderProject`.
   - Keep the pager and the final `arm(artView)` call.
4. Write a Playwright check script outside the repo (in the session scratchpad) that performs criteria
   2-17, run it with the page served as described, and report its output together with the outputs of
   `python tools/check_site_assets.py` and `python tools/test_check_site_assets.py`.
