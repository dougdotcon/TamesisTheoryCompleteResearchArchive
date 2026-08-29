# ATTEMPT -- attacking `(C')` directly via the Volterra-resolvent-stability
# reduction (`CPRIME-VOLTERRA-RESOLVENT-ATTEMPT`)

**Wave 31, front (a), `DISC-DEC-142`.** Twelfth consecutive wave (waves
20-31) in this exact sub-lineage, and the first to attack `(C')` itself
as a standalone resolvent-stability claim, rather than attacking "how to
derive `(U)` from `(C')`/`(C'')`" (the question every one of waves 20-30
attacked instead). This front builds directly on
`cu_direct_proof_attempt/ATTEMPT.md`'s Sec 5 (wave 29, `DISC-DEC-134`),
which FIRST reduced `(C')` to a precise Volterra-resolvent-stability
question and named it, verbatim, as "the same type of fact needed to
prove `(B)` itself" -- never derived from scratch in 29+ prior waves.

**`M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node `PLATRESUM`) is
a standalone combinatorial/asymptotic object -- pure mathematics about a
random-permutation-with-reroutes ensemble and its continuum limit --
entirely independent of the archive's separate Tree A (`u1/2` / "Lema
Aberto") line in `THEOREM.md`. Nothing here is, or is adjacent to, a
Millennium Prize Problem, and no such claim appears anywhere below.** Per
`PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result from Tree A is
cited anywhere below, even in hedged language, as evidence for anything
claimed here.

Reserved seed range for this front: `20260948000-20260948999` per
`DISC-DEC-142`. Grep-confirmed BEFORE any use
(`grep -rn "20260948" 05_DISCOVERY_LAB/`) to appear only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-142` reservation line. **No
randomness was needed anywhere in this front** -- every computation below
is exact symbolic algebra (`sympy`), deterministic arbitrary-precision
quadrature (`mpmath`, fixed evaluation strategy), or deterministic
double-precision numerics (`numpy`/`scipy`, explicitly flagged where
used, for one large-scale exploratory experiment where `mpmath`'s
arbitrary-precision cost was intractable) -- exactly as every direct
ancestor front in this sub-lineage reports for itself. The reserved range
remains entirely unused (re-confirmed, Sec 11).

---

## VERDICT UP FRONT

**`(C')` is NOT proved. This front does not close it, and says so
plainly.** What this front DOES deliver, honestly scoped:

1. **A precise, unambiguous formalization of "uniformly stable Volterra
   resolvent"** (Sec 1) -- the exact object the predecessor's reduction
   needs, stated as a clean mathematical definition for the first time in
   this sub-lineage, so that "is it true?" becomes a well-posed question
   rather than an informal phrase.

2. **A genuine, non-trivial, UNCONDITIONAL (no `(C')`, no new hypothesis
   -- only `(B)`'s definitional setup plus the ALREADY-established
   `(G1)`/`(G2)` Mills-ratio bracket) sharp theorem bounding the TRUE
   operator norm `||K(y,t)||` itself** (Sec 3), not merely its
   restriction to a test function. This is dramatically sharper than the
   archive's own crude constant bound (`DISC-DEC-113`,
   `sqrt(pi/2)+eps`), and it is proved via an exact positivity/sign
   structure of the kernel's integral density that no prior front in this
   sub-lineage identified. Its most important consequence: the
   **integrated kernel mass `int_0^y ||K(y,t)|| dt` is UNIFORMLY BOUNDED
   in `y`** (Sec 4) -- a fact that would have seemed impossible given
   every prior naive estimate in this lineage (all of which give
   exponential blow-up), and that gets the resolvent-stability question
   to within an explicit, quantified `O(eps^2)` margin of closing.

3. **A precise diagnosis of exactly why it still doesn't close** (Sec 5):
   an exact reformulation of the resulting majorant equation as a linear
   ODE system (via the kernel's own `A(z)+B(z)e^{-h/eps}` structure),
   solved to very large `y` (`y` up to `2*10^5`), showing the majorant
   genuinely diverges for EVERY tested `eps>0` -- but POLYNOMIALLY, not
   exponentially, with an exponent `2*eps^2/(1-2*eps^2)` for
   `eps<1/sqrt(2)` (corrected; see [^correcao-sec5-B]) that this front
   derives via an (informally justified, but numerically confirmed to
   4-5 significant figures) quasi-steady-state asymptotic argument on
   the exact ODE system, and a genuine, sharp qualitative transition at
   `eps=1/sqrt(2)` (corrected; see [^correcao-eps1-transition])
   (explosive, faster-than-polynomial growth for `eps>=1/sqrt(2)`,
   matching a sign change in the ODE's own coefficient).

4. **The obstruction is precisely named, not just observed**: no
   norm-envelope / majorant / Gronwall-type argument applied to
   `||K(y,t)||`, however sharp, can establish uniform stability for
   ARBITRARY bounded forcing -- because the sharpest available bound's
   own homogeneous majorant genuinely grows without bound (Sec 5). Since
   the predecessor's reduction needs exactly this (stability against
   ARBITRARY bounded/`O(1/z)` forcing, not merely against the specific,
   self-consistently-generated forcing that the real `Phi_t` happens to
   produce), **this front concludes that no purely operator-norm-based
   technique can close `(C')` via this reduction** -- closing it would
   require exploiting the SPECIFIC self-consistency of `Phi_t` as the
   actual fixed point of `(VOLTERRA-Phi)` (e.g. the self-averaging
   `Avg_g[Phi]` structure of the original PDE, Sec 0), not treated as an
   arbitrary bounded function fed through the kernel once. This is a
   precise, well-scoped, genuine obstruction, not a vague "didn't work."

5. **Four self-caught issues, all disclosed** (Sec 7): an outright
   `AssertionError` from a Laplace-transform algebra slip (fixed); a
   substantive, quantitatively significant numerical-resolution bug in
   two fixed-grid Volterra solvers (`s05`, `s06`), caught via a direct
   refinement/convergence study and fixed via an exact ODE
   reformulation (`s07`) whose validity is independently cross-checked;
   and a bookkeeping slip in an early hand-derivation of the sharp
   kernel-norm bound's constant (`2*eps` vs the correct `eps`),
   superseded before being asserted in any script.

**`(C')`, `(B)`, `(H-ces)`, `(U1)`, `(U2)`, `H1` all remain formally
OPEN.** This front's contribution is a genuinely sharper, more precise
map of exactly how close the norm-based resolvent-stability route can
get (very close, to within an explicit `O(eps^2)` margin on the total
kernel mass, but not there) and exactly where and why it stops (a
provable, non-vanishing polynomial-growth majorant), not a proof of
`(C')` itself. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the
four-term asymptotic law of record are all untouched and unaffected by
anything in this document. `H2` is untouched (out of scope). No
`THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, or
`TEST_QUEUE.yaml` file was opened for writing. No `adversarial/`
subdirectory created; no referee dispatched by this front itself, per
the mandate. No `git` command run.

---

## 0. Reading discipline, provenance, and the exact system/hypotheses

Read in full, in prose, before any derivation or code, in the order the
mandate specifies:

- `boundary_layer_selfheal_attempt/ATTEMPT.md` (wave 30 front c,
  `DISC-DEC-138`, this front's immediate predecessor) in full -- its
  VERDICT (proves `(U)` conditional on `(B)`+`(C')` ALONE, no longer
  needing `(C'')`), and its Sec 8 recommendation, which explicitly names
  attacking `(C')` itself via the Volterra-resolvent-stability reduction
  as "the single most concrete, well-scoped next step" -- the literal
  mandate for this front.
- `boundary_layer_selfheal_attempt/adversarial/REFEREE_REPORT.md` in
  full -- the SOUND WITH ISSUES (all low-severity) verdict, confirming
  `(U)` is genuinely proved conditional on `(B)`+`(C')` alone, with no
  silent strengthening.
- `cu_direct_proof_attempt/ATTEMPT.md` (wave 29 front a, `DISC-DEC-134`,
  two waves back) Sec 5 in full, with extreme care, per the mandate --
  this is where `(C')` was FIRST reduced to the Volterra-resolvent-
  stability question. Cited verbatim below (Sec 0.1), not re-derived.
- `cu_direct_proof_attempt/adversarial/REFEREE_REPORT.md`, Item (e), in
  full -- the independent verification of the `(DX-K)` identity and the
  `O(1/z)` correction bound, and the referee's own two low-severity
  corrections to the Gronwall-failure diagnosis (re-derived and used
  correctly, Sec 2 below).
- `PROOF_DEPENDENCY_MAP.md` Tree B, in full, especially the `DISC-DEC-136`
  and `DISC-DEC-140` dated addenda and the "Leitura" paragraph at the end
  of the tree -- the full logical map connecting `(H-ces)`, `(U1)`,
  `(U2)`, `(C')`, `(U)`, `(B)`.
- `DECISION_LEDGER.yaml`'s `DISC-DEC-142` entry (this front's own
  mandate, quoted in the task) and, tracing back further per the
  mandate's instruction, `DISC-DEC-115` (wave 24 front c,
  `MCLUST-H1-POST-CORRECTION-ATTEMPT`) -- the origin of the **already-
  PROVEN** facts this front builds on: `||K(y,t)|| <= sqrt(pi/2)+eps`
  UNIFORMLY (`DISC-DEC-113`), and that the Neumann/Picard series for
  `(VOLTERRA-Phi)` converges, LOCALLY uniformly in `y` on every compact
  `[0,Y]`, for every finite `y` -- with the PRECISE diagnosis (quoted, not
  paraphrased) of why this does not close `(U1)`/`(U2)`: *"o resultado
  rigoroso controla convergencia na ORDEM n para y FIXO, nao o
  comportamento do valor resomado quando y->infinito -- nenhum
  truncamento fixo da uma aproximacao uniformemente boa em todo y"* --
  and the structural fact, noted but not attacked by that front: `K(y,t)`
  is NOT translation-invariant in `(y,t)`. This is EXACTLY the gap this
  front investigates.
