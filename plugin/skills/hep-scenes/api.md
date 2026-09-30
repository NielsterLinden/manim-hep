# manim-hep 0.1 API (import from `manim_hep` or the submodule)

This page documents the same release as the installed package. When in doubt, read the
docstring: `python -c "import manim_hep.plots as m; help(m.DataAxes)"`.

## Theme: `manim_hep.style`

- `use_theme(name=None) -> Theme`: `generic` | `atlas` | `cms` | `cms-opendata` | `lhcb`.
  - With no name, it reads `[style] experiment` from the nearest `manim-hep.toml`.
  - It sets the background, and the ink colour and font defaults for shapes and text.
- `Theme` fields: `experiment`, `palette`, `font`, `title_band` (2.7) and `keep_out`.
  Properties: `content_box` `(x0, y0, x1, y1)` and `content_center` (point).
- `current_theme() -> Theme`.
- `intrusions(mobject, theme=None) -> list[str]` returns a subset of `"frame"`,
  `"title band"` and `"keep-out N"`; an empty list is good.

## Colours: `manim_hep.palette` (no Manim import)

- `Palette` roles: `background`, `ink`, `muted`, `data`, `theory`, `detector`, `highlight`,
  `cycle` (tuple).
- `DEFAULT`: Okabe–Ito on white.
- `OKABE_ITO`: the 8 colours, black first.
- `tint(c, amount)` moves toward white; `shade(c, amount)` toward black;
  `mix(a, b, t)`; `to_rgb(c)`; `to_hex(rgb)`.

## Experiment labels: `manim_hep.experiments`

- `label(experiment, *, status, lumi=None, sqrt_s=None, loc="upper left", target=None, doi=None, font_size=24, buff=0.2) -> VGroup`
  - `status` is **required**.
    - ATLAS: Internal, Preliminary, Simulation, Simulation Internal, Simulation Preliminary,
      Work in Progress, or `None` for the bare "ATLAS" of papers.
    - CMS: Preliminary, Simulation, Simulation Preliminary, Supplementary, Work in progress,
      Private work.
    - LHCb: Preliminary, Unofficial, Simulation.
    - cms-opendata: `None`, Simulation, Private work; also needs `doi=`.
  - `lumi` is in fb⁻¹ and `sqrt_s` in TeV (numbers or verbatim strings).
  - `loc` is `"upper left"`, `"upper right"` or `"above"` (CMS style: name top-left, lumi
    top-right, outside the frame).
  - `target` is a `DataAxes` (its plot frame is used) or any mobject; the default is the
    content area.
  - The result has `.main`, `.info`, `.note` (the Open Data note) and `.plain` (the text).
- `logo(path, *, height=0.6) -> Mobject` loads an `.svg`, `.png` or `.jpg` that the user
  supplied. No logos ship.

## State-first helpers: `manim_hep.build`

- `add_state(scene, builder) -> dict`: `builder` is a dict of mobjects or a function
  returning one; the values are added in dict order.
- `check_order(scene, expected)`: `expected` is a dict or a list. It asserts the scene
  holds exactly these top-level objects, in drawing order; wait placeholders and
  `ValueTracker`s are ignored.
- `place(mobject, placement, natural_center=ORIGIN) -> mobject`: `placement` is `(x, y)`,
  or `(scale, (x, y))` (scale about `natural_center`, then move it there).

## Frozen numbers: `manim_hep.data`

- `freeze(values, path, *, source, selection=None, version=None) -> Path` writes JSON with
  provenance: the time, the producing script, and the git commit plus dirty flag.
- `load_frozen(path, *, expect=None, rtol=1e-9) -> dict`. Any mismatch with `expect`
  raises `FrozenDataError` listing every problem.

## Feynman diagrams: `manim_hep.feynman`

- `FeynmanDiagram(vertices, edges, *, label_buff=0.18, label_size=40, color=None)`
  - `vertices` maps a name to `(x, y)`.
  - `edges` holds `(a, b, kind)` or `(a, b, kind, label)`; `label` is a LaTeX string
    (MathTex) or a mobject.
  - `kind` is one of `fermion`, `antifermion`, `photon`, `boson` (wavy, for W/Z), `gluon`
    (curly), `scalar` (dashed) or `plain`.
  - Attributes: `.lines`, `.labels`, `.dots` (internal vertices), `.edge_labels`,
    `.edge(a, b)`.
  - `.draw_in_order(time_per_edge=0.6)` returns one animation that keeps the diagram a
    single group.
