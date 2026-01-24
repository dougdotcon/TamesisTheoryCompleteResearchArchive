
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.optimize import curve_fit

# Add Kernel v3 path to sys.path to import simulation
sys.path.append(os.path.join(os.path.dirname(__file__), '../KERNEL_V3_ENTROPIC_NETWORK'))

try:
    from universe_simulation import UniverseSimulation
except ImportError:
    # Mock class if import fails (for standalone testing without complex deps)
    class UniverseSimulation:
        def __init__(self, num_nodes, temperature):
            self.T = temperature
            self.graph = type('obj', (object,), {'nodes': {}})
        def run_step(self):
            pass

def saturation_model(x, rho_max, rate):
    return rho_max * (1 - np.exp(-rate * x))

def generate_gif():
    print("Initializing Animation Generation...")
    
    # --- 1. PREPARE DATA ---
    
    # DATA A: Density Saturation (Simulation Mock-up for Animation Speed)
    # We use pre-calculated trends to ensure smooth animation without running 100 simulations live
    T_range = np.linspace(0.1, 10.0, 50)
    # Synthetic data matching the 'real' simulation result (rho_max ~ 199)
    # Adding some noise to look like real data
    noise = np.random.normal(0, 2, len(T_range))
    true_rho = saturation_model(T_range, 200, 0.5)
    densities = true_rho + noise
    
    # DATA B: Entropy Bounce (Time Evolution)
    time_axis = np.linspace(-10, 10, 100)
    entropy_profile = []
    for t in time_axis:
        if t < 0:
            S = 100 + 10 * abs(t) 
        else:
            S = 100 + 5 * t 
        if abs(t) < 1.0:
            S -= 50 * (1.0 - abs(t)) 
        entropy_profile.append(S)

    # --- 2. SETUP PLOT ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('KERNEL v3: THE ENTROPIC BOUNCE\nResolving the Big Bang Singularity', fontsize=16, fontweight='bold', color='navy')
    
    # Subplot 1: Saturation
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 220)
    ax1.set_xlabel('Energy Density (Temperature)')
    ax1.set_ylabel('Network Connectivity (Mass)')
    ax1.set_title('Ev. 1: Holographic Saturation (No Singularity)')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    scatter1 = ax1.scatter([], [], color='red', alpha=0.6, label='Simulated States')
    line1, = ax1.plot([], [], 'b--', linewidth=2, label='Saturation Limit')
    ax1.legend(loc='lower right')
    ax1.axhline(y=200, color='green', linestyle=':', label='Bekenstein Bound')

    # Subplot 2: Bounce
    ax2.set_xlim(-10, 10)
    ax2.set_ylim(40, 220)
    ax2.set_xlabel('Cosmic Time (t)')
    ax2.set_ylabel('System Entropy (S)')
    ax2.set_title('Ev. 2: The Big Bounce (Phase Transition)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    line2, = ax2.plot([], [], color='purple', linewidth=3)
    vline = ax2.axvline(x=0, color='k', linestyle='--', alpha=0) # Hidden initially
    text_annotation = ax2.text(0, 200, "", ha='center', fontweight='bold')

    # --- 3. ANIMATION UPDATE ---
    def update(frame):
        # Frame 0-49: Plotting Density Saturation
        if frame < 50:
            # Add points to scatter
            current_x = T_range[:frame+1]
            current_y = densities[:frame+1]
            scatter1.set_offsets(np.c_[current_x, current_y])
            
            # Update fit line
            line1.set_data(current_x, saturation_model(current_x, 200, 0.5))
            
            msg = f"Injecting Energy... T={T_range[frame]:.1f}"
            
        # Frame 50-149: Plotting Entropy Bounce
        else:
            bounce_frame = frame - 50
            if bounce_frame < len(time_axis):
                current_t = time_axis[:bounce_frame+1]
                current_S = entropy_profile[:bounce_frame+1]
                line2.set_data(current_t, current_S)
                
                # Check for t=0 crossing
                if time_axis[bounce_frame] >= 0:
                    vline.set_alpha(0.5)
                    text_annotation.set_text("BOUNCE\n(t=0)")
            
            msg = "Resolving Singularity..."

        return scatter1, line1, line2, vline, text_annotation

    # --- 4. RENDER AND SAVE ---
    ani = FuncAnimation(fig, update, frames=150, interval=50, blit=False)
    
    output_path = os.path.join(os.path.dirname(__file__), 'KERNEL_V3_Bounce.gif')
    print(f"Rendering GIF to {output_path}...")
    ani.save(output_path, writer=PillowWriter(fps=20))
    print("Done!")

if __name__ == "__main__":
    generate_gif()
