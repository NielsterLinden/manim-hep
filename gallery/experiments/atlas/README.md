# ATLAS: contributions welcome

Experiment-specific animations go here: detector overviews, trigger chains,
reconstruction steps and analysis ideas that only make sense for ATLAS.

Rules for this folder:

- use the `atlas` theme (`use_theme("atlas")`) and `label("atlas", status=...)` with an
  explicit status;
- use no official geometry you may not redistribute, and never add collaboration logos
  (a scene may load a logo file the user supplies with `manim_hep.logo(path)`);
- use synthetic data, or public data with a DOI.

Generic detector animations live in [`../generic/`](../generic/), and ATLAS-styled
result plots in [`../../plots/atlas/`](../../plots/atlas/). Changes here are reviewed by
the ATLAS code owners (see `.github/CODEOWNERS`).
