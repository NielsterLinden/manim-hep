---
name: hep-storyline
description: Plan a HEP animation before any code is written. Interview the user briefly, write storylines/<slug>.md from the template (beats, on-screen whitelist, numbers with sources, final-frame checklist, chaining, allowed exceptions), present it as markdown or as a claude.ai artifact, and wait for approval. Use before building a clip unless manim-hep.toml sets storyline = "off", or whenever the user asks for a storyline, storyboard, brief or plan for an animation.
---

# Storylines: plan first, then build

A storyline is a short markdown file that the user approves before any render time is spent.
It is also the clip's record afterwards. Template: [template.md](template.md).

## 1. Interview (one or two rounds)

Ask at most six questions per round. Give your recommendation with every question
("I suggest X because Y; OK?"), and only ask about what the request leaves open.
Never guess a number.

1. **Point.** What should the audience understand after this clip? Keep it to one sentence
   and one idea. If it holds two ideas, propose two clips.
2. **Context.** The talk and its audience, what comes before and after, and whether the clip
   chains to a neighbouring one (entry and exit frames).
3. **Numbers.** Every value that will appear on screen: its value, unit and source (DOI,
   arXiv, PDG year, or a frozen data file). Schematic values must be declared schematic.
4. **Experiment and status.** Which theme? If an experiment label appears, which **explicit**
   status (see `hep-experiment-style`)? Never propose "Preliminary" or "Internal" yourself.
5. **Text.** The default is none beyond physics symbols, units and numbers. Record any
   caption the user asks for as an allowed exception.
6. **Length and pace.** 4–13 s per clip. Calm is 10–13 s, brisk is 6–9 s. A particle track
   takes about 2 s.

## 2. Write `<root>/storylines/<slug>.md`

- Use the slug of the clip in kebab-case (`drell-yan`, `zmumu-fill`).
- Fill every section of the template:
  - **Beats**: one row per beat, with its duration and an **on-screen whitelist** (every
    symbol and digit allowed in that beat).
  - **Numbers**: every value with its source.
  - **Final frame must show**: a checklist that verification ticks off.
  - **Chaining**: entry and exit frames.
  - **Allowed exceptions**: anything that bends a house rule, with who asked for it.
- Leave *Record* empty; the deliver step fills it in.
- Set `state: draft`.

## 3. Present it (the `storyline` setting)

- **`markdown`**: give the path and a five-line summary in chat, then ask for approval.
- **`artifact`**:
  - Only if a tool for publishing claude.ai artifacts is available in this session (for
    example an `Artifact` tool in your tool list). Otherwise fall back to `markdown` and say so.
  - Build one self-contained HTML page from the storyline: the title and point, the beats as
    a table, the numbers table with sources, and the final-frame checklist.
  - Publish it and give the link, and also give the markdown path.
  - After rendering, republish the same page with the keyframes: pass the PNGs from
    `storylines/<slug>/frames/` as supporting files and reference them by relative path, so
    the page becomes the visual record.
- **`off`**: no storyline. Still state your assumptions before building.

## 4. The approval gate

Do not write scene code, freeze numbers or render until the user approves this storyline.
Then set `state: approved`.

- If the user changes the story, edit the file and ask again.
- If they approve with changes, apply the changes first.

After delivery, the deliver step fills in *Record* and sets `state: built`.

## Good storylines

- **One idea per clip.** If two things move for different reasons, cut one.
- **Numbers own the frame at the end.** A value appears small next to what measured it, then
  grows to reading size as the plot recedes.
- **"The data never move."** Only the prediction and the ratio change.
- **Chains are designed.** When clips chain, the exit frame of clip N is the entry frame of
  clip N+1, and the storyline names what stays on screen.
