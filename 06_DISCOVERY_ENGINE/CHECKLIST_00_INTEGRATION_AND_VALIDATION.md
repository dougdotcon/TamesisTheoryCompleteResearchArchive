# Checklist — Integration + the required Stage 1 benchmark

Source: `ROADMAP.md` §1 Stage 1 ("Required validation before Stage 1
counts as done") and §3 ("Why `U₁/₂` is the required first benchmark,
not an example"). This is the acceptance gate for the whole MVP, not
just one more module — **do not mark Stage 1 done in `GOAL.md` until
every box below is checked and the tests actually pass when run.**

Depends on Modules 1–5 all being complete (their own checklists fully
checked off, their own tests green).

## Integration

- [x] `src/tamesis_discovery_engine/__init__.py` exposes a small
      `DiscoveryEngine` facade wiring `Registry`, `Runner`, `Reproducer`,
      `AdversarialReviewer`, and `Ledger` together, all sharing one
      `data/` directory root passed at construction. Each module's
      major event (claim created, claim advanced, run completed,
      reproduction completed, review run, verdict recorded) appends one
      entry to the shared `Ledger` — wire this here, inside the facade,
      not by modifying Modules 1–4's own internals to import `Ledger`
      directly (keep the modules independently testable in isolation,
      as their own checklists already verified).
- [x] `tests/test_integration.py`: a claim driven through the **entire**
      state machine via the `DiscoveryEngine` facade
      (`DRAFT→...→CONFIRMED` or a deliberately `REFUTED`/`INCONCLUSIVE`
      path) and the `Ledger` ends up with one entry per major event, in
      the correct order, chain-verifiable.

## The required benchmark — reproduce `U₁/₂` end-to-end, no hand-holding

This is not optional and not a formality. Per `ROADMAP.md` §3: *"If a
candidate Discovery Engine cannot re-derive what this archive's own
manual pipeline already proved and adversarially confirmed, it has no
business being pointed at an unproven hypothesis."*

- [x] `benchmarks/u12_hypothesis.py`: an **independent** implementation
      of the `u12` permutation-with-reroutes ensemble (Definitions 1–4
      in `THEOREM.md` — read the definitions directly from
      `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/THEOREM.md`
      to get them right, but do **not** import any code from
      `05_DISCOVERY_LAB`, and do **not** hardcode `THEOREM.md`'s stated
      closed-form answers as the computation itself — only as the
      comparison target of an assertion at the very end). Must include:
      1. A brute-force / exact-enumeration function for small `n`
         computing the exact CDF of `M_n^{(0)}` (or `M_n` generally),
         used to sanity-check the closed form directly against ground
         truth for `n` small enough to enumerate exhaustively.
      2. A Monte Carlo simulator for larger `n`, used to check
         convergence of the empirical distribution toward `φ_∞(c)` as
         `n→∞` for fixed `c`.
      3. The closed form itself, `φ_∞(c) = ½·√(π/c)·erf(√c)`, coded
         directly from the formula (this is fine to hardcode — it's the
         *target*, not the computation being validated).
- [x] `tests/test_u12_end_to_end.py` drives the full claim lifecycle
      through `DiscoveryEngine`:
      1. `register()` a claim whose `statement` is the bare `U₁/₂`
         hypothesis (`φ_∞(c) = ½·√(π/c)·erf(√c)` as `n→∞`).
      2. `advance()` to `PRE_REGISTERED` with a declared threshold
         (e.g. "empirical CDF within `1e-2` of `φ_∞(c)` for `n≥N`" and
         "brute-force exact CDF within `1e-9` of `φ_∞(c)`'s finite-`n`
         correction term for small `n`").
      3. `advance()` to `LOCKED`, `run()` the test plan calling into
         `benchmarks/u12_hypothesis.py`'s brute-force + Monte Carlo
         functions (not pre-computed numbers).
      4. `reproduce()` with a second, independently-written
         implementation of at least the brute-force check (e.g. a
         different enumeration order/algorithm for the same
         combinatorial definition).
      5. `review()` then `record_verdict()`.
      6. **Assert**, at the end, that the computed values from step 3
         match the closed forms cited in `THEOREM.md`:
         - `φ_∞(c)` (brute-force/MC vs. the formula) — required.
         - The `M_K` distribution for at least one `K≥1` case (e.g.
           `K=1`, `f_{M_1}` — check the exact closed form actually
           cited in `THEOREM.md`) — required per `ROADMAP.md` §3 item 2.
         - At least one finite-`n` correction term, compared against the
           value stated in `THEOREM.md` for that `n` — required per
           `ROADMAP.md` §3 item 3.
         - The `γ=c/n` scaling regime: run the simulator at fixed `γ`
           across a few growing `n`, confirm `φ(n,γn)/φ_∞(γn) →
           √(2/(2-γ))` in the right direction — required per
           `ROADMAP.md` §3 item 4.
- [x] If **any** of the four required checks cannot be made to pass
      honestly (not adjusted by loosening tolerance until it passes),
      that failure is recorded explicitly in this checklist and in
      `GOAL.md` as an open gap — **do not silently drop a failing
      check or claim Stage 1 complete with an unmet requirement.**
      (No such failure occurred: all four required checks — `φ_∞(c)`,
      the `M_1` distribution, the `φ_n^{(1)}` finite-`n` correction, and
      the `γ=c/n` scaling ratio — pass honestly with the tolerances
      declared at pre-registration time; see
      `tests/test_u12_end_to_end.py`.)

## Acceptance

- [x] `pytest 06_DISCOVERY_ENGINE/tests/ -v` — full suite, zero
      failures, zero skips (a "skip" on the benchmark test specifically
      is not acceptable; it must actually run and assert). Verified:
      `python3 -m pytest tests/ -v` → 77 passed, 0 skipped (~50s),
      re-run twice for determinism.
- [x] `benchmarks/u12_hypothesis.py` contains no `import` from
      `05_DISCOVERY_LAB` anywhere (grep to confirm) and no numeric
      literal that is one of `THEOREM.md`'s stated results used as
      anything other than an assertion target (spot check a few
      literals by hand). Verified: `grep -rn "05_DISCOVERY_LAB"
      benchmarks/` finds only doc-string prose (no `import`); the four
      closed-form literals (`0.5*sqrt(pi/c)*erf(sqrt(c))`,
      `4**K*(K!)^2/(2K+1)!`, `2/3+1/(3n^2)`, `sqrt(2/(2-gamma))`) live
      only in the "Closed-form targets" section at the bottom of the
      module and are never referenced by `brute_force_*` or
      `monte_carlo_*` above them.
- [x] A short adversarial review pass (separate from Module 4's own
      unit tests — this is a review of the *engine's own honesty*, done
      by a reviewer who did not write the benchmark code) confirms the
      benchmark genuinely recomputes its answers rather than smuggling
      in the known result. This is the hostile-review step for the
      whole Stage 1 deliverable, not just its individual modules.
      **Done, correctly, by a separately-dispatched agent** (not the one
      that wrote the benchmark): re-read every module and test file in
      full, independently re-verified `THEOREM.md`'s closed forms by
      hand against `benchmarks/u12_hypothesis.py`'s "Closed-form
      targets" section, confirmed no fabricated/tautological tests
      anywhere, confirmed the state machine has no verdict-without-
      review bypass — and found one genuine HIGH-severity defect
      unrelated to the benchmark itself: `Ledger.verify_chain()` could
      not detect tampering with the most recently appended (tail)
      entry, since hash-chaining only protects an entry via its
      *successor's* `prev_hash`, and the tail has none. Verdict:
      `SOUND_WITH_ISSUES`. Fixed by a third, separately-dispatched agent
      (tail-hash commitment file, `TamperDetectedError` on mismatch,
      plus a new regression test targeting the tail specifically,
      red/green-verified) — see `src/tamesis_discovery_engine/ledger.py`
      and `tests/test_ledger.py::test_tampering_with_the_last_persisted_entry_is_detected_by_a_fresh_ledger`.
      **Independently re-confirmed by the orchestrating session**
      (2026-08-29): re-ran the full suite (78 passed), reconstructed the
      tail-tamper scenario from scratch in a throwaway script (not
      reusing the fix agent's own test) and confirmed `verify_chain()`
      now raises `TamperDetectedError` on tail tampering.
