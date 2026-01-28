
"""
simulation_hawking_tunneling_v3.py
----------------------------------
Tamesis-Leue Integration Project
Hypothesis 2 Verification: Tunneling Method (Parikh-Wilczek Style)

Previous spectral attempts failed because projecting white noise just gives white noise shapes.
Correct Approach: Measure the Tunneling Probability T(omega) of a mode trying to escape the LMC barrier.

Theory:
For a Black Hole, tunneling probability is P ~ exp(- Delta_E / T_H).
In Leue Frame: The LMC barrier acts as a damped region for P- modes.
We simulate a 1D wavepacket (simplification of radial mode) hitting the LMC gradient.
We measure Transmission (T) vs Frequency (omega).
If T ~ exp(-c * omega / Gradient), then it behaves thermally.

Author: Antigravity (Agent) for Tamesis Research
"""

import numpy as np
import matplotlib.pyplot as plt

def run_experiment_h2_v3():
    print("=== TAMESIS-LEUE INTEGRATION: EXPERIMENT 02 V3 (Tunneling) ===")
    
    # 1D Simulation of a Radial Mode
    N = 1000
    x = np.linspace(-20, 20, N)
    dx = x[1] - x[0]
    dt = 0.01 * dx
    steps = 4000
    
    # Frequencies to test
    omegas = np.linspace(0.5, 5.0, 10)
    
    # Gradients (Horizon Stiffness)
    gradients = [1.0, 2.0, 4.0, 8.0]
    
    derived_temps = {}
    
    print(f"{'Gradient':<10} | {'Decay Constant (Beta)':<20} | {'Temperature':<15}")
    print("-" * 55)
    
    for g in gradients:
        # Define Barrier (LMC Damping)
        # AMRD Damping profile: Zero inside, High outside? 
        # Actually Horizon blocks P- (outgoing from inside).
        # So we start inside and try to go out.
        # Barrier at x=0.
        # Damping Gamma(x) ~ Sigmoid.
        
        # Leue AMRD: Damping is proportional to volatility/gradient?
        # Let's model the Horizon as a "Viscous Region" for P- modes.
        # Viscosity = g * Sigmoid(x)
        viscosity = g * 0.5 * (np.tanh(2.0*x) + 1) # Barrier step
        
        transmissions = []
        
        for w in omegas:
            # Solve Damped Wave Equation: u_tt + gamma * u_t - c^2 u_xx = 0
            # FDM Scheme
            u_prev = np.zeros(N)
            u = np.zeros(N)
            u_next = np.zeros(N)
            
            # Inject source at left (inside horizon)
            source_pos = N // 4
            
            # Record transmitted energy at right
            e_received = 0
            
            for t_step in range(steps):
                time = t_step * dt
                
                # Source: Oscillating drive
                u[source_pos] = np.sin(w * time) * np.exp(-0.001*(time-50)**2) # Gaussian pulse
                
                # Laplacian
                u_xx = (np.roll(u, -1) - 2*u + np.roll(u, 1)) / (dx**2)
                
                # Damping term: gamma * u_t
                # Central diff for u_t: (u_next - u_prev) / 2dt
                # Equation: (u_next - 2u + u_prev)/dt^2 + gamma*(u_next - u_prev)/2dt = u_xx
                # Solve for u_next
                
                gamma = viscosity
                
                # Coeffs
                alpha = gamma * dt / 2
                u_next = (2*u + u_xx*dt**2 - u_prev*(1-alpha)) / (1 + alpha)
                
                # Update
                u_prev = u.copy()
                u = u_next.copy()
                
                # Measure at detector (far right)
                e_received += u[N * 3 // 4]**2
            
            transmissions.append(e_received)
        
        transmissions = np.array(transmissions)
        # Avoid log(0)
        transmissions = np.maximum(transmissions, 1e-20)
        
        # Fit T ~ exp(-beta * omega)
        # log(T) ~ -beta * omega
        log_t = np.log(transmissions)
        
        slope, intercept = np.polyfit(omegas, log_t, 1)
        # Slope = -beta. Temperature ~ 1/beta ? 
        # Actually in Hawking: P ~ exp(-2pi w / g). So slope ~ -1/g.
        
        beta = -slope
        temp = 1.0 / beta if beta > 0 else 0
        
        derived_temps[g] = temp
        print(f"{g:<10.2f} | {beta:<20.4f} | {temp:<15.4f}")
        
    # Correlation Check
    gs = np.array(list(derived_temps.keys()))
    Ts = np.array(list(derived_temps.values()))
    
    corr = np.corrcoef(gs, Ts)[0,1]
    
    print("\n--- RESULTS V3 ---")
    print(f"Correlation (Gradient vs Temperature): {corr:.4f}")
    
    plt.figure()
    plt.plot(gs, Ts, 'o-')
    plt.xlabel('Horizon Gradient (g)')
    plt.ylabel('Effective Temperature (T)')
    plt.title('H2 V3: Tunneling Temperature')
    plt.grid()
    plt.savefig('h2_v3_tunneling.png')
    
    if corr > 0.95:
        print("[SUCCESS] H2 CONFIRMED: Tunneling Temperature scales with Gradient.")
    else:
        print("[FAILURE] H2 Refuted.")

if __name__ == "__main__":
    run_experiment_h2_v3()
