from __future__ import annotations

from pathlib import Path

import pytest

from manim_hep._settings import Settings, find_settings, load_settings

FULL = """
[paths]
root = "presentation"

[style]
experiment = "cms"
title_band = 2.5
keep_out = [[-7.1, 0.2, -5.85, 4.0]]

[agent]
storyline = "markdown"
verify = "review"
branch = "worktree"
commit = "auto"
"""


def test_defaults_without_a_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = load_settings()
    assert s == Settings()
    assert (s.experiment, s.storyline, s.verify, s.branch, s.commit) == (
        "generic",
        "artifact",
        "frames",
        "feature",
        "ask",
    )
    assert s.title_band == 2.7


def test_upward_search_and_all_keys(tmp_path: Path):
    (tmp_path / "manim-hep.toml").write_text(FULL, encoding="utf-8")
    deep = tmp_path / "presentation" / "scenes"
    deep.mkdir(parents=True)
    assert find_settings(deep) == tmp_path / "manim-hep.toml"
    s = load_settings(search_from=deep)
    assert s.project_dir == tmp_path.resolve()
    assert s.root_dir == (tmp_path / "presentation").resolve()
    assert (s.experiment, s.title_band) == ("cms", 2.5)
    assert s.keep_out == ((-7.1, 0.2, -5.85, 4.0),)
    assert (s.storyline, s.verify, s.branch, s.commit) == ("markdown", "review", "worktree", "auto")


def test_search_from_a_file_path(tmp_path: Path):
    (tmp_path / "manim-hep.toml").write_text("", encoding="utf-8")
    scene = tmp_path / "scene.py"
    scene.write_text("", encoding="utf-8")
    assert find_settings(scene) == tmp_path / "manim-hep.toml"


@pytest.mark.parametrize(
    ("toml", "message"),
    [
        ('[agent]\nverify = "sometimes"', "verify = 'sometimes' is not allowed"),
        ('[agent]\ncommit = "push"', "commit = 'push' is not allowed"),
        ('[style]\nexperiment = "alice"', "style.experiment = 'alice' is not allowed"),
        ('[style]\ntitle_band = "high"', "title_band must be a number"),
        ("[style]\nkeep_out = [[1, 2, 3]]", r"\[x0, y0, x1, y1\]"),
    ],
)
def test_invalid_values_are_explained(tmp_path: Path, toml, message):
    path = tmp_path / "manim-hep.toml"
    path.write_text(toml, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        load_settings(path)


def test_unknown_keys_warn(tmp_path: Path):
    path = tmp_path / "manim-hep.toml"
    path.write_text('[agent]\nverfy = "none"\n[extra]\nx = 1\n', encoding="utf-8")
    with pytest.warns(UserWarning) as record:
        load_settings(path)
    messages = [str(w.message) for w in record]
    assert any("unknown key agent.verfy" in m for m in messages)
    assert any("unknown section [extra]" in m for m in messages)
