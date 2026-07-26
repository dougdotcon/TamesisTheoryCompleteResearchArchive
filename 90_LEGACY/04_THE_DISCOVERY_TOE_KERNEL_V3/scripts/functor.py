"""
KERNEL v3: THE FUNCTOR
The Bridge between Discrete (Graph) and Continuous (Manifold).
Translates Network Topology into Metric Geometry.
"""

import numpy as np
import networkx as nx

class GraphFunctor:
    """
    Maps a CausalGraph to a Riemannian Manifold approximation.
    """
    def __init__(self, causal_graph):
        self.graph = causal_graph
        # Convert internal graph representation to NetworkX for calculations
        self.nx_graph = self._to_networkx()

    def _to_networkx(self):
        G = nx.Graph()
        G.add_nodes_from(self.graph.nodes.keys())
        G.add_edges_from(self.graph.edges)
        return G

    def geodesic_distance(self, id_a, id_b):
        """
        Calculates the Emergent Metric distance d(A, B).
        In a causal set, distance is the length of the shortest chain (geodesic).
        """
        try:
            return nx.shortest_path_length(self.nx_graph, source=id_a, target=id_b)
        except nx.NetworkXNoPath:
            return float('inf')

    def effective_curvature(self, node_id):
        """
        Estimates local discrete curvature (Ollivier-Ricci or Forman).
        Simplified: 
        R ~ 1 - (Average Distance of Neighbors in Graph / Average Distance in Flat Space)
        
        Alternative Heuristic: Clustering Coefficient C.
        In flat space (grid), C is 0.
        In curved space (sphere/clique), C is high.
        """
        if node_id not in self.nx_graph:
            return 0.0
            
        return nx.clustering(self.nx_graph, node_id)

    def recover_metric_tensor(self):
        """
        Statistical recovery of g_uv.
        Returns average geodesic distance and average curvature.
        This represents the 'Global Geometry' of the universe.
        """
        if len(self.nx_graph) == 0:
            return {'avg_dist': 0, 'scalar_curvature': 0}
            
        # Sampling paths for speed
        total_dist = 0
        count = 0
        nodes = list(self.nx_graph.nodes())
        sample_size = min(len(nodes), 20)
        
        for i in range(sample_size):
            for j in range(i+1, sample_size):
                d = self.geodesic_distance(nodes[i], nodes[j])
                if d != float('inf'):
                    total_dist += d
                    count += 1
        
        avg_dist = total_dist / max(count, 1)
        
        # Scalar Curvature (Average Clustering)
        avg_curvature = nx.average_clustering(self.nx_graph)
        
        return {
            'emergent_radius': avg_dist, # R ~ diameter
            'scalar_curvature': avg_curvature, # R_scalar
            'manifold_type': 'Flat' if avg_curvature < 0.1 else 'Curved'
        }

    def check_lorentz_variance(self):
        """
        Checks if the graph looks the same from different 'connected' perspectives.
        A rough proxy for Lorentz Invariance in graphs is Homogeneity.
        """
        degrees = [d for n, d in self.nx_graph.degree()]
        variance = np.var(degrees)
        return 1.0 / (1.0 + variance) # 1.0 = Perfect Symmetry, 0.0 = Broken Symmetry
