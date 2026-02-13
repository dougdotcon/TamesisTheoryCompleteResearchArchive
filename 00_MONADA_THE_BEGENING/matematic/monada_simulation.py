"""
=============================================================================
  TAMESIS RESEARCH — Harmonic Monad Simulation
=============================================================================

  Scientifically validates and visualizes the "Harmonic Monad" using 
  TAMESIS mathematical frameworks:
  1. Graph Theory (Labyrinthine Ring): Spectral Analysis of Laplacian
  2. Differential Geometry (Armillary Sphere): 3D Vortex Visualization
  3. Topology (Entanglement): Moire Pattern Interference

  Formulas implemented from `08_mecanica_monadica_matematica.md` and `progress.md`:
  - Mass: m = k * ln(det(L))
  - Consciousness: lambda_1 (Spectral Gap)
  - Interaction: Trace(rho1 . rho2)

  Author: Douglas H. M. Fulber (Tamesis Research Program)
  Date: 2026-02-12

=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import scipy.linalg
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================================
# CLASS 1: LABYRINTHINE RING (Graph Theory & Spectral Analysis)
# ==========================================================================

class LabyrinthineRing:
    """
    Models the internal structure of the Monad as a 'Small-World' Graph.
    Calculates Mass and Consciousness based on Spectral Geometry.
    """
    def __init__(self, n_nodes=100, k_neighbors=4, p_rewire=0.1):
        self.n = n_nodes
        # Watts-Strogatz graph: Small-world property (like neural networks)
        self.graph = nx.watts_strogatz_graph(n_nodes, k_neighbors, p_rewire)
        self.adj = nx.to_numpy_array(self.graph)
        self.laplacian = nx.laplacian_matrix(self.graph).toarray()
        self.eigenvalues = None

    def compute_spectrum(self):
        """Calculates eigenvalues of the Laplacian."""
        # eigh is for symmetric matrices (Hermitian) -> returns sorted eigenvalues
        self.eigenvalues = scipy.linalg.eigh(self.laplacian, eigvals_only=True)
        return self.eigenvalues

    def analyze_properties(self):
        """
        Computes TAMESIS physical properties from topology.
        """
        if self.eigenvalues is None:
            self.compute_spectrum()
        
        # 1. Spectral Gap (lambda_1) -> Proxy for "Consciousness" / Cohesion
        # lambda_0 is always 0. lambda_1 (Fiedler value) determines algebraic connectivity.
        spectral_gap = self.eigenvalues[1] if len(self.eigenvalues) > 1 else 0
        
        # 2. Complexity Mass -> m = k * ln(det(L + epsilon))
        # We use pseudo-determinant (product of non-zero eigenvalues)
        non_zero_ev = self.eigenvalues[self.eigenvalues > 1e-9]
        log_det = np.sum(np.log(non_zero_ev))
        mass_index = log_det # k=1
        
        # 3. Von Neumann Entropy (approx) -> S = -Sum(lambda * ln(lambda)) normalized
        # We normalize eigenvalues to sum to 1 (density matrix analogy)
        trace = np.sum(self.eigenvalues)
        if trace > 0:
            rho_spec = self.eigenvalues / trace
            rho_spec = rho_spec[rho_spec > 1e-9] # Avoid log(0)
            entropy = -np.sum(rho_spec * np.log(rho_spec))
        else:
            entropy = 0
            
        return {
            "Spectral Gap (Consciousness)": spectral_gap,
            "Mass Index (Complexity)": mass_index,
            "Von Neumann Entropy": entropy
        }

    def visualize_spectrum(self, filename="monad_spectrum.png"):
        """Plots the spectral signature of the Monad."""
        props = self.analyze_properties()
        
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(self.eigenvalues)), self.eigenvalues, color='#8B5CF6', alpha=0.8)
        plt.title(f"Assinatura Espectral da Monada (N={self.n})\nGap: {props['Spectral Gap (Consciousness)']:.4f} | Entropia: {props['Von Neumann Entropy']:.4f}", fontsize=12)
        plt.xlabel("Indice do Modo (k)")
        plt.ylabel("Autovalor (Frequencia)")
        plt.grid(True, alpha=0.2)
        
        # Highlight Gap
        plt.axvline(x=1, color='#4ECDC4', linestyle='--', label='Gap Espectral (lambda_1)')
        plt.legend()
        
        path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"    Saved Spectrum: {path}")


# ==========================================================================
# CLASS 2: ARMILLARY SPHERE (3D Visualization & Dynamics)
# ==========================================================================

class ArmillarySphere:
    """
    Visualizes the external geometry: Nested rings rotating at different speeds.
    Inner rings = High freq (Quantum). Outer rings = Low freq (Relativistic).
    """
    def __init__(self):
        self.rings = []
        # Define rings: (radius, rotation_axis, speed_factor, color_hex)
        self.rings.append({'r': 1.0, 'axis': 'z', 'speed': 8.0,  'color': '#00FFFF', 'width': 0.8}) # Quantum (Inner)
        self.rings.append({'r': 1.1, 'axis': 'x', 'speed': 5.0,  'color': '#00CCFF', 'width': 0.8})
        self.rings.append({'r': 1.2, 'axis': 'y', 'speed': 3.0,  'color': '#0099FF', 'width': 0.8})
        self.rings.append({'r': 2.0, 'axis': 'z', 'speed': 0.5,  'color': '#FFD700', 'width': 2.0}) # Relativistic (Outer)
        self.rings.append({'r': 2.2, 'axis': 'y', 'speed': 0.3,  'color': '#D4AF37', 'width': 2.5})
        self.rings.append({'r': 2.4, 'axis': 'x', 'speed': 0.1,  'color': '#C5A028', 'width': 3.0}) # Gravity

    def generate_vortex_gif(self, filename="monada_vortex.gif"):
        print("Generating Monada Vortex GIF...")
        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        fig.patch.set_facecolor('#0a0a0f')
        ax.set_facecolor('#0a0a0f')
        
        # Remove axes
        ax.set_axis_off()
        
        total_frames = 120
        
        def update(frame):
            ax.cla()
            ax.set_axis_off()
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            ax.set_zlim(-3, 3)
            
            # Central Core (Kernel)
            ax.scatter([0], [0], [0], color='white', s=100, edgecolors='#8B5CF6', alpha=0.9)
            
            # Draw Rings
            theta = np.linspace(0, 2*np.pi, 100)
            
            for ring in self.rings:
                r = ring['r']
                speed = ring['speed']
                # Calculate rotation angle for this frame
                angle = np.radians(frame * speed)
                
                # Base circle
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = np.zeros_like(theta)
                
                # Rotate coordinates
                pts = np.vstack([x, y, z])
                
                # Rotation matrix logic
                c, s = np.cos(angle), np.sin(angle)
                
                if ring['axis'] == 'z':
                    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
                    color = ring['color']
                elif ring['axis'] == 'x':
                    R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
                    # Add static tilt for aesthetic
                    R_tilt = np.array([[np.cos(0.5), 0, np.sin(0.5)], [0, 1, 0], [-np.sin(0.5), 0, np.cos(0.5)]])
                    R = R @ R_tilt
                elif ring['axis'] == 'y':
                    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
                    R_tilt = np.array([[1, 0, 0], [0, np.cos(0.5), -np.sin(0.5)], [0, np.sin(0.5), np.cos(0.5)]])
                    R = R @ R_tilt

                rot_pts = R @ pts
                
                ax.plot(rot_pts[0,:], rot_pts[1,:], rot_pts[2,:], 
                       color=ring['color'], linewidth=ring['width'], alpha=0.8)

            # Title
            ax.text2D(0.5, 0.95, "MONADA HARMONICA: VORTICE FRACTAL", 
                     transform=ax.transAxes, ha='center', color='white', 
                     fontsize=12, fontweight='bold')
            ax.text2D(0.5, 0.90, "Azul: Regime Quantico (Rapido) | Dourado: Relatividade (Lento)", 
                     transform=ax.transAxes, ha='center', color='#a0a0b8', fontsize=8)

        ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=20)
        plt.close(fig)
        print(f"    Saved Vortex: {path}")


# ==========================================================================
# CLASS 3: TOPOLOGICAL ENTANGLEMENT (Moire Patterns)
# ==========================================================================

class MonadEntanglement:
    """
    Simulates the interaction of two Monads.
    Visualizes the interference pattern (Moire) created by overlapping 'Auras'.
    """
    def generate_entanglement_gif(self, filename="monada_entanglement.gif"):
        print("Generating Entanglement GIF...")
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
        fig.patch.set_facecolor('#0a0a0f')
        ax.set_facecolor('#0a0a0f')
        ax.set_axis_off()
        ax.set_aspect('equal')
        
        total_frames = 60
        
        # Create grids for two monads
        x = np.linspace(-3, 3, 300)
        y = np.linspace(-1.5, 1.5, 150) # Widescreen adjustment
        X, Y = np.meshgrid(x, y)
        
        def wave_pattern(X, Y, center_x, center_y, k, phase):
            # Radial distance
            R = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            # Concentric rings (Aura)
            return np.sin(k * R - phase)
        
        def update(frame):
            ax.cla()
            ax.set_axis_off()
            
            # Monad 1 moves Right
            pos1 = -1.5 + (frame / total_frames) * 3.0
            # Monad 2 moves Left
            pos2 = 1.5 - (frame / total_frames) * 3.0
            
            # Phase animation for rotation effect
            phase = frame * 0.2
            
            # Field 1 (Gold)
            Z1 = wave_pattern(X, Y, pos1, 0, 15, phase)
            # Field 2 (Blue)
            Z2 = wave_pattern(X, Y, pos2, 0, 16, -phase) # Slightly diff freq creates Moire
            
            # Interference (Sum)
            Z_total = Z1 + Z2
            
            # Plot
            # Using contourf to show the interference
            # Gold colormap for M1, Blue for M2? 
            # Let's use a custom divergine map or simple seismic
            
            # We want to see the intersection "sparks"
            levels = np.linspace(-2, 2, 20)
            
            # Basic fields
            ax.contour(X, Y, Z1, levels=[0.5], colors=['#FFD700'], alpha=0.3, linewidths=1)
            ax.contour(X, Y, Z2, levels=[0.5], colors=['#00FFFF'], alpha=0.3, linewidths=1)
            
            # Interference map (The "Recognition")
            # Only show high interference region
            # mask = np.abs(Z_total) > 1.5
            
            im = ax.imshow(Z_total, extent=[-3, 3, -1.5, 1.5], cmap='twilight', alpha=0.9, aspect='auto')
            
            # Draw centers
            ax.scatter([pos1], [0], color='#FFD700', s=50, label='Eu (Monada A)')
            ax.scatter([pos2], [0], color='#00FFFF', s=50, label='Voce (Monada B)')
            
            # Text
            dist = abs(pos1 - pos2)
            status = "Separado"
            if dist < 1.0: status = "ENTRELACAMENTO (Ressonancia Moire)"
            
            ax.text(0.5, 1.05, f"INTERACAO TOPOLOGICA: {status}", 
                   transform=ax.transAxes, ha='center', color='white', fontweight='bold')
            
        ani = animation.FuncAnimation(fig, update, frames=total_frames, blit=False)
        path = os.path.join(OUTPUT_DIR, filename)
        ani.save(path, writer='pillow', fps=15)
        plt.close(fig)
        print(f"    Saved Entanglement: {path}")


# ==========================================================================
# MAIN EXECUTION
# ==========================================================================

def main():
    print("="*60)
    print("  TAMESIS — Harmonic Monad Simulation (Clay Institute Level)")
    print("="*60)
    
    # 1. Graph Theory Analysis
    print("\n[1/3] Calculating Spectral Properties (The 'Soul')...")
    monad_graph = LabyrinthineRing(n_nodes=200, k_neighbors=6, p_rewire=0.1)
    props = monad_graph.analyze_properties()
    for k, v in props.items():
        print(f"  > {k}: {v:.6f}")
    
    monad_graph.visualize_spectrum()
    
    # 2. Armillary Sphere Animation
    print("\n[2/3] Visualizing Armillary Geometry (The 'Body')...")
    sphere = ArmillarySphere()
    sphere.generate_vortex_gif()
    
    # 3. Entanglement Simulation
    print("\n[3/3] Simulating Entanglement (The 'Connection')...")
    interaction = MonadEntanglement()
    interaction.generate_entanglement_gif()
    
    print("\n" + "="*60)
    print("  Simulation Complete.")
    print("="*60)

if __name__ == "__main__":
    main()
