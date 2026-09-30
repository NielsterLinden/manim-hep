---
slug: backprop
state: built
experiment: generic
label_status: none
---
# Backpropagation in a small network

**Point (one sentence):** The error at the output flows back through the network and tells
every weight which way to move, and one step lowers the loss.
**Context:** Before a result that uses a neural network, for an audience that has not
trained one.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | The network appears; thickness shows each weight | x_1, x_2, ŷ | 1.0 |
| 2 | The inputs light up | 0.8, −0.4 | 0.6 |
| 3 | Signals flow to the hidden layer, which lights up | 0.29, 0.58, 0.86 | 1.6 |
| 4 | Signals flow to the output | 0.51 | 1.5 |
| 5 | Target and loss | y = 1, L = ½(ŷ − y)² = 0.119 | 1.3 |
| 6 | (clip 2) Gradients flow back, output layer first | ∂L/∂w | 2.0 |
| 7 | (clip 2) Every weight takes a step; the lines change thickness | w ← w − η ∂L/∂w | 1.2 |
| 8 | (clip 2) A new forward pass: the prediction improves and the loss drops | 0.29, 0.59, 0.85, 0.59, L = 0.085 | 1.9 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| weights | normal(0, 1) | — | seeded synthetic (seed 120) | yes |
| x, y, η | (0.8, −0.4), 1, 2 | — | chosen for the example | yes |
| activations, ŷ, L, gradients | computed | — | from the numbers above | no |

## Final frame must show
- [x] (clip 1) The network with the input, hidden and output values, the target and the loss
- [x] (clip 2) Updated line thicknesses, the gradient symbol, the update rule, the new values
  and the lower loss
- [x] Nothing above y = 2.7

## Chaining
Entry frame: empty · Exit frame of clip 1 (`state_forward()`) = entry frame of clip 2

## Allowed exceptions
None.

## Record (filled after rendering)
Clips: BackpropForward (6.1 s), BackpropBackward (5.3 s) · Frames inspected:
first, t = 2, 3, 3.5 and 4 s, last · Seam at 480p: mean 0.48, 0 blobs · Keyframes: gallery
previews come from CI
