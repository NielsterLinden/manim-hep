from __future__ import annotations

import subprocess
import sys
from importlib.metadata import entry_points

import manim_hep


def test_version():
    assert manim_hep.__version__ == "0.1.0"


def test_manim_plugin_entry_point():
    names = {ep.name: ep.value for ep in entry_points(group="manim.plugins")}
    assert names.get("manim_hep") == "manim_hep"


def test_console_script():
    scripts = {ep.name: ep.value for ep in entry_points(group="console_scripts")}
    assert scripts.get("manim-hep") == "manim_hep.cli:main"


def test_import_does_not_pull_in_manim():
    code = "import sys, manim_hep; print('manim' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "False"


def test_manim_import_loads_plugin_without_error():
    code = "import manim; print('ok')"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert "Missing Plugins" not in out.stdout + out.stderr
