# Adversarial referee report — `GENERAL-K-CLOSED-CDF-ATTEMPT`

**Target reviewed:** `.../general_k_joint_attempt/general_k_closed_cdf_attempt/ATTEMPT.md`
(`DISC-DEC-114`, wave 24 front (b)).

**Mandate followed:** hostile, adversarial review. Prose-only reading of
`THEOREM.md` (Estágios 27, 39, 40, 41, 42) and the three cited
`ATTEMPT.md` source documents (`pnn_general_k_egf_attempt`,
`k3_full_cdf_attempt`, `general_k_decomposition_attempt`). **No `.py`
file from the target front or any ancestor front was read.** Every
script in this `adversarial/` directory is written completely fresh from
the mathematical prose, independently of the target's own code.

**Seeds:** this front's own randomized bonus section uses
`20260927001`–`20260927006`; this referee's mandate reserved
`20260927500`–`20260927799` for any randomized checks. Grep-confirmed
before use:
```
$ grep -rn "20260927" 05_DISCOVERY_LAB/
```
returned only the target front's own files (`ATTEMPT.md`,
`monte_carlo_bonus.py`) and the governance reservation line in
`DECISION_LEDGER.yaml:7519` — the `20260927500`–`20260927799` sub-range
was unused before this review. As anticipated by the mandate, this
review ended up needing **no randomized checks at all** in its final
deliverables: every script in this `adversarial/` directory (`script1`
through `script7`) uses only exhaustive loops over small parameter
ranges and exact symbolic/rational arithmetic, with no calls to
`random` or `numpy.random` anywhere. (A handful of throwaway interactive
spot-checks during the investigation did use Python's `random` module
seeded from this reserved range, purely to pick a few extra numeric
test points; those checks are superseded by the exhaustive versions
saved here and are not part of the final record.) No seed collision
with any other front's reserved range occurred.

---

## Verdict

**SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

Every core mathematical claim independently re-checked by this referee
holds up, **including the central and most consequential one** — the
Gosper "no antidifference exists for symbolic `K`" certificate — which
this referee independently reproduced from scratch (own re-derivation of
the summand, own `gosper_term` call, `K`/`r`/`n`/`O` all symbolic, run to
completion in `325.59`s, result `None`, closely matching the target's own
`313.1`s/`319.0`s). However, this referee found **two MODERATE issues**
(one a genuine transcription error in the document's own printed
evidence for its main result, the other an overclaimed secondary
"bonus") and **two LOW issues**, detailed below. None of these issues
overturns the headline claim; the Executive Summary's "Net verdict" is
accurate and not overclaimed.

---

## Summary of independent checks performed

| # | Check | Result | Script |
|---|---|---|---|
| 1 | Raw (Prop-S-based) vs. exchangeability-reduced `S_r` CDF, `K=4,5,6`, 102 `(n,K,k)` triples, from scratch | **MATCH** | `script1_exchangeability.py` |
| 2 | Both of the above vs. D1/D2/D3 closed forms, `n=3..8`, all `k` | **MATCH** | `script1_exchangeability.py` |
| 3 | Both vs. true Definition-4 brute force at `(n,K)=(5,4),(6,4),(7,3)` — **new pairs beyond the front's own brute-force coverage** | **MATCH** (933,120 and 1,728,720 raw configs at the two largest cells) | `script1_exchangeability.py` |
| 4 | Layer-1 `InnerJ(V,O)` closed form (`r<K`) vs. own from-scratch direct summation, 1635 configs, `K=3..7` | **MATCH** | `script2_layer1.py` |
| 5 | Layer-1 `InnerJ(V,O)` closed form (`r=K` boundary) vs. own direct sum | **MATCH** | `script2_layer1.py` |
| 6 | Symbolic proof that the `r<K` formula, evaluated *at* `r=K`, is **identical** to the separately-stated `r=K` formula | **IDENTICAL** (bonus finding, not in the target document) | `script2_layer1.py` |
| 7 | Full `S_r` reconstruction via closed Layer-1 `InnerJ` vs. raw `S_r` | **MATCH** | `script2_layer1.py` |
| 8 | Own re-derivation of Layer-2 `term(V)` from `InnerJ`, checked against the target's own printed "exact expression" (Sec. 4.3, Part C) | **MISMATCH FOUND** — see Finding M1 | `script5_gosper_certification.py`, `script6_term_bug_investigation.py` |
| 9 | Positive/negative Gosper harness controls, independently run | **MATCH** target's reported behavior | `script5_gosper_certification.py` |
| 10 | `gosper_term` on the (referee-corrected) Layer-2 summand, concrete `K=3..7` | **all non-`None`**, timings `11.5–18.2`s, closely matching target's `11.3–22.1`s | `script5_gosper_certification.py` |
| 11 | `gosper_sum` closed form extracted, `K=3,4`, checked against own from-scratch brute truncated `V`-sum at 5+3 configurations **independent of the target's own** | **8/8 exact matches** | `script5_gosper_certification.py` |
| 12 | **`gosper_term` on the corrected Layer-2 summand, `K`,`r`,`n`,`O` ALL symbolic — reproducing THE MAIN CERTIFICATE** | **`None`, ran to completion in `325.59`s** (target: `313.1`s/`319.0`s) | `script5_part_c_symbolicK_full_run.log` |
| 13 | Layer-2 naive-Vandermonde-fails demonstration, `(n,K,r,O)=(12,5,2,0)` | **exact reproduction** of the target's own reported numbers (`1584,3852,6120,7968,9228,9930,10224,10296`) | `script7_layer2_naive_vandermonde_demo.py` |
| 14 | "No regime-splitting on `k`" claim, `K=3`, every `k=0..n`, `n=3..11` | **literally true as stated**, but see Finding M2 for a nuancing counter-experiment | `script4_regime_split.py` |
| 15 | `hypersimp`-recognition sensitivity investigation (why a "quick `None`" is not the same as a genuine certificate) | confirms the target's `313.1`s / `325.59`s runtimes are genuine full-algorithm runs, not recognition failures | `script6_term_bug_investigation.py` |

