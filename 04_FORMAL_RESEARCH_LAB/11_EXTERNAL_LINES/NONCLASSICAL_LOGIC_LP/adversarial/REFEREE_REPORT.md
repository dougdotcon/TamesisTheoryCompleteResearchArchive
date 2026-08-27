# LP-001 — Adversarial Referee Report

**Reviewer role:** hostile adversarial referee, independent of the authoring
front. Task: refute, not confirm. This report covers only the mathematical
and documentary content of `TamesisLab/ExternalLines/NonclassicalLogicLP/`
(6 files, 876 lines) and its governance docs at
`04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/`. The
build-passes / zero-`sorry` / standard-axiom-footprint claims were already
independently confirmed twice (front + orchestrating session) before this
review started; this review re-spot-checked those (see §6) but its primary
job was mathematical content, not re-running `lake build`.

**Date of review:** 2026-08-27. **Branch:**
`claude/lean4-pesquisa-ultima-parada-njox09`.

---

## Verdict

**SOUND WITH NAMED ISSUES.**

Every formally verified Lean theorem in this line is **true** and **states
what its name/docstring claims** for the semantics actually implemented
(3-valued LP with `F<B<T`, `neg`/`and`/`or` as involution/min/max, a
*derived* material conditional `a→b := ¬a∨b`, `D={T,B}`). All twelve
headline meta-theorems were checked by hand against Priest (1979) and the
SEP "Paraconsistent Logic" entry, and independently re-derived in a fresh,
from-scratch Lean file (compiled clean, 0 errors, standard axiom
footprint) plus an independent brute-force computational search. No
theorem statement is vacuous, no `Entails`/`Sat`/`Valid` definition is
subtly wrong, no countermodel witness fails to witness what it claims, and
the collapse theorem is a genuine, correctly-quantified (arbitrary `Atom`,
arbitrary `Γ`/`φ`) two-way `iff`, not a narrowed or one-sided restatement.

One real issue was found, in the **documentation**, not in any formally
verified statement:

| # | Issue | Severity |
|---|---|---|
| 1 | `CollapseTheorem.lean`'s docstring on `valid_implies_cvalid` asserts "the converse fails" for `CValid φ → Valid φ`, and justifies this with an *entailment*-level example that does not actually establish it. Extensive independent testing (literature + a from-scratch Lean proof + a 300k+-formula brute-force search) finds **no counterexample** and strongly supports that this converse in fact *holds* (LP and classical logic have exactly the same valid formulas — a well-known, independently-citable fact about LP). The claim as written is unsupported and most likely false. | **MODERATE** |

Nothing here invalidates any of the 12 proven theorems, the countermodel
claims, or the collapse `iff`. Issue 1 is a false or unsupported claim
*about* the mathematics in a comment, not a bug in the mathematics itself
— but it is exactly the kind of thing a type-checker cannot catch, it
mischaracterizes what is and is not established, and a future reader could
easily take it as settling a question (formula-level classical recapture)
that is, if anything, settled the *other* way.

---

## 1. Truth tables vs. Priest (1979) / SEP "Paraconsistent Logic" §3

Checked `Definitions.lean`'s `neg`/`and`/`or`/`imp` against the standard
LP presentation (values `{T,B,F}`, order `F<B<T`, `D={T,B}`,
`∧`=min, `∨`=max, `¬` an involution swapping `T`/`F` and fixing `B`,
material conditional `a→b := ¬a∨b`):

```
neg: T↦F, B↦B, F↦T                    — matches (involution)
and: min under F<B<T (T,T)=T (T,B)=B (T,F)=F
                      (B,T)=B (B,B)=B (B,F)=F
                      (F,T)=F (F,B)=F (F,F)=F   — matches exactly
or:  max under F<B<T (T,_)=T
                      (B,T)=T (B,B)=B (B,F)=B
                      (F,T)=T (F,B)=B (F,F)=F   — matches exactly
imp: def imp a b := (neg a).or b       — the derived ¬a∨b, NOT an
                                          independent truth table
```

`Definitions.lean`'s `and`/`or` are given as explicit pattern-matched
3×3 tables, with `and_eq_min`/`or_eq_max` proved (not assumed) equal to
`min`/`max` under the installed order. `imp` is a one-line derived
definition, `(neg a).or b` — confirmed by reading the code (§ line 106 of
`Definitions.lean`) that there is **no** independent/primitive truth
table for `→` anywhere; `Audit.lean`'s 9-cell `imp` table is checked by
`decide` against this same derived definition, not against a second,
independently-typed table. This is exactly what the task asked to rule
out, and it is ruled out.

