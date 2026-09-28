"""Check that site/index.html and site/img/ agree on which pictures exist.

Finds site/ from this file's own location, not the current directory, so it
gives the same answer whether run from the repo root or from inside tools/.
"""
import posixpath
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
SITE_PREFIX = f"{SITE.name}/"

INDEX_FILE = "index.html"
IMG_DIR = "img"

PICTURE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}

_EXTS_PATTERN = "|".join(re.escape(s.lstrip(".")) for s in sorted(PICTURE_SUFFIXES))

# Accepts "img/a.jpg" and "./img/a.jpg". Rejects a web address
# (https://x.test/img/a.jpg), a path that climbs out of the site (../img/a.jpg),
# a picture under some other folder (art/img/a.jpg), a folder name that merely
# ends in "img" (myimg/a.jpg), and a name that runs past the extension
# (img/a.jpgx, img/notes.svg.txt, img/a.jpg/foo.txt). A "?" or "#" after the
# extension is fine (img/a.jpg?v=2, img/a.jpg#x still count), since a browser
# treats those as a query string or a fragment, not part of the path.
# Known limit: a picture link that contains a space or a % sign is not
# recognised, so the picture it names is reported as unused and such a link
# to a missing picture is not caught; a link inside an HTML comment still
# counts as a reference. Name pictures with letters, digits, underscores,
# dots and hyphens only.
REF_PATTERN = re.compile(
    rf"(?<![\w/.-])(?:\./)?({IMG_DIR}/[A-Za-z0-9_./-]+\.(?:{_EXTS_PATTERN}))(?![\w./-])",
    re.IGNORECASE,
)


def find_problems(site: Path):
    """Return (missing, unreferenced, referenced_count) for the site at `site`.

    Assumes `site / INDEX_FILE` exists; the caller checks that first.
    """
    html = (site / INDEX_FILE).read_text(encoding="utf-8")
    # IGNORECASE only decides whether something looks like a picture reference;
    # the path is then compared to disk exactly, because the eventual web host
    # is case-sensitive and a case mismatch there is a real broken image.
    # Normalised the same way a browser resolves the link, so "img/./a.jpg"
    # and "img//a.jpg" match the real file and "img/../index.jpg" does not.
    referenced = set()
    for match in REF_PATTERN.findall(html):
        normalized = posixpath.normpath(match)
        if normalized.lower().startswith(f"{IMG_DIR}/"):
            referenced.add(normalized)

    on_disk = set()
    img_dir = site / IMG_DIR
    if img_dir.is_dir():
        for f in img_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in PICTURE_SUFFIXES:
                on_disk.add(f.relative_to(site).as_posix())

    missing = sorted(p for p in referenced if p not in on_disk)
    unreferenced = sorted(p for p in on_disk if p not in referenced)

    return missing, unreferenced, len(referenced)


def main():
    if not (SITE / INDEX_FILE).is_file():
        print(f"missing: {SITE_PREFIX}{INDEX_FILE}")
        return 1

    missing, unreferenced, referenced_count = find_problems(SITE)

    for p in missing:
        print(f"missing: {SITE_PREFIX}{p}")
    for p in unreferenced:
        print(f"unreferenced: {SITE_PREFIX}{p}")

    print(f"referenced {referenced_count}, missing {len(missing)}, unreferenced {len(unreferenced)}")

    return 0 if (not missing and not unreferenced) else 1


if __name__ == "__main__":
    sys.exit(main())
