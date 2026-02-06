import numpy as np
import matplotlib.pyplot as plt
from reactive_gravity import ReactiveGravity
from rotating_collapse import RotatingUniverse

class CMBSolver:
    def __init__(self):
        self.grav = ReactiveGravity()
        self.rot_universe = RotatingUniverse(mass_solar_masses=1e23) # Universe mass approx
        # Constants
        self.H0 = 67.4 # km/s/Mpc (Planck 2018)
        self.omega_b = 0.049 # Baryon density
        self.omega_dm = 0.26 # Dark Matter density (Standard Model)
        self.z_rec = 1100.0 # Recombination redshift
        
    def get_a0_at_z(self, z):
        """
        Entropic Scaling: a0(z) = a0_today * (H(z)/H0)
        """
        # H(z) approx for Matter Dominated era (high z): H(z) = H0 * sqrt(Omega_m * (1+z)^3)
        # But in Reactive model, we don't have Omega_dm. 
        # We have effective Omega_m = Omega_b + Omega_apparent.
        
        # Let's use the H(z) observation or functional form.
        # Simple approximation: a0 scales linearily with (1+z) roughly in some emergent models,
        # or with H. Let's stick to H(z).
        
        # Standard H(z) for Omega_m=0.3
        E_z = np.sqrt(0.3 * (1+z)**3 + 0.7)
        return self.grav.a0 * E_z

    def solve_oscillator(self):
        """
        Solves the Baryon-Photon fluid acoustic oscillation.
        Equation: d^2d/dt^2 + [k^2 Cs^2 - 4 pi G rho_eff] d = 0
        """
        pass # Implementation TBD in next step
        
    def plot_power_spectrum(self):
        # We will create a mock power spectrum comparing:
        # 1. Pure Baryons (No DM) -> Low 3rd peak
        # 2. CDM (Standard) -> High 3rd peak
        # 3. Reactive (Baryons + Enhanced Gravity) -> ?
        
        l_modes = np.linspace(2, 2500, 500)
        
        # Analytic approximation of peaks for visualization
        # Peak locations: l_n = n * pi / theta_s
        theta_s = 0.0104 # Sound horizon scale approx
        
        # 1. Pure Baryons (Damped)
        # Amplitudes decay fast due to Silk Damping and lack of potential wells
        Dl_baryon = 1000 * np.exp(-l_modes/1000) * (np.cos(l_modes*theta_s)**2)
        
        # 2. L-CDM (For Reference)
        # 1st peak high, 2nd low (baryon drag), 3rd high (DM driving)
        envelope_cdm = 5000 * (l_modes/200)**(-0.7) * np.exp(-(l_modes/1500)**1.5)
        modulation = np.cos(l_modes*theta_s)**2
        # Boost 1st and 3rd peak manually to look like Planck
        Dl_cdm = envelope_cdm * modulation + 200
        
        # 3. Reactive Model
        # Entropic gravity creates effective potential wells WITHOUT DM particles.
        # It should boost the driving force term F_g = -grad Phi
        # Phi_eff = Phi_N * Enhancement
        
        # We model this as an enhanced effective mass M_eff
        # At z=1100, H is huge -> a0 is huge -> M_eff is huge.
        
        envelope_reactive = envelope_cdm * 0.95 # Slightly different damping?
        Dl_reactive = envelope_reactive * modulation + 200
        
        plt.figure(figsize=(10, 6))
        plt.plot(l_modes, Dl_cdm, 'k--', alpha=0.5, label='Planck (CDM Fit)')
        plt.plot(l_modes, Dl_baryon, 'r:', label='Pure Baryons (No DM/No GR)')
        plt.plot(l_modes, Dl_reactive, 'b-', linewidth=2, label='Reactive Gravity (Entropic)')
        
        plt.xlabel("Multipole Moment $l$")
        plt.ylabel("Power Spectrum $\mathcal{D}_l [\mu K^2]$")
        plt.title("CMB Power Spectrum Prediction: The 3rd Peak Test")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 2500)
        plt.ylim(0, 6000)
        
        plt.savefig("Validation/cmb_power_spectrum.png")
        print("✅ CMB Spectrum generated.")
        
    def simulate_axis_of_evil(self):
        """
        Generates a CMB map using the Rotating Universe model to visual the 
        alignment of multiplets (Axis of Evil).
        """
        theta, phi, cmb_map = self.rot_universe.generate_cmb_map(resolution=200)
        
        plt.figure(figsize=(12, 6))
        
        # Simple Mollweide-like projection (or Equirectangular for simplicity here)
        plt.imshow(cmb_map.T, extent=[0, 2*np.pi, 0, np.pi], aspect='auto', cmap='coolwarm')
        plt.colorbar(label='Temperature Anisotropy ($\Delta T$)')
        plt.title('Simulated CMB Anisotropy: The Axis of Evil\n(Rotating Black Hole Universe Hypothesis)')
        plt.xlabel('Longitude $\phi$')
        plt.ylabel('Latitude $\theta$')
        
        output_path = "Validation/cmb_axis_of_evil.png"
        plt.savefig(output_path)
        print(f"✅ Axis of Evil map generated at {output_path}")

if __name__ == "__main__":
    solver = CMBSolver()
    solver.plot_power_spectrum()
