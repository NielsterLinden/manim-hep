# Manim trap list (Manim Community Edition 0.21, cairo renderer)

Each of these cost at least one render round in real talks. **(0.21 test)** means a test in
manim-hep's suite re-checks it on every release; the rest are from 0.20.1 experience and
still apply to 0.21 as far as we know.

1. **The last frame comes one step before the end state (0.21 test).** A clip that ends on
   `self.play(...)` rests at alpha = (n−1)/n, so a fade-out is still a little visible.
   End every clip with `self.wait(0.1)`; `manim-hep lint` checks this (MH004).
2. **`Indicate` and `.animate(rate_func=there_and_back)` leave the object at peak scale.**
   `finish()` snaps to the method's target whatever the rate function. For a pulse, animate
   a throwaway `m.copy()` and remove it after the play.
3. **`LaggedStart`/`AnimationGroup` over children of an already-added `VGroup` re-stacks
   the z-order.** Without `group=` they wrap the children in a new group on top. Pass
   `group=parent`. `check_order` catches the symptom.
4. **Every `self.wait()` leaves an empty placeholder `Mobject` in `self.mobjects`.**
   `check_order` ignores these; your own z-order guards must too.
5. **The cairo static-frame cache drops side-effect repaints.** An object repainted by
   *another* object's updater may never be redrawn. Put the updater on the object it changes.
6. **`AnimationGroup.begin()` begins every child up front.** A per-child side effect must
   happen in that child's own `interpolate`, not in `begin()`. (manim-hep's
   `FeynmanDiagram.draw_in_order` relies on this to keep undrawn edges hidden.)
7. **`tracker.animate.set_value()` adds the `ValueTracker` to the scene.** Remove it after
   the play (`check_order` ignores trackers).
8. **`Scene.remove(group)` does not remove children re-parented by a `LaggedStart`.**
   Remove the children.
9. **Never pass a plain list as `FadeIn(..., shift=...)`.** `list * -1` is `[]` and the
   render *hangs* with no error. Use `UP * 0.3` or a NumPy array.
10. **`MathTex.get_parts_by_tex` (plural) may not exist.** `get_part_by_tex` returns only
    the first match, and `substrings_to_isolate` does not split `.submobjects`. Split the
    formula into separate strings and index them instead.
11. **`ImageMobject.set_opacity` scales `orig_alpha_pixel_array`.** If you mutate
    `pixel_array`, keep that in sync.
12. **ManimCE only.** `Create`, not `ShowCreation`; no `CONFIG` dicts, no `self.embed()`.
    Check any borrowed snippet: the APIs of 3b1b's ManimGL diverged years ago and the error
    messages don't say so (lint MH003).
13. **`MoveAlongPath` needs `path.copy()`** when the same path is also being `Create`d in
    the group.
14. **Never put `Flash` inside a `Succession`.** Its spokes appear at the start and hang
    there until their slot; give flashes their own `play`.
15. **Concurrent `MathTex` compiles race on the SVG cache** and fail with
    `FileNotFoundError`. Render one scene at a time; `manim-hep render` holds a lock.
16. **`VMobject.scale(f, scale_stroke=True)` on a group sets every member's stroke to the
    group's width × f.** Scale strokes per submobject instead.
17. **`squish_rate_func` inside a `LaggedStart` with `lag_ratio > 0` mis-times.** Use
    explicit windows.
18. **`-qh` works in 0.21 (0.21 test).** Older notes said to write `--quality h`; either is
    fine.
19. **H.264 (yuv420p) shifts decoded colours slightly** (`#00A6D6` becomes `#00A4D6`). To
    match a slide shape to a clip, sample the decoded frame.
20. **A bare `texlive-core` is not enough for `MathTex`.** You need `standalone.cls`,
    `preview.sty` and `dvisvgm`; `manim-hep doctor` checks them.
21. **Windows: the first `Text` of every render takes a few seconds.** ManimPango loads the
    bundled fonts once per process. That is expected; later texts are fast.
22. **Small `Text` gets uneven letter spacing.** Pango hints glyphs badly at small sizes,
    worst in serif fonts. manim-hep's labels, ticks and titles render at size 48 and scale
    down. Do the same in scenes: `Text("...", font_size=48).scale(0.4)`.
23. **The experiment fonts have no Greek.** TeX Gyre Heros and Termes (the ATLAS, CMS and
    LHCb themes) lack Greek letters, so Pango falls back to another font. In `Text` and axis
    titles, use the micro sign `µ` (U+00B5) for "mu", or pass a `MathTex` title.
24. **`AnimationGroup(..., group=parent)` keeps `check_order` happy only if every child
    animates a member of `parent`'s family.** A temporary `VGroup` built around some parts
    ends up in the scene as a stray object.