All checks above were built completely from scratch, independently of
the target's own `.py` files (never read), from the prose of `THEOREM.md`
and the cited `ATTEMPT.md` documents only.

---

## Findings

### Finding M1 (MODERATE) — the printed Layer-2 `term(V)` formula in Section 4.3, Part C, does not algebraically equal what the document says it equals

Section 4.3 states, correctly, in prose immediately before invoking
`gosper_term`:
```
term(V) = C(V-1,r-1) * [ (O+V)*C(n-V-O+r-1,K-1) + r*C(n-V-O+r-1,K) ]
```
This referee re-derived this *exact* expression independently, from
Layer 1's own combinatorially-verified `InnerJ(V,O)` closed form (see
`script2_layer1.py`), and confirms it is correct.

But the "exact expression sympy simplified the summand to" printed a few
lines later in the *same section* (Part C) is:
```
term(V) = binomial(V - 1, r - 1)*((K*O + K*V - K*r - O*r - V*r + n*r + r**2)
          *binomial(V - 1, V - r)*factorial(n - K - O - V + r - 1)
          /(factorial(K)*factorial(n - K - O - V + r)))
```
This referee verified — **both symbolically (`sp.simplify` of the
difference is nonzero) and numerically** (e.g. at
`n=20,K=5,r=2,V=6,O=3`: the correct value is `30195`; the printed
formula evaluates to `305/192`, not even an integer) — that this printed
expression is **not** algebraically equal to the correct
`C(V-1,r-1)*InnerJ(V,O)`. Two concrete defects were identified: (a) a
spurious duplicate factor `binomial(V-1,V-r)` (which equals
`binomial(V-1,r-1)`, already present as the outer prefactor — so the
printed formula effectively squares this factor), and (b) an incorrect
factorial argument `n-K-O-V+r-1` where algebra shows it should be
`n-O-V+r-1` (an erroneous extra `-K`). See `script5_gosper_certification.py`
Part 0 and `script6_term_bug_investigation.py` for the full derivation
and numeric reproduction.

**Does this undermine the main result?** This referee investigated
further and found strong, convergent evidence that it does **not**:

1. `gosper_term`, run on this referee's own **correctly re-derived**
   term at concrete `K=3,4,5,6,7`, gives timings (`11.5s, 18.2s, 11.7s,
   11.9s, 12.1s`) that closely match the target's own reported timings
   (`11.3s, 22.1s, 13.0s, 11.5s, 13.1s`) — a specific, multi-point
   fingerprint match.
2. `gosper_term` on this referee's correct term with `K`, `r`, `n`, `O`
   **all symbolic** ran to completion in `325.59`s and returned `None`
   — closely matching the target's own reported `313.1`s/`319.0`s (two
   independent runs).
