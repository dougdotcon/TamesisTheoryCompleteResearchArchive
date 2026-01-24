"""
Stage 53: Formal Definition of Transition
==========================================

A transition is NOT:
- An interpolation between regimes
- A continuous limit
- A parameter variation

A transition IS:
- A controlled breaking of invariants
- A map E_ij: R_i -> R_j with structure

This is the foundation of TDTR.

Author: TDTR Research Program
Date: 2026-01-23
"""

import sys
sys.path.insert(0, '../43_Regime_Definition')
sys.path.insert(0, '../44_Regime_Invariants')

from dataclasses import dataclass, field
from typing import List, Set, Optional, Callable
from enum import Enum, auto


# =============================================================================
# TRANSITION TYPE
# =============================================================================

class TransitionType(Enum):
    """Classification of transition mechanisms."""
    
    DECOHERENCE = auto()       # Quantum -> Classical (U_2)
    RANDOMIZATION = auto()     # Ordered -> Random (U_1/2)
    THRESHOLD = auto()         # Parameter crosses critical value (U_0)
    SYMMETRY_BREAK = auto()    # Symmetry lost (Ising-like)
    COARSE_GRAIN = auto()      # Fine -> Effective
    EMERGENCE = auto()         # Micro -> Macro


# =============================================================================
# INVARIANT CHANGE
# =============================================================================

@dataclass
class InvariantChange:
    """Describes how an invariant changes during transition."""
    
    invariant_name: str
    source_value: any
    target_value: any
    is_broken: bool  # True if invariant is lost/changed
    
    def describe(self) -> str:
        if self.is_broken:
            return f"{self.invariant_name}: {self.source_value} -> {self.target_value} [BROKEN]"
        else:
            return f"{self.invariant_name}: {self.source_value} -> {self.target_value} [preserved]"


# =============================================================================
# TRANSITION DEFINITION
# =============================================================================

@dataclass
class Transition:
    """
    A transition E_ij: R_i -> R_j between regimes.
    
    Key properties:
    - Source and target regimes
    - Which invariants break
    - Which monotones exist
    - Whether it's reversible (spoiler: fundamental ones never are)
    """
    
    name: str
    source_regime: str            # R_i
    target_regime: str            # R_j
    transition_type: TransitionType
    
    # Invariant changes
    invariant_changes: List[InvariantChange] = field(default_factory=list)
    
    # Monotones (quantities that only increase or decrease)
    monotones: List[str] = field(default_factory=list)
    
    # Metadata
    is_reversible: bool = False
    universality_class: Optional[str] = None
    critical_exponent: Optional[float] = None
    description: str = ""
    
    def broken_invariants(self) -> List[str]:
        """Return list of broken invariants."""
        return [ic.invariant_name for ic in self.invariant_changes if ic.is_broken]
    
    def preserved_invariants(self) -> List[str]:
        """Return list of preserved invariants."""
        return [ic.invariant_name for ic in self.invariant_changes if not ic.is_broken]
    
    def signature(self) -> str:
        """Return transition signature."""
        return f"{self.source_regime} --[{self.transition_type.name}]--> {self.target_regime}"


# =============================================================================
# TRANSITION VS NON-TRANSITION
# =============================================================================

def is_true_transition(source: str, target: str, mechanism: str) -> bool:
    """
    Check if a proposed change is a TRUE transition (TDTR sense).
    
    A true transition is NOT:
    - Parameter variation within a regime
    - Continuous interpolation
    - Adiabatic limit
    
    A true transition IS:
    - Discrete change in at least one invariant
    - Non-invertible
    - Has associated monotone
    """
    
    # In a full implementation, this would check invariant structures
    # For now, we define by example
    
    true_transitions = {
        ("Quantum", "Classical"): True,        # Decoherence is true
        ("Ordered", "Random"): True,           # Randomization is true
        ("Integrable", "Chaotic"): True,       # KAM is true
        ("Ferromagnetic", "Paramagnetic"): True,  # Ising is true
    }
    
    not_transitions = {
        ("QFT_weak", "QFT_strong"): False,    # Same regime, different coupling
        ("GR_flat", "GR_curved"): False,      # Same regime, different solution
        ("T=0", "T=1"): False,                # Parameter change
    }
    
    return true_transitions.get((source, target), 
                                 not not_transitions.get((source, target), True))


# =============================================================================
# FUNDAMENTAL TRANSITIONS CATALOG
# =============================================================================

