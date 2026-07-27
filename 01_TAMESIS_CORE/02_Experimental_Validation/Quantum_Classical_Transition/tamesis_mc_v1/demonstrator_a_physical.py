from __future__ import annotations
import hashlib, json
from pathlib import Path
import yaml
from synthetic_validation.provenance import write_sidecar
from synthetic_validation.protocol import BASE

CFG=BASE/"config/demonstrator_a_v0_6.yaml"; DATA=BASE/"data/demonstrator_a_v0_6"; REPORTS=BASE/"reports"
def cfg(): return yaml.safe_load(CFG.read_text(encoding="utf-8"))
def cfg_hash(): return hashlib.sha256(json.dumps(cfg(),sort_keys=True,separators=(",",":")).encode()).hexdigest()
def protocol_id(): return "tamesis-demonstrator-a-v0.6:"+cfg_hash()

def campaign_state():
    c=cfg(); origin=c["data_origin"]
    return {"protocol_id":protocol_id(),"campaign_state":"HARDWARE_QUALIFICATION_NOT_STARTED","data_origin":origin,"q0_status":"not_started","traceability":"not_supplied","absolute_readout_heating_limit_k":None,"stability_criteria":"awaiting real time series","particles_evaluated":0,"particles_advanced":0,"model_locked":False,"leakage_test":"not_run","blind_predictions":0,"reveal_metrics":None,"invalid_runs":0,"candidate_decisions":[],"A2_authorized":False,"physical_evidence":False,"pre_hardware_conclusion":"A0_A1_HARDWARE_PACKAGE_READY_WITH_LIMITATIONS"}

def enforce_origin(origin):
    if origin != "real_hardware": return {"decision":"material_candidate_inconclusive","physical_evidence":False,"reason":"data_origin is not real_hardware"}
    return {"decision":"blocked_pending_schema_Q0_and_traceability_validation","physical_evidence":False}

def report(name,text):
    p=REPORTS/name; p.write_text(text.rstrip()+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario=name,seed=None,kind="physical_execution_protocol_report")
def save_state(state):
    DATA.mkdir(exist_ok=True); p=DATA/"campaign_state.json"; p.write_text(json.dumps(state,indent=2)+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario="v0_6_pre_acquisition_state",seed=None,kind="physical_campaign_state")

def build_pre_acquisition_package():
    DATA.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True); state=campaign_state(); save_state(state)
    report("DEMONSTRATOR_A_V0_6_PREREGISTRATION.md",f"# Demonstrator A v0.6 preregistration\n\nProtocol `{protocol_id()}`. Q0, A0 and A1 require schema-valid real hardware data. Fixtures and emulators are forced to `material_candidate_inconclusive`. Tamesis, Mc, mu_T, visibility and A3/A4 are outside scope.\n")
    report("Q0_INSTRUMENT_QUALIFICATION.md","# Q0 instrument qualification\n\nStatus: `HARDWARE_QUALIFICATION_NOT_STARTED`. No instrument IDs, calibration certificates, uncertainties or traceability chains have been supplied. A1 is blocked.\n")
    report("REFERENCE_THERMOMETRY_TRACEABILITY.md","# Reference thermometry traceability\n\nStatus: not supplied. The primary reference must be traceable or independently compared before Q0 can pass. Stage, substrate and particle temperatures remain distinct.\n")
    report("THERMAL_STABILITY_DERIVATION.md","# Thermal stability derivation\n\nStatus: awaiting real time series. Slope, variance, Allan deviation, autocorrelation, mean changes and window stability cannot be derived from fixtures.\n")
    report("ABSOLUTE_READOUT_HEATING_BUDGET.md","# Absolute readout-heating budget\n\n`Delta T_max,budget` remains undefined. It must be derived from reference, gradient, stability, spectral, model, readout and repeatability covariance before locked A1 acquisition.\n")
    report("A0_PARTICLE_CHARACTERIZATION.md","# A0 particle characterization\n\nStatus: not started. Particles evaluated: 0. No material decision exists. Raw dark, background, spectra, power/field sweeps, stability and persistent identity are required.\n")
    report("A0_TO_A1_SELECTION.md","# A0 to A1 selection\n\nStatus: blocked. Allowed preliminary outcomes are advance_to_A1, repeat_A0, reject_candidate and inconclusive. A0 progression is not material selection.\n")
    report("A1_ACQUISITION_AUDIT.md","# A1 acquisition audit\n\nStatus: not started and blocked by Q0, traceability, absolute heating budget and stability criteria. No sweep data exist.\n")
    report("BLINDING_LEAKAGE_AUDIT.md","# Blinding leakage audit\n\nStatus: not run. Future audit must inspect filenames, paths, timestamps, controller labels, thermal metadata, material labels and sweep order before predictions.\n")
    report("LOCKED_MODEL_RECORD.md","# Locked model record\n\nStatus: no model selected or locked. Model hash, parameters and training freeze do not exist because no development data were supplied.\n")
    report("BLIND_TEMPERATURE_PREDICTIONS.md","# Blind temperature predictions\n\nPredictions: 0. Reveal is forbidden. Predictions cannot be edited after future freezing.\n")
    report("A1_BLIND_VALIDATION_RESULT.md","# A1 blind validation result\n\nStatus: not performed. Bias, RMSE, MAE, coverage, interval width, hysteresis and per-particle metrics are unavailable.\n")
    report("MATERIAL_CANDIDATE_DECISION.md","# Material candidate decision\n\nNo candidates evaluated. No material selected. Non-real data must return `material_candidate_inconclusive`; invalid hardware runs remain preserved as `calibration_run_invalid`.\n")
    report("DEMONSTRATOR_A_V0_6_LIMITATIONS.md","# Limitations\n\nNo real instrument, particle, calibration, thermal sweep, prediction or reveal is present. This protocol cannot generate physical evidence without externally supplied hardware data.\n")
    final=f"""A0_A1_HARDWARE_PACKAGE_READY_WITH_LIMITATIONS\n\n# Demonstrator A v0.6 execution report\n\nProtocol `{protocol_id()}`. Data origin is unset. Q0 is `HARDWARE_QUALIFICATION_NOT_STARTED`; A0 and A1 are not executed. Traceability, absolute readout-heating limit and empirical stability criteria are absent. There are zero particles, zero predictions and no reveal. A2 is blocked. This is the terminal computational state until real hardware data are supplied.\n"""
    report("DEMONSTRATOR_A_V0_6_EXECUTION_REPORT.md",final)
    return state

def verify_outputs():
    required=[REPORTS/"DEMONSTRATOR_A_V0_6_EXECUTION_REPORT.md",REPORTS/"Q0_INSTRUMENT_QUALIFICATION.md",REPORTS/"A1_BLIND_VALIDATION_RESULT.md",DATA/"campaign_state.json"]
    missing=[str(p) for p in required if not p.exists()]; return {"valid":not missing,"protocol_id":protocol_id(),"missing":missing,"physical_evidence":False}
if __name__=="__main__": print(json.dumps(build_pre_acquisition_package(),indent=2))
