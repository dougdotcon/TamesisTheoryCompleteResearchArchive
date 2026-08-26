# Continuum-native Theorem J, attempted by transfer — a new reduction that bypasses the destination-information obstruction, an exact K=0,1 closure, and a precisely relocated remaining gap

> **Governance.** Wave 18, front (c) (`JOINT-EXPLORATION-CONTINUUM-ATTEMPT`),
> authorized by `DISC-DEC-078` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Mandate:
> complete the continuum-native version of Theorem J (`THEOREM.md`
> Estágio 25, §6.3 — attempted, explicitly not completed; same
> obstruction as Estágio 18 §3.3). `THEOREM.md` is **not** edited by
> this document, nor any ledger/governance/portfolio file. No git
> command was run. No `adversarial/` subdirectory created, no referee
> dispatched, per mandate. All work confined to this new subdirectory.
> Seeds: reserved block `20260874000`–`20260875000`, grep-confirmed
> unused before first use (see `PREREG.md`); referee range
> `20260875000+` not used.

> **Executive summary (read first).** The mandate offered two distinct
> acceptable routes: (1) a from-scratch continuum construction directly
> from Definition 3's primitives, or (2) a rigorous `n\to\infty`
> *transfer* of the already-proved finite Theorem J. **This document
> does not re-attempt route (1)** — a third blind attempt at
> constructing a genuine joint two-point exploration on `L(c)` is not a
> "genuinely new angle" on an obstruction two prior fronts (Estágio 18,
> Estágio 25 §6.3) have already independently stalled on for the same
> stated reason. Instead it finds and executes **route (2)**, via an
> angle that appears not to have been tried: **Theorem J's Corollary is
> an *exact algebraic identity* at every finite `n,K`** (not merely
> asymptotic), so dividing through it and passing to the limit is valid
> **for free**, with *zero* new joint-exploration machinery, provided
> only that the purely scalar total `P_n^{(K)}(\text{both cyclic})`
> converges — a **marginal-type, not joint-dynamics**, question,
> structurally parallel to the *already-closed* first-moment fixed-`K`
> bridge (`THEOREM.md` Estágio 3–6), just one moment order up. This
> reduction is new: it is not stated anywhere in `THEOREM.md`, Estágio
> 18, or Estágio 25.
>
> **What this document proves, unconditionally:**
> 1. **The Reduction Proposition** (§2, PROVED): for any fixed `K`, IF
>    `P_n^{(K)}(\text{both cyclic})\to\tau_K` as `n\to\infty`, THEN
>    `P_n^{(K)}(\text{same final cycle})\to\tau_K/2`, automatically, by
>    Theorem J's Corollary alone — no extension of Definition 3 needed.
> 2. **A new exact closed form for the second-moment fixed-`K=1`
>    bridge** (§3, PROVED): `P_n^{(1)}(0,1\text{ both cyclic}) =
>    \frac{3n^2-n+2}{6n^2} = \frac12-\frac1{6n}+\frac1{3n^2}` for every
>    `n\ge2` — the two-point analogue of `THEOREM.md` Proposition 4,
>    generalizing its method from one query point to two. It converges
>    to `\tfrac12 = E[M_1^2]` (already PROVED in the continuum directly,
>    Estágio 24) at rate `\Theta(1/n)` — **slower** than the marginal
>    bridge's `\Theta(1/n^2)` rate (Corollary 4.3), for a precise,
>    identified reason (§3.3): an `O(1/n)`-probability event — the
>    single reroute source coinciding with one of the two query points —
>    that has no counterpart at all in the one-point marginal
>    computation.
> 3. **Trivial exact closure at `K=0`** (§3.1): `P_n^{(0)}(\text{both}) =
>    1` for every `n` (no reroutes, `f=\pi`, everyone cyclic), reducing
>    Theorem J at `K=0` to the classical fact `P(\text{same cycle})=1/2`
>    for a uniform random permutation (elementary; already cited without
>    further attribution throughout this lineage, e.g.
>    `.../joint_two_point_attempt/ATTEMPT.md` §3).
> 4. **Combining 1–3: a new PROVED continuum theorem, by transfer, not
>    construction.** `P(x_1,x_2\text{ same final cycle in }L(c)\mid
>    \text{exactly }K\text{ marks}) = 1/(2(K{+}1))` for `K=0,1`
>    (`=1/2, 1/4`), obtained **without ever constructing a joint
>    two-point exploration process on `L(c)`**, and hence **without
>    resolving, or needing to resolve, the destination-information
>    obstruction Estágio 18 §3.3 and Estágio 25 §6.3 named.** This is
>    the first genuinely continuum-native piece of Theorem J's content
>    obtained since Estágio 25 first proved the finite theorem.
> 5. **`K\ge2`: honestly NOT closed**, with a precise account of why
>    (§4): the same-order combinatorial explosion that made the
>    *marginal* `K=2` fixed-`K` bridge require a dedicated front
>    (`THEOREM.md` Estágio 3) rather than direct hand computation
>    applies here too, now to a joint (not marginal) quantity. Exact
>    enumeration (§4.1, `n` up to 7) and coarse large-`n` Monte Carlo
>    (§4.2, `n=2000`, `K=2,3,4,5`, fresh seeds) are both consistent with
>    — but do not prove — convergence to the already-known continuum
>    target `1/(K{+}1)` (Estágio 24). A genuine closure of this specific
>    narrower bridge is named as the natural next target for a future
>    front (§6).
> 6. **What this result does NOT do, stated precisely (§5):** it does
>    not touch, resolve, or weaken Estágio 18/25's diagnosis of the
>    *from-scratch* obstruction — it is a scalar-transfer end-run around
>    it for the *specific* question Theorem J already reduced to a bare
>    number. Any question about the *physical/geometric* structure of a
>    genuine two-point exploration on `L(c)` (e.g. "where," not just
>    "whether," relative to marks) remains exactly as open as before
>    this document.
> 7. **One self-disclosed false start** (§3.2, in the archive's
>    disclosure tradition — see `../ATTEMPT.md` §7.1 for style): the
>    first hand-derivation of the `K=1` closed form silently assumed
>    the single reroute source is always disjoint from the two query
>    points, missing an `O(1/n)`-weight case entirely and producing a
>    *wrong* closed form (`5/9` instead of the correct `13/27` at
>    `n=3`) — caught by cross-checking against exhaustive brute force
>    before it went anywhere near this document's main claims.
>
> **Net verdict.** A genuine, new piece of continuum-native content for
> Theorem J is established — by transfer, unconditionally at `K=0,1` —
> together with a precise, narrower, well-posed open lemma for `K\ge2`
> that is a **different and more tractable target** than Estágio 18's
> original obstruction (it is a scalar limit, not a joint-dynamics
> construction), and an explicit statement of what remains completely
> untouched. No Millennium Problem claim of any kind; pure internal
> combinatorics on this archive's own random-permutation-with-reroutes
> ensemble.