Cross-checked against two independent secondary-source searches (web
search results below, §8) confirming Priest's own tables and the D={T,B}
designation convention. All 30 audited cells (3+9+9+9) are correct.

## 2. The twelve meta-theorems — statement-level check (not just "it compiles")

Read every theorem STATEMENT, not the front's prose summary, in
`ValidTheorems.lean`, `Countermodels.lean`, `CollapseTheorem.lean`.

- **`explosion_invalid`**: `∃ a b : Bool, a ≠ b ∧ ¬ Entails [atom a, (atom a).neg] (atom b)`.
  `Entails` is the genuine designated-value definition
  (`∀ v, (∀ψ∈Γ, Sat v ψ) → Sat v φ`, `Sat v φ := eval v φ ∈ D`) — not
  vacuous, not trivially true (checked the definition directly in
  `Definitions.lean`, not trusted from the docstring). The existential
  quantifier is the *correct* shape for an invalidity claim (one
  countermodel suffices) — this is not a case of `∃`/`∀` confusion.
- **`mp_invalid`**: uses `(Formula.atom a).imp (Formula.atom b)`, i.e. the
  `Formula.imp` constructor, which evaluates through the *derived*
  `LPVal.imp` (`eval_imp` in `Definitions.lean`) — confirmed this is the
  derived conditional, not some other implication.
- **Witness `a↦B, b↦F` — hand-verified independently** (not trusting the
  Lean proof):
  - Explosion: `Sat(atom a)=B∈D` ✓, `Sat(¬a)=neg(B)=B∈D` ✓,
    `Sat(atom b)=F∉D` ✗ → premises hold, conclusion fails → invalid. ✓ matches.
  - MP: `imp(atom a)(atom b) = imp(B,F) = neg(B) or F = B or F = B ∈ D` ✓
    (premises: `a`=B∈D, `a→b`=B∈D), conclusion `b`=F∉D → invalid. ✓ matches.
  - Disjunctive syllogism: `or(atom a)(atom b) = or(B,F) = B ∈ D` ✓,
    `neg(atom a)=B∈D` ✓, conclusion `b`=F∉D → invalid. ✓ matches.
  All three by-hand computations confirm the single shared witness really
  does witness all three invalidities, exactly as claimed.
- **`imp_neg_imp_valid` / `deduction_theorem_breakdown`**: hand-verified
  `x → (¬x → y)` is designated for **all** `x,y ∈ LPVal` (case-by-case:
  `x=T`→ outer `neg(T) or (...)` = `F or T = T`; `x=B`→ `neg(B) or (B or
  y) = B or {T or B} = B` regardless of `y`; `x=F`→ `neg(F) or (...) = T
  or ... = T`) — genuinely valid as a *formula*, for every substitution
  instance, not a narrow/finite-only fact. `deduction_theorem_breakdown`
  is literally `⟨imp_neg_imp_valid, explosion_invalid⟩` — an honest
  conjunction of two independently-meaningful, non-trivial facts (the
  valid conditional-form vs. the invalid inference-form), not a vacuous
  restatement of either half.
- **LEM (`lem_valid`)** and **LNC-as-schema (`lnc_valid`)**: hand-verified
  `or(x, neg x) ∈ D` and `neg(and(x, neg x)) ∈ D` for all three `x` —
  both correct and both match the textbook fact that LP retains LEM/LNC
  as valid schemas while tolerating `φ∧¬φ` as *satisfiable* (at `B`).
  This is a real, subtle point about LP (paraconsistent ≠ paracomplete)
  and the file gets it right.
- **Adjunction / ∧-elim / ∨-intro**: straightforward, correctly stated as
  entailments (not formula-validities), correctly proved from the
  `and_mem_D`/`or_mem_D_*` value-level lemmas.

No unused-hypothesis vacuity, no `Decidable`-instance mismatch, no
`∃`/`∀` swap was found anywhere in this file set.

## 3. The collapse theorem — quantification and direction check

```
theorem collapse (Γ : List (Formula Atom)) (φ : Formula Atom) :
    BooleanEntails Γ φ ↔ BEntails Γ φ
```
sits inside `variable {Atom : Type*}` — i.e. it is stated for an
**arbitrary** atom type and **arbitrary** `Γ`/`φ`, not specialized to a
finite/tiny instance the way a `decide`-only proof would have to be
(`Formula Atom` is infinite, so this genuinely cannot be `decide`d; it is
proved by real structural induction — `eval_ne_B`, `toBool_eval` — over
the formula grammar). Both directions of the `constructor` block are used
non-trivially (`mp`: given `BooleanEntails`, produce a `BEntails` witness
by lifting a classical valuation to a Boolean LP valuation via `ofBool`;
`mpr`: the reverse projection via `toBool`) — this is a genuine two-way
`iff`, not an `Iff` where only the trivial direction was needed.

