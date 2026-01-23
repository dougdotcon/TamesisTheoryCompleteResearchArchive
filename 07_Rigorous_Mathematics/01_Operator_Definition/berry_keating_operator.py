"""
Berry-Keating Operator Implementation
=====================================

This module implements the Berry-Keating xp-Hamiltonian:

    H = (1/2)(xp + px) = -iℏ(x d/dx + 1/2)

This operator is central to the Hilbert-Pólya approach to RH.

IMPORTANT: This is a NUMERICAL EXPLORATION, not a proof.
The operator requires regularization to be self-adjoint.

References:
- Berry, M. V., & Keating, J. P. (1999). "The Riemann zeros and eigenvalue asymptotics"
- Connes, A. (1999). "Trace formula in noncommutative geometry and the zeros of the Riemann zeta function"
"""

import numpy as np
from scipy.linalg import eigh, eigvals
from typing import Tuple, Dict
import warnings


class BerryKeatingOperator:
    """
    Discretized Berry-Keating Hamiltonian on a finite interval.
    
    The continuous operator H = -i(x d/dx + 1/2) is discretized using
    finite differences on the interval [a, b].
    
    Boundary conditions are critical for self-adjointness.
    """
    
    def __init__(self, n_points: int = 100, x_min: float = 0.1, x_max: float = 10.0):
        """
        Parameters
        ----------
        n_points : int
            Number of grid points for discretization
        x_min : float
            Left boundary (must be > 0 to avoid singularity)
        x_max : float
            Right boundary
        """
        self.n = n_points
        self.x_min = x_min
        self.x_max = x_max
        
        # Grid
        self.x = np.linspace(x_min, x_max, n_points)
        self.dx = self.x[1] - self.x[0]
        
        # Build operator matrix
        self.H = self._build_hamiltonian()
        
    def _build_hamiltonian(self) -> np.ndarray:
        """
        Construct the matrix representation of H = -i(x d/dx + 1/2)
        
        Using central differences: d/dx ≈ (f(x+h) - f(x-h)) / (2h)
        """
        n = self.n
        H = np.zeros((n, n), dtype=complex)
        
        for i in range(n):
            x_i = self.x[i]
            
            # Diagonal: -i * (1/2) = -i/2
            H[i, i] = -0.5j
            
            # Off-diagonal: -i * x * d/dx using central difference
            if i > 0:
                H[i, i-1] = -1j * x_i * (-1 / (2 * self.dx))
            if i < n - 1:
                H[i, i+1] = -1j * x_i * (1 / (2 * self.dx))
        
        return H
    
    def symmetrize(self) -> np.ndarray:
        """
        Force Hermitian symmetry: H_sym = (H + H†) / 2
        
        This is a regularization that ensures real eigenvalues,
        but may not preserve the physics of the original operator.
        """
        H_symmetric = (self.H + self.H.conj().T) / 2
        return H_symmetric
    
    def verify_self_adjoint(self, tolerance: float = 1e-10) -> Dict:
        """
        Check if H = H† (Hermitian/self-adjoint condition)
        
        For finite matrices, self-adjoint = Hermitian = H†.
        Returns detailed verification results.
        """
        H_dagger = self.H.conj().T
        difference = self.H - H_dagger
        max_error = np.max(np.abs(difference))
        
        is_hermitian = max_error < tolerance
        
        return {
            'is_hermitian': is_hermitian,
            'max_error': max_error,
            'tolerance': tolerance,
            'message': f"Operator {'IS' if is_hermitian else 'IS NOT'} Hermitian (error: {max_error:.2e})"
        }
    
    def eigenspectrum(self, use_symmetric: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenvalues and eigenvectors.
        
        Parameters
        ----------
        use_symmetric : bool
            If True, use symmetrized operator (guarantees real eigenvalues)
            If False, use original operator (may have complex eigenvalues)
        
        Returns
        -------
        eigenvalues : np.ndarray
            Sorted eigenvalues (real if symmetric)
        eigenvectors : np.ndarray
            Corresponding eigenvectors
        """
        if use_symmetric:
            H = self.symmetrize()
            eigenvalues, eigenvectors = eigh(H)
        else:
            eigenvalues = eigvals(self.H)
            eigenvectors = None
            
        return eigenvalues, eigenvectors
    
    def eigenvalue_spacing_statistics(self, eigenvalues: np.ndarray) -> Dict:
        """
        Compute level spacing statistics.
        
        If eigenvalues follow RMT (Random Matrix Theory) GUE statistics,
        this suggests quantum chaos and potential connection to Riemann zeros.
        """
        # Sort and compute spacings
        sorted_eig = np.sort(np.real(eigenvalues))
        spacings = np.diff(sorted_eig)
        
        # Normalize by mean spacing
        mean_spacing = np.mean(spacings)
        normalized_spacings = spacings / mean_spacing if mean_spacing > 0 else spacings
        
        # Compute statistics
        return {
            'mean_spacing': mean_spacing,
            'std_spacing': np.std(normalized_spacings),
            'min_spacing': np.min(spacings),
            'max_spacing': np.max(spacings),
            'normalized_spacings': normalized_spacings
        }


def main():
    """
    Demonstration of Berry-Keating operator analysis.
    """
    print("=" * 70)
    print("BERRY-KEATING OPERATOR: NUMERICAL EXPLORATION")
    print("=" * 70)
    print("\n⚠️  DISCLAIMER: This is numerical exploration, NOT a proof of RH.\n")
    
    # Create operator
    n_points = 200
    op = BerryKeatingOperator(n_points=n_points, x_min=0.1, x_max=50.0)
    
    # 1. Verify self-adjointness
    print("1. SELF-ADJOINTNESS TEST")
    print("-" * 40)
    result = op.verify_self_adjoint()
    print(f"   {result['message']}")
    
    if not result['is_hermitian']:
        print("   → Original Berry-Keating operator is NOT Hermitian.")
        print("   → This is expected: the operator needs regularization.")
        print("   → Using symmetrized version for eigenvalue computation.\n")
    
    # 2. Compute eigenvalues
    print("2. EIGENVALUE COMPUTATION")
    print("-" * 40)
    eigenvalues, _ = op.eigenspectrum(use_symmetric=True)
    
    print(f"   Grid points: {n_points}")
    print(f"   Domain: [{op.x_min}, {op.x_max}]")
    print(f"   Number of eigenvalues: {len(eigenvalues)}")
    print(f"\n   First 10 eigenvalues:")
    for i, e in enumerate(eigenvalues[:10]):
        print(f"      E_{i+1} = {e:.6f}")
    
    # 3. Spacing statistics
    print("\n3. LEVEL SPACING STATISTICS")
    print("-" * 40)
    stats = op.eigenvalue_spacing_statistics(eigenvalues)
    print(f"   Mean spacing: {stats['mean_spacing']:.6f}")
    print(f"   Std of normalized spacing: {stats['std_spacing']:.6f}")
    
    # 4. Honest assessment
    print("\n4. HONEST ASSESSMENT")
    print("-" * 40)
    print("   ❌ This operator does NOT reproduce the Riemann zeros.")
    print("   ❌ The naive discretization destroys essential properties.")
    print("   ❌ A proper regularization (Connes, Berry-Keating) is needed.")
    print("   ✓ The code demonstrates the computational framework.")
    print("   ✓ Real research requires more sophisticated methods.")
    
    print("\n" + "=" * 70)
    print("END OF DEMONSTRATION")
    print("=" * 70)
    
    return eigenvalues, op


if __name__ == "__main__":
    eigenvalues, operator = main()
