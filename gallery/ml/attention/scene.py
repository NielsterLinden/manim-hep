"""Self-attention for one head: scores, softmax rows, and a weighted sum of values.

ML honesty: four tokens with seeded random query, key and value vectors (d = 3),
so every number on screen is computed, not typed: s_ij = q_i·k_j/√d, a_ij is the
softmax of row i, and z_i = Σ_j a_ij v_j. Only the update of token 2 is shown.
Cell shading increases with the value in the cell; bar heights are proportional to
the vector components.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
)

from manim_hep import add_state, check_order, use_theme

theme = use_theme()
C = theme.palette

RNG = np.random.default_rng(98)
D = 3
Q = RNG.normal(size=(4, D))
K = RNG.normal(size=(4, D))
VALUES = RNG.normal(size=(4, D))
SCORES = Q @ K.T / np.sqrt(D)
_EXP = np.exp(SCORES - SCORES.max(axis=1, keepdims=True))
WEIGHTS = _EXP / _EXP.sum(axis=1, keepdims=True)
ROW = 1  # token 2 (rows count from 0 here, from 1 on screen)
Z = WEIGHTS[ROW] @ VALUES

CELL = 1.0
BAR_W, BAR_GAP, BAR_SCALE = 0.2, 0.26, 0.55
# Anchors (scene units).
A = {
    "grid": (-1.3, -0.9),  # centre of the 4×4 grid
    "score_formula": (3.9, 0.55),
    "weight_formula": (3.9, -1.35),
    "values": (2.0, 0.95),  # baseline centre of v_1; the others follow to the right
    "value_step": 1.25,
    "result": (3.9, -1.75),  # baseline centre of z_2
}


def fmt(value: float, digits: int) -> str:
    return f"{value:.{digits}f}".replace("-", "−")


def cell_centre(i: int, j: int) -> np.ndarray:
    gx, gy = A["grid"]
    return np.array([gx + (j - 1.5) * CELL, gy - (i - 1.5) * CELL, 0.0])


def score_opacity(s: float) -> float:
    return 0.06 + 0.5 * (s - SCORES.min()) / (SCORES.max() - SCORES.min())


def weight_opacity(a: float) -> float:
    return 0.06 + 0.9 * a


def cell_rows(values: np.ndarray, opacity) -> list[VGroup]:
    return [
        VGroup(
            *(
                Square(
                    CELL,
                    stroke_color=C.muted,
                    stroke_width=1.5,
                    fill_color=C.theory,
                    fill_opacity=opacity(values[i, j]),
                ).move_to(cell_centre(i, j))
                for j in range(4)
            )
        )
        for i in range(4)
    ]


def number_rows(values: np.ndarray, digits: int) -> list[VGroup]:
    return [
        VGroup(
            *(
                Text(fmt(values[i, j], digits), font_size=22).move_to(cell_centre(i, j))
                for j in range(4)
            )
        )
        for i in range(4)
    ]


def state_weights() -> dict:
    """AttentionScores' last frame. Dict order = drawing order."""
    queries = VGroup(
        *(
            MathTex(f"q_{i + 1}", font_size=40, color=C.cycle[i]).move_to(
                cell_centre(i, 0) + LEFT * (CELL / 2 + 0.45)
            )
            for i in range(4)
        )
    )
    keys = VGroup(
        *(
            MathTex(f"k_{j + 1}", font_size=40, color=C.cycle[j]).move_to(
                cell_centre(0, j) + UP * (CELL / 2 + 0.4)
            )
            for j in range(4)
        )
    )
    state: dict = {"queries": queries, "keys": keys}
    for i, row in enumerate(cell_rows(WEIGHTS, weight_opacity)):
        state[f"cells{i}"] = row
    state["score_formula"] = MathTex(
        r"s_{ij} = \frac{q_i \cdot k_j}{\sqrt{d}}", font_size=40
    ).move_to([*A["score_formula"], 0])
    for i, row in enumerate(number_rows(WEIGHTS, 2)):
        state[f"weights{i}"] = row
    state["weight_formula"] = MathTex(
        r"a_{ij} = \frac{e^{s_{ij}}}{\sum_{j'} e^{s_{ij'}}}", font_size=40
    ).move_to([*A["weight_formula"], 0])
    return state


def value_vector(j: int) -> VGroup:
    """v_j as three bars on a baseline, with its label: VGroup(baseline, bars, label)."""
    x0, y0 = A["values"]
    x = x0 + j * A["value_step"]
    bars = VGroup()
    for c in range(D):
        h = VALUES[j, c] * BAR_SCALE
        bar = Rectangle(
            width=BAR_W,
            height=max(abs(h), 0.02),
            stroke_width=0,
            fill_color=C.cycle[j],
            fill_opacity=1.0,
        )
        bars.add(bar.move_to([x + (c - 1) * BAR_GAP, y0 + h / 2, 0]))
    base = Line([x - 0.45, y0, 0], [x + 0.45, y0, 0], color=C.muted, stroke_width=2)
    label = MathTex(f"v_{j + 1}", font_size=38, color=C.cycle[j]).move_to([x, y0 - 0.95, 0])
    return VGroup(base, bars, label)


