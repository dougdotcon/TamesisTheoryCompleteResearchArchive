import numpy as np
from scipy.spatial import KDTree

class VoidScanner:
    def __init__(self, data_df):
        """
        Initialize with galaxy coordinates DataFrame [x, y, z].
        """
        self.data_xyz = data_df[['x', 'y', 'z']].values
        print(f"🕳️ VoidScanner initialized using {len(self.data_xyz)} galaxies.")
        
        # Build Tree for fast spatial queries
        self.tree = KDTree(self.data_xyz)
        
        # Define Survey Bounds (Bounding Box)
        # In a real survey like SDSS, geometry is complex (Mask). 
        # We approximate with the bounding box of the data.
        self.min_bounds = np.min(self.data_xyz, axis=0)
        self.max_bounds = np.max(self.data_xyz, axis=0)
        
        print(f"   - Volume Bounds: X[{self.min_bounds[0]:.1f}, {self.max_bounds[0]:.1f}]")

    def scan_for_voids(self, n_probes=100000):
        """
        Algorithm: Stochastic Spherical Underdensity (Zero-Density).
        1. Drop N random seeds in the volume.
        2. Find distance to nearest galaxy for each seed.
        3. This distance is the radius of the maximal empty sphere centered at that seed.
        """
        print(f"   - Scanning volume with {n_probes} random probes...")
        
        # 1. Generate Random Seeds
        seeds = np.random.uniform(self.min_bounds, self.max_bounds, (n_probes, 3))
        
        # 2. Query Nearest Neighbors
        # This returns the Euclidean distance to the closest galaxy
        radii, _ = self.tree.query(seeds, k=1)
        
        # 3. Edge Correction (Simple)
        # If a void radius is larger than distance to edge, it might be artificial.
        # Ideally we check against mask. Here we accept the raw distribution as "Internal + Edge"
        # For a comparative statistic, as long as we treat models same way, it's fine.
        
        return radii
