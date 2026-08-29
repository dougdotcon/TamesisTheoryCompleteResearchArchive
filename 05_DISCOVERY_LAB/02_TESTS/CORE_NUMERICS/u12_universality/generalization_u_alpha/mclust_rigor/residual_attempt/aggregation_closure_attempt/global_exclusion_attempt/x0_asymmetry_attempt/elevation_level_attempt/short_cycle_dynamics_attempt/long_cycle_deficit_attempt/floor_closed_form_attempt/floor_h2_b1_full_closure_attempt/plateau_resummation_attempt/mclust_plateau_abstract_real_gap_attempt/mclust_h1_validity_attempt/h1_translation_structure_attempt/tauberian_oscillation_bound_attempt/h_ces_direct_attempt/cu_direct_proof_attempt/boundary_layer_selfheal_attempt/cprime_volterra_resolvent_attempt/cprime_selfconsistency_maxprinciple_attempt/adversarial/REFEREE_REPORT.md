# REFEREE REPORT — `CPRIME-SELFCONSISTENCY-MAXPRINCIPLE-ATTEMPT` (wave 32, front a, `DISC-DEC-145`)

**Referee stance: hostile/adversarial.** Every central algebraic claim was
independently re-derived from scratch (fresh `sympy`/`mpmath`, not by reading
or importing the front's own `s01`-`s05` scripts, except where explicitly
noted for cross-checking numeric transcription into `ATTEMPT.md`). Every
required background document (predecessor `ATTEMPT.md` Sec 0/6/10,
`h1_energy_estimate_attempt` Sec 8.2/8.4, `mclust_plateau_abstract_real_gap_
attempt` Sec A.3, `DECISION_LEDGER.yaml` `DISC-DEC-144`/`145`,
`PROOF_DEPENDENCY_MAP.md` Tree B including the `DISC-DEC-144` addendum) was
read in full or in the specific cited sections.

## VERDICT: **SOUND WITH NAMED ISSUES**

No algebraic identity, no symbolic derivation, and no numeric claim in the
front's `ATTEMPT.md` was found to be **false**. Every equation checked
independently reproduced exactly (zero symbolic residual; numeric agreement
to the reported precision). Scope discipline (seed block, file-touch
discipline, citation accuracy) is fully confirmed. However, the document's
own **most important, most quotable claim** — that the "unifying identity"
of Sec 2 explains *why* the maximum-principle route of Sec 3 fails, and that
this "sharpens" `DISC-DEC-144` — is an **overclaim**: the actual proof of
failure (Sec 3.3) is self-contained and does not depend on, or need, the
sign-flip mechanism Sec 2 emphasizes. There is also one factually inaccurate
quantitative range claim in Sec 5, self-contradicted by the same paragraph
and by the front's own `s04` output. Both are named below as MODERATE
issues; two further LOW/cosmetic issues and one positive (under-claim)
finding round out the list. None of this affects the front's bottom-line
honest conclusion: `(B)`/`(C')` remain open, and this front does not close
them.

---

## 1. Independent re-derivation of every algebraic identity (Sec 2, 3, 6)

Script: `ref01_symbolic_rederivation.py` / `.log` (fresh `sympy`, written from
the raw definitions in `ATTEMPT.md` Sec 0.1, not by reading `s01`/`s02`/`s05`
first).

All of the following were re-derived from scratch and confirmed **exactly**
(symbolic residual `0` in every case):

| Identity | Result |
|---|---|
| `(BRIDGE-1)` `g*Avg_g[Phi](s,g) = eps*I(x,y)` | CONFIRMED (definitional under `s=eps*x,g=eps*y`) |
| `(BRIDGE-2)` `(1-s-g) = eps*M_y` | CONFIRMED, residual `0` |
| Sec 2.2 collapse: `eps*I + eps*M_y*Psi` (via `(E1)`) `= Psi - eps*Psi_x` (`KEY`) | CONFIRMED, residual `0` |
| Sec 2.3 threshold: `s+g=1 <=> x+y=1/eps` | CONFIRMED |
| Sec 3.1: `(E2)` kernel total weight `= e^{-y/eps}+(1-e^{-y/eps}) = 1` | CONFIRMED |
| Sec 3.2: `g+(1-s-g) = 1-s` | CONFIRMED |
| Sec 3.3: `(1-s)*M - M = -s*M <= 0` for `s,M>=0`, hence `T(M)<=M` for `M>=1` | CONFIRMED |
| Sec 6: `W_x = Psi_x - eps*Psi_xx` (differentiating `KEY`) | CONFIRMED, coefficient of `Psi_xx` exactly `-eps` |
| Sec 6 Part 3: `Psi_xx = Psi + (x+y)*Psi_x - I_x` (differentiating `(E1)`) | CONFIRMED |

