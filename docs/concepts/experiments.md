# Experiments and labels

!!! note
    Not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. The presets follow
    public conventions. Your collaboration's approval rules still apply to anything you
    show.

## Presets

`use_theme("atlas" | "cms" | "cms-opendata" | "lhcb")` sets the colour cycle and font
from [mplhep](https://github.com/scikit-hep/mplhep)'s styles (`ATLAS`, `CMS`, `LHCb2`).
- **Fonts.** The exact experiment fonts (TeX Gyre Heros / Termes) need
  `pip install "manim-hep[mplhep]"`; without it, text uses the bundled DejaVu Sans.
- **Parity.** A test checks the presets against mplhep.

## Labels need an explicit status

```python
label("atlas", status="Simulation", sqrt_s=13.6, target=axes)       # ATLAS Simulation
label("atlas", status=None, sqrt_s=13, lumi=140)                    # bare "ATLAS" (papers)
label("cms", status="Private work", lumi=138, sqrt_s=13, loc="above", target=axes)
label("lhcb", status="Unofficial", sqrt_s=13, loc="upper right", target=axes)
```

`status` has no default, and it must be one of the experiment's statuses. A wrong one,
including a wrong capitalisation, raises an error that lists the valid ones.

| Experiment | Allowed statuses |
|---|---|
| ATLAS | Internal, Preliminary, Simulation, Simulation Internal, Simulation Preliminary, Work in Progress, or `None` |
| CMS | Preliminary, Simulation, Simulation Preliminary, Supplementary, Work in progress, Private work |
| LHCb | Preliminary, Unofficial, Simulation |
| CMS Open Data | `None`, Simulation, Private work (and a DOI is required) |

Which status a result may carry is decided by your collaboration's approval process, never
by manim-hep or an agent.

## CMS Open Data

CMS Open Data are released under CC0. The CMS data policy says neither CMS nor CERN
endorse works made with them, and asks users to cite the dataset DOIs.

`label("cms-opendata", status=None, doi=[...])` shows "CMS Open Data" in plain weight,
deliberately not in the bold and italic style of official CMS figures. It always adds "Not
endorsed by CMS or CERN" and the DOIs.

No public CMS rule fixes the header wording for Open Data results; this choice is
manim-hep's own, made to stay clearly apart from official figures.

## Logos

No collaboration logos ship with manim-hep, and agents never download or redraw one.
`logo(path)` only loads a file you supply. Check first that you may use it:
- ATLAS requires prior written approval;
- CMS, LHCb and KM3NeT publish no general reuse grant.
