import pandas as pd
import numpy as np
from reactive_gravity import ReactiveGravity
from data_ingestor import DataIngestor
import matplotlib.pyplot as plt
import os

class ReactiveCosmoMapper:
    """
    Main class that orchestrates:
    1. Data Ingestion (SPARC/SDSS)
    2. Physics Calculation (ReactiveGravity)
    3. Comparison/Visualization
    """
    
    def __init__(self, data_dir="data"):
        self.ingestor = DataIngestor(data_dir=data_dir)
        self.gravity = ReactiveGravity()
        self.sparc_data = None
        self.sdss_data = None

    def load_data(self):
        """Loads data into memory."""
        self.sparc_data = self.ingestor.get_sparc_data()
        self.sdss_data = self.ingestor.get_sdss_sample(limit=500)

    def analyze_galaxy(self, galaxy_name):
        """
        Analyzes a specific galaxy from SPARC dataset.
        Compares observed velocity with:
        - Newtonian Prediction (Stellar Mass Only)
        - Entropic Prediction (Stellar Mass + Reactive Correction)
        """
        if self.sparc_data is None:
            print("Data not loaded. Loading now...")
            self.load_data()
            
        galaxy = self.sparc_data[self.sparc_data['Galaxy'] == galaxy_name]
        
        if galaxy.empty:
            print(f"Galaxy {galaxy_name} not found.")
            return None
        
        # In SPARC, usually we just have total Mstar, Mgas, and Vflat.
        # But for a proper rotation curve plot, we need the radial profile data.
        # The SPARC Master file only has global properties.
        # For this prototype, we will simulate a rotation curve based on the Total Mass 
        # assuming an exponential disk profile, just to demonstrate the physics.
        
        mass_star = galaxy.iloc[0]['Mstar'] * 1e9 * self.gravity.M_sun # Solar masses to kg
        mass_gas = galaxy.iloc[0]['Mgas'] * 1e9 * self.gravity.M_sun
        v_flat_obs = galaxy.iloc[0]['Vflat'] # km/s
        
        total_mass = mass_star + mass_gas
        
        # Simulate radii from 1 kpc to 20 kpc
        radii_kpc = np.linspace(1, 20, 50)
        radii_m = radii_kpc * 3.086e19
        
        v_newton = []
        v_entropic = []
        
        for r in radii_m:
            # Simple Point Mass Approx for demonstration (valid at large radii)
            # v_n = self.gravity.calculate_velocity(total_mass, r) -> This calls calculate_velocity which uses calculate_effective_acceleration
            
            # Use raw Newtonian calc for comparison
            g_n = self.gravity.calculate_newtonian_acceleration(total_mass, r)
            v_n = np.sqrt(g_n * r) / 1000.0 # km/s
            v_newton.append(v_n)
            
            # Entropic calc
            v_e = self.gravity.calculate_velocity(total_mass, r)
            v_entropic.append(v_e)
            
        return {
            'radii_kpc': radii_kpc,
            'v_newton': v_newton,
            'v_entropic': v_entropic,
            'v_flat_obs': v_flat_obs,
            'galaxy_name': galaxy_name
        }

    def plot_comparison(self, analysis_result):
        """Generates a plot comparing the models."""
        if analysis_result is None:
            return
            
        plt.figure(figsize=(10, 6))
        plt.plot(analysis_result['radii_kpc'], analysis_result['v_newton'], '--', label='Newtonian (Baryons Only)')
        plt.plot(analysis_result['radii_kpc'], analysis_result['v_entropic'], '-', linewidth=2, label='Reactive/Entropic Gravity')
        plt.axhline(y=analysis_result['v_flat_obs'], color='r', linestyle=':', label=f"Observed Vflat ({analysis_result['v_flat_obs']} km/s)")
        
        plt.xlabel('Radius (kpc)')
        plt.ylabel('Velocity (km/s)')
        plt.title(f"Rotation Curve: {analysis_result['galaxy_name']}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig(f"{analysis_result['galaxy_name']}_rotation.png")
        print(f"✅ Plot saved: {analysis_result['galaxy_name']}_rotation.png")

if __name__ == "__main__":
    mapper = ReactiveCosmoMapper()
    mapper.load_data()
    
    # Example: Analyze a galaxy if data exists
    # Just picking the first one from SPARC dataframe for test
    if mapper.sparc_data is not None and not mapper.sparc_data.empty:
        first_galaxy = mapper.sparc_data.iloc[0]['Galaxy']
        print(f"Analyzing first galaxy: {first_galaxy}")
        results = mapper.analyze_galaxy(first_galaxy)
        mapper.plot_comparison(results)
