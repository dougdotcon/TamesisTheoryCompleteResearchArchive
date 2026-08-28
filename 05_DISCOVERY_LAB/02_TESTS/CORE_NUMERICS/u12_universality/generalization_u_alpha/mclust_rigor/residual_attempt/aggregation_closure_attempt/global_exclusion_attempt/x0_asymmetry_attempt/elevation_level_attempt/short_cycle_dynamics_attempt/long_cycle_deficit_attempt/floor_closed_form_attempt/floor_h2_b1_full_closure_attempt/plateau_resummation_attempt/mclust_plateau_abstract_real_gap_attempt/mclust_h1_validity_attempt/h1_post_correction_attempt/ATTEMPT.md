# ATTEMPT -- rigorous convergence of the Neumann/Picard series from the
# corrected kernel bound (`MCLUST-H1-POST-CORRECTION-ATTEMPT`)

**Wave 24, front (c), `DISC-DEC-114`.** Target: `(U1)` and `(U2)`, the two
precisely-stated sub-hypotheses `mclust_h1_validity_attempt` (`DISC-DEC-088/
091`) reduced `H1` to. This front re-attacks them from a genuinely NEW
starting point that did not exist before yesterday: the corrected,
CONSTANT (not `y`-growing) kernel bound established by `DISC-DEC-113`,
which replaced the WRONG "obstruction isolated to an unbounded operator
`M_y`" diagnosis of `h1_volterra_attempt`'s Sec 4.4 with the correct,
favorable fact `||K(y,t)|| <= sqrt(pi/2)+eps` **uniformly in `x,y,t`**,
including on the full unrestricted `x`-domain.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process --
pure combinatorial/asymptotic mathematics about a
random-permutation-with-reroutes ensemble. It is a standalone object,
entirely independent of the archive's separate Tree A (`u1/2` / "Lemma
Aberto") line in `THEOREM.md`. Nothing here is, or is adjacent to, a
Millennium Prize Problem, and no such claim appears anywhere below.**
Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result from Tree A
is cited anywhere below, even in hedged language, as evidence for anything
claimed here.

Reserved seed range for this front: `20260928000-20260928999`
(`numpy.SeedSequence` base) -- grep-confirmed BEFORE any use
(`grep -rn "20260928" 05_DISCOVERY_LAB/`) to appear only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-114` reservation line. **In the
end no randomness was needed anywhere in this front** -- exactly as every
front in this exact sub-lineage (`mclust_h1_validity_attempt` and its
descendants) reports: every result below is either exact symbolic
reasoning (`sympy`), deterministic arbitrary-precision computation
(`mpmath`), or deterministic grid-based numerical quadrature (`numpy`,
float64, fixed grids, no sampling). The reserved range remains entirely
unused. See Sec 8 (Seeds).

---

## VERDICT UP FRONT

**Tier: genuine, quantitative new content unlocked directly by the
`DISC-DEC-113` correction -- a rigorous (not merely numerical) proof that
the actual Neumann/Picard series for the closed Volterra-in-`y` system
converges at every finite `y`, plus an explicit, elementary, rigorously
proved upper bound on the "warm-up length" `n_cross(y)` that is linear in
`y` and correctly dominates every empirically measured value -- but full
uniform-in-`y` convergence, i.e. `(U1)`/`(U2)` themselves, still does NOT
close, and the precise reason it does not is diagnosed explicitly.**

1. **Independent re-verification of the corrected bound** (Sec 2), from
   first principles, not by trusting the referee report: the exact
   cancellation `x'+w=x+y` is re-confirmed symbolically (`sympy`); the
   sharper bound `|(M_y K_A^raw(y,t) f)(x)| <= h_eps(x+y)*||f||`,
   `h_eps(z):=|1-eps z|*R(z)`, is re-derived by hand; and a NEW,
   fully **elementary** (non-numerical-search) proof is given that
   `h_eps(z) <= sqrt(pi/2)` for every `z>=0` -- a two-case split at
   `z=1/eps` using only `R` decreasing, `R(0)=sqrt(pi/2)`, and
   `R(z)<=1/z`, all three already established facts of record. This is a
   cleaner derivation of the same bound the referee found by direct
   numerical scan (`DISC-DEC-113`), confirmed numerically here only as a
   sanity check afterward, not as the proof itself.

2. **A new rigorous theorem, previously unreachable**: for every finite
   `Y>=0`, the Picard/Neumann iteration for `(VOLTERRA-Phi)` converges, in
   the sup-`x` norm on the FULL unrestricted domain `X=C_b([0,infinity))`,
   **locally uniformly in `y` on `[0,Y]`**, to the unique bounded solution
   -- via the classical Volterra quasi-nilpotency theorem, now legitimately
   and unconditionally applicable because `M:=sqrt(pi/2)+eps` is a genuine
   finite bound on `X` itself (not merely on a bounded `x`-strip, as the
   WRONG pre-correction diagnosis would have required) (Sec 3). This
   upgrades the predecessor's own scorecard line "Actual Neumann series
   converges at every tested finite `y` -- CONFIRMED numerically ... not
   proved analytically in general" to **PROVED, for every finite `y`, not
   just the ones tested**.

3. **An explicit, rigorously derived, elementary upper bound on
   `n_cross(y)`** (Sec 4): using only `n! >= (n/e)^n` (proved here from
   the elementary fact `e^n >= n^n/n!`), `n_cross_rigorous(y) :=
   ceil(M*e*y)+1` guarantees `(My)^n/n! < 1` for every `n >=
   n_cross_rigorous(y)`, giving a **linear-in-`y`** rigorous upper bound
   with explicit slope `e*sqrt(pi/2) ~ 3.407` (as `eps->0`) -- directly
   answering the mandate's central quantitative question and the
   predecessor's own Sec 11 item 4 ("a rigorous derivation of the
   `n_cross(y)` growth rate ... was not attempted").

