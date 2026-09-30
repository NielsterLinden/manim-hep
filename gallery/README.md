# Gallery

Self-contained examples, by topic. Each folder holds three files:
- `scene.py`, which imports only `manim`, `manim_hep`, NumPy and the standard library,
  and uses seeded synthetic data;
- `README.md`, saying what the example shows, with the physics sources and how to adapt it;
- `storyline.md`, the plan the example was built from.

CI renders every example.

| Folder | Example | Shows |
|---|---|---|
| `theory/` | [drell-yan](theory/drell-yan) | q q̄ → γ*/Z → ℓ⁺ℓ⁻, drawn in build order |
| | [higgs-potential](theory/higgs-potential) | The double well, the vacuum at v, and m_H from λ |
| `methods/` | [counting-experiment](methods/counting-experiment) | A rare signal tallied against background |
| | [significance-roc](methods/significance-roc) | A threshold sweep, the ROC curve and Z(cut) |
| | [template-fit](methods/template-fit) | Templates, pseudo-data, a signal-strength slider, −2ΔlnL |
| `experiments/generic/` | [detector-signatures](experiments/generic/detector-signatures) | A barrel detector built inside-out; e, μ, γ, jet, ν |
| | [tracks-in-field](experiments/generic/tracks-in-field) | The curvature sign from the charge, the radius from pT |
| `experiments/atlas, cms, lhcb, km3net/` | | Contributions welcome |
| `plots/general/` | [histogram-fill](plots/general/histogram-fill) | One event → one entry → the histogram fills |
| | [stack-data-ratio](plots/general/stack-data-ratio) | Stack, data, ratio: the data never move |
| `plots/atlas, cms, lhcb/` | labelled-result ([ATLAS](plots/atlas/labelled-result), [CMS](plots/cms/labelled-result), [LHCb](plots/lhcb/labelled-result)) | One result in each experiment's style, with an explicit status |
| `ml/` | [attention](ml/attention) | Q·Kᵀ scores, softmax rows, a weighted value update |
| | [backprop](ml/backprop) | A forward pass, the loss, gradients flowing back |

## Run one

```bash
pip install manim-hep
manim-hep render gallery/theory/drell-yan/scene.py DrellYan
```

The scene names are listed in each example's README header (`scenes:`). `render` writes
the clip and its first and last frames to `.manim-hep/work/<name>/`.

## Add one

Copy [`_template/`](_template), then read [CONTRIBUTING.md](../CONTRIBUTING.md). Ideas
waiting for a contributor are in the [port backlog](../docs/port-backlog.md).