FUNDAMENTAL_TRANSITIONS = [
    
    Transition(
        name="Decoherence",
        source_regime="Quantum (Hilbert)",
        target_regime="Classical (Phase Space)",
        transition_type=TransitionType.DECOHERENCE,
        invariant_changes=[
            InvariantChange("quantumness", True, False, True),
            InvariantChange("commutativity", False, True, True),
            InvariantChange("superposition", True, False, True),
            InvariantChange("locality", True, True, False),
        ],
        monotones=["von Neumann entropy", "purity loss"],
        is_reversible=False,
        universality_class="U_2",
        critical_exponent=2.0,
        description="Quantum to classical via environment coupling"
    ),
    
    Transition(
        name="Randomization",
        source_regime="Ordered (Identity)",
        target_regime="Random (Permutation)",
        transition_type=TransitionType.RANDOMIZATION,
        invariant_changes=[
            InvariantChange("structure", "ordered", "disordered", True),
            InvariantChange("cycle_count", "n", "expected", True),
            InvariantChange("discreteness", True, True, False),
        ],
        monotones=["cycle entropy", "disorder parameter"],
        is_reversible=False,
        universality_class="U_1/2",
        critical_exponent=0.5,
        description="Order to randomness via perturbation"
    ),
    
    Transition(
        name="KAM Breakdown",
        source_regime="Integrable (Tori)",
        target_regime="Chaotic (Stochastic)",
        transition_type=TransitionType.THRESHOLD,
        invariant_changes=[
            InvariantChange("integrability", True, False, True),
            InvariantChange("KAM_tori", "present", "absent", True),
            InvariantChange("phase_space", "foliated", "mixed", True),
        ],
        monotones=["Lyapunov exponent"],
        is_reversible=False,
        universality_class="U_0",
        critical_exponent=0.0,
        description="Sharp transition to chaos"
    ),
    
    Transition(
        name="Ising Transition",
        source_regime="Ferromagnetic",
        target_regime="Paramagnetic",
        transition_type=TransitionType.SYMMETRY_BREAK,
        invariant_changes=[
            InvariantChange("magnetization", "nonzero", "zero", True),
            InvariantChange("symmetry", "broken", "restored", True),
            InvariantChange("correlation_length", "finite", "divergent", True),
        ],
        monotones=["free energy"],
        is_reversible=True,  # This one is special - equilibrium reversible
        universality_class="U_Ising",
        critical_exponent=0.125,
        description="Thermal phase transition"
    ),
    
    Transition(
        name="Spectral to Geometric",
        source_regime="QFT (Fock)",
        target_regime="GR (Riemannian)",
        transition_type=TransitionType.COARSE_GRAIN,
        invariant_changes=[
            InvariantChange("quantumness", True, False, True),
            InvariantChange("state_space", "Fock", "Riemannian", True),
            InvariantChange("observables", "spectral", "curvature", True),
            InvariantChange("background", "fixed", "dynamical", True),
        ],
        monotones=["geometric entropy"],
        is_reversible=False,
        universality_class=None,  # Key focus of TDTR Phase IV
        description="The central mystery - how does geometry emerge?"
    ),
]


# =============================================================================
# WHAT IS A TRANSITION? (THE PAPER)
# =============================================================================

def what_is_a_transition():
    """Output for the short paper."""
    
    print("=" * 70)
    print("WHAT IS A PHYSICAL TRANSITION?")
    print("Stage 53 of TDTR")
    print("=" * 70)
    
    print("""
    DEFINITION:
    
    A transition E_ij: R_i -> R_j is a map between regimes where:
    
    1. At least one invariant BREAKS (changes value or is lost)
    
    2. At least one MONOTONE exists (quantity that only increases/decreases)
    
    3. The process is IRREVERSIBLE at the fundamental level
       (equilibrium reversibility is phenomenological, not fundamental)
    
    WHAT A TRANSITION IS NOT:
    
    1. NOT an interpolation:
       There is no continuous path R_i -> R_j in regime space.
       The transition is a JUMP, not a walk.
    
    2. NOT a limit:
       R_j is not "R_i as some parameter -> infinity".
       The target regime has genuinely different structure.
    
    3. NOT a parameter variation:
       Changing coupling in QFT is not a transition.
       Changing geometry in GR is not a transition.
       A transition changes the TYPE of physics, not just values.
    
    THE KEY INSIGHT:
    
    Transitions are where INVARIANTS BREAK.
    
    This is why physics cannot be unified:
    - Regimes are defined by invariants
    - Transitions break invariants
    - You cannot preserve what must break
    
    Transitions are the EDGES of the physics graph.
    They are more fundamental than the nodes (regimes).
    """)


def display_fundamental_transitions():
    """Display the catalog of fundamental transitions."""
    
    print("\n" + "=" * 70)
    print("CATALOG OF FUNDAMENTAL TRANSITIONS")
    print("=" * 70)
    
    for t in FUNDAMENTAL_TRANSITIONS:
        print(f"\n{t.signature()}")
        print(f"  Type: {t.transition_type.name}")
        print(f"  Class: {t.universality_class} (alpha = {t.critical_exponent})")
        print(f"  Broken invariants: {t.broken_invariants()}")
        print(f"  Monotones: {t.monotones}")
        print(f"  Reversible: {t.is_reversible}")


def key_distinction():
    """The key distinction of TDTR."""
    
    print("\n" + "=" * 70)
    print("THE KEY DISTINCTION")
    print("=" * 70)
    print("""
    TRI asks:  "Why can't regimes be unified?"
    TDTR asks: "What are the laws governing transitions?"
    
    TRI sees NODES as fundamental.
    TDTR sees EDGES as fundamental.
    
    The edge E_ij is not derivable from R_i or R_j alone.
    The transition has its own structure, its own laws.
    
    THIS IS THE NEW FOUNDATION:
    
    Physics is not about states.
    Physics is about what happens BETWEEN states.
    """)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    
    what_is_a_transition()
    display_fundamental_transitions()
    key_distinction()
    
    print("\n" + "=" * 70)
    print("STAGE 53 COMPLETE")
    print("=" * 70)
    print("""
    ESTABLISHED:
    
    1. Formal definition of transition as E_ij: R_i -> R_j
    
    2. Key properties: invariant breaking, monotones, irreversibility
    
    3. Catalog of 5 fundamental transitions
    
    4. Distinction: transitions != limits, != interpolations
    
    NEXT: Stage 54 - Transition Space (which transitions are allowed?)
    """)