`Boolean v := ∀ a, v a ≠ B` is the correct "B-free" reading, and
`BooleanEntails` quantifies over `Boolean v` (not vacuously — `Boolean`
is satisfiable, e.g. by any `ofBool ∘ b`). The homomorphism lemmas
(`toBool_neg`, `toBool_and`, `toBool_or`, `toBool_imp`) are each proved by
a genuine 1-2 case `decide`, all correctly guarded by `≠ B` hypotheses.

`valid_implies_cvalid : Valid φ → CValid φ` — the "cheap corollary" — is
correctly derived as `Valid φ`'s universal quantifier restricted to the
Boolean-valuation subset, composed with `collapse`. This is real and
correctly scoped (not specialized to a finite instance; `Atom` remains
arbitrary).

**The one issue found** is in the prose attached to this theorem — see
Verdict §1 above and §4 below.

## 4. The "converse fails" claim — the one real finding

`CollapseTheorem.lean`, docstring on `valid_implies_cvalid`:

> "Every LP-valid formula is classically valid. (**The converse fails**:
> `φ.imp (φ.neg.imp ψ)` shows a formula can be valid in both, while e.g.
> the *inference* `φ, ¬φ ⊢ ψ` is classically sound but not LP-sound...
> so the two notions of validity genuinely diverge once inferences, not
> just single formulas, are in view.)"

Read literally, "the converse" of `Valid φ → CValid φ` is
`CValid φ → Valid φ`. The justification offered is about *entailment*
(`φ,¬φ⊢ψ`), which never bears on whether a single formula can be
classically valid without being LP-valid — no such formula is exhibited,
anywhere in the six files. This is either (a) a false claim about
formula-level validity, or (b) true but attached to the wrong theorem —
a real fact about entailment-level divergence (already correctly
established by `Countermodels.lean`) mislabeled as "the converse" of a
formula-level corollary it isn't the converse of. Either reading is a
documentation defect worth flagging.

It is also, as far as this reviewer can establish, **not true that the
converse fails**. The standard fact in the paraconsistent-logic
literature (independently searched, not taken from the front's own
`Audit.lean` citations — see §8) is that **LP and classical logic have
exactly the same valid formulas**; only the consequence relation (which
formula follows from which premises) differs. That is, `Valid φ ↔ CValid
φ` should hold as a full `iff`, not merely the one direction proved here.

Three independent checks were run to test this, none of which found a
counterexample:

1. **Literature.** Two web searches (queries and results/sources in §8)
   both return, from multiple independent secondary sources (an arXiv
   survey of paraconsistent logics, notes on LP, SEP-adjacent material):
   "LP and similar logics have the same tautologies as classical logic,
   though their consequence relations are different" — i.e. formula-level
   validity coincides; only entailment diverges.
2. **Brute-force computational search** (`adversarial/lp_collapse_search.py`,
   `adversarial/lp_collapse_search_extra.py`, both saved alongside this
   report): exhaustively enumerated all formulas up to size 4 over 2
   atoms (56,842 formulas), up to size 6 over 1 atom with deep negation
   nesting (299,713 formulas), and up to size 2 over 3 atoms (603
   formulas). **Zero** counterexamples to `CValid φ → Valid φ` in any of
   the three sweeps (and, as a sanity re-check of the *proven* direction,
   zero counterexamples to `Valid φ → CValid φ` either).
3. **A from-scratch, independently-compiled Lean proof** of the
   easy/proven direction (`ref_valid_implies_cvalid` in
   `adversarial/RefereeCheck.lean`, disjoint proof from the audited
   `valid_implies_cvalid`), plus four concrete `decide`-checked spot
   instances of the *converse* direction on deliberately adversarial
   shapes — 4-deep negation, self-implication, the contrapositive
   pattern, and Peirce's law — all confirming the converse on those
   instances. (`Formula Atom` is infinite, so the fully general converse
   is not itself a `Decidable` proposition and cannot be settled by a
   single `decide`; this review does not claim to supply a general Lean
   proof of it — see the note in that file's Part 3 on why the natural
   proof strategy, a global "round every glut up/down" argument, breaks
   on a naive first attempt because LP negation is order-*reversing*, and
   a correct proof needs a polarity-tracking induction this review did
   not complete.)

