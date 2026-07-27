from __future__ import annotations

from math import log
from typing import Any
from functools import lru_cache

import numpy as np

from environment_model import Environment
from mc_model import McModel
from .protocol import config_payload


@lru_cache(maxsize=1)
def official_model() -> McModel:
    return McModel()


def estimate_visibility(observation: dict[str, Any]) -> tuple[float, float]:
    counts = np.asarray(observation["counts"], dtype=float) - float(observation.get("background_recorded", 0.0))
    phases = np.asarray(observation["phases_rad"], dtype=float)
    total = float(np.sum(counts))
    if total <= 0:
        return 0.0, 1.0
    c = 2.0 * float(np.sum(counts * np.cos(phases))) / total
    s = 2.0 * float(np.sum(counts * np.sin(phases))) / total
    return float(np.clip(np.sqrt(c * c + s * s), 0.0, 1.0)), float(np.sqrt(2.0 / max(total, 1.0)))


def _environment_reference(observation: dict[str, Any]) -> tuple[float, float]:
    env = Environment(pressure_pa=max(observation["pressure_recorded_pa"], 0.0), gas_temperature_k=max(observation["gas_temperature_recorded_k"], 0.2))
    reference = env.total_rate(observation["mass_measured_kg"])
    return reference, max(0.30 * reference, 1e-4)


def fit_model(observation: dict[str, Any], *, tamesis_enabled: bool) -> dict[str, Any]:
    model = official_model()
    vhat, sigma = estimate_visibility(observation)
    reference_env, env_sigma = _environment_reference(observation)
    env_grid = np.unique(np.maximum(0.0, reference_env * np.asarray([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0])))
    v0_grid = np.linspace(0.70, 0.999, 13)
    gamma_t = model.intrinsic_rate(observation["mass_measured_kg"]) if tamesis_enabled else 0.0
    predicted = v0_grid[:, None] * np.exp(-(env_grid[None, :] + gamma_t) * observation["time_measured_s"])
    scores = -0.5 * ((vhat - predicted) / max(sigma, 1e-4)) ** 2 - 0.5 * ((env_grid[None, :] - reference_env) / env_sigma) ** 2
    best_index = np.unravel_index(int(np.argmax(scores)), scores.shape)
    best = {"log_likelihood": float(scores[best_index]), "environment_rate_hat_s-1": float(env_grid[best_index[1]]), "V0_hat": float(v0_grid[best_index[0]]), "gamma_t_hat_s-1": float(gamma_t), "predicted_visibility": float(predicted[best_index])}
    best.update({"visibility_hat": vhat, "visibility_sigma": sigma, "environment_reference_s-1": reference_env, "environment_sigma_s-1": env_sigma, "model": "Tamesis" if tamesis_enabled else "QM_plus_environment"})
    best["environment_95_interval"] = [max(0.0, best["environment_rate_hat_s-1"] - 1.96 * env_sigma), best["environment_rate_hat_s-1"] + 1.96 * env_sigma]
    truth_environment = observation.get("truth_environment_rate_s-1")
    best["environment_coverage_proxy"] = None if truth_environment is None else best["environment_95_interval"][0] <= truth_environment <= best["environment_95_interval"][1]
    return best


def infer_observation(observation: dict[str, Any]) -> dict[str, Any]:
    null = fit_model(observation, tamesis_enabled=False)
    alternative = fit_model(observation, tamesis_enabled=True)
    likelihood_ratio = 2.0 * (alternative["log_likelihood"] - null["log_likelihood"])
    total_counts = int(np.sum(observation["counts"]))
    rules = config_payload()["decision_rules"]
    threshold = float(rules["likelihood_ratio_absolute_threshold"])
    informative = total_counts >= int(rules["minimum_total_counts"]) and alternative["visibility_sigma"] <= float(rules["maximum_visibility_sigma"])
    if not informative:
        classification = "inconclusive"
    elif likelihood_ratio > threshold:
        classification = "tamesis_plus_environment"
    elif likelihood_ratio < -threshold:
        classification = "environment_only"
    else:
        classification = "inconclusive"
    gamma = observation.get("truth_gamma_t_s-1")
    env = observation.get("truth_environment_rate_s-1")
    gamma_for_diagnostic = alternative["gamma_t_hat_s-1"] if gamma is None else gamma
    env_for_diagnostic = alternative["environment_reference_s-1"] if env is None else env
    ratio = gamma_for_diagnostic / max(env_for_diagnostic, 1e-12)
    if ratio > 5.0 and observation["mass_ratio"] > 1.2 and observation["pressure_true_pa"] <= 1e-12 and informative:
        identifiability = "locally_identifiable"
    elif ratio > 1.0 and informative:
        identifiability = "weakly_identifiable"
    elif gamma_for_diagnostic == 0.0 and observation["mass_ratio"] < 1.0:
        identifiability = "locally_identifiable"
    elif not informative:
        identifiability = "practically_non_identifiable"
    else:
        identifiability = "structurally_non_identifiable"
    return {
        "scenario_id": observation["scenario_id"], "family": observation["family"], "replicate_id": observation["replicate_id"], "seed": observation["seed"], "truth_model": observation.get("truth_model", "hidden"), "truth_gamma_t_s-1": gamma, "truth_environment_rate_s-1": env, "mass_ratio": observation["mass_ratio"], "mass_measured_kg": observation["mass_measured_kg"], "likelihood_ratio": likelihood_ratio, "classification": classification, "identifiability": identifiability, "informative": informative, "total_counts": total_counts, "null": null, "alternative": alternative, "environment_mimic_ratio": None if env is None or gamma is None else env / max(gamma, 1e-12), "coverage_proxy": None if env is None else (alternative["environment_95_interval"][0] <= env <= alternative["environment_95_interval"][1] if observation.get("truth_model") == "tamesis" else null["environment_95_interval"][0] <= env <= null["environment_95_interval"][1]), "misspecification": observation["misspecification"],
    }