def weight_tag(j: int) -> Text:
    x0, y0 = A["values"]
    return Text(fmt(WEIGHTS[ROW, j], 2), font_size=22).move_to(
        [x0 + j * A["value_step"], y0 - 1.45, 0]
    )


def scaled_bars(vector: VGroup, j: int, target_base: np.ndarray | None = None) -> VGroup:
    """Copies of v_j's bars scaled by a_2j about the baseline, optionally moved."""
    base_centre = vector[0].get_center()
    bars = vector[1].copy()
    for bar in bars:
        bar.stretch(WEIGHTS[ROW, j], dim=1, about_point=[bar.get_x(), base_centre[1], 0])
    if target_base is not None:
        bars.shift(target_base - base_centre)
    return bars


def result_parts() -> tuple[Line, VGroup, MathTex]:
    x, y0 = A["result"]
    bars = VGroup()
    for c in range(D):
        h = Z[c] * BAR_SCALE
        bar = Rectangle(
            width=BAR_W,
            height=max(abs(h), 0.02),
            stroke_width=0,
            fill_color=C.highlight,
            fill_opacity=1.0,
        )
        bars.add(bar.move_to([x + (c - 1) * BAR_GAP, y0 + h / 2, 0]))
    base = Line([x - 0.45, y0, 0], [x + 0.45, y0, 0], color=C.muted, stroke_width=2)
    formula = MathTex(r"z_2 = \sum_j a_{2j}\, v_j", font_size=40)
    formula.next_to(base, DOWN, buff=0.75)
    return base, bars, formula


class AttentionScores(Scene):
    """Every query meets every key; each row of scores becomes softmax weights."""

    def construct(self):
        state = state_weights()
        score_cells = cell_rows(SCORES, score_opacity)
        score_numbers = number_rows(SCORES, 1)
        self.play(FadeIn(state["queries"]), FadeIn(state["keys"]), run_time=0.8)
        for i in range(4):
            self.play(FadeIn(score_cells[i]), FadeIn(score_numbers[i]), run_time=0.45)
        self.play(FadeIn(state["score_formula"]), run_time=0.6)
        for i in range(4):
            self.play(
                ReplacementTransform(score_cells[i], state[f"cells{i}"]),
                FadeOut(score_numbers[i]),
                FadeIn(state[f"weights{i}"]),
                run_time=0.6,
            )
        self.play(FadeIn(state["weight_formula"]), run_time=0.6)
        check_order(self, state)
        self.wait(0.1)


class AttentionUpdate(Scene):
    """Opens on AttentionScores' last frame: token 2 becomes the weighted sum of the values."""

    def construct(self):
        entry = state_weights()
        add_state(self, entry)
        others = [i for i in range(4) if i != ROW]
        box = SurroundingRectangle(
            entry[f"cells{ROW}"], color=C.highlight, buff=0.05, stroke_width=4
        )
        self.play(
            FadeOut(entry["score_formula"]),
            FadeOut(entry["weight_formula"]),
            *(entry[f"cells{i}"].animate.fade(0.75) for i in others),
            *(entry[f"weights{i}"].animate.fade(0.75) for i in others),
            *(entry["queries"][i].animate.fade(0.75) for i in others),
            Create(box),
            run_time=1.0,
        )

        vectors = [value_vector(j) for j in range(4)]
        self.play(*(FadeIn(v, shift=0.2 * UP) for v in vectors), run_time=0.8)

        tags = [weight_tag(j) for j in range(4)]
        base, bars, formula = result_parts()
        self.play(
            *(TransformFromCopy(entry[f"weights{ROW}"][j], tags[j]) for j in range(4)),
            FadeIn(base),
            run_time=1.0,
        )

        movers = VGroup(*(v[1].copy() for v in vectors))
        self.add(movers)
        self.play(
            Transform(movers, VGroup(*(scaled_bars(v, j) for j, v in enumerate(vectors)))),
            *(v[1].animate.fade(0.7) for v in vectors),
            run_time=1.0,
        )
        target = base.get_center()
        self.play(
            Transform(movers, VGroup(*(scaled_bars(v, j, target) for j, v in enumerate(vectors)))),
            run_time=0.9,
        )
        self.play(ReplacementTransform(movers, bars), run_time=0.8)
        self.play(FadeIn(formula, shift=0.2 * UP), run_time=0.7)

        final = [entry["queries"], entry["keys"]]
        final += [entry[f"cells{i}"] for i in range(4)] + [entry[f"weights{i}"] for i in range(4)]
        final += [box, *vectors, *tags, base, bars, formula]
        check_order(self, final)
        self.wait(0.1)
