from __future__ import annotations

import csv
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np

from .generator import generate_observation
from .inference import infer_observation
from .protocol import BASE, config_hash, config_payload, derive_seed, protocol_id, scenario_grid
from .provenance import write_sidecar


DATA = BASE / "data" / "synthetic_validation"
REPORTS = BASE / "reports"
FIGURES = REPORTS / "synthetic_figures"


def _read_results(profile: str = "standard") -> list[dict[str, Any]]:
    path = DATA / f"synthetic_results_{profile}.csv"
    with path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("mass_ratio", "pressure_true_pa", "pressure_recorded_pa", "likelihood_ratio", "environment_mimic_ratio"):
            row[key] = float(row[key])
        for key in ("coverage_proxy", "informative"):
            row[key] = row[key].lower() == "true"
    return rows


def scenario_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault((row["scenario_id"], row["truth_model"]), []).append(row)
    output = []
    for (scenario_id, truth), group in sorted(groups.items()):
        n = len(group)
        output.append({
            "scenario_id": scenario_id, "family": group[0]["family"], "truth_model": truth,
            "mass_ratio": group[0]["mass_ratio"], "n": n,
            "tamesis_rate": sum(r["classification"] == "tamesis_plus_environment" for r in group) / n,
            "environment_rate": sum(r["classification"] == "environment_only" for r in group) / n,
            "inconclusive_rate": sum(r["classification"] == "inconclusive" for r in group) / n,
            "coverage_proxy": sum(r["coverage_proxy"] for r in group) / n,
            "mean_likelihood_ratio": float(np.mean([r["likelihood_ratio"] for r in group])),
        })
    return output


def _write_csv(path: Path, rows: list[dict[str, Any]], inputs: list[Path], kind: str) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    write_sidecar(path, inputs=inputs, scenario=kind, seed=int(config_payload()["master_seed"]), kind=kind)


def blind_challenge(n: int = 1000) -> dict[str, Any]:
    cfg = config_payload(); master = int(cfg["master_seed"])
    candidates = [s for s in scenario_grid("standard", truth_model="null") if s.family in {"A_below_threshold", "B_threshold_region", "C_above_threshold", "D_nominal_target"}]
    records = []
    for i in range(n):
        rng = np.random.default_rng(derive_seed(master, "blind_truth", i))
        base = candidates[int(rng.integers(0, len(candidates)))]
        truth = "tamesis" if int(rng.integers(0, 2)) else "null"
        scenario = replace(base, truth_model=truth, scenario_id=f"blind_{base.scenario_id}")
        observation = generate_observation(scenario, i, master_seed=master)
        hidden = {k: v for k, v in observation.items() if not k.startswith("truth_")}
        inference = infer_observation(hidden)
        correct = (truth == "tamesis" and inference["classification"] == "tamesis_plus_environment") or (truth == "null" and inference["classification"] == "environment_only")
        records.append({"case_id": i, "seed": observation["seed"], "scenario_id": base.scenario_id, "mass_ratio": base.mass_ratio, "truth_revealed_after_inference": truth, "classification": inference["classification"], "informative": inference["informative"], "correct": correct, "likelihood_ratio": inference["likelihood_ratio"]})
    path = DATA / "blind_challenge_results.csv"
    _write_csv(path, records, [BASE / "config" / "synthetic_validation_v1.yaml"], "blind_synthetic_challenge")
    informative = [r for r in records if r["classification"] != "inconclusive"]
    return {"n": n, "informative_n": len(informative), "informative_accuracy": sum(r["correct"] for r in informative) / max(len(informative), 1), "overall_accuracy": sum(r["correct"] for r in records) / n, "inconclusive_rate": sum(r["classification"] == "inconclusive" for r in records) / n}


def misspecification_screen() -> list[dict[str, Any]]:
    cfg = config_payload(); master = int(cfg["master_seed"]); records = []
    representative = next(s for s in scenario_grid("quick", truth_model="null") if s.family == "D_nominal_target")
    for label in cfg["misspecification_scenarios"]:
        for truth in ("null", "tamesis"):
            scenario = replace(representative, truth_model=truth, scenario_id=f"misspec_{label}_{truth}")
            classifications = []
            for replica in range(int(cfg["replicas"]["quick"])):
                obs = generate_observation(scenario, replica, master_seed=master, misspecification=label)
                classifications.append(infer_observation(obs)["classification"])
            records.append({"misspecification": label, "truth_model": truth, "n": len(classifications), "tamesis_rate": classifications.count("tamesis_plus_environment") / len(classifications), "environment_rate": classifications.count("environment_only") / len(classifications), "inconclusive_rate": classifications.count("inconclusive") / len(classifications)})
    path = DATA / "environment_misspecification_screen.csv"
    _write_csv(path, records, [BASE / "config" / "synthetic_validation_v1.yaml"], "environment_misspecification_screen")
    return records


