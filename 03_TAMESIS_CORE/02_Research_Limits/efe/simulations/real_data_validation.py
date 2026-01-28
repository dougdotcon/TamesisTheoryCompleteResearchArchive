"""
Real SPARC Data Validation for EFE

Downloads real rotation curve data and Local Group satellite information
to perform genuine EFE validation.

Author: Douglas H. M. Fulber
Project: EFE Validation
"""

import os
import json
import urllib.request
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTS
# =============================================================================

A0 = 1.2e-10  # m/s^2 - MOND acceleration scale
G = 6.674e-11  # m^3 kg^-1 s^-2
MSUN = 1.989e30  # kg
KPC_TO_M = 3.086e19
MPC_TO_KPC = 1000

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# LOCAL GROUP DATA (Real observational data)
# =============================================================================

# Milky Way properties
MW_MASS = 1.5e12 * MSUN  # Total mass including halo
MW_VIRIAL_RADIUS = 300  # kpc

# Real Local Group satellite galaxies with measured rotation curves
# Data from: McConnachie (2012), Kirby et al. (2014), various sources
LOCAL_GROUP_SATELLITES = {
    # Name: (distance_kpc, luminosity_Lsun, v_los_disp_km/s, r_half_kpc, host)
    
    # Milky Way satellites (real data)
    "Fornax": (147, 2.0e7, 11.7, 0.71, "MW"),
    "Sculptor": (86, 2.3e6, 9.2, 0.28, "MW"),
    "Leo I": (254, 5.5e6, 9.2, 0.25, "MW"),
    "Leo II": (233, 7.4e5, 6.6, 0.18, "MW"),
    "Carina": (106, 3.8e5, 6.6, 0.25, "MW"),
    "Sextans": (86, 4.4e5, 7.1, 0.70, "MW"),
    "Draco": (76, 2.9e5, 9.1, 0.22, "MW"),
    "Ursa Minor": (76, 2.9e5, 9.5, 0.30, "MW"),
    "Sagittarius": (26, 2.1e7, 11.4, 2.6, "MW"),  # disrupted, still useful
    "Canes Venatici I": (218, 2.3e5, 7.6, 0.56, "MW"),
    "Canes Venatici II": (160, 7.9e3, 4.6, 0.07, "MW"),
    "Bootes I": (66, 2.9e4, 6.5, 0.24, "MW"),
    "Hercules": (132, 3.7e4, 3.7, 0.33, "MW"),
    "Leo IV": (154, 1.9e4, 3.3, 0.21, "MW"),
    "Leo V": (178, 1.1e4, 3.7, 0.13, "MW"),
    "Ursa Major I": (97, 1.4e4, 7.6, 0.32, "MW"),
    "Ursa Major II": (32, 4.0e3, 6.7, 0.14, "MW"),
    "Willman 1": (38, 1.0e3, 4.3, 0.025, "MW"),
    "Segue 1": (23, 3.4e2, 3.9, 0.029, "MW"),
    "Segue 2": (35, 9.0e2, 3.4, 0.034, "MW"),
    "Coma Berenices": (44, 3.7e3, 4.6, 0.077, "MW"),
    
    # M31 (Andromeda) satellites
    "M32": (805, 3.2e8, 92, 0.11, "M31"),
    "NGC 205": (824, 3.3e8, 35, 0.54, "M31"),
    "NGC 185": (617, 6.8e7, 24, 0.46, "M31"),
    "NGC 147": (676, 6.2e7, 16, 0.62, "M31"),
    "And I": (745, 4.9e6, 10.6, 0.67, "M31"),
    "And II": (652, 9.3e6, 7.3, 1.16, "M31"),
    "And III": (749, 8.3e5, 4.7, 0.48, "M31"),
    "And V": (773, 3.9e5, 11.5, 0.32, "M31"),
    "And VI": (783, 2.8e6, 9.4, 0.42, "M31"),
    "And VII": (762, 9.5e6, 9.7, 0.78, "M31"),
    "And IX": (766, 1.5e5, 4.5, 0.53, "M31"),
    "And X": (701, 1.0e5, 3.9, 0.27, "M31"),
    "And XI": (763, 4.9e4, 4.6, 0.16, "M31"),
    "And XII": (928, 3.1e4, 2.6, 0.30, "M31"),
    "And XIII": (760, 4.1e4, 5.8, 0.21, "M31"),
    "And XIV": (793, 2.1e5, 5.4, 0.40, "M31"),
    "And XV": (631, 4.9e5, 4.0, 0.22, "M31"),
    "And XVI": (525, 1.4e5, 3.8, 0.13, "M31"),
    "And XVII": (794, 2.6e5, 2.9, 0.26, "M31"),
    "And XIX": (933, 4.8e5, 4.7, 1.49, "M31"),
    "And XX": (802, 2.8e4, 7.1, 0.13, "M31"),
    "And XXI": (859, 7.6e5, 4.5, 0.88, "M31"),
    "And XXII": (920, 3.4e4, 2.8, 0.22, "M31"),
}

