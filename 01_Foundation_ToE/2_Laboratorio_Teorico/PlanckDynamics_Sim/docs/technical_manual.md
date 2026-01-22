# Technical Manual: PlanckDynamics Legacy Simulation Engine

**Version:** 2.0 (Legacy)
**Module:** `src/` physics engine

## Overview
This document details the architecture of the legacy Python simulation engine found in the `src/` directory. This engine was used for the initial "TARDIS Universe" simulations and hypothesis testing before the Phase 1-3 MCMC validation.

## Architecture

### Directory Structure
The core logic resides in `src/` and is structured as follows:

-   `src/constants_physics.py`: Classes for time-varying physical constants.
-   `src/tardis_universe_model.py`: Implementation of the metric compression model.
-   `src/main_physics_test_v2.py`: The numerical integrator for the Friedmann equations.

### component Descriptions

#### 1. DynamicPhysicsConstants (`src/constants_physics.py`)
**Purpose:** Models the theoretical variation of fundamental constants ($G, c, h, \alpha$) during early cosmological epochs.

**Key Features:**
*   **Supercosmic Events:** Registry for discrete phase transitions (e.g., Symmetry Breaking).
*   **Temporal Variation functions:** $G(t)$ and $c(t)$ models based on scalar field coupling.
*   **Regularization:** Numerical dampening to prevent divergences at $t \to 0$.

#### 2. TARDISUniverse (`src/tardis_universe_model.py`)
**Purpose:** Implements the "Internal vs External" dimensional manifold logic.

**Core Concept:**
The universe is modeled as a manifold with fixed external topology but varying internal metric density.
*   **Measurement:** $\Gamma = \frac{V_{internal}}{V_{external}}$ (Compression Factor).
*   **Observables:** Predicts redshift anomalies due to metric compression.

#### 3. PhysicsTestSystemV2 (`src/main_physics_test_v2.py`)
**Purpose:** A robust numerical solver (DOP853 integrator) for the modified cosmological equations.

**Numerical Method:**
*   **Integrator:** `scipy.integrate.ode` with 8th order Runge-Kutta.
*   **Stability:** Includes $\epsilon = 10^{-15}$ regularization terms.
*   **Hypotheses Tested:**
    1.  Dynamic Laws (Variation of Constants).
    2.  TARDIS Metric (Quantum Compression).

## Usage
To reproduce the legacy simulations:

```bash
python src/main_physics_test_v2.py
```

## Data Artifacts
Simulations generate JSON reports and NPZ archives in the `resultados/` directory, containing time-series data for $a(t)$, $H(t)$, and thermodynamic variables.
