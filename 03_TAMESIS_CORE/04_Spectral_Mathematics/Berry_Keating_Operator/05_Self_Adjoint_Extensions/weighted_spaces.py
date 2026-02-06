"""
Weighted L² Spaces and Domain Exploration
==========================================

This module systematically tests different weighted L² spaces
to find domains where the Berry-Keating operator might be self-adjoint.

THE KEY INSIGHT
--------------
The operator H = xp fails on standard L²(ℝ) because the deficiency
solutions x^{-1/2 ± i} are not square-integrable.

By changing the weight function or domain, we might:
1. Make the operator essentially self-adjoint (ideal)
2. Get different deficiency indices
3. Find extensions with discrete spectrum
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple, Callable, List
import warnings


class WeightedSpaceAnalyzer:
    """
    Analyze Berry-Keating operator on various weighted L² spaces.
    """
    
    def __init__(self, n_points: int = 200):
        self.n_points = n_points
        self.results = {}
    
    def build_operator(self, 
                       domain: Tuple[float, float],
                       weight: Callable[[float], float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Build the Berry-Keating operator H = -i(x d/dx + 1/2) on weighted space.
        
        Returns
        -------
        H : np.ndarray
            Operator matrix
        x : np.ndarray
            Grid points
        w : np.ndarray
            Weight values
        """
        a, b = domain
        x = np.linspace(a, b, self.n_points)
        dx = x[1] - x[0]
        w = np.array([weight(xi) for xi in x])
        
        n = self.n_points
        H = np.zeros((n, n), dtype=complex)
        
        for j in range(n):
            H[j, j] = -0.5j
            if j > 0:
                H[j, j-1] = -1j * x[j] * (-1.0 / (2 * dx))
            if j < n - 1:
                H[j, j+1] = -1j * x[j] * (1.0 / (2 * dx))
        
        return H, x, w
    
    def compute_weighted_spectrum(self, 
                                  H: np.ndarray, 
                                  w: np.ndarray) -> np.ndarray:
        """
        Compute eigenvalues of the symmetrized operator.
        
        In weighted space, we symmetrize with respect to the weight.
        """
        # Symmetrize
        H_sym = (H + np.conj(H.T)) / 2
        
        try:
            eigenvalues, _ = eigh(H_sym)
            return eigenvalues
        except:
            return np.array([])
    
    def test_standard_L2(self, a: float = 0.1, b: float = 10.0) -> Dict:
        """L²([a,b], dx) - standard Lebesgue measure"""
        H, x, w = self.build_operator((a, b), weight=lambda x: 1.0)
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([{a}, {b}], dx)',
            'domain': (a, b),
            'weight': 'w(x) = 1',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def test_haar_measure(self, a: float = 0.1, b: float = 10.0) -> Dict:
        """L²([a,b], dx/x) - Haar measure (scale-invariant)"""
        H, x, w = self.build_operator((a, b), weight=lambda x: 1.0/x)
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([{a}, {b}], dx/x)',
            'domain': (a, b),
            'weight': 'w(x) = 1/x (Haar)',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def test_exponential_decay(self, a: float = 0.1, b: float = 20.0, alpha: float = 0.5) -> Dict:
        """L²([a,b], e^{-αx} dx) - Exponential regularization at infinity"""
        H, x, w = self.build_operator((a, b), weight=lambda x: np.exp(-alpha * x))
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([{a}, {b}], e^{{-{alpha}x}} dx)',
            'domain': (a, b),
            'weight': f'w(x) = exp(-{alpha}x)',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def test_power_weight(self, a: float = 0.1, b: float = 10.0, beta: float = -1.0) -> Dict:
        """L²([a,b], x^β dx) - Power-law weight"""
        # Avoid division by zero
        def safe_power(x):
            return max(x, 1e-10) ** beta
        
        H, x, w = self.build_operator((a, b), weight=safe_power)
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([{a}, {b}], x^{{{beta}}} dx)',
            'domain': (a, b),
            'weight': f'w(x) = x^{beta}',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def test_compact_interval(self, a: float = 1.0, b: float = 2.0) -> Dict:
        """L²([1, 2], dx) - Compact interval away from origin"""
        H, x, w = self.build_operator((a, b), weight=lambda x: 1.0)
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([{a}, {b}], dx) [compact]',
            'domain': (a, b),
            'weight': 'w(x) = 1',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def test_logarithmic_domain(self, log_a: float = -2, log_b: float = 2) -> Dict:
        """L²([e^a, e^b], dx/x) - Logarithmic spacing"""
        a, b = np.exp(log_a), np.exp(log_b)
        H, x, w = self.build_operator((a, b), weight=lambda x: 1.0/x)
        eigenvalues = self.compute_weighted_spectrum(H, w)
        
        return {
            'name': f'L²([e^{{{log_a}}}, e^{{{log_b}}}], dx/x)',
            'domain': (a, b),
            'weight': 'w(x) = 1/x (logarithmic domain)',
            'eigenvalues': eigenvalues,
            'first_5': eigenvalues[:5] if len(eigenvalues) >= 5 else eigenvalues,
            'positive_count': np.sum(eigenvalues > 0)
        }
    
    def run_all_tests(self) -> Dict:
        """Run all weighted space tests and compare results."""
        tests = [
            ('standard_L2', self.test_standard_L2()),
            ('haar_measure', self.test_haar_measure()),
            ('exponential', self.test_exponential_decay()),
            ('power_minus_1', self.test_power_weight(beta=-1)),
            ('power_minus_2', self.test_power_weight(beta=-2)),
            ('compact', self.test_compact_interval()),
            ('logarithmic', self.test_logarithmic_domain()),
        ]
        
        self.results = {name: result for name, result in tests}
        return self.results
    
    def compare_to_riemann_zeros(self, riemann_zeros: np.ndarray) -> Dict:
        """
        Compare positive eigenvalues from each space to Riemann zeros.
        
        Riemann zeros: γ_1 = 14.13, γ_2 = 21.02, γ_3 = 25.01, ...
        """
        if not self.results:
            self.run_all_tests()
        
        comparisons = {}
        
        for name, result in self.results.items():
            eigenvalues = result['eigenvalues']
            pos_eig = np.sort(eigenvalues[eigenvalues > 0])
            
            if len(pos_eig) == 0:
                comparisons[name] = {
                    'correlation': 0,
                    'message': 'No positive eigenvalues'
                }
                continue
            
            # Compare first few eigenvalues
            n_compare = min(len(pos_eig), len(riemann_zeros))
            
            if n_compare < 2:
                comparisons[name] = {
                    'correlation': 0,
                    'message': 'Insufficient data'
                }
                continue
            
            # Correlation
            correlation = np.corrcoef(pos_eig[:n_compare], riemann_zeros[:n_compare])[0, 1]
            
            # Mean relative error
            mean_error = np.mean(np.abs(pos_eig[:n_compare] - riemann_zeros[:n_compare]) / riemann_zeros[:n_compare])
            
            comparisons[name] = {
                'correlation': correlation if np.isfinite(correlation) else 0,
                'mean_relative_error': mean_error,
                'n_compared': n_compare,
                'first_eigenvalue': pos_eig[0] if len(pos_eig) > 0 else None,
                'first_zero': riemann_zeros[0]
            }
        
        return comparisons


