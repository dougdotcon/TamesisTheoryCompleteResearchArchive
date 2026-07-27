from dataclasses import replace
import math

from synthetic_validation.generator import generate_observation
from synthetic_validation.inference import infer_observation
from synthetic_validation.protocol import config_payload, scenario_grid


def test_protocol_is_bound_to_frozen_contract():
    cfg = config_payload()
    assert cfg["tamesis_contract_hash"] == "d3d9b22cdb62a335a9cfe14d4a066d7f4ea314881892453e7594b3fa7a546d0e"
    assert cfg["models"]["rivals"] == "exploratory_non_authoritative_comparison"


def test_generator_is_seed_deterministic():
    scenario = scenario_grid("quick", truth_model="null")[0]
    assert generate_observation(scenario, 7, master_seed=20260726) == generate_observation(scenario, 7, master_seed=20260726)


def test_blind_inference_needs_no_truth_fields():
    scenario = scenario_grid("quick", truth_model="tamesis")[-1]
    obs = generate_observation(scenario, 3, master_seed=20260726)
    result = infer_observation({k: v for k, v in obs.items() if not k.startswith("truth_")})
    assert result["truth_model"] == "hidden"
    assert math.isfinite(result["likelihood_ratio"])


def test_strong_injection_has_positive_official_rate():
    scenario = next(s for s in scenario_grid("quick", truth_model="tamesis") if s.family == "C_above_threshold" and s.mass_ratio >= 2)
    assert generate_observation(scenario, 2, master_seed=20260726)["truth_gamma_t_s-1"] > 0


def test_truth_switch_changes_generator_truth_only():
    base = scenario_grid("quick", truth_model="null")[0]
    alt = replace(base, truth_model="tamesis")
    assert generate_observation(base, 0, master_seed=1)["truth_model"] == "null"
    assert generate_observation(alt, 0, master_seed=1)["truth_model"] == "tamesis"