---

## 1. Setup and recap (cited, not re-derived)

Work in `THEOREM.md`'s **Definition 4** (finite conditional-`K` model,
§7.2) exactly as `.../joint_two_point_attempt/ATTEMPT.md` §1 sets it
up: `\pi` a uniform random permutation of `[n]=\{0,\dots,n-1\}`,
`R\subseteq[n]` a uniform random `K`-subset (the reroute sources),
`U_i` i.i.d. `\mathrm{Uniform}([n])` for `i\in R`, `f(i):=U_i` if
`i\in R`, `f(i):=\pi(i)` otherwise. `C(f)` is the (disjoint-cycle)
cyclic set.

**Theorem J (CITED, Estágio 25, PROVED there).** Conditional on
`C(f)=c` (`|c|=m\ge2`), `f|_c` is exactly uniform over
`\mathrm{Sym}(c)`.

**Corollary (CITED, Estágio 25, PROVED there, EXACT at every finite
`n,K`).** For fixed distinct `i,j\in[n]`,

`P_n^{(K)}(i,j\text{ both cyclic, same final cycle}) =
P_n^{(K)}(i,j\text{ both cyclic, different final cycles}) =
\tfrac12\,P_n^{(K)}(i,j\text{ both cyclic})`.  (★)

This is the single fact this document's entire route rests on. It is
re-cited, not re-proved (`.../joint_two_point_attempt/ATTEMPT.md` §2–3
has the full proof, independently re-verified by a hostile referee,
`.../joint_two_point_attempt/adversarial/REFEREE_REPORT.md`).

**Notation.** `P_n^{(K)}(\text{both}) := P_n^{(K)}(0,1\text{ both
cyclic})` (fixed distinct labels `0,1`; by Definition 4's own
exchangeability argument, `THEOREM.md` §7.2, this does not depend on
*which* pair, only on `n,K` — the exact same style of reduction
`THEOREM.md` already uses for `\varphi_n^{(K)}`). This is the finite-`n`
analogue of the continuum quantity `E[M_K^2]` — the identity
`E[M_K^2] = P(x_1,x_2\text{ both cyclic in }L(c)\mid K)` for two
independent uniform points is Fubini–Tonelli, the exact same device
`THEOREM.md` §2.4 uses for the mean (`\varphi_\infty(c)=E[M(c)]`), see
also `.../conjecture2_direct_attempt/ATTEMPT.md` §2.

**Cited target (Estágio 24, PROVED directly on `L(c)`, no finite-`n`
limit involved).** `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` on `(0,1)` for every
`K\ge1` (`M_0\equiv1` trivially), hence `E[M_K^2]=1/(K{+}1)` for
**every** `K\ge0`, exactly, as a fact about `L(c)` itself. This is
already a continuum-native fact; this document does not re-derive it
— it *uses* it as the target the second-moment fixed-`K` bridge must
converge to, if it converges at all.

---

## 2. The Reduction Proposition

> **Proposition R (reduction; PROVED, elementary).** Fix `K\ge0`.
> Suppose `\displaystyle\lim_{n\to\infty}P_n^{(K)}(\text{both}) =
> \tau_K` exists. Then
> `\displaystyle\lim_{n\to\infty}P_n^{(K)}(\text{same final cycle}) =
> \tau_K/2`.

*Proof.* By (★), `P_n^{(K)}(\text{same}) = \tfrac12 P_n^{(K)}(\text{both})`
identically, for **every** `n` — an exact algebraic identity, not an
asymptotic one, with no error term to control. Multiplication by the
constant `\tfrac12` is continuous, so
`\lim_n P_n^{(K)}(\text{same}) = \tfrac12\lim_n P_n^{(K)}(\text{both}) =
\tau_K/2`. `\square`

