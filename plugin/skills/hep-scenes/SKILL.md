---
name: hep-scenes
description: Write or edit Manim Community Edition scene code for HEP talks on the manim-hep building blocks (themes, FeynmanDiagram, DataAxes and histograms, BarrelSlice, tracks and signatures, experiment labels, state-first builders with add_state, check_order and place), with pacing, text and 3D guidance and a trap list of Manim pitfalls. Use when writing or fixing a scene, turning an approved storyline into code, or when Manim behaves unexpectedly.
---

# Writing scenes on manim-hep

- **API:** [api.md](api.md) (exact signatures).
- **Traps:** [traps.md](traps.md). Read it before debugging anything odd.
- **Examples:** the manim-hep gallery (`gallery/<category>/<slug>/scene.py`). Start from the
  closest one.

## File skeleton

```python
"""<Clip title>: <one sentence>.

Physics honesty: what is schematic or exaggerated; where the numbers come from.
"""
from __future__ import annotations

import numpy as np
from manim import Create, FadeIn, Scene, linear

from manim_hep import add_state, check_order, place, use_theme

theme = use_theme()          # experiment from manim-hep.toml, or use_theme("cms")
C = theme.palette            # C.ink, C.data, C.theory, C.detector, C.highlight, C.muted, C.cycle
A = {"plot": (1.0, (1.2, -0.5)), "detector": (0.8, (-4.0, -0.6))}   # all anchors in one dict
RNG = np.random.default_rng(20260930)                                # seeded: renders repeat


def state_final() -> dict:
    """The clip's last frame without animation; dict order is drawing order."""
    ...

class ClipName(Scene):
    def construct(self):
        s = state_final()
        ...                              # animate the objects in s into place
        check_order(self, s)             # exactly these objects, in this order
        self.wait(0.1)                   # end on the last change
```

Import explicitly (no `from manim import *` mixed with `manimlib`). Scenes import only
`manim`, `manim_hep`, NumPy and the standard library. Data comes in through
`load_frozen`, never through ROOT, uproot or pandas at render time.

## State first, then animate

- **One pure builder per end state.** It returns a dict of mobjects in drawing order, and
  nothing else happens in it.
- **Opening a chained clip:** start clip N+1 with `add_state(self, state_clip_n)`, so its
  first frame is clip N's last frame. Check the joint with `manim-hep seam`.
- **Closing a clip:** end with `check_order(self, state)`. It fails the render if a stray
  object remains (a leftover `Flash`, a tracker) or if the z-order changed.
- **Placement:** every position goes through `place(mobject, A[...])`, so rebuilt states
  match exactly.
- **Order:** build order is z-order. Add backgrounds first and labels last.

## Pacing

- **One idea per clip, 4–13 s.** Calm is 10–13 s, brisk 6–9 s. Reviewers almost always ask
  for faster.
- **Particles fly with `rate_func=linear`**, about 2 s per track; easing makes them look
  like they accelerate.
- **Prefer a `Transform` flow to staged waits.** No holds inside a clip: the speaker talks
  over the last frame.
- **End with `self.wait(0.1)` after the last change.** Anything longer is dead time in the
  deck.

## Text and LaTeX

- **Allowed text:** physics symbols, units, tick labels and numbers. `MathTex` is for
  math. `Text`/`MarkupText` pick up the theme font; never pass `font=`.
- **Morphing formulas:** to morph between two different `MathTex` strings, cross-fade
  (`FadeOut` + `FadeIn`). `Transform` jumbles the glyphs unless the strings share structure.
- **Picking parts of a `MathTex`:** use `get_part_by_tex` (singular), or split the formula
  into separate strings (`MathTex("E", "=", "mc^2")`) and index them.
- **Speed:** the first `Text` of a render on Windows takes a few seconds (font loading);
  after that it is fast.

## Plots, detectors, diagrams

- **Plots:** position `DataAxes` first (`move_frame_to`), then build the content through
  `axes.c2p`. Histograms are step outlines. Stacks morph with `Transform` (fixed point
  count). Keep the data points still while the prediction changes.
- **Detector:** `BarrelSlice` is about 6 units tall. Scale it and move it to
  `theme.content_center` to stay below the title band. Build it inside-out
  (`slice.layers` is already in that order).
- **Tracks:** `track(pt, charge, field)`. With `field > 0` (out of the screen), positive
  charges bend clockwise. Signatures come from `signature(kind, detector, phi=...)`.
- **Feynman diagrams:** keep one vertex dict. Time runs left to right; keep spectators
  straight, and do not cross lines that need not cross. `draw_in_order()` keeps the diagram
  one group.

## 3D (when a flat view is not enough)

- **Rotate the object, not the camera.** An identity-pose `ThreeDScene` at z = 0 matches a 2D
  scene pixel for pixel, so 2D→3D chains stay seamless.
- **Text in 3D:** use `add_fixed_in_frame_mobjects`.
- **Face opacities stack as 1 − (1 − o)ⁿ:** use 0.03–0.10 per face.
- **Keep every point well short of the focal distance (20):** fly in with a dolly (shift
  toward +z), not a camera move.
- **Many points:** use a `PMobject`/`DotCloud` rather than hundreds of spheres.

## When you need something new

1. Write it in the scene file first.
2. It moves into `manim_hep` only when a second scene needs it, and it arrives with tests.
3. Never change an existing helper's signature or default: add a new name instead.
