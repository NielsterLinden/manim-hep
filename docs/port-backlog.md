# Port backlog

These animations exist in talks that manim-hep grew from, or are standard HEP explainers.
They are not in the gallery yet. Each one becomes a **"Port this"** issue (label `port`;
`good first issue` where marked ★) once the repository is public. Re-implement each on
synthetic or public data, and cite every physics source.

## Theory

| # | Example | What it shows | Core pieces |
|---|---|---|---|
| 1 | `theory/tau-decay` ★ | τ → ν W* → pions; the boost collimates them into a narrow jet; π⁰ → γγ | `FeynmanDiagram`, `signature("tau1"/"tau3")` |
| 2 | `theory/factorisation` | x₁P and x₂P from two protons; σ = Σ ∫ f f σ̂; the PDFs as curves | `DataAxes.plot`, `MathTex` |
| 3 | `theory/perturbative-orders` | LO → NLO → NNLO → N³LO: the prediction band shrinks | `band`, `DataAxes` |
| 4 | `theory/prediction-band` | The uncertainty builds up: scale, then α_s, then PDF | `band` |
| 5 | `theory/lepton-universality` | The (g_A, g_V) plane per lepton flavour; sin²θ_W | `DataAxes`, ellipses |
| 6 | `theory/lambda-running` | One-loop β_λ; λ(μ) runs negative at high scales (with a literature citation) | `DataAxes.plot` |
| 7 | `theory/top-loop` ★ | The quartic Higgs vertex gets a top-quark box correction | `FeynmanDiagram` |
| 8 | `theory/yukawa-hierarchy` ★ | y_f ∝ m_f across the fermions, on a log scale | `DataAxes(log_y=True)` |
| 9 | `theory/sm-particles` | A Standard Model particle table, designed from scratch (no share-alike layouts) | new: `ParticleTable` |
| 10 | `theory/top-decay` ★ | t → bW, W → ℓν or qq̄ | `FeynmanDiagram` |
| 11 | `theory/fiducial-cross-section` | A generator-level spectrum; counting in a fiducial window gives σ | `step_hist`, `band` |
| 12 | `theory/line-shapes` ★ | Breit–Wigner versus double-sided Crystal Ball; the radiative tail | `DataAxes.plot` |

## Methods

| # | Example | What it shows | Core pieces |
|---|---|---|---|
| 13 | `methods/tag-and-probe` | Tag and probe; pass/fail panels; efficiency in data and simulation; scale factors | `DataAxes`, `errorbars` |
| 14 | `methods/fake-factor` | A same-sign control region; the fake factor; closure | `stack_hist` |
| 15 | `methods/trigger-chain` | 40 MHz → L1 → HLT → storage, with rates (generic numbers) | new: rate funnel |
| 16 | `methods/analysis-map` | The theory and experiment rows meet: selection → corrections → fit → σ | new: `spine` |
| 17 | `methods/cuts-vs-ml` ★ | Rectangular cuts on overlapping 2D clouds versus a learned boundary | `DataAxes`, dots |
| 18 | `methods/pulls` | Nuisance parameters, pre-fit versus post-fit pulls | new: `pull_plot` |
| 19 | `methods/combination` | Three channels combine into one result | `errorbars`, `band` |
| 20 | `methods/reweighting` | Pileup reweighting morphs a distribution | `step_hist`, `Transform` |
| 21 | `methods/invariant-mass` | Tracks → four-momenta → m² → one histogram entry | `BarrelSlice`, `DataAxes` |
| 22 | `methods/limit-setting` | CLs and the "Brazil band" of expected limits | `band`, `DataAxes.polyline` |

## Experiments

| # | Example | What it shows | Core pieces |
|---|---|---|---|
| 23 | `experiments/generic/lhc-ring` ★ | Counter-rotating bunches, a √s counter, the collision | new |
| 24 | `experiments/generic/forward-spectrometer` | A side view: dipole, tracking stations, calorimeters, muon system; a 3D extrusion as a follow-up | new: `SideView` |
| 25 | `experiments/generic/em-shower` ★ | An electromagnetic shower's branching tree in a calorimeter | new: `shower_tree` |
| 26 | `experiments/generic/jet-clustering` | Particles → anti-kT jets | new |
| 27 | `experiments/km3net/cherenkov` | A muon track's Cherenkov cone reaching optical modules | new (see dvnanima) |

## Plotting results

| # | Example | What it shows | Core pieces |
|---|---|---|---|
| 28 | `plots/general/result-summary` | Measurements as points with a theory band and the value | `errorbars`, `band`, `label` |
| 29 | `plots/general/log-rain` ★ | A fill that switches from linear to log y as statistics grow | `DataAxes(log_y=True)` |
| 30 | `plots/general/mass-peak-marks` | Reference line, tolerance band, FWHM arrows, peak versus mean | `DataAxes.plot`, `band` |

## Machine learning

| # | Example | What it shows | Core pieces |
|---|---|---|---|
| 31 | `ml/event-tokens` | An event becomes rows of tokens | new |
| 32 | `ml/embeddings` ★ | One-hot versus learned versus frozen embeddings | new |
| 33 | `ml/mlp-to-kan` | Edge splines replace fixed activations | `DataAxes.plot` |
| 34 | `ml/bdt` | Decision-tree splits, the score, categories | `DataAxes`, `step_hist` |
| 35 | `ml/transformer-forward` | A full forward pass: tokens → attention → feed-forward → logits (builds on `ml/attention`) | new |
