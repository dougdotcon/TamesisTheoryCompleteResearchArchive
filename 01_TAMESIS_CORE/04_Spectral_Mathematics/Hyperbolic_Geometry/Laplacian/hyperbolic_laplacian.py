"""
Hyperbolic Laplacian Operator
=============================

Stage 11: Implementing Δ_H on the modular surface.

THE HYPERBOLIC LAPLACIAN
------------------------
On H with metric ds² = (dx² + dy²)/y², the Laplace-Beltrami operator is:

    Δ_H = -y² (∂²/∂x² + ∂²/∂y²)

Or equivalently:
    Δ_H = -y² ∂²/∂z∂z̄   (where z = x + iy)

SPECTRAL PROPERTIES ON SL(2,Z)\H
--------------------------------
- Continuous spectrum: [1/4, ∞)
- Discrete spectrum: finite number of eigenvalues λ_n
- Eigenvalues have form λ = 1/4 + r² where r is real or purely imaginary [0, i/2]

THE SELBERG CONNECTION
----------------------
The eigenvalues of Δ_H on Γ\H are related to Selberg zeta zeros.
For SL(2,Z)\H, these connect to Riemann zeros via the Riemann-Weil formula.
"""

import numpy as np
from scipy.sparse import diags, csr_matrix
from scipy.sparse.linalg import eigsh, eigs
from scipy.linalg import eigh
from typing import Tuple, Dict, List, Optional
import warnings


class HyperbolicLaplacian:
    """
    Discretized hyperbolic Laplacian on a portion of the fundamental domain.
    
    NOTE: Discretizing on a truncated domain is an approximation.
    The full spectrum requires more sophisticated methods (spectral theory, 
    automorphic forms).
    """
    
    def __init__(self, 
                 nx: int = 50, 
                 ny: int = 100,
                 y_min: float = 0.1,
                 y_max: float = 5.0,
                 x_min: float = -0.5,
                 x_max: float = 0.5):
        """
        Parameters
        ----------
        nx, ny : int
            Grid points in x and y directions
        y_min, y_max : float
            Truncated y range (full domain extends to infinity)
        x_min, x_max : float
            x range (standard fundamental domain: [-1/2, 1/2])
        """
        self.nx = nx
        self.ny = ny
        self.y_min = y_min
        self.y_max = y_max
        self.x_min = x_min
        self.x_max = x_max
        
        # Grid
        self.x = np.linspace(x_min, x_max, nx)
        self.y = np.linspace(y_min, y_max, ny)
        self.dx = self.x[1] - self.x[0]
        self.dy = self.y[1] - self.y[0]
        
        self.n_total = nx * ny
        
    def _index(self, i: int, j: int) -> int:
        """Convert 2D index (i,j) to 1D index."""
        return i * self.ny + j
    
    def _in_fundamental_domain(self, x: float, y: float) -> bool:
        """
        Check if point is in the fundamental domain.
        
        F = { z : |z| >= 1, |x| <= 1/2 }
        """
        r_sq = x**2 + y**2
        return r_sq >= 1 - 1e-10 and abs(x) <= 0.5 + 1e-10
    
    def build_laplacian_matrix(self, use_mask: bool = True) -> np.ndarray:
        """
        Build the discretized Laplacian matrix.
        
        Δ_H = -y² (∂²/∂x² + ∂²/∂y²)
        
        Using 5-point stencil:
        ∂²f/∂x² ≈ (f[i+1,j] - 2f[i,j] + f[i-1,j]) / dx²
        ∂²f/∂y² ≈ (f[i,j+1] - 2f[i,j] + f[i,j-1]) / dy²
        """
        n = self.n_total
        H = np.zeros((n, n))
        
        mask = np.ones((self.nx, self.ny), dtype=bool)
        
        for i in range(self.nx):
            for j in range(self.ny):
                x_val = self.x[i]
                y_val = self.y[j]
                
                # Check if in fundamental domain (for |z| >= 1 part)
                if use_mask and not self._in_fundamental_domain(x_val, y_val):
                    mask[i, j] = False
                    continue
                
                idx = self._index(i, j)
                y2 = y_val ** 2
                
                # Diagonal (center point)
                center_coeff = -y2 * (-2 / self.dx**2 - 2 / self.dy**2)
                H[idx, idx] = center_coeff
                
                # Off-diagonal (neighbors)
                # x-direction
                if i > 0 and (not use_mask or mask[i-1, j]):
                    H[idx, self._index(i-1, j)] = -y2 / self.dx**2
                if i < self.nx - 1 and (not use_mask or self._in_fundamental_domain(self.x[i+1], y_val)):
                    H[idx, self._index(i+1, j)] = -y2 / self.dx**2
                
                # y-direction
                if j > 0:
                    H[idx, self._index(i, j-1)] = -y2 / self.dy**2
                if j < self.ny - 1:
                    H[idx, self._index(i, j+1)] = -y2 / self.dy**2
        
        return H
    
    def compute_eigenvalues(self, n_eigenvalues: int = 20, use_mask: bool = False) -> np.ndarray:
        """
        Compute lowest eigenvalues of Δ_H.
        
        Returns the eigenvalues (should be >= 0 for -Δ_H).
        """
        H = self.build_laplacian_matrix(use_mask=use_mask)
        
        # Symmetrize (should be symmetric, but numerical errors)
        H = (H + H.T) / 2
        
        try:
            eigenvalues, _ = eigh(H)
            # Sort and return lowest
            eigenvalues = np.sort(eigenvalues)
            return eigenvalues[:n_eigenvalues]
        except Exception as e:
            warnings.warn(f"Eigenvalue computation failed: {e}")
            return np.array([])
    
    def spectral_parameter(self, eigenvalue: float) -> complex:
        """
        Convert eigenvalue λ to spectral parameter s.
        
        λ = s(1-s) = 1/4 + r² where s = 1/2 + ir
        
        So r = sqrt(λ - 1/4)
        """
        if eigenvalue >= 0.25:
            r = np.sqrt(eigenvalue - 0.25)
            return complex(0.5, r)  # s = 1/2 + ir
        else:
            # Exceptional eigenvalue
            r = np.sqrt(0.25 - eigenvalue)
            return complex(0.5 + r, 0)  # s = 1/2 + r (real)