3. By contrast, `gosper_term` on the **literally-printed** (buggy)
   formula at concrete `K=3` alone did **not complete within 7+
   minutes** (process killed by this referee) — wildly inconsistent
   with the target's own reported `11.3`s for "the same" computation.

This fingerprint (correct term: fast at concrete `K`, ~5 minutes at
symbolic `K`, both matching the target's numbers closely; buggy printed
term: anomalously slow even at concrete `K`) is strong circumstantial
evidence that **the target's actual script used the mathematically
correct term**, and that the error is confined to a **transcription
mistake when the "exact expression" was copied/retyped into the
markdown** — not a computational error in the underlying certification.
This referee's own independent, from-scratch reproduction of the
symbolic-`K` `None` result (item 12 in the table above) directly
confirms the certificate's conclusion survives.

**A related methodological point (folded into this finding, not a
separate one):** `sympy`'s `gosper_term` calls `hypersimp` as its first
internal step (`sympy/concrete/gosper.py:104-108`); if `hypersimp` fails
to recognize the input as a hypergeometric term at all, `gosper_term`
returns `None` **immediately**, and this is a fundamentally different
(much weaker) kind of `None` than a genuine "ran the decision procedure
and found no antidifference" result. This referee confirmed that the
"natural first-draft" way of writing the summand (as a sum of two
binomial-coefficient terms, `C(V-1,r-1)*InnerJ(V,O)` left unexpanded)
causes exactly this fast, spurious failure (`0.015`s, `None`) — whereas
the same object, once algebraically combined into a single fraction,
is correctly recognized by `hypersimp` (`0.66`s) and `gosper_term` then
genuinely engages the decision procedure (~5 minutes, `None`). The
target document does not discuss this sensitivity explicitly, though
its own emphasis on "ran to completion in 313.1 seconds" (as opposed to
an instant `None`) is, in retrospect, exactly the right diagnostic — it
is simply not spelled out *why* that timing matters. This referee
recommends, for any future front doing this kind of certification,
explicitly demonstrating that `hypersimp` succeeds on the exact
expression handed to `gosper_term`, to pre-empt exactly the confusion
this referee had to resolve by hand.

**Severity: MODERATE.** A real, verifiable error in the document's own
displayed evidence for its main result (Section 4.3, Part C) — a reader
attempting to reproduce the certificate from the printed formula alone
would fail (they'd either get a fast, spurious `None` in milliseconds,
or — if they preserved the printed formula's structure — an anomalously
slow, possibly non-terminating computation, as this referee experienced
directly). But the underlying claim (item 9 of the scorecard) survives:
this referee's own independent, from-scratch computation, using the
provably-correct term, reproduces both the concrete-`K` positive results
and the symbolic-`K` `None` certificate with closely matching runtimes.

---

### Finding M2 (MODERATE) — the "no regime-splitting on `k` needed" bonus overclaims its significance relative to Estágio 40's achievement

The Executive Summary and Section 3.1 present, as "a genuine structural
bonus," the fact that checking the exchangeability-reduced `S_r`
reformulation against brute force / D1-D2-D3 "needs no regime-splitting
on `k` at all (unlike Estágio 40's original K=3 derivation, which needed
three separate combinatorial regimes)." Scorecard item 4 labels this
**PROVED**.

This referee confirmed the literal numerical claim: re-implementing the
`S_r` reorganization via Layer 1's own closed `InnerJ` plus a raw
double loop over `O` and `V` (no case-splitting anywhere in the code),
this referee's version exactly reproduces Proposição D3 at **every**
`k=0..n`, for `n=3..11`, `K=3` (`script4_regime_split.py`, Part I).

However, this referee argues the comparison to Estágio 40 is not
apples-to-apples, and ran a direct counter-experiment to test this:

- Estágio 40's three regimes (`THEOREM.md` Estágio 40 §4.3, confirmed by
  reading `k3_full_cdf_attempt/ATTEMPT.md` in full) arose specifically
  while deriving an actual **closed rational-function-in-`n` formula**
  by symbolically summing the composition simplex — the split is driven
  by the *`O`-sum's own range*, `0<=O<=min(k,n-3)`, switching behavior
  depending on whether `k` or `n-3` binds. This is a genuinely hard,
  substantive derivation step.