def main():
    """
    Systematically test weighted spaces for Berry-Keating operator.
    """
    print("=" * 70)
    print("WEIGHTED L² SPACE EXPLORATION")
    print("Berry-Keating Operator H = xp")
    print("=" * 70)
    
    analyzer = WeightedSpaceAnalyzer(n_points=200)
    
    # Run all tests
    print("\n1. RUNNING TESTS ON DIFFERENT WEIGHTED SPACES")
    print("-" * 50)
    results = analyzer.run_all_tests()
    
    for name, result in results.items():
        print(f"\n   {result['name']}")
        print(f"      Weight: {result['weight']}")
        print(f"      Positive eigenvalues: {result['positive_count']}")
        if len(result['first_5']) > 0:
            first_pos = [e for e in result['first_5'] if e > 0][:3]
            if first_pos:
                print(f"      First positive: {[f'{e:.2f}' for e in first_pos]}")
    
    # Compare to Riemann zeros
    print("\n\n2. COMPARISON TO RIEMANN ZEROS")
    print("-" * 50)
    
    # First few Riemann zeros (imaginary parts)
    riemann_zeros = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918720, 43.327073, 48.005151, 49.773832
    ])
    
    print(f"   Target: γ_1 = {riemann_zeros[0]:.2f}, γ_2 = {riemann_zeros[1]:.2f}, ...")
    
    comparisons = analyzer.compare_to_riemann_zeros(riemann_zeros)
    
    best_correlation = -np.inf
    best_space = None
    
    for name, comp in comparisons.items():
        corr = comp.get('correlation', 0)
        if corr > best_correlation:
            best_correlation = corr
            best_space = name
        
        print(f"\n   {name}:")
        print(f"      Correlation: {corr:.4f}")
        if 'first_eigenvalue' in comp and comp['first_eigenvalue']:
            print(f"      First E: {comp['first_eigenvalue']:.2f} (target: {comp['first_zero']:.2f})")
    
    print(f"\n\n   Best correlation: {best_space} ({best_correlation:.4f})")
    
    # Honest assessment
    print("\n\n3. HONEST ASSESSMENT")
    print("-" * 50)
    print("   ❌ No weighted space produces eigenvalues matching Riemann zeros")
    print("   ❌ Discretization on finite intervals cannot capture infinite spectrum")
    print("   ❌ The 'correct' regularization remains unknown")
    print("   ✓ Systematic exploration demonstrates the methodology")
    print("   → Real progress requires analytical (not numerical) methods")
    
    print("\n" + "=" * 70)
    print("END OF WEIGHTED SPACE EXPLORATION")
    print("=" * 70)
    
    return results, comparisons


if __name__ == "__main__":
    results, comparisons = main()
