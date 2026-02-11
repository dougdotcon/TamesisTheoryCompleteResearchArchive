import numpy as np
import matplotlib.pyplot as plt
import sys

# --- CONFIGURATION ---
INPUT_SIZE = 16
HIDDEN_SIZE = 128
LEARNING_RATE = 0.005
EPOCHS = 25000
BATCH_SIZE = 32
L1_LAMBDA = 0.002 # The Metabolic Cost (Price of connection)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

def generate_data(batch_size):
    X = np.random.randint(0, 2, size=(batch_size, INPUT_SIZE))
    X_model = 2 * X - 1
    
    # Task A: Parity
    Y_parity = np.sum(X, axis=1) % 2
    Y_parity = Y_parity.reshape(-1, 1)
    
    # Task B: Sine
    input_sum = np.sum(X_model, axis=1) 
    Y_sine = np.sin(input_sum / 2.0)
    Y_sine = Y_sine.reshape(-1, 1)
    
    return X_model, Y_parity, Y_sine

class MetabolicNet:
    def __init__(self):
        # He Init
        self.W1 = np.random.randn(INPUT_SIZE, HIDDEN_SIZE) * np.sqrt(2/INPUT_SIZE)
        self.b1 = np.zeros((1, HIDDEN_SIZE))
        
        # Heads
        self.W2a = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2a = np.zeros((1, 1))
        
        self.W2b = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2b = np.zeros((1, 1))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = relu(self.z1)
        
        self.z2a = np.dot(self.a1, self.W2a) + self.b2a
        self.prob_a = sigmoid(self.z2a)
        
        self.z2b = np.dot(self.a1, self.W2b) + self.b2b
        self.pred_b = self.z2b
        return self.prob_a, self.pred_b
    
    def backwards(self, X, Y_a, Y_b):
        m = X.shape[0]
        
        # Standard Gradients
        dZ2a = self.prob_a - Y_a
        dW2a = np.dot(self.a1.T, dZ2a) / m
        db2a = np.sum(dZ2a, axis=0, keepdims=True) / m
        
        dZ2b = (self.pred_b - Y_b)
        dW2b = np.dot(self.a1.T, dZ2b) / m
        db2b = np.sum(dZ2b, axis=0, keepdims=True) / m
        
        dA1 = np.dot(dZ2a, self.W2a.T) + np.dot(dZ2b, self.W2b.T)
        dZ1 = dA1 * relu_derivative(self.z1)
        
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # --- METABOLIC UPDATE (L1 Regularization) ---
        # W = W - lr * (gradient + lambda * sign(W))
        # This forces small weights to ZERO (Pruning)
        
        self.W1 -= LEARNING_RATE * (dW1 + L1_LAMBDA * np.sign(self.W1))
        self.b1 -= LEARNING_RATE * db1
        
        self.W2a -= LEARNING_RATE * (dW2a + L1_LAMBDA * np.sign(self.W2a))
        self.b2a -= LEARNING_RATE * db2a
        
        self.W2b -= LEARNING_RATE * (dW2b + L1_LAMBDA * np.sign(self.W2b))
        self.b2b -= LEARNING_RATE * db2b
        
        # Losses
        loss_a = -np.mean(Y_a * np.log(self.prob_a + 1e-8) + (1-Y_a)*np.log(1-self.prob_a + 1e-8))
        loss_b = np.mean((self.pred_b - Y_b)**2)
        
        return loss_a, loss_b

def run_experiment():
    print(f"--- TAMESIS EXPERIMENT 02 v2: METABOLIC TRI ---")
    print(f"Goal: Force Modularization via Energy Cost (L1 Lambda={L1_LAMBDA}).")
    
    net = MetabolicNet()
    
    for i in range(EPOCHS):
        X, Ya, Yb = generate_data(BATCH_SIZE)
        net.forward(X)
        la, lb = net.backwards(X, Ya, Yb)
        
        if i % 5000 == 0:
            print(f"Epoch {i}: LossA={la:.4f}, LossB={lb:.4f}")
            
    # --- ANALYSIS ---
    print("\n--- ANALYZING STRUCTURE ---")
    
    # Pruning Threshold (weights effectively zero)
    THRESHOLD = 0.05
    
    imp_a = np.abs(net.W2a).flatten()
    imp_b = np.abs(net.W2b).flatten()
    
    # Count dead neurons
    dead_neurons = np.sum((imp_a < THRESHOLD) & (imp_b < THRESHOLD))
    print(f"Dead/Pruned Neurons: {dead_neurons} (Energy Saving)")
    
    # Scale for plot
    max_val = max(np.max(imp_a), np.max(imp_b)) + 1e-6
    imp_a /= max_val
    imp_b /= max_val
    
    # Calculate Modularity Score
    # Ideally, points are on axes.
    # We penalize points that are far from axes (i.e. x*y is large)
    # Score = 1 - 2*mean(x*y)  (If x=1,y=0 -> x*y=0 -> Score=1. If x=1,y=1 -> x*y=1 -> Score=-1)
    
    modularity = 1.0 - 2.0 * np.mean(imp_a * imp_b)
    
    n_a = np.sum((imp_a > 0.2) & (imp_b < 0.2))
    n_b = np.sum((imp_a < 0.2) & (imp_b > 0.2))
    n_mixed = np.sum((imp_a > 0.2) & (imp_b > 0.2))
    
    print(f"Neurons Logic-Only:    {n_a}")
    print(f"Neurons Chaos-Only:    {n_b}")
    print(f"Neurons Mixed (Bad):   {n_mixed}")
    print(f"Modularization Score:  {modularity:.4f}")
    
    # Plot
    plt.figure(figsize=(8, 8))
    plt.scatter(imp_a, imp_b, c='green', alpha=0.7)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.title(f"Metabolic Neuron Map (Lambda={L1_LAMBDA})")
    plt.xlabel("Connection to Logic Head")
    plt.ylabel("Connection to Chaos Head")
    plt.grid(True)
    plt.savefig("metabolic_tri_result.png")
    print("Map saved to metabolic_tri_result.png")
    
    if modularity > 0.5 and n_mixed < min(n_a, n_b):
        print("\nSUCCESS: The network modularized under energy pressure!")
        print("This validates the Tamesis Cognitive Topology hypothesis.")
    else:
        print("\nFAILURE: Still monolithic or dead.")

if __name__ == "__main__":
    run_experiment()
