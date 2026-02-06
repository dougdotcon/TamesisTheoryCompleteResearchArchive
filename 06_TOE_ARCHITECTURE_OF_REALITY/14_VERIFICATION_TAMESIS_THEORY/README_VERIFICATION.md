# Tamesis Verification Engine: GRB 090510

This folder contains the **Empirical Validation Suite** for the Tamesis Theory. It simulates the predicted time-of-flight delays for high-energy photons caused by the discrete grain of the Tamesis Kernel.

## 1. The Physics (Tamesis Dispersion)

Tamesis predicts that the discrete graph structure acts as a refractive medium for high-energy particles. The velocity of a photon is energy-dependent:

$$ v(E) \approx c \left( 1 - \xi \frac{E}{E_{Pl}} \right) $$

For a source at distance $D$, this accumulates into a time lag ($\Delta t$):

$$ \Delta t \approx \xi \frac{E_{high} - E_{low}}{E_{Pl}} \frac{D}{c} $$

## 2. Using the Engine

The script `grb_validation_engine.py` performs a multi-phase validation:

1. **Linear Check:** Tests the naive Tamesis prediction ($\xi=1$).
2. **Constraint Search:** Calculates the precise **Fermi Limit** for the coupling constant $\xi$.
3. **Quadratic Check:** Simulates second-order suppression ($E^2/E_{Pl}^2$).

### Running the Test

```bash
python grb_validation_engine.py
```

### Output

* **Console:** Reports the **Tamesis Bound** ($xi < \dots$) and the graph smoothness efficiency.
* **Plot:** Generates `tamesis_constraints.png` showing the forbidden lag region and parameter space exclusion.

## 3. Results & Empirical Bounds

Based on simulation of **GRB 090510** ($z=0.903, E_{high}=30$ GeV):

* **Naive Linear Prediction ($\xi=1$):** $\Delta t \approx 455 \text{ ms}$ (Refuted by Fermi).
* **Experimental Bound:** **$\xi < 0.065$** (The Tamesis Bound).
* **Graph Smoothness:** > 93.4% Efficient (The "Anti-Aliasing" factor).

**Conclusion:**
The "null result" from Fermi-LAT does not kill Tamesis; it refines it. It proves that the informational graph of the Kernel is either significantly smoother than the Planck length suggests ($\xi \ll 1$) or that the dispersion follows a **Quadratic Suppression** model ($\Delta t \approx 10^{-15} \text{ ms}$), which remains consistent with all current observations.
