# The Hybrid Stability Theorem

**Theorem 1 (Hybrid Stability):**
A hybrid cognitive system $\Psi = \mathcal{H} \circ \mathcal{F} \circ \mathcal{M}$ is thermodynamically stable (bounded error variance) *if and only if* the Filter Function $\mathcal{F}$ enforces the Bandwidth Constraint:
$$ \text{Rate}(\mathcal{F}) \le C_H $$
where $C_H$ is the channel capacity of the Human Operator.

**Proof Sketch:**

1. **Assumption:** $\mathcal{H}$ is the only operator capable of Grounding (reducing variance to 0).
2. **Assumption:** $\mathcal{H}$ loses grounding capability if saturated ($Rate > C_H$).
3. **Case A (Unfiltered):** If $\mathcal{F}$ is Identity, the high flux of $\mathcal{M}$ saturates $\mathcal{H}$. $\mathcal{H}$ becomes a random selector. Error Variance diverges. (System Unstable).
4. **Case B (Filtered):** If $Rate \le C_H$, $\mathcal{H}$ maintains grounding capability. $\mathcal{H}$ acts as a "Maxwell's Demon", selectively decreasing the entropy of $\mathcal{M}$'s output.
5. **Conclusion:** The total system entropy $S$ decreases over time only in Case B. $\blacksquare$

---

## Implications

1. **AI Acceleration is Dangerous:** Increasing the speed of AI (`Rate(M)`) without improving the Filter (`F`) paradoxically *destabilizes* the total system by flooding the verifier.
2. **The "Human-in-the-loop" Bottleneck:** The human is not a bug; the human is the *stabilizer*. The bottleneck is the feature that prevents thermalization.
