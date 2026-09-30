# Agentic Manim for HEP

!!! warning "Work in progress"
    manim-hep is not released yet. Expect changes until v0.1.0.

**manim-hep** helps high-energy physicists make animations for their talks with
[Manim Community Edition](https://www.manim.community). There are three ways in:

- **Ask an agent.** Paste one sentence into Claude Code, Codex or another coding agent (see
  [Quick install](install/AGENT_INSTALL.md)). Its skills then plan the clip with you,
  build it, render it, look at the frames and deliver an MP4 for your slides.
- **Import it.** `pip install manim-hep` gives you building blocks: experiment themes and
  status-checked labels, Feynman diagrams, HEP-style plots, a detector slice with tracks
  and signatures, and helpers for chained clips and frozen numbers.
- **Work by hand.** Copy an example from the [gallery](gallery/index.md) and adapt it.

## What a clip looks like

A clip is 4–13 seconds long and says one thing. It ends on a complete last frame, and it
drops into PowerPoint, Keynote, Google Slides or Beamer next to the slide title. For the
reasoning behind this, see the [workflow](concepts/workflow.md).

## Credits

manim-hep is a small layer on top of Manim. All the credit for the animation engine goes
to Grant Sanderson (3Blue1Brown) and the Manim Community developers; see
[Credits](credits.md).

Not affiliated with or endorsed by ATLAS, CMS, LHCb, KM3NeT or CERN. Experiment presets
follow public conventions. Your collaboration's approval rules still apply to anything you
show.
