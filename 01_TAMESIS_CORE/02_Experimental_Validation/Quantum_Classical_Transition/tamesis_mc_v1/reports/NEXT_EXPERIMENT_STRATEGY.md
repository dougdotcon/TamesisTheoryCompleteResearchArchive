# Next experiment strategy for a Bohr-level Tamesis test

## Current best target

The current best experimental class is not the observed 2026 sodium nanoparticle
record. That record is important, but it remains far below `M_c`.

The best target class is planned nanodiamond/macroscopic spatial superposition,
especially proposals that reach:

```text
mass: 1e-15 kg
M/M_c: 1.8894
observation time: 0.1 s to 1 s
spatial separation: nanometer to tens of micrometers
```

## Why 1e-15 kg matters

At `1e-15 kg`, Tamesis v1 predicts:

```text
Gamma_T = 1.64 s^-1
V(0.1 s) = 0.8487
V(1.0 s) = 0.1945
```

This is large enough to be measurable, but not so large that every run is simply
dark. That makes it a practical discrimination zone.

## Minimal mass ladder

The useful ladder is:

```text
0.3 M_c  = 1.59e-16 kg
0.5 M_c  = 2.65e-16 kg
0.9 M_c  = 4.76e-16 kg
1.01 M_c = 5.35e-16 kg
1.89 M_c = 1.00e-15 kg
2.0 M_c  = 1.06e-15 kg
5.0 M_c  = 2.65e-15 kg
```

The pre-threshold points are controls. The `1e-15 kg` point is the first
decisive test. The `5 M_c` point would be much stronger but likely much harder.

## What would count as a serious result

A serious result needs measured center-of-mass visibility with uncertainty at
multiple masses, not merely successful state preparation.

The decisive observable is a visibility curve whose residual decoherence:

- turns on near `M_c`;
- does not vanish when environmental controls improve;
- beats CSL, GRW, Diosi-Penrose and nuisance environment in the preregistered
  comparison.

## Immediate research action

The next best move is to extract detailed noise budgets and feasibility
parameters from:

- arXiv:2601.06608;
- arXiv:2408.11909;
- QGEM/nanodiamond design literature around `10^-15 kg`.

Then convert these into environmental nuisance priors for `compare_models.py`.

## First-pass environmental triage

This has now been started in:

- `environment_model.py`;
- `analyze_target_1e15.py`;
- `target_1e15_analysis.json`.

The first-pass model includes gas-collision decoherence and placeholder
nuisance rates for magnetic/current noise and blackbody effects. The latter two
must be replaced by values extracted from detailed chip geometry and noise
budgets before any strong claim.

The current first-pass normalized budget is in:

- `target_1e15_noise_budget.py`
- `TARGET_1E15_NOISE_BUDGET.md`

It anchors the extracted 99% contrast tolerances to a reference rate of
`-ln(0.99)/0.1 ≈ 0.1005 s^-1`, then scans best-case / tolerance / 10x-worse
conditions.
