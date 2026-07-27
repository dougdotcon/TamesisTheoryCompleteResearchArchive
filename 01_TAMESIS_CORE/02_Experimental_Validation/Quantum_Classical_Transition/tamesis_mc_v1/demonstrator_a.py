from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import numpy as np, yaml
from synthetic_validation.provenance import write_sidecar
from synthetic_validation.protocol import BASE

CFG=BASE/"config/demonstrator_a_v0_4.yaml"; DATA=BASE/"data/demonstrator_a_v0_4"; REPORTS=BASE/"reports"; SCHEMAS=BASE/"schemas"
def cfg(): return yaml.safe_load(CFG.read_text(encoding="utf-8"))
def cfg_hash(): return hashlib.sha256(json.dumps(cfg(),sort_keys=True,separators=(",",":")).encode()).hexdigest()
def protocol_id(): return "tamesis-demonstrator-a-v0.4:"+cfg_hash()

def method_registry():
    return [
      {"method":"GeV_optical","role":"primary","independence":"interferometer_independent_direct_candidate","range":"5-20 K target; stationary component evidence only","readout":"linewidth+line position+intensity","status":"plausible_not_hardware_validated"},
      {"method":"controlled_heat_pulse_calorimetry","role":"secondary","independence":"independent_indirect","range":"A1-A2 stationary","readout":"known energy input+thermal relaxation","status":"protocol_ready"},
      {"method":"stage_equilibrium_reference","role":"secondary_A1","independence":"independent_direct_reference_after_equilibrium_test","range":"5-20 K stationary","readout":"traceable stage thermometer","status":"protocol_ready"},
      {"method":"NV_optical_spin","role":"sensitivity","independence":"partially_shared_model","range":"higher-temperature cross-check","readout":"optical/spin response","status":"limited_target_range"},
      {"method":"COM_dynamics","role":"sensitivity","independence":"non_independent","range":"suspension/levitation","readout":"damping/fluctuation","status":"cannot_satisfy_triangulation_alone"},
      {"method":"thermal_emission","role":"secondary_candidate","independence":"independent_indirect","range":"signal-limited at cryogenic T","readout":"spectrum/radiance","status":"conceptual_only"},
      {"method":"sacrificial_matched_particle","role":"secondary_A3_A4","independence":"independent_indirect","range":"population transfer","readout":"matched calibration particle","status":"requires_transfer_validation"},
      {"method":"thermal_image_force","role":"secondary_candidate","independence":"conceptual_only","range":"unknown","readout":"image-force/displacement","status":"conceptual_only"},
    ]

def gate_registry():
    return [
      {"gate":"A0","objective":"material characterization","entry":"raw candidate particles","success":"select at least one particle-specific candidate with separable signal and acceptable readout power","failure":"no candidate supports secondary validation","current_status":"ready_to_start_hardware"},
      {"gate":"A1","objective":"stationary equilibrium calibration 5-20 K","entry":"A0 selected candidate","success":"locked up/down sweep, equilibrium verified, coverage 90-98%, agreement <=2 combined sigma","failure":"hysteresis/cross-sensitivity or gradient unresolved","current_status":"ready_to_start_after_A0"},
      {"gate":"A2","objective":"stationary transient calibration","entry":"A1 passed","success":"tau_th, readout heating, R_th and C_eff recovered on locked pulses","failure":"inverse model fails or readout heating >10% calibrated step","current_status":"protocol_ready_hardware_pending"},
      {"gate":"A3","objective":"20-77 K suspension/levitation integration","entry":"A0-A2 passed","success":"calibration transfer and low perturbation demonstrated","failure":"spectral response or thermal model does not transfer","current_status":"new_integration_required"},
      {"gate":"A4","objective":"5-20 K levitated thermometry","entry":"A0-A3 passed","success":"two-channel triangulation, tau_th and total uncertainty demonstrated","failure":"no independent secondary channel or calibration transfer","current_status":"blocked_by_A3_and_hardware"},
    ]

def thermal_models():
    return [
      {"model":"single_node_thermal","state":"T_int","forward":"C_eff(T)dT/dt=P_abs+P_readout+P_mw+P_technical-P_gas-P_rad-P_other","selection":"baseline only","risk":"misses internal gradients"},
      {"model":"core_surface_two_node","state":"T_core,T_surface","forward":"coupled capacities and core-surface conductance","selection":"preferred if locked residuals show two scales","risk":"parameter correlation"},
      {"model":"multi_timescale_empirical","state":"T_int plus empirical modes","forward":"sum of calibrated relaxation modes","selection":"sensitivity model, never selected only by fit score","risk":"poor physical extrapolation"},
    ]

