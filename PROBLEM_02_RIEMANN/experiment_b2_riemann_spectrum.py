"""
EXPERIMENT B2: Riemann Spectrum Analysis (The Critical Instant)

Goal:
1. Generate a large Finite Causal Graph (N=500).
2. Evolve it to the "Critical Instant" (Max Entropy State) via Entropic Pressure.
3. Compute the Eigenvalue Spectrum.
4. Calculate the Nearest-Neighbor Spacing Distribution (NNSD).
5. Compare with GUE (Gaussian Unitary Ensemble) statistics.

Reference:
- Montgomery (1973): Pair correlation of zeros.
- Odlyzko (1987): Numerical distribution of spacing.
- Theoretical GUE SURMISE: P(s) approx (32/pi^2) * s^2 * exp(-4*s^2/pi)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time

# Add engine path
sys.path.append(os.path.join(os.getcwd(), 'PROBLEM_01_P_VS_NP'))
from entropic_engine import FiniteCausalGraph

def gue_surmise(s):
    """Wigner Surmise for GUE (Gaussian Unitary Ensemble)."""
    # P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)
    return (32 / np.pi**2) * (s**2) * np.exp(-4 * s**2 / np.pi)

def poisson_dist(s):
    """Poisson distribution for uncorrelated levels."""
    return np.exp(-s)

def run_experiment(N=400, steps=2000, beta=10.0):
    print(f"=== EXPERIMENT B2: RIEMANN SPECTRUM (N={N}) ===")
    print(f"Goal: Confirm GUE statistics at the Critical Instant.")
    
    # 1. Initialization
    print("\n[1] Initializing Entropic Vacuum...")
    G = FiniteCausalGraph(num_nodes=N)
    # Start with a random-ish regular graph to ensure connectivity
    for i in range(N):
        G.add_edge(i, (i+1)%N)
        G.add_edge(i, (i+2)%N)
        
    s0 = G.calculate_spectral_entropy()
    print(f"    Initial Entropy: {s0:.4f}")

    # 2. Evolution (The Creation of the Operator)
    print(f"\n[2] Evolving towards Critical Instant (Entropic Pressure)...")
    t0 = time.time()
    # Batch updates for performance (check entropy every 50 mutations)
    G.apply_entropic_pressure(steps=steps, beta=beta, check_interval=50)
    dt = time.time() - t0
    
    s_final = G.calculate_spectral_entropy()
    print(f"    Final Entropy: {s_final:.4f} (Delta: {s_final - s0:.4f})")
    print(f"    Evolution Time: {dt:.2f}s")
    
    # 3. Spectral Extraction
    print("\n[3] Extracting Spectrum...")
    # We use the Hamiltonian (Laplacian + Potential) or just Adjacency?
    # Berry-Keating suggests Quantum Chaos involves the full dynamics.
    # Let's check the LAPLACIAN spectrum (common for graph statistics).
    
    # Get all eigenvalues for N=400 is feasible in standard numpy (dense)
    # Sparse solver for interior eigenvalues is tricky without good shifts.
    # We convert to dense for reliability at this scale.
    L = G.get_laplacian_matrix().toarray()
    evals = np.linalg.eigvalsh(L)
    
    print(f"    Computed {len(evals)} eigenvalues.")
    
    # 4. Unfolding & NNSD Calculation
    print("\n[4] Analyzing Spacing Distribution (NNSD)...")
    
    # Discard ground state (0) and large spectral edges
    # Focus on the "Bulk" where universality lives.
    # Typically remove top/bottom 15%
    cut = int(N * 0.15)
    bulk_evals = evals[cut:-cut]
    
    # Unfolding (normalize density to 1)
    # Simple method: Local rescaling by mean level spacing
    diffs = np.diff(bulk_evals)
    mean_spacing = np.mean(diffs)
    normalized_spacings = diffs / mean_spacing
    
    # Filter out numerical zeros (degeneracies due to symmetry remnants)
    s_values = normalized_spacings[normalized_spacings > 1e-5]
    
    print(f"    Valid Spacings: {len(s_values)}")
    print(f"    Mean Spacing (should be ~1.0): {np.mean(s_values):.4f}")
    
    # 5. Visualization & Metrics
    print("\n[5] Generating Plot...")
    
    plt.figure(figsize=(10, 6))
    
    # Histogram of simulation
    count, bins, ignored = plt.hist(s_values, bins=30, density=True, alpha=0.6, color='#6c5ce7', label='Simulated (Critical Instant)')
    
    # Theoretical Curves
    x = np.linspace(0, 3, 100)
    plt.plot(x, gue_surmise(x), 'r-', linewidth=2, label='GUE (Riemann Prediction)')
    plt.plot(x, poisson_dist(x), 'k--', linewidth=1, alpha=0.5, label='Poisson (Random/Uncorrelated)')
    
    plt.title(f"Spectral Spacing: Critical Instant (N={N})")
    plt.xlabel("Normalized Spacing s")
    plt.ylabel("P(s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = "PROBLEM_02_RIEMANN/spectral_stats_plot.png"
    plt.savefig(output_path)
    print(f"    Plot saved to: {output_path}")
    
    # Simple metric: distance to GUE mean
    # GUE mean s is 1, but let's check standard deviation or just visual fit
    # GUE typical feature: Level Repulsion (P(0) = 0). Poisson has P(0) = 1.
    
    p_near_zero = np.mean(s_values < 0.2)
    print(f"\n    P(s < 0.2) [Level Repulsion Check]: {p_near_zero:.4f}")
    if p_near_zero < 0.1:
        print("    ✅ STRONG Level Repulsion observed (Consistent with GUE).")
    else:
        print("    ⚠️ Weak Level Repulsion (Closer to Poisson?).")

if __name__ == "__main__":
    # N=300 is a good balance for quick turnaround vs statistical significance
    run_experiment(N=400, steps=2000, beta=10.0)
