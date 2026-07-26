"""
KERNEL v3: UNIVERSE SIMULATION (MICRO-KERNEL)
The Engine that drives the Entropic Network.
Implements:
1. Free Energy Minimization (F = U - TS)
2. Dynamic Rewiring (Emergence of Geometry)
"""

import numpy as np
import random
from ontology import CausalGraph, EntropicNode

class UniverseSimulation:
    def __init__(self, num_nodes=100, temperature=0.5):
        self.graph = CausalGraph()
        self.T = temperature
        self.step_count = 0
        
        # Initialize nodes with random states
        print(f"Initializing Universe with {num_nodes} nodes...")
        for i in range(num_nodes):
            n = EntropicNode(node_id=f"N{i}")
            self.graph.add_node(n)
            
        # Initial random connectivity (Soup Phase)
        # Connect 10% of possible edges randomly
        all_ids = list(self.graph.nodes.keys())
        for i in range(num_nodes * 2):
            id1, id2 = random.sample(all_ids, 2)
            self.graph.add_edge(id1, id2)

    def calculate_free_energy(self):
        """
        F = U - T*S
        U = Energy (Frustration/Alignment)
        S = Entropy (Information/Complexity)
        """
        U = self.graph.get_energy()
        S = self.graph.get_total_entropy()
        return U - self.T * S, U, S

    def run_step(self):
        self.step_count += 1
        
        # 1. STATE LOOK
        # Nodes flip state to minimize local energy cost
        # (Metropolis-Hastings update)
        for node in self.graph.nodes.values():
            # Current Energy Contribution
            # E = -Sum(s_i * s_j)
            current_E = 0
            for nid in node.neighbors:
                current_E += -1.0 * node.state * self.graph.nodes[nid].state
            
            # Proposed Flip
            proposed_state = -1 * node.state
            proposed_E = -1 * current_E # Flips sign of interaction
            
            dE = proposed_E - current_E
            
            # Acceptance Probability
            # If dE < 0 (Lowers Energy), accept.
            # If dE > 0, accept with prob exp(-dE/T)
            if dE < 0 or np.random.rand() < np.exp(-dE / self.T):
                node.state = proposed_state

        # 2. DYNAMIC REWIRING (The Emergence of Geometry)
        # Rules:
        # - If nodes are ALIGNED (s_i == s_j) but NOT Connected -> Connect (Attraction)
        # - If nodes are ANTI-ALIGNED (s_i != s_j) but Connected -> Disconnect (Repulsion/Expansion)
        # Scale probability by Temperature
        
        all_ids = list(self.graph.nodes.keys())
        
        # Attempt some rewires
        for _ in range(len(all_ids)):
            id1, id2 = random.sample(all_ids, 2)
            if id1 == id2: continue
            
            n1 = self.graph.nodes[id1]
            n2 = self.graph.nodes[id2]
            
            aligned = (n1.state == n2.state)
            connected = (id2 in n1.neighbors)
            
            if aligned and not connected:
                # Attempt Connect (Gravity)
                # Prob ~ 1 - Distance? No metric yet.
                # Pure probability
                if random.random() < 0.1:
                    self.graph.add_edge(id1, id2)
                    
            elif not aligned and connected:
                # Attempt Disconnect (Dark Energy)
                if random.random() < 0.1:
                    self.graph.remove_edge(id1, id2)

    def run_simulation(self, steps=50):
        history = []
        print(f"Running simulation for {steps} steps at T={self.T}...")
        
        for t in range(steps):
            self.run_step()
            F, U, S = self.calculate_free_energy()
            
            # Track geometry statistics
            # Avg Degree, Clustering
            degrees = [len(n.neighbors) for n in self.graph.nodes.values()]
            avg_deg = np.mean(degrees)
            
            history.append({
                't': self.step_count,
                'F': F, 'U': U, 'S': S,
                'avg_deg': avg_deg
            })
            
        return history
