---
slug: atlas-labelled-result
state: built
experiment: atlas
label_status: Work in Progress
---
# Result plot in ATLAS style

**Point (one sentence):** A dimuon mass spectrum builds up in ATLAS style: the prediction, then the data, then a label with an explicit status.
**Context:** The gallery example of the ATLAS preset. In a talk it would follow a slide on the Z → μμ selection.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | The frame is drawn; ticks and axis titles fade in | tick labels 70–110 and 0–2000; "m_µµ [GeV]", "Events / 2 GeV" | 1.4 |
| 2 | The stacked prediction grows from the baseline, bin by bin | nothing new | 1.8 |
| 3 | Data points appear from left to right | nothing new | 1.8 |
| 4 | The experiment label appears | "ATLAS Work in Progress", "√s = 13.6 TeV, 50 fb⁻¹" | 0.8 |
| 5 | The note appears | "Synthetic data" | 0.5 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Z mass | 91.1876 | GeV | PDG 2024 (Phys. Rev. D 110, 030001) | no |
| Z width | 2.4955 | GeV | PDG 2024 (Phys. Rev. D 110, 030001) | no |
| Mass resolution | 1.5 | GeV | made up | yes |
| Signal and background yields | 4000 and 900 | events | made up | yes |
| Background slope | 0.045 | 1/GeV | made up | yes |
| Data | Poisson draw from the prediction, seed 20260930 | events | synthetic | yes |
| √s | 13.6 | TeV | illustrative | yes |
| Integrated luminosity | 50 | fb⁻¹ | illustrative | yes |

## Final frame must show
- [x] The frame with inward ticks on all four sides; tick labels and axis titles in the ATLAS font
- [x] The stacked prediction (background below, Z peak on top), drawn under the frame lines
- [x] Data points with capless error bars
- [x] "ATLAS Work in Progress" inside the upper left, with √s and luminosity on the line below
- [x] "Synthetic data" under the label: smaller than the tick labels, in the muted colour
- [x] Nothing above y = 2.7 (the title band)

## Chaining
Entry frame: empty · Exit frame: the complete plot

## Allowed exceptions
- The two-word note "Synthetic data" under the label. It is required for honesty, because the data are synthetic.

## Record (filled after rendering)
Clip: AtlasLabelledResult, 6.4 s · Frames inspected: first, 1.4 s, 3.2 s, 5.0 s and last (480p), plus the last frame at 1080p · Keyframes: gallery previews come from CI
