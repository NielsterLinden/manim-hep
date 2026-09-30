"""Gallery helpers for CI and the docs site.

    python scripts/gallery_tool.py list [--since REF]      # example folders (changed since REF)
    python scripts/gallery_tool.py render [--since REF]    # low-quality render of their scenes
    python scripts/gallery_tool.py pages                   # docs/gallery/*.md from the READMEs

``--since`` selects the examples touched since a git ref; any change under ``src/``
selects them all, because the core affects every example.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "gallery"
DOCS = ROOT / "docs" / "gallery"
REPO_TREE = "https://github.com/NielsterLinden/manim-hep/tree/main"
CATEGORY_TITLES = {
    "theory": "Theory",
    "methods": "Methods",
    "experiments": "Experiments",
    "plots": "Plotting results",
    "ml": "Machine learning",
}


def examples() -> list[Path]:
    return sorted(p.parent for p in GALLERY.rglob("scene.py") if "_template" not in p.parts)


def header(folder: Path) -> tuple[dict, str]:
    text = (folder / "README.md").read_text(encoding="utf-8")
    _, meta, body = text.split("---\n", 2)
    return yaml.safe_load(meta), body.strip()


def slug(folder: Path) -> str:
    return "-".join(folder.relative_to(GALLERY).parts)


def changed_since(ref: str) -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{ref}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    if any(name.startswith("src/") for name in out):
        return examples()
    touched = {ROOT / name for name in out}
    return [f for f in examples() if any(f in path.parents for path in touched)]


def render(folders: list[Path]) -> int:
    failures = []
    for folder in folders:
        for scene in header(folder)[0]["scenes"]:
            cmd = [sys.executable, "-m", "manim_hep.cli", "render", str(folder / "scene.py"), scene]
            cmd += ["--slug", f"{slug(folder)}--{scene}"]
            print("::group::" + " ".join(cmd[3:]), flush=True)
            result = subprocess.run(cmd, cwd=ROOT)
            print("::endgroup::", flush=True)
            if result.returncode:
                failures.append(f"{folder.relative_to(ROOT)} {scene}")
    for failure in failures:
        print(f"FAILED: {failure}")
    return 1 if failures else 0


def pages() -> int:
    """Write one docs page per example plus an index, linking CI-rendered previews."""
    if DOCS.exists():
        for old in DOCS.glob("*.md"):
            old.unlink()
    DOCS.mkdir(parents=True, exist_ok=True)
    rows: dict[str, list[str]] = {c: [] for c in CATEGORY_TITLES}
    for folder in examples():
        if not (folder / "README.md").is_file():
            print(f"skipping {folder.relative_to(ROOT).as_posix()}: no README.md yet")
            continue
        meta, body = header(folder)
        name = slug(folder)
        scene = meta["scenes"][0]
        preview = f"previews/{name}--{scene}.mp4"
        poster = f"previews/{name}--{scene}_last.png"
        source = folder.relative_to(ROOT).as_posix()
        page = [
            f"# {meta['title']}",
            "",
            f'<video controls muted loop playsinline poster="{poster}" src="{preview}" '
            'width="100%"></video>',
            "",
            f"**Source:** [`{source}/scene.py`]({REPO_TREE}/{source}) · "
            f"**Data:** {meta['data']} · **Label status:** {meta['label_status']} · "
            f"**Tags:** {', '.join(meta['tags'])}",
            "",
            body.split("\n", 1)[1] if body.startswith("# ") else body,
            "",
        ]
        (DOCS / f"{name}.md").write_text("\n".join(page), encoding="utf-8")
        rows[meta["category"]].append(f"| [{meta['title']}]({name}.md) | `{source}` |")
    index = ["# Gallery", "", "Every example renders in CI; previews are built with the site.", ""]
    for category, title in CATEGORY_TITLES.items():
        if rows[category]:
            index += [f"## {title}", "", "| Example | Folder |", "|---|---|", *rows[category], ""]
    (DOCS / "index.md").write_text("\n".join(index), encoding="utf-8")
    print(f"wrote {sum(len(r) for r in rows.values())} gallery pages to {DOCS}")
    return 0


def collect_previews() -> int:
    """Copy CI renders from .manim-hep/work into docs/gallery/previews/."""
    target = DOCS / "previews"
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for work in (ROOT / ".manim-hep" / "work").glob("*--*"):
        for file in (work / f"{work.name}.mp4", work / f"{work.name}_last.png"):
            if file.is_file():
                shutil.copy2(file, target / file.name)
                count += 1
    print(f"copied {count} preview files to {target}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "render", "pages", "previews"])
    parser.add_argument("--since", help="only examples changed since this git ref")
    args = parser.parse_args(argv)
    folders = changed_since(args.since) if args.since else examples()
    if args.command == "list":
        print("\n".join(str(f.relative_to(ROOT).as_posix()) for f in folders))
        return 0
    if args.command == "render":
        return render(folders)
    if args.command == "previews":
        return collect_previews()
    return pages()


if __name__ == "__main__":
    sys.exit(main())
