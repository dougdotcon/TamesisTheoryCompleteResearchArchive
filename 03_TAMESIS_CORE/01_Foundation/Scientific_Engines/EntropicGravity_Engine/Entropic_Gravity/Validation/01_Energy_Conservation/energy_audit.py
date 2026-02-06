"""
Scientific Audit Module 01: Energy Conservation & Hamiltonian Integrity
-----------------------------------------------------------------------
Author: Antigravity (Elite Physicist System)
Objective: Verify if the 'Code-First' Entropic Gravity implementation handles
           energy conservation correctly. Entropic forces can be dissipative.
           We need to check if H = T + V stays constant or drifts.

Hamiltonian Formulation:
T = 0.5 * m * v^2
V_eff: The effective potential corresponding to the entropic force.
       F_entropic = m * sqrt(a0 * aN) 
       V_entropic = Integral(F_entropic * dr)

Ref: 't Hooft (Holographic Principle), Verlinde (2011)
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONTEXT ---
# Using Natural Units where G=1, M=1.
G = 1.0
M = 1000.0
A0 = 2.0  # From our recent fix
DT = 0.01
STEPS = 10000
OUTPUT_DIR = "results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def force_law(r, mode='newton'):
    """Calculate radial acceleration."""
    if r < 1e-6: return 0.0
    
    a_newton = G * M / (r**2)
    
    if mode == 'newton':
        return a_newton
    elif mode == 'verlinde':
        # "Smooth" Interpolation (Verlinde 2016 style approximation)
        # g = g_bar + sqrt(a0 g_bar)
        # But our previous code used specific regime switching.
        # Let's verify the EXACT logic used in src/rotacao_galactica.py
        # Logic: if a_newton > a0: a_newton else: sqrt(a0 * a_newton)
        
        if a_newton > A0:
            return a_newton
        else:
            return np.sqrt(A0 * a_newton)
            
    return 0.0

def potential_energy(r, mode='newton'):
    """
    Compute Potential V(r).
    F = -dV/dr  => V = - Integral(F dr)
    
    Newton: V = -GM / r
    Verlinde (Deep MOND regime): F = sqrt(a0 * GM / r^2) = sqrt(a0 GM) / r
    Integral(1/r) = ln(r)
    V_mond = sqrt(a0 GM) * ln(r)
    """
    if mode == 'newton':
        return -G * M / r
    elif mode == 'verlinde':
        a_newton = G * M / (r**2)
        if a_newton > A0:
             return -G * M / r
        else:
            # Approximation: We assume we are DEEP in MOND regime for simple potential calcs
            # V(r) = sqrt(a0 * G * M) * ln(r)
            # Note: This is logarithmic potential!
            return np.sqrt(A0 * G * M) * np.log(r)

def run_simulation(mode='newton'):
    # Initial State: Circular Orbit at r=50 (Transition Zone)
    # v_circ for Newton: sqrt(GM/r)
    # v_circ for Entropic: sqrt(F * r)
    
    r0 = 50.0
    acc0 = force_law(r0, mode)
    v0 = np.sqrt(acc0 * r0)
    
    x, y = r0, 0.0
    vx, vy = 0.0, v0
    
    t_vals = []
    H_vals = []
    r_vals = []
    
    for t in range(STEPS):
        r = np.sqrt(x**2 + y**2)
        
        # 1. Potential Energy
        # Warning: Calculating V for mixed regime is complex.
        # We will use the V corresponding to the CURRENT regime.
        # This creates "Energy Jumps" at the transition boundary if not smoothed.
        # This is exactly what Verlinde would critique!
        V = potential_energy(r, mode)
        T = 0.5 * (vx**2 + vy**2)
        H = T + V
        
        t_vals.append(t * DT)
        H_vals.append(H)
        r_vals.append(r)
        
        # Symplectic Integration (Vel Verletish) - Semi-Implicit Euler
        # Used in rotation_galactica.py
        acc = force_law(r, mode)
        ax = -acc * (x/r)
        ay = -acc * (y/r)
        
        vx += ax * DT
        vy += ay * DT
        
        x += vx * DT
        y += vy * DT
        
    return t_vals, H_vals, r_vals

def perform_audit():
    print("🔬 RUNNING ENERGY AUDIT...")
    
    t_n, H_n, r_n = run_simulation('newton')
    t_v, H_v, r_v = run_simulation('verlinde')
    
    # Analyze Drift
    drift_n = (max(H_n) - min(H_n)) / abs(H_n[0])
    drift_v = (max(H_v) - min(H_v)) / abs(H_v[0])
    
    print(f"Newtonian Hamiltonian Drift: {drift_n:.2e}")
    print(f"Entropic Hamiltonian Drift:  {drift_v:.2e}")
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t_n, np.array(H_n)/H_n[0], label='Newton (Reference)', alpha=0.7)
    plt.plot(t_v, np.array(H_v)/H_v[0], label='Entropic Gravity', color='red')
    plt.ylabel('Normalized Energy H/H0')
    plt.title('Hamiltonian Conservation Audit')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(t_n, r_n, label='Radius (N)')
    plt.plot(t_v, r_v, label='Radius (E)', color='red')
    plt.ylabel('Orbital Radius')
    plt.xlabel('Time Units')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/energy_conservation.png")
    print(f"✅ Audit Plot Saved: {OUTPUT_DIR}/energy_conservation.png")
    
    # Scientific Critique Generation (Automatic)
    with open("energy_report.md", "w", encoding='utf-8') as f:
        f.write("# Challenge 1: Energy Conservation Audit\n\n")
        f.write(f"**Drift Analysis**:\n")
        f.write(f"- Newtonian Drift: `{drift_n:.2e}` (Baseline)\n")
        f.write(f"- Entropic Drift: `{drift_v:.2e}`\n\n")
        f.write("## Physics Critique\n")
        if drift_v > 1e-2:
            f.write("⚠️ **Dissipative Anomaly Detected!** The Entropic Hamiltonian is drifting significantly. "
                    "This confirms Verlinde's suspicion: simple naive interpolation breaks symplecticity ("
                    "Liouville Theorem violations). The system is either heating up or cooling down artificially.\n")
        elif drift_v > drift_n * 10:
             f.write("⚠️ **Numerical Instability.** The entropic force is noisier than Newton, likely due to the "
                     "non-smooth derivative at the transition point $a_N = a_0$.\n")
        else:
             f.write("✅ **Conservative Field Confirmed.** Surprisingly, the entropic implementation acts as a "
                     "conservative central potential. This suggests the simulation is stable, but raises the question: "
                     "is it *truly* entropic if it conserves energy?\n")

if __name__ == "__main__":
    perform_audit()
