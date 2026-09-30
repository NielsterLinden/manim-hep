from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("hygiene", ROOT / "scripts" / "hygiene.py")
hygiene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hygiene)


@pytest.mark.parametrize(
    "line",
    [
        "data = '/afs/cern.ch/user/x/someone/file.root'",
        "path = r'C:\\Users\\someone\\talk'",
        "ssh someone@lxplus9.cern.ch",
        "host = 'lxplus9.cern.ch'",
        "cache = '/data/atlas/users/someone/cache'",
    ],
)
def test_private_patterns_are_caught(tmp_path: Path, line: str):
    f = tmp_path / "x.py"
    f.write_text(line + "\n", encoding="utf-8")
    assert hygiene.check_file(f, "x.py")


@pytest.mark.parametrize(
    "line",
    [
        "run it on lxplus with TeX Live from CVMFS",
        "export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux:$PATH",
        "see https://opendata.cern.ch/record/414",
        "data/yields.json",
    ],
)
def test_public_text_passes(tmp_path: Path, line: str):
    f = tmp_path / "x.md"
    f.write_text(line + "\n", encoding="utf-8")
    assert hygiene.check_file(f, "x.md") == []


def test_media_and_size(tmp_path: Path):
    clip = tmp_path / "clip.mp4"
    clip.write_bytes(b"\0" * 10)
    big = tmp_path / "big.json"
    big.write_bytes(b" " * 1_100_000)
    assert "media file" in hygiene.check_file(clip, "clip.mp4")[0]
    assert "over the 1 MB limit" in hygiene.check_file(big, "big.json")[0]


def test_this_repository_is_clean():
    if subprocess.run(["git", "status"], cwd=ROOT, capture_output=True).returncode != 0:
        pytest.skip("not a git checkout")
    assert hygiene.main(ROOT) == 0
