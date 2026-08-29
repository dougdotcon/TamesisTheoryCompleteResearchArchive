# ATTEMPT -- resolving the predecessor's "boundary-layer self-healing"
# question: does `(C')` ALONE (without `(C'')`) already suffice to prove
# `(U)`? (`BOUNDARY-LAYER-SELFHEAL-ATTEMPT`)

**Wave 30, front (c), `DISC-DEC-138`.** Eleventh consecutive wave (waves
20-30) in this exact sub-lineage, and the first with a narrowly-scoped
technical target handed down explicitly by its immediate predecessor: not
another architecture for `(H-ces)`/`(U1)`/`H1`, and not a fresh attack on
`(C')` itself (deliberately deferred, per `DISC-DEC-138`'s own mandate,
until a genuinely new resolvent-stability technique appears), but the
ONE precise open question wave 29 front (a) (`CU-DIRECT-PROOF-ATTEMPT`,
`DISC-DEC-136`) left honestly unresolved: **can the "boundary-layer
self-healing" phenomenon it found numerically -- that the AGGREGATE
remainder `E_full` recovers the full `O(1/z^3)` rate even when the
POINTWISE remainder `E(h',z)` provably does not, under mere `(C')` -- be
turned into an actual proof, replacing that front's dependence on the
strictly-stronger hypothesis `(C'')`?**

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process --
pure combinatorial/asymptotic mathematics about a random-permutation-
with-reroutes ensemble. It is a standalone object, entirely independent
of the archive's separate Tree A (`u1/2` / "Lema Aberto") line in
`THEOREM.md`. Nothing here is, or is adjacent to, a Millennium Prize
Problem, and no such claim appears anywhere below.** Per
`PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result from Tree A is
cited anywhere below, even in hedged language, as evidence for anything
claimed here.

Reserved seed range for this front: `20260947000-20260947999`.
Grep-confirmed BEFORE any use (`grep -rn "20260947" 05_DISCOVERY_LAB/`) to
appear only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-138` reservation
line (re-confirmed again at the end of this front, Sec 9). **No
randomness was needed anywhere in this front** -- every computation below
is exact symbolic algebra (`sympy`) or deterministic arbitrary-precision
quadrature (`mpmath`, fixed evaluation strategy, no sampling), exactly as
every direct ancestor front in this sub-lineage reports for itself. The
reserved range remains entirely unused.

---

## VERDICT UP FRONT

**`(U)` is now PROVED conditional on `(B)` + `(C')` ALONE -- `(C'')` is NOT
needed. This resolves the predecessor's open question in the POSITIVE
direction: the "boundary-layer self-healing" phenomenon it found
numerically is genuine, general (not an artifact of its one test
function), and provable via an elementary, fully rigorous argument.**

1. **A clean, self-contained proof that `E_full(z) = O(1/z^3)` using
   ONLY `(C')` (Lipschitz `f`, constant `L1`) -- no assumption whatsoever
   on `f'` beyond the a.e. bound `|f'|<=L1` that Lipschitz continuity
   already implies (Sec 3).** The route is genuinely different from the
   predecessor's own (which differentiates `rho(h',z)` first, via
   `rho(h',z)=int f'(x+h'+u)Q_u(z)du`, then bounds the resulting pointwise
   `E(h',z)` and integrates the sup): this front instead swaps the ORDER
   of the `h'`- and `u`-integrations FIRST (Fubini), reducing the entire
   question to a single clean inequality, `|Gamma_u(h)-Gamma(h)|<=3*L1*u`
   (`Gamma_u(h):=int_0^h e^{-h'/eps}f'(x+h'+u)dh'`), proved via an
   f-VALUES-ONLY closed form (the elementary IBP/FTC identity, valid for
   any Lipschitz -- i.e. absolutely continuous -- `f`, needing no
   assumption on `f'` beyond what Lipschitz `f` already gives) and three
   applications of the triangle inequality against `f`'s own Lipschitz
   bound. Combined with the ALREADY-established fact `int_0^inf u*Q_u(z)
   du = R''(z)/2` (re-derived here independently, matching a claim
   the predecessor front's own `s01`-`s03` scripts never derived --
   though the predecessor's own referee DID derive it independently in
   `adv02_rho_and_E_routes.py` [^r1]) and a NEW, simpler,
   self-contained elementary bound
   `R''(z)<=2/z^3` (via one substitution, `w=s/z`, no ODE
   comparison-function machinery needed), this gives
   `|E_full(z)|<=3*L1/z^3` for EVERY `z>0` -- exactly the rate `(U)`
   needs, with NO dependence on `f'`'s own regularity at all.

2. **This is a genuine strengthening of the predecessor's Theorem, not a
   re-statement of it (Sec 3.4).** Combining this front's new bound with
   the predecessor's ALREADY-established, independently-referee-verified
   `(B)`-only bound on the closed form's "value-only" piece (cited, not
   re-derived -- that piece never needed any regularity of `f` at all)
   gives: `|K(y,t)f(x)-[f(x)-e^{-h/eps}f(x+h)]/z| <= D(x,eps)/z^2`,
   `D(x,eps) := M_Phi*eps*(1+1/eps^2+1/eps)+2*M_Phi/eps + 3*L1*(1+eps)/eps`
   -- IDENTICAL in form to the predecessor's own assembled theorem, with
   `L2` (the `(C'')`-only Lipschitz-`f'` constant) replaced throughout by
   `L1` (the `(C')` Lipschitz-`f` constant). **`(U)` is PROVED conditional
   on `(B)`+`(C')` -- exactly the two hypotheses named in this
   sub-lineage's own long-standing record, with no strengthening
   whatsoever.**

3. **Decisive numerical stress-testing, going well beyond the
   predecessor's own single-test-function check, finds zero evidence of
   any failure (Sec 4).** The new bound is confirmed to hold, with
   comfortable margin, on: the predecessor's own published adversarial
   kink (exact reproduction of `z^3|E_full|->0.936`, confirming this
   front's fresh, independently-written implementation before trusting
   it on anything new); a NEW four-simultaneous-kink construction (tests
   whether MULTIPLE kinks present at once can defeat the bound -- they
   cannot, since the bound has no dependence on kink count); and a NEW,
   more severe eight-kink construction with GEOMETRICALLY SHRINKING
   spacing accumulating toward a point (the most adversarial fixed
   construction this front could make numerically tractable, designed
   specifically to stress-test whether a cluster of many kinks at
   many simultaneous scales could defeat the aggregate rate) -- pushed to
   `z=2500`, where the kernel's own resonant window (`~1/z=0.0004`) is
   already smaller than the finest gap in the kink cluster; `z^3|E_full|`
   stabilizes cleanly around `1.5`, well inside the proved bound of `3.0`,
   in every case.

