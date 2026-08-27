#!/usr/bin/env python3
"""
Pre-registered PyPhi Phi reproduction test.

Pre-registration (LOCKED, do not modify after this script is committed):
  05_DISCOVERY_LAB/02_TESTS/IIT_PHI_REPRODUCTION/PREREGISTRATION.md

Hypothesis under test: PyPhi, applied to the 3-node ABC network from
Figure 4 of Oizumi, Albantakis & Tononi (2014), reproduces the published
Phi = 1.916665 (cited as 1.92 in Mayner et al. 2018) for the full system
{A,B,C} in state (1,0,0), with MIP = severs causal connections {A,B} -> C.

This script performs ONLY the primary locked analysis (Sections 1, 4, 5
of the pre-registration). The optional secondary FG minor-complex check
(Section 6) is implemented separately and is NOT part of the falsification
criterion.

Environment note (documented, not a change to any IIT/PyPhi default):
PyPhi 1.2.0 (the current PyPI release as of this run; see pip show output
recorded in RESULTS_PRIMARY.md) was written for Python <= 3.9 and imports
`collections.Iterable` / `collections.Mapping` directly from the top-level
`collections` module (pyphi/db.py, pyphi/models/cmp.py, pyphi/registry.py).
These aliases were removed from `collections` in Python 3.10 (they moved
to `collections.abc` back in Python 3.3, deprecated since 3.3, removed in
3.10). This environment runs Python 3.11, so `import pyphi` raises
`ImportError: cannot import name 'Iterable' from 'collections'` unless a
compatibility shim is installed first. The shim below re-attaches the
`collections.abc` objects under their old `collections.*` names before
PyPhi is imported. This does NOT alter any IIT computation, any PyPhi
config default, or any numerical behavior -- it only restores a stdlib
name that PyPhi's own source expects to exist. It is applied identically
regardless of network/state, so it cannot bias the result one way or the
other. This is recorded transparently per pre-registration Section 3/5
(explicitly anticipates checking whether divergence traces to a
documented version/environment change).
"""

import collections
import collections.abc
import json
import sys
from pathlib import Path

for _name in ("Iterable", "Mapping", "Callable", "Sequence", "MutableMapping"):
    if not hasattr(collections, _name) and hasattr(collections.abc, _name):
        setattr(collections, _name, getattr(collections.abc, _name))

import numpy as np  # noqa: E402

import pyphi  # noqa: E402


OUT_DIR = Path(__file__).resolve().parent
RESULTS_JSON = OUT_DIR / "phi_results.json"


def _json_default(o):
    """Coerce numpy scalar types (numpy>=2 renames np.bool_ -> np.bool,
    which the stdlib json encoder does not recognize) to plain Python
    types for JSON serialization. Purely a serialization convenience;
    does not touch any computed value."""
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def dumps(obj):
    return json.dumps(obj, indent=2, default=_json_default)


def get_config_snapshot():
    """Record every documented PyPhi config value in effect for this run."""
    cfg = pyphi.config
    keys = [
        "ASSUME_CUTS_CANNOT_CREATE_NEW_CONCEPTS",
        "CACHE_POTENTIAL_PURVIEWS",
        "CACHE_REPERTOIRES",
        "CACHE_SIAS",
        "CUT_ONE_APPROXIMATION",
        "MEASURE",
        "NUMBER_OF_CORES",
        "PARALLEL_COMPLEX_EVALUATION",
        "PARALLEL_CONCEPT_EVALUATION",
        "PARALLEL_CUT_EVALUATION",
        "PARTITION_TYPE",
        "PICK_SMALLEST_PURVIEW",
        "PRECISION",
        "SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI",
        "SYSTEM_CUTS",
        "USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE",
        "VALIDATE_CONDITIONAL_INDEPENDENCE",
        "VALIDATE_SUBSYSTEM_STATES",
        "WELCOME_OFF",
    ]
    snap = {}
    for k in keys:
        v = getattr(cfg, k, "N/A")
        try:
            json.dumps(v)
            snap[k] = v
        except TypeError:
            snap[k] = str(v)
    return snap


