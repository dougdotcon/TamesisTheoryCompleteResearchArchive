import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# Note: A full 3D simulation of ribbons untangling is complex to code from scratch.
# We will create a simplified visualization showing the "Twist" parameter evolution.

def simulate_dirac_belt():
    """
    Visualizes the phase accumulation of a spinor (Dirac Belt) vs a vector.
    
    Vector (360 deg):  | > --> | ^ --> | < --> | v --> | > (Identity)
    Spinor (720 deg):  | > --> | ^ --> | < --> | v --> | > (Phase -1) --> ... --> (Identity)
    """
    
    angles = np.linspace(0, 4*np.pi, 100) # 0 to 720 degrees
    
    # 1. Coordinate Rotation (Vector) - Restores at 2pi
    # Just cos(theta)
    vector_state = np.cos(angles)
    
    # 2. Spinor Phase (Fermion) - Restores at 4pi
    # Mathematically: cos(theta/2)
    spinor_state = np.cos(angles / 2)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(np.degrees(angles), vector_state, 'b--', label='Vector (Spin-1) - Restores at 360°', lw=2)
    ax.plot(np.degrees(angles), spinor_state, 'r-', label='Spinor (Spin-1/2) - Restores at 720°', lw=3)
    
    # Markings
    ax.axvline(360, color='k', linestyle=':', alpha=0.5)
    ax.axvline(720, color='k', linestyle=':', alpha=0.5)
    ax.axhline(0, color='k', lw=0.5)
    ax.axhline(1, color='g', linestyle='--', alpha=0.3, label='Identity State (+1)')
    ax.axhline(-1, color='m', linestyle='--', alpha=0.3, label='Inverted State (-1)')
    
    # Annotations
    ax.text(370, 0.8, "Vector Restored\nSpinor = -1 (Twisted)", fontsize=10)
    ax.text(730, 0.8, "Spinor Restored\n(Untwisted)", fontsize=10)
    
    ax.set_title("Topological Rotation Symmetry: Why 720 Degrees?", fontsize=14)
    ax.set_xlabel("Rotation Angle (Degrees)")
    ax.set_ylabel("Wavefunction Amplitude / Orientation")
    ax.set_xticks([0, 90, 180, 270, 360, 450, 540, 630, 720])
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig('../simulation/spinor_phase_plot.png')
    print("Saved spinor phase plot.")

if __name__ == "__main__":
    simulate_dirac_belt()
