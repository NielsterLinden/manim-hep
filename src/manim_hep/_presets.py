"""Experiment presets. This module never imports Manim.

Colour cycles and fonts follow mplhep's experiment styles (Scikit-HEP; mplhep
1.3.3: ``ATLAS``, ``CMS`` and ``LHCb2``); ``tests/test_presets.py`` checks the
parity whenever mplhep is installed. Status lists follow the experiments'
public figure conventions. None of this implies endorsement by any experiment.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["PRESETS", "Preset", "get_preset"]


@dataclass(frozen=True)
class Preset:
    name: str
    display: str  # the experiment name as printed in a label
    cycle: tuple[str, ...]
    font: str  # preferred font family; falls back to DejaVu Sans when not installed
    font_dir: str | None  # folder in mplhep_data/fonts that provides `font`
    statuses: tuple[str, ...]  # allowed values for label(status=...)
    allow_bare: bool  # whether status=None (the bare experiment name) is allowed
    requires_doi: bool  # Open Data: the label must cite the dataset DOI(s)
    exp_style: str  # "bold italic" | "bold" | "regular": how the experiment name is set
    status_style: str  # "regular" | "italic"
    info_style: str  # "sqrt_s first" (ATLAS, LHCb) | "lumi first" (CMS)
    mplhep_style: str | None  # name in mplhep.style used by the parity test


_OKABE_ITO_ATLAS = ("#d55e00", "#56b4e9", "#e69f00", "#f0e442", "#009e73", "#cc79a7", "#0072b2")
_PETROFF_6 = ("#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd")
_LHCB2 = (
    "#0078FF",
    "#FF6600",
    "#0AAFB6",
    "#FF3333",
    "#0000FF",
    "#00CC00",
    "#BF8040",
    "#FF33CC",
    "#FF7733",
    "#BFD1D4",
)
_GENERIC = ("#0072B2", "#D55E00", "#009E73", "#E69F00", "#CC79A7", "#56B4E9", "#F0E442")

PRESETS: dict[str, Preset] = {
    "generic": Preset(
        name="generic",
        display="",
        cycle=_GENERIC,
        font="DejaVu Sans",
        font_dir=None,
        statuses=(),
        allow_bare=False,
        requires_doi=False,
        exp_style="regular",
        status_style="regular",
        info_style="sqrt_s first",
        mplhep_style=None,
    ),
    "atlas": Preset(
        name="atlas",
        display="ATLAS",
        cycle=_OKABE_ITO_ATLAS,
        font="TeX Gyre Heros",
        font_dir="texgyreheros",
        statuses=(
            "Internal",
            "Preliminary",
            "Simulation",
            "Simulation Internal",
            "Simulation Preliminary",
            "Work in Progress",
        ),
        allow_bare=True,
        requires_doi=False,
        exp_style="bold italic",
        status_style="regular",
        info_style="sqrt_s first",
        mplhep_style="ATLAS",
    ),
    "cms": Preset(
        name="cms",
        display="CMS",
        cycle=_PETROFF_6,
        font="TeX Gyre Heros",
        font_dir="texgyreheros",
        statuses=(
            "Preliminary",
            "Simulation",
            "Simulation Preliminary",
            "Supplementary",
            "Work in progress",
            "Private work",
        ),
        allow_bare=False,
        requires_doi=False,
        exp_style="bold",
        status_style="italic",
        info_style="lumi first",
        mplhep_style="CMS",
    ),
    # No public CMS rule fixes the header wording for results made with CMS Open Data.
    # manim-hep sets "CMS Open Data" in plain weight, deliberately NOT in the bold/italic
    # style of official CMS figures, and always adds the non-endorsement statement of the
    # CMS data policy plus the dataset DOI(s).
    "cms-opendata": Preset(
        name="cms-opendata",
        display="CMS Open Data",
        cycle=_PETROFF_6,
        font="TeX Gyre Heros",
        font_dir="texgyreheros",
        statuses=("Simulation", "Private work"),
        allow_bare=True,
        requires_doi=True,
        exp_style="regular",
        status_style="regular",
        info_style="lumi first",
        mplhep_style="CMS",
    ),
    "lhcb": Preset(
        name="lhcb",
        display="LHCb",
        cycle=_LHCB2,
        font="TeX Gyre Termes",
        font_dir="texgyretermes",
        statuses=("Preliminary", "Unofficial", "Simulation"),
        allow_bare=False,
        requires_doi=False,
        exp_style="regular",
        status_style="regular",
        info_style="sqrt_s first",
        mplhep_style="LHCb2",
    ),
}


def get_preset(name: str) -> Preset:
    """Return the preset called ``name`` (case-insensitive)."""
    key = str(name).lower()
    if key not in PRESETS:
        raise ValueError(f"unknown experiment {name!r}; choose one of: {', '.join(PRESETS)}")
    return PRESETS[key]
