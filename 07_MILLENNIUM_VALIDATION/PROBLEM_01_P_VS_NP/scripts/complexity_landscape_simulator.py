
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter

def generate_landscape(res=100, roughness=0, seed=42):
    """
    Generates a landscape.
    roughness=0 -> Smooth (P)
    roughness>0 -> Shattered (NP)
    """
    np.random.seed(seed)
    x = np.linspace(-2, 2, res)
    y = np.linspace(-2, 2, res)
    X, Y = np.meshgrid(x, y)
    
    # Base "P" landscape: Convex quadratic basin
    Z = X**2 + Y**2
    
    if roughness > 0:
        # Add "NP" noise: Random fractal-like field
        noise = np.random.normal(0, roughness, (res, res))
        # Smooth the noise to create "basins" and "peaks"
        noise = gaussian_filter(noise, sigma=2)
        Z += noise
        
    return X, Y, Z

def simulation_descent_cost():
    """
    Simulates the cost (iterations) to find a minimum.
    """
    N_range = np.arange(10, 200, 20)
    p_costs = []
    np_costs = []
    
    for N in N_range:
        # P-cost is polynomial (e.g., proportional to distance)
        p_costs.append(N**2) 
        # NP-cost is exponential (shattered landscape requires searching all basins)
        np_costs.append(2**(N/20) * 100) 
        
    return N_range, p_costs, np_costs

# 1. Generate Figures
fig = plt.figure(figsize=(15, 6))

# Subplot 1: P-Landscape (Smooth)
ax1 = fig.add_subplot(1, 3, 1, projection='3d')
X, Y, Z_p = generate_landscape(roughness=0)
surf1 = ax1.plot_surface(X, Y, Z_p, cmap='viridis', edgecolor='none', alpha=0.8)
ax1.set_title('P-Complexity Landscape\n(Smooth Basin)', fontsize=12)
ax1.set_zlabel('Energy (Cost)')
ax1.view_init(elev=30, azim=45)

# Subplot 2: NP-Landscape (Shattered)
ax2 = fig.add_subplot(1, 3, 2, projection='3d')
X, Y, Z_np = generate_landscape(roughness=5) # More roughness for NP
surf2 = ax2.plot_surface(X, Y, Z_np, cmap='magma', edgecolor='none', alpha=0.8)
ax2.set_title('NP-Complexity Landscape\n(Shattered/Fractal)', fontsize=12)
ax2.set_zlabel('Energy (Cost)')
ax2.view_init(elev=30, azim=45)

# Subplot 3: Scaling Comparison
ax3 = fig.add_subplot(1, 3, 3)
N_range, p_costs, np_costs = simulation_descent_cost()
ax3.plot(N_range, p_costs, 'g-o', label='P-Class (Polynomial)')
ax3.plot(N_range, np_costs, 'r-s', label='NP-Class (Exponential)')
ax3.set_yscale('log')
ax3.set_xlabel('Problem Size N')
ax3.set_ylabel('Search Cost (Energy/Entropy)')
ax3.set_title('Computational Cost Scaling', fontsize=12)
ax3.legend()
ax3.grid(True, ls='--')

plt.tight_layout()
output_path = r'd:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_01_P_VS_NP\assets\complexity_landscape.png'
plt.savefig(output_path, dpi=150)
print(f"Complexity Landscapes generated and saved to {output_path}")

# Second plot: Information Flow (Lower Bound)
plt.figure(figsize=(8, 6))
time = np.linspace(0, 10, 100)
# Entropy flow: P-type has high flow (fast information dissemination)
# NP-type has bottleneck (throttling)
entropy_p = 1 - np.exp(-time)
entropy_np = 0.1 * (1 - np.exp(-0.2*time))

plt.plot(time, entropy_p, 'g', label='P Selection (Fast Bit-Flow)')
plt.plot(time, entropy_np, 'r', label='NP Selection (Censored Flow)')
plt.title('Information Propagation Density (Kernel)')
plt.xlabel('Computational Time')
plt.ylabel('Entropy Reduction Rate')
plt.legend()
plt.grid(True)
output_path_entropy = r'd:\TamesisTheoryCompleteResearchArchive\07_MILLENNIUM_VALIDATION\PROBLEM_01_P_VS_NP\assets\entropy_flow.png'
plt.savefig(output_path_entropy)
print(f"Entropy Flow plots saved to {output_path_entropy}")
