import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
INPUT_SIZE = 16
HIDDEN_SIZE = 128
LEARNING_RATE = 0.005
EPOCHS = 35000
BATCH_SIZE = 32
DIST_LAMBDA = 0.002 # Cost of Distance

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
    
    Y_parity = np.sum(X, axis=1) % 2
    Y_parity = Y_parity.reshape(-1, 1)
    
    input_sum = np.sum(X_model, axis=1) 
    Y_sine = np.sin(input_sum / 2.0)
    Y_sine = Y_sine.reshape(-1, 1)
    
    return X_model, Y_parity, Y_sine

class SpatialNet:
    def __init__(self):
        # He Init
        self.W1 = np.random.randn(INPUT_SIZE, HIDDEN_SIZE) * np.sqrt(2/INPUT_SIZE)
        self.b1 = np.zeros((1, HIDDEN_SIZE))
        
        # HEADS
        # Logic Head is at x=0
        # Chaos Head is at x=1
        self.W2a = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2a = np.zeros((1, 1))
        
        self.W2b = np.random.randn(HIDDEN_SIZE, 1) * np.sqrt(2/HIDDEN_SIZE)
        self.b2b = np.zeros((1, 1))
        
        # --- TOPOLOGY ---
        # Neuron positions x_i in [0, 1]
        self.neuron_pos = np.linspace(0, 1, HIDDEN_SIZE)
        
        # Calculate Distances to Heads
        # Head A is at 0.0. Dist = pos[i]
        self.dist_to_a = self.neuron_pos.reshape(-1, 1)
        
        # Head B is at 1.0. Dist = 1.0 - pos[i]
        self.dist_to_b = (1.0 - self.neuron_pos).reshape(-1, 1)

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
        
        # Gradients
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
        
        # --- SPATIAL UPDATE ---
        # Penalize W based on Distance
        # We assume W1 (Input->Hidden) has no distance cost (all inputs reach all hidden).
        # We ONLY penalize Hidden->Head connections.
        
        # Head A Penalty: W2a_i * Dist_i (to Head A)
        reg_grad_a = np.sign(self.W2a) * self.dist_to_a
        
        # Head B Penalty: W2b_i * Dist_i (to Head B)
        reg_grad_b = np.sign(self.W2b) * self.dist_to_b
        
        self.W1 -= LEARNING_RATE * dW1
        self.b1 -= LEARNING_RATE * db1
        
        self.W2a -= LEARNING_RATE * (dW2a + DIST_LAMBDA * reg_grad_a)
        self.b2a -= LEARNING_RATE * db2a
        
        self.W2b -= LEARNING_RATE * (dW2b + DIST_LAMBDA * reg_grad_b)
        self.b2b -= LEARNING_RATE * db2b
        
        loss_a = -np.mean(Y_a * np.log(self.prob_a + 1e-8) + (1-Y_a)*np.log(1-self.prob_a + 1e-8))
        loss_b = np.mean((self.pred_b - Y_b)**2)
        
        return loss_a, loss_b

def run_experiment():
    print(f"--- TAMESIS EXPERIMENT 02 v3: SPATIAL TRI ---")
    print(f"Goal: Force Spatial Separation (Hemispheres) via Wiring Cost.")
    
    net = SpatialNet()
    
    for i in range(EPOCHS):
        X, Ya, Yb = generate_data(BATCH_SIZE)
        net.forward(X)
        la, lb = net.backwards(X, Ya, Yb)
        
        if i % 5000 == 0:
            print(f"Epoch {i}: LossA={la:.4f}, LossB={lb:.4f}")
            
    # --- ANALYSIS ---
    print("\n--- ANALYZING TOPOLOGY ---")
    
    # Calculate Center of Mass for each Task
    # CoM = sum(|W_i| * Pos_i) / sum(|W_i|)
    
    w_a = np.abs(net.W2a).flatten()
    w_b = np.abs(net.W2b).flatten()
    pos = net.neuron_pos
    
    com_a = np.sum(w_a * pos) / (np.sum(w_a) + 1e-8)
    com_b = np.sum(w_b * pos) / (np.sum(w_b) + 1e-8)
    
    print(f"Center of Mass (Logic Head at 0): {com_a:.4f}")
    print(f"Center of Mass (Chaos Head at 1): {com_b:.4f}")
    
    separation = com_b - com_a
    print(f"Hemispheric Separation: {separation:.4f}")
    
    # Plot Strength vs Position
    plt.figure(figsize=(10, 6))
    plt.plot(pos, w_a, 'b-', alpha=0.7, label='Connection to Logic (Left)')
    plt.plot(pos, w_b, 'r-', alpha=0.7, label='Connection to Chaos (Right)')
    plt.xlabel("Neuron Position (0=Left, 1=Right)")
    plt.ylabel("Synaptic Strength")
    plt.title(f"Hemispheric Specialization (Separation={separation:.2f})")
    plt.legend()
    plt.grid(True)
    plt.savefig("spatial_tri_result.png")
    print("Map saved to spatial_tri_result.png")
    
    if separation > 0.3:
        print("\nSUCCESS: The network spontaneously lateralized!")
        print("Logic moved Left, Chaos moved Right. Geometry creates Modularity.")
    else:
        print("\nFAILURE: Mixed soup.")

if __name__ == "__main__":
    run_experiment()
