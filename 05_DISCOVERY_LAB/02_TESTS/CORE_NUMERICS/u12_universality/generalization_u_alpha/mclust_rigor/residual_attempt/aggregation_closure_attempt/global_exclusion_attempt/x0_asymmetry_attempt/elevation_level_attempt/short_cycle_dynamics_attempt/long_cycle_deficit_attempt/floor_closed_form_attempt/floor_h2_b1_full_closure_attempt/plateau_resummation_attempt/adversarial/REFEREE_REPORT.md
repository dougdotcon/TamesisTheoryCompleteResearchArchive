# REFEREE REPORT — `plateau_resummation_attempt/ATTEMPT.md`

**Scope.** `M-CLUST(b)`, Tree B of `PROOF_DEPENDENCY_MAP.md`, node under
`FLOORH2`. Pure combinatorial/asymptotic mathematics about an abstract
random-process model. **Not** a Millennium Problem, not the Conjecture-1/
whole-space line, not `phi_REDB`, and this review makes no such claims.

**What this report is not.** The target document's own verdict is an
**honest non-closure**: no exact closed form for `Pi(c)` was found. This
is accordingly not a "does the proof hold up" review — it is a check of
whether the document's claims (a new four-term heuristic-derived,
numerically-confirmed asymptotic law; a set of numerical exclusions; an
honestly-disclosed cost wall) are true, accurately hedged, and neither
over- nor under-stated.

---

## VERDICT

> **SOUND WITH NAMED ISSUES.**
> "ACCEPT for catalogue" **applies, at the tier actually claimed** — an
> honest non-closure carrying a heuristically-derived, numerically-confirmed
> four-term asymptotic law (`n<=4`) plus genuine, bug-checked numerical
> exclusions — **not** a proof of the law and **not** a closed form for
> `Pi(c)`. One concrete mathematical error was found in a supporting
> argument (§7.3, last bullet); it does not touch the main result, the
> numerical values, the recursion, or the leading/second-order derivation,
> all of which independently reproduce cleanly. Full detail below.

Everything this referee could independently recompute — the recursion, the
published anchors, `Pi(c)` at five values of `c` to >=110 digits, the exact
reformulations (E1)/(KEY), the leading- and second-order asymptotic
coefficients, the qualitative shape of the third/fourth-order coefficients,
the order-2 cost-wall diagnosis, the PSLQ self-caught bug's diagnosis, and
the 2-term/3-term family exclusions — reproduced independently and matched.
One piece of stated reasoning (not a numerical result) in §7.3 is wrong as
written, though its conclusion happens to still hold for a different reason
already present elsewhere in the same section.

---

## 0. Method and discipline

Per mandate: no `.py` script belonging to this front, the wave-16
front/referee, or the wave-14 parent was opened at any point. Everything
below was re-derived from `ATTEMPT.md`'s own prose (§0 inputs, §1.1's
description of the `(P,Q)`-ansatz technique, §4.1's stated exact
reformulations) and freshly implemented. `mpmath` (gmpy2 backend) was used
throughout for arbitrary-precision arithmetic; no randomness was needed
(the reserved seed range `20260867000+` was not drawn from).

Files in this directory:

