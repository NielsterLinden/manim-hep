# Verification

The rule: **nobody assumes a scene looks right.** Render it, look at the frames, fix it.

## `manim-hep render`

- **One scene at a time.** A lock makes parallel calls wait, because concurrent `MathTex`
  compiles race on Manim's cache.
- **Frames to look at.** It writes the first and last frames, plus any `--frames` times, as
  PNGs in `.manim-hep/work/<slug>/`.
- **Safe-area scan.** It scans every frame for ink in the title band and the keep-out
  areas. More than 0.1 % of an area counts as an intrusion.
- **Delivery.** `--final` renders 1920×1080 at 60 fps and delivers a versioned copy to
  `clips/`.

Frames come from PyAV, which ships its own FFmpeg libraries: no separate `ffmpeg` install
is needed.

## `manim-hep lint`

| Code | Rule |
|---|---|
| MH001 | Hard-coded colour: take colours from the theme palette |
| MH002 | Hard-coded font: the theme sets the font |
| MH003 | ManimGL code (`manimlib`, `ShowCreation`, `CONFIG`, ...) |
| MH004 | `construct` must end with `self.wait(t)`, t ≤ 0.2 s |
| MH005 | A hand-typed experiment label: use `label(...)` |
| MH006 | A private path or host name |

It also lists every on-screen string, for comparison with the storyline. Silence one line
with `# noqa: MH001`.

## `manim-hep seam A.mp4 B.mp4`

Compares A's last frame with B's first frame at 1920×1080. A pixel "differs" when a
colour channel changes by more than 24 (on a 0–255 scale). The check fails when any of
these holds:
- the mean difference is above **1.0**;
- more than **0.5 %** of pixels differ;
- there are more than **50 blobs**, a blob being a 5×5 window where every pixel differs.

These thresholds were calibrated on real chained 1080p clips:
- **Seamless joints** measure a mean of 0.2–0.6, with no blobs. H.264 ringing on glyph
  edges never fills a whole 5×5 window.
- **A misplaced object** scores blobs in the hundreds.

Judge seams on `--final` renders: 480p drafts, upscaled, can fail on codec noise alone.

## Why every clip ends with `self.wait(0.1)`

Manim writes a clip's last frame one step *before* the final state. A clip ending on a
fade-out still shows a trace of the faded object. The test suite re-checks this on every
Manim upgrade (`tests/test_manim_behaviour.py`), and lint enforces the final wait (MH004).