This matches, and independently corroborates from scratch, the dispatching
session's own spot-check summary. No discrepancy found anywhere in the
symbolic content.

## 2. Independent numeric reproduction (Sec 4.2, Sec 5)

Script: `ref02_independent_numerics.py` / `.log` (fresh `mpmath`, `dps=35`, a
**different test field** than the front's own `s03`/`s04` test field, plus a
handful of `(y,z)` grid points not in the front's own displayed table).

- **`M_Psi<=M_Phi` corollary** (Sec 4.1): confirmed on the new test field at
  5 points, `max|Psi|=0.518 <= M_Phi=1.0` throughout.
- **Naive same-`x` bound refutation** (Sec 4.2): on the front's own test
  field, the reported numbers (`x=0,y=0.5: |Psi|=0.2919` vs
  `wrong-bound=0.1256`, a `>2x` violation) were reproduced **exactly** from
  `s03`'s own log. On an **independently constructed, differently-shaped**
  test field, the same naive bound was independently found to be violated
  at `2/6` tested points — corroborating that the refutation is a genuine
  structural fact about `(BB-Psi')`, not an artifact of the front's
  particular test function.
- **Corrected bound** `|Psi(x,y)|<=y*R(x+y)*sup_{x'>=x,y'<=y}|Phi(x',y')|`:
  held at all 6 points on the independent test field too.
- **`(BB-Psi')` proof of the corrected bound (item 5 of the mandate)**: I
  proved this directly, not merely numerically — see Sec 4 below. It is
  actually a rigorous one-line consequence of the definition, stronger than
  what `ATTEMPT.md` claims for it ("confirmed numerically at every one of
  the 6 tested points").
- **Sec 5 anti-causal-leakage table**: all 8 displayed `(z,y,fraction)`
  triples reproduced to the stated 3 decimal places exactly (`0.730, 0.681,
  0.472, 0.356, 0.186, 0.098, 0.033, 0.010`).
- **Sec 5 range claim, extended grid**: computing 7 additional `(y,z)`
  points from the front's own stated 18-point grid (all `y=2.0` rows, and
  `y=0.5` at `z=30,100`) that are *not* shown in the displayed 8-row table
  gives a minimum fraction of **`0.4999%`** at `z=100,y=2.0` — see Issue 2
  below.

---

## 3. Scrutiny of the "unifying identity" claim (task item 3) — the central
finding of the document

`(BRIDGE-1)`/`(BRIDGE-2)`/`(BRIDGE-3)` are exact and correctly re-derived
(Sec 1 above). Taken at face value they establish a real, previously
unwritten fact: the self-consistency coefficient `(1-s-g)` of the ORIGINAL
`(s,g)`-side `W` formula is, under the archive's own standard rescaling,
**literally the same scalar function** as `eps*M_y`, the multiplication
operator that has governed `K(y,t)`'s structure since `DISC-DEC-113` and is
the subject of `DISC-DEC-144`'s theorem.

But `ATTEMPT.md` goes further, in the VERDICT (item 1), Sec 2.4, and Sec 7
(item 1, "sharpens... DISC-DEC-144"): it claims a maximum-principle argument
built from the original coefficients "inherits, automatically and
unavoidably, exactly the same sign structure that `DISC-DEC-144` already
proved defeats every norm-based technique tried on the kernel side" — i.e.
that Sec 2's bridge identity is *why* the maximum-principle route of Sec 3
fails.

**This causal claim is not established, and is contradicted by the front's
own Sec 3.3.** Sec 3.3's non-contraction proof (`T(M)=max(1,(1-s)*M)<=M`)
is stated, and proved, to hold **"even restricted to the fully SAFE regime
`s+g<=1`"** — i.e. throughout the region where `(1-s-g)>=0` and the
`M_y`/sign-flip phenomenon of Sec 2 has *not yet occurred at all*. The actual
mechanism defeating the maximum principle is a completely different,
strictly more elementary fact: the `Phi->Psi` Lipschitz constant is exactly
`1` (not `<1`), already established in `DISC-DEC-100` Sec 8.2 (independently
re-read and confirmed, see background reading below) and cited correctly by
this front in Sec 4.1 — a fact that has nothing intrinsically to do with the
`M_y=0` threshold at `z=1/eps`. `DISC-DEC-144`'s obstruction, by contrast, is
a statement about `||K(y,t)||`'s growth via an ODE majorant that genuinely
does hinge on the sign structure of `D(s)` around `w=z-1/eps`.

**Conclusion**: the two negative findings (Sec 3.3's non-contraction, and
`DISC-DEC-144`'s operator-norm obstruction) are logically **independent**
results that happen to both concern the same underlying scalar `M_y`, not
one "sharpening" or being causally "inherited" from the other. Sec 2's bridge
identity is genuine, correct, and mildly interesting (it shows the two
representations share the same coefficient function, so the averaging
structure is not drawing on unrelated new machinery) — but it does not do
the explanatory work the VERDICT and Sec 7 ascribe to it. The actual reason
this front's own maximum-principle attempt fails is Sec 3.3's argument
alone, standing on its own, provable without ever invoking Sec 2's bridge or
`DISC-DEC-144`.

**Severity: MODERATE.** No false statement is made (every individual claim
in Sec 2 and Sec 3 is separately true), but the document's headline framing
overstates the logical connection between them, in exactly the place a
reader is most likely to quote it. Recommend a dated nota clarifying: (a)
the bridge identity is a real, correct, previously-unrecorded consistency
fact between the `(s,g)`- and `(x,y)`-side formulations; (b) it does **not**
explain, and is not needed to derive, Sec 3.3's non-contraction result,
which is self-contained and occurs entirely within the sign-flip-free safe
regime; (c) the "sharpens DISC-DEC-144" language in Sec 7 should be
softened to "a second, independent negative result about a different
technique class, which happens to be built from the same underlying scalar
`M_y`."

## 4. Sec 3.3 non-contraction: is a sharper comparison function available?
(task item 4)

Re-examined directly: could a different choice of iterated bound (not the
crude `T(M):=max(1,(1-s)*M)`) rescue the argument? The obstruction is not a
poor choice of `T` — it traces to `DISC-DEC-100`'s Lipschitz constant for
`Phi->Psi` being **exactly** `1`, and (per that document's own referee
correction, re-read here, Sec 8.2) *tight*, approached (not merely bounded)
as `y->infinity` at fixed `x`. Any argument that bounds `sup W` using only
global sup-quantities (`M_Phi`, `M_Psi`) inherits this tightness: at `s=0`
(a slice `M_Phi`, a *global* sup, must dominate), the coefficient of `Psi`
in `W` is exactly `1`, so no sup-level scalar iteration — whatever weighting
or comparison function `T` is chosen — can produce strict decrease at that
slice without extra (oscillation/variance) structure. I tried the natural
alternatives (a growing weight in `y`, a decaying weight in `y`) informally;
both fail for exactly the reasons the ancestor `h1_energy_estimate_attempt`
Sec 8.3 already diagnosed for the closely analogous `Phi->Psi` contraction
question (growing weights overshoot because `R(z)~1/z` only marginally
compensates; decaying weights are mismatched to `Phi`'s actual non-decaying
plateau behavior). **Sec 3.4's own diagnosis — that a genuine fix requires
an oscillation-decay statement `Avg_g[Phi]<=(1-delta)*M_Phi`, `delta>0`,
independent of `M_Phi`, which is essentially `(H-ces)`/`(U1)` under a
different name — is correct and matches what I found by trying the obvious
alternatives.** No sharper choice within this technique class (global-sup
maximum principle) was found. This part of the document's negative
conclusion is well-supported.

## 5. Sec 8 Issue 1 (self-caught anti-causality): direct proof, not just
numeric confirmation (task item 5)

The corrected bound is not merely "confirmed numerically at 6 points" as
`ATTEMPT.md` states — it is a **rigorous, one-line consequence of `(BB-
Psi')`'s own definition**, and I proved it directly:

```
Psi(x,y) = int_0^inf e^{-u^2/2-u(x+y)} I(x+u,y) du,   I(x,y)=int_0^y Phi(x,y')dy'
```

Since `u` ranges over `[0,infinity)`, `x+u >= x` for every term in the
integral — so `|I(x+u,y)| <= y * sup_{y'<=y}|Phi(x+u,y')| <= y *
sup_{x'>=x, y'<=y}|Phi(x',y')|` **for every `u>=0`**, unconditionally. The
kernel `e^{-u^2/2-u(x+y)}` is nonnegative with `int_0^inf ... du = R(x+y)`
(cited, `(G1)`-adjacent closed form). Hence

```
|Psi(x,y)| <= [sup_{x'>=x,y'<=y}|Phi(x',y')|] * y * R(x+y)
```

**exactly**, for every `(x,y)`, unconditionally — no genericity assumption,
no restriction to the test field used in `s03`. This is stronger than what
`ATTEMPT.md` claims for it. It is a genuine (and easy) THEOREM, not merely
a numerically-verified conjecture, and the diagnosed root cause (`Psi` is
"anti-causal" in `x` because `(BB-Psi')`'s inner integral looks forward, at
`x+u`, not backward) is correct.

**Severity: NOTE, not an issue** (this *strengthens* the front's own
claim; recorded here so the next front can cite it as PROVED rather than
merely numerically confirmed).

## 6. Sec 5 range claim — numeric discrepancy (independently found)

`ATTEMPT.md` Sec 5 states: *"The fraction is SUBSTANTIAL (`19%`-`73%` across
the full tested grid) in the `z=O(1)` "boundary layer" regime... and DECAYS
... but never reaches `0` at any FINITE `z` tested (still `~1%` at
`z=100`)."*

The displayed 8-row table (a curated subset: all `y=0.5,1.0` rows up to
`z=10`, plus `y=1.0` at `z=30,100`) does **not** itself span `19%`-`73%`
either (its own minimum, at `z=100,y=1.0`, is `1.0%`, matching the "still
`~1%` at `z=100`" clause quoted in the very same sentence — an internal
inconsistency already visible without going beyond the displayed table).
Going to the **full 18-point grid** the front's own `s04` script computed
(confirmed by my independent re-run, `ref02_independent_numerics.log`), the
true range is approximately **`0.5%`-`73%`** — the minimum, `0.4999%`,
occurs at `z=100,y=2.0`, well below the claimed `19%` floor. I was unable to
find a natural reading of "the full tested grid" under which `19%`-`73%` is
literally correct; `19%` appears to be the value at `z=10,y=0.5` (a point
that is not the minimum of anything named in the text) rather than an actual
bound.

**Severity: MODERATE** (a factual, checkable numeric misstatement in the
prose, contradicted by the front's own computed data and by an internal
inconsistency within the same sentence — but it does not affect any
downstream conclusion; the qualitative point Sec 5 is making — leakage is
large near `z=O(1)`, decays like `~1/z`, never vanishes at finite `z` — is
correct and independently reproduced by me). Recommend a dated correção
replacing the specific range with an accurate one, e.g. "ranges from under
1% (far from the boundary layer, e.g. `z>=30` at `y>=1`) up to about 73%
(deep in the boundary layer, `z=O(1)`)," or restricting the "19%-73%" claim
explicitly to the near-field portion of the grid it was apparently computed
from.

## 7. Cosmetic issue: stale docstring in `s03_mpsi_le_mphi_corollary_numeric.py`

The file's top-of-file docstring, item (3), describes the "SHARPER... form
this front derives" as `|Psi(x,y)| <= (y/(x+y)) * sup_{y'<=y}|Phi(x,y')|` —
this is the **wrong**, already-refuted "naive same-`x`" conjecture (the very
thing Sec 4.2/Issue 1 catches and refutes), not the corrected form the
script actually implements and confirms in Part 3
(`y*R(x+y)*sup_{x'>=x,y'<=y}|Phi(x',y')|`). The docstring evidently predates
the self-caught fix and was never updated to match the final script content;
the actual code, its output, and `ATTEMPT.md`'s prose are all correct and
mutually consistent — only the header comment is stale.

**Severity: LOW** (cosmetic; no mathematical or numeric consequence; a
reader who reads only the header comment, not the code or `ATTEMPT.md`,
could be briefly misled about which bound was ultimately established).

## 8. Minor style note: Sec 0's Portuguese rendering of the `mclust_
plateau_abstract_real_gap_attempt` Sec A.3 quote

`ATTEMPT.md` Sec 0's reading-list bullet presents a Portuguese sentence in
quotation marks ("o `(1-s-g)*Psi` termo em `W`...") ahead of the real,
English, verbatim quotation given later in Sec 2.3. I checked the actual
source (`mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` Sec A.3): it
is written in English, and the Sec 2.3 quotation matches it **word-for-word,
exactly** — fully accurate, fair use, not out of context (the source
sentence is itself part of a larger argument that concludes the boundary
mechanism does *not* explain the abstract-vs-real gap it was investigating;
this front correctly notes that separately and does not misuse the
quotation to claim otherwise). The Sec 0 Portuguese text is a faithful
translation of the same sentence, not a separate/different claim, and Sec 0
itself flags it as a preview ("quoted verbatim below (Sec 2.3)") rather than
claiming the Portuguese itself is verbatim.

**Severity: LOW / optional** (no accuracy problem; purely a stylistic
choice that could be read as implying the Portuguese is the verbatim
source when it is a translation — worth a one-line clarification if the
next correção pass is already touching this section, not worth a dedicated
correção on its own).

---

## 9. Background reading verified

- `DECISION_LEDGER.yaml` `DISC-DEC-144` and `DISC-DEC-145`: read in full;
  the ATTEMPT.md's characterization of both (the `2*eps` coefficient
  correction, the `eps=1/sqrt(2)` threshold, the "no norm-based technique...
  can close" conclusion; the wave-32 authorization and its "literal
  Recommendation #1" framing) is accurate.
- Predecessor `cprime_volterra_resolvent_attempt/ATTEMPT.md` Sec 0 (system/
  hypotheses), Sec 6 (verdict), Sec 10 (Recommendation #1): read in full.
  The Sec 0.1 system/hypotheses block quoted verbatim in this front's own
  Sec 0.1 matches the predecessor's Sec 0.1 exactly. Sec 10's recommendation
  #1 text matches this front's own paraphrase of "the literal mandate"
  closely (not word-for-word, but faithfully).
- `h1_energy_estimate_attempt/ATTEMPT.md` Sec 8.2 (the `DISC-DEC-100`
  Lipschitz-`<=1` bound) and Sec 8.4 (the "derivative loss" diagnosis): read
  in full. Both are accurately cited; the "derivative loss" phrase this
  front attributes to "`DISC-DEC-100` Sec 8.4" is correctly attributed —
  `DISC-DEC-100` is the integration decision covering the entire
  `h1_energy_estimate_attempt` document, Sec 8.4 included.
- `mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` Sec A.3: verified,
  see Sec 8 above — quotation is exact and used fairly.
- `PROOF_DEPENDENCY_MAP.md` Tree B, `DISC-DEC-144` addendum (and the
  general "Leitura" close): read; confirms `H1`, `(U1)`, `(U2)`, `(H-ces)`,
  `(C')`, `(B)` all remain formally OPEN entering wave 32, matching this
  front's own characterization exactly. (`DISC-DEC-136` does not have its
  own dated addendum block in `PROOF_DEPENDENCY_MAP.md` — it exists only in
  `DECISION_LEDGER.yaml`; this front's own required-reading list does not
  claim otherwise, so this is not a discrepancy attributable to this
  front.)

## 10. Governance / scope discipline

- **Seed block**: `grep -rn "20260950" 05_DISCOVERY_LAB/` (run independently)
  confirms the range `20260950000-20260950999` appears **only** in the
  `DISC-DEC-145` reservation line of `DECISION_LEDGER.yaml`, the mirrored
  note in `DISCOVERY_LAB_STATE.md`, and this front's own `ATTEMPT.md` prose
  quoting the reservation — never as an actually-used numeric seed anywhere.
  Confirmed unused, exactly as claimed.
- **File-touch discipline**: `git status --porcelain` shows only two new
  untracked directories in the whole working tree — this front's own
  `cprime_selfconsistency_maxprinciple_attempt/` and the wave-32 front (b)
  directory (`gamma_c_gamma_uniform_watson_remainder_attempt/`, unrelated).
  `git diff --stat` against tracked files is **empty** — no existing file
  was modified. Confirms the front's own Sec 14 claims exactly.
- No `.py` file from an ancestor front was found imported or referenced by
  `s01`-`s05`'s own code (spot-checked their `import` statements: only
  `sympy`/`mpmath`, no local-path imports).

