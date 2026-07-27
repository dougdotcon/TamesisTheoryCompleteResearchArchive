from __future__ import annotations

import json
from pathlib import Path

from .contract_bridge import tamesis_integration
from .graph import COLORS, input_files
from .loader import load_transitions
from .provenance import OUTPUTS, write_sidecar


STATUS_ORDER = ["metaphorical", "conjectured", "mathematically_specified", "computationally_reproduced", "phenomenologically_constrained", "preregistered_test", "observational_anomaly", "transition_detected", "independently_replicated", "established_regime_boundary"]


def main() -> None:
    import matplotlib.pyplot as plt
    OUTPUTS.mkdir(exist_ok=True)
    transitions = load_transitions()
    names = list(transitions)

    fig, ax = plt.subplots(figsize=(11, 6))
    for i, (name, transition) in enumerate(transitions.items()):
        ax.scatter([i], [STATUS_ORDER.index(transition.epistemic_status.value) if transition.epistemic_status.value in STATUS_ORDER else 0], s=180, color=COLORS.get(transition.epistemic_status.value, "#6b7280"))
        ax.text(i, 0.2, name, rotation=35, ha="right", fontsize=8)
    ax.set_xticks([]); ax.set_ylabel("epistemic level (registry ordinal)"); ax.set_title("Atlas evidence map — ordinal status, not a physical metric")
    path = OUTPUTS / "atlas_evidence_status_map.png"; fig.savefig(path, dpi=180, bbox_inches="tight"); plt.close(fig); write_sidecar(path, input_files(), kind="evidence_status_map")

    counts = {}
    for transition in transitions.values(): counts[transition.epistemic_status.value] = counts.get(transition.epistemic_status.value, 0) + 1
    fig, ax = plt.subplots(figsize=(10, 5)); ax.bar(list(counts), list(counts.values()), color=[COLORS.get(k, "#6b7280") for k in counts]); ax.set_ylabel("transitions"); ax.set_title("Atlas transitions by epistemic status"); ax.tick_params(axis="x", rotation=35)
    path = OUTPUTS / "atlas_status_histogram.png"; fig.savefig(path, dpi=180, bbox_inches="tight"); plt.close(fig); write_sidecar(path, input_files(), kind="status_histogram")

    integration = tamesis_integration()
    fig, ax = plt.subplots(figsize=(12, 6)); ax.axis("off")
    lines = ["Tamesis quantum → classical candidate", f"status: preregistered_test", f"protocol: {integration['protocol_id']}", f"config hash: {integration['config_hash']}", f"M_c: {integration['Mc_kg']:.12e} kg", f"tau_c: {integration['tau_c_s']:.12g} s", "promotion: multiple masses + nuisance control + rival rejection + independent replication", "limitations: separation, geometry, composition, multipartícula"]
    ax.text(0.02, 0.95, "\n".join(lines), va="top", family="monospace", fontsize=11); ax.set_title("Atlas edge card — registry metadata, not a discovery claim")
    path = OUTPUTS / "tamesis_edge_card.png"; fig.savefig(path, dpi=180, bbox_inches="tight"); plt.close(fig); write_sidecar(path, input_files(), kind="tamesis_edge_card")

    fig, ax = plt.subplots(figsize=(11, 5));
    for i, (name, transition) in enumerate(transitions.items()):
        level = STATUS_ORDER.index(transition.epistemic_status.value) if transition.epistemic_status.value in STATUS_ORDER else 0
        ax.plot([0, level], [i, i], color=COLORS.get(transition.epistemic_status.value, "#6b7280"), linewidth=3)
        ax.scatter([level], [i], color=COLORS.get(transition.epistemic_status.value, "#6b7280"), s=100)
        ax.text(-0.1, i, name, ha="right", va="center", fontsize=8)
    ax.set_xlim(-len(STATUS_ORDER) * 0.05, len(STATUS_ORDER)); ax.set_yticks([]); ax.set_xlabel("registry status ordinal; not elapsed time"); ax.set_title("Epistemic promotion history (current snapshots)")
    path = OUTPUTS / "epistemic_promotion_timeline.png"; fig.savefig(path, dpi=180, bbox_inches="tight"); plt.close(fig); write_sidecar(path, input_files(), kind="promotion_timeline")
    print(json.dumps({"figures": 4, "outputs": str(OUTPUTS)}, indent=2))


if __name__ == "__main__":
    main()
