"""
Von Neumann Self-Adjoint Extension Theory
==========================================

This module implements the von Neumann theory for self-adjoint extensions
of symmetric operators. Focus: the Berry-Keating operator H = xp.

MATHEMATICAL BACKGROUND
-----------------------
For a symmetric operator H on domain D(H):

1. The adjoint H* has a larger domain D(H*)
2. Define deficiency subspaces:
   K_+ = ker(H* - iI)  (solutions to H*f = if)
   K_- = ker(H* + iI)  (solutions to H*f = -if)
   
3. Deficiency indices: n_+ = dim(K_+), n_- = dim(K_-)

4. Von Neumann Theorem:
   - H is essentially self-adjoint iff n_+ = n_- = 0
   - H has self-adjoint extensions iff n_+ = n_-
   - If n_+ = n_- = n, extensions form a U(n) family

REFERENCES
----------
- von Neumann, J. (1930) Math. Ann. 102, 49-131
- Reed & Simon, Methods of Modern Mathematical Physics, Vol. II
"""

import numpy as np
from scipy.linalg import eigh, null_space
from scipy.integrate import quad
from typing import Dict, Tuple, List, Callable, Optional
import warnings


class SymmetricOperator:
    """
    Base class for symmetric operators on L²(Ω, w(x)dx).
    
    A symmetric operator satisfies <Hf, g> = <f, Hg> for all f,g in D(H).
    """
    
    def __init__(self, 
                 domain: Tuple[float, float] = (0.1, 10.0),
                 weight: Callable[[float], float] = lambda x: 1.0,
                 n_points: int = 200):
        """
        Parameters
        ----------
        domain : Tuple[float, float]
            (a, b) interval for discretization
        weight : Callable
            Weight function w(x) for L²(Ω, w(x)dx)
        n_points : int
            Number of grid points
        """
        self.a, self.b = domain
        self.weight = weight
        self.n = n_points
        
        self.x = np.linspace(self.a, self.b, n_points)
        self.dx = self.x[1] - self.x[0]
        self.w = np.array([weight(xi) for xi in self.x])
    
    def inner_product(self, f: np.ndarray, g: np.ndarray) -> complex:
        """
        Weighted inner product: <f, g>_w = ∫ f*(x) g(x) w(x) dx
        """
        return np.trapz(np.conj(f) * g * self.w, self.x)
    
    def norm(self, f: np.ndarray) -> float:
        """||f||_w = sqrt(<f, f>_w)"""
        return np.sqrt(np.real(self.inner_product(f, f)))
    
    def is_symmetric(self, H: np.ndarray, tol: float = 1e-8) -> Dict:
        """
        Check if <Hf, g> = <f, Hg> for random test vectors.
        
        For weighted spaces, symmetry means:
        ∫ (Hf)* g w dx = ∫ f* (Hg) w dx
        
        In matrix form with weight: W^(1/2) H W^(-1/2) should be Hermitian
        """
        W_sqrt = np.diag(np.sqrt(self.w))
        W_inv_sqrt = np.diag(1.0 / np.sqrt(self.w))
        
        # Transform to weighted-symmetric form
        H_weighted = W_sqrt @ H @ W_inv_sqrt
        H_weighted_adj = np.conj(H_weighted.T)
        
        error = np.max(np.abs(H_weighted - H_weighted_adj))
        
        return {
            'is_symmetric': error < tol,
            'max_error': error,
            'tolerance': tol
        }


