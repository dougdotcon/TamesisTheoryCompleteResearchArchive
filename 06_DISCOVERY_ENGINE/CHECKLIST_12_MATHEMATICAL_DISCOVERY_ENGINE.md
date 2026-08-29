# Checklist — Module 12: Mathematical Discovery Engine (Stage 3a)

Source: `ROADMAP.md` §1 Stage 3 product table. "Given a
combinatorial/asymptotic system definition, runs exact enumeration →
symbolic algebra → simulation → asymptotic fitting → proof-candidate
search. Generalizes exactly the `05_DISCOVERY_LAB/02_TESTS/
CORE_NUMERICS` workflow that produced the `U₁/₂` family."

File: `src/tamesis_discovery_engine/mathematical_discovery_engine.py`.
Tests: `tests/test_mathematical_discovery_engine.py`. Builds on Module 6
(`symbolic.py`) and Module 7 (`montecarlo.py`) — read both first.

**Scope honesty constraint (read before writing code):** "proof-candidate
search" does **not** mean an AI system that invents closed-form
candidates on its own — that is not a solved, deterministic problem and
faking it would be dishonest. What this module actually does: given a
**caller-supplied list** of candidate closed-form expressions (e.g. three
different guesses for a limiting formula), it runs each candidate through
the same funnel `05_DISCOVERY_LAB` already uses by hand — exact
enumeration for small cases, symbolic identity checking, Monte Carlo
triangulation for larger cases, and a simple asymptotic-fit residual
check — and reports which candidates survive and which are refuted, with
the evidence. Generating the candidates in the first place is still a
human/agent job, exactly as it is in `05_DISCOVERY_LAB` today.

## Design

- [ ] `CandidateResult` dataclass: `candidate_name`, `enumeration_match:
      Optional[bool]` (`None` if no enumerator was supplied), `symbolic_match:
      Optional[bool]`, `mc_triangulates: Optional[bool]`,
      `asymptotic_fit_residual: Optional[float]`, `verdict:
      Literal["SURVIVES", "REFUTED", "INCONCLUSIVE"]` (a candidate is
      `REFUTED` if ANY stage that ran produced a clear mismatch;
      `SURVIVES` only if every stage that ran agreed; `INCONCLUSIVE` if
      no stage produced a clear result either way — never silently
      default to `SURVIVES` when nothing was actually checked).
- [ ] `MathDiscoveryPipeline.run_candidate(candidate_name, candidate_expr,
      free_symbols, enumerator=None, mc_estimators=None,
      asymptotic_target=None, tolerance=1e-6) -> CandidateResult`:
      1. If `enumerator` is given (a callable `n -> exact_value` plus a
         range of small `n` to check, or similar — design the exact
         signature, document it clearly), compares the candidate
         expression evaluated at each `n` against the enumerator's exact
         value (uses Module 6's `verify_numeric_spot_check` machinery,
         reused not reimplemented).
      2. If `free_symbols`/a target identity is given, runs Module 6's
         `verify_identity` between the candidate and the target.
      3. If `mc_estimators` is given (reuses Module 7's `triangulate`),
         checks the candidate's predicted value triangulates against the
         Monte Carlo estimate(s).
      4. If `asymptotic_target` is given (a callable describing the
         expected limiting behavior), fits/compares the candidate's
         large-`n`/large-parameter behavior against it and reports a
         residual.
      5. Assembles the `CandidateResult`, deriving `verdict` from the
         rule above.
- [ ] `MathDiscoveryPipeline.run(candidates: list[tuple[name, expr]],
      **shared_kwargs) -> list[CandidateResult]`: runs `run_candidate`
      for each supplied candidate against the same shared setup
      (enumerator/mc_estimators/asymptotic_target), returning all
      results — this is the actual "given several candidates, which
      survive" entry point.

## Tests (must all pass)

- [ ] A single true candidate (e.g. the real closed form for a toy
      combinatorial quantity you define for the test, small enough to
      brute-force exactly) run through all four stages reports
      `verdict="SURVIVES"` with every populated field agreeing.
- [ ] A deliberately wrong candidate (differs from the true value at
      some tested `n`) is caught and reports `verdict="REFUTED"`, and
      the specific stage(s) that caught it are visible in the result
      (not just a bare boolean with no attribution).
- [ ] Running `run_candidate` with NO enumerator/mc/asymptotic args
      supplied (only a symbolic identity check) still produces a
      correct `SURVIVES`/`REFUTED` from that one stage, and does not
      crash on the unpopulated optional fields (`enumeration_match` etc.
      stay `None`, not a fabricated `True`).
- [ ] `run()` with 3 candidates (2 true-equivalent forms, 1 wrong) run
      against the same toy problem correctly separates them — the 2
      correct ones `SURVIVES`, the wrong one `REFUTED`.
- [ ] The toy problem's enumerator and Monte Carlo estimator are written
      independently of each other (not one derived by copy-pasting the
      other) — this is the same "genuinely independent evidence, not the
      same check twice" discipline as the rest of this engine.

## Acceptance

- [ ] `pytest tests/test_mathematical_discovery_engine.py -v` passes
      with zero failures.
- [ ] `run_candidate`/`run` never fabricate a `SURVIVES` verdict for a
      candidate where zero stages actually ran (confirm the
      all-stages-`None` case reports `INCONCLUSIVE`, covered by a
      dedicated test, not just asserted in prose here).
- [ ] This module imports `symbolic.py` and `montecarlo.py` rather than
      re-implementing their logic — grep to confirm no duplicated
      `sympy.simplify`/RNG-estimator code exists in this file.
