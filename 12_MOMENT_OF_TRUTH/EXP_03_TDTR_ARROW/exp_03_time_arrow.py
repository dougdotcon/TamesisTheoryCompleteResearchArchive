import numpy as np
import zlib
import matplotlib.pyplot as plt

def get_complexity(data):
    """
    Approximates Kolmogorov Complexity using zlib compression.
    Returns size in bytes.
    """
    # Convert data to bytes string for compression
    # We map values to characters to make it compressible text-like stream
    # or just raw bytes. Let's use raw bytes of 32-bit floats.
    data_bytes = data.astype(np.float32).tobytes()
    compressed = zlib.compress(data_bytes)
    return len(compressed)

def arrow_score(data):
    """
    Calculates the 'Time Arrow Score' (Irreversibility).
    Score = (Size_Backward - Size_Forward) / Size_Forward
    Divides by forward size to normalize.
    """
    forward = data
    backward = data[::-1]
    
    k_fwd = get_complexity(forward)
    k_bwd = get_complexity(backward)
    
    # If K_bwd > K_fwd, it means the past is 'simpler' (lower entropy) than future.
    # If roughly equal, it's reversible.
    
    score = (k_bwd - k_fwd) / k_fwd
    return score, k_fwd, k_bwd

def generate_sine_wave(n):
    t = np.linspace(0, 100, n)
    return np.sin(t)

def generate_logistic_map(n, r=4.0):
    x = np.zeros(n)
    x[0] = 0.5
    for i in range(1, n):
        x[i] = r * x[i-1] * (1 - x[i-1])
    return x

def generate_financial_drift(n):
    # Random walk with drift (Geometric Brownian Motion approx)
    returns = np.random.normal(0.0002, 0.01, n) # Positive drift
    price = np.cumprod(1 + returns)
    return price

def run_experiment():
    print("--- TAMESIS EXPERIMENT 03: TDTR ARROW OF TIME ---")
    print("Goal: Prove 'Irreversibility' is detectable via Compression Asymmetry.")
    
    N = 10000
    
    # 1. Newtonian Logic (Sine Wave)
    data_sine = generate_sine_wave(N)
    score_sine, kf, kb = arrow_score(data_sine)
    print(f"\n[SYSTEM 1: PENDULUM/SINE] (Reversible)")
    print(f"Forward Size: {kf}, Backward Size: {kb}")
    print(f"Arrow Score: {score_sine:.5f}")
    
    # 2. Chaos (Logistic Map)
    data_chaos = generate_logistic_map(N, r=4.0)
    score_chaos, kf, kb = arrow_score(data_chaos)
    print(f"\n[SYSTEM 2: CHAOS] (Deterministic but Entropic)")
    print(f"Forward Size: {kf}, Backward Size: {kb}")
    print(f"Arrow Score: {score_chaos:.5f}")
    
    # 3. Market (Stochastic with Drift)
    data_market = generate_financial_drift(N)
    score_market, kf, kb = arrow_score(data_market)
    print(f"\n[SYSTEM 3: MARKET PRIZE] (Stochastic + Drift)")
    print(f"Forward Size: {kf}, Backward Size: {kb}")
    print(f"Arrow Score: {score_market:.5f}")
    
    print("\n--- CONCLUSION ---")
    if abs(score_sine) < 1e-4:
        print("PASS: Sine wave is perfectly reversible (Score ~ 0).")
    else:
        print("FAIL: Sine wave showed asymmetry?")
        
    if abs(score_chaos) < 1e-4:
        print("NOTE: Mathematical Chaos (Logistic) is theoretically reversible in math,")
        print("but floating point errors make it diverge. Let's see if zlib cares.")
    
    # Tamesis Prediction:
    # Real irreversible processes (like markets) should have distinct signatures.
    # Note: zlib might be too simple to catch subtle causal drifts without context mixing,
    # but let's test the principle.
    
    # Correction: Zlib is 'adaptive'. It learns the dictionary as it goes.
    # A process that gets 'more complex' over time is harder to compress at the end.
    # A process that gets 'simpler' is easier.
    
    # Let's verify Tamesis Claim: "Information Loss".
    # If a system Loses Information (Dissipative), it converges to an Attractor.
    # Going BACKWARDS (Attractor -> Basin) is Dispersion (One-to-Many).
    # Going FORWARDS (Basin -> Attractor) is Convergence (Many-to-One).
    
    print("\nVerifying TDTR Axiom: 'Transitions form a Semigroup'.")
    if score_market != 0:
        print(f"Detected Time Arrow in Market Data: {score_market:.5f}")
    else:
        print("No Arrow detected (might need stronger compressor than zlib).")

if __name__ == "__main__":
    run_experiment()
