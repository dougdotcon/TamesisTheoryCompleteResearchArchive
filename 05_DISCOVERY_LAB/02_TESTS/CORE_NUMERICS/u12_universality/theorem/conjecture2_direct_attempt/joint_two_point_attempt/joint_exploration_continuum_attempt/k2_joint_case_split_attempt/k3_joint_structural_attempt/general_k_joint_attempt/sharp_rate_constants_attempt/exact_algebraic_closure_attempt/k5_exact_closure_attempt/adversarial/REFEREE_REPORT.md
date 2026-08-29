# Hostile Referee Report — K5-EXACT-CLOSURE-ATTEMPT

**Target:** `.../sharp_rate_constants_attempt/exact_algebraic_closure_attempt/k5_exact_closure_attempt/ATTEMPT.md`
(wave 29, front (c), `DISC-DEC-134`(c))

**Referee:** dedicated hostile session. Read, in full, before opening any
of the target's own scripts: the predecessor `exact_algebraic_closure_attempt/ATTEMPT.md`
(wave 26 front b, `K=3,4` exact closure) and its own
`adversarial/REFEREE_REPORT.md`; `THEOREM.md` Estágios 40, 41, 42, 43,
44, 45, 46, 48 in full; `general_k_decomposition_attempt/ATTEMPT.md`
(Estágio 41, Proposição S / Decomposition Theorem) and
`general_k_closed_cdf_attempt/ATTEMPT.md` (Estágio 44, the `S_r(n,K,k)`
reduction and Layer-1 `InnerJ` closed form) in full. Only after
independently reconstructing the target's central new claim (Proposição
D5) from this cited machinery — matching it exactly — were the target's
own scripts opened, to compare method and dig into specific numeric
claims.

---

## VERDICT: SOUND — ACCEPT for catalogue integration. One LOW-severity exposition finding.

