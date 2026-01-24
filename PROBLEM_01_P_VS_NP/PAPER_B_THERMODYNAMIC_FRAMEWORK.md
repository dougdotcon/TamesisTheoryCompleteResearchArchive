# DOCUMENT B: PHYSICAL FRAMEWORK

## The Thermodynamic Cost of Logic

> **Abstract:** This document provides the physical context for the Censorship Theorem. We analyze computation not as logic, but as a thermodynamic process of state selection. We show that "solving" a hard problem is equivalent to "freezing" a spin glass, a process inherently limited by the Third Law of Thermodynamics.

---

## 1. Computation as Entropy Reduction

Solving a decision problem (like 3-SAT) is physically equivalent to reducing the entropy of a system.

* **Initial State:** Uniform superposition/distribution of all $2^N$ possible assignments. Entropy $S = N \ln 2$.
* **Final State:** The single satisfying assignment (or 'unsatisfiable' flag). Entropy $S = 0$.

### 1.1 Landauer's Limit

Landauer's Principle states that erasing 1 bit of information costs $k_B T \ln 2$ energy.
Pure erasure is linear. However, **State Selection** (finding the low entropy state in a rugged landscape) is non-linear.

## 2. The Entropic Barrier

### 2.1 The Spin Glass Analogy

NP-Hard problems map to **Spin Glasses**.

* The solution is the Ground State.
* Local minima are "False Solutions".
* The landscape is "frustrated".

In a Spin Glass, the time required to relax to the true ground state scales as $e^{\xi N}$ (Arrhenius Law). This is not an artifact of the algorithm; it is a property of the **Energy Landscape**.

### 2.2 The Demon's Dilemma

To "guide" the system to the solution faster than thermal relaxation would allow, one needs a **Maxwell's Demon** (a feedback control system).

* The Demon must measure the state.
* Measurement accuracy is limited by $\Delta E \Delta t \ge \hbar$.
* As the gap $\Delta E$ closes exponentially (Lemma 2.1 in Doc A), the measurement time $\Delta t$ must diverge.

## 3. The "Free Lunch" of Quantum Computing?

Does Quantum Computing (QC) bypass this?

* QC relies on adiabatic evolution or interference.
* **Adiabatic:** Limited by the gap $\Delta(N)$ (Landau-Zener). If $\Delta \to 0$, $T_{run} \to \infty$.
* **Grover:** Quadratic speedup ($N \to \sqrt{N}$), not exponential.
* **QAA (Quantum Annealing):** Evidence suggests it effectively cools but hits the same spin-glass barriers (exponentially closing gaps).

**Conclusion:**
Quantum mechanics changes the constants, but not the scaling class. The "Thermodynamic Censorship" applies to Quantum Computers just as it applies to steam engines.
