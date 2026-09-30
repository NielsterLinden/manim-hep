from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from manim_hep.cli import main
from manim_hep.cli.lint import lint_source, onscreen_strings

GOOD = textwrap.dedent(
    """
    from manim import Create, Scene, Square, Text
    from manim_hep import label, use_theme

    C = use_theme().palette


    class Good(Scene):
        def construct(self):
            box = Square(color=C.highlight)
            self.play(Create(box))
            self.add(Text("m = 125 GeV"), label("atlas", status="Simulation"))
            self.wait(0.1)
    """
)


def codes(source: str) -> list[str]:
    return [f.code for f in lint_source(textwrap.dedent(source))]


def test_clean_scene_has_no_findings():
    assert lint_source(GOOD) == []


@pytest.mark.parametrize(
    ("source", "code"),
    [
        ("x = Square(color='#FF0000')", "MH001"),
        ("from manim import RED\nx = RED", "MH001"),
        ("import manim\nx = manim.BLUE_C", "MH001"),
        ("x = ManimColor('#123456')", "MH001"),
        ("t = Text('a', font='Arial')", "MH002"),
        ("from manimlib import *", "MH003"),
        ("import manimlib.scene", "MH003"),
        ("self.play(ShowCreation(sq))", "MH003"),
        (
            "class A(Scene):\n    CONFIG = {'x': 1}\n"
            "    def construct(self):\n        self.wait(0.1)",
            "MH003",
        ),
        ("t = Text('<b>ATLAS</b> Preliminary')", "MH005"),
        ("t = Text('CMS Work in progress')", "MH005"),
        ("p = '/afs/cern.ch/user/x/xyz/data.json'", "MH006"),
        ("p = r'C:\\Users\\someone\\talk'", "MH006"),
        ("p = 'ssh lxplus9'", "MH006"),
    ],
)
def test_each_rule_fires(source, code):
    assert code in codes(source)


@pytest.mark.parametrize(
    "construct_end",
    ["self.play(Create(sq))", "self.wait()", "self.wait(1)", "self.wait(duration=0.5)"],
)
def test_construct_must_end_on_a_short_wait(construct_end):
    source = f"class A(Scene):\n    def construct(self):\n        {construct_end}\n"
    assert codes(source) == ["MH004"]


def test_short_waits_are_fine():
    for end in ("self.wait(0.1)", "self.wait(0.2)", "self.wait(duration=0.15)"):
        assert codes(f"class A(Scene):\n    def construct(self):\n        {end}\n") == []


def test_things_that_look_close_but_are_fine():
    assert codes("t = Text('ATLAS')") == []  # the name alone is not a status label
    assert codes("x = '#hashtag'") == []
    assert codes("p = 'data/yields.json'") == []
    assert codes("colour = C.data") == []


def test_noqa():
    assert codes("x = '#FF0000'  # noqa: MH001") == []
    assert codes("x = '#FF0000'  # noqa: MH002") == ["MH001"]
    assert codes("x = '#FF0000'  # noqa") == []


def test_syntax_error_is_reported():
    assert codes("def broken(:\n") == ["MH000"]


def test_onscreen_strings():
    found = onscreen_strings(GOOD)
    assert [text for _, text in found] == ["m = 125 GeV"]
    fstring = onscreen_strings("n = 3\nt = MathTex(f'N = {n}', r'\\pm 1')\n")
    assert [text for _, text in fstring] == ["N = {…}", "\\pm 1"]


def test_command_on_files(awkward_dir: Path, capsys):
    (awkward_dir / "good.py").write_text(GOOD, encoding="utf-8")
    assert main(["lint", str(awkward_dir / "good.py")]) == 0
    out = capsys.readouterr().out
    assert "'m = 125 GeV'" in out and "0 finding(s) in 1 file(s)" in out
    (awkward_dir / "bad.py").write_text("x = RED\n", encoding="utf-8")
    assert main(["lint", str(awkward_dir)]) == 1
    assert "bad.py:1: MH001" in capsys.readouterr().out
    assert main(["lint", str(awkward_dir / "missing")]) == 2


def test_default_path_is_the_scenes_folder(awkward_dir: Path, capsys, monkeypatch):
    (awkward_dir / "manim-hep.toml").write_text('[paths]\nroot = "talk"\n', encoding="utf-8")
    scenes = awkward_dir / "talk" / "scenes"
    scenes.mkdir(parents=True)
    (scenes / "a.py").write_text("x = BLUE\n", encoding="utf-8")
    (awkward_dir / "elsewhere.py").write_text("x = RED\n", encoding="utf-8")
    monkeypatch.chdir(awkward_dir)
    assert main(["lint"]) == 1
    out = capsys.readouterr().out
    assert "a.py:1: MH001" in out and "elsewhere" not in out


def test_folders_named_like_skipped_ones_above_the_target_do_not_hide_files(tmp_path, capsys):
    project = tmp_path / "media" / "talk"  # e.g. a project inside a folder called media
    project.mkdir(parents=True)
    (project / "a.py").write_text("x = RED\n", encoding="utf-8")
    assert main(["lint", str(project)]) == 1
    assert "1 file(s)" in capsys.readouterr().out


def test_encodings_python_accepts_are_accepted(tmp_path, capsys):
    bom = tmp_path / "bom.py"
    bom.write_bytes(b"\xef\xbb\xbf" + b"x = 1\n")
    assert main(["lint", str(bom)]) == 0
    latin = tmp_path / "latin.py"
    latin.write_bytes(b"# -*- coding: latin-1 -*-\nname = '\xe9'\n")
    assert main(["lint", str(latin)]) == 0
    broken = tmp_path / "cp1252.py"
    broken.write_bytes(b"name = '\xe9'\n")  # not UTF-8 and no coding line: Python rejects it
    assert main(["lint", str(broken)]) == 1
    assert "MH000" in capsys.readouterr().out


def test_only_self_embed_is_manimgl():
    assert codes("model.embed(x)") == []
    assert "MH003" in codes("self.embed()")
