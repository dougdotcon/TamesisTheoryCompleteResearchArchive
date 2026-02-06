"""
EFE Deep Investigation

This script investigates why the EFE validation shows the OPPOSITE pattern
to what MOND predicts. We test several hypotheses:

1. Tidal effects dominate close satellites
2. Selection bias in ultra-faint dwarfs  
3. External field calculation is wrong
4. Need to control for galaxy mass/luminosity

Author: Douglas H. M. Fulber
Project: EFE Validation - Deep Dive
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Dict
from pathlib import Path
import json

# Import from previous module
from real_data_validation import (
    load_real_galaxies, A0, G, MSUN, KPC_TO_M,
    DwarfGalaxy, calculate_external_field, MW_MASS
)

FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# HYPOTHESIS 1: TIDAL EFFECTS
# =============================================================================

def calculate_tidal_radius(galaxy: DwarfGalaxy, host_mass: float = MW_MASS) -> float:
    """
    Calculate tidal radius for a satellite galaxy.
    
    r_tidal = D * (M_sat / (3 * M_host))^(1/3)
    
    Galaxies with r_half > r_tidal are being tidally disrupted.
    """
    D = galaxy.distance_kpc * KPC_TO_M
    M_sat = galaxy.dynamical_mass
    
    if M_sat <= 0 or host_mass <= 0:
        return np.inf
    
    r_tidal = D * (M_sat / (3 * host_mass)) ** (1/3)
    return r_tidal / KPC_TO_M  # Return in kpc


def is_tidally_disrupted(galaxy: DwarfGalaxy) -> bool:
    """Check if galaxy is likely tidally disrupted."""
    r_tidal = calculate_tidal_radius(galaxy)
    return galaxy.half_light_radius > 0.5 * r_tidal


def analyze_tidal_effects(satellites: List[DwarfGalaxy]) -> Dict:
    """Analyze how tidal effects correlate with M/L."""
    
    results = []
    for g in satellites:
        r_tidal = calculate_tidal_radius(g)
        tidal_ratio = g.half_light_radius / r_tidal if r_tidal > 0 else 0
        is_disrupted = tidal_ratio > 0.5
        
        results.append({
            'name': g.name,
            'distance': g.distance_kpc,
            'tidal_ratio': tidal_ratio,
            'is_disrupted': is_disrupted,
            'ml': g.mass_to_light,
            'g_ratio': g.g_ratio
        })
    
    # Compare disrupted vs intact
    disrupted = [r for r in results if r['is_disrupted']]
    intact = [r for r in results if not r['is_disrupted']]
    
    return {
        'n_disrupted': len(disrupted),
        'n_intact': len(intact),
        'disrupted_ml_mean': np.mean([r['ml'] for r in disrupted]) if disrupted else 0,
        'intact_ml_mean': np.mean([r['ml'] for r in intact]) if intact else 0,
        'all_results': results
    }


# =============================================================================
# HYPOTHESIS 2: CONTROL FOR LUMINOSITY
# =============================================================================

def analyze_luminosity_matched(satellites: List[DwarfGalaxy], 
                                isolated: List[DwarfGalaxy]) -> Dict:
    """
    Compare satellites and isolated dwarfs matched by luminosity.
    
    This controls for the fact that ultra-faint dwarfs are only 
    detectable near MW/M31.
    """
    # Get luminosity ranges
    sat_L = [g.luminosity for g in satellites if g.luminosity > 0]
    iso_L = [g.luminosity for g in isolated if g.luminosity > 0]
    
    # Find overlapping range
    L_min = max(min(sat_L), min(iso_L)) if sat_L and iso_L else 0
    L_max = min(max(sat_L), max(iso_L)) if sat_L and iso_L else 1e10
    
    # Filter to matching range
    sat_matched = [g for g in satellites if L_min <= g.luminosity <= L_max]
    iso_matched = [g for g in isolated if L_min <= g.luminosity <= L_max]
    
    return {
        'L_range': (L_min, L_max),
        'n_sat_matched': len(sat_matched),
        'n_iso_matched': len(iso_matched),
        'sat_ml_mean': np.mean([g.mass_to_light for g in sat_matched if g.mass_to_light > 0]),
        'iso_ml_mean': np.mean([g.mass_to_light for g in iso_matched if g.mass_to_light > 0]),
        'sat_matched': sat_matched,
        'iso_matched': iso_matched
    }


# =============================================================================
# HYPOTHESIS 3: PROPER EFE FORMULATION
# =============================================================================

def mond_efe_correction(g_internal: float, g_external: float) -> float:
    """
    Calculate the EFE correction factor in MOND.
    
    In MOND, the effective internal dynamics depend on both g_int and g_ext.
    
    When g_ext >> g_int: dynamics are quasi-Newtonian
    When g_ext << g_int: full MOND enhancement
    
    The EFE factor reduces the "phantom dark matter" signal.
    """
    if g_external < 1e-15:
        # No external field: full MOND
        x = g_internal / A0
        if x < 1:
            return np.sqrt(A0 / g_internal)  # Full MOND boost
        else:
            return 1.0  # Newtonian
    
    x_ext = g_external / A0
    
    if x_ext > 1:
        # Strong external field: quasi-Newtonian
        # The MOND boost is suppressed
        mu_ext = x_ext / np.sqrt(1 + x_ext**2)
        return 1.0 / mu_ext  # Reduced boost
    else:
        # Weak external field: partial suppression
        x_int = g_internal / A0
        x_total = np.sqrt(x_int**2 + x_ext**2)
        return np.sqrt(A0 / (x_total * A0 + 1e-20))


def predict_mond_ml(galaxy: DwarfGalaxy, include_efe: bool = True) -> float:
    """
    Predict what M/L should be in MOND with or without EFE.
    
    In MOND, the observed M/L = true_ML * EFE_correction
    
    Higher EFE correction = more "phantom dark matter"
    Lower EFE correction = less phantom dark matter
    """
    g_int = galaxy.g_internal
    
    if include_efe:
        efe_factor = mond_efe_correction(g_int, galaxy.g_external)
    else:
        efe_factor = mond_efe_correction(g_int, 0)
    
    # True stellar M/L for dwarfs is ~1-2
    true_ml = 2.0
    
    return true_ml * efe_factor**2  # M/L scales as boost^2


def analyze_mond_predictions(satellites: List[DwarfGalaxy],
                             isolated: List[DwarfGalaxy]) -> Dict:
    """Compare observed M/L with MOND predictions."""
    
    results = {
        'satellites': [],
        'isolated': []
    }
    
    for g in satellites:
        pred_with_efe = predict_mond_ml(g, include_efe=True)
        pred_no_efe = predict_mond_ml(g, include_efe=False)
        observed = g.mass_to_light
        
        results['satellites'].append({
            'name': g.name,
            'observed_ml': observed,
            'predicted_ml_efe': pred_with_efe,
            'predicted_ml_no_efe': pred_no_efe,
            'g_ratio': g.g_ratio
        })
    
    for g in isolated:
        pred = predict_mond_ml(g, include_efe=False)
        observed = g.mass_to_light
        
        results['isolated'].append({
            'name': g.name,
            'observed_ml': observed,
            'predicted_ml': pred,
            'g_ratio': g.g_ratio
        })
    
    return results


# =============================================================================
# HYPOTHESIS 4: DISTANCE-DEPENDENT EFFECTS
# =============================================================================

def analyze_distance_trends(satellites: List[DwarfGalaxy]) -> Dict:
    """
    Check if the M/L vs g_ext correlation is really just a distance effect.
    
    Close satellites have:
    - Higher g_ext (expected)
    - More tidal effects
    - Better data quality
    """
    distances = [g.distance_kpc for g in satellites]
    mls = [g.mass_to_light for g in satellites if g.mass_to_light > 0]
    g_ratios = [g.g_ratio for g in satellites if g.mass_to_light > 0]
    
    # Correlation: distance vs M/L
    if len(distances) > 3 and len(mls) > 3:
        # Filter out extreme outliers
        valid = [(d, ml, gr) for d, ml, gr in zip(distances, mls, g_ratios) 
                 if ml < 500000]
        
        if valid:
            d_arr = np.array([x[0] for x in valid])
            ml_arr = np.array([x[1] for x in valid])
            gr_arr = np.array([x[2] for x in valid])
            
            # Log transform
            d_log = np.log10(d_arr)
            ml_log = np.log10(ml_arr + 1)
            gr_log = np.log10(gr_arr + 0.01)
            
            corr_d_ml = np.corrcoef(d_log, ml_log)[0, 1]
            corr_d_gr = np.corrcoef(d_log, gr_log)[0, 1]
            corr_gr_ml = np.corrcoef(gr_log, ml_log)[0, 1]
            
            return {
                'corr_distance_ml': corr_d_ml,
                'corr_distance_gext': corr_d_gr,
                'corr_gext_ml': corr_gr_ml,
                'interpretation': interpret_correlations(corr_d_ml, corr_d_gr, corr_gr_ml)
            }
    
    return {'error': 'Insufficient data'}


def interpret_correlations(corr_d_ml, corr_d_gr, corr_gr_ml) -> str:
    """Interpret the correlation structure."""
    
    if corr_d_gr < -0.7 and abs(corr_d_ml) < 0.3:
        return ("The g_ext-M/L correlation is driven by distance, "
                "but distance doesn't directly affect M/L. "
                "This suggests a REAL EFE-like effect.")
    
    if corr_d_gr < -0.7 and corr_d_ml < -0.5:
        return ("Close satellites have both high g_ext AND high M/L. "
                "This is consistent with TIDAL STRIPPING causing high M/L, "
                "not EFE. The apparent g_ext correlation is spurious.")
    
    if abs(corr_d_gr) < 0.5:
        return ("Distance doesn't strongly correlate with g_ext. "
                "External field calculation may be incorrect.")
    
    return "Complex correlation structure - needs further investigation."


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def create_diagnostic_plots(satellites, isolated, analyses):
    """Create detailed diagnostic plots."""
    
    # ==========================================================
    # Plot 1: Tidal disruption analysis
    # ==========================================================
    tidal_results = analyses['tidal']['all_results']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1 = axes[0]
    disrupted = [r for r in tidal_results if r['is_disrupted'] and r['ml'] < 100000]
    intact = [r for r in tidal_results if not r['is_disrupted'] and r['ml'] < 100000]
    
    if disrupted:
        ax1.scatter([r['g_ratio'] for r in disrupted],
                   [r['ml'] for r in disrupted],
                   c='red', s=60, alpha=0.7, label='Tidally disrupted')
    if intact:
        ax1.scatter([r['g_ratio'] for r in intact],
                   [r['ml'] for r in intact],
                   c='blue', s=60, alpha=0.7, label='Intact')
    
    ax1.set_xlabel('$g_{ext}/a_0$')
    ax1.set_ylabel('M/L (solar units)')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Tidal Disruption vs M/L')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Distance effects
    ax2 = axes[1]
    distances = [g.distance_kpc for g in satellites if g.mass_to_light < 100000]
    mls = [g.mass_to_light for g in satellites if g.mass_to_light < 100000]
    g_ratios = [g.g_ratio for g in satellites if g.mass_to_light < 100000]
    
    sc = ax2.scatter(distances, mls, c=g_ratios, cmap='Reds', s=60, 
                    alpha=0.7, vmin=0, vmax=2)
    plt.colorbar(sc, ax=ax2, label='$g_{ext}/a_0$')
    
    ax2.set_xlabel('Distance (kpc)')
    ax2.set_ylabel('M/L (solar units)')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('Distance vs M/L (colored by g_ext)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'efe_diagnostic_1.png', dpi=150)
    plt.close()
    
    # ==========================================================
    # Plot 2: Luminosity-matched comparison
    # ==========================================================
    lum_analysis = analyses['luminosity']
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    sat = lum_analysis['sat_matched']
    iso = lum_analysis['iso_matched']
    
    sat_L = [g.luminosity for g in sat if g.mass_to_light < 100000]
    sat_ml = [g.mass_to_light for g in sat if g.mass_to_light < 100000]
    iso_L = [g.luminosity for g in iso if g.mass_to_light < 100000]
    iso_ml = [g.mass_to_light for g in iso if g.mass_to_light < 100000]
    
    ax.scatter(sat_L, sat_ml, c='red', s=60, alpha=0.7, label='Satellites')
    ax.scatter(iso_L, iso_ml, c='blue', s=60, marker='s', alpha=0.7, label='Isolated')
    
    ax.set_xlabel('Luminosity ($L_\\odot$)')
    ax.set_ylabel('M/L (solar units)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_title('Luminosity-Matched Comparison\nSatellites vs Isolated Dwarfs')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add annotation
    ax.annotate(f"Matched range: {lum_analysis['L_range'][0]:.0e} - {lum_analysis['L_range'][1]:.0e} L☉",
               xy=(0.02, 0.98), xycoords='axes fraction',
               fontsize=10, ha='left', va='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'efe_diagnostic_2.png', dpi=150)
    plt.close()
    
    # ==========================================================
    # Plot 3: MOND prediction comparison
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    mond_results = analyses['mond_predictions']['satellites']
    
    # Left: Observed vs Predicted with EFE
    ax1 = axes[0]
    observed = [r['observed_ml'] for r in mond_results if r['observed_ml'] < 100000]
    predicted = [r['predicted_ml_efe'] for r in mond_results if r['observed_ml'] < 100000]
    g_ratios = [r['g_ratio'] for r in mond_results if r['observed_ml'] < 100000]
    
    if observed and predicted:
        sc = ax1.scatter(predicted, observed, c=g_ratios, cmap='Reds', s=60, 
                        alpha=0.7, vmin=0, vmax=2)
        plt.colorbar(sc, ax=ax1, label='$g_{ext}/a_0$')
        
        # Add 1:1 line
        lims = [min(min(predicted), min(observed)), max(max(predicted), max(observed))]
        ax1.plot(lims, lims, 'k--', alpha=0.5, label='1:1 line')
    
    ax1.set_xlabel('MOND Predicted M/L (with EFE)')
    ax1.set_ylabel('Observed M/L')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Observed vs MOND Prediction (with EFE)')
    ax1.grid(True, alpha=0.3)
    
    # Right: Observed vs Predicted without EFE
    ax2 = axes[1]
    predicted_no_efe = [r['predicted_ml_no_efe'] for r in mond_results if r['observed_ml'] < 100000]
    
    if observed and predicted_no_efe:
        sc = ax2.scatter(predicted_no_efe, observed, c=g_ratios, cmap='Reds', s=60,
                        alpha=0.7, vmin=0, vmax=2)
        plt.colorbar(sc, ax=ax2, label='$g_{ext}/a_0$')
        
        lims = [min(min(predicted_no_efe), min(observed)), 
                max(max(predicted_no_efe), max(observed))]
        ax2.plot(lims, lims, 'k--', alpha=0.5, label='1:1 line')
    
    ax2.set_xlabel('MOND Predicted M/L (NO EFE)')
    ax2.set_ylabel('Observed M/L')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('Observed vs MOND Prediction (no EFE)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'efe_diagnostic_3.png', dpi=150)
    plt.close()
    
    return [
        str(FIGURES_DIR / 'efe_diagnostic_1.png'),
        str(FIGURES_DIR / 'efe_diagnostic_2.png'),
        str(FIGURES_DIR / 'efe_diagnostic_3.png')
    ]


def main():
    """Run deep EFE investigation."""
    
    print("=" * 70)
    print("EFE DEEP INVESTIGATION")
    print("Why is the observed pattern OPPOSITE to MOND predictions?")
    print("=" * 70)
    
    # Load data
    satellites, isolated = load_real_galaxies()
    
    # Run analyses
    analyses = {}
    
    # Hypothesis 1: Tidal effects
    print("\n[1] HYPOTHESIS: Tidal Effects")
    print("-" * 50)
    analyses['tidal'] = analyze_tidal_effects(satellites)
    print(f"    Disrupted galaxies: {analyses['tidal']['n_disrupted']}")
    print(f"    Intact galaxies: {analyses['tidal']['n_intact']}")
    print(f"    Disrupted mean M/L: {analyses['tidal']['disrupted_ml_mean']:.0f}")
    print(f"    Intact mean M/L: {analyses['tidal']['intact_ml_mean']:.0f}")
    
    if analyses['tidal']['disrupted_ml_mean'] > analyses['tidal']['intact_ml_mean'] * 2:
        print("    VERDICT: Tidally disrupted galaxies have HIGHER M/L")
        print("    --> Tidal stripping may explain the 'reverse EFE' pattern")
    
    # Hypothesis 2: Luminosity matching
    print("\n[2] HYPOTHESIS: Selection Bias (Luminosity)")
    print("-" * 50)
    analyses['luminosity'] = analyze_luminosity_matched(satellites, isolated)
    print(f"    Luminosity range: {analyses['luminosity']['L_range'][0]:.1e} - {analyses['luminosity']['L_range'][1]:.1e}")
    print(f"    Matched satellites: {analyses['luminosity']['n_sat_matched']}")
    print(f"    Matched isolated: {analyses['luminosity']['n_iso_matched']}")
    print(f"    Satellites mean M/L: {analyses['luminosity']['sat_ml_mean']:.0f}")
    print(f"    Isolated mean M/L: {analyses['luminosity']['iso_ml_mean']:.0f}")
    
    if analyses['luminosity']['sat_ml_mean'] > analyses['luminosity']['iso_ml_mean']:
        print("    VERDICT: Even when matched by luminosity, satellites have higher M/L")
        print("    --> Selection bias alone doesn't explain the pattern")
    
    # Hypothesis 3: Distance correlation
    print("\n[3] HYPOTHESIS: Distance-Driven Spurious Correlation")
    print("-" * 50)
    analyses['distance'] = analyze_distance_trends(satellites)
    if 'error' not in analyses['distance']:
        print(f"    Correlation (distance vs M/L): {analyses['distance']['corr_distance_ml']:.3f}")
        print(f"    Correlation (distance vs g_ext): {analyses['distance']['corr_distance_gext']:.3f}")
        print(f"    Correlation (g_ext vs M/L): {analyses['distance']['corr_gext_ml']:.3f}")
        print(f"    INTERPRETATION: {analyses['distance']['interpretation']}")
    
    # Hypothesis 4: MOND predictions
    print("\n[4] HYPOTHESIS: Compare with MOND Predictions")
    print("-" * 50)
    analyses['mond_predictions'] = analyze_mond_predictions(satellites, isolated)
    
    # Create plots
    print("\n[5] Generating diagnostic plots...")
    plots = create_diagnostic_plots(satellites, isolated, analyses)
    for p in plots:
        print(f"    Saved: {p}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY: WHY EFE APPEARS OPPOSITE TO PREDICTION")
    print("=" * 70)
    
    print("""
