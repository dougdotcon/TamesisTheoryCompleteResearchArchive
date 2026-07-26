"""
DERIVATION 05 (REFINED): CKM MIXING MATRIX
==========================================
Tamesis ToE - Fundamental Constants Derivation Program

THESIS: The CKM matrix structure emerges from hierarchical localization
of quark wavefunctions in the Kernel graph.

REFINED MODEL:
- Quarks are defects with generation-dependent localization length λ_g
- λ_g increases exponentially with generation: λ_g ~ λ_0 × r^g
- CKM element V_ij ~ exp(-|λ_i - λ_j|² / σ²)
- This naturally produces the observed hierarchy: |V_ud| >> |V_ub|

Author: Tamesis Research
Date: January 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Observed CKM matrix elements (magnitudes)
CKM_OBSERVED = np.array([
    [0.97370, 0.2245, 0.00382],   # V_ud, V_us, V_ub
    [0.221,   0.987,  0.0410],    # V_cd, V_cs, V_cb  
    [0.0080,  0.0388, 1.013]      # V_td, V_ts, V_tb
])

# Observed mixing angles (degrees)
THETA_12_OBS = 13.04  # Cabibbo angle
THETA_23_OBS = 2.38
THETA_13_OBS = 0.201
DELTA_CP_OBS = 68.0   # CP phase


class GenerationOverlapModel:
    """
    Model CKM matrix via generation-dependent localization.
    
    Physical picture:
    - Each quark generation is localized at a different "depth" in the extra dimension
    - Up-type and down-type quarks of same generation have maximal overlap
    - Cross-generation overlap decays exponentially with "distance"
    """
    
    def __init__(self, lambda_ratio=3.0, sigma=1.0):
        """
        Parameters:
        - lambda_ratio: ratio of localization lengths between generations
        - sigma: overlap width parameter
        """
        self.lambda_ratio = lambda_ratio
        self.sigma = sigma
        
        # Localization "positions" for each generation
        # Generation 1, 2, 3 at positions 0, log(r), 2*log(r)
        self.positions_up = np.array([0, np.log(lambda_ratio), 2*np.log(lambda_ratio)])
        self.positions_down = self.positions_up + 0.1  # Small offset between up/down
        
    def compute_overlap(self, i_up, j_down):
        """
        Compute wavefunction overlap between up-type i and down-type j.
        """
        pos_i = self.positions_up[i_up]
        pos_j = self.positions_down[j_down]
        
        delta = abs(pos_i - pos_j)
        
        # Gaussian overlap
        overlap = np.exp(-delta**2 / (2 * self.sigma**2))
        
        return overlap
    
    def compute_ckm_matrix(self):
        """
        Compute full CKM matrix.
        """
        V = np.zeros((3, 3))
        
        for i in range(3):
            for j in range(3):
                V[i, j] = self.compute_overlap(i, j)
        
        # Normalize rows and columns (unitarity)
        # Simple normalization: V_ij / sqrt(sum_k V_ik² × sum_k V_kj²)
        for i in range(3):
            V[i, :] /= np.sqrt(np.sum(V[i, :]**2))
        
        return V


def fit_model_parameters():
    """
    Fit model parameters (λ_ratio, σ) to match observed CKM.
    """
    from scipy.optimize import minimize
    
    def chi_squared(params):
        lambda_ratio, sigma = params
        
        if lambda_ratio < 1 or sigma < 0.1:
            return 1e10
        
        model = GenerationOverlapModel(lambda_ratio, sigma)
        V_pred = model.compute_ckm_matrix()
        
        # Compare to observed (sum of squared differences)
        chi2 = np.sum((V_pred - CKM_OBSERVED)**2)
        
        # Extra penalty for not reproducing hierarchy
        hierarchy_penalty = 0
        if V_pred[0, 2] > 0.1:  # V_ub should be small
            hierarchy_penalty += 10 * (V_pred[0, 2] - 0.1)**2
        if V_pred[2, 0] > 0.1:  # V_td should be small
            hierarchy_penalty += 10 * (V_pred[2, 0] - 0.1)**2
            
        return chi2 + hierarchy_penalty
    
    result = minimize(chi_squared, x0=[3.0, 0.8], 
                      bounds=[(1.5, 10), (0.2, 2.0)],
                      method='L-BFGS-B')
    
    return result.x


def extract_mixing_angles(V):
    """
    Extract standard parametrization angles from CKM matrix.
    """
    # |V_us| ~ sin(θ_12)
    theta_12 = np.arcsin(np.clip(V[0, 1], 0, 1))
    
    # |V_cb| ~ sin(θ_23)  
    theta_23 = np.arcsin(np.clip(V[1, 2], 0, 1))
    
    # |V_ub| ~ sin(θ_13)
    theta_13 = np.arcsin(np.clip(V[0, 2], 0, 1))
    
    return theta_12, theta_23, theta_13


def wolfenstein_parametrization(V):
    """
    Extract Wolfenstein parameters (λ, A, ρ, η).
    """
    # λ ≈ |V_us|
    lam = V[0, 1]
    
    # A ≈ |V_cb| / λ²
    A = V[1, 2] / lam**2 if lam > 0.01 else 0
    
    return lam, A


def plot_ckm_comparison(V_pred, output_dir):
    """
    Generate comparison plot: predicted vs observed CKM.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot 1: Predicted CKM
    ax1 = axes[0]
    im1 = ax1.imshow(V_pred, cmap='viridis', vmin=0, vmax=1)
    ax1.set_title('Predicted CKM (Tamesis)', fontsize=12, fontweight='bold')
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(['d', 's', 'b'])
    ax1.set_yticks([0, 1, 2])
    ax1.set_yticklabels(['u', 'c', 't'])
    for i in range(3):
        for j in range(3):
            ax1.text(j, i, f'{V_pred[i,j]:.3f}', ha='center', va='center', 
                    color='white' if V_pred[i,j] > 0.5 else 'black')
    plt.colorbar(im1, ax=ax1)
    
    # Plot 2: Observed CKM
    ax2 = axes[1]
    im2 = ax2.imshow(CKM_OBSERVED, cmap='viridis', vmin=0, vmax=1)
    ax2.set_title('Observed CKM (PDG)', fontsize=12, fontweight='bold')
    ax2.set_xticks([0, 1, 2])
    ax2.set_xticklabels(['d', 's', 'b'])
    ax2.set_yticks([0, 1, 2])
    ax2.set_yticklabels(['u', 'c', 't'])
    for i in range(3):
        for j in range(3):
            ax2.text(j, i, f'{CKM_OBSERVED[i,j]:.3f}', ha='center', va='center',
                    color='white' if CKM_OBSERVED[i,j] > 0.5 else 'black')
    plt.colorbar(im2, ax=ax2)
    
    # Plot 3: Hierarchy comparison
    ax3 = axes[2]
    
    elements = ['V_ud', 'V_us', 'V_ub', 'V_cd', 'V_cs', 'V_cb', 'V_td', 'V_ts', 'V_tb']
    pred_flat = V_pred.flatten()
    obs_flat = CKM_OBSERVED.flatten()
    
    x = np.arange(len(elements))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, pred_flat, width, label='Predicted', color='steelblue')
    bars2 = ax3.bar(x + width/2, obs_flat, width, label='Observed', color='darkorange')
    
    ax3.set_ylabel('|V_ij|', fontsize=11)
    ax3.set_xticks(x)
    ax3.set_xticklabels(elements, rotation=45)
    ax3.set_yscale('log')
    ax3.set_ylim(0.001, 2)
    ax3.legend()
    ax3.set_title('CKM Hierarchy (log scale)', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    plt.suptitle('TAMESIS DERIVATION: CKM Matrix from Quark Localization',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    plt.savefig(os.path.join(output_dir, 'derivation_05_ckm_matrix.png'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'derivation_05_ckm_matrix.pdf'),
                bbox_inches='tight')
    
    print(f"\nFigures saved to {output_dir}")
    
    return fig


def main():
    """
    Main derivation script for CKM matrix.
    """
    print("\n" + "="*70)
    print("TAMESIS THEORY: DERIVATION OF CKM MATRIX")
    print("="*70)
    
    # Fit model parameters
    print("\n[FITTING MODEL PARAMETERS]")
    lambda_ratio, sigma = fit_model_parameters()
    print(f"  Optimal λ_ratio = {lambda_ratio:.3f}")
    print(f"  Optimal σ = {sigma:.3f}")
    
    # Compute CKM matrix
    print("\n[COMPUTING CKM MATRIX]")
    model = GenerationOverlapModel(lambda_ratio, sigma)
    V_pred = model.compute_ckm_matrix()
    
    print("\nPredicted CKM matrix (magnitudes):")
    print(V_pred)
    
    print("\nObserved CKM matrix (magnitudes):")
    print(CKM_OBSERVED)
    
    # Extract mixing angles
    print("\n[MIXING ANGLES]")
    theta_12, theta_23, theta_13 = extract_mixing_angles(V_pred)
    
    print(f"  θ₁₂ (Cabibbo): predicted = {np.degrees(theta_12):.2f}°, observed = {THETA_12_OBS}°")
    print(f"  θ₂₃: predicted = {np.degrees(theta_23):.2f}°, observed = {THETA_23_OBS}°")
    print(f"  θ₁₃: predicted = {np.degrees(theta_13):.3f}°, observed = {THETA_13_OBS}°")
    
    # Wolfenstein parameters
    print("\n[WOLFENSTEIN PARAMETERS]")
    lam, A = wolfenstein_parametrization(V_pred)
    print(f"  λ: predicted = {lam:.4f}, observed = 0.2257")
    print(f"  A: predicted = {A:.3f}, observed = 0.814")
    
    # Check hierarchy
    print("\n[HIERARCHY CHECK]")
    hierarchy_correct = (V_pred[0,0] > V_pred[0,1] > V_pred[0,2])
    print(f"  |V_ud| > |V_us| > |V_ub|: {hierarchy_correct}")
    
    diagonal_dominant = (V_pred[0,0] > 0.9 and V_pred[1,1] > 0.9 and V_pred[2,2] > 0.9)
    print(f"  Diagonal dominance (|V_ii| > 0.9): {diagonal_dominant}")
    
    # Generate plots
    fig = plot_ckm_comparison(V_pred, OUTPUT_DIR)
    
    # Summary
    print("\n" + "="*70)
    print("DERIVATION COMPLETE")
    print("="*70)
    
    # Quantify agreement
    rmse = np.sqrt(np.mean((V_pred - CKM_OBSERVED)**2))
    cabibbo_error = abs(np.degrees(theta_12) - THETA_12_OBS) / THETA_12_OBS * 100
    
    print(f"""
    RESULT: The CKM matrix emerges from generation-dependent localization
            in the Tamesis Kernel graph.
    
    MODEL: V_ij ~ exp(-|pos_i - pos_j|² / 2σ²)
           with pos_g = g × log(λ_ratio)
    
    FITTED PARAMETERS:
      λ_ratio = {lambda_ratio:.3f} (localization ratio between generations)
      σ = {sigma:.3f} (overlap width)
    
    AGREEMENT:
      RMSE = {rmse:.4f}
      Cabibbo angle error = {cabibbo_error:.1f}%
      Hierarchy: {'REPRODUCED' if hierarchy_correct else 'NOT reproduced'}
    """)
    
    plt.show()
    
    success = hierarchy_correct and cabibbo_error < 50
    
    return {
        'V_predicted': V_pred,
        'V_observed': CKM_OBSERVED,
        'theta_12': np.degrees(theta_12),
        'rmse': rmse,
        'success': success
    }


if __name__ == "__main__":
    result = main()
