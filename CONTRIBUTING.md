# Contributing to manim-hep

Thank you for helping. manim-hep grows through examples that people found useful in their
own talks. Everything is MIT-licensed, and so is your contribution.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md). If you are unsure whether something
fits, open an issue first: "Animation request", "Port this" or "Bug".

## Ways to contribute

### 1. A gallery example (the most common)

Each example is a folder, `gallery/<category>/[<experiment>/]<slug>/`:

| File | Contents |
|---|---|
| `scene.py` | self-contained; imports only `manim`, `manim_hep`, NumPy and the standard library; seeded synthetic data |
| `README.md` | a YAML header (`title`, `category`, `tags`, `authors`, `data`, `label_status`, `manim_hep`, `scenes`, `references`), then what it shows, physics notes with sources, and how to adapt it |
| `storyline.md` | optional: the storyline it was built from |

- **Categories:** `theory`, `methods`, `experiments/<generic|atlas|cms|lhcb|km3net>`,
  `plots/<general|atlas|cms|lhcb>` and `ml`.
- **Start point:** copy `gallery/_template/`.
- **With an agent:** use the `hep-contribute` skill. It walks through the privacy scrub, the
  folder contract and the pull request.

### 2. A core addition (`src/manim_hep/`)

- **Promotion rule.** Code starts in a gallery example. It moves into the core when a
  second example needs it.
- **Add-only API.** Never change an existing public signature or default: finished clips
  depend on them. Add a new name instead.
- **Tests are required**, and the same PR updates `plugin/skills/hep-scenes/api.md` and the
  docs.

### 3. An experiment preset or label change

- **Code owners.** Changes to `src/manim_hep/_presets.py`, `src/manim_hep/experiments.py`,
  `gallery/experiments/<exp>/` or `gallery/plots/<exp>/` need a review from that
  experiment's code owner (`.github/CODEOWNERS`).
- **Status lists** follow the collaboration's public figure conventions. Link your source.
- **We are looking for one code owner per experiment**, including KM3NeT. Open an issue if
  you would like to help.

### 4. Skills and agents (`plugin/`)

- **Portability.** Skills use the Agent Skills format (`SKILL.md` with `name` and
  `description`) and must work on their own, because not every tool has subagents.
- **Validation.** Run `claude plugin validate --strict plugin/` and the plugin tests.

## Development setup

```bash
conda create -n manim-hep-dev python=3.12 -y && conda activate manim-hep-dev
pip install -e ".[dev]"
manim-hep doctor
```

## Checks (CI runs the same)

```bash
python -m pytest -m "not render"                       # fast tests
python -m pytest -m render                             # renders; some need LaTeX
ruff check src tests gallery scripts && ruff format --check src tests gallery scripts
manim-hep lint gallery/
python scripts/hygiene.py                              # publication safety
claude plugin validate --strict plugin/                # when you change plugin/
```

## Pull request checklist

- [ ] It renders in CI
- [ ] `manim-hep lint` is clean
- [ ] Synthetic data, or public data with a DOI
- [ ] Physics sources are cited
- [ ] No logos, internal results, private paths, host names or personal names
- [ ] Licence-compatible (MIT; nothing copied from share-alike, non-commercial or
      proprietary sources)

## Publication safety

The gallery is public and so are the renders CI makes from it.
- **Unpublished results and private details.** Never commit unpublished results, internal
  plots, private paths, cluster host names or other people's names.
- **Media and logos.** Never commit collaboration logos or rendered media (MP4, GIF).
- **Enforcement.** `scripts/hygiene.py` and a secret scan run on every pull request.
