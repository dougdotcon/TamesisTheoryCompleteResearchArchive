# Report 08: Cosmic Voids Statistics
**Date:** December 2025
**Module:** `src/void_scanner.py`
**Validation Artifact:** `Validation/void_size_distribution.png`

## Objectives
To analyze the topology of the under-dense regions (Voids) in the Reactive Universe and compare them with the predictions of Cold Dark Matter.

## Methodology
We implemented a **Stochastic Spherical Underdensity Scanner**:
1.  Launched 100,000 random probe seeds into the simulation volume.
2.  Inflated spheres until they encountered the first galaxy.
3.  Cataloged the Maximal Void Radii.

## Results
*   **Mean Void Radius:** $\sim 740$ Mpc.
*   **Max Void Radius:** $\sim 3095$ Mpc.
*   **Topology:** The voids are significantly "cleaner" and larger than typical CDM predictions.
*   **Interpretation:** In CDM, "sticky" Dark Matter leaves debris in voids. In Entropic Gravity, the specific force law acts effectively as a repulsive pressure in low-density regions (where $a \ll a_0$), clearing them out efficiently. This aligns with the "Peebles Tension" regarding the emptiness of observed voids.
