"""Sensitivity summary for the 1e-15 kg Tamesis candidate."""

from __future__ import annotations

from config import reject_runtime_overrides

import json
from pathlib import Path

from analyze_target_1e15 import analyze
from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


def run(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_sensitivity.json")
    analysis = analyze(data_path("target_1e15_analysis.json"))
    contract = McModel().contract

    sensitivity = {
        "protocol_id": analysis["protocol_id"],
        "config_hash": analysis["config_hash"],
        "target_mass_kg": analysis["target"]["mass_kg"],
        "target_superposition_m": analysis["target"]["separation_m"],
        "target_time_s": analysis["target"]["observation_time_s"],
        "tamesis_visibility_0p1s": analysis["tamesis"]["visibility_at_0p1s"],
        "gradient_fluctuation_tolerance_for_99pct_contrast": {
            "linear": 1e-7,
            "nonlinear": 1e-7,
            "legacy_nonlinear_only": 1e-9,
        },
        "initial_position_tolerance_m_for_99pct_contrast": {
            "with_IHP": 1e-9,
            "without_IHP": 1e-11,
        },
        "pressure_requirements_pa": analysis["pressure_requirements"],
        "dominant_remaining_unknowns": [
            "chip-specific magnetic noise to visibility mapping",
            "blackbody decoherence from the actual nanodiamond and substrate",
            "rotational dynamics and libration coupling",
        ],
        "decision_rule": [
            "If the measured contrast budget cannot sustain gradient stability at the 1e-7 level, the target is not yet clean enough for a strong Tamesis test.",
            "If pressure is above the 1e-12 to 1e-10 Pa band, gas decoherence can swamp the intrinsic Tamesis effect.",
        ],
    }

    output_path.write_text(json.dumps(sensitivity, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=contract,
            script="target_1e15_sensitivity.py",
            inputs=[str(data_path("target_1e15_analysis.json"))],
            arguments={},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return sensitivity


def main() -> None:
    reject_runtime_overrides()
    data = run()
    print(json.dumps({
        "tamesis_visibility_0p1s": data["tamesis_visibility_0p1s"],
        "gradient_tolerance": data["gradient_fluctuation_tolerance_for_99pct_contrast"],
        "position_tolerance": data["initial_position_tolerance_m_for_99pct_contrast"],
    }, indent=2))


if __name__ == "__main__":
    main()
