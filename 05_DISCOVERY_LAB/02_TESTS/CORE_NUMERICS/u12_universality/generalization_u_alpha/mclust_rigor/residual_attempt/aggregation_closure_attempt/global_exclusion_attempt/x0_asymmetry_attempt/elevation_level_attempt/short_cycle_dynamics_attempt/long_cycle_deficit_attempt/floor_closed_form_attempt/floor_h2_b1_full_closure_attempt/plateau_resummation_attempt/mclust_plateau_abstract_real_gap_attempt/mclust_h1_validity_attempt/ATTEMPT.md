# ATTEMPT — uniform validity of the matched outer/inner decomposition
# (H1), plateau resummation lineage (`MCLUST-H1-VALIDITY-ATTEMPT`)

**Wave 20, front (c), `DISC-DEC-088`.** Target: `H1`, one of two named
heuristic gaps left open by `plateau_resummation_attempt` (`DISC-DEC-072/
077`) and left untouched by `mclust_plateau_abstract_real_gap_attempt`
(`DISC-DEC-083/085`, which explicitly declined to attempt H1/H2, §B.5 of
that document) — the assumption, stated but not proved, that the
Watson/matched-layer (outer/inner boundary-layer) asymptotic
decomposition used to derive the 4-term asymptotic law for the M-CLUST(b)
plateau constant `Pi(c)` is **uniformly valid**, not merely formally
consistent order-by-order.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`), the `b=1`
floor's abstract `(s,g)` recursive process — pure combinatorial/asymptotic
mathematics about a random-permutation-with-reroutes ensemble. It is a
standalone object, entirely independent of the archive's separate Tree A
(`u1/2` / "Lemma Aberto") line in `THEOREM.md`. Nothing here is, or is
adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

Reserved seed range for this front: `20260894000-20260894999`
(`numpy.SeedSequence` base) — grep-confirmed to appear only in the
ledger's/queue's reservation lines before use. **In the end no randomness
was needed anywhere in this front**: every result below is either exact
symbolic/analytic reasoning or deterministic arbitrary-precision (`mpmath`,
`dps` between 50 and 110 depending on the sub-computation) series
summation, so the reserved range remains entirely unused, exactly as in
`plateau_resummation_attempt` and `mclust_plateau_abstract_real_gap_attempt`
before it.

---

## EXECUTIVE SUMMARY (read first)

**Tier: genuine, non-trivial progress — a theoretical reduction of H1 to
two smaller, precisely-stated sub-hypotheses, plus wide-ranging,
independent high-precision numerical evidence for uniform validity across
a domain substantially larger than any ancestor front tested — but NOT a
proof.** H1 is **not closed**.

1. **Theoretical reduction.** Working from the EXACT (not asymptotic)
   renewal representation of the plateau limit already established in the
   required reading (`Phi(x,y) = e^{-y/eps} + (1/eps)\int_0^y e^{-v/eps}
   W(x+v,y-v)\,dv`), this front proves a precise **Watson-concentration
   lemma** (§2.1): *if* `W(x,g)` converges to a limit `W_inf(x)` as
   `g\to\infty`, **locally uniformly in `x`** (a specific, checkable
   condition, named `(U1)` below — strictly weaker than assuming the
   whole matched-asymptotics machinery), *then*

   ```
   Pi(c) = Phi(0,infty) = (1/eps) * int_0^infty e^{-v/eps} * W_inf(v) dv     (STAR)
   ```

   **exactly**, with no further approximation at this step. `H1` then
   reduces exactly to the conjunction of `(U1)` and a second, separate
   condition `(U2)`: that `W_inf(x;eps)` itself admits a genuine,
   uniform-in-`x` asymptotic (Poincaré) expansion in `eps` as `eps\to0`,
   valid down to the boundary-layer scale `x=O(eps)` — this is where the
   classical, rigorous theory of Watson's lemma with explicit error bounds
   *would* apply, but only once `(U2)` is independently established. Full
   closure of `H1` still needs `(U1)`+`(U2)` proved from the exact PDE
   system, which was **not attempted** here — a substantially larger
   undertaking, consistent with the mandate's own risk assessment.

2. **A second, independent exact structural fact.** This front derives
   (§2.3) — from the same exact system, under separately-stated
   integrability/regularity conditions, and independently of the
   Watson-concentration lemma — an **exact, closed, first-order linear ODE
   for the plateau profile itself**: `F'(x) - x*F(x) = -C(x)`, with
   `C(x) := int_0^infty [Phi(x,y')-F(x)] dy'`. This is new to the record
   (not stated in any required-reading document); it is consistent with
   (reduces to) the record's own leading-order `psi1` equation, a
   consistency check performed here (§2.3). It narrows exactly WHERE the
   heuristic content of `H1` lives (in expanding `C(x)` order-by-order in
   `eps`, not in the exactness of `F`'s governing equation itself) —
   again, conditional on stated hypotheses, not a closure.

3. **Numerical uniformity test — the main result of this front, by
   volume of evidence.** A **fresh, from-scratch implementation of the
   `(P,Q)`-family recursion at GENERAL `s`** (not just `s=0`, extending
   what any ancestor front computed) is built (§3.1), validated against
   **7/7 published numeric anchors at `c=1000`** (§3.2) plus an
   **independent re-derivation of `psi3(x)` in closed integral form**
   (§3.3, via the same bounded-branch variation-of-parameters method used
   throughout this lineage for `R(x)` itself), verified to `~30` digits
   against the record's own `psi3(0)=(7/2)\sqrt{\pi/2}` and against the
   record's own two published `resid3` spot values (`4.058` at `c=1000`,
   `4.175` at `c=2560`) — **matched exactly** by this front's independent
   pipeline (§3.4), a strong cross-validation before any new claim is
   made.

   Using this machinery, a grid of **6 `c`-values (`200` to `8000`) times
   7 `x`-values (`0` to `8`)** — wider in `x` by nearly `3\times` and
   covering both smaller and larger `c` than the record's own 2-value,
   5-`x`-value spot check (`plateau_resummation_attempt/ATTEMPT.md`
   §6) — measures, at TWO successive orders, the ratio of the measured
   remainder to the derived NEXT-order prediction (`\rho_1/\psi_3(x)` and
   `\rho_2/\psi_4(x)`, using the record's own closed forms `\psi_3,\psi_4`
   — the latter re-derived here in closed integral/derivative form, §3.3).
   **At every one of the 42 grid points, at both orders, this ratio
   converges toward `1` as `eps\to0`** (§4.2), and a per-`x` linear
   (Richardson-type) extrapolation to `eps=0` lands within `0.04\%`–`0.8\%`
   of `1` at every tested `x`, **monotonically TIGHTER (not looser) as `x`
   grows** (§4.2, verified explicitly monotone at both orders) — the
   opposite of what a genuine non-uniformity (error blowing up away from
   `x=0`) would look like.

