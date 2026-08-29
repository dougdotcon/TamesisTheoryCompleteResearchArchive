# ATTEMPT — a relative-step oscillation bound on Φ, and a sharper map of
# what the classical Tauberian theorem still needs (`TAUBERIAN-OSCILLATION-
# BOUND-ATTEMPT`)

**Wave 26, front (c), `DISC-DEC-123`.** Seventh consecutive wave (waves
20–26) attacking the same `H1`/`(U1)`/`(U2)` gap in this exact sub-lineage.
Target, per `DISC-DEC-122`'s addendum: the two named ingredients needed to
upgrade the already-proved (unconditional, given `(B)`,`(C)`) self-averaging
identity `Φ_y(x) − A(y)/(x+y) → 0` into an actual proof of `(U1)` via the
classical continuous Tauberian theorem for Cesàro-`(C,1)` summability —
(i) a relative-step oscillation bound on `Φ` itself (not `Ψ`, for which
`(⋆⋆)` already exists), and (ii) formal verification that the classical
theorem's hypotheses transfer to this two-variable PDE setting.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`), the `b=1` floor's abstract `(s,g)` recursive process — pure
combinatorial/asymptotic mathematics about a random-permutation-with-reroutes
ensemble. It is a standalone object, entirely independent of the archive's
separate Tree A (`u1/2` / "Lema Aberto") line in `THEOREM.md`. Nothing here
is, or is adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.** Per `PROOF_DEPENDENCY_MAP.md` Sec 3's explicit rule, no
result from Tree A is cited anywhere below, even in hedged language, as
evidence for anything claimed here.

Reserved seed range for this front: `20260935000-20260935999`.
Grep-confirmed BEFORE any use (`grep -rn "20260935" 05_DISCOVERY_LAB/`) to
appear only in `DECISION_LEDGER.yaml`'s own `DISC-DEC-123` reservation line
(re-confirmed again at the end of this front, Sec 9). **In the end no
randomness was needed anywhere in this front** — every computation below is
exact symbolic algebra (`sympy`) or deterministic arbitrary-precision
adaptive quadrature (`mpmath`, fixed evaluation strategy, de-stiffened
substitutions, no sampling), exactly as every direct ancestor front in this
sub-lineage reports for itself. The reserved range remains entirely unused.

---

## VERDICT UP FRONT

**Tier: honest non-closure of `(U1)`/`(U2)`, with a genuine candidate
derivation of ingredient (i) (conditional on two named, not-fully-closed
technical hypotheses, one of them newly numerically tested in a regime no
ancestor front tested), route (a) of the mandate closed off with a precise
dead-end diagnosis, and — the sharpest new contribution of this front — an
explicit demonstration that the classical Tauberian theorem needs a THIRD
hypothesis beyond the two DISC-DEC-122/123 named: Cesàro-`(C,1)` convergence
of `A(y)/(x+y)` itself, which is established nowhere in this lineage's
record and is NOT supplied by the oscillation bound, however sharp.**

1. **Route (a) — transferring `(⋆⋆)` from `Ψ` to `Φ` via `(E2)`/`(KEY)` —
   is a genuine dead end, precisely diagnosed** (Sec 2): both the direct
   `(KEY)` route and an algebraically-equivalent `(E1)`-substituted route
   (a new identity, `W = ε·[M_y·Ψ + I]`, derived and verified here) hit the
   SAME wall — an individually-UNBOUNDED operator (`M_y ~ −z`) multiplying
   the oscillation being bounded, with no companion term available to cancel
   against (unlike the `Φ`-Volterra kernel `K(y,t)=M_y K_A^raw+K_B`, where
   `h1_translation_structure_attempt` found exactly such a cancellation).
   This sharpens, into a specific mechanism, `h1_energy_estimate_attempt`
   Sec 8.4's general "derivative loss" diagnosis for this specific route.

2. **Route (b) — a relative-step oscillation bound on `Φ` itself, derived
   directly from the closed-form kernel asymptotic applied to the exact
   Volterra equation** (Sec 3) — **succeeds, conditionally**:
   ```
   |Φ_{y2}(x) − Φ_{y1}(x)|  ≤  C1(x,ε)·δ + C2(x,ε)/y1        (OSC-PHI)
   ```
   for `y2−y1 = δ·y1` (`0<δ<1`), `y1` large — EXACTLY the relative-step
   "slowly oscillating" form the classical Tauberian theorem needs. Derived
   by splitting `Φ_{y2}(x)−Φ_{y1}(x)` into three exact pieces (`T0`: the
   forcing-term difference, trivial; `T1`: the kernel difference integrated
   over the FULL history `t∈[0,y1]`; `T2`: the new-kernel contribution over
   `t∈[y1,y2]`) and bounding each using the closed-form kernel asymptotic
   (`h1_translation_structure_attempt`, `DISC-DEC-122`) rather than the
   cruder constant operator-norm bound (`DISC-DEC-113/115`) — the crude
   bound alone gives `O(δ·y1)`, useless; the closed form gives `O(δ)`.