- Primitives:
  - `fermion(start, end, *, arrow=True)`: mid-arrow along start → end;
  - `photon(start, end, *, amplitude=0.09, wavelength=0.45)`;
  - `gluon(start, end, *, radius=0.12, loops=None)`;
  - `scalar(start, end)`;
  - `vertex(point)`.

## Plots: `manim_hep.plots`

- `DataAxes(x_range, y_range, *, x_length=7.0, y_length=4.0, x_ticks=None, y_ticks=None, x_fmt="{:g}", y_fmt="{:g}", x_title=None, y_title=None, log_y=False, y_floor=None, show_x_labels=True, show_y_labels=True, tick_height=0.2, tick_length=0.1, stroke_width=2.5, color=None)`
  - Ranges are `(low, high)` in data units; log ranges are real values.
  - Titles: a `str` is rendered as MarkupText (`m<sub>μμ</sub> [GeV]`); a `MathTex` is used
    as is.
  - Methods: `.c2p(x, y)`, `.p2c(point)`, `.move_frame_to(point)`,
    `.plot(f, *, x_range=None, samples=200, color=None)` and `.polyline(xs, ys)`.
  - Attributes: `.frame`, `.x_ticks`, `.y_ticks`, `.x_labels`, `.y_labels`, `.y_base`.
- `step_hist(axes, edges, counts, *, color=None, stroke_width=3.0, fill_opacity=0.0)`.
- `stack_hist(axes, edges, layers, *, stroke_width=0.0, fill_opacity=0.95)`
  - `layers` holds `(name, counts[, color])`, bottom first; the colours default to the
    theme cycle.
  - The result has `.layer[name]`, `.names`, `.counts`, `.cum` and `.total`, and keeps a
    fixed point count, so `Transform` works between two stacks.
- `errorbars(axes, x, y, yerr, *, xerr=None, color=None, radius=0.05)`, capless.
  - `yerr` is a scalar, one value per point, or `(low, high)`.
  - Each point is `VGroup(dot, bar[, xbar])`.
- `band(axes, x, low, high, *, color=None, opacity=0.25, step=False)`. With `step=True`,
  `x` are bin edges.
- `ratio_panel(main, edges, num, den, *, y_range=(0.5, 1.5), y_length=1.2, y_ticks=None, num_err=None, gap=0.12, y_title="Data / Pred.", x_title=None, color=None)`
  - It sits under `main` and lines up with it. Build `main` with `show_x_labels=False`.
  - The result has `.axes`, `.ref`, `.dots`, `.errs`, `.ratio` and `.bins`.

## Detector: `manim_hep.detector`

- `BarrelSlice(radii=None, *, center=ORIGIN, tracker_layers=5, ecal_cells=72, hcal_cells=36, muon_stations=3)`
  - Layers: `beam_pipe`, `tracker`, `solenoid`, `ecal`, `hcal`, `muon`. Override any
    `(inner, outer)` pair.
  - `.layers` is ordered inside out.
  - `.radius(name)` and `.point_at(r, phi)` follow moves and scaling; `.ip` is the centre,
    `.scale_factor` the scaling.
- `track(pt, charge, field, *, phi=0.0, r_max=1.0, origin=ORIGIN, scale=1.0, color=None, stroke_width=3.5)`
  - `pt` in GeV, `field` in T (positive: out of the screen), `scale` in units per metre.
  - The radius is R = pT / (0.3 |q| B).
- `signature(kind, detector, *, phi=0.0, charge=-1, pt=None, field=3.8, seed=0)`
  - `kind` is one of `electron`, `muon`, `photon`, `jet`, `tau1`, `tau3`, `neutrino`.
  - The result has `.tracks`, `.deposits` and `.hits`.

## Command line

- `manim-hep doctor [--no-tex]`
- `manim-hep init [--root DIR] [--agent claude|codex|both|none] [--experiment X]`
- `manim-hep render FILE SCENE [--final] [--frames 1.5,3] [--slug S]`
- `manim-hep lint [PATHS]`
- `manim-hep seam A.mp4 B.mp4`
