import numpy as np

def simulate_channel(capacity_C, input_rate_R, duration=100):
    """
    Shannon Channel Simulation.
    C: Human Cognitive Capacity (bits/s) ~ Attention Gap
    R: AI Bandwidth (bits/s) ~ Perturbation K
    """
    buffer = 0
    buffer_history = []
    loss = 0
    
    for t in range(duration):
        # Data arrival (Poisson-ish)
        arrival = np.random.poisson(input_rate_R)
        buffer += arrival
        
        # Human processing
        processed = min(buffer, capacity_C)
        buffer -= processed
        
        # Buffer Overflow (Seizure/Panic)
        if buffer > 50: # Biological Panic Threshold
            loss += (buffer - 50)
            buffer = 50 
            
        buffer_history.append(buffer)
        
    return np.mean(buffer_history), loss

def run_ai_sim():
    print("\n--- SIMULATION 04: AI BANDWIDTH SAFETY ---")
    
    # Human Capacity (Cognitive Gap)
    C_human = 40 # bits/s (Standard attention estimate)
    
    # 1. Neuralink Mode (Raw Feed)
    # R = 1000 bits/s
    avg_buf_raw, loss_raw = simulate_channel(C_human, 1000)
    print(f"[UNRESTRICTED] Input: 1000 | Loss: {loss_raw} (Seizure)")
    
    # 2. Tamesis Protocol (Filtered)
    # R = 20 bits/s (< C/2)
    avg_buf_safe, loss_safe = simulate_channel(C_human, 20)
    print(f"[TAMESIS SAFE] Input: 20   | Loss: {loss_safe} (Stable)")
    
    # Analytical Verification
    print(f"Safety Condition: R < C/2 ({C_human/2})")

if __name__ == "__main__":
    run_ai_sim()
