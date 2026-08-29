# Hostile Referee Report — K6-EXACT-CLOSURE-ATTEMPT

**Target:** `.../sharp_rate_constants_attempt/exact_algebraic_closure_attempt/
k5_exact_closure_attempt/k6_exact_closure_attempt/ATTEMPT.md`
(wave 30, front (b), `DISC-DEC-138`(b))

**Referee:** dedicated hostile session. Read, in full, before opening any
of the target's own scripts: `k5_exact_closure_attempt/ATTEMPT.md`
(immediate predecessor, `K=5` exact closure) and its own
`adversarial/REFEREE_REPORT.md`; `THEOREM.md` Estágios 46, 48
(`K=2,3,4` exact closure, including `K=4`'s own lower-bound "wrinkle"
at `n≈64.77` and its §5.1 `count_roots`-vs-`real_roots` performance
finding) and 53 (`K=5` integration); `THEOREM.md` Definition 4
(lines 859–872); `exact_algebraic_closure_attempt/ATTEMPT.md` in full
(the `K=3,4` document itself, not just its `THEOREM.md` summary — its
§4.5 wrinkle narrative and §5.1 performance diagnosis are the direct
template this front extends). Only after this reading, and after
independently reconstructing the target's central claims from the cited
general-`K` machinery and from first principles, was any of the target's
own `.py` scripts opened — read only to confirm which specific numeric
claims to check, never copied.

---

## VERDICT: SOUND WITH ISSUES — ACCEPT for catalogue integration. Six LOW-severity, purely expository/documentation findings (all "nota"); zero "correção"-level (correctness) findings.

The target's central claims — (1) Proposição D6, a genuinely new
closed-form CDF for `K=6`, derived by instantiating the archive's
already-proved general-`K` machinery at the concrete value `K=6`; (2)
full **exact** closure of the sharp finite-`n` rate constant,
`|F_n^{(6)}(x)-F_6(x)|\le M_6/n` for all integer `n\ge8`, via a **novel**
shift-certificate technique (Descartes' rule of signs after a
`Poly.shift()` Taylor shift) that replaces the `factor_list`-then-
`real_roots()` recipe used at `K=2,\ldots,5` because that recipe did not
finish in practical time on `K=6`'s degree-`1052`/`1056` resultant
polynomials; and (3) a **genuine, confirmed** `K=4`-style lower-bound
"wrinkle" (a real root of the lower-target resultant polynomial strictly
between `n=34` and `n=35`), resolved by an exact per-integer-`n` patch —
**all hold up completely under independent, hostile, from-scratch
reconstruction.**

Every headline number and every headline *technique* this referee
attempted to independently reproduce was reproduced **exactly**, via
genuinely separate code (typed fresh from the cited mathematical prose
and from first principles, never from the target's `.py` files, except
where explicitly noted as a deliberate reproducibility check of the
target's own script in unmodified form — §2 Item 6 below):

- Proposição D6 itself, reproduced **symbolically, with zero
  difference**, by an independently-typed pipeline that also reproduces
  `D1`–`D5` — including catching, diagnosing, and fixing a **referee's
  own bug** along the way (a wrong assumption that the `r=0` edge case
  needed no special-casing), which ended up **independently confirming**
  that the target's own explicit `r=0` special case is mathematically
  *necessary*, not an arbitrary implementation choice.
- The same `D6` formula independently confirmed against a **fresh,
  independent, fully exhaustive** brute-force implementation of
  Definition 4 at `K=6`, `n=6` (`6/6` exact matches), using a
  **structurally different** cyclic-point detection algorithm from the
  target's own (forward-iteration-and-check instead of the
  colour/visited-frontier walk) — and matching the target's own reported
  per-`k` counts to the exact integer.
- `g_6(x)`, `g_6'(x)`'s factorizations, the interior quartic's
  irreducibility, `M_6`'s value and irreducible minimal quartic (exact
  match, confirmed via an independent `sp.minimal_polynomial` call).
- The full resultant-elimination construction end-to-end: `R(n,m)`
  (degree `264`/`11`, `20.13`s), `S(n)` (degree `1052`), `S_2(n)` (degree
  `1056`) — all exactly matching the target's claimed degrees.
- **THE headline novel-technique claim**, the single highest-priority
  item of this review: `S(y+8)` has uniform-sign (all negative)
  coefficients (proving `S(n)` has no real root `>8`, in fact `\ge8`
  since `S(8)` itself — a `1207`-digit integer — is confirmed nonzero and
  shares the sign); `S_2(y+8)` is confirmed **not** uniform-sign (the
  genuine wrinkle is real, not a fabricated pretext); `S_2(y+35)` **is**
  uniform-sign (proving `S_2(n)` has no real root `>35`); and the sign
  change of `S_2(n)` strictly between `n=34` and `n=35` is confirmed by
  direct integer evaluation, all reproduced independently, exactly.
