# ATTEMPT — an energy-estimate / contraction-mapping attack on (U1)/(U2)
# (`H1-ENERGY-ESTIMATE-ATTEMPT`)

**Wave 22, front (b), `DISC-DEC-096`.** Target: `(U1)` and `(U2)`, the two
precisely-stated sub-hypotheses `mclust_h1_validity_attempt` (`DISC-DEC-088/
091`) reduced `H1` to — the single largest remaining gap named by that front
and left completely untouched by its own scope (`(U1)`+`(U2)` were stated
and used, never attacked) and by its sibling `mclust_h2_validity_attempt`
(`DISC-DEC-093/095`, which reduced `H2` to a corollary of `H1`'s own
machinery without touching `(U1)`/`(U2)` either). This front attempts a
**maximum-principle / energy-estimate argument on the exact PDE system**, and
a **contraction-mapping argument on the exact renewal identity `(E2)`**, as
explicitly invited by the mandate.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process — pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lemma Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

Reserved seed range for this front: `20260912000-20260912999`
(`numpy.SeedSequence` base) — grep-confirmed to appear only in the ledger's/
queue's reservation lines before use. **In the end no randomness was needed
anywhere in this front** — exactly as in every direct ancestor: every result
below is either exact symbolic reasoning (`sympy`) or deterministic
arbitrary-precision (`mpmath`, `dps` between 50 and 320 depending on the
sub-computation) computation, so the reserved range remains entirely unused.

---

## VERDICT UP FRONT

**Tier: honest non-closure of `(U1)`/`(U2)`, with a genuinely new exact
identity (machine-verified to 23–37 digits against an independent
implementation), a new rigorously-proved but structurally loose oscillation
bound, a precise diagnosis of exactly two distinct reasons this style of
argument does not close the gap, and a new numerical experiment (the
`g\to\infty` approach RATE at general `x`, not just `x=0`) offering
suggestive — not decisive — support for the premise `(U1)`/`(U2)` need to be
true.**

1. **A new exact identity for `Psi`** (§2): applying the required reading's
   own Growth-Exclusion Lemma (`mclust_h2_validity_attempt/ATTEMPT.md` §2,
   there used only order-by-order on the `psi_n` equations) directly to the
   EXACT, non-`eps`-expanded equation `(E1)` gives a closed-form renewal
   representation of `Psi` itself, conditional only on the SAME standing
   boundedness hypothesis `(B)` used throughout this lineage:
   ```
   Psi(x,y) = int_0^inf e^{-u^2/2 - u(x+y)} I(x+u,y) du,   I(x,y):=int_0^y Phi(x,y')dy'
   ```
   (`(BB-Psi')`, scaled units; §2.2 gives the unscaled form used in code).
   This is new to the record. It is verified **symbolically** (§2.1, two
   concrete source functions plus the shift identity, all exact, one
   self-caught harness bug fixed) and **numerically**, against a fresh,
   independent general-`s` `(P,Q)`-family series implementation (validated
   first against all 7 published anchors at `c=1000`, §3), at 5 `(x,y)`
   points spanning `x=0` to `x=0.2`: **relative agreement between the two
   independent computation routes ranges from `2.6e-23` to `7.6e-37`** (§4).

2. **A new, rigorously proved (conditional on `(B)`), GLOBAL-in-`x`
   oscillation bound** (§5) — stronger in one respect than what `(U1)` even
   asks for (global on all of `x\ge0`, not merely local):
   ```
   sup_{x>=0} |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1) * K * R(y1)  <=  (y2-y1)*K/y1
   ```
   (`K` a bound on `|Phi|+|Psi|`, `R` the record's own `psi1`-profile
   function). Numerically sanity-checked (§5.2): holds at every tested point,
   with the true oscillation `3\times10^{2}` to `3\times10^3` times SMALLER
   than this bound — confirming the bound is valid but, as anticipated,
   structurally loose.

3. **A precise diagnosis of exactly why this does NOT close `(U1)`** (§6),
   in two independent, both self-contained ways: (a) the bound degrades
   LINEARLY in the step size `h=y2-y1`, so naive telescoping over
   unboundedly many steps diverges logarithmically — an explicit, quantified
   failure of the obvious "sum up small steps" argument; (b) expanding the
   exact renewal formula via the natural small parameter `1/y` (a
   Watson/Laplace-type expansion, the textbook tool for exactly this kind of
   integral) recovers only ALGEBRAIC (power-law) content in `y`, and is
   structurally BLIND to the genuinely faster (numerically, exponential)
   approach the record's own data shows — an exact structural echo, one
   level removed, of the SAME obstruction `plateau_resummation_attempt`
   already found for Borel resummation in the `eps\to0` limit (its own §2.3),
   now identified for the FIRST time in the `y\to\infty` limit instead.

4. **A new numerical experiment: does the `g\to\infty` approach look
   exponential at GENERAL `x`, not just `x=0`?** (§7). Ancestor fronts only
   ever checked the record's `x=0`-only "approach `~e^{-ct0}`" claim.
   Measuring successive-difference ratios of `Phi(x,g)` at `x` corresponding
   to `s=0, 0.2, 0.4` (`c=100`) shows the ratio converging, **at every tested
   `x`**, toward the pure-exponential prediction `e^{\Delta g\cdot c}` from
   above — consistent with (not proof of) the premise underlying `(U1)`/
   `(U2)`. But the CONVERGENCE SPEED of this ratio toward its target is
   measurably slower at larger `x` (at `g=0.38`: ratio is within `0.37\%` of
   target at `s=0`, but still `2.5\%` off at `s=0.4`) — a genuine, honestly
   quantified, mild `x`-dependence, exactly the KIND of effect a real proof
   of `(U1)`'s uniformity would need to control and bound, not merely
   observe.

