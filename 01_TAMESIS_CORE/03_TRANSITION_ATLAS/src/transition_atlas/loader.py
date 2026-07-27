from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .contract_bridge import tamesis_integration
from .models import Evidence, Protocol, Regime, Transition


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "registry"


def read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"registry entry must be a mapping: {path}")
    return data


def load_regimes() -> dict[str, Regime]:
    regimes = {}
    for path in sorted((REGISTRY / "regimes").glob("*.yaml")):
        item = Regime.model_validate(read_yaml(path))
        if item.regime_id in regimes:
            raise ValueError(f"duplicate regime_id: {item.regime_id}")
        regimes[item.regime_id] = item
    return regimes


def load_transitions() -> dict[str, Transition]:
    transitions = {}
    for path in sorted((REGISTRY / "transitions").glob("*.yaml")):
        data = read_yaml(path)
        if not data.get("evidence_weight"):
            data["evidence_weight"] = {
                key: {"value": None, "scale": "0-1", "justification": "not yet quantified", "method": "pending preregistered analysis", "date": "2026-07-26", "provenance": "atlas_v0_1_unknown"}
                for key in ("mathematical_completeness", "computational_reproducibility", "observational_support", "experimental_discrimination", "technical_feasibility", "independent_replication", "uncertainty")
            }
        if data.get("transition_id") == "tamesis_quantum_classical_v1":
            data["contract_integration"] = tamesis_integration()
        item = Transition.model_validate(data)
        if item.transition_id in transitions:
            raise ValueError(f"duplicate transition_id: {item.transition_id}")
        transitions[item.transition_id] = item
    return transitions


def load_evidence() -> dict[str, Evidence]:
    evidence = {}
    for path in sorted((REGISTRY / "evidence").glob("*.yaml")):
        item = Evidence.model_validate(read_yaml(path))
        evidence[item.evidence_id] = item
    return evidence


def load_protocols() -> dict[str, Protocol]:
    protocols = {}
    for path in sorted((REGISTRY / "protocols").glob("*.yaml")):
        data = read_yaml(path)
        if path.name == "tamesis_mc_v1.yaml":
            integration = tamesis_integration()
            data["protocol_id"] = integration["protocol_id"]
        item = Protocol.model_validate(data)
        protocols[item.protocol_id] = item
    return protocols


def snapshot() -> dict[str, Any]:
    return {
        "regimes": {k: v.model_dump(mode="json") for k, v in load_regimes().items()},
        "transitions": {k: v.model_dump(mode="json") for k, v in load_transitions().items()},
        "evidence": {k: v.model_dump(mode="json") for k, v in load_evidence().items()},
        "protocols": {k: v.model_dump(mode="json") for k, v in load_protocols().items()},
    }
