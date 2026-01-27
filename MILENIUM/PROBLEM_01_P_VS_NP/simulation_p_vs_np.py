
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt
import os

# Configuration for reproducible results
np.random.seed(42)

def create_sk_hamiltonian(N, J=1.0):
    """
    Creates the Sherrington-Kirkpatrick Hamiltonian for N spins
    PLUS local random fields to break symmetry (mimicking 3-SAT).
    H = - sum_{i<j} J_{ij} sigma_i sigma_j - sum_i h_i sigma_i
    
    Returns: (interactions_matrix, fields_vector)
    """
    # Random couplings
    interactions = np.random.normal(0, J, size=(N, N))
    interactions = (interactions + interactions.T) / 2
    np.fill_diagonal(interactions, 0)
    
    # Random local fields (breaking Z2 symmetry)
    fields = np.random.normal(0, J, size=N)
    
    return interactions, fields

def get_spectrum(interactions, N):
    """
    Exact Diagonalization to find the full spectrum.
    WARNING: Exponential cost O(2^N). Keep N <= 12.
    """
    dim = 2**N
    hamiltonian_matrix = np.zeros((dim, dim))
    
    # Iterate through all basis states
    for i in range(dim):
        # Convert integer i to spin configuration (-1, +1)
        # Using bit manipulation
        spins = np.array([1 if (i >> b) & 1 else -1 for b in range(N)])
        
        # Calculate energy for this state basis state
        # E = -0.5 * sum(J_ij * s_i * s_j)
        energy = -0.5 * np.dot(spins, np.dot(interactions, spins))
        hamiltonian_matrix[i, i] = energy
        
    # Find eigenvalues (energies are on diagonal for classical Ising, 
    # but strictly we are looking at the classical energy landscape. 
    # For Quantum Adiabatic, we would add a transverse field term B * sum(sigma_x).
    # Here let's stay classical landscape to show the gap in density of states closer to GS.
    
    # Actually, for "Spectral Gap" in the context of AQC/Adiabatic, 
    # we need the Quantum Hamiltonian: H(t) = (1-s)H_init + s H_problem.
    # The minimum gap occurs at the critical point.
    
    return np.diag(hamiltonian_matrix)

def get_quantum_gap_min(interactions, fields, N, steps=20):
    """
    Simulates the Adiabatic passage and finds the MINIMUM GAP.
    H(s) = (1-s) * (- sum sigma_x) + s * H_problem
    """
    dim = 2**N
    
    # H_problem (Diagonal in Z-basis)
    h_problem_diag = np.zeros(dim)
    for i in range(dim):
        spins = np.array([1 if (i >> b) & 1 else -1 for b in range(N)])
        # E = -0.5 * sigma^T J sigma - h^T sigma
        term_J = -0.5 * np.dot(spins, np.dot(interactions, spins))
        term_h = -np.dot(fields, spins)
        h_problem_diag[i] = term_J + term_h
    
    # H_driver (Transverse Field - sum sigma_x)
    # This matrix connects states with hamming distance 1
    rows = []
    cols = []
    data = []
    
    for i in range(dim):
        for bit in range(N):
            target = i ^ (1 << bit) # Flip one bit
            rows.append(i)
            cols.append(target)
            data.append(-1.0) # - sum sigma_x
            
    # We build dense for simplicity as N is small
    h_driver = np.zeros((dim, dim))
    for r, c, d in zip(rows, cols, data):
        h_driver[r, c] = d
        
    # Scan s from 0 to 1
    s_values = np.linspace(0, 1, steps)
    gaps = []
    
    for s in s_values:
        H_total = (1-s) * h_driver + np.diag(s * h_problem_diag)
        # Get lowest 2 eigenvalues
        # Since matrix is real symmetric, use eigh
        eigvals = la.eigh(H_total, eigvals_only=True, subset_by_index=[0, 1])
        gaps.append(eigvals[1] - eigvals[0])
        
    return min(gaps)

def simulation_gap_scaling():
    """
    Simulates Gap vs N
    """
    N_range = range(3, 11) # Small N due to exponential cost
    avg_gaps = []
    
    print("Simulating Spectral Gap Scaling...")
    for N in N_range:
        gaps_n = []
        for trial in range(5): # Average over disorder
            J_mat, h_vec = create_sk_hamiltonian(N)
            min_gap = get_quantum_gap_min(J_mat, h_vec, N)
            gaps_n.append(min_gap)
        avg_gap = np.mean(gaps_n)
        avg_gaps.append(avg_gap)
        print(f"N={N}, Gap={avg_gap:.4f}")
        
    return list(N_range), avg_gaps

def simulation_thermal_noise(N=10):
    """
    Simulates probability of finding ground state vs Temperature
    Boltzmann distribution P_gs = exp(-E_0/T) / Z
    """
    J_mat, h_vec = create_sk_hamiltonian(N)
    
    # Get classical energies
    dim = 2**N
    energies = []
    for i in range(dim):
        spins = np.array([1 if (i >> b) & 1 else -1 for b in range(N)])
        E = -0.5 * np.dot(spins, np.dot(J_mat, spins)) - np.dot(h_vec, spins)
        energies.append(E)
    
    energies = np.array(sorted(energies))
    E0 = energies[0]
    E1 = energies[1] # First excited (might be degenerate)
    
    # We want to see how P(GS) drops with T
    T_range = np.linspace(0.1, 5.0, 50)
    probs = []
    
    for T in T_range:
        beta = 1.0 / T
        Z = np.sum(np.exp(-beta * (energies - E0))) # Shift E0 for stability
        # Probability of being in Ground State (or degenerate GS)
        # Count degeneracy
        num_gs = np.sum(np.abs(energies - E0) < 1e-6)
        
        prob_gs = num_gs * np.exp(0) / Z # exp(-beta*(E0-E0)) = 1
        probs.append(prob_gs)
        
    return T_range, probs

# Execute Simulations
N_data, Gap_data = simulation_gap_scaling()
T_data, Prob_data = simulation_thermal_noise(N=10)

# Generate Plots
plt.figure(figsize=(12, 5))

# Plot 1: Gap Scaling
plt.subplot(1, 2, 1)
plt.plot(N_data, Gap_data, 'o-', linewidth=2, color='crimson')
# Fit exponential
coeffs = np.polyfit(N_data, np.log(Gap_data), 1)
fit_y = np.exp(coeffs[1]) * np.exp(coeffs[0] * np.array(N_data))
plt.plot(N_data, fit_y, '--', color='black', label=f'Fit: exp({coeffs[0]:.2f}N)')
plt.title('Spectral Gap Closure (Hard Instances)')
plt.xlabel('System Size N')
plt.ylabel('Minimum Gap $\Delta E$')
plt.yscale('log')
plt.grid(True, which="both", ls="-")
plt.legend()

# Plot 2: Thermal Stability
plt.subplot(1, 2, 2)
plt.plot(T_data, Prob_data, 'b-', linewidth=2)
plt.axhline(y=0.5, color='r', linestyle='--', label='Threshold P=0.5')
plt.title('Thermal Stability of Ground State (N=10)')
plt.xlabel('Temperature $k_B T$')
plt.ylabel('P(Ground State)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('p_vs_np_simulation_results.png')
print("Simulation Complete. Image saved.")
