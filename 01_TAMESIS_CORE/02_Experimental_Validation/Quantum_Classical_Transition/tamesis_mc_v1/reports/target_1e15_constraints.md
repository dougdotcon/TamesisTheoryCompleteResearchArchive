# Target 1e-15 kg: extracted experimental constraints

This file records the concrete constraints extracted from the source papers for
the current Bohr-level candidate target.

## Source 1: arXiv:2408.11909

Relevant extracted values:

- mass: `1e-15 kg`
- target superposition size: `~50 μm`
- total sequence time: `~0.1 s`
- initial separation after stage 1: `~6 nm`
- separation after enhancement stage: `~37.14 μm`
- final large separation: `~50 μm`
- initial wave packet width: `σ0 = 2e-11 m`
- gradient fluctuation tolerance for 99% contrast:
  - linear magnetic field: `< 1e-7`
  - nonlinear magnetic field: `< 1e-7`
- earlier nonlinear-only scheme tolerance for 99% contrast:
  - `< 1e-9`
- initial position deviation tolerance for 99% contrast:
  - with IHP: `~1e-9 m`
  - without IHP: `~1e-11 m`

Source:
https://arxiv.org/abs/2408.11909

## Source 2: arXiv:2601.06608

Relevant extracted values:

- mass range: `1e-19 kg < m < 1e-15 kg`
- target superposition size: `O(10 μm) < Δx < O(1 nm)` depending on launch position
- ideal `1e-15 kg` case: `Δx ~ O(1 nm)` in `t ~ 0.1 s`
- wire geometry: `2a = 18 μm`, `2b = 14 μm`
- levitation current: `24 A`
- field gradient scale: `η_L ~ 1e5 T/m`
- tight trap frequencies in orthogonal directions: `ω_y ≈ ω_z ~ 1.05e4 Hz`
- magnetic field control is acknowledged as a future high-temperature-superconducting challenge
- subsequent work explicitly points to magnetic-noise and rotational effects as remaining issues

Source:
https://arxiv.org/abs/2601.06608

## Interpretation for Tamesis

The target is not yet Bohr-level because the decisive quantity is not only mass.
It is mass plus control of:

- magnetic gradient stability;
- initial position precision;
- rotational stability;
- gas pressure;
- blackbody and thermal noise;
- readout contrast uncertainty.

The key extracted threshold is:

```text
99% contrast requires gradient fluctuations below 1e-7
```

That is a very useful experimental budget for the first hard Tamesis test.
