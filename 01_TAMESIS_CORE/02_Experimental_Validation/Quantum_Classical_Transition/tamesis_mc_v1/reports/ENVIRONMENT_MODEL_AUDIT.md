# Environment Model Audit

## Scope

Current environment layer:

- gas collisions
- scalar magnetic/current nuisance rate
- scalar blackbody nuisance rate

## What the code actually does

The present model uses:

- a hard-sphere gas collision estimate
- a total nuisance rate `Gamma_env`
- a multiplicative visibility loss `exp(-Gamma_env t)`

This is a transparent first-pass triage model.

## Why `7e-13 Pa` is not universal

The pressure number comes from a specific scenario:

- target mass: `1e-15 kg`
- gas temperature: `20 K`
- assumed gas species mass: `28 amu`
- assumed material density: `3500 kg m^-3`
- assumed geometry: sphere-equivalent radius from mass
- assumed time: `0.1 s`

Therefore `7e-13 Pa` is not a law.
It is the pressure at which this simplified gas model becomes comparable to the Tamesis rate for this specific target.

## Missing channels

The current environment model does not yet separate:

- gas species dependence beyond one mean mass
- blackbody absorption and emission as full channels
- rotational decoherence
- charge / patch potential noise
- vibrational noise
- detector-induced contrast loss
- geometry-specific cross sections

## Thermal gate

The `4 K` gate is conservative and source-linked.
It should not be interpreted as a universal cutoff across all platforms.

## Conclusion

The current environment model is useful for screening.
It is not yet a publication-grade environmental theory.