4. **An explicit stress test into unphysical territory, with a
   self-caught numerical pitfall, disclosed.** Pushing `x` to `20` (at
   `c=200`, `s=x/\sqrt c` reaches `1.41`, well beyond the process's
   presumed physical domain `s\in[0,1]`) with the SAME `(K,\text{dps})`
   sizing used for the main grid produced an apparent, dramatic
   "blow-up" of the uniformity ratio (`\sim1.4\times10^4` at `x=20`) —
   caught by this front's own two-`t_0` convergence diagnostic as **pure
   numerical non-convergence** (the direct-summation series, at large
   `x`, suffers the SAME order-2-entire cancellation cost wall the record
   already documents for small `c`; §5.1). Rerunning with `K=800,
   \text{dps}=90` (up from `K=400,\text{dps}=60`) restores full
   convergence, and the uniformity ratio at `x=20` is `0.983` — **squarely
   consistent with, and continuing, the same clean trend** as the rest of
   the grid. **No counterexample or failure mode of H1 was found**, even
   in this extended, partly-unphysical stress region.

5. **Explicit, honest limitations (§6).** This is order-1/order-2
   (and, via `psi_4`, effectively order-2/order-3) numerical evidence
   only — it CANNOT rule out non-perturbative (trans-series) content
   invisible to any finite number of orders, which is exactly the
   structural concern the `plateau_resummation_attempt` referee raised
   about `Phi(0,\cdot)` being entire of order 2 (a growth class where
   such content is common) and which `mclust_plateau_abstract_real_gap_
   attempt` left completely untouched. `(U1)` and `(U2)` are stated
   precisely but **neither is proved** from the exact PDE system; that
   remains the single largest gap relative to a full closure. `H2`
   (uniqueness of the bounded-order solution) is **not attempted** here
   at all, exactly as the mandate scoped this front to `H1`.

`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and every formula of record:
**untouched.** No claim of a proof of the 4-term (or any) asymptotic law
is made anywhere below. No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing.
No `adversarial/` subdirectory created; no referee dispatched. No git
command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `PROOF_DEPENDENCY_
MAP.md` §2 (Tree B), specifically the `FLOORH2` and `PLATRESUM` nodes and
BOTH dated addenda under `PLATRESUM` (wave-17, `DISC-DEC-072/077`; wave-19,
`DISC-DEC-083/085`); the full `mclust_plateau_abstract_real_gap_attempt/
ATTEMPT.md` (predecessor front, same directory tree, §A.2–§A.4 in
particular for the exact statement of the two post-adversarial corrections
N1/N2 to that front); and the full `plateau_resummation_attempt/ATTEMPT.md`
(direct parent), in particular §4 (the matched-asymptotics derivation),
§4.5 (the EXACT statement of `H1`/`H2`, quoted verbatim below), and §6
(the record's own 2-value, 5-`x`-value profile spot check, which this
front's §4 extends substantially).

**No `.py` file from any front in the `mclust_rigor` lineage — this front's
own ancestors down through `mclust_plateau_abstract_real_gap_attempt` — was
opened, read, or imported at any point.** Every script in this directory
(`k01`–`k07`) was written fresh, from the mathematical content of the
prose cited above; every previously-published number used as a
cross-check (anchors, `resid3` values, `psi_n(0)` closed forms) is
transcribed as plain text, never imported as code.

**The exact statement of H1, quoted verbatim** (`plateau_resummation_
attempt/ATTEMPT.md` §4.5, "Status of the derivation (honest)"):

> Exactly TWO steps are heuristic (named, not hidden): (H1) the
> Watson/matched-layer framework itself — smoothness and uniform validity
> of the outer/inner decomposition and the `O(eps^n)` remainder bounds are
> assumed, not proved; (H2) uniqueness of the `y`-independent bounded
> solution at each order (proved only within fields where the
> `y`-differentiated homogeneous equation's `e^{xy+x^2/2}` growth can be
> excluded by boundedness).

This front's mandate is `H1` only; `H2` is not attempted (consistent with
`mclust_plateau_abstract_real_gap_attempt`'s own explicit scoping, §B.5 of
that document, which also left both untouched).

**The established inputs this front works from** (restated for
self-containedness, exactly as quoted in the two required-reading
documents — not re-derived except where explicitly marked "re-derived"
below):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Series-recursion (Phi(s,g)=sum a_k(s)g^k, Psi(s,g)=sum b_k(s)g^k):
  a_0=1, b_0=0, a_1(s)=-c, b_1(s)=sqrt(pi c/2)*erfcx(s*sqrt(c/2))
  a_{k+1}(s) = [a_k'(s) - c a_k(s) + c w_k(s)] / (k+1)
  b_k'(s) - c s b_k(s) = -c a_{k-1}(s)/k + c b_{k-1}(s)      (bounded branch)
  w_k(s) = a_{k-1}(s)/k + (1-s) b_k(s) - b_{k-1}(s)
  every a_k, b_k in F = {P(s) + Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials

Governing PDE system:
  dPhi/ds - dPhi/dg = c[Phi-W],   dPsi/ds = c[Psi-W]
  W = g*Avg_g[Phi] + (1-s-g)*Psi,   Avg_g[Phi] = (1/g) int_0^g Phi dg'
  Phi(s,0)=1;  target Phi(0,t0), plateau Pi(c) := lim_{t0->inf} Phi(0,t0)

Exact reformulation in (x,y) (plateau_resummation_attempt Section 4.1):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                          (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv   (E2)

Derived 4-term law (Pi(c)*sqrt(2c/pi) =: y(eps) = sum d_j eps^j):
  d0=1, d1=-2 sqrt(2/pi), d2=7/2, d3=-(34/3) sqrt(2/pi)
  psi1(x)=R(x):=sqrt(pi/2)*erfcx(x/sqrt2),  R'=xR-1,  R(inf)=0
  psi2(x) = 2 x R(x) - 2                      [psi2(0)=-2=d1... wait
    d_n and psi_n(0) are related by psi_n(0)=gamma_n*R^{(n-1)}(0); the
    d_j table above is the eps-expansion AT x=0, i.e. Pi(c) itself]
  psi4(x) = (17/3) R'''(x)                    [psi4(0) = -34/3]
  Pi(1000) = 0.0377615983402126188243712025905770479904...
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory was written to.

---

## 1. Overview of approach

Two independent lines of attack, both aimed squarely at `H1`:

- **Part A (§2, theoretical).** Work directly with the EXACT `(x,y)`
  system `(E1)`/`(KEY)`/`(E2)` — not its asymptotic expansion — to see how
  much of the informal "boundary-layer matching" step can be replaced by
  a genuine, provable (if conditional) statement. This is new analysis,
  not present in either required-reading document, built from the exact
  identities they establish.
- **Part B (§3–§5, numerical).** Build a fresh, independent
  implementation of the exact series recursion at GENERAL `s` (not just
  `s=0`), and use it to directly, quantitatively test the one thing `H1`
  actually claims and no ancestor front checked systematically: that the
  matched-asymptotics remainder stays the SAME ORDER `O(eps^{n+1})`
  **uniformly as `x` ranges over an extended domain**, not just
  pointwise at a handful of `x` values close to `0`.

Both lines report their own honest limits; neither closes `H1`.

---

## 2. Part A — theoretical reduction

### 2.1 The Watson-concentration lemma

**Setup.** Fix `x0`, `eps>0`. From `(E2)`:

```
Phi(x0,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x0+v, y-v) dv
```

**Hypothesis (U1).** There is a function `W_inf(x)` (for the fixed `eps`
under consideration) such that: for every `delta>0` there is `G(delta)`
with `|W(x', g') - W_inf(x')| < delta` for ALL `g' > G(delta)` and ALL
`x' in [x0, x0+G(delta)]` (i.e. local uniformity of the `g\to\infty`
convergence, over exactly the window of `x'` values the convolution in
`(E2)` sweeps as `v` ranges over `[0,y]` at `x=x0`).

