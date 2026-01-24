
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent to path to import engine
sys.path.append(os.path.join(os.getcwd(), 'PROBLEM_01_P_VS_NP'))

from entropic_engine import FiniteCausalGraph

def run_test():
    print("=== TEST: Generating the Critical Instant ===")
    
    # 1. Initialize a low-entropy graph (e.g., disconnected or regular)
    N = 20
    G = FiniteCausalGraph(num_nodes=N)
    
    # Create a simple line graph (low entropy)
    for i in range(N-1):
        G.add_edge(i, i+1)
        
    initial_entropy = G.calculate_spectral_entropy()
    print(f"Initial Entropy (Line Graph): {initial_entropy:.4f}")
    
    # 2. Apply Entropic Pressure
    steps = 500
    beta = 5.0 # High pressure
    print(f"Applying Entropic Pressure for {steps} steps (beta={beta})...")
    
    G.apply_entropic_pressure(steps=steps, beta=beta)
    
    final_entropy = G.calculate_spectral_entropy()
    print(f"Final Entropy: {final_entropy:.4f}")
    
    if final_entropy > initial_entropy:
        print("[OK] SUCCESS: System evolved towards higher entropic structural complexity.")
    else:
        print("❌ FAILURE: Entropy did not increase.")
        
    # 3. Quick Spectrum Check
    L = G.get_laplacian_matrix().toarray()
    evals = np.linalg.eigvalsh(L)
    print("Final Spectrum Sample (First 5):", evals[:5])
    
if __name__ == "__main__":
    run_test()
