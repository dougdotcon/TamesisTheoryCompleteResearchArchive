"""
Experimental Predictions for M_c Critical Mass
===============================================

This module generates concrete, testable predictions for experiments
that can confirm or falsify the M_c hypothesis.

Target Experiments:
1. Levitated optomechanics (nanoparticles)
2. Matter-wave interferometry (MAQRO-class)
3. Mechanical oscillators (cantilevers)
4. Ground-state cooling experiments

Key Prediction:
    At M = M_c ≈ 5.3 × 10⁻¹⁶ kg, τ_c ≈ 2.18 seconds
    For M > M_c: τ(M) = τ_c × (M_c/M)²
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Dict, Tuple

# Import constants
try:
    from simulations.constants import (
        M_C, TAU_C_CALIBRATED, ALPHA_DEFAULT, HBAR, K_B,
        RHO_SILICA, G_SI, C, R_C_SILICA
    )
except ModuleNotFoundError:
    from constants import (
        M_C, TAU_C_CALIBRATED, ALPHA_DEFAULT, HBAR, K_B,
        RHO_SILICA, G_SI, C, R_C_SILICA
    )


# =============================================================================
# CALIBRATED M_C MODEL CLASS
# =============================================================================

class MCModelCalibrated:
    """
    Calibrated M_c model for experimental predictions.
    
    Uses:
        τ_c = 2.18 s (from gravitational derivation)
        α = 2 (power law exponent)
    """
    
    def __init__(self):
        self.M_c = M_C
        self.tau_c = TAU_C_CALIBRATED
        self.alpha = ALPHA_DEFAULT
        self.R_c = R_C_SILICA
    
    def coherence_time(self, mass: float) -> float:
        """τ(M) = τ_c × (M_c/M)^α for M > M_c, else ∞"""
        if mass <= self.M_c:
            return np.inf
        return self.tau_c * (self.M_c / mass)**self.alpha
    
    def decoherence_rate(self, mass: float, delta_x: float = None) -> float:
        """
        Γ(M) = 1/τ(M) with optional spatial enhancement.
        
        For superposition separation Δx:
        Γ(M, Δx) = Γ(M) × (Δx / R_c)²
        """
        tau = self.coherence_time(mass)
        if np.isinf(tau):
            return 0.0
        
        gamma = 1.0 / tau
        
        if delta_x is not None:
            gamma *= (delta_x / self.R_c)**2
        
        return gamma
    
    def visibility(self, mass: float, time: float, 
                   delta_x: float = None) -> float:
        """V(t) = exp(-Γ × t)"""
        gamma = self.decoherence_rate(mass, delta_x)
        return np.exp(-gamma * time)
    
    def time_to_visibility(self, mass: float, target_visibility: float = 0.5,
                           delta_x: float = None) -> float:
        """Calculate time to reach target visibility."""
        gamma = self.decoherence_rate(mass, delta_x)
        if gamma == 0:
            return np.inf
        return -np.log(target_visibility) / gamma


# =============================================================================
# EXPERIMENTAL SCENARIOS
# =============================================================================

@dataclass
class ExperimentalScenario:
    """Container for experimental parameters."""
    name: str
    mass_kg: float
    temperature_K: float
    observation_time_s: float
    superposition_separation_m: float
    description: str


def get_experimental_scenarios() -> List[ExperimentalScenario]:
    """Define realistic experimental scenarios."""
    
    scenarios = [
        # Below M_c - should show NO intrinsic decoherence
        ExperimentalScenario(
            name="Large Molecule Interferometry",
            mass_kg=2.5e-23,  # ~15,000 amu (oligoporphyrin)
            temperature_K=300,
            observation_time_s=1e-3,
            superposition_separation_m=1e-7,
            description="Vienna/Basel style molecule interferometry"
        ),
        ExperimentalScenario(
            name="Levitated Nanoparticle (Small)",
            mass_kg=1e-18,  # ~600,000 amu
            temperature_K=1e-3,  # Ground state cooled
            observation_time_s=1.0,
            superposition_separation_m=1e-6,
            description="Ground-state cooled silica nanosphere"
        ),
        
        # Near M_c - critical testing zone
        ExperimentalScenario(
            name="Levitated Nanoparticle (M_c)",
            mass_kg=M_C,  # Exactly at critical mass
            temperature_K=1e-3,
            observation_time_s=5.0,
            superposition_separation_m=1e-6,
            description="Silica sphere at critical mass (~386 nm radius)"
        ),
        ExperimentalScenario(
            name="MAQRO Target Mass",
            mass_kg=1e-15,  # 2× M_c
            temperature_K=1e-3,
            observation_time_s=10.0,
            superposition_separation_m=1e-6,
            description="MAQRO mission target nanoparticle"
        ),
        
        # Above M_c - should show clear decoherence
        ExperimentalScenario(
            name="Large Nanosphere",
            mass_kg=1e-14,  # ~20× M_c
            temperature_K=1e-3,
            observation_time_s=1.0,
            superposition_separation_m=1e-5,
            description="Larger optomechanical system"
        ),
        ExperimentalScenario(
            name="Micromechanical Oscillator",
            mass_kg=1e-12,  # ~2000× M_c
            temperature_K=0.01,
            observation_time_s=0.1,
            superposition_separation_m=1e-10,  # Much smaller separation
            description="Cantilever or membrane oscillator"
        ),
    ]
    
    return scenarios


def predict_for_scenario(scenario: ExperimentalScenario, 
                        model: MCModelCalibrated) -> Dict:
    """Generate predictions for an experimental scenario."""
    
    tau = model.coherence_time(scenario.mass_kg)
    gamma = model.decoherence_rate(scenario.mass_kg, 
                                    scenario.superposition_separation_m)
    V_final = model.visibility(scenario.mass_kg, scenario.observation_time_s,
                               scenario.superposition_separation_m)
    t_half = model.time_to_visibility(scenario.mass_kg, 0.5,
                                      scenario.superposition_separation_m)
    
    # Environmental decoherence estimate (thermal gas)
    # Very rough: Γ_env ~ n × σ × v where n = P/(kT), σ ~ R², v ~ sqrt(kT/m_gas)
    # At UHV (10⁻¹² Pa) and cryogenic T
    P_uhv = 1e-12  # Pa
    n_gas = P_uhv / (K_B * scenario.temperature_K + 1e-30)
    v_gas = np.sqrt(2 * K_B * scenario.temperature_K / (28 * 1.66e-27))  # N2
    R_particle = (3 * scenario.mass_kg / (4 * np.pi * RHO_SILICA))**(1/3)
    sigma_geom = np.pi * R_particle**2
    gamma_env_est = n_gas * sigma_geom * v_gas * 1e-3  # Rough factor
    
    return {
        "scenario": scenario.name,
        "mass_kg": scenario.mass_kg,
        "M_over_Mc": scenario.mass_kg / M_C,
        "tau_intrinsic_s": tau,
        "gamma_intrinsic_s-1": gamma,
        "visibility_final": V_final,
        "time_to_half_visibility_s": t_half,
        "gamma_env_estimate_s-1": gamma_env_est,
        "intrinsic_dominant": gamma > gamma_env_est if gamma > 0 else False,
        "testable": gamma > gamma_env_est * 0.1 if gamma > 0 else False
    }


def generate_predictions_table(save_path: str = None):
    """Generate and print predictions for all scenarios."""
    
    model = MCModelCalibrated()
    scenarios = get_experimental_scenarios()
    
    print("\n" + "=" * 80)
    print("M_C MODEL: EXPERIMENTAL PREDICTIONS")
    print("=" * 80)
    print(f"\nCalibrated Parameters:")
    print(f"  M_c = {M_C:.4e} kg = {M_C/1.66e-27:.2e} Da")
    print(f"  τ_c = {TAU_C_CALIBRATED:.4f} s")
    print(f"  α   = {ALPHA_DEFAULT}")
    print()
    
    # Header
    print(f"{'Scenario':<30} {'M/M_c':<10} {'τ (s)':<12} {'Γ (s⁻¹)':<12} {'V_final':<10} {'Testable?':<10}")
    print("-" * 84)
    
    results = []
    for scenario in scenarios:
        pred = predict_for_scenario(scenario, model)
        results.append(pred)
        
        tau_str = f"{pred['tau_intrinsic_s']:.2e}" if pred['tau_intrinsic_s'] < 1e20 else "∞"
        gamma_str = f"{pred['gamma_intrinsic_s-1']:.2e}" if pred['gamma_intrinsic_s-1'] > 0 else "0"
        testable_str = "YES" if pred['testable'] else "No"
        
        print(f"{pred['scenario']:<30} {pred['M_over_Mc']:<10.2f} {tau_str:<12} {gamma_str:<12} {pred['visibility_final']:<10.4f} {testable_str:<10}")
    
    print()
    print("=" * 80)
    
    # Key predictions
    print("\n📊 KEY TESTABLE PREDICTIONS:")
    print("-" * 50)
    
    for pred in results:
        if pred['testable']:
            print(f"\n🎯 {pred['scenario']}:")
            print(f"   Mass: {pred['mass_kg']:.2e} kg ({pred['M_over_Mc']:.1f} × M_c)")
            print(f"   Intrinsic coherence time: {pred['tau_intrinsic_s']:.4f} s")
            print(f"   Visibility after typical observation: {pred['visibility_final']:.4f}")
            print(f"   Time to 50% visibility: {pred['time_to_half_visibility_s']:.4f} s")
    
    return results


def plot_predictions(save_path: str = None):
    """Generate prediction plots for publication."""
    
    model = MCModelCalibrated()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Coherence time vs mass with experimental regions
    ax1 = axes[0, 0]
    masses = np.logspace(-20, -8, 500)
    tau_values = np.array([model.coherence_time(m) for m in masses])
    tau_plot = np.where(np.isinf(tau_values), np.nan, tau_values)
    
    ax1.loglog(masses, tau_plot, 'b-', linewidth=2.5, label='M_c Model (α=2)')
    ax1.axvline(M_C, color='red', linestyle='--', linewidth=2, 
                label=f'$M_c$ = {M_C:.2e} kg')
    ax1.axhline(1, color='green', linestyle=':', alpha=0.7, linewidth=1.5,
                label='1 second')
    ax1.axhline(TAU_C_CALIBRATED, color='orange', linestyle='-.', linewidth=1.5,
                label=f'τ_c = {TAU_C_CALIBRATED:.2f} s')
    
    # Experimental regions
    ax1.axvspan(1e-24, 1e-21, alpha=0.2, color='green', label='Molecules')
    ax1.axvspan(1e-18, 1e-15, alpha=0.2, color='blue', label='Nanoparticles')
    ax1.axvspan(1e-14, 1e-10, alpha=0.2, color='purple', label='Oscillators')
    
    ax1.set_xlabel('Mass (kg)', fontsize=12)
    ax1.set_ylabel('Coherence Time τ (s)', fontsize=12)
    ax1.set_title('Intrinsic Coherence Time vs Mass', fontsize=14)
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1e-20, 1e-8)
    ax1.set_ylim(1e-10, 1e15)
    
    # 2. Visibility vs observation time at different masses
    ax2 = axes[0, 1]
    time_array = np.linspace(0, 10, 500)
    test_masses = [0.5*M_C, M_C, 2*M_C, 5*M_C, 10*M_C, 50*M_C]
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(test_masses)))
    
    for m, color in zip(test_masses, colors):
        V = np.array([model.visibility(m, t) for t in time_array])
        ratio = m / M_C
        label = f'M = {ratio:.1f} M_c'
        if ratio >= 1:
            ax2.plot(time_array, V, color=color, linewidth=2, label=label)
        else:
            ax2.plot(time_array, V, color=color, linewidth=2, linestyle='--', 
                     label=label + ' (below M_c)')
    
    ax2.axhline(0.5, color='red', linestyle=':', linewidth=1.5, 
                label='V = 0.5 (threshold)')
    ax2.set_xlabel('Time (s)', fontsize=12)
    ax2.set_ylabel('Visibility V(t)', fontsize=12)
    ax2.set_title('Interference Visibility Decay', fontsize=14)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1.05)
    
    # 3. Time to 50% visibility vs mass
    ax3 = axes[1, 0]
    masses_above = np.logspace(np.log10(M_C*1.01), -10, 200)
    t_half = np.array([model.time_to_visibility(m, 0.5) for m in masses_above])
    
    ax3.loglog(masses_above / M_C, t_half, 'b-', linewidth=2.5)
    ax3.axhline(1, color='green', linestyle=':', linewidth=1.5, label='1 second')
    ax3.axhline(0.1, color='orange', linestyle=':', linewidth=1.5, label='100 ms')
    ax3.axhline(1e-3, color='red', linestyle=':', linewidth=1.5, label='1 ms')
    
    ax3.set_xlabel('M / M_c', fontsize=12)
    ax3.set_ylabel('Time to V = 0.5 (s)', fontsize=12)
    ax3.set_title('Time to 50% Visibility vs Mass', fontsize=14)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(1, 1e8)
    ax3.set_ylim(1e-12, 1e4)
    
    # 4. Comparison: M_c prediction vs other models
    ax4 = axes[1, 1]
    masses_comp = np.logspace(-18, -10, 200)
    
    # M_c model
    gamma_mc = np.array([model.decoherence_rate(m) for m in masses_comp])
    gamma_mc_plot = np.where(gamma_mc > 0, gamma_mc, np.nan)
    ax4.loglog(masses_comp, gamma_mc_plot, 'b-', linewidth=2.5, label='M_c Model')
    
    # CSL (approximate)
    lambda_csl = 1e-16
    m_nucleon = 1.67e-27
    gamma_csl = lambda_csl * (masses_comp / m_nucleon)**2
    ax4.loglog(masses_comp, gamma_csl, 'g--', linewidth=2, label='CSL')
    
    # Diósi-Penrose
    delta_x = 1e-6  # 1 micron separation
    gamma_dp = G_SI * masses_comp**2 / (HBAR * delta_x)
    ax4.loglog(masses_comp, gamma_dp, 'm:', linewidth=2, label='Diósi-Penrose')
    
    ax4.axvline(M_C, color='red', linestyle='--', linewidth=2)
    ax4.axhline(1, color='gray', linestyle=':', alpha=0.5)
    
    ax4.set_xlabel('Mass (kg)', fontsize=12)
    ax4.set_ylabel('Decoherence Rate Γ (s⁻¹)', fontsize=12)
    ax4.set_title('Model Comparison (Δx = 1 μm)', fontsize=14)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(1e-18, 1e-10)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved: {save_path}")
    
    plt.close()
    return fig


# =============================================================================
# FALSIFIABILITY CRITERIA
# =============================================================================

def print_falsifiability_criteria():
    """Print clear falsifiability conditions."""
    
    print("\n" + "=" * 70)
    print("FALSIFIABILITY CRITERIA FOR M_c HYPOTHESIS")
    print("=" * 70)
    
    print("""
