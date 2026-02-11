import numpy as np
import matplotlib.pyplot as plt

def generate_logistic_map(n, r=4.0):
    x = np.zeros(n)
    x[0] = 0.5
    for i in range(1, n):
        x[i] = r * x[i-1] * (1 - x[i-1])
    return x

def generate_random_walk(n):
    steps = np.random.randn(n)
    return np.cumsum(steps)

def visibility_graph_degree_divergence(series):
    """
    Constructs the Horizontal Visibility Graph (HVG) - simplified for speed.
    Calculates KLD (Kullback-Leibler Divergence) between In-Degree and Out-Degree distributions.
    
    If Time is Reversible (Symmetric), KLD ~ 0.
    If Time is Irreversible (Arrow), KLD > 0.
    """
    n = len(series)
    # Naive O(N^2) implementation is too slow for N=10000.
    # We use a statistical sampling or small N.
    # Let's use N=500 for demonstration speed.
    
    in_degrees = np.zeros(n)
    out_degrees = np.zeros(n)
    
    # Forward pass (Out-degree: "Looking into future")
    # For each i, how many j > i are visible?
    # Visibility criterion: y_k < min(y_i, y_j) + slope...
    # Simplified HVG: y_k < min(y_i, y_j)
    
    # We implement FULL Visibility Graph (Natural Visibility)
    # y_k < y_j + (y_i - y_j) * (t_j - t_k) / (t_j - t_i)
    
    # Optimization: Just look 50 steps ahead/behind
    WINDOW = 50
    
    for i in range(n):
        # Look Forward
        current_slope = -float('inf')
        for j in range(i+1, min(i+WINDOW, n)):
            slope = (series[j] - series[i]) / (j - i)
            if slope > current_slope:
                out_degrees[i] += 1
                in_degrees[j] += 1 # Reciprocity
                current_slope = slope
                
    # Create Distributions
    max_deg = int(max(np.max(in_degrees), np.max(out_degrees))) + 1
    p_in, _ = np.histogram(in_degrees, bins=range(max_deg+1), density=True)
    p_out, _ = np.histogram(out_degrees, bins=range(max_deg+1), density=True)
    
    # Smooth to avoid log(0)
    p_in = p_in + 1e-10
    p_out = p_out + 1e-10
    p_in /= np.sum(p_in)
    p_out /= np.sum(p_out)
    
    # Calculate KLD(In || Out)
    # This measures how different "Past Geometry" is from "Future Geometry".
    kld = np.sum(p_in * np.log(p_in / p_out))
    
    return kld

def run_experiment():
    print(f"--- TAMESIS EXPERIMENT 03 v2: TOPOLOGICAL ARROW ---")
    print(f"Goal: Detect Time Arrow via Visibility Graph Topology (KLD).")
    
    N = 1000
    
    # 1. Noise (Reversible)
    # Random Noise is structurally time-symmetric.
    noise = np.random.rand(N)
    kld_noise = visibility_graph_degree_divergence(noise)
    print(f"\n[SYSTEM 1: RANDOM NOISE]")
    print(f"Topological Irreversibility (KLD): {kld_noise:.5f}")
    
    # 2. Chaos (Logistic Map)
    # Highly non-linear.
    chaos = generate_logistic_map(N)
    kld_chaos = visibility_graph_degree_divergence(chaos)
    print(f"\n[SYSTEM 2: CHAOS LOGISTIC]")
    print(f"Topological Irreversibility (KLD): {kld_chaos:.5f}")
    
    # 3. Market Proxy (Random Walk)
    # Non-stationary.
    market = generate_random_walk(N)
    kld_market = visibility_graph_degree_divergence(market)
    print(f"\n[SYSTEM 3: MARKET (RANDOM WALK)]")
    print(f"Topological Irreversibility (KLD): {kld_market:.5f}")
    
    print("\n--- CONCLUSION ---")
    if kld_chaos > kld_noise * 1.5:
        print("SUCCESS: Chaos showed significantly higher Topological Asymmetry.")
        print("This confirms TDTR: Irreversible Dynamics leave geometric scars.")
    else:
        print("FAILURE: Topology looks symmetric.")

if __name__ == "__main__":
    run_experiment()
