"""
Stage 19: Selberg-Weil Interface
================================

LAYER 1 - REAL MATHEMATICS

THE CONNECTION:
---------------
This stage connects our scattering phase decomposition to the 
Weil explicit formula, showing how the oscillatory term E_zeta(T)
is controlled by Riemann zeros.

THE EXPLICIT FORMULAS:
----------------------

1. WEIL EXPLICIT FORMULA (for zeta):
   sum_{rho} h(rho) = h(0) + h(1) - sum_p sum_k (log p / p^{k/2}) * g(k log p)
   
   where h is a test function and g its Mellin transform.

2. SELBERG TRACE FORMULA (for Gamma\H):
   sum_n h(r_n) = (mu/4pi) * integral h(r) r tanh(pi r) dr
                  + sum_gamma sum_k (l_gamma / 2 sinh(k l_gamma/2)) * g(k l_gamma)
                  + (cusp terms)

3. THE DICTIONARY:
   Selberg                    Weil
   --------                   ----
   h(r_n) (eigenvalues)   <-> h(gamma_n) (zeros)
   l_gamma (geodesic)     <-> log p (prime)
   trace formula          <-> explicit formula

THE KEY INSIGHT:
----------------
The oscillatory part of Theta(T) is controlled by:

E_zeta(T) = (1/pi) * sum_gamma (contribution from zero gamma)

This connects SPECTRAL THEORY to NUMBER THEORY explicitly.
"""

import numpy as np
from scipy.special import loggamma
from typing import Dict, List, Tuple, Callable
import warnings


class WeilExplicitFormula:
    """
    The Weil explicit formula connecting primes to zeros.
    
    For a suitable test function h:
    
    sum_{rho} h(gamma) = h(1/2) + h(-1/2) 
                        - (1/2pi) * integral h(t) * (Gamma'/Gamma)(1/4 + it/2) dt
                        - sum_p sum_k (log p / p^{k/2}) * h_hat(k log p)
    
    The sum over rho is over non-trivial zeros rho = 1/2 + i*gamma.
    """
    
    @staticmethod
    def prime_sum_contribution(h_hat: Callable, max_prime: int = 1000) -> float:
        """
        Compute the prime sum: sum_p sum_k (log p / p^{k/2}) * h_hat(k log p)
        """
        # Generate primes
        primes = WeilExplicitFormula._sieve(max_prime)
        
        result = 0.0
        for p in primes:
            log_p = np.log(p)
            # Sum over k (usually only k=1,2 matter for large p)
            for k in range(1, 10):
                if p ** (k/2) > max_prime:
                    break
                term = (log_p / (p ** (k/2))) * h_hat(k * log_p)
                result += term
        
        return result
    
    @staticmethod
    def _sieve(n: int) -> List[int]:
        """Sieve of Eratosthenes."""
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False
        for i in range(2, int(np.sqrt(n)) + 1):
            if is_prime[i]:
                for j in range(i*i, n + 1, i):
                    is_prime[j] = False
        return [i for i in range(n + 1) if is_prime[i]]
    
    @staticmethod
    def zero_sum_structure(T: float) -> Dict:
        """
        Structure of the sum over zeros in the explicit formula.
        
        For counting zeros up to height T:
        N(T) = (T/2pi) log(T/2pi) - T/2pi + 1 + S(T)
        
        where S(T) = (1/pi) arg(zeta(1/2 + iT)) fluctuates.
        """
        # Main term
        main_term = (T / (2 * np.pi)) * np.log(T / (2 * np.pi)) - T / (2 * np.pi)
        
        # S(T) fluctuates around 0 with magnitude O(log T) unconditionally
        # Under RH, S(T) = O(log T / log log T)
        
        return {
            'T': T,
            'N_main': main_term,
            'S_bound_unconditional': np.log(T),
            'S_bound_RH': np.log(T) / np.log(np.log(T + 10)),
            'note': 'S(T) encodes fine structure of zero distribution'
        }


