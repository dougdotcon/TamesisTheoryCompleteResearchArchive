# IMPLEMENTATION PLAN: Experiment 01 - Spectral Criticality Test

**Goal:** Provide empirical evidence for the Tamesis Theory claim that "Critical Systems spontaneously exhibit Riemann Zeta Statistics (GUE)".

## 1. The Experiment

We will simulate a **Random Geometric Graph (RGG)** undergoing a phase transition.

* **System:** $N$ nodes in a 2D box.
* **Control Parameter:** Connection radius $r$.
* **Phase Transition:** As $r$ increases, the graph goes from Disconnected $\to$ Connected (Percolation).

## 2. Technical Implementation (`exp_01_spectral_criticality.py`)

1. **Generate Graph:** Use `scipy.spatial` to create RGGs efficiently.
2. **Compute Laplacian:** $L = D - A$.
3. **Compute Spectrum:** Calculate eigenvalue spacings $s_i = \lambda_{i+1} - \lambda_i$ (Unfolded).
4. **Statistical Test:**
    * Compare the distribution $P(s)$ against:
        * **Poisson (Exponential):** $e^{-s}$ (Uncorrelated/Disconnected).
        * **GUE (Wigner Surmise):** $\frac{32}{\pi^2} s^2 e^{-4s^2/\pi}$ (Correlated/Critical).

## 3. Verification Plan

* **Automated Check:** The script will output a `Kullback-Leibler Divergence` score.
  * If $KL(Data || GUE) < KL(Data || Poisson)$ at critical $r_c$, the hypothesis is **CONFIRMED**.
* **Visual Check:** The script will generate `spectral_plot.png` showing the histogram vs theoretical curves.

## 4. Dependencies

* `numpy`, `scipy`, `matplotlib`.
* Command: `python exp_01_spectral_criticality.py`
