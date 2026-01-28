import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def dirac_belt_animation():
    """
    Simulates the Dirac Belt Trick (Plate Trick).
    
    Setup:
    - A central Cube (The Spinor) rotates around Z axis.
    - 4 Belts connect the Cube to a fixed outer frame.
    - As the cube rotates, the belts twist.
    
    Topology:
    - 360 deg rotation: Belts are twisted (-1 phase). Cannot be undone without moving cube.
    - 720 deg rotation: Belts are double twisted. Isotopic to 0 twist! Can be "combed" out.
    
    This animation shows the accumulation of twist.
    Visualizing the 'unknotting' move is mathematically complex for a procedural script,
    so we will visualize the 'Twist Density' accumulating and then resetting at 720.
    """
    
    print("Generating Dirac Belt animation...")
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('white')
    
    # Parameters
    cube_size = 0.4
    belt_length = 2.0
    
    # Cube Vertices (Center at 0,0,0)
    s = cube_size / 2
    cube_verts_base = np.array([
        [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s], # Bottom
        [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]      # Top
    ])
    
    # Faces indices
    faces = [
        [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], 
        [2, 3, 7, 6], [1, 2, 6, 5], [4, 7, 3, 0]
    ]
    
    # Belts (Ribbons)
    # Belt 1: From Cube Right (+X) to Wall (+X)
    # Belt 2: From Cube Left (-X) to Wall (-X)
    # Belt 3: From Cube Front (+Y) to Wall (+Y)
    # Belt 4: From Cube Back (-Y) to Wall (-Y)
    
    def get_rotated_cube(angle):
        c, s = np.cos(angle), np.sin(angle)
        Rz = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
        return np.dot(cube_verts_base, Rz.T)
        
    def get_belt_surface(start_pt, end_pt, twist_angle, axis):
        """
        Generates a ribbon mesh between start_pt (rotating) and end_pt (fixed).
        Twist varies linearly along the length.
        """
        N = 20
        t = np.linspace(0, 1, N) # Parameter along belt
        
        # Center line
        P = np.outer(1-t, start_pt) + np.outer(t, end_pt)
        
        # Ribbon width vector
        # At start (cube), it rotates with the cube.
        # At end (wall), it is fixed.
        
        width = 0.3
        
        # Local rotation angle at distance t
        # Crucial: The twist is distributed along the belt
        # At t=0 (Cube), angle = twist_angle
        # At t=1 (Wall), angle = 0
        local_theta = twist_angle * (1 - t)
        
        X = np.zeros((N, 3))
        Y = np.zeros((N, 3))
        Z = np.zeros((N, 3))
        
        for i in range(N):
            th = local_theta[i]
            cx, sx = np.cos(th), np.sin(th)
            
            # Base orientation depending on axis
            if axis == 'x': # Belt along X
                # Width is along Y initially
                # Rotated by th around X? No, around Z (the belt axis is X)
                # No, the cube rotates around Z. The belt twists around X.
                # Actually, the belt plane rotates around Z.
                
                # Let's simplify:
                # Vector perpendicular to belt axis (Z-axis is up)
                # At cube, normal is rotated by twist_angle around Z.
                # At wall, normal is y-axis (fixed).
                
                # Wait, this is tricky. 
                # Let's just rotate the 'width vector' around the belt axis.
                # Belt axis is from start to end.
                
                pass
                
        # Alternative simple ribbon:
        # Just 2 lines
        ribbon_x = []
        ribbon_y = []
        ribbon_z = []
        
        return P # Placeholder
        
    # Let's try a simpler visualization:
    # Just show the Cube and lines representing the twist state.
    
    line_cube_x, = ax.plot([], [], [], 'k-', lw=2)
    belts_lines = [ax.plot([], [], [], 'b-', lw=2, alpha=0.7)[0] for _ in range(4)]
    
    txt_status = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)

    def init():
        return [line_cube_x] + belts_lines + [txt_status]

    def update(frame):
        # 0 to 720 degrees
        angle = np.radians(frame * 4) # Speed
        
        # Cube
        v = get_rotated_cube(angle)
        
        # Draw Cube edges (simplified)
        # Just draw a few loops
        edges_x = [v[0,0], v[1,0], v[2,0], v[3,0], v[0,0], v[4,0], v[5,0], v[1,0]]
        edges_y = [v[0,1], v[1,1], v[2,1], v[3,1], v[0,1], v[4,1], v[5,1], v[1,1]]
        edges_z = [v[0,2], v[1,2], v[2,2], v[3,2], v[0,2], v[4,2], v[5,2], v[1,2]]
        line_cube_x.set_data(edges_x, edges_y)
        line_cube_x.set_3d_properties(edges_z)
        
        # Belts
        # Connect center of cube faces to fixed walls at distance 2
        
        # Cube Face Centers
        # Right (+X local) -> Rotates
        c, s = np.cos(angle), np.sin(angle)
        
        # Anchor points on Cube (rotating)
        anchors = [
            np.array([cube_size/2 * c, cube_size/2 * s, 0]),   # +X face (rotated)
            np.array([-cube_size/2 * c, -cube_size/2 * s, 0]), # -X face
            np.array([-cube_size/2 * s, cube_size/2 * c, 0]),  # +Y face
            np.array([cube_size/2 * s, -cube_size/2 * c, 0])   # -Y face
        ]
        
        # Fixed points on Walls
        walls = [
            np.array([2, 0, 0]),
            np.array([-2, 0, 0]),
            np.array([0, 2, 0]),
            np.array([0, -2, 0])
        ]
        
        # Draw ribbons with twist
        for i in range(4):
            # Parametric curve for twisting ribbon
            # Line from anchor to wall
            # Add a 'spiral' to it to show twist?
            
            p0 = anchors[i]
            p1 = walls[i]
            
            num_points = 20
            t_vals = np.linspace(0, 1, num_points)
            
            # Line center
            lx = (1-t_vals)*p0[0] + t_vals*p1[0]
            ly = (1-t_vals)*p0[1] + t_vals*p1[1]
            lz = (1-t_vals)*p0[2] + t_vals*p1[2]
            
            # Add Twist
            # Twist amount: -angle (to counteract rotation? or show accumulation?)
            # Let's show accumulation. Twist = angle * (1-t)
            # Modulation: At 720, we want it to look 'straight' again?
            # No, physically it IS twisted at 720. 
            # The 'Trick' is that you can move the belt over the cube.
            # We can't easily animate that.
            # So we will show the twist accumulation.
            
            # Visualize twist as a helix amplitude around the belt
            twist_phase = angle * (1 - t_vals) 
            
            # Amplitude vector perpendicular to belt
            # Belt 0 is along X approx. Perpendicular is Z and Y.
            
            if i < 2: # X axis belts
                dx = 0
                dy = 0.2 * np.cos(twist_phase)
                dz = 0.2 * np.sin(twist_phase)
            else: # Y axis belts
                dx = 0.2 * np.cos(twist_phase)
                dy = 0
                dz = 0.2 * np.sin(twist_phase)
                
            belts_lines[i].set_data(lx + dx, ly + dy)
            belts_lines[i].set_3d_properties(lz + dz)
            
        deg = np.degrees(angle)
        state_str = "Twisting..."
        if deg > 350 and deg < 370: state_str = "360: TANGLED (-1)"
        if deg > 710: state_str = "720: IDENITY (TOPOLOGICALLY UNTANGLED)"
        
        txt_status.set_text(f"Rotation: {deg:.0f}\n{state_str}")
        
        return [line_cube_x] + belts_lines + [txt_status]

    # Limits
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_title("Dirac Belt Trick: Spin-1/2 Topology\nCube rotates 720 degrees", fontsize=14)
    
    # Animate
    # 0 to 720 deg. 
    # 4 deg per frame -> 180 frames.
    ani = animation.FuncAnimation(fig, update, frames=181, init_func=init, blit=False)
    
    save_path = '../simulation/dirac_belt.gif'
    print(f"Saving animation to {save_path}...")
    ani.save(save_path, writer='pillow', fps=30)
    print("Done.")

if __name__ == "__main__":
    dirac_belt_animation()