def run_primary():
    """Section 1/4 of the pre-registration: full ABC system, state (1,0,0)."""
    # TPM/CM EXACTLY as specified in PREREGISTRATION.md Section 1.
    tpm = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ])
    cm = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ])
    state = (1, 0, 0)
    node_labels = ("A", "B", "C")

    network = pyphi.Network(tpm, cm=cm, node_labels=node_labels)
    subsystem = pyphi.Subsystem(network, state, network.node_indices)

    sia = pyphi.compute.sia(subsystem)
    phi = sia.phi

    cut = sia.cut
    partition_repr = repr(sia.partition) if hasattr(sia, "partition") else None

    from_labels = tuple(node_labels[i] for i in cut.from_nodes)
    to_labels = tuple(node_labels[i] for i in cut.to_nodes)
    # Pre-registration Section 5: MIP must sever causal connections from
    # {A,B} to C.
    mip_matches_preregistered = (
        set(from_labels) == {"A", "B"} and set(to_labels) == {"C"}
    )

    # Cross-check: compare TPM/CM against PyPhi's own bundled fig4() example
    # network (same lineage / same source group), if present in this version.
    # IMPORTANT: PyPhi internally converts a 2D state-by-node TPM into a
    # canonical multidimensional array (shape (2,2,...,2,n)); that internal
    # form is what `network.tpm` returns, NOT the flat (2**n, n) array we
    # passed to the constructor. So the correct comparison is between the
    # two constructed Network objects' internal `.tpm`/`.cm`, not between
    # our raw input array and a reshape of the bundled network's `.tpm`
    # (naively reshaping mixes up PyPhi's internal state-indexing order and
    # produces a spurious mismatch even when the networks are identical).
    fig4_match = None
    fig4_error = None
    try:
        fig4_net = pyphi.examples.fig4()
        fig4_match = bool(
            np.array_equal(np.asarray(fig4_net.tpm), np.asarray(network.tpm))
            and np.array_equal(np.asarray(fig4_net.cm), np.asarray(network.cm))
        )
    except AttributeError as e:
        fig4_error = str(e)

    result = {
        "test": "primary",
        "pyphi_version": pyphi.__version__,
        "python_version": sys.version,
        "config_snapshot": get_config_snapshot(),
        "network": {
            "tpm": tpm.tolist(),
            "cm": cm.tolist(),
            "state": list(state),
            "node_labels": list(node_labels),
            "subsystem_nodes": list(network.node_indices),
        },
        "fig4_bundled_example_available": fig4_error is None,
        "fig4_bundled_example_matches_preregistered_network": fig4_match,
        "fig4_bundled_example_error": fig4_error,
        "phi": phi,
        "phi_rounded_2dp": round(phi, 2),
        "target_phi": 1.916665,
        "tolerance": 1e-4,
        "abs_diff": abs(phi - 1.916665),
        "within_tolerance": abs(phi - 1.916665) < 1e-4,
        "cut_repr": repr(cut),
        "cut_str": str(cut),
        "cut_from_node_indices": list(cut.from_nodes),
        "cut_to_node_indices": list(cut.to_nodes),
        "cut_from_labels": list(from_labels),
        "cut_to_labels": list(to_labels),
        "mip_matches_preregistered_ab_to_c": mip_matches_preregistered,
        "partition_repr": partition_repr,
        "sia_time_seconds": sia.time,
        "small_phi_time_seconds": sia.small_phi_time,
        "sia_repr": repr(sia),
        "sia_str": str(sia),
    }
    result["verdict"] = (
        "CONFIRMED"
        if (result["within_tolerance"] and result["mip_matches_preregistered_ab_to_c"])
        else "FALSIFIED_OR_NON_REPRODUCING"
    )
    return result, sia


