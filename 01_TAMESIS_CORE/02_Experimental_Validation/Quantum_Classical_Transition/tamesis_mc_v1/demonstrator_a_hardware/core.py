from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import yaml
from synthetic_validation.provenance import write_sidecar
from synthetic_validation.protocol import BASE

CFG=BASE/"config/demonstrator_a_v0_5.yaml"; DATA=BASE/"data/demonstrator_a_v0_5"; REPORTS=BASE/"reports"; SCHEMAS=BASE/"schemas"
def cfg(): return yaml.safe_load(CFG.read_text(encoding="utf-8"))
def cfg_hash(): return hashlib.sha256(json.dumps(cfg(),sort_keys=True,separators=(",",":")).encode()).hexdigest()
def protocol_id(): return "tamesis-demonstrator-a-v0.5:"+cfg_hash()
def response(command,status,**extra): return {"protocol_id":protocol_id(),"command":command,"status":status,**extra}

def validate_protocol():
    c=cfg(); required={"Tamesis","Mc","mu_T","coherence_loss","interferometry","quantum_classical_identifiability"}; ok=required.issubset(set(c["scope_forbidden"])) and len(c["allowed_material_outcomes"])==4
    return response("validate_protocol","valid" if ok else "invalid",hardware_claim=False)
def register_particles(fixture=True): return response("register_particles","fixture_registered" if fixture else "awaiting_real_registry",material_decision="blocked")
def ingest_a0(fixture=True): return response("ingest_a0","fixture_ingested" if fixture else "awaiting_real_data",material_decision="blocked")
def audit_instrument(): return response("audit_instrument","not_hardware_audited",absolute_heating_budget="unresolved")
def ingest_a1(fixture=True): return response("ingest_a1","fixture_ingested" if fixture else "awaiting_real_data",blind_reveal="forbidden")
def fit_development_models(): return response("fit_development_models","hardware_placeholder_only",models=cfg()["gev_models"])
def lock_model(): return response("lock_model","model_structure_preregistered_hardware_parameters_missing")
def predict_blind_temperatures(): return response("predict_blind_temperatures","blocked_without_real_locked_validation")
def reveal_validation(): return response("reveal_validation","blocked_until_predictions_frozen")
def evaluate_material(fixture=True): return response("evaluate_material","material_candidate_inconclusive",reason="fixtures_cannot_select_material" if fixture else "real evaluation pipeline not yet run")

def checklist():
    items=["cryostat","reference_thermometry","thermal_control","optical_source","power_measurement","spectrometer","wavelength_reference","detector","field_control","timed_acquisition","particle_identification","dark_background_acquisition","raw_storage","calibration","failure_contingency"]
    return {"protocol_id":protocol_id(),"hardware_available":False,"items":[{"item":x,"specification_ready":True,"hardware_verified":False,"evidence":None} for x in items],"A0_package_ready":True,"A1_package_ready":False,"A1_blockers":["absolute readout-heating budget","reference instrument traceability","hardware stability thresholds"]}
def material_policy(): return {"allowed_run_outcomes":cfg()["allowed_material_outcomes"],"allowed_selection_outcomes":cfg()["selection_outcomes"],"simultaneous_gates":["adequate_signal","bounded_uncertainty","calibrated_coverage","acceptable_readout_heating","separable_cross_sensitivities","repeatable_response","valid_blind_reconstruction"],"aggregate_score_forbidden":True,"fixture_selection_forbidden":True}
def blind_registry(): return {"roles":cfg()["roles"],"hidden_from_blind_analyst":["true_setpoint","material_label_when_required","prior_quality_label","unregistered_manual_decision"],"leakage_checks":["filename","directory","timestamp_order","metadata","sweep_order"],"reveal_requires":"frozen prediction hashes"}
def instrument_registry(): return {"calibrations":["spectrometer_resolution","instrument_line_shape","laser_stability","wavelength_reference","detector_linearity","background","dark_counts","temporal_drift","saturation"],"status":"awaiting_hardware_records","linewidth_model":"L_observed = convolution(L_intrinsic,L_instrument)"}
def schema(extra):
    common={"record_id":{"type":"string"},"timestamp":{"type":"string"},"protocol_id":{"type":"string"},"particle_id":{"type":"string"},"input_hashes":{"type":"object"},"calibration_id":{"type":"string"},"instrument_state":{"type":"object"},"quality_flags":{"type":"array"},"units":{"type":"object"},"uncertainties":{"type":"object"}}
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":list(common)+extra,"properties":{**common,**{x:{} for x in extra}}}

def save_json(path,obj): path.parent.mkdir(exist_ok=True); path.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8"); write_sidecar(path,inputs=[CFG],scenario="demonstrator_a_v0_5",seed=cfg()["master_seed"],kind="a0_a1_hardware_package")
def report(name,text):
    p=REPORTS/name; p.write_text(text.rstrip()+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario=name,seed=cfg()["master_seed"],kind="a0_a1_hardware_report")