The target's central claims — (1) a genuinely new closed-form CDF
Proposição D5 for `K=5`, derived by instantiating the archive's already-
proved general-`K` machinery (Proposição S, the Full Cycle-Count
Decomposition Theorem, Estágio 44's Layer-1 `InnerJ` formula) at the
concrete value `K=5`; and (2) full **exact** closure of the sharp
finite-`n` rate constant, `|F_n^{(5)}(x)-F_5(x)|\le M_5/n` for all
integer `n\ge7`, via the identical resultant-elimination method that
closed `K=3,4` — **both hold up completely under independent, hostile,
from-scratch reconstruction.**

Every headline number this referee attempted to independently reproduce
was reproduced **exactly**, to every digit shown in the target's own
document, via genuinely separate code (typed fresh from the cited
mathematical prose, never from the target's `.py` files):

- Proposição D5 itself — the target's own new mathematical content —
  reproduced **symbolically, with zero difference**, by a referee-typed
  pipeline built directly from the cited formulas, which also
  independently reproduces D1–D4 (a real, non-circular check, since this
  referee's pipeline is not the target's code).
- The same D5 formula independently confirmed against a **fresh,
  independent, fully exhaustive** brute-force implementation of
  Definition 4 at `K=5`, `n=5,6` (`11/11` exact matches).
- `g_5(x)`, `g_5'(x)`'s factorizations, `M_5`'s value and irreducible
  minimal quartic (cross-checked via an independent `sp.minimal_polynomial`
  call and a from-scratch `mpmath` 50-digit computation).
- All four resultant-elimination headline numbers: the boundary
  threshold `n_0^{boundary}=6.2961979658945123566\ldots`, the upper
  interior threshold `4.1433247158401868693\ldots`, the lower interior
  threshold `4.3806034572679090712\ldots`, including the exact
  `factor_list` structure (`n^{316}\cdot(\text{cubic})^4\cdot B(n)`,
  `B` degree `388`/`392`) at both bounds.
- `a(7)=1/3`, `\min_xh_5(5,x)=-0.4356\ldots`, `\min_xh_5(7,x)=-0.1712\ldots`,
  `\min_xh_5(11,x)=-0.0313\ldots` — all exact matches.

One additional check, **beyond** what the target's own document shows,
was performed and also confirms the target's claim: this referee
verified that the "largest real root" reported at each bound is
genuinely the largest real root of the **entire** `S(n)`, not just of
the largest-*degree* factor `B(n)`/`B_2(n)` — i.e. that the smaller
cofactors (`n^{316}`, and a cubic of multiplicity `4`) do not silently
hide a larger real root. They do not (see §2 Item 4 below). This closes
a gap the target's own write-up left implicit (unlike the `K=4`
predecessor's document, which explicitly showed its analogous quadratic
cofactor's negative discriminant) — named as Finding F1, LOW severity,
purely expository.

---

## 1. Methodology

Per the task's instruction, the reading order was: predecessor
`ATTEMPT.md` (wave 26 front b) and its `adversarial/REFEREE_REPORT.md`
in full; `THEOREM.md` Estágios 46 and 48 in full (the exact setup of
`M_K`, `F_n^{(K)}(x)`, `F_K(x)`, `h(n,x)`, `D(n)`); then, tracing back
through the ancestor chain, `THEOREM.md` Estágios 40, 41, 42, 43, 44, 45
in full (`D1`–`D4`, Proposição S, the Decomposition Theorem, and the two
Gosper-certification fronts establishing that no CDF closed form exists
*symbolic in `K`*, but that the same summand **is** Gosper-summable —
hence tractable — at every concrete `K` tested, including `K=5`); the
full prose of `general_k_decomposition_attempt/ATTEMPT.md` and
`general_k_closed_cdf_attempt/ATTEMPT.md` for the exact boxed formulas
(Proposição S; `S_r(n,K,k)`; the Layer-1 `InnerJ(V,O)` closed form) the
target instantiates at `K=5`. Only after this reading, and after
independently re-typing and running the general-`K` pipeline from these
formulas (reproducing `D1`–`D4` and then `D5` before ever opening the
target's own `d5_derivation.py`), was any of the target's own code read.

Every independent script referenced below was written fresh by this
referee (`adv1`–`adv4` in this directory); none imports or copies code
from the target's own `.py` files, which were read only for their prose
claims and specific numeric values to check against.

---

## 2. Item-by-item results

### Item 1 (task §a) — Proposição D5's derivation: PASS, independently reproduced from the cited general-K machinery

This was treated as the highest-priority check, since — unlike `K=3,4`,
which reused an *already independently-proved* closed-form CDF — `K=5`
has no closed-form CDF anywhere else in the archive (confirmed: no
`k5_full_cdf_attempt` sibling exists next to `k3_full_cdf_attempt`/
`k4_full_cdf_attempt`, and `THEOREM.md` Estágios 44/45 explicitly leave
every concrete `K\ge5` CDF undecided, certifying non-existence only for
`K` symbolic). Proposição D5 is thus the one piece of genuinely new
mathematics this front had to produce, not merely cite.

This referee typed, from scratch, directly from the two boxed formulas
in `general_k_closed_cdf_attempt/ATTEMPT.md` §2–4 (`S_r(n,K,k)`'s
exchangeability-reduced form, and the Layer-1 `InnerJ(V,O)` closed form,
both **cited results, PROVED elsewhere and already adversarially
reviewed** — see `THEOREM.md` Estágios 41/44's own referee verdicts,
both SOUND), an independent pipeline (`adv1_D5_derivation.py`). Running
it:

```
K=1 vs D1 (Estagio 27):  diff = 0
K=2 vs D2 (Estagio 42):  diff = 0
K=3 vs D3 (Estagio 40):  diff = 0
K=4 vs D4 (Estagio 43):  diff = 0
```

— all four **already-independently-proved** closed forms are reproduced
exactly by this referee's own pipeline, confirming the self-validation
claim is genuine, not circular: this is a second, independently-coded
implementation of the same cited general machinery, checked against the
same external ground truth (`D1`–`D4`, each individually proved and
adversarially reviewed by its own dedicated prior front), not a
re-running of the target's own code.

Then, at `K=5`:

```
Referee-derived D5 NUM = k**10 - 15*k**9 - 5*k**8*n**2 + 30*k**8*n + ...
Referee-derived D5 DEN = 120*n**5*binomial(n, 5)

Target's claimed Proposicao D5 vs referee's independently-derived
D5, symbolic difference: 0
EXACT MATCH.
```

`sp.simplify(referee\_D5 - target\_D5) == 0` — **zero symbolic
difference**, confirmed by an independently-typed pipeline against a
hand-transcription of the target's own boxed formula (§3.3 of the
target's `ATTEMPT.md`). The `1-D5(n,n-1)=120/n^5` sanity identity is
also independently reconfirmed. Script/log:
`adv1_D5_derivation.py`/`.log`.

**Verdict: the target's Proposição D5 is independently confirmed
correct**, and its self-validation-against-`D1`–`D4` methodology is
genuine (this referee's own from-scratch reconstruction of the exact
same methodology also passes the same test, which would be an
extraordinary coincidence if either pipeline actually contained a
`K`-dependent error).

### Item 2 (task §b) — Fresh brute-force cross-check of Definition 4, K=5: PASS

This referee wrote its own, fully independent, fully exhaustive
enumeration of `THEOREM.md` Definition 4 at `K=5` (`adv2_bruteforce_def4_k5.py`
— a different cycle-detection implementation style than the target's own
`bruteforce_definition4_k5.py`, which was not read for its code), and ran
it at `n=5,6` (the two feasible sizes explicitly asked for):

```
n=5 K=5  total configs=375000    elapsed=0.6s
n=6 K=5  total configs=5598720   elapsed=9.4s
```

Cross-checked against Proposição D5's formula (transcribed by hand, not
copy-pasted): **`11/11` exact `Fraction` matches** (`k=0..4` at `n=5`,
`k=0..5` at `n=6`) — e.g. `P(T\le2|n=5)=13/25` matches D5 exactly;
`P(T\le5|n=6)=319/324` matches exactly. Script/log:
`adv2_bruteforce_def4_k5.py`/`.log`.

`n=7,8` were not independently re-run by this referee (compute cost;
the target's own `n=7` run alone took `120.6`s and `n=8` took `1861.9`s
in their environment) — but this is not a gap in the verification,
because Item 1 above already establishes `D5(n,k)` is *symbolically*
correct for **all** `n,k` simultaneously, a strictly stronger guarantee
than any additional finite brute-force point could add. The target's own
`n=7,8` logs (`bruteforce_crosscheck_D5.log`, `n8_bonus_check.log`) were
read and are internally consistent with everything else independently
verified here (same `D5` formula, same structure of match).

### Item 3 (task §c) — `g_5`, `M_5`, and the full resultant-elimination construction: PASS, independently reproduced end-to-end

Starting from the referee's own independently-derived `D5` (Item 1, not
transcribed from the target), `adv3_g5_M5_resultant.py` independently
re-derives everything in the target's §4–5:

```
g5(x) = 10*x**10 - 15*x**9 - 20*x**8 + 40*x**7 - 30*x**5 + 20*x**4 - 10*x**2 + 5*x
      = 5x(x-1)^4(x+1)^3(2x^2-x+1)                              [diff: 0]
g5'(x) = 5(x-1)^3(x+1)^2(20x^4-7x^3+x^2+3x-1)                   [diff: 0]
interior quartic 20x^4-7x^3+x^2+3x-1 irreducible over Q: True
x5* = 0.309430603103057048428294338496
M5  = 0.696803198946355211196876665384
minimal polynomial of M5 = 1024000000000t^4 - 887007704239t^3
      - 7821482127360t^2 + 14635525734400t - 6341787648000    [diff: 0, irreducible]
mpmath (50 dps, zero sympy symbolic machinery): M5 agrees to 40+ digits
```

— every claim in the target's §4 independently reproduced exactly,
including a from-scratch `mpmath` cross-check (not reusing the target's
`k5_mpmath_crosscheck.py`).

Boundary threshold:

```
h5(n,1) = 120/((n-1)(n-2)(n-3)(n-4))
real roots of the M5-crossing equation: [-1.296..., 6.2961979658945123566...]
n0_boundary = 6.2961979658945123566...   (matches target's ~6.2962 to all digits shown)
```

Resultant elimination, upper bound (target `m=M_5`):

```
Res_x(F1,F2): degree 180 in n, degree 9 in m      [matches target exactly]
factor_list: n^316 * (cubic)^4 * B(n), B degree 388, 32 real roots
largest real root: 4.1433247158401868693...        [EXACT match, all digits]
```

Resultant elimination, lower bound (target `m=-M_5`):

```
factor_list: n^316 * (cubic)^4 * B2(n), B2 degree 392, 30 real roots
largest real root: 4.3806034572679090712...         [EXACT match, all digits]
```

Both interior thresholds land below `n0_boundary=6.30`, confirming the
target's claim that the boundary term alone pins the domain and that
`K=5`, unlike `K=4`, needs no exhaustive per-integer-`n` patch. Final
threshold: `n_0=\max(6.2962,4.1433,4.3806)=6.2962\ldots\Rightarrow`
smallest integer domain start `=7`. **Independently confirmed.**

**Extra check, beyond the target's own document (`adv4_all_factors_root_check.py`):**
`factor_list` produces three factors at each bound — a linear factor
(multiplicity `316`), a cubic factor (multiplicity `4`), and the
large-degree `B(n)`/`B_2(n)`. The target's `ATTEMPT.md` reports the
"largest real root" using only `B(n)`/`B_2(n)` (the largest-*degree*
factor), without showing that the two smaller cofactors don't hide a
*larger* real root (degree does not by itself bound root location — the
`K=4` predecessor's document explicitly showed its analogous quadratic
cofactor had negative discriminant for exactly this reason; the `K=5`
document does not show the analogous check). This referee ran
`real_roots()` on **every** factor independently:

```
UPPER: linear factor = n (root: 0); cubic factor = 10n^3-35n^2+50n-24 (single real root: 0.905...)
       => GLOBAL largest real root across ALL factors of S(n): 4.14332471584019   (matches B(n) alone)
LOWER: linear factor = n (root: 0); cubic factor = 10n^3-35n^2+50n-24 (single real root: 0.905...)
       => GLOBAL largest real root across ALL factors of S(n): 4.38060345726791   (matches B2(n) alone)
```

Both smaller cofactors' real roots (`0` and `\approx0.905`) sit far below
the reported thresholds, confirming no larger real root was silently
missed. **The target's numeric claim is correct**; only the write-up's
justification for it was less complete than `K=4`'s analogous passage —
see Finding F1 below.

### Item 4 (task §d) — Root-selection methodology: CONFIRMED robust

`g_5'(x)=5(x-1)^3(x+1)^2(20x^4-7x^3+x^2+3x-1)` has exactly `7` real
roots counted with multiplicity: `\{-1,-1,-0.509167962464232,
0.309430603103057,1,1,1\}` — `-1` with multiplicity `2` (matching
`(x+1)^2`), `1` with multiplicity `3` (matching `(x-1)^3`), plus the
quartic's own `2` real roots (`0.3094\ldots\in(0,1)`, and
`-0.5092\ldots\notin(0,1)`), confirmed by this referee's own
`Poly(g5p,x).real_roots()` call. The `0<x<1` filter, applied to the
exact algebraic reals (never to a symbolic radical form or a `sp.solve()`
output), correctly and unambiguously isolates the single genuine
interior critical point. No `sp.solve()` is used anywhere in either the
target's or this referee's pipeline for this step, avoiding the
predecessor's self-disclosed `.is_real`-on-nested-radicals bug by
construction. This referee could not find any point at which a spurious
or wrong root could have been selected: `real_roots()` returns exact
isolating intervals (not floating-point approximations subject to
misclassification), and the numeric filter `0<sp.N(x)<1` is applied only
to disambiguate among already-exact candidates, never to determine
reality.

