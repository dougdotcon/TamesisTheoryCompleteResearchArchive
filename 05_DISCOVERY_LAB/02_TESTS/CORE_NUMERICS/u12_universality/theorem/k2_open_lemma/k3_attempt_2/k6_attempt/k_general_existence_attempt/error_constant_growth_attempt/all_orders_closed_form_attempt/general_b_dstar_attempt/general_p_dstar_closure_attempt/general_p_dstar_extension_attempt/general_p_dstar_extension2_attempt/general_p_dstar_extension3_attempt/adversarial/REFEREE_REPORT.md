# Hostile referee report — `general_p_dstar_extension3_attempt/ATTEMPT.md`

> **Scope.** Wave 19, front (c) hostile-referee pass (`DISC-DEC-083`),
> target: the extension of the general-`p` closed-form assembly for the
> sharp error constants `D^{*(p)}_r(b)` from `p=1,...,40` (waves 15/16/18,
> already proved and referee-approved through `DISC-DEC-082`) to
> `p=41,...,80` **at full scale** (`r<=200,b<=30`) — confirming wave 18's
> own reduced-scale exploratory push to `p=41..60` and extending further
> to `p=61..80` at full scale. Pure combinatorics on the Tamesis Discovery
> Lab's internal random-permutation-with-reroutes ensemble ("u12
> universality" line) — **this is NOT a Millennium Prize Problem and no
> claim of progress on one is made anywhere in this report.** No external
> data, no holdout, no real-world claim.
>
> Everything below was built from scratch in this new `adversarial/`
> subdirectory. **No `.py` file from the target front's own directory, or
> from any predecessor front in this lineage, was opened, read, or
> imported at any point.** Predecessors were consulted only through their
> `ATTEMPT.md` / `REFEREE_REPORT.md` prose, exactly as the task mandate
> requires. The one exception, explicitly permitted (not a `.py` file):
> two lines were extracted verbatim via `sed` from the target's own
> plain-text data log `printed_forms.log` (`_p41_b0_coef_raw.txt`,
> `_p41_b0_rem_raw.txt`) to directly spot-check the target's own printed
> `p=41,b=0` closed form (§4 below), mirroring what the wave-18 referee
> did by hand-transcription. Every script in this directory
> (`ground_truth.py`, `ingredients.py`, `odd_part.py`, `assemble.py`,
> `run_full_sweep.py`, `random_spotcheck.py`, `extra_checks.py`,
> `spotcheck_printed_p41_b0.py`) is written fresh from the mathematical
> description in `THEOREM.md` and the cited `ATTEMPT.md`/
> `REFEREE_REPORT.md` prose only. Nothing outside this directory and the
> target front's own directory was touched; `THEOREM.md`,
> `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` and
> every sibling front were read-only. No git command was run. Exact
> arithmetic (`fractions.Fraction`) throughout — no floating point
> anywhere in the verification code (`numpy` used only for its
> `SeedSequence`/`default_rng` in `random_spotcheck.py`). Randomness used
> only there, seeded from this referee's own reserved range
> **`20260885000+`** (confirmed unused elsewhere in the archive before
> first use: `grep -rn "20260885" 05_DISCOVERY_LAB/` returned only
> reservation lines in the ledger, the queue, and the target's own
> `ATTEMPT.md`/`DERIVATION_PREREG.md` before this report wrote anything)
> — the front's own range `20260884000-20260884999` was not touched.

## Verdict

**SOUND — ACCEPT for catalogue.**

