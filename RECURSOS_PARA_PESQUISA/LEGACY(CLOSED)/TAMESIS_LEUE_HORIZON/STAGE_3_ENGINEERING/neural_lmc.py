
"""
neural_lmc.py
-------------
Stage 3: Engineering Prototype (Recovery V4)
Neural-LMC: A Physics-Inspired Neural Network Architecture

Refinements:
1. Gradient: Using "Surrogate Gradient" (STE-like) for stability (Option B).
   Exact derivative of sharp horizon kills learning. We use smooth tanh proxy.
2. Metric: MSE Rollout (Robust).
3. Baselines: ReLU+L2 (Strong Baseline) vs Tamesis.
4. Data: Steps=2000 (Consistent with V2 success).

Objective: Predict Lorenz Attractor chaotic time series.
Comparison: LMC/AMRD vs ReLU/L2.

Author: Antigravity AI for Tamesis Research
"""

import numpy as np
import matplotlib.pyplot as plt
import copy

# --- 1. DATASET: CHAOTIC LORENZ ATTRACTOR ---
def generate_lorenz_data(steps=2000, dt=0.01):
    sigma, rho, beta = 10.0, 28.0, 8.0/3.0
    xyz = np.zeros((steps, 3))
    xyz[0] = [1.0, 1.0, 1.0]
    
    for i in range(steps-1):
        x, y, z = xyz[i]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        xyz[i+1] = xyz[i] + dt * np.array([dx, dy, dz])
        
    # Normalize
    xyz = (xyz - np.mean(xyz, axis=0)) / np.std(xyz, axis=0)
    X = xyz[:-1]
    Y = xyz[1:]
    return X, Y

# --- 2. BASE NETWORK COMPONENTS ---
class Layer:
    def __init__(self, in_dim, out_dim, init_scale=0.1):
        self.W = np.random.randn(in_dim, out_dim) * init_scale
        self.b = np.zeros((1, out_dim))
        self.grad_W = np.zeros_like(self.W)
        self.grad_b = np.zeros_like(self.b)
        self.input = None
        self.z = None
        
    def forward(self, x):
        self.input = x
        self.z = np.dot(x, self.W) + self.b
        return self.z
        
    def backward(self, grad_output):
        self.grad_W = np.dot(self.input.T, grad_output)
        self.grad_b = np.sum(grad_output, axis=0, keepdims=True)
        return np.dot(grad_output, self.W.T)

# --- 3. ACTIVATIONS ---
def relu(x):
    return np.maximum(0, x)
def relu_deriv(x):
    return (x > 0).astype(float)

class LMC_Activation:
    """
    Formula: f(x) = x * tanh(k / |x|)
    Gradient: Surrogate (Option B) used for stability.
    We approximate backward pass of saturation as smooth tanh dampening.
    """
    def __init__(self, k=2.5):
        self.k = k
        self.last_x = None
        
    def forward(self, x):
        self.last_x = x
        eps = 1e-8
        abs_x = np.abs(x) + eps
        return x * np.tanh(self.k / abs_x)
        
    def backward(self, grad_output):
        # Surrogate Gradient:
        # Treat the function behavior as 'soft clamping'.
        # Approximating derivative as 1.0 - tanh^2(x/k) 
        # This matches the behavior: 1 near zero, 0 near infinity.
        # This was the V2 logic that worked.
        x = self.last_x
        # Scaled argument for surrogate
        arg = x / self.k
        d_mod = 1.0 - np.tanh(arg)**2
        return grad_output * d_mod

# --- 4. OPTIMIZERS ---
class SGD:
    def __init__(self, lr=0.01, weight_decay=0.0): # Standard L2
        self.lr = lr
        self.wd = weight_decay
        
    def step(self, layer):
        penalty = self.wd * layer.W
        layer.W -= self.lr * (layer.grad_W + penalty)
        layer.b -= self.lr * layer.grad_b

class AMRD_Optimizer:
    def __init__(self, lr=0.01, G=0.001):
        self.lr = lr
        self.G = G
        
    def step(self, layer):
        w_mean = np.mean(layer.W)
        gravity = self.G * (layer.W - w_mean) 
        layer.W -= self.lr * (layer.grad_W + gravity)
        layer.b -= self.lr * layer.grad_b

