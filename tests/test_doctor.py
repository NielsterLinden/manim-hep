from __future__ import annotations

from pathlib import Path

import pytest

from manim_hep.cli import doctor, main


@pytest.fixture
def healthy(monkeypatch, tmp_path: Path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(doctor, "_which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(doctor, "_kpsewhich", lambda filename: True)
    monkeypatch.setattr(doctor, "_version", lambda d: "0.21.0" if d == "manim" else None)
    monkeypatch.setattr(doctor, "_import_error", lambda: None)
    monkeypatch.setattr(doctor, "detect_platform", lambda: "linux")
    return monkeypatch


def test_all_green(healthy, capsys):
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "all good" in out
    assert "[note] settings: no manim-hep.toml" in out


@pytest.mark.parametrize(
    ("platform", "hint"),
    [
        ("windows", "MiKTeX"),
        ("macos", "tlmgr install standalone"),
        ("linux", "texlive-latex-extra"),
        ("lxplus", "/cvmfs/sft.cern.ch/lcg/external/texlive"),
        ("cluster", "texlive-core package is not enough"),
    ],
)
def test_missing_latex_prints_the_platform_fix(healthy, capsys, platform, hint):
    healthy.setattr(doctor, "_which", lambda name: None if name == "latex" else "/x")
    healthy.setattr(doctor, "detect_platform", lambda: platform)
    assert main(["doctor"]) == 1
    out = capsys.readouterr().out
    assert "[FAIL] LaTeX: latex: not on PATH" in out and hint in out


def test_no_tex_reports_but_passes(healthy, capsys):
    healthy.setattr(doctor, "_which", lambda name: None if name in ("latex", "dvisvgm") else "/x")
    assert main(["doctor", "--no-tex"]) == 0
    assert "[note] LaTeX: latex" in capsys.readouterr().out


def test_missing_packages_are_named(healthy, capsys):
    healthy.setattr(doctor, "_kpsewhich", lambda f: f != "standalone.cls")
    assert main(["doctor"]) == 1
    assert "missing standalone.cls" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("versions", "message"),
    [
        ({"manim": "0.20.1"}, "need 0.21.x"),
        ({"manimgl": "1.7.2"}, "only ManimGL"),
        ({}, "not installed"),
    ],
)
def test_wrong_manim(healthy, capsys, versions, message):
    healthy.setattr(doctor, "_version", versions.get)
    assert main(["doctor"]) == 1
    assert message in capsys.readouterr().out


def test_broken_import_is_reported(healthy, capsys):
    healthy.setattr(doctor, "_import_error", lambda: "OSError: cannot load library 'pango'")
    assert main(["doctor"]) == 1
    assert "cannot load library 'pango'" in capsys.readouterr().out


def test_settings_file_is_described(healthy, capsys, tmp_path: Path):
    (tmp_path / "manim-hep.toml").write_text('[style]\nexperiment = "lhcb"\n', encoding="utf-8")
    assert main(["doctor"]) == 0
    assert "experiment lhcb" in capsys.readouterr().out


def test_real_platform_detection_is_one_of_the_known():
    assert doctor.detect_platform() in doctor.LATEX_FIX


def test_invalid_settings_are_a_failure_not_a_crash(healthy, capsys, tmp_path: Path):
    (tmp_path / "manim-hep.toml").write_text('[agent]\nverify = "maybe"\n', encoding="utf-8")
    assert main(["doctor"]) == 1
    assert "[FAIL] settings" in capsys.readouterr().out
