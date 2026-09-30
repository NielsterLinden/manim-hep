---
slug: counting-experiment
state: built
experiment: generic
label_status: none
---
# Counting experiment

**Point (one sentence):** A rare signal only becomes significant by counting many
collisions, and the significance grows like √N.
**Context:** A methods talk, straight after the physics motivation and before the first
result plot. Clip 2 follows clip 1 without a cut.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Beam line, collision point, empty tally grid and zero counts appear | N_B = 0, N_S = 0 | 1.4 |
| 2 | Eight events fly from the collision point into the grid, one at a time | the counts | 3.5 |
| 3 | The rest of the grid fills at a steady rate; the counts follow the grid | the counts | 4.6 |
| 4 | Z is computed from the counts | Z = S/√B = 0.59 | 0.8 |
| 5 | (clip 2) The grid gives way to a plot of Z against N; the formula moves into the plot | N, Z, tick labels, Z = S/√B | 1.3 |
| 6 | 3σ and 5σ reference lines | 3σ, 5σ | 0.9 |
| 7 | Our 240 events become one point; the measured Z(N) is drawn to N = 8000 | the point | 4.6 |
| 8 | The expectation Z ∝ √N is drawn dashed | none | 1.3 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Signal probability per event | 0.06 | none | chosen | yes |
| Events in the grid | 240 | events | chosen | yes |
| N_B, N_S in the grid | 231, 9 | events | seeded synthetic data (seed 20260930) | yes |
| Z in the grid | 0.59 | σ | computed from N_S and N_B | yes |
| Events in the curve | 8000 | events | chosen | yes |

## Final frame must show
- [x] Clip 1: the full grid with the signal cells in the highlight colour
- [x] Clip 1: N_B, N_S and Z, with the counts matching the grid
- [x] Clip 2: Z against N with the 3σ and 5σ lines, the measured and expected curves, and
  the point for the grid's events
- [x] Nothing above the title band (y > 2.7)

## Chaining
Entry frame: empty (clip 1); clip 1's last frame (clip 2) · Exit frame: tally with Z (clip 1);
the Z(N) plot (clip 2)

## Allowed exceptions
None.

## Record (filled after rendering)
Clips: CountingTally (11.4 s), CountingSignificance (8.3 s), 480p15 drafts ·
Frames inspected: CountingTally at 1.5, 3.5, 6.5 s and the last frame; CountingSignificance
at 1, 3, 6 s and the last frame; the seam between the two clips passes `manim-hep seam` ·
Keyframes: gallery previews come from CI
