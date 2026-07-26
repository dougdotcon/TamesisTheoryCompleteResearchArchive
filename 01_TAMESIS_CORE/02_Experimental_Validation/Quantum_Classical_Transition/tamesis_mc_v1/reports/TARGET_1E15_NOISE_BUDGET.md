# Target 1e-15 kg: normalized noise budget

This file translates the extracted experimental tolerances into first-pass
nuisance rates.

## Anchors

From the source papers, the 99% contrast tolerances used here are:

- magnetic gradient fluctuation: `1e-7`
- initial position error with IHP: `1e-9 m`

The reference visibility used for normalization is `0.99` over `0.1 s`.

That gives a normalized rate scale:

```text
Gamma_ref = -ln(0.99) / 0.1 ≈ 0.1005 s^-1
```

## Scenario scan

The first-pass combined nuisance budget uses quadratic scaling in the fraction
of tolerance.

### best_case

- magnetic fraction: `0.1`
- position fraction: `0.1`
- combined nuisance rate: `~0.00201 s^-1`
- combined visibility at 0.1 s: `~0.9998`

### at_tolerance

- magnetic fraction: `1.0`
- position fraction: `1.0`
- combined nuisance rate: `~0.2010 s^-1`
- combined visibility at 0.1 s: `~0.9801`

### ten_x_worse

- magnetic fraction: `10.0`
- position fraction: `10.0`
- combined nuisance rate: `~20.10 s^-1`
- combined visibility at 0.1 s: `~0.133`

## Interpretation

The Tamesis intrinsic visibility at the target is `0.8487`.
So:

- the best-case nuisance budget is safely below the Tamesis signal;
- operation right at tolerance starts to compete but still leaves room;
- 10x worse noise buries the effect.

This is the exact reason the target is interesting: it sits in a regime where
instrument quality decides whether the theory is testable.
