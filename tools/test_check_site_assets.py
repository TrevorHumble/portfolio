"""Tests for check_site_assets.py.

Lives in tools/, not tests/, because tools/retire-example.ps1 deletes tests/
when a project retires the bundled example.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

sys.path.insert(0, str(TOOLS))
from check_site_assets import find_problems  # noqa: E402

INDEX_HTML = '<img src="img/a.jpg"><img src="img/b.png">'

REJECTED_REFERENCE_FORMS = [
    "https://x.test/img/a.jpg",
    "../img/a.jpg",
    "art/img/a.jpg",
    "myimg/a.jpg",
    "img/a.jpgx",
    "img/notes.svg.txt",
    "img/a.jpg/foo.txt",
]


def build_site(root: Path, index_html=INDEX_HTML):
    site = root / "site"
    img = site / "img"
    img.mkdir(parents=True)
    (site / "index.html").write_text(index_html, encoding="utf-8")
    (img / "a.jpg").write_bytes(b"")
    (img / "b.png").write_bytes(b"")
    return site


def check(condition, message):
    if not condition:
        print(f"FAILED: {message}")
        sys.exit(1)


def test_find_problems_clean():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp))
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == [], f"expected no unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_missing():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp))
        (site / "img" / "b.png").unlink()
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == ["img/b.png"], f"expected img/b.png missing, got {missing}")
        check(unreferenced == [], f"expected no unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_unreferenced():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp))
        (site / "img" / "c.png").write_bytes(b"")
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == ["img/c.png"], f"expected img/c.png unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_accepts_dot_slash_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="img/a.jpg"><img src="./img/b.png">')
        (site / "img" / "b.png").unlink()
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == ["img/b.png"], f"expected ./img/b.png to count and be missing, got {missing}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_rejects_non_root_forms():
    # img/notes.svg.txt is meaningless as a rejection test unless a real
    # img/notes.svg exists for it to be wrongly credited against, so every
    # site in this loop carries one alongside the usual a.jpg and b.png.
    for ref in REJECTED_REFERENCE_FORMS:
        with tempfile.TemporaryDirectory() as tmp:
            site = build_site(Path(tmp), f'<img src="{ref}">')
            (site / "img" / "notes.svg").write_bytes(b"")
            missing, unreferenced, referenced_count = find_problems(site)
            check(referenced_count == 0, f"expected {ref!r} to not count as a reference, got count {referenced_count}")
            check(
                unreferenced == ["img/a.jpg", "img/b.png", "img/notes.svg"],
                f"expected all site pictures unreferenced when only ref is {ref!r}, got {unreferenced}",
            )
            check(missing == [], f"expected no missing for ref {ref!r}, got {missing}")


def test_find_problems_finds_subfolder_picture():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="img/a.jpg"><img src="img/b.png"><img src="img/art/x.jpg">')
        art = site / "img" / "art"
        art.mkdir()
        (art / "x.jpg").write_bytes(b"")
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == [], f"expected no unreferenced, got {unreferenced}")
        check(referenced_count == 3, f"expected referenced count 3, got {referenced_count}")


def test_find_problems_ignores_non_picture_file():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp))
        (site / "img" / "readme.txt").write_text("not a picture", encoding="utf-8")
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == [], f"expected readme.txt not reported unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_accepts_trailing_query_or_fragment():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="img/a.jpg?v=2"><img src="img/b.png#x">')
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == [], f"expected no unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_counts_reference_inside_html_comment():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<!-- <img src="img/a.jpg"> --><img src="img/b.png">')
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(
            unreferenced == [],
            f"expected no unreferenced (commented-out reference still counts), got {unreferenced}",
        )
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_normalizes_dot_and_double_slash():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="img/./a.jpg"><img src="img//b.png">')
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == [], f"expected no missing, got {missing}")
        check(unreferenced == [], f"expected no unreferenced, got {unreferenced}")
        check(referenced_count == 2, f"expected referenced count 2, got {referenced_count}")


def test_find_problems_rejects_reference_that_escapes_img():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="img/../index.jpg">')
        missing, unreferenced, referenced_count = find_problems(site)
        check(referenced_count == 0, f"expected img/../index.jpg to not count as a reference, got count {referenced_count}")
        check(
            unreferenced == ["img/a.jpg", "img/b.png"],
            f"expected both site pictures unreferenced, got {unreferenced}",
        )
        check(missing == [], f"expected no missing, got {missing}")


def test_find_problems_case_sensitive_comparison():
    with tempfile.TemporaryDirectory() as tmp:
        site = build_site(Path(tmp), '<img src="IMG/a.jpg">')
        missing, unreferenced, referenced_count = find_problems(site)
        check(missing == ["IMG/a.jpg"], f"expected IMG/a.jpg reported missing (case-sensitive compare), got {missing}")
        check("img/a.jpg" in unreferenced, f"expected img/a.jpg unreferenced (case mismatch), got {unreferenced}")
        check(referenced_count == 1, f"expected referenced count 1, got {referenced_count}")


def test_cli_exit_code_and_output():
    # Same made-up site, three states, checked from both working folders.
    states = [
        ("clean", lambda site: None, [], "referenced 2, missing 0, unreferenced 0", 0),
        (
            "missing",
            lambda site: (site / "img" / "b.png").unlink(),
            ["missing: site/img/b.png"],
            "referenced 2, missing 1, unreferenced 0",
            1,
        ),
        (
            "extra",
            lambda site: (site / "img" / "c.png").write_bytes(b""),
            ["unreferenced: site/img/c.png"],
            "referenced 2, missing 0, unreferenced 1",
            1,
        ),
    ]

    for name, mutate, expected_lines, expected_summary, expected_exit in states:
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp)
            site = build_site(copy_root)
            mutate(site)
            (copy_root / "tools").mkdir()
            shutil.copy2(TOOLS / "check_site_assets.py", copy_root / "tools" / "check_site_assets.py")

            working_folders = [
                (copy_root, ["tools/check_site_assets.py"]),
                (copy_root / "tools", ["check_site_assets.py"]),
            ]
            for cwd, args in working_folders:
                result = subprocess.run(
                    [sys.executable] + args,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                )
                check(
                    result.stdout.strip() != "",
                    f"[{name}] expected non-empty output from {cwd}, stderr was: {result.stderr}",
                )
                lines = result.stdout.splitlines()
                for expected in expected_lines:
                    check(
                        expected in lines,
                        f"[{name}] expected line {expected!r} from {cwd}, got {lines!r}, stderr: {result.stderr}",
                    )
                check(
                    lines[-1] == expected_summary,
                    f"[{name}] unexpected summary line from {cwd}: {lines[-1]!r}, stderr: {result.stderr}",
                )
                check(
                    result.returncode == expected_exit,
                    f"[{name}] expected exit code {expected_exit} from {cwd}, got {result.returncode}, stderr: {result.stderr}",
                )


def test_cli_reports_missing_index():
    with tempfile.TemporaryDirectory() as tmp:
        copy_root = Path(tmp)
        (copy_root / "site").mkdir()
        (copy_root / "tools").mkdir()
        shutil.copy2(TOOLS / "check_site_assets.py", copy_root / "tools" / "check_site_assets.py")

        result = subprocess.run(
            [sys.executable, "tools/check_site_assets.py"],
            cwd=copy_root,
            capture_output=True,
            text=True,
        )
        check(result.stdout.strip() != "", f"expected non-empty output, stderr was: {result.stderr}")
        lines = result.stdout.splitlines()
        check(
            lines == ["missing: site/index.html"],
            f"expected exactly one line 'missing: site/index.html', got {lines!r}, stderr: {result.stderr}",
        )
        check(result.returncode == 1, f"expected exit code 1, got {result.returncode}, stderr: {result.stderr}")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print("site asset tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
