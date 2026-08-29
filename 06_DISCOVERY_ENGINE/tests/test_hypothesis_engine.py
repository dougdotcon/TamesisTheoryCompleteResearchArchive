import dataclasses

import pytest

from tamesis_discovery_engine.claim import ClaimState, IllegalTransitionError
from tamesis_discovery_engine.hypothesis_engine import (
    SPEC_METADATA_KEY,
    FalsifiableSpec,
    HypothesisEngine,
    IncompleteSpecError,
)
from tamesis_discovery_engine.registry import Registry

from .conftest import FakeClock


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_complete_spec(**overrides):
    fields = dict(
        raw_claim="I think higher cluster density suppresses star formation.",
        prediction="Star formation rate declines with local cluster density above rho_c.",
        null_model="Star formation rate is independent of local cluster density.",
        competing_model="Star formation rate declines with total halo mass, not density.",
        competing_model_rationale=None,
        effect_size_metric="Spearman correlation between SFR and local density",
        threshold="p < 0.01 and |rho| > 0.3",
    )
    fields.update(overrides)
    return FalsifiableSpec(**fields)


# ---------------------------------------------------------------------------
# FalsifiableSpec.validate()
# ---------------------------------------------------------------------------


def test_validate_returns_empty_list_for_complete_spec():
    spec = make_complete_spec()
    assert spec.validate() == []


def test_validate_flags_empty_prediction():
    spec = make_complete_spec(prediction="")
    problems = spec.validate()
    assert problems != []
    assert any("prediction" in p for p in problems)


def test_validate_flags_empty_null_model():
    spec = make_complete_spec(null_model="   ")
    problems = spec.validate()
    assert problems != []
    assert any("null_model" in p for p in problems)


def test_validate_flags_empty_effect_size_metric():
    spec = make_complete_spec(effect_size_metric="")
    problems = spec.validate()
    assert problems != []
    assert any("effect_size_metric" in p for p in problems)


def test_validate_flags_empty_threshold():
    spec = make_complete_spec(threshold="")
    problems = spec.validate()
    assert problems != []
    assert any("threshold" in p for p in problems)


def test_validate_flags_both_competing_model_and_rationale_empty():
    spec = make_complete_spec(competing_model=None, competing_model_rationale=None)
    problems = spec.validate()
    assert problems != []
    assert any("competing_model" in p for p in problems)


def test_validate_accepts_competing_model_rationale_alone():
    spec = make_complete_spec(
        competing_model=None,
        competing_model_rationale="No plausible alternative mechanism identified in prior work.",
    )
    assert spec.validate() == []


def test_validate_threshold_zero_is_not_empty():
    spec = make_complete_spec(threshold=0)
    assert spec.validate() == []


# ---------------------------------------------------------------------------
# to_claim_metadata() / from_claim_metadata() round-trip
# ---------------------------------------------------------------------------


def test_to_claim_metadata_and_from_claim_metadata_round_trip():
    spec = make_complete_spec()
    metadata = spec.to_claim_metadata()

    assert SPEC_METADATA_KEY in metadata
    rebuilt = FalsifiableSpec.from_claim_metadata(metadata)

    assert rebuilt == spec
    assert dataclasses.asdict(rebuilt) == dataclasses.asdict(spec)


def test_from_claim_metadata_raises_when_key_missing():
    with pytest.raises(KeyError):
        FalsifiableSpec.from_claim_metadata({"tags": ["astro"]})


# ---------------------------------------------------------------------------
# HypothesisEngine.draft()
# ---------------------------------------------------------------------------


def test_draft_with_valid_spec_creates_draft_claim_with_reconstructible_metadata(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec()

    claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)

    assert claim.state is ClaimState.DRAFT
    assert claim.statement == spec.raw_claim

    reloaded = registry.get(claim.id)
    rebuilt_spec = FalsifiableSpec.from_claim_metadata(reloaded.metadata)
    assert rebuilt_spec == spec


