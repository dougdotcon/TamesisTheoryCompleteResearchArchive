"""
Stage 38: U_{1/2} Applications
==============================

TEST U_{1/2} IN SYSTEMS WITH DISCRETE STATE SPACES

HYPOTHESIS
----------
U_{1/2} should appear in any system where:
1. State space is discrete (finite n elements)
2. Perturbation probability is c/n per element
3. Observable counts "deterministic" fraction

CANDIDATE APPLICATIONS
----------------------
1. Quantum Error Correction: error threshold
2. Genetic Algorithms: fitness landscape navigation
3. Hash Tables: collision fraction
4. Database lookups: cache hit rate under noise
"""

import numpy as np
from scipy.optimize import curve_fit
from typing import List, Tuple


def u12(c):
    return (1 + c) ** (-0.5)


def power_law(c, alpha):
    return (1 + c) ** (-alpha)


# ============================================================
# APPLICATION 1: SIMPLIFIED QUANTUM ERROR CORRECTION MODEL
# ============================================================

class QuantumErrorCorrection:
    """
    Simplified model of quantum error correction threshold.
    
    Model: n qubits, each has probability p = c/n of error.
    "Correctable" if errors form correctable pattern.
    
    For simplicity: correctable = all errors in separate locations
    (no two adjacent errors).
    """
    
    def __init__(self, n_qubits: int):
        self.n = n_qubits
    
    def simulate(self, c: float, n_trials: int = 100) -> float:
        """
        Simulate error correction success rate.
        
        c = expected number of errors (probability p = c/n per qubit)
        Returns fraction of trials where errors are correctable.
        """
        p = c / self.n
        success_count = 0
        
        for _ in range(n_trials):
            # Generate errors
            errors = np.random.random(self.n) < p
            
            # Check if correctable: no adjacent errors
            correctable = True
            for i in range(self.n - 1):
                if errors[i] and errors[i+1]:
                    correctable = False
                    break
            
            if correctable:
                success_count += 1
        
        return success_count / n_trials


# ============================================================
# APPLICATION 2: GENETIC ALGORITHM FITNESS LANDSCAPE
# ============================================================

class GeneticAlgorithm:
    """
    Simplified GA: binary string optimization with noise.
    
    Model: n-bit string, target is all 1s.
    With probability c/n per bit, bit is flipped (mutated).
    "Success" if Hamming distance to target is <= threshold.
    """
    
    def __init__(self, n_bits: int, threshold: int = 0):
        self.n = n_bits
        self.threshold = threshold
    
    def simulate(self, c: float, n_trials: int = 100) -> float:
        """
        Simulate fraction of "successes" after mutation.
        
        Start with optimal solution (all 1s).
        Apply mutations with probability c/n per bit.
        Count fraction where solution is still "good".
        """
        p = c / self.n
        success_count = 0
        
        for _ in range(n_trials):
            # Start with optimal
            solution = np.ones(self.n, dtype=bool)
            
            # Apply mutations
            mutations = np.random.random(self.n) < p
            solution = solution ^ mutations  # XOR
            
            # Check fitness
            fitness = np.sum(solution)  # count of 1s
            hamming_distance = self.n - fitness
            
            if hamming_distance <= self.threshold:
                success_count += 1
        
        return success_count / n_trials


# ============================================================
# APPLICATION 3: HASH TABLE COLLISION MODEL
# ============================================================

class HashTable:
    """
    Model: n slots, insert elements with probability c/n of collision.
    
    Actually this is similar to the birthday problem / random maps.
    """
    
    def __init__(self, n_slots: int):
        self.n = n_slots
    
    def simulate(self, c: float, n_trials: int = 100) -> float:
        """
        Insert c elements into n slots.
        Return fraction of elements without collision.
        """
        n_inserts = int(c)
        if n_inserts == 0:
            return 1.0
        
        success_count = 0
        
        for _ in range(n_trials):
            slots = np.zeros(self.n, dtype=bool)
            no_collision_count = 0
            
            for _ in range(n_inserts):
                slot = np.random.randint(0, self.n)
                if not slots[slot]:
                    no_collision_count += 1
                slots[slot] = True
            
            success_count += no_collision_count / n_inserts
        
        return success_count / n_trials


