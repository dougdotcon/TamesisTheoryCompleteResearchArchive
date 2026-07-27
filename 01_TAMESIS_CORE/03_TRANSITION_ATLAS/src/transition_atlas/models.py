from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EpistemicStatus(str, Enum):
    metaphorical = "metaphorical"
    conjectured = "conjectured"
    mathematically_specified = "mathematically_specified"
    computationally_reproduced = "computationally_reproduced"
    phenomenologically_constrained = "phenomenologically_constrained"
    preregistered_test = "preregistered_test"
    observational_anomaly = "observational_anomaly"
    transition_detected = "transition_detected"
    independently_replicated = "independently_replicated"
    established_regime_boundary = "established_regime_boundary"
    falsified = "falsified"
    superseded = "superseded"


class TransitionType(str, Enum):
    isomorphism = "isomorphism"
    reduction = "reduction"
    singular_limit = "singular_limit"
    coarse_graining = "coarse_graining"
    phase_transition = "phase_transition"
    symmetry_breaking = "symmetry_breaking"
    environmental_decoherence = "environmental_decoherence"
    intrinsic_collapse = "intrinsic_collapse"
    emergence = "emergence"
    duality = "duality"
    effective_description_change = "effective_description_change"
    unknown = "unknown"


class ReversibilityClass(str, Enum):
    reversible = "reversible"
    effectively_irreversible = "effectively_irreversible"
    fundamentally_irreversible = "fundamentally_irreversible"
    non_markovian = "non_markovian"
    unknown = "unknown"


class UnitValue(StrictModel):
    value: Any = None
    unit: str
    interval: Optional[dict[str, Any]] = None
    justification: Optional[str] = None
    interpretation: Optional[str] = None
    status: Optional[str] = None


class Regime(StrictModel):
    regime_id: str
    name: str
    version: str
    description: str
    state_space: str
    observable_algebra: str
    dynamics: str
    invariants: list[str]
    symmetries: list[str]
    composition_rule: str
    validity_domain: dict[str, Any]
    control_parameters: list[str]
    limiting_cases: list[str]
    relations_to_other_regimes: list[str]
    epistemic_status: EpistemicStatus
    references: list[dict[str, Any]]
    provenance: dict[str, Any]

    @field_validator("validity_domain")
    @classmethod
    def domain_is_mapping(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(value, dict) or not value:
            raise ValueError("validity_domain must be a non-empty mapping")
        return value


class WeightComponent(StrictModel):
    value: Optional[float] = None
    scale: str
    justification: str
    method: str
    date: str
    provenance: str


class EvidenceWeight(StrictModel):
    mathematical_completeness: WeightComponent
    computational_reproducibility: WeightComponent
    observational_support: WeightComponent
    experimental_discrimination: WeightComponent
    technical_feasibility: WeightComponent
    independent_replication: WeightComponent
    uncertainty: WeightComponent


class Transition(StrictModel):
    transition_id: str
    name: str
    source_regime: str
    target_regime: str
    transition_type: TransitionType
    control_space: dict[str, Any]
    critical_surface: dict[str, Any]
    trigger: str
    transition_map: str
    generator: str
    order_parameters: list[dict[str, Any]]
    entropy_production: UnitValue
    reversibility_class: ReversibilityClass
    observables: list[dict[str, Any]]
    predictions: list[dict[str, Any]]
    falsification_conditions: list[str]
    competing_explanations: list[str]
    nuisance_parameters: list[str]
    experimental_protocols: list[str]
    epistemic_status: EpistemicStatus
    claim_classification: str
    evidence_weight: dict[str, Any]
    uncertainty: UnitValue
    references: list[dict[str, Any]]
    provenance: dict[str, Any]
    contract_integration: Optional[dict[str, Any]] = None


class Evidence(StrictModel):
    evidence_id: str
    evidence_type: str
    claim: str
    result: str
    uncertainty: UnitValue
    source: dict[str, Any]
    provenance: dict[str, Any]


class Protocol(StrictModel):
    protocol_id: str
    name: str
    version: str
    source_module: str
    status: EpistemicStatus
    provenance: dict[str, Any]
