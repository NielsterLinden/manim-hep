from __future__ import annotations

import numpy as np
import pytest
from manim import DashedLine, Dot, Scene, Square, VGroup

from manim_hep.build import check_order
from manim_hep.feynman import EDGE_KINDS, FeynmanDiagram, fermion, gluon, photon, scalar
from manim_hep.style import use_theme

V = {
    "q": (-3, 1.5),
    "qbar": (-3, -1.5),
    "a": (-1, 0),
    "b": (1, 0),
    "l-": (3, 1.5),
    "l+": (3, -1.5),
}


def _labels():
    return [Square(0.3) for _ in range(5)]  # stand-ins, so the tests need no LaTeX


def _drell_yan(labels=None):
    labels = labels or _labels()
    return FeynmanDiagram(
        V,
        [
            ("q", "a", "fermion", labels[0]),
            ("a", "qbar", "fermion", labels[1]),
            ("a", "b", "photon", labels[2]),
            ("b", "l-", "fermion", labels[3]),
            ("l+", "b", "fermion", labels[4]),
        ],
    )


@pytest.fixture(autouse=True)
def _theme():
    use_theme("generic")


def _ends(mob):
    line = mob[0] if isinstance(mob, VGroup) else mob
    return line.get_start(), line.get_end()


@pytest.mark.parametrize("make", [fermion, photon, gluon, scalar])
def test_lines_start_and_end_on_their_points(make):
    a, b = np.array([-1.0, 0.5, 0]), np.array([2.0, -1.0, 0])
    start, end = _ends(make(a, b))
    assert np.allclose(start, a, atol=1e-6)
    assert np.allclose(end, b, atol=1e-6)


def test_gluon_loops_stay_close_to_the_line():
    g = gluon((0, 0), (3, 0), radius=0.12)
    assert g.height == pytest.approx(0.24, abs=0.02)


def test_fermion_arrow_points_along_the_flow():
    f = fermion((0, 0), (2, 0))
    tip = f[1]
    assert tip.get_vertices()[0][0] > 1.0  # the first vertex is the arrow point
    d = _drell_yan()
    anti = FeynmanDiagram(V, [("q", "a", "antifermion")])
    assert np.allclose(anti.lines[0][0].get_start(), [*V["q"], 0])  # still drawn q -> a
    assert anti.lines[0][1].get_vertices()[0][0] < d.lines[0][1].get_vertices()[0][0]


def test_topology_and_dots_on_internal_vertices():
    d = _drell_yan()
    assert len(d.lines) == 5 and len(d.labels) == 5
    assert len(d.dots) == 2  # a and b are internal
    for (start, end, _), line in zip(d.edge_list, d.lines, strict=True):
        s, e = _ends(line)
        assert np.allclose(s, [*V[start], 0], atol=1e-6)
        assert np.allclose(e, [*V[end], 0], atol=1e-6)
    assert d.edge("b", "a") is d.lines[2]
    assert all(isinstance(dot, Dot) for dot in d.dots)


def test_scalar_is_dashed():
    d = FeynmanDiagram({"a": (0, 0), "b": (2, 0)}, [("a", "b", "scalar")])
    assert isinstance(d.lines[0], DashedLine)


def test_errors_are_explained():
    with pytest.raises(KeyError, match="unknown vertex 'x'"):
        FeynmanDiagram(V, [("q", "x", "fermion")])
    with pytest.raises(ValueError, match="use one of: " + ", ".join(EDGE_KINDS)):
        FeynmanDiagram(V, [("q", "a", "graviton")])
    with pytest.raises(ValueError, match="start, end, kind"):
        FeynmanDiagram(V, [("q", "a")])
    with pytest.raises(KeyError, match="no edge"):
        _drell_yan().edge("q", "l+")


def test_labels_sit_outside_the_diagram():
    d = _drell_yan()
    centre = np.mean([[*p, 0] for p in V.values()], axis=0)
    for (start, end, _), lab in zip(d.edge_list, d.edge_labels, strict=True):
        mid = (np.array([*V[start], 0]) + np.array([*V[end], 0])) / 2
        if np.linalg.norm(mid - centre) > 1e-6:
            assert np.linalg.norm(lab.get_center() - centre) > np.linalg.norm(mid - centre)
    assert d.edge_labels[2].get_center()[1] > 0  # the propagator label goes above it


def test_draw_in_order_keeps_the_diagram_one_group():
    d = _drell_yan()
    anim = d.draw_in_order(time_per_edge=0.5)
    assert anim.mobject is d
    assert len(anim.animations) == 5
    scene = Scene()
    scene.add(d)
    anim.begin()
    anim.interpolate(1.0)
    anim.finish()
    check_order(scene, [d])


@pytest.mark.latex
def test_string_labels_use_mathtex():
    d = FeynmanDiagram(V, [("q", "a", "fermion", r"q"), ("a", "b", "photon", r"\gamma^*/Z")])
    assert len(d.labels) == 2
