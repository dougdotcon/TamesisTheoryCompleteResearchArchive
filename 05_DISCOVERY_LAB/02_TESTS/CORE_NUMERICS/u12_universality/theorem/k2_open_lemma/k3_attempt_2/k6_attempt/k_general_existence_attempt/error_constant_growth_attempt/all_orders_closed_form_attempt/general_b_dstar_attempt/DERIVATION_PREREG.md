# Pre-registration — general-`b` closed form for `D^{*(p)}_r(b)`

> Governance: wave 14, front (d), `DISC-DEC-057` item (d) (`GENERAL-B-DSTAR-ATTEMPT`).
> Written and committed to *before* any non-throwaway numerical verification run in
> this directory. A handful of throwaway hand-algebra sanity scripts were run
> beforehand, off-repository, purely to catch arithmetic slips before committing to
> this plan (this is disclosed in `ATTEMPT.md` §0); none of their output is cited as
> evidence anywhere below or in `ATTEMPT.md` — every number quoted there is
> reproduced by the scripts in *this* directory.

## 0. Sources read before this plan was fixed

1. `00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-057`, item (d).
2. `all_orders_closed_form_attempt/ATTEMPT.md` in full, in particular §1 (definitions
   of `g_r, h_r`), §3 (Theorem M, the Stirling-number multiplier), §4 (Theorem A, the
   exact all-orders closed form, and Corollary A3, the definition
   `D^{*(p)}_r(b):=\Phi^{[p]}_r(1,b)=\sum_{j=p}^r c_j^{(r)}(b)\,c(j{+}1,j{+}1{-}p)`),
   and §6.3 items 3–4 including the `[Correção pós-adversarial, 2026-08-23]` block
   naming the exact obstruction and the exact recommended route.
