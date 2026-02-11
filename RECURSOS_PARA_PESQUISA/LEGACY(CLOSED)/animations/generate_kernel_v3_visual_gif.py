
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import os

# Ensure output directory exists
OUTPUT_DIR = r"d:\TamesisTheoryCompleteResearchArchive\ANIMATIONS"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Generating KERNEL v3 Visual in: {OUTPUT_DIR}")

def generate_kernel_v3_visual_loop():
    # Setup Figure
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_title("KERNEL v3: The Entropic Bounce", color='white', y=0.95, fontsize=12, fontname='serif')

    # Simulation Parameters
    N = 60 # Number of nodes
    np.random.seed(42) # Reproducibility
    
    # Initial Positions (Random Cloud)
    # We will modulate these positions radially
    # Angles are fixed, radii breathe
    angles = np.random.rand(N) * 2 * np.pi
    base_radii = np.random.rand(N) * 0.5 + 0.2 # 0.2 to 0.7

    # Graphics Objects
    # Nodes (Scatter)
    nodes = ax.scatter([], [], s=30, zorder=10)
    
    # Connections (LineCollection)
    # We will compute connections dynamically based on distance threshold
    lines = LineCollection([], linewidths=0.5, zorder=5)
    ax.add_collection(lines)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    def update(frame):
        # Time t: 0 to 2pi (One full bounce cycle)
        # However, a bounce is Contraction -> Expansion.
        # Let's make one loop = Contraction -> Expansion -> Contraction
        # So sin wave perfect loop.
        t = (frame / 60.0) * 2 * np.pi
        
        # Breathing Factor:
        # We want tight compression at t=0 (and 2pi), max expansion at t=pi
        # cos(t) goes 1 -> -1 -> 1.
        # Let 'scale' be small when cos(t) is 1 (t=0)
        # scale = 1.2 - 0.8 * cos(t)  -> Range: [0.4, 2.0]
        # At t=0: scale=0.4 (Compressed/Bounce)
        # At t=pi: scale=2.0 (Expanded)
        
        # Use a sharper compression curve for dramatic "Bounce" effect
        # Gaussian-like dip? Or just simple harmonic?
        # Let's stick to harmonic for perfect loop smoothness.
        scale = 1.0 - 0.7 * np.cos(t) # Range: 0.3 (Bounce) to 1.7 (Expansion)
        
        # Update Node Positions
        current_radii = base_radii * scale
        
        # Add some rotation (Spinning Universe)
        current_angles = angles + t * 0.2
        
        xs = current_radii * np.cos(current_angles)
        ys = current_radii * np.sin(current_angles)
        
        # Update Nodes
        # Color: Hot (Red/White) when compressed, Cold (Blue/Purple) when expanded
        # Map scale 0.3->Hot, 1.7->Cold
        # Normalize scale for colormap: (scale - 0.3) / 1.4 -> 0 to 1
        norm_scale = (scale - 0.3) / 1.4
        
        # Invert for Heat: 0->Hot(1.0), 1->Cold(0.0)
        heat_val = 1.0 - norm_scale
        
        # Use 'inferno' colormap
        node_colors = plt.cm.inferno(0.2 + 0.8*heat_val) # Avoid pitch black
        nodes.set_offsets(np.column_stack([xs, ys]))
        nodes.set_color(node_colors)
        nodes.set_sizes(np.ones(N) * (20 + 40*heat_val)) # Bigger when hot
        
        # Update Connections
        # Connect nodes that are close to each other
        # This is O(N^2), but N=60 is fine.
        xy = np.column_stack([xs, ys])
        
        # Calculate distance matrix efficiently?
        # Just loop for visual simplicity and custom opacity logic
        segments = []
        colors = []
        
        # Dynamic connection threshold
        # When compressed, everything connects (Saturation).
        # When expanded, only close neighbors connect.
        threshold = 0.3 * scale # Threshold scales with universe size?
        # Actually, if we keep threshold constant-ish, connections break as it expands.
        # That's physically correct (Decoupling).
        dist_threshold = 0.25 # Fixed physical distance
        
        for i in range(N):
            for j in range(i+1, N):
                dist = np.sqrt((xs[i]-xs[j])**2 + (ys[i]-ys[j])**2)
                if dist < dist_threshold:
                    segments.append([(xs[i], ys[i]), (xs[j], ys[j])])
                    # Line color follows heat but with alpha fading at distance limit
                    alpha = 1.0 - (dist / dist_threshold)
                    # Use same colormap logic
                    base_col = plt.cm.inferno(0.2 + 0.8*heat_val)
                    # Matplotlib colors are (R,G,B,A)
                    # We need to set A
                    rgba = list(base_col)
                    rgba[3] = alpha * 0.8 # Max alpha 0.8
                    colors.append(rgba)

        lines.set_segments(segments)
        lines.set_color(colors)
        
        return nodes, lines

    # Create Animation
    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    
    # Save GIF
    filename = "KERNEL_V3_Visual_Loop.gif"
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Saving {filename}...")
    anim.save(filepath, writer='pillow', fps=20)
    print(f"Done! Saved to {filepath}")

if __name__ == "__main__":
    generate_kernel_v3_visual_loop()
