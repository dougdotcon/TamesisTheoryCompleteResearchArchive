# ATTEMPT — a direct bounded-variation/Cauchy-criterion route to `(H-ces)`,
# bypassing the classical Tauberian theorem entirely (`H-CES-DIRECT-ATTEMPT`)

**Wave 28, front (a), `DISC-DEC-131`.** Ninth consecutive wave in this exact
sub-lineage (waves 20-27, eight waves, already attacked `(U1)`/`(U2)`
through five distinct techniques plus a dedicated `(U2)` boundary-layer
angle; this is the first to target `(H-ces)` — Cesàro-`(C,1)` convergence of
the running average `A(y)/(x+y)` — directly, per the explicit recommendation
of wave 26 (`DISC-DEC-125`) and its referee's Finding 2.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process — pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lema Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.** Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no
result from Tree A is cited anywhere below, even in hedged language, as
evidence for anything claimed here.

Reserved seed range for this front: `20260940000-20260940999`.
Grep-confirmed BEFORE any use (`grep -rn "20260940" 05_DISCOVERY_LAB/`) to
appear only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-131` reservation line
(re-confirmed again at the end of this front, Sec 11). **No randomness was
needed anywhere in this front** — every computation below is exact symbolic
algebra (`sympy`) or deterministic arbitrary-precision quadrature (`mpmath`,
fixed evaluation strategy, explicit de-stiffening substitutions, no
sampling), exactly as every direct ancestor front in this sub-lineage
reports for itself. The reserved range remains entirely unused.

---

## VERDICT UP FRONT

**Tier: a genuine, verified REDUCTION of `(H-ces)` (and, by an already-known
corollary, of `(U1)` itself) down to exactly the SAME two named, open
hypotheses this lineage has carried since waves 25/26 — `(C')` and `(U)` —
via a NEW argument that is simpler than, and entirely bypasses, the
classical Tauberian theorem this whole sub-lineage has been building toward
since wave 25. `(H-ces)` is NOT unconditionally proved (`(C')`/`(U)` remain
open for the real `Φ`), so `H1`/`(U1)`/`(U2)` remain formally OPEN — but the
logical distance from the two standing hypotheses to `(U1)` has been closed
essentially to zero, where wave 26 explicitly flagged this distance as
"not examined... structurally a comparably-hard question." That
speculation is shown here to be false.**

1. **The main new result (Sec 2-3): a bounded-variation/Cauchy-criterion
   argument closes `(H-ces)`, conditional on `(B)`+`(C')`+`(U)` — the exact
   same hypotheses wave 26 already needed for `(OSC-PHI)`, no new hypothesis
   introduced.** The mechanism: wave 26's own derivation of the (already
   unconditionally proved) self-averaging identity `Φ_y(x)-A(y)/(x+y)->0`
   implicitly computes the error `e(y):=Φ_y(x)-A(y)/(x+y)` at rate `O(1/y)`
   — not merely `o(1)` — GIVEN `(C')` and `(U)`. This front's contribution
   is noticing that `d/dy[A(y)/(x+y)] = e(y)/(x+y)`, so an `O(1/y)` bound on
   `e(y)` makes this derivative `O(1/y^2)` — **absolutely integrable** on
   `[Y0,infinity)`. By the elementary Cauchy criterion for improper
   integrals, `A(y)/(x+y)` therefore CONVERGES. This is `(H-ces)`. Verified
   symbolically end-to-end (`s01`), including an explicit closed-form tail
   bound and a fully independent discrete telescoping-sum cross-check
   (`s04`) of the same conclusion via a structurally different route.

2. **Immediate corollary: `(U1)` itself follows, under the same hypotheses,
   WITH AN EXPLICIT `O(1/(x+y))` convergence rate** (Sec 3, `s04` Part 2) —
   not previously stated anywhere in this lineage's record. Combined with
   wave 26's referee's already-established fact ("H-ces" alone is necessary
   AND sufficient for `(U1)` given the unconditional self-averaging bridge,
   `DISC-DEC-125`), this front supplies the missing "how": an actual
   argument that gets `(H-ces)`, not merely the observation that it would
   suffice.

3. **This closes off the entire Tauberian apparatus as unnecessary
   machinery for `(U1)` specifically** (Sec 6) — no oscillation bound on
   `Φ` (`(H-osc)`/`(OSC-PHI)`, wave 26's own central technical result) and
   no "hypotheses transfer to a two-variable PDE setting" check (wave 26
   Sec 5) are needed at all; the Cauchy-criterion argument is a one-line
   fact about the single real-valued function `y -> A(y)/(x+y)` at fixed
   `x`, with no PDE-slice subtlety to resolve in the first place. This
   sharpens wave 26 referee's Finding 2 from "logically unnecessary as a
   stepping stone" to "there is a strictly simpler stepping stone that
   actually closes the gap."

4. **Sharpness, established via two elementary worked examples (Sec 4,
   `s02`):** the `O(1/z)` rate this front needs is not a wasteful safety
   margin. A POSITIVE example (`e(y)=D/(x+y)` exactly) confirms the
   mechanism achieves convergence with the derived rate met with equality.
   A companion SHARPNESS example (`h(y)=sin(log(log(x+y+3)))`) exhibits a
   self-averaging error that is still `o(1)` (consistent with the
   unconditional identity of record) but only `O(1/log z)`, and is shown,
   via an EXPLICIT CONSTRUCTIVE subsequence (not sampling), to fail to
   converge — locating the boundary of what works precisely, and connecting
   directly to wave 26's own `sin(log(1+t))` counter-example methodology.

5. **A genuinely new numerical test of `(U)`+`(C')` combined (Sec 5,
   `s03`):** all three of wave 26's own `(U)`-tests (and their referee's
   independent reproductions) varied `h/y` at a SINGLE FIXED test function
   `f`. This front's argument needs the closed form's `O(1/z^2)` remainder
   to stay uniformly bounded not just across `h/y` but ALSO as `f` ranges
   over a family sharing a common `(B)`+`(C')`-type bound — simulating how
   `{Φ_t}_{t∈[0,y]}` would need to behave. A fresh raw-kernel implementation
   (independently re-derived, sanity-checked against the predecessor's
   published cross-check value to `~2.1e-12` absolute before trusting
   anything new) tests a `6×6` grid of `h/y` ratio × oscillation phase: the
   remainder constant stays bounded and shows no trend toward blowup across
   the family dimension. **Support, not proof** — see Sec 7 for the precise
   scope of what this test does and does not establish.

6. **Route (c) of the mandate (a genuine counter-example specific to the
   real `Φ`) was actively searched for and NOT found** — if anything, this
   front's central argument points the opposite direction (toward `(H-ces)`
   holding, conditionally). No claim is made that `(H-ces)` fails for the
   real system; the sharpness examples of Sec 4 are elementary/abstract, in
   exactly the same scope-disciplined sense as wave 26's own
   `sin(log(1+t))` example.

