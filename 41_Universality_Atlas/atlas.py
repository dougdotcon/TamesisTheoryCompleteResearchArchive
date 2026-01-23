"""
Stage 41: Universality Atlas
=============================

COMPLETE MAP OF TRANSITION UNIVERSALITY CLASSES

DISCOVERED CLASSES
------------------
U_{1/2} (alpha = 0.5): Discrete-to-random transitions
U_2 (alpha = 2.0): Lindblad decoherence
U_0 (alpha ~ 0): Threshold transitions
U_exp (exponential): Poisson processes

GOAL
----
Create a complete classification of transition universality classes
based on:
1. Mathematical structure
2. Physical mechanism  
3. Observable type
4. State space geometry
"""

import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional


class StateSpaceType(Enum):
    DISCRETE = "Discrete (finite n)"
    CONTINUOUS = "Continuous"
    MIXED = "Mixed"
    QUANTUM = "Hilbert space"


class PerturbationType(Enum):
    BERNOULLI = "Bernoulli(c/n) per element"
    POISSON = "Poisson(c) total"
    GAUSSIAN = "Gaussian noise"
    LINDBLAD = "Lindblad master equation"
    THRESHOLD = "Threshold crossing"


class ObservableType(Enum):
    COUNTING = "Fraction of states"
    PURITY = "Quantum purity"
    COHERENCE = "Off-diagonal coherence"
    SPANNING = "Spanning cluster"
    LYAPUNOV = "Lyapunov exponent"


@dataclass
class UniversalityClass:
    """Definition of a universality class."""
    name: str
    exponent: float
    exponent_error: Optional[float]
    state_space: StateSpaceType
    perturbation: PerturbationType
    observable: ObservableType
    examples: List[str]
    source: str
    formula: str


