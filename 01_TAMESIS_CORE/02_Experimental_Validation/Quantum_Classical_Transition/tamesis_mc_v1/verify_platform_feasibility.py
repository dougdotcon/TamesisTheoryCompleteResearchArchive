from __future__ import annotations
import json
from platform_feasibility import DATA, REPORTS, protocol_id
REPORTS_REQUIRED=["PLATFORM_FEASIBILITY_V0_3_PREREGISTRATION.md","PLATFORM_FEASIBILITY_V0_3_EXECUTION_REPORT.md","EXTREME_VACUUM_FEASIBILITY.md","CRYOGENIC_THERMOMETRY_TRADE_STUDY.md","PLATFORM_TRADE_SPACE.md","REQUIREMENT_RELAXATION_ANALYSIS.md","TECHNOLOGY_MATURITY_MATRIX.md","INCREMENTAL_DEMONSTRATOR_PLAN.md","GO_NO_GO_CRITERIA.md","PLATFORM_RISK_REGISTER.md","VALUE_OF_INFORMATION_ANALYSIS.md","TARGET_MASS_REASSESSMENT.md","PLATFORM_FEASIBILITY_LIMITATIONS.md"]
DATA_REQUIRED=["platform_registry.json","platform_trade_space.csv","requirement_relaxation_results.csv","technology_maturity_matrix.csv","demonstrator_plan.json","platform_risk_register.csv","value_of_information.csv"]
def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORTS_REQUIRED),*(DATA/n for n in DATA_REQUIRED)] if not p.exists()]
    final=(REPORTS/"PLATFORM_FEASIBILITY_V0_3_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    out={"valid":not missing and final.startswith("PLATFORM_"),"protocol_id":protocol_id(),"conclusion":final.splitlines()[0] if final else None,"missing":missing}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out["valid"] else 1)
if __name__=="__main__": main()
