import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from p_vs_np_polyphys import ThermodynamicComputer

def run_complexity_test():
    print("🧮 Running P vs NP Physical Complexity Test...")
    print("---------------------------------------------")
    
    computer = ThermodynamicComputer(temperature_k=300) # Room temp
    
    # Test range: 3 to 20 cities (TSP)
    ns = np.arange(3, 16)
    
    energies_np = []
    energies_p = []
    
    print(f"{'N Cities':<10} | {'Ops (NP)':<15} | {'Energy (Joule)':<15} | {'Time (Titan Supercomputer)'}")
    print("-" * 75)
    
    titan_flops = 10**18 # Exaflop (optimistic)
    # Energy to Time: Energy / (Power Limit?)
    # Let's check pure ops time for now
    
    for n in ns:
        e_np = computer.solve_tsp_bruteforce(n)
        e_p = computer.simulate_annealing_cost(n)
        
        energies_np.append(e_np)
        energies_p.append(e_p)
        
        ops_np = computer.solution_space_volume(n)
        time_s = ops_np / titan_flops if ops_np > 0 else 0
        
        print(f"{n:<10} | {ops_np:<15.0e} | {e_np:<15.2e} | {time_s:.2e} s")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(ns, energies_np, 'r-o', label='Exact Solution (NP) - O(N!)')
    plt.plot(ns, energies_p, 'g-s', label='Approx Solution (P) - O(N^3)')
    
    plt.yscale('log')
    plt.xlabel('Problem Size (N Cities)')
    plt.ylabel('Minimum Energy Cost (Joules) [Log Scale]')
    plt.title('The Physical Wall: Why P != NP')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    output_path = "Validation/entropy_cost_growth.png"
    plt.savefig(output_path)
    print(f"\n✅ Complexity plot saved: {output_path}")

if __name__ == "__main__":
    run_complexity_test()
