---
title: Drell–Yan production
category: theory
tags: [feynman-diagram, drell-yan, electroweak, lepton-pair]
authors: [Niels ter Linden]
data: none
label_status: none
manim_hep: "0.1.0"
scenes: [DrellYan]
references:
  - "S. D. Drell and T.-M. Yan, Phys. Rev. Lett. 25 (1970) 316, doi:10.1103/PhysRevLett.25.316"
---

# Drell–Yan production

**What it shows.** The tree-level diagram for q q̄ → γ*/Z → ℓ⁻ℓ⁺, drawn edge by edge
in reading order. The incoming quark and antiquark appear first, then the s-channel
photon or Z, then the outgoing lepton pair. Each edge gets its label as it arrives.

**Physics notes.**
- Leading order only, with time running left to right.
- Fermion-flow arrows follow the standard convention. The incoming antiquark and the
  outgoing antilepton are drawn as `antifermion` edges: they are drawn in the direction of
  time, with the arrow pointing backwards.
- The exchanged boson is drawn wavy. γ* and Z share the line; the label tells them
  apart.
- Vertex positions are schematic.

**How to adapt it.**
- Move vertices in the `V` dictionary. It is the only place positions live, so chained
  clips stay identical.
- For W production, change the final state to ℓν and the label to `W^\pm`.
- Recolour an edge after construction, e.g.
  `diagram.edge("a", "b").set_color(C.highlight)`.
- `time_per_edge` in `draw_in_order` sets the pace. About 1 s per edge reads well on a
  slide.

**Render it.**

```bash
manim-hep render gallery/theory/drell-yan/scene.py DrellYan
```
