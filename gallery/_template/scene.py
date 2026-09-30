"""<Title of the example>: one sentence on what the clip shows.

Physics honesty: say here what is schematic or exaggerated, and where every
number comes from (a reference, or "seeded synthetic data").
"""

from __future__ import annotations

import numpy as np
from manim import Circle, Create, Dot, FadeIn, Scene

from manim_hep import add_state, check_order, place, use_theme

theme = use_theme()  # experiment from manim-hep.toml; pass a name to fix it
C = theme.palette  # colour roles: C.ink, C.data, C.theory, C.highlight, C.cycle, ...

# Every position lives here, so chained clips place things identically.
A = {"ring": (1.0, (0.0, -0.6))}

RNG = np.random.default_rng(20260930)  # seeded: every render is identical


def state_ring() -> dict:
    """Clip 1's last frame, built without animation. Dict order = drawing order."""
    ring = Circle(radius=1.5, color=C.theory)
    place(ring, A["ring"])
    return {"ring": ring}


def state_ring_with_dot() -> dict:
    """Clip 2's last frame: clip 1's state plus one new object on top."""
    state = state_ring()
    angle = RNG.uniform(0, 2 * np.pi)
    state["dot"] = Dot(state["ring"].point_at_angle(angle), color=C.highlight)
    return state


class TemplateRing(Scene):
    def construct(self):
        state = state_ring()
        self.play(Create(state["ring"]), run_time=1.5)
        check_order(self, state)
        self.wait(0.1)  # end on the last change: the final frame is complete


class TemplateDot(Scene):
    """Opens exactly on TemplateRing's last frame, so the two clips chain seamlessly."""

    def construct(self):
        state = state_ring_with_dot()
        add_state(self, {"ring": state["ring"]})
        self.play(FadeIn(state["dot"], scale=0.5), run_time=0.6)
        check_order(self, state)
        self.wait(0.1)
