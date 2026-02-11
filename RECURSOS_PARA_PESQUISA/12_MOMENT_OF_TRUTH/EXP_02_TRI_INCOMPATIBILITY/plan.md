# IMPLEMENTATION PLAN: Experiment 02 - TRI Incompatibility (The Cognitive Limit)

**Goal:** Test the "Theory of Regime Incompatibility" (TRI) by forcing a neural network to solve two topologically distinct tasks simultaneously.

## 1. The Experiment ("The Torture")

We will create a multi-headed Neural Network and force it to learn:

1. **Task A (Logical/Rigid):** The **Parity Problem (XOR)** extended to N bits. This is a "Class A" problem (Sensitive to single bit flips, requires rigid logic).
2. **Task B (Chaotic/Fluid):** **Sine Wave Regression** with noise. This is a "Class B" problem (Smooth, error-tolerant).

**Hypothesis:** By monitoring the weights, we predict that the network CANNOT solve both efficiently with a shared "monolithic" hidden layer. It must either fail or spontaneously "lobotomize" itself (disconnect weights to form two separate sub-networks).

## 2. Technical Implementation (`exp_02_tri_incompatibility.py`)

1. **Framework:** `numpy` (Manual Backprop with Adam) to avoid heavy dependencies, or `torch` if available. We will stick to `numpy` purely for zero-dependency robustness.
2. **Architecture:**
    * Input: vector of size $N$.
    * Hidden: Large dense layer.
    * Output 1: Parity bit (Sigmoid).
    * Output 2: Sine value (Linear).
3. **Training:**
    * Loss = $L_{ parity} + L_{sine}$.
    * Optimiser: Adam.
4. **Metric - The "Modularization Index":**
    * We analyze the Correlation Matrix of the hidden neurons.
    * If TRI is true, the matrix should become block-diagonal (two separate clusters).

## 3. Verification Plan

* **Run:** `python exp_02_tri_incompatibility.py`
* **Success Condition:** The script outputs a "Modularization Score" (Participation Ratio or similar).
  * If Score > Threshold AND Accuracy is High -> TRI Validated (Spontaneous Separation).
  * If Score Low AND Accuracy High -> TRI Falsified (Monolithic Solution Possible).
  * If Score Low AND Accuracy Low -> TRI Partially Validated (Monolithic Failure).