**Lemma.** Under `(U1)`, assuming also `W` is bounded (a standing
assumption throughout this lineage, `Phi,Psi` being probability-related
quantities bounded on `[0,1]`-type ranges — consistent with, not proved
beyond, the required reading):

```
lim_{y->infty} Phi(x0,y) = (1/eps) * int_0^infty e^{-v/eps} W_inf(x0+v) dv     (STAR)
```

**Proof.** Split the `v`-integral at `v=G(delta)`. For `y>2G(delta)`, on
`v\in[0,G(delta)]` we have `y-v>G(delta)`, so `(U1)` gives `W(x0+v,y-v) =
W_inf(x0+v) + O(delta)` uniformly in `v` on this range; extending the
resulting `v`-integral of `W_inf` to `[0,\infty)` incurs an error
`O(\sup|W_inf|\cdot e^{-G(delta)/eps})` (the omitted tail of the `e^{-v/
eps}` kernel), independent of `y`. The complementary piece,
`(1/eps)\int_{G(delta)}^y e^{-v/eps}W(x0+v,y-v)\,dv`, is bounded in
absolute value by `\sup|W|\cdot e^{-G(delta)/eps}` regardless of how
large `y` is (the kernel mass beyond `G(delta)` is exactly
`e^{-G(delta)/eps}`) — this term does **not** vanish merely by taking
`y\to\infty` at `eps` fixed; it is bounded, not zero, at this stage.
Combining: for every `delta>0`,

```
| lim_{y->inf} Phi(x0,y) - (1/eps) int_0^inf e^{-v/eps} W_inf(x0+v) dv |
    <= O(delta) + O(sup|W| * e^{-G(delta)/eps})
```

Since this holds for every `delta>0` (with `G(delta)\to\infty` as
`delta\to0`, `eps` held fixed, by the definition of `(U1)`), both error
terms can be sent to `0` by letting `delta\to0`, proving `(STAR)`. **QED**
(elementary real analysis; no heuristic step anywhere in this proof,
conditional only on `(U1)` and boundedness).

**Reading.** `(STAR)` is the precise, provable content behind the
record's informal "boundary layer matching" — but note it is genuinely
NOT the naive statement "`Phi(x0,\infty)=W_inf(x0)`" (an earlier internal
draft of this argument, superseded before being used for anything,
initially derived exactly this simpler-looking but WRONG conclusion — see
disclosed self-caught issue S1, §7). Because `eps` is held fixed while
`y\to\infty`, the exponential kernel does **not** collapse to a point
mass at `v=0`; `(STAR)` is a genuine convolution over the WHOLE
half-line `v\ge0`, and only a SECOND, separate limit (`eps\to0`, taken
afterward) can turn it into an expansion localized near `v=0`. This
distinction is exactly `H1`'s "uniform validity ... down to the
boundary-layer scale" content, made precise for the first time here.

### 2.2 Reduction of H1 to (U1) + (U2)

Given `(STAR)`, expanding `Pi(c) = (1/eps)\int_0^\infty e^{-v/eps}
W_inf(v;eps)\,dv` (at `x0=0`) in powers of `eps` as `eps\to0` is now,
IF `W_inf(\cdot;eps)` itself had a FIXED (eps-independent) integrand,
exactly the setting of the classical Watson's lemma — a completely
rigorous, textbook result (Olver, *Asymptotics and Special Functions*,
Ch. 2–3) with EXPLICIT, provable error bounds, given only that the
integrand has a valid Taylor-type expansion near `v=0` with a controlled
remainder. The genuine difficulty — and the reason this is NOT a trivial
application — is that `W_inf` itself depends on `eps` (through the whole
coupled system), so a second condition is needed:

**Hypothesis (U2).** `W_inf(x;eps)`, as a function of `x\ge0` for each
`eps`, admits a genuine asymptotic (Poincaré) power series in `eps` as
`eps\to0`, **uniformly for `x` in `[0,\infty)`** (in particular, remaining
valid down to `x=O(eps)`, the boundary-layer scale that dominates the
Watson-type integral in `(STAR)` once `eps` is also sent to `0`), with a
remainder after `N` terms that is `O(eps^{N+1})` with a constant
independent of `x`.

**Claim: `H1` (as it concerns deriving `Pi(c)` via this route) is exactly
the conjunction of `(U1)` and `(U2)`.**
**[Nota pós-adversarial, 2026-08-26 — DISC-DEC-091, sem correção — o
referee hostil não encontrou nenhum erro matemático nesta frente.] O
referee observou que esta frase reivindica uma equivalência, mas o que
de fato é mostrado é que `(U1)+(U2)` são SUFICIENTES para recuperar a
lei de 4 termos rigorosamente via o lema de Watson — necessidade (que
nenhuma outra rota para `H1` poderia evitar precisar de algo equivalente
a `(U1)`/`(U2)`) não é, e não seria facilmente, estabelecida. O
qualificador "(as it concerns deriving `Pi(c)` via this route)" já
presente no texto amplamente neutraliza esta observação; o referee
classificou-a como achado de severidade negligível/retórica, não
contada como issue formal, e nenhuma alegação posterior no documento
depende de necessidade — apenas de suficiência, usada corretamente ao
longo de todo o texto.**
Given both, the classical rigorous
Watson's-lemma machinery applies to `(STAR)` and delivers the 4-term law
(and any further term) with an explicit, provable remainder bound — no
further heuristic step would remain. **Neither `(U1)` nor `(U2)` is
proved by this front** from the exact PDE system (`dPsi/ds=c[Psi-W]` etc.)
— doing so would require, at minimum, a maximum-principle or
energy-estimate argument establishing that `Psi(x,g)` (and its
`x`-derivative) converges to its `g\to\infty` limit at a RATE that is
itself uniform in `x` over an unbounded domain, which is a substantially
larger undertaking than this front's budget, and was not attempted. What
IS achieved: `H1`'s single, monolithic "the whole matched-asymptotics
framework is assumed valid" is replaced by two independent, more
narrowly-scoped, precisely-stated analytic conditions, one of which
(`(U1)`) is now the exact hypothesis under which a clean, rigorous
QED-proof (§2.1) already exists — closing the GAP BETWEEN `(U1)`+`(U2)`
and `H1` itself, even though `(U1)` and `(U2)` remain themselves open.

### 2.3 An exact ODE for the plateau profile `F(x)` (new structural fact)

Write `F(x) := \lim_{y\to\infty}\Phi(x,y)` (so `F(0)=Pi(c)`; `F(x)/eps
\to \psi_1(x)` etc. as `eps\to0`, but here `F` is treated at FIXED `eps`,
exactly, no expansion). From `(E1)`: `Psi_x(x,y) = (x+y)Psi(x,y) -
I(x,y)`, `I(x,y)=\int_0^y \Phi(x,y')\,dy'`.

**Hypotheses (stated explicitly, not proved):** (i) `\Phi(x,\cdot)-F(x)`
is integrable on `[0,\infty)`, with `C(x):=\int_0^\infty[\Phi(x,y')-F(x)]
\,dy'` finite; (ii) `\Psi(x,y)-F(x) = o(1/y)` as `y\to\infty` (in
particular satisfied if the approach is exponential, `\sim e^{-y/eps}`,
as the record states, Section 0 above); (iii) `\lim_{y\to\infty}\Psi_x(x,y)
= F'(x)` (an interchange-of-limits condition, itself a form of local
uniformity akin to `(U1)`).

**Derivation.** Write `I(x,y) = y\,F(x) + [I(x,y)-yF(x)]`, and
`I(x,y)-yF(x) = \int_0^y[\Phi(x,y')-F(x)]\,dy' \to C(x)` by (i). Then

```
Psi_x(x,y) = x*Psi(x,y) + y*[Psi(x,y)-F(x)] - [I(x,y)-yF(x)]
```