3. **This derivation needs two hypotheses beyond the standing `(B)`**,
   both explicitly flagged, one newly and successfully numerically tested
   in a regime NO ancestor front tested (Sec 4): `(C')`, a Lipschitz-type
   regularity bound on `Φ_t(·)` UNIFORM in `t` (strictly stronger than the
   predecessor's single-fixed-`f` `(C)`); and `(U)`, uniformity of the
   closed-form kernel's `O(1/z²)` remainder across the FULL range
   `h∈[0,y]`, INCLUDING `h/y→1` (i.e. `t→0`, the "distant past" of the
   Volterra history) — the predecessor only tested `h=y/2` (a single fixed
   ratio). This front tests the FULL ratio sweep (`h/y` from `0.0002` to
   `0.99`) at multiple `z`, including a combined sweep that ALSO crosses the
   `h~ε` transition in the same run, at both `x=0` and `x=3` — **`(U)` holds
   in every case tested, `z²·`(error) staying bounded and smoothly varying,
   with NO blowup detected anywhere, including the previously-untested
   `h/y→1` regime this front's own derivation specifically needs.**

4. **Ingredient (ii) — hypotheses transfer — is mostly resolved
   positively, but reveals a genuinely new, THIRD requirement** (Sec 5–6):
   (ii-a) the classical theorem's proof, once `x` is fixed, applies
   VERBATIM to `g(y):=Φ_y(x)` as an abstract bounded real function of `y`
   — no PDE-specific obstruction here. (ii-b) `(OSC-PHI)`'s constants are
   AUTOMATICALLY non-increasing in `x` for `x≥0` (an exact consequence of
   the derivation's own algebra), given `(C')` and `(U)` hold uniformly in
   `x` — spot-checked numerically at `x=3` in addition to `x=0`, consistent.
   **(ii-c), the sharp new finding: the classical theorem ALSO requires
   Cesàro-`(C,1)` convergence of `A(y)/(x+y)` to SOME limit — a hypothesis
   LOGICALLY SEPARATE from the oscillation bound, established nowhere in
   this lineage's record, and NOT implied by `(B)`+`(C')`+`(U)`+`(OSC-PHI)`
   together.** A fully worked, elementary counter-example (Sec 6) —
   `g(t):=sin(log(1+t))` — is bounded, satisfies the EXACT relative-step
   oscillation condition `(OSC-PHI)` needs (verified symbolically and
   numerically), yet BOTH `g(t)` itself and its own Cesàro mean fail to
   converge, oscillating forever with the same non-vanishing amplitude
   (exact closed form derived and confirmed by direct differentiation).
   This makes concrete, not merely assert, that `(H-osc)` does not
   substitute for `(H-ces)` — DISC-DEC-122/123's "two ingredients" framing
   implicitly bundled a third, independent requirement into "hypotheses
   transfer" that this front makes explicit for the first time in this
   sub-lineage.

5. **`(U1)`/`(U2)` do NOT close.** Even granting `(OSC-PHI)` in full
   (conditional on `(C')` and `(U)`, both flagged, `(U)` now well-supported
   numerically in the needed regime), the classical Tauberian theorem
   cannot be applied to conclude `Φ_y(x)→L(x)` without independently
   establishing Cesàro convergence of `A(y)/(x+y)` — a requirement this
   front identifies precisely but does not attempt to close (naming, not
   solving, a candidate route in Sec 7). **No claim of closure is made
   anywhere in this document.**

**`H1` remains ABERTO/OPEN, exactly as before this front.** `φ_REDB`,
`Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of record are
all untouched and unaffected by anything in this document. `H2` is untouched
(out of scope). No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was opened for writing. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself. No `git` command run.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, in prose, before any derivation or code: `DISC-DEC-123`'s full
entry in `DECISION_LEDGER.yaml` (this front's own mandate and authorization,
including the explicit checkpoint clause); `PROOF_DEPENDENCY_MAP.md` Sec 2
(Tree B), the `PLATRESUM` node's complete addenda history through the final
addendum (dated 2026-08-29, `DISC-DEC-122`, this front's immediate mandate
source), working backward through `DISC-DEC-115`, `DISC-DEC-113`,
`DISC-DEC-096/100`, `DISC-DEC-088/091`; and Sec 3 ("Regra de uso deste
mapa"), the safety rule against conflating this Tree B line with the
separate Tree A (`U_α`) line — followed strictly throughout, confirmed by
inspection that no result or hedge from Tree A appears anywhere below.

Also read in full: `h1_translation_structure_attempt/ATTEMPT.md` (immediate
predecessor, wave 25 front c) — establishing the closed-form kernel
asymptotic `K(y,t)f(x)=[f(x)-e^{-h/ε}f(x+h)]/(x+y)+O(1/(x+y)²)`, the
self-averaging/Cesàro identity, and Sec 6.3's precise naming of the
Tauberian gap — this front's direct starting point; the same document's
`adversarial/REFEREE_REPORT.md` in full, INCLUDING its Finding 1 (the
corrected logical framing — `(U1)` is equivalent to Cesàro-mean convergence
of `Φ_t(x)`, NOT literally "equivalent to" the self-averaging identity
itself — this corrected framing is used throughout, not the predecessor's
original imprecise phrasing) and Finding 2 (a documentation-precision note
on Bug-1's catch mechanism, not otherwise relevant here); and
`mclust_h1_validity_attempt/h1_energy_estimate_attempt/ATTEMPT.md` in full
— establishing the oscillation bound on `Ψ` (not `Φ`), `(⋆⋆)`, the `(E1)`,
`(KEY)`, `(E2)` system, and the "derivative loss" diagnosis (Sec 8.4) this
front's Sec 2 sharpens for the specific route (a) it examines.

**No `.py` file from any ancestor front, or from any referee, was opened,
read, or imported at any point.** Every script in this directory (`s01`–
`s04`) was written fresh from the mathematical content of the prose cited
above, exactly as every direct ancestor front in this sub-lineage reports
for itself. No `(P,Q)`-family series solver was built for this front — see
Sec 1.2 for why, and what this scopes out.

**The exact inputs this front works from** (restated for
self-containedness, cited not re-derived except where marked NEW below):

```
Scaled variables: x = s*sqrt(c), y = g*sqrt(c), eps = 1/sqrt(c)

Closed Volterra-in-y system (cited, record fact):
  Phi_y = g_y + int_0^y K(y,t)[Phi_t] dt                       (VOLTERRA-Phi)
    g_y(x) := e^{-y/eps},   Phi_y := Phi(.,y) in X := C_b([0,infinity))
    K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
      K_B(h)       := int_0^h e^{-v/eps} S_v dv,   (S_v f)(x):=f(x+v)
      K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
      (T_w f)(x)   := int_0^infinity e^{-u^2/2-u(x+w)} f(x+u) du
      M_y          := multiplication-by-[(1-eps(x+y))/eps]

Exact system for Psi (cited, DISC-DEC-096/100):
  Psi_x = (x+y) Psi - I,   I := int_0^y Phi(x,y') dy'                (E1)
  W = Psi - eps * dPsi/dx                                            (KEY)
  Phi(x,y) = e^{-y/eps} + (1/eps) int_0^y e^{-v/eps} W(x+v,y-v) dv    (E2)

R(x) := sqrt(pi/2)*erfcx(x/sqrt2) = psi1(x),  R'=xR-1,  R(0)=sqrt(pi/2),
  R strictly decreasing on [0,infinity),  R(z)<=1/z for z>0
Standing hypothesis (B): Phi, Psi bounded (used throughout this lineage).

THE CORRECTION (DISC-DEC-113): ||K(y,t)|| <= sqrt(pi/2)+eps UNIFORMLY,
  operator-norm level (sup over ALL bounded f, not pointwise-in-f).

THE CLOSED-FORM ASYMPTOTIC (DISC-DEC-122, cited, pointwise-in-f, NOT an
operator-norm claim -- conditional on (B) plus an auxiliary Lipschitz-type
regularity hypothesis (C) on f):
  K(y,t) f(x) = [f(x) - e^{-h/eps} f(x+h)] / z + O(1/z^2),  h:=y-t, z:=x+y
  confirmed numerically to 3.2e-8 worst-case rel. err (6 cases), and to
  remain accurate with h growing PROPORTIONALLY with y, tested to h=y/2,
  y=3000 (2.8e-7).

The self-averaging identity (DISC-DEC-122, PROVED unconditionally given
(B),(C), cited, corrected framing per the referee's Finding 1):
  Phi_y(x) - A(y)/(x+y) -> 0,   A(y):=int_0^y Phi_t(x) dt
  <=> [(U1) is equivalent to]: A(y)/(x+y) itself converges (Cesaro-(C,1)).

The oscillation bound on Psi (h1_energy_estimate_attempt Sec 5.1, cited, "(star-star)"):
  sup_{x>=0} |Psi(x,y2)-Psi(x,y1)|  <=  (y2-y1)*K*R(y1)  <=  (y2-y1)*K/y1
  (K := 2*max(|Phi|,|Psi|), an empirically-measured, not independently
  proved, constant -- consistent with (B) being standing throughout).

The classical Tauberian theorem (cited external tool, NOT re-derived --
Hardy, Divergent Series; Korevaar, Tauberian Theory), quoted per the
predecessor's own Sec 6.3: if g:[0,infinity)->R is bounded, (1/y)int_0^y
g(t)dt -> L, AND g is slowly oscillating in the relative-step sense (for
every epsilon>0 there exist delta>0,Y such that y>=Y, 0<=s-y<=delta*y imply
|g(s)-g(y)|<epsilon), then g(y)->L.
```

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`adversarial/` were read-only references throughout; nothing
outside this front's own new subdirectory was written to.

---

## 1. Overview

### 1.1 The mandate's structure and this front's approach

Two ingredients named by `DISC-DEC-122`, restated by `DISC-DEC-123`:

- **(i) a relative-step oscillation bound on `Φ`.** Three candidate routes
  were named: (a) transfer `(⋆⋆)` from `Ψ` via `(E2)`/`(KEY)`; (b) derive
  directly from the closed-form kernel + the exact Volterra equation; (c)
  any other legitimate route. This front attempts (a) first (Sec 2, quick,
  conclusively a dead end) and then (b) in full (Sec 3–4, the main content).
- **(ii) formal verification the classical theorem's hypotheses transfer**
  to the two-variable PDE setting. Attempted carefully (Sec 5), and this is
  where the front's sharpest new finding emerges: a THIRD hypothesis, not
  named by the mandate, is also required (Sec 6).

If both (i) and (ii) were established, the mandate directs applying the
theorem and checking whether `(U1)` actually closes. **It does not** — Sec
6 identifies precisely why, and Sec 7 states this without hedging.

### 1.2 Why no fresh `(P,Q)`-family series solver was built

Every numerical check in this front tests either (I) an ELEMENTARY
inequality/identity that holds for ANY bounded function satisfying the
stated hypotheses (the `T0`/`T1`/`T2` sub-bounds of Sec 3, and the Sec 6
counter-example — neither depends on `Φ` being the SPECIFIC solution of
this system), or (II) the closed-form kernel `K(y,t)` itself, evaluated
directly from its own raw definitions (Sec 4) — a self-contained object not
requiring the `(P,Q)`-family recursion at all. Building an independent
`(c,s,g)`-indexed series solver, as `h1_energy_estimate_attempt` and its
siblings did, would let this front test the FINAL bound `(OSC-PHI)` against
the actual physical `Φ`, at real added value only if it could be built
without repeating the well-documented pitfalls (index bugs, precision-vs-
truncation cancellation needing `dps~250-300`) every such solver in this
lineage has hit — a substantial undertaking oriented at a DIFFERENT question
(numerically confirming a bound already derivable and testable by more
targeted, lower-risk means, Sec 3–4) than this front's actual new content
(the derivation itself, and the Sec 6 gap it exposes). This scope choice is
disclosed explicitly, not hidden — see Sec 7 item 5 for what it leaves
untested.

---

## 2. Route (a) — transferring `(⋆⋆)` from `Ψ` to `Φ` via `(E2)`/`(KEY)`:
a precise dead end

Full derivation, symbolic and self-checked: `s04_route_a_key_transfer_
symbolic.py`/`.log`.

### 2.1 A new algebraic simplification, verified

Substituting `(E1)`'s expression for `Ψ_x` directly into `(KEY)`:

```
W = Psi - eps*Psi_x = Psi - eps*[(x+y)Psi - I]
```

**New identity (to this front — both inputs are already record facts, this
is a re-packaging, not an independently new fact), verified exactly by
`sympy`**:

```
W(x,y) = eps * [ M_y * Psi(x,y) + I(x,y) ]
```

### 2.2 Why the natural bound fails: an unbounded operator with no
cancellation partner

Writing `Δ_W(x):=W(x,y2)-W(x,y1)` via the identity above, and splitting
`M_{y2}Ψ(x,y2)-M_{y1}Ψ(x,y1) = M_{y2}·Δ_Ψ(x) + (M_{y2}-M_{y1})·Ψ(x,y1)`
(verified exactly, `sympy`): the second piece is fine (`M_{y2}-M_{y1}
=-(y2-y1)`, exactly `O(Δ)`). **The first piece is the wall**: `M_{y2} =
1/ε-z2 → -∞` as `y2→∞` — an UNBOUNDED coefficient multiplying `Δ_Ψ(x)`,
which `(⋆⋆)` only bounds by `O(Δ/y1)`. The product is `O(Δ·y2/y1)
=O(δ·y2)` for `Δ=δy1` — **growing, not vanishing**.

> **Nota (2026-08-29, achado F1 do referee hostil dedicado, severidade
> BAIXA, precisão de enquadramento -- nenhum erro matemático):** chamar
> o segundo termo de "fine" enquanto o primeiro é "the wall" é impreciso
> -- ambos os termos são, na verdade, `O(Δ)=O(δy_1)` na MESMA ordem
> (o segundo termo, `(M_{y2}-M_{y1})\cdot\Psi(x,y_1)`, é exatamente
> `-\Delta\cdot\Psi(x,y_1)`, que NÃO se anula quando `y_1\to\infty` a
> `\delta` fixo, já que `\Psi` é apenas limitado, não decrescente).
> Nenhuma das duas peças isoladamente se anula; a conclusão de que a
> rota (a) falha permanece correta e inalterada (a SOMA continua
> não-limitada), mas o enquadramento "uma peça é inofensiva, a outra é
> o problema" não é preciso -- ambas contribuem igualmente para a
> falha. Fonte: `adversarial/REFEREE_REPORT.md`, achado F1.

This is the exact same
"`M_y` individually unbounded" fact `h1_translation_structure_attempt`'s
entire Part A/B was built to rescue — but that rescue was an EXACT
cancellation against `K_B`, a companion term specific to the `Φ`-Volterra
kernel's own structure. **No such companion term exists inside `(KEY)`
alone** — `M_{y2}·Δ_Ψ(x)` has nothing to cancel against here.

### 2.3 The direct route hits the same wall from a different angle

Without the `(E1)` substitution, `(KEY)` directly gives `Δ_W(x) = Δ_Ψ(x) -
ε·d/dx[Δ_Ψ(x)]`. `(⋆⋆)` bounds `sup_x|Δ_Ψ(x)|` — a sup-NORM bound, not a
bound on its `x`-DERIVATIVE. This is exactly the "derivative loss"
`h1_energy_estimate_attempt` Sec 8.4 named in general terms for its OWN
(different) contraction-mapping route; this front's Sec 2.2 makes the SAME
underlying obstruction concrete and specific for the `(KEY)`-transfer route
in particular — two syntactically different attempts into the identical
wall, confirming (not merely repeating) the predecessor's diagnosis with a
sharper mechanism.

**Conclusion: route (a) does not work.** No further attempt is made along
this line; Sec 3 pursues route (b) instead.

---

## 3. Route (b) — a relative-step oscillation bound on `Φ`, derived from
the closed-form kernel

Full symbolic bookkeeping: `s01_oscillation_bound_symbolic.py`/`.log`.

### 3.1 The exact `T0`/`T1`/`T2` split

Fix `x`, `y1<y2`, `Δ:=y2-y1`. From `(VOLTERRA-Phi)` at `y1` and `y2`,
splitting `y2`'s integration range at `y1` — **exact rearrangement, no
approximation**:

```
Phi_{y2}(x) - Phi_{y1}(x)
  = [g_{y2}(x) - g_{y1}(x)]                                    =: T0
  + int_0^{y1} [K(y2,t) - K(y1,t)] Phi_t(x) dt                  =: T1
  + int_{y1}^{y2} K(y2,t) Phi_t(x) dt                           =: T2
```

### 3.2 `T0`: trivial

`|T0| ≤ e^{-y1/ε}`, vanishing as `y1→∞` for any fixed `ε`, regardless of
`Δ`.

### 3.3 `T2`: the closed form beats the crude bound

For `t∈[y1,y2]`, `h:=y2-t∈[0,Δ]`, and `z:=x+y2` is CONSTANT across this
range (it depends on `y2`, not `t`). The crude operator-norm bound
(`DISC-DEC-113/115`) gives `|T2|≤Δ·(√(π/2)+ε)·M_Φ = O(Δ)` — for
`Δ=δ·y1`, this is `O(δ·y1)`, **useless** (does not vanish as `y1→∞` at
fixed `δ`). Using the CLOSED FORM instead (each `Φ_t` assumed to satisfy
`(C)` — flagged, Sec 3.5):

```
K(y2,t) Phi_t(x) = [Phi_t(x) - e^{-h/eps} Phi_t(x+h)] / z2 + O(1/z2^2)
```

giving `|T2| ≤ Δ·2M_Φ/z2 + Δ·O(1/z2²) = O(Δ/z2)` (the dominant term,
`sympy`-confirmed the ratio `(Δ/z2)/(Δ/z2²)=z2→∞` so `Δ/z2` genuinely
dominates). For `Δ=δy1`, `z2~y1(1+δ)`: `|T2| = O(δ)`, **uniformly in
`y1`** — this is where the closed-form asymptotic earns its keep over the
cruder operator bound.

### 3.4 `T1`: the hard integral over the full history `[0,y1]`

For `t∈[0,y1]`, `h1:=y1-t` ranges over the FULL `[0,y1]` — including `h1`
as large as `y1` itself (`t` near `0`, the "distant past"). Applying the
closed form to both `K(y2,t)` and `K(y1,t)` and subtracting:

```
K(y2,t)Phi_t(x) - K(y1,t)Phi_t(x)
  = Phi_t(x)*[1/z2-1/z1]  -  [e^{-h2/eps}Phi_t(x+h2)/z2 - e^{-h1/eps}Phi_t(x+h1)/z1]
    + O(1/z1^2)+O(1/z2^2)
  =: A_t - B_t + (error)
```

**`A_t` (bulk term)**: `1/z2-1/z1 = -Δ/(z1z2)` (`sympy`-verified
identity), CONSTANT in `t`. So `∫_0^{y1}A_t dt = -Δ/(z1z2)·A(y1)`,
`|A(y1)|≤y1M_Φ` (hypothesis `(B)`), giving `|∫A_tdt| = O(Δ/z1) = O(δ)`.

**`B_t` (exponentially-localized term)**: bounded CRUDELY, using ONLY
boundedness `(B)` — no smoothness assumption needed here at all, sidestepping
any accuracy concern about the closed form specifically in this piece:
`|∫_0^{y1}e^{-h1/ε}Φ_{y1-h1}(x+h1)dh1| ≤ M_Φ·ε·(1-e^{-y1/ε}) ≤ M_Φε`, and
similarly for the `h2=h1+Δ` piece (with an extra `e^{-Δ/ε}` factor `≤1`).
Total: `|∫B_tdt| ≤ M_Φε(1/z1+1/z2) = O(ε/y1)` — vanishes at FIXED `ε` as
`y1→∞`, with **no `δ`-dependence at all**.

**Error term**: `y1·O(1/z1²) = O(1/y1)`, GIVEN the closed form's `O(1/z²)`
remainder is uniform over the FULL `t∈[0,y1]` range, including `h1` close
to `y1` — this is hypothesis `(U)`, tested numerically in Sec 4 (NOT tested
by any ancestor front in this regime — Sec 3.5).

**Assembling**: `|T1| ≤ O(δ) + O(ε/y1) + O(1/y1) = O(δ) + O(1/y1)`.

### 3.5 The final bound, and its two open hypotheses

```
|Phi_{y2}(x) - Phi_{y1}(x)|  <=  C1(x,eps)*delta + C2(x,eps)/y1        (OSC-PHI)
```

for `y2-y1=δ·y1` (`0<δ<1`) — **exactly** the relative-step "slowly
oscillating" form the classical Tauberian theorem needs: for every `ε>0`,
choose `δ` small enough that `C1δ<ε/2`, then `Y` large enough that
`C2/Y<ε/2`; then `y1≥Y` and `0≤y2-y1≤δy1` give
`|Φ_{y2}(x)-Φ_{y1}(x)|<ε`.

**Two hypotheses this derivation needs, beyond the standing `(B)`:**

- **`(C')`**: a Lipschitz-type regularity bound on `Φ_t(·)`, UNIFORM in
  `t` — strictly stronger than the predecessor's `(C)` (needed there only
  for ONE fixed `f`). Not independently proved here, consistent with how
  `(B)` itself has never been independently proved anywhere in this
  lineage — disclosed, not hidden.
- **`(U)`**: the closed-form kernel's `O(1/z²)` remainder is uniform over
  the FULL range `h∈[0,y]`, including `h/y→1` — the predecessor
  (`h1_translation_structure_attempt` Sec 5.4) tested only `h=y/2` (a
  SINGLE fixed ratio, up to `y=3000`). This front's own `T1` bound
  specifically needs the "distant past" regime (`t→0`, i.e. `h1→y1`) that
  no ancestor tested. **Numerically tested fresh, Sec 4 below.**

---

## 4. Numerical verification of hypothesis `(U)`

Full logs: `s02_kernel_uniformity_h_to_y.py`/`.log`,
`s02b_kernel_uniformity_transition.py`/`.log`,
`s02c_kernel_uniformity_xnonzero.py`/`.log`. Raw kernel definitions
(`K_A^raw` via the single-integral reduction, `K_B`, `M_y` — established,
independently-referee-confirmed facts of record, cited not re-derived)
re-implemented FRESH, with de-stiffened quadrature (substitution `u=w/z`
for the inner integral, explicit breakpoints for the outer `h'`-integral
concentrated near its exponential-decay scale) — per this lineage's own
established discipline against naive `scipy`-style quadrature failures at
large `z` (the predecessor's referee found and root-caused a ~6-order-of-
magnitude failure mode from exactly this kind of naive quadrature).

**Sanity check first**: cross-validated against
`h1_translation_structure_attempt`'s own published Sec 5.4 value
(`x=0,ε=0.1,f=1/(1+x),h=y/2,y=10`: published `z·K(y,t)f(0)=0.9156333394`).
This front's independent implementation gives `0.9156333394`, agreeing to
`2.1×10⁻¹²` — confirms the fresh implementation is correct before trusting
any new result.

### 4.1 Full `h/y` ratio sweep at `ε=0.1` (`s02`)

`x=0`, `f∈{1/(1+x), e^{-x/3}}`, `z∈{100,500,2000}`, `h/y` ratio from `0.1`
to `0.99`: at `ε=0.1`, `h/ε` already exceeds `10` (deeply saturated,
`e^{-h/ε}≈0`) at EVERY tested ratio, so this sweep confirms `z²·err` is
**constant across the entire ratio range** (`-0.900` at `z=100` up to
`-0.908` at `z=2000` for the rational `f`; `-0.246`→`-0.237` for the
exponential `f`) — bounded, converging smoothly with `z`, **no blowup
anywhere as `h/y→0.99`** — but does not by itself stress the transition
region.

### 4.2 Combined transition + large-`h` sweep at `ε=5` (`s02b`)

To genuinely stress BOTH regimes in one run: `x=0`, `z=1000` (so `ε` is no
longer negligible relative to `z`), `h/y` from `0.0002` (`h/ε≈0.04`,
UNSATURATED) up to `0.99` (`h/ε≈198`, deeply saturated) — an 11-point sweep
crossing the entire transition on the way to the large-`h`/`(t→0)` regime
this front's `T1` bound needs:

| `h/y` | `h/ε` | `z²·err` |
|---|---|---|
| 0.0002 | 0.04 | −0.154 |
| 0.001 | 0.20 | −0.160 |
| 0.005 | 1.00 | +0.310 |
| 0.01 | 2.00 | +0.449 |
| 0.02 | 4.00 | +0.489 |
| 0.05–0.99 | 10–198 | +0.493 (stable) |

`max|z²·err|=0.493`, `min=0.154` — **bounded and smoothly varying through
the ENTIRE transition, with no divergence anywhere**, including deep into
the `h/y→1` regime. This is strictly more demanding than either `s02` or
the predecessor's own single-ratio `h=y/2` test.

### 4.3 Spot check away from `x=0` (`s02c`)

`x=3`, `ε=0.1`, `z∈{200,1000}`, ratios `{0.1,0.5,0.9}`: `z²·err` again
constant across all ratios at each `z` (`−0.039` at `z=200`, `−0.038` at
`z=1000`) — bounded, same order of magnitude as (in fact smaller than) the
`x=0` values at comparable `z`, **no sign of `(U)` breaking down away from
`x=0`** — a spot-check, not a proof of uniformity for all `x`, but
consistent with the analytic expectation (Sec 5.2).

**Conclusion: hypothesis `(U)` is well-supported numerically in exactly the
regime `(OSC-PHI)`'s derivation needs, including the previously-untested
`h/y→1` (distant-past) regime and away from `x=0`.** This is genuine new
numerical content, not merely a re-run of the predecessor's own test.

---

## 5. Ingredient (ii) — do the classical theorem's hypotheses transfer to
the two-variable PDE setting?

### 5.1 The abstract-function part: yes, verbatim

Once `x` is FIXED, `g(y):=Φ_y(x)` is, by hypothesis `(B)`, a bounded
function of `y` alone (`x` enters only as a fixed parameter). The classical
theorem's statement and proof (an abstract real-analysis fact about
bounded, Cesàro-summable, slowly-oscillating functions) make no reference
to `y` living inside a larger PDE — nothing about `Φ_y(x)` being a "slice"
of a two-variable solution, rather than an abstract one-variable function,
obstructs applying the theorem's proof once `(OSC-PHI)` and Cesàro
convergence (Sec 6) are both in hand, AT a fixed `x`. **This part of
ingredient (ii) transfers cleanly.**

### 5.2 `x`-uniformity: transfers, given `(C')` and `(U)` hold uniformly in `x`

`(U1)` demands LOCAL UNIFORM convergence over `x`, not merely pointwise
convergence at each fixed `x` — so it matters whether `(OSC-PHI)`'s
constants `C1(x,ε),C2(x,ε)` stay controlled as `x` ranges over a compact
interval `[0,X_max]`. Tracing through Sec 3's derivation: `M_Φ` (hypothesis
`(B)`) is a GLOBAL bound, independent of `x`; every bound obtained is
`O(1/z1)` or `O(1/z2)`-type, and since `z1=x+y1≥y1`, `z2=x+y2≥y2` for
`x≥0`, **every term in `(OSC-PHI)`'s derivation is automatically
non-increasing in `x` for `x≥0`** — the bound gets BETTER, not worse, as
`x` grows, GIVEN `(C')` and `(U)` themselves hold uniformly in `x` (Sec
4.3's spot-check at `x=3` is consistent with, though does not prove, this
for all `x`). **This part of ingredient (ii) is resolved positively, with
the caveat that `(C')`/`(U)`'s own `x`-uniformity is not exhaustively
tested (Sec 7 item 4).**

### 5.3 A minor inherited-scope note: `(U1)` as originally stated is about
`W`, not `Φ`

`(U1)`'s original statement (`DISC-DEC-088/091`) is about `W(x,g)`
converging locally uniformly as `g→∞`; from `DISC-DEC-096` onward this
sub-lineage has operationally worked with `Φ_y(x)` converging instead (via
`(E2)` and the Watson Concentration Lemma connecting the two). This front
inherits that operational identification, exactly as `h1_translation_
structure_attempt` (its immediate predecessor) and its referee both did
without flagging it as an issue — noted here for completeness, not
re-litigated, since doing so is outside this front's specific mandate.

---

## 6. The sharp new finding — a third, unaddressed hypothesis

Full derivation: `s03_cesaro_gap_counterexample.py`/`.log`.

### 6.1 The classical theorem needs THREE hypotheses, not two

Restating precisely (Sec 0): `(H-bdd)` `g` bounded; `(H-ces)` `(1/y)∫_0^y
g(t)dt→L` for SOME `L` [Cesàro-`(C,1)` convergence]; `(H-osc)` `g` slowly
oscillating (relative-step). **DISC-DEC-122/123's mandate names only two
missing ingredients — matching `(H-osc)` [ingredient (i)] and a general
"hypotheses transfer" check [ingredient (ii)] — but the classical theorem's
own hypothesis list has `(H-ces)` as a THIRD, logically independent item.**
Establishing `(H-osc)` (Sec 3, successfully, conditionally) does **not**
establish `(H-ces)`, and the unconditionally-proved self-averaging identity
(`Φ_y(x)-A(y)/(x+y)→0`) does not either — it only says the two SEQUENCES
differ by `o(1)`, which says nothing about whether either one has a limit.

### 6.2 A concrete counter-example: `g(t):=sin(log(1+t))`

**Part 1 — `g` satisfies `(H-bdd)` and `(H-osc)` exactly.** `|g(t)|≤1`
trivially. The relative-step oscillation: `g(y(1+δ_frac))-g(y)`, expanded
to first order in `δ_frac` (`sympy`, exact): `δ_frac·y·cos(log(1+y))/(1+y)`
— the coefficient `y·cos(log(1+y))/(1+y)` is bounded by `1` in absolute
value **for ALL `y≥0`, uniformly, with no exceptional points** (unlike a
piecewise-constant construction with boundaries, which would fail the
condition arbitrarily close to each boundary). Numerically confirmed at
`y∈{10,100,1000,10000}`, `δ∈{0.01,0.05,0.1}`: `|g(s)-g(y)|` stays `≤δ`
(or `O(δ)`) in every case tested — **`g` genuinely satisfies the EXACT
relative-step condition `(OSC-PHI)`'s form demands, for every `y`, not
merely eventually or on a subsequence.**

**Part 2 — the exact Cesàro mean, in closed form.** Via `t=e^u-1`:
`∫sin(u)e^u\,du = -√2·e^u·cos(u+π/4)/2` (`sympy`, exact). So:

```
int_0^Y g(t) dt  =  -sqrt(2)*(Y+1)*cos(log(Y+1)+pi/4)/2 + 1/2
Cesaro mean       =  [-sqrt(2)*(Y+1)*cos(log(Y+1)+pi/4) + 1] / (2Y)
```

**Verified by direct differentiation** (`sympy`, `d/dY[∫_0^Y g\,dt] -
g(Y) ≡ 0`, confirmed exactly) — a self-caught harness bug on the first run
(the check initially compared against the bare free symbol from the
integration variable rather than `g` evaluated AT `Y`, producing a
residual that itself still contained an unrelated free symbol — immediately
flagged as a harness bug, not a mathematical failure, and fixed by
substitution; disclosed here per this lineage's convention).

**Part 3 — NEITHER `g(Y)` nor its Cesàro mean converges.** As `Y→∞`, the
Cesàro mean is asymptotically `(1/2)(sin(log(1+Y))-cos(log(1+Y)))` — an
oscillation of amplitude `√2/2`, not a limit. Numerically confirmed,
`Y=10` through `Y=10^8`: both `g(Y)` and its Cesàro mean keep oscillating
without settling at every scale tested (e.g. at `Y=10^7`: `g=-0.399`,
Cesàro mean `=0.259`; at `Y=10^8`: `g=-0.416`, Cesàro mean `=-0.663` — no
trend toward convergence at 8 orders of magnitude in `Y`).

### 6.3 What this means for `(U1)`

`(H-bdd)`+`(H-osc)` genuinely, exactly holding (as this front's Sec 3
derives, conditionally, for `Φ`) is **not sufficient**, by this concrete
elementary example, to conclude convergence — `(H-ces)` must be
established SEPARATELY. For `M-CLUST(b)`, this means: even with `(OSC-PHI)`
in hand (Sec 3–4), **Cesàro-`(C,1)` convergence of `A(y)/(x+y)` itself is
STILL an open, unaddressed requirement**, not established anywhere in this
lineage's record (the numerically-observed plateau value,
`Φ(0,t0)=0.0377616` for `t0≥0.02`, from `FLOORH2`/`PLATRESUM`, is a
high-precision NUMERICAL/solver-convergence fact about a small-`t0` series
resummation — a structurally different route from the large-`y` Volterra
machinery this front and its direct ancestors work with, and does not by
itself constitute a proof that `A(y)/(x+y)` converges via THIS route).
**This is the genuinely new reduction this front contributes beyond what
`DISC-DEC-122` named**: not merely "ingredient (i) attempted, ingredient
(ii) checked" but a sharper map showing the classical theorem's actual
hypothesis list has one more independent item than the mandate's two-item
framing suggested, and that item remains entirely open.

---

## 7. What did NOT close, precisely

1. **`(U1)`/`(U2)`/`H1` are not closed.** `(OSC-PHI)` (Sec 3) is a genuine
   conditional derivation of relative-step slow oscillation for `Φ` — not a
   proof of convergence, and Sec 6 shows precisely why it cannot be one
   without an additional, independent ingredient.
2. **Cesàro-`(C,1)` convergence of `A(y)/(x+y)` is an open, unaddressed
   requirement** (Sec 6) — not attempted to completion here. One
   unexplored candidate route is named, not solved: an `L¹`-in-`y` /
   bounded-variation argument on `d/dy[A(y)/(x+y)] = [Φ_y(x)(x+y)-A(y)]/
   (x+y)²`, which via the self-averaging identity is formally `o(1)/(x+y)`
   — whether this is integrable in `y` (which would give convergence by
   the Cauchy criterion) is not examined, and is structurally a
   comparably-hard question, not an obvious shortcut.
3. **Hypothesis `(C')`** (Lipschitz regularity of `Φ_t(·)`, uniform in
   `t`) **is not independently proved** for the actual `Φ` of this system —
   assumed, consistent with how `(B)` itself is a standing, not
   independently proved, hypothesis throughout this entire lineage. It is
   STRICTLY STRONGER than the predecessor's single-fixed-`f` `(C)`.
4. **Hypothesis `(U)`'s `x`-uniformity** is spot-checked at `x=0` and
   `x=3` only (Sec 4.3), not exhaustively tested over a range of `x`, and
   not proved analytically from the closed-form derivation's own error
   bookkeeping (`h1_translation_structure_attempt` did not track the
   `x`-dependence of its `O(1/z²)` constant explicitly either).
5. **No fresh `(P,Q)`-family series solver was built** (Sec 1.2) — this
   front's numerical content tests elementary inequalities/identities and
   the raw kernel directly, not the actual physical `Φ` at specific
   `(c,s,g)` values. `(OSC-PHI)` is therefore verified analytically and via
   its key input hypothesis `(U)`, not by directly measuring
   `|Φ_{y2}(x)-Φ_{y1}(x)|` against the bound for the true solution.
6. **Route (a) is a confirmed dead end** (Sec 2) — not a partial result, a
   precisely-diagnosed closure of that avenue.
7. **`H2`, non-perturbative (trans-series) content**: untouched, out of
   scope, exactly as every ancestor front in this sub-line reports.

**No formula of record is proposed as a replacement for anything.**
`φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of
record are all untouched and unaffected by anything in this document.

---

## 8. Scorecard

| claim | status |
|---|---|
| Route (a) (`(⋆⋆)` transfer via `(KEY)`/`(E2)`) | **DEAD END, precisely diagnosed** (new identity `W=ε[M_yΨ+I]` verified; unbounded `M_y` with no cancellation partner is the exact obstruction, `s04`) |
| `(OSC-PHI)`: relative-step oscillation bound on `Φ` | **DERIVED** (conditional on `(B)`, `(C')` [new, stronger hypothesis], `(U)` [numerically tested]), `s01` |
| Hypothesis `(U)` (closed-form error uniform for `h/y→1`) | **NUMERICALLY CONFIRMED** in the previously-untested regime, 3 independent sweeps (`s02`,`s02b`,`s02c`), no blowup detected |
| Hypothesis `(C')` | **NOT independently proved** (assumed, disclosed, stronger than predecessor's `(C)`) |
| Ingredient (ii)(a): abstract-theorem transfer at fixed `x` | **CONFIRMED, clean** (Sec 5.1) |
| Ingredient (ii)(b): `x`-uniformity of `(OSC-PHI)`'s constants | **CONFIRMED analytically** (automatic, given `(C')`,`(U)` uniform in `x`), spot-checked numerically at `x=0,3` |
| Ingredient (ii)(c): Cesàro-`(C,1)` convergence of `A(y)/(x+y)` | **IDENTIFIED as a THIRD, separate, unaddressed requirement** — NOT established anywhere in this lineage's record (Sec 6, new finding) |
| Counter-example `g(t)=sin(log(1+t))` (bounded + exactly slowly-oscillating, yet non-convergent, Cesàro mean also non-convergent) | **PROVED** (exact `sympy` derivation + `mpmath` numerical confirmation, `s03`) |
| `(U1)` (locally-uniform `y→infinity` convergence, operationally: of `Φ`) | **OPEN** (unchanged) |
| `(U2)` | **OPEN** (unchanged) |
| `H1` | **OPEN** (unchanged) |
| `H2` | **NOT ATTEMPTED** (out of scope) |
| Classical Tauberian theorem applied to close `(U1)` | **NOT APPLICABLE YET** — hypothesis `(H-ces)` [Cesàro convergence] missing, independent of `(H-osc)` |

`H1` remains ABERTO/OPEN. `φ_REDB`, `Φ_U(c)`, `Φ_infinity(c)`, and the
four-term asymptotic law of record are all untouched and unaffected by
anything in this document.

---

## 9. Recommendation on this angle

Per `DISC-DEC-123`'s explicit checkpoint: this front DOES produce a
genuinely new reduction beyond what `DISC-DEC-122` named — not merely an
attempt at the two named ingredients, but the identification that the
classical theorem's hypothesis list has a third, independent item
(`H-ces`) that neither ingredient (i) nor ingredient (ii) as originally
framed addresses, concretely illustrated (Sec 6) rather than asserted. This
is real progress, not a repetition.

That said: **this specific angle (the classical continuous Tauberian
theorem applied to the self-averaging identity) now has a clearly-named,
seemingly hard, terminal-looking requirement** (`H-ces`, Sec 6.3) that does
not appear to follow from anything currently in this lineage's record by
an easy argument — establishing Cesàro convergence of a running average is,
in general, not obviously easier than establishing convergence of the
original sequence, and the one candidate route named here (Sec 7 item 2)
is speculative, not scoped. A future wave attempting to continue THIS
specific Tauberian angle should attack `(H-ces)` directly and head-on,
rather than revisiting `(H-osc)` (now reasonably well-established,
conditionally) — or the orchestrating session may reasonably judge, per
the checkpoint's own terms, that a fundamentally different angle on
`M-CLUST(b)`'s `H1`/`(U1)`/`(U2)` gap (not building further on the
self-averaging/Tauberian machinery specifically) is a better use of an
eighth wave, given seven consecutive waves have now worked this exact gap.
Both are legitimate; this front does not have a basis to prefer one over
the other beyond what is stated here.

> **Nota (2026-08-29, achado F2 do referee hostil dedicado, severidade
> MODERADA, construtivo -- reforça, não contradiz, a recomendação
> acima):** o referee identificou um corolário mais afiado do próprio
> achado da Seção 6 deste documento: dado que a ponte de auto-mediação
> incondicional `\Phi_y(x)-A(y)/(x+y)\to0` já está PROVADA (herdada de
> `DISC-DEC-122`), `(H\text{-}ces)` -- convergência de Cesàro de
> `A(y)/(x+y)` -- é, sozinha, NECESSÁRIA E SUFICIENTE para `(U1)`, via
> simples desigualdade triangular (duas sequências que diferem por
> `o(1)` convergem ao mesmo limite se e somente se uma delas converge).
> Isto torna `(H\text{-}osc)`/`(OSC-PHI)` -- o resultado técnico central
> desta própria frente (Seção 3) -- logicamente DESNECESSÁRIO como
> degrau intermediário para fechar `(U1)` especificamente: o teorema
> Tauberiano clássico completo (com suas três hipóteses) é uma
> ferramenta mais forte do que o necessário aqui, já que a identidade de
> auto-mediação já faz todo o trabalho que `(H-osc)` faria. Isto NÃO
> invalida `(OSC-PHI)` como resultado matemático em si (permanece
> provado, condicional a `(C')` e `(U)`, e continua um resultado novo e
> genuíno sobre o núcleo `K(y,t)`) -- apenas esclarece que ele não é a
> rota mais direta para `(U1)`. Reforça, sem contradizer, a recomendação
> acima: uma oitava onda que queira continuar esta linha deveria atacar
> `(H-ces)` diretamente, sem precisar primeiro re-estabelecer
> `(H-osc)`. Fonte: `adversarial/REFEREE_REPORT.md`, achado F2.

---

## 10. Seeds

Reserved range `20260935000-20260935999` per `DISC-DEC-123`. Grep-confirmed
BEFORE any use (`grep -rn "20260935" 05_DISCOVERY_LAB/`): appeared only in
`DECISION_LEDGER.yaml`'s own `DISC-DEC-123` reservation line. Re-confirmed
again at the end of this front (same command, same result): still appears
ONLY in that reservation line, and nowhere inside this front's own new
directory. **No randomness was used anywhere in this front** — every
computation is exact symbolic algebra (`sympy`) or deterministic
arbitrary-precision adaptive quadrature (`mpmath`, fixed evaluation
strategy with explicit de-stiffening substitutions, no sampling) — exactly
as every direct ancestor front in this exact sub-lineage reports for its
own reservation. The reserved range remains entirely unused.

---

## 11. Files

| file | role |
|---|---|
| `s01_oscillation_bound_symbolic.py`/`.log` | the `T0`/`T1`/`T2` split of `Φ_{y2}(x)-Φ_{y1}(x)`, elementary algebraic bookkeeping (`sympy`), deriving `(OSC-PHI)` and naming hypotheses `(C')`,`(U)` (Sec 3) |
| `s02_kernel_uniformity_h_to_y.py`/`.log` | numerical test of hypothesis `(U)` at `ε=0.1`: full `h/y` ratio sweep `0.1`–`0.99` at `z∈{100,500,2000}`, 2 test functions, plus sanity check against the predecessor's own published Sec 5.4 value (agreement `2.1e-12`) (Sec 4.1) |
| `s02b_kernel_uniformity_transition.py`/`.log` | numerical test of hypothesis `(U)` at `ε=5,z=1000`: combined sweep crossing the `h~ε` transition AND the large-`h`/`h→y` regime in one run, 11 points (Sec 4.2) |
| `s02c_kernel_uniformity_xnonzero.py`/`.log` | numerical spot-check of hypothesis `(U)` at `x=3` (nonzero), supporting `x`-uniformity (Sec 4.3, Sec 5.2) |
| `s03_cesaro_gap_counterexample.py`/`.log` | the `g(t)=sin(log(1+t))` counter-example: exact symbolic derivation (`sympy`) plus numerical confirmation (`mpmath`) that bounded + exactly-relative-step-slowly-oscillating does NOT imply convergence, establishing the Sec 6 finding; includes one self-caught, disclosed harness bug |
| `s04_route_a_key_transfer_symbolic.py`/`.log` | route (a) analysis: the new `W=ε[M_yΨ+I]` identity, and the precise diagnosis of why transferring `(⋆⋆)` via `(KEY)`/`(E2)` is a dead end (Sec 2) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this front's own new
`tauberian_oscillation_bound_attempt/` subdirectory was written to — every
ancestor `ATTEMPT.md`/`adversarial/` file and `PROOF_DEPENDENCY_MAP.md`/
`THEOREM.md`/`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md`
further up the tree were read-only references (Sec 0), never modified. No
`adversarial/` subdirectory created; no referee dispatched by this front
itself, per the mandate.

---

## 12. Scope discipline confirmation

- No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
  `index.html`, or any file outside this front's own new
  `tauberian_oscillation_bound_attempt/` directory — including the parent
  `h1_translation_structure_attempt/` directory and its own ancestor
  siblings (`h1_volterra_attempt/`, `h1_post_correction_attempt/`,
  `h1_energy_estimate_attempt/`, `mclust_h2_validity_attempt/`), all read
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
- One self-caught error (Sec 6.2, `s03`) was found by this front's OWN
  symbolic-verification check (comparing an antiderivative's derivative
  against a bare, un-substituted free symbol, producing a residual that
  visibly still contained that unrelated symbol — immediately flagging
  itself as a harness bug, not a mathematical failure), fixed in place, and
  disclosed here with the before/after visible in the committed `.py` file
  — found by this front itself, not by an external referee.
- No `THEOREM.md`-tier claim of closure is made anywhere in this document.
  Per the mandate's explicit caution: this front does **not** believe it
  has closed `(U1)`, and states this plainly and repeatedly (VERDICT UP
  FRONT, Sec 6.3, Sec 7, Sec 8, Sec 9) rather than hedging toward an
  overclaim.