**Why this is the right new angle, precisely.** Every previously
attempted route into the continuum two-point law (`PREREG.md`'s
inherited S1–S3, Estágio 18 §3.3, Estágio 25 §6.3) tried to build a
*joint dynamical process* — run two hazard-clock explorations
simultaneously, tracking enough shared destination information to know
whether they end up on the same background block and, eventually, the
same final cycle. Proposition R shows that for the **specific** target
"same vs. different, given both cyclic" — as opposed to, say, the
detailed *shape* of the joint exploration — no such process needs to
be built at all: Theorem J already collapses the entire same/different
question, at every finite `n`, to a bare multiplicative constant times
the *total* both-cyclic probability, and that total is a **marginal**
quantity in the relevant sense (a sum/count, not a joint-dynamics
object) — exactly the kind of thing `THEOREM.md`'s own Stage 2
machinery (Estágio 3–6) already knows how to attack for the *first*
moment. This is why the resulting open problem (§4) is narrower and
structurally different in kind from Estágio 18/25's obstruction, not
merely a restatement of it.

**What Proposition R does *not* need, and what it costs.** It needs
*nothing* about Definition 3, no extension of the hazard-clock
primitives, and no physical/geometric reasoning about where marks land
relative to two points. Its cost is entirely concentrated in proving
`\tau_K` exists (and, separately — though this document argues it is
the natural expectation, not a free assumption — that `\tau_K` equals
the already-known continuum value `1/(K{+}1)`, i.e. that the finite
model really converges to the continuum one at second order, the same
kind of non-trivial fact the first-moment bridge needed genuine proof
for, `THEOREM.md` Estágio 3–6). §3 proves exactly this, unconditionally,
at `K=0,1`.

---

## 3. Exact closure at `K=0,1`

### 3.1 `K=0` (trivial, exact for every `n`)

With `K=0`, `f=\pi`, a permutation — every point of a permutation is
cyclic (`THEOREM.md` §7.3's identical remark for the marginal case).
So `P_n^{(0)}(\text{both})=1=E[M_0^2]` for every `n`: `\tau_0=1`
trivially, no limit needed. By Proposition R,
`P_n^{(0)}(\text{same})\to1/2` — but in fact this holds **exactly at
every finite `n`** too (Theorem J at `K=0` degenerates to "`\pi` itself
is uniform on `\mathrm{Sym}([n])`," which it is by definition, so the
Corollary's `1/2` is just the classical fact `P(i,j\text{ same
cycle})=1/2` for a uniform permutation — already cited throughout this
lineage, e.g. `.../joint_two_point_attempt/ATTEMPT.md` §3). This case
is a consistency check on the whole framework, not new content.

### 3.2 `K=1`: derivation, with a disclosed false start

**Setup.** Fix query points `0,1`. `R=\{r\}` for `r` uniform on
`[n]`. Two structurally different situations:

**Case (a): `r\notin\{0,1\}`** (probability `(n-2)/n`) — the reroute
source is a third point, disjoint from the query pair; call it `0'`
generically (i.e. this is literally Proposition 4's own setup, with
the query pair playing the role of two *generic other* points).

**Case (b)/(c): `r\in\{0,1\}`** (probability `2/n`) — the reroute
source **is** one of the two query points themselves.

**The false start (self-caught, disclosed per archive convention —
see `.../joint_two_point_attempt/ATTEMPT.md` §7.1 for style).** The
first hand-derivation attempted here treated only Case (a) — i.e. it
implicitly assumed the reroute source is always some point other than
`0,1`, exactly reusing Proposition 4's case analysis (offset of a
point within the rerouted point's `\pi`-cycle) for *both* query points
at once, and averaging. This gives a specific closed form (call it
`V_a(n)`, recovered exactly in `debug_k1_subcases.py`) that **is
correct as the Case-(a) conditional value**, but was wrongly reported
as the unconditional answer. Cross-checking against exhaustive brute
force caught this immediately: at `n=3`, the false-start value is
`5/9`, while brute force gives `13/27\ne5/9`. The error is an omission,
not an arithmetic mistake: Case (b)/(c) has probability `O(1/n)`, easy
to overlook as "negligible," but it contributes an `O(1)`-different
conditional value (see below), so it changes the **leading-order rate**
of convergence, not just a lower-order correction — this is exactly
the kind of error the archive's own K=1 marginal proof (Proposition 4)
is structured to avoid by explicitly summing over *all* of `U`'s `n`
possible values rather than "the generic case," a discipline this
document's second attempt (below) restores.

**Case (a), derived exactly.** Let `L` be the length of `\pi`'s cycle
containing the reroute source (`\sim\mathrm{Uniform}\{1,\dots,n\}`,
Proposition 4 Step 1, PROVED there). Given `L=\ell`, classify whether
`0,1` (both, one, or neither) are among the `\ell-1` other members of
that cycle (a hypergeometric computation on the `(n-1)`-point
complement of the reroute source):

`P(\text{neither}\mid\ell) = \dfrac{(n-\ell)(n-\ell-1)}{(n-1)(n-2)}`,
`\quad P(\text{exactly one}\mid\ell) = \dfrac{2(\ell-1)(n-\ell)}{(n-1)(n-2)}`,
`\quad P(\text{both}\mid\ell) = \dfrac{(\ell-1)(\ell-2)}{(n-1)(n-2)}`.

