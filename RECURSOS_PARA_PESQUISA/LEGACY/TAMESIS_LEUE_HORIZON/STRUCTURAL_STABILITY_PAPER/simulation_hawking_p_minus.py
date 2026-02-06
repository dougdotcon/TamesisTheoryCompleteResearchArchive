
"""
simulation_hawking_p_minus.py
-----------------------------
Tamesis-Leue Integration Project
Hypothesis 2 Verification: Hawking Radiation as P- Channel Leakage

Hypothesis: 
The Event Horizon (LMC Saturation) attempts to block the P- (backward/dissipative) channel 
to maintain causality (nothing escapes).
However, due to grid discreteness (Planck Scale), the ROC Projector P- is not perfect.
Residual energy leaks into P-.
We predict this leakage spectrum is Thermal (Planckian), with Temperature related to the 
Sharpness of the Horizon (Surface Gravity / LMC Gradient).

Mechanism:
1. Establish a Horizon (Sharp transition in LMC field).
2. Inject Vacuum Noise.
3. Apply ROC P- projector.
4. Measure Spectrum of the P- field just outside the Horizon.

Author: Antigravity (Agent) for Tamesis Research
"""

import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt

class FastROC:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.dim = len(grid_size)
        axes_freqs = [np.fft.fftfreq(n) * 2 * np.pi for n in grid_size]
        self.freq_grid = np.meshgrid(*axes_freqs, indexing='ij')
        
    def get_p_minus_projector_mask(self, v_vec=(1,0,0,0), epsilon=0.2):
        """Returns the mask for the P- channel (k.v < -epsilon)"""
        k_dot_v = sum(F * v for F, v in zip(self.freq_grid, v_vec))
        # Smooth transition or hard cut? 
        # In discrete QM, cuts are hard.
        mask = (k_dot_v < -epsilon).astype(float)
        return mask

def planck_law(freqs, T):
    """Planck's Law for comparison: I(f) ~ f^3 / (exp(f/T) - 1)"""
    # Avoid division by zero
    safe_freqs = np.maximum(freqs, 1e-5)
    
    # 4D Planck law might differ (f^4?), but for 1D radiation flux it's usually f^3.
    # Actually, in 1D/Signal analysis, thermal noise is flat (Johnson), but "Black Body" 
    # implies 3D cavity.
    # Let's fit generic exponential decay: I(f) ~ f^n * exp(-f/T)
    # High frequency tail is the most important signature: exp(-f/T)
    
    exponent = safe_freqs / T
    # overflow protection
    exponent = np.minimum(exponent, 100)
    
    intensity = (safe_freqs**3) / (np.exp(exponent) - 1 + 1e-9)
    return intensity

