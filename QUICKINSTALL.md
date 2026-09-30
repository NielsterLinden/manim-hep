# Quick install

> **Work in progress:** manim-hep is not released yet; this works once v0.1.0 is out.

Open your coding agent (Claude Code, Codex, Cursor, ...) **in the repository where you
want to make animations**, and paste this sentence:

> Set up manim-hep in this repository: follow https://github.com/NielsterLinden/manim-hep/blob/main/docs/install/AGENT_INSTALL.md, and ask me the setup questions first.

The agent then:
1. asks a few setup questions;
2. installs `manim-hep` and runs `manim-hep doctor`;
3. runs `manim-hep init` to write the settings, the agent rules, a `.gitignore` block and
   the skills;
4. renders a smoke test and checks its last frame;
5. reports what it did, and anything it could not do.

It never overwrites your files and never pushes.

Rather do it yourself? Read [docs/install/HUMAN_GUIDE.md](docs/install/HUMAN_GUIDE.md).
