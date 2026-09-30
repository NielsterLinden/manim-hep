"""Publication-safety checks for this repository (spec §10.3); CI runs them on every PR.

- no committed media (videos, GIFs): previews are built by CI
- no file over 1 MB
- no private paths or host names in tracked text files

Run from the repository root: ``python scripts/hygiene.py``. Exit status 1 on problems.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MEDIA = {".mp4", ".mov", ".gif", ".webm", ".mkv", ".avi"}
MAX_BYTES = 1_000_000
DENYLIST = [
    (re.compile(r"/afs/\w"), "AFS path"),
    (re.compile(r"/eos/\w"), "EOS path"),
    (re.compile(r"/dcache/\w"), "dCache path"),
    (re.compile(r"/project/\w"), "cluster project path"),
    (re.compile(r"/data/\w[^\s'\"`]*/users?/\w"), "cluster user-data path"),
    (re.compile(r"\b[A-Za-z]:[\\/]+Users[\\/]+\w"), "Windows user folder"),
    (re.compile(r"/home/[a-z]"), "home folder"),
    (re.compile(r"(?<![\w.])/Users/[A-Za-z]"), "macOS user folder"),
    (re.compile(r"\blxplus\d+|\blxplus\.cern\.ch"), "CERN host name"),
    (re.compile(r"\bstbc(?:-i\d+)?\b"), "cluster host name"),
    (re.compile(r"\b[\w-]+\.nikhef\.nl\b"), "institute host name"),
]
# Real leaks continue after the prefix (/afs/cern.ch/...); bare mentions in docs pass.
# Files that must mention the patterns in order to define or test them, and design notes.
EXEMPT = (
    "scripts/hygiene.py",
    "src/manim_hep/cli/lint.py",
    "tests/test_lint.py",
    "tests/test_hygiene.py",
    "docs/superpowers/",
)


def tracked_files(root: Path) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True
    ).stdout.decode("utf-8")
    return [root / name for name in out.split("\0") if name]


def check_file(path: Path, rel: str) -> list[str]:
    problems = []
    if path.suffix.lower() in MEDIA:
        problems.append(f"{rel}: media file (previews are built by CI, not committed)")
    size = path.stat().st_size
    if size > MAX_BYTES:
        problems.append(f"{rel}: {size / 1e6:.1f} MB is over the 1 MB limit")
    if rel.startswith(EXEMPT) or path.suffix.lower() in {".png", ".jpg", ".ttf", ".otf", ".whl"}:
        return problems
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return problems
    for number, line in enumerate(text.splitlines(), start=1):
        for pattern, what in DENYLIST:
            if pattern.search(line):
                problems.append(f"{rel}:{number}: {what}: {line.strip()[:100]}")
    return problems


def main(root: Path | None = None) -> int:
    root = root or Path(__file__).resolve().parents[1]
    problems = []
    for path in tracked_files(root):
        if path.is_file():
            problems += check_file(path, path.relative_to(root).as_posix())
    for problem in problems:
        print(problem)
    print(f"hygiene: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
