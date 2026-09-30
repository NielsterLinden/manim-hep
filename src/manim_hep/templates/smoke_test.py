"""manim-hep smoke test: theme, font, formula and plot in one frame.

Render it with `manim-hep render <root>/scenes/smoke_test.py SmokeTest` and look at the
last frame. It should show a white background, a line of text in the theme font, a
typeset formula (this needs LaTeX; without it a note says the formula was skipped) and a
small histogram. Nothing may be drawn above the title band.
"""

from __future__ import annotations

import shutil

import numpy as np
from manim import DOWN, LEFT, RIGHT, Create, FadeIn, MathTex, Scene, Text

from manim_hep import DataAxes, check_order, step_hist, use_theme

theme = use_theme()
C = theme.palette


def state() -> dict:
    heading = Text("manim-hep smoke test", font_size=34).move_to([0, 1.9, 0])
    if shutil.which("latex"):
        formula = MathTex(r"\Delta p_\mathrm{T} / p_\mathrm{T} = 1\%", font_size=44)
    else:
        formula = Text("(no LaTeX found: formula skipped)", font_size=24, color=C.muted)
    formula.move_to([-3.2, -0.6, 0])
    axes = DataAxes((0, 10), (0, 40), x_length=4.2, y_length=2.6, x_title="x", y_title="N")
    axes.move_frame_to((3.2, -0.8))
    edges = np.linspace(0, 10, 11)
    counts = np.array([3, 8, 15, 27, 34, 30, 21, 12, 6, 2])
    hist = step_hist(axes, edges, counts, color=C.theory)
    return {"heading": heading, "formula": formula, "axes": axes, "hist": hist}


class SmokeTest(Scene):
    def construct(self):
        s = state()
        self.play(FadeIn(s["heading"], shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(s["formula"], shift=RIGHT * 0.2), FadeIn(s["axes"], shift=LEFT * 0.2))
        self.play(Create(s["hist"]), run_time=1.2)
        check_order(self, s)
        self.wait(0.1)