4. **No counter-example was found anywhere, and the analytic proof gives
   a structural reason none should exist**: the core lemma
   (`|Gamma_u(h)-Gamma(h)|<=3*L1*u`) never references the fine structure
   of `f'` at all -- only `f`'s own Lipschitz bound, applied three times
   via the triangle inequality to an f-VALUES-ONLY closed form. Nothing
   about the number, spacing, or accumulation pattern of `f'`'s possible
   discontinuities enters the proof, so no adversarial construction
   built from a Lipschitz `f` (however pathological its derivative) can
   defeat it. This is a genuinely different (and, on this specific
   question, decisive) resolution from the predecessor's honest
   "left open" verdict.

**`(H-ces)`, `(U1)`, `(U2)`, `H1` remain formally OPEN** -- `(C')` itself
is still not proved for the real `Phi`/`Psi` of this system (deliberately
NOT re-attacked here, per this front's own narrow mandate). But the
logical distance from the sub-lineage's TWO standing named hypotheses to
`(U1)` is now strictly SHORTER than before this front: `(U)` no longer
needs the auxiliary strengthening `(C'')` the immediately-preceding front
introduced -- it follows from `(C')` exactly as literally named in this
lineage's own decade-long record, with no strengthening at all. `phi_REDB`,
`Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law of record
are all untouched and unaffected by anything in this document. `H2` is
untouched (out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing.
No `adversarial/` subdirectory created; no referee dispatched by this
front itself, per the mandate. No `git` command run.

---

## 0. Reading discipline and provenance

Read in full, in prose, before any derivation or code, in the exact order
the mandate specifies:

- `.../tauberian_oscillation_bound_attempt/h_ces_direct_attempt/
  cu_direct_proof_attempt/ATTEMPT.md` (wave 29 front (a),
  `CU-DIRECT-PROOF-ATTEMPT`, `DISC-DEC-136`, this front's immediate
  predecessor) in full -- Sec 2 (the rigorous Gordon-type Mills-ratio
  double inequality `(G1)`-`(G3)`), Sec 3 (the proof of `(U)` conditional
  on `(B)`+`(C'')`, the exact decomposition `K(y,t)f(x)=[1+c(z)]K_B(h)f(x)
  +[(1-eps z)/eps]*int_0^h e^{-h'/eps}rho(h',z)dh'`, the definitions of
  `rho(h',z)`, `sigma(z)`, `Q_u(z)`, `E(h',z)`, `E_full`, and the final
  assembled `D(x,eps)`), and CRITICALLY Sec 4 (the sharpness investigation
  this front's entire mandate is built on: 4.1 non-adversarial kink shows
  no degradation; 4.2 adversarially-aligned kink shows genuine POINTWISE
  `O(1/z^2)` degradation, `z^2|E|->0.2208`, confirming `(C'')` is needed
  at the pointwise level of THAT front's specific proof technique; 4.3
  the SAME kink's AGGREGATE `E_full` was found NUMERICALLY to still
  achieve `O(1/z^3)`, `z^3|E_full|->0.936`, WITHOUT `(C'')` -- the
  "boundary-layer self-healing" phenomenon; 4.4 leaves OPEN, precisely,
  whether mere `(C')` suffices via a sharper boundary-layer-aware
  argument).
- `.../cu_direct_proof_attempt/adversarial/REFEREE_REPORT.md` (sibling
  directory) in full -- independently reproduced `z^2|E|->0.2208` and
  `z^3|E_full|->0.936` with fresh code, and separately confirmed the
  pointwise-degradation phenomenon (but NOT a fully clean aggregate
  self-healing signal by `z=500`) on a second, differently-shaped kink
  function (a one-sided ramp) -- explicitly flagged there as
  "suggestive-but-not-fully-resolved," a genuine open loose end this
  front's own Sec 4 numerics (going to larger `z` and to structurally
  different multi-kink constructions) speaks to.
- `.../h1_translation_structure_attempt/ATTEMPT.md` (wave 25,
  grandparent) in full -- the origin of the closed-form kernel `K(y,t)`,
  `K_A^raw`, `K_B`, `M_y` operator definitions, the `Theta_h'(z)=f(x+h')
  R(z)+rho(h',z)` decomposition, and the original (non-rigorous-remainder)
  derivation of the same closed form this whole apparatus targets.
- `PROOF_DEPENDENCY_MAP.md`'s dated addenda under `DISC-DEC-132`
  (integrating wave 28 front (a), `H-CES-DIRECT-ATTEMPT`) and
  `DISC-DEC-136` (integrating the immediate predecessor,
  `CU-DIRECT-PROOF-ATTEMPT`) -- the orchestrating session's own precise,
  independently-referee-cross-checked record of `(C')`, `(C'')`, `(U)`,
  and this front's exact target, plus `DECISION_LEDGER.yaml`'s own
  `DISC-DEC-138` entry (front (c)'s literal mandate, quoted verbatim in
  Sec 1 below).

**No `.py` file from any ancestor front, or from any referee, was opened,
read, or imported at any point.** Every script in this directory
(`s01`-`s05`) was written fresh from the mathematical content of the
prose cited above -- matching this exact sub-lineage's own established
discipline. Where a script below reproduces a number the predecessor or
its referee already published (Sec 4.1), this is stated explicitly as a
cross-check, computed via a fresh, independently-written implementation.

**The exact target, quoted from `DISC-DEC-138` (Sec 0 of
`DECISION_LEDGER.yaml`, front (c)'s own mandate, re-stated here
verbatim in translation, not paraphrased):**

> Frente (c): o quebra-cabeca de "autocura de camada-limite"
> especificamente -- se um argumento ciente-de-camada-limite sobre o
> resto agregado `E_full` pode provar `(U)` a partir de `(C')` sozinha
> (sem `(C'')`), dado que a peca pontual precisa de `(C'')` mas o
> agregado empiricamente parece nao precisar. ... a questao de
> equivalencia `(C')=(B)` em si (nunca quebrada em 29 ondas) e
> deliberadamente NAO reatacada.

