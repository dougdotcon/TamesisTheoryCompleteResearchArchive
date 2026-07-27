from __future__ import annotations
import json
from sensor_models import DATA, REPORTS, protocol_id

REPORTS_REQUIRED=["SENSOR_TRANSFER_MODELS_V0_2_PREREGISTRATION.md","SENSOR_TRANSFER_MODELS_V0_2_EXECUTION_REPORT.md","INSTRUMENT_REQUIREMENT_DERIVATION_AUDIT.md","INTERNAL_TEMPERATURE_OBSERVABILITY.md","CRYOGENIC_THERMOMETRY_FEASIBILITY.md","EFFECTIVE_PRESSURE_TRANSFER_MODEL.md","DETECTOR_TRANSFER_MODEL.md","PHASE_REFERENCE_TRANSFER_MODEL.md","MASS_METROLOGY_TRANSFER_MODEL.md","TRAJECTORY_TRANSFER_MODEL.md","SENSOR_RECOVERY_VALIDATION.md","SENSOR_FUSION_ANALYSIS.md","DECISION_ORIENTED_SENSOR_ERROR_BUDGET.md","THERMAL_FALSE_THRESHOLD_VALIDATION.md","PROFILE_LIKELIHOOD_WITH_SENSOR_MODELS.md","SENSOR_TRANSFER_MODELS_LIMITATIONS.md"]
DATA_REQUIRED=["sensor_model_registry.json","internal_temperature_model_comparison.csv","sensor_recovery_results.csv","decision_oriented_error_budget.csv","thermal_false_threshold_results.csv","sensor_fusion_results.csv"]
def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORTS_REQUIRED),*(DATA/n for n in DATA_REQUIRED)] if not p.exists()]
    final=(REPORTS/"SENSOR_TRANSFER_MODELS_V0_2_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    out={"valid":not missing and final.startswith("SENSOR_TRANSFER_MODELS_"),"protocol_id":protocol_id(),"conclusion":final.splitlines()[0] if final else None,"missing":missing}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out["valid"] else 1)
if __name__=="__main__": main()
