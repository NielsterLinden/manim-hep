---
title: Result plot in ATLAS style
category: plots
tags: [result-plot, histogram, stacked-histogram, data-points, experiment-label, atlas, z-boson]
authors: [Niels ter Linden]
data: synthetic
label_status: Work in Progress
manim_hep: "0.1.0"
scenes: [AtlasLabelledResult]
references:
  - "mplhep (Scikit-HEP): ATLAS plot style, colour cycle and label layout, https://github.com/scikit-hep/mplhep"
  - "S. Navas et al. (Particle Data Group), Review of Particle Physics, Phys. Rev. D 110 (2024) 030001: m_Z = 91.1876 GeV, Γ_Z = 2.4955 GeV"
---

# Result plot in ATLAS style

> **Synthetic data.** Every number in this plot is made up. The label only demonstrates
> the ATLAS style. Showing a real result follows ATLAS's own approval rules, whatever
> this example does.

**What it shows.** A dimuon mass spectrum builds up in about six seconds:
1. the plot frame is drawn, then its ticks and axis titles fade in;
2. the stacked prediction (a falling background, with a Z peak on top) grows bin by bin
   from the baseline;
3. the data points appear from left to right;
4. the label "**_ATLAS_** Work in Progress" appears inside the upper left, with √s and
   the luminosity on the line below;
5. a small "Synthetic data" note appears under the label.

**Physics notes.**
- The Z peak is a Breit–Wigner with the PDG mass and width, convolved with a Gaussian
  resolution of 1.5 GeV. The resolution is made up, but typical of a muon-momentum
  smearing.
- The background is a falling exponential, standing in for the Drell–Yan continuum and
  everything else.
- The "data" are a Poisson draw from the prediction with seed 20260930, so every render
  is identical.
- The yields, √s = 13.6 TeV and 50 fb⁻¹ are illustrative only.

**What the ATLAS preset does.**
- `use_theme("atlas")` takes the colour cycle from mplhep's ATLAS style (the Okabe–Ito
  colours). With `manim-hep[mplhep]` installed it also uses the font, TeX Gyre Heros;
  without it, text falls back to DejaVu Sans.
- `label("atlas", status=..., sqrt_s=..., lumi=...)` sets "ATLAS" in bold italic and the
  status in regular weight, and puts √s and the luminosity on the next line. It places
  the label inside the upper left of the plot frame.

**Using it for a real result.**
- Replace the synthetic arrays with numbers frozen by your analysis code
  (`manim_hep.freeze` and `load_frozen`).
- Set the status your collaboration allows for that plot. The choices are
  `"Internal"`, `"Preliminary"`, `"Simulation"`, `"Simulation Internal"`,
  `"Simulation Preliminary"` and `"Work in Progress"`, or `status=None` for the bare
  "ATLAS" label of a published paper. manim-hep never picks one for you:
  ```python
  lab = label("atlas", status="Preliminary", sqrt_s=13.6, lumi=140, target=axes)
  ```
- Delete the "Synthetic data" note.
- Never draw or download the ATLAS logo. It needs written approval, and
  `manim_hep.logo(path)` only loads a file you were given.

**Two details in the code.**
- The label and the note are built at twice their size and scaled down (`crisp_text`).
  Pango spaces small text unevenly, most visibly in the TeX Gyre fonts.
- The axis title uses µ, the micro sign (U+00B5), not the Greek μ (U+03BC). TeX Gyre
  has only the former, so the Greek letter would fall back to another font.

**Render it.**

```bash
manim-hep render gallery/plots/atlas/labelled-result/scene.py AtlasLabelledResult
```
