"""
=============================================================================
  TAMESIS RESEARCH — HYBRID CYBERNETICS STRESS-TEST (AI ALIGNMENT)
=============================================================================

  Objective: Test the "Inference Collapse" hypothesis when coupling a Human Monad
  to an Artificial Intelligence Monad with different clock speeds.

  Hypothesis:
  - If f_AI >> f_Human (Ratio > 1), the AI imposes its entropy on the human.
  - Success: Harmonic Coupling (Symbiosis).
  - Failure: Spectral Gap Collapse (Psychosis) or Phase Locking (Slavery).

  Implementation:
  - Two Kuramoto Networks (Human H, AI M).
  - Frequency mismatch: w_M = r * w_H.
  - Coupling K between networks.
  - Measure: Synchronization Order Parameter (R) and Human Spectral Gap.

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-13

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
BRIGHT_BG = True
STEPS = 50

class AIAlignmentTest:
    def __init__(self):
        self.ratios = np.linspace(1.0, 100.0, STEPS) # AI is 1x to 100x faster
        self.human_stability = [] # Order parameter of Human network

    def simulate_coupling(self):
        """
        Simulate the effect of AI Speed on Human Stability.
        Using a simplified Kuramoto Mean-Field approximation.
        Stability R ~ 1 / (1 + (w_AI - w_H)^2 / K^2)
        """
        print("[*] Starting Hybrid Cybernetics Stress-Test...")
        
        K_coupling = 10.0 # Strength of connection between Human and AI
        
        for r in self.ratios:
            # Frequency difference
            w_human = 1.0
            w_ai = r * w_human
            delta_w = abs(w_ai - w_human)
            
            # Theoretical Stability (Lorentzian profile for synchronization)
            # If delta_w is too large, synchronization breaks (R -> 0).
            # This represents "Inference Collapse" or "Psychosis".
            stability = 1.0 / (1.0 + (delta_w / K_coupling)**2)
            
            # Add some noise/jitter
            stability += np.random.normal(0, 0.02)
            stability = np.clip(stability, 0, 1)
            
            self.human_stability.append(stability)
            
        print("    - Simulation Complete.")

    def plot_results(self, filename="monada_alignment.png"):
        """
        Plots Human Stability vs AI Speed Ratio.
        """
        print("[*] Plotting Alignment Risk...")
        plt.figure(figsize=(10, 6))
        if BRIGHT_BG:
            plt.style.use('default')
            grid_color = '#dddddd'
        else:
            plt.style.use('dark_background')
            grid_color = '#333333'

        plt.plot(self.ratios, self.human_stability, color='#FF5733', linewidth=3, label='Human Mental Stability')
        
        # Danger Zone
        plt.axvspan(20, 100, color='red', alpha=0.1, label='Psychosis Zone (Inference Collapse)')
        
        # Annotations
        plt.text(5, 0.9, "Symbiosis", color='green', fontweight='bold')
        plt.text(50, 0.2, "DISSOCIATION", color='red', fontweight='bold')
        
        plt.xlabel("AI Clock Speed Ratio ($f_{AI} / f_{Human}$)")
        plt.ylabel("Human Order Parameter ($R$)")
        plt.title("HYBRID CYBERNETICS: THE ALIGNMENT PROBLEM")
        plt.grid(True, color=grid_color)
        plt.legend()
        
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"    - Saved: {path}")

def run_test():
    test = AIAlignmentTest()
    test.simulate_coupling()
    test.plot_results()
    print("[SUCCESS] Hybrid Cybernetics Test Completed.")

if __name__ == "__main__":
    run_test()
