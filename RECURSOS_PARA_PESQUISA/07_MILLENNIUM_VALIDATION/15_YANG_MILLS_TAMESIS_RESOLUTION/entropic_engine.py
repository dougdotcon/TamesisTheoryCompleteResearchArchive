"""
KERNEL v3: ENTROPIC ENGINE
Common Infrastructure for P vs NP (Thermodynamic) and Riemann (Spectral) tracks.

This module defines the `FiniteCausalGraph`, a discrete structure that:
1. Evolves according to entropic update rules (Layer 0.2).
2. Can map NP-problems to its energy landscape (Track A).
3. Can export its operator spectrum (Track B).

Based on the legacy `ThermodynamicTuringMachine` but generalized for the Tamesis Ontology.
"""

import numpy as np
import scipy.sparse as sparse
import scipy.sparse.linalg as sla
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

@dataclass
class EntropicNode:
    id: int
    state: float = 0.0  # Normalized Information Content [0, 1]
    capacity: float = 1.0 # Bekenstein Bound for this node local region
    neighbors: Dict[int, float] = field(default_factory=dict) # id -> weight

@dataclass
class FiniteCausalGraph:
    """
    A Graph G(V, E) representing a discrete slice of the Tamesis Vacuum.
    """
    num_nodes: int
    nodes: Dict[int, EntropicNode] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize nodes if empty
        if not self.nodes:
            for i in range(self.num_nodes):
                self.nodes[i] = EntropicNode(id=i)

    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Adds a causal link (entanglement) between nodes."""
        self.nodes[u].neighbors[v] = weight
        self.nodes[v].neighbors[u] = weight # Symmetric for spatial graph

    def get_adjacency_matrix(self) -> sparse.csr_matrix:
        """Exports the graph as a sparse Adjacency Matrix A."""
        row = []
        col = []
        data = []
        
        for u_id, node in self.nodes.items():
            for v_id, weight in node.neighbors.items():
                row.append(u_id)
                col.append(v_id)
                data.append(weight)
                
        return sparse.csr_matrix((data, (row, col)), shape=(self.num_nodes, self.num_nodes))

    def get_laplacian_matrix(self) -> sparse.csr_matrix:
        """Exports the Combinatorial Laplacian L = D - A."""
        A = self.get_adjacency_matrix()
        degrees = np.array(A.sum(axis=1)).flatten()
        D = sparse.diags(degrees)
        return D - A

    def get_hamiltonian_operator(self) -> sparse.csr_matrix:
        """
        Constructs the Physical Operator H for the Spectral Attack.
        
        Hypothesis: The 'Critical Instant' operator is related to the Graph Laplacian
        modified by the Entropic Potential (Node States).
        
        H = -L + V(entropy)
        """
        L = self.get_laplacian_matrix()
        
        # Potential V dependent on node saturation states
        # V_ii = -log(1 - state_i) ? (Information Singularity)
        # For simple spectral tests, let's start with just L or A.
        # But to be 'Physical', we add the Potential term.
        
        potentials = []
        for i in range(self.num_nodes):
            # Avoid log(0)
            s = min(self.nodes[i].state, 0.9999)
            # Entropic Potential: High Entropy -> High Potential Barrier
            v_i = -np.log(1.0 - s) 
            potentials.append(v_i)
            
        V = sparse.diags(potentials)
        
        # H = L + V (Schrodinger-like)
        return L + V

    def compute_spectrum(self, k: int = 10, operator_type: str = 'hamiltonian') -> np.ndarray:
        """
        Computes the first k eigenvalues.
        Used for Track B (Riemann).
        """
        if operator_type == 'adjacency':
            Op = self.get_adjacency_matrix()
        elif operator_type == 'laplacian':
            Op = self.get_laplacian_matrix()
        else:
            Op = self.get_hamiltonian_operator()
            
        if self.num_nodes < 20:
            evals = np.linalg.eigvalsh(Op.toarray())
            return evals[:k]
        else:
            # For H/L, we usually want smallest eigenvalues (Low energy)
            # For A, we might want largest.
            which = 'SM' if operator_type != 'adjacency' else 'LM'
            try:
                evals, _ = sla.eigsh(Op, k=k, which=which)
                return np.sort(evals)
            except:
                # Fallback
                return np.linalg.eigvalsh(Op.toarray())[:k]

    def load_np_problem(self, J_matrix: np.ndarray, h_vector: np.ndarray):
        """
        Maps an NP problem (Ising formulation) into the Graph topology.
        Used for Track A (P vs NP).
        
        The Graph Structure itself must reflect the constraints J.
        """
        # Reset edges
        for node in self.nodes.values():
            node.neighbors.clear()
            
        rows, cols = J_matrix.nonzero()
        for i, j in zip(rows, cols):
            if i < j: # Upper triangle
                # Edge weight represents coupling strength
                self.add_edge(i, j, weight=J_matrix[i, j])
                
        # Node states initialized by h? 
        # Or bias affects 'capacity'? 
        # For now, let's Map h to initial state bias.
        for i in range(self.num_nodes):
            self.nodes[i].state = 0.5 + 0.1 * h_vector[i] # Bias

    def calculate_spectral_entropy(self) -> float:
        """
        Calculates the Von Neumann Entropy of the Graph Spectrum.
        S = - sum(lambda_i * log(lambda_i))
        normalized.
        """
        try:
            L = self.get_laplacian_matrix()
            # For efficiency on large graphs, we might approximate.
            # ideally we want full S.
            if self.num_nodes < 100:
                evals = np.linalg.eigvalsh(L.toarray())
            else:
                # Use standard sparse solver for restricted k
                evals = self.compute_spectrum(k=min(self.num_nodes-1, 50), operator_type='laplacian')
            
            # Normalize to probability distribution
            total = np.sum(np.abs(evals))
            if total == 0: return 0.0
            probs = np.abs(evals) / total
            
            entropy = 0.0
            for p in probs:
                if p > 1e-9:
                    entropy -= p * np.log(p)
            return entropy
        except:
            return 0.0

    def apply_entropic_pressure(self, steps: int = 100, beta: float = 1.0, check_interval: int = 20):
        """
        Evolves the graph under Entropic Pressure.
        Monte Carlo simulation favoring high-entropy configurations.
        
        Args:
            steps: Number of MC steps.
            beta: Inverse temperature (1/T).
            check_interval: How often to re-diagonalize matrix (expensive).
        """
        current_entropy = self.calculate_spectral_entropy()
        
        # Cache for optimization:
        # We can accept *any* change blindly in between checks? 
        # No, that's random walk. 
        # We need a proxy for entropy? Or just accept the cost?
        # A compromise: We assume small changes locally don't destroy entropy.
        # But we need to drive it Up.
        # Efficient Entropic Force:
        # Using Degree centrality variance as a cheap proxy? 
        # High entropy ~ Regular degrees? No, GUE is complex.
        
        # STRATEGY:
        # We perform 'check_interval' mutations, then check if the batch improved entropy.
        # If yes, keep batch. If no, revert batch.
        
        # Backup state
        import copy
        
        for batch in range(0, steps, check_interval):
             # Save current best state
             backup_nodes = copy.deepcopy(self.nodes)
             
             # Perform blind mutations
             for _ in range(check_interval):
                u = np.random.randint(0, self.num_nodes)
                v = np.random.randint(0, self.num_nodes)
                if u == v: continue
                
                exists = v in self.nodes[u].neighbors
                if exists:
                    del self.nodes[u].neighbors[v]
                    del self.nodes[v].neighbors[u]
                else:
                    self.nodes[u].neighbors[v] = 1.0
                    self.nodes[v].neighbors[u] = 1.0
             
             # Check cost
             new_entropy = self.calculate_spectral_entropy()
             delta_S = new_entropy - current_entropy
             
             if delta_S > 0 or np.random.rand() < np.exp(beta * delta_S):
                 current_entropy = new_entropy
                 # Accept
             else:
                 # Revert
                 self.nodes = backup_nodes