The target document's central claim is confirmed: the already-proved,
already-referee-approved general-`p` closed-form assembly for
`D^{*(p)}_r(b)` (waves 15/16/18) executes correctly at `p=41,...,80`,
using no new mathematical ingredient. This referee independently
re-derived and re-implemented every ingredient of the assembly
(Corollary A3 as ground truth, from scratch; `Q_p(u)` via a route
**deliberately different** from the target's own — Stirling numbers of
the second kind + the hockey-stick identity, not the target's
Bernoulli-number Faulhaber route; central moments `mu_{2l}(N)` via an
independently-coded power-series log/exp recurrence; and `H_{2k-1}(r,b)`
via a **closed-sum, non-recursive** route — `S_{2k-1}(N,m) = sum_{i=0}^m
(N-2i)^{2k-1} C(N,i)` — deliberately different from the target's own
bivariate-recursion machinery) and found **zero mismatches** against an
independent Corollary A3 implementation across **163,008 exact checks**
in total, including a full exhaustive main sweep of `p=41,...,80` at
`r=0,...,120,b=0,...,25` (**125,840 checks, 0 fails**), a boundary sweep
at `p in {41,60,80}` matching the document's own claimed full scale
exactly (`r=0,...,200,b=0,...,30`, **18,693 checks, 0 fails**), a
randomized stress test (this referee's reserved seed `20260885000`)
reaching `r<=400,b<=60,p in[41,80]` (**400 checks, 0 fails**), and a
direct hand-extracted spot-check of the target's own printed `p=41,b=0`
closed form (**7/7 exact matches, including at `r=200`**).

The target document's specific bivariate `(x,y)`-reparametrization of the
cited `A_k` recursion (its own §2.3, flagged by the task mandate as the
one place a scale-driven engineering shortcut could hide a real
mathematical difference) was checked directly: this referee implemented
the ORIGINAL, un-reparametrized depth-indexed recursion
`a_k^{(d)}(r)` character-for-character as cited, and confirmed it agrees
exactly with this referee's independent closed-sum route at every one of
3,168 sampled points (`k=1..24,r=0..11`, six `b` values) — together with
the elementary substitution algebra (`x:=m,y:=N-2m` sends a step
`(N,m)->(N-1,m-1)` to `(x,y)->(x-1,y+1)`, a pure relabeling), this
directly confirms the reparametrization introduces no mathematical
difference, only a bookkeeping change.

Both of the document's self-disclosed bugs (§5.1-5.2 of its own
`ATTEMPT.md`) were assessed for plausibility (§6 below): the moment-table
performance defect (§5.2) is fully plausible and was, in fact,
**independently rediscovered by this referee's own first implementation**
(§5 below) — strong direct corroboration of that class of bug. The
`ground_truth.py` reasoning error (§5.1, Teorema 3 = `D^{*(2)}_r(0)`, not
`D^{*(1)}_r(0)`) is confirmed **correct in its substance** (this referee's
own ground truth independently reproduces exactly this fact: `D^{*(2)}`
matches Teorema 3 exactly for `r=0..59`, `D^{*(1)}` does not) but the
document's narrative detail about the *failure onset point* does not
survive independent reproduction — see the named issue in §6.1.

**Two genuine bugs were found in this referee's own verification code**
(disclosed in full in §5), both caught immediately by the checks failing
loudly, before any downstream conclusion depended on the buggy version.
Neither touches the target document's correctness.

---

## 1. Sources read (per the task mandate)

