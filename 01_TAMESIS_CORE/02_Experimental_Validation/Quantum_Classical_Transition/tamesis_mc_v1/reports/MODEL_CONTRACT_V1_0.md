# MODEL CONTRACT V1.0

## 1. Exact equation for M_c

`M_c = m_P * (a_0 / a_P)^(1/8)`

with:

- `a_0 = c H_0`
- `a_P = c^2 / l_P`
- `m_P = sqrt(hbar c / G)`

## 2. Constants used

- `G = 6.67430e-11 m^3 kg^-1 s^-2`
- `hbar = 1.054571817e-34 J s`
- `c = 299792458 m s^-1`
- `H_0 = 70 km s^-1 Mpc^-1 = 2.268545502662652e-18 s^-1`
- `silica_density = 2200 kg m^-3`

## 3. Value of M_c

- full value: `5.292674126388712e-16 kg`
- reportable value: `5.29e-16 kg`
- `M_c ≈ 3.1873e11 amu`

## 4. Exact Tamesis rate

`Gamma_T(M) = 0` for `M <= M_c`

`Gamma_T(M) = tau_c^-1 * (M/M_c)^2` for `M > M_c`

This is the v1.0 contract. It is a sharp-threshold hypothesis.

## 5. Exact visibility

`V(t) = exp(-(Gamma_T + Gamma_env) * t)`

If `Gamma_env = 0`, then `V(t) = exp(-Gamma_T t)`.

## 6. Meaning of tau_c

`tau_c = hbar * R / (G * M_c^2)`

where:

- `R` is the silica-equivalent radius derived from `M_c`
- `tau_c = 2.176246482178091 s`

## 7. Meaning of the 1/8 root

The root-eighth is a structural hypothesis.
It is not derived in v1.0.
It is frozen as part of the versioned contract.

## 8. Separation dependence

`separation_dependence: absent_in_v1_0`

In v1.0, separation does not enter `Gamma_T`.
Only mass and time enter the intrinsic Tamesis rate.

## 9. Geometrical dependence

Not modeled in v1.0.
Geometry appears only in nuisance / target-specific environmental interpretation.

## 10. Domain of validity

- versioned as `v1.0`
- phenomenological
- sharp-threshold
- auditable
- not a proof

## 11. Falsification criteria

The model is falsified if a pre-registered experiment in the threshold region shows:

- no intrinsic visibility loss where `Gamma_T > 0` predicts one, or
- a statistically stronger rival model under the registered likelihood, or
- internal inconsistencies in the frozen `M_c` contract.

## 12. What is derived vs assumed

- `derived`: `M_c`, `R`, `tau_c`, predicted rates, predicted visibilities
- `measured_input`: `H_0`
- `fixed_convention`: units, `Gamma_T = 0` below threshold, `separation_dependence = absent_in_v1_0`
- `modelling_assumption`: root-eighth, quadratic above-threshold exponent, sharp threshold, silica density

