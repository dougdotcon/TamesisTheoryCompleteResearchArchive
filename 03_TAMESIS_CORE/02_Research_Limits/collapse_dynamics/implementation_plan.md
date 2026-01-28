# Implementation Plan: Quantum Collapse Dynamics ($M_c$)

## Goal

To computationally model the transition from quantum to classical mechanics using Entropic Gravity principles, specifically identifying the critical mass $M_c$ where intrinsic decoherence becomes dominant.

## User Review Required
>
> [!IMPORTANT]
> **Theory Choice:** We will use the **Schrödinger-Newton-Entropic** approach. This modifies the standard Schrödinger equation with a non-linear term representing the information cost of spacetime superposition.
> confirm if we should align with **Penrose-Diosi** (gravitational self-energy) or **Verlinde/TAMESIS** (entropic force fluctuations). *Defaulting to Hybrid TAMESIS model.*

## Proposed Changes

### 1. `collapse_dynamics/simulation/`

#### [NEW] `decoherence_calc.py`

- **Function:** Calculate decoherence times for varying masses and delocalizations.
- **Input:** Mass array ($10^{-18}$ kg to $10^{-6}$ kg), Separation distance.
- **Output:** Decoherence time $\tau$.
- **Key Logic:** Implement $\tau \approx \hbar / \Delta E_{entropic}$.

#### [NEW] `wavefunction_evolve.py`

- **Function:** Time-evolution of a 1D wavefunction for a massive particle.
- **Method:** Split-operator Fourier Transform method.
- **Dynamics:** Standard Hamiltonian + Entropic Decay term.

### 2. `collapse_dynamics/analysis/`

#### [NEW] `experimental_limits.py`

- **Function:** Plot our predictions against current experimental exclusion plots (e.g., TEQ, Aspelmeyer group results).
- **Goal:** Show where $M_c$ sits relative to current technology.

## Verification Plan

### Automated Tests

- Run `decoherence_calc.py` for an electron (should be infinite/stable).
- Run `decoherence_calc.py` for a bowling ball (should be instantaneous).
- Verify $M_c$ emerges around $10^{-14} - 10^{-11}$ kg.

### Manual Verification

- Inspect the "Collapse vs Mass" plot.
- Verify the transition curve is sharp (phase transition like).
