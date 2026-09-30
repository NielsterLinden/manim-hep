---
slug: template-ring
state: built
experiment: generic
label_status: none
---
# Template example

**Point (one sentence):** A ring appears, then one point on it lights up.
**Context:** Shows the file layout of a gallery example; not for a talk.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | The ring is drawn | nothing but the ring | 1.5 |
| 2 | A point on the ring appears (second clip) | the point | 0.6 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Point angle | random | rad | seeded synthetic data | yes |

## Final frame must show
- [x] The ring, centred below the title band
- [x] The point on the ring, in the highlight colour

## Chaining
Entry frame: empty · Exit frame: ring (clip 1), ring and point (clip 2)

## Allowed exceptions
None.

## Record (filled after rendering)
Clips: TemplateRing (1.6 s), TemplateDot (0.7 s) · Frames inspected: first and last of each ·
Keyframes: gallery previews come from CI