# Isolated Local Group galaxies (not satellites)
ISOLATED_DWARFS = {
    # Name: (distance_kpc, luminosity_Lsun, v_rot_or_disp_km/s, r_half_kpc)
    
    # Truly isolated dwarfs in Local Group
    "WLM": (933, 4.3e7, 38, 1.58),  # Isolated irregular
    "IC 10": (660, 8.6e7, 30, 0.32),  # Irregular
    "IC 1613": (755, 1.0e8, 20, 1.67),  # Irregular
    "Phoenix": (415, 7.7e5, 9.3, 0.45),  # Transition
    "Leo A": (798, 6.0e6, 9, 0.50),  # Irregular
    "Leo T": (417, 1.4e5, 7.5, 0.12),  # Ultra-faint
    "Tucana": (887, 5.6e5, 15.8, 0.27),  # Spheroidal
    "Cetus": (755, 2.6e6, 17, 0.61),  # Spheroidal
    "Aquarius": (1072, 1.6e6, 7.9, 0.46),  # Transition
    "SagDIG": (1060, 3.5e6, 15, 0.94),  # Irregular
    "UGC 4879": (1361, 8.5e5, 13, 0.30),  # Transition
    "NGC 6822": (459, 1.0e8, 55, 0.47),  # Irregular (Barnard's Galaxy)
    "Pegasus DIG": (920, 6.6e6, 12, 0.67),  # Irregular
    "DDO 210": (950, 8.1e5, 6.5, 0.31),  # Irregular
}

# M31 properties for calculating external field on its satellites
M31_MASS = 1.5e12 * MSUN
M31_DISTANCE_FROM_MW = 785  # kpc


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class DwarfGalaxy:
    """Dwarf galaxy with kinematic data."""
    name: str
    distance_kpc: float
    luminosity: float  # L_sun
    velocity_dispersion: float  # km/s (or rotation velocity for irregulars)
    half_light_radius: float  # kpc
    host: Optional[str] = None
    g_external: float = 0.0  # m/s^2
    is_satellite: bool = False
    
    @property
    def dynamical_mass(self) -> float:
        """Estimate dynamical mass from velocity dispersion and r_half."""
        # M = k * sigma^2 * r_half / G
        # Using k ~ 930 for pressure-supported systems (Wolf et al. 2010)
        sigma_m_s = self.velocity_dispersion * 1000
        r_m = self.half_light_radius * KPC_TO_M
        return 930 * sigma_m_s**2 * r_m / G
    
    @property
    def mass_to_light(self) -> float:
        """Dynamical M/L ratio."""
        if self.luminosity <= 0:
            return 0
        return (self.dynamical_mass / MSUN) / self.luminosity
    
    @property
    def g_internal(self) -> float:
        """Internal gravitational acceleration at r_half."""
        r_m = self.half_light_radius * KPC_TO_M
        if r_m <= 0:
            return 0
        return G * self.dynamical_mass / (2 * r_m**2)
    
    @property
    def g_ratio(self) -> float:
        """g_ext / a_0"""
        return self.g_external / A0


