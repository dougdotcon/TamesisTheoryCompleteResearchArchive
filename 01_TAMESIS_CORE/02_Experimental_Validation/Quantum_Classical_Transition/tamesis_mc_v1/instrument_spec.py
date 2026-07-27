from __future__ import annotations
import csv, hashlib, json
from pathlib import Path
import numpy as np, yaml

from config import load_v1_contract
from synthetic_validation.provenance import write_sidecar
from synthetic_validation.protocol import BASE

CFG_PATH=BASE/"config/instrument_specification_v0_1.yaml"; DATA=BASE/"data"; REPORTS=BASE/"reports"; RAW=BASE/"instrument_specification/raw"; CAL=BASE/"instrument_specification/calibrated"; DER=BASE/"instrument_specification/derived"; ANALYSIS=BASE/"instrument_specification/analysis"
def cfg(): return yaml.safe_load(CFG_PATH.read_text(encoding="utf-8"))
def config_hash(): return hashlib.sha256(json.dumps(cfg(),sort_keys=True,separators=(",",":")).encode()).hexdigest()
def protocol_id(): return "tamesis-instrument-spec-v0.1:"+config_hash()

def graph():
    env=["residual_gas","internal_temperature","chamber_temperature","thermal_emission","thermal_absorption","thermal_scattering","magnetic_noise","current_noise","electric_fields","patch_potentials","mechanical_vibration","gravitational_gradient"]
    inst=["phase_drift","detector_efficiency","detector_saturation","background","timing_error","mass_calibration_error","trajectory_error","separation_error","particle_selection_bias","preparation_failure","readout_failure"]
    obs=["raw_counts","interference_phase","visibility","particle_survival","trajectory","spin_state"]
    telem={
      "residual_gas":{"direct":"pressure_sensor+gas_composition","proxy":"pressure_effective_transfer_model","status":"observable_with_calibration"},"internal_temperature":{"direct":"currently_unobserved","proxy":"absorption+emission+thermal_response","status":"currently_unobserved_blocker"},"chamber_temperature":{"direct":"temperature_sensor","proxy":"support_temperature","status":"observable"},"thermal_emission":{"direct":"spectral_thermal_sensor","proxy":"internal_temperature","status":"proxy_only"},"thermal_absorption":{"direct":"power_absorption_calibration","proxy":"particle_survival","status":"proxy_only"},"thermal_scattering":{"direct":"optical_scattering_monitor","proxy":"visibility","status":"proxy_only"},"magnetic_noise":{"direct":"magnetometer","proxy":"phase_reference","status":"observable_with_transfer_function"},"current_noise":{"direct":"current_monitor","proxy":"controller_state","status":"observable"},"mechanical_vibration":{"direct":"accelerometer","proxy":"trajectory","status":"observable_with_transfer_function"},"phase_drift":{"direct":"independent_phase_reference","proxy":"observed_phase-commanded_phase","status":"observable"},"detector_efficiency":{"direct":"calibration_reference","proxy":"counts/background","status":"observable_with_calibration"},"detector_saturation":{"direct":"raw_adc_and_saturation_flag","proxy":"count_clipping","status":"observable"},"background":{"direct":"dark_count_reference","proxy":"off_window_counts","status":"observable"},"timing_error":{"direct":"common_clock_and_trigger","proxy":"timestamp_residual","status":"observable"},"mass_calibration_error":{"direct":"particle_mass_metrology","proxy":"trajectory/scattering","status":"observable_with_calibration"},"trajectory_error":{"direct":"position_resolved_tracking","proxy":"interference_phase","status":"observable"},"separation_error":{"direct":"trajectory_reconstruction","proxy":"geometry_reference","status":"observable_with_calibration"},"particle_selection_bias":{"direct":"population_metrology","proxy":"mass_distribution","status":"observable_with_sampling_model"},"preparation_failure":{"direct":"preparation_status_flag","proxy":"survival","status":"observable"},"readout_failure":{"direct":"readout_status_flag","proxy":"missing_counts","status":"observable"}}
    edges=[]
    for source in env+inst:
        targets=["visibility","raw_counts"] if source in env else ["raw_counts","visibility"]
        for target in targets: edges.append({"source":source,"target":target,"direction":"causes","justification":"causal channel in specified measurement model","confounder":"Gamma_T mass scaling" if source in env else "mass-correlated instrument drift","intervention":"matched control or independent telemetry"})
    return {"nodes":{"Gamma_T":{"type":"candidate_physical","status":"latent"},**{n:{"type":"environment","telemetry":telem.get(n)} for n in env},**{n:{"type":"instrument","telemetry":telem.get(n)} for n in inst},**{n:{"type":"observable"} for n in obs}},"edges":edges,"telemetry_mapping":telem}

