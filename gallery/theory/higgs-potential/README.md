---
title: The Higgs potential
category: theory
tags: [higgs, electroweak-symmetry-breaking, potential, chained-clips]
authors: [Niels ter Linden]
data: none
label_status: none
manim_hep: "0.1.0"
scenes: [HiggsPotential, HiggsMass]
references:
  - "S. Navas et al. (Particle Data Group), Phys. Rev. D 110 (2024) 030001, doi:10.1103/PhysRevD.110.030001"
  - "P. W. Higgs, Phys. Rev. Lett. 13 (1964) 508, doi:10.1103/PhysRevLett.13.508"
  - "F. Englert and R. Brout, Phys. Rev. Lett. 13 (1964) 321, doi:10.1103/PhysRevLett.13.321"
---

# The Higgs potential

**What it shows.** Two chained clips.
1. `HiggsPotential`: the double-well potential V(φ) appears. A ball leaves the
   symmetric point φ = 0 and settles in the minimum, which is marked as the vacuum
   expectation value v.
2. `HiggsMass` opens on that exact frame. A parabola with the potential's curvature at
   the minimum appears, then m_H² = V''(v) = 2λv², and the value of λ that follows from
   the measured Higgs mass.

**Physics notes.**
- The curve is the tree-level Standard Model potential along one real direction of the
  field, V(φ) = −½μ²φ² + ¼λφ⁴ with μ² = λv². Its minimum is at φ = v and its curvature
  there is V''(v) = 2μ² = 2λv² = m_H².
- The numbers come from the PDG 2024 review:
  - v = (√2 G_F)^(−1/2) = 246.22 GeV, from the Fermi constant;
  - m_H = 125.20 GeV;
  - λ = m_H² / (2v²) = 0.129 follows from these.
- The shape is drawn exactly for these values. The vertical axis carries no scale (V is
  plotted in units of λv⁴), so no number is read off it.
- The rolling ball is a picture of spontaneous symmetry breaking, not a time evolution.
  In the full theory the minimum is a circle of degenerate vacua; the clip shows one real
  slice.

**How to adapt it.**
- The plot position lives in the anchor dict `A`. `build_axes()` is shared by both
  clips, which is what makes the seam between them invisible (check it with
  `manim-hep seam`).
- To show the tilt of a "wrong" vacuum, add a linear term to `potential()`.
- A follow-up clip can open on `state_mass()` with `add_state`.

**Render it.**

```bash
manim-hep render gallery/theory/higgs-potential/scene.py HiggsPotential
manim-hep render gallery/theory/higgs-potential/scene.py HiggsMass
manim-hep seam .manim-hep/work/higgs-potential/higgs-potential.mp4 .manim-hep/work/higgs-mass/higgs-mass.mp4
```