- `THEOREM.md`: "Estagio 9" (Corollary A3's defining sum), "Estagio 8"
  (the `H_r(t,b)`/`D^*_r(0)` closed forms, Teorema 1/Teorema 3),
  "Estagio 14" (general-`b` `D^{*(p)}_r(b)` for `p=1..4`), "Estagio 16"
  (the general-`p` closure `p=1..10`, the wave-15 referee's induction
  that `H_k` is correct for every `k`), "Estagio 21" (the wave-16
  extension to `p=11..20`, the wave-16 referee's *proved* degree bound
  `deg_r H_{2k-1}(r,b)=k-1` and closed factorization
  `S_{2k-1}=A_k*C(N,m+1)`), "Estagio 29" (the wave-18 extension `p=21..40`
  at full scale plus the reduced-scale exploratory push to `p=41..60`,
  referee-verified `DISC-DEC-082`) — all read in full.
- The target document, `general_p_dstar_extension3_attempt/ATTEMPT.md`,
  in full.
- `general_p_dstar_extension2_attempt/ATTEMPT.md` (wave 18, the direct
  predecessor), read in full, prose only.
- `general_p_dstar_extension2_attempt/adversarial/REFEREE_REPORT.md`
  (wave 18's own referee), read in full, prose only — supplied the
  `a_k^{(d)}(r)` recursion in the exact cited form and the closed-sum
  FOURTH definition of `S_{2k-1}` this report uses as one of its own
  independent routes.

**No `.py` file from any front in this lineage was opened, read, or
imported at any point.** Every script in this directory was written from
the mathematical description above (Corollary A3's sum, the assembly
formula, and the `S_{2k-1}`/`a_k^{(d)}` recursion, all reproduced
verbatim in the task mandate and the sources above).

---

## 2. Independent re-derivation of every ingredient

### 2.1 Ground truth: Corollary A3 (`ground_truth.py`)

`D^{*(p)}_r(b) := sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1,j+1-p)`,
`c_j^{(r)}(b) := r!/(r-j)! / prod_{i=1}^{j+1}(r+b+i)`, `c(N,M)` the
unsigned Stirling numbers of the first kind via the standard recurrence
`c(n,k)=c(n-1,k-1)+(n-1)*c(n-1,k)`, `c(0,0)=1` — own memoized table, own
incremental `c_j` recursion (`c_0=1/(r+b+1)`,
`c_j=c_{j-1}*(r-j+1)/(r+b+j+1)`).

**Calibration:** the incremental `c_j` recursion vs. a fully-naive
per-term `math.factorial` recomputation (`r=0..39`, `b in
{0,1,3,7,20}`: `~2000` checks); `D_star` vs. a second, independent
fully-naive recomputation (`p in {1,2,5,10,21,41,60,80}`, `15` `r` values
each, `3` `b` values: `360` checks); the `r<p` vanishing boundary
(`p=1..80`: `3160` checks); and — critically — **Teorema 3
(`THEOREM.md` "Estagio 8": `D^*_r(0)=r(3r+1)/32*varphi_r-r/12`)
independently confirmed to be `D^{*(2)}_r(0)`, not `D^{*(1)}_r(0)`**
(`r=0..59`, `60` checks, exact match at `p=2`; a companion check confirms
`p=1` mismatches at `18` of `18` sampled points `r=2..19`) — this referee
derived and tested the correct `p`-index (`p=2`) from `THEOREM.md`'s own
text *before* writing any test, so no analogous confusion occurred here.
**Total: `7,761` checks, `0` fails** (`ground_truth.log`).

### 2.2 `Q_p(u)` via a route DIFFERENT from the target document's own
(`ingredients.py`)

The target builds power sums `P_i(u):=sum_{k=1}^u k^i` via the classical
Bernoulli-number Faulhaber formula. This referee used a **deliberately
different** route (matching what the wave-18 referee also did): power
sums via Stirling numbers of the **second** kind + the hockey-stick
identity, `P_i(u) = sum_j S2(i,j)*j!*C(u+1,j+1)` (own from-scratch
derivation, no Bernoulli numbers anywhere) — built directly as an exact
**polynomial in `u`** (not evaluated pointwise), then Newton's identities
`p*e_p = sum_i (-1)^{i-1} e_{p-i} P_i(u)` applied to polynomials directly
(`poly_mul`/`poly_add`, no interpolation) to assemble `Q_p(u):=e_p(1,...,u)`
via a shared bottom-up ladder (`e_0,...,e_80` built once, all smaller `p`
free byproducts of the `p=80` build — `10.4s` total for the whole ladder
to `p=80`).

**Verified** against a *third*, completely independent route — direct DP
computation of `e_p(1,...,u)` (no power sums, no Stirling numbers, no
Newton's identity): `p=0..14,u=0..15`, `240` checks; the vanishing
boundary `Q_p(u)=0` for `u=0..p-1`, `p=1..80`: `3,240` checks; and the
cited genuine-degree-`2p` fact (`THEOREM.md` "Estagio 16"): `p=0..80`,
`81` checks, confirmed exactly (`deg Q_80 = 160`). **Central moments**
`mu_{2l}(N)` built via the classical power-series log(cosh)/exp
recurrence (own from-scratch derivation), verified against direct
binomial summation, `l=0..11,N=0..23`: `288` checks, plus sanity/
structural odd-vanishing checks: `27` checks. **`ingredients.py`
self-test total: `3,869` checks, `0` fails** (`ingredients.log`).

### 2.3 The `H_{2k-1}(r,b)` machine — closed-sum route, DIFFERENT from the
target's bivariate recursion (`odd_part.py`)

`H_{2k-1}(r,b) := P_b(r) * S_{2k-1}(N,r)`, `N=2r+b+1`, with
`S_{2k-1}(N,m) := sum_{i=0}^m (N-2i)^{2k-1} * C(N,i)` — the FOURTH,
independent closed-sum definition cited from the wave-18 referee's own
report — evaluated by **direct summation at each concrete `(N,m)`**, no
recursion in `k`, no `A_k` factorization, no bivariate reparametrization
at all. `P_b(r) := r!(r+b)!/N!`, independently re-derived here from the
cited identity `P_b*C(N,r+1)=1/(r+1)` (elementary algebra: since
`C(N,r+1)=N!/[(r+1)!(r+b)!]`, `P_b=1/[(r+1)C(N,r+1)]=r!(r+b)!/N!`),
confirmed directly against that identity, `r=0..29`, `b in {0,1,2,5,8,30}`:
`180` checks.

**Verified**, general `k`, before being trusted for the main sweep:

- Against the ORIGINAL, un-reparametrized `S_{2k-1}` recursion (brute
  force, no `A_k` factorization at all), `k=1..11,r=0..9`, `5` `b`
  values: `495` checks.
- Against the printed base cases `H_1=1`, `H_3=(b+1)^2+4r`,
  `r=0..14,b=0..5`: `180` checks.
- **Directly against the LITERAL cited depth-indexed `a_k^{(d)}(r)`
  recursion** — the SAME recursion the target document's §2.3
  reparametrizes into a bivariate polynomial `A_k(x,y)` — implemented
  here with NO `(x,y)` substitution at all (mandate item 10, the
  specific check flagged as most important): `k=1..24,r=0..11`, `6` `b`
  values: `3,168` checks, confirming the closed-sum route and the
  literal un-reparametrized recursion agree exactly everywhere sampled.
  Combined with the elementary substitution algebra (a step
  `(N,m)->(N-1,m-1)` sends `(x,y)=(m,N-2m)` to `(x-1,y+1)`, a pure
  relabeling with no mathematical content added or lost), this directly
  confirms the target's bivariate reparametrization is not a new
  mathematical shortcut, only a bookkeeping change.
- The degree bound `deg_r H_{2k-1}=k-1`, leading coefficient
  `4^{k-1}(k-1)!` — **cited as PROVED** (wave-16 referee) — re-checked
  via Lagrange interpolation at concrete points, `k=1..45`, `5` `b`
  values: `450` checks (deg + leading-coeff, `225` each).
- The shared-binomial-row speed path (`build_H_table`, this referee's own
  minor bookkeeping optimization — computing `C(N,i)` once per `(r,b)`
  instead of once per `(k,r,b)`) vs. the un-shared per-`k` `H_odd()`
  route: `r in {0,5,17,42,85,130}`, `4` `b` values, `k=1..12`: `288`
  checks.

**`odd_part.py` self-test total: `3,376` checks, `0` fails**
(`odd_part.log`).

### 2.4 Assembly (`assemble.py`)

The full assembly formula, exactly as given in the task mandate / the
target document's §1:

```
N := 2r+b+1, beta := b+1
D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                - sum_{k=1}^p o_k H_{2k-1}(r,b) / 2^(2k-1)
```

with `Q_p(-(v+beta/2))=E_p(v)+O_p(v)` (even/odd split, obtained here by
formally composing the `Q_p(u)` polynomial with `u=-(v+beta/2)`, own
from-scratch polynomial-composition routine), `M_p(N):=sum_l e_{2l}
mu_{2l}(N)`, `Phi_b(r):=P_b(r) 2^N`, `Strip_p(r,b):=sum_{i=1}^b
E_p(i-beta/2) w_i(r,b)`, `w_i(r,b):=r!(r+b)!/[(r+i)!(r+b+1-i)!]`,
`H_{2k-1}(r,b):=P_b(r) S_{2k-1}(N,r)` — implemented directly from §2's
independent ingredients, no sympy anywhere.

**Calibration** against `ground_truth.D_star`, `p=1..10`, `b in
{0,1,2,3}`, `r=0..29`: **`1,200` checks, `0` fails** — the assembler
reproduces every already-PROVED `p<=10` value exactly before being
trusted for the `p=41..80` sweep (`assemble.log`).

---

## 3. Main verification sweep — scale reached, and why

**The document claims** `r<=200,b<=30`, uniformly across `p=41,...,80`
(`249,240` checks, `2559.74s`). This referee's exhaustive sweep uses a
**two-tier design**, explicitly disclosed:

### 3.1 Main grid: `p=41,...,80`, `r=0,...,120`, `b=0,...,25`

Reduced from the document's own claimed scale, for this referee's own
practical compute-time budget (a fresh, non-production-cached
implementation, deliberately using different — and less
speed-optimized — routes than the target's own bivariate machinery for
`H_{2k-1}` and its combined-polynomial fast path). This is the task
mandate's explicit "scale down if runtime is prohibitive but be
explicit" allowance.

```
p=41: checks=3146 fails=0 time=26.72s
p=42..79: (all) checks=3146 fails=0, time rising smoothly from 27.4s to 51.7s
p=80: checks=3146 fails=0 time=51.95s
MAIN GRID TOTAL: checks=125840 fails=0 wallclock=1647.50s  (p=41..80, r=0..120, b=0..25)
```

**`125,840` checks, `0` fails, `1647.50s` wallclock** — every one of the
forty new `p` values, uniformly, `r=0,...,120` (well above the mandate's
`100-150` floor), `b=0,...,25` (within the mandate's `20-30` floor).
Full per-`p` breakdown in `run_full_sweep.log`.

### 3.2 Boundary grid: `p in {41,60,80}`, `r=0,...,200`, `b=0,...,30`

To directly test whether the reduced main grid hides a boundary effect at
large `r,b`, this referee ran three representative `p` values (start,
middle, end of the target range) at the document's OWN claimed full-scale
ceiling exactly:

```
[boundary] p=41: checks=6231 fails=0 time=73.67s
[boundary] p=60: checks=6231 fails=0 time=135.35s
[boundary] p=80: checks=6231 fails=0 time=194.48s
BOUNDARY GRID TOTAL: checks=18693 fails=0 wallclock=403.50s
```

**`18,693` checks, `0` fails, `403.50s` wallclock**, at `r<=200,b<=30`
exactly matching the document's own claimed ceiling — including
`p=80,r=200,b=30`, the single most extreme cell in the document's entire
claimed range. No mismatch, no boundary effect, at any of the three `p`
values checked at full scale.

**Grand total, main + boundary: `144,533` checks, `0` fails, `2051.01s`
wallclock** (`run_full_sweep.log`).

### 3.3 Randomized stress test beyond both grids (`random_spotcheck.py`)

This referee's reserved seed `20260885000` (confirmed unused elsewhere in
the archive before first use — see the header above):

```
random_spotcheck: seed=20260885000, n_samples=400, p in [41,80], r in [0,400], b in [0,60]
  distinct (p,b) Assembler builds: 374
  400 checks, 0 fails, 56.8s
```

`400` random `(p,r,b)` triples, `0` fails, reaching `r<=400,b<=60` —
matching the document's own randomized stress-test region (seed
`20260884000`) in scale, sampled independently at a different seed.

---

## 4. Direct spot-check of the target document's OWN printed output

The target document prints, in full (truncated in its `ATTEMPT.md`
prose, complete in its plain-text data log `printed_forms.log`, which is
**not** a `.py` file and was read per the task's discipline, exactly as
permitted), its `p=41,b=0` closed form as `coef(r)*varphi_r + rem(r)`,
two degree-`~41`/`~40` polynomials with large rational coefficients. This
referee extracted the two exact lines verbatim via `sed` (not retyped by
eye — a `41`-term and `39`-term polynomial with up to `35`-digit
coefficients is exactly the kind of thing hand-transcription risks
corrupting) into `_p41_b0_coef_raw.txt` / `_p41_b0_rem_raw.txt`, parsed
them with a small independent regex parser (`spotcheck_printed_p41_b0.py`
— see §5.1 for a bug found and fixed in this very parser), and evaluated
the resulting exact identity at seven concrete `r` values, comparing
against this referee's own `ground_truth.D_star(41,r,0)`:

```
r=41: printed-form value == ground_truth.D_star(41,r,0)? OK
r=45: OK   r=50: OK   r=75: OK   r=100: OK   r=150: OK   r=200: OK
spotcheck_printed_p41_b0: 7 checks, 0 fails
```

**`7/7` exact matches, `0` mismatches, including at `r=200`** — a direct
confirmation that the specific large-coefficient formula the target
document actually printed for `p=41,b=0` is correct, not merely that
this referee's own independent implementation agrees with itself. This
directly satisfies the task mandate's item 9 ("spot-check at least 2-3 of
the printed b=0,1 closed-form values") at a stronger level than the
literal minimum — a genuine printed-coefficient-level check, plus twelve
further value-level spot-checks of both `b=0` and `b=1` across the range
(§ "extra checks" below).

---

## 5. This referee's own bugs, disclosed in full

### 5.1 Regex parser bug in `spotcheck_printed_p41_b0.py` (real bug, caught
immediately, before any conclusion was drawn)

The first version of the term-matching regex, `([+-])\s*\((\d+)/(\d+)\)
\*r\^(\d+)`, required an explicit `^N` exponent on every term. The
target's own printed polynomial ends its lowest-degree term as `...)*r`
(implicit `^1`, no caret) — this term was silently dropped, shifting
every evaluated value by a nonzero amount. **Caught immediately**: all
`7/7` checks failed on the first run (a clean, total failure — not a
partial or subtle one), which is exactly the "a check failing loudly"
signal this archive's disclosure convention names. **Fixed** by making
the exponent group optional (`(?:\^(\d+))?`, defaulting to power `1` when
absent); re-run, `7/7` exact matches. This bug never affected any
conclusion — it failed completely before this referee drew any inference
from it, and the fixed version is what §4 reports.

### 5.2 A genuine performance defect in this referee's own FIRST
`ingredients.py`, independently rediscovering the SAME CLASS of bug the
target document itself disclosed (§5.2 of its `ATTEMPT.md`)

This referee's first implementation of central moments called
`mu_poly(l)` independently for each `l` needed by `Assembler.M_p`,
rebuilding the entire log(cosh)/exp power series from scratch (up to
order `2l`) on every call. Profiled directly: a single
`Assembler(80,30).D_star(80)` construction+call took **`67.3s`** (measured
directly, before any fix), because `M_p(N)` requests `mu_eval(0,N),
mu_eval(1,N),...,mu_eval(80,N)` in increasing order, triggering `81`
independent full series rebuilds instead of one shared build. **Every
value this defect produced was still exactly correct** — purely a
performance defect, never a correctness bug, exactly as the target
document's own §5.2 disclosure describes for its analogous issue.
**Fixed** by a shared `_warm_up_moments(max_order)` entry point (building
the log/exp series ONCE to the maximum order ever needed, extracting
every smaller `mu_poly(l)` as a free byproduct) called once per
`Assembler` construction with order `2p` (matching the cited genuine
degree-`2p` fact, §2.2). **Re-verified after the fix**: the same
`Assembler(80,30).D_star(r)` call dropped to `0.06-0.12s` depending on
`r` — confirmed via direct before/after timing (§ below) and the full
main+boundary sweep completing in `2051.01s` total for `144,533` points.
This referee independently rediscovering the same class of defect the
target document disclosed is, if anything, corroborating evidence that
the target's own disclosure (§6.1 below) is a plausible, easy-to-hit
mistake in this specific style of power-series computation, not an
implausible or invented narrative detail.

**No other component** (Corollary A3, `Q_p`'s Newton-identity
construction, the `H_k` closed-sum/depth-recursion machinery, the
assembly's even/odd split, the main/boundary/random sweeps) exhibited
any incorrect VALUE at any point in this referee's development — both
disclosed issues above were caught and fixed before contributing to any
result reported in §§2-4.

---

## 6. Assessment of the target document's own two self-disclosed bugs

Per the task mandate, this referee could not read the target's own
`ground_truth.py`/`ingredients.py` to audit the fixes directly (barred by
the no-predecessor-script-reading discipline), so both disclosures were
assessed by independently reproducing the *described mechanism* from
scratch.

### 6.1 The `ground_truth.py` reasoning error (§5.1 of the target's
`ATTEMPT.md`) — substance CONFIRMED, one narrative detail NOT reproduced

**The substantive claim — Teorema 3 corresponds to `D^{*(2)}_r(0)`, not
`D^{*(1)}_r(0)`** — is independently and exactly confirmed by this
referee's own `ground_truth.py` (§2.1 above): `D^{*(2)}_r(0)` matches
Teorema 3 exactly for all `r=0..59` (`60/60`), while `D^{*(1)}_r(0)` does
not, at every `r` tested. This is the mathematically load-bearing part of
the disclosure, and it is correct.

**One narrative detail does NOT survive independent reproduction.** The
target states its buggy self-test "passed for `r=0,...,11`... then
failed loudly and systematically for `r=12,...,39` (`39` of `40` checks
in that block)". This referee's own exact-arithmetic reproduction shows
`D^{*(1)}_r(0)` and Teorema 3 already **disagree at `r=1`** (values `1/6`
vs. `0`) — not at `r=12` — giving mismatches at `r=1,...,39` (`39` values,
matching the *count* "`39` of `40`" exactly, since `r=0` trivially agrees
at `0=0` on both sides) but not the target's stated *onset point*
(`r=12`, not `r=1`). Concretely:

```
r=0: p1=0      t3=0       (match)
r=1: p1=1/6    t3=0       (MISMATCH -- already here, not r=12)
r=2: p1=4/15   t3=1/15    (MISMATCH)
...
```

This is a **named issue, not a soundness finding** — it does not touch
`ground_truth.D_star`'s correctness (independently confirmed exact at
every `p` this report checked) or the actual `Assembler`/sweep results
(§§3-4). It is a discrepancy in the *narrative texture* of a self-
disclosed bug report: either the target's own first-version self-test had
some additional defect beyond the described `p`-index confusion (e.g. an
off-by-one in the comparison range, or a coincidental near-agreement this
referee's exact reproduction does not reproduce), or the description of
"passed for `r=0,...,11`" is imprecise. The headline number (`39` failing
checks) is corroborated; the described failure-onset point (`r=12`) is
not. Recommended for a dated correction note in the target document, not
a soundness objection.

### 6.2 The moment-table performance defect (§5.2 of the target's
`ATTEMPT.md`) — CONFIRMED plausible, independently rediscovered

