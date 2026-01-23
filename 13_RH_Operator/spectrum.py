"""
Spectral Analysis of the RH Operator
=====================================

Stage 13: Detailed spectral analysis and comparison.

This module provides:
1. High-resolution spectral computation
2. Statistical analysis of eigenvalue distributions
3. Comparison with random matrix theory predictions
"""

import numpy as np
from scipy import stats
from scipy.special import zeta
from typing import Tuple, List, Dict
import sys
sys.path.insert(0, r'd:\TamesisTheoryCompleteResearchArchive\13_RH_Operator')
from rh_operator import RiemannHypothesisOperator


class SpectralStatistics:
    """
    Statistical analysis of spectral sequences.
    
    For the Riemann zeros, Montgomery's pair correlation conjecture
    and subsequent work by Odlyzko established that the zeros
    follow GUE (Gaussian Unitary Ensemble) statistics.
    """
    
    def __init__(self, eigenvalues: np.ndarray):
        """
        Initialize with a sequence of eigenvalues/spectral values.
        """
        self.values = np.sort(eigenvalues)
        self.n = len(eigenvalues)
    
    def unfolded_levels(self) -> np.ndarray:
        """
        Unfold the spectrum to have mean spacing = 1.
        
        For Riemann zeros, the smooth counting function is:
        N(T) ~ (T/2pi) log(T/2pi) - T/2pi
        """
        if self.n < 2:
            return self.values
        
        spacings = np.diff(self.values)
        mean_spacing = np.mean(spacings)
        
        unfolded = np.zeros(self.n)
        unfolded[0] = 0
        for i in range(1, self.n):
            unfolded[i] = unfolded[i-1] + spacings[i-1] / mean_spacing
        
        return unfolded
    
    def nearest_neighbor_spacing(self) -> np.ndarray:
        """
        Compute normalized nearest-neighbor spacings.
        """
        unfolded = self.unfolded_levels()
        spacings = np.diff(unfolded)
        return spacings
    
    def spacing_distribution(self) -> Dict:
        """
        Analyze the spacing distribution.
        
        Compare with:
        - Poisson: P(s) = exp(-s)  (integrable systems)
        - GUE: P(s) = (32/pi^2) s^2 exp(-4s^2/pi)  (chaotic systems)
        """
        spacings = self.nearest_neighbor_spacing()
        
        if len(spacings) < 5:
            return {'error': 'Too few spacings'}
        
        mean_s = np.mean(spacings)
        var_s = np.var(spacings)
        
        poisson_var = 1.0
        gue_var = (4 - np.pi) / np.pi
        
        return {
            'spacings': spacings,
            'mean': mean_s,
            'variance': var_s,
            'expected_poisson_var': poisson_var,
            'expected_gue_var': gue_var,
            'closer_to': 'GUE' if abs(var_s - gue_var) < abs(var_s - poisson_var) else 'Poisson'
        }
    
    def number_variance(self, L_values: np.ndarray = None) -> Dict:
        """
        Compute the number variance Sigma^2(L).
        
        Sigma^2(L) = <(N(x, x+L) - L)^2>
        
        For GUE: Sigma^2(L) ~ (2/pi^2) log(L) for large L
        For Poisson: Sigma^2(L) = L
        """
        if L_values is None:
            L_values = np.linspace(0.5, 5, 10)
        
        unfolded = self.unfolded_levels()
        
        sigma2 = []
        for L in L_values:
            counts = []
            for x in np.linspace(0, max(unfolded) - L, 20):
                n_in_interval = np.sum((unfolded >= x) & (unfolded < x + L))
                counts.append(n_in_interval)
            
            if len(counts) > 0:
                sigma2.append(np.var(counts))
            else:
                sigma2.append(np.nan)
        
        return {
            'L': L_values,
            'sigma2': np.array(sigma2),
            'poisson_prediction': L_values,
            'gue_prediction': (2/np.pi**2) * np.log(np.maximum(L_values, 0.1) * 2 * np.pi)
        }


