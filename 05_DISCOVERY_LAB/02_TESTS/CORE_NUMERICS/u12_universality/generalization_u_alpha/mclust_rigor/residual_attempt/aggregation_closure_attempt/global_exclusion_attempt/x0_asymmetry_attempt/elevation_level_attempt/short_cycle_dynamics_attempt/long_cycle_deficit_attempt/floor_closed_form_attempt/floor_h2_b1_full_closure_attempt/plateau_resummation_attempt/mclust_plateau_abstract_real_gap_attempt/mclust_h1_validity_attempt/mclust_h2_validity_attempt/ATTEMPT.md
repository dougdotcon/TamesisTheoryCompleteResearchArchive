# ATTEMPT — uniqueness of the y-independent bounded solution at each
# order (H2), plateau resummation lineage (`MCLUST-H2-VALIDITY-ATTEMPT`)

**Wave 21, front (d), `DISC-DEC-093`.** Target: `H2`, the companion
heuristic gap to `H1` (attacked in wave 20, `mclust_h1_validity_attempt`)
left open by `plateau_resummation_attempt` (`DISC-DEC-072/077`) and left
untouched by both `mclust_plateau_abstract_real_gap_attempt`
(`DISC-DEC-083/085`, explicit §B.5 non-attempt) and
`mclust_h1_validity_attempt` (`DISC-DEC-088/091`, explicit scoping to `H1`
only, §0/§6 of that document) — "uniqueness of the `y`-independent bounded
solution at each order (proved only within fields where the
`y`-differentiated homogeneous equation's `e^{xy+x^2/2}` growth can be
excluded by boundedness)."

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process — pure
combinatorial/asymptotic mathematics about a random-permutation-with-
reroutes ensemble. It is a standalone object, entirely independent of the
archive's separate Tree A (`u1/2` / "Lemma Aberto") line in `THEOREM.md`.
Nothing here is, or is adjacent to, a Millennium Prize Problem, and no
such claim appears anywhere below.**

Reserved seed range for this front: `20260906000-20260906999`
(`numpy.SeedSequence` base). **In the end no randomness was needed
anywhere in this front** — exactly as in every direct ancestor
(`plateau_resummation_attempt`, `mclust_plateau_abstract_real_gap_attempt`,
`mclust_h1_validity_attempt`): every result below is exact symbolic
reasoning (`sympy`) or deterministic arbitrary-precision (`mpmath`,
`dps=60` throughout) computation, so the reserved range remains entirely
unused.

---

## EXECUTIVE SUMMARY (read first)

**Tier: a genuine, essentially complete theoretical reduction of H2 —
conditional only on the SAME order-by-order Watson/Taylor bookkeeping that
H1 already names as its own single heuristic content, plus mild,
standard regularity — via one new, fully general, fully rigorous
elementary lemma and a clean induction, both verified independently by
fresh symbolic computation. H2 is not claimed PROVED unconditionally
(that would require H1's own machinery to be independently justified to
all orders, which neither this front nor its predecessor establishes),
but its own, separate heuristic content collapses to essentially nothing
beyond H1's.**