For `\lim_{y\to\infty}\Psi_x(x,y)` to exist finitely (needed for (iii)),
the middle term `y\cdot[\Psi(x,y)-F(x)]` must have a finite limit; if
`\lim_{y\to\infty}\Psi(x,y) \ne F(x)`, this term diverges linearly — a
contradiction — so **`\lim_{y\to\infty}\Psi(x,y) = F(x)` is forced**
(`\Phi` and `\Psi` share the same `g\to\infty` limit; not previously
stated this way in either required-reading document).
**[Nota pós-adversarial, 2026-08-26 — DISC-DEC-091, sem correção — o
referee hostil não encontrou nenhum erro matemático nesta frente.] O
referee observou que este aside "forçado" é redundante com a hipótese
(ii), já assumida (`\Psi(x,y)-F(x)=o(1/y)`, uma afirmação mais forte —
uma taxa — do que a mera convergência `\Psi(x,y)\to F(x)` que este
aside estabelece). A derivação efetiva de `(ODE-F)` logo abaixo usa a
hipótese (ii) diretamente ("Given (ii), the middle term itself `\to
0`"), não este aside "forçado" — então este parágrafo não acrescenta
conteúdo além do que (ii) já concede, e a formulação "not previously
stated this way" superestima levemente sua novidade/independência. Não
afeta a correção de `(ODE-F)` nem nenhuma alegação posterior — é uma
questão de rotulagem em um parágrafo, não uma lacuna matemática;
classificado pelo referee como achado de severidade negligível/
cosmética, não contado como issue formal.]** Given (ii), the
middle term itself `\to 0`. Combining with (iii):

```
F'(x) - x*F(x) = -C(x)                                      (ODE-F)
```

**Consistency check (this front, not a new derivation of `psi1`).** At
leading order `eps\to0`, `F(x)\approx eps\,\psi_1(x)` and — by the SAME
bookkeeping — `C(x)` should be `\approx eps\cdot(\text{const})`; plugging
into `(ODE\text{-}F)` gives `\psi_1'(x)-x\psi_1(x) = -(\text{const})`,
matching the record's own leading-order equation `\psi_1'=x\psi_1-1`
(i.e. the constant is exactly `1`) **exactly**, a genuine (if
leading-order-only) cross-check that `(ODE\text{-}F)` is consistent with
the established derivation. This front did **not** independently verify
`(ODE\text{-}F)` numerically beyond this leading-order check (it would
require tabulating `\Phi(x,y)` over a `y`-grid and numerically integrating
`C(x)`, a separate computational undertaking not executed here — named as
a concrete next step, §6).

**Reading.** `(ODE\text{-}F)` isolates the heuristic content of `H1` one
layer further: `F`'s own governing equation is EXACT (modulo hypotheses
(i)-(iii), themselves unproved but more localized/checkable than "the
whole framework"); the only remaining approximation is in expanding
`C(x)` — which depends on the FULL function `\Phi`, not just its limit —
order-by-order in `eps`. This does not close `H1`, but is a genuinely new
exact structural fact, absent from both required-reading documents.

---

## 3. Part B — numerical machinery: fresh general-`s` implementation

### 3.1 Implementation

`k01_family_series.py` implements the `(P,Q)`-family recursion of Section
0 above **at general `s`** (polynomial-pair representation `(P,Q)` for
`P(s)+Q(s)\,\mathrm{erfcx}(s\sqrt{c/2})`), built entirely from the prose
recursion and the family-closure/descending-recursion/`\kappa`-pinning
method described in `plateau_resummation_attempt/ATTEMPT.md` §1.1 (quoted
in Section 0 above), independently re-derived by hand (worked through
step-by-step before any code was written) and then implemented. Key
components: polynomial arithmetic (`p_add`, `p_mul_one_minus_s`,
`p_deriv`, `p_antideriv`, `p_eval`), the family differentiation rule
`(P+QE)' = (P'-sc\,Q) + (Q'+cs\,Q)E` (from `E'=cs\,E-sc`, `sc:=\sqrt{2c/
\pi}`), and `solve_b_step`, which solves the `b`-ODE within the family via
the descending-recursion/`\kappa`-pinning algorithm (worked through in
full generality, including the low-degree edge cases, in the module
docstring and code comments). A numerically-safe `erfcx(z)` (direct
formula for `z\le6`, asymptotic series beyond) is implemented since
`mpmath` has no built-in `erfcx` and `z=s\sqrt{c/2}` reaches several
hundred in this front's grid.

### 3.2 Validation against published anchors (`k02_validate.py`/`.log`)

At `c=1000`, `K=220`, `dps=60`, against the SAME anchors quoted verbatim
(as plain text) in both required-reading documents:

| quantity | this front's value | published anchor | rel. diff | verdict |
|---|---|---|---|---|
| `a2(0)` | `520316.63648803` | `520316.636488` | `5.8e-14` | PASS |
| `a3(0)` | `-180730907.628508` | `-180730907.6285` | `4.5e-14` | PASS |
| `a4(0)` | `47146963944.1379` | `47146963944.14` | `4.5e-14` | PASS |
| `b2(0)` | `-20816.6364880301` | `-20816.636488` | `1.4e-12` | PASS |
| `b1(0)` | `39.6332729760601` | `sqrt(pi*1000/2)` | `0` (exact) | PASS |
| `Phi(0,0.002)` | `0.158500145747308` | `0.15850015` | `2.7e-8` | PASS |
| `Phi(0,0.05)` [plateau] | `0.0377615983402126` | `0.0377615983402126...` | `2.2e-21` | PASS |

**7/7 PASS.** These are exactly the same anchors ancestor fronts
validated their own (unopened) implementations against — matching them
independently confirms this front's general-`s` machinery is correct at
`s=0` before trusting it at `s\ne0`.

**General-`s` cross-check.** The required reading (`plateau_resummation_
attempt/ATTEMPT.md` §6) publishes `F(s)` values at `c\in\{1000,2560\}`,
`x=s\sqrt c\in\{0,0.5,1,2,3\}` (10 numbers). This front's independent
pipeline reproduces the `c=1000` row to `\sim12` digits (`5.6\times10^{-12}`
to `8.2\times10^{-12}` relative, limited only by the `K=260,\text{dps}=50`
sizing used for that spot check, not a discrepancy) and, after correcting
the `(K,\text{dps})` sizing for the larger `c=2560` (§3.4 below, where a
first pass under-sized `K` and was CAUGHT before being trusted), matches
the `c=2560` row to the same precision — see the `resid3` cross-check
below for the more demanding, decisive version of this test.

### 3.3 `psi3(x)` and `psi4(x)` at general `x` (fresh derivation / reuse)

`k03_profiles.py`. `\psi_1(x)=R(x)`, `\psi_2(x)=2xR(x)-2` are given in
closed form directly in the required reading. `\psi_3(x)` at general `x`
is **not** — only its ODE (`\psi_3'=x\psi_3+7R'`, bounded branch) and its
value at `x=0` are stated. This front derives the general-`x` closed
(integral) form by the SAME bounded-branch variation-of-parameters method
the record itself uses for `R` (whose own representation `R(x)=e^{x^2/2}
\int_x^\infty e^{-t^2/2}\,dt` is exactly this method applied to `R'=xR-1`):
for `y'-xy=f(x)`, the solution bounded as `x\to\infty` is `y(x) =
-e^{x^2/2}\int_x^\infty e^{-t^2/2}f(t)\,dt`; with `f=7R'`,

```
psi3(x) = -e^{x^2/2} * int_x^infty e^{-t^2/2} * 7*R'(t) dt
```

(the module's first draft omitted the leading minus sign — caught
immediately by its own `x=0` validation, self-caught issue S2, §7, before
being used anywhere.) Verified: `psi3(0) = 4.3865994806042508792...`
against the record's closed form `(7/2)\sqrt{\pi/2} =
4.3865994806042508792...` — agreement to `30` digits (`4.5\times10^{-31}`
relative). `\psi_4(x) := (17/3)R'''(x)` uses the record's OWN stated
closed form (§4.4b of the required reading) directly, via the elementary
derivative recursion `R''=R+xR'`, `R'''=2R'+xR''` (re-derived here by
direct differentiation of `R'=xR-1`, not quoted from anywhere); verified
`\psi_4(0) = -34/3` exactly, matching the record.

