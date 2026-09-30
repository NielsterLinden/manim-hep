"""Drell–Yan production: q q̄ → γ*/Z → ℓ⁻ℓ⁺, drawn in the order you read it.

Physics honesty: the leading-order (tree-level) s-channel diagram. Time runs left
to right. Fermion-flow arrows follow the usual convention: the incoming antiquark
and the outgoing antilepton carry arrows against the direction of time. Vertex
positions are schematic; no numbers appear on screen.
"""

from __future__ import annotations

from manim import Scene

from manim_hep import FeynmanDiagram, check_order, use_theme

theme = use_theme()
C = theme.palette

# Vertex positions in scene units: the diagram is centred in the content area,
# below the title band (y > 2.7 stays empty).
V = {
    "q": (-4.3, 1.3),
    "qbar": (-4.3, -2.5),
    "a": (-1.7, -0.6),
    "b": (1.7, -0.6),
    "l-": (4.3, 1.3),
    "l+": (4.3, -2.5),
}

# Build order = drawing order: the quarks come in, annihilate, the leptons fly out.
EDGES = [
    ("q", "a", "fermion", "q"),
    ("qbar", "a", "antifermion", r"\bar{q}"),
    ("a", "b", "photon", r"\gamma^*/Z"),
    ("b", "l-", "fermion", r"\ell^-"),
    ("b", "l+", "antifermion", r"\ell^+"),
]


def state_diagram() -> dict:
    """The final frame: the full diagram, with the exchanged boson in the theory colour."""
    diagram = FeynmanDiagram(V, EDGES, label_size=48, label_buff=0.22)
    diagram.edge("a", "b").set_color(C.theory)
    diagram.edge_labels[2].set_color(C.theory)
    return {"diagram": diagram}


class DrellYan(Scene):
    """The diagram builds edge by edge in reading order, each label with its edge."""

    def construct(self):
        state = state_diagram()
        self.play(state["diagram"].draw_in_order(time_per_edge=1.0))
        check_order(self, state)
        self.wait(0.1)
