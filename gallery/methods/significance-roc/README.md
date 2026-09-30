---
title: Significance and ROC curve
category: methods
tags: [statistics, classifier, roc, auc, significance, cut-optimisation, machine-learning]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [RocSweep, CutSignificance]
references:
  - "G. Cowan, K. Cranmer, E. Gross, O. Vitells, Asymptotic formulae for likelihood-based tests of new physics, Eur. Phys. J. C 71 (2011) 1554, arXiv:1007.1727 (the Asimov significance Z_A)"
  - "T. Fawcett, An introduction to ROC analysis, Pattern Recognition Letters 27 (2006) 861"
  - "Seeded synthetic data (numpy default_rng(20260930))"
---

# Significance and ROC curve

**What it shows.** Two chained clips about choosing a cut on a classifier score.

1. `RocSweep`: signal (S) and background (B) score distributions. A cut c sweeps from 0 to
   1, and the parts of both histograms above the cut are shaded. The operating point
   (ε<sub>B</sub>, ε<sub>S</sub>) traces the ROC curve, and the area under it (AUC = 0.88)
   appears at the end.
2. `CutSignificance`: opens on the sweep's last frame. The ROC panel gives way to the
   expected significance Z<sub>A</sub> against the cut. The cut sweeps again, and then
   settles where Z<sub>A</sub> is largest: Z<sub>A</sub> = 3.67 at c = 0.75.

**Physics notes.**
- The scores are 50 000 seeded samples each of Beta(5, 2) for signal and Beta(2, 3) for
  background.
- The expected yields before the cut, s = 40 and b = 400 events, are schematic. After a
  cut, s = 40 ε<sub>S</sub> and b = 400 ε<sub>B</sub>; at the best cut, s ≈ 18.9 and
  b ≈ 20.9.
- Z<sub>A</sub> = √(2[(s+b) ln(1+s/b) − s]) is the Asimov median discovery significance
  (Cowan et al. 2011). For s ≪ b it reduces to s/√b.
- The curve is drawn only where at least one background event is expected (c ≤ 0.915).
  Below one expected background event the asymptotic formula is not trustworthy, and a
  "best cut" found there is an artefact.
- The shapes are chosen so that the optimum lies well inside that range. With a much
  harder signal tail, s/√b keeps growing as the cut tightens, and the optimum is then set
  only by where you stop trusting the background estimate.
- The ROC curve and the AUC use the same samples. The AUC is the probability that a
  random signal event scores higher than a random background event.

**How to adapt it.**
- Replace `SIGNAL` and `BACKGROUND` with frozen classifier scores (`manim_hep.freeze` in
  your analysis environment), and `S_TOTAL` and `B_TOTAL` with your expected yields.
- Keep the one-expected-event guard (`VALID`), or replace Z<sub>A</sub> with a formula
  that includes background systematics.
- `CutSignificance` opens on the exact last frame of `RocSweep` (`add_state`). Moving
  parts (`always_redraw`) are swapped for identical static ones before `check_order`.

**Render it.**

```bash
manim-hep render gallery/methods/significance-roc/scene.py RocSweep
manim-hep render gallery/methods/significance-roc/scene.py CutSignificance
```
