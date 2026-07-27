"""Rank planned experiments by Tamesis M_c discriminating power."""

from __future__ import annotations

from config import reject_runtime_overrides

import csv
import json
from pathlib import Path
from typing import Dict, List

try:
    from .mc_model import McModel
except ImportError:
    from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def threshold_score(m_over_mc: float, visibility_at_t: float, status: str) -> float:
    if status != "planned":
        return 0.0
    threshold_bonus = 1.0 / (1.0 + abs(m_over_mc - 1.0))
    above_bonus = 1.0 if m_over_mc > 1.0 else 0.25 * m_over_mc
    contrast_bonus = abs(0.5 - visibility_at_t) + (1.0 - visibility_at_t)
    return threshold_bonus + above_bonus + contrast_bonus


def decisiveness_score(m_over_mc: float, visibility_at_t: float, status: str) -> float:
    if status != "planned":
        return 0.0
    if m_over_mc <= 1.0:
        return 0.0
    expected_loss = 1.0 - visibility_at_t
    above_strength = min(m_over_mc / 2.0, 5.0)
    measurable_window = 1.0 - abs(visibility_at_t - 0.5)
    measurable_window = max(0.0, measurable_window)
    return expected_loss + above_strength + measurable_window


def prioritize(dataset_path: Path | None = None, output_path: Path | None = None) -> Dict:
    ensure_workspace_dirs()
    dataset_path = dataset_path or data_path("literature_points.csv")
    output_path = output_path or data_path("target_priority_report.json")
    mc = McModel()
    summary = mc.summary()

    rows = load_rows(dataset_path)
    enriched = []
    for row in rows:
        mass = float(row["mass_kg"])
        time_s = float(row["observation_time_s"])
        m_over_mc = mass / mc.mc
        visibility = mc.visibility(mass, time_s)
        enriched_row = dict(row)
        enriched_row["M_over_Mc"] = m_over_mc
        enriched_row["tamesis_visibility_at_observation_time"] = visibility
        enriched_row["tamesis_rate_s-1"] = mc.intrinsic_rate(mass)
        enriched_row["threshold_score"] = threshold_score(m_over_mc, visibility, row["status"])
        enriched_row["decisiveness_score"] = decisiveness_score(m_over_mc, visibility, row["status"])
        enriched.append(enriched_row)

    planned = [r for r in enriched if r["status"] == "planned"]
    threshold_sorted = sorted(planned, key=lambda r: float(r["threshold_score"]), reverse=True)
    decisive_sorted = sorted(planned, key=lambda r: float(r["decisiveness_score"]), reverse=True)

    report = {
        "dataset": dataset_path.name,
        "protocol_id": summary["protocol_id"],
        "config_hash": summary["config_hash"],
        "Mc_kg": mc.mc,
        "Mc_amu": mc.mc / 1.66053906660e-27,
        "top_threshold_targets": threshold_sorted[:10],
        "top_decisive_targets": decisive_sorted[:10],
        "interpretation": [
            "Threshold score favors proximity to M_c.",
            "Decisiveness score favors planned, above-threshold targets with measurable predicted loss.",
            "Scores are not evidence; they are triage metrics for where a real experiment could discriminate.",
        ],
    }
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_sidecar(
        output_path,
        provenance_record(
            output_path=output_path,
            contract=mc.contract,
            script="prioritize_targets.py",
            inputs=[str(dataset_path)],
            arguments={},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    return report


def main() -> None:
    reject_runtime_overrides()
    report = prioritize()
    print(json.dumps({
        "Mc_kg": report["Mc_kg"],
        "Mc_amu": report["Mc_amu"],
        "top_targets": [
            {
                "experiment": row["experiment"],
                "M_over_Mc": row["M_over_Mc"],
                "visibility": row["tamesis_visibility_at_observation_time"],
                "threshold_score": row["threshold_score"],
                "decisiveness_score": row["decisiveness_score"],
            }
            for row in report["top_decisive_targets"][:5]
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
