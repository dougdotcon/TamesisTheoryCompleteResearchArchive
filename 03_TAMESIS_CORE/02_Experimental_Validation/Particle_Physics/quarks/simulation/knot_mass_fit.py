import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def knot_mass_fit():
    """
    Tests the hypothesis that Quark Masses scale with the Topological Complexity 
    (Ideal Rope Length) of their corresponding Prime Knots.
    
    Mapping Hypothesis:
    - Generation 1 (Up/Down) -> Trefoil (3_1)
    - Generation 2 (Charm/Strange) -> Figure-8 (4_1)
    - Generation 3 (Top/Bottom) -> Cinquefoil (5_1)
    """
    
    # 1. Topological Data (Ideal Rope Length L/D)
    # Source: Pieranski, S. (1998). "Ideal Knots".
    knots = ['Trefoil (3_1)', 'Figure-8 (4_1)', 'Cinquefoil (5_1)']
    generations = [1, 2, 3]
    
    # Ideal Lengths (L/D)
    ideal_lengths = np.array([16.37, 21.17, 23.55])
    
    # Crossing Numbers (Alternative metric)
    crossings = np.array([3, 4, 5])
    
    # 2. Physical Data (Quark Masses in MeV)
    # Using UP-TYPE Quarks (Up, Charm, Top) - The most dramatic hierarchy
    # Up: ~2.2 MeV
    # Charm: ~1275 MeV
    # Top: ~173000 MeV
    masses_up_type = np.array([2.2, 1275, 173000])
    
    # Using DOWN-TYPE Quarks (Down, Strange, Bottom)
    # Down: ~4.7 MeV
    # Strange: ~95 MeV
    # Bottom: ~4180 MeV
    masses_down_type = np.array([4.7, 95, 4180])
    
    # 3. The Hypothesis Model: M = M0 * exp(alpha * Topological_Complexity)
    # Why? Local Knot Energy ~ Length. Bolztmann probability ~ exp(-E/kT). 
    # But mass is energy. Maybe M ~ exp(Length)?
    
    def exponential_model(x, a, b):
        return a * np.exp(b * x)
    
    # Fit for Up-Type (Linear fit on Log Mass)
    # log(M) = log(a) + b * L
    # y = C + b*x
    coeffs_up = np.polyfit(ideal_lengths, np.log(masses_up_type), 1)
    b_up = coeffs_up[0]
    a_up = np.exp(coeffs_up[1])
    popt_up = [a_up, b_up]
    
    # Fit for Down-Type
    coeffs_down = np.polyfit(ideal_lengths, np.log(masses_down_type), 1)
    b_down = coeffs_down[0]
    a_down = np.exp(coeffs_down[1])
    popt_down = [a_down, b_down]
    
    # Generate curves
    x_range = np.linspace(15, 25, 100)
    y_pred_up = a_up * np.exp(b_up * x_range)
    y_pred_down = a_down * np.exp(b_down * x_range)
    
    # 4. Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Up-Type
    ax.semilogy(ideal_lengths, masses_up_type, 'ro', markersize=10, label='Up-Type Quarks (Data)')
    ax.semilogy(x_range, y_pred_up, 'r--', alpha=0.5, label=f'Fit: M ~ exp({popt_up[1]:.2f} * L)')
    
    # Plot Down-Type
    ax.semilogy(ideal_lengths, masses_down_type, 'bo', markersize=10, label='Down-Type Quarks (Data)')
    ax.semilogy(x_range, y_pred_down, 'b--', alpha=0.5, label=f'Fit: M ~ exp({popt_down[1]:.2f} * L)')
    
    # Annotate Knots
    for i, txt in enumerate(knots):
        ax.annotate(txt, (ideal_lengths[i], masses_up_type[i]), xytext=(5, 5), textcoords='offset points', color='r')
        ax.annotate(txt, (ideal_lengths[i], masses_down_type[i]), xytext=(5, -15), textcoords='offset points', color='b')

    ax.set_title("Topological Mass Scaling: Quark Masses vs Knot Rope Length", fontsize=14)
    ax.set_xlabel("Ideal Knot Rope Length (L/D)", fontsize=12)
    ax.set_ylabel("Mass (MeV) - Log Scale", fontsize=12)
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.legend()
    
    # Save
    plt.tight_layout()
    plt.savefig('../analysis/knot_mass_scaling.png')
    print(f"Saved plot. Fit Parameters (Up-Type): a={popt_up[0]:.2e}, b={popt_up[1]:.2f}")
    print(f"Saved plot. Fit Parameters (Down-Type): a={popt_down[0]:.2e}, b={popt_down[1]:.2f}")

if __name__ == "__main__":
    knot_mass_fit()
