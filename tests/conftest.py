from __future__ import annotations

import shutil
from pathlib import Path

import pytest


def pytest_collection_modifyitems(config, items):
    if shutil.which("latex") is None:
        skip = pytest.mark.skip(reason="LaTeX (`latex`) is not on PATH")
        for item in items:
            if "latex" in item.keywords:
                item.add_marker(skip)


@pytest.fixture
def awkward_dir(tmp_path: Path) -> Path:
    """A working folder whose name has a space and a non-ASCII character."""
    path = tmp_path / "with space é"
    path.mkdir()
    return path


@pytest.fixture
def generic_theme():
    """Activate the generic theme for a test and restore it afterwards."""
    from manim_hep.style import use_theme

    theme = use_theme("generic")
    yield theme
    use_theme("generic")
