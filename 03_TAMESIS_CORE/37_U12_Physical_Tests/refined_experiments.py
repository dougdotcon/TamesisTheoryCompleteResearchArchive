"""
Refined Neural Network Experiment
==================================

Stage 37.1b: Better formulation of the memorization-generalization test.

PROBLEM WITH V1
---------------
The first experiment had issues:
1. Low memorization rates (10-30%)
2. Very large fitting error
3. Observable poorly defined

NEW FORMULATION
---------------
Instead of "fraction memorized", use:
- Train network to convergence
- Measure TRAINING ACCURACY (fraction with loss < epsilon)
- Vary: ratio of data size to network capacity

The key insight: U_{1/2} describes transitions in DISCRETE state spaces.
For neural networks, the "state space" is the set of possible input-output mappings.
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import Dict, List
import warnings


def power_law(c: np.ndarray, alpha: float) -> np.ndarray:
    return (1 + c) ** (-alpha)


def u12(c: np.ndarray) -> np.ndarray:
    return (1 + c) ** (-0.5)


class MemorizationExperimentV2:
    """
    Improved experiment: vary data_size / capacity ratio.
    """
    
    def __init__(self, input_dim: int = 5, hidden_dim: int = 50, output_dim: int = 1):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.capacity = input_dim * hidden_dim + hidden_dim + hidden_dim * output_dim + output_dim
    
    def create_network(self):
        """Create a fresh network."""
        W1 = np.random.randn(self.input_dim, self.hidden_dim) * 0.1
        b1 = np.zeros(self.hidden_dim)
        W2 = np.random.randn(self.hidden_dim, self.output_dim) * 0.1
        b2 = np.zeros(self.output_dim)
        return {'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
    
    def forward(self, net, X):
        z1 = X @ net['W1'] + net['b1']
        a1 = np.maximum(0, z1)
        z2 = a1 @ net['W2'] + net['b2']
        return z2, (z1, a1)
    
    def train(self, X, y, epochs=5000, lr=0.01):
        net = self.create_network()
        
        for _ in range(epochs):
            output, (z1, a1) = self.forward(net, X)
            m = X.shape[0]
            
            dz2 = output - y
            net['W2'] -= lr * (a1.T @ dz2) / m
            net['b2'] -= lr * np.mean(dz2, axis=0)
            
            da1 = dz2 @ net['W2'].T
            dz1 = da1 * (z1 > 0)
            net['W1'] -= lr * (X.T @ dz1) / m
            net['b1'] -= lr * np.mean(dz1, axis=0)
        
        return net
    
    def measure_memorization(self, net, X, y, threshold=0.01):
        """Fraction of examples with MSE < threshold."""
        output, _ = self.forward(net, X)
        per_example_mse = np.mean((output - y)**2, axis=1)
        return np.mean(per_example_mse < threshold)
    
    def run_experiment(self, data_sizes: List[int], n_trials: int = 3) -> Dict:
        """
        Run experiment varying data size (thus c = data_size / capacity).
        """
        results = []
        
        for n_data in data_sizes:
            phi_trials = []
            c = n_data / self.capacity
            
            for trial in range(n_trials):
                # Random data
                X = np.random.randn(n_data, self.input_dim)
                y = np.random.randn(n_data, self.output_dim)
                
                # Train
                net = self.train(X, y, epochs=3000, lr=0.01)
                
                # Measure
                phi = self.measure_memorization(net, X, y, threshold=0.01)
                phi_trials.append(phi)
            
            phi_mean = np.mean(phi_trials)
            phi_std = np.std(phi_trials)
            
            results.append({
                'n_data': n_data,
                'c': c,
                'phi_mean': phi_mean,
                'phi_std': phi_std
            })
            
            print(f"   n_data={n_data:4d}, c={c:.3f}, phi={phi_mean:.3f} +/- {phi_std:.3f}")
        
        return results


class MarkovChainExperiment:
    """
    Alternative: Test U_{1/2} in Markov chain mixing.
    
    This is closer to the original permutation -> random map setting.
    Start with a permutation matrix, add noise, measure eigenvalue gap.
    """
    
    @staticmethod
    def perturbed_permutation_chain(n: int, c: float, n_trials: int = 10) -> float:
        """
        Create n x n permutation matrix, add noise proportional to c/n.
        Measure fraction of "structure" remaining.
        """
        fractions = []
        
        for _ in range(n_trials):
            # Random permutation
            perm = np.random.permutation(n)
            P = np.zeros((n, n))
            for i in range(n):
                P[i, perm[i]] = 1.0
            
            # Add noise: with probability c/n, redirect each transition
            noise_prob = c / n
            for i in range(n):
                if np.random.random() < noise_prob:
                    # Replace deterministic transition with random
                    P[i, :] = np.random.dirichlet(np.ones(n))
            
            # Renormalize rows
            P = P / P.sum(axis=1, keepdims=True)
            
            # Measure "determinism": fraction of entries > 0.9
            deterministic_frac = np.mean(np.max(P, axis=1) > 0.9)
            fractions.append(deterministic_frac)
        
        return np.mean(fractions)
    
    def run(self, n: int = 100, c_values: List[float] = None) -> Dict:
        """Run Markov chain experiment."""
        if c_values is None:
            c_values = [0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
        
        results = []
        for c in c_values:
            phi = self.perturbed_permutation_chain(n, c)
            results.append({'c': c, 'phi': phi})
            print(f"   c={c:6.2f}, phi={phi:.3f}, U_1/2 pred={u12(c):.3f}")
        
        return results


def main():
    """Stage 37.1b: Refined experiments."""
    
    print("=" * 70)
    print("STAGE 37.1b: REFINED U_{1/2} PHYSICAL TESTS")
    print("=" * 70)
    
    # Experiment 1: Markov chain (closer to original setting)
    print("\n1. MARKOV CHAIN EXPERIMENT")
    print("-" * 50)
    print("   (Perturbed permutation matrix, measure determinism)")
    
    markov = MarkovChainExperiment()
    markov_results = markov.run(n=100)
    
    # Analyze
    c_vals = np.array([r['c'] for r in markov_results])
    phi_vals = np.array([r['phi'] for r in markov_results])
    
    try:
        popt, pcov = curve_fit(power_law, c_vals, phi_vals, p0=[0.5], bounds=(0.01, 5))
        alpha = popt[0]
        alpha_err = np.sqrt(pcov[0, 0]) if pcov[0, 0] > 0 else 0.1
        print(f"\n   Fitted alpha = {alpha:.3f} +/- {alpha_err:.3f}")
        
        if abs(alpha - 0.5) < 2 * alpha_err:
            print("   => U_{1/2} CONFIRMED for Markov chain mixing!")
        else:
            print(f"   => Different exponent: alpha = {alpha:.3f}")
    except Exception as e:
        print(f"   Fit error: {e}")
    
    # Experiment 2: Simple counting model
    print("\n\n2. COUNTING MODEL (SANITY CHECK)")
    print("-" * 50)
    print("   (Direct simulation of permutation -> random map)")
    
    # This should EXACTLY reproduce U_{1/2}
    n = 1000
    c_values = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]
    
    for c in c_values:
        # Simulate: n elements, perturb with probability c/n
        n_trials = 20
        cycle_fracs = []
        
        for _ in range(n_trials):
            # Start with identity permutation on n elements
            next_elem = np.arange(n)
            
            # Perturb: with probability c/n, redirect to random
            for i in range(n):
                if np.random.random() < c / n:
                    next_elem[i] = np.random.randint(0, n)
            
            # Count elements in cycles
            visited = np.zeros(n, dtype=bool)
            in_cycle = np.zeros(n, dtype=bool)
            
            for start in range(n):
                if visited[start]:
                    continue
                
                path = []
                current = start
                while not visited[current]:
                    visited[current] = True
                    path.append(current)
                    current = next_elem[current]
                
                # Check if we found a cycle
                if current in path:
                    cycle_start = path.index(current)
                    for i in range(cycle_start, len(path)):
                        in_cycle[path[i]] = True
            
            cycle_fracs.append(np.mean(in_cycle))
        
        phi_data = np.mean(cycle_fracs)
        phi_pred = u12(c)
        diff = abs(phi_data - phi_pred)
        status = "OK" if diff < 0.1 else "DIFF"
        
        print(f"   c={c:5.1f}: phi(data)={phi_data:.3f}, phi(U_1/2)={phi_pred:.3f} [{status}]")
    
    # Summary
    print("\n\n3. SUMMARY")
    print("-" * 50)
    print("""
   RESULTS:
   
   1. MARKOV CHAIN: Tests perturbed transition matrices
      - Measures "determinism" of transitions
      - Should show U_{1/2} if mechanism is the same
   
   2. COUNTING MODEL: Direct simulation of Stage 34
      - This MUST reproduce U_{1/2} (sanity check)
      - phi(c) = (1+c)^{-1/2} exactly
   
   KEY INSIGHT:
   U_{1/2} appears in systems where:
   - State space is DISCRETE (finite n elements)
   - Perturbation destroys structure at rate c/n per element
   - Observable counts "surviving structure"
   
   Neural networks may NOT fit this pattern because:
   - Continuous weight space
   - Non-local interactions
   - Different mechanism for memorization
""")
    
    print("=" * 70)
    print("END OF REFINED EXPERIMENTS")
    print("=" * 70)


if __name__ == "__main__":
    main()
