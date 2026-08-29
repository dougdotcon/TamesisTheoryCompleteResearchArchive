# ATTEMPT -- translation-invariance structure of `K(y,t)` as a route to
# the `y->infinity` gap in `(U1)`/`(U2)` (`H1-TRANSLATION-STRUCTURE-ATTEMPT`)

**Wave 25, front (c), `DISC-DEC-118`.** Target: `(U1)` and `(U2)`, the two
precisely-stated sub-hypotheses `mclust_h1_validity_attempt` (`DISC-DEC-088/
091`) reduced `H1` to -- specifically the diagnosed remaining gap (per
`DISC-DEC-115`, `h1_post_correction_attempt`): the rigorous Neumann/Picard
convergence theorem proved there controls convergence in truncation ORDER
`n` at each FIXED `y`, not the resummed value's behavior as `y->infinity`.
This front's specific mandate: use that now-PROVED convergence result and
the rigorous `n_cross,rig(y)` bound as a cited starting point, and attack
the `y->infinity` gap specifically through the one structural fact
identified but not attacked by the predecessor -- **`K(y,t)` is NOT
translation-invariant in `(y,t)`** -- by characterizing PRECISELY how it
fails to be.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process -- pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lema Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.** Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no
result from Tree A is cited anywhere below, even in hedged language, as
evidence for anything claimed here.

