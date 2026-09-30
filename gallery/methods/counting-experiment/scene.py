"""Counting experiment: collisions are recorded one by one, a rare signal stands out
against a large background, and its significance grows like the square root of the
number of events.

Two chained clips:

- ``CountingTally``: events land in a tally grid; the counts N_B and N_S run up and
  Z = S/√B is computed from them.
- ``CountingSignificance``: opens on the tally's last frame and shows Z against the
  number of recorded events, growing like √N past 3σ and 5σ.

Physics honesty: every event comes from one seeded random sequence in which each
event is signal with probability ``P_SIGNAL`` (schematic). The colours show
simulation truth, which a real experiment never has event by event. Z = S/√B is the
usual approximation for S ≪ B.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    DR,
    LEFT,
    RIGHT,
    UL,
    UP,
    ChangeDecimalToValue,
    Create,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    Integer,
    LaggedStart,
    Line,
    MathTex,
    Scene,
    Square,
    TransformFromCopy,
    VGroup,
    linear,
)

from manim_hep import DataAxes, add_state, check_order, use_theme
from manim_hep.palette import tint

theme = use_theme()
C = theme.palette

# --- the synthetic event sequence ------------------------------------------------------
RNG = np.random.default_rng(20260930)
P_SIGNAL = 0.06  # chance that a recorded event is signal (schematic)
N_EVENTS = 8000
IS_SIGNAL = RNG.random(N_EVENTS) < P_SIGNAL  # truth, in recording order

COLS, ROWS = 20, 12
N_GRID = COLS * ROWS  # the events that land in the tally grid
S_GRID = int(IS_SIGNAL[:N_GRID].sum())
B_GRID = N_GRID - S_GRID
Z_GRID = S_GRID / np.sqrt(B_GRID)

N_CURVE = np.arange(N_GRID, N_EVENTS + 1, 20)
S_CUM = np.cumsum(IS_SIGNAL)[N_CURVE - 1]
Z_CURVE = S_CUM / np.sqrt(N_CURVE - S_CUM)


def z_expected(n: float) -> float:
    """Z = S/√B for the expected counts S = pN and B = (1 - p)N."""
    return P_SIGNAL * np.sqrt(n) / np.sqrt(1 - P_SIGNAL)


# --- layout -----------------------------------------------------------------------------
A = {
    "ip": (-5.7, -0.4),
    "grid": (-0.6, -0.4),
    "tally": (3.35, 0.9),  # upper-left corner of the counts column
    "axes": (0.2, -0.55),  # plot-area centre in the second clip
}
CELL, PITCH = 0.2, 0.26
N_ONE_BY_ONE = 8  # the first events are shown flying in one at a time
FONT = 40


def _grid_points() -> list[np.ndarray]:
    x0, y0 = A["grid"]
    xs = (np.arange(COLS) - (COLS - 1) / 2) * PITCH + x0
    ys = ((ROWS - 1) / 2 - np.arange(ROWS)) * PITCH + y0
    return [np.array([x, y, 0.0]) for y in ys for x in xs]  # row by row from the top left


def _event_colour(i: int) -> str:
    return C.highlight if IS_SIGNAL[i] else C.muted


def state_tally() -> dict:
    """Last frame of CountingTally: the full grid, both counts and Z."""
    points = _grid_points()
    ip_point = np.array([*A["ip"], 0.0])
    beam = Line(ip_point + LEFT * 1.2, ip_point + RIGHT * 1.2, color=C.muted, stroke_width=4)
    ip = Dot(ip_point, radius=0.1, color=C.ink)
    cells = VGroup(
        *(Square(CELL, color=tint(C.muted, 0.55), stroke_width=1.2).move_to(p) for p in points)
    )
    hits = VGroup(
        *(
            Square(CELL, stroke_width=0, fill_color=_event_colour(i), fill_opacity=1).move_to(p)
            for i, p in enumerate(points)
        )
    )

    def count(symbol: str, value: int, colour: str) -> VGroup:
        lab = MathTex(symbol, "=", font_size=FONT)
        lab[0].set_color(colour)
        num = Integer(value, font_size=FONT)
        num.next_to(lab, RIGHT, buff=0.2).align_to(lab[0][0], DOWN)
        return VGroup(lab, num)

    n_b = count("N_B", B_GRID, C.muted)
    n_s = count("N_S", S_GRID, C.highlight)
    z_lab = MathTex(r"Z = S/\sqrt{B}", "=", font_size=FONT)
    z_val = DecimalNumber(Z_GRID, num_decimal_places=2, font_size=FONT)
    z_val.next_to(z_lab, RIGHT, buff=0.2).align_to(z_lab[0][0], DOWN)
    z = VGroup(z_lab, z_val)
    tally = VGroup(n_b, n_s).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
    tally.move_to([*A["tally"], 0], aligned_edge=UL)
    z.next_to(tally, DOWN, buff=0.75, aligned_edge=LEFT)
    return {"beam": beam, "ip": ip, "cells": cells, "hits": hits, "tally": tally, "z": z}


def state_growth() -> dict:
    """Last frame of CountingSignificance: Z against the number of events."""
    axes = DataAxes(
        (0, N_EVENTS),
        (0, 6),
        x_length=8.4,
        y_length=4.3,
        x_ticks=[0, 2000, 4000, 6000, 8000],
        y_ticks=[0, 1, 2, 3, 4, 5, 6],
        x_title=MathTex("N", font_size=36),
        y_title=MathTex("Z", font_size=36),
    ).move_frame_to(A["axes"])
    formula = MathTex(r"Z = S/\sqrt{B}", font_size=FONT)
    formula.move_to(axes.frame.get_corner(DR) + np.array([-0.3, 0.3, 0]), aligned_edge=DR)
    # In one play(), TransformFromCopy adds its mobject before FadeIn does, so the
    # formula is drawn first (the two never overlap).
    state = {"formula": formula, "axes": axes}
    for level in (3, 5):
        line = DashedLine(axes.c2p(0, level), axes.c2p(N_EVENTS, level), color=C.muted)
        state[f"ref{level}"] = line
        state[f"lab{level}"] = MathTex(rf"{level}\sigma", font_size=34, color=C.muted).next_to(
            line, RIGHT, buff=0.15
        )
    state["observed"] = axes.polyline(N_CURVE, Z_CURVE, color=C.ink, stroke_width=3)
    expected = axes.plot(z_expected, x_range=(1, N_EVENTS), color=C.theory, stroke_width=3)
    state["expected"] = DashedVMobject(expected, num_dashes=70)
    dot = Dot(axes.c2p(N_GRID, Z_GRID), radius=0.08, color=C.highlight)
    dot.set_z_index(1)  # stays on top of the curves drawn after it
    state["dot"] = dot
    return state


class CountingTally(Scene):
    def construct(self):
        state = state_tally()
        n_b, n_s = state["tally"][0][1], state["tally"][1][1]
        n_b.set_value(0)
        n_s.set_value(0)
        for hit in state["hits"]:
            hit.set_fill(opacity=0)

        self.play(
            Create(state["beam"]),
            FadeIn(state["ip"], scale=0.5),
            Create(state["cells"], lag_ratio=0.002),
            FadeIn(state["hits"]),
            FadeIn(state["tally"]),
            run_time=1.4,
        )

        # The first events, one at a time: collision -> event -> one entry in the grid.
        counts = [0, 0]
        for i in range(N_ONE_BY_ONE):
            slow = i < 3
            hit = state["hits"][i]
            spark = Dot(state["ip"].get_center(), radius=0.09, color=_event_colour(i))
            self.play(FadeIn(spark, scale=2.5), run_time=0.15 if slow else 0.08)
            self.play(spark.animate.move_to(hit), run_time=0.3 if slow else 0.18, rate_func=linear)
            counts[int(IS_SIGNAL[i])] += 1
            counter = n_s if IS_SIGNAL[i] else n_b
            self.play(
                hit.animate.set_fill(opacity=1),
                FadeOut(spark),
                ChangeDecimalToValue(counter, counts[int(IS_SIGNAL[i])]),
                run_time=0.15 if slow else 0.09,
            )

        # Then the rest of the grid fills at a steady rate; the counts follow the grid.
        def count_shown(signal: bool) -> int:
            return sum(
                1
                for i, hit in enumerate(state["hits"])
                if IS_SIGNAL[i] == signal and hit.get_fill_opacity() > 0.5
            )

        n_b.add_updater(lambda m: m.set_value(count_shown(False)))
        n_s.add_updater(lambda m: m.set_value(count_shown(True)))
        rest = [h.animate.set_fill(opacity=1) for h in state["hits"][N_ONE_BY_ONE:]]
        self.play(LaggedStart(*rest, lag_ratio=0.03, group=state["hits"]), run_time=4.6)
        n_b.clear_updaters()
        n_s.clear_updaters()
        self.play(FadeIn(state["z"], shift=UP * 0.2), run_time=0.8)
        check_order(self, state)
        self.wait(0.1)


class CountingSignificance(Scene):
    """Opens on CountingTally's last frame."""

    def construct(self):
        tally = add_state(self, state_tally)
        state = state_growth()
        leaving = [tally[k] for k in ("beam", "ip", "cells", "hits", "tally", "z")]
        self.play(
            FadeIn(state["axes"]),
            TransformFromCopy(tally["z"][0][0], state["formula"]),
            *(FadeOut(m) for m in leaving),
            run_time=1.3,
        )
        self.play(
            Create(state["ref3"]),
            FadeIn(state["lab3"]),
            Create(state["ref5"]),
            FadeIn(state["lab5"]),
            run_time=0.9,
        )
        self.play(FadeIn(state["dot"], scale=2), run_time=0.6)
        self.play(Create(state["observed"]), run_time=4.0, rate_func=linear)
        self.play(Create(state["expected"]), run_time=1.3)
        check_order(self, state)
        self.wait(0.1)
