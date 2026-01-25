# Header Info
>
> **Universidade Federal do Rio de Janeiro**
> **DOI:** [10.5281/zenodo.18364790](https://doi.org/10.5281/zenodo.18364790)
> **Category:** Theoretical Modeling / Computational Psychiatry

# Entropic Psychiatry: An Illustrative Computational Case Study

**Douglas H. M. Fulber**
*Universidade Federal do Rio de Janeiro*

---

## Abstract

We present a computational demonstration of the **Topological Theory of Cognitive States**. Using a simplified coupled-oscillator model, we simulate the dynamics of a neural network under three distinct pathological constraints: (1) High Metric Depth (The Entropic Trap), (2) Low Phase Coupling (Oscillatory Chaos), and (3) High Medium Damping (Viscosity). We show that standard therapeutic interventions (Energy Injection vs. Damping vs. Frequency Driving) act distinctively on these topologies, suggesting that "Treatment Resistance" may essentially be a "Topology-Intervention Mismatch". This case study serves as a proof-of-concept for Physics-Based Stratification.

---

## 1. Introduction

Current psychiatric nosology (DSM-5) classifies disorders by symptom clusters. However, two patients with "Major Depression" may respond oppositely to the same treatment (e.g., SSRIs vs. TMS). We hypothesize that this divergence arises because "Depression" is a phenomenological attractor that can be reached via distinct physical pathways.

## 2. Methodology: The Simulation

We utilized the **Topological Cognition Toy Model** (Fulber, 2026) to generate synthetic neural networks ($N=100$) representing distinct biotypes.

### 2.1 The Biotypes Defined

* **Type A: The Entropic Trap (Deep Well)**
  * **Physics:** High internal connectivity ($k \gg k_{crit}$) leading to deep local minima in the energy landscape.
  * **Simulation:** Watts-Strogatz graph with high clustering ($C \to 1$) and rewiring $p \approx 0$.
  * **Behavior:** System states gets "stuck" in loops; highly resistant to noise.

* **Type B: Oscillatory Chaos (Desynchronization)**
  * **Physics:** Weak coupling strength ($\kappa < \kappa_{crit}$) prevents global phase locking.
  * **Simulation:** Ring lattice with randomized edge weights.
  * **Behavior:** High-frequency noise, inability to sustain coherent global states.

* **Type C: Viscous Medium (Overdamping)**
  * **Physics:** High friction coefficient ($\gamma$) in the nodal equation of motion: $\ddot{x} + \gamma \dot{x} + \nabla V = 0$.
  * **Simulation:** Standard Small-World topology but with high global damping parameter.
  * **Behavior:** Signals decay exponentially; system is sluggish.

## 3. Results: Intervention Mismatch

We simulated the application of three abstract interventions:

1. **Kick (TMS):** Adding random high-energy noise ($\eta(t)$).
2. **Drive (Neurofeedback):** Adding a periodic driver ($F\sin(\omega t)$).
3. **Thinning (Metabolic):** Reducing the damping coefficient ($\gamma$).

### 3.1 The "Trap" Response

* **Kick:** **Effective.** The noise provides the activation energy ($\Delta E$) to cross the barrier and exit the trap.
* **Drive:** Ineffective. The system is too rigid to follow the driver.
* **Thinning:** Ineffective. The well is topological, not frictional.

### 3.2 The "Chaos" Response

* **Kick:** **Detrimental.** Adds more entropy to an already entropic system. Worsens anxiety.
* **Drive:** **Effective.** The external frequency forces phase-locking via resonance (Arnold Tongues).
* **Thinning:** Neutral.

### 3.3 The "Viscous" Response

* **Kick:** **ineffective.** The energy is dissipated by friction (heat) before reorganization occurs.
* **Drive:** **Ineffective.** The driver is overdamped.
* **Thinning:** **Effective.** Lowering $\gamma$ restores signal propagation range.

## 4. Discussion: Towards Entropic Stratification

This computational exercise demonstrates that **phenomenological similarity does not imply physical identity**. All three biotypes might score high on a standard depression scale (e.g., HAM-D) due to "low activity", but the **physics of the failure**—and thus the cure—is orthogonal.

We propose that future clinical trials should stratify patients not by symptoms, but by **Spectral Signature**, matching the physics of the intervention to the topology of the disorder.

---

## Disclaimer

This is a **computational theoretical model** illustrating the principles of the Topological Theory of Cognitive States. It is not a report of clinical trial results. The "Treatments" described are abstract mathematical operators.
