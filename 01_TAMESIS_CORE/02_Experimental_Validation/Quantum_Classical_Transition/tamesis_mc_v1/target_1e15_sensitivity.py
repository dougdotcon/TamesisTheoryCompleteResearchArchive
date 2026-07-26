"""Sensitivity summary for the 1e-15 kg Tamesis candidate."""

from __future__ import annotations

import json
from pathlib import Path

from analyze_target_1e15 import analyze
from workspace_paths import data_path, ensure_workspace_dirs


def run(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_sensitivity.json")
    analysis = analyze(data_path("target_1e15_analysis.json"))

    sensitivity = {
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
    return sensitivity


def main() -> None:
    data = run()
    print(json.dumps({
        "tamesis_visibility_0p1s": data["tamesis_visibility_0p1s"],
        "gradient_tolerance": data["gradient_fluctuation_tolerance_for_99pct_contrast"],
        "position_tolerance": data["initial_position_tolerance_m_for_99pct_contrast"],
    }, indent=2))


if __name__ == "__main__":
    main()
