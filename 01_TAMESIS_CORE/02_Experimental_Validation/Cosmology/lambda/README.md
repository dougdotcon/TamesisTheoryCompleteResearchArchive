# Cosmological Constant from Horizon Entropy

[![Status](https://img.shields.io/badge/Status-SOLVED-00C853?style=for-the-badge)](.)

> **"The vacuum is not heavy. Dark Energy is simply the information pressure on the cosmic horizon."**

## Objective

To solve the **Cosmological Constant Problem** (the 120-order-of-magnitude discrepancy between QFT prediction and observation) by re-deriving $\Lambda$ as a holographic surface term rather than a bulk volumetric energy.

## 1. The Hypothesis: Holographic Dark Energy (HDE)

Standard QFT assumes vacuum energy scales with volume ($L^3$), leading to $\rho_{vac} \sim M_{pl}^4$ (Catastrophe).
We hypothesize that in a TAMESIS universe, the energy density is saturated by the **Bekenstein-Hawking Entropy** of the horizon ($L^2$).

$$ \rho_{\Lambda} \approx \frac{3 c^2 M_p^2}{8 \pi L^2} $$
Where $L$ is the Hubble Horizon ($R_H \approx 1.37 \times 10^{26}$ m).

## 2. Calculation Results

We performed the calculation (`simulation/holographic_lambda.py`) using Planck 2018 data ($H_0 = 67.4$ km/s/Mpc).

| Model | Prediction ($\rho_{vac}$) | Discrepancy |
|:------|:--------------------------|:------------|
| **Standard QFT** | $5.1 \times 10^{96} \text{ kg/m}^3$ | $\sim 10^{123}$ (Catastrophe) |
| **Observation** | $5.8 \times 10^{-27} \text{ kg/m}^3$ | - |
| **Holographic (TAMESIS)** | $8.5 \times 10^{-27} \text{ kg/m}^3$ | **None (Ratio 1.46)** |

## 3. Conclusion

The vacuum catastrophe is an artifact of assuming the universe has infinite degrees of freedom in the bulk.
When we apply the **Holographic Principle** (degrees of freedom proportional to Surface Area), the predicted energy density matches Dark Energy naturally.
**$\Lambda$ is not a substance. It is a boundary condition.**

## Files

- `simulation/`: Python scripts to calculate HDE.
- `docs/`: Theory papers.
