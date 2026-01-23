"""
Modular Group SL(2,Z) and Fundamental Domain
=============================================

Stage 10: The modular group and its action on H.

THE MODULAR GROUP
-----------------
SL(2,Z) = { [[a,b],[c,d]] : a,b,c,d ∈ Z, ad - bc = 1 }

Acts on H by Möbius transformations:
    γ · z = (az + b) / (cz + d)

GENERATORS
----------
T = [[1,1],[0,1]]  (translation: z → z + 1)
S = [[0,-1],[1,0]] (inversion: z → -1/z)

FUNDAMENTAL DOMAIN
------------------
F = { z ∈ H : |z| ≥ 1, |Re(z)| ≤ 1/2 }

Area(F) = π/3
"""

import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
import matplotlib.patches as mpatches


class ModularGroup:
    """
    The modular group SL(2,Z) and its action on H.
    """
    
    # Generators
    T = np.array([[1, 1], [0, 1]], dtype=int)  # z → z + 1
    S = np.array([[0, -1], [1, 0]], dtype=int)  # z → -1/z
    
    def __init__(self):
        pass
    
    @staticmethod
    def is_valid_matrix(gamma: np.ndarray) -> bool:
        """
        Check if matrix is in SL(2,Z).
        """
        a, b, c, d = gamma[0, 0], gamma[0, 1], gamma[1, 0], gamma[1, 1]
        det = a * d - b * c
        
        # Must have det = 1 and integer entries
        return det == 1 and all(isinstance(x, (int, np.integer)) for x in [a, b, c, d])
    
    @staticmethod
    def action(gamma: np.ndarray, z: complex) -> complex:
        """
        Möbius action of γ on z.
        
        γ · z = (az + b) / (cz + d)
        """
        a, b, c, d = gamma[0, 0], gamma[0, 1], gamma[1, 0], gamma[1, 1]
        
        denominator = c * z + d
        if abs(denominator) < 1e-10:
            return complex(np.inf, np.inf)  # Point at infinity
        
        return (a * z + b) / denominator
    
    @staticmethod
    def compose(gamma1: np.ndarray, gamma2: np.ndarray) -> np.ndarray:
        """
        Compose two modular transformations.
        """
        return gamma1 @ gamma2
    
    @staticmethod
    def inverse(gamma: np.ndarray) -> np.ndarray:
        """
        Inverse of a modular transformation.
        
        For [[a,b],[c,d]] in SL(2,Z), inverse is [[d,-b],[-c,a]]
        """
        a, b, c, d = gamma[0, 0], gamma[0, 1], gamma[1, 0], gamma[1, 1]
        return np.array([[d, -b], [-c, a]], dtype=int)
    
    def in_fundamental_domain(self, z: complex, tol: float = 1e-10) -> bool:
        """
        Check if z is in the standard fundamental domain F.
        
        F = { z ∈ H : |z| ≥ 1, |Re(z)| ≤ 1/2 }
        """
        return (z.imag > 0 and 
                abs(z) >= 1 - tol and 
                abs(z.real) <= 0.5 + tol)
    
    def reduce_to_fundamental(self, z: complex, max_iter: int = 1000) -> Tuple[complex, np.ndarray]:
        """
        Reduce z to the fundamental domain using modular transformations.
        
        Returns (z_reduced, gamma) where gamma · z_reduced = z
        """
        gamma_total = np.eye(2, dtype=int)
        z_current = z
        
        for _ in range(max_iter):
            # Apply T^n to bring Re(z) to [-1/2, 1/2]
            n = round(z_current.real)
            if n != 0:
                Tn = np.array([[1, -n], [0, 1]], dtype=int)
                z_current = self.action(Tn, z_current)
                gamma_total = self.compose(Tn, gamma_total)
            
            # If |z| < 1, apply S
            if abs(z_current) < 1 - 1e-10:
                z_current = self.action(self.S, z_current)
                gamma_total = self.compose(self.S, gamma_total)
            else:
                break
        
        return z_current, self.inverse(gamma_total)
    
    def fundamental_domain_area(self) -> float:
        """
        Area of the fundamental domain.
        
        Area = π/3
        """
        return np.pi / 3


