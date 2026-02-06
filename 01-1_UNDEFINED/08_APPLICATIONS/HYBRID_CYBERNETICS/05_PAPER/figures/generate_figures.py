"""
Hybrid Cybernetics Figure Generator
Generates scientific diagrams for the Anchor Paper.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_architecture():
    """Generates Fig 1: The Hybrid Control Loop"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    # Styles
    box_props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=1.5)
    arrow_props = dict(facecolor='black', width=0.5, headwidth=2, headlength=3)

    # Nodes
    # Input
    ax.text(0.5, 2, "Input (x)\n(Problem)", ha='center', va='center', fontsize=10)
    
    # Machine (M)
    rect_m = patches.FancyBboxPatch((2, 1), 2, 2, boxstyle="round,pad=0.1", fc='#e0f7fa', ec='black')
    ax.add_patch(rect_m)
    ax.text(3, 2, "Machine ($O_M$)\nHigh Bandwidth\nStochastic", ha='center', va='center', fontsize=10)

    # Filter (F)
    rect_f = patches.FancyBboxPatch((5, 1.25), 1.5, 1.5, boxstyle="round,pad=0.1", fc='#fff3e0', ec='black')
    ax.add_patch(rect_f)
    ax.text(5.75, 2, "Filter ($\mathcal{F}$)\nBandwidth\nLimiter", ha='center', va='center', fontsize=9)

    # Human (H)
    rect_h = patches.FancyBboxPatch((7.5, 1), 2, 2, boxstyle="round,pad=0.1", fc='#e8f5e9', ec='black')
    ax.add_patch(rect_h)
    ax.text(8.5, 2, "Human ($O_H$)\nLow Bandwidth\nSemantic", ha='center', va='center', fontsize=10)
    
    # Output
    ax.text(10.5, 2, "Output (y)\n(Truth)", ha='center', va='center', fontsize=10)

    # Arrows (Fluxes)
    # x -> M
    ax.annotate("", xy=(2, 2), xytext=(0.8, 2), arrowprops=dict(arrowstyle="->", lw=2))
    
    # M -> F (Supercritical Flux)
    ax.annotate("", xy=(5, 2), xytext=(4, 2), arrowprops=dict(arrowstyle="->", lw=4, color='red'))
    ax.text(4.5, 2.5, r"Flux $\Phi \gg C_{bio}$", ha='center', color='red', fontsize=8)

    # F -> H (Critical Flux)
    ax.annotate("", xy=(7.5, 2), xytext=(6.5, 2), arrowprops=dict(arrowstyle="->", lw=1.5, color='green'))
    ax.text(7, 2.5, r"Flux $\Phi \leq C_{bio}$", ha='center', color='green', fontsize=8)


    # H -> y
    ax.annotate("", xy=(10.5, 2), xytext=(9.5, 2), arrowprops=dict(arrowstyle="->", lw=1.5))

    plt.tight_layout()
    plt.savefig('fig1_architecture.png', dpi=300, bbox_inches='tight')
    print("Generated Fig 1.")

def draw_stability():
    """Generates Fig 2: Thermodynamic Stability Zones"""
    fig, ax = plt.subplots(figsize=(8, 6))

    # X-axis: Input Flux (Rate)
    x = np.linspace(0, 10, 100)
    c_bio = 5 # Critical Threshold
    
    # Y-axis: Error Variance (Sigma^2) over long T
    # Regime 1: Grounding (Linear small error due to fatigue)
    y_stable = 0.1 * x 
    # Regime 2: Saturation (Exponential Divergence)
    # We model a phase transition at C_bio
    y_divergent = np.where(x <= c_bio, 0.1 * x, 0.5 + np.exp(0.8 * (x - c_bio)) - 1)

    ax.plot(x, y_divergent, color='black', linewidth=2)
    
    # Zones
    ax.axvline(c_bio, color='red', linestyle='--', linewidth=1.5, label='$C_{bio}$ (Capacity Limit)')
    
    # Fill Stable Zone
    ax.fill_between(x, 0, 10, where=(x <= c_bio), color='green', alpha=0.1)
    ax.text(2.5, 8, "STABLE REGIONE\n(Grounding)", ha='center', color='darkgreen', fontsize=12, fontweight='bold')
    
    # Fill Unstable Zone
    ax.fill_between(x, 0, 10, where=(x > c_bio), color='red', alpha=0.1)
    ax.text(7.5, 8, "UNSTABLE REGIME\n(Hallucination\nAmplification)", ha='center', color='darkred', fontsize=12, fontweight='bold')

    ax.set_title("Phase Transition in Hybrid Cognitive Systems", fontsize=14)
    ax.set_xlabel("Input Information Flux ($\Phi_{in}$)", fontsize=12)
    ax.set_ylabel("Long-term Error Variance ($\sigma^2$)", fontsize=12)
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fig2_stability.png', dpi=300)
    print("Generated Fig 2.")

if __name__ == "__main__":
    draw_architecture()
    draw_stability()
