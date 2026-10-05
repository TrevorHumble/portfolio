# Issue #0005: Design projects browse on the home page; the Design index page goes away

**Type:** ready. **Category:** product feature.
**Depends on:** #0004.
**Blocks:** none.
**Touches:** `site/index.html` only in: the hero `.strip` third link's `href`; the body of `<section id="art">` (the `.art` grid and the `.art-more` paragraph); the `.more` CSS rule (one added `cursor: pointer` declaration); the page script's `renderIndex` function and the `artView` `[data-filter]` click listener (both removed, replaced by two new page-script variables `HOME_PICKS` and `expanded` (plus cached element references for the filter bar, grid and button), a one-time fill of the filter buttons, a home-section render function and its listeners); the `renderProject` back link; `route()`; and, in the wireframe-inspector `PICK` selector string, `a.more` changed to `.more`. Also `issues/0005-design-section-on-home.md` (this file) and `BUILDLOG.md` (one line).

## User story
As a visitor to the portfolio (a hiring manager or collaborator), I need the Design card at the top of the
home page to take me to the Design section like the other two cards do, and to browse and filter every
design project right there, so that I am never dropped three levels deep (project page, inside the Design
page, inside the home page) and lose my place.

## Background
Today, in `site/index.html`:
- The hero `.strip` has three links. `MyUI redesign` goes to `#work` and `Flatland` to `#blender` (sections
  on the home page). The third, `Liminal Fields`, goes to `#art-DAnGqo`, a project page.
- `<section id="art">` holds 8 static `<a class="art-tile">` links and a `See all` link to `#art-all`.
- `#art-all` is a separate Design index page drawn by `renderIndex()` into `#art-view`: a back link, a
  "Design" header, a filter button group (`GROUPS = ["All", "Animation", "3D", "Traditional and digital"]`,
  buttons `data-filter`, `aria-pressed`) and every project tile. The listener on `artView` for
  `[data-filter]` re-renders it.
- Each project page (`renderProject`) starts with `<p class="back"><a href="#art-all">All design</a></p>`.

The owner approved this change on 2026-10-05 from a prototype:
- The `Liminal Fields` hero card goes to `#art`.
- The Design index page is removed. Its filter buttons move into the home `#art` section, above the tiles.
- With `All` picked, the section shows the same 8 projects as today, in today's order (`DAnGqo`, `xDmrgR`,
  `zPkN3Q`, `DvEoo0`, `VJEGy4`, `8bJnLQ`, `8bK5zQ`, `PXQGa1`), and a button `See all N` (N = number of
  projects in `art-data`, 16 today). Clicking it shows every project in place: the same 8 first, then the
  rest in `art-data` order; the button then reads `Show fewer` and clicking it returns to the 8.
- Picking any other filter shows every project in that group, in `art-data` order, and hides the button.
  Picking `All` again shows the 8 or all, whichever was last chosen with the button.
- The project page back link `All design` goes to `#art`.
- An old link to `#art-all` lands on the home page scrolled to the Design section.
- Filter and expand choices survive leaving for a project page and coming back (they live in page-script
  variables, not in the URL).

Project ids by group, in `art-data` order (16 total):
- Animation (6): `DAnGqo`, `xDmrgR`, `VJEGy4`, `8bJnLQ`, `140WGo`, `kQY4zn`.
- 3D (6): `zPkN3Q`, `DvEoo0`, `8bK5zQ`, `d0dqaA`, `QnvPYd`, `2qwP8e`.
- Traditional and digital (4): `PXQGa1`, `n0mZo4`, `kQ5ZDn`, `qeDOAP`.

The home Design section is now drawn by the page script, so it is empty without JavaScript. This is
accepted: every project page and the old Design page are already drawn by the page script, so the static
tiles led nowhere without it.

Out of scope: project pages other than their back link, the `art-data` JSON, images, CSS other than the one
`.more` declaration, every other section and page.

## Acceptance criteria
All browser checks use Chromium driven by Playwright, against `site/` served with
`python3 -m http.server` from inside `site/`, after waiting 1500 ms for the page to settle after each
`page.goto`, and 500 ms after each click or hash change. "Desktop" is a 1440x900 viewport; "phone" is
390x844. "Tile ids" means the `href` of each `#art .art .art-tile`, in DOM order, with `#art-` removed.
"Section at top" means `Math.abs(document.getElementById("art").getBoundingClientRect().top) <= 1`.
"Home view" means `#home-view` is not `hidden` and `#art-view` is `hidden`. An element's "text" means its
`textContent` with leading and trailing whitespace trimmed (not `innerText`, which applies the CSS
uppercase).

