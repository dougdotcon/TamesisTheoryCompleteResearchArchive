import numpy as np
import matplotlib.pyplot as plt
import os

# Configuração Estética "Sci-Fi"
plt.style.use('dark_background')

# Criar pasta para os frames se não existir
OUTPUT_DIR = 'frames'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Simulation Logic (Adapted from src/simulacao_galaxia.py) ---

G = 1.0
M_CORE = 1.0e4
N_STARS = 1000  # Increased for better visual
R_MIN = 10.0
R_MAX = 500.0
A0 = 1.0e-3
DT = 0.5        # Adjusted for smoother animation vs long waits
STEPS = 600     # Sufficient for a 20s video at 30fps

class GalacticSimulation:
    def __init__(self, mode='Entropic'):
        self.mode = mode
        self.stars_pos = self._init_positions()
        self.stars_vel = self._init_velocities()
        self.position_history = [] 

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
            # Entropic / MOND interpolation
            return 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

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
            self.position_history.append(self.stars_pos.copy())
            
            # Verlet Integration
            self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
            new_acc = self.get_forces(self.stars_pos)
            self.stars_vel += 0.5 * (acc + new_acc) * dt
            acc = new_acc

        return np.array(self.position_history)

# --- Rendering Logic ---

def render_simulation(positions, limits=600):
    """
    positions: Array (N_steps, N_particles, 2)
    limits: Visual limits
    """
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    total_frames = len(positions)
    print(f"🚀 Iniciando renderização de {total_frames} frames...")

    for i, pos_step in enumerate(positions):
        ax.clear()
        
        # Trail Effect (Motion Blur)
        if i > 0:
            prev_pos = positions[i-1]
            ax.scatter(prev_pos[:, 0], prev_pos[:, 1], 
                       s=0.5, c='cyan', alpha=0.3, edgecolors='none')

        # Main Particles
        ax.scatter(pos_step[:, 0], pos_step[:, 1], 
                   s=1.2, c='white', alpha=0.8, edgecolors='none') # White core stars look better on dark

        # Core
        ax.scatter([0], [0], s=50, c='yellow', alpha=0.5, edgecolors='none') # Central bulge

        # Aesthetics
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)
        ax.set_aspect('equal')
        
        # Title/Text
        # ax.set_title(f"Entropic Gravity Simulation - T = {i}", color='white', fontsize=16)
        ax.text(-limits*0.9, limits*0.85, "Simulation: Entropic Gravity (Verlinde)", color='cyan', fontsize=20, weight='bold')
        ax.text(-limits*0.9, limits*0.80, "No Dark Matter Required", color='yellow', fontsize=16)
        
        # Clean look
        ax.axis('off') # Turn off axis completely for cinematic look

        filename = f"{OUTPUT_DIR}/frame_{i:04d}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='black')
        
        if i % 20 == 0:
            print(f"Renderizando frame {i}/{total_frames}...")

    plt.close()
    print(f"✅ Todos os frames gerados na pasta {OUTPUT_DIR}")

if __name__ == "__main__":
    # 1. Run Physics
    sim = GalacticSimulation(mode='Entropic')
    history = sim.run()
    
    # 2. Render Video Frames
    render_simulation(history)