- The target's own "no regime-splitting" check (Section 3.1) is,
  by contrast, a check that an **exact algebraic reorganization
  identity** (grouping subset-sum terms by size `r`, via
  exchangeability of the composition simplex under index permutation)
  holds — which it must, by symmetry, for *every* `k`, with **no
  possibility of ever needing case-splitting in the first place**: this
  is a consequence of the summation domain's symmetry, entirely
  independent of `k`'s value. It is not testing the same kind of
  difficulty Estágio 40 overcame.
- This referee tested directly whether the *actual* symbolic-closure
  step (the kind Estágio 40 needed) shows the same regime-free behavior,
  by attempting `sp.summation` on Layer 2's own `V`-sum (symbolic
  `n,k,O`, concrete `K=3`, `r=1` and `r=2`) — a step *prior to* the
  `O`-sum where Estágio 40's regimes technically originated, and a step
  this front's own Section 5.2 explicitly marks **NOT ATTEMPTED**.
  **`sp.summation` immediately produces a `Piecewise` result** with a
  special case at `Eq(k, n)` (see `script4_regime_split.py`, Part II,
  full output saved in `script4_regime_split.log`) — i.e., regime-like
  boundary structure reappears as soon as an actual symbolic closure is
  attempted, even one layer *before* the layer where Estágio 40's own
  regimes arose.

This suggests the "no regime-splitting" bonus is a much narrower and
more modest fact (an automatic consequence of exchangeability that would
hold for *any* correct reorganization by subset size, regardless of how
the CDF eventually gets closed, or whether it closes at all) than the
Executive Summary's framing ("a genuine structural bonus… a genuine
simplification of means") suggests, and that a fair comparison to
Estágio 40 would require this front to have reached an actual closed
symbolic formula — which it explicitly has not (Layers 2–3 remain open).

**Severity: MODERATE.** The literal claim, as narrowly stated and
scoped, is true and was independently reproduced. But its framing in the
Executive Summary and its own scorecard line overclaims the depth of the
structural achievement relative to Estágio 40's — a genuine gap in the
*strength* of a secondary claim, not affecting the main Gosper result.

---

### Finding L1 (LOW) — Section 5.5's "trivially is one [a hypergeometric function]" characterization of the Layer-2 V-sum glosses over a real distinction its own Section 4.2 draws

Section 5.5 explains why the hypergeometric-fallback (`hyperexpand`) test
Estágio 39 used was not attempted for the full `S_r(n,K,k)`, adding: "as
opposed to just the inner V-sum, which trivially is one, by the same
term-ratio argument Estagio 39 used."

This referee confirmed the V-**summand** genuinely is a hypergeometric
term (`hypersimp` succeeds on the single-fraction form; term ratio in
`i:=V-r` extracted explicitly — parameters `a1=r`, `a2=K+O-n`, a third
non-integer-in-general parameter, `b1=O-n+1`, a fourth, with `z=1`,
giving a `_3F_2`-shaped structure). But Estágio 39's own fallback worked
specifically because *its* finite `r`-sum is a **complete, naturally
terminating** hypergeometric series — one Pochhammer parameter (`1-K`)
equals exactly the negative of the sum's own upper bound, so the series
automatically stops there, and is thus directly expressible via the
standard `pFq` definition (confirmed by reading
`pnn_general_k_egf_attempt/ATTEMPT.md` §5.4 in full).

The target's *own* Section 4.2, by contrast, goes to some lengths to
establish that the Layer-2 `V`-sum's upper limit `t:=k-O` is
**externally imposed**, generally *below* the summand's own natural
termination point (`V<=n-O-(K-r)`) — i.e. it is a genuine **partial
sum** of the hypergeometric series, with an independent free upper-limit
parameter, not the complete series itself. A partial sum of this kind is
not simply `T(0)*pFq(...;1)` the way Estágio 39's complete sum was, and
is not amenable to a single `hyperexpand` call in the same direct way.

