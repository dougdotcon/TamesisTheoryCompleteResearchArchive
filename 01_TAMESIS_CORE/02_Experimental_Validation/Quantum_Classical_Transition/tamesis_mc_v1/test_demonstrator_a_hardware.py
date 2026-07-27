from demonstrator_a_hardware.core import cfg, evaluate_material, reveal_validation, validate_protocol

def test_v05_forbids_tamesis_scope():
    prohibited=set(cfg()["scope_forbidden"])
    assert {"Tamesis","Mc","mu_T","interferometry"}.issubset(prohibited)

def test_fixture_cannot_select_material():
    result=evaluate_material(fixture=True)
    assert result["status"]=="material_candidate_inconclusive"

def test_reveal_is_fail_closed():
    assert reveal_validation()["status"]=="blocked_until_predictions_frozen"

def test_protocol_validates_without_hardware_claim():
    result=validate_protocol()
    assert result["status"]=="valid"
    assert result["hardware_claim"] is False
