"""``manim-hep doctor``: is this machine ready to render HEP animations?

Checks Python, Manim Community Edition 0.21, LaTeX (for ``MathTex``), the
bundled fonts and write access, and prints the fix for your platform
(Windows, macOS, Linux, lxplus or another cluster). Exits non-zero when
something needed is missing. With ``--no-tex``, missing LaTeX is reported but
not counted: scenes must then avoid ``MathTex`` and ``Tex``.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from manim_hep._settings import find_settings, load_settings

# What Manim's default TeX template (standalone + preview, babel english, AMS) needs.
TEX_FILES = (
    "standalone.cls",
    "preview.sty",
    "babel.sty",
    "english.ldf",
    "amsmath.sty",
    "amssymb.sty",
)

LATEX_FIX = {
    "windows": (
        "install MiKTeX (https://miktex.org/download, or `winget install MiKTeX.MiKTeX`) or "
        "TeX Live, open a new terminal, then: miktex packages install standalone preview "
        "babel-english"
    ),
    "macos": (
        "brew install --cask basictex, open a new terminal, then: sudo tlmgr update --self && "
        "sudo tlmgr install standalone preview babel-english dvisvgm (or install MacTeX)"
    ),
    "linux": (
        "Debian/Ubuntu: sudo apt install texlive texlive-latex-extra dvisvgm; "
        "Fedora: sudo dnf install texlive-scheme-medium texlive-dvisvgm"
    ),
    "lxplus": (
        "export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux:$PATH "
        "(add it to your shell profile)"
    ),
    "cluster": (
        "put a full TeX Live on PATH, e.g. from CVMFS: "
        "/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux; "
        "a bare texlive-core package is not enough"
    ),
}
MANIM_FIX = (
    'pip install "manim>=0.21,<0.22"  (see https://docs.manim.community for system libraries)'
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    fix: str = ""
    counts: bool = True  # False: reported, but not a failure


def detect_platform() -> str:
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    if socket.gethostname().lower().startswith("lxplus"):
        return "lxplus"
    if Path("/cvmfs/sft.cern.ch").is_dir() or os.environ.get("SLURM_JOB_ID"):
        return "cluster"
    return "linux"


def _which(name: str) -> str | None:
    return shutil.which(name)


def _kpsewhich(filename: str) -> bool:
    exe = _which("kpsewhich")
    if exe is None:
        return False
    try:
        out = subprocess.run([exe, filename], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0 and bool(out.stdout.strip())


def _version(distribution: str) -> str | None:
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def _import_error() -> str | None:
    """Why ``import manim`` fails (missing system libraries show up here), or None."""
    code = "import manim"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    return None if out.returncode == 0 else (out.stderr.strip().splitlines() or ["?"])[-1]


def check_python() -> Check:
    v = sys.version_info
    ok = v >= (3, 11)
    return Check("Python", ok, f"{v.major}.{v.minor}.{v.micro}", "" if ok else "use Python 3.11+")


def check_manim() -> Check:
    version = _version("manim")
    if version is None:
        if _version("manimgl"):
            return Check("Manim", False, "only ManimGL (3b1b/manim) is installed", MANIM_FIX)
        return Check("Manim", False, "Manim Community Edition is not installed", MANIM_FIX)
    if not version.startswith("0.21."):
        return Check("Manim", False, f"Manim Community Edition {version}, need 0.21.x", MANIM_FIX)
    error = _import_error()
    if error:
        return Check("Manim", False, f"`import manim` fails: {error}", MANIM_FIX)
    return Check("Manim", True, f"Manim Community Edition {version}")


def check_latex(platform: str, tex: bool) -> list[Check]:
    fix = LATEX_FIX[platform]
    checks = []
    for tool in ("latex", "dvisvgm"):
        path = _which(tool)
        checks.append(Check(f"LaTeX: {tool}", bool(path), path or "not on PATH", fix, tex))
    if checks[0].ok:
        missing = [f for f in TEX_FILES if not _kpsewhich(f)]
        detail = "all found" if not missing else "missing " + ", ".join(missing)
        checks.append(Check("LaTeX: packages", not missing, detail, fix, tex))
    return checks


def check_fonts() -> Check:
    fonts = sorted((Path(__file__).parents[1] / "fonts").glob("DejaVuSans*.ttf"))
    if len(fonts) < 4:
        return Check("fonts", False, "bundled DejaVu Sans files are missing", "reinstall manim-hep")
    try:
        import manimpango

        ok = bool(manimpango.register_font(str(fonts[0])))
    except Exception as err:  # manimpango failures vary by platform
        return Check("fonts", False, f"cannot register fonts: {err}", MANIM_FIX)
    note = (
        " (Windows: the first text of each render takes a few seconds)" if os.name == "nt" else ""
    )
    return Check("fonts", ok, "DejaVu Sans (bundled)" + note, "" if ok else MANIM_FIX)


def check_write(project: Path) -> Check:
    folder = project / ".manim-hep"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=folder):
            pass
    except OSError as err:
        return Check(
            "write access", False, f"{folder}: {err}", "run from a folder you can write to"
        )
    return Check("write access", True, str(folder))


def run_checks(platform: str, tex: bool = True) -> list[Check]:
    settings_file = find_settings()
    project = settings_file.parent if settings_file else Path.cwd()
    settings_error = None
    if settings_file:
        try:
            s = load_settings(settings_file)
        except (ValueError, OSError) as err:  # includes TOML syntax errors
            settings_error = str(err)
    checks = [check_python(), check_manim(), *check_latex(platform, tex), check_fonts()]
    checks.append(check_write(project))
    if settings_error:
        checks.append(Check("settings", False, settings_error, "fix manim-hep.toml"))
    elif settings_file:
        detail = f"{settings_file} (experiment {s.experiment}, root {s.root})"
        checks.append(Check("settings", True, detail, counts=False))
    else:
        checks.append(
            Check("settings", False, "no manim-hep.toml", "run `manim-hep init`", counts=False)
        )
    return checks


def run(args: argparse.Namespace) -> int:
    platform = detect_platform()
    print(f"manim-hep doctor (platform: {platform})")
    checks = run_checks(platform, tex=not args.no_tex)
    problems = 0
    for c in checks:
        if c.ok:
            tag = "[ok]  "
        elif c.counts:
            tag = "[FAIL]"
            problems += 1
        else:
            tag = "[note]"
        print(f"{tag} {c.name}: {c.detail}")
        if not c.ok and c.fix:
            print(f"       fix: {c.fix}")
    print("all good" if not problems else f"{problems} problem(s) to fix")
    return 1 if problems else 0


def add_parser(sub) -> None:
    p = sub.add_parser(
        "doctor",
        help="check Python, Manim, LaTeX, fonts and write access",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--no-tex", action="store_true", help="do not count missing LaTeX as a failure")
    p.set_defaults(func=run)
