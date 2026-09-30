from __future__ import annotations

import math

import numpy as np
import pytest
from manim import DashedVMobject

from manim_hep.detector import DEFAULT_RADII, SIGNATURE_KINDS, BarrelSlice, signature, track
from manim_hep.style import intrusions, use_theme


@pytest.fixture(autouse=True)
def _theme():
    use_theme("generic")


@pytest.fixture(scope="module")
def det():
    use_theme("generic")
    return BarrelSlice()


def test_layers_are_inside_out(det):
    assert list(det.layers) == ["beam_pipe", "tracker", "solenoid", "ecal", "hcal", "muon"]
    assert det.radius("muon") == pytest.approx(DEFAULT_RADII["muon"])


def test_partial_override_and_validation():
    s = BarrelSlice({"solenoid": (2.36, 2.42)})
    assert list(s.layers) == ["beam_pipe", "tracker", "ecal", "hcal", "solenoid", "muon"]
    with pytest.raises(ValueError, match="overlap"):
        BarrelSlice({"ecal": (0.9, 1.5)})
    with pytest.raises(ValueError, match="inner < outer"):
        BarrelSlice({"hcal": (2.0, 1.9)})
    with pytest.raises(ValueError, match="unknown layer"):
        BarrelSlice({"toroid": (3.1, 3.5)})


def test_geometry_follows_moves_and_scaling():
    s = BarrelSlice().scale(0.5).move_to([2, -1, 0])
    assert np.allclose(s.ip, [2, -1, 0])
    assert s.radius("muon")[1] == pytest.approx(1.5)
    assert np.allclose(s.point_at(1.0, 0.0), [3, -1, 0])


def test_default_slice_needs_moving_below_the_title_band(det):
    assert "title band" in intrusions(det)
    theme = use_theme("generic")
    moved = BarrelSlice().scale(0.95).move_to(theme.content_center)
    assert intrusions(moved) == []


@pytest.mark.parametrize(("charge", "field", "sign"), [(1, 3.8, -1), (-1, 3.8, 1), (1, -3.8, 1)])
def test_curvature_sign(charge, field, sign):
    t = track(1.0, charge, field, phi=0.0, r_max=1.0)
    assert math.copysign(1, t.get_end()[1]) == sign


def test_radius_follows_pt_and_track_stops_at_r_max():
    soft = track(1.0, 1, 3.8, r_max=1.0)
    hard = track(10.0, 1, 3.8, r_max=1.0)
    assert abs(soft.get_end()[1]) > 5 * abs(hard.get_end()[1])
    assert np.linalg.norm(soft.get_end()) == pytest.approx(1.0, abs=1e-6)


def test_neutral_and_no_field_are_straight():
    for t in (track(1.0, 0, 3.8, phi=0.5), track(1.0, 1, 0.0, phi=0.5)):
        assert t.get_end() == pytest.approx([math.cos(0.5), math.sin(0.5), 0.0])


def test_curler_stops_after_one_turn():
    t = track(0.1, 1, 3.8, r_max=1.0)  # R = 8.8 cm, never reaches r = 1
    assert np.linalg.norm(t.get_end()) < 0.01
    with pytest.raises(ValueError, match="positive"):
        track(0.0, 1, 3.8)


def _r(det, point):
    return float(np.linalg.norm(point - det.ip))


def test_signatures(det):
    ecal_in = det.radius("ecal")[0]
    e = signature("electron", det, phi=0.3)
    assert len(e.tracks) == 1 and len(e.deposits) == 1
    assert _r(det, e.tracks[0].get_end()) == pytest.approx(ecal_in, abs=1e-6)

    mu = signature("muon", det, phi=1.0, charge=1)
    assert _r(det, mu.tracks[0].get_end()) == pytest.approx(det.radius("muon")[1], abs=1e-3)
    assert len(mu.hits) == 3

    g = signature("photon", det, phi=2.0)
    assert isinstance(g.tracks[0], DashedVMobject) and len(g.deposits) == 1

    nu = signature("neutrino", det, phi=-1.0)
    assert max(_r(det, p) for p in nu.get_all_points()) > det.radius("muon")[1]

    jet = signature("jet", det, phi=-2.0)
    assert len(jet.tracks) >= 3 and len(jet.deposits) == 2

    assert len(signature("tau1", det).tracks) == 1
    assert len(signature("tau3", det).tracks) == 3


def test_signature_errors(det):
    with pytest.raises(ValueError, match="use one of: " + ", ".join(SIGNATURE_KINDS)):
        signature("graviton", det)
    with pytest.raises(ValueError, match=r"\+1 or -1"):
        signature("muon", det, charge=2)


def test_signature_markers_scale_with_the_detector():
    small = BarrelSlice().scale(0.5)
    big = BarrelSlice()
    hit_small = signature("muon", small, phi=1.0).hits[0]
    hit_big = signature("muon", big, phi=1.0).hits[0]
    assert hit_small.width == pytest.approx(hit_big.width / 2, rel=1e-3)


def _net_charge(sig, field_sign=1):
    """Charge from each track's bending: with B out of the screen, + bends clockwise."""
    total = 0
    for trk in sig.tracks:
        pts = trk.get_anchors()
        d, e = pts[1] - pts[0], pts[-1] - pts[0]
        turn = d[0] * e[1] - d[1] * e[0]  # > 0: anticlockwise
        total += -field_sign * int(np.sign(turn))
    return total


@pytest.mark.parametrize("charge", [-1, 1])
def test_tau_prongs_add_up_to_the_tau_charge(det, charge):
    assert _net_charge(signature("tau3", det, phi=0.4, charge=charge)) == charge
    assert _net_charge(signature("tau1", det, phi=0.4, charge=charge)) == charge
