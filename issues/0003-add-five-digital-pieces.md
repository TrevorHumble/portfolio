# Issue #0003: Add five pieces to the Digital project

**Type:** ready. **Category:** product feature.
**Depends on:** #0002.
**Blocks:** none.
**Touches:** `site/index.html` (the `kQ5ZDn` entry in the `art-data` JSON only), `site/img/art/kQ5ZDn-6.jpg` to `site/img/art/kQ5ZDn-10.jpg` (new), `site/img/art/kQ5ZDn-cover.jpg` (replaced), `issues/0003-add-five-digital-pieces.md` (this file), `BUILDLOG.md` (one line).

## User story
As a visitor to the portfolio (a hiring manager or collaborator), I need the owner's five newest digital
paintings in the Digital project, with the soldier piece as its tile, so that the project shows current work.

## Source
Five pictures supplied by the owner on 2026-10-04, in this order (the order they appear on the page):

| New file | Source file (under `/root/.claude/uploads/4f77e5a1-8ab3-5f77-9e1d-9f46077dd602/`) | Source size | Subject | Source SHA-256 |
|---|---|---|---|---|
| `kQ5ZDn-6.jpg` | `d10bc2c1-image.jpg` | 1739x2576 | soldier with a rifle under storm clouds | `56bd7ce26b3f7f36fa204da18f818a5b8b89106b9861d1c52a0a1831297754b0` |
| `kQ5ZDn-7.jpg` | `ae2733db-image.jpg` | 2576x1932 | woman lighting a cigarette held by a fish | `7431bb8c88c13e0b22e65b8c832829dcc6bb8650855ecaab40a1c55369d5d6f2` |
| `kQ5ZDn-8.jpg` | `c62a6d19-image.png` | 2064x2752 | blue pencil caricature of a face | `c0e84918971b5ede91ba0882b1dfaf38dff83015c8a54b5d4969497113d774f1` |
| `kQ5ZDn-9.jpg` | `c07416c8-image.png` | 2064x2752 | black and white seated figure in boots | `a26e69ae362c4a4bccb7c80982167a1e273ed5c5f2dee1f50872f69f7b95fef0` |
| `kQ5ZDn-10.jpg` | `b560b65b-image.png` | 2064x2752 | teal dancer on navy with a cable | `d30157797cec579bfa2f196cd4429c76cf1ed387d00620564dd5eb1d37bb6aed` |

The owner chose to append them to the existing Digital project (`id` `kQ5ZDn`) and to make the soldier the
project's cover. The project's title, kind, group, text and tools stay as they are.

Out of scope: any other project, the home page tiles, and publishing.

## Acceptance criteria
1. **Given** the committed repo, **When** `python tools/check_site_assets.py` is run from the repo root,
   **Then** its last line is exactly `referenced 134, missing 0, unreferenced 0` and it exits with code `0`.
2. **Given** the `art-data` JSON in `site/index.html`, **When** it is parsed and the entry with `"id": "kQ5ZDn"`
   is read, **Then** its `imgs` list has 10 items, the first five are unchanged from commit `ce9d6af`, and
   items 6 to 10 have `src` values `img/art/kQ5ZDn-6.jpg` to `img/art/kQ5ZDn-10.jpg` in that order.
3. **Given** each of `site/img/art/kQ5ZDn-6.jpg` to `kQ5ZDn-10.jpg`, **When** it is opened with Pillow,
   **Then** its format is `JPEG`, its mode is `RGB`, it has no `icc_profile`, its size is `(1600, 2370)`,
   `(1600, 1200)`, `(1600, 2133)`, `(1600, 2133)`, `(1600, 2133)` respectively, and that size equals the `w`
   and `h` recorded for it in the JSON.
