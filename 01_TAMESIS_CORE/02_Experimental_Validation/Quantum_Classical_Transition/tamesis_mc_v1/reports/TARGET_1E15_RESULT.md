# Target 1e-15 kg: first hard Tamesis triage

## Source basis

The target comes from arXiv:2408.11909, whose abstract states that a spatial
superposition with:

```text
mass = 1e-15 kg
separation = 50 micrometers
time = 0.1 seconds
```

is realized in their proposed spin-dependent force plus inverted harmonic
potential scheme.

Source: https://arxiv.org/abs/2408.11909

## Tamesis prediction

Using `mc_model.py`:

```text
M_c = 5.292674126388712e-16 kg
M/M_c = 1.8894040632770233
Gamma_T = 1.6403692061364539 s^-1
tau = 0.6096188566934212 s
V(0.1 s) = 0.8487106863823988
V(1.0 s) = 0.19390843688831894
```

This is the first target where the Tamesis effect is large enough to be
measurable but not so large that the signal is simply gone.

## Comparison models at 0.1 s

First-pass values from `target_1e15_analysis.json`:

| model | predicted visibility at 0.1 s | effective rate s^-1 |
|---|---:|---:|
| Tamesis | 0.8487 | 1.6404 |
| GRW | 0.999994 | 5.98e-5 |
| Diosi-Penrose | 0.998735 | 0.01266 |
| CSL naive point-mass | ~0 | 276.31 |

The CSL row is intentionally marked naive. A publishable comparison must use an
extended-body CSL model and current experimental bounds.

## Environmental condition

Using the first-pass gas-collision model in `environment_model.py`, for a
diamond-like particle at 20 K:

```text
pressure for gas rate = Tamesis rate:       7.02e-12 Pa
pressure for gas rate = 10% Tamesis rate:   7.02e-13 Pa
```

At `1e-15 Pa`, gas collisions are negligible. At `1e-12 Pa`, they are already a
small but relevant nuisance. At `1e-10 Pa`, environmental decoherence dominates.

## Thermal gate

Blackbody radiation becomes a considerable decoherence channel above about
`4 K` for micrometer-size superpositions in diamond. Since the target is around
`50 μm`, treat `4 K` as a conservative upper limit and `1 K` as the practical
goal.

## Current verdict

This is a real Bohr-level candidate target, but not yet a discovery route by
itself.

It becomes serious if the experiment can report center-of-mass visibility near
`1e-15 kg` with:

- pressure below about `7e-13 Pa`, or a measured gas-collision nuisance model;
- blackbody decoherence budget;
- magnetic/current noise budget;
- visibility uncertainty small enough to distinguish `V ~ 0.85` from `V ~ 1`;
- a mass ladder below and above `M_c`.

## Next technical gap

The next model gap is not gas. It is chip-specific current/magnetic noise and
blackbody decoherence. Those must be extracted from the detailed paper geometry
or requested from the authors before a strong Tamesis-vs-environment claim.
