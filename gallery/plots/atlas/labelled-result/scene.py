"""A dimuon mass plot in ATLAS style, labelled with an explicit status.

Synthetic data: a Z peak (Breit–Wigner with the PDG mass and width, smeared by a
made-up 1.5 GeV resolution) on a falling exponential background, and Poisson
"data" drawn from their sum with a fixed seed. The yields, the luminosity and
the centre-of-mass energy are illustrative only.

The label uses the status meant for unofficial plots and carries a small
"Synthetic data" note, so no frame of this clip can pass for an ATLAS result.
"""

from __future__ import annotations

import itertools

import numpy as np
from manim import (
    DOWN,
    LEFT,
    AnimationGroup,
    Create,
    FadeIn,
    LaggedStart,
    ReplacementTransform,
    Scene,
    Text,
)

from manim_hep import DataAxes, check_order, errorbars, label, stack_hist, use_theme

theme = use_theme("atlas")
C = theme.palette

A = {"axes": (0.35, -0.25)}  # centre of the plot frame

# --- synthetic data -------------------------------------------------------------------
RNG = np.random.default_rng(20260930)
EDGES = np.arange(70.0, 110.0 + 1e-9, 2.0)  # 20 bins of 2 GeV
CENTRES = (EDGES[:-1] + EDGES[1:]) / 2
M_Z, GAMMA_Z = 91.1876, 2.4955  # GeV, PDG
RESOLUTION = 1.5  # GeV, made up
N_SIGNAL, N_BACKGROUND, SLOPE = 4000, 900, 0.045  # made up; SLOPE in 1/GeV


def _binned(density: np.ndarray, grid: np.ndarray, total: float) -> np.ndarray:
    """Integrate a density on a fine grid into the bins, normalised to ``total``."""
    per_bin = [density[(grid >= lo) & (grid < hi)].sum() for lo, hi in itertools.pairwise(EDGES)]
    return total * np.array(per_bin) / sum(per_bin)


def expected_counts() -> tuple[np.ndarray, np.ndarray]:
    """Background and Z signal per bin: exponential, and Breit–Wigner ⊗ Gaussian."""
    grid = np.arange(60.0, 120.0, 0.01)
    breit_wigner = (GAMMA_Z / 2) / np.pi / ((grid - M_Z) ** 2 + (GAMMA_Z / 2) ** 2)
    offsets = np.arange(-6 * RESOLUTION, 6 * RESOLUTION + 1e-9, 0.01)
    kernel = np.exp(-0.5 * (offsets / RESOLUTION) ** 2)
    signal = np.convolve(breit_wigner, kernel / kernel.sum(), mode="same")
    background = np.exp(-SLOPE * (grid - EDGES[0]))
    return _binned(background, grid, N_BACKGROUND), _binned(signal, grid, N_SIGNAL)


BACKGROUND, SIGNAL = expected_counts()
DATA = RNG.poisson(BACKGROUND + SIGNAL).astype(float)


def crisp_text(text: str, font_size: float, color) -> Text:
    """``Text`` rendered at a large size and scaled down.

    Pango spaces small text unevenly ("S ynthetic", "1 3.6"), most visibly with
    the TeX Gyre fonts; rendering large and scaling keeps the letter spacing right.
    """
    return Text(text, font_size=48, color=color).scale(font_size / 48)


def final_state() -> dict:
    """The last frame, built without animation. Dict order = drawing order."""
    axes = DataAxes(
        (70, 110),
        (0, 2000),
        x_length=8.0,
        y_length=4.0,
        x_ticks=[70, 80, 90, 100, 110],
        y_ticks=[0, 500, 1000, 1500, 2000],
        # µ is the micro sign (U+00B5): it is in the TeX Gyre fonts, Greek μ is not.
        x_title="m<sub>µµ</sub> [GeV]",
        y_title="Events / 2 GeV",
    ).move_frame_to(A["axes"])
    stack = stack_hist(axes, EDGES, [("background", BACKGROUND), ("Z", SIGNAL)])
    stack.set_z_index(-1)  # the frame and ticks stay on top of the filled histogram
    data = errorbars(axes, CENTRES, DATA, yerr=np.sqrt(DATA))
    lab = label("atlas", status="Work in Progress", sqrt_s=13.6, lumi=50, target=axes)
    note = crisp_text("Synthetic data", axes.y_labels[0].font_size * 0.8, C.muted)
    note.next_to(lab, DOWN, aligned_edge=LEFT, buff=0.12)
    return {"stack": stack, "axes": axes, "data": data, "label": lab, "note": note}


class AtlasLabelledResult(Scene):
    def construct(self):
        state = final_state()
        axes, stack, data = state["axes"], state["stack"], state["data"]

        # Animating the parts with group=axes keeps the axes one object in the scene.
        parts = (axes.ticks, axes.x_labels, axes.y_labels, axes.x_title, axes.y_title)
        self.play(
            AnimationGroup(
                Create(axes.frame), *(FadeIn(p) for p in parts), lag_ratio=0.12, group=axes
            ),
            run_time=1.4,
        )
        empty = stack_hist(axes, EDGES, [("background", 0 * BACKGROUND), ("Z", 0 * SIGNAL)])
        empty.set_z_index(-1)
        self.play(ReplacementTransform(empty, stack), run_time=1.8)
        self.play(
            LaggedStart(*(FadeIn(point) for point in data), lag_ratio=0.08, group=data),
            run_time=1.8,
        )
        self.play(FadeIn(state["label"]), run_time=0.8)
        self.play(FadeIn(state["note"]), run_time=0.5)
        check_order(self, state)
        self.wait(0.1)
