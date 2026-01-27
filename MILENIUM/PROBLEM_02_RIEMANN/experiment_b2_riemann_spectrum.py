
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import networkx as nx

# Configuration
N = 400
BETA_START = 0.1
BETA_END = 10.0
STEPS = 1000
SEED = 42

np.random.seed(SEED)

def generate_random_hermitian(n):
    """
    Generates a random Hermitian matrix (Initial Chaos).
    GOE/GUE mix.
    """
    A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    H = (A + A.conj().T) / 2
    return H

def unfold_spectrum(eigenvalues):
    """
    Unfolds the spectrum to have mean spacing 1.
    Uses polynomial fitting for the cumulative density function.
    """
    eigenvalues = np.sort(eigenvalues)
    n = len(eigenvalues)
    
    # Empirical CDF
    cdf = np.arange(n)
    
    # Fit a smooth curve (polynomial of degree 5)
    coeffs = np.polyfit(eigenvalues, cdf, 5)
    poly = np.poly1d(coeffs)
    
    # Map eigenvalues to unfolded values
    unfolded = poly(eigenvalues)
    return unfolded

def spacing_distribution(unfolded_eigs):
    """
    Computes nearest neighbor spacings.
    """
    spacings = np.diff(unfolded_eigs)
    # Filter out outliers (ends of spectrum)
    spacings = spacings[spacings > 0]
    spacings = spacings / np.mean(spacings)
    return spacings

def wigner_surmise(s, beta=2):
    """
    Analytical prediction for RMT spacing distribution.
    beta=1 (GOE), beta=2 (GUE).
    """
    if beta == 1:
        return (np.pi * s / 2) * np.exp(-np.pi * s**2 / 4)
    elif beta == 2:
        return (32 * s**2 / np.pi**2) * np.exp(-4 * s**2 / np.pi)
    else: # Poisson
        return np.exp(-s)

def run_simulation():
    print(f"Generating Matrix N={N}...")
    H = generate_random_hermitian(N)
    
    print("Diagonalizing...")
    eigs = la.eigvalsh(H)
    
    print("Unfolding Spectrum...")
    unfolded = unfold_spectrum(eigs)
    spacings = spacing_distribution(unfolded)
    
    # Plotting
    print("Plotting Results...")
    plt.figure(figsize=(10, 6))
    
    # Histogram of data
    count, bins, ignored = plt.hist(spacings, bins=30, density=True, alpha=0.6, color='blue', label='Simulation (N=400)')
    
    # Theoretical Curves
    s_axis = np.linspace(0, 3, 100)
    plt.plot(s_axis, wigner_surmise(s_axis, beta=2), 'r-', linewidth=2, label='GUE (Critical Class)')
    plt.plot(s_axis, wigner_surmise(s_axis, beta=0), 'g--', linewidth=2, label='Poisson (Random/Integrable)')
    
    plt.title('Spectral Statistics of Maximum Entropy Matrix (Class $C_{crit}$)')
    plt.xlabel('Normalized Spacing $s$')
    plt.ylabel('Probability Density $P(s)$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_file = 'spectral_stats_plot.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
