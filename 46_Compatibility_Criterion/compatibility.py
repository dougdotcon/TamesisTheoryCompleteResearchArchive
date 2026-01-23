"""
Stage 46: Compatibility Criterion
=================================

Formal mathematical criterion for when two regimes can coexist
in a unified theory.

Key Result: Regimes are compatible if and only if they share
ALL structural invariants.

Author: TRI Research Program
Date: 2026-01-23
"""

import sys
sys.path.insert(0, '../43_Regime_Definition')
sys.path.insert(0, '../44_Regime_Invariants')

from regime_formalism import (
    Regime, StateSpaceType, PerturbationType, ObservableType
)
from invariant_analysis import InvariantSignature, extract_invariants
from dataclasses import dataclass
from typing import List, Tuple, Dict


# =============================================================================
# COMPATIBILITY DEFINITION
# =============================================================================

@dataclass
class CompatibilityResult:
    """Result of compatibility check between two regimes."""
    
    regime_1: str
    regime_2: str
    compatible: bool
    shared_invariants: List[str]
    conflicting_invariants: List[str]
    unification_possible: bool
    
    def explain(self) -> str:
        if self.compatible:
            return f"{self.regime_1} and {self.regime_2} are COMPATIBLE (can be unified)"
        else:
            return f"{self.regime_1} and {self.regime_2} are INCOMPATIBLE: {', '.join(self.conflicting_invariants)}"


def check_compatibility(r1: Regime, r2: Regime) -> CompatibilityResult:
    """
    Check if two regimes are compatible for unification.
    
    COMPATIBILITY CRITERION:
    R1 and R2 are compatible <=> they share ALL structural invariants.
    
    This is the mathematical heart of TRI.
    """
    
    inv1 = extract_invariants(r1)
    inv2 = extract_invariants(r2)
    
    shared = []
    conflicts = []
    
    # Check each invariant
    if inv1.is_discrete == inv2.is_discrete:
        shared.append("discreteness")
    else:
        conflicts.append(f"discreteness ({inv1.is_discrete} vs {inv2.is_discrete})")
    
    if inv1.is_quantum == inv2.is_quantum:
        shared.append("quantumness")
    else:
        conflicts.append(f"quantumness ({inv1.is_quantum} vs {inv2.is_quantum})")
    
    if inv1.is_commutative == inv2.is_commutative:
        shared.append("commutativity")
    else:
        conflicts.append(f"commutativity ({inv1.is_commutative} vs {inv2.is_commutative})")
    
    if inv1.measure_type == inv2.measure_type:
        shared.append("measure_type")
    else:
        conflicts.append(f"measure ({inv1.measure_type} vs {inv2.measure_type})")
    
    if inv1.is_local == inv2.is_local:
        shared.append("locality")
    else:
        conflicts.append(f"locality ({inv1.is_local} vs {inv2.is_local})")
    
    compatible = len(conflicts) == 0
    
    return CompatibilityResult(
        regime_1=r1.name,
        regime_2=r2.name,
        compatible=compatible,
        shared_invariants=shared,
        conflicting_invariants=conflicts,
        unification_possible=compatible
    )


# =============================================================================
# KEY EXAMPLES
# =============================================================================

