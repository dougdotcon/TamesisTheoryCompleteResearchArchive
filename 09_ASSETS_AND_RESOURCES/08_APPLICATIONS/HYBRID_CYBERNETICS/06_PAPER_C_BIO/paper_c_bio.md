# Empirical and Neuroinformational Bounds on Human Verification Bandwidth: Defining $C_{bio}$

**A Foundational Parametrization for Hybrid Cybernetics**

**Douglas H. M. Fulber**
*Institute for Hybrid Cybernetics*

---

## Abstract

The **Theory of Hybrid Stability** relies on a critical parameter: the biological channel capacity for semantic verification, denoted as $C_{bio}$. While literature often cites reading speeds of 200-400 wpm (~50 bits/s), verification requires active error detection, which imposes a higher cognitive load. This paper synthesizes evidence from cognitive psychology (Miller, Sweller), information theory (Pierce, Shannon), and neurophysiology to derive a rigorous bound for $C_{bio}$. We distinguish between **Passive Reception Flux** ($ \Phi_{Rx} $) and **Active Verification Flux** ($ \Phi_{Ver} $), demonstrating that for high-entropy tasks (e.g., code review, hallucination detection), the effective capacity drops to the range $C_{bio} \in [10^1, 20]$ bits/s. This finding reinforces the necessity of "Thermodynamic Throttling" in Human-AI interfaces.

---

## 1. Introduction: The "Human Bottleneck"

In Hybrid Cybernetics, the stability of a coupled system $\mathcal{H} \circ \mathcal{M}$ is conditional on the Bandwidth Constraint:
$$ \mathcal{F}(\Phi_{out}) \le C_{bio} $$
If $C_{bio}$ is overestimated, the filter $\mathcal{F}$ will fail, leading to saturation and error divergence. Therefore, establishing a physically defensible value for $C_{bio}$ is not a detail, but a safety-critical requirement.

## 2. Theoretical Bounds

### 2.1 The Shannon Limit of Language

Shannon (1951) estimated the entropy of English text $H_{eng}$ to be $\approx 1.5$ bits/letter.
For a reading speed of 250 words/minute ($\approx 20$ letters/s):
$$ R_{shannon} \approx 20 \times 1.5 = 30 \text{ bits/s} $$
This represents the *maximum reception rate* for native text.

### 2.2 The Psychometric Limit (Hick-Hyman Law)

Verification is a decision process. The time $T$ to verify a bit of information follows the Hick-Hyman Law:
$$ T = b \cdot \log_2(n+1) $$
For binary verification (True/False) per semantic unit, the processing cost is non-negligible.

## 3. Empirical Evidence

### 3.1 Code Review Studies

Studies on software engineering (e.g., Cohen et al.) show that code review effectiveness drops precipitously after **400 LOC/hour**.
Assuming 1 line $\approx$ 50 bits of entropy:
$$ R_{review} = \frac{400 \times 50}{3600} \approx 5.5 \text{ bits/s} $$
This suggests active verification is an order of magnitude slower than passive reading.

### 3.2 The "Invisible Gorilla" Effect (Inattentional Blindness)

When flux increases ($\Phi \gg 10$ bits/s), the brain engages heuristic filters (System 1). In this mode, "hallucinations" (plausible but false statements) become invisible because they fit the heuristic pattern.
**Correction Cost:** Detecting a semantic error requires switching to System 2 (Analytical), which has a metabolic cost and requires $T_{switch} \approx 200$ms.

## 4. Derived Bounds for $C_{bio}$

We propose a tri-level classification for $C_{bio}$:

| Regime | Flux ($\Phi$) | Mechanism | Reliability |
| :--- | :--- | :--- | :--- |
| **Scanning** | $\sim 50$ bits/s | Pattern Matching | Low ($\sigma^2_{high}$) |
| **Reading** | $\sim 30$ bits/s | Semantic Reconstruction | Medium |
| **Verification** | $\sim 5-10$ bits/s | Logical Falsification | High ($\sigma^2 \to 0$) |

## 5. Implications for AI Interface Design

The naive assumption that "Humans can read AI output at 300 wpm" is dangerous.
For **Safety-Critical Tasks**, the interface must throttle the AI output to the **Verification Bandwidth** (~10 bits/s), not the Reading Bandwidth.
This implies that **High-Speed Chat Interfaces** are structurally unsafe for debugging or fact-checking.

## 6. Conclusion

We define the operational parameter $C_{bio}$ for Hybrid Cybernetics as:
$$ C_{bio}^{safety} \approx 10 \text{ bits/s} $$
Any system pushing flux beyond this limit without algorithmic pre-filtering is thermodynamically unstable.

## References

1. Shannon, C. E. (1951). *Prediction and Entropy of Printed English*.
2. Miller, G. A. (1956). *The Magical Number Seven, Plus or Minus Two*.
3. Sweller, J. (1988). *Cognitive Load During Problem Solving*.
4. Kahneman, D. (2011). *Thinking, Fast and Slow*.
