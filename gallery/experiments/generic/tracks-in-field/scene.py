"""Tracks in a magnetic field: the sign of the bending gives the charge, the
radius gives the transverse momentum.

Physics: in a uniform field B along the beam, a particle of charge q and
transverse momentum pT moves on a circle of radius R = pT / (0.3 |q| B)
(R in m, pT in GeV, B in T). With B pointing out of the screen (⊙), the force
q v × B turns positive charges clockwise and negative charges anticlockwise.
Values: B = 3.8 T and a field region of radius 1.1 m (typical of a large
solenoid; schematic); pT = 1 GeV gives R = 0.88 m, pT = 20 GeV gives R = 17.6 m.
"""

from __future__ import annotations

import math

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
    Circle,
    Create,
    Dot,
    FadeIn,
    MathTex,
    Scene,
    VGroup,
    linear,
)

from manim_hep import check_order, track, use_theme
from manim_hep.palette import tint

theme = use_theme()
C = theme.palette

FIELD_T = 3.8  # tesla, out of the screen
REGION_M = 1.1  # radius of the field region in metres
REGION = 2.4  # the same radius in scene units
SCALE = REGION / REGION_M  # scene units per metre
LOW_PT, HIGH_PT = 1.0, 20.0  # GeV

A = {
    "ip": np.array([-2.4, -0.65, 0.0]),
    "field_value": np.array([3.6, 1.9, 0.0]),
    "formula": np.array([3.6, -0.1, 0.0]),
}


def radius_m(pt: float) -> float:
    """Radius of curvature in metres for a unit charge in FIELD_T."""
    return pt / (0.299792458 * FIELD_T)


def out_of_screen(point, colour, size: float = 0.1) -> VGroup:
    """The ⊙ symbol: a field line pointing out of the screen."""
    return VGroup(
        Circle(radius=size, color=colour, stroke_width=2).move_to(point),
        Dot(point, radius=size * 0.3, color=colour),
    )


def _outside(tex: str, colour, direction: np.ndarray, buff: float = 0.35) -> MathTex:
    """A label just outside the field region, along ``direction`` from the IP."""
    u = direction / np.linalg.norm(direction)
    return MathTex(tex, font_size=36, color=colour).move_to(A["ip"] + u * (REGION + buff))


def state_field() -> dict:
    ip = A["ip"]
    disc = Circle(radius=REGION, color=C.detector, stroke_width=2.5)
    disc.set_fill(tint(C.detector, 0.88), opacity=1.0).move_to(ip)
    grid = VGroup(
        *(
            out_of_screen(ip + np.array([x, y, 0.0]), tint(C.muted, 0.35))
            for x in np.arange(-2.0, 2.01, 0.8)
            for y in np.arange(-2.0, 2.01, 0.8)
            if 0.6 < math.hypot(x, y) < REGION - 0.3
        )
    )
    value = MathTex(rf"B = {FIELD_T:g}\ \mathrm{{T}}", font_size=36)
    field = VGroup(out_of_screen(np.zeros(3), C.ink, size=0.16), value)
    field.arrange(RIGHT, buff=0.25).move_to(A["field_value"])
    return {
        "region": VGroup(disc, grid),
        "field": field,
        "vertex": Dot(ip, radius=0.06, color=C.ink),
    }


def _pair() -> VGroup:
    """Two tracks of equal pT and opposite charge, launched straight up."""
    kw = {"origin": A["ip"], "r_max": REGION, "scale": SCALE, "phi": math.pi / 2}
    plus = track(LOW_PT, +1, FIELD_T, color=C.highlight, **kw)
    minus = track(LOW_PT, -1, FIELD_T, color=C.theory, **kw)
    labels = VGroup(
        _outside(r"\mu^+", C.highlight, plus.get_end() - A["ip"]),
        _outside(r"\mu^-", C.theory, minus.get_end() - A["ip"]),
        MathTex(rf"p_T = {LOW_PT:g}\ \mathrm{{GeV}}", font_size=34).move_to(
            A["ip"] + UP * (REGION + 0.4)
        ),
    )
    group = VGroup(VGroup(plus, minus), labels)
    group.tracks, group.labels = group[0], group[1]
    return group


def _stiff() -> VGroup:
    """A high-pT positive track, launched straight down: it barely bends."""
    stiff = track(
        HIGH_PT, +1, FIELD_T, phi=-math.pi / 2, origin=A["ip"], r_max=REGION, scale=SCALE,
        color=C.highlight,
    )  # fmt: skip
    label = (
        MathTex(rf"\mu^+,\ p_T = {HIGH_PT:g}\ \mathrm{{GeV}}", font_size=34, color=C.highlight)
        .next_to(stiff.get_end(), RIGHT, buff=0.3)
        .shift(0.22 * DOWN)
    )
    group = VGroup(VGroup(stiff), VGroup(label))  # animated parts must be real submobjects
    group.tracks, group.labels = group[0], group[1]
    return group


def _formula() -> VGroup:
    arrow = r"\;\rightarrow\;"
    lines = VGroup(
        MathTex(r"R = \frac{p_T}{0.3\,|q|\,B}", font_size=46),
        MathTex(r"[R] = \mathrm{m},\ [p_T] = \mathrm{GeV},\ [B] = \mathrm{T}", font_size=26),
        MathTex(
            rf"p_T = {LOW_PT:g}\ \mathrm{{GeV}}{arrow}R = {radius_m(LOW_PT):.2f}\ \mathrm{{m}}",
            font_size=32,
        ),
        MathTex(
            rf"p_T = {HIGH_PT:g}\ \mathrm{{GeV}}{arrow}R = {radius_m(HIGH_PT):.1f}\ \mathrm{{m}}",
            font_size=32,
        ),
    ).arrange(-UP, buff=0.3)
    return lines.move_to(A["formula"])


def state_tracks() -> dict:
    """The clip's last frame. Dict order = drawing order."""
    state = state_field()
    state["pair"] = _pair()
    state["stiff"] = _stiff()
    state["formula"] = _formula()
    return state


def reveal(group: VGroup, track_time: float) -> AnimationGroup:
    """Draw the tracks together at constant speed, then their labels (one mobject)."""
    return AnimationGroup(
        Create(group.tracks, run_time=track_time, rate_func=linear, lag_ratio=0),
        FadeIn(group.labels, run_time=0.5),
        lag_ratio=1.0,
        group=group,
    )


class TracksInField(Scene):
    def construct(self):
        state = state_tracks()
        self.play(
            FadeIn(state["region"]), FadeIn(state["field"]), FadeIn(state["vertex"]), run_time=1.0
        )
        self.play(reveal(state["pair"], 2.0))
        self.play(reveal(state["stiff"], 1.5))
        self.play(FadeIn(state["formula"], shift=0.2 * UP), run_time=1.0)
        check_order(self, state)
        self.wait(0.1)
