import matplotlib
matplotlib.use('Agg') # Force non-interactive backend for speed
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuração Estética "Sci-Fi"
plt.style.use('dark_background')

# Criar pasta para os frames se não existir
OUTPUT_DIR = 'frames_clash'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Simulation Logic ---

G = 1.0
M_CORE = 1.0e4
N_STARS = 400   # Stars per galaxy
R_MIN = 10.0
R_MAX = 500.0
A0 = 1.0e-3
DT = 0.5
STEPS = 400     # Duration of the clash

class GalacticSimulation:
    def __init__(self, mode='Newton'):
        self.mode = mode
        self.stars_pos = self._init_positions()
        if mode == 'Newton_Fail':
             # We want to start with Entropic velocities to show the crash, so we defer initialization or call specific one
             self.stars_vel = None # Will assign below
        else:
             self.stars_vel = None

        if self.mode == 'Newton_Fail':
            # Initialize with Entropic (Fast) velocities to show it flying apart under Newton gravity
            self.stars_vel = self._init_velocities_entropic()
            self.true_mode_physics = 'Newton' 
        else:
            self.stars_vel = self._init_velocities_entropic() # Both start fast
            self.true_mode_physics = 'Entropic'

    def _init_positions(self):
        theta = np.random.uniform(0, 2*np.pi, N_STARS)
        u = np.random.uniform(R_MIN**2, R_MAX**2, N_STARS)
        r = np.sqrt(u)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack((x, y))

    def _init_velocities_entropic(self):
        """Calculate velocities required for a FLAT rotation curve (Entropic/Observed)."""
        r = np.linalg.norm(self.stars_pos, axis=1)
        
        # Calculate Entropic Acceleration (which matches observation)
        a_newton = G * M_CORE / (r**2)
        a_entropic = 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        
        v_mag = np.sqrt(a_entropic * r) # Fast velocities
        
        vx = -self.stars_pos[:, 1] / r * v_mag
        vy =  self.stars_pos[:, 0] / r * v_mag
        return np.column_stack((vx, vy))

    def _calc_acceleration_magnitude(self, r):
        a_newton = G * M_CORE / (r**2)
        
        if self.true_mode_physics == 'Newton':
            return a_newton
        elif self.true_mode_physics == 'Entropic':
            return 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        else:
            raise ValueError()

    def get_forces(self, positions):
        r_mag = np.linalg.norm(positions, axis=1)
        r_mag = np.maximum(r_mag, 1e-5)
        a_mag = self._calc_acceleration_magnitude(r_mag)
        
        # Vector pointing to center is -positions
        acc_x = (-positions[:, 0] / r_mag) * a_mag
        acc_y = (-positions[:, 1] / r_mag) * a_mag
        return np.column_stack((acc_x, acc_y))

    def step(self):
        dt = DT
        acc = self.get_forces(self.stars_pos)
        
        # Verlet
        self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
        new_acc = self.get_forces(self.stars_pos)
        self.stars_vel += 0.5 * (acc + new_acc) * dt
        
        return self.stars_pos

# --- Rendering Logic ---

def render_clash():
    # Initialize Simulations
    # 1. Newton Simulation initialized with Observation Velocities (Fast) -> Should fly apart
    sim_newton = GalacticSimulation(mode='Newton_Fail')
    
    # 2. Entropic Simulation initialized with Observation Velocities (Fast) -> Should hold together
    sim_entropic = GalacticSimulation(mode='Entropic')

    print(f"🚀 Iniciando Clash Render ({STEPS} frames)...")
    
    fig, axes = plt.subplots(1, 2, figsize=(19.2, 10.8), dpi=80) 
    
    # Static Setup
    limits = 800 # Zoom out a bit to see Newton expansion
    
    for i in range(STEPS):
        # Evolve physics
        pos_n = sim_newton.step()
        pos_e = sim_entropic.step()
        
        # Draw
        for ax in axes:
            ax.clear()
            ax.set_xlim(-limits, limits)
            ax.set_ylim(-limits, limits)
            ax.set_aspect('equal')
            ax.axis('off')

        # --- LEFT: NEWTONIAN (FAIL) ---
        axes[0].scatter(pos_n[:, 0], pos_n[:, 1], s=2, c='red', alpha=0.7)
        axes[0].scatter([0], [0], s=80, c='white', alpha=0.5)
        axes[0].text(0, limits*0.9, "STANDARD MODEL (No Dark Matter)", 
                     color='red', fontsize=16, ha='center', weight='bold')
        axes[0].text(0, limits*0.8, "Galaxy flies apart ('Mass Deficit')", 
                     color='white', fontsize=12, ha='center')

        # --- RIGHT: ENTROPIC (SUCCESS) ---
        axes[1].scatter(pos_e[:, 0], pos_e[:, 1], s=2, c='cyan', alpha=0.9)
        axes[1].scatter([0], [0], s=80, c='yellow', alpha=0.8)
        axes[1].text(0, limits*0.9, "ENTROPIC GRAVITY", 
                     color='cyan', fontsize=16, ha='center', weight='bold')
        axes[1].text(0, limits*0.8, "Galaxy remains stable naturally", 
                     color='white', fontsize=12, ha='center')
        
        # Middle Line
        # line = plt.Line2D([0.5, 0.5], [0.1, 0.9], transform=fig.transFigure, color="white", alpha=0.5)
        # fig.add_artist(line)

        # Save
        filename = f"{OUTPUT_DIR}/frame_{i:04d}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='black')
        
        if i % 20 == 0:
            print(f"Renderizando frame {i}/{STEPS}...")

    plt.close()
    print(f"✅ Dashboard frames gerados na pasta {OUTPUT_DIR}")

if __name__ == "__main__":
    render_clash()
