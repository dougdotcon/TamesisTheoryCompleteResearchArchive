"""Generate the pre-registered numerical prediction table for M_c v1.0."""

from __future__ import annotations

import csv
import json

from config import reject_runtime_overrides
from mc_model import McModel
from provenance import provenance_record, write_sidecar
from workspace_paths import data_path, ensure_workspace_dirs


def main() -> None:
    reject_runtime_overrides()
    ensure_workspace_dirs()
    model = McModel()
    masses = [0.25, 0.5, 0.9, 1.0, 1.01, 2.0, 10.0, 100.0]
    summary = model.summary()
    rows = []
    for ratio in masses:
        mass = ratio * model.mc
        rows.append({
            "protocol_id": summary["protocol_id"],
            "M_over_Mc": ratio,
            "mass_kg": mass,
            "rate_s-1": model.intrinsic_rate(mass),
            "tau_s": model.coherence_time(mass),
            "t_half_s": model.half_visibility_time(mass),
            "V_at_1s": model.visibility(mass, 1.0),
        })
    summary_path = data_path("model_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with data_path("predictions.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    write_sidecar(
        summary_path,
        provenance_record(
            output_path=summary_path,
            contract=model.contract,
            script="run_predictions.py",
            inputs=[],
            arguments={"masses": masses},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    write_sidecar(
        data_path("predictions.csv"),
        provenance_record(
            output_path=data_path("predictions.csv"),
            contract=model.contract,
            script="run_predictions.py",
            inputs=[str(summary_path)],
            arguments={"masses": masses},
            status="derived_result",
            epistemic_status="derived_result",
        ),
    )
    print(json.dumps(summary, indent=2))
    for row in rows:
        print("M/Mc={M_over_Mc:g}  tau={tau_s:.6g}s  V(1s)={V_at_1s:.6g}".format(**row))


if __name__ == "__main__":
    main()
