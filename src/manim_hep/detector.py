"""A neutral detector cross-section, tracks and particle signatures.

``BarrelSlice`` is a generic transverse (r-φ) view of a collider detector. It
is not any experiment's geometry and is not derived from any logo.

    det = BarrelSlice()
    self.play(LaggedStart(*(FadeIn(layer) for layer in det.layers.values()), lag_ratio=0.3))
    mu = signature("muon", det, phi=0.6, charge=+1)
    self.play(Create(mu.tracks[0], rate_func=linear, run_time=2))

Tracks bend with the correct sign: with the field pointing out of the screen
(``field > 0``), positive particles curve clockwise.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Mapping, Sequence

import numpy as np
from manim import (
    ORIGIN,
    AnnularSector,
    Annulus,
    Circle,
    DashedVMobject,
    Line,
    Polygon,
    Rectangle,
    VGroup,
    VMobject,
)

from manim_hep.palette import tint
from manim_hep.style import current_theme

__all__ = ["DEFAULT_RADII", "SIGNATURE_KINDS", "BarrelSlice", "signature", "track"]

#: Inner and outer radius of each layer, in scene units, inside out.
DEFAULT_RADII: dict[str, tuple[float, float]] = {
    "beam_pipe": (0.0, 0.12),
    "tracker": (0.2, 1.0),
    "solenoid": (1.05, 1.12),
    "ecal": (1.2, 1.65),
    "hcal": (1.75, 2.35),
    "muon": (2.5, 3.0),
}

SIGNATURE_KINDS = ("electron", "muon", "photon", "jet", "tau1", "tau3", "neutrino")

_C = 0.299792458  # GeV / (T m) per unit charge: pT = 0.3 q B R


def _p(point: Sequence[float]) -> np.ndarray:
    arr = np.asarray(point, dtype=float)
    return np.append(arr, 0.0) if arr.shape == (2,) else arr


class BarrelSlice(VGroup):
    """A generic barrel detector seen along the beam, built from concentric layers.

    Parameters
    ----------
    radii
        ``{layer: (inner, outer)}`` overriding any of :data:`DEFAULT_RADII`
        (beam_pipe, tracker, solenoid, ecal, hcal, muon). Layers may not overlap.
    center
        Where the beam line (the interaction point) sits.

    Attributes: ``layers`` (name → mobject, inside out, which is also a good build
    order) and ``outline`` (an invisible circle at the outer radius). Use
    ``radius(name)`` and ``point_at(r, phi)`` for positions; both follow the slice
    when it is moved or scaled.
    """

    def __init__(
        self,
        radii: Mapping[str, tuple[float, float]] | None = None,
        *,
        center: Sequence[float] = ORIGIN,
        tracker_layers: int = 5,
        ecal_cells: int = 72,
        hcal_cells: int = 36,
        muon_stations: int = 3,
        **kwargs,
    ):
        super().__init__(**kwargs)
        merged = dict(DEFAULT_RADII)
        for name, value in (radii or {}).items():
            if name not in DEFAULT_RADII:
                raise ValueError(f"unknown layer {name!r}; layers are: {', '.join(DEFAULT_RADII)}")
            merged[name] = (float(value[0]), float(value[1]))
        ordered = sorted(merged.items(), key=lambda item: item[1][0])
        for name, (inner, outer) in ordered:
            if not 0 <= inner < outer:
                raise ValueError(f"{name}: need 0 <= inner < outer, got ({inner}, {outer})")
        for (a, (_, a_out)), (b, (b_in, _)) in itertools.pairwise(ordered):
            if b_in < a_out:
                raise ValueError(f"layers {a} and {b} overlap ({a_out} > {b_in})")
        self._natural = dict(ordered)
        self._outer = max(outer for _, outer in merged.values())

        palette = current_theme().palette
        c = _p(center)
        background = palette.background
        self.layers: dict[str, VMobject] = {}
        for name, (inner, outer) in ordered:
            if name == "beam_pipe":
                layer = VGroup(Circle(radius=outer, color=palette.ink, stroke_width=2).move_to(c))
            elif name == "tracker":
                layer = VGroup(
                    *(
                        Circle(radius=r, color=palette.detector, stroke_width=1.6).move_to(c)
                        for r in np.linspace(inner, outer, tracker_layers)
                    )
                )
            elif name == "muon":
                thickness = (outer - inner) / (2 * muon_stations - 1)
                layer = VGroup(
                    *(
                        Annulus(
                            inner_radius=inner + 2 * k * thickness,
                            outer_radius=inner + (2 * k + 1) * thickness,
                            fill_color=tint(palette.muted, 0.45),
                            fill_opacity=1.0,
                            stroke_width=0,
                        ).move_to(c)
                        for k in range(muon_stations)
                    )
                )
            else:
                fill = {
                    "solenoid": tint(palette.muted, 0.3),
                    "ecal": tint(palette.detector, 0.55),
                    "hcal": tint(palette.detector, 0.78),
                }[name]
                ring = Annulus(
                    inner_radius=inner,
                    outer_radius=outer,
                    fill_color=fill,
                    fill_opacity=1.0,
                    stroke_width=0,
                ).move_to(c)
                layer = VGroup(ring)
                cells = {"ecal": ecal_cells, "hcal": hcal_cells}.get(name, 0)
                if cells:
                    layer.add(
                        VGroup(
                            *(
                                Line(
                                    c + inner * np.array([math.cos(a), math.sin(a), 0]),
                                    c + outer * np.array([math.cos(a), math.sin(a), 0]),
                                    color=background,
                                    stroke_width=1.2,
                                )
                                for a in np.linspace(0, 2 * math.pi, cells, endpoint=False)
                            )
                        )
                    )
            self.layers[name] = layer
            self.add(layer)
        self.outline = Circle(radius=self._outer, stroke_opacity=0.0, stroke_width=0).move_to(c)
        self.add(self.outline)

    @property
    def scale_factor(self) -> float:
        """Scene units per unit of the ``radii`` it was built with."""
        return self.outline.width / (2 * self._outer)

    @property
    def ip(self) -> np.ndarray:
        """The interaction point (the centre) in scene coordinates."""
        return self.outline.get_center()

    def radius(self, name: str) -> tuple[float, float]:
        """(inner, outer) radius of a layer, in current scene units."""
        if name not in self._natural:
            raise KeyError(f"no layer {name!r}")
        inner, outer = self._natural[name]
        return inner * self.scale_factor, outer * self.scale_factor

    def point_at(self, r: float, phi: float) -> np.ndarray:
        """The scene point at radius ``r`` (scene units) and angle ``phi`` from the centre."""
        return self.ip + r * np.array([math.cos(phi), math.sin(phi), 0.0])


def _arc_points(
    pt: float, charge: float, field: float, phi: float, r_max: float, origin, scale: float, n: int
) -> list[np.ndarray]:
    o = _p(origin)
    direction = np.array([math.cos(phi), math.sin(phi), 0.0])
    if charge == 0 or field == 0:
        return [o, o + direction * r_max]
    radius = pt / (_C * abs(charge) * abs(field)) * scale
    sense = math.copysign(1.0, charge * field)  # +1: clockwise
    right = np.array([math.sin(phi), -math.cos(phi), 0.0])
    centre = o + sense * radius * right
    start = math.atan2(o[1] - centre[1], o[0] - centre[0])
    turn = 2 * math.asin(r_max / (2 * radius)) if r_max < 2 * radius else 2 * math.pi * 0.999
    angles = start - sense * np.linspace(0.0, turn, n)
    return [centre + radius * np.array([math.cos(a), math.sin(a), 0.0]) for a in angles]


def track(
    pt: float,
    charge: float,
    field: float,
    *,
    phi: float = 0.0,
    r_max: float = 1.0,
    origin: Sequence[float] = ORIGIN,
    scale: float = 1.0,
    color=None,
    stroke_width: float = 3.5,
    samples: int = 120,
) -> VMobject:
    """A charged-particle track in a solenoid field, from ``origin`` out to ``r_max``.

    ``pt`` in GeV, ``charge`` in units of e, ``field`` in tesla (positive: out of
    the screen), ``scale`` in scene units per metre. The radius of curvature is
    R = pT / (0.3 |q| B); positive charges bend clockwise when ``field > 0``. A
    neutral particle (or no field) gives a straight line. The track stops at
    distance ``r_max`` from ``origin``, or after one turn if it curls up first.
    """
    if pt <= 0:
        raise ValueError("pt must be positive")
    points = _arc_points(pt, charge, field, phi, r_max, origin, scale, samples)
    line = VMobject(color=color or current_theme().palette.ink, stroke_width=stroke_width)
    line.set_points_as_corners(points)
    return line


def _extend_straight(points: list[np.ndarray], centre: np.ndarray, r_out: float, n: int = 30):
    """Continue a track along its final direction until it reaches radius ``r_out``."""
    end, before = points[-1], points[-2]
    direction = (end - before) / np.linalg.norm(end - before)
    rel = end - centre
    b = float(np.dot(rel, direction))
    c = float(np.dot(rel, rel)) - r_out**2
    t = -b + math.sqrt(max(b * b - c, 0.0))
    return [end + direction * s for s in np.linspace(0, t, n)[1:]]


def _deposit(det: BarrelSlice, layer: str, phi: float, width: float, depth: float, color):
    inner, outer = det.radius(layer)
    return AnnularSector(
        inner_radius=inner,
        outer_radius=inner + (outer - inner) * depth,
        angle=width,
        start_angle=phi - width / 2,
        arc_center=det.ip,
        fill_color=color,
        fill_opacity=0.9,
        stroke_width=0,
    )


def _dashed(points, color, stroke_width=3.0):
    path = VMobject(color=color, stroke_width=stroke_width)
    path.set_points_as_corners(points)
    return DashedVMobject(path, num_dashes=max(8, int(np.linalg.norm(points[-1] - points[0]) * 7)))


def signature(
    kind: str,
    detector: BarrelSlice,
    *,
    phi: float = 0.0,
    charge: int = -1,
    pt: float | None = None,
    field: float = 3.8,
    seed: int = 0,
) -> VGroup:
    """How a particle ``kind`` shows up in ``detector``, drawn at angle ``phi``.

    Kinds: electron (track, then an ECAL shower), muon (track through everything,
    hits in the muon stations), photon (no track, an ECAL shower), jet (several
    tracks, ECAL and HCAL deposits), tau1 and tau3 (a narrow jet with one or three
    tracks), neutrino (escapes unseen: a dashed line out of the detector).

    The tracker radius stands for about 1.1 m; ``pt`` (GeV) sets the curvature.
    The result has ``tracks``, ``deposits`` and ``hits`` (``VGroup``s) and ``kind``.
    """
    if kind not in SIGNATURE_KINDS:
        raise ValueError(f"unknown kind {kind!r}; use one of: {', '.join(SIGNATURE_KINDS)}")
    if kind not in ("photon", "neutrino") and charge not in (-1, 1):
        raise ValueError("charge must be +1 or -1")
    palette = current_theme().palette
    cycle = palette.cycle
    color = {
        "electron": cycle[1 % len(cycle)],
        "muon": cycle[0],
        "photon": cycle[2 % len(cycle)],
        "jet": cycle[3 % len(cycle)],
        "tau1": cycle[4 % len(cycle)],
        "tau3": cycle[4 % len(cycle)],
        "neutrino": palette.muted,
    }[kind]
    tracker_out = detector.radius("tracker")[1]
    scale = tracker_out / 1.1  # scene units per metre
    ip = detector.ip
    tracks, deposits, hits = VGroup(), VGroup(), VGroup()
    ecal_in = detector.radius("ecal")[0]

    def charged(pt_: float, q: int, angle: float, r_max: float) -> list[np.ndarray]:
        return _arc_points(pt_, q, field, angle, r_max, ip, scale, 120)

    def polyline(points) -> VMobject:
        line = VMobject(color=color, stroke_width=3.5)
        line.set_points_as_corners(points)
        return line

    if kind == "electron":
        points = charged(pt or 3.0, charge, phi, ecal_in)
        tracks.add(polyline(points))
        exit_phi = math.atan2(points[-1][1] - ip[1], points[-1][0] - ip[0])
        deposits.add(_deposit(detector, "ecal", exit_phi, 0.12, 0.75, color))
    elif kind == "photon":
        end = detector.point_at(ecal_in, phi)
        tracks.add(_dashed([ip, end], color))
        deposits.add(_deposit(detector, "ecal", phi, 0.12, 0.75, color))
    elif kind == "muon":
        sol_out = detector.radius("solenoid")[1]
        points = charged(pt or 3.0, charge, phi, sol_out)
        muon_out = detector.radius("muon")[1]
        points += _extend_straight(points, ip, muon_out)
        tracks.add(polyline(points))
        for station in detector.layers["muon"]:
            r = (station.inner_radius + station.outer_radius) / 2 * detector.scale_factor
            hit = min(points, key=lambda p: abs(np.linalg.norm(p - ip) - r))
            size = 0.1 * detector.scale_factor
            box = Rectangle(
                width=size, height=size, fill_color=color, fill_opacity=1, stroke_width=0
            )
            hits.add(box.move_to(hit).rotate(math.atan2(hit[1] - ip[1], hit[0] - ip[0])))
    elif kind == "neutrino":
        _, muon_out = detector.radius("muon")
        end = detector.point_at(muon_out * 1.12, phi)
        direction = (end - ip) / np.linalg.norm(end - ip)
        normal = np.array([-direction[1], direction[0], 0.0])
        tip = 0.2 * detector.scale_factor
        tracks.add(_dashed([ip, end - direction * tip * 0.9], color))
        tip = Polygon(
            end,
            end - direction * tip + normal * tip * 0.4,
            end - direction * tip - normal * tip * 0.4,
            fill_color=color,
            fill_opacity=1.0,
            stroke_width=0,
        )
        tracks.add(tip)
    else:  # jet, tau1, tau3
        rng = np.random.default_rng(seed)
        n, spread, width = {
            "jet": (4, 0.16, 0.34),
            "tau1": (1, 0.0, 0.14),
            "tau3": (3, 0.05, 0.16),
        }[kind]
        for i in range(n):
            q = charge if n == 1 else (1 if i % 2 == 0 else -1)
            angle = phi + (rng.uniform(-spread, spread) if spread else 0.0)
            tracks.add(polyline(charged(pt or float(rng.uniform(1.5, 5.0)), q, angle, ecal_in)))
        deposits.add(_deposit(detector, "ecal", phi, width * 0.6, 0.5, color))
        deposits.add(_deposit(detector, "hcal", phi, width, 0.8, color))

    group = VGroup(deposits, hits, tracks)
    group.tracks, group.deposits, group.hits, group.kind = tracks, deposits, hits, kind
    return group
