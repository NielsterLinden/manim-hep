"""Graphical regression tests (spec §11): key primitives drawn to one frame and compared
with reference images in ``tests/golden/``.

Text is left out on purpose: font rasterisation differs between operating systems, while
cairo draws shapes the same everywhere within the tolerance used here. After an
intended change, regenerate the references with ``MANIM_HEP_UPDATE_GOLDEN=1 pytest
tests/test_graphics.py`` and look at the new images before committing them.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pytest
from manim import Camera
from PIL import Image

from manim_hep import (
    BarrelSlice,
    DataAxes,
    FeynmanDiagram,
    band,
    errorbars,
    signature,
    stack_hist,
    step_hist,
    use_theme,
)

GOLDEN = Path(__file__).parent / "golden"
UPDATE = os.environ.get("MANIM_HEP_UPDATE_GOLDEN") == "1"
SIZE = (480, 270)


def feynman():
    vertices = {
        "q": (-4, 1.5), "qbar": (-4, -1.5), "a": (-2, 0), "b": (0, 0),
        "l-": (2, 1.5), "l+": (2, -1.5), "g0": (2.5, -2.5), "g1": (5.5, -2.5),
        "h0": (2.5, 2.5), "h1": (5.5, 2.5),
    }  # fmt: skip
    edges = [
        ("q", "a", "fermion"),
        ("a", "qbar", "fermion"),
        ("a", "b", "photon"),
        ("b", "l-", "fermion"),
        ("l+", "b", "antifermion"),
        ("g0", "g1", "gluon"),
        ("h0", "h1", "scalar"),
    ]
    return [FeynmanDiagram(vertices, edges)]


def plot():
    axes = DataAxes((0, 10), (0, 100), show_x_labels=False, show_y_labels=False)
    edges = np.linspace(0, 10, 11)
    background = np.array([60, 50, 42, 35, 30, 25, 21, 18, 15, 12], dtype=float)
    signal = np.array([0, 2, 10, 25, 30, 20, 8, 2, 0, 0], dtype=float)
    stack = stack_hist(axes, edges, [("b", background), ("s", signal)])
    total = background + signal
    unc = band(axes, edges, total * 0.93, total * 1.07, step=True)
    outline = step_hist(axes, edges, total)
    centres = (edges[:-1] + edges[1:]) / 2
    noise = np.array([3, -4, 2, 5, -3, 1, -2, 2, -1, 1], dtype=float)
    data = errorbars(axes, centres, total + noise, yerr=np.sqrt(total))
    return [stack, unc, outline, axes, data]


def detector():
    det = BarrelSlice().scale(0.8)
    kinds = [("muon", 1.0, 1), ("electron", 0.2, -1), ("jet", -1.0, 1), ("photon", 2.5, 1)]
    return [det, *(signature(k, det, phi=phi, charge=q) for k, phi, q in kinds)]


def draw(build) -> np.ndarray:
    theme = use_theme("generic")
    camera = Camera(
        pixel_width=SIZE[0], pixel_height=SIZE[1], background_color=theme.palette.background
    )
    camera.capture_mobjects(build())
    return np.asarray(camera.get_image().convert("L"), dtype=float)


@pytest.mark.parametrize("build", [feynman, plot, detector], ids=lambda f: f.__name__)
def test_primitives_look_the_same(build):
    got = draw(build)
    reference = GOLDEN / f"{build.__name__}.png"
    if UPDATE or not reference.exists():
        GOLDEN.mkdir(exist_ok=True)
        Image.fromarray(got.astype(np.uint8)).save(reference)
        if not UPDATE:
            pytest.fail(f"no reference yet: wrote {reference.name}; check it and commit it")
        return
    want = np.asarray(Image.open(reference).convert("L"), dtype=float)
    assert got.shape == want.shape
    diff = np.abs(got - want)
    # antialiasing may differ slightly between cairo builds; moved geometry does not hide
    assert diff.mean() < 1.5, f"mean difference {diff.mean():.2f}"
    assert (diff > 64).mean() < 0.004, f"{(diff > 64).mean():.2%} of pixels changed"
