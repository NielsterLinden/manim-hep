"""manim-hep: high-energy-physics building blocks for Manim Community Edition.

Import what you need, e.g. ``from manim_hep import use_theme, DataAxes, label``.

The top-level names are loaded lazily. Manim imports every ``manim.plugins``
entry point while it is itself being imported, so this module must not import
Manim at import time, and ``manim_hep.palette`` must stay usable without Manim.
"""

from __future__ import annotations

import importlib
from typing import Any

__version__ = "0.1.0"

_LAZY = {
    "Theme": "style",
    "use_theme": "style",
    "current_theme": "style",
    "intrusions": "style",
    "TITLE_BAND_Y": "style",
    "tint": "palette",
    "shade": "palette",
    "mix": "palette",
    "Palette": "palette",
    "label": "experiments",
    "logo": "experiments",
    "add_state": "build",
    "check_order": "build",
    "place": "build",
    "freeze": "data",
    "load_frozen": "data",
    "FrozenDataError": "data",
    "FeynmanDiagram": "feynman",
    "fermion": "feynman",
    "photon": "feynman",
    "gluon": "feynman",
    "scalar": "feynman",
    "vertex": "feynman",
    "DataAxes": "plots",
    "step_hist": "plots",
    "stack_hist": "plots",
    "errorbars": "plots",
    "band": "plots",
    "ratio_panel": "plots",
    "BarrelSlice": "detector",
    "track": "detector",
    "signature": "detector",
}

__all__ = ["__version__", *_LAZY]


def __getattr__(name: str) -> Any:
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module 'manim_hep' has no attribute {name!r}")
    return getattr(importlib.import_module(f"manim_hep.{module}"), name)


def __dir__() -> list[str]:
    return sorted(__all__)
