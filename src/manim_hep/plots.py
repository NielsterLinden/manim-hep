"""Result plots drawn natively in Manim, in the look of HEP figures.

Position the axes first, then build content through ``axes.c2p``::

    axes = DataAxes((60, 120), (0, 900), x_title="m<sub>μμ</sub> [GeV]",
                    y_title="Events / 2 GeV").move_frame_to((0, -0.4))
    mc = stack_hist(axes, edges, [("Z→μμ", z_counts), ("tt̄", tt_counts)])
    data = errorbars(axes, centres, counts, yerr=np.sqrt(counts))

Histograms are step outlines: the polyline *is* the binning. Stacks keep a fixed
number of points per layer, so ``Transform(old_stack, new_stack)`` morphs bin by
bin, and in a data/prediction comparison "the data never move".
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence

import numpy as np
from manim import (
    DL,
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    UR,
    DashedLine,
    Dot,
    Line,
    MarkupText,
    Mobject,
    Polygon,
    Rectangle,
    Text,
    VGroup,
    VMobject,
)

from manim_hep.style import _sized_text, current_theme

__all__ = ["DataAxes", "band", "errorbars", "ratio_panel", "stack_hist", "step_hist"]

_DIGIT_HEIGHT: dict[str, float] = {}


def _digit_font_size(height: float) -> float:
    """Font size at which a digit in the theme font is ``height`` tall."""
    font = current_theme().font
    if font not in _DIGIT_HEIGHT:
        _DIGIT_HEIGHT[font] = Text("0", font_size=48).height / 48
    return height / _DIGIT_HEIGHT[font]


def _nice_ticks(lo: float, hi: float, target: int = 6) -> list[float]:
    span = hi - lo
    raw = span / max(target - 1, 1)
    power = 10 ** math.floor(math.log10(raw))
    step = min((m * power for m in (1, 2, 2.5, 5, 10)), key=lambda s: abs(span / s - target))
    first = math.ceil(lo / step - 1e-9) * step
    ticks = []
    value = first
    while value <= hi + step * 1e-9:
        ticks.append(round(value, 12))
        value += step
    return ticks


def _inner_ticks(lo: float, hi: float) -> list[float]:
    """Nice ticks strictly inside (lo, hi), so stacked panels never share a label."""
    return [t for t in _nice_ticks(lo, hi, target=3) if lo < t < hi]


def _title(text: str | Mobject, font_size: float, color) -> Mobject:
    if isinstance(text, str):
        return _sized_text(MarkupText, text, font_size, color=color)
    return text


class DataAxes(VGroup):
    """A plot frame with inward ticks on all sides and labels in the theme font.

    Parameters
    ----------
    x_range, y_range
        ``(low, high)`` in data units. With ``log_y`` the y values are real
        values (e.g. ``(1e-1, 1e5)``), not exponents.
    x_ticks, y_ticks
        Tick values; by default about six "nice" values (decades on a log axis).
    x_title, y_title
        A string (rendered as ``MarkupText``, so ``m<sub>ℓℓ</sub> [GeV]`` works)
        or any mobject, e.g. a ``MathTex``. Placed HEP-style: x at the right end,
        y at the top.
    log_y, y_floor
        Logarithmic y axis. Values below ``y_floor`` (default: the lower end of the
        range) are drawn at the floor, so empty bins sit on the axis.
    show_x_labels, show_y_labels
        Hide tick labels, e.g. on a main panel above a ratio panel.

    ``c2p(x, y)`` converts data to scene coordinates at any time, even after the
    axes were moved; ``frame`` is the plot area.
    """

    def __init__(
        self,
        x_range: Sequence[float],
        y_range: Sequence[float],
        *,
        x_length: float = 7.0,
        y_length: float = 4.0,
        x_ticks: Sequence[float] | None = None,
        y_ticks: Sequence[float] | None = None,
        x_fmt: str = "{:g}",
        y_fmt: str = "{:g}",
        x_title: str | Mobject | None = None,
        y_title: str | Mobject | None = None,
        log_y: bool = False,
        y_floor: float | None = None,
        show_x_labels: bool = True,
        show_y_labels: bool = True,
        tick_height: float = 0.2,
        tick_length: float = 0.1,
        stroke_width: float = 2.5,
        color=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        (self.x_min, self.x_max), (self.y_min, self.y_max) = (
            map(float, x_range),
            map(float, y_range),
        )
        if self.x_max <= self.x_min or self.y_max <= self.y_min:
            raise ValueError("ranges are (low, high) with low < high")
        if log_y and self.y_min <= 0:
            raise ValueError("a log y axis needs a positive lower limit")
        self.log_y = log_y
        self.y_floor = float(y_floor) if y_floor is not None else (self.y_min if log_y else None)
        self.x_fmt, self.y_fmt, self.tick_height = x_fmt, y_fmt, tick_height
        self.tick_length, self.stroke_width = tick_length, stroke_width
        self.color_ = color if color is not None else current_theme().palette.ink

        self.frame = Rectangle(
            width=x_length, height=y_length, stroke_color=self.color_, stroke_width=stroke_width
        )
        self.add(self.frame)
        if x_ticks is None:
            x_ticks = _nice_ticks(self.x_min, self.x_max)
        if y_ticks is None:
            y_ticks = self._default_log_ticks() if log_y else _nice_ticks(self.y_min, self.y_max)
        self.x_ticks = [float(v) for v in x_ticks if self.x_min <= v <= self.x_max]
        self.y_ticks = [float(v) for v in y_ticks if self.y_min <= v <= self.y_max]

        self.ticks = VGroup()
        for x in self.x_ticks:
            bottom, top = self.c2p(x, self.y_min), self.c2p(x, self.y_max)
            self.ticks.add(
                Line(bottom, bottom + UP * tick_length), Line(top, top + DOWN * tick_length)
            )
        for y in self.y_ticks:
            left, right = self.c2p(self.x_min, y), self.c2p(self.x_max, y)
            self.ticks.add(
                Line(left, left + RIGHT * tick_length), Line(right, right + LEFT * tick_length)
            )
        self.ticks.set_stroke(self.color_, stroke_width)
        self.add(self.ticks)

        size = _digit_font_size(tick_height)
        self.x_labels, self.y_labels = VGroup(), VGroup()
        if show_x_labels:
            for x in self.x_ticks:
                lab = _sized_text(Text, x_fmt.format(x), size, color=self.color_)
                lab.next_to(self.c2p(x, self.y_min), DOWN, buff=0.14)
                self.x_labels.add(lab)
        if show_y_labels:
            for y in self.y_ticks:
                if log_y:
                    exponent = math.log10(y)
                    text = (
                        f"{exponent:g}"
                        if abs(exponent - round(exponent)) > 1e-9
                        else f"{round(exponent)}"
                    )
                    lab = _sized_text(MarkupText, f"10<sup>{text}</sup>", size, color=self.color_)
                else:
                    lab = _sized_text(Text, y_fmt.format(y), size, color=self.color_)
                lab.next_to(self.c2p(self.x_min, y), LEFT, buff=0.14)
                self.y_labels.add(lab)
        self.add(self.x_labels, self.y_labels)

        title_size = size * 1.15
        self.x_title = self.y_title = None
        if x_title is not None:
            self.x_title = _title(x_title, title_size, self.color_)
            below = self.x_labels if len(self.x_labels) else self.frame
            self.x_title.next_to(below, DOWN, buff=0.16)
            self.x_title.align_to(self.frame, RIGHT)
            self.add(self.x_title)
        if y_title is not None:
            self.y_title = _title(y_title, title_size, self.color_).rotate(math.pi / 2)
            beside = self.y_labels if len(self.y_labels) else self.frame
            self.y_title.next_to(beside, LEFT, buff=0.16)
            self.y_title.align_to(self.frame, UP)
            self.add(self.y_title)

    def _default_log_ticks(self) -> list[float]:
        lo, hi = math.ceil(math.log10(self.y_min) - 1e-9), math.floor(math.log10(self.y_max) + 1e-9)
        step = max(1, math.ceil((hi - lo + 1) / 7))
        return [10.0**k for k in range(lo, hi + 1, step)]

    @property
    def y_base(self) -> float:
        """The data value of the bottom edge (where histograms start)."""
        return self.y_floor if self.y_floor is not None else self.y_min

    def _fy(self, y: float) -> float:
        if self.y_floor is not None:
            y = max(y, self.y_floor)
        if self.log_y:
            return (math.log10(y) - math.log10(self.y_min)) / (
                math.log10(self.y_max) - math.log10(self.y_min)
            )
        return (y - self.y_min) / (self.y_max - self.y_min)

    def c2p(self, x: float, y: float) -> np.ndarray:
        """Data coordinates → scene point."""
        x0, y0 = self.frame.get_corner(DL)[:2]
        x1, y1 = self.frame.get_corner(UR)[:2]
        fx = (float(x) - self.x_min) / (self.x_max - self.x_min)
        return np.array([x0 + fx * (x1 - x0), y0 + self._fy(float(y)) * (y1 - y0), 0.0])

    def p2c(self, point: Sequence[float]) -> tuple[float, float]:
        """Scene point → data coordinates."""
        x0, y0 = self.frame.get_corner(DL)[:2]
        x1, y1 = self.frame.get_corner(UR)[:2]
        fx, fy = (point[0] - x0) / (x1 - x0), (point[1] - y0) / (y1 - y0)
        x = self.x_min + fx * (self.x_max - self.x_min)
        if self.log_y:
            lo, hi = math.log10(self.y_min), math.log10(self.y_max)
            return x, 10 ** (lo + fy * (hi - lo))
        return x, self.y_min + fy * (self.y_max - self.y_min)

    def move_frame_to(self, point: Sequence[float]) -> DataAxes:
        """Move the axes so the plot area (not the labels) is centred on ``point``."""
        target = np.array([*point, 0.0][:3], dtype=float)
        self.shift(target - self.frame.get_center())
        return self

    def polyline(self, xs: Sequence[float], ys: Sequence[float], *, color=None, stroke_width=3.0):
        """Straight segments through data points."""
        line = VMobject(color=color or current_theme().palette.ink, stroke_width=stroke_width)
        line.set_points_as_corners([self.c2p(x, y) for x, y in zip(xs, ys, strict=True)])
        return line

    def plot(
        self,
        function: Callable[[float], float],
        *,
        x_range: Sequence[float] | None = None,
        samples: int = 200,
        color=None,
        stroke_width: float = 3.0,
    ) -> VMobject:
        """A curve ``y = function(x)`` sampled over ``x_range`` (default: the axis range)."""
        lo, hi = x_range if x_range is not None else (self.x_min, self.x_max)
        xs = np.linspace(lo, hi, samples)
        return self.polyline(xs, [function(x) for x in xs], color=color, stroke_width=stroke_width)


def _step_points(axes: DataAxes, edges, heights) -> list[np.ndarray]:
    points = []
    for i, h in enumerate(heights):
        points += [axes.c2p(edges[i], h), axes.c2p(edges[i + 1], h)]
    return points


def _check_bins(edges, counts, what: str = "counts"):
    edges = np.asarray(edges, dtype=float)
    counts = np.asarray(counts, dtype=float)
    if edges.ndim != 1 or len(edges) < 2 or np.any(np.diff(edges) <= 0):
        raise ValueError("edges must be increasing, with at least two values")
    if counts.shape != (len(edges) - 1,):
        raise ValueError(f"{what} needs {len(edges) - 1} values for {len(edges)} edges")
    return edges, counts


def step_hist(
    axes: DataAxes,
    edges: Sequence[float],
    counts: Sequence[float],
    *,
    color=None,
    stroke_width: float = 3.0,
    fill_opacity: float = 0.0,
) -> VMobject:
    """A histogram as a step outline; with ``fill_opacity > 0`` a filled polygon."""
    edges, counts = _check_bins(edges, counts)
    color = color or current_theme().palette.ink
    points = _step_points(axes, edges, counts)
    if fill_opacity > 0:
        base = axes.y_base
        return Polygon(
            axes.c2p(edges[0], base),
            *points,
            axes.c2p(edges[-1], base),
            stroke_color=color,
            stroke_width=stroke_width,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
    line = VMobject(color=color, stroke_width=stroke_width)
    line.set_points_as_corners(points)
    return line


def stack_hist(
    axes: DataAxes,
    edges: Sequence[float],
    layers: Sequence[tuple],
    *,
    stroke_width: float = 0.0,
    fill_opacity: float = 0.95,
) -> VGroup:
    """A stacked histogram; ``layers`` are ``(name, counts[, color])``, bottom first.

    Every layer is one polygon with the same number of points (4 per bin), also
    when its counts are all zero, so two stacks built from the same layer list
    ``Transform`` into each other bin by bin.

    Attributes: ``names``, ``layer`` (name → polygon), ``counts`` (layers × bins),
    ``cum`` (running sums, first row zeros) and ``total``.
    """
    edges = np.asarray(edges, dtype=float)
    cycle = current_theme().palette.cycle
    names, rows, colors = [], [], []
    for i, layer in enumerate(layers):
        if len(layer) not in (2, 3):
            raise ValueError(f"a layer is (name, counts[, color]), got {layer!r}")
        _, counts = _check_bins(edges, layer[1], f"layer {layer[0]!r}")
        names.append(layer[0])
        rows.append(counts)
        colors.append(layer[2] if len(layer) == 3 else cycle[i % len(cycle)])
    counts = np.array(rows) if rows else np.zeros((0, len(edges) - 1))
    cum = np.vstack([np.zeros(len(edges) - 1), np.cumsum(counts, axis=0)])
    group = VGroup()
    group.layer = {}
    for i, (name, color) in enumerate(zip(names, colors, strict=True)):
        top = _step_points(axes, edges, cum[i + 1])
        bottom = _step_points(axes, edges, cum[i])
        empty = not np.any(counts[i] > 0)
        polygon = Polygon(
            *top,
            *bottom[::-1],
            stroke_color=color,
            stroke_width=0 if empty else stroke_width,
            fill_color=color,
            fill_opacity=fill_opacity,
        )
        group.add(polygon)
        group.layer[name] = polygon
    group.names, group.counts, group.cum, group.total = names, counts, cum, cum[-1]
    return group


def _errors(err, n: int) -> tuple[np.ndarray, np.ndarray]:
    if isinstance(err, tuple) and len(err) == 2:
        lo, hi = (np.broadcast_to(np.asarray(e, dtype=float), (n,)) for e in err)
        return lo, hi
    sym = np.broadcast_to(np.asarray(err, dtype=float), (n,))
    return sym, sym


def errorbars(
    axes: DataAxes,
    x: Sequence[float],
    y: Sequence[float],
    yerr,
    *,
    xerr=None,
    color=None,
    radius: float = 0.05,
    stroke_width: float = 2.5,
) -> VGroup:
    """Data points with error bars, without caps (the HEP convention).

    ``yerr`` (and ``xerr``) is one value, one per point, or a ``(low, high)``
    tuple for asymmetric errors. The result holds one ``VGroup(dot, bar[, xbar])``
    per point, so ``Transform`` works point by point.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.shape != y.shape:
        raise ValueError("x and y need the same length")
    color = color or current_theme().palette.data
    lo, hi = _errors(yerr, len(x))
    xlo, xhi = _errors(xerr, len(x)) if xerr is not None else (None, None)
    group = VGroup()
    for i, (xi, yi) in enumerate(zip(x, y, strict=True)):
        point = VGroup(Dot(axes.c2p(xi, yi), radius=radius, color=color))
        point.add(
            Line(
                axes.c2p(xi, yi - lo[i]),
                axes.c2p(xi, yi + hi[i]),
                color=color,
                stroke_width=stroke_width,
            )
        )
        if xlo is not None:
            point.add(
                Line(
                    axes.c2p(xi - xlo[i], yi),
                    axes.c2p(xi + xhi[i], yi),
                    color=color,
                    stroke_width=stroke_width,
                )
            )
        group.add(point)
    return group


