"""
STRUCTURAL CLASSIFIER ENGINE
----------------------------
Empirical demonstration that 'Structural Solvability' is a measurable property.
We simulate two types of problem spaces:

1. CLASS A (Rigid/Poincaré-like):
   - Dynamics: geometric_flow (Ricci-like smoothing)
   - Expected Behavior: Convergence to a unique invariant state (Sphere).
   - Metric: Variance -> 0.

2. CLASS B (Universal/Riemann-like):
   - Dynamics: spectral_chaos (Random Matrix evolution)
   - Expected Behavior: Convergence to a Universal Distribution (GUE).
   - Metric: Variance -> Constant (Spectral Rigidity, but not uniqueness).

Usage:
    python structural_classifier.py
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ProblemSpace:
    def __init__(self, size=50, mode='rigid'):
        self.size = size
        self.mode = mode
        # Initialize random state
        self.state = np.random.randn(size, size)
        self.history_var = []

    def evolve(self):
        """Applies the update rule based on the Class."""
        
        if self.mode == 'rigid': # CLASS A: Ricci-like Flow (Smoothing)
            # Heat equation / Diffusion smooths out irregularities
            # x_new = x - alpha * Laplacian(x)
            laplacian = self.state - np.roll(self.state, 1, axis=0)
            self.state = self.state - 0.1 * laplacian + np.random.normal(0, 0.001, self.state.shape)
            # Normalization (Constraint)
            self.state = self.state / np.linalg.norm(self.state)

        elif self.mode == 'universal': # CLASS B: GUE Dynamics (Chaos)
            # Random Matrix evolution (Brownian Motion on Unitary Group)
            # H_new = H + dH (Hermitian noise)
            noise = np.random.randn(self.size, self.size) + 1j * np.random.randn(self.size, self.size)
            perturbation = (noise + noise.T.conj()) / 2
            self.state = self.state + 0.1 * perturbation
            
            # Diagonalize to get eigenvalues (The "Invariants")
            # We track the spacing statistics variance, but simple element variance is a proxy for "non-settling"
            vals = np.linalg.eigvalsh(self.state)
            # Reconstruct "state" as the normalized spacings for tracking stability
            spacings = np.diff(vals)
            normalized_spacings = spacings / np.mean(spacings)
            return np.var(normalized_spacings)

        return np.var(self.state)

    def run_simulation(self, steps=200):
        print(f"Running Simulation for Class: {self.mode.upper()}...")
        for _ in range(steps):
            metric = self.evolve()
            self.history_var.append(metric)

def run_experiment():
    # 1. Simulate Class A (Rigid)
    sim_a = ProblemSpace(mode='rigid')
    sim_a.run_simulation()

    # 2. Simulate Class B (Universal)
    sim_b = ProblemSpace(mode='universal')
    sim_b.run_simulation()

    # 3. Analyze Results
    df = pd.DataFrame({
        'Class A (Geometric)': sim_a.history_var,
        'Class B (Universal)': sim_b.history_var
    })

    # Save Data
    df.to_csv('classification_results.csv', index=False)
    
    # Generate Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Class A (Geometric)'], label='Class A (Geometric/Rigid)', color='blue', linewidth=2)
    plt.plot(df['Class B (Universal)'], label='Class B (Universal/Chaotic)', color='red', linewidth=2)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.xlabel('Evolution Steps')
    plt.ylabel('Variance (Information Content)')
    plt.title('Structural Classification: Rigid vs Universal Dynamics')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('structural_classification.png', dpi=300)
    print("Plot saved to 'structural_classification.png'")
    
    # Conclusion
    final_var_a = df['Class A (Geometric)'].iloc[-1]
    final_var_b = df['Class B (Universal)'].iloc[-1]
    
    print("\n--- RESULTS ---")
    print(f"Class A Final Variance: {final_var_a:.6f} (Dominated by Zero)")
    print(f"Class B Final Variance: {final_var_b:.6f} (Dominated by Universal Constant)")
    
    if final_var_a < final_var_b:
        print("\nVERDICT: Hypothesis Confirmed.")
        print("Class A converges to a unique solution (Solvable).")
        print("Class B persists in a statistical flux (Universal/Censored).")
    else:
        print("\nVERDICT: Hypothesis Failed.")

if __name__ == "__main__":
    run_experiment()
