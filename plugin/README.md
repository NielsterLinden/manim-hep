# manim-hep: Claude Code plugin

> **Work in progress:** not yet released.

This is the agent layer of [manim-hep](https://github.com/NielsterLinden/manim-hep)
("Agentic Manim for HEP"). It contains nine skills and four agents for planning, building,
rendering and checking high-energy-physics animations with
[Manim Community Edition](https://www.manim.community).

## Install

In Claude Code:

```
/plugin marketplace add NielsterLinden/manim-hep
/plugin install manim-hep@manim-hep
```

Or in a shell: `claude plugin marketplace add NielsterLinden/manim-hep`, then
`claude plugin install manim-hep@manim-hep`.

The Python package does the rendering: `pip install manim-hep`. After that,
`manim-hep init --agent claude` sets up a project, including this plugin for everyone who
trusts the folder.

## Skills

| Skill | Use it for |
|---|---|
| `hep-animate` | The entry point: settings, house rules, the workflow |
| `hep-storyline` | Planning a clip and getting it approved |
| `hep-scenes` | Writing scenes on the manim-hep API, and the Manim trap list |
| `hep-render-verify` | Rendering, inspecting frames, lint, seams, the report |
| `hep-physics` | Physics conventions and the BLOCK/MAJOR/MINOR checklist |
| `hep-experiment-style` | ATLAS / CMS / LHCb presets, status labels, Open Data, logos |
| `hep-plots-data` | Frozen data with provenance and result plots |
| `hep-setup` | Installation and troubleshooting |
| `hep-contribute` | Sharing a scene back to the gallery |

The skills use the open Agent Skills format. Codex and other agents get the same files
through `manim-hep init --agent codex`, which copies them to `.agents/skills/`.

## Agents

`scene-builder`, `plot-recreator`, `render-verifier` (read-only) and `physics-checker`
(read-only). They inherit your session's model. Coordination stays in the main session.

## Credits

Built on Manim Community Edition (MIT; © 2018 3Blue1Brown LLC, © 2024 the Manim Community
Developers), originally created by Grant Sanderson (3Blue1Brown). See
[CREDITS.md](https://github.com/NielsterLinden/manim-hep/blob/main/CREDITS.md). MIT licence.