Writing `c_0` for the reroute source and `c_1,\dots,c_{\ell-1}` for the
rest of its cycle in forward `\pi`-order, a direct re-derivation of
`THEOREM.md` Proposition 4 Step 3's case split (which point of `C`
ends up cyclic, as a function of the reroute target `U`) gives, for
`k\ge1`: **`c_k` is cyclic iff `U\in\{c_1,\dots,c_k\}`** (probability
`k/n`), and `c_0` is cyclic iff `U\in C` at all (probability `\ell/n`)
— a clean sharpening of Proposition 4's within-`C` case analysis into a
per-point rule, verified directly against the case-by-case description
there. Consequently, for two points at offsets `j<k` (`j,k\ge1`),
`\{c_j\text{ cyclic}\}\subseteq\{c_k\text{ cyclic}\}` (a strict
containment of events — the point *closer* to the reroute source, in
forward order, is cyclic whenever the farther one is), so **both
cyclic `\iff` the nearer one is**, with probability `\min(j,k)/n`.

Given "both" (offsets uniform without replacement over
`\{1,\dots,\ell-1\}`), `E[\min(j,k)]=\ell/3` (standard fact for two
distinct uniform draws from `\{1,\dots,m\}`: `E[\min]=(m{+}1)/3`, here
`m=\ell-1`). Given "exactly one" (its offset uniform over
`\{1,\dots,\ell-1\}`, the other point untouched hence automatically
cyclic), `E[\text{offset}]=\ell/2`, so the conditional both-cyclic
probability is `\ell/(2n)`. Given "neither," both points' own cycles
are untouched by the reroute, so both are cyclic with probability `1`
(`THEOREM.md` §7.3 Step 2's argument, applied to two points instead of
one). Assembling and averaging over `L\sim\mathrm{Uniform}\{1,\dots,n\}`:

`V_a(n) := P(\text{both}\mid\text{Case a}) = \dfrac1n\sum_{\ell=1}^n
\left[P(\text{neither}\mid\ell)\cdot1 + P(\text{one}\mid\ell)\cdot
\dfrac\ell{2n} + P(\text{both}\mid\ell)\cdot\dfrac\ell{3n}\right]
= \dfrac{3n+1}{6n}`  (exact, `sympy` closed form).

**Case (b)/(c), derived exactly.** WLOG (by relabeling) `r=0` (the
query point `0` is itself the reroute source; `1` is not). Let `L` be
the length of `\pi`'s cycle containing `0`. `1\in C_0` with probability
`(\ell-1)/(n-1)` given `L=\ell`, at a uniform offset `d\in\{1,\dots,
\ell-1\}` if so; else `1\notin C_0` with probability `(n-\ell)/(n-1)`.
If `1\notin C_0`: `1` is automatically cyclic (untouched), and `0`
(the reroute source itself, at "offset `0`") is cyclic iff
`U\in C_0`, probability `\ell/n`. If `1\in C_0` at offset `d\ge1`: by
the same per-point rule as Case (a) (`c_0` cyclic iff `U\in C`; `c_d`
cyclic, `d\ge1`, iff `U\in\{c_1,\dots,c_d\}`, and the latter implies
the former, exactly as before), both cyclic iff `1=c_d` is cyclic,
probability `d/n`. Averaging over `d\sim\mathrm{Uniform}\{1,\dots,
\ell-1\}` (`E[d]=\ell/2`) and assembling:

`V_b(n) := P(\text{both}\mid\text{Case b or c}) = \dfrac1n\sum_{\ell=1}^n
\dfrac{\ell(2n-\ell-1)}{2n(n-1)} = \dfrac{n+1}{3n}`  (exact, `sympy`
closed form; Case (c) gives the identical value by the symmetric
relabeling `0\leftrightarrow1`).

**Reassembly.**

> **Proposition K1 (PROVED).** For every `n\ge2`,
>
> `P_n^{(1)}(\text{both}) = \dfrac{n-2}n V_a(n) + \dfrac2n V_b(n) =
> \dfrac{3n^2-n+2}{6n^2} = \dfrac12-\dfrac1{6n}+\dfrac1{3n^2}`.

Both `V_a,V_b`, and the reassembled total, are cross-checked **exactly**
against fresh brute-force enumeration (`n=3,\dots,6`, `debug_k1_subcases.py`
— zero mismatches, including with `R` held *fixed* rather than averaged,
isolating each sub-case independently) and the reassembled total is
further cross-checked against the *original* full brute-force
enumeration over all `R` (`second_moment_bridge_exact.py`, `n=2,\dots,7`
— zero mismatches). `n=6` also independently reproduces the value
`44/135` that `.../joint_two_point_attempt/ATTEMPT.md` §4.2 reports
for a *different* quantity in a *different* front's script
(`P_\text{both}` at `n=6,K=2` there — a coincidental numeric match at
a different `K`, noted here only to record that it was checked and is
not evidence of anything; the genuine cross-checks are the exact
sympy/brute-force agreements just described).

### 3.3 The rate: `\Theta(1/n)`, and precisely why

