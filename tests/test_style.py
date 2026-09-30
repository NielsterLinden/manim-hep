from __future__ import annotations

from pathlib import Path

import pytest
from manim import Circle, Dot, Line, MarkupText, Square, Text, config

from manim_hep.palette import DEFAULT
from manim_hep.style import TITLE_BAND_Y, current_theme, intrusions, use_theme


@pytest.fixture(autouse=True)
def _restore_theme():
    yield
    use_theme("generic")


def test_generic_theme_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    theme = use_theme()
    assert theme.experiment == "generic"
    assert theme.palette == DEFAULT
    assert theme.font == "DejaVu Sans"
    assert theme.title_band == TITLE_BAND_Y
    assert config.background_color.to_hex().upper() == DEFAULT.background


def test_shapes_and_text_take_the_ink_colour():
    theme = use_theme("generic")
    ink = theme.palette.ink.upper()
    for mob in (Line(), Square(), Dot(), Circle()):
        assert mob.get_color().to_hex().upper() == ink, type(mob).__name__
    assert Text("A")[0].get_fill_color().to_hex().upper() == ink
    assert MarkupText("<b>A</b>")[0].get_fill_color().to_hex().upper() == ink
    assert Text("A").font == theme.font


def test_experiment_theme_uses_the_preset_cycle():
    theme = use_theme("cms")
    assert theme.experiment == "cms"
    assert theme.palette.cycle[0].lower() == "#5790fc"
    assert theme.palette.ink == DEFAULT.ink


def test_experiment_font_with_mplhep():
    pytest.importorskip("mplhep_data")
    assert use_theme("atlas").font == "TeX Gyre Heros"
    assert use_theme("lhcb").font == "TeX Gyre Termes"


def test_argument_beats_the_settings_file(tmp_path: Path, monkeypatch):
    (tmp_path / "manim-hep.toml").write_text('[style]\nexperiment = "lhcb"\n', encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    assert use_theme().experiment == "lhcb"
    assert use_theme("atlas").experiment == "atlas"


def test_unknown_theme_is_explained():
    with pytest.raises(ValueError, match="choose one of"):
        use_theme("alice")


def test_calling_twice_replaces_the_defaults():
    use_theme("cms")
    use_theme("generic")
    assert Line().get_color().to_hex().upper() == DEFAULT.ink


def test_current_theme_activates_one():
    assert current_theme().experiment in {"generic", "atlas", "cms", "cms-opendata", "lhcb"}


def test_intrusions(tmp_path: Path, monkeypatch):
    (tmp_path / "manim-hep.toml").write_text(
        "[style]\nkeep_out = [[-7.2, 0.2, -5.85, 4.0]]\n", encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)
    theme = use_theme()
    assert intrusions(Square(1), theme) == []
    assert intrusions(Square(1).move_to([0, 3.0, 0]), theme) == ["title band"]
    assert intrusions(Square(1).move_to([0, 3.9, 0]), theme) == ["frame", "title band"]
    assert intrusions(Square(1).move_to([-6.2, 1.0, 0]), theme) == ["keep-out 1"]
    assert theme.content_box[3] == TITLE_BAND_Y
    assert theme.content_center[1] == pytest.approx((-4 + TITLE_BAND_Y) / 2)


def test_highlight_shapes_follow_the_theme():
    from manim import Cross, SurroundingRectangle

    theme = use_theme("generic")
    box = SurroundingRectangle(Square(1))
    assert box.get_color().to_hex().upper() == theme.palette.highlight
    cross = Cross(Square(1))
    assert cross[0].get_stroke_color().to_hex().upper() == theme.palette.highlight
