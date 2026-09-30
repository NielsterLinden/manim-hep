# Agentic Manim for HEP (`manim-hep`)

> **Work in progress:** not yet released; expect changes until v0.1.0.

High-energy-physics animations with [Manim Community Edition](https://www.manim.community),
with three ways in:

- **Ask an agent.** Paste one sentence into Claude Code, Codex or another coding agent.
  Its skills then:
  - plan a clip with you;
  - build it on tested HEP building blocks;
  - render it, look at the frames;
  - deliver an MP4 for your slides.
- **Import it.** `pip install manim-hep` gives you:
  - experiment themes and status-checked labels (ATLAS, CMS, CMS Open Data, LHCb);
  - Feynman diagrams, HEP-style plots, and a detector slice with tracks and signatures;
  - helpers for seamless chained clips and for numbers with provenance.
- **Work by hand.** Copy an example from the [gallery](gallery/) and adapt it.

## Quick install (with an agent)

In the repository where you want to make animations, give your agent this sentence
(see [QUICKINSTALL.md](QUICKINSTALL.md)):

> Set up manim-hep in this repository: follow https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/AGENT_INSTALL.md, and ask me the setup questions first.

**Claude Code users** can also install the plugin directly:

```
/plugin marketplace add NielsterLinden/manim-hep
/plugin install manim-hep@manim-hep
```

**By hand:** `pip install manim-hep`, then `manim-hep doctor` and `manim-hep init`
([HUMAN_GUIDE](docs/install/HUMAN_GUIDE.md)).

## A taste

```python
import numpy as np
from manim import UL, Create, FadeIn, Scene, Text
from manim_hep import DataAxes, check_order, errorbars, label, stack_hist, use_theme

C = use_theme("cms").palette
rng = np.random.default_rng(1)
edges = np.arange(70.0, 111.0, 2.0)
centres = (edges[:-1] + edges[1:]) / 2
bkg = 45 * np.exp(-0.045 * (centres - 70))
sig = 1300 * np.exp(-0.5 * ((centres - 91.2) / 2.5) ** 2)
data = rng.poisson(bkg + sig).astype(float)       # synthetic


class ZPeak(Scene):
    def construct(self):
        axes = DataAxes((70, 110), (0, 1600), x_title="m<sub>µµ</sub> [GeV]",
                        y_title="Events / 2 GeV").move_frame_to((0.3, -0.5))
        note = Text("Synthetic data", font_size=48, color=C.muted).scale(0.4)
        state = {
            "stack": stack_hist(axes, edges, [("background", bkg), ("Z", sig)]).set_z_index(-1),
            "axes": axes,
            "data": errorbars(axes, centres, data, yerr=np.sqrt(data)),
            "label": label("cms", status="Private work", lumi=50, sqrt_s=13.6,
                           loc="above", target=axes),
            "note": note.move_to(axes.frame.get_corner(UL) + [0.2, -0.2, 0], aligned_edge=UL),
        }
        self.play(FadeIn(axes))
        self.play(Create(state["stack"]), run_time=1.5)
        self.play(FadeIn(state["data"]), FadeIn(state["label"]), FadeIn(state["note"]))
        check_order(self, state)   # exactly these objects, in drawing order
        self.wait(0.1)             # clips end on their last change
```

Render it with `manim-hep render zpeak.py ZPeak`. It writes the clip and its first and last
frames, and checks that nothing is drawn in the slide's title band.

There is **no default status**. `label()` makes you choose one of the experiment's public
statuses; manim-hep never picks "Preliminary" for you. Synthetic data carry a visible
note, so no frame can pass for a real result.

## What is inside

| | |
|---|---|
| **`manim_hep`** | `use_theme`, `label`, `logo`, `FeynmanDiagram`, `DataAxes`, `step_hist`, `stack_hist`, `errorbars`, `band`, `ratio_panel`, `BarrelSlice`, `track`, `signature`, `add_state`, `check_order`, `place`, `freeze`, `load_frozen` |
| **`manim-hep` CLI** | `init` (safe project setup), `doctor` (environment check with fixes per platform), `render` (one render at a time, frame PNGs, safe-area scan, versioned delivery), `lint` (house rules), `seam` (checks joints between chained clips) |
| **Skills** | `hep-animate`, `hep-storyline`, `hep-scenes`, `hep-render-verify`, `hep-physics`, `hep-experiment-style`, `hep-plots-data`, `hep-setup`, `hep-contribute` |
| **Claude agents** | `scene-builder`, `plot-recreator`, `render-verifier` (read-only), `physics-checker` (read-only) |

The agents follow four principles adapted from
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills):
- think before coding;
- simplicity first;
- surgical changes;
- goal-driven execution.

Settings in `manim-hep.toml` decide:
- whether the agent writes a storyline first (and publishes it as an artifact);
- how thoroughly it checks the rendered frames;
- which branch it works on;
- whether it may commit. It never pushes.

## Gallery

Every example renders in CI on seeded synthetic data.

| Topic | Examples |
|---|---|
| Theory | [Drell–Yan diagram](gallery/theory/drell-yan) · [Higgs potential](gallery/theory/higgs-potential) |
| Methods | [Counting experiment](gallery/methods/counting-experiment) · [Significance and ROC](gallery/methods/significance-roc) · [Template fit](gallery/methods/template-fit) |
| Experiments | [Detector signatures](gallery/experiments/generic/detector-signatures) · [Tracks in a field](gallery/experiments/generic/tracks-in-field) · ATLAS, CMS, LHCb, KM3NeT: contributions welcome |
| Plotting results | [Histogram fill](gallery/plots/general/histogram-fill) · [Stack, data, ratio](gallery/plots/general/stack-data-ratio) · [ATLAS](gallery/plots/atlas/labelled-result), [CMS](gallery/plots/cms/labelled-result) and [LHCb](gallery/plots/lhcb/labelled-result) style |
| Machine learning | [Attention](gallery/ml/attention) · [Backpropagation](gallery/ml/backprop) |

About 35 more are waiting to be ported: see the [port backlog](docs/port-backlog.md) and
[CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

manim-hep is a small layer on top of Manim. **All the credit for the animation engine goes
to Grant Sanderson (3Blue1Brown), the 3Blue1Brown team, and the Manim Community developers
who created, maintain and improve Manim.** The author of this library is just a happy user.

> Built on Manim Community Edition (MIT; © 2018 3Blue1Brown LLC, © 2024 the Manim Community
> Developers), originally created by Grant Sanderson (3Blue1Brown).

Style conventions follow [mplhep](https://github.com/scikit-hep/mplhep) and
[cmsstyle](https://github.com/cms-cat/cmsstyle). Full credits are in
[CREDITS.md](CREDITS.md). If you use manim-hep, please cite it
([CITATION.cff](CITATION.cff)), and cite Manim too.

## Disclaimer

Not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. Experiment presets
follow public conventions. Your collaboration's approval rules still apply to anything you
show.

## Licence

MIT; see [LICENSE](LICENSE). The bundled DejaVu fonts keep their own licence.
