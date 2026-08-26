# ATTEMPT — resummation of the b=1 floor plateau (`PLATEAU-RESUMMATION-ATTEMPT`)

**Wave 17, front (d), `DISC-DEC-072`.** Target: the ONE mathematical gap
left by wave 16 front (d) + its referee (`floor_h2_b1_full_closure_attempt`,
`DISC-DEC-071`, node `FLOORH2` in `PROOF_DEPENDENCY_MAP.md` Tree B): a
CLOSED-FORM RESUMMATION of the (exactly-coefficiented, everywhere-convergent)
series for the abstract b=1 floor process's `Phi(0,t0)`, whose plateau
constant `Phi(0,t0>=0.02) = 0.0377615983...` at `c=1000` had no identified
closed form. This is the `M-CLUST(b)` line (Tree B) — a standalone
combinatorial/probabilistic object; nothing here touches the archive's
separate Conjecture-1/whole-space line, `phi_REDB`, or any formula of
record, and nothing here concerns the real `n=65536` engine (the ~30%
abstract-vs-real gap is explicitly out of scope per the mandate).

Notation, this document: `Pi(c) := lim_{t0->inf} Phi(0,t0)` — the plateau
constant of the ABSTRACT process at parameter `c` (the limit exists; the
approach is `~e^{-c t0}`, §2). The wave-16 target cell is `c=1000`.

---

## VERDICT UP FRONT

**Tier: honest non-closure of the strict target (no exact closed form for
`Pi(c)` at finite `c` was found; inverse-symbolic search excludes several
natural candidate families to the tested precision), with a genuinely new,
machine-verified, numerically-confirmed FOUR-TERM ASYMPTOTIC LAW — the
first closed-form statement about the plateau constant in this
lineage — plus the sharpest numerical characterization of `Pi(c)` to date
(7 independent values at >=110 correct digits, spanning `c=640` to
`c=655360`) and a set of proved/measured exclusions that any future
closed-form candidate must satisfy.**

1. **DERIVED (heuristic matched asymptotics; every algebraic step
   machine-verified, §4; two named heuristic gaps stated in §4.5) and
   CONFIRMED numerically at >=110-digit data across 7 values of `c` (§5),
   plus one independent out-of-sample holdout at `c=250` (46 digits):**

   ```
   Pi(c) = sqrt(pi/(2c)) - 2/c + (7/2)*sqrt(pi/2)*c^{-3/2} - (34/3)*c^{-2} + O(c^{-5/2})
   ```

   equivalently, with `eps := c^{-1/2}` and `y := Pi(c)*sqrt(2c/pi)`:
   `y = 1 - 2*sqrt(2/pi)*eps + (7/2)*eps^2 - (34/3)*sqrt(2/pi)*eps^3 + O(eps^4)`.
   All four coefficients are clean closed forms — exactly `1`, `-2`
   (times `sqrt(2/pi)`), `7/2`, and `-34/3` (times `sqrt(2/pi)`) — and an
   exact polynomial fit of the >=110-digit multi-`c` data (no free
   parameters; §5) reproduces them to `~12`, `~9`, `~6`, and `~4`
   significant digits respectively, with the whole degree-6 fit further
   confirmed by an independent out-of-sample check at `c=250` (2.3e-7
   relative, `c=250` never entering the fit). A conjectured fifth term
   (`209/8 * sqrt(pi/2) * c^{-5/2}`, from extrapolating a `gamma_n`
   recursion pattern the matched-asymptotics derivation exhibits only
   through `n=4`) is numerically consistent but weak (`~2-3` digits,
   itself UNVERIFIED as a derivation, §4.5) — reported as a named
   conjecture, not a result. At `c=1000` the four-term law gives
   `Pi ~= 0.03776066` against the exact `0.03776160` (`2.5e-5` relative,
   ~4.6 significant figures — `c=1000` is not deep into the asymptotic
   regime; the law is confirmed far more sharply, §5, from its
   coefficients matching independently at each order across the whole
   `c=640..655360` ladder), so the wave-16 "unidentified constant" is
   now *asymptotically* identified to a sharper order than a first pass
   found, even though its finite-`c` value is not.

2. **`Pi(c)` computed to >=110 significant digits at 7 values of `c`**
   (c = 640, 1000, 2560, 10240, 40960, 163840, 655360 — a 1024x range in
   `c`), plus one value at 46 digits (`c=250`, used only as a holdout,
   never a fit input) and, honestly disclosed, a genuine COST WALL below
   `c~250` that this front hit and, per the mandate's anti-stall
   instruction, did not force through (§2.2/§3: `c=160,100,40,10,1` were
   attempted — some inherited from a predecessor instance, one re-attempted
   by this front — and none completed within budget; the cost scaling is
   quantified, not just asserted). Each retained value carries its own
   three-way error control (approach / truncation / roundoff) and, for
   `c=640` and `c=1000`, two independent-parameter cross-computations
   agreeing to ALL reported digits (§3). `Pi(1000) =
   0.0377615983402126188243712025905770479904...` (121 digits computed,
   111 stable, §3), consistent with the wave-16 referee's 10-digit
   `0.0377615983`.

3. **Inverse-symbolic identification of the finite-`c` constant FAILED
   honestly** (§7): `mpmath.identify`/PSLQ over natural constant bases
   (`sqrt(2), sqrt(pi), pi, ln(2), e`; and separately the `erfcx`/
   `sqrt(pi c/2)` family that provably generates every series coefficient)
   found NO MATCH / NO RELATION at up to 100 digits, at 4 independent `c`
   values, after this front caught and fixed a methodological bug in the
   inherited PSLQ setup that had been manufacturing spurious "relations"
   not actually involving `Pi` (§9, S4). Separately, simple closed-form
   families are EXCLUDED by genuine, bug-free cross-`c` numerical tests:
   any 2-term (`a/sqrt(c)+b/c`) or 3-term truncating polynomial-in-`eps`
   family, fit on some `c` values and tested out-of-sample on others,
   mismatches by `3.6e-4` to `5.6e-3` (2-term) or `2.6e-5` (3-term) —
   far above the `>=1e-40` roundoff floor of the data (§7); and any
   function whose `eps`-expansion is purely EVEN in `eps` (every rational
   function of `c`) is excluded outright by `d1 != 0` (§5/§7, confirmed to
   ~9 digits). These are exclusions "to the stated precision over the
   stated bases/families", not impossibility proofs.

4. **Two structural findings that reframe why closure is hard (§2.3, §6):**
   (a) `Phi(0,.)` is entire of order 2 in `t0` — its partial-sum terms
   reach `~e^{c t0 + 0.9 (c t0)^2/c}` before cancelling — which makes
   plain Borel(-1) resummation *analytically valid but numerically and
   structurally useless* (the Borel transform itself grows like
   `exp(2.9 (c u^2/8)^{1/3})` on the real axis: disclosed failed attempt,
   §2.3), and puts the natural resummation target outside the classical
   Borel class; (b) the plateau PROFILE in `s` is asymptotically the SAME
   `erfcx` shape as the `k=1` coefficient `psi1 = b_1` —
   `F(s) = eps*R(x) + eps^2*(2xR(x)-2) + O(eps^3)`, `x = s*sqrt(c)`,
   `R(x) = sqrt(pi/2)*erfcx(x/sqrt(2))` — verified directly from this
   front's own polynomials at `s>0`, numerically, at 5 values of `x` and
   2 values of `c` (`1000, 2560`), with the residual after both terms
   trending toward the DERIVED 3rd-order prediction as `c` grows (§6).
   This supplies the quantitative, analytic resolution of the wave-16
   SS3.4 "near-rank-2 tension": the surface is `e^{-cg} + (1-e^{-cg})F(s)`
   to the orders computed, exactly the referee's no-fit ansatz, now with
   `F` pinned in closed form at two full asymptotic orders (plus a
   numerically-confirmed trend at the third).

