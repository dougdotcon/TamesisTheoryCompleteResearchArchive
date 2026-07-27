from __future__ import annotations
import json
from .robust_v1_2 import DATA, REPORTS, protocol_id

REPORTS_REQUIRED=["SYNTHETIC_V1_2_PREREGISTRATION.md","SYNTHETIC_V1_2_EXECUTION_REPORT.md","DISCRIMINATION_VS_IDENTIFIABILITY_AUDIT.md","ROBUST_LIKELIHOOD_IDENTIFIABILITY.md","OUTLIER_TAXONOMY_RESULTS.md","SIGNAL_PRESERVATION_UNDER_ROBUSTIFICATION.md","MONOTONIC_DRIFT_ANALYSIS.md","CYCLIC_DRIFT_ANALYSIS.md","FALSE_THRESHOLD_ADVERSARIAL_VALIDATION.md","JOINT_ROBUST_BLIND_CHALLENGE.md","PROFILE_LIKELIHOOD_MU_T.md","D4_CLASSIFICATION_AUDIT.md","TARGET_1E15_ROBUST_ANALYSIS.md","SYNTHETIC_V1_2_LIMITATIONS.md"]
DATA_REQUIRED=["synthetic_v1_2_baseline.json","outlier_taxonomy_results.csv","false_threshold_results.csv","profile_likelihood_mu_T.json"]
def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORTS_REQUIRED),*(DATA/n for n in DATA_REQUIRED)] if not p.exists()]
    final=(REPORTS/"SYNTHETIC_V1_2_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    out={"valid":not missing and final.startswith("ROBUST_JOINT_IDENTIFIABILITY_"),"protocol_id":protocol_id(),"conclusion":final.splitlines()[0] if final else None,"missing":missing}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out["valid"] else 1)
if __name__=="__main__": main()
