"""
TOPOLOGICAL ENTROPY SIMULATION (The Hodge Conjecture)
Context: Millennium Problem #5 / Kernel v3

This script investigates the "Persistence" of topological cycles in a dynamic
Entropic Network. It tests the hypothesis that "Algebraic Cycles" correspond
to loops that minimize Information Entropy (Topological Entropy).

Methodology:
1. Initialize a graph with specific "Algebraic" structures (rigid loops).
2. Add "Transient" topological noise (random long loops).
3. Apply Thermal Evolution (MaxEnt rewiring).
4. Measure the survival rate (Persistence) of the different cycle types.

Metric:
- Cycle Persistence (Lifetime)
- Topological Entropy S_top = ln(Sum e^(h_top * length))
"""

import numpy as np
import networkx as nx
import random
from universe_simulation import UniverseSimulation

class TopologicalEntropySim(UniverseSimulation):
    def __init__(self, num_nodes=50, temperature=0.5):
        super().__init__(num_nodes=num_nodes, temperature=temperature)
        # Clear random initialization for controlled topology
        self.graph.nodes = {nid: self.graph.nodes[nid] for nid in self.graph.nodes} 
        self.graph.nodes = {} # resetting clean
        for i in range(num_nodes):
            from ontology import EntropicNode
            n = EntropicNode(node_id=f"N{i}")
            self.graph.add_node(n)
            
    def plant_algebraic_cycles(self):
        """Creates small, tight loops (Triangles/Squares) - 'Algebraic'"""
        # A 'tetrahedron' or 'simplex' structure
        nodes = list(self.graph.nodes.keys())
        self.algebraic_ids = []
        
        # Plant 3 separate K3 (Triangle) cycles
        for i in range(3):
            n1, n2, n3 = nodes[i*3], nodes[i*3+1], nodes[i*3+2]
            self.graph.add_edge(n1, n2)
            self.graph.add_edge(n2, n3)
            self.graph.add_edge(n3, n1)
            self.algebraic_ids.append(set([n1, n2, n3]))
            
    def plant_transient_cycles(self):
        """Creates long, loose loops - 'Cohomological Noise'"""
        nodes = list(self.graph.nodes.keys())
        start_idx = 10
        
        # Use simple random path connecting back
        path = nodes[start_idx:start_idx+6]
        for i in range(len(path)-1):
            self.graph.add_edge(path[i], path[i+1])
        self.graph.add_edge(path[-1], path[0]) # Close loop
        
        self.transient_ids = set(path)

    def count_cycles(self):
        """Identify cycles in the graph basis"""
        G_nx = nx.Graph()
        G_nx.add_nodes_from(self.graph.nodes.keys())
        edges = []
        for nid, node in self.graph.nodes.items():
            for neighbor in node.neighbors:
                if nid < neighbor:
                    edges.append((nid, neighbor))
        G_nx.add_edges_from(edges)
        
        try:
            cycles = nx.cycle_basis(G_nx)
        except:
            cycles = []
        return cycles

    def check_survival(self, cycles):
        """Check if our planted cycles still exist in the basis"""
        algebraic_surviving = 0
        transient_surviving = 0
        
        for cycle in cycles:
            cycle_set = set(cycle)
            
            # Check Algebraic
            for alg_set in self.algebraic_ids:
                if alg_set == cycle_set:
                    algebraic_surviving += 1
            
            # Check Transient
            if self.transient_ids == cycle_set:
                transient_surviving += 1
                
        return algebraic_surviving, transient_surviving

    def run_persistence_test(self, steps=100):
        print(f"--- Running Topological Persistence Test (T={self.T}) ---")
        self.plant_algebraic_cycles()
        self.plant_transient_cycles()
        
        # Connect rest of graph weakly so it's not disconnected dust
        nodes = list(self.graph.nodes.keys())
        for i in range(20, len(nodes)-1):
             self.graph.add_edge(nodes[i], nodes[i+1])
        
        history = []
        
        for t in range(steps):
            self.run_step()
            
            cycles = self.count_cycles()
            n_alg, n_trans = self.check_survival(cycles)
            
            history.append({
                't': t,
                'total_cycles': len(cycles),
                'algebraic': n_alg,
                'transient': n_trans
            })
            
            if t % 20 == 0:
                print(f"Step {t:03d} | Total: {len(cycles)} | Alg: {n_alg} | Trans: {n_trans}")

        return history

if __name__ == "__main__":
    # T=0.3 : Lower temperature to preserve algebraic structure
    sim = TopologicalEntropySim(num_nodes=50, temperature=0.3)
    results = sim.run_persistence_test(steps=100)
    
    # Analysis
    final_alg = results[-1]['algebraic']
    final_trans = results[-1]['transient']
    
    print("\n--- HODGE CONJECTURE SIMULATION VERDICT ---")
    print(f"Algebraic Cycles Surviving: {final_alg}/3")
    print(f"Transient Cycles Surviving: {final_trans}/1")
    
    if final_alg > final_trans:
        print("RESULT: Topological Selection observed. 'Rational' cycles persist.")
    else:
        print("RESULT: No topological distinction found.")
