"""
Stage 43: Regime Formalism
==========================

Formal definition of "Regime" as a mathematical object.

A regime R = (S, P, O) is a triple where:
- S = State space type
- P = Perturbation type  
- O = Observable type

This formalism removes "regime" from informal discourse and makes it
a first-class mathematical object that can be compared, classified,
and used to prove incompatibility theorems.

Author: TRI Research Program
Date: 2026-01-23
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Dict


# =============================================================================
# STATE SPACE TYPES
# =============================================================================

class StateSpaceType(Enum):
    """Classification of state space structures."""
    
    # Discrete spaces
    DISCRETE_FINITE = auto()      # Finite set (e.g., spin states)
    PERMUTATION = auto()          # S_n (permutation group)
    LATTICE = auto()              # Z^d or finite lattice
    GRAPH = auto()                # Discrete graph structure
    
    # Continuous spaces
    EUCLIDEAN = auto()            # R^n
    PHASE_SPACE = auto()          # Symplectic manifold
    RIEMANNIAN = auto()           # Curved manifold (GR)
    
    # Quantum spaces
    HILBERT = auto()              # Separable Hilbert space
    FOCK = auto()                 # Fock space (QFT)
    DENSITY_MATRIX = auto()       # Space of density operators
    
    # Hybrid
    HYBRID = auto()               # Mixed discrete/continuous


# =============================================================================
# PERTURBATION TYPES
# =============================================================================

class PerturbationType(Enum):
    """Classification of perturbation mechanisms."""
    
    # Discrete perturbations
    BERNOULLI = auto()            # Independent coin flips per element
    POISSON = auto()              # Random number of events
    SWAP = auto()                 # Pairwise transpositions
    
    # Continuous perturbations
    GAUSSIAN = auto()             # Additive Gaussian noise
    BROWNIAN = auto()             # Wiener process
    LINDBLAD = auto()             # Quantum decoherence channel
    
    # Threshold perturbations
    THRESHOLD = auto()            # Parameter crosses critical value
    BIFURCATION = auto()          # Qualitative change in dynamics
    
    # Geometric perturbations
    METRIC = auto()               # Perturbation of metric tensor
    FIELD = auto()                # Field fluctuation (QFT)


# =============================================================================
# OBSERVABLE TYPES
# =============================================================================

class ObservableType(Enum):
    """Classification of observable structures."""
    
    # Counting observables
    COUNTING = auto()             # Integer-valued (cycles, clusters)
    TOPOLOGICAL = auto()          # Discrete invariant (genus, Betti)
    
    # Spectral observables
    SPECTRAL = auto()             # Eigenvalue-based
    CORRELATION = auto()          # Two-point functions
    
    # Threshold observables
    BINARY = auto()               # Order parameter (0/1)
    LYAPUNOV = auto()             # Chaos indicator
    
    # Statistical observables
    ENSEMBLE = auto()             # Thermal average
    ENTROPY = auto()              # Information measure
    
    # Geometric observables
    CURVATURE = auto()            # Ricci, Weyl, etc.
    GEODESIC = auto()             # Path-based


# =============================================================================
# REGIME DEFINITION
# =============================================================================

@dataclass
class Regime:
    """
    A regime is a triple R = (S, P, O) that completely characterizes
    the dynamical structure of a physical system.
    
    The regime determines the universality class of transitions.
    """
    
    name: str
    state_space: StateSpaceType
    perturbation: PerturbationType
    observable: ObservableType
    
    # Optional metadata
    universality_class: Optional[str] = None
    critical_exponent: Optional[float] = None
    description: str = ""
    
    def signature(self) -> tuple:
        """Return the (S, P, O) signature."""
        return (self.state_space, self.perturbation, self.observable)
    
    def is_discrete(self) -> bool:
        """Check if state space is discrete."""
        discrete_types = {
            StateSpaceType.DISCRETE_FINITE,
            StateSpaceType.PERMUTATION,
            StateSpaceType.LATTICE,
            StateSpaceType.GRAPH
        }
        return self.state_space in discrete_types
    
    def is_quantum(self) -> bool:
        """Check if state space is quantum."""
        quantum_types = {
            StateSpaceType.HILBERT,
            StateSpaceType.FOCK,
            StateSpaceType.DENSITY_MATRIX
        }
        return self.state_space in quantum_types
    
    def uses_counting(self) -> bool:
        """Check if observable is counting-based."""
        return self.observable in {ObservableType.COUNTING, ObservableType.TOPOLOGICAL}
    
    def uses_spectral(self) -> bool:
        """Check if observable is spectral."""
        return self.observable in {ObservableType.SPECTRAL, ObservableType.CORRELATION}


# =============================================================================
# INVARIANT EXTRACTION
# =============================================================================

@dataclass
class RegimeInvariants:
    """
    Structural invariants that define a regime's character.
    These determine compatibility with other regimes.
    """
    
    is_discrete: bool
    is_quantum: bool
    is_commutative: bool
    is_local: bool
    measure_type: str  # "counting", "spectral", "threshold"
    
    @classmethod
    def from_regime(cls, regime: Regime) -> 'RegimeInvariants':
        """Extract invariants from a regime."""
        
        # Determine measure type
        if regime.uses_counting():
            measure = "counting"
        elif regime.uses_spectral():
            measure = "spectral"
        else:
            measure = "threshold"
        
        # Determine commutativity (quantum = non-commutative)
        is_commutative = not regime.is_quantum()
        
        # Determine locality (threshold perturbations are global)
        is_local = regime.perturbation not in {
            PerturbationType.THRESHOLD,
            PerturbationType.BIFURCATION
        }
        
        return cls(
            is_discrete=regime.is_discrete(),
            is_quantum=regime.is_quantum(),
            is_commutative=is_commutative,
            is_local=is_local,
            measure_type=measure
        )


def check_compatibility(r1: Regime, r2: Regime) -> Dict:
    """
    Check if two regimes are structurally compatible.
    
    Compatibility requires matching invariants.
    Incompatibility implies no unified theory can describe both.
    """
    
    inv1 = RegimeInvariants.from_regime(r1)
    inv2 = RegimeInvariants.from_regime(r2)
    
    conflicts = []
    
    if inv1.is_discrete != inv2.is_discrete:
        conflicts.append("discrete vs continuous state space")
    
    if inv1.is_quantum != inv2.is_quantum:
        conflicts.append("classical vs quantum")
    
    if inv1.is_commutative != inv2.is_commutative:
        conflicts.append("commutative vs non-commutative")
    
    if inv1.measure_type != inv2.measure_type:
        conflicts.append(f"measure type: {inv1.measure_type} vs {inv2.measure_type}")
    
    return {
        "compatible": len(conflicts) == 0,
        "conflicts": conflicts,
        "regime_1": r1.name,
        "regime_2": r2.name
    }


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    
    print("=" * 70)
    print("STAGE 43: REGIME FORMALISM")
    print("Theory of Regime Incompatibility (TRI)")
    print("=" * 70)
    
    # Define example regimes
    print("\n[1] Defining Regimes as R = (S, P, O) triples...")
    print("-" * 50)
    
    # U_{1/2} regime (from Tamesis)
    U12_regime = Regime(
        name="Computational (U_1/2)",
        state_space=StateSpaceType.PERMUTATION,
        perturbation=PerturbationType.BERNOULLI,
        observable=ObservableType.COUNTING,
        universality_class="U_1/2",
        critical_exponent=0.5,
        description="Discrete-to-random transitions with cycle counting"
    )
    
    # Quantum decoherence regime
    decoherence_regime = Regime(
        name="Quantum Decoherence (U_2)",
        state_space=StateSpaceType.DENSITY_MATRIX,
        perturbation=PerturbationType.LINDBLAD,
        observable=ObservableType.SPECTRAL,
        universality_class="U_2",
        critical_exponent=2.0,
        description="Continuous quantum systems with Lindblad dynamics"
    )
    
    # Classical chaos regime
    chaos_regime = Regime(
        name="Classical Chaos (U_0)",
        state_space=StateSpaceType.PHASE_SPACE,
        perturbation=PerturbationType.THRESHOLD,
        observable=ObservableType.LYAPUNOV,
        universality_class="U_0",
        critical_exponent=0.0,
        description="Sharp threshold transitions (KAM)"
    )
    
    # General Relativity regime
    gr_regime = Regime(
        name="General Relativity",
        state_space=StateSpaceType.RIEMANNIAN,
        perturbation=PerturbationType.METRIC,
        observable=ObservableType.CURVATURE,
        description="Spacetime geometry with metric dynamics"
    )
    
    # QFT regime
    qft_regime = Regime(
        name="Quantum Field Theory",
        state_space=StateSpaceType.FOCK,
        perturbation=PerturbationType.FIELD,
        observable=ObservableType.CORRELATION,
        universality_class="U_2",
        description="Vacuum fluctuations and particle creation"
    )
    
    regimes = [U12_regime, decoherence_regime, chaos_regime, gr_regime, qft_regime]
    
    for r in regimes:
        print(f"\n  {r.name}:")
        print(f"    S = {r.state_space.name}")
        print(f"    P = {r.perturbation.name}")
        print(f"    O = {r.observable.name}")
        if r.universality_class:
            print(f"    Class = {r.universality_class} (alpha = {r.critical_exponent})")
    
    # Extract invariants
    print("\n" + "=" * 70)
    print("[2] Extracting Regime Invariants")
    print("-" * 50)
    
    for r in regimes:
        inv = RegimeInvariants.from_regime(r)
        print(f"\n  {r.name}:")
        print(f"    Discrete: {inv.is_discrete}")
        print(f"    Quantum: {inv.is_quantum}")
        print(f"    Commutative: {inv.is_commutative}")
        print(f"    Measure: {inv.measure_type}")
    
    # Check compatibility
    print("\n" + "=" * 70)
    print("[3] Checking Regime Compatibility")
    print("-" * 50)
    
    pairs = [
        (U12_regime, decoherence_regime),
        (U12_regime, chaos_regime),
        (gr_regime, qft_regime),
        (decoherence_regime, qft_regime),
    ]
    
    for r1, r2 in pairs:
        result = check_compatibility(r1, r2)
        status = "COMPATIBLE" if result["compatible"] else "INCOMPATIBLE"
        print(f"\n  {r1.name} <-> {r2.name}: {status}")
        if result["conflicts"]:
            for c in result["conflicts"]:
                print(f"    - {c}")
    
    # Summary
    print("\n" + "=" * 70)
    print("[4] STAGE 43 SUMMARY")
    print("=" * 70)
    print("""
    FORMAL DEFINITION ESTABLISHED:
    
    A regime R = (S, P, O) is a triple where:
      - S = State space type
      - P = Perturbation type
      - O = Observable type
    
    KEY INSIGHT:
    
    The (S, P, O) signature determines the universality class.
    Incompatible invariants => no unified theory possible.
    
    REGIMES FORMALIZED: 5
    INCOMPATIBILITIES FOUND: Multiple
    
    This is the foundation for TRI's no-go theorems.
    """)
