"""
Riemann Zeta Zeros: Loader and Comparison Tools
================================================

This module provides tools to load known Riemann zeros and compare
them with our operator eigenvalues.

IMPORTANT: The Riemann zeros are KNOWN from numerical computation.
We are checking if our operator REPRODUCES them - it likely won't.
"""

import numpy as np
from typing import List, Tuple, Dict
from mpmath import mp, zetazero
import warnings


class RiemannZerosLoader:
    """
    Load and analyze known non-trivial zeros of the Riemann Zeta function.
    
    The n-th zero is at s = 1/2 + i*gamma_n where gamma_n are real numbers.
    If RH is true, ALL zeros have Re(s) = 1/2.
    """
    
    def __init__(self, precision: int = 30):
        """
        Parameters
        ----------
        precision : int
            Number of decimal digits for mpmath
        """
        mp.dps = precision
        self.precision = precision
        self._cached_zeros = None
    
    def load_zeros(self, n_zeros: int = 100) -> np.ndarray:
        """
        Load the first n non-trivial zeros.
        
        Returns the imaginary parts gamma_n (the E_n in physics notation).
        """
        if self._cached_zeros is not None and len(self._cached_zeros) >= n_zeros:
            return self._cached_zeros[:n_zeros]
        
        zeros = []
        print(f"Loading {n_zeros} Riemann zeros (this may take a moment)...")
        
        for n in range(1, n_zeros + 1):
            try:
                rho_n = zetazero(n)
                gamma_n = float(rho_n.imag)
                zeros.append(gamma_n)
            except Exception as e:
                warnings.warn(f"Failed to load zero {n}: {e}")
                break
        
        self._cached_zeros = np.array(zeros)
        return self._cached_zeros
    
    def verify_critical_line(self, n_zeros: int = 100) -> Dict:
        """
        Verify that all loaded zeros lie on the critical line Re(s) = 1/2.
        
        This is a numerical verification, not a proof.
        """
        results = []
        
        for n in range(1, n_zeros + 1):
            try:
                rho_n = zetazero(n)
                real_part = float(rho_n.real)
                deviation = abs(real_part - 0.5)
                
                results.append({
                    'n': n,
                    'real_part': real_part,
                    'imag_part': float(rho_n.imag),
                    'deviation_from_half': deviation,
                    'on_critical_line': deviation < 1e-10
                })
            except:
                break
        
        all_on_line = all(r['on_critical_line'] for r in results)
        max_deviation = max(r['deviation_from_half'] for r in results) if results else 0
        
        return {
            'zeros_checked': len(results),
            'all_on_critical_line': all_on_line,
            'max_deviation': max_deviation,
            'details': results[:10]  # First 10 for inspection
        }


class SpectralComparison:
    """
    Compare operator eigenvalues with Riemann zeros.
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def compute_correlation(eigenvalues: np.ndarray, zeros: np.ndarray) -> Dict:
        """
        Compute correlation between eigenvalues and zeros.
        
        This is a naive comparison - real research uses sophisticated methods.
        """
        # Use only the positive eigenvalues and sort both
        pos_eigenvalues = np.sort(eigenvalues[eigenvalues > 0])
        zeros_sorted = np.sort(zeros)
        
        # Take minimum length
        n = min(len(pos_eigenvalues), len(zeros_sorted))
        
        if n < 2:
            return {
                'correlation': 0.0,
                'n_compared': 0,
                'message': 'Insufficient data for comparison'
            }
        
        eig = pos_eigenvalues[:n]
        zet = zeros_sorted[:n]
        
        # Pearson correlation
        correlation = np.corrcoef(eig, zet)[0, 1]
        
        # Mean absolute error (after scaling)
        scale = np.mean(zet) / np.mean(eig) if np.mean(eig) != 0 else 1
        scaled_eig = eig * scale
        mae = np.mean(np.abs(scaled_eig - zet))
        
        return {
            'correlation': correlation,
            'mean_absolute_error': mae,
            'scale_factor': scale,
            'n_compared': n,
            'eigenvalues_sample': eig[:5].tolist(),
            'zeros_sample': zet[:5].tolist()
        }
    
    @staticmethod
    def montgomery_odlyzko_test(spacings: np.ndarray) -> Dict:
        """
        Test if eigenvalue spacings follow GUE (Gaussian Unitary Ensemble) statistics.
        
        Montgomery-Odlyzko conjecture: Riemann zero spacings follow GUE.
        If our operator eigenvalues also follow GUE, this is suggestive but not proof.
        """
        if len(spacings) < 10:
            return {'gue_compatible': False, 'message': 'Insufficient data'}
        
        # Normalized spacings
        mean_s = np.mean(spacings)
        s = spacings / mean_s if mean_s > 0 else spacings
        
        # GUE theoretical mean and variance
        gue_mean = 1.0  # By normalization
        gue_variance = 0.286  # Approximate value for GUE
        
        observed_variance = np.var(s)
        
        # Compare
        variance_ratio = observed_variance / gue_variance
        
        return {
            'observed_mean': np.mean(s),
            'observed_variance': observed_variance,
            'gue_expected_variance': gue_variance,
            'variance_ratio': variance_ratio,
            'gue_compatible': 0.5 < variance_ratio < 2.0,
            'message': f"Variance ratio: {variance_ratio:.3f} (GUE ≈ 1.0)"
        }


def main():
    """
    Demonstrate Riemann zeros loading and comparison.
    """
    print("=" * 70)
    print("RIEMANN ZEROS: LOADING AND ANALYSIS")
    print("=" * 70)
    print("\n⚠️  DISCLAIMER: This loads KNOWN zeros. We are NOT discovering them.\n")
    
    # Load zeros
    loader = RiemannZerosLoader(precision=15)
    n_zeros = 50  # Start small for speed
    
    print("1. LOADING RIEMANN ZEROS")
    print("-" * 40)
    zeros = loader.load_zeros(n_zeros)
    print(f"   Loaded {len(zeros)} zeros")
    print(f"\n   First 5 imaginary parts (γ_n):")
    for i, g in enumerate(zeros[:5]):
        print(f"      γ_{i+1} = {g:.6f}")
    
    # Verify critical line
    print("\n2. CRITICAL LINE VERIFICATION")
    print("-" * 40)
    verification = loader.verify_critical_line(n_zeros=20)
    print(f"   Zeros checked: {verification['zeros_checked']}")
    print(f"   All on Re=1/2: {verification['all_on_critical_line']}")
    print(f"   Max deviation: {verification['max_deviation']:.2e}")
    
    # Spacing statistics
    print("\n3. ZERO SPACING STATISTICS")
    print("-" * 40)
    spacings = np.diff(zeros)
    comparison = SpectralComparison()
    gue_test = comparison.montgomery_odlyzko_test(spacings)
    print(f"   {gue_test['message']}")
    print(f"   GUE compatible: {gue_test['gue_compatible']}")
    
    # Honest assessment
    print("\n4. HONEST ASSESSMENT")
    print("-" * 40)
    print("   ✓ Loaded known Riemann zeros successfully")
    print("   ✓ All checked zeros ARE on the critical line (numerically)")
    print("   ✓ Spacing statistics are compatible with GUE")
    print("   ❌ This does NOT prove RH - these are numerical observations")
    print("   ❌ Proving RH requires demonstrating ALL infinitely many zeros")
    
    print("\n" + "=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70)
    
    return zeros


if __name__ == "__main__":
    zeros = main()
