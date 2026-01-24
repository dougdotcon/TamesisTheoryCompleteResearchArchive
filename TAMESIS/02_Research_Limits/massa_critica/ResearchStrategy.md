# Research Strategy: Universal Critical Mass (M_c)

[![Status](https://img.shields.io/badge/Status-Active_Research-00C853?style=flat-square)](.)
[![Phase](https://img.shields.io/badge/Phase-Calibration_Complete-8B5CF6?style=flat-square)](.)
[![Priority](https://img.shields.io/badge/Priority-Experimental_Validation-FF6B6B?style=flat-square)](.)

> *"Do not expand the theory. Sharpen the blade."*

---

## Central Anchor Point

| Parameter | Value | Status |
|:----------|:------|:-------|
| **M_c** | 5.29 × 10⁻¹⁶ kg | ![Derived](https://img.shields.io/badge/-Derived-00C853?style=flat-square) |
| **τ_c** | 2.18 seconds | ![Calibrated](https://img.shields.io/badge/-Calibrated-00C853?style=flat-square) |
| **α** | 2.0 | ![Set](https://img.shields.io/badge/-Set-00C853?style=flat-square) |
| **R_c** | 386 nm | ![Calculated](https://img.shields.io/badge/-Calculated-00C853?style=flat-square) |

---

## Phase 1: Phenomenology — ![Complete](https://img.shields.io/badge/-COMPLETE-00C853?style=for-the-badge)

### 1.1 Collapse Dynamics Model

| Task | Status |
|:-----|:-------|
| [x] Define power law: τ(M) = τ_c × (M_c/M)^α | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement `collapse_dynamics.py` | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Test exponents α = 1, 2, 4, 8 | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Generate collapse time plots | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

### 1.2 Model Calibration

| Task | Status |
|:-----|:-------|
| [x] Derive τ_c from first principles | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Gravitational self-energy derivation | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Compare with experimental constraints | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement `calibration.py` | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Generate calibrated model plots | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

### 1.3 Decoherence Models Comparison

| Task | Status |
|:-----|:-------|
| [x] Implement M_c model class | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement CSL model | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement GRW model | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement Diósi-Penrose model | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Generate comparison plots | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

---

## Phase 2: Experimental Predictions — ![Complete](https://img.shields.io/badge/-COMPLETE-00C853?style=for-the-badge)

### 2.1 Concrete Scenarios

| Task | Status |
|:-----|:-------|
| [x] Define experimental scenarios | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Calculate predictions for each | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Implement `experimental_predictions.py` | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Generate prediction plots | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

### 2.2 Key Predictions Generated

| Experiment | M/M_c | τ(M) | Status |
|:-----------|:------|:-----|:-------|
| MAQRO Target | 1.9 | 0.61 s | ![Testable](https://img.shields.io/badge/-Testable-4ECDC4?style=flat-square) |
| Large Nanosphere | 18.9 | 6.1 ms | ![Testable](https://img.shields.io/badge/-Testable-4ECDC4?style=flat-square) |
| Micromechanical | 1889 | 0.6 μs | ![Testable](https://img.shields.io/badge/-Testable-4ECDC4?style=flat-square) |

---

## Phase 3: Documentation — ![Complete](https://img.shields.io/badge/-COMPLETE-00C853?style=for-the-badge)

| Task | Status |
|:-----|:-------|
| [x] Create `constants.py` with all parameters | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Create project README.md | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Create index.html article | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| [x] Define falsifiability criteria | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

---

## Phase 4: Paper Drafts — ![Pending](https://img.shields.io/badge/-PENDING-FFC107?style=for-the-badge)

### Paper 0: Formal Derivation

| Task | Status |
|:-----|:-------|
| [ ] Write introduction and motivation | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Formalize 8D phase space argument | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Derive M_c with full rigor | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Derive τ_c calibration | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Prepare for arXiv submission | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |

### Paper 1: Cantilever Noise Predictions

| Task | Status |
|:-----|:-------|
| [ ] Calculate excess noise at M > M_c | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Compare with experimental data | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Target: Phys. Rev. A | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |

### Paper 2: Interferometry Visibility

| Task | Status |
|:-----|:-------|
| [ ] Model visibility decay V(t, M) | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] MAQRO mission predictions | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Target: New J. Phys. | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |

### Paper 3: Model Discrimination

| Task | Status |
|:-----|:-------|
| [ ] Identify discrimination regions | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] M_c vs CSL vs GRW vs DP | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |
| [ ] Target: Phys. Rev. Lett. | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) |

---

## Phase 5: Extended Analysis — ![Not Started](https://img.shields.io/badge/-NOT_STARTED-9E9E9E?style=for-the-badge)

### 5.1 Geometric Origin of Exponent

| Task | Status |
|:-----|:-------|
| [ ] Derive 1/8 from phase space volumes | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |
| [ ] Connect to spectral dimension | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |
| [ ] Explore AdS/dS connections | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |

### 5.2 Quantum Computing Implications

| Task | Status |
|:-----|:-------|
| [ ] Maximum coherent qubit mass | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |
| [ ] Architecture limits from M_c | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |
| [ ] Target: npj Quantum Information | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) |

---

## Phase 6: Collaboration — ![Planned](https://img.shields.io/badge/-PLANNED-2196F3?style=for-the-badge)

| Task | Status |
|:-----|:-------|
| [ ] Contact MAQRO team | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) |
| [ ] Contact Vienna/Basel groups | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) |
| [ ] Contact levitated optomechanics labs | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) |
| [ ] Prepare collaboration proposal | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) |

---

## Files Generated

| File | Purpose | Status |
|:-----|:--------|:-------|
| `simulations/constants.py` | Physical constants, M_c derivation | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `simulations/collapse_dynamics.py` | Temporal dynamics models | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `simulations/decoherence_models.py` | CSL, GRW, DP, M_c comparison | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `simulations/calibration.py` | Model calibration | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `simulations/experimental_predictions.py` | Concrete predictions | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `README.md` | Project documentation | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `index.html` | Web article | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `calibrated_mc_model.png` | Calibrated model figure | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `experimental_predictions.png` | Predictions figure | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `models_mass_comparison.png` | Model comparison figure | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `collapse_time_vs_mass.png` | Collapse time figure | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |
| `phase_portrait.png` | Phase space figure | ![Done](https://img.shields.io/badge/-Done-00C853?style=flat-square) |

---

## Falsifiability Criteria

The theory is **falsified** if:

| # | Criterion | Test |
|:--|:----------|:-----|
| 1 | Coherence limit | V > 50% for M ≥ 10⁻¹⁴ kg at t > 1 s |
| 2 | No threshold | Coherence at M >> M_c for t >> τ(M) |
| 3 | Wrong scaling | α ≠ 2 observed |
| 4 | Environmental dependence | τ increases with isolation for M > 5×10⁻¹⁵ kg |

---

## Summary

| Phase | Status | Progress |
|:------|:-------|:---------|
| Phenomenology | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) | 100% |
| Experimental Predictions | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) | 100% |
| Documentation | ![Complete](https://img.shields.io/badge/-Complete-00C853?style=flat-square) | 100% |
| Paper Drafts | ![Pending](https://img.shields.io/badge/-Pending-FFC107?style=flat-square) | 0% |
| Extended Analysis | ![Not Started](https://img.shields.io/badge/-Not_Started-9E9E9E?style=flat-square) | 0% |
| Collaboration | ![Planned](https://img.shields.io/badge/-Planned-2196F3?style=flat-square) | 0% |

---

## Next Immediate Actions

| Priority | Action | Target |
|:---------|:-------|:-------|
| **HIGH** | Write Paper 0 formal derivation | arXiv |
| **HIGH** | Refine discrimination regions plot | Paper 3 |
| **MEDIUM** | Calculate cantilever noise excess | Paper 1 |
| **MEDIUM** | Model MAQRO visibility curves | Paper 2 |
| **LOW** | Formalize 1/8 exponent derivation | Phase 5 |

---

<p align="center">
<strong>The number M_c ~ 10⁻¹⁶ kg bites reality.</strong><br>
<em>Explore where this number makes predictions.</em>
</p>
