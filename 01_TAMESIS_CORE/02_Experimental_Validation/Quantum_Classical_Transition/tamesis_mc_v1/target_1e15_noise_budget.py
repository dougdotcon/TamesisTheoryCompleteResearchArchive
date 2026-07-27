"""Normalized noise budget for the 1e-15 kg target.

The goal is to translate the extracted tolerances into a first-pass visibility
budget. This is a triage layer, not a final chip-specific decoherence theory.
"""

from __future__ import annotations

from config import reject_runtime_overrides

import json
from dataclasses import dataclass, asdict
from math import exp, log
from pathlib import Path

from analyze_target_1e15 import analyze
from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


@dataclass(frozen=True)
class NoiseChannel:
    name: str
    tolerance: float
    reference_visibility: float
    time_s: float
    scaling_exponent: float = 2.0

    @property
    def reference_rate(self) -> float:
        return -log(self.reference_visibility) / self.time_s

    def rate_for_fraction(self, fraction_of_tolerance: float) -> float:
        return self.reference_rate * (fraction_of_tolerance ** self.scaling_exponent)

    def visibility_for_fraction(self, fraction_of_tolerance: float, time_s: float | None = None) -> float:
        t = self.time_s if time_s is None else time_s
        return exp(-self.rate_for_fraction(fraction_of_tolerance) * t)


def run(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_noise_budget.json")
    analysis = analyze(data_path("target_1e15_analysis.json"))
    contract = McModel().contract

    target_time = analysis["target"]["observation_time_s"]

    magnetic = NoiseChannel(
        name="magnetic_gradient",
        tolerance=1e-7,
        reference_visibility=0.99,
        time_s=target_time,
    )
    position = NoiseChannel(
        name="initial_position",
        tolerance=1e-9,
        reference_visibility=0.99,
        time_s=target_time,
    )

    scenarios = []
    for label, f_mag, f_pos in [
        ("best_case", 0.1, 0.1),
        ("at_tolerance", 1.0, 1.0),
        ("ten_x_worse", 10.0, 10.0),
    ]:
        gamma_mag = magnetic.rate_for_fraction(f_mag)
        gamma_pos = position.rate_for_fraction(f_pos)
        combined_rate = gamma_mag + gamma_pos
        scenarios.append(
            {
                "label": label,
                "fraction_of_magnetic_tolerance": f_mag,
                "fraction_of_position_tolerance": f_pos,
                "magnetic_rate_s-1": gamma_mag,
                "position_rate_s-1": gamma_pos,
                "combined_noise_rate_s-1": combined_rate,
                "combined_visibility_at_target_time": exp(-combined_rate * target_time),
                "combined_visibility_at_1s": exp(-combined_rate * 1.0),
            }
        )

    budget = {
        "protocol_id": analysis["protocol_id"],
        "config_hash": analysis["config_hash"],
        "target": analysis["target"],
        "tamesis": analysis["tamesis"],
        "channels": {
            "magnetic_gradient": {**asdict(magnetic), "reference_rate_s-1": magnetic.reference_rate},
            "initial_position": {**asdict(position), "reference_rate_s-1": position.reference_rate},
        },
        "scenarios": scenarios,
        "interpretation": [
            "The reference visibility 0.99 at the extracted tolerance is a normalized budget anchor.",
            "This does not replace a chip-specific simulation; it turns the paper's tolerances into a measurable first-pass nuisance scale.",
            "If the real experiment operates around the tolerance boundary, the nuisance channels can easily compete with Tamesis at 0.1 s.",
        ],
    }

    output_path.write_text(json.dumps(budget, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=contract,
            script="target_1e15_noise_budget.py",
            inputs=[str(data_path("target_1e15_analysis.json"))],
            arguments={},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return budget


def main() -> None:
    reject_runtime_overrides()
    data = run()
    print(json.dumps({
        "reference_rate_magnetic_s-1": data["channels"]["magnetic_gradient"]["reference_rate_s-1"],
        "reference_rate_position_s-1": data["channels"]["initial_position"]["reference_rate_s-1"],
        "scenarios": data["scenarios"],
    }, indent=2))


if __name__ == "__main__":
    main()
