# Credits

manim-hep is a small layer on top of other people's work. We are grateful to all of them.

## Manim

All the credit for the animation engine goes to **Grant Sanderson** (3Blue1Brown), who
created Manim, and to **the Manim Community developers**, who maintain and improve Manim
Community Edition. The author of manim-hep is just a happy user.

> Built on Manim Community Edition (MIT; © 2018 3Blue1Brown LLC, © 2024 the Manim Community
> Developers), originally created by Grant Sanderson (3Blue1Brown).

- Manim Community Edition: https://github.com/ManimCommunity/manim, and
  https://www.manim.community
- 3Blue1Brown's ManimGL: https://github.com/3b1b/manim

If manim-hep helps you, please also cite Manim through its
[CITATION.cff](https://github.com/ManimCommunity/manim/blob/main/CITATION.cff).

## The four coding principles

The rules the agents follow (see `AGENTS.md` and the `hep-animate` skill) adapt four
principles:
- **Think Before Coding**
- **Simplicity First**
- **Surgical Changes**
- **Goal-Driven Execution**

They come from Jiayuan Zhang's
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), which distils
[Andrej Karpathy's notes on coding with LLMs](https://x.com/karpathy/status/2015883857489522876)
(26 January 2026). Karpathy wrote the observations; Zhang wrote the principles. The wording
here is our own, adapted to HEP animation.

## HEP style conventions

- **[mplhep](https://github.com/scikit-hep/mplhep)** (Scikit-HEP): the experiment colour
  cycles, fonts and label conventions that the manim-hep presets follow. With
  `manim-hep[mplhep]`, the TeX Gyre fonts come from mplhep's font package, under their own
  (GUST Font) licence.
- **[cmsstyle](https://github.com/cms-cat/cmsstyle)**: the CMS figure conventions.
- **CMS colour palettes** by M. A. Petroff, "Accessible Color Sequences for Data
  Visualization", arXiv:2107.02270.
- **The Okabe–Ito palette**: M. Okabe and K. Ito, "Color Universal Design" (2002).

## Colour-vision science (in the tests)

- G. M. Machado, M. M. Oliveira and L. A. F. Fernandes, "A Physiologically-based Model for
  Simulation of Color Vision Deficiency", IEEE TVCG 15 (2009) 1291.
- G. Sharma, W. Wu and E. N. Dalal, "The CIEDE2000 Color-Difference Formula",
  Color Res. Appl. 30 (2005) 21.

## Fonts

- **DejaVu Sans** is bundled in `src/manim_hep/fonts/`: © Bitstream (Bitstream Vera), with
  the DejaVu changes in the public domain. See `LICENSE_DEJAVU`.

## Related projects

- **[feynmanim](https://github.com/PTremper/feynmanim)** draws Feynman diagrams in Manim.
- **[dvnanima](https://github.com/NeutrinoHit/dvnanima)** animates neutrino interactions,
  Cherenkov light and air showers.

## Where the practices come from

The workflow, house rules, verification thresholds and trap list were distilled from three
talks built with Manim and coding agents:
- an ATLAS MSc thesis;
- an LHCb summer project;
- a CMS Open Data school.

The gallery examples re-implement ideas from those talks on synthetic data. No code, text,
data or assets were copied from them.

## Disclaimer

Not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. Experiment presets
follow public conventions. Your collaboration's approval rules still apply to anything you
show.
