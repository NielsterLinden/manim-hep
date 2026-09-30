"""Template fit: a signal strength μ scales the signal template until the prediction
matches the data best, at the minimum of −2ΔlnL.

One clip, ``TemplateFit``:

- data with a fixed background template and a signal template scaled by μ;
- μ sweeps from 0 to 2: the signal layer of the stack grows and −2ΔlnL(μ) is traced;
- μ settles at the best fit μ̂, and the 1σ interval is read off where −2ΔlnL = 1.

The data never move: only the prediction changes.

Physics honesty: the templates and the pseudo-data are synthetic. The background is an
exponential with a fixed normalisation (no nuisance parameters), the signal a Gaussian
at 125 GeV with σ = 3 GeV. The data are one Poisson draw of b + s (μ_true = 1) with the
seed below; that seed gives a typical draw (μ̂ within 0.1σ of μ_true). μ̂, the
likelihood curve and the interval are computed exactly from the Poisson likelihood.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    DL,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    UR,
    Create,
    DashedLine,
    DecimalNumber,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Scene,
    Square,
    ValueTracker,
    VGroup,
    linear,
    smooth,
)

from manim_hep import DataAxes, check_order, errorbars, stack_hist, use_theme
from manim_hep.palette import tint

theme = use_theme()
C = theme.palette
COLOUR_B = tint(C.theory, 0.5)
COLOUR_S = C.highlight

# --- templates, pseudo-data and the likelihood -------------------------------------------
EDGES = np.linspace(100, 160, 31)  # 2 GeV bins
CENTRES = (EDGES[:-1] + EDGES[1:]) / 2
S_NOMINAL, B_TOTAL, SLOPE, M_SIGNAL, WIDTH = 55.0, 1500.0, 40.0, 125.0, 3.0


def _gauss_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf((x - M_SIGNAL) / (WIDTH * math.sqrt(2))))


S_TEMPLATE = S_NOMINAL * np.diff([_gauss_cdf(e) for e in EDGES])  # events at μ = 1
_exp = np.diff(1 - np.exp(-(EDGES - EDGES[0]) / SLOPE))
B_TEMPLATE = B_TOTAL * _exp / _exp.sum()

MU_TRUE = 1.0
RNG = np.random.default_rng(20260940)
DATA = RNG.poisson(B_TEMPLATE + MU_TRUE * S_TEMPLATE)


def nll2(mu: float) -> float:
    """−2 ln L(μ) for Poisson bins, up to a constant."""
    nu = B_TEMPLATE + mu * S_TEMPLATE
    return float(2 * np.sum(nu - DATA * np.log(nu)))


def _fit() -> float:
    mu = 1.0
    for _ in range(50):  # Newton's method on d(−2 ln L)/dμ = 0
        nu = B_TEMPLATE + mu * S_TEMPLATE
        grad = 2 * np.sum(S_TEMPLATE * (1 - DATA / nu))
        curv = 2 * np.sum(DATA * S_TEMPLATE**2 / nu**2)
        mu -= grad / curv
    return float(mu)


MU_HAT = _fit()
MU_GRID = np.linspace(0, 2, 401)
Q = np.array([nll2(m) for m in MU_GRID]) - nll2(MU_HAT)  # −2ΔlnL
_below, _above = MU_GRID < MU_HAT, MU_GRID > MU_HAT
MU_LO = float(np.interp(1.0, Q[_below][::-1], MU_GRID[_below][::-1]))
MU_HI = float(np.interp(1.0, Q[_above], MU_GRID[_above]))

# --- layout -----------------------------------------------------------------------------
A = {"data": (-2.8, -0.45), "likelihood": (4.2, -0.45)}
FONT = 34


def data_axes() -> DataAxes:
    return DataAxes(
        (100, 160),
        (0, 120),
        x_length=5.8,
        y_length=3.7,
        x_ticks=[100, 110, 120, 130, 140, 150, 160],
        y_ticks=[0, 40, 80, 120],
        x_title="m [GeV]",
        y_title="Events / 2 GeV",
    ).move_frame_to(A["data"])


def likelihood_axes() -> DataAxes:
    return DataAxes(
        (0, 2),
        (0, 12),
        x_length=4.2,
        y_length=3.7,
        x_ticks=[0, 0.5, 1, 1.5, 2],
        y_ticks=[1, 4, 9],  # the 1σ, 2σ and 3σ levels
        x_title=MathTex(r"\mu", font_size=FONT + 4),
        y_title=MathTex(r"-2\Delta\ln L", font_size=FONT),
    ).move_frame_to(A["likelihood"])


def stack_at(axes: DataAxes, mu: float):
    return stack_hist(axes, EDGES, [("b", B_TEMPLATE, COLOUR_B), ("s", mu * S_TEMPLATE, COLOUR_S)])


def trace_to(axes: DataAxes, mu: float):
    """−2ΔlnL from μ = 0 up to ``mu``."""
    upto = mu >= MU_GRID
    xs = [*MU_GRID[upto], mu]
    return axes.polyline(xs, [*Q[upto], float(np.interp(mu, MU_GRID, Q))], color=C.ink)


def point_on_curve(axes: DataAxes, mu: float):
    return axes.c2p(mu, float(np.interp(mu, MU_GRID, Q)))


def key() -> VGroup:
    """Symbols for data, signal and background."""
    marker = VGroup(Line(DOWN * 0.13, UP * 0.13, color=C.data), Dot(radius=0.06, color=C.data))
    rows = [
        (marker, "n"),
        (Square(0.24, stroke_width=0, fill_color=COLOUR_S, fill_opacity=1), r"\mu\, s"),
        (Square(0.24, stroke_width=0, fill_color=COLOUR_B, fill_opacity=1), "b"),
    ]
    group = VGroup()
    for symbol, tex in rows:
        text = MathTex(tex, font_size=FONT).next_to(symbol, RIGHT, buff=0.18)
        group.add(VGroup(symbol, text))
    return group.arrange(DOWN, aligned_edge=LEFT, buff=0.16)


def state_fit() -> dict:
    """Last frame of TemplateFit."""
    axes, lik = data_axes(), likelihood_axes()
    readout = VGroup(MathTex(r"\mu =", font_size=FONT), DecimalNumber(MU_HAT, 2, font_size=FONT))
    # Put the digits on the baseline: μ has a descender, so centring would set them low.
    reference = MathTex(r"\mu = 0", font_size=FONT)
    reference.shift(readout[0][0][0].get_corner(DL) - reference[0][0].get_corner(DL))
    readout[1].move_to(reference[0][2].get_corner(DL), aligned_edge=DL)
    readout.move_to(axes.frame.get_corner(UR) + np.array([-0.3, -0.3, 0]), aligned_edge=UR)
    legend = key().next_to(readout, DOWN, buff=0.3).align_to(readout, RIGHT)
    one = DashedLine(lik.c2p(0, 1), lik.c2p(2, 1), color=C.muted, stroke_width=2)
    interval = VGroup(
        DashedLine(lik.c2p(MU_LO, 0), lik.c2p(MU_LO, 1), color=C.highlight, stroke_width=2),
        DashedLine(lik.c2p(MU_HI, 0), lik.c2p(MU_HI, 1), color=C.highlight, stroke_width=2),
        Line(lik.c2p(MU_LO, 1), lik.c2p(MU_HI, 1), color=C.highlight, stroke_width=5),
    )
    result = MathTex(
        rf"\hat\mu = {MU_HAT:.2f}^{{+{MU_HI - MU_HAT:.2f}}}_{{-{MU_HAT - MU_LO:.2f}}}",
        font_size=FONT + 2,
    ).move_to(lik.c2p(1.0, 10.2))
    dot = Dot(point_on_curve(lik, MU_HAT), radius=0.08, color=C.highlight).set_z_index(1)
    return {
        "axes": axes,
        "stack": stack_at(axes, MU_HAT),
        "data": errorbars(axes, CENTRES, DATA, yerr=np.sqrt(DATA)),
        "key": legend,
        "readout": readout,
        "likelihood": lik,
        "one_sigma": one,
        "curve": lik.polyline(MU_GRID, Q, color=C.ink),
        "interval": interval,
        "result": result,
        "dot": dot,  # z_index 1: drawn last
    }


class TemplateFit(Scene):
    def construct(self):
        state = state_fit()
        axes, lik = state["axes"], state["likelihood"]
        stack, number, curve, dot = (
            state["stack"],
            state["readout"][1],
            state["curve"],
            state["dot"],
        )
        mu = ValueTracker(0.0)

        # Start every μ-dependent object at μ = 0, then let it follow the tracker.
        stack.become(stack_at(axes, 0.0))
        number.set_value(0.0)
        curve.become(trace_to(lik, 0.0))
        dot.move_to(point_on_curve(lik, 0.0))

        self.play(FadeIn(axes), FadeIn(stack), FadeIn(state["data"]), run_time=1.4)
        self.play(
            FadeIn(state["key"]),
            FadeIn(state["readout"]),
            FadeIn(lik),
            Create(state["one_sigma"]),
            FadeIn(dot, scale=1.5),
            run_time=1.0,
        )
        self.add(curve)
        stack.add_updater(lambda m: m.become(stack_at(axes, mu.get_value())))
        number.add_updater(lambda m: m.set_value(mu.get_value()))
        curve.add_updater(lambda m: m.become(trace_to(lik, mu.get_value())))
        dot.add_updater(lambda m: m.move_to(point_on_curve(lik, mu.get_value())))
        self.play(mu.animate.set_value(2.0), run_time=5.0, rate_func=linear)

        curve.clear_updaters()
        curve.become(lik.polyline(MU_GRID, Q, color=C.ink))
        self.play(mu.animate.set_value(MU_HAT), run_time=1.8, rate_func=smooth)
        for mob in (stack, number, dot):
            mob.clear_updaters()
        self.remove(mu)

        self.play(Create(state["interval"]), FadeIn(state["result"]), run_time=1.0)
        check_order(self, state)
        self.wait(0.1)
