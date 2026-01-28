import numpy as np

class ConsciousnessModeler:
    """
    Simulates Consciousness based on Integrated Information Theory (IIT).
    Hypothesis: The 'Observer Effect' in Quantum Mechanics is a function of Phi (Φ).
    High Phi -> Deterministic Reality (Collapse).
    Low Phi -> Stochastic/Superposed Reality.
    """
    
    def __init__(self):
        """
        Initialize the Consciousness Modeler.
        """
        pass
        
    def calculate_phi_heuristic(self, connectivity_matrix):
        """
        Estimates Phi (Integrated Information) for a given network topology.
        Full IIT is computationally irreducible (NP-Hard).
        We use a heuristic: Phi ~ (Global Integration) - (Partitioned Integration).
        
        For simulation purposes, we approximate Phi based on network density and recurrence (loops).
        A feedforward network has Phi = 0.
        A strongly connected recurrent network has High Phi.
        """
        # 1. Check for cycles/recurrence. 
        # If the matrix is triangular (feedforward), Phi is low/zero.
        eigenvalues = np.linalg.eigvals(connectivity_matrix)
        
        # The magnitude of eigenvalues relates to the cyclic behavior.
        # Spectral Radius
        rho = np.max(np.abs(eigenvalues))
        
        # Density of connections
        n_nodes = connectivity_matrix.shape[0]
        n_edges = np.count_nonzero(connectivity_matrix)
        density = n_edges / (n_nodes**2)
        
        # Heuristic Phi Score
        # Feedforward net (eigvals ~ 0 usually for strictly triangular) -> Phi ~ 0
        # Recurrent net (rho > 0, often > 1) -> Phi > 0
        
        # A simple model: Phi = Density * SpectralRadius^2 * NodeCount
        phi_score = density * (rho**2) * np.log(n_nodes)
        
        # Normalize/Clamp for simulation context (0 to 100 scale)
        return float(phi_score * 10.0)

    def observe_wavefunction(self, psi_prob, phi_level):
        """
        Simulates the effect of an observer with a given Phi level on a quantum state.
        
        Args:
            psi_prob: Array of probabilities summing to 1 (Superposition).
            phi_level: The 'Consciousness' of the observer.
            
        Returns:
            collapsed_prob: The state after observation.
        """
        # Hypothesis: Collapse is not binary (Yes/No), but gradual based on Interaction Strength (Phi).
        # Softmax cooling?
        # New P_i = P_i^(1 + alpha * Phi) / Z
        
        # If Phi is 0 (Rock), alpha*Phi = 0 -> P_i remains same (Passthrough/Superposition).
        # If Phi is High (Human), alpha*Phi is large -> Amplifies the max probability (Collapse).
        
        psi = np.array(psi_prob)
        
        # Coefficient of Reality Hardening
        hardening_factor = phi_level * 0.5 
        if hardening_factor < 0: hardening_factor = 0
        
        # We apply a "Sharpening" function to the probability distribution
        # P'_i = P_i^(1 + hardening)
        
        sharpened = np.power(psi, 1 + hardening_factor)
        
        # Normalize
        collapsed_prob = sharpened / np.sum(sharpened)
        
        return collapsed_prob

    def entropy(self, prob_dist):
        """Calculates Shannon Entropy in bits."""
        # Avoid log(0)
        p = prob_dist[prob_dist > 0]
        return -np.sum(p * np.log2(p))
