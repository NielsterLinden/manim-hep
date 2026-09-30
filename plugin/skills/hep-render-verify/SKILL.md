---
name: hep-render-verify
description: Render and verify manim-hep scenes with manim-hep render, inspect the first, mid and last frames, run lint, check the title band and keep-out areas, check seams between chained clips, and report what was checked. Use after building or changing a scene, before delivering a clip, when manim-hep.toml sets a verify level, or when the user asks to render, check or review an animation.
---

# Render, look, fix

You never assume a scene looks right: you render it and look at the frames.

## Commands

| Command | What it does |
|---|---|
| `manim-hep render <file> <Scene>` | Low-quality render (854×480, 15 fps) in `.manim-hep/work/<slug>/`: writes the MP4, plus `<slug>_first.png` and `<slug>_last.png`. Warns if the title band or a keep-out area gets ink in any frame. One render at a time (it waits for a lock) |
| `... --frames 1.5,4` | Also writes the frames on screen at those times (`<slug>_t1.5.png`, ...) |
| `... --final` | 1920×1080 at 60 fps; delivers `<root>/clips/<slug>_vK.mp4` and `_vK_final.png` with the next free K. Never overwrites |
| `manim-hep lint [paths]` | House rules (MH001–MH006), plus a list of every on-screen string |
| `manim-hep seam A.mp4 B.mp4` | Checks that B starts exactly where A ended |

Render **only the scene you changed**. Never run two renders at once.

## Verification levels (`agent.verify` in `manim-hep.toml`)

| Level | Do | Stop when |
|---|---|---|
| `none` | Write the code and tell the user the render command | code written |
| `render` | `manim-hep render` | it succeeds (at most 3 fix rounds) |
| `frames` | as `render`, plus: look at the first, last and one frame per beat (`--frames` at the beat midpoints) against the storyline's *Final frame must show*; run `lint`; the safe-area line must say "clear" | all criteria pass, or 3 rounds, then report |
| `review` | as `frames`, plus: read-only reviews by `physics-checker` and `render-verifier` (Claude Code) or the `hep-physics` checklist yourself (elsewhere); `seam` for every chained pair; inspect a `--final` render | the reviews are clean, or 3 rounds, then report |

After three rounds, stop and report what is still wrong. Do not loop.

## Visual checklist (look at every frame you grab)

1. **Complete end state.** The last frame shows everything the storyline promises, with
   nothing half-faded. If not, add or keep `self.wait(0.1)`.
2. **Nothing clipped** at the frame edges, and **no overlaps**: labels on lines, tick labels
   colliding, text on data.
3. **Legible at the back of the room.** Tick labels at least about 0.18 units tall; no
   hairlines thinner than 2 px at 1080p.
4. **Drawing order.** Labels on top, data above predictions, tracks above detector layers.
   `check_order` passed.
5. **Safe areas.** The title band is empty, and so is every keep-out area.
6. **Colour roles.** Data in `C.data`, theory in `C.theory`, one highlight at a time, no
   stray colours.
7. **Motion reads** in the mid frames: one thing moves at a time, and particles move
   linearly.
8. **Numbers.** Every on-screen number matches the storyline's *Numbers* table (compare
   with lint's string list).
9. **Duration** is within the storyline's seconds; `render` prints it.

## Seams between chained clips

- **Thresholds.** `seam` compares A's last frame with B's first at 1080p. It fails when the
  mean difference is above 1.0 (0–255 scale), when more than 0.5 % of pixels differ by more
  than 24, or when there are more than 50 blobs (5×5 windows entirely over threshold).
- **What real joints look like.** Real 1080p joints measure a mean of 0.2–0.6 and 0 blobs;
  a misplaced object scores blobs in the hundreds.
- **Judge on `--final` renders.** 480p drafts upscaled to 1080p can fail on codec noise
  alone.
- **The usual fixes:** the second clip must open with `add_state(self, state_of_first_clip)`,
  and both clips must place things through the same anchors.

## Report (always, even when all is well)

```
| Clip | Scene | Duration | Frames inspected | Checks | Findings |
|------|-------|----------|------------------|--------|----------|
| drell-yan | DrellYan | 6.4 s | first, t2, t4, last (.manim-hep/work/drell-yan/) | lint ok, safe areas clear | label ℓ⁺ touches its line at t4 → fixed |
```

Then: what is left, and the next step (for example "render --final when you are happy").
