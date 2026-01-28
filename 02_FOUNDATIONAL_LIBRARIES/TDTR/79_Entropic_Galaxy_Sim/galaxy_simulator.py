import numpy as np
import matplotlib.pyplot as plt

class GalaxySimulator:
    def __init__(self, galaxy_mass_solar_masses, scale_length_kpc, a0_ms2=1.2e-10):
        """
        Initialize the Entropic Galaxy Simulator.
        
        Args:
            galaxy_mass_solar_masses (float): Total mass of the galaxy (visible baryonic) in Solar Masses.
            scale_length_kpc (float): Characteristic scale length of the galaxy disk in kpc.
            a0_ms2 (float): The critical acceleration parameter a_0 (~1.2e-10 m/s^2).
        """
        self.M_total = galaxy_mass_solar_masses
        self.Rd = scale_length_kpc
        self.a0 = a0_ms2
        
        # Constants
        self.G = 4.301e-6  # kpc (km/s)^2 / M_sun (Gravitational constant in galactic units)
        self.G_SI = 6.674e-11 # m^3 kg^-1 s^-2
        self.M_sun_kg = 1.989e30 # kg
        self.kpc_to_m = 3.086e19 # m
        
        # Convert G to compatible units for internal calculation if needed, 
        # but let's stick to galactic units for output velocities (km/s).
        # We need a0 in galactic units for consistency?
        # a0 is usually given in m/s^2. Let's convert a0 to (km/s)^2 / kpc?
        # 1 m/s^2 = (1e-3 km/s)^2 / (1/3.086e19 kpc) ... this is getting messy.
        # Let's compute accelerations in m/s^2 and then convert velocity to km/s.
        
    def radius_grid(self, max_r_kpc=30, points=100):
        """Generate radial points."""
        return np.linspace(0.1, max_r_kpc, points) # Avoid r=0
        
    def enclosed_mass_exponential_disk(self, r_kpc):
        """
        Calculate enclosed mass M(r) for an exponential disk profile.
        Sigma(r) = Sigma_0 * exp(-r/Rd)
        M(r) = M_total * [1 - exp(-r/Rd) * (1 + r/Rd)]
        """
        x = r_kpc / self.Rd
        return self.M_total * (1 - np.exp(-x) * (1 + x))

    def newtonian_acceleration(self, r_kpc):
        """
        Calculate standard Newtonian acceleration a_N = GM(r)/r^2.
        Returns acceleration in m/s^2.
        """
        M_enc = self.enclosed_mass_exponential_disk(r_kpc)
        
        # Convert to SI for acceleration calculation
        M_kg = M_enc * self.M_sun_kg
        r_m = r_kpc * self.kpc_to_m
        
        a_n_si = self.G_SI * M_kg / (r_m**2)
        return a_n_si
        
    def newtonian_velocity(self, r_kpc):
        """
        Calculate the Keplerian velocity v = sqrt(r * a_N).
        Returns velocity in km/s.
        """
        a_n_si = self.newtonian_acceleration(r_kpc)
        r_m = r_kpc * self.kpc_to_m
        v_si = np.sqrt(r_m * a_n_si)
        return v_si / 1000.0 # Convert m/s_to km/s

    def run_baseline_simulation(self):
        """Run the Newtonian baseline simulation."""
        print(f"Running Newtonian Baseline for Galaxy Mass={self.M_total:.1e} M_sun, Rd={self.Rd} kpc")
        r = self.radius_grid()
        v_newton = [self.newtonian_velocity(ri) for ri in r]
        
        return r, v_newton

if __name__ == "__main__":
    # Test with a Milky-Way-like galaxy
    # Mass ~ 6e10 M_sun (baryonic only), Scale length ~ 3 kpc
    sim = GalaxySimulator(galaxy_mass_solar_masses=6e10, scale_length_kpc=3.0)
    r, v_newton = sim.run_baseline_simulation()
    
    # Simple ASCII plot for verification
    print("\nNewtonian Rotation Curve (Baseline):")
    print("r (kpc) | v (km/s)")
    print("--------|---------")
    for i in range(0, len(r), 10):
        print(f"{r[i]:6.1f}  | {v_newton[i]:6.1f}")
