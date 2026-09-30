---
slug: stack-data-ratio
state: built
experiment: generic
label_status: none
---
# Stacked prediction, data and ratio

**Point (one sentence):** When the prediction is corrected, it moves onto the data;
the data themselves never move.
**Context:** In a talk about a calibration or a background estimate, just before the
final data/prediction comparison.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Empty main and ratio panels | tick labels, axis titles | 0.8 |
| 2 | Data points appear, left to right; legend row | Data | 1.2 |
| 3 | The prediction grows in, peak too high; legend rows | Z/γ* → μμ, tt̄ | 1.2 |
| 4 | Ratio points show the S shape; hold | ratio points | 1.2 |
| 5 | The correction: the stack slides onto the data, the ratio flattens | Δm = −0.8 GeV | 1.5 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| m_Z, Γ_Z | 91.1876, 2.4952 | GeV | PDG 2024 | no |
| Resolution | 1.6 | GeV | chosen | yes |
| Z and tt̄ yields | 40 000, 5 000 | events | chosen | yes |
| Scale bias Δm | 0.8 | GeV | invented | yes |
| Data | Poisson draws | events | numpy seed 20260930 | yes |

## Final frame must show
- [x] Data points exactly where they appeared in beat 2
- [x] Prediction on the data; ratio points near 1
- [x] Legend with Data, Z/γ* → μμ and tt̄; Δm = −0.8 GeV
- [x] Axis titles on both panels; nothing above the title band

## Chaining
Entry frame: empty · Exit frame: the corrected comparison (no chained clip)

## Allowed exceptions
The legend word "Data", as standard plot furniture.

## Record (filled after rendering)
Clip: StackDataRatio (6.0 s) · Frames inspected: first, 1.5 s, 3.6 s, 4.6 s and last ·
Keyframes: gallery previews come from CI
