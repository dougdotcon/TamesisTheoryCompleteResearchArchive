# General-`p` closure, extended: `D^{*(p)}_r(b)` for `p=11,...,20`

> **Governance.** Wave 15/16 follow-on front `GENERAL-P-DSTAR-EXTENSION-ATTEMPT`,
> authorized by `DISC-DEC-066` (`TEST_QUEUE.yaml`: "Estende a montagem de
> `D*(p)_r(b)` (Estágio 16) de `p=1,...,10` para `p` mais alto (meta
> `p=11,...,20`), usando a máquina `H_k` já provada correta para TODO `k`
> por indução (referee da onda 15). Risco baixo — barreira puramente de
> execução/custo simbólico."). Pure combinatorics on the Tamesis Discovery
> Lab's internal random-permutation-with-reroutes ensemble — **no
> Millennium Prize claim of any kind is made anywhere in this document**,
> no external data, no holdout, no real-world claim. **Nothing outside this
> directory was created, modified, or deleted.** No git commit was made.
> `THEOREM.md`, the decision ledger, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
> and every sibling attempt's files were not touched. **No `adversarial/`
> subdirectory was created and no referee was dispatched here** — per the
> task's explicit instructions, that is out of scope for this front,
> reserved for the orchestrating session. **This document requires
> independent mandatory adversarial verification before any integration
> into `THEOREM.md` or any other governance artifact**, exactly as every
> predecessor in this lineage required. Every claim below is labelled
> PROVED, CITED, NUMERICALLY SUPPORTED, or OPEN.

---

## Executive summary (read first)

1. **This is an execution front, not a new-theory front — and it executed
   cleanly all the way to the mandate's full target.** The already-proved,
   already-adversarially-confirmed general-`p` algorithm for `D^{*(p)}_r(b)`
   (`general_p_dstar_closure_attempt/ATTEMPT.md`, `p=1,...,10`, and its
   referee's inductive proof that the underlying `H_k(r,b)` machine is
   correct for **every** `k`) is run further here, unchanged in its
   mathematical content, for **`p=11,...,20` — the full requested range**.
   No new ingredient, no new identity, no new derivation step anywhere in
   this document.
2. **The two ingredients whose ORIGINAL (closure-attempt) implementation
   would genuinely have been too slow to reach `p=20`** — central moments
   `\mu_{2l}(N)` via `sympy`'s generic `series()`/`exp()` pipeline, and the
   `H_k(r,b)` machine via `sympy.cancel` — **were re-implemented as
   mathematically-identical, faster extractions of the SAME generating
   function / SAME recursion** (a classical power-series-exponentiation
   recurrence for the moments, the same algorithmic class as Newton's
   identities already used for `Q_p`; evaluate-then-exact-interpolate for
   `H_k(r,b)`, one step further along the same "substitute before
   simplify" axis the closure attempt's own `H_reduced_at_b` already used).
   **Both fast routes were cross-validated character-for-character against
   the original slow routes** — `l=1,\dots,10` for moments (`0` mismatches,
   plus `72` direct-binomial-summation checks), `\mathrm{power}=1,\dots,19`
   at five `b` values for `H_k` (`0` mismatches, plus `847` brute-force
   checks) — **before either was trusted for anything new**.
3. **`62 310` exact exhaustive checks against an independent ground truth
   (Corollary A3, own Stirling table), `0` mismatches, across
   `p=11,\dots,20`, at `r=0,\dots,200`, `b=0,\dots,30` for *every one* of
   the ten new `p` values** — matching the largest scale ever reached
   anywhere in this lineage (the wave-15 referee's own `p=5,6` scale
   ceiling), uniformly, not scaled down as `p` grows. This is possible
   (not merely attempted) because the fast ingredients above make the
   whole sweep run in `14`–`24` seconds even at `p=20`, where the closure
   attempt's own routes would not have reached even `p=11` at this scale
   in any reasonable time (see §0, exploratory timing).
4. **New, previously-unknown closed forms are produced for every
   `p=11,\dots,20` at `b=0,1`** (full list, `assemble_ext.log`), with
   representative instances at `b=2,3` for `p=11,15,20` printed in §3 below
   to confirm the `(2r+3)`-denominator pattern established at `p\le10`
   persists.
5. **One genuine bug was self-caught and fixed** (distinct from, but the
   same general lesson as, the closure attempt's own self-caught `w_i`
   off-by-one): a latent, previously-unexercised `sp.nsimplify` misuse in
   `D_star_predicted`, which silently corrupted an exact large `Rational`
   into a spurious irrational-looking expression. Disclosed in full in §2.4.
6. **What is not claimed:** exactly the same limits the closure attempt
   itself named — no single elementary formula with `p` as a free
   symbolic variable, and no claim about `p>20` (not attempted). Unlike
   the closure attempt, which left `p>10` open only because it ran out of
   scope, this document's own honest frontier assessment (§5) argues the
   remaining barrier for `p>20` is, if anything, *lower* than it looked
   after the closure attempt — see §5 for the reasoning and its limits.

---

## 0. Disciplina

**Sources read, in full, before any derivation:**

1. `general_p_dstar_closure_attempt/ATTEMPT.md` — the target front. Proves
   the general-`p` algorithm for `D^{*(p)}_r(b)`, executed for `p=1,\dots,10`,
   `26\,710` exact checks, `0` mismatches, plus `4054`+`2778`+`800`
   ingredient/ground-truth checks.
2. `general_p_dstar_closure_attempt/adversarial/REFEREE_REPORT.md` — the
   hostile referee's report (verdict SOUND, ACCEPT). Its §1c constructs an
   **inductive proof** (on depth, decreasing, then on power) that the
   `H(power,depth)` recursion — using only `(E2)` and the cited
   `S_{2k-1}(N,m)` recursion — equals `P_b\cdot S_{\mathrm{power}}(N-d,r-d)`
   for **every** `(\mathrm{power},d)`, not merely the values checked
   numerically. This is the load-bearing fact behind this front's low-risk
   classification and is used here as cited, PROVED input, exactly as the
   task's dispatch brief frames it.
3. `THEOREM.md`, "Estágio 16" — read for the archive's own framing of what
   the closure attempt closed (`p=1,\dots,10`) and left open (`p>10`,
   "barreira restante é de custo computacional... não de correção
   matemática").

**Reuse policy.** Every script in this directory (`ground_truth.py`,
`ingredients_ext.py`, `odd_part_ext.py`, `assemble_ext.py`) is written
fresh in this directory — none of the closure attempt's or its referee's
own scripts were imported or executed; they were read only for
understanding. **Used as fixed, already-PROVED/CITED input, never
re-derived:** Corollary A3; `Q_p(u)`'s degree/vanishing and Newton's-
identity computation method; the cumulant-generating-function definition
of `\mu_{2l}(N)`; `(E1)`, `(E2)`; the referee's cited `S_{2k-1}(N,m)`
recursion and its inductive all-`k` correctness proof; the full assembly
formula (§2 of the closure attempt, reproduced verbatim in §1 below).

**What is executed here for the first time:** the assembly, for
`p=11,\dots,20`, using two ingredients extracted via faster (but
mathematically identical, cross-validated) routes than the closure
attempt's own — see §2.

**Exploratory timing that motivated the faster routes** (run in
`/tmp/.../scratchpad/`, not part of this directory's non-throwaway record,
but reported here in full per the task's honesty requirements): the
closure attempt's own `central_moment` (`sympy` cumulant-GF series) costs
`12.1s` at `l=10` (`\mu_{20}`, needed for `p=10`, matching the closure
attempt's own reported ~`3.4s` `ingredients.py` runtime being dominated by
smaller `l`'s), `45.5s` at `l=11`, `158.2s` at `l=12` — clearly
intractable for `l=20` (`p=20`) within a reasonable session. The closure
attempt's own `H_reduced_at_b` (`sympy.cancel`) costs `4.5s` at
`\mathrm{power}=19` (`k=10`, needed for `p=10`), `50.4s` at `\mathrm{power}=21`,
`99.2s` at `\mathrm{power}=25`, `171.6s` at `\mathrm{power}=27` — also clearly
intractable for `\mathrm{power}=39` (`k=20`, needed for `p=20`). **This is
exactly the "purely computational, not mathematical" barrier
`THEOREM.md`'s Estágio 16 entry predicted** — and it is a barrier in the
closure attempt's specific *implementation choices*, not in the underlying
mathematics (already proved correct for all `k`), so a faster
implementation of the *same* mathematics was the natural next step, per
the task's own framing.

**Exactness policy.** `sympy.Rational` / `fractions.Fraction` throughout.
No floating point anywhere in this directory's non-throwaway code.

**No randomness.** Every verification here is exact symbolic algebra or an
exhaustive finite sweep; the reserved seed range `20260854000+`
(`DISC-DEC-066`, this front) was not needed and was not used. Confirmed
unused elsewhere in the archive before this document was written
(`grep -rn "20260854" 05_DISCOVERY_LAB/` returns only `DECISION_LEDGER.yaml`'s
and `TEST_QUEUE.yaml`'s own reservation lines for this front).

**Pre-registration.** `DERIVATION_PREREG.md` in this directory was written,
naming the route, the planned honesty checkpoint around the fast-route
substitution, and the exploratory timing that justified it, before any
non-throwaway verification run.

---

## 1. The target and the route, restated (cited, unchanged)

Fix `p\ge0`. Corollary A3 (PROVED, cited, not re-derived):

`\displaystyle D^{*(p)}_r(b):=\sum_{j=p}^{r}c_j^{(r)}(b)\cdot c(j{+}1,\,j{+}1{-}p)`,
`c_j^{(r)}(b):=\dfrac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}`, `c(N,M)` the
unsigned Stirling numbers of the first kind.

The closure attempt's assembly (PROVED given its cited ingredients,
reproduced verbatim, unchanged):

`N:=2r+b+1`, `\beta:=b+1`,

`\displaystyle D^{*(p)}_r(b)=\tfrac12\Big[\Phi_b(r)M_p(N)-\mathrm{Strip}_p(r,b)\Big]-\sum_{k=1}^{p}o_k\,\dfrac{H_{2k-1}(r,b)}{2^{2k-1}}`,

with `Q_p(-(v+\beta/2))=E_p(v)+O_p(v)` (even/odd split), `e_{2l}`,`o_k` its
coefficients, `M_p(N):=\sum_l e_{2l}\mu_{2l}(N)`, `\Phi_b(r):=P_b2^N`,
`\mathrm{Strip}_p(r,b):=\sum_{i=1}^bE_p(i-\beta/2)w_i(r,b)`,
`w_i(r,b):=r!(r{+}b)!/[(r{+}i)!(r{+}b{+}1{-}i)!]`, `H_{2k-1}(r,b):=P_b\,S_{2k-1}(N,r)`.

This front changes nothing about the above. It runs it for `p=11,\dots,20`.

---

## 2. What is executed here for the first time: fast, cross-validated ingredient routes

### 2.1 Central moments `\mu_{2l}(N)`, fast route (`ingredients_ext.py`)

**Same generating function, same Taylor-extraction target** as the closure
attempt (`K(t)=N\log\cosh(t/2)`, `M(t)=e^{K(t)}`, `\mu_{2l}(N)=(2l)![t^{2l}]M(t)`),
computed via the classical power-series-exponentiation recurrence: writing
`f(t):=\log\cosh(t/2)=\sum f_nt^n` (Fraction coefficients, gotten from
`\cosh(t/2)`'s elementary closed-form coefficients `1/((2j)!\,2^{2j})` by
the standard power-series-division-then-integration recipe for `\log` of a
series with constant term `1`), and `h(t):=N f(t)`, then `g(t):=e^{h(t)}`
satisfies `g_0=1`, `m\,g_m=\sum_{k=1}^mk\,h_k\,g_{m-k}` (from `g'=h'g`) — the
same algorithmic class as Newton's identities, exact `Fraction` arithmetic
throughout, no `sympy`, no floating point. `\mu_{2l}(N):=(2l)!\,g_{2l}(N)`.

**Cross-validated against the closure attempt's own slow route**
(`central_moment_slow`, reproduced verbatim in `ingredients_ext.py` for
this purpose only), character-for-character, `l=1,\dots,10`: **`10/10`
match, `0` residual.** Also checked against direct binomial summation,
`l=1,\dots,8`, `72` checks, `0` mismatches, and against the closure
attempt's own printed `\mu_2,\mu_4,\mu_6,\mu_8`: exact match, `4/4`.

**Timing:** the fast route computes `\mu_2,\dots,\mu_{40}` (`l=1,\dots,20`,
covering every `p` up to `20`) in **`0.13s` total** — versus `12.1s`
(`l=10` alone) for the slow route.

### 2.2 `H_k(r,b)` machine, fast route (`odd_part_ext.py`)

**Same `H(\mathrm{power},\mathrm{depth})` recursion** as the closure
attempt (identical formula, reproduced verbatim as `H_symbolic` for
cross-validation), extracted via evaluation at concrete, sufficiently-large
integer `r` (an offset chosen so no intermediate `\mathrm{falling}(N,\mathrm{depth})`
is zero) plus exact Newton-divided-difference interpolation, using the
empirically-confirmed degree pattern `\deg_rH_{2k-1}(r,b)=k-1` — with a
built-in self-consistency check (extra held-out evaluation points,
verified to match the interpolated polynomial on every call) that would
immediately raise if the degree assumption were ever wrong.

**Why this is safe beyond the cross-validation below:** the closure
attempt's own referee proved, by induction, that `H(\mathrm{power},\mathrm{depth})`
[[as literally defined by the recursion]] equals `P_b\cdot S_{\mathrm{power}}(N-d,r-d)`
for **every** `(\mathrm{power},d)` — a fact about the recursion's
mathematical content, independent of how a downstream script extracts its
polynomial coefficients. The interpolation route evaluates the identical
recursion at concrete points; it cannot silently diverge from the slow
route's output except by an interpolation-degree error, which the
self-check catches on every single call.

**Cross-validated against the closure attempt's own slow route**
(`H_reduced_at_b_slow`, `sympy.cancel`), character-for-character,
`\mathrm{power}=1,3,\dots,19` (`k=1,\dots,10`) at `b\in\{0,1,2,5,8\}`:
**`50/50` match, `0` residual.** Also checked against brute-force direct
summation of `P_b\cdot S_{\mathrm{power}}(N,r)`, `\mathrm{power}=1,\dots,21`
(`k=1,\dots,11`), `r\le10,b\le6`: `847` checks, `0` mismatches. Also
matches the closure attempt's own printed `k=1,2,3,4` brackets exactly.

**Timing:** the fast route computes `H_1,H_3,\dots,H_{39}` (`k=1,\dots,20`,
covering every `p` up to `20`) at `b=1` in **`0.36s` total** — the single
slowest individual value (`\mathrm{power}=39`, `k=20`) taking `0.076s` —
versus `171.6s` for `\mathrm{power}=27` (`k=14`) alone via the slow route,
which never reached `\mathrm{power}=39` in the exploratory timing before it
was abandoned as intractable.

### 2.3 `Q_p(u)`, UNCHANGED (needs no speed-up)

Newton's-identity computation (identical to the closure attempt) remains
fast through `p=20`: `1.72s` total for `Q_1,\dots,Q_{20}` (the single
slowest, `Q_{20}`, `0.28s`). No performance variant needed for this
ingredient; re-verified against direct `e_p(1,\dots,u)` evaluation,
`p=0,\dots,8`, `225` checks, `0` mismatches.

### 2.4 Honest process note: a self-caught bug, distinct from the `w_i` off-by-one

The task explicitly asked this front to watch for a *recurrence* of the
closure attempt's disclosed `w_i(r,b)` off-by-one class. That specific bug
class did **not** recur: `w_i(r,b)` was written directly in the
already-corrected form from the start and independently re-verified
against the elementary factorial identity `w_i(r,b)=r!(r{+}b)!/[(r{+}i)!(r{+}b{+}1{-}i)!]`
at `r\le15,b\le10`: `880` checks, `0` mismatches (`assemble_ext.py`,
`verify_w_i_correctness`, run **before** any assembly result is trusted).

A **different** bug was caught, in code copied verbatim from the closure
attempt's `D_star_predicted`: its final line, `return
sp.nsimplify(vc*varphi_r_val+rem)`, silently corrupts an exact,
already-fully-reduced `sp.Rational` once the numerator/denominator get
large — e.g. at `p=3,r=15,b=0`, the true value
`1143904849/80144052` was returned by `sp.nsimplify` as
`3\cdot2^{269/341}3^{57/682}5^{290/341}7^{329/682}/4`, a spurious
irrational-looking expression produced by `nsimplify`'s float-based
algebraic-constant-guessing algorithm losing precision on a large exact
rational. This was **caught by exactly the discipline the task asked
for**: a calibration sweep (`p=1,\dots,4` reproduced against ground truth
at a spread of `(r,b)`) failed loudly (`2/16` mismatches, both at `r=15`,
the largest `r` tested) rather than silently. It had never been caught in
the closure attempt itself because `D_star_predicted` was defined there
but never actually invoked in that document's own `__main__` — a dormant,
previously-unexercised latent bug, exposed here only because this front
uses that function for an end-to-end symbolic-route sanity gate before
trusting the fast ingredients. **Fix:** drop the `nsimplify` call entirely
— the substituted value is already exact `sp.Rational` arithmetic and
needs no "simplification". Re-run after the fix: `0/16` calibration
mismatches (§4). No other component (`w_i`, `Q_p`, the fast moments, the
fast `H_k`, `(E1)`, `(E2)`) exhibited any error at any point.

**Could this recur at higher `p`?** The bug is `p`-independent in its
mechanism (it is triggered purely by the *size* of the rational, via
`varphi_r_val`'s numerator/denominator growing with `r`, not by `p` at
all) — so it was equally latent at `p=1` as at `p=20`; it was simply never
exercised before. `check_against_ground_truth` (the actual production
verification route used for the `62\,310`-check sweep in §4) never called
`D_star_predicted` or `nsimplify` at all — it works entirely in
`fractions.Fraction`, immune to this class of issue by construction. This
bug therefore affected **only** the small (`16`-point) calibration
sanity-gate, not the main verification sweep, and was fixed before that
sweep ran.

---

## 3. Assembly and independent ground truth

`ground_truth.py`: independent, from-scratch Corollary A3 implementation
(own unsigned-Stirling recurrence), matching every PROVED calibration
formula available (`p=1,2` at `b=0`, `p=1,4` at `b=1`) and the `r<p`
vanishing boundary extended through `p=20`: `1044+120=1164` checks (see
`ground_truth.log`), `0` fails.

`assemble_ext.py` builds the assembly two ways, exactly mirroring the
closure attempt's own dual-route design: a `sympy`-symbolic route
(`D_formula_symbolic_r`, produces the printed closed forms below) and a
pure-`fractions.Fraction` route (`check_against_ground_truth`, using the
fast Fraction-coefficient-list ingredients from §2 directly, with no
`sympy` round-trip in the hot loop) — both checked against `ground_truth.py`.

### 3.1 Calibration: reproduces `p\le4` exactly (sanity gate before trusting `p=11..20`)

`D_star_predicted` (symbolic route, using the fast ingredients), spot-
checked against `ground_truth.D_star` for `p=1,2,3,4`, `r\in\{0,3,7,15\}`,
`b\in\{0,1,2,3\}`: **`64/64` exact match, `0` fails** (post-fix; see §2.4
for the one bug found and fixed along the way).

### 3.2 Exhaustive verification against ground truth, `p=11,\dots,20`

`check_against_ground_truth`, checked against `ground_truth.py`:

| `p` | `r` range | `b` range | checks | fails | time |
|---|---|---|---|---|---|
| 11 | 0..200 | 0..30 | 6231 | 0 | 13.8s |
| 12 | 0..200 | 0..30 | 6231 | 0 | 14.3s |
| 13 | 0..200 | 0..30 | 6231 | 0 | 14.6s |
| 14 | 0..200 | 0..30 | 6231 | 0 | 15.9s |
| 15 | 0..200 | 0..30 | 6231 | 0 | 14.6s |
| 16 | 0..200 | 0..30 | 6231 | 0 | 17.7s |
| 17 | 0..200 | 0..30 | 6231 | 0 | 16.5s |
| 18 | 0..200 | 0..30 | 6231 | 0 | 19.7s |
| 19 | 0..200 | 0..30 | 6231 | 0 | 22.3s |
| 20 | 0..200 | 0..30 | 6231 | 0 | 23.6s |

**Total: `62 310` checks, `0` fails.** Every row uses `r=0,\dots,200`,
`b=0,\dots,30` — the **same scale for all ten new `p` values**, matching
the largest scale ever reached anywhere in this lineage (the wave-15
referee's own `p=5,6` push, previously the ceiling of this whole family of
documents), not scaled down as `p` grows. The `r<p` boundary (Corollary
A3's empty-sum region) is included in every row (`r` starts at `0`) and
passes throughout — the assembled formula's own algebra forces this, it is
not separately coded.

### 3.3 New explicit closed forms, `p=11,\dots,20`

Printed by `assemble_ext.py` (raw sum-of-monomials form, not
`sympy.factor`-compressed — the closure attempt's `p=5,6,7` forms were
printed factored, but factoring a degree-`\sim2p` numerator over `\mathbb Q`
becomes unwieldy to typeset correctly by hand at `p\ge11`; the exact,
unfactored polynomial is preferred here over risking a transcription error
in a hand-copied factorization). Full list (`b=0,1` for every
`p=11,\dots,20`, plus `b=2,3` for `p=11,15,20`) in `assemble_ext.log`.
`p=11` (the smallest of the new range, still large — degree-`10`/`11`
numerators) is printed here in full as the representative instance; `p=15,20`
are far larger (degree up to `19`/`20`, coefficients up to `20`+ digits) and
are reported only by reference to the log, per the same "don't hand-transcribe
what can't be checked by eye" principle:

`\displaystyle D^{*(11)}_r(0)=\frac{r(3968055r^{10}+862579575r^9+15274070240r^8+12844616070r^7-94363958117r^6+125447834919r^5-46985095850r^4-25898862660r^3+20435271032r^2-825938784r-754686720)}{48318382080}\varphi_r`
`\displaystyle\qquad-\frac{r^2(51975r^8+2735964r^7+14988974r^6-34308120r^5+5427335r^4+59050476r^3-77632828r^2+39528912r-7181568)}{31933440}`,

`\displaystyle D^{*(11)}_r(1)=\frac{(r{+}1)(3968055r^{10}+1193250825r^9+39799547450r^8+337950639650r^7+1010897391023r^6+1555995024809r^5+1599826247600r^4+1068617462060r^3+451546690992r^2+111372936576r+12079595520)}{48318382080}\varphi_r`
`\displaystyle\qquad-\frac{(r{+}1)(239085r^9+19592496r^8+308006930r^7+1414191240r^6+2596553381r^5+2992650984r^4+2239033244r^3+1031665248r^2+274064832r+31933440)}{127733760}`,

`\displaystyle D^{*(11)}_r(2)=\frac{(r{+}2)(3968055r^{11}+1575506790r^{10}+82248351185r^9+1412647842320r^8+11320053472013r^7+51274410030926r^6+145424146304231r^5+270717635178860r^4+333323123562372r^3+262972781793744r^2+120956406724224r+24751091220480)}{24159191040(2r{+}3)}\varphi_r`
`\displaystyle\qquad-\frac{(r{+}2)(135135r^{10}+15711003r^9+432939430r^8+4704949942r^7+26103581407r^6+85587718795r^5+178090518652r^4+240016007524r^3+204389630496r^2+100471023936r+21810539520)}{63866880(r{+}1)}`.

Every `b=0,1` instance across all ten new `p` (checked in the full
`assemble_ext.log` listing) has a polynomial (not merely
polynomial-times-`\varphi_r`) remainder and a `\varphi_r`-coefficient with
**no** `(2r+3)` denominator — matching the `b\in\{0,1\}` pattern established
at `p\le10`. Every `b=2,3` instance checked (`p=11,15,20`) carries the
`(2r+3)` denominator pattern (and, at `b=3`, the additional `(r+1)(r+2)`
remainder-denominator factor) — confirming the structural signature the
closure attempt identified persists through `p=20`, by direct construction,
not by analogy.

---

## 4. What this closes, precisely

**The general-`p` closed-form algorithm for `D^{*(p)}_r(b)` is now executed
and verified for `p=1,\dots,20`, every `b\ge0`** — doubling the range
closed by the closure attempt (`p=1,\dots,10`), using the identical
algorithm and identical cited ingredients, extracted via faster
(cross-validated) routes for two of the four ingredients. Concretely:

- The closure attempt's `p=1,\dots,4` results are reproduced exactly by
  this front's fast-ingredient implementation (§3.1, §2.4).
- **New closed forms for `p=11,\dots,20` — the mandate's full target
  range — are produced and verified at the largest scale reached anywhere
  in this lineage, uniformly across all ten values** (§3.2, §3.3).
- The exploratory timing (§0) confirms `THEOREM.md`'s Estágio 16
  prediction was correct in substance (the `p>10` barrier was purely
  computational) and additionally shows that barrier was specific to the
  closure attempt's *implementation choices*, not an inherent property of
  the underlying mathematics — a faster (but unchanged-in-content)
  extraction of the same two generating objects removes it through at
  least `p=20`.

## 5. What remains open, precisely

1. **`p>20` was not attempted.** This document's fast-route timing data
   (§2.1, §2.2 — both ingredients still comfortably sub-second even at
   `\mathrm{power}=39`/`l=20`, with no sign of the steep growth that
   afflicted the slow routes) is evidence that `p=21,\dots,30` or beyond
   would likely also be tractable with the same fast routes, but this is
   **not demonstrated** — no run was made past `p=20`, and no claim is
   made about where the fast routes' own growth eventually becomes a
   problem (Newton-divided-difference interpolation is `O(\mathrm{npts}^2)`
   in the number of sample points, and the power-series-exponentiation
   recurrence is `O(\mathrm{order}^3)`-ish; both are polynomial, not
   exponential, in `p`, but "polynomial and fast in practice through
   `p=20`" is not a proof of tractability at, say, `p=100`). A future
   front wanting `p>20` should re-time both fast routes at the powers it
   would actually need before assuming they remain free.
2. **No single elementary formula with `p` as a free symbolic variable is
   produced or believed to exist**, unchanged from the closure attempt's
   own position (§5 item 1 there) — `Q_p(u)` has genuine degree `2p`.
3. **The strip sum is still an explicit `b`-term sum**, unchanged, by
   design, from every predecessor in this lineage.
4. **No independent adversarial re-verification of this document has been
   performed.** Per standing archive discipline and the task's explicit
   instructions, referee dispatch is out of scope for this front and is
   reserved for the orchestrating session. §6 names what a referee should
   attack first.
5. **It does not change the status of anything already catalogued.**
   Corollary A3, the closure attempt's `p=1,\dots,10` results, and every
   PROVED calibration formula quoted here are reproduced exactly, not
   superseded or weakened.

---

## 6. What a hostile referee should attack first

- **§2.1, §2.2 — the two fast-route re-implementations.** These are the
  only genuinely new pieces of engineering in this document (everything
  else is a verbatim re-use of the closure attempt's cited mathematics). A
  referee should independently re-derive the power-series-exponentiation
  recurrence (one line, classical) and the interpolation route's degree
  bound (`\deg_rH_{2k-1}(r,b)=k-1`, empirically confirmed but not proved
  here from first principles — a referee with more time could try to prove
  it directly from the `H(\mathrm{power},\mathrm{depth})` recursion's
  structure, e.g. by induction on depth mirroring the wave-15 referee's
  own induction), and re-check both fast routes against the slow routes at
  a handful of `(p,b)` values not already checked here.
- **§2.4's self-caught `nsimplify` bug, and whether the fix is complete.**
  A referee should confirm `check_against_ground_truth` (the actual
  production verification route for the `62\,310`-check sweep) never calls
  `sp.nsimplify` anywhere in its call graph (it does not — grep
  `assemble_ext.py` for `nsimplify`; the only call site left is inside
  `sp_to_fraction`'s conditional branch, guarded by `not (x.is_Rational or
  x.is_Integer)`, which never fires for the already-fully-substituted
  Rational inputs `check_against_ground_truth` produces internally — but a
  referee should verify this claim directly rather than trusting the
  description).
- **Whether the `r,b=0..200,0..30` scale is truly uniform coverage or
  hides a boundary effect.** A referee with more compute budget could push
  `p=20` specifically further (e.g. `r=300`) to further rule out a
  scale-dependent failure mode, mirroring the wave-15 referee's own
  scale-push methodology for `p=5,6`.
- **Whether the `H_k` interpolation route's self-consistency check is a
  genuine safeguard or could be fooled.** The held-out points are chosen
  close to the sample points (`\mathrm{offset}+\mathrm{npts}+j+5`); a
  referee could check whether a *wrong* degree guess could still pass the
  self-check by coincidence (e.g. if the true polynomial happened to agree
  with a wrong-degree interpolant at those specific extra points) — this
  was not separately stress-tested here beyond the direct cross-validation
  against the slow route (§2.2), which is the actually load-bearing
  safeguard.

---

## 7. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Fast central-moment route (`\mu_{2l}(N)`, power-series-exponentiation recurrence) | **PROVED** (classical algorithm) + cross-validated character-for-character vs. the closure attempt's slow route, `l=1..10`, `0`/`10` mismatches; vs. direct summation, `72` checks, `0` fails |
| 2 | Fast `H_k(r,b)` route (evaluate-then-interpolate) | **PROVED given the wave-15 referee's `H` induction** (cited) + cross-validated vs. the closure attempt's slow route, `power=1..19`×`5` `b` values, `50/50` match; vs. brute force, `847` checks, `0` fails |
| 3 | `Q_p(u)`, unchanged, needs no speed-up | **PROVED** (unchanged from closure attempt), re-verified, `225` checks, `0` fails |
| 4 | `w_i(r,b)` — the disclosed off-by-one class did NOT recur | **CONFIRMED**, `880` checks, `0` fails (checked BEFORE trusting any assembly, per the task's instruction) |
| 5 | Self-caught `nsimplify` bug in `D_star_predicted`, found and fixed | **DISCLOSED**, fixed, re-verified (§2.4, §3.1) |
| 6 | Calibration: reproduces closure attempt's `p=1..4` | **CONFIRMED**, `64/64`, `0` fails (post-fix) |
| 7 | General-`p` assembly, `p=11,\dots,20`, every `b\ge0`, `r\le200,b\le30` | **PROVED given items 1-3 and the closure attempt's cited ingredients**; `62\,310` exact checks vs. independent ground truth, `0` fails |
| 8 | New closed forms, `p=11,\dots,20` | **PROVED** (algorithm) + **NUMERICALLY VERIFIED at the largest scale reached anywhere in this lineage**, uniformly |
| 9 | `p>20` | **OPEN** — not attempted; the fast routes' own timing data (§2.1,§2.2) suggests, but does not prove, this remains tractable |
| 10 | A single symbolic-in-`p` elementary formula | **NOT CLAIMED, believed not to exist in elementary form** — unchanged from the closure attempt |
| 11 | Independent adversarial re-verification of this document | **NOT PERFORMED** — out of scope for this front, reserved for the orchestrating session |

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-070`] Revisão
> adversarial concluída: veredito **SOUND — ACCEPT for catalogue**,
> `75.899` checagens independentes do referee, `0` divergências,
> incluindo replicação integral do grid de `62.310` pontos por
> pipeline próprio sem `sympy` e push de escala a `r=300` em
> `p=15,20`. Três atualizações a este documento: **(i)** a cota de
> grau `\deg_r H_{2k-1}(r,b)=k-1` (§2.2), aqui empírica, foi
> **PROVADA pelo referee** (coeficiente líder `4^{k-1}(k-1)!`,
> independente de `b`, via a fatoração `S_{2k-1}=A_k\cdot C(N,m+1)`
> derivada da recursão aceita) — a linha 2 do scorecard deve ser lida
> como PROVED sem ressalva empírica, com crédito ao referee; **(ii)**
> o tally "1044+120=1164" do §3 sub-conta as checagens do próprio
> `ground_truth.log` (omite a linha de calibração `b=1`) — a contagem
> é um sub-relato, na direção segura; **(iii)** o self-check da
> interpolação foi provado determinístico pelo referee (um grau
> sub-estimado é capturado por qualquer ponto held-out; `36/36` em
> testes de ajuste deliberadamente errado), respondendo à pergunta
> que o §6 deixara ao referee. Integrado como "Estágio 21" em
> `THEOREM.md`. Ver `adversarial/REFEREE_REPORT.md`.

**Net honest verdict.** The mandate's full target (`p=11,\dots,20`) was
reached, at the largest verification scale used anywhere in this lineage,
uniformly across all ten new values — not a shrinking-scale fallback. This
was possible because the genuine computational wall the closure attempt's
own (slow) routes would have hit was specific to *how* two ingredients
were extracted from their generating objects, not to the underlying
mathematics (already proved correct for all `k` by the wave-15 referee's
induction) — and a faster, cross-validated extraction of those same two
objects removed the wall entirely through `p=20`. One genuine bug was
found and disclosed along the way (§2.4), in previously-dormant code, via
exactly the discipline the task asked for (a sweep failing loudly rather
than silently). The one substantive limitation is scope, not soundness:
`p>20` was not attempted, and this document's own timing data is
suggestive but not dispositive about how far the fast routes would
continue to work past `p=20`.

---

## 8. Seeds

No randomness was used anywhere in this document; the reserved seed range
`20260854000+` (`DISC-DEC-066`, this front) was not needed. Every check in
this directory is exact symbolic algebra or an exhaustive finite sweep
over a stated integer range.

---

## 9. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any non-throwaway verification run | — |
| `ground_truth.py` / `.log` | independent Corollary A3 implementation, own Stirling table, smoke tests | ~0.1s |
| `ingredients_ext.py` / `.log` | `Q_p(u)` (unchanged), fast central moments (power-series-exponentiation recurrence), cross-validated vs. the closure attempt's slow route and direct summation | ~21s (dominated by the slow-route cross-validation calls, kept only for validation; the fast route itself is `0.13s` for every `l` up to `20`) |
| `odd_part_ext.py` / `.log` | fast `H_k(r,b)` (evaluate-then-interpolate), cross-validated vs. the closure attempt's slow route and brute force | ~71s (dominated by the slow-route/brute-force cross-validation calls, kept only for validation; the fast route itself is `0.36s` for every `k` up to `20`) |
| `assemble_ext.py` / `.log` | full general-`p` assembly, `p=11..20`; `w_i` re-verification; calibration; exhaustive ground-truth sweeps (`62 310` checks); printed closed forms | ~3 min (sweep alone: `173`–`180s` across two independent full runs, reproducing identical check counts and closed forms both times, only wall-clock timings differing — see §3.2; the rest is `sympy` printing/formatting of the closed forms) |
| `ATTEMPT.md` | this document | — |

Reproduce in order: `python3 ground_truth.py`; `python3 ingredients_ext.py`;
`python3 odd_part_ext.py`; `python3 assemble_ext.py`. Total well under 10
minutes.
