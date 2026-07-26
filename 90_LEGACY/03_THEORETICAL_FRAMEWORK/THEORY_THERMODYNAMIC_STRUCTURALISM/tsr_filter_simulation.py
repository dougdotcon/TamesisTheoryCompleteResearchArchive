"""
TSR FILTER SIMULATION
---------------------
Simulation of the "Reality Filter" (Theory of Structural Realization).
We model the probability of a mathematical structure 'surviving' as a physical object
based on its Thermodynamic Cost.

Principles:
1. Cost = exp(Complexity) for Class NR (Non-Realizable).
2. Cost = poly(Complexity) for Class R (Realizable).
3. Landauer Wall: Maximum available resource threshold.

This script generates the "Wall of Censorship" plot.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simulate_filter():
    complexity = np.linspace(1, 50, 100) # System Size N
    limit_resource = 1e12 # The Landauer Wall (Arbitrary units)

    # 1. Class R (Realizable) - Polynomial Scaling
    # Cost ~ N^3 (Standard Matrix Operations)
    cost_r = complexity ** 3
    
    # 2. Class NR (Non-Realizable) - Exponential Scaling
    # Cost ~ exp(N) (Spin Glass / NP-Hard)
    cost_nr = np.exp(0.5 * complexity)
    
    # 3. The Filter (Survivability)
    # P(Survive) ~ exp(-Cost / Temperature)
    # Actually, simplistic view: if Cost > Limit -> Censored
    
    plt.figure(figsize=(10, 6))
    
    # Plot Costs
    plt.semilogy(complexity, cost_r, label='Class R (Polynomial / Stable)', color='blue', linewidth=2)
    plt.semilogy(complexity, cost_nr, label='Class NR (Exponential / Unstable)', color='red', linewidth=2)
    
    # Plot The Wall
    plt.axhline(y=limit_resource, color='black', linestyle='--', linewidth=3, label='Landauer Wall (Physical Limit)')
    
    # Shade the "Forbidden Zone"
    plt.fill_between(complexity, limit_resource, np.max(cost_nr)*1.1, color='gray', alpha=0.2, label='Censored Region')
    
    plt.xlabel('Structural Complexity (N)')
    plt.ylabel('Thermodynamic Cost (Log Scale)')
    plt.title('The Reality Filter: Why Class NR is Censored')
    plt.legend()
    plt.grid(True, alpha=0.3, which="both")
    
    # Find Crossing Points
    # Approx check
    crossing_r = complexity[cost_r > limit_resource]
    crossing_nr = complexity[cost_nr > limit_resource]
    
    msg_r = f"Class R hits wall at N={crossing_r[0]:.1f}" if len(crossing_r)>0 else "Class R survives range"
    msg_nr = f"Class NR hits wall at N={crossing_nr[0]:.1f}" if len(crossing_nr)>0 else "Class NR survives range"
    
    plt.text(5, limit_resource*2, "NON-REALIZABLE ZONE", fontsize=12, fontweight='bold', color='gray')
    
    print(f"Simulation Complete.")
    print(msg_r)
    print(msg_nr)
    
    plt.savefig('tsr_filter_plot.png', dpi=300)
    print("Plot saved to 'tsr_filter_plot.png'")

if __name__ == "__main__":
    simulate_filter()