# --- 5. MODEL WRAPPER ---
class NeuralNet:
    def __init__(self, hidden_size, mode='ReLU', k=2.5):
        self.l1 = Layer(3, hidden_size)
        self.l2 = Layer(hidden_size, hidden_size)
        self.l3 = Layer(hidden_size, 3)
        self.mode = mode
        if mode == 'LMC':
            self.act = LMC_Activation(k=k)
        
    def forward(self, x):
        z1 = self.l1.forward(x)
        if self.mode == 'ReLU': a1 = relu(z1)
        else: a1 = self.act.forward(z1)
        
        z2 = self.l2.forward(a1)
        if self.mode == 'ReLU': a2 = relu(z2)
        else: a2 = self.act.forward(z2)
        
        out = self.l3.forward(a2)
        return out
        
    def backward(self, x, y_true, y_pred):
        grad_out = 2 * (y_pred - y_true) / x.shape[0]
        
        grad_a2 = self.l3.backward(grad_out)
        
        if self.mode == 'ReLU': grad_z2 = grad_a2 * relu_deriv(self.l2.z)
        else: grad_z2 = self.act.backward(grad_a2)
            
        grad_a1 = self.l2.backward(grad_z2)
        
        if self.mode == 'ReLU': grad_z1 = grad_a1 * relu_deriv(self.l1.z)
        else: grad_z1 = self.act.backward(grad_a1)
            
        self.l1.backward(grad_z1)

# --- 6. METRICS ---
def mse_rollout_error(model, start_x, steps, truth):
    curr = start_x.reshape(1, -1)
    preds = []
    for _ in range(steps):
        curr = model.forward(curr)
        preds.append(curr[0])
    preds = np.array(preds)
    t_slice = truth[:steps]
    return np.mean((preds - t_slice)**2)

# --- 7. EXPERIMENT RUNNER ---
def run_recovery_experiment():
    print("=== RECOVERY EXPERIMENT: V2 LOGIC + L2 BASELINE ===")
    
    X, Y = generate_lorenz_data(2000)
    split = 1600
    X_tr, Y_tr = X[:split], Y[:split]
    X_te, Y_te = X[split:], Y[split:]
    
    seeds = 5
    
    configs = [
        {'name': 'ReLU+L2 (Baseline)', 'mode': 'ReLU', 'opt': 'SGD_L2', 'k': 0},
        {'name': 'Tamesis (Surrogate)', 'mode': 'LMC', 'opt': 'AMRD', 'k': 2.5},
    ]
    
    final_results = {}
    
    for cfg in configs:
        name = cfg['name']
        print(f"\nTesting Config: {name}")
        scores = []
        
        for s in range(seeds):
            np.random.seed(s+100)
            model = NeuralNet(32, mode=cfg['mode'], k=cfg['k'])
            if cfg['opt'] == 'SGD_L2': opt = SGD(lr=0.01, weight_decay=0.01)
            else: opt = AMRD_Optimizer(lr=0.01, G=0.01)
            
            for epoch in range(80): # Little more training
                p = model.forward(X_tr)
                model.backward(X_tr, Y_tr, p)
                opt.step(model.l1); opt.step(model.l2); opt.step(model.l3)
                
            err = mse_rollout_error(model, X_te[0], 50, Y_te)
            scores.append(err)
            
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        final_results[name] = (mean_score, std_score)
        print(f"  -> Score (MSE): {mean_score:.4f} +/- {std_score:.4f}")

    print("\n| Configuration | Rollout Error (Mean) | Deviation |")
    print("|---|---|---|")
    for cfg in configs:
        n = cfg['name']
        print(f"| {n} | {final_results[n][0]:.4f} | {final_results[n][1]:.4f} |")
        
    # Plot
    plt.figure(figsize=(8, 5))
    names = [c['name'] for c in configs]
    means = [final_results[n][0] for n in names]
    stds = [final_results[n][1] for n in names]
    plt.bar(names, means, yerr=stds, capsize=10, color=['gray', 'blue'])
    plt.title('Tamesis vs Strong Baseline (ReLU+L2)')
    plt.ylabel('Rollout MSE (Lower is Better)')
    plt.savefig('final_recovery_benchmark.png')
    print("Saved final_recovery_benchmark.png")

if __name__ == "__main__":
    run_recovery_experiment()
