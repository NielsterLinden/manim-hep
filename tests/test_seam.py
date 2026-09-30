from __future__ import annotations

import numpy as np
import pytest
from _video import canvas, with_square, write_clip

from manim_hep.cli import main
from manim_hep.cli.frames import ink_fraction, scan, to_1080p
from manim_hep.cli.seam import seam_metrics


def test_identical_frames_pass():
    img = with_square(canvas(), 800, 400)
    result = seam_metrics(img, img.copy())
    assert (result.mean, result.blobs, result.ok) == (0.0, 0, True)


def test_a_shifted_object_fails_on_blobs():
    a = with_square(canvas(), 800, 400)
    b = with_square(canvas(), 830, 400)  # 30 px ≈ 0.12 scene units
    result = seam_metrics(a, b)
    assert result.blobs > 50 and not result.ok


def test_sparse_codec_like_noise_passes():
    rng = np.random.default_rng(0)
    a = with_square(canvas(), 800, 400)
    noise = rng.integers(-3, 4, size=a.shape) * (rng.random(a.shape[:2]) < 0.15)[..., None]
    b = np.clip(a.astype(int) + noise, 0, 255).astype(np.uint8)
    result = seam_metrics(a, b)
    assert result.mean < 0.6 and result.ok


def test_low_resolution_frames_are_judged_at_1080p():
    small = with_square(canvas(854, 480), 300, 200, size=60)
    assert to_1080p(small).shape == (1080, 1920, 3)
    assert seam_metrics(small, small).ok


def test_other_aspect_ratios_are_an_error():
    with pytest.raises(ValueError, match="expected a 16:9 frame, got 1000x1000"):
        to_1080p(canvas(1000, 1000))


def test_ink_fraction_in_the_title_band():
    img = canvas(854, 480)
    band = (-7.2, 2.7, 7.2, 4.0)
    assert ink_fraction(img, band, (255, 255, 255)) == 0.0
    img[:40, :] = 0  # the top 40 rows are inside the band (band = top 78 rows at 480p)
    assert ink_fraction(img, band, (255, 255, 255)) == pytest.approx(40 / 78, abs=0.01)


def test_scan_and_seam_command_on_real_clips(awkward_dir, capsys):
    base = canvas(854, 480)
    a_frames = [with_square(base, 100 + 10 * i, 200, 60) for i in range(8)]
    last = a_frames[-1]
    a = write_clip(awkward_dir / "clip a.mp4", a_frames)
    good = write_clip(awkward_dir / "good.mp4", [last] * 3 + [with_square(base, 400, 100, 60)])
    bad = write_clip(awkward_dir / "bad.mp4", [with_square(base, 300, 200, 60)] * 3)

    s = scan(a, times=[0.2, 99])
    assert s.count == 8 and (s.width, s.height) == (854, 480)
    assert s.duration == pytest.approx(8 / 15)
    assert np.abs(s.frames["t0.2"].astype(int) - a_frames[3].astype(int)).mean() < 2
    assert set(s.frames) == {"first", "last", "t0.2", "t99"}

    assert main(["seam", str(a), str(good)]) == 0
    assert main(["seam", str(a), str(bad)]) == 1
    out = capsys.readouterr().out
    assert "-> OK" in out and "-> FAIL" in out
    assert main(["seam", str(a), str(awkward_dir / "missing.mp4")]) == 2
