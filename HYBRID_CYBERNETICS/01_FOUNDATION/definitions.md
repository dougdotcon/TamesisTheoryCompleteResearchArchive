# Formal Definitions

To ensure rigor, we define all terms using standard Information Theory and Control Theory nomenclature.

---

## 1. Informational Entropy ($S$)

We use the **Shannon Entropy** definition to quantify uncertainty in the system's state space.
$$ S = - \sum p_i \log p_i $$
In the context of inference, $S$ represents the uncertainty about the "Ground Truth". High entropy implies high confusion or low precision.

## 2. Saturation ($\Sigma$)

A state of an operator $O$ where the input flux $\Phi_{in}$ exceeds the processing rate $R_{proc}$, leading to buffer overflow or thermalization.
$$ \Sigma := \frac{\Phi_{in}}{C_{max}} $$

- **Subcritical:** $\Sigma < 1$ (Stable)
- **Supercritical:** $\Sigma > 1$ (Unstable / Error Accumulating)

## 3. Stability ($\xi$)

A system is **Stable** if its error variance $\sigma^2_E$ over time $t$ remains bounded.
$$ \lim_{t \to \infty} \sigma^2_E(t) < K $$
A system where error compounds (hallucination loops) is **Unstable**.

## 4. Grounding Error ($\epsilon$)

The divergence between the operator's output $O(x)$ and the physical ground truth $y$.
$$ \epsilon = || O(x) - y || $$

## 5. The Hybrid System ($H \circ M$)

A composite system where the Machine Operator $M$ acts as a pre-filter or generator, and the Human Operator $H$ acts as a selector or verifier. The coupling is defined by the **Filter Function** $F$ that restricts the bandwidth from $M \to H$.
