# Universal Critical Mass for Quantum Collapse (M_c)

[![Theory](https://img.shields.io/badge/Theory-Quantum_Gravity-8B5CF6?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Calibrated-00C853?style=for-the-badge)](.)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](.)

> *"Do not expand the theory. Sharpen the blade."*

---

## Overview

This repository presents a **calibrated model** for the breakdown of quantum unitarity at macroscopic scales. We derive a fundamental mass threshold where quantum coherence spontaneously decays due to interaction with the cosmological acceleration horizon.

[![Central Prediction](https://img.shields.io/badge/M__c-5.29_×_10⁻¹⁶_kg-FF6B6B?style=for-the-badge)](.)
[![Coherence Time](https://img.shields.io/badge/τ__c-2.18_seconds-4ECDC4?style=for-the-badge)](.)
[![Exponent](https://img.shields.io/badge/α-2.0-FFE66D?style=for-the-badge)](.)

---

## Key Parameters

| Parameter | Value | Physical Meaning |
|:----------|:------|:-----------------|
| **M_c** | `5.29 × 10⁻¹⁶ kg` | Universal critical mass |
| **τ_c** | `2.18 seconds` | Intrinsic coherence time at M_c |
| **α** | `2.0` | Power law exponent |
| **R_c** | `386 nm` | Silica sphere radius at M_c |
| **M_c** | `3.19 × 10¹¹ Da` | In atomic mass units |

---

## Theoretical Foundation

### Core Equation

The critical mass derives from 8-dimensional phase space geometry:

$$M_c = m_P \cdot \left(\frac{a_0}{a_P}\right)^{1/8}$$

**Where:**

- `m_P ≈ 2.17 × 10⁻⁸ kg` — Planck mass
- `a_0 ≈ 6.8 × 10⁻¹⁰ m/s²` — Cosmological acceleration (c · H₀)
- `a_P ≈ 5.56 × 10⁵¹ m/s²` — Planck acceleration

### Why Exponent 1/8?

The relativistic phase space of a particle is 8-dimensional:

$$\dim(\mathcal{M}_8) = \dim(x^\mu) + \dim(p_\mu) = 4 + 4 = 8$$

Projection from 8D volume to 1D mass parameter yields the eighth root.

### Coherence Time (Calibrated)

Derived from gravitational self-energy (Penrose-like):

$$\tau_c = \frac{\hbar \cdot R_c}{G \cdot M_c^2} \approx 2.18 \text{ s}$$

For masses above threshold:

$$\tau(M) = \tau_c \cdot \left(\frac{M_c}{M}\right)^\alpha \quad \text{for } M > M_c$$

---

## Results

### Calibrated Model

<p align="center">
  <img src="calibrated_mc_model.png" alt="Calibrated M_c Model" width="90%">
</p>

*Four-panel visualization: (a) Coherence time vs mass, (b) Decoherence rate, (c) Visibility decay, (d) Parameter space regions*

### Experimental Predictions

<p align="center">
  <img src="experimental_predictions.png" alt="Experimental Predictions" width="90%">
</p>

*Comparison with experimental scenarios and competing collapse models (CSL, Diósi-Penrose)*

### Model Comparison

<p align="center">
  <img src="models_mass_comparison.png" alt="Models Comparison" width="80%">
</p>

*Decoherence rate predictions: M_c vs CSL, GRW, and Diósi-Penrose across mass range*

---

## Experimental Predictions

| Experiment | M/M_c | τ(M) | Testable |
|:-----------|:------|:-----|:---------|
| Large Molecule Interferometry | ≪ 1 | ∞ | Below threshold |
| Levitated Nanoparticle (small) | ≪ 1 | ∞ | Below threshold |
| Nanoparticle @ M_c | 1.0 | ~2.2s | Threshold |
| **MAQRO Target Mass** | **1.9** | **0.61s** | **Yes** |
| Large Nanosphere | 18.9 | 6.1ms | Yes |
| Micromechanical Oscillator | 1889 | 0.6μs | Yes |

### Critical Test: MAQRO Mission

[![Target Mass](https://img.shields.io/badge/Target-10⁻¹⁵_kg-informational?style=flat-square)](.)
[![Coherence](https://img.shields.io/badge/τ-0.61_s-success?style=flat-square)](.)
[![T_half](https://img.shields.io/badge/t₁/₂-63_ms-warning?style=flat-square)](.)

- **Mass:** 10⁻¹⁵ kg (≈ 2× M_c)
- **Predicted coherence time:** 0.61 seconds
- **Time to 50% visibility:** ~63 milliseconds
- **Verdict:** Stable interference for t > 1s falsifies the theory

---

## Falsifiability Criteria

> **The theory is falsified if:**

| Criterion | Condition |
|:----------|:----------|
| Coherence limit | V > 50% observed for M ≥ 10⁻¹⁴ kg at t > 1 second |
| No threshold | Coherence observed for M ≫ M_c at t ≫ τ(M) |
| Wrong scaling | Observed α ≠ 2 |
| Environmental dependence | τ increases with isolation for M > 5×10⁻¹⁵ kg |

---

## Project Structure

```
limits/
├── README.md                        # This file
├── index.html                       # Web article (full paper)
├── ESTRATEGIA_MC_RESEARCH.md        # Strategic research roadmap
│
├── massa_critica/                   # Original hypothesis
│   ├── README.md                    # Full derivation (English)
│   └── hipotese_colapso_quantico/   # Portuguese version
│
├── simulations/                     # Python framework
│   ├── constants.py                 # Physical constants & M_c
│   ├── calibration.py               # Model calibration
│   ├── collapse_dynamics.py         # Temporal models
│   ├── decoherence_models.py        # CSL, GRW, DP, M_c
│   └── experimental_predictions.py  # Concrete predictions
│
└── ajustefino/                      # Background materials
```

---

## Quick Start

```bash
# Print calibrated constants
python -c "from simulations.constants import print_constants; print_constants()"

# Run full calibration analysis
cd simulations && python calibration.py

# Generate experimental predictions
cd simulations && python experimental_predictions.py
```

### Sample Output

```
============================================================
PHYSICAL CONSTANTS FOR M_c RESEARCH
============================================================

--- CRITICAL MASS (CENTRAL PREDICTION) ---
M_c = m_P × Xi^(1/8)     = 5.2926e-16 kg
M_c in Daltons           = 3.1873e+11 Da

--- CALIBRATED MODEL PARAMETERS ---
τ_c (coherence @ M_c)    = 2.1763e+00 s (2.18 seconds)
α (power law exponent)   = 2.0

--- EXPERIMENTAL SCALES ---
Silica sphere radius @ M_c = 385.8 nm
============================================================
```

---

## Additional Figures

<details>
<summary><b>Collapse Time vs Mass (Multiple Exponents)</b></summary>
<br>
<p align="center">
  <img src="collapse_time_vs_mass.png" alt="Collapse Time" width="70%">
</p>

*Coherence time τ(M) for different power law exponents α = 1, 2, 4, 8*
</details>

<details>
<summary><b>Phase Portrait</b></summary>
<br>
<p align="center">
  <img src="phase_portrait.png" alt="Phase Portrait" width="70%">
</p>

*Parameter space: collapse time as function of mass and exponent*
</details>

<details>
<summary><b>Spatial Dependence</b></summary>
<br>
<p align="center">
  <img src="models_spatial_comparison.png" alt="Spatial Comparison" width="70%">
</p>

*Model predictions as function of superposition separation Δx*
</details>

---

## References

1. Verlinde, E. (2011). *On the Origin of Gravity and the Laws of Newton*. JHEP 1104:029.
2. Verlinde, E. (2017). *Emergent Gravity and the Dark Universe*. SciPost Phys. 2, 016.
3. Penrose, R. (1996). *On Gravity's role in Quantum State Reduction*. Gen. Relativ. Gravit. 28, 581.
4. Diósi, L. (1987). *A universal master equation for the gravitational violation of quantum mechanics*. Phys. Lett. A 120, 377.
5. Bassi, A. et al. (2013). *Models of wave-function collapse*. Rev. Mod. Phys. 85, 471.
6. Romero-Isart, O. (2011). *Quantum Superposition of Massive Objects*. Phys. Rev. A 84, 052121.
7. Kaltenbaek, R. et al. (2016). *MAQRO: 2015 Update*. EPJ Quantum Technology 3, 5.

---

## Author

**Douglas H. M. Fulber**  
Federal University of Rio de Janeiro  
January 2026

---

## Status

| Component | Status |
|:----------|:-------|
| Theoretical derivation | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) |
| Model calibration | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) |
| Numerical simulations | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) |
| Experimental predictions | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) |
| Paper 0 (derivation) | ![In Progress](https://img.shields.io/badge/-In_Progress-FFC107?style=flat-square) |
| Experimental collaboration | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) |

---

<p align="center">
  <strong>The number M_c ~ 10⁻¹⁶ kg bites reality.</strong><br>
  <em>Explore where this number makes predictions.</em>
</p>
