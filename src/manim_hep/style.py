"""The theme: background, colours, fonts and safe areas for every scene.

Call :func:`use_theme` once at the top of a scene file::

    from manim import *
    from manim_hep import use_theme

    theme = use_theme()          # reads [style] experiment from manim-hep.toml
    C = theme.palette            # colour roles: C.ink, C.data, C.theory, ...

After that, new shapes, ``Text`` and ``MathTex`` are drawn in ``C.ink`` on the
theme background, and text uses the theme font. Scenes take every other colour
from ``C``, never from literals.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from manim import (
    AnnularSector,
    Annulus,
    Circle,
    Dot,
    MarkupText,
    Mobject,
    Polygram,
    Rectangle,
    Text,
    VMobject,
    config,
)

from manim_hep._presets import Preset, get_preset
from manim_hep._settings import load_settings
from manim_hep.palette import DEFAULT, Palette

__all__ = ["TITLE_BAND_Y", "Theme", "current_theme", "intrusions", "use_theme"]

#: Nothing is drawn above this y: the band is kept clear for the slide title.
TITLE_BAND_Y = 2.7

_FONT_DIR = Path(__file__).parent / "fonts"
_FALLBACK_FONT = "DejaVu Sans"
# Classes whose own signature sets a colour default (e.g. Dot is WHITE, Square is BLUE),
# so VMobject's default alone does not reach them.
_COLOURED_CLASSES = (VMobject, Circle, Dot, Annulus, AnnularSector, Polygram, Rectangle)
_TEXT_CLASSES = (Text, MarkupText)

_registered: set[str] = set()
_active: Theme | None = None


@dataclass(frozen=True)
class Theme:
    experiment: str
    palette: Palette
    font: str
    title_band: float = TITLE_BAND_Y
    keep_out: tuple[tuple[float, float, float, float], ...] = ()

    @property
    def content_box(self) -> tuple[float, float, float, float]:
        """(x0, y0, x1, y1) of the area scenes may draw in: the frame below the title band."""
        w, h = config.frame_width / 2, config.frame_height / 2
        return (-w, -h, w, min(self.title_band, h))

    @property
    def content_center(self) -> np.ndarray:
        x0, y0, x1, y1 = self.content_box
        return np.array([(x0 + x1) / 2, (y0 + y1) / 2, 0.0])


def _register(font_file: Path) -> bool:
    import manimpango

    key = str(font_file.resolve())
    if key in _registered:
        return True
    if manimpango.register_font(key):
        _registered.add(key)
        return True
    return False


def _resolve_font(preset: Preset) -> str:
    """Register the bundled DejaVu fonts, and mplhep's font for the preset if installed."""
    for font_file in sorted(_FONT_DIR.glob("*.ttf")):
        _register(font_file)
    family = _FALLBACK_FONT
    if preset.font_dir and preset.font != _FALLBACK_FONT:
        try:
            import mplhep_data
        except ImportError:
            pass
        else:
            folder = Path(mplhep_data.__file__).parent / "fonts" / preset.font_dir
            files = sorted([*folder.glob("*.otf"), *folder.glob("*.ttf")])
            if files and all(_register(f) for f in files):
                family = preset.font
    Text.font_list.cache_clear()
    MarkupText.font_list.cache_clear()
    return family


def _apply(theme: Theme) -> None:
    config.background_color = theme.palette.background
    for cls in _COLOURED_CLASSES:
        cls.set_default()
        cls.set_default(color=theme.palette.ink)
    for cls in _TEXT_CLASSES:
        cls.set_default()
        cls.set_default(font=theme.font)


def _search_start() -> Path:
    input_file = config.input_file
    if input_file:
        return Path(input_file).resolve().parent
    return Path.cwd()


def use_theme(name: str | None = None) -> Theme:
    """Activate the theme for ``name`` (generic, atlas, cms, cms-opendata or lhcb).

    With no name, the experiment comes from ``[style] experiment`` in the nearest
    ``manim-hep.toml`` (searched upward from the scene file, else the working
    directory), and otherwise ``generic``. Calling it again replaces the theme.
    """
    global _active
    settings = load_settings(search_from=_search_start())
    preset = get_preset(name or settings.experiment)
    palette = DEFAULT
    if preset.name != "generic":
        palette = dataclasses.replace(DEFAULT, name=preset.name, cycle=preset.cycle)
    theme = Theme(
        experiment=preset.name,
        palette=palette,
        font=_resolve_font(preset),
        title_band=settings.title_band,
        keep_out=settings.keep_out,
    )
    _apply(theme)
    _active = theme
    return theme


def current_theme() -> Theme:
    """The active theme; activates the default one if none is active yet."""
    return _active if _active is not None else use_theme()


def intrusions(mobject: Mobject, theme: Theme | None = None) -> list[str]:
    """Which safe-area rules the bounding box of ``mobject`` breaks.

    Returns a subset of ``["frame", "title band", "keep-out 1", ...]``; empty is good.
    """
    theme = theme or current_theme()
    left, right = mobject.get_left()[0], mobject.get_right()[0]
    bottom, top = mobject.get_bottom()[1], mobject.get_top()[1]
    w, h = config.frame_width / 2, config.frame_height / 2
    eps = 1e-6
    problems = []
    if left < -w - eps or right > w + eps or bottom < -h - eps or top > h + eps:
        problems.append("frame")
    if top > theme.title_band + eps:
        problems.append("title band")
    for i, (x0, y0, x1, y1) in enumerate(theme.keep_out, start=1):
        if left < x1 and right > x0 and bottom < y1 and top > y0:
            problems.append(f"keep-out {i}")
    return problems
