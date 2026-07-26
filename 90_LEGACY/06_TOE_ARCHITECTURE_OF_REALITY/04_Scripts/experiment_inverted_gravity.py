"""
EXPERIMENT: INVERTED GRAVITY (CKM MATRIX)
=========================================
Testing the hypothesis: "Invert gravity so heavier particles are further from the center"

MODIFICATIONS FROM BASE DERIVATION:
- Up-type Quarks are placed at nodes [80, 50, 20] (Gen 1, 2, 3) instead of [20, 50, 80].
- Down-type Quarks are placed at nodes [180, 150, 120] (Gen 1, 2, 3) instead of [120, 150, 180].

Rationale: Testing if placing heavier quarks further from the center (weaker binding?) 
improves or changes the CKM mixing angle predictions.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh, svd
from scipy.optimize import minimize
import sys
import os

# Add kernel path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '06_THE_DISCOVERY_TOE_KERNEL_V3', 'scripts'))

from ontology import EntropicNode, CausalGraph

# Observed CKM matrix elements (magnitudes)
V_CKM_OBS = np.array([
    [0.97370, 0.2245, 0.00382],   # |V_ud|, |V_us|, |V_ub|
    [0.2210, 0.987, 0.0410],      # |V_cd|, |V_cs|, |V_cb|
    [0.0080, 0.0388, 1.013]       # |V_td|, |V_ts|, |V_tb|
])

# Observed mixing angles (radians)
THETA_12_OBS = np.radians(13.04)
THETA_23_OBS = np.radians(2.38)
THETA_13_OBS = np.radians(0.201)
DELTA_CP_OBS = np.radians(68.0)


class QuarkDefect:
    """
    A quark modeled as a localized topological defect in the Kernel.
    
    Each quark flavor has:
    - A "shape" (spatial structure in the graph)
    - A "color" (internal SU(3) index)
    - A "generation" (excitation mode)
    """
    def __init__(self, graph, center_id, flavor='u', generation=1):
        self.graph = graph
        self.center = center_id
        self.flavor = flavor
        self.generation = generation
        self.node_list = []
        self.node_to_idx = {}
        self.wavefunction = self._compute_wavefunction()
        
    def _compute_wavefunction(self):
        """
        Compute the "wavefunction" of the defect.
        This is the eigenvector of the local Laplacian corresponding
        to the generation-th excitation.
        """
        # Get local neighborhood
        self.node_list, self.node_to_idx = self._get_neighborhood(radius=3)
        local_nodes = self.node_list
        node_to_idx = self.node_to_idx
        n = len(local_nodes)
        
        if n < 3:
            return np.ones(3) / np.sqrt(3)
        
        # Build local Laplacian
        A = np.zeros((n, n))
        for nid in local_nodes:
            if nid not in self.graph.nodes:
                continue
            node = self.graph.nodes[nid]
            i = node_to_idx[nid]
            for neighbor_id in node.neighbors:
                if neighbor_id in node_to_idx:
                    j = node_to_idx[neighbor_id]
                    A[i, j] = 1
        
        D = np.diag(A.sum(axis=1))
        L = D - A
        
        # Eigenvalues and eigenvectors
        eigenvalues, eigenvectors = eigh(L)
        
        # The wavefunction is the (generation)-th non-zero eigenvector
        # (generation=1 is the first excited state, etc.)
        mode_idx = min(self.generation, len(eigenvalues) - 1)
        psi = eigenvectors[:, mode_idx]
        
        # Normalize
        psi = psi / np.linalg.norm(psi)
        
        return psi
    
    def _get_neighborhood(self, radius):
        """Get nodes within radius hops."""
        visited = {self.center: 0}
        frontier = {self.center}
        
        for d in range(radius):
            new_frontier = set()
            for nid in frontier:
                if nid in self.graph.nodes:
                    for neighbor in self.graph.nodes[nid].neighbors:
                        if neighbor not in visited:
                            visited[neighbor] = d + 1
                            new_frontier.add(neighbor)
            frontier = new_frontier
        
        node_list = list(visited.keys())
        node_to_idx = {nid: i for i, nid in enumerate(node_list)}
        
        return node_list, node_to_idx
    
    def overlap(self, other_defect):
        """
        Compute the overlap between this defect and another.
        
        This is the mixing matrix element: V_ij = <ψ_i | ψ_j>
        """
        # Compute overlap ONLY on common nodes
        common_nodes = set(self.node_list) & set(other_defect.node_list)
        
        if not common_nodes:
            return 0.0
            
        overlap_val = 0.0
        for nid in common_nodes:
            # Get index in self
            idx_self = self.node_to_idx[nid]
            val_self = self.wavefunction[idx_self]
            
            # Get index in other
            idx_other = other_defect.node_to_idx[nid]
            val_other = other_defect.wavefunction[idx_other]
            
            overlap_val += val_self * val_other
            
        return np.abs(overlap_val)


def create_quark_graph(n_nodes=300, avg_degree=8):
    """
    Create a background graph for quarks.
    """
    graph = CausalGraph()
    
    for i in range(n_nodes):
        node = EntropicNode(node_id=str(i))
        graph.add_node(node)
    
    p = avg_degree / (n_nodes - 1)
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if np.random.random() < p:
                graph.add_edge(str(i), str(j))
    
    return graph


def compute_ckm_from_graph(n_samples=20):
    """
    Compute the CKM matrix from quark defect overlaps.
    """
    print("\n" + "="*60)
    print("COMPUTING CKM MATRIX FROM DEFECT OVERLAPS (INVERTED GRAVITY)")
    print("="*60)
    
    # Up-type quarks: u, c, t (generations 1, 2, 3)
    # Down-type quarks: d, s, b (generations 1, 2, 3)
    
    V_samples = []
    
    print(f"Starting simulation with {n_samples} samples...")
    for sample in range(n_samples):
        # Progress indicator
        print(f"Processing sample {sample+1}/{n_samples}...", end='\r')
        
        graph = create_quark_graph(n_nodes=200, avg_degree=6)
        
        # Create defects at different locations
        # INVERTED GRAVITY: Heavy (Gen 3) is FURTHER from center (closer to edges/higher index)
        # Assuming center is around 100/150 for 300 nodes, but here n_nodes=200.
        # Original: ['20', '50', '80'] (Gen 1->3). if 20 is "center" ?? No, usually 0 is one side.
        # Let's stick to the prompt's explicit request for indices.
        
        # Prompt Request:
        # Up-type Quarks: [80, 50, 20] (Gen 1, 2, 3).
        # Down-type Quarks: [180, 150, 120] (Gen 1, 2, 3).
        
        centers_up = ['80', '50', '20']      # u, c, t
        centers_down = ['180', '150', '120']  # d, s, b
        
        # Create up-type quarks
        up_quarks = []
        for i, (center, gen) in enumerate(zip(centers_up, [1, 2, 3])):
            quark = QuarkDefect(graph, center, flavor=['u', 'c', 't'][i], generation=gen)
            up_quarks.append(quark)
        
        # Create down-type quarks
        down_quarks = []
        for i, (center, gen) in enumerate(zip(centers_down, [1, 2, 3])):
            quark = QuarkDefect(graph, center, flavor=['d', 's', 'b'][i], generation=gen)
            down_quarks.append(quark)
        
        # Compute overlap matrix
        V = np.zeros((3, 3))
        for i, up in enumerate(up_quarks):
            for j, down in enumerate(down_quarks):
                V[i, j] = up.overlap(down)
        
        # Normalize rows (unitarity)
        for i in range(3):
            row_norm = np.linalg.norm(V[i, :])
            if row_norm > 0:
                V[i, :] /= row_norm
        
        V_samples.append(V)
    
    # Average CKM matrix
    V_mean = np.mean(V_samples, axis=0)
    V_std = np.std(V_samples, axis=0)
    
    print("\nComputed CKM matrix (magnitudes):")
    print(V_mean.round(4))
    
    print("\nObserved CKM matrix (magnitudes):")
    print(V_CKM_OBS.round(4))
    
    return V_mean, V_std


def extract_mixing_angles(V):
    """
    Extract mixing angles from CKM matrix using standard parameterization.
    """
    s13 = V[0, 2]  # |V_ub|
    c13 = np.sqrt(1 - s13**2)
    
    s12 = V[0, 1] / c13 if c13 > 0 else 0
    s23 = V[1, 2] / c13 if c13 > 0 else 0
    
    # Clamp to valid range
    s12 = np.clip(s12, -1, 1)
    s23 = np.clip(s23, -1, 1)
    s13 = np.clip(s13, -1, 1)
    
    theta_12 = np.arcsin(s12)
    theta_23 = np.arcsin(s23)
    theta_13 = np.arcsin(s13)
    
    return theta_12, theta_23, theta_13


def plot_results(V_computed, V_std, output_dir):
    """
    Generate publication-quality figures for Experiment.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: CKM matrix comparison (heatmap)
    ax1 = axes[0, 0]
    
    im = ax1.imshow(V_computed, cmap='Blues', vmin=0, vmax=1)
    plt.colorbar(im, ax=ax1, label='|V|')
    
    # Annotate
    for i in range(3):
        for j in range(3):
            text = f"{V_computed[i,j]:.3f}\n({V_CKM_OBS[i,j]:.3f})"
            ax1.text(j, i, text, ha='center', va='center', fontsize=10)
    
    ax1.set_xticks([0, 1, 2])
    ax1.set_yticks([0, 1, 2])
    ax1.set_xticklabels(['d', 's', 'b'])
    ax1.set_yticklabels(['u', 'c', 't'])
    ax1.set_xlabel('Down-type Quarks', fontsize=12)
    ax1.set_ylabel('Up-type Quarks', fontsize=12)
    ax1.set_title('Inverted Gravity CKM (Predicted)', fontsize=14)
    
    # Plot 2: Mixing angles comparison
    ax2 = axes[0, 1]
    
    theta_12_pred, theta_23_pred, theta_13_pred = extract_mixing_angles(V_computed)
    
    angles = ['θ₁₂', 'θ₂₃', 'θ₁₃']
    predicted = [np.degrees(theta_12_pred), np.degrees(theta_23_pred), np.degrees(theta_13_pred)]
    observed = [np.degrees(THETA_12_OBS), np.degrees(THETA_23_OBS), np.degrees(THETA_13_OBS)]
    
    x = np.arange(len(angles))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, observed, width, label='Observed', color='blue', alpha=0.7)
    bars2 = ax2.bar(x + width/2, predicted, width, label='Inverted Exp.', color='orange', alpha=0.7)
    
    ax2.set_xlabel('Mixing Angle', fontsize=12)
    ax2.set_ylabel('Angle (degrees)', fontsize=12)
    ax2.set_title('CKM Mixing Angles (Inverted)', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(angles)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Correlation
    ax3 = axes[1, 0]
    
    V_flat_pred = V_computed.flatten()
    V_flat_obs = V_CKM_OBS.flatten()
    
    ax3.scatter(V_flat_obs, V_flat_pred, s=100, c='purple', alpha=0.7)
    ax3.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Perfect fit')
    
    # Annotate points
    labels = ['Vud', 'Vus', 'Vub', 'Vcd', 'Vcs', 'Vcb', 'Vtd', 'Vts', 'Vtb']
    for i, label in enumerate(labels):
        ax3.annotate(label, (V_flat_obs[i], V_flat_pred[i]), fontsize=8,
                     xytext=(3, 3), textcoords='offset points')
    
    ax3.set_xlabel('Observed |V|', fontsize=12)
    ax3.set_ylabel('Predicted |V|', fontsize=12)
    ax3.set_title('CKM Elements Check', fontsize=14)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # R²
    ss_res = np.sum((V_flat_obs - V_flat_pred)**2)
    ss_tot = np.sum((V_flat_obs - np.mean(V_flat_obs))**2)
    r_squared = 1 - ss_res / ss_tot
    ax3.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax3.transAxes,
             fontsize=12, verticalalignment='top')
    
    # Plot 4: Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary_text = f"""
    EXPERIMENT: INVERTED GRAVITY
    ════════════════════════════
    
    SETUP:
    - Inverted quark generation placement.
    - Heavier generations = Further from origin.
    - Up:   [80, 50, 20] (u, c, t)
    - Down: [180, 150, 120] (d, s, b)
    
    MIXING ANGLES:
                    Predicted    Observed
    theta_12        {np.degrees(theta_12_pred):6.2f} deg      {np.degrees(THETA_12_OBS):6.2f} deg
        theta_23        {np.degrees(theta_23_pred):6.2f} deg      {np.degrees(THETA_23_OBS):6.2f} deg
        theta_13        {np.degrees(theta_13_pred):6.2f} deg      {np.degrees(THETA_13_OBS):6.2f} deg
    
    CORRELATION: R² = {r_squared:.3f}
    
    HYPOTHESIS CHECK:
    Does inverting gravity improve CKM fit?
    
    Compare R² with original derivation baseline.
    """
    
    ax4.text(0.02, 0.98, summary_text, transform=ax4.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'experiment_inverted_ckm.png'), 
                dpi=300, bbox_inches='tight')
    print(f"\nFigures saved to {output_dir}")
    
    return fig, r_squared


def main():
    """
    Main execution: Inverted Gravity CKM Experiment.
    """
    print("\n" + "="*70)
    print("TAMESIS EXPERIMENT: INVERTED GRAVITY CKM")
    print("="*70)
    print("\nTesting: Placing heavier quarks FURTHER from graph center.")
    print("="*70)
    
    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(output_dir, exist_ok=True)
    
    # Compute CKM
    # Using more samples for stability in experiment
    V_computed, V_std = compute_ckm_from_graph(n_samples=30)
    
    # Extract angles
    theta_12, theta_23, theta_13 = extract_mixing_angles(V_computed)
    
    print(f"\nExtracted mixing angles (Inverted):")
    print(f"  theta_12 = {np.degrees(theta_12):.2f} deg (observed: {np.degrees(THETA_12_OBS):.2f} deg)")
    print(f"  theta_23 = {np.degrees(theta_23):.2f} deg (observed: {np.degrees(THETA_23_OBS):.2f} deg)")
    print(f"  theta_13 = {np.degrees(theta_13):.2f} deg (observed: {np.degrees(THETA_13_OBS):.2f} deg)")
    
    # Plot results
    fig, r_squared = plot_results(V_computed, V_std, output_dir)
    
    # Final summary
    print("\n" + "="*70)
    print("EXPERIMENTAL RESULT")
    print("="*70)
    print(f"R² = {r_squared:.3f}")
    
    # Save data
    np.savez(os.path.join(output_dir, 'inverted_ckm_matrix_data.npz'),
             V_computed=V_computed,
             V_observed=V_CKM_OBS,
             r_squared=r_squared)
    
    # Do not block on show() for automated runs
    # plt.show()
    
    return V_computed, r_squared


if __name__ == "__main__":
    results = main()
