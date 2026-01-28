import numpy as np
import matplotlib.pyplot as plt

def simulate_explicit_formula_attack():
    print("--- Riemann Attack: Explicit Formula & Variance ---")
    
    x = np.linspace(10, 1000, 500)
    
    # 1. Critical Line Zero contribution
    # x^(1/2 + i gamma)
    gamma = 14.13 # First zero
    term_critical = x**(0.5) * np.cos(gamma * np.log(x))
    
    # 2. Off-line Zero contribution (Hypothetical)
    # x^(0.8 + i gamma) -> Violates RH
    term_offline = x**(0.8) * np.cos(gamma * np.log(x))
    
    # Variance "Detector" (Bound from Number Theory)
    # The error E(x) should be O(x^(1/2) log x)
    bound = x**(0.5) * np.log(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, term_critical, label='Critical Zero Contribution ($x^{1/2}$)', alpha=0.6)
    plt.plot(x, term_offline, 'r--', label='Off-Line Zero Contribution ($x^{0.8}$)', linewidth=2)
    plt.plot(x, bound, 'k:', label='Admissible Variance Bound ($x^{1/2} \log x$)')
    plt.plot(x, -bound, 'k:')
    
    plt.title('Arithmetic Rigidity: Off-line zeros violate Variance Bounds')
    plt.xlabel('x')
    plt.ylabel('Contribution to $\psi(x) - x$')
    plt.legend()
    plt.grid(True)
    
    print("\nReduction to Pure Math:")
    print("Physical 'Instability' = Arithmetic 'Variance Explosion'.")
    print("If an off-line zero exists, the integral of |E(x)|^2 diverges beyond the Admissible/GUE limit.")
    
    plt.savefig('riemann_attack.png')
    print("Plot saved to riemann_attack.png")

if __name__ == "__main__":
    simulate_explicit_formula_attack()
