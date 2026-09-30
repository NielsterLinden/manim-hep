---
slug: significance-roc
state: built
experiment: generic
label_status: none
---
# Significance and ROC curve

**Point (one sentence):** Every cut on a classifier score is a trade-off between signal
and background efficiency, and the best cut is the one that maximises the expected
significance.
**Context:** A methods talk, after the classifier has been introduced and before the
result. Clip 2 follows clip 1 without a cut.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Score panel and ROC panel with the diagonal appear | tick labels, axis titles (score, fraction / 0.04, ε_B, ε_S) | 1.2 |
| 2 | The background and signal histograms are drawn and named | B, S | 1.7 |
| 3 | The cut appears at 0, with the accepted parts shaded and the operating point at (1, 1) | c | 0.6 |
| 4 | The cut sweeps to 1; the operating point traces the ROC curve | c | 6.5 |
| 5 | The area under the curve | AUC = 0.88 | 0.8 |
| 6 | (clip 2) ROC panel gives way to Z_A against the cut; the cut returns to 0 | Z_A formula, c, Z_A, tick labels | 1.5 |
| 7 | The cut sweeps to 0.915; Z_A(c) is traced with a point | c | 5.0 |
| 8 | The cut and the point slide back to the maximum | c | 1.4 |
| 9 | The optimum is marked | Z_A = 3.67, c = 0.75 | 0.9 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Signal and background scores | Beta(5, 2), Beta(2, 3), 50 000 each | none | seeded synthetic data (seed 20260930) | yes |
| Yields before the cut | s = 40, b = 400 | events | chosen | yes |
| AUC | 0.88 | none | computed from the samples | yes |
| Best cut, Z_A there | c = 0.75, Z_A = 3.67 | none, σ | computed (Asimov formula, arXiv:1007.1727) | yes |
| Last cut drawn | 0.915 (one expected background event) | none | computed | yes |

## Final frame must show
- [x] Clip 1: both histograms, the cut at 1, the full ROC curve with the operating point at
  (0, 0), and the AUC
- [x] Clip 2: the cut at the best value with the accepted parts shaded, the Z_A curve with
  its maximum marked, and the values Z_A and c
- [x] Nothing above the title band (y > 2.7)

## Chaining
Entry frame: empty (clip 1); clip 1's last frame (clip 2) · Exit frame: ROC with AUC
(clip 1); the optimum on the Z_A curve (clip 2)

## Allowed exceptions
The Z_A formula above the right panel in clip 2; it is physics notation.

## Record (filled after rendering)
Clips: RocSweep (10.9 s), CutSignificance (8.9 s), 480p15 drafts · Frames inspected:
RocSweep at 2.5, 4.5, 7 s and the last frame; CutSignificance at 1, 4, 7.2 s and the last
frame; the seam between the two clips passes `manim-hep seam` · Keyframes: gallery
previews come from CI