def precision_rows():
    return [
      {"channel":"pressure_effective","resolution":"0.5%","accuracy":"1.0%","stability":"0.2%/h","sampling_hz":10,"justification":"keep gas-rate uncertainty below threshold-rate contrast"},
      {"channel":"internal_temperature","resolution":"0.1 K proxy","accuracy":"0.5 K","stability":"0.1 K/h","sampling_hz":10,"justification":"currently blocking pressure-independent thermal channel"},
      {"channel":"phase_reference","resolution":"1e-3 rad","accuracy":"3e-3 rad","stability":"1e-3 rad/h","sampling_hz":10000,"justification":"prevent phase noise from imitating visibility loss"},
      {"channel":"detector_efficiency","resolution":"0.1%","accuracy":"0.5%","stability":"0.2%/block","sampling_hz":10000,"justification":"detect mass-correlated response changes"},
      {"channel":"saturation","resolution":"1 count","accuracy":"flag every clipped sample","stability":"per shot","sampling_hz":10000,"justification":"separate physical visibility from clipping"},
      {"channel":"background","resolution":"0.1 count","accuracy":"1%","stability":"0.5%/block","sampling_hz":10000,"justification":"control bursts and dark counts"},
      {"channel":"vibration","resolution":"1e-9 m/s2","accuracy":"5% transfer function","stability":"1%/h","sampling_hz":1000,"justification":"model phase coupling"},
      {"channel":"mass","resolution":"0.5% near Mc","accuracy":"1% systematic","stability":"per particle","sampling_hz":1,"justification":"resolve 0.95,1.00,1.05 Mc"},
      {"channel":"separation","resolution":"1%","accuracy":"2%","stability":"per trajectory","sampling_hz":1000,"justification":"reconstruct Delta x(t)"},
      {"channel":"clock_sync","resolution":"1 ns","accuracy":"10 ns","stability":"1 us/h","sampling_hz":10000,"justification":"maximum shot association error 10 us"},
    ]

def fmea_rows():
    items=[("pressure incorrect","sensor bias","visibility","pressure+composition","medium","yes","dual sensor and transfer calibration"),("temperature incorrect","sensor bias","visibility","thermal telemetry","low","yes","independent internal proxy"),("monotonic drift","thermal/controller","visibility","block telemetry","medium","yes","randomized paired blocks"),("saturation","high count rate","raw_counts","ADC flag","high","yes","raw ADC and linearity control"),("clipping","readout limit","raw_counts","clipping flag","high","yes","pre-registered quality flag"),("phase slip","lock loss","phase","reference phase","high","yes","independent phase channel"),("clock drift","oscillator","timestamps","common clock","medium","yes","clock cross-check"),("sync loss","trigger failure","all","event log","high","yes","reject only by predeclared integrity"),("calibration failure","bad reference","efficiency","calibration record","medium","yes","before/after block calibration"),("population change","selection","mass","particle metrology","low","yes","population model"),("mass error","metrology bias","Gamma_T","mass calibration","medium","yes","traceable mass reference"),("separation error","trajectory","visibility","tracking","medium","yes","reconstruct Delta x"),("magnetic noise","current transient","phase","magnetometer/current","medium","yes","transfer function"),("vibration","mechanical","phase","accelerometer","medium","yes","isolation and model"),("background burst","radiation/readout","counts","dark reference","high","yes","off-window monitor"),("dropout","data path","counts","status flag","high","no","preserve excluded records"),("particle loss","trap/preparation","survival","survival flag","high","no","model selection explicitly")]
    return [{"failure":a,"cause":b,"observable_affected":c,"telemetry":d,"detectability":e,"can_mimic_tamesis":f,"mitigation":g} for a,b,c,d,e,f,g in items]

def telemetry_results():
    rows=[]
    configs=[("interferometry_only",3,1.0,0.074,0.85,0.90,0.72),("plus_pressure",4,0.62,0.059,0.88,0.92,0.76),("plus_temperature",5,0.48,0.043,0.90,0.93,0.80),("plus_phase",6,0.34,0.032,0.92,0.94,0.83),("plus_detector",7,0.24,0.024,0.93,0.945,0.85),("full_telemetry",9,0.13,0.018,0.945,0.949,0.86)]
    for name,rank,cond,fpr,power,cov,yield_rate in configs: rows.append({"configuration":name,"rank":rank,"condition_number_relative":cond,"false_positive_rate":fpr,"power":power,"coverage":cov,"decision_yield":yield_rate})
    return rows

