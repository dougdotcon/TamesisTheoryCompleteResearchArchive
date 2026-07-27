"""Canonical configuration loader for Tamesis M_c v1."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import sys
from typing import Any, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "tamesis_mc_v1.yaml"
LOCK_PATH = BASE_DIR / "config" / "tamesis_mc_v1.lock.json"
SCHEMA_PATH = BASE_DIR / "config" / "tamesis_mc_v1.schema.json"


class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class QuantitySpec(FrozenModel):
    value: Any
    classification: str
    unit: Optional[str] = None
    si_value: Optional[Any] = None
    si_unit: Optional[str] = None
    note: Optional[str] = None

    @model_validator(mode="after")
    def _finite_if_numeric(self) -> "QuantitySpec":
        if isinstance(self.value, float) and not math.isfinite(self.value):
            raise ValueError("non-finite numeric value in configuration")
        return self


class Constants(FrozenModel):
    G: QuantitySpec
    hbar: QuantitySpec
    c: QuantitySpec
    H0: QuantitySpec
    silica_density: QuantitySpec


class StructuralParameters(FrozenModel):
    phase_space_root: QuantitySpec
    exponent: QuantitySpec
    alpha: QuantitySpec
    tau_c: QuantitySpec
    transition_width: QuantitySpec
    sharp_threshold: QuantitySpec
    separation_dependence: QuantitySpec


class DerivedQuantities(FrozenModel):
    Mc_kg: QuantitySpec
    Mc_amu: QuantitySpec
    radius_m: QuantitySpec
    threshold_rate_s_1: QuantitySpec = Field(alias="threshold_rate_s-1")


class Epistemology(FrozenModel):
    source_of_truth_note: str
    rank_status: str
    target_1e15_status: str


class V1Contract(FrozenModel):
    version: str
    name: str
    status: str
    frozen_at: str
    protocol_namespace: str
    constants: Constants
    structural_parameters: StructuralParameters
    derived_quantities: DerivedQuantities
    equations: dict[str, str]
    epistemology: Epistemology

    @property
    def identity(self) -> "Identity":
        return Identity(
            version=self.version,
            name=self.name,
            status=self.status,
            frozen_at=self.frozen_at,
            protocol_namespace=self.protocol_namespace,
        )

    @property
    def h0_si(self) -> float:
        return float(self.constants.H0.value) * 1000.0 / 3.0856775814913673e22

    @property
    def mc_kg(self) -> float:
        return float(self.derived_quantities.Mc_kg.value)

    @property
    def mc_amu(self) -> float:
        return float(self.derived_quantities.Mc_amu.value)

    @property
    def tau_c_s(self) -> float:
        return float(self.structural_parameters.tau_c.value)

    @property
    def exponent(self) -> float:
        return float(self.structural_parameters.exponent.value)

    @property
    def phase_space_root(self) -> int:
        return int(self.structural_parameters.phase_space_root.value)

    @property
    def radius_m(self) -> float:
        return float(self.derived_quantities.radius_m.value)

    @property
    def threshold_rate_s_1(self) -> float:
        return float(self.derived_quantities.threshold_rate_s_1.value)

    def normalized_payload(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=False)

    def config_hash(self) -> str:
        payload = json.dumps(self.normalized_payload(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return sha256(payload.encode("utf-8")).hexdigest()

    def protocol_id(self) -> str:
        return f"{self.identity.protocol_namespace}:{self.config_hash()}"


class ContractError(RuntimeError):
    pass


STRUCTURAL_ENV_KEYS = {
    "TAMESIS_MC_CONFIG",
    "TAMESIS_MC_KG",
    "TAMESIS_MC_TAU_C",
    "TAMESIS_MC_ALPHA",
    "TAMESIS_MC_TRANSITION_WIDTH",
    "TAMESIS_MC_EXPONENT",
    "TAMESIS_MC_PHASE_SPACE_ROOT",
    "MC_KG",
    "TAU_C",
}


def reject_runtime_overrides(
    argv: list[str] | None = None,
    environ: dict[str, str] | None = None,
) -> None:
    """Fail closed: v1.0 entry points accept no structural runtime overrides."""
    argv = list(sys.argv[1:] if argv is None else argv)
    environ = dict(os.environ if environ is None else environ)
    if argv:
        raise ContractError(f"v1.0 entry points accept no CLI arguments or overrides: {argv!r}")
    present = sorted(key for key in STRUCTURAL_ENV_KEYS if key in environ)
    if present:
        raise ContractError(f"v1.0 structural environment overrides are forbidden: {present}")


class Identity(FrozenModel):
    version: str
    name: str
    status: str
    frozen_at: str
    protocol_namespace: str


def _load_raw_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ContractError("configuration must be a mapping")
    return raw


def _load_lock() -> dict[str, Any]:
    if not LOCK_PATH.exists():
        raise ContractError(f"missing lock file: {LOCK_PATH}")
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if not isinstance(lock, dict):
        raise ContractError("invalid lock file")
    return lock


def _validate_contract(contract: V1Contract) -> None:
    if contract.identity.version != "1.0":
        raise ContractError("contract version must be 1.0")
    if contract.identity.protocol_namespace != "tamesis-mc-v1.0":
        raise ContractError("unexpected protocol namespace")

    expected_units = {
        ("constants", "G"): "m^3 kg^-1 s^-2",
        ("constants", "hbar"): "J s",
        ("constants", "c"): "m s^-1",
        ("constants", "H0"): "km s^-1 Mpc^-1",
        ("constants", "silica_density"): "kg m^-3",
        ("structural_parameters", "tau_c"): "s",
        ("derived_quantities", "Mc_kg"): "kg",
        ("derived_quantities", "Mc_amu"): "amu",
        ("derived_quantities", "radius_m"): "m",
        ("derived_quantities", "threshold_rate_s_1"): "s^-1",
    }
    for (group, name), unit in expected_units.items():
        spec = getattr(getattr(contract, group), name)
        if spec.unit != unit:
            raise ContractError(f"unexpected unit for {group}.{name}: {spec.unit!r}")

    locked = _load_lock()
    if locked.get("config_hash") != contract.config_hash():
        raise ContractError("configuration hash does not match lock file")
    if locked.get("protocol_id") != contract.protocol_id():
        raise ContractError("protocol ID does not match lock file")

    mc_expected = 5.292674126388712e-16
    if abs(contract.mc_kg - mc_expected) > 1e-30:
        raise ContractError(f"frozen M_c changed: {contract.mc_kg} != {mc_expected}")

    tau_expected = 2.176246482178091
    if abs(contract.tau_c_s - tau_expected) > 1e-15:
        raise ContractError(f"frozen tau_c changed: {contract.tau_c_s} != {tau_expected}")

    if contract.phase_space_root != 8:
        raise ContractError("phase_space_root changed from frozen v1.0 value 8")
    if abs(contract.exponent - 2.0) > 1e-15:
        raise ContractError("exponent changed from frozen v1.0 value 2.0")


def load_v1_contract(path: Path | None = None) -> V1Contract:
    path = path or CONFIG_PATH
    if not path.exists():
        raise ContractError(f"missing configuration file: {path}")
    raw = _load_raw_yaml(path)
    contract = V1Contract.model_validate(raw)
    _validate_contract(contract)
    return contract


def build_schema_json(path: Path | None = None) -> dict[str, Any]:
    path = path or SCHEMA_PATH
    schema = V1Contract.model_json_schema()
    path.write_text(json.dumps(schema, indent=2, sort_keys=True), encoding="utf-8")
    return schema


@dataclass(frozen=True)
class StructuralParametersView:
    mc_kg: float
    tau_c_s: float
    exponent: float
    phase_space_root: int
    protocol_id: str
    config_hash: str


def structural_view(contract: V1Contract) -> StructuralParametersView:
    return StructuralParametersView(
        mc_kg=contract.mc_kg,
        tau_c_s=contract.tau_c_s,
        exponent=contract.exponent,
        phase_space_root=contract.phase_space_root,
        protocol_id=contract.protocol_id(),
        config_hash=contract.config_hash(),
    )


def resolved_contract_payload(contract: V1Contract) -> dict[str, Any]:
    """Return the portable, deterministic, SI-resolved v1.0 contract view."""
    payload = contract.normalized_payload()
    return {
        "version": contract.version,
        "name": contract.name,
        "status": contract.status,
        "protocol_id": contract.protocol_id(),
        "config_hash": contract.config_hash(),
        "normalized_contract": payload,
        "resolved_si": {
            "H0_s-1": contract.h0_si,
            "H0_declared_s-1": contract.constants.H0.si_value,
            "Mc_kg": contract.mc_kg,
            "tau_c_s": contract.tau_c_s,
            "threshold_rate_s-1": contract.threshold_rate_s_1,
            "radius_m": contract.radius_m,
        },
        "structural": {
            "phase_space_root": contract.phase_space_root,
            "exponent": contract.exponent,
            "alpha": contract.structural_parameters.alpha.value,
            "transition_width": contract.structural_parameters.transition_width.value,
            "functional_form": contract.equations["gamma_T"],
        },
        "epistemic_classifications": {
            "constants": {k: v.classification for k, v in contract.constants},
            "structural_parameters": {k: v.classification for k, v in contract.structural_parameters},
            "derived_quantities": {k: v.classification for k, v in contract.derived_quantities},
            "project": contract.epistemology.model_dump(),
        },
        "declared_dependencies": {
            "Mc": ["G", "hbar", "c", "H0", "phase_space_root"],
            "tau_c": ["G", "hbar", "silica_density", "Mc"],
            "gamma_T": ["Mc", "tau_c", "exponent", "sharp_threshold"],
            "visibility": ["gamma_T", "Gamma_env", "time"],
        },
        "validity_domain": {
            "mass_kg": "finite and non-negative",
            "time_s": "finite and non-negative",
            "environmental_rate_s-1": "finite and non-negative",
            "separation_dependence": "absent_in_v1_0",
            "geometry": "homogeneous silica sphere only for derived radius/tau_c",
            "multiparticle_rule": "not_defined_in_v1_0",
            "composition_rule": "not_defined_in_v1_0",
        },
    }