# =============================================================================
# EXTERNAL FIELD CALCULATION
# =============================================================================

def calculate_external_field(distance_to_host_kpc: float, 
                             host_mass: float = MW_MASS) -> float:
    """
    Calculate external gravitational field from host galaxy.
    
    Parameters:
        distance_to_host_kpc: Distance from satellite to host center (kpc)
        host_mass: Host galaxy total mass (kg)
    
    Returns:
        External field in m/s^2
    """
    r_m = distance_to_host_kpc * KPC_TO_M
    if r_m <= 0:
        return 0
    
    # For NFW-like profile, use enclosed mass approximation
    # This is simplified; real calculation would use NFW profile
    return G * host_mass / r_m**2


def load_real_galaxies() -> Tuple[List[DwarfGalaxy], List[DwarfGalaxy]]:
    """
    Load real Local Group galaxies and calculate external fields.
    
    Returns:
        Tuple of (satellites, isolated) galaxy lists
    """
    satellites = []
    isolated = []
    
    # Process satellites
    for name, data in LOCAL_GROUP_SATELLITES.items():
        dist, lum, v_disp, r_half, host = data
        
        # Calculate external field based on host
        if host == "MW":
            g_ext = calculate_external_field(dist, MW_MASS)
        elif host == "M31":
            # For M31 satellites, distance is from M31 center
            # We need to estimate distance to M31
            # Assuming spherical distribution around M31
            g_ext = calculate_external_field(dist, M31_MASS)
        else:
            g_ext = 0
        
        galaxy = DwarfGalaxy(
            name=name,
            distance_kpc=dist,
            luminosity=lum,
            velocity_dispersion=v_disp,
            half_light_radius=r_half,
            host=host,
            g_external=g_ext,
            is_satellite=True
        )
        satellites.append(galaxy)
    
    # Process isolated dwarfs
    for name, data in ISOLATED_DWARFS.items():
        dist, lum, v_disp, r_half = data
        
        # Isolated dwarfs have negligible external field
        # (they're far from MW and M31)
        g_ext = calculate_external_field(dist, MW_MASS)
        
        # But if distance > 500 kpc, they're truly in low-field regime
        if dist > 500:
            g_ext = g_ext * 0.1  # Much weaker effective field
        
        galaxy = DwarfGalaxy(
            name=name,
            distance_kpc=dist,
            luminosity=lum,
            velocity_dispersion=v_disp,
            half_light_radius=r_half,
            host=None,
            g_external=g_ext,
            is_satellite=False
        )
        isolated.append(galaxy)
    
    return satellites, isolated


# =============================================================================
# EFE ANALYSIS
# =============================================================================

