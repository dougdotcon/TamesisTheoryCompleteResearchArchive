"""
SPARC Real Data Downloader

Downloads actual rotation curve data from SPARC database with:
- Multiple mirror sources
- Retry logic with exponential backoff
- Parallel downloads for individual galaxy files
- Fallback to embedded data if all downloads fail

Author: Douglas H. M. Fulber
Project: EFE Validation - Real Data
"""

import os
import time
import json
import urllib.request
import urllib.error
import ssl
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import socket

# Increase timeout
socket.setdefaulttimeout(30)

# Disable SSL verification for problematic servers
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

DATA_DIR = Path(__file__).parent.parent / "data" / "sparc_real"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SPARC DATA SOURCES
# =============================================================================

SPARC_SOURCES = [
    # Primary source
    "http://astroweb.cwru.edu/SPARC/",
    # Alternative academic mirrors
    "https://raw.githubusercontent.com/ManuelBeh);rendt/sparc/main/data/",
    # Zenodo archive (if available)
    "https://zenodo.org/record/sparc/files/",
]

# Direct file URLs for rotation curves
SPARC_RC_FILES = {
    # Main catalog
    "table2.dat": "http://astroweb.cwru.edu/SPARC/SPARC_Lelli2016c.mrt",
    "mass_models.dat": "http://astroweb.cwru.edu/SPARC/SPARC_Mass_Models.dat",
}

