from lensing_projector import LensingProjector
from visualizer import GalaxyVisualizer
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("👁️ Starting Weak Lensing Tomography...")
    
    # 1. Load Data
    viz = GalaxyVisualizer(data_file="data/sdss_sample.csv")
    df = viz.load_and_transform()
    
    if df is None:
        return

    # 2. Initialize Projector (500 Mpc box, 128^3 grid)
    # Adjust box size to match data spread (approx -250 to 250)
    # df goes from approx -300 to 600?
    # Let's measure bounds
    min_v = df[['x','y','z']].min().min()
    max_v = df[['x','y','z']].max().max()
    box_size = max_v - min_v
    print(f"   - Data Scope: {min_v:.1f} to {max_v:.1f} Mpc")
    
    # We realign data in the class, so passing size is enough
    lp = LensingProjector(df, box_size_mpc=box_size*1.1, grid_res=128)
    
    # 3. Compute
    s_bar, s_eff = lp.compute_convergence_map()
    
    # 4. Visualize
    lp.plot_maps(s_bar, s_eff)

if __name__ == "__main__":
    main()
