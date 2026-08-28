# ATTEMPT -- Volterra-in-y reformulation of the exact renewal identity (E2)
# (`MCLUST-H1-VOLTERRA-ATTEMPT`)

**Wave 23, front (c), `DISC-DEC-110`.** Target: `(U1)` and `(U2)`, the two
precisely-stated sub-hypotheses `mclust_h1_validity_attempt` (`DISC-DEC-088/
091`) reduced `H1` to. The immediate predecessor, `h1_energy_estimate_attempt`
(`DISC-DEC-096/100`), attacked `(U1)`/`(U2)` via a maximum-principle/energy-
estimate argument and a contraction-mapping argument on the exact renewal
identity `(E2)`; it obtained real partial results (a new exact renewal
identity for `Psi`, a new GLOBAL oscillation bound) but did **not** close
`(U1)`/`(U2)`, and diagnosed precisely why the contraction route fails
(Lipschitz constant `<=1`, not `<1` -- the kernel `R(z)~1/z` only MATCHES,
not beats, the linear-in-`y` growth of the source). That front's own
closing paragraph named, as "the most promising avenue, entirely
unexplored", a **Volterra-in-`y` reformulation of `(E2)`** -- a genuinely
different idea from the sup-norm/single-order contraction map already
tried. **This front attacks exactly that avenue.**

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process -- pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lemma Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

Reserved seed range for this front: `20260925000-20260925999`
(`numpy.SeedSequence` base) -- grep-confirmed (`grep -rn "20260925"
05_DISCOVERY_LAB/`) to appear ONLY in `DECISION_LEDGER.yaml`'s own
`DISC-DEC-110` reservation line and in `DISCOVERY_LAB_STATE.md`'s summary
of that same reservation, before any use by this front. **In the end no
randomness was needed anywhere in this front** -- exactly as in every
direct ancestor: every result below is either exact symbolic reasoning
(`sympy`), deterministic arbitrary-precision computation (`mpmath`, `dps`
between 40 and 280 depending on the sub-computation), or deterministic
grid-based numerical quadrature (`numpy`, float64) -- so the reserved range
remains entirely unused. See Sec 8 (Seeds).

---

> **CORREÇÃO (2026-08-28, sessão orquestradora, pós-adversarial,
> `DISC-DEC-113`).** O referee hostil desta frente
> (`adversarial/REFEREE_REPORT.md`, achado H1, ALTA severidade,
> independentemente reconfirmado pela sessão orquestradora) encontrou
> um erro real na Seção 4.4 abaixo: a alegação de que a limitação do
> núcleo completo "depende inteiramente" do operador de multiplicação
> não-limitado `M_y`, e que isto "é o conteúdo real da obstrução",
> **não se sustenta**. A Seção 4.4 nunca limita o operador COMPOSTO
> `M_y \circ K_A^{\mathrm{raw}}(y,t)` que de fato aparece no núcleo —
> apenas o `M_y` isolado. Explorando um cancelamento exato que a
> própria álgebra da Seção 4.1 produz mas nunca usa
> (`x'+w=x+y`, independente de `w`), o referee derivou o limitante mais
> afiado `\|M_y K_A^{\mathrm{raw}}(y,t)\|\le h_\varepsilon(x+y)`,
> `h_\varepsilon(z):=|1-\varepsilon z|R(z)`, e mostrou por computação
> direta (duas rotas independentes) que `h_\varepsilon` é
> **globalmente limitado** por `\sqrt{\pi/2}` (atingido em `z=0`),
> **não crescendo** em `y` — o oposto exato da Seção 4.4 abaixo. O
> núcleo completo `K(y,t)` é, portanto, limitado por
> `\sqrt{\pi/2}+\varepsilon` **uniformemente**, incluindo no domínio
> `x` irrestrito, contradizendo as duas linhas "REFUTED" da Seção 10 e
> o item 3 abaixo. **Isto NÃO afeta o veredito geral de não-fechamento
> de `H1`/`(U1)`/`(U2)`** (permanecem ABERTOS) nem as Seções 2, 3, 5-6
> (álgebra, estrutura de Volterra, numérica nova) — apenas invalida o
> mecanismo de diagnóstico específico alegado como a contribuição
> central da Parte C. A sessão orquestradora reconfirmou
> independentemente o achado do referee (verificação numérica direta
> de `h_\varepsilon(z)` e de `\sup_{z\ge y}h_\varepsilon(z)` versus
> `y`, antes de aceitar a correção). Ver correções pontuais nas Seções
> 4.4, 4.6 e 10 abaixo.

## VERDICT UP FRONT

**Tier: honest non-closure of `(U1)`/`(U2)`, with (a) a genuinely new,
derivative-free closed-form algebraic identity for `W` that resolves the
"derivative-loss" obstruction the predecessor front explicitly flagged as
blocking a rigorous Volterra treatment; (b) a precise, rigorously-derived
operator-norm diagnosis of EXACTLY why the classical Volterra
quasi-nilpotency theorem does not apply unconditionally to the closed
system, pinpointing the identical underlying mechanism the predecessor
front found via a completely different route (contraction-mapping); and
(c) new, independently-verified numerical evidence -- going beyond the
predecessor's single-order Lipschitz analysis -- that the actual (not
linearized) Neumann/Picard series for the closed Volterra-in-y system DOES
converge at every finite `y` tested, with an explicitly measured two-regime
structure (a "warm-up" phase, then genuine super-geometric/factorial-type
decay) whose warm-up length grows with `y`, roughly linearly, at every `c`
tested.**

