---
slug: higgs-potential
state: built
experiment: generic
label_status: none
---
# The Higgs potential

**Point (one sentence):** The Higgs field settles away from zero, at v, and the curvature
of the potential there is the Higgs mass.
**Context:** The theory part of a Higgs talk, after "why do particles have mass?" and
before the measurements.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Axes appear | φ [GeV], V(φ), tick labels −400 … 400 | 0.8 |
| 2 | The double well draws | the curve | 2.0 |
| 3 | A ball appears on the hump, then rolls into the right-hand minimum | the ball | 2.7 |
| 4 | The minimum is marked | v = 246.22 GeV | 1.4 |
| 5 | (clip 2) A parabola hugs the minimum | the parabola | 1.5 |
| 6 | (clip 2) The mass is the curvature | m_H² = V''(v) = 2λv² | 1.8 |
| 7 | (clip 2) The measured mass fixes λ | m_H = 125.20 GeV ⇒ λ ≈ 0.129 | 1.0 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| v | 246.22 | GeV | PDG 2024, doi:10.1103/PhysRevD.110.030001 (from G_F) | no |
| m_H | 125.20 | GeV | PDG 2024, doi:10.1103/PhysRevD.110.030001 | no |
| λ | 0.129 | — | m_H²/(2v²) from the two above | no |
| V axis scale | — | — | none shown (units of λv⁴) | yes |

## Final frame must show
- [x] The full double well, the ball resting in the right-hand minimum
- [x] The dashed marker at φ = v with its value
- [x] (clip 2) The osculating parabola and both formulas, inside the plot area
- [x] Nothing above y = 2.7

## Chaining
Entry frame: empty · Exit frame of clip 1 = entry frame of clip 2 (`state_vacuum()`),
seam checked with `manim-hep seam` · Exit frame of clip 2: `state_mass()`

## Allowed exceptions
None.

## Record (filled after rendering)
Clips: HiggsPotential (7.0 s), HiggsMass (4.4 s) · Frames inspected: first, t = 1.5,
3.5 and 5 s, last (clip 1); first, t = 1.5 and 3 s, last (clip 2) · Seam at 480p: mean
0.38, 0 blobs · Keyframes: gallery previews come from CI