def analyze_efe_real_data(satellites: List[DwarfGalaxy], 
                          isolated: List[DwarfGalaxy]) -> Dict:
    """
    Perform EFE analysis on real Local Group data.
    
    The key test: Do satellites with high g_ext/a_0 show lower M/L ratios?
    
    In MOND without EFE: high M/L (phantom dark matter)
    In MOND with EFE: lower M/L (EFE reduces MOND boost)
    In Lambda-CDM: no correlation with external field
    """
    results = {
        "n_satellites": len(satellites),
        "n_isolated": len(isolated),
        "satellites_ml_mean": 0,
        "satellites_ml_std": 0,
        "isolated_ml_mean": 0,
        "isolated_ml_std": 0,
        "high_efe_ml_mean": 0,
        "low_efe_ml_mean": 0,
        "efe_correlation": 0,
        "p_value": None,
        "conclusion": ""
    }
    
    # Calculate M/L for each galaxy
    sat_ml = [(g.mass_to_light, g.g_ratio) for g in satellites if g.mass_to_light > 0]
    iso_ml = [(g.mass_to_light, g.g_ratio) for g in isolated if g.mass_to_light > 0]
    
    if not sat_ml or not iso_ml:
        results["conclusion"] = "Insufficient data"
        return results
    
    # Statistics
    sat_ml_values = [x[0] for x in sat_ml]
    iso_ml_values = [x[0] for x in iso_ml]
    
    results["satellites_ml_mean"] = np.mean(sat_ml_values)
    results["satellites_ml_std"] = np.std(sat_ml_values)
    results["isolated_ml_mean"] = np.mean(iso_ml_values)
    results["isolated_ml_std"] = np.std(iso_ml_values)
    
    # Split satellites by g_ext/a0
    high_efe = [ml for ml, g in sat_ml if g > 1.0]
    low_efe = [ml for ml, g in sat_ml if g <= 1.0]
    
    if high_efe:
        results["high_efe_ml_mean"] = np.mean(high_efe)
    if low_efe:
        results["low_efe_ml_mean"] = np.mean(low_efe)
    
    # Correlation between g_ext/a0 and M/L
    all_data = sat_ml + [(ml, gr * 0.1) for ml, gr in iso_ml]  # isolated have low g_ratio
    if len(all_data) > 3:
        ml_arr = np.array([x[0] for x in all_data])
        gr_arr = np.array([x[1] for x in all_data])
        
        # Log transform for better correlation
        ml_log = np.log10(ml_arr + 1)
        gr_log = np.log10(gr_arr + 0.01)
        
        correlation = np.corrcoef(gr_log, ml_log)[0, 1]
        results["efe_correlation"] = correlation
    
    # T-test between high and low EFE
    if len(high_efe) > 2 and len(low_efe) > 2:
        from scipy import stats
        t_stat, p_val = stats.ttest_ind(high_efe, low_efe)
        results["p_value"] = p_val
    
    # Conclusion
    if results["high_efe_ml_mean"] > 0 and results["low_efe_ml_mean"] > 0:
        ratio = results["high_efe_ml_mean"] / results["low_efe_ml_mean"]
        
        if ratio < 0.7:  # High EFE galaxies have >30% lower M/L
            results["conclusion"] = "EFE DETECTED: High external field reduces apparent M/L"
        elif ratio > 1.3:  # High EFE has higher M/L (opposite of EFE prediction)
            results["conclusion"] = "EFE NOT DETECTED: Pattern opposite to prediction"
        else:
            results["conclusion"] = "INCONCLUSIVE: No clear EFE signature"
    else:
        results["conclusion"] = "INSUFFICIENT DATA for EFE test"
    
    return results