def cross_sensitivities():
    names=["magnetic_field","magnetic_gradient","strain","orientation","charge","spectral_diffusion","optical_power","microwave_power","pressure","gas_composition","vibration","motion","trap_position","color_center_state"]
    return [{"variable":n,"derivative":"calibrate partial dz_GeV/partial "+n,"can_mimic_temperature":n in {"strain","spectral_diffusion","optical_power","magnetic_field","charge"},"required_intervention":"orthogonal sweep and locked holdout","status":"not_measured"} for n in names]

def synthetic_fixture():
    rng=np.random.default_rng(cfg()["master_seed"]); times=np.linspace(0,1,101); tau=.18; base=10.; step=4.; truth=base+step*np.exp(-times/tau); observed=truth+rng.normal(0,.12,len(times)); estimate=observed.copy(); return {"fixture_only":True,"hardware_placeholder":True,"truth_hidden_during_inverse_fit":True,"time_s":times.tolist(),"recorded_proxy":observed.tolist(),"reconstructed_temperature_k":estimate.tolist(),"reference_sha256":hashlib.sha256(truth.tobytes()).hexdigest(),"tau_th_fixture_s":tau}

def go_no_go_rows():
    return [{"gate":g["gate"],"criterion":g["success"],"threshold_source":"previous decision-oriented error budget + combined uncertainty agreement","evidence_required":"real raw hardware data","status":"not_evaluated_hardware"} for g in gate_registry()]

def schema(name,extra):
    base={"record_id":{"type":"string"},"timestamp":{"type":"string"},"protocol_id":{"type":"string"},"particle_id":{"type":"string"},"units":{"type":"object"},"uncertainties":{"type":"object"},"calibration_id":{"type":"string"},"status":{"type":"string"},"provenance_hash":{"type":"string"}}
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","required":list(base)+extra,"properties":{**base,**{x:{} for x in extra}}}

def ingest_raw_calibration(record): return dict(record)
def validate_units(record):
    if not record.get("units"): raise ValueError("formal units required")
    return record
def fit_forward_model(record): return {"model":"hardware_placeholder","parameters":{},"status":"not_hardware_fitted"}
def fit_inverse_model(record): return {"temperature_estimate":None,"status":"requires_calibration"}
def cross_validate(model,validation): return {"status":"not_evaluated_without_hardware"}
def estimate_thermal_time_constant(record): return {"tau_th":None,"status":"requires_A2"}
def estimate_readout_heating(record): return {"delta_T_readout":None,"status":"requires_A2"}
def compare_thermometers(primary,secondary): return {"agreement_sigma":None,"status":"requires_two_real_channels"}
def generate_uncertainty_budget(record): return {"status":"requires_hardware_covariance"}
def evaluate_go_no_go(evidence): return "not_evaluated_hardware"

def save_json(name,obj):
    DATA.mkdir(exist_ok=True); p=DATA/name; p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario="demonstrator_a_v0_4",seed=cfg()["master_seed"],kind="demonstrator_a_data")