def test_draft_with_invalid_spec_raises_and_creates_no_claim(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec(prediction="", threshold="")

    before = registry.list()
    assert before == []

    with pytest.raises(IncompleteSpecError) as excinfo:
        HypothesisEngine.draft(registry, "Broken hypothesis", spec)

    assert "prediction" in " ".join(excinfo.value.problems)
    assert "threshold" in " ".join(excinfo.value.problems)

    after = registry.list()
    assert after == []


# ---------------------------------------------------------------------------
# HypothesisEngine.pre_register()
# ---------------------------------------------------------------------------


def test_pre_register_succeeds_on_still_valid_spec(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec()
    claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)

    updated = HypothesisEngine.pre_register(registry, claim.id)

    assert updated.state is ClaimState.PRE_REGISTERED
    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.PRE_REGISTERED
    assert len(reloaded.history) == 1
    assert reloaded.history[0].to_state is ClaimState.PRE_REGISTERED


def test_pre_register_raises_on_tampered_metadata_and_leaves_claim_in_draft(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec()
    claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)

    # Simulate an out-of-band hand-edit that strips a required field from
    # the spec stored in claim metadata, exactly the kind of post-draft
    # tampering pre_register() exists to catch. Registry exposes no public
    # API to edit metadata after create(), so the fixture reaches into the
    # same JSON store Registry writes to, mirroring test_adversarial.py.
    tampered = registry.get(claim.id)
    tampered.metadata[SPEC_METADATA_KEY]["prediction"] = ""
    registry._save(tampered)

    with pytest.raises(IncompleteSpecError) as excinfo:
        HypothesisEngine.pre_register(registry, claim.id)

    assert "prediction" in " ".join(excinfo.value.problems)

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.DRAFT
    assert reloaded.history == []


def test_pre_register_raises_incomplete_spec_error_when_required_key_deleted(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec()
    claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)

    # Distinct from the tampering test above: here the required key is
    # deleted outright rather than emptied, so FalsifiableSpec(**metadata[...])
    # raises TypeError ("missing 1 required positional argument") instead of
    # producing a spec that validate() can flag. pre_register() must still
    # surface this as IncompleteSpecError, not let the bare TypeError escape.
    tampered = registry.get(claim.id)
    del tampered.metadata[SPEC_METADATA_KEY]["prediction"]
    registry._save(tampered)

    with pytest.raises(IncompleteSpecError) as excinfo:
        HypothesisEngine.pre_register(registry, claim.id)

    assert excinfo.type is IncompleteSpecError

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.DRAFT
    assert reloaded.history == []


def test_pre_register_raises_on_claim_with_no_spec_at_all(tmp_path):
    registry = make_registry(tmp_path)
    claim = registry.create("Free-text claim", "Some vague idea with no spec.")

    with pytest.raises(IncompleteSpecError):
        HypothesisEngine.pre_register(registry, claim.id)

    reloaded = registry.get(claim.id)
    assert reloaded.state is ClaimState.DRAFT


def test_pre_register_on_already_pre_registered_claim_still_illegal_transition(tmp_path):
    registry = make_registry(tmp_path)
    spec = make_complete_spec()
    claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)
    HypothesisEngine.pre_register(registry, claim.id)

    with pytest.raises(IllegalTransitionError):
        HypothesisEngine.pre_register(registry, claim.id)


# ---------------------------------------------------------------------------
# Scope honesty regression: HypothesisEngine.pre_register()'s completeness
# check is enforced only for callers that go through it. Registry.advance()
# is a generic, ungated state-machine transition that knows nothing about
# FalsifiableSpec and does not check it -- this is documented current
# behavior (see the module docstring's "Scope honesty constraint" and
# CHECKLIST_11's Design section), not a gap this module claims to close.
# This test pins that behavior down so a future doc-only edit cannot
# silently reintroduce the false "impossible to bypass" claim without a
# failing test to contradict it.
# ---------------------------------------------------------------------------


def test_registry_advance_bypasses_pre_register_completeness_check(tmp_path):
    registry = make_registry(tmp_path)

    # (1) A claim created via bare Registry.create() with no spec at all --
    # HypothesisEngine.pre_register() would reject this (see
    # test_pre_register_raises_on_claim_with_no_spec_at_all above) but
    # nothing stops a caller from reaching Registry.advance() directly.
    spec_less_claim = registry.create("Free-text claim", "Some vague idea with no spec.")
    advanced = registry.advance(spec_less_claim.id, ClaimState.PRE_REGISTERED)
    assert advanced.state is ClaimState.PRE_REGISTERED
    assert registry.get(spec_less_claim.id).state is ClaimState.PRE_REGISTERED

    # (2) A claim drafted through HypothesisEngine.draft() with a valid
    # spec, then hand-tampered to delete a required field. pre_register()
    # correctly rejects it...
    spec = make_complete_spec()
    tampered_claim = HypothesisEngine.draft(registry, "Cluster density suppresses SFR", spec)
    tampered = registry.get(tampered_claim.id)
    tampered.metadata[SPEC_METADATA_KEY]["prediction"] = ""
    registry._save(tampered)

    with pytest.raises(IncompleteSpecError):
        HypothesisEngine.pre_register(registry, tampered_claim.id)
    assert registry.get(tampered_claim.id).state is ClaimState.DRAFT

    # ...but the same claim reaches PRE_REGISTERED anyway via the generic,
    # ungated Registry.advance() -- the exact bypass this regression test
    # exists to pin down.
    advanced_tampered = registry.advance(tampered_claim.id, ClaimState.PRE_REGISTERED)
    assert advanced_tampered.state is ClaimState.PRE_REGISTERED
    assert registry.get(tampered_claim.id).state is ClaimState.PRE_REGISTERED