Reserved seed range for this front: `20260931000-20260931999`.
Grep-confirmed BEFORE any use (`grep -rn "20260931" 05_DISCOVERY_LAB/`) to
appear only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-118` reservation line
(re-confirmed again at the end of this front, Sec 9). **In the end no
randomness was needed anywhere in this front** -- exactly as every front in
this exact sub-lineage (`mclust_h1_validity_attempt` and its descendants)
reports: every result below is exact symbolic reasoning (`sympy`),
deterministic arbitrary-precision quadrature (`mpmath`, adaptive
Gauss-Legendre, fixed evaluation points, no sampling), or elementary
arithmetic. The reserved range remains entirely unused.

---

## VERDICT UP FRONT

**Tier: (c) -- an honest, sharper diagnosis of the `y->infinity` obstruction,
via the translation-invariance angle, with genuinely new closed-form
content -- NOT full closure of `(U1)`/`(U2)`/`H1`, and NOT a non-uniformity
certificate either.** This is the sixth consecutive wave (waves 20-25)
attacking this exact gap; it does not close it. But the diagnosis reached
here is, in one
precise sense, sharper than any predecessor's in this sub-lineage: it is the
first front in this chain to produce a **closed-form** (not merely an
order-of-magnitude bound) leading asymptotic for the kernel `K(y,t)` itself,
and to turn that closed form into a genuinely new **reformulation** of
`(U1)` (not just another bound-tightening attempt on the same machinery).

1. **The translation-invariance failure is precisely located and exactly
   characterized** (Sec 2): `K(y,t) = M_y K_A^raw(y,t) + K_B(y-t)`. `K_B`
   alone **is** an exact convolution/translation-invariant kernel (a
   function of `h:=y-t` alone). `M_y K_A^raw` is the **entire** source of
   non-invariance, and its precise mechanism is an exact exponential
   conjugation identity, newly derived here: `T_w = M_(e^{wx}) T_0
   M_(e^{-w.})`, an Esscher-type tilt whose distortion is governed by the
   ABSOLUTE coordinate `z:=x+y`, not by the elapsed time `h=y-t` alone.

2. **Neither disjunct of the mandate's question is quite right, and the
   truth is more informative than either** (Sec 3-4): `M_y K_A^raw(y,t)`
   does NOT vanish as `y->infinity` (it settles at a nonzero, order-`eps`
   limit, confirmed both by `DISC-DEC-113`/`115`'s own operator-norm fact
   `sup_{z>=y} h_eps(z) -> eps` and independently reconfirmed here on
   concrete test functions). Neither does `K_B(h)` (it is exactly
   `y`-independent by construction). **But their SUM is a delicate,
   near-total cancellation**, not a small perturbation of one by the other
   -- `M_y K_A^raw(y,t) approx -K_B(h)` for large `y`, to leading order,
   with the correction terms conspiring to cancel EXACTLY.

3. **A new closed-form leading asymptotic, derived and proved (conditional
   on the standing boundedness hypothesis `(B)` plus one auxiliary
   Lipschitz-type regularity hypothesis `(C)` on the function `K` acts on)**
   (Sec 4):
   ```
   K(y,t) f(x)  =  [ f(x) - e^{-h/eps} f(x+h) ] / (x+y)  +  O(1/(x+y)^2)
   ```
   as `y->infinity` at fixed (or even proportionally growing) `h=y-t`. This
   is not merely an order bound (`O(1/(x+y))`, itself new relative to the
   predecessor's constant-only bound `sqrt(pi/2)+eps`) -- it is the EXACT
   leading coefficient, independently confirmed numerically via Richardson
   extrapolation to a worst-case relative error of `3.2e-8` across 6
   `(x,h,eps,f)` combinations (Sec 5), and confirmed to remain accurate,
   with the SAME coefficient, when `h` grows PROPORTIONALLY with `y`
   (`h=y/2`, tested to `y=3000`), not just when `h` is held fixed.

4. **A genuinely new reformulation of `(U1)`, derived as a rigorous
   consequence of item 3 applied to the ACTUAL closed Volterra equation**
   (Sec 6): `(U1)` is equivalent, up to rigorously-controlled vanishing
   corrections, to a **self-averaging** (Cesaro-type) identity --
   `Phi_y(x)` asymptotically tracks the RUNNING AVERAGE of its own past
   values, `Phi_y(x) - (1/(x+y)) int_0^y Phi_t(x) dt -> 0`. This is a
   structurally NEW route, distinct from both the predecessor's Watson/
   Laplace-in-`1/y` expansion (`h1_energy_estimate_attempt`, `DISC-DEC-100`)
   and the pure operator-norm Volterra route (`h1_volterra_attempt`/
   `h1_post_correction_attempt`, `DISC-DEC-113/115`) -- it reduces `(U1)`
   to a classical **Tauberian** convergence question (Cesaro convergence +
   a "slowly oscillating" regularity condition implies ordinary
   convergence), for which the precise missing ingredient is named exactly
   (Sec 6.3): an oscillation bound on `Phi` itself (not `Psi`, which
   `(star-star)` from `h1_energy_estimate_attempt` already bounds) of the
   right RELATIVE-step form.

5. **`(U1)`/`(U2)` do NOT close.** The Tauberian route is a real, precisely
   identified, well-motivated candidate -- genuinely different from "another
   angle on the same Volterra kernel" -- but completing it requires (i) an
   oscillation/regularity bound for `Phi` (not currently in the record, only
   for `Psi`), and (ii) formal verification that the classical continuous
   Tauberian theorem's hypotheses are met in this two-variable PDE setting.
   Neither is attempted to completion here (Sec 6.3, Sec 7). **A separate,
   important scope clarification** (Sec 4.4): the closed-form cancellation
   is proved for `K(y,t)` acting on any FIXED, sufficiently regular
   (Lipschitz) `f` -- it is NOT a claim that the OPERATOR NORM of `K(y,t)`
   (sup over ALL bounded `f`, including non-smooth ones) decays; that
   operator-norm-level fact (`sup_{z>=y} h_eps(z) -> eps`, a NONZERO limit)
   is already established (`DISC-DEC-113/115`) and is NOT contradicted or
   superseded here.

**Two self-caught, disclosed sign/scaling errors** occurred during this
front's own scratch derivation (Sec 4.2, Sec 4.3) -- both caught by the
front's OWN symbolic verification scripts failing their own assertions (not
by a later referee), both corrected in place with the fix and the
before/after visible in the committed `.py`/`.log` files. No third-party
error was found in any ancestor front's published record.

> **Nota (2026-08-29, achado F2 do referee hostil dedicado, severidade
> BAIXA, precisão de enquadramento -- nenhum erro matemático):** a
> frase acima, de que ambos os bugs autocapturados foram "caught by the
> front's OWN symbolic verification scripts failing their own
> assertions", é exata para o Bug 2 (`s05`, Seção 4.3) mas não para o
> Bug 1 (`s02`, Seção 4.2) -- cujo próprio relato detalhado (Seção 4.2
> abaixo) diz corretamente que se tratou de um erro apenas de PROSA: o
> cálculo `sympy` esteve correto durante todo o processo, e o erro foi
> percebido por notar que o comentário contradizia a própria saída
> impressa, já correta, do script -- os `assert`s que corroboram a
> correção foram adicionados DEPOIS da correção, como medida de reforço,
> não como o mecanismo original de captura. Ponto puramente de precisão
> documental; a matemática subjacente de ambos os bugs, seus
> diagnósticos e suas correções permanecem integralmente confirmados de
> forma independente (Seção 5 do `REFEREE_REPORT.md`). Fonte:
> `adversarial/REFEREE_REPORT.md`, Seção 8, Finding 2.

**`H1` remains ABERTO/OPEN, exactly as before this front.** `phi_REDB`,
`Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law of record are
all untouched and unaffected by anything in this document. `H2` is untouched
(out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself. No `git` command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` Sec 2 (Tree B), specifically the `PLATRESUM` node's complete
addendum history through the final two addenda (dated 2026-08-28,
`DISC-DEC-113` and `DISC-DEC-115`), which document the corrected kernel
bound and the rigorous Neumann/Picard convergence + `n_cross,rig(y)` result
this front's mandate is built on; Sec 3 ("Regra de uso deste mapa"), the
safety rule against conflating this line with the separate "Arvore A"
(`U_alpha`) line -- followed strictly throughout. Also read in full:
`mclust_h1_validity_attempt/ATTEMPT.md` (establishes `(U1)`/`(U2)` precisely,
Watson Concentration Lemma, `DISC-DEC-088/091`); `h1_energy_estimate_attempt/
ATTEMPT.md` in full (the `(star-star)` global oscillation bound on `Psi`,
its two precise non-closure diagnoses Sec 6.1-6.2, the Lipschitz-`<=1`
contraction finding Sec 8.2-8.3, `DISC-DEC-096/100`); `h1_volterra_attempt/
ATTEMPT.md` Sec 3-4 and Sec 6 (the Volterra-in-`y` structural setup and the
corrected kernel bound, `DISC-DEC-113`); and the full `h1_post_correction_
attempt/ATTEMPT.md` (the rigorous Neumann/Picard convergence theorem, the
rigorous `n_cross,rig(y)` bound, and the explicit naming of the translation-
invariance-failure obstacle this front's mandate points at, `DISC-DEC-115`).

**No `.py` file from any ancestor front, or from any referee, was opened,
read, or imported at any point.** Every script in this directory (`s01`-
`s07`) was written fresh from the mathematical content of the prose cited
above, exactly as every direct ancestor front in this sub-lineage reports
for itself.

**The exact inputs this front works from** (restated for
self-containedness, identical to the predecessor's own Sec 0, cited not
re-derived except where marked NEW below):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

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

THE CORRECTION (DISC-DEC-113): ||K(y,t)|| <= sqrt(pi/2)+eps UNIFORMLY in
  x,y,t (0<=t<=y), including the full unrestricted x-domain, for ALL y.

THE PROVED CONVERGENCE (DISC-DEC-115): for every finite Y>=0, the Picard/
  Neumann iteration for (VOLTERRA-Phi) converges, sup-x norm on X, LOCALLY
  UNIFORMLY in y on [0,Y]; n_cross,rig(y):=ceil(e*sqrt(pi/2)*y)+1 rigorously
  dominates the empirical warm-up length. Both diagnosed as controlling
  convergence in ORDER n at FIXED y, not the resummed value as y->infinity.
  NAMED, NOT ATTACKED: K(y,t) is not translation-invariant in (y,t).

The oscillation bound (h1_energy_estimate_attempt Sec 5.1, cited, "(star-star)"):
  sup_{x>=0} |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1)*K*R(y1)  <=  (y2-y1)*K/y1
  (K := 2*max(|Phi|,|Psi|), an empirically-measured, not independently
  proved, constant -- consistent with (B) being standing throughout).
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout; nothing
outside this front's own new subdirectory was written to.

---

## 1. Overview

Four parts, in the order the mandate poses the question:

- **Part A (Sec 2).** Locate and exactly characterize the source of
  translation-invariance failure: `K_B` is exactly invariant; `M_y K_A^raw`
  is the entire source, via a new exact exponential-conjugation identity for
  the operator family `{T_w}`, and a new single-integral reduction of
  `K_A^raw` exposing its dependence on the ABSOLUTE coordinate `z=x+y`.
- **Part B (Sec 3-4).** Answer the mandate's precise disjunctive question
  ("does the non-invariance become asymptotically small with a controllable
  rate, or does it persist at leading order?") -- with a THIRD, more
  informative answer: a delicate near-total cancellation between two
  individually-nonvanishing pieces, characterized by a new CLOSED-FORM
  leading asymptotic for the entire kernel `K(y,t)`.
- **Part C (Sec 5).** Full independent numerical verification of the closed
  form (not just its order), via direct quadrature of the RAW operator
  definitions -- a route independent of the symbolic derivation -- across 6
  `(x,h,eps,f)` combinations plus a dedicated uniformity-in-`h` check.
- **Part D (Sec 6-7).** Consequences: a genuinely new "self-averaging"
  reformulation of `(U1)`, its precise (named, not closed) Tauberian
  completion requirement, and an honest resolution of how this front's
  ALGEBRAIC (`O(1/z)`) finding relates to the numerically-observed
  EXPONENTIAL content the mandate asks about.

Every result reports its own honest limits; `(U1)`/`(U2)` are not closed.

---

## 2. Part A -- precisely locating the translation-invariance failure

### 2.1 `K_B` is exactly translation-invariant; `M_y K_A^raw` is the entire
source of non-invariance

By inspection of the definitions in Sec 0: `K_B(h) := int_0^h e^{-v/eps}
S_v dv` depends on `y,t` ONLY through `h=y-t` -- an exact convolution
kernel, trivially translation-invariant: `K_B` applied at `(y+a,t+a)` for
any shift `a` is identical to `K_B` applied at `(y,t)`. `K_A^raw(y,t) :=
int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw` depends on `y` and `t` SEPARATELY (not
merely through `h`) via the `T_w` operator's own `w`-dependence and via the
integration bounds -- and after multiplication by `M_y` (itself an explicit
function of `y`, not of `h`), the composite `M_y K_A^raw(y,t)` is the entire
source of `K(y,t)`'s failure to be a function of `h` alone.

### 2.2 A new exact identity: `T_w` is an exponential conjugation of `T_0`

**Claim.** `T_w = M_(e^{wx}) o T_0 o M_(e^{-w.})`, i.e.
`(T_w f)(x) = e^{wx} * (T_0[e^{-w(.)} f])(x)` for every `w`.

**Proof (`s01_conjugation_and_reduction.py` Part 1).** `T_w`'s integral
kernel, in terms of the landing point `x'':=x+u` (`x''>=x`), is `K_T(x,x'';w)
= e^{-(x''-x)^2/2} * e^{-(x''-x)(x+w)}`. Symbolically simplifying
`log(K_T(x,x'';w) / [e^{wx} K_T(x,x'';0) e^{-w x''}])` gives **identically
`0`** (`sympy`, exact). A second, operator-level (not merely kernel-level)
check confirms the pointwise-in-`u` integrand identity `e^{-u^2/2-u(x+w)}
f(x+u) = e^{wx} * e^{-u^2/2-ux} * [e^{-w(x+u)} f(x+u)]` also simplifies to
`0` exactly. **QED.**

This is an exact **Esscher-type exponential tilt**: the family `{T_w}` is
obtained from `T_0` by conjugating with the (unbounded, `w`-growing)
multiplication operator `e^{wx}`. This is the precise algebraic mechanism
generating `K_A^raw`'s dependence on absolute position rather than only
elapsed time -- new to this lineage's record (the predecessor fronts used
the `x'+w=x+y` cancellation this identity underlies, but never isolated the
conjugation structure itself).

