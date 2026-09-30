"""The agent layer: plugin manifest, marketplace, skills and agents (spec §7, §9.2)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

import manim_hep

ROOT = Path(__file__).parents[1]
PLUGIN = ROOT / "plugin"
SKILLS = sorted(p.parent for p in (PLUGIN / "skills").glob("*/SKILL.md"))
AGENTS = sorted((PLUGIN / "agents").glob("*.md"))
EXPECTED_SKILLS = {
    "hep-animate",
    "hep-storyline",
    "hep-scenes",
    "hep-render-verify",
    "hep-physics",
    "hep-experiment-style",
    "hep-plots-data",
    "hep-setup",
    "hep-contribute",
}
EXPECTED_AGENTS = {"scene-builder", "render-verifier", "physics-checker", "plot-recreator"}


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path} needs YAML frontmatter"
    return yaml.safe_load(text.split("---\n", 2)[1])


def test_plugin_version_matches_the_package():
    manifest = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "manim-hep"
    assert manifest["version"] == manim_hep.__version__


def test_marketplace_points_at_the_plugin():
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert market["name"] == "manim-hep"
    [entry] = market["plugins"]
    assert entry["name"] == "manim-hep" and entry["source"] == "./plugin"


def test_all_skills_and_agents_are_there():
    assert {p.name for p in SKILLS} == EXPECTED_SKILLS
    assert {p.stem for p in AGENTS} == EXPECTED_AGENTS


@pytest.mark.parametrize("folder", SKILLS, ids=[p.name for p in SKILLS])
def test_skill_frontmatter(folder: Path):
    meta = frontmatter(folder / "SKILL.md")
    assert meta["name"] == folder.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["name"]) and len(meta["name"]) <= 64
    assert 1 <= len(meta["description"]) <= 1024
    assert re.search(r"\bUse (when|before|after)\b", meta["description"])


@pytest.mark.parametrize("folder", SKILLS, ids=[p.name for p in SKILLS])
def test_skill_links_resolve(folder: Path):
    text = (folder / "SKILL.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+)\)", text):
        if "://" not in target:
            assert (folder / target).is_file(), f"{folder.name} links to missing {target}"


@pytest.mark.parametrize("path", AGENTS, ids=[p.stem for p in AGENTS])
def test_agent_frontmatter(path: Path):
    meta = frontmatter(path)
    assert meta["name"] == path.stem
    assert meta["description"] and meta["tools"]
    assert "model" not in meta, "agents inherit the session model"


def test_critics_are_read_only():
    for name in ("render-verifier", "physics-checker"):
        tools = {
            t.strip() for t in frontmatter(PLUGIN / "agents" / f"{name}.md")["tools"].split(",")
        }
        assert not tools & {"Write", "Edit"}


def test_rules_block_is_marked_for_init():
    text = (PLUGIN / "skills" / "hep-animate" / "SKILL.md").read_text(encoding="utf-8")
    start, end = text.index("<!-- rules:start -->"), text.index("<!-- rules:end -->")
    rules = text[start:end]
    for rule in ("Think before coding", "Simplicity first", "Surgical changes", "Goal-driven"):
        assert rule in rules
    assert "andrej-karpathy-skills" in rules


def test_plugin_is_installable_everywhere():
    assert not (PLUGIN / "bin").exists(), "a top-level bin/ blocks claude.ai and Cowork installs"
    assert sum(1 for p in PLUGIN.rglob("*") if p.is_file()) < 5000