3. `error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3 (Theorem 3′,
   the referee's own general-`b` exact closed form for the `p=2` case, `D^*_r(b)`),
   read in full including its proof (the two boundary identities I1/I3, the two
   prefactor collapses, the even/odd split, the reflection argument that turns the
   truncated half-range sum into a full symmetric sum minus a `b`-term strip).

## 1. The target

`D^{*(p)}_r(b) = \Phi^{[p]}_r(1,b) = \sum_{j=p}^{r} c_j^{(r)}(b)\cdot c(j{+}1,j{+}1{-}p)`,
`c_j^{(r)}(b) := \dfrac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}`, `c(N,M)` the unsigned
Stirling numbers of the first kind. This is an **already-established, PROVED**
definition/formula (Corollary A3 of the target document, itself proved given Theorem
A/Theorem M of that same document — not re-derived here, taken as fixed input exactly
as that document's own convention requires: reused as a formula, not re-proved).

Known closed forms used only for calibration, never as derivation input:
`D^{*(p)}_r(0)` for `p=0,1,2` (PROVED, Estágio 8 Teorema 3 for `p=2`) and `p=3,4,5`
(numerically verified / referee-proved elsewhere); `D^{*(p)}_r(1)` for `p=1,2,3,4`
(the four displayed formulas in the task, `p=2` PROVED via Teorema 3′ specialised at
`b=1`); Teorema 3′ itself, the known **general-`b`** closed form for `p=2`.

## 2. The route (pre-registered before execution)

Write `N:=2r+b+1`, `\beta:=b+1`, `P_b:=r!(r+b)!/N!` (so `c_j^{(r)}(b)=P_b\binom N{r-j}`).

**Step 1 (range extension for free).** `Q_p(u):=c(u{+}1,u{+}1{-}p)=e_p(1,\dots,u)`
(elementary symmetric polynomial of degree `p` in `1,\dots,u`) vanishes identically
for `u<p` (fewer than `p` factors available). Hence
`D^{*(p)}_r(b)=P_b\sum_{\alpha=0}^{r}Q_p(r-\alpha)\binom N\alpha}` — the sum can be
extended from `\alpha\le r-p` to `\alpha\le r` at no cost, because the added terms
are exactly zero. This is claimed to hold for **every** `p`, not just `p=2`.

**Step 2 (the substitution that makes the prefactor-collapse mechanism visible).**
Put `v:=\alpha-N/2`. Then `u:=r-\alpha=-(v+\beta/2)`, **independent of `p`**. Since
`Q_p` has degree `2p` in `u` (classical fact: `e_p(1,\dots,u)` is polynomial in `u` of
degree `2p`, provable via Newton's identities from the Faulhaber power-sum
polynomials), `Q_p(r-\alpha)` becomes a degree-`2p` polynomial in `v` with
coefficients depending on `b` (via `\beta`) but **not on `r`**. Split it into its even
part `E_p(v)` and odd part `O_p(v)`.

**Step 3 (even part → prefactor collapse).** The reflection `\alpha\mapsto N-\alpha`
maps `\{r{+}b{+}1,\dots,N\}` onto `\{0,\dots,r\}` and fixes `\{r{+}1,\dots,r{+}b\}`
setwise as a genuine `b`-term "strip". Since `E_p` is even in `v` and
`\binom N\alpha=\binom N{N-\alpha}`,
`\sum_{\alpha=0}^r E_p\binom N\alpha=\tfrac12\big[\sum_{\alpha=0}^N E_p\binom
N\alpha-\sum_{\alpha=r+1}^{r+b}E_p\binom N\alpha\big]`. The full sum is `2^N` times a
polynomial in `N` built from the central moments `\mu_{2l}(N):=2^{-N}\sum_{\alpha=0}^N
(\alpha-N/2)^{2l}\binom N\alpha}` of `\mathrm{Bin}(N,\tfrac12)`, `l\le p`, which have
closed forms derivable from the cumulant generating function `N\log\cosh(t/2)`
(classical). Multiplying by `P_b` turns `P_b\cdot2^N` into the already-named
`\Phi_b(r)=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}` — the prefactor-collapse
object the mandate names. The strip is a genuine, unavoidable finite sum of `b`
explicit terms — expected **not** to collapse further into a fixed-degree polynomial
in `b` (that is the honest content of "fails structurally for `b\ge2`"), but each term
is fully explicit and the sum is closed form in every sense that matters (`O(b)` exact
rational arithmetic, no limit, no series).

**Step 4 (odd part → partial-sum identities `I_{2k-1}`).**
`P_b\sum_{\alpha=0}^r v^{2k-1}\binom N\alpha` reduces, via `v=-(N-2\alpha)/2`, to
`P_b` times the referee's `I1`/`I3`-type partial binomial sums
`S_{2k-1}(N,r):=\sum_{\alpha=0}^r(N-2\alpha)^{2k-1}\binom N\alpha`. `I1,I3` are
already PROVED (referee, wave 10). `I5, I7` are **not** in any prior document; if
needed (`p\ge3`) they will be derived here by the same Abel-summation-by-parts
technique the referee used to get `I3` from `I1` (telescoping against
`A(i):=(i{+}1)\binom N{i+1}`), each reducing recursively to `I_{2k-3}` evaluated at
`(N{-}1,r{-}1)`, and then reduced to an explicit polynomial-in-`r,b` value via a
family of prefactor collapses
`P_b\cdot[N]_k\cdot(r{-}k{+}1)\cdot\binom{N-k}{r-k+1}=[r]_k` (falling factorials),
generalising the two collapses the referee already names (`k=0,1`); each instance of
this family used will be proved, not merely fitted (by algebraic identity, `k!` and
factorial cancellation, plus symbolic sympy confirmation).

## 3. Concrete deliverable and verification plan

- Carry Steps 1–4 through explicitly for `p=1` (mandatory target). Produce a single
  explicit formula for `D^{*(1)}_r(b)`, valid for every `b\ge0`, reducing at `b=0` to
  the PROVED `\tfrac r4\varphi_r` and at `b=1` to the given, PROVED-via-Teorema-3′
  calibration formula `D^{*(1)}_r(1)=\tfrac{r+1}4\varphi_r-\tfrac14` **character for
  character**, not merely numerically.
- Attempt the same for `p=2` (should reproduce Theorem 3′, itself already an
  independent PROVED result — an exact match is a strong end-to-end validation of the
  whole method) and `p=3,4` (needs `I5,I7` and `\mu_6,\mu_8`) if the required
  ingredients close out cleanly.
- Exact verification, `fractions.Fraction` throughout, no floating point except
  possibly display. Ground truth for every check: **direct evaluation of the already-
  PROVED Corollary-A3 sum** `D^{*(p)}_r(b)=\sum_{j=p}^r c_j^{(r)}(b)c(j{+}1,j{+}1{-}p)`
  (own from-scratch implementation, own from-scratch unsigned-Stirling table via the
  standard recursion `c(n,k)=c(n{-}1,k{-}1)+(n{-}1)c(n{-}1,k)`) — never the derived
  closed form checked against itself.
- Sweeps planned: `Q_p(u)` identified by exact interpolation on `2p+1` points (using
  the a-priori degree bound `2p`) then confirmed on `\ge10` further out-of-sample
  points, for `p=0,\dots,4`. Central moments `\mu_2,\mu_4,\mu_6,\mu_8` checked
  exhaustively for `N\le17`. New partial-sum identities `I5,I7` checked exhaustively
  for all `(N,m)`, `N\le34`. Prefactor-collapse family checked exhaustively for
  `b\le10,r\le20`, **and symbolically** (general symbolic `r,b`, `sympy.simplify`) for
  every instance actually used. Final assembled formulas checked against ground truth
  for: `p=1`, `b\le20,r\le150` (`\ge3000` exact checks); `p=2,3,4`, `b\le10,r\le60`
  each (`\ge650` exact checks each).
- No randomness needed anywhere (pure exhaustive exact sweeps over finite integer
  ranges); the reserved seed `20260837000+` is therefore not used. Confirmed unused
  elsewhere in the archive before this document was written
  (`grep -rn "20260837" 05_DISCOVERY_LAB/` — the only hit was the ledger's own
  reservation line).

## 4. Pre-registered honesty criteria

- If Steps 1–4 fail to close for `p=1` (the mandatory target): report exactly which
  step failed and why, and whether a fallback (e.g. leaving the strip un-collapsed, or
  leaving an `I`-identity unresolved) still yields a valid, if less clean, closed
  form. Non-closure at `p=1` would be reported honestly as OPEN.
- Any formula is labelled PROVED only if (a) every step used is itself proved (by
  algebraic identity or by a previously-PROVED source, cited) and (b) it survives
  exhaustive exact numerical corroboration against ground truth with **zero**
  mismatches over the stated range. A formula surviving only the numerical
  corroboration, with some step not fully closed algebraically, is labelled
  NUMERICALLY VERIFIED, not PROVED, and the gap is named precisely.
- Reduction to the known `b\in\{0,1\}` calibration formulas is a **hard requirement**,
  checked character-for-character (not just numerically), before any `p` is reported
  as closed.
