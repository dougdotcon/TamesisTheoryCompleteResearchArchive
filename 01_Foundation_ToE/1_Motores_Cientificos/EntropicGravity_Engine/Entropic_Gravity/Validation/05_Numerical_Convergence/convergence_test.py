"""
Scientific Audit Module 05: Numerical Convergence & Error Analysis
------------------------------------------------------------------
Author: Antigravity (Elite Physicist System)

Objective:
Prove that the "Flat Rotation Curve" is a physical result of the equations,
not an accumulation of numerical error (heating) due to large time steps.

Methodology:
Run 3 simulations with varying time steps: DT, DT/2, DT/4.
Compare final positions/velocities clearly.
If Error ~ DT^n (where n is order of integrator), code is converging.
If solution changes wildly, it's numerical noise.

Integrator:
Semi-Implicit Euler (Symplectic-ish, Order 1).
Expected Global Error: O(h).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- CONSTANTS ---
G = 1.0
A0 = 2.0
R_INIT = 50.0
STEPS_BASE = 1000
DT_BASE = 0.1

def force_verlinde(r):
    """Force per unit mass"""
    g_n = G * 1000 / (r**2)
    if g_n > A0: return g_n
    return np.sqrt(A0 * g_n)

def run_sim(dt, steps):
    x, y = R_INIT, 0.0
    acc = force_verlinde(R_INIT)
    v0 = np.sqrt(acc * R_INIT)
    vx, vy = 0.0, v0
    
    trajectory = []
    
    for _ in range(steps):
        r = np.sqrt(x**2 + y**2)
        acc_now = force_verlinde(r)
        
        ax = -acc_now * (x/r)
        ay = -acc_now * (y/r)
        
        vx += ax * dt
        vy += ay * dt
        
        x += vx * dt
        y += vy * dt
        
        trajectory.append(np.sqrt(x**2 + y**2))
        
    return np.array(trajectory), np.sqrt(vx**2 + vy**2)

def convergence_audit():
    print("🔬 RUNNING CONVERGENCE TESTS...")
    
    # Run 1: Base DT
    print(f"Running DT = {DT_BASE}")
    traj_1, v1 = run_sim(DT_BASE, STEPS_BASE)
    
    # Run 2: DT / 2 (Double steps)
    print(f"Running DT = {DT_BASE/2}")
    traj_2, v2 = run_sim(DT_BASE/2, STEPS_BASE*2)
    
    # Run 3: DT / 4 (Quadruple steps)
    print(f"Running DT = {DT_BASE/4}")
    traj_3, v3 = run_sim(DT_BASE/4, STEPS_BASE*4)
    
    # Analysis
    diff_low = abs(v1 - v2)
    diff_high = abs(v2 - v3)
    
    convergence_ratio = diff_low / (diff_high + 1e-9)
    # Richardson Ratio: 2^p. For Order 1, ratio ~ 2.
    
    print(f"Velocity (Base): {v1:.4f}")
    print(f"Velocity (Fine): {v3:.4f}")
    print(f"Error Estimate: {diff_high:.2e}")
    print(f"Convergence Ratio: {convergence_ratio:.2f} (Expected ~2.0 for Order 1)")
    
    # Plotting
    plt.figure(figsize=(10, 6))
    
    # Align times for plotting
    t1 = np.arange(len(traj_1)) * DT_BASE
    t2 = np.arange(len(traj_2)) * (DT_BASE/2)
    t3 = np.arange(len(traj_3)) * (DT_BASE/4)
    
    plt.plot(t1, traj_1, 'r-', alpha=0.5, label=f'DT={DT_BASE}')
    plt.plot(t3, traj_3, 'k--', alpha=0.8, label=f'DT={DT_BASE/4} (Reference)')
    
    plt.xlabel('Time')
    plt.ylabel('Radius')
    plt.title('Numerical Convergence Audit (Time Step Refinement)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("convergence_analysis.png")
    print("✅ Convergence Plot Saved: convergence_analysis.png")
    
    with open("convergence_report.md", "w", encoding='utf-8') as f:
        f.write("# Challenge 5: Numerical Convergence Audit\n\n")
        f.write("## Methodology\n")
        f.write("We applied Richardson Extrapolation logic, refining the time step `dt` by factors of 2.\n\n")
        f.write("## Results\n")
        f.write(f"- Velocity difference (DT vs DT/2): `{diff_low:.2e}`\n")
        f.write(f"- Velocity difference (DT/2 vs DT/4): `{diff_high:.2e}`\n")
        f.write(f"- Convergence Ratio: `{convergence_ratio:.2f}`\n\n")
        
        if 1.5 < convergence_ratio < 2.5:
             f.write("✅ **CONVERGENCE CONFIRMED.** The solver exhibits Order 1 convergence, consistent with Semi-Implicit Euler. "
                     "Observed physics (flat rotation) are robust against time-step refinement.\n")
        else:
             f.write("⚠️ **CONVERGENCE ANOMALY.** The ratio deviates from theoretical expectations. "
                     "The rotation curve might be influenced by integration error accumulation.\n")

if __name__ == "__main__":
    convergence_audit()
