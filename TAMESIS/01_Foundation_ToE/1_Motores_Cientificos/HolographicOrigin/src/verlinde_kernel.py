"""
Scientific Audit Module 02: Theoretical Derivation & Interpolation
------------------------------------------------------------------
Author: Antigravity (Elite Physicist System)

Objective:
Replace the naive `if/else` transition logic with a physically motivated
Interpolation Function (mu-function) as requested by 'Prof. Verlinde'.

Theory:
Original code: Hard switch at a_N = a_0. This violates Smoothness (C1 continuity).
New code:      Simple Interpolation Function standard in MOND/Verlinde literature.

Equation:
g * mu(g/a0) = g_N
Standard Interpolation: mu(x) = x / (1+x)
This leads to: g = g_N/2 + sqrt(g_N^2/4 + g_N * a_0)

This ensures a smooth transition from Newton (g ~ g_N) to Deep MOND (g ~ sqrt(g_N a_0)).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTS ---
G = 1.0
M = 1000.0
A0 = 2.0
R_RANGE = np.linspace(1, 200, 500)

def force_newton(r):
    return G * M / (r**2)

def force_naive_switch(r):
    """The original logic: Discontinuous derivative."""
    g_n = force_newton(r)
    if g_n > A0:
        return g_n
    else:
        return np.sqrt(g_n * A0)

def force_scientific_interpolation(r):
    """
    Physically rigorous smooth interpolation.
    Inverting mu(x) = x/(1+x) -> g = g_N * (1 + sqrt(1 + 4/(g_N/a0))) / 2 ??
    
    Actually, let's derive it:
    g * (g / (g + a0)) = g_N  -> g^2 / (g + a0) = g_N
    g^2 = g*g_N + a0*g_N
    g^2 - g*g_N - a0*g_N = 0
    Quadratic formula:
    g = (g_N + sqrt(g_N^2 + 4*a0*g_N)) / 2
    """
    g_n = force_newton(r)
    term_sqrt = np.sqrt(g_n**2 + 4 * A0 * g_n)
    return (g_n + term_sqrt) / 2

def run_comparison():
    print("🔬 RUNNING INTERPOLATION ANALYSIS...")
    
    g_newton = force_newton(R_RANGE)
    g_naive = [force_naive_switch(r) for r in R_RANGE]
    g_smooth = [force_scientific_interpolation(r) for r in R_RANGE]
    
    # Calculate Orbital Velocities
    v_newton = np.sqrt(g_newton * R_RANGE)
    v_naive = np.sqrt(np.array(g_naive) * R_RANGE)
    v_smooth = np.sqrt(np.array(g_smooth) * R_RANGE)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(R_RANGE, v_newton, 'k--', label='Newtonian Prediction', alpha=0.5)
    plt.plot(R_RANGE, v_naive, 'r-', label='Original Naive (Switch)', linewidth=1)
    plt.plot(R_RANGE, v_smooth, 'g-', label='Smooth Theory (Verlinde 2016)', linewidth=2)
    
    plt.xlabel('Radius')
    plt.ylabel('Orbital Velocity')
    plt.title('Theoretical Consistency Check: Interpolation Functions')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("interpolation_analysis.png")
    print("✅ Analysis Plot Saved: interpolation_analysis.png")
    
    # Generate Report
    with open("derivation_analysis.md", "w") as f:
        f.write("# Challenge 2: Theoretical Fundamentals\n\n")
        f.write("## The Interpolation Problem\n")
        f.write("The original code used a hard switch `if a_N < a_0`. This creates a `kink` in the force field, "
                "which implies an infinite jerk (da/dt) for particles crossing the threshold. This is unphysical.\n\n")
        f.write("## The Improved Derivation\n")
        f.write("We implemented the standard MOND interpolation function $\mu(x) = x/(1+x)$, inverted to solve for $g$:\n")
        f.write("$$ g = \\frac{g_N + \\sqrt{g_N^2 + 4 g_N a_0}}{2} $$\n\n")
        f.write("## Comparison Result\n")
        f.write("As seen in `interpolation_analysis.png`, the Green Curve (Smooth) creates a much more physical transition "
                "than the Red Curve (Naive). It avoids the sharp corner at the transition radius.\n")
        f.write("\n**Verdict:** The code must be updated to use the Smooth function to withstand peer review.")

if __name__ == "__main__":
    run_comparison()