**The real system and hypotheses this front works from** (traced back
through the cited chain, quoted for self-containedness, IDENTICAL to the
predecessor's own Sec 0 -- not re-derived, cited):

```
Closed Volterra-in-y system (h1_volterra_attempt, cited):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
    R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = int_0^inf e^{-u^2/2-ux} du,
      R'=xR-1,  R(0)=sqrt(pi/2)
Standing hypothesis (B): Phi, Psi bounded, M_Phi := sup|Phi|.

(C'): a Lipschitz-type regularity bound on Phi_t(.), UNIFORM in t --
  exists L1 independent of t s.t. |Phi_t(x1)-Phi_t(x2)|<=L1|x1-x2| for
  ALL t>=0, x1,x2>=0.
(C''): [the predecessor's strengthening] Phi_t'(.) is ALSO Lipschitz,
  t-uniform constant L2 (i.e. Phi_t in C^{1,1}, t-uniformly).
(U): the closed-form kernel's O(1/z^2) remainder is uniform over the
  FULL range h in [0,y] AND across the whole family {Phi_t}_{t in [0,y]}
  -- exists D(x,eps), independent of t,h,y, s.t.
    |K(y,t)f(x) - [f(x)-e^{-h/eps}f(x+h)]/z| <= D(x,eps)/z^2,  z:=x+y.

The predecessor's exact decomposition (cu_direct_proof_attempt Sec 3.1,
cited, re-verified there via sympy, NOT re-derived here):
  K(y,t)f(x) = [1+c(z)]*K_B(h)f(x) + [(1-eps*z)/eps] * Efull
  c(z) := (1-eps*z)*R(z)/eps,   sigma(z) := 1-z*R(z)
  Efull := int_0^h e^{-h'/eps} rho(h',z) dh'  -  sigma(z)*int_0^h
             e^{-h'/eps} f'(x+h') dh'   [the SAME quantity, re-expressed
             below (Sec 2) without ever needing f' pointwise]
  rho(h',z) := int_0^inf e^{-u^2/2-uz}[f(x+h'+u)-f(x+h')] du
  E(h',z) := rho(h',z) - sigma(z)*f'(x+h')   [pointwise-in-h' quantity]
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout; nothing
outside this front's own new `boundary_layer_selfheal_attempt/`
subdirectory was written to.

---

## 1. Precise restatement of the target

Per `DISC-DEC-138`, quoted in full above: prove (or decisively refute)
that `(C')` ALONE -- without the predecessor's auxiliary strengthening
`(C'')` -- suffices to prove `(U)`, via an argument on the AGGREGATE
quantity `E_full` that is genuinely aware of the "boundary-layer"
structure the predecessor found numerically (the pointwise-bad `h'`-region
has shrinking width `~O(1/z)`), rather than the predecessor's own
sup-then-integrate strategy (which discards this structure and hence
needs the pointwise bound to already be `O(1/z^3)`, forcing `(C'')`).

The predecessor's Sec 3.2 (the "value-only" piece of the closed form,
i.e. everything in `K(y,t)f(x)` EXCEPT the `Efull` term) is **cited
verbatim, not re-derived** -- it is already established, using `(B)`
alone (no regularity of `f` at all), and already independently
referee-verified (`adv01`/`adv03` in the predecessor's own
`adversarial/` directory). **This front's entire new content is a bound
on `Efull` itself, using `(C')` alone.**

---

## 2. A different starting decomposition: swap the integration order
FIRST, avoid ever invoking `f'(x+h')` pointwise

The predecessor's own route (Sec 3.3 there) first rewrites `rho(h',z)`
via `rho(h',z)=int_0^inf f'(x+h'+u)Q_u(z)du` (`Q_u(z):=e^{-u^2/2-uz}
R(u+z)`, obtained by integrating `rho`'s definition by parts in `u`) and
`E(h',z):=rho(h',z)-sigma(z)f'(x+h')=int_0^inf[f'(x+h'+u)-f'(x+h')]Q_u(z)
du` -- a POINTWISE-in-`h'` quantity that, to be bounded better than the
crude `O(1/z^2)` (`|E(h',z)|<=2*L1*sigma(z)`, valid under `(C')` alone),
needs `f'` ITSELF to be Lipschitz (`(C'')`) so that `|f'(x+h'+u)-
f'(x+h')|<=L2*u`.

**This front's mandate explicitly asks for a genuinely different starting
decomposition that only ever uses `f` (Lipschitz, `(C')`), not a route
that differentiates first.** The key realization: `Efull` itself, as a
SINGLE `h'`-INTEGRATED quantity, can be written in a form that NEVER
needs `f'(x+h')` at a single point -- only the GLOBAL fact that `f` is
absolutely continuous (which `(C')`-Lipschitz `f` already gives, via the
classical fundamental theorem of calculus for absolutely continuous
functions, using its a.e.-defined derivative as an integrand -- a fact
that needs NO further regularity of that a.e.-derivative itself).

### 2.1 The IBP bracket, f-VALUES ONLY

Since `f` is `L1`-Lipschitz (hence absolutely continuous) on `[0,inf)`,
for EVERY `a,b>=0` (not just a.e.): `f(b)-f(a) = int_a^b f'(t)dt`
(classical FTC for AC functions, using the a.e.-defined `f'`). Applying
this with the weight `e^{-h'/eps}` and integrating by parts (`s01` Part 4
verifies this symbolically on a fresh concrete test function):

```
int_0^h e^{-h'/eps} f'(x+h') dh'
  = e^{-h/eps}*f(x+h) - f(x) + (1/eps)*int_0^h e^{-h'/eps}*f(x+h') dh'
```

**valid whenever `f` is Lipschitz -- no assumption on `f'` beyond its
a.e. existence, which Lipschitz `f` already guarantees.** The RHS is
expressed PURELY in terms of `f`-VALUES (plus the already-defined `K_B`
integral) -- call this `Gamma(h)`.

### 2.2 `rho(h',z)` re-derived via `f'`, independently re-checked (`s01`
Part 2)