1. **A new algebraic identity, resolving the derivative-loss obstruction**
   (Sec 2): substituting the required reading's own exact `(E1)`
   (`Psi_x=(x+y)Psi-I`) into `(KEY)` (`W=Psi-eps*Psi_x`) gives, by pure
   algebra (no differentiation of any integral representation needed):
   ```
   W(x,y) = (1 - eps*(x+y)) * Psi(x,y) + eps * I(x,y)                 (NEW-W)
   ```
   Verified symbolically (`sympy`, exact, Sec 2.2) and numerically, at 4
   `(s,g)` points, against a STRUCTURALLY INDEPENDENT computation of
   `Psi_x` (direct term-by-term differentiation of the `b_k(s)` series, NOT
   using `(E1)`): agreement to 22-65 digits (Sec 2.3). This directly
   answers the predecessor's own named obstruction to making the coupled
   Volterra system rigorous (`h1_energy_estimate_attempt/ATTEMPT.md` Sec
   8.4: "differentiating `(BB-Psi')` in `x` requires control of
   `partial_x Delta Phi` ... an honest 'derivative loss' obstruction") --
   `(NEW-W)` never differentiates `(BB-Psi')` at all.

2. **The precise Volterra-in-y structure, and why it is not what a first
   guess suggests** (Sec 3): `(E2)` ALONE, with `W` treated as external
   data, is not a fixed-point problem at all -- it is already an EXPLICIT
   formula for `Phi` (linear, non-self-referential). The genuine
   self-referential loop only enters once `W` is closed in terms of `Phi`
   via `(NEW-W)` + `(BB-Psi')` + `I`, and that closure step reaches out to
   `Phi` at `x'>=x` **arbitrarily far** (via the Growth-Exclusion Lemma's
   own `u->infinity` integral) -- so the closed system is a genuine linear
   Volterra equation in `y`, but Banach-space-VALUED (values in `x`), with
   an OPERATOR-valued kernel that is **not confined to a compact `(x,y)`
   domain**. This precisely explains why the classical "Volterra kernels on
   a compact interval are always quasi-nilpotent" fact cannot be invoked
   for free.

3. **A rigorous operator-norm bound that isolates the exact obstruction**
   (Sec 4): decomposing the closed kernel `K(y,t)` into its `I`-only piece
   (bounded by `eps`, UNCONDITIONALLY, on the full unbounded `x`-domain --
   proved, Sec 4.2) and its `Psi`-via-`(BB-Psi')` piece (bounded by
   `eps*sqrt(pi/2)`, also UNCONDITIONALLY -- proved, Sec 4.3), the ENTIRE
   obstruction to a domain-independent bound is isolated to a single
   multiplication operator, `M_y := (1-eps(x+y))/eps` acting on functions
   of `x`, whose operator norm is `sup_x |1/eps - x - y|` -- **unbounded**
   as `x->infinity`, and, even restricted to any bounded `x`-strip, GROWS
   LINEARLY in `y` as `y->infinity`. This is a rigorous, analytic
   confirmation -- via a completely different route (operator norms on a
   Volterra kernel) -- of the SAME underlying mechanism the predecessor
   front found via contraction-mapping Lipschitz analysis (their own
   finding: `R(z)~1/z` only matches, not beats, linear-in-`y` growth of the
   source); here the "linear-in-`y` growth" is traced to its algebraic
   root, `Psi_x`'s own forced linear growth via the EXACT identity `(E1)`.
   **Two independent routes converge on the identical obstruction.**

4. **New numerical evidence: the actual Neumann series, iterated, does
   converge -- with a precisely measured two-regime structure** (Sec 5-6):
   a fresh, interpolation-free, grid-aligned discretization of the closed
   system (`v03_neumann_iteration.py`) is validated end-to-end against the
   independently-built `(P,Q)`-family series (itself validated 7/7 against
   all published anchors, Sec 5.2, 21+ digit match) via a clean Richardson
   grid-refinement test: discretization error shrinks at ratio `~4.09` per
   halving of `h`, matching `O(h^2)` trapezoid-quadrature error exactly
   (Sec 5.3, 9/9 test points, `mean ratio=4.087`). Then, iterating the
   ACTUAL (not linearized-in-one-step) Neumann/Picard map `Phi^(n+1) =
   g + L[Phi^(n)]` up to `n=16`, at `c=100` and `c=1000`, `y` up to `6`
   (Sec 6): **the successive-difference ratio, at every tested `y`, is
   eventually MONOTONICALLY DECREASING and heading toward `0`** (the
   qualitative signature of the classical `(MY)^n/n!` quasi-nilpotent
   decay) -- genuinely NEW content, since the predecessor's Lipschitz-`<=1`
   finding only examined a SINGLE step of the linearized map and could not
   see this. But the number of iterations needed before this favorable
   regime sets in ("warm-up length") **grows with `y`, empirically close to
   linearly** (least-squares slope `~0.50` at `c=100`, `~0.77` at
   `c=1000`), consistent with (not derived rigorously from) the Sec 4
   operator-norm bound's `M(y)~eps*y` growth.

**`H1` remains ABERTO/OPEN, exactly as before this front.** `phi_REDB`,
`Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law of record
are all untouched and unaffected by anything in this document. `H2` is
untouched (out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing.
No `adversarial/` subdirectory created; no referee dispatched by this front
itself, per the mandate. No git command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` Sec 2 (Tree B), specifically the `FLOORH2` and `PLATRESUM` nodes and
ALL dated addenda under `PLATRESUM` from its creation (wave-17,
`DISC-DEC-072/077`) through the most recent (wave-22 front b,
`DISC-DEC-096/100`); Sec 3 ("Regra de uso deste mapa"), the safety rule
against conflating this line with the separate "Arvore A" (`U_alpha`) line
-- followed strictly throughout (nothing from Arvore A is cited anywhere
below, even in hedged language); the full `mclust_h1_validity_attempt/
ATTEMPT.md` (the front that reduced `H1` to `(U1)`+`(U2)` via the Watson
Concentration Lemma, wave 20 front c); and the full
`h1_energy_estimate_attempt/ATTEMPT.md` (direct predecessor, wave 22 front
b -- establishing the exact identity `(BB-Psi')`, the global oscillation
bound `(star-star)`, and the precise Lipschitz-`<=1` contraction-mapping
diagnosis).

**No `.py` file from this front's own lineage or any ancestor front was
opened, read, or imported at any point.** Every script in this directory
(`v01`-`v07`) was written fresh, from the mathematical content of the prose
cited above; every previously-published number used as a cross-check (7
anchors at `c=1000`) is transcribed as plain text, never imported as code.
The `(P,Q)`-family recursion (Sec 5.1 below) is re-implemented from the same
verbatim prose recursion quoted in every ancestor `ATTEMPT.md` -- but via a
DIFFERENT algorithmic route than any predecessor is known to have used (an
explicit bounded-branch INTEGRAL formula rather than a hand-tuned
"descending-recursion/kappa-pinning" polynomial scheme; see Sec 5.1),
independently re-derived here from first principles (the Growth-Exclusion
mechanism already established in the required reading, applied to the
`b_k`-ODE itself) and validated 7/7 on the first attempt against the
published anchors (Sec 5.2) -- no self-caught bug was needed to reach that
result, unlike several ancestor fronts' own `(P,Q)`-family implementations.

**The exact inputs this front works from** (restated for self-containedness,
exactly as given in the required reading, quoted verbatim in
`h1_energy_estimate_attempt/ATTEMPT.md` Sec 0 -- cited, not re-derived from
further upstream, per the mandate):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Governing PDE system (record):
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi]+(1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                           (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv   (E2)

New exact identity for Psi (h1_energy_estimate_attempt Sec 2, cited, NOT
re-derived here -- used as an input in Sec 3.3):
  Psi(x,y) = int_0^infinity e^{-u^2/2-u(x+y)} I(x+u,y) du            (BB-Psi')

Series-recursion (Phi(s,g)=sum a_k(s)g^k, Psi(s,g)=sum b_k(s)g^k):
  a_0=1, b_0=0, a_1(s)=-c, b_1(s)=sqrt(pi c/2)*erfcx(s*sqrt(c/2))
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

Growth-Exclusion Lemma (mclust_h2_validity_attempt/ATTEMPT.md Sec 2, cited):
  for  u_x(x,y) - (x+y)u(x,y) = f(x)  (y a fixed parameter, f mild growth),
  the UNIQUE solution bounded as x->infinity is
     u(x,y) = -e^{x^2/2+xy} int_x^infinity e^{-(t^2/2+ty)} f(t) dt

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = psi1(x),  R'=xR-1,  R(z)<=1/z for z>0
Standing hypothesis (B): Phi, Psi bounded (used throughout this lineage).
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory was written to.

---

## 1. Overview of approach

Four lines of work, building on each other:

- **Part A (Sec 2).** Derive and verify a new, purely algebraic, closed-form
  identity for `W` -- eliminating the need to differentiate any integral
  representation of `Psi`, which is exactly the obstruction
  `h1_energy_estimate_attempt` Sec 8.4 named as blocking a rigorous
  treatment of the coupled Volterra system.
- **Part B (Sec 3).** Work out, precisely and structurally, what "the
  Volterra-in-y reformulation of `(E2)`" actually means once the self-
  referential loop is properly closed -- identifying exactly where the
  naive expectation (a classical, compact-domain Volterra equation) breaks
  down, and why.
- **Part C (Sec 4).** Turn that structural diagnosis into a rigorous
  operator-norm bound, isolating the precise obstruction analytically and
  connecting it explicitly to the predecessor front's independently-found
  Lipschitz-`<=1` obstruction.
- **Part D (Sec 5-6).** Build a fresh, independent numerical implementation
  of the WHOLE closed system (not the abstract `(P,Q)`-family series, a
  genuinely different computational route: grid-based Picard/Neumann
  iteration with quadrature) and use it to directly test whether the actual
  (non-linearized) Neumann series converges, at concrete `(c,y)` values, and
  to measure how its convergence rate depends on `y`.

Every result reports its own honest limits; none closes `(U1)` or `(U2)`.

---

## 2. Part A -- a new derivative-free algebraic identity for W

### 2.1 Derivation

`(KEY)` gives `W = Psi - eps*Psi_x`. Computing `Psi_x` by differentiating
the integral representation `(BB-Psi')` requires control of
`partial_x[Delta Phi]`, not merely `Delta Phi` -- the "derivative loss"
`h1_energy_estimate_attempt` Sec 8.4 names as an obstruction to making the
coupled system rigorous. But `(E1)` -- already exact, already in the
required reading, established independently of `(BB-Psi')` -- gives
`Psi_x` DIRECTLY, algebraically, with no differentiation at all:

```
W = Psi - eps*Psi_x = Psi - eps*[(x+y)Psi - I] = (1 - eps*(x+y))*Psi + eps*I     (NEW-W)
```

This is new to the record: no ancestor `ATTEMPT.md` performs this
substitution. It converts `W` from "a quantity requiring a derivative of an
integral" into "an explicit algebraic combination of `Psi` and `I`
themselves" -- both of which have their own closed integral representations
(`(BB-Psi')` for `Psi`, the elementary antiderivative `I=int_0^y Phi dy'`
for `I`) that do NOT need differentiating.

### 2.2 Symbolic verification (`v04_symbolic_algebra.py`)

Exact `sympy` algebra, treating `Psi`, `Psi_x`, `I` as free symbols and
`(E1)`/`(KEY)` as given substitution rules:

```
Check A: W (via KEY+E1 substitution) - (1-eps(x+y))Psi - eps*I  simplifies to: 0
  PASS: W = (1 - eps*(x+y))*Psi + eps*I   is an exact algebraic consequence of (E1)+(KEY).
```

**PASS**, trivially (this is linear algebra) but load-bearing: it confirms
the substitution introduces no sign error or missed term before any
numerical claim is built on it.

### 2.3 Numerical verification, via a STRUCTURALLY INDEPENDENT route
(`v02_new_identity_check.py`)

`(NEW-W)` is only useful if it agrees with the ORIGINAL `(KEY)` computed a
DIFFERENT way -- i.e. if `(E1)` itself is correct (already established by
the required reading, but re-verified here independently, since this front
leans on it directly) and if the algebra of Sec 2.1 is applied correctly.
Using the fresh `(P,Q)`-family series (Sec 5.1, `c=200`, `K=90`, `dps=90`):

- `Psi_x` route (a): via `(E1)`, `Psi_x = (x+y)*Psi - I`, both `Psi,I` read
  off the series.
- `Psi_x` route (b): via DIRECT term-by-term differentiation of the `b_k(s)`
  series itself (`Family.deriv()`, chain rule `Psi_x = eps * d(Psi)/ds`
  since `x=s/eps`) -- a completely independent computation, NOT using
  `(E1)` at all.

```
=== Check 1: (E1) cross-check -- Psi_x via (E1) vs via direct d/ds of b_k series ===
  (s=0.0,g=0.05): Psi_x[E1]=-0.0602182512125493  Psi_x[direct d/ds]=-0.0602182512125493  reldiff=5.02e-39
  (s=0.05,g=0.05): Psi_x[E1]=-0.0282436487041587  Psi_x[direct d/ds]=-0.0282436487041587  reldiff=3.176e-40
  (s=0.1,g=0.08): Psi_x[E1]=-0.0154126515978811  Psi_x[direct d/ds]=-0.0154126515978811  reldiff=9.322e-23
  (s=0.2,g=0.03): Psi_x[E1]=-0.00620433292499503  Psi_x[direct d/ds]=-0.00620433292499503  reldiff=2.063e-63

=== Check 2: new identity W = (1-eps(x+y))Psi + eps*I  vs  W = Psi - eps*Psi_x[direct] ===
  (s=0.0,g=0.05): W[KEY,direct-diff]=0.0841942839807378  W[NEW algebraic]=0.0841942839807378  reldiff=2.539e-40
  (s=0.05,g=0.05): W[KEY,direct-diff]=0.0525022893367294  W[NEW algebraic]=0.0525022893367294  reldiff=1.208e-41
  (s=0.1,g=0.08): W[KEY,direct-diff]=0.0367754843419312  W[NEW algebraic]=0.0367754843419312  reldiff=2.763e-24
  (s=0.2,g=0.03): W[KEY,direct-diff]=0.0221427068949415  W[NEW algebraic]=0.0221427068949415  reldiff=4.088e-65
```

**Agreement 22-65 digits at 4 points** -- both `(E1)` itself (Check 1) and
`(NEW-W)` (Check 2) confirmed via a computation route (differentiating a
convergent power series term-by-term) that shares NO algebraic step with
`(E1)`'s own derivation. This meets, and in several cases exceeds, the
lineage's own "23-37 digit agreement between structurally independent
routes" standard.

Two further checks in the same script re-verify `(BB-Psi')` itself (already
established by the required reading, re-confirmed here as this front leans
on it) and the pulled-out-constant form `(E2')` of Sec 3.1 below, both
against direct series evaluation:

```
=== Check 3: (BB-Psi') re-verification (Psi via series vs via renewal integral) ===
  (s=0.0,g=0.05): reldiff=6.318e-40
  (s=0.05,g=0.05): reldiff=2.876e-41
  (s=0.1,g=0.08): reldiff=5.921e-24

=== Check 4: (E2') pulled-out-constant form vs direct Phi(x,y) from series ===
  (s=0.0,g=0.05): reldiff=1.052e-38
  (s=0.05,g=0.05): reldiff=4.973e-40
  (s=0.1,g=0.08): reldiff=1.059e-22
```

**All PASS.** Full output: `v02_new_identity_check.log`.

---

## 3. Part B -- the precise Volterra-in-y structure

### 3.1 `(E2')`: a pulled-out-constant form, via an invariance already built
into `(E2)`

`(E2)`'s convolution shifts `(x,y) -> (x+v, y-v)` as `v` ranges over
`[0,y]`. A trivial but structurally important fact:

```
(x+v) + (y-v) = x+y                                                    for every v
```

`x+y` is **exactly invariant** along this shift (`v04_symbolic_algebra.py`
Check B, exact `sympy`, confirms this by direct simplification). Combined
with `(NEW-W)`, whose coefficient `(1-eps(x'+y'))` at the shifted point
`(x',y')=(x+v,y-v)` therefore equals `(1-eps(x+y))` -- a CONSTANT in `v` --
this factor pulls entirely outside the `v`-integral in `(E2)` (Check C,
verified by direct symbolic substitution and linearity of integration):

```
Phi(x,y) = e^{-y/eps} + [(1-eps(x+y))/eps] * A(x,y) + B(x,y)                  (E2')
  A(x,y) := int_0^y e^{-v/eps} Psi(x+v,y-v) dv
  B(x,y) := int_0^y e^{-v/eps} I(x+v,y-v) dv
```

This is new to the record and is not an approximation -- it is an exact
rearrangement of `(E2)`+`(NEW-W)`, verified numerically to 22-38 digits
against direct series evaluation (Sec 2.3, Check 4).

### 3.2 Why `x+y` is invariant: the transport-equation origin

This invariance is not a coincidence: the underlying governing PDE,
`dPhi/ds - dPhi/dg = c[Phi-W]`, is a transport equation whose characteristics
satisfy `d s/d(tau)=1, d g/d(tau)=-1`, i.e. `s+g` (equivalently `x+y`,
`x=s*sqrt(c)`, `y=g*sqrt(c)`) is EXACTLY conserved along them. `(E2)`'s
convolution direction IS the characteristic direction. This gives a clean
structural reading of `(E2')`: `A(x,y)` and `B(x,y)` are literal 1-D
Volterra convolutions of `Psi` (resp. `I`) restricted to the SINGLE
characteristic line `x'+y'=x+y`, against the fixed kernel `e^{-v/eps}` --
`y` genuinely plays the role of a Volterra "time" variable ALONG that one
line.

### 3.3 The catch: `I` and `Psi` are NOT themselves confined to that line

`I(x',y') = int_0^{y'} Phi(x',y'') dy''` fixes `x'` and integrates over
`y''`, sweeping characteristics `x'+y''` for `y'' in [0,y']` -- i.e. it
reaches OTHER characteristics (`x'+y'' <= x'+y' = ` the value at that
sub-point, in general `!= x+y`). And `Psi`, via `(BB-Psi')`, reaches even
further: `Psi(x',y') = int_0^infinity e^{-u^2/2-u(x'+y')} I(x'+u,y') du`
integrates `I` at `x'+u` for `u` ranging over the ENTIRE half-line
`[0,infinity)` -- i.e. `Phi` at characteristics `x'+u+y''` for
`u in [0,infinity)`, reaching arbitrarily far beyond `x+y` itself.

**This is the crux.** A single application of `(E2')` to compute
`Phi(x,y)` needs `Phi` at points reaching arbitrarily far in `x` (via the
Growth-Exclusion/`(BB-Psi')` mechanism's own `u->infinity` integral, which
is precisely what makes the bounded-branch solution UNIQUE in the first
place -- Sec 0's Growth-Exclusion Lemma). So the SELF-REFERENTIAL closure
of `(E2')` -- writing `A,B` (hence `Phi(x,y)`) in terms of `Phi` itself via
`I` and `Psi[I]` -- is a genuine Banach-space-VALUED (values: bounded
functions of `x in [0,infinity)`) linear Volterra equation in `y`:

```
Phi_y = g_y + int_0^y K(y,t) [Phi_t] dt                                (VOLTERRA-Phi)
```

where `Phi_y := Phi(.,y) in X := C_b([0,infinity))`, `g_y(x):=e^{-y/eps}`,
and `K(y,t)` is an OPERATOR on `X` (derived explicitly in Sec 4). This is
the precise, correct content of "the Volterra-in-y reformulation of `(E2)`"
-- and it is a **genuinely different** object from the sup-norm-in-`(x,y)`
fixed-point map `h1_energy_estimate_attempt` Sec 8 examined (which
linearized the FULL `(x,y)`-joint problem into a single contraction
question; here `y` alone is the Volterra/causal variable, `x` is carried as
a Banach-space index).

### 3.4 Why this is NOT automatically the classical, compact-domain case

The classical fact this front was asked to state and verify (mandate item
2): a linear Volterra operator `(Kf)(t) = int_0^t k(t,s) f(s) ds` on
`C([0,T];X)`, with `k:[0,T]x[0,T] -> B(X)` (bounded operators on `X`)
continuous, hence `sup ||k(t,s)|| =: M < infinity` on the COMPACT triangle
`0<=s<=t<=T`, is quasi-nilpotent:

```
||K^n|| <= (M*T)^n / n!  -> 0   as n -> infinity
```

**Proof** (standard, stated here for completeness): `(K^n f)(t)` is an
`n`-fold iterated integral of `k(t,t_1)k(t_1,t_2)...k(t_{n-1},t_n)f(t_n)`
over the simplex `0<=t_n<=...<=t_1<=t<=T`, whose volume is `t^n/n! <=
T^n/n!`; bounding the integrand by `M^n ||f||` gives the stated bound. This
requires ONLY that `k` be bounded on the (compact) domain -- it does **not**
require any smallness of `M` or `T`; quasi-nilpotency is unconditional once
`M,T` are merely finite.

The catch, precisely: **our kernel `K(y,t)` is NOT bounded, uniformly, on
any domain that includes the FULL range `x in [0,infinity)` needed for `X`
to be the natural space** -- because, per Sec 3.3, evaluating `K(y,t)` at a
given `x` requires reaching to `x'>=x` arbitrarily far. This is exactly
where the classical compact-domain argument's hypothesis fails to hold for
free, and exactly why the required reading's own Growth-Exclusion Lemma
(needed to make `Psi` well-defined and unique at all) is doing real,
non-compact-domain work that the textbook Volterra theorem does not, by
itself, control. Sec 4 makes this precise with an actual operator-norm
computation, rather than leaving it at this qualitative level.

---

## 4. Part C -- a rigorous operator-norm bound, isolating the obstruction

### 4.1 Setup

Write `Phi_y(x):=Phi(x,y)`, and similarly `Psi_y, I_y`. From `(BB-Psi')`,
`Psi_y = T_y[I_y]` where `(T_y f)(x) := int_0^infinity e^{-u^2/2-u(x+y)}
f(x+u) du` is a bounded linear operator on `X=C_b([0,infinity))` (sup norm).
`I_y = int_0^y Phi_t dt` (a Bochner integral in `X`). Substituting into
`(E2')` and changing the order of integration (routine algebra --
substitute `A_y(x)=int_0^y e^{-v/eps}Psi(x+v,y-v)dv`, write
`Psi(x+v,y-v)=(T_{y-v}[I_{y-v}])(x+v)=(S_v T_{y-v}[I_{y-v}])(x)`, expand
`I_{y-v}=int_0^{y-v}Phi_{y''}dy''`, substitute `w=y-v` and swap the two
integration orders exactly as in Sec 3.1's `x+y`-invariance argument,
applied here to the `(v,y'')` pair instead of the single `v`) gives
`(VOLTERRA-Phi)` with

```
K(y,t) = M_y o K_A^raw(y,t)  +  K_B(y-t)
  K_B(h)       := int_0^h e^{-v/eps} S_v dv                    (S_v f)(x):=f(x+v), the shift operator
  K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
  M_y          := multiplication-by-[(1-eps(x+y))/eps]   (a function of x, for fixed y)
```

### 4.2 The `I`-only piece `K_B(h)` is bounded by `eps`, unconditionally

`S_v` is an isometry on `X` (`||S_v||=1` for every `v>=0`, trivially --
shifting a bounded function does not change its sup norm). So

```
||K_B(h)||  <=  int_0^h e^{-v/eps} * ||S_v|| dv  =  eps*(1-e^{-h/eps})  <=  eps
```

**for every `h>=0`** -- no domain restriction on `x` needed at all. (This
matches, and gives an independent operator-theoretic derivation of, the
`(E2)` kernel's own elementary normalization `int_0^infinity (1/eps)
e^{-v/eps} dv = 1`.)

### 4.3 The `Psi`-via-`(BB-Psi')` piece `K_A^raw(y,t)` is bounded by
`eps*sqrt(pi/2)`, unconditionally

`||T_w|| <= sup_x R(x+w) = R(w)` (`R` decreasing, so the sup over `x>=0` is
at `x=0`) -- `R` and its two facts used here (`R(0)=sqrt(pi/2)`, `R`
strictly decreasing) are re-verified independently in `v07_operator_bounds.py`
(Sec 4.5 below). Then, using `R` decreasing (`R(w)<=R(t)` for `w>=t`):

```
||K_A^raw(y,t)||  <=  int_t^y e^{-(y-w)/eps} R(w) dw
                  <=  R(t) * int_t^y e^{-(y-w)/eps} dw
                  <=  R(t) * eps
                  <=  eps * R(0)  =  eps * sqrt(pi/2)
```

**again for every `y,t` with `0<=t<=y`** -- unconditionally, no domain
restriction on `x` (this bound never used `x` at all: it is a bound on an
operator norm, i.e. already the worst case over all `x`).

### 4.4 The obstruction is isolated entirely to `M_y`

> **CORREÇÃO (2026-08-28, referee hostil + sessão orquestradora,
> `DISC-DEC-113`, achado H1, ALTA).** Esta subseção contém um erro
> real: ela nunca limita o operador COMPOSTO
> `M_y \circ K_A^{\mathrm{raw}}(y,t)` que de fato aparece no núcleo —
> apenas o `M_y` isolado, e `\|AB\|\le\|A\|\|B\|` é inútil quando
> `\|A\|=\infty`. Explorando o cancelamento `x'+w=x+y` (independente
> de `w`) já presente na álgebra da §4.1 mas nunca usado aqui, o
> operador composto satisfaz
> `\|M_yK_A^{\mathrm{raw}}(y,t)\|\le h_\varepsilon(x+y)`,
> `h_\varepsilon(z):=|1-\varepsilon z|R(z)`, que é **globalmente
> limitado** por `\sqrt{\pi/2}` (atingido em `z=0`) e **não cresce em
> `y`** — confirmado por computação direta em duas rotas
> independentes pelo referee, e reconfirmado independentemente pela
> sessão orquestradora. O texto abaixo ("a limitação... depende
> inteiramente de `M_y`"; "isto é o conteúdo real da obstrução") está
> **errado** e é preservado apenas para registro histórico — ver
> `adversarial/REFEREE_REPORT.md` achado H1 para a derivação completa
> do limitante corrigido.

Both `K_B` and `K_A^raw` are bounded by `O(eps)`, uniformly over the ENTIRE
unbounded `(x,y,t)` domain -- genuinely good news, and new content (this
decomposition and these two bounds are not present in any required-reading
document). The full kernel's boundedness therefore hinges entirely on

```
||M_y||_{op}  =  sup_{x>=0} |(1-eps(x+y))/eps|  =  sup_{x>=0} |1/eps - x - y|
```

which is **unbounded** as `x -> infinity` on the full space `X`. Restricting
to a bounded strip `X_L := C_b([0,L])`:

```
||M_y||_{X_L}  <=  1/eps + L + y            (triangle inequality)
```

-- finite for any fixed `L`, but **growing linearly in `y`** as `y ->
infinity`, for ANY fixed `L` (including `L` scaled with `1/eps` to match the
"physical" domain `s<=1`, i.e. `x<=1/eps`, still gives `||M_y|| <= 2/eps +
y`, still `~y` for large `y`). Since `(U1)`/`(U2)` are precisely statements
about the `y->infinity` limit, this growth is not a technicality that a
smarter choice of `L` removes -- **it is the actual content of the
obstruction**, expressed for the first time here as an operator-norm growth
rate rather than a single Lipschitz-constant saturation.

### 4.5 Independent verification of the `R(z)` facts used above
(`v07_operator_bounds.py`)

```
=== (i) int_0^inf e^{-u^2/2-uz} du == R(z) ===
  z=0.0: reldiff=0.0        z=0.5: reldiff=1.31e-41
  z=2.0: reldiff=4.086e-41  z=5.0: reldiff=1.488e-41
=== (ii)+(iii) R(0) and monotone decreasing ===
  R(0) = 1.2533141373155002512 = sqrt(pi/2)   PASS
  monotone strictly decreasing on [0,4.5]: True
=== (iv) R(z) <= 1/z for z>0 ===
  z=0.1,1.0,5.0,20.0: all PASS
```

**All facts used in Sec 4.2-4.4 independently confirmed**, up to 41 digits
where applicable. Full output: `v07_operator_bounds.log`.

### 4.6 Reading: two independent routes converge on the same obstruction

> **CORREÇÃO (2026-08-28, referee hostil + sessão orquestradora,
> `DISC-DEC-113`, achado H2, ALTA, decorrente do achado H1).** Como a
> §4.4 (achado H1) está errada — o operador composto de fato NÃO
> cresce em `y`, sendo limitado uniformemente — não há uma segunda
> confirmação independente aqui. A alegação "duas rotas independentes
> convergem no mesmo mecanismo" está **incorreta**: apenas a rota do
> `h1_energy_estimate_attempt` (Lipschitz `<=1`) estabelece de fato
> uma obstrução; a rota desta frente não estabelece nada — o texto
> abaixo é preservado apenas para registro histórico.

`h1_energy_estimate_attempt` Sec 8.2-8.3 found, via a DIFFERENT method
(sup-norm Lipschitz analysis of the composite `Phi -> Psi -> W -> Phi` map,
examining a SINGLE application), that the obstruction is "the kernel
`R(z)~1/z` only MATCHES, not beats, the linear-in-`y` growth of the source
`I`" -- an essentially empirical/computed-bound finding (Lipschitz constant
`<=1`, shown numerically tight). This front's Sec 4 finds, via a
STRUCTURALLY DIFFERENT method (operator-norm decomposition of the Volterra
kernel itself, tracing the growth to its algebraic source), that the SAME
linear-in-`y` growth is the FORCED consequence of `Psi_x`'s own linear
growth via the EXACT identity `(E1)` -- not a property of any particular
norm or bounding strategy, but a fact about `Psi_x` itself: since `Psi,I`
are `O(1)` (bounded, hypothesis `(B)`), `(E1)` forces `Psi_x = (x+y)*Psi -
I ~ (x+y)*O(1)`, i.e. genuinely, unavoidably, LINEARLY GROWING in `x+y`
(barring exact cancellation). **Two a priori unrelated strategies -- a
crude sup-norm contraction bound, and a careful operator-norm Volterra-
kernel decomposition -- independently arrive at the identical underlying
mechanism.** This is itself a meaningful finding: it upgrades "one attempted
route failed for reason X" to "two structurally different routes both fail
for the SAME reason X", making it substantially more likely that X is a
genuine feature of this system rather than an artifact of either technique.

---

## 5. Part D -- numerical machinery

### 5.1 Fresh `(P,Q)`-family series implementation, via a bounded-branch
INTEGRAL method (`v01_family_series.py`)

Rather than reverse-engineering the "descending-recursion/kappa-pinning"
scheme ancestor fronts describe (informally) for solving the bounded-branch
ODE `y'(s)-c*s*y(s)=source(s)` within the `(P,Q)` family, this front uses
the SAME Growth-Exclusion mechanism already established elsewhere in the
lineage, applied directly to THIS ODE (a special case with `y`-parameter
`0`): the unique solution bounded as `s->infinity` is

```
y(s) = -e^{c s^2/2} * int_s^infinity e^{-c t^2/2} * source(t) dt
```

Since `e^{-c t^2/2} * erfcx(t*sqrt(c/2)) = erfc(t*sqrt(c/2))` EXACTLY (the
defining identity of `erfcx`), this integral splits into two classical,
closed-form families -- `G_n(s):=int_s^inf t^n e^{-ct^2/2}dt` (elementary
Gaussian moments) and `H_m(s):=int_s^inf t^m erfc(t sqrt(c/2))dt` (via
integration by parts, reducing to `G_{m+1}`) -- both computed by elementary,
hand-derived recursions (module docstring, `v01_family_series.py`), giving
`a_k(s), b_k(s)` directly in `(P,Q)`-family form with NO free/undetermined
constant at any step (the "bounded branch" selection IS the choice of this
specific integral, exactly as elsewhere in this lineage -- no separate
"pinning" heuristic needed).

**Self-check at module load**: reproduces `b_1(s)=sqrt(pi c/2)*erfcx(s
sqrt(c/2))` (the `k=1` case of the recursion, source `f(s)=-c`) EXACTLY,
before being trusted for anything else.

### 5.2 Validation against all 7 published anchors (`v01_family_series.log`)

At `c=1000`:

| quantity | this front's value | published anchor | digits agree |
|---|---|---|---|
| `a2(0)` | `520316.636488030055...` | `520316.636488` | full (13 shown) |
| `a3(0)` | `-180730907.628508066766...` | `-180730907.6285` | full (14 shown) |
| `a4(0)` | `47146963944.1378859211...` | `47146963944.14` | full (14 shown) |
| `b1(0)` | `39.6332729760601101...` | `sqrt(pi*1000/2)` | exact, symbol-for-symbol |
| `b2(0)` | `-20816.6364880300550667...` | `-20816.636488` | full (13 shown) |
| `Phi(0,0.002)` | `0.1585001457473084842...` | `0.15850015` | full (10 shown) |
| `Phi(0,0.05)` [plateau] | `0.0377615983402126188244...` (K=220, dps=280) | `0.0377615983402126188243712...` | **21+ digits** |

**7/7 PASS**, on the first implementation attempt (no self-caught bug
needed for correctness -- see Sec 7 for the one self-caught issue that DID
occur, unrelated to correctness). The last anchor (the plateau value,
requiring resolving a `~24-26` order-of-magnitude internal cancellation)
needed `K=220,dps=280`, matching exactly the `(K,dps)` sizing ancestor
fronts independently converged on for the same computation -- itself a
useful cross-check that this is an intrinsic property of the series, not an
artifact of any one front's implementation.

### 5.3 The Neumann/Picard grid iteration (`v03_neumann_iteration.py`)

Implements the closed system `(VOLTERRA-Phi)` (via `(E2')`+`(NEW-W)`+
`(BB-Psi')`+`I`) as an explicit, INTERPOLATION-FREE grid computation: `x`
and `y` share the same step `h`, so every shift used by the formulas (`x+v`,
`x+u`) lands exactly on a grid point (no interpolation error introduced).
Because the map reaches `x -> x+y+u` (up to a truncation `Umax` on the
`(BB-Psi')` `u`-integral, `e^{-Umax^2/2}` negligible at `Umax=6`), computing
`Phi^(n)` accurately on a "core" `x`-window `[0,Xcore]` requires
`Phi^(n-1)` on an EXTENDED window `[0,Xcore+Ycore+Umax]`; iterating `n_max`
times therefore starts from a domain of width `Xcore+n_max*(Ycore+Umax)`
(where `Phi^(0)=g_y` is explicit, needing no precomputation) and SHRINKS by
`Ycore+Umax` grid-steps each iteration, ending at exactly `Xcore` after
`n_max` steps.

**Core demonstration** (`c=100`, `h=0.1`, `n_max=5`, 9 test points spanning
`x in {0,0.3,0.6}`, `y in {0.2,0.5,1.0}`), compared against the ground-truth
`(P,Q)`-family series (`K=100, dps=120`, itself independently stable across
`K,dps` -- confirmed by re-running at `K=60..220,dps=60..300` and finding
agreement to 12+ digits already at the smallest sizing, since these `(s,g)`
values are far from the deep-cancellation regime of Sec 5.2's plateau
anchor):

```
(x=0.0,y=0.2): n=0..5: 0.1353, 0.2184, 0.2224, 0.2225, 0.2225, 0.2225   TRUE=0.2060
(x=0.0,y=0.5): n=0..5: 0.0067, 0.1118, 0.1335, 0.1352, 0.1353, 0.1353   TRUE=0.1127
(x=0.0,y=1.0): n=0..5: 0.0000, 0.0809, 0.1255, 0.1343, 0.1352, 0.1352   TRUE=0.1089
   [full 9-point table in v03_neumann_iteration.log]
```

The iteration converges (in `n`, at this fixed `h=0.1`) to a value close to,
but not exactly matching, the TRUE continuum value -- the residual gap is
diagnosed and resolved in Sec 5.4 as ordinary `O(h^2)` trapezoid
discretization error, not a failure of the Neumann series.

### 5.4 End-to-end validation: Richardson grid-refinement convergence
(`v05_richardson_convergence.py`/`.log`)

Refining `h: 0.1 -> 0.05 -> 0.025` (same 9 test points, `n_max=6`):

| point | err(h=.1) | err(h=.05) | err(h=.025) | ratio1 | ratio2 |
|---|---|---|---|---|---|
| (0,0.2) | +1.644e-2 | +3.997e-3 | +9.920e-4 | 4.113 | 4.030 |
| (0,0.5) | +2.260e-2 | +5.470e-3 | +1.356e-3 | 4.131 | 4.034 |
| (0,1.0) | +2.639e-2 | +6.304e-3 | +1.558e-3 | 4.187 | 4.047 |
| (0.3,0.2) | +1.309e-2 | +3.184e-3 | +7.903e-4 | 4.111 | 4.029 |
| (0.3,0.5) | +1.795e-2 | +4.351e-3 | +1.079e-3 | 4.126 | 4.032 |
| (0.3,1.0) | +2.076e-2 | +4.970e-3 | +1.229e-3 | 4.176 | 4.045 |
| (0.6,0.2) | +1.073e-2 | +2.610e-3 | +6.478e-4 | 4.110 | 4.029 |
| (0.6,0.5) | +1.468e-2 | +3.562e-3 | +8.837e-4 | 4.121 | 4.031 |
| (0.6,1.0) | +1.683e-2 | +4.038e-3 | +9.989e-4 | 4.168 | 4.042 |

**Mean ratio `4.087` (std `0.055`), at every one of 9/9 points, both
halvings** -- a clean, textbook `O(h^2)` signature (pure trapezoid-rule
quadrature error), confirming the discretized Neumann/Picard fixed point
converges to the TRUE continuum `Phi` as `h->0`. This is a strong,
structurally-independent (grid-based Picard iteration + quadrature, vs. an
infinite power series with symbolically-solved coefficients) end-to-end
validation of the ENTIRE closed system derived in Sec 2-3: `(NEW-W)`,
`(E2')`, `(BB-Psi')`, and the discretization itself, simultaneously.

---

## 6. The two-regime convergence structure: warm-up, then super-geometric
decay (`v06_warmup_vs_y.py`/`.log`)

### 6.1 Method

At fixed `x=0`, `h=0.1`, `Umax=6`, `n_max=16`, track the FULL sequence
`Phi^(0),...,Phi^(16)` at several `y` values (`0.5` to `6.0`), and examine
the ratio of successive differences `|Phi^(n)-Phi^(n-1)| /
|Phi^(n-1)-Phi^(n-2)|` -- this is exactly the "verify convergence
numerically by computing several terms and checking the partial sums
stabilize" test the mandate names, applied to the ACTUAL (not linearized
single-step) Neumann/Picard map.

### 6.2 Results at c=100

```
y=0.5: ratios = 0.207, 0.076, 0.044, 0.031, 0.025, 0.021, 0.018, 0.016, 0.015, ...
y=1.0: ratios = 0.552, 0.197, 0.105, 0.068, 0.049, 0.038, 0.031, 0.026, 0.023, ...
y=2.0: ratios = 1.124, 0.432, 0.238, 0.154, 0.109, 0.082, 0.065, 0.053, 0.045, ...
y=3.0: ratios = 1.550, 0.622, 0.352, 0.232, 0.166, 0.127, 0.100, 0.082, 0.068, ...
y=4.0: ratios = 1.879, 0.775, 0.448, 0.299, 0.217, 0.167, 0.133, 0.109, 0.091, ...
y=5.0: ratios = 2.143, 0.901, 0.528, 0.357, 0.261, 0.202, 0.162, 0.133, 0.112, ...
y=6.0: ratios = 2.362, 1.008, 0.597, 0.407, 0.300, 0.233, 0.188, 0.156, 0.131, ...
```

At `y=0.5,1.0` the ratio is `<1` from the very first step. At `y>=2.0` the
ratio EXCEEDS `1` for the first `1-2` steps (i.e. the second difference is
LARGER than the first -- a genuine transient growth, not divergence) before
turning over and decreasing monotonically and (empirically) super-
geometrically for the remainder of every sequence tested (the ratio itself
keeps shrinking at each further step -- e.g. at `y=6.0`: `2.362, 1.008,
0.597, 0.407, 0.300, ..., 0.063` at `n=16` -- never plateauing at a fixed
value `<1`, which is exactly the qualitative signature the `(MY)^n/n!`
bound of Sec 3.4 predicts and that a mere Lipschitz-`<1` contraction would
NOT produce (a true contraction gives an EVENTUALLY CONSTANT ratio, not a
ratio that keeps shrinking).

### 6.3 Robustness check at c=1000

The identical qualitative pattern (transient growth at large `y`, then
permanent, accelerating decrease) is confirmed at `c=1000` (`eps=0.0316`),
ruling out a `c=100`-specific artifact:

```
y=1.0: ratios = 1.112, 0.447, 0.258, 0.175, 0.130, ..., 0.035
y=3.0: ratios = 2.659, 1.121, 0.663, 0.454, 0.338, ..., 0.079
y=6.0: ratios = 3.937, 1.728, 1.049, 0.732, 0.552, ..., 0.135
```

### 6.4 The warm-up length grows (roughly linearly) with y

Defining `n_cross(y)` as the smallest `n` after which the ratio stays
permanently below `0.5`:

| `y` | `n_cross`, `c=100` | `n_cross`, `c=1000` |
|---|---|---|
| 0.5 | (already `<0.5` at `n=2`) | (already `<0.5` at `n=2`) |
| 1.0 | (already `<0.5` at `n=2`) | 3 |
| 2.0 | 3 | 4 |
| 3.0 | 4 | 5 |
| 4.0 | 4 | 6 |
| 5.0 | 5 | 6 |
| 6.0 | 5 | 7 |

Least-squares linear fit: `n_cross ~ 0.500*y + 2.200` (`c=100`), `n_cross ~
0.771*y + 2.467` (`c=1000`). **The warm-up length grows with `y` at both
tested `c` values, roughly linearly**, with a slope that itself grows
mildly as `c` increases (`eps` decreases) -- consistent, qualitatively, with
the Sec 4.4 operator-norm bound `||M_y|| ~ 1/eps + y` (more terms needed to
"pay down" a larger effective kernel bound before the `1/n!` suppression in
`(MY)^n/n!`-type decay takes over), though this front does **not** derive
the specific linear-in-`y` rate (nor its `c`-dependence) rigorously from
that bound -- the crude Sec 4 bound, taken literally, would predict
something closer to quadratic-in-`y` growth (`M(y)~eps*y`, combined with
domain size `~y`, gives `MY~eps*y^2`); the empirically MILDER, closer-to-
linear growth indicates the true (unbounded, self-consistent) system
converges FASTER than the crude worst-case operator-norm bound of Sec 4
predicts -- unsurprising for a sup-norm-style bound, but a concrete,
honestly-reported gap between what was rigorously proved (Sec 4) and what
was numerically measured (Sec 6).

---

## 7. Self-caught issues (disclosed, per this lineage's convention)

**S1 (this front's own catch, numerical, during initial script development,
before any result was reported).** The first version of the Neumann-
iteration comparison script evaluated the ground-truth `(P,Q)`-family
series directly at the SCALED grid coordinates `(x,y)` (e.g. `y=1.0`)
instead of converting to the UNSCALED series coordinates `(s,g)=(x/sqrt(c),
y/sqrt(c))` before calling `Phi_true(s,g)`. Since the series diverges wildly
outside its region of good numerical behavior when fed values many times
larger than intended (`g=1.0` at `c=100` vs. the intended `g=0.1`), this
produced absurd "ground truth" values (e.g. `Phi_true ~ 10^24`) that were
IMMEDIATELY visually obvious as wrong (a probability-like quantity `Phi`
must lie in `[0,1]`) before being used in any reported comparison. Traced by
inspection (the scaling relation `x=s*sqrt(c)` was simply not applied at
the call site) and fixed by explicit division by `sqrt(c)`; re-run
confirmed sane values (`Phi_true` in `[0.07,0.25]` across all test points,
matching Sec 5.3's table) before Sec 5.3-6.4's results were trusted or
reported.

No other issue was encountered in this front's own new work. (Section 5.1's
bounded-branch integral method for the `(P,Q)`-family recursion passed its
self-check and all 7 anchor validations on the first attempt, with no
correction needed -- noted in Sec 5.2, in contrast to several ancestor
fronts' own independent implementations of the SAME recursion, which each
required at least one self-caught fix.)

---

## 8. Seeds

Reserved range `20260925000-20260925999` per `DISC-DEC-110`. Grep-confirmed
BEFORE any use (`grep -rn "20260925" 05_DISCOVERY_LAB/`): appears only in
`DECISION_LEDGER.yaml`'s `DISC-DEC-110` entry and `DISCOVERY_LAB_STATE.md`'s
summary of that reservation. **No randomness was used anywhere in this
front** -- every computation is exact symbolic algebra (`sympy`),
deterministic arbitrary-precision series/quadrature (`mpmath`), or
deterministic grid-based numerical iteration (`numpy`, float64, fixed grids
and fixed test points, no sampling). The reserved range remains entirely
unused, exactly as every direct ancestor front in this lineage reports for
its own reservation.

---

## 9. Files

| file | role |
|---|---|
| `v01_family_series.py`/`.log` | fresh `(P,Q)`-family recursion via a bounded-branch INTEGRAL method (new algorithmic route, Sec 5.1); 7/7 published-anchor validation at `c=1000` (Sec 5.2) |
| `v02_new_identity_check.py`/`.log` | numerical verification of `(NEW-W)` (Sec 2.3) against a structurally-independent differentiation route; re-verification of `(BB-Psi')` and `(E2')` |
| `v03_neumann_iteration.py`/`.log` | grid-based, interpolation-free Neumann/Picard iteration of the closed Volterra-in-y system; core 9-point demonstration vs. ground truth (Sec 5.3) |
| `v04_symbolic_algebra.py`/`.log` | exact `sympy` verification of the `(NEW-W)` and `(E2')` algebra (Sec 2.2, 3.1) |
| `v05_richardson_convergence.py`/`.log` | grid-refinement (`h`-halving) Richardson test, `O(h^2)` convergence to true `Phi` (Sec 5.4) |
| `v06_warmup_vs_y.py`/`.log` | the two-regime (warm-up then super-geometric decay) Neumann-series experiment, `c in {100,1000}`, `y` up to 6 (Sec 6) |
| `v07_operator_bounds.py`/`.log` | independent verification of the `R(z)` facts used in the Sec 4 operator-norm bound |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`mclust_h1_validity_attempt/h1_volterra_attempt/` subdirectory was written
to -- every ancestor `ATTEMPT.md`/`adversarial/` file and
`PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (Sec 0), never modified. No `adversarial/`
subdirectory created; no referee dispatched by this front itself, per the
mandate.

---

## 10. Scorecard

| claim | status |
|---|---|
| `(NEW-W)`: `W=(1-eps(x+y))Psi+eps*I`, exact algebraic consequence of `(E1)`+`(KEY)` | **PROVED** (symbolic, Sec 2.2) + numerically confirmed 22-65 digits (Sec 2.3) |
| `(E2')`: pulled-out-constant reformulation of `(E2)` | **PROVED** (exact rearrangement, Sec 3.1) + numerically confirmed 22-38 digits |
| `x+y` invariant along `(E2)`'s convolution shift | **PROVED** (trivial exact identity, Sec 3.1) |
| Closed system is a Banach-space-valued linear Volterra equation in `y` | **PROVED** (structural derivation, Sec 3.3-4.1) |
| `||K_B(h)|| <= eps` unconditionally (full unbounded `x`-domain) | **PROVED** (Sec 4.2) |
| `||K_A^raw(y,t)|| <= eps*sqrt(pi/2)` unconditionally | **PROVED** (Sec 4.3), using `R` facts independently re-verified (Sec 4.5) |
| Full kernel `K(y,t)` bounded on the UNRESTRICTED `x in [0,infinity)` domain | ~~REFUTED (Sec 4.4: `\|\|M_y\|\|` unbounded as `x->infinity`)~~ **CORRIGIDO 2026-08-28 (`DISC-DEC-113`): PROVED** — o operador COMPOSTO `M_y K_A^raw(y,t)` (não `M_y` isolado) é o que de fato aparece no núcleo, e é limitado por `sqrt(pi/2)` uniformemente, incluindo no domínio irrestrito (ver correção na Sec 4.4) |
| Full kernel bounded on any FIXED bounded `x`-strip, for FIXED `y` | **PROVED** (Sec 4.4, `||M_y||<=1/eps+L+y` — bound on `M_y` alone still correct, apenas irrelevante dado o item acima) |
| That strip-restricted bound stays bounded as `y->infinity` | ~~REFUTED (Sec 4.4: grows linearly in `y`, for any fixed strip)~~ **CORRIGIDO 2026-08-28 (`DISC-DEC-113`): PROVED** — o operador composto de fato relevante não cresce em `y`, saturando perto de `eps` (ver correção na Sec 4.4) |
| Classical Volterra quasi-nilpotency theorem, stated and re-derived | **PROVED** (classical fact, re-derived from scratch, Sec 3.4) |
| ... applies unconditionally to give `(U1)`/`(U2)` | **NOT ESTABLISHED** (Sec 3.4/4.4: hypothesis of the theorem, `M` finite on the RELEVANT unbounded-in-y domain, fails) |
| Discretized Neumann/Picard fixed point converges to TRUE `Phi` as `h->0` | **PROVED numerically** (Richardson `O(h^2)`, mean ratio `4.087`, 9/9 points, Sec 5.4) |
| Actual (non-linearized) Neumann series converges at every tested finite `y` | **CONFIRMED numerically** (ratio `->0` super-geometrically at every tested `(c,y)`, Sec 6.2-6.3; not proved analytically in general) |
| Warm-up length before super-geometric regime grows with `y` | **MEASURED numerically**, roughly linear, both `c` tested (Sec 6.4); not derived rigorously |
| Warm-up length's specific rate matches the crude Sec 4 bound's prediction | **REFUTED literally** (bound predicts closer to quadratic; measured is closer to linear -- true system converges faster than the crude worst-case bound, Sec 6.4) |
| `(U1)` (locally-uniform `g->infinity` convergence of `W`) | **OPEN** (unchanged) |
| `(U2)` (uniform-in-`x` Poincare expansion of `W_inf`) | **OPEN** (unchanged) |
| `H1` | **OPEN** (unchanged) |
| `H2` | **NOT ATTEMPTED** (out of scope, per mandate) |
| Non-perturbative/trans-series content | **NOT ATTEMPTED** (named, not addressed, exactly as every ancestor front) |

---

## 11. What remains open, precisely

1. **`(U1)`/`(U2)` themselves remain unproved.** This front's contribution is
   a SHARPER, more precisely LOCATED diagnosis of the obstruction (Sec 4:
   the multiplication operator `M_y`, growing linearly in `y`, traced to
   `Psi_x`'s forced linear growth via the exact `(E1)`) plus new numerical
   evidence that the actual Neumann series nonetheless DOES converge at
   every finite `y` (Sec 6) -- but converting "converges at every finite `y`,
   with an empirically-measured, roughly-linear-in-`y` warm-up length" into
   a rigorous, UNIFORM (as `y->infinity`) statement is exactly `(U1)`/`(U2)`
   restated, not yet achieved.
2. **The gap between the rigorous Sec 4 bound and the numerically measured
   Sec 6 behavior is itself unexplained.** The crude operator-norm bound
   over-predicts the warm-up length's growth rate (closer to quadratic
   than the observed near-linear). Closing this gap -- e.g. by exploiting
   SIGN/CANCELLATION structure in the iterated kernel that the crude
   sup-norm bound throws away, similar in spirit to what
   `h1_energy_estimate_attempt` Sec 10 item 1(a) already named as the
   needed ingredient for its own route -- was not attempted here.
3. **The `(c,y)` range tested numerically is finite** (`c in {100,1000}`,
   `y` up to `6`, `h` down to `0.025`). No claim is made that the two-regime
   pattern (Sec 6) persists at all `c`, all `y` -- only that it was found,
   robustly, at every point tested, with no counterexample.
4. **A rigorous derivation of the `n_cross(y)` growth rate** (Sec 6.4),
   analytically from the operator structure of Sec 4 (rather than merely
   observing it numerically and noting qualitative consistency), was not
   attempted -- named as the single most concrete, well-defined next step
   this front identifies.
5. **`H2` untouched**, exactly as the mandate scoped this front to
   `(U1)`/`(U2)` (equivalently `H1`) alone.
6. **Non-perturbative (trans-series) content remains entirely untested**,
   exactly as every ancestor front in this specific sub-line already names.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law
of record are all untouched and unaffected by anything in this document.

---

## 12. Scope discipline

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html`, or any file outside this front's own new
`h1_volterra_attempt/` directory. No `adversarial/` subdirectory created (a
separate hostile referee is dispatched later by the orchestrating session,
per the mandate). No `git` command of any kind run. No claim of progress on
any Millennium Prize Problem appears anywhere in this document -- `M-CLUST(b)`
is, as stated at the top of this document and throughout the required
reading, a standalone combinatorial/asymptotic object, entirely independent
of the archive's separate Tree A (`u1/2`) line. Per `PROOF_DEPENDENCY_MAP.md`
Sec 3's explicit rule, no result, finding, or hedge from the Tree A line is
cited anywhere in this document as evidence for anything claimed here, and
no result from this document is intended to be read as evidence for
anything in Tree A.
