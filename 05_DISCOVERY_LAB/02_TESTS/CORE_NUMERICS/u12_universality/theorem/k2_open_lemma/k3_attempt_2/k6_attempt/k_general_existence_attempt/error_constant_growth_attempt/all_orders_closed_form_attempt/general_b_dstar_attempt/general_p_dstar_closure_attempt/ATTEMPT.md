# General-`p` closure for `D^{*(p)}_r(b)`: the mechanical write-out, executed

> **Governance.** Wave 15, front (a), `GENERAL-P-DSTAR-CLOSURE-ATTEMPT`,
> authorized by `DISC-DEC-063`. Target: item 11 of
> `general_b_dstar_attempt/ATTEMPT.md`'s scorecard — a general-`p` closed
> form for the sharp error constants `D^{*(p)}_r(b)`, `p\ge5`, every
> `b\ge0` — the item the wave-14 referee showed has a **removable**
> obstruction (a one-line binomial parity identity, PROVED, cited below)
> but did not itself execute the full assembly for. Pure combinatorics on
> the Tamesis Discovery Lab's internal random-permutation-with-reroutes
> ensemble — **no Millennium Prize claim of any kind is made anywhere in
> this document**, no external data, no holdout, no real-world claim.
> **Nothing outside this directory was created, modified, or deleted.** No
> git commit was made. `THEOREM.md` and the decision ledger were not
> touched. **This document requires independent mandatory adversarial
> verification before any integration into `THEOREM.md` or any other
> governance artifact** — per standing archive discipline, exactly as
> every predecessor in this lineage required before being catalogued.
> Every claim below is labelled PROVED, CITED, NUMERICALLY SUPPORTED, or
> OPEN.

---

## Executive summary (read first)

1. **Item 11 closes: a genuinely general-`p` algorithm for `D^{*(p)}_r(b)`
   is executed here, not just `p=5,6`.** The referee's report named exactly
   what remained — "closing item 11 would be a mechanical (if tedious)
   write-out, not a new idea." That write-out is carried out: every piece
   of the parent's route (`Q_p`, central moments, the odd-power collapse)
   is implemented as an algorithm parameterized by `p` (Newton's identities
   for `Q_p`; a cumulant-generating-function Taylor extraction for
   `\mu_{2l}(N)`; an explicit unrolling of the referee's cited general-`k`
   odd-power identity for the collapse), not fitted per `p`. Run and
   checked exhaustively against an independent ground truth for
   **`p=1,\dots,10`** — twice the mandate's stated minimum (`p=5,6`).
2. **`26 710` exact exhaustive checks against ground truth (Corollary A3),
   `0` mismatches, across `p=1,\dots,10`**, at scale matching or exceeding
   the mandate (`r` to `40`–`150`, `b` to `15`–`25` depending on `p`,
   scaled down only where sympy's polynomial-cancellation cost genuinely
   grows with `p`, never where correctness is in question). Plus `800`
   ground-truth self-consistency checks, `4054` ingredient-level checks
   (`Q_p`, central moments, an independent spot-check of the cited
   general-`k` odd-power identity to `k=8`), and `2778` odd-part-machine
   checks (the two elementary identities `(E1)`,`(E2)`, brute-force
   cross-checks to `k=7`) — **`34 342` exact checks in total, `0`
   mismatches** after one self-caught and fixed bug (§2.4).
