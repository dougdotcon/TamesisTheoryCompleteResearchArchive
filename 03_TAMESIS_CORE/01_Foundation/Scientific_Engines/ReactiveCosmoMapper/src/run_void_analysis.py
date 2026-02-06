from void_scanner import VoidScanner
from visualizer import GalaxyVisualizer
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🕳️ Starting Cosmic Void Analysis...")
    
    # 1. Load Data
    viz = GalaxyVisualizer(data_file="data/sdss_sample.csv")
    df = viz.load_and_transform()
    
    if df is None:
        return

    # 2. Initialize Scanner
    scanner = VoidScanner(df)
    
    # 3. Run Scan
    # 100k probes gives good statistics
    void_radii = scanner.scan_for_voids(n_probes=100000)
    
    # 4. Analysis
    mean_radius = np.mean(void_radii)
    max_radius = np.max(void_radii)
    print(f"✅ Scan Complete.")
    print(f"   - Average Void Radius: {mean_radius:.2f} Mpc")
    print(f"   - Largest Void Detectable: {max_radius:.2f} Mpc")
    
    # 5. Plot Void Size Function
    plt.figure(figsize=(10, 6))
    
    # Histogram / PDF
    counts, bins, _ = plt.hist(void_radii, bins=50, density=True, 
                               alpha=0.6, color='purple', label='Reactive Universe (Observed)')
    
    # Theoretical curve fitting (Optional / Stylistic)
    # Poisson distribution of voids usually follows exp(-n*V)
    # Just plotting the KDE or curve derived from hist
    
    plt.axvline(mean_radius, color='k', linestyle='dashed', linewidth=1, label=f'Mean Radius: {mean_radius:.1f} Mpc')
    plt.axvline(max_radius, color='r', linestyle='dashed', linewidth=1, label=f'Max Radius: {max_radius:.1f} Mpc')
    
    plt.title("Cosmic Void Size Distribution (Reactive Gravity)")
    plt.xlabel("Void Radius (Mpc)")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_file = "Validation/void_size_distribution.png"
    plt.savefig(output_file)
    print(f"✅ Distribution plot saved to {output_file}")

if __name__ == "__main__":
    main()
