"""
Neural Network Memorization-Generalization Transition
======================================================

Stage 37.1: Testing U_{1/2} in neural networks.

HYPOTHESIS
----------
Neural networks undergo a transition from:
- MEMORIZATION: Network "remembers" all training examples (like permutation)
- GENERALIZATION: Network "forgets" individuals but learns patterns (like random map)

The transition parameter:
- c ~ data_size / network_capacity
- phi(c) = fraction of examples "perfectly memorized"

PREDICTION
----------
If U_{1/2} applies:
    phi(c) = (1 + c)^{-1/2}

EXPERIMENTAL DESIGN
-------------------
1. Train networks of varying capacity on fixed dataset
2. Measure fraction of training examples with zero loss
3. Plot phi vs c = dataset_size / network_capacity
4. Fit to power law and check if exponent = 1/2
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple
import warnings


def power_law(c: np.ndarray, alpha: float) -> np.ndarray:
    """General power law: phi(c) = (1 + c)^{-alpha}"""
    return (1 + c) ** (-alpha)


def u12(c: np.ndarray) -> np.ndarray:
    """U_{1/2} prediction: phi(c) = (1 + c)^{-1/2}"""
    return (1 + c) ** (-0.5)


class SimpleNN:
    """
    Minimal neural network for memorization experiment.
    Single hidden layer, ReLU activation.
    """
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.1
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, output_dim) * 0.1
        self.b2 = np.zeros(output_dim)
        self.hidden_dim = hidden_dim
        self.capacity = input_dim * hidden_dim + hidden_dim + hidden_dim * output_dim + output_dim
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass."""
        self.z1 = X @ self.W1 + self.b1
        self.a1 = np.maximum(0, self.z1)  # ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        return self.z2
    
    def backward(self, X: np.ndarray, y: np.ndarray, learning_rate: float = 0.01):
        """Backward pass with gradient descent."""
        m = X.shape[0]
        
        # Forward
        output = self.forward(X)
        
        # Backward
        dz2 = output - y
        dW2 = self.a1.T @ dz2 / m
        db2 = np.mean(dz2, axis=0)
        
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)  # ReLU derivative
        dW1 = X.T @ dz1 / m
        db1 = np.mean(dz1, axis=0)
        
        # Update
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        
        return np.mean(np.sum((output - y)**2, axis=1))
    
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 1000, 
            learning_rate: float = 0.01, verbose: bool = False) -> List[float]:
        """Train the network."""
        losses = []
        for epoch in range(epochs):
            loss = self.backward(X, y, learning_rate)
            losses.append(loss)
            if verbose and epoch % 100 == 0:
                print(f"Epoch {epoch}: loss = {loss:.6f}")
        return losses
    
    def memorization_fraction(self, X: np.ndarray, y: np.ndarray, threshold: float = 0.01) -> float:
        """
        Fraction of examples with per-example loss below threshold.
        This measures "perfect memorization".
        """
        output = self.forward(X)
        per_example_loss = np.mean((output - y)**2, axis=1)
        memorized = per_example_loss < threshold
        return np.mean(memorized)


class MemorizationExperiment:
    """
    Experiment to test U_{1/2} in neural network memorization.
    """
    
    def __init__(self, input_dim: int = 10, output_dim: int = 1, 
                 n_examples: int = 100, noise_level: float = 0.1):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.n_examples = n_examples
        self.noise_level = noise_level
        
        # Generate random dataset
        self.X = np.random.randn(n_examples, input_dim)
        self.y = np.random.randn(n_examples, output_dim)
    
    def run(self, hidden_dims: List[int], epochs: int = 2000, 
            threshold: float = 0.01) -> Dict:
        """
        Run experiment for different network capacities.
        
        c = data_size / capacity
        phi = memorization fraction
        """
        results = []
        
        for hidden_dim in hidden_dims:
            nn = SimpleNN(self.input_dim, hidden_dim, self.output_dim)
            capacity = nn.capacity
            
            # c = data_size / network_capacity
            c = self.n_examples / capacity
            
            # Train
            nn.fit(self.X, self.y, epochs=epochs, learning_rate=0.01)
            
            # Measure memorization
            phi = nn.memorization_fraction(self.X, self.y, threshold)
            
            results.append({
                'hidden_dim': hidden_dim,
                'capacity': capacity,
                'c': c,
                'phi': phi
            })
            
            print(f"   hidden={hidden_dim:4d}, capacity={capacity:6d}, c={c:.4f}, phi={phi:.3f}")
        
        return {
            'results': results,
            'c_values': np.array([r['c'] for r in results]),
            'phi_values': np.array([r['phi'] for r in results])
        }
    
    def fit_exponent(self, c_values: np.ndarray, phi_values: np.ndarray) -> Dict:
        """Fit exponent alpha and compare to 1/2."""
        try:
            # Filter valid data (phi > 0)
            valid = phi_values > 0
            c_valid = c_values[valid]
            phi_valid = phi_values[valid]
            
            if len(c_valid) < 3:
                return {'error': 'Insufficient data points'}
            
            popt, pcov = curve_fit(
                power_law,
                c_valid, phi_valid,
                p0=[0.5],
                bounds=(0.01, 5)
            )
            
            alpha = popt[0]
            alpha_err = np.sqrt(pcov[0, 0]) if pcov[0, 0] > 0 else 0.1
            
            is_u12 = abs(alpha - 0.5) < 2 * alpha_err
            
            return {
                'alpha': alpha,
                'alpha_error': alpha_err,
                'is_U12': is_u12,
                'deviation_from_half': abs(alpha - 0.5)
            }
        except Exception as e:
            return {'error': str(e)}