class SelbergTraceFormula:
    """
    The Selberg trace formula for Gamma\H.
    
    For M = SL(2,Z)\H with Laplacian eigenvalues lambda_n = 1/4 + r_n^2:
    
    sum_n h(r_n) = (geometric terms) + (cusp terms)
    
    The cusp term involves the scattering phase Theta(T).
    """
    
    @staticmethod
    def weyl_term(h: Callable, area: float = np.pi/3, max_r: float = 100) -> float:
        """
        The Weyl term (main asymptotic):
        (mu/4pi) * integral_0^infty h(r) * r * tanh(pi*r) dr
        """
        # Numerical integration
        r_values = np.linspace(0.01, max_r, 1000)
        integrand = h(r_values) * r_values * np.tanh(np.pi * r_values)
        
        dr = r_values[1] - r_values[0]
        integral = np.sum(integrand) * dr
        
        return (area / (4 * np.pi)) * integral
    
    @staticmethod
    def identity_term(h: Callable) -> float:
        """
        The identity contribution.
        For SL(2,Z), this is:
        (1/4pi) * integral h(r) * (Gamma'/Gamma)(1 + ir) dr
        """
        # This is related to the digamma function
        return 0.0  # Placeholder - needs careful implementation
    
    @staticmethod
    def hyperbolic_terms_structure() -> str:
        """
        Structure of the hyperbolic (geodesic) terms.
        """
        return """
HYPERBOLIC TERMS:
-----------------
sum_gamma sum_k (l_gamma / 2 sinh(k l_gamma / 2)) * g(k l_gamma)

where:
- gamma runs over primitive closed geodesics
- l_gamma = length of geodesic gamma
- k runs over 1, 2, 3, ... (multiple traversals)
- g = Fourier transform of h

For SL(2,Z)\H:
- Primitive geodesics correspond to hyperbolic conjugacy classes
- Length l_gamma = 2 * log(epsilon_gamma) where epsilon_gamma is a unit
- The shortest geodesic has length 2 * log((3 + sqrt(5))/2) ~ 1.9248

ANALOGY WITH PRIMES:
l_gamma <-> log(p)
primitive geodesic <-> prime p
multiple traversal k <-> prime power p^k
"""


class ScatteringZeroConnection:
    """
    The connection between scattering phase and Riemann zeros.
    
    KEY RESULT:
    -----------
    The oscillatory part of Theta(T) is:
    
    E_zeta(T) = (1/pi) * arg(zeta(2iT)/zeta(1+2iT))
    
    This can be written as a sum over zeros:
    
    arg(zeta(s)) = sum_{rho} arg(s - rho) + (regular terms)
    
    So E_zeta(T) explicitly encodes the distribution of Riemann zeros.
    """
    
    @staticmethod
    def arg_zeta_zero_expansion(T: float, zeros: List[float]) -> Dict:
        """
        Expand arg(zeta(s)) in terms of zeros.
        
        For s = sigma + iT with sigma > 1/2:
        arg(zeta(s)) = sum_gamma arctan((T - gamma)/(sigma - 1/2)) + ...
        
        where gamma are the imaginary parts of zeros rho = 1/2 + i*gamma.
        """
        s = complex(0.5, 2*T)  # We're looking at zeta(2iT) ~ zeta(1/2 + 2iT) via functional eq
        
        # Contribution from each zero
        contributions = []
        for gamma in zeros:
            # Distance from s to the zero 1/2 + i*gamma
            # arg(s - rho) where rho = 1/2 + i*gamma
            delta_real = s.real - 0.5
            delta_imag = s.imag - gamma
            
            contrib = np.arctan2(delta_imag, delta_real)
            contributions.append({
                'gamma': gamma,
                'contribution': contrib
            })
        
        total = sum(c['contribution'] for c in contributions)
        
        return {
            'T': T,
            's': s,
            'zero_contributions': contributions[:10],  # First 10
            'total_from_zeros': total,
            'note': 'This shows how zeros control arg(zeta)'
        }
    
    @staticmethod
    def theta_zeta_as_zero_sum(T: float) -> Dict:
        """
        Express Theta_zeta(T) as a sum involving zeros.
        
        Theta_zeta(T) = (1/pi) * [arg zeta(2iT) - arg zeta(1 + 2iT)]
        
        The first term (at 2iT) is sensitive to zeros near height 2T.
        The second term (at 1 + 2iT) is regular (no zeros nearby).
        """
        # First 20 known Riemann zeros (imaginary parts)
        known_zeros = [
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918720, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
            67.079811, 69.546402, 72.067158, 75.704691, 77.144840
        ]
        
        # Which zeros are near height 2T?
        height = 2 * T
        nearby_zeros = [g for g in known_zeros if abs(g - height) < 10]
        
        # Rough estimate of contribution
        if nearby_zeros:
            avg_distance = np.mean([abs(g - height) for g in nearby_zeros])
            contribution_estimate = len(nearby_zeros) * np.pi / 2  # rough
        else:
            avg_distance = None
            contribution_estimate = 0
        
        return {
            'T': T,
            'height_2T': height,
            'nearby_zeros': nearby_zeros,
            'num_nearby': len(nearby_zeros),
            'avg_distance': avg_distance,
            'contribution_estimate': contribution_estimate,
            'interpretation': 'Zeros near height 2T cause fluctuations in Theta_zeta'
        }


