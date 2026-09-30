---
slug: histogram-fill
state: built
experiment: generic
label_status: none
---
# Filling a histogram

**Point (one sentence):** A histogram is events counted one by one; with enough of them
a peak appears.
**Context:** Before the first result plot of a talk, so the audience knows what every
bin means.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Empty axes | tick labels, axis titles | 0.8 |
| 2 | One event's mass drops into its bin; the bin grows by one | m_ℓℓ value, N = 1 | 1.4 |
| 3 | Four more entries, one at a time | N = 2…5 | 2.5 |
| 4 | The y axis zooms out (12 → 60) | tick labels | 0.8 |
| 5 | The rest rains in; the peak forms | N = 150 | 3.2 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| m_Z (centre of the draws) | 91.1876 | GeV | PDG 2024 | no |
| Width of the draws | 2.8 | GeV | stands for width ⊗ resolution | yes |
| Masses, including the one shown (91.2 GeV) | seeded draws | GeV | numpy seed 7 | yes |
| N | 150 | events | synthetic sample size | yes |

## Final frame must show
- [x] A peaked histogram near 91 GeV on a 0–60 axis
- [x] N = 150 inside the plot frame
- [x] Axis titles, and nothing above the title band

## Chaining
Entry frame: empty · Exit frame: the filled histogram (no chained clip)

## Allowed exceptions
None.

## Record (filled after rendering)
Clip: HistogramFill (9.3 s) · Frames inspected: first, 1.0 s, 2.3 s, 4.4 s, 5.2 s, 6.3 s
and last · Keyframes: gallery previews come from CI
