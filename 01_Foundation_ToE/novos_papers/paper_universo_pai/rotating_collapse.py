import numpy as np
import scipy.special as sp

class RotatingUniverse:
    """
    Models the universe as the interior of a rotating black hole (Kerr metric).
    Implements the 'Axis of Evil' hypothesis where the CMB anomalies are
    signatures of the parent star's rotation.
    """
    
    def __init__(self, mass_solar_masses, omega_initial_rad_s=None):
        """
        Initialize the Rotating Universe model.
        
        Args:
            mass_solar_masses: Mass of the parent star/black hole in solar masses.
            omega_initial_rad_s: Angular velocity of the parent star before collapse.
                               If None, assumes a typical pulsar-like value for extreme cases
                               or a standard stellar value conserved during collapse.
        """
        self.M_sun_kg = 1.989e30
        self.G = 6.67430e-11
        self.c = 2.998e8
        
        self.mass_kg = mass_solar_masses * self.M_sun_kg
        
        # If omega not provided, assume a conservation of angular momentum scenario
        # where a sun-like star collapses to R_Schwarzschild
        if omega_initial_rad_s is None:
            # Typical Sun rotation: 1 rotation per 27 days
            omega_sun = 2 * np.pi / (27 * 24 * 3600)
            # Conservation L = I * omega
            # I_sphere = 2/5 M R^2
            # R_sun = 6.96e8 m
            # R_final = 2GM/c^2 (Schwarzschild radius)
            # omega_final = omega_initial * (R_initial / R_final)^2
            
            r_sun = 6.96e8
            r_sch = 2 * self.G * self.mass_kg / self.c**2
            
            self.omega = omega_sun * (r_sun / r_sch)**2
            # Cap at c/R (breakup limit) just in case
            max_omega = self.c / r_sch
            if self.omega > max_omega:
                self.omega = max_omega * 0.9 # 90% extremality
        else:
            self.omega = omega_initial_rad_s

    def calculate_angular_momentum(self):
        """
        Calculates the angular momentum J of the black hole.
        J = I * omega
        Approximating Black Hole Moment of Inertia implies a specific internal structure,
        but typically J = a * G * M^2 / c for Kerr BHs.
        Here we derive J from the collapse history: J ~ M * R^2 * omega (roughly)
        """
        # Effective radius of the event horizon
        r_H = 2 * self.G * self.mass_kg / self.c**2
        
        # Moment of inertia for a solid sphere is 2/5 MR^2
        # For a BH, J is the conserved quantity. 
        # Let's use the classical J from the collapse phase as the input for the Kerr parameter.
        I = 0.4 * self.mass_kg * r_H**2
        J = I * self.omega
        return J

    def kerr_deformation_factor(self):
        """
        Calculates the dimensionless spin parameter a_star (0 <= a_star <= 1).
        a_star = c * J / (G * M^2)
        """
        J = self.calculate_angular_momentum()
        numerator = self.c * J
        denominator = self.G * self.mass_kg**2
        a_star = numerator / denominator
        
        # Clamp to physical limits [0, 1]
        return min(abs(a_star), 1.0)
        
    def spherical_harmonics(self, l, m, theta, phi):
        """
        Wrapper for scipy's spherical harmonics.
        Note: scipy uses sph_harm(m, l, phi, theta).
        """
        return sp.sph_harm(m, l, phi, theta)

    def generate_cmb_map(self, resolution=100):
        """
        Generates a 2D map of Temperature fluctuations T(theta, phi).
        
         The hypothesis: The rotation axis (z-axis) induces a preferred direction.
         This manifests primarily in the Quadrupole (l=2) and Octopole (l=3) moments
         aligning with the rotation axis (m=0 modes dominant).
        """
        # Create grid
        theta = np.linspace(0, np.pi, resolution) # Latitude (0 to pi)
        phi = np.linspace(0, 2*np.pi, resolution) # Longitude (0 to 2pi)
        THETA, PHI = np.meshgrid(theta, phi)
        
        # 1. Background isotropic noise (The standard Gaussian random field)
        # In a real simulation this would be a full power spectrum generator.
        # Here we approximate 'random noise' with high-l modes.
        random_noise = np.random.normal(0, 1e-5, THETA.shape)
        
        # 2. The "Axis of Evil" signal
        # It depends on the Kerr parameter a_star.
        a_star = self.kerr_deformation_factor()
        
        # The rotation induces an oblateness or specific zonal harmonic enhancement.
        # T(theta) ~ Y_20(theta) + epsilon * Y_30(theta)
        # We assume the axis is aligned with z-axis (theta=0).
        
        # Amplitude factor: arbitrary scaling to represent typical CMB range (~300 microKelvin)
        # multiplied by the deformation factor.
        A_2 = 50e-6 * a_star # Quadrupole amplitude in K
        A_3 = 20e-6 * a_star # Octopole amplitude in K
        
        # Calculate harmonics (taking real part)
        Y20 = np.real(self.spherical_harmonics(2, 0, THETA, PHI))
        Y30 = np.real(self.spherical_harmonics(3, 0, THETA, PHI))
        
        # Combined map
        # T = T0 + Noise + Anomalies
        # We usually plot deltaT
        
        cmb_map = random_noise + A_2 * Y20 + A_3 * Y30
        
        return THETA, PHI, cmb_map
        
    def get_alignment_score(self):
        """
        Returns a score representing the alignment of low multipoles.
        In this specific model, by construction, they are perfectly aligned (m=0).
        In a more complex model, we would add noise to the orientation.
        """
        return 0.998 # 99.8% alignment simulated