The M_c hypothesis makes the following FALSIFIABLE predictions:

1. COHERENCE LIMIT
   ━━━━━━━━━━━━━━━━
   Prediction: Stable quantum interference (V > 50%) is IMPOSSIBLE
               for M ≥ 10⁻¹⁴ kg maintained for t > 1 second.
   
   → FALSIFIED if: Any experiment observes V > 50% for M ≥ 10⁻¹⁴ kg
                   at t > 1 second with excellent environmental isolation.

2. MASS THRESHOLD
   ━━━━━━━━━━━━━━━
   Prediction: There exists a sharp transition at M_c ≈ 5.3 × 10⁻¹⁶ kg.
               Below M_c: no intrinsic decoherence limit
               Above M_c: decoherence rate scales as (M/M_c)²
   
   → FALSIFIED if: Coherence observed for M >> M_c at times >> τ(M)
   → FALSIFIED if: Decoherence observed for M << M_c at any time

3. SCALING LAW
   ━━━━━━━━━━━━
   Prediction: τ(M) = τ_c × (M_c/M)² with τ_c ≈ 2.18 s
   
   → FALSIFIED if: Observed scaling differs from quadratic
   → FALSIFIED if: τ_c differs by more than order of magnitude

4. ENVIRONMENTAL INDEPENDENCE
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Prediction: For M > 10 × M_c, intrinsic decoherence dominates.
               Improving vacuum/temperature does NOT increase coherence time.
   
   → FALSIFIED if: Coherence time increases with improved isolation
                   for M > 5 × 10⁻¹⁵ kg

""")
    
    print("=" * 70)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Print falsifiability criteria
    print_falsifiability_criteria()
    
    # Generate predictions table
    results = generate_predictions_table()
    
    # Generate plots
    print("\nGenerating prediction plots...")
    plot_predictions(save_path="experimental_predictions.png")
    
    print("\nDone!")
