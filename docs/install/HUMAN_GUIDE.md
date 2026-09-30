# Installing manim-hep yourself

The same steps the agent procedure follows, for people.

## 1. Python and Manim

Use Python 3.11 or newer, ideally in its own environment:

```bash
conda create -n manim python=3.12 -y && conda activate manim     # or a venv
pip install manim-hep            # add [mplhep] for the exact ATLAS/CMS/LHCb fonts
```

This installs [Manim Community Edition](https://www.manim.community) 0.21 as well. If
`pip` has to build `pycairo` or `manimpango`, install the system libraries first:
- **macOS:** `brew install cairo pango pkg-config`
- **Debian/Ubuntu:** `sudo apt install libcairo2-dev libpango1.0-dev pkg-config`

## 2. LaTeX (for formulas)

`MathTex` needs a full LaTeX with `standalone`, `preview` and `dvisvgm`:

| Platform | Install |
|---|---|
| Windows | [MiKTeX](https://miktex.org/download) (or TeX Live), then `miktex packages install standalone preview babel-english` |
| macOS | `brew install --cask basictex`, then `sudo tlmgr install standalone preview babel-english dvisvgm` (or MacTeX) |
| Linux | `sudo apt install texlive texlive-latex-extra dvisvgm` |
| lxplus | `export PATH=/cvmfs/sft.cern.ch/lcg/external/texlive/latest/bin/x86_64-linux:$PATH` |

Without LaTeX everything else still works; just avoid `MathTex` in your scenes.

## 3. Check

```bash
manim-hep doctor
```

Fix every `[FAIL]` line; each one prints the command for your platform.

## 4. Set up your repository

```bash
cd my-talk
manim-hep init --root presentation --experiment cms --agent claude   # or codex, both, none
```

This creates or merges:
- **`manim-hep.toml`**, the settings. It is explained in
  [docs/concepts/settings.md](../concepts/settings.md).
- **`AGENTS.md`**, the rules for coding agents, inside a marked block. Your own text stays.
- **`.gitignore`**: rendered media and the `.manim-hep/` working folder stay out of git.
- **`presentation/scenes/smoke_test.py`**, plus empty `storylines/`, `data/` and `clips/`.
- **With `--agent claude`:** `CLAUDE.md` imports `AGENTS.md`, and `.claude/settings.json`
  offers the manim-hep plugin to everyone who trusts the folder.
- **With `--agent codex`:** the skills, in `.agents/skills/`.

Running it again changes nothing. If it cannot merge a file safely, it writes
`<file>.manim-hep.new` for you to merge by hand.

## 5. Smoke test

```bash
manim-hep render presentation/scenes/smoke_test.py SmokeTest
```

Open the last frame it prints and compare it with
[smoke_reference.png](smoke_reference.png). You should see a white background, text, a
formula and a histogram, and the output line `safe areas: clear`.

## 6. Make something

- **Start from an example.** Copy one from the [gallery](../../gallery/), or start from
  `gallery/_template/`.
- **Render it.** Run `manim-hep render <file> <Scene>` while you work, and look at the
  frames it writes.
- **Deliver it.** `manim-hep render <file> <Scene> --final` writes
  `clips/<name>_vK.mp4` and `_vK_final.png`, ready for your slides. Set the clip to start
  automatically, and turn off "rewind after playing", so it rests on its last frame.
- **Check it.** Run `manim-hep lint` before you share a scene.