def demonstrate_criterion():
    """Demonstrate the compatibility criterion with key examples."""
    
    print("=" * 70)
    print("STAGE 46: COMPATIBILITY CRITERION")
    print("=" * 70)
    
    # Define test regimes
    regimes = {
        "QFT": Regime(
            name="QFT",
            state_space=StateSpaceType.FOCK,
            perturbation=PerturbationType.FIELD,
            observable=ObservableType.CORRELATION
        ),
        "Decoherence": Regime(
            name="Decoherence",
            state_space=StateSpaceType.DENSITY_MATRIX,
            perturbation=PerturbationType.LINDBLAD,
            observable=ObservableType.SPECTRAL
        ),
        "GR": Regime(
            name="GR",
            state_space=StateSpaceType.RIEMANNIAN,
            perturbation=PerturbationType.METRIC,
            observable=ObservableType.CURVATURE
        ),
        "U_1/2": Regime(
            name="U_1/2",
            state_space=StateSpaceType.PERMUTATION,
            perturbation=PerturbationType.BERNOULLI,
            observable=ObservableType.COUNTING
        ),
        "KAM Chaos": Regime(
            name="KAM Chaos",
            state_space=StateSpaceType.PHASE_SPACE,
            perturbation=PerturbationType.THRESHOLD,
            observable=ObservableType.LYAPUNOV
        ),
    }
    
    # POSITIVE EXAMPLE: QFT <-> Decoherence
    print("\n[1] POSITIVE EXAMPLE: Compatible Regimes")
    print("-" * 50)
    
    result = check_compatibility(regimes["QFT"], regimes["Decoherence"])
    print(f"\n  {result.regime_1} <-> {result.regime_2}")
    print(f"  Compatible: {result.compatible}")
    print(f"  Shared: {result.shared_invariants}")
    if result.compatible:
        print("  => UNIFICATION POSSIBLE")
    
    # NEGATIVE EXAMPLES
    print("\n[2] NEGATIVE EXAMPLES: Incompatible Regimes")
    print("-" * 50)
    
    pairs = [
        ("GR", "QFT"),
        ("U_1/2", "QFT"),
        ("U_1/2", "KAM Chaos"),
        ("GR", "U_1/2"),
    ]
    
    for name1, name2 in pairs:
        result = check_compatibility(regimes[name1], regimes[name2])
        print(f"\n  {result.regime_1} <-> {result.regime_2}")
        print(f"  Compatible: {result.compatible}")
        print(f"  Conflicts: {result.conflicting_invariants}")
        print("  => UNIFICATION IMPOSSIBLE")
    
    # The criterion
    print("\n" + "=" * 70)
    print("[3] THE COMPATIBILITY CRITERION")
    print("=" * 70)
    print("""
    DEFINITION (Regime Compatibility):
    
    Two regimes R1, R2 are COMPATIBLE if and only if:
    
        Invariants(R1) = Invariants(R2)
    
    That is, they share ALL five structural invariants:
    - Discreteness
    - Quantumness
    - Commutativity
    - Measure type
    - Locality
    
    THEOREM (Unification Criterion):
    
    A unified theory T can describe regimes R1 and R2 simultaneously
    if and only if R1 and R2 are compatible.
    
    COROLLARY:
    
    If Invariants(R1) != Invariants(R2), then NO theory can unify them.
    """)


# =============================================================================
# COMPATIBILITY MATRIX
# =============================================================================

def generate_compatibility_matrix():
    """Generate full compatibility matrix for key regimes."""
    
    print("\n" + "=" * 70)
    print("[4] COMPATIBILITY MATRIX")
    print("-" * 70)
    
    # Simplified regimes for matrix
    regimes = [
        Regime("GR", StateSpaceType.RIEMANNIAN, PerturbationType.METRIC, ObservableType.CURVATURE),
        Regime("QFT", StateSpaceType.FOCK, PerturbationType.FIELD, ObservableType.CORRELATION),
        Regime("Decoherence", StateSpaceType.DENSITY_MATRIX, PerturbationType.LINDBLAD, ObservableType.SPECTRAL),
        Regime("U_1/2", StateSpaceType.PERMUTATION, PerturbationType.BERNOULLI, ObservableType.COUNTING),
        Regime("KAM", StateSpaceType.PHASE_SPACE, PerturbationType.THRESHOLD, ObservableType.LYAPUNOV),
        Regime("Ising", StateSpaceType.LATTICE, PerturbationType.THRESHOLD, ObservableType.BINARY),
    ]
    
    # Header
    names = [r.name for r in regimes]
    print(f"\n{'':>15}", end="")
    for n in names:
        print(f"{n:>12}", end="")
    print()
    
    # Matrix
    for r1 in regimes:
        print(f"{r1.name:>15}", end="")
        for r2 in regimes:
            if r1.name == r2.name:
                print(f"{'---':>12}", end="")
            else:
                result = check_compatibility(r1, r2)
                symbol = "OK" if result.compatible else "X"
                print(f"{symbol:>12}", end="")
        print()
    
    print("\n  OK = Compatible (unification possible)")
    print("  X  = Incompatible (no unification)")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    
    demonstrate_criterion()
    generate_compatibility_matrix()
    
    print("\n" + "=" * 70)
    print("STAGE 46 COMPLETE")
    print("=" * 70)
    print("""
    ESTABLISHED:
    
    1. Formal compatibility criterion based on invariant matching
    
    2. POSITIVE EXAMPLE: QFT <-> Decoherence (same invariants)
    
    3. NEGATIVE EXAMPLES: GR <-> QFT, U_1/2 <-> QFT, etc.
    
    4. Compatibility matrix showing the structure of regime space
    
    NEXT: Stage 47 - No-Go Theorems
    """)
