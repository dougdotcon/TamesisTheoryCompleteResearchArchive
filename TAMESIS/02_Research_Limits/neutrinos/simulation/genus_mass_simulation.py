import numpy as np
import matplotlib.pyplot as plt

def neutrino_genus_fit():
    """
    Investigates the hypothesis that Neutrino Masses scale with the Genus (g) 
    of the topological manifold.
    
    Data (Normal Ordering Approximation):
    m1 ~ 0 (Reference)
    m2 = sqrt(Delta_m21^2) ~ sqrt(7.5e-5) ~ 0.0086 eV
    m3 = sqrt(Delta_m31^2) ~ sqrt(2.5e-3) ~ 0.0500 eV
    
    Ratio m3 / m2 ~ 5.8
    """
    
    # 1. Physical Data
    delta_m21_sq = 7.5e-5
    delta_m32_sq = 2.5e-3
    
    # Assuming Normal Ordering with m1 = 0 (lightest)
    m1 = 0.0
    m2 = np.sqrt(delta_m21_sq)
    m3 = np.sqrt(delta_m21_sq + delta_m32_sq)
    
    masses = np.array([m1, m2, m3])
    ratios = np.array([0, 1, m3/m2]) # Relative to m2
    
    print(f"Neutrino Masses (Approx):")
    print(f"m1: {m1:.5f} eV")
    print(f"m2: {m2:.5f} eV")
    print(f"m3: {m3:.5f} eV")
    print(f"Ratio m3/m2: {m3/m2:.2f}")
    
    # 2. Topological Models
    # Hypothesis: Genus g = 1, 2, 3? Or 2, 3, 4?
    # Knowing Quarks (g=1, torus?) are heavy.
    # Maybe Neutrinos are g=2, 3, 4?
    
    # Model A: Mass ~ Scaling Factor ^ (Genus - Offset)
    # Let's try Genus sets:
    genus_set_1 = np.array([1, 2, 3])
    genus_set_2 = np.array([2, 3, 4])
    
    # We want to match the jump factor ~5.8
    
    # Geometric Properties of Genus g surfaces (Hyperbolic Metric):
    # Area = 4pi(g-1)
    # Euler Characteristic = 2 - 2g
    
    # Check Area Scaling:
    # A(g=2) = 4pi(1)
    # A(g=3) = 4pi(2)
    # Ratio A3/A2 = 2.0 (Too small, we need ~5.8)
    
    # Check Exponential of Euler Characteristic:
    # M ~ exp(-Chi) = exp(2g - 2)
    # g=2 -> exp(2) ~ 7.38
    # g=3 -> exp(4) ~ 54.6
    # Ratio m3/m2 ~ 7.38 (Close to 5.8!)
    
    print(f"\n--- Testing Model: Mass ~ exp(Euler_Characteristic) ---")
    print(f"M ~ exp(2g)")
    
    # Fit: M_g = M_0 * exp(alpha * g)
    # Log(M) = Log(M0) + alpha * g
    
    # We only have 2 non-zero points (m2, m3) to fit 2 parameters (M0, alpha).
    # m2 (g=2) = 0.0086
    # m3 (g=3) = 0.0500
    
    # log(m2) = log(M0) + 2*alpha
    # log(m3) = log(M0) + 3*alpha
    # alpha = log(m3) - log(m2) = log(m3/m2) = log(5.8)
    
    alpha = np.log(m3/m2)
    print(f"Calculated Alpha (Slope): {alpha:.3f}")
    print(f"Comparison:")
    print(f"  Observed Slope log(m3/m2): {np.log(5.8):.3f} ~ 1.76")
    print(f"  Prediction from Euler (exp(2g)): Slope = 2.0")
    print(f"  Prediction from Hyperbolic Vol (exp(V)): V3/V2?")
    
    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Data Points
    generations = [2, 3] # Assigning Genus 2 and 3 to nu2, nu3
    mass_vals = [m2, m3]
    
    ax.semilogy(generations, mass_vals, 'bo-', markersize=10, label='Neutrino Data (m2, m3)')
    
    # Geometric Prediction (alpha = 1.76)
    g_range = np.linspace(1.5, 3.5, 100)
    # Calibrate M0
    # log(m2) = logM0 + 2*alpha -> logM0 = log(m2) - 2*alpha
    logM0 = np.log(m2) - 2*alpha
    M0 = np.exp(logM0)
    
    y_pred = M0 * np.exp(alpha * g_range)
    
    ax.semilogy(g_range, y_pred, 'r--', label=f'Fit: M ~ exp({alpha:.2f} * g)')
    
    # Extrapolate to g=1 (Electron??)
    m_g1 = M0 * np.exp(alpha * 1)
    print(f"Extrapolation to g=1: {m_g1:.5f} eV")
    print(f"Actual Electron Mass: 511,000 eV (Mismatch - implies distinct topology class)")
    
    ax.set_title("Neutrino Mass vs Topological Genus", fontsize=14)
    ax.set_xlabel("Genus (g)", fontsize=12)
    ax.set_ylabel("Mass (eV)", fontsize=12)
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../analysis/genus_mass_fit.png')
    print("Plot saved.")

if __name__ == "__main__":
    neutrino_genus_fit()
