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
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from manim import (
    AnnularSector,
    Annulus,
    Circle,
    Cross,
    Dot,
    MarkupText,
    Mobject,
    Polygram,
    Rectangle,
    SurroundingRectangle,
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
_unlisted: list = []  # our fonts, loaded into Pango and taken off ManimPango's re-add list
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


_TEXT_RENDER_SIZE = 48.0


def _sized_text(cls, content: str, font_size: float, **kwargs):
    """``Text``/``MarkupText`` at ``font_size`` with even letter spacing.

    Pango spaces glyphs unevenly at small sizes, so small text is rendered at size 48
    and scaled down.
    """
    size = max(float(font_size), _TEXT_RENDER_SIZE)
    mob = cls(content, font_size=size, **kwargs)
    if size != font_size:
        mob.scale(font_size / size)
    return mob


def _load_and_unlist_on_windows() -> None:
    """Work around a slow path in ManimPango on Windows.

    ManimPango re-adds every registered font file to Pango's font map on every
    text render, which costs about a second per file per ``Text``. One warm-up
    render loads the files into the process-wide font map, where they stay; then
    they are taken off ManimPango's re-add list. The font list Manim checks
    names against is cached first, while the fonts are still listed.
    """
    import tempfile

    import manimpango

    with tempfile.TemporaryDirectory() as tmp:
        setting = manimpango.TextSetting(0, 1, _FALLBACK_FONT, "NORMAL", "NORMAL")
        manimpango.text2svg([setting], 10, 0, True, str(Path(tmp) / "w.svg"), 0, 0, 50, 50, "x")
    manimpango.registered_fonts.update(_unlisted)  # so the font list names every family
    Text.font_list.cache_clear()
    Text.font_list()
    MarkupText.font_list.cache_clear()
    MarkupText.font_list()
    for font in list(manimpango.registered_fonts):
        if str(Path(font.path).resolve()) in _registered:
            manimpango.registered_fonts.discard(font)
            if font not in _unlisted:
                _unlisted.append(font)


def _register(files: list[Path]) -> bool:
    """Register font files with Pango once per process; True if all are available."""
    import manimpango

    new = [str(f.resolve()) for f in files if str(f.resolve()) not in _registered]
    ok = all(str(f.resolve()) in _registered for f in files if str(f.resolve()) not in new)
    for key in new:
        if manimpango.register_font(key):
            _registered.add(key)
        else:
            ok = False
    if new:
        if sys.platform == "win32":
            _load_and_unlist_on_windows()
        else:
            Text.font_list.cache_clear()
            MarkupText.font_list.cache_clear()
    return ok


def _resolve_font(preset: Preset) -> str:
    """Make the preset's font available and return its family name.

    Experiment presets use mplhep's fonts when ``manim-hep[mplhep]`` is
    installed (regular, bold, italic and bold italic faces only); everything
    else uses the bundled DejaVu Sans.
    """
    if preset.font_dir and preset.font != _FALLBACK_FONT:
        try:
            import mplhep_data
        except ImportError:
            pass
        else:
            folder = Path(mplhep_data.__file__).parent / "fonts" / preset.font_dir
            files = sorted(folder.glob(f"{preset.font_dir}-*.otf"))
            if files and _register(files):
                return preset.font
    _register(sorted(_FONT_DIR.glob("*.ttf")))
    return _FALLBACK_FONT


def _apply(theme: Theme) -> None:
    config.background_color = theme.palette.background
    for cls in _COLOURED_CLASSES:
        cls.set_default()
        cls.set_default(color=theme.palette.ink)
    for cls in _TEXT_CLASSES:
        cls.set_default()
        cls.set_default(font=theme.font)
    # Manim's highlight shapes default to yellow and red, which vanish or clash on white.
    SurroundingRectangle.set_default()
    SurroundingRectangle.set_default(color=theme.palette.highlight)
    Cross.set_default()
    Cross.set_default(stroke_color=theme.palette.highlight)


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
