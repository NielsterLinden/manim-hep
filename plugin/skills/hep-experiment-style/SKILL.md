---
name: hep-experiment-style
description: Style animations for ATLAS, CMS or LHCb with manim-hep. Covers the experiment presets (colour cycles and fonts following mplhep), labels with an explicit status (Preliminary, Simulation, Internal, Work in progress, Private work, Unofficial, Supplementary), CMS Open Data labels with DOIs and the non-endorsement note, and the logo policy. Use when a clip shows an experiment's result, style or label, or when the user asks for an ATLAS, CMS or LHCb label or logo.
---

# Experiment styles, labels and logos

manim-hep is not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. The
presets follow public conventions. **Your collaboration's figure and approval rules always
apply**, and they decide what you may show and with which label.

## Presets

| `use_theme(...)` | Colour cycle | Font |
|---|---|---|
| `generic` | Okabe–Ito | DejaVu Sans (bundled) |
| `atlas` | mplhep `ATLAS` (Okabe–Ito order) | TeX Gyre Heros* |
| `cms` / `cms-opendata` | mplhep `CMS` (Petroff 6, arXiv:2107.02270) | TeX Gyre Heros* |
| `lhcb` | mplhep `LHCb2` | TeX Gyre Termes* |

\* With `pip install "manim-hep[mplhep]"`; otherwise DejaVu Sans. A test checks the cycles
and fonts against mplhep.

- **Colour-vision deficiency.** The CMS and LHCb cycles fall below the Okabe–Ito baseline
  under some colour-vision deficiencies. They ship unchanged, because they are the official
  choices. When distinguishability matters, prefer the first colours of the cycle, and add a
  second cue (line style, position, label).
- **Where the theme comes from.** Set the theme once per project in `manim-hep.toml`
  (`[style] experiment = "cms"`). Pass a name only in experiment-specific scenes.

## Labels: `label(experiment, *, status, ...)`

`status` is **required**. Ask the user which status their result may carry; never choose
"Preliminary", "Internal" or a bare label for them. The typical meanings are below. The
collaboration's own guidelines are the authority, so check them.

| Experiment | Status | Typical use |
|---|---|---|
| ATLAS | `Internal` | internal meetings and documents only; never in public |
| ATLAS | `Preliminary` | approved preliminary results (conference notes) |
| ATLAS | `Simulation`, `Simulation Internal`, `Simulation Preliminary` | plots of simulation only |
| ATLAS | `Work in Progress` | a result still under way |
| ATLAS | `None` (bare "ATLAS") | published results (papers) |
| CMS | `Preliminary` | approved preliminary results (PAS) |
| CMS | `Simulation`, `Simulation Preliminary` | simulation only |
| CMS | `Supplementary` | additional material for a publication |
| CMS | `Work in progress` | ongoing work |
| CMS | `Private work` | plots made by individuals (e.g. theses) that CMS has not approved |
| LHCb | `Preliminary` | approved preliminary results |
| LHCb | `Unofficial` | not approved by LHCb |
| LHCb | `Simulation` | simulation only |

Placement follows each experiment's habit:
- **ATLAS:** inside, upper left, with √s and luminosity on the line below.
- **CMS:** `loc="above"`, with "CMS *status*" top left and "lumi (√s)" top right, outside
  the frame.
- **LHCb:** inside, upper right.

```python
lab = label("cms", status="Private work", lumi=138, sqrt_s=13, loc="above", target=axes)
```

## Open Data

The CMS Open Data portal releases data under **CC0**. The CMS data policy says neither CMS
nor CERN endorse works made with them, and asks users to cite the dataset DOIs.

- Use `label("cms-opendata", status=None, doi=[...], lumi=..., sqrt_s=...)`.
  - It sets "CMS Open Data" in plain weight, deliberately not the bold and italic look of
    official CMS figures.
  - It always adds "Not endorsed by CMS or CERN" and the DOIs.
- Never put an official CMS status ("Preliminary", "Supplementary") on Open Data results.
- Cite the dataset DOIs in the talk as well.

## Logos

- **None ship with manim-hep, and you never download, trace or redraw one.**
- **Using a logo.** Only use a file the user gives you: `logo("assets/experiment.svg")`.
  Before showing it, confirm with the user that they may use it:
  - ATLAS requires prior written approval;
  - CMS, LHCb and KM3NeT publish no general reuse grant.
- **Neutral geometry.** Detector geometry derived from a logo counts as the logo. Use the
  neutral `BarrelSlice`.

## When the user asks for "official" style

1. Use the preset and an explicit status.
2. Keep official figures unmodified. To show an approved figure itself, import the image
   (see `hep-plots-data`) rather than recreating it.
3. Remind the user that approved figures often must be shown exactly as approved.