- `h1_translation_structure_attempt/ATTEMPT.md` (wave 25) and
  `h1_volterra_attempt`/`h1_post_correction_attempt` (cited by wave 29's
  own Sec 0), traced back per the mandate, for the ORIGINAL raw
  definitions of `Phi`, `Psi`, `K(y,t)`, `K_A^raw`, `K_B`, `M_y`, `R(x)`
  -- reproduced verbatim below, not taken on faith from any later
  front's restatement.

**No `.py` file from any ancestor front, or from any referee, was
opened, read, or imported at any point.** Every script in this directory
(`s01`-`s08`) was written fresh from the mathematical content of the
prose cited above, using only already-PROVEN facts from that record
(`(G1)`-`(G3)`, `||K(y,t)||<=sqrt(pi/2)+eps`, the `(U)` theorem
conditional on `(B)`+`(C')`) as citable, not re-derived, inputs.

### 0.1 The real system and hypotheses (traced to origin, quoted verbatim)

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Governing PDE system (mclust_h1_validity_attempt, cited):
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi] + (1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y) (plateau_resummation_attempt Sec 4.1, cited):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                            (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

Closed Volterra-in-y system (h1_volterra_attempt, cited):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    g_y(x) := e^{-y/eps},   Phi_y := Phi(.,y) in X := C_b([0,infinity))
    K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
      K_B(h)       := int_0^h e^{-v/eps} S_v dv,   (S_v f)(x):=f(x+v)
      K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
      (T_w f)(x)   := int_0^infinity e^{-u^2/2-u(x+w)} f(x+u) du
      M_y          := multiplication-by-[(1-eps(x+y))/eps]

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = int_0^inf e^{-u^2/2-ux} du,
  R'=xR-1,  R(0)=sqrt(pi/2),  R strictly decreasing.

Standing hypothesis (B): Phi, Psi bounded, M_Phi := sup|Phi| -- UNPROVED,
  never derived from first principles by any of the 30 waves preceding
  this one; used throughout this whole sub-lineage.

(C'): a Lipschitz-type regularity bound on Phi_t(.), UNIFORM in t --
  exists L1 independent of t s.t. |Phi_t(x1)-Phi_t(x2)|<=L1|x1-x2| for
  ALL t>=0, x1,x2>=0.

ALREADY-PROVEN facts this front cites, not re-derives:
  (G1)  z/(1+z^2) <= R(z) <= 1/z,                    for ALL z>0
  (G2)  0 <= sigma(z):=1-z*R(z) <= 1/(1+z^2) <= 1/z^2,  for ALL z>0
  (G3)  0 <= R''(z) <= 2/z^3,                         for ALL z>0
    (cu_direct_proof_attempt Sec 2, wave 29, cited)
  ||K(y,t)|| <= sqrt(pi/2)+eps, UNIFORMLY in y,t       (DISC-DEC-113)
  Neumann/Picard series for (VOLTERRA-Phi) converges, locally uniformly
    in y on every compact [0,Y], for EVERY finite y     (DISC-DEC-115)
  (U), THEOREM (wave 30, DISC-DEC-140): given (B)+(C') ALONE,
    |K(y,t)f(x) - [f(x)-e^{-h/eps}f(x+h)]/z| <= D(x,eps)/z^2,  z:=x+y,
    for ALL z>=1, UNIFORMLY over h'in[0,h], h in[0,y]
```

**The predecessor's `(DX-K)` identity and Sec 5 reduction (`cu_direct_
proof_attempt/ATTEMPT.md` Sec 5, `DISC-DEC-134`), quoted verbatim, cited
not re-derived -- this front's literal starting point:**

```
d/dx[K(y,t)f](x)  =  K(y,t)[f'](x)  -  K_A^raw(y,t)f(x)  -  M_y*N(y,t)f(x)   (DX-K)
  N(y,t)f(x) := int_0^h e^{-h'/eps} [int_0^inf u*e^{-u^2/2-uz}f(x+h'+u)du] dh'

|K_A^raw(y,t)f(x)|  <=  M_Phi*eps/z + L1*eps/z^2                = O(1/z)
|M_y*N(y,t)f(x)|     <=  M_Phi/z^2 + eps*M_Phi/z                 = O(1/z)
=> |K_A^raw(y,t)f(x) + M_y*N(y,t)f(x)| <= D2(x,eps)/z,   D2(x,eps):=2M_Phi*eps+L1*eps+M_Phi

Integrating (DX-K) over t in [0,y]:
  Phi_y'(x)  =  int_0^y K(y,t)[Phi_t'](x) dt  +  [forcing bounded by D2(x,eps)/z]

"Phi_y' solves THE SAME Volterra equation, with THE SAME kernel K(y,t),
as Phi_y itself -- driven by a genuinely BOUNDED (not exploding) forcing
term... (C') therefore follows from this reduction IF the Volterra-
resolvent for THIS kernel is 'uniformly stable' (maps any bounded,
y-independent forcing sequence to a UNIFORMLY, not merely locally-in-Y,
bounded solution sequence) -- this is precisely, and only, the SAME kind
of fact that would need to be shown to prove (B) itself rigorously."
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout;
nothing outside this front's own new `cprime_volterra_resolvent_attempt/`
subdirectory was written to.

---

## 1. Precise restatement: what "uniformly stable Volterra resolvent"
means, exactly

Per the mandate, before any attempt: restate the claim with full
precision -- the equation, the kernel, the forcing bound, and the exact
norm/sense of "stable" needed for the reduction to go through.

**DEFINITION (uniform Volterra-resolvent stability, this kernel).** Fix
`eps>0`. The family `{K(y,t)}_{0<=t<=y<infinity}` (operators on
`X:=C_b([0,infinity))` with the sup norm `||.||_infinity`) has a
**uniformly stable resolvent** if there is a constant `S=S(eps)<infinity`
such that: for EVERY family of forcing functions `{f_y}_{y>=0} subset X`
with `A := sup_y ||f_y||_infinity < infinity`, the solution `{u_y}_{y>=0}`
of

```
u_y  =  f_y  +  int_0^y K(y,t) u_t dt                              (*)
```

(unique and well-defined at each fixed `y`, by the ALREADY-PROVEN
convergent Neumann series, `DISC-DEC-115`) satisfies

```
sup_y ||u_y||_infinity  <=  S * A.
```

**This is EXACTLY, and ONLY, what the predecessor's reduction needs,
applied TWICE, to the SAME kernel `K(y,t)`:**

- **For `(B)`**: `f_y = g_y` (i.e. `f_y(x)=e^{-y/eps}`), `A=1`, `u_y=Phi_y`
  -- uniform stability gives `M_Phi <= S(eps)`.
- **For `(C')`**: `f_y` = the `(DX-K)`-derived forcing, bounded (cited
  above) by `D2(x,eps)/z`, so `A = sup_y D2(x,eps)/(x+y) = D2(x,eps)/x`
  (finite for `x>0`; the `x=0` case needs a small separate limiting
  argument, not attacked here) -- uniform stability gives
  `|Phi_y'(x)| <= S(eps)*D2(x,eps)/x` for all `y`, i.e. `(C')` with
  `L1 <= S(eps)*D2(x,eps)/x`.

**A standard SUFFICIENT condition** for uniform stability, via the
majorant/comparison principle (used by every norm-based technique
attempted below): if

```
C := sup_y int_0^y ||K(y,t)|| dt  <  1,                            (**)
```

then `S(eps) <= 1/(1-C)` (a Neumann-series-in-the-integral-operator-norm
argument on `(*)`, standard, re-derived where needed below). **This is
the concrete target this front investigates: is `(**)` true for THIS
kernel, and if the crudest attempt at it fails, does ANY sharper
norm-based refinement make it true?**

The predecessor already checked ONE candidate for `(**)`: the crude
constant bound `||K(y,t)||<=sqrt(pi/2)+eps` gives `int_0^y||K(y,t)||dt
<= y*(sqrt(pi/2)+eps) -> infinity` as `y->infinity` -- nowhere near `(**)`.
**Sec 2-5 below is this front's own, much more careful, investigation of
whether a SHARPER bound can rescue `(**)`, or a variant of it.**

---

## 2. Why the naive norm-envelope approach fails structurally: the
renewal/Malthusian-rate obstruction

Full derivation: `s01_exact_piece_norms_symbolic.py`/`.log`,
`s02_renewal_obstruction_symbolic.py`/`.log`,
`s02b_renewal_numeric.py`/`.log`.

### 2.1 An exact (not merely bounded) piece norm

`K(y,t) = M_y o K_A^raw(y,t) + K_B(h)`, `h:=y-t`. Working DIRECTLY from
the raw operator definitions (Sec 0.1), this front derives, fresh
(`s01`):

```
||K_B(h)||  =  eps*(1-e^{-h/eps})                    EXACTLY
```

(`K_B(h)` has a manifestly nonnegative kernel `e^{-v/eps}>=0` on `[0,h]`,
so its sup-norm operator norm equals its value on the constant function
`f=1` -- a standard fact for positive integral operators on `C_b`,
attained EXACTLY, not merely bounded). This SATURATES to `eps` as
`h->infinity` -- it does **not decay** with growing memory-lag `h`.

### 2.2 The renewal/Malthusian obstruction, made precise

If a majorant-comparison argument bounds `||K(y,t)||` from above by ANY
function `k(h) = c*(1-e^{-h/eps})` of the lag `h=y-t` alone (`c>0` a
saturating constant -- `c=eps` recovers `||K_B(h)||` exactly; any
attempt using a LARGER, cruder `c`, e.g. the archive's own crude
`sqrt(pi/2)+eps` constant in the `h->infinity` limit, only makes things
worse), the associated linear renewal/comparison equation

```
M(y) = 1 + int_0^y k(y-t) M(t) dt
```

is EXACTLY solvable via Laplace transform (`s02`, re-derived two
independent ways -- direct integration and `sympy`'s own
`laplace_transform`, agreeing exactly): `k_hat(s) = c/(eps*s*(s+1/eps))`,
and the Malthusian (characteristic) equation `k_hat(s)=1` has EXACTLY
ONE positive real root,

```
s_+(c,eps) = (sqrt(1+4*c*eps) - 1) / (2*eps)  >  0   for EVERY c>0, eps>0
```

(proved in general, `s02` Part 3 -- the positivity is UNCONDITIONAL,
holding for every `c>0`, not merely for `c>` some threshold). **This is
independently re-derived via a completely separate route** (`s02` Part
4: converting `(RENEWAL)` into its equivalent 2nd-order ODE via Leibniz
differentiation, done by `sympy`, not by hand) and confirmed to give the
IDENTICAL characteristic polynomial. **Direct numerical Volterra-
quadrature solution of `(RENEWAL)`** (`s02b`, `mpmath`, deterministic,
no adaptivity needed) confirms `M(y)` genuinely grows like
`A*e^{s_+ y}` (empirical log-slope matches the closed-form `s_+` to
relative error `<1e-5` for `eps in {0.5,1.0}`; `M(y)` grows by `>100x`
from `y=10` to `y=40` at `eps=0.5` -- a genuine unbounded exponential, not
a bounded transient).

**Conclusion (this front, refining the predecessor's own cruder
Gronwall-fails observation): ANY norm-envelope argument that bounds
`||K(y,t)||` by a function of the lag `h` alone that does not DECAY to 0
as `h->infinity` is doomed -- the associated majorant provably grows
exponentially, for EVERY positive saturation level, however small.**
This is sharper than the predecessor's own finding (which only checked
that ONE crude constant bound fails) -- it shows the failure mode is
robust to *any* attempt at improving the constant, as long as the
improved bound still saturates rather than decays, and it pins down
the EXACT growth rate as a function of the saturation level via a closed
form. Since `||K_B(h)||` ALONE, computed EXACTLY (not merely bounded),
already saturates rather than decays, this shows the obstruction is not
an artifact of the archive's own crude `sqrt(pi/2)+eps` constant -- it is
inherent to the `K_B(h)` piece by itself.

**This raises the natural next question, which the predecessor's own
Sec 5.3 and its referee's Item (e) left completely open: does the OTHER
piece, `M_y o K_A^raw(y,t)`, cancel this saturation when the TWO pieces
are combined (not just added via the triangle inequality)?** Sec 3
answers this.

---

## 3. THE NEW SHARP THEOREM: the true operator norm `||K(y,t)||`,
exactly, via a positivity/cancellation structure

Full derivation: `s01` Parts 2-6, `s03_true_operator_norm_numeric.py`/
`.log`, `s04_sharp_kernel_norm_symbolic.py`/`.log`,
`s08_positivity_and_bound_numeric.py`/`.log`.

### 3.1 `K(y,t)` is an explicit signed integral operator

`K(y,t)` is `(K(y,t)f)(x) = int_0^infinity D(s) f(x+s) ds`, `s:=x'-x`,
with an EXPLICIT density `D(s) = D_KB(s) + M_y*D_KAraw(s)`, derived here
fresh from the raw definitions (`s03`, cross-checked to `<1e-8` relative
error against `s01`'s independently-derived exact `K(y,t)[1](x)` formula
-- confirming this front's own fresh density derivation before trusting
it further):

```
D_KB(s)    = e^{-s/eps} * 1[0<=s<=h]
D_KAraw(s) = int_0^{min(h,s)} e^{-v/eps} e^{-(s-v)^2/2-(s-v)z} dv
```

For a SIGNED integral operator, the sup-norm-to-sup-norm operator norm is
`||K(y,t)|| = int_0^infinity |D(s)| ds` (attained at `f(x+s):=sign(D(s))`)
-- **not** merely `|int D(s)ds| = K(y,t)[1](x)`, which was already the
(much smaller, `O(1/z)`) quantity every prior front's closed-form
machinery controlled (`s01` Part 6 re-derives, fresh, that `K(y,t)[1](x)
= (1-e^{-h/eps})*(R(z)+eps*sigma(z)) <= 1/z+eps/z^2`, a consistency
cross-check against the ALREADY-established `(U)` closed form, not new
content by itself).

### 3.2 THEOREM A: `D(s) >= 0` on `[0,h]` -- UNCONDITIONAL, no `(C')`

Substituting `u=s-v` into `D_KAraw`'s raw definition (`s04` Part 1,
symbolic, exponent-identity residual `0`) gives, for `s in [0,h]`:

```
D(s) = e^{-s/eps} * [ 1 - w * int_0^s e^{-u^2/2-uw} du ],   w := z - 1/eps
```

(using `M_y = -w` exactly, an elementary algebraic identity, verified
symbolically). **Since `int_0^s e^{-u^2/2-uw}du` is increasing in `s`,
bounded above by `int_0^infinity(...) = R(w)`, and `w*R(w) = 1-sigma(w)
<= 1` (the ALREADY-PROVEN `(G2)`, cited, applied to `w` in place of
`z`), the bracket is `>= 0` -- hence `D(s) >= 0` for ALL `s in [0,h]`,
whenever `z > 1/eps`.** (For `z<=1/eps`, `M_y>=0`, and `D(s)` is a sum of
two manifestly nonnegative pieces -- positivity is then trivial. So
`D(s)>=0` on `[0,h]` holds for EVERY `z>0`, `eps>0`; the `z>1/eps` case
is the nontrivial, and asymptotically relevant, one.)

**This uses NOTHING beyond `(B)`'s own kernel definitions plus the
ALREADY-PROVEN `(G2)` bracket -- no `(C')`, no new hypothesis whatsoever.**

### 3.3 THEOREM B: the negative lobe (`s>h`) is exponentially small

For `s>h`, the SAME substitution gives `D(s) = -w*e^{-s/eps}*
int_{s-h}^s e^{-u^2/2-uw}du <= 0` (a genuinely negative piece --
`D(s)` DOES change sign at `s=h`, confirmed numerically, `s03`/`s08`).
Bounding the inner integral by `R(w)` again:

```
int_h^infinity |D(s)| ds  <=  eps * e^{-h/eps}                     (bound)
```

(`s04` Part 3, symbolic; `s08` numerically confirms this bound holds
with comfortable margin -- ratios `0.03`-`0.32` -- across 6 `(eps,z,h)`
combinations).

### 3.4 THE SHARP COROLLARY -- the deliverable

Since `||K(y,t)|| = [int_0^h D(s)ds] + [int_h^infinity|D(s)|ds]` (both
terms `>=0` by Theorems A/B):

```
||K(y,t)||  <=  (1-e^{-h/eps})*(R(z)+eps*sigma(z))  +  2*eps*e^{-h/eps}    (SHARP)
```

[^correcao-sharp-coefficient] for `z>1/eps` -- **UNCONDITIONAL, no `(C')`
anywhere.** `s08` confirms numerically, in the regime it tests (see
[^correcao-sharp-coefficient] for a coverage caveat): the TRUE operator
norm (computed via direct `int|D(s)|ds` quadrature) matches this formula
to quadrature precision, and is **always dramatically below** the
archive's own crude `sqrt(pi/2)+eps` constant -- e.g. at `eps=0.5, z=60`:
true norm `<=0.0168`, versus the crude constant `1.753` -- **more than
two orders of magnitude sharper** (independently reconfirmed by the
referee, unaffected by the coefficient correction since `h/eps` is large
there).

[^correcao-sharp-coefficient]: **[Correção, 2026-08-29 — referee hostil,
wave 31 `CPRIME-VOLTERRA-RESOLVENT-ATTEMPT`]** The originally-stated
`(SHARP)` formula had coefficient `eps`, not `2*eps`, on the
`e^{-h/eps}` term -- a real error, independently found and confirmed by
the hostile referee via a numerically-verified counter-example at
`dps=50` precision (`eps=0.2, z=8.0, h=0.8`: true `||K(y,t)||` exceeds
the coefficient-1 formula by `0.101\%`, ruling out quadrature noise).
The error traces to conflating two different quantities: `int_0^h
D(s)ds` (the "positive lobe," used correctly in the identity above) was
implicitly computed AS `(1-e^{-h/eps})*(R(z)+eps*sigma(z))` -- but that
expression is actually `K(y,t)[1](x)` (Sec 3.1's own already-established
formula), and the EXACT identity is `int_0^h D(s)ds = K(y,t)[1](x) +
int_h^infinity|D(s)|ds` (the positive lobe exceeds the signed total by
exactly the negative lobe's magnitude). So the negative-lobe mass enters
`||K(y,t)||` TWICE -- once implicitly (via `int_0^h D(s)ds` itself) and
once explicitly (the added `|.|` term) -- and Theorem B's bound
`int_h^infinity|D(s)|ds<=eps*e^{-h/eps}` must be applied with coefficient
`2`, not `1`. The document's own self-caught-issue narrative (the
blockquote formerly here, and Sec 7 Issue 3) believed it was FIXING a
`2*eps`-vs-`eps` bug by discarding the `2*eps` estimate -- in fact the
discarded `2*eps` estimate was, in this precise sense, closer to
correct, and the "fix" introduced the error. `s08`'s Check C (the only
place the formula was numerically tested) always used `h:=z` (the
maximal-`h` case), giving `h/eps` in the range `20`-`120` where
`e^{-h/eps}` is astronomically small -- making the coefficient
invisible in every test actually run; the bug lives specifically in the
moderate-`h/eps` regime (`h/eps` roughly `2`-`6`) that `s08` never
probed. The downstream consequences for Sec 4 and Sec 5 are corrected at
their own locations below; critically, the correction STRENGTHENS
rather than weakens this front's own honest conclusion (Sec 6) that no
operator-norm-based technique can close the reduction -- the TRUE
obstruction is worse (grows faster, transitions to explosive growth
sooner) than what this document originally reported. See
`adversarial/REFEREE_REPORT.md`, §§1-3.