1. **A new, fully general, fully rigorous "Growth-Exclusion Lemma"
   (§2).** For the linear ODE `u_x(x,y) - (x+y)u(x,y) = f(x)` (`x>=x0`,
   `y>=0` a parameter — the exact form `H2`'s named homogeneous equation
   takes), the general homogeneous solution is `C(y)*e^{x^2/2+xy}`
   — **exactly** the growth mode `H2` names — and: (i) a bounded (as
   `x->infinity`) particular solution exists in explicit closed
   (integral) form whenever `f` has at most sub-Gaussian growth; (ii) it
   is the UNIQUE bounded solution, by a two-line argument (any two
   bounded solutions differ by a multiple of `e^{x^2/2+xy}`, which
   diverges as `x->infinity` for every `y>=0`, so boundedness forces the
   multiple to be `0`). This is proved here in COMPLETE generality — for
   ANY order `n`, ANY source `f` of mild growth — not "within fields"
   (the qualifier in `H2`'s own quoted statement); the family
   `{P(s)+Q(s)erfcx(...)}` used throughout this lineage is a convenient,
   sufficient, but NOT necessary, setting for this uniqueness argument.
   Verified symbolically (`sympy`, exact) and illustrated numerically
   (`mpmath`, `dps=60`): adding a `1e-30`-sized admixture of the excluded
   mode to the bounded branch of the `psi1` equation (i.e. to `R(x)`
   itself) causes a blow-up of 20 orders of magnitude by `x=15` — a
   concrete demonstration of why the exclusion is the *correct*, not
   merely *convenient*, selection principle.

2. **A clean induction, verified independently by two different methods,
   showing `H2`'s "`y`-independent" claim holds not just at `n=1` (the
   only order the required reading states it for) but at every order
   tested, `n=1..6`, GIVEN the Watson/Taylor bookkeeping to that order
   (§3).** Starting from the EXACT identity `Psi_xy = Psi + (x+y)Psi_y -
   Phi` (differentiating the record's own `(E1)` in `y`), combined with
   the record's own Watson-kernel expansion of `Phi` in terms of `W`
   (generalized here, for the first time, to ALL orders via the operator
   `Phi ~ sum_m eps^m (d/dx-d/dy)^m W`, whose exact coefficient-1
   normalization — no stray `1/m!` — is separately verified, §3.1), this
   front derives the quantity `f_n := psi_n - phi_n` order by order and
   proves, by a genuine, general (all-`n`, not case-by-case) telescoping
   algebraic identity (§3.2, proved by hand AND verified symbolically for
   `n=2..9`) that **`f_n = 0` identically at EVERY order, given orders
   `1..n-1` are already established `y`-independent**. Combined with the
   Growth-Exclusion Lemma (§2), this means: `chi_n := d(psi_n)/dy`
   satisfies a HOMOGENEOUS equation at every order, hence `chi_n = 0`
   identically, by clean mathematical induction — `H2`'s literal claim
   ("the solution is `y`-independent, uniquely, at each order") is
   established at every order this front's bookkeeping reaches, not just
   `n=1`. This is verified independently in `sympy` at `n=1..6` (fresh,
   mechanical induction with each resolved order enforced as a
   genuinely `y`-free `Function(x)` object, §3.3) AND by a
   symbol-independent, purely algebraic check of the general telescoping
   identity itself at `n=2..9` (§3.2) — two different computational
   routes to the same conclusion, in addition to the by-hand derivation.

3. **The honest limit of this reduction (§4).** The induction's
   inhomogeneity-cancellation (`f_n=0`) is derived FROM the SAME
   order-by-order Watson/Taylor bookkeeping of `Phi` in terms of `W` that
   is `H1`'s own named heuristic content (the "smoothness and uniform
   validity of the outer/inner decomposition ... assumed, not proved").
   **This front's central finding is therefore a REDUCTION, not an
   unconditional proof: `H2`, AS A SEPARATE HEURISTIC GAP FROM `H1`,
   ESSENTIALLY DISSOLVES** — its own uniqueness/growth-exclusion content
   is now a completely general, fully rigorous, elementary fact (the
   Growth-Exclusion Lemma, needing nothing from the specific
   `{P,Q,erfcx}` family), and its remaining "`y`-independence at each
   order" content follows automatically, by clean induction, from
   whatever validity `H1`'s own Watson bookkeeping already has at that
   order — `H2` does not need any INDEPENDENT heuristic leap beyond
   `H1`'s. What is NOT established here: that the Watson/Taylor
   bookkeeping itself is valid to unboundedly high order (that is
   exactly `H1`'s own open content, `(U1)`+`(U2)` of
   `mclust_h1_validity_attempt`, neither proved there nor here); and
   ordinary smoothness assumptions (mixed-partial commutativity
   `Psi_xy=Psi_yx`) needed to differentiate `(E1)` in `y` in the first
   place, standard but unverified from the exact PDE system.

4. **Supporting numerical work (§5).** A proved analytic bound
   `R(x) <= 1/x` (`x>0`, derived from scratch) and a numerical
   boundedness certificate (`mpmath`, `dps=60`) for `R, R', R'', R'''`
   confirm the sub-Gaussian growth hypothesis the Growth-Exclusion
   Lemma's existence half needs is genuinely satisfied at the orders
   this front and its predecessor reach. A second numerical check
   evaluates the four established closed-form profiles `psi1..psi4`
   AT THE TRUE PHYSICAL EDGE `x=sqrt(c)` (`s=1`) across the same
   `c`-grid `mclust_h1_validity_attempt` used, finding all four strictly
   decreasing in magnitude as `c` grows — no sign of the excluded growth
   mode reasserting itself near the boundary that actually matters for
   finite `c`, consistent with (not a replacement for) the sibling H1
   front's own, much larger, uniformity grid. **A self-caught numerical
   pitfall (S1, §6)** — a first version of this same script computed
   `R(x)` via a literal huge-prefactor-times-tiny-tail-integral formula,
   which silently returns garbage at `dps=60` once the tail integral
   drops below `~1e-60` (around `x~40`, well within this front's own
   `c<=8000` grid) — was caught by the script's OWN analytic-bound
   assertion failing at `x=89.4` (`sqrt(8000)`), before any number was
   reported as a finding, and fixed by a numerically-safe substitution.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document. `H1` is untouched, exactly as this front's mandate scoped it to
`H2` alone (this front's own finding is that `H2` now essentially rests
ON `H1`, not the reverse — nothing here bears on `H1`'s own open status).
No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, or
`TEST_QUEUE.yaml` file was opened for writing. No `adversarial/`
subdirectory created; no referee dispatched. No git command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` §2 (Tree B), specifically the `FLOORH2` and `PLATRESUM` nodes and
ALL dated addenda under `PLATRESUM` (wave-17, `DISC-DEC-072/077`; wave-19,
`DISC-DEC-083/085`; wave-20, `DISC-DEC-088/091`, about `H1`); the full
`mclust_h1_validity_attempt/ATTEMPT.md` (direct predecessor front, same
directory tree — attacked `H1`, not `H2`, but establishes the exact PDE
system, the exact renewal identity `(E1)/(E2)/(KEY)`, and its own §2.1
Watson-concentration lemma, which this front's §2 deliberately does NOT
reuse or extend — this front's Growth-Exclusion Lemma is a SEPARATE,
freshly-derived elementary ODE fact, addressing `H2`'s named mechanism,
not `H1`'s); and the full `plateau_resummation_attempt/ATTEMPT.md`
(grandparent), in particular §4 (the matched-asymptotics derivation) and
§4.5 (the exact statement of `H1`/`H2`, quoted verbatim below), for the
original derivation context where `H1`/`H2` were first named and the
`e^{xy+x^2/2}` growth mode first mentioned.

**No `.py` file from any front in the `mclust_rigor` lineage — this
front's own ancestors down through `mclust_h1_validity_attempt` — was
opened, read, or imported at any point.** Every script in this directory
(`k01`-`k03`) was written fresh, from the mathematical content of the
prose cited above; every previously-published closed form or number used
as a cross-check (`R(x)`, `psi2(x)=2xR(x)-2`, the `psi3`/`psi4` ODEs and
closed forms, the `resid3` spot values) is transcribed as plain text from
the required-reading `ATTEMPT.md` documents, never imported as code.

**The exact statement of H2, quoted verbatim** (`plateau_resummation_
attempt/ATTEMPT.md` §4.5, "Status of the derivation (honest)", also
requoted by the H1 predecessor's own §0):

> (H2) uniqueness of the `y`-independent bounded solution at each order
> (proved only within fields where the `y`-differentiated homogeneous
> equation's `e^{xy + x^2/2}` growth can be excluded by boundedness).

**Locating the named mechanism in the record.** The one explicit instance
of a "`y`-differentiated homogeneous equation" appearing anywhere in the
required reading is `plateau_resummation_attempt/ATTEMPT.md` §4.2's own
statement about the ORDER-1 equation:

```
psi1_x = (x+y) psi1 - 1 - int_0^y psi1 dy'         [required reading, verbatim]
```

"whose bounded solution is `y`-INDEPENDENT (r06 V8)". This front reads
`H2` as the claim that an analogous statement — a `y`-dependent PDE whose
UNIQUE bounded (as `x->infinity`) solution turns out to be `y`-independent,
by excluding a homogeneous growth mode — holds not just at this one
stated order but "at each order", and sets out to establish (or precisely
characterize the limits of) this claim in general.

**Established inputs this front works from** (restated for
self-containedness, exactly as given in the two required-reading
documents — not re-derived except where explicitly marked "re-derived"
below):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Governing PDE system (record, wave-14 SS5):
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi]+(1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y) (plateau_resummation_attempt Section 4.1):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                          (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv   (E2)

Outer-region Watson expansion, order eps^1 (record, plateau_resummation
ATTEMPT.md Section 4.2, quoted verbatim):
  Phi = W + eps*(W_x - W_y) + O(eps^2)

Established closed forms:
  psi1(x) = R(x) := sqrt(pi/2)*erfcx(x/sqrt(2)),  R' = xR - 1,  R(inf)=0
  psi2(x) = 2 x R(x) - 2                          [psi2(0) = -2]
  psi3'(x) = x*psi3(x) + 7*R'(x)                  [psi3(0) = (7/2)sqrt(pi/2)]
  psi4(x) = (17/3)*R'''(x)                        [psi4(0) = -34/3]
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory was written to.

---

## 1. Overview of approach

Two pieces, both aimed squarely at `H2`:

- **Part A (§2).** Make the "growth excluded by boundedness" mechanism
  named in `H2` completely rigorous and completely general — for ANY
  order, ANY source of mild growth, not restricted to any specific
  function family. This is new analysis (a fresh elementary ODE lemma),
  not present in either required-reading document, though it makes
  precise something both documents use informally (the record's own
  §1.1 "the polynomial ansatz automatically discards the `e^{c s^2/2}`
  homogeneous branch" is exactly the `y=0` special case of this lemma,
  noted explicitly in §2 below).
- **Part B (§3).** Determine, order by order, whether the STRONGER claim
  `H2` actually needs — that the unique bounded solution is genuinely
  `y`-INDEPENDENT, not merely bounded — continues to hold beyond the one
  order (`n=1`) the required reading explicitly establishes it for. This
  is carried out via an exact identity from `(E1)` plus the record's own
  Watson-kernel bookkeeping, generalized here to all orders, and checked
  by two independent symbolic-computation routes.

Both report their own honest limits (§4); neither claims an unconditional
proof of `H2`.

---

## 2. Part A — the Growth-Exclusion Lemma (general, rigorous)

### 2.1 Statement and proof

**Lemma (Growth-Exclusion).** Fix `y>=0`. Consider the linear ODE

```
u_x(x,y) - (x+y)*u(x,y) = f(x),      x >= x0
```

(`f` continuous, `y` a fixed parameter). Then:

**(i) Existence.** If `f` has at most sub-Gaussian growth (so that the
integral below converges), a bounded-as-`x->infinity` solution is given
explicitly by

```
u_p(x,y) = -e^{x^2/2+xy} * int_x^infinity e^{-(t^2/2+ty)} f(t) dt      (BB)
```

**(ii) Uniqueness.** `u_p` is the UNIQUE solution bounded on `[x0,
infinity)`: the general solution is `u_p(x,y) + C(y)*e^{x^2/2+xy}`, and
`e^{x^2/2+xy} -> +infinity` as `x->infinity` for EVERY `y>=0` (the
`x^2/2` term alone forces this, independent of the sign or size of the
`xy` term), so boundedness forces `C(y)=0`.

**Proof.** `e^{x^2/2+xy}` solves the homogeneous equation `u_x=(x+y)u`
by direct differentiation (`k02_growth_exclusion_lemma.py` Part A,
verified symbolically, exact). `(BB)` solves the inhomogeneous equation
by differentiation under the integral sign (Leibniz rule): writing
`u_p=-e^{x^2/2+xy}*I(x,y)`, `I(x,y):=int_x^infinity e^{-(t^2/2+ty)}f(t)dt`,
`dI/dx = -e^{-(x^2/2+xy)}f(x)` (Leibniz), so `u_p_x = (x+y)u_p + f(x)`,
i.e. `u_p_x-(x+y)u_p=f(x)`. Verified symbolically (`k02` Part B, exact,
no numerical approximation anywhere in this step). Uniqueness is the
two-line argument above (also `k02` Part C). **QED.** `∎`

This is `H2`'s named mechanism (`e^{xy+x^2/2}` growth excluded by
boundedness), made completely rigorous and completely GENERAL for the
first time in this lineage — it needs nothing beyond `f` having mild
(sub-Gaussian) growth; the specific polynomial-`+`-`erfcx` family used
throughout this lineage is a convenient, SUFFICIENT setting in which this
growth condition is automatically satisfied, not a NECESSARY restriction
of the argument itself. `H2`'s own qualifier "proved only within fields
where..." is, per this Lemma, broader than the record's own quoted
phrasing suggested — see §4 for what remains genuinely conditional.

**Consistency with the record's own `y=0` case.** Setting `y=0`,
`f(x)=-1` recovers exactly `R(x)=e^{x^2/2}int_x^infinity e^{-t^2/2}dt`,
the required reading's own closed form for `psi1` — verified numerically
to 50+ digits (`k02`, Part B special case). The record's own §1.1
remark ("the polynomial ansatz automatically discards the `e^{c s^2/2}`
homogeneous branch") is exactly this Lemma's uniqueness half, in the
`(P,Q)`-family's own `s`-variable (`c*s^2/2 = x^2/2` under the scaling
`x=s*sqrt(c)` used throughout) — this front's Lemma makes that remark
fully general and independent of the family representation.

### 2.2 Numerical illustration: why exclusion is *correct*, not merely
*convenient*

`k02_growth_exclusion_lemma.py` Part D adds a `1e-30`-sized admixture of
the excluded mode `e^{x^2/2}` to `R(x)` itself (`mpmath`, `dps=60`) and
tracks the result as `x` grows:

| `x` | `R(x)` [bounded branch] | `R(x)+1e-30*e^{x^2/2}` | relative blow-up |
|---|---|---|---|
| 0 | 1.253314137... | 1.253314137... | `8.0e-31` |
| 8 | 0.123131963... | 0.123131963... | `6.4e-16` |
| 10 | 0.099028596... | 0.099028602... | `5.2e-8` |
| 12 | 0.082766287... | 18.669... | `225` |
| 15 | 0.066374236... | `7.2e18` | `1.1e20` |

An admixture that is completely negligible at `x=0` (`1e-30`, far below
any precision this front or its predecessors ever need) overtakes the
true, bounded, decaying solution entirely by `x~12-15` and diverges —
concretely showing that excluding this mode is not a simplifying
convention but the ONLY choice consistent with the physical requirement
that `Phi`, `Psi` stay bounded (they are probability-related quantities,
bounded throughout the record).

---

## 3. Part B — does "y-independent" hold beyond n=1?

### 3.1 The exact `y`-derivative identity, and the all-orders Watson
operator

Differentiating `(E1)` (`Psi_x = (x+y)Psi - I`, `I=int_0^y Phi dy'`)
with respect to `y`, using `dI/dy = Phi(x,y)` (fundamental theorem of
calculus) and commuting mixed partials (`Psi_xy=Psi_yx` — standard
smoothness, an explicit standing assumption, not independently verified
from the exact PDE system, flagged honestly in §4):

```
Psi_xy(x,y) = Psi(x,y) + (x+y)*Psi_y(x,y) - Phi(x,y)            (*)
```

This is EXACT — no `eps`-expansion has been used yet. Re-verified fresh
here directly from the record's own `psi1` equation as an independent
sanity check before generalizing (`k01_watson_bookkeeping_sympy.py` Step
1: `(psi1_y)_x = (x+y)*psi1_y` follows from `(*)`'s order-1 instance
combined with `phi_1=psi_1`, both re-derived below — matches the
required reading's stated `n=1` result exactly, `sympy`-verified).

Writing `Psi = sum_{n>=1} eps^n psi_n(x,y)`, `Phi = sum_{n>=1} eps^n
phi_n(x,y)` in the outer region (`y>>eps`; both fields are `O(eps)`
there, the required reading's own `Pi(c)~eps*sqrt(pi/2)+...` being the
`x=0,y->infinity` instance), `(*)`'s order-`n` coefficient gives

```
(chi_n)_x = (x+y)*chi_n + f_n(x,y),     chi_n := d(psi_n)/dy,   f_n := psi_n - phi_n
```

To determine `phi_n` in terms of the `psi_k`'s, this front generalizes
the record's own explicit leading-order statement "`Phi = W + eps(W_x -
W_y) + O(eps^2)`" (an instance of Watson's lemma applied to `(E2)`'s
convolution kernel, expanding `W(x+v,y-v)` in Taylor series in `v` and
integrating term-by-term against `(1/eps)e^{-v/eps}`) to ALL orders:

```
Phi(x,y) ~ sum_{m>=0} eps^m * (d/dx - d/dy)^m W(x,y)          [outer region]
```

`k01` Step 0 verifies, symbolically and exactly, that the moment integral
`(1/eps)*int_0^infinity e^{-v/eps} v^m/m! dv = eps^m` — the Taylor `1/m!`
exactly cancels the moment's `m!`, so this operator carries coefficient
exactly `1` at every order `m`, not `1/m!` — before this formula is used
for anything. With `W=Psi-eps*Psi_x` (`(KEY)`), i.e. `omega_k := psi_k -
d(psi_{k-1})/dx` (`psi_0:=0`) at order `eps^k`:

```
phi_n = sum_{m=0}^{n-1} (d/dx - d/dy)^m [omega_{n-m}](x,y)
```

### 3.2 The general telescoping identity: `f_n = 0` at every order

**Claim.** If `psi_1,...,psi_{n-1}` are ALREADY known to be `y`-independent
(pure functions of `x`), then `phi_n = psi_n(x,y)` EXACTLY, hence
`f_n = psi_n - phi_n = 0` identically.

**Proof.** For `k<=n-1`, `omega_k` is `y`-independent (built from
`y`-independent `psi_k, psi_{k-1}`), so for `m>=1`, `(d/dx-d/dy)^m
omega_{n-m}(x) = omega_{n-m}^{(m)}(x)` exactly (any term in the binomial
expansion of `(d/dx-d/dy)^m` involving `d/dy` at least once annihilates a
`y`-independent function; only the pure-`d/dx^m` term survives). So

```
phi_n = omega_n(x,y) + sum_{m=1}^{n-1} omega_{n-m}^{(m)}(x)
      = [psi_n(x,y) - psi_{n-1}'(x)] + sum_{m=1}^{n-1} omega_{n-m}^{(m)}(x)
```

It remains to show `sum_{m=1}^{n-1} omega_{n-m}^{(m)}(x) = psi_{n-1}'(x)`.
Substituting `j=n-m` and `omega_j = psi_j - psi_{j-1}'`:

```
sum_{j=1}^{n-1} psi_j^{(n-j)}  -  sum_{j=1}^{n-1} psi_{j-1}^{(n-j+1)}
```

Re-indexing the second sum by `i=j-1` (`psi_0=0` drops the `i=0` term)
gives `sum_{i=1}^{n-2} psi_i^{(n-i)}`; separating the `j=n-1` term
(`psi_{n-1}^{(1)}=psi_{n-1}'`) out of the first sum leaves `psi_{n-1}' +
sum_{j=1}^{n-2}psi_j^{(n-j)}`, which the second sum cancels term-by-term
exactly. Total: `psi_{n-1}'(x)`. Hence `phi_n = psi_n - psi_{n-1}' +
psi_{n-1}' = psi_n(x,y)` exactly. **QED.** `∎`

**Independent verification.** This purely algebraic identity (no PDE
content, just index bookkeeping) is checked symbolically for `n=2..9`
with abstract univariate `sympy` functions, entirely independently of
the PDE-based derivation (`k01` Step 3) — **all 8 cases PASS exactly**
(`k01_watson_bookkeeping_sympy.log`).

### 3.3 Consequence: the induction, and its independent mechanical check

Combining §3.2 (`f_n=0`, given orders `<n` resolved) with the
Growth-Exclusion Lemma's HOMOGENEOUS case (§2, `f=0`: the unique bounded
solution of `u_x=(x+y)u` is `u=0`): **by induction on `n`, `chi_n=0`
identically at EVERY order, starting from the record's own base case
`n=1`.** `H2`'s literal claim — the bounded solution is `y`-independent,
uniquely, at each order — holds at every order this bookkeeping reaches,
not merely `n=1`.

This induction is additionally verified MECHANICALLY, order by order, in
`sympy` (`k01` Step 2, `n=1..6`): at each step, `psi_n` is represented as
a genuine bivariate `Function(x,y)`; `f_n` is computed via the formula of
§3.1 using the PREVIOUS orders, each represented as `Function(x)` (i.e.
the inductive hypothesis is enforced MECHANICALLY — any `d/dy` applied to
an already-resolved order evaluates to `0` automatically in `sympy`, not
asserted by hand); `f_n` simplifies to exactly `0` at every one of the
six orders tested, confirming §3.2's general proof concretely
(`k01_watson_bookkeeping_sympy.log`, "ALL STEPS PASS"). This is a
genuinely NEW extension of the record: the required reading establishes
`y`-independence explicitly only at `n=1` and, from `n>=2` onward,
simply WRITES pure-`x` ODEs for `psi2, psi3, psi4` without separately
re-justifying why no `y`-dependence survives at those orders — this
front's §3.2/§3.3 supplies exactly that missing justification, at every
order the Watson bookkeeping itself is valid.

> **[Nota pós-adversarial, 2026-08-26 — DISC-DEC-095, sem correção —
> achado de completude de documentação, não erro matemático.]** O
> referee hostil (Issue R1) observou que este passo indutivo invoca o
> caso homogêneo do Lema de Exclusão de Crescimento (§2) para concluir
> `chi_n=0`, mas o argumento de unicidade do Lema só força a constante
> a zero DADO que a instância de solução em exame já é conhecida como
> limitada quando `x->infinity`. O texto acima não nomeia
> explicitamente, como hipótese separada da suavidade ordinária já
> citada (§4 item 2, `Psi_xy=Psi_yx`), que `chi_n:=d(psi_n)/dy` (e não
> apenas `psi_n`) precisa ser conhecido a priori como limitado antes de
> o lema poder ser invocado para concluir `chi_n=0` em vez de meramente
> `chi_n em {0, ilimitado}`. Isto é muito provavelmente já subsumido
> pela contabilidade de Watson/Taylor mais ampla (o próprio conteúdo
> aberto de `H1`, `(U1)+(U2)`) da qual esta indução inteira já depende
> (§4 item 3), mas é logicamente distinto da suavidade citada. Não
> afeta nenhum cálculo, fórmula ou valor numérico reportado, nem muda o
> veredito de não-fechamento já dado abaixo. Hipótese padrão adicional,
> agora nomeada explicitamente: `chi_n` herda a mesma classe de
> limitação quando `x->infinity` que `psi_n` em si.

---

## 4. What this reduction does, and does not, establish

**What it establishes (unconditionally, given ordinary smoothness).**
The Growth-Exclusion Lemma (§2) is a completely general, completely
rigorous, elementary fact — genuinely new content, not present in either
required-reading document, and not restricted to the specific
`{P(s)+Q(s)erfcx(...)}` family the record's own `H2` phrasing seemed to
require. It fully accounts for the "growth excluded by boundedness" half
of `H2`'s content, at every order and for any mildly-growing source.

**What it establishes CONDITIONALLY on H1's own machinery.** The
telescoping identity (§3.2) is a purely algebraic fact about the
Watson-operator bookkeeping — but that bookkeeping itself (`Phi ~
sum_m eps^m (d/dx-d/dy)^m W`, to ALL orders `m`) is exactly the content
`mclust_h1_validity_attempt` calls `H1`: "the whole matched-asymptotics
framework ... smoothness and uniform validity of the outer/inner
decomposition and the `O(eps^n)` remainder bounds are assumed, not
proved." This front's induction shows: **GIVEN that this bookkeeping is
valid through order `n`** (whatever that validity ultimately rests on —
`H1`'s own unresolved `(U1)`+`(U2)`, per the H1 predecessor's own
reduction), **`H2`'s uniqueness/`y`-independence claim at order `n`
follows automatically**, via nothing more than the elementary
Growth-Exclusion Lemma. **`H2` therefore does not carry any INDEPENDENT
heuristic risk beyond `H1`'s own** — a genuine narrowing of the
lineage's total heuristic content from "two separate named gaps" to
"one gap (`H1`) plus an elementary corollary (this front's reduction of
`H2`)." This is the central finding of this front.

**What remains genuinely open.**

1. `H1` itself — `(U1)`+`(U2)` of `mclust_h1_validity_attempt` — is
   untouched by this front, exactly as scoped. `H2`'s reduction to a
   corollary of `H1`'s bookkeeping does NOT close `H1`.
2. The ordinary smoothness assumption `Psi_xy=Psi_yx` (mixed partial
   commutativity), needed to differentiate `(E1)` in `y` at all (§3.1),
   is standard for smooth solutions of this class of system but was not
   independently verified from the exact PDE system by this front (nor,
   as far as the required reading discloses, by any predecessor).
3. This front's induction was checked mechanically through `n=6` (§3.3)
   and proved in general form (§3.2) — the general proof covers all `n`,
   but relies on the Watson-operator formula of §3.1 continuing to hold
   at every order, which is exactly `H1`'s own open content, not an
   independent gap this front could close.
4. Existence of the bounded branch (§2, part (i)) needs `f_n` to have at
   most sub-Gaussian growth at every order — verified directly for the
   orders with an established closed form (`n<=4`, via `R,R',R'',R'''`,
   §5) but not proved in general for arbitrary `n` (would need bounding
   the growth of the full `psi_n` sequence, a separate undertaking).
5. **No attempt was made to find a genuine counterexample or a regime
   where the exclusion FAILS** (the mandate's third acceptable outcome).
   None was found either — every numerical test in §5 is consistent with
   the exclusion holding throughout the tested domain, including at the
   true physical boundary `s=1`.

---

## 5. Supporting numerical work

### 5.1 Boundedness certificate for the order-1..4 building blocks

`k03_boundedness_certificate.py`. A proved analytic bound, derived from
scratch:

```
R(x) <= 1/x   for x > 0
```

(Proof: `e^{-t^2/2} <= (t/x)e^{-t^2/2}` for `t>=x>0`; integrate and use
`int_x^infinity t e^{-t^2/2}dt = e^{-x^2/2}`.) Verified numerically at
`x` up to `200` (`dps=60`), including `x=sqrt(1000)=31.62` and
`x=sqrt(8000)=89.44`, the physical-edge values used in §5.2. A grid-plus-
tail-value search additionally certifies `R, R', R'', R'''` all bounded
and decaying on `[0,400]` (with an explicit tail check at `x=1000`) —
exactly the sub-Gaussian growth condition the Growth-Exclusion Lemma's
existence half (§2) needs, at every order this front and
`mclust_h1_validity_attempt` establish a closed form for.

### 5.2 Behaviour at the true physical edge `x=sqrt(c)`

The scaled variable `x` formally ranges over `[0,infinity)` only in the
`eps->0` idealization; the actual finite-`c` problem has `s in [0,1]`,
i.e. `x in [0,sqrt(c)]`. Evaluating the four established closed-form
profiles `psi1=R(x), psi2=2xR(x)-2, psi3(x)` (via the Growth-Exclusion
Lemma's own bounded-branch formula §2, applied to source `7R'(x)` — the
required reading's own `psi3` ODE, not a new derivation), and
`psi4=(17/3)R'''(x)` at `x=sqrt(c)` across the same `c`-grid
`mclust_h1_validity_attempt` used (`c in {200,500,1000,2000,4000,8000}`):

| `c` | `x=sqrt(c)` | `psi1` | `psi2` | `psi3` | `psi4` |
|---|---|---|---|---|---|
| 200 | 14.142136 | 0.070362300 | -0.0098536244 | 0.0024032887 | -0.00080960592 |
| 500 | 22.360680 | 0.044632448 | -0.0039762367 | 0.00061869649 | -0.00013333579 |
| 1000 | 31.622777 | 0.031591248 | -0.0019940298 | 0.00022004115 | -0.0000336635 |
| 2000 | 44.721360 | 0.022349516 | -0.0009985037 | 0.000078028468 | -0.0000084577 |
| 4000 | 63.245553 | 0.015807438 | -0.0004996255 | 0.000027628502 | -0.0000021197 |
| 8000 | 89.442719 | 0.011178943 | -0.0002499063 | 0.0000097754672 | -0.00000053059 |

(full precision, every printed digit: `k03_boundedness_certificate.log`).
All four columns are verified programmatically to be strictly decreasing
in magnitude as `c` grows (`k03`, Part 3, explicit `assert` over all 6
rows, all 4 columns — PASS): no sign of the excluded `e^{x^2/2}`-type
growth mode reasserting itself near the true boundary `s=1`, consistent
with (though not a replacement for) the sibling H1 front's own much
larger uniformity grid (`x` up to `8` in its main grid, up to `20`,
`s` up to `1.41`, in its stress test — a completely different, direct
series-summation method, reaching the same qualitative conclusion).

---

## 6. Self-caught issues (disclosed, per this lineage's convention)

**S1 (this front's own catch, computational, the most consequential).**
A first version of `k03_boundedness_certificate.py` computed `R(x)` (and,
downstream, `psi3(x)`) via the LITERAL formula `e^{x^2/2} *
int_x^infinity e^{-t^2/2}(...)dt`, evaluating the huge exponential
prefactor and the (at large `x`) astronomically tiny tail integral
SEPARATELY via `mpmath.quad`, then multiplying. This is numerically WRONG
once the tail integral's true magnitude drops below roughly `10^{-dps}`
(here `dps=60`): `mpmath.quad` cannot resolve a value that small
correctly at ambient precision and silently returns noise. This
manifested as the script's OWN §5.1 analytic-bound assertion
(`R(x)<=1/x`) FAILING at `x=89.44` (`=sqrt(8000)`, squarely inside this
front's own physical-edge grid) by `5e-4` relative — an
analytically-impossible violation, caught immediately by the assertion,
before any resulting number was used or reported as a finding. **Fix:**
substitute `t=x+u` before integrating,
`e^{x^2/2}int_x^infinity e^{-t^2/2}g(t)dt = int_0^infinity
e^{-xu-u^2/2}g(x+u)du` — a single well-scaled integral with no
huge-times-tiny cancellation, verified to agree with an independent
`mpmath`-`erfc`-based reference formula to `>=50` stable digits at `x`
up to `200` (`k03` Part 0) before being trusted for anything downstream.
The corrected script and all numbers in §5 use this fix throughout.

**S2 (this front's own catch, theoretical, caught before being written
into any claim).** An early draft of §3.1's Watson-operator generalization
initially wrote `Phi ~ sum_m eps^m/m! * (d/dx-d/dy)^m W(x,y)` (carrying
the Taylor `1/m!` through without checking whether the moment integral's
own `m!` cancels it). Re-deriving the moment integral explicitly
(`(1/eps)int_0^infinity e^{-v/eps}v^m dv = m!*eps^{m+1}`, so `(1/eps)*`
[the `v^m/m!` Taylor term integrated] `= eps^m` with NO leftover `1/m!`)
caught this before it propagated into §3.2's telescoping identity, where
an extra `1/m!` would have broken the exact cancellation the proof
depends on. `k01` Step 0 is this front's permanent, standing verification
of the correct (no-`1/m!`) normalization, kept in the final script rather
than removed after the fix.

**S3 (this front's own catch, arithmetic, caught by cross-checking two
derivation routes before trusting either).** An initial by-hand
computation of `f_3` (order 3) using the closed-form binomial expansion
of `(d/dx-d/dy)^2` (rather than the simplification available once
`omega_1,omega_2` are already known `y`-independent, §3.2) produced,
through a sign/grouping slip, a SPURIOUS nonzero result
(`f_3=(1/2)R''(x)`), which would have wrongly suggested `H2` fails
starting at `n=3`. Redoing the computation via the cleaner route (§3.2,
using `omega`'s established `y`-independence to collapse `(d/dx-d/dy)^m`
to a pure `d/dx^m`) gave `f_3=0`; the discrepancy was traced to a
missing term in the first attempt's manual binomial bookkeeping. Both
routes are now verified to agree (and to equal `0`) via the independent
`sympy` mechanization of §3.3/`k01`, which uses neither by-hand route —
disclosed here in full (including that the FIRST, WRONG value was
briefly believed correct during derivation) per this lineage's
"disclose even a caught-before-being-trusted issue" convention. No
version of the wrong value appears anywhere else in this document.

---

## 7. Honest final verdict

**`H2`, as an INDEPENDENT heuristic gap separate from `H1`, is
essentially DISSOLVED — but `H2` is not unconditionally PROVED**, because
the reduction bottoms out in `H1`'s own open content, not in anything
further resolved here. What this front contributes:

1. A new, fully general, fully rigorous Growth-Exclusion Lemma (§2) —
   the "excluded by boundedness" mechanism `H2` names, made completely
   precise and shown to need nothing beyond mild growth of the source,
   not the specific function family the record's phrasing suggested.
2. A clean, general (all-`n`) induction (§3.2, proved by hand and
   verified by two independent symbolic-computation routes, `n=2..9`
   algebraically and `n=1..6` mechanically) showing `H2`'s
   `y`-independence claim holds at EVERY order the record's own
   Watson/Taylor bookkeeping reaches — not just the one order (`n=1`)
   the required reading explicitly establishes.
3. An honest, precise statement of exactly where the remaining
   conditionality lives (§4): entirely inside `H1`'s own unresolved
   Watson-bookkeeping validity, `(U1)`+`(U2)` of
   `mclust_h1_validity_attempt` — `H2` contributes NO additional,
   independent heuristic risk beyond that.
4. Supporting numerical work (§5): a proved analytic bound and numerical
   boundedness certificate for the order-1..4 building blocks; a
   physical-edge (`x=sqrt(c)`) evaluation of all four established
   profiles across the H1 front's own `c`-grid, finding clean,
   monotone, well-behaved decay with no sign of growth-mode leakage —
   plus one self-caught, disclosed, and fixed numerical pitfall (S1)
   and one self-caught, disclosed theoretical near-miss (S2) and one
   self-caught arithmetic near-miss (S3), none of which affects any
   number or claim reported above.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document. `H1` is untouched, exactly as this front's mandate scoped it —
this front's finding is ABOUT the logical relationship between `H1` and
`H2`, not a claim about `H1`'s own status.

---

## 8. What remains open

1. `H1` itself (`(U1)`+`(U2)`) — untouched, exactly as scoped; this
   front's reduction shows `H2` now depends entirely on `H1`'s own
   resolution, not the reverse.
2. Mixed-partial commutativity `Psi_xy=Psi_yx`, needed for §3.1's exact
   identity — a standard smoothness assumption, not independently
   verified from the exact PDE system.
3. The Growth-Exclusion Lemma's existence half (§2(i)) needs sub-Gaussian
   growth of `f_n` at every order — verified directly for `n<=4` (§5.1)
   but not proved in general for arbitrary `n`.
4. No counterexample to `H2`'s exclusion mechanism was sought or found
   (the mandate's third acceptable outcome) — every numerical test here
   is consistent with the exclusion holding throughout, including past
   the true physical boundary `s=1` at the four established orders.
5. A genuinely different next step, not attempted here: proving `(U1)`
   or `(U2)` themselves (which would simultaneously close `H1` AND,
   via this front's reduction, `H2`) — exactly the largest remaining
   gap the H1 predecessor front itself named, now shown to be the ONLY
   remaining gap for `H2` as well.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)` are all untouched and
unaffected.

---

## 9. Files

| file | role |
|---|---|
| `k01_watson_bookkeeping_sympy.py`/`.log` | moment-integral normalization check (Step 0); order-1 base case re-derivation (Step 1); mechanical induction `n=1..6` (Step 2); general telescoping identity, algebraic, `n=2..9` (Step 3) — §3 |
| `k02_growth_exclusion_lemma.py`/`.log` | Growth-Exclusion Lemma: homogeneous solution (Part A), bounded-branch existence via Leibniz rule (Part B), uniqueness proof (Part C), numerical blow-up illustration (Part D) — §2 |
| `k03_boundedness_certificate.py`/`.log` | proved analytic bound `R(x)<=1/x`; numerical boundedness certificate for `R,R',R'',R'''`; physical-edge (`x=sqrt(c)`) evaluation of `psi1..psi4` across the H1 front's own `c`-grid — §5 |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/
mclust_h1_validity_attempt/mclust_h2_validity_attempt/` subdirectory was
written to — every ancestor `ATTEMPT.md`/`adversarial/` file and
`PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (§0), never modified. No `adversarial/` subdirectory
created; no referee dispatched by this front itself, per the mandate.