class MaassWaveform:
    """
    Maass waveforms are eigenfunctions of the hyperbolic Laplacian on Γ\H.
    
    These are the analogs of "energy eigenstates" for the modular surface.
    """
    
    # Known spectral parameters for SL(2,Z)\H (first few Maass cusp forms)
    # These are r values where λ = 1/4 + r²
    KNOWN_R_VALUES = [
        9.533695,   # First Maass cusp form
        12.173008,
        13.779751,
        14.358509,
        16.138067,
        17.738563,
        18.880897,
        19.423483,
    ]
    
    @classmethod
    def known_eigenvalues(cls) -> np.ndarray:
        """
        Return known eigenvalues λ = 1/4 + r² for SL(2,Z)\H.
        """
        return np.array([0.25 + r**2 for r in cls.KNOWN_R_VALUES])
    
    @classmethod
    def compare_to_riemann(cls) -> Dict:
        """
        Compare Maass eigenvalues to Riemann zeros.
        
        The connection is not direct equality, but through the Selberg zeta function.
        """
        # First Riemann zeros (imaginary parts)
        riemann_zeros = np.array([
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918720, 43.327073, 48.005151, 49.773832
        ])
        
        r_values = np.array(cls.KNOWN_R_VALUES[:len(riemann_zeros)])
        
        return {
            'maass_r': r_values,
            'riemann_gamma': riemann_zeros[:len(r_values)],
            'note': 'These are NOT the same, but related via Selberg-Riemann-Weil'
        }


def main():
    """
    Demonstrate hyperbolic Laplacian computation.
    """
    print("=" * 70)
    print("STAGE 11: HYPERBOLIC LAPLACIAN")
    print("=" * 70)
    
    # 1. Build Laplacian
    print("\n1. BUILDING HYPERBOLIC LAPLACIAN")
    print("-" * 50)
    
    H = HyperbolicLaplacian(nx=30, ny=60, y_min=0.5, y_max=3.0)
    print(f"   Grid: {H.nx} x {H.ny} = {H.n_total} points")
    print(f"   Domain: x ∈ [{H.x_min}, {H.x_max}], y ∈ [{H.y_min}, {H.y_max}]")
    
    # 2. Compute eigenvalues
    print("\n2. COMPUTING EIGENVALUES")
    print("-" * 50)
    
    eigenvalues = H.compute_eigenvalues(n_eigenvalues=10, use_mask=False)
    
    print("   First 10 eigenvalues of Δ_H:")
    for i, lam in enumerate(eigenvalues[:10]):
        r = np.sqrt(abs(lam - 0.25)) if lam >= 0.25 else np.sqrt(0.25 - lam) * 1j
        print(f"      λ_{i+1} = {lam:10.4f}  →  r = {abs(r):8.4f}")
    
    # 3. Known Maass eigenvalues
    print("\n3. KNOWN MAASS EIGENVALUES (Literature)")
    print("-" * 50)
    
    known = MaassWaveform.known_eigenvalues()
    print("   First 5 known Maass cusp form eigenvalues:")
    for i, lam in enumerate(known[:5]):
        r = MaassWaveform.KNOWN_R_VALUES[i]
        print(f"      λ_{i+1} = {lam:10.4f}  (r = {r:.6f})")
    
    # 4. Comparison note
    print("\n4. THE DELICATE CONNECTION")
    print("-" * 50)
    comparison = MaassWaveform.compare_to_riemann()
    print("   Maass r-values vs Riemann zeros γ_n:")
    print(f"   {'n':>3} | {'r_maass':>12} | {'γ_riemann':>12}")
    print("   " + "-" * 35)
    for i in range(min(5, len(comparison['maass_r']))):
        print(f"   {i+1:>3} | {comparison['maass_r'][i]:>12.4f} | {comparison['riemann_gamma'][i]:>12.4f}")
    
    print("\n   NOTE: Maass eigenvalues and Riemann zeros are NOT directly equal.")
    print("   They are related through the Selberg zeta function Z(s).")
    print("   The full connection requires the trace formula machinery.")
    
    # 5. Honest assessment
    print("\n5. HONEST ASSESSMENT")
    print("-" * 50)
    print("   ❌ Our discretized eigenvalues do NOT match known Maass values")
    print("   ❌ Truncated domain destroys spectral properties")
    print("   ✓ Framework demonstrates the structure")
    print("   → Real computation requires automorphic form methods")
    
    print("\n" + "=" * 70)
    print("END OF HYPERBOLIC LAPLACIAN DEMONSTRATION")
    print("=" * 70)
    
    return H, eigenvalues


if __name__ == "__main__":
    H, eigenvalues = main()
