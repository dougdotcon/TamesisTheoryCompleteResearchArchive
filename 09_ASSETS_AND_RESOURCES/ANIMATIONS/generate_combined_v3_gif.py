
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from matplotlib.collections import LineCollection
from matplotlib.animation import PillowWriter

# Add Kernel v3 path just in case
sys.path.append(os.path.join(os.path.dirname(__file__), '../KERNEL_V3_ENTROPIC_NETWORK'))

def saturation_model(x, rho_max, rate):
    return rho_max * (1 - np.exp(-rate * x))

def generate_synchronized_gif():
    print("Initializing SYNCHRONIZED Animation Generation...")
    
    # ==========================
    # 1. DATA & TIMELINE
    # ==========================
    FRAMES = 120
    time_axis = np.linspace(-4, 4, FRAMES) # t from -4 to 4 (The Bounce Window)
    
    # Entropy Data (Bounce)
    entropy_profile = []
    for t in time_axis:
        if t < 0: S = 100 + 10 * abs(t) 
        else: S = 100 + 5 * t 
        if abs(t) < 1.0: S -= 50 * (1.0 - abs(t)) 
        entropy_profile.append(S)
    
    # Saturation Data (Background Curve)
    E_space = np.linspace(0, 10, 100)
    rho_space = saturation_model(E_space, 200, 0.5)

    # Visual Nodes
    N_nodes = 80 # More nodes for cinematic feel
    np.random.seed(42)
    vis_angles = np.random.rand(N_nodes) * 2 * np.pi
    # Elliptical distribution for 16:9? No, just render in a wide box.
    vis_base_radii = np.random.rand(N_nodes) * 0.8 + 0.2

    # ==========================
    # 2. PLOT SETUP
    # ==========================
    fig = plt.figure(figsize=(12, 12)) # Wide and Tall
    fig.patch.set_facecolor('white')
    
    # heights: Top Graphs (1), Bottom Visual (1.5)
    gs = GridSpec(2, 2, height_ratios=[1, 1.5], figure=fig)
    
    ax1 = fig.add_subplot(gs[0, 0]) # Saturation
    ax2 = fig.add_subplot(gs[0, 1]) # Bounce
    ax3 = fig.add_subplot(gs[1, :]) # Visual (Full Width)
    
    fig.suptitle('THE ENTROPIC BOUNCE: SYNCHRONIZED SIMULATION\nKernel v3 Singularity Resolution', fontsize=18, fontweight='bold', color='#002147')

    # --- Plot 1: Saturation (Phase Space) ---
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 220)
    ax1.set_xlabel('Energy Density (Temperature)', fontweight='bold')
    ax1.set_ylabel('Connectivity Density (bits/Vol)', fontweight='bold')
    ax1.set_title('state.density_saturation', fontsize=12, fontname='monospace', color='navy')
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.plot(E_space, rho_space, 'b--', linewidth=1, alpha=0.5, label='Theory Limit')
    ax1.axhline(y=200, color='green', linestyle=':', label='Bekenstein Bound')
    
    # The Active State Dot
    sat_dot, = ax1.plot([], [], 'ro', markersize=10, markeredgecolor='black', label='Current State')
    sat_trail, = ax1.plot([], [], 'r-', linewidth=2, alpha=0.6)
    ax1.legend(loc='lower right')

    # --- Plot 2: Bounce (Time Evolution) ---
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(40, 200)
    ax2.set_xlabel('Cosmic Time (t)', fontweight='bold')
    ax2.set_ylabel('System Entropy (S)', fontweight='bold')
    ax2.set_title('history.entropy_evolution', fontsize=12, fontname='monospace', color='navy')
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.plot(time_axis, entropy_profile, color='gray', linewidth=3, alpha=0.3) # Background ghost path
    
    # The Active State
    bounce_line, = ax2.plot([], [], color='purple', linewidth=3)
    bounce_dot, = ax2.plot([], [], 'o', color='purple', markersize=10)
    time_cursor = ax2.axvline(x=-4, color='k', linestyle='--', alpha=0.8)

    # --- Plot 3: Visual Simulation (Cinematic 16:9) ---
    ax3.set_facecolor('black')
    ax3.set_title('visual.spacetime_geometry', fontsize=12, fontname='monospace', color='black', y=0.95)
    # Removing axes for immersion
    ax3.set_xticks([])
    ax3.set_yticks([])
    # 16:9 aspect ratio limits
    # x: -1.6 to 1.6, y: -0.9 to 0.9
    ax3.set_xlim(-1.8, 1.8) 
    ax3.set_ylim(-1.0, 1.0)
    ax3.set_aspect('equal')
    
    # Add a background "Horizon" circle
    horizon = plt.Circle((0,0), 0.1, color='white', fill=False, linestyle='--', alpha=0.3)
    ax3.add_patch(horizon)
    
    vis_nodes = ax3.scatter([], [], s=40, zorder=10)
    vis_lines = LineCollection([], linewidths=0.8, zorder=5)
    ax3.add_collection(vis_lines)
    
    # Status Text on visual
    status_text = ax3.text(0, 0.9, "", color='white', ha='center', fontsize=14, fontweight='bold', bbox=dict(facecolor='black', alpha=0.7, edgecolor='none'))

    # ==========================
    # 3. UPDATE LOGIC
    # ==========================
    def update(frame):
        # Current Time t
        t = time_axis[frame]
        
        # --- PHYSICS MAPPING ---
        # 1. Contraction/Expansion Factor (Scale)
        # At t=0, scale is min (0.2). At t=4, scale is max (1.5).
        # Use a smooth Gaussian-like dip or absolute value
        # scale = 0.2 + 0.3 * |t|
        scale = 0.2 + 0.35 * abs(t)
        
        # 2. Energy/Temperature Mapping (Inverse to Scale)
        # Small scale = High Temp.
        # E ~ 1 / scale (roughly)
        # Let's map t=0 -> E=10, t=4 -> E=0
        temp_factor = np.exp(-0.5 * t**2) # Gaussian peak at t=0
        current_E = 10.0 * temp_factor
        
        # 3. Calculate Density from E
        current_rho = saturation_model(current_E, 200, 0.5)
        
        # --- UPDATE PLOT 1 (Saturation) ---
        sat_dot.set_data([current_E], [current_rho])
        # Trail? Maybe just the dot moving on the dashed line is cleaner
        
        # --- UPDATE PLOT 2 (Bounce) ---
        # Show history up to now
        bounce_line.set_data(time_axis[:frame+1], entropy_profile[:frame+1])
        bounce_dot.set_data([t], [entropy_profile[frame]])
        time_cursor.set_xdata([t])

        # --- UPDATE PLOT 3 (Visual) ---
        # Positions
        current_radii = vis_base_radii * scale * 2.5 # multiplier to fill 16:9
        # Rotation
        current_angles = vis_angles + t * 0.5
        xs = current_radii * np.cos(current_angles)
        ys = current_radii * np.sin(current_angles)
        
        # Color/Heat
        # High Density (t near 0) -> HOT (Red/White)
        # Low Density -> COLD (Blue/Dark)
        heat = temp_factor # 0 to 1
        node_colors = plt.cm.magma(0.3 + 0.7*heat)
        vis_nodes.set_offsets(np.column_stack([xs, ys]))
        vis_nodes.set_color(node_colors)
        vis_nodes.set_sizes(np.ones(N_nodes) * (20 + 60*heat))
        
        # Connections
        # Connections form when dense (t near 0). Break when expanding.
        # We check distances in the SCALED space.
        # But to show "Structure", lines should exist.
        # Let's simple connect neighbors.
        segments = []
        colors = []
        phys_threshold = 0.5 # Fixed distance in visual space
        
        # Optimization: Only connect if close
        # To make it look "connected" at the bounce and "fragmented" at expansion
        
        # Just loop a subset or optimize? N=80 is small enough for O(N^2) ~ 3200 checks * 120 frames. Should be < 10s render.
        # Let's do it.
        xy = np.column_stack([xs, ys])
        
        # Only check if scale is small enough to have connections?
        # No, check all.
        count = 0
        for i in range(N_nodes):
            for j in range(i+1, N_nodes):
                # Quick check
                if abs(xs[i]-xs[j]) > phys_threshold: continue
                
                dist = np.sqrt((xs[i]-xs[j])**2 + (ys[i]-ys[j])**2)
                if dist < phys_threshold:
                    segments.append([(xs[i], ys[i]), (xs[j], ys[j])])
                    # Alpha depends on dist and HEAT
                    alpha = (1.0 - (dist/phys_threshold)) * (0.3 + 0.7*heat)
                    rgba = list(plt.cm.magma(0.3 + 0.7*heat))
                    rgba[3] = alpha
                    colors.append(rgba)
                    count += 1
                    if count > 300: break # Limiter for aesthetic cleanliness
            if count > 300: break
        
        vis_lines.set_segments(segments)
        vis_lines.set_color(colors)
        
        # Horizon pulse
        horizon.set_radius(0.1 + 0.05*np.sin(t*5))
        horizon.set_color(plt.cm.magma(heat))
        
        # Text
        if t < -0.5:
            status = "PHASE: CONTRACTION"
        elif t > 0.5:
            status = "PHASE: EXPANSION"
        else:
            status = "*** CRITICAL BOUNCE (t=0) ***"
        status_text.set_text(status)

        return sat_dot, bounce_line, bounce_dot, time_cursor, vis_nodes, vis_lines, status_text

    # Draw
    anim = animation.FuncAnimation(fig, update, frames=FRAMES, interval=40, blit=False) # 40ms = 25fps
    
    output_path = os.path.join(os.path.dirname(__file__), 'KERNEL_V3_Combined_Showcase.gif')
    print(f"Rendering Synchronized GIF to {output_path}...")
    anim.save(output_path, writer=PillowWriter(fps=25))
    print("Done!")

if __name__ == "__main__":
    generate_synchronized_gif()
