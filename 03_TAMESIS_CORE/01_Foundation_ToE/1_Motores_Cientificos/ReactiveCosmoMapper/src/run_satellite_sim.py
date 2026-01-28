from satellite_plane import SatelliteDynamics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🛸 Simulating 'Plane of Satellites' Formation...")
    
    sim = SatelliteDynamics(n_satellites=100, g_ext_factor=0.3)
    
    initial_pos, final_pos = sim.simulate(t_gyr=5.0)
    
    # Visualization
    fig = plt.figure(figsize=(12, 6))
    
    # Initial State
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(initial_pos[:,0], initial_pos[:,1], initial_pos[:,2], c='blue', s=5, alpha=0.6)
    ax1.set_title("Initial: Isotropic Sphere")
    ax1.set_xlim(-150, 150); ax1.set_ylim(-150, 150); ax1.set_zlim(-150, 150)
    
    # Final State
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(final_pos[:,0], final_pos[:,1], final_pos[:,2], c='orange', s=20, edgecolors='k')
    
    # Draw arrow for External Field
    ax2.quiver(0, 0, 0, 0, 0, 100, color='red', length=1.0, label='External Field')
    
    ax2.set_title("Final (Reactive Gravity + EFE)")
    ax2.set_xlim(-150, 150); ax2.set_ylim(-150, 150); ax2.set_zlim(-150, 150)
    
    plt.suptitle("Symmetry Breaking by External Field Effect")
    plt.savefig("Validation/satellite_plane_collapse.png")
    print("✅ Simulation saved to Validation/satellite_plane_collapse.png")

if __name__ == "__main__":
    main()
