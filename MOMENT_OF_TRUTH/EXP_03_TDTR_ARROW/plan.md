# IMPLEMENTATION PLAN: Experiment 03 - TDTR Arrow of Time (The Irreversibility Test)

**Goal:** Validate the "Theory of Dynamic Transition Regimes" (TDTR) by proving that the Arrow of Time is fundamentally an **Information Asymmetry** phenomenon.

## 1. The Experiment ("The Backward Test")

TDTR Claims: "Real physical transitions (Regime Changes) are Semigroups. They lose information. Therefore, a forward process is compressible, but a backward process looks like random noise."

We will build a tool that measures **Compression Asymmetry**:
$$ \Delta K = \text{Size}(\text{Compress}(X_{reversed})) - \text{Size}(\text{Compress}(X_{forward})) $$

* **Hypothesis A (Newtonian/Unitary):** $\Delta K \approx 0$. (Planets moving backwards make as much sense as forwards).
* **Hypothesis B (Tamesis/TDTR):** $\Delta K > 0$. (Explosions/Markets backwards make NO sense and cannot be compressed).

## 2. Technical Implementation (`exp_03_time_arrow.py`)

1. **Data Sources:**
    * **Control (Reversible):** Simple Sine Waves, Pendulum physics simulation.
    * **Test (Irreversible):** Chaotic Logistic Map ($r=4.0$), Financial Proxy (Random Walk with Drift), or Text.
2. **Compression Algorithm:** We use `gzip` (LZ77) as a proxy for Kolmogorov Complexity.
3. **Procedure:**
    * Generate time series $T$.
    * Create $T_{rev} = T[::-1]$.
    * Compress both.
    * Calculate "Arrow Score" = $(Size_{bwd} - Size_{fwd}) / Size_{fwd}$.

## 3. Verification Plan

* **Run:** `python exp_03_time_arrow.py`
* **Success Condition:**
  * **Sine Wave:** Arrow Score $\approx 0$.
  * **Chaos/Entropy:** Arrow Score SIGNIFICANTLY positive.
  * This proves we can mathematically detect "Time's Direction" without a clock, just by measuring Entropy Production.