class UniversalityAtlas:
    """
    Complete atlas of transition universality classes.
    """
    
    def __init__(self):
        self.classes: List[UniversalityClass] = []
        self._populate()
    
    def _populate(self):
        """Populate with discovered classes."""
        
        # U_{1/2} - The primary discovery
        self.classes.append(UniversalityClass(
            name="U_{1/2}",
            exponent=0.5,
            exponent_error=0.03,
            state_space=StateSpaceType.DISCRETE,
            perturbation=PerturbationType.BERNOULLI,
            observable=ObservableType.COUNTING,
            examples=[
                "Permutation -> Random map (Stage 34)",
                "Cycle fraction decay"
            ],
            source="Stage 34-37: Tamesis Theory",
            formula="phi(c) = (1 + c)^{-1/2}"
        ))
        
        # U_2 - Lindblad class
        self.classes.append(UniversalityClass(
            name="U_2",
            exponent=2.0,
            exponent_error=0.1,
            state_space=StateSpaceType.QUANTUM,
            perturbation=PerturbationType.LINDBLAD,
            observable=ObservableType.PURITY,
            examples=[
                "Quantum dephasing (T2)",
                "GUE level repulsion",
                "Quadratic noise"
            ],
            source="Lindblad 1976, Dyson 1962",
            formula="phi(c) = (1 + c)^{-2} or P(s) ~ s^2"
        ))
        
        # U_0 - Threshold class
        self.classes.append(UniversalityClass(
            name="U_0",
            exponent=0.0,
            exponent_error=0.05,
            state_space=StateSpaceType.MIXED,
            perturbation=PerturbationType.THRESHOLD,
            observable=ObservableType.SPANNING,
            examples=[
                "KAM chaos threshold",
                "Percolation transition",
                "Anderson localization",
                "Glass transition"
            ],
            source="KAM 1954, Stauffer 1994",
            formula="phi(c) ~ Theta(c_c - c)"
        ))
        
        # U_exp - Exponential class
        self.classes.append(UniversalityClass(
            name="U_exp",
            exponent=float('inf'),  # exponential, not power law
            exponent_error=None,
            state_space=StateSpaceType.CONTINUOUS,
            perturbation=PerturbationType.POISSON,
            observable=ObservableType.COUNTING,
            examples=[
                "Radioactive decay",
                "Poisson process survival",
                "Markov chain mixing"
            ],
            source="Classical",
            formula="phi(c) = exp(-lambda*c)"
        ))
        
        # Ising class
        self.classes.append(UniversalityClass(
            name="U_{Ising}",
            exponent=0.125,  # beta = 1/8 for 2D Ising
            exponent_error=0.0,
            state_space=StateSpaceType.DISCRETE,
            perturbation=PerturbationType.GAUSSIAN,  # thermal
            observable=ObservableType.COUNTING,  # magnetization
            examples=[
                "2D Ising ferromagnet",
                "Order-disorder transitions"
            ],
            source="Onsager 1944",
            formula="M ~ |T - T_c|^{1/8}"
        ))
    
    def summary_table(self) -> str:
        """Generate summary table."""
        lines = [
            "=" * 80,
            "UNIVERSALITY ATLAS: COMPLETE CLASSIFICATION",
            "=" * 80,
            "",
            f"{'Class':<12} {'alpha':<10} {'State Space':<20} {'Observable':<15}",
            "-" * 80
        ]
        
        for uc in self.classes:
            alpha_str = f"{uc.exponent:.3f}" if uc.exponent != float('inf') else "exp"
            lines.append(
                f"{uc.name:<12} {alpha_str:<10} {uc.state_space.value:<20} {uc.observable.value:<15}"
            )
        
        return "\n".join(lines)
    
    def classification_guide(self) -> str:
        """Generate classification decision tree."""
        return """
CLASSIFICATION GUIDE
====================

To classify a transition, ask:

1. Is the STATE SPACE discrete (finite n)?
   - YES: Continue to Q2
   - NO (continuous): Likely U_2 or U_exp

2. Is the PERTURBATION Bernoulli(c/n) per element?
   - YES: Continue to Q3
   - NO (Poisson/Gaussian): Different class

3. Is the OBSERVABLE counting-based (fraction of states)?
   - YES: Likely U_{1/2}
   - NO (threshold): Likely U_0

DECISION TREE:
--------------

           Is state space discrete?
                 /        \\
              YES          NO
               |            |
    Is perturbation     Is it Lindblad?
    Bernoulli(c/n)?     /          \\
       /     \\        YES          NO
     YES      NO       |            |
      |       |      U_2         U_exp
   Is observable
   counting-based?
     /     \\
   YES      NO
    |       |
  U_{1/2}  U_0
"""
    
    def phase_diagram_concept(self) -> str:
        """Conceptual phase diagram."""
        return """
PHASE DIAGRAM OF UNIVERSALITY CLASSES
======================================

        Observable
           ^
           |
  Counting |  U_{1/2}  |  U_0
           |  (discrete)|  (threshold)
           |------------|----------------
  Purity   |  U_2       |  U_exp
           |  (Lindblad)|  (Poisson)
           |
           +-------------------------> State Space
                Discrete    Continuous
                
Each quadrant has its own universality class.
The exponent encodes the MECHANISM, not just the system.
"""


def generate_atlas():
    """Generate the complete universality atlas."""
    
    atlas = UniversalityAtlas()
    
    print(atlas.summary_table())
    print()
    print(atlas.classification_guide())
    print()
    print(atlas.phase_diagram_concept())
    
    print("\n" + "=" * 80)
    print("DETAILED CLASS DESCRIPTIONS")
    print("=" * 80)
    
    for uc in atlas.classes:
        print(f"\n--- {uc.name} ---")
        print(f"Formula: {uc.formula}")
        print(f"Source: {uc.source}")
        print(f"Examples:")
        for ex in uc.examples:
            print(f"  - {ex}")
    
    print("\n" + "=" * 80)
    print("KEY INSIGHT")
    print("=" * 80)
    print("""
    UNIVERSALITY IS ABOUT MECHANISMS, NOT SYSTEMS
    
    The same exponent appears in seemingly different systems
    because they share the same MATHEMATICAL MECHANISM:
    
    - U_{1/2}: Discrete counting with random perturbation
    - U_2: Quadratic decay in continuous spaces
    - U_0: Threshold crossing with sharp boundary
    - U_exp: Independent Poisson events
    
    The Tamesis discovery (U_{1/2}) is a NEW member of this
    classification, describing a specific family of
    discrete-to-random transitions.
""")
    
    print("=" * 80)
    print("END OF UNIVERSALITY ATLAS")
    print("=" * 80)
    
    return atlas


if __name__ == "__main__":
    atlas = generate_atlas()
