import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# --- KERNEL V3 ENTROPIC PROCESSOR SIMULATION ---
# Tamesis Mode: Solving TSP via Thermodynamic Relaxation (Boltzmann Machine)

class EntropicTSP:
    def __init__(self, num_cities=15, temp_initial=10.0, cooling_rate=0.995):
        self.num_cities = num_cities
        self.T = temp_initial
        self.cooling_rate = cooling_rate
        
        # Initialize "Cities" as nodes in a 2D metric space
        self.cities = np.random.rand(num_cities, 2)
        self.dist_matrix = self._calculate_distances()
        
        # State: A permutation of cities (the path)
        # In a real quantum/entropic computer, this would be a superposition.
        # Here we simulate the trajectory of the system's state vector.
        self.current_state = np.arange(num_cities)
        np.random.shuffle(self.current_state)
        
        self.history_energy = []
        self.history_entropy = []

    def _calculate_distances(self):
        """Precompute the metric tensor (distances) between all nodes."""
        dist = np.zeros((self.num_cities, self.num_cities))
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                dist[i, j] = np.linalg.norm(self.cities[i] - self.cities[j])
        return dist

    def get_energy(self, state):
        """
        Hamiltonian H(s) = Total Path Length.
        The 'Cost' function we want to minimize physically.
        """
        energy = 0
        for i in range(self.num_cities):
            u = state[i]
            v = state[(i + 1) % self.num_cities] # Loop back to start
            energy += self.dist_matrix[u, v]
        return energy

    def propose_fluctuation(self):
        """
        Simulate a thermal fluctuation (Entropic Kick).
        Swap two cities in the path.
        """
        new_state = self.current_state.copy()
        i, j = np.random.randint(0, self.num_cities, 2)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def relax(self, steps=1000):
        """
        The 'Computing' Phase.
        The system evolves to minimize Free Energy F = U - TS.
        """
        current_energy = self.get_energy(self.current_state)
        
        for step in range(steps):
            # 1. Propose a quantum/thermal fluctuation
            new_state = self.propose_fluctuation()
            new_energy = self.get_energy(new_state)
            
            # 2. Thermodynamic Selection (Metropolis-Hastings)
            # Probability P = exp(-Delta_E / T)
            delta_E = new_energy - current_energy
            
            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / self.T):
                self.current_state = new_state
                current_energy = new_energy
            
            # 3. Cooling (Simulating the Universe's expansion/entropy maximization)
            self.T *= self.cooling_rate
            
            # Log
            self.history_energy.append(current_energy)
            # Entropy proxy: T (high T = high disorder/entropy)

    def visualize(self):
        """Render the final crystallized topological state."""
        plt.figure(figsize=(12, 5))
        
        # Plot 1: The Geometry (The Path)
        plt.subplot(1, 2, 1)
        path_coords = self.cities[self.current_state]
        # Close the loop for plotting
        path_coords = np.vstack([path_coords, path_coords[0]])
        
        plt.plot(path_coords[:, 0], path_coords[:, 1], 'o-', color='crimson', linewidth=2, markersize=8)
        plt.title(f"Solução Cristalizada (Energia: {self.get_energy(self.current_state):.2f})")
        plt.xlabel("Coordenada X")
        plt.ylabel("Coordenada Y")
        plt.grid(True, linestyle='--', alpha=0.6)
        
        # Plot 2: The Dynamics (Energy Relaxation)
        plt.subplot(1, 2, 2)
        plt.plot(self.history_energy, color='darkblue', alpha=0.7)
        plt.title("Relaxamento Termodinâmico (Processamento)")
        plt.xlabel("Tempo (Passos MCMC)")
        plt.ylabel("Energia do Sistema (Comprimento)")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('entropic_processor_result.png')

# Run the simulation
processor = EntropicTSP(num_cities=20, temp_initial=5.0, cooling_rate=0.99)
processor.relax(steps=2000)
processor.visualize()
print("Simulation complete.")