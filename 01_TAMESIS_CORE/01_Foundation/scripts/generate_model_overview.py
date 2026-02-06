"""
TAMESIS Model Overview - Academic Version
Clean hierarchical flowchart suitable for scientific publications
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Set up the figure - white background for academic papers
fig, ax = plt.subplots(1, 1, figsize=(14, 16), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 14)
ax.set_ylim(0, 16)
ax.axis('off')

# Colors - professional palette
PRIMARY = '#2C3E50'      # Dark blue-gray
SECONDARY = '#34495E'    # Lighter blue-gray
ACCENT = '#E74C3C'       # Red accent
SUCCESS = '#27AE60'      # Green for verified
INFO = '#3498DB'         # Blue for info
GOLD = '#F39C12'         # Gold for main result

def draw_box(ax, x, y, w, h, title, content, result, color=PRIMARY, 
             title_color='white', bg_color='#ECF0F1'):
    """Draw a professional rectangular box"""
    # Main box
    box = FancyBboxPatch((x - w/2, y - h/2), w, h, 
                          boxstyle="round,pad=0.02,rounding_size=0.1",
                          facecolor=bg_color, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    
    # Title bar
    title_bar = FancyBboxPatch((x - w/2, y + h/2 - 0.4), w, 0.4,
                                boxstyle="round,pad=0.02,rounding_size=0.1",
                                facecolor=color, edgecolor=color, linewidth=0)
    ax.add_patch(title_bar)
    
    ax.text(x, y + h/2 - 0.2, title, fontsize=10, fontweight='bold', 
            color=title_color, ha='center', va='center')
    ax.text(x, y, content, fontsize=9, color=PRIMARY, ha='center', va='center')
    ax.text(x, y - h/2 + 0.25, result, fontsize=8, color=SUCCESS, 
            ha='center', va='center', fontweight='bold')

def draw_arrow(ax, x1, y1, x2, y2, color=PRIMARY):
    """Draw a connecting arrow"""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# === TITLE ===
ax.text(7, 15.3, 'TAMESIS Framework: Unified Derivation Hierarchy', 
        fontsize=16, fontweight='bold', color=PRIMARY, ha='center')
ax.text(7, 14.8, 'Theory of Everything - Derivation Flow', 
        fontsize=11, color=SECONDARY, ha='center', style='italic')

# === LEVEL 0: FUNDAMENTAL PARAMETER ===
omega_box = FancyBboxPatch((4.5, 13), 5, 1.2, boxstyle="round,pad=0.03",
                            facecolor=GOLD, edgecolor=PRIMARY, linewidth=2)
ax.add_patch(omega_box)
ax.text(7, 13.7, 'FUNDAMENTAL PARAMETER', fontsize=10, fontweight='bold', 
        color='white', ha='center')
ax.text(7, 13.3, r'$\Omega = 117.038$', fontsize=14, fontweight='bold', 
        color='white', ha='center')

# === LEVEL 1: PRIMARY DERIVATIONS ===
ax.text(7, 12, 'PRIMARY DERIVATIONS', fontsize=9, color=SECONDARY, 
        ha='center', fontweight='bold')
ax.plot([2, 12], [11.8, 11.8], color=SECONDARY, linewidth=0.5, linestyle='--')

# Arrows from Omega
draw_arrow(ax, 5.5, 13, 3.5, 11.2)
draw_arrow(ax, 7, 13, 7, 11.2)
draw_arrow(ax, 8.5, 13, 10.5, 11.2)

# Box 1: Electron Mass
draw_box(ax, 3.5, 10.5, 3.2, 1.4, 'ELECTRON MASS', 
         r'$m_e = M_U \cdot \Omega^{-40.23}$', 
         'Error: 0.000%', INFO)

# Box 2: Fine Structure
draw_box(ax, 7, 10.5, 3.2, 1.4, 'FINE STRUCTURE', 
         r'$\alpha^{-1} = \Omega^{1.03}$', 
         'Error: 0.003%', INFO)

# Box 3: Reactive Gravity
draw_box(ax, 10.5, 10.5, 3.2, 1.4, 'REACTIVE GRAVITY', 
         r'$\alpha_{reac} = 0.47$', 
         'Hubble Tension: Solved', INFO)

# === LEVEL 2: SECONDARY DERIVATIONS ===
ax.text(7, 8.8, 'SECONDARY DERIVATIONS', fontsize=9, color=SECONDARY, 
        ha='center', fontweight='bold')
ax.plot([2, 12], [8.6, 8.6], color=SECONDARY, linewidth=0.5, linestyle='--')

# Arrows
draw_arrow(ax, 3.5, 9.8, 3.5, 8.2)
draw_arrow(ax, 7, 9.8, 7, 8.2)
draw_arrow(ax, 10.5, 9.8, 10.5, 8.2)

# Box 4: Electron Spin
draw_box(ax, 3.5, 7.5, 3.2, 1.4, 'ELECTRON SPIN', 
         'Genus-1 Wormhole Topology\nS = h/2', 
         'Error: 0.000%', SUCCESS)

# Box 5: Lepton Generations
draw_box(ax, 7, 7.5, 3.2, 1.4, 'LEPTON GENERATIONS', 
         r'$m_n/m_e = \Omega^{\gamma(n-1)^d}$', 
         '4th Gen: Unstable (>4.5 TeV)', SUCCESS)

# Box 6: CMB Analysis
draw_box(ax, 10.5, 7.5, 3.2, 1.4, 'CMB 3rd PEAK', 
         'Entropic Potential Wells\nNo WIMPs Required', 
         'Planck 2018: Compatible', SUCCESS)

# === LEVEL 3: TERTIARY DERIVATIONS ===
ax.text(7, 5.8, 'TERTIARY DERIVATIONS', fontsize=9, color=SECONDARY, 
        ha='center', fontweight='bold')
ax.plot([2, 12], [5.6, 5.6], color=SECONDARY, linewidth=0.5, linestyle='--')

# Arrows
draw_arrow(ax, 3.5, 6.8, 5, 5.2)
draw_arrow(ax, 7, 6.8, 7, 5.2)
draw_arrow(ax, 10.5, 6.8, 9, 5.2)

# Box 7: Quark Topology
draw_box(ax, 5, 4.5, 3.2, 1.4, 'QUARK TOPOLOGY', 
         'Trefoil Knots (3_1)\nQ = crossing/3', 
         r'$\alpha_s = 1$ (Exact)', SUCCESS)

# Box 8: Schrodinger
draw_box(ax, 9, 4.5, 3.2, 1.4, 'SCHRODINGER EQ.', 
         'Holographic Thermodynamics\n' + r'$i\hbar\partial\psi/\partial t = H\psi$', 
         'QM: Emergent', SUCCESS)

# === MASTER EQUATION ===
draw_arrow(ax, 5, 3.8, 7, 2.6)
draw_arrow(ax, 9, 3.8, 7, 2.6)

master_box = FancyBboxPatch((3.5, 1.2), 7, 1.4, boxstyle="round,pad=0.03",
                             facecolor='#1A1A2E', edgecolor=PRIMARY, linewidth=2)
ax.add_patch(master_box)
ax.text(7, 2.1, 'UNIFIED FIELD EQUATION', fontsize=10, fontweight='bold', 
        color='white', ha='center')
ax.text(7, 1.6, r'$F = \alpha \cdot \Gamma \cdot T \cdot \nabla S$', 
        fontsize=12, color=GOLD, ha='center', fontweight='bold')

# === LEGEND ===
legend_x = 11.5
ax.text(legend_x, 3.2, 'Legend:', fontsize=9, fontweight='bold', color=PRIMARY)
ax.plot([legend_x - 0.3, legend_x + 0.3], [2.9, 2.9], color=SUCCESS, linewidth=3)
ax.text(legend_x + 0.5, 2.9, 'Verified', fontsize=8, color=SUCCESS, va='center')
ax.plot([legend_x - 0.3, legend_x + 0.3], [2.6, 2.6], color=INFO, linewidth=3)
ax.text(legend_x + 0.5, 2.6, 'Derived', fontsize=8, color=INFO, va='center')

# === FOOTER ===
ax.text(7, 0.5, 'Fulber, D.H.M. (2025). Federal University of Rio de Janeiro (UFRJ)', 
        fontsize=9, color=SECONDARY, ha='center')
ax.text(7, 0.15, 'DOI: 10.5281/zenodo.18090702', 
        fontsize=8, color=INFO, ha='center')

# Save
plt.tight_layout()
plt.savefig('tardis_academic.png', dpi=300, facecolor='white', 
            bbox_inches='tight', pad_inches=0.3)
plt.savefig('assets/tardis_model_overview.png', dpi=300, facecolor='white', 
            bbox_inches='tight', pad_inches=0.3)
print("Generated: tardis_academic.png")
print("Generated: assets/tardis_model_overview.png")
plt.show()
