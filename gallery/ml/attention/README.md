---
title: Self-attention, step by step
category: ml
tags: [transformer, attention, softmax, machine-learning, chained-clips]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [AttentionScores, AttentionUpdate]
references:
  - "A. Vaswani et al., Attention Is All You Need, NeurIPS 2017, arXiv:1706.03762"
---

# Self-attention, step by step

**What it shows.** One attention head acting on four tokens, in two chained clips.
1. `AttentionScores`: every query meets every key. The 4×4 grid fills with the scores
   s_ij = q_i·k_j/√d, then each row turns into softmax weights a_ij.
2. `AttentionUpdate` opens on that frame and follows token 2:
   - its row of weights travels to the value vectors v_1 … v_4;
   - each vector shrinks by its weight;
   - the weighted vectors pour together into the new representation
     z_2 = Σ_j a_2j v_j.

**Numbers.** All synthetic. The query, key and value vectors (d = 3) are drawn from a
normal distribution with seed 98, and everything on screen is computed from them: the
scores, the softmax weights (each row sums to 1) and z_2. Cell shading increases with
the number in the cell, and bar heights are proportional to the vector components.

**How to adapt it.**
- Change the seed in `RNG` for other numbers, or `ROW` to follow another token.
- `A` holds every position. The grid and the value vectors are built by `cell_rows()`
  and `value_vector()`.
- For a causal (decoder) mask, set the scores above the diagonal to −∞ before the
  softmax; those cells then show 0.00.

**Render it.**

```bash
manim-hep render gallery/ml/attention/scene.py AttentionScores
manim-hep render gallery/ml/attention/scene.py AttentionUpdate
```
