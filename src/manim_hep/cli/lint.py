"""``manim-hep lint [PATHS]``: check scene files against the house rules.

Codes (silence one on a line with ``# noqa: MH001``):

- MH001  hard-coded colour: take colours from the theme palette
- MH002  hard-coded font: the theme sets the font
- MH003  ManimGL (manimlib) code: manim-hep uses Manim Community Edition
- MH004  ``construct`` must end with ``self.wait(t)``, t ≤ 0.2 s, so the last frame
         shows the final state
- MH005  hand-typed experiment label: use ``manim_hep.label(...)``
- MH006  private path or host name

It also lists every on-screen string, to compare with the storyline.
"""

from __future__ import annotations

import argparse
import ast
import io
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path

from manim_hep._settings import load_settings

MESSAGES = {
    "MH000": "file does not parse",
    "MH001": "hard-coded colour; take it from the theme palette",
    "MH002": "hard-coded font; the theme sets the font",
    "MH003": "ManimGL code; manim-hep uses Manim Community Edition (`from manim import ...`)",
    "MH004": "construct() must end with self.wait(t), t <= 0.2 s (end on the last change)",
    "MH005": "hand-typed experiment label; use manim_hep.label(experiment, status=...)",
    "MH006": "private path or host name",
}

# Manim Community Edition 0.21 colour constants (manim.utils.color.manim_colors).
MANIM_COLOURS = frozenset(
    [
        "BLACK",
        "BLUE",
        "BLUE_A",
        "BLUE_B",
        "BLUE_C",
        "BLUE_D",
        "BLUE_E",
        "DARKER_GRAY",
        "DARKER_GREY",
        "DARK_BLUE",
        "DARK_BROWN",
        "DARK_GRAY",
        "DARK_GREY",
        "GOLD",
        "GOLD_A",
        "GOLD_B",
        "GOLD_C",
        "GOLD_D",
        "GOLD_E",
        "GRAY",
        "GRAY_A",
        "GRAY_B",
        "GRAY_BROWN",
        "GRAY_C",
        "GRAY_D",
        "GRAY_E",
        "GREEN",
        "GREEN_A",
        "GREEN_B",
        "GREEN_C",
        "GREEN_D",
        "GREEN_E",
        "GREY",
        "GREY_A",
        "GREY_B",
        "GREY_BROWN",
        "GREY_C",
        "GREY_D",
        "GREY_E",
        "LIGHTER_GRAY",
        "LIGHTER_GREY",
        "LIGHT_BROWN",
        "LIGHT_GRAY",
        "LIGHT_GREY",
        "LIGHT_PINK",
        "LOGO_BLACK",
        "LOGO_BLUE",
        "LOGO_GREEN",
        "LOGO_RED",
        "LOGO_WHITE",
        "MAROON",
        "MAROON_A",
        "MAROON_B",
        "MAROON_C",
        "MAROON_D",
        "MAROON_E",
        "ORANGE",
        "PINK",
        "PURE_BLUE",
        "PURE_CYAN",
        "PURE_GREEN",
        "PURE_MAGENTA",
        "PURE_RED",
        "PURE_YELLOW",
        "PURPLE",
        "PURPLE_A",
        "PURPLE_B",
        "PURPLE_C",
        "PURPLE_D",
        "PURPLE_E",
        "RED",
        "RED_A",
        "RED_B",
        "RED_C",
        "RED_D",
        "RED_E",
        "TEAL",
        "TEAL_A",
        "TEAL_B",
        "TEAL_C",
        "TEAL_D",
        "TEAL_E",
        "WHITE",
        "YELLOW",
        "YELLOW_A",
        "YELLOW_B",
        "YELLOW_C",
        "YELLOW_D",
        "YELLOW_E",
    ]
)
COLOUR_CALLS = {"ManimColor", "rgb_to_color", "rgba_to_color", "hex_to_rgb", "color_to_rgb"}
MANIMGL_NAMES = {
    "ShowCreation",
    "InteractiveScene",
    "TexText",
    "OldTex",
    "OldTexText",
    "ShowCreationThenDestruction",
}
TEXT_CALLS = {"Text", "MarkupText", "Paragraph", "Tex", "MathTex", "Title", "BulletedList"}

_HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_TAG = re.compile(r"<[^>]+>")
_LABEL = re.compile(
    r"\b(ATLAS|CMS|LHCb)\b\s*(Internal|Preliminary|Simulation|Supplementary|Unofficial"
    r"|Work in [Pp]rogress|Private [Ww]ork|Open Data)"
)
_PRIVATE = [
    re.compile(p)
    for p in (
        r"/afs/",
        r"/eos/",
        r"/project/\w",
        r"/data/[^'\"\s]*/users?/",
        r"\b[A-Za-z]:[\\/]+Users[\\/]+\w",
        r"/home/[a-z]",
        r"/Users/[A-Za-z]",
        r"\blxplus\w*",
        r"\blxbatch\b",
    )
]
_NOQA = re.compile(r"#\s*noqa(?::\s*(?P<codes>[A-Z0-9, ]+))?")
_SKIP_DIRS = {".git", ".manim-hep", "media", "__pycache__", ".venv", "venv", "node_modules"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.message}"


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _number(node: ast.AST) -> float | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    return None


