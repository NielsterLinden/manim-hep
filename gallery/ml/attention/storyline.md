---
slug: attention
state: built
experiment: generic
label_status: none
---
# Self-attention, step by step

**Point (one sentence):** Each token becomes a mix of all tokens, weighted by how well its
query matches their keys.
**Context:** The machine-learning part of a talk that uses a transformer (e.g. jet tagging
or event classification), before the architecture diagram.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Queries and keys appear around an empty grid | q_1 … q_4, k_1 … k_4 | 0.8 |
| 2 | The grid fills row by row with scores | score values, one decimal | 1.8 |
| 3 | The score formula appears | s_ij = q_i·k_j/√d | 0.6 |
| 4 | Each row becomes softmax weights | weights, two decimals | 2.4 |
| 5 | The softmax formula appears | a_ij = e^{s_ij} / Σ_j' e^{s_ij'} | 0.6 |
| 6 | (clip 2) Row 2 is picked out, the rest dims | frame around row 2 | 1.0 |
| 7 | (clip 2) The value vectors appear | v_1 … v_4 | 0.8 |
| 8 | (clip 2) Row 2's weights move under the values | the four weights | 1.0 |
| 9 | (clip 2) The values shrink by their weights and pour into z_2 | bars | 2.7 |
| 10 | (clip 2) The result is named | z_2 = Σ_j a_2j v_j | 0.7 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| q, k, v vectors | normal(0, 1), d = 3 | — | seeded synthetic (seed 98) | yes |
| scores, weights, z_2 | computed | — | from the vectors above | no |

## Final frame must show
- [x] (clip 1) The full 4×4 grid of weights, each row summing to 1, and both formulas
- [x] (clip 2) Row 2 framed, the four value vectors with their weights, and z_2 with its
  formula
- [x] Nothing above y = 2.7

## Chaining
Entry frame: empty · Exit frame of clip 1 (`state_weights()`) = entry frame of clip 2

## Allowed exceptions
None.

## Record (filled after rendering)
Clips: AttentionScores (6.3 s), AttentionUpdate (6.3 s) · Frames inspected: first,
t = 2.5 and 4.5 s, last of each · Seam at 480p: mean 0.67, 0 blobs · Keyframes: gallery
previews come from CI
