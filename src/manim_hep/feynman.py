"""Tree-level Feynman diagrams from a coordinate dictionary.

Every vertex position lives in one dict, so a diagram is reproducible across
chained clips and is tuned in one place::

    V = {"q": (-3, 1.5), "qbar": (-3, -1.5), "a": (-1, 0), "b": (1, 0),
         "l-": (3, 1.5), "l+": (3, -1.5)}
    diagram = FeynmanDiagram(V, [
        ("q", "a", "fermion", r"q"),
        ("a", "qbar", "fermion", r"\\bar{q}"),
        ("a", "b", "photon", r"\\gamma^*/Z"),
        ("b", "l-", "fermion", r"\\ell^-"),
        ("l+", "b", "fermion", r"\\ell^+"),
    ])
    self.play(diagram.draw_in_order())

Line styles follow the usual conventions (as in TikZ-Feynman): fermions are
solid with an arrow along the fermion flow, photons and massive vector bosons
are wavy (the label tells them apart), gluons are curly and scalars dashed.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from manim import (
    PI,
    AnimationGroup,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Mobject,
    Polygon,
    VGroup,
    VMobject,
    linear,
)

from manim_hep.style import current_theme

__all__ = [
    "EDGE_KINDS",
    "FeynmanDiagram",
    "fermion",
    "gluon",
    "photon",
    "scalar",
    "vertex",
]

EDGE_KINDS = ("fermion", "antifermion", "photon", "boson", "gluon", "scalar", "plain")


def _p(point: Sequence[float]) -> np.ndarray:
    arr = np.asarray(point, dtype=float)
    return np.append(arr, 0.0) if arr.shape == (2,) else arr


def _frame(start, end) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Start, unit direction, unit normal (direction turned left) and length."""
    a, b = _p(start), _p(end)
    length = float(np.linalg.norm(b - a))
    if length == 0:
        raise ValueError("a line needs two different end points")
    u = (b - a) / length
    return a, u, np.array([-u[1], u[0], 0.0]), length


def _ink(color):
    return color if color is not None else current_theme().palette.ink


def fermion(
    start,
    end,
    *,
    arrow: bool = True,
    color=None,
    stroke_width: float = 3.0,
    tip_length: float = 0.22,
) -> VGroup:
    """A straight fermion line with an arrow at its middle, pointing start → end."""
    a, u, n, length = _frame(start, end)
    color = _ink(color)
    line = Line(a, a + u * length, color=color, stroke_width=stroke_width)
    group = VGroup(line)
    if arrow:
        mid = a + u * length / 2
        tip = Polygon(
            mid + u * tip_length / 2,
            mid - u * tip_length / 2 + n * tip_length * 0.42,
            mid - u * tip_length / 2 - n * tip_length * 0.42,
            color=color,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )
        group.add(tip)
    return group


def photon(
    start,
    end,
    *,
    amplitude: float = 0.09,
    wavelength: float = 0.45,
    color=None,
    stroke_width: float = 3.0,
) -> VMobject:
    """A wavy line (photon, W or Z) with a whole number of half-waves."""
    a, u, n, length = _frame(start, end)
    half_waves = max(2, round(2 * length / wavelength))
    t = np.linspace(0.0, 1.0, max(60, 24 * half_waves))
    points = [a + u * (s * length) + n * amplitude * np.sin(np.pi * half_waves * s) for s in t]
    wave = VMobject(color=_ink(color), stroke_width=stroke_width)
    wave.set_points_smoothly(points)
    return wave


def gluon(
    start,
    end,
    *,
    radius: float = 0.12,
    loops: int | None = None,
    color=None,
    stroke_width: float = 3.0,
) -> VMobject:
    """A curly gluon line: loops of ``radius`` centred on the line, ends on the line."""
    a, u, n, length = _frame(start, end)
    if loops is None:
        loops = max(2, round(length * 1.8 / (2 * np.pi * radius)))
    step = length / (2 * np.pi * loops)  # advance per radian; loops form since step < radius
    theta = np.linspace(-np.pi / 2, 2 * np.pi * loops - np.pi / 2, 40 * loops)
    x = step * theta - radius * np.sin(theta) + (step * np.pi / 2 - radius)
    y = radius * np.cos(theta)
    curl = VMobject(color=_ink(color), stroke_width=stroke_width)
    curl.set_points_smoothly([a + u * xi + n * yi for xi, yi in zip(x, y, strict=True)])
    return curl


def scalar(
    start, end, *, color=None, stroke_width: float = 3.0, dash_length: float = 0.12
) -> DashedLine:
    """A dashed line (Higgs or other scalar)."""
    a, u, _, length = _frame(start, end)
    return DashedLine(
        a, a + u * length, dash_length=dash_length, color=_ink(color), stroke_width=stroke_width
    )


def vertex(point, *, radius: float = 0.06, color=None) -> Dot:
    """A vertex dot."""
    return Dot(_p(point), radius=radius, color=_ink(color))


def _edge_line(kind: str, a, b, color) -> Mobject:
    if kind == "fermion":
        return fermion(a, b, color=color)
    if kind == "antifermion":  # drawn start → end, arrow against the drawing direction
        line = fermion(a, b, color=color)
        line[1].rotate(PI, about_point=(_p(a) + _p(b)) / 2)
        return line
    if kind in ("photon", "boson"):
        return photon(a, b, color=color)
    if kind == "gluon":
        return gluon(a, b, color=color)
    if kind == "scalar":
        return scalar(a, b, color=color)
    return fermion(a, b, arrow=False, color=color)


