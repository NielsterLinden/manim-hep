"""Detector signatures: a generic barrel detector is built inside out, then an
electron, a muon, a photon, a jet and a neutrino each leave their signature.

Physics honesty: the detector is a neutral cartoon (no experiment's geometry).
The layer order beam pipe → tracker → solenoid → ECAL → HCAL → muon system is one
common choice; ATLAS puts its solenoid inside the calorimeters, CMS puts it
outside the HCAL. Track curvatures are computed for B = 3.8 T but with pT of a
few GeV, far below typical W/Z decay leptons, so the bending is visible.
"""

from __future__ import annotations

import math

from manim import AnimationGroup, Create, FadeIn, MathTex, Scene, VGroup, linear

from manim_hep import BarrelSlice, add_state, check_order, place, signature, use_theme

theme = use_theme()
C = theme.palette

A = {"detector": (0.85, tuple(theme.content_center[:2]))}

# kind, angle (rad), charge, symbol, time to draw the track (s)
PARTICLES = [
    ("electron", 0.35, -1, r"e^-", 1.6),
    ("muon", 1.95, +1, r"\mu^+", 1.8),
    ("photon", 2.95, 0, r"\gamma", 1.2),
    ("jet", -0.60, +1, r"\mathrm{jet}", 1.6),
    ("neutrino", -2.20, 0, r"\nu", 1.6),
]


def state_detector() -> dict:
    """Clip 1's last frame: the complete detector."""
    detector = BarrelSlice()
    place(detector, A["detector"])
    return {"detector": detector}


def _particle(detector: BarrelSlice, kind: str, phi: float, charge: int, symbol: str) -> VGroup:
    sig = signature(kind, detector, phi=phi, charge=charge)
    colour = sig.tracks[0].get_color()
    if kind in ("electron", "muon"):  # label where the curved track actually ends
        end = sig.tracks[0].get_end() - detector.ip
        phi = math.atan2(end[1], end[0])
    radius = detector.radius("muon")[1] + (0.65 if kind == "neutrino" else 0.35)
    label = MathTex(symbol, font_size=38, color=colour).move_to(detector.point_at(radius, phi))
    group = VGroup(sig, label)
    group.sig, group.label = sig, label
    return group


def state_signatures() -> dict:
    """Clip 2's last frame: the detector plus one group (signature and symbol) per particle."""
    state = state_detector()
    for kind, phi, charge, symbol, _ in PARTICLES:
        state[kind] = _particle(state["detector"], kind, phi, charge, symbol)
    return state


def build_detector(detector: BarrelSlice) -> AnimationGroup:
    """Reveal the layers one after the other, inside out; the detector stays one mobject."""
    steps = []
    for name, layer in detector.layers.items():
        if name in ("beam_pipe", "tracker"):
            steps.append(Create(layer, run_time=0.5 if name == "beam_pipe" else 1.0))
        else:
            steps.append(FadeIn(layer, run_time=0.75))
    return AnimationGroup(*steps, lag_ratio=1.0, group=detector)


def reveal(particle: VGroup, track_time: float) -> AnimationGroup:
    """Draw the track at constant speed, then the energy deposits, hits and symbol."""
    sig = particle.sig
    after = [FadeIn(part, run_time=0.4) for part in (sig.deposits, sig.hits) if len(part)]
    after.append(FadeIn(particle.label, run_time=0.4))
    return AnimationGroup(
        Create(sig.tracks, run_time=track_time, rate_func=linear),
        AnimationGroup(*after),
        lag_ratio=1.0,
        group=particle,
    )


class DetectorBuild(Scene):
    def construct(self):
        state = state_detector()
        self.play(build_detector(state["detector"]))
        check_order(self, state)
        self.wait(0.1)


class DetectorSignatures(Scene):
    """Opens on DetectorBuild's last frame."""

    def construct(self):
        state = state_signatures()
        add_state(self, {"detector": state["detector"]})
        for kind, _, _, _, track_time in PARTICLES:
            self.play(reveal(state[kind], track_time))
        check_order(self, state)
        self.wait(0.1)
