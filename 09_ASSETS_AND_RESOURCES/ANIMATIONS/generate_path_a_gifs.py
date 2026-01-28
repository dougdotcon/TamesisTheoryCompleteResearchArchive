import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
import os

# Output Directory
OUTPUT_DIR = r"d:\TamesisTheoryCompleteResearchArchive\animations"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"Generating Path A animations in: {OUTPUT_DIR}")

def save_gif(anim, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Saving {filename}...")
    anim.save(filepath, writer='pillow', fps=30)
    print(f"Saved {filepath}")

# Helper for Void Lensing
def lensing_effect(x, y, strength):
    # Radial push (concave lens)
    r = np.sqrt(x**2 + y**2)
    # Avoid div by zero
    r = np.maximum(r, 0.1)
    
    # Gaussian envelope for the effect
    # Simple push from center, fading out.
    push = strength * (1.0 / r) * np.exp(-r/2)
    
    return x + push * (x/r), y + push * (y/r)

# ==========================================
# 1. GALAXY ROTATION: Newton vs Entropic
# ==========================================
def generate_galaxy_loop():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_title("Stage 2: Entropic Gravity (a0) vs Newton", color='white', y=1.02)
    
    # Galaxy Center
    ax.add_patch(Circle((0,0), 0.1, color='white', zorder=10))
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')

    # Stars Setup
    n_stars = 150
    radii_raw = np.linspace(0.3, 2.2, n_stars)
    angles = np.random.rand(n_stars) * 2 * np.pi
    
    # Velocities setup (Quantized for loop)
    w_newton_phys = (1.0 / np.sqrt(radii_raw)) * 2 * np.pi
    k_newton = np.round(w_newton_phys / (2*np.pi))
    k_newton[k_newton < 1] = 1 
    w_newton_loop = k_newton * 2 * np.pi 
    
    v_flat_phys = 1.0
    w_entropic_phys = (v_flat_phys / radii_raw) * 2 * np.pi
    k_entropic = np.round(w_entropic_phys / (2*np.pi))
    k_entropic[k_entropic < 1] = 1
    w_entropic_loop = k_entropic * 2 * np.pi

    stars_newton = ax.scatter([], [], color='cyan', s=10, alpha=0.6, label='Newton')
    starts_entropic_artist = ax.scatter([], [], color='magenta', s=25, alpha=0.8, marker='*', label='Entropic')
    
    ax.text(-2.3, 2.3, "Cyan: Newton (Decay)", color='cyan', fontsize=8)
    ax.text(-2.3, 2.1, "Magenta: Tamesis (Flat)", color='magenta', fontsize=8)

    def update(frame):
        t = frame / 60.0
        theta_n = angles + w_newton_loop * t
        theta_e = angles + w_entropic_loop * t
        
        xn = radii_raw * np.cos(theta_n)
        yn = radii_raw * np.sin(theta_n)
        xe = radii_raw * np.cos(theta_e)
        ye = radii_raw * np.sin(theta_e)
        
        stars_newton.set_offsets(np.column_stack([xn, yn]))
        starts_entropic_artist.set_offsets(np.column_stack([xe, ye]))
        return [stars_newton, starts_entropic_artist]

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "PATH_A_Galaxy_Rotation.gif")
    plt.close(fig)

# ==========================================
# 2. VOID LENSING: The Void Anomaly
# ==========================================
def generate_void_loop():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_axis_off()
    fig.patch.set_facecolor('black')
    ax.set_title("Stage 4: Void Lensing (Entropy Gradient)", color='white', y=1.02)
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')

    void = Circle((0,0), 1.0, color='#111111', zorder=5)
    ax.add_patch(void)
    
    n_lines = 14
    x_grid = np.linspace(-1.9, 1.9, n_lines)
    lines = []
    
    for i in range(n_lines):
        line, = ax.plot([], [], color='gold', lw=1, alpha=0.5)
        lines.append(line)

    def update(frame):
        t = (frame / 60.0) * 2 * np.pi
        strength = 0.4 * np.sin(t)
        artists = [void]
        
        for i, x0 in enumerate(x_grid):
            y_vals = np.linspace(-1.9, 1.9, 100)
            x_vals = np.full_like(y_vals, x0)
            Lx, Ly = lensing_effect(x_vals, y_vals, strength)
            lines[i].set_data(Lx, Ly)
            lines[i].set_alpha(0.3 + 0.3 * np.abs(np.sin(t)))
            artists.append(lines[i])

        return artists

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "PATH_A_Void_Lensing.gif")
    plt.close(fig)

