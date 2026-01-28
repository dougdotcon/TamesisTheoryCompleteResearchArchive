import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cmb_solver import CMBSolver

def run_simulation():
    print("🌌 Starting Axis of Evil Simulation...")
    print("----------------------------------------")
    
    try:
        solver = CMBSolver()
        
        # 1. Run standard Power Spectrum (Baseline)
        print("1. Generanting Power Spectrum...")
        solver.plot_power_spectrum()
        
        # 2. Run new Axis of Evil map
        print("2. Simulating Rotating Universe / Axis of Evil...")
        solver.simulate_axis_of_evil()
        
        print("\n✅ Simulation Complete.")
        print("Output files check:")
        
        files = [
            "Validation/cmb_power_spectrum.png",
            "Validation/cmb_axis_of_evil.png"
        ]
        
        for f in files:
            if os.path.exists(f):
                print(f"  [FOUND] {f} - {os.path.getsize(f)} bytes")
            else:
                print(f"  [MISSING] {f}")
                
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_simulation()
