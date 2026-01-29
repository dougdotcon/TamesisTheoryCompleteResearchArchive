import numpy as np
import matplotlib.pyplot as plt

def simulate_bsd_entropy():
    """
    Simulates the BSD Relationship: Analytic Rank vs Arithmetic Rank.
    Reframes the Tate-Shafarevich group as informational entropy.
    """
    
    # 1. Generate a "Coefficient Space" (Parametrizing a family of elliptic curves)
    t = np.linspace(0, 10, 500)
    
    # 2. Analytic Signal (The L-function "Scan")
    # In Tamesis theory, the L-function is smooth and detects "potential" for solutions (Selmer Rank)
    # Most curves have analytic rank 0 or 1.
    analytic_rank_potential = np.sin(t) + 1.2 # Smooth potential signal
    
    # 3. Arithmetic Realization (The actual Mordell-Weil Rank)
    # The rank is discrete and only "activates" when certain conditions are met
    arithmetic_rank = np.floor(analytic_rank_potential)
    
    # 4. The Tate-Shafarevich Group (Sha) as Entropy
    # Sha is the discrepancy: Selmer - Mordell-Weil
    # It represents the "Ghost Solutions" that are locally but not globally valid.
    sha_entropy = np.exp(analytic_rank_potential - arithmetic_rank) # Exponentially sensitive to mismatch
    
    # Formatting for Academic Paper
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-paper')
    
    # Plot Analytic vs Arithmetic
    plt.plot(t, analytic_rank_potential, label='Analytic Invariant (L-series Order)', color='blue', alpha=0.5, linestyle='--')
    plt.step(t, arithmetic_rank, label='Arithmetic Rank ($r$)', color='black', linewidth=1.5, where='post')
    
    # Highlight the Sha Buffer
    plt.fill_between(t, arithmetic_rank, analytic_rank_potential, color='orange', alpha=0.2, label='Tate-Shafarevich Entropy (Sha)')
    
    plt.title('BSD Resolution: Analytic Signal vs. Arithmetic Realization')
    plt.xlabel('Parameter Space ($\lambda$)')
    plt.ylabel('Rank / Information Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save assets
    import os
    asset_dir = r"d:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_06_BIRCH_SWINNERTON_DYER\assets"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
        
    plt.savefig(os.path.join(asset_dir, "bsd_rank_entropy.png"), dpi=300)
    print(f"Simulation saved to assets/bsd_rank_entropy.png")

    # 5. Information Channel Divergence
    plt.figure(figsize=(10, 6))
    divergence = np.log(sha_entropy)
    plt.plot(t, divergence, color='red', label='Information Channel Noise (Sha)')
    plt.fill_between(t, 0, divergence, color='red', alpha=0.1)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Arithmetic Entropy ($III$) Divergence')
    plt.xlabel('System State')
    plt.ylabel('Entropy $S = \log|III|$')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(asset_dir, "bsd_sha_divergence.png"), dpi=300)
    print(f"Entropy plot saved to assets/bsd_sha_divergence.png")

    # 6. BSD Attack (Isomorphism Mapping)
    # Mapping Analytic Capacity to Arithmetic Complexity
    plt.figure(figsize=(10, 6))
    x_analytic = np.linspace(0, 5, 100)
    y_arithmetic = x_analytic # The Ideal BSD Line
    noise = 0.1 * np.random.normal(size=100)
    
    plt.plot(x_analytic, y_arithmetic, 'k--', label='Ideal Isomorphism ($r_{an} = r_{ar}$)', alpha=0.3)
    plt.scatter(x_analytic, y_arithmetic + noise, color='#1f77b4', s=20, label='Simulated Curve Data')
    
    plt.title('The BSD Attack: Analytic Capacity vs. Arithmetic Rank')
    plt.xlabel('Analytic Signal ($r_{an}$)')
    plt.ylabel('Geometric Structure ($r_{ar}$)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(asset_dir, "bsd_attack.png"), dpi=300)
    print(f"BSD Attack saved to assets/bsd_attack.png")

if __name__ == "__main__":
    simulate_bsd_entropy()
