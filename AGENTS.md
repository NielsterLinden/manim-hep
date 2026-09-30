# Working on manim-hep (rules for coding agents)

This repository is manim-hep ("Agentic Manim for HEP"). It has three layers that ship
together:

| Layer | Where | What |
|---|---|---|
| Core package | `src/manim_hep/` | the thin, tested Python API and the `manim-hep` CLI |
| Agent layer | `plugin/` | 9 skills (`plugin/skills/hep-*`) and 4 Claude agents; the root `.claude-plugin/marketplace.json` lists it |
| Gallery | `gallery/` | self-contained examples on synthetic data, by topic |

The design is in `docs/superpowers/specs/2026-09-30-manim-hep-design.md`, and the
implementation plan in `docs/superpowers/plans/`.

## How to work

These four principles are adapted from Jiayuan Zhang's
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), which distils
[Andrej Karpathy's notes on coding with LLMs](https://x.com/karpathy/status/2015883857489522876).

1. **Think before coding.** State your assumptions. If a requirement, a physics claim or a
   number is unclear, ask; never guess.
2. **Simplicity first.** Write the smallest change that does the job. No new option, helper
   or abstraction that nothing needs yet.
3. **Surgical changes.** Touch only what the task needs. Don't reformat or refactor
   neighbouring code.
4. **Goal-driven execution.** Define the check that proves the change works (a test, a
   render you look at), run it, and report it.

## Library rules

- **Add-only public API.** An existing public signature or default never changes, because
  finished clips depend on it. New behaviour gets a new name. Breaking changes are only
  allowed in a new minor version (0.x → 0.y), with a `CHANGELOG.md` entry.
- **Promotion rule.** Code starts in a gallery example. It moves into `src/manim_hep/` only
  when a second example needs it, and it arrives with tests.
- **Ship API and skills together.** A public API change updates
  `plugin/skills/hep-scenes/api.md` and the docs in the same PR.
- **Versions match.** The plugin version (`plugin/.claude-plugin/plugin.json`) always equals
  `manim_hep.__version__`; a test checks it.
- **Tests are required for core changes.** Rendering tests are marked `@pytest.mark.render`.
- **`manim_hep.palette` never imports Manim**, and `manim_hep/__init__.py` stays lazy:
  Manim imports its plugins while it is being imported.
- **Manim Community Edition 0.21 only** (`manim>=0.21,<0.22`). Upgrading Manim is a
  deliberate step: re-run `tests/test_manim_behaviour.py` and review
  `plugin/skills/hep-scenes/traps.md`.

## Checks to run before you say "done"

```bash
python -m pytest -m "not render"          # fast: unit, CLI, plugin and gallery-contract tests
python -m pytest -m render                # renders (slow; needs LaTeX for some)
ruff check src tests gallery scripts && ruff format --check src tests gallery scripts
manim-hep lint gallery/
claude plugin validate --strict plugin/   # and: claude plugin validate --strict .
python scripts/hygiene.py
```

- Render one scene at a time, and look at the frames. On Windows, the first text of each
  render takes a few seconds (font loading).

## Publication safety (enforced in CI by `hygiene.yml`)

- **Data and results:** no unpublished or internal results. The gallery data is synthetic,
  or public with a DOI.
- **Private details:** no private paths (`/afs/`, `/eos/`, `/project/`, home folders), no
  cluster host names, no usernames or personal names other than the credited authors.
- **Logos:** no collaboration logos, logo-derived geometry or official figures.
- **Files:** no committed media (MP4, MOV, GIF) and no file over 1 MB. Previews come from
  CI.
- **Licences:** nothing copied from CC BY-SA, NC or proprietary sources. Everything here is
  MIT.
- **Git:** never push, tag, publish or create GitHub issues or repositories without the
  owner's explicit go-ahead.
