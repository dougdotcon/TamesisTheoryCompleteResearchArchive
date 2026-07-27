from __future__ import annotations

from src.transition_atlas.contract_bridge import tamesis_integration
from src.transition_atlas.graph import build_graph
from src.transition_atlas.loader import load_evidence, load_protocols, load_regimes, load_transitions
from src.transition_atlas.models import EpistemicStatus
from src.transition_atlas.promotion import promotion_decision
from src.transition_atlas.validator import validate


def test_all_regimes_match_schema_and_have_units_in_domain():
    regimes = load_regimes()
    assert len(regimes) == 6
    for regime in regimes.values():
        assert regime.validity_domain
        for value in regime.validity_domain["variables"].values():
            assert "unit" in value


def test_all_transitions_match_schema_and_have_endpoints():
    transitions = load_transitions(); regimes = load_regimes()
    assert len(transitions) == 4
    assert all(t.source_regime in regimes and t.target_regime in regimes for t in transitions.values())


def test_strict_validator_accepts_registry_with_explicit_limitations():
    findings = validate(load_regimes(), load_transitions())
    assert not [f for f in findings if f.severity == "error"]
    assert any(f.item == "holographic_bounce_candidate" for f in findings)


def test_tamesis_imports_canonical_contract_without_manual_copy():
    integration = tamesis_integration()
    assert integration["protocol_id"].startswith("tamesis-mc-v1.0:")
    assert len(integration["config_hash"]) == 64
    assert integration["alpha"] is None
    assert integration["transition_width"] is None


def test_tamesis_edge_has_required_threshold_variables_and_falsification():
    edge = load_transitions()["tamesis_quantum_classical_v1"]
    assert edge.epistemic_status == EpistemicStatus.preregistered_test
    assert {"mass", "separation", "time"} <= set(edge.control_space["variables"])
    assert edge.falsification_conditions


def test_hubble_anomaly_is_separate_from_legacy_mechanism():
    transitions = load_transitions()
    assert transitions["hubble_early_late_anomaly"].epistemic_status == EpistemicStatus.observational_anomaly
    assert transitions["hubble_string_coupling_candidate"].claim_classification == "legacy_conjecture"
    assert transitions["hubble_string_coupling_candidate"].epistemic_status == EpistemicStatus.conjectured


def test_holographic_bound_is_separate_from_bounce_dynamics():
    edge = load_transitions()["holographic_bounce_candidate"]
    assert edge.claim_classification == "theoretical_transition_conjecture"
    assert edge.generator.startswith("action")
    assert edge.epistemic_status == EpistemicStatus.conjectured


def test_invalid_promotion_to_detection_is_rejected():
    edge = load_transitions()["tamesis_quantum_classical_v1"]
    decision = promotion_decision(edge, EpistemicStatus.transition_detected)
    assert not decision["approved"]
    assert decision["reasons"]


def test_missing_falsification_is_detectable():
    edge = load_transitions()["tamesis_quantum_classical_v1"].model_copy(update={"falsification_conditions": []})
    findings = validate(load_regimes(), {edge.transition_id: edge})
    assert any(f.item == edge.transition_id and "falsificação" in f.message for f in findings)


def test_fundamental_irreversibility_requires_global_argument():
    edge = load_transitions()["tamesis_quantum_classical_v1"].model_copy(update={"reversibility_class": "fundamentally_irreversible"})
    findings = validate(load_regimes(), {edge.transition_id: edge})
    assert any("irreversibilidade fundamental" in f.message for f in findings)


def test_graph_hash_is_reproducible():
    first = build_graph(); second = build_graph()
    assert first["graph_hash"] == second["graph_hash"]


def test_protocol_and_evidence_registries_load():
    assert len(load_protocols()) == 1
    assert len(load_evidence()) == 3
