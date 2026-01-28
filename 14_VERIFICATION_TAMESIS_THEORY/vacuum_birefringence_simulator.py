import numpy as np
import matplotlib.pyplot as plt

# Constants
E_PLANCK_GEV = 1.22e19
DEG_TO_RAD = np.pi / 180.0

class BirefringenceSimulator:
    def __init__(self, energy_gev, distance_gpc):
        self.energy = energy_gev
        self.distance = distance_gpc
        # Distance Gpc to meters 
        self.D_meters = distance_gpc * 3.086e25
        
    def calculate_rotation(self, eta, order=1):
        """
        Calculates the rotation of the polarization angle.
        phi = eta * (E/E_pl)^order * (D / lambda_pl)
        Simplified for simulation: delta_theta (rad)
        """
        # Relative energy scale
        epsilon = self.energy / E_PLANCK_GEV
        
        # In Tamesis, the asymmetry factor eta represents 
        # the anisotropy of the graph connectivity.
        # D/lambda_pl is roughly D * E_pl / (hbar * c)
        # We'll use a standard phenomenology formula for Lorentz Violation
        rotation_rad = eta * (epsilon**order) * (self.D_meters * self.energy / (1.97e-16)) # conversion factor
        return np.rad2deg(rotation_rad) % 360

    def simulate_stokes(self, initial_angle_deg, eta_values, order=1):
        """
        Simulates the drift of the polarization angle over eta range.
        """
        results = []
        for eta in eta_values:
            drift = self.calculate_rotation(eta, order)
            final_angle = (initial_angle_deg + drift) % 180 # Polarization is 180-periodic
            results.append(final_angle)
        return np.array(results)

    def run_experiment(self):
        print(f"[Tamesis] Starting Birefringence Simulation...")
        print(f"[Setup] Energy: {self.energy} GeV | Distance: {self.distance} Gpc")
        
        # Parameter Space for eta (anisotropy)
        # Usually eta is expected to be very small if space is isotropic
        eta_space = np.logspace(-25, -15, 100)
        
        # 1. Linear Rotation (Standard LV)
        angles_linear = self.simulate_stokes(45, eta_space, order=1)
        
        # 2. Quadratic Rotation (Suppressed)
        angles_quad = self.simulate_stokes(45, eta_space, order=2)
        
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.title("Tamesis Vacuum Birefringence: Polarization Rotation")
        plt.plot(eta_space, angles_linear, label='Linear Model (Standard)', color='orange')
        plt.plot(eta_space, angles_quad, label='Quadratic Model (Tamesis v3)', color='green')
        plt.xscale('log')
        plt.axhline(45, color='blue', linestyle='--', label='Initial Polarization (45°)')
        plt.ylabel("Observed Angle (°)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 1, 2)
        plt.title("Detection Sensitivity (IXPE Threshold)")
        # IXPE sensitivity is around 1-2% in polarization degree, 
        # and few degrees in angle for bright sources.
        plt.fill_between(eta_space, 43, 47, color='gray', alpha=0.2, label='Instrument Noise Floor')
        plt.plot(eta_space, angles_linear, color='orange')
        plt.xscale('log')
        plt.xlabel("Graph Anisotropy Factor (eta)")
        plt.ylabel("Angle (°)")
        plt.ylim(0, 90)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('d:/TamesisTheoryCompleteResearchArchive/14_VERIFICATION_TAMESIS_THEORY/birefringence_analysis.png')
        print("[Output] Birefringence plot saved.")

if __name__ == "__main__":
    # Test for a high-energy X-ray source (e.g. Magnetar in a distant galaxy)
    # Energy: 10 keV (0.00001 GeV), Distance: 100 Mpc (0.1 Gpc)
    sim = BirefringenceSimulator(energy_gev=1e-5, distance_gpc=0.1)
    sim.run_experiment()
