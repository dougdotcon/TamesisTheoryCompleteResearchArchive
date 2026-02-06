# Header Info
>
> **Universidade Federal do Rio de Janeiro**
> **DOI:** [10.5281/zenodo.18364790](https://doi.org/10.5281/zenodo.18364790)

# The Foundations of Relational Cognition

## Chapter 1: Minimal Ontology and Network Dynamics

### Abstract

This document establishes the ontological basis for a cognitive theory grounded in dynamic network principles and information theory, free from premature psychological metaphors. We define a minimal set of primitives and the central postulate of relational dynamics.

---

### 1. Epistemological Stance: The Golden Rule

To ensure the solidity of the theoretical foundation, we adopt a strict constraint on what constitutes a valid element in the model. This is the **Foundation's Golden Rule**:

> **No concept shall be postulated unless it can be translated, consistently and without ambiguity, into:**
>
> 1. A quantifiable variable;
> 2. A defined mathematical structure; or
> 3. An observable and falsifiable consequence.

Metaphors and analogies serve exclusively as pedagogical tools *a posteriori*, never as cornerstones of the theory. Terms such as "mind", "consciousness", or "qualia" are temporarily suspended until they necessarily emerge from the dynamics of the primitives.

---

### 2. Minimal Ontology

We define the universe of discourse through the smallest necessary set of entities required to describe the system. We do not assume the existence of biological "neurons" or silicon "circuits" *a priori*; we treat information processing at its most abstract level.

#### 2.1 Ontological Primitives

The model operates on four fundamental entities:

1. **Node ($n \in N$)**: The atomic unit of locality and processing. A node is a discrete point capable of holding a value or state.
2. **Relation / Edge ($e \in E$)**: A channel of causal interaction. The existence of a directed edge $e_{ij}$ from $n_i$ to $n_j$ implies that the state of $n_i$ can influence the state of $n_j$.
3. **State ($S$)**: The instantaneous configuration of the system. Defined as the vector or set of values of all nodes in $N$ at a given moment.
4. **Discrete Time ($t$)**: The dimension of sequential evolution. The system evolves in discrete steps $t \to t+1$, where the state at $t+1$ is a function of the state and topology at $t$.

**Note:** In this ontology, there are no concepts of energy, mass, or 3D space yet. "Space" is defined purely by the topology of relations ($E$).

---

### 3. The Fundamental Postulate

Given the ontological set, we introduce the axiom that governs the system's operation.

#### Postulate 1: Relational Dynamics under Constraints
>
> *Cognitive systems are dynamic networks whose evolution is strictly governed by the redistribution of information, subject to physical constraints of capacity and processing cost.*

This postulate has two immediate implications that separate this theory from purely computational models (like infinite Turing Machines):

1. **Dynamic and Topological Nature**: Cognition is not the *output* of a function, but the *evolution* of the network configuration itself. The graph structure ($E$) can change as a function of states ($S$), allowing for plasticity.
2. **Realistic Finitude**: The clause "under constraints" imposes that information does not flow freely or instantaneously. There are bandwidth limits (edge saturation) and state limits (node saturation).

This postulate unifies, under a single definition, biological systems (brains) and artificial ones, treating them as instances of the same class of physical information processing systems.

---

### Next Steps

In the next chapter, we will formalize the definition of **Information ($I$)** within this context and introduce the **Saturation Postulate**, which mathematically prevents the "explosion" of information and gives rise to selection and attention phenomena.