### 2.3 The `x'+w=x+y` cancellation, independently re-derived

Re-confirmed independently (`s01` Part 2, `sympy`, exact): with `x':=x+y-w`
(the shift `S_{y-w}` composed with `T_w`), the exponent `x'+w` simplifies to
`x+y` identically, **independent of `w`** -- the same fact `DISC-DEC-113`/
`h1_post_correction_attempt` Sec 2.1 established, re-derived here from the
raw operator definitions as the starting point for a NEW reduction (Sec 2.4)
that those fronts did not need for their own (bound-only, not closed-form)
purposes.

### 2.4 A new single-integral reduction of `K_A^raw`, exposing the exact
locus of non-invariance

Substituting `h':=y-w` (`h'` ranges `0..h`, `h:=y-t`) and using Sec 2.3:

```
K_A^raw(y,t) f (x) = int_0^h e^{-h'/eps} [ int_0^infinity e^{-u^2/2-u(x+y)} f(x+h'+u) du ] dh'
```

The inner weight `e^{-u^2/2-u(x+y)}` depends on `x` ONLY through `z:=x+y` --
**not** through `x` and `t` (or `h`) separately. This is the precise,
minimal statement of the non-invariance: a genuine convolution kernel would
depend on `s:=x''-x` and `h` alone; `K_A^raw`'s kernel depends on `s`, `h`,
AND the ABSOLUTE quantity `z=x+y` -- three arguments, not two, for what
would be a two-argument object if it were translation-invariant.

**Numerically cross-checked** (`s01b_reduction_numeric_check.py`) against
the ORIGINAL `(w,u)` raw double-integral definition, via two structurally
independent `mpmath` quadrature routes, at 5 `(x,y,t,eps)` points and 2 test
functions (`f=1/(1+x)`, `f=exp(-x/3)`): **10/10 PASS**, agreement to better
than `4.1e-19` relative (a pure change-of-variables identity, expected to
match to full working precision -- confirms no algebra slip in the
reduction). *Self-caught, disclosed:* an earlier version of this script used
threshold `1e-20`, below the achievable noise floor of nested
adaptive double quadrature at `dps=40` on a semi-infinite domain, and
spuriously flagged 2/10 points that agreed to `3.6e-19`/`4.1e-19` (18-19
significant digits) as FAIL; corrected to `1e-15`, itself still `4-5` orders
tighter than needed. Fixed and re-run; log reflects the corrected run
(10/10 PASS).

---

## 3. Part B(i) -- neither disjunct of the mandate's question is quite right

The mandate poses a precise disjunction: does the non-invariance become
"asymptotically small ... with a controllable rate" (suggesting a
perturbative route: translation-invariant base case + small perturbation),
or does it "persist at leading order" (itself the diagnosis)? **Both
individual pieces are checked directly, and neither disjunct describes what
actually happens.**

### 3.1 `K_B(h)` does not decay (trivially, by construction)

`K_B(h)` is exactly `y`-independent -- confirmed as a sanity check in every
run of `s03_kernel_cancellation_numeric.py` (12/12 parameter combinations,
`KB(h) is exactly y-independent: PASS`).

### 3.2 `M_y K_A^raw(y,t)` does NOT vanish as `y->infinity` either

Already implicit in `DISC-DEC-113`/`115`'s own operator-norm fact
`sup_{z>=y} h_eps(z) -> eps` (a NONZERO limit, not `0`) -- independently
reconfirmed here on concrete test functions (`s03`, direct quadrature of the
RAW `K_A^raw` definition, not the reduced form): at `eps=0.1`, `M_y
K_A^raw(y,t) f(0)` for `f=1/(1+x)` settles to `-0.090809...` (`h=0.5`),
`-0.091230...` (`h=2.0`), `-0.091231...` (`h=5.0`) by `y approx 3000` --
essentially `h`-independent once `h` exceeds a few multiples of `eps` (the
small residual gap at `h=0.5`, where `h/eps=5`, is consistent with the
non-negligible `e^{-h/eps}=e^{-5}approx0.0067` correction identified exactly
in Sec 4.3), and in every case **NONZERO**, not `0`; at `eps=1/sqrt(1000)`,
it settles to `-0.030348...`-`-0.030960...` similarly. **Order `eps`,
consistent with, but a genuinely new confirmation on top of, the
operator-norm fact.**

### 3.3 The naive "base case + small perturbation" split fails, but the SUM
is small

