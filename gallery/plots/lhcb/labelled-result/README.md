---
title: Result plot in LHCb style
category: plots
tags: [result-plot, histogram, stacked-histogram, data-points, experiment-label, lhcb, z-boson]
authors: [Niels ter Linden]
data: synthetic
label_status: Unofficial
manim_hep: "0.1.0"
scenes: [LhcbLabelledResult]
references:
  - "mplhep (Scikit-HEP): LHCb plot style (LHCb2), colour cycle and label layout, https://github.com/scikit-hep/mplhep"
  - "S. Navas et al. (Particle Data Group), Review of Particle Physics, Phys. Rev. D 110 (2024) 030001: m_Z = 91.1876 GeV, Γ_Z = 2.4955 GeV"
---

# Result plot in LHCb style

> **Synthetic data.** Every number in this plot is made up. The label only demonstrates
> the LHCb style. Showing a real result follows LHCb's own approval rules, whatever this
> example does.

**What it shows.** A dimuon mass spectrum builds up in about six seconds:
1. the plot frame is drawn, then its ticks and axis titles fade in;
2. the stacked prediction (a falling background, with a Z peak on top) grows bin by bin
   from the baseline;
3. the data points appear from left to right;
4. the label "LHCb Unofficial" appears inside the upper right, with √s and the
   luminosity on the line below;
5. a small "Synthetic data" note appears under the label.

The axis titles keep the factors of *c*, as LHCb figures usually do: m(µ⁺µ⁻) in
GeV/*c*², and candidates per (2 GeV/*c*²).

**Physics notes.**
- The Z peak is a Breit–Wigner with the PDG mass and width, convolved with a Gaussian
  resolution of 1.5 GeV. The resolution is made up, but typical of a muon-momentum
  smearing.
- The background is a falling exponential, standing in for the Drell–Yan continuum and
  everything else.
- The "data" are a Poisson draw from the prediction with seed 20260930, so every render
  is identical.
- The yields, √s = 13.6 TeV and 5 fb⁻¹ are illustrative only.

**What the LHCb preset does.**
- `use_theme("lhcb")` takes the colour cycle from mplhep's LHCb2 style. With
  `manim-hep[mplhep]` installed it also uses the serif font, TeX Gyre Termes; without it,
  text falls back to DejaVu Sans.
- Under colour-vision deficiencies two of these colours are hard to tell apart. The
  preset keeps the official cycle and documents this exception; for a stack with many
  processes, pick colours that stay distinguishable.
- `label("lhcb", status=..., sqrt_s=..., lumi=..., loc="upper right")` sets "LHCb" and the
  status in upright roman, and puts √s and the luminosity on the next line.

**Using it for a real result.**
- Replace the synthetic arrays with numbers frozen by your analysis code
  (`manim_hep.freeze` and `load_frozen`).
- Set the status your collaboration allows for that plot. The choices are
  `"Preliminary"`, `"Unofficial"` and `"Simulation"`. manim-hep never picks one for you:
  ```python
  lab = label("lhcb", status="Preliminary", sqrt_s=13, lumi=5.4, loc="upper right", target=axes)
  ```
- Delete the "Synthetic data" note.
- Never draw or download the LHCb logo. `manim_hep.logo(path)` only loads a file you
  were given.

**Two details in the code.**
- The label and the note are built at twice their size and scaled down (`crisp_text`).
  Pango spaces small text unevenly, and TeX Gyre Termes shows it most.
- The axis title uses µ, the micro sign (U+00B5), not the Greek μ (U+03BC). TeX Gyre
  has only the former, so the Greek letter would fall back to another font.

**Render it.**

```bash
manim-hep render gallery/plots/lhcb/labelled-result/scene.py LhcbLabelledResult
```
