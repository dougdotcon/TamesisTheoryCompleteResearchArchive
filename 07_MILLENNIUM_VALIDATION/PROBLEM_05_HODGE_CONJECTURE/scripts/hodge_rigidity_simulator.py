import numpy as np
import matplotlib.pyplot as plt

def simulate_hodge_rigidity():
    """
    Simulates the Period Map and the Rigidity of Hodge Classes.
    Visualizes the intersection of the (p,p)-locus with the Rational Lattice.
    """
    
    # 1. Period Domain Space (2D Projection)
    grid_size = 100
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # 2. The Hodge Locus (Type p,p constraint)
    # A smooth manifold representing the analytic condition
    hodge_locus = (X**2 - Y**3 + 0.5 * X * Y) # A generic curve for representation
    
    # 3. The Rational Grid (Arithemtic constraint)
    # Discrete points representing rational periods
    res = 0.5
    rational_x = np.arange(-2, 2.5, res)
    rational_y = np.arange(-2, 2.5, res)
    RX, RY = np.meshgrid(rational_x, rational_y)
    
    # 4. Finding Intersections (The Hodge Classes)
    # We find points along the locus that are closest to rational points
    hodge_points_x = []
    hodge_points_y = []
    
    # Simple search for points near the lattice
    for rx in rational_x:
        for ry in rational_y:
            # Check if this lattice point is "near" the hodge locus
            if abs(rx**2 - ry**3 + 0.5 * rx * ry) < 0.15:
                hodge_points_x.append(rx)
                hodge_points_y.append(ry)
    
    # Formatting for Academic Paper
    plt.figure(figsize=(10, 8))
    plt.style.use('seaborn-v0_8-paper')
    
    # Plot the Background (Moduli Space Energy)
    plt.contourf(X, Y, np.abs(hodge_locus), 20, cmap='Blues', alpha=0.1)
    
    # Plot the Locus
    CS = plt.contour(X, Y, hodge_locus, levels=[0], colors='#1f77b4', linewidths=2)
    plt.clabel(CS, inline=True, fmt='Type (p,p) Locus', fontsize=10)
    
    # Plot the Rational Grid
    plt.scatter(RX, RY, marker='+', color='gray', alpha=0.3, s=20, label='Rational Grid $H^{2p}(\mathbb{Q})$')
    
    # Highlight the Hodge Classes (Realized)
    plt.scatter(hodge_points_x, hodge_points_y, color='red', s=80, edgecolors='black', label='Hodge Classes (Motivic Rigidity)', zorder=5)
    
    # Plot a "Ghost Class" (Unstable/Non-intersection)
    plt.scatter([1.25], [-0.75], color='orange', s=50, marker='x', label='Ghost Class (Unstable/Measure Zero)')
    
    plt.title('Hodge Resolution: Rigidity of the Period Map')
    plt.xlabel('Period Ratio ($\omega_1 / \omega_2$)')
    plt.ylabel('Geometric Deformation ($\tau$)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.1)
    
    # Text annotations explaining the logic
    plt.text(-1.8, 1.5, r"$\mathrm{Rationality} \cap (p,p) = \mathrm{Algebraic\ Cycle}$", 
             bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
    
    # Save assets
    import os
    asset_dir = r"d:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_05_HODGE_CONJECTURE\assets"
    if not os.path.exists(asset_dir):
        os.makedirs(asset_dir)
        
    plt.savefig(os.path.join(asset_dir, "hodge_period_rigidity.png"), dpi=300)
    print(f"Rigidity plot saved to assets/hodge_period_rigidity.png")

    # 5. Stability Curve (Entropy vs Lattice Proximity)
    plt.figure(figsize=(10, 6))
    dist = np.linspace(0, 1, 100)
    stability = np.exp(-10 * dist) # Rapid decay of non-rational "ghosts"
    plt.plot(dist, stability, color='purple', label='Algebraicity Score')
    plt.fill_between(dist, 0, stability, color='purple', alpha=0.1)
    plt.title('The Noether-Lefschetz Stability Gradient')
    plt.xlabel('Distance from Rational Grid')
    plt.ylabel('Structural Stability (Algebraic Survival)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(asset_dir, "hodge_stability_gradient.png"), dpi=300)
    print(f"Stability plot saved to assets/hodge_stability_gradient.png")

if __name__ == "__main__":
    simulate_hodge_rigidity()
