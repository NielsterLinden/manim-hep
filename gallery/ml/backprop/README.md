---
title: Backpropagation in a small network
category: ml
tags: [neural-network, backpropagation, gradient-descent, machine-learning, chained-clips]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [BackpropForward, BackpropBackward]
references:
  - "D. E. Rumelhart, G. E. Hinton and R. J. Williams, Nature 323 (1986) 533, doi:10.1038/323533a0"
---

# Backpropagation in a small network

**What it shows.** A 2-3-1 network learns from one example, in two chained clips.
1. `BackpropForward`: the inputs x = (0.8, −0.4) flow forward. The hidden nodes light up
   with their activations, the network predicts ŷ = 0.51, and the loss against the target
   y = 1 appears.
2. `BackpropBackward` opens on that frame:
   - gradients flow back through the network, output layer first;
   - every weight takes one gradient-descent step, so the lines change thickness;
   - a new forward pass gives ŷ = 0.59, and the loss drops from 0.119 to 0.085.

**Numbers.** All synthetic and all computed, nothing typed in by hand.
- The weights come from a normal distribution with seed 120. There are no biases.
- The activations are sigmoids, ŷ = σ(w₂·h), and L = ½(ŷ − y)².
- The gradients follow the chain rule; the step uses η = 2.
- Line thickness grows with |w| (width 1 + 3|w|). Hidden and output nodes are shaded by their
  activation; the inputs get a fixed light shade.
- The first-layer weights move very little (by 0.07 at most), which is the familiar
  behaviour of gradients shrinking as they pass back through sigmoids. Their thickness
  change is barely visible; that is intended.

**How to adapt it.**
- Change `X_IN`, `Y_TRUE`, `ETA` or the seed. Every number on screen follows.
- The layer positions and label anchors live in `A`.
- For a deeper network, extend `EDGE_ENDS`, `node_centre` and `forward()`.

**Render it.**

```bash
manim-hep render gallery/ml/backprop/scene.py BackpropForward
manim-hep render gallery/ml/backprop/scene.py BackpropBackward
```