### 3.4 Decisive cross-check: reproducing the record's own `resid3` values

The required reading's §6 reports, as raw measured numbers (not a
closed-form prediction), `resid3 := (F-eps\,R-eps^2(2xR-2))/eps^3` at
`x=0`: `4.058` (`c=1000`), `4.175` (`c=2560`). Using this front's own,
independently-built `F(0;c)` (§3.1/3.2) and its own `\psi_1,\psi_2` (§3.3),
this front computes:

```
c=1000: resid3 = 4.0580043   (record: 4.058)
c=2560: resid3 = 4.1746489   (record: 4.175)
```

**Exact match**, to every digit the record itself published — a strong,
decisive, independent confirmation that this front's fresh general-`s`
pipeline reproduces the ancestor front's own (unopened) numbers correctly,
via a completely different code path (this front's own polynomial-family
solve, `(K,\text{dps})` sizing, and `\psi_3` integral representation),
before this front's own NEW results (§4-§5) are trusted.

---

## 4. Main experiment: the `(x,c)` uniformity grid

### 4.1 Grid and diagnostics (`k04_uniformity_grid.py`/`.log`/`.json`)

Grid: `c\in\{200,500,1000,2000,4000,8000\}` (each with its own `(K,\text{
dps})`, sized by direct convergence probing — two-`t_0` cross-check
(`t_0=45/c` vs `60/c`) required to agree to `\ge15` digits at `x=8` BEFORE
being trusted, disclosed in the module docstring and verified per-`c` in
the log), `x\in\{0,0.5,1,2,4,6,8\}` (`s=x/\sqrt c` up to `0.71` at the
smallest `c` tested — within the process's presumed physical domain
`s\in[0,1]`). For each `(x,c)`:

```
rho1(x,c) := [F(x;c) - eps*psi1(x)] / eps^2          (should -> psi2(x))
rho2(x,c) := [F(x;c) - eps*psi1(x) - eps^2*psi2(x)] / eps^3   (should -> psi3(x))
gap1 := rho1 - psi2(x),   gap2 := rho2 - psi3(x)
```

Every one of the `42` grid points passes its own approach-rate
convergence check to `\ge12` stable digits (`\max` relative disagreement
`1.3\times10^{-12}` at `c=200`, `<10^{-19}` at larger `c` — logged
per-`c` in `k04_uniformity_grid.log`) before being used.

### 4.2 Uniformity-in-`x` diagnostic (`k06_uniformity_analysis.py`/`.log`)

Define `\text{ratio}_1(x,c):=\text{gap}_1/(eps\cdot\psi_3(x))` and
`\text{ratio}_2(x,c):=\text{gap}_2/(eps\cdot\psi_4(x))` — both should
`\to1` as `eps\to0` at each fixed `x` if the respective order transition
is valid there. **The uniformity question is whether this convergence
degrades as `x` grows.** A per-`x` least-squares linear extrapolation of
each ratio to `eps=0` (over all 6 `c`-values) gives, for order 1:

| `x` | extrapolated ratio (`eps\to0`) | `|1-\text{extrap}|` |
|---|---|---|
| 0 | 0.99303586 | 0.006964 |
| 0.5 | 0.99451027 | 0.005490 |
| 1 | 0.99564812 | 0.004352 |
| 2 | 0.99719108 | 0.002809 |
| 4 | 0.99866749 | 0.001333 |
| 6 | 0.99926072 | 0.0007393 |
| 8 | 0.99953952 | 0.0004605 |

and, for order 2 (using `\psi_4`):

| `x` | extrapolated ratio (`eps\to0`) | `|1-\text{extrap}|` |
|---|---|---|
| 0 | 0.99166188 | 0.008338 |
| 0.5 | 0.99323185 | 0.006768 |
| 1 | 0.99448841 | 0.005512 |
| 2 | 0.99627906 | 0.003721 |
| 4 | 0.99813065 | 0.001869 |
| 6 | 0.99893160 | 0.001068 |
| 8 | 0.99932366 | 0.0006763 |

**Both columns are verified explicitly monotonically NON-INCREASING in
`x`** (checked programmatically, `k06_uniformity_analysis.log`, last
section: `True` at both orders) — i.e. the discrepancy from the
`H1`-predicted value `1` **shrinks, not grows**, as `x` increases over the
whole tested range. This is the qualitative opposite of what a genuine
failure of uniform validity (an error that grows away from the point
`x=0` actually used to extract `Pi(c)`) would look like, and is
substantially more information than any ancestor front's pointwise,
few-point checks provided.

### 4.3 Reading this honestly

This is strong, clean, **numerical, non-perturbative-content-blind**
evidence FOR `H1` (or more precisely, for `(U1)`+`(U2)` jointly) over the
tested domain, at orders 1 and 2. It is not, and cannot be, a proof: (i)
it tests only two successive order-transitions, not "all orders
uniformly" as `H1` literally claims; (ii) it cannot detect
exponentially-small-in-`eps` (trans-series) corrections that would be
invisible to any finite-order polynomial-in-`eps` fit — exactly the
concern the `plateau_resummation_attempt` referee raised about
`\Phi(0,\cdot)` being order-2 entire (§4.5 of that document, cited
faithfully in `mclust_plateau_abstract_real_gap_attempt` §B.5) and which
this front does not address; (iii) the `x`-range tested (`0` to `8`, `s`
up to `0.71`) is wide relative to any ancestor check but still finite —
see §5 for an explicit attempt to push further.

---

## 5. Stress test: pushing `x` further, including past the physical
boundary `s=1`

