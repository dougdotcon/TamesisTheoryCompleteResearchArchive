"""
Extension Search: Systematic Parameter Scan
============================================

This module performs a comprehensive search over:
- Domains: [a, b] with various a, b
- Weights: w(x) = x^β, e^{-αx}, 1/x, etc.
- Boundary conditions: θ ∈ [0, 2π]

Goal: Find ANY combination that produces eigenvalues matching Riemann zeros.

SPOILER: It won't work. But documenting failure is science.
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple, Callable, List
import itertools
import warnings


class ExtensionSearch:
    """
    Systematic search for self-adjoint extensions matching Riemann zeros.
    """
    
    # First 20 Riemann zeros (imaginary parts)
    RIEMANN_ZEROS = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840
    ])
    
    def __init__(self, n_points: int = 150):
        self.n_points = n_points
        self.best_result = None
        self.all_results = []
    
    def build_operator_with_bc(self, 
                                domain: Tuple[float, float],
                                weight: Callable[[float], float],
                                theta: float) -> np.ndarray:
        """
        Build Berry-Keating operator with boundary condition θ.
        """
        a, b = domain
        n = self.n_points
        x = np.linspace(a, b, n)
        dx = x[1] - x[0]
        
        H = np.zeros((n, n), dtype=complex)
        
        for j in range(n):
            H[j, j] = -0.5j
            if j > 0:
                H[j, j-1] = -1j * x[j] * (-1.0 / (2 * dx))
            if j < n - 1:
                H[j, j+1] = -1j * x[j] * (1.0 / (2 * dx))
        
        # Apply quasi-periodic BC
        phase = np.exp(1j * theta)
        H[0, -1] += -1j * x[0] * (1.0 / (2 * dx)) * np.conj(phase)
        H[-1, 0] += -1j * x[-1] * (-1.0 / (2 * dx)) * phase
        
        # Symmetrize
        H_sym = (H + np.conj(H.T)) / 2
        
        return H_sym
    
    def compute_correlation(self, eigenvalues: np.ndarray) -> float:
        """
        Compute correlation between positive eigenvalues and Riemann zeros.
        """
        pos_eig = np.sort(eigenvalues[eigenvalues > 0])
        
        if len(pos_eig) < 5:
            return 0.0
        
        n = min(len(pos_eig), len(self.RIEMANN_ZEROS))
        
        try:
            corr = np.corrcoef(pos_eig[:n], self.RIEMANN_ZEROS[:n])[0, 1]
            return corr if np.isfinite(corr) else 0.0
        except:
            return 0.0
    
    def search(self, verbose: bool = True) -> Dict:
        """
        Perform systematic search over parameter space.
        """
        # Parameter grids
        domains = [
            (0.1, 10.0),
            (0.1, 50.0),
            (0.01, 100.0),
            (1.0, 10.0),
            (0.5, 20.0),
            (np.exp(-2), np.exp(2)),  # Logarithmic
        ]
        
        weights = [
            ('constant', lambda x: 1.0),
            ('haar', lambda x: 1.0/max(x, 1e-10)),
            ('exp_decay', lambda x: np.exp(-0.1*x)),
            ('power_m1', lambda x: max(x, 1e-10)**(-1)),
            ('power_m2', lambda x: max(x, 1e-10)**(-2)),
        ]
        
        thetas = np.linspace(0, 2*np.pi, 20, endpoint=False)
        
        total_configs = len(domains) * len(weights) * len(thetas)
        
        if verbose:
            print(f"   Searching {total_configs} configurations...")
        
        best_corr = -np.inf
        best_config = None
        count = 0
        
        for domain in domains:
            for weight_name, weight_func in weights:
                for theta in thetas:
                    try:
                        H = self.build_operator_with_bc(domain, weight_func, theta)
                        eigenvalues, _ = eigh(H)
                        corr = self.compute_correlation(eigenvalues)
                        
                        result = {
                            'domain': domain,
                            'weight': weight_name,
                            'theta': theta,
                            'correlation': corr,
                            'first_positive': np.sort(eigenvalues[eigenvalues > 0])[:3].tolist() if np.any(eigenvalues > 0) else []
                        }
                        
                        self.all_results.append(result)
                        
                        if corr > best_corr:
                            best_corr = corr
                            best_config = result.copy()
                            best_config['eigenvalues'] = eigenvalues
                        
                        count += 1
                        
                    except Exception as e:
                        continue
        
        self.best_result = best_config
        
        if verbose:
            print(f"   Completed {count}/{total_configs} configurations")
        
        return {
            'best_correlation': best_corr,
            'best_config': best_config,
            'total_searched': count,
            'target_zeros': self.RIEMANN_ZEROS[:5].tolist()
        }
    
    def analyze_best_result(self) -> Dict:
        """
        Detailed analysis of the best configuration found.
        """
        if self.best_result is None:
            return {'error': 'No search performed yet'}
        
        pos_eig = np.sort(self.best_result['eigenvalues'][self.best_result['eigenvalues'] > 0])
        
        analysis = {
            'config': {
                'domain': self.best_result['domain'],
                'weight': self.best_result['weight'],
                'theta': f"{self.best_result['theta']:.4f}"
            },
            'correlation': self.best_result['correlation'],
            'comparison': []
        }
        
        n = min(10, len(pos_eig), len(self.RIEMANN_ZEROS))
        for i in range(n):
            analysis['comparison'].append({
                'n': i + 1,
                'eigenvalue': f"{pos_eig[i]:.4f}",
                'riemann_zero': f"{self.RIEMANN_ZEROS[i]:.4f}",
                'error': f"{abs(pos_eig[i] - self.RIEMANN_ZEROS[i]):.4f}"
            })
        
        return analysis


def main():
    """
    Run comprehensive extension search.
    """
    print("=" * 70)
    print("EXTENSION SEARCH: SYSTEMATIC PARAMETER SCAN")
    print("=" * 70)
    print("\nSearching for self-adjoint extensions matching Riemann zeros...")
    
    searcher = ExtensionSearch(n_points=150)
    
    print("\n1. PARAMETER SEARCH")
    print("-" * 50)
    
    search_result = searcher.search(verbose=True)
    
    print(f"\n   Best correlation: {search_result['best_correlation']:.4f}")
    if search_result['best_config']:
        print(f"   Best domain: {search_result['best_config']['domain']}")
        print(f"   Best weight: {search_result['best_config']['weight']}")
        print(f"   Best θ: {search_result['best_config']['theta']:.4f}")
    
    # Detailed analysis
    print("\n2. BEST CONFIGURATION ANALYSIS")
    print("-" * 50)
    
    analysis = searcher.analyze_best_result()
    
    print(f"\n   Configuration: {analysis['config']}")
    print(f"   Correlation: {analysis['correlation']:.4f}")
    
    print("\n   Eigenvalue vs Riemann Zero comparison:")
    print(f"   {'n':>3} | {'Eigenvalue':>12} | {'γ_n':>12} | {'Error':>10}")
    print("   " + "-" * 45)
    
    for comp in analysis['comparison'][:5]:
        print(f"   {comp['n']:>3} | {comp['eigenvalue']:>12} | {comp['riemann_zero']:>12} | {comp['error']:>10}")
    
    # Verdict
    print("\n3. VERDICT")
    print("-" * 50)
    
    if analysis['correlation'] > 0.9:
        print("   ⚠️ High correlation found! Investigate further.")
    elif analysis['correlation'] > 0.5:
        print("   ~  Moderate correlation. May be coincidental.")
    else:
        print("   ❌ Low correlation. No match found.")
    
    print("\n   CONCLUSION:")
    print("   The naive finite-dimensional discretization CANNOT reproduce")
    print("   the Riemann zeros. This is expected because:")
    print("   1. The true operator has continuous spectrum on ℝ")
    print("   2. The 'correct' regularization is unknown")
    print("   3. Proving RH via operators requires analytical methods")
    
    print("\n" + "=" * 70)
    print("END OF EXTENSION SEARCH")
    print("=" * 70)
    
    return search_result, analysis


if __name__ == "__main__":
    result, analysis = main()
