import inspect

import pytest

from tamesis_discovery_engine.atlas import Atlas, AtlasEntry, NonTerminalClaimError
from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.registry import Registry

from .conftest import FakeClock

_CHAIN = [
    ClaimState.PRE_REGISTERED,
    ClaimState.LOCKED,
    ClaimState.RUNNING,
    ClaimState.RESULT,
    ClaimState.ADVERSARIAL_REVIEW,
]


def advance_to(registry: Registry, claim_id: str, target: ClaimState):
    claim = registry.get(claim_id)
    for step in _CHAIN:
        if claim.state == target:
            return claim
        claim = registry.advance(claim_id, step)
    if claim.state != target:
        claim = registry.advance(claim_id, target)
    return claim


def make_claim_in_state(registry: Registry, target: ClaimState, title="Test claim", statement="A testable statement."):
    claim = registry.create(title, statement)
    return advance_to(registry, claim.id, target)


def make_atlas(tmp_path, registry=None, clock=None):
    registry = registry or Registry(data_dir=tmp_path / "claims", clock=FakeClock())
    atlas = Atlas(registry, data_dir=tmp_path / "atlas", clock=clock or FakeClock())
    return atlas, registry


@pytest.mark.parametrize(
    "terminal_state",
    [ClaimState.CONFIRMED, ClaimState.REFUTED, ClaimState.INCONCLUSIVE, ClaimState.NULL],
)
def test_register_against_terminal_claim_succeeds_and_verdict_matches(tmp_path, terminal_state):
    atlas, registry = make_atlas(tmp_path)
    claim = make_claim_in_state(registry, terminal_state)

    entry = atlas.register("TRI-RG", "critical_exponent_beta", 0.326, claim.id)

    assert isinstance(entry, AtlasEntry)
    assert entry.domain == "TRI-RG"
    assert entry.invariant_name == "critical_exponent_beta"
    assert entry.value == 0.326
    assert entry.source_claim_id == claim.id
    assert entry.verdict == terminal_state
    assert entry.registered_at is not None

    found = atlas.search(domain="TRI-RG")
    assert found == [entry]


@pytest.mark.parametrize(
    "non_terminal_state",
    [
        ClaimState.DRAFT,
        ClaimState.PRE_REGISTERED,
        ClaimState.LOCKED,
        ClaimState.RUNNING,
        ClaimState.RESULT,
        ClaimState.ADVERSARIAL_REVIEW,
    ],
)
def test_register_against_non_terminal_claim_raises_and_creates_no_entry(tmp_path, non_terminal_state):
    atlas, registry = make_atlas(tmp_path)
    claim = make_claim_in_state(registry, non_terminal_state)

    with pytest.raises(NonTerminalClaimError) as excinfo:
        atlas.register("TRI-RG", "critical_exponent_beta", 0.326, claim.id)

    assert excinfo.value.claim_id == claim.id
    assert excinfo.value.state == non_terminal_state
    assert atlas.search() == []


def test_search_filters_by_domain_invariant_name_both_and_neither(tmp_path):
    atlas, registry = make_atlas(tmp_path)

    tri_rg_claim = make_claim_in_state(registry, ClaimState.NULL, title="TRI-RG candidate 1")
    tri_rg_claim_2 = make_claim_in_state(registry, ClaimState.NULL, title="TRI-RG candidate 2")
    u12_claim = make_claim_in_state(registry, ClaimState.CONFIRMED, title="u12 candidate")

    e1 = atlas.register("TRI-RG", "hurst_exponent", 0.5, tri_rg_claim.id)
    e2 = atlas.register("TRI-RG", "lyapunov_exponent", 1.2, tri_rg_claim_2.id)
    e3 = atlas.register("u12_universality", "hurst_exponent", 0.71, u12_claim.id)

    assert set(atlas.search()) == {e1, e2, e3}

    assert atlas.search(domain="TRI-RG") == [e1, e2]
    assert atlas.search(domain="u12_universality") == [e3]
    assert atlas.search(domain="no-such-domain") == []

    assert set(atlas.search(invariant_name="hurst_exponent")) == {e1, e3}
    assert atlas.search(invariant_name="lyapunov_exponent") == [e2]
    assert atlas.search(invariant_name="no-such-invariant") == []

    assert atlas.search(domain="TRI-RG", invariant_name="hurst_exponent") == [e1]
    assert atlas.search(domain="u12_universality", invariant_name="hurst_exponent") == [e3]
    assert atlas.search(domain="TRI-RG", invariant_name="no-such-invariant") == []


