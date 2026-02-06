from lensing_projector import LensingProjector
from visualizer import GalaxyVisualizer
import matplotlib.pyplot as plt
import numpy as np
import os

FRAMES_DIR = "frames/lensing"
os.makedirs(FRAMES_DIR, exist_ok=True)

def run_animation():
    print("🎥 Rendering Lensing Tomography Scan...")
    
    # 1. Load Data
    viz = GalaxyVisualizer(data_file="data/sdss_sample.csv")
    df = viz.load_and_transform()
    if df is None: return

    # 2. Init Projector (Reuse valid logic)
    min_v = df[['x','y','z']].min().min()
    max_v = df[['x','y','z']].max().max()
    box_size = (max_v - min_v) * 1.1
    
    lp = LensingProjector(df, box_size_mpc=box_size, grid_res=64) # 64^3 for speed
    
    # 3. Compute Density & Potential
    rho_bar = lp._mesh_density()
    phi_N = lp._solve_poisson_fft(rho_bar)
    g_N_mag, _, _, _ = lp._compute_acceleration(phi_N)
    
    # Reactive Correction
    # Compute full grid
    mean_g = np.mean(g_N_mag[g_N_mag > 0])
    effective_a0 = mean_g * 5 
    g_eff_mag = (g_N_mag + np.sqrt(g_N_mag**2 + 4 * g_N_mag * effective_a0)) / 2
    
    # "Phantom Mass" Density = div(g_eff) - rho_bar
    # Approx via enhancement factor eta
    mask = g_N_mag > 0
    eta = np.ones_like(g_N_mag)
    eta[mask] = g_eff_mag[mask] / g_N_mag[mask]
    rho_eff = rho_bar * eta
    
    rho_phantom = rho_eff - rho_bar
    
    # 4. Animate Slice Scanning along Z
    # We will slice indices k from 0 to grid_res
    
    for k in range(lp.grid_res):
        fig, axes = plt.subplots(1, 2, figsize=(16, 8), dpi=80)
        
        # Baryonic Slice
        im1 = axes[0].imshow(np.log1p(rho_bar[:,:,k]), cmap='inferno', vmin=0, vmax=np.log1p(rho_bar.max()))
        axes[0].set_title(f"Baryonic Mass Slice (Z={k})")
        
        # Phantom Slice
        im2 = axes[1].imshow(np.log1p(rho_phantom[:,:,k]), cmap='magma', vmin=0, vmax=np.log1p(rho_phantom.max()))
        axes[1].set_title(f"Phantom Mass Emergence (Z={k})")
        
        plt.suptitle(f"Tomographic Scan: Slice {k}/{lp.grid_res}")
        plt.tight_layout()
        plt.savefig(f"{FRAMES_DIR}/frame_{k:03d}.png")
        plt.close()
        
        print(f"   - Frame {k+1}/{lp.grid_res}")

if __name__ == "__main__":
    run_animation()
