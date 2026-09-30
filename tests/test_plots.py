from __future__ import annotations

import math

import numpy as np
import pytest
from manim import DL, UR

from manim_hep.plots import (
    DataAxes,
    band,
    errorbars,
    ratio_panel,
    stack_hist,
    step_hist,
)
from manim_hep.style import intrusions, use_theme

EDGES = np.linspace(60, 120, 7)


@pytest.fixture(autouse=True)
def _theme():
    use_theme("generic")


@pytest.fixture(scope="module")
def axes():
    use_theme("generic")
    return DataAxes((60, 120), (0, 1000), x_title="m [GeV]", y_title="Events")


def test_c2p_maps_the_range_onto_the_frame(axes):
    assert np.allclose(axes.c2p(60, 0), axes.frame.get_corner(DL))
    assert np.allclose(axes.c2p(120, 1000), axes.frame.get_corner(UR))
    x, y = axes.p2c(axes.c2p(75, 250))
    assert (x, y) == (pytest.approx(75), pytest.approx(250))


def test_move_frame_to_moves_the_plot_area_and_c2p_follows():
    ax = DataAxes((0, 10), (0, 5), x_title="x", y_title="y").move_frame_to((1.0, -0.5))
    assert np.allclose(ax.frame.get_center(), [1.0, -0.5, 0])
    assert np.allclose(ax.c2p(5, 2.5), [1.0, -0.5, 0])


def test_default_ticks_are_nice(axes):
    assert axes.x_ticks == [60, 70, 80, 90, 100, 110, 120]
    assert axes.y_ticks == [0, 200, 400, 600, 800, 1000]
    assert len(axes.x_labels) == 7 and len(axes.y_labels) == 6


def test_tick_labels_use_the_theme_font(axes):
    assert axes.x_labels[0].font == "DejaVu Sans"


def test_log_axis_spaces_decades_evenly_and_floors_zero():
    ax = DataAxes((0, 1), (1e-1, 1e3), log_y=True)
    ys = [ax.c2p(0, 10.0**k)[1] for k in range(-1, 4)]
    assert np.allclose(np.diff(ys), np.diff(ys)[0])
    assert ax.c2p(0.5, 0)[1] == pytest.approx(ax.c2p(0.5, 0.1)[1])
    assert ax.y_ticks == [0.1, 1, 10, 100, 1000]
    with pytest.raises(ValueError, match="positive lower limit"):
        DataAxes((0, 1), (0, 10), log_y=True)


def test_bad_ranges_are_explained():
    with pytest.raises(ValueError, match="low < high"):
        DataAxes((1, 0), (0, 1))


def test_default_axes_stay_out_of_the_title_band(axes):
    assert intrusions(axes) == []


def test_step_hist_points(axes):
    counts = [10, 200, 800, 600, 100, 5]
    outline = step_hist(axes, EDGES, counts)
    assert len(outline.get_anchors()) >= 12
    assert np.allclose(outline.get_start(), axes.c2p(60, 10))
    filled = step_hist(axes, EDGES, counts, fill_opacity=0.5)
    assert np.allclose(filled.get_vertices()[0], axes.c2p(60, 0))
    with pytest.raises(ValueError, match="needs 6 values"):
        step_hist(axes, EDGES, [1, 2])


def test_stack_keeps_its_point_count_so_it_can_morph(axes):
    a = stack_hist(axes, EDGES, [("bkg", [100] * 6), ("sig", [0] * 6)])
    b = stack_hist(
        axes, EDGES, [("bkg", [50, 60, 70, 80, 90, 100]), ("sig", [5, 50, 300, 50, 5, 0])]
    )
    for la, lb in zip(a, b, strict=True):
        assert len(la.points) == len(lb.points) == len(a[0].points)
    assert np.allclose(b.total, b.counts.sum(axis=0))
    assert b.layer["sig"] is b[1]
    assert a[1].get_stroke_width() == 0  # an empty layer draws no hairline
    assert b.names == ["bkg", "sig"]


def test_stack_layers_default_to_the_cycle_colours(axes):
    theme = use_theme("generic")
    s = stack_hist(axes, EDGES, [("a", [1] * 6), ("b", [1] * 6)])
    assert s[0].get_fill_color().to_hex().upper() == theme.palette.cycle[0]
    assert s[1].get_fill_color().to_hex().upper() == theme.palette.cycle[1]


def test_errorbars_are_capless_and_asymmetric_errors_work(axes):
    centres = (EDGES[:-1] + EDGES[1:]) / 2
    counts = np.array([10.0, 200, 800, 600, 100, 5])
    pts = errorbars(axes, centres, counts, yerr=np.sqrt(counts))
    assert len(pts) == 6 and all(len(p) == 2 for p in pts)
    asym = errorbars(axes, centres[:1], counts[:1], yerr=([1.0], [4.0]))
    bar = asym[0][1]
    assert bar.get_start()[1] == pytest.approx(axes.c2p(65, 9)[1])
    assert bar.get_end()[1] == pytest.approx(axes.c2p(65, 14)[1])


def test_band_step_and_smooth(axes):
    b = band(axes, EDGES, [90] * 6, [110] * 6, step=True)
    assert len(b.get_vertices()) == 24
    s = band(axes, [60, 90, 120], [1, 2, 3], [4, 5, 6])
    assert len(s.get_vertices()) == 6
    with pytest.raises(ValueError, match="same length"):
        band(axes, [60, 90], [1], [2, 3])


def test_ratio_panel_lines_up_and_skips_empty_bins():
    main = DataAxes((60, 120), (0, 1000), show_x_labels=False).move_frame_to((0, 0.6))
    rp = ratio_panel(
        main,
        EDGES,
        [10, 20, 30, 40, 50, 60],
        [10, 0, 30, 20, 50, 60],
        num_err=[1, 1, 1, 1, 1, 1],
        x_title="m [GeV]",
    )
    assert rp.axes.frame.get_left()[0] == pytest.approx(main.frame.get_left()[0])
    assert rp.axes.frame.width == pytest.approx(main.frame.width)
    assert rp.axes.frame.get_top()[1] < main.frame.get_bottom()[1]
    assert rp.bins == [0, 2, 3, 4, 5]
    assert math.isnan(rp.ratio[1]) and rp.ratio[3] == pytest.approx(2.0)
    assert len(rp.dots) == len(rp.errs) == 5