def run_application_tests():
    """Test all applications for U_{1/2}."""
    
    print("=" * 70)
    print("STAGE 38: U_{1/2} APPLICATIONS")
    print("=" * 70)
    
    c_values = [1, 2, 5, 10, 20, 50]
    n = 500
    
    # Application 1: QEC
    print("\n1. QUANTUM ERROR CORRECTION MODEL")
    print("-" * 50)
    
    qec = QuantumErrorCorrection(n)
    qec_results = []
    
    print(f"{'c':>6} {'phi(data)':>12} {'phi(U_1/2)':>12} {'diff':>10}")
    print("-" * 45)
    
    for c in c_values:
        phi_data = qec.simulate(c, n_trials=100)
        phi_pred = u12(c)
        diff = abs(phi_data - phi_pred)
        qec_results.append((c, phi_data, phi_pred, diff))
        print(f"{c:>6} {phi_data:>12.4f} {phi_pred:>12.4f} {diff:>10.4f}")
    
    # Fit exponent
    c_arr = np.array([r[0] for r in qec_results])
    phi_arr = np.array([r[1] for r in qec_results])
    try:
        popt, _ = curve_fit(power_law, c_arr, phi_arr, p0=[0.5], bounds=(0.01, 5))
        print(f"\n   Fitted alpha = {popt[0]:.4f}")
        print(f"   U_{{1/2}} match: {abs(popt[0] - 0.5) < 0.2}")
    except:
        print("   Fit failed")
    
    # Application 2: GA
    print("\n\n2. GENETIC ALGORITHM MODEL")
    print("-" * 50)
    
    ga = GeneticAlgorithm(n, threshold=0)
    ga_results = []
    
    print(f"{'c':>6} {'phi(data)':>12} {'phi(U_1/2)':>12} {'diff':>10}")
    print("-" * 45)
    
    for c in c_values:
        phi_data = ga.simulate(c, n_trials=100)
        phi_pred = u12(c)
        diff = abs(phi_data - phi_pred)
        ga_results.append((c, phi_data, phi_pred, diff))
        print(f"{c:>6} {phi_data:>12.4f} {phi_pred:>12.4f} {diff:>10.4f}")
    
    c_arr = np.array([r[0] for r in ga_results])
    phi_arr = np.array([r[1] for r in ga_results])
    try:
        popt, _ = curve_fit(power_law, c_arr, phi_arr, p0=[0.5], bounds=(0.01, 5))
        print(f"\n   Fitted alpha = {popt[0]:.4f}")
        print(f"   U_{{1/2}} match: {abs(popt[0] - 0.5) < 0.2}")
    except:
        print("   Fit failed")
    
    # Application 3: Hash Table
    print("\n\n3. HASH TABLE COLLISION MODEL")
    print("-" * 50)
    
    ht = HashTable(n)
    ht_results = []
    
    print(f"{'c':>6} {'phi(data)':>12} {'phi(U_1/2)':>12} {'diff':>10}")
    print("-" * 45)
    
    for c in c_values:
        phi_data = ht.simulate(c, n_trials=100)
        phi_pred = u12(c)
        diff = abs(phi_data - phi_pred)
        ht_results.append((c, phi_data, phi_pred, diff))
        print(f"{c:>6} {phi_data:>12.4f} {phi_pred:>12.4f} {diff:>10.4f}")
    
    c_arr = np.array([r[0] for r in ht_results if r[0] > 0])
    phi_arr = np.array([r[1] for r in ht_results if r[0] > 0])
    try:
        popt, _ = curve_fit(power_law, c_arr, phi_arr, p0=[0.5], bounds=(0.01, 5))
        print(f"\n   Fitted alpha = {popt[0]:.4f}")
        print(f"   U_{{1/2}} match: {abs(popt[0] - 0.5) < 0.2}")
    except:
        print("   Fit failed")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    APPLICATION TESTING RESULTS:
    
    1. QEC Model: Tests error correction threshold
       - Measures fraction of correctable error patterns
       - Expected: U_{1/2} if errors are independent
    
    2. GA Model: Tests mutation robustness
       - Measures fraction of solutions surviving mutation
       - Expected: Exponential decay (different from U_{1/2})
    
    3. Hash Table: Tests collision-free fraction
       - Related to birthday problem
       - Expected: (1 - c/n)^c ~ exp(-c^2/n) for small c
    
    KEY INSIGHT:
    U_{1/2} appears specifically when the OBSERVABLE is CYCLE COUNTING.
    Other observables (survival, collision-free) have different exponents.
""")
    
    print("=" * 70)
    print("END OF APPLICATION TESTS")
    print("=" * 70)


if __name__ == "__main__":
    run_application_tests()
