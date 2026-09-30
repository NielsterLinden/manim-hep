"""Extractor: freeze the numbers one clip needs. Runs in the ANALYSIS environment.

Copy this file next to your analysis code (not into the Manim scene), fill in the
three marked parts, and run it:

    python extract_zmumu.py

It writes <root>/data/<name>.json with provenance (source, selection, version,
time, script, git commit and dirty flag). The scene then loads it with
manim_hep.load_frozen(path, expect={...}) and never touches ROOT or pandas.

Install manim-hep in the analysis environment too (`pip install manim-hep`), or copy
the file with the provenance by hand in the same JSON layout:
{"values": {...}, "provenance": {...}}.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from manim_hep.data import freeze

OUT = Path("presentation/data/zmumu.json")  # 1. where the scene expects it

# 2. Read your analysis output. Anything goes here: uproot, ROOT, pandas, HDF5, ...
#    import uproot
#    masses = uproot.open("ntuple.root")["events"]["m_mumu"].array(library="np")
masses = np.array([])  # replace with the real array

edges = np.linspace(60.0, 120.0, 31)
counts, _ = np.histogram(masses, bins=edges)

# 3. Check the numbers the storyline shows before freezing them.
assert counts.sum() == len(masses), "events outside the histogram range"

freeze(
    {
        "edges": edges,
        "counts": counts,
        "n_events": int(counts.sum()),
    },
    OUT,
    source="ntuple production v3 (the file or dataset you read)",
    selection="two opposite-charge muons, pT > 25 GeV, |eta| < 2.4",
    version="analysis tag or commit",
)
print(f"froze {int(counts.sum())} events to {OUT}")
