"""Mathematical Discovery Engine — Stage 3a, Module 12 of the Tamesis
Discovery Engine.

Source: ``ROADMAP.md`` Stage 3 product table, "given a combinatorial/
asymptotic system definition, runs exact enumeration -> symbolic algebra
-> simulation -> asymptotic fitting -> proof-candidate search. Generalizes
exactly the ``05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS`` workflow that
produced the U_{1/2} family." (``CHECKLIST_12_MATHEMATICAL_DISCOVERY_ENGINE.md``)

Scope honesty constraint
-------------------------
"Proof-candidate search" does **not** mean an AI system that invents
closed-form candidates on its own — that is not a solved, deterministic
problem and faking it would be dishonest. This module runs each
**caller-supplied** candidate closed-form expression through the same
funnel ``05_DISCOVERY_LAB`` already uses by hand: exact enumeration for
small cases, symbolic identity checking, Monte Carlo triangulation for
larger cases, and an asymptotic-fit residual check — then reports which
candidates survive and which are refuted, with the evidence attributing
the verdict to the specific stage(s) that produced it. Generating the
candidates in the first place is still a human/agent job, exactly as it
is in ``05_DISCOVERY_LAB`` today. This module never invents an expression,
never guesses a closed form, and never fabricates a verdict for a stage
that did not actually run.

Reuse, not reimplementation
-----------------------------
Every numeric/symbolic decision below is delegated to Module 6
(:mod:`tamesis_discovery_engine.symbolic`) or Module 7
(:mod:`tamesis_discovery_engine.montecarlo`):

- The enumeration stage calls :func:`~tamesis_discovery_engine.symbolic.verify_numeric_spot_check`
  once per tested ``n`` (the enumerator's exact value at ``n`` varies with
  ``n``, so it cannot be handed to that function as a single fixed ``rhs``
  across every substitution the way a single target expression could).
- The symbolic stage calls :func:`~tamesis_discovery_engine.symbolic.verify_identity`
  directly, unmodified.
- The Monte Carlo stage calls :func:`~tamesis_discovery_engine.montecarlo.triangulate`
  directly: the candidate's predicted numeric value (at a caller-declared
  substitution) is wrapped as one more constant-valued estimator and
  triangulated alongside the caller's genuinely-random estimator(s) — the
  candidate is judged to triangulate only if it is not named among the
  estimators :func:`~tamesis_discovery_engine.montecarlo.triangulate` itself
  flags as diverging.

No ``sympy.simplify``/``Expr.equals`` call and no seeded-RNG estimator loop
is reimplemented in this file (grep to confirm, per the checklist's own
acceptance note).

Designed signatures for the two stages the checklist left open
------------------------------------------------------------------
The checklist spells out only that "enumerator" is "a callable ``n ->
exact_value`` plus a range of small ``n`` to check, or similar — design the
exact signature, document it clearly". This module extends that same
"design it, document it" latitude to the Monte Carlo and asymptotic stages,
whose exact shapes the checklist likewise leaves unspecified, plus adds one
parameter the checklist's prose requires but its literal signature list
omits:

- :class:`Enumerator` bundles the ``n -> exact_value`` callable with the
  sequence of small ``n`` to check and the name of the symbol in
  ``candidate_expr`` that stands for ``n`` (default ``"n"``).
- ``symbolic_target``: the checklist's design step 2 says "if
  ``free_symbols``/a target identity is given, runs ``verify_identity``
  between the candidate and the target" — but a symbolic identity check is
  inherently binary (it compares *two* expressions) and cannot run from
  ``candidate_expr``/``free_symbols`` alone, so this module adds an explicit
  ``symbolic_target`` parameter carrying that second expression.
  ``free_symbols`` remains optional and, when given, is forwarded to
  :func:`~tamesis_discovery_engine.symbolic.verify_identity` as its own
  declared-vocabulary safety check.
- :class:`MonteCarloCheck` bundles the caller's independent estimator(s),
  the symbol substitution used to turn ``candidate_expr`` into one concrete
  number for triangulation, and ``triangulate``'s own ``n_trials``/``seed``/
  ``tolerance`` — kept on this dataclass, not on ``run_candidate``'s shared
  ``tolerance``, because a triangulation tolerance is a z-score threshold
  (``triangulate``'s default is ``3.0``) on a completely different scale
  from an absolute numeric tolerance.
- :class:`AsymptoticCheck` bundles the expected-limiting-behavior callable,
  the (large, increasing) sequence of ``n`` to test, the symbol name, and
  its own ``tolerance`` — again kept separate from ``run_candidate``'s
  shared ``tolerance``, because an asymptotic-fit tolerance is a *relative*
  residual threshold (an approximation is expected to still differ from the
  exact value at any finite ``n``; only the relative gap need shrink), not
  the tight absolute tolerance appropriate to an exact enumeration spot
  check.

``run_candidate``'s own ``tolerance`` argument (default ``1e-6``, matching
:func:`~tamesis_discovery_engine.symbolic.verify_numeric_spot_check`'s own
parameter) is therefore used for exactly one thing: the enumeration stage's
numeric spot check.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Sequence, Tuple

import numpy as np
import sympy

from .montecarlo import Estimator, triangulate
from .symbolic import verify_identity, verify_numeric_spot_check

__all__ = [
    "CandidateResult",
    "Enumerator",
    "MonteCarloCheck",
    "AsymptoticCheck",
    "MathDiscoveryPipeline",
]

Verdict = Literal["SURVIVES", "REFUTED", "INCONCLUSIVE"]


@dataclasses.dataclass(frozen=True)
class Enumerator:
    """Exact ``n -> value`` ground truth for the enumeration stage.

    ``fn`` computes the exact value of the quantity under study at one
    small ``n`` (e.g. by brute-force combinatorial counting); ``ns`` is the
    sequence of small ``n`` to check the candidate against; ``symbol`` names
    the free symbol in ``candidate_expr`` that stands for ``n`` (default
    ``"n"``).
    """

    fn: Callable[[int], Any]
    ns: Sequence[int]
    symbol: str = "n"


@dataclasses.dataclass(frozen=True)
class MonteCarloCheck:
    """Triangulation setup for the Monte Carlo stage.

    ``estimators`` are the caller's independently-implemented estimator(s)
    of the same quantity ``candidate_expr`` predicts (same shape as
    :data:`tamesis_discovery_engine.montecarlo.Estimator`, i.e.
    ``Callable[[numpy.random.Generator], float]``); ``substitution`` maps
    symbol names in ``candidate_expr`` to the concrete values that turn it
    into the single number being triangulated (e.g. ``{"n": 20}``);
    ``n_trials``/``seed``/``tolerance`` are forwarded to
    :func:`~tamesis_discovery_engine.montecarlo.triangulate` unchanged.
    """

    estimators: Sequence[Tuple[str, Estimator]]
    substitution: Dict[str, Any]
    n_trials: int
    seed: int
    tolerance: float = 3.0


@dataclasses.dataclass(frozen=True)
class AsymptoticCheck:
    """Expected-limiting-behavior setup for the asymptotic-fit stage.

    ``target`` computes the expected leading-order/limiting value at one
    ``n``; ``ns`` is a strictly increasing sequence of (typically large) ``n``
    to evaluate the candidate at; ``symbol`` names the free symbol in
    ``candidate_expr`` standing for ``n``. The reported residual is the
    *relative* gap ``|candidate(n) - target(n)| / |target(n)|`` at the
    largest ``n`` in ``ns`` — relative, not absolute, because an asymptotic
    approximation is only expected to converge in a relative sense (its
    absolute gap can grow without bound even while it is the objectively
    correct leading-order behavior). ``tolerance`` is the relative-residual
    threshold below which the stage counts as agreeing.
    """

    target: Callable[[int], float]
    ns: Sequence[int]
    symbol: str = "n"
    tolerance: float = 1e-2


@dataclasses.dataclass(frozen=True)
class CandidateResult:
    """The outcome of running one candidate closed-form expression through
    every stage the caller supplied evidence for.

    Every ``Optional`` field stays ``None`` when its stage was not supplied
    (no enumerator/no symbolic target/no mc_estimators/no asymptotic
    target) — a stage that never ran must never be reported as having
    agreed. ``verdict`` is ``REFUTED`` if any stage that ran produced a
    clear mismatch, ``SURVIVES`` only if every stage that ran agreed, and
    ``INCONCLUSIVE`` if no stage produced a clear result either way (i.e.
    every one of the four fields below is ``None``).

    ``details`` carries one short, human-readable evidence string per stage
    that actually ran, keyed by stage name (``"enumeration"``, ``"symbolic"``,
    ``"mc"``, ``"asymptotic"``) — the concrete "with the evidence" this
    module's scope constraint promises, beyond the bare booleans/residual.
    """

    candidate_name: str
    enumeration_match: Optional[bool]
    symbolic_match: Optional[bool]
    mc_triangulates: Optional[bool]
    asymptotic_fit_residual: Optional[float]
    verdict: Verdict
    details: Dict[str, str] = dataclasses.field(default_factory=dict)


def _resolve_symbol(expr: Any, name: str) -> sympy.Symbol:
    for symbol in expr.free_symbols:
        if symbol.name == name:
            return symbol
    return sympy.Symbol(name)


def _substitute(expr: Any, mapping: Dict[str, Any]) -> Any:
    resolved = {_resolve_symbol(expr, name): value for name, value in mapping.items()}
    return expr.subs(resolved)


class MathDiscoveryPipeline:
    """Runs caller-supplied closed-form candidates through the exact
    enumeration / symbolic identity / Monte Carlo triangulation /
    asymptotic-fit funnel and reports which survive.

    Stateless: every method is a pure function of its arguments, mirroring
    Modules 6/7 which this class is built entirely out of.
    """

    def run_candidate(
        self,
        candidate_name: str,
        candidate_expr: Any,
        free_symbols: Optional[Iterable[Any]] = None,
        symbolic_target: Optional[Any] = None,
        enumerator: Optional[Enumerator] = None,
        mc_estimators: Optional[MonteCarloCheck] = None,
        asymptotic_target: Optional[AsymptoticCheck] = None,
        tolerance: float = 1e-6,
    ) -> CandidateResult:
        candidate = sympy.sympify(candidate_expr)
        details: Dict[str, str] = {}

        enumeration_match: Optional[bool] = None
        if enumerator is not None:
            enumeration_match, note = self._check_enumeration(candidate, enumerator, tolerance)
            details["enumeration"] = note

        symbolic_match: Optional[bool] = None
        if symbolic_target is not None:
            symbolic_match, note = self._check_symbolic(candidate, symbolic_target, free_symbols)
            details["symbolic"] = note

        mc_triangulates: Optional[bool] = None
        if mc_estimators is not None:
            mc_triangulates, note = self._check_mc(candidate, mc_estimators)
            details["mc"] = note

        asymptotic_fit_residual: Optional[float] = None
        asymptotic_mismatch = False
        if asymptotic_target is not None:
            asymptotic_fit_residual, asymptotic_mismatch, note = self._check_asymptotic(
                candidate, asymptotic_target
            )
            details["asymptotic"] = note

        verdict = self._derive_verdict(
            enumeration_match, symbolic_match, mc_triangulates, asymptotic_fit_residual, asymptotic_mismatch
        )

        return CandidateResult(
            candidate_name=candidate_name,
            enumeration_match=enumeration_match,
            symbolic_match=symbolic_match,
            mc_triangulates=mc_triangulates,
            asymptotic_fit_residual=asymptotic_fit_residual,
            verdict=verdict,
            details=details,
        )

    def run(
        self,
        candidates: List[Tuple[str, Any]],
        free_symbols: Optional[Iterable[Any]] = None,
        symbolic_target: Optional[Any] = None,
        enumerator: Optional[Enumerator] = None,
        mc_estimators: Optional[MonteCarloCheck] = None,
        asymptotic_target: Optional[AsymptoticCheck] = None,
        tolerance: float = 1e-6,
    ) -> List[CandidateResult]:
        return [
            self.run_candidate(
                name,
                expr,
                free_symbols=free_symbols,
                symbolic_target=symbolic_target,
                enumerator=enumerator,
                mc_estimators=mc_estimators,
                asymptotic_target=asymptotic_target,
                tolerance=tolerance,
            )
            for name, expr in candidates
        ]

    @staticmethod
    def _check_enumeration(candidate: Any, enumerator: Enumerator, tolerance: float) -> Tuple[bool, str]:
        first_mismatch: Optional[Tuple[int, str]] = None
        checked = 0
        for n in enumerator.ns:
            exact = enumerator.fn(n)
            result = verify_numeric_spot_check(
                candidate,
                sympy.sympify(exact),
                substitutions=[{enumerator.symbol: n}],
                tolerance=tolerance,
            )
            checked += 1
            if not result.holds and first_mismatch is None:
                first_mismatch = (n, result.detail)

        if first_mismatch is not None:
            n, detail = first_mismatch
            return False, f"mismatch at {enumerator.symbol}={n}: {detail}"
        return True, f"matched exact enumeration at all {checked} tested {enumerator.symbol} value(s)"

    @staticmethod
    def _check_symbolic(
        candidate: Any, symbolic_target: Any, free_symbols: Optional[Iterable[Any]]
    ) -> Tuple[bool, str]:
        symbols = list(free_symbols) if free_symbols is not None else None
        result = verify_identity(candidate, symbolic_target, free_symbols=symbols)
        return result.holds, f"{result.method}: {result.detail}"

    @staticmethod
    def _check_mc(candidate: Any, mc_check: MonteCarloCheck) -> Tuple[bool, str]:
        predicted = float(_substitute(candidate, mc_check.substitution).evalf())

        def candidate_estimator(rng: np.random.Generator, _value: float = predicted) -> float:
            return _value

        estimators: List[Tuple[str, Estimator]] = [("candidate", candidate_estimator)]
        estimators.extend(mc_check.estimators)

        result = triangulate(
            estimators,
            n_trials=mc_check.n_trials,
            seed=mc_check.seed,
            tolerance=mc_check.tolerance,
        )
        agrees = "candidate" not in result.diverging
        note = (
            f"predicted={predicted}, max_z={result.max_z:.3f}, "
            f"diverging={result.diverging}"
        )
        return agrees, note

    @staticmethod
    def _check_asymptotic(candidate: Any, check: AsymptoticCheck) -> Tuple[float, bool, str]:
        if len(check.ns) < 1:
            raise ValueError("AsymptoticCheck.ns must contain at least one n")
        if list(check.ns) != sorted(check.ns):
            raise ValueError(f"AsymptoticCheck.ns must be non-decreasing, got {list(check.ns)}")

        n = check.ns[-1]
        candidate_value = float(_substitute(candidate, {check.symbol: n}).evalf())
        target_value = float(check.target(n))

        denominator = abs(target_value) if target_value != 0.0 else 1.0
        residual = abs(candidate_value - target_value) / denominator
        mismatch = residual > check.tolerance
        note = (
            f"relative residual={residual:.3e} at {check.symbol}={n} "
            f"(candidate={candidate_value}, target={target_value}, tolerance={check.tolerance})"
        )
        return residual, mismatch, note

    @staticmethod
    def _derive_verdict(
        enumeration_match: Optional[bool],
        symbolic_match: Optional[bool],
        mc_triangulates: Optional[bool],
        asymptotic_fit_residual: Optional[float],
        asymptotic_mismatch: bool,
    ) -> Verdict:
        ran = False
        mismatch = False

        for outcome in (enumeration_match, symbolic_match, mc_triangulates):
            if outcome is not None:
                ran = True
                if not outcome:
                    mismatch = True

        if asymptotic_fit_residual is not None:
            ran = True
            if asymptotic_mismatch:
                mismatch = True

        if mismatch:
            return "REFUTED"
        if ran:
            return "SURVIVES"
        return "INCONCLUSIVE"
