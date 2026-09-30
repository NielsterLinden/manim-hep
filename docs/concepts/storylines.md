# Storylines

A storyline is a short markdown file, `storylines/<slug>.md`. You approve it before any
render time is spent, and afterwards it becomes the record of the clip. Agents write it
with the `hep-storyline` skill, after a short interview.

```markdown
---
slug: zmumu-fill
state: draft            # draft → approved → built
experiment: cms-opendata
label_status: none      # explicit status, or "none" if no experiment label
---
# Filling the Z peak

**Point (one sentence):** Every event adds one entry; the peak emerges.
**Context:** after the detector clip, before the fit clip.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | One event flies in, its mass lands in a bin | m_μμ, 91.2 GeV | 3 |
| 2 | Events rain in faster; the peak grows | axis ticks | 5 |

## Numbers
| Quantity | Value | Unit | Source | Schematic? |
|---|---|---|---|---|
| m_Z | 91.1876 | GeV | PDG 2024 | no |
| counts | — | — | data/zmumu.json | no |

## Final frame must show
- [ ] the full histogram, with no half-faded entries
- [ ] the axis titles and ticks, nothing above the title band

## Chaining
Entry frame: detector clip's last frame · Exit frame: the filled histogram

## Allowed exceptions
None.

## Record (filled after rendering)
Clip: clips/zmumu-fill_v1.mp4 · Duration: 8.1 s · Frames inspected: first, t3, last ·
Keyframes: storylines/zmumu-fill/frames/
```

**Why it works.**
- **On-screen whitelist.** The whitelist column keeps narrative text out of clips.
- **Traceable numbers.** The numbers table makes every digit traceable.
- **A checkable goal.** The final-frame checklist gives verification something concrete to
  check against.

## Presenting a storyline

- **`markdown`:** the agent gives you the path and a short summary.
- **`artifact`:** in Claude with artifacts available, the agent also publishes a page with
  the tables. After rendering, it republishes that page with the keyframes, so you have a
  visual record to share.
