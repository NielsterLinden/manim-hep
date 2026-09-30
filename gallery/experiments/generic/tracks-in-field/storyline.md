---
slug: tracks-in-field
state: built
experiment: generic
label_status: none
---
# Tracks in a magnetic field

**Point (one sentence):** In a magnetic field the direction of the bending tells the
charge and the radius tells the momentum.
**Context:** Explains how a tracker measures charge and momentum, before any result that
relies on them.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | The field region appears, filled with ⊙; the field value | ⊙, B = 3.8 T | 1.0 |
| 2 | μ⁺ and μ⁻ with equal pT leave the vertex and bend apart | μ⁺, μ⁻, pT = 1 GeV | 2.5 |
| 3 | A 20 GeV μ⁺ goes almost straight | μ⁺, pT = 20 GeV | 2.0 |
| 4 | The relation and the two radii | R = pT/(0.3\|q\|B), units, R values | 1.0 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| B | 3.8 | T | typical large solenoid | yes |
| Field-region radius | 1.1 | m | typical tracker radius | yes |
| pT (pair, stiff track) | 1, 20 | GeV | chosen for contrast | yes |
| R(1 GeV), R(20 GeV) | 0.88, 17.6 | m | R = pT / (0.3 \|q\| B) (PDG detector review) | no |

## Final frame must show
- [x] ⊙ field symbols across the region, and B = 3.8 T
- [x] μ⁺ bending clockwise and μ⁻ anticlockwise, equal radii
- [x] The 20 GeV track almost straight
- [x] The formula with units and both radii

## Chaining
Entry frame: empty · Exit frame: all of the above (no chained clip)

## Allowed exceptions
None.

## Record (filled after rendering)
Clip: TracksInField (6.6 s) · Frames inspected: first, 2.0 s, 3.8 s and last ·
Keyframes: gallery previews come from CI
