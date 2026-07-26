# Nanodiamond target dossier for Tamesis M_c v1

## Why this target matters

The 2026 nanodiamond/current-chip proposal is the first source found in this
search whose planned mass range directly crosses the Tamesis threshold:

```text
proposal range: 1e-19 kg < m < 1e-15 kg
Tamesis M_c:    5.292674126388712e-16 kg
```

That makes it more relevant than current observed matter-wave records, which
remain far below M_c.

## Tamesis predictions for target masses

Using `mc_model.py` with no environmental nuisance rate:

| M/M_c | mass kg | rate s^-1 | tau s | V(0.1 s) | V(1 s) |
|---:|---:|---:|---:|---:|---:|
| 0.3 | 1.5878e-16 | 0 | inf | 1.0000 | 1.0000 |
| 0.5 | 2.6463e-16 | 0 | inf | 1.0000 | 1.0000 |
| 0.9 | 4.7634e-16 | 0 | inf | 1.0000 | 1.0000 |
| 1.0 | 5.2927e-16 | 0 | inf | 1.0000 | 1.0000 |
| 1.01 | 5.3456e-16 | 4.6874e-1 | 2.1334 | 0.9542 | 0.6258 |
| 2.0 | 1.0585e-15 | 1.8380 | 0.5441 | 0.8321 | 0.1591 |
| 10.0 | 5.2927e-15 | 45.9507 | 0.0218 | 0.0101 | ~0 |

## Practical implication

A `0.1 s` experiment near `1.01 M_c` is not decisive by itself because Tamesis
still predicts high visibility. The decisive region is either:

- longer observation time near `1.01 M_c`, or
- mass above `2 M_c`, and ideally toward `10 M_c`.

The proposal's stated upper mass of `1e-15 kg` is about:

```text
1e-15 kg / M_c = 1.89 M_c
```

At that point Tamesis predicts visible but substantial intrinsic loss over
`0.1 s`, and strong loss over `1 s`.

## Current target ranking

After adding planned targets to `literature_points.csv`, the highest
decisiveness targets are:

1. `Nanodiamond chip upper target`: `1e-15 kg`, about `1.89 M_c`.
2. `Spin-IHP 1e-15 kg 50um target`: `1e-15 kg`, about `1.89 M_c`.
3. `Nanodiamond chip 1.01Mc target`: useful for locating the edge, but weaker
   at `0.1 s`.

The conclusion is slightly counterintuitive but important: the first Bohr-level
attempt should not merely touch `M_c`. It should include a mass around
`1e-15 kg` and, if possible, a longer hold/readout window.

## Required data for a real test

To turn this into a discriminating Tamesis test, the experiment must report:

- center-of-mass mass distribution, not only nominal mass;
- spatial separation distribution;
- observation time and recombination time;
- fringe visibility with uncertainty;
- pressure, temperature and blackbody environment;
- magnetic/current-noise budget;
- independent environmental decoherence model;
- pre-registered inclusion/exclusion criteria.

## Decision rule

This target becomes Bohr-level only if measured center-of-mass visibility shows
a threshold-like change around M_c that beats CSL, GRW, Diosi-Penrose and
environmental nuisance models under the pre-registered likelihood comparison.
