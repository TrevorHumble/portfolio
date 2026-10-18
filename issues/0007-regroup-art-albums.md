# Issue #0007: Regroup the art albums

**Type:** ready. **Category:** product feature.
**Depends on:** #0006.
**Blocks:** none.
**Touches:** `site/index.html` (art data only), `site/img/art/` (the album files listed under Source; in git terms 26 added, 26 deleted, 5 modified: shards-1, -3, -4, -6 and -cover; shards-2 and shards-5 are byte-identical in both versions and stay unchanged), `BUILDLOG.md` (one line, appended by the orchestrator at commit per BUILDLOG.md, not by the implementer), `issues/0007-regroup-art-albums.md` (this file).

## User story
As a visitor browsing the Design section of trevorhumble.com, I need Trevor's drawings and digital art
grouped the way he sorts them himself (Expressive Sketches, Shards, Heavy Paint, Krita, Characters), with
the right tool named on each, so that each album shows one way of working.

## Source
The owner directed this regrouping piece by piece on 2026-10-17, after #0006 went live. The approved files
are staged, already processed, in:

`C:\Users\thumb\AppData\Local\Temp\claude\C--Blender-Practice\1893e6c9-7b05-4ab7-b5d0-858b7b4585f3\scratchpad\newart\stage2\`

That folder is a full copy of the site after the change, built on top of #0006 (the current main). If it
is gone, this issue cannot be implemented as written; halt per step 1. Compared with the repo's `site/`:

- `index.html` (SHA-256 `890812056d6f014a96452f23805279070339cd3b34eece3803c785226e433ad9`): the art data
  drops the albums `live-wire`, `shards`, `the-cast` and `haze` and adds `expressive-sketches` (8 pictures,
  tools Alcohol markers and Procreate), `shards` (6, Procreate), `heavy-paint` (3, Heavy Paint), `krita` (3,
  Krita) and `characters` (8, Procreate), each with a cover. Every other album is unchanged.
- `img/art/`: every file whose name starts with `live-wire-`, `shards-`, `the-cast-` or `haze-` is removed
  (33 files), and every file whose name starts with `expressive-sketches-`, `shards-`, `heavy-paint-`,
  `krita-` or `characters-` is added from the staged copy (33 files). Note that `shards-` names appear on
  both sides: shards-1, -3, -4, -6 and -cover get new content, shards-7 and -8 are removed, and shards-2 and -5
  are byte-identical in both versions.

## Acceptance criteria
1. **Given** `site/index.html` in the committed repo, **When** its SHA-256 is computed, **Then** it equals
   `890812056d6f014a96452f23805279070339cd3b34eece3803c785226e433ad9`.
2. **Given** the committed repo, **When** `python tools/check_site_assets.py` is run from the repo root,
   **Then** its last line is exactly `referenced 150, missing 0, unreferenced 0` and it exits with code `0`.
3. **Given** the JSON inside `<script type="application/json" id="art-data">` in `site/index.html`, **When**
   it is parsed, **Then** it contains albums with ids
   `expressive-sketches`, `shards`, `heavy-paint`, `krita` and `characters` whose `imgs` lists have 8, 6, 3, 3
   and 8 entries, and no album with id `live-wire`, `the-cast` or `haze`.
4. **Given** `site/img/art/` in the committed repo, **When**
   `sha256sum expressive-sketches-* shards-* heavy-paint-* krita-* characters-* | sed 's/ \*/  /' | LC_ALL=C sort -k2 | sha256sum`
   is run inside it, **Then** it prints `20d061e3b2bb1751d11baaccec5e86798d9c5168a60def18dd64a0a76f09d300`,
   `ls expressive-sketches-* shards-* heavy-paint-* krita-* characters-* | wc -l` prints `33`, and no file
   starting with `live-wire-`, `the-cast-` or `haze-` exists.
5. **Given** `python tools/test_check_site_assets.py` run from the repo root, **When** it finishes, **Then**
   its last line is `site asset tests passed` and it exits with code `0`.

## Implementation plan
1. Compute the SHA-256 of the staged `index.html` and run the criterion 4 command inside the staged
   `img/art/`. If the staged folder is missing, the index hash is not
   `890812056d6f014a96452f23805279070339cd3b34eece3803c785226e433ad9`, or the picture hash is not
   `20d061e3b2bb1751d11baaccec5e86798d9c5168a60def18dd64a0a76f09d300`, stop and report; do not recreate or edit any file.
2. Copy the staged `index.html` over `site/index.html` without changing a byte.
3. In `site/img/art/`, remove (`git rm`) every file whose name starts with `live-wire-`, `shards-`,
   `the-cast-` or `haze-`. Then copy every staged `img/art/` file whose name starts with
   `expressive-sketches-`, `shards-`, `heavy-paint-`, `krita-` or `characters-` into `site/img/art/`. Then run `git add site/index.html site/img/art/` so every
   copied file is staged.
4. From the repo root, compute the SHA-256 of `site/index.html`, parse the art data, run
   `python tools/check_site_assets.py` and `python tools/test_check_site_assets.py`, run the criterion 4
   command in `site/img/art/`, and confirm criteria 1 to 5.