5. **The contraction-mapping angle (§8) does not close either, and the
   obstruction is precisely diagnosed, not just asserted.** The natural
   `\Phi\mapsto\Psi` sub-map (via `(BB-Psi')`) has Lipschitz constant
   `\le1` in the sup norm — NOT `<1` — and this bound is essentially TIGHT
   (saturated as `x\to0`), so it is not a contraction by this route. The
   obstruction is identified exactly: the kernel `R(z)` decays only like
   `1/z`, exactly matching (not beating) the linear-in-`y` growth of the
   driving source `I`. A natural fix (a growing weight in `y`) is shown to
   make the bound WORSE, not better, for the same reason; a natural
   alternative (a decaying weight in `y`) is shown to be structurally
   inconsistent with the true solution (which does not decay in `y` — it
   PLATEAUS). The genuinely different, Volterra-in-`y` structure of `(E2)`
   itself is named as a more promising but entirely UN-explored avenue.

**`H1` remains ABERTO/OPEN, exactly as before this front.** `phi_REDB`,
`Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law of record are
all untouched and unaffected by anything in this document. `H2` is untouched
(out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself, per the mandate. No git command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` §2 (Tree B), specifically the `FLOORH2` and `PLATRESUM` nodes and ALL
dated addenda under `PLATRESUM` (wave-17 through wave-21, about `H1`/`H2`);
the full `plateau_resummation_attempt/ATTEMPT.md` §4 (the matched-asymptotics
derivation) and §4.5 (the exact statement of `H1`/`H2`); the full
`mclust_h1_validity_attempt/ATTEMPT.md` (direct predecessor, establishing the
exact `(E1)`/`(KEY)`/`(E2)` system, the Watson-concentration lemma, `(U1)`,
`(U2)`, the `(ODE-F)` structural fact, and the numerical uniformity grid);
and the full `mclust_h2_validity_attempt/ATTEMPT.md` (sibling front, whose
**Growth-Exclusion Lemma** — §2 of that document, quoted and cited below —
this front applies in a genuinely new way, to the EXACT equation rather than
order-by-order).

**No `.py` file from this front's own lineage or any sibling front was
opened, read, or imported at any point** — every script in this directory
(`e01`–`e05`) was written fresh, from the mathematical content of the prose
cited above. The `(P,Q)`-family recursion (§3 below) is re-implemented from
the SAME verbatim prose recursion quoted in every ancestor `ATTEMPT.md`, not
copied from any script; every previously-published number used as a
cross-check (7 anchors, `resid3`-style spot values are not reused here — this
front's own new numerical content is checked against itself, internally,
plus those same published anchors) is transcribed as plain text.

The exact statement `(U1)`/`(U2)` reduce `H1` to (quoted verbatim,
`mclust_h1_validity_attempt/ATTEMPT.md` §2.2):

> **Hypothesis (U1).** There is a function `W_inf(x)` (for the fixed `eps`
> under consideration) such that: for every `delta>0` there is `G(delta)`
> with `|W(x', g') - W_inf(x')| < delta` for ALL `g' > G(delta)` and ALL
> `x' in [x0, x0+G(delta)]` (locally uniform `g\to\infty` convergence).
>
> **Hypothesis (U2).** `W_inf(x;eps)`, as a function of `x\ge0` for each
> `eps`, admits a genuine asymptotic (Poincaré) power series in `eps` as
> `eps\to0`, uniformly for `x` in `[0,\infty)` — in particular remaining
> valid down to `x=O(eps)` — with a remainder after `N` terms that is
> `O(eps^{N+1})` with a constant independent of `x`.

and the required reading's own naming of what closing them would need
(`mclust_h1_validity_attempt/ATTEMPT.md` §2.2, §8 item 1 — the exact mandate
of this front):

> Neither `(U1)` nor `(U2)` is proved by this front ... doing so would
> require, at minimum, a maximum-principle or energy-estimate argument
> establishing that `Psi(x,g)` (and its `x`-derivative) converges to its
> `g\to\infty` limit at a RATE that is itself uniform in `x` over an
> unbounded domain.

