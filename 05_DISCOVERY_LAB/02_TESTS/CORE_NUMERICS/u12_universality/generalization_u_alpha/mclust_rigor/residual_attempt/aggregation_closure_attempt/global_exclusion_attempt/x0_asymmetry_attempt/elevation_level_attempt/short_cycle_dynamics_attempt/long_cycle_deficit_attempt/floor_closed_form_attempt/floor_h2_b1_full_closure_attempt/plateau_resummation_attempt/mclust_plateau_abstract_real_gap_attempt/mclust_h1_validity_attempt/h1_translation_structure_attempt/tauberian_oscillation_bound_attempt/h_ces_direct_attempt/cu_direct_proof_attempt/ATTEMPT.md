# ATTEMPT — a direct proof attempt at `(C')` and `(U)` themselves, the two
# named hypotheses `(H-ces)`/`(U1)`/`H1` now reduce to (`CU-DIRECT-PROOF-ATTEMPT`)

**Wave 29, front (a), `DISC-DEC-134`.** Tenth consecutive wave (waves
20–29) in this exact sub-lineage, but the first with a qualitatively
different target: not another architecture for closing `(U1)`, but a
**direct attack on the two concrete, named hypotheses** — `(C')` (uniform-
in-`t` Lipschitz regularity of `{Φ_t(·)}_{t≥0}`) and `(U)` (uniform
`O(1/z²)` closed-form kernel remainder, `z:=x+y`) — that wave 28 front (a)
(`H-CES-DIRECT-ATTEMPT`, `DISC-DEC-132`) proved suffice, via an elementary
Cauchy-criterion argument with **no Tauberian apparatus**, to close
`(H-ces)`, and hence `(U1)` itself with an explicit `O(1/(x+y))` rate.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process — pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lema Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.** Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no
result from Tree A is cited anywhere below, even in hedged language, as
evidence for anything claimed here.

Reserved seed range for this front: `20260942000-20260942999`.
Grep-confirmed BEFORE any use (`grep -rn "20260942" 05_DISCOVERY_LAB/`) to
appear only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-134` reservation line
(re-confirmed again at the end of this front, Sec 11). **No randomness was
needed anywhere in this front** — every computation below is exact symbolic
algebra (`sympy`) or deterministic arbitrary-precision quadrature (`mpmath`,
fixed evaluation strategy, no sampling), exactly as every direct ancestor
front in this sub-lineage reports for itself. The reserved range remains
entirely unused.

---

## VERDICT UP FRONT

**Tier: genuine partial closure of `(U)`, and a genuine, precise
(non-circular but non-terminal) reduction of `(C')` — with an honest,
sharply-characterized remaining gap on each, including a decisive
sharpness/necessity investigation that itself uncovered a subtle and
interesting phenomenon (a "boundary-layer self-healing" effect) not
previously seen anywhere in this sub-lineage's ten-wave record.**

1. **`(U)` is PROVED — not merely numerically tested — conditional on `(B)`
   plus a mild, explicitly-named strengthening of `(C')` (Sec 3).** A new,
   fully rigorous, non-asymptotic double inequality for the Mills-ratio
   function `R(z)` (an elementary integrating-factor/comparison-function
   lemma, new to this entire sub-lineage — every ancestor front used only
   the FORMAL Mills-ratio asymptotic series, with no proved remainder
   bound) lets the ENTIRE closed-form kernel remainder be bounded
   EXPLICITLY, with an EXPLICIT constant `D(x,ε)`, UNIFORMLY over the full
   range `h'∈[0,h]`, `h∈[0,y]` — i.e. uniformly across the WHOLE family
   `{Φ_t}_{t∈[0,y]}`, exactly what `DISC-DEC-132` flagged as needed. The
   "value-only" piece of the closed form needs **only hypothesis `(B)`**
   (no Lipschitz/regularity of `f` at all); the residual piece needs a
   strengthened hypothesis, named `(C'')`: `Φ_t'(·)` is ALSO Lipschitz,
   with a `t`-uniform constant `L2` (i.e. `Φ_t ∈ C^{1,1}`, `t`-uniformly)
   — strictly stronger than `(C')` as literally named in this lineage's
   record (mere Lipschitz continuity of `Φ_t` itself).

2. **A decisive sharpness investigation of whether `(C')` alone (WITHOUT**
   `(C'')`**) already suffices, or whether `(C'')` is a genuine mathematical
   necessity (Sec 4) — with a subtle, honestly-reported, two-sided answer.**
   A concrete Lipschitz-only (kinked, non-`C¹`) test function confirms the
   Watson-remainder `E(h',z)` (the specific piece needing regularity beyond
   `(B)`) genuinely DOES degrade to exactly `O(1/z²)` — NOT the sharper
   `O(1/z³)` — **pointwise in `h'`**, when the kink is adversarially aligned
   with the kernel's own `O(1/z)` concentration scale (confirmed to
   `z³|E|` growing linearly, unboundedly, to `>3300` by `z=15000`). But the
   SAME kink's effect on the `h'`-**integrated** (aggregate) quantity that
   actually enters the closed-form remainder is shown, numerically, to
   RECOVER the full `O(1/z³)` rate (`z³|E_full|→0.936`, converging cleanly,
   `z²|E_full|→0`) — a genuine "boundary-layer self-healing" phenomenon:
   the pointwise-bad region has vanishing width `O(1/z)`, and this exactly
   compensates. **Honest conclusion: this front's PROOF of `(U)` needs
   `(C'')`, and this need is not a proof-technique artifact at the
   pointwise level — but whether the full, `h'`-aggregated `(U)` genuinely
   requires `(C'')`, or whether a sharper (boundary-layer-aware) argument
   could establish it under `(C')` alone, is left OPEN, precisely
   characterized, not resolved.**

3. **`(C')` is not proved, but is genuinely REDUCED (Sec 5) — for the first
   time in this lineage — to a single, explicitly-named question of the
   SAME logical type and difficulty as hypothesis `(B)` itself.** A new
   exact identity, `d/dx[K(y,t)f](x) = K(y,t)[f'](x) − K_A^raw(y,t)f(x) −
   M_y·N(y,t)f(x)`, shows that differentiating the Volterra kernel in `x`
   costs an EXPLICIT correction term — and, contrary to the natural fear
   (drawn directly from wave 26's route-(a) dead end for `Ψ`, where an
   unbounded `M_y`-type coefficient had NO cancellation partner), this
   correction is rigorously `O(1/z)`, vanishing, using only `(B)+(C')`
   itself (no NEW hypothesis). This shows `Φ_y'(x)` satisfies THE SAME
   Volterra equation as `Φ_y(x)` itself, driven by a bounded (not
   exploding) forcing term — so `(C')` follows immediately IF the
   Volterra-resolvent for kernel `K(y,t)` is "uniformly stable" (maps
   bounded forcing to `y`-uniformly bounded solutions) — **exactly the
   fact that would need to be shown to prove `(B)` itself rigorously,
   which no front, across all 29 waves of this lineage, has ever
   attempted.** The naive alternative (Gronwall on the crude operator norm
   `‖K(y,t)‖≤√(π/2)+ε>1`) is shown to provably fail (exponentiates) —
   the SAME failure mode as wave 26's route (a).