class FeynmanDiagram(VGroup):
    """A diagram built from named vertices and an ordered list of edges.

    Parameters
    ----------
    vertices
        ``{name: (x, y)}`` in scene units.
    edges
        ``(start, end, kind)`` or ``(start, end, kind, label)`` tuples, in build
        order. ``kind`` is one of :data:`EDGE_KINDS`; ``label`` is a LaTeX string
        (rendered with ``MathTex``) or any mobject.
    label_buff
        Gap between an edge and its label. Each label sits on the side of its edge
        with more room, away from the other edges (so legs meeting in a "<" keep
        their labels outside the wedge); on a tie, above or to the left.

    Attributes
    ----------
    lines : VGroup
        The drawn edges, in edge order.
    dots : VGroup
        One dot per internal vertex.
    labels : VGroup
        The edge labels that exist, in edge order.
    edge_labels : list
        One entry per edge: its label, or ``None``.
    points_by_name : dict
        Vertex name → scene position.
    """

    def __init__(
        self,
        vertices: Mapping[str, Sequence[float]],
        edges: Sequence[tuple],
        *,
        label_buff: float = 0.18,
        label_size: float = 40,
        color=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.points_by_name = {name: _p(p) for name, p in vertices.items()}
        self.edge_list: list[tuple[str, str, str]] = []
        self.lines, self.dots, self.labels = VGroup(), VGroup(), VGroup()
        self.edge_labels: list[Mobject | None] = []
        self._dot_of: dict[str, Dot] = {}
        degree: dict[str, int] = dict.fromkeys(self.points_by_name, 0)
        pending: list[tuple[Mobject, np.ndarray, np.ndarray, int]] = []

        for edge in edges:
            if len(edge) not in (3, 4):
                raise ValueError(f"an edge is (start, end, kind[, label]), got {edge!r}")
            start, end, kind = edge[:3]
            text = edge[3] if len(edge) == 4 else None
            for name in (start, end):
                if name not in self.points_by_name:
                    raise KeyError(f"edge {edge[:3]!r} uses unknown vertex {name!r}")
            if kind not in EDGE_KINDS:
                raise ValueError(f"unknown edge kind {kind!r}; use one of: {', '.join(EDGE_KINDS)}")
            a, b = self.points_by_name[start], self.points_by_name[end]
            self.lines.add(_edge_line(kind, a, b, color))
            self.edge_list.append((start, end, kind))
            degree[start] += 1
            degree[end] += 1
            lab = None
            if text is not None:
                lab = MathTex(text, font_size=label_size) if isinstance(text, str) else text
                if color is not None and isinstance(text, str):
                    lab.set_color(color)
                pending.append((lab, a, b, len(self.edge_list) - 1))
                self.labels.add(lab)
            self.edge_labels.append(lab)

        for lab, a, b, index in pending:
            others = [
                np.linspace(self.points_by_name[s], self.points_by_name[e], 25)
                for i, (s, e, _) in enumerate(self.edge_list)
                if i != index
            ]
            self._place_label(lab, a, b, np.concatenate(others) if others else None, label_buff)

        for name, count in degree.items():
            if count >= 2:  # internal vertex
                dot = vertex(self.points_by_name[name], color=color)
                self._dot_of[name] = dot
                self.dots.add(dot)
        self.add(self.lines, self.dots, self.labels)

    @staticmethod
    def _place_label(lab: Mobject, a, b, others: np.ndarray | None, buff: float) -> None:
        """Put ``lab`` beside edge a–b, on the side farther from the other edges."""
        _, _, n, _ = _frame(a, b)
        mid = (a + b) / 2

        def spot(side: np.ndarray) -> np.ndarray:
            extent = abs(side[0]) * lab.width / 2 + abs(side[1]) * lab.height / 2
            return mid + side * (buff + extent)

        def room(side: np.ndarray) -> float:
            if others is None:
                return 0.0
            return float(np.min(np.linalg.norm(others - spot(side), axis=1)))

        preferred = n if (n[1] > 1e-6 or (abs(n[1]) <= 1e-6 and n[0] < 0)) else -n
        other = -preferred
        side = other if room(other) > room(preferred) + 1e-3 else preferred
        lab.move_to(spot(side))

    def edge(self, start: str, end: str) -> Mobject:
        """The line drawn for the edge between ``start`` and ``end`` (either order)."""
        for (a, b, _), line in zip(self.edge_list, self.lines, strict=True):
            if {a, b} == {start, end}:
                return line
        raise KeyError(f"no edge between {start!r} and {end!r}")

    def draw_in_order(self, time_per_edge: float = 0.6) -> AnimationGroup:
        """Draw the edges one by one in build order, each followed by its label.

        The diagram stays one group in the scene (so ``check_order`` can name it).
        """
        steps = []
        seen: set[str] = set()
        for (start, end, _), line, lab in zip(
            self.edge_list, self.lines, self.edge_labels, strict=True
        ):
            parts = [Create(line, run_time=time_per_edge, rate_func=linear)]
            for name in (start, end):
                if name in self._dot_of and name not in seen:
                    seen.add(name)
                    parts.append(FadeIn(self._dot_of[name], run_time=time_per_edge * 0.4))
            if lab is not None:
                parts.append(FadeIn(lab, run_time=time_per_edge * 0.5))
            steps.append(AnimationGroup(*parts, lag_ratio=0.6))
        return AnimationGroup(*steps, lag_ratio=1.0, group=self)