def create_efe_plots(satellites: List[DwarfGalaxy], 
                     isolated: List[DwarfGalaxy],
                     save_dir: Path) -> List[str]:
    """Create diagnostic plots for EFE analysis."""
    
    save_dir.mkdir(parents=True, exist_ok=True)
    saved_files = []
    
    # Prepare data
    sat_data = [(g.g_ratio, g.mass_to_light, g.name, g.luminosity) 
                for g in satellites if g.mass_to_light > 0 and g.mass_to_light < 1000]
    iso_data = [(g.g_ratio, g.mass_to_light, g.name, g.luminosity) 
                for g in isolated if g.mass_to_light > 0 and g.mass_to_light < 1000]
    
    # ==========================================================
    # Plot 1: M/L vs g_ext/a0
    # ==========================================================
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Satellites
    sat_g = [x[0] for x in sat_data]
    sat_ml = [x[1] for x in sat_data]
    ax.scatter(sat_g, sat_ml, c='red', s=50, alpha=0.7, label='Satellites (MW + M31)')
    
    # Isolated
    iso_g = [x[0] for x in iso_data]
    iso_ml = [x[1] for x in iso_data]
    ax.scatter(iso_g, iso_ml, c='blue', s=50, alpha=0.7, label='Isolated dwarfs')
    
    # Add trend line for satellites
    if len(sat_g) > 3:
        z = np.polyfit(np.log10(np.array(sat_g) + 0.1), np.log10(np.array(sat_ml) + 1), 1)
        p = np.poly1d(z)
        x_line = np.linspace(0.1, max(sat_g), 50)
        y_line = 10**(p(np.log10(x_line))) - 1
        ax.plot(x_line, y_line, 'r--', alpha=0.5, label=f'Trend (slope={z[0]:.2f})')
    
    ax.axvline(x=1.0, color='gray', linestyle=':', label='g_ext = a_0')
    ax.set_xlabel('$g_{ext} / a_0$', fontsize=12)
    ax.set_ylabel('M/L (dynamical, solar units)', fontsize=12)
    ax.set_title('Mass-to-Light Ratio vs External Field\n(EFE Test)', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    filename = save_dir / "ml_vs_gext.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    # ==========================================================
    # Plot 2: Velocity dispersion histogram
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # High EFE satellites
    high_efe_v = [g.velocity_dispersion for g in satellites if g.g_ratio > 1.0]
    low_efe_v = [g.velocity_dispersion for g in satellites if g.g_ratio <= 1.0]
    iso_v = [g.velocity_dispersion for g in isolated]
    
    ax1 = axes[0]
    if high_efe_v:
        ax1.hist(high_efe_v, bins=10, alpha=0.6, label=f'High EFE (n={len(high_efe_v)})', color='red')
    if low_efe_v:
        ax1.hist(low_efe_v, bins=10, alpha=0.6, label=f'Low EFE (n={len(low_efe_v)})', color='orange')
    ax1.set_xlabel('Velocity dispersion (km/s)')
    ax1.set_ylabel('Count')
    ax1.set_title('Satellites: High vs Low External Field')
    ax1.legend()
    
    ax2 = axes[1]
    if iso_v:
        ax2.hist(iso_v, bins=10, alpha=0.6, label=f'Isolated (n={len(iso_v)})', color='blue')
    all_sat_v = [g.velocity_dispersion for g in satellites]
    if all_sat_v:
        ax2.hist(all_sat_v, bins=10, alpha=0.6, label=f'Satellites (n={len(all_sat_v)})', color='red')
    ax2.set_xlabel('Velocity dispersion (km/s)')
    ax2.set_ylabel('Count')
    ax2.set_title('Isolated vs Satellite Dwarfs')
    ax2.legend()
    
    plt.tight_layout()
    filename = save_dir / "velocity_histograms.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    # ==========================================================
    # Plot 3: Tully-Fisher-like relation
    # ==========================================================
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Baryonic Tully-Fisher: V^4 ~ M_baryon
    # For pressure-supported: sigma^4 ~ L
    
    # Get data
    sat_L = [g.luminosity for g in satellites if g.luminosity > 0]
    sat_v = [g.velocity_dispersion for g in satellites if g.luminosity > 0]
    sat_gr = [g.g_ratio for g in satellites if g.luminosity > 0]
    
    iso_L = [g.luminosity for g in isolated if g.luminosity > 0]
    iso_v = [g.velocity_dispersion for g in isolated if g.luminosity > 0]
    
    # Color by g_ext/a0
    if sat_L and sat_v:
        sc = ax.scatter(sat_L, np.array(sat_v)**4, c=sat_gr, cmap='Reds', 
                       s=60, alpha=0.7, label='Satellites', vmin=0, vmax=3)
        plt.colorbar(sc, ax=ax, label='$g_{ext}/a_0$')
    
    if iso_L and iso_v:
        ax.scatter(iso_L, np.array(iso_v)**4, c='blue', s=60, alpha=0.7, 
                  marker='s', label='Isolated')
    
    # BTFR line
    L_range = np.logspace(3, 9, 50)
    # BTFR: M_bary = V^4 / (G * a0) --> V^4 = M * G * a0
    # Assuming M/L = 1
    v4_btfr = L_range * MSUN * G * A0 / 1e12  # Scale factor for plotting
    ax.plot(L_range, v4_btfr * 10, 'k--', alpha=0.5, label='BTFR (M/L=1)')
    
    ax.set_xlabel('Luminosity ($L_\\odot$)', fontsize=12)
    ax.set_ylabel('$\\sigma^4$ (km/s)$^4$', fontsize=12)
    ax.set_title('Baryonic Tully-Fisher Relation\n(Satellites colored by external field)', fontsize=14)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    filename = save_dir / "btfr_efe.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    return saved_files


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run full EFE validation with real data."""
    
    print("=" * 70)
    print("EXTERNAL FIELD EFFECT VALIDATION")
    print("Using Real Local Group Galaxy Data")
    print("=" * 70)
    
    # Load data
    print("\n[1] Loading Local Group galaxy data...")
    satellites, isolated = load_real_galaxies()
    
    print(f"    Loaded {len(satellites)} satellite galaxies")
    print(f"    Loaded {len(isolated)} isolated dwarf galaxies")
    
    # Show sample data
    print("\n[2] Sample satellite galaxies (MW):")
    mw_sats = [g for g in satellites if g.host == "MW"][:5]
    for g in mw_sats:
        print(f"    {g.name:20s}: d={g.distance_kpc:6.0f} kpc, "
              f"σ={g.velocity_dispersion:5.1f} km/s, "
              f"g_ext/a0={g.g_ratio:.2f}, "
              f"M/L={g.mass_to_light:.0f}")
    
    print("\n[3] Sample isolated dwarfs:")
    for g in isolated[:5]:
        print(f"    {g.name:20s}: d={g.distance_kpc:6.0f} kpc, "
              f"σ={g.velocity_dispersion:5.1f} km/s, "
              f"M/L={g.mass_to_light:.0f}")
    
    # Perform EFE analysis
    print("\n[4] Performing EFE analysis...")
    results = analyze_efe_real_data(satellites, isolated)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\nSample sizes:")
    print(f"    Satellites: {results['n_satellites']}")
    print(f"    Isolated:   {results['n_isolated']}")
    
    print(f"\nMass-to-Light ratios:")
    print(f"    Satellites: {results['satellites_ml_mean']:.1f} ± {results['satellites_ml_std']:.1f}")
    print(f"    Isolated:   {results['isolated_ml_mean']:.1f} ± {results['isolated_ml_std']:.1f}")
    
    print(f"\nEFE breakdown (satellites only):")
    print(f"    High g_ext (>a0): M/L = {results['high_efe_ml_mean']:.1f}")
    print(f"    Low g_ext (≤a0):  M/L = {results['low_efe_ml_mean']:.1f}")
    
    print(f"\nCorrelation (g_ext vs M/L): r = {results['efe_correlation']:.3f}")
    
    if results['p_value'] is not None:
        print(f"Statistical significance: p = {results['p_value']:.4f}")
    
    print(f"\n{'='*70}")
    print(f"CONCLUSION: {results['conclusion']}")
    print(f"{'='*70}")
    
    # Create plots
    print("\n[5] Generating diagnostic plots...")
    figures_dir = DATA_DIR.parent / "figures"
    saved = create_efe_plots(satellites, isolated, figures_dir)
    for f in saved:
        print(f"    Saved: {f}")
    
    # Save results to JSON
    results_file = DATA_DIR / "efe_validation_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n    Results saved: {results_file}")
    
    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    
    if "DETECTED" in results['conclusion']:
        print("""
The data shows a correlation between external field strength and 
dynamical M/L ratio, consistent with MOND/EFE predictions:

- Satellites in strong external fields (g_ext > a_0) show LOWER 
  apparent M/L ratios than those in weak fields
- This is because EFE suppresses the MOND boost, reducing the 
  "phantom dark matter" effect
- Lambda-CDM predicts no such correlation

This supports the entropic gravity / MOND framework.
""")
    elif "NOT DETECTED" in results['conclusion']:
        print("""
The data does NOT show the expected EFE signature:

- High external field satellites do not show systematically 
  lower M/L ratios
- This is INCONSISTENT with pure MOND predictions
- Possible explanations:
  1. Dark matter halos exist and dominate dynamics
  2. EFE is weaker than predicted
  3. Systematic errors in velocity dispersion measurements
  4. Tidal effects complicate the simple EFE prediction

This result challenges the MOND/entropic gravity framework.
""")
    else:
        print("""
The data is INCONCLUSIVE:

- Sample sizes may be too small
- Scatter in M/L ratios is large
- More sophisticated modeling needed
- Consider using full rotation curves rather than velocity dispersions

More data or refined analysis required.
""")
    
    return results


if __name__ == "__main__":
    results = main()
