---
name: hep-physics
description: Check the physics fidelity of HEP animations. Covers Feynman-diagram conventions, detector signatures and track curvature, notation and units, statistics definitions, and the rule that every on-screen number has a source, graded BLOCK, MAJOR or MINOR. Use when designing or reviewing any clip with physics content, before delivering it, or when the user asks whether an animation is physically correct.
---

# Physics fidelity

An audience of physicists notices a wrong arrow or a curvature with the wrong sign
immediately. Check these before a clip ships.

## Feynman diagrams

- **Time and arrows.**
  - State the time direction (left to right is the default); reading order follows it.
  - Fermion arrows follow fermion flow, so an incoming antiparticle's arrow points *out of*
    the diagram. An antiquark entering from the left therefore has an arrow pointing left
    (manim-hep: an edge from the vertex to the external point, or `antifermion`).
- **Line styles.**
  - Photons are wavy; W and Z are wavy with a label; gluons are curly; the Higgs and other
    scalars are dashed. Keep one style per particle type across a talk.
- **Conservation.**
  - Every vertex conserves electric charge, lepton and baryon number, and colour.
  - It also has a physical coupling: no ggZ vertex, and no neutral-current flavour change
    at tree level.
- **Labels.**
  - Use proper particle symbols in MathTex: q, \bar{q}, \ell^\pm, \nu_\ell, \gamma^*/Z, W^\pm,
    H, g, t, b, \tau.
  - Put the charge on the label when it matters, and label bound states between their
    quark lines.
- **Readability.**
  - Keep spectator lines straight, and never cross lines that do not have to cross.
  - Crossings read as a different topology.

## Detector signatures

| Object | Tracker | ECAL | HCAL | Muon system |
|---|---|---|---|---|
| electron | curved track | shower (stops) | — | — |
| photon | none (dashed guide at most) | shower (stops) | — | — |
| muon | curved track | minimal | minimal | hits, leaves the detector |
| charged hadron | curved track | small deposit | shower (stops) | — |
| neutral hadron | none | small | shower | — |
| jet | several tracks, a cone | deposits | deposits | — |
| τ_h | 1 or 3 collimated tracks (+ π⁰ → γγ in the ECAL) | yes | yes | — |
| neutrino | nothing: inferred from missing transverse momentum | — | — | — |

- **Curvature.**
  - Direction: F = q v × B. With B out of the screen, a positive charge bends *clockwise*.
  - Radius: R[m] = pT[GeV] / (0.3 |q| B[T]). A 1 GeV track in 3.8 T has R ≈ 0.88 m; a
    50 GeV track looks straight.
  - Two tracks of the same pT and opposite charge bend with equal radius, in opposite
    directions.
- **Where tracks stop.**
  - Tracks stop where the particle stops: electrons at the ECAL, hadrons in the HCAL.
  - Muons leave the detector; draw them to the outermost layer.
  - Draw the part outside the tracker dashed or lighter if it is not measured.

## Notation and units

- **Units** are upright and variables italic: `m_{\ell\ell}\,[\mathrm{GeV}]`, `p_\mathrm{T}`,
  `\sqrt{s} = 13.6\,\mathrm{TeV}`, `\mathcal{L}\,dt = 140\,\mathrm{fb}^{-1}`. Write GeV and
  TeV, never Gev.
- **Uncertainties.**
  - Give significant figures consistent with the uncertainty: `125.2 \pm 0.1`, not
    `125.2137 \pm 0.1`.
  - Write asymmetric errors as `^{+0.3}_{-0.2}`, and keep one result format for the whole
    talk.
- **Kinematic variables.**
  - η is pseudorapidity, and φ the azimuth.
  - Label the transverse plane (x–y) and the beam axis (z) the same way throughout.

## Numbers

- **Every on-screen number has a source.**
  - Measured or analysis values come from a frozen JSON file with provenance
    (`load_frozen(..., expect=...)` asserts them).
  - Literature values carry a citation: PDG with its year, a DOI or an arXiv number.
- **No number may be read off schematic geometry.**
  - Schematic plots carry no digits, or the storyline declares them schematic.
- **If a number does not match its source, stop and report.** Never adjust it quietly.

## Statistics

- **Significance.** Z = S/√B only when S ≪ B. Otherwise use the Asimov form
  Z = √(2((s+b) ln(1+s/b) − s)).
- **Likelihoods.** −2ΔlnL = 1 gives the 1σ interval for one parameter, and 3.84 the 95 %
  CL interval.
- **Tests.** A p-value is not the probability that a hypothesis is true. Say which test
  statistic you use and whether the result is expected or observed.
- **Distributions.** Histograms show counts per bin, with Poisson errors √N for data unless
  stated. Normalised shapes must say so on the axis title.

## Review checklist and grades

| Grade | Meaning | Examples |
|---|---|---|
| **BLOCK** | Wrong physics or a false number: do not ship | wrong curvature sign; an arrow against the fermion flow; a vertex violating charge; an on-screen number that differs from its source; a result with a label status the user did not choose |
| **MAJOR** | Misleading, or inconsistent with the rest of the talk | a neutrino with a track; a muon stopping in the calorimeter; a schematic plot with digits; mixed units; crossings that suggest another topology |
| **MINOR** | Polish | label spacing; a missing charge sign that the context makes clear; too many significant figures |

Report findings as `GRADE | clip / frame or line | what | why | suggested fix`, most severe
first. Critics report; they never edit.
