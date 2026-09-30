from __future__ import annotations

import subprocess
import sys

import pytest
from _cvd import MACHADO_2009, ciede2000, min_pairwise_distance

from manim_hep.palette import DEFAULT, OKABE_ITO, Palette, mix, shade, tint, to_hex, to_rgb


def test_parse_long_short_and_case():
    assert to_rgb("#FF8000") == (1.0, 128 / 255, 0.0)
    assert to_rgb("#f80") == to_rgb("#FF8800")
    assert to_rgb("#abcdef") == to_rgb("#ABCDEF")


@pytest.mark.parametrize("bad", ["FF8000", "#FF80", "#GG0000", "red", "", None, "#FF800000"])
def test_parse_rejects_other_forms(bad):
    with pytest.raises(ValueError, match="expected a colour"):
        to_rgb(bad)


def test_round_trip_and_clipping():
    assert to_hex(to_rgb("#12AB9F")) == "#12AB9F"
    assert to_hex((1.2, -0.1, 0.5)) == "#FF0080"


def test_mix_endpoints_and_midpoint():
    assert mix("#000000", "#FFFFFF", 0.0) == "#000000"
    assert mix("#000000", "#FFFFFF", 1.0) == "#FFFFFF"
    assert mix("#000000", "#FFFFFF", 0.5) == "#808080"


def test_tint_and_shade():
    assert tint("#0072B2", 0.0) == "#0072B2"
    assert tint("#0072B2", 1.0) == "#FFFFFF"
    assert shade("#0072B2", 1.0) == "#000000"
    with pytest.raises(ValueError, match="between 0 and 1"):
        tint("#0072B2", 1.5)
    with pytest.raises(ValueError, match="between 0 and 1"):
        shade("#0072B2", -0.1)


def test_palette_validates_its_colours():
    with pytest.raises(ValueError):
        Palette("bad", "#FFF", "#000", "#888", "#000", "#00F", "#0FF", "notacolour", ("#F00",))
    with pytest.raises(ValueError, match="cycle"):
        Palette("bad", "#FFF", "#000", "#888", "#000", "#00F", "#0FF", "#F00", ())


def test_default_is_white_background_okabe_ito_cycle():
    assert DEFAULT.background == "#FFFFFF"
    assert set(DEFAULT.cycle) == set(OKABE_ITO[1:])


def test_palette_module_does_not_import_manim():
    code = "import sys, manim_hep.palette; print('manim' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "False"


# --- colour-vision-deficiency checks -------------------------------------------------


@pytest.mark.parametrize(
    ("lab1", "lab2", "expected"),
    [  # reference pairs from Sharma, Wu and Dalal (2005)
        ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
        ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
        ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
        ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
    ],
)
def test_ciede2000_reference_pairs(lab1, lab2, expected):
    assert ciede2000(lab1, lab2) == pytest.approx(expected, abs=1e-4)


def _shipped_cycles() -> dict[str, tuple[str, ...]]:
    from manim_hep._presets import PRESETS

    cycles = {"default": DEFAULT.cycle}
    cycles.update({name: p.cycle for name, p in PRESETS.items()})
    return cycles


# Official experiment palettes are shipped as the experiments publish them. If one
# falls below the Okabe–Ito baseline it is listed here and in docs/concepts/colour.md,
# never altered.
CVD_EXCEPTIONS = {
    # min ΔE00 (deuteranopia, protanopia, tritanopia); Okabe–Ito baseline: 11.6, 12.2, 10.9
    "cms": "Petroff 6 (arXiv:2107.02270): 14.7, 10.6, 18.3; #964a8b vs #7a21dd (protanopia)",
    "cms-opendata": "same cycle as cms",
    "lhcb": "mplhep LHCb2: 0.2, 4.2, 4.2; green #00CC00 and orange #FF7733 merge (deuteranopia)",
}


@pytest.mark.parametrize("kind", sorted(MACHADO_2009))
def test_shipped_cycles_are_as_distinguishable_as_okabe_ito(kind):
    baseline = min_pairwise_distance(OKABE_ITO[1:], kind)
    for name, cycle in _shipped_cycles().items():
        if name in CVD_EXCEPTIONS:
            continue
        got = min_pairwise_distance(cycle, kind)
        assert got >= baseline - 1e-9, f"{name} under {kind}: {got:.2f} < baseline {baseline:.2f}"


def test_cvd_exceptions_really_fall_below_baseline():
    """Keep the exception list honest: drop an entry once the palette passes."""
    cycles = _shipped_cycles()
    for name in CVD_EXCEPTIONS:
        worst = min(
            min_pairwise_distance(cycles[name], kind) - min_pairwise_distance(OKABE_ITO[1:], kind)
            for kind in MACHADO_2009
        )
        assert worst < 0, f"{name} now meets the baseline; remove it from CVD_EXCEPTIONS"