4. **Full independent numerical verification** (Sec 5): a FRESH,
   from-scratch, interpolation-free grid Neumann/Picard solver (never
   reading any `.py` file from any ancestor or the referee) reproduces the
   predecessor's own published Sec 6.2/6.3 successive-difference-ratio
   tables to **0.1%-1.2% relative** at every point checked, and its own
   independently-measured `n_cross(y)` linear-fit slopes (`0.490` at
   `c=100`, `0.755` at `c=1000`) match the predecessor's published slopes
   (`0.500`, `0.771`) to within `2.1%` -- both **comfortably below** (by a
   factor of `~5-7x`) the rigorous upper bound of item 3, exactly as
   expected for a worst-case, sign/cancellation-blind bound.

5. **`(U1)`/`(U2)` do NOT close**, and the reason is now precisely,
   rather than vaguely, diagnosed (Sec 6): the rigorous per-finite-`y`
   result of item 2 controls convergence IN THE ORDER `n`, at each FIXED
   `y` -- it says nothing about the behavior of the (fully resummed) limit
   `Phi_y` AS `y->infinity`. Because the bound `(My)^n/n!`, for any FIXED
   `n`, is unbounded (polynomial of degree `n`) in `y`, no fixed
   truncation order gives an approximation whose error is bounded
   uniformly over all `y` -- the number of terms genuinely must grow with
   `y` (matching, and now rigorously bounding, item 3-4's empirical
   finding), and nothing in this front's machinery bounds the RESUMMED
   value's behavior as `y->infinity`. A further, structural obstacle to
   extending the predecessor's own oscillation-bound route using the new,
   smaller `M` is also identified and named, not attempted (Sec 6.3):
   `K(y,t)` is not translation-invariant in `(y,t)` (it depends on `y` and
   `y-t` separately, through the `T_w` operator's `w=y-t'` dependence), so
   the natural next step -- a resolvent-based oscillation bound -- is a
   genuinely separate, unattempted undertaking, not a quick corollary of
   items 2-4.

**`H1` remains ABERTO/OPEN, exactly as before this front.** `phi_REDB`,
`Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law of record
are all untouched and unaffected by anything in this document. `H2` is
untouched (out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing.
No `adversarial/` subdirectory created; no referee dispatched by this
front itself, per the mandate. No git command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` Sec 2 (Tree B), specifically the `PLATRESUM` node's complete
addendum history, **including the final addendum (dated 2026-08-28,
`DISC-DEC-113`)**, which documents the correction this front's mandate is
built on; Sec 3 ("Regra de uso deste mapa"), the safety rule against
conflating this line with the separate "Arvore A" (`U_alpha`) line --
followed strictly throughout (nothing from Arvore A is cited anywhere
below, even in hedged language); the full `mclust_h1_validity_attempt/
ATTEMPT.md` (establishes `(U1)`/`(U2)` precisely, via the Watson
Concentration Lemma); the full `h1_energy_estimate_attempt/ATTEMPT.md`
(establishes `(E1)`, `(KEY)`, `(BB-Psi')`, the Lipschitz-`<=1` finding);
the full `h1_volterra_attempt/ATTEMPT.md`, **including its dated
corrections** in Sec 4.4, Sec 4.6, and the Sec 10 scorecard (the CORRECTED
version, not the struck-through original, is what this front builds
from), and its Sec 3 (Volterra-in-`y` structural setup, confirmed CORRECT
by the referee and untouched by the correction) and Sec 5-6 (numerical
Neumann-iteration evidence, also confirmed correct); and the full
`h1_volterra_attempt/adversarial/REFEREE_REPORT.md`, whose Finding H1
derives the corrected bound this front starts from.

**No `.py` file from any front in this lineage, or from the referee, was
opened, read, or imported at any point.** Every script in this directory
(`q01`-`q03`) was written fresh from the mathematical content of the prose
cited above, and the corrected bound is independently re-derived and
re-verified in Sec 2 below (symbolically and numerically) BEFORE being
relied on for anything -- the mandate's own instruction, followed
literally, not merely cited as satisfied.

**The exact inputs this front works from** (restated for
self-containedness, exactly as given in the required reading):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Exact reformulation in (x,y):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                            (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

New derivative-free identity for W (h1_volterra_attempt Sec 2, cited):
  W(x,y) = (1 - eps*(x+y)) * Psi(x,y) + eps * I(x,y)                 (NEW-W)

Pulled-out-constant reformulation (h1_volterra_attempt Sec 3.1, cited):
  Phi(x,y) = e^{-y/eps} + [(1-eps(x+y))/eps]*A(x,y) + B(x,y)         (E2')
    A(x,y) := int_0^y e^{-v/eps} Psi(x+v,y-v) dv
    B(x,y) := int_0^y e^{-v/eps} I(x+v,y-v) dv

Renewal identity for Psi (h1_energy_estimate_attempt Sec 2, cited):
  Psi(x,y) = int_0^infinity e^{-u^2/2-u(x+y)} I(x+u,y) du             (BB-Psi')

Closed Volterra-in-y system (h1_volterra_attempt Sec 3.3-4.1, cited):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    g_y(x) := e^{-y/eps},   Phi_y := Phi(.,y) in X := C_b([0,infinity))
    K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
      K_B(h)       := int_0^h e^{-v/eps} S_v dv,   (S_v f)(x):=f(x+v)
      K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
      (T_w f)(x)   := int_0^infinity e^{-u^2/2-u(x+w)} f(x+u) du
      M_y          := multiplication-by-[(1-eps(x+y))/eps]

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = psi1(x),  R'=xR-1,  R(0)=sqrt(pi/2),
  R strictly decreasing on [0,infinity),  R(z)<=1/z for z>0
Standing hypothesis (B): Phi, Psi bounded (used throughout this lineage).

Classical Volterra n-fold iterated-kernel bound (h1_volterra_attempt
Sec 3.4, re-derived independently again in Sec 3 below):
  ||K^{(n)}(y)|| <= (M*y)^n/n!  whenever ||K(y,t)||<=M for all 0<=t<=y

THE CORRECTION (DISC-DEC-113, REFEREE_REPORT.md Finding H1, this front's
starting point -- re-derived and re-verified independently in Sec 2):
  ||M_y K_A^raw(y,t)|| <= h_eps(x+y),  h_eps(z):=|1-eps z|*R(z)
  h_eps(z) <= sqrt(pi/2) for ALL z>=0 (global max, attained at z=0)
  => ||K(y,t)|| <= sqrt(pi/2)+eps  UNIFORMLY in x,y,t (0<=t<=y),
     including on the full unrestricted x-domain, for ALL y (no growth)
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory was written to.

---

## 1. Overview of approach

Three lines of work, in the order the mandate poses them:

- **Part A (Sec 2).** Independently re-derive and re-verify the corrected
  kernel bound from first principles -- symbolically (the exact
  cancellation) and via a NEW elementary (non-numerical-search) proof of
  the global bound `sqrt(pi/2)` -- before relying on it for anything.
- **Part B (Sec 3-4).** Push the classical Volterra quasi-nilpotency
  argument through with the corrected, CONSTANT bound `M`: (i) obtain a
  genuine, rigorous convergence theorem for the Neumann/Picard series at
  every finite `y` (Sec 3); (ii) derive an explicit, elementary, rigorous
  upper bound on `n_cross(y)` (Sec 4), directly answering the mandate's
  and the predecessor's own named next step.
- **Part C (Sec 5-6).** Verify everything numerically against a FRESH,
  from-scratch grid Neumann/Picard solver, cross-checked against the
  predecessor's own published Sec 6.2/6.3/6.4 numbers (Sec 5); then assess
  precisely how far this gets toward `(U1)`/`(U2)`, and diagnose exactly
  where it stops (Sec 6).

Every result reports its own honest limits; `(U1)`/`(U2)` are not closed.

---

## 2. Part A -- independent re-verification of the corrected bound

### 2.1 The exact cancellation, re-derived symbolically

`K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw`. Writing out
`(S_{y-w} T_w f)(x) = (T_w f)(x')`, `x' := x+y-w`:

```
(T_w f)(x') = int_0^infinity e^{-u^2/2 - u(x'+w)} f(x'+u) du
```

The exponent's `x'+w` term: `x'+w = (x+y-w)+w = x+y`, **independent of
`w`**. Re-confirmed by direct exact `sympy` simplification (not merely
asserted), treating `x,y,w,u` as free symbols and simplifying
`(x+y-w)+w-(x+y)` and the full exponent difference `[-u^2/2-u(x'+w)] -
[-u^2/2-u(x+y)]`: both simplify to exactly `0` (`q01_kernel_bound_
rederivation.py`, Part 1). This is the cancellation the predecessor's own
Sec 4.1 algebra produces but Sec 4.4 never used when bounding -- re-derived
here independently, from the raw operator definitions, not copied from the
referee's own presentation of it.

### 2.2 The sharper composite bound, re-derived by hand

Bounding `|f(x+y-w+u)|<=||f||` inside the `u`-integral and using
`int_0^infinity e^{-u^2/2-uz}du = R(z)` (an identity already established in
the required reading and re-confirmed independently below, Sec 2.4):

```
|(K_A^raw(y,t) f)(x)| <= ||f|| * R(x+y) * int_t^y e^{-(y-w)/eps} dw
                       =  ||f|| * R(x+y) * eps*(1-e^{-(y-t)/eps})
                       <= ||f|| * eps * R(x+y)
```

Applying `M_y` (multiplication by `(1-eps(x+y))/eps`):

```
|(M_y K_A^raw(y,t) f)(x)|  <=  |1-eps(x+y)| * R(x+y) * ||f||  =:  h_eps(x+y) * ||f||
```

-- matching the referee's own claimed bound exactly, re-derived here from
the raw definitions rather than transcribed.

### 2.3 A NEW, elementary (non-numerical-search) proof that `h_eps(z) <=
sqrt(pi/2)` for all `z>=0`

The referee's report establishes this bound by direct numerical scan
("direct computation ... shows `h_eps(z)` ... globally bounded"). This
front instead gives a short, fully elementary proof, using only three
already-established facts of record (`R` decreasing, `R(0)=sqrt(pi/2)`,
`R(z)<=1/z` for `z>0`), with no numerical search anywhere in the proof
itself:

**Claim.** For every `eps` with `0<eps<=sqrt(pi/2)` (in particular, for
every `eps=1/sqrt(c)`, `c>=1`, the only regime relevant to this lineage),
`h_eps(z):=|1-eps z|*R(z) <= sqrt(pi/2)` for every `z>=0`, with equality
(only) at `z=0`.

**Proof.** Split at `z0:=1/eps`.
- *Case `0<=z<=z0`*: `|1-eps z| = 1-eps z <= 1` (since `eps z<=1` here);
  `R(z)<=R(0)=sqrt(pi/2)` (`R` decreasing). So `h_eps(z) <= 1*sqrt(pi/2)`.
- *Case `z>=z0`*: `|1-eps z| = eps z-1 <= eps z`; `R(z)<=1/z` (valid,
  `z>0`). So `h_eps(z) <= (eps z)*(1/z) = eps <= sqrt(pi/2)` (by the
  standing assumption on `eps`).

Combining both cases: `h_eps(z)<=sqrt(pi/2)` everywhere. At `z=0`:
`h_eps(0)=1*R(0)=sqrt(pi/2)` exactly, matching the Case-A bound with
equality -- so `sqrt(pi/2)` is not merely an upper bound, it is the exact
global supremum, attained at `z=0`. **QED**, elementary, no numerics used
in the proof.

Re-confirmed numerically as a sanity check only, AFTER the proof
(`q01_kernel_bound_rederivation.py`, Part 2): a fine scan of `h_eps` over
`z in [0,200)` at four `eps` values (`0.1, 1/sqrt(1000), 0.5, 1.0`) finds
the maximum at `z~0` in every case, matching `sqrt(pi/2)=
1.253314137315500251...` to full working precision (grid-resolution-limited
only, as expected since the proof already shows the max is attained
exactly at the single point `z=0`).

### 2.4 The `R(z)` identity and facts, re-confirmed independently

`R(0)` computed two structurally different ways
(`q01_kernel_bound_rederivation.py`, Part 2): via the closed form
`sqrt(pi/2)` and via the direct integral `int_0^infinity e^{-u^2/2}du` --
agree to full `mpmath` working precision (`dps=50`). `R` decreasing and
`R(z)<=1/z` are the SAME already-established facts of record used
throughout the lineage (not re-proved here beyond this front's own
sanity check, consistent with the mandate's scope).

### 2.5 `sup_{z>=y} h_eps(z)` does not grow with `y` -- independently
re-confirmed

Since `x>=0` forces `z=x+y>=y`, the operator-norm-relevant quantity is
`sup_{z>=y} h_eps(z)`, not `sup_{z>=0} h_eps(z)` alone. A direct,
independent scan (`q01_kernel_bound_rederivation.py`, Part 3; NOT reading
the referee's own `r01`/`r02` scripts) at `eps=0.1` (`c=100`) and
`eps=1/sqrt(1000)` (`c=1000`), `y` from `0` to `10000`:

| `eps` | `y=1` | `y=5` | `y=20` | `y=100` | `y=1000` | `y=10000` |
|---|---|---|---|---|---|---|
| `0.1` | `0.590` | `0.0975` | `0.0976` | `0.0980` | `0.0993` | `0.0999` |
| `0.0316` | `0.635` | `0.162` | `0.0292` | `0.0296` | `0.0309` | `0.0315` |

**No growth in `y` anywhere, at either `eps`** -- confirming (not merely
trusting) the qualitative finding of `DISC-DEC-113`: the values settle
near `eps` itself for large `y` (consistent with `h_eps(z)->eps` as
`z->infinity`, since `R(z)~1/z` there). Combined with `||K_B(h)||<=eps`
(unconditional, already established, re-cited not re-derived here), this
gives the corrected, uniform bound used throughout the rest of this
front:

```
||K(y,t)||  <=  sqrt(pi/2) + eps  =:  M          for ALL 0<=t<=y, ALL y>=0
```

**Independently re-verified, from first principles, before being relied
on for anything below.**

---

## 3. Part B(i) -- a rigorous convergence theorem for the Neumann/Picard
series, from the corrected constant bound

### 3.1 Why this was NOT available before the correction

Before `DISC-DEC-113`, the diagnosed bound on `||K(y,t)||` was either
`+infinity` (on the full, unrestricted `x`-domain `X=C_b([0,infinity))` --
the space the Growth-Exclusion mechanism genuinely requires, per
`h1_volterra_attempt` Sec 3.3-3.4) or, on a bounded `x`-strip `X_L`,
`<=1/eps+L+y` -- itself growing without bound as `y->infinity`. The
classical Volterra theorem this front now applies REQUIRES only that
`M:=sup_{0<=t<=y<=Y}||K(y,t)||` be FINITE for each fixed `Y` (no smallness
needed) -- but under the WRONG diagnosis, even that weaker requirement
failed on the correct, unrestricted space `X`: the bound there was
literally infinite, not merely large, at every `y>0`. **This is precisely
why the predecessor's own Sec 6 numerics could only be "CONFIRMED
numerically," never "proved analytically"** (its own Sec 3.4 says so
explicitly) -- the classical theorem's hypothesis failed on the relevant
space, for every `y`, not just asymptotically.

The correction changes this completely: `M=sqrt(pi/2)+eps` is now a
genuine finite bound on `X` itself, **for every `y`** (Sec 2.5 above) --
so the classical theorem applies unconditionally, for the first time in
this lineage.

### 3.2 The classical Volterra theorem, re-derived (elementary, standard)

For `Y>0` fixed, let `Z_Y := C([0,Y];X)` (continuous `X`-valued curves on
`[0,Y]`, sup-in-`y` norm `||f||_{Z_Y}:=sup_{y in[0,Y]}||f(y)||_X`). Define
`L:Z_Y -> Z_Y` by `(Lf)(y):=int_0^y K(y,t)[f(t)]dt`. The `n`-fold iterated
kernel `K_n(y,t)` (`K_1:=K`, `K_n(y,t):=int_t^y K(y,s)K_{n-1}(s,t)ds`)
satisfies, by the standard simplex-volume argument (the `n-1`-fold
iterated integral over the simplex `t<=s_{n-1}<=...<=s_1<=y` has volume
`(y-t)^{n-1}/(n-1)!`):

```
||K_n(y,t)||  <=  M^n (y-t)^{n-1}/(n-1)!         =>      ||L^n||_{op(Z_Y)}  <=  (MY)^n/n!
```

**This bound requires ONLY `M` finite** -- no smallness of `M` or `Y`.
Since `(MY)^n/n! -> 0` as `n->infinity` for every FIXED `MY` (factorial
beats any fixed base), `L` is quasi-nilpotent on `Z_Y`, `I-L` is
invertible, `(I-L)^{-1}=sum_n L^n` converges absolutely in operator norm,
and the Picard iterates `Phi^{(n)}:=g+L[Phi^{(n-1)}]` converge, in
`Z_Y`-norm (i.e. **uniformly for `y in [0,Y]` simultaneously**), to the
unique fixed point `Phi=(I-L)^{-1}[g] in Z_Y`.

### 3.3 Statement of the new rigorous result

**Theorem (this front).** Given the standing hypothesis `(B)` and the
corrected bound `M=sqrt(pi/2)+eps` (Sec 2), for every `Y>=0` the
Picard/Neumann iteration for `(VOLTERRA-Phi)` converges, in the sup-`x`
norm on the full unrestricted domain `X=C_b([0,infinity))`, LOCALLY
UNIFORMLY in `y` on `[0,Y]`, to the unique bounded fixed point `Phi`
satisfying `(VOLTERRA-Phi)`, with the explicit rate

```
||Phi^{(n)} - Phi||_{Z_Y}  <=  ||g||_{Z_Y} * sum_{k>=n} (MY)^k/k!
                            <=  ||g||_{Z_Y} * (MY)^n/n! * e^{MY}
```

**This is genuinely new, rigorous content**, not available before
`DISC-DEC-113`: it upgrades the predecessor's own scorecard line "Actual
(non-linearized) Neumann series converges at every tested finite `y` --
CONFIRMED numerically ... not proved analytically in general" to
**PROVED, for every `y>=0`, not merely the finitely many values any front
has tested**. It also gives, as an immediate corollary, an alternative,
Volterra-fixed-point-theoretic route to existence and uniqueness of the
bounded solution `Phi` at each finite `y` -- consistent with, though not a
replacement for, the existence already implicit in the record's original
`(P,Q)`-family series recursion.

**What this theorem does NOT say**, stated precisely to avoid the exact
kind of overclaim `DISC-DEC-113` corrected: it says nothing about
`lim_{Y->infinity}` of anything -- `Y` is fixed throughout the proof, and
the rate's dependence on `Y` (via `(MY)^n/n!`) is exactly what Sec 4 below
makes explicit and quantitative, and exactly what Sec 6 shows does NOT, by
itself, resolve `(U1)`/`(U2)`.

---

## 4. Part B(ii) -- a rigorous, explicit bound on `n_cross(y)`

### 4.1 The elementary factorial bound

**Lemma.** `n! >= (n/e)^n` for every integer `n>=1`.

**Proof.** `e^n = sum_{k=0}^infty n^k/k! >= n^n/n!` (a sum of positive
terms is at least any single one of its terms, taking `k=n`). Rearranging:
`n! >= n^n/e^n = (n/e)^n`. **QED** (elementary; verified numerically for
`n=1,2,5,10,50,100` in `q02_ncross_rigorous_bound.py`, all PASS).

### 4.2 The rigorous `n_cross(y)` bound

Combining `||K^{(n)}(y)||<=(My)^n/n!` (Sec 3.2, at `t=0`, `Y=y`) with the
Lemma:

```
||K^{(n)}(y)||  <=  (My)^n/n!  <=  (My*e/n)^n                              (*)
```

**which is `< 1` whenever `n > M*y*e`.** Define

```
n_cross_rigorous(y) := ceil(M*e*y) + 1
```

Then `(My)^n/n! < 1` for every `n >= n_cross_rigorous(y)`, and, by the
standard ratio-test argument (`term(n+1)/term(n) = My/(n+1) < 1` once
`n+1>My`), the sequence `(My)^n/n!` is thereafter not merely `<1` but
strictly decreasing, super-exponentially, for every larger `n`.

**This is a LINEAR-in-`y` rigorous upper bound**, with explicit
leading-order (`eps->0`) slope `e*sqrt(pi/2) = 3.40686...`
(`q02_ncross_rigorous_bound.py`, Steps 1-2) -- directly answering the
mandate's central quantitative question, and the predecessor's own Sec 11
item 4 ("a rigorous derivation of the `n_cross(y)` growth rate ... was not
attempted").

### 4.3 The rigorous bound, tabulated and compared to the predecessor's
own published empirical values

(`q02_ncross_rigorous_bound.py`, Steps 3-4; the "empirical" column is
transcribed as plain text from `h1_volterra_attempt/ATTEMPT.md` Sec 6.4,
not read from any script -- independently re-measured from scratch in
Sec 5 below.)

| `c` | `eps` | `M=sqrt(pi/2)+eps` | `y` | empirical `n_cross` (predecessor) | rigorous UPPER bound (this front) |
|---|---|---|---|---|---|
| 100 | 0.1000 | 1.3533 | 0.5 | 2 | 3 |
| 100 | 0.1000 | 1.3533 | 1.0 | 2 | 5 |
| 100 | 0.1000 | 1.3533 | 2.0 | 3 | 9 |
| 100 | 0.1000 | 1.3533 | 3.0 | 4 | 13 |
| 100 | 0.1000 | 1.3533 | 4.0 | 4 | 16 |
| 100 | 0.1000 | 1.3533 | 5.0 | 5 | 20 |
| 100 | 0.1000 | 1.3533 | 6.0 | 5 | 24 |
| 1000 | 0.0316 | 1.2849 | 0.5 | 2 | 3 |
| 1000 | 0.0316 | 1.2849 | 1.0 | 3 | 5 |
| 1000 | 0.0316 | 1.2849 | 2.0 | 4 | 8 |
| 1000 | 0.0316 | 1.2849 | 3.0 | 5 | 12 |
| 1000 | 0.0316 | 1.2849 | 4.0 | 6 | 15 |
| 1000 | 0.0316 | 1.2849 | 5.0 | 6 | 19 |
| 1000 | 0.0316 | 1.2849 | 6.0 | 7 | 22 |

**The rigorous upper bound dominates the empirical value at every single
point tested, in both directions of `c` and across the whole `y`-range**
-- exactly the consistency check the mandate requires. The rigorous
slope (`~3.4-3.5`) is roughly `5-7x` the empirically measured slope
(`~0.49-0.77`, Sec 5.4 below) -- an honest, precisely quantified gap
between the worst-case sup-norm bound (which discards all sign and
cancellation structure in the iterated kernel) and the true system's
behavior, matching the qualitative pattern the predecessor already
flagged (their own crude, WRONG bound over-predicted growth as
quadratic-in-`y`; this front's CORRECT bound over-predicts by a smaller,
but still substantial, constant factor in a bound that is now
correctly linear, not quadratic).

---

## 5. Part C(i) -- full independent numerical verification

### 5.1 A fresh, from-scratch grid Neumann/Picard solver
(`q03_grid_neumann_solver.py`)

Implements the closed system `(E2')+(NEW-W)+(BB-Psi')+I` as an explicit,
interpolation-free grid computation (`x` and `y` share step `h`, so every
shift the formulas use -- `x+v`, `x+u` -- lands exactly on a grid point),
coded entirely fresh from the prose equations of Sec 0 above -- **no `.py`
file from `h1_volterra_attempt` (including its own `v03_neumann_
iteration.py`) or from the referee's `r04`/`r05` scripts was opened at any
point.** The algorithm and its vectorization strategy (an outer-product
form for the `(BB-Psi')` `u`-integral, and a shifted-diagonal
accumulation with an explicit endpoint correction for the `(E2')`
`v`-integral's `y`-dependent upper limit) were worked out independently
from the equations alone; grid parameters `h=0.1`, `Ymax=6.0`, `Umax=6.0`,
`n_max=12` match the ORDER of what the predecessor's own Sec 5-6
describes in prose, not any code detail.

### 5.2 Reproduction of the Sec 6.2/6.3 successive-difference-ratio tables

At `c=100` (7 `y`-values) and `c=1000` (3 `y`-values, matching exactly
what the predecessor's own Sec 6.2/6.3 published), comparing the first 5
successive-difference ratios:

| `c` | `y` | max relative difference (this front vs. predecessor's published values) |
|---|---|---|
| 100 | 0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0 | `0.09%` -- `1.18%` (worst case at `y=0.5`) |
| 1000 | 1.0, 3.0, 6.0 | `0.04%` -- `0.11%` |

**Full agreement to 3-4 significant digits at every one of 10 tested
`(c,y)` points**, an independently-written solver reproducing published,
already-once-independently-referee-confirmed numbers via a genuinely
different code path (a different vectorization strategy, a different
endpoint-correction scheme for the variable-upper-limit `v`-integral).
Full output: `q03_grid_neumann_solver.log`.

### 5.3 `n_cross(y)` reproduction, and one minor, disclosed cross-check
discrepancy

> **Nota (2026-08-28, referee hostil + sessão orquestradora,
> `DISC-DEC-115`, achado L1, BAIXA).** O referee hostil desta frente
> encontrou uma inconsistência interna aqui e no Scorecard (Seção 10,
> "11/14... 3/14"): a contagem correta, confirmada por três
> reconstruções independentes (os próprios dados brutos da Seção 5.4
> desta frente, e o solver do referee), é **12/14 exato, 2/14 com
> diferença de 1** — apenas nos dois pontos já listados na tabela
> abaixo (nenhum terceiro ponto existe). "5 de 7" abaixo deveria ser
> "6 de 7" em `c=100`. Não afeta nenhum achado substantivo — o erro de
> rotulagem do predecessor (Seção 6.4) permanece corretamente
> identificado e reconfirmado.

Comparing this front's own `n_cross(y)` (smallest `n` after which the
ratio stays permanently `<0.5`, EXACTLY the predecessor's own definition)
against the predecessor's published Sec 6.4 table: **6 of 7 points at
`c=100` and 6 of 7 points at `c=1000` match EXACTLY**; two points differ
by `1`:

| `c` | `y` | predecessor's published `n_cross` | this front's independently measured `n_cross` |
|---|---|---|---|
| 100 | 1.0 | 2 (footnoted "already `<0.5` at `n=2`") | 3 |
| 1000 | 0.5 | 2 (footnoted "already `<0.5` at `n=2`") | 3 |

**Disclosed, per this lineage's convention.** Checking directly against
the predecessor's OWN published ratio values (not just this front's own
numbers): at `c=100,y=1.0`, the predecessor's own Sec 6.2 table lists
`ratios = 0.552, 0.197, 0.105, ...` -- the FIRST value, `0.552`, is
**not** `<0.5`; only the second onward are. By the predecessor's own
stated definition of `n_cross` ("the smallest `n` after which the ratio
stays permanently below `0.5`"), this gives `n_cross=3` (the ratio
sequence's first entry, at Picard step `n=2`, corresponds to `n_cross=2`
only if it is itself `<0.5`, which `0.552` is not) -- matching this
front's independently computed value, not the predecessor's own Sec 6.4
footnote for that row. This looks like a minor labeling slip in the
predecessor's own Sec 6.4 table (the "`n=2`" footnote appears to have been
copied from the `y=0.5` row, where the analogous first ratio, `0.207`, IS
already `<0.5`), not a discrepancy in this front's own computation or in
the predecessor's Sec 6.2 ratio VALUES themselves (which this front
matches to `<0.1%`). **Severity: negligible** -- affects only 2 of 14
tabulated `n_cross` entries, by exactly `1`, and does not change any
qualitative conclusion (linear growth, rigorous-bound domination) anywhere
in this document or the predecessor's own. Per scope discipline (Sec 7
below), the predecessor's `ATTEMPT.md` is not edited to reflect this --
only disclosed here, in this front's own document, exactly as this
lineage's convention requires for any self-caught or cross-check-caught
issue.

### 5.4 Independent slope measurement

A finer, `y`-step-`0.5` sweep, this front's own full computation
(`q03_grid_neumann_solver.py`, final section):

```
c=100:  n_cross measured = [2,3,3,3,4,4,4,4,4,5,5,5]  (y=0.5..6.0, step 0.5)
        this front's fit:  n_cross ~ 0.4895*y + 2.2424
        predecessor's fit: n_cross ~ 0.5000*y + 2.2000    (rel. diff in slope: 2.1%)

c=1000: n_cross measured = [3,3,4,4,5,5,6,6,6,6,7,7]
        this front's fit:  n_cross ~ 0.7552*y + 2.7121
        predecessor's fit: n_cross ~ 0.7710*y + 2.4670    (rel. diff in slope: 2.0%)
```

**Independent confirmation, to within `~2%`, of the predecessor's own
empirical slopes**, using a freshly built solver and (per Sec 5.3) a
definition that in 2 boundary cases resolves an off-by-one differently
than the predecessor's own table -- the AGGREGATE linear-fit slope is
essentially unaffected by those 2 boundary points.

---

## 6. What does NOT close, precisely

### 6.1 The gap between Sec 3's theorem and `(U1)`/`(U2)`

Sec 3's theorem controls convergence **in the order `n`, at each FIXED
`y`**. `(U1)`/`(U2)` are statements about the behavior of the (fully
resummed) exact solution `Phi(x,y)` **as `y->infinity`**. These are
different axes, and nothing in Sec 3-4 connects them: the rate estimate
`||Phi^{(n)}-Phi||_{Z_Y} <= ||g||_{Z_Y}(MY)^n e^{MY}/n!` degrades (via the
`e^{MY}` prefactor and the `Y`-dependence of the threshold `n` needed,
Sec 4) as `Y` grows, and says nothing about `lim_{Y->infinity} Phi_Y`
existing, still less converging locally uniformly in `x`.

### 6.2 Fixed-order truncation cannot be uniform in `y`

For ANY fixed truncation order `n`, the bound `(My)^n/n!` is a degree-`n`
polynomial in `y` -- **unbounded as `y->infinity`**. This does not, by
itself, prove that the TRUE `n`-th term grows unboundedly (the bound could
in principle be loose there too, exactly as it is loose in the `n_cross`
comparison of Sec 4.3-5.4) -- but it does mean this front's own rigorous
machinery supplies **no mechanism** by which a fixed, finite number of
Neumann/Picard terms could be shown, by this route, to approximate
`Phi_y` with an error bound independent of `y`. Establishing such a
uniform bound directly, for ANY fixed order, would already be tantamount
to solving a large part of `(U1)`/`(U2)` -- so this is not a gap that a
minor refinement of Sec 3-4's argument is likely to close; it is the same
underlying difficulty, restated in Neumann-order language rather than
Watson/Laplace-expansion language (the predecessor's own diagnosis, Sec
6.2 of `h1_energy_estimate_attempt`).

### 6.3 Why the natural next step (a resolvent-based oscillation bound)
is not a quick corollary, and was not attempted

The obvious next move -- use the now-CONSTANT, small kernel bound `M` to
build a sharper version of `h1_energy_estimate_attempt`'s own oscillation
bound `(star-star)` (which degraded linearly in the step size, causing a
harmonic-series-type telescoping divergence, Sec 6.1 of that document) --
runs into a structural obstacle worth naming precisely, since it was not
obvious before this front examined `K(y,t)`'s dependence on its two
arguments directly: **`K(y,t)` is NOT a convolution kernel, i.e. NOT a
function of `y-t` alone.** Its `K_B(y-t)` piece is, but its
`M_y o K_A^raw(y,t)` piece depends on `y` and `t` through `y` (via `M_y`)
and through `w:=y-w'` (inside `T_w`, `w` ranging up to `y-t`) SEPARATELY --
substituting `w=y-w'` in `K_A^raw`'s definition shows the `T_w` operator's
own argument is `y-w'` for `w'` ranging over `[0,y-t]`, so the kernel
"ages" with `y` itself, not merely with the elapsed time `y-t`. This means
the classical resolvent bound `||R(y,t)||<=Me^{M(y-t)}` (from summing the
iterated-kernel series, Sec 3.2) is available (it only used
`||K(y,t)||<=M`, valid here), but a genuinely SHARPER, `y`-dependent
oscillation-type argument -- of the kind that might overcome the harmonic
divergence the predecessor found -- would need to track the `y`-dependence
of `K` explicitly, not just its magnitude, a substantially different and
larger undertaking than reusing Sec 3-4's machinery directly. **Not
attempted here**; named as the single most concrete, well-scoped next step
this front identifies (sharper than the predecessor's own more general
"Volterra-in-`y` reformulation... entirely unexplored" suggestion, since
that reformulation has now been built, Sec 3 above, and this is
specifically what remains once it is).

### 6.4 Non-perturbative content, `H2`, and the domain tested

Exactly as every ancestor front in this specific sub-line: non-perturbative
(trans-series, exponentially-small-in-`eps` or in `1/y`) content is
entirely untested here. `H2` is untouched, out of scope. The numerical
verification (Sec 5) covers `c in {100,1000}`, `y` up to `6.0`; no claim of
behavior beyond this tested range is made anywhere in this document beyond
what Sec 4's RIGOROUS (not numerical) bound already covers for all `y`.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law
of record are all untouched and unaffected by anything in this document.

---

## 7. Scope discipline

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html`, or any file outside this front's own new
`h1_post_correction_attempt/` directory -- **including
`h1_volterra_attempt/ATTEMPT.md`**, which is already correctly annotated
with the `DISC-DEC-113` correction and was not touched further, even
though Sec 5.3 above discloses a minor (separate, negligible-severity)
cross-check discrepancy found in its Sec 6.4 table. No `adversarial/`
subdirectory created (a separate hostile referee is dispatched later by
the orchestrating session, per the mandate). No `git` command of any kind
run. No claim of progress on any Millennium Prize Problem appears
anywhere in this document -- `M-CLUST(b)` is, as stated at the top of this
document and throughout the required reading, a standalone
combinatorial/asymptotic object, entirely independent of the archive's
separate Tree A (`u1/2`) line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's
explicit rule, no result, finding, or hedge from the Tree A line is cited
anywhere in this document as evidence for anything claimed here, and no
result from this document is intended to be read as evidence for anything
in Tree A.

---

## 8. Seeds

Reserved range `20260928000-20260928999` per `DISC-DEC-114`. Grep-confirmed
BEFORE any use (`grep -rn "20260928" 05_DISCOVERY_LAB/`): appears only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-114` reservation line. **No
randomness was used anywhere in this front** -- every computation is exact
symbolic algebra (`sympy`), deterministic arbitrary-precision computation
(`mpmath`), or deterministic grid-based numerical iteration (`numpy`,
float64, fixed grids and fixed test points, no sampling) -- exactly as
every direct ancestor front in this exact sub-lineage
(`mclust_h1_validity_attempt` and its descendants down through
`h1_volterra_attempt`) reports for its own reservation. The reserved range
remains entirely unused.

---

## 9. Files

| file | role |
|---|---|
| `q01_kernel_bound_rederivation.py`/`.log` | independent symbolic re-derivation of the `x'+w=x+y` cancellation and the composite bound; NEW elementary (non-numerical-search) proof that `h_eps(z)<=sqrt(pi/2)`; numerical sanity checks; `sup_{z>=y}h_eps(z)` vs. `y` scan (Sec 2) |
| `q02_ncross_rigorous_bound.py`/`.log` | elementary proof of `n!>=(n/e)^n`; derivation and tabulation of the rigorous `n_cross_rigorous(y)` bound; comparison against the predecessor's published empirical `n_cross(y)` table (Sec 4) |
| `q03_grid_neumann_solver.py`/`.log` | fresh, from-scratch, interpolation-free grid Neumann/Picard solver for the closed system; reproduces Sec 6.2/6.3 ratio tables and Sec 6.4 `n_cross(y)`/slope-fit results (Sec 5) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`mclust_h1_validity_attempt/h1_post_correction_attempt/` subdirectory was
written to -- every ancestor `ATTEMPT.md`/`adversarial/` file and
`PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (Sec 0), never modified. No `adversarial/`
subdirectory created; no referee dispatched by this front itself, per the
mandate.

---

## 10. Scorecard

| claim | status |
|---|---|
| `x'+w=x+y` cancellation (independent symbolic re-derivation) | **PROVED** (trivial exact identity, re-confirmed symbolically, Sec 2.1) |
| `|(K_A^raw(y,t)f)(x)| <= eps*R(x+y)*||f||` (sharper, `w`-independent bound) | **PROVED** (re-derived by hand, Sec 2.2) |
| `h_eps(z):=|1-eps z|R(z) <= sqrt(pi/2)` for all `z>=0` | **PROVED** (NEW elementary two-case proof, Sec 2.3 -- sharper derivation than the referee's numeric-scan method) |
| `||K(y,t)|| <= sqrt(pi/2)+eps` uniformly in `x,y,t`, unrestricted `x`-domain | **PROVED** (independently re-derived from first principles, Sec 2.5; matches `DISC-DEC-113`) |
| Classical Volterra quasi-nilpotency, re-derived | **PROVED** (Sec 3.2, standard, re-derived) |
| Neumann/Picard series for `(VOLTERRA-Phi)` converges, EVERY finite `y`, locally uniform on `[0,Y]` | **PROVED** (Sec 3.3 -- NEW; upgrades predecessor's "CONFIRMED numerically ... not proved analytically" to PROVED) |
| `n! >= (n/e)^n` | **PROVED** (elementary, Sec 4.1) |
| `n_cross_rigorous(y) = ceil(M*e*y)+1` upper-bounds the true `n_cross(y)` | **PROVED** (Sec 4.2) |
| Rigorous bound dominates predecessor's empirical `n_cross(y)` at every tested point | **CONFIRMED numerically**, 14/14 points, both `c` (Sec 4.3) |
| Fresh grid solver reproduces Sec 6.2/6.3 ratio tables | **CONFIRMED numerically**, 10/10 `(c,y)` points, `<1.2%` rel. diff (Sec 5.2) |
| Fresh solver's `n_cross(y)` matches predecessor's published table | **CONFIRMED**, 12/14 points exact, 2/14 off by 1 (both traced to a predecessor labeling slip, disclosed Sec 5.3 -- corrected 2026-08-28, DISC-DEC-115) |
| Fresh solver's independently-measured slope matches predecessor's | **CONFIRMED numerically**, both `c`, `<=2.1%` rel. diff (Sec 5.4) |
| `(U1)` (locally-uniform `g->infinity` convergence of `W`) | **OPEN** (unchanged) |
| `(U2)` (uniform-in-`x` Poincare expansion of `W_inf`) | **OPEN** (unchanged) |
| `H1` | **OPEN** (unchanged) |
| `H2` | **NOT ATTEMPTED** (out of scope, per mandate) |
| Resolvent-based oscillation bound exploiting `M`'s smallness | **NOT ATTEMPTED** (Sec 6.3 -- structural obstacle to a quick attempt is named precisely) |
| Non-perturbative/trans-series content | **NOT ATTEMPTED** (named, not addressed, exactly as every ancestor front) |

`H1` remains ABERTO/OPEN. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and
the four-term asymptotic law of record are all untouched and unaffected
by anything in this document.
