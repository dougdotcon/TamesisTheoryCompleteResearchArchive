import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure assets directory exists
output_dir = r"c:\Users\Douglas\Desktop\ToE\assets"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set style for academic look
plt.style.use('default')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12

# --- Figure 1: Entropy vs Time (The Landauer Limit) ---
def plot_entropy_compression():
    fig, ax = plt.subplots(figsize=(8, 6))
    
    t = np.linspace(0, 10, 100)
    
    # Class P: Polynomial Entropy Reduction (Manageable Heat)
    S_P = 100 * np.exp(-0.2 * t)
    
    # Class NP (hypothetical P=NP): Exponential Entropy Reduction (Massive Heat Spike)
    # Ideally it drops instantly or very fast
    S_NP = 100 * np.exp(-2.0 * t) 
    
    ax.plot(t, S_P, 'b-', linewidth=2, label='Class P (Polynomial Reversibility)')
    ax.plot(t, S_NP, 'r--', linewidth=2, label='Class NP solved in P (Violates Landauer Limit)')
    
    ax.set_title('Thermodynamic Cost of Computation', fontsize=14)
    ax.set_xlabel('Computational Time (steps)', fontsize=12)
    ax.set_ylabel('System Entropy $S(t)$ (bits)', fontsize=12)
    
    # Annotation for Landauer Limit
    ax.axhline(y=0, color='k', linewidth=1)
    ax.text(5, 10, r'Heat Dissipation $\Delta Q = T \Delta S$', fontsize=12, color='red')
    
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig1_entropy.png"), dpi=300)
    plt.close()
    print("Generated fig1_entropy.png")

# --- Figure 2: Energy Landscapes (Convex vs Glassy) ---
def plot_energy_landscapes():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    x = np.linspace(-5, 5, 200)
    
    # Plot 1: Class P (Convex / Funnel)
    y_p = x**2
    ax1.plot(x, y_p, 'b-', linewidth=2)
    ax1.set_title('Class P: Convex Landscape', fontsize=14)
    ax1.set_xlabel('Configuration Space', fontsize=12)
    ax1.set_ylabel('Energy $H(x)$', fontsize=12)
    ax1.text(0, 5, 'Global Minimum easy to find\n(Gradient Descent works)', ha='center')
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Plot 2: Class NP (Rugged / Spin Glass)
    # Create a rugged landscape using sin waves
    y_np = x**2 + 5*np.sin(3*x) + 2*np.cos(10*x)
    ax2.plot(x, y_np, 'r-', linewidth=2)
    ax2.set_title('Class NP: Glassy Landscape', fontsize=14)
    ax2.set_xlabel('Configuration Space', fontsize=12)
    ax2.set_ylabel('Energy $H(x)$', fontsize=12)
    ax2.text(0, 15, 'Many Local Minima\n(Traps Algorithms)', ha='center')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "fig2_landscape.png"), dpi=300)
    plt.close()
    print("Generated fig2_landscape.png")

if __name__ == "__main__":
    plot_entropy_compression()
    plot_energy_landscapes()
