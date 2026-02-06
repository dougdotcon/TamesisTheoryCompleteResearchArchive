# IMPLEMENTATION PLAN: Experiment 02 v3 - Spatial TRI (Hemispheric Evolution)

**Goal:** Solve the "Failure to Modularize" from v1/v2 by introducing **Space**.
**Hypothesis:** If connections have a "physical length cost", Incompatible Regimes will spontaneously repel each other to opposite ends of the substrate to minimize wiring stress.

## 1. The Setup (Simulated Biology)

* **Neuron Topology:** We arrange the 128 hidden neurons on a 1D line ($x \in [0, 1]$).
* **Wiring Cost:** The cost of a connection $w_{ij}$ is proportional to $|x_i - x_j| \cdot |w_{ij}|$.
  * Short connections are cheap.
  * Long connections are expensive.

## 2. The Dynamics

We train the network on the same Logic (Parity) vs Chaos (Sine) task.

* **Loss:** $Accuracy + \lambda \sum (|w_{ij}| \cdot Distance_{ij})$
* **Prediction:**
  * The Logic task requires high precision/coupling, so it might form a tight local cluster (e.g., at $x < 0.3$).
  * The Chaos task might form its own cluster (e.g., at $x > 0.7$).
  * The middle ($x \approx 0.5$) should become a "Corpus Callosum" (sparsely connected boundary).

## 3. Implementation (`exp_02_spatial_tri.py`)

1. Matrix of Distances $D$.
2. Loss Update: Gradient Descent penalizes weights based on $D$.
3. Visualization: Plot the "Center of Mass" of the weights for Task A vs Task B.

## 4. Success Condition

* If Task A neurons separate from Task B neurons spatially (Bimodal Distribution), **TRI is SOLVED**.
* This would prove that "Brain Lateralization" is a physical inevitability of solving incompatible tasks in a spatial constraints.
