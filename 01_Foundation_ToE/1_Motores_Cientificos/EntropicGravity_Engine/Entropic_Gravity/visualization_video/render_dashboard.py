import matplotlib
matplotlib.use('Agg') # Force non-interactive backend
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

# Configuração Estética "Sci-Fi"
plt.style.use('dark_background')

# Criar pasta para os frames se não existir
OUTPUT_DIR = 'frames_dashboard'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Simulation Logic (Same as before) ---

G = 1.0
M_CORE = 1.0e4
N_STARS = 400
R_MIN = 10.0
R_MAX = 500.0
A0 = 1.0e-3
DT = 0.5
STEPS = 150

class GalacticSimulation:
    def __init__(self, mode='Entropic'):
        self.mode = mode
        self.stars_pos = self._init_positions()
        self.stars_vel = self._init_velocities()
        # History now stores (pos, vel) tuple
        self.history = [] 

    def _init_positions(self):
        theta = np.random.uniform(0, 2*np.pi, N_STARS)
        u = np.random.uniform(R_MIN**2, R_MAX**2, N_STARS)
        r = np.sqrt(u)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack((x, y))

    def _init_velocities(self):
        r = np.linalg.norm(self.stars_pos, axis=1)
        a = self._calc_acceleration_magnitude(r)
        v_mag = np.sqrt(a * r)
        vx = -self.stars_pos[:, 1] / r * v_mag
        vy =  self.stars_pos[:, 0] / r * v_mag
        return np.column_stack((vx, vy))

    def _calc_acceleration_magnitude(self, r):
        a_newton = G * M_CORE / (r**2)
        if self.mode == 'Newton':
            return a_newton
        elif self.mode == 'Entropic':
            return 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        else:
            raise ValueError()

    def get_forces(self, positions):
        r_vec = -positions
        r_mag = np.linalg.norm(positions, axis=1)
        r_mag = np.maximum(r_mag, 1e-5)
        a_mag = self._calc_acceleration_magnitude(r_mag)
        acc_x = (r_vec[:, 0] / r_mag) * a_mag
        acc_y = (r_vec[:, 1] / r_mag) * a_mag
        return np.column_stack((acc_x, acc_y))

    def run(self):
        dt = DT
        acc = self.get_forces(self.stars_pos)
        
        print(f"[INFO] Running Simulation ({self.mode})...")
        for step in range(STEPS):
            self.history.append((self.stars_pos.copy(), self.stars_vel.copy()))
            
            self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
            new_acc = self.get_forces(self.stars_pos)
            self.stars_vel += 0.5 * (acc + new_acc) * dt
            acc = new_acc

        return self.history # List of tuples

# --- Dashboard Rendering Logic ---

def render_dashboard(history, limits=600):
    """
    history: List of (positions, velocities)
    """
    # Setup Figure with GridSpec (1 row, 2 cols, different widths)
    # Reduced DPI for speed (100 -> 60)
    fig = plt.figure(figsize=(12, 6), dpi=60)
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.2]) 
    
    # Ax1: Simulation (Left)
    ax_sim = plt.subplot(gs[0])
    
    # Ax2: Plots (Right)
    ax_plot = plt.subplot(gs[1])

    # Pre-calculate analytical curves for reference on the plot
    r_grid = np.linspace(R_MIN, limits, 200)
    
    # Newton Analytical
    a_n = G * M_CORE / r_grid**2
    v_n = np.sqrt(a_n * r_grid)
    
    # Entropic Analytical
    a_e = 0.5 * (a_n + np.sqrt(a_n**2 + 4 * a_n * A0))
    v_e = np.sqrt(a_e * r_grid)

    total_frames = len(history)
    print(f"🚀 Iniciando Dashboard Render ({total_frames} frames)...")

    for i, (pos_step, vel_step) in enumerate(history):
        # --- LEFT PANEL: GALAXY ---
        ax_sim.clear()
        
        # Trail (Removed for speed) - Keeping simple stars
        # Particles
        ax_sim.scatter(pos_step[:, 0], pos_step[:, 1], s=2, c='white', alpha=0.9)
        # Core
        ax_sim.scatter([0], [0], s=60, c='yellow', alpha=0.8)
        
        ax_sim.set_xlim(-limits, limits)
        ax_sim.set_ylim(-limits, limits)
        ax_sim.set_aspect('equal')
        ax_sim.set_title("Visual Simulation", fontsize=14, color='cyan')
        ax_sim.axis('off')

        # --- RIGHT PANEL: ROTATION CURVE ---
        ax_plot.clear()
        
        # Calculate R and V for current particles
        r = np.linalg.norm(pos_step, axis=1)
        v = np.linalg.norm(vel_step, axis=1)

        # Plot Analytical Reference Lines
        ax_plot.plot(r_grid, v_n, color='gray', linestyle='--', alpha=0.5, label='Newtonian Prediction')
        ax_plot.plot(r_grid, v_e, color='cyan', linestyle='-', linewidth=2, alpha=0.8, label='Entropic Prediction')
        
        # Plot Live Data
        # We plot scatter of current status
        ax_plot.scatter(r, v, s=3, c='white', alpha=0.6)
        
        ax_plot.set_xlim(0, limits)
        ax_plot.set_ylim(0, np.max(v_e)*1.5)
        ax_plot.set_xlabel("radius [kpc]", fontsize=10)
        ax_plot.set_ylabel("velocity [km/s]", fontsize=10)
        ax_plot.set_title("Real-Time Rotation Curve", fontsize=12, color='yellow')
        # Legend removed for speed/clutter or simplified
        # ax_plot.legend(loc='upper right', frameon=False)
        ax_plot.grid(True, alpha=0.2)

        # --- SAVE ---
        filename = f"{OUTPUT_DIR}/frame_{i:04d}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, facecolor='black')
        
        if i % 20 == 0:
            print(f"Renderizando frame {i}/{total_frames}...")

    plt.close()
    print(f"✅ Dashboard frames gerados na pasta {OUTPUT_DIR}")

if __name__ == "__main__":
    # 1. Run Physics
    sim = GalacticSimulation(mode='Entropic')
    hist = sim.run()
    
    # 2. Render Dashboard
    render_dashboard(hist)
