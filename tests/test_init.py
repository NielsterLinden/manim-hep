from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from manim_hep._settings import load_settings
from manim_hep.cli import main
from manim_hep.cli.init import skills_dir


def snapshot(folder: Path) -> dict[str, bytes]:
    return {
        p.relative_to(folder).as_posix(): p.read_bytes()
        for p in sorted(folder.rglob("*"))
        if p.is_file()
    }


def init(folder: Path, *extra: str) -> int:
    return main(["init", "--dir", str(folder), *extra])


def test_fresh_repository_gets_everything(awkward_dir: Path):
    assert (
        init(awkward_dir, "--agent", "both", "--root", "presentation", "--experiment", "cms") == 0
    )
    files = snapshot(awkward_dir)
    for name in (
        "manim-hep.toml",
        "AGENTS.md",
        ".gitignore",
        "CLAUDE.md",
        ".claude/settings.json",
        ".agents/skills/hep-animate/SKILL.md",
        ".agents/skills/hep-scenes/traps.md",
        "presentation/scenes/smoke_test.py",
        "presentation/storylines/.gitkeep",
        "presentation/data/.gitkeep",
    ):
        assert name in files, name
    assert (awkward_dir / "presentation" / "clips").is_dir()
    settings = load_settings(awkward_dir / "manim-hep.toml")
    assert (settings.root, settings.experiment, settings.verify) == (
        "presentation",
        "cms",
        "frames",
    )
    agents = (awkward_dir / "AGENTS.md").read_text(encoding="utf-8")
    assert "Think before coding" in agents and "<!-- >>> manim-hep -->" in agents
    assert "@AGENTS.md" in (awkward_dir / "CLAUDE.md").read_text(encoding="utf-8")
    claude = json.loads((awkward_dir / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert claude["enabledPlugins"]["manim-hep@manim-hep"] is True
    assert (
        claude["extraKnownMarketplaces"]["manim-hep"]["source"]["repo"]
        == "NielsterLinden/manim-hep"
    )
    gitignore = (awkward_dir / ".gitignore").read_text(encoding="utf-8")
    assert "# >>> manim-hep" in gitignore and ".manim-hep/" in gitignore and "clips/" in gitignore


def test_second_run_changes_nothing(awkward_dir: Path):
    assert init(awkward_dir, "--agent", "both") == 0
    before = snapshot(awkward_dir)
    assert init(awkward_dir, "--agent", "both") == 0
    assert snapshot(awkward_dir) == before


def test_no_placeholders_are_left(awkward_dir: Path):
    init(awkward_dir, "--agent", "both")
    for name, content in snapshot(awkward_dir).items():
        text = content.decode("utf-8", errors="replace")
        assert not re.search(r"<[A-Z][A-Z_]+>", text), name
        assert "{root}" not in text and "{experiment}" not in text, name


def test_foreign_content_and_crlf_survive(awkward_dir: Path):
    agents = "# My project\r\n\r\nOur own rules.\r\n"
    (awkward_dir / "AGENTS.md").write_bytes(agents.encode())
    (awkward_dir / ".gitignore").write_bytes(b"*.root\n")
    (awkward_dir / "CLAUDE.md").write_bytes(b"Be nice.")
    assert init(awkward_dir, "--agent", "claude") == 0
    new = (awkward_dir / "AGENTS.md").read_bytes()
    assert new.startswith(agents.encode())
    assert b"\n" not in new.replace(b"\r\n", b"")  # still CRLF throughout
    assert (awkward_dir / ".gitignore").read_bytes().startswith(b"*.root\n\n# >>> manim-hep\n")
    assert (awkward_dir / "CLAUDE.md").read_bytes() == b"Be nice.\n\n@AGENTS.md\n"


def test_the_block_is_replaced_not_duplicated(awkward_dir: Path):
    stale = "top\n<!-- >>> manim-hep -->\nold rules\n<!-- <<< manim-hep -->\nbottom\n"
    (awkward_dir / "AGENTS.md").write_text(stale, encoding="utf-8")
    assert init(awkward_dir) == 0
    text = (awkward_dir / "AGENTS.md").read_text(encoding="utf-8")
    assert text.startswith("top\n<!-- >>> manim-hep -->") and text.endswith(
        "<!-- <<< manim-hep -->\nbottom\n"
    )
    assert "old rules" not in text and text.count("<!-- >>> manim-hep -->") == 1


def test_a_broken_block_is_not_guessed(awkward_dir: Path, capsys):
    broken = "<!-- >>> manim-hep -->\nsomeone deleted the end marker\n"
    (awkward_dir / "AGENTS.md").write_text(broken, encoding="utf-8")
    assert init(awkward_dir) == 1
    assert (awkward_dir / "AGENTS.md").read_text(encoding="utf-8") == broken
    assert (awkward_dir / "AGENTS.md.manim-hep.new").is_file()
    assert "merge by hand" in capsys.readouterr().out


def test_settings_json_merge_keeps_user_choices(awkward_dir: Path):
    claude = awkward_dir / ".claude"
    claude.mkdir()
    original = {
        "permissions": {"allow": ["Bash(ls)"]},
        "enabledPlugins": {"manim-hep@manim-hep": False},
    }
    (claude / "settings.json").write_text(json.dumps(original, indent=4), encoding="utf-8")
    assert init(awkward_dir, "--agent", "claude") == 0
    text = (claude / "settings.json").read_text(encoding="utf-8")
    merged = json.loads(text)
    assert merged["permissions"] == original["permissions"]
    assert merged["enabledPlugins"]["manim-hep@manim-hep"] is False  # the user's choice stays
    assert "manim-hep" in merged["extraKnownMarketplaces"]
    assert '\n    "permissions"' in text  # the file's own indentation is kept


def test_invalid_settings_json_gets_a_new_file(awkward_dir: Path):
    claude = awkward_dir / ".claude"
    claude.mkdir()
    (claude / "settings.json").write_text("{ // comments are not JSON\n}", encoding="utf-8")
    assert init(awkward_dir, "--agent", "claude") == 1
    assert (claude / "settings.json.manim-hep.new").is_file()


def test_existing_files_are_never_overwritten(awkward_dir: Path):
    (awkward_dir / "manim-hep.toml").write_text('[style]\nexperiment = "lhcb"\n', encoding="utf-8")
    scenes = awkward_dir / "scenes"
    scenes.mkdir()
    (scenes / "smoke_test.py").write_text("# mine\n", encoding="utf-8")
    assert init(awkward_dir, "--experiment", "atlas") == 0
    assert load_settings(awkward_dir / "manim-hep.toml").experiment == "lhcb"
    assert (scenes / "smoke_test.py").read_text(encoding="utf-8") == "# mine\n"


def test_edited_skill_gets_a_new_file_instead_of_being_replaced(awkward_dir: Path):
    init(awkward_dir, "--agent", "codex")
    skill = awkward_dir / ".agents" / "skills" / "hep-physics" / "SKILL.md"
    skill.write_text("my edits\n", encoding="utf-8")
    assert init(awkward_dir, "--agent", "codex") == 1
    assert skill.read_text(encoding="utf-8") == "my edits\n"
    assert skill.with_name("SKILL.md.manim-hep.new").is_file()


@pytest.mark.parametrize("bad", [["--root", "../outside"], ["--experiment", "alice"]])
def test_bad_arguments(awkward_dir: Path, bad):
    assert init(awkward_dir, *bad) == 2


def test_skills_are_found():
    assert (skills_dir() / "hep-animate" / "SKILL.md").is_file()