This does not change any PROVED/OPEN/NOT ATTEMPTED label (Section 5.5 is
still correctly marked **NOT ATTEMPTED**), but the supporting sentence
undersells the actual difficulty of the fallback test it explains away
as easy — a reader could reasonably conclude a trivial follow-up
experiment was skipped for no good reason, when in fact the reason
(the partial-sum structure) is real, just not the one stated ("lack of
remaining scope").

**Severity: LOW.** Affects only an explanatory sentence in an
already-honestly-labeled NOT-ATTEMPTED section; no numeric or algebraic
claim is affected.

---

### Finding L2 (LOW, informational — not an error) — Layer 1's two closed forms (`r<K` and `r=K`) are not actually independent; the `r<K` formula, evaluated at `r=K`, already gives the `r=K` formula exactly

Section 4.1 presents two separate closed forms for `InnerJ(V,O)`:
```
InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
InnerJ(V,O) = n * C(N+r-1,r-1),   N:=n-V-O                     (r=K)
```
presented (correctly) as needing separate derivations, since the
underlying Vandermonde-Chu convolution identity used for `r<K` requires
`K-r>=1` and breaks down at `r=K` (this referee re-derived this
combinatorial fact from first principles independently, confirming the
`r=K` case genuinely needs a different, delta-function-style argument
at the level of the *raw defining sum* — not just the closed form; see
`script2_layer1.py` Part (b), where a naive translation of the general
"`compositions into `K-r` positive parts" formula to `K-r=0` silently
gives 0 always, rather than the correct value 1 at the single point
where the remaining total is exactly 0).

However, this referee found — and verified both symbolically (`sp.simplify`
gives exactly `0`) and numerically (170+ configurations, `K=2..7`) —
that the `r<K` formula, if one simply **substitutes `r=K` into it
anyway** (formally, ignoring that the derivation technically required
`K-r>=1`), gives **exactly** the same value as the separately-derived
`r=K` formula, for every tested case:
```
(O+V)*C(N+K-1,K-1) + K*C(N+K-1,K)  ==  n*C(N+K-1,K-1)   [always, provably]
```
(Proof: `C(N+K-1,K) = C(N+K-1,K-1)*N/K` by Pascal's relation, so
`K*C(N+K-1,K) = N*C(N+K-1,K-1)`, and `(O+V)+N = n`, giving the identity
directly.)

This is not an error — both of the document's formulas are individually
correct, and were independently verified as such by this referee. It is
simply a missed opportunity: a single unified closed form,
`InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K)`, valid for **every**
`0<=r<=K` with no case split needed at the level of the final formula
(only the *derivation route* differs), would have been a cleaner
presentation. Reported for completeness; does not affect any claim's
correctness.

**Severity: LOW, informational.**

---

## Section-by-section assessment against the adversarial mandate

**1. Exchangeability reduction to `S_r`, general `K`.** Independently
re-derived from Proposição S and cross-checked against a from-scratch
raw (un-reduced, `2^K`-subset) implementation at `K=4,5,6` (102
triples), and against true Definition-4 brute force at `(5,4)`, `(6,4)`,
`(7,3)` — three `(n,K)` pairs beyond the front's own brute-force
coverage, the largest at `1,728,720` raw configurations. **All exact
matches.** No error found in the reduction itself; see Finding M2 for a
caveat about how the "no regime-splitting" side-claim is framed.

**2. Layer 1's closed form.** The underlying "concatenation of two
compositions" (Vandermonde-Chu) identity was re-derived by this referee
from first principles (not just numerically checked) and applied twice,
exactly reproducing both terms of the `r<K` formula. The `r=K` boundary
case was checked with particular care per the mandate: this referee
found it **is** genuinely a separate combinatorial regime at the level
of the *raw defining sum* (the general "`K-r` positive parts" formula
degenerates incorrectly at `K-r=0`), confirming the document's choice to
state it separately is justified — but also found (Finding L2, LOW) that
the two *closed-form results* coincide exactly when the `r<K` formula is
evaluated at `r=K`, a fact the document does not note.

**3. The central Gosper certification — the primary focus of this
review.** (a) This referee's own re-derivation of `term(V)` from Layer
1's `InnerJ` **does not match** the document's own printed "exact
expression" in Section 4.3 Part C (Finding M1) — a genuine, verified
discrepancy. (b) This referee ran its own `gosper_term` call on the
correctly re-derived summand with `K` (together with `r,n,O`) left fully
symbolic: it ran to completion in `325.59`s and returned `None`,
independently reproducing the target's headline result. (c) Positive
controls at concrete `K=3,4,5,6,7` were independently reproduced: all
non-`None`, with timings closely matching the target's own reported
figures. (d) For `K=3` (and, as a bonus, `K=4` too), this referee
extracted the actual `gosper_sum` closed form and verified it
numerically against a from-scratch brute truncated `V`-sum at `5+3=8`
configurations **independent of the target's own reported ones** — all
8 exact matches.

**4. "No regime-splitting on `k`" claim.** Verified true at every
`k=0..n` for `K=3`, `n=3..11` — but see Finding M2 for why this referee
believes the comparison to Estágio 40 is framed more strongly than the
underlying fact supports.

**5. "One layer deeper than Estágio 39" comparison (Section 4.5).**
Assessed as a **fair, appropriately hedged** structural comparison, not
overstated. Re-reading Estágio 39's own certification (`THEOREM.md`
Estágio 39 block and `pnn_general_k_egf_attempt/ATTEMPT.md` §5 in full)
confirms its obstruction lived strictly in the *outermost* `r`-assembly
step, reached only after all lower-level moment formulas (the direct
analogue of this front's Layer 1) closed cleanly. This front's Layer 2
obstruction sits *inside* a single `S_r` building block, structurally
prior to any outer `r`-assembly — a genuinely earlier point in the
pipeline. The document's own explicit disclaimer ("No claim is made that
this is a 'harder' problem in any absolute sense — only that... the
obstruction sits at a structurally earlier point") is accurate and
appropriately limits the claim. No issue found here.

**6. Honesty/scope check.** Every scorecard label is earned by what is
shown in the body, **modulo** Finding M1 (the printed evidence for item
9 contains an error, though the underlying result independently
reproduces) and Finding M2 (item 4's "PROVED" is technically earned but
its Executive-Summary framing overclaims significance). The Net verdict
in the Executive Summary — "NOT CLOSED positively... but a real,
rigorous, precisely-located Gosper-certified non-existence result" — is
accurate; this referee found no hedging that could be misread as a
partial positive closure. Section 5.5's "NOT ATTEMPTED" hyperexpand
fallback is a reasonable scope cut for the reason that actually applies
(the partial-sum/complete-sum distinction, Finding L1) though not
exactly the reason the document states; its absence is a real but minor
(LOW) gap in the supporting narrative, not in the certified result
itself, since the certificate's core mechanism (Gosper's algorithm) was
independently reproduced by this referee end-to-end.

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `script1_exchangeability.py` / `.log` | fresh brute-force ground truth, raw Prop-S-based CDF, exchangeability-reduced `S_r`, and D1/D2/D3 cross-check, all built from scratch; `K=4,5,6` general checks plus 3 new brute-force `(n,K)` pairs |
| `script2_layer1.py` / `.log` | Layer-1 `InnerJ` closed form: own direct-sum verification (1635 configs), `r=K` boundary investigation, and the symbolic proof that the two stated formulas agree when evaluated at the same point (Finding L2) |
| `script3d_gosper_sum_K3.py` | standalone `K=3` `gosper_sum` extraction + brute-force verification module (superseded for final numbers by `script5`, kept for reference) |
| `script4_regime_split.py` / `.log` | the "no regime-splitting" literal-claim reproduction (Part I) and the `sp.summation`-produces-`Piecewise` counter-experiment (Part II, Finding M2) |
| `script5_gosper_certification.py` / `.log` | the main Gosper-certification script: `term(V)` mismatch discovery (Part 0, Finding M1), positive/negative controls (Part A), concrete-`K` positive results `K=3..7` (Part B), and `gosper_sum` extraction + numeric verification `K=3,4` (Part D) |
| `script5_part_c_symbolicK_full_run.log` | **the actual timed run of THE MAIN CERTIFICATE**: `gosper_term` on the corrected summand, `K,r,n,O` all symbolic, `None` after `325.59`s |
| `script6_term_bug_investigation.py` / `.log` | the `hypersimp`-sensitivity investigation and the timing-fingerprint comparison (Form 1 fast-spurious-`None` vs. Form 2 genuine ~5-minute `None` vs. Form 3 anomalously slow, supporting Finding M1's conclusion that the document's actual script used the correct term) |
| `script7_layer2_naive_vandermonde_demo.py` / `.log` | independent reproduction of Section 4.2's naive-Vandermonde-fails demonstration at the target's own quoted cell `(n,K,r,O)=(12,5,2,0)` — exact match of all 8 reported values |

---

## Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html`, or the target front's own `ATTEMPT.md`. No `git` command of
any kind was run. All writes confined to this `adversarial/`
subdirectory. No `.py` file from the target front or any ancestor front
(`general_k_decomposition_attempt`, `pnn_general_k_egf_attempt`,
`k3_full_cdf_attempt`, or any other) was opened, read, or imported at any
point — every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the cited `ATTEMPT.md` documents,
per the mandate's hard constraint. Reserved seed range
`20260927500`–`20260927799` confirmed unused before this review (see
Seeds section above); no collision with the target front's own
`20260927001`–`20260927006`.