**Net assessment:** this is a real documentation problem (an unsupported,
likely-false mathematical claim, attached to the wrong theorem via
possibly-conflated formula-level/entailment-level notions of "the
converse"), not a bug in any proved Lean statement. Severity **MODERATE**:
it doesn't corrupt `valid_implies_cvalid` (still true, still correctly
scoped) or `collapse` (still a genuine two-way `iff`) or any countermodel
claim, but it does misrepresent the state of knowledge about LP's
classical recapture at the formula level, in a way a future reader could
easily propagate.

## 5. Independent axiom-footprint cross-check

Re-ran (not the whole `lake build` — that was already independently
confirmed twice — but a targeted `lake env lean` pass) on the audited
`Audit.lean` directly. `#print axioms` output matches `RESULTS.md`'s
table **verbatim**, entry for entry: every one of `lem_valid`,
`lnc_valid`, `dne_entails`, `dni_entails`, `adjunction_valid`,
`and_elim_left/right`, `or_intro_left/right`, `imp_neg_imp_valid`,
`explosion_invalid`, `mp_invalid`, `disjunctive_syllogism_invalid`,
`deduction_theorem_breakdown`, `collapse`, `valid_implies_cvalid` shows
exactly `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.

Also independently confirmed the file's own explanation for *why* even
plain `decide`-based facts carry this footprint: this review's own
from-scratch `ref_explosion_invalid`/`ref_mp_invalid`/
`ref_disjunctive_syllogism_invalid` (which do **not** use
`Entails.decidable`'s `Fintype`/`Finset` machinery at all — they are
hand-unfolded through `Sat`, using `decide` only on 3-element `LPVal`
facts) still carry the identical `[propext, Classical.choice,
Quot.sound]` footprint, because `LPVal.D : Finset LPVal` membership
alone (a quotient-type fact) pulls in `Quot.sound` regardless of proof
route. This corroborates, rather than merely repeats, the front's stated
explanation.

`grep -rniE "sorry|admit|native_decide"` over
`TamesisLab/ExternalLines/` independently re-run: 0 hits.

## 6. Documentation accuracy (README.md / RESULTS.md)

- **Line counts**: independently re-`wc -l`'d all 6 files —
  `Definitions.lean` 195, `ValidTheorems.lean` 148, `Countermodels.lean`
  115, `CollapseTheorem.lean` 231, `Audit.lean` 164,
  `NonclassicalLogicLP.lean` 23 — **total 876**. Matches `RESULTS.md`
  exactly, per-file and in total.
- **File list**: matches exactly (no extra/missing files under
  `TamesisLab/ExternalLines/NonclassicalLogicLP/`).
- **Theorem checklist** (`RESULTS.md`'s 11-item table): every named
  theorem/lemma was located in the file it claims (cross-checked by
  reading, not just `#check`-trusting the front's own registry).
- **Scope note / DISC-DEC-102 disclosure**: `README.md` and `RESULTS.md`
  both correctly and prominently state this line is tracked only in
  `05_DISCOVERY_LAB` (`DISC-DEC-102`) and is **not** entered into
  `04_FORMAL_RESEARCH_LAB/00_GOVERNANCE/` or
  `04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/`. Independently verified this is
  true: `git status --porcelain 04_FORMAL_RESEARCH_LAB/00_GOVERNANCE/
  04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/` returns **empty** — neither
  directory shows any change.
- `04_FORMAL_RESEARCH_LAB/11_EXTERNAL_LINES/NONCLASSICAL_LOGIC_LP/`
  contains exactly the two files it claims (`README.md`, `RESULTS.md`),
  nothing else, before this review added the `adversarial/` subfolder.

No inaccuracies found in either governance doc.

## 7. `git status` / `git diff` check

```
$ git status --porcelain 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/
 M 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab.lean
?? 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/ExternalLines/

$ git diff -- 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab.lean
 import TamesisLab.Foundations
 import TamesisLab.Engineering
+import TamesisLab.ExternalLines.NonclassicalLogicLP
 import TamesisLab.Riemann
 ...
```

Confirmed: the **only** modification to a previously-tracked file is
exactly the one claimed import line, inserted between the
`Foundations`/`Engineering` and `Riemann` imports, syntactically
well-formed, following the file's existing one-import-per-subsystem
convention. Nothing else in `TamesisLab.lean` changed (full `git diff
--stat` shows `1 file changed, 1 insertion(+)`, no deletions). This
addition cannot alter any other module's behavior — Lean imports are
additive (they bring declarations into scope; they cannot rebind or
shadow an existing subsystem's names, and no name clash was introduced,
since `TamesisLab.ExternalLines.NonclassicalLogicLP` is a fresh
namespace with no overlap with `Foundations`/`Engineering`/`Riemann`/etc.).

