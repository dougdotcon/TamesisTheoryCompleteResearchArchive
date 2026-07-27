from __future__ import annotations

from .models import EpistemicStatus, Transition


def promotion_decision(transition: Transition, target: EpistemicStatus) -> dict:
    reasons: list[str] = []
    if target in {EpistemicStatus.mathematically_specified, EpistemicStatus.computationally_reproduced, EpistemicStatus.preregistered_test}:
        if transition.critical_surface.get("status") in {"not_derived", "candidate_not_derived"} and target == EpistemicStatus.mathematically_specified:
            reasons.append("superfície crítica ainda não derivada")
        if not transition.falsification_conditions:
            reasons.append("falsificação ausente")
    if target == EpistemicStatus.transition_detected:
        reasons.extend(["exige observação prospectiva", "exige marginalização de nuisance e rejeição de rivais"])
    if target == EpistemicStatus.independently_replicated:
        reasons.append("exige fonte independente")
    return {"transition_id": transition.transition_id, "from": transition.epistemic_status.value, "to": target.value, "approved": not reasons, "reasons": reasons, "decision_type": "non_mutating_review"}
