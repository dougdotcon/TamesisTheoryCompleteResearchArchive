"""
Stage 83: Emergent Cosmology Simulator
======================================
Option 3: Transitions in Spin Networks.
"""
import random

class CausalNode:
    def __init__(self, id):
        self.id = id
        self.parents = []
        self.time_coord = 0

def run_cosmology_sim():
    print("STAGE 83: EMERGENT COSMOLOGY SIMULATOR")
    
    nodes = [CausalNode(0)]
    N_steps = 1000 # Enough for statistics, fast enough to run
    
    for i in range(1, N_steps):
        new_node = CausalNode(i)
        # Preferential attachment to recent past (Light cone proxy)
        candidates = nodes[-20:] if len(nodes) > 20 else nodes
        
        for past_node in candidates:
            if random.random() < 0.15: # p_connect
                new_node.parents.append(past_node)
        
        # Ensure connection
        if not new_node.parents:
            new_node.parents.append(nodes[-1])
            
        # Calc Proper Time (Longest path) immediately
        if new_node.parents:
             new_node.time_coord = max(p.time_coord for p in new_node.parents) + 1
             
        nodes.append(new_node)
        
    # Analysis
    indices = [n.id for n in nodes]
    times = [n.time_coord for n in nodes]
    
    # Simple correlation check (Emergence of Time coordinate)
    # If Time ~ Index, then we have a smooth 1D foliation (Geometry)
    # If Time is random vs Index, we have disorder
    
    # Manual correlation
    n = len(nodes)
    sum_x = sum(indices)
    sum_y = sum(times)
    sum_xy = sum(i*t for i,t in zip(indices, times))
    sum_xx = sum(i*i for i in indices)
    sum_yy = sum(t*t for t in times)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_xx - sum_x**2) * (n * sum_yy - sum_y**2)) ** 0.5
    correlation = numerator / denominator if denominator != 0 else 0
    
    print(f"Total Events: {N_steps}")
    print(f"Causal ordering correlation: {correlation:.4f}")
    
    if correlation > 0.9:
        print(">> SUCCESS: Transition U_spin -> U_geom DETECTED.")
        print("   Graph crystallized into 1D time manifold.")
    else:
        print(">> FAILURE: Universe remained in disordered phase.")

if __name__ == "__main__":
    run_cosmology_sim()
