import numpy as np
from scipy.fft import fftn, ifftn
import matplotlib.pyplot as plt
from astropy.cosmology import Planck15

class LensingProjector:
    def __init__(self, data_df, box_size_mpc=500, grid_res=128):
        """
        data_df: DataFrame w/ x,y,z (Mpc)
        box_size_mpc: Cubic box side length
        grid_res: Grid resolution (N^3 cells)
        """
        self.data = data_df[['x', 'y', 'z']].values
        self.box_size = box_size_mpc
        self.grid_res = grid_res
        self.dx = box_size_mpc / grid_res
        self.G = 4.30091e-3 # pc M_sun^-1 (km/s)^2 -> Conversion needed for Mpc units
        # Let's stick to consistent units. 
        # G ~ 4.3e-6 kpc M_sun^-1 (km/s)^2
        # Or simply rely on relative Phantom/Baryon ratio if we don't need absolute kappa yet.
        # But for correctness, let's assume mass=1e11 M_sun per galaxy (rough approx)
        self.GAL_MASS = 1e11 # M_sun
        self.a0 = 1.2e-10 # m/s^2 -> Need conversion to Mpc/Gyr^2 or similar if not normalized
        
        print(f"🔮 LensingProjector init: Box={box_size_mpc} Mpc, Grid={grid_res}^3")

    def _mesh_density(self):
        """Discretize galaxies into density grid"""
        print("   - Gridding particles...")
        # Simple CIC or NGP assignment
        # Normalize to 0..grid_res
        # Shift to center
        pos = self.data + self.box_size/2
        
        # Filter out of bounds
        mask = (pos >= 0).all(axis=1) & (pos < self.box_size).all(axis=1)
        valid_pos = pos[mask]
        
        # Convert to grid indices
        indices = (valid_pos / self.dx).astype(int)
        
        density_grid = np.zeros((self.grid_res, self.grid_res, self.grid_res))
        
        # Add mass
        # np.add.at is unbuffered, fast for histograms
        np.add.at(density_grid, (indices[:,0], indices[:,1], indices[:,2]), self.GAL_MASS)
        
        return density_grid

    def _solve_poisson_fft(self, density_grid):
        """Solve Del^2 Phi = 4 pi G rho via FFT"""
        print("   - Solving Poisson (FFT)...")
        # k-space
        freq = np.fft.fftfreq(self.grid_res, d=self.dx)
        kx, ky, kz = np.meshgrid(freq, freq, freq, indexing='ij')
        k_sq = (2 * np.pi * kx)**2 + (2 * np.pi * ky)**2 + (2 * np.pi * kz)**2
        k_sq[0,0,0] = 1e-10 # Avoid singularity
        
        rho_k = fftn(density_grid)
        
        # Phi_k = - 4 pi G rho_k / k^2 (Sign convention varies, usually -)
        # Using -4piG for attractive potential
        phi_k = -4 * np.pi * self.G * rho_k / k_sq
        
        phi_grid = np.real(ifftn(phi_k))
        return phi_grid

    def _compute_acceleration(self, phi_grid):
        """Compute g = -Grad Phi"""
        # Gradient using central difference
        gz, gy, gx = np.gradient(phi_grid, self.dx)
        # Magnitude
        g_mag = np.sqrt(gx**2 + gy**2 + gz**2)
        return g_mag, gx, gy, gz

    def compute_convergence_map(self):
        """
        Main Pipeline:
        Rho_bar -> g_N -> g_eff -> Rho_eff -> Sigma_eff -> Kappa
        """
        # 1. Baryonic Density
        rho_bar = self._mesh_density()
        
        # 2. Newtonian Acceleration
        # We need g_N. Solving Poisson for Phi_N is best way.
        # Note on Units: G=1 for now to see relative enhancement? 
        # No, let's try to keep physical scaling or just return the Phantom/Baryon ratio map.
        # Actually, for 2D visualization, comparing Sigma_eff vs Sigma_bar is powerful.
        
        phi_N = self._solve_poisson_fft(rho_bar)
        g_N_mag, _, _, _ = self._compute_acceleration(phi_N)
        
        # 3. Entropic Correction (Verlinde)
        # g_obs = (g_N + sqrt(g_N^2 + 4 g_N a0)) / 2
        # Need to handle unit conversion carefully or normalize.
        # Let's assume a0 is in compatible units. 
        # For simplicity in this PoC, we assume standard units or dimensionless multiplier for a0 effect.
        # Using a relative a0 scaled to grid typical g_N
        mean_g = np.mean(g_N_mag[g_N_mag > 0])
        effective_a0 = mean_g * 5 # Strong scaling for visibility in PoC
        
        print(f"   - Applying Reactive Kernel (a0 ~ {effective_a0:.2e})...")
        g_eff_mag = (g_N_mag + np.sqrt(g_N_mag**2 + 4 * g_N_mag * effective_a0)) / 2
        
        # Enhancement factor eta = g_eff / g_N
        # Avoid div zero
        mask = g_N_mag > 0
        eta = np.ones_like(g_N_mag)
        eta[mask] = g_eff_mag[mask] / g_N_mag[mask]
        
        # 4. Effective Density (Phantom)
        # rho_eff approx rho_bar * eta (Locally)
        # Or rigorous: div(g_eff). 
        # Detailed div is noisy on grid. Local scaling rho_eff = rho_bar * eta is a good 1st order approximation for the LENSING contrast.
        # Actually, lensing is sourced by Sigma_eff.
        # Let's Scale the density grid by eta.
        rho_eff = rho_bar * eta
        
        # 5. Projection (Sigma)
        # Integrate along Z
        sigma_eff = np.sum(rho_eff, axis=2)
        sigma_bar = np.sum(rho_bar, axis=2)
        
        return sigma_bar, sigma_eff

    def plot_maps(self, sigma_bar, sigma_eff):
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Log scale maps
        im1 = axes[0].imshow(np.log1p(sigma_bar), cmap='inferno')
        axes[0].set_title("Newtonian Mass (Baryons Only)")
        plt.colorbar(im1, ax=axes[0])
        
        im2 = axes[1].imshow(np.log1p(sigma_eff), cmap='magma')
        axes[1].set_title("Reactive Lensing Mass (Baryons + Entropy)")
        plt.colorbar(im2, ax=axes[1])
        
        plt.suptitle("Weak Lensing Prediction: Newtonian vs Entropic", fontsize=16)
        plt.savefig("Validation/lensing_prediction_map.png")
        print("✅ Lensing map saved to Validation/lensing_prediction_map.png")