- The boundary threshold `n_0^{\text{boundary}}=7.278581437127420988290004\ldots`
  — reproduced independently (after catching and fixing a **sign bug in
  this referee's own first attempt**, disclosed below), and confirmed to
  be genuinely the larger of the two candidate boundary-crossing
  branches, not an arbitrary choice of "the relevant one."
- The exact per-integer patch, independently spot-checked at
  referee-chosen `n\in\{8,20,34,35,42,50,100\}` — including the two most
  adversarially interesting points (`n=34,35`, straddling the confirmed
  `S_2(n)` sign change) — zero violations, matching the target's own
  values to every digit shown where they overlap.
- The `n_0=8` **tightness** claim: `h_6(7,1)=-1` exactly, and
  `-1<-M_6\approx-0.6797`, confirming `n=7` genuinely violates the lower
  bound.

One additional, structural point independently confirmed **beyond** what
the target's own document shows: the K=5 predecessor's referee Finding
F1 (a LOW-severity concern about smaller cofactors possibly hiding a
larger real root) genuinely **cannot arise** for this front's own method,
because the shift certificate is applied directly to the full, unfactored
`S(n)`/`S_2(n)` — there is no cofactor-splitting step anywhere in the
load-bearing proof chain for this front to have omitted a check on. This
front's own §5.3 claims this; this referee independently confirms the
reasoning is sound, not merely rhetorically appealing.

Six LOW-severity, purely expository/documentation findings are named
below (§3) — a citation/timing-source mismatch, an unbacked (now
independently supplied) validation claim, a stale crash-triggering
default argument, a loose word choice ("coefficients" for what are
actually evaluated values), a dangling file reference, and a slightly
under-confident framing of an already-explained pattern. **None affects
the correctness of any mathematical claim** — `M_6`, Proposição D6, both
resultant-elimination thresholds, the shift-certificate results, the
confirmed-and-resolved wrinkle, and the final `n_0=8` all survive
independent, hostile, from-scratch reconstruction intact.

---

## 1. Methodology

Reading order matched the task's instructions exactly (see header
above). Before opening any of the target's own scripts, this referee:
(a) independently re-typed the general-`K` CDF pipeline from the two
boxed formulas cited in both the `K=5` and `K=6` `ATTEMPT.md` documents
(Estágio 41's Proposição S, Estágio 44's `S_r`/`InnerJ` formulas),
self-validated it against `D1`–`D5`, and only then computed `D6` and
diffed it against the target's own claimed `Bracket6`; (b) independently
wrote a structurally different brute-force Definition-4 engine; (c)
independently re-derived `g_6`, `g_6'`, `M_6`, and the entire
resultant-elimination + shift-certificate construction from scratch,
reusing only the (by-then independently-confirmed) `D6` formula as a
starting point. The target's own `.py` files were read only afterward,
to confirm which specific numeric claims and technique details to check
— never copied into this referee's own scripts, which use different
variable names, different control flow, and in several places
deliberately different algorithms (see §2 Item 2, Item 6).

