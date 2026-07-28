from tamesis_lab.evidence_policy import (
    can_promote_automatically,
    validate_evidence_level,
)


def test_evidence_levels_are_explicit():
    assert validate_evidence_level("F")
    assert validate_evidence_level("T")
    assert not validate_evidence_level("SOLVED")


def test_forbidden_promotions_are_not_automatic():
    assert not can_promote_automatically("C", "T")
    assert not can_promote_automatically("F", "T")
    assert not can_promote_automatically("P", "E")
    assert can_promote_automatically("C", "C")