`P_n^{(1)}(\text{both}) - \tfrac12 = -\dfrac1{6n}+\dfrac1{3n^2}`, so
`n\big(P_n^{(1)}(\text{both})-\tfrac12\big) \to -\tfrac16` — an exact
`\Theta(1/n)` rate. This is a genuinely new, precise observation: the
marginal fixed-`K=1` bridge (`THEOREM.md` Corollary 4.3) converges at
rate `\Theta(1/n^2)` (`\varphi_n^{(1)}-\varphi_1 = 1/(3n^2)` exactly),
**one order faster** than the second-moment bridge just proved here.
The reason is identifiable directly from the derivation: the
`O(1/n)`-weight Case (b)/(c) — the reroute source coinciding with one
of the *two* query points — has **no counterpart whatsoever** in the
one-point marginal computation (there is only one query point, so
"the reroute source is one of the query points" is a *single* point
event already folded into the marginal computation's own definition,
not a distinguishable extra case). For two query points, this event
has probability `\Theta(1/n)` and shifts the conditional value from
`V_a(n)\to\tfrac12` to `V_b(n)\to\tfrac13` — an `O(1)` jump — which
is exactly enough to produce an `O(1/n)` contribution to the overall
average (`\tfrac2n\cdot\Theta(1)`), dominating whatever `O(1/n^2)`
behavior Case (a) alone would have shown. **This is a structural fact
about second (and, presumably, higher) moments of the cyclic-count
functional that has no analogue at first order** — worth flagging
explicitly for any future front attempting a general-`K` version:
the collision-probability heuristic sketched in `THEOREM.md` §7.4 for
the marginal case (`O(K^2/n)` collision probability, driving an
`O(1/n)` *marginal* rate for `K\ge2`) is the *same order of magnitude*
as the *unavoidable* query-point-collision term identified here, so a
general-`K` second-moment bridge should be expected, on this evidence,
to converge at rate `\Theta(1/n)`, not faster, **for every `K\ge0`**
(the `K=0` case is exact with zero error at every `n`, a degenerate
boundary case, not a counterexample to this expectation for `K\ge1`).

> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-081.]** O referee
> hostil (`adversarial/REFEREE_REPORT.md` §5) encontrou e confirmou que
> a frase acima — "dominating whatever `O(1/n^2)` behavior Case (a)
> alone would have shown" — está **errada**, contradita pela própria
> fórmula de `V_a(n)` do documento: `V_a(n)=(3n+1)/(6n)=\tfrac12+\tfrac1{6n}`
> já tem desvio `\Theta(1/n)` explícito e exato, não `\Theta(1/n^2)`.
> Decomposição correta (via `(n-2)/n\cdot V_a(n) =
> \tfrac12-\tfrac5{6n}-\tfrac1{3n^2}` e `\tfrac2n\cdot V_b(n)`-ponderado
> com coeficiente `+2/3`): os dois termos `O(1/n)` **cancelam
> parcialmente** (`-5/6+2/3=-1/6`) para dar a taxa `-1/6` corretamente
> relatada — Casos (a) e (b)/(c) contribuem individualmente em
> `O(1/n)`; nenhum é desprezível, e não compõem como "base `O(1/n^2)`
> mais perturbação `O(1/n)`". Este erro está confinado à narrativa
> causal explicativa desta seção; **não afeta** a Proposição K1, a
> reassemblagem, nem o valor da taxa `-1/6` em si, todos independentemente
> confirmados corretos pelo referee. Diagnóstico correto provável
> (oferecido pelo referee como observação, não como resultado provado):
> a taxa mais lenta é um efeito posicional conjunto de dois pontos já
> presente dentro do próprio Caso (a) (via o termo `E[\min(j,k)]/n`, sem
> análogo no problema marginal de um ponto), não algo atribuível
> exclusivamente à colisão fonte-do-reroute/ponto-de-consulta.

---

## 4. `K\ge2`: not closed, precisely why, and what the numbers show

### 4.1 Exact enumeration (small `n`, no closed form obtained)

`second_moment_bridge_exact.py` extends brute-force enumeration
(arbitrary-precision, no randomness) to `K=2` (`n=3,\dots,7`) and `K=3`
(`n=4,\dots,6`):

| `n` | `K=2`: `P_n^{(2)}(\text{both})` | `n(\text{val}-1/3)` |
|---|---|---|
| 3 | `10/27\approx0.3704` | `1/9\approx0.111` |
| 4 | `49/144\approx0.3403` | `1/36\approx0.028` |
| 5 | `33/100=0.3300` | `-1/60\approx-0.017` |
| 6 | `44/135\approx0.3259` | `-2/45\approx-0.044` |
| 7 | `143/441\approx0.3243` | `-4/63\approx-0.063` |

| `n` | `K=3`: `P_n^{(3)}(\text{both})` | `n(\text{val}-1/4)` |
|---|---|---|
| 4 | `19/64\approx0.2969` | `3/16=0.1875` |
| 5 | `3383/12500\approx0.2706` | `129/1250\approx0.1032` |
| 6 | `233/900\approx0.2589` | `4/75\approx0.0533` |

