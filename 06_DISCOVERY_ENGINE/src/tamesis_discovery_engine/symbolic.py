"""Symbolic Mathematics — Stage 2, Module 6 of the Tamesis Discovery Engine.

Wires computer-algebra support directly into the Hypothesis Registry
(``ROADMAP.md`` Stage 2, item 6), rather than bolting ``sympy`` on as a
standalone utility: :func:`make_symbolic_identity_test_plan` turns a claimed
symbolic identity into a :class:`~tamesis_discovery_engine.runner.TestPlan`
(Module 2's type) that can be locked and run through the existing
:class:`~tamesis_discovery_engine.runner.Runner` exactly like any other
claim.

Two genuinely different verification routes
---------------------------------------------
:func:`verify_identity` decides identity by symbolic simplification
(``sympy.simplify(lhs - rhs)`` followed by ``Expr.equals(0)``, which itself
combines symbolic simplification with an independent randomized numeric
check internally and can return ``True``, ``False``, or ``None`` when it
genuinely cannot decide). :func:`verify_numeric_spot_check` is a *different*
proof technique: it evaluates both sides at caller-supplied numeric
substitutions and compares the results within a tolerance, without ever
calling ``simplify`` or ``equals``. Module 3 (Reproduction Engine) uses the
numeric route to reproduce a claim whose original run used the symbolic
route (or vice versa) — satisfying the "second, independent implementation"
spirit of Module 3's own checklist, rather than wrapping one function in a
thin shell that calls the same code twice.

Never silently confirming an inconclusive check
--------------------------------------------------
``Expr.equals(0)`` returns ``None`` when sympy cannot decide whether an
expression is identically zero (e.g. it involves an undefined/abstract
function). :func:`verify_identity` treats that ``None`` as
``holds=False, method="symbolic_simplify_inconclusive"`` — never as
``holds=True`` — because "couldn't decide" is not evidence the identity
holds; it is the absence of evidence either way, and only a positive
demonstration should ever produce ``holds=True``.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, Iterable, List, Optional

import sympy

from .runner import TestPlan

__all__ = [
    "VerificationResult",
    "verify_identity",
    "verify_numeric_spot_check",
    "make_symbolic_identity_test_plan",
]


@dataclasses.dataclass
class VerificationResult:
    """The outcome of one identity-verification attempt.

    ``method`` names the proof technique used (``"symbolic_simplify"``,
    ``"symbolic_simplify_inconclusive"``, or ``"numeric_spot_check"``) so a
    caller — or a later reproduction attempt — can tell which route produced
    a given verdict. ``detail`` carries the simplified difference for the
    symbolic route, or a description of the first failing (or, on success,
    every passing) substitution for the numeric route.
    """

    holds: bool
    method: str
    detail: str


def _symbol_name(symbol: Any) -> str:
    return symbol.name if isinstance(symbol, sympy.Symbol) else str(symbol)


def verify_identity(
    lhs: Any,
    rhs: Any,
    free_symbols: Optional[Iterable[Any]] = None,
) -> VerificationResult:
    """Decide whether ``lhs`` and ``rhs`` are identically equal.

    Uses ``sympy.simplify(lhs - rhs)`` and then ``Expr.equals(0)`` on the
    simplified difference. ``equals`` can return ``True``, ``False``, or
    ``None`` (cannot decide); only ``True`` ever produces ``holds=True`` —
    there is deliberately no fallback path that defaults an inconclusive
    result to "holds".

    ``free_symbols``, when given, declares the complete set of symbols
    ``lhs``/``rhs`` are allowed to reference (by name — assumptions on the
    declared symbols, if any, are not required to match); a symbol appearing
    in either expression but missing from this declared set raises
    ``ValueError`` rather than silently checking an identity in more
    variables than the caller intended.
    """
    lhs_expr = sympy.sympify(lhs)
    rhs_expr = sympy.sympify(rhs)

    if free_symbols is not None:
        declared_names = {_symbol_name(symbol) for symbol in free_symbols}
        actual_names = {_symbol_name(symbol) for symbol in lhs_expr.free_symbols | rhs_expr.free_symbols}
        undeclared = actual_names - declared_names
        if undeclared:
            raise ValueError(
                f"lhs/rhs reference free symbol(s) {sorted(undeclared)} not listed in free_symbols "
                f"{sorted(declared_names)}"
            )

    difference = sympy.simplify(lhs_expr - rhs_expr)
    decision = difference.equals(0)

    if decision is True:
        return VerificationResult(
            holds=True,
            method="symbolic_simplify",
            detail=f"simplify(lhs - rhs) = {difference}",
        )
    if decision is False:
        return VerificationResult(
            holds=False,
            method="symbolic_simplify",
            detail=f"simplify(lhs - rhs) = {difference}, not identically zero",
        )
    return VerificationResult(
        holds=False,
        method="symbolic_simplify_inconclusive",
        detail=(
            f"sympy could not decide whether simplify(lhs - rhs) = {difference} "
            "is identically zero"
        ),
    )


def verify_numeric_spot_check(
    lhs: Any,
    rhs: Any,
    substitutions: List[Dict[Any, Any]],
    tolerance: float = 1e-9,
) -> VerificationResult:
    """Check ``lhs == rhs`` numerically at each of ``substitutions``.

    This is a genuinely different proof technique from
    :func:`verify_identity`: it never calls ``simplify`` or ``equals``, only
    numeric substitution and evaluation. Substitution keys may be symbol
    names (``str``) or ``sympy.Symbol`` objects; both are resolved against
    the symbols actually appearing in ``lhs``/``rhs``. Stops and reports at
    the first substitution where the two sides disagree by more than
    ``tolerance``; if every substitution agrees, reports ``holds=True``
    naming how many substitutions were checked.
    """
    lhs_expr = sympy.sympify(lhs)
    rhs_expr = sympy.sympify(rhs)

    if not substitutions:
        raise ValueError("verify_numeric_spot_check requires at least one substitution")

    symbol_pool = {_symbol_name(symbol): symbol for symbol in lhs_expr.free_symbols | rhs_expr.free_symbols}

    for index, substitution in enumerate(substitutions):
        resolved = {
            symbol_pool.get(_symbol_name(key), sympy.Symbol(_symbol_name(key))): value
            for key, value in substitution.items()
        }
        lhs_value = complex(lhs_expr.subs(resolved).evalf())
        rhs_value = complex(rhs_expr.subs(resolved).evalf())
        gap = abs(lhs_value - rhs_value)
        if gap > tolerance:
            return VerificationResult(
                holds=False,
                method="numeric_spot_check",
                detail=(
                    f"first divergence at substitution #{index} {substitution}: "
                    f"lhs={lhs_value}, rhs={rhs_value}, |lhs - rhs|={gap} > tolerance={tolerance}"
                ),
            )

    return VerificationResult(
        holds=True,
        method="numeric_spot_check",
        detail=f"lhs and rhs agreed within tolerance={tolerance} at all {len(substitutions)} substitution(s)",
    )


def make_symbolic_identity_test_plan(
    name: str,
    lhs: Any,
    rhs: Any,
    free_symbols: Optional[Iterable[Any]] = None,
    version: str = "v1",
) -> TestPlan:
    """Build a :class:`~tamesis_discovery_engine.runner.TestPlan` that checks ``lhs == rhs``.

    This is the actual "wired into the Hypothesis Registry" integration
    point: the returned ``TestPlan`` can be passed to
    ``Runner.lock``/``Runner.run`` exactly like any other, and its callable
    runs :func:`verify_identity` and returns a JSON-serializable dict
    result. ``lhs``/``rhs``/``free_symbols`` are stringified into
    ``TestPlan.params`` (rather than closed over as live ``sympy`` objects)
    so the declared inputs are exactly what gets persisted in the resulting
    ``LockRecord``/``RunRecord`` and exactly what the callable is invoked
    with, matching every other ``TestPlan`` in this codebase.
    """
    lhs_expr = sympy.sympify(lhs)
    rhs_expr = sympy.sympify(rhs)
    declared_names = [_symbol_name(symbol) for symbol in free_symbols] if free_symbols is not None else None

    def fn(lhs: str, rhs: str, free_symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        # Only ``holds`` is returned (not ``method``/``detail``): those two are
        # narrative to *this* proof technique and would differ, by
        # construction, from a genuinely different second implementation
        # (e.g. verify_numeric_spot_check) reproducing the same claim — such
        # a difference is not a real disagreement and must not make an
        # otherwise-agreeing reproduction register as a mismatch.
        symbols = [sympy.Symbol(name) for name in free_symbols] if free_symbols else None
        result = verify_identity(sympy.sympify(lhs), sympy.sympify(rhs), free_symbols=symbols)
        return {"holds": result.holds}

    params: Dict[str, Any] = {
        "lhs": str(lhs_expr),
        "rhs": str(rhs_expr),
        "free_symbols": declared_names,
    }
    return TestPlan(name=name, version=version, fn=fn, params=params)
