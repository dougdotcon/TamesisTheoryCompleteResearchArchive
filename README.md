# Tamesis Theory: Complete Research Archive

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18343477.svg)](https://doi.org/10.5281/zenodo.18343477)
[![Status](https://img.shields.io/badge/Status-SYSTEM%20CLOSED-success?style=flat-square)](.)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

**Archive Version:** 1.0.0 (System Closure)
**Date:** January 2026
**Author:** Douglas H. M. Fulber

---

## 1. Project Overview

This repository contains the complete source code, derivations, and simulation engines for the **Tamesis Theory**, a unified framework proposing a structural closure to physics via holographic spacetime topology.

The project is organized into three irreversible stages, representing the evolution from theoretical proposal to falsifiable system.

### Key Predictions

1. **Topological Interference Step:** A discontinuity in wavefunction collapse at $M_c \approx 2.2 \times 10^{-14}$ kg.
2. **Spectral Mass Hierarchy:** Particle masses derived from the eigenvalues of a single spectral operator.
3. **Holographic Entropy:** Gravity and forces derived as entropic gradients on the cosmological horizon.

---

## 2. Archive Structure (Architecture)

The repository is structured logically to separate foundational theory, exploration limits, and the final rigorous closure.

```
limits/
├── paper.html                  # MASTER INDEX. Interactive definition of the theory.
├── TheTamesisTheory...pdf      # The consolidated scientific paper reference.
│
├── 01_Foundation_ToE/          # STAGE 1: THE ORIGIN
│   ├── The 43 Papers           # Deep dives into specific verticals (Cosmology, QCD, etc).
│   ├── Unified Theory          # The core holographic framework.
│   ├── Scientific Engines      # Python scripts for fundamental constants.
│   └── Derivations             # Geometric origin of Mass, Charge, Spin.
│
├── 02_Research_Limits/         # STAGE 2: THE EXPLORATION
│   ├── M_c Derivation          # Calculation of the Critical Mass threshold.
│   └── Experimental Maps       # Mapping theory to MAQRO/TEQ experiments.
│
├── 03_System_Closure/          # STAGE 3: THE END (FALSIFICATION)
│   ├── Axiomatic Reduction     # The 5 irreducible axioms.
│   ├── Spectral Operator       # Code: spectral_solver.py (GUE Statistics).
│   ├── Killer Prediction       # Code: interference_sim.py (The "Cliff" Simulation).
│   └── Death Criteria          # Code: falsify.py (Automated consistency check).
│
├── LICENSE                     # Creative Commons Attribution 4.0
├── CITATION.cff                # Citation metadata
└── README.md                   # This file
```

---

## 3. How to Reproduce Results

The simulation engines are written in Python 3.9+. They require standard scientific libraries.

### Prerequisites

```bash
pip install numpy scipy matplotlib seaborn pandas
```

### Running the Core Simulations (Stage 3)

**1. The "Killer" Interference Prediction:**
Simulates the transition from quantum to classical visibility, showing the topological step.

```bash
python 03_System_Closure/03_Killer_Prediction/interference_sim.py
```

*Output:* Generates `collapse_animation.gif` demonstrating the "Tamesis Cliff".

**2. The Spectral Operator Validation:**
Simulates the eigenvalues of the Tamesis Operator to verify GUE (Gaussian Unitary Ensemble) statistics.

```bash
python 03_System_Closure/02_Spectral_Operator/spectral_solver.py
```

*Output:* Generates `spectral_statistics.gif`.

**3. Automated Falsification Check:**
Runs the current experimental bounds against the theory's predictions.

```bash
python 03_System_Closure/05_Falsification_Criteria/falsify.py
```

*Output:* Returns `[THEORY ALIVE]` or `[THEORY DEAD]` based on data constants.

---

## 4. The "Paper.html" Interface

The file `paper.html` located in the root directory is the **primary entry point** for reviewing the theory. It is designed to be a self-contained, interactive scientific document that:

* Displays the 5 Axioms.
* Visualizes the Death Criteria.
* Links the conceptual pillars to the code verification engines.

**Recommendation:** Open `paper.html` in any modern web browser to begin the review.

---

## 5. License & Citation

This work is licensed under a **Creative Commons Attribution 4.0 International License**.

If you use this data or code in your research, please cite it using the metadata in `CITATION.cff` or:

> Fulber, D. H. M. (2026). *The Tamesis Theory: Structural Unity through Spectral Topology & Falsifiable Limits*. Zenodo. <https://doi.org/10.5281/zenodo.18343477>

---

## 6. References

### Internal Research (The 43 Papers)

The complete collection of 43 derived research papers can be found in `01_Foundation_ToE/The 43 Papers`. These cover detailed derivations for specific domains including Cosmology, QCD, and Electroweak Unification.

### Foundational Works

1. Verlinde, E. (2011). *On the Origin of Gravity and the Laws of Newton*. JHEP 04, 029.
2. Bekenstein, J. D. (1973). *Black holes and entropy*. Physical Review D 7(8), 2333.
3. 't Hooft, G. (1993). *Dimensional Reduction in Quantum Gravity*. arXiv:gr-qc/9310026.
4. Maldacena, J. and Susskind, L. (2013). *Cool horizons for entangled black holes (ER=EPR)*. Fortschr. Phys. 61, 781.
5. Penrose, R. (1996). *On gravity's role in quantum state reduction*. General relativity and gravitation, 28(5), 581-600.
