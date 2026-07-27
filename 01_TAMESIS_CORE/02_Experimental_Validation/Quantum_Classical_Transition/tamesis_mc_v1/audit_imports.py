from __future__ import annotations

import ast
import json
from pathlib import Path

from config import load_v1_contract, reject_runtime_overrides
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path


BASE = Path(__file__).resolve().parent
ENTRYPOINTS = [
    "validate_environment.py", "validate_contract.py", "resolve_contract.py", "run_predictions.py", "compare_models.py",
    "prioritize_targets.py", "analyze_target_1e15.py", "target_1e15_noise_budget.py", "target_1e15_sensitivity.py",
    "target_1e15_decision.py", "target_1e15_thermal_gate.py", "generate_figures.py", "build_manifest.py", "verify_artifacts.py",
]


def local_module(name: str) -> Path | None:
    candidate = BASE / (name.replace(".", "/") + ".py")
    return candidate if candidate.exists() else None


def imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.append(node.module)
    return sorted(set(found))


def main() -> None:
    reject_runtime_overrides()
    contract = load_v1_contract()
    graph: dict[str, list[str]] = {}
    visited: set[Path] = set()
    queue = [BASE / name for name in ENTRYPOINTS]
    while queue:
        path = queue.pop()
        if path in visited or not path.exists():
            continue
        visited.add(path)
        local = []
        for name in imports(path):
            module = local_module(name)
            if module:
                local.append(module.relative_to(BASE).as_posix())
                queue.append(module)
        graph[path.relative_to(BASE).as_posix()] = local
    legacy_edges = [(source, target) for source, targets in graph.items() for target in targets if "legacy" in target.lower() or "90_" in target]
    output = data_path("active_import_graph.json")
    payload = {"protocol_id": contract.protocol_id(), "config_hash": contract.config_hash(), "entrypoints": ENTRYPOINTS, "graph": graph, "legacy_edges": legacy_edges, "legacy_edges_count": len(legacy_edges)}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(output, provenance_record(output_path=output, contract=contract, script="audit_imports.py", inputs=ENTRYPOINTS))
    print(json.dumps({"visited_modules": len(graph), "legacy_edges": legacy_edges}, indent=2))


if __name__ == "__main__":
    main()
