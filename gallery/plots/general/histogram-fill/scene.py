"""Filling a histogram: one event gives one entry, and entries add up to a peak.

The first entries land on a zoomed-in axis (0–12 events) so each one is visible;
before the rest of the sample rains in, the axis rescales to 0–60 while the tick
marks stay where they are.

Physics honesty: the masses are seeded synthetic draws from a Gaussian around
m_Z = 91.1876 GeV (PDG) with a width of 2.8 GeV that stands in for the natural
width and the detector resolution together (schematic, not a real line shape).
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    DR,
    RIGHT,
    UL,
    UP,
    Dot,
    FadeIn,
    FadeOut,
    Integer,
    LaggedStart,
    MathTex,
    Scene,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    linear,
    rate_functions,
)

from manim_hep import DataAxes, check_order, step_hist, use_theme

theme = use_theme()
C = theme.palette

M_Z, WIDTH = 91.1876, 2.8  # GeV
EDGES = np.arange(80.0, 102.0 + 1e-9, 2.0)
N_EVENTS, N_SINGLE, N_RAIN = 150, 5, 40
Y_ZOOM, Y_FULL = 12, 60  # both give seven ticks at the same heights

RNG = np.random.default_rng(7)
_draws = RNG.normal(M_Z, WIDTH, 400)
MASSES = _draws[(_draws > EDGES[0]) & (_draws < EDGES[-1])][:N_EVENTS]

A = {"frame": (0.3, -0.95), "drop_height": 0.75}


def counts(n: int) -> np.ndarray:
    return np.histogram(MASSES[:n], EDGES)[0].astype(float)


def make_axes(y_max: float) -> DataAxes:
    axes = DataAxes(
        (EDGES[0], EDGES[-1]),
        (0, y_max),
        x_length=7.5,
        y_length=3.8,
        y_ticks=np.linspace(0, y_max, 7),
        x_title="m<sub>ℓℓ</sub> [GeV]",
        y_title="Events / 2 GeV",
    )
    return axes.move_frame_to(A["frame"])


def make_hist(axes: DataAxes, n: int) -> VGroup:
    """Filled steps plus an outline; both keep their point count as ``n`` changes."""
    c = counts(n)
    fill = step_hist(axes, EDGES, c, color=C.theory, fill_opacity=0.25, stroke_width=0)
    outline = step_hist(axes, EDGES, c, color=C.theory, stroke_width=3)
    if n == 0:
        outline.set_stroke(opacity=0)
    return VGroup(fill, outline)


def make_counter(axes: DataAxes, value: int) -> VGroup:
    label = MathTex("N =", font_size=36)
    number = Integer(value, font_size=36).next_to(label, RIGHT, buff=0.15)
    number.align_to(label, DOWN)
    group = VGroup(label, number)
    group.next_to(axes.frame.get_corner(UL), DR, buff=0.25)
    group.number = number
    return group


def entry_dot(axes: DataAxes, mass: float, lift: float = 0.0) -> Dot:
    top = axes.c2p(mass, axes.y_max)
    return Dot(top + UP * (A["drop_height"] + lift), radius=0.07, color=C.data)


def landing(axes: DataAxes, mass: float, n_before: int) -> np.ndarray:
    """Where an entry lands: on top of its bin as it was before the entry."""
    b = int(np.searchsorted(EDGES, mass, side="right") - 1)
    return axes.c2p(mass, counts(n_before)[b])


def fall(dot: Dot, end: np.ndarray) -> UpdateFromAlphaFunc:
    """Appear, fall with gravity-like easing, and fade out on landing."""
    start = dot.get_center()

    def update(m, alpha):
        m.move_to(start + (end - start) * rate_functions.ease_in_quad(alpha))
        m.set_opacity(min(1.0, 6 * alpha) * (1 - max(0.0, (alpha - 0.85) / 0.15)))

    return UpdateFromAlphaFunc(dot, update)


def final_state() -> dict:
    axes = make_axes(Y_FULL)
    return {
        "axes": axes,
        "hist": make_hist(axes, N_EVENTS),
        "counter": make_counter(axes, N_EVENTS),
    }


class HistogramFill(Scene):
    def construct(self):
        axes = make_axes(Y_ZOOM)
        hist = make_hist(axes, 0)
        counter = make_counter(axes, 0)
        self.play(FadeIn(axes), run_time=0.8)
        self.add(hist)

        # One event: its mass, one dot, one entry.
        first = entry_dot(axes, MASSES[0])
        value = MathTex(rf"m_{{\ell\ell}} = {MASSES[0]:.1f}\ \mathrm{{GeV}}", font_size=34)
        value.next_to(first, RIGHT, buff=0.25)
        self.play(FadeIn(first), FadeIn(value), FadeIn(counter), run_time=0.4)
        self.play(
            first.animate.move_to(landing(axes, MASSES[0], 0)),
            FadeOut(value),
            run_time=0.7,
            rate_func=rate_functions.ease_in_quad,
        )
        self.play(
            Transform(hist, make_hist(axes, 1)),
            FadeOut(first),
            counter.number.animate.set_value(1),
            run_time=0.3,
        )

        # A few more, one at a time and faster.
        for n in range(1, N_SINGLE):
            dot = entry_dot(axes, MASSES[n])
            self.play(FadeIn(dot), run_time=0.12)
            self.play(
                dot.animate.move_to(landing(axes, MASSES[n], n)),
                run_time=0.35,
                rate_func=rate_functions.ease_in_quad,
            )
            self.play(
                Transform(hist, make_hist(axes, n + 1)),
                FadeOut(dot),
                counter.number.animate.set_value(n + 1),
                run_time=0.15,
            )

        # Zoom out: the y labels cross-fade from 0–12 to 0–60; frame and ticks stay.
        full = make_axes(Y_FULL)
        self.play(
            FadeOut(axes.y_labels),
            FadeIn(full.y_labels),
            Transform(hist, make_hist(full, N_SINGLE)),
            run_time=0.8,
        )
        self.remove(*axes.submobjects, full.y_labels)
        self.add(full)
        self.bring_to_back(full)  # identical frame, ticks and titles: no visible change

        # Then it rains: the rest of the sample fills the peak.
        masses = MASSES[N_SINGLE : N_SINGLE + N_RAIN]
        rain = [entry_dot(full, m, lift=float(RNG.uniform(0.0, 0.4))) for m in masses]
        self.add(*rain)
        self.play(
            LaggedStart(
                *(fall(d, full.c2p(m, 0)) for d, m in zip(rain, masses, strict=True)),
                lag_ratio=0.08,
            ),
            Transform(hist, make_hist(full, N_EVENTS), rate_func=linear),
            counter.number.animate(rate_func=linear).set_value(N_EVENTS),
            run_time=3.2,
        )
        self.remove(*rain)
        check_order(self, {"axes": full, "hist": hist, "counter": counter})
        self.wait(0.1)