def save_csv(name,rows):
    DATA.mkdir(exist_ok=True); p=DATA/name
    with p.open("w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    write_sidecar(p,inputs=[CFG],scenario="demonstrator_a_v0_4",seed=cfg()["master_seed"],kind="demonstrator_a_data")
def report(name,text):
    REPORTS.mkdir(exist_ok=True); p=REPORTS/name; p.write_text(text.rstrip()+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario=name,seed=cfg()["master_seed"],kind="demonstrator_a_report")

def main():
    methods=method_registry(); gates=gate_registry(); models=thermal_models(); cross=cross_sensitivities(); fixture=synthetic_fixture(); gonogo=go_no_go_rows()
    save_json("thermometry_method_registry.json",methods); save_json("a0_a4_gate_registry.json",gates); save_json("thermal_model_registry.json",models); save_csv("thermometry_cross_sensitivities.csv",cross); save_csv("demonstrator_a_go_no_go.csv",gonogo); save_json("demonstrator_a_locked_synthetic_fixture.json",fixture)
    SCHEMAS.mkdir(exist_ok=True)
    for name,extra in {"stationary_calibration_record":["stage_temperature","particle_spectrum","heat_soak_duration"],"thermal_step_record":["input_power","pulse_duration","spectral_time_series"],"spectral_record":["wavelength_axis","raw_counts","excitation_power","magnetic_field","strain_proxy"],"levitation_thermometry_record":["trap_state","particle_spectrum","motion_record","readout_power","environment"]}.items():
        p=SCHEMAS/(name+".schema.json"); p.write_text(json.dumps(schema(name,extra),indent=2)+"\n",encoding="utf-8"); write_sidecar(p,inputs=[CFG],scenario="demonstrator_a_schema",seed=cfg()["master_seed"],kind="demonstrator_a_schema")
    report("DEMONSTRATOR_A_V0_4_PREREGISTRATION.md",f"# Demonstrator A v0.4 preregistration\n\nProtocol `{protocol_id()}`. This protocol prohibits Tamesis inference, mu_T, H0/H1 and use of visibility as a thermometer. Only real audited hardware data can support a future demonstration claim.\n")
    report("THERMOMETRY_METHOD_SELECTION.md","# Thermometry method selection\n\nGeV optical thermometry is the primary candidate for 5-20 K. Controlled heat-pulse calorimetry and a traceable stage-equilibrium reference provide the stationary secondary path. COM dynamics cannot count as independent triangulation.\n")
    report("GEV_PRIMARY_THERMOMETER_MODEL.md","# GeV primary thermometer model\n\nThe forward model includes temperature, linewidth, line position, intensity, spectral diffusion, strain, charge, field, orientation, laser power, background and particle variation. No hardware calibration is claimed.\n")
    report("SECONDARY_THERMOMETRY_CANDIDATES.md","# Secondary candidates\n\nHeat-pulse calorimetry is independent-indirect; stage equilibrium is an independent reference only after equilibrium is demonstrated; sacrificial matched particles require transfer validation; thermal emission and image-force methods remain conceptual.\n")
    report("THERMOMETRY_INDEPENDENCE_AUDIT.md","# Independence audit\n\n`interferometer_independent_thermometry` means the estimate does not use visibility, coherence loss, Gamma_T, mu_T or H0/H1. Physical location inside the particle is allowed.\n")
    report("THERMAL_TIME_CONSTANT_PROTOCOL.md","# Thermal time-constant protocol\n\nA2 applies randomized locked heat pulses and compares one-node, two-node and multi-timescale models on held-out transients. Sampling, latency and pre/post versus continuous readout are derived only after tau_th is measured.\n")
    report("READOUT_HEATING_PROTOCOL.md","# Readout heating protocol\n\nContinuous, pulsed, pre/post, interleaved and low-duty readout are compared. Delta T_readout, microwave heating and optical-power slopes are measured; the method cannot pass by hiding heating in calibration.\n")
    report("PARTICLE_SPECIFIC_CALIBRATION.md","# Particle-specific calibration\n\nEvery particle preserves mass, geometry, defect center, spectrum, strain, absorption, effective emissivity, response and calibration history. Population averages are sensitivity checks only.\n")
    report("A0_A4_GATE_SPECIFICATION.md","# A0-A4 gates\n\nA0 material → A1 stationary equilibrium → A2 stationary transient → A3 20-77 K suspension/levitation → A4 5-20 K levitation. No gate may be skipped.\n")
    report("THERMOMETRY_GO_NO_GO_CRITERIA.md","# Go/no-go criteria\n\nAgreement is fixed at two combined standard uncertainties; coverage must remain 90-98%; mass/power residual slopes must include zero; readout heating must remain below 10% of the calibrated thermal step. Absolute temperature precision remains to be derived from A1/A2 hardware covariance.\n")
    report("DEMONSTRATOR_A_HARDWARE_DATA_REQUIREMENTS.md","# Hardware data requirements\n\nPreserve raw spectra, counts, timestamps, powers, fields, pressure, reference temperatures, trap state, exclusions and calibration provenance. Estimated temperatures alone are insufficient.\n")
    report("DEMONSTRATOR_A_LIMITATIONS.md","# Limitations\n\nGeV has not been demonstrated in the target levitated protocol. The secondary channel for A4 is not yet proven independent and transfer from stationary calibration to levitation is unknown. Synthetic fixtures only verify software plumbing.\n")
    final=f"""DEMONSTRATOR_A_PROTOCOL_READY_WITH_LIMITATIONS\n\n# Demonstrator A v0.4 execution report\n\nProtocol `{protocol_id()}`. A0 and A1 can begin with a stationary particle and existing component-level methods; A2 is protocol-ready after A1. A3 and A4 require new integration and cannot start. GeV is the primary candidate; controlled heat-pulse calorimetry plus stage equilibrium are the stationary secondary route. No internal thermometry demonstration is claimed.\n\n| Question | Result | Limitation |\n|---|---|---|\n| GeV plausible primary? | Yes, component-level | not levitated |\n| Independent secondary? | Yes for A1/A2 | A4 route unproven |\n| Start at 5 K? | No | start 20-77 K integration after stationary 5-20 K calibration |\n| A0/A1 executable? | Yes | hardware/data required |\n| tau_th measurable? | Protocol defined | no real transient yet |\n| Pre/post sufficient? | Conditional on tau_th >> experiment time | tau_th unknown |\n| Individual calibration? | Mandatory | population transfer risky |\n| A3/A4 need development? | Yes | integration blocker |\n"""
    report("DEMONSTRATOR_A_V0_4_EXECUTION_REPORT.md",final)
    print(json.dumps({"protocol_id":protocol_id(),"conclusion":"DEMONSTRATOR_A_PROTOCOL_READY_WITH_LIMITATIONS","methods":len(methods),"gates":len(gates),"schemas":4},indent=2))
if __name__=="__main__": main()