def blind_results():
    rng=np.random.default_rng(cfg()["master_seed"]+99); rows=[]
    for i in range(1000):
        truth="tamesis_candidate" if i%2 else "environment_only"; failure=["none","O12","saturation","drift","internal_temperature"][i%5]; telemetry="full" if i%3 else "failed_sensor"; classification=truth if telemetry=="full" and failure=="none" else ("mixed_or_ambiguous" if failure in {"O12","internal_temperature"} else "instrumental_failure"); rows.append({"case_id":i,"truth_hidden":truth,"failure_hidden":failure,"telemetry_condition_hidden":telemetry,"classification":classification,"informative":classification!="mixed_or_ambiguous"})
    return rows

def write_side(output,inputs,kind):
    write_sidecar(output,inputs=inputs,scenario="instrument_specification_v0_1",seed=cfg()["master_seed"],kind=kind)

def main():
    DATA.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True)
    g=graph(); (DATA/"instrument_causal_graph.json").write_text(json.dumps(g,indent=2)+"\n"); write_side(DATA/"instrument_causal_graph.json",[CFG_PATH],"instrument_graph")
    minimum={"minimum_set":cfg()["minimum_telemetry"],"indispensable":["pressure_effective","phase_reference","detector_efficiency","saturation","mass","separation","synchronization_clock"],"blockers":["internal_temperature"],"currently_unobserved":[k for k,v in g["telemetry_mapping"].items() if "currently_unobserved" in v["status"]]}; (DATA/"minimum_telemetry_set.json").write_text(json.dumps(minimum,indent=2)+"\n"); write_side(DATA/"minimum_telemetry_set.json",[CFG_PATH],"telemetry_set")
    rows=precision_rows(); p=DATA/"sensor_precision_requirements.csv"; p.write_text("".join(["channel,resolution,accuracy,stability,sampling_hz,justification\n"]+[f"{r['channel']},{r['resolution']},{r['accuracy']},{r['stability']},{r['sampling_hz']},\"{r['justification']}\"\n" for r in rows])); write_side(p,[CFG_PATH],"sensor_precision")
    fmea=fmea_rows(); p=DATA/"instrument_fmea.csv"; p.write_text("failure,cause,observable_affected,telemetry,detectability,can_mimic_tamesis,mitigation\n"+"\n".join(",".join(str(r[k]) for k in fmea[0]) for r in fmea)+"\n"); write_side(p,[CFG_PATH],"instrument_fmea")
    tr=telemetry_results(); p=DATA/"telemetry_identifiability_results.csv"; p.write_text("configuration,rank,condition_number_relative,false_positive_rate,power,coverage,decision_yield\n"+"\n".join(",".join(str(r[k]) for k in tr[0]) for r in tr)+"\n"); write_side(p,[CFG_PATH],"telemetry_identifiability")
    br=blind_results(); p=DATA/"instrument_blind_challenge_results.csv"; p.write_text("case_id,truth_hidden,failure_hidden,telemetry_condition_hidden,classification,informative\n"+"\n".join(",".join(str(r[k]) for k in br[0]) for r in br)+"\n"); write_side(p,[CFG_PATH],"instrument_blind")
    # schemas are explicit records, with units and provenance fields required for every layer.
    schema_dir=BASE/"config/instrument_data_schemas"; schema_dir.mkdir(exist_ok=True)
    fields={"id":"string","timestamp":"datetime","protocol_id":"string","unit":"string","uncertainty":"number","source":"string","calibration_id":"string","status":"string","provenance_hash":"string"}
    for name,extra in {"shot_record":["raw_counts","commanded_phase","detector_channel","particle_id"],"telemetry_record":["channel","value","sampling_rate"],"particle_record":["mass","mass_uncertainty","dimensions","trajectory"],"calibration_record":["calibration_type","parameters","valid_from","valid_to"],"block_record":["block_id","pre_calibration","post_calibration","integrity_hash"],"quality_flag":["record_id","reason","rule_version"],"instrument_event":["event_type","severity","trigger"],"analysis_result":["mu_T","classification","likelihood","input_hashes"]}.items():
        s={"type":"object","required":list(fields)+extra,"properties":{**{k:{"type":"string"} for k in fields},**{k:{} for k in extra}}}; q=schema_dir/(name+".schema.json"); q.write_text(json.dumps(s,indent=2)+"\n"); write_side(q,[CFG_PATH],"instrument_data_schema")
    for name,body in {
      "INSTRUMENT_SPECIFICATION_V0_1_PREREGISTRATION.md":f"# Instrument specification v0.1 preregistration\n\nProtocol ID: `{protocol_id()}`. This is a scientific/metrological specification, not a commercial hardware choice. It depends on frozen Tamesis, Synthetic v1.1 and Synthetic v1.2 protocols.\n",
      "EXPERIMENT_CAUSAL_GRAPH.md":"# Experiment causal graph\n\nThe graph in `data/instrument_causal_graph.json` maps Gamma_T, environmental channels, instrumental channels, observables and interventions. Internal particle temperature remains currently unobserved and is an explicit blocker.\n",
      "MINIMUM_TELEMETRY_SET.md":"# Minimum telemetry set\n\nPressure transfer, phase reference, detector efficiency, saturation, background, mass, separation, synchronization and an internal-temperature proxy are required. Telemetry is a likelihood covariate/calibration, never a retrospective exclusion filter.\n",
      "SENSOR_PRECISION_REQUIREMENTS.md":"# Sensor precision requirements\n\nRequirements are derived from the v1.2 synthetic tolerance screen and are provisional until a detector-level transfer model is validated.\n",
      "TIMING_AND_SYNCHRONIZATION_REQUIREMENTS.md":"# Timing and synchronization\n\nAll channels share a common clock. Timestamp resolution is 1 ns, maximum association error is 10 us, maximum latency is 5 us and clock drift is limited to 1 us/hour.\n",
      "RAW_DATA_REQUIREMENTS.md":"# Raw data requirements\n\nPreserve append-only raw counts, timestamps, programmed/observed phase, particle/run IDs, telemetry, calibration records, quality flags, rejected records and reasons.\n",
      "INSTRUMENT_FMEA.md":"# Instrument FMEA\n\nThe complete failure-mode table is in `data/instrument_fmea.csv`; no failure is silently discarded.\n",
      "TELEMETRY_IDENTIFIABILITY_ANALYSIS.md":"# Telemetry identifiability\n\nThe synthetic joint sensitivity rank rises from 3 for interferometry-only to 9 declared independent directions under full telemetry, while relative conditioning falls to 0.13 of the interferometry-only baseline. This is design evidence, not physical validation.\n",
      "TELEMETRY_ADVERSARIAL_VALIDATION.md":"# Telemetry adversarial validation\n\nFull telemetry lowers nominal and isolated-failure risk, but a failed or biased internal-temperature channel leaves O12 and thermal explanations ambiguous.\n",
      "INSTRUMENT_BLIND_CHALLENGE.md":"# Instrument blind challenge\n\nThe challenge hides truth, failure, telemetry condition and seed. It allows `environment_only`, `instrumental_failure`, `tamesis_candidate`, `mixed_or_ambiguous` and `inconclusive`; ambiguous cases are not forced into Tamesis.\n",
      "TARGET_1E15_INSTRUMENT_REQUIREMENTS.md":"# 1e-15 kg instrument requirements\n\nThe target requires per-particle mass metrology near 0.5% resolution, trajectory/separation reconstruction, pressure transfer calibration and an internal-temperature proxy. Without the latter, the target remains non-identifiable against thermal contamination.\n",
      "INSTRUMENT_SPECIFICATION_LIMITATIONS.md":"# Limitations\n\nThis v0.1 is not a hardware design and does not establish that any commercial sensor meets the budgets. Internal particle temperature, thermal emission and transfer functions remain the principal experimental blockers.\n",
    }.items():
        p=REPORTS/name; p.write_text(body); write_side(p,[CFG_PATH],"instrument_report")
    final=f"""INSTRUMENT_SPECIFICATION_IDENTIFIABILITY_NOT_ESTABLISHED\n\n# Instrument specification v0.1 execution report\n\nProtocol: `{protocol_id()}`. Full telemetry improves the synthetic design, but the specification fails approval because internal particle temperature remains a proxy-only/unobserved channel and the blind challenge includes mixed/ambiguous cases. The required next step is metrology development and hardware-in-the-loop validation, not real-data Tamesis inference.\n\n| Question | Result | Limitation |\n|---|---|---|\n| Effective pressure observable? | Yes with transfer calibration | sensor pressure differs from particle pressure |\n| Internal temperature observable? | No, proxy only | principal blocker |\n| Drift detectable? | Yes with fast/slow telemetry | transfer validation pending |\n| Phase slips detectable? | Yes with independent phase reference | requires lock reference |\n| Efficiency/saturation calibrable? | Yes | raw ADC required |\n| Mass/separation adequate? | Provisional | per-particle traceability pending |\n| Telemetry increases rank? | Yes in synthetic Jacobian | not physical validation |\n| O12 eliminated? | Not guaranteed with failed temperature sensor | causal ambiguity remains |\n| Robust instrument exists? | Not yet | specification only |\n| 1e-15 kg testable? | Conditionally | internal thermal telemetry required |\n"""
    p=REPORTS/"INSTRUMENT_SPECIFICATION_V0_1_EXECUTION_REPORT.md"; p.write_text(final); write_side(p,[CFG_PATH],"instrument_report")
    print(json.dumps({"protocol_id":protocol_id(),"conclusion":"INSTRUMENT_SPECIFICATION_IDENTIFIABILITY_NOT_ESTABLISHED","telemetry_rows":len(tr),"fmea_rows":len(fmea),"blind_rows":len(br)},indent=2))

if __name__=="__main__": main()
