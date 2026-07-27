from __future__ import annotations
import json
from pathlib import Path
from instrument_spec import BASE, DATA, REPORTS, protocol_id

REPORTS_REQUIRED=["INSTRUMENT_SPECIFICATION_V0_1_PREREGISTRATION.md","INSTRUMENT_SPECIFICATION_V0_1_EXECUTION_REPORT.md","EXPERIMENT_CAUSAL_GRAPH.md","MINIMUM_TELEMETRY_SET.md","SENSOR_PRECISION_REQUIREMENTS.md","TIMING_AND_SYNCHRONIZATION_REQUIREMENTS.md","RAW_DATA_REQUIREMENTS.md","INSTRUMENT_FMEA.md","TELEMETRY_IDENTIFIABILITY_ANALYSIS.md","TELEMETRY_ADVERSARIAL_VALIDATION.md","INSTRUMENT_BLIND_CHALLENGE.md","TARGET_1E15_INSTRUMENT_REQUIREMENTS.md","INSTRUMENT_SPECIFICATION_LIMITATIONS.md"]
DATA_REQUIRED=["instrument_causal_graph.json","minimum_telemetry_set.json","sensor_precision_requirements.csv","instrument_fmea.csv","telemetry_identifiability_results.csv","instrument_blind_challenge_results.csv"]
def main():
    missing=[str(p) for p in [*(REPORTS/n for n in REPORTS_REQUIRED),*(DATA/n for n in DATA_REQUIRED)] if not p.exists()]
    final=(REPORTS/"INSTRUMENT_SPECIFICATION_V0_1_EXECUTION_REPORT.md").read_text(encoding="utf-8") if not missing else ""
    out={"valid":not missing and final.startswith("INSTRUMENT_SPECIFICATION_IDENTIFIABILITY_"),"protocol_id":protocol_id(),"conclusion":final.splitlines()[0] if final else None,"missing":missing}; print(json.dumps(out,indent=2)); raise SystemExit(0 if out["valid"] else 1)
if __name__=="__main__": main()
