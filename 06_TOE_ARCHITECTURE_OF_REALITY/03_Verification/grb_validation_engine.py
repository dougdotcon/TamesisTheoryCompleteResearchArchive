import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Constants
C = 299792458.0  # Speed of light (m/s)
H_BAR = 1.0545718e-34 # Reduced Planck constant (J*s)
G_CONST = 6.674e-11   # Gravitational constant (m^3 kg^-1 s^-2)
# Planck Energy in GeV
# E_pl = sqrt(hbar * c^5 / G)
# 1 Joule = 6.242e+9 GeV
E_PLANCK_J = np.sqrt(H_BAR * C**5 / G_CONST)
E_PLANCK_GEV = E_PLANCK_J * 6.242e9  # ~ 1.22e19 GeV

class TamesisVerification:
    def __init__(self):
        print(f"[Tamesis] Initializing Verification Engine...")
        print(f"[Tamesis] Planck Energy: {E_PLANCK_GEV:.2e} GeV")
        
    def norris_pulse(self, t, t_start, A, tau1, tau2):
        """
        Standard GRB Pulse Model (Norris et al. 2005).
        I(t) = A * lambda * exp(-tau1/(t-t_s) - (t-t_s)/tau2)
        """
        # Avoid division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            val = A * np.exp(-tau1 / (t - t_start) - (t - t_start) / tau2)
        val[np.isnan(val)] = 0
        val[t <= t_start] = 0
        return val

    def generate_light_curve(self, time_bins, energies_gev):
        """
        Generates a synthetic light curve for a given energy band.
        Higher energy -> Typically narrower pulses (not modeled here for simplicity)
        """
        # GRB 090510-like parameters (Short GRB)
        intensity = np.zeros_like(time_bins)
        
        # Main pulse
        intensity += self.norris_pulse(time_bins, t_start=0.5, A=100, tau1=0.01, tau2=0.1)
        # Secondary pulse
        intensity += self.norris_pulse(time_bins, t_start=0.7, A=50, tau1=0.02, tau2=0.2)
        
        # Add Poisson Noise
        # noise = np.random.normal(0, 2, size=len(time_bins))
        # intensity += noise
        
        return np.maximum(intensity, 0)

    def calculate_tamesis_delay(self, E_high_gev, E_low_gev, distance_gpc, xi):
        """
        Calculates predicted time delay based on Tamesis Dispersion Relation:
        dt = xi * (E_high - E_low) / E_pl * D / c
        """
        # Convert Distance Gpc to meters
        D_meters = distance_gpc * 3.086e25 
        
        # Energy difference
        dE = E_high_gev - E_low_gev
        
        # Delay calculation
        dt = xi * (dE / E_PLANCK_GEV) * (D_meters / C)
        return dt

    def measure_lag(self, t, signal_low, signal_high):
        """
        Measures time lag using Cross-Correlation Function (CCF).
        """
        correlation = signal.correlate(signal_high, signal_low, mode='full')
        lags = signal.correlation_lags(len(signal_low), len(signal_high), mode='full')
        dt_bin = t[1] - t[0]
        lag_bins = lags[np.argmax(correlation)]
        lag_time = lag_bins * dt_bin
        return lag_time

    def run_simulation(self):
        # Simulation Parameters
        T_DURATION = 2.0 # seconds
        DT_BIN = 0.001   # 1 ms resolution
        time_bins = np.arange(0, T_DURATION, DT_BIN)
        
        # GRB 090510 Parameters
        DISTANCE_GPC = 1.8 # z=0.903 approx
        E_LOW = 0.001 # 1 MeV
        E_HIGH = 30.0 # 30 GeV
        FERMI_LIMIT_MS = 30.0
        
        # Generate 'Clean' Light Curve (Low Energy Reference)
        lc_low = self.generate_light_curve(time_bins, E_LOW)
        
        print(f"\n--- PHASE 1: LINEAR TAMESIS CHECK ---")
        # 1. Calculate Lag for xi=1
        XI_TEST = 1.0 
        theoretical_lag = self.calculate_tamesis_delay(E_HIGH, E_LOW, DISTANCE_GPC, XI_TEST)
        print(f"[Tamesis] Theoretical Lag for xi={XI_TEST}: {theoretical_lag*1000:.4f} ms")
        
        # 2. Find Xi Limit
        print(f"\n--- PHASE 2: FINDING Xi LIMIT (target < {FERMI_LIMIT_MS} ms) ---")
        xi_limit = FERMI_LIMIT_MS / (theoretical_lag * 1000)
        print(f"[Analysis] Fermi Constraint: |dt| < {FERMI_LIMIT_MS} ms")
        print(f"[Result] Tamesis Coupling Limit: xi < {xi_limit:.4f}")
        print(f"Interpreation: The graph 'smoothness' is > {100*(1-xi_limit):.1f}% efficient.")

        # Re-run with Limit
        lag_at_limit = self.calculate_tamesis_delay(E_HIGH, E_LOW, DISTANCE_GPC, xi_limit)
        
        # 3. Quadratic Suppression Check
        print(f"\n--- PHASE 3: QUADRATIC SUPPRESSION CHECK ---")
        # dt_quad ~ xi * (E^2 / E_pl^2) * D / c
        # The linear term was (E/E_pl). Ratio is E/E_pl ~ 30 / 1e19 ~ 3e-18
        # Quadratic lag will be ~ 455ms * 3e-18 ~ 1e-15 ms.
        lag_quad = theoretical_lag * (E_HIGH / E_PLANCK_GEV)
        print(f"[Tamesis] Quadratic Lag (xi=1): {lag_quad*1000:.4e} ms (Undetectable)")

        # Inject Delay at Limit for Plotting
        shift_bins = int(lag_at_limit / DT_BIN)
        lc_high = np.roll(lc_low, shift_bins)
        if shift_bins > 0:
            lc_high[:shift_bins] = 0
            
        # Add Noise
        np.random.seed(42)
        lc_low_noisy = lc_low + np.random.normal(0, 5, size=len(lc_low))
        lc_high_noisy = lc_high + np.random.normal(0, 5, size=len(lc_high))
        
        # Measure
        measured_lag = self.measure_lag(time_bins, lc_low_noisy, lc_high_noisy)
        print(f"\n[Validation] Simulated Lag at xi={xi_limit:.4f}: {measured_lag*1000:.4f} ms")

        # Plotting
        plt.figure(figsize=(10, 8))
        
        plt.subplot(2, 1, 1)
        plt.title(f"Tamesis Refinement: Constraining Graph Granularity\nTarget: Fermi Limit (<30ms) -> Result: xi < {xi_limit:.3f}")
        plt.plot(time_bins, lc_low_noisy, label=f'Low Energy (Ref)', color='blue', alpha=0.6)
        plt.plot(time_bins, lc_high_noisy, label=f'High Energy (Shifted by Limit)', color='red', alpha=0.6)
        plt.fill_between(time_bins, 0, 150, where=(time_bins > 0.5) & (time_bins < 0.53 + lag_at_limit), color='red', alpha=0.1, label='Forbidden Lag Region (Excluded)')
        plt.legend()
        plt.ylabel("Counts")
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 1, 2)
        plt.title("Parameter Space Exclusion")
        plt.barh(['Linear (xi=1)', 'Fermi Limit (xi~0.06)', 'Quadratic'], [455, 30, 1e-12], color=['red', 'orange', 'green'])
        plt.xlabel("Lag (ms) - Log Scale")
        plt.xscale('log')
        plt.axvline(30, color='red', linestyle='--', label='Fermi Detection Threshold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('d:/TamesisTheoryCompleteResearchArchive/14_VERIFICATION_TAMESIS_THEORY/tamesis_constraints.png')
        print("[Output] Constraints plot saved.")

if __name__ == "__main__":
    engine = TamesisVerification()
    engine.run_simulation()
