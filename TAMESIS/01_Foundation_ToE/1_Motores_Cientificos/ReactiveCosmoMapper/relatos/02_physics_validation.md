# Report 02: Physical Validation of the Reactive Model

**Date:** 12/29/2025
**Module:** `src/reactive_gravity.py`, `src/reactive_cosmo_mapper.py`

## Objective
To computationally validate whether **Entropic Gravity** (without Dark Matter) can reproduce the flat rotation curves observed in spiral galaxies.

## Theoretical Foundation
The model is based on the Verlinde/MOND interpolation equation, where the effective acceleration $g_{obs}$ emerges from the Newtonian acceleration $g_N$ and a fundamental acceleration scale $a_0$:

$$ g_{obs} = \frac{g_N + \sqrt{g_N^2 + 4 g_N a_0}}{2} $$

Where $a_0 \approx 1.2 \times 10^{-10} m/s^2$ (critical acceleration related to the Hubble constant).

## Testing Methodology
1. **`ReactiveGravity` Class:** Pure implementation of the vector and scalar mathematics of the theory.
2. **Unit Tests:**
    - Newtonian Regime ($g_N \gg a_0$): Confirmed relative error $< 0.1\%$.
    - Entropic Regime ($g_N \ll a_0$): Confirmed $1/r$ force behavior (constant velocity).
3. **Simulation of Galaxy NGC0024:**
    - Input Data: Baryonic Mass (Stars + Gas).
    - Comparison: Newtonian Velocity vs. Reactive Velocity vs. Observation.

## Results and Evidence
- **Generated Plot:** `NGC0024_rotation.png`
- **Analysis:**
    - The Newtonian curve (blue) decays as expected ($v \propto r^{-1/2}$), failing to explain rotation at the edges.
    - The Reactive curve (orange) **remains flat** at the edges, aligning with the observed value ($V_{flat} \approx 106 km/s$).
- **Conclusion:** The "Reactive Gravity Kernel" successfully reproduces the dynamic effects attributed to Dark Matter, utilizing only visible mass.
