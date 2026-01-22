import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from evaporating_universe import EvaporatingUniverse

def run_escatology_sim():
    print("⏳ Starting Escatologia Simulation (End Times)...")
    print("------------------------------------------------")
    
    universe = EvaporatingUniverse()
    
    # 1. Calculate fundamental stats
    M0 = universe.mass_kg
    T0 = universe.hawking_temperature()
    dM0 = universe.mass_loss_rate()
    life0 = universe.lifetime()
    
    print(f"Initial Universe Mass: {M0:.2e} kg")
    print(f"Current Hawking Temp:  {T0:.2e} K (Ultra-cold)")
    print(f"Mass Loss Rate:        {dM0:.2e} kg/s")
    print(f"Time to End:           {life0:.2e} s")
    print(f"                       {life0 / (3.15e7):.2e} years")
    
    # 2. Simulate Evolution
    print("\nSimulating decay timeline...")
    time, mass = universe.time_evolution()
    
    # Plotting Mass Decay
    plt.figure(figsize=(10, 6))
    plt.plot(time / (3.15e7), mass / M0, 'r-', linewidth=2)
    plt.xlabel('Time (Years)')
    plt.ylabel('Mass Fraction $M(t)/M_0$')
    plt.title('The Fate of the Universe: Hawking Evaporation Timeline')
    plt.grid(True, alpha=0.3)
    plt.yscale('linear')
    plt.xscale('log') # Log scale for time because it's huge
    
    output_path = "Validation/universe_lifetime_plot.png"
    plt.savefig(output_path)
    print(f"✅ Lifetime plot saved: {output_path}")
    
    # 3. Save Doomsday Clock
    with open("Validation/doomsday_clock.txt", "w") as f:
        f.write("DOOMSDAY CLOCK REPORT\n")
        f.write("=====================\n")
        f.write(f"Mass (kg): {M0}\n")
        f.write(f"Temperature (K): {T0}\n")
        f.write(f"Evaporation Rate (kg/s): {dM0}\n")
        f.write(f"Years Remaining: {life0 / (3.15e7)}\n")
        f.write("Status: The Universe is slowly evaporating.\n")
        
    print("✅ Report saved to doomsday_clock.txt")

if __name__ == "__main__":
    run_escatology_sim()
