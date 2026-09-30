---
slug: detector-signatures
state: built
experiment: generic
label_status: none
---
# Detector signatures

**Point (one sentence):** Each kind of particle leaves its own recognisable pattern in
the layers of a detector.
**Context:** Introductory part of a talk. The first clip builds the detector. The
second, chained to it, shows the five signatures. Later clips could zoom into one of them.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Layers appear inside out (clip `DetectorBuild`) | detector only | 4.5 |
| 2 | An electron track curls to the ECAL; a shower appears | e⁻ | 2.0 |
| 3 | A muon crosses everything; three station hits | μ⁺ | 2.2 |
| 4 | A photon: no track, an ECAL shower | γ | 1.6 |
| 5 | A jet: a cone of tracks, ECAL and HCAL deposits | jet | 2.0 |
| 6 | A neutrino leaves unseen (dashed arrow) | ν | 2.0 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Field for the curvatures | 3.8 | T | typical large solenoid | yes |
| Lepton pT | 3 | GeV | chosen so the bending is visible | yes |
| Jet track pT | 1.5–5 | GeV | seeded random | yes |

## Final frame must show
- [x] The complete detector, below the title band
- [x] Five signatures, each in its own colour, with its symbol outside the detector
- [x] e⁻ bending anticlockwise and μ⁺ clockwise (B out of the screen)
- [x] Muon hits in all three stations; the neutrino arrow leaving the detector

## Chaining
Entry frame: empty (clip 1); the complete detector (clip 2) · Exit frame: the complete
detector (clip 1); detector plus five signatures (clip 2)

## Allowed exceptions
The word "jet" is shown as the name of a physics object.

## Record (filled after rendering)
Clips: DetectorBuild (4.6 s), DetectorSignatures (9.9 s) · Frames inspected: first,
1.0 s, 2.5 s and last of DetectorBuild; first, 1.0 s, 3.0 s, 6.5 s and last of
DetectorSignatures · Seam DetectorBuild → DetectorSignatures: OK (mean 0.84 at 480p,
0 blobs) · Keyframes: gallery previews come from CI