`phi_REDB` and every formula of record: untouched. No referee dispatched
(per mandate); no git commit; nothing written outside this directory.

---

## 0. Setup, provenance, discipline

Read first, in full, prose only: the wave-16 `ATTEMPT.md` (with all dated
addenda) and its `adversarial/REFEREE_REPORT.md`; the wave-14 parent
`floor_closed_form_attempt/ATTEMPT.md` (process definition, SS3.1/SS4/SS5);
`PROOF_DEPENDENCY_MAP.md` SS2 (Tree B). **No script of the wave-16 front,
its referee, or the wave-14 parent was opened** — per the mandate, the
`(P,Q)`-family solve was re-derived from the prose of record and
implemented fresh (§1), then validated against the published anchor
numbers before being trusted.

The established inputs (referee-proved, session-verified, wave 16):

```
Phi(s,g) = sum_k a_k(s) g^k ,  Psi(s,g) = sum_k b_k(s) g^k ,  a_0=1, b_0=0
a_{k+1} = [a_k' - c a_k + c w_k]/(k+1)
b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}          (bounded branch)
w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
a_1 = -c ,  b_1 = psi1 = sqrt(pi c/2)*erfcx(s sqrt(c/2))
every a_k, b_k lies in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polys
Phi(0,t0) = sum_k a_k(0) t0^k converges for all t0; plateau at c=1000:
0.0377615983 for t0 >= 0.02, approach ~e^{-c t0}
```

and the underlying PDE system of record (wave-14 SS5):

```
dPhi/ds - dPhi/dg = c[Phi - W],   dPsi/ds = c[Psi - W]
W = g*Avg_g[Phi] + (1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
Phi(s,0) = 1;  target Phi(0,t0)
```

**This front is fully deterministic — no randomness was needed or used; no
seeds consumed** (the reserved range `20260866000+` was grep-confirmed to
appear only in ledger/queue reservation lines and remains unused).

Work directory: this directory only. All scripts/logs alongside this file.

---

## 1. Fresh implementation of the recursion inside the `(P,Q)` family

### 1.1 Own re-derivation of the family solve (independent of the referee's)

With `E(s) := erfcx(s*sqrt(c/2))` and `sc := sqrt(2c/pi)`, the identity
`E' = c s E - sc` closes `F` under `d/ds`:
`(P + Q E)' = (P' - sc Q) + (Q' + c s Q) E`. For the Psi-ODE
`b' - c s b = A + B E` with polynomial `A, B`, writing `b = U + V E`:

- E-part: `V' = B`, so `V = int B + kappa` with one free constant `kappa`;
- non-E part: `U' - c s U = A + sc*V =: R`; matching `s^j` coefficients,
  `(j+1)u_{j+1} - c u_{j-1} = r_j`, solved DESCENDING from `j = deg R`
  (which forces `deg U = deg R - 1` and uses no integration), leaving the
  single leftover `j=0` relation `u_1 = r_0` — which PINS `kappa`
  (`kappa = (u_1 - A_0)/sc`), exactly the "integration constant pinned by
  a consistency condition" of the record.

The polynomial ansatz automatically discards the `e^{c s^2/2}` homogeneous
branch — i.e. *is* the bounded-branch selection — and the solution in `F`
is unique (the homogeneous system forces `U = V = 0`).

### 1.2 Implementation and validation

`r01_family_series.py` implements this with mpmath (gmpy backend)
arbitrary-precision coefficients. Validation before ANY use
(`r01_family_series.log`): **10/10 anchors pass** — the published numeric
anchors `a_2(0) = 520316.636488`, `a_3(0) = -180730907.6285`,
`a_4(0) = 47146963944.14`, `b_2(0) = -20816.636488`,
`Phi(0,0.002) = 0.15850015`, plateau `0.0377615983` (at `t0 = 0.03` AND
`0.05`, agreeing with each other to `4.6e-14`, matching the record's
stated approach rate), plus exact-identity checks against the referee's
closed forms `b_2(s)`, `b_3(s)`, `a_3(0)` closed form, `b_1 = sqrt(pi c/2)`.

`r02_symbolic_check.py` repeats the whole construction in exact sympy
arithmetic with SYMBOLIC `c` (strictly stronger than any numeric check):
the `E'` identity, the b-ODE residuals of the family solve at `k = 1..5`
(all exactly 0), and the closed forms of record (`b_1, b_2, b_3, a_2`,
`a_3(0)` for symbolic `c`; `a_4(0)` at `c=1000`) — **all PASS exactly**
(`r02_symbolic_check.log`).

---

## 2. Computing the plateau constant: method, error control, and a
disclosed failed route

### 2.1 Direct summation, three-way error control

`Pi(c)` is computed as `S(t0) = sum_{k<=K} a_k(0) t0^k` at `c*t0 in
{230, 260, 290}` (`e^{-260} ~ 1e-113`), with, per `c`:

- **approach error** measured directly as `|S(260/c) - S(290/c)|`
  (reported digits = stable common prefix of the two largest-`ct0` sums;
  the `|S(230/c) - S(290/c)|` difference confirms the `~e^{-c t0}`
  approach rate at every `c`);
- **truncation** controlled by the printed last-term magnitude (required
  `< 1e-115` relative);
- **roundoff** controlled by an independent rerun at higher dps (`c=1000`
  at dps 360 vs 440: all 121 printed digits identical) and by
  independent-parameter duplicates (`c=640` computed in two jobs with
  different `K`/dps: identical to all 121 digits).

### 2.2 The cost structure (found the hard way, disclosed)

`Phi(0,.)` is entire of ORDER 2: beyond the `~e^{c t0}` "race" content,
the partial sums must resolve content whose terms reach
`~e^{0.9 (c t0)^2 / c}` before cancelling (measured empirically:
max|term| `~1e150` at `c=1000, ct0=290` but `~1e768` at `c=160, ct0=290`,
per-c logs). At fixed `c*t0` this cost EXPLODES as `c` decreases — a
uniform-parameter first attempt produced pure cancellation garbage at
small `c` (partial sums `~1e+1866` at `c=1`, `~1e+1132` at `c=10`, both
`stable_digits=0`), caught immediately by the max-term/stability
diagnostics (self-caught issue S1, §9). A second, per-`c`-sized attempt
(`fixmid`/`c100deep`/`c40deep`/`c10mid`/`c1small` jobs in
`r03_plateau_multi_c.py`) recovered `c=640` and `c=250` (46 stable digits
at `c=250`, `736s`) but the `c=160` job never completed (no output in
`r03_fixmid.log` beyond `c=250`) and the `c=100,40,10,1` jobs produced NO
output at all — empty log files, confirmed by this front (`ls -la`) before
trusting anything from them. **Honest, quantified conclusion (this
front):** direct summation at the precision target used here (`>=100`
stable digits) is affordable from `c=655360` down to `c=640`
(`160s`-`210s` each); `c=250` is a demonstrated, expensive (`736s`) floor
at REDUCED precision (46 digits); `c<=160` is a genuine cost wall, not a
bug — extrapolating the requested `(K,dps)` for `c=40`
(`K=16000,dps=1200`, the predecessor's own sizing) against this front's
OWN measured `c=1000` runtime (`163.5s` at `K=2000,dps=360`) via the
method's `O(K^2)` descending-solve cost times an `O(dps)`-ish mpf-op cost
gives `~(16000/2000)^2*(1200/360) ~= 213x ~= 9.7 HOURS` — correctly out of
this front's budget, so `c=40,10,1` were NOT re-attempted (anti-stall
instruction, mandate). `c=250` (46 digits) is used below ONLY as an
out-of-sample holdout check (§5), never as a fit input; `c<=160` is not
used at all. This is a genuine, disclosed limitation, not a hidden gap: a
faster method for small `c` (ideally the resummation this front set out to
find) would remove it, and its absence is exactly why that resummation
would matter practically, not just aesthetically.