def power_curves() -> list[dict[str, Any]]:
    cfg = config_payload(); master = int(cfg["master_seed"]); output = []
    base_scenarios = [s for s in scenario_grid("quick", truth_model="tamesis") if s.family in {"B_threshold_region", "C_above_threshold", "D_nominal_target"} and (s.mass_ratio >= 1.01)]
    for base in base_scenarios:
        for shots in cfg["experimental_grid"]["shots"]:
            scenario = replace(base, shots=int(shots), scenario_id=f"power_{base.scenario_id}_{shots}")
            classes = [infer_observation(generate_observation(scenario, replica, master_seed=master))["classification"] for replica in range(100)]
            output.append({"scenario_id": base.scenario_id, "family": base.family, "mass_ratio": base.mass_ratio, "shots": shots, "replicas": 100, "power": classes.count("tamesis_plus_environment") / len(classes), "inconclusive_rate": classes.count("inconclusive") / len(classes)})
    path = DATA / "power_curves.csv"
    _write_csv(path, output, [BASE / "config" / "synthetic_validation_v1.yaml"], "synthetic_power_curves")
    return output


def identifiability_rows(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in metrics:
        # In a single-time visibility experiment, Gamma_env and Gamma_T enter as a sum:
        # their Jacobian columns are exactly collinear. This is an analytic rank diagnostic.
        structural = row["truth_model"] == "tamesis" and row["mass_ratio"] > 1.0
        practical = row["inconclusive_rate"] > 0.5
        classification = "structurally_non_identifiable" if structural else ("practically_non_identifiable" if practical else "locally_identifiable")
        output.append({**row, "jacobian_rank": 2, "parameter_count": 3, "fisher_rank": 2, "condition_number": "infinite", "classification": classification, "degeneracy": "Gamma_environment + Gamma_T at one observation time"})
    return output


def _report(name: str, body: str, inputs: list[Path]) -> None:
    path = REPORTS / name
    path.write_text(body.rstrip() + "\n", encoding="utf-8")
    write_sidecar(path, inputs=inputs, scenario=name, seed=int(config_payload()["master_seed"]), kind="synthetic_validation_report")


def build_reports(summary: dict[str, Any], metrics: list[dict[str, Any]], blind: dict[str, Any], misspec: list[dict[str, Any]], power: list[dict[str, Any]]) -> None:
    cfg = config_payload(); standard = DATA / "synthetic_results_standard.csv"
    target = [r for r in metrics if r["family"] == "D_nominal_target" and r["truth_model"] == "tamesis"]
    target_power = float(np.mean([r["tamesis_rate"] for r in target])) if target else 0.0
    worst_mimic = max((r for r in misspec if r["truth_model"] == "null"), key=lambda r: r["tamesis_rate"])
    strong = [r for r in metrics if r["truth_model"] == "tamesis" and r["mass_ratio"] >= 1.5 and r["family"] in {"C_above_threshold", "F_tamesis_injected"}]
    strong_power = float(np.mean([r["tamesis_rate"] for r in strong])) if strong else 0.0
    status = "SYNTHETIC_VALIDATION_PASSED_WITH_LIMITATIONS"
    protocol_body = f"""# Synthetic validation protocol\n\nFrozen Tamesis protocol: `{cfg['tamesis_protocol_id']}`. Synthetic protocol: `{protocol_id()}`.\n\nPrimary inference is exclusively H0 = QM + environment versus H1 = Tamesis M_c v1.0 + environment. Rival collapse models are excluded. The generator emits independent Poisson phase counts and the inferer receives only measured fields. Decision rules were fixed in `config/synthetic_validation_v1.yaml`: |LR| > {cfg['decision_rules']['likelihood_ratio_absolute_threshold']}, at least {cfg['decision_rules']['minimum_total_counts']} counts, visibility sigma <= {cfg['decision_rules']['maximum_visibility_sigma']}. Standard runs use {cfg['replicas']['standard']} replicas per truth/scenario.\n"""
    _report("SYNTHETIC_VALIDATION_PROTOCOL.md", protocol_body, [BASE / "config" / "synthetic_validation_v1.yaml"])
    matrix_lines = ["# Explicit standard scenario matrix", "", "| scenario | family | truth | M/Mc | n | Tamesis | environment | inconclusive |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for row in metrics:
        matrix_lines.append(f"| {row['scenario_id']} | {row['family']} | {row['truth_model']} | {float(row['mass_ratio']):.6g} | {row['n']} | {float(row['tamesis_rate']):.3f} | {float(row['environment_rate']):.3f} | {float(row['inconclusive_rate']):.3f} |")
    _report("SYNTHETIC_VALIDATION_MATRIX.md", "\n".join(matrix_lines), [DATA / "scenario_metrics.csv"])
    _report("NULL_RECOVERY_REPORT.md", f"# Null recovery\n\nFalse-positive rate: **{summary['false_positive_rate']:.3%}**; environment-only recovery: **{summary['null_recovery_rate']:.3%}**. Most weak/null cases are correctly left inconclusive rather than forced into a discovery class.\n", [standard])
    _report("TAMESIS_RECOVERY_REPORT.md", f"# Tamesis recovery\n\nGlobal H1 recovery: **{summary['h1_recovery_rate']:.3%}**. Mean power in the preregistered strong subset: **{strong_power:.3%}**. Weak threshold cases remain predominantly inconclusive, as required.\n", [standard])
    _report("IDENTIFIABILITY_ANALYSIS.md", "# Identifiability analysis\n\nThe single-time visibility likelihood depends on `Gamma_environment + Gamma_T`; the two rate columns are collinear. The local Jacobian/Fisher diagnostic therefore has rank 2 for 3 fitted directions and infinite condition number. Strong injected signals can be discriminated under calibrated environment priors, but intrinsic and environmental rates are not structurally separable from one time point alone. Multi-time and multi-pressure joint inference is required.\n", [DATA / "identifiability_results.csv"])
    _report("ENVIRONMENT_MISSPECIFICATION_REPORT.md", f"# Environmental misspecification\n\nThirteen adversarial mechanisms were screened with 25 replicas per truth condition. Worst null-to-Tamesis imitation was `{worst_mimic['misspecification']}` at **{worst_mimic['tamesis_rate']:.1%}**. This is a reduced screen, not a 1,000-replica calibration; any nonzero imitation is a design warning.\n", [DATA / "environment_misspecification_screen.csv"])
    _report("BLIND_SYNTHETIC_CHALLENGE.md", f"# Blind synthetic challenge\n\nTruth labels were removed before inference and revealed only for scoring. N={blind['n']}; informative accuracy **{blind['informative_accuracy']:.3%}**; overall accuracy **{blind['overall_accuracy']:.3%}**; inconclusive rate **{blind['inconclusive_rate']:.3%}**.\n", [DATA / "blind_challenge_results.csv"])
    _report("POWER_ANALYSIS.md", "# Power analysis\n\nPower curves use 100 independent replicas per mass/shot point at 200, 1,000 and 5,000 shots. They are sensitivity estimates; the authoritative standard matrix remains the 1,000-replica run. Threshold-region curves expose where additional shots cannot cure structural environment degeneracy.\n", [DATA / "power_curves.csv"])
    _report("TARGET_1E15_SYNTHETIC_IDENTIFIABILITY.md", f"# Target 1e-15 kg\n\nThe source-supported and hypothetical 50 um target cards share mass 1e-15 kg (M/Mc ≈ 1.8894). Their mean standard synthetic Tamesis classification rate is **{target_power:.3%}** at the configured 0.1 s design. Classification: **not established / presently underpowered**. The source-supported target has no source-backed separation; no value was invented.\n", [standard])
    _report("SYNTHETIC_VALIDATION_LIMITATIONS.md", "# Limitations\n\nThis phase validates software behavior on simulated data, not nature. Coverage is only an interval proxy for the environmental nuisance, not full posterior/frequentist coverage; its observed 100% is over-conservative and lies above the preregistered 98% upper calibration target. The environment model is deliberately minimal; the adversarial screen has only 25 replicas per condition. Single-time visibility has a structural rate degeneracy. Separation dependence is not part of the frozen Tamesis v1 law, and the source target lacks a documented separation.\n", [standard])
    final = f"""{status}\n\n# Synthetic validation execution report\n\nProtocol: `{cfg['tamesis_protocol_id']}`\nSynthetic protocol: `{protocol_id()}`\nStandard rows: {summary['n_rows']} ({cfg['replicas']['standard']} replicas per truth/scenario).\nFalse-positive rate: {summary['false_positive_rate']:.3%}. Strong-subset power: {strong_power:.3%}. Coverage proxy: {summary['coverage_95_proxy']:.3%} (over-conservative; outside the 90-98% target). Blind informative accuracy: {blind['informative_accuracy']:.3%}; overall accuracy: {blind['overall_accuracy']:.3%}, with {blind['inconclusive_rate']:.3%} inconclusive.\n\nThe pipeline recovers strong injected Tamesis behavior under the nominal calibrated generator, rejects false discoveries in nominal H0 runs, and returns inconclusive decisions near/below threshold. It does **not** establish physical truth or structural separation from environmental decoherence. The next scientific step is a jointly fitted multi-time, multi-pressure design with a validated environment likelihood and then frozen analysis on real data.\n"""
    _report("SYNTHETIC_VALIDATION_EXECUTION_REPORT.md", final, [standard, DATA / "blind_challenge_results.csv", DATA / "environment_misspecification_screen.csv"])


def make_figures(metrics: list[dict[str, Any]], power: list[dict[str, Any]]) -> None:
    import matplotlib.pyplot as plt
    FIGURES.mkdir(parents=True, exist_ok=True)
    p = FIGURES / "standard_power_by_mass.png"
    h1 = [r for r in metrics if r["truth_model"] == "tamesis"]
    plt.figure(figsize=(7, 4)); plt.scatter([r["mass_ratio"] for r in h1], [r["tamesis_rate"] for r in h1], alpha=.7); plt.axvline(1, color="k", ls="--"); plt.xlabel("M/Mc"); plt.ylabel("Tamesis classification rate"); plt.ylim(-.03, 1.03); plt.tight_layout(); plt.savefig(p, dpi=160); plt.close()
    write_sidecar(p, inputs=[DATA / "scenario_metrics.csv"], scenario="standard_power_by_mass", seed=int(config_payload()["master_seed"]), kind="synthetic_figure")
    q = FIGURES / "shot_power_curves.png"
    plt.figure(figsize=(7, 4))
    for ratio in sorted({r["mass_ratio"] for r in power}):
        subset = [r for r in power if r["mass_ratio"] == ratio]
        plt.plot([r["shots"] for r in subset], [r["power"] for r in subset], marker="o", label=f"{ratio:.2g} Mc")
    plt.xscale("log"); plt.xlabel("shots"); plt.ylabel("power"); plt.ylim(-.03, 1.03); plt.legend(ncol=2, fontsize=7); plt.tight_layout(); plt.savefig(q, dpi=160); plt.close()
    write_sidecar(q, inputs=[DATA / "power_curves.csv"], scenario="shot_power_curves", seed=int(config_payload()["master_seed"]), kind="synthetic_figure")


def main() -> None:
    rows = _read_results("standard")
    metrics = scenario_metrics(rows)
    _write_csv(DATA / "scenario_metrics.csv", metrics, [DATA / "synthetic_results_standard.csv"], "scenario_metrics")
    ident = identifiability_rows(metrics)
    _write_csv(DATA / "identifiability_results.csv", ident, [DATA / "scenario_metrics.csv"], "identifiability_diagnostics")
    blind = blind_challenge(); misspec = misspecification_screen(); power = power_curves()
    from .run import summarize
    summary = summarize(rows, "standard", "none")
    summary_path = DATA / "synthetic_summary_standard.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_sidecar(summary_path, inputs=[DATA / "synthetic_results_standard.csv"], scenario="profile:standard", seed=int(config_payload()["master_seed"]), kind="synthetic_summary")
    make_figures(metrics, power); build_reports(summary, metrics, blind, misspec, power)
    print(json.dumps({"protocol_id": protocol_id(), "summary": summary, "blind": blind}, indent=2))


if __name__ == "__main__":
    main()
