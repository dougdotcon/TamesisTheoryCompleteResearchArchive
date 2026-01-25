# Header Info
>
> **Universidade Federal do Rio de Janeiro**
> **DOI:** [10.5281/zenodo.18364790](https://doi.org/10.5281/zenodo.18364790)
> **Target Journal/Repo:** arXiv (q-bio.NC / cs.NI)

# Topological Theory of Cognitive States: Spectral Signatures of Information Processing Regimes

**Douglas H. M. Fulber**
*Universidade Federal do Rio de Janeiro*

---

## Abstract

We propose a formal theoretical framework where "cognitive states" are defined not by their semantic content, but by the topological regime of the underlying dynamic network. Building on the **Information Saturation Postulate** ($I_{flow} \le C_{max}$), we demonstrate that attention and functional segregation are thermodynamic necessities for systems operating near capacity. By applying **Spectral Graph Theory**, we map phenomenological states to specific eigenvalue distributions of the network Laplacian. We identify three distinct topological regimes: (1) **Critical Integration** (Healthy/Scale-Free), (2) **Entropic Trapping** (Over-regular/Anxiety), and (3) **Modular Fragmentation** (Disconnected/Dissociation). This model offers a physics-based taxonomy for cognitive dynamics, replacing descriptive psychological labels with rigorous topological metrics.

---

## 1. Introduction

The quantitative description of cognitive states remains an open problem in complex systems science. While neuroscience has successfully mapped local functions to specific anatomical regions, the global dynamical regimes that characterize the *quality* of processing (e.g., focused attention, mind-wandering, hyper-vigilance) lack a unified mathematical definition.

Current approaches often rely on psychological descriptors ("anxious", "distracted") that are semantically rich but mathematically opaque. In this work, we propose a shift from semantic description to **topological characterization**. We hypothesize that what are perceived as macro-states of cognition are, in reality, phase states of the information flow on a dynamic graph.

We present a minimal model based on two pillars:

1. **Relational Ontology:** The system is defined by its edges (causal relations), not just its nodes.
2. **Thermodynamic Boundedness:** Information processing is constrained by finite channel capacity and metabolic cost.

## 2. Formal Framework

### 2.1 Primitives and Dynamics

We define a cognitive system as a time-varying directed graph $G(t) = (V, E(t))$, where $V = \{n_1, ..., n_N\}$ represents the set of processing units (nodes), and $E(t)$ represents the set of weighted edges $w_{ij}(t)$ representing causal influence.

The state of the system $S(t)$ evolves according to a dual dynamic:

1. **Flow Dynamics:** Information propagates on the fixed topology.
2. **Topological Plasticity:** The topology $E(t)$ updates based on the history of the flow (Hysteresis/Hebbian learning).

### 2.2 The Saturation Constraint

A fundamental axiom of our framework is that no physical edge has infinite bandwidth. We define the **Information Capacity** $C_{ij}$ of an edge as its Shannon capacity. The **Saturation Postulate** states:

$$ I_{flow}(e_{ij}) \le C_{ij} $$

where $I_{flow}$ is the mutual information between the source and target nodes.

**Consequence (The Bottleneck Theorem):**
In an environment where the input information density $I_{env} \gg \sum C_{input}$, the system must implement a selection mechanism $\sigma$ (Attention) such that:
$$ \sigma(I_{env}) \subset I_{env} \quad \text{s.t.} \quad |\sigma(I_{env})| \le C_{system} $$

Failure to select leads to **Perceptual Collapse** (thermalization of the signal), where $H_{obs} \to H_{max}$ (white noise).

## 3. Topological Regimes

We identify three primary classes of network configurations that correspond to distinct information processing capabilities.

### 3.1 Regime I: Critical Integration ("Healthy")

This regime is characterized by a **Small-World** topology (Watts-Strogatz), balancing local clustering $C$ with short average path length $L$.

* **Metric Signature:** High $\lambda_2$ (Algebraic Connectivity), Power-law degree distribution $P(k) \sim k^{-\gamma}$.
* **Functional Implication:** The system resides at the "Edge of Chaos", maximizing the dynamic range and susceptibility to external inputs without losing coherence.

### 3.2 Regime II: Entropic Trapping ("Overfitting")

This regime emerges when the system minimizes energy expenditure by reinforcing existing loops, leading to excessive local clustering.

* **Metric Signature:** $C \to 1$, $L \gg L_{rand}$, low Spectral Gap.
* **Topological Feature:** The network forms deep **Attractor Basins**. Information becomes trapped in reverberating subgraphs (loops).
* **Cognitive Correlate:** This topology corresponds to states of rigidity, rumination, or "anxiety", where the system cannot easily switch contexts due to high energy barriers.

### 3.3 Regime III: Modular Fragmentation ("Underfitting")

This regime is characterized by a breakdown of the "Giant Component". The global graph effectively splits into weakly coupled subgraphs $G_1, G_2, ...$.

* **Metric Signature:** Modularity $Q \to 1$, $\lambda_2 \to 0$.
* **Topological Feature:** Failure of global integration. Signals in $G_1$ have zero causal efficacy on $G_2$.
* **Cognitive Correlate:** This corresponds to dissociative states or dreaming, where sensory processing is decoupled from executive narrative.

## 4. Spectral Analysis

To move beyond static metrics, we employ **Spectral Graph Theory**. The eigenvalues of the Laplacian matrix $L = D - A$ provide a frequency-domain analysis of the graph's structure.

### 4.1 The Spectral Spectrum as State Signature

The set of eigenvalues $0 = \lambda_1 \le \lambda_2 \le ... \le \lambda_N$ defines the "sound" of the network. We propose that the **Spectral Distribution** is the rigorous signature of the cognitive state.

* **Low Eigenvalues (Global Modes):** Correspond to slow, integrative processes (e.g., Delta/Theta bands).
* **High Eigenvalues (Local Modes):** Correspond to fast, localized processing (e.g., Gamma bands).

### 4.2 Isomorphism to Neural Oscillations

While this model is abstract, there is a formal isomorphism between the Laplacian eigenvectors and the standing waves of neural activity. A change in topology (e.g., pruning edges) directly shifts the eigenvalue spectrum, altering the "resonant frequencies" of the mind.

## 5. Discussion

We have outlined a **Topological Theory of Cognitive States** that operationalizes vague psychological concepts into concrete graph-theoretical metrics.

* **Anxiety** is re-framed as **Topological Overfitting** (High $C$, Deep Attractors).
* **Dissociation** is re-framed as **Spectral Fragmentation** ($\lambda_2 \to 0$).

This framework suggests that clinical interventions (pharmacological or electromagnetic) theoretically act by modifying the **effective topology** of the network, pushing the system from a pathological regime back towards the Critical Regime.

Future work will involve simulating these regimes using standard coupled-oscillator models (Kuramoto) on representative graph topologies to quantify the hysteresis effects and transition costs.

---

## References

1. Shannon, C. E. (1948). A Mathematical Theory of Communication.
2. Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks.
3. Chung, F. R. K. (1997). Spectral Graph Theory.
4. Tononi, G. (2004). An information integration theory of consciousness.
5. Fulber, D. H. M. (2026). *The Foundations of Relational Cognition* (Series).
