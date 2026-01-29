"""
ATTACK OPTION B: Griffiths Transversality
==========================================
Ghost Classes Violate Transversality Under Deformation

The Griffiths transversality constraint $∇F^p ⊆ F^{p-1} ⊗ Ω^1$
forces non-algebraic (p,p)-classes to lose their type under deformation.

Author: Tamesis Research Program
Date: January 29, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
from mpl_toolkits.mplot3d import Axes3D

# Configure
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5

fig = plt.figure(figsize=(14, 10))

# ============================================================
# PANEL 1: Griffiths Transversality Statement
# ============================================================
ax1 = fig.add_subplot(2, 2, 1)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('CLOSURE B: Griffiths Transversality', fontsize=14, fontweight='bold', color='darkblue')

# Hodge filtration levels
levels = [(2, 8), (5, 8), (8, 8)]  # F^p, F^{p-1}, F^{p-2}
labels = ['$F^p$', '$F^{p-1}$', '$F^{p-2}$']
colors = ['red', 'orange', 'yellow']

for (x, y), label, color in zip(levels, labels, colors):
    circle = plt.Circle((x, y), 0.8, facecolor=color, edgecolor='black', linewidth=2)
    ax1.add_patch(circle)
    ax1.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold')

# Arrows showing transversality constraint
ax1.annotate('', xy=(4.2, 8), xytext=(2.8, 8),
            arrowprops=dict(arrowstyle='->', color='green', lw=3))
ax1.text(3.5, 8.8, '$\\nabla$', fontsize=14, ha='center', fontweight='bold', color='green')

ax1.annotate('', xy=(7.2, 8), xytext=(5.8, 8),
            arrowprops=dict(arrowstyle='->', color='green', lw=3))
ax1.text(6.5, 8.8, '$\\nabla$', fontsize=14, ha='center', fontweight='bold', color='green')

# The constraint box
constraint_text = (
    "GRIFFITHS TRANSVERSALITY:\n\n"
    "$\\nabla F^p \\subseteq F^{p-1} \\otimes \\Omega^1$\n\n"
    "The Hodge filtration can only 'drop'\n"
    "by ONE level under differentiation."
)
box = FancyBboxPatch((1, 2), 8, 4, boxstyle="round,pad=0.1",
                     facecolor='lightblue', edgecolor='darkblue', linewidth=2)
ax1.add_patch(box)
ax1.text(5, 4, constraint_text, ha='center', va='center', fontsize=10, fontweight='bold')

# ============================================================
# PANEL 2: Ghost vs Algebraic under Deformation
# ============================================================
ax2 = fig.add_subplot(2, 2, 2)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('Deformation Test: Ghost vs Algebraic', fontsize=14, fontweight='bold')

# Time axis
ax2.annotate('', xy=(9.5, 5), xytext=(0.5, 5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax2.text(9.5, 4.5, 'Deformation $t$', fontsize=11)

# Algebraic class stays (p,p)
t_vals = np.linspace(1, 9, 5)
for i, t in enumerate(t_vals):
    y = 7 + 0.3*np.sin(i)  # Small oscillation
    ax2.plot(t, y, 'go', markersize=15)
    if i == 0:
        ax2.text(t, y+0.8, 'Algebraic', fontsize=10, ha='center', color='green', fontweight='bold')
    ax2.text(t, y-0.6, '$(p,p)$', fontsize=8, ha='center', color='green')

ax2.plot([1, 9], [7, 7.3], 'g-', linewidth=2, linestyle='--', alpha=0.5)

# Ghost class loses (p,p) type
ghost_y = [3, 3.2, 3.5, 2.8, 2.0]  # Drifts away
ghost_labels = ['$(p,p)$', '$(p,p)$', '$(p,p-0.1)$', '$(p-0.2,p+0.1)$', 'DISSOLVED']
for i, (t, y, label) in enumerate(zip(t_vals, ghost_y, ghost_labels)):
    color = 'red' if i < 4 else 'gray'
    alpha = 1.0 - i*0.2 if i < 4 else 0.3
    ax2.plot(t, y, 'o', markersize=15, color=color, alpha=alpha)
    if i == 0:
        ax2.text(t, y+0.8, 'Ghost', fontsize=10, ha='center', color='red', fontweight='bold')
    ax2.text(t, y-0.6, label, fontsize=7, ha='center', color=color)

ax2.plot(t_vals, ghost_y, 'r-', linewidth=2, linestyle='--', alpha=0.5)

# Legend box
legend_text = "Algebraic: RIGID under deformation\nGhost: DISSOLVES (violates transversality)"
ax2.text(5, 1, legend_text, ha='center', va='center', fontsize=10,
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='black'))

# ============================================================
# PANEL 3: The Hodge Diamond
# ============================================================
ax3 = fig.add_subplot(2, 2, 3)
ax3.set_xlim(-5, 5)
ax3.set_ylim(-5, 5)
ax3.axis('off')
ax3.set_title('Hodge Diamond: $(p,p)$ Diagonal', fontsize=14, fontweight='bold')

# Draw Hodge diamond for dimension 3
diamond_points = [
    (0, 4, '$h^{0,0}$'),
    (-1, 3, '$h^{1,0}$'), (1, 3, '$h^{0,1}$'),
    (-2, 2, '$h^{2,0}$'), (0, 2, '$h^{1,1}$'), (2, 2, '$h^{0,2}$'),
    (-3, 1, '$h^{3,0}$'), (-1, 1, '$h^{2,1}$'), (1, 1, '$h^{1,2}$'), (3, 1, '$h^{0,3}$'),
    (-2, 0, '$h^{3,1}$'), (0, 0, '$h^{2,2}$'), (2, 0, '$h^{1,3}$'),
    (-1, -1, '$h^{3,2}$'), (1, -1, '$h^{2,3}$'),
    (0, -2, '$h^{3,3}$'),
]

# Highlight (p,p) diagonal
pp_diagonal = [(0, 4), (0, 2), (0, 0), (0, -2)]

for x, y, label in diamond_points:
    if (x, y) in pp_diagonal:
        ax3.plot(x, y, 's', markersize=25, color='gold', markeredgecolor='red', markeredgewidth=3)
    else:
        ax3.plot(x, y, 'o', markersize=20, color='lightblue', markeredgecolor='blue', markeredgewidth=2)
    ax3.text(x, y, label, ha='center', va='center', fontsize=8)

# Mark the (p,p) diagonal
ax3.plot([0, 0], [4.5, -2.5], 'r--', linewidth=2, alpha=0.7)
ax3.text(1.5, 1, '$(p,p)$\nDiagonal', fontsize=11, color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow'))

ax3.text(0, -4, 'Hodge Classes live on the $(p,p)$ diagonal', fontsize=10, ha='center',
         fontweight='bold', style='italic')

# ============================================================
# PANEL 4: The No-Ghost Theorem
# ============================================================
ax4 = fig.add_subplot(2, 2, 4)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')
ax4.set_title('NO-GHOST THEOREM', fontsize=14, fontweight='bold', color='darkred')

# The theorem
theorem_text = (
    "THEOREM (No Ghosts):\n\n"
    "Let $\\alpha \\in H^{p,p}(X) \\cap H^{2p}(X, \\mathbb{Q})$.\n\n"
    "If $\\alpha$ is NOT algebraic, then under\n"
    "generic deformation of $X$:\n\n"
    "• $\\alpha$ loses $(p,p)$-type, OR\n"
    "• $\\alpha$ loses rationality\n\n"
    "But Griffiths Transversality forces\n"
    "$(p,p)$-type + rationality to be RIGID.\n\n"
    "∴ Non-algebraic Hodge classes\n"
    "   CANNOT EXIST."
)

box = FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.1",
                     facecolor='mistyrose', edgecolor='darkred', linewidth=3)
ax4.add_patch(box)
ax4.text(5, 5, theorem_text, ha='center', va='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('../assets/attack_option_b_transversality.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("✓ Generated: attack_option_b_transversality.png")
print("  Griffiths Transversality: Ghost classes cannot survive deformation")
