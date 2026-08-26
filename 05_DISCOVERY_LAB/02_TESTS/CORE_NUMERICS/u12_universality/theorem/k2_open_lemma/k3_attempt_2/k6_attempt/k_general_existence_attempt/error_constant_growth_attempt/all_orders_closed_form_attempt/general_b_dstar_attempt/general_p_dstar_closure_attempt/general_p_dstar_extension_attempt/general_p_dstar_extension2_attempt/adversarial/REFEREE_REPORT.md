# Hostile referee report — `general_p_dstar_extension2_attempt/ATTEMPT.md`

> **Scope.** Wave 18, front (a) hostile-referee pass (`DISC-DEC-078`),
> target: the extension of the general-`p` closed-form assembly for the
> sharp error constants `D^{*(p)}_r(b)` from `p=1,...,20` (waves 15-16,
> referee-approved `DISC-DEC-070`) to `p=21,...,40` at full scale, plus a
> reduced-scale exploratory push to `p=41,...,60`. Pure combinatorics on
> the Tamesis Discovery Lab's internal random-permutation-with-reroutes
> ensemble ("u12 universality" line) — **this is NOT a Millennium Prize
> Problem and no claim of progress on one is made anywhere in this
> report.** No external data, no holdout, no real-world claim.
>
> Everything below was built from scratch in this new `adversarial/`
> subdirectory. **No `.py` file from the target front's own directory, or
> from any predecessor front in this lineage, was opened, read, or
> imported at any point** — `k2_open_lemma/`, `general_p_dstar_closure_attempt/`,
> `general_p_dstar_extension_attempt/`, and every other front in the
> chain were consulted only through their `ATTEMPT.md` prose and (for the
> two named predecessors) their `adversarial/REFEREE_REPORT.md` prose,
> per the task's explicit discipline. Every script in this directory
> (`ground_truth.py`, `ingredients.py`, `odd_part.py`, `assemble.py`,
> `sweep_main.py`, `extra_checks.py`, `random_spotcheck.py`,
> `spotcheck_printed_p21_b0.py`) is written fresh from the mathematical
> description in `THEOREM.md` and the cited `ATTEMPT.md` prose only.
> Nothing outside this directory and the target front's own directory was
> touched; `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
> `DISCOVERY_LAB_STATE.md` and every sibling front were read-only. No git
> command was run. Exact arithmetic (`fractions.Fraction`) throughout —
> no floating point anywhere in the verification code. Randomness used
> only in `random_spotcheck.py`, seeded from this referee's own reserved
> range **`20260871000+`** (`DISC-DEC-078`), confirmed unused elsewhere in
> the archive before first use (`grep -rn "20260871" 05_DISCOVERY_LAB/`
> returns only reservation lines in the ledger, the queue, and the
> target's own `ATTEMPT.md`/`DERIVATION_PREREG.md`) — the front's own
> range `20260870000-20260870999` was not touched.

## Verdict

**SOUND — ACCEPT for catalogue.**

The target document's central claim is confirmed: the already-proved,
already-referee-approved general-`p` closed-form assembly for
`D^{*(p)}_r(b)` (waves 15-16) executes correctly at `p=21,...,40`, using
no new mathematical ingredient. This referee independently re-derived and
re-implemented every ingredient of the assembly (Corollary A3 as ground
truth; `Q_p(u)` via a Newton's-identity route built on a **different**
power-sum construction than the target's own — Stirling numbers of the
second kind plus a hockey-stick identity, rather than the target's
Bernoulli-number Faulhaber route; the central moments `mu_{2l}(N)` via
the same class of power-series log/exp recurrence, independently coded;
and the `H_{2k-1}(r,b)` machine via the cited `a_k^{(d)}` recursion) and
found **zero mismatches** against an independent Corollary A3
implementation across **86,112 exact checks**, including a full
exhaustive sweep of `p=21,...,40` at `r=0,...,150`, `b=0,...,25`
(**78,520 checks, 0 fails**), a deterministic push into the reduced-scale
`p=41,...,60` region, and a randomized stress test (this referee's
reserved seed `20260871000`) reaching `r<=300`, `b<=40` for `p<=40` and
into `p<=60`.

**One genuine bug was found — in this referee's own verification code,
not in the target document** — disclosed in full in §5 below, caught by
exactly the "a check failing loudly" discipline this archive asks for,
and fixed before any result below depended on the buggy version. The
target document's own two self-disclosed bugs (§5.1-5.2 of its
`ATTEMPT.md`) were independently reproduced and confirmed plausible and
immaterial (§6 below). The document's scale claim (`r<=200,b<=30`) was
**not** matched exactly — this referee's exhaustive sweep reached
`r<=150,b<=25` for practical time-budget reasons, explicitly disclosed
in §4, with supplementary deterministic and randomized checks reaching
well beyond that reduced grid in specific directions. No mismatch of any
kind was found at any scale reached.

---

## 1. Sources read (per the task mandate)

- `THEOREM.md`: Corollary A3 (cited from `all_orders_closed_form_attempt/ATTEMPT.md`
  §4.3, itself read in `THEOREM.md`'s own "Estágio 9" account), and
  "Estágios" 8, 9, 14, 16, 21 in full (the `H_r(t,b)`/`D^*_r(0)` closed
  forms; the all-orders closed form and Corollary A3's statement;
  general-`b` `D^{*(p)}_r(b)` for `p=1..4`; the general-`p` closure
  `p=1..10`; the wave-16 extension to `p=11..20` and its referee's
  degree-bound proof).
- The target document, `general_p_dstar_extension2_attempt/ATTEMPT.md`,
  in full.
- `general_p_dstar_closure_attempt/ATTEMPT.md` (wave 15, prose only) —
  the load-bearing `H_k(r,b)` induction and the assembly formula's
  original statement.
- `general_p_dstar_extension_attempt/ATTEMPT.md` (wave 16, prose only)
  and its `adversarial/REFEREE_REPORT.md` in full — the closed
  factorization `S_{2k-1}(N,m)=A_k(N,m)*C(N,m+1)` and the proved degree
  bound `deg_r H_{2k-1}(r,b)=k-1`, leading coefficient `4^{k-1}(k-1)!`,
  that the target document (and this report) use directly as cited,
  PROVED input.

**No `.py` file from any front in this lineage was opened, read, or
imported at any point**, per the task's explicit discipline. Every
script in this directory was written from the mathematical description
above.

---

## 2. Independent re-derivation of every ingredient

### 2.1 Ground truth: Corollary A3 (`ground_truth.py`)

`D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1,j+1-p)`,
`c_j^{(r)}(b) := r!/(r-j)! / prod_{i=1}^{j+1}(r+b+i)`, `c(N,M)` the
unsigned Stirling numbers of the first kind via the standard recurrence
`c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k)`, `c(0,0)=1` — implemented directly in
`fractions.Fraction`/exact-integer arithmetic, with its own memoized
Stirling table (independent of anything in the target's or any
predecessor's code).

**Calibration** against every PROVED formula this referee could
independently confirm from `THEOREM.md`'s own text: `p=1,2` at `b=0`
(`r=0..59`); `p=1,2,3,4` at `b=1` (`r=0..79`); the wave-15 closure
attempt's cited `p=1,b=2` Theorem D1 instance (`r=0..59`); the `r<p`
vanishing boundary for `p=1,...,40` (`b=3`); a non-negativity smoke test
at six `(p,b)` combinations including `p=21,30,40`.
**Result: `1920` checks, `0` fails** (`ground_truth.log`).

### 2.2 `Q_p(u)` via a route DIFFERENT from the target document's own
(`ingredients.py`)

The target document builds power sums `P_i(u):=sum_{k=1}^u k^i` via the
classical Bernoulli-number Faulhaber formula (`B_1=-1/2` convention).
This referee deliberately used a **different** construction: power sums
via Stirling numbers of the **second** kind and the hockey-stick
identity,
`sum_{k=1}^u k^i = sum_j S2(i,j) j! C(u+1,j+1) - [j=0 correction]`
(own from-scratch derivation, no Bernoulli numbers anywhere), then
Newton's identities `p*e_p = sum_i (-1)^{i-1} e_{p-i} P_i(u)` to build
`Q_p(u) := e_p(1,...,u)` as an exact polynomial-in-`u`.

**Verified** against a *third*, completely different route — direct DP
computation of `e_p(1,...,u)` at concrete integer `u` (no power sums, no
Stirling numbers, no Newton's identity) — for `p=0,...,14`, `u=0,...,15`:
`240` checks, and the vanishing boundary `Q_p(u)=0` for `u=0,...,p-1`,
`p=1,...,40`: `760` checks (this report's `p` range, wider than the
target's own `p=1..24`). **Central moments** `mu_{2l}(N)` were built via
the classical power-series log(cosh)/exp recurrence (own from-scratch
derivation of both recurrences), verified against direct binomial
summation for `l=0,...,11`, `N=0,...,23` (`288` checks), plus
`mu_0(N)=1`, `mu_2(N)=N/4` sanity checks. **`ingredients.py` self-test
total: `1368` checks, `0` fails.**

### 2.3 The `H_{2k-1}(r,b)` machine (`odd_part.py`) — and a self-caught
bug in this referee's OWN code

Implemented via the `a_k^{(d)}(r)` recursion cited from the wave-16
referee's report (§2a-2b there), used here directly as PROVED input,
per the task mandate:

```
a_k^{(d)}(r) = (r-d+1) * [ (beta+d)^(2k-2)
                 + 2 * sum_{s odd, 1<=s<=2k-3} C(2k-2,s) * a_{(s+1)/2}^{(d+1)}(r) ]
