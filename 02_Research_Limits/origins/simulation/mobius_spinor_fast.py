import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def generate_mobius_animation_fast():
    """
    Optimized version: Faster generation (fewer frames).
    Simulates a Spinor (Spin-1/2) as a vector traversing a Mobius Strip.
    """
    print("Initializing Fast Animation...")
    
    # Setup Figure
    fig = plt.figure(figsize=(8, 6)) # Smaller figure
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')
    
    # 1. Create the Mobius Strip Mesh (Background)
    u_vals = np.linspace(0, 2*np.pi, 40) # Lower resolution mesh
    v_vals = np.linspace(-0.4, 0.4, 5)
    u, v = np.meshgrid(u_vals, v_vals)
    
    # Mobius equations (R=2)
    x = (2 + v * np.cos(u/2)) * np.cos(u)
    y = (2 + v * np.cos(u/2)) * np.sin(u)
    z = v * np.sin(u/2)
    
    # Plot Surface
    ax.plot_surface(x, y, z, alpha=0.2, color='cyan', edgecolor='gray', linewidth=0.1)
    
    # 2. Setup the Moving Vector
    arrow, = ax.plot([], [], [], 'r-', linewidth=3, label='Spinor Vector')
    point, = ax.plot([], [], [], 'ko', markersize=4)
    status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=10)
    
    def get_pos_and_normal(theta):
        u = theta % (2*np.pi) 
        x_p = 2 * np.cos(u)
        y_p = 2 * np.sin(u)
        z_p = 0
        
        alpha = theta / 2.0
        nx = np.cos(u) * np.sin(alpha) 
        ny = np.sin(u) * np.sin(alpha) 
        nz = np.cos(alpha)
        
        return (x_p, y_p, z_p), (nx, ny, nz)

    def init():
        arrow.set_data([], [])
        arrow.set_3d_properties([])
        return arrow, point, status_text

    def update(frame):
        # 80 frames for 4pi (720 deg)
        # Frame 0 to 80
        total_frames = 80
        theta = frame * (4 * np.pi / total_frames)
        
        pos, normal = get_pos_and_normal(theta)
        scale = 0.8
        
        line_x = [pos[0], pos[0] + normal[0]*scale]
        line_y = [pos[1], pos[1] + normal[1]*scale]
        line_z = [pos[2], pos[2] + normal[2]*scale]
        
        arrow.set_data(line_x, line_y)
        arrow.set_3d_properties(line_z)
        
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])
        
        degrees = np.degrees(theta)
        
        state = "|+>"
        if 90 < degrees < 270: state = "Twisting..."
        elif 270 <= degrees <= 450: state = "|-> (Flipped)"
        elif 450 < degrees < 630: state = "Restoring..."
        
        status_text.set_text(f"Angle: {degrees:.0f}\nState: {state}")
        
        return arrow, point, status_text

    # Set limits
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title("Spinor Topology (Mobius 720)", fontsize=12)
    
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Animate - Fewer frames for speed
    print("Generating frames...")
    ani = animation.FuncAnimation(fig, update, frames=81, init_func=init, blit=False)
    
    save_path = '../simulation/mobius_spinor_fast.gif'
    print(f"Saving to {save_path}...")
    ani.save(save_path, writer='pillow', fps=20) # 20 fps * 4s
    print("Done.")

if __name__ == "__main__":
    generate_mobius_animation_fast()