4. **Given** each of `kQ5ZDn-6.jpg` to `kQ5ZDn-10.jpg`, its own Source table row's file (whose SHA-256 must
   first equal the table's value), and a reference made from that file by converting from the embedded profile to sRGB with `ImageCms.profileToProfile` (or `convert('RGB')` when the
   source has no profile) and resizing to the saved size with `LANCZOS`, **When**
   `ImageStat.Stat(ImageChops.difference(saved.convert('RGB'), reference)).mean` is computed, **Then** every
   channel is below `3.0`. For `kQ5ZDn-7.jpg` and `kQ5ZDn-10.jpg`, the mean against a reference made with plain
   `convert('RGB')` (no profile conversion) is at least `3.0` in at least one channel. (`kQ5ZDn-8.jpg` and
   `kQ5ZDn-9.jpg` are near-neutral, so the conversion barely changes them and this second check does not apply.)
5. **Given** `site/img/art/kQ5ZDn-cover.jpg` and a reference made (after confirming the source's SHA-256
   matches the table) by `Image.open('/root/.claude/uploads/4f77e5a1-8ab3-5f77-9e1d-9f46077dd602/d10bc2c1-image.jpg').convert('RGB').crop((0, 600, 1739, 2339)).resize((600, 600), Image.LANCZOS)`,
   **When** it is opened with Pillow and the per-channel mean of `ImageChops.difference` is computed, **Then**
   its format is `JPEG`, its size is `(600, 600)`, and every channel is below `3.0`.
6. **Given** `git diff ce9d6af -- site/index.html` (the working tree, or the commit holding this change,
   against the #0002 commit), **When** it is read, **Then** the only changed line is the
   one holding the `art-data` JSON; parsing the JSON at `ce9d6af` and the new JSON shows every entry other than `kQ5ZDn` is
   identical and the `kQ5ZDn` entry differs only in `imgs`; and `json.dumps(new_data)` equals, byte for byte, the new
   text between `<script type="application/json" id="art-data">` and `</script>` on that line.
7. **Given** each of `kQ5ZDn-6.jpg` to `kQ5ZDn-10.jpg` and `kQ5ZDn-cover.jpg`, **When** opened with Pillow,
   **Then** `.quantization` equals `Image.open('site/img/art/kQ5ZDn-1.jpg').quantization` and
   `.info['progressive']` is `1`.
8. **Given** the committed repo, **When** `python tools/test_check_site_assets.py` is run from the repo root,
   **Then** its last line is exactly `site asset tests passed` and it exits with code `0`.

## Implementation plan
1. For each row of the Source table, open the source with Pillow. If it has `info['icc_profile']` (four of the
   five carry Display P3), convert it to sRGB first:
   `im = ImageCms.profileToProfile(im.convert('RGB'), ImageCms.ImageCmsProfile(io.BytesIO(im.info['icc_profile'])), ImageCms.createProfile('sRGB'), outputMode='RGB')`;
   otherwise `im = im.convert('RGB')` (the PNG alpha channels are fully opaque). Resize to width 1600 with
   height `round(1600 * h / w)` using `LANCZOS`, and save to the new file under `site/img/art/` as JPEG with
   `quality=80, optimize=True, progressive=True` and no embedded profile (`kQ5ZDn-1..5.jpg` match quality 80).
2. Make the cover: open `d10bc2c1-image.jpg`, convert to `RGB` (it has no profile), crop the square box `(0, 600, 1739, 2339)` (full width,
   centered on the soldier), resize to 600x600 with `LANCZOS`, and save over `site/img/art/kQ5ZDn-cover.jpg`
   with the same JPEG settings (`quality=80`).
3. In `site/index.html`, in the `art-data` JSON entry with `"id": "kQ5ZDn"`, append five objects to `imgs`,
   in table order, each `{"src": "img/art/kQ5ZDn-N.jpg", "w": W, "h": H}` with W and H read from the saved
   file. Parse the JSON, edit it, and re-serialize with `json.dumps(data)` at default settings (`ensure_ascii=True`),
   which reproduces the current text between the `<script type="application/json" id="art-data">` and
   `</script>` tags byte for byte; replace only that text. The file uses CRLF line endings and is marked `-text`;
   read and write it with `open(..., encoding='utf-8', newline='')` so the CRLFs are kept. Change no other
   byte of the file.
4. Run `python tools/check_site_assets.py` and `python tools/test_check_site_assets.py` and report both outputs.
