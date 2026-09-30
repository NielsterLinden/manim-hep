---
name: hep-setup
description: Install and set up manim-hep in a repository, following the agent install procedure (setup questions, manim-hep doctor, manim-hep init, a smoke render and a hand-back report), with per-platform notes for Windows, macOS, Linux, lxplus and batch clusters, and troubleshooting for Manim, LaTeX and fonts. Use when the user asks to install, set up or configure manim-hep, when manim-hep doctor fails, or when manim-hep.toml is missing.
---

# Setting up manim-hep

The canonical procedure is
[docs/install/AGENT_INSTALL.md](https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/AGENT_INSTALL.md).
If you can read it, follow it. The summary below is the same procedure.

## Phase 0: ask first (one message, with defaults)

1. The experiment preset: generic, atlas, cms, cms-opendata or lhcb (default generic).
2. The OS or cluster: Windows, macOS, Linux, lxplus, another cluster.
3. conda or pip, and which environment to install into.
4. Is a full LaTeX available? (Without it, scenes must avoid `MathTex`.)
5. `paths.root`: where scenes, storylines, data and clips live (default `.`; for example
   `presentation`).
6. The four agent settings, with defaults: storyline `artifact`, verify `frames`, branch
   `feature`, commit `ask`.
7. Files that must not be touched.
8. Whether you may commit the setup.

## Phase 1: probe

- Run `pip install manim-hep` (or `"manim-hep[mplhep]"` for exact experiment fonts), then
  `manim-hep doctor`.
- **Gate:** doctor ends with "all good", or every `[FAIL]` has a fix the user has seen.
- Big installs (LaTeX, system libraries) are the user's. Print the doctor's fix commands;
  do not start long installs mid-turn unless the user tells you to.

## Phase 2: scaffold

- Run `manim-hep init --root <root> --agent <claude|codex|both|none> --experiment <preset>`.
- Then set the four `[agent]` values in `manim-hep.toml` from the answers.
- **Gate 1:** `init` exits 0. If it wrote a `<file>.manim-hep.new`, show the user both
  versions and merge by hand. Never overwrite their file.
- **Gate 2:** grep the new files for unfilled placeholders (`<...>` in capitals). There must
  be none.

## Phase 3: smoke test

- Run `manim-hep render <root>/scenes/smoke_test.py SmokeTest`.
- Open `.manim-hep/work/smoke-test/smoke-test_last.png` and check it:
  - a white background;
  - text in DejaVu Sans (or the experiment font);
  - a rendered formula;
  - a small histogram;
  - "safe areas: clear".
- If TeX is not available, the formula is skipped; say so.
- **Gate:** the frame shows all of the above. Compare it with the reference image
  `docs/install/smoke_reference.png` in the manim-hep repository.

## Phase 4: hand back

Report:
- what was installed and created (paths);
- the settings chosen;
- **what could not be done, and why**;
- the next step ("ask me for your first animation").

Commit only if the user said you may.

## Platform notes

- **Windows.**
  - Use MiKTeX or TeX Live. MiKTeX may prompt to install packages on first use: run
    `miktex packages install standalone preview babel-english` once.
  - The first text of every render takes a few seconds (font loading).
  - Run from a folder you can write to; paths with spaces are fine.
- **macOS.**
  - Run `brew install cairo pango pkg-config` if pip has to build pycairo or manimpango.
  - For LaTeX, BasicTeX plus
    `sudo tlmgr install standalone preview babel-english dvisvgm`, or the full MacTeX.
- **Linux.**
  - Run `sudo apt install libcairo2-dev libpango1.0-dev pkg-config texlive texlive-latex-extra dvisvgm`
    (Debian/Ubuntu).
- **lxplus.**
  - Keep the environment and renders off your AFS home (quota): use an EOS or work area.
  - Put TeX Live from CVMFS on PATH:
    `export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux:$PATH`.
  - Render with the default cairo renderer; there is no display.
- **Batch clusters.** As on lxplus: use the cairo renderer (never `--renderer=opengl`), a
  full TeX Live, and non-home storage for `media/` and `.manim-hep/`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `import manim` fails with a cairo or pango error | install the system libraries above, then reinstall `manim` |
| `MathTex` fails with `FileNotFoundError` | two renders at once: use `manim-hep render` (it serialises renders) |
| `MathTex` fails with "standalone.cls not found" | a full TeX Live, or the missing packages; see `doctor` |
| Text in the wrong font | call `use_theme()` at module level; never pass `font=` |
| A `ManimGL` / `manimlib` error | wrong package: `pip uninstall manimgl`, then `pip install "manim>=0.21,<0.22"` |
