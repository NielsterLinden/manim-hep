# Settings (`manim-hep.toml`)

The settings live in a `manim-hep.toml` file in your repository, so every agent and every
collaborator reads the same values. `manim-hep init` writes it. Tools find it by searching
upward from the scene file or the working directory. Missing keys take the defaults below.

```toml
[paths]
root = "."                # where scenes/, storylines/, data/, clips/ live (e.g. "presentation")

[style]
experiment = "generic"    # generic | atlas | cms | cms-opendata | lhcb
# title_band = 2.7        # nothing is drawn above this y
# keep_out = [[-7.1, 0.2, -5.85, 4.0]]   # more areas to keep clear: [x0, y0, x1, y1]

[agent]
storyline = "artifact"    # off | markdown | artifact
verify    = "frames"      # none | render | frames | review
branch    = "feature"     # current | feature | worktree
commit    = "ask"         # never | ask | auto   (pushing is never automatic)
```

## `[style]`

- **`experiment`** picks the theme that `use_theme()` activates: the colour cycle and font.
  The label status is always chosen per plot, never here.
- **`title_band`** is the lowest y of the slide-title area; `4.0` disables it.
  `manim-hep render` warns when any frame puts ink there.
- **`keep_out`** lists other rectangles to keep clear, in scene units (the frame is 14.2 ×
  8 units, centred on the origin). An example is a corner your slide uses for a chapter
  marker.

## `[agent]`

**`storyline`**

| Value | Behaviour |
|---|---|
| `off` | No storyline: build straight from the request (for small tweaks) |
| `markdown` | Write `storylines/<slug>.md` and ask for approval in the chat |
| `artifact` | As `markdown`, and also publish the storyline as a claude.ai artifact page for review. It falls back to `markdown` wherever artifacts are not available: Codex, other agents, or Claude through the API |

**`verify`**

| Value | What the agent does | Stops when |
|---|---|---|
| `none` | Writes the code and tells you how to render it | the code is written |
| `render` | Renders at low quality | the render succeeds (at most 3 fix rounds) |
| `frames` | As `render`, plus: inspects the first, last and per-beat frames against the storyline, runs `lint`, checks the title band | all criteria pass, or 3 rounds |
| `review` | As `frames`, plus: read-only physics and render reviews, seam checks between chained clips, a look at the final-quality render | the reviews are clean, or 3 rounds |

**`branch`**
- **`current`**: work on the checked-out branch.
- **`feature`**: `anim/<slug>`, created from the current branch; merging is up to you.
- **`worktree`**: a git worktree for `anim/<slug>` under `.manim-hep/worktrees/`, so
  several agents can build clips in parallel. `manim-hep render --final` delivers clips to
  the main checkout's `clips/`, so removing the worktree never deletes a delivered clip.

**`commit`**
- **`never`**: leave everything uncommitted.
- **`ask`**: propose the files and a message, and wait.
- **`auto`**: commit scene, storyline and data once verification passes.

Rendered media are never committed, and no agent ever pushes.
