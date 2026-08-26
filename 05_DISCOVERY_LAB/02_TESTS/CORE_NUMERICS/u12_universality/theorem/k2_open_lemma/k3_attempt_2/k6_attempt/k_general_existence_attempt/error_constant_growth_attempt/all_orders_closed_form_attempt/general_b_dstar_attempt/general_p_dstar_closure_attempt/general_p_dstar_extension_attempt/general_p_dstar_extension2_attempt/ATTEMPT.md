# General-`p` closure, extended again: `D^{*(p)}_r(b)` for `p=21,...,40`

> **Governance.** Wave 18, front (a), `GENERAL-P-DSTAR-EXTENSION2-ATTEMPT`,
> authorized by `DISC-DEC-078`. Target: extend the general-`p` closed-form
> assembly for the sharp error constants `D^{*(p)}_r(b)` (already PROVED
> and executed for `p=1,...,10` in wave 15,
> `general_p_dstar_closure_attempt/ATTEMPT.md`, and `p=11,...,20` in wave
> 16, `general_p_dstar_extension_attempt/ATTEMPT.md`, referee-approved
> `DISC-DEC-070`) to `p>20`. Pure combinatorics on the Tamesis Discovery
> Lab's internal random-permutation-with-reroutes ensemble — **this is
> NOT any Millennium Prize Problem and no claim of progress on one is made
> anywhere in this document.** No external data, no holdout, no
> real-world claim. **Nothing outside this directory was created,
> modified, or deleted.** No git commit was made. `THEOREM.md`, the
> decision ledger, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, and every
> sibling attempt's files were not touched. **No `adversarial/`
> subdirectory was created and no referee was dispatched here** — per the
> task's explicit instructions, that is out of scope for this front,
> reserved for the orchestrating session. **This document requires
> independent mandatory adversarial verification before any integration
> into `THEOREM.md` or any other governance artifact**, exactly as every
> predecessor in this lineage required. Every claim below is labelled
> PROVED, CITED, NUMERICALLY VERIFIED, or OPEN.
>
> **Reading discipline honored.** Per the task mandate, `THEOREM.md`
> §§6–9 and "Estágios" 8, 9, 14, 16, 21 were read in full; the wave-15
> `general_p_dstar_closure_attempt/ATTEMPT.md` (the load-bearing citation
> for the `H_k(r,b)` induction) was read in full, and two of its base
> cases (`H_1=1`, `H_3=(b+1)^2+4r`) were independently reproduced as a
> sanity check (§2 below) before anything else was trusted. The direct
> predecessor, `general_p_dstar_extension_attempt/ATTEMPT.md`, was read
> in full (prose only) for methodology, together with its referee report
> (which supplied a strictly stronger, PROVED closed factorization of
> `S_{2k-1}` this front uses directly — see §2). **No `.py` file from any
> predecessor front was opened, read, or imported** — every script in
> this directory is written fresh, from the mathematical description in
> `THEOREM.md` and the cited `ATTEMPT.md` prose only, per the task's
> explicit discipline.

---

## Executive summary (read first)

1. **The mandate's full target is reached and then doubled: `p=21,...,40`
   is closed and verified, at the largest scale used anywhere in this
   lineage, uniformly across all twenty new `p` values.** The mandate
   asked for "at least `p=21..30`, more if computationally tractable." It
   was computationally very tractable — the same fast-ingredient
   discipline the wave-16 predecessor introduced (and one further
   optimization, native to this front, described below) makes even
   `p=40` at full scale (`r≤200,b≤30`) run in under 30 seconds — so this
   front closed the doubled range `p=21,...,40` at full scale, plus an
   honestly-labelled *reduced-scale* exploratory push to `p=41,...,60`
   as bonus evidence (not claimed as fully verified at the main scale).
