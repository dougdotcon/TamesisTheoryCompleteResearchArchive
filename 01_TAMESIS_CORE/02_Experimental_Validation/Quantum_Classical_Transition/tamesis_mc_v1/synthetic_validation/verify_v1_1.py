from __future__ import annotations
import json
from pathlib import Path
from .joint_v1_1 import BASE, DATA, REPORTS, FIGURES, cfg, protocol_id

REPORT_NAMES = ["SYNTHETIC_V1_1_PREREGISTRATION.md", "SYNTHETIC_V1_1_EXECUTION_REPORT.md", "JOINT_DESIGN_STRUCTURAL_IDENTIFIABILITY.md", "MULTI_TIME_ANALYSIS.md", "MULTI_PRESSURE_ANALYSIS.md", "MULTI_MASS_THRESHOLD_ANALYSIS.md", "PRESSURE_ZERO_INTERCEPT_ANALYSIS.md", "PRESSURE_INDEPENDENT_ENVIRONMENT_ANALYSIS.md", "OUTLIER_STANDARD_ANALYSIS.md", "FALSE_THRESHOLD_ADVERSARIAL_TEST.md", "JOINT_BLIND_CHALLENGE.md", "OPTIMAL_EXPERIMENTAL_DESIGN.md", "TARGET_1E15_JOINT_DESIGN.md", "SYNTHETIC_V1_1_LIMITATIONS.md"]
DATA_NAMES = ["joint_design_rank_analysis.json", "profile_likelihood_mu_T.json", "joint_design_monte_carlo.json", "outlier_standard_1000.json"]

def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORT_NAMES), *(DATA/n for n in DATA_NAMES)] if not p.exists()]
    final=(REPORTS/"SYNTHETIC_V1_1_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    result={"valid":not missing and final.startswith("JOINT_IDENTIFIABILITY_"),"protocol_id":protocol_id(),"missing":missing,"conclusion":final.splitlines()[0] if final else None}
    print(json.dumps(result,indent=2)); raise SystemExit(0 if result["valid"] else 1)
if __name__ == "__main__": main()