### 5.1 First pass and a self-caught numerical pitfall (`k05_stress_x.py`/`.log`)

Extending the grid to `x\in\{10,12,15,20\}` (and, at `c=200`, further to
`x=25`) with the SAME `(K,\text{dps})` sizing validated for `x\le8`
produces, at `c=1000,4000`, `x` up to `20`, results fully consistent with
§4's pattern (ratio continuing smoothly toward `1`, no degradation — see
`k05_stress_x.log`). But at `c=200` specifically, pushing to `x=14`
(`s=0.99`, at the edge of `s=1`) and beyond, the two-`t_0` convergence
diagnostic **itself fails** (relative disagreement `0.86` at `x=14`,
`\approx1.0` — i.e. zero stable digits — at `x=16,20,25`): caught
immediately by this front's own diagnostic, BEFORE any of these numbers
were used in a ratio table. This is the SAME "order-2-entire cancellation
cost wall" phenomenon the record documents for small `c` (`plateau_
resummation_attempt/ATTEMPT.md` §2.2), here appearing as `x` (equivalently
`s`) grows large at fixed, smaller `c` — a genuinely new instance of the
same known numerical difficulty, not previously observed in the `x`
direction because no ancestor front tested `x` this large.

### 5.2 Corrected rerun (`k07_stress_x_corrected.py`/`.log`)

Rerunning `c=200`, `x\in\{14,16,20\}` at `K=800,\text{dps}=90` (up from
`K=400,\text{dps}=60`) restores full convergence (`\le3.7\times10^{-20}`
relative at `x=14,16`; `1.2\times10^{-17}` at `x=20`):

| `x` | `s=x/\sqrt c` | `F(x;200)` | approach reldiff | ratio1 |
|---|---|---|---|---|
| 14 | 0.9899 | 0.0049759743912426 | `3.2\times10^{-20}` | 0.97665 |
| 16 | 1.1310 | 0.0043643173460695 | `3.7\times10^{-20}` | 0.97941 |
| 20 | 1.4142 | 0.0035022454736161 | `1.2\times10^{-17}` | 0.98335 |

**Reading.** Even at `x=20`, `s=1.41` — well beyond the process's
presumed physical domain `s\in[0,1]` (the abstract `(x,y)` recursion
continues to be perfectly well-defined mathematically there; only its
original combinatorial meaning as "fraction of pool consumed" would cease
to apply) — the ratio continues the SAME smooth trend toward `1` as the
main grid, `0.983`, consistent with (indeed slightly BETTER than) the
`x=8` value (`0.981` at the corresponding `c=200` row of §4.1's grid,
recoverable from `k04_uniformity_grid_results.json`). **The apparent
"blow-up" in the uncorrected `k05_stress_x.log` raw output (ratio
`\sim1.4\times10^4` at `x=20`, `\sim7\times10^{12}` at `x=25`) is
entirely a numerical non-convergence artifact of undersized `(K,\text{
dps})`, not a finding about `H1` — disclosed explicitly here, per this
lineage's convention, rather than silently discarded.** No counterexample
or genuine failure mode of uniform validity was found anywhere in the
stress-tested region.

---

## 6. Honest final verdict

**`H1` is NOT closed.** What this front contributes:

1. A genuine theoretical reduction (§2): the exact renewal identity
   `(E2)` already in the record, combined with a new, fully rigorous
   Watson-concentration lemma proved here (§2.1, elementary real analysis,
   no gaps), reduces `H1` to two smaller, independently-stated,
   more-checkable conditions `(U1)` (locally-uniform `g\to\infty`
   convergence of `W`) and `(U2)` (a uniform-in-`x` `eps`-expansion of
   `W_\infty`) — narrowing, not closing, the black box. Neither `(U1)`
   nor `(U2)` is proved here.
2. A second, independent exact structural fact (§2.3): the plateau
   profile `F(x)` satisfies an EXACT (conditional on stated integrability
   hypotheses) first-order linear ODE `F'-xF=-C(x)`, new to the record,
   consistent with the known leading-order equation. This isolates the
   remaining heuristic content to expanding `C(x)`, one layer further
   than the record's own framing of `H1`.
3. Extensive, carefully cross-validated (§3.4: exact reproduction of the
   record's own `resid3` numbers via an independent code path),
   high-precision (`dps` 50–110) numerical evidence, at TWO successive
   asymptotic orders, across a grid substantially wider than any ancestor
   front's own spot checks (`6\times` more `c`-values, `\sim3\times`
   wider `x`-range), plus an explicit stress test into the unphysical
   `s>1` region (with a self-caught, disclosed, and then corrected
   numerical convergence failure) — **shows no sign whatsoever of
   non-uniform behavior**; if anything, the convergence to the
   `H1`-predicted limit `1` gets systematically TIGHTER as `x` grows,
   monotonically, at both orders tested.
