from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import EpistemicStatus, ReversibilityClass, Regime, Transition


@dataclass(frozen=True)
class Finding:
    severity: str
    item: str
    message: str


def validate(regimes: dict[str, Regime], transitions: dict[str, Transition], *, strict: bool = True) -> list[Finding]:
    findings: list[Finding] = []
    for regime_id, regime in regimes.items():
        if not regime.validity_domain:
            findings.append(Finding("error", regime_id, "regime sem domínio de validade"))
        for key, value in regime.validity_domain.get("variables", {}).items():
            if isinstance(value, dict) and "unit" not in value:
                findings.append(Finding("error", regime_id, f"variável {key} sem unidade"))
    for transition_id, transition in transitions.items():
        if transition.source_regime not in regimes or transition.target_regime not in regimes:
            findings.append(Finding("error", transition_id, "fonte ou alvo inexistente"))
        if not transition.critical_surface.get("equation"):
            findings.append(Finding("error", transition_id, "superfície crítica sem equação"))
        if not transition.falsification_conditions:
            findings.append(Finding("error", transition_id, "transição sem falsificação"))
        if not transition.observables and transition.epistemic_status in {EpistemicStatus.preregistered_test, EpistemicStatus.transition_detected}:
            findings.append(Finding("error", transition_id, "teste sem observáveis"))
        reversibility = getattr(transition.reversibility_class, "value", transition.reversibility_class)
        if reversibility == ReversibilityClass.fundamentally_irreversible.value and transition.entropy_production.value in {None, "unknown"}:
            findings.append(Finding("error", transition_id, "irreversibilidade fundamental sem dinâmica global/produção de entropia"))
        if transition.transition_id.startswith("tamesis_"):
            variables = transition.control_space.get("variables", {})
            for required in ("mass", "separation", "time"):
                if required not in variables:
                    findings.append(Finding("error", transition_id, f"threshold Tamesis sem variável {required}"))
            if not transition.contract_integration:
                findings.append(Finding("error", transition_id, "integração canônica ausente"))
        for prediction in transition.predictions:
            if "frequency" in str(prediction.get("name", "")).lower() and "amplitude" not in prediction:
                findings.append(Finding("limitation", transition_id, "frequência sem amplitude; conjectura não promovível"))
        if transition.epistemic_status in {EpistemicStatus.transition_detected, EpistemicStatus.independently_replicated, EpistemicStatus.established_regime_boundary} and not transition.evidence_weight:
            findings.append(Finding("error", transition_id, "status elevado sem peso vetorial de evidência"))
        if transition.epistemic_status == EpistemicStatus.observational_anomaly and not transition.references:
            findings.append(Finding("error", transition_id, "anomalia sem referência"))
        if all(ref.get("type") == "secondary" for ref in transition.references) and transition.references:
            findings.append(Finding("limitation", transition_id, "referência primária ausente"))
        for container_name, container in (("critical_surface", transition.critical_surface), ("uncertainty", transition.uncertainty.model_dump())):
            if isinstance(container, dict) and str(container.get("status", "")).lower() in {"unknown", "unquantified", "not_derived"} and container.get("value") == 0:
                findings.append(Finding("error", transition_id, f"{container_name} unknown preenchido com zero"))
    return findings