2. **`124 620` exact exhaustive checks against an independent ground
   truth (Corollary A3, own from-scratch Stirling-number
   implementation), `0` mismatches, across `p=21,...,40`, at
   `r=0,...,200`, `b=0,...,30` for every one of the twenty new `p`
   values** — matching the wave-16 predecessor's own scale ceiling
   exactly (`r≤200,b≤30`), not scaled down as `p` grows, for a range
   twice as wide as its own (`372.2s` wall clock). Plus a further
   reduced-scale exhaustive push to `p=41,...,60` (`13 420` checks, `0`
   mismatches, `295.1s`) and a randomized stress test (seed
   `20260870000`, this front's reserved range) reaching `r` up to `400`
   and `b` up to `60` (`400` checks, `0` mismatches, `291.5s`). **Grand
   total: `138 040` exhaustive checks + `400` randomized checks, `0`
   mismatches anywhere.** See §3.2-3.3 for the full per-`p` breakdown
   (`run_full_sweep.log`, `random_spotcheck.log`).
3. **No new mathematical ingredient is used or claimed anywhere in this
   document.** Every piece of the assembly is cited, PROVED input: the
   assembly formula itself (wave 15, reproduced unchanged by wave 16);
   the `H_k(r,b)` machine's correctness for *every* `k` (wave-15
   referee's induction); and — used directly here, one level stronger
   than either predecessor had — the wave-16 referee's own **closed
   factorization** `S_{2k-1}(N,m)=A_k(N,m)\cdot C(N,m{+}1)` and **proved**
   degree bound `\deg_r H_{2k-1}(r,b)=k-1`. This front independently
   re-derives that same factorization from the ORIGINAL cited
   `S_{2k-1}` recursion (not by copying the referee's restated form) as
   a documented sanity check (§2), then implements it as a direct,
   interpolation-free polynomial recursion — one algorithmic step
   simpler than either predecessor's own `H_k` route (the wave-15
   closure attempt used raw `sympy.cancel`; the wave-16 extension used
   evaluate-then-interpolate; this front's `H_k` comes out as an exact
   polynomial in `r` by construction, no cancellation and no
   interpolation needed at all).
4. **Every script in this directory is written fresh** — `ground_truth.py`,
   `ingredients.py`, `odd_part.py`, `assemble.py`, `symbolic_route.py`,
   `random_spotcheck.py` — none imported from, and none reading, any
   predecessor front's `.py` files, per the task's explicit discipline.
5. **Two self-caught bugs are disclosed in full** (§5): an off-by-one in
   the classical Faulhaber power-sum formula (a Bernoulli-number
   convention mismatch, caught immediately by a from-scratch
   cross-check against direct summation, before anything downstream was
   trusted), and a test-only indexing slip in this front's own
   `odd_part.py` self-test (comparing the wrong dictionary key, not a
   bug in the `H_k` machine itself, caught the same way). Both are
   exactly the class of error this archive's disclosure convention asks
   for — caught by a sweep or cross-check failing loudly, not by careful
   a-priori reasoning, and fixed before any downstream result depended
   on the buggy version.
6. **New, previously-unknown closed forms are printed for `p=21,...,40`
   at `b=0,1`** (pure Fraction poly-in-`r` arithmetic, no denominator —
   proved clean via a fact independently discovered and verified while
   resolving an apparent paradox during derivation: `Q_p(-1)=0` for
   every `p\ge1`, §2.4), plus representative `b=2,3` instances for two
   `p` values via a separate sympy-based symbolic route, cross-validated
   against the main Fraction route.
7. **What is not claimed:** exactly the same limits every predecessor in
   this lineage named — no single elementary formula with `p` as a free
   symbolic variable (`Q_p(u)` has genuine degree `2p`); the strip sum
   is still an explicit `b`-term sum, by design; `p>40` at full scale was
   not attempted (only the reduced-scale `p=41..60` push, honestly
   labelled as such); no independent adversarial re-verification of this
   document has been performed (out of scope for this front, per the
   task's instructions).

---

## 0. Disciplina

**Sources read, in full, before any derivation:**

1. `THEOREM.md` §§6–9 and "Estágio" 8 (the `H_r(t,b)`/`D^*_r(0)` closed
   forms, Teorema 1/Teorema 3), "Estágio 9" (the all-orders closed form,
   `F_r/G_r/H_r`, Corollary A3), "Estágio 14" (general-`b`
   `D^{*(p)}_r(b)` for `p=1,2,3,4`), "Estágio 16" (general-`p` closure
   `p=1..10`, the wave-15 referee's induction that `H_k` is correct for
   every `k`), "Estágio 21" (the wave-16 extension to `p=11..20`, and
   the wave-16 referee's *proved* degree bound `\deg_r H_{2k-1}=k-1`).
2. `general_p_dstar_closure_attempt/ATTEMPT.md` — the wave-15 front. Two
   of its base cases were independently reproduced here as a sanity
   check (§2 below) before anything else was trusted, per the task
   mandate's explicit instruction.
3. `general_p_dstar_extension_attempt/ATTEMPT.md` — the direct
   predecessor (prose only, no `.py` file opened). Its own
   `adversarial/REFEREE_REPORT.md` was also read — it supplies a closed
   factorization of `S_{2k-1}` and a *proved* degree bound that this
   front uses directly as cited input (see §2), a strictly stronger
   starting point than either predecessor had at the time it was
   written.

**Reuse policy** (same convention as every predecessor in this lineage).
Every script in this directory (`ground_truth.py`, `ingredients.py`,
`odd_part.py`, `assemble.py`, `symbolic_route.py`, `random_spotcheck.py`)
is written from scratch — **no predecessor `.py` file, from any front in
this lineage, was opened, read, or imported at any point**, per the
task's explicit instruction. **Used as fixed, already-PROVED input, never
re-derived:**

- Corollary A3 (`all_orders_closed_form_attempt/ATTEMPT.md` §4.3).
- The general-`p` assembly formula itself (`general_p_dstar_closure_attempt/ATTEMPT.md`
  §2, reproduced unchanged by `general_p_dstar_extension_attempt/ATTEMPT.md`
  §1) — `Q_p(u)`'s degree/vanishing; the even/odd split and Step-3
  reflection collapse; `(E1)`, `(E2)`; the cited `S_{2k-1}(N,m)`
  recursion.
- The wave-15 referee's inductive proof that `H(power,depth)` — as
  defined by the `(E2)`-based recursion — equals
  `P_b\cdot S_{\mathrm{power}}(N{-}d,r{-}d)` for **every** `(power,d)`,
  not just numerically-checked values (load-bearing fact behind this
  entire lineage's low-risk classification for `p>10`).
- The wave-16 referee's closed factorization
  `S_{2k-1}(N,m)=A_k(N,m)\cdot C(N,m{+}1)` and the **proved** degree
  bound `\deg_r H_{2k-1}(r,b)=k-1`, leading coefficient `4^{k-1}(k-1)!`,
  independent of `b` (`general_p_dstar_extension_attempt/adversarial/REFEREE_REPORT.md`
  §2a–2b).

**What is executed here for the first time:** the assembly, run for
`p=21,...,40` at full scale (and `p=41,...,60` at reduced scale), using a
*from-scratch re-derivation and re-implementation* of every ingredient —
including an independent re-derivation of the `A_k` recursion directly
from the originally-cited `S_{2k-1}` recursion (§2), not a re-use of the
wave-16 referee's own restated recursive form (which was read, but not
copied into code) — and one further speed optimization native to this
front (combining, once per `(p,b)`, the several `H_k`- and
`\mu_{2l}`-weighted sums into single polynomials before the `r`-sweep,
turning an `O(p^2)`-per-`r` evaluation into `O(p)`-per-`r`; §3, cross-
validated against the un-combined route before being trusted).

**Exactness policy.** `fractions.Fraction` throughout the verification
sweep; `sympy.Rational` only in the separate, clearly-marked
`symbolic_route.py`, used solely to print a handful of representative
`b\ge2` closed forms (never for the verification sweep). No floating
point anywhere in this directory's non-throwaway code.

**Randomness.** Python's `numpy.random.SeedSequence`, seeded from this
front's reserved range **`20260870000-20260870999`**
(`DISC-DEC-078`, front (a)) — used only in `random_spotcheck.py`, a
supplementary stress test beyond the exhaustive grid (§3.3). Confirmed
unused elsewhere in the archive before first use:
`grep -rn "20260870" 05_DISCOVERY_LAB/` returns only the ledger's and
`DISCOVERY_LAB_STATE.md`'s own reservation lines for this front. The
referee range `20260871000+` was not touched.

**Pre-registration.** `DERIVATION_PREREG.md` in this directory was
written, naming the route, the target scale (`p=21..30` floor, `p=31..40`
stretch, both at `r≤200,b≤30`), and the honesty commitments, before any
non-throwaway verification run.

---

## 1. The target and the route, restated (cited, unchanged)

Fix `p\ge0`. Corollary A3 (PROVED, cited, not re-derived):

`\displaystyle D^{*(p)}_r(b):=\sum_{j=p}^{r}c_j^{(r)}(b)\cdot c(j{+}1,\,j{+}1{-}p)`,
`c_j^{(r)}(b):=\dfrac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}`, `c(N,M)` the
unsigned Stirling numbers of the first kind.

The assembly formula (PROVED given its cited ingredients, reproduced
verbatim from `general_p_dstar_closure_attempt/ATTEMPT.md` §2, unchanged
by `general_p_dstar_extension_attempt/ATTEMPT.md` §1, unchanged again
here):

`N:=2r+b+1`, `\beta:=b+1`,

`\displaystyle D^{*(p)}_r(b)=\tfrac12\Big[\Phi_b(r)M_p(N)-\mathrm{Strip}_p(r,b)\Big]-\sum_{k=1}^{p}o_k\,\dfrac{H_{2k-1}(r,b)}{2^{2k-1}}`,

with `Q_p(-(v+\beta/2))=E_p(v)+O_p(v)` (even/odd split), `e_{2l}`, `o_k`
its coefficients, `M_p(N):=\sum_l e_{2l}\mu_{2l}(N)`, `\Phi_b(r):=P_b2^N`,
`\mathrm{Strip}_p(r,b):=\sum_{i=1}^bE_p(i-\beta/2)w_i(r,b)`,
`w_i(r,b):=r!(r{+}b)!/[(r{+}i)!(r{+}b{+}1{-}i)!]`,
`H_{2k-1}(r,b):=P_b\,S_{2k-1}(N,r)`.

This front changes nothing about the above. It runs it for `p=21,...,40`
(and, at reduced scale, `p=41,...,60`).

---

## 2. Ingredients, re-derived and re-implemented from scratch

### 2.1 `Q_p(u)`, via Newton's identities (`ingredients.py`)

`Q_p(u):=e_p(1,\dots,u)`, computed via the classical Faulhaber power-sum
polynomials `P_i(u):=\sum_{k=1}^uk^i` and Newton's identity
`p\cdot e_p=\sum_{i=1}^p(-1)^{i-1}e_{p-i}P_i(u)` — a textbook algorithm,
general in `p`. `P_i(u)` is computed from Bernoulli numbers (own
recurrence, `B_1=-1/2` convention) via the classical formula, general in
`i`, not fitted.

**Verified**, general `p`: against a direct, independent computation of
`e_p(1,\dots,u)` (DP over the numbers `1,\dots,u`, no Newton's identity
involved), `p=0,\dots,14`, `u=0,\dots,15`: **`240` exact checks, `0`
mismatches**, and against the vanishing boundary `Q_p(u)=0` for
`u=0,\dots,p-1`, `p=1,\dots,24`: **`300` checks, `0` mismatches**.

### 2.2 Central moments `\mu_{2l}(N)`, via the cumulant generating function
(`ingredients.py`)

`\mu_{2l}(N):=2^{-N}\sum_\alpha(\alpha-N/2)^{2l}\binom N\alpha`, extracted
from `M(t)=\exp(N\log\cosh(t/2))` via the classical power-series
log-then-exponentiate recurrence (own from-scratch derivation of both the
`\log` recurrence and the `\exp` recurrence, standard "match derivative
coefficients" technique — exact `Fraction` arithmetic, `N` tracked as a
formal linear-in-`N` polynomial throughout so `\mu_{2l}(N)` comes out
directly as a **reusable polynomial in `N`**, no interpolation needed).

**Verified**, general `l`: against direct binomial summation,
`l=0,\dots,11`, `N=0,\dots,23`: **`288` exact checks, `0` mismatches**,
plus `\mu_0(N)=1`, `\mu_2(N)=N/4` sanity checks for `N=0,\dots,9`.

### 2.3 The `H_{2k-1}(r,b)` machine, INDEPENDENTLY re-derived and
interpolation-free (`odd_part.py`)

**Independent re-derivation, done here, not copied from the referee's own
restated form.** Starting from the ORIGINALLY-cited recursion
(`general_p_dstar_closure_attempt/ATTEMPT.md` §0 item 2, itself citing
`DISC-DEC-059`):

`S_1(N,m)=(m{+}1)C(N,m{+}1)`,
`S_{2k-1}(N,m)=(N{-}2m)^{2k-2}(m{+}1)C(N,m{+}1)+2N\sum_{s\text{ odd},1\le s\le2k-3}\binom{2k-2}{s}S_s(N{-}1,m{-}1)`,

substitute `S_{2k-1}=A_k\cdot C(N,m{+}1)` (`A_1(N,m):=m{+}1`), use the
elementary factorial identity `C(N{-}1,m)=\tfrac{m+1}N C(N,m{+}1)`
(one line, verified below), and divide through by `C(N,m{+}1)`:

`\displaystyle A_k(N,m)=(m{+}1)\Big[(N{-}2m)^{2k-2}+2\sum_{s\text{ odd},1\le s\le2k-3}\binom{2k-2}sA_{(s+1)/2}(N{-}1,m{-}1)\Big]`.

Specializing `N=2r{+}b{+}1,\ m=r`, tracking depth `d` via
`a_k^{(d)}(r):=A_k(N{-}d,r{-}d)`:

`\displaystyle a_k^{(d)}(r)=(r{-}d{+}1)\Big[(\beta{+}d)^{2k-2}+2\sum_{s\text{ odd},1\le s\le2k-3}\binom{2k-2}sa_{(s+1)/2}^{(d+1)}(r)\Big]`,
base case `a_1^{(d)}(r)=r{-}d{+}1`.

This **matches** the wave-16 referee's independently-stated closed form
character-for-character — an independent confirmation via a different
route (algebra from the originally-cited recursion, not the referee's own
inductive proof) — and is what `odd_part.py` implements. Since
`P_b\cdot C(N,r{+}1)=1/(r{+}1)` (elementary), and the top-level prefactor
at depth `0` is exactly `(r{+}1)` for `k\ge2`, `H_{2k-1}(r,b)` is read off
**directly** as the depth-`0` bracket — no division step is ever
performed (avoided by construction, not performed-then-checked); `H_1=1`
by the `k=1` base case.

**Verified**, general `k`, fixed concrete `b`:

- Against `S_odd_direct`, an independent brute-force implementation of
  the ORIGINAL cited `S_{2k-1}` recursion (no `A_k` factorization at
  all), `k=1,\dots,9`, `r=0,\dots,9`, `b\in\{0,1,2,5,8\}`: **`450` exact
  checks, `0` mismatches**.
- Against the two concrete brackets printed by the wave-15 closure
  attempt and confirmed by the wave-16 referee — `H_1=1`, `H_3=\beta^2+4r`
  — `b=0,\dots,5`, `r=0,\dots,14`: **`180` exact checks, `0`
  mismatches** (this is the "reproduce a couple of the citation's base
  cases" sanity check the task mandate explicitly asked for).
- The degree bound `\deg_rH_{2k-1}(r,b)=k-1`, leading coefficient
  `4^{k-1}(k-1)!`, independent of `b` — **cited as PROVED** (wave-16
  referee), **re-checked numerically here**, `k=1,\dots,45`,
  `b\in\{0,1,3,7,30\}`: **`450` checks, `0` mismatches**.
- Cross-consistency between two different `K_max` table-build sizes
  (`6` vs. `20`), `k=1,\dots,6`, `b\in\{0,4\}`, `r=0,\dots,7`: **`96`
  checks, `0` mismatches** (catches any `K_max`-dependent bug in the
  rolling depth-table construction).

**`odd_part.py` self-test total: `1176` exact checks, `0` mismatches.**

### 2.4 A note on `Q_p(-1)`, discovered and verified while resolving an
apparent paradox

While checking whether the printed `b=1` closed forms (§4) could be pure
polynomials in `r` (as every predecessor's own `p\le4,b=1` formulas are),
a structural worry arose: the assembly's `\mathrm{Strip}_p(r,1)` term
equals `Q_p(-1)/(r{+}1)` (since `\beta=2` at `b=1`, so
`i-\beta/2=1-1=0`, and `E_p(0)=Q_p(-1)`, `w_1(r,1)=1/(r{+}1)`), which
would introduce a genuine `1/(r{+}1)` denominator **unless** `Q_p(-1)=0`.
Hand-checking `p=1,2` (both `0`) suggested a pattern; **this was tested
computationally, not assumed** — and the first test, run against the
(at that point still buggy — see §5) `power_sum_poly`, appeared to
*refute* the pattern for `p\ge3` (returning `1`, not `0`). After the
Faulhaber off-by-one (§5) was found and fixed, the same test showed
`Q_p(-1)=0` for **every** `p=1,\dots,40` tested — confirming the original
by-hand observation and resolving the paradox: the `b=1` remainder
**is** a pure polynomial for every `p`, because the one term that could
have broken that pattern vanishes identically.

---

## 3. Assembly, ground truth, and verification

`ground_truth.py`: independent, from-scratch Corollary A3 implementation
(own unsigned-Stirling recurrence `c(n,k)=c(n{-}1,k{-}1)+(n{-}1)c(n{-}1,k)`),
calibrated against **every** PROVED formula already in `THEOREM.md`:
`p=1,2` at `b=0`; `p=1,2,3,4` at `b=1`; the closure attempt's printed
`p=1,b=2` instance; the `r<p` vanishing boundary (`p=1,\dots,40`); and a
plain non-negativity smoke test, and (added after the speed
optimizations of §3) a check that the cached `factorial()` matches
`math.factorial` exactly, `n=0,\dots,299` — **`4260` checks, `0` fails**
(`ground_truth.py::self_test`).

`assemble.py`'s `Assembler` class precomputes, once per `(p,b)` pair
(§0's "what is executed here for the first time"): the even/odd split of
`Q_p(-(v+\beta/2))`; the `H_k` polynomial-in-`r` table; and — this
front's own speed optimization — two **combined** polynomials
(`combined_mu_poly` in `N`, `combined_H_poly` in `r`) replacing the
per-term sums, cutting the per-`r` evaluation cost from `O(p^2)` to
`O(p)`. **Cross-validated against the un-combined ("slow") per-term
route before being trusted for anything**, `p\in\{1,2,5,10\}`,
`b\in\{0,1,3\}`, `r\in\{0,1,5,17,42\}`: **`180` checks, `0` mismatches**
(`speed_route_selftest`).

### 3.1 Calibration: reproduces `p\le10` exactly (sanity gate before the
`p\ge21` sweep)

`Assembler.D_star`, checked against `ground_truth.D_star`:

| range | checks | fails |
|---|---|---|
| `p=1..10`, `b=0,1`, `r=0..59` | `1200` | `0` |
| `p=1..3`, `b=2,3`, `r=0..39` | `240` | `0` |

**`1440` checks, `0` fails** (`assemble.py::calibration_self_test`).

### 3.2 Main sweep: `p=21,...,40`, `r=0,...,200`, `b=0,...,30`

`Assembler.D_star`, checked against `ground_truth.D_star`, exact
`fractions.Fraction` comparison throughout:

| `p` | `r` range | `b` range | checks | fails | time |
|---|---|---|---|---|---|
| 21 | 0..200 | 0..30 | 6231 | 0 | 13.24s |
| 22 | 0..200 | 0..30 | 6231 | 0 | 13.10s |
| 23 | 0..200 | 0..30 | 6231 | 0 | 13.10s |
| 24 | 0..200 | 0..30 | 6231 | 0 | 13.62s |
| 25 | 0..200 | 0..30 | 6231 | 0 | 14.29s |
| 26 | 0..200 | 0..30 | 6231 | 0 | 15.04s |
| 27 | 0..200 | 0..30 | 6231 | 0 | 15.62s |
| 28 | 0..200 | 0..30 | 6231 | 0 | 15.54s |
| 29 | 0..200 | 0..30 | 6231 | 0 | 16.13s |
| 30 | 0..200 | 0..30 | 6231 | 0 | 17.72s |
| 31 | 0..200 | 0..30 | 6231 | 0 | 17.77s |
| 32 | 0..200 | 0..30 | 6231 | 0 | 19.09s |
| 33 | 0..200 | 0..30 | 6231 | 0 | 20.73s |
| 34 | 0..200 | 0..30 | 6231 | 0 | 19.85s |
| 35 | 0..200 | 0..30 | 6231 | 0 | 20.53s |
| 36 | 0..200 | 0..30 | 6231 | 0 | 22.43s |
| 37 | 0..200 | 0..30 | 6231 | 0 | 23.15s |
| 38 | 0..200 | 0..30 | 6231 | 0 | 25.00s |
| 39 | 0..200 | 0..30 | 6231 | 0 | 27.93s |
| 40 | 0..200 | 0..30 | 6231 | 0 | 28.36s |

**Total: `124 620` checks (`20` values of `p` × `6231` `(r,b)` pairs
each), `0` fails, `372.2s` wall clock** — the same full scale used at
every one of the twenty new `p` values, matching the wave-16
predecessor's own scale ceiling exactly, for a range twice as wide as
its own. Full log: `run_full_sweep.log`.

### 3.3 Beyond the committed target: reduced-scale exploratory push and
a randomized stress test

**(a) `p=41,...,60` at reduced scale (`r\le60,b\le10`)** — an honestly-
labelled exploratory push, **not** claimed as verified at the main
scale:

| `p` | `r` range | `b` range | checks | fails | time |
|---|---|---|---|---|---|
| 41 | 0..60 | 0..10 | 671 | 0 | 6.28s |
| 42 | 0..60 | 0..10 | 671 | 0 | 6.95s |
| 43 | 0..60 | 0..10 | 671 | 0 | 7.47s |
| 44 | 0..60 | 0..10 | 671 | 0 | 8.14s |
| 45 | 0..60 | 0..10 | 671 | 0 | 8.99s |
| 46 | 0..60 | 0..10 | 671 | 0 | 9.91s |
| 47 | 0..60 | 0..10 | 671 | 0 | 10.36s |
| 48 | 0..60 | 0..10 | 671 | 0 | 11.98s |
| 49 | 0..60 | 0..10 | 671 | 0 | 13.35s |
| 50 | 0..60 | 0..10 | 671 | 0 | 13.52s |
| 51 | 0..60 | 0..10 | 671 | 0 | 14.89s |
| 52 | 0..60 | 0..10 | 671 | 0 | 16.01s |
| 53 | 0..60 | 0..10 | 671 | 0 | 15.95s |
| 54 | 0..60 | 0..10 | 671 | 0 | 17.46s |
| 55 | 0..60 | 0..10 | 671 | 0 | 19.25s |
| 56 | 0..60 | 0..10 | 671 | 0 | 20.15s |
| 57 | 0..60 | 0..10 | 671 | 0 | 21.53s |
| 58 | 0..60 | 0..10 | 671 | 0 | 22.37s |
| 59 | 0..60 | 0..10 | 671 | 0 | 24.77s |
| 60 | 0..60 | 0..10 | 671 | 0 | 25.74s |

**Total: `13 420` checks, `0` fails, `295.1s` wall clock.**

**Grand total, this front's entire verification effort (main + stretch
sweep, not counting the randomized spot-check below or the `280`
printed-form cross-checks or the various self-tests already tallied in
§2): `138 040` checks, `0` fails.**

**(b) Randomized stress test beyond the exhaustive grid**
(`random_spotcheck.py`, seed `20260870000`): `400` random `(p,r,b)`
triples, `p\in[21,60]`, `r\in[0,400]`, `b\in[0,60]` — reaching further
in `r` and `b` than either the main sweep or the exploratory push, at
the cost of coverage being random rather than exhaustive:

```
random_spotcheck: seed=20260870000, n_samples=400, p in (21, 60), r in (0, 400), b in (0, 60)
  distinct (p,b) Assembler builds: 364
  400 checks, 0 fails, 291.5s
random_spotcheck: OK
```

### 3.4 New closed forms, printed and cross-validated

**`b=0,1`, all `p=21,\dots,40`** — pure Fraction poly-in-`r` arithmetic
(`assemble.py::printed_form_b0/b1`), no denominator (justified by §2.4:
`\mathrm{Strip}_p(r,0)\equiv0` trivially; `\mathrm{Strip}_p(r,1)\equiv0`
because `Q_p(-1)=0`, checked at four concrete `r` before trusting each
`b=1` print, per `printed_form_b1`'s own internal assertion). Every
printed instance cross-checked against `ground_truth.D_star` at
`r\in\{0,5,17,50,150\}` (and, for `b=1`, additionally `r=0,\dots,50` in
`assemble.py`'s own module-level smoke test): **`0` mismatches**. Full
list in `printed_forms.log`; representative instance (`p=21,b=0`,
raw unfactored form, degree-`21` numerator — following the wave-16
predecessor's own choice at `p\ge11` to print unfactored monomial sums
rather than risk a hand-transcription error in a large factorization):

```
D^{*(21)}_r(0):

coef(r) = (67282234305/1152921504606846976)*r^21 + (59101699231575/576460752303423488)*r^20
  + (74857893550250965/3458764513820540928)*r^19 + (18222106392424142285/15564440312192434176)*r^18
  + (80221061678628360589/5188146770730811392)*r^17 - (87654986612590271920819/1470839609502185029632)*r^16
  - (2910034888705227821675969/4902798698340616765440)*r^15 + (1073957351962682453144939/210119944214597861376)*r^14
  - (8666579961263612211340381/653706493112082235392)*r^13 - (528384082314035014618752697/32358471409048070651904)*r^12
  + (62931426527274494657537489/280159925619463815168)*r^11 - (2297987468004055006611438115/2941679219004370059264)*r^10
  + (26949293874782913893915777/17509995351216488448)*r^9 - (665153984333173182419966189/367709902375546257408)*r^8
  + (206087921935183819301653333/204283279097525698560)*r^7 + (56511580623452656383022613/183854951187773128704)*r^6
  - (1945917227091802380986503/2188749418902061056)*r^5 + (612992945919459418495453/1276770494359535616)*r^4
  + (13246352637939039966527/531987705983139840)*r^3 - (1755807114380064545749/16255179905040384)*r^2
  + (120286097510180813/4398046511104)*r

rem(r) = -(5/1572864)*r^20 - (37639/23592960)*r^19 - (850069/5160960)*r^18 - (5122076591/1114767360)*r^17
  - (10145992332797/662171811840)*r^16 + (69516483968077/220723937280)*r^15 - (60343126900871/78829977600)*r^14
  - (8744256774746851781/1641634283520000)*r^13 + (219160539866070782832469/4865804016353280000)*r^12
  - (47362280795819410229/310418119065600)*r^11 + (328052681424454692887/1301017116672000)*r^10
  + (84499808343298394737/18431075819520000)*r^9 - (465981045762588971581/438835138560000)*r^8
  + (5059812737412590078189/1843107581952000)*r^7 - (59454690145506858403589/15205637551104000)*r^6
  + (22287585948893468255587/6335682312960000)*r^5 - (1049038073134805937851/527973526080000)*r^4
  + (2828728705843865537/4399779384000)*r^3 - (39529321243553/436486050)*r^2
```

(so `D^{*(21)}_r(0) = coef(r)\cdot\varphi_r + rem(r)`, exactly — pure
polynomials in `r`, no denominator, exactly as at `b\le20`; note `rem`
has NO linear or constant term at this `p`, a pattern also visible at
several other new-`p` instances in `printed_forms.log`, not investigated
further here.) The remaining `19` new `p=22,\dots,40` instances at
`b=0,1` are in `printed_forms.log`, along with `b=2,3` instances at
`p=21,25` referenced below.

**`b=2,3`, representative instances (`p=21,25`)** — via `symbolic_route.py`
(a separate sympy-based construction, r kept symbolic, `sympy.cancel`
used for the genuinely non-polynomial strip-sum denominators that appear
at `b\ge2` — matching the `(2r{+}3)`-type denominator pattern every
predecessor observed at `p\le20`). Cross-validated against
`Assembler.D_star` at five concrete `r` values per `(p,b)`:

```
p=21 b=2: cross-validate OK
p=21 b=3: cross-validate OK
p=25 b=2: cross-validate OK
p=25 b=3: cross-validate OK
symbolic_route.py: OK
```

Representative instance (`p=21,b=2`; full expressions, `p=21,b=3` and
`p=25,b=2,3`, in `symbolic_forms_p21b2.txt` and reproducible via
`symbolic_route.py`) — note the `(2r{+}3)` denominator on the `\varphi_r`
coefficient and the `(r{+}1)` denominator on the remainder, exactly the
pattern every predecessor observed at `b\ge2`, `p\le20`, now confirmed to
persist at `p=21`:

`\displaystyle D^{*(21)}_r(2)=\frac{(r{+}2)\cdot N_{21,2}(r)}{808961785226201766297600\,(2r{+}3)}\varphi_r-\frac{D_{21,2}(r)}{19463216065413120000\,(r{+}1)}`,

where `N_{21,2}(r)` (degree `21`) and `D_{21,2}(r)` (degree `21`) are the
explicit integer-coefficient polynomials printed in full by
`symbolic_route.py` (coefficients up to `48` digits; omitted here for the
same "don't hand-transcribe what risks a copy error" reason the wave-16
predecessor gave for its own `p=15,20` instances).

---

## 4. What this closes, precisely

**The general-`p` closed-form algorithm for `D^{*(p)}_r(b)` is now
executed and verified for `p=1,\dots,40`, every `b\ge0`** — doubling the
range closed by the wave-16 predecessor (`p=1,\dots,20`), using the
identical mathematical content (assembly formula, `H_k` correctness for
every `k`) and an independently re-derived, interpolation-free
implementation of every ingredient. Concretely:

- The predecessors' `p=1,\dots,10` (wave 15) and `p=11,\dots,20`
  (wave 16) results are reproduced exactly by this front's independently
  re-derived and re-implemented assembly (§3.1) — **not** by importing
  or re-running any predecessor code.
- **New closed forms for `p=21,\dots,40` — the mandate's full target
  range, doubled — are produced and verified at the largest scale used
  anywhere in this lineage, uniformly across all twenty new values**
  (§3.2, §3.4).
- **An honestly-labelled reduced-scale push reaches `p=60`** (§3.3(a)),
  and a randomized stress test independently confirms correctness at
  `r,b` values beyond either sweep's exhaustive range (§3.3(b)) — both
  presented as exactly what they are (reduced-scale/randomized, not
  full-scale-exhaustive), per this front's own pre-registered honesty
  commitments.
- **The `H_k(r,b)` machine's underlying correctness-for-every-`k`**
  (wave-15 referee's induction) **and its degree bound** (wave-16
  referee's proof) are used directly, and this front's own independent
  re-derivation of the `A_k` factorization (§2.3) from the ORIGINAL
  cited recursion is an additional, independent confirmation of that
  factorization via a different route than the referee's own.

## 5. Self-caught issues, disclosed

Per this archive's standing transparency convention (see e.g.
`general_p_dstar_extension_attempt/ATTEMPT.md` §2.4's own disclosure, the
model this front followed):

### 5.1 Faulhaber power-sum off-by-one (real bug, in `ingredients.py`,
caught before anything downstream was trusted)

The first version of `power_sum_poly(i)` applied the classical Faulhaber
formula `\tfrac1{i+1}\sum_jC(i{+}1,j)B_ju^{i+1-j}` (with this file's
`B_1=-1/2` Bernoulli convention) directly, as if it computed
`P_i(u)=\sum_{k=1}^uk^i`. **It does not** — with that convention the
classical formula computes `S_i(n):=\sum_{k=0}^{n-1}k^i` (an off-by-one:
`n` terms, `k=0,\dots,n{-}1`), not `\sum_{k=1}^uk^i`. **Caught
immediately** by `ingredients.py`'s own from-scratch cross-check against
direct summation (`_power_sum_direct`), which failed loudly and
systematically (every `(i,u)` pair with `i\ge1` showed `got(u)=want(u{-}1)`
— a clean, diagnostic shift) — before `power_sum_poly` had been used to
build a single `Q_p`. **Fixed** by using `P_i(u):=S_i(u{+}1)` (evaluating
the classical formula at `n=u{+}1` via `poly_compose_linear`), with a
**second**, smaller edge case caught by the same re-run: `i=0` needs a
`-1` correction the general formula doesn't supply (`0^0=1` under the
usual convention spuriously counts a `k=0` term that
`P_0(u):=\sum_{k=1}^u1=u` must exclude), handled by special-casing
`i=0` directly rather than patching the general formula. **Re-verified**
after both fixes: `i=0,\dots,24`, `u=0,\dots,19`, **`500` checks, `0`
mismatches**; downstream, `Q_p(u)` and every check depending on it (§2.1,
and everything after) were only ever run against the FIXED version — the
bug never propagated into any trusted result.

### 5.2 A test-only indexing slip in `odd_part.py`'s own self-test (NOT a
bug in the `H_k` machine itself)

An early version of `odd_part.py`'s self-test compared `H[3]` (this
file's dict is keyed by `k`, so `H[k]` represents `H_{2k-1}` — `H[3]` is
therefore `H_5`) against the printed formula for `H_3` (which is
`H[2]`). This produced large, obviously-wrong mismatches for `b\ge2`
(`H_5` and the `H_3` formula are genuinely different polynomials of
different degree) — caught immediately, on the very first run, by the
same "a sweep failing loudly" discipline. **This was a test bug, not an
implementation bug**: `build_H_table` itself had already been
independently validated in the *same* self-test run, one block earlier,
against brute-force `S_odd_direct` for `k=1,\dots,9` (§2.3) — that block
passed with `0` mismatches both before and after the indexing fix.
Fixed by indexing `H[2]`, not `H[3]`, for the `H_3` formula check;
re-run, `0` mismatches (§2.3).

**No other component** (`Q_p`'s Newton-identity construction beyond the
Faulhaber layer, the central-moment power-series recurrence, the `H_k`
recursion itself, `(E1)`, `(E2)`, the combined-polynomial speed route,
`ground_truth.py`'s Stirling recurrence) exhibited any error at any
point in this front's development.

---

## 6. What remains open, precisely

1. **`p>40` at the main (full) scale was not attempted.** A reduced-scale
   push reached `p=60` (§3.3(a)) and a randomized spot-check sampled up
   to `p=60` at larger `r,b` than either sweep (§3.3(b)) — both
   suggestive, neither dispositive, of continued tractability beyond
   `p=60`. No claim, positive or negative, is made about `p>60`.
2. **No single elementary formula with `p` as a free symbolic variable is
   produced or believed to exist**, unchanged from every predecessor's
   own position — `Q_p(u)` has genuine degree `2p`.
3. **The strip sum is still an explicit `b`-term sum**, unchanged, by
   design, from every predecessor in this lineage.
4. **`b\ge2` closed forms are printed only for two representative `p`
   values** (`p=21,25`, via the separate sympy route, §3.4) — not for
   the full `p=21,\dots,40` range. This is a scope choice (the main
   exhaustive sweep already verifies every `b\le30` numerically for
   every `p` in range; printing every symbolic `b\ge2` instance was not
   attempted and is not needed for the numerical closure claimed here),
   not a limitation of the method.
5. **No independent adversarial re-verification of this document has
   been performed.** Per standing archive discipline and the task's
   explicit instructions, referee dispatch is out of scope for this
   front and is reserved for the orchestrating session. §7 names what a
   referee should attack first.
6. **It does not change the status of anything already catalogued.**
   Corollary A3, the wave-15/16 fronts' `p=1,\dots,20` results, and every
   PROVED calibration formula quoted here are reproduced exactly, not
   superseded or weakened.

---

## 7. What a hostile referee should attack first

- **§2.3, the independent re-derivation of the `A_k` recursion.** This
  front re-derived the closed factorization from the ORIGINALLY-cited
  `S_{2k-1}` recursion rather than reusing the wave-16 referee's own
  restated form — a referee should redo this derivation independently
  (it is a few lines of factorial algebra) and confirm it matches both
  this document's stated recursion and the wave-16 referee's own,
  character-for-character.
- **The combined-polynomial speed optimization (§3, `Assembler`'s
  `combined_mu_poly`/`combined_H_poly`).** This front's own cross-check
  (`speed_route_selftest`, `180` checks) is smaller in scale than the
  main sweep it gates — a referee with more compute budget should push
  this cross-check to a scale closer to the main sweep itself, or
  construct an independent argument for why the combined and per-term
  routes must agree (they are the same finite sum reassociated, so
  agreement is essentially forced by exact-arithmetic associativity —
  but this was not separately argued in this document beyond the
  empirical check).
- **§2.4's `Q_p(-1)=0` fact**, used to justify that the `b=1` printed
  forms are pure polynomials. This is verified numerically here
  (`p=1,\dots,40`) but not proved from first principles in this
  document — a referee could attempt a short direct proof (e.g. via the
  Stirling-number identity `Q_p(u)=c(u{+}1,u{+}1{-}p)` and a known
  vanishing/reflection property of unsigned Stirling numbers at negative
  arguments, if one exists) or extend the numerical check further.
- **Whether the `r,b=0..200,0..30` scale is truly uniform coverage or
  hides a boundary effect**, mirroring both predecessors' own referees'
  scale-push methodology — a referee with more compute budget could push
  specific `p` values (e.g. `p=40`) further (`r=300` or beyond,
  mirroring the wave-16 referee's own push).
- **The two self-caught bugs (§5) and whether either fix is complete** —
  a referee should independently re-derive the Faulhaber power-sum
  fix (`P_i(u)=S_i(u{+}1)`, plus the `i=0` special case) from the
  Bernoulli-number definition used, and confirm `odd_part.py`'s
  corrected self-test indexing (`H[2]` for `H_3`, not `H[3]`) is used
  consistently everywhere `H_3` is referenced in this document.

---

## 8. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `Q_p(u)`, general `p`, via Newton's identities | **PROVED** (classical algorithm) + `540` exact checks vs. direct `e_p(1,\dots,u)` and the vanishing boundary, `0` fails |
| 2 | Central moments `\mu_{2l}(N)`, general `l`, via cumulant GF | **PROVED** (classical algorithm) + `288` exact checks vs. direct summation, `0` fails |
| 3 | `H_{2k-1}(r,b)` machine, independently re-derived, interpolation-free | **PROVED given cited `S_{2k-1}` recursion and (E2)** (both cited) + `1176` exact checks (brute force, printed brackets, degree bound, `K_max`-consistency), `0` fails |
| 4 | Degree bound `\deg_rH_{2k-1}=k-1`, lead `4^{k-1}(k-1)!` | **CITED** (PROVED, wave-16 referee) + re-checked numerically here, `k=1..45`, `0` fails |
| 5 | `Q_p(-1)=0` for every `p\ge1` | **NUMERICALLY VERIFIED**, `p=1..40`, `0` fails (not proved from first principles in this document — see §7) |
| 6 | Speed-optimized combined-polynomial assembly route | **PROVED given items 1-4** (mechanical reassociation) + `180` cross-checks vs. the un-combined route, `0` fails |
| 7 | Calibration: reproduces `p=1..10` (`b=0,1,2,3`) exactly | **CONFIRMED**, `1440/1440`, `0` fails |
| 8 | Main sweep, `p=21,\dots,40`, `r\le200,b\le30` | **PROVED given items 1-6**; `124 620` exact checks vs. independent ground truth, `0` fails |
| 9 | New closed forms, `b=0,1`, `p=21,\dots,40` | **PROVED** (algorithm, §2.4) + printed, cross-validated at concrete `r`, `0` fails |
| 10 | New closed forms, `b=2,3`, representative `p=21,25` | **NUMERICALLY VERIFIED** (via `symbolic_route.py`, cross-validated against the main Fraction route), `0` fails |
| 11 | Exploratory `p=41,\dots,60`, reduced scale | **NUMERICALLY VERIFIED at reduced scale** (`r\le60,b\le10`) — not claimed at the main scale |
| 12 | Randomized stress test, `p\in[21,60]`, `r\le400`, `b\le60` | **NUMERICALLY VERIFIED** at the sampled points (`400` random triples, seed `20260870000`) |
| 13 | A single symbolic-in-`p` elementary formula | **NOT CLAIMED, believed not to exist in elementary form** — `Q_p` has genuine degree `2p` |
| 14 | `p>60` | **OPEN** — not attempted at any scale |
| 15 | Independent adversarial re-verification of this document | **NOT PERFORMED** — out of scope for this front, reserved for the orchestrating session |

**Net honest verdict.** The mandate's full target (`p=21,\dots,30`) was
reached and doubled (`p=21,\dots,40`), at the largest verification scale
used anywhere in this lineage, uniformly across all twenty new values —
plus an honestly-labelled reduced-scale push to `p=60` and a randomized
stress test beyond either sweep's exhaustive range. This was possible
because the underlying mathematics has been PROVED correct for every `k`
(wave-15 referee's induction) and the wave-16 referee's proved degree
bound and closed factorization gave this front a strictly stronger,
faster-to-implement starting point than either predecessor had — and this
front's own further speed optimization (combining sums into single
polynomials before the `r`-sweep) kept even `p=40` at full scale under
`30` seconds. Two genuine issues were found and disclosed along the way
(§5): one real implementation bug (the Faulhaber off-by-one, caught
before it propagated anywhere), and one test-only indexing slip (caught
the same way, never a bug in the machine itself). The one substantive
limitation is scope, not soundness: `p>60` was not attempted at any
scale, and the `b\ge2` closed forms were only printed for two
representative `p` values, not the full new range (though verified
numerically for every `b\le30` throughout).

---

## 9. Seeds

| Use | Seed / range | Notes |
|---|---|---|
| `random_spotcheck.py` | `numpy.random.SeedSequence(20260870000)` | This front's reserved range, `20260870000-20260870999` (`DISC-DEC-078`, front (a)). Confirmed unused elsewhere before first use. Referee range `20260871000+` not touched. |
| Everything else in this directory | none | Exact symbolic/rational algebra or exhaustive finite sweeps over stated integer ranges — no randomness needed. |

---

## 10. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any non-throwaway verification run | — |
| `ground_truth.py` / `.log` | independent Corollary A3 implementation, own Stirling table, calibration smoke tests (`4260` checks) | ~1s |
| `ingredients.py` / `.log` | `Q_p(u)` (Newton's identities), central moments (power-series log/exp recurrence), self-tests (`1388` checks) — includes the disclosed Faulhaber off-by-one fix (§5.1) | ~1s |
| `odd_part.py` / `.log` | the `H_k(r,b)` machine (independently re-derived `A_k` recursion, interpolation-free), self-tests (`1176` checks) | ~4s |
| `assemble.py` / `.log` | full assembly (`Assembler` class), speed-route cross-check, calibration sweep, `printed_form_b0/b1` | <1s |
| `run_full_sweep.py` / `.log` | the production verification: `p=21..40` at full scale, `p=41..60` at reduced scale | see §3.2-3.3 |
| `random_spotcheck.py` / `.log` | randomized stress test, seed `20260870000` | see §3.3(b) |
| `symbolic_route.py` / `.log` | sympy-based route for representative `b=2,3` printed closed forms, cross-validated | see §3.4 |
| `symbolic_forms_p21b2.txt` | full printed `p=21,b=2` closed form (coef, remainder) | — |
| `print_closed_forms.py` / `printed_forms.log` | prints and cross-validates the full `b=0,1`, `p=21..40` closed-form list (`280` cross-checks) | ~1s |
| `ATTEMPT.md` | this document | — |

Reproduce in order: `python3 ground_truth.py`; `python3 ingredients.py`;
`python3 odd_part.py`; `python3 assemble.py`; `python3 run_full_sweep.py`
(the dominant cost, `~11` minutes wall clock — `372.2s` main sweep +
`295.1s` stretch sweep, measured); `python3 random_spotcheck.py`
(`~292s`, measured); `python3 symbolic_route.py`; `python3
print_closed_forms.py`. Total measured wall clock for the full
reproduction sequence: well under `20` minutes.
