"""
TAMESIS ANIMATION ENGINE: ER = EPR (3D LOOP)
============================================
Generates a sequence of frames visualizing the high-dimensional
connection (wormhole) between entangled particles on a 1D manifold.

Output: 
- /frames/frame_XXX.png
- Generates a perfect loop rotation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import shutil

# Configuration
FRAMES = 60
NODES = 50
RADIUS = 5
OUTPUT_DIR = "frames"

def ensure_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

def generate_frames():
    print(f"Initializing Tamesis Animation Engine ({FRAMES} frames)...")
    ensure_dir(OUTPUT_DIR)
    
    # Geometry Setup (The Ring)
    theta = np.linspace(0, 2*np.pi, NODES)
    x = RADIUS * np.cos(theta)
    y = RADIUS * np.sin(theta)
    z = np.zeros(NODES) # Flat 1D universe on 2D plane initially
    
    # Identify Entangled Pair (Indices)
    idx_A = 0
    idx_B = NODES // 2
    
    # Process Frames
    for i in range(FRAMES):
        fig = plt.figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        # Black background for "Space"
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')
        ax.grid(False)
        ax.set_axis_off()
        
        # 1. Draw the "Universe" (The Ring)
        # Add some vertical fluctuation to look like 'quantum foam' or just keep it clean
        # Let's keep it clean but rotate the ring slightly in logic or view
        
        # Plot Ring Edges
        ax.plot(x, y, z, color='cyan', alpha=0.3, linewidth=1)
        
        # Plot Nodes
        ax.scatter(x, y, z, color='cyan', s=10, alpha=0.6)
        
        # 2. Draw the Homological Holes (Entanglement)
        # The Wormhole - Connecting A and B directly through the bulk
        # We animate the wormhole "pulsing" or just existing
        
        # Coordinates of A and B
        pA = np.array([x[idx_A], y[idx_A], z[idx_A]])
        pB = np.array([x[idx_B], y[idx_B], z[idx_B]])
        
        # Draw the Wormhole (The Bridge)
        # Color it hot pink/magenta to contrast with cyan space
        ax.plot([pA[0], pB[0]], [pA[1], pB[1]], [pA[2], pB[2]], 
                color='#ff00ff', linewidth=3, alpha=0.9)
        
        # Highlight the Entangled Particles
        ax.scatter([pA[0], pB[0]], [pA[1], pB[1]], [pA[2], pB[2]], 
                   color='#ffffff', s=100, edgecolors='#ff00ff')
        
        # 3. Camera Rotation logic (Perfect Loop)
        # Rotate Azimuth 360 degrees over FRAMES
        angle = 360 * (i / FRAMES)
        ax.view_init(elev=20, azim=angle)
        
        # Title (Optional, maybe clean is better)
        # ax.set_title("ER = EPR", color='white')
        
        # Save Frame
        filename = f"{OUTPUT_DIR}/frame_{i:03d}.png"
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if i % 10 == 0:
            print(f"Generated frame {i}/{FRAMES}")

    print("Frames generated successfully.")

if __name__ == "__main__":
    generate_frames()
