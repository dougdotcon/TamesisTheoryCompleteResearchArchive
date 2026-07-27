from __future__ import annotations
import json
from demonstrator_a import DATA, REPORTS, SCHEMAS, protocol_id
REPORTS_REQUIRED=["DEMONSTRATOR_A_V0_4_PREREGISTRATION.md","DEMONSTRATOR_A_V0_4_EXECUTION_REPORT.md","THERMOMETRY_METHOD_SELECTION.md","GEV_PRIMARY_THERMOMETER_MODEL.md","SECONDARY_THERMOMETRY_CANDIDATES.md","THERMOMETRY_INDEPENDENCE_AUDIT.md","THERMAL_TIME_CONSTANT_PROTOCOL.md","READOUT_HEATING_PROTOCOL.md","PARTICLE_SPECIFIC_CALIBRATION.md","A0_A4_GATE_SPECIFICATION.md","THERMOMETRY_GO_NO_GO_CRITERIA.md","DEMONSTRATOR_A_HARDWARE_DATA_REQUIREMENTS.md","DEMONSTRATOR_A_LIMITATIONS.md"]
DATA_REQUIRED=["thermometry_method_registry.json","a0_a4_gate_registry.json","thermal_model_registry.json","thermometry_cross_sensitivities.csv","demonstrator_a_go_no_go.csv","demonstrator_a_locked_synthetic_fixture.json"]
SCHEMA_REQUIRED=["stationary_calibration_record.schema.json","thermal_step_record.schema.json","spectral_record.schema.json","levitation_thermometry_record.schema.json"]
def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORTS_REQUIRED),*(DATA/n for n in DATA_REQUIRED),*(SCHEMAS/n for n in SCHEMA_REQUIRED)] if not p.exists()]
    final=(REPORTS/"DEMONSTRATOR_A_V0_4_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    forbidden=any(x in final for x in ["INTERNAL_THERMOMETRY_DEMONSTRATED","mu_T =","H1 wins"])
    out={"valid":not missing and not forbidden and final.startswith("DEMONSTRATOR_A_"),"protocol_id":protocol_id(),"conclusion":final.splitlines()[0] if final else None,"missing":missing,"forbidden_claim":forbidden}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out["valid"] else 1)
if __name__=="__main__": main()