1. **Given** the repo after this change, **When** `python tools/check_site_assets.py` is run from the repo
   root, **Then** its last line is exactly `referenced 134, missing 0, unreferenced 0` and it exits `0`;
   and `python tools/test_check_site_assets.py` ends with `site asset tests passed` and exits `0`.
2. **Given** `site/index.html` after this change, **When** it is searched, **Then** the strings
   `renderIndex`, `artindex` and `href="#art-all"` each occur 0 times; `.compare, .more";` occurs 1 time
   and `.compare, a.more"` occurs 0 times; and the `.more {` CSS rule contains `cursor: pointer;`.
3. **Given** desktop at `/`, **When** the third `.strip a` is read and then clicked, **Then** its `href`
   attribute is `#art`, and after the click `location.hash` is `#art`, it is the home view, and the section
   is at top.
4. **Given** desktop at `/`, **When** the `#art` section is read, **Then** the tile ids are exactly
   `DAnGqo, xDmrgR, zPkN3Q, DvEoo0, VJEGy4, 8bJnLQ, 8bK5zQ, PXQGa1`; the `#art .filters button` texts are
   exactly `All, Animation, 3D, Traditional and digital` in that order, with `aria-pressed="true"` on `All`
   only; and `#art .art-more button` is displayed (`offsetParent !== null`), its text is `See all 16`, and
   its `aria-expanded` is `false`.
5. **Given** desktop at `/`, **When** `#art .art-more button` is clicked, **Then** the tile ids are exactly
   `DAnGqo, xDmrgR, zPkN3Q, DvEoo0, VJEGy4, 8bJnLQ, 8bK5zQ, PXQGa1, 140WGo, d0dqaA, QnvPYd, kQY4zn, 2qwP8e,
   n0mZo4, kQ5ZDn, qeDOAP`, the button text is `Show fewer` and its `aria-expanded` is `true`; **When** it
   is clicked again, **Then** the tile ids are the 8 of criterion 4, the text is `See all 16` and
   `aria-expanded` is `false`.
6. **Given** desktop at `/`, **When** the filter button `Animation` is clicked, **Then** the tile ids are
   exactly `DAnGqo, xDmrgR, VJEGy4, 8bJnLQ, 140WGo, kQY4zn`, `Animation` has `aria-pressed="true"` and the
   other three `aria-pressed="false"`, and `#art .art-more button` is not displayed (`offsetParent ===
   null`); **When** `3D` is then clicked, **Then** the tile ids are exactly `zPkN3Q, DvEoo0, 8bK5zQ, d0dqaA,
   QnvPYd, 2qwP8e`; **When** `Traditional and digital` is then clicked, **Then** they are exactly `PXQGa1,
   n0mZo4, kQ5ZDn, qeDOAP`; **When** `All` is then clicked, **Then** they are the 8 of criterion 4 and the
   button is displayed with text `See all 16`.
7. **Given** desktop at `/`, **When** `#art .art-more button` is clicked, then `Animation`, then `All`,
   **Then** there are 16 tiles and the button text is `Show fewer`.
8. **Given** desktop, **When** `/#art-all` is loaded with `page.goto`, **Then** it is the home view and the
   section is at top; **And given** desktop at `/#art-kQ5ZDn`, **When** `location.hash = "art-all"` is
   run, **Then** it is the home view and the section is at top.
9. **Given** desktop at `/#art-kQ5ZDn`, **When** `#art-view .back a` is read and then clicked, **Then** its
   text is `All design` and its `href` is `#art`, and after the click it is the home view and the section
   is at top.
10. **Given** desktop at `/`, **When** `Animation` is clicked, then the tile `a[href="#art-140WGo"]` is
    clicked, then `#art-view .back a` is clicked, **Then** `Animation` has `aria-pressed="true"` and the
    tile ids are the 6 Animation ids of criterion 6.
11. **Given** desktop at `/`, **When** `#art .art-more button` is clicked, then the tile
    `a[href="#art-140WGo"]` is clicked, then `#art-view .back a` is clicked, **Then** there are 16 tiles
    and the `#art .art-more button` text is `Show fewer`.
12. **Given** desktop at `/`, **When** `#art .filters button[data-filter="3D"]` is focused and Enter is
    pressed, **Then** `document.activeElement` text is `3D` and its `aria-pressed` is `true`, and the tile
    ids are the 6 3D ids of criterion 6.
13. **Given** phone at `/#art`, **When** layout is read, **Then** the 8 tiles' left edges (rounded to whole
    px) take exactly 2 distinct values, every `#art .filters button` right edge is `<= 366` (390 minus the 24px page gutter), and
    `document.documentElement.scrollWidth` is `<= 390`.
