from __future__ import annotations

import json
from math import exp, pi
from pathlib import Path
from typing import Any
from functools import lru_cache

import numpy as np

from environment_model import Environment
from mc_model import McModel

from .protocol import Scenario, derive_seed


def _environment_rate(mass_kg: float, pressure_pa: float, gas_temperature_k: float, *, wrong_species: bool = False) -> float:
    env = Environment(
        pressure_pa=pressure_pa,
        gas_temperature_k=gas_temperature_k,
        gas_molecular_mass_kg=(2.0 if wrong_species else 28.0) * 1.66053906660e-27,
    )
    return env.total_rate(mass_kg)


def generate_observation(scenario: Scenario, replicate_id: int, *, master_seed: int, misspecification: str = "none") -> dict[str, Any]:
    seed = derive_seed(master_seed, scenario.scenario_id + "|" + misspecification, replicate_id)
    rng = np.random.default_rng(seed)
    model = official_model()
    true_pressure = scenario.pressure_pa * float(rng.lognormal(mean=0.0, sigma=0.30))
    recorded_pressure = true_pressure * (1.5 if misspecification == "pressure_miscalibration" else float(rng.normal(1.0, 0.10)))
    true_temperature = max(0.2, scenario.gas_temperature_k + float(rng.normal(0.0, 0.5)))
    recorded_temperature = true_temperature * (0.5 if misspecification == "internal_temperature_underestimated" else 1.0)
    wrong_species = misspecification == "wrong_gas_species"
    env_rate = _environment_rate(scenario.mass_kg, true_pressure, true_temperature, wrong_species=wrong_species)
    if misspecification == "omitted_environment_channel":
        env_rate += 0.15
    if misspecification == "nonlinear_environment":
        env_rate *= 1.0 + 0.3 * min(scenario.mass_ratio, 3.0)
    gamma_t = model.intrinsic_rate(scenario.mass_kg) if scenario.truth_model == "tamesis" else 0.0
    if misspecification == "mixed_population" and replicate_id % 2:
        gamma_t = 0.0
    if misspecification == "threshold_mimicking_systematic":
        gamma_t += 0.35 / (1.0 + np.exp(-40.0 * (scenario.mass_ratio - 1.0)))
    v0 = float(np.clip(rng.normal(0.92, 0.03), 0.4, 0.999))
    if misspecification == "mass_dependent_V0":
        v0 = float(np.clip(v0 - 0.08 * max(scenario.mass_ratio - 1.0, 0.0), 0.3, 0.999))
    phase_offset = float(rng.uniform(-0.15, 0.15))
    phase_count = scenario.phase_count
    phases = np.linspace(0.0, 2.0 * pi, phase_count, endpoint=False)
    phase_noise = rng.normal(0.0, 0.02, size=phase_count)
    if misspecification == "correlated_phase_noise":
        phase_noise = np.cumsum(rng.normal(0.0, 0.01, size=phase_count))
    time_observed = max(1e-6, scenario.observation_time_s * float(rng.normal(1.0, 0.01)))
    visibility = v0 * exp(-(env_rate + gamma_t) * time_observed)
    drift = float(rng.normal(0.0, 0.01)) if misspecification in {"temporal_drift", "run_to_run_variation"} else 0.0
    background = float(rng.poisson(2.0))
    efficiency = float(np.clip(rng.normal(0.90, 0.02), 0.5, 1.0))
    baseline = scenario.shots / phase_count
    mu = efficiency * baseline * (1.0 + visibility * np.cos(phases + phase_offset + phase_noise + drift * np.arange(phase_count))) + background
    mu = np.maximum(mu, 1e-6)
    counts = rng.poisson(mu)
    if misspecification == "outliers" and replicate_id % 11 == 0:
        counts[int(rng.integers(0, phase_count))] += int(4 * baseline)
    if misspecification == "non_gaussian_noise":
        counts = np.maximum(0, counts + rng.standard_t(df=3, size=phase_count).astype(int))
    measured_mass = scenario.mass_kg * float(rng.normal(1.0, 0.02))
    return {
        "scenario_id": scenario.scenario_id,
        "family": scenario.family,
        "replicate_id": replicate_id,
        "seed": seed,
        "truth_model": scenario.truth_model,
        "truth_gamma_t_s-1": gamma_t,
        "truth_environment_rate_s-1": env_rate,
        "mass_ratio": scenario.mass_ratio,
        "mass_true_kg": scenario.mass_kg,
        "mass_measured_kg": measured_mass,
        "separation_m": scenario.separation_m,
        "separation_basis": scenario.separation_basis,
        "time_true_s": scenario.observation_time_s,
        "time_measured_s": time_observed,
        "pressure_true_pa": true_pressure,
        "pressure_recorded_pa": recorded_pressure,
        "gas_temperature_true_k": true_temperature,
        "gas_temperature_recorded_k": recorded_temperature,
        "shots": scenario.shots,
        "phase_count": phase_count,
        "phases_rad": phases.tolist(),
        "counts": counts.tolist(),
        "background_recorded": background,
        "efficiency_recorded": efficiency,
        "v0_truth": v0,
        "visibility_truth": visibility,
        "misspecification": misspecification,
    }
@lru_cache(maxsize=1)
def official_model() -> McModel:
    return McModel()
