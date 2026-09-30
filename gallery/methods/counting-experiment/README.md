---
title: Counting experiment
category: methods
tags: [statistics, significance, counting, poisson, sqrt-n]
authors: [Niels ter Linden]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [CountingTally, CountingSignificance]
references:
  - "G. Cowan, K. Cranmer, E. Gross, O. Vitells, Asymptotic formulae for likelihood-based tests of new physics, Eur. Phys. J. C 71 (2011) 1554, arXiv:1007.1727"
  - "Particle Data Group, Review of Particle Physics, chapter 40: Statistics"
  - "Seeded synthetic data (numpy default_rng(20260930))"
---

# Counting experiment

**What it shows.** Two chained clips about finding a rare signal by counting.

1. `CountingTally`: collisions are recorded one by one, and each event fills one cell of a
   tally grid. Most events are background (grey) and a few are signal (vermillion). The
   counts N<sub>B</sub> and N<sub>S</sub> run up, and Z = S/√B is computed from them.
2. `CountingSignificance`: opens on the tally's last frame. It shows Z against the number of
   recorded events N. The measured curve wanders around the expectation Z ∝ √N and crosses
   3σ and then 5σ.

**Physics notes.**
- Every event comes from one seeded random sequence. Each event is signal with probability
  p = 0.06, which is schematic.
- With the seed used here, the grid holds 231 background and 9 signal events, so Z = 0.59.
  The curve crosses 3σ after about 2100 events and 5σ after about 6400.
- The colours are simulation truth. A real experiment cannot tell signal from background
  event by event; it compares the observed count with the expected background.
- Z = S/√B is the usual approximation for S ≪ B. When the background is small, use the
  Asimov formula Z = √(2[(S+B) ln(1+S/B) − S]) (Cowan et al. 2011).
- For expected counts S = pN and B = (1 − p)N, Z grows like √N. Doubling the data gives
  √2 more significance, not twice as much.

**How to adapt it.**
- `P_SIGNAL` sets how rare the signal is. `COLS` and `ROWS` set the size of the tally grid.
  Change the seed in `RNG` for another draw.
- `N_ONE_BY_ONE` sets how many events fly in individually before the grid fills.
- For real numbers, freeze the observed counts and expected background with
  `manim_hep.freeze` in your analysis environment, and load them with
  `load_frozen(..., expect=...)`.
- `CountingSignificance` opens on the exact last frame of `CountingTally` (`add_state`), so
  the two clips chain without a visible cut. Check a joint with `manim-hep seam`.

**Render it.**

```bash
manim-hep render gallery/methods/counting-experiment/scene.py CountingTally
manim-hep render gallery/methods/counting-experiment/scene.py CountingSignificance
```
