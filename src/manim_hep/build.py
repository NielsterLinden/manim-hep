"""Helpers for building scenes state-first.

The pattern that makes chained clips seamless:

1. A **builder** returns the final state of a clip as a dict of mobjects, with no
   animation. The dict order is the drawing order (later entries on top).
2. The next clip opens on that exact frame with ``add_state(self, build_previous)``.
3. A clip animates its own state into view and ends with ``check_order`` to prove
   the scene holds exactly that state, in that order, before ``self.wait(0.1)``.

Positions live in one module-level anchor dict and are applied with ``place``.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

import numpy as np
from manim import ORIGIN, Mobject, Scene, ValueTracker

__all__ = ["add_state", "check_order", "place"]

State = Mapping[str, Mobject]


def add_state(scene: Scene, builder: State | Callable[[], State]) -> State:
    """Add a clip's state to ``scene`` without animation and return it.

    ``builder`` is the state dict or a function returning it; values are added
    in dict order, which is the drawing order.
    """
    state = builder() if callable(builder) else builder
    if not isinstance(state, Mapping):
        raise TypeError("a builder must return a dict of mobjects (name -> mobject)")
    scene.add(*state.values())
    return state


def _is_placeholder(mob: Mobject) -> bool:
    """Empty mobjects left behind by ``wait()`` and some finished animations."""
    return len(mob.get_family()) == 1 and not mob.has_points()


def check_order(scene: Scene, expected: State | Sequence[Mobject]) -> None:
    """Assert that ``scene`` shows exactly ``expected``, in that drawing order.

    Both sides are compared in drawing order: add order, re-sorted by ``z_index``.
    Wait placeholders and ``ValueTracker``s are ignored. On a mismatch this raises
    ``AssertionError`` naming what was found, so Manim stops before writing a
    misleading clip.
    """
    names: dict[int, str] = {}
    if isinstance(expected, Mapping):
        names = {id(m): k for k, m in expected.items()}
        want = list(expected.values())
    else:
        want = list(expected)

    def drawable(m: Mobject) -> bool:
        return not _is_placeholder(m) and not isinstance(m, ValueTracker)

    live = [m for m in scene.mobjects if drawable(m)]
    want = [m for m in want if drawable(m)]
    # Manim draws in add order, stably re-sorted by z_index; compare both sides that way.
    live.sort(key=lambda m: m.z_index)
    want.sort(key=lambda m: m.z_index)
    if len(live) == len(want) and all(a is b for a, b in zip(live, want, strict=True)):
        return

    def describe(mobs: list[Mobject]) -> list[str]:
        return [names.get(id(m), f"<{type(m).__name__}>") for m in mobs]

    raise AssertionError(f"scene draws {describe(live)}, expected {describe(want)}")


def place(
    mobject: Mobject,
    placement: Sequence[float] | tuple[float, Sequence[float]],
    natural_center: Sequence[float] = ORIGIN,
) -> Mobject:
    """Put ``mobject`` where an anchor says, and return it.

    ``placement`` is a point ``(x, y)``/``(x, y, z)``, which moves the mobject's
    centre there, or a pair ``(scale, (x, y))``, which scales about
    ``natural_center`` and then moves that point to ``(x, y)``. Keep the anchors
    in one module-level dict so every clip places things identically::

        A = {"detector": (0.42, (-4.6, -0.7)), "plot": (1.85, -0.25)}
        place(BarrelSlice(), A["detector"])
    """
    if len(placement) == 2 and np.ndim(placement[1]) == 1:
        scale, center = placement
        about = _point(natural_center)
        mobject.scale(float(scale), about_point=about)
        mobject.shift(_point(center) - about)
        return mobject
    mobject.move_to(_point(placement))
    return mobject


def _point(p: Sequence[float]) -> np.ndarray:
    arr = np.asarray(p, dtype=float)
    if arr.shape == (2,):
        arr = np.append(arr, 0.0)
    if arr.shape != (3,):
        raise ValueError(f"expected a 2D or 3D point, got {p!r}")
    return arr
