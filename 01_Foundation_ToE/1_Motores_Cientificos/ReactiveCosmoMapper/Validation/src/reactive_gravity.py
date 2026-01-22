import numpy as np
from astropy import constants as const
from astropy import units as u

class ReactiveGravity:
    """
    Implements the physics of Entropic/Emergent Gravity.
    Core Logic: Interpolation between Newtonian and MONDian regimes.
    """
    
    def __init__(self, a0=1.2e-10):
        """
        Initialize with the fundamental acceleration scale a0.
        Default a0 approx 1.2e-10 m/s^2 (Standard MOND value).
        """
        self.G = const.G.value # 6.674e-11
        self.a0 = a0
        self.M_sun = 1.989e30 # Solar mass in kg

    def calculate_newtonian_acceleration(self, mass_kg, radius_m):
        """
        Standard Newtonian Gravity: g_N = G * M / r^2
        """
        radius_m = np.maximum(radius_m, 1.0) # Avoid division by zero
        return (self.G * mass_kg) / (radius_m**2)

    def calculate_effective_acceleration(self, mass_kg, radius_m):
        """
        Entropic Gravity Formula (Verlinde/MOND interpolation):
        g_obs = (g_N + sqrt(g_N^2 + 4 * g_N * a0)) / 2
        
        Args:
            mass_kg: Mass in kilograms (baryonic only).
            radius_m: Distance in meters.
            
        Returns:
            Effective acceleration (m/s^2).
        """
        g_N = self.calculate_newtonian_acceleration(mass_kg, radius_m)
        
        # Eq 37 from documentation
        term_sqrt = np.sqrt(g_N**2 + 4 * g_N * self.a0)
        g_det = (g_N + term_sqrt) / 2.0
        
        return g_det

    def calculate_velocity(self, mass_kg, radius_m):
        """
        Calculates orbital velocity for a circular orbit: v = sqrt(g_obs * r)
        
        Returns:
            Velocity in km/s (for easy comparison with SPARC).
        """
        g_eff = self.calculate_effective_acceleration(mass_kg, radius_m)
        v_ms = np.sqrt(g_eff * radius_m)
        return v_ms / 1000.0 # Convert to km/s
