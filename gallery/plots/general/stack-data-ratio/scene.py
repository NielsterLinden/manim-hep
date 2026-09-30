"""Stacked prediction, data and a ratio panel: the data never move.

The simulated Z peak starts 0.8 GeV too high (a muon momentum-scale bias), so
the ratio data / prediction shows an S shape. The scale correction slides the
prediction onto the data and the ratio flattens; only the prediction and the
ratio move.

Physics honesty: seeded synthetic numbers. The Z shape is a Breit–Wigner with
m_Z = 91.1876 GeV and Γ_Z = 2.4952 GeV (PDG) smeared by a 1.6 GeV resolution;
the tt̄ background is a falling exponential; the 0.8 GeV bias is invented.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DL,
    DOWN,
    DR,
    LEFT,
    RIGHT,
    UL,
    UR,
    Dot,
    FadeIn,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    Scene,
    Transform,
    VGroup,
)

from manim_hep import DataAxes, check_order, errorbars, ratio_panel, stack_hist, use_theme

theme = use_theme()
C = theme.palette

M_Z, GAMMA_Z, RESOLUTION = 91.1876, 2.4952, 1.6  # GeV
BIAS = 0.8  # GeV: the invented momentum-scale bias of the first prediction
N_Z, N_TT = 40_000, 5_000
EDGES = np.arange(70.0, 110.0 + 1e-9, 2.0)
CENTRES = (EDGES[:-1] + EDGES[1:]) / 2
COLOURS = {"tt": C.cycle[0], "z": C.cycle[3]}

A = {"frame": (0.35, 0.72)}


def _z_shape(shift: float) -> np.ndarray:
    rng = np.random.default_rng(3)
    u = rng.random(2_000_000)
    m = M_Z + shift + GAMMA_Z / 2 * np.tan(np.pi * (u - 0.5)) + rng.normal(0, RESOLUTION, u.size)
    return np.histogram(m, EDGES)[0] / u.size


Z_TRUE, Z_BIASED = N_Z * _z_shape(0.0), N_Z * _z_shape(BIAS)
_tt = np.exp(-(CENTRES - 70.0) / 40.0)
TT = N_TT * _tt / _tt.sum()
DATA = np.random.default_rng(20260930).poisson(Z_TRUE + TT).astype(float)


def make_axes() -> DataAxes:
    axes = DataAxes(
        (EDGES[0], EDGES[-1]),
        (0, 13_000),
        x_length=7.0,
        y_length=3.1,
        y_ticks=[0, 4_000, 8_000, 12_000],
        y_title="Events / 2 GeV",
        show_x_labels=False,
    )
    return axes.move_frame_to(A["frame"])


def make_stack(axes: DataAxes, z: np.ndarray, tt: np.ndarray):
    return stack_hist(axes, EDGES, [("tt", tt, COLOURS["tt"]), ("z", z, COLOURS["z"])])


def make_ratio(axes: DataAxes, prediction: np.ndarray):
    return ratio_panel(
        axes,
        EDGES,
        DATA,
        prediction,
        num_err=np.sqrt(DATA),
        y_range=(0.5, 1.5),
        x_title="m<sub>μμ</sub> [GeV]",
    )


def _legend_row(marker, tex: str) -> VGroup:
    return VGroup(marker, MathTex(tex, font_size=30)).arrange(RIGHT, buff=0.2)


def make_legend(axes: DataAxes) -> tuple[VGroup, VGroup]:
    """(data row, prediction rows), laid out together in the plot's upper right."""
    point = VGroup(
        Line(DOWN * 0.12, DOWN * -0.12, color=C.data, stroke_width=2.5),
        Dot(radius=0.05, color=C.data),
    )
    rows = VGroup(
        _legend_row(point, r"\mathrm{Data}"),
        _legend_row(Rectangle(width=0.3, height=0.2, fill_color=COLOURS["z"], fill_opacity=1,
                              stroke_width=0), r"Z/\gamma^* \to \mu\mu"),
        _legend_row(Rectangle(width=0.3, height=0.2, fill_color=COLOURS["tt"], fill_opacity=1,
                              stroke_width=0), r"t\bar{t}"),
    )  # fmt: skip
    for row in rows:  # markers in one column
        row[1].next_to(rows[0][0], RIGHT, buff=0.25).set_y(row[0].get_y())
        row[0].set_x(rows[0][0].get_x())
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    rows.next_to(axes.frame.get_corner(UR), DL, buff=0.25)
    return rows[0], VGroup(rows[1], rows[2])


def make_data(axes: DataAxes) -> VGroup:
    data = errorbars(axes, CENTRES, DATA, yerr=np.sqrt(DATA))
    return data.set_z_index(1)  # always drawn on top of the prediction


def final_state() -> dict:
    """The last frame. Keys in drawing order (the data sit on top via z_index)."""
    axes = make_axes()
    ratio = make_ratio(axes, Z_TRUE + TT)
    legend_data, legend_mc = make_legend(axes)
    shift = MathTex(rf"\Delta m = -{BIAS:g}\ \mathrm{{GeV}}", font_size=30)
    shift.next_to(axes.frame.get_corner(UL), DR, buff=0.25)
    return {
        "axes": axes,
        "ratio_axes": ratio.axes,
        "ratio_ref": ratio.ref,
        "legend_data": legend_data,
        "stack": make_stack(axes, Z_TRUE, TT),
        "legend_mc": legend_mc,
        "ratio_points": VGroup(ratio.errs, ratio.dots),
        "shift": shift,
        "data": make_data(axes),
    }


class StackDataRatio(Scene):
    def construct(self):
        axes = make_axes()
        biased = make_ratio(axes, Z_BIASED + TT)
        corrected = make_ratio(axes, Z_TRUE + TT)
        legend_data, legend_mc = make_legend(axes)
        data = make_data(axes)
        shift = MathTex(rf"\Delta m = -{BIAS:g}\ \mathrm{{GeV}}", font_size=30)
        shift.next_to(axes.frame.get_corner(UL), DR, buff=0.25)

        # The frame first, then the data: they will not move again.
        self.play(FadeIn(axes), FadeIn(biased.axes), FadeIn(biased.ref), run_time=0.8)
        self.play(
            LaggedStart(*(FadeIn(point) for point in data), lag_ratio=0.05, group=data),
            FadeIn(legend_data),
            run_time=1.2,
        )

        # The prediction grows in, with a biased momentum scale.
        stack = make_stack(axes, np.zeros_like(Z_TRUE), np.zeros_like(TT))
        self.add(stack)
        self.play(Transform(stack, make_stack(axes, Z_BIASED, TT)), FadeIn(legend_mc), run_time=1.2)
        points = VGroup(biased.errs, biased.dots)
        self.play(FadeIn(points), run_time=0.6)
        self.wait(0.6)

        # The scale correction: the prediction slides onto the data, the ratio flattens.
        self.play(
            Transform(stack, make_stack(axes, Z_TRUE, TT)),
            Transform(points, VGroup(corrected.errs, corrected.dots)),
            FadeIn(shift),
            run_time=1.5,
        )
        check_order(
            self,
            {
                "axes": axes,
                "ratio_axes": biased.axes,
                "ratio_ref": biased.ref,
                "legend_data": legend_data,
                "stack": stack,
                "legend_mc": legend_mc,
                "ratio_points": points,
                "shift": shift,
                "data": data,
            },
        )
        self.wait(0.1)
