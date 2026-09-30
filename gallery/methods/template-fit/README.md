---
title: Template fit
category: methods
tags: [statistics, likelihood, template-fit, signal-strength, profile-likelihood, stack]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [TemplateFit]
references:
  - "G. Cowan, K. Cranmer, E. Gross, O. Vitells, Asymptotic formulae for likelihood-based tests of new physics, Eur. Phys. J. C 71 (2011) 1554, arXiv:1007.1727"
  - "Particle Data Group, Review of Particle Physics, chapter 40: Statistics (likelihood intervals)"
  - "Seeded synthetic data (numpy default_rng(20260940))"
---

# Template fit

**What it shows.** One clip, `TemplateFit`, about fitting a signal strength μ.
- The left panel shows the data n next to a stacked prediction: a background template b,
  plus a signal template s scaled by μ.
- μ sweeps from 0 to 2. The signal layer grows, and −2ΔlnL(μ) is traced on the right.
- μ then settles at the best fit, μ̂ = 1.02<sup>+0.34</sup><sub>−0.33</sub>. The 1σ
  interval is read off where −2ΔlnL = 1.
- The data never move; only the prediction changes.

**Physics notes.**
- The templates are synthetic. The background is an exponential (slope 40 GeV, 1500
  events in 100–160 GeV) with a fixed normalisation. The signal is a Gaussian at 125 GeV
  with σ = 3 GeV (55 events at μ = 1).
- The data are one Poisson draw of b + s, with μ<sub>true</sub> = 1.
- The seed was chosen to give a typical draw: μ̂ lies within 0.1σ of μ<sub>true</sub>.
  Across seeds, μ̂ scatters by about ±0.35, as the interval says.
- −2 ln L(μ) = 2 Σ<sub>i</sub> [ν<sub>i</sub>(μ) − n<sub>i</sub> ln ν<sub>i</sub>(μ)], with
  ν<sub>i</sub> = b<sub>i</sub> + μ s<sub>i</sub>.
- μ̂ is found with Newton's method. The curve and the interval are exact on a fine grid;
  the curve is not forced to be a parabola.
- Here the only free parameter is μ. A real fit profiles the nuisance parameters too
  (background normalisation, energy scale, ...), which widens the curve.
- √(−2ΔlnL(0)) ≈ 3.2 is the significance of the excess over the background-only
  hypothesis (asymptotically; Cowan et al. 2011).

**How to adapt it.**
- Replace `S_TEMPLATE`, `B_TEMPLATE` and `DATA` with frozen histograms from your analysis
  (`manim_hep.freeze`/`load_frozen`), and keep `nll2` unless your fit has more parameters.
- The μ-dependent objects use `become` in updaters. The stack, the readout, the curve and
  the point stay the same mobjects throughout, so `check_order` can name them in the
  final frame.

**Render it.**

```bash
manim-hep render gallery/methods/template-fit/scene.py TemplateFit
```