a_1^{(d)}(r) = r-d+1,   H_{2k-1}(r,b) = a_k^{(0)}(r) / (r+1)
```

**Bug found and fixed (disclosed in full):** the first version of this
referee's `odd_part.py` implemented the bracket's summation term as
`C(2k-2,s)*a_{(s+1)/2}^{(d+1)}(r)`, **omitting the factor of `2` in front
of the sum** that the recursion above requires. This was caught by
exactly the discipline this archive's convention asks for: the degree-
bound self-test (checking `deg_r H_{2k-1}=k-1`, leading coefficient
`4^{k-1}(k-1)!`, cited from the wave-16 referee's proof) failed loudly
and systematically — `811` of `1190` checks failed, with the *measured*
leading coefficient coming out as exactly `2^{k-1}(k-1)!`, a clean
factor of `2^{k-1}` below the expected `4^{k-1}(k-1)!` at every `k`
tested, which localized the missing-factor-of-2 bug immediately (a
missing `2*` on a term whose recursive depth is `k-1` compounds
multiplicatively into exactly a `2^{k-1}` shortfall). **Fixed** by adding
the missing `2*`; re-verified: `0` mismatches everywhere afterward,
including re-confirming `H_1=1`, `H_3=(b+1)^2+4r` (the two base cases
`THEOREM.md`/the wave-15 document quote) and the degree bound out to
`k=45` (§4 below). The bug never propagated into any result reported in
this report — it was caught before `assemble.py` was written.

**Verified**, post-fix, three independent ways: against a brute-force
recursive re-implementation of the ORIGINAL cited `S_{2k-1}(N,m)`
recursion (no `A_k` factorization), `k=1,...,9`, `r=0,...,9`,
`b in {0,1,2,5,8}`: `405` checks; against the closed sum-form
`S_{2k-1}(N,m)=sum_{i=0}^m (N-2i)^{2k-1} C(N,i)` (a fourth, independent
definition), `k=1,...,8`, `r=0,...,9`, `b in {0,1,3,7}`: `288` checks;
against the two concrete base cases `H_1=1`, `H_3=(b+1)^2+4r`,
`r=0,...,14`, `b=0,...,5`: `180` checks; and the degree bound (§4).
**`odd_part.py` self-test total: `1190` checks, `0` fails** (post-fix).

### 2.4 Assembly (`assemble.py`)

The full assembly formula, exactly as given in the task mandate / the
target document's §1:

```
N := 2r+b+1, beta := b+1
D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                - sum_{k=1}^p o_k H_{2k-1}(r,b) / 2^(2k-1)
```

with `Q_p(-(v+beta/2))=E_p(v)+O_p(v)` (even/odd split, obtained here by
formally composing the `Q_p(u)` polynomial with the linear map
`u = -(v+beta/2)` and separating coefficients by parity of the power of
`v`), `M_p(N):=sum_l e_{2l} mu_{2l}(N)`, `Phi_b(r):=P_b 2^N`,
`Strip_p(r,b):=sum_{i=1}^b E_p(i-beta/2) w_i(r,b)`,
`w_i(r,b):=r!(r+b)!/[(r+i)!(r+b+1-i)!]`, `H_{2k-1}(r,b):=P_b S_{2k-1}(N,r)`
— implemented directly from §2's ingredients, no sympy anywhere.

**Calibration** against `ground_truth.D_star`, `p=1,...,10`,
`b in {0,1,2,3}`, `r=0,...,29`: **`1200` checks, `0` fails** — the
assembler reproduces every already-PROVED `p<=10` value exactly before
being trusted for the `p=21,...,40` sweep.

---

## 3. Direct spot-check of the target document's OWN printed output

The target document prints, in full, its `p=21,b=0` closed form (§3.4 of
its `ATTEMPT.md`) as `coef(r)*varphi_r + rem(r)`, two degree-`~20`
polynomials with large rational coefficients. This referee **hand-
transcribed both polynomials verbatim** from the document's text into
`spotcheck_printed_p21_b0.py` and evaluated the resulting closed form
exactly at `r=21,25,50,100,150`, comparing against this referee's own
`ground_truth.D_star(21,r,0)`:

**`5/5` exact matches, `0` mismatches** (`spotcheck_printed_p21_b0.log`)
— a direct confirmation that the specific large-coefficient formula the
target document actually printed for `p=21,b=0` is correct, not merely
that this referee's own independent implementation agrees with itself.

`b=1` was not separately hand-transcribed (no full `b=1` closed form is
printed verbatim in the document's prose to transcribe against), but is
covered far more thoroughly by the main exhaustive sweep (§4 below),
which includes `b=1` at every `p=21,...,40` across `151` values of `r`.

---

## 4. Main exhaustive sweep — scale reached, and why it differs from the
document's claim

**The document claims** `r<=200, b<=30`, uniformly across `p=21,...,40`
(`124,620` checks, `372.2s`). **This referee's exhaustive sweep reached
`r=0,...,150`, `b=0,...,25`** (a `151x26=3926`-point grid per `p`,
`20` values of `p`) — smaller than the document's claim in both `r` and
`b`. This reduction was made explicitly for this referee's own practical
compute-time budget (this referee's independently-built `Assembler` is
slower per point than the document's own fast/interpolation-based
routes, since it recomputes the `a_k^{(d)}` recursion and the `E_p`/`H_k`
evaluations from scratch at every grid point with no caching across `r`)
and is disclosed here rather than silently matched to the document's own
numbers.

```
referee main sweep: p=21..40, r=0..150, b=0..25
p=21: checks=3926 fails=0 time=14.39s
p=22: checks=3926 fails=0 time=14.51s
p=23: checks=3926 fails=0 time=15.31s
p=24: checks=3926 fails=0 time=16.38s
p=25: checks=3926 fails=0 time=17.44s
p=26: checks=3926 fails=0 time=18.86s
p=27: checks=3926 fails=0 time=19.54s
p=28: checks=3926 fails=0 time=20.02s
p=29: checks=3926 fails=0 time=21.44s
p=30: checks=3926 fails=0 time=22.03s
p=31: checks=3926 fails=0 time=24.20s
p=32: checks=3926 fails=0 time=24.16s
p=33: checks=3926 fails=0 time=26.12s
p=34: checks=3926 fails=0 time=27.20s
p=35: checks=3926 fails=0 time=26.78s
p=36: checks=3926 fails=0 time=28.07s
p=37: checks=3926 fails=0 time=29.97s
p=38: checks=3926 fails=0 time=31.50s
p=39: checks=3926 fails=0 time=32.56s
p=40: checks=3926 fails=0 time=33.25s
TOTAL: checks=78520 fails=0 wallclock=463.75s
```

**`78,520` checks, `0` fails, `463.75s` wallclock** (`sweep_main.py` /
`sweep_main.log`), covering **every one of the twenty new `p` values at
the identical reduced grid**, uniformly — `r<p` (Corollary A3's
empty-sum boundary) included throughout (`r` starts at `0`).

**To partially close the gap to the document's claimed `r<=200,b<=30`**,
this referee ran three supplementary, targeted checks reaching further
in specific directions than the main grid (§§4.1-4.3), rather than
extending the exhaustive grid itself (which would have cost roughly
`3-4x` longer, an impractical addition to this referee's own compute
budget for this task):

### 4.1 Randomized stress test (this referee's reserved seed `20260871000`)

```
[beyond-main-sweep p in 21..40] seed=20260871000 n=300 p in [21,40] r<= 300 b<= 40: 300 checks, 0 fails, 9.1s
[reduced-scale-region p in 41..60] seed=20260871000 n=200 p in [41,60] r<= 100 b<= 20: 200 checks, 0 fails, 18.7s
TOTAL random_spotcheck: 500 checks, 0 fails
```

`500` random `(p,r,b)` triples, `0` fails, reaching `r<=300` (beyond both
this referee's own `150` and the document's own claimed `200`) and
`b<=40` (beyond both this referee's own `25` and the document's own
claimed `30`), for `p` in `[21,60]` — i.e. exactly the region the main
exhaustive grid does not cover, sampled instead of swept
(`random_spotcheck.py` / `random_spotcheck.log`).

### 4.2 Structural / boundary checks (`extra_checks.py`)

```
(1) Q_p(-1)=0 for p=1..60: 60 checks, 0 fails
(2) degree bound k=1..45, b in (0, 1, 3, 7, 30): 225 checks, 0 fails
(3) Strip_p(r,1) vanishing (E_p(0)=Q_p(-1)) p=21..40: 20 checks, 0 fails
(4) r<p region forced to zero by the FULL formula (not a shortcut), p in (21, 25, 30, 35, 40), b in (0, 1, 2, 5): 604 checks, 0 fails
(5) p=41..60 deterministic targeted spot-check: 500 checks, 0 fails, 13.6s
TOTAL extra_checks: 1409 checks, 0 fails
```

Item (4) is a specific check this referee added beyond the task's
explicit list: it confirms the `r<p` vanishing boundary is not merely a
hard-coded early return in `assemble.py` (which it is, for speed — see
`Assembler.D_star`'s first line) but is *also* forced by the **full**
assembly formula's own algebra when the shortcut is bypassed
(`604` checks across five `p` values and four `b` values, all
identically zero via the full `Phi_b*M_p - Strip - odd_sum` computation)
— directly confirming the document's own claim ("the assembled formula's
own algebra forces this... not a separately-coded special case").

### 4.3 Grand total across all checks in this report

`1920 + 1368 + 1190 + 1200 + 5 + 1409 + 500 + 78520 = ` **`86,112` exact
checks, `0` mismatches**, across every script in this directory.

---

## 5. This referee's own bug, disclosed (required by the task mandate)

See §2.3 above for the full account. **Summary:** an early version of
`odd_part.py`'s `a_k_table` function omitted the factor of `2` in front
of the recursive sum in the `a_k^{(d)}(r)` recursion (`... + comb(...)*a(...)`
instead of `... + 2*comb(...)*a(...)`). This produced a systematic
`2^{k-1}`-factor error in every `H_{2k-1}(r,b)` value for `k>=2`,
undetectable by the brute-force cross-checks at small `k` alone by
coincidence for `k=1` (where the missing factor is vacuous, since the
sum is over an empty range) but caught immediately and unambiguously by
the degree-bound self-test at `k>=2` (`811/1190` checks failed, with a
clean, diagnostic `2^{k-1}` ratio between measured and expected leading
coefficients). Fixed by adding the missing `2*`; every result in this
report post-dates the fix. This bug never affected any check reported
as passing in §§3-4 above (all of which were run against the corrected
`odd_part.py`).

---

## 6. Assessment of the target document's own two self-disclosed bugs

Per the task mandate, this referee could not read the target's own
`ingredients.py`/`odd_part.py` to audit the fix directly (that is
explicitly barred by the no-predecessor-script-reading discipline), so
the two disclosures were assessed for **internal mathematical
consistency and plausibility** by independently reproducing the
*described mechanism* of each bug from scratch.

### 6.1 The Faulhaber power-sum off-by-one (§5.1 of the target's `ATTEMPT.md`)

The target claims that applying the classical Faulhaber formula
`(1/(i+1)) sum_j C(i+1,j) B_j u^{i+1-j}` (with `B_1=-1/2`) directly at
`n=u` computes `sum_{k=0}^{u-1} k^i`, not `sum_{k=1}^u k^i` — an
off-by-one — and that the fix is to evaluate at `n=u+1` instead, plus a
special-cased `-1` correction at `i=0`.

**This referee independently implemented exactly this classical formula**
(own from-scratch Bernoulli-number recurrence, `B_1=-1/2` convention,
verified `B_1=-1/2` explicitly) and confirmed, for `i=1,...,9`,
`u=1,...,9` (`81` points, all mismatching as claimed):

```
i=3,u=5: buggy(naive S_i(u))=100, true P_i(u)=225, P_i(u-1)=100, buggy==P_i(u-1)? True
fixed S_i(u+1)=225, true P_i(u)=225, match=True
```

— i.e. the naive application produces **exactly** `P_i(u-1)` (matching
the target's own diagnostic description, "`got(u)=want(u-1)`"), and the
described fix (`n=u+1`) restores the correct value exactly. The `i=0`
special case was also independently confirmed: even after the general
fix, `S_0(u+1) = u+1`, one more than the true `P_0(u)=u`, exactly the
"spurious `k=0` term" the target names and special-cases. **Both parts
of the disclosed bug narrative are independently reproduced,
mathematically exact, and the disclosed fix is verified correct** — the
disclosure is plausible and, as claimed, immaterial to any downstream
result once fixed.

### 6.2 The `odd_part.py` self-test indexing slip (§5.2 of the target's `ATTEMPT.md`)

The target claims an early self-test compared `H[3]` (representing
`H_5` in its `k`-indexed dict) against the printed formula for `H_3`
(which is `H[2]`), producing large, obviously-wrong mismatches for
`b>=2`. This referee's own `H_odd_fast` table (§2.3) directly confirms
`H_3` and `H_5` are substantially different in magnitude at concrete
points:

```
r=5,b=2:  H_3 (=H[2]) = 29,    H_5 (=H[3]) = 1401   -- ratio=48.3
r=10,b=3: H_3 (=H[2]) = 56,    H_5 (=H[3]) = 5216   -- ratio=93.1
```

confirming that comparing `H_5`'s value against `H_3`'s printed formula
would indeed produce large, immediately-visible mismatches, exactly as
described — a plausible, low-risk, test-only bug whose described fix
(index `H[2]`, not `H[3]`) is the obviously correct one given the
document's own `k`-indexing convention (`H[k]` represents `H_{2k-1}`).
This referee has no way to audit that the fix was *actually applied
everywhere* in the target's own code (barred from reading it), but the
narrative is internally consistent with the document's own final
reported numbers (its `odd_part.py` self-test total, `1176` checks,
`0` mismatches, is of the same order as this referee's own equivalent
self-test, `1190` checks, and includes a `k=1,...,9` brute-force cross-
check block the document says passed both before and after the fix,
which is the load-bearing claim for "not a bug in the machine itself").

---

## 7. "No new mathematical ingredient" claim — verified

The task mandate asks this referee to confirm every non-trivial fact the
target document uses really is cited from an already-integrated,
already-referee-approved source, not newly asserted. Cross-checked
directly against `THEOREM.md` and the two predecessor documents read in
full (§1 above):

- **Corollary A3** (the defining sum) — stated in `THEOREM.md` "Estágio
  9" / `all_orders_closed_form_attempt/ATTEMPT.md` §4.3, PROVED there.
  The target document reproduces it verbatim, unchanged (its §1) — no
  new claim.
- **The assembly formula itself** (`N,beta,Phi_b,M_p,Strip_p,H_{2k-1}`
  and their combination) — first proved and executed in
  `general_p_dstar_closure_attempt/ATTEMPT.md` (wave 15, `p=1..10`,
  referee-approved), reproduced verbatim by
  `general_p_dstar_extension_attempt/ATTEMPT.md` (wave 16, `p=11..20`,
  referee-approved `DISC-DEC-070`), and reproduced verbatim again by the
  target document (its §1 states "This front changes nothing about the
  above"). Confirmed unchanged across all three documents by direct
  textual comparison.
- **`H_k(r,b)` correctness for every `k`** — proved by the wave-15
  referee's induction (cited in `THEOREM.md` "Estágio 16" and in the
  wave-16 predecessor's own §0/§2.2), used by the target as cited input,
  not re-derived. Confirmed: `THEOREM.md`'s "Estágio 16" account states
  this explicitly ("a prova indutiva do referee estabelece que a
  máquina de colapso `I_{2k+1}` subjacente é correta para todo `k`").
- **The `S_{2k-1}=A_k*C(N,m+1)` factorization and the degree bound
  `deg_r H_{2k-1}=k-1`** — proved by the wave-16 referee (its own
  `REFEREE_REPORT.md` §2a-2b, read in full for this report), cited in
  `THEOREM.md` "Estágio 21" ("a cota de grau... agora PROVADA"). The
  target document uses this directly (its §2.3 states it "matches the
  wave-16 referee's independently-stated closed form character-for-
  character" and uses it "as cited input"), while also performing its
  own independent re-derivation from the originally-cited `S_{2k-1}`
  recursion as an *additional* sanity check (not a new mathematical
  claim, since it reproduces the same cited recursion). This referee's
  own `odd_part.py` independently confirms the degree bound out to
  `k=45` (§4.2 item (2)) — matching the wave-16 referee's proof exactly,
  with leading coefficient `4^{k-1}(k-1)!`, `b`-independent, as claimed.

**No step in the target document's mathematical content was found to be
newly asserted without a traceable citation to an already-integrated,
already-referee-approved source.** The document's own claim ("no new
mathematical ingredient is used or claimed anywhere in this document")
is accurate.

---

## 8. Named issues (non-substantive)

1. **Scale gap vs. the document's claim** (§4): this referee's
   exhaustive grid (`r<=150,b<=25`) is smaller than the document's own
   claimed `r<=200,b<=30`. Not a finding against the document — purely
   this referee's own compute-budget choice, disclosed explicitly, with
   supplementary checks (§4.1-4.2) reaching *beyond* the document's own
   claimed scale in `r` (`300` vs `200`) and `b` (`40` vs `30`) at
   randomly/deterministically sampled points rather than exhaustively.
   No mismatch was found at any scale reached by either the exhaustive
   grid or the supplementary checks.
2. **`b=1` printed closed forms were not independently hand-transcribed**
   from the document's prose (only `b=0,p=21` was, §3) — `b=1` coverage
   instead comes from the much larger exhaustive numerical sweep (§4),
   which this referee judges to be at least as strong evidence of
   correctness for that specific `(p,b)` slice, though it does not audit
   the document's own *printed coefficients* at `b=1` the way §3 does at
   `b=0`.
3. **This referee's own missing-factor-of-2 bug** (§5) is disclosed in
   full per the task mandate; it was caught and fixed before any
   reported result depended on it.

Neither item touches the target document's own correctness.

---

## 9. Files, reproducibility

| file | contents | checks | fails |
|---|---|---|---|
| `ground_truth.py` / `.log` | independent Corollary A3 implementation, own Stirling table, calibration | 1920 | 0 |
| `ingredients.py` / `.log` | `Q_p(u)` (Stirling2+hockey-stick route, independent of the target's Bernoulli route), central moments (log/exp power-series recurrence) | 1368 | 0 |
| `odd_part.py` / `.log` | `H_{2k-1}(r,b)` machine via the cited `a_k^{(d)}` recursion; this referee's own missing-factor-of-2 bug found and fixed here | 1190 | 0 (post-fix) |
| `assemble.py` / `.log` | full assembly formula, calibration `p<=10` | 1200 | 0 |
| `spotcheck_printed_p21_b0.py` / `.log` | hand-transcribed spot-check of the document's own printed `p=21,b=0` closed form | 5 | 0 |
| `extra_checks.py` / `.log` | `Q_p(-1)=0` (p=1..60), degree bound (k=1..45), Strip-vanishing structural check, `r<p` full-formula-forced-zero check, `p=41..60` deterministic spot-check | 1409 | 0 |
| `sweep_main.py` / `.log` | main exhaustive sweep, `p=21..40`, `r=0..150`, `b=0..25` | 78520 | 0 |
| `random_spotcheck.py` / `.log` | randomized stress test, seed `20260871000` (this referee's reserved range), `r<=300,b<=40,p<=60` | 500 | 0 |
| `REFEREE_REPORT.md` | this report | — | — |

**Grand total: `86,112` exact checks, `0` mismatches**, plus the
degree-bound proof and factorization lemma cited from the wave-16
referee's report (§7) and independently re-confirmed numerically here to
`k=45`.

Reproduce in order: `python3 ground_truth.py`; `python3 ingredients.py`;
`python3 odd_part.py`; `python3 assemble.py`; `python3 spotcheck_printed_p21_b0.py`;
`python3 extra_checks.py`; `python3 sweep_main.py` (dominant cost, `~8`
minutes); `python3 random_spotcheck.py` (`~30s`). Total well under 15
minutes.

---

## 10. Net verdict

**SOUND — ACCEPT for catalogue.** The general-`p` closed-form assembly
for `D^{*(p)}_r(b)` executes correctly at `p=21,...,40` using no new
mathematical ingredient beyond what waves 15-16 already proved and this
lineage's referees already verified (the assembly formula itself, the
`H_k` correctness-for-every-`k` induction, and the `S_{2k-1}`
factorization / degree bound). Every ingredient was independently
re-derived and re-implemented from scratch by this referee, using
deliberately different constructions where practical (a different
power-sum route for `Q_p`), and cross-checked against an independent
Corollary A3 implementation: `86,112` exact checks, `0` mismatches,
including a full exhaustive sweep of all twenty new `p` values (at a
scale this referee explicitly reduced from the document's own claim for
practical time-budget reasons, disclosed in §4, with supplementary
checks reaching beyond the document's claimed scale in specific
directions) and a direct hand-transcribed spot-check of the document's
own printed `p=21,b=0` output. Both of the document's self-disclosed
bugs were independently reproduced and confirmed plausible and
immaterial. This referee's own single bug (§5) is fully disclosed and
was fixed before it could affect any reported result. No mismatch of any
kind was found anywhere, at any scale reached.

Pure combinatorial mathematics internal to the Tamesis Discovery Lab's
u12-universality research line; no claim of progress on any Millennium
Prize Problem is made anywhere in this report.
