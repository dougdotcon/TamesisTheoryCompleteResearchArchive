"""
Simulations Package for Critical Mass (M_c) Quantum Collapse Research
=====================================================================

This package implements computational models for testing the hypothesis
of a universal critical mass for quantum coherence breakdown.

Main Hypothesis:
    M_c ≈ 5.3 × 10⁻¹⁶ kg

    For M > M_c, intrinsic decoherence occurs regardless of environmental
    isolation, representing a fundamental limit to unitarity.

Modules:
--------
- constants: Physical constants and derived scales
- collapse_dynamics: Temporal dynamics of quantum collapse
- decoherence_models: Implementation of CSL, GRW, DP, and M_c models
- optomechanics: Cantilever and levitated nanoparticle simulations
- interferometry: Matter-wave interference visibility predictions

Author: Douglas H. M. Fulber
Date: January 2026
"""

from .constants import M_C, M_PLANCK, A_0, A_PLANCK, TAU_PLANCK, OMEGA

__version__ = "1.0.0"
__all__ = [
    "constants",
    "collapse_dynamics", 
    "decoherence_models",
    "optomechanics",
    "interferometry"
]
