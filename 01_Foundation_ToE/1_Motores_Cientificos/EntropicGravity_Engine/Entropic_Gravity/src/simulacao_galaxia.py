"""
Entropic Gravity Galaxy Simulation
----------------------------------
Author: Antigravity (AI Theoretical Physicist)
Date: 2025-12-27

Objective:
Simulate the rotation curve of a galaxy under two paradigms:
1. Classical Newtonian Gravity (Standard Model)
2. Entropic Gravity (Verlinde/MOND limit)

Methodology:
- N-Body Simulation with test particles orbiting a central massive core.
- Symplectic Velocity Verlet Integrator for energy stability.
- Vectorized NumPy implementation for performance.

Units:
Arbitrary simulation units used to ensure numerical stability.
G = 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configuration & Constants ---
G = 1.0
M_CORE = 1.0e4      # Mass of the galactic core
N_STARS = 500       # Number of stars
R_MIN = 10.0        # Inner radius of disk
R_MAX = 500.0       # Outer radius of disk
A0 = 1.0e-3         # Critical acceleration parameter (Verlinde/MOND)
DT = 0.1            # Time step
STEPS = 2000        # Simulation steps
OUTPUT_DIR = r"C:\Users\Douglas\Desktop\Entropy\Gravidade_Entropica\results"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

class GalacticSimulation:
    def __init__(self, mode='Newton'):
        """
        Initialize the galaxy simulation.
        
        Args:
            mode (str): 'Newton' for classical gravity, 'Entropic' for Verlinde/MOND.
        """
        self.mode = mode
        self.stars_pos = self._init_positions()
        self.stars_vel = self._init_velocities()
        self.history_v = []
        self.history_r = []
        
        print(f"[INFO] Initialized Simulation. Mode: {self.mode}")

    def _init_positions(self):
        """Initialize stars in a disk distribution."""
        # Random angles
        theta = np.random.uniform(0, 2*np.pi, N_STARS)
        # Random radii (uniform areal distribution)
        # r = sqrt(u) to distribute uniformly on disk area
        u = np.random.uniform(R_MIN**2, R_MAX**2, N_STARS)
        r = np.sqrt(u)
        
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        # z is 0 for 2D disk
        return np.column_stack((x, y))

    def _init_velocities(self):
        """Initialize velocities for circular orbits (approximate)."""
        # Calculate distance to center
        r = np.linalg.norm(self.stars_pos, axis=1)
        
        # Calculate Circular Velocity v_circ = sqrt(a * r)
        # We need the acceleration at this radius to match circular orbit condition.
        # F = m*a = m*v^2/r => v = sqrt(a*r)
        
        # Calculate expected acceleration for this r
        a = self._calc_acceleration_magnitude(r)
        
        v_mag = np.sqrt(a * r)
        
        # Velocity is perpendicular to position vector
        # If pos is (x, y), perp is (-y, x)
        vx = -self.stars_pos[:, 1] / r * v_mag
        vy =  self.stars_pos[:, 0] / r * v_mag
        
        return np.column_stack((vx, vy))

    def _calc_acceleration_magnitude(self, r):
        """
        Calculate acceleration magnitude based on the selected physics model.
        r: array of distances from center
        """
        # Newtonian Acceleration: a_N = GM / r^2
        a_newton = G * M_CORE / (r**2)
        
        if self.mode == 'Newton':
            return a_newton
        elif self.mode == 'Entropic':
            # Entropic Correction (Simple Interpolation Function)
            # a = (a_N + sqrt(a_N^2 + 4 a_N a_0)) / 2
            # This derives from the interpolation function mu(x) = x / (1+x)
            return 0.5 * (a_newton + np.sqrt(a_newton**2 + 4 * a_newton * A0))
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def get_forces(self, positions):
        """
        Calculate acceleration vectors for all stars towards the center.
        Assuming central potential dominates (ignoring star-star gravity for now).
        """
        r_vec = -positions # Vector pointing to center (0,0)
        r_mag = np.linalg.norm(positions, axis=1)
        
        # Avoid division by zero
        r_mag = np.maximum(r_mag, 1e-5)
        
        a_mag = self._calc_acceleration_magnitude(r_mag)
        
        # Normalize direction and scale by acceleration magnitude
        # a_vec = (r_vec / r_mag) * a_mag
        # But r_vec has length r_mag, so r_vec/r_mag is unit vector
        # We need to be careful with dimensions for broadcasting
        
        acc_x = (r_vec[:, 0] / r_mag) * a_mag
        acc_y = (r_vec[:, 1] / r_mag) * a_mag
        
        return np.column_stack((acc_x, acc_y))

    def run(self):
        """Run the simulation using Velocity Verlet integration."""
        dt = DT
        
        # Initial Forces
        acc = self.get_forces(self.stars_pos)
        
        print(f"[INFO] Starting integration for {STEPS} steps...")
        
        for step in range(STEPS):
            # 1. Update positions
            self.stars_pos += self.stars_vel * dt + 0.5 * acc * dt**2
            
            # 2. Update forces (acceleration) at new positions
            new_acc = self.get_forces(self.stars_pos)
            
            # 3. Update velocities
            self.stars_vel += 0.5 * (acc + new_acc) * dt
            
            # Update acc for next step
            acc = new_acc
            
            # Store data for final snapshot
            if step == STEPS - 1:
                r_final = np.linalg.norm(self.stars_pos, axis=1)
                v_final = np.linalg.norm(self.stars_vel, axis=1)
                self.history_r = r_final
                self.history_v = v_final

        print("[INFO] Simulation Complete.")

def plot_results(sim_newton, sim_entropic):
    """Generate comparative plots."""
    plt.figure(figsize=(12, 6))
    
    # Analytical predictions for reference
    r_grid = np.linspace(R_MIN, R_MAX, 100)
    
    # Newton Analytical
    a_n = G * M_CORE / r_grid**2
    v_n = np.sqrt(a_n * r_grid)
    
    # Entropic Analytical
    a_e = 0.5 * (a_n + np.sqrt(a_n**2 + 4 * a_n * A0))
    v_e = np.sqrt(a_e * r_grid)

    plt.plot(r_grid, v_n, 'k--', label='Newtonian Prediction ($v \propto r^{-1/2}$)', alpha=0.7)
    plt.plot(r_grid, v_e, 'r--', label='Entropic Prediction (Flat)', alpha=0.7)

    # Simulation Data
    plt.scatter(sim_newton.history_r, sim_newton.history_v, 
                s=10, c='gray', label='Sim Data: Newtonian', alpha=0.5)
    plt.scatter(sim_entropic.history_r, sim_entropic.history_v, 
                s=10, c='red', label='Sim Data: Entropic', alpha=0.5)

    plt.xlabel('Distance from Galactic Center ($r$)')
    plt.ylabel('Orbital Velocity ($v$)')
    plt.title(f'Galactic Rotation Curves: Newton vs Entropic Gravity ($a_0={A0}$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_path = os.path.join(OUTPUT_DIR, 'rotation_curve_comparison.png')
    plt.savefig(output_path)
    print(f"[RESULT] Plot saved to: {output_path}")

if __name__ == "__main__":
    print("=== Entropic Gravity Simulation ===")
    
    # precision formatting
    np.set_printoptions(precision=3)
    
    # Run Newtonian Simulation
    sim_n = GalacticSimulation(mode='Newton')
    sim_n.run()
    
    # Run Entropic Simulation
    sim_e = GalacticSimulation(mode='Entropic')
    sim_e.run()
    
    # Plot Comparison
    plot_results(sim_n, sim_e)