14. **Given** desktop, **When** `/` is loaded with `page.goto`, then `/#art`, `/#art-all` and each of the 16
    `/#art-<id>` are loaded in turn with `page.goto`, and on `/` the `See all 16` button and each filter
    button are clicked, **Then** no `pageerror` is recorded, and no `console` message of type `error` is recorded whose
    `location().url` is empty or starts with the served origin, ignoring the `favicon.ico` 404 from
    `http.server` (errors from other hosts, such as video embeds and fonts the sandbox cannot reach, are
    not counted).

## Implementation plan
1. In `site/index.html`, in the hero `.strip`, change the third link from `<a href="#art-DAnGqo">` to
   `<a href="#art">`. Change nothing else in that link.
2. In `<section id="art">`, keep the `.section-head` as is. Replace the `<div class="art">` and its 8 static
   tiles, and the `<p class="art-more">` paragraph, with exactly:
   `<div class="toggle filters" role="group" aria-label="Show" id="art-filters" hidden></div>`,
   `<div class="art" id="art-grid"></div>`, and
   `<p class="art-more" hidden><button type="button" class="more" id="art-more" aria-controls="art-grid" aria-expanded="false"></button></p>`.
   In the `.more` CSS rule add `cursor: pointer;` (the rule now styles a button as well as links).
3. In the page script, delete `renderIndex()` and the `artView` `click` listener that handles
   `[data-filter]`. Keep `GROUPS`, `filter` and `tile(p)` as they are. Directly after the existing
   `function tile(p) { ... }`, add, in this order:
   - `var HOME_PICKS = ["DAnGqo", "xDmrgR", "zPkN3Q", "DvEoo0", "VJEGy4", "8bJnLQ", "8bK5zQ", "PXQGa1"];`
     with a one-line comment that these are the projects the collapsed section shows, in order.
   - `var expanded = false;`
   - Two statements: one that fills `#art-filters` once, with one
     `<button type="button" data-filter="G" aria-pressed="false">G</button>` per `GROUPS` entry `G`, in
     `GROUPS` order (the `renderIndex` markup, but every `aria-pressed="false"`; `renderHomeArt` sets them), and one that
     sets `#art-filters` `hidden` to `false`. The buttons are never rebuilt after this, so a focused filter
     button keeps focus.
   - `function renderHomeArt()` that builds the list to show: when `filter === "All"`, the `HOME_PICKS`
     projects in `HOME_PICKS` order (looked up in `ART` by `id`, skipping any id not found, e.g. with
     `.filter(Boolean)` after the lookup, so a later `art-data` edit can never stop the page script), followed, only when `expanded`, by every
     other `ART` project in `ART` order; otherwise every `ART` project whose `group === filter`, in `ART`
     order. It sets `#art-grid` `innerHTML` to those tiles via `tile(p)`; sets each `#art-filters button`'s
     `aria-pressed` to `String(button.getAttribute("data-filter") === filter)`; sets the `.art-more`
     paragraph's `hidden` to `filter !== "All"`; and sets the `#art-more` button's text to `Show fewer`
     when `expanded`, else `See all ` + `ART.length`, and its `aria-expanded` to `String(expanded)`.
   - Directly after the closing brace of `renderHomeArt`: one `click` listener on `#art-filters` that, for
     a `[data-filter]` target (via `closest`), sets `filter` and calls `renderHomeArt()`; one `click`
     listener on `#art-more` that flips `expanded` and calls `renderHomeArt()`; and one `renderHomeArt();`
     call. These run once at load, before the existing `route();` call near the end of the script, so
     `#art` is filled before `route()` scrolls to it.
4. In `renderProject`, change the back link to `<p class="back"><a href="#art">All design</a></p>`.
5. In `route()`: right after `var h = ...`, add `if (h === "art-all") { h = "art"; }` with a one-line
   comment that old links to the removed Design page land on its home section. Delete the
   `h === "art-all"` / `view = "artindex"` branch and the `if (view === "artindex") { renderIndex(); }`
   line, and change `artView.hidden = view !== "artindex" && view !== "project";` to
   `artView.hidden = view !== "project";`. The existing home branch then scrolls `#art` into view.
6. In the wireframe-inspector script near the end of the file, in the `PICK` selector string, change
   `a.more` to `.more` so the `See all` button still highlights in wireframe mode.
7. Write a Playwright check script outside the repo, at `<session scratchpad>/check-0005.js` (Node, using
   the globally installed `playwright` package), that performs criteria 2-14 and prints one line per
   criterion: `AC<n> PASS` or `AC<n> FAIL <what was read>`. Run it with the page served as described, on a free port
   (check nothing else is already listening on it). In
   the handoff report give the script's absolute path, the exact command to re-run it, its full raw
   output, and the outputs of `python tools/check_site_assets.py` and `python tools/test_check_site_assets.py`,
   so the PR reviewer can re-run the same check itself.
