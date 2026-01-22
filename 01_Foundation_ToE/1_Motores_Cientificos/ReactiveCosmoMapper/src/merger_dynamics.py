import numpy as np
from reactive_gravity import ReactiveGravity

class GalaxyMerger:
    def __init__(self, n_stars_per_gal=200, separation_kpc=150.0, impact_kpc=30.0, vel_kms=100.0):
        self.grav = ReactiveGravity(a0=1.2e-10)
        
        # Simulation Units
        self.KPC_TO_M = 3.086e19
        self.GYR_TO_S = 3.154e16
        self.KM_TO_M = 1000.0
        self.M_GAL = 1e11 # Solar mass per galaxy
        self.M_STAR_SOL = self.M_GAL / n_stars_per_gal
        self.M_STAR_KG = self.M_STAR_SOL * 1.989e30
        
        self.N = n_stars_per_gal * 2
        
        # Init Galaxy 1 (Target)
        pos1, vel1 = self._init_galaxy(n_stars_per_gal)
        pos1[:, 0] -= separation_kpc / 2
        pos1[:, 1] -= impact_kpc / 2
        vel1[:, 0] += vel_kms / 2
        
        # Init Galaxy 2 (Impactor)
        pos2, vel2 = self._init_galaxy(n_stars_per_gal)
        pos2[:, 0] += separation_kpc / 2
        pos2[:, 1] += impact_kpc / 2
        vel2[:, 0] -= vel_kms / 2
        
        self.pos = np.vstack([pos1, pos2])
        self.vel = np.vstack([vel1, vel2])
        
        # Track centers for statistics
        self.idx_g1 = slice(0, n_stars_per_gal)
        self.idx_g2 = slice(n_stars_per_gal, self.N)
        
        self.t = 0.0

    def _init_galaxy(self, n):
        # reuse disk logic
        Rd = 3.0 
        pos = []
        vel = []
        while len(pos) < n:
            r = np.random.uniform(0.1, 10) # Smaller disk to see tidal tails clearly
            if np.random.uniform(0, 1.5) < r * np.exp(-r/Rd):
                theta = np.random.uniform(0, 2*np.pi)
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = np.random.uniform(-0.1, 0.1) # Slight thickness
                pos.append([x, y, z])
                
                # Circular Velocity (Approximate for stability)
                # v^2 = G M(<r) / r? Or use reactive curve?
                # Let's use reactive curve for a single galaxy
                r_m = r * self.KPC_TO_M
                g_eff = self.grav.calculate_effective_acceleration(self.M_GAL, r_m) 
                # Note: M_GAL is total mass, but at r < 10 inside 10 it's less.
                # Approx point mass center for initialization speed is ok for visual "spiral"
                v = np.sqrt(g_eff * r_m) / 1000.0 
                
                # Tangent
                vx = -v * np.sin(theta)
                vy = v * np.cos(theta)
                vel.append([vx, vy, 0.0])
                
        return np.array(pos), np.array(vel)

    def step(self, dt_gyr):
        # Direct N-Body (O(N^2))
        # 1. Calculate Distances
        # Broadcast mechanism
        # r_vec shape (N, N, 3)
        # We need to avoid memory blowup. Loop over particles might be safer for python if N=400.
        # N=400 -> N^2 = 160000. small enough for matrix.
        
        pos_m = self.pos * self.KPC_TO_M
        
        # r_ij = r_j - r_i
        # shape (N, 1, 3) - (1, N, 3) -> (N, N, 3)
        diff = self.pos[:, np.newaxis, :] - self.pos[np.newaxis, :, :] 
        r_sq = np.sum(diff**2, axis=-1) # (N, N) in kpc^2
        np.fill_diagonal(r_sq, np.inf) # No self-force
        
        r_dist = np.sqrt(r_sq) # kpc
        r_m = r_dist * self.KPC_TO_M
        
        # 2. Newtonian Force Magnitude (F = G m m / r^2)
        # a_i = sum_j (G m_j / r_ij^2)
        # All stars have same mass
        g_N_mag = (self.grav.G * self.M_STAR_KG) / (r_m**2) # m/s^2 per pair contribution
        
        # 3. Sum Newtonian Vectors
        # vec_N = sum ( g_N_mag * (diff / r_dist) )
        # diff (N, N, 3) kcp ... diff/r_dist is unit vector.
        # careful with units. diff is kpc. r_dist is kpc. ratio is unitless.
        
        # We need Total Newtonian Acceleration on particle i
        # g_N_total_i = sum_j ( G m_j / r_ij^2 * r^hat_ij )
        # Let's project g_N_mag onto unit vectors
        
        # Unit vectors
        u_vec = diff / r_dist[:, :, np.newaxis] # (N, N, 3)
        
        # Acc vectors (N, N, 3)
        a_vec_pairwise = g_N_mag[:, :, np.newaxis] * u_vec # m/s^2 is g_N_mag? yes.
        # Who pulls who? r_ij = r_j - r_i. Vector points to j. Correct.
        
        # Sum over j (axis 1)
        g_N_tot_vec = np.nansum(a_vec_pairwise, axis=1) # (N, 3) m/s^2
        g_N_tot_mag = np.linalg.norm(g_N_tot_vec, axis=1)
        
        # 4. Reactive Correction (on the TOTAL vector)
        # a_eff = (g_N + sqrt(g_N^2 + 4 g_N a0)) / 2
        # direction same as g_N
        
        g_eff_mag = (g_N_tot_mag + np.sqrt(g_N_tot_mag**2 + 4 * g_N_tot_mag * self.grav.a0)) / 2
        
        # Scale vector
        # avoid div by zero
        factor = np.zeros_like(g_N_tot_mag)
        mask = g_N_tot_mag > 1e-15
        factor[mask] = g_eff_mag[mask] / g_N_tot_mag[mask]
        
        acc_eff_vec = g_N_tot_vec * factor[:, np.newaxis] # m/s^2
        
        # 5. Integration (Leapfrog-ish or Euler)
        # dv (km/s) = a (m/s^2) * dt (Gyr) * conversion
        CONV = (self.GYR_TO_S / 1000.0) # m/s^2 -> km/s per Gyr ? 
        # a [m/s^2] * t [s] = v [m/s]. /1000 -> km/s.
        
        self.vel += acc_eff_vec * dt_gyr * CONV
        
        # dx (kpc) = v (km/s) * dt (Gyr) * conversion
        # 1 km/s * 1 Gyr = 1.022 kpc
        CONV_POS = (self.KM_TO_M * self.GYR_TO_S) / self.KPC_TO_M
        
        self.pos += self.vel * dt_gyr * CONV_POS
        self.t += dt_gyr
        
        # Return center distance
        c1 = np.mean(self.pos[self.idx_g1], axis=0)
        c2 = np.mean(self.pos[self.idx_g2], axis=0)
        dist = np.linalg.norm(c1 - c2)
        return dist