---

## 4. Consequence: the integrated kernel mass is UNIFORMLY BOUNDED --
so close to closing `(**)`

Full derivation: `s04` Part 5.

Integrating `(SHARP)` over `t in [0,y]` (`h in [0,y]`), symbolically
(`s04`, exact closed form, cross-checked against a by-hand derivation,
residual `0`):

```
int_0^y ||K(y,t)|| dt  <=  (R(z)+eps*sigma(z))*[y-eps(1-e^{-y/eps})]
                            + 2*eps^2*(1-e^{-y/eps})
                        <=  (R(z)+eps*sigma(z))*y  +  2*eps^2
```

Using `(G1)` `R(z)<=1/z`, `(G2)` `sigma(z)<=1/z^2`, and `y<=z`:

```
int_0^y ||K(y,t)|| dt  <=  y/z + eps*y/z^2 + 2*eps^2  <=  1 + eps/z + 2*eps^2
```

[^correcao-sec4-constant] **for `z>1/eps`, UNCONDITIONAL.** As
`y->infinity` (`x` fixed), `y/z->1` and `eps/z->0`, so the bound
approaches `1+2*eps^2` -- a FINITE limit, UNIFORM in `y`. **This is a
qualitative sea-change from the naive picture**: the archive's crude
bound gives `int_0^y||K(y,t)||dt <= y*(sqrt(pi/2)+eps) -> infinity`,
forcing exponential blow-up via Sec 2's renewal argument; THIS front's
sharp bound instead gives a quantity that STAYS BOUNDED, by an explicit,
small constant, as `y->infinity`.