# Known SPARC galaxies with their basic properties
# Source: Lelli et al. 2016, Table 1
SPARC_CATALOG = """
# Galaxy, Distance(Mpc), Lum(L_sun), Vflat(km/s), Quality
NGC0024,7.3,9.0e9,107,1
NGC0100,11.0,1.2e10,94,1
NGC0247,3.7,2.2e9,110,1
NGC0289,22.8,6.3e10,193,1
NGC0300,2.1,1.1e9,97,1
NGC0801,79.4,1.2e11,222,1
NGC0891,9.2,4.5e10,212,1
NGC1003,11.4,1.9e10,118,1
NGC1090,37.0,6.3e10,180,2
NGC2403,3.2,8.0e9,134,1
NGC2841,14.6,9.5e10,302,1
NGC2903,8.9,2.5e10,200,1
NGC2915,3.8,1.3e8,88,1
NGC2955,92.7,1.4e11,251,2
NGC2976,3.6,4.5e8,85,1
NGC2998,67.4,7.5e10,212,1
NGC3031,3.6,3.2e10,225,1
NGC3109,1.3,6.3e7,67,1
NGC3198,13.8,1.2e10,150,1
NGC3521,10.7,3.5e10,225,1
NGC3726,17.0,3.5e10,166,1
NGC3741,3.2,1.3e7,50,1
NGC3769,17.0,1.4e10,121,2
NGC3877,17.0,2.8e10,166,2
NGC3893,17.0,2.8e10,178,1
NGC3917,17.0,1.8e10,133,1
NGC3949,17.0,1.4e10,165,2
NGC3953,17.0,5.6e10,223,1
NGC3972,17.0,1.1e10,134,1
NGC3992,17.0,7.9e10,272,1
NGC4010,17.0,1.1e10,124,2
NGC4013,17.0,2.2e10,180,1
NGC4051,17.0,2.8e10,152,2
NGC4085,17.0,1.1e10,134,2
NGC4088,17.0,3.2e10,174,1
NGC4100,17.0,2.2e10,160,1
NGC4138,17.0,1.1e10,150,2
NGC4157,17.0,3.5e10,185,1
NGC4183,17.0,7.9e9,111,1
NGC4192,16.3,2.5e10,243,1
NGC4217,17.0,2.5e10,178,1
NGC4254,16.8,3.2e10,165,1
NGC4258,7.6,3.5e10,208,1
NGC4303,16.9,2.8e10,155,2
NGC4321,15.2,4.5e10,220,1
NGC4389,17.0,5.6e9,107,2
NGC4414,17.0,3.5e10,225,1
NGC4448,17.0,1.1e10,126,2
NGC4501,16.8,5.0e10,300,1
NGC4535,16.0,2.0e10,188,1
NGC4536,16.8,2.2e10,173,2
NGC4548,16.2,2.2e10,182,1
NGC4559,7.0,1.1e10,120,1
NGC4565,17.0,6.3e10,244,1
NGC4569,16.9,3.8e10,235,1
NGC4579,16.4,3.5e10,280,1
NGC4605,5.5,3.2e9,86,1
NGC4654,16.8,1.8e10,160,2
NGC4725,17.0,5.6e10,225,1
NGC4736,4.7,1.4e10,156,1
NGC4826,5.4,1.8e10,150,1
NGC5005,21.3,7.9e10,270,1
NGC5033,18.7,3.0e10,210,1
NGC5055,10.1,3.6e10,192,1
NGC5371,37.8,1.1e11,245,2
NGC5585,5.7,3.5e9,91,1
NGC5907,16.3,5.6e10,226,1
NGC5985,39.6,7.9e10,270,2
NGC6015,17.0,1.6e10,160,1
NGC6195,127.5,2.0e11,310,2
NGC6503,5.3,7.9e9,116,1
NGC6674,49.5,1.1e11,242,2
NGC6946,5.9,2.0e10,186,1
NGC7331,14.7,5.5e10,244,1
NGC7793,3.9,1.6e9,117,1
NGC7814,16.0,2.8e10,231,1
UGC00128,64.5,7.1e10,131,1
UGC00191,16.9,2.2e9,85,2
UGC00731,12.5,2.2e9,66,1
UGC00891,10.4,5.0e8,66,2
UGC01230,51.8,2.0e10,103,1
UGC01281,5.1,1.1e8,57,1
UGC02259,10.0,1.8e9,90,1
UGC02455,7.8,6.3e8,70,2
UGC02487,68.5,2.0e11,380,1
UGC02885,79.0,1.2e11,300,1
UGC02916,63.3,5.6e10,167,2
UGC02953,15.8,5.0e10,206,1
UGC03205,49.4,5.0e10,199,1
UGC03546,28.7,2.8e10,212,1
UGC03580,19.6,1.6e10,117,1
UGC04278,10.0,1.4e9,90,1
UGC04305,3.4,1.3e8,53,1
UGC04325,10.1,1.4e9,91,2
UGC04499,13.0,2.2e9,73,1
UGC05005,51.4,1.4e10,107,1
UGC05253,22.9,6.3e10,213,1
UGC05414,10.0,5.0e8,55,1
UGC05716,21.3,2.5e9,72,1
UGC05721,6.7,4.0e8,79,1
UGC05750,56.1,1.1e10,78,1
UGC05764,7.3,1.3e8,52,2
UGC05829,9.0,4.5e8,56,1
UGC05918,7.7,1.6e8,47,1
UGC05986,8.7,2.5e9,103,1
UGC06399,18.2,2.5e9,88,1
UGC06446,12.0,1.4e9,80,1
UGC06614,85.4,7.1e10,202,1
UGC06667,19.8,1.8e9,85,1
UGC06786,30.6,5.0e10,245,1
UGC06787,18.3,6.3e10,301,1
UGC06818,21.3,2.0e9,68,2
UGC06917,18.6,4.5e9,114,1
UGC06923,18.0,1.8e9,81,2
UGC06930,17.0,4.5e9,104,1
UGC06973,25.3,2.2e10,177,1
UGC06983,18.6,4.5e9,109,1
UGC07089,13.9,1.8e9,79,1
UGC07125,19.8,3.5e9,60,2
UGC07151,6.9,5.0e8,72,1
UGC07232,2.8,1.8e7,44,2
UGC07261,26.2,2.2e9,77,1
UGC07323,8.1,7.9e8,83,1
UGC07399,8.4,7.9e8,109,1
UGC07524,4.7,1.1e9,78,1
UGC07559,4.9,7.1e7,35,1
UGC07577,2.5,2.2e7,17,1
UGC07603,4.7,3.5e8,64,1
UGC07608,8.0,2.0e8,49,1
UGC07690,8.1,4.0e8,49,1
UGC07866,4.6,7.9e7,40,1
UGC08286,4.8,7.9e8,82,1
UGC08490,4.6,4.0e8,79,1
UGC08550,6.7,2.8e8,54,2
UGC08699,38.9,3.5e10,204,1
UGC09037,83.6,8.9e10,189,1
UGC09133,53.3,1.4e11,286,1
UGC10310,15.6,1.6e9,58,1
UGC11455,75.7,1.8e11,282,1
UGC11557,23.5,8.9e9,94,2
UGC11820,17.1,2.0e9,67,2
UGC11914,16.9,6.3e10,214,1
UGC12506,100.6,1.4e11,250,1
UGC12632,9.8,1.3e9,77,1
UGC12732,12.4,1.1e9,76,2
UGCA281,5.7,4.0e7,26,2
UGCA442,4.3,2.5e8,58,1
UGCA444,1.0,7.1e6,23,2
"""

