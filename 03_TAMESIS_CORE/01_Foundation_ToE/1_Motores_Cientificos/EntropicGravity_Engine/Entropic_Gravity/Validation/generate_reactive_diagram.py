"""
Conceptual Diagram: Reactive Dark Matter Mechanism
--------------------------------------------------
Illustrates how cosmic horizon tension creates apparent "Dark Matter" effects
through entropic back-reaction in spacetime.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.patches as mpatches

# Create figure
fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('white')

# Main 3D plot
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('white')

# Parameters for the spacetime fabric
x = np.linspace(-10, 10, 100)
y = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x, y)

# Define three galaxy positions
galaxy_positions = [
    {'x': -5, 'y': 0, 'mass': 1.0, 'label': 'Galaxy A'},
    {'x': 0, 'y': 5, 'mass': 0.8, 'label': 'Galaxy B'},
    {'x': 5, 'y': -3, 'mass': 0.9, 'label': 'Galaxy C'}
]

# Calculate the deformation (gravitational wells)
Z = np.zeros_like(X)

for galaxy in galaxy_positions:
    gx, gy, mass = galaxy['x'], galaxy['y'], galaxy['mass']
    
    # Distance from galaxy
    r = np.sqrt((X - gx)**2 + (Y - gy)**2) + 0.5
    
    # Newtonian well (expected)
    Z_newtonian = -mass * 2.0 / r
    
    # Entropic enhancement (Reactive Dark Matter effect)
    # The well is deeper due to horizon back-reaction
    entropic_factor = 1.0 + 0.8 * np.exp(-r/3.0)  # Extra depth from entropy
    Z_entropic = Z_newtonian * entropic_factor
    
    Z += Z_entropic

# Create the surface plot (spacetime fabric)
surf = ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.7, 
                       edgecolor='none', antialiased=True, vmin=-5, vmax=0)

# Add wireframe to show grid structure
ax.plot_wireframe(X, Y, Z, color='purple', alpha=0.15, linewidth=0.5, 
                  rstride=5, cstride=5)

# Mark galaxy positions with spheres
for galaxy in galaxy_positions:
    gx, gy = galaxy['x'], galaxy['y']
    # Find Z value at galaxy position
    idx_x = np.argmin(np.abs(x - gx))
    idx_y = np.argmin(np.abs(y - gy))
    z_val = Z[idx_y, idx_x]
    
    # Draw galaxy as golden sphere
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    xs = 0.5 * np.cos(u) * np.sin(v) + gx
    ys = 0.5 * np.sin(u) * np.sin(v) + gy
    zs = 0.5 * np.cos(v) + z_val
    ax.plot_surface(xs, ys, zs, color='gold', alpha=0.9, edgecolor='orange')

# Add visual elements showing horizon tension
# Arrows pointing from edges toward galaxies
arrow_props = dict(arrowstyle='->', lw=2, color='cyan', alpha=0.6)
for galaxy in galaxy_positions:
    gx, gy = galaxy['x'], galaxy['y']
    
    # Arrows from cosmic horizon (edges) toward galaxy
    if gx < 0:
        ax.plot([-10, gx], [gy, gy], [0.5, 0.5], 'c--', alpha=0.4, linewidth=1.5)
    else:
        ax.plot([10, gx], [gy, gy], [0.5, 0.5], 'c--', alpha=0.4, linewidth=1.5)

# Labels and annotations
ax.text(0, 0, 2, "Cosmic Horizon (Hubble Scale)", color='navy', 
        fontsize=14, fontweight='bold', ha='center')

ax.text(-5, 0, -2.5, "Baryonic\nGalaxy", color='darkgoldenrod', 
        fontsize=10, ha='center', fontweight='bold')

ax.text(5, -3, -2.5, "Reactive\nEntropy", color='purple', 
        fontsize=11, ha='center', fontweight='bold', style='italic')

ax.text(0, -8, -1, "Entropic Deepening\n(NOT Particle DM)", color='red', 
        fontsize=10, ha='center', fontweight='bold', 
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='red', alpha=0.8))

# Styling
ax.set_xlabel('Spatial Coordinate (Mpc)', fontsize=11, labelpad=10)
ax.set_ylabel('Spatial Coordinate (Mpc)', fontsize=11, labelpad=10)
ax.set_zlabel('Spacetime Curvature\n(Gravitational Potential)', fontsize=11, labelpad=10)
ax.set_title('Reactive Dark Matter Mechanism\nEntropy-Induced Gravitational Wells', 
             fontsize=16, fontweight='bold', pad=20)

# Set viewing angle
ax.view_init(elev=25, azim=45)

# Set limits
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-5, 2)

# Grid
ax.grid(True, alpha=0.3)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='gold', edgecolor='orange', label='Baryonic Matter'),
    mpatches.Patch(facecolor='purple', alpha=0.5, label='Entropic Curvature'),
    mpatches.Patch(facecolor='cyan', alpha=0.4, label='Horizon Tension'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

# Add explanatory text box
textstr = ('Mechanism: Cosmic horizon stretches spacetime.\n'
           'Baryonic mass creates initial curvature.\n'
           'Entropic back-reaction deepens wells.\n'
           'Result: "Dark Matter" effect without particles.')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black')
fig.text(0.15, 0.02, textstr, fontsize=9, verticalalignment='bottom',
         bbox=props, family='monospace')

plt.tight_layout()

# Save
output_path = "reactive_dark_matter_diagram.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Diagram saved: {output_path}")

plt.show()
