# Checklist — Module 9: Formal Proof / Lean Bridge (Stage 2)

Source: `ROADMAP.md` §1 Stage 2, item 9. "A bridge from a CONFIRMED
claim into `04_FORMAL_RESEARCH_LAB`-style Lean4 formalization, for the
subset of results with a genuine mathematical core (this archive already
draws this line explicitly; the module should enforce it, not blur it)."

File: `src/tamesis_discovery_engine/lean_bridge.py`. Tests:
`tests/test_lean_bridge.py`.

**Hard scope boundary, non-negotiable:** this module must NEVER write
into, modify, or execute a build against
`04_FORMAL_RESEARCH_LAB/` — that is the archive's own real, governed
Lean formalization line with its own history and provenance; generated
engine stub files have no business there. This module manages its own,
completely separate Lean project directory under
`06_DISCOVERY_ENGINE/lean_scratch/` (a minimal skeleton — a
`lean-toolchain` file pinned to the same version as the one already
installed in this environment, and either a trivial `lakefile.toml` or,
if a bare `lean` invocation with no project/Mathlib dependency is
sufficient for the trivial statements this bridge checks, no `lakefile`
at all — verify empirically which is simplest and document the choice
in the module docstring). Generated per-claim `.lean` files go under
`06_DISCOVERY_ENGINE/lean_scratch/generated/` and are **not** committed
to git (add that path to `06_DISCOVERY_ENGINE/.gitignore` if it isn't
covered already) — they're reproducible from a claim's own record, not
source of truth. Before writing any code, run `lean --version` and a
throwaway trivial `.lean` file through `lean <file>.lean` (or the
Lake-based route if you determine a project is actually needed) to
confirm the mechanism you intend to use actually works in this
environment — do not assume.

## Design

- [x] `LeanFormalizationResult` dataclass: `compiled: bool`,
      `stdout: str`, `stderr: str`, `duration_seconds: float`,
      `lean_file_path: str`.
- [x] `LeanBridge(scratch_dir=...)`: manages the isolated scratch project
      described above (created on first use if absent).
- [x] `LeanBridge.formalize(claim_id, lean_source: str, theorem_name: str)
      -> LeanFormalizationResult`. **Enforced precondition:** raises
      unless the claim (looked up via Stage 1's `Registry`) is in state
      `CONFIRMED` — this is the literal ROADMAP.md requirement ("a
      bridge from a CONFIRMED claim"), and it is what "enforces the line
      rather than blurring it": a claim that is merely `RESULT` or even
      `ADVERSARIAL_REVIEW`-passed-but-not-yet-verdicted has no business
      being formalized as if it were an accepted fact. Writes
      `lean_source` to a new file under
      `lean_scratch/generated/{claim_id}.lean`, invokes the verified
      compilation mechanism, captures stdout/stderr/exit code/timing,
      returns the result. A failing compile is reported honestly in
      `compiled=False` with the real compiler output — never swallowed,
      never silently retried with a "fixed" version of the source.
- [x] Record the outcome via Stage 1's `Ledger` (one entry per
      `formalize()` call, decision_type e.g. `"LEAN_FORMALIZE"`,
      summarizing compiled/failed) — this module does not invent its own
      persistence for outcomes; it reuses Stage 1's existing ledger.

## Tests (must all pass)

- [x] Formalizing a trivial, genuinely true statement (e.g.
      `theorem <name> : (1:Nat) + 1 = 2 := by decide`, or an equally
      minimal true fact requiring no `Mathlib` import) against a
      `CONFIRMED` claim succeeds: `compiled=True`.
- [x] Formalizing a deliberately false statement (e.g.
      `theorem <name> : (1:Nat) + 1 = 3 := by decide`) against a
      `CONFIRMED` claim fails to compile: `compiled=False`, and
      `stderr`/`stdout` contains the real Lean error, not a
      generic/fabricated message.
- [x] Formalizing a malformed (syntactically invalid) Lean source also
      fails to compile with `compiled=False`, distinctly from the
      false-but-well-formed case (both must be `False`, but confirm the
      module doesn't crash/raise an unhandled exception on syntax
      errors — a compile failure is an expected, handled outcome, not a
      bug).
- [x] Attempting `formalize()` on a claim in any state other than
      `CONFIRMED` (e.g. `DRAFT`, `RESULT`, `REFUTED`) raises, without
      invoking the Lean compiler at all.
- [x] A successful `formalize()` call appends exactly one `Ledger` entry
      for that claim; a failed one still appends an entry (recording the
      failure honestly), not silently skipping the ledger on failure.

## Acceptance

- [x] `pytest tests/test_lean_bridge.py -v` passes with zero failures.
      (These tests genuinely shell out to the `lean`/`lake` binary — they
      will be slower than the rest of the suite; that's expected, not a
      bug. If a single compile takes long enough to make the test suite
      impractically slow, say so honestly in this checklist and in the
      module docstring rather than skip the test.) Verified: 13/13 passed
      in 2.79s standalone (page cache already warm from the pre-flight
      probe); the one genuinely slow cost is a one-time ~18s `lean`
      cold-start the very first time any process invokes it in a fresh
      environment, not a per-compile cost — see the module docstring's
      "Timing" section. Not impractically slow.
- [x] `grep -rn "04_FORMAL_RESEARCH_LAB" src/tamesis_discovery_engine/lean_bridge.py`
      finds no path ever opened for writing — read-only references (if
      any, e.g. citing it in a docstring) are fine; write access is not.
      Verified: the only two hits are both prose inside the module
      docstring (lines 18 and 45), neither is ever passed to `open`,
      `write_text`, `subprocess.run`, or any other write/execute call.
