import numpy as np
from astropy import constants as const
from astropy import units as u

class EvaporatingUniverse:
    """
    Models the Universe as a Schwarzschild Black Hole that is evaporating via Hawking Radiation.
    Hypothesis: Dark Energy is the phenomenological manifestation of this mass loss.
    """
    
    def __init__(self, mass_kg=None):
        """
        Initialize the Evaporating Universe.
        
        Args:
            mass_kg: Mass of the universe. If None, uses estimated Mass of Observable Universe (~10^53 kg).
        """
        self.G = const.G.value
        self.c = const.c.value
        self.hbar = const.hbar.value
        self.k_B = const.k_B.value
        
        # Standard estimate: M_universe ~ 1.5e53 kg
        self.mass_kg = mass_kg if mass_kg is not None else 1.5e53
        
        # Stefan-Boltzmann constant (derived for consistency)
        # sigma = pi^2 k^4 / (60 hbar^3 c^2)
        
    def schwarzschild_radius(self, mass=None):
        """R_s = 2GM/c^2"""
        m = mass if mass is not None else self.mass_kg
        return 2 * self.G * m / self.c**2

    def hawking_temperature(self, mass=None):
        """
        T_H = hbar c^3 / (8 pi G M k_B)
        Inverse proportional to mass.
        """
        m = mass if mass is not None else self.mass_kg
        denominator = 8 * np.pi * self.G * m * self.k_B
        numerator = self.hbar * self.c**3
        return numerator / denominator

    def mass_loss_rate(self, mass=None):
        """
        Calculates dM/dt due to Hawking Radiation.
        P = -dE/dt = -c^2 dM/dt
        P = hbar c^6 / (15360 pi G^2 M^2)  (for photons only, simplified)
        
        Returns:
            dM/dt in kg/s (negative value)
        """
        m = mass if mass is not None else self.mass_kg
        
        # Power radiated (Joules/s)
        # Factor 15360 comes from standard derivation for non-rotating, photon-only emission
        # P = (hbar c^6) / (15360 pi G^2 M^2)
        numerator = self.hbar * self.c**6
        denominator = 15360 * np.pi * self.G**2 * m**2
        
        power = numerator / denominator
        
        # dM/dt = - P / c^2
        dM_dt = - power / self.c**2
        return dM_dt

    def lifetime(self, mass=None):
        """
        Time to full evaporation.
        t_evap = 5120 pi G^2 M^3 / (hbar c^4)
        """
        m = mass if mass is not None else self.mass_kg
        
        numerator = 5120 * np.pi * self.G**2 * m**3
        denominator = self.hbar * self.c**4
        return numerator / denominator

    def time_evolution(self, steps=1000):
        """
        Simulates the full evaporation history.
        Because scale is huge, we return log-scale time or relative mass.
        """
        # Since t_evap ~ M^3, we can plot analytically.
        # t_remaining = K * M(t)^3
        # M(t) = M0 * (1 - t/t_life)^(1/3)
        
        t_life = self.lifetime()
        t_norm = np.linspace(0, 1, steps) # t / t_life
        
        # Mass fraction evolution
        # M(t) / M0 = (1 - t/t_life)^(1/3)
        M_norm = (1 - t_norm)**(1/3)
        
        return t_life * t_norm, self.mass_kg * M_norm

    def apparent_acceleration(self, mass=None):
        """
        Hypothesis: The mass loss creates a reduction in gravitational pull
        that mimics acceleration for internal observers.
        
        a_eff = - (G / R^2) * (dM/dt * Delta_t_signal)? 
        
        Or simpler:
        The horizon recedes.
        R_s = 2GM/c^2
        dR_s/dt = (2G/c^2) * dM/dt
        
        Since dM/dt is negative, dR_s/dt is negative (Horizon shrinks).
        If the universe is the INTERIOR, a shrinking horizon might be perceived paradoxically.
        But let's look at the 'Entropic Force' view.
        Psi ~ -GM/R. Gradient changes.
        
        For this simulation, we return the rate of Horizon Shrinkage.
        """
        dM = self.mass_loss_rate(mass)
        dR_dt = (2 * self.G / self.c**2) * dM
        return dR_dt # m/s