class FundamentalDomainVisualizer:
    """
    Visualize the fundamental domain and modular group action.
    """
    
    def __init__(self):
        self.M = ModularGroup()
    
    def plot_fundamental_domain(self, ax=None, y_max: float = 2.5):
        """
        Plot the standard fundamental domain.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 10))
        
        # The fundamental domain boundary
        # Left edge: x = -1/2
        # Right edge: x = 1/2
        # Bottom: arc |z| = 1
        
        # Arc from -1/2 + sqrt(3)/2 i to 1/2 + sqrt(3)/2 i
        theta = np.linspace(2*np.pi/3, np.pi/3, 100)
        arc_x = np.cos(theta)
        arc_y = np.sin(theta)
        
        # Left edge
        left_x = [-0.5, -0.5]
        left_y = [np.sqrt(3)/2, y_max]
        
        # Right edge
        right_x = [0.5, 0.5]
        right_y = [np.sqrt(3)/2, y_max]
        
        # Fill the fundamental domain
        vertices = np.array([
            [-0.5, y_max],
            [-0.5, np.sqrt(3)/2],
            *zip(arc_x, arc_y),
            [0.5, np.sqrt(3)/2],
            [0.5, y_max]
        ])
        poly = Polygon(vertices, alpha=0.3, facecolor='blue', edgecolor='blue', linewidth=2)
        ax.add_patch(poly)
        
        # Plot boundary
        ax.plot(arc_x, arc_y, 'b-', linewidth=2)
        ax.plot(left_x, left_y, 'b-', linewidth=2)
        ax.plot(right_x, right_y, 'b-', linewidth=2)
        
        # Plot neighboring copies
        for dx in [-1, 1]:
            ax.plot(arc_x + dx, arc_y, 'b--', alpha=0.3, linewidth=1)
            ax.plot([dx - 0.5, dx - 0.5], [0.1, y_max], 'b--', alpha=0.3, linewidth=1)
        
        # Mark special points
        ax.plot(0, 1, 'ro', markersize=8)
        ax.annotate('i', (0.05, 1), fontsize=12)
        
        rho = complex(-0.5, np.sqrt(3)/2)
        ax.plot(rho.real, rho.imag, 'go', markersize=8)
        ax.annotate('ρ = e^{2πi/3}', (-0.45, rho.imag - 0.1), fontsize=10)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(0, y_max)
        ax.set_aspect('equal')
        ax.set_xlabel('Re(z)')
        ax.set_ylabel('Im(z)')
        ax.set_title('Fundamental Domain of SL(2,Z)\\H')
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5, linestyle='--', alpha=0.5)
        
        return ax


def main():
    """
    Demonstrate modular group and fundamental domain.
    """
    print("=" * 70)
    print("STAGE 10: MODULAR GROUP SL(2,Z)")
    print("=" * 70)
    
    M = ModularGroup()
    
    # 1. Generators
    print("\n1. GENERATORS")
    print("-" * 50)
    print(f"   T (translation):\n{M.T}")
    print(f"   S (inversion):\n{M.S}")
    
    # 2. Action examples
    print("\n2. MODULAR ACTION")
    print("-" * 50)
    
    z = complex(0, 1)  # i
    print(f"   z = i")
    print(f"   T · i = i + 1 = {M.action(M.T, z)}")
    print(f"   S · i = -1/i = {M.action(M.S, z)}")
    
    # 3. Fundamental domain check
    print("\n3. FUNDAMENTAL DOMAIN")
    print("-" * 50)
    
    test_points = [
        complex(0, 1),
        complex(0, 2),
        complex(0.3, 1.5),
        complex(0.6, 0.5),
        complex(-0.4, 0.9),
    ]
    
    for z in test_points:
        in_F = M.in_fundamental_domain(z)
        print(f"   z = {z}: in F = {in_F}")
    
    # 4. Reduction to fundamental domain
    print("\n4. REDUCTION TO FUNDAMENTAL DOMAIN")
    print("-" * 50)
    
    z_outside = complex(3.7, 0.5)
    z_reduced, gamma = M.reduce_to_fundamental(z_outside)
    print(f"   Original: z = {z_outside}")
    print(f"   Reduced:  z' = {z_reduced:.4f}")
    print(f"   In F: {M.in_fundamental_domain(z_reduced)}")
    
    # 5. Area
    print("\n5. FUNDAMENTAL DOMAIN PROPERTIES")
    print("-" * 50)
    print(f"   Area = π/3 = {M.fundamental_domain_area():.6f}")
    print(f"   Cusp at infinity")
    print(f"   2 elliptic points: i (order 2) and ρ (order 3)")
    
    print("\n" + "=" * 70)
    print("END OF MODULAR GROUP DEMONSTRATION")
    print("=" * 70)
    
    return M


if __name__ == "__main__":
    M = main()
