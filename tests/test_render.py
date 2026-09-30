from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from manim_hep.cli import main
from manim_hep.cli.render import kebab, next_version, render_lock

SCENES = textwrap.dedent(
    """
    from manim import Create, Scene, Square
    from manim_hep import use_theme

    theme = use_theme()


    class GoodClip(Scene):
        def construct(self):
            self.play(Create(Square(1.5)), run_time=0.4)
            self.wait(0.1)


    class HighClip(Scene):
        def construct(self):
            self.play(Create(Square(1.0).move_to([0, 3.4, 0])), run_time=0.4)
            self.wait(0.1)
    """
)


def test_kebab():
    assert kebab("DrellYan") == "drell-yan"
    assert kebab("ROCCurve") == "roc-curve"
    assert kebab("Clip2Detector") == "clip2-detector"


def test_next_version(tmp_path: Path):
    assert next_version(tmp_path, "drell-yan") == 1
    (tmp_path / "drell-yan_v1.mp4").touch()
    (tmp_path / "drell-yan_v3.mp4").touch()
    (tmp_path / "drell-yan-other_v7.mp4").touch()
    assert next_version(tmp_path, "drell-yan") == 4


def test_lock_can_be_taken_twice_in_a_row(tmp_path: Path):
    lock = tmp_path / ".manim-hep" / "render.lock"
    with render_lock(lock):
        pass
    with render_lock(lock):
        pass


def test_missing_file(tmp_path: Path, capsys):
    assert main(["render", str(tmp_path / "nope.py"), "X"]) == 2


@pytest.mark.render
def test_render_frames_warnings_and_delivery(awkward_dir: Path, capsys, monkeypatch):
    (awkward_dir / "manim-hep.toml").write_text('[paths]\nroot = "talk"\n', encoding="utf-8")
    scene = awkward_dir / "talk" / "scenes" / "clips.py"
    scene.parent.mkdir(parents=True)
    scene.write_text(SCENES, encoding="utf-8")
    monkeypatch.chdir(awkward_dir)

    assert main(["render", str(scene), "GoodClip", "--frames", "0.2"]) == 0
    out = capsys.readouterr().out
    work = awkward_dir / ".manim-hep" / "work" / "good-clip"
    for name in ("good-clip_first.png", "good-clip_t0.2.png", "good-clip_last.png"):
        assert (work / name).is_file()
    assert "safe areas: clear" in out

    assert main(["render", str(scene), "HighClip"]) == 0
    assert "WARNING: title band has ink" in capsys.readouterr().out

    assert main(["render", str(scene), "GoodClip", "--final"]) == 0
    assert main(["render", str(scene), "GoodClip", "--final"]) == 0
    clips = awkward_dir / "talk" / "clips"
    assert sorted(p.name for p in clips.iterdir()) == [
        "good-clip_v1.mp4",
        "good-clip_v1_final.png",
        "good-clip_v2.mp4",
        "good-clip_v2_final.png",
    ]


@pytest.mark.render
def test_failed_render_reports_and_writes_no_frames(awkward_dir: Path, capsys, monkeypatch):
    scene = awkward_dir / "broken.py"
    scene.write_text(
        "from manim import Scene\nclass Broken(Scene):\n    def construct(self)\n", "utf-8"
    )
    monkeypatch.chdir(awkward_dir)
    assert main(["render", str(scene), "Broken"]) == 1
    out = capsys.readouterr().out
    assert "render FAILED" in out
    assert not list((awkward_dir / ".manim-hep" / "work" / "broken").glob("*.png"))


def test_unknown_scene_is_an_error_before_rendering(tmp_path: Path, capsys):
    scene = tmp_path / "clips.py"
    scene.write_text(SCENES, encoding="utf-8")
    assert main(["render", str(scene), "GoodClp"]) == 2
    assert "no scene 'GoodClp'" in capsys.readouterr().out


def test_imported_scenes_are_accepted(tmp_path: Path):
    from manim_hep.cli.render import scene_names

    f = tmp_path / "s.py"
    f.write_text("from shared import Opening as Intro\nclass A: pass\n", encoding="utf-8")
    assert scene_names(f) == {"Intro", "A"}


def test_clips_from_a_worktree_go_to_the_main_checkout(tmp_path: Path):
    import shutil
    import subprocess

    from manim_hep.cli.render import delivery_root

    if shutil.which("git") is None:
        pytest.skip("git not installed")
    main_repo = tmp_path / "talk"
    main_repo.mkdir()

    def git(*args, cwd=main_repo):
        subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)

    git("init", "-q")
    (main_repo / "f").write_text("x", encoding="utf-8")
    git("add", "f")
    git("-c", "user.name=t", "-c", "user.email=t@example.org", "commit", "-q", "-m", "x")
    git("worktree", "add", "-q", str(tmp_path / "wt"), "-b", "anim/x")
    inside = tmp_path / "wt" / "presentation"
    inside.mkdir()
    assert delivery_root(inside) == (main_repo / "presentation").resolve()
    assert delivery_root(main_repo) == main_repo


def test_a_file_system_without_locking_runs_unlocked(tmp_path: Path, monkeypatch, capsys):
    import errno
    import os

    def no_locks(*args, **kwargs):
        raise OSError(errno.ENOLCK, "No locks available")

    if os.name == "nt":
        import msvcrt

        monkeypatch.setattr(msvcrt, "locking", no_locks)
    else:
        import fcntl

        monkeypatch.setattr(fcntl, "flock", no_locks)
    with render_lock(tmp_path / "render.lock", timeout=1):
        pass
    assert "not serialised" in capsys.readouterr().out
