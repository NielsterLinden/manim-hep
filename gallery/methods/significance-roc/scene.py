"""Significance and ROC: sweeping a cut on a classifier score.

Two chained clips:

- ``RocSweep``: signal and background score distributions; a cut sweeps from 0 to 1,
  the accepted parts are shaded, and the operating point (ε_B, ε_S) traces the ROC
  curve. The area under it is shown at the end.
- ``CutSignificance``: opens on the sweep's last frame. The ROC panel gives way to the
  expected significance Z_A against the cut; the cut sweeps again and settles where
  Z_A is largest.

Physics honesty: the scores are seeded samples of Beta(5, 2) (signal) and Beta(2, 3)
(background); the yields before the cut, s = 40 and b = 400 events, are schematic.
Z_A is the Asimov median discovery significance (Cowan et al. 2011), which reduces to
s/√b for s ≪ b. It is only drawn where at least one background event is expected,
because the asymptotic formula is not trustworthy below that.
"""

from __future__ import annotations

import itertools

import numpy as np
from manim import (
    DOWN,
    UP,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    Polygon,
    Scene,
    ValueTracker,
    VMobject,
    always_redraw,
    linear,
    smooth,
)

from manim_hep import DataAxes, add_state, check_order, step_hist, use_theme

theme = use_theme()
C = theme.palette

# --- the synthetic classifier ----------------------------------------------------------
RNG = np.random.default_rng(20260930)
N_MC = 50_000
SIGNAL = RNG.beta(5, 2, N_MC)
BACKGROUND = RNG.beta(2, 3, N_MC)
S_TOTAL, B_TOTAL = 40.0, 400.0  # expected events before the cut (schematic)

EDGES = np.linspace(0, 1, 26)
FRAC_S = np.histogram(SIGNAL, EDGES)[0] / N_MC  # fraction of events per bin
FRAC_B = np.histogram(BACKGROUND, EDGES)[0] / N_MC

CUTS = np.linspace(0, 1, 401)
EPS_S = 1 - np.searchsorted(np.sort(SIGNAL), CUTS, side="right") / N_MC
EPS_B = 1 - np.searchsorted(np.sort(BACKGROUND), CUTS, side="right") / N_MC
AUC = np.searchsorted(np.sort(BACKGROUND), SIGNAL).sum() / N_MC**2  # P(score_S > score_B)


