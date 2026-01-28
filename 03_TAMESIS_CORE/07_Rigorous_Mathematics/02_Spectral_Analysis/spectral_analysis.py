"""
Spectral Analysis for Operators
================================

This module contains tools for analyzing the spectral properties
of operators, independent of the Riemann zeta function.

Focus:
- Eigenvalue computation
- Level spacing statistics
- Random Matrix Theory (RMT) comparisons
"""

import numpy as np
from scipy.linalg import eigh
from typing import Dict, Tuple
import sys
sys.path.append('..')

# Import the operator from Phase 1
from pathlib import Path
parent = Path(__file__).parent.parent / "01_Operator_Definition"
sys.path.insert(0, str(parent))


def compute_eigenvalues(H: np.ndarray, verify_hermitian: bool = True) -> Tuple[np.ndarray, Dict]:
    """
    Compute eigenvalues of a matrix.
    
    Parameters
    ----------
    H : np.ndarray
        The operator matrix
    verify_hermitian : bool
        If True, symmetrize the matrix first
        
    Returns
    -------
    eigenvalues : np.ndarray
        Sorted real eigenvalues
    info : Dict
        Additional information
    """
    if verify_hermitian:
        H_sym = (H + H.conj().T) / 2
        err = np.max(np.abs(H - H_sym))
    else:
        H_sym = H
        err = 0
    
    eigenvalues, eigenvectors = eigh(H_sym)
    
    return eigenvalues, {
        'hermitian_error': err,
        'n_eigenvalues': len(eigenvalues),
        'min_eigenvalue': eigenvalues[0],
        'max_eigenvalue': eigenvalues[-1]
    }


def level_spacing_distribution(eigenvalues: np.ndarray) -> Dict:
    """
    Compute the level spacing distribution.
    
    This is a key quantity in Random Matrix Theory.
    - Poisson: integrable systems (uncorrelated levels)
    - GOE/GUE: chaotic systems (level repulsion)
    """
    sorted_eig = np.sort(np.real(eigenvalues))
    spacings = np.diff(sorted_eig)
    
    # Normalize
    mean_s = np.mean(spacings)
    if mean_s > 0:
        normalized = spacings / mean_s
    else:
        normalized = spacings
    
    return {
        'raw_spacings': spacings,
        'normalized_spacings': normalized,
        'mean': mean_s,
        'variance': np.var(normalized),
        'min': np.min(spacings),
        'max': np.max(spacings)
    }


def gue_comparison(normalized_spacings: np.ndarray) -> Dict:
    """
    Compare level spacings to GUE (Gaussian Unitary Ensemble) prediction.
    
    For GUE, the level spacing distribution follows the Wigner surmise:
    P(s) = (32/π²) s² exp(-4s²/π)
    
    Key statistic: variance ≈ 0.286 for GUE
    """
    if len(normalized_spacings) < 5:
        return {'gue_compatible': None, 'message': 'Insufficient data'}
    
    observed_var = np.var(normalized_spacings)
    gue_var = 0.286  # Theoretical GUE variance
    
    ratio = observed_var / gue_var
    
    return {
        'observed_variance': observed_var,
        'gue_variance': gue_var,
        'ratio': ratio,
        'gue_compatible': 0.5 < ratio < 2.0,
        'interpretation': 'GUE-like' if 0.8 < ratio < 1.2 else 'Deviates from GUE'
    }


def main():
    """Demonstrate spectral analysis on Berry-Keating operator."""
    print("=" * 60)
    print("SPECTRAL ANALYSIS MODULE")
    print("=" * 60)
    
    # Import and create operator
    try:
        from berry_keating_operator import BerryKeatingOperator
        op = BerryKeatingOperator(n_points=150, x_min=0.1, x_max=30.0)
        H = op.symmetrize()
    except ImportError:
        # Create a test matrix if operator not available
        print("Note: Using test matrix (operator module not found)")
        n = 100
        H = np.random.randn(n, n)
        H = (H + H.T) / 2  # Symmetrize
    
    # Compute eigenvalues
    eigenvalues, info = compute_eigenvalues(H)
    print(f"\n1. Eigenvalue Computation")
    print(f"   Count: {info['n_eigenvalues']}")
    print(f"   Range: [{info['min_eigenvalue']:.4f}, {info['max_eigenvalue']:.4f}]")
    
    # Spacing statistics
    spacing = level_spacing_distribution(eigenvalues)
    print(f"\n2. Level Spacing Statistics")
    print(f"   Mean spacing: {spacing['mean']:.6f}")
    print(f"   Variance: {spacing['variance']:.6f}")
    
    # GUE comparison
    gue = gue_comparison(spacing['normalized_spacings'])
    print(f"\n3. GUE Comparison")
    print(f"   Variance ratio: {gue['ratio']:.3f}")
    print(f"   Interpretation: {gue['interpretation']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
