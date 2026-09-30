# LHCb: contributions welcome

Experiment-specific animations go here: detector overviews, trigger chains,
reconstruction steps and analysis ideas that only make sense for LHCb.

Rules for this folder:

- use the `lhcb` theme (`use_theme("lhcb")`) and `label("lhcb", status=...)` with an
  explicit status;
- use no official geometry you may not redistribute, and never add collaboration logos
  (a scene may load a logo file the user supplies with `manim_hep.logo(path)`);
- use synthetic data, or public data with a DOI.

Generic detector animations live in [`../generic/`](../generic/), and LHCb-styled
result plots in [`../../plots/lhcb/`](../../plots/lhcb/). Changes here are reviewed by
the LHCb code owners (see `.github/CODEOWNERS`).
