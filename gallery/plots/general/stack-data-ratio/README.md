---
title: Stacked prediction, data and ratio
category: plots
tags: [stacked-histogram, data-mc, ratio-panel, calibration, z-boson]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [StackDataRatio]
references:
  - "m_Z = 91.1876 GeV and Γ_Z = 2.4952 GeV: S. Navas et al. (Particle Data Group), Phys. Rev. D 110, 030001 (2024)"
---

# Stacked prediction, data and ratio

**What it shows.** A dimuon mass plot built in the order a physicist reads it.
1. The empty frame and ratio panel appear, then the data points. The data never move
   again.
2. The stacked prediction (Z/γ* → μμ on top of tt̄) grows in, but its peak sits
   0.8 GeV too high, as a biased muon momentum scale would place it. The ratio
   data/prediction shows the typical S shape: above 1 below the peak, below 1 above it.
3. The scale correction (Δm = −0.8 GeV) slides the prediction onto the data, and the
   ratio flattens to 1. Only the prediction and the ratio move.

**Physics notes.**
- The numbers are seeded synthetic, not a measurement:
  - the Z shape is a Breit–Wigner with the PDG m_Z and Γ_Z, smeared by a 1.6 GeV
    Gaussian resolution;
  - tt̄ is a falling exponential;
  - the data are Poisson draws from the corrected prediction;
  - the 0.8 GeV bias is invented.
- The sample (40 000 Z plus 5 000 tt̄) is large enough that Poisson noise does not hide
  the S shape.
- The error bars are √N (the Poisson approximation); the ratio error is √N divided by
  the prediction. There is no uncertainty band on the prediction.

**How to adapt it.**
- Replace `DATA`, `Z_TRUE`, `Z_BIASED` and `TT` with frozen numbers from your analysis
  (`load_frozen`). `stack_hist` layers go from the bottom up.
- Keep the layer list the same in both stacks, so `Transform` morphs bin by bin.
- A missing background that grows in is the same move: start that layer at zero.
- The legend is built in the scene with `make_legend`; change its rows there.

**Render it.**

```bash
manim-hep render gallery/plots/general/stack-data-ratio/scene.py StackDataRatio
```
