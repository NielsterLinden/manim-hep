"""Reading ``manim-hep.toml``, the per-project settings file. Never imports Manim."""

from __future__ import annotations

import math
import tomllib
import warnings
from dataclasses import dataclass, field
from pathlib import Path

from manim_hep._presets import PRESETS

__all__ = ["ALLOWED", "SETTINGS_FILE", "Settings", "find_settings", "load_settings"]

SETTINGS_FILE = "manim-hep.toml"

ALLOWED = {
    "storyline": ("off", "markdown", "artifact"),
    "verify": ("none", "render", "frames", "review"),
    "branch": ("current", "feature", "worktree"),
    "commit": ("never", "ask", "auto"),
}

_KNOWN = {
    "paths": {"root"},
    "style": {"experiment", "title_band", "keep_out"},
    "agent": set(ALLOWED),
}


@dataclass(frozen=True)
class Settings:
    """The project settings, with the documented defaults for anything not set."""

    project_dir: Path | None = None  # folder that holds manim-hep.toml (None: no file)
    root: str = "."
    experiment: str = "generic"
    title_band: float = 2.7
    keep_out: tuple[tuple[float, float, float, float], ...] = field(default=())
    storyline: str = "artifact"
    verify: str = "frames"
    branch: str = "feature"
    commit: str = "ask"

    @property
    def root_dir(self) -> Path:
        """Where scenes/, storylines/, data/ and clips/ live."""
        return ((self.project_dir or Path.cwd()) / self.root).resolve()


def find_settings(start: Path | str | None = None) -> Path | None:
    """The nearest ``manim-hep.toml`` in ``start`` or any folder above it."""
    here = Path(start or Path.cwd()).resolve()
    if here.is_file():
        here = here.parent
    for folder in (here, *here.parents):
        candidate = folder / SETTINGS_FILE
        if candidate.is_file():
            return candidate
    return None


def _is_number(value) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and math.isfinite(value)


def _choice(section: dict, key: str, allowed: tuple[str, ...], default: str) -> str:
    value = section.get(key, default)
    if value not in allowed:
        raise ValueError(
            f"{SETTINGS_FILE}: {key} = {value!r} is not allowed; use one of: {', '.join(allowed)}"
        )
    return value


def load_settings(path: Path | str | None = None, *, search_from: Path | str | None = None):
    """Load settings from ``path``, or from the nearest file above ``search_from``/cwd."""
    if path is None:
        path = find_settings(search_from)
    if path is None:
        return Settings()
    path = Path(path)
    with path.open("rb") as fh:
        data = tomllib.load(fh)

    for section, keys in data.items():
        if section not in _KNOWN:
            warnings.warn(f"{path}: unknown section [{section}] ignored", stacklevel=2)
            continue
        for key in keys if isinstance(keys, dict) else ():
            if key not in _KNOWN[section]:
                warnings.warn(f"{path}: unknown key {section}.{key} ignored", stacklevel=2)

    for section in _KNOWN:
        if not isinstance(data.get(section, {}), dict):
            raise ValueError(f"{SETTINGS_FILE}: [{section}] must be a table of settings")
    paths, style, agent = data.get("paths", {}), data.get("style", {}), data.get("agent", {})
    root = paths.get("root", ".")
    if not isinstance(root, str) or not root:
        raise ValueError(f"{SETTINGS_FILE}: paths.root must be a non-empty string")
    experiment = str(style.get("experiment", "generic")).lower()
    if experiment not in PRESETS:
        raise ValueError(
            f"{SETTINGS_FILE}: style.experiment = {experiment!r} is not allowed; "
            f"use one of: {', '.join(PRESETS)}"
        )
    title_band = style.get("title_band", 2.7)
    if not _is_number(title_band):
        raise ValueError(f"{SETTINGS_FILE}: style.title_band must be a number (4.0 disables it)")
    keep_out = []
    boxes = style.get("keep_out", [])
    if not isinstance(boxes, list):
        raise ValueError(f"{SETTINGS_FILE}: keep_out is a list of [x0, y0, x1, y1] boxes")
    for box in boxes:
        if not isinstance(box, list) or len(box) != 4 or not all(_is_number(v) for v in box):
            raise ValueError(
                f"{SETTINGS_FILE}: each keep_out entry is [x0, y0, x1, y1], e.g. "
                "keep_out = [[-7.1, 0.2, -5.85, 4.0]]"
            )
        x0, y0, x1, y1 = (float(v) for v in box)
        keep_out.append((min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)))

    return Settings(
        project_dir=path.parent.resolve(),
        root=root,
        experiment=experiment,
        title_band=float(title_band),
        keep_out=tuple(keep_out),
        storyline=_choice(agent, "storyline", ALLOWED["storyline"], "artifact"),
        verify=_choice(agent, "verify", ALLOWED["verify"], "frames"),
        branch=_choice(agent, "branch", ALLOWED["branch"], "feature"),
        commit=_choice(agent, "commit", ALLOWED["commit"], "ask"),
    )
