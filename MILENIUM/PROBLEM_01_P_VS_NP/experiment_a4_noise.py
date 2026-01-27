"""
KERNEL v3: TRACK A4 - DECISIVE NOISE EXPERIMENT
The "Thermodynamic Censorship" Test.

Objective:
Demonstrate that for any non-zero Temperature T, the fidelity of finding the solution (Ground State)
collapses to random guessing as N increases, because the Spectral Gap Delta becomes < kT.

Physics:
The probability of the system remaining in the Ground State (Solution) vs jumping to the First Excited State (Error)
is governed by the Boltzmann distribution:
    P(Ground) = 1 / Z
    P(Excited) = exp(-Delta / kT) / Z
    Z = 1 + exp(-Delta / kT) + ...

    Fidelity = 1 / (1 + exp(-Delta / kT))

Hypothesis:
Since Delta ~ exp(-alpha * N),
exp(-Delta / kT) approaches exp(0) = 1 as N increases.
Fidelity approaches 0.5 (Random Guessing) exponentially fast.
To maintain Fidelity > 0.99, one must cool T -> 0 exponentially fast (Infinite Energy Cost).
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from entropic_engine import FiniteCausalGraph
from np_translator import generate_3sat_instance, sat_to_ising

def run_noise_experiment(min_n=3, max_n=10, samples_per_n=5):
    # Temperatures to test (in arbitrary energy units, relative to coupling J=1)
    temperatures = [0.01, 0.1, 0.5, 1.0] 
    results = []
    
    print(f"--- RUNNING NOISE EXPERIMENT (N={min_n} to {max_n}) ---")
    
    for n in range(min_n, max_n + 1):
        print(f"Processing N={n}...")
        
        gaps = []
        for i in range(samples_per_n):
            clauses = generate_3sat_instance(n, clause_ratio=3.0)
            J, h = sat_to_ising(n, clauses)
            g = FiniteCausalGraph(num_nodes=n)
            g.load_np_problem(J, h)
            
            # Compute Gap
            evals = g.compute_spectrum(k=2, operator_type='hamiltonian')
            gap = evals[1] - evals[0]
            if gap < 1e-9: gap = 1e-9
            gaps.append(gap)
            
        avg_gap = np.mean(gaps)
        
        # Calculate Fidelity for each Temperature
        row = {'N': n, 'Avg_Gap': avg_gap}
        for T in temperatures:
            # Boltzmann Factor for error transition
            # Error comes from thermal excitation overcoming the gap
            # Fidelity = Prob(Ground) in a 2-level approximation
            fidelity = 1.0 / (1.0 + np.exp(-avg_gap / T))
            row[f'Fidelity_T={T}'] = fidelity
            
        results.append(row)
            
    return pd.DataFrame(results)

def plot_noise_results(df):
    plt.figure(figsize=(10, 6))
    
    temperatures = [col.split('=')[1] for col in df.columns if 'Fidelity' in col]
    
    for T in temperatures:
        plt.plot(df['N'], df[f'Fidelity_T={T}'], marker='o', label=f'Temp T={T}')
        
    plt.axhline(y=0.5, color='gray', linestyle='--', label='Random Guessing (0.5)')
    plt.axhline(y=0.9, color='green', linestyle=':', label='Reliable Threshold (0.9)')
    
    plt.xlabel('Problem Size (N)')
    plt.ylabel('Computation Fidelity (P_ground)')
    plt.title('Thermodynamic Censorship: Noise Destroys Computation')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('results_noise_a4.png')
    print(">> Saved plot to 'results_noise_a4.png'")

if __name__ == "__main__":
    df = run_noise_experiment(min_n=3, max_n=12, samples_per_n=5)
    print("\nResults Sample:")
    print(df.round(4))
    plot_noise_results(df)
    df.to_csv('results_noise_a4.csv')
