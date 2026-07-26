"""Generate the pre-registered numerical prediction table for M_c v1.0."""

from __future__ import annotations

import csv
import json

from mc_model import McModel
from workspace_paths import data_path, ensure_workspace_dirs


def main() -> None:
    ensure_workspace_dirs()
    model = McModel()
    masses = [0.25, 0.5, 0.9, 1.0, 1.01, 2.0, 10.0, 100.0]
    rows = []
    for ratio in masses:
        mass = ratio * model.mc
        rows.append({
            "M_over_Mc": ratio,
            "mass_kg": mass,
            "rate_s-1": model.intrinsic_rate(mass),
            "tau_s": model.coherence_time(mass),
            "t_half_s": model.half_visibility_time(mass),
            "V_at_1s": model.visibility(mass, 1.0),
        })
    data_path("model_summary.json").write_text(json.dumps(model.summary(), indent=2) + "\n", encoding="utf-8")
    with data_path("predictions.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(model.summary(), indent=2))
    for row in rows:
        print("M/Mc={M_over_Mc:g}  tau={tau_s:.6g}s  V(1s)={V_at_1s:.6g}".format(**row))


if __name__ == "__main__":
    main()
