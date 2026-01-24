"""
Visualizations for Topological Particle Spectrum
=================================================

Professional figures for Knot Theory Mass Scaling and Spin Topology.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

# Academic style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})


def plot_mass_scaling():
    """
    Exponential scaling of quark masses with knot complexity (ideal length).
    """
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    # Data from TAMESIS knot theory model
    # (Generation, Knot, N, Ideal Length L/D, Observed Mass MeV)
    quarks = [
        {'name': 'Up', 'gen': 1, 'knot': '3_1', 'L_D': 16.37, 'mass': 2.2},
        {'name': 'Charm', 'gen': 2, 'knot': '4_1', 'L_D': 21.17, 'mass': 1275},
        {'name': 'Top', 'gen': 3, 'knot': '5_1', 'L_D': 23.55, 'mass': 172760},
    ]
    
    L_D = np.array([q['L_D'] for q in quarks])
    mass = np.log([q['mass'] for q in quarks])  # Log mass
    names = [q['name'] for q in quarks]
    
    # Linear fit in log-space
    slope, intercept = np.polyfit(L_D, mass, 1)
    
    # Plot data points
    ax.scatter(L_D, mass, s=100, c='red', zorder=5)
    
    # Plot fit line
    x_fit = np.linspace(15, 25, 100)
    y_fit = slope * x_fit + intercept
    ax.plot(x_fit, y_fit, 'k--', lw=1.5, label=f'Fit: $M \\propto e^{{{slope:.2f}(L/D)}}$')
    
    # Annotate points
    for i, name in enumerate(names):
        ax.annotate(name, xy=(L_D[i], mass[i]), xytext=(L_D[i], mass[i]+0.5),
                    ha='center', fontweight='bold')
    
    ax.set_xlabel('Ideal Rope Length ($L/D$)')
    ax.set_ylabel('ln(Mass [MeV])')
    ax.set_title('Quark Mass vs Topological Complexity', fontweight='bold')
    ax.legend(loc='lower right', frameon=True, edgecolor='black')
    
    # Secondary axis for actual mass
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    yticks = np.log([2.2, 1275, 172760, 1e5])
    yticklabels = ['2.2', '1275', '173k', '']
    ax2.set_yticks(yticks)
    ax2.set_yticklabels(yticklabels)
    ax2.set_ylabel('Mass (MeV)')
    
    plt.tight_layout()
    plt.savefig('mass_scaling_plot.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: mass_scaling_plot.png")


def plot_knot_generations():
    """
    Schematic of the first three prime knots.
    """
    fig = plt.figure(figsize=(10, 4), facecolor='white')
    
    # Knot 3_1 (Trefoil)
    ax1 = fig.add_subplot(131, projection='3d')
    t = np.linspace(0, 2*np.pi, 100)
    x = np.sin(t) + 2*np.sin(2*t)
    y = np.cos(t) - 2*np.cos(2*t)
    z = -np.sin(3*t)
    ax1.plot(x, y, z, lw=2, c='blue')
    ax1.set_title('Gen 1: Trefoil ($3_1$)\nN=3 | u/d quarks', fontsize=10, fontweight='bold')
    ax1.axis('off')
    
    # Knot 4_1 (Figure Eight)
    ax2 = fig.add_subplot(132, projection='3d')
    t = np.linspace(0, 2*np.pi, 100)
    x = (2 + np.cos(2*t)) * np.cos(3*t)
    y = (2 + np.cos(2*t)) * np.sin(3*t)
    z = np.sin(4*t)
    ax2.plot(x, y, z, lw=2, c='green')
    ax2.set_title('Gen 2: Figure-8 ($4_1$)\nN=4 | c/s quarks', fontsize=10, fontweight='bold')
    ax2.axis('off')
    
    # Knot 5_1 (Cinquefoil)
    ax3 = fig.add_subplot(133, projection='3d')
    t = np.linspace(0, 2*np.pi, 100)
    x = np.cos(2*t) * (3 + np.cos(5*t))
    y = np.sin(2*t) * (3 + np.cos(5*t))
    z = np.sin(5*t)
    ax3.plot(x, y, z, lw=2, c='red')
    ax3.set_title('Gen 3: Cinquefoil ($5_1$)\nN=5 | t/b quarks', fontsize=10, fontweight='bold')
    ax3.axis('off')
    
    plt.tight_layout()
    plt.savefig('knot_generations.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: knot_generations.png")


def plot_spin_topology():
    """
    Dirac belt trick / Moebius strip concept for spin-1/2.
    """
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    
    # Draw simple schematic of rotation
    angle = np.linspace(0, 4*np.pi, 200)
    phase = np.cos(angle/2)  # Spin-1/2 behavior (4pi periodicity)
    
    ax.plot(angle, phase, 'b-', lw=2, label='Spinor Wavefunction $\\Psi(\\theta)$')
    
    # Mark 2pi and 4pi
    ax.axvline(2*np.pi, color='red', ls='--', lw=1)
    ax.axvline(4*np.pi, color='green', ls='--', lw=1)
    
    ax.text(2*np.pi + 0.2, -0.9, '360° rotation\n$\\Psi \\to -\\Psi$', color='red', fontsize=9)
    ax.text(4*np.pi - 3.5, 0.9, '720° rotation\n$\\Psi \\to +\\Psi$', color='green', fontsize=9)
    
    ax.set_xlabel('Rotation Angle (radians)')
    ax.set_ylabel('Wavefunction Amplitude')
    ax.set_title('Topological Origin of Spin-1/2', fontweight='bold')
    ax.legend(loc='upper right', frameon=True, edgecolor='black')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spin_topology.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: spin_topology.png")


if __name__ == "__main__":
    print("Generating topological particle visualizations...")
    print()
    
    plot_mass_scaling()
    plot_knot_generations()
    plot_spin_topology()
    
    print()
    print("All particle figures generated!")
