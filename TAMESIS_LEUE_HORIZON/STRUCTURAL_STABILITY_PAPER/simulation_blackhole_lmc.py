
"""
simulation_blackhole_lmc.py
---------------------------
Tamesis-Leue Integration Project
Hypothesis 1 Verification: Event Horizon as LMC Saturation

This script implements the ExactROC and ExactLMC modules from Leue's framework
to simulate a scalar field collapse. It tests if the region where the LMC coefficient
saturates (|t| -> 1) exhibits Holographic properties (Entropy ~ Area).

Author: Antigravity (Agent) for Tamesis Research
"""

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
import sys
import os

# --- 1. CORE MODULES (LEUE FRAMEWORK) ---

class ExactROC:
    def __init__(self, grid_size=(16,16,16,16), v_direction=(1,0,0,0), epsilon=0.1):
        self.Lt, self.Lx, self.Ly, self.Lz = grid_size
        self.N = np.prod(grid_size)
        self.v = np.array(v_direction, dtype=float)
        self.v /= np.linalg.norm(self.v)
        self.epsilon = epsilon
        
        # Build frequency grids
        self.kx = 2*np.pi * np.fft.fftfreq(self.Lx)
        self.ky = 2*np.pi * np.fft.fftfreq(self.Ly)
        self.kz = 2*np.pi * np.fft.fftfreq(self.Lz)
        self.kt = 2*np.pi * np.fft.fftfreq(self.Lt) # Frequency in time as well
        
    def build_roc_projectors_exact(self):
        """Construct exact P+, P0, P- projectors (in Fourier Space)"""
        # We need to construct the full 4D k-grid to apply direction dot product
        # Broadcasting handles the meshgrid efficiently without full expansion if we are careful,
        # but for clarity in this proof-of-concept, we iterate or use meshgrid.
        # Given memory, meshgrid is better.
        
        Kt, Kx, Ky, Kz = np.meshgrid(self.kt, self.kx, self.ky, self.kz, indexing='ij')
        
        # k dot v
        k_dot_v = Kt*self.v[0] + Kx*self.v[1] + Ky*self.v[2] + Kz*self.v[3]
        
        # Indicator functions
        # For P+, k.v > epsilon
        indicator_plus = (k_dot_v > self.epsilon).astype(float)
        
        # For P0, |k.v| <= epsilon
        indicator_zero = (np.abs(k_dot_v) <= self.epsilon).astype(float)
        
        # For P-, k.v < -epsilon
        indicator_minus = (k_dot_v < -self.epsilon).astype(float)
        
        # Normalize (Partition of Unity enforcement - theoretically sum is 1 except at boundaries if overlap)
        # Here they are disjoint by definition, so sum is 1.
        
        return indicator_plus, indicator_zero, indicator_minus

    def apply_projector(self, f_field_4d, indicator_grid):
        """Apply ROC projector to field f"""
        # f_4d is (Lt, Lx, Ly, Lz)
        f_hat = np.fft.fftn(f_field_4d)
        f_filtered_hat = f_hat * indicator_grid
        f_filtered = np.fft.ifftn(f_filtered_hat).real
        return f_filtered

class ExactLMC:
    def __init__(self, grid_size, beta=0.12, sigma_0=1.0):
        self.grid_size = grid_size
        self.N = np.prod(grid_size)
        self.beta = beta
        self.sigma_0 = sigma_0
        
    def build_lmc_field_from_source(self, source_field, elasticity=1.0):
        """
        Maps a physical source field (e.g. Mass Density) to LMC coefficients.
        
        In Leue framework, LMC t(x) is the 'modulation'.
        Hypothesis: Mass acts as a 'saturating pressure' on the LMC field.
        
        t(x) = tanh(elasticity * source(x))
        This enforces t in [-1, 1].
        """
        # Normalize source to act as pressure
        t_field = np.tanh(elasticity * source_field)
        return t_field

    def get_horizon_mask(self, t_field, threshold=0.99):
        """Identifies regions where LMC is saturated."""
        return np.abs(t_field) >= threshold

# --- 2. EXPERIMENT SETUP ---

