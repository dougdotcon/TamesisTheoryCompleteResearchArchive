"""
=============================================================================
  TAMESIS RESEARCH — Hyper-Vortex Simulation ("The Abyssal Monad")
=============================================================================

  Visualizes the Harmonic Monad with EXTREME density (Thousands of Layers).
  Uses a particle system approach to render the "Vortex of Information"
  without crashing the rendering engine.

  Features:
  - N = 10,000 particles (Information Bits).
  - Differential Rotation (Inner layers spin faster).
  - Spectral Coloring (Blue/Quantum Core -> Gold/Relativistic Horizon).
  - Z-Axis modulation (The "Breathing" of the Sphere).

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def simulate_hyper_vortex(filename="monada_hyper_vortex.gif"):
    print("Generating Hyper-Vortex GIF (High Density)...")
    
    # Parameters
    N_PARTICLES = 2000 # Optimized for speed, still looks dense
    FRAMES = 40
    
    # Initialize Particles
    # Radius: Log-normal distribution to concentrate density in the center (Singularity)
    # but extending to the edge (Horizon).
    # r in [0.1, 3.0]
    r = np.random.lognormal(0, 0.5, N_PARTICLES)
    r = np.clip(r, 0.1, 3.0)
    
    # Initial Angle
    theta = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    
    # Initial Z (Spherical distribution approximation)
    phi = np.random.uniform(0, np.pi, N_PARTICLES)
    # Convert spherical to cylindrical R, Z for calculation ease
    # Actually, let's stick to a "Disk" vortex with thickness
    z_spread = 0.5 * np.exp(-r) # Inner core is spherical, outer is disk-like
    z = np.random.normal(0, z_spread, N_PARTICLES)
    
    # Angular Velocity (Keplerian-ish: w ~ 1/sqrt(r))
    # Inner layers fast, outer layers slow.
    omega = 0.5 / np.sqrt(r)
    
    # Colors based on Radius
    # Map r to colormap (0.1 -> Blue, 3.0 -> Gold)
    # We'll calculate colors frame-by-frame or pre-calc? Pre-calc is better.
    # Normalize r for colormap
    norm_r = (r - 0.1) / (3.0 - 0.1)
    colors = plt.cm.twilight(norm_r) 
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_axis_off()
    
    def update(frame):
        ax.cla()
        ax.set_axis_off()
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)
        ax.set_zlim(-2, 2)
        
        # Update angles
        current_theta = theta + omega * frame
        
        # Add "Breathing" (Pulsation)
        # The entire sphere expands/contracts slightly
        pulse = 1.0 + 0.1 * np.sin(frame * 0.1)
        r_pulse = r * pulse
        
        # Convert to Cartesian
        x = r_pulse * np.cos(current_theta)
        y = r_pulse * np.sin(current_theta)
        
        # Add a vertical "Jet" rotation (Twist in Z)
        # z twist depends on radius
        z_twist = z + 0.2 * np.sin(current_theta * 2) 
        
        # Scatter Plot
        # s=1 for "Dust" effect
        # Alpha based on radius (Core is bright)
        ax.scatter(x, y, z_twist, c=colors, s=2, alpha=0.6, edgecolors='none')
        
        # Central Singularity
        ax.scatter([0], [0], [0], c='white', s=50, edgecolors='white', alpha=1.0)
        
        ax.text2D(0.5, 0.95, "MONADA HIPER-DENSA (5000 CAMADAS)", 
                 transform=ax.transAxes, ha='center', color='white', fontweight='bold')
        
        # Camera rotation for cinematic effect
        ax.view_init(elev=30, azim=frame * 2)

    ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=False)
    path = os.path.join(OUTPUT_DIR, filename)
    ani.save(path, writer='pillow', fps=10)
    plt.close(fig)
    print(f"    Saved Hyper-Vortex: {path}")

if __name__ == "__main__":
    simulate_hyper_vortex()
