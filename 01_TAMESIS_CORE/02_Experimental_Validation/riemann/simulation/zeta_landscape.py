import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import mpmath

# Set low precision for fast visualization
mpmath.mp.dps = 5

def zeta_magnitude(x, y):
    # mpmath.zeta accepts complex args
    try:
        s = x + 1j * y
        val = mpmath.zeta(s)
        return float(abs(val))
    except:
        return 6.0 # Clamp on error

def generate_landscape_gif():
    print("Generating Riemann Landscape GIF (using mpmath)...")
    
    # Coarser Grid for speed
    x = np.linspace(0, 1, 30)
    y = np.linspace(0, 50, 60) # Up to t=50 (first few zeros)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    print("Calculating Zeta surface (this may take 30s)...")
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = min(zeta_magnitude(X[i, j], Y[i, j]), 6.0)
            
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Riemann Zeta Landscape: The Critical Line", fontsize=16, color='purple')
    
    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
    
    # Critical Line (Re(s) = 0.5) - calculate separately
    print("Calculating Critical Line...")
    crit_y = np.linspace(0, 50, 150)
    crit_x = np.full_like(crit_y, 0.5)
    crit_z = []
    for t in crit_y:
        crit_z.append(min(zeta_magnitude(0.5, t), 6.0))
    crit_z = np.array(crit_z)
    
    ax.plot(crit_x, crit_y, crit_z + 0.1, 'r-', linewidth=3, label='Critical Line (Re=0.5)')
    
    ax.set_xlabel("Re(s)")
    ax.set_ylabel("Im(s) = t")
    ax.set_zlabel("|Zeta(s)|")
    ax.set_ylim(0, 50)
    
    # Add scattered zeros points (approx known locations) to highlight them
    zeros_t = [14.13, 21.02, 25.01, 30.42, 32.93, 37.58, 40.91, 43.32, 48.00, 49.77]
    zeros_x = [0.5] * len(zeros_t)
    zeros_z = [0.1] * len(zeros_t) # Near zero
    ax.scatter(zeros_x, zeros_t, zeros_z, color='red', s=50, marker='o', depthshade=False, label='Zeros')
    
    ax.legend()
    
    # Animation function
    def update(frame):
        angle = 45 + frame * 2
        ax.view_init(elev=30, azim=angle)
        return surf,
    
    # Fewer frames for speed
    ani = FuncAnimation(fig, update, frames=60, interval=80, blit=False)
    
    output_path = "zeta_landscape.gif"
    print(f"Angle rotation... Saving to {output_path}")
    
    ani.save(output_path, writer=PillowWriter(fps=15))
    print("GIF saved successfully.")

if __name__ == "__main__":
    generate_landscape_gif()