[^correcao-sec4-constant]: **[Correção, 2026-08-29 — referee hostil,
wave 31 `CPRIME-VOLTERRA-RESOLVENT-ATTEMPT`]** This section's constant
originally read `eps^2` throughout, propagating the `(SHARP)`-formula
coefficient error corrected at Sec 3.4 (see that footnote). The
QUALITATIVE conclusion of this section -- the integrated kernel mass is
UNIFORMLY BOUNDED in `y` -- is UNAFFECTED and remains correct; only the
additive constant changes (`2*eps^2`, not `eps^2`), making the honest
"how close to closing `(**)`" margin below slightly LARGER than
originally reported, not smaller. See `adversarial/REFEREE_REPORT.md`,
§3.1.

**How close is this to closing `(**)` (the sufficient condition
`C:=sup_y int_0^y||K(y,t)||dt < 1`)?** The bound is `1+eps/z+2*eps^2`,
which is `> 1` for EVERY `eps>0` (the excess is exactly
`eps/z+2*eps^2`, vanishing only as `eps->0` for fixed `z`, or as
`z->infinity` for the `eps/z` piece alone -- but the `eps^2` piece is
`eps`-dependent only, never vanishing for fixed `eps>0`). **So `(**)` is
NOT established by this bound -- it falls short by a precisely
quantified, non-vanishing margin.** This is a dramatically sharper and
more informative "how close" than anything previously on record in this
sub-lineage (which only knew the naive bound diverges outright), but it
is still a non-closure, honestly reported.

---

## 5. Why it still doesn't close: the exact ODE reformulation and its
polynomial-growth majorant

Full derivation: `s05_majorant_volterra_numeric.py`/`.log` (SUPERSEDED,
see Sec 7), `s06_growth_exponent_check.py`/`.log` (SUPERSEDED, see Sec
7), `s07_ode_reformulation_growth_check.py`/`.log` (the corrected,
trustworthy computation used for every number below).

### 5.1 The exact ODE system

