"""Probes of Manim behaviour that the skills' trap list relies on (spec §16.1).

They run on every OS in CI, so a Manim upgrade that changes one of these shows
up as a failing test rather than as a surprise in someone's talk.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np
import pytest

from manim_hep.cli.frames import region_pixels, scan

PROBES = textwrap.dedent(
    """
    from manim import FadeOut, Scene, Square, linear
    from manim_hep import use_theme

    use_theme("generic")


    class EndsOnPlay(Scene):
        def construct(self):
            square = Square(2).set_fill("#262A33", 1)
            self.add(square)
            self.play(FadeOut(square), run_time=1, rate_func=linear)


    class EndsOnWait(Scene):
        def construct(self):
            square = Square(2).set_fill("#262A33", 1)
            self.add(square)
            self.play(FadeOut(square), run_time=1, rate_func=linear)
            self.wait(0.1)
    """
)


def _render(folder: Path, scene: str, *flags: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "manim", "render", *flags, "--media_dir", str(folder / "media")]
    return subprocess.run(
        [*cmd, str(folder / "probes.py"), scene],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=folder,
    )


@pytest.fixture(scope="module")
def probes(tmp_path_factory) -> Path:
    folder = tmp_path_factory.mktemp("probes")
    (folder / "probes.py").write_text(PROBES, encoding="utf-8")
    return folder


def _square_ink(folder: Path, scene: str) -> float:
    clip = next((folder / "media" / "videos").rglob(f"{scene}.mp4"))
    last = scan(clip).frames["last"]
    rows, cols = region_pixels(last.shape, (-0.8, -0.8, 0.8, 0.8))
    return float(255 - last[rows, cols].mean())


@pytest.mark.render
def test_last_frame_bug_still_needs_a_final_wait(probes: Path):
    """Trap 1: a clip that ends on a play() rests one frame before the end state.

    With a linear fade at 15 fps the last frame still shows about 1/15 of the square.
    """
    for scene in ("EndsOnPlay", "EndsOnWait"):
        result = _render(probes, scene, "-ql")
        assert result.returncode == 0, result.stderr[-2000:]
    residual = _square_ink(probes, "EndsOnPlay")
    clean = _square_ink(probes, "EndsOnWait")
    assert clean < 1.0, "a final wait gives the true end state"
    assert residual > 5.0, (
        "Manim no longer leaves a residual when a clip ends on play(): "
        "update the trap list and the lint rule (MH004)"
    )


@pytest.mark.render
def test_short_quality_flag_parses(probes: Path):
    """`-qh` works in 0.21 (older notes said to write --quality h)."""
    result = _render(probes, "EndsOnWait", "-qh", "--dry_run")
    assert result.returncode == 0, result.stderr[-2000:]


def test_frames_need_no_ffmpeg_binary():
    """Frames and durations come from PyAV, which ships its own FFmpeg libraries."""
    import av

    assert hasattr(av, "open")
    assert np.__version__
