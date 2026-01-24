# TAMESIS: The Holographic Origin of Matter and Dynamics

## A Unified Geometric Framework for Fundamental Physics

![Status: Under Review](https://img.shields.io/badge/Status-Under_Review-orange.svg)
![Version: 4.1.0](https://img.shields.io/badge/Version-4.1.0-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Framework: Entropic Gravity](https://img.shields.io/badge/Framework-Entropic_Gravity-violet.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18134060.svg)](https://doi.org/10.5281/zenodo.18134060)

---

## 📄 Executive Summary

This repository contains the source code, derivations, and manuscripts for the **TAMESIS (Topological Analysis of Recursive Dimensional Information Systems)** framework.

This work proposes a phenomenological extension to the Standard Model of particle physics and Cosmology, based on a single **Postulate of Holographic Compression**. We explore the hypothesis that the values of fundamental constants (electron mass, $\alpha$, $G$) are not random, but coupled through a dimensionless structural parameter $\Omega \approx 117.038$.

**Key Proposal:**  
*"Standard Model parameters are thermodynamic equations of state for a holographic universe."*

---

## 🧭 Scope and Non-Claims

To ensure scientific clarity, we define exactly what this framework is and what it is not.

**The TAMESIS framework does NOT claim to:**

- Provide a UV-complete quantum gravity theory (like String Theory or Loop Quantum Gravity).
- Replace Quantum Field Theory or General Relativity at currently tested scales.
- Derive exact numerical values from pure mathematics without phenomenological calibration.

**Instead, TAMESIS is intended as:**

- A **phenomenological geometric framework** that unifies constants.
- A method for **parameter reduction** via holographic scaling arguments.
- A generator of **falsifiable mesoscopic and cosmological predictions** (e.g., $M_c$, Lepton stability).

---

## 📐 Core Postulate: The $\Omega$ Scaling

We posit that the ratio between the bulk information capacity ($I_{bulk}$) and the boundary encoding ($I_{boundary}$) is governed by a universal constant $\Omega$.

$$ \boxed{\Omega \equiv \frac{\text{Information Capacity (Bulk)}}{\text{Information Capacity (Boundary)}} \approx 117.038} $$

**Methodology:**

1. **Calibration:** We fix $\Omega$ using the electron mass $m_e$ and the observable universe mass $M_U$.
2. **Validation:** We test if this *same* $\Omega$ successfully predicts the fine-structure constant $\alpha$, lepton generations, and critical collapse scales.

---

## 🧪 Falsifiability ("The Kill List")

Unlike traditional "Everything Theories" that are untestable, the TAMESIS framework makes specific, dangerous predictions.

### Local Refutations (Invalidate Specific Sectors)

- **Failure of $M_c$:** Observation of stable quantum interference for mass $M \gg 10^{-16}$ kg falsifies the holographic collapse hypothesis (but not necessarily the scaling laws).

- **Lepton Instability:** Discovery of a stable 4th generation lepton falsifies the topological resonance model.

### Global Refutations (Invalidate the Framework)

- **Inconsistency of $\Omega$:** If $\Omega$ calculated from $\alpha$ drifts apart from $\Omega$ calculated from $m_e$ over cosmological time.

- **Emergence of Free Parameters:** If fitting new data requires introducing arbitrary "fudge factors" not derived from $\Omega$.

---

## 🔍 On Numerology vs. Phenomenology

We explicitly address the concern of "curve fitting":

While the framework employs scaling laws, **these relations are not claimed as exact derivations** in the vacuum. They are consistency constraints imposed by the postulated parameter $\Omega$.

The scientific content lies not in numerical coincidence, but in:

1. **Parameter Reduction:** Reducing 19+ free parameters to 1 ($\Omega$).
2. **Cross-Domain Consistency:** The same $\Omega$ appears in Cosmology, Particle Physics, and Thermodynamics.
3. **Refutation Criteria:** The model prohibits specific observations (e.g., Axions, stable massive leptons) that other theories allow.

---

## 📊 Summary of Scaling Relationships

All "derivations" below are to be understood as **geometric consistencies** required by the $\Omega$-Postulate.

| Quantity | Scaling Hypothesis | CODATA | Status |
|:---------|:-------------------|:-------------|:----------|
| **Electron Mass** | $m_e = M_U \cdot \Omega^{-40.23}$ | $9.109...$ kg | **Fixed (Calibrated)** |
| **Fine Structure** | $\alpha^{-1} \approx \Omega^{1.03}$ | $137.036$ | **Scaling Match** |
| **Muon Mass** | $m_\mu = m_e \cdot \Omega^{1.12}$ | $1.883...$ kg | **Hierarchy Match** |
| **Tau Mass** | $m_\tau = m_e \cdot \Omega^{1.71}$ | $3.167...$ kg | **Hierarchy Match** |
| **Critical Mass $M_c$**| $M_c \approx M_P \cdot \Omega^{-4}$ | $\mathbf{1.16 \times 10^{-16}}$ **kg** | **Prediction** |

---

## 🧠 New: Universal Critical Mass ($M_c$)

Recent work (Jan 2026) has identified a specific threshold for quantum wavefunction collapse.

> **The Holographic Limit to Unitarity:**
> Objects with mass $M > M_c \approx 10^{-16}$ kg exceed the information update rate of the local holographic horizon, forcing spontaneous entropy maximization (collapse).

*See the full paper in `novos_papers/massa_critica/index.html`*

---

## 🚀 Suggested Reading Path

For external physicists and auditors, we recommend this order:

1. **Start Here:** `novos_papers/massa_critica/index.html`
    *(The shortest, most falsifiable prediction of the framework.)*

2. **Then Check Consistency:** `paper_fine_structure/`
    *(Demonstrates how $\Omega$ constrains electromagnetism.)*

3. **Full Framework:** `unified_papers_complete.html`
    *(The complete geometric interpretation and derivation set.)*

---

## 📂 Project Structure

### `1_Motores_Cientificos/` (Scientific Engines)

Core Python algorithms for testing the hypothesis.

- `Electron_Holography_Engine`: Numerical solver for topological invariants.
- `ReactiveCosmoMapper`: N-Body cosmological simulations under entropic gravity.

### `2_Laboratorio_Teorico/` (Theoretical Lab)

- `PlanckDynamics_Sim`: Simulation of scale-dependent constants.
- `FINETUNNING`: Corpus for AI-assisted physics reasoning.

### `novos_papers/` (Manuscripts)

Collection of 30+ papers exploring specific domains:

- **`massa_critica/`**: **(NEW)** Derivation of the collapse threshold.
- `paper_fine_structure/`: Topological origin of $\alpha$.
- `paper_validacao_galactica/`: Dark matter free rotation curves.

---

## 📄 Unified Documentation

The complete framework, including all derivation papers and the new Critical Mass hypothesis, is consolidated in:

👉 **[unified_papers_complete.html](unified_papers_complete.html)**
*(Comprehensive HTML document with MathJax support)*

---

## 📜 Citation

If you use this code or framework in your research, please cite:

```bibtex
@article{fulber2026tardis,
  title={The Holographic Origin of Matter and Dynamics: A Phenomenological Framework},
  author={Fulber, Douglas H. M.},
  year={2026},
  doi={10.5281/zenodo.18134060},
  note={Proposed Limit on Quantum Linearity via Omega Scaling}
}
```

---

*Disclaimer: This is a theoretical framework proposing an informational basis for physical laws. While consistent with current data, it requires specific experimental validation as outlined in the "Falsifiability" section.*