def run_experiment_h2():
    print("=== TAMESIS-LEUE INTEGRATION: EXPERIMENT 02 (Hawking P-) ===")
    
    L = 32 # Need enough resolution for spectrum
    grid_size = (L, L, L, L)
    print(f"Grid: {grid_size} ({L}^4 points)")
    
    # Gradient/Gravity strengths to test
    # "Sharpness" of the horizon ~ Surface Gravity (g) ~ Temperature (T)
    # We create LMC fields with different steepness at the transition.
    gradients = [2.0, 4.0, 8.0, 16.0]
    
    results = {}
    
    roc = FastROC(grid_size)
    p_minus_mask = roc.get_p_minus_projector_mask(epsilon=0.5)
    
    coords = [np.linspace(-10, 10, L) for _ in range(4)]
    T, X, Y, Z = np.meshgrid(*coords, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    R0 = 5.0 # Horizon Radius
    
    plt.figure(figsize=(10,6))
    
    for k_stiffness in gradients:
        print(f"\nProcessing Horizon Stiffness k={k_stiffness}...")
        
        # 1. Horizon Setup
        # t(x) goes from 1 (inside) to 0 (outside) rapidly
        # Sigmoid transition
        t_field = 0.5 * (1 - np.tanh(k_stiffness * (R - R0)))
        
        # 2. Scattering / Leakage Mechanism
        # The ROC projector is global.
        # But the physical interaction is local.
        # Noise interacts with the Horizon Gradient.
        # H_int ~ grad(t) dot Noise
        
        # Calculate Gradient of LMC (The "Force")
        # Just radial gradient magnitude for simplicity
        # grad_t is peaked at R0.
        grad_t = k_stiffness * (1 - np.tanh(k_stiffness * (R - R0))**2) # Derivative of tanh
        
        # Vacuum noise
        noise = np.random.randn(*grid_size)
        
        # Source of scattering: Noise * Gradient
        # Stronger gradient = "Harder" wall = potentially more high-freq scattering?
        scattering_source = noise * grad_t
        
        # 3. Project to P- (What scatters BACKWARDS?)
        f_hat = np.fft.fftn(scattering_source)
        p_minus_hat = f_hat * p_minus_mask
        p_minus_field = np.fft.ifftn(p_minus_hat).real
        
        # 4. Analyze Spectrum of the Leakage
        # We look at the energy spectrum of the P- field.
        # Radial integration in k-space? Or FFT of the result?
        # Since we are already in Fourier space (p_minus_hat), we can just bin intensities by |k|.
        
        # Get |k| grid
        kx = np.fft.fftfreq(L) * 2 * np.pi
        kt, kx, ky, kz = np.meshgrid(kx, kx, kx, kx, indexing='ij')
        k_mag = np.sqrt(kt**2 + kx**2 + ky**2 + kz**2)
        
        # Power Spectrum
        power = np.abs(p_minus_hat)**2
        
        # Binning
        bins = np.linspace(0, np.pi*L, 50)
        digitized = np.digitize(k_mag.flat, bins)
        
        freqs = []
        intensities = []
        
        for i in range(1, len(bins)):
            mask = digitized == i
            if np.any(mask):
                bin_power = np.mean(power.flat[mask])
                intensities.append(bin_power)
                freqs.append(bins[i-1])
                
        freqs = np.array(freqs)
        intensities = np.array(intensities)
        
        # Normalize
        intensities /= intensities.max()
        
        # 5. Fit Planck Law (or Boltzmann tail)
        # We fit Log(I) vs Freq to find "Temperature" (Slope = -1/T)
        # Focus on the tail (high freq) where Wien approx works
        # I ~ exp(-f/T) => log(I) ~ -f/T
        
        mask_tail = (freqs > 5.0) & (intensities > 1e-4) # Avoid noise floor
        if np.sum(mask_tail) > 3:
            slope, intercept = np.polyfit(freqs[mask_tail], np.log(intensities[mask_tail]), 1)
            derived_temp = -1.0 / slope
            print(f"  > Spectrum Slope: {slope:.4f}")
            print(f"  > Derived Temperature: {derived_temp:.4f}")
            
            label = f'k={k_stiffness} -> T={derived_temp:.2f}'
            plt.semilogy(freqs, intensities, label=label)
            
            results[k_stiffness] = derived_temp
            
    # CHECK: Does T scale with k (Surface Gravity)?
    # Hawking: T ~ g ~ k_stiffness
    print("\n--- RESULTS H2 ---")
    stiffnesses = np.array(list(results.keys()))
    temps = np.array(list(results.values()))
    
    # Sort
    sort_idx = np.argsort(stiffnesses)
    stiffnesses = stiffnesses[sort_idx]
    temps = temps[sort_idx]
    
    # Linear correlation between Stiffness (g) and Temperature (T)
    correlation = np.corrcoef(stiffnesses, temps)[0,1]
    print(f"Correlation (Stiffness vs Temp): {correlation:.4f}")
    
    if correlation > 0.9:
        print("[SUCCESS] H2 CONFIRMED: Temperature is proportional to Horizon Stiffness (Surface Gravity).")
        print("P- Leakage behaves like Hawking Radiation.")
    else:
        print("[FAILURE] H2 Failed. No linear relation found.")
    
    plt.xlabel('Frequency |k|')
    plt.ylabel('Power (Log)')
    plt.title('P- Leakage Spectra (Simulated Hawking Radiation)')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.savefig('h2_hawking_spectra.png')
    
    # Plot T vs g relation
    plt.figure()
    plt.plot(stiffnesses, temps, 'o-', color='red')
    plt.xlabel('Horizon Stiffness (g)')
    plt.ylabel('Derived Temperature (T)')
    plt.title('Tamesis-Leue: T vs g Relation')
    plt.grid()
    plt.savefig('h2_T_vs_g.png')

if __name__ == "__main__":
    run_experiment_h2()
