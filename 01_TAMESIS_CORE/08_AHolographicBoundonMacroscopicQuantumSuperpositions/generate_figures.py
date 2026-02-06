"""
Ghost Paper - Visualization Generator
Creates figures and GIFs to illustrate the manuscript
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.animation as animation
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path("figures")
OUTPUT_DIR.mkdir(exist_ok=True)

# Style configuration
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'legend.fontsize': 10,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# Physical constants
M_C = 2.2e-14  # Critical mass in kg
M_PLANCK = 2.176e-8  # Planck mass in kg


def fig1_step_vs_exponential():
    """
    Figure 1: The key prediction - step function vs exponential decay
    Compares this work with CSL models
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Mass range (log scale)
    M = np.logspace(-17, -11, 1000)
    
    # This work: Step function at M_c
    V_step = np.where(M < M_C, 1.0, 0.0)
    # Add small transition width for visualization
    transition_width = M_C * 0.02
    V_step_smooth = 1 / (1 + np.exp((M - M_C) / (transition_width)))
    
    # CSL model: Exponential decay
    M_csl = 1e-14  # CSL characteristic mass
    lambda_csl = 1e-16  # CSL rate
    V_csl = np.exp(-(M / M_csl) ** 2 * lambda_csl * 1e12)
    
    # Environmental decoherence (gradual)
    V_env = np.exp(-M / (5e-15))
    
    # Plot
    ax.semilogx(M, V_step_smooth, 'b-', linewidth=3, label='This work (holographic limit)')
    ax.semilogx(M, V_csl, 'r--', linewidth=2.5, label='CSL model (exponential)')
    ax.semilogx(M, V_env, 'g:', linewidth=2, label='Environmental decoherence')
    
    # Mark M_c
    ax.axvline(M_C, color='blue', linestyle=':', alpha=0.7, linewidth=1.5)
    ax.annotate(r'$M_c \approx 2 \times 10^{-14}$ kg', 
                xy=(M_C, 0.5), xytext=(M_C * 5, 0.6),
                fontsize=11, color='blue',
                arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7))
    
    # Labels
    ax.set_xlabel('Mass $M$ (kg)', fontsize=12)
    ax.set_ylabel('Interference Visibility $V$', fontsize=12)
    ax.set_title('Prediction: Discontinuous vs Continuous Collapse', fontsize=14, fontweight='bold')
    ax.set_xlim(1e-17, 1e-11)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc='upper right', framealpha=0.95)
    
    # Add quantum/classical regions
    ax.fill_between([1e-17, M_C], 0, 1.1, alpha=0.1, color='blue', label='Quantum regime')
    ax.fill_between([M_C, 1e-11], 0, 1.1, alpha=0.1, color='red', label='Classical regime')
    ax.text(1e-16, 1.02, 'QUANTUM', fontsize=10, color='blue', fontweight='bold')
    ax.text(1e-12, 1.02, 'CLASSICAL', fontsize=10, color='red', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig1_step_vs_exponential.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig1_step_vs_exponential.svg', bbox_inches='tight')
    print("✓ Figure 1: Step vs Exponential saved")
    plt.close()


def fig2_entropy_scaling():
    """
    Figure 2: Entropy scaling - S_required vs S_max
    Shows the crossing point at M_c
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Mass range
    M = np.logspace(-18, -10, 500)
    
    # S_required ~ M (linear in mass)
    mu = 1e-15  # characteristic scale
    S_required = M / mu
    
    # S_max ~ M^(2/3) (holographic bound)
    S_max = (M / mu) ** (2/3) * 10  # scaled for visualization
    
    # Normalize both to cross at M_c
    norm_factor = (M_C / mu) / ((M_C / mu) ** (2/3) * 10)
    S_max_normalized = S_max * norm_factor
    
    # Plot
    ax.loglog(M, S_required, 'b-', linewidth=2.5, label=r'$S_{required} \propto M$ (superposition)')
    ax.loglog(M, S_max_normalized, 'r-', linewidth=2.5, label=r'$S_{max} \propto M^{2/3}$ (holographic)')
    
    # Mark crossing point
    ax.axvline(M_C, color='purple', linestyle='--', alpha=0.7, linewidth=1.5)
    ax.plot(M_C, M_C / mu, 'ko', markersize=12, zorder=5)
    ax.annotate(r'Crossing at $M_c$', 
                xy=(M_C, M_C / mu), xytext=(M_C * 10, M_C / mu * 3),
                fontsize=11, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black'))
    
    # Shade forbidden region
    mask = M > M_C
    ax.fill_between(M[mask], S_max_normalized[mask], S_required[mask], 
                    alpha=0.3, color='red', label='Forbidden region')
    
    # Labels
    ax.set_xlabel('Mass $M$ (kg)', fontsize=12)
    ax.set_ylabel('Entropy $S / k_B$', fontsize=12)
    ax.set_title('Entropy Scaling: Required vs Available', fontsize=14, fontweight='bold')
    ax.set_xlim(1e-18, 1e-10)
    ax.legend(loc='upper left', framealpha=0.95)
    
    # Add text annotations
    ax.text(1e-17, 1e4, 'Superposition\npossible', fontsize=10, color='blue', 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax.text(1e-11, 1e4, 'Superposition\nforbidden', fontsize=10, color='red',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig2_entropy_scaling.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig2_entropy_scaling.svg', bbox_inches='tight')
    print("✓ Figure 2: Entropy Scaling saved")
    plt.close()


def fig3_mass_comparison():
    """
    Figure 3: Mass scale comparison with other theories
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Mass scales (in kg)
    masses = {
        'Electron': 9.1e-31,
        'Proton': 1.67e-27,
        'C60 molecule': 1.2e-24,
        'Largest QM\nobject tested': 2.5e-23,
        'Penrose\nthreshold': 1e-17,
        'This work\n$M_c$': 2.2e-14,
        'CSL\nthreshold': 1e-11,
        'Planck\nmass': 2.2e-8,
    }
    
    positions = np.arange(len(masses))
    colors = ['gray', 'gray', 'green', 'green', 'orange', 'blue', 'red', 'purple']
    
    # Plot
    for i, (name, mass) in enumerate(masses.items()):
        ax.barh(i, np.log10(mass), color=colors[i], alpha=0.7, height=0.6)
        ax.text(np.log10(mass) + 0.5, i, f'{mass:.0e} kg', 
                va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(positions)
    ax.set_yticklabels(masses.keys(), fontsize=10)
    ax.set_xlabel('log₁₀(Mass / kg)', fontsize=12)
    ax.set_title('Mass Scale Comparison: Quantum-Classical Boundary', fontsize=14, fontweight='bold')
    ax.set_xlim(-32, 0)
    
    # Add vertical line for M_c
    ax.axvline(np.log10(M_C), color='blue', linestyle='--', linewidth=2, alpha=0.7)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', alpha=0.7, label='Experimentally verified QM'),
        Patch(facecolor='blue', alpha=0.7, label='This work prediction'),
        Patch(facecolor='orange', alpha=0.7, label='Penrose prediction'),
        Patch(facecolor='red', alpha=0.7, label='CSL prediction'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig3_mass_comparison.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig3_mass_comparison.svg', bbox_inches='tight')
    print("✓ Figure 3: Mass Comparison saved")
    plt.close()


def fig4_experimental_protocol():
    """
    Figure 4: Schematic of experimental protocol
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(6, 5.5, 'Talbot-Lau Interferometry: Experimental Protocol', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Components
    components = [
        (1, 3, 'Particle\nSource', 'lightblue'),
        (3, 3, 'Grating 1', 'gray'),
        (5, 3, 'Free\nEvolution', 'white'),
        (7, 3, 'Grating 2', 'gray'),
        (9, 3, 'Grating 3', 'gray'),
        (11, 3, 'Detector', 'lightgreen'),
    ]
    
    for x, y, label, color in components:
        rect = FancyBboxPatch((x-0.5, y-0.5), 1, 1, 
                               boxstyle="round,pad=0.05", 
                               facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Arrows
    for i in range(5):
        ax.annotate('', xy=(1.5 + i*2, 3), xytext=(0.7 + i*2, 3),
                   arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    
    # Mass sweep annotation
    ax.annotate('Mass sweep:\n$10^{-15}$ → $10^{-13}$ kg', 
                xy=(1, 2), fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Observable
    ax.annotate('Observable:\nFringe visibility $V(M)$', 
                xy=(11, 2), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # Expected result
    ax.text(6, 0.8, 'Expected: Sharp visibility drop at $M_c \\approx 2 \\times 10^{-14}$ kg',
            ha='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    plt.savefig(OUTPUT_DIR / 'fig4_experimental_protocol.png', dpi=150, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig4_experimental_protocol.svg', bbox_inches='tight')
    print("✓ Figure 4: Experimental Protocol saved")
    plt.close()


def gif_collapse_transition():
    """
    GIF: Animated transition from quantum to classical at M_c
    Shows interference pattern disappearing
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Mass values to animate through
    masses = np.linspace(0.5e-14, 4e-14, 60)
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        
        M = masses[frame]
        
        # Visibility calculation (step function)
        if M < M_C:
            V = 1.0
        else:
            V = max(0, 1 - (M - M_C) / (0.05 * M_C))
        V = max(0, V)
        
        # Left plot: Interference pattern
        x = np.linspace(-5, 5, 500)
        pattern = 1 + V * np.cos(2 * np.pi * x)
        ax1.fill_between(x, 0, pattern, alpha=0.7, color='blue')
        ax1.set_xlim(-5, 5)
        ax1.set_ylim(0, 2.5)
        ax1.set_xlabel('Position (a.u.)', fontsize=11)
        ax1.set_ylabel('Intensity', fontsize=11)
        ax1.set_title(f'Interference Pattern\nMass = {M:.2e} kg', fontsize=12)
        
        # Add quantum/classical indicator
        if M < M_C:
            ax1.text(0, 2.2, 'QUANTUM', ha='center', fontsize=14, fontweight='bold', color='blue')
        else:
            ax1.text(0, 2.2, 'CLASSICAL', ha='center', fontsize=14, fontweight='bold', color='red')
        
        # Right plot: Visibility vs Mass
        M_range = np.logspace(-15, -12, 200)
        V_range = np.where(M_range < M_C, 1.0, 0.0)
        
        ax2.semilogx(M_range, V_range, 'b-', linewidth=2, alpha=0.5)
        ax2.axvline(M_C, color='red', linestyle='--', alpha=0.7, label=r'$M_c$')
        ax2.plot(M, V, 'ro', markersize=15, zorder=5)
        ax2.set_xlabel('Mass (kg)', fontsize=11)
        ax2.set_ylabel('Visibility $V$', fontsize=11)
        ax2.set_title('Visibility vs Mass', fontsize=12)
        ax2.set_xlim(1e-15, 1e-12)
        ax2.set_ylim(-0.1, 1.2)
        ax2.legend(loc='upper right')
        
        plt.tight_layout()
        return ax1, ax2
    
    ani = animation.FuncAnimation(fig, update, frames=len(masses), interval=100)
    ani.save(OUTPUT_DIR / 'gif_collapse_transition.gif', writer='pillow', fps=10)
    print("✓ GIF: Collapse Transition saved")
    plt.close()


def gif_holographic_saturation():
    """
    GIF: Animated visualization of holographic saturation
    Shows information filling up the boundary
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    frames = 60
    
    def update(frame):
        ax.clear()
        
        # Progress through mass range
        progress = frame / (frames - 1)
        M = 10 ** (-16 + 4 * progress)  # From 10^-16 to 10^-12 kg
        
        # Draw the "holographic boundary" (circle)
        theta = np.linspace(0, 2*np.pi, 100)
        R = 1.5
        ax.plot(R * np.cos(theta), R * np.sin(theta), 'k-', linewidth=3)
        
        # Calculate fill levels
        S_required = M / 1e-15  # Arbitrary normalization
        S_max = (M / 1e-15) ** (2/3) * 10
        
        # Normalize to fit in visualization
        fill_required = min(1, S_required / 100)
        fill_max = min(1, S_max / 100)
        
        # Fill boundary (holographic capacity)
        fill_angle = 2 * np.pi * fill_max
        theta_fill = np.linspace(0, fill_angle, 100)
        ax.fill(R * np.cos(theta_fill), R * np.sin(theta_fill), 
                color='lightblue', alpha=0.5, label='Available (holographic)')
        
        # Fill required (superposition needs)
        req_angle = 2 * np.pi * fill_required
        theta_req = np.linspace(0, req_angle, 100)
        if M > M_C:
            color = 'red'
            ax.fill(1.3 * np.cos(theta_req), 1.3 * np.sin(theta_req), 
                    color=color, alpha=0.4, label='Required (overflow!)')
        else:
            color = 'green'
            ax.fill(1.3 * np.cos(theta_req), 1.3 * np.sin(theta_req), 
                    color=color, alpha=0.4, label='Required')
        
        # Center text
        ax.text(0, 0, f'M = {M:.1e} kg', ha='center', va='center', 
                fontsize=14, fontweight='bold')
        
        # Status indicator
        if M < M_C:
            status = "COHERENT"
            status_color = 'green'
        else:
            status = "COLLAPSED"
            status_color = 'red'
        
        ax.text(0, -0.5, status, ha='center', va='center', 
                fontsize=16, fontweight='bold', color=status_color)
        
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Holographic Saturation', fontsize=14, fontweight='bold')
        ax.legend(loc='upper right', fontsize=9)
        
        return ax,
    
    ani = animation.FuncAnimation(fig, update, frames=frames, interval=100)
    ani.save(OUTPUT_DIR / 'gif_holographic_saturation.gif', writer='pillow', fps=10)
    print("✓ GIF: Holographic Saturation saved")
    plt.close()


def fig5_collapse_static():
    """
    Figure 5 (Static): Collapse transition snapshots
    Three panels: Quantum (M < Mc), Critical (M ~ Mc), Classical (M > Mc)
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Masses: Deep quantum, Critical, Deep classical
    masses = [0.5 * M_C, M_C, 1.5 * M_C]
    titles = ['Quantum ($M < M_c$)\nFull Superposition', 
              'Critical ($M \\approx M_c$)\nPhase Transition', 
              'Classical ($M > M_c$)\nCollapse']
    
    for i, ax in enumerate(axes):
        M = masses[i]
        
        # Visibility calculation
        if M < M_C:
            V = 1.0
        elif M > 1.05 * M_C:
            V = 0.0
        else:
            V = 0.5 # Sharp transition snapshot
            
        # Plot interference pattern
        x = np.linspace(-5, 5, 500)
        pattern = 1 + V * np.cos(2 * np.pi * x)
        
        # Color coding
        if i == 0: color = 'blue'
        elif i == 1: color = 'purple'
        else: color = 'red'
        
        ax.fill_between(x, 0, pattern, alpha=0.6, color=color)
        ax.plot(x, pattern, color=color, linewidth=2)
        
        ax.set_xlim(-5, 5)
        ax.set_ylim(0, 2.2)
        ax.set_xlabel('Detector Position (a.u.)', fontsize=11)
        if i == 0:
            ax.set_ylabel('Intensity', fontsize=11)
        ax.set_title(titles[i], fontsize=12, fontweight='bold')
        
        # Add Visibility text
        ax.text(0, 2.05, f'Visibility $V \\approx {V:.1f}$', 
                ha='center', fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'fig5_collapse_static.png', dpi=300, bbox_inches='tight')
    plt.savefig(OUTPUT_DIR / 'fig5_collapse_static.svg', bbox_inches='tight')
    print("✓ Figure 5: Static Collapse Panels saved")
    plt.close()


def main():
    print("=" * 50)
    print("Ghost Paper - Generating Visualizations")
    print("=" * 50)
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print()
    
    # Generate all figures
    fig1_step_vs_exponential()
    fig2_entropy_scaling()
    fig3_mass_comparison()
    fig4_experimental_protocol()
    fig5_collapse_static()

    
    # Generate GIFs
    gif_collapse_transition()
    gif_holographic_saturation()
    
    print()
    print("=" * 50)
    print("All visualizations generated successfully!")
    print(f"Files saved to: {OUTPUT_DIR.absolute()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
