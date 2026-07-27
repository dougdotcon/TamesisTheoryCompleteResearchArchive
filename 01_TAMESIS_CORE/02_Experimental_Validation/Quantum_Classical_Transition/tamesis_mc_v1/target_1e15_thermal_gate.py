"""Thermal gate for the 1e-15 kg target.

This is a conservative classification layer based on the extracted literature:
for micrometer-size superpositions in diamond, blackbody radiation becomes a
considerable or dominant decoherence channel above roughly 4 K.
"""

from __future__ import annotations

from config import reject_runtime_overrides

import json
from pathlib import Path

from analyze_target_1e15 import analyze
from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


def classify_temperature(temp_k: float) -> str:
    if temp_k <= 1.0:
        return "low_blackbody_risk"
    if temp_k <= 4.0:
        return "borderline_blackbody_risk"
    return "blackbody_dominant"


def run(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_thermal_gate.json")
    analysis = analyze(data_path("target_1e15_analysis.json"))
    contract = McModel().contract

    temperatures = [0.1, 1.0, 4.0, 10.0, 20.0]
    rows = []
    for temp in temperatures:
        rows.append(
            {
                "temperature_k": temp,
                "classification": classify_temperature(temp),
            }
        )

    gate = {
        "protocol_id": analysis["protocol_id"],
        "config_hash": analysis["config_hash"],
        "target": analysis["target"],
        "blackbody_rule": {
            "source": "https://arxiv.org/pdf/2410.20910",
            "statement": "For micrometer-size superpositions in diamond, blackbody radiation becomes a considerable decoherence channel above ~4 K.",
            "conservative_use": "Because the target superposition is ~50 um, treat 4 K as a conservative upper bound, not a design goal.",
        },
        "temperature_rows": rows,
        "interpretation": [
            "At 0.1 K and 1 K the target is in the low-risk band.",
            "At 4 K the gate is borderline.",
            "Above 4 K blackbody is dominant enough to threaten any clean Tamesis test.",
        ],
    }

    output_path.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=contract,
            script="target_1e15_thermal_gate.py",
            inputs=[str(data_path("target_1e15_analysis.json"))],
            arguments={},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return gate


def main() -> None:
    reject_runtime_overrides()
    data = run()
    print(json.dumps(data["temperature_rows"], indent=2))


if __name__ == "__main__":
    main()
