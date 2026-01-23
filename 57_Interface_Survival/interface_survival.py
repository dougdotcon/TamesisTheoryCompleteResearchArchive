"""
Stage 57: What Survives a Transition?
=====================================

Interface quantities: not from R_i, not from R_j, but from the crossing.

Author: TDTR Research Program
Date: 2026-01-23
"""


# =============================================================================
# INTERFACE QUANTITIES
# =============================================================================

def what_survives():
    """What survives the crossing between regimes?"""
    
    print("=" * 70)
    print("STAGE 57: WHAT SURVIVES A TRANSITION?")
    print("=" * 70)
    
    print("""
    THE PROBLEM:
    
    In a transition E_ij: R_i -> R_j:
    - Invariants of R_i are lost (some of them)
    - Invariants of R_j don't exist yet in R_i
    
    Question: What quantities exist AT THE INTERFACE?
    
    INTERFACE QUANTITIES:
    
    These are NOT properties of R_i or R_j alone.
    They are properties of the TRANSITION ITSELF.
    
    Candidates:
    
    1. COARSE-GRAINED ENTROPY
       - Not the fine-grained entropy of R_i
       - Not the equilibrium entropy of R_j
       - The entropy OF THE COARSE-GRAINING PROCESS
    
    2. CAUSAL ORDER
       - Which events can influence which
       - Survives if R_i and R_j both have causal structure
       - Defines what "before" and "after" mean during transition
    
    3. EFFECTIVE DIMENSION
       - Number of degrees of freedom that matter
       - Can change (reduce) during transition
       - But always well-defined AT the interface
    
    4. MONOTONE VALUE
       - The value of the transition monotone M
       - Defined throughout the transition
       - Gives "progress" through the crossing
    
    5. INFORMATION CONTENT (RESIDUAL)
       - What information survives erasure
       - The "coarse" information, not the "fine"
    """)


def interface_vs_regime():
    """Distinguish interface quantities from regime quantities."""
    
    print("\n" + "=" * 70)
    print("INTERFACE vs REGIME QUANTITIES")
    print("-" * 50)
    
    print("""
    REGIME QUANTITIES (R_i or R_j specific):
    
    - Wavefunction psi (quantum only)
    - Metric tensor g (Riemannian only)
    - Permutation sigma (discrete only)
    - Temperature T (equilibrium only)
    
    These DON'T SURVIVE the transition.
    They are DESTROYED and REPLACED.
    
    INTERFACE QUANTITIES (transition-specific):
    
    - Coarse-grained entropy S_cg
    - Effective dimension d_eff
    - Causal ordering <
    - Monotone value M
    
    These EXIST DURING the transition.
    They connect R_i to R_j.
    
    KEY INSIGHT:
    
    Interface quantities are what allow us to COMPARE
    states before and after transition.
    
    Without them, R_i and R_j would be INCOMMENSURABLE.
    """)


def examples_of_survival():
    """Examples of what survives each transition type."""
    
    print("\n" + "=" * 70)
    print("EXAMPLES: WHAT SURVIVES EACH TRANSITION")
    print("-" * 50)
    
    examples = [
        {
            "transition": "Quantum -> Classical (Decoherence)",
            "lost": ["superposition", "phase coherence", "entanglement"],
            "survives": ["coarse energy", "classical correlations", "causal order"],
            "monotone": "von Neumann entropy"
        },
        {
            "transition": "Ordered -> Random (Perturbation)",
            "lost": ["exact structure", "determinism"],
            "survives": ["statistical properties", "cycle statistics (in expectation)"],
            "monotone": "disorder parameter"
        },
        {
            "transition": "Integrable -> Chaotic (KAM)",
            "lost": ["KAM tori", "action-angle variables", "integrability"],
            "survives": ["energy (if Hamiltonian)", "phase space volume"],
            "monotone": "Lyapunov exponent"
        },
        {
            "transition": "Micro -> Macro (Coarse-graining)",
            "lost": ["microscopic detail", "individual particle positions"],
            "survives": ["thermodynamic quantities", "conservation laws (coarse)"],
            "monotone": "coarse-grained entropy"
        },
    ]
    
    for ex in examples:
        print(f"\n  {ex['transition']}:")
        print(f"    Lost: {ex['lost']}")
        print(f"    Survives: {ex['survives']}")
        print(f"    Monotone: {ex['monotone']}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    
    what_survives()
    interface_vs_regime()
    examples_of_survival()
    
    print("\n" + "=" * 70)
    print("STAGE 57 COMPLETE")
    print("=" * 70)
