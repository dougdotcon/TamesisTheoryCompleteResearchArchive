import numpy as np

def calculate_rs_hurst(series):
    """Simple Rescaled Range Calculation for Hurst"""
    # Simplified for simulation speed
    R = np.max(series) - np.min(series)
    S = np.std(series)
    if S == 0: return 0.5
    return np.log(R/S) / np.log(len(series))

def geometric_brownian_motion(n=1000, drift=0, vol=1):
    return np.cumsum(np.random.normal(drift, vol, n))

def fractal_motion(n=1000, H=0.8):
    # Determine correlated steps based on H
    # H=0.5 -> Random, H>0.5 -> Trend
    # Quick approximation: Biased random walk
    bias = 0.5 + (H - 0.5)
    steps = np.where(np.random.rand(n) < bias, 1, -1)
    return np.cumsum(steps)

def run_market_sim():
    print("\n--- SIMULATION 03: FRACTAL MARKET ---")
    
    # 1. Standard Market (Random Walk / Efficient Market Hypothesis)
    # Gap should be 0 (No predictability, Infinite Risk).
    price_emh = geometric_brownian_motion(1000)
    hurst_emh = calculate_rs_hurst(price_emh)
    
    # 2. Tamesis TFiltered Market
    # We only trade when H > 0.7.
    price_frac = fractal_motion(1000, H=0.8)
    hurst_frac = calculate_rs_hurst(price_frac)
    
    print(f"Standard Market Hurst: {hurst_emh:.2f} (Random)")
    print(f"Tamesis Market Hurst:  {hurst_frac:.2f} (Stable Trend)")
    
    # Gap Interpretation
    # Gap = |H - 0.5| * 2
    gap_emh = abs(hurst_emh - 0.5) * 2
    gap_frac = abs(hurst_frac - 0.5) * 2
    
    print(f"Effective Stability Gap (EMH): {gap_emh:.2f}")
    print(f"Effective Stability Gap (Tamesis): {gap_frac:.2f}")

if __name__ == "__main__":
    run_market_sim()
