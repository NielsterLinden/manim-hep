---
slug: template-fit
state: built
experiment: generic
label_status: none
---
# Template fit

**Point (one sentence):** Fitting a signal strength means scaling the signal template until
the prediction matches the data best, which is the minimum of −2ΔlnL, and the 1σ interval
is where the curve rises by one.
**Context:** A methods talk, after the selection and before the result; the data are shown
first and never move.

## Beats
| # | What happens | On screen (allowed symbols and numbers) | Seconds |
|---|---|---|---|
| 1 | Axes, background-only stack and data appear | m [GeV], Events / 2 GeV, tick labels | 1.4 |
| 2 | Key, μ readout and the likelihood panel appear, with the point at μ = 0 | n, μ s, b, μ = 0.00, μ, −2ΔlnL, 1, 4, 9 | 1.0 |
| 3 | μ sweeps from 0 to 2: the signal layer grows and −2ΔlnL is traced | μ readout | 5.0 |
| 4 | μ settles at the best fit; the point slides back along the curve | μ readout | 1.8 |
| 5 | The 1σ interval and the result | μ̂ = 1.02 +0.34 −0.33 | 1.0 |

## Numbers
| Quantity | Value | Unit | Source (DOI, arXiv, or frozen data file) | Schematic? |
|---|---|---|---|---|
| Background template | exponential, slope 40 GeV, 1500 events in 100–160 GeV | events | chosen | yes |
| Signal template | Gaussian, 125 GeV, σ = 3 GeV, 55 events at μ = 1 | events | chosen | yes |
| Data | one Poisson draw of b + s (μ_true = 1), 1510 events | events | seeded synthetic data (seed 20260940) | yes |
| μ̂ and 1σ interval | 1.02, +0.34, −0.33 | none | computed (Poisson likelihood) | yes |

## Final frame must show
- [x] Data, background and signal at μ̂, with the key and μ = 1.02
- [x] The full −2ΔlnL curve with the point at its minimum and the 1σ interval where it
  crosses 1
- [x] μ̂ with its asymmetric uncertainties
- [x] Nothing above the title band (y > 2.7)

## Chaining
Entry frame: empty · Exit frame: the fitted stack and the likelihood curve with the result

## Allowed exceptions
None.

## Record (filled after rendering)
Clip: TemplateFit (10.3 s, 480p15 draft) · Frames inspected: 1.2, 2, 3, 5.5 and 8.5 s and the
last frame · Keyframes: gallery previews come from CI
