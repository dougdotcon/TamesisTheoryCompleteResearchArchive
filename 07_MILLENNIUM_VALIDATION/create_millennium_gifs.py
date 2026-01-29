"""
MILLENNIUM PRIZE ANIMATIONS
============================
Creates looping GIF animations for each of the 6 Millennium Problems.
Uses matplotlib for frame generation and imageio for GIF creation.

Author: Tamesis Research Program
Date: January 29, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge, Arrow
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors
import os
import imageio.v2 as imageio
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("animations")
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_frames"
TEMP_DIR.mkdir(exist_ok=True)

# Common settings
FPS = 30
DURATION = 3  # seconds per loop
N_FRAMES = FPS * DURATION
DPI = 100
SIZE = (400, 400)  # pixels

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12


def clear_temp():
    """Clear temporary frames"""
    for f in TEMP_DIR.glob("*.png"):
        f.unlink()


# ============================================================
# 1. P vs NP - Thermodynamic Censorship
# Visualization: Energy barrier that cannot be crossed
# ============================================================
def create_pvsnp_animation():
    print("Creating P vs NP animation...")
    clear_temp()
    
    frames = []
    for i in range(N_FRAMES):
        t = i / N_FRAMES  # 0 to 1
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-0.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Energy landscape (double well potential)
        x = np.linspace(-2, 2, 200)
        # Barrier height oscillates
        barrier = 1.5 + 0.3 * np.sin(2 * np.pi * t)
        y = (x**2 - 1)**2 + 0.5
        
        # Draw landscape
        ax.fill_between(x, 0, y, color='#1a1a40', alpha=0.8)
        ax.plot(x, y, color='#00ff88', linewidth=2)
        
        # Ball trying to cross (oscillates but can't get over)
        ball_x = -1 + 0.5 * np.sin(2 * np.pi * t)
        ball_y = (ball_x**2 - 1)**2 + 0.5 + 0.1
        
        # Ball with glow
        for r, alpha in [(0.25, 0.1), (0.18, 0.2), (0.12, 0.5)]:
            circle = Circle((ball_x, ball_y), r, color='#ff6644', alpha=alpha)
            ax.add_patch(circle)
        circle = Circle((ball_x, ball_y), 0.08, color='#ffaa00', alpha=1)
        ax.add_patch(circle)
        
        # Barrier indicator (pulsing)
        barrier_alpha = 0.5 + 0.3 * np.sin(2 * np.pi * t)
        ax.axvline(x=0, color='#ff0000', alpha=barrier_alpha, linewidth=3, linestyle='--')
        
        # Labels
        ax.text(0, 2.3, 'P ≠ NP', color='#00ff88', fontsize=16, ha='center', fontweight='bold')
        ax.text(-1.2, 0.2, 'P', color='#44aaff', fontsize=14, ha='center', fontweight='bold')
        ax.text(1.2, 0.2, 'NP', color='#ff4444', fontsize=14, ha='center', fontweight='bold')
        ax.text(0, 1.8, '∞ Energy', color='#ff6666', fontsize=10, ha='center', alpha=barrier_alpha)
        
        # Save frame
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    # Create GIF
    imageio.mimsave(OUTPUT_DIR / "01_pvsnp_thermodynamic.gif", frames, fps=FPS, loop=0)
    print("  ✓ 01_pvsnp_thermodynamic.gif")


# ============================================================
# 2. Riemann Hypothesis - Spectral Entropy
# Visualization: Zeros aligning on critical line
# ============================================================
def create_riemann_animation():
    print("Creating Riemann animation...")
    clear_temp()
    
    frames = []
    np.random.seed(42)
    
    # Generate some "zeros" that will align
    n_zeros = 15
    initial_x = np.random.uniform(-0.3, 0.3, n_zeros)
    final_x = np.zeros(n_zeros)  # All align to x=0.5 (shown as 0)
    y_positions = np.linspace(-1.5, 1.5, n_zeros)
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        # Smooth easing
        ease = 0.5 - 0.5 * np.cos(np.pi * t)
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Critical line (glowing)
        for lw, alpha in [(8, 0.1), (4, 0.3), (2, 0.6)]:
            ax.axvline(x=0, color='#00ffff', alpha=alpha, linewidth=lw)
        
        # Critical strip background
        ax.axvspan(-0.5, 0.5, color='#002244', alpha=0.4)
        
        # Zeros moving towards critical line
        current_x = initial_x * (1 - ease) + final_x * ease
        
        for j, (x, y) in enumerate(zip(current_x, y_positions)):
            # Glow effect
            glow_size = 0.15 + 0.05 * np.sin(2 * np.pi * (t + j/n_zeros))
            for r, alpha in [(glow_size, 0.2), (glow_size*0.7, 0.4)]:
                circle = Circle((x, y), r, color='#ffaa00', alpha=alpha)
                ax.add_patch(circle)
            circle = Circle((x, y), 0.05, color='#ffffff', alpha=1)
            ax.add_patch(circle)
        
        # Labels
        ax.text(0, 1.85, 'Riemann ζ(s)', color='#00ffff', fontsize=14, ha='center', fontweight='bold')
        ax.text(0, -1.85, 'Re(s) = ½', color='#ffaa00', fontsize=12, ha='center')
        
        # Entropy indicator
        entropy = 1.0 - ease * 0.7  # Decreases as zeros align
        ax.text(-1.3, 1.6, f'S = {entropy:.2f}', color='#ff6666', fontsize=10)
        
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    # Reverse for perfect loop
    frames = frames + frames[::-1]
    imageio.mimsave(OUTPUT_DIR / "02_riemann_spectral.gif", frames, fps=FPS, loop=0)
    print("  ✓ 02_riemann_spectral.gif")


# ============================================================
# 3. Yang-Mills - Mass Gap
# Visualization: Gluon field with mass gap emergence
# ============================================================
def create_yangmills_animation():
    print("Creating Yang-Mills animation...")
    clear_temp()
    
    frames = []
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Central gluon ball (pulsing)
        pulse = 0.8 + 0.2 * np.sin(2 * np.pi * t)
        
        # Glow layers
        for r, alpha in [(1.2*pulse, 0.1), (0.9*pulse, 0.2), (0.6*pulse, 0.4)]:
            circle = Circle((0, 0), r, color='#ff4400', alpha=alpha)
            ax.add_patch(circle)
        
        # Core
        circle = Circle((0, 0), 0.3*pulse, color='#ffff00', alpha=0.9)
        ax.add_patch(circle)
        
        # Rotating gluon field lines
        n_lines = 8
        for j in range(n_lines):
            angle = 2 * np.pi * j / n_lines + 2 * np.pi * t
            r_inner = 0.4 * pulse
            r_outer = 1.5
            
            # Spiral field line
            theta = np.linspace(0, np.pi, 50)
            r = r_inner + (r_outer - r_inner) * theta / np.pi
            x = r * np.cos(angle + theta * 0.5)
            y = r * np.sin(angle + theta * 0.5)
            
            # Color gradient
            colors = plt.cm.hot(np.linspace(0.3, 0.9, len(theta)-1))
            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, colors=colors, linewidth=2, alpha=0.7)
            ax.add_collection(lc)
        
        # Mass gap indicator
        gap_y = -1.7
        gap_width = 0.5 + 0.2 * np.sin(2 * np.pi * t)
        ax.plot([-gap_width, gap_width], [gap_y, gap_y], color='#00ff00', linewidth=4)
        ax.text(0, gap_y - 0.25, f'Δm > 0', color='#00ff00', fontsize=12, ha='center', fontweight='bold')
        
        # Title
        ax.text(0, 1.8, 'Yang-Mills', color='#ff8800', fontsize=14, ha='center', fontweight='bold')
        
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    imageio.mimsave(OUTPUT_DIR / "03_yangmills_massgap.gif", frames, fps=FPS, loop=0)
    print("  ✓ 03_yangmills_massgap.gif")


# ============================================================
# 4. Navier-Stokes - Structural Regulator
# Visualization: Turbulence being regulated/smoothed
# ============================================================
def create_navierstokes_animation():
    print("Creating Navier-Stokes animation...")
    clear_temp()
    
    frames = []
    np.random.seed(123)
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Create flow field
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        
        # Velocity field with time-varying turbulence
        turbulence = 0.5 + 0.5 * np.sin(2 * np.pi * t)  # oscillates
        
        # Base flow + turbulent perturbation
        U = -Y + turbulence * 0.5 * np.sin(3*X + 2*np.pi*t) * np.cos(2*Y)
        V = X + turbulence * 0.5 * np.cos(2*X) * np.sin(3*Y + 2*np.pi*t)
        
        # Normalize
        speed = np.sqrt(U**2 + V**2)
        U = U / (speed + 0.1)
        V = V / (speed + 0.1)
        
        # Color by speed
        colors = plt.cm.cool(speed / speed.max())
        
        # Streamplot
        ax.streamplot(X, Y, U, V, color=speed, cmap='cool', 
                     density=1.5, linewidth=1, arrowsize=0.8)
        
        # Central vortex indicator
        vortex_size = 0.3 + 0.1 * turbulence
        circle = Circle((0, 0), vortex_size, fill=False, color='#ff4444', 
                        linewidth=2, linestyle='--')
        ax.add_patch(circle)
        
        # Regulator indicator
        reg_alpha = 0.7 - 0.3 * turbulence
        ax.text(0, 1.8, 'Navier-Stokes', color='#00aaff', fontsize=14, 
                ha='center', fontweight='bold')
        ax.text(0, -1.8, f'ω < ∞', color='#00ff88', fontsize=12, 
                ha='center', alpha=reg_alpha + 0.3)
        
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    imageio.mimsave(OUTPUT_DIR / "04_navierstokes_flow.gif", frames, fps=FPS, loop=0)
    print("  ✓ 04_navierstokes_flow.gif")


# ============================================================
# 5. BSD Conjecture - Information Conservation
# Visualization: Elliptic curve with rational points
# ============================================================
def create_bsd_animation():
    print("Creating BSD animation...")
    clear_temp()
    
    frames = []
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Elliptic curve y^2 = x^3 - x (with animation parameter)
        x_pos = np.linspace(0.01, 2.2, 200)
        x_neg = np.linspace(-1.05, -0.01, 200)
        
        # Time-varying parameter
        a = -1 + 0.2 * np.sin(2 * np.pi * t)
        
        # Positive branch
        y_sq = x_pos**3 + a*x_pos
        mask = y_sq >= 0
        y_pos = np.sqrt(np.maximum(y_sq, 0))
        ax.plot(x_pos[mask], y_pos[mask], color='#00ffaa', linewidth=2)
        ax.plot(x_pos[mask], -y_pos[mask], color='#00ffaa', linewidth=2)
        
        # Negative branch (oval)
        y_sq_neg = x_neg**3 + a*x_neg
        mask_neg = y_sq_neg >= 0
        if np.any(mask_neg):
            y_neg = np.sqrt(np.maximum(y_sq_neg, 0))
            ax.plot(x_neg[mask_neg], y_neg[mask_neg], color='#00ffaa', linewidth=2)
            ax.plot(x_neg[mask_neg], -y_neg[mask_neg], color='#00ffaa', linewidth=2)
        
        # Rational points (pulsing)
        rational_points = [(-1, 0), (0, 0), (1, 0)]
        for j, (px, py) in enumerate(rational_points):
            pulse = 0.12 + 0.04 * np.sin(2 * np.pi * (t + j/3))
            # Glow
            for r, alpha in [(pulse*2, 0.2), (pulse*1.5, 0.4)]:
                circle = Circle((px, py), r, color='#ffaa00', alpha=alpha)
                ax.add_patch(circle)
            circle = Circle((px, py), pulse*0.5, color='#ffffff')
            ax.add_patch(circle)
        
        # L-function indicator
        L_val = 1.0 + 0.3 * np.sin(2 * np.pi * t)
        ax.text(1.5, 2.0, f'L(E,1)', color='#ff8844', fontsize=11, ha='center')
        
        # Rank indicator
        ax.text(0, -2.2, 'rank E(ℚ) = ord L(E,s)', color='#44aaff', fontsize=10, ha='center')
        
        # Title
        ax.text(0, 2.2, 'BSD', color='#00ffaa', fontsize=16, ha='center', fontweight='bold')
        
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    imageio.mimsave(OUTPUT_DIR / "05_bsd_elliptic.gif", frames, fps=FPS, loop=0)
    print("  ✓ 05_bsd_elliptic.gif")


# ============================================================
# 6. Hodge Conjecture - Triple Lock / Motivic Rigidity
# Visualization: Three interlocking rings
# ============================================================
def create_hodge_animation():
    print("Creating Hodge animation...")
    clear_temp()
    
    frames = []
    
    for i in range(N_FRAMES):
        t = i / N_FRAMES
        
        fig, ax = plt.subplots(figsize=(4, 4), dpi=DPI)
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#0a0a20')
        fig.patch.set_facecolor('#0a0a20')
        
        # Three rings representing the triple lock
        # Ring positions rotate slightly
        angle_offset = 0.2 * np.sin(2 * np.pi * t)
        
        ring_params = [
            (0, 1, '#ff4444', '(p,p)'),      # Top - red
            (-0.87, -0.5, '#44ff44', 'ℚ'),   # Bottom left - green  
            (0.87, -0.5, '#4444ff', 'Rigid'), # Bottom right - blue
        ]
        
        theta = np.linspace(0, 2*np.pi, 100)
        ring_radius = 1.0
        tube_radius = 0.15
        
        for (cx, cy, color, label) in ring_params:
            # Ring position with slight rotation
            cx_rot = cx * np.cos(angle_offset) - cy * np.sin(angle_offset) * 0.1
            cy_rot = cy + 0.1 * np.sin(2 * np.pi * t)
            
            # Draw ring as thick circle
            for dr, alpha in [(0.25, 0.2), (0.18, 0.4), (0.12, 0.7)]:
                ring_x = cx_rot + ring_radius * np.cos(theta)
                ring_y = cy_rot + ring_radius * np.sin(theta)
                ax.plot(ring_x, ring_y, color=color, linewidth=8*dr/0.12, alpha=alpha)
            
            # Label
            ax.text(cx_rot, cy_rot, label, color='white', fontsize=10, 
                   ha='center', va='center', fontweight='bold')
        
        # Central intersection point (algebraic cycle)
        pulse = 0.15 + 0.08 * np.sin(2 * np.pi * t * 2)
        for r, alpha in [(pulse*3, 0.2), (pulse*2, 0.4), (pulse, 0.8)]:
            circle = Circle((0, 0), r, color='#ffff00', alpha=alpha)
            ax.add_patch(circle)
        
        # Title
        ax.text(0, 2.2, 'Hodge', color='#aa88ff', fontsize=16, ha='center', fontweight='bold')
        ax.text(0, -2.2, 'Triple Lock', color='#ffaa00', fontsize=11, ha='center')
        
        frame_path = TEMP_DIR / f"frame_{i:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(imageio.imread(frame_path))
        plt.close()
    
    imageio.mimsave(OUTPUT_DIR / "06_hodge_triplelock.gif", frames, fps=FPS, loop=0)
    print("  ✓ 06_hodge_triplelock.gif")


# ============================================================
# Create the 2x3 grid of all animations
# ============================================================
def create_grid():
    print("\nCreating 2x3 grid...")
    
    # Load all GIFs
    gif_files = [
        "01_pvsnp_thermodynamic.gif",
        "02_riemann_spectral.gif",
        "03_yangmills_massgap.gif",
        "04_navierstokes_flow.gif",
        "05_bsd_elliptic.gif",
        "06_hodge_triplelock.gif",
    ]
    
    # Read all GIFs
    gifs = []
    for gf in gif_files:
        gif_path = OUTPUT_DIR / gf
        if gif_path.exists():
            gifs.append(imageio.mimread(gif_path))
        else:
            print(f"  Warning: {gf} not found")
            return
    
    # Find minimum number of frames
    min_frames = min(len(g) for g in gifs)
    
    # Create grid frames
    grid_frames = []
    for frame_idx in range(min_frames):
        # Create 2x3 grid
        fig, axes = plt.subplots(2, 3, figsize=(12, 8), dpi=100)
        fig.patch.set_facecolor('#0a0a20')
        
        titles = ['P vs NP', 'Riemann', 'Yang-Mills', 
                  'Navier-Stokes', 'BSD', 'Hodge']
        
        for idx, (ax, gif, title) in enumerate(zip(axes.flat, gifs, titles)):
            ax.imshow(gif[frame_idx])
            ax.axis('off')
            ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=5)
        
        plt.tight_layout(pad=0.5)
        
        # Save to temp
        frame_path = TEMP_DIR / f"grid_{frame_idx:04d}.png"
        plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none')
        grid_frames.append(imageio.imread(frame_path))
        plt.close()
    
    # Save grid GIF
    imageio.mimsave(OUTPUT_DIR / "millennium_grid_2x3.gif", grid_frames, fps=FPS, loop=0)
    print("  ✓ millennium_grid_2x3.gif")


# ============================================================
# Main execution
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("MILLENNIUM PRIZE ANIMATIONS")
    print("=" * 60)
    print()
    
    # Create individual animations
    create_pvsnp_animation()
    create_riemann_animation()
    create_yangmills_animation()
    create_navierstokes_animation()
    create_bsd_animation()
    create_hodge_animation()
    
    # Create combined grid
    create_grid()
    
    # Cleanup temp frames
    print("\nCleaning up temporary files...")
    for f in TEMP_DIR.glob("*.png"):
        f.unlink()
    TEMP_DIR.rmdir()
    
    print()
    print("=" * 60)
    print("COMPLETE! All animations saved to:", OUTPUT_DIR)
    print("=" * 60)
    print("\nGenerated files:")
    for f in sorted(OUTPUT_DIR.glob("*.gif")):
        print(f"  • {f.name}")
