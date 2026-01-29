import numpy as np
import matplotlib.pyplot as plt

def simulate_p_np_gap():
    """
    Simulates the spectral gap closure for NP-Complete instances.
    Models the 'Complexity Gap' G(N) between P-class (Large Gap) 
    and NP-class (Exponentially vanishing gap).
    """
    N = np.arange(4, 30, 1)
    
    # 1. P-Class: Smooth landscape, Gap is constant or poly-decay
    # We model it as Delta ~ 1 / poly(N)
    gap_p = 1.0 / (N**0.5)
    
    # 2. NP-Class: Frustrated landscape (Spin Glass / SAT)
    # The gap between solution (ground state) and traps vanishes exponentially
    # Delta ~ exp(-alpha * N)
    alpha = 0.25
    gap_np = 1.0 * np.exp(-alpha * N)
    
    # 3. Readout Time (Resolution Cost)
    # T ~ 1 / Delta^2 (Quantum/Thermal limit)
    time_p = 1.0 / (gap_p**2)
    time_np = 1.0 / (gap_np**2)
    
    plt.figure(figsize=(10, 8))
    plt.style.use('seaborn-v0_8-paper')
    
    # Plot 1: Spectral Gap Decay
    plt.subplot(2, 1, 1)
    plt.plot(N, gap_p, 'g', label='P-Class (Smooth Landscape)', linewidth=2)
    plt.plot(N, gap_np, 'r', label='NP-Class (Shattered Landscape)', linewidth=2)
    plt.yscale('log')
    plt.title('Self-Adjoint Rigidity: Spectral Gap $\Delta(N)$')
    plt.ylabel('Resolution Gap (Log Scale)')
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    # Plot 2: Computation Time (Physical Resources)
    plt.subplot(2, 1, 2)
    plt.plot(N, time_p, 'g', label='Polynomial Solver ($t_{poly}$)', linewidth=2)
    plt.plot(N, time_np, 'r', label='NP Selection ($t_{exp}$)', linewidth=2)
    plt.yscale('log')
    plt.title('Physically Realizable Time $t_{phys}$')
    plt.xlabel('Problem Size (N bits / variables)')
    plt.ylabel('Time Cost (Log Scale)')
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    
    # Save assets
    import os
    asset_dir = r"d:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_01_P_VS_NP\assets"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
        
    plt.savefig(os.path.join(asset_dir, "p_vs_np_gap_analysis.png"), dpi=300)
    print(f"P vs NP gap analysis plot saved to assets/p_vs_np_gap_analysis.png")

if __name__ == "__main__":
    simulate_p_np_gap()