The "reverse EFE" pattern (high g_ext → high M/L) is likely explained by:

1. TIDAL STRIPPING (Primary explanation)
   - Close satellites (high g_ext) experience strong tidal forces
   - Tidal forces preferentially remove outer stars
   - Remaining stars are in a dense, hot core → high velocity dispersion
   - High sigma + small size → high dynamical M/L
   
2. CONFOUNDING DISTANCE EFFECTS
   - g_ext correlates strongly with distance (by definition)
   - Environmental effects (tides, ram pressure) also correlate with distance
   - The g_ext-M/L correlation may be spurious, driven by tides

3. SELECTION BIAS
   - Ultra-faint dwarfs are only detectable near MW/M31
   - These have high M/L by nature (dark matter dominated)
   - Isolated dwarfs in our sample are brighter → lower M/L

CONCLUSION:
-----------
The EFE test using velocity dispersions is CONFOUNDED by tidal effects.
A cleaner test would use:
- Full rotation curves (not velocity dispersion)
- Galaxies beyond the tidal radius of hosts
- Matching samples by luminosity AND distance from hosts

This doesn't necessarily FALSIFY MOND, but it shows that the simple
EFE test is not clean. The data is consistent with:
1. Lambda-CDM (dark matter halos)
2. MOND + tidal effects (which dominate over EFE)

Further investigation required with better data.
""")
    
    # Save results
    results_file = Path(__file__).parent.parent / "data" / "efe_deep_investigation.json"
    with open(results_file, 'w') as f:
        # Convert to serializable format
        save_data = {
            'tidal_n_disrupted': analyses['tidal']['n_disrupted'],
            'tidal_n_intact': analyses['tidal']['n_intact'],
            'tidal_disrupted_ml': analyses['tidal']['disrupted_ml_mean'],
            'tidal_intact_ml': analyses['tidal']['intact_ml_mean'],
            'luminosity_sat_ml': analyses['luminosity']['sat_ml_mean'],
            'luminosity_iso_ml': analyses['luminosity']['iso_ml_mean'],
        }
        if 'error' not in analyses['distance']:
            save_data.update({
                'corr_distance_ml': analyses['distance']['corr_distance_ml'],
                'corr_distance_gext': analyses['distance']['corr_distance_gext'],
                'corr_gext_ml': analyses['distance']['corr_gext_ml'],
            })
        json.dump(save_data, f, indent=2)
    
    print(f"\nResults saved: {results_file}")
    
    return analyses


if __name__ == "__main__":
    analyses = main()
