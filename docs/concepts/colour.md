# Colour

Scenes take every colour from the theme's **roles**, never from literals:

```python
C = use_theme().palette
C.ink         # text, axes, outlines (dark slate)
C.muted       # guides, extrapolations, secondary lines
C.data        # data points
C.theory      # predictions, theory curves
C.detector    # detector layers (drawn as tints)
C.highlight   # the one "look here" colour
C.cycle       # categorical colours: processes in a stack, several tracks
```

`tint`, `shade` and `mix` derive lighter or darker variants. `manim_hep.palette` does not
import Manim, so matplotlib scripts for the static figures of a talk can use the same hex
values.

## Colour-vision deficiency

The default palette is Okabe–Ito-based. A test simulates protanopia, deuteranopia and
tritanopia (Machado et al. 2009, severity 1) and measures the smallest CIEDE2000 distance
between any two colours of each cycle. Every shipped cycle must be at least as
distinguishable as the Okabe–Ito colours, with these documented exceptions:

| Cycle | Deuteranopia | Protanopia | Tritanopia | Closest pair |
|---|---|---|---|---|
| Okabe–Ito (baseline) | 11.6 | 12.2 | 10.9 | — |
| `generic`, `atlas` | 11.6 | 12.2 | 10.9 | — |
| `cms`, `cms-opendata` (Petroff 6) | 14.7 | **10.6** | 18.3 | `#964a8b` / `#7a21dd` (protanopia) |
| `lhcb` (mplhep LHCb2) | **0.2** | **4.2** | **4.2** | `#00CC00` / `#FF7733` (deuteranopia) |

The CMS and LHCb cycles ship unchanged, because they follow the experiments' published
conventions. When distinguishability matters in those themes:
- use the first few colours of the cycle;
- add a second cue: line style, position, or a direct label.
