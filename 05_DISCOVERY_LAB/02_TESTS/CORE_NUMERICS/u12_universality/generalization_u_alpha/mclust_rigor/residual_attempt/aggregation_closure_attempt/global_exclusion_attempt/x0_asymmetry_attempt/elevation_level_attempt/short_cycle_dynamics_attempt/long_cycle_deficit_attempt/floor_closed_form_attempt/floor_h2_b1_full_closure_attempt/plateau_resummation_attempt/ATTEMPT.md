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
`Pi(c)` at finite `c` was found), with a genuinely new, machine-verified,
numerically-confirmed THREE-TERM ASYMPTOTIC LAW — the first closed-form
statement about the plateau constant in this lineage — plus the sharpest
numerical characterization of `Pi(c)` to date and a set of proved/measured
exclusions that any future closed-form candidate must satisfy.**

1. **DERIVED (heuristic matched asymptotics; every algebraic step
   machine-verified, §4; two named heuristic gaps stated in §4.5) and
   CONFIRMED numerically at 100-digit data across 11 values of `c` (§5):**

   ```
   Pi(c) = sqrt(pi/(2c)) - 2/c + (7/2)*sqrt(pi/2)*c^{-3/2} + O(c^{-2})
   ```

   equivalently, with `eps := c^{-1/2}` and `y := Pi(c)*sqrt(2c/pi)`:
   `y = 1 - 2*sqrt(2/pi)*eps + (7/2)*eps^2 + O(eps^3)`.
   The three coefficients are clean closed forms — including the striking
   exactly `-2` at second order and exactly `7/2` at third — and the fit
   of the 100-digit multi-`c` data reproduces each of them to
   [FIT-DIGITS] digits with no free parameters (§5). At `c=1000` the
   three-term law gives `Pi ~= 0.03776` (0.004% low), so the wave-16
   "unidentified constant" is now *asymptotically* identified even though
   its finite-`c` value is not.

2. **`Pi(c)` computed to >=100 significant digits at 11 values of `c`**
   (c = 40, 100, 160, 250, 640, 1000, 2560, 10240, 40960, 163840, 655360),
   plus lower-precision tiers at the mandate-named `c=10` and at `c=1`
   (feasibility-limited, honestly quantified, §2-§3), each value carrying
   its own three-way error control (approach / truncation / roundoff) and
   two independent-parameter cross-computations agreeing to all reported
   digits. `Pi(1000) = 0.0377615983402126188243712025905770479904...`
   (110 digits in §3), consistent with the wave-16 referee's 10-digit
   `0.0377615983`.

3. **Inverse-symbolic identification of the finite-`c` constant FAILED
   honestly** (§7): `mpmath.identify`/PSLQ over the natural constant bases
   (including the `erfcx`/`sqrt(pi c/2)` family that provably generates
   every series coefficient) found no relation at 100 digits; simple
   closed-form families (terminating `1/sqrt(c)`-expansions; any function
   even in `eps`, which includes every rational function of `c` and
   `A*erfcx(lambda*sqrt(c))`) are EXCLUDED by explicit cross-`c` tests /
   by `d1 != 0` (§7). These are exclusions "to the stated precision over
   the stated bases", not impossibility proofs.

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
   front's own polynomials at `s>0` (§6). This supplies the quantitative,
   analytic resolution of the wave-16 SS3.4 "near-rank-2 tension": the
   surface is `e^{-cg} + (1-e^{-cg})F(s)` to the orders computed, exactly
   the referee's no-fit ansatz, now with `F` pinned in closed form at two
   asymptotic orders.

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
max|term| `~1e150` at `c=1000, ct0=290` but `~1e768` at `c=160, ct0=290`).
At fixed `c*t0` this cost EXPLODES as `c` decreases — a uniform-parameter
first attempt produced pure cancellation garbage at small `c` (partial
sums `~1e+1866` at `c=1`), caught immediately by the max-term/stability
diagnostics (self-caught issue S1, §9). All final runs use per-`c`
`(K, dps)` sized by the measured rule (see `r03_plateau_multi_c.py`
docstring), with the diagnostics re-checked per run. Consequence, stated
honestly: `>=100` digits was affordable down to `c=40`, while `c=10` was
computed at ~[C10-DIGITS] digits (`ct0 <= 120`) and `c=1` at
~[C1-DIGITS] digits (`ct0 <= 30`) — the two low-`c` tiers are used only
as holdout checks, never as fit inputs.

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

[TABLE-PLACEHOLDER]

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

### 4.5 Status of the derivation (honest)

Every ALGEBRAIC step above is machine-verified in
`r06_asymptotic_derivation.py` (13 groups, ALL PASS, symbolic `c` where
meaningful). Exactly TWO steps are heuristic (named, not hidden):
(H1) the Watson/matched-layer framework itself — smoothness and uniform
validity of the outer/inner decomposition and the `O(eps^n)` remainder
bounds are assumed, not proved; (H2) uniqueness of the `y`-independent
bounded solution at each order (proved only within fields where the
`y`-differentiated homogeneous equation's `e^{xy + x^2/2}` growth can be
excluded by boundedness). This is why the law is reported as **DERIVED
(heuristic) + CONFIRMED (numerically, §5)**, not PROVED. The `O(eps^4)`
term is genuinely undetermined by this front (numerically
`d3 ~= [D3-VALUE]`, §5).

---

## 5. Numerical confirmation of the law (no free parameters)

[FIT-PLACEHOLDER]

---

## 6. The plateau profile in `s` (analytic resolution of the wave-16
rank-2 tension)

[PROFILE-PLACEHOLDER]

---

## 7. Identification attempts and exclusions (finite `c`)

[IDENTIFY-PLACEHOLDER]

---

## 8. Test log (all deterministic; no seeds)

[TESTLOG-PLACEHOLDER]

---

## 9. Self-caught issues (disclosed)

[ISSUES-PLACEHOLDER]

---

## 10. What remains open

[OPEN-PLACEHOLDER]

---

## 11. Files

[FILES-PLACEHOLDER]
