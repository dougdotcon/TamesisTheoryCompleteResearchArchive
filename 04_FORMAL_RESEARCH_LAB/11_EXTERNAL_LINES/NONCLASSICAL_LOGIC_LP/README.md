# LP-001 — Priest's Logic of Paradox in Lean4

**A new, standalone Lean4 formalization of Priest's LP (Logic of Paradox),
the classic 3-valued paraconsistent logic.**

## Scope note (read this first)

This line is tracked **only** in `05_DISCOVERY_LAB` — `DISC-DEC-102` in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, and
`PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §3.1 for the choice
rationale (LP over modal logic, to avoid duplicating the mature,
actively-maintained `github.com/FormalizedFormalLogic/Foundation`; LP
over fuzzy logic, on formalization-cost grounds). It is **not** entered
into `04_FORMAL_RESEARCH_LAB/00_GOVERNANCE/` or
`04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/RESEARCH_QUEUE.yaml` — that lab's
own ledgers, conventions (`formalization_cost`, `phase_status`, per-item
line ceilings), and portfolio gate are deliberately untouched by this
work. This directory exists purely as a **documentation home** — a
lightweight README + `RESULTS.md`, not the multi-document portfolio-gate
apparatus used by `02_FOUNDATIONS/NN_.../FOUND_*_001/` items (compare
e.g. `02_FOUNDATIONS/08_BISIMULATION/FOUND_BISIMULATION_BOUNDARY_001/`,
which carries `STATUS.yaml`, `GAP_REGISTER.yaml`, `CLAIM_BOUNDARY.md`,
four review gates, etc.). This line has not gone through that gate and
does not claim to have.

## Where the actual Lean code lives, and why

`lake`'s module resolution requires source files to live under the
package's existing source tree for the module path to resolve
(`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/`, package `TamesisLab`,
`lean_lib` rooted at `TamesisLab/`). The physical `.lean` files are
therefore at:

```
04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/ExternalLines/NonclassicalLogicLP/
├── Definitions.lean       LPVal, connectives, Formula, eval, Sat, Entails, Valid
├── ValidTheorems.lean     LEM, LNC, DNE/DNI, adjunction, ∧-elim, ∨-intro (survivors)
├── Countermodels.lean     explosion / MP / disjunctive syllogism INVALID (the point)
├── CollapseTheorem.lean   classical recapture under B-free valuations
├── Audit.lean             truth-table cross-check + #check + #print axioms
└── (aggregator one level up: TamesisLab/ExternalLines/NonclassicalLogicLP.lean)
```

This is **infrastructure reuse**, not a claim on `02_FOUNDATIONS/`'s
numbered track: the namespace is `TamesisLab.ExternalLines.NonclassicalLogicLP`,
a sibling of `TamesisLab.Foundations`/`TamesisLab.Engineering`/etc., not
nested inside either. The single change made to a file this lab already
owns is one import line added to the root shim
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab.lean` (adding
`import TamesisLab.ExternalLines.NonclassicalLogicLP`, following the
exact convention every other subsystem there already uses), so that
`lake build`'s default target picks the new files up — the same
mechanism this lab already relies on for `Foundations`, `Riemann`,
`RHNogo`, etc. No file under `04_FORMAL_RESEARCH_LAB/00_GOVERNANCE/` or
`04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/` was touched.

If this split (governance docs here, source there) is unwanted, it is
reversible at no cost — nothing beyond this note and the DISC-DEC-102
ledger entry has been locked.

## What was formalized

Priest's LP: three truth values `{T, B, F}` (`F < B < T`), negation as
an involution, conjunction/disjunction as min/max, a **derived** (not
primitive) material conditional `a → b := ¬a ∨ b`, designated values
`D = {T, B}`, and the standard `eval`/`Sat`/`Entails`/`Valid` semantic
stack over an arbitrary atom type. See `RESULTS.md` for the full
meta-theorem list, build log, `sorry`/`admit` grep, and axiom audit.

## References

* Graham Priest, "The Logic of Paradox", *Journal of Philosophical
  Logic* 8 (1979), 219–241.
* Stanford Encyclopedia of Philosophy, "Paraconsistent Logic",
  https://plato.stanford.edu/entries/logic-paraconsistent/, §3.
