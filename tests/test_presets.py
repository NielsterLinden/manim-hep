from __future__ import annotations

import pytest

from manim_hep._presets import PRESETS, get_preset


def test_preset_names():
    assert list(PRESETS) == ["generic", "atlas", "cms", "cms-opendata", "lhcb"]


def test_status_lists_match_the_spec():
    assert PRESETS["atlas"].statuses == (
        "Internal",
        "Preliminary",
        "Simulation",
        "Simulation Internal",
        "Simulation Preliminary",
        "Work in Progress",
    )
    assert PRESETS["atlas"].allow_bare
    assert PRESETS["cms"].statuses == (
        "Preliminary",
        "Simulation",
        "Simulation Preliminary",
        "Supplementary",
        "Work in progress",
        "Private work",
    )
    assert not PRESETS["cms"].allow_bare
    assert PRESETS["lhcb"].statuses == ("Preliminary", "Unofficial", "Simulation")
    assert not PRESETS["lhcb"].allow_bare
    assert PRESETS["cms-opendata"].requires_doi
    assert PRESETS["generic"].statuses == ()


def test_get_preset_is_case_insensitive_and_explains_errors():
    assert get_preset("CMS") is PRESETS["cms"]
    with pytest.raises(ValueError, match="choose one of: generic, atlas, cms"):
        get_preset("alice")


@pytest.mark.parametrize("name", ["atlas", "cms", "lhcb"])
def test_parity_with_mplhep(name):
    mplhep = pytest.importorskip("mplhep")
    preset = PRESETS[name]
    style = getattr(mplhep.style, preset.mplhep_style)
    mpl_cycle = [d["color"].lower() for d in style["axes.prop_cycle"]]
    assert [c.lower() for c in preset.cycle] == mpl_cycle
    family = style["font.family"]
    family = family[0] if isinstance(family, list) else family
    fonts = style["font.sans-serif"] if family == "sans-serif" else style["font.serif"]
    assert fonts[0].lower() == preset.font.lower()