def band(
    axes: DataAxes,
    x: Sequence[float],
    low: Sequence[float],
    high: Sequence[float],
    *,
    color=None,
    opacity: float = 0.25,
    step: bool = False,
) -> Polygon:
    """A filled band between ``low`` and ``high``.

    With ``step=True``, ``x`` are bin edges and ``low``/``high`` one value per bin
    (an uncertainty band on a histogram); otherwise all three have equal length.
    """
    low, high = np.asarray(low, dtype=float), np.asarray(high, dtype=float)
    if step:
        edges, _ = _check_bins(x, low, "low")
        _check_bins(x, high, "high")
        top, bottom = _step_points(axes, edges, high), _step_points(axes, edges, low)
    else:
        x = np.asarray(x, dtype=float)
        if not (len(x) == len(low) == len(high)):
            raise ValueError("x, low and high need the same length")
        top = [axes.c2p(a, b) for a, b in zip(x, high, strict=True)]
        bottom = [axes.c2p(a, b) for a, b in zip(x, low, strict=True)]
    color = color or current_theme().palette.muted
    return Polygon(*top, *bottom[::-1], stroke_width=0, fill_color=color, fill_opacity=opacity)


def ratio_panel(
    main: DataAxes,
    edges: Sequence[float],
    num: Sequence[float],
    den: Sequence[float],
    *,
    y_range: Sequence[float] = (0.5, 1.5),
    y_length: float = 1.2,
    y_ticks: Sequence[float] | None = None,
    num_err: Sequence[float] | None = None,
    gap: float = 0.12,
    y_title: str | Mobject | None = "Data / Pred.",
    x_title: str | Mobject | None = None,
    color=None,
) -> VGroup:
    """A ratio panel (``num / den`` per bin) directly under ``main``.

    The panel copies the main plot's x range, width and ticks, and its frame lines
    up with the main frame. Build ``main`` with ``show_x_labels=False`` so the tick
    labels are not drawn twice. Bins with ``den == 0`` get no point.

    Attributes: ``axes``, ``ref`` (the line at 1), ``dots``, ``errs``, ``ratio``
    (NaN where ``den == 0``) and ``bins`` (the bins that got a point).
    """
    edges, num = _check_bins(edges, num, "num")
    _, den = _check_bins(edges, den, "den")
    axes = DataAxes(
        (main.x_min, main.x_max),
        y_range,
        x_length=main.frame.width,
        y_length=y_length,
        x_ticks=main.x_ticks,
        y_ticks=y_ticks if y_ticks is not None else _inner_ticks(*y_range),
        x_fmt=main.x_fmt,
        x_title=x_title,
        y_title=y_title,
        tick_height=main.tick_height,
        tick_length=main.tick_length,
        stroke_width=main.stroke_width,
    )
    axes.shift(main.frame.get_corner(DL) + DOWN * gap - axes.frame.get_corner(UL))
    muted = current_theme().palette.muted
    ref = DashedLine(
        axes.c2p(main.x_min, 1.0), axes.c2p(main.x_max, 1.0), color=muted, stroke_width=2.0
    )
    ok = den > 0
    ratio = np.full(len(den), np.nan)
    ratio[ok] = num[ok] / den[ok]
    centres = (edges[:-1] + edges[1:]) / 2
    color = color or current_theme().palette.data
    dots, errs, bins = VGroup(), VGroup(), []
    for i in np.flatnonzero(ok):
        dots.add(Dot(axes.c2p(centres[i], ratio[i]), radius=0.04, color=color))
        if num_err is not None:
            e = float(num_err[i]) / den[i]
            errs.add(
                Line(
                    axes.c2p(centres[i], ratio[i] - e),
                    axes.c2p(centres[i], ratio[i] + e),
                    color=color,
                    stroke_width=2.0,
                )
            )
        bins.append(int(i))
    group = VGroup(axes, ref, errs, dots)
    group.axes, group.ref, group.dots, group.errs = axes, ref, dots, errs
    group.ratio, group.bins = ratio, bins
    return group
