# Header Info
>
> **Universidade Federal do Rio de Janeiro**
> **DOI:** [10.5281/zenodo.18364790](https://doi.org/10.5281/zenodo.18364790)

# The Foundations of Relational Cognition

## Chapter 2: The Physics of Information and the Saturation Postulate

### Abstract

In this chapter, we operationally define "information" as an abstract physical quantity subject to conservation and capacity laws. We introduce the Saturation Postulate, which imposes finite limits on state processing, demonstrating how attention and forgetting emerge as thermodynamic necessities rather than psychological choices.

---

### 1. Information as a Physical Quantity

Following the Golden Rule, we avoid semantic definitions of information (e.g., "meaning"). We adopt the syntactic definition of Shannon/Boltzmann, treated here as a measurable property of the system's state.

#### 1.1 Operational Definition

The information $I$ contained in a subset $X$ of the network is defined by the reduction of uncertainty about its state:

$$I(X) = H_{max}(X) - H_{obs}(X)$$

Where:

* $H_{max}(X)$ is the maximum possible entropy (theoretical channel capacity).
* $H_{obs}(X)$ is the observed entropy (remaining uncertainty).

 For a node $n$ with a discrete set of possible states with probabilities $p_i$:

$$I_n = - \sum_{i} p_i \log_2 p_i$$

This establishes that information is **physical** in the sense that it requires the distinction of distinguishable states within the network substrate.

---

### 2. The Saturation Postulate

Unlike ideal mathematical systems, real cognitive systems operate under severe physical constraints. Information does not flow freely; it encounters barriers.

#### Postulate 2: Local and Global Capacity Limit
>
> *For any node $n$, edge $e$, or subgraph $G$, there exists a finite upper bound for the amount of information that can be sustained or transmitted per unit of time.*

Formally:

$$I_{flow}(t) \le C_{max}$$

Where $C_{max}$ is the Channel Capacity.

#### 2.1 The Correlate of Energy Cost

Maintaining high-information states (low entropy) requires thermodynamic work to resist the natural tendency towards dissipation (noise).
$$E_{cost} \propto I$$
This implies that "thinking" (processing information) has an irreducible metabolic cost.

---

### 3. Immediate Consequences: The Rise of Cognitive Economy

The Saturation Postulate is not a passive limitation; it is the engine that forces the emergence of complex cognitive architectures.

#### 3.1 The Bottleneck Imperative

Given that the environment (input) almost always contains more information ($I_{env}$) than the system's capacity ($C_{sys}$):
$$I_{env} \gg C_{sys}$$

The system is mathematically *obliged* to discard information. This defines:

* **Filtering**: Passive rejection of data above cut-off frequency.
* **Compression**: Re-encoding $I_{env}$ into denser representations.

#### 3.2 The Genesis of Attention

If $I_{flow} > C_{max}$, the system would collapse (catastrophic signal loss). To prevent this, there must be a control mechanism that selects *which* information to process.
Therefore:
> **Attention is not a higher-order psychological function; it is a mechanical flow control solution to prevent thermal and informational saturation.**

#### 3.3 Perceptual Collapse

When the information input rate exceeds $C_{max}$ and compression mechanisms fail, *Perceptual Collapse* occurs: the indistinguishability of states. The system goes "blind" or enters a white noise state.

---

### Partial Verdict

So far, we have explained the need for "focus" and "memory limits" without resorting to psychology. They are inevitable consequences of the network's finitude.

### Next Steps

In the next chapter, we will explore **Topology**, demonstrating how the *shape* of the network determines the quality of processing, differentiating states like "anxiety" or "epiphany" purely through graphs.