def main():
    """Stage 37.1: Neural network memorization experiment."""
    
    print("=" * 70)
    print("STAGE 37.1: NEURAL NETWORK MEMORIZATION-GENERALIZATION TRANSITION")
    print("=" * 70)
    
    print("\n1. EXPERIMENTAL SETUP")
    print("-" * 50)
    print("   Input dimension: 10")
    print("   Output dimension: 1")
    print("   Training examples: 100")
    print("   Varying: hidden layer size (network capacity)")
    
    # Run experiment
    print("\n2. RUNNING EXPERIMENT")
    print("-" * 50)
    
    exp = MemorizationExperiment(
        input_dim=10,
        output_dim=1,
        n_examples=100
    )
    
    # Test different capacities
    hidden_dims = [5, 10, 20, 50, 100, 200, 500]
    
    results = exp.run(hidden_dims, epochs=2000, threshold=0.01)
    
    # Fit exponent
    print("\n3. FITTING EXPONENT")
    print("-" * 50)
    
    fit = exp.fit_exponent(results['c_values'], results['phi_values'])
    
    if 'alpha' in fit:
        print(f"   Fitted alpha = {fit['alpha']:.3f} +/- {fit['alpha_error']:.3f}")
        print(f"   Deviation from 1/2 = {fit['deviation_from_half']:.3f}")
        
        if fit['is_U12']:
            print("\n   RESULT: U_{1/2} DETECTED!")
            print("   Neural network transition follows phi(c) = (1+c)^{-1/2}")
        else:
            print(f"\n   RESULT: DIFFERENT EXPONENT (alpha = {fit['alpha']:.3f})")
            print("   Neural network transition has its own universality class")
    else:
        print(f"   Fit error: {fit.get('error', 'Unknown')}")
    
    # Theoretical comparison
    print("\n4. THEORETICAL COMPARISON")
    print("-" * 50)
    
    c_theory = np.linspace(0.01, max(results['c_values']), 50)
    phi_u12 = u12(c_theory)
    
    print("   c        phi(data)   phi(U_{1/2})")
    for i, r in enumerate(results['results']):
        phi_pred = u12(r['c'])
        diff = abs(r['phi'] - phi_pred)
        print(f"   {r['c']:.4f}   {r['phi']:.3f}       {phi_pred:.3f}       (diff={diff:.3f})")
    
    # Interpretation
    print("\n5. INTERPRETATION")
    print("-" * 50)
    
    if 'alpha' in fit:
        if fit['is_U12']:
            print("""
   POSITIVE RESULT: U_{1/2} appears in neural networks!
   
   This suggests that memorization -> generalization is the SAME
   universality class as permutation -> random map.
   
   Both are "discrete-to-random" transitions where:
   - n = number of "slots" (weights or elements)
   - c/n = perturbation per slot
   - phi = fraction of "deterministic" behavior
""")
        else:
            print(f"""
   DIFFERENT EXPONENT: alpha = {fit['alpha']:.3f}
   
   Neural networks have their OWN universality class,
   distinct from U_{{1/2}}.
   
   This is still valuable: it defines NN_alpha = {fit['alpha']:.3f}
   as a new exponent for learning transitions.
""")
    
    print("=" * 70)
    print("END OF NEURAL NETWORK EXPERIMENT")
    print("=" * 70)
    
    return results, fit


if __name__ == "__main__":
    results, fit = main()
