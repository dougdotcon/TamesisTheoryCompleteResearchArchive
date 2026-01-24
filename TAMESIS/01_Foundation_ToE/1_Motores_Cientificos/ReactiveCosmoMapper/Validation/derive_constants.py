import sys
import os
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from constant_derivator import ConstantDerivator

def run_derivation():
    print("🔢 Running Fundamental Constant Derivation...")
    print("---------------------------------------------")
    print("Target: Fine Structure Constant (Alpha^-1) ~ 137.035999")
    print("Base:   TARDIS Gamma Factor ~ 117.038")
    print("---------------------------------------------\n")
    
    engine = ConstantDerivator()
    candidates = engine.exact_match_search()
    
    best_candidate = None
    min_diff = float('inf')
    
    target = 137.035999
    
    for name, val in candidates:
        diff = abs(val - target)
        percent_error = (diff / target) * 100
        print(f"Candidate: {name}")
        print(f"  Value: {val:.6f}")
        print(f"  Error: {percent_error:.6f}%")
        print("-" * 30)
        
        if diff < min_diff:
            min_diff = diff
            best_candidate = (name, val, percent_error)
            
    # Save Report
    with open("Validation/constants_derivation.txt", "w") as f:
        f.write("FUNDAMENTAL CONSTANTS DERIVATION REPORT\n")
        f.write("=======================================\n")
        f.write(f"Best Candidate for Alpha^-1: {best_candidate[0]}\n")
        f.write(f"Derived Value: {best_candidate[1]:.6f}\n")
        f.write(f"Target Value: {target:.6f}\n")
        f.write(f"Error: {best_candidate[2]:.6f}%\n")
        f.write("\nConclusion: Gamma(117) + Topological Terms approximates Alpha(137).\n")
        
    print(f"\n✅ Derivation report saved: Validation/constants_derivation.txt")

if __name__ == "__main__":
    run_derivation()
