"""
Stage 80: Elastic Memory Transition
===================================

Implementing the core mechanism of TDTR:
The transition from Newtonian/GR acceleration to Entropic acceleration
due to the elastic memory of the holographic screen.

Mathematical Model:
We implement the transition knowing that at low accelerations (a < a0),
the entropy-area relation changes due to memory effects (Verlinde).

Relation:
g_obs = g_bar + sqrt(a0 * g_bar)   (Simple approximation)
or
g_obs^2 / (g_obs - g_bar) = a0    (If we follow MOND-like interpolation)

For this stage, we use the Entropic Gravity relation derived by Verlinde (2016):
g_obs = g_bar + (a0 * g_bar)^0.5  (Deep MOND limit approx)

However, the FULL equation usually involves an interpolation.
We will implement the 'Simple' interpolation function commonly used in MOND
as a proxy for the Entropic transition, as they are phenomenologically similar.

a = a_N * nu(a_N / a0)

where nu(x) -> 1 for x >> 1
      nu(x) -> 1/sqrt(x) for x << 1

But TDTR claims this is a PHASE TRANSITION, not just a smooth curve.
We will test if a sharp transition works better?
No, let's stick to the standard Entropic formula for now.

Author: TDTR Research Program
Date: 2026-01-23
"""

import numpy as np

def entropic_interpolation_function(x):
    """
    Interpolation function nu(x) where x = a_N / a0.
    Standard 'Simple' function: nu(x) = 0.5 * (1 + sqrt(1 + 4/x))
    
    Derivation:
    a = a_N * nu(x)
    In deep limit: a = sqrt(a_N * a0)
    
    Relation: a * mu(a/a0) = a_N where mu(y) = y / (1+y) (Simple)
    Inverse gives the simple interpolation above.
    """
    # x = a_N / a0
    # a_result = a_N * 0.5 * (1 + np.sqrt(1 + 4/x))
    # Let's check limits:
    # Large x: 1 + 4/x ~ 1. sqrt(1) = 1. 0.5*(2) = 1. a = a_N. Correct.
    # Small x: 1 + 4/x ~ 4/x. sqrt(4/x) = 2/sqrt(x). 0.5*(2/sqrt(x)) = 1/sqrt(x).
    #          a = a_N * 1/sqrt(x) = a_N * sqrt(a0/a_N) = sqrt(a_N * a0). Correct.

    return 0.5 * (1 + np.sqrt(1 + 4.0/x))

def calculate_entropic_acceleration(a_newton_ms2, a0_ms2=1.2e-10):
    """
    Calculate the observed entropic acceleration.
    
    Args:
        a_newton_ms2 (float or array): Newtonian acceleration in m/s^2.
        a0_ms2 (float): Critical acceleration scale.
        
    Returns:
        float or array: Entropic acceleration in m/s^2.
    """
    # Avoid division by zero
    a_newton_safe = np.maximum(a_newton_ms2, 1e-20)
    
    x = a_newton_safe / a0_ms2
    nu = entropic_interpolation_function(x)
    
    a_entropic = a_newton_safe * nu
    return a_entropic

def test_transition():
    """Verify the transition logic."""
    print("Testing Elastic Memory Transition Logic...")
    a0 = 1.2e-10
    
    # Test High Acceleration (Solar System scale)
    a_high = 1e-5 # >> a0
    a_high_obs = calculate_entropic_acceleration(a_high, a0)
    ratio_high = a_high_obs / a_high
    print(f"High Acc (a_N={a_high:.1e}): a_obs={a_high_obs:.1e}, Ratio={ratio_high:.4f} (Expect ~1.0)")
    
    # Test Low Acceleration (Galactic outskirts)
    a_low = 1e-12 # << a0
    a_low_obs = calculate_entropic_acceleration(a_low, a0)
    ratio_low = a_low_obs / a_low
    expected_low = np.sqrt(a_low * a0)
    print(f"Low Acc  (a_N={a_low:.1e}): a_obs={a_low_obs:.1e}, Ratio={ratio_low:.1f}")
    print(f"  Expected Deep Limit: {expected_low:.1e}")
    
    if np.isclose(a_low_obs, expected_low, rtol=0.1):
        print(">> PASS: Deep limit behavior confirmed.")
    else:
        print(">> FAIL: Deep limit mismatch.")

if __name__ == "__main__":
    test_transition()
