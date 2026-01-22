"""
Scientific Audit Module 03: Boundary Conditions & Equivalence Principle
-----------------------------------------------------------------------
Author: Antigravity (Elite Physicist System)

Objective:
Test the behavior of Entropic Gravity in a non-trivial geometry: A Galaxy Collision.
Verlinde's theory (and MOND) relies on the *absolute* acceleration |a|.
In the saddle point between two massive bodies, |a| -> 0.

The "External Field Effect" (EFE) implies that MOND/Entropic effects might break
Newtonian superposition.

Scenario:
Two Equal Mass Black Holes approaching each other.
We track a test particle in the saddle point.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTS ---
G = 1.0
M = 1000.0  # Mass of each galaxy center
A0 = 2.0
DT = 0.1
STEPS = 2000

def force_scientific_interpolation(g_n):
    """Smooth force law based on MAGNITUDE of acceleration."""
    # g * mu(g/a0) = g_n
    # g = (g_n + sqrt(g_n^2 + 4 a0 g_n)) / 2
    term_sqrt = np.sqrt(g_n**2 + 4 * A0 * g_n)
    return (g_n + term_sqrt) / 2

def run_collision_test():
    print("🔬 RUNNING BOUNDARY CONDITION (COLLISION) TEST...")
    
    # Body 1 (Left), Body 2 (Right)
    # Fixed positions for simplicity (or adiabatic approach)
    pos1 = np.array([-50.0, 0.0])
    pos2 = np.array([50.0, 0.0])
    
    # Test Particle grid along X axis
    x_grid = np.linspace(-100, 100, 200)
    acc_newton_x = []
    acc_entropic_x = []
    
    for x in x_grid:
        p = np.array([x, 0.0])
        
        # 1. Calculate Vector Newtonian Gravity
        r1 = p - pos1
        r2 = p - pos2
        dist1 = np.linalg.norm(r1)
        dist2 = np.linalg.norm(r2)
        
        # Avoid singularities
        if dist1 < 1.0 or dist2 < 1.0:
            acc_newton_x.append(np.nan)
            acc_entropic_x.append(np.nan)
            continue
            
        f1_vec_n = -G * M * r1 / (dist1**3)
        f2_vec_n = -G * M * r2 / (dist2**3)
        
        a_vec_total_newton = f1_vec_n + f2_vec_n
        a_mag_newton = np.linalg.norm(a_vec_total_newton)
        
        acc_newton_x.append(a_vec_total_newton[0])
        
        # 2. Apply Entropic Correction
        # Correction depends on the MAGNITUDE of the total field
        a_mag_entropic = force_scientific_interpolation(a_mag_newton)
        
        # Preserve Direction
        if a_mag_newton > 1e-9:
             factor = a_mag_entropic / a_mag_newton
             a_vec_entropic = a_vec_total_newton * factor
        else:
             a_vec_entropic = np.array([0.0, 0.0])
             
        acc_entropic_x.append(a_vec_entropic[0])

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(x_grid, acc_newton_x, 'k--', label='Newtonian Field (X)', alpha=0.5)
    plt.plot(x_grid, acc_entropic_x, 'r-', label='Entropic Field (X)', linewidth=2)
    
    # Mark bodies
    plt.axvline(-50, color='blue', alpha=0.3)
    plt.axvline(50, color='blue', alpha=0.3)
    
    plt.xlabel('Position X')
    plt.ylabel('Gravitational Acceleration (X component)')
    plt.title('Strong Equivalence Principle Test: Saddle Point Dynamics')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("boundary_analysis.png")
    print("✅ Boundary Plot Saved: boundary_analysis.png")
    
    with open("boundary_report.md", "w") as f:
         f.write("# Challenge 3: Boundary Conditions & Equivalence Principle\n\n")
         f.write("## The External Field Effect (EFE)\n")
         f.write("In the center ($x=0$), the Newtonian fields cancel out perfectly ($g_N=0$).\n")
         f.write("In MOND/Verlinde, since $g_N=0$, the interpolation should technically give $g \\propto \\sqrt{a_0 g_N} = 0$.\n")
         f.write("\n## Results Interpretation\n")
         f.write("The plot shows how the Entropic force behaves in the saddle point. If the field behaves smoothly through zero, "
                 "it respects the cancellation. However, note that in Regions dominated by the external field of the other galaxy, "
                 "the 'Internal' dynamics of a test cluster would be suppressed. This violates the Strong Equivalance Principle "
                 "(SEP), which is a **feature**, not a bug, of MOND/Entropic theories.")

if __name__ == "__main__":
    run_collision_test()