Since we DO still want to relate `rho` to `f'(x+h'+u)` (to exploit the
kernel's own concentration structure), this front re-derives, fresh, from
scratch, the SAME representation the predecessor used
(`rho(h',z)=int_0^inf f'(x+h'+u)Q_u(z)du`, `Q_u(z):=e^{-u^2/2-uz}
R(u+z)`) via the FTC-for-AC-functions route (`G(h'+u)-G(h')=int_0^u
G'(h'+s)ds`, Fubini/Tonelli swap, and the elementary tail-integral
identity `int_s^inf e^{-u^2/2-uz}du = e^{-s^2/2-sz}R(z+s)`, verified via
a clean substitution `u=s+v`) -- confirmed independently via `s01` Part 2
(TWO representations of `Q_u(z)`, the tail-integral form
`Q_u(z):=int_u^inf e^{-w^2/2-wz}dw` and the `e^{-u^2/2-uz}R(u+z)` form,
shown to have the SAME derivative in `u`, hence the same function). **The
crucial difference from the predecessor's route: this front does NOT
stop here and bound `E(h',z)=int_0^inf[f'(x+h'+u)-f'(x+h')]Q_u(z)du`
pointwise. Instead, `h'`-integration is applied to the WHOLE expression
`rho(h',z)-sigma(z)f'(x+h')` FIRST, and the order of the `h'`- and
`u`-integrations is swapped (Sec 3) -- turning the question into a bound
on `Gamma_u(h)-Gamma(h)` (Sec 2.1's `Gamma`, now with an extra shift
`u`), which is ITSELF re-expressible via the f-VALUES-ONLY closed form of
Sec 2.1, needing no pointwise regularity of `f'` at all.**

---

## 3. THE NEW PROOF: `|E_full(z)| <= 3*L1/z^3` using `(C')` alone

### 3.1 Fubini swap

`E_full(z) = int_0^h e^{-h'/eps}[rho(h',z)-sigma(z)f'(x+h')]dh'`. Using
Sec 2.2's representation of `rho` and absolute integrability
(`|f'(h'+u)-f'(h')|<=2*L1` a.e., `int_0^h e^{-h'/eps}dh' <= eps`,
`int_0^inf Q_u(z)du = sigma(z) < inf` -- an elementary fact, `s01`
implicitly, `int_0^inf u*e^{-u^2/2-uz}du=sigma(z)` from `R'=zR-1` directly
matches `Q_0(z)=R(z)` and the tail-integral definition), Fubini applies:

```
E_full(z) = int_0^inf Q_u(z) * [Gamma_u(h) - Gamma(h)] du
  Gamma_u(h) := int_0^h e^{-h'/eps} f'(h'+u) dh'      (Gamma_0=Gamma)
```

### 3.2 The core lemma: `|Gamma_u(h)-Gamma(h)| <= 3*L1*u`, for ALL `h,u>=0`

Applying Sec 2.1's f-VALUES-ONLY closed form to BOTH `Gamma_u(h)` (with
`f(.+u)` in place of `f`) and `Gamma(h)`, and subtracting:

```
Gamma_u(h)-Gamma(h) = e^{-h/eps}[f(x+h+u)-f(x+h)] - [f(x+u)-f(x)]
                       + (1/eps)*int_0^h e^{-h'/eps}[f(x+h'+u)-f(x+h')]dh'
```

**Every term is a plain DIFFERENCE OF `f`-VALUES, bounded directly by
`(C')`'s Lipschitz constant `L1` -- `|f(a)-b)|<=L1*u` whenever `|a-b|=u`
-- with NO reference to `f'` anywhere in this formula.** Bounding each of
the three terms (`s04` verifies this identity AND the resulting
inequality numerically, on both a smooth and a genuinely kinked `f`):

```
|e^{-h/eps}[f(x+h+u)-f(x+h)]|  <= L1*u        (e^{-h/eps}<=1)
|f(x+u)-f(x)|                   <= L1*u
|(1/eps)*int_0^h e^{-h'/eps}[f(x+h'+u)-f(x+h')]dh'|
   <= (1/eps)*L1*u*int_0^h e^{-h'/eps}dh'  <=  (1/eps)*L1*u*eps  =  L1*u
```

(the LAST bound is `h`-INDEPENDENT: `int_0^h e^{-h'/eps}dh'<=eps` for
EVERY `h>=0`, so the `1/eps` and `eps` cancel EXACTLY -- this is the
step that makes the bound uniform in `h`, matching what `(U)` needs.)

**Total: `|Gamma_u(h)-Gamma(h)| <= 3*L1*u`, for ALL `h,u>=0` -- using
ONLY `(C')`, uniform in `h` (not needing `h` small or bounded).**

### 3.3 Assembling: `int_0^inf u*Q_u(z)du = R''(z)/2 <= 1/z^3`

```
|E_full(z)| <= int_0^inf Q_u(z)*3*L1*u du = 3*L1*int_0^inf u*Q_u(z)du
```

`int_0^inf u*Q_u(z)du = R''(z)/2` -- re-derived here independently (`s01`
Parts 2-3, `s02` numerically) via the tail-integral form `Q_u(z)=
int_u^inf e^{-w^2/2-wz}dw` and a Tonelli order-swap (`int_0^inf u*
int_u^inf g(w)dw du = int_0^inf g(w)*w^2/2 dw`, verified symbolically on
two independent concrete `g`, `s01` Part 3), giving `int_0^inf u*Q_u(z)du
= (1/2)*int_0^inf w^2*e^{-w^2/2-wz}dw = R''(z)/2` directly from `R`'s own
definition. **`R''(z)<=2/z^3` for ALL `z>0`** via one elementary
substitution (`s01` Part 5, `w=s/z`, then `e^{-s^2/(2z^2)}<=1`):
`R''(z)=(1/z^3)*int_0^inf s^2*e^{-s^2/(2z^2)}*e^{-s}ds <= (1/z^3)*
int_0^inf s^2*e^{-s}ds = 2/z^3` -- self-contained, no ODE
comparison-function machinery needed for this specific bound (though `s02`
also confirms it is fully consistent with, and in fact asymptotically
matches, the predecessor's own Gordon-type `(G3)` bound, and independently
re-derives the closed form `R''(z)=(1+z^2)R(z)-z` from `R'=zR-1`, used for
high-precision numerical cross-checking).

```
|E_full(z)|  <=  3*L1 * R''(z)/2  <=  3*L1/z^3,     for EVERY z>0
```

**using ONLY `(C')` -- no assumption on `f'`'s own regularity anywhere.**

### 3.4 Final assembled theorem

Combining with `|1-eps*z|/eps <= (1+eps*z)/eps` and, for `z>=1`,
`1/z^3<=1/z^2` (`s05`, exact symbolic algebra, zero residual):

```
|(1-eps*z)/eps * Efull(z)|  <=  3*L1*(1+eps)/eps / z^2,   for z>=1
```

**Combined with the predecessor's own already-established, already
independently-referee-verified `(B)`-only bound on the closed form's
value-only piece (`cu_direct_proof_attempt/ATTEMPT.md` Sec 3.2, CITED
verbatim, NOT re-derived here -- `D1(x,eps):=M_Phi*eps*(1+1/eps^2+1/eps)
+2*M_Phi/eps`), the FULL closed-form kernel remainder satisfies:**

```
|K(y,t)f(x) - [f(x)-e^{-h/eps}f(x+h)]/z|  <=  D(x,eps)/z^2,   z>=1

D(x,eps) := M_Phi*eps*(1+1/eps^2+1/eps) + 2*M_Phi/eps + 3*L1*(1+eps)/eps
```