---

## 11. Summary scorecard

| Item | Verdict |
|---|---|
| `(BRIDGE-1)`, `(BRIDGE-2)`, `(BRIDGE-3)` | CONFIRMED, exact, independently re-derived |
| THEOREM 1 (Sec 3.1, kernel weight `=1`) | CONFIRMED |
| Sec 3.2 sub-convex-combination characterization | CONFIRMED |
| Sec 3.3 non-contraction (`T(M)<=M`) | CONFIRMED, correct algebra; **but see Sec 3 finding above: it is logically independent of Sec 2, not "inheriting" from it** |
| Sec 4.1 `M_Psi<=M_Phi` corollary | CONFIRMED |
| Sec 4.2 naive-bound refutation | CONFIRMED, and independently reproduced on a different test field |
| Sec 4.2 corrected bound | CONFIRMED numerically **and now PROVED directly** (Sec 5 of this report) |
| Sec 5 anti-causal leakage table (8 displayed values) | CONFIRMED exactly |
| Sec 5 "19%-73% across the full tested grid" | **NOT CONFIRMED — numeric range is wrong; true range on the full 18-point grid is ~0.5%-73%** |
| Sec 6 derivative-loss identities | CONFIRMED, exact |
| VERDICT item 1 / Sec 2.4 / Sec 7 "sharpens DISC-DEC-144" framing | **OVERCLAIM — the explanatory link asserted is not established; Sec 3.3 is self-contained** |
| Scope discipline (seeds, file-touch, citations) | CONFIRMED fully |
| Overall bottom line: `(B)`/`(C')` not closed | CONFIRMED, honestly reported |

