"""Final first-pass decision matrix for the 1e-15 kg target."""

from __future__ import annotations

from config import reject_runtime_overrides

import json
from math import exp
from pathlib import Path

from analyze_target_1e15 import analyze
from target_1e15_noise_budget import run as run_noise_budget
from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


def decide(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_decision.json")

    analysis = analyze(data_path("target_1e15_analysis.json"))
    noise = run_noise_budget(data_path("target_1e15_noise_budget.json"))
    contract = McModel().contract

    tamesis_visibility = analysis["tamesis"]["visibility_at_0p1s"]
    tamesis_rate = analysis["tamesis"]["intrinsic_rate_s-1"]
    gas_scenarios = analysis["environment_scenarios"]

    decision_rows = []
    for scenario in noise["scenarios"]:
        label = scenario["label"]
        noise_rate = scenario["combined_noise_rate_s-1"]
        combined_tamesis_visibility = exp(-(tamesis_rate + noise_rate) * analysis["target"]["observation_time_s"])
        decision_rows.append(
            {
                "scenario": label,
                "tamesis_visibility_at_0p1s": tamesis_visibility,
                "normalized_noise_visibility_at_0p1s": scenario["combined_visibility_at_target_time"],
                "combined_visibility_at_0p1s": combined_tamesis_visibility,
                "combined_visibility_at_1s": exp(-(tamesis_rate + noise_rate) * 1.0),
                "dominant_condition": "Tamesis" if combined_tamesis_visibility > 0.5 else "suppressed",
            }
        )

    verdict = {
        "protocol_id": analysis["protocol_id"],
        "config_hash": analysis["config_hash"],
        "target": analysis["target"],
        "tamesis": analysis["tamesis"],
        "gas_environment": gas_scenarios,
        "normalized_noise_budget": noise,
        "decision_rows": decision_rows,
        "summary": [
            "At 1e-15 kg, Tamesis predicts a measurable intrinsic loss at 0.1 s.",
            "Best-case normalized chip noise does not erase the effect.",
            "At-tolerance chip noise competes but still leaves a visible Tamesis signature.",
            "10x worse chip noise suppresses the signature and would make the experiment non-decisive.",
            "Gas pressure above roughly 7e-13 Pa is already too noisy for a clean first-pass test.",
            "This target is therefore Bohr-level candidate territory, but only under very strong control of chip noise and vacuum.",
        ],
    }

    output_path.write_text(json.dumps(verdict, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=contract,
            script="target_1e15_decision.py",
            inputs=[str(data_path("target_1e15_analysis.json")), str(data_path("target_1e15_noise_budget.json"))],
            arguments={},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return verdict


def main() -> None:
    reject_runtime_overrides()
    data = decide()
    print(json.dumps(
        {
            "summary": data["summary"],
            "decision_rows": data["decision_rows"],
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
