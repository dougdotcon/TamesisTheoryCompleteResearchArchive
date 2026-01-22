
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def generate_looping_gif():
    print("Initializing Enhanced 3D Loop...")
    
    # Setup Figure
    fig = plt.figure(figsize=(10, 8), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d', facecolor='#050505')
    
    # Aesthetic adjustments
    ax.set_axis_off()
    ax.grid(False)
    
    num_particles = 3000
    
    # Base shapes
    # Two Lobes (Superposition)
    phi = np.random.uniform(0, 2*np.pi, num_particles)
    costheta = np.random.uniform(-1, 1, num_particles)
    u = np.random.uniform(0, 1, num_particles)
    
    theta = np.arccos(costheta)
    r = 1.0 * np.cbrt(u) # Uniform sphere volume
    
    # Lobe 1 centered at (-2, 0, 0)
    x1 = r * np.sin(theta) * np.cos(phi) - 2.0
    y1 = r * np.sin(theta) * np.sin(phi)
    z1 = r * np.cos(theta)
    
    # Lobe 2 centered at (2, 0, 0)
    x2 = r * np.sin(theta) * np.cos(phi) + 2.0
    y2 = r * np.sin(theta) * np.sin(phi)
    z2 = r * np.cos(theta)
    
    # Combined Quantum State (Half in each lobe)
    idx = int(num_particles/2)
    q_x = np.concatenate([x1[:idx], x2[:idx]])
    q_y = np.concatenate([y1[:idx], y2[:idx]])
    q_z = np.concatenate([z1[:idx], z2[:idx]])
    
    # Classical State (One dense sphere at 0,0,0)
    # Tighter radius for impact
    r_c = 0.5 * np.cbrt(u)
    c_x = r_c * np.sin(theta) * np.cos(phi)
    c_y = r_c * np.sin(theta) * np.sin(phi)
    c_z = r_c * np.cos(theta)
    
    # Animation Parameters
    total_frames = 90
    collapse_start = 30
    collapse_duration = 10
    expand_start = 70
    expand_duration = 20
    
    # Text objects
    title_text = ax.text2D(0.5, 0.9, "TAMESIS THEORY", transform=ax.transAxes, color='white', 
                          fontsize=20, fontweight='bold', ha='center')
    sub_text = ax.text2D(0.5, 0.85, "Quantum-Classical Transition", transform=ax.transAxes, color='gray', 
                        fontsize=12, ha='center')
    
    # Initialize scatter
    scatter = ax.scatter([], [], [], s=5, alpha=0.8, edgecolors='none')
    
    def update(frame):
        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_zlim(-4, 4)
        
        # Camera Rotation (Constant speed loop)
        angle = (frame / total_frames) * 360
        ax.view_init(elev=20, azim=angle)
        
        # State Logic
        # Phase 1: Superposition (Breathing)
        if frame < collapse_start:
            progress = frame / collapse_start
            # Subtle breathing
            scale = 1.0 + 0.05 * np.sin(progress * 4 * np.pi)
            
            curr_x = q_x * scale
            curr_y = q_y * scale
            curr_z = q_z * scale
            color = '#00ffff' # Cyan
            label = "STATE: SUPERPOSITION"
            
        # Phase 2: The COLLAPSE (Snapping together)
        elif frame < collapse_start + collapse_duration:
            t = (frame - collapse_start) / collapse_duration
            t_smooth = ease_in_out(t)
            
            # Interpolate positions
            curr_x = (1 - t_smooth) * q_x + t_smooth * c_x
            curr_y = (1 - t_smooth) * q_y + t_smooth * c_y
            curr_z = (1 - t_smooth) * q_z + t_smooth * c_z
            
            # Color transition Cyan -> Red
            # We'll just snap color for impact or blend
            if t < 0.5:
                color = '#00ffff'
                label = "COLLAPSING..."
            else:
                color = '#ff3333'
                label = "COLLAPSED"
                
        # Phase 3: Classical State (Stable)
        elif frame < expand_start:
            curr_x = c_x
            curr_y = c_y
            curr_z = c_z
            color = '#ff3333' # Red
            label = "STATE: CLASSICAL REALITY"
            
        # Phase 4: Reset (Splitting back) to loop
        else:
            t = (frame - expand_start) / expand_duration
            t_smooth = ease_in_out(t)
            
            curr_x = (1 - t_smooth) * c_x + t_smooth * q_x
            curr_y = (1 - t_smooth) * c_y + t_smooth * q_y
            curr_z = (1 - t_smooth) * c_z + t_smooth * q_z
            
            color = '#00ffff'
            label = "RESETTING..."
        
        # Plot
        ax.scatter(curr_x, curr_y, curr_z, c=color, s=4, alpha=0.7)
        
        # Re-add text (cleared)
        ax.text2D(0.5, 0.92, "TAMESIS THEORY", transform=ax.transAxes, color='white', 
                 fontsize=24, fontweight='bold', ha='center', fontfamily='sans-serif')
        ax.text2D(0.5, 0.05, label, transform=ax.transAxes, color=color, 
                 fontsize=16, ha='center', fontweight='bold', fontfamily='monospace')
        
        return scatter,
        
    print("Rendering loop...")
    anim = FuncAnimation(fig, update, frames=total_frames, interval=80)
    
    # Saving
    output = 'tamesis_loop.gif'
    anim.save(output, writer=PillowWriter(fps=20))
    print(f"Saved {output}")

if __name__ == '__main__':
    generate_looping_gif()
