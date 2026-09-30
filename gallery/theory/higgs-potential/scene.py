"""The Higgs potential: its minimum sets v, its curvature there sets m_H.

Physics honesty: the curve is the tree-level Standard Model potential along one
real direction of the field, V(φ) = −½μ²φ² + ¼λφ⁴ with μ² = λv², drawn exactly for
λ = m_H²/(2v²) ≈ 0.129 from the PDG values of v and m_H. The vertical axis has no
scale (V is in units of λv⁴). The ball rolling into the minimum pictures
spontaneous symmetry breaking; it is not a time evolution. The dashed parabola has
the potential's curvature at the minimum, V''(v) = 2λv² = m_H².
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    UP,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    MathTex,
    MoveAlongPath,
    Scene,
    rate_functions,
)

from manim_hep import DataAxes, add_state, check_order, use_theme

theme = use_theme()
C = theme.palette

V_EW = 246.22  # GeV, v = (√2 G_F)^(-1/2); PDG 2024
M_H = 125.20  # GeV; PDG 2024
LAMBDA = M_H**2 / (2 * V_EW**2)  # ≈ 0.129

X_RANGE = (-1.65 * V_EW, 1.65 * V_EW)
Y_RANGE = (-0.62, 0.55)  # V / (λ v⁴)
BALL_R = 0.13

# Anchors (scene units): the plot area's centre, and where the formulas go.
A = {"plot": (0.35, -0.5), "mass_formula": (0.35, 1.3), "lambda_formula": (0.35, 0.55)}


def potential(phi: float) -> float:
    """V(φ) / (λv⁴) = −½ (φ/v)² + ¼ (φ/v)⁴."""
    x = phi / V_EW
    return -0.5 * x**2 + 0.25 * x**4


def osculating(phi: float) -> float:
    """The parabola with V's value and curvature at φ = v (V''(v) = 2λv², i.e. 2 here)."""
    x = phi / V_EW
    return potential(V_EW) + (x - 1.0) ** 2


def build_axes() -> DataAxes:
    axes = DataAxes(
        X_RANGE,
        Y_RANGE,
        x_length=8.6,
        y_length=4.6,
        x_ticks=[-400, -200, 0, 200, 400],
        y_ticks=[],
        x_title="φ [GeV]",
        y_title="V(φ)",
    )
    return axes.move_frame_to(A["plot"])


def state_vacuum() -> dict:
    """Clip 1's last frame. The ball draws on top of everything (z-index 1)."""
    axes = build_axes()
    curve = axes.plot(potential, samples=300, color=C.theory, stroke_width=4)
    minimum = axes.c2p(V_EW, potential(V_EW))
    vline = DashedLine(axes.c2p(V_EW, Y_RANGE[0]), minimum, color=C.muted, stroke_width=2.5)
    vlabel = MathTex(r"v = 246.22~\mathrm{GeV}", font_size=34)
    vlabel.next_to(axes.c2p(V_EW, -0.47), LEFT, buff=0.18)
    ball = Dot(minimum + UP * BALL_R, radius=BALL_R, color=C.highlight).set_z_index(1)
    return {"axes": axes, "curve": curve, "vline": vline, "vlabel": vlabel, "ball": ball}


def state_mass() -> dict:
    """Clip 2's last frame: clip 1 plus the curvature at the minimum and m_H."""
    state = state_vacuum()
    axes, ball = state["axes"], state.pop("ball")
    parabola = axes.plot(osculating, x_range=(0.45 * V_EW, 1.55 * V_EW), color=C.highlight)
    state["parabola"] = DashedVMobject(parabola, num_dashes=32)
    state["mass"] = MathTex(r"m_H^2 = V''(v) = 2\lambda v^2", font_size=40).move_to(
        [*A["mass_formula"], 0]
    )
    state["lambda"] = MathTex(
        r"m_H = 125.20~\mathrm{GeV}", r"\;\Rightarrow\;", r"\lambda \approx 0.129", font_size=40
    ).move_to([*A["lambda_formula"], 0])
    state["ball"] = ball  # last: it has z-index 1
    return state


class HiggsPotential(Scene):
    """The double well appears; a ball leaves the symmetric point and settles at φ = v."""

    def construct(self):
        state = state_vacuum()
        axes, ball = state["axes"], state["ball"]
        top = axes.c2p(0.0, potential(0.0)) + UP * BALL_R
        path = axes.plot(potential, x_range=(0.0, V_EW), samples=120).shift(UP * BALL_R)
        ball.move_to(top)

        self.play(FadeIn(axes), run_time=0.8)
        self.play(Create(state["curve"]), run_time=2.0)
        self.play(FadeIn(ball, scale=0.5), run_time=0.5)
        self.wait(0.4)
        self.play(
            MoveAlongPath(ball, path), run_time=1.8, rate_func=rate_functions.ease_in_out_sine
        )
        self.play(Create(state["vline"]), run_time=0.6)
        self.play(FadeIn(state["vlabel"], shift=0.2 * DOWN), run_time=0.8)
        check_order(self, state)
        self.wait(0.1)


class HiggsMass(Scene):
    """Opens on HiggsPotential's last frame: the curvature at the minimum is m_H²."""

    def construct(self):
        state = state_mass()
        add_state(self, {k: state[k] for k in ("axes", "curve", "vline", "vlabel", "ball")})
        self.play(Create(state["parabola"]), run_time=1.5)
        self.play(FadeIn(state["mass"], shift=0.2 * UP), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(state["lambda"], shift=0.2 * UP), run_time=1.0)
        check_order(self, state)
        self.wait(0.1)