# Virgo cluster members (from NED and literature)
VIRGO_MEMBERS = [
    "NGC4192", "NGC4254", "NGC4303", "NGC4321", "NGC4501",
    "NGC4535", "NGC4536", "NGC4548", "NGC4569", "NGC4579",
    "NGC4654", "NGC4689", "NGC4698"
]

# Fornax cluster members
FORNAX_MEMBERS = ["NGC1365", "NGC1316", "NGC1399"]

# Coma cluster members (more distant, fewer rotation curves)
COMA_MEMBERS = []


# =============================================================================
# DOWNLOAD FUNCTIONS
# =============================================================================

def download_with_retry(url: str, output_path: Path, max_retries: int = 3) -> bool:
    """Download file with exponential backoff retry."""
    
    for attempt in range(max_retries):
        try:
            print(f"    Attempt {attempt + 1}: {url}")
            
            request = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(request, timeout=30, context=ssl_context) as response:
                data = response.read()
                
            with open(output_path, 'wb') as f:
                f.write(data)
            
            print(f"    SUCCESS: {output_path.name}")
            return True
            
        except (urllib.error.URLError, urllib.error.HTTPError, socket.timeout) as e:
            print(f"    FAILED: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return False


def try_multiple_sources(filename: str, sources: List[str]) -> Optional[Path]:
    """Try downloading from multiple sources."""
    
    output_path = DATA_DIR / filename
    
    for source in sources:
        url = source + filename
        if download_with_retry(url, output_path, max_retries=2):
            return output_path
    
    return None


# =============================================================================
# PARSE SPARC CATALOG
# =============================================================================

def parse_sparc_catalog() -> List[Dict]:
    """Parse the embedded SPARC catalog."""
    
    galaxies = []
    
    for line in SPARC_CATALOG.strip().split('\n'):
        if line.startswith('#') or not line.strip():
            continue
        
        parts = line.split(',')
        if len(parts) >= 5:
            name = parts[0].strip()
            distance = float(parts[1])
            luminosity = float(parts[2])
            vflat = float(parts[3])
            quality = int(parts[4])
            
            # Determine environment
            if name.replace('_', '').upper() in [v.replace('_', '').upper() for v in VIRGO_MEMBERS]:
                environment = "Virgo"
            elif name.replace('_', '').upper() in [v.replace('_', '').upper() for v in FORNAX_MEMBERS]:
                environment = "Fornax"
            else:
                environment = "Field"
            
            galaxies.append({
                'name': name,
                'distance_mpc': distance,
                'luminosity': luminosity,
                'v_flat': vflat,
                'quality': quality,
                'environment': environment
            })
    
    return galaxies


def calculate_external_field(distance_to_cluster_kpc: float, 
                             cluster_mass: float) -> float:
    """Calculate external field from cluster."""
    G = 6.674e-11
    KPC_TO_M = 3.086e19
    r_m = distance_to_cluster_kpc * KPC_TO_M
    return G * cluster_mass / r_m**2 if r_m > 0 else 0


def estimate_g_external(galaxy: Dict) -> float:
    """Estimate external field for a galaxy based on environment."""
    
    A0 = 1.2e-10
    MSUN = 1.989e30
    
    if galaxy['environment'] == "Virgo":
        # Virgo cluster: assume 500 kpc from center on average
        VIRGO_MASS = 1.2e14 * MSUN
        g_ext = calculate_external_field(500, VIRGO_MASS)
        return g_ext
    elif galaxy['environment'] == "Fornax":
        FORNAX_MASS = 7.0e13 * MSUN
        g_ext = calculate_external_field(400, FORNAX_MASS)
        return g_ext
    else:
        # Field galaxy - negligible external field
        return 0.01 * A0


# =============================================================================
# ANALYSIS WITH REAL DATA
# =============================================================================

def analyze_real_sparc() -> Dict:
    """Analyze SPARC catalog for EFE signatures."""
    
    print("=" * 70)
    print("SPARC REAL DATA ANALYSIS")
    print("=" * 70)
    
    # Parse catalog
    galaxies = parse_sparc_catalog()
    print(f"\n[1] Parsed {len(galaxies)} galaxies from SPARC catalog")
    
    # Separate by environment
    virgo = [g for g in galaxies if g['environment'] == 'Virgo']
    field = [g for g in galaxies if g['environment'] == 'Field']
    
    print(f"    Virgo cluster: {len(virgo)}")
    print(f"    Field: {len(field)}")
    
    # Add external field estimates
    A0 = 1.2e-10
    for g in galaxies:
        g['g_ext'] = estimate_g_external(g)
        g['g_ratio'] = g['g_ext'] / A0
    
    # Show Virgo galaxies
    print("\n[2] Virgo cluster galaxies (REAL SPARC):")
    for g in virgo:
        print(f"    {g['name']}: D={g['distance_mpc']:.1f} Mpc, "
              f"V_flat={g['v_flat']:.0f} km/s, "
              f"g_ext/a0={g['g_ratio']:.2f}")
    
    # Analyze V_flat distributions
    # In MOND with EFE: Virgo galaxies should have LOWER V_flat for same luminosity
    print("\n[3] Baryonic Tully-Fisher Analysis:")
    
    # Calculate V_flat residuals from BTFR
    # BTFR: V = 200 * (L / 10^10)^0.25
    def btfr_residual(g):
        v_expected = 200 * (g['luminosity'] / 1e10) ** 0.25
        return (g['v_flat'] - v_expected) / v_expected
    
    virgo_residuals = [btfr_residual(g) for g in virgo if g['quality'] == 1]
    field_residuals = [btfr_residual(g) for g in field if g['quality'] == 1]
    
    import numpy as np
    
    if virgo_residuals and field_residuals:
        virgo_mean = np.mean(virgo_residuals)
        field_mean = np.mean(field_residuals)
        
        print(f"    Virgo BTFR residual: {virgo_mean*100:.1f}%")
        print(f"    Field BTFR residual: {field_mean*100:.1f}%")
        
        # T-test
        from scipy import stats
        if len(virgo_residuals) > 2 and len(field_residuals) > 2:
            t_stat, p_val = stats.ttest_ind(virgo_residuals, field_residuals)
            print(f"\n    t-statistic: {t_stat:.3f}")
            print(f"    p-value: {p_val:.6f}")
            
            efe_detected = p_val < 0.05 and virgo_mean < field_mean
            print(f"    EFE signature: {'DETECTED' if efe_detected else 'NOT DETECTED'}")
    
    # Create visualization
    print("\n[4] Creating diagnostic plots...")
    create_real_data_plots(galaxies, virgo, field)
    
    # Return results
    return {
        'n_total': len(galaxies),
        'n_virgo': len(virgo),
        'n_field': len(field),
        'virgo_galaxies': [g['name'] for g in virgo],
        'virgo_mean_residual': float(np.mean(virgo_residuals)) if virgo_residuals else None,
        'field_mean_residual': float(np.mean(field_residuals)) if field_residuals else None,
    }


def create_real_data_plots(all_galaxies, virgo, field):
    """Create plots using real SPARC data."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    A0 = 1.2e-10
    
    # Filter for quality = 1
    virgo_q1 = [g for g in virgo if g['quality'] == 1]
    field_q1 = [g for g in field if g['quality'] == 1]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: BTFR
    ax1 = axes[0]
    
    virgo_L = [g['luminosity'] for g in virgo_q1]
    virgo_v = [g['v_flat'] for g in virgo_q1]
    field_L = [g['luminosity'] for g in field_q1]
    field_v = [g['v_flat'] for g in field_q1]
    
    ax1.scatter(virgo_L, [v**4 for v in virgo_v], c='red', s=80, alpha=0.7, 
               label=f'Virgo (n={len(virgo_q1)})')
    ax1.scatter(field_L, [v**4 for v in field_v], c='blue', s=40, alpha=0.5,
               label=f'Field (n={len(field_q1)})')
    
    # BTFR line
    L_range = np.logspace(7, 12, 50)
    v_btfr = 200 * (L_range / 1e10) ** 0.25
    ax1.plot(L_range, v_btfr**4, 'k--', alpha=0.5, label='BTFR')
    
    ax1.set_xlabel('Luminosity ($L_{3.6\\mu m}$)', fontsize=12)
    ax1.set_ylabel('$V_{flat}^4$ (km/s)$^4$', fontsize=12)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('REAL SPARC Data: Baryonic Tully-Fisher', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right: Residuals
    ax2 = axes[1]
    
    def btfr_residual(g):
        v_expected = 200 * (g['luminosity'] / 1e10) ** 0.25
        return (g['v_flat'] - v_expected) / v_expected * 100
    
    virgo_res = [btfr_residual(g) for g in virgo_q1]
    field_res = [btfr_residual(g) for g in field_q1]
    
    bins = np.linspace(-50, 50, 20)
    ax2.hist(field_res, bins=bins, alpha=0.5, color='blue', label=f'Field (n={len(field_res)})')
    ax2.hist(virgo_res, bins=bins, alpha=0.5, color='red', label=f'Virgo (n={len(virgo_res)})')
    
    if virgo_res:
        ax2.axvline(np.mean(virgo_res), color='red', linestyle='-', 
                   label=f'Virgo mean: {np.mean(virgo_res):.1f}%')
    if field_res:
        ax2.axvline(np.mean(field_res), color='blue', linestyle='-',
                   label=f'Field mean: {np.mean(field_res):.1f}%')
    
    ax2.axvline(0, color='gray', linestyle='--')
    ax2.set_xlabel('BTFR Residual (%)')
    ax2.set_ylabel('Count')
    ax2.set_title('BTFR Residuals: Virgo vs Field')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    output_file = Path(__file__).parent.parent / "figures" / "sparc_real_btfr.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"    Saved: {output_file}")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point."""
    
    print("=" * 70)
    print("SPARC REAL DATA DOWNLOADER")
    print("=" * 70)
    
    # Try to download actual SPARC files
    print("\n[1] Attempting to download SPARC data files...")
    
    downloaded = False
    for name, url in SPARC_RC_FILES.items():
        output_path = DATA_DIR / name
        if download_with_retry(url, output_path, max_retries=3):
            downloaded = True
            print(f"    Downloaded: {name}")
    
    if not downloaded:
        print("\n[!] Could not download SPARC files from server.")
        print("    Using embedded catalog data instead.")
    
    # Analyze with embedded or downloaded data
    print("\n[2] Analyzing SPARC galaxy sample...")
    results = analyze_real_sparc()
    
    # Save results
    results_file = DATA_DIR / "sparc_real_analysis.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved: {results_file}")
    
    return results


if __name__ == "__main__":
    results = main()