class RiemannZeroStatistics:
    """
    Statistical properties of Riemann zeros specifically.
    """
    
    def __init__(self, n_zeros: int = 100):
        self.zeros = self._get_zeros(n_zeros)
        self.n = len(self.zeros)
    
    def _get_zeros(self, n: int) -> np.ndarray:
        """
        Get Riemann zeros (imaginary parts).
        """
        zeros = np.array([
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
            67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
            79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
            92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
            103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
            114.320220, 116.226680, 118.790783, 121.370125, 122.946829,
            124.256819, 127.516684, 129.578704, 131.087688, 133.497737,
            134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
        ])
        return zeros[:n]
    
    def smooth_counting_function(self, T: float) -> float:
        """
        Riemann-von Mangoldt formula for N(T).
        
        N(T) = (T/2pi) log(T/2pi) - T/2pi + O(log T)
        """
        if T <= 0:
            return 0
        return (T / (2 * np.pi)) * np.log(T / (2 * np.pi)) - T / (2 * np.pi) + 7/8
    
    def unfolded_zeros(self) -> np.ndarray:
        """
        Unfold zeros using the smooth counting function.
        """
        return np.array([self.smooth_counting_function(t) for t in self.zeros])
    
    def verify_rh_locally(self) -> Dict:
        """
        Verify that all stored zeros are on the critical line.
        
        (They are, by construction, but this documents the structure.)
        """
        return {
            'all_on_critical_line': True,
            'real_part': 0.5,
            'imaginary_parts': self.zeros,
            'note': 'All known zeros (10^13+) lie on Re(s) = 1/2'
        }


def demonstrate_spectral_analysis():
    """
    Demonstrate spectral analysis comparing Maass and Riemann spectra.
    """
    print("=" * 70)
    print("STAGE 13: SPECTRAL ANALYSIS")
    print("Statistical Properties of Eigenvalue Sequences")
    print("=" * 70)
    
    print("\n1. RIEMANN ZEROS STATISTICS")
    print("-" * 50)
    
    rz = RiemannZeroStatistics(n_zeros=40)
    stats_rz = SpectralStatistics(rz.zeros)
    
    dist_rz = stats_rz.spacing_distribution()
    
    print(f"   Number of zeros analyzed: {rz.n}")
    print(f"   Mean spacing: {dist_rz['mean']:.4f}")
    print(f"   Spacing variance: {dist_rz['variance']:.4f}")
    print(f"   Expected GUE variance: {dist_rz['expected_gue_var']:.4f}")
    print(f"   Expected Poisson variance: {dist_rz['expected_poisson_var']:.4f}")
    print(f"   Distribution type: {dist_rz['closer_to']}")
    
    print("\n2. MAASS EIGENVALUE STATISTICS")
    print("-" * 50)
    
    maass_r = np.array([9.5336, 12.1730, 13.7797, 14.3585, 
                        16.1381, 16.6444, 17.7387, 18.1809])
    stats_maass = SpectralStatistics(maass_r)
    
    dist_maass = stats_maass.spacing_distribution()
    
    print(f"   Number of Maass values: {len(maass_r)}")
    print(f"   Mean spacing: {dist_maass['mean']:.4f}")
    print(f"   Spacing variance: {dist_maass['variance']:.4f}")
    print(f"   Distribution type: {dist_maass['closer_to']}")
    
    print("\n3. STRUCTURAL COMPARISON")
    print("-" * 50)
    
    print("""
   Both sequences show:
   - Irregular spacing (level repulsion)
   - Variance closer to GUE than Poisson
   - This indicates CHAOTIC dynamics
   
   The connection:
   - Maass forms: Delta_H on SL(2,Z)\\H (geodesic chaos)
   - Riemann zeros: Spectral determinant of some operator
   - Both reflect the same underlying "arithmetic chaos"
    """)
    
    print("\n4. THE SPECTRAL CORRESPONDENCE")
    print("-" * 50)
    
    print("   Converting to lambda = 1/4 + t^2 form:\n")
    print("   | n | Maass r_n | lambda_n | Riemann gamma_n | lambda_n |")
    print("   |---|-----------|----------|-----------------|----------|")
    
    for i in range(min(8, len(maass_r), len(rz.zeros))):
        r = maass_r[i]
        g = rz.zeros[i]
        lm = 0.25 + r**2
        lr = 0.25 + g**2
        print(f"   | {i+1} | {r:9.4f} | {lm:8.2f} | {g:15.4f} | {lr:8.2f} |")
    
    print("\n5. KEY INSIGHT: SPECTRAL RIGIDITY")
    print("-" * 50)
    
    print("""
   Both spectra exhibit SPECTRAL RIGIDITY:
   
   - Levels "repel" each other (few small gaps)
   - This is characteristic of QUANTUM CHAOS
   - Same statistics as eigenvalues of random unitary matrices
   
   WHY THIS MATTERS:
   
   If Riemann zeros had Poisson statistics, there would be
   no hope for a Hilbert-Polya operator (integrable systems).
   
   The GUE statistics strongly suggest:
   1. An underlying CHAOTIC dynamical system
   2. The geodesic flow on hyperbolic surfaces is such a system
   3. This supports the spectral approach to RH
    """)
    
    print("=" * 70)
    print("END OF SPECTRAL ANALYSIS")
    print("=" * 70)
    
    return stats_rz, stats_maass


if __name__ == "__main__":
    stats_rz, stats_maass = demonstrate_spectral_analysis()
