import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import Planck18
from astropy import units as u
from scipy.integrate import solve_ivp

class EarlyUniverseCollapse:
    def __init__(self, mass_cloud_solar=1e10, z_start=20.0):
        """
        mass_cloud_solar: Mass in Solar Masses
        z_start: Starting Redshift
        """
        self.M_sol = mass_cloud_solar
        self.z_start = z_start
        
        # Constants
        # G in (Mpc/Gyr)^2 * Mpc / M_sol is weird.
        # Let's use standard SI or km/s/Mpc and convert carefully inside acceleration.
        # Actually simplest is to stick to SI for the physics kernel and convert for plotting.
        # G = 6.674e-11 m^3 kg^-1 s^-2
        self.G_SI = 6.67430e-11
        self.M_SUN_KG = 1.989e30
        self.MPC_M = 3.086e22
        self.GYR_S = 3.154e16
        
        self.mass_kg = self.M_sol * self.M_SUN_KG
        
        # Baseline a0 (Verlinde / MOND)
        self.a0_today = 1.2e-10 # m/s^2
        
        # Calculate start time (Age of universe at z_start)
        self.t_start_gyr = Planck18.age(z_start).value
        # End time (e.g., z=4 or 2 Gyr)
        self.t_end_gyr = 2.0 
        
        print(f"⏳ EarlyUniverse Simulator: Cloud Mass={mass_cloud_solar:.1e} M_sun, z_start={z_start} (t={self.t_start_gyr:.3f} Gyr)")

    def get_redshift_from_time(self, t_gyr):
        """approximation or look up z(t)"""
        # astropy.cosmology.z_at_value is slow to call every step.
        # For simplicity in this derivative, we can pre-compute a table or use an approximation.
        # Let's use a simple matter-dominated approx for z >> 1: H(z) ~ H0 * Omega_m^0.5 * (1+z)^1.5
        # t ~ 2/3 * 1/H(t).
        # But Planck18 has a robust z_at_value. Let's try to map t -> z linearly or just use the a0 scaled by H(t) directly?
        # Verlinde: a0 ~ c * H.
        # So we just need H(t). Planck18 gives H(z). We need H(time).
        # We can implement a look-up table.
        return 0 # Placeholder if needed, but better to use H(t) directly

    def get_H_at_time(self, t_gyr):
        # We assume standard cosmology expansion history for the background
        # H(t) roughly 1/t for high z. 
        # Precise: use pre-calculated array.
        return Planck18.H(self.get_redshift_from_time_fast(t_gyr)).value

    def _precompute_cosmo(self):
        # Create interpolation table for H(t) and z(t)
        ts = np.linspace(0.1, 3.0, 100) # 0.1 to 3 Gyr
        zs = [999] # dummy
        Hs = []
        from astropy.cosmology import z_at_value
        
        z_vals = []
        H_vals = []
        
        print("   - Pre-computing Cosmology Table (z, H vs t)...")
        for t in ts:
            # this is slow, doing it 100 times is ok
            z = z_at_value(Planck18.age, t * u.Gyr)
            H = Planck18.H(z).value # km/s/Mpc
            z_vals.append(z)
            H_vals.append(H)
            
        self.interp_H = lambda t: np.interp(t, ts, H_vals)
        self.interp_z = lambda t: np.interp(t, ts, z_vals)

    def acceleration(self, r_m, t_s, model='reactive'):
        """
        r_m: radius in meters
        t_s: time in seconds
        """
        if r_m <= 0: return 0
        
        # Newtonian g
        g_N = self.G_SI * self.mass_kg / (r_m**2)
        
        if model == 'cdm':
            # CDM: Assume additional mass M_dm.
            # Usually M_dm ~ 5 * M_baryon. But it is extended.
            # Point mass approx for shell collapse: g = G (M_bar + M_dm_enclosed) / r^2
            # Let's be generous to CDM: It has 5x mass immediately.
            g_total = g_N * 6.0 
            return g_total
            
        elif model == 'reactive':
            # 1. Get current H(t)
            t_gyr = t_s / self.GYR_S
            # H comes in km/s/Mpc. Convert to SI (1/s).
            # 1 km/s/Mpc ~ 3.24e-20 1/s
            H_kms_mpc = self.interp_H(t_gyr)
            H_si = H_kms_mpc * 1000 / self.MPC_M 
            
            # 2. Calculate dynamic a0(t) = c * H(t) / (c*H0) * a0? 
            # User formula: a0(z) = a0_today * (Hz / H0)
            # This makes sense if a0 ~ cH.
            H0_val = Planck18.H0.value
            a0_dynamic = self.a0_today * (H_kms_mpc / H0_val)
            
            # 3. Interpolate
            g_eff = (g_N + np.sqrt(g_N**2 + 4 * g_N * a0_dynamic)) / 2
            return g_eff
            
        return g_N

    def simulate_collapse(self, R_initial_kpc=100.0):
        self._precompute_cosmo()
        
        # Initial conditions
        R_0 = R_initial_kpc * 1000 * self.MPC_M / 1e6 # meters (kpc -> m)
        # Start at rest (turnaround point) or with Hubble flow? 
        # Usually distinct structure starts expanding then collapses. 
        # Let's assume turnaround: v=0 at R_0.
        y0 = [R_0, 0.0] 
        
        t_eval = np.linspace(self.t_start_gyr, self.t_end_gyr, 500) * self.GYR_S # seconds
        
        # CDM Solver
        def deriv_cdm(t, y):
            R, v = y
            if R <= 1e10: return [0, 0] # Collapsed
            acc = -self.acceleration(R, t, model='cdm')
            return [v, acc]

        # Reactive Solver
        def deriv_reactive(t, y):
            R, v = y
            if R <= 1e10: return [0, 0]
            acc = -self.acceleration(R, t, model='reactive')
            return [v, acc]
            
        print("   - Evolving CDM Model...")
        sol_cdm = solve_ivp(deriv_cdm, [t_eval[0], t_eval[-1]], y0, t_eval=t_eval, rtol=1e-6)
        
        print("   - Evolving Reactive Model...")
        sol_reactive = solve_ivp(deriv_reactive, [t_eval[0], t_eval[-1]], y0, t_eval=t_eval, rtol=1e-6)
        
        return t_eval, sol_cdm, sol_reactive
