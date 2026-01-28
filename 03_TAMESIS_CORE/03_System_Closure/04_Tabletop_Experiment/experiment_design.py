
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

class ExperimentDesign:
    def __init__(self):
        print("Initializing Interferometer Visualizer...")
        self.Mc = 2.2e-14 # Critical mass (22 pg)
        self.rho = 2200    # Density of Silica (kg/m^3)
    
    def mass_from_radius(self, R_nm):
        R_m = R_nm * 1e-9
        return (4/3) * np.pi * (R_m**3) * self.rho

    def visibility_signal(self, mass):
        """
        Simulate the visibility V with noise.
        Tamesis model: V = 1 if M < Mc, V = 0 if M > Mc (Idealized)
        Add gaussian noise.
        """
        # Step function
        V_ideal = np.where(mass < self.Mc, 0.95, 0.05)
        
        # Add experimental noise (sigma = 0.05)
        noise = np.random.normal(0, 0.02, size=len(mass))
        return np.clip(V_ideal + noise, 0, 1)

    def animate_experiment(self):
        print("Generating Experiment Animation...")
        
        # Data generation
        R_nm = np.linspace(100, 2000, 60)
        M = self.mass_from_radius(R_nm)
        Rc_nm = (self.Mc / ( (4/3)*np.pi*self.rho ))**(1/3) * 1e9
        V_detected = self.visibility_signal(M)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Static Background setup
        ax.set_xlabel('Nanoparticle Radius (nm)')
        ax.set_ylabel('Interference Visibility')
        ax.set_title('Experimental Readout: Searching for the Cliff')
        ax.axvline(Rc_nm, color='red', linestyle='--', linewidth=2, label=f'Predicted Cutoff ({Rc_nm:.1f} nm)')
        ax.axvspan(100, Rc_nm, alpha=0.1, color='green', label='Quantum Regime')
        ax.axvspan(Rc_nm, 2000, alpha=0.1, color='gray', label='Classical Regime')
        ax.grid(True)
        ax.set_xlim(0, 2100)
        ax.set_ylim(-0.1, 1.1)
        ax.legend(loc='lower left')
        
        # Empty container for points
        # We will replot errorbars each frame or just add new ones
        
        def update(frame):
            # Frame is index
            if frame == 0:
                return []
                
            current_R = R_nm[:frame]
            current_V = V_detected[:frame]
            
            # Clear previous points (not background)
            # Actually, reusing ax.errorbar is tricky as it returns a container.
            # We will just plot a NEW errorbar for the LATEST point, and keep old ones?
            # Or just clear the 'data' artists. 
            # Simplest for this scale: Replot all current points. 
            # (To avoid clearing background, we can't use ax.cla())
            
            # A hack: Loop and remove previous errorbar collections if we stored them.
            # But let's just plot the *new* point each frame and let them accumulate. 
            # This is efficient.
            
            r_val = R_nm[frame-1]
            v_val = V_detected[frame-1]
            
            ax.errorbar(r_val, v_val, yerr=0.05, fmt='o', color='black', 
                        ecolor='gray', capsize=3)
            
            return ax.lines
            
        anim = FuncAnimation(fig, update, frames=len(R_nm)+1, interval=100, repeat=False)
        
        output = 'experiment_readout.gif'
        try:
            anim.save(output, writer=PillowWriter(fps=15))
            print(f"[SUCCESS] Animation saved to {output}")
        except Exception as e:
            print(f"[WARNING] Could not save animation: {e}")

    def run_sweep(self):
        self.animate_experiment()

if __name__ == "__main__":
    exp = ExperimentDesign()
    exp.run_sweep()
