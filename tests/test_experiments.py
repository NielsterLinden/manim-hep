from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from manim import ImageMobject, Rectangle, SVGMobject
from PIL import Image

from manim_hep.experiments import label, logo
from manim_hep.style import intrusions, use_theme


@pytest.fixture(autouse=True)
def _theme():
    use_theme("generic")


def test_status_is_required():
    with pytest.raises(TypeError, match="status"):
        label("atlas")  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("experiment", "status", "message"),
    [
        ("cms", "preliminary", r"did you mean 'Preliminary'"),
        ("cms", "Unofficial", r"not a CMS status; choose one of: Preliminary, Simulation"),
        ("lhcb", "Internal", r"choose one of: Preliminary, Unofficial, Simulation"),
        ("atlas", "Private work", r"or None"),
    ],
)
def test_invalid_status_lists_the_valid_ones(experiment, status, message):
    with pytest.raises(ValueError, match=message):
        label(experiment, status=status)


def test_bare_label_only_where_allowed():
    assert label("atlas", status=None).plain == "ATLAS"
    for experiment in ("cms", "lhcb"):
        with pytest.raises(ValueError, match="need an explicit status"):
            label(experiment, status=None)


def test_generic_has_no_label():
    with pytest.raises(ValueError, match="generic preset has no experiment label"):
        label("generic", status=None)


def test_atlas_text():
    lab = label("atlas", status="Simulation Internal", sqrt_s=13.6, lumi=140)
    assert lab.plain == "ATLAS Simulation Internal\n√s = 13.6 TeV, 140 fb⁻¹"
    assert lab.note is None


def test_cms_puts_lumi_first():
    lab = label("cms", status="Preliminary", sqrt_s=13, lumi=138)
    assert lab.plain == "CMS Preliminary\n138 fb⁻¹ (13 TeV)"
    assert label("cms", status="Simulation", sqrt_s=13).plain == "CMS Simulation\n(13 TeV)"


def test_lhcb_text():
    assert label("lhcb", status="Unofficial", sqrt_s=13).plain == "LHCb Unofficial\n√s = 13 TeV"


def test_open_data_needs_and_shows_the_doi():
    with pytest.raises(ValueError, match="must cite the dataset DOI"):
        label("cms-opendata", status=None)
    lab = label(
        "cms-opendata",
        status=None,
        lumi=16.4,
        sqrt_s=13,
        doi=["10.7483/OPENDATA.CMS.AAAA.AAAA", "10.7483/OPENDATA.CMS.BBBB.BBBB"],
    )
    assert lab.plain.splitlines() == [
        "CMS Open Data",
        "16.4 fb⁻¹ (13 TeV)",
        "Not endorsed by CMS or CERN · doi:10.7483/OPENDATA.CMS.AAAA.AAAA, "
        "doi:10.7483/OPENDATA.CMS.BBBB.BBBB",
    ]
    assert lab.note is not None


def test_doi_is_only_for_open_data():
    with pytest.raises(ValueError, match="only used by Open Data labels"):
        label("cms", status="Preliminary", doi="10.1/x")


def test_unknown_loc():
    with pytest.raises(ValueError, match="loc must be one of"):
        label("atlas", status=None, loc="bottom")


@pytest.mark.parametrize("loc", ["upper left", "upper right"])
def test_inside_label_stays_inside_the_target(loc):
    target = Rectangle(width=6, height=4).move_to([1, -1, 0])
    lab = label("atlas", status="Preliminary", sqrt_s=13, lumi=140, loc=loc, target=target)
    assert lab.get_left()[0] >= target.get_left()[0]
    assert lab.get_right()[0] <= target.get_right()[0]
    assert lab.get_top()[1] <= target.get_top()[1]
    corner_x = target.get_left()[0] if loc == "upper left" else target.get_right()[0]
    edge_x = lab.get_left()[0] if loc == "upper left" else lab.get_right()[0]
    assert abs(edge_x - corner_x) == pytest.approx(0.2, abs=1e-6)


def test_above_label_sits_on_top_of_the_target():
    target = Rectangle(width=6, height=3).move_to([0, -1.5, 0])
    lab = label("cms", status="Preliminary", sqrt_s=13, lumi=138, loc="above", target=target)
    top = target.get_top()[1]
    assert lab.main.get_bottom()[1] > top
    assert lab.info.get_bottom()[1] > top
    assert lab.main.get_left()[0] == pytest.approx(target.get_left()[0])
    assert lab.info.get_right()[0] == pytest.approx(target.get_right()[0])


def test_default_target_is_the_content_area():
    lab = label("lhcb", status="Preliminary", loc="upper right")
    assert intrusions(lab) == []


def test_logo_needs_a_real_file(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="ships no logos"):
        logo(tmp_path / "missing.svg")
    bad = tmp_path / "logo.gif"
    bad.write_bytes(b"GIF89a")
    with pytest.raises(ValueError, match=r"\.svg, \.png or \.jpg"):
        logo(bad)


def test_logo_loads_svg_and_png(tmp_path: Path):
    svg = tmp_path / "logo.svg"
    svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
        '<rect width="10" height="5" fill="#123456"/></svg>',
        encoding="utf-8",
    )
    png = tmp_path / "logo.png"
    Image.fromarray(np.zeros((20, 40, 3), dtype=np.uint8)).save(png)
    s = logo(svg, height=1.0)
    p = logo(png, height=0.5)
    assert isinstance(s, SVGMobject) and s.height == pytest.approx(1.0)
    assert isinstance(p, ImageMobject) and p.height == pytest.approx(0.5)


def test_default_target_labels_stay_out_of_the_title_band():
    for loc in ("upper left", "upper right", "above"):
        lab = label("cms", status="Private work", lumi=138, sqrt_s=13, loc=loc)
        assert intrusions(lab) == [], loc
