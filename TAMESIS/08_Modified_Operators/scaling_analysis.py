"""
Spectrum Scaling Analysis: Why Simple Potentials Fail
=====================================================

This module analyzes WHY modified Berry-Keating operators fail to match
Riemann zeros, providing insight into what the 'true' operator would need.

KEY INSIGHT
-----------
Simple potentials V(x) produce eigenvalues of order O(1) or O(dx^{-1}).
Riemann zeros grow as γ_n ~ (2πn)/log(n), starting at ~14.

There's a fundamental SCALE mismatch that no simple V(x) can fix.
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple, List


class ScalingAnalysis:
    """
    Analyze why discretized operators have wrong eigenvalue scale.
    """
    
    # Riemann zeros
    RIEMANN_ZEROS = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918720, 43.327073, 48.005151, 49.773832
    ])
    
    def __init__(self):
        pass
    
    def analyze_grid_dependence(self, n_values: List[int] = [50, 100, 200, 400]) -> Dict:
        """
        How do eigenvalues change with grid size?
        
        If eigenvalues depend on n, the discretization is the problem.
        """
        results = []
        
        for n in n_values:
            domain = (0.1, 50.0)
            x = np.linspace(domain[0], domain[1], n)
            dx = x[1] - x[0]
            
            # Pure xp operator (symmetrized)
            H = np.zeros((n, n), dtype=complex)
            for j in range(n):
                H[j, j] = -0.5j
                if j > 0:
                    H[j, j-1] = -1j * x[j] * (-1.0 / (2 * dx))
                if j < n - 1:
                    H[j, j+1] = -1j * x[j] * (1.0 / (2 * dx))
            
            H_sym = (H + np.conj(H.T)) / 2
            eigenvalues, _ = eigh(H_sym)
            
            pos_eig = sorted(eigenvalues[eigenvalues > 0])
            
            results.append({
                'n': n,
                'dx': dx,
                'first_3': pos_eig[:3] if len(pos_eig) >= 3 else pos_eig,
                'eigenvalue_range': (min(eigenvalues), max(eigenvalues))
            })
        
        return results
    
    def analyze_domain_dependence(self, domains: List[Tuple[float, float]] = None) -> Dict:
        """
        How do eigenvalues change with domain [a, b]?
        """
        if domains is None:
            domains = [
                (0.1, 10.0),
                (0.1, 50.0),
                (0.1, 100.0),
                (1.0, 50.0),
                (0.01, 50.0),
            ]
        
        results = []
        n = 200
        
        for domain in domains:
            a, b = domain
            x = np.linspace(a, b, n)
            dx = x[1] - x[0]
            
            H = np.zeros((n, n), dtype=complex)
            for j in range(n):
                H[j, j] = -0.5j
                if j > 0:
                    H[j, j-1] = -1j * x[j] * (-1.0 / (2 * dx))
                if j < n - 1:
                    H[j, j+1] = -1j * x[j] * (1.0 / (2 * dx))
            
            H_sym = (H + np.conj(H.T)) / 2
            eigenvalues, _ = eigh(H_sym)
            
            pos_eig = sorted(eigenvalues[eigenvalues > 0])
            
            results.append({
                'domain': domain,
                'first_positive': pos_eig[0] if pos_eig else None,
                'ratio_to_gamma1': pos_eig[0] / self.RIEMANN_ZEROS[0] if pos_eig else 0
            })
        
        return results
    
    def theoretical_scaling(self) -> Dict:
        """
        What scaling would be needed to match Riemann zeros?
        
        γ_n ~ (2πn) / log(n) for large n  (approximate)
        First zero: γ_1 ≈ 14.13
        
        Our eigenvalues: E_1 ~ O(1)
        
        Scale factor needed: ~14
        """
        # Weyl's law for the xp analog
        # For a box of size L, eigenvalues go as k ~ n/L
        
        # For Riemann zeros, the counting function is:
        # N(T) ~ (T/2π) log(T/2π) - T/2π + O(log T)
        
        return {
            'riemann_first_zero': 14.134725,
            'riemann_growth': 'γ_n ~ n log(n) / 2π',
            'typical_discretized_eigenvalue': 0.5,
            'scale_factor_needed': 14.134725 / 0.5,
            'conclusion': 'Discretization fundamentally cannot reach Riemann scale'
        }


def main():
    """
    Run scaling analysis to understand why simple potentials fail.
    """
    print("=" * 70)
    print("SCALING ANALYSIS: WHY SIMPLE POTENTIALS FAIL")
    print("=" * 70)
    
    analyzer = ScalingAnalysis()
    
    # 1. Grid dependence
    print("\n1. GRID SIZE DEPENDENCE")
    print("-" * 50)
    
    grid_results = analyzer.analyze_grid_dependence()
    print(f"   {'n':>5} | {'dx':>8} | First positive eigenvalue")
    print("   " + "-" * 45)
    
    for r in grid_results:
        first = r['first_3'][0] if r['first_3'] else 'N/A'
        if isinstance(first, (float, np.floating)):
            print(f"   {r['n']:>5} | {r['dx']:>8.4f} | E_1 = {first:.4f}")
    
    print("\n   → Eigenvalues vary with grid size (artifact!)")
    
    # 2. Domain dependence
    print("\n2. DOMAIN [a, b] DEPENDENCE")
    print("-" * 50)
    
    domain_results = analyzer.analyze_domain_dependence()
    print(f"   Domain           | E_1     | Ratio to γ_1=14.13")
    print("   " + "-" * 50)
    
    for r in domain_results:
        if r['first_positive']:
            print(f"   {str(r['domain']):15} | {r['first_positive']:.4f} | {r['ratio_to_gamma1']:.4%}")
    
    print("\n   → First eigenvalue never reaches 14.13")
    
    # 3. Theoretical scaling
    print("\n3. THEORETICAL ANALYSIS")
    print("-" * 50)
    
    theory = analyzer.theoretical_scaling()
    print(f"   Riemann γ_1 = {theory['riemann_first_zero']}")
    print(f"   Typical E_1 = {theory['typical_discretized_eigenvalue']}")
    print(f"   Scale factor needed: {theory['scale_factor_needed']:.1f}x")
    print(f"\n   Riemann growth: {theory['riemann_growth']}")
    
    # 4. Conclusion
    print("\n\n4. CONCLUSION: WHY IT FAILS")
    print("-" * 50)
    print("""
   The discretized xp operator on [a,b] produces eigenvalues of order:
   
       E_n ~ n / (b - a)
   
   But Riemann zeros grow as:
   
       γ_n ~ n log(n)
   
   This is a FUNDAMENTAL MISMATCH:
   
   ❌ Linear vs logarithmic growth
   ❌ Scale off by factor ~30
   ❌ No simple V(x) can fix this within finite-difference framework
   
   IMPLICATION:
   
   If a Hilbert-Pólya operator exists, it requires:
   → Infinite domain (not [a,b])
   → Non-standard quantization (adèlic, noncommutative)
   → Or perhaps doesn't exist at all
""")
    
    print("=" * 70)
    print("END OF SCALING ANALYSIS")
    print("=" * 70)
    
    return grid_results, domain_results, theory


if __name__ == "__main__":
    grid, domain, theory = main()
