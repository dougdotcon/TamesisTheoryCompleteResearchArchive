"""Model comparison scaffold for Tamesis vs CSL, GRW, DP, and environment.

This script is intentionally conservative:
- it reads a small CSV of experiment records;
- it compares fixed model predictions with observed binary outcomes;
- it fits only a nuisance environmental-rate baseline by family;
- it writes a compact JSON report for auditability.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from math import exp, log
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from config import reject_runtime_overrides

try:
    from .mc_model import McModel
except ImportError:
    from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


@dataclass(frozen=True)
class ExperimentRecord:
    experiment: str
    family: str
    mass_kg: float
    separation_m: float
    observation_time_s: float
    observed_coherence: bool
    status: str
    source: str
    source_url: str = ""
    notes: str = ""


@dataclass(frozen=True)
class ModelScore:
    name: str
    log_likelihood: float
    aic: float
    bic: float
    parameters: int


def clamp_probability(p: float, eps: float = 1e-12) -> float:
    return max(eps, min(1.0 - eps, p))


def predict_coherence_probability(model_name: str, record: ExperimentRecord, mc: McModel) -> float:
    """Map each model to a coherence probability on [0, 1]."""
    t = record.observation_time_s
    m = record.mass_kg
    dx = max(record.separation_m, 1e-18)

    if model_name == "Tamesis":
        return clamp_probability(mc.visibility(m, t))

    if model_name == "CSL":
        lambda_csl = 1e-16
        r_c = 1e-7
        m_nucleon = 1.67262192369e-27
        gamma = lambda_csl * (m / m_nucleon) ** 2 * (1.0 - exp(-((dx / r_c) ** 2)))
        return clamp_probability(exp(-gamma * t))

    if model_name == "GRW":
        lambda_grw = 1e-16
        a = 1e-7
        m_nucleon = 1.67262192369e-27
        gamma = (m / m_nucleon) * lambda_grw * (1.0 - exp(-((dx / a) ** 2)))
        return clamp_probability(exp(-gamma * t))

    if model_name == "DP":
        G = 6.67430e-11
        hbar = 1.054571817e-34
        gamma = G * m * m / (hbar * dx)
        return clamp_probability(exp(-gamma * t))

    raise ValueError(f"Unknown model: {model_name}")


def log_likelihood_binary(records: Iterable[ExperimentRecord], probs: Iterable[float]) -> float:
    total = 0.0
    for rec, p in zip(records, probs):
        p = clamp_probability(p)
        total += log(p if rec.observed_coherence else (1.0 - p))
    return total


def fit_environment_rates(records: List[ExperimentRecord]) -> Dict[str, float]:
    """Fit one nuisance decay rate per family by grid search."""
    families = sorted({r.family for r in records})
    rates: Dict[str, float] = {}
    grid = [10 ** x for x in [i / 2 - 12 for i in range(0, 49)]]
    for family in families:
        family_records = [r for r in records if r.family == family]
        best_rate = 0.0
        best_ll = float("-inf")
        for rate in grid:
            ll = 0.0
            for rec in family_records:
                p = clamp_probability(exp(-rate * rec.observation_time_s))
                ll += log(p if rec.observed_coherence else (1.0 - p))
            if ll > best_ll:
                best_ll = ll
                best_rate = rate
        rates[family] = best_rate
    return rates


def score_fixed_model(name: str, records: List[ExperimentRecord], mc: McModel) -> ModelScore:
    probs = [predict_coherence_probability(name, r, mc) for r in records]
    ll = log_likelihood_binary(records, probs)
    k = 0
    n = len(records)
    aic = 2 * k - 2 * ll
    bic = k * log(n) - 2 * ll if n else float("inf")
    return ModelScore(name=name, log_likelihood=ll, aic=aic, bic=bic, parameters=k)


def score_environment_model(records: List[ExperimentRecord]) -> tuple[ModelScore, Dict[str, float]]:
    rates = fit_environment_rates(records)
    probs = []
    for rec in records:
        rate = rates[rec.family]
        probs.append(clamp_probability(exp(-rate * rec.observation_time_s)))
    ll = log_likelihood_binary(records, probs)
    k = len(rates)
    n = len(records)
    aic = 2 * k - 2 * ll
    bic = k * log(n) - 2 * ll if n else float("inf")
    return ModelScore(name="Environment", log_likelihood=ll, aic=aic, bic=bic, parameters=k), rates


def load_records(path: Path) -> List[ExperimentRecord]:
    records: List[ExperimentRecord] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("status", "").strip().lower() != "observed":
                continue
            records.append(
                ExperimentRecord(
                    experiment=row["experiment"].strip(),
                    family=row["family"].strip(),
                    mass_kg=float(row["mass_kg"]),
                    separation_m=float(row["separation_m"]),
                    observation_time_s=float(row["observation_time_s"]),
                    observed_coherence=row["observed_coherence"].strip() in {"1", "true", "True", "yes", "YES"},
                    status=row["status"].strip(),
                    source=row["source"].strip(),
                    source_url=row.get("source_url", "").strip(),
                    notes=row.get("notes", "").strip(),
                )
            )
    return records


def run_comparison(dataset_path: Optional[Path] = None, output_path: Optional[Path] = None) -> Dict:
    ensure_workspace_dirs()
    dataset_path = dataset_path or data_path("literature_points.csv")
    output_path = output_path or data_path("comparison_report.json")

    records = load_records(dataset_path)
    mc = McModel()
    summary = mc.summary()

    fixed_models = ["Tamesis", "CSL", "GRW", "DP"]
    scores = [score_fixed_model(name, records, mc) for name in fixed_models]
    env_score, fitted_rates = score_environment_model(records)
    scores.append(env_score)

    ranking = sorted(scores, key=lambda s: (s.aic, -s.log_likelihood))

    per_record = []
    for rec in records:
        row = asdict(rec)
        row["protocol_id"] = summary["protocol_id"]
        row["M_over_Mc"] = rec.mass_kg / mc.mc
        row["predictions"] = {name: predict_coherence_probability(name, rec, mc) for name in fixed_models}
        row["predictions"]["Environment"] = exp(-fitted_rates[rec.family] * rec.observation_time_s)
        per_record.append(row)

    diagnostics = {
        "coherent_records": sum(1 for r in records if r.observed_coherence),
        "decohered_records": sum(1 for r in records if not r.observed_coherence),
        "near_threshold_records": sum(1 for r in records if 0.5 * mc.mc <= r.mass_kg <= 10.0 * mc.mc),
        "above_threshold_records": sum(1 for r in records if r.mass_kg > mc.mc),
        "is_discriminating_dataset": any(not r.observed_coherence for r in records)
        and any(0.5 * mc.mc <= r.mass_kg <= 10.0 * mc.mc for r in records),
    }

    report = {
        "dataset": dataset_path.name,
        "protocol_id": summary["protocol_id"],
        "config_hash": summary["config_hash"],
        "n_observed_records": len(records),
        "diagnostics": diagnostics,
        "records": per_record,
        "scores": [asdict(s) for s in scores],
        "legacy_exploratory_ranking": [s.name for s in ranking],
        "environment_rates_s-1": fitted_rates,
        "notes": [
            "This report is a pre-registered comparison scaffold, not a discovery claim.",
            "Only observed rows are included in the likelihood.",
            "Planned rows remain in the CSV for future extension but are excluded here.",
            "The current archive table is not yet discriminating: it has no observed threshold-region outcome.",
        ],
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=mc.contract,
            script="compare_models.py",
            inputs=[str(dataset_path)],
            arguments={"fixed_models": fixed_models},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return report


def main() -> None:
    reject_runtime_overrides()
    report = run_comparison()
    print(
        json.dumps(
            {
                "dataset": report["dataset"],
                "n_observed_records": report["n_observed_records"],
                "legacy_exploratory_ranking": report["legacy_exploratory_ranking"],
                "environment_rates_s-1": report["environment_rates_s-1"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
