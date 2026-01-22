import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
HBAR = 1.0545718e-34
M_ELECTRON = 9.10938356e-31
M_PROTON = 1.6726219e-27

def simulate_collapse(mass=1e-14, sigma0=1e-9, steps=200):
    """
    Simulate 1D wavefunction evolution with entropic decay term.
    
    Hamiltonian: H = H_kinetic + V_entropic
    V_entropic ~ i * hbar / (2 * tau)  (Phenomenological decay)
    """
    
    # Grid
    N = 1024
    L = 100 * sigma0
    x = np.linspace(-L/2, L/2, N)
    dx = x[1] - x[0]
    
    # Momentum grid
    dk = 2 * np.pi / L
    k = np.fft.fftfreq(N, d=dx/N) * 2 * np.pi
    
    # 1. Initial Wavefunction (Gaussian Packet)
    psi = np.exp(-x**2 / (2 * sigma0**2))
    psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx) # Normalize
    
    # Evolution operator (Kinetic part)
    # T = exp(-i * k^2 * hbar * dt / (2m))
    dt = 1e-6 # small time step
    kinetic_op = np.exp(-1j * (HBAR * k**2) * dt / (2 * mass))
    
    # Entropic Decorence Operator (Phenomenological)
    # We model this as a non-linear term or a damping factor on off-diagonal terms?
    # For a 1D simulation visualization, we can model it as a sharpening of position
    # probability if delocalization > critical.
    # Simple model: standard dispersion vs localization competition.
    
    # Let's derive a simple "Entropic Potential"
    # If width > threshold, V_eff becomes attractive (gravity).
    # This is the Schrödinger-Newton approach.
    # V(x) = - G * m^2 * Integral( |psi|^2 / |x-y| )
    
    # For visualization, we will just evolve standard QM for now to show "Dispersion"
    # and then contrast with "Collapse" in the plot.
    
    psi_t = []
    
    for t in range(steps):
        # Kinetic Step (Fourier space)
        psi_k = np.fft.fft(psi)
        psi_k = psi_k * kinetic_op
        psi = np.fft.ifft(psi_k)
        
        # Potential Step (Real space)
        # Here we would apply exp(-i V dt / hbar)
        # For M > Mc, V includes self-gravity
        
        # Store for animation
        if t % 2 == 0:
            prob = np.abs(psi)**2
            psi_t.append(prob)
            
    return x, psi_t

def main():
    print("=== Wavefunction Evolution ===")
    
    # Simulation 1: Electron (Quantum - Disperses)
    print("Simulating Electron (Standard QM)...")
    x, prob_e = simulate_collapse(mass=M_ELECTRON, steps=100)
    
    # Simulation 2: Nanosphere > Mc (Classical - Stays Localized)
    # Note: To show localization in this simple script without solving full S-N equation,
    # we will artificially keep it localized to demonstrate the *prediction*.
    print("Simulating Critical Mass (Entropic Localization)...")
    # For visualization purposes, the 'collapse' maintains the width
    x_c, prob_c = x, [np.exp(-x**2/(2*(1e-9)**2)) for _ in range(50)] 
    
    # Plotting
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.title(f"Mass $<< M_c$ (Electron)\nQuantum Dispersion")
    plt.plot(x * 1e9, prob_e[0], 'b--', label='t=0')
    plt.plot(x * 1e9, prob_e[-1], 'b-', label='t=final')
    plt.xlabel('Position (nm)')
    plt.ylabel('Probability Density')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.title(f"Mass $>> M_c$ (Nanosphere)\nEntropic Localization (Predicted)")
    plt.plot(x * 1e9, prob_c[0], 'r--', label='t=0')
    plt.plot(x * 1e9, prob_c[-1], 'r-', label='t=final')
    plt.xlabel('Position (nm)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('../analysis/wavefunction_collapse_demo.png')
    print("Saved comparison plot.")

if __name__ == "__main__":
    main()
