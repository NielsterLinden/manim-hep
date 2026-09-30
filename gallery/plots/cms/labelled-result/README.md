---
title: Result plot in CMS style
category: plots
tags: [result-plot, histogram, stacked-histogram, data-points, experiment-label, cms, z-boson]
authors: [Niels ter Linden]
data: synthetic
label_status: Private work
manim_hep: "0.1.0"
scenes: [CmsLabelledResult]
references:
  - "mplhep (Scikit-HEP): CMS plot style, colour cycle and label layout, https://github.com/scikit-hep/mplhep"
  - "M. Petroff, Accessible Color Sequences for Data Visualization, arXiv:2107.02270 (the CMS colour cycle)"
  - "S. Navas et al. (Particle Data Group), Review of Particle Physics, Phys. Rev. D 110 (2024) 030001: m_Z = 91.1876 GeV, Γ_Z = 2.4955 GeV"
---

# Result plot in CMS style

> **Synthetic data.** Every number in this plot is made up. The label only demonstrates
> the CMS style. Showing a real result follows CMS's own approval rules, whatever this
> example does.

**What it shows.** A dimuon mass spectrum builds up in about six seconds:
1. the plot frame is drawn, then its ticks and axis titles fade in;
2. the stacked prediction (a falling background, with a Z peak on top) grows bin by bin
   from the baseline;
3. the data points appear from left to right;
4. the CMS header appears above the frame: "**CMS** _Private work_" on the left, and
   "50 fb⁻¹ (13.6 TeV)" on the right;
5. a small "Synthetic data" note appears in the upper left corner of the plot.

**Physics notes.**
- The Z peak is a Breit–Wigner with the PDG mass and width, convolved with a Gaussian
  resolution of 1.5 GeV. The resolution is made up, but typical of a muon-momentum
  smearing.
- The background is a falling exponential, standing in for the Drell–Yan continuum and
  everything else.
- The "data" are a Poisson draw from the prediction with seed 20260930, so every render
  is identical.
- The yields, √s = 13.6 TeV and 50 fb⁻¹ are illustrative only.

**What the CMS preset does.**
- `use_theme("cms")` takes the colour cycle from mplhep's CMS style (Petroff's
  six-colour sequence). With `manim-hep[mplhep]` installed it also uses the font, TeX
  Gyre Heros; without it, text falls back to DejaVu Sans.
- `label("cms", status=..., sqrt_s=..., lumi=..., loc="above")` sets "CMS" in bold and
  the status in italics, above the top-left corner of the frame. It puts the
  luminosity, with √s in brackets, above the top-right corner.

**Using it for a real result.**
- Replace the synthetic arrays with numbers frozen by your analysis code
  (`manim_hep.freeze` and `load_frozen`).
- Set the status your collaboration allows for that plot. The choices are
  `"Preliminary"`, `"Simulation"`, `"Simulation Preliminary"`, `"Supplementary"`,
  `"Work in progress"` and `"Private work"`. manim-hep never picks one for you:
  ```python
  lab = label("cms", status="Preliminary", sqrt_s=13.6, lumi=62, loc="above", target=axes)
  ```
- For results made with CMS Open Data, use the Open Data preset. It sets "CMS Open Data"
  in plain weight and adds the non-endorsement note and the dataset DOI:
  ```python
  lab = label("cms-opendata", status=None, doi="10.7483/OPENDATA.CMS.XXXX.XXXX", target=axes)
  ```
- Delete the "Synthetic data" note.
- Never draw or download the CMS logo. `manim_hep.logo(path)` only loads a file you
  were given.

**Two details in the code.**
- The label and the note are built at twice their size and scaled down (`crisp_text`).
  Pango spaces small text unevenly, most visibly in the TeX Gyre fonts.
- The axis title uses µ, the micro sign (U+00B5), not the Greek μ (U+03BC). TeX Gyre
  has only the former, so the Greek letter would fall back to another font.

**Render it.**

```bash
manim-hep render gallery/plots/cms/labelled-result/scene.py CmsLabelledResult
```
