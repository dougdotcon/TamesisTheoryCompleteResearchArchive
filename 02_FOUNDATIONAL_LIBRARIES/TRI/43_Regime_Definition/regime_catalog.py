"""
Stage 43: Regime Catalog
========================

Complete catalog of known physical regimes mapped to R = (S, P, O) triples.

This creates the "world map" of physics, showing that each fundamental
theory occupies a distinct point in regime space.

Author: TRI Research Program
Date: 2026-01-23
"""

from regime_formalism import (
    Regime, StateSpaceType, PerturbationType, ObservableType,
    RegimeInvariants, check_compatibility
)


# =============================================================================
# COMPLETE REGIME CATALOG
# =============================================================================

REGIME_CATALOG = {
    
    # -------------------------------------------------------------------------
    # DISCRETE REGIMES
    # -------------------------------------------------------------------------
    
    "U_1/2 (Computational)": Regime(
        name="U_1/2 (Computational)",
        state_space=StateSpaceType.PERMUTATION,
        perturbation=PerturbationType.BERNOULLI,
        observable=ObservableType.COUNTING,
        universality_class="U_1/2",
        critical_exponent=0.5,
        description="Discrete-to-random transitions with cycle counting"
    ),
    
    "Ising Model": Regime(
        name="Ising Model",
        state_space=StateSpaceType.LATTICE,
        perturbation=PerturbationType.THRESHOLD,
        observable=ObservableType.BINARY,
        universality_class="U_Ising",
        critical_exponent=0.125,  # beta for 2D Ising
        description="Spin lattice with temperature-driven phase transition"
    ),
    
    "Percolation": Regime(
        name="Percolation",
        state_space=StateSpaceType.LATTICE,
        perturbation=PerturbationType.BERNOULLI,
        observable=ObservableType.TOPOLOGICAL,
        universality_class="U_perc",
        critical_exponent=0.139,  # beta for 2D percolation
        description="Random graph connectivity with sharp threshold"
    ),
    
    # -------------------------------------------------------------------------
    # CONTINUOUS CLASSICAL REGIMES
    # -------------------------------------------------------------------------
    
    "Classical Mechanics": Regime(
        name="Classical Mechanics",
        state_space=StateSpaceType.PHASE_SPACE,
        perturbation=PerturbationType.GAUSSIAN,
        observable=ObservableType.GEODESIC,
        description="Hamiltonian dynamics on symplectic manifold"
    ),
    
    "Classical Chaos (KAM)": Regime(
        name="Classical Chaos (KAM)",
        state_space=StateSpaceType.PHASE_SPACE,
        perturbation=PerturbationType.THRESHOLD,
        observable=ObservableType.LYAPUNOV,
        universality_class="U_0",
        critical_exponent=0.0,
        description="Transition to chaos at KAM threshold"
    ),
    
    "Thermodynamics": Regime(
        name="Thermodynamics",
        state_space=StateSpaceType.PHASE_SPACE,
        perturbation=PerturbationType.GAUSSIAN,
        observable=ObservableType.ENSEMBLE,
        universality_class="U_exp",
        description="Statistical mechanics with exponential distributions"
    ),
    
    "General Relativity": Regime(
        name="General Relativity",
        state_space=StateSpaceType.RIEMANNIAN,
        perturbation=PerturbationType.METRIC,
        observable=ObservableType.CURVATURE,
        description="Spacetime geometry with metric dynamics"
    ),
    
    # -------------------------------------------------------------------------
    # QUANTUM REGIMES
    # -------------------------------------------------------------------------
    
    "Quantum Mechanics": Regime(
        name="Quantum Mechanics",
        state_space=StateSpaceType.HILBERT,
        perturbation=PerturbationType.GAUSSIAN,
        observable=ObservableType.SPECTRAL,
        description="Unitary evolution on Hilbert space"
    ),
    
    "Quantum Decoherence": Regime(
        name="Quantum Decoherence",
        state_space=StateSpaceType.DENSITY_MATRIX,
        perturbation=PerturbationType.LINDBLAD,
        observable=ObservableType.SPECTRAL,
        universality_class="U_2",
        critical_exponent=2.0,
        description="Open quantum system with environment coupling"
    ),
    
    "Quantum Field Theory": Regime(
        name="Quantum Field Theory",
        state_space=StateSpaceType.FOCK,
        perturbation=PerturbationType.FIELD,
        observable=ObservableType.CORRELATION,
        universality_class="U_2",
        description="Vacuum fluctuations and particle creation"
    ),
    
    # -------------------------------------------------------------------------
    # HYBRID / BOUNDARY REGIMES
    # -------------------------------------------------------------------------
    
    "MOND": Regime(
        name="MOND",
        state_space=StateSpaceType.PHASE_SPACE,
        perturbation=PerturbationType.THRESHOLD,
        observable=ObservableType.GEODESIC,
        universality_class="U_0",
        description="Transition at acceleration threshold a_0"
    ),
    
    "Quantum-Classical Boundary": Regime(
        name="Quantum-Classical Boundary",
        state_space=StateSpaceType.HYBRID,
        perturbation=PerturbationType.LINDBLAD,
        observable=ObservableType.ENTROPY,
        description="Decoherence-driven emergence of classicality"
    ),
}


