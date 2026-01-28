
import numpy as np
import pytest
from entropic_engine import FiniteCausalGraph, EntropicNode

def test_graph_construction():
    print("\n--- Testing Graph Construction ---")
    g = FiniteCausalGraph(num_nodes=5)
    g.add_edge(0, 1, 1.0)
    g.add_edge(1, 2, 0.5)
    
    A = g.get_adjacency_matrix().toarray()
    print("Adjacency Matrix:")
    print(A)
    
    assert A[0, 1] == 1.0
    assert A[1, 0] == 1.0
    assert A[1, 2] == 0.5
    assert A[0, 2] == 0.0
    print(">> Graph Construction: PASS")

def test_spectrum_computation():
    print("\n--- Testing Spectrum Computation ---")
    g = FiniteCausalGraph(num_nodes=10)
    # Create a ring
    for i in range(10):
        g.add_edge(i, (i+1)%10, 1.0)
        
    evals = g.compute_spectrum(k=4, operator_type='laplacian')
    print(f"Laplacian Smallest Evals: {evals}")
    
    # Laplacian first eval is always ~0 (connected component)
    assert abs(evals[0]) < 1e-9
    print(">> Spectrum: PASS")

def test_np_problem_loading():
    print("\n--- Testing NP Problem Loading ---")
    # Simulate a small 3-node Ising problem
    J = np.array([[0, -1, 0], 
                  [-1, 0, 2], 
                  [0, 2, 0]])
    h = np.array([0.1, 0.0, -0.1])
    
    g = FiniteCausalGraph(num_nodes=3)
    g.load_np_problem(J, h)
    
    A = g.get_adjacency_matrix().toarray()
    print("Loaded Adjacency (from J):")
    print(A)
    
    assert A[0, 1] == -1.0
    assert A[1, 2] == 2.0
    print(">> NP Loading: PASS")

if __name__ == "__main__":
    test_graph_construction()
    test_spectrum_computation()
    test_np_problem_loading()
