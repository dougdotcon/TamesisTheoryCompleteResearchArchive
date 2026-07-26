"""Analyze the 1e-15 kg macroscopic-superposition target."""

from __future__ import annotations

import json
from pathlib import Path
from math import exp

try:
    from .compare_models import ExperimentRecord, predict_coherence_probability
    from .environment_model import Environment, pressure_for_rate
    from .mc_model import McModel
except ImportError:
    from compare_models import ExperimentRecord, predict_coherence_probability
    from environment_model import Environment, pressure_for_rate
    from mc_model import McModel
from workspace_paths import data_path, ensure_workspace_dirs


def analyze(output_path: Path | None = None) -> dict:
    ensure_workspace_dirs()
    output_path = output_path or data_path("target_1e15_analysis.json")

    mc = McModel()
    mass = 1e-15
    separation = 50e-6
    time_s = 0.1

    record = ExperimentRecord(
        experiment="Spin-IHP 1e-15 kg 50um target",
        family="nanodiamond_chip",
        mass_kg=mass,
        separation_m=separation,
        observation_time_s=time_s,
        observed_coherence=False,
        status="planned",
        source="arXiv:2408.11909",
        source_url="https://arxiv.org/abs/2408.11909",
        notes="Abstract target: 1e-15 kg, 50 micrometers, 0.1 seconds.",
    )

    environment_scenarios = {
        "space_cryogenic_1e-15Pa": Environment(pressure_pa=1e-15, gas_temperature_k=20.0),
        "extreme_uhv_1e-12Pa": Environment(pressure_pa=1e-12, gas_temperature_k=20.0),
        "uhv_1e-10Pa": Environment(pressure_pa=1e-10, gas_temperature_k=20.0),
    }

    intrinsic_rate = mc.intrinsic_rate(mass)
    result = {
        "target": {
            "mass_kg": mass,
            "separation_m": separation,
            "observation_time_s": time_s,
            "source": "https://arxiv.org/abs/2408.11909",
            "source_basis": "arXiv abstract: 1e-15 kg, 50 micrometers, 0.1 seconds.",
        },
        "tamesis": {
            "Mc_kg": mc.mc,
            "M_over_Mc": mass / mc.mc,
            "intrinsic_rate_s-1": intrinsic_rate,
            "coherence_time_s": mc.coherence_time(mass),
            "visibility_at_0p1s": mc.visibility(mass, time_s),
            "visibility_at_1s": mc.visibility(mass, 1.0),
        },
        "comparison_models": {},
        "environment_scenarios": {},
        "pressure_requirements": {
            "gas_pressure_for_environment_equal_tamesis_rate_pa": pressure_for_rate(intrinsic_rate, mass),
            "gas_pressure_for_environment_10pct_tamesis_rate_pa": pressure_for_rate(0.1 * intrinsic_rate, mass),
        },
        "thermal_gate": {
            "blackbody_dominance_temperature_k": 4.0,
            "low_risk_temperature_k": 1.0,
            "source": "https://arxiv.org/pdf/2410.20910",
            "source_basis": "Above ~4 K, blackbody radiation becomes a considerable decoherence channel for micrometer-size superpositions in diamond.",
        },
        "interpretation": [],
    }

    for name in ["CSL", "GRW", "DP"]:
        visibility = predict_coherence_probability(name, record, mc)
        result["comparison_models"][name] = {
            "visibility_at_0p1s": visibility,
            "effective_rate_s-1": -1.0 * (0.0 if visibility <= 0 else __import__("math").log(visibility) / time_s),
        }

    for name, env in environment_scenarios.items():
        env_rate = env.total_rate(mass)
        result["environment_scenarios"][name] = {
            **env.summary(mass),
            "visibility_environment_only": env.visibility(mass, time_s),
            "visibility_tamesis_plus_environment": exp(-(intrinsic_rate + env_rate) * time_s),
        }

    result["interpretation"] = [
        "At 1e-15 kg the target is above Tamesis M_c and should show a measurable intrinsic visibility loss.",
        "Gas collisions must be kept below roughly 10 percent of the Tamesis rate for a clean first-pass test.",
        "Blackbody/radiative decoherence should be kept below the 4 K gate, ideally near 1 K or colder.",
        "The CSL number here is a naive canonical point-mass comparison; a publication-grade analysis needs extended-body CSL.",
        "The dominant missing terms are magnetic/current noise and full blackbody decoherence from the actual chip geometry.",
    ]

    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    result = analyze()
    print(json.dumps({
        "M_over_Mc": result["tamesis"]["M_over_Mc"],
        "tamesis_visibility_0p1s": result["tamesis"]["visibility_at_0p1s"],
        "pressure_10pct_rate_pa": result["pressure_requirements"]["gas_pressure_for_environment_10pct_tamesis_rate_pa"],
        "environment_scenarios": {
            key: {
                "env_rate": value["total_environment_rate_s-1"],
                "combined_visibility": value["visibility_tamesis_plus_environment"],
            }
            for key, value in result["environment_scenarios"].items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
