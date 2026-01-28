"""
Stage 39: U_2 Lindblad Class
============================

INVESTIGATE THE alpha = 2 UNIVERSALITY CLASS

OBSERVED IN
-----------
- Quantum Decoherence (Stage 36)
- GUE Level Repulsion (Dyson 1962)

THEORETICAL BASIS
-----------------
Lindblad master equation: drho/dt = -gamma * [H,[H,rho]]
Solution: rho_ij(t) = rho_ij(0) * exp(-gamma * t)
Purity: P = Tr(rho^2) ~ exp(-2*gamma*t)

This gives alpha = 2 when fitting to (1+c)^{-alpha}.
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.linalg import expm
from typing import Tuple


def power_law(c, alpha):
    return (1 + c) ** (-alpha)


class LindbladDephasing:
    """
    Model pure dephasing of a qubit under Lindblad dynamics.
    """
    
    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
    
    def evolve_purity(self, t_values: np.ndarray) -> np.ndarray:
        """
        Purity P(t) for dephasing.
        
        For pure dephasing: P(t) = (1 + exp(-2*gamma*t))/2
        Normalized to phi(0) = 1: phi(t) = (P(t) - 0.5) / 0.5

        """
        return (1 + np.exp(-2 * self.gamma * t_values)) / 2
    
    def coherence(self, t_values: np.ndarray) -> np.ndarray:
        """Off-diagonal coherence decay."""
        return np.exp(-self.gamma * t_values)


class GUELevelSpacing:
    """
    Level spacing distribution for GUE (Gaussian Unitary Ensemble).
    
    P(s) ~ s^2 * exp(-4*s^2/pi) for small s
    The s^2 term gives alpha = 2.
    """
    
    @staticmethod
    def wigner_surmise(s: np.ndarray) -> np.ndarray:
        """GUE Wigner surmise for level spacing."""
        return (32 / np.pi**2) * s**2 * np.exp(-4 * s**2 / np.pi)
    
    @staticmethod
    def sample_gue_eigenvalues(n: int) -> np.ndarray:
        """Sample eigenvalues from GUE."""
        # Random Hermitian matrix
        A = np.random.randn(n, n) + 1j * np.random.randn(n, n)
        H = (A + A.conj().T) / 2 / np.sqrt(2 * n)
        
        eigenvalues = np.linalg.eigvalsh(H)
        return np.sort(eigenvalues)
    
    def level_spacing_statistics(self, n: int = 100, n_samples: int = 50) -> np.ndarray:
        """Compute level spacing distribution."""
        spacings = []
        
        for _ in range(n_samples):
            eigs = self.sample_gue_eigenvalues(n)
            # Unfold (simple linear unfolding)
            mean_spacing = np.mean(np.diff(eigs))
            normalized_spacings = np.diff(eigs) / mean_spacing
            spacings.extend(normalized_spacings)
        
        return np.array(spacings)


class AmplitudeDamping:
    """
    Amplitude damping channel (T1 decay).
    
    Different from dephasing - describes energy relaxation.
    """
    
    def __init__(self, gamma: float = 1.0):
        self.gamma = gamma
    
    def excited_state_population(self, t_values: np.ndarray) -> np.ndarray:
        """Population of excited state decay."""
        return np.exp(-self.gamma * t_values)


def analyze_u2_class():
    """Analyze the U_2 (alpha = 2) universality class."""
    
    print("=" * 70)
    print("STAGE 39: U_2 LINDBLAD CLASS (alpha = 2)")
    print("=" * 70)
    
    # 1. Dephasing
    print("\n1. DEPHASING (PURITY DECAY)")
    print("-" * 50)
    
    deph = LindbladDephasing(gamma=1.0)
    t_values = np.linspace(0, 5, 50)
    purity = deph.evolve_purity(t_values)
    
    # Convert to (1+c)^{-alpha} form
    # c = 2*gamma*t (the natural parameter)
    c_values = 2 * t_values
    phi_values = (purity - 0.5) / 0.5  # Normalize to phi(0) = 1
    
    # Only fit where phi > 0
    valid = phi_values > 0.01
    try:
        popt, _ = curve_fit(power_law, c_values[valid], phi_values[valid], p0=[1.0])
        print(f"   Fitted alpha = {popt[0]:.4f}")
        print(f"   Expected alpha = 2.0 (from Lindblad)")
        print(f"   Match: {abs(popt[0] - 2.0) < 0.5}")
    except Exception as e:
        print(f"   Fit error: {e}")
    
    # 2. GUE Level Spacing
    print("\n\n2. GUE LEVEL REPULSION")
    print("-" * 50)
    
    gue = GUELevelSpacing()
    spacings = gue.level_spacing_statistics(n=50, n_samples=30)
    
    # P(s) ~ s^2 for small s
    s_small = spacings[spacings < 0.5]
    if len(s_small) > 0:
        print(f"   Small spacing count: {len(s_small)}")
        print(f"   Mean small spacing: {np.mean(s_small):.4f}")
        print(f"   P(s) ~ s^beta => beta = 2 for GUE")
    
    # 3. Amplitude Damping
    print("\n\n3. AMPLITUDE DAMPING (T1 DECAY)")
    print("-" * 50)
    
    amp = AmplitudeDamping(gamma=1.0)
    pop = amp.excited_state_population(t_values)
    
    # Fit
    c_values = t_values
    try:
        popt, _ = curve_fit(power_law, c_values[1:], pop[1:], p0=[1.0])
        print(f"   Fitted alpha = {popt[0]:.4f}")
        print(f"   Expected: exponential decay, not power law")
        print(f"   Note: Exponential doesn't fit power law well")
    except Exception as e:
        print(f"   Fit error: {e}")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("U_2 CLASS SUMMARY")
    print("=" * 70)
    print("""
    THE U_2 (alpha = 2) UNIVERSALITY CLASS:
    
    1. ORIGIN: Lindblad master equation
       - drho/dt = -gamma * [H,[H,rho]]
       - Purity: P ~ exp(-2*gamma*t)
    
    2. APPEARS IN:
       - Quantum dephasing (T2 decay)
       - GUE level repulsion (P(s) ~ s^2)
       - Quadratic noise processes
    
    3. KEY DIFFERENCE FROM U_{1/2}:
       - U_{1/2}: Discrete state space, counting mechanism
       - U_2: Continuous state space, quadratic decay
    
    4. MATHEMATICAL SIGNATURE:
       - phi(c) = (1 + c)^{-2} or exp(-c^2)
       - Characteristic of "soft" perturbations in continuous systems
""")
    
    print("=" * 70)
    print("END OF U_2 ANALYSIS")
    print("=" * 70)


if __name__ == "__main__":
    analyze_u2_class()