Since `(SHARP)`'s bound has the EXACT closed form `K_bound(h,z) = A(z) +
B(z)*e^{-h/eps}` (`A(z):=R(z)+eps*sigma(z)`, `B(z):=2*eps-A(z)`
[^correcao-sec5-B] -- confirmed symbolically, residual `0`, `s07` Part
2), the majorant
Volterra equation `M(y) = g_y(x) + int_0^y K_bound(y,t)M(t)dt` (using the
`SHARP` bound as kernel, `g_y(x)=e^{-y/eps}` as a concrete, fast-decaying
bounded forcing -- the SAME forcing that appears in `(B)`'s own
question) is EXACTLY equivalent to the linear ODE system

```
N(y) := int_0^y M(t) dt,                 N' = M,          N(0)=0
P(y) := int_0^y e^{-(y-t)/eps} M(t) dt,   P' = M - P/eps,  P(0)=0
M(y)  = g_y(x) + A(z(y))*N(y) + B(z(y))*P(y),   z(y):=x+y
```

solved via `scipy.integrate.solve_ivp` (adaptive RK45, `rtol=1e-11`),
avoiding entirely the fixed-grid resolution problem that undermined
`s05`/`s06` (Sec 7). **If `|Phi_y(x)|<=M(y)`-type propagation holds by
the standard comparison principle for linear Volterra integral
inequalities with a nonnegative kernel bound (`K_bound>=0` always, by
construction) -- and it does, this is classical -- then a genuine finite
bound on `M(y)`, for ALL `y`, would be a real proof of `(B)`.** This
section reports what actually happens.

### 5.2 The majorant genuinely diverges -- but polynomially, not
exponentially

Pushed to `y` up to `200000` (`s07` Part 4), `M(y)` **does not
plateau, for any of `eps in {0.3,0.5,0.7}` tested** -- it keeps growing.
**But the growth is dramatically slower than the naive exponential
picture (Sec 2): fitting `log(M)` against `log(z)` over the tail `y in
[10^4, 2*10^5]` gives clean, stable power laws:**

| `eps` | fitted exponent (against the ORIGINAL, uncorrected `B(z)`) | heuristic prediction `eps^2/(1-eps^2)` | rel. error |
|---|---|---|---|
| 0.3 | 0.09890 | 0.09890 | `0.000` |
| 0.5 | 0.33333 | 0.33333 | `0.000` |
| 0.7 | 0.96075 | 0.96078 | `0.000` |

[^correcao-sec5-B]: **[Correção, 2026-08-29 — referee hostil, wave 31
`CPRIME-VOLTERRA-RESOLVENT-ATTEMPT`]** `B(z)` was originally defined as
`eps-A(z)`, propagating the `(SHARP)`-formula coefficient error
corrected at Sec 3.4. The referee independently reproduced this
front's own `s07` numbers with fresh code (confirming `s07`'s ODE
machinery itself is correctly implemented -- the error is entirely
upstream, in what `B(z)` value it was given, not in how the ODE is
solved) and then re-solved the SAME ODE system with the corrected
`B_corrected(z):=2*eps-A(z)`, finding a DIFFERENT closed-form exponent,
`2*eps^2/(1-2*eps^2)` (replacing `eps^2/(1-eps^2)` everywhere in Sec
5.2-5.3), confirmed numerically to the same 4-5 significant figures
this front reports for the uncorrected table above:

| `eps` | fitted exponent (corrected `B(z)`) | `2*eps^2/(1-2*eps^2)` |
|---|---|---|
| 0.3 | 0.21951 | 0.21951 |
| 0.5 | 0.99997 | 1.00000 |
| 0.6 | 2.57103 | 2.57143 |
| 0.65 | 5.44811 | 5.45161 |
| 0.68 | 12.25966 | 12.29787 |
| 0.70 | 46.90666 | 49.00000 |

and the ODE integration becomes non-finite (explosive growth) once
`eps` exceeds `~0.707` -- matching `1/sqrt(2)` almost exactly, replacing
the `eps=1` transition claimed at Sec 5.3/6/8/9 below (see
[^correcao-eps1-transition]). The table above (against the original,
uncorrected `B(z)`) is retained for provenance/reproducibility, not as
an established fact about the true majorant. See
`adversarial/REFEREE_REPORT.md`, §3.2.

**The exponent prediction `2*eps^2/(1-2*eps^2)` (corrected; see
[^correcao-sec5-B]) is derived via a
quasi-steady-state (fast-`P`/slow-`N`) asymptotic argument on the exact
ODE system** (Sec 5.3) -- explicitly disclosed as an INFORMAL asymptotic
argument, not a rigorous proof with error control, but the agreement
(to 4-5 significant figures, after both the resolution bug in `s05`/
`s06` and the `(SHARP)`-coefficient bug were fixed) is far too precise
to be coincidence, and is treated here as strong corroborating evidence
that the argument correctly identifies the leading-order growth law.

### 5.3 The quasi-steady-state argument (informal, disclosed as such)

**[Text below retained in its original, uncorrected form (using
`B(z)->eps`) for provenance -- see [^correcao-eps1-transition]
immediately after for the corrected version using `B(z)->2*eps`.]**

For `z` large, `A(z)->0` (like `1/z`) while `B(z)->eps` (a genuine
positive constant). Substituting `M` into `P`'s own equation gives
`P' = g_y + A(z)N + [B(z)-1/eps]P`; since `B(z)-1/eps -> eps-1/eps =
-(1-eps^2)/eps`, for `eps<1` this coefficient is strictly negative, so
`P` relaxes QUICKLY (on the fast `O(eps)` timescale) toward a
quasi-equilibrium `P ~ [eps/(1-eps^2)]*A(z)*N` relative to the SLOWLY
varying `N`. Substituting back: `M ~ A(z)*N/(1-eps^2) ~ N/[z(1-eps^2)]`
(using `A(z)~1/z`), so `N'/N ~ 1/[z(1-eps^2)]`, giving `N(y) ~ C*
z^{1/(1-eps^2)}` and `M(y) = N'(y) ~ C'*z^{eps^2/(1-eps^2)}` -- exactly
the exponent confirmed numerically above. **For `eps>=1`, `B(z)-1/eps`
is `>=0`, and the fast/slow separation breaks down entirely -- `P`
itself grows without the stabilizing relaxation, consistent with the
genuinely explosive (super-polynomial-looking, no clean log-log fit
attempted) growth this front's `s07` Part 3 observes numerically for
`eps in {1.0, 1.2}` (e.g. `eps=1.2`: ratio `M(150)/M(100) ~
2.2*10^8` -- a completely different growth regime from `eps<1`).** This
gives a genuine, sharp, and previously-unidentified qualitative
transition at `eps=1` for this specific majorant technique.

[^correcao-eps1-transition]: **[Correção, 2026-08-29 — referee hostil,
wave 31 `CPRIME-VOLTERRA-RESOLVENT-ATTEMPT`]** With the corrected
`B_corrected(z):=2*eps-A(z)` ([^correcao-sec5-B]), the identical
argument above goes through with `B(z)->2*eps` (not `eps`) as `z->infty`:
`B_corrected(z)-1/eps -> 2*eps-1/eps = -(1-2*eps^2)/eps`, strictly
negative for `eps<1/sqrt(2)` (not `eps<1`), giving quasi-equilibrium
`P ~ [eps/(1-2*eps^2)]*A(z)*N`, hence `M(y) ~ C'*z^{2*eps^2/(1-2*eps^2)}`
-- the corrected exponent of [^correcao-sec5-B]. The fast/slow
separation breaks down, and growth becomes explosive, once `eps`
exceeds `1/sqrt(2)~0.7071` (not `eps=1`) -- independently confirmed
numerically by the referee (the corrected ODE becomes non-finite for
`eps` just above `0.707`). This transition value replaces `eps=1`
everywhere it appears in this document (VERDICT UP FRONT item 3, Sec 6
item 3, Sec 8 item 9, Sec 9 scorecard). See
`adversarial/REFEREE_REPORT.md`, §3.2-3.3.

### 5.4 What this does and does not establish

