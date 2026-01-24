
import numpy as np
from np_translator import generate_3sat_instance, sat_to_ising, evaluate_satisfiability
from entropic_engine import FiniteCausalGraph

def run_demonstration():
    print("--- TRACK A1: P vs NP TRANSLATION DEMO ---")
    
    # 1. Generate Problem
    N = 10 # Small size for demo
    print(f"\n1. Generating 3-SAT Instance (N={N})...")
    clauses = generate_3sat_instance(N, clause_ratio=3.0, seed=42)
    print(f"Generated {len(clauses)} clauses.")
    print(f"Sample Clause 0: {clauses[0]}")
    
    # 2. Translate to Physics
    print(f"\n2. Translating to Entropic Hamiltonian...")
    J, h = sat_to_ising(N, clauses)
    print("Coupling Matrix J shape:", J.shape)
    print("Non-zero couplings:", np.count_nonzero(J))
    
    # 3. Load into Engine
    print(f"\n3. Loading into Finite Causal Graph...")
    graph = FiniteCausalGraph(num_nodes=N)
    graph.load_np_problem(J, h)
    
    # 4. Verify Structure
    print(f"\n4. Verifying Graph Topology...")
    A = graph.get_adjacency_matrix()
    density = A.getnnz() / (N*N)
    print(f"Graph Connection Density: {density:.2f}")
    
    # 5. Compute 'Cost' (Spectrum)
    # The lowest energy eigenvalue corresponds to the solution cost approximation
    print(f"\n5. Computing Thermodynamic Cost (Spectrum)...")
    evals = graph.compute_spectrum(k=3, operator_type='hamiltonian')
    print(f"Energy Spectrum (Lowest Levels): {evals}")
    
    print("\n>> SUCCESS: Problem mapped to physical substrate.")
    print("   Hypothesis Check: 'Difficult' problems should generate 'gapped' or 'glassy' spectra.")

if __name__ == "__main__":
    run_demonstration()
