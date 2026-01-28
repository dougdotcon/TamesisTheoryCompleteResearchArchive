
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.linalg import eigh
from scipy.stats import kstest

class SpectralSolver:
    def __init__(self, matrix_size=1000):
        self.N = matrix_size
        print(f"Initializing Spectral Solver (Matrix Size: {self.N}x{self.N})...")

    def generate_gue_matrix(self):
        """
        Generate a random Hermitian matrix from the Gaussian Unitary Ensemble.
        H = (A + A.dag) / 2, where A is complex Gaussian random.
        """
        # A = X + iY
        X = np.random.normal(0, 1, (self.N, self.N))
        Y = np.random.normal(0, 1, (self.N, self.N))
        A = X + 1j * Y
        
        # Make Hermitian
        self.H = (A + A.conj().T) / 2
        return self.H

    def compute_spectrum(self):
        """Solve for eigenvalues."""
        print("Computing eigenvalues...")
        self.eigenvalues, _ = eigh(self.H)
        # Sort is guaranteed by eigh, but good updates
        self.eigenvalues = np.sort(self.eigenvalues)
        return self.eigenvalues

    def analyze_level_spacing(self):
        """
        Compute unfolded level spacing statistics.
        s = (E_{i+1} - E_i) / <Delta E>
        """
        # Normalize/Unfold
        # In the bulk of the semicircle law, density is approx constant locally
        # We take the middle 50% to avoid edge effects
        center_start = int(self.N * 0.25)
        center_end = int(self.N * 0.75)
        core_eigs = self.eigenvalues[center_start:center_end]
        
        raw_diffs = np.diff(core_eigs)
        mean_diff = np.mean(raw_diffs)
        self.spacings = raw_diffs / mean_diff
        
        return self.spacings

    def wigner_surmise_gue(self, s):
        """Theoretical PDF for GUE (approx)."""
        # P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)
        return (32 / np.pi**2) * (s**2) * np.exp(-4 * s**2 / np.pi)

    def animate_convergence(self):
        """
        Animate the convergence to Wigner-Dyson distribution by accumulating statistics
        from multiple random matrices.
        """
        print("Generating Spectral Convergence Animation...")
        
        # We will use smaller matrices for speed in animation
        self.N = 300 
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Theoretical Curve
        s_range = np.linspace(0, 3, 100)
        pdf = self.wigner_surmise_gue(s_range)
        ax.plot(s_range, pdf, 'k--', linewidth=2, label='GUE (Wigner-Dyson) Theory')
        
        ax.set_title('Vacuum Level Spacing Statistics (Accumulating Samples)')
        ax.set_xlabel('Normalized Spacing (s)')
        ax.set_ylabel('P(s)')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 0.9)
        
        all_spacings = []
        
        def update(frame):
            # Generate new sample
            self.generate_gue_matrix()
            self.compute_spectrum()
            new_s = self.analyze_level_spacing()
            all_spacings.extend(new_s)
            
            # Clear previous bars avoiding clearing the whole axis (which clears the line)
            # Actually easier to clear and redraw or use return artist
            # We will just clear patches
            for patch in ax.patches:
                patch.remove()
                
            # Plot new histogram
            count, bins, patches = ax.hist(all_spacings, bins=30, density=True, 
                                          alpha=0.6, color='purple', label='Simulated Vacuum Spectrum')
            
            # Update title with sample count
            ax.set_title(f'Vacuum Level Spacing Statistics (Matrices: {frame+1}, Spacings: {len(all_spacings)})')
            
            # Re-add legend only if not present (but clearing patches might remove it?)
            # We plotted the line once, it persists. The legend might need refresh if handles change.
            if frame == 0:
                ax.legend(loc='upper right')
                
            return patches

        # 40 Frames
        anim = FuncAnimation(fig, update, frames=40, interval=100, repeat=False)
        
        output_file = 'spectral_statistics.gif'
        try:
            anim.save(output_file, writer=PillowWriter(fps=10))
            print(f"[SUCCESS] Animation saved to {output_file}")
        except Exception as e:
            print(f"[WARNING] Could not save animation: {e}")

    def run_validation(self):
        """Run the full pipeline."""
        # Run animation instead of single static plot
        self.animate_convergence()

if __name__ == "__main__":
    solver = SpectralSolver(matrix_size=300) # Initial size, but overridden in animation
    solver.run_validation()