All computation was run in this session's own environment (`Python
3.11.15`, `sympy 1.14.0`, `mpmath 1.3.0`, `4` CPU cores) — the same
versions the target itself reports using.

Every script referenced below (`adv1`–`adv6`) was written fresh by this
referee and is persisted, with its full logged output, in this
directory.

---

## 2. Item-by-item results

### Item 1 — Proposição D6's derivation: PASS, independently reproduced from the cited general-K machinery

Highest-priority check alongside Item 3 below, since (exactly as at
`K=5`) `K=6` has no closed-form CDF anywhere else in the archive
(grep-confirmed by this referee independently: no `k6_full_cdf_attempt`
directory exists; `THEOREM.md` Estágios 44/45 certify Gosper
non-existence only for `K` symbolic).

This referee typed, from scratch, an independent pipeline
(`adv1_D6_derivation.py`) directly from the two boxed formulas cited in
the target's own §3.1 (themselves cited, PROVED elsewhere, from Estágios
41/44). **A genuine bug was caught during this referee's own
development**, disclosed here in the same spirit this archive's own
fronts disclose self-caught issues: an initial version assumed the `r=0`
case of `S_r(n,K,k)` needed **no** special-casing, reasoning (incorrectly)
that the generic `V`-sum with the blanket convention `C(x,\text{negative})=0`
would naturally collapse to the correct single `V=0` term. It does not —
that blanket convention zeroes the *entire* `r=0` contribution at every
`V`, including `V=0`, because `r-1=-1<0` triggers unconditionally. Caught
immediately by the `K=1` self-validation assertion failing. Root-caused
(via first-principles combinatorial reasoning about what `C(V-1,r-1)`
actually counts) and fixed by special-casing `r=0` exactly as the
target's own `d6_derivation.py` does. **This is a positive finding, not
a defect**: it independently confirms, via an actual failed alternative
that this referee tried and diagnosed, that the target's own `r=0`
special case is mathematically *necessary*, not an arbitrary
implementation choice. Full disclosure and fix are documented in the
script's own docstring.

With that fix, all five self-validations pass:

```
K=1 vs D1 (Estagio 27): MATCH (diff=0)
K=2 vs D2 (Estagio 42): MATCH (diff=0)
K=3 vs D3 (Estagio 40): MATCH (diff=0)
K=4 vs D4 (Estagio 43): MATCH (diff=0)
K=5 vs D5 (Estagio 53, cited from predecessor ATTEMPT.md Sec 3.3): MATCH (diff=0)
```

— all five **already-independently-proved** closed forms reproduced
exactly by this referee's own from-scratch pipeline. Then, at `K=6`:

```
Referee-derived D6 vs target's own claimed D6 (transcribed from
ATTEMPT.md Sec 3.3): symbolic difference = 0
EXACT MATCH -- Proposicao D6 independently confirmed correct.
```

Additional independent sanity identities (`1-D6(n,n-1)=720/n^6`,
`D6(n,0)=D6(n,-1)=0`, monotonicity at referee-chosen `n=6,7,8,11,13`,
deliberately different from the target's own spot-check `n`'s) all PASS.
Script/log: `adv1_D6_derivation.py`/`.log`.

**Verdict: Proposição D6 is independently confirmed correct**, via a
pipeline that is genuinely non-circular (independently typed from the
cited formulas, not from the target's code) and that caught and
correctly resolved its own bug along the way.

### Item 2 — Fresh brute-force cross-check of Definition 4, K=6: PASS

`adv2_bruteforce_def4_k6.py` implements a **structurally different**
cyclic-point detector from the target's own `bruteforce_definition4_k6.py`
(forward-iterate up to `n` steps and check for a return to the start,
rather than the target's colour/visited-frontier rho-walk) — a genuine
second, independent algorithm, not a re-implementation of the same one.
Run at `n=6` (the full run instructed):

```
n=6 K=6  total configs=33592320  elapsed=55.8s
counts (T=0..6): [0, 5598720, 9331200, 9331200, 6220800, 2592000, 518400]
ALL k in [0,n-1] MATCH D6: True
```

— **exact match**, digit for digit, with both the target's own reported
counts (`bruteforce_definition4_k6.log`) and with Proposição D6. `n=7`
was **not** independently re-run by this referee (the target's own run
took `804.7`s single-process; this referee's own detector is `O(n)` per
point vs. the target's `O(1)` amortised, so would be considerably
slower) — matching the `K=5` referee's own precedent and reasoning: Item
1 above already establishes `D6(n,k)` is *symbolically* correct for
**all** `n,k` simultaneously, a strictly stronger guarantee than one
more finite brute-force point could add. The target's own `n=7` log was
read and is internally consistent with everything else independently
verified here.

### Item 3 — g6, M6, and the FULL resultant-elimination + shift-certificate construction: PASS, independently reproduced end-to-end (THE central check of this review)

Starting from the referee's own independently-derived `D6` (Item 1),
`adv3_resultant_shift_certificate.py` independently re-derives
everything in the target's §4–§5:

```
g6(x) = -3x(x-1)^5(x+1)^4(5x^2-3x+2)                          [diff: 0]
g6'(x) = -6(x-1)^4(x+1)^3(30x^4-14x^3+x^2+4x-1)                [diff: 0]
interior quartic 30x^4-14x^3+x^2+4x-1 irreducible over Q: True
g6'(x): 9 real roots with multiplicity (matches -1x3, 1x4, quartic's own 2)
x6* = 0.26036172400671492484172362842265674
M6  = 0.67967830129138512967160338683005533
minpoly(M6) = 35429400000000000t^4+17921731935293824t^3
              -248044660324924125t^2+350950285900800000t-137134080000000000
              [ratio to target's claimed form: exactly 1 -- identical]
```

**Boundary threshold — a self-caught sign bug, disclosed.** This
referee's *first* attempt at the boundary elimination (solving
`h_6(n,1)=-M_6` via resultant elimination against `M_6`'s minimal
polynomial) used the wrong substitution branch (`t\to-m` instead of
`t\to m`, having mislabeled which branch corresponds to which physical
crossing), producing a spurious `n_0^{\text{boundary}}=6.2608670274\ldots`
that did **not** match the target's claimed `7.2785814371\ldots`. Caught
immediately by the mismatch; root-caused by an independent `mpmath`
direct numeric solve of `h_6(n,1)=-M_6` (bracketing and Newton-polishing,
zero resultant machinery), which confirmed `7.2786\ldots` is genuinely
correct and pinpointed the referee's own sign transcription as the bug —
**not** an error in the target. After the fix:

```
n0_boundary (h6(n,1)=-M6 crossing) = 7.278581437127420988290004...
```

— **exact match** to every digit the target reports. `adv6_supplementary_checks.py`
additionally confirms this is genuinely the *larger* of the two candidate
boundary branches (`7.2786\ldots` vs. the other, physically-irrelevant
branch's own largest root `6.2609\ldots`) — picking "the relevant one"
was not an arbitrary or lucky simplification.

**Resultant construction:**

```
Res_x(F1,F2): degree 264 in n, degree 11 in m       [20.13s -- matches target]
S(n) [upper target]:  degree 1052                    [5.28s]
S2(n) [lower target]: degree 1056                    [5.97s]
```

— all exactly matching the target's claimed degrees.

**THE headline shift-certificate claims — independently verified, exactly:**

```
(a) S(y+8) uniform-sign (all -1)      => NO real root of S(n) exceeds 8.
    S(8) itself: nonzero, 1207-digit integer, sign -1 (same sign as every
    other coefficient) => rigorously NO real root of S(n) is >= 8 either
    way -- confirms the target's stronger "n>=8" claim (not merely "n>8").
    S2(y+8) uniform-sign: False  -- CONFIRMED inconclusive (the wrinkle
    is genuine, not a fabricated pretext for switching methods).
(b) S2(y+35) uniform-sign (all +1)    => NO real root of S2(n) exceeds 35.
    S2(y+34) uniform-sign: False -- confirms 35 is genuinely where the
    certificate first clears, not an arbitrary overshoot.
```

**Direct sign evaluation, confirming the genuine sign change:**

```
S2(28..34) sign = -1 (all)
S2(35..37) sign = +1 (all)
=> sign change strictly between n=34 and n=35.  CONFIRMED.
```

— exact match to the target's own reported values.

**On the shift-certificate technique's mathematical soundness itself**
(the task's highest-priority scrutiny item): this referee independently
sanity-checked `sympy`'s `Poly.shift(B)` on toy examples
(`adv6_supplementary_checks.py`, part A) — confirmed it computes `P(y+B)`
exactly, as a polynomial in the *same* generator symbol, and that the
resulting "uniform-sign-after-shift ⟹ no root exceeds `B`" certificate
correctly distinguishes `B` below vs. at-or-above a *known* root location
(a toy polynomial `(n-5)(n-2)` with a known largest real root at `5`:
`shift(4)` gives mixed signs, `shift(5)` and `shift(6)` give uniform
signs, exactly as the classical Descartes-rule-of-signs-after-Taylor-shift
argument predicts). This is a completely standard, textbook root-bounding
technique (a special case of the classical fact that a polynomial with
all-nonnegative coefficients has no positive real root, applied after a
shift to move the region of interest to the positive axis) — correctly
stated and correctly implemented by the target. The logical composition
with the rest of the resultant-elimination proof is also sound: `S(n)=0`
is a *necessary* condition for a genuine real interior critical point
achieving `h_6(n,x)=M_6` at that `n` (by construction of the elimination
chain `F_1,F_2\to R\to S`), so `S(n)\ne0` for `n>8` (or `\ge8`) rigorously
rules out such a violation there — exactly the same logical shape already
validated at `K=2,\ldots,5`, only the *method of proving* `S(n)\ne0` in
this range is new (uniform-sign-after-shift instead of exhaustive root
isolation). **This referee independently confirms the shift-certificate
technique is mathematically sound, correctly stated, and correctly
applied**, both in general principle and in this specific instance.

Script/log: `adv3_resultant_shift_certificate.py`/`.log`,
`adv6_supplementary_checks.py`/`.log`.

### Item 4 — The confirmed, resolved lower-bound wrinkle: PASS, independently confirmed genuine AND resolved

Beyond Item 3's shift-certificate confirmation, `adv4_patch_spotcheck_and_tightness.py`
independently spot-checks the exact per-integer-`n` patch at
referee-chosen `n\in\{8,20,34,35,42,50,100\}` — deliberately including
the two most adversarially interesting integers, `n=34` and `n=35`,
straddling the confirmed `S_2(n)` sign change (if the "extraneous
resultant branch, not a real theorem violation" diagnosis were wrong,
this is exactly where a genuine violation would first appear):

```
n= 34: max_x h6 = 0.564972652570038765952293302247 (<=M6: True)
       min_x h6 = -0.000472144315610147970828509815556 (>=-M6: True)
n= 35: max_x h6 = 0.568225893094488540694319317582 (<=M6: True)
       min_x h6 = -0.000405733760824339672570701951487 (>=-M6: True)
```

— zero violations, matching the target's own `k6_exact_patch_n8_42.log`
values exactly at every overlapping `n`. All seven referee-chosen `n`
pass.

**Verdict: the `K=4`-style lower-bound wrinkle at `K=6` is genuine (a
real root of `S_2(n)` in `(34,35)`, confirmed by direct sign evaluation,
not a red herring or sign error) and is genuinely and fully resolved**
by the exact per-integer patch plus the shift-certificate interior bound
(`\le35`) plus the continuity+IVT argument for `n>35` — the same
methodological pattern `K=4`'s own predecessor used, correctly applied.

### Item 5 — n_0=8 tightness: PASS, independently confirmed

```
h6(7,1) [exact] = -1
-M6 = -0.679678301291385129671603386830
-1 < -M6  =>  n=7 GENUINELY VIOLATES the lower bound.
```

Independently confirmed exactly (`adv4_patch_spotcheck_and_tightness.py`),
including the context that the minimum at `n=7` is achieved exactly at
the boundary `x=1`, matching `h_6(7,1)` — consistent with the general
picture that the boundary term, not an interior critical point, drives
the violation just below the domain. `n_0=8` is confirmed to be the true
minimal integer threshold, not merely an upper bound on sufficiency.

### Item 6 — Self-caught issues (target's own §7): all fixes confirmed genuinely present in the final code

- **Issue #1** (wrong `assert deg_k==10`): confirmed fixed — the current
  `d6_derivation.py` correctly asserts the full numerator's degree in `k`
  is `12` and, only after dividing by `k(k+1)`, asserts the resulting
  `Bracket6`'s degree is `10`. No lingering trace of the described bug.
- **Issue #2** (bruteforce crash at `n=5`, `assert 0<=K<=n`): the guard
  is present (`bruteforce_definition4_k6.py` line 65) and is the correct,
  intentional fix for the described crash. **However** (see Finding F3
  below), the script's own *default* argument fallback (line 125,
  `ns = [...] or [5, 6, 7]`) still begins at `n=5` — running the script
  today with no arguments would immediately reproduce the exact disclosed
  crash. The logged run (`bruteforce_definition4_k6.log`) shows only
  `n=6,7` were ever processed, confirming the script was actually invoked
  with explicit arguments bypassing the buggy default — so no wrong
  result was ever produced, but the self-disclosure's phrasing ("Fixed
  by starting the sweep at n=6") is imprecise about *where* the fix
  lives (the invocation, not the code's own default).
- **Issue #3** (`k=n` boundary, `D6(n,n)\ne1` via the rational formula):
  confirmed correctly handled — `bruteforce_definition4_k6.py` restricts
  the per-`k` match loop to `0\le k\le n-1` and checks `k=n` separately
  via `1-D6(n,n-1)=720/n^6`, exactly as described.
- **Issue #4** (`sp.solve()`/`.is_real` bug avoidance): confirmed — a
  grep across every `.py` file in the target's directory finds **zero**
  occurrences of `sp.solve(` or `.is_real` anywhere; `real_roots()` is
  used throughout for all root-selection steps (`7` occurrences across
  `4` files), exactly matching the archive's own precedent-driven
  discipline.
- **Issue #5** (the central computational-obstacle narrative — three
  failed `factor_list`/`real_roots` variants, pivot to the shift
  certificate): the *conclusion* (the shift certificate completing in
  `0.05`–`0.2`s where the old recipe did not finish in `>4`–`>17`
  minutes) is independently reproduced and confirmed exactly (Item 3
  above). The failed-attempt *timings themselves* were not independently
  re-run (reproducing multi-minute timeouts would consume significant
  compute budget for no additional verification value — the object of
  the check, the successful shift-certificate result, is what this
  referee actually needed to verify, and did). One wording imprecision
  is named as Finding F4 below (§5.2's "~1800 decimal digits" figure
  actually describes evaluated values, not raw stored coefficients).
- **Issue #6** (scratchpad file-collision, environment-level, unrelated
  to the mathematics): not independently verifiable from outside the
  target's own session (it is a claim about that session's own working
  environment). This referee notes that **every** numeric and symbolic
  claim in the final `ATTEMPT.md` has been independently reproduced from
  its permanent `.py`/`.log` artifacts with zero discrepancy (aside from
  this referee's own two self-caught and immediately-fixed bugs, both
  clearly attributable to this referee's own transcription, not to the
  target) — fully consistent with the front's own claim that no
  mathematical content was lost in the collision, since everything
  checks out against what *is* on disk.

### Item 7 — Governance / scope-discipline checks: CLEAN

- **Files outside the target's own directory:** `git status --porcelain`
  shows only the target's own new directory (untracked) and one
  pre-existing, unrelated `k3_full_cdf_attempt_ABANDONED_STALLED/`
  directory — not attributable to this front. `git diff --stat` against
  `THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md` is
  **empty**.
- **Mandate text:** `DISC-DEC-138`'s own ledger entry (frente (b)) was
  read directly from `DECISION_LEDGER.yaml` and matches the target's own
  quoted mandate text exactly, verbatim.
- **No `adversarial/` subdirectory pre-existed** in the target's own
  directory before this review (confirmed by directory listing before
  this referee created one).
- **No `git` command run by the target:** `git reflog` shows only the
  orchestrating session's own prior wave-integration commits; the
  target's own files remain untracked.
- **Seed range** `20260946000`–`20260946999`: grep-confirmed unused
  anywhere in `05_DISCOVERY_LAB/` except the target's own reservation
  notice and its self-quoted grep output.
- **No randomness anywhere:** grep for `random`/`seed`/`np.random`
  across every `.py` file in the target's directory finds only one
  unrelated prose match (a docstring's use of the English word "random"
  describing the combinatorial object, not a call to any randomness
  API) — confirming the target's own claim.

---

## 3. Named findings

All six findings below are **LOW severity, "nota"** — clarifications or
write-up-precision points, **not** "correção"-level correctness errors.
None affects `M_6`, Proposição D6, either resultant-elimination
threshold, the shift-certificate results, the confirmed-and-resolved
wrinkle, or the final `n_0=8`.

**Finding F1 (nota).** ATTEMPT.md §6.1 states the exact per-integer patch
took "`100.7`s total" and cites `k6_exact_patch_n8_42.log` as the "Full
transcript" — but that log file's own printed total is `104.7`s (its
line 38), not `100.7`s. The `100.7`s figure actually appears in the
*other* file, `k6_exact_closure.log` (its Step 6). Both numbers are
genuine (two separate runs of the same deterministic computation
naturally have different wall-clock times), and all the underlying
numeric results (max/min `h_6` at each `n`) are byte-identical between
the two logs — this is a citation slip (the wrong source is named for a
timing figure), not a computational error.

**Finding F2 (nota, now independently closed by this review).** §10's
file manifest claims `n8_attempt_k6.py` was "validated correct via a dry
run at `n=6` matching `bruteforce_definition4_k6.py` exactly" — but no
such dry-run log exists anywhere in the target's own directory (only
`n8_attempt_k6_incomplete.log`, the `120`-byte startup header of the
never-completed `n=8` attempt). This claim was, as delivered,
unverifiable from the target's own artifacts — a real (if minor) gap
against this archive's own stated discipline of persisting every claim
to a log. This referee independently performed exactly this dry run
(`adv5_n8_engine_dryrun_at_n6.py`, patching `N=8\to6` into an unmodified
copy of the target's own multiprocessing engine) and **confirms the
underlying claim is true**: the engine produces the identical counts
array (`[0, 5598720, 9331200, 9331200, 6220800, 2592000, 518400]`) as
both the target's own `n=6` run and this referee's own independent `n=6`
brute force — so the multiprocessing chunking logic genuinely is correct
and would have produced the right answer had the `n=8` run completed.
The gap was purely a missing artifact, now supplied.

**Finding F3 (nota).** Self-caught issue #2 states the `n=5` crash was
"Fixed by starting the sweep at `n=6`" — but `bruteforce_definition4_k6.py`'s
own default argument fallback (line 125) is still `[5, 6, 7]`, which
would reproduce the exact disclosed crash if the script were run today
with no command-line arguments. The actually-logged run only processed
`n=6,7`, confirming explicit arguments were used in practice — no wrong
result was ever produced or reported — but the fix lives in *how the
script was invoked*, not in the script's own code, making the
disclosure's phrasing slightly imprecise about where the fix resides.

**Finding F4 (nota, very minor).** §7 issue #5 states "`S(n)`'s
coefficients run to `\sim1800` decimal digits, per direct inspection in
§5.2's integer-evaluation step." Independently confirmed
(`adv6_supplementary_checks.py`, part C): `S(n)`/`S_2(n)`'s own raw
stored polynomial coefficients top out around `543` digits; the
`\sim1800`–`1900`-digit magnitude actually comes from **evaluating**
`S_2(n)` at specific large integers (e.g. `S_2(35)` has `1918` digits) —
exactly the computation §5.2 performs. The claimed magnitude is accurate
and independently confirmed; "coefficients" is a loose description of
what is actually an evaluated value.

**Finding F5 (nota, cosmetic).** `n8_attempt_k6.py`'s own final `print`
statement references a file `n8_crosscheck_k6.py` ("Cross-check against
Proposicao D6 ... is performed separately by n8_crosscheck_k6.py") —
this file does not exist anywhere in the target's directory and is not
mentioned in `ATTEMPT.md`. Harmless: the `n=8` run never completed, so
this line never actually printed in the logged (incomplete) run, and no
claim anywhere depends on this file existing. A vestigial/dangling
reference, worth cleaning up in a future revision.

**Finding F6 (nota).** §8's disclosure of the alternating boundary-term
sign pattern ("K=3,5: positive; K=4,6: negative — an alternating-by-two
pattern visible now across four data points, suggestive but unproven as
a general fact") slightly undersells what is already available: the
immediate predecessor's own `ATTEMPT.md` §5.3 (part of this front's own
mandatory reading, item 1) already states the general closed form
`h_K(n,1)=(-1)^{K+1}K!/[(n-1)\cdots(n-K+1)]`, whose sign manifestly
alternates with *every* unit increase in `K` (not merely "by two," and
not merely an empirical coincidence across four spot-checked values).
This referee independently confirmed this formula continues to hold
exactly at `K=6`: `h_6(n,1)=(-1)^7\cdot720/[(n-1)\cdots(n-5)]=
-720/[(n-1)\cdots(n-5)]`, matching exactly. Nothing false is claimed —
a fully general, `K`-free *proof* of this formula is indeed not on
record in the archive — but the "suggestive... unproven" framing reads
more tentative than warranted given the front's own cited source already
supplies the explanation.

No other issues, of any severity, were found. No mathematical claim in
the target's document — Proposição D6, `g_6`, `M_6` and its minimal
polynomial, the shift-certificate technique and both its headline
results, the confirmed-and-resolved lower-bound wrinkle, the boundary
threshold, the final `n_0=8`, or the "no new Galois obstruction"
diagnosis — was found to be incorrect, unverified, or under-verified in
a way that survives independent reconstruction.

---

## 4. Answering the task's explicit questions

- **Is the lower-bound wrinkle genuine (not a red herring or sign
  error), and does the patch genuinely cover and resolve it?** Yes,
  fully independently confirmed. `S_2(n)`'s sign change strictly between
  `n=34` and `n=35` was reproduced by direct integer evaluation
  (Item 3), and the exact per-integer patch was independently
  spot-checked at the two most adversarial points (`n=34,35`) plus five
  others spanning the patch range and beyond — zero violations
  throughout.
- **Is the shift-certificate technique mathematically sound, and does
  the target apply it correctly?** Yes. It is a standard, textbook
  Descartes-rule-of-signs-after-Taylor-shift root-bounding argument.
  `Poly.shift(B)` was independently verified to compute `P(y+B)`
  correctly (toy-example sanity check). Both headline claims (`S(y+8)`
  uniform-sign; `S_2(y+35)` uniform-sign; `S_2(y+8)` correctly *not*
  uniform-sign) were independently reproduced on the referee's own
  from-scratch reconstruction of `R(n,m)`, `S(n)`, `S_2(n)` — exactly,
  including the stronger "`n\ge8`" (not merely "`n>8`") claim, verified
  via direct confirmation that `S(8)` itself is a nonzero, correctly-signed
  `1207`-digit integer.
- **Does the front's §5.3 preemptive resolution of the K=5 predecessor's
  Finding F1 actually hold?** Yes. The shift certificate is applied
  directly to the full, unfactored `S(n)`/`S_2(n)` — confirmed by this
  referee's own independent reconstruction, which likewise never
  factors either polynomial before applying the certificate. There is
  structurally no smaller cofactor anywhere in this proof's load-bearing
  chain that could hide a larger root, so Finding F1's underlying concern
  genuinely cannot arise here, by construction — not merely by
  assertion.
- **Does Proposição D6 match the general-K machinery it claims to
  instantiate?** Yes, confirmed by an independently-typed pipeline
  (built from the same cited formulas, not from the target's code) that
  also reproduces `D1`–`D5` first, with zero symbolic difference at
  every stage including `K=6` itself.
- **Are the brute-force cross-checks accurately reported, including the
  honest `n=8` non-completion disclosure?** Yes. The `n=6,7` checks were
  independently reproduced (`n=6` fully, by this referee; `n=7`
  cross-read and found consistent). The `n=8` bonus attempt's incomplete
  log (`n8_attempt_k6_incomplete.log`) genuinely shows only the startup
  header (`0/32` chunks) — the disclosure is accurate, not glossing over
  a silent failure. This referee additionally confirmed the underlying
  multiprocessing engine is itself correct (Finding F2's dry-run), so
  had more compute been available, the check would have succeeded.
- **Does `n_0=8` survive independent scrutiny as the true minimal
  threshold, not just a sufficient one?** Yes — `h_6(7,1)=-1<-M_6`
  independently confirmed exactly.
- **Are all seven self-caught issues (§7) accurately described, with
  genuine fixes present in the final code?** Yes for issues #1, #3, #4,
  and #5's central conclusion; issue #2's fix is real in effect but
  imprecisely described (Finding F3); issue #6 is not independently
  verifiable but is consistent with everything else checked out on disk.

---

## 5. File manifest (this referee's own work)

| File | Role |
|---|---|
| `adv1_D6_derivation.py`/`.log` | Independent re-derivation of Proposição D6 from the cited general-K machinery; reproduces D1–D5 exactly; catches and fixes a genuine referee-side `r=0`-handling bug along the way; matches the target's claimed D6 with zero symbolic difference. |
| `adv2_bruteforce_def4_k6.py`/`.log` | Independent, fully exhaustive brute-force enumeration of Definition 4 at K=6, n=6, using a structurally different cyclic-point detector — 6/6 exact matches against D6, exact match to the target's own counts. |
| `adv3_resultant_shift_certificate.py`/`.log` | THE central check: independent re-derivation of g6, g6', M6, the boundary threshold (catches and fixes a genuine referee-side sign bug), R(n,m), S(n), S2(n), and both headline shift-certificate claims — every number and every technique-level claim reproduced exactly. |
| `adv4_patch_spotcheck_and_tightness.py`/`.log` | Independent spot-check of the exact per-integer-n patch at referee-chosen n (including the two most adversarial points, n=34,35) plus independent confirmation of the n_0=8 tightness claim (h6(7,1)=-1<-M6). |
| `adv5_n8_engine_dryrun_at_n6.py`/`.log` | Supplies the missing dry-run validation of n8_attempt_k6.py's multiprocessing engine at n=6 (Finding F2) — confirms the engine is correct. |
| `adv6_supplementary_checks.py`/`.log` | Poly.shift(B) semantics sanity check on toy examples; confirms the boundary threshold is genuinely the larger of two candidate branches; confirms the "~1800 digits" figure's true source (Finding F4). |

---

## 6. Summary

| # | Item | Result |
|---|---|---|
| 1 | Proposição D6 derivation from cited general-K machinery | **PASS**, independently reproduced, zero symbolic difference; a referee-side bug caught and fixed along the way, itself confirming the target's `r=0` special case is necessary |
| 2 | Fresh brute-force cross-check, Definition 4, K=6, n=6 | **PASS**, 6/6 exact matches, structurally different independent algorithm |
| 3 | g6, g6', M6 + minimal polynomial, full resultant construction | **PASS**, exact match; a referee-side sign bug in the boundary elimination caught and fixed |
| 4 | Shift-certificate technique: soundness + both headline results | **PASS** — independently confirmed sound in general (toy-example check) and correct in this instance (both S(y+8) and S2(y+35) uniform-sign claims exactly reproduced, plus the stronger S(8)≠0 "n≥8" claim) |
| 5 | Genuine K=4-style lower-bound wrinkle: confirmed real + resolved | **PASS** — sign change at (34,35) independently confirmed; patch independently spot-checked at the two most adversarial points, zero violations |
| 6 | Pre-emptive resolution of K5 predecessor's Finding F1 | **CONFIRMED SOUND** — shift certificate never factors S(n)/S2(n), so no cofactor-hiding question can structurally arise |
| 7 | n_0=8 tightness (h6(7,1)=-1<-M6) | **PASS**, independently confirmed exactly |
| 8 | Self-caught issues #1–#6: fixes genuinely present | **PASS** (issues #1,3,4,5); **F3 named** (issue #2's fix location imprecisely described); issue #6 not independently verifiable (environment-level) but consistent with everything on disk |
| 9 | Governance / scope discipline / seeds | **CLEAN** |
| — | Named findings | **F1–F6, all LOW/"nota"**, zero "correção"-level findings |

**Bottom line:** the target's central claims are true and the proofs are
sound, including — the single most consequential extension over
`K=2,\ldots,5` — a genuinely new, correctly-stated and correctly-applied
shift-certificate technique that this referee independently verified
both in general principle and in every specific numeric instance it
produces, and a genuine (not spurious) `K=4`-style lower-bound wrinkle
that is fully and rigorously resolved. Six LOW-severity, purely
expository/documentation findings are named for a future write-up
revision; none affects the truth of any mathematical claim in the
document.

No Millennium Problem framing anywhere in this report or in the target.
Pure combinatorial mathematics internal to this archive (the `u12`
permutation-with-reroutes ensemble).
