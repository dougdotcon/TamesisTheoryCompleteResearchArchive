# Topological Cognition Toy Model

This simulation implements the core postulates of the **Topological Theory of Cognitive States** (Paper A).
It validates the theory by demonstrating that distinct phenomenological states (Health, Anxiety, Dissociation) correspond to mathematically distinct topological regimes with unique spectral signatures.

## Regimes Simulated

1. **Critical Integration (Healthy)**
    * **Topology:** Small-World (Watts-Strogatz).
    * **Features:** Balance of local clustering and global efficiency.
    * **Spectrum:** Broad distribution, healthy $\lambda_2$ gap.

2. **Entropic Trapping (Anxiety)**
    * **Topology:** Over-clustered Lattice.
    * **Features:** High local redundancy, poor global transfer. "Rumination" loops.
    * **Spectrum:** Discrete peaks, very low $\lambda_2$ (slow diffusion).

3. **Modular Fragmentation (Dissociation)**
    * **Topology:** Relaxed Caveman (Weakly coupled communities).
    * **Features:** Extreme segregation.
    * **Spectrum:** $\lambda_2 \to 0$. Near-zero algebraic connectivity.

## How to Run

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the simulation:

    ```bash
    python structural_regimes.py
    ```

3. View results in `regimes_comparison.png`.
