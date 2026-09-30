---
title: Tracks in a magnetic field
category: experiments
tags: [tracking, magnetic-field, curvature, charge, transverse-momentum]
authors: [Niels ter Linden]
data: none
label_status: none
manim_hep: "0.1.0"
scenes: [TracksInField]
references:
  - "S. Navas et al. (Particle Data Group), Review of Particle Physics, Phys. Rev. D 110, 030001 (2024): review 'Particle detectors at accelerators' (momentum measurement, pT = 0.3 B R)"
---

# Tracks in a magnetic field

**What it shows.** A field region with the field pointing out of the screen (⊙). A μ⁺
and a μ⁻ with the same transverse momentum (pT = 1 GeV) leave the vertex together.
They bend in opposite directions: the **sign of the curvature gives the charge**. Then
a μ⁺ with pT = 20 GeV hardly bends at all: the **radius gives the momentum**. The
relation R = pT / (0.3 |q| B) and the two radii close the clip.

**Physics notes.**
- The force q **v** × **B** turns positive charges clockwise and negative charges
  anticlockwise when **B** points out of the screen. `manim_hep.track` uses this sign
  convention: `field > 0` means out of the screen.
- R = pT / (0.3 |q| B) with R in m, pT in GeV and B in T. For B = 3.8 T this gives
  0.88 m for 1 GeV and 17.6 m for 20 GeV. The field region has a radius of 1.1 m.
  Both B and the region size are typical of a large solenoid and are schematic here.
- The tracks are exact circles. Energy loss and multiple scattering are ignored.

**How to adapt it.**
- Change `FIELD_T`, `LOW_PT` and `HIGH_PT`; the formula lines recompute the radii.
- `REGION_M` and `REGION` set the size of the field region in metres and scene units,
  and with them the scale.
- Set `FIELD_T` negative to show a field into the screen. Draw ⊗ instead of ⊙ then.

**Render it.**

```bash
manim-hep render gallery/experiments/generic/tracks-in-field/scene.py TracksInField
```
