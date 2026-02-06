import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Configuração Estética "Sci-Fi"
plt.style.use('dark_background')

OUTPUT_DIR = 'frames_3d'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Simulation Logic (Entropic) ---
G = 1.0
M_CORE = 1.0e4
N_STARS = 1000
R_MIN = 10.0
R_MAX = 500.0
A0 = 1.0e-3
DT = 0.5
STEPS = 300 

class GalacticSimulation:
    def __init__(self, mode='Entropic'):
        self.mode = mode
        self.stars_pos = self._init_positions()
        self.stars_vel = self._init_velocities()

    def _init_positions(self):
        theta = np.random.uniform(0, 2*np.pi, N_STARS)
        u = np.random.uniform(R_MIN**2, R_MAX**2, N_STARS)
        r = np.sqrt(u)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = np.random.normal(0, 5, N_STARS) # Add slight thickness to disk for 3D effect
        return np.column_stack((x, y, z))

    def _init_velocities(self):
        # 2D projection for velocity calc
        r = np.linalg.norm(self.stars_pos[:, :2], axis=1) 
        
        a_newton = G * M_CORE / (r**2)
        a_entropic = 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        v_mag = np.sqrt(a_entropic * r)
        
        vx = -self.stars_pos[:, 1] / r * v_mag
        vy =  self.stars_pos[:, 0] / r * v_mag
        vz = np.zeros(N_STARS) # No vertical velocity, just thickness
        return np.column_stack((vx, vy, vz))

    def get_forces(self, positions):
        # Force is purely radial in XY plane
        r_xy = np.linalg.norm(positions[:, :2], axis=1)
        r_xy = np.maximum(r_xy, 1e-5)
        
        a_n = G * M_CORE / (r_xy**2)
        a_mag = 0.5 * (a_n + np.sqrt(a_n**2 + 4 * a_n * A0))
        
        acc_x = (-positions[:, 0] / r_xy) * a_mag
        acc_y = (-positions[:, 1] / r_xy) * a_mag
        acc_z = np.zeros(len(positions)) # No vertical force
        
        return np.column_stack((acc_x, acc_y, acc_z))

    def step(self):
        dt = DT
        acc = self.get_forces(self.stars_pos)
        self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
        new_acc = self.get_forces(self.stars_pos)
        self.stars_vel += 0.5 * (acc + new_acc) * dt
        return self.stars_pos

# --- Rendering Logic ---

def render_3d():
    sim = GalacticSimulation(mode='Entropic')
    
    print(f"🚀 Iniciando 3D Cinematic Render ({STEPS} frames)...")
    
    fig = plt.figure(figsize=(16, 9), dpi=80)
    ax = fig.add_subplot(111, projection='3d')
    
    limits = 600
    
    for i in range(STEPS):
        pos = sim.step()
        
        ax.clear()
        
        # Plot Stars
        # Depth shading is tricky in matplotlib, but we can fake it with alpha or color maps based on Z
        # staying simple: white stars
        ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2], s=1.5, c='white', alpha=0.8)
        
        # Plot Core
        ax.scatter([0], [0], [0], s=100, c='yellow', alpha=1.0)
        
        # Camera Animation
        # Elev: Start at 90 (top down), go down to 30 (oblique)
        # Azim: Rotate around continuously
        
        # Smooth transition from top-down to angled
        if i < 100:
            elev = 90 - (i/100)*60 # 90 -> 30
        else:
            elev = 30
            
        azim = i * 0.5 # Rotate 0.5 deg per frame
        
        ax.view_init(elev=elev, azim=azim)
        
        # Aesthetics
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)
        ax.set_zlim(-limits/2, limits/2)
        
        # Hide pane/grid for "Space" look
        ax.set_axis_off()
        # Matplotlib 3D background is usually gray, let's try to fix it
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        filename = f"{OUTPUT_DIR}/frame_{i:04d}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='black')
        
        if i % 20 == 0:
            print(f"Renderizando frame {i}/{STEPS}...")

    plt.close()
    print(f"✅ 3D frames gerados na pasta {OUTPUT_DIR}")

if __name__ == "__main__":
    render_3d()
