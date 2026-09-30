"""The gallery contract (spec §8.2): every example folder must pass these checks."""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import manim_hep
from manim_hep.cli.frames import FRAME_HEIGHT, FRAME_WIDTH, ink_fraction, scan
from manim_hep.cli.lint import lint_source

GALLERY = Path(__file__).parents[1] / "gallery"
CATEGORIES = {"theory", "methods", "experiments", "plots", "ml"}
REQUIRED = {"title", "category", "tags", "authors", "data", "label_status", "manim_hep", "scenes"}
ALLOWED_IMPORTS = {"manim", "manim_hep", "numpy", *sys.stdlib_module_names}

EXAMPLES = sorted(p.parent for p in GALLERY.rglob("scene.py"))
IDS = [str(p.relative_to(GALLERY)).replace("\\", "/") for p in EXAMPLES]


def header(folder: Path) -> dict:
    text = (folder / "README.md").read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{folder}/README.md must start with a YAML header"
    return yaml.safe_load(text.split("---\n", 2)[1])


def scene_classes(folder: Path) -> list[str]:
    tree = ast.parse((folder / "scene.py").read_text(encoding="utf-8"))
    return [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(isinstance(b, ast.Name) and b.id.endswith("Scene") for b in node.bases)
    ]


def test_there_are_examples():
    assert any("_template" not in i for i in IDS)


@pytest.mark.parametrize("folder", EXAMPLES, ids=IDS)
def test_readme_header(folder: Path):
    meta = header(folder)
    missing = REQUIRED - set(meta)
    assert not missing, f"README header lacks {sorted(missing)}"
    rel = folder.relative_to(GALLERY).parts
    if rel[0] != "_template":
        assert meta["category"] == rel[0] and meta["category"] in CATEGORIES
    assert meta["data"] in {"synthetic", "none"}
    assert str(meta["manim_hep"]) == manim_hep.__version__
    assert isinstance(meta["tags"], list) and isinstance(meta["authors"], list)
    assert meta["label_status"] is not None
    assert meta["scenes"] and set(meta["scenes"]) <= set(scene_classes(folder))


@pytest.mark.parametrize("folder", EXAMPLES, ids=IDS)
def test_scene_imports_and_lint(folder: Path):
    source = (folder / "scene.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            roots.add(node.module.split(".")[0])
    assert roots <= ALLOWED_IMPORTS, (
        f"imports outside manim/manim_hep/stdlib: {roots - ALLOWED_IMPORTS}"
    )
    assert lint_source(source, str(folder / "scene.py")) == []


@pytest.mark.render
@pytest.mark.parametrize("folder", EXAMPLES, ids=IDS)
def test_example_renders_and_keeps_the_title_band_clear(folder: Path, tmp_path: Path):
    for scene in header(folder)["scenes"]:
        cmd = [sys.executable, "-m", "manim", "render", "-ql", "--progress_bar", "none"]
        cmd += ["--media_dir", str(tmp_path), str(folder / "scene.py"), scene]
        out = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        assert out.returncode == 0, (out.stdout + out.stderr)[-3000:]
        clip = next(tmp_path.rglob(f"{scene}.mp4"))
        last = scan(clip).frames["last"]
        band = (-FRAME_WIDTH / 2, 2.7, FRAME_WIDTH / 2, FRAME_HEIGHT / 2)
        assert ink_fraction(last, band, (255, 255, 255)) <= 0.001, (
            f"{scene} draws in the title band"
        )
