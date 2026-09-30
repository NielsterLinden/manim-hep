# CMS: contributions welcome

Experiment-specific animations go here: detector overviews, trigger chains,
reconstruction steps and analysis ideas that only make sense for CMS.

Rules for this folder:

- use the `cms` theme (`use_theme("cms")`) and `label("cms", status=...)` with an
  explicit status;
- use no official geometry you may not redistribute, and never add collaboration logos
  (a scene may load a logo file the user supplies with `manim_hep.logo(path)`);
- use synthetic data, or public data with a DOI.

Generic detector animations live in [`../generic/`](../generic/), and CMS-styled
result plots in [`../../plots/cms/`](../../plots/cms/). Changes here are reviewed by
the CMS code owners (see `.github/CODEOWNERS`).
