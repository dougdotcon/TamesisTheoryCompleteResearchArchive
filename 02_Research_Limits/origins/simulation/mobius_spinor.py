import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def generate_mobius_animation():
    """
    Simulates a Spinor (Spin-1/2) as a vector traversing a Mobius Strip.
    
    Why: 
    - A Mobius strip has a non-orientable topology.
    - One full loop (360 deg) along the center line returns you to the 'starting point' 
      but on the OPPOSTIE side of the surface.
    - The normal vector is flipped (multiplied by -1).
    - This visualizes why Spinors need 720 deg (2 loops) to return to the original state.
    
    The User's Request: "Visualization of spin 360, which looks like 180 spin"
    - At 360 deg (1 loop), the vector is flipped (like a 180 deg rotation of a vector).
    """
    
    # Setup Figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')
    
    # 1. Create the Mobius Strip Mesh (Background)
    # Parameterization:
    # u in [0, 2pi] (loop angle)
    # v in [-1, 1] (width)
    u_vals = np.linspace(0, 2*np.pi, 60)
    v_vals = np.linspace(-0.4, 0.4, 10)
    u, v = np.meshgrid(u_vals, v_vals)
    
    # Mobius equations
    # R = 2
    x = (2 + v * np.cos(u/2)) * np.cos(u)
    y = (2 + v * np.cos(u/2)) * np.sin(u)
    z = v * np.sin(u/2)
    
    # Plot Surface
    ax.plot_surface(x, y, z, alpha=0.3, color='cyan', edgecolor='gray', linewidth=0.2)
    
    # 2. Setup the Moving Vector (The Spinor)
    # Trajectory along center line (v=0)
    # Vector points along the local Normal of the strip
    
    # Initial Arrow
    arrow, = ax.plot([], [], [], 'r-', linewidth=4, label='Spinor Vector')
    point, = ax.plot([], [], [], 'ko', markersize=5)
    
    # Text
    status_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12)
    
    def get_pos_and_normal(theta):
        # Position on center line (v=0)
        # We go up to 4pi (720 deg)
        # Note: The strip mesh is only 2pi. The particle travels it twice.
        
        # Effective angle on the strip geometry
        u = theta % (2*np.pi) 
        
        # Pos
        x_p = 2 * np.cos(u)
        y_p = 2 * np.sin(u)
        z_p = 0
        
        # Normal vector calculation
        # Tangent T = (-sin u, cos u, 0) approx
        # The 'twist' vector depends on u/2.
        # Let's use the explicit normal of the Mobius surface twist.
        # A normal at center points "up" then twists to "down".
        
        # Twist angle alpha = theta / 2
        # In the local frame of the line:
        # Radial vector R = (cos u, sin u, 0)
        # Vertical vector K = (0, 0, 1)
        # The strip twists around the Tangent.
        # Normal rotates in the (R, K) plane.
        
        alpha = theta / 2.0
        nx = np.cos(u) * np.sin(alpha) 
        ny = np.sin(u) * np.sin(alpha) 
        nz = np.cos(alpha)
        
        # Note: 
        # Theta = 0: Normal = (0,0,1) UP
        # Theta = 360 (2pi): Normal = (0,0,-1) DOWN (Flipped!)
        # Theta = 720 (4pi): Normal = (0,0,1) UP (Restored)
        
        return (x_p, y_p, z_p), (nx, ny, nz)

    def init():
        arrow.set_data([], [])
        arrow.set_3d_properties([])
        return arrow, point, status_text

    def update(frame):
        # Frame 0 to 200 corresponds to 0 to 4pi
        theta = frame * (4 * np.pi / 200)
        
        pos, normal = get_pos_and_normal(theta)
        scale = 0.8
        
        # Draw Arrow
        # From pos to pos + normal
        line_x = [pos[0], pos[0] + normal[0]*scale]
        line_y = [pos[1], pos[1] + normal[1]*scale]
        line_z = [pos[2], pos[2] + normal[2]*scale]
        
        arrow.set_data(line_x, line_y)
        arrow.set_3d_properties(line_z)
        
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])
        
        # Status Text
        degrees = np.degrees(theta)
        
        state_desc = "Identifying..."
        if degrees < 10: state_desc = "Start: State |+>"
        elif 350 < degrees < 370: state_desc = "360 Deg: State |-> (Flipped!)\nLooks like 180 vector rotation"
        elif degrees > 710: state_desc = "720 Deg: State |+> (Restored)"
        else: state_desc = "Twisting..."
        
        status_text.set_text(f"Rotation: {degrees:.0f} deg\n{state_desc}")
        
        return arrow, point, status_text

    # Set limits
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title("Spinor Topology: The Mobius Phase", fontsize=16)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    # Remove pane background for cleaner look
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Animate
    # Frames: 200 frames for 720 degrees
    ani = animation.FuncAnimation(fig, update, frames=200, init_func=init, blit=False, interval=50)
    
    # Save
    print("Generating animation... this may take a moment.")
    save_path = '../simulation/mobius_spinor.gif'
    ani.save(save_path, writer='pillow', fps=30)
    print(f"Animation saved to {save_path}")

if __name__ == "__main__":
    generate_mobius_animation()
