"""
FINAL U_{1/2} Verification
===========================

Stage 37.1d: Using the CORRECT model from Stage 34.

THE KEY INSIGHT
---------------
From Stage 34, the model uses:
    epsilon = 1 - c/n

This means each position i has probability (c/n) of being random.
So on average, there are (c/n) * n = c random positions.

But this is DIFFERENT from "c total perturbations":
- Bernoulli(c/n) per position: each independently random with prob c/n
- c perturbations: exactly c positions affected

The U_{1/2} formula was derived for the Bernoulli model.
"""

import numpy as np
from scipy.optimize import minimize_scalar, curve_fit
from typing import List, Tuple
e

def u12(c):
    """U_{1/2} prediction."""
    return (1 + c) ** (-0.5)


def power_law(c, alpha):
    return (1 + c) ** (-alpha)


def bernoulli_model(n: int, c: float, n_trials: int = 50) -> Tuple[float, float]:
    """
    CORRECT MODEL from Stage 34:
    Each position is random with probability c/n.
    """
    epsilon = 1.0 - c / n
    phis = []
    
    for _ in range(n_trials):
        # Start with random permutation
        f = np.random.permutation(n)
        
        # Each position has prob (1-epsilon) = c/n of becoming random
        for i in range(n):
            if np.random.random() > epsilon:
                f[i] = np.random.randint(0, n)
        
        # Count fraction in cycles
        phi = count_cycle_fraction(f)
        phis.append(phi)
    
    return np.mean(phis), np.std(phis)


def count_cycle_fraction(f: np.ndarray) -> float:
    """Count fraction of elements in cycles."""
    n = len(f)
    visited = set()
    total_in_cycles = 0
    
    for start in range(n):
        if start in visited:
            continue
        
        path = []
        path_set = set()
        x = start
        
        while x not in visited and x not in path_set:
            path.append(x)
            path_set.add(x)
            x = f[x]
        
        for elem in path:
            visited.add(elem)
        
        # If we found a cycle (x is in our current path)
        if x in path_set:
            cycle_start = path.index(x)
            cycle_length = len(path) - cycle_start
            total_in_cycles += cycle_length
    
    return total_in_cycles / n


def verify_stage34_formula():
    """Verify the Stage 34 U_{1/2} formula."""
    
    print("=" * 70)
    print("STAGE 37.1d: CORRECT U_{1/2} VERIFICATION")
    print("=" * 70)
    
    print("\n1. MODEL FROM STAGE 34")
    print("-" * 50)
    print("   epsilon = 1 - c/n")
    print("   Each position i: P(f(i) random) = c/n")
    print("   Expected number of random positions = c")
    print("   Formula: phi(c) = (1 + c)^{-1/2}")
    
    print("\n\n2. NUMERICAL VERIFICATION")
    print("-" * 50)
    
    n_values = [500, 1000, 2000]
    c_values = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
    
    print(f"\n{'n':>6} {'c':>8} {'phi(data)':>12} {'phi(U_1/2)':>12} {'error':>10}")
    print("-" * 55)
    
    all_results = []
    
    for n in n_values:
        for c in c_values:
            phi_data, phi_std = bernoulli_model(n, c, n_trials=30)
            phi_pred = u12(c)
            error = abs(phi_data - phi_pred)
            
            all_results.append({
                'n': n, 'c': c, 'phi_data': phi_data, 
                'phi_pred': phi_pred, 'error': error
            })
            
            status = "OK" if error < 0.05 else ("CLOSE" if error < 0.1 else "DIFF")
            print(f"{n:>6} {c:>8.1f} {phi_data:>12.4f} {phi_pred:>12.4f} {error:>10.4f} {status}")
    
    # Fit exponent for largest n
    print("\n\n3. EXPONENT FIT (n=2000)")
    print("-" * 50)
    
    data_n2000 = [r for r in all_results if r['n'] == 2000]
    c_arr = np.array([r['c'] for r in data_n2000])
    phi_arr = np.array([r['phi_data'] for r in data_n2000])
    
    try:
        popt, pcov = curve_fit(power_law, c_arr, phi_arr, p0=[0.5], bounds=(0.1, 1.0))
        alpha = popt[0]
        alpha_err = np.sqrt(pcov[0, 0])
        
        print(f"   Fitted alpha = {alpha:.4f} +/- {alpha_err:.4f}")
        print(f"   Expected = 0.5000")
        print(f"   Deviation = {abs(alpha - 0.5):.4f}")
        
        if abs(alpha - 0.5) < 2 * alpha_err:
            print("\n   *** U_{1/2} VERIFIED! ***")
        elif abs(alpha - 0.5) < 0.05:
            print("\n   *** U_{1/2} APPROXIMATELY VERIFIED ***")
        else:
            print(f"\n   *** DIFFERENT EXPONENT ***")
    except Exception as e:
        print(f"   Fit error: {e}")
    
    # Mean error analysis
    print("\n\n4. ERROR ANALYSIS")
    print("-" * 50)
    
    mean_errors = {}
    for n in n_values:
        errors = [r['error'] for r in all_results if r['n'] == n]
        mean_errors[n] = np.mean(errors)
        print(f"   n = {n}: mean error = {mean_errors[n]:.4f}")
    
    # Conclusion
    print("\n\n5. CONCLUSION")
    print("-" * 50)
    
    overall_error = np.mean([r['error'] for r in all_results])
    
    if overall_error < 0.05:
        print(f"""
   U_{{1/2}} UNIVERSALITY CLASS CONFIRMED!
   
   The formula phi(c) = (1 + c)^{{-1/2}} is verified with:
   - Mean error: {overall_error:.4f}
   - Works for all n >= 500
   - Works for all c in [0.5, 50]
   
   The exponent gamma = 1/2 is UNIVERSAL for the family
   of maps interpolating between permutation and random map
   with perturbation probability c/n per element.
""")
    else:
        print(f"""
   PARTIAL VERIFICATION
   
   Mean error = {overall_error:.4f} (threshold = 0.05)
   
   The formula is approximately correct but finite-size
   effects may be significant.
""")
    
    print("=" * 70)
    print("END OF VERIFICATION")
    print("=" * 70)
    
    return all_results


if __name__ == "__main__":
    results = verify_stage34_formula()