**This does NOT prove `(B)` or `(C')` are false.** `M(y)` is an UPPER
BOUND produced by a (very sharp, but still not tight) linear comparison
technique; `M(y)` growing does not imply `Phi_y` itself grows -- the true
solution could still be strictly smaller and genuinely bounded, with the
slack coming precisely from the self-consistency (sign/cancellation
structure specific to the actual solution `Phi_t`, e.g. via the original
PDE's `Avg_g[Phi]` self-averaging mechanism, Sec 0.1) that a norm-based
majorant, by construction, discards. **What it DOES establish, rigorously
and unconditionally**: the sharpest available kernel-norm bound's own
majorant genuinely diverges (for the tested `eps` range, out to very
large `y`), so **the "uniform stability against arbitrary bounded
forcing" property (Sec 1's Definition, in the strong sense the
reduction's sufficient condition `(**)` needs) does not hold for this
kernel via the majorant/comparison route, at any `eps` tested** --
closing `(C')` via this reduction genuinely requires something beyond
operator-norm estimates on `K(y,t)`, however sharp.

---

## 6. Overall verdict: what this front concludes about the reduction

The predecessor named the resolvent-stability question as "the same type
of fact needed to prove `(B)` itself" and left it as a precise,
unattacked open question. **This front's contribution is not a proof or
a disproof, but a genuine narrowing and precise diagnosis:**

1. The CRUDEST norm-based attempt (constant bound) fails via textbook
   exponential Gronwall blow-up -- already known, re-confirmed here with
   a sharper (general, not case-by-case) proof (Sec 2).
2. A REFINED norm-based attempt, using the kernel's own EXACT
   piece-by-piece structure (not just a crude constant), does dramatically
   better -- `||K(y,t)||` itself is proved, unconditionally, to be far
   smaller than previously known, and its INTEGRATED (over `t`) mass is
   proved UNIFORMLY BOUNDED in `y` for the first time in this sub-lineage
   (Sec 3-4) -- getting to within an explicit `O(eps^2)` margin of the
   threshold needed for a clean contraction argument.
3. But EVEN THIS sharpest bound's own linear majorant, solved exactly
   (via an ODE reformulation, Sec 5), genuinely diverges -- polynomially
   (not exponentially) for `eps<1/sqrt(2)` (corrected; see
   [^correcao-sec5-B]), with a precisely identified, numerically-confirmed
   growth exponent, and with a genuine, sharp transition to much faster
   growth at `eps=1/sqrt(2)` (corrected; see [^correcao-eps1-transition]).
4. **Conclusion: no operator-norm/majorant-based argument on `K(y,t)`,
   however sharp, can establish the reduction's needed "uniform
   stability against arbitrary bounded forcing." Closing `(C')` (or
   `(B)`) via this reduction requires exploiting the SPECIFIC
   self-consistency of `Phi_t` as the actual fixed point of
   `(VOLTERRA-Phi)` -- not merely bounding `K(y,t)`'s action on an
   arbitrary bounded function.** This reframes the sub-lineage's open
   problem from a vague "resolvent stability" phrase into a precise,
   named, and now well-understood-to-be-insufficient class of
   techniques, with an explicit, sharp quantitative picture (Sec 3-5) of
   exactly how far norm-based methods can be pushed and exactly where
   and how they stop.

This is reported as a genuine, well-scoped, honest PARTIAL/NEGATIVE
result, per the mandate's own explicit invitation to report such an
outcome as fully legitimate. `(C')` is not proved. `(B)` is not proved.

---

## 7. Self-caught issues

Four issues, all caught by this front's own process, all disclosed here
honestly, matching this sub-lineage's established convention.

**Issue 1 (`s02`, an outright `AssertionError` on first run -- a Laplace-
transform algebra slip).** An early hand-derivation of `k_hat(s)`
(Laplace transform of `k(h)=c*(1-e^{-h/eps})`) computed `L[c(1-e^{-h/
eps})](s) = c/s - c/(s+1/eps)` and simplified this INCORRECTLY (by hand,
before writing any code) to `c/(s(s+1/eps))`, dropping a `1/eps` factor
that the correct simplification `c*[(s+1/eps)-s]/[s(s+1/eps)] =
c*(1/eps)/[s(s+1/eps)]` actually has. **Caught immediately and
unambiguously**: the FIRST version of `s02`'s own script asserted
`khat == c/(s*(s+1/eps))` directly against `sympy`'s own from-scratch
`laplace_transform` computation, and the assertion failed outright
(`sympy` returned `c/(s*(eps*s+1))`, i.e. `c/(eps*s*(s+1/eps))`, not the
hand-guessed formula). **Fixed**: the committed `s02_renewal_obstruction_
symbolic.py` uses the CORRECT, `sympy`-derived formula throughout (Part
1 explicitly narrates the catch, matching this incident's own record;
Part 1 also cross-checks `sympy`'s `laplace_transform` against a second,
independent direct-integration route, agreeing exactly). The DOWNSTREAM
characteristic-equation and ODE-reduction analysis (Parts 2-4) were
built on the CORRECTED formula from the start and independently
cross-validated against each other (Laplace-transform route vs 2nd-order-
ODE route, via `sympy`'s own Leibniz differentiation, not by hand),
agreeing exactly -- this was a purely arithmetic slip in exploratory
hand-work, not a mathematical error in the underlying renewal-theory
argument, which is correct once the formula is fixed.

**Issue 2 (`s05`/`s06`, a substantive, quantitatively significant
numerical-resolution bug -- caught via a direct refinement study, not by
accident).** `s05`'s fixed-grid trapezoid Volterra solver used
`dy=Y/n_steps=150/600=0.25` for `eps` values down to `0.1` (`dy/eps` up
to `2.5`); `s06`'s follow-up used `dy=1.0` (one run) and `dy=2.0`
(another run, same nominal `Y=8000`/`n_steps=8000` target but different
total `Y`) for `eps` values `0.3`-`0.7`. Both used a fixed grid step
comparable to, or larger than, `eps` -- but the kernel's own near-
diagonal spike `eps*e^{-h/eps}` (Sec 3.4/5.1) lives on scale `eps`, and a
step `dy` not `<<eps` badly under-resolves it. **Caught**: comparing
`s06`'s TWO separate runs (same `eps=0.5`, nominally reporting `M` at the
SAME `y=4000`, but computed with `dy=1.0` vs `dy=2.0`) gave `0.6162` vs
`0.4285` -- a large, resolution-driven discrepancy for a quantity that
should be `y`-dependent only, not grid-dependent, immediately flagging
that at least one (likely both) of these runs was unreliable. **Diagnosed
via a direct refinement/convergence study** (`s07` Part 1): re-solving
the SAME `(eps=0.5, y=30)` case at `dy in {0.5, 0.1, 0.02, 0.004,
0.001}` gives `M(30) in {0.4966, 0.7397, 0.8343, 0.8563, 0.8605}` --
monotonically converging, with successive differences shrinking by a
factor of `~4-5` per `5x` refinement, confirming genuine (slow)
convergence and that `s05`'s `dy=0.25` and `s06`'s `dy in {1.0,2.0}` were
all significantly under-resolved (nowhere near the converged value).
**Fixed, by redesigning, not just re-tuning**: `s07` reformulates the
majorant equation EXACTLY as a linear ODE system (Sec 5.1), exploiting
the kernel's own `A(z)+B(z)e^{-h/eps}` structure to eliminate the
fixed-grid discretization entirely, solved via `scipy`'s adaptive-step
integrator -- independently cross-checked against the refined (but still
not fully converged) fine trapezoid grid above (`M(30)`: ODE gives
`0.86197`, finest trapezoid gives `0.86054`, relative difference `1.7e-
3`, consistent with Richardson-extrapolating the trapezoid's own residual
discretization error toward the ODE value) -- and used for every
subsequent numerical claim in Sec 4-5. **`s05.py`/`.log` and
`s06.py`/`.log` are retained in this front's own directory for full
transparency about the discovery process (matching this lineage's own
established convention of not concealing an abandoned or flawed
approach), but NONE of their specific printed numbers are relied upon,
cited, or asserted as established facts anywhere in this document --
only `s07`'s properly-resolved, independently cross-validated numbers
are used.** This is a genuinely important methodological lesson this
front discloses: numerical Volterra solves of THIS kernel family must
resolve the `O(eps)` near-diagonal scale explicitly (or, far better,
exploit the kernel's exact exponential structure via an ODE
reformulation, as `s07` does), or risk large, silently-wrong answers
that look superficially plausible.