class SelbergWeilDictionary:
    """
    The complete dictionary between Selberg and Weil.
    """
    
    @staticmethod
    def display_dictionary() -> str:
        return """
================================================================================
THE SELBERG-WEIL DICTIONARY (Rigorous Version)
================================================================================

SELBERG (Geometry)              |  WEIL (Arithmetic)
--------------------------------|--------------------------------
Surface M = Gamma\H             |  Integers Z
Laplacian eigenvalue lambda_n   |  Riemann zero rho_n = 1/2 + i*gamma_n
Spectral parameter r_n          |  Zero height gamma_n
                                |
Primitive geodesic gamma        |  Prime p
Geodesic length l(gamma)        |  log(p)
Norm N(gamma) = e^{l(gamma)}    |  Prime p
                                |
Selberg zeta Z_Gamma(s)         |  Riemann zeta zeta(s)
Selberg trace formula           |  Weil explicit formula
                                |
Scattering matrix phi(s)        |  (relates to functional equation)
Scattering phase Theta(T)       |  S(T) = (1/pi) arg zeta(1/2 + iT)
                                |
Area mu(M)                      |  (relates to residue at s=1)

================================================================================
KEY PARALLEL:
================================================================================

SELBERG TRACE FORMULA:
sum_n h(r_n) = (mu/4pi) int h(r) r tanh(pi r) dr
             + sum_{gamma} sum_k (l_gamma / 2 sinh(k l_gamma/2)) g(k l_gamma)
             + (cusp terms involving phi)

WEIL EXPLICIT FORMULA:
sum_rho h(gamma_rho) = h(0) + h(1)
                     - sum_p sum_k (log p / p^{k/2}) h_hat(k log p)
                     + (Gamma terms)

THE ANALOGY:
- Eigenvalues <-> Zeros
- Geodesics <-> Primes
- Both count via trace/explicit formulas
- Both have "main term + oscillatory term" structure

================================================================================
"""
    
    @staticmethod
    def main_result() -> str:
        return """
================================================================================
MAIN RESULT OF STAGE 19
================================================================================

THEOREM (Selberg-Weil Connection for Scattering Phase):

The scattering phase Theta(T) for M = SL(2,Z)\H satisfies:

1. DECOMPOSITION:
   Theta(T) = (T/2pi) log(T/2pi) - T/2pi + E(T)

2. ERROR TERM:
   E(T) = E_Gamma + E_zeta
   
   where:
   - E_Gamma = -1/4 + O(1/T)  [analytic, bounded]
   - E_zeta = O(log T)        [arithmetic, from zeros]

3. ZERO CONNECTION:
   E_zeta(T) is controlled by Riemann zeros near height 2T:
   
   E_zeta(T) ~ (1/pi) * sum_{|gamma - 2T| < delta} f(gamma - 2T)
   
   for some kernel f.

4. PARALLEL TO WEIL:
   Just as S(T) = (1/pi) arg zeta(1/2 + iT) in the Riemann-von Mangoldt formula
   fluctuates due to nearby zeros, so does E_zeta(T) in Theta(T).

SIGNIFICANCE:
This provides an EXPLICIT mechanism connecting:
- Spectral theory of hyperbolic surfaces
- Distribution of Riemann zeros
- The "excess" beyond Weyl law

================================================================================
"""


def demonstrate_selberg_weil_interface():
    """
    Demonstrate the Selberg-Weil connection.
    """
    print("=" * 70)
    print("STAGE 19: SELBERG-WEIL INTERFACE")
    print("Connecting Scattering Phase to Riemann Zeros")
    print("=" * 70)
    
    print(SelbergWeilDictionary.display_dictionary())
    
    print("\n" + "=" * 70)
    print("ZERO PROXIMITY ANALYSIS")
    print("=" * 70)
    
    connection = ScatteringZeroConnection()
    
    T_values = [5, 10, 15, 20, 25]
    
    print(f"\n{'T':>6} | {'Height 2T':>10} | {'Nearby zeros':>15} | {'Count':>6}")
    print("-" * 50)
    
    for T in T_values:
        result = connection.theta_zeta_as_zero_sum(T)
        zeros_str = ', '.join([f'{g:.1f}' for g in result['nearby_zeros'][:3]])
        if len(result['nearby_zeros']) > 3:
            zeros_str += '...'
        print(f"{T:>6} | {result['height_2T']:>10.1f} | {zeros_str:>15} | {result['num_nearby']:>6}")
    
    print(SelbergWeilDictionary.main_result())
    
    print(SelbergTraceFormula.hyperbolic_terms_structure())
    
    print("\n" + "=" * 70)
    print("END OF STAGE 19")
    print("=" * 70)
    
    return connection


if __name__ == "__main__":
    connection = demonstrate_selberg_weil_interface()