7. **What remains open (Sec 7), stated without hedging:** `(C')` (uniform-
   in-`t` Lipschitz regularity of `Φ_t(·)`) and `(U)` (uniform `O(1/z^2)`
   closed-form remainder, now needed uniformly across the family `{Φ_t}`,
   not merely across `h/y`) are NOT independently proved for the actual
   `Φ`/`Ψ` of this system — same status as wave 25/26 left them. A genuine
   direct numerical test on the REAL `Φ` (via a full `(P,Q)`-family series
   solver or a full spatial-profile Volterra solve) is explicitly OUT OF
   SCOPE here, for the same well-documented reasons wave 25 cited for not
   building one (Sec 1.2 there) — disclosed, not hidden (Sec 7 below).

**`H1`/`(U1)`/`(U2)` remain ABERTO/OPEN**, because `(C')` and `(U)` remain
open. `φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law
of record are all untouched and unaffected by anything in this document.
`H2` is untouched (out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself. No `git` command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `DISC-DEC-131`'s full
entry in `DECISION_LEDGER.yaml` (this front's mandate and portfolio
justification, including the explicit statement that `(H-ces)` is targeted
directly "para o Phi exato do sistema (não o contraexemplo sin(log(1+t))
usado pela onda 26 apenas para provar independência lógica)"); the full,
immediate-predecessor `tauberian_oscillation_bound_attempt/ATTEMPT.md`
(wave 26, front c) — its `T0`/`T1`/`T2` decomposition, its `(H-osc)`/
`(OSC-PHI)` result, its precise statement of hypotheses `(C')` and `(U)`,
its `sin(log(1+t))` counter-example (Sec 6), and its own dated referee note
(Achado F2) proving `(H-ces)` necessary AND sufficient for `(U1)` given the
unconditional self-averaging bridge; both `adversarial/REFEREE_REPORT.md`
files (`h1_translation_structure_attempt`'s and
`tauberian_oscillation_bound_attempt`'s) in full, including every Finding
and the precise wording of Finding 1/Finding 2 in each; and the full
`h1_translation_structure_attempt/ATTEMPT.md` (wave 25) — the closed-form
kernel asymptotic, the exact `(VOLTERRA-Phi)` system, and the self-averaging
identity's own derivation (Sec 6.1), which this front's Sec 2 builds on
directly. `PROOF_DEPENDENCY_MAP.md`'s `PLATRESUM` node addenda for
`DISC-DEC-122`, `DISC-DEC-125`, and `DISC-DEC-127` were read in full for the
orchestrating session's own summaries and the portfolio-survey context.

**No `.py` file from any ancestor front, or from any referee, was opened,
read, or imported at any point** — matching this exact sub-lineage's own
established discipline. Every script in this directory (`s01`-`s04`) was
written fresh from the mathematical content of the prose cited above.

**The exact inputs this front works from** (restated for
self-containedness, cited not re-derived except where marked NEW below —
identical to wave 26's own Sec 0, itself identical to wave 25's):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Closed Volterra-in-y system (cited, record fact):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    g_y(x) := e^{-y/eps},   Phi_y := Phi(.,y) in X := C_b([0,infinity))

Standing hypothesis (B): Phi, Psi bounded, M_Phi := sup|Phi| (used
  throughout this lineage).

THE CLOSED-FORM ASYMPTOTIC (DISC-DEC-122, cited, pointwise-in-f, conditional
on (B) plus an auxiliary Lipschitz-type regularity hypothesis (C) on f):
  K(y,t) f(x) = [f(x) - e^{-h/eps} f(x+h)] / z + O(1/z^2),  h:=y-t, z:=x+y

The self-averaging identity (DISC-DEC-122, PROVED unconditionally given
(B),(C), cited, corrected framing per wave-25-referee's Finding 1):
  Phi_y(x) - A(y)/(x+y) -> 0,   A(y):=int_0^y Phi_t(x) dt
  <=> [(U1) is equivalent to]: A(y)/(x+y) itself converges (Cesaro-(C,1)).

Hypotheses named by wave 26 (DISC-DEC-123/125, cited, NOT weakened or
strengthened by this front -- reused verbatim):
  (C'): a Lipschitz-type regularity bound on Phi_t(.), UNIFORM in t --
    strictly stronger than wave 25's single-fixed-f (C).
  (U): the closed-form kernel's O(1/z^2) remainder is uniform over the FULL
    range h in [0,y], including h/y->1 -- numerically tested by wave 26
    (three sweeps) and by its referee (independent reproduction), for FIXED
    test functions f; NOT independently proved analytically.

Wave 26's own oscillation bound (cited, NOT used by this front's main
argument -- see Sec 6 for why it becomes unnecessary):
  |Phi_{y2}(x) - Phi_{y1}(x)| <= C1(x,eps)*delta + C2(x,eps)/y1   (OSC-PHI)

Wave-26-referee's Finding 2 (DISC-DEC-125, cited, used directly in Sec 3):
  Given the unconditional self-averaging bridge, (H-ces) alone is NECESSARY
  AND SUFFICIENT for (U1), via the elementary fact that two sequences
  differing by o(1) converge to the same limit iff either one does.
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout; nothing
outside this front's own new subdirectory was written to.

---

## 1. Precise restatement of the target

Per the mandate: prove, for the system's actual `Φ` (not a toy example),

```
(H-ces):  A(y)/(x+y) --> L(x)   as y -> infinity,   Cesaro-(C,1) convergence,
          A(y) := int_0^y Phi_t(x) dt
```

in the same `(x,y)` regime wave 26's own `(OSC-PHI)` targets (`y1,y2`
large, `x>=0` fixed or ranging over a compact set for local uniformity).

Per wave 26's own referee (`DISC-DEC-125`, Achado F2, restated in Sec 0
above): **given the already-unconditionally-proved self-averaging bridge**
`Φ_y(x)-A(y)/(x+y)->0`, `(H-ces)` is logically equivalent (necessary AND
sufficient) to `(U1)` itself, via elementary triangle-inequality reasoning.
So proving `(H-ces)` — this front's actual mandate — is, modulo that already
-established equivalence, the same task as proving `(U1)` directly. This
front does not re-derive that equivalence (it is cited, spot-checked for
plausibility by inspection, and matches standard real-analysis: two
sequences differing by `o(1)` converge to the same limit iff either one
does) — it derives an actual PROOF of `(H-ces)`, conditional on named
hypotheses, closing the "how" that the equivalence alone left open.

---

## 2. The main new argument: a quantitative self-averaging-error bound, and
a bounded-variation/Cauchy-criterion closure of `(H-ces)`

Full symbolic verification: `s01_bounded_variation_derivation_symbolic.py`/
`.log`.

### 2.1 A quantitative (not merely `o(1)`) bound on the self-averaging error

Define `e(y) := Φ_y(x) - A(y)/(x+y)`, `z:=x+y`. Substitute the closed-form
kernel (Sec 0, cited) into `(VOLTERRA-Phi)`, applied POINTWISE in `t` for
each `t∈[0,y]` (`f:=Φ_t(.)`, needing hypothesis `(C)` applied to the WHOLE
family `{Φ_t}_{t∈[0,y]}` with a `t`-UNIFORM constant — this is exactly
hypothesis `(C')`, wave 26's own strengthening, reused here unchanged), and
integrate over `t∈[0,y]` — **exact rearrangement of the already-established
`(VOLTERRA-Phi)` equation, no new approximation beyond the cited closed
form**:

```
Phi_y(x) = g_y(x) + (1/z)A(y) - (1/z)J(y) + E_W(y)
  J(y)   := int_0^y e^{-(y-t)/eps} Phi_t(x+y-t) dt   [substituting h=y-t]
  E_W(y) := int_0^y rho(y,t,x;Phi_t) dt   [the integrated Watson's-lemma
                                            remainder, |rho|<=D(x,eps)/z^2
                                            pointwise in t, per (U)+(C')]

=> e(y) = g_y(x) - J(y)/z + E_W(y)
```

**Three elementary bounds, each verified fresh (`s01` Checks 2 and 4):**

- `|g_y(x)| = e^{-y/eps}` — exact, trivial.
- `|J(y)/z| <= M_Phi*eps/z` — by `(B)` alone (the extremal case
  `Phi_t ≡ M_Phi` evaluates `J(y)` EXACTLY to `M_Phi*eps*(1-e^{-y/eps})
  <= M_Phi*eps`, `s01` Check 4(a); a concrete non-constant example
  `Phi_t(u):=M_Phi*cos(t)/(1+u)` confirms the SAME bound applies via a
  pointwise absolute-value majorant, `s01` Check 4(b) — the mechanism is
  general, illustrated concretely, not merely asserted for one case).
- `|E_W(y)| <= y*D(x,eps)/z^2 <= D(x,eps)/z` — the second inequality using
  `y <= z` for `x>=0` (`s01` Check 2, symbolic + a 64-point numeric sweep,
  with one self-caught tolerance bug, Sec 8 below).

**Assembling (`s01` Check 5), for `y` large enough that `e^{-y/eps} <= 1/z`
(true eventually — exponential decay beats any fixed power of `1/z`):**

```
|e(y)|  <=  C(x,eps) / z,      C(x,eps) := 1 + M_Phi*eps + D(x,eps)     (QUANT-E)
```

**This is the front's key new ingredient**: not merely `e(y)->0` (already
known, wave 25) but an EXPLICIT, UNIFORM `O(1/z)` RATE, under EXACTLY the
same hypotheses `(C')`,`(U)` wave 26 already needed for `(OSC-PHI)` — no
new hypothesis is introduced anywhere in this derivation.

### 2.2 The bounded-variation / Cauchy-criterion closure

**Exact algebraic identity** (`s01` Check 1, quotient rule, verified via
sympy with `A` an abstract `Function` and `A'(y)` identified with
`Φ_y(x)`):

```
d/dy[ A(y)/(x+y) ]  =  [Phi_y(x)*(x+y) - A(y)] / (x+y)^2  =  e(y) / (x+y)
```

Combining with `(QUANT-E)`:

```
| d/dy[ A(y)/(x+y) ] |  <=  C(x,eps) / (x+y)^2      for y >= Y0(x,eps)
```

**This is ABSOLUTELY INTEGRABLE on `[Y0,infinity)`** — verified via an
EXACT closed-form tail (`s01` Check 3, re-derived independently again in
`s04` Part 1):

```
int_Y0^infinity  C(x,eps)/(x+y)^2  dy  =  C(x,eps)/(x+Y0)     <  infinity
```

**By the Cauchy criterion for improper integrals** (standard: if
`h:[Y0,infinity)->R` is `C^1` with `int_{Y0}^infinity |h'(y)| dy < infinity`,
then `h(Y2)-h(Y1) = int_{Y1}^{Y2} h'(y)dy -> 0` as `Y1,Y2->infinity`, so
`{h(Y)}` is Cauchy and converges), `h(y):=A(y)/(x+y)` converges to a finite
limit `L(x)` as `y->infinity`. **This is `(H-ces)`, established conditional
on `(B)`, `(C')`, `(U)` — this front's main result.**

*(A mild, standard, essentially-free regularity fact this argument uses:
`Φ_t(x)` continuous in `t`, needed for `A'(y)=Φ_y(x)` via the fundamental
theorem of calculus — implicit in this whole lineage's treatment of `Φ` as
a genuine PDE-slice solution, not separately flagged as a distinct
hypothesis by any ancestor front either.)*

### 2.3 A fully independent cross-check: discrete telescoping sum

Full verification: `s04_explicit_asymptotic_and_telescoping.py`/`.log`
Part 3. Rather than trust the continuous improper-integral argument alone,
this front verifies the SAME conclusion via a structurally DIFFERENT route:
partition `[Y0,infinity)` geometrically, `Y_n:=Y0*2^n`. The mean-value-type
bound on each sub-interval, `|h(Y_{n+1})-h(Y_n)| <= C*(1/(x+Y_n) -
1/(x+Y_{n+1}))`, TELESCOPES EXACTLY (`sympy` `Sum`, closed form, confirmed):

```
sum_{n=0}^{N-1} |h(Y_{n+1})-h(Y_n)|  <=  C*(1/(x+Y0) - 1/(x+Y0*2^N))  -->  C/(x+Y0)
```

as `N->infinity` — i.e. `{h(Y_n)}` is Cauchy by the standard "absolutely
convergent increments" criterion for series, independent of the continuous
integral argument. Confirmed numerically on the concrete `D/(x+y)` example
of Sec 4 (`x=1,D=2,Y0=1`): the running sum of 11 successive increments
reaches `0.999024` against a predicted total of exactly `1.0` — visibly
converging to the predicted bound. Two independent arguments, agreeing.

---

## 3. Consequence: `(U1)` itself, with an explicit convergence rate

Full symbolic derivation: `s04_explicit_asymptotic_and_telescoping.py`/
`.log` Parts 1-2.

**Step 1 — explicit rate for the Cesàro mean.** Since `h(y)=A(y)/(x+y)`
has `h'` bounded by `C(x,eps)/(x+y)^2` for `y>=Y0`, the SAME exact tail
identity as Sec 2.2 gives, for every `y>=Y0`:

```
|L(x) - A(y)/(x+y)|  <=  int_y^infinity C(x,eps)/(x+y')^2 dy'  =  C(x,eps)/(x+y)
```

i.e. `A(y)/(x+y) = L(x) + O(1/(x+y))` — an EXPLICIT rate, not merely
eventual convergence. Cross-checked against the exact `D/(x+y)` worked
example of Sec 4 Part A, where the bound is met WITH EQUALITY (`s04`,
"saturates ... with equality" check) — confirming the derived rate is not
a wasteful over-estimate in that case.

**Step 2 — the same rate transfers to `Φ_y(x)` itself.** Since
`Φ_y(x) = e(y) + A(y)/(x+y)`, and both `|e(y)|<=C(x,eps)/z`
(`(QUANT-E)`, Sec 2.1) and `|A(y)/(x+y)-L(x)|<=C(x,eps)/z` (Step 1 above),
the triangle inequality (verified symbolically, `s04` Part 2) gives:

```
Phi_y(x)  =  L(x)  +  O(1/(x+y))                                    (RATE)
```

**This is `(U1)` itself** — `Φ_y(x)` converges to `L(x)` as `y->infinity`,
at a fixed `x` — **conditional on `(B)`, `(C')`, `(U)`**, WITH an explicit
convergence rate not previously stated anywhere in this lineage's record.

**Local uniformity in `x`** (needed for the full statement of `(U1)`, which
requires locally-uniform-in-`x` convergence, not merely pointwise
convergence at each fixed `x`): this front does NOT re-derive wave 26's own
Sec 5.2 finding, but inherits it directly by citation — every constant
entering `(QUANT-E)` and hence `(RATE)` is of the same `O(1/z1)`/`O(1/z2)`
type wave 26 Sec 5.2 already showed is automatically non-increasing in `x`
for `x>=0` (since `z=x+y>=y`), GIVEN `(C')` and `(U)` themselves hold
uniformly in `x`. This inheritance is structurally direct: `M_Phi`
(hypothesis `(B)`) is a global, `x`-independent bound; `D(x,eps)` carries
the same `x`-uniformity caveat wave 26 already flagged (spot-checked at
`x=0,3` only, not exhaustively proved) — no NEW `x`-uniformity concern is
introduced by this front's argument beyond what wave 26 already named.

---

## 4. Sharpness of the `O(1/z)` threshold: two worked examples

Full symbolic + numeric verification: `s02_cauchy_criterion_worked_
examples.py`/`.log`. Both examples are ELEMENTARY/ABSTRACT — exactly the
same scope discipline wave 26's own `sin(log(1+t))` counter-example uses
(a toy function used to test a LOGICAL fact, not a claim about the actual
`Φ`). No claim is made that either example describes the real system.

### 4.1 Positive example: the `O(1/z)` rate genuinely suffices

`e(y):=D/(x+y)` exactly (concretely, `x=1,D=2,Y0=1,h(Y0)=0.3`): the closed
form `h(y)=h(Y0)-D/(x+y)+D/(x+Y0)` (`sympy`, exact) is confirmed, via an
INDEPENDENT `mpmath` quadrature of `h'(y)=D/(x+y)^2` (not the closed-form
antiderivative — genuinely re-integrating from scratch), to match the
closed form to `<10^-30` absolute at every tested `Y` from `2` to `10^7`,
and to approach the predicted limit `L=1.3` (gap `2×10^-7` at `Y=10^7`).
The corresponding `Φ_y(x):=h(y)+e(y)` converges to the SAME `L`, confirming
end-to-end consistency of the mechanism (Sec 2's argument, applied to a
concrete instance, produces the predicted convergent behavior).

### 4.2 Sharpness example: `O(1/log z)` is NOT enough

`h(y):=sin(log(log(x+y+3)))`. Symbolically (`sympy`): `h'(y) =
cos(log(log(w)))/(w*log(w))`, `w:=x+y+3`, so `e(y):=z*h'(y) ~
cos(log(log(w)))/log(w)`, satisfying `|e(y)|<=1/log(w)->0` — **`e(y)` IS
`o(1)`, consistent with the already-unconditionally-proved self-averaging
identity** — but `[1/log(w)]/[1/w] -> infinity` (`sympy` `limit`,
confirmed): `e(y)` is STRICTLY WEAKER than the `O(1/z)` rate Sec 2 derives.
The antiderivative of the governing majorant `1/(w*log(w))` is
`log(log(w))` (`sympy`, exact), which **diverges** as `w->infinity` —
`h'` is NOT absolutely integrable.

**`h(y)` is shown, via an EXPLICIT CONSTRUCTIVE subsequence (not sampling),
to fail to converge**: for any target `v∈{-1,0,+1}`, choosing
`θ=asin(v)+2πk` (or the supplementary angle) and `y_k:=e^{e^θ}-3` gives
`h(y_k)=sin(θ+2πk)=v` EXACTLY, for `k=0,1,2,3` — `y_k` growing by more than
`10^100`-fold between consecutive `k` (`mpmath`, `dps=50`, confirmed exactly
to `<10^-30`) — so `h` keeps hitting `-1`, `0`, and `+1` exactly,
arbitrarily far out; a convergent bounded sequence cannot do this.

> **[Correção, 2026-08-29 — referee hostil, wave 28 `H-CES-DIRECT-
> ATTEMPT`]** "para `k=0,1,2,3`" acima é impreciso para o alvo `v=0`: com
> `θ=0` (a escolha de `asin(0)`) e `x=1`, `k=0` dá `y_0=e^{e^0}-3-x=e-4
> \approx-1{,}28<0` — uma violação de domínio (`y` deve ser `\ge0`), não
> detectada nem pela própria frente nem pelo seu script `s02` (que também
> não guarda contra isso). A conclusão de não-convergência em si **não é
> afetada**: `k=1,2,3,\ldots` já bastam para exibir a subsequência
> explícita atingindo `-1`, `0`, `+1` arbitrariamente longe, exatamente
> como o argumento requer — apenas o índice inicial `k=0` deveria ser
> omitido para o alvo `v=0` especificamente (os alvos `v=\pm1` não sofrem
> desta ressalva, pois seus `θ` de partida são estritamente positivos).
> Achado de severidade BAIXA, puramente cosmético; confirmado pelo
> referee hostil e reconfirmado por esta sessão. Ver
> `adversarial/REFEREE_REPORT.md`.

**Interpretation**: the `O(1/z)` threshold this front's Sec 2 derives is
not an arbitrary safety margin — weakening it even to `O(1/log z)` (still
strictly stronger than bare `o(1)`) already breaks the Cauchy-criterion
argument. This locates, precisely, how much room hypotheses `(C')`/`(U)`
need to leave: NOT "any decay rate," but specifically integrability of
`e(y)/z` — which `O(1/z)` gives with room to spare (even `O(1/(z\log z))`
would still work, since `\int dz/(z^2\log z)` converges), but `O(1/\log z)`
does not.

---

## 5. Numerical stress-test of `(U)`+`(C')` combined: a family-uniformity
grid on the real kernel definitions

Full log: `s03_kernel_family_uniformity_stress_test.py`/`.log`. Fresh,
from-scratch `mpmath` re-implementation of the RAW kernel
`K(y,t)=M_y∘K_A^raw(y,t)+K_B(y-t)` via the single-integral reduction of
`K_A^raw` (an identity independently re-derived and numerically
cross-checked TWICE already in this lineage's record — wave 25 Sec 2.4, and
its referee's `adv01` Check 3 — reused here as a cited, derived FORMULA,
not the closed-form ASYMPTOTIC this front's own argument is trying to
support; using it is an exact change of variables on the raw operator
definitions, not circular). De-stiffened via the substitution `u=v/z` for
the inner integral (established methodology in this sub-lineage,
re-implemented fresh).

**Sanity check first** (mandatory discipline): reproduces
`h1_translation_structure_attempt`'s own published Sec 5.4 cross-check
value (`x=0,ε=0.1,f=1/(1+x),h=y/2,y=10`: published `z·K(y,t)f(0)=
0.9156333394`) — this front's independent implementation gives
`0.915633339398`, agreeing to `~2.1×10^-12` absolute — confirms the fresh
implementation before trusting anything new.

**The new test.** All three of wave 26's own `(U)`-tests (`s02`/`s02b`/
`s02c` there, and their referee's independent reproductions) held `f`
FIXED and swept `h/y`. This front's Sec 2 argument needs the remainder
constant `D(x,eps)` to be uniform not just across `h/y` but across the
WHOLE FAMILY `{Φ_t}_{t∈[0,y]}` (via hypothesis `(C')`) — a dimension no
ancestor test varied. This script tests a `6×6` grid: `h/y` ratio
`∈{0.002,0.02,0.1,0.5,0.9,0.98}` × family member `f_k(u):=0.7·cos(0.3u+k)`
for phase `k∈{0,π/4,π/2,3π/4,π,5π/4}` — a RIGID family sharing an IDENTICAL
sup-norm bound (`0.7`) and Lipschitz constant (`0.21`) for every `k`,
simulating `Φ_t`'s shape varying with `t` under a fixed `(B)`+`(C')`
envelope. `x=0,ε=0.5,y=100,z=100`.

**Result**: `max|z²·remainder|=0.4225`, `min=0.0336` across the full
`36`-point grid — bounded, with **no trend toward blowup** as the family
member (phase `k`) varies at fixed `h/y`. The remainder stabilizes quickly
in `h/y` (values at ratios `0.1,0.5,0.9,0.98` are numerically identical to
6 significant figures — matching wave 26's own finding that the closed
form is `h`-insensitive once `h` exceeds a few multiples of `ε`), and the
phase-spread at each fixed ratio (`≤0.757`, same order of magnitude as the
values themselves, not growing) shows no sign that varying the family
member destabilizes the bound.

**Scope of this result, stated precisely**: this is numerical SUPPORT for
`(U)`+`(C')` holding uniformly across a Lipschitz-bounded family of test
functions, extending wave 26's own tests into the one dimension they did
not probe. It is **NOT** a test on the actual, evolving `Φ_t` of the real
system (that would require a full spatial-profile Volterra solve or a
`(P,Q)`-family series solver — Sec 7 explains why this is out of scope
here, exactly as wave 25 Sec 1.2 explains for its own front), and it is
**NOT** a proof that `D(x,eps)` is uniformly bounded for ALL possible
`(B)`+`(C')`-admissible families (only this one rigid, deliberately simple
family was tested).

---

## 6. Why this bypasses the classical Tauberian theorem entirely

Wave 25 introduced, and wave 26 built on, a route toward `(U1)` via the
classical continuous Tauberian theorem: `(H-bdd)`+`(H-ces)`+`(H-osc)` (three
hypotheses) plus a "hypotheses transfer to the PDE-slice setting" check
(wave 26 Sec 5). Wave 26's own referee (Finding 2, `DISC-DEC-125`) already
observed that, GIVEN the self-averaging bridge, `(H-ces)` alone is
necessary and sufficient — making `(H-osc)`/`(OSC-PHI)` logically
unnecessary as a stepping stone. **This front supplies the missing piece
that makes that observation actionable**: an actual argument for
`(H-ces)`, which (Sec 2) needs neither `(H-osc)` nor any "hypotheses
transfer" check — the Cauchy-criterion argument is a one-line real-analysis
fact about the single function `y -> A(y)/(x+y)` at fixed `x`, with the
abstract-function-transfer question (wave 26 Sec 5.1) never even arising,
because nothing about the classical Tauberian theorem's own proof machinery
is invoked at all. **The entire Tauberian apparatus this sub-lineage has
built since wave 25 — `(OSC-PHI)`, its two supporting hypotheses framed as
enabling a THREE-hypothesis classical theorem, and the abstract-transfer
check — turns out to be unnecessary for closing `(U1)` via this specific
self-averaging bridge.** `(OSC-PHI)` remains correct and interesting as an
independent fact about `K(y,t)` (not invalidated by anything here), but is
not on the critical path to `(U1)` any more than wave 26's referee already
suspected.

---

## 7. What did NOT close, precisely

1. **`(H-ces)`/`(U1)`/`(U2)`/`H1` are not unconditionally closed.** The
   bounded-variation/Cauchy-criterion argument (Sec 2-3) is a genuine,
   fully-verified-conditional-on-named-hypotheses proof — not an
   unconditional one.
2. **Hypothesis `(C')`** (Lipschitz-type regularity of `Φ_t(·)`, uniform in
   `t`) **is not independently proved** for the actual `Φ` of this system —
   inherited unchanged from wave 26, neither strengthened nor weakened by
   this front.
3. **Hypothesis `(U)`, now needed in a slightly sharper form** (uniform not
   just across `h/y` but across the family `{Φ_t}`) **is not independently
   proved analytically.** Sec 5's numerical test is genuine new support, on
   a Lipschitz-bounded family of test functions — but not a test on the
   real, evolving `Φ_t`, and not exhaustive over all admissible families.
4. **No direct numerical test on the real physical `Φ` was performed.**
   Building either a fresh `(P,Q)`-family series solver, or a full
   spatial-profile Volterra solver (needed because `Φ_t` is an ELEMENT OF
   `C_b([0,infinity))`, not a scalar — evaluating `K_A^raw`'s inner
   integral at a specific `t` genuinely requires `Φ_t` as a function of a
   continuous spatial variable, not merely its value at one fixed `x`),
   is a substantial undertaking this front judges out of scope for the same
   reasons wave 25 Sec 1.2 gives for its own front (index-bug and
   precision-vs-truncation risk for a `(P,Q)`-solver; here, additionally,
   the spatial-profile requirement makes even a raw-kernel-based Volterra
   march an `O(N^2)`-kernel-evaluation undertaking with a genuinely new
   engineering problem — representing `Φ_t(·)` as a continuous function,
   not a scalar sequence — not attempted here). **Disclosed explicitly, not
   hidden** — this is the single largest scope limitation of this front,
   and directly explains why "for the system's ACTUAL `Φ`" is honored only
   at the level of (i) reusing the closed-form kernel machinery that IS
   about the actual system (Sec 2's derivation is not about a toy function
   — it directly manipulates the actual `(VOLTERRA-Phi)` equation and the
   actual closed-form kernel), and (ii) a numerical stress-test on the raw
   kernel with `Φ`-like test functions (Sec 5), not (iii) a direct
   numerical measurement of the real `Φ_t`'s own behavior.
5. **Route (c) of the mandate** (a genuine counter-example specific to the
   real `Φ`) **was not found** — this front's search (Sec 4) instead
   located exactly how much slack the sufficient `(C')`+`(U)` hypotheses
   have, via elementary sharpness examples, without evidence that `(H-ces)`
   actually fails for the real system.
6. **`x`-uniformity of `(C')`/`(U)`** is inherited from wave 26's own
   Sec 5.2 spot-check (`x=0,3` only) — not independently extended here.
7. **`H2`, non-perturbative (trans-series) content, `(U2)`**: untouched,
   out of scope, exactly as every ancestor front in this sub-line reports.

**No formula of record is proposed as a replacement for anything.**
`φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of
record are all untouched and unaffected by anything in this document.

---

## 8. Self-caught issues

Two, both caught by this front's OWN scripts failing their own checks on
first run (not by an external referee), both fixed in place, both disclosed
here with the before/after visible in the committed `.py`/`.log` files —
matching this lineage's established honesty convention.

**Issue 1 (`s01`, Check 2 — a tolerance-scale bug, not a mathematical
error).** The first version of the numeric sweep confirming
`y/(x+y)^2 <= 1/(x+y)` for `x>=0` used a fixed ABSOLUTE tolerance
(`1e-15`) in the comparison `lhs <= rhs + tol`. At `x=0` the identity is
EXACT equality (`lhs=rhs=1/y` algebraically), but at small `y` (e.g.
`y=0.001`) the values themselves are `O(1000)`, so float64 rounding in
computing `y/(x+y)**2` versus `1/(x+y)` SEPARATELY produces an absolute
difference of order `1e-13` (`1000.0000000000001` vs `1000.0`) — far above
a `1e-15` ABSOLUTE tolerance, even though the RELATIVE error is `~1e-16`
(exactly float64 machine epsilon, not a real violation). Caught immediately
on the sweep's first run (its own assertion failed, and the printed
"violation" visibly differed from the true value only in the 16th
significant digit — the signature of a tolerance-scale bug). **Fixed** by
switching to a RELATIVE tolerance (`1e-12 * max(|rhs|,1)`), the correct
comparison discipline for a sweep spanning `y` from `0.001` to `50000`
(four orders of magnitude). Re-run is clean (`0` violations across `64`
points). Visible in the committed `s01_bounded_variation_derivation_
symbolic.py`'s inline comment marked as a documented fix.

**Issue 2 (`s03` — a performance bug, not a correctness error, caught
during development before any numbers were trusted).** The first version
of the outer-integral breakpoint helper `_breakpoints(h,eps)` placed one
breakpoint at EVERY multiple of `eps` up to `h` (linear in `h/eps`). At the
sanity-check parameters (`h/eps=50`), a single kernel evaluation took `38`
seconds; at the planned family-uniformity grid's largest `h/eps` (`~196`,
for the `h/y=0.98` row), the full `36`-evaluation grid would have taken on
the order of `20+` minutes and risked timing out mid-run. Caught by timing
the sanity check alone BEFORE launching the full grid (a deliberate check,
not a failed assertion) and recognizing the breakpoint count would not
scale to the planned grid. **Fixed** by replacing the linear breakpoint
list with a GEOMETRIC one (`eps/4, eps/2, eps, 2eps, 4eps, ...`, capped at
`12` points regardless of `h/eps`) — mathematically justified because the
integrand `e^{-h'/eps}·Θ_{h'}(z)` is smooth (no singularities) on `[0,h]`,
so `mp.quad`'s adaptive Gauss-Legendre needs only enough breakpoints to
resolve the exponential decay's SCALE, not one per decay-length. **Fixed
version reproduces the SAME sanity-check value to the SAME precision**
(`0.915633339398`, matching the published `0.9156333394` to `~2.1×10^-12`)
in `3.9` seconds instead of `38` (the exact figure in the committed
`s03_kernel_family_uniformity_stress_test.log`; an earlier, isolated timing
probe of the fix alone measured `3.2`s, consistent within normal run-to-run
variation) — a roughly `10-12×` speedup with no loss of accuracy, confirmed
by direct comparison before running the full grid.
Visible in the committed `s03_kernel_family_uniformity_stress_test.py`'s
inline comment marked as a documented fix, including the "SELF-CAUGHT
PERFORMANCE ISSUE" label.

No other issues were found. In particular: `s02` and `s04` ran cleanly on
their first attempt, with all checks passing (their logs show no failed
assertions at any point).

---

## 9. Scorecard

| claim | status |
|---|---|
| Quantitative bound `\|e(y)\|<=C(x,eps)/(x+y)` (`QUANT-E`) | **DERIVED** (conditional on `(B)`,`(C')`,`(U)` — SAME hypotheses as wave 26, none new), `s01` |
| `d/dy[A(y)/(x+y)] = e(y)/(x+y)` (exact quotient-rule identity) | **PROVED** (exact, symbolic, `s01` Check 1) |
| `d/dy[A(y)/(x+y)]` absolutely integrable on `[Y0,infinity)` | **PROVED** (exact closed-form tail `C/(x+y)`, `s01` Check 3/5) |
| `(H-ces)`: `A(y)/(x+y)` converges (Cauchy criterion) | **CLOSED, conditional on `(B)`,`(C')`,`(U)`** — main result, `s01`+`s04` |
| Independent discrete telescoping-sum cross-check | **CONFIRMS** the continuous argument via a structurally different route, `s04` Part 3 |
| Explicit rate `A(y)/(x+y)=L(x)+O(1/(x+y))` | **DERIVED** (exact tail bound), `s04` Part 1 |
| Explicit rate `Phi_y(x)=L(x)+O(1/(x+y))`, i.e. `(U1)` with a rate | **DERIVED, conditional on `(B)`,`(C')`,`(U)`**, `s04` Part 2 |
| `(U1)` itself (via wave-26-referee's necessary+sufficient bridge) | **CLOSED, conditional on `(B)`,`(C')`,`(U)`** — no new hypothesis beyond wave 26's own |
| Classical Tauberian theorem / `(H-osc)`/`(OSC-PHI)` needed for this route | **NOT NEEDED** — bypassed entirely (Sec 6) |
| Sharpness: `O(1/z)` suffices, positive example | **CONFIRMED** (exact + independent quadrature), `s02` Part A |
| Sharpness: `O(1/log z)` does NOT suffice, constructive counter-example | **CONFIRMED** (explicit subsequence, not sampling), `s02` Part B |
| Fresh raw-kernel implementation, sanity check vs. published value | **CONFIRMED** (`~2.1e-12` abs. agreement), `s03` |
| `(U)`+`(C')` family-uniformity stress test (NEW dimension) | **SUPPORTED numerically** (`6×6` grid, bounded, no blowup trend) — NOT a proof, `s03` |
| Hypothesis `(C')` | **NOT independently proved** (unchanged from wave 26) |
| Hypothesis `(U)`, family-uniform version | **NOT independently proved** (numerically supported, new dimension) |
| Direct numerical test on the real, evolving `Φ_t` | **NOT ATTEMPTED** (explicitly out of scope, Sec 7 item 4) |
| Route (c): counter-example specific to the real `Φ` | **NOT FOUND** — search instead located the sufficient-hypotheses' sharp boundary (Sec 4) |
| `(U1)` (locally-uniform `y→infinity` convergence, operationally: of `Φ`) | **OPEN unconditionally; CLOSED conditional on `(C')`,`(U)`** |
| `(U2)` | **OPEN** (untouched, out of scope) |
| `H1` | **OPEN** (unchanged, since `(C')`,`(U)` remain open) |
| `H2` | **NOT ATTEMPTED** (out of scope) |

`H1` remains ABERTO/OPEN. `φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the
four-term asymptotic law of record are all untouched and unaffected by
anything in this document.

---

## 10. Recommendation for the next wave

This front reduces the ENTIRE remaining gap in the self-averaging/Tauberian
-adjacent sub-lineage (waves 25-28) to exactly two named hypotheses,
`(C')` and `(U)` — with the logical path from them to `(U1)` now fully
closed (Sec 2-3), and the classical Tauberian machinery no longer part of
the critical path at all (Sec 6). **A ninth wave that wants to close `H1`
via this specific route should attack `(C')` and `(U)` directly** — i.e.
either (a) prove a genuine Lipschitz-type regularity bound on `Φ_t(·)`
uniform in `t` from the system's own defining equations (not assumed), or
(b) prove the closed-form kernel's `O(1/z^2)` remainder is uniform in the
sense now needed (across `h/y` AND across the family `{Φ_t}`) analytically,
via an explicit Watson's-lemma remainder bound with a controlled,
`t`-independent constant — rather than attempting yet another angle on
`(H-osc)`, the Tauberian transfer, or the self-averaging identity itself,
all three of which this front's Sec 6 shows are no longer on the critical
path. Alternatively, given this is now the NINTH consecutive wave in this
exact sub-lineage (waves 20-28), the orchestrating session may reasonably
judge — as `DISC-DEC-131`'s own portfolio survey already flagged for a
THIRD candidate not dispatched this wave — that a fundamentally different
angle (e.g. a genuine, scoped, engineering effort at a real-`Φ` numerical
solver, unlocking direct tests of `(C')`/`(U)` rather than further
analytic reduction) is a better use of a tenth wave. Both are legitimate;
this front does not have a basis to prefer one over the other beyond what
is stated here.

---

## 11. Seeds

Reserved range `20260940000-20260940999` per `DISC-DEC-131`. Grep-confirmed
BEFORE any use (`grep -rn "20260940" 05_DISCOVERY_LAB/`): appeared only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-131` reservation line. Re-confirmed
again at the end of this front (same command, same result): still appears
ONLY in that reservation line, and nowhere inside this front's own new
directory. **No randomness was used anywhere in this front** — every
computation is exact symbolic algebra (`sympy`) or deterministic
arbitrary-precision adaptive quadrature (`mpmath`, fixed evaluation
strategy with explicit de-stiffening substitutions and geometric — not
random — breakpoint placement, no sampling) — exactly as every direct
ancestor front in this exact sub-lineage reports for its own reservation.
The reserved range remains entirely unused.

---

## 12. Files

| file | role |
|---|---|
| `s01_bounded_variation_derivation_symbolic.py`/`.log` | the core derivation: quotient-rule identity, the `y/(x+y)^2<=1/(x+y)` inequality, the exact tail-integral identity, the `J(y)` bound (extremal + concrete non-constant example), and assembly of `(QUANT-E)` (Sec 2) — includes one self-caught tolerance bug (Sec 8) |
| `s02_cauchy_criterion_worked_examples.py`/`.log` | two elementary worked examples: a positive `O(1/z)`-rate example (exact closed form + independent `mpmath` quadrature), and a sharpness `O(1/log z)` counter-example (explicit constructive non-convergent subsequence) (Sec 4) |
| `s03_kernel_family_uniformity_stress_test.py`/`.log` | fresh raw-kernel implementation (single-integral reduction of `K_A^raw`, de-stiffened quadrature), sanity-checked against the predecessor's published value, then a `6×6` family-uniformity stress grid testing `(U)`+`(C')` combined for the first time in this lineage (Sec 5) — includes one self-caught performance bug (Sec 8) |
| `s04_explicit_asymptotic_and_telescoping.py`/`.log` | the explicit `O(1/(x+y))` rate for both `A(y)/(x+y)` and `Φ_y(x)` (Sec 3), and an independent discrete telescoping-sum cross-check of the Cauchy-criterion argument (Sec 2.3) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`h_ces_direct_attempt/` subdirectory was written to — every ancestor
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
  `h_ces_direct_attempt/` directory — including the parent
  `tauberian_oscillation_bound_attempt/` directory and its own ancestor
  siblings (`h1_translation_structure_attempt/`, `h1_volterra_attempt/`,
  `h1_post_correction_attempt/`, `h1_energy_estimate_attempt/`,
  `mclust_h2_validity_attempt/`, `h1_u2_boundary_layer_attempt/`), all read
  as required background but never written to.
- No `adversarial/` subdirectory created (a separate hostile referee is
  dispatched later by the orchestrating session, per the mandate, exactly
  as every direct ancestor in this sub-lineage's own `ATTEMPT.md` states for
  itself).
- No `git` command of any kind run.
- No claim of progress on any Millennium Prize Problem appears anywhere in
  this document — `M-CLUST(b)` is, as stated at the top of this document
  and throughout the required reading, a standalone combinatorial/asymptotic
  object, entirely independent of the archive's separate Tree A (`u1/2`)
  line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result,
  finding, or hedge from the Tree A line is cited anywhere in this document
  as evidence for anything claimed here, and no result from this document is
  intended to be read as evidence for anything in Tree A.
- Two self-caught issues (Sec 8, `s01` and `s03`) were found by this
  front's OWN scripts (a failed assertion in `s01`; a deliberate timing
  check in `s03`), fixed in place, and disclosed here with the before/after
  visible in the committed `.py`/`.log` files — neither was found by, or
  required, an external referee.
- No `THEOREM.md`-tier claim of closure is made anywhere in this document.
  Per the mandate's explicit caution: this front does **not** believe it
  has UNCONDITIONALLY closed `(U1)`, and states this plainly and repeatedly
  (VERDICT UP FRONT, Sec 1, Sec 3, Sec 7, Sec 9, Sec 10) — every claim of
  closure in this document is explicitly and consistently qualified as
  "conditional on `(C')` and `(U)`," which themselves remain open.
