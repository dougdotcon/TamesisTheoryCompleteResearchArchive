# Target 1e-15 kg — Feasibility Audit

## Verdict

The `1e-15 kg` target is scientifically interesting, but the current repository target is not yet a fully source-supported experimental point.

The valid statement is:

- `1e-15 kg` is a plausible frontier target.
- `1e-15 kg + 0.1 s` is useful.
- `1e-15 kg + 50 µm + 0.1 s` is not yet fully justified as a single source-supported configuration.

## Source-supported target

Supported by the 2026 nanodiamond/chip proposal:

- mass range: `1e-19 kg < m < 1e-15 kg`
- time: `t <= 0.1 s`
- upper-mass end: `m = 1e-15 kg`
- corresponding superposition size at the upper end: approximately `O(1 nm)`

This is the most defensible source-supported upper-edge point.

## Interpolated target

An interpolated target is allowed only if the interpolation rule is explicit.

Example:

- mass between `1e-19 kg` and `1e-15 kg`
- separation interpolated between the source-supported extremes
- method: monotone interpolation along the proposal's launch-position family

Current repository does not yet compute this interpolation explicitly.

## Hypothetical ideal target

The repository's current operational point:

- `m = 1e-15 kg`
- `Δx = 50 µm`
- `t = 0.1 s`

This is useful as a stress test, but it is not yet proven to be a physically realizable triple.

## Observed experiment

Observed matter-wave records used as consistency checks:

- C60 diffraction
- molecules beyond 10,000 amu
- oligoporphyrins beyond 25 kDa
- sodium nanoparticles above 170,000 Da

These are below `M_c` and do not directly test the threshold.

## Practical conclusion

The target becomes strong only after the source-supported geometry is separated from the idealized geometry.

The repository should keep three distinct labels:

1. `source_supported_target`
2. `interpolated_target`
3. `hypothetical_ideal_target`

Until that separation is enforced, the `50 µm` result should be treated as provisional.

