
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

class InterferenceSiimulator:
    def __init__(self):
        print("Initializing Tamesis Collapse Simulator...")
        # Fundamental Parameters
        self.M_c = 2.2e-14 # kg (According to Final Synthesis)
        self.width = 1e-3   # Relative width of transition
        
    def standard_decoherence(self, M_array):
        """
        Visibility decay due to environmental scattering (e.g., gas collisions).
        V ~ exp(-k * M^2)
        """
        # Tuning k to match M_c rough scale for visual comparison
        k = 1.0 / (2 * self.M_c**2) 
        return np.exp(-k * (M_array**2) * 0.1) # Slower decay for contrast

    def csl_model(self, M_array):
        """
        Continuous Spontaneous Localization (CSL).
        V ~ exp(-lambda * M^2 * T)
        Smooth decay, steeper than environmental.
        """
        k = 1.0 / (self.M_c**2)
        return np.exp(-k * (M_array**2))

    def tamesis_collapse(self, M_array):
        """
        Topological Collapse: Sigmoid/Step Function.
        V = 1 / (1 + exp((M - M_c) / width))
        """
        # Sharp transition
        delta = self.M_c * self.width
        # Logistic function approximating Heaviside step
        argument = (M_array - self.M_c) / delta
        # Clip argument to avoid overflow
        argument = np.clip(argument, -100, 100)
        return 1.0 / (1.0 + np.exp(argument))

    def animate_collapse(self):
        print("Generating Collapse Animation...")
        
        # Mass range
        M = np.logspace(-15, -13, 500)
        V_env = self.standard_decoherence(M)
        V_csl = self.csl_model(M)
        V_tam = self.tamesis_collapse(M)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xscale('log')
        
        # Static Background
        ax.semilogx(M, V_env, 'b--', label='Environmental Decoherence', alpha=0.3)
        ax.semilogx(M, V_csl, 'g--', label='CSL (Continuous)', alpha=0.3)
        ax.semilogx(M, V_tam, 'r-', linewidth=2, label='Tamesis Topological Jump', alpha=0.5)
        ax.axvline(self.M_c, color='k', linestyle=':', alpha=0.5)
        
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel('Particle Mass (kg)')
        ax.set_ylabel('Interference Visibility V')
        ax.set_title('The Killer Prediction: Crossing the Critical Mass')
        ax.grid(True, which="both", ls="-", alpha=0.2)
        
        # Moving Point
        point, = ax.plot([], [], 'ro', markersize=10, markeredgecolor='black', label='Test Particle')
        status_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, fontweight='bold')
        
        # Animation frames: Logspace movement
        frames = np.logspace(np.log10(1.5e-15), np.log10(1e-13), 60)
        
        def update(mass_val):
            # Calculate V for this mass
            v_val = self.tamesis_collapse(np.array([mass_val]))[0]
            point.set_data([mass_val], [v_val])
            
            # Update Text
            if mass_val < self.M_c:
                state = "QUANTUM SUPERPOSITION"
                color = "green"
            else:
                state = "CLASSICAL REALITY"
                color = "red"
                
            status_text.set_text(f"Mass: {mass_val:.2e} kg\nState: {state}")
            status_text.set_color(color)
            
            return point, status_text
            
        anim = FuncAnimation(fig, update, frames=frames, interval=80)
        ax.legend(loc='lower left')
        
        output = 'collapse_animation.gif'
        try:
            anim.save(output, writer=PillowWriter(fps=15))
            print(f"[SUCCESS] Animation saved to {output}")
        except Exception as e:
            print(f"[WARNING] Could not save animation: {e}")

    def run_simulation(self):
        self.animate_collapse()

if __name__ == "__main__":
    sim = InterferenceSiimulator()
    sim.run_simulation()
