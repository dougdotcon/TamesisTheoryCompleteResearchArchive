from early_universe import EarlyUniverseCollapse
import matplotlib.pyplot as plt
import numpy as np
import os

FRAMES_DIR = "frames/early_universe"
os.makedirs(FRAMES_DIR, exist_ok=True)

def run_animation():
    print("🎥 Rendering Early Universe Collapse...")
    
    # 1. Simulate
    sim = EarlyUniverseCollapse(mass_cloud_solar=1e10, z_start=15.0)
    t_sec, sol_cdm, sol_reactive = sim.simulate_collapse(R_initial_kpc=50.0)
    
    # Process Data
    t_cdm_gyr = sol_cdm.t / sim.GYR_S
    t_reactive_gyr = sol_reactive.t / sim.GYR_S
    
    R_cdm_kpc = sol_cdm.y[0] / (sim.MPC_M / 1e6 * 1000)
    R_reactive_kpc = sol_reactive.y[0] / (sim.MPC_M / 1e6 * 1000)
    
    # Common Time Axis for Animation
    max_t = max(t_cdm_gyr[-1], t_reactive_gyr[-1])
    frames = 100
    t_anim = np.linspace(t_cdm_gyr[0], max_t, frames)
    
    # Interpolate R values onto common t
    R_cdm_interp = np.interp(t_anim, t_cdm_gyr, R_cdm_kpc)
    R_reactive_interp = np.interp(t_anim, t_reactive_gyr, R_reactive_kpc)
    
    # Get Zs
    zs = sim.interp_z(t_anim)

    # 2. Render Frames via "Reveal"
    for i in range(frames):
        fig, ax1 = plt.subplots(figsize=(10, 6), dpi=80)
        
        # Plot up to current index
        current_t = t_anim[:i+1]
        
        ax1.plot(current_t, R_cdm_interp[:i+1], 'k--', linewidth=2, label='Standard CDM')
        ax1.plot(current_t, R_reactive_interp[:i+1], 'tab:orange', linewidth=2, label='Reactive Gravity')
        
        ax1.set_xlim(t_anim[0], t_anim[-1])
        ax1.set_ylim(0, 55) # Start at 50
        ax1.set_xlabel('Cosmic Time (Gyr)')
        ax1.set_ylabel('Cloud Radius (kpc)')
        ax1.set_title(f"Primordial Galaxy Formation (z={zs[i]:.1f})")
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # Visual Marker for collapse
        if R_reactive_interp[i] < 1.0:
             ax1.text(current_t[-1], 5, "Reactive Collapse!", color='orange', fontweight='bold')
             
        # Add Z axis on top
        ax2 = ax1.twiny()
        ax2.set_xlim(ax1.get_xlim())
        tick_locs = np.linspace(t_anim[0], t_anim[-1], 6)
        tick_zs = sim.interp_z(tick_locs)
        ax2.set_xticks(tick_locs)
        ax2.set_xticklabels([f"z={z:.1f}" for z in tick_zs])
        
        plt.tight_layout()
        plt.savefig(f"{FRAMES_DIR}/frame_{i:03d}.png")
        plt.close()

if __name__ == "__main__":
    run_animation()
