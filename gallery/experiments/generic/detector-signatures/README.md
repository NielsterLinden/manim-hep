---
title: Detector signatures
category: experiments
tags: [detector, barrel-slice, signatures, tracks, calorimeter, muon-system, neutrino]
authors: [Niels ter Linden]
data: none
label_status: none
manim_hep: "0.1.0"
scenes: [DetectorSignatures, DetectorBuild]
references:
  - "S. Navas et al. (Particle Data Group), Review of Particle Physics, Phys. Rev. D 110, 030001 (2024): reviews 'Particle detectors at accelerators' and 'Passage of particles through matter'"
---

# Detector signatures

**What it shows.** Two chained clips. `DetectorBuild` builds a generic barrel detector
inside out: beam pipe, tracker, solenoid, electromagnetic calorimeter (ECAL), hadronic
calorimeter (HCAL) and muon system. `DetectorSignatures` opens on that exact frame.
One by one, it then shows how five particles appear in the detector:

| Particle | Signature |
|---|---|
| electron, e⁻ | a track that stops in the ECAL with a shower |
| muon, μ⁺ | a track through everything, with hits in the muon stations |
| photon, γ | no track (dashed), then an ECAL shower |
| jet | several tracks, with ECAL and HCAL deposits |
| neutrino, ν | nothing: it escapes (dashed arrow) |

**Physics notes.**
- The detector is a neutral cartoon, not any experiment's geometry. The layer order
  (solenoid between tracker and ECAL) is one common choice. ATLAS puts its solenoid in
  front of the calorimeters; CMS puts it outside the HCAL.
- Track curvatures follow the charge correctly for a field pointing out of the screen:
  the e⁻ curls anticlockwise and the μ⁺ clockwise. The transverse momenta are only a
  few GeV, so the bending is visible. Leptons from W and Z decays (pT ≈ 40 GeV) would
  look almost straight at this scale.
- Energy deposits are drawn as wedges with a fixed size, not proportional to energy.

**How to adapt it.**
- Change `PARTICLES` to pick kinds, angles and charges (`signature` also knows `tau1`
  and `tau3`).
- Pass `radii={...}` to `BarrelSlice` to move layers, e.g. the solenoid outside the HCAL.
- Change the anchor `A["detector"]` (scale, centre) to make room for other content.

**Render it.**

```bash
manim-hep render gallery/experiments/generic/detector-signatures/scene.py DetectorBuild
manim-hep render gallery/experiments/generic/detector-signatures/scene.py DetectorSignatures
manim-hep seam .manim-hep/work/detector-build/detector-build.mp4 \
               .manim-hep/work/detector-signatures/detector-signatures.mp4
```