### 2.3 Disclosed failed route: Borel-Laplace resummation

Since the direct-cost wall is the order-2 content, the natural move is
Borel: `B(u) = sum a_k(0) u^k/k!` and
`Phi(0,t0) = (1/t0) int_0^inf e^{-u/t0} B(u) du` (analytically valid here:
the series is absolutely convergent everywhere, so Fubini justifies the
exchange term-by-term). Implemented (`r03b_borel.py`, kept for the
record): it FAILS numerically, for a structural reason worth recording:
the order-2 content makes `B(u)` itself grow like
`exp(2.9*(c u^2/8)^{1/3})` on the real axis (measured: `max|B| ~ 1e1237`
at `c=1`), so the Laplace integrand has an interior hump of `e^{+tens of
thousands}` that must cancel in quadrature — worse than the direct sum.
Rotating the contour cannot fix it (the transform's order-2/3 indicator
is positive on every usable ray), and a second-level (Borel-2) transform
trades the hump for equally fatal transform growth. **Any resummation of
this series that stays in the classical Borel-1 class is numerically (and
plausibly structurally) the wrong tool** — a concrete negative finding
that narrows where a future closed form can come from. (Self-caught
issue S2, §9: the first Borel run's garbage was flagged by its own
`max|B|` diagnostic and the `Phi > 1` sanity check.)

---

## 3. The multi-`c` constant table

**Primary table — 7 values, `>=110` stable digits each, direct exact
summation (§2.1), spanning a `1024x` range in `c`:**

| `c` | `Pi(c)` (leading 40 digits shown; full value in `.log`/`.json`) | stable digits | cross-check |
|---|---|---|---|
| 640 | `0.0466626652057907264316848615295666243978...` | 112 | 2nd independent run (`fixmid`, different `K`/`dps`): identical to ALL 121 printed digits |
| 1000 | `0.0377615983402126188243712025905770479904...` | 111 | 2nd independent run (`control`, `dps=440` vs `360`): identical to ALL 121 printed digits |
| 2560 | `0.0240217755876659764091477607960026096265...` | 111 | approach-rate self-check (`|S_lo-S_hi|` vs `|S_mid-S_hi|`) consistent with `~e^{-ct0}`, §2.1 |
| 10240 | `0.0121942135050897716189679273526861033446...` | 111 | \" |
| 40960 | `0.0061443932785551918066159319216308650218...` | 111 | \" |
| 163840 | `0.0030842081459557513799990201104874476322...` | 110 | \" |
| 655360 | `0.0015451312096662308759993857963513008680...` | 110 | \" |

(full values: `r03_plateau_values_ladder.json`; runtimes `159.8s`-`209.9s`
each, `r03_ladder.log`.)

**Secondary, out-of-sample-only value — `c=250`, 46 stable digits,
COST-EXPENSIVE (`736s`):**

```
Pi(250) = 0.0722226317815141619643797100974506988118877722234201774...
```

Used ONLY as an independent holdout for §5's asymptotic-law fit, NEVER as
a fit input (deliberately, to keep the fit/test split honest).

**Failed / not-completed attempts, disclosed (self-caught issue S5, §9):**

| `c` | attempted `(K,dps)` | outcome |
|---|---|---|
| 160 | `2600/380` (ladder), then `4700/560` (fixmid) | BOTH failed: ladder run gave pure cancellation garbage (`stable_digits=0`, sum `~1e+335`); fixmid run never completed (no output past `c=250` in `r03_fixmid.log`) |
| 100 | `7400/690` (queued by predecessor) | never ran (`r03_c100deep.log` is a 0-byte file) |
| 40 | `16000/1200` (queued by predecessor) | never ran (`r03_c40deep.log` is a 0-byte file); this front's OWN cost-scaling estimate (§2.2) puts this job at `~9.7` hours — correctly not attempted |
| 10 | `1500/320` (first pass, uniform sizing) | pure cancellation garbage (`stable_digits=0`, sum `~1e+1132`); no corrected-sizing rerun exists |
| 1 | `1500/320` (first pass, uniform sizing) | pure cancellation garbage (`stable_digits=0`, sum `~1e+1866`); no corrected-sizing rerun exists |

**`Pi(c)*sqrt(2c/pi)` (the natural `eps`-rescaled quantity used in §4-§5),
all 7 primary values, showing the approach to the derived limit `1`:**

| `c` | `eps=c^{-1/2}` | `y := Pi(c)*sqrt(2c/pi)` | `y-1` |
|---|---|---|---|
| 640 | 0.03953 | 0.9418887051589530 | -0.05811 |
| 1000 | 0.03162 | 0.9527751685565295 | -0.04722 |
| 2560 | 0.01976 | 0.9697619715505595 | -0.03024 |
| 10240 | 0.00988 | 0.9845637336047824 | -0.01544 |
| 40960 | 0.00494 | 0.9921995845890996 | -0.00780 |
| 163840 | 0.00247 | 0.9960788323507785 | -0.00392 |
| 655360 | 0.00124 | 0.9980341263096878 | -0.00197 |

`(y-1)` shrinks essentially in step with `eps` (ratio `(y-1)/eps` moves
from `-1.470` at `c=640` to `-1.591` at `c=655360`, converging toward the
derived `d1 = -2*sqrt(2/pi) = -1.5958`), a first visual confirmation of
§4's law ahead of the quantitative fit in §5.

---

## 4. The asymptotic derivation

Scaled variables `x = s*sqrt(c)`, `y = g*sqrt(c)`, `eps = 1/sqrt(c)`.

### 4.1 Two exact reformulations

(i) The mode-E PDE of record `dPsi/ds = c[Psi - W]` becomes, EXACTLY and
`c`-free:

```
Psi_x = (x+y) Psi - I(x,y),      I := int_0^y Phi(x,y') dy'      (E1)
```

(ii) substituting (E1) into the definition of `W` gives the EXACT operator
identity (machine-verified, r06 V1):

```
W = Psi - eps * dPsi/dx                                          (KEY)
```

so the whole coupled system collapses to ONE unknown: `Phi` is the
characteristic renewal of `Psi - eps Psi_x`,

```
Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} [Psi - eps Psi_x](x+v, y-v) dv   (E2)
```

and (E1)+(E2) close. This reduction is new in this lineage (the wave-14/16
record treats `(Phi,Psi)` as irreducibly coupled; it is — but only up to
this one-line elimination in scaled variables).

### 4.2 Leading order: `Pi(c) ~ sqrt(pi/(2c))`

Expanding the renewal kernel (Watson; exact term-by-term on polynomials,
r06 V3) for `y >> eps` gives `Phi = W + eps(W_x - W_y) + O(eps^2)`, and
`I = eps(1 - e^{-y/eps}) + [kernel expansion of J - eps J_x]` with
`J := int_0^y Psi`. At `O(eps)`, writing `Psi = eps psi1 + ...`:

```
psi1_x = (x+y) psi1 - 1 - int_0^y psi1 dy'
```

whose bounded solution is `y`-INDEPENDENT (r06 V8) and equals

```
psi1(x) = R(x) := sqrt(pi/2) * erfcx(x/sqrt(2)),   R' = xR - 1, R(inf)=0
```

— the SAME function as the `k=1` coefficient profile `b_1(s) = sqrt(c) R(s sqrt(c))`.
Hence `Pi(c) = eps*R(0) + O(eps^2) = sqrt(pi/(2c)) + O(1/c)`.

### 4.3 Second order: the exact `-2/c`

