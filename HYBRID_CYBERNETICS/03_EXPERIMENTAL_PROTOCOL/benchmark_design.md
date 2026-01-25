# Benchmark Design: The 3-Body Problem

To prove the **Hybrid Stability Theorem**, we must demonstrate that the coupled system outperforms the decoupled components *under saturation*.

---

## Experimental Groups

### Group A: Solo Biological (Control I)

- **Setup:** Human Expert works alone to solve the task. No AI assistance.
- **Prediction:** High Precision / Low Speed.
- **Failure Mode:** Time-out. Cannot handle the volume ($V \to \infty$).

### Group B: Solo Stochastic (Control II)

- **Setup:** LLM generates the solution fully autonomously. No Human verification.
- **Prediction:** Infinite Speed / Low Precision (Variable).
- **Failure Mode:** Hallucination. High Entropy Output.

### Group C: Coupled Hybrid (Experimental)

- **Setup:** Human uses an AI tool with a specific **Bandwidth Filter** (e.g., "AI suggests, Human verifies" or "Code Autocomplete").
- **Prediction:** Optimal trade-off.
- **Condition:** Success depends on the interface enforcing $\Phi_{in} \le C_{bio}$.

## Procedure

1. **Calibration:** Measure baseline reading speed ($C_{bio}$) of participant.
2. **Saturation:** Inject payload at $3 \times C_{bio}$.
3. **Measurement:** Record interaction logs, final output, and subjective load.
4. **Analysis:** Compute Total Variance ($\sigma^2_{total}$) and Efficiency ($\eta$) for all groups.

## The Winning Criteria

The Hybrid Hypothesis is confirmed if:
$$ \sigma^2_C \approx \sigma^2_A \quad \text{(Preserves Human Precision)} $$
$$ T_C \ll T_A \quad \text{(Approaches Machine Speed)} $$
AND
$$ T_C > T_B \quad \text{(Does not succumb to zero-cost generation)} $$

This "Goldilocks Zone" is the region of **Thermodynamic Stability**.
