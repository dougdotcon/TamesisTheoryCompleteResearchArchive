#!/usr/bin/env python3
"""
INDEPENDENT adversarial re-implementation (referee agent, not the original
implementer). Written from the LOCKED pre-registration spec alone, WITHOUT
reading analysis/reproduce_phi.py.

Goal: build the ABC network exactly as specified in PREREGISTRATION.md
Section 1, compute Phi via pyphi.compute.sia(subsystem).phi, and report
the number plus the MIP/cut, plus config/version provenance, plus the
secondary FG check.
"""

import sys
import json

# --- Python 3.10+ / PyPhi 1.2.0 compatibility shim -------------------------
# PyPhi 1.2.0 imports `collections.Iterable` / `collections.Mapping` at
# module scope in pyphi/db.py, pyphi/models/cmp.py, pyphi/registry.py.
# These names were literal aliases for collections.abc.Iterable /
# collections.abc.Mapping (same object) until removed from the top-level
# `collections` namespace in Python 3.10. Restoring them as aliases to the
# abc versions is therefore bit-identical to pre-3.10 behavior, not a
# reimplementation.
import collections
import collections.abc as _abc
for _name in ("Iterable", "Mapping", "Callable", "Sequence", "MutableMapping", "Set", "MutableSet"):
    if not hasattr(collections, _name) and hasattr(_abc, _name):
        setattr(collections, _name, getattr(_abc, _name))

try:
    import pyphi
except Exception as e:
    print("FATAL: import pyphi failed even after shim:", repr(e))
    sys.exit(1)

import numpy as np

report = {}

report["pyphi_version"] = pyphi.__version__
report["python_version"] = sys.version

# --- Config snapshot (task 4) ----------------------------------------------
cfg = pyphi.config
config_snapshot = {
    "MEASURE": cfg.MEASURE,
    "PARTITION_TYPE": cfg.PARTITION_TYPE,
    "SYSTEM_CUTS": cfg.SYSTEM_CUTS,
    "CUT_ONE_APPROXIMATION": cfg.CUT_ONE_APPROXIMATION,
    "PICK_SMALLEST_PURVIEW": cfg.PICK_SMALLEST_PURVIEW,
    "ASSUME_CUTS_CANNOT_CREATE_NEW_CONCEPTS": cfg.ASSUME_CUTS_CANNOT_CREATE_NEW_CONCEPTS,
    "USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE": cfg.USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE,
    "SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI": cfg.SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI,
    "PRECISION": cfg.PRECISION,
    "VALIDATE_CONDITIONAL_INDEPENDENCE": cfg.VALIDATE_CONDITIONAL_INDEPENDENCE,
    "VALIDATE_SUBSYSTEM_STATES": cfg.VALIDATE_SUBSYSTEM_STATES,
    "CACHING_BACKEND": cfg.CACHING_BACKEND,
    "CACHE_SIAS": cfg.CACHE_SIAS,
    "WELCOME_OFF": cfg.WELCOME_OFF,
}
report["config_snapshot"] = config_snapshot

# Check for any pyphi_config.yml / PYPHI_* env vars that could have changed defaults
import os
env_pyphi_vars = {k: v for k, v in os.environ.items() if k.startswith("PYPHI")}
report["env_pyphi_vars"] = env_pyphi_vars
report["cwd_has_pyphi_config_yml"] = os.path.exists("pyphi_config.yml")

# --- Build network exactly per PREREGISTRATION.md Section 1 ----------------
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

network = pyphi.Network(tpm, cm=cm, node_labels=("A", "B", "C"))
state = (1, 0, 0)
subsystem = pyphi.Subsystem(network, state, network.node_indices)

report["network_tpm_input"] = tpm.tolist()
report["network_cm_input"] = cm.tolist()
report["state"] = list(state)

# --- Cross-check against bundled fig4 example (independent sanity check) ---
try:
    bundled = pyphi.examples.fig4()
    tpm_match = bool(np.array_equal(np.asarray(bundled.tpm), np.asarray(network.tpm)))
    cm_match = bool(np.array_equal(np.asarray(bundled.cm), np.asarray(network.cm)))
    report["bundled_fig4_tpm_matches"] = tpm_match
    report["bundled_fig4_cm_matches"] = cm_match
except Exception as e:
    report["bundled_fig4_check_error"] = repr(e)

# --- Primary computation -----------------------------------------------
sia = pyphi.compute.sia(subsystem)
phi = sia.phi

target = 1.916665
diff = abs(phi - target)
tol = 1e-4

report["phi_computed"] = phi
report["phi_target"] = target
report["abs_diff"] = diff
report["tolerance"] = tol
report["within_tolerance"] = diff < tol
report["phi_rounded_2dp"] = round(phi, 2)

cut = sia.cut
report["cut_repr"] = repr(cut)
try:
    from_labels = tuple(network.node_labels.indices2labels(cut.from_nodes))
    to_labels = tuple(network.node_labels.indices2labels(cut.to_nodes))
except Exception as e:
    report["label_lookup_error"] = repr(e)
    from_labels = cut.from_nodes
    to_labels = cut.to_nodes
report["cut_from_nodes"] = list(cut.from_nodes)
report["cut_to_nodes"] = list(cut.to_nodes)
report["cut_from_labels"] = list(from_labels)
report["cut_to_labels"] = list(to_labels)
mip_matches = (set(from_labels) == {"A", "B"} and set(to_labels) == {"C"})
report["mip_matches_ab_to_c"] = mip_matches

report["sia_time"] = sia.time
try:
    report["ces_time"] = sia.ces.time
except Exception:
    pass
try:
    report["num_concepts_unpartitioned"] = len(sia.ces)
except Exception:
    pass

# --- Secondary/optional FG check (task 6) -----------------------------
try:
    net16 = pyphi.examples.fig16()
    state16 = (1, 0, 0, 1, 1, 1, 0)  # sourced from readthedocs 2014paper.html example, fetched independently
    labels16 = net16.node_labels
    f_idx = labels16.index("F")
    g_idx = labels16.index("G")
    sub_fg = pyphi.Subsystem(net16, state16, (f_idx, g_idx))
    sia_fg = pyphi.compute.sia(sub_fg)
    report["fg_phi"] = sia_fg.phi
    report["fg_target"] = 0.069445
    report["fg_abs_diff"] = abs(sia_fg.phi - 0.069445)
    report["fg_cut_repr"] = repr(sia_fg.cut)
except Exception as e:
    report["fg_error"] = repr(e)

print(json.dumps(report, indent=2, default=str))

with open("referee_phi_results.json", "w") as f:
    json.dump(report, f, indent=2, default=str)
