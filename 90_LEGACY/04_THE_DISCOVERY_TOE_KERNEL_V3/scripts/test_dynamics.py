"""
TEST: KERNEL v3 DYNAMICS
Verifies the Entropic Force and Time Evolution.
"""

from ontology import CausalGraph, EntropicNode
from dynamics import EntropicEngine
import matplotlib.pyplot as plt
import numpy as np

def test_dynamics():
    print("--- 1. SETUP SIMULATION ---")
    universe = CausalGraph()
    engine = EntropicEngine(temperature=1.0)
    
    # Initialize 50 nodes with low entropy (pure states)
    for i in range(50):
        # Create pure state [1, 0] -> S=0 approx
        n = EntropicNode(node_id=f"N{i}")
        n.update_state(np.array([1.0, 0.0])) 
        universe.add_node(n)
        
    print(f"Initial State: {universe}")
    
    print("\n--- 2. RUNNING EVOLUTION (100 Steps) ---")
    history = engine.run_simulation(universe, steps=100)
    
    print(f"Final State: {universe}")
    
    # Check 2nd Law
    s_initial = history[0]['S']
    s_final = history[-1]['S']
    
    print(f"\nEntropy Delta: {s_initial:.4f} -> {s_final:.4f}")
    if s_final >= s_initial:
        print(">> SUCCESS: 2nd Law (dS >= 0) observed.")
    else:
        print(">> WARNING: Entropy decreased. Check Hamiltonians.")
        
    # Check Connectivity Distribution (Emergent Gravity)
    densities = universe.get_network_density()
    degrees = list(densities.values())
    
    print(f"Average Connectivity: {np.mean(degrees):.2f}")
    print(f"Max Connectivity (Black Hole Candidate): {np.max(degrees)}")
    
    # Simple ASCII Plot of Entropy over Time
    print("\n[Entropy History]")
    for h in history[::10]: # every 10 steps
        bars = "#" * int(h['S'] * 2)
        print(f"t={h['t']:3} | {h['S']:6.2f} {bars}")

if __name__ == "__main__":
    test_dynamics()