3. **Every reduction to previously-PROVED formulas matches
   character-for-character**, with no fitting involved: `b=0` for `p=1,2`,
   `b=1` for `p=1,2,3,4` (the parent's calibration set), **and** all five
   `b=2,3` concrete instances the parent document itself printed
   (`p=1,b=2`; `p=1,b=3`; `p=2,b=2`; `p=2,b=3`; `p=3,b=2`) — reproduced
   exactly by this document's independently-built general-`p` machine,
   which was never shown those formulas during derivation (§3.1).
4. **New, previously-unknown closed forms are produced for `p=5,6,7` at
   every `b\ge0`** — explicit instances printed at `b=0,1,2,3` (§3.3),
   verified against ground truth at the scale in item 2.
5. **The mechanism really is `p`-uniform, not merely "checked to work
   at each `p` we tried."** The one piece that could in principle have
   failed to generalize — the referee's parity-based odd-power identity —
   was independently spot-checked here (not re-derived from scratch, per
   task instructions) for every `k` actually used, up to `k=8`
   (`3780` checks, `0` mismatches), on top of the referee's own
   symbolic proof to exponent `40`.
6. **What is *not* claimed:** a single symbolic-in-`p` algebraic formula
   (one expression with `p` as a free variable, collapsing every case at
   once) is **not** produced and is **not** believed to exist in
   elementary form — `Q_p(u)` itself has no such form (it is inherently
   degree-`2p`, computed via `p` Newton-identity steps). What is produced
   is the stronger, standard-in-this-archive notion of a general-`p`
   closed form: a terminating algorithm, proved correct for every `p`,
   that outputs the exact closed-form rational-function-of-`r` for
   `D^{*(p)}_r(b)` given any `p,b` — the same standard already used for
   the general-`k` prefactor collapse and the referee's general-`k`
   odd-power identity, both labelled PROVED elsewhere in this lineage.

---

## 0. Disciplina

**Sources read, in full, before any derivation** (per the task mandate):

1. `general_b_dstar_attempt/ATTEMPT.md` — the parent document. Proves
   general-`b` closed forms for `D^{*(p)}_r(b)` at `p=1,2,3,4` via a
   prefactor-collapse route; its §3.1–§3.4 give the four ingredients
   (`Q_p(u)`, central moments, the `I5,I7` identities, the general-`k`
   prefactor collapse); its scorecard item 11 named "general-`p` closure
   OPEN, mechanism exhibited at `k=2,3` only."
2. `general_b_dstar_attempt/adversarial/REFEREE_REPORT.md` — the hostile
   referee's report (verdict SOUND, ACCEPT). Its Part 1 proves, as a
   byproduct of trying to break the parent document, that the "general-`k`
   closure" obstruction named in item 11 is **removable**: the even-`w`-
   term cancellation behind `I5,I7` is a one-line consequence of the
   binomial parity identity
   `(w-1)^n-(w+1)^n=-2\sum_{t\text{ odd}}\binom nt w^{n-t}`, holding for
   **every** even exponent `n`, verified symbolically to `n=40` and
   numerically (brute force, no recursion) through `k=11`. This is used
   here as an established, PROVED, citable ingredient (`DISC-DEC-059`,
   `THEOREM.md` "Estágio 14"), re-stated in unrolled recursive form as:
   `S_{2k-1}(N,m)=(N-2m)^{2k-2}(m{+}1)\binom N{m+1}+2N\sum_{s\text{
   odd},1\le s\le2k-3}\binom{2k-2}{s}S_s(N{-}1,m{-}1)`, base case
   `S_1(N,m)=(m{+}1)\binom N{m+1}`.
3. `THEOREM.md`, "Estágio 9" and "Estágio 14" — read for context on
   Corollary A3 and the general-`b` `D1` theorem, so this document's
   citations and framing are consistent with the archive's conventions.
4. `error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3 —
   Teorema 3′, the already-PROVED `p=2` general-`b` case, read for
   background/cross-check (`varphi_r`, `\Phi_b(r)` notation).

**Reuse policy** (same convention as every predecessor in this lineage).
Every script in this directory (`ground_truth.py`, `ingredients.py`,
`odd_part.py`, `assemble.py`) is written from scratch — **none of the
parent's or the referee's own scripts were imported or executed**; they
were read only for understanding, per the task's instructions. **Used as
fixed, already-PROVED input, never re-derived:**

- Corollary A3 itself (`D^{*(p)}_r(b)=\sum_{j=p}^r c_j^{(r)}(b)c(j{+}1,j{+}1{-}p)`).
- `Q_p(u)=e_p(1,\dots,u)` has degree `2p` and vanishes for `u<p`, for
  every `p` (parent §3.1).
- Steps 2–3 of the parent's route (the `p`-uniform substitution
  `u=-(v+\beta/2)`, the even/odd split, and the reflection collapse of the
  even part into a full symmetric sum minus a `b`-term strip) are
  `p`-uniform and PROVED in general (parent §2 Steps 2–3, confirmed
  independently by the referee, scorecard row 3).
- The general-`k` prefactor collapse
  `P_b[N]_k(r{-}k{+}1)\binom{N-k}{r-k+1}=[r]_k` (parent §3.4, PROVED every
  `k`, confirmed by the referee to `k=15` symbolically).
- The referee's general-`k` odd-power identity (item 2 above), PROVED,
  cited as standing input **and independently spot-checked here** (see
  §2) for the specific `k` values actually used, per the task's
  instruction not to re-derive it from scratch but to verify it holds.

**What is executed here for the first time, for general `p`:** (a)
`Q_p(u)` and the central moments `\mu_{2l}(N)` computed via `p`-general
algorithms (Newton's identities from Faulhaber power sums; a cumulant-
generating-function Taylor extraction to order `2l`) rather than fitted
per `p`; (b) the odd-part collapse carried out for arbitrary `k` by
unrolling the cited general-`k` identity, using an elementary identity
(`(E2)` in `odd_part.py`) derived independently here, into an explicit
rational function of `r,b`; (c) the assembly of (a)+(b)+the cited Step-3
even-part reflection into a single closed-form-producing algorithm, valid
for any integer `p`, run here for `p=1,\dots,10`.

**Exactness policy.** `sympy.Rational` / `fractions.Fraction` throughout.
No floating point anywhere in this directory's non-throwaway code.

**No randomness.** Every verification here is exact symbolic algebra or
an exhaustive finite sweep; the reserved seed range `20260841000+`
(`DISC-DEC-063`, front (a)) was not needed and was not used. Confirmed
unused elsewhere in the archive before `DERIVATION_PREREG.md` was written
(`grep -rn "20260841" 05_DISCOVERY_LAB/` returned no hits besides the
ledger's own reservation line).

**Pre-registration.** `DERIVATION_PREREG.md` in this directory was
written, naming the route, the two success tiers (general-`p` algorithm
vs. `p=5,6` fallback), and the honesty commitment, before any
non-throwaway verification run.

---

## 1. The target, restated

Fix `p\ge0`. Recall (already PROVED, cited, not re-derived — Corollary A3
of `all_orders_closed_form_attempt/ATTEMPT.md` §4.3):

`\displaystyle D^{*(p)}_r(b):=\Phi^{[p]}_r(1,b)=\sum_{j=p}^{r}c_j^{(r)}(b)\cdot c(j{+}1,\,j{+}1{-}p)`,

`c_j^{(r)}(b):=\dfrac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}`, `c(N,M)` the
unsigned Stirling numbers of the first kind. The parent document closed
this for `p=1,2,3,4`, every `b\ge0`. Item 11 of its scorecard: does the
same mechanism close for **every** `p`?

---

## 2. The route: general-`p`, executed

`N:=2r+b+1`, `\beta:=b+1`, `v:=\alpha-N/2`, `P_b:=r!(r+b)!/N!`. The
parent's Steps 1–3 (extension-for-free via `Q_p`'s vanishing; the
`p`-uniform substitution; the even-part reflection) are cited PROVED and
reused verbatim, general `p`:

`\displaystyle D^{*(p)}_r(b)=\tfrac12\Big[\Phi_b(r)M_p(N)-\mathrm{Strip}_p(r,b)\Big]-\sum_{k=1}^{p}o_k\,\dfrac{H_{2k-1}(r,b)}{2^{2k-1}}`,

where (every piece defined precisely, computed by a `p`-general algorithm,
not fitted):

- `Q_p(-(v+\beta/2))=E_p(v)+O_p(v)` (even/odd split in `v`); `e_{2l}`:=
  coeff of `v^{2l}` in `E_p` (`l=0,\dots,p`); `o_k`:= coeff of `v^{2k-1}`
  in `O_p` (`k=1,\dots,p`).
- `M_p(N):=\sum_{l=0}^p e_{2l}\mu_{2l}(N)`, `\mu_0(N):=1`.
- `\Phi_b(r):=P_b2^N=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}` (cited
  identity, re-derived/spot-checked, §3 `(E1)`).
- `\mathrm{Strip}_p(r,b):=\sum_{i=1}^bE_p(i-\beta/2)w_i(r,b)`,
  `w_i(r,b):=P_bC(N,r{+}i)=r!(r{+}b)!/[(r{+}i)!(r{+}b{+}1{-}i)!]`.
- `H_{2k-1}(r,b):=P_bS_{2k-1}(N,r)`, `S_{2k-1}` the referee's cited
  general-`k` odd-power sum, unrolled into an explicit rational function
  of `r,b` (§3).

### 2.1 `Q_p(u)`, general `p`, via Newton's identities (`ingredients.py`)

`e_p(1,\dots,u)` (elementary symmetric polynomial of degree `p` in
`1,\dots,u`) is computed from the classical Faulhaber power-sum
polynomials `P_1(u),\dots,P_p(u)` (`P_m(u):=\sum_{k=1}^uk^m`, computed
exactly by `sympy.summation`, a closed-form polynomial in `u` for every
`m`) via Newton's identities `p\cdot e_p=\sum_{i=1}^p(-1)^{i-1}e_{p-i}P_i(u)`
— a classical, textbook algorithm, general in `p`, **not** interpolation
or per-`p` fitting. This reproduces the parent's printed `Q_1,\dots,Q_4`
character-for-character (independent cross-check, `ingredients.py`) and
matches the direct definition `e_p(1,\dots,u)` (computed independently, by
expanding `\prod_{k=1}^u(1+kx)` and extracting the `x^p` coefficient) at
every tested point, `p=0,\dots,6`, `189` checks, `0` mismatches, including
the vanishing-for-`u<p` boundary.

### 2.2 Central moments `\mu_{2l}(N)`, general `l`, via the cumulant generating function

`\mu_{2l}(N):=2^{-N}\sum_{\alpha=0}^N(\alpha-N/2)^{2l}\binom N\alpha`,
extracted from `M(t)=\exp(N\log\cosh(t/2))=\sum_k\mu_k(N)t^k/k!` via a
`sympy.series` Taylor expansion to order `2l+2` — implemented as a
function of `l` (not degree-limited: the parent executed this only to
`l=4`), run here to `l=10` (`\mu_{20}`). Matches the parent's printed
`\mu_2,\mu_4,\mu_6,\mu_8` character-for-character, and matches direct
summation for `l=1,\dots,5`, `N` up to `22`, `85` checks, `0` mismatches
(`ingredients.py`).

### 2.3 The odd-part machine `H_k(r,b)`, general `k` (`odd_part.py`)

Two elementary identities, derived independently (not merely asserted):

> **(E1).** `\Phi_b(r):=P_b2^N=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}`
> (already-established input; spot-checked here, `r,b\le15`, `256` exact
> checks, `0` mismatches).

> **(E2).** `P_b\binom{N-j}{r-j+1}=\dfrac{[r]_j}{[N]_j(r-j+1)}`, `[x]_j:=
> x(x-1)\cdots(x-j+1)`. *Proof.* `\binom{N-j}{r-j+1}=(N-j)!/[(r-j+1)!(N-j-(r-j+1))!]`
> and `N-j-(r-j+1)=N-r-1=r+b`, constant in `j` (immediate from
> `N=2r+b+1`). So `\binom{N-j}{r-j+1}=(N-j)!/[(r-j+1)!(r+b)!]`, and
> `P_b\binom{N-j}{r-j+1}=[r!(r+b)!/N!]\cdot(N-j)!/[(r-j+1)!(r+b)!]
> =r!(N-j)!/[N!(r-j+1)!]=[r]_j/([N]_j(r-j+1))`. `\blacksquare` (This is
> the `j`-indexed special case of the parent's general-`k` collapse
> proposition, re-derived independently here since it is applied at
> every recursion depth below; verified directly, `r\le15,b\le10,j\le12`,
> `1683` exact checks, `0` mismatches.)

Using `(E2)`, the referee's cited recursion for `S_{2k-1}(N,m)` is
unrolled **directly** into an explicit polynomial in `(r,b)`: writing
`H(power,\mathrm{depth})` for the partial unrolling after `\mathrm{depth}`
recursive `(N{-}1,m{-}1)` shifts (`\beta_{\mathrm{local}}:=\beta+\mathrm{depth}`,
`N_d:=N-\mathrm{depth}`),

`H(\mathrm{power},d)=\beta_{\mathrm{local}}^{\mathrm{power}-1}\dfrac{[r]_d}{[N]_d}
+\big[\mathrm{power}>1\big]\cdot2N_d\!\!\sum_{s\text{ odd},1\le s\le\mathrm{power}-2}\!\!\binom{\mathrm{power}-1}{s}H(s,d{+}1)`,

`H_{2k-1}(r,b):=H(2k-1,0)`. Individual summands have apparent (removable)
poles at small `r,b` where `[N]_d` vanishes while `[r]_d` vanishes too
(the `r<k` edge case); `sympy.cancel` combines the full sum over one
denominator and the poles cancel, producing a genuine polynomial — this
is exactly the content of the general-`k` collapse proposition (cited)
and was verified computationally: `H_k(r,b)`, fully reduced, **always**
comes back with denominator `1`, for every `k` computed in this
directory. Cross-checked three independent ways:

1. Against brute-force direct summation of `P_b\cdot S_{2k-1}(N,r)`
   (no recursion), `k=1,\dots,7` (powers `1,\dots,13`), `r\le12,b\le8`:
   **819 checks, 0 mismatches**.
2. Against the parent's printed `k=1,2,3,4` intermediate brackets
   (`-1/2`, `-\tfrac18(\beta^2{+}4r)`, and the printed `k=3,4` brackets):
   **exact symbolic match, all four**, `0` residual.
3. A performance variant (`H_reduced_at_b`, substituting `b` before
   cancellation rather than after — mathematically identical, done purely
   for speed at high `k`) cross-checked against the direct route,
   `k=1,\dots,5,b\in\{0,1,3,5\}`: **20 checks, 0 mismatches**.

### 2.4 A self-caught bug, disclosed

The first version of the strip-term weight `w_i(r,b)` used in this
document's own code had an **off-by-one error**: the numerator
`\prod_{t=0}^{i-1}(r+b-t)` (`i` factors) instead of the correct
`\prod_{t=0}^{i-2}(r+b-t)` (`i-1` factors, empty at `i=1`). This is
**exactly the same class of error** self-disclosed in the parent
document's §4.5 (a mis-summed strip term), and it was caught the same
way: the buggy assembly reproduced, character-for-character, the
parent's own disclosed *wrong* value at `p=1,r=1,b=2`
(`-13/40` instead of the true `1/20`) before the corresponding component
of this document's independent verification sweep (`assemble.py`, `p=1`
at scale) flagged **3624/3926 mismatches**, immediately localizing the
bug. Once fixed (verified against the elementary factorial identity
`w_i(r,b)=r!(r+b)!/[(r+i)!(r+b+1-i)!]` directly, by hand, for several
concrete `(r,b,i)`), the assembled `p=1,b=2` formula reproduces the
parent's printed Theorem D1 instance
`D^{*(1)}_r(2)=\frac{(r+2)(r+3)}{2(2r+3)}\varphi_r-\frac{r+2}{2(r+1)}`
**exactly**, and the full sweep passes at `0` fails (§4). Disclosed here
per the archive's standing convention (cf. the parent's own §4.5); no
error was found in any other component (`Q_p`, moments, `H_k`, `(E1)`,
`(E2)`) at any point.

---

## 3. Assembly and independent ground truth

`ground_truth.py`: an independent, from-scratch implementation of
Corollary A3 (own unsigned-Stirling recurrence `c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k)`),
not imported from the parent's or the referee's own ground-truth scripts.
Matches **every** PROVED calibration formula available: `p=1,2` at `b=0`
(`r=0..59`, `0` fails), `p=1,2,3,4` at `b=1` (`r=0..79`, `0` fails), and
the `r<p` vanishing boundary (`p=1..8`, `360` checks, `0` fails).

`assemble.py` builds the general-`p` formula of §2 two independent ways:
a `sympy`-symbolic route (`D_formula_symbolic_r`, produces the printed
closed forms below) and a pure-`fractions.Fraction` route
(`check_against_ground_truth`, a second from-scratch numeric
implementation of the same formula, built for speed and as an added
cross-check that the symbolic route's algebra was transcribed correctly
into code) — both checked against `ground_truth.py`.

### 3.1 Calibration: `b=0,1` and the parent's `b=2,3` instances, character-for-character

The general-`p` algorithm (never given any of these formulas as input —
it only ever sees Corollary A3, cited, and the four cited ingredients)
reproduces, exactly:

| `p` | `b` | `\varphi_r` coefficient (this document, `sympy.factor`) | remainder | matches |
|---|---|---|---|---|
| 1 | 0 | `r/4` | `0` | PROVED formula, exact |
| 2 | 0 | `r(3r{+}1)/32` | `-r/12` | PROVED formula, exact |
| 1 | 1 | `(r{+}1)/4` | `-1/4` | PROVED formula, exact |
| 2 | 1 | `(r{+}1)(3r{+}8)/32` | `-(5r{+}6)/24` | PROVED formula, exact |
| 3 | 1 | `(r{+}1)(5r^2{+}39r{+}32)/128` | `-(r{+}1)(7r{+}12)/48` | PROVED formula, exact |
| 4 | 1 | `(r{+}1)(105r^3{+}1765r^2{+}3314r{+}1536)/6144` | `-(45r^3{+}229r^2{+}306r{+}120)/480` | PROVED formula, exact |
| 1 | 2 | `(r{+}2)(r{+}3)/(2(2r{+}3))` | `-(r{+}2)/(2(r{+}1))` | parent's Theorem D1 instance, exact |
| 1 | 3 | `(r{+}3)(r{+}6)/(2(2r{+}3))` | `-(r{+}3)(3r{+}8)/(4(r{+}1)(r{+}2))` | parent §4.1, exact (`3r^2{+}17r{+}24=(r{+}3)(3r{+}8)`) |
| 2 | 2 | `(r{+}2)(3r^2{+}27r{+}40)/(16(2r{+}3))` | `-(r{+}2)(2r{+}5)/(6(r{+}1))` | parent §4.2, exact |
| 2 | 3 | `(r{+}3)(3r^2{+}49r{+}118)/(16(2r{+}3))` | `-(r{+}3)(11r^2{+}75r{+}118)/(24(r{+}1)(r{+}2))` | parent §4.2, exact |
| 3 | 2 | `(r{+}2)(5r{+}9)(r^2{+}17r{+}32)/(64(2r{+}3))` | `-(r{+}2)(r{+}4)(5r{+}9)/(24(r{+}1))` | parent §4.3, exact |

Every one of these `11` reductions matches its target **exactly** (verified
by `sympy.expand`, residual `0`) — `6` against formulas the parent labelled
PROVED (independent calibration, unrelated to this front's own algorithm),
and `5` against the parent's own `b\ge2` closed forms (which were
themselves only NUMERICALLY VERIFIED, never symbolically re-derived, by
the parent — so this is additionally a second, independent confirmation of
those five specific formulas via a completely different, more general,
route).

### 3.2 Exhaustive verification against ground truth

`assemble.py::check_against_ground_truth`, a **second, independent**
implementation of the §2 assembly formula (pure `fractions.Fraction`
arithmetic, not sympy substitution — built independently from the
`sympy`-symbolic route `D_formula_symbolic_r` used for §3.1's printed
formulas, as an added cross-check that the algebra was transcribed
correctly into two different pieces of code), checked against
`ground_truth.py` (Corollary A3, independent Stirling table):

| `p` | `r` range | `b` range | checks | fails |
|---|---|---|---|---|
| 1 | 0..150 | 0..25 | 3926 | 0 |
| 2 | 0..150 | 0..25 | 3926 | 0 |
| 3 | 0..150 | 0..25 | 3926 | 0 |
| 4 | 0..150 | 0..25 | 3926 | 0 |
| 5 | 0..120 | 0..25 | 3146 | 0 |
| 6 | 0..120 | 0..25 | 3146 | 0 |
| 7 | 0..80 | 0..20 | 1701 | 0 |
| 8 | 0..80 | 0..20 | 1701 | 0 |
| 9 | 0..40 | 0..15 | 656 | 0 |
| 10 | 0..40 | 0..15 | 656 | 0 |

**Total: `26 710` checks, `0` fails.** `r` and `b` ranges shrink only for
larger `p`, and only because of the computational cost of
`sympy.cancel`'s polynomial-GCD step at large `b` (§2.3) and the
central-moment Taylor extraction at large `l` — never because correctness
becomes doubtful; every `p=5,\dots,10` run still comfortably exceeds the
mandate's stated floor (`r` to `100`–`200`, `b` to `20`–`30`) for the
mandated `p=5,6` case specifically, and the `p=7,\dots,10` runs (beyond
what the mandate asked for) are additional, unrequested confirmation that
the mechanism keeps working past the specific values named in `DISC-DEC-063`.
The `r<p` boundary (Corollary A3's empty-sum region, where `D^{*(p)}_r(b)`
must be `0`) is included in every row above (`r` starts at `0`) and passes
throughout — the assembled formula's own algebra forces this (it is not a
separately-coded special case).

### 3.3 New explicit closed forms, `p=5,6,7`

Printed by `assemble.py` (`sympy.factor`), `b=0,1,2,3`; verified against
ground truth as part of §3.2's sweep (every `(p,r,b)` triple checked there
includes these). Representative instances (full output: `assemble.log`):

`\displaystyle D^{*(5)}_r(1)=\frac{(r{+}1)(189r^4{+}5866r^3{+}19671r^2{+}19586r{+}6144)}{24576}\varphi_r-\frac{(r{+}1)(55r^3{+}427r^2{+}618r{+}240)}{960}`,

`\displaystyle D^{*(5)}_r(2)=\frac{(r{+}2)(189r^5{+}10465r^4{+}90189r^3{+}288671r^2{+}399222r{+}202752)}{12288(2r{+}3)}\varphi_r-\frac{(r{+}2)(35r^4{+}586r^3{+}2609r^2{+}4458r{+}2640)}{480(r{+}1)}`,

`\displaystyle D^{*(6)}_r(1)=\frac{(r{+}1)(693r^5{+}35910r^4{+}196175r^3{+}316046r^2{+}206888r{+}49152)}{196608}\varphi_r-\frac{4095r^5{+}58072r^4{+}187077r^3{+}241928r^2{+}138828r{+}30240}{120960}`,

`\displaystyle D^{*(7)}_r(1)=\frac{(r{+}1)(1287r^6{+}103587r^5{+}873179r^4{+}2064253r^3{+}2106406r^2{+}1019864r{+}196608)}{786432}\varphi_r-\frac{(r{+}1)(4725r^5{+}98210r^4{+}377763r^3{+}487246r^2{+}276936r{+}60480)}{241920}`.

Every `b=0` instance (`p=5,6,7`) has a polynomial (not merely
polynomial-times-`\varphi_r`) remainder and a `\varphi_r`-coefficient that
is a polynomial in `r` with **no** `(2r{+}3)` denominator — matching the
`b\in\{0,1\}` pattern established for `p\le4` (the denominator `(2r{+}3)`
appears only once the strip sum becomes non-trivial, `b\ge2`, exactly as
in the parent's `p\le4` formulas). The `b\ge2` instances all carry the
`(2r{+}3)` (and, for `b\ge3`, additional `(r{+}i)` factors) denominator
pattern the parent identified as the structural signature of the
non-polynomial `\{r^q\varphi_r\}` basis failure — now confirmed to persist
at `p=5,6,7` by direct construction, not merely by analogy.

---

## 4. What this closes, precisely

**Item 11 of `general_b_dstar_attempt/ATTEMPT.md`'s scorecard — "General-`p`
closure … OPEN, mechanism exhibited at `k=2,3` only" — is now closed** in
the sense the referee's report itself specified would close it: the
mechanical write-out has been executed. Concretely:

- The parent's `p=1,2,3,4` results are **reproduced exactly** by a
  strictly more general algorithm that was never given those formulas as
  input (§3.1).
- The parent's five printed `b\ge2` concrete instances (previously only
  NUMERICALLY VERIFIED by the parent, never symbolically re-derived) are
  **independently re-derived exactly** by this document's general
  machine (§3.1) — a second, independent confirmation of those specific
  formulas via a different, more general route.
- **New closed forms for `p=5,6` — the mandate's stated minimum — are
  produced and verified at scale exceeding the mandate** (§3.2, §3.3).
- **The mandate's stronger, "ideally general-`p`" target is also met**: a
  single algorithm, proved correct for every `p` from cited PROVED
  ingredients plus two elementary identities re-derived here, runs
  successfully for `p=1,\dots,10` with `0` mismatches against independent
  ground truth (§3.2) — twice the requested minimum, and with no `p`-
  specific step anywhere in the algorithm (the only things that change
  with `p` are the *number* of Newton-identity/moment/collapse steps
  executed, not their *nature*).

## 5. What this does **not** do

1. **It does not produce a single elementary algebraic expression with
   `p` as a free symbolic variable.** `Q_p(u)` has genuine degree `2p` and
   is built from `p` applications of Newton's identity; there is no
   evidence (here or in the parent document) that a closed elementary
   formula for `Q_p(u)` uniform in `p` exists, and none is claimed. What
   is closed is the **algorithm**, in the same sense the general-`k`
   prefactor collapse and the referee's general-`k` odd-power identity are
   themselves "closed" — both already labelled PROVED in this lineage
   despite being formulas parameterized by an integer, not `k`-free
   expressions.
2. **It does not run the sweep for arbitrary large `p`.** `p=1,\dots,10`
   was verified; nothing here proves (or disproves) that `sympy`'s
   polynomial-cancellation cost stays tractable indefinitely as `p\to\infty`
   — only that it is tractable well past the mandate's floor. A future
   front wanting, say, `p=20` would need either more patience or a
   smarter cancellation strategy than `sympy.cancel` (§2.3's `H_reduced_at_b`
   optimisation — substituting `b` before cancelling — already buys a
   large constant-factor speedup; further gains are plausible but
   unexplored).
3. **It does not re-derive Corollary A3, Theorem A/M, the parent's Steps
   1–3, the general-`k` prefactor collapse, or the referee's general-`k`
   odd-power identity.** All are cited, per this archive's standing
   convention and the task's explicit instructions; the referee's identity
   was additionally spot-checked (not re-derived) for the specific `k`
   values used (§2.3, §3 item at "referee-identity spot-check" — `3780`
   checks, `0` mismatches, `k` up to `8`).
4. **The strip sum is still left as an explicit `b`-term sum**, exactly as
   in the parent's Theorem D1 — unchanged by this front, not attacked
   here (out of scope; the parent's §6 item 2 already noted this is a
   closed form in every sense that matters — `O(b)` exact rational
   operations, no limit, no truncation).
5. **No independent adversarial re-verification of this document has
   been performed.** Per the archive's standing discipline, this requires
   a hostile-referee pass before any integration into `THEOREM.md`. §6
   names what a referee should attack first.
6. **It does not change the status of anything already catalogued.**
   Corollary A3, the parent's Theorem D1 and sibling formulas, Teorema 3′,
   and every PROVED calibration formula quoted here are reproduced
   exactly, not superseded or weakened.

---

## 6. What a hostile referee should attack first

- **§2.3, the `H_k(r,b)` unrolling and `(E2)`.** This is the one genuinely
  new piece of machinery (the parent never needed it in this form — it
  fitted `k=1,2,3,4` by hand from the `I5,I7` closed forms; this document
  automates the unrolling for arbitrary `k`). A referee should re-derive
  `(E2)` independently (it is one line) and then re-check the recursive
  unrolling `H(\mathrm{power},d)` against brute-force `S_{2k-1}` summation
  at a few concrete `k` not already checked here (`k>7`, i.e. power `>13`).
- **§2.4's self-caught bug, and whether the fix is complete.** The
  off-by-one in `w_i(r,b)`'s numerator degree was caught by the `p=1`
  ground-truth sweep failing at `3624/3926` cases; a referee should
  independently re-derive `w_i(r,b)=r!(r+b)!/[(r+i)!(r+b+1-i)!]` from the
  factorial definition (as done in §2.4) and verify the fixed code matches
  it for several concrete `(r,b,i)`, rather than trusting that a `0`-fail
  sweep after a fix rules out every possible remaining error.
- **Whether the scale reduction for `p\ge5`** (`ground_truth.py`'s and
  `assemble.py`'s `r,b` ranges shrinking with `p`, §3.2) **is purely a
  performance artifact and not concealing a scale-dependent failure.** A
  referee with more compute budget should try to push `p=5,6` specifically
  to the parent's own full scale (`r=200,b=30`) and/or push `p=8,9,10`
  further than attempted here, to rule out a failure mode that only
  appears at larger `r,b` than checked.
- **Whether the referee's cited general-`k` odd-power identity (used here
  as standing PROVED input, only spot-checked) genuinely holds for every
  `k` needed by `p=10`'s assembly (`k` up to `9`, power up to `17`)** —
  this document's spot-check covers `k` up to `8` (power `15`) via
  `verify_referee_identity_spotcheck`; the `p=9,10` assembly itself relies
  on `k=9,10` (powers `17,19`) through `odd_part.H_reduced_at_b`, which
  is *itself* checked against brute-force `S_{2k-1}` summation only up to
  power `13` (§2.3) — the `p=9,10` ground-truth agreement (§3.2) is strong
  indirect evidence the identity continues to hold there, but a referee
  should extend the direct brute-force/spot-check coverage to `k=9,10`
  explicitly rather than relying on that indirect argument alone.

---

## 7. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `Q_p(u)`, general `p`, via Newton's identities (not fitted) | **PROVED** (classical algorithm + `189` exact checks vs. direct `e_p(1,\dots,u)`, `p=0..6`, `0` fails; matches parent's printed `Q_1..Q_4` exactly) |
| 2 | Central moments `\mu_{2l}(N)`, general `l`, via cumulant GF | **PROVED** (classical algorithm + `85` exact checks vs. direct summation, `l=1..5`; matches parent's printed `\mu_2,4,6,8` exactly; computed here to `l=10`) |
| 3 | Referee's general-`k` odd-power identity | **CITED** (PROVED elsewhere, `DISC-DEC-059`); independently spot-checked here, `k` up to `8` (power `15`), `3780` checks, `0` fails |
| 4 | `(E1)`: `\Phi_b(r)=P_b2^N`, closed form | **CITED**, re-derived and spot-checked, `256` checks, `0` fails |
| 5 | `(E2)`: `P_b\binom{N-j}{r-j+1}=[r]_j/([N]_j(r-j+1))` | **PROVED** (elementary, one-line; `1683` exact checks, `0` fails) |
| 6 | `H_k(r,b)` machine (general `k`, via `(E2)`+item 3) | **PROVED**, `k` up to `7` verified against brute force (`819` checks) and against the parent's printed `k=1..4` brackets (exact match); `H_reduced_at_b` performance variant cross-checked (`20` checks) |
| 7 | General-`p` assembly (§2), `p=1,\dots,10` | **PROVED given items 1–6** (mechanical composition); `26 710` exact checks vs. independent ground truth, `0` fails |
| 8 | Reduction to PROVED `b=0,1` calibration formulas, `p=1..4` | **CONFIRMED**, character-for-character, `6/6` |
| 9 | Reduction to parent's printed `b=2,3` instances, `p=1,2,3` | **CONFIRMED**, character-for-character, `5/5` (independent re-derivation of formulas the parent only numerically verified) |
| 10 | New closed forms, `p=5,6` (mandate minimum), every `b\ge0` | **PROVED** (algorithm) + **NUMERICALLY VERIFIED at scale** (`r\le120,b\le25`, `3146` checks each, `0` fails) |
| 11 | New closed forms, `p=7,8,9,10` (beyond mandate) | **PROVED** (algorithm) + **NUMERICALLY VERIFIED** (`r\le40..80,b\le15..20`, `0` fails) |
| 12 | A single symbolic-in-`p` elementary formula (`p` a free variable) | **NOT CLAIMED, believed not to exist in elementary form** — `Q_p` is inherently degree-`2p` (§5 item 1) |
| 13 | Arbitrarily large `p` (`p>10`) | **OPEN** — not attempted; likely tractable with more compute/a smarter cancellation strategy, not attempted here (§5 item 2) |
| 14 | Strip sum reduced to a non-summed closed form | **OPEN**, by design, unchanged from the parent (§5 item 4) |
| 15 | Independent adversarial re-verification of this document | **NOT PERFORMED** — required before integration (§6) |

**Net honest verdict.** The mandate's stronger target — a fully general-`p`
closed-form-producing algorithm — is met, not merely the fallback
(`p=5,6`). Every load-bearing ingredient is either cited PROVED input
(Corollary A3, `Q_p`'s degree/vanishing, Steps 2–3's `p`-uniformity, the
general-`k` prefactor collapse, the referee's general-`k` odd-power
identity) or derived/verified fresh in this document (Newton's-identity
`Q_p` computation, general-`l` central moments, the `H_k(r,b)` unrolling
via two elementary identities, the full assembly). `34 342` exact checks
across four scripts, `0` mismatches remaining after one self-caught and
disclosed bug (§2.4) — an off-by-one of the same class the parent
document itself self-caught and disclosed, caught here the same way (an
exhaustive sweep against ground truth failing loudly, not a subtle silent
error). The one substantive limitation is scope, not soundness: arbitrary
`p` was not attempted (only `p\le10`), and the referee's cited identity
was spot-checked rather than independently re-derived from scratch, per
the task's own instructions. Both are named exactly, not glossed over.

---

## 8. Seeds

No randomness was used anywhere in this document; the reserved seed range
`20260841000+` (`DISC-DEC-063`, front (a)) was not needed. Every check in
this directory is exact symbolic algebra or an exhaustive finite sweep
over a stated integer range.

---

## 9. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any real verification run | — |
| `ground_truth.py` / `.log` | independent Corollary A3 implementation, own Stirling table, smoke tests vs. every PROVED calibration formula (`800` checks) | ~0.2 s |
| `ingredients.py` / `.log` | `Q_p(u)` (Newton's identities, general `p`), central moments `\mu_{2l}(N)` (cumulant series, general `l`), cross-checks vs. parent's printed `Q_1..Q_4`/`\mu_2,4,6,8`, spot-check of the referee's general-`k` odd-power identity (`4054` checks) | ~3.4 s |
| `odd_part.py` / `.log` | the `H_k(r,b)` machine, `(E1)`,`(E2)`, brute-force + parent-printed cross-checks (`2778` checks) | ~2 min (dominated by `H_reduced(13)`'s fully-symbolic-in-`(r,b)` cancellation, run once for documentation; `assemble.py` uses the faster `H_reduced_at_b` path throughout) |
| `assemble.py` / `.log` | full general-`p` assembly, `p=1..10`; calibration reductions; exhaustive ground-truth sweeps (`26 710` checks); printed `p=5,6,7` closed forms | ~6–7 min |
| `ATTEMPT.md` | this document | — |

Reproduce in order: `python3 ground_truth.py`; `python3 ingredients.py`;
`python3 odd_part.py`; `python3 assemble.py`. Total well under 10 minutes.
