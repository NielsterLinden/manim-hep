---
title: Filling a histogram
category: plots
tags: [histogram, statistics, invariant-mass, z-boson]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [HistogramFill]
references:
  - "m_Z = 91.1876 GeV: S. Navas et al. (Particle Data Group), Phys. Rev. D 110, 030001 (2024)"
---

# Filling a histogram

**What it shows.** How a mass histogram comes about.
1. One event gives one number, its dilepton mass (shown). That number drops into its
   bin and the bin grows by one entry.
2. Four more events follow, faster.
3. The y axis zooms out from 12 to 60 events; the tick marks stay put and only their
   labels change.
4. The rest of the sample rains in until 150 entries form a peak.

A counter N keeps track of the entries.

**Physics notes.**
- The 150 masses are seeded synthetic draws from a Gaussian around
  m_Z = 91.1876 GeV. The Gaussian's 2.8 GeV width stands in for the natural width and
  the detector resolution together, so this is not a real Z line shape.
- The rain shows 40 falling entries as the counter runs to 150. The falling dots
  illustrate the fill; they are not one dot per entry.

**How to adapt it.**
- Use your own values in `MASSES` (e.g. from `load_frozen("data/masses.json")`), and
  set `EDGES`, the axis titles and `Y_ZOOM`/`Y_FULL`. Keep both axes at the same
  number of ticks, so the frame does not change during the zoom.
- `N_SINGLE` and `N_RAIN` set how many entries are shown one by one and in the rain.

**Render it.**

```bash
manim-hep render gallery/plots/general/histogram-fill/scene.py HistogramFill
```
