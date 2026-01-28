
"""
simulation_blackhole_lmc_v2.py
------------------------------
Tamesis-Leue Integration Project
Hypothesis 1.1 Verification: Rigid Core & Surface Entropy

Refinement: The previous simulation showed Volume Law because we assumed the saturated bulk 
was active.
New Hypothesis (Rigid Core): As LMC |t| -> 1, the ROA Spectral Gap becomes maximal, 
suppressing low-energy fluctuations (Freezing). 
Entropy (Information Capacity) is confined to the "Phase Transition" layer (Horizon)
where the gap is closable.

We weight the vacuum noise interaction by a "Susceptibility" factor:
Chi(x) = 1 - |t(x)|^k
This represents that saturated vacuum is rigid/incompressible.

Author: Antigravity (Agent) for Tamesis Research
"""

import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion

# --- 1. LEUE MODULES (Simplified for V2) ---

class FastROC:
    """Optimized ROC for 4D Grid"""
    def __init__(self, grid_size, epsilon=0.2):
        self.grid_size = grid_size
        self.dim = len(grid_size)
        
        # Frequencies
        axes_freqs = [np.fft.fftfreq(n) * 2 * np.pi for n in grid_size]
        self.freq_grid = np.meshgrid(*axes_freqs, indexing='ij')
        
    def get_p0_projector_mask(self, v_vec=(1,0,0,0)):
        """Returns the mask for the P0 channel in k-space"""
        # k dot v
        k_dot_v = sum(F * v for F, v in zip(self.freq_grid, v_vec))
        # Mask
        mask = (np.abs(k_dot_v) <= 0.2).astype(float)
        return mask

def run_experiment_v2():
    print("=== TAMESIS-LEUE INTEGRATION: EXPERIMENT 01.1 (Rigid Core) ===")
    print("Hypothesis: Saturated Core (|t|~1) is Entropically Rigid.")
    print("Entropy should reside in the transition shell (Area Law).")
    
    L = 16
    grid_size = (L, L, L, L)
    print(f"Grid: {grid_size}")
    
    roc = FastROC(grid_size)
    p0_mask_k = roc.get_p0_projector_mask()
    
    # Coordinates
    coords = [np.linspace(-1, 1, L) for _ in range(4)]
    T, X, Y, Z = np.meshgrid(*coords, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    
    masses = np.linspace(0.5, 8.0, 15)
    
    res_area = []
    res_p0_entropy = []
    res_vol = []
    
    print(f"{'Mass':<10} | {'Active Entropy':<15} | {'Horizon Area':<15} | {'Core Vol':<15}")
    print("-" * 65)
    
    for M in masses:
        # 1. Source & LMC Field
        # Source is 4D cylinder Gaussian (static mass)
        source = M * np.exp(-R**2 / 0.4)
        t_field = np.tanh(2.0 * source)
        
        # 2. Susceptibility / Rigidity
        # Hypothesis: Information Capacity Chi ~ (1 - |t|^2)
        # This means saturated regions (t=1) have Chi=0 (Frozen)
        chi_field = 1.0 - (t_field**4) # Quartic mostly for sharp transition
        
        # 3. Vacuum Interaction
        # Noise can only exist where Chi > 0
        raw_noise = np.random.randn(*grid_size)
        active_fluctuations = raw_noise * chi_field
        
        # 4. Project to P0 (Neutral Channel)
        # This tells us how much of these surface fluctuations map to "Horizon Modes"
        f_hat = np.fft.fftn(active_fluctuations)
        p0_hat = f_hat * p0_mask_k
        p0_modes = np.fft.ifftn(p0_hat).real
        
        # 5. Calculate Entropy
        # Total energy in P0 channel
        entropy = np.sum(p0_modes**2) / 1000.0
        
        # 6. Geometric Measures
        # Horizon = Region where t > 0.5 (arbitrary definition of 'inside')
        horizon_mask = t_field[L//2] > 0.8
        vol = np.sum(horizon_mask)
        
        if vol > 0:
            eroded = binary_erosion(horizon_mask)
            area = np.sum(horizon_mask ^ eroded)
        else:
            area = 0
            
        res_area.append(area)
        res_vol.append(vol)
        res_p0_entropy.append(entropy)
        
        print(f"{M:<10.2f} | {entropy:<15.4f} | {area:<15.0f} | {vol:<15.0f}")
        
    # Analysis
    areas = np.array(res_area)
    vols = np.array(res_vol)
    ents = np.array(res_p0_entropy)
    
    # Filter valid
    mask = areas > 5
    a = areas[mask]
    v = vols[mask]
    e = ents[mask]
    
    # Normalize
    a_n = a / a.max()
    v_n = v / v.max()
    e_n = e / e.max()
    
    mse_area = np.mean((e_n - a_n)**2)
    mse_vol = np.mean((e_n - v_n)**2)
    
    print("\n--- RESULTS V2 ---")
    print(f"MSE (Entropy vs Area):   {mse_area:.6f}")
    print(f"MSE (Entropy vs Volume): {mse_vol:.6f}")
    
    if mse_area < mse_vol:
        print("\n[SUCCESS] Hypothesis 1.1 CONFIRMED: Rigid Core Model recreates Area Law.")
    else:
        print("\n[FAILURE] Hypothesis 1.1 REFUTED: Still Volume Law.")
        
    # Plot
    plt.figure(figsize=(10,6))
    plt.plot(a_n, 'o-', label='Area')
    plt.plot(v_n, 's--', label='Volume')
    plt.plot(e_n, 'x-', label='Entropy (Calculated)', linewidth=2)
    plt.legend()
    plt.title('V2: Rigid Core Hypothesis')
    plt.grid(True)
    plt.savefig('h1_v2_rigid_core.png')

if __name__ == "__main__":
    run_experiment_v2()
