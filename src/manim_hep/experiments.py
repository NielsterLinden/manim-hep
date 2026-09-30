"""Experiment labels and user-supplied logos.

``label()`` always needs an explicit ``status``: manim-hep never picks
"Preliminary" or "Internal" for you, because what you may show depends on your
collaboration's approval of the result::

    lab = label("atlas", status="Simulation", sqrt_s=13.6, target=axes)
    lab = label("atlas", status=None, sqrt_s=13, lumi=140)   # bare "ATLAS" of a paper
    lab = label("cms-opendata", status=None, doi="10.7483/OPENDATA.CMS.XXXX.XXXX")

No collaboration logo ships with manim-hep. ``logo()`` only loads a file you
supply, and whether you may show it is your collaboration's rule.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ImageMobject,
    MarkupText,
    Mobject,
    Rectangle,
    SVGMobject,
    VGroup,
)

from manim_hep._presets import PRESETS, Preset, get_preset
from manim_hep.style import _resolve_font, _sized_text, current_theme

__all__ = ["PRESETS", "label", "logo"]

_LOCS = ("upper left", "upper right", "above")
_NOT_ENDORSED = "Not endorsed by CMS or CERN"


def _check_status(preset: Preset, status: str | None) -> None:
    if status is None:
        if preset.allow_bare:
            return
        raise ValueError(
            f"{preset.display} labels need an explicit status; "
            f"choose one of: {', '.join(preset.statuses)}"
        )
    if status in preset.statuses:
        return
    hint = ""
    for allowed in preset.statuses:
        if allowed.lower() == str(status).lower():
            hint = f" (did you mean {allowed!r}?)"
    choices = ", ".join(preset.statuses) + (", or None" if preset.allow_bare else "")
    raise ValueError(f"{status!r} is not a {preset.display} status{hint}; choose one of: {choices}")


def _number(value: float | str) -> str:
    return value if isinstance(value, str) else f"{value:g}"


def _info(preset: Preset, lumi, sqrt_s) -> tuple[str, str] | None:
    """(markup, plain) of the luminosity / centre-of-mass line."""
    lumi_m = lumi_p = energy_m = energy_p = None
    if lumi is not None:
        lumi_m, lumi_p = f"{_number(lumi)} fb<sup>−1</sup>", f"{_number(lumi)} fb⁻¹"
    if sqrt_s is not None:
        energy_m, energy_p = f"{_number(sqrt_s)} TeV", f"{_number(sqrt_s)} TeV"
    if lumi_m is None and energy_m is None:
        return None
    if preset.info_style == "lumi first":
        if lumi_m and energy_m:
            return f"{lumi_m} ({energy_m})", f"{lumi_p} ({energy_p})"
        if lumi_m:
            return lumi_m, lumi_p
        return f"({energy_m})", f"({energy_p})"
    parts_m, parts_p = [], []
    if energy_m:
        parts_m.append(f"√<i>s</i> = {energy_m}")
        parts_p.append(f"√s = {energy_p}")
    if lumi_m:
        parts_m.append(lumi_m)
        parts_p.append(lumi_p)
    return ", ".join(parts_m), ", ".join(parts_p)


def _styled(text: str, style: str) -> str:
    return {
        "bold italic": f"<b><i>{text}</i></b>",
        "bold": f"<b>{text}</b>",
        "italic": f"<i>{text}</i>",
        "regular": text,
    }[style]


def _area(target: Mobject | None) -> Mobject:
    if target is None:
        x0, y0, x1, y1 = current_theme().content_box
        return Rectangle(width=x1 - x0, height=y1 - y0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    return getattr(target, "frame", target)


def label(
    experiment: str,
    *,
    status: str | None,
    lumi: float | str | None = None,
    sqrt_s: float | str | None = None,
    loc: str = "upper left",
    target: Mobject | None = None,
    doi: str | Sequence[str] | None = None,
    font_size: float = 24,
    buff: float = 0.2,
) -> VGroup:
    """An experiment label such as "ATLAS Preliminary", placed on ``target``.

    Parameters
    ----------
    experiment
        ``"atlas"``, ``"cms"``, ``"cms-opendata"`` or ``"lhcb"``.
    status
        Required, and checked against the experiment's public list. ``None``
        gives the bare experiment name (ATLAS papers, CMS Open Data).
    lumi, sqrt_s
        Integrated luminosity in fb⁻¹ and centre-of-mass energy in TeV (numbers,
        or strings used verbatim).
    loc
        ``"upper left"`` or ``"upper right"`` inside the target, or ``"above"``
        it (CMS style: name top-left, luminosity top-right).
    target
        What to label: a ``DataAxes`` (its plot frame is used) or any mobject.
        Defaults to the content area of the frame.
    doi
        Dataset DOI(s); required for ``cms-opendata`` and not used otherwise.

    The result is a ``VGroup`` with ``.main``, ``.info`` and ``.note`` (or ``None``)
    and ``.plain``, the label as plain text.
    """
    preset = get_preset(experiment)
    if preset.name == "generic":
        raise ValueError(
            "the generic preset has no experiment label; "
            "use 'atlas', 'cms', 'cms-opendata' or 'lhcb'"
        )
    _check_status(preset, status)
    dois = [doi] if isinstance(doi, str) else list(doi or [])
    if preset.requires_doi and not dois:
        raise ValueError(f"{preset.name} labels must cite the dataset DOI: pass doi='10.7483/...'")
    if dois and not preset.requires_doi:
        raise ValueError("doi= is only used by Open Data labels (experiment='cms-opendata')")
    if loc not in _LOCS:
        raise ValueError(f"loc must be one of: {', '.join(_LOCS)}")

    font = _resolve_font(preset)
    ink = current_theme().palette.ink

    def text(markup: str, scale: float) -> MarkupText:
        return _sized_text(MarkupText, markup, font_size * scale, font=font, color=ink)

    main_markup = _styled(preset.display, preset.exp_style)
    plain = [preset.display]
    if status:
        main_markup += " " + _styled(status, preset.status_style)
        plain[0] += " " + status
    main = text(main_markup, 1.0)
    info_line = _info(preset, lumi, sqrt_s)
    info = text(info_line[0], 0.8) if info_line else None
    if info_line:
        plain.append(info_line[1])
    note = None
    if preset.requires_doi:
        note_plain = f"{_NOT_ENDORSED} · " + ", ".join(f"doi:{d}" for d in dois)
        note = text(note_plain, 0.55)
        plain.append(note_plain)

    area = _area(target)
    group = VGroup(*(m for m in (main, info, note) if m is not None))
    if loc == "above":
        block = VGroup(main, *([note] if note else []))
        block.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        block.next_to(area.get_corner(UP + LEFT), UP, buff=buff, aligned_edge=LEFT)
        if info is not None:
            info.next_to(area.get_corner(UP + RIGHT), UP, buff=buff, aligned_edge=RIGHT)
            info.align_to(main, DOWN)
    else:
        edge = LEFT if loc == "upper left" else RIGHT
        group.arrange(DOWN, aligned_edge=edge, buff=0.1)
        group.move_to(area.get_corner(UP + edge), aligned_edge=UP + edge)
        group.shift(DOWN * buff - edge * buff)
    group.main, group.info, group.note = main, info, note
    group.plain = "\n".join(plain)
    group.experiment, group.status = preset.name, status
    return group


def logo(path: str | Path, *, height: float = 0.6) -> Mobject:
    """Load a logo file you supply (.svg, .png or .jpg), scaled to ``height``.

    manim-hep never ships or downloads collaboration logos. Check your
    collaboration's rules before showing one.
    """
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(
            f"logo file not found: {file}. manim-hep ships no logos; pass a file you were given."
        )
    suffix = file.suffix.lower()
    if suffix == ".svg":
        mob: Mobject = SVGMobject(str(file))
    elif suffix in {".png", ".jpg", ".jpeg"}:
        mob = ImageMobject(str(file))
    else:
        raise ValueError(f"logo must be an .svg, .png or .jpg file, got {file.name}")
    mob.height = height
    return mob