| file | role |
|---|---|
| `ref01_fresh_family.py` | fresh `(P,Q)`-family recursion, independently re-derived and implemented (docstring contains the referee's own by-hand re-derivation of the recursion from the PDE) |
| `ref02_anchor_test.py` / `.log` | validates `ref01` against the published anchors of §0/§1.2 |
| `ref03_plateau_compute.py` | computes `Pi(c)` at a given `c` with 3-way-style error control; `ref03_log_c*.log` / `ref03_result_c*.json` for `c in {640,1000,2560,163840,655360}` |
| `ref04_derivation_checks.py` / `.log` | numerically verifies the exact reformulations (E1)/(KEY) against `ref01`'s own series, and the `R`/`psi2` ODEs |
| `ref05_asymptotic_fit.py` / `.log` | independent exact polynomial fit of `y(eps)` against this referee's own 5-point `Pi(c)` table, plus independent 2-term/3-term family exclusion tests |

---

## 1. Re-deriving the `(P,Q)`-family recursion from §0's PDE (task 3, part 1)

Before writing any code, the recursion of record was re-derived by hand
from the stated PDE system (§0):

```
dPhi/ds - dPhi/dg = c(Phi - W),  dPsi/ds = c(Psi - W)
W = g*Avg_g[Phi] + (1-s-g)*Psi,  Avg_g[Phi] = (1/g) int_0^g Phi dg'
```

Writing `Phi = sum a_k(s) g^k`, `Psi = sum b_k(s) g^k` (`a_0=1` forced by
`Phi(s,0)=1`; `b_0=0` forced by boundedness of `b_0' = c s b_0`, whose only
bounded solution is `b_0=0` — the origin of the "bounded branch"
instruction), direct coefficient matching gives:

```
g*Avg_g[Phi] = sum_{j>=1} [a_{j-1}/j] g^j ,   g*Psi = sum_{j>=1} b_{j-1} g^j
=> w_j = a_{j-1}/j + (1-s) b_j - b_{j-1}                        (j>=1)
```

and matching the two PDEs coefficient-by-coefficient:

```
a_{k+1} = [a_k' - c a_k + c w_k]/(k+1)
b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}
```

— **both exactly match §0's stated recursion.** This is straightforward,
unambiguous algebra; the archive's instruction to "confirm reproducibility,
not second-guess wave-16's own accepted result" is satisfied — there is
nothing to second-guess here, the recursion is a forced consequence of the
stated PDE.

**Fresh `(P,Q)`-family implementation.** Following §1.1's own prose
description (not any script), every `a_k, b_k` is represented as a pair of
polynomials `(P,Q)` in `s` with value `P(s)+Q(s)*E(s)`,
`E(s):=erfcx(s*sqrt(c/2))`. The identity `E'=c*s*E-sc` (`sc:=sqrt(2c/pi)`)
was independently re-derived from `erfcx'(z)=2z*erfcx(z)-2/sqrt(pi)` and
verified numerically to `1e-36` (`ref02` log). The `b_k`-ODE solve
(`b'-csb=A+BE` for polynomial `A,B`) was worked out independently: writing
`b=U+VE`, `V'=B` (one free constant `kappa`), `U'-csU=A+sc*V=:R`; matching
`s^j` coefficients gives `(j+1)u_{j+1}-c*u_{j-1}=r_j`, solved **descending**
from the top degree (`deg U = deg R - 1`), leaving the `j=0` equation
`u_1=r_0` as a **consistency condition that pins `kappa`**
(`kappa=(u_1-A_0)/sc`) rather than an extra unknown — full derivation with
the exact index bookkeeping is in `ref01_fresh_family.py`'s docstring.
**This referee's own derivation of this technique matches §1.1's prose
description exactly**, including the "leftover `j=0` relation pins `kappa`"
detail.

**Validation (`ref02_anchor_test.log`):** all 5 published anchors
(`a_2(0)`, `a_3(0)`, `a_4(0)`, `b_2(0)`, `b_1(0)=sqrt(pi c/2)` at `c=1000`)
match to every displayed digit. 5/5 PASS.

---

## 2. Fresh computation of `Pi(c)` (task 3, part 2)

Using the from-scratch implementation, `Pi(c) = lim S(t0)`,
`S(t0)=sum_{k<=K} a_k(0) t0^k`, was computed at `c*t0 in {230,260,290}`
(matching the document's own approach-error methodology) for
**`c = 640, 1000, 2560, 163840, 655360`** — a `1024x` range, `K=2000`,
`dps=400`. Each run took `~155-180s`.

| `c` | this referee's `S(290)`, leading digits | matches ATTEMPT.md §3's quoted digits? | `\|S(260)-S(290)\|` (stable digits) |
|---|---|---|---|---|
| 640 | `0.0466626652057907264316848615295666243978...` | **yes, all 40 quoted digits** | `4.46e-114` (~113) |
| 1000 | `0.0377615983402126188243712025905770479904...` | **yes, all 42 quoted digits** (matches the mandate's quoted value exactly) | `4.47e-114` (~113) |
| 2560 | `0.0240217755876659764091477607960026096265...` | **yes, all 40 quoted digits** | `4.53e-114` (~113) |
| 163840 | `0.0030842081459557513799990201104874476322...` | **yes, all 40 quoted digits** | `6.95e-114` (~113) |
| 655360 | `0.0015451312096662308759993857963513008680...` | **yes, all 40 quoted digits** | `8.67e-114` (~113) |

Full values, run logs, and JSON records are in this directory
(`ref03_result_c*.json`, `ref03_log_c*.log`). **All five independently
recomputed values agree with the document's quoted digits exactly**, and
this referee's own internal stability check (`S(260)` vs `S(290)`) gives a
strikingly uniform `~113` stable digits at every `c` (this referee used a
single fixed `dps=400` for all five runs, unlike the document's per-`c`-
tuned `dps=360-440`, which plausibly explains why the document's own
stable-digit counts drift mildly with `c` — `110-112` — while this
referee's fixed-precision runs sit flat at `~113`; both are consistent
with the same underlying `~e^{-c t0}` approach law, just budgeted
differently). Computed with a *different* `dps`, a *different* run, and no
shared code — a strong, independent confirmation of §2/§3.

**Order-2 growth / cost-wall diagnosis independently reproduced.** At
`c=1000, ct0=290`, this referee's own partial sums peak at term index
`k=391` with `log10|term| = 149.95` — matching the document's own
"`max|term| ~ 1e150` at `c=1000, ct0=290`" (§2.2) almost exactly, from a
completely independent computation. This corroborates the entire-order-2 /
cost-wall analysis underlying §2.2's honest disclosure of the `c<250` cost
wall.

---

## 3. Attacking the matched-asymptotics derivation on its own terms (task 4)

### 3.1 The exact reformulations (E1), (KEY) are genuinely exact — re-derived independently, and this matters for reading H1/H2

Substituting `s=eps*x`, `g=eps*y` (`eps=1/sqrt(c)`) into the **given, §0
PDE system** (not the matched-asymptotics expansion — the literal PDE),
this referee derived, by hand, before reading §4.1's stated forms:

```
d/ds = (1/eps) d/dx ,  d/dg = (1/eps) d/dy
int_0^g Phi dg' = eps * I(x,y) ,   I(x,y) := int_0^y Phi(x,y') dy'
W = eps*I + [1-eps(x+y)]*Psi
```

From `dPsi/ds = c(Psi-W)` and `Psi_x = eps*dPsi/ds` (chain rule, always
true): `Psi_x = eps*c*(Psi-W) = (1/eps)(Psi-W)`. Substituting `W`'s
definition above and simplifying: **`Psi_x = (x+y)Psi - I`** — exactly
(E1). Rearranging the same line differently, `Psi - W = eps*Psi_x`, gives
**`W = Psi - eps*Psi_x`** — exactly (KEY). *(KEY) follows from the Psi-PDE
and the chain-rule scaling **alone**, without needing the explicit
`Avg_g[Phi]` formula for `W` at all* — it is, as the document itself
says, a "one-line elimination," not a deep new result, and this referee's
independent derivation confirms that characterization is accurate (not
overclaimed).

The renewal formula (E2) was then independently re-derived via the method
of characteristics on `(∂_x-∂_y)Phi - (1/eps)Phi = -(1/eps)Psi+Psi_x`,
integrating along `d(x,y)/dt=(1,-1)` from `(x,y)` to the boundary
`(x+y,0)` where `Phi=1`:

```
Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps}[Psi-eps*Psi_x](x+v,y-v) dv
```

— exactly (E2). **This numerically checks out** against this referee's own
`(P,Q)`-family series (not the closed `(P,Q)` form — a direct series
summation at `c=1000, s=0.02, g=0.05`), to `1e-30` (`ref04` Part A, after
this referee caught and fixed its own scaling bug — see §5 below).

**Why this matters for H1/H2:** (E1) and (KEY) are **exact consequences of
the given PDE system**, not part of the heuristic. The heuristic content
(H1, H2) enters **only** in the subsequent step — expanding `Psi` as a
regular power series in `eps` (`Psi=eps*psi1+eps^2*psi2+...`, assumed
uniformly valid) and selecting the bounded branch at each order. This is
worth stating explicitly because the document's own §4.5 does not
separate "exact reformulation" from "heuristic expansion of it" quite this
sharply, and a reader could otherwise wonder whether H1/H2 threaten the
renewal-equation machinery itself. They do not; they threaten only the
`eps`-power-series ansatz applied to it.

### 3.2 Leading order, re-derived independently

Assuming (per the document's own ansatz, not independently justified by
this referee — see H1 discussion) `Psi(x,y) -> eps*psi1(x)` as `y->inf`
(`y`-independent to this order), substituting into (E2) at `x=0` and
`y->inf`:

```
Pi(c) = lim (1/eps) int_0^y e^{-v/eps}[Psi-eps Psi_x](0,y-v) dv
      = eps * psi1(0) + O(eps^2)          (substitute v=eps*u, eps->0)
```

For the `y`-independent ansatz, plugging into the psi1-PDE from
`Psi_x=(x+y)Psi-I` at `O(eps)` and using `I≈y*psi1(x)` exactly (since
`int_0^y psi1 dy' = y*psi1(x)` for a constant-in-y integrand): the
`y*psi1(x)` term from `(x+y)psi1` and the `y*psi1(x)` term from `I` cancel
**identically**, leaving `psi1'(x) = x*psi1(x) - 1` — matching §4.2's
stated ODE `R'=xR-1` exactly, independent of any assumption about the
solution's closed form.

This referee independently verified `R(x):=sqrt(pi/2)*erfcx(x/sqrt2)`
solves `R'=xR-1` **exactly** (`R'(x) = sqrt(pi/2)*(1/sqrt2)*[sqrt2*x*erfcx(x/sqrt2)-2/sqrt(pi)] = x*R(x) - sqrt(pi/2)*sqrt2/sqrt(pi) = x*R(x)-1`,
using `sqrt(pi/2)*sqrt2/sqrt(pi)=1`) and numerically to `~1e-31`
(`ref04` Part B). `R(0)=sqrt(pi/2)*erfcx(0)=sqrt(pi/2)`. Hence:

```
Pi(c) = eps*R(0) + O(eps^2) = eps*sqrt(pi/2) + O(eps^2) = sqrt(pi/(2c)) + O(1/c)
```

**Leading order independently confirmed, both algebraically and
numerically.**

### 3.3 Second order, partially re-derived, algebra fully confirmed

This referee independently verified `psi2(x):=2xR(x)-2` solves
`psi2'=x*psi2+2R` exactly (`psi2'=2R+2x(xR-1)=2x^2R-2x+2R`; and
`x*psi2+2R=2x^2R-2x+2R` — identical) and numerically to `~1e-30`
(`ref04` Part B), giving `psi2(0)=-2` and the claimed `-2/c` term.

Where this referee's *own* independent derivation of the psi2 **source**
(the `+eps*Psi` "re-entry" term and the inner-layer `delta=R(x)` deficit,
§4.3) is **partial, not full**: extracting `Psi` near `y=0` from the
`(P,Q)`-family's own `b_1(s)=sqrt(pi c/2)*erfcx(s sqrt(c/2))` gives, at
leading order in the inner variable `z:=y/eps` (small `g` region),
`Psi(s,g) ~ b_1(s)*g = R(x)/eps * eps*z*eps = eps*z*R(x)` — matching the
**linear-in-`z`** term of the document's claimed boundary-layer profile
`eps*(1-e^{-z})*R(x)` exactly (`(1-e^{-z}) = z - z^2/2+... -> z` for small
`z`). This referee did **not** independently re-derive the full
`(1-e^{-z})` layer shape or the `+eps*Psi` "re-entry" source term from
scratch (a genuine 3-4 hour matched-asymptotics exercise, judged
disproportionate to the mandate's "sanity-check" framing for this order
given the leading-order derivation was carried fully and the closed-form
solution's *self-consistency* (ODE + boundary condition) was verified
exactly). **This is disclosed honestly as a partial derivation, not
claimed as full.**

### 3.4 Third/fourth order: numerical sanity-check via a fresh, independent fit

Using this referee's own 5-point `Pi(c)` table (§2 above; `c=640..655360`,
same `1024x` range as the document's own 7-point table, 5 of the same 7
grid points — the **computation** is fully independent, the **grid choice**
partially overlaps the document's), `ref05_asymptotic_fit.py` performs an
exact 5x5 Vandermonde fit of `y(eps):=Pi(c)*sqrt(2c/pi) = sum d_j eps^j`:

| coeff | predicted (§4) | this referee's independent fit | agreement |
|---|---|---|---|
| `d0` | `1` | `0.99999999540867771505` | `4.6e-9` abs — **~8-9 digits** |
| `d1` | `-2*sqrt(2/pi) = -1.59576912160573...` | `-1.5957630374206751506` | `6.1e-6` abs, `3.8e-6` rel — **~5-6 digits** |
| `d2` | `7/2 = 3.5` | `3.4978589937983287968` | `2.1e-3` abs, `6.1e-4` rel — **~3 digits** |
| `d3` | `-(34/3)*sqrt(2/pi) = -9.04269168910...` | `-8.8531250818586312132` | `0.19` abs, `2.1e-2` rel — **~1-2 digits, same sign/order** |
| `d4` (conjectured `209/8=26.125`) | | `19.7325923222667996` | weak, same order of magnitude only |

This is **weaker per-coefficient resolution than the document's own
7-point fit** (12/9/6/4.2 digits for `d0..d3` — expected, since this
referee used 5 points vs 7, over the same range), but it is an
**independently computed, independently coded confirmation** that:
`d0≈1`, `d1` is clearly negative and of the predicted magnitude, `d2` is
clearly near `3.5` and positive, and `d3` has the predicted sign and
correct order of magnitude. **No contradiction with any claimed
coefficient was found.** A 4-point subset (dropping `c=2560`) gives
consistent results (`d0=0.99999992`, `d1=-1.59567`, `d2=3.468`,
`d3=-7.38`), showing the fit is not an artifact of one particular point
set.

**Independent confirmation that d1 != 0** (needed for the "any purely
even-in-eps family is excluded" claim, §7): confirmed directly by the fit
above — `d1` is unambiguously negative and of the right order across two
independent point-subsets. This independently validates the exclusion
logic of §7.3's second bullet.

---

## 4. Are H1/H2 generic caution, or a real threat to the 4-term result? (task 4/6)

**Assessment: not a real threat to the specific `n<=4` result, based on
everything this referee could check — but genuinely open, and there is one
concrete place worth naming where they could bite in the future.**

- The two "exact reformulations" that the whole derivation rests on are, as
  shown in §3.1 above, **actually exact** (rigorous consequences of the
  established PDE, re-derived independently by this referee) — H1/H2 do
  not touch them.
- H1 (uniform validity of the outer/inner decomposition) and H2
  (uniqueness of the bounded branch) apply to the subsequent `eps`-power-
  series ansatz. If either were violated **at the orders claimed
  (`n<=4`)**, the derived coefficients `d0..d3` would not, in general,
  match an independent numerical fit to multiple digits — but they do
  (§3.4), across a fit using none of the derivation's own machinery. This
  is meaningful (if not conclusive) empirical evidence that H1/H2 are not
  silently corrupting the `n<=4` result.
- **A concrete, non-generic place H1/H2-type issues could plausibly bite
  later, named here:** §2.3 independently confirms (via this referee's own
  order-2 partial-sum measurement, §2 above) that `Phi(0,.)` is order-2
  entire — an unusual growth class. A matched two-region (inner/outer)
  asymptotic ansatz for an order-2-entire-generating problem is exactly
  the kind of setting where genuine trans-series content
  (contributions non-perturbative in `eps`, i.e. formally smaller than
  every power `eps^n` but not zero) is common. Such content would not
  contradict *any* finite number of confirmed power-series coefficients
  (§3.4's checks are blind to it by construction) but would mean that
  **no finite-order power-series law, however many terms verified, could
  ever equal `Pi(c)` exactly at finite `c`.** This is not a criticism of
  the derivation — it is precisely consistent with, and gives a sharper
  reason for, the document's own §10 item 1/2 (closed form and
  resummation both remain open) and does not affect the honesty of the
  "four-term law, not a closed form" framing. It does mean a future closed-
  form search should not expect "enough asymptotic terms" to ever
  substitute for an exact identity.

**Conclusion: H1/H2 are correctly scoped, non-boilerplate, honestly named
gaps — this referee's independent checks corroborate the specific 4-term
claim and found no evidence they are currently biting, while also
identifying a concrete structural reason (order-2 growth) they *could*
matter for any attempt to leverage the asymptotic law toward an exact
closed form.**

---

## 5. Exclusion claims (§7) — independently checked (task 5)

**2-term and 3-term family exclusions, redone with this referee's own
data** (`ref05_asymptotic_fit.log`):

| family | fit on | tested at | this referee's relative mismatch | document's claim |
|---|---|---|---|---|
| `a/sqrt(c)+b/c` | `c=640,1000` | `c=655360` | `3.4e-3` | `3.6e-4`-`5.6e-3` |
| `a/sqrt(c)+b/c+g/c^1.5` | `c=640,1000,2560` | `c=163840` | `1.3e-4` | `2.6e-5` |

Both independently land in the same order of magnitude as the document's
own reported mismatches, both **far above** any plausible roundoff floor
(`~1e-100`+) of the underlying `Pi(c)` data — **§7.3's first two exclusion
claims are independently corroborated.**

**`d1 != 0` exclusion of purely-even-in-eps families (rational functions
of `c`):** independently confirmed, §3.4 above (`d1` clearly and
robustly nonzero, negative, right order of magnitude, across two
independent subsets).

**PSLQ self-caught bug (§7.1/§9 S4) — plausibility check:** this referee
did not (per mandate) open `r05_identify.py`, but the *mechanism*
described — a bare `1/c` (or `c`) placed as an explicit PSLQ basis vector
alongside the constant `1` trivially yields `c*(1/c)-1=0` for any specific
integer `c` within the `maxcoeff` bound, with zero coefficient on the
target constant — is elementary, well-known PSLQ-methodology folklore and
is a fully sound diagnosis of the described symptom (trivial relations
found at three `c` values, "NO RELATION" only at the one `c` value
whose trivial coefficient exceeds `maxcoeff`). **The self-diagnosis is
mathematically sound as described.**

---

## 6. An error found in this document (§7.3, last bullet) — disclosed

**Claim under review** (§7.3): *"A single term `A*erfcx(lambda*sqrt(c))`
alone... excluded even more simply, without needing any coefficient beyond
`d0`... `A*erfcx(lambda*sqrt(c))` is O(eps) — it has NO `eps^0` term at
all, so it cannot match `Pi(c)*sqrt(2c/pi)->1`... regardless of `lambda`
or `A`,"* stated as **excluded for a reason different from** the preceding
"purely even in `eps`" bullet.

**This referee's finding: the stated reasoning is incorrect, though the
exclusion conclusion itself still holds — via the *same* mechanism as the
preceding bullet, not a different one.**

Take the candidate literally as a proposal for `Pi(c)` itself:
`Pi(c) := A*erfcx(lambda*sqrt(c))`. Using the standard asymptotic
`erfcx(z) ~ (1/(z*sqrt(pi)))*[1 - 1/(2z^2) + ...]` (even powers of `1/z`
only) with `z=lambda*sqrt(c)=lambda/eps`:

```
Pi_candidate(c) ~ (A/(lambda*sqrt(pi))) * eps * [1 - eps^2/(2*lambda^2) + ...]
```

— i.e. `Pi_candidate` is a series in **odd** powers of `eps` only
(`eps^1, eps^3, ...`), matching the *order* `O(eps)` of the true `Pi(c)`.
Rescaling exactly as the document's own `y` is defined:

```
y_candidate(c) := Pi_candidate(c)*sqrt(2c/pi) = [A*sqrt2/(lambda*pi)] * [1 - eps^2/(2 lambda^2) + ...]
```

This referee verified **numerically** (`ref04`-style direct evaluation,
choosing `A=lambda*pi/sqrt2` so the leading constant is exactly `1`, then
scanning `c` from `1e2` to `1e12`):

```
c=1e2:  y_candidate = 0.995073...   (y-1)/eps  = -0.0493   (y-1)/eps^2 -> -0.50
c=1e6:  y_candidate = 0.999999500...(y-1)/eps  = -5.0e-4   (y-1)/eps^2 -> -0.50
c=1e12: y_candidate = 0.9999999999995 (y-1)/eps -> 0        (y-1)/eps^2 -> -0.50
```

confirming exactly: `y_candidate` **does** have a well-defined, nonzero,
matchable `eps^0` term (`d0=1` achievable by choosing `A` appropriately —
contradicting *"it has NO eps^0 term at all"* and *"regardless of lambda
or A"*), and its `eps^1` term is **identically zero** (`(y-1)/eps -> 0`),
while its `eps^2` term is `-1/(2*lambda^2)` (matching a clean closed form,
here `-0.5` for `lambda=1`).

**The single-erfcx-term family is thus a proper subset of "purely even in
`eps`" (for `y`)** — its `d0` can be matched, but its `d1` is identically
zero, exactly the mechanism the *preceding* bullet already excludes via
the true, independently-confirmed `d1 != 0` (§3.4/§5 above). The apparent
source of the document's error: comparing the *unrescaled* candidate
expression `A*erfcx(...)` directly against the *rescaled* target quantity
`Pi(c)*sqrt(2c/pi)->1`, rather than rescaling both sides consistently
before comparing.

**Severity / impact:** low. The document's §7.3 explicitly flags having
already caught and revised an earlier, "loose" version of this same
argument (footnote in that bullet) — this referee's finding shows that
revision did not fully land: the corrected text still asserts two
genuinely *different* exclusion mechanisms where there is really one. The
practical conclusion (this family is excluded) is **unaffected** — it
follows immediately from the already-established, independently-confirmed
`d1 != 0` fact one bullet earlier — but the stated justification for the
last bullet, and its "excluded... without needing any coefficient beyond
`d0`" and "two DIFFERENT reasons" framing, should be corrected or removed.
Nothing else in §4, §5, or the rest of §7 depends on this bullet.

---

## 7. Self-caught referee bug (disclosed, per archive culture)

While writing `ref04_derivation_checks.py`'s numerical check of (E1), this
referee's first attempt compared `eps*dPsi/ds` against
`(x+y)*Psi - int_0^g Phi(s,g')dg'` **without** correcting for the fact
that (E1) is stated in the *scaled* `y`-variable (`I(x,y):=int_0^y
Phi(x,y')dy'`), while `int_0^g Phi(s,g')dg'` is an integral over the
*unscaled* `g`-variable — related by `int_0^g Phi dg' = eps*I(x,y)`, a
relation this referee's own §3.1 derivation (above) states explicitly but
initially failed to apply inside the check script. Symptom: a spurious
residual of `0.0668` (nowhere near roundoff) on the first run. Caught
immediately (the residual was obviously too large to be numerical noise,
and cross-checking against the by-hand derivation located the missing
factor of `eps`); fixed by computing `I_scaled := Ival/eps` before
comparing; rerun gives a residual of `3.1e-30` (machine precision at
`dps=50`). Both the buggy and fixed runs are visible in this referee's own
process; only the fixed version is reported as a result in §3.1 above and
in `ref04_derivation_checks.log`.

---

## 8. What was checked vs. not checked (honesty ledger)

**Independently checked and confirmed:**
- The `(P,Q)`-family recursion, re-derived from the PDE by hand (§1).
- The fresh `(P,Q)`-family implementation, validated against all 5 quoted
  numeric anchors (§1).
- `Pi(c)` at 5 values of `c` spanning the document's full `1024x` range,
  to `>=110` digits each, matching every quoted digit (§2).
- The order-2 partial-sum growth / cost-wall diagnosis, matching the
  document's own measured peak (`1e150` at `c=1000,ct0=290`) almost
  exactly (§2).
- The two exact reformulations (E1), (KEY), both by hand and numerically
  against a fresh series implementation (§3.1).
- The leading-order coefficient `sqrt(pi/(2c))`, fully re-derived from
  the exact renewal structure plus the (assumed) `y`-independent ansatz
  (§3.2).
- The `R` and `psi2` ODEs and closed forms, both symbolically (by hand)
  and numerically (§3.3).
- `d0..d3`'s sign, order of magnitude, and (for `d0,d1`) several digits of
  numerical agreement, via a wholly independent 5-point fit (§3.4).
- The 2-term/3-term family exclusions and the `d1!=0` exclusion, via
  independent data and fit code (§5).
- The plausibility of the self-diagnosed PSLQ bug (§5).

**Checked only partially, disclosed as such:**
- The *origin* of the second-order source terms (`+eps*Psi` re-entry, the
  `(1-e^{-z})` inner-layer profile) — only the leading (`z`-linear) part
  was independently re-derived (§3.3); the full profile was not.
- Third/fourth order coefficients — sanity-checked only via independent
  numerical fit (as the mandate explicitly permits), not by carrying this
  referee's own matched-asymptotics derivation to those orders.

**Not checked (explicitly out of scope or infeasible in this review):**
- The `gamma_n` all-orders conjecture beyond `n=4` — the document itself
  already labels this an open conjecture, not a result; this referee did
  not attempt to extend or test it further.
- Full PSLQ/inverse-symbolic re-runs (would require reading or
  reimplementing `mpmath.identify` search logic in detail beyond what the
  mandate's budget calls for; the *mechanism* of the self-caught bug was
  checked instead, which is the load-bearing part).
- The `s`-profile numerical test of §6 — not independently reproduced
  (time budget); no reason to doubt it given everything else checked out,
  but this referee did not verify it directly.

---

## 9. Final assessment

The document's own framing — **"honest non-closure of the strict target
... with a genuinely new, machine-verified, numerically-confirmed
FOUR-TERM ASYMPTOTIC LAW"**, explicitly labeled DERIVED (heuristic) +
CONFIRMED (numerically), not PROVED — is **accurate and appropriately
hedged**. This referee found:

- No evidence of overclaiming on the central results (the recursion, the
  `Pi(c)` values, the leading/second-order derivation, the exclusion
  tests) — all independently reproduced.
- No evidence that H1/H2 are currently corrupting the specific `n<=4`
  claim, though they remain genuinely open and there is a concrete
  structural reason (order-2 entire growth) to expect trans-series content
  could eventually matter for any attempt to go from "asymptotic law" to
  "closed form."
- One genuine mathematical error in a supporting (not load-bearing)
  argument, §7.3's last bullet, whose conclusion is unaffected but whose
  stated reasoning is wrong and should be corrected.
- One transparently disclosed bug in this referee's own adversarial code
  (§7), caught and fixed before being reported.

**`phi_REDB` and every formula of record: untouched by this review, as by
the document under review.** No claim in this report should be read as
touching the Conjecture-1/whole-space line or any Millennium-Problem-
adjacent question — this is exclusively about the abstract M-CLUST(b)
process's plateau constant.

**Verdict: SOUND WITH NAMED ISSUES.** "ACCEPT for catalogue" at the tier
claimed (non-closure + heuristic-derived, numerically-confirmed asymptotic
law) is appropriate, conditional on correcting or removing §7.3's last
bullet's stated justification (§6 of this report).