def run_secondary_fg_optional():
    """
    Section 6 (OPTIONAL, NOT part of the locked falsification criterion):
    FG minor-complex network from the larger Figure 16 system, target
    Phi ~= 0.069445, same source lineage. Reported separately.

    The installed PyPhi 1.2.0 examples module (`pyphi.examples.fig16`)
    provides the Figure 16 network's TPM/CM but does NOT expose a
    canonical analyzed state (no `fig16_state()` in this version). Rather
    than invent one, the state was obtained by direct fetch (per AGENTS.md
    Sec. "Proibições": no citation/value without direct-fetch verification)
    of the same documentation page already cited in the pre-registration
    Section 2 as "Confirmacao adicional":
      https://pyphi.readthedocs.io/en/latest/examples/2014paper.html
    which documents, for the Figure 16 analysis: network via
    `pyphi.examples.fig16_network()`, state = (1, 0, 0, 1, 1, 1, 0) (7
    nodes A-G, H-L omitted), FG minor complex Phi ~= 0.069445 -- matching
    the pre-registration's Section 6 target value exactly, which is itself
    an independent corroboration that the fetched state is the correct
    canonical one for this secondary check.
    """
    out = {
        "test": "secondary_fg_optional",
        "note": "NOT part of locked primary criterion (Section 6).",
        "state_source_url": "https://pyphi.readthedocs.io/en/latest/examples/2014paper.html",
        "state_used": [1, 0, 0, 1, 1, 1, 0],
    }
    try:
        fig16_net = pyphi.examples.fig16()
    except AttributeError as e:
        out["error"] = f"pyphi.examples.fig16 not available in installed version: {e}"
        return out

    out["fig16_tpm_shape"] = list(np.asarray(fig16_net.tpm).shape)
    out["fig16_cm"] = np.asarray(fig16_net.cm).tolist()
    out["fig16_node_labels"] = list(fig16_net.node_labels) if fig16_net.node_labels else None

    labels = list(fig16_net.node_labels) if fig16_net.node_labels else None
    out["attempted_fg_subsystem"] = None
    out["fg_error"] = None
    full_state = (1, 0, 0, 1, 1, 1, 0)
    try:
        if labels and "F" in labels and "G" in labels:
            f_idx = labels.index("F")
            g_idx = labels.index("G")
            fg_subsystem = pyphi.Subsystem(fig16_net, full_state, (f_idx, g_idx))
            fg_sia = pyphi.compute.sia(fg_subsystem)
            out["fg_phi"] = fg_sia.phi
            out["fg_target_phi"] = 0.069445
            out["fg_abs_diff"] = abs(fg_sia.phi - 0.069445)
            out["fg_cut_repr"] = repr(fg_sia.cut)
            out["fg_sia_str"] = str(fg_sia)
            out["attempted_fg_subsystem"] = [f_idx, g_idx]
        else:
            out["fg_error"] = (
                f"Bundled fig16() node_labels do not include both 'F' and "
                f"'G' (labels={labels}); cannot identify FG minor complex "
                f"without guessing an index mapping."
            )
    except Exception as e:  # pragma: no cover - diagnostic path
        out["fg_error"] = f"{type(e).__name__}: {e}"

    return out


def main():
    print("=" * 70)
    print("PRIMARY LOCKED TEST (pre-registration Sections 1, 4, 5)")
    print("=" * 70)
    result, sia = run_primary()
    print(dumps({k: v for k, v in result.items() if k != "config_snapshot"}))
    print()
    print("Config snapshot:")
    print(dumps(result["config_snapshot"]))
    print()
    print("Full SIA repr:")
    print(result["sia_repr"])

    print()
    print("=" * 70)
    print("OPTIONAL SECONDARY CORROBORATION (Section 6, NOT part of criterion)")
    print("=" * 70)
    secondary = run_secondary_fg_optional()
    print(dumps(secondary))

    combined = {"primary": result, "secondary_optional": secondary}

    with open(RESULTS_JSON, "w") as f:
        f.write(dumps(combined))
    print()
    print(f"Raw results written to: {RESULTS_JSON}")


if __name__ == "__main__":
    main()