## 12. Issues list (for dated correções)

1. **[MODERATE]** VERDICT item 1 / Sec 2.4 / Sec 7's "sharpens `DISC-DEC-
   144`" framing overclaims the explanatory connection between the Sec 2
   bridge identity and the Sec 3.3 non-contraction result; the latter is
   self-contained and occurs entirely in the sign-flip-free safe regime.
   See Sec 3 of this report for the precise correction language suggested.
2. **[MODERATE]** Sec 5's "`19%`-`73%` across the full tested grid" claim
   is numerically wrong (true range on the full 18-point grid computed by
   the front's own `s04` is approximately `0.5%`-`73%`) and is
   self-contradicted by the same paragraph's own "`~1%` at `z=100`" clause.
   See Sec 6 of this report for suggested correction text.
3. **[LOW]** `s03_mpsi_le_mphi_corollary_numeric.py`'s docstring item (3)
   describes the already-refuted "naive same-`x`" bound as if it were the
   front's final result; stale, predates the self-caught fix, purely
   cosmetic. See Sec 7 of this report.
4. **[LOW / optional]** Sec 0's Portuguese rendering of the Sec A.3
   quotation could be misread as itself verbatim; the actual Sec 2.3
   quotation is accurate and fairly used. See Sec 8 of this report.
5. **[NOTE, not a defect — strengthens the front]** The Sec 4.2 corrected
   bound is provable in one elementary line directly from `(BB-Psi')`, not
   merely numerically confirmed as `ATTEMPT.md` states. See Sec 5 of this
   report for the one-line proof; recommend upgrading the claim's status
   from "numerically confirmed" to "PROVED" in a future correção.

No issue found rises to the level of invalidating any specific theorem
stated in `ATTEMPT.md`, and none affects the document's honest bottom-line
conclusion that `(B)` and `(C')` remain open and that this front's technique
class does not close them.

---

## 13. Files in this directory

| file | role |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `ref01_symbolic_rederivation.py`/`.log` | independent, from-scratch `sympy` re-derivation of every algebraic identity in `ATTEMPT.md` Sec 2, 3, 6 |
| `ref02_independent_numerics.py`/`.log` | independent, from-scratch `mpmath` re-verification of Sec 4.2 (different test field) and Sec 5 (table reproduction plus an extended grid revealing the range discrepancy) |

No file outside this `adversarial/` subdirectory was modified. No `git`
command was run.
