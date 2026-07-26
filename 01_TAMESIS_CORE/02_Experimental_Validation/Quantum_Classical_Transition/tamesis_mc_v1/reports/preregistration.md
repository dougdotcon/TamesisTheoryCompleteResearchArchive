# Pre-registration: Tamesis vs CSL, GRW, DP, and environmental decoherence

This document defines the comparison before looking at the final data.
It is a protocol, not a result.

## Question

Does the Tamesis threshold model explain center-of-mass coherence data better than fixed-parameter CSL, GRW, Diosi-Penrose, or a nuisance environmental baseline?

## Primary endpoint

Binary coherence outcome at a fixed observation time:

- `observed_coherence = true` when interference survives above the preregistered threshold;
- `observed_coherence = false` when it does not.

## Inclusion rules

Use only experiments that probe center-of-mass coherence or direct decoherence.
Exclude internal-mode coherence, purely thermal noise measurements, and any point where mass is not the relevant control variable.

## Model set

- Tamesis `McModel` with fixed `M_c`, fixed `tau_c`, fixed exponent `alpha = 2`.
- CSL with canonical literature values.
- GRW with canonical literature values.
- Diosi-Penrose with standard gravitational self-energy scaling.
- Environmental baseline with one fitted nuisance decay rate per experiment family.

## Statistical plan

For each record:

1. Compute model coherence probability `p`.
2. Use Bernoulli likelihood on the observed binary outcome.
3. Sum log-likelihoods across records.
4. Compare models with AIC and BIC.
5. Report ranking and per-record predictions.

## Sensitivity checks

- Repeat the fit with and without each experiment family.
- Report whether the ranking changes under reasonable nuisance-rate variation.
- Keep the full record table and do not drop failures after seeing outcomes.

## Falsification language

Tamesis v1.0 is disfavored if:

- the environmental baseline explains the data equally well or better with fewer assumptions;
- the fixed-threshold prediction does not beat CSL/GRW/DP on preregistered likelihood;
- the observed transition remains smooth where Tamesis predicts a sharp threshold.

## Current status

The archive does not yet contain a full raw-data table with all nuisance metadata.
This means the protocol is ready before the inference is.
