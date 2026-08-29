import sympy
import pytest

from tamesis_discovery_engine.claim import ClaimState
from tamesis_discovery_engine.registry import Registry
from tamesis_discovery_engine.reproduction import (
    Reproducer,
    ReproductionPlan,
    ReproductionVerdict,
)
from tamesis_discovery_engine.runner import Runner, TestPlan
from tamesis_discovery_engine.symbolic import (
    VerificationResult,
    make_symbolic_identity_test_plan,
    verify_identity,
    verify_numeric_spot_check,
)

from .conftest import FakeClock

x = sympy.Symbol("x")

TRUE_LHS = (x + 1) ** 2
TRUE_RHS = x**2 + 2 * x + 1

FALSE_LHS = (x + 1) ** 2
FALSE_RHS = x**2 + 2 * x + 2  # typo'd constant term: not identically equal to FALSE_LHS


def make_registry(tmp_path, clock=None):
    return Registry(data_dir=tmp_path / "claims", clock=clock or FakeClock())


def make_runner(tmp_path, registry, clock=None):
    return Runner(registry, data_dir=tmp_path / "runs", clock=clock or FakeClock())


def make_reproducer(tmp_path, registry, runner, clock=None):
    return Reproducer(registry, runner, data_dir=tmp_path / "reproductions", clock=clock or FakeClock())


def make_locked_claim(registry, runner, test_plan, title="Symbolic claim"):
    claim = registry.create(title, "A symbolic identity claim.")
    claim = registry.advance(claim.id, ClaimState.PRE_REGISTERED)
    claim = runner.lock(claim.id, test_plan)
    return claim


def default_substitutions():
    return [{"x": value} for value in (-3, -1, 0, 1, 2, sympy.Rational(7, 2))]


def numeric_spot_check_reproduction_fn(lhs, rhs, free_symbols=None):
    # Mirrors the shape make_symbolic_identity_test_plan's callable returns
    # (only "holds"): "method"/"detail" are narrative to whichever proof
    # technique produced them and would differ between the symbolic and
    # numeric routes even when they agree on the actual truth value.
    lhs_expr = sympy.sympify(lhs)
    rhs_expr = sympy.sympify(rhs)
    result = verify_numeric_spot_check(lhs_expr, rhs_expr, default_substitutions())
    return {"holds": result.holds}


# --- verify_identity -----------------------------------------------------


def test_verify_identity_confirms_true_identity():
    result = verify_identity(TRUE_LHS, TRUE_RHS, free_symbols=[x])

    assert isinstance(result, VerificationResult)
    assert result.holds is True
    assert result.method == "symbolic_simplify"
    assert result.detail


def test_verify_identity_rejects_false_identity_with_nonzero_detail():
    result = verify_identity(FALSE_LHS, FALSE_RHS, free_symbols=[x])

    assert result.holds is False
    assert result.method == "symbolic_simplify"
    assert result.detail
    # the simplified difference itself must be a nonzero constant
    simplified = sympy.simplify(sympy.sympify(FALSE_LHS) - sympy.sympify(FALSE_RHS))
    assert simplified != 0


def test_verify_identity_rejects_undeclared_free_symbols():
    y = sympy.Symbol("y")
    with pytest.raises(ValueError):
        verify_identity(x + y, y + x, free_symbols=[x])


def test_verify_identity_reports_inconclusive_rather_than_holds_true():
    f = sympy.Function("f")
    result = verify_identity(f(x) + f(-x), 0, free_symbols=[x])

    assert result.holds is False
    assert result.method == "symbolic_simplify_inconclusive"
    assert result.detail


# --- verify_numeric_spot_check --------------------------------------------


def test_verify_numeric_spot_check_confirms_true_identity_at_several_points():
    result = verify_numeric_spot_check(TRUE_LHS, TRUE_RHS, default_substitutions())

    assert result.holds is True
    assert result.method == "numeric_spot_check"
    assert "6" in result.detail  # six substitutions checked


def test_verify_numeric_spot_check_flags_false_identity_at_first_divergence():
    substitutions = default_substitutions()
    result = verify_numeric_spot_check(FALSE_LHS, FALSE_RHS, substitutions)

    assert result.holds is False
    assert result.method == "numeric_spot_check"
    assert "#0" in result.detail


def test_verify_numeric_spot_check_requires_at_least_one_substitution():
    with pytest.raises(ValueError):
        verify_numeric_spot_check(TRUE_LHS, TRUE_RHS, [])