# ==========================================
# 3. UNIFIED COLLAGE
# ==========================================
def generate_unified_loop():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplots_adjust(wspace=0.1, left=0.05, right=0.95, bottom=0.05, top=0.90)
    fig.patch.set_facecolor('black')
    
    # --- SETUP AX1 (GALAXY) ---
    ax1.set_axis_off()
    ax1.set_title("Stage 2: Galaxy Rotation (a0)", color='white', fontsize=12)
    ax1.set_xlim(-2.5, 2.5)
    ax1.set_ylim(-2.5, 2.5)
    ax1.set_aspect('equal')
    ax1.add_patch(Circle((0,0), 0.1, color='white', zorder=10))

    # Galaxy Data
    n_stars = 150
    radii_raw = np.linspace(0.3, 2.2, n_stars)
    angles = np.random.rand(n_stars) * 2 * np.pi
    
    w_newton_phys = (1.0 / np.sqrt(radii_raw)) * 2 * np.pi
    k_newton = np.round(w_newton_phys / (2*np.pi)); k_newton[k_newton < 1] = 1 
    w_newton_loop = k_newton * 2 * np.pi 
    
    v_flat_phys = 1.0
    w_entropic_phys = (v_flat_phys / radii_raw) * 2 * np.pi
    k_entropic = np.round(w_entropic_phys / (2*np.pi)); k_entropic[k_entropic < 1] = 1
    w_entropic_loop = k_entropic * 2 * np.pi

    stars_newton = ax1.scatter([], [], color='cyan', s=10, alpha=0.6)
    stars_entropic = ax1.scatter([], [], color='magenta', s=25, alpha=0.8, marker='*')
    
    ax1.text(0, -2.4, "Cyan: Newton | Magenta: Tamesis", color='white', fontsize=9, ha='center')

    # --- SETUP AX2 (VOID) ---
    ax2.set_axis_off()
    ax2.set_title("Stage 4: Void Lensing (S_vac)", color='white', fontsize=12)
    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-2, 2)
    ax2.set_aspect('equal')
    
    void = Circle((0,0), 1.0, color='#111111', zorder=5)
    ax2.add_patch(void)
    
    n_lines = 14
    x_grid = np.linspace(-1.9, 1.9, n_lines)
    lines = []
    for i in range(n_lines):
        l, = ax2.plot([], [], color='gold', lw=1, alpha=0.5)
        lines.append(l)

    def update(frame):
        t = frame / 60.0
        
        # Update Galaxy
        theta_n = angles + w_newton_loop * t
        theta_e = angles + w_entropic_loop * t
        xn = radii_raw * np.cos(theta_n); yn = radii_raw * np.sin(theta_n)
        xe = radii_raw * np.cos(theta_e); ye = radii_raw * np.sin(theta_e)
        stars_newton.set_offsets(np.column_stack([xn, yn]))
        stars_entropic.set_offsets(np.column_stack([xe, ye]))
        
        # Update Void
        t_phase = t * 2 * np.pi
        strength = 0.4 * np.sin(t_phase)
        
        void_artists = []
        for i, x0 in enumerate(x_grid):
            y_vals = np.linspace(-1.9, 1.9, 50)
            x_vals = np.full_like(y_vals, x0)
            Lx, Ly = lensing_effect(x_vals, y_vals, strength)
            lines[i].set_data(Lx, Ly)
            lines[i].set_alpha(0.3 + 0.3 * np.abs(np.sin(t_phase)))
            void_artists.append(lines[i])

        return [stars_newton, stars_entropic, void] + void_artists

    anim = animation.FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    save_gif(anim, "PATH_A_Unified_Loop.gif")
    plt.close(fig)

if __name__ == "__main__":
    generate_galaxy_loop()
    generate_void_loop()
    generate_unified_loop()
