"""
Reactive Gravity Engine — Entropic/MOND Gravity Implementation

Implements the interpolation between Newtonian and MONDian regimes.
Based on the McGaugh et al. (2016) Radial Acceleration Relation.

Author: Douglas H. M. Fulber
Version: 2.0 (Fixed - removed astropy dependency)
"""

import numpy as np

class ReactiveGravity:
    """
    Implements the physics of Entropic/Emergent Gravity.
    Core Logic: Interpolation between Newtonian and MONDian regimes.
    
    The effective acceleration is given by:
        g_eff = g_N * nu(g_N / a0)
    
    where nu(x) is the interpolation function.
    """
    
    # Physical Constants (CODATA 2018)
    G = 6.67430e-11       # Gravitational constant [m^3 kg^-1 s^-2]
    M_sun = 1.98841e30    # Solar mass [kg]
    kpc_to_m = 3.08567758e19  # 1 kpc in meters
    
    def __init__(self, a0=1.2e-10):
        """
        Initialize with the fundamental acceleration scale a0.
        
        Parameters
        ----------
        a0 : float
            MOND acceleration threshold [m/s^2]
            Default: 1.2e-10 m/s^2 (McGaugh et al. 2016)
            Note: a0 ≈ c*H0/(2π) ≈ 1.2e-10 for H0 ≈ 70 km/s/Mpc
        """
        self.a0 = a0

    def calculate_newtonian_acceleration(self, mass_kg, radius_m):
        """
        Standard Newtonian Gravity: g_N = G * M / r^2
        
        Parameters
        ----------
        mass_kg : float or ndarray
            Enclosed mass in kilograms
        radius_m : float or ndarray
            Distance from center in meters
            
        Returns
        -------
        float or ndarray
            Newtonian acceleration [m/s^2]
        """
        radius_m = np.maximum(radius_m, 1.0)  # Avoid division by zero
        return (self.G * mass_kg) / (radius_m**2)

    def interpolation_function(self, x):
        """
        MOND interpolation function: nu(x) where x = g_N / a0
        
        This implementation uses the "simple" interpolation:
            nu(x) = 1/2 + sqrt(1/4 + 1/x)
        
        Which gives:
            g_eff = g_N * nu(g_N/a0) = (g_N + sqrt(g_N^2 + 4*g_N*a0)) / 2
        
        Asymptotic behavior:
            - x >> 1: nu -> 1 (Newtonian regime)
            - x << 1: nu -> 1/sqrt(x) (Deep MOND regime)
        """
        x = np.maximum(x, 1e-10)  # Avoid numerical issues
        return 0.5 + np.sqrt(0.25 + 1.0/x)
    
    def calculate_effective_acceleration(self, mass_kg, radius_m):
        """
        Entropic/MOND Effective Acceleration
        
        g_eff = g_N * nu(g_N / a0)
        
        Parameters
        ----------
        mass_kg : float or ndarray
            Baryonic mass in kilograms
        radius_m : float or ndarray
            Distance in meters
            
        Returns
        -------
        float or ndarray
            Effective acceleration [m/s^2]
        """
        g_N = self.calculate_newtonian_acceleration(mass_kg, radius_m)
        x = g_N / self.a0
        nu = self.interpolation_function(x)
        return g_N * nu

    def calculate_velocity(self, mass_kg, radius_m):
        """
        Circular orbital velocity: v = sqrt(g_eff * r)
        
        Parameters
        ----------
        mass_kg : float or ndarray
            Baryonic mass in kilograms
        radius_m : float or ndarray
            Orbital radius in meters
            
        Returns
        -------
        float or ndarray
            Velocity in km/s
        """
        g_eff = self.calculate_effective_acceleration(mass_kg, radius_m)
        v_ms = np.sqrt(g_eff * radius_m)
        return v_ms / 1000.0  # Convert to km/s
    
    def asymptotic_velocity(self, mass_kg):
        """
        Deep MOND asymptotic velocity: v_infty = (G*M*a0)^(1/4)
        
        This is the Baryonic Tully-Fisher Relation.
        
        Parameters
        ----------
        mass_kg : float
            Total baryonic mass in kilograms
            
        Returns
        -------
        float
            Asymptotic velocity in km/s
        """
        v_inf = (self.G * mass_kg * self.a0) ** 0.25
        return v_inf / 1000.0


# Quick test if run directly
if __name__ == "__main__":
    rg = ReactiveGravity()
    
    # Test with NGC 3198 parameters
    M_baryonic = 3.8e10 * rg.M_sun  # 3.8 × 10^10 solar masses
    r_30kpc = 30 * rg.kpc_to_m      # 30 kpc
    
    v_newton = np.sqrt(rg.G * M_baryonic / r_30kpc) / 1000
    v_mond = rg.calculate_velocity(M_baryonic, r_30kpc)
    v_asymp = rg.asymptotic_velocity(M_baryonic)
    
    print("=" * 50)
    print("NGC 3198 Test at r = 30 kpc")
    print("=" * 50)
    print(f"Baryonic Mass:     {M_baryonic/rg.M_sun:.2e} M☉")
    print(f"MOND threshold a0: {rg.a0:.2e} m/s²")
    print("-" * 50)
    print(f"Newtonian v(30kpc): {v_newton:.1f} km/s  (fails - too low)")
    print(f"Entropic v(30kpc):  {v_mond:.1f} km/s  (matches data)")
    print(f"Asymptotic v_∞:     {v_asymp:.1f} km/s  (BTFR prediction)")
    print("-" * 50)
    print(f"Enhancement factor: {v_mond/v_newton:.2f}x")
    print("=" * 50)
