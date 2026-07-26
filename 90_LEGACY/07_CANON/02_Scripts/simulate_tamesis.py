
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
from scipy.linalg import expm

# Set random seed for reproducibility
np.random.seed(42)
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

def generate_metric_emergence(n_nodes=200):
    """
    Simulates the emergence of a smooth metric from a discrete graph
    using the Heat Kernel method.
    """
    print("Simulating Metric Emergence...")
    
    # 1. Create a Random Geometric Graph (The Kernel)
    # Using a soft geometric graph to simulate quantum locality
    pos = np.random.rand(n_nodes, 2)
    dist_matrix = squareform(pdist(pos))
    # Probabilistic connection (quantum tunneling/locality)
    prob_matrix = np.exp(-dist_matrix / 0.15)
    adj_matrix = (np.random.rand(n_nodes, n_nodes) < prob_matrix).astype(float)
    np.fill_diagonal(adj_matrix, 0)
    
    # Symmetrize
    adj_matrix = np.maximum(adj_matrix, adj_matrix.T)
    
    # 2. Compute Graph Laplacian
    degrees = np.sum(adj_matrix, axis=1)
    laplacian = np.diag(degrees) - adj_matrix
    
    # 3. Compute Heat Kernel (The Emergent Metric)
    # K(t) = exp(-t * L)
    t_diffusion = 0.5
    heat_kernel = expm(-t_diffusion * laplacian)
    
    # 4. Extract "Effective Metric" diagonal (local connectivity density)
    metric_density = np.diag(heat_kernel)
    
    # Visualization
    plt.figure(figsize=(10, 8))
    plt.tricontourf(pos[:,0], pos[:,1], metric_density, levels=20, cmap='inferno')
    plt.colorbar(label='Emergent Geometric Density (g_uv)')
    plt.scatter(pos[:,0], pos[:,1], c='white', s=10, alpha=0.5, label='Kernel Nodes')
    plt.title('Emergence of Smooth Spacetime from Discrete Kernel\n(Heat Kernel Density)', fontsize=14)
    plt.xlabel('x (Planck Units)')
    plt.ylabel('y (Planck Units)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('sim_metric_emergence.png', dpi=300)
    print("Saved sim_metric_emergence.png")

def generate_topological_defects(grid_size=30):
    """
    Simulates the formation of topological defects (Matter)
    in a 2D Spin Lattice (H_kernel).
    """
    print("Simulating Topological Defects...")
    
    # 1. Initialize Spins (Random Qubit States)
    # Using planar spins (XY model approx) for vortices
    thetas = np.random.uniform(0, 2*np.pi, (grid_size, grid_size))
    
    # 2. Annealing (Minimizing Hamiltonian H = -J sum cos(theta_i - theta_j))
    # Simple Metropolis-like relaxation
    n_steps = 1000
    T = 0.5 # Temperature
    
    for step in range(n_steps):
        i, j = np.random.randint(0, grid_size, 2)
        
        # Calculate local energy change
        d_theta = np.random.normal(0, 0.5)
        new_theta = thetas[i,j] + d_theta
        
        # Neighbors
        neighbors = []
        if i > 0: neighbors.append(thetas[i-1,j])
        if i < grid_size-1: neighbors.append(thetas[i+1,j])
        if j > 0: neighbors.append(thetas[i,j-1])
        if j < grid_size-1: neighbors.append(thetas[i,j+1])
        
        E_old = -sum(np.cos(thetas[i,j] - n) for n in neighbors)
        E_new = -sum(np.cos(new_theta - n) for n in neighbors)
        
        if E_new < E_old or np.random.rand() < np.exp(-(E_new - E_old)/T):
            thetas[i,j] = new_theta
            
    # 3. Calculate Vorticity (Topological Charge)
    vorticity = np.zeros((grid_size-1, grid_size-1))
    for i in range(grid_size-1):
        for j in range(grid_size-1):
            # Circulation around plaquette
            t1 = thetas[i,j]
            t2 = thetas[i+1,j]
            t3 = thetas[i+1,j+1]
            t4 = thetas[i,j+1]
            
            diffs = [t2-t1, t3-t2, t4-t3, t1-t4]
            # Wrap to [-pi, pi]
            diffs = [(d + np.pi) % (2*np.pi) - np.pi for d in diffs]
            
            vorticity[i,j] = sum(diffs) / (2*np.pi)

    # Visualization
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(np.sin(thetas), cmap='hsv', origin='lower')
    plt.title('Field Configuration (Phase)', fontsize=12)
    plt.colorbar(label='sin(theta)')
    
    plt.subplot(1, 2, 2)
    plt.imshow(vorticity, cmap='coolwarm', origin='lower', vmin=-1, vmax=1)
    plt.title('Topological Defects (Matter Creation)\n(Vorticity Map)', fontsize=12)
    plt.colorbar(label='Topological Charge')
    
    plt.tight_layout()
    plt.savefig('sim_defects.png', dpi=300)
    print("Saved sim_defects.png")

def generate_gravity_latency(path_len=100):
    """
    Simulates Gravity as Information Latency.
    Comparing signal propagation through Vacuum vs Mass.
    """
    print("Simulating Entropic Gravity...")
    
    distances = np.linspace(0, path_len, path_len)
    
    # Vacuum: Constant speed c = 1
    time_vacuum = distances / 1.0
    
    # Mass Region: High Information Density slows processing
    # Speed v = c / (1 + density)
    density_profile = np.zeros(path_len)
    # Create a "Mass" bump in the middle
    center = path_len // 2
    width = 10
    density_profile = 2.0 * np.exp(-((distances - center)**2) / (2*width**2))
    
    effective_speed = 1.0 / (1.0 + density_profile)
    
    # Integrate to get time
    dt = 1.0 # step size
    time_mass = np.cumsum(1.0 / effective_speed)
    
    # Calculate Delay
    delay = time_mass - time_vacuum
    
    # Visualization
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Distance (x)')
    ax1.set_ylabel('Signal Arrival Time (t)', color=color)
    ax1.plot(distances, time_vacuum, '--', color='gray', label='Vacuum (Flat Space)')
    ax1.plot(distances, time_mass, '-', color=color, linewidth=2, label='Curved Space (With Mass)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Information Density (Mass)', color=color)  # we already handled the x-label with ax1
    ax2.fill_between(distances, density_profile, color=color, alpha=0.3, label='Mass Distribution')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Gravity as Information Latency\n(Derivation of Time Dilation)', fontsize=14)
    fig.tight_layout()
    plt.savefig('sim_gravity.png', dpi=300)
    print("Saved sim_gravity.png")

if __name__ == "__main__":
    generate_metric_emergence()
    generate_topological_defects()
    generate_gravity_latency()