# --- make_symbolic_identity_test_plan + Runner integration -----------------


def test_true_identity_claim_run_through_runner_reflects_holds_true(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan = make_symbolic_identity_test_plan(
        "expand_square", TRUE_LHS, TRUE_RHS, free_symbols=[x]
    )

    claim = make_locked_claim(registry, runner, test_plan)
    record = runner.run(claim.id, test_plan)

    assert record.success is True
    assert record.result["holds"] is True
    assert registry.get(claim.id).state is ClaimState.RESULT


def test_false_identity_claim_run_through_runner_reflects_holds_false(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan = make_symbolic_identity_test_plan(
        "typo_square", FALSE_LHS, FALSE_RHS, free_symbols=[x]
    )

    claim = make_locked_claim(registry, runner, test_plan)
    record = runner.run(claim.id, test_plan)

    assert record.success is True
    assert record.result["holds"] is False
    # a false identity still reaches RESULT: the *run* succeeded (it produced
    # a verdict), even though the identity itself does not hold.
    assert registry.get(claim.id).state is ClaimState.RESULT


def test_test_plan_params_are_json_serializable_declared_inputs(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    test_plan = make_symbolic_identity_test_plan(
        "expand_square", TRUE_LHS, TRUE_RHS, free_symbols=[x]
    )

    assert test_plan.params == {"lhs": str(TRUE_LHS), "rhs": str(TRUE_RHS), "free_symbols": ["x"]}

    claim = make_locked_claim(registry, runner, test_plan)
    record = runner.run(claim.id, test_plan)

    fresh_runner = Runner(registry, data_dir=tmp_path / "runs", clock=FakeClock())
    reloaded = fresh_runner.get_run(claim.id)
    assert reloaded.params == test_plan.params
    assert reloaded.result == record.result


# --- Reproduction Engine: genuinely independent second route ---------------


def test_numeric_reproduction_of_true_identity_matches(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    test_plan = make_symbolic_identity_test_plan(
        "expand_square", TRUE_LHS, TRUE_RHS, free_symbols=[x]
    )
    claim = make_locked_claim(registry, runner, test_plan)
    runner.run(claim.id, test_plan)

    reproduction_plan = ReproductionPlan(
        name="numeric_spot_check", version="v1", fn=numeric_spot_check_reproduction_fn
    )
    record = reproducer.reproduce(claim.id, reproduction_plan)

    assert record.verdict in (
        ReproductionVerdict.EXACT_MATCH.value,
        ReproductionVerdict.MATCH_WITHIN_TOLERANCE.value,
    )
    assert record.original_result["holds"] is True
    assert record.reproduced_result["holds"] is True


def test_numeric_reproduction_catches_a_buggy_original_symbolic_result_as_mismatch(tmp_path):
    registry = make_registry(tmp_path)
    runner = make_runner(tmp_path, registry)
    reproducer = make_reproducer(tmp_path, registry, runner)

    def buggy_verify_identity_fn(lhs, rhs, free_symbols=None):
        # Simulates a bug in the original check: it never actually calls
        # verify_identity/sympy at all, and just asserts the identity holds
        # regardless of lhs/rhs (e.g. a copy-pasted stub, or the typo'd rhs
        # having been eyeballed as "looks right").
        return {"holds": True, "method": "symbolic_simplify", "detail": "(unchecked)"}

    buggy_test_plan = TestPlan(
        name="typo_square_buggy",
        version="v1",
        fn=buggy_verify_identity_fn,
        params={"lhs": str(FALSE_LHS), "rhs": str(FALSE_RHS), "free_symbols": ["x"]},
    )
    claim = make_locked_claim(registry, runner, buggy_test_plan, title="Buggy symbolic claim")
    original_record = runner.run(claim.id, buggy_test_plan)
    assert original_record.result["holds"] is True  # the (wrong) original verdict

    reproduction_plan = ReproductionPlan(
        name="numeric_spot_check", version="v1", fn=numeric_spot_check_reproduction_fn
    )
    record = reproducer.reproduce(claim.id, reproduction_plan)

    assert record.reproduced_result["holds"] is False
    assert record.verdict == ReproductionVerdict.MISMATCH.value
    mismatched_fields = {delta.field for delta in record.deltas}
    assert "holds" in mismatched_fields
