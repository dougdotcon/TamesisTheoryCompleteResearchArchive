from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
from typing import Any

from .generator import generate_observation
from .inference import infer_observation
from .protocol import BASE, config_payload, config_hash, protocol_id, scenario_grid, derive_seed
from .provenance import write_sidecar


def output_dir() -> Path:
    path = BASE / "data" / "synthetic_validation"
    path.mkdir(parents=True, exist_ok=True)
    (BASE / "reports" / "synthetic_figures").mkdir(parents=True, exist_ok=True)
    return path


def run_profile(profile: str = "quick", *, misspecification: str = "none", max_scenarios: int | None = None) -> dict[str, Any]:
    cfg = config_payload(); n_replicas = int(cfg["replicas"][profile]); master_seed = int(cfg["master_seed"])
    scenarios = scenario_grid(profile, truth_model="null") + scenario_grid(profile, truth_model="tamesis")
    if max_scenarios is not None: scenarios = scenarios[:max_scenarios]
    out = output_dir(); suffix = f"_{misspecification}" if misspecification != "none" else ""
    observations_path = out / f"synthetic_observations_{profile}{suffix}.jsonl"
    results_path = out / f"synthetic_results_{profile}{suffix}.csv"
    summary_path = out / f"synthetic_summary_{profile}{suffix}.json"
    rows: list[dict[str, Any]] = []
    with observations_path.open("w", encoding="utf-8") as obs_file:
        for scenario in scenarios:
            for replicate_id in range(n_replicas):
                observation = generate_observation(scenario, replicate_id, master_seed=master_seed, misspecification=misspecification)
                inference = infer_observation(observation)
                obs_file.write(json.dumps(observation, separators=(",", ":")) + "\n")
                rows.append({
                    "protocol_id": protocol_id(), "config_hash": config_hash(), "scenario_id": scenario.scenario_id, "family": scenario.family, "replicate_id": replicate_id, "seed": observation["seed"], "truth_model": observation["truth_model"], "truth_gamma_t_s-1": observation["truth_gamma_t_s-1"], "truth_environment_rate_s-1": observation["truth_environment_rate_s-1"], "mass_ratio": scenario.mass_ratio, "pressure_true_pa": observation["pressure_true_pa"], "pressure_recorded_pa": observation["pressure_recorded_pa"], "classification": inference["classification"], "identifiability": inference["identifiability"], "likelihood_ratio": inference["likelihood_ratio"], "informative": inference["informative"], "coverage_proxy": inference["coverage_proxy"], "environment_mimic_ratio": inference["environment_mimic_ratio"], "misspecification": misspecification,
                })
    with results_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    summary = summarize(rows, profile, misspecification)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    inputs = [BASE / "config" / "synthetic_validation_v1.yaml", BASE / "config" / "tamesis_mc_v1.lock.json"]
    write_sidecar(observations_path, inputs=inputs, scenario=f"profile:{profile}", seed=master_seed, kind="synthetic_observations")
    write_sidecar(results_path, inputs=[observations_path], scenario=f"profile:{profile}", seed=master_seed, kind="synthetic_inference_results")
    write_sidecar(summary_path, inputs=[results_path], scenario=f"profile:{profile}", seed=master_seed, kind="synthetic_summary")
    return summary


def summarize(rows: list[dict[str, Any]], profile: str, misspecification: str) -> dict[str, Any]:
    def rate(predicate): return sum(bool(predicate(r)) for r in rows) / max(len(rows), 1)
    null_rows = [r for r in rows if r["truth_model"] == "null"]
    h1_rows = [r for r in rows if r["truth_model"] == "tamesis"]
    strong = [r for r in h1_rows if r["mass_ratio"] >= 1.5 and r["pressure_true_pa"] <= 1e-12]
    weak = [r for r in rows if 0.95 <= r["mass_ratio"] <= 1.2 or r["mass_ratio"] < 0.9]
    return {
        "synthetic_protocol_id": protocol_id(), "synthetic_config_hash": config_hash(), "profile": profile, "misspecification": misspecification, "n_rows": len(rows), "n_scenarios": len({r["scenario_id"] for r in rows}), "replicas_per_scenario": len(rows) // max(len({r["scenario_id"] for r in rows}), 1),
        "false_positive_rate": rate(lambda r: r in null_rows and r["classification"] == "tamesis_plus_environment"),
        "null_recovery_rate": rate(lambda r: r in null_rows and r["classification"] == "environment_only"),
        "h1_recovery_rate": rate(lambda r: r in h1_rows and r["classification"] == "tamesis_plus_environment"),
        "strong_signal_power": rate(lambda r: r in strong and r["classification"] == "tamesis_plus_environment"),
        "weak_inconclusive_rate": rate(lambda r: r in weak and r["classification"] == "inconclusive"),
        "coverage_95_proxy": rate(lambda r: r["coverage_proxy"]),
        "identifiability_counts": {key: sum(r["identifiability"] == key for r in rows) for key in sorted({r["identifiability"] for r in rows})},
        "environment_mimic_rate": rate(lambda r: r["truth_model"] == "null" and r["classification"] == "tamesis_plus_environment"),
        "seed_set": sorted({r["seed"] for r in rows})[:20],
    }


def main() -> None:
    profile = sys.argv[1] if len(sys.argv) > 1 else "quick"
    if profile not in {"quick", "standard", "high_precision"}:
        raise SystemExit("profile must be quick, standard or high_precision")
    print(json.dumps(run_profile(profile), indent=2))


if __name__ == "__main__":
    main()