def _check_construct(func: ast.FunctionDef, add) -> None:
    last = func.body[-1]
    wait = None
    if (
        isinstance(last, ast.Expr)
        and isinstance(last.value, ast.Call)
        and isinstance(last.value.func, ast.Attribute)
        and last.value.func.attr == "wait"
        and isinstance(last.value.func.value, ast.Name)
        and last.value.func.value.id == "self"
    ):
        call = last.value
        if call.args:
            wait = _number(call.args[0])
        else:
            given = [k.value for k in call.keywords if k.arg == "duration"]
            wait = _number(given[0]) if given else 1.0  # Scene.wait() defaults to 1 s
    if wait is None or wait > 0.2:
        add(last.lineno, "MH004")


def lint_source(source: str, path: str = "<string>") -> list[Finding]:
    """All findings for one file's source text."""
    try:
        tree = ast.parse(source)
    except SyntaxError as err:
        return [Finding(path, err.lineno or 1, "MH000", f"{MESSAGES['MH000']}: {err.msg}")]
    lines = source.splitlines()
    found: list[Finding] = []

    def add(line: int, code: str, detail: str = "") -> None:
        text = lines[line - 1] if 0 < line <= len(lines) else ""
        m = _NOQA.search(text)
        if m and (not m.group("codes") or code in m.group("codes")):
            return
        found.append(Finding(path, line, code, MESSAGES[code] + (f": {detail}" if detail else "")))

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if _HEX.match(value.strip()):
                add(node.lineno, "MH001", repr(value))
            plain = _TAG.sub("", value)
            if _LABEL.search(plain):
                add(node.lineno, "MH005", repr(plain))
            if any(p.search(value) for p in _PRIVATE):
                add(node.lineno, "MH006", repr(value))
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if node.id in MANIM_COLOURS:
                add(node.lineno, "MH001", node.id)
            elif node.id in MANIMGL_NAMES:
                add(node.lineno, "MH003", node.id)
        elif isinstance(node, ast.Attribute) and node.attr in MANIM_COLOURS:
            add(node.lineno, "MH001", node.attr)
        elif isinstance(node, ast.Call):
            name = _call_name(node)
            if name in COLOUR_CALLS and any(isinstance(a, ast.Constant) for a in node.args):
                add(node.lineno, "MH001", f"{name}(...)")
            if (
                name == "embed"
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "self"
            ):
                add(node.lineno, "MH003", "self.embed()")
            for kw in node.keywords:
                if kw.arg == "font" and isinstance(kw.value, ast.Constant):
                    add(node.lineno, "MH002", repr(kw.value.value))
        elif isinstance(node, ast.Import | ast.ImportFrom):
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else []
            if isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            if any(m == "manimlib" or m.startswith("manimlib.") for m in modules):
                add(node.lineno, "MH003", "manimlib")
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "CONFIG" for t in item.targets
                ):
                    add(item.lineno, "MH003", "CONFIG class dict")
                if isinstance(item, ast.FunctionDef) and item.name == "construct":
                    _check_construct(item, add)
    return sorted(found, key=lambda f: (f.line, f.code))


def _text(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value if isinstance(v, ast.Constant) else "{…}" for v in node.values)
    return None


def onscreen_strings(source: str) -> list[tuple[int, str]]:
    """``(line, text)`` for every string given to a text-making call."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    strings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node) in TEXT_CALLS:
            for arg in node.args:
                text = _text(arg)
                if text is not None:
                    strings.append((node.lineno, text))
    return sorted(strings)


def _files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".py":
            files.append(path)
        elif path.is_dir():
            for candidate in sorted(path.rglob("*.py")):
                if not any(part in _SKIP_DIRS for part in candidate.relative_to(path).parts):
                    files.append(candidate)
    return files


def run(args: argparse.Namespace) -> int:
    if args.paths:
        paths = [Path(p) for p in args.paths]
    else:
        scenes = load_settings().root_dir / "scenes"
        paths = [scenes if scenes.is_dir() else Path.cwd()]
    missing = [p for p in paths if not p.exists()]
    if missing:
        print(f"error: {', '.join(map(str, missing))} not found")
        return 2
    files = _files(paths)
    findings: list[Finding] = []
    listing: list[str] = []
    for file in files:
        raw = file.read_bytes()
        try:  # the encoding Python itself would use (UTF-8, BOM or a coding line)
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source = raw.decode(encoding)
        except (SyntaxError, UnicodeDecodeError, LookupError) as err:
            findings.append(Finding(str(file), 1, "MH000", f"{MESSAGES['MH000']}: {err}"))
            continue
        findings += lint_source(source, str(file))
        strings = onscreen_strings(source)
        if strings:
            listing.append(f"{file}:")
            listing += [f"  {line}: {text!r}" for line, text in strings]
    for finding in findings:
        print(finding)
    if listing:
        print("\nOn-screen strings (compare with the storyline):")
        print("\n".join(listing))
    print(f"\n{len(findings)} finding(s) in {len(files)} file(s)")
    return 1 if findings else 0


def add_parser(sub) -> None:
    p = sub.add_parser(
        "lint",
        help="check scene files against the house rules",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("paths", nargs="*", help="files or folders (default: <root>/scenes)")
    p.set_defaults(func=run)