def z_asimov(s: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.sqrt(2 * ((s + b) * np.log1p(s / b) - s))


VALID = B_TOTAL * EPS_B >= 1.0  # at least one expected background event
Z_CUTS = CUTS[VALID]
Z_VALUES = z_asimov(S_TOTAL * EPS_S[VALID], B_TOTAL * EPS_B[VALID])
C_END = float(Z_CUTS[-1])
BEST = int(np.argmax(Z_VALUES))
C_BEST, Z_BEST = float(Z_CUTS[BEST]), float(Z_VALUES[BEST])

# --- layout -----------------------------------------------------------------------------
A = {"scores": (-2.8, -0.45), "roc": (3.95, -0.45), "z": (4.4, -0.45)}
FONT = 36


def score_axes() -> DataAxes:
    return DataAxes(
        (0, 1),
        (0, 0.12),
        x_length=5.6,
        y_length=3.7,
        x_ticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
        y_ticks=[0, 0.04, 0.08, 0.12],
        x_title="score",
        y_title="fraction / 0.04",
    ).move_frame_to(A["scores"])


def roc_axes() -> DataAxes:
    return DataAxes(
        (0, 1),
        (0, 1),
        x_length=3.7,
        y_length=3.7,
        x_ticks=[0, 0.5, 1],
        y_ticks=[0, 0.5, 1],
        x_title=MathTex(r"\varepsilon_B", font_size=FONT),
        y_title=MathTex(r"\varepsilon_S", font_size=FONT),
    ).move_frame_to(A["roc"])


def z_axes() -> DataAxes:
    return DataAxes(
        (0, 1),
        (0, 5),
        x_length=4.6,
        y_length=3.7,
        x_ticks=[0, 0.2, 0.4, 0.6, 0.8, 1],
        y_ticks=[0, 1, 2, 3, 4, 5],
        x_title=MathTex("c", font_size=FONT),
        y_title=MathTex("Z_A", font_size=FONT),
    ).move_frame_to(A["z"])


def efficiencies(c: float) -> tuple[float, float]:
    return float(np.interp(c, CUTS, EPS_S)), float(np.interp(c, CUTS, EPS_B))


def accepted(axes: DataAxes, fractions: np.ndarray, c: float, colour: str) -> VMobject:
    """The part of a histogram above the cut, shaded."""
    if c >= 1:
        return VMobject()
    xs = [c, *(e for e in EDGES if e > c)]
    points = [axes.c2p(c, 0)]
    for lo, hi in itertools.pairwise(xs):
        height = fractions[min(int(lo / (EDGES[1] - EDGES[0]) + 1e-9), len(fractions) - 1)]
        points += [axes.c2p(lo, height), axes.c2p(hi, height)]
    points.append(axes.c2p(xs[-1], 0))
    return Polygon(*points, stroke_width=0, fill_color=colour, fill_opacity=0.3)


def cut_parts(axes: DataAxes, c: float) -> dict:
    """Everything on the score panel that depends on the cut."""
    line = DashedLine(axes.c2p(c, 0), axes.c2p(c, 0.12), color=C.ink, stroke_width=3)
    label = MathTex("c", font_size=FONT).next_to(line, UP, buff=0.1)
    return {
        "shade_b": accepted(axes, FRAC_B, c, C.theory),
        "shade_s": accepted(axes, FRAC_S, c, C.highlight),
        "cut": line,
        "cut_label": label,
    }


def roc_parts(axes: DataAxes, c: float) -> dict:
    """The ROC curve from c = 0 up to the cut, and the operating point."""
    upto = c >= CUTS
    xs, ys = [*EPS_B[upto], efficiencies(c)[1]], [*EPS_S[upto], efficiencies(c)[0]]
    trace = axes.polyline(xs, ys, color=C.ink, stroke_width=3)
    dot = Dot(axes.c2p(xs[-1], ys[-1]), radius=0.08, color=C.ink)
    return {"roc": trace, "dot": dot}


def z_parts(axes: DataAxes, c: float) -> dict:
    """The significance curve up to the cut, and the point at the cut."""
    c = min(c, C_END)
    upto = c >= Z_CUTS
    z_now = float(np.interp(c, Z_CUTS, Z_VALUES))
    trace = axes.polyline([*Z_CUTS[upto], c], [*Z_VALUES[upto], z_now], color=C.ink)
    dot = Dot(axes.c2p(c, z_now), radius=0.08, color=C.highlight).set_z_index(1)
    return {"z_curve": trace, "z_dot": dot}


def state_roc() -> dict:
    """Last frame of RocSweep."""
    scores, roc = score_axes(), roc_axes()
    peak_b, peak_s = int(np.argmax(FRAC_B)), int(np.argmax(FRAC_S))
    state = {
        "scores": scores,
        "roc_axes": roc,
        "diagonal": DashedLine(roc.c2p(0, 0), roc.c2p(1, 1), color=C.muted, stroke_width=2),
        "hist_b": step_hist(scores, EDGES, FRAC_B, color=C.theory),
        "hist_s": step_hist(scores, EDGES, FRAC_S, color=C.highlight),
        "label_b": MathTex("B", font_size=FONT, color=C.theory).next_to(
            scores.c2p(EDGES[peak_b], FRAC_B[peak_b]), UP + np.array([-0.4, 0, 0]), buff=0.12
        ),
        "label_s": MathTex("S", font_size=FONT, color=C.highlight).next_to(
            scores.c2p(EDGES[peak_s + 1], FRAC_S[peak_s]), UP + np.array([0.4, 0, 0]), buff=0.12
        ),
    }
    parts = cut_parts(scores, 1.0)
    state["cut"], state["cut_label"] = parts["cut"], parts["cut_label"]
    state.update(roc_parts(roc, 1.0))
    auc = MathTex(rf"\mathrm{{AUC}} = {AUC:.2f}", font_size=FONT)
    state["auc"] = auc.move_to(roc.c2p(0.62, 0.14))
    return state


class RocSweep(Scene):
    def construct(self):
        state = state_roc()
        scores, roc = state["scores"], state["roc_axes"]
        self.play(FadeIn(scores), FadeIn(roc), Create(state["diagonal"]), run_time=1.2)
        self.play(Create(state["hist_b"]), Create(state["hist_s"]), run_time=1.2)
        self.play(FadeIn(state["label_b"]), FadeIn(state["label_s"]), run_time=0.5)

        cut = ValueTracker(0.0)
        moving = {
            key: always_redraw(lambda key=key: cut_parts(scores, cut.get_value())[key])
            for key in ("shade_b", "shade_s", "cut", "cut_label")
        }
        moving.update(
            {
                key: always_redraw(lambda key=key: roc_parts(roc, cut.get_value())[key])
                for key in ("roc", "dot")
            }
        )
        self.play(*(FadeIn(m) for m in moving.values()), run_time=0.6)
        self.play(cut.animate.set_value(1.0), run_time=6.5, rate_func=linear)

        # Swap the moving pieces for the identical static ones of the final state.
        self.remove(cut, *moving.values())
        self.add(*(state[k] for k in ("cut", "cut_label", "roc", "dot")))
        self.play(FadeIn(state["auc"]), run_time=0.8)
        check_order(self, state)
        self.wait(0.1)


def state_significance() -> dict:
    """Last frame of CutSignificance."""
    roc_state = state_roc()
    scores, zax = roc_state["scores"], z_axes()
    state = {k: roc_state[k] for k in ("scores", "hist_b", "hist_s", "label_b", "label_s")}
    formula = MathTex(r"Z_A = \sqrt{2\left[(s+b)\ln(1+s/b) - s\right]}", font_size=30)
    state["z_axes"] = zax
    state["formula"] = formula.next_to(zax.frame, UP, buff=0.3)
    state["z_curve"] = z_parts(zax, C_END)["z_curve"]
    state.update(cut_parts(scores, C_BEST))
    guide = DashedLine(zax.c2p(C_BEST, 0), zax.c2p(C_BEST, Z_BEST), color=C.muted, stroke_width=2)
    value = MathTex(rf"Z_A = {Z_BEST:.2f}", font_size=FONT)
    value.next_to(zax.c2p(C_BEST, Z_BEST), UP, buff=0.3)
    cut_value = MathTex(rf"c = {C_BEST:.2f}", font_size=FONT)
    cut_value.next_to(zax.c2p(C_BEST, 0), UP + np.array([-0.9, 0, 0]), buff=0.2)
    state.update({"guide": guide, "z_value": value, "cut_value": cut_value})
    state["z_dot"] = z_parts(zax, C_BEST)["z_dot"]  # z_index 1: drawn last
    return state


class CutSignificance(Scene):
    """Opens on RocSweep's last frame."""

    def construct(self):
        before = add_state(self, state_roc)
        state = state_significance()
        scores, zax = before["scores"], state["z_axes"]
        state["scores"] = scores  # the score panel stays on screen: reuse its objects
        for k in ("hist_b", "hist_s", "label_b", "label_s"):
            state[k] = before[k]

        cut = ValueTracker(1.0)
        on_scores = {
            key: always_redraw(lambda key=key: cut_parts(scores, cut.get_value())[key])
            for key in ("shade_b", "shade_s", "cut", "cut_label")
        }
        self.remove(before["cut"], before["cut_label"])
        self.add(*on_scores.values())
        leaving = [before[k] for k in ("roc_axes", "diagonal", "roc", "dot", "auc")]
        self.play(
            *(FadeOut(m) for m in leaving),
            FadeIn(zax),
            FadeIn(state["formula"]),
            cut.animate.set_value(0.0),
            run_time=1.5,
        )

        on_z = {
            key: always_redraw(lambda key=key: z_parts(zax, cut.get_value())[key])
            for key in ("z_curve", "z_dot")
        }
        self.add(*on_z.values())
        self.play(cut.animate.set_value(C_END), run_time=5.0, rate_func=linear)

        # The full curve stays; the cut and the point slide back to the best cut.
        self.remove(on_z["z_curve"])
        self.add(state["z_curve"])
        self.play(cut.animate.set_value(C_BEST), run_time=1.4, rate_func=smooth)

        self.remove(cut, *on_scores.values(), on_z["z_dot"])
        self.add(*(state[k] for k in ("shade_b", "shade_s", "cut", "cut_label", "z_dot")))
        self.play(
            Create(state["guide"]),
            FadeIn(state["z_value"], shift=DOWN * 0.1),
            FadeIn(state["cut_value"], shift=DOWN * 0.1),
            run_time=0.9,
        )
        check_order(self, state)
        self.wait(0.1)
