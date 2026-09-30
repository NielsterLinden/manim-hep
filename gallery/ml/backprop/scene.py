"""Backpropagation in a 2-3-1 network: forward pass and loss, then gradients flow back.

ML honesty: the weights are seeded random numbers (no biases). Every number on
screen is computed: sigmoid activations, ŷ = σ(w₂·h), L = ½(ŷ − y)², the
gradients by the chain rule, and one gradient-descent step with η = 2. Line
thickness grows with |w| (1 + 3|w|); hidden and output shading with the activation.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    UP,
    Circle,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Restore,
    Scene,
    ShowPassingFlash,
    Text,
    VGroup,
)

from manim_hep import add_state, check_order, use_theme
from manim_hep.palette import mix

theme = use_theme()
C = theme.palette

RNG = np.random.default_rng(120)
X_IN = np.array([0.8, -0.4])
Y_TRUE = 1.0
ETA = 2.0
W1 = RNG.normal(0.0, 1.0, size=(3, 2))  # input -> hidden
W2 = RNG.normal(0.0, 1.0, size=3)  # hidden -> output


def sigmoid(t):
    return 1.0 / (1.0 + np.exp(-t))


def forward(w1: np.ndarray, w2: np.ndarray) -> tuple[np.ndarray, float, float]:
    hidden = sigmoid(w1 @ X_IN)
    y_hat = float(sigmoid(w2 @ hidden))
    return hidden, y_hat, 0.5 * (y_hat - Y_TRUE) ** 2


H, Y_HAT, LOSS = forward(W1, W2)
_DELTA_OUT = (Y_HAT - Y_TRUE) * Y_HAT * (1 - Y_HAT)
GRAD_W2 = _DELTA_OUT * H
GRAD_W1 = np.outer(_DELTA_OUT * W2 * H * (1 - H), X_IN)
W1_NEW, W2_NEW = W1 - ETA * GRAD_W1, W2 - ETA * GRAD_W2
H_NEW, Y_HAT_NEW, LOSS_NEW = forward(W1_NEW, W2_NEW)

R = 0.42
A = {  # anchors (scene units)
    "layers_x": (-4.4, -1.3, 1.8),
    "mid_y": -0.7,
    "spacing": 1.55,
    "target": (4.55, 0.35),
    "loss": (4.55, -0.7),
    "gradient": (0.25, 1.75),
    "update": (-1.3, -3.35),
}


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace("-", "−")


def node_centre(layer: int, k: int) -> np.ndarray:
    n = (2, 3, 1)[layer]
    y = A["mid_y"] + (n - 1) / 2 * A["spacing"] - k * A["spacing"]
    return np.array([A["layers_x"][layer], y, 0.0])


EDGE_ENDS = [((0, i), (1, h)) for h in range(3) for i in range(2)] + [
    ((1, h), (2, 0)) for h in range(3)
]


def weight(index: int, w1: np.ndarray, w2: np.ndarray) -> float:
    if index < 6:
        return float(w1[index // 2, index % 2])
    return float(w2[index - 6])


def edge_width(w: float) -> float:
    return 1.0 + 3.0 * abs(w)


def edge_line(index: int, width: float) -> Line:
    (l0, k0), (l1, k1) = EDGE_ENDS[index]
    a, b = node_centre(l0, k0), node_centre(l1, k1)
    u = (b - a) / np.linalg.norm(b - a)
    return Line(a + u * R, b - u * R, color=C.muted, stroke_width=width)


def shade(activation: float) -> str:
    return mix(C.background, C.theory, 0.75 * activation)


def values_in(layer: int, numbers) -> VGroup:
    return VGroup(
        *(
            Text(fmt(v, 1 if layer == 0 else 2), font_size=22).move_to(node_centre(layer, k))
            for k, v in enumerate(numbers)
        )
    )


def loss_formula(loss: float) -> MathTex:
    return MathTex(rf"L = \tfrac{{1}}{{2}}(\hat{{y}} - y)^2 = {loss:.3f}", font_size=36).move_to(
        [*A["loss"], 0]
    )


def state_forward() -> dict:
    """BackpropForward's last frame. Dict order = drawing order."""
    edges = VGroup(*(edge_line(i, edge_width(weight(i, W1, W2))) for i in range(9)))
    fills = [0.4, 0.4, *H, Y_HAT]  # inputs get a fixed light shade
    positions = [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 0)]
    nodes = VGroup(
        *(
            Circle(
                radius=R, color=C.ink, stroke_width=3, fill_color=shade(a), fill_opacity=1.0
            ).move_to(node_centre(*p))
            for p, a in zip(positions, fills, strict=True)
        )
    )
    labels = VGroup(
        MathTex("x_1", font_size=40).next_to(node_centre(0, 0), LEFT, buff=R + 0.2),
        MathTex("x_2", font_size=40).next_to(node_centre(0, 1), LEFT, buff=R + 0.2),
        MathTex(r"\hat{y}", font_size=40).next_to(node_centre(2, 0), UP, buff=R + 0.15),
    )
    return {
        "edges": edges,
        "nodes": nodes,
        "labels": labels,
        "inputs": values_in(0, X_IN),
        "hidden": values_in(1, H),
        "output": values_in(2, [Y_HAT]),
        "target": MathTex(r"y = 1", font_size=36).move_to([*A["target"], 0]),
        "loss": loss_formula(LOSS),
    }


