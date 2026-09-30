---
name: hep-animate
description: Entry point for making high-energy-physics (HEP) animations with Manim Community Edition and manim-hep, such as Feynman diagrams, detectors and particle signatures, result plots, statistics and machine-learning explainers, delivered as clips for a slide deck. Use when the user asks for an animation, clip, scene or visual for a physics talk, or mentions Manim or manim-hep. It reads manim-hep.toml, applies the house rules, and runs the storyline → build → verify → deliver workflow.
---

# Making a HEP animation with manim-hep

You make short MP4 clips that the user drops into a slide deck (PowerPoint, Keynote, Google
Slides or Beamer). Each clip ends on a complete last frame, and it is delivered together
with that frame as a PNG.

## 1. Setup check (first use in a project)

1. Run `manim-hep doctor`. If it fails, follow its fix lines or the `hep-setup` skill;
   do not start long installs mid-task without asking.
2. If there is no `manim-hep.toml`, offer `manim-hep init` (see `hep-setup`).

## 2. Read the settings

Read the nearest `manim-hep.toml` (search upward from the working directory). Missing keys
take the defaults shown here.

| Key | Default | What it means for you |
|---|---|---|
| `paths.root` | `"."` | `scenes/`, `storylines/`, `data/` and `clips/` live under this folder |
| `style.experiment` | `"generic"` | Theme: `generic`, `atlas`, `cms`, `cms-opendata` or `lhcb`. `use_theme()` picks it up |
| `style.title_band` | `2.7` | Nothing may be drawn above this y (the slide title sits there) |
| `style.keep_out` | none | More `[x0, y0, x1, y1]` areas to keep clear |
| `agent.storyline` | `"artifact"` | `off`: build from the request. `markdown`: write the storyline and get approval in chat. `artifact`: the same, and also publish it as a claude.ai artifact where available |
| `agent.verify` | `"frames"` | `none`, `render`, `frames` or `review` (see `hep-render-verify`) |
| `agent.branch` | `"feature"` | `current`: stay on the checked-out branch. `feature`: `git switch -c anim/<slug>`. `worktree`: `git worktree add .manim-hep/worktrees/<slug> -b anim/<slug>` |
| `agent.commit` | `"ask"` | `never`, `ask` (propose the files and a message, then wait) or `auto` (commit scene, storyline and data once verified) |

Rendered media are never committed, and you never push.

<!-- rules:start -->
## How to work (manim-hep)

These four principles are adapted from Jiayuan Zhang's
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), which distils
[Andrej Karpathy's notes on coding with LLMs](https://x.com/karpathy/status/2015883857489522876).

1. **Think before coding.** Unless the `storyline` setting is `off`, agree the storyline
   before writing scene code. Either way, say what you are assuming. If a number, physics
   claim or requirement is unclear, or does not match its source, stop and ask. Never guess,
   and never quietly adjust.
2. **Simplicity first.** Write the smallest scene that tells the story, one idea per clip.
   Use `manim_hep` building blocks before writing new ones. Add no option, helper or
   abstraction the storyline doesn't need.
3. **Surgical changes.** Touch only the scene you were asked about. Shared helpers are
   add-only: never change an existing signature or default.
4. **Goal-driven execution.** The storyline states what the final frame must show; with the
   storyline off, the request does. Render, look at the frames, and compare them against it,
   as far as the `verify` setting asks. Report which frames you inspected.

### House rules

- **Animation only.** No narrative text on screen unless the storyline allows it. Physics
  symbols, units, tick labels and numbers are always allowed.
- **Theme only.** Colours and fonts come from the theme (`use_theme()`), never from literals.
- **Every number on screen has a source.** It comes from a frozen JSON file with provenance,
  or the storyline declares it schematic.
- **Manim Community Edition only.** Use `from manim import ...`, never `manimlib`.
- **One render at a time**, through `manim-hep render`.
- **End every clip on its last change** (`self.wait(0.1)`), so the final frame is complete.
- **Keep the title band clear** (nothing above y = 2.7 unless the settings say otherwise).
- **Explicit status labels.** Experiment labels always carry an explicit status. Never
  invent or default one.
- **No logos you weren't given.** Never download or draw collaboration logos; only use a
  file the user supplies.
- **Never push.** Commit only as far as the `commit` setting allows.
<!-- rules:end -->

## 3. Workflow

1. **Storyline** (skip when `storyline = "off"`). Use the `hep-storyline` skill: a short
   interview, then `<root>/storylines/<slug>.md`. **Wait for approval.**
2. **Branch** as `agent.branch` says. Check `git status` first and never carry unrelated
   changes onto the new branch.
3. **Build** `<root>/scenes/<slug>.py` with the `hep-scenes` skill. Also use `hep-physics`
   for physics content, `hep-plots-data` for data and plots, and `hep-experiment-style` for
   experiment labels. In Claude Code, delegate the build to the `scene-builder` agent (or
   `plot-recreator` for result plots) with the approved storyline path; elsewhere, build it
   yourself.
4. **Verify** to the `verify` level with the `hep-render-verify` skill.
5. **Deliver** (skip when `verify = "none"`: the user renders). Run
   `manim-hep render <scene> <Scene> --final`, which writes `<root>/clips/<slug>_vK.mp4` and
   `_vK_final.png`. Fill in the storyline's *Record* (clip path, duration, frames inspected),
   save a few keyframes as small PNGs in `<root>/storylines/<slug>/frames/`, and set
   `state: built`.
6. **Commit** as `agent.commit` says: scene, storyline, data and keyframes, never `clips/`
   or `media/`. Never push; tell the user the branch name.

Report at the end: what you built (paths), the clip and its duration, the frames you
inspected, what you could not do, and the next step.

## Which skill for what

| Need | Skill |
|---|---|
| Plan the clip, interview, approval | `hep-storyline` |
| Write or fix scene code, Manim traps | `hep-scenes` |
| Render, inspect frames, lint, seams, report | `hep-render-verify` |
| Physics conventions and review checklist | `hep-physics` |
| ATLAS / CMS / LHCb style, labels, logos, Open Data | `hep-experiment-style` |
| Real or synthetic data, histograms, fits, extractors | `hep-plots-data` |
| Install, doctor, init, platform problems | `hep-setup` |
| Share a scene back to the manim-hep gallery | `hep-contribute` |

## Tool notes

- **Claude Code.** The agents `scene-builder`, `plot-recreator`, `render-verifier` and
  `physics-checker` are available. You, the main session, keep the coordination, because
  only you can ask the user questions and publish artifacts. Critics only read; builders fix.
- **Codex and other agents.** There are no subagents: do the steps yourself, in order.
  Storylines are markdown.
- **Examples.** The manim-hep gallery (`gallery/` in the manim-hep repository) has a worked
  example for most topics. Start from the closest one.
