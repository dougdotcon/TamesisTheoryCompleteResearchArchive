"""
KERNEL v3: TRACK A2 - SCALING EXPERIMENT
The "Forward vs Inverse" Protocol.

Objective:
Compare the thermodynamic cost of Finding a solution (Inverse) vs Verifying it (Forward).

Metric:
1. Inverse Cost (Finding): Proportional to the inverse square of the Spectral Gap (1/Delta^2).
   Adiabatic Theorem: Time ~ O(1 / min_gap^2).
   Thermodynamic Cost: Dissipation ~ Time.
2. Forward Cost (Verifying): Number of clause checks (Linear/Polynomial).

Hypothesis:
Inverse Cost scales Exponentially (Gap closes exponentially).
Forward Cost scales Polynomially.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from entropic_engine import FiniteCausalGraph
from np_translator import generate_3sat_instance, sat_to_ising, evaluate_satisfiability
import time

def run_scaling_experiment(min_n=3, max_n=10, samples_per_n=5):
    results = []
    
    print(f"--- RUNNING SCALING EXPERIMENT (N={min_n} to {max_n}) ---")
    
    for n in range(min_n, max_n + 1):
        print(f"Processing N={n}...")
        
        for i in range(samples_per_n):
            # 1. Generate Problem
            clauses = generate_3sat_instance(n, clause_ratio=3.0, seed=None)
            J, h = sat_to_ising(n, clauses)
            
            # 2. Setup Engine
            g = FiniteCausalGraph(num_nodes=n)
            g.load_np_problem(J, h)
            
            # 3. INVERSE PROTOCOL (Finding)
            # We approximate the difficulty by the "Spectral Gap" of the final Hamiltonian.
            # In a full adiabatic simulation, we'd check the minimum gap along the path H(s).
            # Here, as a proxy for 'Glassiness' or 'Frustration', we check the gap of the 
            # problem Hamiltonian itself between Ground and First Excited state.
            # If gap is tiny, the ground state is hard to isolate from noise.
            
            # NOTE: For pure classical Ising, ground state finding is the issue.
            # The gaps in the spectrum indicate the "flatness" of the energy landscape.
            
            t0 = time.time()
            evals = g.compute_spectrum(k=2, operator_type='hamiltonian')
            t_inverse = time.time() - t0
            
            gap = evals[1] - evals[0]
            # Avoid division by zero
            if gap < 1e-9: gap = 1e-9
            
            inverse_cost_proxy = 1.0 / (gap**2) # Adiabatic Time Proxy
            
            # 4. FORWARD PROTOCOL (Verifying)
            # Create a random 'solution' (just to measure op cost)
            assignment = np.ones(n) # Dummy
            t0 = time.time()
            _ = evaluate_satisfiability(assignment, clauses)
            t_forward = time.time() - t0
            
            # Count logical operations
            forward_ops = len(clauses) * 3 # 3 checks per clause
            
            results.append({
                'N': n,
                'Gap': gap,
                'Inverse_Cost_Metric': inverse_cost_proxy, # Theoretical
                'Inverse_Compute_Time': t_inverse, # Actual Diagonalization Time (Exp)
                'Forward_Ops': forward_ops,
                'Forward_Time': t_forward
            })
            
    return pd.DataFrame(results)

def plot_results(df):
    # Average per N
    summary = df.groupby('N').mean()
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Plot Inverse Cost (Log Scale)
    color = 'tab:red'
    ax1.set_xlabel('Problem Size (N)')
    ax1.set_ylabel('Inverse Cost (1/Gap^2) [Log Scale]', color=color)
    ax1.plot(summary.index, summary['Inverse_Cost_Metric'], color=color, marker='o', label='Finding (NP)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_yscale('log')
    
    # Plot Forward Cost (Linear Scale)
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Forward Cost (Operations) [Linear]', color=color)
    ax2.plot(summary.index, summary['Forward_Ops'], color=color, marker='x', linestyle='--', label='Verifying (P)')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('P vs NP: Thermodynamic Cost Scaling')
    fig.tight_layout()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # Save
    plt.savefig('results_scaling_a2.png')
    print(">> Saved plot to 'results_scaling_a2.png'")

if __name__ == "__main__":
    df = run_scaling_experiment(min_n=3, max_n=11, samples_per_n=5)
    print("\nResults Sample:")
    print(df.head())
    plot_results(df)
    
    # Save raw data
    df.to_csv('results_scaling_a2.csv')