class BerryKeatingOperator(SymmetricOperator):
    """
    The Berry-Keating xp operator:
    
    H = (1/2)(xp + px) = -i(x d/dx + 1/2)
    
    This is the canonical candidate for Hilbert-Pólya approach to RH.
    """
    
    def __init__(self, 
                 domain: Tuple[float, float] = (0.1, 10.0),
                 weight: Callable[[float], float] = lambda x: 1.0,
                 n_points: int = 200):
        super().__init__(domain, weight, n_points)
        self.H = self._build_operator()
    
    def _build_operator(self) -> np.ndarray:
        """
        Discretize H = -i(x d/dx + 1/2)
        
        Using central differences for d/dx.
        """
        n = self.n
        H = np.zeros((n, n), dtype=complex)
        
        for j in range(n):
            x_j = self.x[j]
            
            # Diagonal: -i * (1/2)
            H[j, j] = -0.5j
            
            # Off-diagonal: -i * x * d/dx (central difference)
            if j > 0:
                H[j, j-1] = -1j * x_j * (-1.0 / (2 * self.dx))
            if j < n - 1:
                H[j, j+1] = -1j * x_j * (1.0 / (2 * self.dx))
        
        return H
    
    def compute_deficiency_indices(self) -> Dict:
        """
        Compute deficiency indices (n_+, n_-).
        
        We need to solve:
        H* f = ±i f
        
        For the xp operator, the formal solutions are:
        f_+(x) = C x^{-1/2 + i}   (for eigenvalue +i)
        f_-(x) = C x^{-1/2 - i}   (for eigenvalue -i)
        
        The deficiency index is 1 if f is in L²(domain, w dx), else 0.
        """
        results = {}
        
        # Test f_+(x) = x^{-1/2 + i}
        def f_plus(x):
            return x ** (-0.5 + 1j)
        
        def f_minus(x):
            return x ** (-0.5 - 1j)
        
        # Check L² integrability on domain
        def check_L2(f: Callable, name: str) -> Dict:
            try:
                values = np.array([f(xi) for xi in self.x])
                norm_sq = np.real(self.inner_product(values, values))
                
                is_finite = np.isfinite(norm_sq) and norm_sq < 1e10
                
                return {
                    'function': name,
                    'norm_squared': norm_sq if is_finite else float('inf'),
                    'is_L2': is_finite,
                    'sample_values': values[:5]
                }
            except:
                return {
                    'function': name,
                    'norm_squared': float('inf'),
                    'is_L2': False,
                    'error': 'Integration failed'
                }
        
        results['f_plus'] = check_L2(f_plus, 'x^{-1/2 + i}')
        results['f_minus'] = check_L2(f_minus, 'x^{-1/2 - i}')
        
        # Deficiency indices
        n_plus = 1 if results['f_plus']['is_L2'] else 0
        n_minus = 1 if results['f_minus']['is_L2'] else 0
        
        results['deficiency_indices'] = (n_plus, n_minus)
        results['has_self_adjoint_extensions'] = (n_plus == n_minus)
        results['is_essentially_self_adjoint'] = (n_plus == 0 and n_minus == 0)
        
        return results
    
    def apply_boundary_condition(self, theta: float) -> np.ndarray:
        """
        Apply U(1) boundary condition parameterized by θ.
        
        For n_+ = n_- = 1, the self-adjoint extensions are parameterized by
        e^{iθ} relating the boundary values at the two ends.
        
        Boundary condition: ψ(b) = e^{iθ} ψ(a)
        """
        H_bc = self.H.copy()
        
        # Modify boundary terms to enforce quasi-periodic BC
        # This is a simplified implementation
        phase = np.exp(1j * theta)
        
        # Connect last row to first
        H_bc[0, -1] = -1j * self.x[0] * (1.0 / (2 * self.dx)) * np.conj(phase)
        H_bc[-1, 0] = -1j * self.x[-1] * (-1.0 / (2 * self.dx)) * phase
        
        # Symmetrize
        H_sym = (H_bc + np.conj(H_bc.T)) / 2
        
        return H_sym
    
    def spectrum_vs_theta(self, n_theta: int = 50) -> Dict:
        """
        Compute spectrum for different boundary conditions θ ∈ [0, 2π].
        
        This is the key experiment: do any θ values produce spectrum
        matching Riemann zeros?
        """
        thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
        spectra = []
        
        for theta in thetas:
            H_theta = self.apply_boundary_condition(theta)
            eigenvalues, _ = eigh(H_theta)
            spectra.append(eigenvalues)
        
        spectra = np.array(spectra)
        
        return {
            'thetas': thetas,
            'spectra': spectra,
            'mean_gap': np.mean(np.diff(spectra, axis=1)),
            'eigenvalue_range': (np.min(spectra), np.max(spectra))
        }


def main():
    """
    Demonstrate von Neumann extension theory for Berry-Keating operator.
    """
    print("=" * 70)
    print("VON NEUMANN SELF-ADJOINT EXTENSION THEORY")
    print("Berry-Keating Operator H = xp")
    print("=" * 70)
    
    # Test 1: Standard L²(0.1, 10)
    print("\n1. STANDARD DOMAIN: L²([0.1, 10], dx)")
    print("-" * 50)
    
    op1 = BerryKeatingOperator(domain=(0.1, 10.0), weight=lambda x: 1.0)
    
    symmetry = op1.is_symmetric(op1.H)
    print(f"   Symmetric: {symmetry['is_symmetric']} (error: {symmetry['max_error']:.2e})")
    
    deficiency = op1.compute_deficiency_indices()
    print(f"   Deficiency indices: {deficiency['deficiency_indices']}")
    print(f"   Has extensions: {deficiency['has_self_adjoint_extensions']}")
    print(f"   Essentially self-adjoint: {deficiency['is_essentially_self_adjoint']}")
    
    # Test 2: Weighted space L²(R+, dx/x)
    print("\n2. WEIGHTED DOMAIN: L²([0.1, 10], dx/x) [Haar measure]")
    print("-" * 50)
    
    op2 = BerryKeatingOperator(
        domain=(0.1, 10.0), 
        weight=lambda x: 1.0/x,  # Haar measure
        n_points=200
    )
    
    symmetry2 = op2.is_symmetric(op2.H)
    print(f"   Symmetric: {symmetry2['is_symmetric']} (error: {symmetry2['max_error']:.2e})")
    
    deficiency2 = op2.compute_deficiency_indices()
    print(f"   Deficiency indices: {deficiency2['deficiency_indices']}")
    
    # Test 3: Boundary condition sweep
    print("\n3. BOUNDARY CONDITION SWEEP")
    print("-" * 50)
    
    theta_results = op1.spectrum_vs_theta(n_theta=20)
    print(f"   θ range: [0, 2π] in {len(theta_results['thetas'])} steps")
    print(f"   Eigenvalue range: [{theta_results['eigenvalue_range'][0]:.2f}, {theta_results['eigenvalue_range'][1]:.2f}]")
    print(f"   Mean spectral gap: {theta_results['mean_gap']:.4f}")
    
    # Compare first eigenvalues at different θ
    print("\n   First eigenvalue vs θ (sample):")
    for i in range(0, len(theta_results['thetas']), 5):
        theta = theta_results['thetas'][i]
        e1 = theta_results['spectra'][i, 0]
        print(f"      θ = {theta:.2f}: E_1 = {e1:.4f}")
    
    # Honest assessment
    print("\n4. HONEST ASSESSMENT")
    print("-" * 50)
    print("   ❌ Eigenvalues do NOT match Riemann zeros (14.13, 21.02, ...)")
    print("   ❌ Discretization on finite interval destroys essential properties")
    print("   ✓ Framework demonstrates how to search systematically")
    print("   → Next: Test more domains, weights, and regularizations")
    
    print("\n" + "=" * 70)
    print("END OF VON NEUMANN ANALYSIS")
    print("=" * 70)
    
    return deficiency, theta_results


if __name__ == "__main__":
    deficiency_results, theta_results = main()