All other repository changes visible in `git status` at review time
belong to unrelated, pre-existing work on other lines
(`05_DISCOVERY_LAB/02_TESTS/...` numeric-attempt scratch files and
`05_DISCOVERY_LAB/02_TESTS/SCHUMANN_RESONANCE/...`) — not touched by, or
relevant to, this review.

## 8. Independent literature check (web search)

Two queries were run (not relying on `Audit.lean`'s own citations):

- "Priest LP logic of paradox same tautologies as classical logic valid
  formulas coincide" — results (arXiv survey of paraconsistent logics,
  notes on LP) state: "Every valid formula of classical logic is valid
  in LP as well... LP has the same theorems as classical logic, but it
  differs at the level of the consequence relation."
- "SEP paraconsistent logic LP designated values tautologies classical
  logic same" — results state: "LP and similar logics have the same
  tautologies as classical logic, though their consequence relations are
  different. LP is paraconsistent in that ¬p, p ⊭ q..."

Both corroborate the Priest 1979 / SEP truth tables and designation
convention used in `Definitions.lean`/`Audit.lean`, and both directly
bear on Finding §4 above.

## 9. Independent verification artifacts (this review's own work)

- `adversarial/RefereeCheck.lean` — a from-scratch Lean file (fresh
  witnesses, fresh proof terms, fresh induction; reuses only *data*
  definitions — `LPVal`, `Formula`, `eval`, `Sat`, `Entails`, `Valid`,
  `BEval`, `CValid` — never the audited proof terms) that:
  - re-derives `explosion_invalid`, `mp_invalid`,
    `disjunctive_syllogism_invalid` with a **different** witness
    (`Fin 2`-indexed atoms instead of `Bool`) via explicit `Sat`/
    `Entails` unfolding rather than a single top-level `decide` call;
  - re-derives the collapse theorem's proven direction
    (`Valid φ → CValid φ`) from scratch, by its own structural induction
    (`ref_eval_ofBool`), independent of `CollapseTheorem`'s
    `toBool`/`ofBool`/`toBool_eval` proof terms;
  - spot-checks the disputed converse direction on 4 concrete adversarial
    formula shapes.
  Compiled independently during this review via
  `cd 04_FORMAL_RESEARCH_LAB/05_FORMAL/lean && lake env lean <path-to-a-copy-of-this-file-placed-under-TamesisLab/ExternalLines/NonclassicalLogicLP/>`
  — **0 errors, 0 warnings**, exit code 0. `#print axioms` on every
  re-derived theorem: `[propext, Classical.choice, Quot.sound]` (or, for
  the pure structural lemma `ref_eval_ofBool`, no axioms at all) — same
  standard footprint as the audited file, independently reproduced.
  (This file is *not* wired into `TamesisLab.lean`/the aggregator and
  is not part of the audited 876-line/6-file line; it is archived here
  only as evidence. To recompile: copy it back under
  `TamesisLab/ExternalLines/NonclassicalLogicLP/` and run the command
  above — it was removed from that tree after compiling cleanly, to
  avoid inflating or altering the audited line's own file/line count.)
- `adversarial/lp_collapse_search.py`,
  `adversarial/lp_collapse_search_extra.py` — the brute-force Python
  truth-table search behind §4's finding (independent reimplementation
  of the LP/classical semantics in Python, not calling into Lean at
  all).

---

## Summary

The mathematical content of LP-001 is sound: the truth tables match
Priest (1979)/SEP exactly; all 12 meta-theorems say what their names
claim and are correctly, non-vacuously proved for the right quantifier
scope; the shared countermodel witness genuinely witnesses all three
classic LP invalidities (hand-verified independently); the collapse
theorem is a real, correctly-quantified two-way `iff`; the axiom
footprint and `sorry`-freedom claims both independently reproduce
exactly. The governance docs' line counts, file lists, theorem lists,
and scope-note disclosures are all accurate, and the only change to a
previously-tracked file is exactly the single claimed import line.

The one substantive issue is a documentation defect, not a proof defect:
`CollapseTheorem.lean`'s claim that the collapse corollary's "converse
fails" is unsupported by any exhibited counterexample, is contradicted
by independent literature and by this review's own 300k+-formula
brute-force search and partial from-scratch Lean confirmation, and
should be corrected or removed rather than left standing as a claim
about the mathematics.

**Verdict: SOUND WITH NAMED ISSUES** — 1 MODERATE (the unsupported/
likely-false "converse fails" claim in `CollapseTheorem.lean`'s
docstring on `valid_implies_cvalid`), 0 HIGH.