**with NO dependence on `h`, `h'`, or `t` -- this IS `(U)`, PROVED
conditional on `(B)`+`(C')` ALONE. `L2` and hypothesis `(C'')` do not
appear anywhere in this theorem or its proof.**

> **[Nota, 2026-08-29 — referee hostil, wave 30
> `BOUNDARY-LAYER-SELFHEAL-ATTEMPT`]** The new `L1`-term above,
> `3*L1*(1+eps)/eps`, carries an extra `1/eps` factor that the
> predecessor's structurally parallel `L2`-term, `L2*(1+eps)`
> (`cu_direct_proof_attempt/ATTEMPT.md` Sec 3.4), does not. The referee
> confirmed this is algebraically correct, not an error: in the
> predecessor's route the `eps`/`1/eps` factors cancel earlier; in this
> front's route the same cancellation already happens INSIDE the Sec 3.2
> core-lemma bound (its third term, `(1/eps)*L1*u*eps=L1*u`), so it is
> not available a second time at this final assembly step. This does
> not affect the theorem's validity or its overall `O(1/eps)` order (the
> cited, unchanged `D1(x,eps)` piece already dominates that order), but
> it does mean this front's new bound is not uniformly tighter than the
> predecessor's old one in every `(L1,L2,eps)` regime -- e.g. as
> `eps->0` with `L1\approx L2`, this front's residual term is
> asymptotically worse by a factor `~1/eps`. Worth noting for any future
> front combining both results (taking the sharper bound when both
> hypotheses happen to hold). See `adversarial/REFEREE_REPORT.md`,
> Nota 3.