Both series are monotone decreasing and heading toward their
respective targets `1/3,1/4` (matching Estágio 24's continuum values),
but **`n(\text{val}-\text{target})` has not stabilized by `n=7`** — a
three-term rational-function fit (in `second_moment_bridge_exact.py`,
ansatz `1/(K{+}1) + a/n+b/n^2+c/n^3`) using the first three `K=2` data points
fails to predict the `n=6,7` values, meaning the true closed form (if
one exists in this simple a family at all) needs more terms/structure
than a 3-parameter fit from 3 points can recover — **not surprising**:
`n=6` for `K=2` already required distinguishing `|R\cap\{0,1\}|\in\{0,1,2\}`
*and*, within `|R\cap\{0,1\}|=0`, tracking whether the two reroute
sources land on the same or different `\pi`-cycles, and whether they
interact via reroute chains — genuinely the same order of combinatorial
complexity that made the *marginal* `K=2` fixed-`K` bridge require its
own dedicated front (`THEOREM.md` Estágio 3) rather than a direct
hand computation analogous to Proposition 4. **This document does not
attempt that full derivation** — it is out of scope for this front's
budget (see `PREREG.md`), and is named explicitly (§6) as the natural
next step for a dedicated future front, now that Proposition R shows
exactly what such a front's payoff would be.

### 4.2 Coarse large-`n` Monte Carlo (fresh, this session)

`second_moment_bridge_mc.py`, `n=2000`, `40{,}000` trials per `K`,
seeds `20260874100`–`20260874103` (reserved block, grep-confirmed
unused before first use):

| `K` | `\hat p` | s.e. | target `1/(K{+}1)` | `z`-score | `n(\hat p-\text{target})` |
|---|---|---|---|---|---|
| 2 | `0.33030` | `0.00235` | `0.33333` | `-1.29` | `-6.07` |
| 3 | `0.24940` | `0.00216` | `0.25000` | `-0.28` | `-1.20` |
| 4 | `0.20128` | `0.00200` | `0.20000` | `+0.64` | `+2.55` |
| 5 | `0.16445` | `0.00185` | `0.16667` | `-1.20` | `-4.43` |

All four `z`-scores are within `\pm1.3` of the target — **consistent
with**, but at this trial count nowhere near a precise confirmation of,
convergence to `1/(K{+}1)`. This is deliberately reported as a *coarse*
sanity check, not a rate-precision study: resolving the `\Theta(1/n)`
coefficient by Monte Carlo (as opposed to the exact closed form §3.2
obtained for `K=1`) would need the standard error on `\hat p` below
`\sim0.1/n`, i.e. of order `10^{-4}`–`10^{-5}` at `n=2000`, requiring
on the order of `10^7`–`10^9` trials — far beyond this front's budget,
and not attempted; the `n(\hat p-\text{target})` column is reported
for completeness but should not be over-read (its own standard error,
`n\times\text{s.e.}(\hat p)`, is `\sim4.5` here, comparable to the
values themselves).

### 4.3 Dedicated `K=1` large-`n` check of the transferred prediction

`k1_transfer_same_cycle_mc.py`, `n=2500`, `60{,}000` trials, seed
`20260874200`, measures all three quantities directly (not merely
`\text{both}`): `P(\text{both})`, `P(\text{same}\mid\text{both})`
(should be `1/2` **exactly** at every `n`, by Theorem J's Corollary —
this arm is a harness-correctness check, not new evidence), and
`P(\text{same and both})` (the actual new transferred prediction,
target `1/4`). See §7 for the numeric results.

---

## 5. What this document does NOT establish (stated precisely)

To avoid any risk of overclaiming:

- **The from-scratch continuum construction (route 1) is untouched.**
  Estágio 18 §3.3 and Estágio 25 §6.3's diagnosis — that Definition 3's
  `(\Theta_j,E_j)` primitives are a *marginal* abstraction discarding
  exactly the destination information a genuine simultaneous
  two-point (or `p`-point) exploration would need — stands exactly as
  written. This document supplies **no** two-point-capable extension of
  Definition 3, and does not claim to.
- **Nothing here says anything about the physical/geometric structure
  of where the split happens.** Theorem J's Corollary is a bare
  probability; it says *that* the split is 50/50, never *why* in
  spatial/exploration terms (e.g. which mark, at what position,
  "decides" same vs. different). A future genuine construction (route
  1) would presumably answer such questions; the transfer route here
  cannot, by design — it only ever manipulates a scalar identity.
- **The general-`K` bridge is a genuinely new open lemma, not a
  renamed version of Estágio 18's obstruction.** It is a scalar
  convergence question (`P_n^{(K)}(\text{both})\to1/(K{+}1)`) with
  finite, concrete combinatorial content, directly analogous in *kind*
  to a bridge THEOREM.md already closed (Estágio 3–6) for the first
  moment — not a "same problem, different name." Whether it turns out
  easy or hard in practice is untested beyond `K=1` here.
- **`\tau_K = 1/(K{+}1)` is not proved for `K\ge2`,** only conjectured
  (on the strength of Estágio 24's independent continuum-native proof
  of the target value, plus the `K=0,1` exact matches here, plus the
  numerics of §4). It is logically possible — though this document
  finds no evidence for it — that the finite-`n` second moment
  converges to something *other* than the continuum second moment for
  some `K\ge2`; ruling that out is exactly what a genuine closure of
  the bridge would need to do, the same way Estágio 3–6 had to *prove*
  (not merely observe) `\varphi_n^{(K)}\to\varphi_K` for the first
  moment.

---

## 6. What a future front would need (concrete, not vague)

To close the general-`K` second-moment bridge (and, via Proposition R,
obtain the full continuum-native Theorem J at every `K`, hence — after
a further, routine Poisson-mixing step exactly analogous to
`THEOREM.md` §5.2's "Consistency with Theorem 1" — the fully
unconditional-in-`c` same/different split `P(\text{same}) =
\frac{1-e^{-c}}{2c}`, mixing `1/(2(K{+}1))` over `K\sim\mathrm{Poisson}(c)`):

1. **Extend the case-split method of §3.2 to `K=2`.** The natural next
   step: classify `|R\cap\{0,1\}|\in\{0,1,2\}` (three cases, exactly as
   sketched in §4.1), and within `|R\cap\{0,1\}|=0`, further classify
   whether the two reroute sources land on the same or different
   background `\pi`-cycles, and whether the second reroute's target can
   land on the first reroute's *source* (a "chain," possible only for
   `K\ge2`, with no analogue in the `K=1` derivation here) — this is
   precisely the same case structure `THEOREM.md`'s own `k2_open_lemma`
   front had to build for the *marginal* `K=2` case; whether it can be
   reused or must be independently re-derived for the *joint* quantity
   is itself an open question this document does not resolve.
