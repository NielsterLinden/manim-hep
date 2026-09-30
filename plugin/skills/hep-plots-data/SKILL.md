---
name: hep-plots-data
description: Turn analysis results into animated HEP plots with manim-hep. Freeze numbers to JSON with provenance in the analysis environment (extractor template), load them with assertions in the scene, draw step histograms, stacks, error bars, bands and ratio panels, keep the data fixed while predictions move, and decide between recreating a plot and importing the figure. Use when a clip shows real or synthetic data, histograms, fits, limits or any result plot.
---

# Plots and data

## Two environments, one frozen file

- **The analysis environment** (ROOT, uproot, awkward, pandas, torch) runs an
  **extractor** that writes `<root>/data/<name>.json` with `manim_hep.data.freeze`. Start
  from [extractor_template.py](extractor_template.py).
- **The scene** never imports the analysis stack. It loads the frozen file and asserts the
  numbers the storyline promised:

  ```python
  values = load_frozen(DATA / "zmumu.json", expect={"n_events": 131_072, "lumi_fb": 16.4})
  ```

  A mismatch raises `FrozenDataError` and stops the render. **Never fix a number in the
  scene:** report the discrepancy.
- **Provenance** is recorded automatically:
  - `source`, `selection` and `version`, as you give them;
  - the time and the producing script;
  - the git commit and dirty flag of the analysis repository. Freeze from a clean checkout
    when you can.
- **The drift guard.** Re-run the extractor after delivery and diff the JSON. If it
  changed, the clip is out of date.
- **Hand-written freezes are for literature constants only**, each with its own `source`
  (PDG year, DOI).
- **Synthetic data** (explainers, gallery examples) are generated in the scene with a
  seeded `np.random.default_rng(...)`, and the storyline declares them synthetic.

## Drawing results

1. **Position the axes first.**

   ```python
   axes = DataAxes((60, 120), (0, 900), x_title="m<sub>μμ</sub> [GeV]",
                   y_title="Events / 2 GeV", show_x_labels=False).move_frame_to((0.5, 0.4))
   ```

   Then build every object through `axes.c2p`.
2. **Histograms are step outlines** (`step_hist`): the polyline *is* the binning. Overlay
   at most three steps.
3. **Stacks** (`stack_hist`) list layers bottom first. Every layer keeps its point count,
   so `Transform(old_stack, new_stack)` morphs bin by bin, even when a layer starts at zero.
4. **Data points** use `errorbars(axes, centres, counts, yerr=np.sqrt(counts))`, capless.
   Asymmetric errors take `yerr=(low, high)`.
5. **Uncertainty bands** use `band(axes, edges, low, high, step=True)`.
6. **Ratio panels** use
   `ratio_panel(axes, edges, data, prediction, num_err=np.sqrt(data), x_title=...)` under
   the main axes, which were built with `show_x_labels=False`.
7. **Log scales** use `DataAxes(..., log_y=True, y_floor=...)`. Empty bins sit on the floor
   instead of breaking the log.
8. **"The data never move."** When the prediction changes (a background added, a fit
   applied), only the prediction and the ratio animate; the data points stay exactly where
   they are.
9. **Labels.** Experiment labels go through `label(...)` with an explicit status (see
   `hep-experiment-style`).

## Recreate or import?

| Situation | Do |
|---|---|
| You will animate the plot (build-up, a morph, highlighting a bin, a fit converging) | **Recreate** it natively from frozen numbers |
| The deck's style must match (fonts, colours) | **Recreate** |
| A dense approved figure (many curves, 2D contours, official layout) shown static | **Import** it: export PNG at ≥ 200 dpi (or SVG), then `ImageMobject(path)` or `SVGMobject(path)`, unmodified |
| Approved figure, but you want to point at something | Import it; overlay a highlight shape on top and never edit the figure itself |

## Fits and statistics clips

- **Fitted values.** Compute them with the real likelihood in the extractor (or, for
  synthetic explainers, in the scene with a seed), and draw from the result. Never hand-tune
  a curve to "look right".
- **Parabolas and scans.** A −2ΔlnL parabola or scan shows the actual scan points. The
  minimum and interval come from the fit result, not from reading the geometry.
