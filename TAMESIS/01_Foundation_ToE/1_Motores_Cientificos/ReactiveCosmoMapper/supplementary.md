# Supplementary Material: The Reactive Universe

## S1. Code-First Physics Methodology
This project adopts a "Code-First" approach to theoretical physics. Instead of deriving abstract equations and fitting parameters to data later, we build the physical laws into a computational kernel and test them against raw observational datasets.

**Core Principles:**
1.  **No Free Parameters:** The critical acceleration $a_0$ is not a fit, but an emergent scale derived from $H(z)$.
2.  **Baryons Only:** No invisible mass components are initialized; gravity is purely a response to information density.
3.  **Falsifiability:** The code must produce testable predictions (rotation curves, void graphs) that can be directly compared to standard catalogs (SDSS, Planck).

## S2. Data Sources & Ingestion
The simulation relies on high-fidelity open data:

*   **Galactic Dynamics:** [SPARC Database](http://astroweb.cwru.edu/SPARC/) (Lelli et al., 2016).
    *   Used for Rotation Curve validation (e.g., NGC 0024).
*   **Large Scale Structure:** [SDSS Data Release 17](https://www.sdss.org/dr17/).
    *   Sample of 50,000 galaxies ($z < 0.1$) for correlation function $\xi(r)$.
*   **Cosmic Microwave Background:** [Planck 2018 Legacy Archive](https://pla.esac.esa.int/).
    *   Power Spectrum ($C_l$) benchmarks used for the 3rd Peak validation.

## S3. Implementation Details

### S3.1 The Reactive Kernel (`reactive_gravity.py`)
The engine uses a vectorized Python implementation to calculate the entropic acceleration boost. The core logic replaces the Poisson equation with a nonlinearity triggered by the acceleration scale $a_0$.

```python
def calculate_effective_acceleration(self, M_baryon, r):
    g_N = (self.G * M_baryon) / (r**2)
    # Verlinde's Interpolation Function
    # In the deep MOND limit (g_N << a0), g_eff -> sqrt(g_N * a0)
    g_eff = g_N + np.sqrt(g_N * self.a0) 
    return g_eff
```

### S3.2 Simulation Optimizations
*   **Vectorization:** Numpy broadcasting is used for N-body interactions ($\mathcal{O}(N^2)$) to avoid Python loops, essential for the Merger and Satellite simulations.
*   **Wigner-Seitz Cells:** For the Void Scanner (`void_scanner.py`), we implement a specialized spatial search algorithm adapted for non-uniform galaxy distributions.

## S4. Reproducibility & Hardware
*   **Minimum Specs:** 8GB RAM, Quad-Core CPU (for Galactic/Satellite simulations).
*   **Recommended:** 16GB+ RAM (for Cosmic Web/Void Scanner).
*   **Environment:** Python 3.10+ with `numpy`, `scipy`, `pandas`, `astropy`, `matplotlib`.

## S5. License & Citation
This code is released under the **MIT License**.
**Cite as:**
> Fulber, D. H. M. (2025). *ReactiveCosmoMapper: A Computational Solution to the Dark Sector* [Source Code]. Zenodo. https://doi.org/10.5281/zenodo.18090702

**See also:**
> Fulber, D. (2025). *Information as Geometry: A Computational Verification of Entropic Gravity*. Submitted to Class. Quant. Grav.
