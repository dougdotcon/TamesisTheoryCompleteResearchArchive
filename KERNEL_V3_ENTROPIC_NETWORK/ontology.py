"""
KERNEL v3: ONTOLOGY (REFINED)
Definition of the fundamental objects of the computational universe.
Refined with Senior Engineer feedback: Capacity, Free Energy, Ollivier-Ricci.
"""

import numpy as np
import uuid

class EntropicNode:
    """
    A fundamental unit of the Entropic Network (Kernel v3).
    Represents a discrete patch of quantum information (Tensor Network Node).
    """
    def __init__(self, node_id=None, capacity_bits=1.0, node_type="QUANTUM"):
        self.id = node_id if node_id else str(uuid.uuid4())[:8]
        self.type = node_type # "QUANTUM", "CLASSICAL"
        
        # State: Simplified Qubit/Tensor for prototype efficiency
        # Ideally this is a Tensor (MPS)
        self.state = np.random.choice([-1, 1]) 
        
        # Connections (Edges) - List of Neighbor Objects/IDs
        # Storing IDs for graph simplicity, simulation wrapper handles object ref
        self.neighbors = [] 
        
        # Holographic Capacity (Bekenstein Bound)
        # How much info this node can hold before saturating (Black Hole)
        self.capacity = capacity_bits
        
        # Current Information Content
        self.entropy = 0.0

    def connect(self, other_node_id):
        if other_node_id not in self.neighbors:
            self.neighbors.append(other_node_id)
            
    def disconnect(self, other_node_id):
        if other_node_id in self.neighbors:
            self.neighbors.remove(other_node_id)

    def compute_local_curvature(self, graph_ref):
        """
        The discrete version of Ricci Curvature (Ollivier-Ricci proxy).
        Based on neighborhood overlap (Clustering Coefficient).
        
        R > 0: Spherical (Gravity/Clusters)
        R < 0: Hyperbolic (Expansion/Trees)
        """
        k = len(self.neighbors)
        if k < 2:
            return 0.0 # Undefined/Flat
            
        links_between_neighbors = 0
        
        # We need access to neighbor's neighbors via graph_ref
        neighbor_nodes = [graph_ref.nodes[nid] for nid in self.neighbors if nid in graph_ref.nodes]
        
        for n1 in neighbor_nodes:
            for n2 in neighbor_nodes:
                if n1.id == n2.id: continue
                if n2.id in n1.neighbors:
                    links_between_neighbors += 1
        
        # Directed/Undirected factor adjustment (here assuming undirected, each link counted twice in loop)
        # Clustering Coeff C = 2 * E_neighbors / k(k-1)
        clustering = links_between_neighbors / (k * (k - 1))
        
        # Ricci proxy: R ~ C (High clustering means positive curvature)
        return clustering

    def calculate_current_entropy(self):
        """
        Shannon Entropy/Von Neumann based on connectivity (degree of mixing).
        """
        k = len(self.neighbors)
        if k == 0:
            return 0.0
        return np.log2(k) # Simplistic measure: more neighbors = more mixed state potential

    def __repr__(self):
        return f"<Node {self.id} | S={self.entropy:.2f} | K={len(self.neighbors)}>"

class CausalGraph:
    """
    The substrate of spacetime.
    """
    def __init__(self):
        self.nodes = {} 

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].connect(id2)
            self.nodes[id2].connect(id1)

    def remove_edge(self, id1, id2):
        if id1 in self.nodes and id2 in self.nodes:
            self.nodes[id1].disconnect(id2)
            self.nodes[id2].disconnect(id1)

    def get_total_entropy(self):
        return sum(n.calculate_current_entropy() for n in self.nodes.values())
    
    def get_energy(self):
        """
        Hamiltonian U.
        Energy Cost = Frustration (anti-aligned neighbors cost energy)
        """
        U = 0
        for node in self.nodes.values():
            for nid in node.neighbors:
                neighbor = self.nodes[nid]
                # Ising-like interaction: -J * s_i * s_j
                # Aligned = Low Energy (-1). Anti-aligned = High Energy (+1).
                U += -1.0 * node.state * neighbor.state
        return U / 2.0 # Each edge counted twice

    def __repr__(self):
        return f"<CausalGraph V={len(self.nodes)}>"
