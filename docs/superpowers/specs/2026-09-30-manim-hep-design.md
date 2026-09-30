# manim-hep ("Agentic Manim for HEP"): v0.1 design

*Date: 2026-09-30 · Status: approved 2026-09-30 · Owner: @NielsterLinden*

## 1. Summary

manim-hep is an open-source toolkit for making high-energy-physics (HEP) animations with [Manim](https://www.manim.community). There are three ways to use it:

- **Import it.** `pip install manim-hep`, then use a small Python package of HEP building blocks.
- **Ask an agent.** Claude Code, Codex and other coding agents get skills that know how to plan, build, render and check HEP animations.
- **Work by hand.** Copy and adapt examples from a gallery organised by topic.

v0.1 is **agent-first with a thin core**. Most of the value comes from the skills, the agents and the gallery. The importable package is small and well tested, and it grows only when examples prove that something is reused.

The design encodes practices that worked across three real talks built with Manim and coding agents: an ATLAS MSc thesis, an LHCb summer project, and a CMS Open Data school. All the credit for the animation engine goes to Grant Sanderson (3Blue1Brown) and the Manim Community developers (§4.3).

## 2. Goals, non-goals, success criteria

**Goals**
- **G1: three ways in.** Import, agents and by hand, all backed by the same package, docs and gallery.
- **G2: community-maintained.** Contributions arrive as gallery examples through pull requests, with a low barrier and clear rules.
- **G3: experiment-correct styling.** ATLAS, CMS and LHCb presets whose status labels ("Preliminary", "Simulation", …) must be chosen explicitly.
- **G4: proven practice.** The library and skills carry the practices shared by the three origin projects (§6.1, §7.1).
- **G5: generous credit.** Manim's creators and maintainers, and everyone else we build on, are credited prominently.
- **G6: safe to publish.** No collaboration logos, internal results, private paths or personal data, in the repo or in anything the tools generate.

**Non-goals for v0.1:** see §15.

**Success criteria for v0.1**
- **S1.** A HEP PhD student who has never used Manim pastes the quickinstall sentence (§9.4) into their agent, in their own repository, on Windows, macOS, Linux or lxplus. Within one working session they have a correct, experiment-styled clip in their talk.
- **S2.** `pip install manim-hep` followed by `manim-hep doctor` passes on Linux, macOS and Windows in CI.
- **S3.** All 14 starter examples (§8.3) render in CI.
- **S4.** `claude plugin validate --strict plugin/` passes, and each skill triggers on its intended prompts in the plugin evals.
- **S5.** A dry run of the quickinstall on a fresh repository ends with a green smoke-frame check: once with Claude Code and once with Codex. This is done by hand before the release.

## 3. Decisions

| # | Decision | Choice | Why |
|---|---|---|---|
| D1 | Focus of v0.1 | Agent-first, thin core | Agents deliver value from day one; the API grows from real reuse, not guesses |
| D2 | Storyline | Plan first, then build | The human owns the story and the physics before render time is spent; matches "think before coding" |
| D3 | Hosting | `github.com/NielsterLinden/manim-hep` | Simplest start; can move to an organisation later (GitHub redirects old URLs) |
| D4 | Architecture | One repo, three layers: package, gallery, plugin | One PR can change code, example and skill together, so the skills never drift from the API |
| D5 | Gallery scope | A curated starter set of 14, plus "port this" issues | Ships sooner and leaves on-ramps for contributors |
| D6 | Name | `manim-hep`, displayed as "Agentic Manim for HEP" | Free on PyPI, conda-forge and GitHub; the `manim-` prefix gets it auto-listed on the Manim plugin registry; neutral (no experiment or CERN name) |
| D7 | Licence | MIT for everything | Matches Manim |
| D8 | Where settings live | A `manim-hep.toml` file in the user's project | Every agent and every collaborator can read it; plugin options would be per-user and Claude-only |
| D9 | Setting defaults | `storyline=artifact`, `verify=frames`, `branch=feature`, `commit=ask` | Balances care with speed; pushing is never automatic |
| D10 | Agent layer | 9 portable skills plus 4 Claude agents; coordination stays in the main session | Skills work in every tool; only the main session can ask the user questions and publish the storyline |
| D11 | What gets delivered | MP4 clips plus a last-frame PNG | The workflow proven in all three talks: the deck is built in PowerPoint, Keynote, Google Slides or Beamer |
| D12 | Gallery data | Synthetic only (public data with a DOI may come later) | Safe to publish |
| D13 | Logos | Never shipped; only files the user supplies | None of ATLAS, CMS, LHCb or KM3NeT grants redistribution |
| D14 | Plugin evals | Run by hand before each release | They cost API credit per run |

## 4. Identity, licence, credits

### 4.1 Names

| Where | Name |
|---|---|
| GitHub | `NielsterLinden/manim-hep` |
| PyPI | `manim-hep` (`import manim_hep`) |
| CLI | `manim-hep` |
| Claude Code plugin | plugin `manim-hep`, in a marketplace also named `manim-hep` |
| Display name | Agentic Manim for HEP |

All of these names were checked as unregistered on 2026-09-30. The package declares a `manim.plugins` entry point, so `plugins.manim.community` lists it automatically. The name avoids experiment and CERN names, as ATLAS's public design guidance asks.

### 4.2 Licence
- MIT for code, skills, agents and docs.
- Gallery data is synthetic.
- Nothing licensed CC BY-SA, NC or proprietary is copied in. For example, the Standard Model chart is designed from scratch rather than following an existing share-alike layout.
- Bundled fonts use permissive licences (DejaVu Sans; see §6.4).

### 4.3 Credits
These go in `CREDITS.md` and a README section, in the voice of a happy user:
- **Manim.** "Built on Manim Community Edition (MIT; © 2018 3Blue1Brown LLC, © 2024 the Manim Community Developers), originally created by Grant Sanderson (3Blue1Brown)." Link to [ManimCommunity/manim](https://github.com/ManimCommunity/manim) and [3b1b/manim](https://github.com/3b1b/manim). Ask users to cite Manim through its `CITATION.cff`.
- **The four coding principles (§7.1).** "Adapted from Jiayuan Zhang's [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), which distils [Andrej Karpathy's notes on coding with LLMs](https://x.com/karpathy/status/2015883857489522876) (26 January 2026)."
  - Karpathy wrote the observations; Zhang wrote the principles.
  - We write our own HEP-adapted wording and don't copy text, because that repository declares MIT but has no licence file.
- **HEP style conventions.** [mplhep](https://github.com/scikit-hep/mplhep) (Scikit-HEP) and [cmsstyle](https://github.com/cms-cat/cmsstyle) for experiment palettes and label conventions, and the CMS colour-vision-deficiency-friendly palettes (Petroff, arXiv:2107.02270).
- **Related projects.** [feynmanim](https://github.com/PTremper/feynmanim) (Feynman diagrams in Manim) and [dvnanima](https://github.com/NeutrinoHit/dvnanima) (neutrino, Cherenkov and air-shower scenes).

### 4.4 Citation and disclaimer
- A `CITATION.cff` file, and a Zenodo DOI minted on every GitHub release.
- The README states: "Not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. Experiment presets follow public conventions. Your collaboration's approval rules still apply to anything you show."

## 5. Repository layout

```
manim-hep/
├── README.md             a one-line work-in-progress note (until v0.1.0), what it is, gallery previews, the three ways in, credits
├── QUICKINSTALL.md       the one sentence to paste into an agent (§9.4)
├── AGENTS.md             rules for agents working ON this repo (§10.4)
├── CLAUDE.md             one line: @AGENTS.md
├── CONTRIBUTING.md  CODE_OF_CONDUCT.md  CREDITS.md  LICENSE  CITATION.cff
├── pyproject.toml        manim-hep; manim>=0.21,<0.22; manim.plugins entry point; `manim-hep` script
├── src/manim_hep/        the thin core (§6)
├── gallery/              examples by category (§8)
├── plugin/               the agent layer (§7)
│   ├── .claude-plugin/plugin.json
│   ├── skills/<name>/SKILL.md (+ reference files)
│   ├── agents/<name>.md
│   └── README.md
├── .claude-plugin/marketplace.json   marketplace "manim-hep" → plugin source "./plugin"
├── docs/                 install guides, concepts, API reference; built into a site with the gallery
├── tests/
└── .github/              CI workflows, issue and PR templates, CODEOWNERS
```

The plugin sits in its own folder. That keeps it small and self-contained (claude.ai caps plugins at 5,000 files and 200 MB) and keeps the gallery out of the plugin cache. The plugin must not contain a top-level `bin/`, because claude.ai and Cowork refuse to install such plugins.

## 6. The core package (`manim_hep`)

### 6.1 Principles
- **Thin.** Only building blocks that the starter gallery needs.
- **Add-only API.** An existing public signature or default never changes, because finished clips depend on it. New behaviour gets a new name. A breaking change is allowed only in a new minor version (0.x → 0.y) with a changelog entry.
- **Promotion rule.** Code starts in a gallery example. It moves into the core when a second example needs it, and it arrives with tests.
- **Shipped together.** The skills document the API of the same release. The plugin version always equals the package version, and CI checks this.

### 6.2 Modules

| Module | Contents (v0.1) |
|---|---|
| `palette` | Colour roles (`ink`, `data`, `theory`, `detector`, `highlight`, `background`, plus tints), a categorical cycle, and the `tint`, `shade` and `mix` functions. **It doesn't import Manim**, so matplotlib figures can share it. The default palette is Okabe–Ito-based. A test checks colour-vision-deficiency safety: under simulated deuteranopia, protanopia and tritanopia, the minimum pairwise colour distance of any shipped cycle must be at least that of the Okabe–Ito palette. |
| `style` | The theme: fonts, a white background ("reads better on a projector"), safe areas (a title band at the top of the frame, kept clear for the slide title; optional keep-out rectangles), and `use_theme(name=None)`. With no name, it reads `[style] experiment` from `manim-hep.toml` (searching upward from the working directory) and otherwise uses `generic`. |
| `experiments` | Presets `generic`, `atlas`, `cms` and `lhcb`: categorical cycle and fonts taken from mplhep's styles, plus `label(experiment, status=…, lumi=…, sqrt_s=…, loc=…)`, which returns a positioned Manim group.<br>**`status` is a required keyword argument with no default**, validated against that experiment's public list: ATLAS Internal, Preliminary, Simulation, Work in Progress, or an explicit `status=None` for the bare "ATLAS" label used on papers; CMS Preliminary, Simulation, Supplementary, Work in progress, Private work; LHCb Preliminary, Unofficial, Simulation.<br>A `cms-opendata` variant requires `doi=` and always adds the non-endorsement note and that DOI.<br>`logo(path)` only loads a file the user supplies.<br>Where mplhep is installed, tests check that the presets match it. |
| `feynman` | Line primitives (fermion with a mid-arrow, photon, gluon, massive boson, scalar), vertices and labels, and `FeynmanDiagram(vertices, edges)`, built from a coordinate dictionary, with an animation that draws the diagram in build order |
| `plots` | `DataAxes` (manual ticks in the theme font, optional log-y with a floor), `step_hist`, `stack_hist` (a fixed polygon count, so stacks can morph with `Transform`), `errorbars` (capless by default), `ratio_panel`, `band` |
| `detector` | A neutral `BarrelSlice` (beam pipe, tracker, ECAL, solenoid, HCAL, muon system, with configurable radii), `track(pt, charge, field, …)` with the correct curvature sign, and `signature(kind)` for electron, muon, photon, jet, τ (1 or 3 prongs) and neutrino/MET. No experiment's official geometry or logo-derived drawing. |
| `build` | Helpers for building scenes state-first: `add_state(scene, builder)`, `check_order(scene, order)` (asserts the drawing order), and `place(mobject, anchor)` for a module-level anchor dictionary |
| `data` | `freeze(values, path, source=…, selection=…, version=…)` writes JSON with provenance (date; the git commit and dirty flag of the producing repository when available). `load_frozen(path, expect={…}, rtol=…)` loads it and raises a clear error on any mismatch. |

### 6.3 CLI (`manim-hep …`)

| Command | What it does |
|---|---|
| `init [--root DIR] [--agent claude\|codex\|both\|none] [--experiment X]` | Scaffolds a user project (§9.6). Merges into existing files and never overwrites them. Running it twice changes nothing. |
| `doctor` | Checks Python, that `manim` is ManimCE 0.21.x (not ManimGL), LaTeX (`latex`, `dvisvgm`, `standalone.cls`), fonts, and write access. Prints the exact fix commands for the platform (Windows, macOS, Linux, lxplus, generic cluster). Exits non-zero on any failure. |
| `render FILE SCENE [--final] [--frames T1,T2…]` | Renders one scene at a time (a cross-platform lock). Low quality by default; `--final` renders at 1080p60. Checks that the render succeeded, then writes the first and last frames (plus any requested times) as PNGs, and warns if pixels intrude into the title band. With `--final` it delivers `clips/<slug>_vK.mp4` and `clips/<slug>_vK_final.png`, where K is the next free version; an existing version is never overwritten. |
| `lint [PATHS]` | Flags hard-coded colours and fonts, `manimlib` or ManimGL-only names, clips whose `construct` doesn't end with `self.wait(t)` where t ≤ 0.2 s, hand-typed experiment labels, and private-path patterns. Lists on-screen strings, so they can be checked against the storyline. |
| `seam A.mp4 B.mp4` | Compares A's last frame with B's first frame at 1080p. Fails if the mean absolute difference is above 1.0 (0–255 scale), if more than 0.5 % of pixels exceed the threshold, or if there are more than 50 blobs (5×5 neighbourhoods entirely above the threshold). These thresholds were calibrated on real chained clips. |

Frame extraction and durations use PyAV, which Manim already depends on, so no separate ffmpeg install is needed (to be verified: §16).

### 6.4 Platforms and dependencies
- Python 3.11 or later, and `manim>=0.21,<0.22`. The upper bound is deliberate: the trap list (§7.5, `hep-scenes`) is specific to a Manim version, so upgrading Manim is a deliberate step.
- Runtime dependencies beyond Manim's own are kept to a minimum. Optional extras:
  - `manim-hep[mplhep]` pulls in mplhep and its fonts, for exact experiment typography;
  - `manim-hep[dev]` pulls in the test and docs tooling.
- DejaVu Sans, used in all three origin projects, is bundled and registered when the theme is activated. Text then looks the same on every OS (Windows and macOS don't ship it).
- LaTeX is needed for `MathTex`. The recommended installs:
  - Windows: MiKTeX or TeX Live;
  - macOS: MacTeX or BasicTeX plus the listed packages;
  - Linux: TeX Live;
  - lxplus: TeX Live from CVMFS.
  A bare `texlive-core` has proven insufficient. `doctor` checks for the actual files needed.

## 7. The agent layer

### 7.1 Rules

This block goes into the `AGENTS.md` that `init` writes into a user project. It is also embedded in the `hep-animate` skill, because a plugin's own `CLAUDE.md` is never loaded.

> **How to work.** These four principles are adapted from Jiayuan Zhang's andrej-karpathy-skills, which distils Andrej Karpathy's notes on coding with LLMs.
> 1. **Think before coding.** Unless the `storyline` setting is `off`, agree the storyline before writing scene code. Either way, say what you are assuming. If a number, physics claim or requirement is unclear, or does not match its source, stop and ask. Never guess, and never quietly adjust.
> 2. **Simplicity first.** Write the smallest scene that tells the story, one idea per clip. Use `manim_hep` building blocks before writing new ones. Add no option, helper or abstraction the storyline doesn't need.
> 3. **Surgical changes.** Touch only the scene you were asked about. Shared helpers are add-only: never change an existing signature or default.
> 4. **Goal-driven execution.** The storyline states what the final frame must show; with the storyline off, the request does. Render, look at the frames, and compare them against it, as far as the `verify` setting asks. Report which frames you inspected.
>
> **House rules**
> - **Animation only.** No narrative text on screen unless the storyline allows it. Physics symbols, units, tick labels and numbers are always allowed.
> - **Theme only.** Colours and fonts come from the theme, never from literals.
> - **Every number on screen has a source.** It comes from a frozen JSON file with provenance, or the storyline declares it schematic.
> - **Manim Community Edition only.** Use `from manim import …`, never `manimlib`.
> - **One render at a time**, through `manim-hep render`.
> - **End every clip on its last change** (`self.wait(0.1)`), so the final frame is complete.
> - **Keep the title band clear.**
> - **Explicit status labels.** Experiment labels always carry an explicit status. Never invent or default one.
> - **No logos you weren't given.** Never download or draw collaboration logos; only use a file the user supplies.
> - **Never push.** Commit only as far as the `commit` setting allows.

### 7.2 Workflow

The `hep-animate` skill drives these steps.

1. **Setup check.** On first use in a project, run `manim-hep doctor`. If `manim-hep.toml` is missing, offer `init`.
2. **Storyline** (unless `storyline = "off"`).
   - Run a short interview. Each question comes with the agent's recommendation.
   - Write `storylines/<slug>.md` from the template (§7.4).
   - Present it as `storyline` says (§7.3), then **wait for approval**.
3. **Branch** as `branch` says.
4. **Build.** Write a state-first scene on the core, using the `scene-builder` agent in Claude Code or working directly elsewhere. Plots use `plot-recreator`, or the `hep-plots-data` skill.
5. **Verify** to the level `verify` sets (§7.3).
6. **Deliver.** Skipped when `verify = "none"`, because the user renders.
   - Run `manim-hep render --final`, which writes a versioned MP4 and last-frame PNG to `clips/`.
   - Fill in the storyline's *Record* section: clip path, duration, and which frames were inspected.
   - Save keyframes as small PNGs in `storylines/<slug>/frames/`, so the storyline becomes the record.
7. **Commit** as `commit` says. Never push.

### 7.3 Settings (`manim-hep.toml`)

```toml
[paths]
root = "."                # where scenes/, storylines/, data/, clips/ live (e.g. "presentation")

[style]
experiment = "generic"    # generic | atlas | cms | lhcb

[agent]
storyline = "artifact"    # off | markdown | artifact
verify    = "frames"      # none | render | frames | review
branch    = "feature"     # current | feature | worktree
commit    = "ask"         # never | ask | auto   (pushing is never automatic)
```

**`storyline`**
- `off`: no storyline; build straight from the request (for small tweaks).
- `markdown`: write the file and ask for approval in the chat.
- `artifact`: the same, and also publish the storyline as a claude.ai artifact page for review. It falls back to `markdown` wherever artifacts aren't available: Codex and other agents, or Claude via the API, Bedrock or Vertex.

**`verify`**

| Level | What the agent does | Stops when |
|---|---|---|
| `none` | Writes the code and tells you how to render it | Code is written |
| `render` | Renders at low quality with `manim-hep render` | The render succeeds (at most 3 fix rounds) |
| `frames` | As `render`, plus: inspects the first, last and per-beat frames against the storyline's "Final frame must show" list, runs `manim-hep lint`, and checks the title band | All criteria pass, or 3 rounds have passed, after which it reports |
| `review` | As `frames`, plus: read-only reviews by `physics-checker` and `render-verifier`, `seam` checks between chained clips, and inspection of the final-quality render | The reviews are clean, or 3 rounds have passed, after which it reports |

**`branch`**
- `current`: work on the checked-out branch.
- `feature`: `anim/<slug>`, created from the current branch; merging is the user's call.
- `worktree`: a git worktree for `anim/<slug>` under `.manim-hep/worktrees/`, so several agents can build clips in parallel.

**`commit`**
- `never`: leave everything uncommitted.
- `ask`: propose the files and a message, and wait.
- `auto`: commit scene, storyline and data files once verification passes.

Rendered media are never committed, and no agent ever pushes.

### 7.4 Storyline template

```markdown
---
slug: <kebab-case>
state: draft | approved | built
experiment: generic | atlas | cms | lhcb
label_status: <explicit status, or "none" if no experiment label>
---
# <Title>
**Point (one sentence):**
**Context:** talk, slot, what comes before and after this clip

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |

## Final frame must show
- [ ] …

## Chaining
Entry frame: … · Exit frame: …

## Allowed exceptions
(e.g. "a two-word caption on beat 3, requested by the user")

## Record (filled after rendering)
Clip: clips/<slug>_vK.mp4 · Duration: … · Frames inspected: … · Keyframes: storylines/<slug>/frames/
```

### 7.5 Skills

Skills use the Agent Skills format: `SKILL.md` with `name` and `description`, where the name matches its directory. Each one works on its own, because agents aren't available on every surface. The names carry a `hep-` prefix so they can't collide when copied into a project's `.agents/skills/`.

| Skill | Purpose | Key contents |
|---|---|---|
| `hep-animate` | Entry point | Reads `manim-hep.toml`; the rules (§7.1); the workflow (§7.2); which skill to use for what |
| `hep-storyline` | Plan first | A question bank (recommendation first); the template (§7.4); how to publish as an artifact, and the fallback |
| `hep-scenes` | Writing scenes on the core | The state-first pattern, anchors, `check_order`; pacing (clips of 4–13 s, particles moving linearly at about 2 s per track, one idea per clip); text and LaTeX rules; 3D tips; **the trap list**, a reference file re-validated against Manim 0.21 |
| `hep-render-verify` | Checking | Commands; the verification levels; a visual checklist (clipping, overlaps, the last-frame bug, drawing order, title band); `seam` thresholds; the report format |
| `hep-physics` | Physics fidelity | Feynman-diagram conventions, particle signatures, notation and units, common pitfalls; a checklist graded BLOCK / MAJOR / MINOR |
| `hep-experiment-style` | Presets and labels | What each status label means and when to use it; logo policy; Open Data rules (CC0, the non-endorsement note, cite the DOI); parity with mplhep |
| `hep-plots-data` | Result plots | An extractor template (it runs in the user's analysis environment and writes frozen JSON); provenance fields; assert on load; step histograms; "the data never move"; when to recreate a plot and when to import the image |
| `hep-setup` | Install | The `AGENT_INSTALL.md` procedure (§9.4); per-platform notes; `doctor`; `init` |
| `hep-contribute` | Upstreaming | A privacy scrub list, swapping in synthetic data, the README header, the PR checklist; fork, branch and PR commands, with pushing only after the user says yes |

### 7.6 Agents (Claude Code and Cowork)

| Agent | Role | Tools | May edit | Must not edit |
|---|---|---|---|---|
| `scene-builder` | Builds or edits one scene from an approved storyline; drafts at low quality | Read, Write, Edit, Glob, Grep, Bash | The scene files named in its task | The `manim_hep` package, other scenes, settings, storylines |
| `render-verifier` | Renders, grabs frames, inspects them; runs `lint` and `seam`; reports findings with frame references | Read, Glob, Grep, Bash | Nothing (read-only; renders go to `.manim-hep/work/`) | Any source file |
| `physics-checker` | Checks physics claims, notation and numbers against the storyline's sources | Read, Glob, Grep | Nothing | Everything |
| `plot-recreator` | Builds result-plot scenes from frozen data; writes extractor scripts for the user to run | Read, Write, Edit, Glob, Grep, Bash | Its scene file, `data/*.json`, extractor scripts | The core package, other scenes |

Coordination stays in the main session, inside `hep-animate`, because only the main session can ask the user questions and publish artifacts. Critics only read; builders fix. No agent sets `model:`, so all of them inherit the session model.

### 7.7 Support across tools

| | Claude Code | Codex | Cursor, Copilot, Gemini CLI, … | By hand |
|---|---|---|---|---|
| Rules | `AGENTS.md`, via `@AGENTS.md` in `CLAUDE.md`; also inside `hep-animate` | `AGENTS.md` | `AGENTS.md` | `CONTRIBUTING.md`, docs |
| Skills | The plugin | `.agents/skills/` (copied by `init`), or Codex's plugin marketplace if it accepts our manifest (§16) | `.agents/skills/` where the tool supports it | The docs cover the same content |
| Agents | The plugin (4 agents) | Not in v0.1; the workflow runs from the skills alone | Not available | Not applicable |
| Storyline artifact | Yes, where claude.ai artifacts are available | Markdown | Markdown | Markdown |

## 8. Gallery

### 8.1 Categories
```
gallery/
├── theory/        Feynman diagrams, Higgs potential, cross sections, couplings
├── methods/       statistics (counting, significance, fits, limits) · analysis flow (selection,
│                  tag-and-probe, background estimation) · simulation and reconstruction
├── experiments/   generic/ · atlas/ · cms/ · lhcb/ · km3net/
├── plots/         general/ · atlas/ · cms/ · lhcb/   (experiment folders use the official-style presets)
└── ml/            neural nets, backprop, attention and transformers, BDTs
```
`experiments/km3net/` starts as a README inviting contributions and pointing to dvnanima's Cherenkov and PMT scenes as prior art.

### 8.2 What an example is
Each example is a folder, `gallery/<category>/[<experiment>/]<slug>/`, containing:
- **`scene.py`**: self-contained; imports only `manim`, `manim_hep` and the standard library; uses synthetic data (seeded).
- **`README.md`**: a YAML header (`title`, `category`, `tags`, `authors`, `data: synthetic`, `label_status`, `manim_hep` version, `references`), then what the example shows, physics notes with sources, and how to adapt it.
- **`storyline.md`** (optional): the storyline it was built from, so the gallery also teaches the workflow. Its *Record* section omits keyframes, because gallery previews come from CI.

CI renders the previews (GIF and MP4) into the docs site. Previews are never committed.

### 8.3 Starter set (14 examples)

| Folder | Example | Adapted from |
|---|---|---|
| `theory/drell-yan` | q q̄ → Z/γ* → ℓℓ Feynman diagram, drawn in build order | CMS talk |
| `theory/higgs-potential` | V(φ): the double well, v, and m_H from λ | ATLAS talk |
| `methods/counting-experiment` | Repeated collisions; a rare signal tallied against background | ATLAS talk |
| `methods/significance-roc` | Threshold sweep, ROC curve and Z(cut) on synthetic scores | ATLAS talk |
| `methods/template-fit` | Templates, data, signal-strength slider, −2ΔlnL parabola | CMS talk |
| `experiments/generic/detector-signatures` | Barrel slice built inside-out; e, μ, γ, jet, ν signatures | ATLAS and CMS talks |
| `experiments/generic/tracks-in-field` | Curvature sign from charge, radius from pT | LHCb and CMS talks |
| `plots/general/histogram-fill` | One event → one entry → the histogram fills | CMS talk |
| `plots/general/stack-data-ratio` | Stacked prediction, data, ratio panel; "the data never move" | CMS talk |
| `plots/atlas/labelled-result` | One result plot in ATLAS style with an explicit status | new |
| `plots/cms/labelled-result` | The same in CMS style | new |
| `plots/lhcb/labelled-result` | The same in LHCb style | new |
| `ml/attention` | Q·K scores, softmax rows, weighted value update | ATLAS talk |
| `ml/backprop` | Forward pass, loss, gradients flowing back through a small network | ATLAS talk |

That makes 14 examples: 11 topics, plus one result plot drawn in each of the three experiment styles.

Examples are **re-implemented** on the core, with synthetic data. No code, text, data or assets are copied from the origin projects, apart from ideas and the author's own generic helpers once they have been scrubbed.

### 8.4 Port backlog
The remaining generic components identified in the origin projects (about 30) each become a "port this" issue, labelled `port` and, where suitable, `good first issue`. Each issue says what the animation shows and which core pieces it needs. Examples:
- **Theory:** τ decay; factorisation and PDFs; the lepton-universality plane; λ running; the SM particle table (designed from scratch).
- **Methods:** tag-and-probe; fake factors; the trigger chain; analysis map; combination.
- **Experiments:** the LHC ring.
- **ML:** tokenisation; embeddings; MLP → KAN; BDTs.
- **Plots:** result frames.

## 9. Distribution and installation

### 9.1 PyPI
`pip install manim-hep`. Manim's own system requirements (cairo/pango where wheels don't cover them, and LaTeX) are documented per platform, and `doctor` checks them. A conda-forge package comes after v0.1.

### 9.2 Claude Code plugin
- **The marketplace file** sits at the repository root in `.claude-plugin/marketplace.json`. It has one entry, with `name` equal to `manim-hep` and `source` equal to `./plugin`.
- **`plugin/.claude-plugin/plugin.json`** sets `name`, `displayName`, `version` (equal to the package version), `description`, `author`, `homepage`, `repository`, `license` and `keywords`.
- **User install:**
  - `/plugin marketplace add NielsterLinden/manim-hep`, then `/plugin install manim-hep@manim-hep`;
  - or, in a shell, `claude plugin marketplace add NielsterLinden/manim-hep` followed by `claude plugin install manim-hep@manim-hep`.
- **Project pre-declaration.** `init --agent claude` merges the following into `.claude/settings.json`, so collaborators are offered the plugin after they trust the folder:
  ```json
  {
    "extraKnownMarketplaces": {
      "manim-hep": { "source": { "source": "github", "repo": "NielsterLinden/manim-hep" } }
    },
    "enabledPlugins": { "manim-hep@manim-hep": true }
  }
  ```
- **Updates.** Bump `version` on every release. Users run `claude plugin update manim-hep@manim-hep`, or turn on auto-update for the marketplace.

### 9.3 Codex and other agents
- `init --agent codex` copies `plugin/skills/hep-*` into `.agents/skills/` and writes `AGENTS.md`.
- If Codex's plugin marketplace (`codex plugin marketplace add owner/repo`) accepts our Claude-format manifest, document that as the preferred route instead (§16).
- Other tools that support the Agent Skills standard read the same `.agents/skills/`.

### 9.4 Quickinstall
`QUICKINSTALL.md` contains the sentence users paste into their agent:

> Set up manim-hep in this repository: follow https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/AGENT_INSTALL.md, and ask me the setup questions first.

`docs/install/AGENT_INSTALL.md` is the agent's procedure. Each phase ends in a check with a known expected result.
- **Phase 0, questions** (with defaults):
  - experiment preset;
  - OS or cluster;
  - conda or pip;
  - whether TeX is available;
  - `paths.root`;
  - the four `[agent]` settings;
  - files it must not touch;
  - whether it may commit.
- **Phase 1, probe.** Run `manim-hep doctor`. Big installs are the user's: the agent prints the commands rather than starting long installs mid-turn, unless the user tells it to.
- **Phase 2, scaffold.** Run `manim-hep init` with the answers. Then grep for unfilled `<PLACEHOLDER>`s; there must be none.
- **Phase 3, smoke test.** Render `scenes/smoke_test.py`, grab its last frame, and check it against the published reference (size, background, font, a rendered `MathTex`). The agent also looks at the frame. If TeX is unavailable, the `MathTex` check is skipped and reported.
- **Phase 4, hand back.** What was done, what couldn't be done and why, and the next step (for example "ask me for your first animation").

A `docs/install/HUMAN_GUIDE.md` explains the same process to people.

### 9.5 `.gitignore` block (written by `init`, between marker comments)
```
# >>> manim-hep
media/
.manim-hep/
__pycache__/
*.pyc
clips/
*.mp4
*.mov
*.gif
.claude/settings.local.json
.claude/worktrees/
# <<< manim-hep
```
To commit clips (some decks link to them), delete the `clips/` and `*.mp4` lines.

### 9.6 What `init` creates in a user project
```
<repo>/
├── manim-hep.toml
├── AGENTS.md            manim-hep block between markers (created or merged)
├── CLAUDE.md            contains "@AGENTS.md" (created or line added)      [claude]
├── .claude/settings.json  marketplace and enabled plugin (merged)          [claude]
├── .agents/skills/hep-*/                                                   [codex]
├── .gitignore           the block above (merged)
└── <root>/
    ├── scenes/smoke_test.py
    ├── storylines/
    ├── data/
    └── clips/
```
Merging is idempotent: blocks between markers are replaced, and anything outside the markers is never touched. If a file can't be merged safely, `init` writes `<file>.manim-hep.new` next to it and reports that.

## 10. Community and governance

### 10.1 Contributing
`CONTRIBUTING.md` covers:
- adding a gallery example (the folder contract in §8.2, a template folder, or the `hep-contribute` skill);
- proposing a core addition (the promotion rule, add-only, with tests);
- changing an experiment preset (needs an experiment code owner).

### 10.2 Review
- **CODEOWNERS.** `/src/manim_hep/experiments/`, `/gallery/experiments/<exp>/` and `/gallery/plots/<exp>/` belong to that experiment's code owners. The owner is initially @NielsterLinden; the aim is to recruit one member per experiment.
- **Issue templates:** "Animation request", "Port this", "Bug".
- **PR template checklist:**
  - it renders in CI;
  - `manim-hep lint` is clean;
  - synthetic data, or public data with a DOI;
  - physics sources are cited;
  - no logos, internal results, private paths, hostnames or personal names;
  - licence-compatible.

### 10.3 Publication safety (enforced, not just written down)
- CI rejects committed media and any file over 1 MB.
- CI runs a secret scan.
- CI checks a denylist of private-path patterns (`/afs/`, `/eos/`, `/project/`, `/data/…/users/`, `C:\Users\`, cluster hostnames).
- `lint` flags hand-typed experiment labels.

### 10.4 This repository's own `AGENTS.md`
It contains the four principles (§7.1), adapted for library work, plus:
- the add-only API and the promotion rule;
- API changes ship with their skill and docs updates in the same PR;
- tests are required for core changes;
- the checks to run: `pytest`, `ruff`, `manim-hep lint gallery/`, `claude plugin validate --strict plugin/`;
- the publication-safety rules.

## 11. Quality: tests and CI

**Tests**
- **Unit tests** for pure logic: palette maths and the colour-vision check, label formatting and status validation, freeze and load, `check_order`, and the `seam` metrics on synthetic images.
- **Construction tests without rendering:** bounding boxes stay within the frame and out of the title band, stack invariants, diagram topology.
- **A few graphical regression tests** for key primitives, using ManimCE's frame-comparison utilities.
- **CLI tests:** `init` is idempotent and preserves foreign content when merging; `doctor` output on mocked environments.
- **Gallery smoke tests:** a low-quality render of each example.

**CI (GitHub Actions)**
- `ci.yml`: ruff, then pytest on {Linux, macOS, Windows} × Python {3.11, 3.12, 3.13}, plus a version-sync check (plugin = package).
- `gallery.yml`: on each PR, a low-quality render and `lint` of the examples it changes (Linux with TeX Live); previews uploaded as artifacts.
- `plugin.yml`: `claude plugin validate --strict plugin/`.
- `docs.yml`: on `main`, builds the docs site (MkDocs Material with mkdocstrings; the gallery pages are generated from the example READMEs and CI previews) and publishes it to GitHub Pages.
- `release.yml`: on a `v*` tag, builds the package, publishes to PyPI via trusted publishing, and creates a GitHub release (Zenodo mints the DOI).
- `hygiene.yml`: the size check, secret scan and path denylist (§10.3).

Plugin evals (`claude plugin eval`) cover skill triggering and the key behaviours. They are run by hand before each release.

## 12. Release and outreach
- **The repository is private during development**, so the privacy scrub is complete before anything is public. It goes public at v0.1.0, with the owner's explicit go-ahead.
- **v0.1.0** is released when S1–S5 pass.
- **After v0.1:**
  - submit to Anthropic's plugin directory (developer portal at claude.ai/directory/manage; needs a paid claude.ai plan);
  - announce on hsf-forum, and offer a PyHEP "Python Module of the Month" talk;
  - open a conversation with Scikit-HEP about becoming an affiliated package;
  - consider applying for HSF affiliation;
  - contact dvnanima's author about KM3NeT and neutrino content;
  - recruit experiment code owners;
  - add conda-forge.

## 13. Implementation milestones
Each milestone can have its own implementation plan.
- **M1: package and CLI.** Repo skeleton, packaging, the core modules (§6.2) with tests, the CLI (§6.3), and `ci.yml`.
- **M2: agent layer.** `plugin/` (9 skills, 4 agents, manifest), the root marketplace, the rules texts, `init --agent`, `QUICKINSTALL.md`, `AGENT_INSTALL.md`, `HUMAN_GUIDE.md`, and `plugin.yml`.
- **M3: gallery.** The starter set (§8.3), `gallery.yml`, the port-backlog issues (drafted in a file; created on GitHub only when the repo exists and with the owner's OK).
- **M4: docs and release.** The docs site, README, CREDITS, CONTRIBUTING, CODE_OF_CONDUCT, CITATION.cff, templates, CODEOWNERS, `hygiene.yml` and `release.yml`; the S5 dry runs; then v0.1.0, with the owner's go-ahead.

## 14. Inputs
- **A harvest of the three origin projects.** This private audit is kept outside the repo, because it contains unpublished results and private paths. It supplied the house rules, the verification loop and thresholds, the trap list, the agent roster and the content inventory. Practices that recurred in all three projects:
  - clips delivered to a slide deck, not a Manim deck;
  - animation-only text;
  - one style module;
  - state-first scenes;
  - frozen numbers with provenance;
  - render, then inspect frames, then fix;
  - plan before building;
  - scoped agents with read-only critics.
- **Research** (2026-09-30) on Manim licensing and plugin conventions, prior HEP/Feynman Manim work, mplhep and cmsstyle, experiment logo and label policies, Claude Code plugin and marketplace mechanics, Codex's `AGENTS.md` and skills support, and name availability. Sources are linked where used.

## 15. Out of scope for v0.1
- manim-slides adapter, PowerPoint final-shot export, voiceover.
- Codex subagents (TOML), plugin `userConfig` options, hooks, an MCP server.
- conda-forge package.
- KM3NeT preset and content; ALICE and DUNE presets (mplhep has them; easy community additions).
- The port backlog (§8.4), including the 3D LHCb spectrometer.
- Public data examples (Open Data with DOIs).

## 16. To verify during implementation
1. **Manim 0.21:**
   - re-validate the trap list (whether the last-frame bug is still present, the MathTex cache race, `-qh` parsing);
   - PyAV-only frame extraction (no system ffmpeg);
   - that `register_font` works for bundled fonts on Linux, macOS and Windows.
2. **LaTeX:** the minimal working package set per platform (MiKTeX on Windows, BasicTeX on macOS).
3. **CMS Open Data labels:** the exact public label wording for Open Data results.
4. **CI:** whether `claude plugin validate` runs in CI without an API key.
5. **Codex:** whether its plugin marketplace accepts the Claude-format `marketplace.json` and `plugin.json`.
6. **Storyline artifacts:** how the `hep-storyline` skill detects that artifacts are available, and how keyframes are embedded in the published page.
7. **Colour vision:** choose the simulation model (e.g. Machado 2009) and the colour-distance metric (e.g. CIEDE2000) for the check in §6.2, then confirm that the experiment cycles taken from mplhep meet the Okabe–Ito baseline. If one doesn't, document the exception rather than altering the official palette.
