"""
Critical Exponents Analysis
===========================

Stage 36.2: Catalog of critical exponents in regime transitions.

HYPOTHESIS
----------
Different regimes have different critical exponents:
- U_{1/2} (alpha = 0.5): Discrete state spaces (permutation -> random map)
- U_2 (alpha = 2.0): Continuous coherence decay (quantum decoherence)  
- U_0 (alpha ~ 0): Threshold transitions (KAM chaos)

This is NOT a failure of universality - it's a CLASSIFICATION of universality classes.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class TransitionType(Enum):
    """Classification of regime transitions."""
    DISCRETE_TO_RANDOM = "Discrete -> Random"
    COHERENT_TO_DECOHERENT = "Coherent -> Decoherent"
    ORDERED_TO_CHAOTIC = "Ordered -> Chaotic"
    LOCAL_TO_GLOBAL = "Local -> Global"
    CLASSICAL_TO_QUANTUM = "Classical -> Quantum"


@dataclass
class CriticalExponent:
    """A critical exponent with context."""
    name: str
    alpha: float
    alpha_error: Optional[float]
    transition_type: TransitionType
    physical_context: str
    source: str  # Literature reference or "This work"
    

class CriticalExponentCatalog:
    """
    Catalog of critical exponents from various physical and mathematical contexts.
    """
    
    def __init__(self):
        self.exponents: List[CriticalExponent] = []
        self._populate_catalog()
    
    def _populate_catalog(self):
        """Populate with known exponents from literature and this work."""
        
        # === FROM THIS WORK (Stage 34, 36) ===
        
        self.exponents.append(CriticalExponent(
            name="U_{1/2} (Permutation -> Random Map)",
            alpha=0.5,
            alpha_error=0.0,  # Exact
            transition_type=TransitionType.DISCRETE_TO_RANDOM,
            physical_context="Cycle fraction in perturbed permutations",
            source="Stage 34: phi(c) = (1+c)^{-1/2}"
        ))
        
        self.exponents.append(CriticalExponent(
            name="Decoherence (Quantum -> Classical)",
            alpha=2.0,
            alpha_error=0.09,
            transition_type=TransitionType.COHERENT_TO_DECOHERENT,
            physical_context="Purity decay under dephasing",
            source="Stage 36.1: Lindblad dephasing"
        ))
        
        self.exponents.append(CriticalExponent(
            name="KAM (Integrable -> Chaotic)",
            alpha=0.004,
            alpha_error=0.002,
            transition_type=TransitionType.ORDERED_TO_CHAOTIC,
            physical_context="Regular phase space fraction in Standard Map",
            source="Stage 36.1: Standard map simulation"
        ))
        
        # === FROM LITERATURE ===
        
        self.exponents.append(CriticalExponent(
            name="Ising 2D Magnetization",
            alpha=0.125,  # beta = 1/8
            alpha_error=0.0,  # Exact (Onsager)
            transition_type=TransitionType.ORDERED_TO_CHAOTIC,
            physical_context="Magnetization near T_c",
            source="Onsager 1944"
        ))
        
        self.exponents.append(CriticalExponent(
            name="Percolation (2D site)",
            alpha=0.139,  # beta = 5/36
            alpha_error=0.0,  # Exact (CFT)
            transition_type=TransitionType.LOCAL_TO_GLOBAL,
            physical_context="Percolating cluster strength",
            source="Cardy 1992"
        ))
        
        self.exponents.append(CriticalExponent(
            name="Random Matrix GUE Level Repulsion",
            alpha=2.0,  # P(s) ~ s^2 as s -> 0
            alpha_error=0.0,
            transition_type=TransitionType.ORDERED_TO_CHAOTIC,
            physical_context="Level spacing distribution",
            source="Dyson 1962"
        ))
        
        self.exponents.append(CriticalExponent(
            name="Kolmogorov Turbulence",
            alpha=0.333,  # -5/3 for energy spectrum -> 1/3 for structure function
            alpha_error=0.0,
            transition_type=TransitionType.ORDERED_TO_CHAOTIC,
            physical_context="Energy cascade scaling",
            source="Kolmogorov 1941"
        ))
        
        self.exponents.append(CriticalExponent(
            name="Anderson Localization (3D)",
            alpha=1.57,  # nu for orth. class
            alpha_error=0.02,
            transition_type=TransitionType.LOCAL_TO_GLOBAL,
            physical_context="Localization length divergence",
            source="Slevin & Ohtsuki 1999"
        ))
    
    def analyze(self) -> Dict:
        """Analyze the catalog for patterns."""
        
        # Group by transition type
        by_type = {}
        for exp in self.exponents:
            t = exp.transition_type.value
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(exp)
        
        # Look for U_{1/2} appearances
        u12_matches = [e for e in self.exponents if abs(e.alpha - 0.5) < 0.1]
        
        # Look for U_2 appearances
        u2_matches = [e for e in self.exponents if abs(e.alpha - 2.0) < 0.2]
        
        return {
            'by_type': by_type,
            'u12_matches': u12_matches,
            'u2_matches': u2_matches,
            'total_exponents': len(self.exponents)
        }
    
    def print_catalog(self):
        """Print the catalog in table format."""
        print("\n" + "=" * 90)
        print("CRITICAL EXPONENT CATALOG")
        print("=" * 90)
        
        print(f"\n{'Name':<45} {'Alpha':>8} {'Type':<25}")
        print("-" * 90)
        
        for exp in self.exponents:
            err_str = f"+/-{exp.alpha_error:.3f}" if exp.alpha_error else "(exact)"
            print(f"{exp.name:<45} {exp.alpha:>8.3f} {exp.transition_type.value:<25}")
    
    def print_analysis(self):
        """Print analysis results."""
        analysis = self.analyze()
        
        print("\n" + "=" * 70)
        print("ANALYSIS: UNIVERSALITY CLASSES")
        print("=" * 70)
        
        print("\n1. GROUPING BY TRANSITION TYPE:")
        print("-" * 50)
        for t, exps in analysis['by_type'].items():
            print(f"\n   {t}:")
            for e in exps:
                print(f"      {e.name}: alpha = {e.alpha}")
        
        print("\n\n2. U_{1/2} CLASS (alpha ~ 0.5):")
        print("-" * 50)
        if analysis['u12_matches']:
            for e in analysis['u12_matches']:
                print(f"   {e.name}")
        else:
            print("   No exact matches found!")
        
        print("\n3. U_2 CLASS (alpha ~ 2.0):")
        print("-" * 50)
        for e in analysis['u2_matches']:
            print(f"   {e.name}")


def compute_theoretical_exponents():
    """
    Derive theoretical exponents from first principles.
    """
    print("\n" + "=" * 70)
    print("THEORETICAL DERIVATION OF EXPONENTS")
    print("=" * 70)
    
    print("""
    1. U_{1/2} DERIVATION (Stage 34 result)
    ----------------------------------------
    
    Random map on n elements with perturbation delta = c/n:
    - Expected number of cyclic destinations: n * (1 + c)^{-1} per component
    - Fraction of points in cycles: phi(c) = (1 + c)^{-1/2}
    
    The 1/2 comes from:
       phi ~ sqrt(n_cyclic / n_total) = sqrt((n * (1+c)^{-1}) / n) = (1+c)^{-1/2}
    
    This is a COUNTING ARGUMENT in discrete state spaces.
    
    2. U_2 DERIVATION (Decoherence)
    --------------------------------
    
    Lindblad dephasing: drho/dt = -gamma * [H,[H,rho]]
    - Off-diagonal elements: rho_{ij}(t) = rho_{ij}(0) * exp(-gamma * t)
    - Purity: P = Tr(rho^2) ~ exp(-2*gamma*t)
    
    The exponent 2 comes from:
       P ~ |rho_{off}|^2 ~ exp(-2*c)  =>  alpha = 2 when fitting to (1+c)^{-alpha}
    
    This is a LINDBLAD MASTER EQUATION result for continuous systems.
    
    3. U_0 DERIVATION (KAM)
    -----------------------
    
    Near KAM threshold:
    - Measure of chaotic region: mu ~ epsilon^{1/nu} for some large nu
    - At threshold k_c ~ 0.9716, transition is SHARP
    
    The exponent ~ 0 comes from:
       Transition is almost a step function (threshold behavior).
    
    CONCLUSION
    ==========
    
    Different exponents reflect different MICROSCOPIC MECHANISMS:
    
    | Exponent | Mechanism | State Space |
    |----------|-----------|-------------|
    | 1/2      | Counting  | Discrete    |
    | 2        | Lindblad  | Continuous  |
    | ~0       | Threshold | Phase space |
    
    U_{1/2} is UNIVERSAL for DISCRETE-to-RANDOM transitions,
    but NOT universal for ALL transitions.
""")


def main():
    """Stage 36.2: Critical exponents catalog and analysis."""
    
    print("=" * 70)
    print("STAGE 36.2: CRITICAL EXPONENTS CATALOG")
    print("=" * 70)
    
    catalog = CriticalExponentCatalog()
    catalog.print_catalog()
    catalog.print_analysis()
    
    compute_theoretical_exponents()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70)
    print("""
    U_{1/2} is NOT a universal theory of all transitions.
    
    It is a SPECIFIC universality class for transitions where:
    1. The state space is DISCRETE (finite n)
    2. The perturbation is ADDITIVE (delta = c/n)
    3. The observable is COUNTING-based (fraction of states)
    
    PHYSICAL CANDIDATES for U_{1/2}:
    - Quantum error correction thresholds
    - Neural network memorization-generalization transition
    - Genetic algorithm fitness landscape transitions
    - Market efficiency-inefficiency transitions?
    
    These all involve DISCRETE states with RANDOM perturbations.
""")
    
    print("=" * 70)
    print("END OF CRITICAL EXPONENTS ANALYSIS")
    print("=" * 70)


if __name__ == "__main__":
    main()