**THEOREM (this front).** Given `(B)` and `(C')` (as literally named in
this sub-lineage's own decade-long record, no strengthening), for all
`z=x+y>=1` (`eps` fixed) and UNIFORMLY over `h'in[0,h]`, `h in[0,y]` --
i.e. across the WHOLE family `{Phi_t}_{t in[0,y]}` -- the closed-form
kernel remainder is bounded by `D(x,eps)/z^2` above.

---

## 4. Numerical verification

All numerical claims below are logged with real output (`.log` files,
this front's own new `boundary_layer_selfheal_attempt/` directory).

- **`s01_new_identities_symbolic.py`/`.log`** (`sympy`, exact): five
  independent checks, ALL PASS, zero discrepancy -- (Part 1) `R''(z)=
  (1+z^2)R(z)-z` from `R'=zR-1`; (Part 2) the two representations of
  `Q_u(z)` (tail-integral vs `e^{-u^2/2-uz}R(u+z)`) have the SAME
  derivative in `u`, `-e^{-u^2/2-uz}`, confirmed via a manual
  product-rule construction (avoiding a `sympy` `Subs`-object pitfall
  hit and fixed on first attempt -- Sec 5); (Part 3) the Tonelli
  order-swap identity `int u*(int_u^inf g dw)du = int g*w^2/2 dw`,
  verified on TWO independent concrete `g`; (Part 4) the elementary
  IBP/FTC identity of Sec 2.1, verified on a fresh concrete `phi(hp)=
  hp^2*e^{-hp/3}+cos(hp)`, deliberately different from any ancestor's
  own test function choice; (Part 5) `R''(z)<=2/z^3` via the elementary
  substitution `w=s/z`.
- **`s02_Rpp_bound_numeric.py`/`.log`** (`mpmath`, `dps=40`): `R_direct`
  (raw definition) vs `R_erfcx` (closed form) agree to `>25` digits at 6
  spot points; numerical `d^2/dz^2 R` matches the closed form `(1+z^2)R
  (z)-z` to `<1e-15` relative at 9 `z` values from `0.3` to `10000`;
  `R''(z)<=2/z^3` holds with ZERO violations at all 9 points, and
  `z^3*R''(z)->2.000000` at `z=10000` -- the bound is confirmed
  ASYMPTOTICALLY TIGHT, not a loose over-estimate; `int_0^inf u*Q_u(z)du
  =R''(z)/2` confirmed via a genuinely INDEPENDENT route (direct nested
  quadrature of `Q_u(z)`'s own tail-integral definition, not the closed
  form) at 4 `z` values, relative error `<2e-32`.
- **`s03_Efull_bound_stress_test.py`/`.log`** (`mpmath`, `dps=20`): THE
  decisive end-to-end test, computing `E_full(z)` via the SAME
  f-VALUES-ONLY route the proof uses (never evaluating `f'` anywhere),
  on three test functions of increasing adversarial severity:
  - **(F1)** exact reproduction of the predecessor's own published kink
    (`a0=0.1`, `eps=0.5`, two-sided `|.-a0|` kink, `L1=1.3`):
    `z^3|E_full|` at `z=500` computed here as `0.9363`, matching the
    predecessor's published `0.936` and the referee's independent
    `0.9362995...` to 4+ significant figures -- confirms this front's
    fresh implementation is correct. Bound `3*L1=3.9` respected at
    every one of 5 tested `z` from `10` to `500`.
  - **(F2)** a NEW four-simultaneous-kink construction (`a_i in
    {0.08,0.22,0.55,1.1}`, `L1=1.0`) -- `z^3|E_full|` stabilizes cleanly
    around `0.97-1.00` across `z=10` to `600`; bound `3.0` respected
    throughout, WITH comfortable margin, despite four kinks being
    simultaneously present (not just one, as in every ancestor test).
  - **(F3)** a NEW, more severe eight-kink construction with
    GEOMETRICALLY SHRINKING spacing (`a_i=0.6*0.55^i`, `i=0..7`, gaps
    shrinking from `0.27` down to `0.0075`) accumulating toward `a=0`,
    `L1=1.0` -- the most adversarial FIXED construction this front made
    numerically tractable (exact kink breakpoints, dynamically computed
    per quadrature node, keep the nested double integral exact and fast
    despite the many kinks). Pushed to `z=2500`, where the kernel's own
    resonant window (`~1/z=0.0004`) is already SMALLER than the finest
    gap in the cluster (`0.0075`) -- `z^3|E_full|` stabilizes cleanly
    around `1.53`, comfortably inside the proved bound of `3.0`, with NO
    sign of blowing up or approaching the bound as `z` grows.
- **`s04_core_lemma_direct_check.py`/`.log`** (`mpmath`, `dps=30`): Part
  A confirms the Sec 2.1/3.2 f-VALUES-ONLY closed form for `Gamma_u(h)-
  Gamma(h)` matches a DIRECT `f'`-based computation to `>20` digits on a
  smooth test function (4 `(h,u,eps)` cases) -- an identity cross-check,
  independent of the inequality it is then used to prove. Part B directly
  confirms `|Gamma_u(h)-Gamma(h)|<=3*L1*u` at 9 `(h,u)` combinations
  (`u` from `0.001` to `5.0`, `h` from `0.05` to `7.0`) on BOTH a smooth
  Lipschitz `G` (worst-case ratio to the bound: `0.19`) and a genuinely
  kinked, non-`C^1` Lipschitz `G` (worst-case ratio: `0.08`) -- confirms
  the core lemma is not an artifact of smoothness, exactly as its proof
  (Sec 3.2, using only `f`-value differences) predicts.

> **[Nota, 2026-08-29 — referee hostil, wave 30
> `BOUNDARY-LAYER-SELFHEAL-ATTEMPT`]** The `s03` end-to-end `E_full(z)`
> stress tests (F1-F3 above) fix the outer `h`-integration cutoff at a
> constant multiple of `eps`, independent of `y`/`z`, so `h` never
> exceeds `~7.5` in any tested case -- even at the `z=2500` stress test.
> This front's own THEOREM (Sec 3.4) claims the bound holds uniformly
> over the FULL range `h in[0,y]`, which grows with `z`; the `s03`
> numerics therefore never directly probe `h` close to `y` at large `z`.
> This is a deliberate numerical-efficiency choice with a correct
> analytic justification (the core lemma bound, Sec 3.2, has no
> dependence on `h` at all) -- not a gap in the proof itself -- but the
> numerics section did not say so explicitly. The referee closed this
> independently: an end-to-end check against the RAW kernel operators
> (not this front's own intermediate `rho`/`E_full` formulas) at
> `h=y` (`t=0`, the maximal-`h` case) across `x in{0,0.3,2.0}`,
> `eps in{0.1,0.5,1.0}`, `z` from `3` to `302`, on a kinked Lipschitz
> test function, found zero violations (ratios `0.0012`-`0.2`). See
> `adversarial/REFEREE_REPORT.md`, Nota 2.

- **`s05_assembly_arithmetic_symbolic.py`/`.log`** (`sympy`, exact):
  confirms the elementary algebra of Sec 3.4 -- the triangle-inequality
  step `|1-eps*z|<=1+eps*z`, the `z>=1` simplification
  `3*L1/(eps*z^3)+3*L1/z^2 <= 3*L1*(1+eps)/(eps*z^2)`, and the final
  additive assembly `D(x,eps)=D1(x,eps)+3*L1*(1+eps)/eps` -- zero
  residual at every step.

---

## 5. Self-caught issues

**Issue 1 (`s01` Part 2, an outright `AssertionError` on first run, not a
subtle near-miss).** The first version of `s01`'s Part 2 attempted to
verify the two representations of `Q_u(z)` have the same `u`-derivative
by having `sympy` symbolically differentiate `e^{-u^2/2-uz}*R(u+z)`
directly via its own chain-rule machinery (`sp.diff(Q_alt, u)`), then
substitute the ODE `R'(u+z)=(u+z)R(u+z)-1` into the result via
`.subs(sp.Derivative(R(u+z), u), ...)`. This substitution silently
FAILED to match (`sympy`'s own chain-rule differentiation of a
composed-argument function application produces an opaque
`Subs(Derivative(R(_xi_1),_xi_1), _xi_1, u+z)` wrapper object, not the
literal `Derivative(R(u+z), u)` pattern the `.subs()` call was written
to match), leaving un-substituted `Derivative`/`Subs` terms in the
result. **Caught immediately and unambiguously**: the script's own
closing `assert diff2 == 0` failed outright, with the printed residual
still visibly containing an un-simplified `Subs(...)` term -- not a
near-zero numerical discrepancy, but a structurally obvious sign that the
substitution had not taken effect. **Fixed**: rewrote the derivative
computation to build the product rule BY HAND, term by term
(`dexpo_du*R(u+z) + expo*Rprime_at_uz`, with `Rprime_at_uz:=(u+z)*
R(u+z)-1` supplied directly as the ODE, rather than relying on `sympy`'s
own opaque chain-rule object) -- mathematically identical, but avoiding
the pattern-matching pitfall entirely. Re-run: `assert diff2==0` PASSES
cleanly, matching Route 1 (the direct FTC differentiation of the
tail-integral form) exactly. Visible in the committed
`s01_new_identities_symbolic.py`'s Part 2 (the by-hand construction, with
an inline comment explaining why) and its clean `.log` exit. This was a
`sympy`-API pitfall in this front's OWN exploratory code, not a
mathematical error in the underlying claim, which is correct and (once
the substitution mechanism was fixed) confirmed with zero discrepancy.

**Issue 2 (numerical-efficiency redesign of `s03`, disclosed not
hidden).** An early design of the multi-kink stress tests (F2/F3) used a
STATIC, densely-spaced grid of candidate quadrature breakpoints (e.g. a
periodic sawtooth `f` with breakpoints at every multiple of a small
period `delta`, independent of the specific `h'` being evaluated). Timed
at a single evaluation point, this took `>115` seconds and was abandoned
before completion (caught by direct wall-clock observation, matching the
predecessor's own Sec 7 Issue 2 experience with a similarly
naively-designed nested double integral). **Diagnosis**: static
breakpoints that do not correspond to the ACTUAL kink locations for the
specific `h'` being evaluated leave every quadrature panel containing an
unresolved kink somewhere inside it, forcing `mpmath`'s adaptive
algorithm into many extra subdivisions to reach its (very tight, `dps=20`
-scale) default tolerance on a genuinely non-smooth integrand. **Fixed,
by redesigning, not just re-tuning**: replaced the periodic-sawtooth
design with a SMALL, explicit set of exactly-known kink locations
(`kink_locs`), and modified `rho_raw`/`Ffull_IBP_bracket`/`Efull_value`
to compute EXACT breakpoints DYNAMICALLY for each quadrature call (for
`rho_raw`'s inner `u`-integral at a given `h'`: breakpoints at
`a_i-x-h'` for every kink `a_i` ahead of `h'`; for the outer `h'`-
integral: breakpoints at `a_i-x` directly) -- since the integrand is then
EXACTLY piecewise-linear between breakpoints, Gauss-Legendre quadrature
converges to full working precision with very few nodes per panel, even
at `dps=20`, even with 4-8 simultaneous kinks. This redesign brought a
single evaluation down from `>115s` (incomplete) to `~10s` (F2) and made
the full `F1`+`F2`+`F3` sweep (14 `z`-points total, several with up to 8
kinks) complete in well under 2 minutes. This is disclosed as a genuine
design pivot (matching this lineage's own established honesty
convention for such issues, e.g. the direct predecessor's own Sec 7
Issue 2), not concealed -- the ABANDONED static-grid design was never
committed to this front's own directory in the first place (caught
during this front's own interactive development, before any script was
finalized), so there is no corresponding "broken" `.py`/`.log` pair to
point to, unlike Issue 1 above.

No other issues were found. `s01`, `s02`, `s03`, `s04`, `s05` all ran
cleanly on their (corrected, where applicable) final version, with every
assertion passing.

---

## 6. What remains open, precisely

1. **`(C')` itself is NOT proved for the real `Phi`/`Psi` of this
   system.** This front's own mandate explicitly, deliberately defers
   re-attacking this (per `DISC-DEC-138`: "a questao de equivalencia
   `(C')=(B)` em si ... e deliberadamente NAO reatacada"). The
   predecessor's Sec 5 reduction of `(C')` to a Volterra-resolvent
   stability question (of the same logical type and difficulty as `(B)`
   itself) is UNTOUCHED and unaffected by anything in this document --
   this front does not engage with it at all.
2. **`(H-ces)`, `(U1)`, `(U2)`, `H1` remain formally OPEN.** `(U)` being
   provable under a WEAKER hypothesis (`(C')` instead of `(C'')`) shrinks
   the logical gap to `(U1)` -- it does not close it, since `(C')` itself
   is still an unproved standing hypothesis.
3. **The proof here covers `Phi` Lipschitz on all of `[0,infinity)`,
   matching `(C')`'s own literal statement** -- no attempt is made to
   weaken this further (e.g. to a merely-bounded-variation, or
   non-Lipschitz, `f`); such a further weakening was not part of this
   front's mandate and is not attempted.
4. **The numerical stress tests (Sec 4, `s03`) are decisive evidence, not
   an exhaustive search.** Three test functions of increasing severity,
   the most severe reaching `z=2500`, show zero sign of the bound
   weakening or being approached -- but this is numerical corroboration
   of an ALREADY analytically-proved fact (Sec 3), not a substitute for
   it; the proof itself (Sec 3.2's elementary triangle-inequality
   argument) is what actually establishes the claim for EVERY Lipschitz
   `f`, not merely the tested ones.
5. **`x`-uniformity**: as with every ancestor front, this front works at
   a fixed, general `x>=0`; `D(x,eps)`'s explicit form (Sec 3.4) shows it
   does not grow with `x` beyond its dependence on `z=x+y`, consistent
   with (not independently re-examined beyond) the predecessor's own Sec
   8 item 6 reasoning.
6. **`H2`, non-perturbative (trans-series) content**: untouched, out of
   scope, exactly as every ancestor front in this sub-line.
7. **The predecessor's referee's own "not fully resolved" second-kink
   test** (a one-sided ramp, aggregate self-healing "still climbing" at
   `z=500`, `adv04b_fresh_kink_robustness.log`, cited not re-derived) is
   now, in light of this front's PROVED bound, understood to simply be a
   slower-converging instance of the SAME general `O(1/z^3)` fact (the
   proved bound `3*L1/z^3` only guarantees boundedness/decay of the
   correct ORDER, not a specific fast rate of approach to any particular
   limiting constant -- a slowly-climbing-but-bounded curve is fully
   consistent with, not in tension with, this front's theorem). This
   front did not re-run that specific second-kink construction itself
   (it was already independently confirmed non-adversarial to the
   overall claim by the referee's own honest partial report, and this
   front's OWN three new adversarial constructions, Sec 4, are more
   severe and more numerous than that single check).

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document.

---

## 7. Scorecard

| claim | status |
|---|---|
| `Q_u(z)=int_u^inf e^{-w^2/2-wz}dw = e^{-u^2/2-uz}R(u+z)` (two representations, same function) | **PROVED** (new derivation here, `s01` Part 2; one self-caught `sympy`-API pitfall, fixed) |
| `int_0^inf u*Q_u(z) du = R''(z)/2` | **PROVED** (independently re-derived here from scratch, `s01` Parts 2-3, `s02` numeric cross-check; matches a claim the predecessor front's own scripts never derived, though the predecessor's own referee DID derive it independently in `adv02_rho_and_E_routes.py` [^r1]) |

[^r1]: **[Nota, 2026-08-29 — referee hostil, wave 30
`BOUNDARY-LAYER-SELFHEAL-ATTEMPT`]** Both mentions above originally read
"the predecessor's own referee made but never itself derived in
committed code," which a future reader could parse as "never derived in
any committed code anywhere in this lineage" -- false: the predecessor's
referee's own `cu_direct_proof_attempt/adversarial/adv02_rho_and_E_routes.py`
Part 2 contains a full, numerically-verified derivation of this exact
identity (`<1e-30` relative error). The true state, matching
`DISC-DEC-136`'s own Finding 1: the identity was never derived in the
predecessor **front's** own `s01`-`s03` scripts -- only in the
predecessor's separate referee script. Corrected here for precision;
does not affect this front's own independent re-derivation or any
result. See `adversarial/REFEREE_REPORT.md`, Nota 1.
| `R''(z) <= 2/z^3` for all `z>0` | **PROVED** (new, elementary, self-contained -- one substitution, `s01` Part 5; numerically confirmed ASYMPTOTICALLY TIGHT, `s02`) |
| Elementary f-VALUES-ONLY IBP/FTC identity (Sec 2.1) | **PROVED** (fresh concrete test function, `s01` Part 4) |
| Core lemma `|Gamma_u(h)-Gamma(h)|<=3*L1*u`, ALL `h,u>=0`, `(C')` alone | **PROVED** (new, Sec 3.2; `s04` numeric confirmation on smooth AND kinked `f`) |
| **`|E_full(z)| <= 3*L1/z^3` for ALL `z>0`, using `(C')` ALONE** | **PROVED** (new, Sec 3.3; this front's central result) |
| **`(U)` PROVED conditional on `(B)`+`(C')` ALONE** (no `(C'')`) | **CLOSED, conditionally** -- resolves the predecessor's Sec 4.4 open question in the POSITIVE direction |
| Reproduction of predecessor's published `z^3|Efull|->0.936` | **CONFIRMED** (fresh implementation, `s03` F1, matches to 4+ sig figs) |
| Multi-kink (4 simultaneous kinks) respects the new bound | **CONFIRMED** (new test, `s03` F2, comfortable margin) |
| Geometrically-accumulating 8-kink cluster respects the new bound, up to `z=2500` | **CONFIRMED** (new test, `s03` F3, comfortable margin, no trend toward violation) |
| Genuine counter-example to the new bound, or to `(U)` under `(C')` alone | **NOT FOUND** -- and the proof structure (Sec 3.2) gives a structural reason none should exist |
| `(C')` itself, for the real `Phi` | **NOT ATTACKED** (deliberately deferred, per `DISC-DEC-138`'s own mandate) |
| `(H-ces)`, `(U1)`, `(U2)`, `H1` | **OPEN** (gap to them is now strictly shorter: `(U)` no longer needs `(C'')`) |
| `H2` | **NOT ATTEMPTED** (out of scope) |

`H1` remains ABERTO/OPEN. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and
the four-term asymptotic law of record are all untouched and unaffected
by anything in this document.

---

## 8. Recommendation for the next wave

**The single most concrete, well-scoped next step this front identifies**:
attack `(C')` itself, via the predecessor's own precisely-named Volterra-
resolvent-stability reduction (`cu_direct_proof_attempt/ATTEMPT.md` Sec
5.3) -- now a strictly MORE VALUABLE target than before this front, since
closing it would give `(U)` UNCONDITIONALLY (via this front's own new
Theorem, Sec 3.4, which needs only `(B)`+`(C')`, not the predecessor's
`(C'')`) rather than merely conditionally. This front deliberately did
NOT attempt this (per its own narrow `DISC-DEC-138` mandate), but its
result makes that reduction's payoff strictly larger than it was when the
predecessor first identified it.

A secondary, lower-priority candidate: revisit the predecessor's
referee's own "not fully resolved" second-kink aggregate test
(`adv04b`, still climbing at `z=500`) with this front's OWN proved bound
in hand -- confirm numerically, at larger `z`, that it does eventually
settle within `3*L1/z^3` (this front's Sec 6 item 7 already argues
analytically why it must, but a direct large-`z` numerical confirmation
on that EXACT function would be a small, cheap, closing loose end).

---

## 9. Seeds

Reserved range `20260947000-20260947999` per `DISC-DEC-138`. Grep-
confirmed BEFORE any use (`grep -rn "20260947" 05_DISCOVERY_LAB/`):
appeared only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-138` reservation
line (shared with the sibling front-b reservation line naming both
blocks together). Re-confirmed again at the end of this front (same
command, same result): still appears ONLY in that reservation-adjacent
line, and nowhere inside this front's own new directory. **No randomness
was used anywhere in this front** -- every computation is exact symbolic
algebra (`sympy`) or deterministic arbitrary-precision quadrature
(`mpmath`, fixed evaluation strategy, no sampling) -- exactly as every
direct ancestor front in this exact sub-lineage reports for its own
reservation. The reserved range remains entirely unused.

---

## 10. Files

| file | role |
|---|---|
| `s01_new_identities_symbolic.py`/`.log` | fresh symbolic derivation of `R''(z)=(1+z^2)R(z)-z`; the two representations of `Q_u(z)`; the Tonelli order-swap identity; the f-values-only IBP/FTC identity; the elementary `R''(z)<=2/z^3` bound (Sec 3.3) -- contains one self-caught, disclosed `sympy`-API pitfall (Sec 5, Issue 1) |
| `s02_Rpp_bound_numeric.py`/`.log` | independent high-precision numerical confirmation of every identity in `s01` that has a numerical form, plus the asymptotic tightness of `R''(z)<=2/z^3` |
| `s03_Efull_bound_stress_test.py`/`.log` | THE decisive end-to-end numerical test of `|E_full(z)|<=3*L1/z^3`, on the predecessor's own kink (sanity cross-check) plus two NEW, more adversarial multi-kink constructions this front designs itself (Sec 4) -- exact dynamically-computed kink breakpoints make the nested double integral tractable despite up to 8 simultaneous kinks (Sec 5, Issue 2 design note) |
| `s04_core_lemma_direct_check.py`/`.log` | direct numerical confirmation of the core lemma `|Gamma_u(h)-Gamma(h)|<=3*L1*u`, both as an identity (vs a direct `f'`-based computation on a smooth function) and as the inequality itself (on both smooth and kinked Lipschitz functions) |
| `s05_assembly_arithmetic_symbolic.py`/`.log` | the elementary algebra assembling this front's new `Efull` bound with the predecessor's cited `(B)`-only value-piece bound into the final `D(x,eps)` |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`boundary_layer_selfheal_attempt/` subdirectory was written to -- every
ancestor `ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/
`DISCOVERY_LAB_STATE.md` further up the tree were read-only references
(Sec 0), never modified. No `adversarial/` subdirectory created; no
referee dispatched by this front itself, per the mandate. No `git`
command run.

---

## 11. Scope discipline confirmation

- No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
  `index.html`, or any file outside this front's own new
  `boundary_layer_selfheal_attempt/` directory -- including the parent
  `cu_direct_proof_attempt/` directory and its own `adversarial/`
  subdirectory, and every other ancestor directory further up the tree
  (`h_ces_direct_attempt/`, `tauberian_oscillation_bound_attempt/`,
  `h1_translation_structure_attempt/`, and further ancestors), all read
  as required background but never written to.
- No `adversarial/` subdirectory created by this front (per the mandate:
  "Do NOT create an `adversarial/` subdirectory or dispatch any referee
  yourself").
- No `git` command of any kind run.
- No claim of progress on any Millennium Prize Problem appears anywhere
  in this document -- `M-CLUST(b)` is, as stated at the top of this
  document and throughout the required reading, a standalone
  combinatorial/asymptotic object, entirely independent of the archive's
  separate Tree A (`u1/2`) line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's
  explicit rule, no result, finding, or hedge from the Tree A line is
  cited anywhere in this document as evidence for anything claimed here,
  and no result from this document is intended to be read as evidence
  for anything in Tree A.
- One self-caught issue in this front's own exploratory `sympy` code
  (Sec 5, Issue 1) was found by this front's OWN process (an outright
  `assert` failure on first run), disclosed here with the before/after
  described and the fixed version visible in the committed
  `s01_new_identities_symbolic.py`; one design-level self-caught
  performance issue (Sec 5, Issue 2), disclosed with the diagnosis and
  redesign described, matching this exact sub-lineage's own established
  honesty convention. Neither was found by, or required, an external
  referee.
- No `THEOREM.md`-tier claim of closure is made anywhere in this
  document. `(C')` itself remains unproved for the real `Phi`; `(H-ces)`,
  `(U1)`, `(U2)`, `H1` remain formally OPEN, stated plainly and
  repeatedly (VERDICT UP FRONT, Sec 3.4, Sec 6, Sec 7) -- this front's
  positive result is that `(U)`'s own proof no longer needs the
  predecessor's `(C'')`, a genuine but strictly SUBORDINATE strengthening
  within the still-open larger gap.
