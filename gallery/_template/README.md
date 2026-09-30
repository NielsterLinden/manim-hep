---
title: Template example
category: methods
tags: [template]
authors: [Your Name]
data: synthetic
label_status: none
manim_hep: "0.1.0"
scenes: [TemplateRing, TemplateDot]
references:
  - "Where the physics and every number come from (DOI, arXiv, PDG, or 'seeded synthetic data')"
---

# Template example

**What it shows.** One or two sentences: the single idea of the clip.

**Physics notes.** What is exact, what is schematic, and the sources.

**How to adapt it.**
- Change the anchors in `A` to move things.
- Change the seed in `RNG` for another random draw.
- Swap the synthetic numbers for frozen data (`manim_hep.load_frozen`).

**Render it.**

```bash
manim-hep render gallery/<category>/<slug>/scene.py TemplateRing
```
