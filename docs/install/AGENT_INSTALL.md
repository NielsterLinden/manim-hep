# Installing manim-hep: procedure for coding agents

You are a coding agent setting up manim-hep in the user's current repository. Follow the
phases in order. Each phase ends in a **gate** with a known result; do not start the next
phase until the gate passes, or until the user decides how to proceed.

**Ground rules**
- Never overwrite or delete a user file.
- Never push.
- Do not start long installs (LaTeX, system libraries) unless the user tells you to: print
  the commands for them instead.

## Phase 0: ask first

Ask these in **one** message, each with the default in brackets, and wait for the answers.

1. Which experiment style? `generic`, `atlas`, `cms`, `cms-opendata` or `lhcb` [generic]
2. Which OS or cluster? Windows, macOS, Linux, lxplus, other cluster [detect it and say
   what you found]
3. conda or pip, and which environment to install into? [the active one]
4. Is a full LaTeX installed? (Without it, scenes cannot use `MathTex`.) [check with
   `latex --version`]
5. Where should scenes, storylines, data and clips live (`paths.root`)? [`.`, or for
   example `presentation`]
6. The agent settings, with defaults:
   - storyline: `off`, `markdown` or `artifact` [artifact];
   - verify: `none`, `render`, `frames` or `review` [frames];
   - branch: `current`, `feature` or `worktree` [feature];
   - commit: `never`, `ask` or `auto` [ask].
7. Files or folders I must not touch? [none]
8. May I commit the setup when it is done? [no]

**Gate:** you have an answer, or the default was accepted, for all eight.

## Phase 1: install and probe

```bash
pip install manim-hep            # or: pip install "manim-hep[mplhep]"  for experiment fonts
manim-hep doctor                 # add --no-tex if the user has no LaTeX
```

- Every `[FAIL]` line comes with a `fix:` line for this platform. Show the fixes to the
  user.
- Run a fix yourself only if it is quick and the user agrees.

**Gate:** `manim-hep doctor` prints `all good`, or the user has decided to continue
without the failing parts (usually LaTeX). Note which.

## Phase 2: scaffold

```bash
manim-hep init --root <paths.root> --agent <claude|codex|both|none> --experiment <preset>
```

- **`--agent`:** use `claude` in Claude Code, `codex` in Codex, `both` when the team
  uses both, and `none` otherwise.
- **Settings:** then edit the `[agent]` values in `manim-hep.toml` to the Phase 0 answers.
- **What `init` changes.** It writes these, or merges them without overwriting:
  - `manim-hep.toml`;
  - an `AGENTS.md` block with the rules;
  - a `.gitignore` block;
  - `<root>/scenes/smoke_test.py`, `<root>/storylines/`, `<root>/data/` and
    `<root>/clips/`;
  - for claude: the `@AGENTS.md` line in `CLAUDE.md`, and the plugin in
    `.claude/settings.json`;
  - for codex: the skills in `.agents/skills/`.
- **Conflicts.** If `init` exits with 1, it wrote `<file>.manim-hep.new` files for what it
  could not merge. Show each one next to the original and merge by hand with the user.
  Delete the `.new` file afterwards.

**Gate:**
1. `init` exits 0, and there are no `.manim-hep.new` files left.
2. A search for unfilled placeholders in the files you changed finds nothing. Search for
   text in angle brackets in capitals, such as `<ROOT>`, and for `{root}` or `{experiment}`.

## Phase 3: smoke test

```bash
manim-hep render <root>/scenes/smoke_test.py SmokeTest
```

Open the last frame it prints (`.manim-hep/work/smoke-test/smoke-test_last.png`) and look
at it. Compare it with the reference:
https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/smoke_reference.png

It must show:
- a white background;
- the line "manim-hep smoke test" in a clean sans-serif font (DejaVu Sans, or the
  experiment font);
- a typeset formula "Δp_T / p_T = 1%" (without LaTeX: a note that the formula was
  skipped);
- a small step histogram with tick labels.

The command must also print `safe areas: clear`.

**Gate:** all of the above hold. Report which frame you inspected. If TeX is missing, say
that the formula check was skipped.

## Phase 4: hand back

Report to the user:
- **Done:** what you installed, the files `init` created or updated, and the settings
  chosen.
- **Could not do:** anything that failed or was skipped, with the reason and the fix
  command.
- **Next:** "Ask me for your first animation, for example: *make a clip of the Drell–Yan
  Feynman diagram for my talk*." For Claude Code, mention that collaborators are offered
  the manim-hep plugin when they trust the folder.

If the user allowed it in Phase 0, commit the setup: `manim-hep.toml`, `AGENTS.md`,
`CLAUDE.md`, `.gitignore`, `.claude/settings.json`, `.agents/skills/` and `<root>/`. Rendered
media and `.manim-hep/` are ignored. Never push.
