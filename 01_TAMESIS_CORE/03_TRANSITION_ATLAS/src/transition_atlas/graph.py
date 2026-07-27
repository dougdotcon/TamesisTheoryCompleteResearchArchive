from __future__ import annotations

import json
from pathlib import Path

from .loader import load_regimes, load_transitions, snapshot
from .provenance import OUTPUTS, REGISTRY, stable_hash, write_sidecar


COLORS = {
    "metaphorical": "#9ca3af", "conjectured": "#f59e0b", "mathematically_specified": "#60a5fa",
    "computationally_reproduced": "#38bdf8", "phenomenologically_constrained": "#22c55e",
    "preregistered_test": "#a78bfa", "observational_anomaly": "#fb7185", "transition_detected": "#16a34a",
    "independently_replicated": "#15803d", "established_regime_boundary": "#14532d", "falsified": "#dc2626", "superseded": "#6b7280",
}


def input_files() -> list[Path]:
    return sorted(list((REGISTRY / "regimes").glob("*.yaml")) + list((REGISTRY / "transitions").glob("*.yaml")) + list((REGISTRY / "protocols").glob("*.yaml")))


def build_graph() -> dict:
    regimes = load_regimes()
    transitions = load_transitions()
    graph = {"atlas_version": "0.1", "regimes": sorted(regimes), "edges": [{"id": t.transition_id, "source": t.source_regime, "target": t.target_regime, "type": t.transition_type.value, "status": t.epistemic_status.value, "claim_classification": t.claim_classification} for t in transitions.values()]}
    graph["graph_hash"] = stable_hash(graph)
    OUTPUTS.mkdir(exist_ok=True)
    json_path = OUTPUTS / "atlas_graph.json"
    dot_path = OUTPUTS / "atlas_graph.dot"
    json_path.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["digraph Atlas {", "  rankdir=LR;"]
    for regime_id in regimes:
        lines.append(f'  "{regime_id}";')
    for edge in graph["edges"]:
        lines.append(f'  "{edge["source"]}" -> "{edge["target"]}" [label="{edge["id"]}\\n{edge["status"]}"];')
    lines.append("}")
    dot_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_sidecar(json_path, input_files(), kind="graph_data")
    write_sidecar(dot_path, input_files(), kind="graph_dot")
    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(13, 7))
        positions = {name: (i % 3, -(i // 3)) for i, name in enumerate(sorted(regimes))}
        for edge in graph["edges"]:
            x1, y1 = positions[edge["source"]]; x2, y2 = positions[edge["target"]]
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "color": COLORS.get(edge["status"], "#6b7280"), "lw": 2})
            ax.text((x1+x2)/2, (y1+y2)/2, edge["id"], fontsize=7)
        for name, (x, y) in positions.items():
            ax.scatter([x], [y], s=1400, color="#e5e7eb", edgecolor="#111827")
            ax.text(x, y, name, ha="center", va="center", fontsize=8, wrap=True)
        ax.set_title("Transition Atlas v0.1 — topology is not evidence")
        ax.axis("off")
        png = OUTPUTS / "atlas_graph.png"
        fig.savefig(png, dpi=180, bbox_inches="tight")
        plt.close(fig)
        write_sidecar(png, [json_path, dot_path], kind="graph_visualization")
    except ImportError:
        pass
    return graph
