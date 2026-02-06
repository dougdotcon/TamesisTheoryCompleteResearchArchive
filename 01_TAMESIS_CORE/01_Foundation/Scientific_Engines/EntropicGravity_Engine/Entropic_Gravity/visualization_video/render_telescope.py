import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import os

# Configuração Estética "Radio Telescope"
plt.style.use('dark_background')

OUTPUT_DIR = 'frames_telescope'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Simulation Logic (Entropic) ---
G = 1.0
M_CORE = 1.0e4
N_STARS = 1500  # More stars needed for good density map
R_MIN = 20.0    # Slightly larger hole in middle
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
        # Higher density in center typically, but uniform disk is fine
        u = np.random.uniform(R_MIN**2, R_MAX**2, N_STARS)
        r = np.sqrt(u)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return np.column_stack((x, y))

    def _init_velocities(self):
        r = np.linalg.norm(self.stars_pos, axis=1)
        a_newton = G * M_CORE / (r**2)
        # Entropic Calculation
        a_entropic = 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        v_mag = np.sqrt(a_entropic * r)
        
        vx = -self.stars_pos[:, 1] / r * v_mag
        vy =  self.stars_pos[:, 0] / r * v_mag
        return np.column_stack((vx, vy))

    def get_forces(self, positions):
        r_mag = np.linalg.norm(positions, axis=1)
        r_mag = np.maximum(r_mag, 1e-5)
        # Entropic acceleration magnitude
        a_n = G * M_CORE / (r_mag**2)
        a_mag = 0.5 * (a_n + np.sqrt(a_n**2 + 4 * a_n * A0))
        
        acc_x = (-positions[:, 0] / r_mag) * a_mag
        acc_y = (-positions[:, 1] / r_mag) * a_mag
        return np.column_stack((acc_x, acc_y))

    def step(self):
        dt = DT
        acc = self.get_forces(self.stars_pos)
        self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
        new_acc = self.get_forces(self.stars_pos)
        self.stars_vel += 0.5 * (acc + new_acc) * dt
        return self.stars_pos

# --- Rendering Logic (Heatmap/Density) ---

def render_telescope():
    sim = GalacticSimulation(mode='Entropic')
    
    print(f"🚀 Iniciando Telescope Render ({STEPS} frames)...")
    
    # Square figure to mimic sensor data
    fig, ax = plt.subplots(figsize=(10, 10), dpi=80)
    
    limits = 600
    
    for i in range(STEPS):
        pos = sim.step()
        
        ax.clear()
        
        # HEXBIN PLOT (The Telescope View)
        # gridsize: resolution of the sensors
        # cmap: 'magma' or 'inferno' looks like radio intensity
        # mincnt: don't plot empty space
        hb = ax.hexbin(pos[:, 0], pos[:, 1], gridsize=60, cmap='magma', 
                       extent=[-limits, limits, -limits, limits], 
                       mincnt=1, vmin=0, vmax=5) # vmax clamps brightness
        
        # Add Central Core Forcefully (saturation)
        ax.scatter([0], [0], s=100, c='white', alpha=0.9)
        
        # Aesthetics: "HUD"
        ax.set_xlim(-limits, limits)
        ax.set_ylim(-limits, limits)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Fake Telemetry
        ax.text(-limits*0.9, limits*0.9, "SENSOR: ENTROPY_ARRAYS_V4", color='lime', fontfamily='monospace')
        ax.text(-limits*0.9, limits*0.85, f"WAVELENGTH: 21cm (HI)", color='lime', fontfamily='monospace')
        ax.text(limits*0.5, limits*0.9, f"T = {i*DT:.1f} Myr", color='lime', fontfamily='monospace')
        
        # Crosshair center
        ax.plot([-50, 50], [0, 0], color='lime', alpha=0.3, lw=1)
        ax.plot([0, 0], [-50, 50], color='lime', alpha=0.3, lw=1)

        filename = f"{OUTPUT_DIR}/frame_{i:04d}.png"
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, facecolor='black')
        
        if i % 20 == 0:
            print(f"Renderizando frame {i}/{STEPS}...")

    plt.close()
    print(f"✅ Dashboard frames gerados na pasta {OUTPUT_DIR}")

if __name__ == "__main__":
    render_telescope()
