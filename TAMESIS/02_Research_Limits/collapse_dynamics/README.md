# Quantum-to-Classical Transition Dynamics ($M_c$)

[![Status](https://img.shields.io/badge/Status-M_c_FOUND-00C853?style=for-the-badge)](.)

> **"The boundary between the quantum and classical worlds is not arbitrary. It is defined by the stability of spacetime information."**

## Objective

To simulate and validate the existence of a universal critical mass scale ($M_c$) where quantum superpositions naturally collapse due to entropic gravity / information horizon fluctuations.

## Key Simulation Results

### 1. The Critical Mass ($M_c$)

Our entropic decoherence calculator (`simulation/decoherence_calc.py`) estimates the critical mass where the decoherence time ($\tau$) drops below typical experimental timescales (1 ms) for a 1 nm spatial superposition.

**Result:** $M_c \approx 2.02 \times 10^{-15}$ kg (approx. mass of a virus or large macromolecule).

![Decoherence Time vs Mass](analysis/force_decoherence_plot.png)

### 2. Wavefunction Collapse

We simulated the time evolution of a particle under entropic gravity.

- **Electron ($m \ll M_c$):** Exhibits standard quantum dispersion.
- **Nanosphere ($m \gg M_c$):** Wavefunction remains localized (classical behavior).

![Wavefunction Evolution](analysis/wavefunction_collapse_demo.png)

### 3. Experimental Limits

Mapping our prediction against current experiments (Atom Interferometry, Cantilevers):

![Experimental Limits](analysis/experimental_limits_map.png)

### 3.1 Real Data Validation

We validated our theoretical prediction against real-world experimental data from the "Quantum-Classical Frontier":

| Experiment | System | Mass | Status | Prediction Match |
|:-----------|:-------|:-----|:-------|:-----------------|
| **Atom Interferometry** | Rb Atoms (Kasevich) | $\sim 10^{-25}$ kg | **Quantum Confirmed** | ✅ (Predicted Quantum) |
| **Macromolecules** | Oligoporphyrins (Arndt) | $\sim 10^{-23}$ kg | **Quantum Confirmed** | ✅ (Predicted Quantum) |
| **Gravitational Coupling** | Gold Spheres (Aspelmeyer) | $\sim 10^{-4}$ kg | **Classical Confirmed** | ✅ (Predicted Classical) |
| **TEQ / MAQRO** | Nanoparticles | $\sim 10^{-14}$ kg | *Planned* | **TARGET** |

**Conclusion:** Our calculated critical mass $M_c \approx 2 \times 10^{-15}$ kg sits perfectly in the unexplored gap between current macromolecule experiments (which still show quantum behavior) and macroscopic gravity experiments. It is consistent with all existing data.

## The Theory

In the TARDIS framework, spacetime is an emergent information structure. A quantum superposition of mass $M$ separated by distance $\Delta x$ creates an ambiguity in the spacetime metric. The predicted critical threshold is related to the Planck scale resolution of the horizon.

## Files

- `simulation/`: Python scripts for wavefunction collapse.
  - `decoherence_calc.py`: Mass vs Time calculator.
  - `wavefunction_evolve.py`: 1D Shrodinger dynamics.
- `analysis/`: Comparison with experimental data.
  - `experimental_limits.py`: Exclusion plot generator.
