"""Frozen numbers: every number on screen comes from a file with provenance.

An extractor script runs in your analysis environment (ROOT, uproot, pandas,
...) and freezes the values a scene needs::

    freeze({"n_signal": 42, "edges": edges, "counts": counts}, "data/yields.json",
           source="ntuples v3, signal region", selection="2 muons, pT > 25 GeV",
           version="analysis tag v1.2")

The scene then loads them without any analysis stack, and asserts the numbers
the storyline promised::

    values = load_frozen("data/yields.json", expect={"n_signal": 42})

If a number moved, ``load_frozen`` stops the render instead of quietly showing
a different value.
"""

from __future__ import annotations

import datetime as _dt
import json
import math
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

__all__ = ["FrozenDataError", "freeze", "load_frozen"]


class FrozenDataError(ValueError):
    """The frozen file does not contain what the scene expects."""


def _plain(value: Any, where: str) -> Any:
    """Convert NumPy values to JSON types and refuse NaN and infinities."""
    if hasattr(value, "tolist") and not isinstance(value, str | bytes):
        value = value.tolist()
    if isinstance(value, Mapping):
        return {str(k): _plain(v, f"{where}.{k}") for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_plain(v, f"{where}[{i}]") for i, v in enumerate(value)]
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{where} is {value}; JSON cannot store NaN or infinity")
    if value is None or isinstance(value, bool | int | float | str):
        return value
    raise TypeError(f"{where} has type {type(value).__name__}, which JSON cannot store")


def _git(*args: str, cwd: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10, check=True
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip()


def _producer() -> Path:
    main = sys.modules.get("__main__")
    main_file = getattr(main, "__file__", None)
    return Path(main_file).resolve() if main_file else Path.cwd()


def freeze(
    values: Mapping[str, Any],
    path: str | Path,
    *,
    source: str,
    selection: str | None = None,
    version: str | None = None,
) -> Path:
    """Write ``values`` to JSON at ``path`` together with where they came from.

    The provenance records ``source``, ``selection`` and ``version`` as given,
    the time, and the git commit and dirty flag of the repository that ran the
    producing script (``None`` outside git).
    """
    if not source:
        raise ValueError("source= is required: say where the numbers come from")
    payload_values = _plain(dict(values), "values")
    producer = _producer()
    repo_dir = producer if producer.is_dir() else producer.parent
    commit = _git("rev-parse", "HEAD", cwd=repo_dir)
    status = _git("status", "--porcelain", cwd=repo_dir) if commit else None
    payload = {
        "values": payload_values,
        "provenance": {
            "source": source,
            "selection": selection,
            "version": version,
            "frozen_at": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
            "producer": producer.name,
            "git_commit": commit,
            "git_dirty": bool(status) if commit else None,
        },
    }
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return out


def _compare(expected: Any, found: Any, rtol: float, where: str, problems: list[str]) -> None:
    if isinstance(expected, Mapping):
        if not isinstance(found, Mapping):
            problems.append(f"{where}: expected a mapping, found {found!r}")
            return
        for key, value in expected.items():
            if key not in found:
                problems.append(f"{where}.{key}: missing")
            else:
                _compare(value, found[key], rtol, f"{where}.{key}", problems)
        return
    if isinstance(expected, list | tuple) or hasattr(expected, "tolist"):
        expected = expected.tolist() if hasattr(expected, "tolist") else list(expected)
        if not isinstance(found, list) or len(found) != len(expected):
            problems.append(f"{where}: expected {expected!r}, found {found!r}")
            return
        for i, (e, f) in enumerate(zip(expected, found, strict=True)):
            _compare(e, f, rtol, f"{where}[{i}]", problems)
        return
    if isinstance(expected, int | float) and not isinstance(expected, bool):
        ok = isinstance(found, int | float) and not isinstance(found, bool)
        if ok and math.isclose(expected, found, rel_tol=rtol, abs_tol=0.0):
            return
        problems.append(f"{where}: expected {expected!r}, found {found!r}")
        return
    if expected != found:
        problems.append(f"{where}: expected {expected!r}, found {found!r}")


def load_frozen(
    path: str | Path, *, expect: Mapping[str, Any] | None = None, rtol: float = 1e-9
) -> dict[str, Any]:
    """Load the values frozen at ``path``; check every key in ``expect``.

    Numbers compare with relative tolerance ``rtol``; everything else must be
    equal. Any mismatch raises :class:`FrozenDataError` listing all of them.
    """
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(f"no frozen data at {file}; run its extractor script first")
    payload = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "values" not in payload:
        raise FrozenDataError(f"{file} is not a manim-hep frozen file (no 'values' key)")
    values = payload["values"]
    if expect:
        problems: list[str] = []
        _compare(dict(expect), values, rtol, "values", problems)
        if problems:
            raise FrozenDataError(
                f"{file} does not match what the scene expects:\n  " + "\n  ".join(problems)
            )
    return values