Two `O(eps^2)` sources appear in the `psi2` equation, and they are EQUAL:

- the outer re-entry source `+eps*Psi` contributes `R(x)`;
- the inner-layer deficit of `J`: near `y = 0`, `Psi` rises from 0 as
  `Psi(x, eps z) = eps*(1 - e^{-z})R(x) + O(eps^2)` (r06 V6), so
  `J_true = J_outer - eps^2 delta(x)` with `delta = R(x)` exactly.

So `psi2' = x psi2 + 2R`, bounded branch (closed form, r06 V7):

```
psi2(x) = 2 x R(x) - 2 ,     psi2(0) = -2
```

giving the second term `-2 eps^2 = -2/c` — with coefficient exactly `-2`.

### 4.4 Third order: `(7/2) sqrt(pi/2) c^{-3/2}`

Carrying every `O(eps^3)` source (kernel expansion one order further; the
`O(eps)` correction to the inner `Phi`, which integrates to
`B(z) = z - 2 + 2e^{-z} + z e^{-z}`, r06 V9; the second-order inner
profile `p2(x,z) = [1-(1+z)e^{-z}] psi2(x)` — whose `z->inf` limit
MATCHES `psi2` automatically, a nontrivial consistency check of the whole
scheme, r06 V10; the second-order layer deficit `delta2 = 2 psi2`, r06
V11; and `+eps^2 Psi_x -> psi1'`), the total third-order source collapses
remarkably:

```
h3 = psi2 + psi1' + delta2 = 3(2xR-2) + (xR-1) = 7(xR - 1) = 7 R'(x)
```

so `psi3' = x psi3 + 7R'`, and `psi3(0) = -int_0^inf e^{-x^2/2} 7R' dx =
(7/2) sqrt(pi/2)` (r06 V12). The plateau extraction telescopes exactly —
`(sum_n eps^n D^n)(1 - eps D) Psi = Psi` for the `y`-independent outer
fields (r06 V13) — so no extraction corrections enter and

```
Pi(c) = eps sqrt(pi/2) - 2 eps^2 + (7/2) sqrt(pi/2) eps^3 + O(eps^4).
```

### 4.4b Fourth order: `-(34/3) c^{-2}`, and a conjectured all-orders pattern

The predecessor instance's `r06_asymptotic_derivation.py` carries the SAME
matched-asymptotics machinery one further order (groups V15-V17: the
`O(eps^2)` inner-`Phi` correction and its integrated source, the `p3`
inner layer, and the resulting `psi4` ODE) and finds the fourth-order
source ALSO collapses cleanly:

```
h4 = 4 psi3 + psi2' + psi1'' = 17 R''(x)
```

so `psi4' = x psi4 + 17 R''`, giving, in closed form, TWO independent
ways (ODE solve and direct integral, both machine-checked, V17):

```
psi4(x) = (17/3) R'''(x) ,     psi4(0) = -34/3
```

