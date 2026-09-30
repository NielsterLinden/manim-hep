# Workflow

manim-hep encodes a way of working that held up in three real talks: an ATLAS thesis, an
LHCb project and a CMS Open Data school. Agents follow it through the `hep-animate`
skill; people can follow it by hand.

## Clips for a slide deck

You build the deck in your usual tool (PowerPoint, Keynote, Google Slides, Beamer).
manim-hep delivers **MP4 clips** that you drop onto slides:
- **One idea per clip, 4–13 s.** If two things move for different reasons, make two clips.
- **The slide carries the words.** Clips show animation, physics symbols, units and
  numbers; titles and captions stay on the slide.
- **Clips end on their last change** (`self.wait(0.1)`). Set the clip to start
  automatically and not to rewind. It then rests on its last frame while you talk.
- **The title band stays empty.** Nothing is drawn above y = 2.7, the top 16 % of the
  frame, where the slide title goes.
- **Every delivery is versioned.** `clips/<slug>_vK.mp4` and `_vK_final.png`; nothing is
  ever overwritten, so a deck that links `_v2` never breaks.

## The steps

1. **Setup check.** Run `manim-hep doctor`; `manim-hep init` if the project is new.
2. **Storyline** (unless `storyline = "off"`). A short interview, then
   `storylines/<slug>.md`. The user approves it before anything is built.
   See [Storylines](storylines.md).
3. **Branch.** Per the `branch` setting (`current`, `feature` or `worktree`).
4. **Build.** A state-first scene on the manim-hep building blocks.
5. **Verify.** To the `verify` level (`none`, `render`, `frames` or `review`). See
   [Verification](verification.md).
6. **Deliver.** `manim-hep render ... --final`, and the storyline's *Record* is filled in.
7. **Commit.** Per the `commit` setting. **Nobody ever pushes automatically.**

## The four principles

The agents' coding rules adapt four principles from Jiayuan Zhang's
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills), which
distils Andrej Karpathy's notes on coding with LLMs:

1. **Think before coding.** Agree the storyline, state assumptions, and ask instead of
   guessing.
2. **Simplicity first.** Write the smallest scene that tells the story.
3. **Surgical changes.** Touch only the scene you were asked about; shared helpers are
   add-only.
4. **Goal-driven execution.** Render, look at the frames, and compare them with what the
   storyline promised.

## State-first scenes

A scene first builds its final frame as a dict of objects: a **builder**, with no
animation. It then animates those same objects into place, and ends with `check_order`,
which proves nothing stray is left and the drawing order is right.

The next clip opens with `add_state(self, previous_builder)`, so it starts on exactly the
frame the previous one ended on. `manim-hep seam` verifies the joint.

```python
def state_final() -> dict:
    axes = DataAxes((60, 120), (0, 900)).move_frame_to((0, -0.4))
    return {"axes": axes, "hist": step_hist(axes, EDGES, COUNTS, color=C.theory)}

class Fill(Scene):
    def construct(self):
        s = state_final()
        self.play(FadeIn(s["axes"]))
        self.play(Create(s["hist"]), run_time=2)
        check_order(self, s)
        self.wait(0.1)
```
