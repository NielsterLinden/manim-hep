"""``manim-hep init``: set up manim-hep in a repository.

Creates or merges ``manim-hep.toml``, an ``AGENTS.md`` block with the rules, a
``.gitignore`` block and the ``<root>/scenes|storylines|data|clips`` folders with
a smoke-test scene. ``--agent claude`` also adds ``@AGENTS.md`` to ``CLAUDE.md``
and pre-declares the manim-hep plugin in ``.claude/settings.json``;
``--agent codex`` copies the skills to ``.agents/skills/``.

It never overwrites your files. Blocks between its markers are replaced, and
nothing outside them is touched. When a file cannot be merged safely, it writes
``<file>.manim-hep.new`` next to it, reports it and exits with 1. Running it
twice changes nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from manim_hep._presets import PRESETS
from manim_hep._settings import load_settings

TEMPLATES = Path(__file__).parents[1] / "templates"
MD_MARKERS = ("<!-- >>> manim-hep -->", "<!-- <<< manim-hep -->")
GI_MARKERS = ("# >>> manim-hep", "# <<< manim-hep")
MARKETPLACE = {"source": {"source": "github", "repo": "NielsterLinden/manim-hep"}}
PLUGIN_ID = "manim-hep@manim-hep"


def skills_dir() -> Path:
    """The skills shipped with this installation (wheel) or checkout (editable)."""
    for candidate in (
        Path(__file__).parents[1] / "_skills",
        Path(__file__).parents[3] / "plugin" / "skills",
    ):
        if (candidate / "hep-animate" / "SKILL.md").is_file():
            return candidate
    raise FileNotFoundError("the manim-hep skills are missing from this installation")


@dataclass
class Report:
    lines: list[tuple[str, Path]] = field(default_factory=list)

    def add(self, status: str, path: Path) -> None:
        self.lines.append((status, path))

    @property
    def conflicts(self) -> list[Path]:
        return [p for s, p in self.lines if s == "conflict"]


def _read(path: Path) -> str:
    with path.open(encoding="utf-8", newline="") as fh:
        return fh.read()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def _newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _conflict(path: Path, text: str, report: Report) -> None:
    new = path.with_name(path.name + ".manim-hep.new")
    _write(new, text)
    report.add("conflict", new)


def _create_or_keep(path: Path, text: str, report: Report) -> None:
    if path.exists():
        report.add("unchanged", path)
    else:
        _write(path, text)
        report.add("created", path)


def merge_block(path: Path, markers: tuple[str, str], body: str, report: Report) -> None:
    """Put ``body`` between ``markers`` in ``path``; leave everything else as it is."""
    start, end = markers
    if not path.exists():
        _write(path, "\n".join([start, *body.splitlines(), end]) + "\n")
        report.add("created", path)
        return
    text = _read(path)
    nl = _newline(text)
    block = nl.join([start, *body.splitlines(), end])
    i, j = text.find(start), text.find(end)
    if i == -1 and j == -1:
        if not text or text.endswith(nl * 2):
            separator = ""
        elif text.endswith(nl):
            separator = nl  # one blank line before the block
        else:
            separator = nl * 2
        new = text + separator + block + nl
    elif i != -1 and j > i and text.count(start) == 1 and text.count(end) == 1:
        new = text[:i] + block + text[j + len(end) :]
    else:
        whole = "\n".join([start, *body.splitlines(), end]) + "\n"
        _conflict(path, whole, report)
        return
    if new == text:
        report.add("unchanged", path)
    else:
        _write(path, new)
        report.add("updated", path)


def ensure_line(path: Path, line: str, report: Report) -> None:
    if not path.exists():
        _write(path, line + "\n")
        report.add("created", path)
        return
    text = _read(path)
    if any(existing.strip() == line for existing in text.splitlines()):
        report.add("unchanged", path)
        return
    nl = _newline(text)
    prefix = "" if not text or text.endswith(nl) else nl
    _write(path, text + prefix + (nl if text else "") + line + nl)
    report.add("updated", path)


def merge_settings_json(path: Path, report: Report) -> None:
    wanted = {
        "extraKnownMarketplaces": {"manim-hep": MARKETPLACE},
        "enabledPlugins": {PLUGIN_ID: True},
    }
    if not path.exists():
        _write(path, json.dumps(wanted, indent=2) + "\n")
        report.add("created", path)
        return
    text = _read(path)
    try:
        data = json.loads(text) if text.strip() else {}
    except json.JSONDecodeError:
        _conflict(path, json.dumps(wanted, indent=2) + "\n", report)
        return
    ok = isinstance(data, dict)
    ok = ok and isinstance(data.get("extraKnownMarketplaces", {}), dict)
    ok = ok and isinstance(data.get("enabledPlugins", {}), dict)
    if not ok:
        _conflict(path, json.dumps(wanted, indent=2) + "\n", report)
        return
    before = json.dumps(data, sort_keys=True)
    data.setdefault("extraKnownMarketplaces", {}).setdefault("manim-hep", MARKETPLACE)
    data.setdefault("enabledPlugins", {}).setdefault(PLUGIN_ID, True)  # never flip a False
    if json.dumps(data, sort_keys=True) == before:
        report.add("unchanged", path)
        return
    indent = re.search(r"\n([ \t]+)\"", text)
    nl = _newline(text)
    out = json.dumps(data, indent=indent.group(1) if indent else 2, ensure_ascii=False)
    _write(path, out.replace("\n", nl) + nl)
    report.add("updated", path)


def copy_skills(target: Path, report: Report) -> None:
    source = skills_dir()
    for skill in sorted(p for p in source.iterdir() if p.name.startswith("hep-") and p.is_dir()):
        for file in sorted(
            f for f in skill.rglob("*") if f.is_file() and "__pycache__" not in f.parts
        ):
            dest = target / skill.name / file.relative_to(skill)
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file, dest)
                report.add("created", dest)
            elif dest.read_bytes() == file.read_bytes():
                report.add("unchanged", dest)
            else:
                _conflict(dest, file.read_text(encoding="utf-8"), report)


def agents_block() -> str:
    text = (skills_dir() / "hep-animate" / "SKILL.md").read_text(encoding="utf-8")
    rules = text.split("<!-- rules:start -->", 1)[1].split("<!-- rules:end -->", 1)[0].strip()
    return "\n".join(
        [
            "<!-- Written by `manim-hep init`; the text between these markers is replaced "
            "on the next run. -->",
            "# Animations with manim-hep",
            "",
            "This repository makes high-energy-physics animations with "
            "[manim-hep](https://github.com/NielsterLinden/manim-hep).",
            "Settings are in `manim-hep.toml`. The workflow lives in the `hep-animate` skill: "
            "the manim-hep plugin in Claude Code, `.agents/skills/hep-animate/` for Codex and "
            "other agents.",
            "",
            rules,
        ]
    )


def run(args: argparse.Namespace) -> int:
    repo = Path(args.dir).resolve()
    if not repo.is_dir():
        print(f"error: {repo} is not a folder")
        return 2
    if args.experiment not in PRESETS:
        print(f"error: --experiment must be one of: {', '.join(PRESETS)}")
        return 2
    root = Path(args.root)
    if root.is_absolute() or ".." in root.parts:
        print("error: --root must be a folder inside the repository, e.g. presentation")
        return 2
    report = Report()
    toml = (TEMPLATES / "manim-hep.toml").read_text(encoding="utf-8")
    toml = toml.replace("{root}", root.as_posix()).replace("{experiment}", args.experiment)
    settings = repo / "manim-hep.toml"
    _create_or_keep(settings, toml, report)
    merge_block(repo / "AGENTS.md", MD_MARKERS, agents_block(), report)
    gitignore = (TEMPLATES / "gitignore.txt").read_text(encoding="utf-8")
    body = "\n".join(gitignore.strip().splitlines()[1:-1])
    merge_block(repo / ".gitignore", GI_MARKERS, body, report)
    if args.agent in ("claude", "both"):
        ensure_line(repo / "CLAUDE.md", "@AGENTS.md", report)
        merge_settings_json(repo / ".claude" / "settings.json", report)
    if args.agent in ("codex", "both"):
        copy_skills(repo / ".agents" / "skills", report)
    base = repo / root
    _create_or_keep(
        base / "scenes" / "smoke_test.py",
        (TEMPLATES / "smoke_test.py").read_text(encoding="utf-8"),
        report,
    )
    for folder in ("storylines", "data"):
        if not (base / folder).exists():
            _write(base / folder / ".gitkeep", "")
            report.add("created", base / folder / ".gitkeep")
    (base / "clips").mkdir(parents=True, exist_ok=True)

    for status, path in report.lines:
        if status != "unchanged" or args.verbose:
            print(f"{status:9s} {path.relative_to(repo).as_posix()}")
    changed = sum(1 for s, _ in report.lines if s in ("created", "updated"))
    print(f"manim-hep init: {changed} file(s) created or updated in {repo}")
    if report.conflicts:
        print("Could not merge these safely; compare each with the original and merge by hand:")
        for path in report.conflicts:
            print(f"  {path.relative_to(repo).as_posix()}")
        return 1
    kept = load_settings(settings)
    if ("unchanged", settings) in report.lines and args.experiment not in (
        "generic",
        kept.experiment,
    ):
        print(f"note: kept the existing manim-hep.toml (experiment {kept.experiment!r})")
    smoke = (Path(kept.root) / "scenes" / "smoke_test.py").as_posix()
    print(f"next: manim-hep doctor, then manim-hep render {smoke} SmokeTest")
    return 0


def add_parser(sub) -> None:
    p = sub.add_parser(
        "init",
        help="set up manim-hep in a repository (safe to run again)",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--root", default=".", help="folder for scenes/, storylines/, data/, clips/")
    p.add_argument("--agent", choices=["claude", "codex", "both", "none"], default="none")
    p.add_argument(
        "--experiment", default="generic", help="generic, atlas, cms, cms-opendata or lhcb"
    )
    p.add_argument("--dir", default=".", help="the repository (default: here)")
    p.add_argument("--verbose", action="store_true", help="also list unchanged files")
    p.set_defaults(func=run)
