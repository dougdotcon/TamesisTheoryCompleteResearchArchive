from __future__ import annotations
import json
from .protocol import BASE, protocol_id, config_payload

REQUIRED = [
    "reports/SYNTHETIC_PHASE_BASELINE.md", "data/synthetic_phase_baseline.json",
    "reports/SYNTHETIC_VALIDATION_PROTOCOL.md", "reports/SYNTHETIC_VALIDATION_EXECUTION_REPORT.md",
    "reports/SYNTHETIC_VALIDATION_MATRIX.md",
    "reports/IDENTIFIABILITY_ANALYSIS.md", "reports/NULL_RECOVERY_REPORT.md",
    "reports/TAMESIS_RECOVERY_REPORT.md", "reports/ENVIRONMENT_MISSPECIFICATION_REPORT.md",
    "reports/BLIND_SYNTHETIC_CHALLENGE.md", "reports/POWER_ANALYSIS.md",
    "reports/TARGET_1E15_SYNTHETIC_IDENTIFIABILITY.md", "reports/SYNTHETIC_VALIDATION_LIMITATIONS.md",
    "data/synthetic_validation/synthetic_results_standard.csv", "data/synthetic_validation/scenario_metrics.csv",
    "data/synthetic_validation/identifiability_results.csv", "data/synthetic_validation/blind_challenge_results.csv",
    "data/synthetic_validation/environment_misspecification_screen.csv", "data/synthetic_validation/power_curves.csv",
]

def main() -> None:
    missing = [p for p in REQUIRED if not (BASE / p).exists()]
    missing_sidecars = [p for p in REQUIRED[2:] if not (BASE / p).with_suffix((BASE / p).suffix + ".provenance.json").exists()]
    report = {"valid": not missing and not missing_sidecars, "protocol_id": protocol_id(), "tamesis_protocol_id": config_payload()["tamesis_protocol_id"], "required_count": len(REQUIRED), "missing": missing, "missing_sidecars": missing_sidecars}
    print(json.dumps(report, indent=2))
    if not report["valid"]: raise SystemExit(1)

if __name__ == "__main__": main()
