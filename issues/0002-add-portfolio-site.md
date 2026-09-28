# Issue #0002: Add the portfolio site

**Type:** ready. **Category:** product feature.
**Depends on:** none.
**Blocks:** none.
**Touches:** `site/index.html` (new), `site/img/**` (new), `tools/check_site_assets.py` (new), `tools/test_check_site_assets.py` (new), `.gitattributes` (one new line), `.github/workflows/ci.yml` (one new step in the `lint` job, one in the `test` job, header comment reflowed at lines 10-13), `issues/0002-add-portfolio-site.md` (this file), `DESIGN.md` (one sentence under `## CI` and one line under `## Repo structure`), `README.md` (one new row and one tools entry in the Repo layout table), `WHAT-IT-CHECKS.md` (one bullet).

## User story
As a visitor to trevorhumble.com (a hiring manager or collaborator reading the portfolio), I need every
picture the portfolio page uses to be in the repo beside it, so that the page can be published later
with no broken images.

## Source
The approved site already exists outside the repo and is copied in unchanged:

- Page: `C:\Users\thumb\AppData\Local\Temp\claude\C--Blender-Practice\1893e6c9-7b05-4ab7-b5d0-858b7b4585f3\scratchpad\portfolio\site\index.html`
- Pictures: the `img\` folder beside it (it has one subfolder, `img\art\`).

The source folder also holds local-only test pages that must NOT be copied: `index_z.html`,
`index_z2.html`, `z_images.html`, `z_images2.html`. The source `img\` folder holds 171 files, of which
129 are referenced by `index.html`; the other 42 are unused drafts and must NOT be copied.

Out of scope: hosting and publishing. This issue only places the site and its pictures in `site/`.

## Acceptance criteria
1. **Given** the repo after this change, **When** a reader lists `site/`, **Then** it contains
   `index.html` and an `img` folder, and does not contain `index_z.html`, `index_z2.html`,
   `z_images.html` or `z_images2.html`.
2. **Given** `site/index.html` in the committed repo, **When** its SHA-256 is computed, **Then** it
   equals `6f75575651b83f185092b5b158fbc93b30b4ae7a4d7212234c97a27af497dd03` (the hash of the approved
   source page, recorded 2026-09-27).
3. **Given** `site/index.html`, **When** a reader greps it, **Then** it contains the literal string
   `<title>Trevor Humble</title>`.
4. **Given** the committed repo, **When** `python tools/check_site_assets.py` is run from the repo root,
   **Then** its last line is exactly `referenced 129, missing 0, unreferenced 0` and it exits with code `0`.
5. **Given** a copy of the repo where the referenced picture `site/img/headshot.jpg` has been deleted,
   **When** `python tools/check_site_assets.py` is run from that copy's root, **Then** it prints a line
   that is exactly `missing: site/img/headshot.jpg` and exits with code `1`.
6. **Given** a copy of the repo with an extra file `site/img/zz_unused.png` added, **When**
   `python tools/check_site_assets.py` is run from that copy's root, **Then** it prints a line that is
   exactly `unreferenced: site/img/zz_unused.png`, its last line is
   `referenced 129, missing 0, unreferenced 1`, and it exits with code `1`.
7. **Given** the committed repo, **When** `python ../tools/check_site_assets.py` is run from inside the
   `tools/` folder, **Then** its last line is exactly `referenced 129, missing 0, unreferenced 0` and it
   exits with code `0`.
8. **Given** `.github/workflows/ci.yml`, **When** a reader reads the `lint` job, **Then** it contains a
   step whose `run:` value is exactly `python tools/check_site_assets.py` and which has no `if:` key.
9. **Given** `.gitattributes`, **When** a reader greps it, **Then** it contains the line `site/** -text`.
10. **Given** `DESIGN.md`, **When** a reader greps it, **Then** it contains `tools/check_site_assets.py`
    and a line beginning with `site/`; `README.md` contains the string ``| `site/` |``; `WHAT-IT-CHECKS.md` contains the string
    `- **Every picture the portfolio page uses is in the repo.**`; and `.github/workflows/ci.yml` contains the line
    `# commit-gate integrity check, the site asset check and its tests always run.` (as amended in the revision
    section below).
11. **Given** the committed repo, **When** `python tools/test_check_site_assets.py` is run from the repo
    root, **Then** its last line is exactly `site asset tests passed` and it exits with code `0`.
12. **Given** `.github/workflows/ci.yml`, **When** a reader reads the `test` job, **Then** it contains a
    step whose `run:` value is exactly `python tools/test_check_site_assets.py` and which has no `if:` key.

## Implementation plan
1. Compute the SHA-256 of the source `index.html`. If the file is missing or the hash is not
   `6f75575651b83f185092b5b158fbc93b30b4ae7a4d7212234c97a27af497dd03`, stop and report; do not recreate
   or edit the page. Otherwise add the line `site/** -text` to the end of `.gitattributes` (the repo has
   `core.autocrlf=true`, which would otherwise rewrite line endings), then create `site/` at the repo
   root and copy the source `index.html` to `site/index.html` without changing a byte.
2. Find every picture path the page references: every match of the regular expression
   `img/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|gif|svg|webp)` in `site/index.html`, de-duplicated. Copy each
   matched path P (which begins with `img/`) from the source folder's P to `site/P`, creating subfolders
   as needed. Copy no other files.
3. Create `tools/check_site_assets.py` (Python standard library only). It finds the site folder from its
   own position, not the current directory: `SITE = Path(__file__).resolve().parent.parent / "site"`. It
   reads `SITE / "index.html"` and collects the referenced paths with the same regular expression as
   step 2. It lists every file under `SITE / "img"` recursively (`(SITE / "img").rglob("*")`, keeping
   only entries where `f.is_file()`), turning each into `f.relative_to(SITE).as_posix()` (giving
   `img/...`). It prints one line `missing: site/<path>` for each referenced path with no file, one line
   `unreferenced: site/<path>` for each file that is not referenced (both lists sorted), then a final
   line `referenced N, missing M, unreferenced U`, where N is the number of unique referenced paths
   (whether or not the file exists), M the number of missing lines and U the number of unreferenced lines. It exits `0` only when M and U are both 0, otherwise
   `1`.
4. In `.github/workflows/ci.yml`, in the `lint` job, insert a step named `Site asset check` with
   `run: python tools/check_site_assets.py` immediately after that job's `actions/setup-python` step,
   then a step named `Site asset tests` with `run: python tools/test_check_site_assets.py` right after
   it. Neither step has an `if:` key. Change no other step. In the header comment, replace the line
   `# commit-gate integrity check always runs. When you add your own code, add your` with
   `# commit-gate integrity check and the site asset check always run. When you add your own code, add your`.
5. In `DESIGN.md`: under `## Repo structure`, insert the line
   `site/                              - the portfolio web page (index.html) and its pictures (img/)`
   directly after the line that begins with `issues/`. Under `## CI`, directly after the numbered gate
   list, add the sentence: `The lint job also always runs tools/check_site_assets.py, which checks that
   every picture site/index.html references exists under site/img/ and that nothing else is there, and
   tools/test_check_site_assets.py, which proves that check catches a missing and an extra picture.`
   In `README.md`, in the `## Repo layout` table, insert the row
   ``| `site/` | The portfolio web page (`index.html`) and its pictures (`img/`) |`` directly after the
   `.github/workflows/` row, and in the `setup.ps1` · `tools/` row append `, check_site_assets` after
   `stop-run`. In `WHAT-IT-CHECKS.md`, directly after the bullet that begins
   `- **The code is auto-checked for cleanliness.**`, add the bullet:
   `- **Every picture the portfolio page uses is in the repo.** Every build confirms each picture the page names is present in site/img/, and that no unused pictures are stored there.`
6. Create `tools/test_check_site_assets.py` (standard library only; it lives in `tools/` because
   `tools/retire-example.ps1` deletes `tests/`). It copies the repo's `site/` folder and
   `tools/check_site_assets.py` (found from its own position: `REPO = Path(__file__).resolve().parent.parent`,
   copying `REPO / "site"` and `REPO / "tools" / "check_site_assets.py"`) into a `tempfile.TemporaryDirectory()` twice, keeping the same layout.
   In the first copy it deletes `site/img/headshot.jpg`, runs the checker with
   `subprocess.run([sys.executable, "tools/check_site_assets.py"], cwd=copy, capture_output=True, text=True)`,
   and asserts that the output has a line exactly `missing: site/img/headshot.jpg`, the last line is
   exactly `referenced 129, missing 1, unreferenced 0`, and the exit code is 1. In the second copy it adds
   an empty `site/img/zz_unused.png` and asserts a line exactly `unreferenced: site/img/zz_unused.png`, a
   last line exactly `referenced 129, missing 0, unreferenced 1`, and exit code 1. It prints
   `site asset tests passed` and exits 0 only if every assertion holds; otherwise it prints the failed
   assertion and exits 1.
7. Run `python tools/check_site_assets.py` from the repo root and from inside `tools/` (criteria 4 and 7),
   and `python tools/test_check_site_assets.py` from the repo root (criteria 5, 6 and 11).

## Revision after design review (2026-09-27)
The design review of the first implementation asked for these changes; they replace the matching parts
of steps 3, 4, 5 and 6 above. All acceptance criteria are unchanged.
- The checker keeps its logic in `find_problems(site: Path)`, which returns the missing and unreferenced
  paths and the referenced count; `main()` only prints and returns the exit code.
- Both sides of the comparison use one rule: references use the pattern
  `(?<![\w/.-])img/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|gif|svg|webp)` with `re.IGNORECASE`, and files on
  disk count only when their extension (lowercased) is one of jpg, jpeg, png, gif, svg, webp.
- `tools/test_check_site_assets.py` builds a small made-up site in a temp folder (two pictures) instead of
  copying the real one, so it does not depend on today's picture count, and it calls `find_problems`
  directly and also runs the real checker once as a subprocess against the made-up site's layout.
- The `Site asset tests` step moves from the `lint` job to the top of the `test` job, right after its
  `actions/setup-python` step, still with no `if:` key. Criterion 12 reads "the `test` job" instead of
  "the `lint` job". Criterion 10's `ci.yml` header line is
  `# commit-gate integrity check, the site asset check and its tests always run.`

## Second revision after review (2026-09-27)
- References use `(?<![\w/.-])(?:\./)?(img/[A-Za-z0-9_./-]+\.(?:EXTS))` with `re.IGNORECASE`, where EXTS
  is built from the one picture-extension set. It accepts `img/a.jpg` and `./img/a.jpg` and rejects web
  addresses (`https://x.test/img/a.jpg`), `../img/`, `art/img/` and `myimg/`. No HTML-comment stripping
  and no `%` decoding.
- If `site/index.html` is missing, `main()` prints `missing: site/index.html` and exits 1 without
  calling `find_problems`.
- Tests cover each accepted and rejected reference form, a picture in a subfolder (`img/art/x.jpg`), a
  non-picture file, and both working folders for the command line.

## Third revision after review (2026-09-27)
- Step 5's DESIGN.md sentence as shipped: `CI also always runs tools/check_site_assets.py in the lint job,
  which checks that every picture site/index.html references exists under site/img/ and that no unused
  pictures are stored there, and tools/test_check_site_assets.py in the test job, which proves that check
  catches a missing and an extra picture.` followed by one sentence stating the naming limit below.
- The reference pattern also ends with `(?![\w.-])`, so `img/a.jpgx` and `img/notes.svg.txt` are not
  read as `img/a.jpg` or `img/notes.svg`; `img/a.jpg?v=2` and `img/a.jpg#x` still count.
- Known limit, stated in the checker's pattern comment and in DESIGN.md: picture names may use only
  letters, digits, `_`, `.`, `-` and `/`; a reference containing a space or `%` is not checked.

## Fourth revision after review (2026-09-27)
- The trailing boundary is `(?![\w./-])` (it also rejects `img/a.jpg/foo.txt`).
- Each matched path goes through `posixpath.normpath`; only results that still start with `img/` count,
  so `img/./a.jpg` and `img//a.jpg` count as `img/a.jpg` and `img/../index.jpg` does not count.
- The known-limit sentence, in the checker comment and DESIGN.md, is: "Known limit: a picture link that
  contains a space or a % sign is not recognised, so the picture it names is reported as unused and such
  a link to a missing picture is not caught; a link inside an HTML comment still counts as a reference.
  Name pictures with letters, digits, underscores, dots and hyphens only."
- The WHAT-IT-CHECKS.md bullet ends with: "(Picture names with spaces or % signs are not checked, and a
  link inside an HTML comment still counts as a use.)"
