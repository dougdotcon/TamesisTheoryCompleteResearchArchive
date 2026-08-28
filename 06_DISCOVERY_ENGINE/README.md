# Tamesis Discovery Engine — Stage 1 MVP

**Status: under active construction, per `../GOAL.md`. Do not treat
anything here as validated until its own checklist is fully checked off
and its tests pass — see the per-module `CHECKLIST_*.md` files in this
directory and the acceptance gate in
`CHECKLIST_00_INTEGRATION_AND_VALIDATION.md`.**

This is a real, tested Python implementation of the 5-module MVP
described in `../ROADMAP.md` §1 Stage 1 ("Tamesis Discovery Engine v1"):
a minimal software encoding of the pre-registration → adversarial-review
→ decision-ledger workflow `05_DISCOVERY_LAB` already runs by hand.

## Why this exists, and what it is not

This is **software-correctness work, not a new mathematical claim**. It
does not get an entry in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml` — that ledger is
for claims about the world (or about `u12`/`M_K` combinatorics); this is
a claim about whether some Python code behaves as specified, verified by
its own test suite. See `../GOAL.md` for the tracking discipline this
build follows.

It is **not** wired to `05_DISCOVERY_LAB`'s existing scripts. The
required validation benchmark
(`tests/test_u12_end_to_end.py`, `benchmarks/u12_hypothesis.py`)
independently recomputes the `U₁/₂` result from the bare combinatorial
definitions and only compares against `THEOREM.md`'s stated closed forms
as an assertion target — see `ROADMAP.md` §3 for why that distinction
matters and `CHECKLIST_00_INTEGRATION_AND_VALIDATION.md` for how it is
enforced.

## Layout

```
06_DISCOVERY_ENGINE/
  src/tamesis_discovery_engine/
    registry.py        — Module 1: Hypothesis Registry (claim state machine)
    runner.py           — Module 2: Experiment Runner
    reproduction.py      — Module 3: Reproduction Engine
    adversarial.py        — Module 4: Adversarial Reviewer
    ledger.py               — Module 5: Decision Ledger (hash-chained, append-only)
    __init__.py               — DiscoveryEngine facade wiring the five together
  tests/                        — one test file per module + integration + the
                                    required U1/2 end-to-end benchmark
  benchmarks/                    — independent U1/2 combinatorics, used only by
                                     the required validation test
  data/                           — runtime state (claims, runs, ledger); not
                                      committed content, created at runtime
  CHECKLIST_01..05_*.md             — one detailed checklist per module
  CHECKLIST_00_INTEGRATION_AND_VALIDATION.md — the Stage 1 acceptance gate
```

## Running the tests

```
cd 06_DISCOVERY_ENGINE
python3 -m pytest tests/ -v
```

## State machine

```
DRAFT → PRE_REGISTERED → LOCKED → RUNNING → RESULT → ADVERSARIAL_REVIEW
                                                              │
                                                              ▼
                                    {CONFIRMED | REFUTED | INCONCLUSIVE | NULL}
```