— **this front independently re-ran `r06_asymptotic_derivation.py` in
full before trusting it** (all 18 verification groups V1-V18 re-executed,
all PASS; `r06_asymptotic_derivation.log`, unchanged from the
predecessor's run, confirming determinism). The assembled four-term law
(used throughout this document) is:

```
Pi(c) = sqrt(pi/(2c)) - 2/c + (7/2)sqrt(pi/2)*c^{-3/2} - (34/3)*c^{-2} + O(c^{-5/2})
```

`r06`'s own group V18 additionally derives a closed-form RECURSION
generating `psi_n(0) = gamma_n * R^{(n-1)}(0)` for a rational sequence
`gamma_n = 1, 2, 7/2, 17/3, 209/24, 773/60, ...` and a derivative-closure
identity `R^{(n+1)} = x R^{(n)} + n R^{(n-1)}` for `R` itself (V14,
machine-verified `n=1..6`) that lets any `R^{(n-1)}(0)` be evaluated in
closed form (`sqrt(pi/2)` or `-1` times a rational, alternating by
parity). **This gives, IN PRINCIPLE, a closed-form generator for every
order of the asymptotic series** — but the `gamma_n` sequence itself is
only DERIVED (via the same matched-layer machinery as `psi1..psi4`, groups
V1-V17) through `n=4`; `gamma_5=209/24` onward is a PATTERN CONJECTURE
extrapolated from the first four values, explicitly flagged as such in
`r06`'s own log ("gamma-pattern conjectured beyond [n=4], tested
numerically in r04") and NOT independently re-derived by carrying the
boundary-layer expansion to a 5th order in this front. This front treats
`gamma_5` and beyond as an open, named conjecture (§4.5, §10), not a
result, and does not attempt to prove the general pattern (out of scope
for the effort level of this front; the four DERIVED terms already exceed
the mandate's minimum ask).

### 4.5 Status of the derivation (honest)

Every ALGEBRAIC step above (through 4th order, `n<=4`) is machine-verified
in `r06_asymptotic_derivation.py` (18 verification groups V1-V18, ALL
PASS, symbolic `c` where meaningful; re-executed fresh by this front, not
merely trusted from the predecessor's log). Exactly TWO steps are
heuristic (named, not hidden): (H1) the Watson/matched-layer framework
itself — smoothness and uniform validity of the outer/inner decomposition
and the `O(eps^n)` remainder bounds are assumed, not proved; (H2)
uniqueness of the `y`-independent bounded solution at each order (proved
only within fields where the `y`-differentiated homogeneous equation's
`e^{xy + x^2/2}` growth can be excluded by boundedness). A THIRD gap
applies only beyond 4th order: (H3) the `gamma_n` all-orders pattern
(§4.4b) is a numerically-motivated CONJECTURE past `n=4`, not derived by
this front's own matched-asymptotics steps. This is why the law is
reported as **DERIVED (heuristic, `n<=4`) + CONFIRMED (numerically, §5)**,
not PROVED, with the `n=5` term reported separately as an unproven,
numerically-weak-but-not-excluded conjecture (§5, §10). The genuinely
UNDETERMINED term (not even conjectured by this front, since `r06`'s own
pattern-extrapolation was not carried further) is `O(c^{-3})` and beyond.

---

## 5. Numerical confirmation of the law (no free parameters)

`r04_asymptotics_fit.py` (this front; a crash bug in the predecessor's
draft — an undefined `d1_pred` at the JSON-dump step, self-caught, §9 S3 —
is fixed here) tests the derived law against the >=110-digit `Pi(c)` table
(§3) by exact polynomial interpolation (Vandermonde/LU solve, `mpmath`,
130 dps): writing `y(eps) := Pi(c)*sqrt(2c/pi) = sum_j d_j eps^j`, it fits
`d_0..d_6` EXACTLY (7 unknowns, 7 data points, `c=640..655360`, no least
squares, no free parameters) and separately on four nested/dropped
subsets, using the spread across subsets as a naive per-coefficient
stability estimate (full output: `r04_asymptotics_fit.log`):

```
d0 = 0.99999999999751694440554077362322   (fit, all 7 points)
d1 = -1.5957691175605389395914598244531
d2 = 3.4999977907731462524579468370944
d3 = -9.0421694016773018703251060350962
d4 = 26.066499250885012496192967538507      (poorly conditioned beyond here)
d5 = -79.018153796861954956074988262355
d6 = 191.85788039330648028313671105115
```

Comparison against the DERIVED closed-form predictions (§4):

| coeff | predicted (DERIVED, §4) | fit value | `fit - pred` | agreement |
|---|---|---|---|---|
| `d0` | `1` | `0.999999999998...` | `-2.5e-12` | ~12 digits |
| `d1` | `-2*sqrt(2/pi) = -1.59576912160573...` | `-1.59576911756...` | `+4.0e-9` | ~9 digits |
| `d2` | `7/2 = 3.5` | `3.49999779...` | `-2.2e-6` | ~6 digits |
| `d3` | `-(34/3)*sqrt(2/pi) = -9.04269168910...` | `-9.04216940...` | `+5.2e-4` | ~4.2 digits |
| `d4` | CONJECTURED `209/8 = 26.125` (§4.4b) | `26.0664992...` | `-5.9e-2` | ~2.6 digits (weak; predictor itself unproven) |
| `d5` | CONJECTURED `-(1546/15)sqrt(2/pi) = -82.2353...` | `-79.0181...` | `+3.2` | not meaningfully constrained |

**Reading this honestly:** `d0, d1, d2, d3` — every coefficient this
front's own matched-asymptotics derivation (§4.2-§4.4b) actually PROVED
(modulo H1/H2) — are confirmed by an INDEPENDENT numerical route (exact
series summation at 7 values of `c`, zero shared machinery with the
matched-asymptotics derivation beyond the recursion itself) to `12, 9, 6,
4` digits respectively, decreasing with order exactly as expected for a
polynomial fit of finite, noisy-in-the-sense-of-truncated data (the raw
`(K,dps)`-limited precision at each `c`, `~110-121` digits, ultimately
caps how many `eps`-orders a degree-6 fit can resolve — this is a fit
conditioning limit, not a sign the law is wrong). `d4`'s comparison to the
CONJECTURED `209/8` is weak (`~2.6` digits) and the fit's own internal
cross-subset stability check independently flags `d4` as "stable to ~0
digits" (i.e. the fit does not even trust its own `d4` — see
`r04_asymptotics_fit.log`), so this is reported as "not excluded, weakly
consistent", never as a confirmation. `d5, d6` are fit artifacts of an
over-determined polynomial degree pushed past what 7 data points can
resolve and carry no evidential weight.

**Independent out-of-sample holdout (`c=250`, 46 digits, NEVER a fit
input):**

```
y_measured(c=250)         = 0.911136355369126
y_fit_extrapolated(c=250) = 0.911136564654532   (from the degree-6 fit above)
relative difference       = 2.297e-7
```

This is the single most convincing confirmation in this section: `c=250`
is `2.56x` outside the fit's `c`-range (`640..655360`) on the LOW-`c`
side, computed by an entirely separate, independent run (different `K`,
different `dps`, §2.2/§3), and the full 7-term polynomial extrapolation
still lands within `2.3e-7` relative — far tighter than an unconstrained
degree-6 polynomial would be expected to extrapolate by chance, and
consistent with the fitted coefficients genuinely tracking the true
`eps`-expansion of `Pi(c)` rather than overfitting 7 numbers.

**Conclusion of this section:** the four-term law of §4.4b is DERIVED
(heuristic, `n<=4`) and independently CONFIRMED numerically to `4-12`
digits per coefficient plus a clean out-of-sample check; the conjectured
5th term is weak and unconfirmed; no claim is made about resummation into
a closed form for `Pi(c)` at finite `c` — that remains the open target
(§7, §10).

---

## 6. The plateau profile in `s` (analytic resolution of the wave-16
rank-2 tension)

§4's matched-asymptotics derivation is carried out for the FULL `s`-profile
of the plateau, not just its `s=0` value: writing `F(s) := lim_{g->inf}
Phi(s,g)` (so `F(0) = Pi(c)`), `x := s*sqrt(c)`, the same expansion gives

```
F(s) = eps*R(x) + eps^2*(2*x*R(x) - 2) + O(eps^3),   R(x) = sqrt(pi/2)*erfcx(x/sqrt(2))
```

— i.e. the plateau's `s`-DEPENDENCE, to leading order, is exactly the
SAME `erfcx` shape as the `k=1` series coefficient `psi1(s) = b_1(s) =
sqrt(pi c/2)*erfcx(s*sqrt(c/2))` from the record (§0): `R(x) = psi1(s)/
sqrt(c)` under the same rescaling. This is a DIRECT, quantitative
explanation of the wave-16 referee's SS5 finding that `Phi(s,g)` is
near-rank-2 with an `s`-profile matching `psi1`'s shape "to 3 significant
figures" (`PROOF_DEPENDENCY_MAP.md` node `FLOORH2` citation) — it is not a
numerical coincidence, it is the leading asymptotic term.

**Direct numerical test** (`r07_profile_check.py`, this front; deterministic,
reuses this front's own validated `(P,Q)`-family recursion evaluated at
`s>0` via the SAME polynomials, at `c=1000` and `c=2560`, `x in
{0, 0.5, 1, 2, 3}`, `ct0 in {230,260}` for a plateau-stability check —
full log `r07_profile_check.log`, `143s`/`136s` runtime):

| `x` | `c` | `F(s)` | `(F-eps*R)/eps^2` | predicted `2xR-2` | `resid3/eps^3` |
|---|---|---|---|---|---|
| 0.0 | 1000 | 0.037761598340... | -1.87167 | -2.0 | 4.058 |
| 0.0 | 2560 | 0.024021775588... | -1.91749 | -2.0 | 4.175 |
| 0.5 | 1000 | 0.026651014044... | -1.06206 | -1.12364 | 1.947 |
| 0.5 | 2560 | 0.016897163351... | -1.08419 | -1.12364 | 1.996 |
| 1.0 | 1000 | 0.020078232025... | -0.65618 | -0.68864 | 1.027 |
| 1.0 | 2560 | 0.012698105520... | -0.66790 | -0.68864 | 1.049 |
| 2.0 | 1000 | 0.013021626995... | -0.30324 | -0.31452 | 0.357 |
| 2.0 | 2560 | 0.008207982998... | -0.30735 | -0.31452 | 0.363 |
| 3.0 | 1000 | 0.009464425126... | -0.16757 | -0.17246 | 0.155 |
| 3.0 | 2560 | 0.005953839037... | -0.16936 | -0.17246 | 0.157 |

(the two-`ct0` plateau-stability check agrees to `~1e-97` to `1e-98` at
every row — the profile itself is at the same >=95-digit precision as §3's
`Pi(c)`, so this table's leading digits are not limited by numerical noise;
only the SHOWN digits are truncated for display.)

**Reading:** at every `x`, moving from `c=1000` to `c=2560` (smaller `eps`)
moves the measured 2nd-order residual `(F-eps*R)/eps^2` CLOSER to the
predicted `2xR-2` — exactly the direction and magnitude a genuine
`O(eps^3)`-suppressed correction should produce, and NOT what a wrong or
coincidental 2nd-order formula would do. The residual after subtracting
BOTH derived terms, `resid3 := (F - eps*R - eps^2*(2xR-2))/eps^3`, is
`O(1)` at every `(x,c)` and itself trends toward the §4.4 3rd-order
prediction `psi3(x)` as `c` grows (at `x=0`: `4.058 -> 4.175`, moving
toward the derived `psi3(0) = (7/2)sqrt(pi/2) = 4.3866...`; the two
`c`-values sampled are not deep enough into the asymptotic regime to
close the remaining gap, consistent with §5's `eps`-order-dependent
precision budget). This is an independent confirmation route from §5
(profile in `s` at fixed `c`, vs. plateau value at `s=0` across `c`) that
agrees with the SAME derived coefficients, using none of §5's data.

**Consequence for the wave-16 tension:** the near-rank-2 surface
`Phi(s,g) ~= e^{-cg} + (1-e^{-cg})*F(s)` (referee's no-fit ansatz) now has
`F` pinned to two full closed-form asymptotic orders plus a confirmed
trend at the third — the "why does a provably-coupled, nonlocal system
produce a near-separable solution" question (wave-16 SS5(2)) is answered,
AT LEADING ORDERS, by this profile being asymptotically IDENTICAL in shape
to the boundary-layer's own leading term (`psi1`), which is exactly the
referee's own conjectured "boundary-layer/plateau effect, expected to
sharpen with `c`" resolution — now derived, not just conjectured.

---

## 7. Identification attempts and exclusions (finite `c`)

`r05_identify.py` runs `mpmath.identify`/PSLQ over the >=110-digit `Pi(c)`
data as HYPOTHESIS GENERATION only (per mandate): every hit must be proved
or reported as "unproven candidate matching to N digits", every miss is an
exclusion "to the stated precision over the stated basis". Full output:
`r05_identify.log`.

### 7.1 A self-caught methodological bug, fixed before trusting any result

The version of this script left by the predecessor instance passed a bare
`1/c` (and, separately, a bare `c`) as an explicit PSLQ basis vector
alongside the constant `1`. For any SPECIFIC integer `c` not exceeding the
`maxcoeff` bound, PSLQ then immediately recovers the TRIVIAL identity
`c*(1/c) - 1 = 0` — a fact about the basis construction, not about `Pi` —
and, having found *a* relation, returns without searching for one that
actually involves `Pi`. **Symptom that exposed it** (before this was
understood as a bug): running the unmodified script produced apparent
"relations" at `c=250, 1000, 2560` (`-1*1 + 250*1/c = 0`, etc.) whose
printed expression showed NO `Pi` term at all (the display only prints
nonzero coefficients, and `Pi`'s coefficient in every one of these hits was
exactly `0`) — while `c=655360` alone, whose trivial coefficient
(`655360`) exceeds the `maxcoeff=1e4` used, correctly fell through to "NO
RELATION". Both observations are exactly what the trivial-identity
diagnosis predicts and nothing else would produce. **Fix**: removed the
bare `c`/`1/c` terms from both PSLQ bases (`erfcx`-family and
`ln`-space); `ln(c)` is retained (not a bare rational/integer, so it
cannot trivially self-cancel against `1`). Rerun gives clean, honestly
weaker (all "NO MATCH"/"NO RELATION") results, below. **Every number
downstream of this bug that survived to the drafted verdict was the
correctly-negative one** (the buggy run's own trivial hits were never
promoted to a claimed identity), but the ATTEMPT.md text this front
inherited did not yet reflect a bug-checked §7 — this front checked it
before writing anything here.

### 7.2 Full-constant identification (hypothesis generation)

`mpmath.identify(Pi(c), bases=[sqrt(2),sqrt(pi),pi,ln(2),e])` and the same
for `Pi(c)*sqrt(2c/pi)`: **NO MATCH** at `c = 250` (40 digits), `1000,
2560, 655360` (100 digits each) — 8/8 attempts. PSLQ against the
`erfcx`-family basis `{Pi, 1, erfcx(sqrt(c/2)), sqrt(pi*c/2)*erfcx(sqrt(c/2)),
1/sqrt(pi*c/2), erfcx(sqrt(c/8))}` (natural special-point evaluations of
the family `F` that provably generates every series coefficient, §0/§1):
**NO RELATION** at all 4 `c` values (`maxcoeff<=1e4`). PSLQ in log-space
(`ln Pi(c)` against `{1, ln(c), ln(pi)}`, testing power-law-times-Gaussian
forms `Pi = A*c^p*pi^q`): **NO RELATION** at all 4 `c` values
(`maxcoeff<=1e3`). **12/12 identification attempts: no candidate found**
to the stated precision over the stated bases.

### 7.3 Cross-`c` exclusion of simple closed-form families

These tests are NOT affected by the §7.1 bug (they compare fitted
predictions against independently-computed `Pi(c)` values, no bare
`c`/`1/c` PSLQ basis vectors involved):

- **2-term family** `Pi(c) = a/sqrt(c) + b/c`: fit exactly on `c=1000,
  40960`, tested out-of-sample: `c=655360` mismatches by `3.6e-4`
  relative, `c=250` by `5.6e-3` relative — both `EXCLUDED` (many orders of
  magnitude above the `>=1e-40`-ish precision floor of the input data).
  This is exactly consistent with the derived, confirmed `d2=7/2 != 0`
  (§4.3/§5): a 2-term family cannot be right because a genuine, nonzero
  `eps^2` term exists.
- **3-term family** `Pi(c) = a/sqrt(c) + b/c + g/c^1.5`: fit exactly on
  `c=1000, 40960, 655360`, tested out-of-sample at `c=2560`: mismatches by
  `2.6e-5` relative — `EXCLUDED`, consistent with the derived, confirmed
  `d3 != 0` (§4.4b/§5): a 3-term TERMINATING family cannot be right either,
  because a genuine, nonzero `eps^3` term exists.
- **Any function whose `eps`-expansion contains ONLY EVEN powers of
  `eps`** (equivalently, any function that is a genuine power series in
  `1/c` alone — every rational function of `c`, e.g.): excluded outright
  by `d1 = -1.5957691... != 0` (confirmed to `~9` digits, §5) — such a
  family's `y(eps)` would have `d1=d3=d5=...=0` by construction, and
  `d1` is unambiguously, robustly nonzero.
- **A single term `A*erfcx(lambda*sqrt(c))` alone** (i.e. NOT combined
  with any polynomial prefactor): excluded even more simply, without
  needing any coefficient beyond `d0`. As `c->infty` with `x:=
  lambda*sqrt(c)=lambda/eps->infty`, `erfcx(x) ~ 1/(x*sqrt(pi))*(1 -
  1/(2x^2) + ...)`, i.e. `A*erfcx(lambda*sqrt(c))` is `O(eps)` — it has NO
  `eps^0` term at all, so it cannot match `Pi(c)*sqrt(2c/pi) -> 1` (the
  DERIVED, numerically-confirmed-to-12-digits `d0=1`, §4.2/§5) at leading
  order, regardless of `lambda` or `A`. (Correction, this front: an
  earlier internal draft of this reasoning conflated "even in `eps`" with
  "a pure `erfcx` term", which are not the same family and are excluded
  for two DIFFERENT reasons, stated separately above, to avoid
  perpetuating a loose argument into the record.)

  > **[Correção pós-adversarial, 2026-08-26 — `DISC-DEC-077`.]** O
  > referee hostil mostrou que a correção acima ainda não havia
  > "aterrissado" por completo: tomando `Pi_candidate(c) :=
  > A*erfcx(lambda*sqrt(c))` literalmente e reescalando exatamente como
  > `y := Pi(c)*sqrt(2c/pi)` é definido no resto do documento, o termo
  > `eps^0` de `y_candidate` NÃO é identicamente zero — é possível
  > escolher `A` de modo que `d0=1` seja igualado exatamente (verificado
  > numericamente pelo referee em `c=1e2,\ldots,1e12`). O que de fato
  > exclui esta família é o mesmo mecanismo do item anterior: seu termo
  > `eps^1` (`d1`) é identicamente zero, contradizendo o `d1\ne0`
  > independentemente confirmado (§4.4/§5) — ou seja, `y_candidate` é um
  > subconjunto próprio de "par em `eps`", não uma família excluída "por
  > uma razão diferente" via `d0`. A conclusão prática (esta família está
  > excluída) permanece **inalterada** — segue imediatamente do `d1\ne0`
  > já estabelecido no item anterior — apenas a justificativa deste item
  > (a alegação de "não precisa de nenhum coeficiente além de `d0`" e de
  > "duas razões DIFERENTES") estava incorreta e é retirada por esta
  > nota. Nenhum outro resultado deste documento depende deste item.
  > Fonte: `adversarial/REFEREE_REPORT.md` §6.

### 7.4 What this section does and does not establish

**Established**: no relation among the tested natural constants/special
functions was found to the tested precision (§7.2); several natural
"terminating" or "single-erfcx-term" closed-form GUESSES are genuinely,
numerically excluded (§7.3), consistent with (not merely orthogonal to)
the derived asymptotic law's own nonzero coefficients. **NOT
established**: that no closed form exists at all — these are exclusions
over a finite, named list of candidate families/bases, not an
impossibility proof, and PSLQ over a much larger basis (e.g. including
higher special-point evaluations of `F`, or genuinely combining
`P(s)+Q(s)*erfcx(...)`-style structure in the `c`-variable rather than
just evaluating at fixed points) was not attempted — named here as a
concrete, not-yet-executed next avenue (§10).

---

## 8. Test log (all deterministic; no seeds)

| ID | script | purpose | result |
|---|---|---|---|
| T1 | `r01_family_series.py` | fresh `(P,Q)`-family recursion implementation; validation against 10 published anchors (`a_2..a_4(0)`, `b_2(0)`, closed forms, `Phi(0,0.002)`, plateau at 2 `t0`) | **10/10 PASS** (`r01_family_series.log`) |
| T2 | `r02_symbolic_check.py` | independent symbolic (sympy, SYMBOLIC `c`) re-derivation: `erfcx'` identity, `b_k` ODE residuals `k=1..5`, closed forms of record | **ALL PASS, residuals exactly 0** (`r02_symbolic_check.log`) |
| T3 | `r03_plateau_multi_c.py` (jobs `ladder`, `control`) | `Pi(c)` at 7 values, `>=110` digits, plus roundoff-control rerun (`c=1000` at `dps=440`) | **7/7 succeeded**; control run identical to ladder run at all 121 printed digits (`r03_ladder.log`, `r03_control.log`) |
| T4 | `r03_plateau_multi_c.py` (job `fixmid`) | independent-parameter cross-check (`c=640` at different `K`/`dps`) + attempted recovery of `c=160,250` | `c=640`: identical to T3 at all 121 digits; `c=250`: 46 digits recovered (expensive, `736s`); `c=160`: did not complete (`r03_fixmid.log`) |
| T5 | `r03_plateau_multi_c.py` (jobs `c100deep`,`c40deep`,`c10mid`,`c1small`) | attempted `c=100,40,10,1` | **all 4 FAILED to produce output** (0-byte logs); confirmed by this front (`ls -la`) before being excluded from every downstream table (§2.2, §3) |
| T6 | `r03_plateau_multi_c.py` (job, uniform first pass) | uniform `(K,dps)` sizing at `c=1,10` (predecessor's first, uncorrected attempt) | pure cancellation garbage (`stable_digits=0`, sums `~1e+1866`,`~1e+1132`), caught by this front's own re-inspection of `r03_plateau_multi_c.log` (self-caught issue S1, §9) — used nowhere in this document except as the negative example in §2.2 |
| T7 | `r03b_borel.py` | Borel-Laplace resummation attempt, `c=1,10` | **FAILS numerically** as predicted by the order-2 analysis (§2.3): `max|B| ~ 1e1237` at `c=1` (`r03b_borel.log`) — disclosed failed route, not used for any number in the record |
| T8 | `r04_asymptotics_fit.py` (this front; fixed a predecessor crash bug, §9 S3) | exact polynomial fit of the derived asymptotic law against the 7-value `>=110`-digit table + `c=250` holdout | `d0..d3` confirmed to `12,9,6,4` digits; `c=250` holdout `2.3e-7` relative (§5); `r04_asymptotics_fit.log` |
| T9 | `r05_identify.py` (this front; fixed a predecessor methodological PSLQ bug, §9 S4) | `mpmath.identify`/PSLQ hypothesis generation + cross-`c` exclusion tests | 12/12 identification attempts NO MATCH/NO RELATION; 3/3 family-exclusion tests EXCLUDED as expected (§7); `r05_identify.log` |
| T10 | `r06_asymptotic_derivation.py` (predecessor's derivation; independently RE-RUN by this front before trusting it) | matched-asymptotics derivation of the 4-term (+conjectured 5th) law, 18 machine-verified groups | **ALL 18 GROUPS PASS**; this front's fresh rerun byte-identical to the inherited log, confirming determinism (§4.4b) |
| T11 | `r07_profile_check.py` (this front) | direct numerical test of the derived `s`-profile `F(s)` at `c=1000,2560`, `x=0,0.5,1,2,3` | residuals trend toward derived predictions as `c` grows, at every `x`, in both directions tested (§6); `r07_profile_check.log` |

All tests deterministic; no randomness anywhere in this front (confirmed:
`grep -rn "20260866" 05_DISCOVERY_LAB/` matches only the ledger's and
`TEST_QUEUE.yaml`'s reservation lines — the reserved seed range was never
needed or drawn from).

---

## 9. Self-caught issues (disclosed)

**S1 (inherited from the predecessor instance, verified genuine by this
front).** A first, uniform-`(K,dps)` attempt at the multi-`c` plateau
computation produced pure cancellation garbage at small `c`
(`c=1`: sums `~1e+1866`; `c=10`: `~1e+1132`) — caught immediately by the
`max|term|`/stable-digits diagnostics built into `r03_plateau_multi_c.py`
(`stable_digits=0` reported honestly, never silently dropped). This front
re-inspected the raw log (`r03_plateau_multi_c.log`) itself rather than
trusting the predecessor's characterization, and confirms the diagnosis:
these are not usable numbers at any precision, and are used nowhere in
this document except as the illustrating negative example in §2.2/T6.

**S2 (inherited, verified genuine by this front).** The first Borel-Laplace
run's transform values were flagged by their own `max|B|` diagnostic and a
`Phi>1` sanity check before being trusted; re-inspection of
`r03b_borel.log` confirms the disclosed failure mode (`max|B| ~ 1e1237` at
`c=1`) is real and the route is correctly abandoned (§2.3).

**S3 (this front's OWN catch).** `r04_asymptotics_fit.py`, as left by the
predecessor instance, referenced an undefined variable `d1_pred` at its
final JSON-dump step — a guaranteed `NameError` crash on any run. This
means the predecessor's own `r06` four-term (`n<=4`) asymptotic
derivation had NEVER been numerically validated against the multi-`c`
data before the front stalled: the un-updated top-of-document verdict
this front inherited stated only a THREE-term law, silently short of what
`r06`'s own log already showed derived. Fixed (added the missing
`d2_minus_pred`/`d3_minus_pred` fields, guarded the `j<7` print/stability
loop against subsets shorter than the full fit at high polynomial order —
a second, smaller bug in the same script, `max() arg is an empty
sequence` at `j=6`, also fixed) and rerun; the fix surfaced the genuine
`~4`-digit numerical confirmation of the 4th-order term reported in §5,
which is new to this document (was never computed before).

**S4 (this front's OWN catch, more serious than S3 — a methodological
bug, not just a crash).** `r05_identify.py`'s PSLQ tests against the
`erfcx`-family and log-space bases included a bare `1/c` (respectively
`c`) as an explicit basis vector alongside the constant `1`. For any
integer `c` within the `maxcoeff` bound, PSLQ then trivially recovers
`c*(1/c)-1=0` — a fact about the basis, not about `Pi` — and stops before
finding anything meaningful. **How it was caught**: the printed
"relations" for `c=250,1000,2560` showed `Pi`'s own coefficient as exactly
`0` in every case (only nonzero terms are printed, so this was visible
directly), and `c=655360` (the one value whose trivial coefficient,
`655360`, exceeds `maxcoeff=1e4`) alone returned "NO RELATION" — a pattern
with no explanation except the trivial-basis diagnosis. Full detail and
fix: §7.1. **Consequence, stated honestly**: nothing in the predecessor's
inherited state had promoted a spurious hit into a claimed identity (the
draft's §7 was still a placeholder when this front began), so no false
positive ever reached a reader — but had this front simply "filled in the
placeholder from the old logs" per the mandate's explicit warning, it
would have reported several fabricated near-relations as genuine PSLQ
findings. This is the clearest instance in this front's work of exactly
the failure mode the mandate warned against, caught by re-deriving and
re-running rather than transcribing.

**S5 (this front's OWN finding, a cost/feasibility diagnosis rather than a
code bug).** The predecessor's queued jobs for `c=100,40,10,1` (`K` up to
`16000`, `dps` up to `1200`) never produced any output — 0-byte log files.
This front verified this is a genuine, quantifiable cost wall rather than
a stray crash: extrapolating the `c=40` job's requested `(K,dps)` against
this front's own freshly-confirmed `c=1000` runtime (`163.5s` at
`K=2000,dps=360`) via the recursion's `O(K^2)` descending-solve cost
gives `~9.7` hours — correctly out of budget, and NOT re-attempted by this
front, per the mandate's explicit anti-stall instruction. Full detail:
§2.2/§3.

---

## 10. What remains open

1. **No exact closed form for `Pi(c)` at any finite `c` was found.**
   Inverse-symbolic search (§7) excludes several natural candidate
   families to the tested precision but is not, and cannot be, exhaustive.
   A genuinely different search — e.g. PSLQ over a richer basis built from
   `F`'s own `s`-dependent structure rather than fixed evaluation points,
   or a targeted search for `Pi(c)` as an INTEGRAL of the closed-form
   `(P,Q)`-family itself (the coefficients are all in `F`; `Pi(c) =
   lim_K sum a_k(0) t0^k` for `t0->infty` inside the radius, so there may
   be an exact integral-transform identity for the LIMIT that this front
   did not look for) — is a concrete, not-yet-executed next avenue.
2. **Resummation into a closed generating function was not achieved.**
   Plain Borel(-1) is shown structurally wrong (§2.3: the transform itself
   has non-Borel-class growth). No alternative resummation method
   (Borel-2+, a Mellin/Watson-transform representation of the exact
   `(s,g)`-PDE system rather than just its asymptotic expansion, a direct
   attack on the exact renewal equation `(E2)` of §4.1 at `s=0,
   g->infty`) was attempted in this front. This is the single largest
   gap relative to the mandate's stated first-choice target ("resum the
   series").
3. **The `gamma_n` all-orders pattern (§4.4b) is unproven beyond `n=4`.**
   `gamma_5=209/24` and beyond are a numerically-motivated extrapolation,
   not derived by carrying this front's own matched-asymptotics machinery
   to a 5th boundary-layer order — and the numerical fit (§5) only weakly,
   inconclusively constrains `d4` (`~2-3` digits) and says essentially
   nothing about `d5`. Carrying the derivation one more order (following
   the exact pattern of §4.4b/V15-V17) is mechanical but was not done here.
4. **The low-`c` range (`c<250`) is inaccessible to the direct-summation
   method within any reasonable budget** (§2.2, S5) — a fundamentally
   different, faster method for small `c` was not found. This matters
   beyond mere completeness: it is direct evidence that the "just sum the
   series" approach, however exact, is not itself the closed form the
   mandate is asking for — a genuine resummation would presumably also
   solve this practical problem, which is a useful, checkable target for
   any future candidate closed form (`c<250` values it predicts can be
   checked against `c=250`'s 46 known digits, and, at real additional
   cost, against a fresh direct computation).
5. **The two heuristic gaps (H1, H2, §4.5) in the matched-asymptotics
   derivation are not rigorously closed.** A fully rigorous PROOF of even
   the 4-term law (as opposed to a derivation with every algebraic step
   machine-verified, plus strong independent numerical confirmation) would
   need to either justify the Watson/matched-layer framework's uniform
   validity directly from the exact `(s,g)`-PDE system (not attempted
   here) or find an entirely different, rigorous route to the same
   coefficients (e.g. from the exact `(P,Q)`-family coefficients
   themselves, via a genuine asymptotic analysis of the coefficient
   sequence `a_k(0)` as `k->infty` at fixed large `c`, rather than the
   `eps->0` matched-layer route used here — a DIFFERENT, not-yet-tried
   angle on the same question).
6. **§6's `s`-profile `F(s)` is confirmed only to 2 full asymptotic orders
   plus a numerically-trending 3rd** — a full closed form for `F(s)` at
   finite `c` (not just its `eps`-expansion) was not attempted, though the
   same `(P,Q)`-family machinery that generates every `Phi(0,t0)` series
   coefficient (§1) presumably also generates every `Phi(s,t0)` coefficient
   at fixed `s>0` (used directly by `r07_profile_check.py`, §6) — so a
   `g->infty` limit of THAT series, for general `s`, is the natural next
   step, structurally identical to the (unsolved) `s=0` resummation
   problem.
7. **The abstract-vs-real `~30%` gap and any connection to the real
   `n=65536` engine remain completely untouched**, as explicitly scoped by
   the mandate (no claims made anywhere in this document about the real
   engine).

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `phi_U(c)`, `phi_infinity(c)` are all untouched and unaffected.

---

## 11. Files

| file | role |
|---|---|
| `r01_family_series.py`/`.log` | fresh `(P,Q)`-family recursion implementation + 10-anchor validation (§1) |
| `r02_symbolic_check.py`/`.log` | independent sympy symbolic re-derivation, symbolic `c` (§1) |
| `r03_plateau_multi_c.py` | multi-`c` plateau computation, all jobs (`ladder`,`control`,`fixmid`,`c100deep`,`c40deep`,`c10mid`,`c1small`) (§2, §3) |
| `r03_plateau_multi_c.log`, `r03_plateau_values.json` | original small-set (`c=1,10`) first-pass log — the S1 negative example (§9) |
| `r03_ladder.log`, `r03_plateau_values_ladder.json` | PRIMARY 7-value `>=110`-digit table (§3) |
| `r03_control.log`, `r03_plateau_values_control.json` | roundoff-control rerun, `c=1000` (§2.1, §3) |
| `r03_fixmid.log`, `r03_plateau_values_fixmid.json` | independent-parameter cross-check (`c=640`) + `c=250` holdout recovery; `c=160` incomplete (§3) |
| `r03_c100deep.log`, `r03_c40deep.log`, `r03_smallc.log` | empty (0 bytes) — never-completed jobs, disclosed in §3/§9 S5, not deleted |
| `r03b_borel.py`/`.log` | disclosed failed Borel-Laplace resummation attempt (§2.3) |
| `r04_asymptotics_fit.py`/`.log` | polynomial fit of the derived law against the multi-`c` table; predecessor crash bug fixed by this front (§5, §9 S3) |
| `r05_identify.py`/`.log` | `mpmath.identify`/PSLQ hypothesis generation + exclusions; predecessor methodological bug fixed by this front (§7, §9 S4) |
| `r06_asymptotic_derivation.py`/`.log` | matched-asymptotics derivation, 18 machine-verified groups (4-term law + conjectured 5th); independently re-run by this front, byte-identical (§4, §4.4b) |
| `r07_profile_check.py`/`.log` | this front's own script: direct numerical test of the derived `s`-profile `F(s)` (§6) |
| `.done_ladder` | empty marker file left by the predecessor instance (harmless; not referenced by any script; left in place) |
| `ATTEMPT.md` | this document |

No git commit made. No `adversarial/` subdirectory created (per mandate,
no referee dispatched by this front). Nothing written outside this
`plateau_resummation_attempt/` subdirectory — the parent
`floor_h2_b1_full_closure_attempt/*.py`/`ATTEMPT.md`/`adversarial/`, the
grandparent `floor_closed_form_attempt/*`, and `PROOF_DEPENDENCY_MAP.md`
further up the tree were read-only references (§0), never modified.
