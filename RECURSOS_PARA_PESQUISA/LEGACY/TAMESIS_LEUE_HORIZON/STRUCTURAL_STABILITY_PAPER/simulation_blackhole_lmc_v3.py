
"""
simulation_blackhole_lmc_v3.py
------------------------------
Tamesis-Leue Integration Project
Hypothesis 1.2 Verification: Rigid Core with Growing Radius

Refinement: V2 used a fixed-width Gaussian, so increasing Mass just sharpened the gradient,
reducing the net active volume (thinning the shell).
Correct approach: Vary the Radius of the source, equivalent to adding mass to a BH.
Metric: Check if Active Entropy follows Area (R^2) or Volume (R^3).

Author: Antigravity (Agent) for Tamesis Research
"""

import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion

class FastROC:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        axes_freqs = [np.fft.fftfreq(n) * 2 * np.pi for n in grid_size]
        self.freq_grid = np.meshgrid(*axes_freqs, indexing='ij')
        
    def get_p0_projector_mask(self, v_vec=(1,0,0,0)):
        k_dot_v = sum(F * v for F, v in zip(self.freq_grid, v_vec))
        mask = (np.abs(k_dot_v) <= 0.2).astype(float)
        return mask

def run_experiment_v3():
    print("=== TAMESIS-LEUE INTEGRATION: EXPERIMENT 01.2 (Growing Radius) ===")
    
    L = 24  # Larger grid for scaling
    grid_size = (L, L, L, L)
    print(f"Grid: {grid_size} ({L}^4 points)")
    
    roc = FastROC(grid_size)
    p0_mask_k = roc.get_p0_projector_mask()
    
    coords = [np.linspace(-10, 10, L) for _ in range(4)] # Physical units
    T, X, Y, Z = np.meshgrid(*coords, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    
    # Radii to test
    radii = np.linspace(1.5, 6.0, 10)
    
    res_area = []
    res_entropy = []
    res_vol = []
    
    print(f"{'Radius':<10} | {'Active Entropy':<15} | {'Horizon Area':<15} | {'Core Vol':<15}")
    print("-" * 65)
    
    for r0 in radii:
        # Source: Top-hat like or Gaussian with width r0
        # To simulate a BH, the interior is saturated (t=1).
        # We use a super-gaussian or tanh to make a blob of radius r0.
        # t(x) = tanh( (R0 - R) * Stiffness )
        # If R < R0, t ~ 1. If R > R0, t ~ -1 (or 0).
        # Leue LMC is usually symmetric around 0, so let's say t goes from 0 to 1.
        
        # Sigmoid profile defining the object
        stiffness = 2.0
        t_field = 0.5 * (1 + np.tanh(stiffness * (r0 - R)))
        
        # Susceptibility: Chi Only active at the transition (R ~ R0)
        # Chi = 1 - (2*t - 1)^4  <-- Zero at t=0 and t=1, max at t=0.5
        # We map t [0, 1] to [-1, 1] for susceptibility logic
        t_norm = 2*t_field - 1
        chi_field = 1.0 - np.abs(t_norm)**6 # Higher power = wider active shell
        
        # Vacuum Interaction
        raw_noise = np.random.randn(*grid_size)
        active_fluctuations = raw_noise * chi_field
        
        # Project P0
        f_hat = np.fft.fftn(active_fluctuations)
        p0_hat = f_hat * p0_mask_k
        p0_modes = np.fft.ifftn(p0_hat).real
        
        # Entropy
        entropy = np.sum(p0_modes**2)
        
        # Geometry
        # Horizon at t=0.5 (R=r0)
        mask = t_field[L//2] > 0.5
        vol_pixels = np.sum(mask)
        
        # Estimate Area from radius r0 (Analytical is 4*pi*r^2)
        # Or count pixels
        area_pixels = 0
        if vol_pixels > 0:
            eroded = binary_erosion(mask)
            area_pixels = np.sum(mask ^ eroded)
            
        res_area.append(area_pixels)
        res_vol.append(vol_pixels)
        res_entropy.append(entropy)
        
        print(f"{r0:<10.2f} | {entropy:<15.4f} | {area_pixels:<15.0f} | {vol_pixels:<15.0f}")

    # Analysis
    # We expect Entropy ~ Area
    # Let's check power law fit: log(E) = a * log(R) + b
    # Area ~ R^2, Vol ~ R^3.
    # If slope is close to 2, it's Area Law. Close to 3, it's Vol.
    
    import math
    
    r_vals = np.array(radii)
    e_vals = np.array(res_entropy)
    
    log_r = np.log(r_vals)
    log_e = np.log(e_vals)
    
    slope, intercept = np.polyfit(log_r, log_e, 1)
    
    print("\n--- RESULTS V3 ---")
    print(f"Entropy Scaling Exponent: {slope:.4f}")
    
    if 1.8 <= slope <= 2.2:
        print("[SUCCESS] Scaling is Quadratic (~R^2). CONFIRMED AREA LAW.")
    elif 2.8 <= slope <= 3.2:
        print("[FAILURE] Scaling is Cubic (~R^3). Volume Law.")
    else:
        print(f"[UNCERTAIN] Scaling is R^{slope:.2f}")

    # Plot
    plt.figure(figsize=(10,6))
    plt.loglog(r_vals, e_vals, 'o-', label=f'Entropy (slope={slope:.2f})')
    plt.loglog(r_vals, r_vals**2 * (e_vals[0]/r_vals[0]**2), '--', label='R^2 (Area)')
    plt.loglog(r_vals, r_vals**3 * (e_vals[0]/r_vals[0]**3), ':', label='R^3 (Volume)')
    plt.xlabel('Radius (R)')
    plt.ylabel('Entropy (S)')
    plt.legend()
    plt.title('V3: Holographic Scaling Verification')
    plt.grid(True, which="both", ls="-")
    plt.savefig('h1_v3_scaling.png')

if __name__ == "__main__":
    run_experiment_v3()
