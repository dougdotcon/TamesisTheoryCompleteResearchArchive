import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class SatelliteDynamics:
    def __init__(self, n_satellites=50, galaxy_mass_solar=1e11, g_ext_factor=0.1):
        """
        n_satellites: Number of particles.
        galaxy_mass_solar: Mass of host.
        g_ext_factor: Strength of external field relative to internal field at typical radius.
        """
        self.N = n_satellites
        self.M_sol = galaxy_mass_solar
        
        # Units
        # Length: kpc
        # Velocity: km/s
        # Time: Gyr
        # G must be consistent.
        # G ~ 4.301e-6 kpc M_sun^-1 (km/s)^2
        self.G = 4.301e-6 
        
        self.a0 = 3700.0 # (km/s)^2 / kpc approx 1.2e-10 m/s^2 
        # 1.2e-10 m/s^2 * (1e-3 km/m) / (3.086e19 kpc/m) * (3.15e16 s/Gyr)^2 ?? No.
        # Let's keep (km/s)^2 / kpc.
        # 1.2e-10 m/s^2 = 1.2e-13 km/s^2
        # = 1.2e-13 * (3.086e16 km/kpc) ... no.
        # 1 kpc = 3.086e19 m
        # 1.2e-10 m/s^2 * (1 kpc / 3.086e19 m) * (1e3 m/km * s)^2? No.
        # Let's stick to: a0 ~ 3700 (km/s)^2 / kpc is commonly cited for MOND.
        
        # Define External Field Vector (e.g., towards Andromeda/Attractor)
        # Choosing Z-axis for simplicity to see if disk forms in XY or otherwise.
        # Assume g_ext is constant.
        # Magnitude set by factor.
        self.g_ext_vec = np.array([0.0, 0.0, 1.0]) 
        # Normalize later in run
        self.g_ext_mag = 0.0 

    def reactive_kernel(self, g_N_vec):
        """
        Verlinde/MOND Interpolation on a vector.
        g_obs = (g_N + sqrt(g_N^2 + 4 g_N a0)) / 2
        
        For Vector with EFE:
        We apply the scalar scaling to the TOTAL Newtonian vector, then subtract host acceleration.
        """
        g_mag = np.linalg.norm(g_N_vec, axis=-1, keepdims=True)
        # If zero, return zero
        mask = g_mag > 1e-12
        
        # Scaling factor mu(x) or nu(y)
        # g_eff = g_N * nu
        # Eq: g_eff = (g_N + sqrt(g_N^2 + 4 g_N a0)) / 2
        # nu = g_eff / g_N = 0.5 * (1 + sqrt(1 + 4 a0 / g_N))
        
        g_eff_mag = np.zeros_like(g_mag)
        g_eff_mag[mask] = 0.5 * (g_mag[mask] + np.sqrt(g_mag[mask]**2 + 4 * g_mag[mask] * self.a0))
        
        # Direction implies parallel to g_N_vec
        # g_eff_vec = (g_eff_mag / g_mag) * g_N_vec
        
        # Careful with broadcasting
        factor = np.ones_like(g_mag)
        factor[mask] = g_eff_mag[mask] / g_mag[mask]
        
        return g_N_vec * factor

    def relative_acceleration(self, positions_kpc, model='reactive'):
        """
        Calculates relative acceleration of satellites w.r.t Host.
        Positions: (N, 3)
        """
        # Host is at [0,0,0] and feels g_ext.
        # Satellites at r feel g_int + g_ext.
        
        # 1. Internal Newtonian Field (Host -> Sat)
        r = np.linalg.norm(positions_kpc, axis=1, keepdims=True)
        r[r < 0.1] = 0.1 # Softening
        
        g_int_dir = -positions_kpc / r
        g_int_mag = self.G * self.M_sol / (r**2)
        g_int_vec = g_int_dir * g_int_mag
        
        # 2. External Field (Constant)
        g_ext_vec_all = np.tile(self.g_ext_vec * self.g_ext_mag, (self.N, 1))
        
        # 3. Total Newtonian Field on Satellites
        g_tot_N_sat = g_int_vec + g_ext_vec_all
        
        # 4. Total Newtonian Field on Host
        # Host is at 0, so g_int is 0. Only g_ext.
        g_tot_N_host = self.g_ext_vec * self.g_ext_mag
        
        if model == 'cdm':
            # In CDM, Strong Equivalence Principle holds.
            # a_sat = g_tot_N_sat + Halo
            # a_host = g_tot_N_host + Halo(0)
            # relative = g_tot_N_sat - g_tot_N_host = g_int_vec.
            # EFE cancels out completely (up to tidal terms, ignored here).
            # Halo: simple NFW or isothermal sphere.
            # Let's assume Isothermal: v_c^2 / r
            # v_c ~ 200 km/s flat.
            v_flat = 200.0
            a_halo_mag = v_flat**2 / r
            a_halo_vec = g_int_dir * a_halo_mag
            return a_halo_vec # Dominates over Newtonian
            
        elif model == 'reactive':
            # EFE DOES NOT cancel.
            # a_sat = R(g_tot_N_sat)
            # a_host = R(g_tot_N_host)
            # a_rel = a_sat - a_host
            
            a_sat = self.reactive_kernel(g_tot_N_sat)
            a_host = self.reactive_kernel(np.array([g_tot_N_host])) # Shape (1,3)
            
            a_rel = a_sat - a_host
            return a_rel

    def simulate(self, t_gyr=5.0):
        print(f"🛸 Simulating Satellite Dynamics (t={t_gyr} Gyr)...")
        # Initialize Random Isotropic Distribution
        # r ~ 100 kpc
        r_scale = 100.0
        
        # Random on sphere
        u_rand = np.random.uniform(0, 1, self.N)
        v_rand = np.random.uniform(0, 1, self.N)
        theta = 2 * np.pi * u_rand
        phi = np.arccos(2 * v_rand - 1)
        
        x = r_scale * np.sin(phi) * np.cos(theta)
        y = r_scale * np.sin(phi) * np.sin(theta)
        z = r_scale * np.cos(phi)
        
        pos = np.column_stack([x,y,z])
        
        # Set g_ext magnitude based on internal field at r_scale
        g_int_at_r = self.G * self.M_sol / (r_scale**2)
        self.g_ext_mag = g_int_at_r * 0.2 # 20% of internal field (Strong EFE)
        print(f"   - External Field: {self.g_ext_mag:.2e} (km/s)^2/kpc (Z-axis)")
        
        # Velocities: Tangential approx to stay in orbit
        # v ~ sqrt(a * r). 
        # Isotropic random directions tangent to radius?
        # Or Just random angular momentum?
        # Let's give them approx circular velocity magnitude but random orientation plane.
        
        vel = np.zeros_like(pos)
        for i in range(self.N):
            p = pos[i]
            r_val = np.linalg.norm(p)
            v_mag = 150.0 # km/s approx
            
            # Random tangent vector
            # p cross z maybe?
            # random vec
            rand_v = np.random.randn(3)
            tangent = np.cross(p, rand_v)
            tangent = tangent / np.linalg.norm(tangent) * v_mag
            vel[i] = tangent
            
        # Integration
        # State: [x1, y1, z1, ..., vx1, vy1, vz1, ...]
        y0 = np.concatenate([pos.flatten(), vel.flatten()])
        
        t_eval = np.linspace(0, t_gyr * 0.977, 200) # 1 Gyr ~ 0.977 units if G is in (km/s)^2 kpc/M_sun?? 
        # G units: kpc * (km/s)^2 / M_sun.
        # Acceleration: (km/s)^2 / kpc.
        # x: kpc. v: km/s.
        # t = x/v = kpc / (km/s).
        # 1 kpc = 3.086e16 km.
        # 1 unit time = 3.086e16 seconds ~ 0.978 Gyr.
        # So t=1 is approx 1 Gyr. Correct.
        t_eval = np.linspace(0, t_gyr, 100)
        
        def deriv(t, y):
            # unpack
            curr_pos = y[:3*self.N].reshape((self.N, 3))
            curr_vel = y[3*self.N:].reshape((self.N, 3))
            
            acc = self.relative_acceleration(curr_pos, model='reactive')
            # Add some drag coefficient?? 
            # No, conservative dynamics should aligns orbits via phase mixing or precession?
            # Actually, without dissipation, they won't settle into a plane unless the potential makes the plane an attractor 
            # or we filter for survivors.
            # But MOND EFE causes "precession" of the orbital plane.
            # Let's see if the potential squashing is visible.
            
            return np.concatenate([curr_vel.flatten(), acc.flatten()])

        sol = solve_ivp(deriv, [0, t_gyr], y0, t_eval=t_eval, rtol=1e-5)
        
        final_pos = sol.y[:3*self.N, -1].reshape((self.N, 3))
        return pos, final_pos