def flashes(indices, color, reverse: bool = False) -> list[ShowPassingFlash]:
    out = []
    for i in indices:
        line = edge_line(i, 7).set_color(color)
        if reverse:
            line = Line(line.get_end(), line.get_start(), color=color, stroke_width=7)
        out.append(ShowPassingFlash(line, time_width=0.5))
    return out


class BackpropForward(Scene):
    """Inputs flow forward to a prediction ŷ, which is compared with the target y."""

    def construct(self):
        state = state_forward()
        nodes = state["nodes"]
        for node in nodes:
            node.save_state()
            node.set_fill(C.background, 1.0)

        self.play(FadeIn(state["edges"]), FadeIn(nodes), FadeIn(state["labels"]), run_time=1.0)
        self.play(Restore(nodes[0]), Restore(nodes[1]), FadeIn(state["inputs"]), run_time=0.6)
        self.play(*flashes(range(6), C.theory), run_time=1.0)
        self.play(*(Restore(nodes[k]) for k in (2, 3, 4)), FadeIn(state["hidden"]), run_time=0.6)
        self.play(*flashes(range(6, 9), C.theory), run_time=0.9)
        self.play(Restore(nodes[5]), FadeIn(state["output"]), run_time=0.6)
        self.play(FadeIn(state["target"], shift=0.2 * LEFT), run_time=0.5)
        self.play(FadeIn(state["loss"], shift=0.2 * LEFT), run_time=0.8)
        check_order(self, state)
        self.wait(0.1)


class BackpropBackward(Scene):
    """Opens on BackpropForward's last frame: gradients flow back and the weights move."""

    def construct(self):
        entry = state_forward()
        add_state(self, entry)
        gradient = MathTex(r"\frac{\partial L}{\partial w}", font_size=40, color=C.highlight)
        gradient.move_to([*A["gradient"], 0])
        update = MathTex(r"w \leftarrow w - \eta\, \frac{\partial L}{\partial w}", font_size=38)
        update.move_to([*A["update"], 0])

        self.play(
            FadeIn(gradient, shift=0.2 * DOWN),
            *flashes(range(6, 9), C.highlight, reverse=True),
            run_time=1.0,
        )
        self.play(*flashes(range(6), C.highlight, reverse=True), run_time=1.0)
        self.play(
            *(
                edge.animate.set_stroke(width=edge_width(weight(i, W1_NEW, W2_NEW)))
                for i, edge in enumerate(entry["edges"])
            ),
            FadeIn(update, shift=0.2 * UP),
            run_time=1.2,
        )

        # One more forward pass with the new weights: the loss went down.
        hidden, output, loss = (
            values_in(1, H_NEW),
            values_in(2, [Y_HAT_NEW]),
            loss_formula(LOSS_NEW),
        )
        self.play(*flashes(range(6), C.theory), run_time=0.5)
        self.play(*flashes(range(6, 9), C.theory), run_time=0.5)
        self.play(
            *(
                entry["nodes"][k].animate.set_fill(shade(a))
                for k, a in zip((2, 3, 4), H_NEW, strict=True)
            ),
            entry["nodes"][5].animate.set_fill(shade(Y_HAT_NEW)),
            FadeOut(entry["hidden"]),
            FadeOut(entry["output"]),
            FadeOut(entry["loss"]),
            FadeIn(hidden),
            FadeIn(output),
            FadeIn(loss),
            run_time=0.9,
        )

        final = [entry[k] for k in ("edges", "nodes", "labels", "inputs", "target")]
        check_order(self, [*final, gradient, update, hidden, output, loss])
        self.wait(0.1)
