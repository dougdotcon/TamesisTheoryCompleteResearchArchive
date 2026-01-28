import pandas as pd
import numpy as np
from astropy.cosmology import Planck15
from astropy import units as u
from astropy.coordinates import SkyCoord
import os
from scipy.spatial import KDTree

class GalaxyVisualizer:
    """
    Visualization engine for ReactiveCosmoMapper.
    Converts observational coordinates (RA, Dec, z) to 3D Cartesian structure (Mpc).
    Exports to Wavefront OBJ format for external rendering.
    """
    
    def __init__(self, data_file="data/sdss_sample.csv"):
        self.data_file = data_file
        self.coords_3d = None # DataFrame x, y, z

    def load_and_transform(self):
        """Loads SDSS data and converts to Cartesian coordinates."""
        if not os.path.exists(self.data_file):
            print(f"❌ File {self.data_file} not found.")
            return None
            
        print("Dataset loaded. Computing distances from Redshift...")
        df = pd.read_csv(self.data_file)
        
        # Filter valid redshift
        df = df[df['redshift'] > 0].copy()
        
        # Distance calculation using Hubble's Law approximation for low z
        # or proper cosmological distance for higher z
        # Using simple Hubble flow for speed: D = c*z / H0
        # H0 ~ 70 km/s/Mpc. c = 300,000 km/s.
        # D_mpc = (300000 * z) / 70 = 4285 * z
        # Or use astropy for accuracy
        
        distances = Planck15.comoving_distance(df['redshift'].values)
        
        # Convert Spherical (RA, Dec, Dist) to Cartesian (X, Y, Z)
        c = SkyCoord(
            ra=df['ra'].values * u.degree, 
            dec=df['dec'].values * u.degree, 
            distance=distances
        )
        
        cartesian = c.cartesian
        
        self.coords_3d = pd.DataFrame({
            'x': cartesian.x.value, # Mpc
            'y': cartesian.y.value,
            'z': cartesian.z.value,
            'redshift': df['redshift'].values
        })
        
        print(f"✅ Transformed {len(self.coords_3d)} galaxies to 3D Cartesian space.")
        return self.coords_3d

    def export_to_obj(self, output_filename="reactive_universe.obj", filament_threshold_mpc=10.0):
        """
        Exports the galaxy distribution as a Wavefront OBJ file.
        Creates "filaments" (lines) between galaxies closer than threshold to simulate the cosmic web.
        """
        if self.coords_3d is None:
            self.load_and_transform()
            
        print(f"generating 3D model: {output_filename}...")
        
        points = self.coords_3d[['x', 'y', 'z']].values
        
        with open(output_filename, 'w') as f:
            f.write(f"# ReactiveCosmoMapper Export\n")
            f.write(f"# Vertices: {len(points)}\n")
            
            # Write Vertices
            for p in points:
                # Scale down for viewer comfort if necessary, or keep raw Mpc
                # Keeping raw Mpc might be huge for some viewers, let's normalize?
                # Usually viewers handle large floats okay, but let's center it.
                f.write(f"v {p[0]:.4f} {p[1]:.4f} {p[2]:.4f}\n")
                
            # Generate Filaments (Edges)
            # Use KDTree for efficient neighbor search
            print("Constructing Gravity Tunnels (KDTree)...")
            tree = KDTree(points)
            
            # Find pairs within threshold
            # query_pairs returns a set of pairs (i, j)
            pairs = tree.query_pairs(r=filament_threshold_mpc)
            
            f.write(f"\n# Filaments (Threshold: {filament_threshold_mpc} Mpc)\n")
            f.write(f"# Edges: {len(pairs)}\n")
            
            for i, j in pairs:
                # OBJ indices are 1-based
                f.write(f"l {i+1} {j+1}\n")
                
        print(f"✅ Export Complete: {output_filename}")
        print(f"   - Vertices (Galaxies): {len(points)}")
        print(f"   - Lines (Tunnels): {len(pairs)}")

if __name__ == "__main__":
    viz = GalaxyVisualizer()
    viz.load_and_transform()
    viz.export_to_obj()
