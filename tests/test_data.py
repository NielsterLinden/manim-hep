from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from manim_hep.data import FrozenDataError, freeze, load_frozen


def test_round_trip_with_numpy_and_provenance(tmp_path: Path):
    out = freeze(
        {"n": np.int64(42), "counts": np.array([1.5, 2.0]), "label": "Z", "nested": {"a": 1}},
        tmp_path / "data" / "yields.json",
        source="toy MC, seed 7",
        selection="none",
        version="v1",
    )
    payload = json.loads(out.read_text(encoding="utf-8"))
    prov = payload["provenance"]
    assert (prov["source"], prov["selection"], prov["version"]) == ("toy MC, seed 7", "none", "v1")
    assert prov["frozen_at"].endswith("+00:00")
    assert {"git_commit", "git_dirty", "producer"} <= set(prov)
    values = load_frozen(out, expect={"n": 42, "counts": [1.5, 2.0], "nested": {"a": 1}})
    assert values == {"n": 42, "counts": [1.5, 2.0], "label": "Z", "nested": {"a": 1}}


def test_source_is_required(tmp_path: Path):
    with pytest.raises(ValueError, match="source= is required"):
        freeze({"n": 1}, tmp_path / "x.json", source="")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), np.float64("nan")])
def test_nan_and_infinity_are_refused(tmp_path: Path, bad):
    with pytest.raises(ValueError, match="NaN or infinity"):
        freeze({"x": [1.0, bad]}, tmp_path / "x.json", source="s")


def test_unserialisable_types_are_refused(tmp_path: Path):
    with pytest.raises(TypeError, match="JSON cannot store"):
        freeze({"x": object()}, tmp_path / "x.json", source="s")


def test_mismatch_lists_every_problem(tmp_path: Path):
    path = freeze({"n": 42, "sigma": 1.0, "name": "Z"}, tmp_path / "x.json", source="s")
    with pytest.raises(FrozenDataError) as err:
        load_frozen(path, expect={"n": 41, "sigma": 1.0, "name": "W", "missing": 0})
    text = str(err.value)
    assert "values.n: expected 41, found 42" in text
    assert "values.name: expected 'W', found 'Z'" in text
    assert "values.missing: missing" in text
    assert "sigma" not in text


def test_relative_tolerance(tmp_path: Path):
    path = freeze({"x": 1.0001}, tmp_path / "x.json", source="s")
    load_frozen(path, expect={"x": 1.0}, rtol=1e-3)
    with pytest.raises(FrozenDataError):
        load_frozen(path, expect={"x": 1.0})


def test_missing_file_and_foreign_json(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="run its extractor"):
        load_frozen(tmp_path / "nope.json")
    other = tmp_path / "other.json"
    other.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(FrozenDataError, match="not a manim-hep frozen file"):
        load_frozen(other)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_git_provenance_inside_a_repository(tmp_path: Path):
    repo = tmp_path / "analysis"
    repo.mkdir()
    script = repo / "extract.py"
    script.write_text(
        "from manim_hep.data import freeze\nfreeze({'n': 1}, 'out.json', source='toy')\n",
        encoding="utf-8",
    )

    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

    git("init", "-q")
    git("-c", "user.name=t", "-c", "user.email=t@example.org", "add", "extract.py")
    git("-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-q", "-m", "x")

    def run():
        subprocess.run([sys.executable, str(script)], cwd=repo, check=True)
        return json.loads((repo / "out.json").read_text(encoding="utf-8"))["provenance"]

    prov = run()
    assert len(prov["git_commit"]) == 40
    assert prov["git_dirty"] is False  # checked before out.json is written
    assert prov["producer"] == "extract.py"
    script.write_text(script.read_text(encoding="utf-8") + "# edited\n", encoding="utf-8")
    assert run()["git_dirty"] is True