4. This numerical evidence is real, checkable support for `H1` holding
   (at least at orders 1–2, over the tested domain), but it is
   **evidence, not proof** — it is structurally blind to non-perturbative
   (trans-series) corrections, which is precisely the referee-named
   concern about `\Phi(0,\cdot)`'s order-2-entire growth class that
   neither this front nor its immediate predecessor addresses.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_\infty(c)`, and the four-term asymptotic law
of record are all untouched and unaffected by anything in this document.
`H2` is untouched, exactly as the mandate scoped this front.

---

## 7. Self-caught issues (disclosed, per this lineage's convention)

**S1 (this front's own catch, theoretical).** An early internal draft of
the Watson-concentration argument (§2.1) concluded, incorrectly, that
`\lim_{y\to\infty}\Phi(x_0,y) = W_\infty(x_0)` directly — treating the
exponential kernel as if it collapsed to a point mass at `v=0` even at
FIXED `eps`. This is wrong: the kernel only concentrates at `v=0` in a
SECOND, separate limit `eps\to0`; at fixed `eps`, `y\to\infty` alone gives
the full convolution `(STAR)`, not the naive pointwise value. Caught
during the derivation itself (re-checking the bound on the "tail" piece
of the split integral, which does not vanish as `y\to\infty` at fixed
`eps`, only as `\text{delta}\to0`, i.e. `G(\text{delta})/eps\to\infty`),
before this incorrect version was written into any result — the correct
`(STAR)` is what appears in §2.1.

**S2 (this front's own catch, computational).** The first draft of
`psi3(x)`'s bounded-branch variation-of-parameters formula
(`k03_profiles.py`) omitted the leading minus sign in `y(x) =
-e^{x^2/2}\int_x^\infty e^{-t^2/2}f(t)\,dt` (a standard integrating-factor
derivation, re-worked by hand for this specific ODE `\psi_3'=x\psi_3+7R'`).
This produced `\psi_3(0) = -4.3865994806...`, matching the record's
`4.3865994806...` in MAGNITUDE but with the wrong sign — caught
immediately by the very next validation step (comparing against the
record's own closed form `(7/2)\sqrt{\pi/2}`, §3.3), before `\psi_3` was
used in any downstream computation. Fixed by adding the missing sign;
re-verified to `30` digits.

**S3 (this front's own catch, computational, the one with the largest
consequence if it had gone unnoticed).** The initial stress-test pass
(§5.1, `k05_stress_x.py`) used the SAME `(K=400,\text{dps}=60)` sizing
validated for `x\le8` all the way out to `x=25` at `c=200`. This produced
a dramatic, superficially alarming "uniformity ratio blow-up"
(`\sim1.4\times10^4` at `x=20`) that, read uncritically, would have looked
like genuine evidence AGAINST `H1`. This front's own two-`t_0`
convergence diagnostic (built into every grid computation from the start,
§4.1) flagged these specific points as non-convergent (`\ge0.86` relative
disagreement — effectively random noise, not stable digits) BEFORE the
ratio was reported as a finding; §5.2 documents the corrected rerun, which
shows the "blow-up" was entirely a numerical artifact. Disclosed here in
full, including the raw (wrong) numbers in `k05_stress_x.log`, exactly per
this lineage's "disclose even a caught-before-being-trusted issue"
convention — this is the clearest instance in this front's own work of
exactly the failure mode (numerical non-convergence masquerading as a
mathematical finding) that the archive's adversarial-review discipline
exists to catch, caught here by the front's own built-in diagnostics
without needing a referee.

---

## 8. What remains open

1. **`(U1)` and `(U2)` (§2.2) are not proved.** Establishing either from
   the exact PDE system would need genuine PDE-theoretic tools (e.g. a
   maximum-principle or energy-estimate argument bounding the RATE at
   which `\Psi(x,g)\to\Psi_\infty(x)` uniformly in `x` over an unbounded
   domain) — substantially beyond this front's scope, exactly as the
   mandate's own risk assessment anticipated. This is the single largest
   remaining gap toward a full closure of `H1`.
2. **`(ODE\text{-}F)` (§2.3) was not independently numerically verified**
   beyond a leading-order consistency check; a direct numerical test
   (tabulating `\Phi(x,y)` over a `y`-grid at fixed `x`, computing `C(x)`
   by quadrature, and checking `F'(x)-xF(x)=-C(x)` against a
   finite-difference `F'(x)` from this front's own general-`s` machinery)
   is a concrete, well-defined, NOT-yet-executed next step.
3. **Non-perturbative (trans-series) content is entirely untested.** The
   numerical evidence of §4-§5, however clean, is blind by construction
   to corrections of size `e^{-A/eps}` for any `A>0` — exactly the kind of
   content the referee's "order-2-entire growth class" concern (inherited
   unaddressed from `plateau_resummation_attempt`) would predict might be
   present. No attempt was made here to search for such content (e.g. via
   a resurgence/Borel-plane analysis of the exact `(x,y)` system, distinct
   from the already-disclosed-failed naive Borel(-1) attempt on the
   `t_0`-series in the record) — a large, separate undertaking.
4. **The uniformity grid's `x`-range (`0` to `20` in the stress test, `0`
   to `8` in the main grid) and `c`-range (`200` to `8000`) are still
   finite.** No claim is made that uniformity holds for ALL `x\ge0` or all
   `c` — only that no failure was found anywhere searched, including
   deliberately past the presumed physical domain `s\le1`.
5. **`H2` is untouched**, exactly as the mandate scoped this front to
   `H1` alone.
6. **A genuinely different, second numerical test** — directly bounding
   the FULL remainder (not just two successive order-transitions) via a
   high-order (`N\ge5`) truncation compared against `\Phi(x,t_0)` at
   MODERATE `t_0` (not just the `t_0\to\infty` plateau), which would probe
   uniformity in `y` as well as in `x` simultaneously — was not attempted;
   named as a further concrete next step.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_\infty(c)` are all untouched and unaffected.

---

## 9. Files

| file | role |
|---|---|
| `k01_family_series.py` | fresh general-`s` `(P,Q)`-family recursion implementation (§3.1) |
| `k02_validate.py`/`.log` | validation against 7 published anchors at `c=1000` (§3.2) |
| `k03_profiles.py` | `psi1,psi2` (record's closed forms), `psi3` (fresh integral derivation), `psi4` (record's closed form via fresh `R`-derivative recursion) (§3.3) |
| `k04_uniformity_grid.py`/`.log`, `k04_uniformity_grid_results.json` | main `(x,c)` grid: `F(x;c)`, `rho1,rho2`, `gap1,gap2` at 42 grid points (§4.1) |
| `k05_stress_x.py`/`.log` | stress test extending `x` to 20-25; contains the self-caught S3 non-convergence artifact, disclosed raw (§5.1) |
| `k06_uniformity_analysis.py`/`.log` | uniformity-in-`x` diagnostic: per-`x` ratio tables and `eps\to0` linear extrapolations, both orders (§4.2) |
| `k07_stress_x_corrected.py`/`.log` | corrected, converged rerun of the `c=200,x\in\{14,16,20\}` stress points (§5.2) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/
mclust_h1_validity_attempt/` subdirectory was written to — every ancestor
`ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/
`DISCOVERY_LAB_STATE.md` further up the tree were read-only references
(§0), never modified. No `adversarial/` subdirectory created; no referee
dispatched by this front itself, per the mandate.