2. **Alternatively, generalize directly.** `THEOREM.md` Estágio 6 built
   a genuinely general-`K`, general-`r` machinery
   (`g_r(m,b)=F_r(t,b)+G_r(t,b)/n+O(1/n^2)`, an exact discrete-Gronwall
   argument) that closed the marginal bridge for *every* `K` at once,
   not `K`-by-`K`. Whether that specific machinery's `r`-indexed family
   already contains, or can be adapted to produce, the second-moment
   quantity `P_n^{(K)}(\text{both})` studied here is a concrete,
   well-posed question this document flags but does not attempt to
   answer (it would require reading and adapting a large body of
   existing machinery, `k2_open_lemma/k3_attempt_2/k6_attempt/
   k_general_existence_attempt/ATTEMPT.md`, out of scope for this
   front's budget).
3. **Separately, and independently of 1–2:** if a future front *does*
   want to attack the from-scratch continuum construction (route 1)
   itself, this document's §3.2 derivation may still be a useful guide
   to *what the correct finite answer looks like* (a concrete target
   to match), even though it supplies no continuum-side machinery
   toward building it.

---

## 7. Verification summary

| Check | Type | Result |
|---|---|---|
| `K=0` trivial identity, `P_n^{(0)}(\text{both})=1`, `n=2..5` | PROVED + exact brute force | 4/4 exact matches |
| `K=1` false-start (`V_a` alone) vs. brute force | self-caught error | mismatch at `n=3` (`5/9` vs. true `13/27`), caught before use |
| `V_a(n)=(3n{+}1)/(6n)` vs. brute force (R fixed, case a) | PROVED + exact brute force | `n=3..6`: 4/4 exact matches |
| `V_b(n)=(n{+}1)/(3n)` vs. brute force (R fixed, case b) | PROVED + exact brute force | `n=3..6`: 4/4 exact matches |
| Reassembled `P_n^{(1)}(\text{both})=(3n^2{-}n{+}2)/(6n^2)` vs. brute force (R averaged) | PROVED + exact brute force | `n=2..7`: 6/6 exact matches |
| Rate `n(P_n^{(1)}(\text{both})-1/2)\to-1/6` | PROVED (exact algebra on closed form) | exact |
| Proposition R (reduction) | PROVED (elementary, 3-line argument from (★)) | — |
| `K=0,1` transferred theorem `P(\text{same}\mid K)=1/(2(K{+}1))` | PROVED (by transfer, via Prop. R + closed forms) | `1/2, 1/4` |
| `K=2,3`: exact enumeration, `n` up to 7 | NUMERICALLY EXPLORED | consistent with, not proof of, `\to1/(K{+}1)` |
| `K=2,3,4,5`: large-`n` MC (`n=2000`, seeds `20260874100`–`103`) | NUMERICALLY EXPLORED | all `|z|<1.3` of target |
| `K=1` dedicated large-`n` triangulation (`n=2500`, seed `20260874200`) | NUMERICALLY EXPLORED | see below |

**`K=1` large-n MC result** (`k1_transfer_same_cycle_mc.py`,
`n=2500`, `60{,}000` trials, seed `20260874200`):

| Quantity | `\hat p` | s.e. | target | diff | `z` |
|---|---|---|---|---|---|
| `P(\text{both cyclic})` | `0.50172` | `0.00204` | `0.5` | `+0.00172` | `+0.84` |
| `P(\text{same}\mid\text{both})` (Theorem J Corollary — harness check, not new evidence) | `0.50204` | `0.00288` | `0.5` | `+0.00204` | `+0.71` |
| `P(\text{same and both})` (the new transferred prediction) | `0.25188` | `0.00177` | `0.25` | `+0.00188` | `+1.06` |

`n=2500`, `60{,}000` trials, seed `20260874200`, `75.5`s. All three
quantities land within `\sim1\sigma` of their predicted values,
including the `P(\text{same}\mid\text{both})\approx1/2` harness check
(confirming the same-cycle-labeling code is behaving as Theorem J's
already-proved exact identity requires) and — the actual new content —
`P(\text{same and both})\approx1/4`, independently triangulating
Proposition K1 + Proposition R's transferred prediction by a route
that does not reuse the exact closed form at all (a fresh simulation,
different code path, from primitives).

---

## 8. Scope, honesty, and scorecard

**PROVED in this document.** Proposition R (the reduction); the exact
`K=1` closed form `P_n^{(1)}(\text{both})=(3n^2{-}n{+}2)/(6n^2)` (both
sub-case formulas `V_a,V_b` and their reassembly); the `K=0,1`
transferred continuum theorem `P(x_1,x_2\text{ same final cycle in
}L(c)\mid K\text{ marks}) = 1/(2(K{+}1))`; the `\Theta(1/n)` exact rate
at `K=1` and the precise structural reason it differs from the
marginal case's `\Theta(1/n^2)` rate.

**NUMERICALLY EXPLORED, not proved.** Convergence of
`P_n^{(K)}(\text{both})\to1/(K{+}1)` for `K=2,3` (exact small-`n`
enumeration) and `K=2,3,4,5` (coarse large-`n` MC).

**NOT achieved, stated precisely.** The general-`K` second-moment
fixed-`K` bridge (§4, §6 names the concrete next steps). The
from-scratch continuum construction (route 1) — untouched, exactly as
diagnosed by Estágio 18/25 (§5 states precisely what remains
unaffected by this document).

| Item | Status |
|---|---|
| Proposition R (reduction: same/diff split limit `=\tau_K/2`) | **PROVED** |
| `K=0`: `P_n^{(0)}(\text{both})=1`, all `n`; `\tau_0=1` | **PROVED** (trivial) |
| `K=1`: exact closed form `(3n^2-n+2)/(6n^2)`; `\tau_1=1/2` | **PROVED** (new) |
| `K=1` rate: `\Theta(1/n)`, coefficient `-1/6` exactly | **PROVED** (new) |
| Continuum transfer: `P(\text{same}\mid K{=}0)=1/2` | **PROVED** (classical, degenerate case) |
| Continuum transfer: `P(\text{same}\mid K{=}1)=1/4` | **PROVED** (new, by transfer) |
| General-`K` second-moment bridge (`K\ge2`) | **OPEN** (new, narrower, precisely named) |
| From-scratch continuum construction (Estágio 18/25's obstruction) | **OPEN**, untouched, exactly as before |
| Exact enumeration `K=2` (`n=3..7`), `K=3` (`n=4..6`) | done, consistent with `\to1/(K{+}1)`, not proof |
| Large-`n` MC, `K=2..5` (`n=2000`) | NUMERICALLY EXPLORED, `|z|<1.3` all |
| `K=1` dedicated large-`n` triangulation | NUMERICALLY EXPLORED, see §7 |
| Self-caught false start (`V_a`-only, missing `O(1/n)` case) | caught before use in any claim; disclosed §3.2 |

**This document's net result: a genuinely new, unconditionally proved
piece of continuum-native content for Theorem J (the `K=0,1` transfer),
obtained via a new reduction that bypasses — without resolving — the
destination-information obstruction Estágio 18 and Estágio 25 both
correctly diagnosed as blocking any from-scratch construction; a
precise, narrower, and structurally different open lemma for `K\ge2`,
with concrete next steps named; and an explicit statement of exactly
what remains exactly as open as it was before this document.** No
Millennium Problem claim of any kind; pure internal combinatorics on
the archive's own random-permutation-with-reroutes ensemble.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `second_moment_bridge_exact.py` | none (exact deterministic enumeration) | n/a |
| `debug_k1_subcases.py` | none (exact deterministic enumeration) | n/a |
| `second_moment_bridge_mc.py` | `20260874100`, `20260874101`, `20260874102`, `20260874103` | reserved `20260874000`–`20260875000` |
| `k1_transfer_same_cycle_mc.py` | `20260874200` | reserved `20260874000`–`20260875000` |

Grep-confirmed before first use (see `PREREG.md`): the only prior
occurrences of `"20260874"` anywhere in the archive were the reservation
line in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` and this front's own
`PREREG.md`. No seed from the referee-reserved range `20260875000+`
was used. No git command was run.

## Files table

| File | Role |
|---|---|
| `PREREG.md` | pre-registration, written before any non-trivial code ran |
| `second_moment_bridge_exact.py` / `.log` | §3–4: exact brute-force enumeration for `K=0,1,2,3`; the corrected `K=1` closed form and its exact cross-check; the failed 3-parameter rational fit for `K=2` |
| `debug_k1_subcases.py` / `.log` | §3.2: isolates and validates the two `K=1` sub-case formulas `V_a,V_b` independently (with `R` fixed, not averaged), including the self-caught false-start comparison |
| `second_moment_bridge_mc.py` / `.log` / `_results.json` | §4.2: coarse large-`n` Monte Carlo, `K=2,3,4,5`, `n=2000`, seeds `20260874100`–`103` |
| `k1_transfer_same_cycle_mc.py` / `.log` / `_results.json` | §4.3/§7: dedicated `K=1` large-`n` triangulation of all three quantities (`both`, `same\|both`, `same and both`), seed `20260874200` |
| `ATTEMPT.md` | this document |