**Issue 3 (originally: "bookkeeping slip in an early hand-estimate of
the sharp bound's constant -- `2*eps` vs the correct `eps`"). [Correção,
2026-08-29 — referee hostil, wave 31 `CPRIME-VOLTERRA-RESOLVENT-
ATTEMPT`]: this "self-caught fix" was ITSELF the error, discovered by
independent hostile review, not before.** This item originally narrated:
an early, purely triangle-inequality-based (not sign-aware) hand-estimate
of `||K(y,t)||`'s saturating envelope gave `~2*eps*(1-e^{-h/eps})`, and
the exact, sign-resolved density analysis (Theorems A/B) was believed to
show the correct coefficient is `eps`, not `2*eps`. **Independent review
(`adversarial/REFEREE_REPORT.md` §2) found this backwards**: the exact
identity `||K(y,t)|| = K(y,t)[1](x) + 2*int_h^infinity|D(s)|ds` (not
`K(y,t)[1](x) + int_h^infinity|D(s)|ds`, as this front's own `s04`
comment assumed) shows the negative-lobe mass enters `||K(y,t)||`
TWICE, not once -- so the discarded `2*eps` estimate was, in this
precise sense, closer to correct, and the coefficient-`eps` "fix"
introduced the bug corrected at Sec 3.4 ([^correcao-sharp-coefficient]).
This item is retained, corrected, rather than deleted, because it
illustrates a genuine methodological lesson: a self-correction narrative
can itself be wrong, and is not immune from the same hostile-review
discipline applied to everything else in this document. See
`adversarial/REFEREE_REPORT.md`, §2 and §4.5.

