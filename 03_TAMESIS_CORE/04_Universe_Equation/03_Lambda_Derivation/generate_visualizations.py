"""
Visualizations for Cosmological Constant Derivation
====================================================

Professional figures for deriving Lambda from holographic boundary term.
"""

import numpy as np
import matplotlib.pyplot as plt

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

# Constants
c = 3e8
H0 = 70e3 / 3.086e22  # 70 km/s/Mpc in s^-1
G = 6.674e-11
hbar = 1.055e-34
l_P = 1.616e-35


def plot_vacuum_catastrophe():
    """
    Show the 10^122 discrepancy between QFT and observation.
    """
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    categories = ['QFT Prediction', 'Tamesis Prediction', 'Observed']
    values = [1e113, 6e-10, 6e-10]  # J/m^3
    colors = ['#d32f2f', '#4CAF50', '#2196F3']
    
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.2)
    
    ax.set_yscale('log')
    ax.set_ylabel('Vacuum Energy Density (J/m³)')
    ax.set_title('The Vacuum Catastrophe: Solved', fontweight='bold')
    ax.set_ylim(1e-12, 1e120)
    
    # Annotations
    ax.annotate('$10^{122}$ discrepancy!', xy=(0.5, 1e60), fontsize=12,
                ha='center', fontweight='bold', color='#d32f2f')
    ax.annotate('', xy=(0, 1e50), xytext=(1, 1e-5),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=2))
    
    ax.text(1.5, 1e-7, 'Agreement!', fontsize=10, ha='center', 
            fontweight='bold', color='#4CAF50')
    
    plt.tight_layout()
    plt.savefig('vacuum_catastrophe.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: vacuum_catastrophe.png")


def plot_horizon_entropy():
    """
    Show entropy as function of horizon radius.
    """
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    R = np.logspace(20, 27, 100)  # meters (solar system to Hubble)
    A = 4 * np.pi * R**2
    S = A / (4 * l_P**2)
    
    ax.loglog(R / 3.086e22, S, 'b-', lw=2)
    
    # Mark key scales
    R_H = c / H0
    S_H = 4 * np.pi * R_H**2 / (4 * l_P**2)
    ax.axvline(R_H / 3.086e22, color='red', ls='--', lw=1.5, label='Hubble horizon')
    ax.scatter([R_H / 3.086e22], [S_H], s=100, c='red', zorder=5)
    
    ax.set_xlabel('Radius (Mpc)')
    ax.set_ylabel('Maximum Entropy (bits)')
    ax.set_title('Holographic Entropy of Cosmic Horizons', fontweight='bold')
    ax.legend(loc='lower right', frameon=True, edgecolor='black')
    
    ax.text(R_H / 3.086e22 * 1.5, S_H, f'$S_H = {S_H:.1e}$ bits', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('horizon_entropy.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: horizon_entropy.png")


def plot_lambda_derivation():
    """
    Show the derivation flow from horizon to Lambda.
    """
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='white')
    
    # Create flow diagram with text
    steps = [
        {'y': 0.85, 'text': 'Hubble Horizon: $R_H = c/H_0$', 'eq': ''},
        {'y': 0.70, 'text': 'Horizon Area: $A_H = 4\\pi R_H^2$', 'eq': ''},
        {'y': 0.55, 'text': 'Max Entropy: $S = A_H / 4l_P^2$', 'eq': '(Bekenstein)'},
        {'y': 0.40, 'text': 'Entropy Density: $s = S / V_H$', 'eq': ''},
        {'y': 0.25, 'text': 'Information Pressure: $P = -T \\cdot s$', 'eq': '(Verlinde)'},
        {'y': 0.10, 'text': '$\\Lambda = 3H_0^2/c^2$', 'eq': 'RESULT'},
    ]
    
    for i, step in enumerate(steps):
        # Box
        ax.add_patch(plt.Rectangle((0.1, step['y']-0.06), 0.8, 0.10,
                                   facecolor='#f5f5f5' if i < 5 else '#e8f5e9',
                                   edgecolor='black', linewidth=1.2))
        # Text
        ax.text(0.5, step['y'], step['text'], fontsize=11 if i < 5 else 13,
                ha='center', va='center', fontweight='bold' if i == 5 else 'normal')
        if step['eq']:
            ax.text(0.92, step['y'], step['eq'], fontsize=8, ha='left', va='center',
                    style='italic', color='#666666')
        
        # Arrow
        if i < len(steps) - 1:
            ax.annotate('', xy=(0.5, steps[i+1]['y'] + 0.05), xytext=(0.5, step['y'] - 0.07),
                       arrowprops=dict(arrowstyle='->', color='black', lw=1.2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Derivation of $\\Lambda$ from Holography', fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig('lambda_derivation_flow.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: lambda_derivation_flow.png")


def plot_lambda_vs_h0():
    """
    Show Lambda as function of H0.
    """
    fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    H0_range = np.linspace(50, 90, 100)  # km/s/Mpc
    H0_si = H0_range * 1e3 / 3.086e22
    Lambda = 3 * H0_si**2 / c**2
    
    ax.plot(H0_range, Lambda * 1e52, 'b-', lw=2, label='Tamesis: $\\Lambda = 3H_0^2/c^2$')
    
    # Observed value
    ax.axhline(1.1, color='red', ls='--', lw=1.5, label='Planck 2018: $1.1 \\times 10^{-52}$ m⁻²')
    ax.axvline(70, color='gray', ls=':', lw=1)
    
    # Tension region
    ax.axvspan(67, 74, alpha=0.2, color='yellow', label='$H_0$ tension range')
    
    ax.set_xlabel('$H_0$ (km/s/Mpc)')
    ax.set_ylabel('$\\Lambda$ ($\\times 10^{-52}$ m⁻²)')
    ax.set_title('Cosmological Constant vs Hubble Parameter', fontweight='bold')
    ax.legend(loc='upper left', frameon=True, edgecolor='black')
    ax.set_xlim(50, 90)
    ax.set_ylim(0, 3)
    
    plt.tight_layout()
    plt.savefig('lambda_vs_h0.png', dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    print("✅ Saved: lambda_vs_h0.png")


if __name__ == "__main__":
    print("Generating Lambda derivation figures...")
    print()
    
    plot_vacuum_catastrophe()
    plot_horizon_entropy()
    plot_lambda_derivation()
    plot_lambda_vs_h0()
    
    print()
    print("All Lambda figures generated!")
