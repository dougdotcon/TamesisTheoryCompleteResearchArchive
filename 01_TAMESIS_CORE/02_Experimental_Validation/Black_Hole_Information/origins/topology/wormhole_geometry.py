import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_wormhole_topology():
    """
    Visualizes the topological difference between a standard particle (Sphere/Genus-0)
    and a TAMESIS spinor particle (Torus/Genus-1 Wormhole).
    """
    fig = plt.figure(figsize=(12, 6))

    # 1. Genus-0: Sphere (Scalar Particle)
    ax1 = fig.add_subplot(121, projection='3d')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax1.plot_surface(x, y, z, color='b', alpha=0.6, edgecolors='k', lw=0.1)
    ax1.set_title("Standard Particle\n(Sphere: Genus-0)\nSpin-0 / Scalar", fontsize=12)
    ax1.axis('off')

    # 2. Genus-1: Torus (Spinor/Wormhole)
    ax2 = fig.add_subplot(122, projection='3d')
    
    # Torus parameterization
    R = 8 # Major radius
    r = 3 # Minor radius
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, 2 * np.pi, 100)
    u, v = np.meshgrid(u, v)
    
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    
    # Plot the surface
    ax2.plot_surface(x, y, z, color='r', alpha=0.6, edgecolors='k', lw=0.1)
    
    # Highlight the "Throat" (The wormhole connection)
    # We can draw lines wrapping around the torus to show the non-contractible loops
    theta = np.linspace(0, 2*np.pi, 100)
    # Loop 1: Poloidal (Short way) - Represents E-field flux through throat
    x1 = (R + r * np.cos(theta)) * np.cos(0)
    y1 = (R + r * np.cos(theta)) * np.sin(0)
    z1 = r * np.sin(theta)
    ax2.plot(x1, y1, z1, 'y-', lw=3, label='Flux Loop (flux)')
    
    # Loop 2: Toroidal (Long way) - Represents Magnetic flux / Spin
    x2 = (R + r * np.cos(np.pi/2)) * np.cos(theta)
    y2 = (R + r * np.cos(np.pi/2)) * np.sin(theta)
    z2 = r * np.sin(np.pi/2) * np.ones_like(theta)
    ax2.plot(x2, y2, z2, 'g-', lw=3, label='Spin Loop (chirality)')

    ax2.set_title("TAMESIS Fermion\n(Wormhole: Genus-1)\nSpin-1/2", fontsize=12)
    ax2.axis('off')
    ax2.legend()
    
    # Adjust layout to prevent title clipping
    # tight_layout can sometimes be aggressive with 3D plots
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    
    plt.savefig('../simulation/topology_comparison.png', bbox_inches='tight', pad_inches=0.1)
    print("Saved topology comparison.")

if __name__ == "__main__":
    plot_wormhole_topology()
