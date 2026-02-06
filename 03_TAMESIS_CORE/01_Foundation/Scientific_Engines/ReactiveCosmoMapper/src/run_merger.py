from merger_dynamics import GalaxyMerger
import matplotlib.pyplot as plt
import numpy as np
import os

FRAMES_DIR = "frames/merger"
os.makedirs(FRAMES_DIR, exist_ok=True)

def run_simulation():
    print("💥 Initializing Galaxy Merger Simulation...")
    # Setup for a near miss / merger
    sim = GalaxyMerger(n_stars_per_gal=200, separation_kpc=60, impact_kpc=10, vel_kms=150)
    
    times = []
    dists = []
    
    t_max = 2.0 # Gyr
    dt = 0.01
    
    frame = 0
    saved_frame_count = 0
    
    print(f"   Integrating {sim.N} bodies for {t_max} Gyr...")
    while sim.t < t_max:
        d = sim.step(dt)
        times.append(sim.t)
        dists.append(d)
        
        # Plot Frame
        if frame % 2 == 0: # Save every 2nd step
            plt.figure(figsize=(8, 8), dpi=80)
            plt.style.use('dark_background')
            
            # Gal 1
            p1 = sim.pos[sim.idx_g1]
            plt.scatter(p1[:,0], p1[:,1], c='cyan', s=5, alpha=0.7, label='Galaxy A')
            
            # Gal 2
            p2 = sim.pos[sim.idx_g2]
            plt.scatter(p2[:,0], p2[:,1], c='magenta', s=5, alpha=0.7, label='Galaxy B')
            
            plt.title(f"Reactive Merger Dynamics (t={sim.t:.2f} Gyr)\nSeparation: {d:.1f} kpc")
            plt.xlim(-100, 100)
            plt.ylim(-100, 100)
            plt.legend(loc='upper right')
            
            plt.savefig(f"{FRAMES_DIR}/frame_{saved_frame_count:04d}.png")
            plt.close()
            saved_frame_count += 1
            
        frame += 1
        if frame % 10 == 0:
            print(f"   t={sim.t:.2f} Gyr, Dist={d:.1f} kpc")

    # Plot Separation History
    plt.figure()
    plt.plot(times, dists)
    plt.xlabel("Time (Gyr)")
    plt.ylabel("Core Separation (kpc)")
    plt.title("Merger Trajectory: Dynamical Friction Test")
    plt.savefig("Validation/merger_timescale.png")
    print("✅ Validation plot saved.")

if __name__ == "__main__":
    run_simulation()
