"""
TEST: KERNEL v3 FUNCTOR
Verifies the Discrete -> Continuous mapping.
"""

from ontology import CausalGraph, EntropicNode
from functor import GraphFunctor
import networkx as nx

def create_flat_graph():
    """Creates a 2D Grid (Flat Space)"""
    g = CausalGraph()
    width, height = 5, 5
    ids = {}
    
    # Create nodes
    for x in range(width):
        for y in range(height):
            nid = f"{x},{y}"
            g.add_node(EntropicNode(node_id=nid))
            ids[(x,y)] = nid
            
    # Connect grid
    for x in range(width):
        for y in range(height):
            if x < width-1: g.add_edge(ids[(x,y)], ids[(x+1,y)])
            if y < height-1: g.add_edge(ids[(x,y)], ids[(x,y+1)])
    return g

def create_black_hole_graph():
    """Creates a Clique/Star (High Curvature)"""
    g = CausalGraph()
    center = EntropicNode(node_id="CENTER")
    g.add_node(center)
    
    for i in range(20):
        n = EntropicNode(node_id=f"S{i}")
        g.add_node(n)
        g.add_edge("CENTER", f"S{i}")
        # Add some cross links
        if i > 0:
            g.add_edge(f"S{i}", f"S{i-1}")
    return g

def test_functor():
    print("--- 1. TESTING FLAT MANIFOLD (Grid) ---")
    flat = create_flat_graph()
    f_flat = GraphFunctor(flat)
    metric_flat = f_flat.recover_metric_tensor()
    lorentz_flat = f_flat.check_lorentz_variance()
    
    print(f"Metrics: {metric_flat}")
    print(f"Symmetry Score: {lorentz_flat:.2f}")
    
    if metric_flat['manifold_type'] == 'Flat':
        print(">> SUCCESS: Identified Flat Space.")
    else:
        print(">> FAIL: Misidentified Flat Space.")

    print("\n--- 2. TESTING CURVED MANIFOLD (Black Hole) ---")
    hole = create_black_hole_graph()
    f_hole = GraphFunctor(hole)
    metric_hole = f_hole.recover_metric_tensor()
    lorentz_hole = f_hole.check_lorentz_variance()
    
    print(f"Metrics: {metric_hole}")
    print(f"Symmetry Score: {lorentz_hole:.2f}")
    
    if metric_hole['manifold_type'] == 'Curved':
        print(">> SUCCESS: Identified Curved Space (Gravity).")
    else:
        print(">> FAIL: Misidentified Curved Space.")

    print("\n--- 3. GEODESIC TEST ---")
    d = f_flat.geodesic_distance("0,0", "4,4")
    print(f"Grid Distance (0,0)->(4,4): {d} (Expected 8)")

if __name__ == "__main__":
    test_functor()
