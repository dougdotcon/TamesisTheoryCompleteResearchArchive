from early_universe import EarlyUniverseCollapse
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("⏳ Starting JWST Early Universe Simulation...")
    
    # Setup: 10^10 Solar Mass cloud (typical early galaxy) starting at z=15
    sim = EarlyUniverseCollapse(mass_cloud_solar=1e10, z_start=15.0)
    
    # Run comparison
    t_sec, sol_cdm, sol_reactive = sim.simulate_collapse(R_initial_kpc=50.0)
    
    # Convert results for plotting
    # Handle variable length solutions due to early collapse
    t_cdm_gyr = sol_cdm.t / sim.GYR_S
    t_reactive_gyr = sol_reactive.t / sim.GYR_S
    
    R_cdm_kpc = sol_cdm.y[0] / (sim.MPC_M / 1e6 * 1000)
    R_reactive_kpc = sol_reactive.y[0] / (sim.MPC_M / 1e6 * 1000)
    
    # Determine redshifts for axis (using longest time array to define axis range)
    max_t = max(t_cdm_gyr[-1], t_reactive_gyr[-1])
    # Create smooth time array for axis ticks
    axis_t_gyr = np.linspace(t_cdm_gyr[0], max_t, 100)
    zs = sim.interp_z(axis_t_gyr)
    
    # Plot
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Radius curves
    ax1.plot(t_cdm_gyr, R_cdm_kpc, 'k--', linewidth=2, label='Standard CDM (Newton + Halo)')
    ax1.plot(t_reactive_gyr, R_reactive_kpc, 'tab:orange', linewidth=2, label='Reactive Gravity (Dynamic a0)')
    
    ax1.set_xlabel('Cosmic Time (Gyr)')
    ax1.set_ylabel('Cloud Radius (kpc)')
    ax1.set_title('Primordial Collapse: Solving the "Impossible Galaxies" Crisis')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right')
    
    # Add Redshift axis on top
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    
    # Pick some ticks
    tick_locs = np.linspace(axis_t_gyr[0], axis_t_gyr[-1], 6)
    tick_zs = sim.interp_z(tick_locs)
    
    ax2.set_xticks(tick_locs)
    ax2.set_xticklabels([f"z={z:.1f}" for z in tick_zs])
    ax2.set_xlabel('Redshift (z)')
    
    output_file = "Validation/jwst_collapse_comparison.png"
    plt.savefig(output_file)
    print(f"✅ Simulation plot saved to {output_file}")

if __name__ == "__main__":
    main()