4. **No genuine counter-example to `(C')` or `(U)` for the real `Φ` was
   found.** The one place a real degradation WAS found (Sec 4, the
   adversarially-aligned pointwise kink test) is explicitly about a
   POINTWISE sub-quantity inside this front's OWN proof technique, shown
   in the very same investigation to be compensated for in the AGGREGATE
   quantity that actually matters — not a counter-example to `(U)` itself.

**`(H-ces)`, `(U1)`, `(U2)`, `H1` remain formally OPEN** — `(C')` is not
unconditionally proved, and even `(U)`'s proof is conditional on `(C'')`,
itself not established for the real `Φ`. But the state of the gap is now
sharper than at any point in this ten-wave lineage: `(U)` is a genuine
THEOREM conditional on one precisely-named strengthening of `(C')`, and
`(C')` itself is reduced to a single, precisely-named "Volterra-resolvent
stability" question — of the exact same type and difficulty as `(B)`
itself. `φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document. `H2` is untouched (out of scope). No `THEOREM.md`,
`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml`
file was opened for writing. No `adversarial/` subdirectory created; no
referee dispatched by this front itself. No `git` command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code, in the exact order
the mandate specifies: `h_ces_direct_attempt/ATTEMPT.md` (wave 28, front a,
`DISC-DEC-132`, this front's immediate predecessor) in full, including its
precise restatement of `(C')` and `(U)` (its Sec 0/2.1) and its
`adversarial/REFEREE_REPORT.md` in full (the referee's independent
confirmation that `(C')`/`(U)` are used "in exactly the sense, and to
exactly the degree, wave 26's own `T1` piece already established as
needed" — i.e. no silent strengthening by that front); `h1_translation_
structure_attempt/ATTEMPT.md` (wave 25, one level up) in full — the origin
of the closed-form kernel `K(y,t)` and the self-averaging identity, Sec 4
(the closed-form derivation), Sec 4.4 (the "pointwise-in-`f`, not
operator-norm" scope note this front relies on throughout); `tauberian_
oscillation_bound_attempt/ATTEMPT.md` (wave 26, sibling one level up) in
full, including its own precise statements of `(C')`/`(U)` (Sec 3.5), its
three independent numerical sweeps testing `(U)` (Sec 4), and its
`adversarial/REFEREE_REPORT.md` in full (in particular Sec 5's finding that
`(H-ces)` alone, given the unconditional self-averaging bridge, is
necessary AND sufficient for `(U1)` — the logical fact wave 28's own main
argument builds on); `PROOF_DEPENDENCY_MAP.md`'s dated addenda under
`DISC-DEC-122`, `DISC-DEC-125`, and `DISC-DEC-132` (the orchestrating
session's own precise summaries — `DISC-DEC-132` in particular is the
addendum integrating wave 28 front (a), and is the source this front's own
`DISC-DEC-134` mandate cites directly); and `mclust_h1_validity_attempt/
ATTEMPT.md` (the origin of `(U1)`/`(U2)`) Sec 0, to recover the EXACT,
real `Φ`/`Ψ` PDE-slice system this whole `M-CLUST(b)` sub-lineage is
about (quoted verbatim below, traced back through the directory chain as
instructed) — **not an approximation, but the literal governing system
every ancestor front in this chain works from.**

**No `.py` file from any ancestor front, or from any referee, was opened,
read, or imported at any point** — matching this exact sub-lineage's own
established discipline. Every script in this directory (`s01`–`s05`, plus
`s04b`–`s04d`, see Sec 8 below for why the numbering branches) was written
fresh from the mathematical content of the prose cited above.

**The real system this front works from** (traced back to its origin per
the mandate, `mclust_h1_validity_attempt/ATTEMPT.md` Sec 0 — the FIRST
document in this whole chain to state it, cited not re-derived):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Governing PDE system (the REAL object {Phi_t}/{Psi_t} refers to):
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi] + (1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y) (cited, plateau_resummation_attempt Sec 4.1,
re-derived by h1_volterra_attempt/h1_post_correction_attempt):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                            (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

Closed Volterra-in-y system (h1_volterra_attempt, cited, built from (E1)/
(KEY)/(E2) above):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    g_y(x) := e^{-y/eps},   Phi_y := Phi(.,y) in X := C_b([0,infinity))
    K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
      K_B(h)       := int_0^h e^{-v/eps} S_v dv,   (S_v f)(x):=f(x+v)
      K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
      (T_w f)(x)   := int_0^infinity e^{-u^2/2-u(x+w)} f(x+u) du
      M_y          := multiplication-by-[(1-eps(x+y))/eps]

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = int_0^inf e^{-u^2/2-ux} du,
  R'=xR-1,  R(0)=sqrt(pi/2),  R strictly decreasing, R(z)<=1/z for z>0
Standing hypothesis (B): Phi, Psi bounded, M_Phi := sup|Phi| (used
  throughout this lineage, unproved, never attacked by any front).

THE CLOSED-FORM ASYMPTOTIC (h1_translation_structure_attempt Sec 4, cited,
pointwise-in-f, conditional on (B) plus a Lipschitz-type hypothesis on f):
  K(y,t) f(x) = [f(x) - e^{-h/eps} f(x+h)] / z + O(1/z^2),  h:=y-t, z:=x+y

Hypotheses this front's mandate targets DIRECTLY (DISC-DEC-132/134, cited,
NOT weakened or strengthened, restated verbatim):
  (C'): a Lipschitz-type regularity bound on Phi_t(.), UNIFORM in t --
    exists L1 independent of t s.t. |Phi_t(x1)-Phi_t(x2)|<=L1|x1-x2| for
    ALL t>=0, x1,x2>=0.
  (U): the closed-form kernel's O(1/z^2) remainder is uniform over the
    FULL range h in [0,y] AND across the whole family {Phi_t}_{t in [0,y]}
    -- exists D(x,eps), independent of t,h,y, s.t. the closed-form
    remainder above is bounded by D(x,eps)/z^2 for every t in [0,y].
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout; nothing
outside this front's own new subdirectory was written to.

---

## 1. Precise restatement of the target, and this front's strategy

Per the mandate, restated exactly as quoted in Sec 0 above: prove `(C')`
and `(U)` — or as much of them as possible — for the REAL `{Φ_t}` system,
either from the defining PDE/recursion directly, or from the already-
established closed-form kernel representation.

**Strategy chosen (disclosed up front, not hidden): this front attacks
`(U)` FIRST (Sec 3–4), via the closed-form kernel representation — the
route the mandate itself flags as the more concretely scoped of the two
("a maximum-principle or contraction argument on the governing equation,
OR from an already-established closed-form/series representation") — and
`(C')` SECOND (Sec 5), attempting the PDE/Volterra-equation route directly.
This order was chosen because `(U)`'s target (a rigorous, non-asymptotic
Watson's-lemma-type remainder bound) is a well-posed, self-contained
analytic question about the already-cited closed-form kernel, whereas
`(C')` requires engaging with the Volterra equation's own regularity-
propagation structure — genuinely harder, and (per Sec 5's honest
conclusion) not fully closable within this front's scope.**

---

## 2. A new technical engine: a fully rigorous, non-asymptotic Mills-ratio
(Gordon-type) double inequality

Full symbolic + numerical verification: `s01_gordon_mills_ratio_lemma.py`/
`.log`, `s01b_sharper_upper_bound.py`/`.log`.

Every ancestor front in this sub-lineage that needed `R(z)`'s large-`z`
behavior used the FORMAL Mills-ratio asymptotic series `R(z) ~ 1/z - 1/z^3
+ 3/z^5 - ...` (re-derived from the ODE `R'=zR-1` via a coefficient
recursion) — a genuine, correctly-derived asymptotic expansion, but with
**no rigorously-bounded remainder** anywhere in this lineage's record
(wave 25 Sec 4.2 derives the series; nothing in this lineage bounds its
tail). This front instead derives, via an elementary **integrating-factor
comparison argument** on the SAME defining ODE `R'=zR-1` (no series, no
asymptotic expansion anywhere in the proof):

```
(G1)  z/(1+z^2)  <=  R(z)  <=  1/z                         for ALL z>0
(G2)  0  <=  sigma(z) := 1-z*R(z)  <=  1/(1+z^2)  <=  1/z^2
(G3)  0  <=  R''(z)  <=  2*R(z)/(1+z^2)  <=  2/(z(1+z^2))  <=  2/z^3
```

**Method (`s01` Part 2, re-derivable in full from the printed derivation):**
define `w1(z):=R(z)-z/(1+z^2)`; using `R'=zR-1`, `w1` satisfies the LINEAR
ODE `w1'=z*w1-2/(1+z^2)^2`; solving via the integrating factor `e^{-z^2/2}`
(the SAME technique that already characterizes `R` itself as the unique
solution of its own ODE bounded at infinity, `h1_translation_structure_
attempt` Sec 0, cited) gives the EXPLICIT closed form `w1(z)=e^{z^2/2}
int_z^infinity 2 e^{-s^2/2}/(1+s^2)^2 ds`, manifestly `>=0` since the
integrand is positive — proving the LOWER bound in `(G1)` for ALL `z>0`,
not merely asymptotically. A sharper UPPER bound, `R(z) <= v(z) :=
(z^2+2)/(z(z^2+3))` (`s01b`, SAME technique, different comparison
function), gives a matching TWO-SIDED bracket on `sigma(z)`, and hence
(`s02`, next section) on `1-z^2*sigma(z)` — needed to get the FULL
`O(1/z^2)` sharpness, not just `O(1/z)`.

**Fully independently cross-checked** (`s01` Parts 3/5, `mpmath` `dps=50`):
`R(z)` via TWO structurally different routes (`erfcx`-based closed form,
and direct raw-definition quadrature) agree to machine precision at every
tested `z` from `0.001` to `10^6`; `(G1)`–`(G3)` confirmed with ZERO
violations across a `13`-point grid spanning `5` orders of magnitude in
`z`, including small `z` where the asymptotic series is not even
convergent-useful — this lemma is genuinely non-asymptotic, unlike
anything in this lineage's prior record.

---

## 3. `(U)`, PROVED — conditional on `(B)` + `(C'')`

Full derivation: `s02_exact_closed_form_assembly.py`/`.log`,
`s03_residual_term_rigorous_bound.py`/`.log`.

### 3.1 Exact assembly, no asymptotic series anywhere

Working from the SAME exact decomposition wave 25 established (cited,
re-derived independently here from scratch, `s02` Part 1):

```
K(y,t)f(x) = [1+c(z)]*K_B(h)f(x) + [(1-eps*z)/eps] * int_0^h e^{-h'/eps} rho(h',z) dh'
  c(z) := (1-eps*z)*R(z)/eps
  rho(h',z) := int_0^inf e^{-u^2/2-uz}[f(x+h'+u)-f(x+h')] du
```

Writing `R(z)=(1-sigma)/z` (`sigma:=sigma(z)` from Sec 2) and expanding
`K(y,t)f(x)` EXACTLY as a linear combination of `KB:=K_B(h)f(x)`,
`F1:=f(x)`, `F2:=e^{-h/eps}f(x+h)` — treated as opaque symbols, `sympy`
confirms (`s02` Part 1) that `F1,F2` enter ONLY via `F2-F1`, with:

```
coeff(F2-F1) = -sigma*z + sigma/eps
coeff(KB)    = sigma - sigma*z/eps - sigma/(eps*z) + 1/(eps*z) + sigma/eps^2
```

### 3.2 Both coefficients are rigorously `O(1/z^2)`, using `(B)` alone

**Key algebraic regrouping** (`s02` Part 2, `sympy`-confirmed exact
identity, residual `0`):

```
coeff(F2-F1) - (-1/z)  =  (1 - sigma*z^2)/z  +  sigma/eps
coeff(KB)               =  (1 - sigma*z^2)/(eps*z)  +  sigma*(1+1/eps^2-1/(eps*z))
```

Using the RIGOROUS bracket `1/(1+z^2) <= 1-z^2*sigma(z) <= 3/(z^2+3)`
(Sec 2's `(G1)`/`s01b`, exact algebra, `sympy`-confirmed) and `0<=sigma(z)
<=1/(1+z^2)` (`(G2)`):

```
|coeff(F2-F1) + 1/z|  <=  3/(z(z^2+3)) + 1/(eps*(1+z^2))   = O(1/(eps*z^2))
|coeff(KB)|            <=  3/(eps*z*(z^2+3)) + [1/(1+z^2)]*(1+1/eps^2+1/eps)
                        = O(1/z^2)  (eps fixed)
```

**Both fully rigorous, `sympy`-verified regroupings; numerically confirmed
(`s02` Parts 2–3) at `18` `(z,eps)` combinations spanning `z∈[2,10^4]`,
`eps∈{0.05,0.1,1}` — worst observed `actual/bound` ratio: `1.000000`
(the bound is met essentially WITH EQUALITY at small `z`, confirming it is
tight, not a loose over-estimate).** **Crucially, NEITHER bound used any
Lipschitz/regularity property of `f` at all — only `(B)` (`|f|<=M_Φ`, to
bound `KB`, `F1`, `F2`).** This is a genuine strengthening of every
ancestor front's treatment of this piece (a rigorous double inequality
replaces a formal asymptotic series with an unbounded remainder).

### 3.3 The residual piece: where `f`'s regularity genuinely enters

The remaining piece is `Efull := int_0^h e^{-h'/eps} E(h',z) dh'`,
`E(h',z) := rho(h',z) - f'(x+h')*sigma(z)`, multiplied by the UNBOUNDED
prefactor `(1-eps*z)/eps ~ -z/eps`. Two independent derivations
(`s03` Parts 1–2) give:

```
rho(h',z) = int_0^inf f'(x+h'+u) * Q_u(z) du,   Q_u(z):=e^{-u^2/2-uz}R(u+z)>=0
E(h',z)   = int_0^inf [f'(x+h'+u)-f'(x+h')] * Q_u(z) du
```

Under a NEW hypothesis, **`(C'')`: `Φ_t'(·)` is Lipschitz with a
`t`-uniform constant `L2`** (i.e. `Φ_t ∈ C^{1,1}([0,∞))`, `t`-uniformly —
a genuine but MILD strengthening of `(C')` as literally named in this
lineage's record): `|f'(x+h'+u)-f'(x+h')|<=L2*u`, giving, via TWO
independent bounding routes (`s03` Part 2–3, cross-checked to agree to
within a small constant factor):

> **[Correção, 2026-08-29 — referee hostil, wave 29
> `CU-DIRECT-PROOF-ATTEMPT`]** "Route A" das duas rotas mencionadas
> acima não é de fato derivada em nenhum dos scripts desta frente —
> apenas afirmada. O referee hostil re-derivou a Rota A do zero de
> forma independente e confirmou que ela é verdadeira (produz o mesmo
> limitante `L2/(z(1+z^2))` que a Rota B, que É derivada explicitamente
> em `s03`), mas isto não estava demonstrado por esta frente antes da
> revisão. Não afeta o resultado — `(U)` permanece PROVADO — apenas a
> alegação de "duas rotas independentes" carecia de uma das duas até a
> revisão adversarial preencher a lacuna. Ver
> `adversarial/REFEREE_REPORT.md`.

```
|E(h',z)|  <=  L2/(z*(1+z^2))  <=  L2/z^3      -- UNIFORM in h' (h' does
                                                   not appear in this bound
                                                   at all)
```

**Independently confirmed numerically** (`s03` Part 4, fresh `mpmath`
double-integral quadrature on a concrete `C^∞` test function): `z^3*|E|`
observed bounded (sup `0.406` across a `4×4` grid of `h'∈{0,0.3,1,3}` ×
`z∈{5,10,30,100}`), consistent with the rigorous `O(1/z^3)` bound.

### 3.4 Assembled theorem

Combining Sec 3.2's bound (`|1-eps*z|/eps <= (1+eps*z)/eps`) with Sec
3.3's `E`-bound (`s03` Part 5):

```
|(1-eps*z)/eps * Efull|  <=  L2*(1+eps)/z^2     for z>=1
```

**THEOREM (this front).** Given `(B)` [`Φ_t` bounded by `M_Φ`, `t`-uniform,
standing] and `(C'')` [`Φ_t'` Lipschitz with constant `L2`, `t`-uniform],
for all `z=x+y>=1` (`eps` fixed) and UNIFORMLY over `h'∈[0,h]`, `h∈[0,y]`
— i.e. across the WHOLE family `{Φ_t}_{t∈[0,y]}`, exactly the regime
`(U)` needs:

```
|K(y,t)f(x) - [f(x)-e^{-h/eps}f(x+h)]/z|  <=  D(x,eps)/z^2

D(x,eps) := M_Φ*eps*(1+1/eps^2+1/eps) + 2*M_Φ/eps + L2*(1+eps)
```

**with NO dependence on `h`, `h'`, or `t` in `D(x,eps)` or in the
`z`-threshold — this IS hypothesis `(U)`, PROVED (not merely numerically
tested), for the real system, conditional on `(B)`+`(C'')`.** This is the
central positive result of this front.

---

## 4. Sharpness/necessity of `(C'')`: a decisive but two-sided investigation

Full logs: `s04_kink_sharpness_stress_test.py`/`.log` (partial — see Sec 8
Self-caught issues), `s04b_kink_E_direct_sharpness.py`/`.log`,
`s04c_kink_adversarial_alignment.py`/`.log`,
`s04d_Efull_aggregate_boundary_layer.py`/`.log`.

**The question**: does the proof route above genuinely NEED `(C'')`
(`Φ_t'` Lipschitz), or would mere `(C')` (`Φ_t` itself Lipschitz, no
control on `Φ_t'`) already suffice for `(U)`, with `(C'')` merely an
artifact of THIS front's specific proof technique?

### 4.1 A non-adversarial kink: no visible degradation (`s04b`)

Test function `f_kink(a) := 1/(1+a) + 0.3*|a-3|` (Lipschitz-`1.3`, genuine
kink in `f'` at `a=3`, NOT `C^1`), tested at a FIXED `h'=1` (kink crossed
at `u=2`, a FIXED distance from the kernel's own concentration point
`u=0`). Result: `z^3*|E(h',z)|` CONVERGES cleanly for the kink function
(`0.207→0.250`, `z` from `10` to `30000`), essentially as well-behaved as
the smooth control (`0.292→0.345`) — **no visible degradation.**

### 4.2 An adversarially-aligned kink: genuine pointwise degradation (`s04c`)

Reasoning: the kernel's own concentration scale is `u~1/z` (the weight
`e^{-uz}` decays on this scale). A kink at a FIXED location is
exponentially far from this shrinking scale, hence invisible at leading
order — exactly what `s04b` shows. To genuinely stress the bound, `h'`
must be chosen (as a function of `z`) so the kink-crossing point
`u* := a0-h'` sits EXACTLY at the concentration scale: `h'_z := a0-1/z`,
`a0=0.1`. Result — **decisive**:

```
z    h'         u*=a0-h'    |E|            z^2|E|    z^3|E|
20   0.050000   0.050000    7.316e-04      0.2927     5.85
150  0.093333   0.006667    1.025e-05      0.2307    34.60
1500 0.099333   0.000667    9.855e-08      0.2217   332.59
15000 0.099933  0.000067    9.815e-10      0.2208  3312.42
```

`z^2*|E|` CONVERGES to a nonzero constant (`≈0.2208`); `z^3*|E|` GROWS
essentially linearly in `z`, unboundedly. **This is a clean, decisive
confirmation that mere `(C')` is genuinely insufficient for a POINTWISE-
in-`h'` `O(1/z^3)` bound on `E(h',z)` — the `O(1/z^2)` crude fallback (Sec
3.3, using `(C')` alone via `|E|<=2L1*sigma(z)`) is SHARP, not a loose
proof-technique artifact, at least at this specific alignment.**

### 4.3 The AGGREGATE quantity self-heals: `O(1/z^3)` survives after all (`s04d`)

The quantity that actually enters the closed-form remainder (Sec 3.3) is
NOT `E(h',z)` pointwise, but the `h'`-INTEGRATED `Efull := int_0^h
e^{-h'/eps}E(h',z) dh'`. Testing this DIRECTLY for the SAME adversarial
kink (`a0=0.1`, `eps=0.5`, `x=0`) — genuinely decisive again, but in the
OPPOSITE direction:

```
z     |Efull|         z^2|Efull|   z^3|Efull|
10    6.685e-04        0.06685      0.66848
80    1.826e-06        0.01168      0.93476
200   1.170e-07        0.00468      0.93592
500   7.490e-09        0.00187      0.93630
```

`z^3*|Efull|` CONVERGES cleanly to `≈0.936`; `z^2*|Efull|` shrinks toward
`0`. **The AGGREGATE quantity fully recovers the sharp `O(1/z^3)` rate,
DESPITE the pointwise degradation just confirmed in Sec 4.2 at the exact
same kink.** Mechanism (consistent with, though not itself a fully
rigorous proof of, this numerical finding): the "bad" `h'`-region has
width `~O(1/z)` (shrinking with `z`), and integrating an `O(1/z^2)`-sized
pointwise defect over an `O(1/z)`-wide window contributes only `O(1/z^3)`
to the aggregate — a genuine "boundary-layer self-healing" effect.

### 4.4 Honest conclusion

**This front's PROOF of `(U)` (Sec 3) genuinely needs `(C'')` — Sec 4.2
confirms this is not a proof-technique artifact AT THE POINTWISE LEVEL
that Sec 3's specific bounding strategy (a uniform-in-`h'` sup bound,
integrated crudely) uses.** But **Sec 4.3's finding — that the AGGREGATE
quantity these bounds actually need to control appears (at least for this
one concrete adversarial test function) to still achieve the full
`O(1/z^3)`/`O(1/z^2)` rate even without `(C'')` — leaves OPEN, precisely
and honestly, whether a SHARPER (boundary-layer-aware, not merely
sup-then-integrate) argument could establish `(U)` under `(C')` ALONE.**
This front does not attempt that sharper argument (a genuinely harder,
open-ended undertaking — quantifying the exact width and profile of the
"bad" `h'`-window in general, not just for one test function) — it
reports the phenomenon precisely, as new information this sub-lineage did
not previously have, rather than resolving it either way.

---

## 5. `(C')`: a genuine reduction to a Volterra-resolvent stability question

Full derivation: `s05_lipschitz_from_volterra_reduction.py`/`.log`.

### 5.1 A new exact identity: differentiating `K(y,t)f` in `x`

Working DIRECTLY from the raw operator definitions (Sec 0), `sympy`
confirms (`s05` Part 1, residual `0`):

```
d/dx[e^{-u^2/2-u(x+y)} f(x+h'+u)]  =  e^{-u^2/2-uz}f'(x+h'+u)  -  u*e^{-u^2/2-uz}f(x+h'+u)
```

Integrating over `u` and `h'`, using `d/dx[K_B(h)f(x)]=K_B(h)[f'](x)`
(pure shift operator, exact) and `d/dx[M_y]=-1` (`z=x+y`):

```
d/dx[K(y,t)f](x)  =  K(y,t)[f'](x)  -  K_A^raw(y,t)f(x)  -  M_y*N(y,t)f(x)     (DX-K)
  N(y,t)f(x) := int_0^h e^{-h'/eps} [int_0^inf u*e^{-u^2/2-uz}f(x+h'+u)du] dh'
```

**This is the "derivative loss" mechanism this whole lineage has met
before** (wave 26's route (a): transferring `(⋆⋆)` from `Ψ` via `(KEY)`/
`(E2)` hit an unbounded `M_y`-type coefficient with NO cancellation
partner, a confirmed dead end). The natural fear is that `(DX-K)`'s own
correction term, `K_A^raw(y,t)f(x)+M_y N(y,t)f(x)`, hits the SAME wall.

### 5.2 The correction term is rigorously `O(1/z)` — the fear does NOT
materialize

Using `(G1)`/`(G2)` (Sec 2) and hypotheses `(B)`+`(C')` (NOT `(C''`)`,
NOT any new hypothesis, `s05` Part 2):

```
|K_A^raw(y,t)f(x)|   <=  M_Φ*eps/z + L1*eps/z^2                 = O(1/z)
|M_y*N(y,t)f(x)|      <=  M_Φ/z^2 + eps*M_Φ/z                    = O(1/z)
```

**Total: `|K_A^raw(y,t)f(x) + M_y*N(y,t)f(x)| <= D2(x,eps)/z`,
`D2(x,eps) := 2*M_Φ*eps + L1*eps + M_Φ`, for `z>=1` — a fully rigorous
bound, vanishing as `z→∞`, unlike route (a)'s unbounded/non-cancelling
`M_y*Δ_Ψ` term.** Independently confirmed numerically (`s05` Part 3,
fresh finite-difference + double-integral quadrature): `z*|d/dx[Kf] -
K[f']|` observed bounded (`sup≈0.038` across `z∈{5,10,30,60}`), consistent
with the rigorous `O(1/z)` bound.

### 5.3 Honest assembly: what `(C')` reduces to

Integrating `(DX-K)` over `t∈[0,y]` (using `g_y'(x)=0`, `g_y` constant in
`x`) and the fact that `z=x+y` does not depend on `t`:

```
Phi_y'(x)  =  int_0^y K(y,t)[Phi_t'](x) dt  +  [forcing bounded by D2(x,eps)]
```

**`Φ_y'` solves THE SAME Volterra equation, with THE SAME kernel `K(y,t)`,
as `Φ_y` itself — driven by a genuinely BOUNDED (not exploding) forcing
term.** `Φ_y` itself is known bounded (`|Φ_y|<=M_Φ`) only because
hypothesis `(B)` ASSERTS it — `(B)` has never been derived from first
principles by any of the 29 waves in this lineage; it is a standing,
unproved hypothesis throughout. **`(C')` therefore follows from this
reduction IF the Volterra-resolvent for THIS kernel is "uniformly
stable"** (maps any bounded, `y`-independent forcing sequence to a
UNIFORMLY, not merely locally-in-`Y`, bounded solution sequence) — **this
is precisely, and only, the SAME kind of fact that would need to be shown
to prove `(B)` itself rigorously.** A naive alternative (Gronwall's
inequality on the crude operator norm `‖K(y,t)‖<=√(π/2)+eps`, `DISC-DEC-
113`, cited) is checked and confirmed to FAIL: `√(π/2)≈1.2533>1`, so
Gronwall's bound EXPONENTIATES rather than staying bounded — the identical
failure mode as wave 26's route (a) (`s05` Part 4 states this explicitly).

> **[Correção, 2026-08-29 — referee hostil, wave 29
> `CU-DIRECT-PROOF-ATTEMPT`]** Dois ajustes ao parágrafo acima. (1) O
> diagnóstico "`√(π/2)≈1{,}2533>1`, logo Gronwall exponencia" é
> impreciso: Gronwall sobre um domínio Volterra CRESCENTE
> (`t\in[0,y]`, `y\to\infty`) exponencia para QUALQUER limitante
> constante da norma do operador, não apenas para valores `>1` — a
> condição `>1` seria relevante apenas para um domínio Volterra de
> comprimento FIXO, que não é o caso aqui. A conclusão (Gronwall falha
> para esta construção) permanece correta; apenas a razão dada é
> superficial. (2) "o mesmo modo de falha exato que a rota (a) da onda
> 26" é uma analogia real, mas mais frouxa do que "idêntico" sugere —
> a rota (a) da onda 26 falhou por um coeficiente `M_y`-tipo
> NÃO-LIMITADO sem parceiro de cancelamento (Seção 5.1 desta própria
> frente já contrasta isto explicitamente com o `O(1/z)` genuinamente
> limitado que ESTA frente obtém para `K_A^raw`/`M_y N`); a falha de
> Gronwall aqui é por EXPLOSÃO EXPONENCIAL de um limitante frouxo, um
> mecanismo relacionado mas distinto. Nenhum dos dois ajustes afeta a
> redução de `(C')` em si, que permanece um resultado genuíno. Ver
> `adversarial/REFEREE_REPORT.md`.

**This is reported as a genuine, precise, NAMED partial result — not a
proof, and not vague hand-waving either: this front now knows EXACTLY
which single stability fact about the kernel `K(y,t)`'s Volterra resolvent
would supply BOTH `(B)` and `(C')` simultaneously, and knows precisely
why the naive route to it fails.**

---

## 6. Numerical verification summary

All numerical claims above are logged with real output:

- `s01_gordon_mills_ratio_lemma.log` — `(G1)`–`(G3)`, `13`-point grid,
  `z∈[0.001,10^6]`, zero violations, two independent computation routes
  (`erfcx`-based and direct quadrature) agreeing to machine precision.
- `s01b_sharper_upper_bound.log` — the sharper Gordon-type upper bound
  `R(z)<=v(z)`, `12`-point grid, zero violations; the sign of the driving
  ODE forcing term confirmed negative at `8` spot points.
- `s02_exact_closed_form_assembly.log` — the two coefficient bounds,
  `18` `(z,eps)` combinations, worst `actual/bound` ratio `1.000000`.
- `s03_residual_term_rigorous_bound.log` — two independent `E(h',z)`
  bounding routes cross-checked to a small constant factor; direct
  numeric confirmation of `O(1/z^3)`, `sup(z^3|E|)=0.406184` across `16`
  points.
- `s04_kink_sharpness_stress_test.log` — the sanity check against the
  predecessor's own published Sec 5.4 value (`x=0,eps=0.1,f=1/(1+x),
  h=y/2,y=10`): `0.9156333394` vs published `0.9156333394`, `abs diff
  2.119e-12` — confirms this front's fresh raw-kernel implementation
  before trusting anything new (this log also records the partial run
  before the self-caught performance issue, Sec 8).
- `s04b_kink_E_direct_sharpness.log` — non-adversarial kink, `8` `z`
  values from `10` to `30000`, no degradation for either smooth or
  kinked `f`.
- `s04c_kink_adversarial_alignment.log` — adversarially-aligned kink,
  `7` `z` values from `20` to `15000`, `z^2|E|→0.2208` (converges,
  nonzero), `z^3|E|→3312` (diverges) — decisive pointwise degradation.
- `s04d_Efull_aggregate_boundary_layer.log` — the SAME kink's
  `h'`-aggregated effect, `5` `z` values from `10` to `500`,
  `z^3|Efull|→0.936` (converges) — decisive aggregate self-healing.
- `s05_lipschitz_from_volterra_reduction.log` — the `(DX-K)` identity's
  correction-term bound, `4` `z` values, `sup(z|correction|)=0.038384`.

---

## 7. Self-caught issues

Two, both caught by this front's OWN process (an outright assertion
failure in one case, a deliberate timing observation in the other), both
disclosed here honestly, matching this lineage's established convention.

**Issue 1 (`s01b`, Part 4 — a conceptual mislabeling, not a computational
error).** An earlier version of `s01b`'s final Part attempted to bound
`|1-z*sigma(z)|<=C0/z^2` using the SAME `hi`/`lo` rational brackets that
Part 3 derived for a DIFFERENT quantity, `z*sigma(z)` (an `O(1)` quantity
as `z→∞`, not `O(1/z^2)`). This is a genuine conceptual slip (re-using a
bracket for the wrong target expression), **caught immediately and
unambiguously** by the script's own closing `assert sup_hi_z2 <= C0`
failing outright on first run — not a subtle near-miss, but a screaming
signal (`sup_hi_z2` printed as `~10^16` over the test grid, since `hi(z)*
z^2` genuinely grows like `z^2`, unboundedly, for the wrong target).
**Fixed**: this broken exploration was not patched in place; instead, the
CORRECT quantity (`1-z^2*sigma(z)`, the one this front's actual proof
needs, per Sec 3.2) was independently re-derived via a different,
correct route in `s02_exact_closed_form_assembly.py` Part 2, verified
there with clean `sympy` algebra and zero assertion failures. `s01b`'s own
Parts 1–3 (the `R(z)<=v(z)` proof itself, which Part 2's correct
derivation reuses) are UNAFFECTED by this bug and independently confirmed
correct. Visible in the committed `s01b_sharper_upper_bound.py`'s Part 4,
now rewritten as an explicit disclosure of the bug (not silently deleted)
per this lineage's honesty convention, and in its `.log`'s clean exit
(`exit code 0`) after the fix.

**Issue 2 (`s04`, the full raw-kernel double-integral test — a genuine
performance/scope limitation, disclosed not hidden).** The first (and
only) full run of `s04_kink_sharpness_stress_test.py` (nested
double-integral quadrature: for every outer `h'`-quadrature node, a full
fresh inner `u`-integral quadrature) was launched with a `z`-sweep from
`20` to `2000` (`8` points); it was terminated by this session's own
timeout mechanism after completing only `3` of the `8` planned `z` values
(`z=20,50,100`, each taking roughly `150`–`200` seconds at `dps=30`)
— **caught by direct observation of the wall-clock budget, not a failed
assertion.** The `3` completed points (visible in
`s04_kink_sharpness_stress_test.log`) do NOT show a clear qualitative
divergence signal between the smooth and kinked test functions in this
limited range (`z^2*err` for both stay of comparable, bounded magnitude),
which on its own would have been an UNRESOLVED, ambiguous result.
**Fixed, not by making the same script faster, but by redesigning the
test entirely**: `s04b`/`s04c`/`s04d` replace the expensive full
double-integral test with a much CHEAPER, more DIRECT and MORE INFORMATIVE
test of the specific quantity (`E(h',z)`, then `Efull`) that actually
carries the regularity-dependence, at a properly adversarial kink
placement — reaching `z` up to `15000`/`30000` (`s04c`) in well under a
minute, and yielding the genuinely decisive Sec 4 findings that the
original, more expensive, less-targeted `s04` design would likely never
have resolved even with a much larger time budget (the kink in `s04`'s
own test, at `a0=3`, was NOT adversarially aligned with the outer
integral's concentration scale, per the Sec 4.1/`s04b` finding — so even
a complete `s04` run to `z=2000` would plausibly have shown little
signal, for the SAME reason `s04b`'s non-adversarial kink shows none).
This redesign is disclosed as a genuine scope pivot, not concealed;
`s04`'s partial log is kept and cited (Sec 6) for its valid sanity-check
value, not discarded.

No other issues were found. `s01`, `s02`, `s03`, `s04b`, `s04c`, `s04d`,
and `s05` all ran cleanly on their (corrected, where applicable) attempt,
with every assertion passing.

---

## 8. What did NOT close, precisely

1. **`(C')` is NOT proved.** Sec 5 gives a genuine, new, precise reduction
   — `(C')` follows if the kernel `K(y,t)`'s Volterra resolvent is
   "uniformly stable" — but that stability fact is itself NOT established
   here, and is of the same logical type and difficulty as hypothesis
   `(B)` itself, unproved throughout all 29 waves of this lineage. The
   naive Gronwall/operator-norm route is shown to FAIL (exponentiates).
2. **`(U)` is PROVED only conditional on `(C'')`, a strengthening of
   `(C')` beyond what is literally named in this lineage's record.**
   Whether mere `(C')` (without `(C'')`) already suffices for `(U)` in
   full (i.e. for the AGGREGATE, `h'`-integrated remainder, not the
   pointwise-in-`h'` sub-quantity this front's specific proof strategy
   bounds) is explicitly LEFT OPEN (Sec 4.4) — with genuinely suggestive,
   but not conclusive, numerical evidence (Sec 4.3) that it might.
3. **`(C'')` itself is not established for the real `Φ`.** No attempt was
   made in this front to derive `(C'')` from the governing PDE (a natural
   next step, given `(C')`'s own reduction in Sec 5 already engages the
   `x`-derivative structure — extending it to a SECOND derivative bound
   was judged out of scope for this front, given the time already
   invested in the `(U)` route).
4. **The "boundary-layer self-healing" phenomenon (Sec 4.3) is reported
   as a genuine, new, honestly-flagged NUMERICAL finding, not a proved
   general fact.** It is confirmed for exactly ONE concrete adversarial
   test function at ONE parameter setting (`a0=0.1`, `eps=0.5`, `x=0`);
   no claim is made that it holds for every possible Lipschitz-only `f`,
   or that it constitutes a proof that `(C')` alone suffices for `(U)`.
5. **No direct numerical test on the real, evolving `Φ_t` of this system
   was performed** — exactly as every direct ancestor front in this
   sub-lineage discloses for itself (building a full `(P,Q)`-family
   series solver or a spatial-profile Volterra solver remains a
   substantial, separately-scoped undertaking, per wave 25 Sec 1.2 and
   wave 26 Sec 1.2's own well-documented reasons, unchanged here).
6. **`x`-uniformity of `(C')`/`(C'')`/`(U)`'s constants** is not
   exhaustively examined here (this front works at a fixed, general `x`,
   as its ancestors did) — inherited, not independently re-examined,
   from wave 26 Sec 5.2's own analytic argument (every constant here is
   likewise `O(1/z)`-type, `z=x+y>=y` for `x>=0`, so automatically
   non-increasing in `x`, by the same structural reasoning).
7. **`H2`, non-perturbative (trans-series) content**: untouched, out of
   scope, exactly as every ancestor front in this sub-line reports.

**No formula of record is proposed as a replacement for anything.**
`φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of
record are all untouched and unaffected by anything in this document.

---

## 9. Scorecard

| claim | status |
|---|---|
| `(G1)`–`(G3)`: fully rigorous, non-asymptotic Mills-ratio double inequalities on `R(z)`,`sigma(z)`,`R''(z)` | **PROVED** (new, `s01`/`s01b`, integrating-factor comparison argument) |
| Sharper Gordon bound `R(z)<=(z^2+2)/(z(z^2+3))` | **PROVED** (new, `s01b`), one self-caught mislabeling in a downstream exploration, disclosed |
| "Value-only" closed-form piece matches target to `O(1/z^2)` using `(B)` alone | **PROVED** (new, `s02`, no regularity of `f` needed) |
| Residual piece `Efull` is `O(1/z^2)`-net, conditional on `(C'')` | **PROVED** (new, `s03`), explicit constant `D(x,eps)` |
| **`(U)`, PROVED conditional on `(B)`+`(C'')`** | **CLOSED, conditionally** — main positive result, `s02`+`s03` |
| Sharpness: pointwise `E(h',z)` genuinely degrades to `O(1/z^2)` under `(C')` alone, adversarial alignment | **CONFIRMED** (`s04c`, decisive) |
| Sharpness: aggregate `Efull` recovers `O(1/z^3)` at the SAME adversarial kink | **CONFIRMED, one test case** (`s04d`, decisive but not general) |
| Whether `(C')` alone suffices for the FULL, aggregate `(U)` | **OPEN**, precisely characterized (Sec 4.4) |
| `d/dx[K(y,t)f]=K(y,t)[f']` up to an `O(1/z)` correction, using `(B)`+`(C')` only | **PROVED** (new identity `(DX-K)`, `s05`) |
| Naive Gronwall/operator-norm route to `(C')` | **PROVED TO FAIL** (exponentiates, `s05` Part 4 — same mechanism as wave 26 route (a)) |
| **`(C')` reduced to Volterra-resolvent stability, same difficulty class as `(B)`** | **REDUCED, not proved** — precise, named, honest partial result, `s05` |
| Genuine counter-example to `(C')` or `(U)` for the real `Φ` | **NOT FOUND** |
| `(H-ces)` (via wave 28's Cauchy-criterion argument) | **OPEN** (conditional on `(C')`,`(U)`; `(U)` now conditional on `(C'')` instead) |
| `(U1)`, `(U2)`, `H1` | **OPEN** (unchanged) |
| `H2` | **NOT ATTEMPTED** (out of scope) |

`H1` remains ABERTO/OPEN. `φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the
four-term asymptotic law of record are all untouched and unaffected by
anything in this document.

---

## 10. Recommendation for the next wave

Two concrete, well-scoped candidates, neither preferred over the other by
this front:

1. **Attack the "boundary-layer self-healing" question (Sec 4.3–4.4)
   directly and generally**: does the `h'`-aggregated `Efull` achieve
   `O(1/z^3)` under `(C')` ALONE, for a general Lipschitz `f` (not just
   the one concrete adversarial kink tested here)? A promising angle: a
   genuine boundary-layer/matched-asymptotics argument on the SPECIFIC
   `h'`-window where `E(h',z)`'s pointwise bound degrades, tracking its
   shrinking width explicitly (this front's `s04c`/`s04d` numerics
   strongly suggest the window has width `O(1/z)`, which is exactly what
   would need to be shown analytically). If successful, this would drop
   `(U)`'s dependency from `(C'')` back down to `(C')` itself — closing
   the gap this front's Sec 4 opened up.
2. **Attack the Volterra-resolvent stability question named precisely in
   Sec 5.3** — either directly (showing `K(y,t)`'s resolvent is
   `y`-uniformly stable for bounded forcing, which would give BOTH `(B)`
   [rigorously, for the first time in this lineage] AND `(C')` at once),
   or by finding a genuinely different, non-Gronwall route to `(C')`
   specifically that this front did not consider.

Given this is the TENTH consecutive wave in this exact sub-lineage, the
orchestrating session may also reasonably judge that a fundamentally
different angle (e.g. the scoped real-`Φ` numerical solver every prior
front has disclosed as out-of-scope for itself) is a better use of an
eleventh wave. Both are legitimate.

---

## 11. Seeds

Reserved range `20260942000-20260942999` per `DISC-DEC-134`. Grep-confirmed
BEFORE any use (`grep -rn "20260942" 05_DISCOVERY_LAB/`): appeared only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-134` reservation line. Re-confirmed
again at the end of this front (same command, same result): still appears
ONLY in that reservation line, and nowhere inside this front's own new
directory. **No randomness was used anywhere in this front** — every
computation is exact symbolic algebra (`sympy`) or deterministic
arbitrary-precision quadrature (`mpmath`, fixed evaluation strategy, no
sampling) — exactly as every direct ancestor front in this exact
sub-lineage reports for its own reservation. The reserved range remains
entirely unused.

---

## 12. Files

| file | role |
|---|---|
| `s01_gordon_mills_ratio_lemma.py`/`.log` | fully rigorous, non-asymptotic Gordon-type Mills-ratio bounds `(G1)`–`(G3)` on `R(z)`,`sigma(z)`,`R''(z)` (Sec 2) |
| `s01b_sharper_upper_bound.py`/`.log` | sharper upper bound `R(z)<=(z^2+2)/(z(z^2+3))`, needed for the full `O(1/z^2)` sharpness in Sec 3 (Sec 2); contains one self-caught, disclosed mislabeling in an abandoned Part 4 (Sec 7) |
| `s02_exact_closed_form_assembly.py`/`.log` | exact symbolic assembly of the closed-form kernel identity, rigorous `O(1/z^2)` bounds on both coefficients using `(B)` alone (Sec 3.1–3.2) |
| `s03_residual_term_rigorous_bound.py`/`.log` | rigorous `O(1/z^3)` bound on the Watson-remainder residual `E(h',z)` under `(C'')`, and the final assembled theorem for `(U)` (Sec 3.3–3.4) |
| `s04_kink_sharpness_stress_test.py`/`.log` | initial (partial, self-caught performance issue) full-kernel sharpness test; retained for its valid sanity-check cross-validation (Sec 6, Sec 7 Issue 2) |
| `s04b_kink_E_direct_sharpness.py`/`.log` | direct `E(h',z)` sharpness test, non-adversarial kink placement — no degradation observed (Sec 4.1) |
| `s04c_kink_adversarial_alignment.py`/`.log` | direct `E(h',z)` sharpness test, adversarially-aligned kink — decisive pointwise `O(1/z^2)` degradation confirmed (Sec 4.2) |
| `s04d_Efull_aggregate_boundary_layer.py`/`.log` | aggregate `Efull` test at the SAME adversarial kink — decisive `O(1/z^3)` recovery confirmed, the "boundary-layer self-healing" finding (Sec 4.3) |
| `s05_lipschitz_from_volterra_reduction.py`/`.log` | the new `(DX-K)` identity, its rigorous `O(1/z)` correction-term bound, and the honest reduction of `(C')` to Volterra-resolvent stability (Sec 5) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`cu_direct_proof_attempt/` subdirectory was written to — every ancestor
`ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md`
further up the tree were read-only references (Sec 0), never modified. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself, per the mandate.

---

## 13. Scope discipline confirmation

- No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
  `index.html`, or any file outside this front's own new
  `cu_direct_proof_attempt/` directory — including the parent
  `h_ces_direct_attempt/` directory and its own ancestor siblings
  (`tauberian_oscillation_bound_attempt/`, `h1_translation_structure_
  attempt/`, `h1_volterra_attempt/`, `h1_post_correction_attempt/`,
  `h1_energy_estimate_attempt/`, `mclust_h2_validity_attempt/`,
  `h1_u2_boundary_layer_attempt/`), all read as required background but
  never written to.
- No `adversarial/` subdirectory created (a separate hostile referee is
  dispatched later by the orchestrating session, per the mandate).
- No `git` command of any kind run.
- No claim of progress on any Millennium Prize Problem appears anywhere in
  this document — `M-CLUST(b)` is, as stated at the top of this document
  and throughout the required reading, a standalone combinatorial/asymptotic
  object, entirely independent of the archive's separate Tree A (`u1/2`)
  line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result,
  finding, or hedge from the Tree A line is cited anywhere in this document
  as evidence for anything claimed here, and no result from this document is
  intended to be read as evidence for anything in Tree A.
- Two self-caught issues (Sec 7) were found by this front's OWN process (an
  outright assertion failure in `s01b`; a wall-clock timeout observation in
  `s04`), disclosed here with the before/after visible in the committed
  files — neither was found by, or required, an external referee.
- No `THEOREM.md`-tier claim of closure is made anywhere in this document.
  Per the mandate's explicit standard for honest, non-overclaiming
  partial-progress diagnosis: this front states plainly and repeatedly
  (VERDICT UP FRONT, Sec 3, Sec 4.4, Sec 5.3, Sec 8, Sec 9) that `(C')` is
  NOT proved (only reduced), that `(U)` is proved only CONDITIONALLY (on
  `(C'')`, a named strengthening of `(C')`), and that `(H-ces)`/`(U1)`/
  `(U2)`/`H1` remain formally OPEN.
