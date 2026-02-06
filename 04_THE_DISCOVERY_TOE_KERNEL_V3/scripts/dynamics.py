"""
KERNEL v3: DYNAMICS
The algorithmic engine that drives the evolution of the Causal Graph.
Core Principle: Things evolve to maximize local entropy / complexity.
"""

import numpy as np
import random

class EntropicEngine:
    """
    The 'CPU' of the Tamesis Universe.
    Manages the discrete time steps $t \to t+1$.
    """
    def __init__(self, temperature=1.0, learning_rate=0.1):
        self.T = temperature
        self.dt = learning_rate # Analogous to time-step or learning rate in gradient ascent
        self.step_count = 0

    def calculate_entropic_gradient(self, node, graph):
        """
        Calculates \nabla S for a given node relative to its potential connections.
        In a graph, 'direction' is defined by potential edges.
        Force points towards nodes with higher Entropy (Information Density).
        """
        current_S = node.entropy
        
        # Look at neighbors to find the "Slope"
        # F_ij = T * (S_j - S_i)
        forces = []
        for neighbor_id in node.neighbors:
            neighbor = graph.nodes[neighbor_id]
            dS = neighbor.entropy - current_S
            forces.append( (neighbor_id, dS) )
            
        return forces

    def entropic_hamiltonian(self, graph):
        """
        Global Cost Function.
        H = -T * S_total (Free Energy principle).
        The universe minimizes H by maximizing S.
        """
        S_total = graph.get_total_entropy()
        return -self.T * S_total

    def evolve_step(self, graph):
        """
        Discrete Time Step t -> t+1.
        1. Connectivity Update: Create/Delete edges based on Entropic Force.
        2. State Update: Scramble quantum states (Scrambling = Information spreading).
        """
        self.step_count += 1
        
        # List of all node IDs
        all_ids = list(graph.nodes.keys())
        
        # 1. ENTROPIC ATTRACTION (Gravity)
        # Pick random pairs and try to connect them
        # Probability of connection ~ exp(Delta S)
        for _ in range(len(all_ids) // 2): # Heuristic: Attempt N/2 interactions per step
            id_a, id_b = random.sample(all_ids, 2)
            
            # Skip if already connected
            if id_b in graph.nodes[id_a].neighbors:
                continue
                
            node_a = graph.nodes[id_a]
            node_b = graph.nodes[id_b]
            
            # S_final if connected (Hypothetical)
            # Connecting mixes information, usually increasing joint entropy if states are distinct
            # Heuristic: Connection favored if target has High Entropy (Mass)
            # Gravity: Small things fall into Big things.
            
            # Force ~ Entropy of Target (Preferential Attachment)
            p_connect = (node_b.entropy + node_a.entropy) / 2.0
            p_connect = np.clip(p_connect, 0, 1) # simple probability map
            
            if random.random() < p_connect:
                graph.add_edge(id_a, id_b)
        
        # 2. STATE SCRAMBLING (Unitarity / Decoherence)
        # Nodes interact with neighbors and scramble phases
        for node_id, node in graph.nodes.items():
            if not node.neighbors:
                continue
            
            gradient = self.calculate_entropic_gradient(node, graph)
            
            # If gradients imply 'flow', update internal state
            # Simple simulation: unitary rotation based on neighbor interaction
            # New State = Old State + small rotation
            random_unitary = np.exp(1j * np.random.rand() * 0.1) 
            node.update_state(node.state * random_unitary)
            
            # Entanglement simulation (simplified)
            # If connected to a high entropy node, become more mixed (increase own entropy)
            # Here we simulate by slightly randomizing the vector magnitude ratios
            noise = (np.random.rand(len(node.state)) - 0.5) * 0.1
            node.state += noise
            node.update_state(node.state) # Re-normalize and recalc S

    def run_simulation(self, graph, steps=10):
        history = []
        for t in range(steps):
            H = self.entropic_hamiltonian(graph)
            history.append( {'t': self.step_count, 'H': H, 'S': graph.get_total_entropy()} )
            self.evolve_step(graph)
        return history
