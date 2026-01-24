"""
KERNEL v3: SINGULARITY RESOLUTION
Looking 'Before the Big Bang' (t < 0).

Hypothesis: 
Standard Physics: Density -> Infinity at t=0 (Singularity).
Tamesis Physics: Density -> Max Capacity (Holographic Saturation).

We simulate the universe going backwards in time (Heating Up) 
to see if it breaks or saturates.
"""

from universe_simulation import UniverseSimulation
import matplotlib.pyplot as plt
import numpy as np

def run_singularity_test():
    print("--- TELESCOPE POINTING AT T=0 ---")
    
    # 1. Initialize Geometric Universe (Now)
    # Start with a cooled, structured universe (T=0.1)
    sim = UniverseSimulation(num_nodes=200, temperature=0.1)
    
    # Run a bit to stabilize geometry
    print("Stabilizing Geometric Era (t > 0)...")
    sim.run_simulation(steps=20)
    
    # 2. REWIND TIME (Heating Up)
    # We increase T to simulate approaching the Big Bang
    # In GR, Density should spike to infinity.
    # In Entropic Network, it should saturate.
    
    print("\nApproaching Big Bang (Rewinding Time)...")
    temperatures = np.linspace(0.1, 5.0, 20) # Heat up to T=5.0 (Planck Era)
    
    max_densities = []
    avg_curvatures = []
    regimes = []
    
    for T in temperatures:
        sim.T = T
        # Evolve "backwards" (High energy updates)
        sim.run_step() 
        
        # Measure Geometry
        degrees = [len(n.neighbors) for n in sim.graph.nodes.values()]
        max_d = np.max(degrees)
        
        # Compute curvature sample
        nodes_sample = list(sim.graph.nodes.values())[:20]
        curvs = [n.compute_local_curvature(sim.graph) for n in nodes_sample]
        avg_R = np.mean(curvs)
        
        max_densities.append(max_d)
        avg_curvatures.append(avg_R)
        
        # Classify Regime
        if avg_R < 0.05:
            regimes.append("Quantum Foam (Disordered)")
        else:
            regimes.append("Spacetime (Ordered)")

    # 3. ANALYZE THE "SINGULARITY"
    peak_density = max(max_densities)
    theoretical_limit = 200 - 1 # Max possible connections (fully connected graph)
    
    print("\n--- RESULTS FROM T=0 ---")
    print(f"Peak Observed Density: {peak_density} connections")
    print(f"Theoretical Limit:     {theoretical_limit} connections")
    print(f"Singularity Status:    {'RESOLVED' if peak_density < theoretical_limit else 'FAILED'}")
    
    if peak_density < theoretical_limit:
        print(">> VERDICT: The universe saturated at finite capacity.")
        print(">> No Infinite Curvature detected.")
    
    # Ascii Plot of Phase Transition
    print("\n[Phase Transition: Geometry -> Quantum Foam]")
    print(f"{'Temp':<6} | {'MaxDeg':<6} | {'Ricci':<6} | {'State'}")
    for i, T in enumerate(temperatures):
        if i % 2 == 0:
            print(f"{T:<6.1f} | {max_densities[i]:<6} | {avg_curvatures[i]:<6.3f} | {regimes[i]}")

if __name__ == "__main__":
    run_singularity_test()
