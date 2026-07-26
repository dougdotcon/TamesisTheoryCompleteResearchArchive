"""
TEST: KERNEL v3 EMERGENCE
Validates the emergence of geometry from random noise.
Goal: Does the graph self-organize?
"""

from universe_simulation import UniverseSimulation
import numpy as np

def test_emergence():
    print("--- 1. STARTING BIG BANG (100 Nodes) ---")
    sim = UniverseSimulation(num_nodes=100, temperature=2.0) # High Temp initially
    
    print("\n--- 2. COOLING PHASE (Annealing) ---")
    # Simulate cooling universe: T decreases
    # High T allows exploring configs, Low T locks in structure
    
    temperatures = [2.0, 1.5, 1.0, 0.5, 0.1]
    
    for T in temperatures:
        sim.T = T
        hist = sim.run_simulation(steps=20)
        final = hist[-1]
        print(f"T={T:.1f} | F={final['F']:.2f} | U={final['U']:.2f} | S={final['S']:.2f} | AvgDeg={final['avg_deg']:.2f}")

    print("\n--- 3. CHECKING FINAL GEOMETRY ---")
    # Check curvature distribution
    # If geometry emerged, we expect non-zero clustering in some regions
    graph = sim.graph
    curvatures = []
    degrees = []
    
    for node in graph.nodes.values():
        R = node.compute_local_curvature(graph)
        curvatures.append(R)
        degrees.append(len(node.neighbors))
        
    avg_R = np.mean(curvatures)
    max_deg = np.max(degrees)
    min_deg = np.min(degrees)
    
    print(f"Avg Curvature (Ricci): {avg_R:.4f}")
    print(f"Degree Range: {min_deg} - {max_deg}")
    
    if avg_R > 0.1:
        print(">> RESULT: Clustered/Spherical Geometry Emerged (Gravity).")
    elif avg_R < 0.01 and avg_R > -0.01:
        print(">> RESULT: Flat/Random Geometry.")
    else:
        print(">> RESULT: Complex/Hyperbolic Geometry.")

    # Check for 'Hubs' (Black Holes)
    if max_deg > np.mean(degrees) * 3:
        print(">> ANOMALY: Massive Information Hub detected (Quantum Black Hole candidate).")

if __name__ == "__main__":
    test_emergence()
