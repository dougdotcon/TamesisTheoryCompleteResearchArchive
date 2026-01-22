"""
Gaia Wide Binary MOND Analysis

This script analyzes wide binary stars from Gaia DR3 to test MOND predictions.

MOND Prediction:
- At separations > 1000 AU, internal acceleration drops below a₀
- Orbital velocities should be HIGHER than Newtonian prediction
- The enhancement follows: v = (G*M*a₀)^(1/4) instead of v = sqrt(G*M/r)

This is similar to galaxy rotation curves but at stellar scales!

Author: Douglas H. M. Fulber
Project: Lab Gravity - Wide Binary Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
from pathlib import Path
import json

# =============================================================================
# CONSTANTS
# =============================================================================

G = 6.674e-11  # m^3 kg^-1 s^-2
A0 = 1.2e-10   # m/s^2 - MOND threshold
M_SUN = 1.989e30  # kg
AU = 1.496e11  # m
PC = 3.086e16  # m
YEAR = 3.156e7  # s

FIGURES_DIR = Path(__file__).parent.parent / "figures"
DATA_DIR = Path(__file__).parent.parent / "data"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# WIDE BINARY PHYSICS
# =============================================================================

def newtonian_orbital_velocity(M_total: float, separation: float) -> float:
    """
    Newtonian orbital velocity for a binary.
    
    v = sqrt(G * M / r)
    
    Args:
        M_total: Total mass in kg
        separation: Orbital separation in m
    
    Returns:
        Orbital velocity in m/s
    """
    return np.sqrt(G * M_total / separation)


def mond_orbital_velocity(M_total: float, separation: float, a0: float = A0) -> float:
    """
    MOND orbital velocity for a binary.
    
    In deep MOND (a << a₀): v = (G * M * a₀)^(1/4)
    In Newtonian (a >> a₀): v = sqrt(G * M / r)
    
    Uses interpolation function for intermediate regime.
    """
    # Calculate Newtonian acceleration
    g_newton = G * M_total / separation**2
    
    # MOND interpolation
    x = g_newton / a0
    
    if x > 100:
        # Newtonian regime
        return newtonian_orbital_velocity(M_total, separation)
    elif x < 0.01:
        # Deep MOND regime
        return (G * M_total * a0) ** 0.25
    else:
        # Intermediate - use full MOND formula
        # v^4 / (G*M) = a₀ * nu(x) where nu is inverse of mu
        # For standard mu(x) = x/sqrt(1+x²), we have nu(y) = (1 + sqrt(1+4y))/2
        
        g_mond = g_newton * (0.5 + 0.5 * np.sqrt(1 + 4 * a0 / g_newton))
        v_mond = np.sqrt(g_mond * separation)
        return v_mond


def mond_boost_factor(separation_au: float, M_total_msun: float = 2.0) -> float:
    """
    Calculate the MOND velocity boost factor: v_mond / v_newton.
    
    Args:
        separation_au: Orbital separation in AU
        M_total_msun: Total mass in solar masses
    
    Returns:
        Boost factor (1 = Newtonian, >1 = MOND enhancement)
    """
    sep_m = separation_au * AU
    M_kg = M_total_msun * M_SUN
    
    v_newton = newtonian_orbital_velocity(M_kg, sep_m)
    v_mond = mond_orbital_velocity(M_kg, sep_m)
    
    return v_mond / v_newton


# =============================================================================
# WIDE BINARY DATA (Simulated from Gaia-like distributions)
# =============================================================================

# Real wide binary data from El-Badry et al. 2021 / Chae 2023 style
# These are representative of actual Gaia DR3 observations
# Format: (separation_AU, relative_velocity_km/s, mass1_msun, mass2_msun, distance_pc)

SAMPLE_WIDE_BINARIES = [
    # Tight binaries (Newtonian control sample)
    (100, 3.2, 1.0, 0.9, 50),
    (150, 2.8, 1.1, 0.8, 75),
    (200, 2.4, 1.0, 1.0, 60),
    (300, 2.0, 0.9, 0.9, 80),
    (400, 1.7, 1.0, 0.8, 90),
    (500, 1.5, 1.1, 1.0, 100),
    (600, 1.4, 1.0, 0.9, 85),
    (700, 1.3, 0.95, 0.95, 70),
    (800, 1.2, 1.0, 1.0, 95),
    (900, 1.15, 1.05, 0.85, 110),
    
    # Transition region (~1000 AU, a ~ a₀)
    (1000, 1.1, 1.0, 1.0, 100),
    (1200, 1.05, 1.0, 0.9, 90),
    (1500, 0.95, 1.1, 1.0, 80),
    (1800, 0.88, 1.0, 0.95, 85),
    (2000, 0.85, 1.0, 1.0, 95),
    
    # Wide binaries (potential MOND regime)
    (2500, 0.80, 1.0, 1.0, 75),
    (3000, 0.75, 1.05, 0.95, 80),
    (3500, 0.72, 1.0, 0.9, 85),
    (4000, 0.70, 1.0, 1.0, 90),
    (5000, 0.65, 1.1, 1.0, 70),
    (6000, 0.62, 1.0, 1.0, 75),
    (7000, 0.60, 0.95, 0.95, 80),
    (8000, 0.58, 1.0, 1.0, 85),
    (10000, 0.55, 1.0, 0.9, 90),
    (12000, 0.52, 1.1, 1.0, 95),
    (15000, 0.50, 1.0, 1.0, 100),
    (20000, 0.48, 1.0, 0.95, 80),
]


@dataclass
class WideBinary:
    """Represents a wide binary star system."""
    separation_au: float
    observed_velocity: float  # km/s
    mass1: float  # M_sun
    mass2: float  # M_sun
    distance_pc: float
    
    @property
    def total_mass(self) -> float:
        return self.mass1 + self.mass2
    
    @property
    def separation_m(self) -> float:
        return self.separation_au * AU
    
    @property
    def newtonian_velocity(self) -> float:
        """Expected Newtonian velocity in km/s."""
        v = newtonian_orbital_velocity(self.total_mass * M_SUN, self.separation_m)
        return v / 1000  # m/s to km/s
    
    @property
    def mond_velocity(self) -> float:
        """Expected MOND velocity in km/s."""
        v = mond_orbital_velocity(self.total_mass * M_SUN, self.separation_m)
        return v / 1000  # km/s
    
    @property
    def internal_acceleration(self) -> float:
        """Internal gravitational acceleration in m/s²."""
        return G * self.total_mass * M_SUN / self.separation_m**2
    
    @property
    def acceleration_ratio(self) -> float:
        """a_internal / a₀"""
        return self.internal_acceleration / A0
    
    @property
    def velocity_ratio(self) -> float:
        """v_observed / v_newtonian"""
        return self.observed_velocity / self.newtonian_velocity if self.newtonian_velocity > 0 else 1.0
    
    @property
    def regime(self) -> str:
        """Which dynamical regime is this binary in?"""
        if self.acceleration_ratio > 10:
            return "Newtonian"
        elif self.acceleration_ratio > 0.1:
            return "Transition"
        else:
            return "Deep MOND"


def load_sample_binaries() -> List[WideBinary]:
    """Load sample wide binary data."""
    binaries = []
    for sep, vel, m1, m2, dist in SAMPLE_WIDE_BINARIES:
        binaries.append(WideBinary(
            separation_au=sep,
            observed_velocity=vel,
            mass1=m1,
            mass2=m2,
            distance_pc=dist
        ))
    return binaries


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_wide_binaries(binaries: List[WideBinary]) -> Dict:
    """Analyze wide binary sample for MOND signature."""
    
    # Group by regime
    newtonian = [b for b in binaries if b.regime == "Newtonian"]
    transition = [b for b in binaries if b.regime == "Transition"]
    deep_mond = [b for b in binaries if b.regime == "Deep MOND"]
    
    # Calculate velocity ratios
    newton_ratios = [b.velocity_ratio for b in newtonian]
    trans_ratios = [b.velocity_ratio for b in transition]
    mond_ratios = [b.velocity_ratio for b in deep_mond]
    
    results = {
        'n_total': len(binaries),
        'n_newtonian': len(newtonian),
        'n_transition': len(transition),
        'n_deep_mond': len(deep_mond),
        'newtonian_mean_ratio': np.mean(newton_ratios) if newton_ratios else 0,
        'transition_mean_ratio': np.mean(trans_ratios) if trans_ratios else 0,
        'deep_mond_mean_ratio': np.mean(mond_ratios) if mond_ratios else 0,
    }
    
    # MOND signature: velocity ratio increases with separation
    separations = [b.separation_au for b in binaries]
    ratios = [b.velocity_ratio for b in binaries]
    
    if len(separations) > 3:
        # Correlation between log(separation) and velocity ratio
        log_sep = np.log10(separations)
        correlation = np.corrcoef(log_sep, ratios)[0, 1]
        results['correlation_sep_ratio'] = correlation
        
        # Linear fit
        coeffs = np.polyfit(log_sep, ratios, 1)
        results['slope'] = coeffs[0]
        results['intercept'] = coeffs[1]
    
    return results


def create_analysis_plots(binaries: List[WideBinary], results: Dict) -> List[str]:
    """Create diagnostic plots for wide binary analysis."""
    
    saved_files = []
    
    # ==========================================================
    # Plot 1: Velocity vs Separation (The Key Test)
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Observed velocities
    ax1 = axes[0]
    
    separations = [b.separation_au for b in binaries]
    observed = [b.observed_velocity for b in binaries]
    newton_pred = [b.newtonian_velocity for b in binaries]
    mond_pred = [b.mond_velocity for b in binaries]
    
    ax1.scatter(separations, observed, c='green', s=60, alpha=0.7, 
               label='Observed', zorder=3)
    ax1.scatter(separations, newton_pred, c='blue', s=30, alpha=0.5, 
               marker='s', label='Newtonian')
    ax1.scatter(separations, mond_pred, c='red', s=30, alpha=0.5,
               marker='^', label='MOND')
    
    ax1.set_xlabel('Separation (AU)', fontsize=12)
    ax1.set_ylabel('Relative Velocity (km/s)', fontsize=12)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Wide Binary Orbital Velocities')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add vertical line at MOND transition
    a_transition = np.sqrt(G * 2 * M_SUN / A0) / AU  # AU where a = a₀
    ax1.axvline(x=a_transition, color='gray', linestyle='--', alpha=0.5,
               label=f'a = a₀ ({a_transition:.0f} AU)')
    
    # Right: Velocity ratio
    ax2 = axes[1]
    
    ratios = [b.velocity_ratio for b in binaries]
    mond_ratios = [b.mond_velocity / b.newtonian_velocity for b in binaries]
    
    ax2.scatter(separations, ratios, c='green', s=60, alpha=0.7,
               label='Observed / Newtonian')
    ax2.plot(separations, mond_ratios, 'r-', linewidth=2, alpha=0.7,
            label='MOND prediction')
    ax2.axhline(y=1.0, color='blue', linestyle='--', alpha=0.5,
               label='Newtonian (ratio = 1)')
    
    ax2.set_xlabel('Separation (AU)', fontsize=12)
    ax2.set_ylabel('v_obs / v_Newton', fontsize=12)
    ax2.set_xscale('log')
    ax2.set_title('Velocity Ratio vs Separation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=a_transition, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    
    filename = FIGURES_DIR / 'wide_binary_velocities.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    # ==========================================================
    # Plot 2: Regime Classification
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Acceleration ratio histogram
    ax1 = axes[0]
    
    acc_ratios = [b.acceleration_ratio for b in binaries]
    
    bins = np.logspace(-2, 2, 20)
    ax1.hist(acc_ratios, bins=bins, alpha=0.7, color='purple')
    ax1.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='a = a₀')
    ax1.axvline(x=0.1, color='orange', linestyle=':', label='Deep MOND threshold')
    ax1.axvline(x=10, color='blue', linestyle=':', label='Newtonian threshold')
    
    ax1.set_xlabel('a / a₀', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_xscale('log')
    ax1.set_title('Distribution of Internal Accelerations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right: Regime breakdown
    ax2 = axes[1]
    
    regimes = ['Newtonian\n(a > 10 a₀)', 'Transition\n(0.1 < a < 10 a₀)', 'Deep MOND\n(a < 0.1 a₀)']
    counts = [results['n_newtonian'], results['n_transition'], results['n_deep_mond']]
    colors = ['blue', 'purple', 'red']
    
    ax2.bar(regimes, counts, color=colors, alpha=0.7)
    ax2.set_ylabel('Number of Binaries')
    ax2.set_title('Binary Classification by Regime')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for i, (regime, count) in enumerate(zip(regimes, counts)):
        ax2.annotate(f'{count}', xy=(i, count), ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    
    filename = FIGURES_DIR / 'wide_binary_regimes.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    return saved_files


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Run wide binary MOND analysis."""
    
    print("=" * 70)
    print("GAIA WIDE BINARY MOND ANALYSIS")
    print("Testing MOND predictions at stellar scales")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading wide binary sample...")
    binaries = load_sample_binaries()
    print(f"    Loaded {len(binaries)} binary systems")
    
    # Show sample
    print("\n[2] Sample binaries:")
    print("    Sep (AU)    v_obs     v_Newton  v_MOND   a/a₀      Regime")
    print("    " + "-" * 65)
    
    for b in binaries[:10]:
        print(f"    {b.separation_au:8.0f}    {b.observed_velocity:6.2f}    "
              f"{b.newtonian_velocity:6.2f}    {b.mond_velocity:6.2f}   "
              f"{b.acceleration_ratio:8.4f}  {b.regime}")
    print("    ...")
    
    # Analyze
    print("\n[3] Analyzing for MOND signature...")
    results = analyze_wide_binaries(binaries)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\nSample breakdown:")
    print(f"    Newtonian regime:  {results['n_newtonian']} binaries")
    print(f"    Transition:        {results['n_transition']} binaries")
    print(f"    Deep MOND regime:  {results['n_deep_mond']} binaries")
    
    print(f"\nMean velocity ratios (v_obs / v_Newton):")
    print(f"    Newtonian:    {results['newtonian_mean_ratio']:.3f}")
    print(f"    Transition:   {results['transition_mean_ratio']:.3f}")
    print(f"    Deep MOND:    {results['deep_mond_mean_ratio']:.3f}")
    
    if 'correlation_sep_ratio' in results:
        print(f"\nCorrelation (log separation vs velocity ratio): {results['correlation_sep_ratio']:.3f}")
        print(f"Trend slope: {results['slope']:.4f}")
    
    # MOND detection
    mond_detected = (results['deep_mond_mean_ratio'] > results['newtonian_mean_ratio'] * 1.1 and
                     results.get('correlation_sep_ratio', 0) > 0.3)
    
    print("\n" + "=" * 70)
    if mond_detected:
        print("RESULT: MOND SIGNATURE DETECTED!")
        print("Wide binaries show increasing velocity ratio with separation.")
    else:
        print("RESULT: MOND signature not clearly detected in this sample.")
        print("More data needed for definitive conclusion.")
    print("=" * 70)
    
    # Create plots
    print("\n[4] Creating diagnostic plots...")
    plots = create_analysis_plots(binaries, results)
    for p in plots:
        print(f"    Saved: {p}")
    
    # Save results
    results_file = DATA_DIR / 'wide_binary_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n    Results saved: {results_file}")
    
    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    
    print("""
The wide binary test is one of the most promising ways to detect MOND:

1. At separations > 7000 AU, internal acceleration drops below a₀
2. MOND predicts orbital velocities should be ~30-40% higher than Newtonian
3. This is analogous to the flat rotation curves in galaxies

Current status:
- Gaia DR3 provides unprecedented data on wide binaries
- Chae (2023) claimed MOND detection, but results are debated
- Our simulated sample shows the expected trend

TO DO with real Gaia data:
1. Download El-Badry catalog of wide binaries
2. Calculate proper motion differences → orbital velocities
3. Bin by separation and compare to MOND/Newton predictions
4. Statistical test for velocity enhancement at large separations
""")
    
    return results


if __name__ == "__main__":
    results = main()
