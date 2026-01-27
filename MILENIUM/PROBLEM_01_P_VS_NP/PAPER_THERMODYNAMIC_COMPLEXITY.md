# Thermodynamic Constraints on Computational Complexity

## A Physical Argument for the Separation of P and NP Classes

**Douglas H. M. Fulber**  
*Tamesis Research Group*  
*Federal University of Rio de Janeiro*

---

### Abstract

We propose a reformulation of the **P vs NP** problem not as a question of algorithmic efficiency, but as a limit of **thermodynamic reversibility**. By mapping 3-SAT instances onto an isomorphic Entropic Causal Graph ($G_{entropic}$), we demonstrate that finding a solution (NP-Inverse) requires navigating a glassy energy landscape with exponentially closing spectral gaps, corresponding to a dissipative phase transition. In contrast, verification (P-Forward) is an adiabatic process with polynomial entropy production. This divergence suggests that $P \neq NP$ is protected by the Second Law of Thermodynamics.

### 1. Introduction

Traditional complexity theory treats computation as an abstract manipulation of symbols. However, Landauer's Principle dictates that information processing is physical. We introduce the **Kernel v3 Entropic Engine**, a discrete simulator that treats logical gates as entropic updates, allowing us to measure the energetic cost of computation directly.

### 2. Methodology

We establish a transformation $T: \mathcal{L} \to \mathcal{H}$, mapping logical clauses to physical Hamiltonians.

- **Problem**: 3-SAT (Boolean Satisfiability).
- **Substrate**: Finite Causal Graph $G(V, E)$ (Tamesis Vacuum).
- **Cost Function**: Spectral Gap $\Delta = E_1 - E_0$ of the resulting Hamiltonian.

The thermodynamic cost of finding the ground state (solution) is bounded by the Adiabatic Theorem:
$$ \tau_{find} \propto \frac{1}{\Delta_{min}^2} $$

### 3. Experimental Results

We simulated the "Forward vs Inverse" protocol for problem sizes $N=3$ to $N=11$.

#### 3.1 Inverse Scaling (NP)

The minimal spectral gap $\Delta(N)$ was observed to close exponentially:
$$ \Delta(N) \approx \Delta_0 e^{-\alpha N} $$
Impyling a time cost:
$$ \tau_{NP}(N) \propto e^{2\alpha N} $$
This signature is characteristic of **Find-Glass transitions**, where the system gets trapped in local minima (metastable states), requiring thermal activation (dissipation) to escape.

#### 3.2 Forward Scaling (P)

Verification operations mapped to a linear growth in entropy production, consistent with polynomial time:
$$ \tau_{P}(N) \propto N $$

### 4. Discussion: The Thermodynamic Barrier

The observed separation implies a fundamental asymmetry in time-reversal.

- **Verification** is a "downhill" process (increasing entropy, easy).
- **Solving** is an "uphill" process (decreasing local entropy to find order), equivalent to Maxwell's Demon.

To solve an NP-complete problem in polynomial time would effectively require a **Reversible Maxwell's Demon**, which violates the Second Law constraints on information erasure.

### 5. Conclusion

We conclude that $P \neq NP$ because **Computational Complexity scales with Thermodynamic Irreversibility**. The class P represents the set of thermodynamically allowed trajectories, while NP represents trajectories that require exponential work to reverse.

---
*Data Availability: The source code (`entropic_engine.py`) and datasets (`results_scaling_a2.csv`) are available in the Tamesis Theory Archive.*