def run_experiment_h1():
    print("=== TAMESIS-LEUE INTEGRATION: EXPERIMENT 01 ===")
    print("Hypothesis: Event Horizon correlates with LMC Saturation")
    print("Metric: Verifying Area Law (Entropy ~ Area) vs Volume Law")
    
    # 1. Setup Grid
    # Using 16^4 grid. 
    L = 16
    grid_size = (L, L, L, L)
    print(f"Grid Size: {grid_size} ({np.prod(grid_size)} pts)")
    
    roc = ExactROC(grid_size=grid_size, v_direction=(1,0,0,0), epsilon=0.2)
    lmc = ExactLMC(grid_size=grid_size)
    
    # Pre-calculate projectors
    print("Building ROC Projectors...")
    IndP, Ind0, IndM = roc.build_roc_projectors_exact()
    
    # 2. Simulation Loop: Increasing Mass
    masses = np.linspace(0.1, 10.0, 20)
    areas = []
    entropies_p0 = []
    entropies_vol = []
    
    # Coordinate grid for source generation
    t = np.linspace(-1, 1, L)
    x = np.linspace(-1, 1, L)
    y = np.linspace(-1, 1, L)
    z = np.linspace(-1, 1, L)
    T, X, Y, Z = np.meshgrid(t, x, y, z, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    
    print("\nStarting Collapse Simulation...")
    print(f"{'Mass':<10} | {'Horizon Area':<15} | {'P0 Entropy':<15} | {'Vol Entropy':<15}")
    print("-" * 65)
    
    for M in masses:
        # Source: Gaussian blob of 'Mass/Information' at center
        # Static in time to simplify (cylinder in 4D)
        source = M * np.exp(-R**2 / (0.5**2))
        
        # Calculate LMC field
        # t(x) saturates to 1 at center as M increases
        t_field = lmc.build_lmc_field_from_source(source, elasticity=2.0)
        
        # Identify Horizon (Where |t| > 0.99)
        horizon_mask = lmc.get_horizon_mask(t_field, threshold=0.95)
        
        # Calculate Horizon Area (Approximate)
        # As this is a 4D grid, the "spatial" horizon is a 2D surface at each time slice.
        # We look at the central time slice for measurement.
        t_slice_idx = L // 2
        horizon_slice = horizon_mask[t_slice_idx]
        
        # Area estimation: Count surface pixels of the boolean mask blob
        # Simple method: Volume - Eroded_Volume (or just count boundary pixels)
        # Here we approximate by simple counting of 'surface' voxels
        # For a sphere, Area ~ (Volume)^(2/3) roughly, but let's try to be more precise
        # A voxel is on surface if it is TRUE and has at least one FALSE neighbor
        
        # Simple 3D Convolution to find edges
        from scipy.ndimage import binary_erosion
        core_vol = np.sum(horizon_slice)
        if core_vol == 0:
            area = 0
        else:
            eroded = binary_erosion(horizon_slice)
            area = np.sum(horizon_slice ^ eroded) # XOR gives the edge
        
        # 3. Calculate "ROA Entropy"
        # Leue theory: Entropy is stored in the Neutral Channel (P0) when P+ is blocked.
        # We inject white noise (vacuum fluctuations) and measure how much gets trapped in P0 
        # within the horizon region.
        
        # Vacuum fluctuations
        noise = np.random.randn(*grid_size)
        
        # Modulate noise by LMC field (Interaction)
        # H_int ~ t(x) * noise
        interaction = t_field * noise
        
        # Project onto P0
        p0_component = roc.apply_projector(interaction, Ind0)
        
        # Energy in P0 confined to the Horizon region
        # We sum P0 energy ONLY inside the saturated region
        p0_energy = np.sum(p0_component[horizon_mask]**2)
        
        # Normalization
        entropy = p0_energy / (np.prod(grid_size)) * 1000 
        
        areas.append(area)
        entropies_p0.append(entropy)
        entropies_vol.append(core_vol) # For comparison
        
        print(f"{M:<10.2f} | {area:<15.0f} | {entropy:<15.4f} | {core_vol:<15.0f}")

    # --- 3. ANALYSIS ---
    
    # Check correlation: Is Entropy linear with Area or Volume?
    areas = np.array(areas)
    ents = np.array(entropies_p0)
    vols = np.array(entropies_vol)
    
    # Filter non-zero
    mask = areas > 0
    if np.sum(mask) < 3:
        print("Not enough data points for correlation.")
        return

    a_valid = areas[mask]
    e_valid = ents[mask]
    v_valid = vols[mask]
    
    # Normalize to compare shapes
    a_norm = a_valid / a_valid.max()
    e_norm = e_valid / e_valid.max()
    v_norm = v_valid / v_valid.max()
    
    mse_area = np.mean((e_norm - a_norm)**2)
    mse_vol = np.mean((e_norm - v_norm)**2)
    
    print("\n--- RESULTS ---")
    print(f"MSE (Entropy vs Area):   {mse_area:.6f}")
    print(f"MSE (Entropy vs Volume): {mse_vol:.6f}")
    
    if mse_area < mse_vol:
        print("\n[SUCCESS] Hypothesis 1 CONFIRMED: Entropy follows Area Law.")
        print("The LMC Saturation Horizon behaves holographically.")
    else:
        print("\n[FAILURE] Hypothesis 1 REFUTED: Entropy follows Volume Law.")
    
    # Plot
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(a_norm, label='Area (Normalized)')
        plt.plot(v_norm, label='Volume (Normalized)', linestyle='--')
        plt.plot(e_norm, label='P0 Entropy (Measured)', linewidth=2, color='red')
        plt.title('H1 Verification: Horizon Area vs P0 Entropy')
        plt.legend()
        plt.grid()
        plt.savefig('h1_result_area_law.png')
        print("Plot saved to h1_result_area_law.png")
    except Exception as e:
        print(f"Plotting failed: {e}")

if __name__ == "__main__":
    run_experiment_h1()
