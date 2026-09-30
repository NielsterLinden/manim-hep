# Changelog

All notable changes are listed here. The public API is add-only: a breaking change is
only allowed in a new minor version and is always listed below.

## [0.1.0]: unreleased

First release (in development).

### Core package (`manim_hep`)

- **Palette and themes.**
  - `palette`: colour roles, `tint`, `shade` and `mix`, the Okabe–Ito default, and a
    colour-vision-deficiency check in the tests.
  - `use_theme`: themes `generic`, `atlas`, `cms`, `cms-opendata` and `lhcb`, following
    mplhep; bundled DejaVu Sans; a title band and keep-out areas.
- **Experiment labels.** `label` requires an explicit status. The `cms-opendata` variant
  cites DOIs and states non-endorsement. `logo` only loads user-supplied files.
- **Diagrams, plots and detector.**
  - `FeynmanDiagram` and the line primitives, drawn in build order.
  - `DataAxes`, `step_hist`, `stack_hist` (morphable), capless `errorbars`, `band` and
    `ratio_panel`.
  - `BarrelSlice`, `track` (with the correct curvature sign) and `signature`.
- **State and data.** `add_state`, `check_order` and `place` for state-first chained clips;
  `freeze` and `load_frozen` for numbers with provenance.

### Command line (`manim-hep`)

- `init`: safe, idempotent project setup for Claude Code and Codex.
- `doctor`: environment checks, with fixes per platform.
- `render`: serial renders, frame PNGs, safe-area scan, versioned delivery.
- `lint`: the house rules.
- `seam`: checks the joint between chained clips.

### Agent layer

- The `manim-hep` Claude Code plugin and marketplace.
- Nine skills: `hep-animate`, `hep-storyline`, `hep-scenes`, `hep-render-verify`,
  `hep-physics`, `hep-experiment-style`, `hep-plots-data`, `hep-setup` and `hep-contribute`.
- Four agents: `scene-builder`, `plot-recreator`, `render-verifier` and `physics-checker`.

### Gallery

- The starter set of 14 examples: theory, methods, generic experiments, plots (general,
  ATLAS, CMS, LHCb) and machine learning.