def generate_catalog_table():
    """Generate formatted table of all regimes."""
    
    print("=" * 100)
    print("COMPLETE REGIME CATALOG")
    print("Theory of Regime Incompatibility (TRI)")
    print("=" * 100)
    
    # Header
    print(f"\n{'Regime':<30} {'S (State)':<20} {'P (Perturb)':<15} {'O (Observable)':<15} {'U_alpha':<10}")
    print("-" * 100)
    
    for name, regime in REGIME_CATALOG.items():
        u_class = regime.universality_class if regime.universality_class else "-"
        print(f"{name:<30} {regime.state_space.name:<20} {regime.perturbation.name:<15} {regime.observable.name:<15} {u_class:<10}")
    
    return REGIME_CATALOG


def analyze_regime_distribution():
    """Analyze how regimes distribute across state space types."""
    
    print("\n" + "=" * 70)
    print("REGIME DISTRIBUTION ANALYSIS")
    print("-" * 70)
    
    # Count by state space type
    ss_counts = {}
    for regime in REGIME_CATALOG.values():
        ss = regime.state_space.name
        ss_counts[ss] = ss_counts.get(ss, 0) + 1
    
    print("\nBy State Space Type:")
    for ss, count in sorted(ss_counts.items(), key=lambda x: -x[1]):
        print(f"  {ss}: {count}")
    
    # Count by universality class
    u_counts = {}
    for regime in REGIME_CATALOG.values():
        u = regime.universality_class if regime.universality_class else "unclassified"
        u_counts[u] = u_counts.get(u, 0) + 1
    
    print("\nBy Universality Class:")
    for u, count in sorted(u_counts.items(), key=lambda x: -x[1]):
        print(f"  {u}: {count}")


def find_incompatibilities():
    """Find all incompatible regime pairs."""
    
    print("\n" + "=" * 70)
    print("INCOMPATIBILITY MAP")
    print("-" * 70)
    
    regimes = list(REGIME_CATALOG.values())
    incompatible_pairs = []
    
    for i, r1 in enumerate(regimes):
        for r2 in regimes[i+1:]:
            result = check_compatibility(r1, r2)
            if not result["compatible"]:
                incompatible_pairs.append((r1.name, r2.name, result["conflicts"]))
    
    print(f"\nTotal incompatible pairs: {len(incompatible_pairs)}")
    print("\nSample incompatibilities:")
    
    for r1, r2, conflicts in incompatible_pairs[:10]:
        print(f"\n  {r1} vs {r2}:")
        for c in conflicts:
            print(f"    - {c}")
    
    return incompatible_pairs


def key_insight():
    """Print the key insight from regime analysis."""
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: NO COMMON CENTER")
    print("=" * 70)
    print("""
    The regime catalog shows that:
    
    1. Each fundamental theory (GR, QFT, Thermo, etc.) occupies a
       DISTINCT point in (S, P, O) space.
    
    2. No single (S, P, O) triple covers all of physics.
    
    3. Transitions BETWEEN regimes have their own universality classes.
    
    CONCLUSION:
    
    There is no "center" of physics.
    There is no regime R* such that all others reduce to R*.
    
    This is the foundation for TRI's no-go theorems.
    """)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    
    generate_catalog_table()
    analyze_regime_distribution()
    find_incompatibilities()
    key_insight()
