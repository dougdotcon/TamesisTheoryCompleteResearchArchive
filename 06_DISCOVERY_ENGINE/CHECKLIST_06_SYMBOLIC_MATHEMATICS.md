# Checklist — Module 6: Symbolic Mathematics (Stage 2)

Source: `ROADMAP.md` §1 Stage 2, item 6. "Computer-algebra support
(`sympy`-class tooling) wired directly into the Hypothesis Registry, not
bolted on afterward."

File: `src/tamesis_discovery_engine/symbolic.py`. Tests:
`tests/test_symbolic.py`. Builds on Stage 1's `runner.py` (`TestPlan`) —
read it first. `sympy` is already a project dependency (used throughout
`05_DISCOVERY_LAB`).

The point of this module is concrete: a claim's `TestPlan` (Module 2)
should be able to declare "verify this symbolic identity holds" as its
check, run it through the existing `Runner`, and have Module 3
(Reproduction Engine) re-verify it via a **genuinely different**
verification route — not by wrapping Stage 1's machinery in a thin shell
that does nothing new.

## Design

- [x] `VerificationResult` dataclass: `holds: bool`, `method: str` (e.g.
      `"symbolic_simplify"`, `"numeric_spot_check"`), `detail: str` (the
      simplified difference, or the first failing substitution).
- [x] `verify_identity(lhs, rhs, free_symbols=None) -> VerificationResult`:
      uses `sympy.simplify(lhs - rhs)` (or `.equals()` where applicable)
      to decide if two `sympy` expressions are identically equal. Must
      handle the case where `simplify` cannot decide (report `holds=False`
      with `method="symbolic_simplify_inconclusive"` — never silently
      treat "couldn't simplify" as "holds").
- [x] `verify_numeric_spot_check(lhs, rhs, substitutions: list[dict],
      tolerance=1e-9) -> VerificationResult`: evaluates both sides
      numerically at each given substitution and checks agreement within
      `tolerance`. This is the **genuinely different** verification route
      Module 3 will use to reproduce a symbolic-simplify result — a
      numeric check is not the same proof technique as symbolic
      simplification, satisfying the "second, independent implementation"
      spirit of Module 3's own checklist.
- [x] `make_symbolic_identity_test_plan(name, lhs, rhs, free_symbols=None)
      -> TestPlan`: returns a `TestPlan` (Module 2's type) whose callable
      runs `verify_identity` and returns a dict result compatible with
      `Runner.run()` — this is the actual "wired into the Hypothesis
      Registry" integration point: a claim can be registered, locked, and
      run using this test plan exactly like any other.

## Tests (must all pass)

- [x] `verify_identity` confirms a true identity (e.g.
      `(x+1)**2 == x**2 + 2*x + 1`) with `holds=True`.
- [x] `verify_identity` correctly rejects a false "identity" (e.g.
      `(x+1)**2 == x**2 + 2*x + 2`) with `holds=False` and a nonzero
      `detail`.
- [x] `verify_numeric_spot_check` confirms the same true identity at
      several substitutions, and correctly flags the false one at the
      substitution where it first diverges.
- [x] A claim driven through `Runner.lock()`/`Runner.run()` using a
      `TestPlan` from `make_symbolic_identity_test_plan` produces a
      `RunRecord` whose result reflects the identity's truth value —
      i.e. this module genuinely integrates with Stage 1's `Runner`, not
      just its own standalone functions.
- [x] Reproducing a true-identity claim via `verify_numeric_spot_check`
      as the "second implementation" (Module 3's `Reproducer`) yields a
      match; reproducing a claim whose original symbolic check was WRONG
      (a deliberately buggy `verify_identity` call, e.g. a typo'd `rhs`)
      is caught as a `MISMATCH` by the numeric route — proving the two
      methods are genuinely independent, not the same check twice.

## Acceptance

- [x] `pytest tests/test_symbolic.py -v` passes with zero failures.
- [x] `verify_identity` never returns `holds=True` for an identity
      `sympy.simplify` could not actually confirm — grep the
      implementation to confirm there is no fallback that defaults to
      `True` on an inconclusive simplify.