def test_find_near_duplicates_respects_tolerance_boundary_and_domain_scope(tmp_path):
    atlas, registry = make_atlas(tmp_path)

    base_claim = make_claim_in_state(registry, ClaimState.NULL, title="baseline")
    at_boundary_claim = make_claim_in_state(registry, ClaimState.NULL, title="exactly at tolerance")
    outside_claim = make_claim_in_state(registry, ClaimState.NULL, title="just outside tolerance")
    other_domain_claim = make_claim_in_state(registry, ClaimState.CONFIRMED, title="other domain")
    formula_claim = make_claim_in_state(registry, ClaimState.INCONCLUSIVE, title="formula-valued")

    # baseline=1.0, at_boundary=1.25 -> |diff| == 0.25 exactly; outside=1.3 -> |diff| == 0.3.
    baseline = atlas.register("TRI-RG", "scaling_exponent", 1.0, base_claim.id)
    at_boundary = atlas.register("TRI-RG", "different_name_same_value", 1.25, at_boundary_claim.id)
    outside = atlas.register("TRI-RG", "yet_another_name", 1.3, outside_claim.id)
    atlas.register("u12_universality", "scaling_exponent", 1.0, other_domain_claim.id)
    atlas.register("TRI-RG", "symbolic_invariant", "pi**2 / 6", formula_claim.id)

    duplicates = atlas.find_near_duplicates("TRI-RG", "scaling_exponent", 1.0, tolerance=0.25)

    assert baseline in duplicates
    assert at_boundary in duplicates
    assert outside not in duplicates
    assert len(duplicates) == 2

    just_under_boundary = atlas.find_near_duplicates("TRI-RG", "scaling_exponent", 1.0, tolerance=0.24)
    assert at_boundary not in just_under_boundary
    assert baseline in just_under_boundary

    assert other_domain_claim.id not in [d.source_claim_id for d in duplicates]

    with pytest.raises(TypeError):
        atlas.find_near_duplicates("TRI-RG", "scaling_exponent", "not-a-number", tolerance=0.01)


def test_persistence_round_trip_across_fresh_atlas_instance(tmp_path):
    claims_dir = tmp_path / "claims"
    atlas_dir = tmp_path / "atlas"
    registry = Registry(data_dir=claims_dir, clock=FakeClock())
    atlas = Atlas(registry, data_dir=atlas_dir, clock=FakeClock())

    claim_a = make_claim_in_state(registry, ClaimState.NULL, title="claim a")
    claim_b = make_claim_in_state(registry, ClaimState.REFUTED, title="claim b")

    entry_a = atlas.register("TRI-RG", "hurst_exponent", 0.5, claim_a.id)
    entry_b = atlas.register("TRI-RG", "formula_invariant", "pi**2 / 6", claim_b.id)

    fresh_registry = Registry(data_dir=claims_dir, clock=FakeClock())
    fresh_atlas = Atlas(fresh_registry, data_dir=atlas_dir, clock=FakeClock())

    reloaded = fresh_atlas.search(domain="TRI-RG")
    assert reloaded == [entry_a, entry_b]
    assert reloaded[0].verdict == ClaimState.NULL
    assert reloaded[1].verdict == ClaimState.REFUTED
    assert reloaded[1].value == "pi**2 / 6"


def test_register_signature_has_no_verdict_parameter():
    parameters = inspect.signature(Atlas.register).parameters
    assert "verdict" not in parameters
    expected = {"self", "domain", "invariant_name", "value", "source_claim_id"}
    assert set(parameters) == expected
