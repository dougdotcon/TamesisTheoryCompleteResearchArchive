import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Wedge
import os

# Ensure output directory exists
OUTPUT_DIR = r"d:\TamesisTheoryCompleteResearchArchive\animations"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Generating animations in: {OUTPUT_DIR}")

def save_gif(anim, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Saving {filename}...")
    anim.save(filepath, writer='pillow', fps=30)
    print(f"Saved {filepath}")

# ==========================================
# 1. TRI: Theory of Regime Incompatibility
# Redesigned for PERFECT LOOP
# Concept: "Breathing Domains" (Interference Pattern)
# ==========================================
def generate_tri_loop():
    N = 200
    x = np.linspace(0, 4*np.pi, N)
    y = np.linspace(0, 4*np.pi, N)
    X, Y = np.meshgrid(x, y)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_title("TRI: Incompatible Regimes (Loop)", color='white')

    # Initial plot
    im = ax.imshow(np.zeros((N, N)), cmap='magma', vmin=-2, vmax=2)

    def update(frame):
        # t goes from 0 to 2*pi
        t = (frame / 60.0) * 2 * np.pi
        
        # Periodic interference pattern
        # Z1 and Z2 represent two "laws" competing
        # They drift in phase but return exactly to start at t=2pi
        Z1 = np.sin(X + np.cos(t)) * np.cos(Y + np.sin(t))
        Z2 = np.sin(X*1.5 - t) * np.cos(Y*1.5 + t)
        
        # The interaction term
        Z = Z1 + Z2
        
        im.set_data(Z)
        return [im]

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "TRI_Infinite_Loop.gif")
    plt.close(fig)

# ==========================================
# 2. TDTR: Thermodynamic Time Reversal
# Redesigned for PERFECT LOOP
# Concept: "Shepard Zoom" (Starfield with Fade)
# ==========================================
def generate_tdtr_loop():
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_title("TDTR: Entropic Flow (Loop)", color='white', y=1.05)

    n_particles = 400
    # Fixed random seeds for consistency
    np.random.seed(42)
    base_theta = np.random.rand(n_particles) * 2 * np.pi
    base_radii = np.random.rand(n_particles)
    
    scatter = ax.scatter([], [], cmap='cool', alpha=1.0)
    ax.set_ylim(0, 1)

    def update(frame):
        # progress 0.0 to 1.0
        prog = frame / 60.0
        
        # Move radii outward
        # We start at base_radii and add 'prog'.
        # We simulate infinite flow by modulo 1.0
        current_radii = (base_radii + prog) % 1.0
        
        # Calculate Opacity (Alpha)
        # Fade in at 0, Fade out at 1.
        # Parabolic curve: 4 * r * (1-r) peaks at 0.5
        # Or better: sin(pi * r)
        alphas = np.sin(np.pi * current_radii)
        
        # Rotation (Spin)
        current_theta = base_theta + (prog * 0.5) # Rotates small amount
        
        # Color based on radius (Redshift)
        colors = current_radii
        
        # Set offsets
        offsets = np.column_stack([current_theta, current_radii])
        scatter.set_offsets(offsets)
        scatter.set_array(colors)
        
        # Manually set alphas because scatter supports array of alphas?
        # Matplotlib scatter doesn't support list of alphas easily in update.
        # Trick: Map alpha to RGBA colors manually
        # Get colormap
        cmap = plt.cm.cool
        rgba_colors = cmap(current_radii)
        rgba_colors[:, 3] = alphas # Set alpha channel
        scatter.set_color(rgba_colors)
        
        return [scatter]

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "TDTR_Infinite_Loop.gif")
    plt.close(fig)

# ==========================================
# 3. TAMESIS: Spectral Geometry
# Redesigned for PERFECT LOOP
# Concept: "Integer Gear Ratios"
# ==========================================
def generate_tamesis_loop():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_title("TAMESIS: Spectral Clockwork (Loop)", color='white')

    boundary = Circle((0, 0), 1, color='white', fill=False, linewidth=2)
    ax.add_patch(boundary)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')

    # Geodesic Chords
    lines = []
    n_lines = 16
    for i in range(n_lines):
        l, = ax.plot([], [], lw=1, alpha=0.7)
        lines.append(l)

    # Prime Points
    # We use integer speeds to ensure loop
    primes = [2, 3, 5, 7, 11]
    points = ax.scatter([], [], color='gold', s=40, zorder=10)

    def update(frame):
        # Global cycle 0 to 2pi
        t = (frame / 60.0) * 2 * np.pi
        
        # 1. Rotating Chords (Background Geometry)
        # They rotate continuously
        for i, line in enumerate(lines):
            angle_base = (i / n_lines) * 2 * np.pi
            # Rotation speed = 1 cycle per loop
            theta = angle_base + t 
            
            # Breathing effect on chord span: sin(2t) is periodic 2pi
            span = (np.pi/2) + 0.5 * np.sin(t)
            
            p1 = (np.cos(theta), np.sin(theta))
            p2 = (np.cos(theta + span), np.sin(theta + span))
            
            line.set_data([p1[0], p2[0]], [p1[1], p2[1]])
            
            # Color cycle
            col_val = (np.sin(theta*2) + 1)/2
            line.set_color(plt.cm.plasma(col_val))

        # 2. Prime Points
        # Each prime p rotates with speed equal to p (integer)
        # This guarantees they return to start at t=2pi
        px = []
        py = []
        for p in primes:
            # Radius inverse to p
            r = 0.9 - (0.5/p)
            # Angle: Base position + Speed*time
            # Using integer `p` as multiplier ensures loop closure
            angle = (p * t) 
            px.append(r * np.cos(angle))
            py.append(r * np.sin(angle))
            
        points.set_offsets(np.column_stack([px, py]))

        return lines + [points]

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "TAMESIS_Infinite_Loop.gif")
    plt.close(fig)

if __name__ == "__main__":
    generate_tri_loop()
    generate_tdtr_loop()
    generate_tamesis_loop()