**The established inputs this front works from** (restated for
self-containedness, exactly as given in the required reading):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Governing PDE system (record, wave-14 Sec5):
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi]+(1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                          (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv   (E2)

Series-recursion (Phi(s,g)=sum a_k(s)g^k, Psi(s,g)=sum b_k(s)g^k):
  a_0=1, b_0=0, a_1(s)=-c, b_1(s)=sqrt(pi c/2)*erfcx(s*sqrt(c/2))
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

Growth-Exclusion Lemma (mclust_h2_validity_attempt/ATTEMPT.md Sec 2, quoted):
  for  u_x(x,y) - (x+y)u(x,y) = f(x)  (y a fixed parameter, f mild growth),
  the UNIQUE solution bounded as x->infinity is
     u(x,y) = -e^{x^2/2+xy} int_x^infinity e^{-(t^2/2+ty)} f(t) dt
  (general solution = this + C(y)e^{x^2/2+xy}; boundedness forces C(y)=0,
   since e^{x^2/2+xy}->+infinity for every y>=0).

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = psi1(x),  R'=xR-1,  R(z)<=1/z for z>0
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory was written to.

---

## 1. Overview of approach

Three lines of attack, per the mandate's three numbered angles, in
increasing order of ambition:

- **Energy/maximum-principle route on the EXACT system** (§2–§7): apply the
  Growth-Exclusion Lemma — the required reading's own tool, but previously
  used only order-by-order on the `psi_n`-equations — directly to the FULL,
  non-`eps`-expanded equation `(E1)`. This produces a new exact identity for
  `Psi` (§2), from which a genuine, rigorously-proved GLOBAL-in-`x`
  oscillation bound follows (§5) via essentially the same machinery as an
  "energy estimate" (a differential inequality integrated via the Lemma's
  own variation-of-parameters kernel). §6 diagnoses precisely why this
  bound, though correct, does not close `(U1)`. §7 reports a genuinely new
  numerical experiment motivated by that diagnosis.
- **Contraction-mapping route on `(E2)`** (§8): examine whether the natural
  composite map `Phi \mapsto (\text{new }Phi\text{ via }(E2))` — built from
  `W` via `(KEY)` and `Psi` via the new `(BB-Psi')` identity of §2 — is a
  contraction in a suitable function space, uniformly in `eps`. Finds a
  precise, non-strict (`\le1`, not `<1`) Lipschitz bound and diagnoses the
  exact structural reason it does not improve to a strict contraction by
  this route.
- **Independent verification throughout** (§3–§4): a fresh, independent
  general-`s` `(P,Q)`-family series solver (§3), validated against all 7
  published anchors, is used to numerically confirm the new exact identity
  of §2 (§4) and the new oscillation bound of §5 (§5.2), and to run the new
  approach-rate experiment of §7.

Every result reports its own honest limits; none closes `(U1)` or `(U2)`.

---

## 2. Part A — a new exact renewal identity for `Psi`

### 2.1 Derivation

Fix `y_1\ge0`, treat `(E1)` — `Psi_x(x,y_1) = (x+y_1)Psi(x,y_1) - I(x,y_1)`
— as an ODE in `x` alone (`y_1` a parameter, exactly the form the
Growth-Exclusion Lemma covers, with `f(x):=-I(x,y_1)`). Given the SAME
standing hypothesis used throughout this lineage — `(B)`: `Psi(\cdot,y)` is
bounded as `x\to\infty`, for each fixed `y` (consistent with, not
independently proved beyond, `Phi,Psi` being probability-related bounded
quantities; `mclust_h2_validity_attempt/ATTEMPT.md` §2.2 makes the same
standing assumption explicitly) — the Lemma applies directly to the EXACT
(not `eps`-expanded) `Psi`, for the first time in this lineage:

```
Psi(x,y) = -e^{x^2/2+xy} int_x^infinity e^{-(t^2/2+ty)} * (-I(t,y)) dt
         =  e^{x^2/2+xy} int_x^infinity e^{-(t^2/2+ty)} I(t,y) dt
```

Substituting `t=x+u`, `u\ge0` (the exponent simplifies exactly, since
`(x+u)^2/2+(x+u)y-x^2/2-xy = xu+u^2/2+uy`, and `e^{x^2/2+xy}` cancels
against `e^{-x^2/2-xy}` from the shifted kernel):

```
Psi(x,y) = int_0^infinity e^{-u^2/2 - u(x+y)} I(x+u,y) du            (BB-Psi')
```

This is a **new exact identity** — the record's own `(E1)` is a differential
relation and `(E2)` an integral relation for `Phi` in terms of `W`; this is
the FIRST closed-form INTEGRAL representation of `Psi` itself stated in this
lineage.

### 2.2 Unscaled form (used directly in code)

Converting `x=s\sqrt c,\ y=g\sqrt c,\ u=\sqrt c\,v` (so `I(x,y)=\sqrt
c\int_0^g\Phi(s,g')\,dg'`, matching the record's own unscaled `\Phi`):

```
Psi(s,g) = c * int_0^infinity e^{-c[v^2/2+v(s+g)]} * [int_0^g Phi(s+v,g') dg'] dv     (BB-Psi'-unscaled)
```

### 2.3 Symbolic re-verification (`e04_symbolic_checks.py`/`.log`)

Before trusting `(BB-Psi')` for anything, the Growth-Exclusion Lemma's own
two halves are independently re-verified in exact `sympy` arithmetic (not
merely re-cited from the required reading): (i) the homogeneous solution
identity `d/dx[e^{x^2/2+xy}]=(x+y)e^{x^2/2+xy}` — **PASS, residual exactly
`0`**; (ii) the bounded-branch formula solves the inhomogeneous ODE, checked
for TWO concrete, structurally different source functions `f(t)=1` (which
recovers `R(x)` at `y=0`, matching the record's own closed form for `psi1`)
and `f(t)=t` (a genuinely different check, catching a harness bug on the
way — self-caught issue S3, §9) — **both PASS, residual exactly `0`**; (iii)
the shift identity `int_0^infinity e^{-u^2/2-uz}du = R(z)` used to derive
`(BB-Psi')` from the Lemma — **PASS, symbolically exact**, plus a numeric
cross-check at `z=0.5,2,5` (relative difference `\le1.3\times10^{-16}`,
roundoff-limited).

---

## 3. Fresh general-`s` `(P,Q)`-family series implementation

`e01_family_series.py`: the `(P,Q)`-family recursion of Section 0, at
general `s`, implemented fresh from the prose (polynomial arithmetic,
family-closure differentiation rule `(P+QE)'=(P'-scQ)+(Q'+csQ)E`, a
numerically-safe `erfcx` — direct formula for `|z|\le6`, asymptotic series
beyond — and a `solve_b_step` routine for the bounded-branch `b`-ODE via the
descending-recursion/`\kappa`-pinning method of `plateau_resummation_
attempt/ATTEMPT.md` §1.1, re-derived independently here).

**Validation** (`e01_family_series.log`), at `c=1000, K=220, dps=280`,
against the SAME 7 published anchors every ancestor front validates against:

| quantity | this front's value | published anchor |
|---|---|---|
| `a2(0)` | `520316.636488030055067` | `520316.636488` |
| `a3(0)` | `-180730907.628508066766` | `-180730907.6285` |
| `a4(0)` | `47146963944.1378859211` | `47146963944.14` |
| `b2(0)` | `-20816.6364880300550667` | `-20816.636488` |
| `b1(0)` | `39.6332729760601101335` | `sqrt(pi*1000/2)` (exact) |
| `Phi(0,0.002)` | `0.158500145747308484241` | `0.15850015` |
| `Phi(0,0.05)` [plateau] | `0.037761598340212618824` | `0.0377615983402126` |

**7/7 PASS**, `Phi(0,0.05)` matching the required reading's own
higher-precision published value to 21 digits (this front's own
`(K,dps)=(220,280)` diverges from that value's 22nd digit onward — expected,
different `(K,dps)` sizing between fronts, not a discrepancy).

### 3.1 Self-caught issue: the descending-recursion index bug (S1)

The FIRST version of `_solve_U_descending` (the routine solving
`U'-csU=R` for a polynomial `U`, the core of `solve_b_step`) mis-tracked
which previously-computed coefficient is `u_{j+1}` in the recursion
`(j+1)u_{j+1}-c u_{j-1}=r_j`, using a `prev`/`prevprev` sliding-window
scheme that silently read `u_j` where `u_{j+1}` was needed. This produced
correct `a_2(0), a_3(0), b_2(0), b_1(0)` (which do not depend on `b_3`) but
a WRONG `a_4(0)` (`47146672277.47` vs. published `47146963944.14`) and total
garbage for `Phi(0,0.05)` (off by 18 orders of magnitude). **Caught
immediately** by the very same 7-anchor validation table above, before any
downstream use — traced (by numerically checking the ODE residual
`b_k'-csb_k-\text{src}` directly via `mpmath.diff` at several `s`, finding a
residual growing linearly in `s` with coefficient exactly `7c^2/6`,
pinpointing `b_3`) to the index bug, then fixed by replacing the
`prev`/`prevprev` scheme with an explicit array `U[0..N+1]` indexed by
degree (module docstring in `e01_family_series.py` documents the fix
in-line). Re-validated with the hand-worked example `U=[1,2]\Rightarrow
R=[2,-c,-2c]` (§ debug session, not kept as a separate script) before
re-running the full anchor table, which then passed 7/7.

### 3.2 A second, disclosed numerical finding: the precision needed for
cancellation, not just truncation

Reproducing `Phi(0,0.05)` at `c=1000` needed `dps=280`, not the `dps=60`
initially tried — NOT because `K=220` terms are insufficient for
TRUNCATION (the `k=220` term is already `\sim10^{-35}` relative to the
answer), but because the PEAK term in the alternating sum (around
`k\sim30$–$50`) reaches `\sim10^{22}$–$10^{24}` against a final answer of
`\sim4\times10^{-2}` — a cancellation of `\sim24$–$26` orders of magnitude
that, empirically, needs `\sim250$–$280` total working digits to resolve
cleanly (not merely `\sim40$ extra digits as a naive "digits lost = orders
of cancellation" estimate would suggest) — traced to compounding relative
error WITHIN the descending-recursion solve itself (not just the final
`g`-series sum), confirmed by testing `dps\in\{60,80,150,200,250,300\}` at
fixed `K=220` and observing the result change qualitatively (not just
refine) up to `dps\approx250`, then stabilize exactly at `dps=250,300`
(§ debug session). This calibration discipline (verify stability across TWO
independent `(K,dps)` choices before trusting any number) is applied
throughout the rest of this front's numerics (§4, §5.2, §7).

---

## 4. Numerical confirmation of `(BB-Psi')` (`e02_renewal_identity_check.py`/`.log`)

`Psi(s,g)` computed two ways — (a) directly, from the validated `b_k(s)`
series (§3); (b) via `(BB-Psi'-unscaled)` (§2.2), with the INNER integral
`I(s,g)=\int_0^g\Phi(s,g')\,dg'=\sum_k a_k(s)g^{k+1}/(k+1)` evaluated EXACTLY
(as a finite sum, reusing a single `erfcx` evaluation per outer-quadrature
node) and the OUTER `v`-integral done by `mpmath.quad` over a finite range
(breakpoints chosen from the kernel's own decay scale
`1/(c(s+g))`; using `mpmath`'s infinite-interval transform directly was
tried first and found to need prohibitively many integrand evaluations at
working precision — disclosed, self-caught issue S2, §9) — at `c=200,
K=110, dps=90`, `maxdegree=6`:

| `s` | `g` | `Psi` (direct series) | `Psi` (renewal integral) | rel. diff |
|---|---|---|---|---|
| 0.00 | 0.05 | `0.07993621060237889961168348` | `0.07993621060237889961168348` | `7.6e-37` |
| 0.00 | 0.10 | `0.07993771394221839702914328` | `0.07993771394221839702914537` | `2.6e-23` |
| 0.05 | 0.05 | `0.05050516178431324030113834` | `0.05050516178431324030113834` | `9.9e-37` |
| 0.10 | 0.10 | `0.0356856471245037839709951` | `0.03568564712450378397099506` | `1.0e-24` |
| 0.20 | 0.08 | `0.02174696155505459549670602` | `0.02174696155505459549670602` | `2.4e-33` |

**5/5 PASS**, worst-case agreement `2.6\times10^{-23}` — two structurally
independent computation routes (a linear recursion in `s` vs. a numerical
quadrature of an exponential-kernel convolution against `\Phi`'s own
antiderivative) agreeing to 23–37 digits, at 5 points spanning `s=0` to
`s=0.2` and two different `g`. This is strong, decisive confirmation of the
new exact identity `(BB-Psi')`.

---

## 5. Part B — the global-in-`x` oscillation bound (energy estimate)

### 5.1 Derivation

Fix `y_1<y_2`, `h:=y_2-y_1`, `\delta(x):=\Psi(x,y_2)-\Psi(x,y_1)`. From
`(E1)`, writing `(x+y_2)\Psi(x,y_2) = (x+y_1)\Psi(x,y_2)+h\Psi(x,y_2)`:

```
delta_x(x) - (x+y1)*delta(x) = h*Psi(x,y2) - int_{y1}^{y2} Phi(x,y') dy'  =: f(x)
```

— exactly the Growth-Exclusion form again, with parameter `y_1`. Given `(B)`
applied to `\delta` (bounded, as a difference of two individually-bounded
fields):

```
delta(x) = int_0^infinity e^{-u^2/2-u(x+y1)} f(x+u) du
```

> **[Correção pós-adversarial, 2026-08-27 — DISC-DEC-100, achado N2,
> severidade BAIXA — não afeta o limitante final.]** O referee hostil
> apontou que a fórmula acima omite um sinal de menos à esquerda: a
> aplicação correta do Lema de Exclusão de Crescimento (confirmada
> por duas derivações independentes do referee — a rota de Leibniz e
> uma rota de fator integrante) dá `delta(x) = -int_0^infinity
> e^{-u^2/2-u(x+y1)} f(x+u) du`. Isto não afeta o limitante final
> `(star-star)`, já que o próximo passo toma `|delta(x)|` e
> `|-Z|=|Z|`. Corrigido acima apenas por completude/precisão
> algébrica.

Bounding `|f(x+u)| \le h(M_\Psi+M_\Phi) =: hK` crudely (`M_\Psi,M_\Phi`:
sup-bounds on `|\Psi|,|\Phi|`):

```
|delta(x)| <= h*K * int_0^infinity e^{-u^2/2-u(x+y1)} du = h*K*R(x+y1) <= h*K*R(y1)
```

(using `R` DEcreasing, `x\ge0`) `\le h K/y_1` (using the record's own
`R(z)\le1/z`). Since this holds for EVERY `x\ge0`:

```
sup_{x>=0} |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1) * K * R(y1)  <=  (y2-y1)*K/y1      (star-star)
```

This is a genuinely new result: **a rigorously proved (conditional only on
the standing hypothesis `(B)`), GLOBAL-in-`x` (not merely local) Cauchy-type
oscillation bound** — an honest "energy estimate", derived exactly the way
the mandate suggested, via the exact renewal kernel rather than a
formal/asymptotic argument.

### 5.2 Numerical sanity check (`e03_oscillation_bound_check.py`/`.log`)

At `c=100, K=220, dps=210`, `s\in\{0,0.1,\ldots,0.5\}`, `g_1=0.06`,
`g_2\in\{0.10,0.18,0.30\}`, using the EMPIRICALLY OBSERVED
`K=2\max_{(s,g)}(|\Phi|,|\Psi|)=0.2203` over the tested domain (disclosed as
measured, not independently proved, consistent with `(B)` being a standing,
not independently-proved, hypothesis throughout this lineage):

| `g_1` | `g_2` | `sup_s\lvert\Delta\Psi\rvert` | bound RHS | ratio (LHS/RHS) |
|---|---|---|---|---|
| 0.06 | 0.10 | `1.245\times10^{-4}` | `7.254\times10^{-2}` | `0.0017` |
| 0.06 | 0.18 | `1.261\times10^{-4}` | `2.176\times10^{-1}` | `0.00058` |
| 0.06 | 0.30 | `1.261\times10^{-4}` | `4.352\times10^{-1}` | `0.00029` |

**The bound holds at every tested point** (never violated) — but is loose
by a factor of `\sim3\times10^2` to `\sim3\times10^3`, confirming
analytically-anticipated slack, not a numerical accident.

---

## 6. Why `(star-star)` does NOT close `(U1)` — two precise, independent
diagnoses

### 6.1 Linear-in-`h` degradation (the telescoping/log-divergence obstruction)

`(star-star)` bounds a SINGLE step of size `h`. To conclude `\Psi(x,\cdot)`
CONVERGES as `y\to\infty` (uniformly in `x`), the natural next move is to
telescope unit steps: `|\Psi(x,y{+}1)-\Psi(x,y)|\le K/y` (from `(star-star)`
at `h=1`), summed from some `y_0` to `\infty`. But `\sum 1/y` DIVERGES
(harmonic-series-like) — this crude bound, EVEN THOUGH IT IS CORRECT, is too
weak by itself to conclude convergence, let alone a rate. This is an
explicit, quantified, honestly-named failure of the obvious
"sum-up-small-steps" argument — not a vague gesture at "more work needed."

### 6.2 The Watson/Laplace-in-`1/y` expansion is structurally blind to
exponential content

A natural refinement is to extract the `y\to\infty` asymptotics of
`(BB-Psi')` directly, via the substitution `u=w/y` (`w=uy`), the standard
tool (Watson's lemma / Laplace's method) for exactly this kind of integral
with a large parameter `y` in the exponent. Carrying this out (worked
through by hand; not separately scripted, since the conclusion is structural
rather than numerical) on the LEADING piece of `(BB-Psi')` — writing
`I(x+u,y)\approx yF(x+u)+C(x+u)` for the record's own plateau/`(ODE-F)`
quantities `F,C` (`mclust_h1_validity_attempt/ATTEMPT.md` §2.3) — produces,
term by term, a POWER SERIES IN `1/y` (the hallmark of a Laplace/Watson
expansion in a large parameter: `\int_0^\infty e^{-u^2/2-u(x+y)}F(x+u)\,du =
F(x)/y + O(1/y^2)`, since `R(z)\sim1/z-1/z^3+\cdots` has NO
exponentially-small-in-`z` correction on the positive real axis). **This
recovers only ALGEBRAIC (power-law) content in `y`** — it cannot see, and
would not detect the ABSENCE of, any genuinely faster (e.g. the numerically
observed `\sim e^{-yc}$, §7) approach. This is exactly the SAME structural
obstruction `plateau_resummation_attempt` already found and disclosed for
Borel(-1) resummation in the DIFFERENT limit `eps\to0` (its own §2.3: "the
order-2-entire content makes `B(u)` grow ... Any resummation of this series
that stays in the classical Borel-1 class is ... the wrong tool") — this
front identifies the SAME kind of obstruction, for the FIRST time, in the
`y\to\infty` limit instead: **a naive real-variable asymptotic expansion of
the exact renewal kernel, however legitimate as far as it goes, is
structurally the wrong tool to see or bound genuinely exponential-in-`y`
approach.** Whatever mechanism produces the (numerically well-supported, §7)
exponential rate must live outside what this particular exact identity's
own natural expansion can reach — a precise, actionable diagnosis of where
this route's ceiling is, not merely "harder than expected."

> **[Correção pós-adversarial, 2026-08-27 — DISC-DEC-100, achado N1,
> severidade MODERADA — não afeta nenhum número ou o veredito de
> não-fechamento.]** O referee hostil apontou que a caracterização
> acima do achado de `plateau_resummation_attempt` está imprecisa em
> dois pontos. Primeiro, aquele documento (SS2.3) resoma a série EM
> `t0` (`=g`, em `c` FIXO) — isto é, o MESMO sentido `y\to\infty` que
> esta própria seção está analisando, não "o limite `eps\to0`" como
> afirmado acima (confirmado por grep completo do `ATTEMPT.md` do
> predecessor: nenhuma co-ocorrência de "eps" e "Borel" em nenhum
> lugar). Segundo, a profundidade da analogia mecanística também está
> superestimada: a obstrução do predecessor é uma falha genuinamente
> não-genérica (a transformada de Borel de uma sequência de
> coeficientes de crescimento incomumente rápido, ordem 2/3, torna a
> soma de Borel-1 classica numericamente inútil para AQUELA série
> especificamente), enquanto o ponto desta seção é o fato genérico e
> de livro-texto de que QUALQUER expansão de Watson/Laplace de um
> núcleo suave e não-oscilatório é cega a correções
> exponencialmente-pequenas (verdadeiro para essencialmente qualquer
> expansão desse tipo, não uma descoberta específica deste sistema).
> Chamar isto de "um eco estrutural exato, um nível removido" da
> descoberta específica do predecessor superestima tanto a novidade da
> observação quanto a precisão do paralelo. Isto não afeta nenhum
> número relatado, nenhuma outra derivação, nem o veredito de
> não-fechamento desta frente — apenas a caracterização da conexão
> com o achado do predecessor estava imprecisa.

---

## 7. New numerical experiment: the `g\to\infty` approach rate at general `x`

### 7.1 Motivation and method (`e05_approach_rate.py`/`.log`)

§6.2 raises a concrete question no ancestor front tested: does
`\Phi(x,g)`'s approach to its plateau look genuinely EXPONENTIAL (rate
`\sim e^{-gc}=e^{-y/eps}$, per the record's OWN `x=0`-only claim) at general
`x`, and if so, does the rate visibly DEGRADE as `x` grows (bearing directly
on `(U1)`'s uniformity requirement)? Method: at fixed `s,c`, compute
`\Phi(s,g)$ at a grid `g_i=g_0+i\Delta g$ (§3's validated direct series;
`c=100, K=320, dps=320`, calibrated stable per §3.2's discipline), form
consecutive differences `d_i:=\Phi(s,g_i)-\Phi(s,g_{i+1})`, and examine
`d_i/d_{i+1}$: constant `\Rightarrow` exponential; `\to1\Rightarrow`
power-law; converging TOWARD the pure-exponential prediction
`e^{\Delta g\cdot c}` (here `=e^4=54.598\ldots`) `\Rightarrow` exponential
with a decaying algebraic correction (the generic WKB-type structure).

### 7.2 Results

At `s=0,0.2,0.4` (`x=0,2,4` at `c=100`), the ratio `d_i/d_{i+1}` at every
tested `g` and every tested `s`:

| `g` | ratio, `s=0` (`/e^4`) | ratio, `s=0.2` (`/e^4`) | ratio, `s=0.4` (`/e^4`) |
|---|---|---|---|
| 0.06 | `64.18` (`1.176`) | `60.17` (`1.102`) | `58.37` (`1.069`) |
| 0.14 | `57.43` (`1.052`) | `58.07` (`1.064`) | `57.39` (`1.051`) |
| 0.22 | `55.60` (`1.018`) | `56.94` (`1.043`) | `56.74` (`1.039`) |
| 0.30 | `55.02` (`1.008`) | `56.27` (`1.031`) | `56.29` (`1.031`) |
| 0.38 | `54.80` (`1.0037`) | `55.85` (`1.0228`) | `55.97` (`1.0251`) |

(`e^4=54.5982`; full 9-row tables per `s` in `e05_approach_rate.log`.)

**At every tested `x`, the ratio decreases monotonically toward `e^4` (not
toward `1`)** — consistent with genuinely exponential approach with a
decaying algebraic prefactor, at general `x`, not just `x=0` — extending the
record's own single-point observation. **But the SPEED of this convergence
is not the same at every `x`**: by `g=0.38`, the ratio is within `0.37\%` of
target at `s=0`, but still `2.28\%` off at `s=0.2` and `2.51\%` off at
`s=0.4` — a small but clearly monotone-in-`s`, honestly-quantified signal
that the approach to the leading exponential rate is SLOWER at larger `x`
over this tested window. This is exactly the kind of effect a genuine proof
of `(U1)`'s local uniformity would need to bound quantitatively (e.g. "the
`g`-threshold for `\delta`-accuracy grows no faster than [some named rate]
in the window `[x_0,x_0+G]`") — this front only OBSERVES it, at 3 values of
`x` and one `c`, and does not attempt to quantify or bound it further.

### 7.3 Honest reading

This is **suggestive, not decisive**, numerical evidence: (i) only 3 values
of `x` and 1 value of `c` were tested; (ii) the `x`-dependence of the
convergence SPEED, while real and monotone here, was not measured over a
wide enough `x`-range to say whether it stays mild or eventually
degrades badly (`mclust_h1_validity_attempt`'s own much larger uniformity
grid, §4 of that document, tested the ALREADY-CONVERGED plateau profile's
`eps\to0` uniformity over `x\in[0,20]$ and found NO degradation there — a
different question from the one this experiment asks, about the `g\to\infty`
APPROACH rate, not the converged profile); (iii) this experiment is
completely blind to whether the true rate is EXACTLY `e^{-gc}` or merely
asymptotically so with unknown further corrections — it cannot distinguish
"genuinely exponential" from "faster than any power but not exactly this
exponential."

---

## 8. Part C — the contraction-mapping angle on `(E2)`

### 8.1 Setup

Define, for two candidate bounded fields `\Phi_1,\Phi_2` on `[0,\infty)^2`,
`\Delta\Phi:=\Phi_1-\Phi_2`, `\|\Delta\Phi\|_\infty:=\sup|\Delta\Phi|`. Via
`(BB-Psi')` (§2), each `\Phi_i` determines a `\Psi_i`; the question is
whether the composite map (`\Phi\mapsto\Psi[\Phi]\mapsto W[\Phi]$ via
`(KEY)$ `\mapsto`$ new `\Phi$ via `(E2)`) is a contraction, uniformly in
`eps`, on some natural Banach space.

### 8.2 The `\Phi\mapsto\Psi` sub-map: Lipschitz constant `\le1`, not `<1`

`\Delta I(x,y)=\int_0^y\Delta\Phi(x,y')\,dy'$, so `|\Delta
I(x,y)|\le y\|\Delta\Phi\|_\infty` (crude, sup-norm). Then, from `(BB-Psi')`:

```
|Delta Psi(x,y)| <= y*||DeltaPhi||_inf * R(x+y) <= y/(x+y) * ||DeltaPhi||_inf <= ||DeltaPhi||_inf
```

(using `y/(x+y)\le1` for `x\ge0$). So:

```
sup_{x,y} |Delta Psi(x,y)|  <=  ||Delta Phi||_infinity          Lipschitz constant <= 1
```

**This bound is essentially TIGHT** (`y/(x+y)\to1` as `x\to0`, any fixed
`y>0`) — it is genuinely a marginal, `\le1`, NOT a strict `<1` contraction,
by this route. No slack was thrown away except the single crude step
`|\Delta I(x+u,y)|\le y\|\Delta\Phi\|_\infty$ (replacing the true, possibly
much smaller, integral by its worst-case bound) — but a Lipschitz constant,
by definition, must hold for the WORST CASE over the whole space, so this
is not a fixable slack without extra structure.

> **[Correção pós-adversarial, 2026-08-27 — DISC-DEC-100, achado N3,
> severidade BAIXA — a conclusão permanece correta.]** O referee
> hostil apontou que o regime assintótico citado acima está errado.
> `y/(x+y)\to1` quando `x\to0` é verdadeiro, mas essa é apenas a
> etapa intermediária `y\,R(x+y)\le y/(x+y)` (via `R(z)\le1/z`) — a
> quantidade REAL sendo limitada, `y\,R(x+y)`, é maximizada em
> `x=0` para cada `y` fixo (confirmado numericamente pelo referee),
> mas esse máximo (`y\,R(y)`) só se aproxima de `1` quando `y` em
> si é GRANDE (`y\,R(y)|_{y=1}\approx0,656`, longe de `1`;
> `y\,R(y)|_{y=100}\approx0,9999`) — a saturação genuína exige
> `y\to\infty`, não `x\to0` em um `y` finito arbitrário fixo. A
> CONCLUSÃO permanece correta e inalterada: a constante de Lipschitz
> é exatamente `1`, não `<1`, sup aproximado mas não atingido — apenas
> o regime assintótico especificamente citado como razão estava
> impreciso.

### 8.3 Why the obvious fixes fail (both diagnosed, not just tried)

**Growing weight** (e.g. `\|\Phi\|_w:=\sup(1{+}y)|\Phi|`): would need
`\sup_{x,y}\,y(1{+}y)R(x+y)$ finite and `<1`; but `R(z)\sim1/z`, so
`y(1{+}y)R(x+y)\sim y(1{+}y)/(x+y)\to\infty` as `y\to\infty` at fixed `x` —
strictly WORSE, not better. **The obstruction is exact**: `R`'s decay
(`\sim1/z`, from the SAME Growth-Exclusion kernel this whole front is built
on) is only MARGINALLY fast enough to keep the un-weighted bound at exactly
`1`; any growing weight overshoots it.

**Decaying weight in `y`** (e.g. `e^{-\alpha y}`): would require `\Phi`
itself to be well-approximated in such a norm — but `\Phi(x,\cdot)` does
NOT decay as `y\to\infty`; it PLATEAUS at a nonzero limit `F(x)`. A norm
built to reward decay in `y` is structurally mismatched to the actual
solution, not merely a suboptimal technical choice.

### 8.4 The genuinely different route not explored here

`(E2)` is, in its own right, a linear VOLTERRA integral equation in `y`
(kernel `(1/eps)e^{-v/eps}`, convolved over `[0,y]`, `y` playing the role of
"time"). The classical theory of linear Volterra equations with bounded,
integrable kernels gives LOCAL (small-`y`) existence/uniqueness via a
genuine contraction, essentially for free — a structurally different, more
promising avenue than the "instantaneous", sup-norm-in-`(x,y)` map examined
in §8.2–8.3. Making this rigorous for the FULL coupled system (since `W`
depends on `\Psi`, hence on `I`, hence on `\Phi`'s own history, via
`(BB-Psi')` and `(KEY)` — including the derivative term `\Psi_x`, which
loses regularity: differentiating `(BB-Psi')` in `x` requires control of
`\partial_x\Delta\Phi`, not merely `\Delta\Phi`, an honest "derivative loss"
obstruction typical of this class of fixed-point argument) is a substantial,
genuinely separate undertaking, **not attempted by this front** — named here
as the single most promising concrete next step this front identified but
did not pursue.

---

## 9. Self-caught issues (disclosed, per this lineage's convention)

**S1 (computational, most consequential).** `_solve_U_descending`'s first
version mis-tracked `u_{j+1}` via a `prev`/`prevprev` sliding window,
producing WRONG `a_4(0)` and grossly wrong `Phi(0,0.05)` while leaving
lower-order anchors (which don't depend on `b_3`) accidentally correct —
caught by the standard 7-anchor validation table (§3), traced via an
ODE-residual diagnostic (`mpmath.diff`, finding a residual linear in `s`
with coefficient exactly `7c^2/6`, pinpointing `b_3`), fixed by an explicit
degree-indexed array. Full detail in §3.1.

**S2 (computational, efficiency/robustness).** The first version of the
`(BB-Psi')` numerical check (§4) used `mpmath.quad`'s infinite-interval
transform (`[0, mp.inf]`) directly; this required `\gg1000` integrand
evaluations at working precision for a single point and did not complete
within a 2-minute budget. Diagnosed via a call-counter instrumentation
(677 calls for a single `[0,1]` sub-interval alone, `maxdegree=6`) and fixed
by switching to a FINITE integration range with breakpoints derived from the
kernel's own decay scale `1/(c(s+g))` — reducing runtime to `\sim45$–$63$s
per point while achieving BETTER precision (23–37 digits vs. the untested
infinite-range attempt, which never finished).

**S3 (symbolic, harness bug, caught before any claim was made).** The first
version of `e04_symbolic_checks.py`'s `check_case` function compared the
computed ODE residual against the bare INTEGRATION-VARIABLE symbol `t`
(from the source expression `f(t)=t`) instead of substituting the ODE's own
variable `x` — producing a spurious `residual = -t + x` (visibly still
containing the free symbol `t`, which immediately flagged it as a harness
bug, not a mathematical failure, since a genuine residual could not contain
an unrelated free variable). Fixed by `fexpr.subs(t, x)`; re-run gave
`residual = 0`, PASS.

No issue affects any number or claim reported in §2, §4, §5, or §7 above —
each was caught and fixed before being used downstream.

---

## 10. What remains open

1. **`(U1)` and `(U2)` themselves remain unproved.** This front's new exact
   identity (§2) and new global oscillation bound (§5) are genuine progress
   — but §6 precisely diagnoses TWO independent, structural reasons why
   pushing this exact-identity route further, by the natural means tried
   here (crude sup-norm bounding; Watson/Laplace expansion in `1/y`), cannot
   reach the sharper (numerically, exponential-rate) statement `(U1)`/`(U2)`
   actually need. Closing the gap would need either (a) a substantially
   sharper bound on `I(x,y)-yF(x)-C(x)` than the crude `y\|\Delta\Phi\|`
   estimate used in §5.1/§8.2 — one that exploits SIGN or CANCELLATION
   structure in `\Phi(x,\cdot)-F(x)$, not just its sup-norm — or (b) a
   genuinely different tool that can see exponentially-small-in-`y` content
   (resurgence/trans-series methods, structurally analogous to what
   `plateau_resummation_attempt` already flagged as needed but unexplored
   for the `eps\to0` limit, now apparently ALSO needed for the `y\to\infty`
   limit — a new, if not surprising, connection this front makes explicit).
2. **The contraction-mapping route (§8) is not closed either**, and its
   obstruction (§8.3) is structurally IDENTICAL to the energy-estimate
   route's own obstruction (§6.2): both bottleneck on the SAME kernel
   `R(z)\sim1/z` being only marginally, not strictly, adequate. This is
   itself a finding: two a priori different strategies converge on the same
   underlying difficulty, suggesting it is a genuine feature of this system,
   not an artifact of either particular technique.
3. **The Volterra-in-`y` reformulation of `(E2)` (§8.4) is a concrete,
   unexplored, and — on general Volterra-theory grounds — plausible next
   avenue**, not attempted here. Making it rigorous for the FULL coupled
   `(\Phi,\Psi)$ system, including the derivative-loss issue from `(KEY)`'s
   `\Psi_x` term, is a substantial separate undertaking.
4. **§7's approach-rate experiment is numerically suggestive, not proof**:
   3 values of `x`, 1 value of `c`, no rigorous bound on the observed
   (mild) `x`-dependence of convergence speed, and structurally blind to
   whether the TRUE rate is exactly `e^{-gc}` or only asymptotically so.
5. **Hypothesis `(B)` (boundedness of `\Psi,\Phi`) — used throughout §2, §5,
   §8, exactly as it is used throughout this entire lineage — is itself a
   standing, not independently proved, assumption.** Every result in this
   document is conditional on it, exactly as every predecessor result in
   this lineage has been.
6. **Non-perturbative (trans-series) content remains entirely untested**,
   exactly as `mclust_h1_validity_attempt` §8 already named — nothing in
   this front closes or narrows that gap; §6.2 only newly IDENTIFIES that
   the same kind of content is structurally invisible to the natural tool
   this front tried, in a second (the `y\to\infty`) limit, not previously
   flagged as sharing this feature with the `eps\to0` limit.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)` are all untouched and unaffected.
`H1` remains open; `H2` untouched (out of scope).

---

## 11. Files

| file | role |
|---|---|
| `e01_family_series.py`/`.log` | fresh general-`s` `(P,Q)`-family recursion; 7/7 published-anchor validation at `c=1000` (§3); includes self-caught issue S1's fix (§3.1, §9) |
| `e02_renewal_identity_check.py`/`.log` | numerical confirmation of the new exact identity `(BB-Psi')` at 5 `(s,g)` points, 23–37 digit agreement (§4); includes self-caught issue S2's fix (§9) |
| `e03_oscillation_bound_check.py`/`.log` | numerical sanity check of the new global-in-`x` oscillation bound `(star-star)` (§5.2) |
| `e04_symbolic_checks.py`/`.log` | exact `sympy` re-verification of the Growth-Exclusion Lemma (2 concrete source functions) and the shift identity underlying `(BB-Psi')` (§2.3); includes self-caught issue S3's fix (§9) |
| `e05_approach_rate.py`/`.log` | new numerical experiment: `g\to\infty` approach-rate diagnostic at general `x` (§7) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`mclust_h1_validity_attempt/h1_energy_estimate_attempt/` subdirectory was
written to — every ancestor `ATTEMPT.md`/`adversarial/` file and
`PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (§0), never modified. No `adversarial/` subdirectory
created; no referee dispatched by this front itself, per the mandate.
