"""``manim-hep render FILE SCENE``: render one scene, grab its frames, check safe areas.

- Renders one scene at a time: a lock in ``.manim-hep/`` makes parallel calls wait,
  because concurrent ``MathTex`` compiles race on Manim's cache.
- Low quality (854×480, 15 fps) by default; ``--final`` renders 1920×1080 at 60 fps.
- Writes the first and last frames (and any ``--frames`` times) as PNGs next to
  the scratch copy in ``.manim-hep/work/<slug>/``, for you or your agent to look at.
- Warns when anything is drawn in the title band or a keep-out area in any frame.
- ``--final`` also delivers ``<root>/clips/<slug>_vK.mp4`` and
  ``<root>/clips/<slug>_vK_final.png`` with the next free version K; an existing
  version is never overwritten.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

from manim_hep._settings import load_settings
from manim_hep.cli.frames import FRAME_HEIGHT, FRAME_WIDTH, save_png, scan, time_key

WARN_FRACTION = 0.001  # more than 0.1 % of a region in ink is an intrusion


def kebab(name: str) -> str:
    """``DrellYan`` → ``drell-yan``; ``ROCCurve`` → ``roc-curve``."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "-", name)
    return re.sub(r"[^a-z0-9]+", "-", spaced.lower()).strip("-")


@contextmanager
def render_lock(path: Path, timeout: float = 3600.0):
    """An exclusive lock on ``path`` that works on Windows, macOS and Linux."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a+b") as handle:
        start, told = time.monotonic(), False
        while True:
            try:
                if os.name == "nt":
                    import msvcrt

                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if not told:
                    print("waiting for another manim-hep render to finish ...", flush=True)
                    told = True
                if time.monotonic() - start > timeout:
                    raise TimeoutError(f"gave up waiting for {path}") from None
                time.sleep(0.5)
        try:
            yield
        finally:
            if os.name == "nt":
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def next_version(folder: Path, slug: str) -> int:
    pattern = re.compile(re.escape(slug) + r"_v(\d+)\.mp4$")
    found = [int(m.group(1)) for p in folder.glob(f"{slug}_v*.mp4") if (m := pattern.match(p.name))]
    return 1 + max(found, default=0)


def _parse_times(text: str) -> list[float]:
    times = []
    for part in filter(None, (p.strip() for p in text.split(","))):
        try:
            times.append(float(part))
        except ValueError:
            raise SystemExit(f"error: --frames takes seconds like 1.5,3; got {part!r}") from None
    return times


def run(args: argparse.Namespace) -> int:
    file = Path(args.file).resolve()
    if not file.is_file():
        print(f"error: {args.file} not found")
        return 2
    settings = load_settings(search_from=file)
    project = settings.project_dir or Path.cwd().resolve()
    slug = args.slug or kebab(args.scene)
    work = project / ".manim-hep" / "work" / slug
    work.mkdir(parents=True, exist_ok=True)
    times = _parse_times(args.frames)
    quality = "h" if args.final else "l"

    cmd = [
        sys.executable, "-m", "manim", "render",
        "--quality", quality,
        "--progress_bar", "none",
        "--media_dir", str(work / "media"),
        "-o", slug,
        str(file), args.scene,
    ]  # fmt: skip
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    with render_lock(project / ".manim-hep" / "render.lock"):
        started = time.time()
        print(f"rendering {args.scene} from {file.name} ({'1080p60' if args.final else '480p15'})")
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env
        )
        log = work / "render.log"
        log.write_text(proc.stdout + proc.stderr, encoding="utf-8")
        candidates = [
            p
            for p in (work / "media" / "videos").rglob(f"{slug}.mp4")
            if p.stat().st_mtime >= started - 1
        ]
        if proc.returncode != 0 or not candidates:
            tail = (proc.stdout + proc.stderr).strip().splitlines()[-25:]
            print("\n".join(tail))
            reason = f"manim exited with {proc.returncode}" if proc.returncode else "no MP4 written"
            print(f"render FAILED ({reason}); full log: {log}")
            return 1
        produced = max(candidates, key=lambda p: p.stat().st_mtime)
        clip = work / f"{slug}.mp4"
        shutil.copy2(produced, clip)

    regions = {
        "title band": (-FRAME_WIDTH / 2, settings.title_band, FRAME_WIDTH / 2, FRAME_HEIGHT / 2)
    }
    for i, box in enumerate(settings.keep_out, start=1):
        regions[f"keep-out {i}"] = box
    result = scan(clip, times=times, regions=regions, step=1 if quality == "l" else 4)
    size = f"{result.width}x{result.height}"
    print(f"clip: {clip}  ({size}, {result.duration:.2f} s, {result.count} frames)")
    for key in ["first", *(time_key(t) for t in times), "last"]:
        png = save_png(result.frames[key], work / f"{slug}_{key}.png")
        print(f"frame {key}: {png}")
    warnings = 0
    for name, (fraction, at) in result.worst.items():
        if fraction > WARN_FRACTION:
            warnings += 1
            print(f"WARNING: {name} has ink ({fraction:.2%} of it) at t = {at:.2f} s")
    if not warnings:
        print("safe areas: clear")

    if args.final:
        clips = settings.root_dir / "clips"
        clips.mkdir(parents=True, exist_ok=True)
        version = next_version(clips, slug)
        delivered = clips / f"{slug}_v{version}.mp4"
        shutil.copy2(clip, delivered)
        final_png = save_png(result.frames["last"], clips / f"{slug}_v{version}_final.png")
        print(f"DELIVERED: {delivered}")
        print(f"DELIVERED: {final_png}")
    return 0


def add_parser(sub) -> None:
    p = sub.add_parser(
        "render",
        help="render one scene, grab frames, check the safe areas",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("file", help="the scene file")
    p.add_argument("scene", help="the Scene class to render")
    p.add_argument("--final", action="store_true", help="1080p60, delivered to clips/")
    p.add_argument("--frames", default="", help="extra frame times in seconds, e.g. 1.5,3")
    p.add_argument("--slug", default=None, help="clip name (default: the scene name in kebab-case)")
    p.set_defaults(func=run)
