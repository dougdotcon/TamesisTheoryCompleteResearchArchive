"""
TEST: KERNEL v3 ONTOLOGY
Verifies the basic data structures.
"""

from ontology import EntropicNode, CausalGraph
import numpy as np

def test_ontology():
    print("--- 1. INITIALIZING GRAPH ---")
    universe = CausalGraph()
    
    # Create a small cluster (The "Big Bang" Seed)
    for i in range(5):
        n = EntropicNode(node_id=f"N{i}")
        universe.add_node(n)
        print(f"Created: {n}")

    print("\n--- 2. CONNECTING NODES (Entanglement) ---")
    # N0 connects to everyone (Hub)
    universe.add_edge("N0", "N1")
    universe.add_edge("N0", "N2")
    universe.add_edge("N0", "N3")
    universe.add_edge("N4", "N3") # Chain
    
    print(universe)
    
    print("\n--- 3. CHECKING PROPERTIES ---")
    densities = universe.get_network_density()
    print("Node Degrees (Mass Proxy):")
    for nid, deg in densities.items():
        print(f"  {nid}: {deg}")
        
    print("\n--- 4. UPDATING STATE ---")
    n0 = universe.nodes["N0"]
    old_S = n0.entropy
    # Collapse to a pure state [1, 0] -> Entropy should go to 0
    n0.update_state(np.array([1, 0]))
    new_S = n0.entropy
    
    print(f"Node N0 Entropy Update: {old_S:.4f} -> {new_S:.4f}")
    
    if new_S < 0.001:
        print(">> SUCCESS: Entropy calculation works correctly for pure states.")
    else:
        print(">> FAILURE: Entropy calculation incorrect.")

if __name__ == "__main__":
    test_ontology()