One structural observation, not a defect: because the resultant-
elimination step's exclusion argument ("no real `x` at all, over *all*
reals, solves `F_1=F_2=0`" `\Rightarrow` "no real `x\in[0,1]`" does
either) is a one-directional implication, it is inherently immune to the
*specific* failure mode that produced the `K=4` predecessor's lower-bound
"wrinkle" (an inflated-but-still-valid threshold from an out-of-domain
branch). At `K=5` this doesn't matter in practice anyway, since both
interior thresholds land safely *below* the domain start regardless of
which branch drives them — but it is worth noting explicitly that the
construction's logical safety here does not depend on correctly
diagnosing *which* branch is responsible, unlike the `K=4` case.

### Item 5 — Governance / scope-discipline checks: CLEAN

- **Files outside the target's own directory:** `git diff --stat` and
  `git status --porcelain` against `THEOREM.md`,
  `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, and
  `05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md` are **empty** — despite these
  files showing recent filesystem mtimes (from unrelated read/checkout
  activity), they carry **zero uncommitted changes** relative to the
  repository `HEAD`. `DISC-DEC-134`'s own ledger text (front (c)) matches
  the target's stated mandate exactly.
- **Untracked files elsewhere:** `git status --porcelain` shows two
  untracked directories outside the target's own tree —
  `cu_direct_proof_attempt/` (under an entirely different
  `tauberian_oscillation_bound_attempt` lineage, `DISC-DEC-134` front
  (a)'s own new work) and a pre-existing `k3_full_cdf_attempt_ABANDONED_STALLED/`
  directory — neither attributable to this front by path or content.
- **Seed range** `20260944000`–`20260944999`: grep-confirmed unused
  anywhere in `05_DISCOVERY_LAB/` except the target's own reservation
  notice and its self-quoted grep output (matching the target's own
  claim that no randomness was needed).
- **No `adversarial/` subdirectory pre-existed** in the target's own
  directory before this review (confirmed by directory listing) — no
  referee was dispatched by the target itself, as its mandate required.
- **No `git` command run by the target:** `git reflog` shows only the
  orchestrating session's own prior integration commits (wave-by-wave
  `Integrate ...` commits); the target's own files are untracked
  (uncommitted), consistent with no `git` activity from this front.
- **No `git` command was run by this referee** at any point (per
  instruction); all checks above used only `git status`/`git diff`/`git
  reflog` in read-only mode, `stat`, and `grep`.

---

## 3. Named findings

**Finding F1 (LOW severity, expository/completeness only — no
correctness impact).** §5.1–5.2 of the target's `ATTEMPT.md` report the
"largest real root" of `S(n)`/`S_2(n)` by running `real_roots()` only on
the largest-*degree* factor (`B(n)`/`B_2(n)`) that `factor_list`
isolates, without explicitly showing that the two smaller cofactors
(linear, multiplicity `316`; cubic, multiplicity `4`) cannot hide a
*larger* real root — unlike the `K=4` predecessor's document, which
explicitly showed its analogous quadratic cofactor had negative
discriminant (hence provably no real roots at all) as reassurance on
exactly this point. This referee independently checked all factors at
both bounds (§2 Item 3 above, `adv4_all_factors_root_check.py`/`.log`)
and confirmed the smaller cofactors' real roots (`0`, and `\approx0.905`
from the cubic) are far below the reported thresholds — **the target's
numeric claims are correct**; only the write-up omits the explicit
check that would rule this out by construction rather than by
after-the-fact confirmation. Recommended fix for a future revision:
print each cofactor's own real roots (or, for the cubic, its
discriminant/root bound), mirroring `K=4`'s level of disclosure.

No other issues, of any severity, were found. No mathematical claim in
the target's document — Proposição D5, `g_5`, `M_5` and its minimal
polynomial, either resultant-elimination threshold, the boundary
threshold, the final `n_0=7`, or the "no `K=4`-style wrinkle" diagnosis
— was found to be incorrect, unverified, or under-verified in a way that
survives independent reconstruction.

---

## 4. Answering the task's explicit questions

- **Is Proposição D5's derivation genuine, non-circular, and correct?**
  Yes. Independently re-derived from the cited (already separately
  proved and adversarially reviewed) general-`K` machinery by a
  from-scratch pipeline that also reproduces `D1`–`D4`, then confirmed
  against a from-scratch brute-force enumeration of Definition 4 at
  `K=5`. Both routes agree with the target's claim and with each other,
  with zero discrepancy.
- **Does `n_0=7` survive independent scrutiny?** Yes, completely. Every
  number feeding into it — `M_5`'s minimal polynomial, the boundary
  threshold `6.2962\ldots`, and both interior resultant-elimination
  thresholds `4.14\ldots`/`4.38\ldots` — was independently reproduced to
  every digit shown, and this referee additionally confirmed (beyond
  what the target itself showed) that no factor of `S(n)`/`S_2(n)` hides
  a larger real root than reported.
- **Does `K=5` need a `K=4`-style wrinkle?** No — independently
  confirmed. Both interior thresholds sit comfortably below the boundary
  threshold and below the domain start, so no out-of-domain-branch
  diagnosis or exhaustive per-`n` patch is logically necessary here,
  regardless of which conjugate root any given branch happens to realize
  (see Item 4 above).
- **Was the overall verdict (CLOSED, `M_5` exact, `n_0=7`) fully
  justified by the evidence presented?** Yes, and this referee's
  independent reconstruction supplies additional evidence (the
  full-factor root check, Item 3/Finding F1) beyond what the target
  itself presented.

---

## 5. File manifest (this referee's own work)

| File | Role |
|---|---|
| `adv1_D5_derivation.py`/`.log` | Independent re-derivation of Proposição D5 from the cited general-K machinery (Proposição S / Decomposition Theorem / Layer-1 InnerJ); reproduces D1–D4 exactly; matches the target's claimed D5 with zero symbolic difference. |
| `adv2_bruteforce_def4_k5.py`/`.log` | Independent, fully exhaustive brute-force enumeration of Definition 4 at K=5, n=5,6 — 11/11 exact matches against D5. |
| `adv3_g5_M5_resultant.py`/`.log` | Independent re-derivation of g5, g5', M5 (+ minimal polynomial, mpmath cross-check), boundary threshold, and both resultant eliminations (upper/lower) — every headline number reproduced exactly. |
| `adv4_all_factors_root_check.py`/`.log` | Extra check (Finding F1): confirms the smaller cofactors of S(n)/S_2(n) do not hide a larger real root than the one reported from B(n)/B_2(n) alone. |

---

## 6. Summary

| # | Item | Result |
|---|---|---|
| 1 | Proposição D5 derivation from cited general-K machinery | **PASS**, independently reproduced, zero symbolic difference; self-validation against D1–D4 confirmed genuine |
| 2 | Fresh brute-force cross-check, Definition 4, K=5, n=5,6 | **PASS**, 11/11 exact matches, independent implementation |
| 3 | g5, g5' factorizations, M5 + minimal polynomial | **PASS**, exact match, cross-confirmed via independent `sp.minimal_polynomial` and from-scratch `mpmath` |
| 4 | Boundary threshold + both resultant-elimination thresholds | **PASS**, exact match to every digit shown |
| 5 | "No K=4-style wrinkle" diagnosis | **CONFIRMED** — both interior thresholds below boundary threshold and domain start |
| 6 | All-factor root check (beyond target's own document) | **PASS**, no hidden larger real root — Finding F1 (LOW, expository only) |
| 7 | Root-selection methodology (§4.2) | **CONFIRMED robust**, no spurious/wrong root selectable |
| 8 | Governance / scope discipline | **CLEAN** |

**Bottom line:** the target's central claims are true and the proofs
are sound. This is a genuinely new, non-trivial mathematical result
(Proposição D5) built correctly on already-proved machinery, combined
correctly with the already-validated resultant-elimination method, and
every load-bearing number survives hostile, independent, from-scratch
reconstruction. One LOW-severity, purely expository finding (F1) is
named for a future write-up revision; it does not affect the truth of
any claim in the document.

No Millennium Problem framing anywhere in this report or in the target.
Pure combinatorial mathematics internal to this archive (the `u12`
permutation-with-reroutes ensemble).
