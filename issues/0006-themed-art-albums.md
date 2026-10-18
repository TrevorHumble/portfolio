# Issue #0006: Themed art albums

**Type:** ready. **Category:** product feature.
**Depends on:** #0005.
**Blocks:** none.
**Touches:** `site/index.html` (art data only), `site/img/art/` (33 files added and 17 removed, listed under Source), `BUILDLOG.md` (one line, appended by the orchestrator at commit per BUILDLOG.md, not by the implementer), `issues/0006-themed-art-albums.md` (this file).

## User story
As a visitor browsing the Design section of trevorhumble.com, I need Trevor's drawings and digital art
grouped into themed albums (Live Wire, Shards, The Cast, Haze) instead of two catch-all albums, so that
I can see the range of his work and how each way of drawing looks.

## Source
The owner approved the look of the four albums from a preview on 2026-10-17. This change is staged on top of #0005
(the current main), and the five pieces #0003 added to Digital are kept (four are the same pictures as pieces in these
albums; the fifth, the soldier painting, leads Haze, as it led Digital). The approved files are
staged, already processed, in:

`C:\Users\thumb\AppData\Local\Temp\claude\C--Blender-Practice\1893e6c9-7b05-4ab7-b5d0-858b7b4585f3\scratchpad\newart\stage\`

That folder is a full copy of the site after the change: `index.html` (SHA-256
`03c7a3f12274eb71c69bd76ed4442ca8d47a1da8c5674b1508666e04a8b21dcd`) and `img/`. Compared with the repo's
current `site/`, its only differences are:

- `index.html`: the art data drops the albums with ids `kQ5ZDn` ("Digital") and `qeDOAP` ("Expressive
  Sketches") and adds four albums with ids `live-wire` (10 pictures), `shards` (8), `the-cast` (7) and
  `haze` (4), each with a cover.
- `img/art/`: adds `live-wire-1.jpg` to `live-wire-10.jpg`, `shards-1.jpg` to `shards-8.jpg`,
  `the-cast-1.jpg` to `the-cast-7.jpg`, `haze-1.jpg` to `haze-4.jpg`, and `live-wire-cover.jpg`,
  `shards-cover.jpg`, `the-cast-cover.jpg`, `haze-cover.jpg` (33 files); removes `kQ5ZDn-1.jpg` to
  `kQ5ZDn-10.jpg`, `kQ5ZDn-cover.jpg`, `qeDOAP-1.jpg` to `qeDOAP-5.jpg` and `qeDOAP-cover.jpg` (17 files).

## Acceptance criteria
1. **Given** `site/index.html` in the committed repo, **When** its SHA-256 is computed, **Then** it equals
   `03c7a3f12274eb71c69bd76ed4442ca8d47a1da8c5674b1508666e04a8b21dcd`.
2. **Given** the committed repo, **When** `python tools/check_site_assets.py` is run from the repo root,
   **Then** its last line is exactly `referenced 150, missing 0, unreferenced 0` and it exits with code `0`.
3. **Given** the art data in `site/index.html` (the JSON inside `<script type="application/json"
   id="art-data">`), **When** it is parsed, **Then** it contains albums with ids `live-wire`, `shards`,
   `the-cast` and `haze` whose `imgs` lists have 10, 8, 7 and 4 entries, and no album with id `kQ5ZDn` or
   `qeDOAP`.
4. **Given** `site/img/art/` in the committed repo, **When** `sha256sum live-wire-* shards-* the-cast-* haze-* | sed 's/ \*/  /' | LC_ALL=C sort -k2 | sha256sum`
   is run inside it, **Then** it prints `5484cdc0339fce8323a38a5889a96cee6da13883a2282455e51c9f15c0660da8`,
   `ls live-wire-* shards-* the-cast-* haze-* | wc -l` prints `33`, and none of the 17 files named as removed exists.
5. **Given** `python tools/test_check_site_assets.py` run from the repo root, **When** it finishes,
   **Then** its last line is `site asset tests passed` and it exits with code `0`.

## Implementation plan
1. Compute the SHA-256 of the staged `index.html` and run the criterion 4 command inside the staged `img/art/`.
   If the staged folder is missing, the index hash is not
   `03c7a3f12274eb71c69bd76ed4442ca8d47a1da8c5674b1508666e04a8b21dcd`, or the picture hash is not
   `5484cdc0339fce8323a38a5889a96cee6da13883a2282455e51c9f15c0660da8`, stop and report; do not recreate or edit any file.
2. Copy the staged `index.html` over `site/index.html` without changing a byte.
3. Copy the 33 added files named in the Source section from the staged `img/art/` into `site/img/art/`,
   and delete the 17 removed files from `site/img/art/` (`git rm`).
4. From the repo root, compute the SHA-256 of `site/index.html`, parse the `art-data` JSON, run
   `python tools/check_site_assets.py` and `python tools/test_check_site_assets.py`, run the criterion 4 command in
   `site/img/art/`, and confirm criteria 1 to 5.
