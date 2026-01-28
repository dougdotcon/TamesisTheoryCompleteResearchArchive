import unittest
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from reactive_gravity import ReactiveGravity

class TestReactiveGravity(unittest.TestCase):
    def setUp(self):
        self.gravity = ReactiveGravity(a0=1.2e-10)
        self.M_sun = 1.989e30 # kg

    def test_newtonian_regime(self):
        """
        High acceleration regime (g_N >> a0).
        Should converge to Newton: g_eff approx g_N.
        """
        # Close to a star: 1 AU
        r = 1.496e11 # meters
        g_N = self.gravity.calculate_newtonian_acceleration(self.M_sun, r)
        g_eff = self.gravity.calculate_effective_acceleration(self.M_sun, r)
        
        # Checking relative error < 0.1% (Deep Newtonian)
        # Note: actually g_eff will be slightly larger than g_N always, but should be close.
        # Actually in solar system a0 is negligible compared to g_sun.
        # g_sun at earth ~ 0.006 m/s^2. a0 ~ 1e-10.
        # Ratio ~ 1e8.
        
        rel_diff = abs(g_eff - g_N) / g_N
        self.assertLess(rel_diff, 1e-4, "High accel regime should be Newtonian")

    def test_entropic_regime(self):
        """
        Deep MOND regime (g_N << a0).
        g_eff approx sqrt(g_N * a0).
        """
        # Very far away: 100 kpc
        # 1 kpc = 3.086e19 m
        r = 100 * 3.086e19 
        mass = 1e10 * self.M_sun # Small galaxy
        
        g_N = self.gravity.calculate_newtonian_acceleration(mass, r)
        g_mond_theoretical = np.sqrt(g_N * self.gravity.a0)
        
        g_eff = self.gravity.calculate_effective_acceleration(mass, r)
        
        # Check agreement with Deep MOND limit
        rel_diff = abs(g_eff - g_mond_theoretical) / g_eff
        self.assertLess(rel_diff, 0.1, "Low accel regime should follow sqrt(gN*a0)")

    def test_flat_rotation_curve(self):
        """
        Velocity should become roughly constant at large radii.
        """
        # Adjusted to ensure we are in Deep MOND regime (g_N << a0)
        # At 20 kpc for a 1e11 M_sun galaxy, we are still in transition.
        # Let's test at 200, 300, 400 kpc
        radii_kpc = np.array([200, 300, 400]) 
        radii_m = radii_kpc * 3.086e19
        
        mass = 1e11 * self.M_sun
        
        velocities = []
        for r in radii_m:
            v = self.gravity.calculate_velocity(mass, r)
            velocities.append(v)
            
        velocities = np.array(velocities)
        
        # Calculate variation spread
        spread = (np.max(velocities) - np.min(velocities)) / np.mean(velocities)
        
        # In pure point mass MOND, v is exactly constant.
        self.assertLess(spread, 0.05, "Velocity should be approximately flat at large radii")

if __name__ == '__main__':
    unittest.main()
