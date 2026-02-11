import numpy as np
import matplotlib.pyplot as plt
import sys

# --- CONFIGURATION ---
INPUT_SIZE = 16
HIDDEN_SIZE = 128
LEARNING_RATE = 0.01
EPOCHS = 20000
BATCH_SIZE = 32

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    return (x > 0).astype(float)

# --- DATA GENERATION ---
def generate_data(batch_size):
    # Input: Random binary vectors (-1, 1 for better stability)
    X = np.random.randint(0, 2, size=(batch_size, INPUT_SIZE))
    X_model = 2 * X - 1 # Center around 0
    
    # Task A: PARITY (XOR of all bits) - Class A (Rigid/Discreete)
    # 1 if sum is odd, 0 if even
    Y_parity = np.sum(X, axis=1) % 2
    Y_parity = Y_parity.reshape(-1, 1)
    
    # Task B: SINE WAVE (Chaos/Continuous) - Class B
    # Map input sum to angle 0..4pi
    input_sum = np.sum(X_model, axis=1) # Range -16 to 16
    Y_sine = np.sin(input_sum / 2.0)
    Y_sine = Y_sine.reshape(-1, 1)
    
    return X_model, Y_parity, Y_sine

# --- MODEL (2-Layer MLP) ---
class MultiTaskNet:
    def __init__(self):
        # Weights initialized with He initialization
        self.W1 = np.random.randn(INPUT_SIZE, HIDDEN_SIZE) * np.sqrt(2/INPUT_SIZE)
        self.b1 = np.zeros((1, HIDDEN_SIZE))
        
        # Output Head A (Parity)
        self.W2a = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2a = np.zeros((1, 1))
        
        # Output Head B (Sine)
        self.W2b = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2b = np.zeros((1, 1))

    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = relu(self.z1) # Hidden Activations
        
        # Head A (Sigmoid for classification)
        self.z2a = np.dot(self.a1, self.W2a) + self.b2a
        self.prob_a = sigmoid(self.z2a)
        
        # Head B (Linear for regression)
        self.z2b = np.dot(self.a1, self.W2b) + self.b2b
        self.pred_b = self.z2b
        
        return self.prob_a, self.pred_b
    
    def backwards(self, X, Y_a, Y_b):
        m = X.shape[0]
        
        # Gradients Head A (BCE Loss derivative)
        dZ2a = self.prob_a - Y_a
        dW2a = np.dot(self.a1.T, dZ2a) / m
        db2a = np.sum(dZ2a, axis=0, keepdims=True) / m
        
        # Gradients Head B (MSE Loss derivative)
        dZ2b = (self.pred_b - Y_b)
        dW2b = np.dot(self.a1.T, dZ2b) / m
        db2b = np.sum(dZ2b, axis=0, keepdims=True) / m
        
        # Backprop to Hidden
        # Combine gradients from both tasks
        dA1 = np.dot(dZ2a, self.W2a.T) + np.dot(dZ2b, self.W2b.T)
        dZ1 = dA1 * relu_derivative(self.z1)
        
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        
        # Update
        self.W1 -= LEARNING_RATE * dW1
        self.b1 -= LEARNING_RATE * db1
        self.W2a -= LEARNING_RATE * dW2a
        self.b2a -= LEARNING_RATE * db2a
        self.W2b -= LEARNING_RATE * dW2b
        self.b2b -= LEARNING_RATE * db2b
        
        loss_a = -np.mean(Y_a * np.log(self.prob_a + 1e-8) + (1-Y_a)*np.log(1-self.prob_a + 1e-8))
        loss_b = np.mean((self.pred_b - Y_b)**2)
        
        return loss_a, loss_b

# --- EXPERIMENT ---
def run_experiment():
    print(f"--- TAMESIS EXPERIMENT 02: TRI INCOMPATIBILITY ---")
    print(f"Goal: Force 1 network to learn Logic (Parity) + Chaos (Sine).")
    print(f"Prediction: Network should modularize (split) to avoid interference.")
    
    net = MultiTaskNet()
    
    history_loss = []
    
    # Training Loop
    for i in range(EPOCHS):
        X, Ya, Yb = generate_data(BATCH_SIZE)
        net.forward(X)
        la, lb = net.backwards(X, Ya, Yb)
        history_loss.append(la + lb)
        
        if i % 2000 == 0:
            print(f"Epoch {i}: LossA(Parity)={la:.4f}, LossB(Sine)={lb:.4f}")

    # --- ANALYSIS: MODULARIZATION ---
    # We check if hidden neurons specialized.
    # We measure this by checking the weights W2a and W2b.
    # If neuron k serves Head A, |W2a[k]| should be high and |W2b[k]| low.
    
    print("\n--- ANALYZING STRUCTURE ---")
    
    # Normalize weights to importance
    imp_a = np.abs(net.W2a).flatten()
    imp_b = np.abs(net.W2b).flatten()
    
    # normalize
    imp_a /= np.max(imp_a)
    imp_b /= np.max(imp_b)
    
    # Scatter plot of Neuron Importance
    plt.figure(figsize=(8, 8))
    plt.scatter(imp_a, imp_b, c='purple', alpha=0.7)
    plt.plot([0,1], [0,1], 'k--', alpha=0.3, label="Mixed Neurons (Bad)")
    plt.title("Neuron Specialization Map (TRI Test)")
    plt.xlabel("Importance for Logic Task (Parity)")
    plt.ylabel("Importance for Chaos Task (Sine)")
    plt.grid(True)
    
    # Calculate "Modularization Score"
    # Ideal: Points cluster at (1,0) and (0,1). Bad: Points at (1,1).
    # We calculate angle from diagonal.
    
    # Distance from diagonal line y=x
    # D = |x - y| / sqrt(2)
    modularity = np.mean(np.abs(imp_a - imp_b))
    
    print(f"Modularization Score (0=Monolithic, 1=Perfect Split): {modularity:.4f}")
    
    # Zone classification
    # Pure A: x > 0.5, y < 0.2
    # Pure B: x < 0.2, y > 0.5
    # Mixed: Rest
    n_a = np.sum((imp_a > 0.5) & (imp_b < 0.2))
    n_b = np.sum((imp_a < 0.2) & (imp_b > 0.5))
    n_mixed = HIDDEN_SIZE - n_a - n_b
    
    print(f"Neurons Specialized for Logic: {n_a}")
    print(f"Neurons Specialized for Chaos: {n_b}")
    print(f"Confused/Mixed Neurons:      {n_mixed}")
    
    plt.axvspan(0.5, 1.0, ymin=0, ymax=0.2, color='blue', alpha=0.1, label='Logic Module')
    plt.axhspan(0.5, 1.0, xmin=0, xmax=0.2, color='red', alpha=0.1, label='Chaos Module')
    plt.legend()
    
    outfile = "tri_modularization_map.png"
    plt.savefig(outfile)
    print(f"Map saved to {outfile}")
    
    print("\n--- CONCLUSION ---")
    if modularity > 0.3 and (n_a > 0 and n_b > 0):
        print("SUCCESS. The network spontaneously lobotomized itself.")
        print("It created two distinct internal modules to solve the incompatible tasks.")
        print("TRI (Regime Incompatibility) is VALIDATED.")
    else:
        print("FAILURE. The network remained monolithic.")
        print("TRI is Falsified.")

if __name__ == "__main__":
    run_experiment()