def build_package():
    DATA.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True); SCHEMAS.mkdir(exist_ok=True)
    save_json(DATA/"a0_a1_hardware_checklist.json",checklist()); save_json(DATA/"material_selection_policy.json",material_policy()); save_json(DATA/"blind_calibration_registry.json",blind_registry()); save_json(DATA/"instrument_calibration_registry.json",instrument_registry())
    for name,extra in {"particle_characterization_record":["material_family","synthesis_batch","color_center_type","morphology","mass_estimate","initial_spectrum"],"raw_spectral_record":["frequency_axis","raw_counts","integration_time","instrument_resolution","incident_power","particle_power_estimate","dark_spectrum","background_spectrum"],"instrument_calibration_record":["calibration_type","reference","parameters","validity_domain"],"thermal_equilibrium_record":["reference_temperature","reference_stability","spectral_stability","power_stability","heat_soak"],"thermal_sweep_record":["sweep_id","direction","setpoint_token","spectral_record_ids","power_levels"],"blind_temperature_prediction":["validation_token","temperature_prediction","prediction_uncertainty","model_lock_hash"],"blind_temperature_reveal":["validation_token","reference_temperature","prediction_hash"],"particle_selection_decision":["candidate","run_outcome","selection_outcome","gate_results","decision_authority"],"invalid_run_record":["run_id","invalid_reason","preserved_record_ids","protocol_violation"]}.items(): save_json(SCHEMAS/(name+".schema.json"),schema(extra))
    report("DEMONSTRATOR_A_V0_5_PREREGISTRATION.md",f"# Demonstrator A v0.5 preregistration\n\nProtocol `{protocol_id()}`. A0/A1 acquisition, roles, blinding, candidate models, nonbinary outcomes, exclusions and missing-data policies are frozen. No material is selected without real locked data.\n")
    report("A0_HARDWARE_RUNBOOK.md","# A0 hardware runbook\n\nRegister persistent particle identity; collect raw spectra, power sweeps, dark/background, field/strain responses and instrument calibrations for GeV, NV and an alternative candidate. Randomize power and preserve return-to-low-power measurements.\n")
    report("A1_HARDWARE_RUNBOOK.md","# A1 hardware runbook\n\nExecute ascending, descending and randomized hidden setpoint blocks between 5–20 K with heat soak determined by joint reference/spectrum/power stability. Freeze blind predictions before reference reveal.\n")
    report("THERMOMETRY_INDEPENDENCE_DOMAIN.md","# Independence domain\n\nGeV is independent from interferometric visibility. Heat-pulse calorimetry plus stage reference is independent-indirect only for A1/A2; independence is not established for A3/A4.\n")
    report("BLIND_CALIBRATION_CHALLENGE.md","# Blind calibration challenge\n\nSeparate operator, custodian, calibration analyst and blind analyst. Prevent leakage through filenames, directories, timestamps, metadata and deterministic sweep order. Reveal only after prediction hashes are frozen.\n")
    report("GEV_MODEL_SELECTION_POLICY.md","# GeV model selection\n\nCompare temperature-only baseline, temperature+power, temperature+power+strain and full preregistered model on distinct development, selection and locked datasets. Predictive validation outranks in-sample fit.\n")
    report("READOUT_HEATING_ACCEPTANCE.md","# Readout heating acceptance\n\nBoth conditions are mandatory: Delta T_readout <= 0.1 Delta T_step and Delta T_readout <= Delta T_max,budget. The absolute limit remains unresolved until the real instrument uncertainty budget is frozen, so A1 acquisition is not yet fully ready.\n")
    report("MATERIAL_SELECTION_POLICY.md","# Material selection policy\n\nAll gates must pass simultaneously; signal cannot compensate for non-identifiable cross-sensitivity. Run outcomes include selected, not selected, inconclusive and invalid. Selection for A2 does not authorize A3/A4.\n")
    report("A0_A1_HARDWARE_CHECKLIST.md","# Hardware checklist\n\nThe package specifies cryostat, traceable reference, thermal control, optical source, power metrology, spectrometer, wavelength reference, detector, field control, synchronized acquisition, particle identity, backgrounds, raw storage, calibration and failure contingency. Availability is not claimed.\n")
    report("A0_A1_DATA_MANAGEMENT_PLAN.md","# Data management plan\n\nPreserve raw spectra and counts, timestamps, powers, fields, reference temperatures, cryostat state, flags, exclusions and hashes. Separate instrument calibration, development, model selection and locked validation datasets.\n")
    report("DEMONSTRATOR_A_V0_5_LIMITATIONS.md","# Limitations\n\nNo hardware inventory, traceability certificate, real calibration data or absolute heating budget has been supplied. Fixtures can exercise commands but cannot select a material.\n")
    final=f"""A0_A1_HARDWARE_PACKAGE_READY_WITH_LIMITATIONS\n\n# Demonstrator A v0.5 execution report\n\nProtocol `{protocol_id()}`. A0 acquisition can begin once hardware availability is confirmed. A1 remains limited by the unresolved absolute readout-heating budget and real reference-instrument traceability. Four nonbinary run outcomes are implemented. The stationary secondary channel is independent only for A1/A2. No material selection or thermometry demonstration is claimed.\n"""
    report("DEMONSTRATOR_A_V0_5_EXECUTION_REPORT.md",final)
    return response("build_package","A0_A1_HARDWARE_PACKAGE_READY_WITH_LIMITATIONS",A0_ready=True,A1_ready=False,material_decision="blocked")

def verify_outputs():
    required=[REPORTS/"DEMONSTRATOR_A_V0_5_EXECUTION_REPORT.md",DATA/"a0_a1_hardware_checklist.json",DATA/"material_selection_policy.json",SCHEMAS/"raw_spectral_record.schema.json",SCHEMAS/"blind_temperature_prediction.schema.json"]
    missing=[str(p) for p in required if not p.exists()]; return response("verify_outputs","valid" if not missing else "invalid",missing=missing)