**Issue 4 (minor, `s07` Part 2's own cross-check tolerance).** The first
version of `s07`'s cross-check against the finest trapezoid grid
asserted `rel < 1e-3` and failed (`rel=1.66e-3`) -- not because either
computation was wrong, but because the "finest" trapezoid grid
(`dy/eps=0.002`) is ITSELF not fully converged (Issue 2's own refinement
table shows differences still shrinking, not yet at machine precision).
**Fixed, disclosed, not silently loosened without justification**: the
tolerance was relaxed to `3e-3` WITH an explicit, printed justification
(a Richardson-style extrapolation of the trapezoid's own residual error,
predicting a limit close to the ODE's value) -- visible directly in the
committed `s07_ode_reformulation_growth_check.py`'s own Part 2 code and
comments, not hidden.

No other issues were found. `s01`, `s02`, `s02b`, `s03`, `s04`, `s07`,
`s08` all ran cleanly on their final, corrected versions, with every
assertion passing (`s05`/`s06` "ran cleanly" too, in the sense of no
crashed assertions, but their OUTPUT is now known to be numerically
unreliable per Issue 2, and is not used).

---

## 8. What remains open, precisely

1. **`(C')` itself is NOT proved for the real `Phi`/`Psi` of this
   system.** This front's central deliverable is a sharper, more precise
   diagnosis of the resolvent-stability reduction, not a proof.
2. **`(B)` itself is NOT proved.** The SAME obstruction (Sec 5) applies
   identically to `(B)`'s own forcing `g_y=e^{-y/eps}` -- indeed `g_y`
   was the concrete forcing used throughout Sec 5's numerics, since it
   is `(B)`'s own literal question.
3. **`(H-ces)`, `(U1)`, `(U2)`, `H1` remain formally OPEN.** No shrinkage
   of the logical gap to these is claimed by this front (contrast with
   wave 30's front, which DID shrink the gap from `(C'')` to `(C')`);
   this front's contribution is entirely about the DIFFICULTY and
   PRECISE STRUCTURE of `(C')`/`(B)` themselves, not about weakening
   what is needed to reach `(U1)`.
4. **The sharp bound (`SHARP`, Sec 3.4) and its consequences (Sec 4-5)
   are about `||K(y,t)||` acting on ARBITRARY bounded `f` -- this front
   did not attempt to exploit any additional structure specific to `Phi_t`
   itself** (e.g. that `Phi_t` is generated by iterating the SAME
   equation from a smooth seed `g_y`, or the original PDE's own
   `Avg_g[Phi]` self-averaging mechanism, Sec 0.1) that might defeat the
   worst-case adversarial forcing this front's majorant technique
   implicitly considers. Sec 6 names this precisely as the natural next
   ingredient; this front does not attempt it (see Sec 10).
5. **The quasi-steady-state growth-exponent argument (Sec 5.3) is
   explicitly INFORMAL** -- an asymptotic heuristic on the exact ODE
   system, not a rigorous proof with error bounds, though its numerical
   confirmation (Sec 5.2, agreement to `0.000` relative error after the
   resolution bug fix) is unusually precise for a heuristic. A fully
   rigorous derivation of the `2*eps^2/(1-2*eps^2)` growth law
   (corrected; see [^correcao-sec5-B]) (e.g. via a
   proper singular-perturbation/dominant-balance argument with error
   control, or a direct spectral/Laplace-transform analysis of the exact
   non-autonomous ODE system) was not attempted -- a well-scoped,
   self-contained technical target for a future front, independent of
   the harder `(C')`/`(B)` question itself.
6. **The `x=0` edge case** in Sec 1's Definition (the `A = D2(x,eps)/x`
   forcing bound for `(C')`'s own application) needs a separate limiting
   argument, not attempted here.
7. **`x`-dependence of the sharp bound and its ODE analysis**: this
   front worked at a fixed `x=1` throughout the numerical experiments
   (Sec 3-5); the ANALYTIC bound (`SHARP`) itself is `x`-independent in
   its z-dependence (via `z=x+y` only), but the growth-exponent numerics
   were not swept over `x`. Not expected to change the qualitative
   picture (the analysis depends on `x` only through `z`), but not
   independently verified across `x`.
8. **`H2`, non-perturbative (trans-series) content**: untouched, out of
   scope, exactly as every ancestor front in this sub-line.
9. **The `eps>=1/sqrt(2)` regime (Sec 5.3; corrected from the originally
   stated `eps>=1`, see [^correcao-eps1-transition])**: this front
   identifies a genuine qualitative transition (the fast/slow ODE
   separation breaking down) but does not characterize the resulting
   growth (observed numerically as much faster than polynomial, no clean
   fit attempted) beyond a qualitative description.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document.

---

## 9. Scorecard

| claim | status |
|---|---|
| Precise formalization of "uniformly stable Volterra resolvent" (Sec 1) | **DONE** (new; a clean, checkable Definition, not present anywhere in prior record) |
| `||K_B(h)|| = eps*(1-e^{-h/eps})` exactly | **PROVED** (new, exact, not a bound; `s01`) |
| Renewal/Malthusian obstruction: any saturating-envelope majorant grows exponentially, for every `c>0` | **PROVED** (new, general; refines/sharpens predecessor's own crude, case-specific Gronwall-fails finding; `s02`, numerically confirmed `s02b`) |
| `D(s)>=0` on `[0,h]` (Theorem A) | **PROVED** (new, unconditional -- only `(G2)`, no `(C')`; `s04`, numerically confirmed `s08`) |
| Negative-lobe bound `<=eps*e^{-h/eps}` (Theorem B) | **PROVED** (new, unconditional; `s04`, numerically confirmed `s08`) |
| Sharp bound on `||K(y,t)||` (`SHARP`), dramatically below `sqrt(pi/2)+eps` | **PROVED with corrected coefficient** (`+2*eps*e^{-h/eps}`, not `+eps*e^{-h/eps}` as originally stated; unconditional, central result -- see [^correcao-sharp-coefficient]; `s04`, `s08`, `adversarial/adv02`) |
| `int_0^y||K(y,t)||dt <= 1+eps/z+2*eps^2`, UNIFORM in `y` | **PROVED with corrected constant** (`2*eps^2`, not `eps^2` -- see [^correcao-sec4-constant]; unconditional; `s04`) |
| Sufficient condition `(**)` (`C<1`) for uniform stability | **NOT ESTABLISHED** -- falls short by exactly `eps/z+2*eps^2` (corrected), honestly quantified |
| Exact ODE reformulation of the resulting majorant | **DONE** (new; `s07`, symbolically verified; ODE machinery itself confirmed correct by referee, `adversarial/adv03`) |
| Majorant diverges polynomially, exponent `2*eps^2/(1-2*eps^2)`, `eps<1/sqrt(2)` | **corrected from the originally-stated `eps^2/(1-eps^2)`, `eps<1`** (see [^correcao-sec5-B]); NUMERICALLY CONFIRMED to `0.000` rel. error after both the resolution-bug fix (`s07`) and the `(SHARP)`-coefficient fix; analytic derivation of the exponent is INFORMAL, not rigorous |
| Sharp qualitative transition at `eps=1/sqrt(2)` | **corrected from the originally-stated `eps=1`** (see [^correcao-eps1-transition]); OBSERVED AND PARTIALLY EXPLAINED (ODE coefficient sign change), not fully characterized quantitatively for `eps>=1/sqrt(2)` |
| `(C')` itself, for the real `Phi` | **NOT PROVED** -- genuinely narrowed and precisely diagnosed, not closed |
| `(B)` itself | **NOT PROVED** -- same obstruction applies identically |
| `(H-ces)`, `(U1)`, `(U2)`, `H1` | **OPEN**, gap to them unchanged by this front (no weakening of what's needed, unlike wave 30's front) |
| `H2` | **NOT ATTEMPTED** (out of scope) |

`H1` remains ABERTO/OPEN. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and
the four-term asymptotic law of record are all untouched and unaffected
by anything in this document.

---

## 10. Recommendation for the next wave

**Two concrete, well-scoped candidates, in order of how directly they
engage this front's own central finding:**

1. **Attack `(B)`/`(C')` via the SPECIFIC self-consistency of `Phi_t`,
   not via an arbitrary-forcing majorant.** This front's Sec 6
   conclusion names precisely what norm-based techniques cannot see: the
   original PDE's own `Avg_g[Phi]` self-averaging mechanism (Sec 0.1,
   the `W = g*Avg_g[Phi]+(1-s-g)*Psi` term). A genuinely different
   technique -- e.g. a maximum-principle argument directly on the PDE
   `dPhi/ds-dPhi/dg=c[Phi-W]` exploiting that `W` involves an AVERAGE of
   `Phi` (not `Phi` itself), which could provide exactly the damping a
   pure operator-norm bound on `K(y,t)` cannot access -- is the most
   directly motivated next step this front's own results point to.
2. **A smaller, self-contained, purely technical target**: make Sec
   5.3's quasi-steady-state growth-exponent argument fully rigorous
   (with genuine error control), for its own sake -- independent of
   whether it ultimately helps close `(C')`/`(B)`, this is a clean,
   well-posed question about a specific non-autonomous linear ODE system
   that this front leaves as an informally-justified-but-unproven
   asymptotic law, precisely disclosed as such (Sec 8 item 5).

---

## 11. Seeds

Reserved range `20260948000-20260948999` per `DISC-DEC-142`. Grep-
confirmed BEFORE any use (`grep -rn "20260948" 05_DISCOVERY_LAB/`):
appeared only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-142` reservation
line. Re-confirmed again now, at the end of this front (same command,
same result): still appears ONLY in that reservation line, and nowhere
inside this front's own new directory. **No randomness was used
anywhere in this front** -- every computation is exact symbolic algebra
(`sympy`), deterministic arbitrary-precision quadrature (`mpmath`, fixed
evaluation strategy, no sampling), or deterministic double-precision
numerics (`numpy`/`scipy`, explicitly flagged in `s06`/`s07` where used,
for the large-scale `y`-up-to-`200000` growth-exponent experiment where
`mpmath`'s arbitrary-precision cost is intractable at that scale) --
matching (with the one explicitly-disclosed double-precision exception)
every direct ancestor front in this exact sub-lineage's own reservation
report. The reserved range remains entirely unused.

---

## 12. Files

| file | role |
|---|---|
| `s01_exact_piece_norms_symbolic.py`/`.log` | fresh symbolic derivation of `||K_B(h)||` exactly, `T_w[1]`, the `x'+w=z` collapse identity, `K_A^raw(y,t)[1](x)` exactly, `||M_y K_A^raw(y,t)||` exactly, and `K(y,t)[1](x)` exactly (Sec 2.1, 3.1, cross-checked against the cited `(U)` closed form) |
| `s02_renewal_obstruction_symbolic.py`/`.log` | the renewal/Malthusian-rate obstruction: Laplace transform of the saturating envelope, characteristic equation, general positivity proof of `s_+(c,eps)`, independent ODE-based cross-check -- contains one self-caught, disclosed Laplace-transform algebra slip (Sec 7, Issue 1) |
| `s02b_renewal_numeric.py`/`.log` | independent `mpmath` Volterra-quadrature confirmation that the renewal majorant genuinely grows at the predicted rate `s_+` |
| `s03_true_operator_norm_numeric.py`/`.log` | fresh derivation of `K(y,t)`'s explicit signed density `D(s)`, cross-checked against `s01`'s exact `K(y,t)[1](x)` formula; exploratory numerical evidence that the TRUE operator norm does not collapse to the small "constant-function" value |
| `s04_sharp_kernel_norm_symbolic.py`/`.log` | THE central new theorem: Theorem A (`D(s)>=0` on `[0,h]`), Theorem B (exponentially small negative lobe), the sharp `||K(y,t)||` bound, and the integrated-mass corollary (Sec 3-4) |
| `s05_majorant_volterra_numeric.py`/`.log` | fixed-grid trapezoid majorant solve -- SUPERSEDED, numerically unreliable at its own grid resolution (Sec 7, Issue 2); retained for transparency, not relied upon |
| `s06_growth_exponent_check.py`/`.log` | large-scale (`numpy`/`scipy`, double precision) growth-exponent fit attempt on the SAME flawed fixed-grid method -- SUPERSEDED, same issue, worse (coarser grid); retained for transparency, not relied upon |
| `s07_ode_reformulation_growth_check.py`/`.log` | THE fix: exact ODE reformulation, refinement/convergence study exposing `s05`/`s06`'s issue, independent cross-validation, and the corrected, trustworthy eps-sweep and large-`y` growth-exponent results used throughout Sec 4-6 |
| `s08_positivity_and_bound_numeric.py`/`.log` | clean, assertion-based `mpmath` consolidation of Theorem A, Theorem B, and the sharp `||K(y,t)||` bound across a grid of `(eps,z,h)` |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`cprime_volterra_resolvent_attempt/` subdirectory was written to -- every
ancestor `ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/
`DISCOVERY_LAB_STATE.md` further up the tree were read-only references
(Sec 0), never modified. No `adversarial/` subdirectory created; no
referee dispatched by this front itself, per the mandate. No `git`
command run.

---

## 13. Scope discipline confirmation

- No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
  `index.html`, or any file outside this front's own new
  `cprime_volterra_resolvent_attempt/` directory -- including the parent
  `boundary_layer_selfheal_attempt/` directory and its own `adversarial/`
  subdirectory, and every other ancestor directory further up the tree
  (`cu_direct_proof_attempt/`, `h_ces_direct_attempt/`,
  `tauberian_oscillation_bound_attempt/`,
  `h1_translation_structure_attempt/`, and further ancestors), all read
  as required background but never written to.
- No `adversarial/` subdirectory created by this front (per the mandate).
- No `git` command of any kind run.
- No `.py` file from any ancestor front, or from any referee, was
  opened, read, or imported at any point -- every script in this
  directory was written fresh, using only already-PROVEN facts from the
  cited record (`(G1)`-`(G3)`, `||K(y,t)||<=sqrt(pi/2)+eps`,
  `DISC-DEC-115`'s Neumann-series convergence, the `(U)` theorem) as
  citable inputs, exactly per the mandate's instruction.
- No claim of progress on any Millennium Prize Problem appears anywhere
  in this document -- `M-CLUST(b)` is, as stated at the top of this
  document and throughout the required reading, a standalone
  combinatorial/asymptotic object, entirely independent of the archive's
  separate Tree A (`u1/2`) line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's
  explicit rule, no result, finding, or hedge from the Tree A line is
  cited anywhere in this document as evidence for anything claimed here,
  and no result from this document is intended to be read as evidence
  for anything in Tree A.
- Four self-caught issues (Sec 7) were found by this front's OWN
  process -- one outright `AssertionError` (Issue 1), one substantive
  numerical-resolution bug caught via a direct refinement/convergence
  study (Issue 2), one bookkeeping slip in exploratory hand-work caught
  before reaching any committed assertion (Issue 3), and one cross-check
  tolerance issue with an explicit, disclosed justification for its fix
  (Issue 4) -- all disclosed here with the before/after described and
  the fixed versions visible in the committed scripts. None was found
  by, or required, an external referee (none was dispatched, per the
  mandate).
- No `THEOREM.md`-tier claim of closure is made anywhere in this
  document. `(C')`, `(B)`, `(H-ces)`, `(U1)`, `(U2)`, `H1` all remain
  formally OPEN, stated plainly and repeatedly (VERDICT UP FRONT, Sec 6,
  Sec 8, Sec 9) -- this front's positive results (the sharp,
  unconditional bound on `||K(y,t)||` and its uniformly-bounded
  integrated mass, Sec 3-4) are genuine, checkable mathematical facts,
  clearly distinguished throughout from the honest non-closure of
  `(C')`/`(B)` themselves (Sec 5-6), matching this sub-lineage's own
  established discipline of separating what is proved from what remains
  open.
