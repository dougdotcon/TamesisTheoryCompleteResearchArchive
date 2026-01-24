"""
Modified Berry-Keating Operators: H = xp + V(x)
================================================

Stage 8 Path A1: Test if adding a potential V(x) to the Berry-Keating
operator produces a spectrum matching Riemann zeros.

MATHEMATICAL MOTIVATION
-----------------------
The pure xp operator has continuous spectrum on R+.
Adding a confining potential V(x) may:
1. Create discrete spectrum
2. Regularize the operator at boundaries
3. Potentially match Riemann zeros (unlikely, but worth testing)

POTENTIALS TO TEST
------------------
1. Harmonic: V(x) = ω²x² (quantum oscillator)
2. Coulomb: V(x) = -Z/x (hydrogen-like)
3. Logarithmic: V(x) = λ log(x) (scale-invariant)
4. Box: V(x) = 0 inside, ∞ outside (infinite well)
5. Exponential: V(x) = exp(-αx) (short-range)
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple, Callable, List
import warnings


class ModifiedBerryKeating:
    """
    H = xp + V(x) = -i(x d/dx + 1/2) + V(x)
    """
    
    # First 20 Riemann zeros
    RIEMANN_ZEROS = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840
    ])
    
    def __init__(self, 
                 potential: Callable[[float], float],
                 potential_name: str,
                 domain: Tuple[float, float] = (0.1, 50.0),
                 n_points: int = 300):
        """
        Parameters
        ----------
        potential : Callable
            V(x) function
        potential_name : str
            Name for display
        domain : Tuple[float, float]
            [a, b] interval
        n_points : int
            Grid points
        """
        self.V = potential
        self.V_name = potential_name
        self.a, self.b = domain
        self.n = n_points
        
        self.x = np.linspace(self.a, self.b, n_points)
        self.dx = self.x[1] - self.x[0]
        
        self.H = self._build_operator()
    
    def _build_operator(self) -> np.ndarray:
        """
        Build H = -i(x d/dx + 1/2) + V(x)
        """
        n = self.n
        H = np.zeros((n, n), dtype=complex)
        
        for j in range(n):
            x_j = self.x[j]
            
            # xp part: -i(1/2) on diagonal
            H[j, j] = -0.5j + self.V(x_j)
            
            # xp part: -i x d/dx off-diagonal
            if j > 0:
                H[j, j-1] = -1j * x_j * (-1.0 / (2 * self.dx))
            if j < n - 1:
                H[j, j+1] = -1j * x_j * (1.0 / (2 * self.dx))
        
        # Symmetrize to get real eigenvalues
        H_sym = (H + np.conj(H.T)) / 2
        
        return H_sym
    
    def compute_spectrum(self) -> np.ndarray:
        """Compute eigenvalues."""
        eigenvalues, _ = eigh(self.H)
        return eigenvalues
    
    def compare_to_zeros(self, eigenvalues: np.ndarray) -> Dict:
        """
        Compare positive eigenvalues to Riemann zeros.
        """
        pos_eig = np.sort(eigenvalues[eigenvalues > 0])
        
        if len(pos_eig) < 5:
            return {
                'match_score': 0,
                'first_eigenvalue': None,
                'message': 'Too few positive eigenvalues'
            }
        
        n = min(len(pos_eig), len(self.RIEMANN_ZEROS))
        
        # Correlation
        corr = np.corrcoef(pos_eig[:n], self.RIEMANN_ZEROS[:n])[0, 1]
        
        # Relative error for first eigenvalue
        first_error = abs(pos_eig[0] - self.RIEMANN_ZEROS[0]) / self.RIEMANN_ZEROS[0]
        
        # Mean relative error
        mean_error = np.mean(np.abs(pos_eig[:n] - self.RIEMANN_ZEROS[:n]) / self.RIEMANN_ZEROS[:n])
        
        # Match score: 1 = perfect, 0 = no match
        match_score = max(0, 1 - mean_error) if np.isfinite(mean_error) else 0
        
        return {
            'correlation': corr if np.isfinite(corr) else 0,
            'first_eigenvalue': pos_eig[0],
            'first_zero': self.RIEMANN_ZEROS[0],
            'first_error_percent': first_error * 100,
            'mean_error_percent': mean_error * 100,
            'match_score': match_score,
            'n_compared': n
        }


class PotentialLibrary:
    """
    Collection of potentials to test.
    """
    
    @staticmethod
    def harmonic(omega: float = 0.1):
        """V(x) = ω²x²"""
        return lambda x: omega**2 * x**2, f"Harmonic(ω={omega})"
    
    @staticmethod
    def coulomb(Z: float = 1.0):
        """V(x) = -Z/x"""
        return lambda x: -Z / max(x, 0.01), f"Coulomb(Z={Z})"
    
    @staticmethod
    def logarithmic(lam: float = 1.0):
        """V(x) = λ log(x)"""
        return lambda x: lam * np.log(max(x, 0.01)), f"Logarithmic(λ={lam})"
    
    @staticmethod
    def inverse_square(alpha: float = 1.0):
        """V(x) = α/x²"""
        return lambda x: alpha / max(x**2, 0.0001), f"InverseSquare(α={alpha})"
    
    @staticmethod
    def exponential_decay(alpha: float = 0.1):
        """V(x) = exp(-αx)"""
        return lambda x: np.exp(-alpha * x), f"ExpDecay(α={alpha})"
    
    @staticmethod
    def linear(slope: float = 0.5):
        """V(x) = slope * x"""
        return lambda x: slope * x, f"Linear(m={slope})"
    
    @staticmethod
    def combined_log_inv(c1: float = 1.0, c2: float = 1.0):
        """V(x) = c1*log(x) + c2/x (Berry-Keating regularization idea)"""
        return lambda x: c1 * np.log(max(x, 0.01)) + c2 / max(x, 0.01), f"LogPlusInv(c1={c1},c2={c2})"


def run_potential_scan():
    """
    Scan all potentials and compare to Riemann zeros.
    """
    print("=" * 70)
    print("STAGE 8: MODIFIED BERRY-KEATING OPERATORS")
    print("Testing H = xp + V(x)")
    print("=" * 70)
    
    # Potentials to test
    potentials = [
        PotentialLibrary.harmonic(0.01),
        PotentialLibrary.harmonic(0.1),
        PotentialLibrary.harmonic(1.0),
        PotentialLibrary.coulomb(1.0),
        PotentialLibrary.coulomb(10.0),
        PotentialLibrary.logarithmic(1.0),
        PotentialLibrary.logarithmic(10.0),
        PotentialLibrary.inverse_square(1.0),
        PotentialLibrary.exponential_decay(0.1),
        PotentialLibrary.linear(0.1),
        PotentialLibrary.linear(1.0),
        PotentialLibrary.combined_log_inv(1.0, 1.0),
        PotentialLibrary.combined_log_inv(10.0, 1.0),
    ]
    
    results = []
    best_match = None
    best_score = 0
    
    print("\n1. SCANNING POTENTIALS")
    print("-" * 50)
    
    for V_func, V_name in potentials:
        try:
            op = ModifiedBerryKeating(V_func, V_name, domain=(0.1, 100.0), n_points=300)
            eigenvalues = op.compute_spectrum()
            comparison = op.compare_to_zeros(eigenvalues)
            comparison['potential'] = V_name
            results.append(comparison)
            
            score = comparison['match_score']
            if score > best_score:
                best_score = score
                best_match = comparison
            
            first_e = comparison.get('first_eigenvalue', 'N/A')
            if isinstance(first_e, float):
                print(f"   {V_name:30} | E_1 = {first_e:8.2f} | γ_1 = 14.13 | Score: {score:.3f}")
            else:
                print(f"   {V_name:30} | {first_e}")
                
        except Exception as e:
            print(f"   {V_name:30} | ERROR: {str(e)[:30]}")
    
    # Best result
    print("\n\n2. BEST RESULT")
    print("-" * 50)
    
    if best_match:
        print(f"   Potential: {best_match['potential']}")
        print(f"   Match score: {best_match['match_score']:.4f}")
        print(f"   First eigenvalue: {best_match['first_eigenvalue']:.4f}")
        print(f"   Target (γ_1): {best_match['first_zero']:.4f}")
        print(f"   Error: {best_match['first_error_percent']:.2f}%")
    
    # Honest assessment
    print("\n\n3. HONEST ASSESSMENT")
    print("-" * 50)
    
    if best_score > 0.9:
        print("   ⚠️ High match score! Investigate further.")
    elif best_score > 0.5:
        print("   ~ Moderate match. May be coincidental.")
    else:
        print("   ❌ No good match found.")
        print("   → Simple potentials do NOT reproduce Riemann zeros.")
        print("   → The 'true' operator (if it exists) is more subtle.")
    
    print("\n" + "=" * 70)
    print("END OF POTENTIAL SCAN")
    print("=" * 70)
    
    return results, best_match


if __name__ == "__main__":
    results, best = run_potential_scan()
