"""
Holographic Principle Visualization
Demonstrates: 2D boundary information encoding 3D volume.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def create_holographic_visualization():
    """
    Creates a visualization of the Holographic Principle:
    - A 2D spherical boundary (the "holographic screen")
    - Information bits on the boundary
    - Projection lines showing how 3D space emerges from 2D encoding
    """
    print("🌀 Generating Holographic Principle Visualization...")
    
    fig = plt.figure(figsize=(14, 6))
    
    # ═══════════════════════════════════════════════════════════════
    # Panel 1: The Holographic Screen (2D Boundary with Bits)
    # ═══════════════════════════════════════════════════════════════
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Create a sphere (the boundary)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Plot semi-transparent boundary
    ax1.plot_surface(x, y, z, alpha=0.15, color='blue', edgecolor='none')
    
    # Add "information bits" on the boundary (random points)
    np.random.seed(117)  # TARDIS seed
    n_bits = 200
    phi = np.random.uniform(0, 2 * np.pi, n_bits)
    theta = np.random.uniform(0, np.pi, n_bits)
    bx = np.sin(theta) * np.cos(phi)
    by = np.sin(theta) * np.sin(phi)
    bz = np.cos(theta)
    
    # Color bits by their "information state" (0 or 1)
    bit_states = np.random.randint(0, 2, n_bits)
    colors = ['#FF6B6B' if s == 1 else '#4ECDC4' for s in bit_states]
    
    ax1.scatter(bx, by, bz, c=colors, s=20, alpha=0.9)
    
    ax1.set_title('Holographic Boundary\n(Information encoded on 2D surface)', fontsize=11)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_xlim([-1.5, 1.5])
    ax1.set_ylim([-1.5, 1.5])
    ax1.set_zlim([-1.5, 1.5])
    
    # ═══════════════════════════════════════════════════════════════
    # Panel 2: Projection to 3D Volume
    # ═══════════════════════════════════════════════════════════════
    ax2 = fig.add_subplot(122, projection='3d')
    
    # Draw the boundary again (fainter)
    ax2.plot_surface(x, y, z, alpha=0.05, color='gray', edgecolor='none')
    
    # Draw projection lines from boundary to center
    n_lines = 30
    for i in range(n_lines):
        p = np.random.randint(0, n_bits)
        ax2.plot([bx[p], 0], [by[p], 0], [bz[p], 0], 
                 color='purple', alpha=0.3, linewidth=0.5)
    
    # Show "emergent" interior points (3D reality)
    n_interior = 100
    r_interior = np.random.uniform(0, 0.8, n_interior)
    phi_int = np.random.uniform(0, 2 * np.pi, n_interior)
    theta_int = np.random.uniform(0, np.pi, n_interior)
    ix = r_interior * np.sin(theta_int) * np.cos(phi_int)
    iy = r_interior * np.sin(theta_int) * np.sin(phi_int)
    iz = r_interior * np.cos(theta_int)
    
    ax2.scatter(ix, iy, iz, c='gold', s=15, alpha=0.8, marker='*')
    
    ax2.set_title('Emergent 3D Reality\n(Volume is projection of boundary)', fontsize=11)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_xlim([-1.5, 1.5])
    ax2.set_ylim([-1.5, 1.5])
    ax2.set_zlim([-1.5, 1.5])
    
    plt.suptitle('The Holographic Principle: 3D from 2D', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Save figure
    output_path = os.path.join(os.path.dirname(__file__), "..", "Validation", "holographic_principle.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    # Also save to DECODIFICANDO
    output_path2 = os.path.join(os.path.dirname(__file__), "..", "..", "DECODIFICANDO", 
                                 "04_DECODIFICACOES_NOVAS", "assets", "holographic_principle.png")
    os.makedirs(os.path.dirname(output_path2), exist_ok=True)
    plt.savefig(output_path2, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path2}")
    
    plt.close()
    return output_path

def create_bekenstein_bound_visualization():
    """
    Visualizes the Bekenstein Bound:
    - Information grows with AREA, not VOLUME
    """
    print("📐 Generating Bekenstein Bound Visualization...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    radii = np.linspace(1, 10, 100)
    volume = (4/3) * np.pi * radii**3
    area = 4 * np.pi * radii**2
    
    # Normalize for comparison
    volume_norm = volume / volume.max()
    area_norm = area / area.max()
    
    ax.plot(radii, volume_norm, 'b-', linewidth=2, label='Volume (naive expectation)')
    ax.plot(radii, area_norm, 'r-', linewidth=2, label='Area (Bekenstein bound)')
    
    ax.fill_between(radii, area_norm, volume_norm, alpha=0.2, color='green',
                     label='"Missing" information')
    
    ax.set_xlabel('Radius (arbitrary units)', fontsize=11)
    ax.set_ylabel('Normalized Information Capacity', fontsize=11)
    ax.set_title('Bekenstein Bound: Information Scales with Area, Not Volume', fontsize=12, fontweight='bold')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Add annotation
    ax.annotate('The 3D "interior"\ncontains no more\ninformation than\nthe 2D surface!',
                xy=(7, 0.5), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "Validation", "bekenstein_bound.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()
    return output_path

if __name__ == "__main__":
    print("=" * 60)
    print("🌀 HOLOGRAPHIC PRINCIPLE SIMULATION")
    print("=" * 60)
    
    path1 = create_holographic_visualization()
    path2 = create_bekenstein_bound_visualization()
    
    print("\n✅ All visualizations generated successfully!")
    print(f"   - Holographic Principle: holographic_principle.png")
    print(f"   - Bekenstein Bound: bekenstein_bound.png")
