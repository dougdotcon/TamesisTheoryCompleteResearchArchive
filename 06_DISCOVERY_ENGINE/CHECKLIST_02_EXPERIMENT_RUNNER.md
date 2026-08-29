# Checklist — Module 2: Experiment Runner

Source: `ROADMAP.md` §1 Stage 1, item 2. "Executes a pre-registered,
locked test plan against declared data/code."

File: `src/tamesis_discovery_engine/runner.py`. Tests:
`tests/test_runner.py`. Depends on Module 1 (`registry.py`).

## Design

- [x] A `TestPlan` object: a Python callable (`fn(**params) -> dict`)
      plus declared `params` (dict), and metadata identifying it (a
      name/version string). The callable's source is hashed (e.g.
      `hashlib.sha256` of `inspect.getsource(fn)`) at `LOCKED` time and
      the hash stored on the claim — this is the tamper-evidence
      mechanism: if the test plan's source changes after locking, the
      hash mismatches on `run()` and the run is refused.
      (Implementation note: `Registry` exposes no API to attach data to
      a persisted claim beyond `create()`, so `Runner.lock()` — which
      performs the `PRE_REGISTERED → LOCKED` transition via
      `Registry.advance` — persists the captured hash in its own
      `LockRecord`, keyed by claim id, rather than reaching into
      `Registry`'s private storage to graft it onto `claim.metadata`.
      This is documented in `runner.py`'s module docstring.)
- [x] `Runner.run(claim_id, test_plan) -> RunRecord`:
      1. Loads the claim; **raises** if not in `LOCKED` state (a
         runner must never execute against a `DRAFT` or `PRE_REGISTERED`
         claim — that's the whole point of locking before running).
      2. Recomputes the test plan's source hash and compares to the one
         stored at lock time; raises `TestPlanTamperedError` on mismatch.
      3. Transitions `LOCKED → RUNNING`.
      4. Executes the callable, capturing start/end wall-clock time,
         the raw return value, and any raised exception.
      5. On success: transitions `RUNNING → RESULT`, persists a
         `RunRecord` (claim_id, params, result payload, start/end time,
         source hash) linked to the claim.
      6. On exception: the claim does **not** silently stay `RUNNING`
         forever and the exception is **not** swallowed — either
         re-raise after recording a failed `RunRecord` (with the
         exception's type/message captured), or transition to a
         distinguishable failure marker. Pick one behavior and test it;
         do not let a raised exception vanish.
      (Chose: record the failed `RunRecord`, then re-raise the original
      exception; the claim is left in `RUNNING`, which the existing
      state machine never lets a successful run leave stale, so it is
      distinguishable from `RESULT` without inventing a new state.)
- [x] `RunRecord` persisted the same way `Registry` persists claims
      (JSON under `data/runs/`), retrievable by claim id.

## Tests (must all pass)

- [x] Running a `LOCKED` claim with a working test plan transitions it
      to `RESULT` and the `RunRecord` contains the correct params and
      result payload.
- [x] Running a `DRAFT` (or any non-`LOCKED`) claim raises immediately,
      without executing the test plan callable at all (assert the
      callable was never invoked, e.g. via a call counter).
- [x] Locking a claim, then mutating the test plan's source (e.g.
      redefining the function with different logic) before calling
      `run()`, raises `TestPlanTamperedError` — this is the "no
      post-hoc rewriting after locking" check.
- [x] A test plan that raises an exception during execution: the
      exception is not silently swallowed (either it propagates, or is
      captured visibly in the `RunRecord` — assert whichever contract
      the design picked) and the claim's state reflects the failure
      distinctly from a normal `RESULT`.
- [x] `RunRecord` persistence round-trip (write, reload in a fresh
      `Runner`, get identical record).

## Acceptance

- [x] `pytest tests/test_runner.py -v` passes with zero failures.
- [x] `run()` never proceeds to execute a test plan without first
      validating both the claim's state and the source hash — cover
      both checks with a dedicated test each, not one combined test.
