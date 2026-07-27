from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any
from functools import lru_cache

import yaml

from config import load_v1_contract


BASE = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE / "config" / "synthetic_validation_v1.yaml"


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    mass_ratio: float
    mass_kg: float
    separation_m: float | None
    separation_basis: str
    truth_model: str
    observation_time_s: float
    pressure_pa: float
    gas_temperature_k: float
    shots: int
    phase_count: int
    misspecification: str = "none"


@lru_cache(maxsize=1)
def config_payload() -> dict[str, Any]:
    data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("synthetic config must be a mapping")
    contract = load_v1_contract()
    if data.get("tamesis_protocol_id") != contract.protocol_id() or data.get("tamesis_contract_hash") != contract.config_hash():
        raise RuntimeError("synthetic protocol is not bound to the current Tamesis contract")
    if data.get("models", {}).get("rivals") != "exploratory_non_authoritative_comparison":
        raise RuntimeError("rival models cannot enter primary synthetic inference")
    return data


@lru_cache(maxsize=1)
def config_hash() -> str:
    return hashlib.sha256(json.dumps(config_payload(), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


@lru_cache(maxsize=1)
def protocol_id() -> str:
    return f"tamesis-synthetic-v1.0:{config_hash()}"


def derive_seed(master_seed: int, scenario_id: str, replicate_id: int) -> int:
    raw = f"{master_seed}|{scenario_id}|{replicate_id}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big") % (2**32 - 1)


def scenario_grid(profile: str = "quick", *, truth_model: str | None = None) -> list[Scenario]:
    data = config_payload()
    contract = load_v1_contract()
    replicas = int(data["replicas"][profile])
    del replicas  # profile is validated here; callers decide how many to execute
    grid = data["experimental_grid"]
    time_s = float(grid["observation_time_s"][2])  # preregistered 0.1 s primary; other times are sensitivity runs
    pressure = float(grid["pressure_pa"][0])
    scenarios: list[Scenario] = []
    family_values = data["families"]
    for family, values in family_values.items():
        if family == "D_nominal_target":
            for item in values:
                ratio = float(item["mass_kg"]) / contract.mc_kg
                target_time = 0.1
                scenarios.append(Scenario(item["id"], family, ratio, float(item["mass_kg"]), item["separation_m"], item["separation_basis"], truth_model or ("tamesis" if family.startswith("F") else "null"), target_time, pressure, 20.0, 1000, 24))
            continue
        for index, ratio_value in enumerate(values):
            ratio = float(ratio_value)
            scenario_id = f"{family}_{index:02d}_{ratio:g}"
            target_time = 1.0 if family in {"C_above_threshold", "F_tamesis_injected"} and ratio >= 1.5 else time_s
            scenarios.append(Scenario(scenario_id, family, ratio, ratio * contract.mc_kg, 1e-6, "synthetic_controlled_separation", truth_model or ("tamesis" if family.startswith("F") else "null"), target_time, pressure, 20.0, 1000, 24))
    return scenarios
