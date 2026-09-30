"""Colours for HEP animations. This module never imports Manim.

matplotlib scripts that make the static figures of a talk can import it too, so
slides and animations share the same hex values::

    from manim_hep.palette import DEFAULT, tint
    plt.plot(x, y, color=DEFAULT.theory)

Colours are ``"#RRGGBB"`` strings, which Manim accepts wherever it takes a colour.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

__all__ = ["DEFAULT", "OKABE_ITO", "Palette", "mix", "shade", "tint", "to_hex", "to_rgb"]

_HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

#: The Okabe–Ito colour-vision-deficiency-safe palette (Okabe and Ito, 2002), black first.
OKABE_ITO: tuple[str, ...] = (
    "#000000",  # black
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
)


def to_rgb(color: str) -> tuple[float, float, float]:
    """Parse ``"#RGB"`` or ``"#RRGGBB"`` (any case) into floats in [0, 1]."""
    if not isinstance(color, str) or not _HEX.match(color):
        raise ValueError(f"expected a colour like '#1A2B3C', got {color!r}")
    digits = color[1:]
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    return tuple(int(digits[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def to_hex(rgb: Sequence[float]) -> str:
    """Format floats in [0, 1] as ``"#RRGGBB"`` (values are clipped to the range)."""
    if len(rgb) != 3:
        raise ValueError(f"expected three channels, got {len(rgb)}")
    return "#" + "".join(f"{round(min(max(float(c), 0.0), 1.0) * 255):02X}" for c in rgb)


def _check_fraction(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1, got {value}")


def mix(a: str, b: str, t: float) -> str:
    """Blend two colours in sRGB: ``t=0`` gives ``a`` and ``t=1`` gives ``b``."""
    _check_fraction("t", t)
    ra, rb = to_rgb(a), to_rgb(b)
    return to_hex([x + (y - x) * t for x, y in zip(ra, rb, strict=True)])


def tint(color: str, amount: float) -> str:
    """Move ``color`` toward white by ``amount`` (0 keeps it, 1 gives white)."""
    _check_fraction("amount", amount)
    return mix(color, "#FFFFFF", amount)


def shade(color: str, amount: float) -> str:
    """Move ``color`` toward black by ``amount`` (0 keeps it, 1 gives black)."""
    _check_fraction("amount", amount)
    return mix(color, "#000000", amount)


@dataclass(frozen=True)
class Palette:
    """Colour roles for one theme.

    Scenes take colours from roles, never from literals, so a whole talk can be
    restyled in one place. ``cycle`` is the categorical sequence for things that
    only need to be told apart (processes in a stack, several tracks).
    """

    name: str
    background: str
    ink: str  # text, axes, outlines; a dark slate rather than pure black
    muted: str  # secondary lines, extrapolations, guides
    data: str  # data points
    theory: str  # predictions, theory curves, Feynman-diagram accents
    detector: str  # detector layers (drawn as tints of this colour)
    highlight: str  # the one "look here" colour
    cycle: tuple[str, ...]

    def __post_init__(self) -> None:
        for field in ("background", "ink", "muted", "data", "theory", "detector", "highlight"):
            to_rgb(getattr(self, field))
        if not self.cycle:
            raise ValueError("a palette needs at least one cycle colour")
        for color in self.cycle:
            to_rgb(color)


#: The default palette: Okabe–Ito colours on a white background
#: ("reads better on a projector").
DEFAULT = Palette(
    name="default",
    background="#FFFFFF",
    ink="#262A33",
    muted="#8A8F98",
    data="#111418",
    theory="#0072B2",
    detector="#56B4E9",
    highlight="#D55E00",
    cycle=(
        "#0072B2",  # blue
        "#D55E00",  # vermillion
        "#009E73",  # bluish green
        "#E69F00",  # orange
        "#CC79A7",  # reddish purple
        "#56B4E9",  # sky blue
        "#F0E442",  # yellow (weak on white: last)
    ),
)