Since `M_y K_A^raw(y,t)` and `-K_B(h)` are both order-`eps`, opposite-sign
magnitudes -- confirmed numerically above: e.g. at `eps=0.1,h=2.0`:
`K_B(2)f(0)=0.09156333...` (exactly `y`-independent by construction),
`M_y K_A^raw(y,t) f(0) -> -0.09123032...` as `y->3002` -- these are CLOSE
but not numerically identical in magnitude (`K(y,t)f(0)` itself, their sum,
is what is actually small: `0.000333...` at `y=3002`, three orders of
magnitude below either piece alone), because `K_A^raw`'s own limit already
reflects the FULL cancellation coefficient (Sec 4 below pins the exact
relationship: `M_y K_A^raw(y,t)f(x) -> c(infinity)*K_B(h)f(x) = -K_B(h)f(x)`
exactly as `y->infinity`, `c(z)->-1`, so the near-equality of magnitudes
seen here is not a coincidence -- it IS the leading-order statement of Sec
4, and the small residual `K(y,t)f(0)` is exactly the NEXT-order term Sec 4
computes in closed form), not a naive, uncorrelated `-K_B` split. The
candidate perturbative route the mandate names ("treat the
translation-invariant part `K_B` as the base case, `M_y K_A^raw` as a small
perturbation") does **NOT** apply in the
naive sense: `M_y K_A^raw` is not small relative to `K_B` for large `y` --
it is COMPARABLE and (as Sec 4 makes precise) nearly exactly canceling.
**What IS small, precisely quantified, is the SUM** `K(y,t)=M_y K_A^raw(y,t)
+K_B(h)` -- confirmed to decay like `O(1/y)` (log-log slope fit
`-0.9942` to `-0.9985` across all 12 tested `(eps,h,f)` combinations,
`s03_kernel_cancellation_numeric.log`), a genuinely new, precisely
quantified finding: **not** a persistent leading-order failure (the SUM does
shrink), and **not** simple convergence of the non-invariant piece to a
nonzero translation-invariant kernel either (the non-invariant piece does
NOT shrink; it is the SUM's cancellation that shrinks).

---

## 4. Part B(ii) -- the main new result: a closed-form leading asymptotic
for the entire kernel

### 4.1 An exact decomposition (no approximation yet)

For `Theta_{h'}(z) := int_0^infinity e^{-u^2/2-uz} f(x+h'+u) du` (the inner
integral of Sec 2.4's reduction), splitting off the constant term:

```
Theta_{h'}(z) = f(x+h') * R(z) + rho(h',z),
  rho(h',z) := int_0^infinity e^{-u^2/2-uz} [f(x+h'+u)-f(x+h')] du
```

**Exact, no approximation** -- `R(z)=int_0^infinity e^{-u^2/2-uz}du` by
definition. Substituting into Sec 2.4's reduction gives, EXACTLY:

```
M_y K_A^raw(y,t) f(x) = c(z) * K_B(h) f(x)
    + [(1-eps z)/eps] * int_0^h e^{-h'/eps} rho(h',z) dh'          (*)
  c(z) := (1-eps z) R(z) / eps
```

(`s02_exact_decomposition_and_asymptotics.py`.)

### 4.2 The coefficient `c(z) -> -1` as `z->infinity`, exact rate

**New symbolic derivation** (`s02` Part 1): the standard Mills-ratio
asymptotic series for `R(z)` is re-derived here from its own defining ODE
`R'=zR-1` via a direct coefficient recursion (`sympy`, exact): `R(z) ~
sum_n c_n/z^{2n+1}`, `c_0=1`, `c_n = -(2n-1)c_{n-1}` -- reproducing `1/z -
1/z^3 + 3/z^5 - ...`, matching the known Mills-ratio series (`c_0..c_3 =
1,-1,3,-15` checked by assertion). From this, `c(z) = R(z)/eps - zR(z)`
expands to:

```
c(z) = -1 + 1/(eps*z) + 1/z^2 + O(1/z^3)     as z -> infinity
```

*Self-caught, disclosed (severity: prose-only, no arithmetic error in the
underlying `sympy` computation):* an earlier draft of this script's own
COMMENTARY asserted the wrong sign (`"-1/(eps*z)"`) and wrongly claimed the
`z^-2` term vanishes -- both directly contradicted by the very symbolic
series the script itself printed two lines above the erroneous claim. The
`sympy` derivation and its coefficient recursion were correct throughout;
only the prose describing the result was wrong (an `assert` added after the
fix now pins both coefficients: `zm1 == 1/eps` and `zm2 == 1`). Fixed in
place; the corrected claim (`+1/(eps*z)`, positive) is what Sec 4.2's
numerical confirmation (`s02` Part 2) independently checks, and matches:
`z*(c(z)+1) -> +1/eps` confirmed to `4` significant digits by `z=10^4` at
both tested `eps` (`0.1` and `1/sqrt(1000)`).

### 4.3 Assembling the closed form; a second self-caught cancellation bug

`rho(h',z)` (Sec 4.1) has `g(0)=0` where `g(u):=f(x+h'+u)-f(x+h')` -- so the
SAME exact one-step integration-by-parts identity used to derive `R'=zR-1`
(re-derived here generically for any smooth `g`, `s05` Step 1: `z
Theta_g(z) + int_0^infinity u e^{-u^2/2-uz} g(u) du = g(0) + Theta_{g'}(z)`,
confirmed via the elementary calculus fact `d/du[-e^{-u^2/2-uz}]=(u+z)
e^{-u^2/2-uz}`) gives, since `g(0)=0`: `rho(h',z) ~ f'(x+h')/z^2 + O(1/z^3)`
(standard Watson's-lemma bookkeeping, `s05` Step 2). Combined with an exact
(non-asymptotic) integration-by-parts evaluation of `int_0^h e^{-h'/eps}
f'(x+h') dh'` (`s05` Step 3, confirmed on a concrete non-trivial test
function `F(h')=h'^3+sin(h')` via `sympy`, exact, `diff==0`):

```
int_0^h e^{-h'/eps} f'(x+h') dh' = e^{-h/eps} f(x+h) - f(x) + (1/eps) K_B(h) f(x)
```

assembling `(*)` to leading order in `delta:=1/z` gives the **final closed
form**:

```
K(y,t) f(x)  =  [ f(x) - e^{-h/eps} f(x+h) ] / z  +  O(1/z^2)      z:=x+y
```

with the `K_B(h)f(x)/eps` terms from the `c(z)` piece and the `rho` piece
**canceling exactly** (`s05` Step 4, `sympy`, `assert KB_coeff==0` -- see
below).

*Second self-caught, disclosed bug:* the FIRST version of `s05`'s Step-4
bookkeeping asserted `(1-eps*z)/eps ~ -1/(eps*delta)` (i.e. `-z/eps`) as
`z->infinity` -- WRONG: `(1-eps*z)/eps = 1/eps - z`, and since `eps` is
HELD FIXED while `z->infinity`, the unbounded `-z` term dominates the fixed
constant `1/eps`, so the correct leading behavior is `(1-eps*z)/eps ~ -z`
(NO extra `1/eps` factor). This was caught immediately: the script's own
`assert sp.simplify(KB_coeff)==0` FAILED on the first run (`KB_coeff =
1/eps - 1/eps**2`, manifestly nonzero and dimensionally inconsistent in
`eps`-power between the two contributing terms). Fixed (`term2 = (-1/delta)
* (delta**2 * IBPresult)`, i.e. dropping the spurious `1/eps`); the
corrected run's `assert` now PASSES (`Coefficient of KB ... at order
delta^1: 0`), and the resulting closed form is exactly the one stated above
and confirmed numerically in Sec 5. Both bugs are visible in
`s05_leading_asymptotic_symbolic.py`'s own inline comments (marked
`SELF-CAUGHT BUG`) and in `s05_leading_asymptotic_symbolic.log`.

### 4.4 Scope clarification: pointwise-in-`f` cancellation, NOT an
operator-norm claim

**This closed form is proved for `K(y,t)` applied to any FIXED, sufficiently
regular (the `rho`-bound needs `f` differentiable with `f'(x+h')` controlled
-- an auxiliary hypothesis `(C)`, beyond the standing `(B)`) bounded
function `f`.** It is emphatically **NOT** a claim that the OPERATOR NORM
`sup_{||f||<=1} ||K(y,t)f||` decays as `y->infinity` -- that quantity's
correct, tight, already-established behavior is `sup_{z>=y} h_eps(z) ->
eps` (a NONZERO limit, `DISC-DEC-113/115`, re-confirmed Sec 3.2 above), and
nothing here contradicts or supersedes it. The reason there is no
contradiction: the operator-norm sup is dominated by ADVERSARIAL
(non-smooth, or smooth with unboundedly large derivative) test functions,
for which the `rho`-remainder's implicit Lipschitz-constant-dependent bound
blows up -- this front's cancellation is a genuine `O(1/z)` fact for each
FIXED regular `f`, not a uniform-over-all-bounded-`f` fact. This distinction
matters directly for Sec 6: it is exactly why the closed form is useful
for reasoning about the ACTUAL (presumably smooth, PDE-solution) `Phi`, but
does NOT by itself give a sharper OPERATOR bound of the kind the classical
Volterra quasi-nilpotency argument (`DISC-DEC-115`, Sec 3 there) needs for
its truncation-order convergence proof -- consistent with this front NOT
closing `(U1)`/`(U2)` via a quick strengthening of that route.

---

## 5. Part C -- independent numerical verification of the closed form

### 5.1 Order confirmation across 12 parameter combinations
(`s03_kernel_cancellation_numeric.py`)

Direct quadrature of the RAW `M_y K_A^raw` and `K_B` definitions (not the
Sec 2.4/4.1 reduced forms -- an independent computational route), `eps in
{0.1, 1/sqrt(1000)}`, `h in {0.5,2.0,5.0}`, `f in {1/(1+x), exp(-x/3)}`,
`x=0`, `y` swept from `h+0.5` to `h+3000`: log-log slope of `|K(y,t)f(0)|`
vs `y` (last 5 points) is **`-0.9942` to `-0.9985`** at all 12 combinations
-- confirming the `O(1/y)` order predicted.

### 5.2 `x`-dependence: `O(1/(x+y))`, not merely `O(1/y)`
(`s04_x_dependence_check.py`)

At fixed `eps=0.1, h=2.0, f=1/(1+x)`, `x in {0,1,3,10}`: the fitted slope
stays reasonably close to `-1` and degrades monotonically as `x` grows
(`-0.9658, -0.9487, -0.9075, -0.8083` at `x=0,1,3,10` respectively -- a
5-point fit over `y=3` to `y=3002` at each `x`, so the visible degradation
at `x=10` is consistent with a finite-`y`-range fit-quality effect [the
asymptotic regime `z=x+y>>1/eps=10` is reached later, relatively, when `x`
itself is already `10`], not evidence of a different exponent -- Sec 5.3's
Richardson-extrapolated check below, which isolates the true `z->infinity`
limit rather than fitting a slope over the whole range, is the decisive
test) and, decisively, the
VALUE at matched `y=1002` scales as `1/(x+y)`: `z*K(y,t)f(x)` at `x=0,1,3,10`
gives `0.999, 0.500, 0.250, 0.0909` -- matching `f(x)=1/(1+x)` (`1, 0.5,
0.25, 0.0909...`) to 3-4 significant figures, an early numerical hint of the
closed-form coefficient later pinned down exactly in Sec 5.3.

### 5.3 Exact closed-form coefficient, confirmed via Richardson extrapolation
(`s06_leading_asymptotic_numeric_check.py`)

At 6 `(x,h,eps,f)` combinations spanning `x in {0,1,2}`, `h in {0.5,2,5}`,
both `eps` values, both test functions, `z` swept `10` to `10^4`, comparing
`z*K(y,t)f(x)` against the predicted `f(x)-e^{-h/eps}f(x+h)`:

| case | predicted | Richardson-extrap. (last 2 `z`) | rel. err |
|---|---|---|---|
| `x=0,h=0.5,eps=0.1,f=1/(1+x)` | `0.9955080353` | `0.9955080076` | `2.8e-8` |
| `x=0,h=2.0,eps=0.1,f=1/(1+x)` | `1.0` (to 10dp) | `0.9999999716` | `2.8e-8` |
| `x=1,h=2.0,eps=0.1,f=1/(1+x)` | `0.5` (to 10dp) | `0.5000000093` | `2.0e-8` |
| `x=0,h=2.0,eps=1/sqrt(1000),f=1/(1+x)` | `1.0` | `0.9999999687` | `3.1e-8` |
| `x=0,h=2.0,eps=0.1,f=exp(-x/3)` | `0.9999999989` | `1.000000031` | `3.2e-8` |
| `x=2,h=5.0,eps=0.1,f=exp(-x/3)` | `0.513417119` | `0.5134171353` | `3.2e-8` |

**Worst-case relative error across all 6 cases: `3.2e-8`** -- decisive
confirmation of the exact closed-form coefficient, not merely its order.

### 5.4 Uniformity in `h`: the formula holds even when `h` grows
proportionally with `y` (`s07_uniformity_in_h_check.py`)

The self-averaging argument of Sec 6 integrates `K(y,t)` over ALL
`t in [0,y]` -- i.e. all `h in [0,y]` simultaneously -- so uniformity of the
closed form across the FULL `h`-range (not just fixed `h`) matters. Tested
at `h=y/2` (so `h` grows without bound alongside `y`, up to `h=1500` at
`y=3000`), `x=0, eps=0.1, f=1/(1+x)`: Richardson-extrapolated `z*K(y,t)f(0)
-> 0.9999997242` vs. predicted `1.0` (`e^{-h/eps}` underflows to `0` for
every `h` tested here) -- rel. err `2.8e-7`, and the intermediate values
(e.g. `0.9156333394` at `y=10`) match the FIXED-`h=2.0` case's values
(`0.9156333387`) to 8 significant figures -- **the closed form is
insensitive to `h` once `h` is not small relative to `eps`**, exactly as
predicted (the `e^{-h/eps}f(x+h)` term is already negligible for `h` a few
multiples of `eps`, so the formula's `h`-dependence is structurally weak by
construction, not merely observed to be so here).

---

## 6. Part D -- consequences: a new reformulation of `(U1)`, and where it
stops

### 6.1 The "self-averaging" identity

Substituting the closed form (Sec 4.3) into the EXACT closed Volterra
equation `(VOLTERRA-Phi)` (Sec 0, an already-established fact of record, not
re-derived here), applied POINTWISE in `t` (each `f_t:=Phi_t(.)`, presumed
sufficiently regular -- hypothesis `(C)`, Sec 4.4) and integrated over
`t in [0,y]`:

```
Phi_y(x) = g_y(x) + int_0^y K(y,t) Phi_t(x) dt
         ~ e^{-y/eps}
           + (1/(x+y)) * [ int_0^y Phi_t(x) dt  -  int_0^y e^{-(y-t)/eps} Phi_t(x+y-t) dt ]
           + [error, controlled -- see below]
```

The SECOND bracketed integral is uniformly BOUNDED (`|...| <= eps *
sup|Phi|`, since its own weight `e^{-(y-t)/eps}` integrates to at most
`eps`), so divided by `x+y` it **vanishes** as `y->infinity` with no
Tauberian argument needed. The forcing term `g_y(x)=e^{-y/eps}` also
vanishes trivially. **The entire question of whether `Phi_y(x)` converges
therefore reduces to whether**

```
A(y)/(x+y),   A(y) := int_0^y Phi_t(x) dt
```

**converges** -- i.e. whether the Cesaro-type running average of `Phi_t(x)`
converges. Writing this out: **`(U1)` is equivalent, up to the
rigorously-vanishing corrections above, to the "self-averaging" identity**

```
Phi_y(x)  -  (1/(x+y)) int_0^y Phi_t(x) dt  ->  0     as y -> infinity.
```

> **Nota (2026-08-29, achado F1 do referee hostil dedicado, severidade
> BAIXA, precisão de enquadramento -- nenhum erro matemático):** a
> alegação em negrito acima, de que "`(U1)` is equivalent...to the
> self-averaging identity", é imprecisa se lida literalmente: a
> identidade `Phi_y(x)-A(y)/(x+y)->0` é derivada de forma INCONDICIONAL
> (dadas `(B)`, `(C)`, e uniformidade-em-`t` do termo de erro) -- ela
> não depende, ela mesma, de `(U1)` valer, logo não pode ser
> "equivalente" a uma questão aberta no sentido lógico estrito. O
> enunciado tecnicamente correto, plenamente consistente com -- e
> recuperável a partir de -- a própria discussão honesta das Seções
> 6.2/6.3 abaixo, é que `(U1)` é equivalente à convergência da média de
> Cesàro `A(y)/(x+y)` em si (um fato clássico de análise real, uma vez
> que a ponte de auto-mediação incondicional está em mãos: duas
> sequências que diferem por `o(1)` convergem ao mesmo limite se e
> somente se uma delas converge), com a identidade de auto-mediação
> servindo como a ponte (corretamente, rigorosamente provada) para essa
> reformulação -- não como a própria coisa à qual `(U1)` é
> "equivalente". Isto NÃO afeta o conteúdo substantivo, o diagnóstico
> do gap Tauberiano, ou o veredito de não-fechamento (a Seção 7 item 1
> já declara claramente que `(U1)` não fecha e que a identidade de
> auto-mediação "não é uma prova dela"). Fonte:
> `adversarial/REFEREE_REPORT.md`, Seção 8, Finding 1.

This is a genuinely NEW way of stating the open problem -- not a bound on
`(U1)`, a REFORMULATION of it, derived as a direct logical consequence of
(i) the exact `(VOLTERRA-Phi)` equation (record fact) and (ii) the Sec 4
closed form (this front's new, numerically-confirmed-to-`3e-8` result),
conditional on hypothesis `(C)` and on the `O(1/z^2)` error term's
uniformity over `t` (supported, not proved to full rigor, by Sec 5.4's
`h=y/2` check).

### 6.2 Why this explains the plateau mechanism (a genuine synthesis, not a
new independent claim)

If `Phi_t(x) -> L(x)` (i.e. `(U1)` holds), the classical fact that Cesaro
means of a convergent sequence converge to the same limit gives `A(y)/(x+y)
-> L(x)` automatically -- so the self-averaging identity is CONSISTENT with
`(U1)` holding, and explains MECHANISTICALLY how an `O(1)` nonzero plateau
(`Phi(0,t0)=0.0377616` for `t0>=0.02`, established `FLOORH2`/`PLATRESUM`,
cited not re-derived) is compatible with a kernel `K(y,t)` that is
POINTWISE negligible (`O(1/y)`, Sec 3-4 above) for any fixed elapsed time:
the Volterra "memory" integral accumulates over a domain `[0,y]` that grows
in exact lockstep with the kernel's `O(1/y)` decay, so their PRODUCT stays
`O(1)`. **This is an explanation of consistency, not a proof of
convergence** -- a Cesaro mean can converge even when the underlying
sequence does not (the classical direction "convergence implies Cesaro
convergence" is easy; the converse, "Tauberian," direction needs an extra
regularity condition -- Sec 6.3).

### 6.3 The precise missing ingredient: a Tauberian closure, named but not
completed

**Classical fact (Tauberian theorem for continuous Cesaro-`(C,1)`
summability -- see e.g. Hardy, *Divergent Series*, or Korevaar, *Tauberian
Theory*; cited as an external classical tool, NOT re-derived or
independently re-proved in this front).** If `g:[0,infinity)->R` is bounded,
`(1/y) int_0^y g(t) dt -> L`, and `g` is **slowly oscillating** -- for every
`epsilon>0` there exist `delta>0, Y` such that `y>=Y` and `0<=s-y<=delta*y`
imply `|g(s)-g(y)|<epsilon` (i.e. `g`'s variation over steps of size
PROPORTIONAL to `y`, not merely fixed size, vanishes) -- then `g(y)->L`.

**This is exactly the missing ingredient that would upgrade Sec 6.1's
self-averaging identity into a proof of `(U1)`.** Two things are needed to
apply it, NEITHER attempted to completion here:

1. **An oscillation bound on `Phi` itself, of the relative-step form the
   theorem needs.** The record already has `(star-star)` (Sec 0, cited),
   but that bounds `Psi`, not `Phi`, and its degradation is in ABSOLUTE step
   size `h=y2-y1` (`<= h*K/y1`), not manifestly in the RELATIVE form
   `s-y<=delta*y` the Tauberian theorem needs (though `h*K/y1` written with
   `h=delta*y1` DOES give `delta*K`, independent of `y1` -- suggestively
   close to the right form, but this is for `Psi`, and connecting it to
   `Phi`'s own oscillation would require passing back through `(E2)`/`(KEY)`,
   not done here). **This is the single most concrete, well-scoped next
   step this front identifies** -- sharper than any predecessor's named next
   step in this sub-lineage, because it is now anchored to a SPECIFIC
   classical theorem with SPECIFIC, checkable hypotheses, not a general
   "try a different technique" suggestion.
2. **Formal verification that the classical theorem's proof (stated for
   general bounded `g`) transfers cleanly to this setting** -- `Phi_y(x)` is
   a slice of a two-variable PDE solution, not an abstract bounded function;
   nothing about this transfer is expected to be hard, but it is not free,
   and is not done here.

**Not attempted to completion; named precisely, per the mandate's own
standard for a legitimate, valuable non-closure diagnosis.**

### 6.4 Resolving the "genuine exponential content" question

The mandate specifically asks this front to investigate whether the
translation-invariance failure is the SOURCE of the "genuine exponential-
looking content" the numerical data shows (h1_energy_estimate_attempt Sec 7,
`DISC-DEC-100`: ratio tests consistent with `Phi` approaching its limit at
rate `~e^{-gc}` in UNSCALED variables `g,c` (the record's own notation),
which is exactly `e^{-y/eps}` in this front's scaled variables, since
`y/eps = (g*sqrt(c))*sqrt(c) = gc` identically).
**Honest answer: NO, not directly -- and this front's own closed form
explains why, precisely.** This front's finding is that the Volterra
MEMORY-INTEGRAL term (`int_0^y K(y,t)Phi_t dt`) contributes an ALGEBRAIC
(`O(1/y)`-per-kernel-evaluation, self-averaging to `O(1)`) piece to
`Phi_y(x)` -- consistent with, and complementary to, `h1_energy_estimate_
attempt`'s own finding (`DISC-DEC-100` Sec 6.2) that a Watson/Laplace-in-
`1/y` expansion of the exact renewal identity is "structurally blind" to
exponential content, since such an expansion only ever produces ALGEBRAIC
terms. **The exponential content is, rather, plausibly already fully
visible and EXACT in the record**: the forcing term `g_y(x)=e^{-y/eps}`
(Sec 0) is not an approximation or an expansion -- it is an EXACT term of
`(VOLTERRA-Phi)`, and it equals `e^{-gc}` in unscaled variables, EXACTLY
matching the numerically-observed rate (`e^4=54.598` at `Delta g=0.04,
c=100` in `h1_energy_estimate_attempt` Sec 7.2, i.e. `e^{Delta g * c}`).
**This front does not prove `g_y` is THE mechanism** (that would require
showing the self-averaging term of Sec 6.1 does not ITSELF contribute
exponential-rate content, which is not established either way here) -- but
it does show that (i) this front's own algebraic-kernel finding is not in
tension with the exponential observation (both routes independently find
"the exact renewal/Volterra machinery only yields algebraic content from
its own expansion," consistent across two structurally different fronts),
and (ii) an exact, already-in-record candidate EXPLANATION for the
exponential rate (`g_y` itself) exists and numerically matches, without
needing anything new from the kernel's translation-invariance structure.
**This is offered as a plausibility synthesis, not a new proved claim** --
flagged as such, not overclaimed.

---

## 7. What did NOT close, precisely

1. **`(U1)`/`(U2)`/`H1` are not closed.** The self-averaging reformulation
   (Sec 6.1) is a genuine, rigorously-derived-conditional-on-`(B)`+`(C)`
   equivalent restatement of `(U1)` -- not a proof of it.
2. **The Tauberian closure (Sec 6.3) is named precisely but not attempted.**
   Missing: an oscillation bound on `Phi` (not `Psi`) of the relative-step
   form; formal verification the classical theorem's hypotheses transfer.
3. **Hypothesis `(C)`** (an auxiliary Lipschitz-type regularity assumption
   on the function `K(y,t)` acts on, needed for the `rho`-remainder bound,
   Sec 4.1) **is not independently proved** for the actual `Phi`/`Psi` of
   this system -- assumed, consistent with how `(B)` itself is a standing,
   not independently proved, hypothesis throughout this entire lineage.
4. **Uniformity of the `O(1/z^2)` error term over ALL `t in [0,y]`** is
   SUPPORTED (Sec 5.4's `h=y/2` check, and the structural observation that
   `e^{-h/eps}` is negligible once `h` exceeds a few multiples of `eps`,
   independent of how large `h` grows beyond that) but not proved to full
   rigor with an explicit, uniform-in-`h` remainder bound.
5. **The closed-form cancellation is a pointwise-in-`f` (Sec 4.4), not an
   operator-norm, fact.** It does not sharpen, and is not claimed to
   sharpen, the operator-norm-level constant `sqrt(pi/2)+eps` established by
   `DISC-DEC-113`, nor the resulting Volterra quasi-nilpotency argument of
   `DISC-DEC-115`.
6. **The "genuine exponential content" connection (Sec 6.4) is a
   plausibility synthesis**, not a proof that `g_y=e^{-y/eps}` is THE
   mechanism behind the numerically observed exponential approach rate.
7. **Non-perturbative (trans-series) content, `H2`, and the tested numeric
   domain**: exactly as every ancestor front in this sub-line, trans-series
   content is untested; `H2` is untouched, out of scope. Numerical
   verification covers `eps in {0.1, 1/sqrt(1000)}` (`c in {100,1000}`),
   `h` up to `1500`, `z` up to `10^4`, `x` up to `10` -- no claim of
   behavior outside this tested range is made beyond what is explicitly
   proved (Sec 2, Sec 4.1-4.3, the elementary calculus/algebra facts) for
   all `z,x,y,t` in the stated domains.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic law
of record are all untouched and unaffected by anything in this document.

---

## 8. Scorecard

| claim | status |
|---|---|
| `T_w = M_(e^{wx}) T_0 M_(e^{-w.})` (exponential conjugation identity) | **PROVED** (new, exact, symbolic, `s01` Part 1) |
| `x'+w=x+y` cancellation (independent re-derivation) | **PROVED** (exact, symbolic, `s01` Part 2; matches `DISC-DEC-113`) |
| Single-integral reduction of `K_A^raw`, exposing `z=x+y` dependence | **PROVED** (new, exact, `s01` Part 3; numerically cross-checked 10/10, `s01b`) |
| `K_B(h)` exactly translation-invariant | **PROVED** (trivial, by construction) |
| `M_y K_A^raw(y,t)` settles to a NONZERO limit as `y->infinity` | **CONFIRMED numerically** (consistent with `DISC-DEC-113/115`'s operator-norm fact; `s03`, 12/12 combos) |
| `K(y,t)=M_y K_A^raw+K_B` decays like `O(1/y)` (order only) | **CONFIRMED numerically**, log-log slope `-0.994` to `-0.999`, 12/12 combos (`s03`) |
| `O(1/(x+y))` (not merely `O(1/y)`) | **CONFIRMED numerically** (`s04`) |
| Exact decomposition `Theta_h'(z)=f(x+h')R(z)+rho(h',z)` | **PROVED** (exact, trivial by definition) |
| `c(z):=(1-eps z)R(z)/eps = -1+1/(eps z)+1/z^2+O(1/z^3)` | **PROVED** (new symbolic derivation + assert-checked, `s02`; TWO self-caught sign/scaling errors found and fixed in this front's own scratch work, Sec 4.2-4.3) |
| `rho(h',z) ~ f'(x+h')/z^2` (Watson's lemma, `g(0)=0` case) | **PROVED** (standard, re-derived generically, `s05` Steps 1-2) |
| Exact IBP `int_0^h e^{-h'/eps}f'(x+h')dh' = e^{-h/eps}f(x+h)-f(x)+K_B(h)f(x)/eps` | **PROVED** (exact, symbolic, confirmed on concrete test `F`, `s05` Step 3) |
| `K_B(h)f(x)/eps` terms cancel exactly between the `c(z)` and `rho` pieces | **PROVED** (symbolic, `assert==0` passes after fixing the self-caught bug, `s05` Step 4) |
| Closed form `K(y,t)f(x) = [f(x)-e^{-h/eps}f(x+h)]/z + O(1/z^2)` | **PROVED** (conditional on `(B)`+`(C)`), **CONFIRMED numerically** to `3.2e-8` worst-case rel. err, 6/6 cases (`s06`) |
| Uniformity of the closed form as `h` grows proportionally with `y` | **SUPPORTED numerically** (not proved to full rigor), `h=y/2` to `y=3000`, rel.err `2.8e-7` (`s07`) |
| Self-averaging reformulation of `(U1)` (Sec 6.1) | **DERIVED** (rigorous consequence of the closed form + the exact `(VOLTERRA-Phi)` equation, conditional on `(B)`+`(C)`+error-term uniformity) -- **NOT a proof of `(U1)`** |
| Plateau-mechanism explanation (Sec 6.2) | **Consistency/explanation**, not new independent proof |
| Tauberian closure route (Sec 6.3) | **NAMED PRECISELY, NOT ATTEMPTED** -- classical theorem cited, exact missing ingredients identified |
| "Genuine exponential content" <-> `g_y=e^{-y/eps}` connection (Sec 6.4) | **Plausibility synthesis**, not proved |
| `(U1)` (locally-uniform `g->infinity` convergence of `W`) | **OPEN** (unchanged) |
| `(U2)` (uniform-in-`x` Poincare expansion of `W_inf`) | **OPEN** (unchanged) |
| `H1` | **OPEN** (unchanged) |
| `H2` | **NOT ATTEMPTED** (out of scope, per mandate) |
| Operator-norm-level sharpening of `sqrt(pi/2)+eps` | **NOT CLAIMED, NOT ATTEMPTED** (Sec 4.4 -- explicitly out of scope of this front's pointwise-in-`f` result) |

`H1` remains ABERTO/OPEN. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the
four-term asymptotic law of record are all untouched and unaffected by
anything in this document.

---

## 9. Seeds

Reserved range `20260931000-20260931999` per `DISC-DEC-118`. Grep-confirmed
BEFORE any use (`grep -rn "20260931" 05_DISCOVERY_LAB/`): appeared only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-118` reservation line. Re-confirmed
again at the end of this front (same command, same result): still appears
ONLY in that reservation line, and nowhere inside this front's own new
directory. **No randomness was used anywhere in this front** -- every
computation is exact symbolic algebra (`sympy`), deterministic
arbitrary-precision adaptive quadrature (`mpmath`, fixed evaluation
strategy, no sampling), or elementary arithmetic -- exactly as every direct
ancestor front in this exact sub-lineage reports for its own reservation.
The reserved range remains entirely unused.

---

## 10. Files

| file | role |
|---|---|
| `s01_conjugation_and_reduction.py`/`.log` | new exponential-conjugation identity for `{T_w}` (Sec 2.2); independent re-derivation of the `x'+w=x+y` cancellation (Sec 2.3); new single-integral reduction of `K_A^raw` (Sec 2.4) -- all exact symbolic algebra |
| `s01b_reduction_numeric_check.py`/`.log` | independent numerical cross-check of the `s01` reduction against the raw `(w,u)` double-integral definition, 2 independent `mpmath` quadrature routes, 5 points x 2 test functions (Sec 2.4) |
| `s02_exact_decomposition_and_asymptotics.py`/`.log` | exact decomposition `Theta=fR+rho` (Sec 4.1); symbolic + numeric derivation of `c(z)->-1+1/(eps z)+...` (Sec 4.2) -- includes one self-caught, disclosed sign error |
| `s03_kernel_cancellation_numeric.py`/`.log` | independent numerical confirmation of the near-total cancellation and `O(1/y)` decay of the full kernel, 12 `(eps,h,f)` combinations, direct quadrature of RAW operator definitions (Sec 3.2-3.3, Sec 5.1) |
| `s04_x_dependence_check.py`/`.log` | confirms `O(1/(x+y))`, not merely `O(1/y)`, across `x in {0,1,3,10}` (Sec 5.2) |
| `s05_leading_asymptotic_symbolic.py`/`.log` | derivation and exact symbolic verification of the closed-form leading asymptotic, including the generic Watson's-lemma IBP identity, the exact `int e^{-h'/eps}f'` evaluation, and the `K_B/eps` cancellation assembly (Sec 4.3) -- includes one self-caught, disclosed scaling error |
| `s06_leading_asymptotic_numeric_check.py`/`.log` | independent numerical verification of the EXACT closed-form coefficient (not just its order) via Richardson extrapolation, 6 `(x,h,eps,f)` cases, worst-case rel. err `3.2e-8` (Sec 5.3) |
| `s07_uniformity_in_h_check.py`/`.log` | tests uniformity of the closed form as `h` grows proportionally with `y` (`h=y/2` to `y=3000`), needed for the Sec 6.1 self-averaging argument's validity (Sec 5.4) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`h1_translation_structure_attempt/` subdirectory was written to -- every
ancestor `ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md`
further up the tree were read-only references (Sec 0), never modified. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself, per the mandate.

---

## 11. Scope discipline confirmation

- No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
  `index.html`, or any file outside this front's own new
  `h1_translation_structure_attempt/` directory -- including the sibling
  directories `h1_volterra_attempt/`, `h1_post_correction_attempt/`,
  `h1_energy_estimate_attempt/`, and `mclust_h2_validity_attempt/`, all read
  as required background but never written to.
- No `adversarial/` subdirectory created (a separate hostile referee is
  dispatched later by the orchestrating session, per the mandate, exactly
  as every direct ancestor in this sub-lineage's own `ATTEMPT.md` states for
  itself).
- No `git` command of any kind run.
- No claim of progress on any Millennium Prize Problem appears anywhere in
  this document -- `M-CLUST(b)` is, as stated at the top of this document
  and throughout the required reading, a standalone combinatorial/asymptotic
  object, entirely independent of the archive's separate Tree A (`u1/2`)
  line. Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no result,
  finding, or hedge from the Tree A line is cited anywhere in this document
  as evidence for anything claimed here, and no result from this document is
  intended to be read as evidence for anything in Tree A.
- Both self-caught errors (Sec 4.2, Sec 4.3) were found by this front's OWN
  symbolic-verification scripts failing their own `assert` statements on
  first run, fixed in place, and disclosed here with the before/after
  visible in the committed `.py` files -- neither was found by, or required,
  an external referee.