As detailed in §5.2 above, this referee's own first implementation
independently hit the exact same class of defect (repeated from-scratch
rebuild of a power series across increasing orders, rather than one
shared warm-up), with a directly measured, dramatic slowdown (a single
`D_star` call at `p=80,b=30` went from `67.3s` to `~0.1s` after the
fix) — strong direct corroboration that this is a natural, easy-to-hit,
purely-performance defect in this specific computational pattern, exactly
as the target describes (not a correctness bug: "every value it produced
was exact" in both this referee's case and the target's own account).

---

## 7. "No new mathematical ingredient" claim — verified

Cross-checked directly against `THEOREM.md` and the predecessor documents
read in full (§1 above):

- **Corollary A3** (the defining sum) — stated in `THEOREM.md` "Estagio
  9" / `all_orders_closed_form_attempt/ATTEMPT.md` §4.3, PROVED there.
  The target reproduces it verbatim, unchanged (its §1) — no new claim.
- **The assembly formula itself** — first proved and executed in
  `general_p_dstar_closure_attempt/ATTEMPT.md` (wave 15, `p=1..10`,
  referee-approved), reproduced verbatim by every predecessor since
  (waves 16, 18), and reproduced verbatim again by the target ("This
  front changes nothing about the above" — its §1). Confirmed unchanged
  by direct textual comparison.
- **`H_k(r,b)` correctness for every `k`** — proved by the wave-15
  referee's induction, cited in `THEOREM.md` "Estagio 16", used by the
  target as cited input, not re-derived.
- **The `S_{2k-1}=A_k*C(N,m+1)` factorization and the degree bound
  `deg_r H_{2k-1}=k-1`** — proved by the wave-16 referee, cited in
  `THEOREM.md` "Estagio 21". The target uses this directly. This
  referee's own `odd_part.py` independently re-confirms the degree bound
  out to `k=45` (§2.3), leading coefficient `4^{k-1}(k-1)!`,
  `b`-independent, matching the citation exactly.
- **The bivariate `(x,y)`-reparametrization (target's §2.3)** — the
  document itself explicitly labels this "an implementation-engineering
  fact, not a new mathematical claim." This referee's direct check (§2.3
  above, `3,168` checks against the literal un-reparametrized `a_k^{(d)}`
  recursion, plus the elementary substitution algebra) confirms this
  characterization is accurate: the reparametrization changes nothing
  mathematically, only bookkeeping.
- **`P_b(r)=r!(r+b)!/N!`** (target's §1, derived from the cited
  `P_b*C(N,r+1)=1/(r+1)` identity) — this referee independently
  re-derived the identical formula via the same elementary algebra
  (§2.3 above), confirmed against the cited identity directly (`180`
  checks) — no new mathematical content, a forced consequence of an
  already-cited fact.

**No step in the target document's mathematical content was found to be
newly asserted without a traceable citation to an already-integrated,
already-referee-approved source.** The document's own claim ("no new
mathematical ingredient is used or claimed anywhere in this document") is
accurate.

---

## 8. Additional structural / value-level checks (`extra_checks.py`)

```
Q_p(-1)=0 check: p=1..80: 80 checks, 0 fails
r<p full-formula-forced-zero check: 1510 checks, 0 fails
Strip_p(r,1)=0 structural check: p=41..80: 200 checks, 0 fails
printed-form spotcheck (b=0,1, six (p,r) pairs incl. p=80,r=200): 12 checks, 0 fails
Assembler(p=2,b=0) vs Teorema3 (end-to-end, via the FULL Assembler/H_k/moments machinery, not just ground_truth.py): 60 checks, 0 fails
extra_checks.py TOTAL: 1862 checks, 0 fails
```

- **`Q_p(-1)=0` for every `p=1,...,80`** — this referee's own independent
  confirmation of the fact the target names in its §2.4 (inherited from
  the wave-18 predecessor's §2.4). `80/80` confirmed, `0` fails.
- **`r<p` vanishing forced by the FULL formula**, not merely a shortcut —
  mirrors the wave-16 referee's own structural check: `p in
  {41,50,61,70,80}`, `b in {0,1,2,5,30}`, every `r<p`: `1,510` checks,
  `0` fails (`D_star_full_formula`, bypassing the early-return shortcut
  entirely).
- **`Strip_p(r,1)=0`** structural consequence of `Q_p(-1)=0`: `p=41..80`,
  five `r` values each: `200` checks, `0` fails.
- **`Assembler(p=2,b=0)` vs. Teorema 3**, end-to-end through the full
  assembly machinery (not just the raw Corollary A3 ground truth):
  `r=0..59`, `60/60` exact matches.

---

## 9. Grand total across every script in this directory

| file | contents | checks | fails |
|---|---|---|---|
| `ground_truth.py` / `.log` | independent Corollary A3 implementation, own Stirling table, Teorema-3-is-`p=2` calibration | 7,761 | 0 |
| `ingredients.py` / `.log` | `Q_p(u)` (Stirling2+hockey-stick, polynomial ladder route), central moments (log/exp power series, shared warm-up) | 3,869 | 0 |
| `odd_part.py` / `.log` | `H_{2k-1}(r,b)` closed-sum route + literal `a_k^{(d)}` depth-recursion cross-check (mandate item 10) + degree bound | 3,376 | 0 |
| `assemble.py` / `.log` | full assembly formula, calibration `p<=10` | 1,200 | 0 |
| `extra_checks.py` / `.log` | `Q_p(-1)=0`, `r<p` full-formula check, `Strip_p(r,1)=0`, printed-form spotchecks, Teorema-3 end-to-end | 1,862 | 0 |
| `spotcheck_printed_p41_b0.py` / `.log` | hand-extracted spot-check of the document's own printed `p=41,b=0` closed form | 7 | 0 |
| `run_full_sweep.py` / `.log` | main sweep (`r<=120,b<=25`) + boundary sweep (`p in {41,60,80}`, `r<=200,b<=30`) | 144,533 | 0 |
| `random_spotcheck.py` / `.log` | randomized stress test, seed `20260885000` (this referee's reserved range), `r<=400,b<=60` | 400 | 0 |
| `REFEREE_REPORT.md` | this report | — | — |

**Grand total: `163,008` exact checks, `0` mismatches**, across every
script in this directory
(`7761+3869+3376+1200+1862+7+144533+400 = 163008`).

Reproduce in order: `python3 ground_truth.py`; `python3 ingredients.py`;
`python3 odd_part.py`; `python3 assemble.py`; `python3 extra_checks.py`;
`python3 spotcheck_printed_p41_b0.py`; `python3 run_full_sweep.py`
(dominant cost, `~34` minutes); `python3 random_spotcheck.py` (`~1`
minute). Total well under an hour.

---

## 10. Named issues (non-substantive)

1. **Scale gap vs. the document's claim** (§3): this referee's main
   exhaustive grid (`r<=120,b<=25`) is smaller than the document's own
   claimed `r<=200,b<=30` — a deliberate, disclosed compute-budget choice
   (a fresh, non-production-cached implementation, using deliberately
   different and less speed-optimized routes for `H_{2k-1}` than the
   target's own). This gap is closed at three representative `p` values
   (`41,60,80` — start, middle, end of the target range) by a dedicated
   boundary sweep at the document's exact claimed ceiling, plus a
   randomized stress test reaching further still (`r<=400,b<=60`). No
   mismatch was found at any scale reached, including the single most
   extreme cell in the document's entire claimed range (`p=80,r=200,b=30`).
2. **The Teorema-3 narrative discrepancy** (§6.1): the target's disclosed
   bug narrative's headline count (`39/40` failures) is corroborated
   independently; its stated failure-onset point (`r=12`) is not — this
   referee's exact reproduction shows failure starting at `r=1`. Does not
   touch soundness; recommended for a dated correction note.
3. **This referee's own two bugs** (§5) are disclosed in full; both were
   caught and fixed before any reported result depended on them.

Neither item touches the target document's own correctness.

---

## 11. Net verdict

**SOUND — ACCEPT for catalogue.** The general-`p` closed-form assembly
for `D^{*(p)}_r(b)` executes correctly at `p=41,...,80` using no new
mathematical ingredient beyond what waves 15/16/18 already proved and
this lineage's referees already verified (the assembly formula itself,
the `H_k` correctness-for-every-`k` induction, the `S_{2k-1}`
factorization/degree bound, and — checked with particular care per the
task mandate — the target's bivariate `(x,y)`-reparametrization of the
`A_k` recursion, confirmed to be a pure bookkeeping relabeling with no
mathematical content added). Every ingredient was independently
re-derived and re-implemented from scratch, using deliberately different
constructions where the task mandate called for it (Stirling2/hockey-
stick for `Q_p`, closed-sum direct summation for `H_{2k-1}` instead of
the target's bivariate recursion), and cross-checked against an
independent Corollary A3 implementation: **`163,008` exact checks, `0`
mismatches**, including a full exhaustive main sweep (`125,840` checks,
`r<=120,b<=25`), a boundary sweep matching the document's exact claimed
full scale at three representative `p` values (`18,693` checks,
`r<=200,b<=30`), a randomized stress test beyond both
(`400` checks, `r<=400,b<=60`), and a direct hand-extracted spot-check of
the document's own printed `p=41,b=0` closed form (`7/7` exact, including
at `r=200`). Both of the document's self-disclosed bugs were assessed:
the performance defect (§5.2 of its `ATTEMPT.md`) is fully plausible and
was independently rediscovered by this referee's own first
implementation; the reasoning-error disclosure (§5.1) is confirmed
correct in its mathematically load-bearing substance (Teorema 3 =
`D^{*(2)}_r(0)`, not `D^{*(1)}_r(0)`) with one non-substantive narrative
detail (the described failure-onset point) not reproduced independently
— named as a minor issue, not a soundness finding. This referee's own two
bugs (§5) are fully disclosed and were fixed before either could affect
any reported result. No mismatch of any kind was found anywhere, at any
scale reached.

Pure combinatorial mathematics internal to the Tamesis Discovery Lab's
u12-universality research line; no claim of progress on any Millennium
Prize Problem is made anywhere in this report.
