"""
EFE Clean Test: Field Galaxies vs Cluster Galaxies

This is a CLEANER test of the External Field Effect that avoids the
confounds found in the Local Group velocity dispersion analysis.

Key improvements:
1. Uses full rotation curves (not velocity dispersions)
2. Compares field galaxies (low g_ext) vs cluster galaxies (high g_ext)
3. Matches samples by baryonic mass and morphology
4. Looks for declining rotation curves as specific EFE signature

The EFE predicts:
- Field galaxies: flat rotation curves (full MOND enhancement)
- Cluster galaxies: DECLINING rotation curves (EFE suppresses MOND)

This is a unique prediction that Lambda-CDM CANNOT easily explain.

Author: Douglas H. M. Fulber
Project: EFE Validation - Clean Test
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json

# Import MOND calculator
from mond_efe import MONDCalculator, GalaxyModel, A0, G, MSUN, KPC_TO_M

FIGURES_DIR = Path(__file__).parent.parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# CLUSTER ENVIRONMENTS
# =============================================================================

# Typical cluster parameters
CLUSTER_ENVIRONMENTS = {
    "Virgo": {
        "mass": 1.2e14 * MSUN,  # Total cluster mass
        "r_virial": 1500,  # kpc
        "g_center": 3.0e-10,  # m/s^2 at center
        "distance": 16.5,  # Mpc from MW
    },
    "Coma": {
        "mass": 1.0e15 * MSUN,
        "r_virial": 2000,
        "g_center": 8.0e-10,
        "distance": 100,
    },
    "Fornax_Cluster": {
        "mass": 7.0e13 * MSUN,
        "r_virial": 700,
        "g_center": 2.5e-10,
        "distance": 19,
    },
}

# Field galaxy environments
FIELD_ENVIRONMENTS = {
    "True_Field": {
        "g_ext": 0.01e-10,  # Essentially zero
        "description": "Isolated field galaxy",
    },
    "Group": {
        "g_ext": 0.3e-10,  # Low external field
        "description": "Galaxy in loose group",
    },
}


# =============================================================================
# GALAXY SAMPLES
# =============================================================================

@dataclass
class RotationCurveGalaxy:
    """Galaxy with full rotation curve data."""
    name: str
    environment: str
    baryonic_mass: float  # M_sun
    disk_scale_length: float  # kpc
    max_radius: float  # kpc
    g_external: float  # m/s^2
    is_cluster: bool
    
    # Observed rotation curve (to be generated or loaded)
    radii: np.ndarray = field(default_factory=lambda: np.array([]))
    v_observed: np.ndarray = field(default_factory=lambda: np.array([]))
    v_error: np.ndarray = field(default_factory=lambda: np.array([]))
    
    @property
    def g_ratio(self) -> float:
        return self.g_external / A0


def generate_sample_galaxies() -> Tuple[List[RotationCurveGalaxy], List[RotationCurveGalaxy]]:
    """
    Generate matched samples of field and cluster galaxies.
    
    We create galaxies with identical baryonic properties but different
    external fields, to isolate the EFE effect.
    """
    field_galaxies = []
    cluster_galaxies = []
    
    # Mass range to sample (log-uniform)
    masses = [1e9, 3e9, 1e10, 3e10, 1e11]  # M_sun
    
    # Scale length relation: h ~ 3 kpc * (M / 10^10)^0.3
    def scale_length(mass):
        return 3.0 * (mass / 1e10) ** 0.3
    
    for i, mass in enumerate(masses):
        h = scale_length(mass)
        r_max = 6 * h  # Observe out to 6 scale lengths
        
        # Field galaxy
        field_gal = RotationCurveGalaxy(
            name=f"Field_{i+1}",
            environment="True_Field",
            baryonic_mass=mass,
            disk_scale_length=h,
            max_radius=r_max,
            g_external=0.01e-10,  # Negligible
            is_cluster=False
        )
        field_galaxies.append(field_gal)
        
        # Cluster galaxy (at various distances from center)
        for j, (cluster_name, cluster) in enumerate(CLUSTER_ENVIRONMENTS.items()):
            if j == i % 3:  # Distribute among clusters
                # Galaxy at 0.5 * r_virial from cluster center
                r_cluster = 0.5 * cluster["r_virial"] * KPC_TO_M
                g_ext = G * cluster["mass"] / r_cluster**2
                
                cluster_gal = RotationCurveGalaxy(
                    name=f"Cluster_{i+1}_{cluster_name}",
                    environment=cluster_name,
                    baryonic_mass=mass,
                    disk_scale_length=h,
                    max_radius=r_max,
                    g_external=g_ext,
                    is_cluster=True
                )
                cluster_galaxies.append(cluster_gal)
    
    return field_galaxies, cluster_galaxies


def generate_rotation_curves(galaxies: List[RotationCurveGalaxy], 
                              include_efe: bool = True,
                              add_noise: bool = True) -> None:
    """Generate synthetic rotation curves using MOND with/without EFE."""
    
    mond = MONDCalculator()
    
    for galaxy in galaxies:
        # Create galaxy model
        model = GalaxyModel(
            name=galaxy.name,
            distance=10.0,  # Arbitrary
            luminosity=galaxy.baryonic_mass,  # Assume M/L = 1
            mass_to_light=1.0,
            scale_length=galaxy.disk_scale_length,
            g_ext=galaxy.g_external if include_efe else 0.0
        )
        
        # Generate radii array
        n_points = 20
        radii = np.linspace(0.5, galaxy.max_radius, n_points)
        galaxy.radii = radii
        
        # Calculate rotation curve
        v_mond = mond.rotation_curve(model, radii, include_efe=include_efe)
        
        # Add observational noise
        if add_noise:
            noise_level = 0.05  # 5% velocity error
            v_error = v_mond * noise_level
            v_observed = v_mond + np.random.normal(0, v_error)
            galaxy.v_observed = np.maximum(v_observed, 1.0)
            galaxy.v_error = v_error
        else:
            galaxy.v_observed = v_mond
            galaxy.v_error = np.zeros_like(v_mond)


# =============================================================================
# EFE SIGNATURE ANALYSIS
# =============================================================================

def measure_rc_shape(radii: np.ndarray, velocities: np.ndarray) -> Dict:
    """
    Measure rotation curve shape to detect EFE.
    
    Key metrics:
    - Outer slope: d(log V) / d(log r) at large radii
    - Flatness: ratio of V_max to V_outer
    - Rise-decline pattern
    
    EFE prediction: outer slope should be negative (declining RC)
    """
    if len(radii) < 5:
        return {'error': 'Insufficient data'}
    
    # Use outer half of rotation curve
    mid = len(radii) // 2
    r_outer = radii[mid:]
    v_outer = velocities[mid:]
    
    # Fit power law: V ~ r^alpha
    log_r = np.log(r_outer)
    log_v = np.log(v_outer + 1e-10)
    
    coeffs = np.polyfit(log_r, log_v, 1)
    outer_slope = coeffs[0]
    
    # V_max and V_outer
    v_max = np.max(velocities)
    v_end = velocities[-1]
    
    # Flatness ratio
    flatness = v_end / v_max if v_max > 0 else 0
    
    # Decline fraction
    decline = (v_max - v_end) / v_max if v_max > 0 else 0
    
    return {
        'outer_slope': outer_slope,
        'v_max': v_max,
        'v_end': v_end,
        'flatness': flatness,
        'decline_fraction': decline,
        'is_declining': outer_slope < -0.1,
        'is_flat': abs(outer_slope) < 0.1,
        'is_rising': outer_slope > 0.1
    }


def analyze_efe_signatures(field_galaxies: List[RotationCurveGalaxy],
                           cluster_galaxies: List[RotationCurveGalaxy]) -> Dict:
    """
    Compare rotation curve shapes between field and cluster galaxies.
    
    EFE prediction:
    - Field galaxies: FLAT rotation curves (slope ~ 0)
    - Cluster galaxies: DECLINING rotation curves (slope < 0)
    """
    results = {
        'field': [],
        'cluster': [],
        'summary': {}
    }
    
    # Analyze field galaxies
    for g in field_galaxies:
        shape = measure_rc_shape(g.radii, g.v_observed)
        shape['name'] = g.name
        shape['g_ratio'] = g.g_ratio
        shape['mass'] = g.baryonic_mass
        results['field'].append(shape)
    
    # Analyze cluster galaxies
    for g in cluster_galaxies:
        shape = measure_rc_shape(g.radii, g.v_observed)
        shape['name'] = g.name
        shape['g_ratio'] = g.g_ratio
        shape['mass'] = g.baryonic_mass
        results['cluster'].append(shape)
    
    # Summary statistics
    field_slopes = [r['outer_slope'] for r in results['field'] if 'error' not in r]
    cluster_slopes = [r['outer_slope'] for r in results['cluster'] if 'error' not in r]
    
    results['summary'] = {
        'field_mean_slope': np.mean(field_slopes) if field_slopes else 0,
        'field_std_slope': np.std(field_slopes) if field_slopes else 0,
        'cluster_mean_slope': np.mean(cluster_slopes) if cluster_slopes else 0,
        'cluster_std_slope': np.std(cluster_slopes) if cluster_slopes else 0,
        'field_n_flat': sum(1 for r in results['field'] if r.get('is_flat', False)),
        'field_n_declining': sum(1 for r in results['field'] if r.get('is_declining', False)),
        'cluster_n_flat': sum(1 for r in results['cluster'] if r.get('is_flat', False)),
        'cluster_n_declining': sum(1 for r in results['cluster'] if r.get('is_declining', False)),
    }
    
    # T-test for difference
    if len(field_slopes) > 2 and len(cluster_slopes) > 2:
        from scipy import stats
        t_stat, p_val = stats.ttest_ind(field_slopes, cluster_slopes)
        results['summary']['t_statistic'] = t_stat
        results['summary']['p_value'] = p_val
        results['summary']['efe_detected'] = (p_val < 0.05 and 
            results['summary']['cluster_mean_slope'] < results['summary']['field_mean_slope'])
    
    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_comparison_plots(field_galaxies: List[RotationCurveGalaxy],
                            cluster_galaxies: List[RotationCurveGalaxy],
                            results: Dict) -> List[str]:
    """Create comparison plots for field vs cluster rotation curves."""
    
    saved_files = []
    
    # ==========================================================
    # Plot 1: Example rotation curves
    # ==========================================================
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Top row: Field galaxies
    for i, g in enumerate(field_galaxies[:3]):
        ax = axes[0, i]
        ax.errorbar(g.radii, g.v_observed, yerr=g.v_error, 
                   fmt='bo-', markersize=4, capsize=2)
        ax.set_xlabel('Radius (kpc)')
        ax.set_ylabel('V (km/s)')
        ax.set_title(f'{g.name}\n$g_{{ext}}/a_0$ = {g.g_ratio:.3f}')
        ax.grid(True, alpha=0.3)
        
        # Add slope annotation
        shape = results['field'][i]
        ax.annotate(f"Slope: {shape['outer_slope']:.3f}",
                   xy=(0.95, 0.95), xycoords='axes fraction',
                   ha='right', va='top', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Bottom row: Cluster galaxies
    for i, g in enumerate(cluster_galaxies[:3]):
        ax = axes[1, i]
        ax.errorbar(g.radii, g.v_observed, yerr=g.v_error,
                   fmt='ro-', markersize=4, capsize=2)
        ax.set_xlabel('Radius (kpc)')
        ax.set_ylabel('V (km/s)')
        ax.set_title(f'{g.name}\n$g_{{ext}}/a_0$ = {g.g_ratio:.2f}')
        ax.grid(True, alpha=0.3)
        
        # Add slope annotation
        shape = results['cluster'][i]
        ax.annotate(f"Slope: {shape['outer_slope']:.3f}",
                   xy=(0.95, 0.95), xycoords='axes fraction',
                   ha='right', va='top', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    axes[0, 0].set_ylabel('Field Galaxies\nV (km/s)')
    axes[1, 0].set_ylabel('Cluster Galaxies\nV (km/s)')
    
    plt.suptitle('EFE Test: Rotation Curves in Different Environments', fontsize=14)
    plt.tight_layout()
    
    filename = FIGURES_DIR / 'efe_field_vs_cluster_rc.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    # ==========================================================
    # Plot 2: Slope comparison
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Slope histogram
    ax1 = axes[0]
    field_slopes = [r['outer_slope'] for r in results['field'] if 'error' not in r]
    cluster_slopes = [r['outer_slope'] for r in results['cluster'] if 'error' not in r]
    
    bins = np.linspace(-0.5, 0.3, 15)
    ax1.hist(field_slopes, bins=bins, alpha=0.6, color='blue', 
            label=f'Field (n={len(field_slopes)})')
    ax1.hist(cluster_slopes, bins=bins, alpha=0.6, color='red',
            label=f'Cluster (n={len(cluster_slopes)})')
    
    ax1.axvline(x=0, color='gray', linestyle='--', label='Flat (slope=0)')
    ax1.axvline(x=np.mean(field_slopes), color='blue', linestyle='-', 
               label=f'Field mean: {np.mean(field_slopes):.3f}')
    ax1.axvline(x=np.mean(cluster_slopes), color='red', linestyle='-',
               label=f'Cluster mean: {np.mean(cluster_slopes):.3f}')
    
    ax1.set_xlabel('Outer RC Slope (d log V / d log r)')
    ax1.set_ylabel('Count')
    ax1.set_title('Distribution of Rotation Curve Slopes')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Right: Slope vs g_ext/a0
    ax2 = axes[1]
    
    field_g = [r['g_ratio'] for r in results['field'] if 'error' not in r]
    cluster_g = [r['g_ratio'] for r in results['cluster'] if 'error' not in r]
    
    ax2.scatter(field_g, field_slopes, c='blue', s=80, alpha=0.7, label='Field')
    ax2.scatter(cluster_g, cluster_slopes, c='red', s=80, alpha=0.7, label='Cluster')
    
    # Add trend line
    all_g = np.array(field_g + cluster_g)
    all_slopes = np.array(field_slopes + cluster_slopes)
    z = np.polyfit(np.log10(all_g + 1e-5), all_slopes, 1)
    p = np.poly1d(z)
    x_line = np.logspace(-4, 1, 50)
    ax2.plot(x_line, p(np.log10(x_line)), 'k--', alpha=0.5, 
            label=f'Trend (slope={z[0]:.2f})')
    
    ax2.axhline(y=0, color='gray', linestyle=':', alpha=0.7)
    ax2.set_xlabel('$g_{ext}/a_0$')
    ax2.set_ylabel('Outer RC Slope')
    ax2.set_xscale('log')
    ax2.set_title('RC Slope vs External Field')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    filename = FIGURES_DIR / 'efe_slope_analysis.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    # ==========================================================
    # Plot 3: Normalized rotation curves
    # ==========================================================
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Normalize by V_max and r_max
    ax1 = axes[0]
    for g in field_galaxies:
        r_norm = g.radii / g.max_radius
        v_norm = g.v_observed / np.max(g.v_observed)
        ax1.plot(r_norm, v_norm, 'b-', alpha=0.5)
    
    ax1.set_xlabel('r / r_max')
    ax1.set_ylabel('V / V_max')
    ax1.set_title(f'Field Galaxies (n={len(field_galaxies)})\n$g_{{ext}}/a_0 < 0.01$')
    ax1.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax1.set_ylim(0.5, 1.2)
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[1]
    for g in cluster_galaxies:
        r_norm = g.radii / g.max_radius
        v_norm = g.v_observed / np.max(g.v_observed)
        ax2.plot(r_norm, v_norm, 'r-', alpha=0.5)
    
    ax2.set_xlabel('r / r_max')
    ax2.set_ylabel('V / V_max')
    ax2.set_title(f'Cluster Galaxies (n={len(cluster_galaxies)})\n$g_{{ext}}/a_0 > 1$')
    ax2.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    ax2.set_ylim(0.5, 1.2)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Normalized Rotation Curves: EFE Prediction', fontsize=14)
    plt.tight_layout()
    
    filename = FIGURES_DIR / 'efe_normalized_rc.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    saved_files.append(str(filename))
    plt.close()
    
    return saved_files


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run field vs cluster EFE test."""
    
    print("=" * 70)
    print("EFE CLEAN TEST: Field vs Cluster Galaxies")
    print("=" * 70)
    
    # Generate samples
    print("\n[1] Generating matched galaxy samples...")
    field_galaxies, cluster_galaxies = generate_sample_galaxies()
    
    print(f"    Field galaxies: {len(field_galaxies)}")
    print(f"    Cluster galaxies: {len(cluster_galaxies)}")
    
    # Generate rotation curves WITH EFE
    print("\n[2] Generating MOND rotation curves (with EFE)...")
    generate_rotation_curves(field_galaxies, include_efe=True)
    generate_rotation_curves(cluster_galaxies, include_efe=True)
    
    # Show examples
    print("\n[3] Sample galaxies:")
    print("\n    Field galaxies:")
    for g in field_galaxies[:3]:
        print(f"      {g.name}: M={g.baryonic_mass:.1e}, "
              f"g_ext/a0={g.g_ratio:.4f}, V_max={max(g.v_observed):.1f} km/s")
    
    print("\n    Cluster galaxies:")
    for g in cluster_galaxies[:3]:
        print(f"      {g.name}: M={g.baryonic_mass:.1e}, "
              f"g_ext/a0={g.g_ratio:.2f}, V_max={max(g.v_observed):.1f} km/s")
    
    # Analyze EFE signatures
    print("\n[4] Analyzing rotation curve shapes...")
    results = analyze_efe_signatures(field_galaxies, cluster_galaxies)
    
    print("\n" + "=" * 70)
    print("RESULTS: ROTATION CURVE SHAPE ANALYSIS")
    print("=" * 70)
    
    summary = results['summary']
    
    print(f"\nOuter slope statistics:")
    print(f"    Field galaxies:   {summary['field_mean_slope']:.4f} ± {summary['field_std_slope']:.4f}")
    print(f"    Cluster galaxies: {summary['cluster_mean_slope']:.4f} ± {summary['cluster_std_slope']:.4f}")
    
    print(f"\nRotation curve classification:")
    print(f"    Field - Flat: {summary['field_n_flat']}, Declining: {summary['field_n_declining']}")
    print(f"    Cluster - Flat: {summary['cluster_n_flat']}, Declining: {summary['cluster_n_declining']}")
    
    if 'p_value' in summary:
        print(f"\nStatistical test:")
        print(f"    t-statistic: {summary['t_statistic']:.3f}")
        print(f"    p-value: {summary['p_value']:.6f}")
        print(f"    EFE detected: {'YES' if summary['efe_detected'] else 'NO'}")
    
    # Create plots
    print("\n[5] Creating diagnostic plots...")
    plots = create_comparison_plots(field_galaxies, cluster_galaxies, results)
    for p in plots:
        print(f"    Saved: {p}")
    
    # Interpretation
    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    
    if summary.get('efe_detected', False):
        print("""
EFE SIGNATURE DETECTED!

The MOND simulation shows clear differences:
- Field galaxies have FLAT rotation curves (slope ~ 0)
- Cluster galaxies have DECLINING rotation curves (slope < 0)

This is the EXPECTED EFE signature:
- Strong external field suppresses MOND boost
- Outer rotation velocities decline toward Keplerian

OBSERVATIONAL TEST:
If real cluster galaxies show systematically declining RCs
compared to field galaxies of the same mass, EFE is confirmed.

If cluster galaxies have the SAME flat RCs as field galaxies,
EFE (and thus MOND) is falsified.
""")
    else:
        print("""
EFE signature NOT clearly detected in this simulation.
Check parameters and sample selection.
""")
    
    # Save results
    results_file = Path(__file__).parent.parent / "data" / "efe_field_vs_cluster.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    
    save_data = {
        'field_mean_slope': summary['field_mean_slope'],
        'field_std_slope': summary['field_std_slope'],
        'cluster_mean_slope': summary['cluster_mean_slope'],
        'cluster_std_slope': summary['cluster_std_slope'],
        'field_n_flat': summary['field_n_flat'],
        'field_n_declining': summary['field_n_declining'],
        'cluster_n_flat': summary['cluster_n_flat'],
        'cluster_n_declining': summary['cluster_n_declining'],
    }
    if 'p_value' in summary:
        save_data['p_value'] = summary['p_value']
        save_data['efe_detected'] = bool(summary['efe_detected'])
    
    with open(results_file, 'w') as f:
        json.dump(save_data, f, indent=2)
    
    print(f"\nResults saved: {results_file}")
    
    return results


if __name__ == "__main__":
    results = main()
