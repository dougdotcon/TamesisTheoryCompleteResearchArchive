# THEOREM — the u12 limit law φ_∞(c): rigorous core and the n→∞ bridge

> **[Atualização 2026-08-22 — ver "Extensão, Estágio 4" ao final do
> documento]** O sumário original abaixo (fechado ao fim da Etapa 2)
> descreve os casos `K=2,3,4,5` como parte do Lema Aberto não-provado.
> Isso **não é mais exato**: o Estágio 3 (onda 5, `DISC-DEC-022`) prova
> o caso `K=2` incondicionalmente; o Estágio 4 (`DISC-DEC-031`) prova
> os casos `K=3,4,5` incondicionalmente por um método de matriz de
> transferência uniforme em `K`, ambos verificados por referee
> adversarial independente sem nenhum erro encontrado. O texto abaixo é
> preservado intacto como registro histórico da Etapa 2; o estado atual
> e correto do documento está nas seções de extensão ao final.

> **SUMÁRIO EXECUTIVO (documento inteiro, adicionado ao fechar a Etapa
> 2).** Este documento prova, de forma autocontida a partir de
> primitivas explicitamente declaradas, cerca de **dez afirmações
> centrais** — na Etapa 1 (§§3–5): Teorema 1 (forma fechada
> `φ_∞(c)=∫₀¹e^{-ct²}dt` em `L(c)`) com dois corolários (série, cauda
> com erro rigoroso), Lema 2 (média `φ_K` para todo `K`, mais a
> densidade completa exata em `K=1`), e uma identidade de
> consistência; na Etapa 2 (§7): Proposição 3 (redução exata,
> incondicional, da ponte `M_n(c)\to L(c)` a uma convergência
> caso-a-caso em `K`, via mistura Binomial→Poisson) e Proposição 4 +
> Corolário 4.3 (fórmula exata `φ_n^{(1)}=2/3+1/(3n^2)`, que **prova**
> — não apenas confirma numericamente — o padrão `a_1(n)=(n^2-1)/
> (3n^2)` que a verificação adversarial da onda 2 só tinha extrapolado
> de quatro pontos). Isso deixa **uma única PROPOSIÇÃO CONDICIONAL**:
> a ponte geral `φ(n,c)\to\varphi_\infty(c)` (Proposição Condicional
> 5, §7.5) depende de um Lema Aberto preciso — a mesma convergência
> caso-a-caso para `K\ge2` — que este documento tenta mas não
> consegue provar, e apenas sonda numericamente (enumeração exata até
> `n=8` em `K=2`, que mostra que a taxa `O(1/n^2)` provada em `K=1`
> **não** se estende obviamente a `K=2`). **Duas CONJECTURAS** ficam
> explicitamente separadas das provas (§8): a densidade
> condicional-`K` completa para `K\ge2`, e a lei distribucional
> incondicional `M(c)\overset d=\min(1,\sqrt{E/c})` — ambas apoiadas
> por testes KS e pela conexão com Hansen–Jaworski (EJC 2014), nenhuma
> provada aqui. Um punhado de fatos clássicos é **CITADO**, não
> re-derivado (Kingman 1975; Arratia–Barbour–Tavaré 2003; Le Cam 1960;
> Scheffé 1947). §9 lista **11 lacunas** remanescentes cobrindo o
> documento inteiro. Em suma: núcleo analítico da Etapa 1 sólido e
> completo; Etapa 2 fecha genuinamente uma fatia da ponte (a redução
> geral + os casos `K=0,1` com taxa exata) mas deixa o caso geral
> `K\ge2` — o coração do gap `n\to\infty` — honestamente em aberto.

**Scope of this document.** Front B of DISC-DEC-015, both stages, now
in one file. §§0–6 (Stage 1) prove what can be stated as a
self-contained probability computation **on the limit object `L(c)`
itself** (see `../limit_characterization/DERIVATION.md`,
`RESULTS_SUMMARY.md`, `adversarial/ADVERSARIAL_VERDICT.md` for the
originating result), with `L(c)` taken as given (constructed explicitly
from elementary primitives). §§7–9 (Stage 2, appended below, same
document) take up exactly what §§0–6 explicitly left open: whether, and
in what precise sense, the finite model `M_n(c)` converges to `L(c)` as
`n → ∞`. That bridge is **not** fully closed — §7 proves a genuine
reduction and two base cases, but the general case is left as a
precisely-stated open lemma (see the executive summary just below the
title for the honest scorecard). Every claim in this document is
labeled PROVED, CITED (a named classical fact used without
re-derivation), CONJECTURED, or — new in §7 — stated as a PROPOSIÇÃO
CONDICIONAL with its exact missing hypothesis named; nothing labeled
PROVED contains an unjustified step.

## Contents

0. Notation
1. The finite model `M_n(c)` (definition, for reference only)
2. The limit object `L(c)`: canonical description and explicit
   construction
3. Theorem 1 (`E[cyclic fraction in L(c)] = ∫₀¹ e^{-ct²} dt`) and proof
4. Corollaries: series, tail asymptotics, sanity checks
5. Lemma 2 (conditional-K law) and the Hansen–Jaworski connection
6. Status at the end of Stage 1
7. **[Stage 2]** The n→∞ bridge: precise statement, a proved reduction,
   two proved base cases, and the exact open lemma
8. **[Stage 2]** Conjectures (separated from proofs)
9. **[Stage 2]** Master list of every open gap in the whole document

**Reading guide (added first, for orientation).** §2 defines `L(c)` in
two layers: a canonical description (§2.1, "PD(1) + Poisson(c) marks",
matching the informal picture in DERIVATION.md) and an explicit
construction from independent primitives (§2.2) that is proved
equivalent *in the sense needed here* — Proposition 2.4 is the one
place in this document where a classical structural fact is CITED
rather than re-derived; everything downstream of it (all of §3–§5) is
self-contained given §2.2.

---

## 0. Notation

`[n] = {1,…,n}`. A *random mapping* is a function `f : [n] → [n]`
(not necessarily injective). The *functional digraph* of `f` has an
arc `i → f(i)` for every `i`. A point `i` is **cyclic** for `f` iff
`f^t(i) = i` for some integer `t ≥ 1`, equivalently iff `i` lies on a
directed cycle of the functional digraph. `Exp(1)` = exponential with
rate 1 (density `e^{-x}`, `x>0`); `Unif(0,1)` = uniform on `(0,1)`. All
random variables below live on one fixed, sufficiently rich probability
space `(Ω, ℱ, P)`; "independent" always means independent under `P`.
We write `PD(1)` for the Poisson–Dirichlet distribution with parameter
`(1,0)` (Kingman 1975, *Random discrete distributions*, JRSS B 37) and
`GEM(1)` for its size-biased-order (stick-breaking) representation.

---

## 1. The finite model `M_n(c)`

**Definition 1.** Fix `n ∈ ℕ` and `c ≥ 0`. Let `π` be a uniformly
random permutation of `[n]`. Independently, for each `i ∈ [n]` let
`ξ_i` be i.i.d. Bernoulli with `P(ξ_i=1) = c/n` (for `n > c`; take
`q=c/n ∧ 1` if one insists on `n ≤ c`, immaterial in the limit), and
let `U_i` be i.i.d. Uniform on `[n]`, independent of `π` and of the
`ξ`'s. Define the random mapping

`f(i) = U_i` if `ξ_i = 1`,  `f(i) = π(i)` if `ξ_i = 0`.

The observable is `φ(n,c) := E[ #{i : i cyclic for f} ] / n`. By
exchangeability of the construction in `i`, `φ(n,c) = P(1 \text{ is
cyclic for } f)`.

This is the object DERIVATION.md §0 studies; it is recorded here only
so that §2 below can be read as "the same ensemble, redescribed in the
`n=∞` scaling limit," and is not otherwise used in this document — no
`n → ∞` limit of `M_n(c)` is taken anywhere below. `L(c)` (§2) is
defined on its own terms.

---

## 2. The limit object `L(c)`

### 2.1 Canonical description

**Definition 2 (canonical form).** `L(c)` consists of: (i) a random
partition of the unit interval `[0,1]` (Lebesgue measure) into
countably many disjoint measurable "cycles," with the multiset of
their masses distributed as `PD(1)`; a marked point `x₀` is placed
uniformly on `[0,1]`, independently; and each block is further
equipped with a cyclic (rotational) order — the standard picture for
the `n→∞` limit of the cycle structure of a uniform random permutation
(Kingman 1975; the size-biased/stick-breaking `GEM(1)` representation
of the same object is due to McCloskey 1965 and Patil–Taillie 1977,
see also Pitman, *Combinatorial Stochastic Processes*, St-Flour 2002,
Springer LNM 1875, Ch. 3). (ii) Independently, a Poisson process of
rate `c` on `[0,1]` ("marks"/reroutes), each mark carrying an
independent `Unif(0,1)` destination. (iii) The resulting mapping: an
unmarked point moves to the next point on its cycle (in the cyclic
order); a marked point moves instead to its destination. A point is
**cyclic** iff its forward orbit under this mapping returns to itself
in finitely many steps.

This is a faithful `n→∞` redescription of `M_n(c)` (§1): `π` becomes
the `PD(1)` cycle partition, `ξ_i=1`-then-`U_i` becomes a Poisson(c)
mark with uniform destination. We do **not** prove this correspondence
in this document (that is a convergence statement about `M_n(c)`,
deferred to Stage 2); §2.1 only fixes *what object is being computed
on*.

### 2.2 Working construction (explicit primitives)

Definition 2 is not, by itself, amenable to direct computation without
importing a substantial amount of exchangeable-partition machinery. We
instead give an **explicit construction** of the random variables that
determine whether `x₀` is cyclic, built from elementary independent
primitives, and relate it to Definition 2 in §2.3–2.4.

**Definition 3 (explicit `L(c)`, restricted to `x₀`'s fate).** On a
common probability space, let:

- `E₀, E₁, E₂, … ` be i.i.d. `Exp(1)`;
- `𝒩` a Poisson process of rate `c` on `[0,1)`, independent of the
  `E_j`'s; write `K := 𝒩([0,1))` (a.s. finite, `K ~ Poisson(c)`) and
  `S₁ < S₂ < ⋯ < S_K` for its points (a.s. distinct);
- `Θ₁, …, Θ_K` i.i.d. `Unif(0,1)`, independent of everything above
  (one per point of `𝒩`, in order).

Define `T₀ := 1 - e^{-E₀}`. Process `j = 1, …, K` in increasing order
of `S_j`, maintaining a finite set `𝒜 ⊆ {0,1,…,K}` of *open arc-heads*
with associated *closure times* `(T_i)_{i∈𝒜}` (initialize `𝒜 = {0}`):

- if `S_j ≥ min_{i∈𝒜} T_i`: **stop** the loop (all later `j' > j` are
  also skipped, since `S_{j'} > S_j`);
- else if `Θ_j < S_j`: declare a **kill** at time `S_j` and **stop**;
- else (`Θ_j ≥ S_j`): set `T_j := S_j + (1-S_j)(1 - e^{-E_j})`, and
  update `𝒜 ← 𝒜 ∪ {j}`; continue.

If the loop exits via a kill: **`x₀` is not cyclic.** Otherwise (loop
exhausts `j=1,…,K` without a kill): let `T^* := \min_{i \in 𝒜} T_i`
and let `i^*` be the (a.s. unique) minimizer; **`x₀` is cyclic iff
`i^* = 0`.**

This is a well-defined, terminating, deterministic function of the
(a.s. finite, since `K<∞` a.s.) list of primitives — no circularity: at
each stage the loop only queries `S_j` (known, sorted in advance) and
the finitely many already-computed `T_i` for `i` already in `𝒜`, and
`𝒜` only grows by indices in increasing `S_j`-order, so `min_{i∈𝒜}T_i`
is always available before it's needed. We take Definition 3, together
with `P(x₀ \text{ cyclic}) =: φ_∞(c)`, as the **operational meaning**
of "the fraction of cyclic points in `L(c)`, evaluated at a uniform
point," for the rest of this document.

### 2.3 Why Definition 3 is the right object

The recipe of §2.2 is exactly a formalization of DERIVATION.md §1–§2's
exploration process, with the (informally argued there) hazard "closure
rate `1/(1-s)` per open arc-head, born at `s`" now built in *by
construction*: an arc-head born at time `s` gets closure time
`s + (1-s)(1-e^{-E})` with `E~Exp(1)` fresh and independent, which
satisfies, for `u ≥ s`: `T>u \iff (1-s)(1-e^{-E})>u-s \iff e^{-E} <
\frac{1-u}{1-s}`, and since `e^{-E}\sim\mathrm{Unif}(0,1)` (immediate
from `E\sim\mathrm{Exp}(1)`: `P(e^{-E}\le z)=P(E\ge-\log z)=z` for
`z\in(0,1)`), this has probability `\frac{1-u}{1-s}` directly —

`P(T>u) = \dfrac{1-u}{1-s}` for `u∈[s,1)`, the survival function of
exactly the hazard-`1/(1-r)dr` clock DERIVATION.md posits. Two
sanity/consistency checks that this construction is not an ad-hoc
device but the standard object:

**Fact A (elementary, PROVED).** `T₀ = 1-e^{-E₀} ~ Unif(0,1)` — for
`y\in(0,1)`, `T_0\le y \iff e^{-E_0}\ge1-y \iff E_0\le-\log(1-y)`, and
since `E_0\sim\mathrm{Exp}(1)` gives `P(E_0\le a)=1-e^{-a}`,
`P(T_0\le y) = 1-e^{-(-\log(1-y))} = 1-e^{\log(1-y)} = 1-(1-y) = y`.
This matches the classical fact recorded (as a `c=0` sanity
check, without proof) in DERIVATION.md §2: *the length of the cycle
containing a uniformly chosen point of a uniform random permutation
(equivalently: a size-biased pick from `PD(1)`) is `Unif(0,1)` in the
`n→∞` limit* — a standard consequence of the `GEM(1)` stick-breaking
representation, where the size-biased first pick has length `V₁`, `V₁`
itself `Unif(0,1)` by definition of stick-breaking (McCloskey 1965;
Patil–Taillie 1977; Pitman 2002 St-Flour notes, Ch. 3, Prop. 3.1).
Definition 3 reproduces this marginal exactly, with no free parameter
to tune — this is the `K=0` (no marks encountered) case of Theorem 1
below and is the first, elementary check that Definition 3 is not
mis-calibrated.

**Proposition 2.4 (multi-arc-head independence; CITED, not
re-derived here).** For `K ≥ 1` open arc-heads born at times
`0 = s_0 < s_1 < ⋯`, the joint construction of §2.2 — mutually
independent closure clocks `T_i`, each with survival function
`(1-u)/(1-s_i)` for `u ≥ s_i`, and the arc-start actually closed at
the first closure time chosen (implicitly, via which `T_i` is
smallest) — is the standard representation of "sequentially explore a
`PD(1)`/`GEM(1)`-distributed cycle partition from several
simultaneously active starting points, with the exploration order
determined by a uniform, `n→∞`-scaled 'lazy revelation' of the
partition." This is the continuum ("Feller coupling" / Chinese
Restaurant Process) representation of `PD(1)`; see Kingman (1975) and
Arratia–Barbour–Tavaré, *Logarithmic Combinatorial Structures: a
Probabilistic Approach*, EMS 2003, Chs. 4–5, especially the "Feller
coupling" (Ch. 4) and the exchangeability/size-biased-sampling
machinery for `GEM(θ)` (Ch. 4–5) — and, restricted to the finite-`n`
level, is exactly the elementary fact that a uniform random bijection
of a finite set can be built by revealing images one at a time, each
new image uniform over not-yet-used targets (a one-line induction on
exchangeability, which is precisely DERIVATION.md §1's "π is revealed
lazily" device). We use Proposition 2.4 as the single classical,
externally-justified structural input to this document; every other
step from here on is a self-contained computation from Definition 3.

*(Honesty note: Proposition 2.4 is standard and low-risk — it is the
textbook representation of `PD(1)`/`GEM(1)`, not a contested or novel
claim — but it is a citation, not a derivation performed in this
document. This is flagged again in §6.)*

**What is and is not at stake here.** The mutual independence of the
`E_j` (hence of the `T_i`, given their birth times) inside Definition
3 is **not** something that needs proving — it holds *by construction*,
since the `E_j` are declared i.i.d. `Exp(1)` from the outset. What
Proposition 2.4 supplies is purely *interpretive*: it says this
particular explicit recipe (independent hazard-`1/(1-s)` clocks,
raced against an independent Poisson(c) mark process) is the standard
way the object of Definition 2 behaves under exploration, so that
`φ_∞(c)` computed from Definition 3 answers the question Definition 2
poses. Every computation in §3–§5 uses only Definition 3's primitives
and is fully self-contained; Proposition 2.4 is not invoked again.

### 2.4 From `P(x₀ cyclic)` to `E[cyclic fraction]`

**Remark (delicate step, justified).** The observable of interest is
`E[\text{Lebesgue measure of the cyclic set}]`, while Definition 3
computes `P(x₀ \text{ cyclic})` for the single point `x₀` fixed at
construction. These coincide by Fubini–Tonelli (integrand
`1\{x \text{ cyclic}\} ≥ 0` is jointly measurable in `(x,ω)` — it is
determined, for each fixed realization of the mark process and cycle
partition, by a finite exploration algorithm identical in form to
Definition 3 run from `x` instead of `x₀`, hence Borel-measurable):

`E[\text{Leb}(\text{cyclic set})] = E\Big[\int_0^1 1\{x \text{ cyclic}\}\,dx\Big] = \int_0^1 P(x \text{ cyclic})\, dx = P(x_0 \text{ cyclic})`,

the last equality because `x₀` was constructed as an *independent
uniform point*, so `P(x_0\text{ cyclic}) = \int_0^1 P(x\text{ cyclic})\,dx`
by definition of "uniform," and by the exchangeability of the
construction (nothing in Definition 3 privileges `x₀` over any other
point of `[0,1]`) `P(x\text{ cyclic})` does not depend on `x`. Hence
`φ_∞(c) := P(x_0\text{ cyclic})` computed in §3 *is* `E[\text{cyclic
fraction}]`, matching DERIVATION.md §0's reduction "by exchangeability."

---

## 3. Theorem 1

> **Theorem 1.** For every `c ≥ 0`, under Definition 3,
> `φ_∞(c) = P(x_0 \text{ cyclic}) = \displaystyle\int_0^1 e^{-ct^2}\,dt
> = \frac{1}{2}\sqrt{\frac{\pi}{c}}\,\mathrm{erf}(\sqrt c)` (the value
> `1` at `c=0`, by continuity / direct check).

### Proof

**Step 1 — the marginal law of `T₀`.** By Fact A (§2.3),
`T₀ ~ Unif(0,1)`, independent of `(𝒩, Θ_1,\dots,\Theta_K, E_1, E_2,
\dots)` (it is a function of `E₀` alone, and `E₀` is independent of
all the other primitives by construction). Hence

`φ_∞(c) = E\big[P(x_0\text{ cyclic} \mid T_0)\big] = \int_0^1 P(x_0\text{ cyclic}\mid T_0=t)\, dt`.  (3.1)

This is an unconditional-from-conditional expectation over a bounded
`[0,1]`-valued integrand (a probability), so no dominated-convergence
issue arises in this step.

**Step 2 — the event `{x₀ cyclic}` in terms of marks before `t`.**
Fix `T_0 = t`. Unwinding Definition 3's loop with `𝒜 = \{0\}` frozen
at `T_0=t` for the moment: the loop, run on the marks in increasing
order of `S_j`, reaches a mark `j` with `S_j ≥ t` only if no closure
(kill, or some `T_i < t` for `i` already in `𝒜`) has occurred yet — but
if no closure has occurred by `S_j ≥ t`, then in particular `T_0 = t ≤
S_j` has already been reached without incident, and by definition of
the loop's stopping rule the process **stops at `S_j`** without ever
resolving `j`; the outcome by then is already `\{i^* = 0\}` (`x₀`
cyclic) provided every mark `j'` with `S_{j'} < t` was neither a kill
nor produced a `T_{j'} < t`. Marks with `S_j ≥ t` are therefore
irrelevant to the event `\{x_0\text{ cyclic}\}` given `T_0=t`, and

`\{x_0\text{ cyclic}\} \cap \{T_0=t\} = \{T_0=t\} \cap \bigcap_{j:\,S_j<t} \big(\{\Theta_j \ge S_j\} \cap \{T_j > t\}\big)`.  (3.2)

(Read: no mark before `t` kills, and no mark before `t` that survives
produces a sibling arc-head that closes before `t`. Marks after `t` are
never reached, because `x₀`'s own clock has already fired first, ending
the exploration.)

**Step 3 — restriction of `𝒩` to `[0,t)` (standard Poisson fact,
stated for completeness).** By the independent-increments /
restriction property of a Poisson process (Kingman, *Poisson
Processes*, OUP 1993, Ch. 2–3 — a Poisson process of rate `c` on
`[0,1)` restricted to a sub-interval `[0,t)` is itself a Poisson
process of rate `c` on `[0,t)`, and is independent of the process
restricted to `[t,1)`), the marks `\{S_j : S_j<t\}`, together with
their `\Theta_j`'s and `E_j`'s (which were declared independent of
`𝒩` and of each other in the first place), form: a Poisson process
`𝒩_t` of rate `c` on `[0,t)`, marked independently at each point `s`
by an independent pair `(\Theta,E) \sim \mathrm{Unif}(0,1)\otimes
\mathrm{Exp}(1)`. This is independent of `T_0=t` (which depends only on
`E_0`).

**Step 4 — the per-mark success probability, exactly (the nuclear
computation).** For a single mark at position `s < t` with its own
independent `(\Theta,E)`, define "success" as the event inside the
intersection in (3.2): `\{\Theta \ge s\} \cap \{T > t\}` where
`T = s + (1-s)(1-e^{-E})` (only defined/relevant on `\{\Theta \ge s\}`,
i.e. the mark survives; on `\{\Theta<s\}` it is a kill, hence
automatically *not* a success). Compute:

`P(\Theta \ge s) = 1-s`.

Given `\Theta \ge s` (independent of `E`), `T>t \iff s+(1-s)(1-e^{-E})>t
\iff (1-s)e^{-E} < 1-t \iff e^{-E} < \frac{1-t}{1-s} \iff E >
\log\frac{1-s}{1-t}` (the log is well-defined and `>0` since `s<t`
gives `1-s>1-t>0`, and `\frac{1-t}{1-s} \in (0,1)`). Since `E\sim
\mathrm{Exp}(1)`,

`P\Big(E > \log\frac{1-s}{1-t}\Big) = \exp\Big(-\log\frac{1-s}{1-t}\Big) = \frac{1-t}{1-s}`.

`\Theta` and `E` are independent, so

`P(\text{success at } s) = P(\Theta\ge s)\cdot P(T>t \mid \Theta \ge s) = (1-s)\cdot\frac{1-t}{1-s} = \boxed{1-t}`  (3.3)

— **independent of `s`.** This is the exact cancellation DERIVATION.md
§3 calls "the entire reason a closed form exists," now derived by
direct computation on two independent elementary random variables
(one survival-probability factor `1-s`, one competing-exponential-tail
factor `(1-t)/(1-s)`) rather than asserted: the "sibling arc-head's own
extra survival requirement `T>t`" is not a separate correction bolted
onto the "does not kill" probability — it *is* computed jointly, and
the `1/(1-s)` growth of the second factor exactly cancels the `(1-s)`
decay of the first, for every `s`.

**Step 5 — assembling via Poisson thinning (PGFL).** By Step 3, the
marks in `[0,t)` form a Poisson(c) process on `[0,t)`; by Step 4, each
mark independently "fails" (kill, or survives but produces `T\le t`)
with probability `1-(1-t)=t`, *independently of its position `s`* and
independently across marks (the `(\Theta_j,E_j)` are i.i.d. across
`j`, independent of `𝒩_t`). By the marking/thinning theorem for
Poisson processes (a mark-dependent independent thinning of a
Poisson(`c`) process on an interval of length `t`, with constant
keep/discard probability, yields a Poisson process for each class,
with rate `c·(\text{prob})` on that interval — Kingman 1993, Ch. 5),
the number of "failing" marks in `[0,t)` is `\mathrm{Poisson}(c\cdot t
\cdot t) = \mathrm{Poisson}(ct^2)`. Hence, by (3.2) (which requires
*zero* failing marks in `[0,t)`),

`P(x_0\text{ cyclic}\mid T_0=t) = P(\mathrm{Poisson}(ct^2)=0) = e^{-ct^2}`.  (3.4)

**Step 6 — conclusion.** Substituting (3.4) into (3.1),

`φ_∞(c) = \int_0^1 e^{-ct^2}\,dt`.

The closed form `\frac12\sqrt{\pi/c}\,\mathrm{erf}(\sqrt c)` follows by
the substitution `u=\sqrt c\, t` (`c>0`): `\int_0^1 e^{-ct^2}dt =
\frac{1}{\sqrt c}\int_0^{\sqrt c} e^{-u^2}\,du = \frac{1}{\sqrt c}\cdot
\frac{\sqrt\pi}{2}\,\mathrm{erf}(\sqrt c)`, using the definition
`\mathrm{erf}(z) = \frac{2}{\sqrt\pi}\int_0^z e^{-u^2}du`. `∎`

### 3.1 The size-biasing pitfall, made explicit

The task of this document singles out one failure mode: a
verification pass (`../limit_characterization/adversarial/
ADVERSARIAL_NOTE.md`, item (c).2) notes that a *heuristic* tail
computation which forgets to size-bias the "currently-traversed arc"
lands on `\sqrt{\pi/2}\,c^{-1/2}` instead of the correct
`(\sqrt\pi/2)\,c^{-1/2}` — off by a factor `\sqrt2`. Two things are
worth making explicit about why the proof above does not fall into
any version of this trap.

**(a) Where an analogous error would enter this proof, and why it
doesn't.** Step 4 computes `P(\text{success at } s) = (1-s)\cdot
\frac{1-t}{1-s}`. A tempting shortcut is to compute only the "does not
kill" factor `(1-s)` and forget the "and the resulting sibling
arc-head doesn't itself close before `t`" factor `\frac{1-t}{1-s}` —
i.e. to treat only event (B) of DERIVATION.md §1 (jump lands on
visited territory) as a failure mode and to overlook that event (A)
(π-closure) can also be triggered by a *sibling* arc-head, not only by
`x₀`'s own clock. Carrying out Steps 5–6 with the truncated
probability `1-s` in place of `1-t` in (3.3) — i.e. thinning by
"fail-probability `s`" instead of "fail-probability `t`, constant in
`s`" — gives failing-mark count `\mathrm{Poisson}\big(c\int_0^t s\,
ds\big) = \mathrm{Poisson}(ct^2/2)`, hence a *wrong* closed form
`\int_0^1 e^{-ct^2/2}dt` (tail `\sqrt{\pi/2}\,c^{-1/2}` — **exactly**
the erroneous coefficient flagged by the adversarial check, reached
here by an independent route). The correct computation is protected
against this specific slip because (3.3) is a joint computation over
the *pair* `(\Theta,E)`, not a probability assigned to `\Theta` alone
— dropping the `E`-dependent factor is visible as dropping a whole
random variable from the model, not as a subtle averaging error.

**(b) The specific "visited-arc size-biasing" trap named in the
adversarial note.** That note's own tail heuristic is a *different*,
non-rigorous shortcut: it treats the gaps between marks as i.i.d.
`Exp(c)` (correct, as a marginal statement about *unconditional*
inter-mark spacings) and then asks for "the length of the arc
currently being traversed at a giv­en moment," implicitly invoking the
inspection/waiting-time paradox — the arc *containing* a uniformly
chosen reference time is length-biased, with mean `2/c` (a
`\mathrm{Gamma}(2,c)`), not the unconditional mean `1/c` of a single
`\mathrm{Exp}(c)` gap. Using the length-biased mean `2/c` where the
correct one is `1/c` inflates a quantity that enters the tail
computation as a square root, producing exactly the observed `\sqrt2`
discrepancy. **The proof above never forms or needs "the length of
the arc currently being traversed."** Step 3–5 work directly with the
Poisson(c) mark process restricted to the *fixed* interval `[0,t)` —
an interval defined by `x₀`'s own clock `T_0=t`, not by "where the
walker happens to be" — and Step 4 computes an exact per-mark
probability, not a mean arc length. There is no inspection/size-biased
quantity anywhere in the chain (3.1)–(3.4); the pitfall is avoided not
by a correction applied after the fact, but because the exact
computation never introduces the object (a "typical traversed arc")
that would need correcting in the first place. (§4.2 re-derives the
tail asymptotics directly from the *proved* closed form by calculus,
sidestepping this heuristic route entirely — see the remark there.)

---

## 4. Corollaries of Theorem 1

### 4.1 The series (entire function)

**Corollary 4.1.** `φ_∞(c) = \sum_{k\ge0} \dfrac{(-c)^k}{k!\,(2k+1)}`
for every real `c` (infinite radius of convergence; for `c\ge0` it
equals the integral of Theorem 1).

*Proof.* Fix `c`. The power series `e^{-ct^2} = \sum_{k\ge0}
\frac{(-c)^k t^{2k}}{k!}` converges for every `t`, and on the compact
set `t\in[0,1]` it converges *uniformly*: `\left|\frac{(-c)^kt^{2k}}
{k!}\right| \le \frac{|c|^k}{k!} =: M_k` with `\sum_k M_k = e^{|c|} <
\infty`, so the Weierstrass `M`-test applies. This is the delicate
step (interchanging `\int_0^1` and `\sum_k`), justified precisely by
this bound, not merely asserted:

`\int_0^1 e^{-ct^2}\,dt = \sum_{k\ge0}\frac{(-c)^k}{k!}\int_0^1 t^{2k}\,dt = \sum_{k\ge0}\frac{(-c)^k}{k!(2k+1)}`. `∎`

First terms: `1 - c/3 + c^2/10 - c^3/42 + c^4/216 - \dots`, matching
DERIVATION.md (4.2). In particular `a_1 = 1/3` (coefficient of `-c`),
the quantity used in `../limit_characterization/adversarial/` to
discriminate against the archive's refuted `(1+c)^{-1/2}` form (which
would give `a_1=1/2`).

### 4.2 Tail asymptotics, with a rigorous error bound

**Corollary 4.2.** As `c\to\infty`,
`\varphi_\infty(c) = \frac{\sqrt\pi}{2}\,c^{-1/2} - R(c)`,
where `0 < R(c) < \dfrac{e^{-c}}{2c}` for all `c>0`. In particular
`\varphi_\infty(c) = \frac{\sqrt\pi}{2}c^{-1/2}\big(1+O(e^{-c})\big)` —
a *pure* power-law tail up to exponentially small corrections.

*Proof.* By Theorem 1's closed form, `\varphi_\infty(c) = \frac1{\sqrt
c}\int_0^{\sqrt c}e^{-u^2}du = \frac{\sqrt\pi}{2\sqrt c} -
\frac1{\sqrt c}\int_{\sqrt c}^\infty e^{-u^2}\,du`. Set `R(c) :=
\frac1{\sqrt c}\int_{\sqrt c}^\infty e^{-u^2}du`. For `z>0`, one
integration by parts gives `\int_z^\infty e^{-u^2}du =
\left[-\frac{e^{-u^2}}{2u}\right]_z^\infty - \int_z^\infty
\frac{e^{-u^2}}{2u^2}\,du = \frac{e^{-z^2}}{2z} - \int_z^\infty
\frac{e^{-u^2}}{2u^2}\,du`, and since the subtracted integral is
strictly positive, `0 < \int_z^\infty e^{-u^2}du <
\frac{e^{-z^2}}{2z}`. With `z=\sqrt c`: `0 < R(c) < \frac1{\sqrt
c}\cdot\frac{e^{-c}}{2\sqrt c} = \frac{e^{-c}}{2c}`. `∎`

(The full expansion `R(c) = e^{-c}[\frac1{2c} - \frac1{4c^2} +
\frac3{8c^3} - \cdots]` of DERIVATION.md (4.3) follows by iterating
the same integration by parts, each remainder again sign-definite and
smaller than the last retained term — the standard control for this
kind of asymptotic series. Not re-derived term by term here, since
Corollary 4.2's leading order and rigorous error bound are all that is
used below.)

**Remark.** This tail derivation uses only elementary calculus on the
*already-proved* closed form — it never mentions "arcs" and so cannot
inherit the size-biasing pitfall of §3.1(b) (which is specific to a
probabilistic shortcut that bypasses the closed form). This is the
cleanest illustration that, once Theorem 1 is proved, the tail
asymptotics are a triviality.

### 4.3 Sanity check: `c=0`

`\varphi_\infty(0) = \int_0^1 1\,dt = 1`: with no reroutes, `M_n(0)` is
a uniform permutation and every point is cyclic, `\varphi(n,0)\equiv1`
for all `n`. Trivially consistent.

---

## 5. Lemma 2: the law conditional on `K` surviving reroutes

### 5.1 Setup

Condition on exactly `K` marks total (rather than `\mathrm{Poisson}(c)`
many). Formally: replace `𝒩` in Definition 3 by exactly `K` i.i.d.
`\mathrm{Unif}(0,1)` positions `S_1,\dots,S_K` (a standard fact —
conditioning a rate-`c` Poisson process on `[0,1)` on its total count
`K` yields exactly `K` i.i.d. uniform points, e.g. Kingman 1993 Ch. 2
— though here we simply *impose* `K` uniform marks directly as the
definition of the conditional model, so no conditioning argument is
even needed); keep `\Theta_1,\dots,\Theta_K` i.i.d. `\mathrm{Unif}(0,1)`
and `E_0,E_1,\dots,E_K` i.i.d. `\mathrm{Exp}(1)` as before, all mutually
independent. Run the same algorithm. Write `\varphi_K := P(x_0
\text{ cyclic})` under this model.

### 5.2 The mean (Wallis integral)

> **Lemma 2 (mean).** `\varphi_K = \displaystyle\int_0^1 (1-t^2)^K\,dt
> = \dfrac{4^K (K!)^2}{(2K+1)!}`.

*Proof.* As in Theorem 1, `\varphi_K = \int_0^1 P(x_0\text{
cyclic}\mid T_0=t)\,dt` (Step 1 is unchanged — `T_0` is still `1-e^{-E_0}`,
independent of the rest). Fix `T_0=t`. Now *every* mark matters (not
just those with `S_j<t`, since we no longer discard the Poisson
process outside `[0,t)` — there are only `K` marks total, each at an
independent uniform position on the *whole* `[0,1)`), but a mark with
`S_j\ge t` is automatically harmless (§3, Step 2's argument: such a
mark is never reached by the exploration once `T_0=t` has already
fired, since — as in Theorem 1 — the process only lets marks matter if
they occur before the eventual closure time, and here that closure
time is exactly `t` when `x_0` is cyclic). For a single mark at
position `S \sim \mathrm{Unif}(0,1)`, condition on `S`:

- if `S \ge t` (probability `1-t`): automatically "success" (does not
  affect `x_0`'s fate before `t`);
- if `S < t` (probability `t`): "success" with (conditional)
  probability `1-t`, computed exactly as in Theorem 1 Step 4 (that
  computation used only `s<t`, not that `s` came from a rate-`c`
  Poisson process — it is a statement about one mark at position `s`,
  which is exactly the situation here).

So `P(\text{one mark is a success}) = (1-t)\cdot 1 + t\cdot(1-t) =
(1-t)(1+t) = 1-t^2`. The `K` marks are i.i.d., so

`P(x_0\text{ cyclic}\mid T_0=t) = (1-t^2)^K`,

and `\varphi_K = \int_0^1(1-t^2)^K\,dt`. For the closed form, substitute
`t=\sin\theta`: `\int_0^1(1-t^2)^K dt = \int_0^{\pi/2}\cos^{2K+1}\theta
\,d\theta = \frac{(2K)!!}{(2K+1)!!} = \frac{4^K(K!)^2}{(2K+1)!}`, the
last equality by `\ (2K)!! = 2^K K!` and `\ (2K+1)!! =
\frac{(2K+1)!}{2^K K!}`, both elementary identities on double
factorials. `∎`

Checks: `K=0`: `\varphi_0=1`. `K=1`: `\varphi_1 = 4/6=2/3`. `K=2`:
`\varphi_2 = 16\cdot4/120 = 8/15`. `K=3`: `64\cdot36/5040=16/35`. All
match DERIVATION.md §4.3 and were confirmed against Poisson-mixture
consistency with Theorem 1's series in the wave-2 numerics.

**Consistency with Theorem 1.** Mixing `\varphi_K` over
`K\sim\mathrm{Poisson}(c)` must reproduce `\varphi_\infty(c)`:
`e^{-c}\sum_K \frac{c^K}{K!}\varphi_K = e^{-c}\sum_K\frac{c^K}{K!}
\int_0^1(1-t^2)^K dt = \int_0^1 e^{-c}e^{c(1-t^2)}dt = \int_0^1
e^{-ct^2}dt`, matching Theorem 1 exactly (interchange of `\sum_K` and
`\int_0^1` justified as in §4.1, now with the uniform bound
`\frac{c^K}{K!}|1-t^2|^K \le \frac{c^K}{K!}` on `[0,1]`, again summing
to `e^c<\infty`). This is not an independent check of Lemma 2 (it was
derived from the same construction) but confirms internal consistency
of the two derivations.

### 5.3 The `K=1` density (proved)

> **Lemma 2 (density, `K=1`).** The cyclic-mass random variable
> `M_1 := \text{Leb}(\text{cyclic set})` under the `K=1` model of §5.1
> has density `f_{M_1}(x) = 2x` on `(0,1)` (i.e. `2Kx(1-x^2)^{K-1}` at
> `K=1`).

*Proof.* With `K=1`, the *whole cyclic set* (not just `P(x_0\text{
cyclic})`) can be computed directly, because with a single reroute the
background cycle structure is disturbed in only one place.
DERIVATION.md §5 already isolates the relevant random variables: let
`L\sim\mathrm{Unif}(0,1)` be the (size-biased, `\mathrm{PD}(1)`-typical)
length of the cycle struck by the reroute, and `u\sim\mathrm{Unif}(0,1)`
its destination, independent of `L`. Then (DERIVATION.md §5, verified
directly by inspection of the two cases): if `u` misses the struck
cycle (probability `1-L`), the cyclic mass is `M_1 = 1-L` exactly
(deterministic given `L`); if `u` lands inside the struck cycle
(probability `L`), the cyclic mass is `M_1 = 1-L+D` with `D\mid(L,u\in
C)\sim\mathrm{Unif}(0,L)` (the forward distance from `u` back to the
reroute point).

We compute the density of `M_1` by summing the two branches'
contributions, each obtained by the standard change-of-variables
formula for a mixture. **Branch 1** (`u\notin C`, weight `1-L`,
`M_1=1-L` deterministic given `L`): for `x\in(0,1)`, this branch's
contribution to `f_{M_1}` at `x` is `f_L(1-x)\cdot P(u\notin C\mid
L=1-x) \cdot \left|\frac{d(1-L)}{dL}\right|^{-1}\Big|_{L=1-x}` — with
`f_L\equiv1` on `(0,1)` and the Jacobian factor `=1` (the map
`L\mapsto1-L` has derivative `-1`), this is `1\cdot x\cdot 1 = x`.
**Branch 2** (`u\in C`, weight `L`, `M_1=1-L+D`, `D\mid L\sim
\mathrm{Unif}(0,L)`): given `L=\ell`, `M_1` is `\mathrm{Unif}(1-\ell,1)`
(density `1/\ell` on that interval); the contribution to `f_{M_1}(x)`
is `\int_0^1 P(u\in C\mid L=\ell)\cdot f_L(\ell)\cdot
\underbrace{\frac1\ell \mathbf 1\{x\in(1-\ell,1)\}}_{\text{density of
}M_1\text{ given }L=\ell}\, d\ell = \int_0^1 \ell\cdot1\cdot
\frac1\ell\mathbf1\{\ell>1-x\}\,d\ell = \int_{1-x}^1 1\,d\ell = x`.

Summing the two branches: `f_{M_1}(x) = x+x = 2x` on `(0,1)`. `∎`

(Sanity check: `\int_0^1 2x\,dx=1` ✓, and `\int_0^1 x\cdot2x\,dx =
2/3 = \varphi_1` ✓, matching Lemma 2's mean above.)

### 5.4 The general-`K` density: CONJECTURE, not proved here

`2Kx(1-x^2)^{K-1}` reduces to `2x` at `K=1` (§5.3) and its mean matches
Lemma 2 exactly:

**Mean-consistency check (PROVED, but only a consistency check — see
below for what this does and does not establish).**
`\int_0^1 x\cdot 2Kx(1-x^2)^{K-1}\,dx = \varphi_K`. *Proof:*
`\frac{d}{dx}\big[x(1-x^2)^K\big] = (1-x^2)^K -2Kx^2(1-x^2)^{K-1}`;
integrating both sides over `[0,1]`, the left side is
`\big[x(1-x^2)^K\big]_0^1=0`, so `2K\int_0^1x^2(1-x^2)^{K-1}dx =
\int_0^1(1-x^2)^K dx = \varphi_K`, i.e. `\int_0^1 x\cdot
2Kx(1-x^2)^{K-1}dx = \varphi_K`. `∎`

**What is genuinely open.** §5.2–5.3 compute, respectively, (i) `P(x_0
\text{ cyclic})` for general `K` (a single-point exploration, handled
by Theorem 1's machinery verbatim) and (ii) the *full distribution* of
the cyclic mass `M_1` for `K=1` (a whole-space computation, tractable
because a single reroute disturbs only one background cycle). For
`K\ge2`, the full law of `M_K := \text{Leb}(\text{cyclic set})` is a
genuinely harder whole-space question: the `K` reroutes can strike the
same background cycle, strike different cycles whose broken pieces
then interact through further reroutes, etc. — a combinatorial
case-analysis growing with `K`, not addressed by the single-point
exploration technique used everywhere else in this document.
Accordingly:

> **We do NOT claim to prove `f_{M_K}(x) = 2Kx(1-x^2)^{K-1}` for
> `K\ge2` in this document.** It is recorded as a **CONJECTURE**,
> exactly as classified in `../limit_characterization/RESULTS_SUMMARY.md`
> ("categoria b"), consistent with — and strengthened by, not resolved
> by — three independent sources: (a) the mean-consistency check just
> given; (b) the Kolmogorov–Smirnov tests against this density for
> `K=1,2,3` reported in `../limit_characterization/RESULTS_SUMMARY.md`
> and re-run independently in `adversarial/adv2_ks.json` (`K=1,2,3`,
> `p=0.70,0.19,0.09`; no rejection); (c) the exact match, for a
> *different* microscopic model with the same `K`-conditional limit
> structure, of Hansen & Jaworski's Theorem 7(ii) — §5.5.

### 5.5 The Hansen–Jaworski connection

**The model (verbatim model description, from the source).** Hansen &
Jaworski, *Structural transition in random mappings*, Electronic
Journal of Combinatorics **21**(1) (2014), #P1.18 (Jennie C. Hansen,
Heriot–Watt University; Jerzy Jaworski, Adam Mickiewicz University;
submitted Jul 11 2013, accepted Jan 17 2014). Abstract (verbatim):
*"In this paper we characterise the structural transition in random
mappings with in-degree restrictions. Specifically, for integers
`0 ⩽ r ⩽ n`, we consider a random mapping model `T̂ⁿᵣ` from
`[n] = {1, 2, . . . , n}` into `[n]` such that `Ĝⁿᵣ`, the directed
graph on `n` labelled vertices which represents the mapping `T̂ⁿᵣ`, has
`r` vertices that are constrained to have in-degree at most 1 and the
remaining vertices have in-degree at most 2. When `r = n`, `T̂ⁿᵣ` is a
uniform random permutation and when `r < n`, we can view `T̂ⁿᵣ` as a
'corrupted' permutation."* (p.1, §1). Their `a := n-r` is the number of
vertices allowed in-degree up to 2 (the "corruption budget"); `X̂ⁿᵣ`
denotes the number of cyclic vertices of `T̂ⁿᵣ` (§3, "the number of
cyclic vertices in `Ĝⁿᵣ`").

**Theorem 7(ii), verbatim (from the fetched PDF, `combinatorics.org`,
`v21i1p18/pdf`, p.12–13):**

> "**Theorem 7.** … (ii) Suppose that `0 < x < 1` (and `x` is fixed).
> If `r = n − a` where `a ∈ Z⁺` is fixed and `k = ⌊xn⌋`, then
>
> `Pr{X̂ⁿᵣ = k} ∼ \dfrac{1}{n}\, 2ax(1-x^2)^{a-1}`."

**The connection.** Their `a` is our `K` (a *fixed* number of
"defects"/reroutes as `n\to\infty`); `X̂ⁿᵣ/n` is their analogue of our
cyclic-mass fraction `M_K`. Their Theorem 7(ii) is a *local limit
theorem*, i.e. it is precisely a statement that the rescaled discrete
variable `X̂ⁿᵣ/n` converges (in the appropriate local sense) to a
continuous limit with density `2ax(1-x^2)^{a-1}` on `(0,1)` — **the
exact density conjectured in §5.4, with `a\leftrightarrow K`.** The two
models are microscopically different: Hansen–Jaworski's `T̂ⁿᵣ` is drawn
*uniformly* from all mappings satisfying the stated in-degree
constraint (no reroute/Bernoulli mechanism at all), whereas `M_n(c)`
(§1) is a uniform permutation with `K\sim\mathrm{Binomial}(n,c/n)`
points independently reroute-corrupted. That two different
microscopic constructions produce, conditionally on the same "defect
count" `K=a`, the *same* limiting mass density is exactly the kind of
universality fact worth flagging rather than assuming: it is
**consistent with, and non-trivial supporting evidence for,** the
conjecture of §5.4, but Theorem 7(ii) is a theorem about `T̂ⁿᵣ`, not
about `M_n(c)` or `L(c)` — it does **not**, by itself, constitute a
proof of §5.4's conjecture for the u12 ensemble. (The mean matches
exactly and unconditionally: `\int_0^1 x\cdot2ax(1-x^2)^{a-1}dx =
\int_0^1(1-x^2)^a dx = \varphi_a` by §5.4's identity — so the *means*
of the two models' `K`-conditional laws provably coincide; it is the
full densities' coincidence across two different microscopic models
that remains conjectural for `K\ge2` from the u12 side.)

This citation was independently fetched and verified in this document
(PDF retrieved from `combinatorics.org`, converted with
`pdftotext -layout`, Theorem 7 located and quoted directly from the
extracted text — not reproduced from the wave-2 adversarial paraphrase,
though it agrees with `../limit_characterization/adversarial/
ADVERSARIAL_VERDICT.md`'s independently-fetched quote).

---

## 6. Status at the end of Stage 1

**PROVED in this document (self-contained, from Definition 3, modulo
only Proposition 2.4's interpretive role — see below):**

1. Theorem 1: `φ_∞(c) = \int_0^1 e^{-ct^2}dt = \frac12\sqrt{\pi/c}\,
   \mathrm{erf}(\sqrt c)` on `L(c)` (§3), with the `(1-t)`-cancellation
   derived (not asserted) from two independent random variables per
   mark (survival factor `\times` competing-clock tail factor), and an
   explicit account (§3.1) of why this derivation cannot fall into the
   `\sqrt2` size-biasing error flagged by the wave-2 adversarial check.
2. Corollary 4.1 (series, entire function, `a_1=1/3` exact) and
   Corollary 4.2 (tail `\frac{\sqrt\pi}2 c^{-1/2}` with a rigorous,
   explicit `O(e^{-c})` error bound), both by elementary calculus on
   the proved closed form, with the term-by-term-integration /
   integration-by-parts steps justified explicitly (Weierstrass
   `M`-test; sign-definite IBP remainder).
3. Lemma 2, mean: `\varphi_K = \int_0^1(1-t^2)^K dt = 4^K(K!)^2/(2K+1)!`
   for every fixed `K\ge0`, by the same exploration technique as
   Theorem 1 (§5.2), plus its Poisson-mixture consistency with
   Theorem 1 (§5.2).
4. Lemma 2, density at `K=1`: `f_{M_1}(x)=2x` on `(0,1)`, by a direct
   whole-space (not single-point) computation (§5.3) — genuinely new
   relative to DERIVATION.md, which only proved the `K=1` *mean*.
5. The mean-consistency identity `\int_0^1 x\cdot2Kx(1-x^2)^{K-1}dx =
   \varphi_K` for every `K` (§5.4), by integration by parts.
6. Hansen–Jaworski (EJC 21(1) 2014, #P1.18) Theorem 7(ii), quoted
   verbatim from an independently fetched and `pdftotext`-extracted
   copy of the source PDF (§5.5), together with an explicit statement
   of exactly what the citation does and does not establish for the
   u12 ensemble (matches the conjectured density's functional form and
   the exact mean; does not itself prove the u12-side conjecture for
   `K\ge2`, since it is a theorem about a different microscopic model).

**CONJECTURED (explicitly, not proved here):**

7. `f_{M_K}(x) = 2Kx(1-x^2)^{K-1}` for `K\ge2` — full distributional
   law of the cyclic mass on `L(c)` conditional on `K` reroutes (§5.4).
   Consistent with its mean (proved), with KS tests reported upstream,
   and with Hansen–Jaworski's theorem for a related-but-different
   model; not derived from first principles here. A proof would need a
   whole-space (not single-point-exploration) argument, analogous to
   §5.3 but for general `K` — flagged as a candidate follow-up, scope
   TBD (not claimed to be Stage 2's job, since Stage 2 as scoped is
   about the `M_n(c)\to L(c)` bridge, a different gap).

**CITED, not re-derived (the one classical structural input):**

8. Proposition 2.4 (§2.3): that the explicit hazard-clock construction
   of Definition 3 is the standard exploration representation of a
   `PD(1)`/`GEM(1)`-distributed cycle partition with independent
   Poisson(c) marks (Kingman 1975; Arratia–Barbour–Tavaré 2003, "Feller
   coupling"). This affects only the *interpretation* of Definition 3
   as "the u12 limit object" — it is not needed for, and is not used
   again in, the internal validity of any proof in §3–§5 (all of which
   use only Definition 3's explicit, independent-by-construction
   primitives). Fact A (§2.3, the `K=0`/single-clock marginal) gives an
   elementary, self-contained partial check of Proposition 2.4.

**Explicitly out of scope for this document (left for Stage 2 or
later):**

9. Any statement that `M_n(c)` (§1, finite `n`) converges to `L(c)`
   (§2) as `n\to\infty`, in any topology or rate. Nothing above proves
   or assumes this; it is the empirical/adversarial control currently
   provided by `../limit_characterization/`'s finite-`n` numerics
   (T1–T4, and the adversarial exact-enumeration/extrapolation and
   Monte Carlo surfaces), not by a theorem.
10. A first-principles (non-cited) proof of Proposition 2.4's
    multi-arc-head independence claim.
11. A proof of the general-`K` density (item 7 above).

No result in this document required fabricating a citation, a
numerical value, or a "novelty" claim; items 7, 10, 11 are left open
honestly rather than asserted. `../limit_characterization/`'s own
numerical/adversarial validation of `\varphi_\infty(c)` and `\varphi_K`
(both means) is untouched and unnecessary to re-litigate here — this
document adds the *proof* layer for exactly the pieces that layer
supports, and no further.

*(Stage 2 continues immediately below, in the same document, and takes
up item 9 above — the `M_n(c)\to L(c)` bridge — directly. It closes
part of item 9 with a genuine proof and isolates precisely what remains
open; see §7.)*

---

## 7. The n→∞ bridge: precise statement, a proved reduction, two proved base cases, and the exact open lemma

### 7.1 What exactly has to be shown

Recall `φ(n,c) := E[\#\{\text{cyclic points of }f\}]/n` under Definition
1 (`M_n(c)`, §1) and `φ_∞(c) := \int_0^1 e^{-ct^2}dt` under Definition 3
(`L(c)`, §2, proved equal to `E[\text{cyclic fraction in }L(c)]` in
Theorem 1). The bridge this section addresses is exactly:

> **Target statement.** For every fixed `c \ge 0`:
> `\displaystyle\lim_{n\to\infty} \varphi(n,c) = \varphi_\infty(c)`.

This is a claim about a *pointwise-in-`c`* limit, one `c` at a time; a
stronger *locally-uniform-in-`c`* version (the limit holding uniformly
for `c` in any compact `[0,C]`) is a natural strengthening, not
attempted here and flagged as its own gap (§9, item 4). Nothing in §§1–6
proves or assumes the Target statement; §6 item 9 lists it as fully
open. This section proves a genuine piece of it and isolates, with
surgical precision, what is missing for the rest.

### 7.2 Exact reduction to a fixed-`K` statement

**Definition 4 (`M_n(c)` conditioned on exactly `K` reroutes).** Under
Definition 1, let `K_n := \#\{i : \xi_i=1\}` (so `K_n\sim
\mathrm{Binomial}(n,c/n)`, though its law plays no role in this
Definition — only its *conditioning* does). For `0\le K\le n` define

`\varphi_n^{(K)} := E\big[\#\{\text{cyclic points of }f\}/n \;\big|\; K_n=K\big]`.

Since `\pi` is independent of `\xi` (Definition 1), conditioning on
`K_n=K` leaves `\pi` a uniform random permutation and makes the set of
`K` rerouted indices a uniform random `K`-subset of `[n]`, independent
of `\pi`; by the resulting exchangeability, `\varphi_n^{(K)}` depends
only on `(n,K)`, not on *which* subset is realized. `\varphi_n^{(K)}`
is thus a well-defined, purely combinatorial quantity — no `c`
anywhere in Definition 4.

**Fact 4.1 (exact finite-`n` mixture identity, immediate from total
expectation).** For every `n` and every `c\ge0`,

`\displaystyle \varphi(n,c) = \sum_{K=0}^n \binom{n}{K}\Big(\frac cn\Big)^K\Big(1-\frac cn\Big)^{n-K}\varphi_n^{(K)}`,  (7.1)

i.e. `\varphi(n,c) = E_{K_n}[\varphi_n^{(K_n)}]` with `K_n\sim
\mathrm{Binomial}(n,c/n)` — exact, not asymptotic, for every finite `n`
with `n>c` (so that `c/n\in(0,1)` is a valid Bernoulli parameter,
matching Definition 1). Likewise, mixing `\varphi_K` (Lemma 2, §5.2)
over `K\sim\mathrm{Poisson}(c)` reproduces `\varphi_\infty(c)` exactly
(already proved in §5.2's "Consistency with Theorem 1" remark):

`\displaystyle \varphi_\infty(c) = \sum_{K=0}^\infty e^{-c}\frac{c^K}{K!}\varphi_K`.  (7.2)

(7.1)–(7.2) reduce the Target statement to a question about matching
the two mixtures as `n\to\infty`, given that `\mathrm{Binomial}(n,c/n)
\to \mathrm{Poisson}(c)` and (hoped) `\varphi_n^{(K)}\to\varphi_K` for
each `K`. The next proposition makes this reduction rigorous.

> **Proposition 3 (mixing reduction; PROVED, unconditionally).** Fix
> `c\ge0`. If `\varphi_n^{(K)} \to \varphi_K` as `n\to\infty`, for
> *every* fixed integer `K\ge0` (the "fixed-`K` bridge" — status
> examined in §7.3–7.4), then `\varphi(n,c)\to\varphi_\infty(c)` as
> `n\to\infty`, i.e. the Target statement of §7.1 holds at `c`.

*Proof.* Write `p:=c/n`, `\mathrm{Bin} := \mathrm{Binomial}(n,p)`,
`\mathrm{Poi}:=\mathrm{Poisson}(c)`. By (7.1)–(7.2), using `0\le
\varphi_K\le1` for all `K` (Lemma 2, §5.2: `\varphi_K` is a probability)
to insert and subtract the cross term,

`\varphi(n,c)-\varphi_\infty(c) = \underbrace{\sum_K P(\mathrm{Bin}=K)\big(\varphi_n^{(K)}-\varphi_K\big)}_{=:A_n} + \underbrace{\sum_K \big(P(\mathrm{Bin}=K)-P(\mathrm{Poi}=K)\big)\varphi_K}_{=:B_n}`.

**Bounding `B_n`.** `|B_n| \le \sum_K |P(\mathrm{Bin}=K)-P(\mathrm{Poi}=K)|
\cdot 1 = 2\,d_{TV}(\mathrm{Bin},\mathrm{Poi})`. For fixed `K`, the
elementary limit (the textbook "Poisson limit theorem," proved directly
here, not cited): with `p=c/n`,

`P(\mathrm{Bin}=K) = \frac{c^K}{K!}\cdot\underbrace{\frac{n(n-1)\cdots(n-K+1)}{n^K}}_{\to\,1}\cdot\Big(1-\frac cn\Big)^{n-K} \xrightarrow[n\to\infty]{} \frac{c^K}{K!}e^{-c} = P(\mathrm{Poi}=K)`,

using `\big(1-\tfrac cn\big)^{n-K}\to e^{-c}` for fixed `K` (standard).
This is *pointwise-in-`K`* convergence of two probability mass functions
on the same countable space `\{0,1,2,\dots\}`; by **Scheffé's lemma**
(Scheffé, *A useful convergence theorem for probability distributions*,
Ann. Math. Statist. 18 (1947) 434–438 — CITED, standard, not
re-derived: pointwise a.e. convergence of a sequence of probability
densities on a common measure space, here counting measure on `\mathbb
N`, implies convergence in `L^1`, i.e. in total variation), `d_{TV}
(\mathrm{Bin},\mathrm{Poi})\to0`. Hence `B_n\to0`. (A quantitative rate
`d_{TV}\le c^2/n` is available — Le Cam, *An approximation theorem for
the Poisson binomial distribution*, Pacific J. Math. 10 (1960)
1181–1197, CITED, not independently re-verified in this session — but
only the qualitative limit is used below.)

**Bounding `A_n`.** Fix `\varepsilon>0`. Since `\varphi_K\in[0,1]` for
every `K` and `\sum_K P(\mathrm{Poi}=K)=1`, choose `M` with
`P(\mathrm{Poi}>M)<\varepsilon/4`. We first show `P(\mathrm{Bin}>M)` is
controlled *uniformly in `n`* by a bound depending only on `c,M` — this
is the step that needs the index `n` handled with care, since `\mathrm
{Bin}`'s support grows with `n`. For any `t>0`, Markov's inequality on
`e^{tX}` gives, with `X\sim\mathrm{Bin}(n,p)`, `\mu:=np=c`, and
`1+x\le e^x`:

`P(X\ge M) \le e^{-tM}E[e^{tX}] = e^{-tM}(1-p+pe^t)^n \le e^{-tM}\exp\big(np(e^t-1)\big) = \exp\big(c(e^t-1)-tM\big)`.

Minimizing the exponent over `t>0` at `t=\log(M/c)` (valid for `M>c`)
gives the standard multiplicative Chernoff bound

`P(\mathrm{Bin}(n,c/n)\ge M) \le e^{-c}\Big(\frac{ec}{M}\Big)^M =: \delta(c,M)`,  (7.3)

a bound depending only on `c,M` — **not on `n`** — and `\delta(c,M)\to0`
as `M\to\infty` for fixed `c` (since `ec/M\to0`). This uniform-in-`n`
tail control is exactly what is needed and is derived here from
scratch (not imported as an unverified citation), so choose `M` large
enough that *also* `\delta(c,M)<\varepsilon/4` (possible by the two
limits just noted; enlarge `M` from the previous paragraph if needed).
Then, for **every** `n`:

`A_n = \sum_{K\le M} P(\mathrm{Bin}=K)(\varphi_n^{(K)}-\varphi_K) + \sum_{K> M} P(\mathrm{Bin}=K)(\varphi_n^{(K)}-\varphi_K)`,

and the second sum is bounded in absolute value by `P(\mathrm{Bin}>M)
\cdot 1 \le \delta(c,M) < \varepsilon/4` (using `(7.3)` and `|\varphi_n^{(K)}-\varphi_K|\le1`, since both are probabilities in `[0,1]`),
**for every `n`**. For the first (finite, `M+1`-term) sum: by
hypothesis `\varphi_n^{(K)}\to\varphi_K` for each of the finitely many
`K\in\{0,\dots,M\}`, and `P(\mathrm{Bin}=K)\to P(\mathrm{Poi}=K)\le1` is
bounded, so the finite sum `\to 0` as `n\to\infty`; hence it is
`<\varepsilon/4` for `n` large enough (depending on `M`, hence on
`\varepsilon`, but `M` itself was fixed once and for all above). For
such `n`, `|A_n| < \varepsilon/4+\delta(c,M) < \varepsilon/2` (using
`\delta(c,M)<\varepsilon/4` from the choice of `M`).

Combining, `|\varphi(n,c)-\varphi_\infty(c)| \le |A_n|+|B_n| < \varepsilon`
for `n` large enough. Since `\varepsilon>0` was arbitrary, `\varphi(n,c)
\to\varphi_\infty(c)`. `∎`

**What this proposition does and does not establish.** It is an
unconditional, fully self-contained proof of *one* implication: fixed-`K`
convergence (for every `K`) `\Rightarrow` the Target statement (at the
given `c`). It uses no unproved input beyond two named classical facts
(Scheffé's lemma, and — only for the optional rate remark — Le Cam's
bound), both used exactly as stated, and an elementary Chernoff-type
tail bound derived from first principles in the proof itself. It does
not by itself prove the Target statement, because its hypothesis is
fixed-`K` convergence for *every* `K` — the genuinely open item
addressed next.

### 7.3 The fixed-`K` bridge: two base cases, proved exactly

**`K=0` (trivial, exact for every `n`, PROVED).** With `K=0` no point is
rerouted, so `f=\pi` exactly, a permutation — and every point of a
permutation is cyclic (a bijection of a finite set decomposes into
disjoint cycles covering all of `[n]`). Hence

`\varphi_n^{(0)} = 1 = \varphi_0`  for every `n\ge1`,  (7.4)

an exact identity, not merely a limit — the `K=0` fixed-bridge gap does
not merely close, it never existed.

**`K=1` (PROVED exactly, with an explicit `O(1/n^2)` rate).**

> **Proposition 4.** For every `n\ge1`,
> `\varphi_n^{(1)} = \dfrac{2n^2+1}{3n^2} = \dfrac23+\dfrac1{3n^2}`.
> In particular `\varphi_n^{(1)}\to\varphi_1=2/3` as `n\to\infty`, with
> exact rate `\varphi_n^{(1)}-\varphi_1 = 1/(3n^2)`.

*Proof.* By Definition 4's exchangeability, fix the rerouted index at
`i^*:=1` WLOG; `\pi` is then an unconditioned uniform random permutation
of `[n]`, independent of the reroute target `U:=U_1`, uniform on `[n]`
(Definition 1). Let `C` be the cycle of `\pi` containing `1`, of length
`L`.

*Step 1 (classical exact fact: `L` is exactly uniform on
`\{1,\dots,n\}`, for every `n`).* For each `\ell\in\{1,\dots,n\}`, the
number of permutations of `[n]` with `1` in a cycle of length `\ell` is
`\binom{n-1}{\ell-1}(\ell-1)!\,(n-\ell)! = (n-1)!` (choose the other
`\ell-1` cycle-mates, arrange the `\ell` elements including `1` into one
cycle in `(\ell-1)!` ways, permute the remaining `n-\ell` elements
freely) — the same count `(n-1)!` for every `\ell`. Dividing by `n!`:
`P(L=\ell)=1/n` for `\ell=1,\dots,n`, exactly, not asymptotically —
this is the classical fact recorded without proof at the
`L\to\mathrm{Unif}(0,1)` continuum level in Fact A (§2.3); here it holds
exactly at every finite `n`.

*Step 2 (points outside `C` are always cyclic).* `\pi`'s cycles
partition `[n]`; a point `y\notin C` has its entire forward `\pi`-orbit
confined to `y`'s own cycle (disjoint from `C`), hence never equal to
`1=i^*`. Since only `i^*=1` is rerouted, `f` agrees with `\pi` along
`y`'s whole forward orbit, so `y` is cyclic under `f` iff cyclic under
`\pi` — always true. **All `n-L` points outside `C` are cyclic under
`f`, regardless of `U`.**

*Step 3 (case analysis inside `C`, exact counts).* Label `C`'s points
`c_0=1,c_1=\pi(1),\dots,c_{L-1}`, `\pi(c_{L-1})=c_0`. Only `f(c_0)=U`
differs from `\pi`; `f(c_j)=\pi(c_j)=c_{j+1}` for `j=1,\dots,L-1`
(unaffected).
- `U\notin C` (prob. `(n-L)/n` given `L`): the chain
  `c_1\to\cdots\to c_{L-1}\to c_0\to U` never returns into `C`; **0**
  points of `C` are cyclic.
- `U=c_0` (prob. `1/n` given `L`): `c_0` is a fixed point (self-loop,
  cyclic); `c_1,\dots,c_{L-1}` feed into it without return; **1** point
  of `C` is cyclic.
- `U=c_d`, `d\in\{1,\dots,L-1\}` (prob. `1/n` each): the arrows
  `c_d\to c_{d+1}\to\cdots\to c_{L-1}\to c_0\to c_d` close a cycle of
  `L-d+1` points; `c_1,\dots,c_{d-1}` (present when `d\ge2`) feed into
  it without return. **`L-d+1`** points of `C` are cyclic.

Summing the within-`C` cyclic count given `L=\ell` (each of the `n`
possible values of `U` equally likely, `\ell` of which land in `C`):

`E[\text{within-}C\mid L=\ell] = \frac1n\Big[1+\sum_{d=1}^{\ell-1}(\ell-d+1)\Big] = \frac1n\Big[1+\frac{(\ell-1)(\ell+2)}2\Big]`,

using `\sum_{d=1}^{\ell-1}(\ell-d+1)=\sum_{j=1}^{\ell-1}(j+1)=\frac{(\ell-1)\ell}2+(\ell-1)=\frac{(\ell-1)(\ell+2)}2`
(checked directly at `\ell=3,4`: `5,9`). With Step 2:

`E[\#\text{cyclic}\mid L=\ell] = (n-\ell) + \frac1n\Big[1+\frac{(\ell-1)(\ell+2)}2\Big]`.

*Step 4 (average over `L\sim\mathrm{Unif}\{1,\dots,n\}`, Step 1).* Using
`E[\ell]=(n+1)/2` and `E[\ell^2]=(n+1)(2n+1)/6`:

`E[(\ell-1)(\ell+2)] = E[\ell^2]+E[\ell]-2 = \frac{(n+1)(n+2)-6}{3}`,

hence `\frac1n\big[1+\tfrac12E[(\ell-1)(\ell+2)]\big] = \frac{(n+1)(n+2)}{6n}`, and

`\varphi_n^{(1)} = \frac{n-1}{2n}+\frac{(n+1)(n+2)}{6n^2}`.

Over common denominator `6n^2`: numerator `3n(n-1)+(n+1)(n+2) =
3n^2-3n+n^2+3n+2 = 4n^2+2`, so `\varphi_n^{(1)} = \dfrac{4n^2+2}{6n^2} =
\dfrac{2n^2+1}{3n^2} = \dfrac23+\dfrac1{3n^2}`. `∎`

**Independent verification (exact enumeration, not sampling).** The
closed form was checked against brute-force exact enumeration (all
`n!` permutations `\times` `n` reroute targets, exact rational
arithmetic) for `n=1,\dots,7`: exact rational agreement in every case
(`n=2`: `3/4`; `n=3`: `19/27`; `n=4`: `11/16`; `n=5`: `17/25`; `n=6`:
`73/108`; `n=7`: `33/49` — all equal `2/3+1/(3n^2)`). Script:
`k1_exact_check.py`, this directory.

**Corollary 4.3 (the `a_1(n)` pattern, PROVED — closing an item the
adversarial check only established empirically).** Define
`a_1(n) := -\partial_c\varphi(n,c)|_{c=0}`, the linear Taylor coefficient
of `\varphi(n,\cdot)` at `c=0` (matching `\varphi_\infty(c) =
1-\tfrac13c+O(c^2)`, Cor. 4.1). Differentiating (7.1) term-by-term at
`c=0` (a finite sum for each fixed `n`): only the `K=0,1` terms of
`\mathrm{Bin}(n,c/n)` contribute a nonzero `c`-derivative at `c=0`
(`P(K=0)=(1-c/n)^n`, `P(K=1)=c(1-c/n)^{n-1}`; `K\ge2` terms are
`O(c^2)`), giving `\partial_c\varphi(n,c)|_0 = -\varphi_n^{(0)}
+\varphi_n^{(1)} = \varphi_n^{(1)}-1` (using (7.4)). By Proposition 4:

`a_1(n) = 1-\varphi_n^{(1)} = \frac13-\frac1{3n^2} = \frac{n^2-1}{3n^2}`,  (7.5)

**exactly reproducing** the pattern the wave-2 adversarial check found
only by numerical extrapolation from exact enumeration at `n=4,5,6,7`
(`../limit_characterization/adversarial/adv2_extrap.json`: `a_1(4)=
15/48=0.3125`, `a_1(5)=24/75=0.32`, `a_1(6)=35/108\approx0.324074`,
`a_1(7)=48/147\approx0.326531` — matching (7.5) to the precision
reported there). What was an empirical pattern inferred from four data
points is here a proved identity for every `n`.

### 7.4 The fixed-`K` bridge for `K≥2`: the exact missing lemma

The `K=1` proof (§7.3) worked because a single reroute disturbs exactly
one background `\pi`-cycle, reducing everything to a case split on one
uniform target `U`. For `K\ge2`, the `K` rerouted points can strike the
*same* background cycle (in either order) or *different* cycles whose
severed pieces can then be re-linked by a later reroute's target landing
on an earlier reroute's severed tail — a combinatorial explosion the
`K=1` argument does not touch. This is not proved here. The precise
missing statement is:

> **Open Lemma (fixed-`K` bridge, `K\ge2`).** For every fixed integer
> `K\ge2`, `\displaystyle\lim_{n\to\infty}\varphi_n^{(K)} = \varphi_K =
> \frac{4^K(K!)^2}{(2K+1)!}` (Definition 4 and Lemma 2 respectively).
>
> *Status:* neither proved nor disproved in this document. By
> Proposition 3 (§7.2), this Open Lemma for **every** `K\ge0` is
> exactly what is needed (together with the already-proved `K=0,1`
> cases) to convert the Target statement of §7.1 into a theorem; it is
> the one remaining piece.

**Proof strategy for the Open Lemma (sketch, not executed).** A natural
route generalizing §7.3: couple the `K` discrete uniform reroute targets
and the discrete cycle structure of `\pi` with `K` continuum points and
the `\mathrm{PD}(1)` cycle partition of `L(c)`'s construction (Def. 3),
and bound the probability that the coupling fails — i.e. that some
"collision" occurs that has no continuum counterpart (two reroute
targets landing on the same point, a reroute target landing exactly on
another reroute's source, or two reroute-affected regions overlapping
within `O(1/n)` of each other in cycle-position). For fixed `K` and
`n\to\infty`, each such collision has probability `O(K^2/n)\to0`, which
is the heuristic reason the Open Lemma should be true; turning this into
a real proof requires (i) a precise coupling construction (not just the
collision-probability heuristic), and (ii) an argument that, off the
collision event, the discrete cyclic-count functional converges to the
continuum one — i.e. essentially redoing DERIVATION.md §1–2's
rates-convergence argument rigorously, but now for `K` simultaneous
arc-heads instead of one. Neither (i) nor (ii) is carried out here; this
is a plausible route, not a proof.

**Empirical exploration for `K=2` (exact enumeration, honestly
reported, including where the pattern from `K=0,1` does *not*
obviously continue).** Exact brute-force enumeration (all `n!`
permutations `\times` `n^2` reroute-target pairs, exact rational
arithmetic, two fixed rerouted indices `i^*_1=1,i^*_2=2`) for
`n=2,\dots,8` (script `k2_exact_exploration.py`, this directory) gives:

| `n` | `\varphi_n^{(2)}` (exact) | decimal | `\varphi_n^{(2)}-\varphi_2` | `n^2\cdot(\varphi_n^{(2)}-\varphi_2)` |
|---|---|---|---|---|
| 2 | 3/4 | 0.75000 | 13/60 | 0.8667 |
| 3 | 17/27 | 0.62963 | 13/135 | 0.8667 |
| 4 | 113/192 | 0.58854 | 53/960 | 0.8833 |
| 5 | 356/625 | 0.56960 | 68/1875 | 0.9067 |
| 6 | 151/270 | 0.55926 | 7/270 | 0.9333 |
| 7 | 569/1029 | 0.55296 | 101/5145 | 0.9619 |
| 8 | 281/512 | 0.54883 | 119/7680 | 0.9917 |

`\varphi_n^{(2)}` decreases monotonically toward `\varphi_2=8/15\approx
0.53333` — **consistent with, and independent evidence for,** the Open
Lemma at `K=2`, beyond the mean-only, sampling-based evidence already
in `RESULTS_SUMMARY.md`/`ADVERSARIAL_VERDICT.md` (this is exact
enumeration of the specific fixed-`K` model of Definition 4, not Monte
Carlo of the mixed-`c` model). **However**, unlike `K=0` (rate exactly
`0`) and `K=1` (rate exactly `1/(3n^2)`, §7.3), the rescaled deviation
`n^2\cdot(\varphi_n^{(2)}-\varphi_2)` is **not** settling to a constant
over this range — it increases from `0.867` at `n=2,3` to `0.992` at
`n=8`, with no sign of leveling off. This does not contradict the Open
Lemma (convergence can hold with a slowly-varying or non-`1/n^2` rate),
but it does mean: **do not extrapolate the clean `O(1/n^2)` rate found
at `K=1` to general `K`** — that would be an unsupported guess, flagged
here precisely so it is not later asserted as if established. Whether
`\varphi_n^{(K)}-\varphi_K` is `\Theta(1/n^2)`, `\Theta(\log n/n^2)`, or
something else for `K\ge2` is left fully open (§9, item 2).

### 7.5 Conclusion: the status of the general bridge

Combining §7.2–7.4: the Target statement of §7.1 is **proved** for every
`c\ge0` restricted to what §7.3 supplies alone — namely, the linear
(`c^1`) Taylor coefficient of `\varphi(n,c)` at `c=0` converges to that
of `\varphi_\infty(c)`, with the exact rate `O(1/n^2)` (Cor. 4.3). The
Target statement **in full** — `\varphi(n,c)\to\varphi_\infty(c)` for
every fixed `c\ge0`, not just to first order near `c=0` — is a
**PROPOSIÇÃO CONDICIONAL**: it follows immediately from Proposition 3
(§7.2, unconditionally proved) *given* the Open Lemma of §7.4 for every
`K\ge2`. No claim of "Teorema 3" is made in this document; the honest
label is:

> **Proposição Condicional 5.** For every fixed `c\ge0`,
> `\varphi(n,c)\to\varphi_\infty(c)` as `n\to\infty`, **conditional on**
> the Open Lemma of §7.4 holding for every integer `K\ge2`.

The gap between Proposição Condicional 5 and a full Theorem 3 is
exactly, and only, the Open Lemma — not vaguely "the finite-`n`→continuum
passage" as stated in DERIVATION.md §6 and old §6 item 9 of this
document, but the single precisely-quantified statement `\varphi_n^{(K)}
\to 4^K(K!)^2/(2K+1)!` for fixed `K\ge2`, `n\to\infty`. The existing
empirical/adversarial control — exact enumeration to `n=7` across
several `c` (`../limit_characterization/adversarial/adv2_exact.json`),
Monte Carlo to `n=65536` at fresh `c` values
(`../limit_characterization/adversarial/adv2_mc.json`), and now this
document's own `K=1` exact proof and `K=2` exact exploration to `n=8`
— is evidence *for* the Open Lemma and Proposição Condicional 5, not a
substitute for proving them; every source of that evidence is named
here precisely so the distinction between "supported" and "proved"
stays visible.

---

## 8. Conjectures (separated from proofs)

This section collects, in one place, every claim in this document that
is a **CONJECTURE** — numerically/adversarially supported, not proved —
as distinct from the **PROVED** theorems/lemmas/propositions of §§3–5
and §7, the **CITED** classical facts, and the single **PROPOSIÇÃO
CONDICIONAL** of §7.5.

**Conjecture 1 (the general-`K` distributional law, `K\ge2`).**

`f_{M_K}(x) = 2Kx(1-x^2)^{K-1}`, `x\in(0,1)`,

the full density of the cyclic-mass random variable `M_K:=\mathrm{Leb}
(\text{cyclic set})` on `L(c)` conditional on exactly `K` reroutes.
Proved only at `K=1` (§5.3, `f_{M_1}(x)=2x`, a genuinely new
whole-space computation). For `K\ge2`, status: CONJECTURE, first stated
in `../limit_characterization/RESULTS_SUMMARY.md` (categoria b).
Support (all independent of each other, none a proof): (a) the
mean-consistency identity `\int_0^1 x\cdot2Kx(1-x^2)^{K-1}dx=\varphi_K`,
proved for every `K` (§5.4) — necessary, not sufficient, for the
density to be correct; (b) Kolmogorov–Smirnov tests against exactly
this density, `K=1,2,3`, no rejection (`p=0.70,0.19,0.09` in
`adversarial/adv2_ks.json`; `p=0.455,0.770,0.357` in
`../limit_characterization/supplementary_distribution.json` — two
independent implementations, consistent); (c) Hansen–Jaworski's Theorem
7(ii) (EJC 21(1) 2014 #P1.18, quoted verbatim in §5.5), the exact same
functional form for a *different* microscopic model's `K`-conditional
limit — non-trivial supporting evidence via a universality argument,
not a proof for the u12 ensemble itself (§5.5 states precisely why not).

> **[Extensão, 2026-08-23 — DISC-DEC-057/DISC-DEC-061.]** `K=2` is now
> **PROVED** (modulo one classical citation at the same rigor level as
> this document's own §2.3 Proposition 2.4 — see "Estágio 15" below):
> `f_{M_2}(x)=4x(1-x^2)`, exactly. Conjecture 1 for `K\ge3` remains
> exactly as open as before — `K\ge3` was explicitly not attempted.

> **[Extensão, 2026-08-25 — DISC-DEC-065/DISC-DEC-067.]** `K=3` is
> also now **PROVED** (same citation, applied recursively — see
> "Estágio 17" below): `f_{M_3}(x)=6x(1-x^2)^2`, exactly. [Esta nota
> deveria ter sido inserida na integração do Estágio 17 e foi
> adicionada na integração seguinte, ao ser notada a omissão.]
> `K\ge4` está sob revisão adversarial (onda 16); nenhum resultado é
> afirmado aqui até o veredito.

> **[Extensão, 2026-08-25 — DISC-DEC-066/DISC-DEC-069.]** `K=4` is
> now **PROVED** as well (same citation, applied recursively up to
> three times — see "Estágio 20" below): `f_{M_4}(x)=8x(1-x^2)^3`,
> exactly — the SECOND consecutive unexpected closure in this line.
> Conjecture 1 is now proved at `K=1,2,3,4`; `K\ge5` remains open,
> explicitly not attempted (a concrete lead — the general
> weighted-forest identity `W(n)=1-Q` — is named for a future front).

> **[Extensão, 2026-08-26 — DISC-DEC-075.]** Conjecture 1 is now
> **PROVED for every `K\ge1`** — see "Estágio 24" below. The general
> weighted-forest identity `W(n)=e(e+Q)^{n-1}` named just above (the
> Estágio-20 lead) is proved for all `n` via Prüfer, closing the last
> per-`K` ingredient at once instead of one `K` at a time; the same
> single `PD(1)` citation as `K=1..4` is applied recursively, up to
> `K-1` times, for each fixed `K`. `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` for
> **all** `K\ge1`, unconditionally.

**Conjecture 2 (the full unconditional distributional law).**

`M(c) \overset{d}{=} \min(1,\sqrt{E/c})`,  `E\sim\mathrm{Exp}(1)`, i.e.
`P(M(c)\le x) = 1-e^{-cx^2}` for `x\in(0,1)` with an atom `e^{-c}` at
`x=1`,

the Poisson(`c`)-mixture of Conjecture 1 over `K`. Its mean is
`\varphi_\infty(c)`, **proved** (Theorem 1) — the mean of Conjecture 2
is not itself conjectural, only the full distribution around that mean.
Status: CONJECTURE (inherits Conjecture 1 for `K\ge2`; the `K=0,1`
components of the mixture are exact). Support: KS test at Poisson
`c=1` against the atom+continuous mixture, no rejection (atom `z=+0.33`,
continuous part `p=0.171`,
`../limit_characterization/supplementary_distribution.json`).

> **[Extensão, 2026-08-25 — DISC-DEC-066/DISC-DEC-067.]** Uma rota
> **direta** (não caso-a-caso em `K`) para esta conjectura foi
> tentada e NÃO fechou — não-fechamento honesto, com progresso parcial
> catalogado (ver "Estágio 18" abaixo): a arquitetura do método dos
> momentos está montada e correta-se-completada; o alvo
> `E[M(c)^2]=(1-e^{-c})/c` (com `E[M_K^2]=1/(K+1)`, incondicional
> apenas em `K\le3` via as densidades provadas; alvo conjectural no
> geral) está registrado; a redução por blocos do caso `p=2` está
> provada; e a rota de acoplamento Poissonization-em-`c` está
> **refutada** como caminho para uma equação-mestra no escalar `M(c)`
> (contraexemplo exato: adicionar um reroute pode AUMENTAR a massa
> cíclica). O passo genuinamente difícil — uma exploração conjunta de
> dois pontos de referência — está precisamente localizado e aberto.

> **[Extensão, 2026-08-26 — DISC-DEC-075.]** Conjecture 2 is now
> **PROVED, at the same modulo-citation tier as Conjecture 1** — see
> "Estágio 24" below. Not via the direct route above (which remains
> exactly as it stood: partial architecture proved, obstruction
> precisely located, still open on its own terms) but as an
> **indirect corollary**: Conjecture 1 general-`K` plus §5.1's already-
> cited Poisson-mixture conditioning fact and countable additivity give
> `P(M(c)\le x)=1-e^{-cx^2}` in three lines. Both closed-form targets
> named just above are now exact and unconditional:
> `E[M(c)^2]=(1-e^{-c})/c` and `E[M_K^2]=1/(K+1)` for **every** `K`,
> not only `K\le3`. The "Status: CONJECTURE" line above is superseded.

**On the Open Lemma of §7.4 — a deliberate non-inclusion here.** The
`n\to\infty` fixed-`K` bridge for `K\ge2` (§7.4) is **not** listed as a
Conjecture 3, even though it is unproved and numerically supported,
because it is a different *kind* of open claim: Conjecture 1–2 concern
an *object* (a distributional law on `L(c)`, already fully and
unambiguously defined) whose exact form is guessed from patterns and
partial checks; the Open Lemma concerns a *convergence statement*
between two well-defined but different-`n` objects, addressed by a
specific (if incomplete) proof strategy in §7.4, not by pattern-matching
a candidate formula. Keeping the two apart matters for follow-up work:
Conjecture 1–2 need a new closed-form computation (of the kind §5.3
carried out for `K=1`); the Open Lemma needs a convergence/coupling
argument (of the kind sketched, but not executed, in §7.4).

Nothing above is asserted as fact anywhere else in this document —
every reference to Conjecture 1 or 2 elsewhere (§5.4, §5.5, §7)
explicitly labels it CONJECTURE at the point of use.

---

## 9. Master list of every open gap in the whole document

Every item below is a genuine gap — nothing here is closed elsewhere in
the document under a different name. Old §6 (Stage 1) numbered its own
residual items 7, 10, 11; those are folded in below (cross-referenced)
rather than duplicated.

1. **The fixed-`K` bridge for `K\ge2`** (§7.4, Open Lemma):
   `\varphi_n^{(K)}\to\varphi_K=4^K(K!)^2/(2K+1)!` as `n\to\infty`, for
   fixed `K\ge2`. Unproved. This is the single hypothesis separating
   Proposição Condicional 5 (§7.5) from a full Theorem 3. A proof
   strategy is sketched, not executed, in §7.4.
2. **The rate of the `K\ge2` fixed-`K` bridge**, given gap 1 is
   eventually resolved. `K=0`: rate `0` (exact). `K=1`: rate exactly
   `1/(3n^2)` (Prop. 4). `K=2`: exact enumeration to `n=8` (§7.4) shows
   the naive `O(1/n^2)` extrapolation does **not** obviously hold — the
   rescaled deviation is still increasing at `n=8`, not leveling off.
   Fully open; do not assume any specific rate for `K\ge2` without
   further work.
3. **The full Target statement** (§7.1: `\varphi(n,c)\to\varphi_\infty
   (c)` for every fixed `c\ge0`, not just its `c^1` Taylor coefficient)
   is therefore only Proposição Condicional 5 (§7.5), not a theorem —
   directly downstream of gap 1.
4. **A locally-uniform-in-`c`** (not merely pointwise-in-`c`) version of
   the Target statement — not formulated in full or attempted; would
   need uniformity, across `c` in a compact set, of whatever resolves
   gaps 1–2.
5. **The general-`K` distributional law** `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`
   for `K\ge2` (Conjecture 1, §8; = old §6 item 7/11). Unproved; proved
   only at `K=1` (§5.3) [and now also at `K=2` — see "Estágio 15"
   below; `K\ge3` remains exactly this open].
6. **The full unconditional distributional law** `M(c)\overset{d}{=}
   \min(1,\sqrt{E/c})` (Conjecture 2, §8). Unproved; inherits gap 5.
7. **Proposition 2.4** (§2.3; = old §6 item 10): the explicit
   hazard-clock construction of Definition 3 as the standard
   `\mathrm{PD}(1)`/`\mathrm{GEM}(1)` exploration representation with
   independent Poisson(`c`) marks — CITED (Kingman 1975;
   Arratia–Barbour–Tavaré 2003), not re-derived from first principles
   in this document. Affects only the *interpretation* of Definition 3
   as "the u12 limit object," not the internal validity of §3–§5, §7's
   proofs (all self-contained given Definition 3 / Definition 4).
8. **Le Cam's quantitative TV bound** (`d_{TV}(\mathrm{Bin}(n,c/n),
   \mathrm{Poi}(c))\le c^2/n`, cited in §7.2's Proposition 3 proof, used
   only for an optional rate remark) — CITED (Le Cam 1960), not
   independently re-verified in this session. The qualitative
   convergence `d_{TV}\to0` that Proposition 3 actually needs *is*
   proved self-contained in §7.2 via the elementary Poisson-limit
   computation plus Scheffé's lemma (also cited, but a much lower-risk,
   extremely standard citation).
9. **The `n\le c` edge case** in Definition 1 (§1's `q=c/n\wedge1`
   proviso) — never analyzed or used anywhere in this document; every
   result here is stated for `n` large enough that `n>c`, which is
   automatic once `n\to\infty` at fixed `c`, but no finite-`n`, small-`n`
   statement in this document accounts for it.
10. **Any second-moment / fluctuation result** — Var of the cyclic
    fraction in `M_n(c)` or `L(c)`, a CLT, a concentration bound around
    `\varphi_\infty(c)` or `\varphi_K` — entirely untouched. Every
    result in this document (Theorem 1, Lemma 2, Propositions 3–4,
    Proposição Condicional 5) concerns first moments (means) or, for
    Conjectures 1–2, full laws asserted but not proved; no variance or
    concentration statement is proved or conjectured anywhere here.
11. **A first-principles proof of the `K=2` (or general `K\ge2`) exact
    finite-`n` formula**, analogous to Proposition 4's proof for `K=1`
    — not attempted beyond the numerical exploration of §7.4; the
    combinatorics (which cycles are struck, in what order, with what
    re-linking) grow substantially with `K` and are not worked out.

No item above was left vague to save effort: each names the precise
missing statement, the section that discusses it, and (where
applicable) exactly what partial progress exists. Items 1–4 are new to
Stage 2; items 5–7 restate Stage 1's own residual gaps (old §6, items
7/10/11) without alteration; items 8–11 are newly identified while
writing Stage 2 and were not present in Stage 1's gap list.

**[Ver Estágio 3 abaixo — item 11 acima está PARCIALMENTE FECHADO: o
caso K=2 do Lema Aberto foi provado, wave 5, DISC-DEC-022, 2026-08-22.
K≥3 permanece aberto exatamente como descrito.]**

---

## [Extensão, Estágio 3 — 2026-08-22] O caso K=2 do Lema Aberto: PROVADO

Onda 5 (`DISC-DEC-022`) autorizou uma tentativa delimitada do Lema
Aberto de §7.4 usando a estratégia de acoplamento ali esboçada. A
tentativa (`../k2_open_lemma/ATTEMPT.md`) não executou o acoplamento
literal, mas encontrou uma rota discreta autocontida que resolve o caso
`K=2` por completo — verificada por um referee adversarial hostil
independente (`../k2_open_lemma/adversarial/REFEREE_REPORT.md`), que
não encontrou nenhum erro e ainda fortaleceu um dos resultados (ver
abaixo). Este é o registro canônico e resumido; os documentos-fonte tem
o detalhe completo, incluindo todas as provas passo a passo.

**Resultado 1 — Lema da Redução A (PROVADO, K geral):**
`φ_n^{(K)} = (K/n)·ψ_n^{(K),R} + (1−K/n)·ψ_n^{(K)}`, reduzindo a ponte
geral à convergência da quantidade "ponto genérico" `ψ_n^{(K)}` sozinha
(o termo do "ponto reroteado, ele mesmo" morre por uma cota `O(K/n)→0`
de graça). Verificado como identidade exata em `n` finito pelo referee,
contra enumeração de força bruta própria, para `K=1` (`n`=2–10), `K=2`
(`n`=3–9) e `K=3` (`n`=4–8) — 24/24 casos batendo exatamente.

**Resultado 2 — K=1 rederivado por esta rota (PROVADO, consistência):**
`ψ_n^{(1)} = 2/3+1/(6n)`, `ψ_n^{(1),R} = 1/2+1/(2n)` — recombinando via
o Lema A, reproduz exatamente a Proposição 4 (`φ_n^{(1)}=2/3+1/(3n²)`),
revelando um cancelamento genuíno de termo `O(1/n)` entre as duas
peças. Confirmado pelo referee por enumeração própria, `n`=2–10.

**Resultado 3 — Lema do co-ciclo (PROVADO):** a probabilidade
`P=1/2` exata usada na análise de casos do `K=2` foi re-derivada do
zero pelo referee (`E[(L−1)/(m−1)]=1/2`) e confirmada por força bruta
para `m`=2–8, zero divergências.

**Resultado 4 — o CASO K=2 (PROVADO, incondicionalmente):**
`ψ_n^{(2)} = 8/15 + 4/(15n) + 1/(15n²)`, derivada por uma análise de
casos explícita (três casos sobre se as duas fontes de reroteamento
caem no próprio ciclo-π do ponto de referência). Verificada pelo
referee em quatro camadas independentes: rederivação manual de cada
peso de caso; força bruta ao nível dos casos (120 configurações,
`n`=3–7, 0 divergências); ressoma simbólica independente via sympy
(diferença simbólica exatamente 0); força bruta pura a partir da
definição crua, `n`=3–9 (`n`=9 é um ponto novo, além do alcance
original). Como `8/15 = φ_2` (a média de Wallis para `K=2`), isto prova
`φ_n^{(2)}→φ_2` **incondicionalmente** — mais forte do que qualquer
coisa que este documento estabelecia antes.

**Resultado 5 — a taxa exata bônus, PROMOVIDA de "ajustada" para
PROVADA:** a peça `ψ_n^{(2),R}` (originalmente encontrada por
interpolação racional exata e explicitamente rotulada "ajustada, não
derivada" pela tentativa original) foi **derivada do zero pelo próprio
referee** — o mesmo método de exploração/conjunto-alvo, aplicado
começando NO ponto-fonte (não num ponto genérico), reduz exatamente a
`P_b(m,0)`/`P_c(m,0,k)`. A ressoma simbólica reproduz
`(n+1)(5n+2)/(12n²)` exatamente (diferença simbólica 0), confirmada ao
nível de caso (75 configurações, `n`=3–7, 0 divergências), e um teste
de unicidade do ansatz mostra que o ajuste original era
sobre-determinado, não arbitrário. Isto **promove** a taxa completa

`φ_n^{(2)} = 8/15 + 1/(30n) + 7/(10n²) + 1/(5n³)`

de "provada condicionalmente a um item ajustado" para **provada
incondicionalmente** — e resolve o item 11 da lista de lacunas para
`K=2`: a taxa verdadeira de convergência é **Θ(1/n)**, não Θ(1/n²)
como a tabela original deste documento (§7.4) sugeria antes de ter a
forma fechada — a tabela nunca estabilizou porque estava medindo a
grandeza errada, não porque a convergência fosse anormalmente lenta.

**K≥3: continua honestamente ABERTO.** O custo combinatório do método
de análise de casos usado para `K=2` cresce com o número de fontes
sobre o próprio ciclo × sua ordenação × ordem de disparo do resto — o
referee confirma que a numeração para `K=3` (`n`=4–8) é apenas
suporte numérico, não uma alegação de taxa, exatamente como a
tentativa original já havia rotulado. Nenhum item foi inflado.

**Veredito honesto atualizado do documento inteiro (ao fim do Estágio
3):** Teorema 1 + corolários (Estágio 1); Lema 2 (Estágio 1);
Proposição 3 (Estágio 2); Proposição 4 = ponte exata K=0,1 (Estágio
2); **ponte exata K=2, incluindo taxa completa (Estágio 3, novo) —
agora PROVADA, não mais listada como faltante**. Resta como
PROPOSIÇÃO CONDICIONAL apenas a ponte geral para `K≥3` (Lema Aberto,
agora estritamente mais estreito do que "K≥2"). Conjecturas 1–2 (§8)
inalteradas. Fontes completas: `../k2_open_lemma/ATTEMPT.md`,
`../k2_open_lemma/adversarial/REFEREE_REPORT.md`.

**[Ver Estágio 4 abaixo — este veredito foi superado: os casos K=3,4,5
também foram provados, wave 6, DISC-DEC-031, 2026-08-22. K≥6 permanece
honestamente aberto.]**

---

## [Extensão, Estágio 4 — 2026-08-22] Os casos K=3,4,5 do Lema Aberto: PROVADOS por matriz de transferência uniforme em K

**Contexto.** O Estágio 3 (acima) provou `K=2` por análise de casos
manual (três casos sobre onde as fontes caem em relação ao próprio
ciclo do ponto de referência, ligados por um lema do co-ciclo com
simetria `P=1/2`), deixando `K≥3` honestamente aberto e diagnosticando
que esse método de análise de casos explode combinatorialmente com
`K`. Pedido explícito ao próximo agente: tentar uma técnica
genuinamente diferente, não mais uma rodada de análise de casos manual
— em particular, uma abordagem de função geradora/matriz de
transferência através de todo `K` simultaneamente.

**O método (novo, `k2_open_lemma/k3_attempt_2/ATTEMPT.md`).** Em vez
de dividir em casos manuais sobre "onde as fontes caem", a caminhada de
exploração discreta (Lema da Redução A, Estágio 3) é reformulada como
uma **cadeia de Markov explícita, exata, uniforme em `K`**, sobre um
estado de 3 inteiros `(a,b,r)` — `a` = número de consultas-π já
feitas (pontos permanentemente removidos do pool de alvos-π futuros),
`b` = número de pontos alcançados por um salto-U em território
inexplorado (permanecem no pool de alvos-π futuros — a distinção-chave
que a análise de casos manual do Estágio 3 não precisou isolar
explicitamente, mas que se torna necessária em `K` geral), `r` =
número das `K` fontes ainda não alcançadas. As regras de transição
exatas são derivadas uma única vez, para `K` geral, do mesmo fato
elementar de revelação-preguiçosa de permutação já usado no Estágio 3.
Resolver essa cadeia em forma fechada é então um **algoritmo
mecânico** (uma recursão linear de primeira ordem resolvida por uma
identidade padrão de telescopagem fatorial-decrescente/hockey-stick,
executada simbolicamente) — não uma nova análise de casos manual para
cada `K`.

**Resultado central — K=3, PROVADO incondicionalmente:**

```
ψ_n^{(3)} = 16/35 + 12/(35n) + 5/(28n²) + 3/(70n³)   (todo n≥4)
```

que pelo Lema da Redução A (Estágio 3, já provado geral em `K`) prova
`φ_n^{(3)} → φ_3 = 16/35` incondicionalmente. A taxa completa também
foi obtida do zero (não por interpolação/ajuste):

```
φ_n^{(3)} = 16/35 + 1/(14n) + 11/(10n²) + 23/(35n³) + 6/(35n⁴)   (todo n≥4)
```

— taxa `Θ(1/n)`, mesmo padrão já encontrado em `K=2` (Estágio 3), não
o `Θ(1/n²)` ingenuamente esperado a partir de `K=1`.

**Bônus — K=4, K=5, também PROVADOS.** Como o procedimento (não cada
resultado individual) é uniforme em `K`, subir mais dois degraus da
mesma escada mecânica produziu, sem nenhuma ideia nova, as formas
fechadas exatas para `ψ_n^{(4)}` e `ψ_n^{(5)}` — ambas verificadas.
Um padrão exato foi também observado (não provado) no coeficiente de
`1/n`: `lim n(ψ_n^{(K)}-φ_K) = Kφ_K/4`, confirmado exatamente para
`K=1,...,5` — reportado como **CONJECTURA para K geral**, não teorema
(a obstrução precisa para uma prova geral-em-K está nomeada em
`ATTEMPT.md` §7.3: seria necessária uma indução em `r` através da
solução por telescopagem, ou um argumento de função geradora em `K`,
nenhum dos dois tentado).

**Verificação, seis camadas independentes (`ATTEMPT.md` §6).** O
método reproduz exatamente as fórmulas já provadas de `K=1,2` do
Estágio 3, por uma derivação completamente diferente; `ψ_n^{(3)}` bate
com o log de força bruta do Estágio 3 (`n=4..8`); bate com um ponto de
força bruta NOVO e independente em `n=9` (nunca computado antes, 264,5
milhões de combinações exatas); bate com uma recursão direta
codificada independentemente (`markov_direct.py`, sem álgebra
simbólica); a fórmula recombinada `φ_n^{(3)}` bate com uma TERCEIRA
força bruta independente da média bruta da Definição 4 (`n=4..7`, sem
usar o Lema A ou a máquina de ponto único); 20/20 checagens
automatizadas passam.

**Verificação adversarial independente (`k3_attempt_2/adversarial/REFEREE_REPORT.md`,
`DISC-DEC-031`).** Um segundo agente, hostil, re-derivou o modelo e as
regras de transição do zero a partir das primitivas de revelação
preguiçosa (não lendo a prova antes de formar sua própria versão),
resolveu a recursão por uma técnica DIFERENTE (método do fator
integrante em vez da soma hockey-stick simbólica), substituiu as 7
formas fechadas de volta na recursão original (diferença simbólica =
0 em todo nível), recomputou `K=1,2` e confirmou contra as fórmulas já
provadas do Estágio 3, rodou sua própria força bruta do zero (detector
de ciclicidade próprio, testado unitariamente, algoritmo diferente do
da tentativa original) em `n=4..8`, verificou `φ_n^{(3)}` via uma
força bruta independente da média bruta (`n=4..7`, sem Lema A),
confirmou `K=4,5` em todo `(K,n)` citado, auditou overclaims (a
conjectura de taxa geral-K permanece rotulada CONJECTURADA em todo
lugar, nunca desliza para linguagem de prova), e reexecutou os
próprios scripts da tentativa original (incluindo a força bruta de
`n=9` de ~7,5 minutos, reproduzindo `3385/6804` de forma independente).
**Veredito: SOUND — nenhum erro encontrado em nenhuma camada.**

**K≥6: continua honestamente ABERTO.** A obstrução mudou de natureza
em relação ao Estágio 3: não é mais "análise de casos manual explode
combinatorialmente" (o procedimento já é uniforme em `K`) — é que a
recursão foi resolvida "em `r`" apenas numericamente, um nível de cada
vez (`r=0,...,5`), não simbolicamente para `r` geral. Uma prova
geral-em-K exigiria uma indução formal em `r` sobre a forma da solução
por telescopagem, ou um argumento de função geradora em `K` — nenhum
dos dois tentado neste documento, mas ambos nomeados como rotas
concretas plausíveis (diferente da obstrução do Estágio 3, que não
tinha rota candidata similar).

**Veredito honesto atualizado do documento inteiro (ao fim do Estágio
4):** Teorema 1 + corolários (Estágio 1); Lema 2 (Estágio 1);
Proposição 3 (Estágio 2); Proposição 4 = ponte exata K=0,1 (Estágio
2); ponte exata K=2, taxa completa (Estágio 3); **ponte exata K=3,4,5,
incluindo taxa completa para K=3 (Estágio 4, novo) — agora PROVADA,
não mais listada como faltante**. Resta como PROPOSIÇÃO CONDICIONAL
apenas a ponte geral para `K≥6` (Lema Aberto, agora estritamente mais
estreito do que "K≥3"), mais a conjectura de taxa geral-K (§7.2 de
`k3_attempt_2/ATTEMPT.md`, não provada). Conjecturas 1–2 (§8, texto
original) inalteradas. Fontes completas:
`../k2_open_lemma/k3_attempt_2/ATTEMPT.md`,
`../k2_open_lemma/k3_attempt_2/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 5 — 2026-08-22] Os casos K=6,...,10 do Lema Aberto: PROVADOS incondicionalmente; a conjectura de taxa geral-K: PROVADA, condicional a uma ressalva de regularidade precisamente nomeada

**Contexto.** O Estágio 4 (acima) provou `K=3,4,5` pelo método uniforme
de matriz de transferência, deixando `K≥6` honestamente aberto, e
observou (não provou) o padrão de taxa geral-`K`
`lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4`, nomeando duas rotas candidatas nunca
tentadas para fechá-lo: indução formal em `r` sobre a forma da solução
por telescopagem, ou um argumento de função geradora em `K`. Este
estágio despacha ambas as frentes autorizadas por `DISC-DEC-033`(a):
(A) subir a escada mecânica de `K=5` até `K=10` pelo método idêntico do
Estágio 4; (B) atacar a conjectura de taxa geral-`K` por uma via nova
— não uma das duas nomeadas literalmente, mas uma reformulação que
sidesteps a obstrução do Estágio 4 por outro caminho (ver abaixo).

### Parte A — `K=6,...,10`: PROVADOS incondicionalmente, mesmo método do Estágio 4

Subir mais cinco degraus da mesma escada mecânica (`k6_attempt/ATTEMPT.md`
§1) produz as formas fechadas exatas de `ψ_n^{(K)}` para `K=6,...,10`,
cada uma provando `φ_n^{(K)}→φ_K` (o Lema Aberto para aquele `K`) pelo
Lema da Redução A já provado (Estágio 3). Resultado central, `K=6`:

```
ψ_n^{(6)} = (2048n⁶+3072n⁵+4293n⁴+4638n³+3529n²+1662n+360)/(6006n⁶)
```

com limite `φ_6=1024/3003`. `K=7,8,9,10` seguem pelo mesmo procedimento
(formas fechadas completas em `ATTEMPT.md` §1.1), cada uma com o
limite `n→∞` batendo exatamente com a integral de Wallis `φ_K` e o
coeficiente de `1/n` batendo exatamente com `Kφ_K/4` — a conjectura de
taxa, agora confirmada **incondicionalmente** para `K=0,...,10` (11
valores consecutivos), diretamente das formas fechadas exatas, sem
nenhum argumento assintótico.

**Verificação adversarial independente
(`k6_attempt/adversarial/REFEREE_REPORT.md`).** Um referee hostil
separado re-executou `markov_transfer.build_levels(6)` e `(7)`
independentemente (não confiando no log da frente), substituiu **todas
as 13 formas fechadas em `K=6`** e **todas as 16 em `K=7`** de volta na
recursão exata original — diferença simbólica `=0` em cada uma —, e
escreveu uma força bruta própria, com estratégia de otimização
genuinamente diferente da frente (vetorização `numpy` sobre todo o
espaço de `U`-tuplas em vez de paralelização `multiprocessing` sobre
permutações), autotestada contra `K=1,2,3` já provados antes de ser
confiada em `K=6,n=7`: `355081/823543`, batendo bit a bit com a frente
e com a rederivação algébrica independente do referee — e, num segundo
ponto held-out independente rodado em segundo plano pelo próprio
referee, `K=6,n=8` (`10.569.646.080` combinações): `191647/458752`,
também batendo bit a bit. `K=7,8,9,10`
foram checados quanto a consistência interna (limite `=φ_K`,
coeficiente de `1/n` `=Kφ_K/4`), 8/8 confirmações exatas. **Veredito:
SOUND.**

**Dois erros encontrados e corrigidos por adendo datado (nenhum afeta
qualquer alegação PROVADA).** (1) Um erro aritmético cosmético na prosa
descritiva do tamanho do espaço de busca em `K=6,n=7`
(`592.912.960` deveria ser `592.950.960`) — achado pelo referee,
confirmado de três formas. (2) Um segundo erro do mesmo tipo em
`K=6,n=8` (`10.568.983.680` deveria ser `10.569.646.080`) — achado
pela sessão orquestradora durante a integração, confirmado por
multiplicação direta. (3) Um erro real, porém contido, na prosa: a
alegação de que o coeficiente de `1/n` da quantidade *recombinada*
`φ_n^{(6)}` é `512/1001` — o valor verdadeiro (confirmado por quatro
métodos independentes pelo referee) é `1093/6006`; a forma fechada em
si permanece correta, e nenhuma alegação PROVADA depende do valor
errado (a conjectura de taxa é sempre sobre `ψ_n^{(K)}`, nunca sobre
`φ_n^{(K)}` combinado, e permanece corretamente escopada em todo o
resto do documento). Todas as três correções aplicadas como blocos
datados `[Correção pós-adversarial, 2026-08-22]` em `k6_attempt/ATTEMPT.md`,
texto original preservado, nada reescrito silenciosamente.

### Parte B — a conjectura de taxa geral-`K`: PROVADA, condicional a uma ressalva de regularidade precisamente nomeada

**O método (novo, `k6_attempt/ATTEMPT.md` §2–§3).** Em vez de resolver
a recursão exata simbolicamente em `r` (a obstrução nomeada pelo
Estágio 4), este documento toma o limite de escala `n→∞` da MESMA
cadeia `(a,b,r)` **antes** de resolver — nesse ponto, `r` deixa de ser
um índice de somatório e vira um parâmetro livre de uma EDO linear de
primeira ordem, que pode ser resolvida honestamente para `r` simbólico.
Isso produz, para `r` simbólico geral: a forma fechada de ordem líder
`F_r(t,b)` (que rederiva a integral de Wallis `φ_K` por uma rota
inteiramente nova) e a correção de ordem `O(1/n)`, `G_r(t,b)` — ambas
provadas como identidades algébricas simbólicas exatas contra suas
respectivas EDOs (não ajuste de curva), e combinadas dando uma prova
completa de que a conjectura de taxa `lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` vale
para todo `K`, **modulo uma ressalva precisamente nomeada** (§4 de
`k6_attempt/ATTEMPT.md`): a *existência* da expansão assintótica de
duas parcelas assumida, para `r` além dos 11 valores concretamente
verificados (`K=0,...,10`, agora provados incondicionalmente pela Parte
A), não é rederivada independentemente de primeiros princípios.

**Verificação adversarial independente, incluindo o julgamento central
sobre o escopo da ressalva.** O mesmo referee hostil rederivou, do
zero e à mão (antes de ler como o documento deriva), ambas as EDOs, a
forma fechada de `F_r`/`c_k^{(r)}(b)`, a forma fechada de
`G_r`/`d_k^{(r)}(b)` (a checagem mais difícil, extraindo a recursão de
`G_r` de forma independente da EDO em vez de transcrever o script da
frente), e a identidade de soma binomial de §3.4 — **zero erros
encontrados** em qualquer etapa, para `r,k,b` simbólicos. O referee foi
além do que o documento verifica: identificou uma assimetria
substantiva não nomeada originalmente (o argumento de limitação que
força a solução particular correta é rigoroso para `F_r`, já que
`g_r(m,b)∈[0,1]` é uma probabilidade genuína; não há argumento análogo
para `G_r`, um termo de correção sem cota a priori) e então testou essa
assimetria diretamente — algo que o documento nunca fazia — checando
`F_r` e `G_r` contra os dados exatos em `t≠1` (45 pontos novos,
`r=0,...,5`, `b` simbólico geral): **zero discrepâncias encontradas**,
evidência nova e não-circular a favor do ansatz na faixa verificável,
não apenas reconfirmação de álgebra já provada.

**Julgamento explícito e central do referee, adotado integralmente por
esta integração: a ressalva está corretamente dimensionada — nem
otimista demais, nem conservadora demais.** Não há base para
reclassificar os resultados de `F_r`/`G_r`/taxa-geral-`K` como
incondicionais, nem para tratar a lacuna de existência como mais séria
do que o próprio §4 já a trata. Dois defeitos de documentação
adicionais (três referências pendentes a uma "§2.4" que nunca fora
escrita; duas linhas do Scorecard rotuladas `PROVED` sem o qualificador
que a linha irmã já carregava) foram corrigidos: `§2.4` foi escrita
como um adendo datado usando exatamente o raciocínio verificado do
referee (o argumento de limitação para `F_r`, a assimetria nomeada para
`G_r`, os 45 pontos de teste empírico), e as duas linhas do Scorecard
receberam nota de correção apontando para o mesmo qualificador da linha
7. Nenhuma dessas correções muda qual resultado é catalogado como
incondicional vs. condicional — apenas torna a fronteira, já
corretamente traçada pelo documento, também consistente em toda a sua
prosa.

**O que isto muda, precisamente, no status do Lema Aberto e da
conjectura de taxa.** Antes deste estágio (fim do Estágio 4): Lema
Aberto provado incondicionalmente para `K=0,...,5`; `K≥6` sem rota de
prova nomeada; conjectura de taxa verificada (não provada) para
`K=1,...,5`. Depois deste estágio: **Lema Aberto provado
incondicionalmente para `K=0,...,10`** (Parte A); para `K≥11`, existe
agora — pela primeira vez — uma rota de prova completa e
adversarialmente verificada como SOUND em cada etapa algébrica, mas que
permanece **explicitamente condicional** à ressalva de regularidade de
§4 (Parte B) — um progresso epistêmico real (de "nenhuma rota nomeada"
para "prova condicional verificada, com a única lacuna restante
precisamente nomeada, delimitada, e testada empiricamente sem nenhuma
evidência contrária encontrada"), mas **não** um fechamento
incondicional do Lema Aberto para `K` geral. A conjectura de taxa segue
o mesmo padrão: **incondicional para `K=0,...,10`**, **PROVADA, modulo a
ressalva de §4, para `K` geral**.

**Por que os dois compartilham exatamente o mesmo status condicional
(não é uma coincidência de rotulagem).** Um limite finito
`lim_n n(ψ_n^{(K)}-φ_K)` força elementarmente `ψ_n^{(K)}-φ_K→0` (se a
diferença não se anulasse, multiplicar por `n→∞` não poderia convergir a
um valor finito). Logo a prova condicional da taxa (Parte B), exatamente
como enunciada, já descarrega condicionalmente o Lema Aberto em si —
como corolário imediato, não como um fato estabelecido separadamente —
sob a mesma ressalva de §4. É por isso que nenhum dos dois é fechado
incondicionalmente para `K≥11`, mas também nenhum dos dois fica "mais
aberto" que o outro: ambos repousam sobre a idêntica, única, hipótese
precisamente nomeada, com o mesmo status — provados condicionalmente,
abertos incondicionalmente.

**O que permanece honestamente aberto.** (i) A forma fechada exata,
todas-as-ordens, geral-`K`, para `ψ_n^{(K)}` (não apenas seu limite e
sua taxa) — nunca tentada além da escada concreta (§6.2 de
`k6_attempt/ATTEMPT.md`). (ii) A existência da expansão assintótica de
duas parcelas para `r` além de `K=10` — a ressalva de §4, agora com
evidência empírica adicional a favor (o teste em `t≠1` do referee) mas
sem prova de primeiros princípios. (iii) Duas rotas tentadas e
abandonadas honestamente e registradas (§6.1, §6.3 de
`k6_attempt/ATTEMPT.md`): soma de função geradora em `K` sobre a
recursão *exata* (obstrução estrutural nomeada antes de codificar);
soma simbólica direta via `sympy.summation` na identidade final (não
termina — o referee tentou independentemente uma segunda via
automatizada, o algoritmo de Gosper, que também retorna sem fechamento,
corroborando que a prova à mão do documento é genuinamente necessária,
não um atalho por preguiça).

**Veredito honesto atualizado do documento inteiro (ao fim do Estágio
5):** Teorema 1 + corolários, Lema 2 (Estágio 1); Proposição 3,
Proposição 4 = ponte exata K=0,1 (Estágio 2); ponte exata K=2, taxa
completa (Estágio 3); ponte exata K=3,4,5, taxa completa para K=3
(Estágio 4); **ponte exata K=6,...,10, incluindo taxa incondicional
para K=0,...,10 (Estágio 5, Parte A) — agora PROVADA**; **conjectura de
taxa geral-K PROVADA, explicitamente condicional à ressalva de
regularidade de §4 (Estágio 5, Parte B, novo) — não mais uma conjectura
sem rota de prova, mas também não um teorema incondicional**. Resta
como PROPOSIÇÃO ABERTA apenas a forma fechada exata geral-`K`
(todas-as-ordens) e a existência da expansão assintótica para `r>10`
(a ressalva de §4). Conjecturas 1–2 (§8, texto original) inalteradas.
Fontes completas: `../k2_open_lemma/k3_attempt_2/k6_attempt/ATTEMPT.md`,
`../k2_open_lemma/k3_attempt_2/k6_attempt/adversarial/REFEREE_REPORT.md`.

**[Ver Estágio 6 abaixo — este veredito foi superado: a ressalva de
regularidade da Parte B foi fechada, onda 8 frente (b), DISC-DEC-040,
2026-08-22. O Lema Aberto geral-`K` e a conjectura de taxa geral-`K`
tornam-se incondicionais para todo `K`, e Proposição Condicional 5
torna-se Teorema 3.]**

---

## [Extensão, Estágio 6 — 2026-08-22] O Lema Aberto geral-`K`: PROVADO INCONDICIONALMENTE para todo `K`; Proposição Condicional 5 → Teorema 3

**Contexto.** O Estágio 5, Parte B, provou a conjectura de taxa geral-`K`
e, como corolário imediato, o próprio Lema Aberto geral-`K`, mas
**condicional** a uma ressalva de regularidade precisamente nomeada
(§4 de `k6_attempt/ATTEMPT.md`): a existência, para `r` além dos 11
valores concretamente verificados (`K=0,\dots,10`), da expansão
assintótica de duas parcelas `g_r(m,b)=F_r(t,b)+\frac1nG_r(t,b)+O(1/n^2)`
assumida pela derivação. `DISC-DEC-038` autorizou, como frente (b) da
onda 8, uma tentativa dedicada de fechar exatamente essa ressalva — a
única peça que separava Proposição Condicional 5 (§7.5) de um Teorema 3
incondicional.

### O fechamento

`k_general_existence_attempt/ATTEMPT.md` prova a existência dessa
expansão, **para todo `r\ge0` e `b\ge0`**, por indução em `r` cujo passo
indutivo é um limitante de Gronwall discreto **exato** — não uma
estimativa assintótica — sobre a recursão discreta exata já provada
(`../../ATTEMPT.md` §2). Os elementos centrais da prova:

1. **Substituição do ansatz de dois termos na recursão exata**, dando
   uma identidade exata (não aproximada) para o resíduo `R_r(m):=
   g_r(m,b)-F_r(t,b)-\frac1nG_r(t,b)`. A expansão de Taylor dos
   polinômios de grau finito envolvidos é **livre de resto** (identidade
   algébrica, não estimativa `O(h^{r+1})`), já que um polinômio de grau
   `d` tem exatamente `d{+}1` termos de Taylor e resto exatamente `0`.
2. Os colchetes de ordem `h^0` e `h^1` da substituição **anulam-se
   identicamente em `t`** (não apenas assintoticamente), porque são
   exatamente as EDOs já provadas do Estágio 5 Parte B (`F_r,G_r` já
   satisfazem essas EDOs por construção) — logo nenhum tratamento
   separado de camada-limite é necessário, mesmo no caso-base.
3. **O coeficiente de contração da recursão do resíduo é exatamente
   ZERO no próprio caso-base** `m=b{+}r{+}1` — um fato algébrico real
   sobre a recursão *já provada* de wave 6 (`(m{-}1{-}r{-}b)/m=0` em
   `m=b{+}r{+}1`), não uma suposição nova. Isso subsome automaticamente
   o caso-base no mesmo limitante, sem caso especial.
4. **Fechamento via a mesma identidade de falling-factorial/hockey-stick**
   que a onda anterior usou para RESOLVER a recursão (`../../ATTEMPT.md`
   §3), agora reaproveitada para LIMITÁ-la — dando um limitante uniforme
   `|R_r(m,b,n)|\le D_r(b)/n^2` **sem nenhum fator espúrio `\log n`** (um
   union bound ingênuo produziria um, como o documento demonstra
   explicitamente construindo-o e comparando).
5. O passo análogo para `h_r` (o "outro lado" da recursão acoplada) é
   pura substituição algébrica, sem Gronwall adicional, porque `h_r` não
   é uma cadeia em `a`.

### Verificação adversarial independente

Um referee hostil dedicado (modelo com maior capacidade de raciocínio,
dado o peso da alegação) rederivou os seis itens centrais **do zero**
— simulador próprio, formas fechadas próprias, recursão coeficiente-a-
coeficiente extraída independentemente da EDO — **antes** de ler como o
documento-alvo os deriva, e leu o próprio documento e seus scripts
apenas depois de ter seus próprios resultados prontos. Verificou a
identidade do resíduo como identidade racional exata em **477 pontos
concretos, 0 divergências**; a identidade de `h_r` em **309 pontos, 0
divergências**; os Fatos 2 e 3 (as EDOs) para `r,k,b` **simbólicos**
via formas fechadas em função gama, **0 divergências em 1200 triplas**;
a identidade de falling-factorial/hockey-stick simbolicamente e em
**4764+429+429 casos concretos, 0 divergências**. Rodou numérica nova
em combinações que o documento-alvo nunca testou (`r=6,7,9,10`;
`b=2,3,5`; `n` até `10^6`; varreduras exaustivas, não amostradas) —
convergência limpa em toda parte, nenhum crescimento `\log n`, nenhuma
explosão de camada-limite. Fez duas **predições próprias** a partir de
sua rederivação — não apenas checou as do documento — e confirmou
ambas exatamente: `R_1\equiv0` para todo `m,b,n` (485 avaliações, 0
resíduos não-nulos) e `R_2(m,0,n)=1/(15n^2)` para todo `m`, não apenas
no caso-base (220 avaliações, 0 desvios).

> **Veredito: SOUND — WITH NAMED ISSUES.** "O Teorema-Alvo está
> genuinamente estabelecido. Ataquei cada passo e não consegui quebrar
> nenhum deles." Quatro questões nomeadas, nenhuma fatal:

- **I-1 (exigia correção).** O expoente exibido na justificativa
  escrita do limitante de §4 do documento-alvo estava trocado
  (`h^{j-1}` em vez de `h^j`), o que, tomado literalmente, só
  estabeleceria `O(1/n)`, não `O(1/n^2)` — um erro de digitação na
  linha mais central da prova, não um erro conceitual: o fato correto
  foi verificado independentemente pelo referee (simbolicamente, `b`
  simbólico, `r=0,\dots,8`) e §3 do próprio documento já enunciava o
  fato certo em prosa. **Corrigido** via adendo datado em
  `k_general_existence_attempt/ATTEMPT.md` §4, texto original
  preservado.
- **I-2 (nota, sem consequência matemática).** Um ponto fora-de-domínio
  não mencionado em §6, cujo coeficiente é exatamente `0` — inofensivo,
  mesmo mecanismo que §3 já usa e explica para `g_r`. Anotado via
  adendo.
- **I-3 (cosmético).** Algumas descrições da evidência numérica em §7 /
  no resumo executivo são mais otimistas que os logs retidos (ex.
  "entire range" descreve na verdade uma amostra log-espaçada). O
  referee re-executou as versões exaustivas por conta própria e
  confirmou os mesmos resultados qualitativos — nenhuma alegação
  numerada afetada. Anotado via adendo.
- **I-4 (a jusante, a que importa para a catalogação).** O documento
  PAI (`k6_attempt/ATTEMPT.md` §5/Scorecard linha 9) carregava a mesma
  ressalva sobre a alegação `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)`
  **para todo `K\ge1`** — mas essa alegação é **FALSA em `K=1`**
  (`\varphi_n^{(1)}-\varphi_1=1/(3n^2)` exatamente, já registrado
  alhures neste documento). Promover essa linha verbatim a incondicional
  converteria uma afirmação condicional falsa em incondicional falsa —
  não é erro do documento-alvo (a ressalva de §4 já cobria essa linha
  corretamente enquanto condicional), mas passa a importar agora que a
  ressalva fecha. **Corrigido** em `k6_attempt/ATTEMPT.md` §5 e no
  Scorecard (adendos datados): a afirmação certa, agora incondicional,
  é o coeficiente exato
  `\varphi_n^{(K)}-\varphi_K=K[\varphi_K/4+F_{K-1}(1,1)-\varphi_K]/n+O(1/n^2)`
  — zero em `K=1`, positivo verificado para `2\le K\le12`
  (reproduzindo `1/30` em `K=2` e `1/14` em `K=3`, já conhecidos de
  ondas anteriores por vias independentes, e `1093/6006` em `K=6`,
  exatamente o valor já confirmado por quatro métodos distintos na
  correção pós-adversarial do Estágio 5 — uma **quinta** confirmação
  independente, por uma rota completamente diferente).

Ver `k_general_existence_attempt/adversarial/REFEREE_REPORT.md` para o
relatório completo (9 scripts independentes, milhares de verificações
exatas).

### O que isto muda, precisamente

**1. A ressalva de regularidade de `k6_attempt/ATTEMPT.md` §4 está
FECHADA.** As formas fechadas gerais-`r` `F_r,G_r` (Estágio 5 Parte B)
e a conjectura de taxa geral-`K` deixam de ser condicionais.

**2. O Lema Aberto de §7.4 (acima) está agora PROVADO PARA TODO
`K\ge0`, não apenas `K=0,\dots,10`.** `ψ_n^{(K)}=g_K(n,0)` é a instância
`t=1` do Teorema-Alvo geral-`r` — logo `ψ_n^{(K)}\to F_K(1,0)=φ_K` para
todo `K`; combinado com o Lema da Redução A (§7.2/Estágio 3, PROVADO,
`K` geral), `φ_n^{(K)}\to φ_K` para todo `K` fixo. O texto original de
§7.4 ("*Status:* neither proved nor disproved in this document")
permanece preservado como registro histórico do estado do documento
antes deste estágio — este parágrafo é a atualização autorizada de seu
status.

**3. A conjectura de taxa geral-`K` está agora INCONDICIONAL:**
`\displaystyle\lim_{n\to\infty}n\big(\psi_n^{(K)}-\varphi_K\big)=\frac{K\varphi_K}4`
para todo `K\ge0` (não mais "modulo a ressalva de §4" como no Estágio 5
Parte B).

**4. §9, item 2 (a taxa do `\varphi_n^{(K)}-\varphi_K` para `K\ge2`,
"fully open" no texto original) está agora respondido com precisão —
mas não completamente fechado.** A fórmula exata do coeficiente de
`1/n`, `K[\varphi_K/4+F_{K-1}(1,1)-\varphi_K]`, é agora PROVADA
incondicional para todo `K\ge1` (corolário direto do item 2 acima mais
a Lemma de Redução A). Isso já responde a pergunta original de "que
ordem é a taxa": nunca pior que `O(1/n)`, nunca `\Theta(\log n/n^2)`.
Mas se esse coeficiente é **estritamente positivo para todo `K\ge2`**
(o que tornaria a taxa exatamente `\Theta(1/n)`, não apenas `O(1/n)`)
foi **verificado, não provado**, para `2\le K\le12` — permanece
genuinamente aberto se a positividade vale para todo `K`, um item novo,
mais estreito, substituindo o item 2 original.

**5. Proposição Condicional 5 (§7.5) torna-se um teorema incondicional.**
A Proposição 3 (§7.2) já era incondicionalmente provada; com o Lema
Aberto agora provado para todo `K\ge0` (item 2 acima), a hipótese que
Proposição Condicional 5 carregava deixa de existir. O enunciado
completo:

> **Teorema 3 (antes Proposição Condicional 5).** Para todo `c\ge0`
> fixo, `\displaystyle\varphi(n,c)\to\varphi_\infty(c)=\int_0^1e^{-ct^2}dt`
> quando `n\to\infty` — **incondicionalmente**, sem nenhuma hipótese
> não provada.

Este é exatamente o enunciado que o resumo executivo do topo deste
documento (e `PROOF_DEPENDENCY_MAP.md`, Árvore A) já citava como o que
resultaria "se a Frente (b) fechasse" — ela fechou.

**O que permanece genuinamente aberto, sem mudança nenhuma por este
estágio:** (i) a forma fechada exata, todas-as-ordens, geral-`K`, para
`\psi_n^{(K)}` (§6.2 de `k6_attempt/ATTEMPT.md` — separada, mais dura,
não tocada por este fechamento); (ii) a taxa de crescimento em `r` das
constantes de erro `D_r(b),C_r(b)` do novo documento (nomeada, não
perseguida — os números observados são muito menores que os limitantes,
ex. `0,78` observado contra `174` de limitante em `r=6`, mas nenhuma
forma fechada para o crescimento foi buscada); (iii) a positividade do
coeficiente de taxa para `K\ge13` (item 4 acima); (iv) a versão
localmente-uniforme-em-`c` do Teorema 3 (§9 item 4 original — nunca
tocada por nada neste estágio, gap genuinamente independente);
(v) Conjecturas 1–2 (§8, a lei distribucional completa) — inalteradas,
gap genuinamente separado de tudo que fechou aqui. Nenhum destes é
afetado, positiva ou negativamente, pelo fechamento acima.

**Veredito honesto atualizado do documento inteiro (ao fim do Estágio
6):** Teorema 1 + corolários, Lema 2 (Estágio 1); Proposição 3, ponte
exata `K=0,1` (Estágio 2); ponte exata `K=2` (Estágio 3); ponte exata
`K=3,4,5` (Estágio 4); ponte exata `K=6,\dots,10` (Estágio 5 Parte A);
**Lema Aberto geral-`K` e conjectura de taxa geral-`K`, agora PROVADOS
INCONDICIONALMENTE para todo `K\ge0` (Estágio 6, novo)**; **Proposição
Condicional 5 promovida a Teorema 3, incondicional (Estágio 6, novo)**.
Restam abertos: a forma fechada todas-as-ordens geral-`K`; a
positividade do coeficiente de taxa para `K\ge13`; a versão
uniforme-em-`c`; a lei distribucional completa (Conjecturas 1–2).
Fontes completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/ATTEMPT.md`,
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/adversarial/REFEREE_REPORT.md`.

**[Ver Estágio 7 abaixo — o item (iii) desta lista ("positividade do
coeficiente de taxa para `K≥13`") foi fechado: PROVADO para todo
`K≥2`, onda 9 frente (b), DISC-DEC-042, 2026-08-22.]**

---

## [Extensão, Estágio 7 — 2026-08-22] O coeficiente de taxa `c_K` é estritamente positivo para todo `K≥2`: a taxa é exatamente `Θ(1/n)`, não apenas `O(1/n)`

**Contexto.** O Estágio 6 provou o coeficiente exato de `1/n` de
`φ_n^{(K)}-φ_K`, incondicionalmente para todo `K≥1`:

`c_K := K[φ_K/4 + F_{K-1}(1,1) - φ_K]`,

com `c_1=0` (consistente com a taxa `Θ(1/n²)` já provada em `K=1`) e
`c_K` verificado — não provado — estritamente positivo para
`2≤K≤12`. Se `c_K>0` para todo `K≥13` permanecia honestamente aberto,
nomeado como o item (iii) da lista "o que permanece aberto" do Estágio
6. `DISC-DEC-041` autorizou, como frente (b) da onda 9, uma tentativa
dedicada de fechar exatamente essa questão.

### O fechamento

`k_general_existence_attempt/rate_coefficient_positivity_attempt/ATTEMPT.md`
prova `c_K>0` para todo `K≥2` — não apenas estende a verificação
numérica, mas fecha a questão por prova elementar, não-assintótica. A
ideia central: a expressão de dois ingredientes `c_K` colapsa para um
único ingrediente, a própria integral de Wallis. Especificamente:

> **Lema 1 (PROVADO, novo — fato autônomo, companheiro de
> `F_r(1,0)=φ_r` já registrado em `k6_attempt/ATTEMPT.md` §2.3):**
> `F_{K-1}(1,1) = [(2K+1)φ_K - 1]/(2K)`.

Substituindo no coeficiente `c_K`:

> **Teorema A (PROVADO):** `c_K = [(K+2)φ_K - 2]/4`.

Logo `c_K>0 ⟺ (K+2)φ_K>2`, com **igualdade exata em `K=1`**
(`v_1:=3φ_1=2`) — explicando estruturalmente, não apenas
observacionalmente, por que `c_1=0` (a mesma degenerescência que o
referee da onda 8 nomeou como issue I-4). Como
`φ_{K+1}/φ_K=(2K+2)/(2K+3)` exatamente, a sequência
`v_K:=(K+2)φ_K` satisfaz `v_{K+1}/v_K-1=K/[(K+2)(2K+3)]>0` para
`K≥1` — uma única cancelação algébrica (`2(K+1)(K+3)-(K+2)(2K+3)=K`)
— logo `v_K` é estritamente crescente a partir de `v_1=2`, dando
`v_K>2`, i.e. `c_K>0`, para todo `K≥2`. Telescopando o incremento dá
a forma mais afiada do resultado, em que a positividade não é uma
desigualdade a provar, mas uma propriedade visível da expressão:

> **Corolário B′ (PROVADO):** `c_K = ¼ Σ_{j=1}^{K-1} j·φ_j/(2j+3)`
> — uma soma de termos estritamente positivos, vazia (logo `0`)
> exatamente em `K=1`.

Uma segunda prova independente, via a desigualdade clássica
`C(2K,K)≤4^K/√(3K+1)` (re-provada pelo mesmo documento), reproduz o
resultado por uma cancelação distinta (`3K²(K-1)>0` para `K≥2`).

### Verificação adversarial independente

Um referee hostil dedicado rederivou cada item **do zero** — mão e
código próprio — **antes** de ler o documento-alvo: o Lema 1 por
quatro rotas numéricas independentes concordando exatamente
(`K=1..50`); a identidade de cauda binomial re-derivada do teorema
binomial + simetria de linha; a cancelação central `2(K+1)(K+3)-
(K+2)(2K+3)=K` e a âncora `v_1=2` verificadas simbolicamente; a
indução checada por uma **indução literal em código**, partindo só da
âncora `v=2` e aplicando somente a razão, `K=1..1500`, sem tocar
`φ_K` de novo; a soma telescópica reproduzindo o exemplo trabalhado
`c_4=23/210`; todas as 85 células da tabela do documento recomputadas
independentemente (0 células erradas); `c_K` calculado da definição
crua (não da forma colapsada) para `K` até `5000`, e uma varredura
exaustiva `K=0,...,3000` confirmando que o conjunto-solução da
igualdade exata `(K+2)φ_K=2` é precisamente `{0,1}` — nenhum outro
`K`. Reconfirmação independente do lado finito-`n`: uma reimplementação
própria, do zero, da recursão exata `(a,b,r)` mais o Lema da Redução A,
extraindo `α_1=c_K` exatamente para `K=1,...,9` por ajuste polinomial
exato em `1/n` validado fora-da-amostra — e o referee foi além,
**predizendo por conta própria** os coeficientes em `K=10,11,12`
(`200965/646646`, `106135/312018`, `1779879/4828850`) antes de
computá-los, confirmados exatamente. `c_6=1093/6006` fica agora
confirmado por uma **sexta** via independente neste arquivo.

> **Veredito: SOUND.** "Ataquei cada passo do argumento, rederivei
> independentemente cada identidade que sustenta o argumento antes de
> ler como o documento a deriva, escrevi cada script de verificação do
> zero, e não encontrei nenhum erro de nenhum tipo em nenhuma alegação
> numerada." Zero discrepâncias, zero contraexemplos, zero tentativas de
> quebra bem-sucedidas — o primeiro documento desta linha em que o
> referee não encontrou nada que exigisse correção. Quatro notas
> presentacionais (N-1 a N-4) foram registradas, nenhuma um erro,
> nenhuma exigindo correção: uma cláusula omitida mas trivial (`v_K>0`,
> suprida pela própria indução); a palavra "independente" na segunda
> prova é melhor lida como "uma segunda rota" (ambas as cancelações
> reduzem à mesma recursão de Wallis subjacente); `K=0` também é caso de
> igualdade exata (inofensivo, já antecipado pelo próprio documento); o
> cabeçalho "todos PROVADOS" de §5 é ligeiramente mais forte que a
> redação mais cuidadosa do Scorecard, que é a que deve valer.

Ver
`k_general_existence_attempt/rate_coefficient_positivity_attempt/adversarial/REFEREE_REPORT.md`
para o relatório completo.

### O que isto muda, precisamente

**O item (iii) da lista "o que permanece aberto" do Estágio 6 está
FECHADO, afirmativamente, para todo `K≥2` uniformemente.** O
enunciado a registrar:

> **Teorema (taxa exata, todo `K≥1`).** Para todo `K` fixo, `K≥2`:
> `\displaystyle\lim_{n\to\infty}n(φ_n^{(K)}-φ_K) = c_K =
> \frac{(K+2)φ_K-2}4 = \frac14\sum_{j=1}^{K-1}\frac{jφ_j}{2j+3} > 0`,
> logo `φ_n^{(K)}-φ_K=Θ(1/n)` — **não apenas `O(1/n)`**. Em `K=1`,
> `c_1=0` e `φ_n^{(1)}-φ_1=1/(3n²)` exatamente (fato a montante,
> Estágio 3), logo a taxa ali é `Θ(1/n²)`. Juntos, estes dois fatos
> determinam a taxa de ordem líder de `φ_n^{(K)}→φ_K` para **todo**
> `K≥1`.

**Cautelas de redação (herdadas do próprio referee, que nomeou
precisamente o mesmo tipo de deslize de quantificador que causou a
issue I-4 da onda 8):** nunca escrever "`c_K>0` para todo `K≥1`" —
`K=1` é caso de igualdade EXATA, não uma aproximação, e `K=0`
igualmente; manter sempre "para todo `K` **fixo**, `K≥2`" na afirmação
`Θ(1/n)` — nenhuma uniformidade em `K` é provada ou alegada.

**Corolários adicionais (todos PROVADOS):** `c_K` é estritamente
crescente em `K` (`K≥1`), logo `c_K≥c_2=1/30` para todo `K≥2` (piso
positivo uniforme); `c_K=√(πK)/8 - 1/2 + O(K^{-1/2}) → ∞` (dado o
desenvolvimento clássico de Wallis-Stirling, re-derivado
independentemente pelo referee a precisão de 60 dígitos até
`K=10^7`, concordando a 7 algarismos significativos).

**O que permanece aberto, sem mudança:** os outros quatro itens do
Estágio 6 — (i) forma fechada exata todas-as-ordens geral-`K`; (ii)
taxa de crescimento em `r` das constantes de erro `D_r(b),C_r(b)`;
(iv) versão localmente-uniforme-em-`c` do Teorema 3; (v) Conjecturas
1–2 (lei distribucional completa) — nenhum tocado por este
fechamento. **O Teorema 3 em si é inteiramente inafetado** — nunca
dependeu desta frente.

**Veredito honesto atualizado do documento inteiro (ao fim do Estágio
7):** tudo do Estágio 6, mais **a taxa exata de `φ_n^{(K)}→φ_K` agora
completamente determinada em ordem líder para todo `K≥1`** (Estágio
7, novo): `Θ(1/n²)` em `K=1`, `Θ(1/n)` para todo `K≥2`, com
coeficiente exato e crescente `c_K`. Restam abertos: forma fechada
todas-as-ordens geral-`K`; taxa de crescimento das constantes de erro
em `r`; versão uniforme-em-`c` do Teorema 3; Conjecturas 1–2. Fontes
completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/rate_coefficient_positivity_attempt/ATTEMPT.md`,
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/rate_coefficient_positivity_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 8 — 2026-08-23]

**Onda 10, frente (b), `DISC-DEC-045`/`DISC-DEC-046`
(`K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT`).** Alvo: item **(ii)** da
lista "o que permanece aberto" do Estágio 6/7 — a taxa de crescimento
em `r` das constantes de erro `D_r(b),C_r(b)` da prova de existência
geral-`K` (Estágio 6), nomeada mas não perseguida ali, com a folga
observada entre limitante provado e valor real já flagrante (`0,78`
observado contra `174` de limitante em `r=6`).

### O que foi provado

Estendendo o mesmo `ε`-matching que produziu `F_r` (ordem `1`) e `G_r`
(ordem `1/n`) mais uma ordem, obtém-se o par `(H_r,L_r)` (ordem
`1/n²`), com `H_r(t,b)` em forma fechada exata:

> **Teorema 1:** `\displaystyle H_r(t,b) =
> \sum_{k=0}^{r-2}\frac{(3k+8)(k+1)(k+2)(k+3)}{24}\cdot\frac{r!}{(r-k-2)!}\cdot\frac{t^k}{\prod_{i=1}^{k+3}(r+b+i)}`,
> todo coeficiente positivo, logo `\max_{[0,1]}|H_r|=H_r(1,b)=:D^*_r(b)`
> a todo `n` (grade inclui `t=1` sempre — nenhum argumento de
> densidade necessário).

O resíduo de três termos existe e é `O(1/n^3)` uniformemente (mesmo
argumento discreto-Gronwall do Estágio 6/7, uma ordem acima — o único
insumo novo é o bracket de ordem `h^2` anular-se, que **é** a EDO de
`H_r`), logo `D^*_r(b)=\lim_n\max_m n^2|R_r|` de fato. Em `b=0`:

> **Teorema 3:** `\displaystyle D^*_r(0) = \frac{r(3r+1)}{32}\varphi_r
> - \frac r{12}` exatamente, `\varphi_r=4^r(r!)^2/(2r{+}1)!`.
> `D^*_0(0)=D^*_1(0)=0` exatamente — a razão estrutural de `R_1≡0`
> (mesmo sabor de degenerescência de `c_1=0` no Estágio 7).

Para `b≥1`, o referee hostil desta frente derivou uma forma fechada
exata **para todo `b`** (Teorema 3′, não reproduzida aqui por
extensão — ver `adversarial/REFEREE_REPORT.md` Parte 3.3), da qual
segue algebricamente, sem estimativa assintótica:

> **Teorema 4 (taxa de crescimento, corrigido, todo `b` fixo):**
> `\displaystyle D^*_r(b) = \frac{3\sqrt\pi}{64}r^{3/2} -
> \frac{(3b{+}2)r}{24} + \frac{\sqrt\pi}{48}\Big[\tfrac{45}{16}\beta^2
> -\tfrac{15}{16}\beta-\tfrac{63}{32}\Big]r^{1/2} + O(1)`, `\beta:=b{+}1`
> — em particular `D^*_r(b)=\Theta(r^{3/2})` com constante líder
> `3\sqrt\pi/64=0{,}0830837742611961\ldots`, **a mesma para todo `b`
> fixo, agora PROVADA incondicionalmente** (não apenas
> "PROVED-MODULO" — item (ii) do Estágio 6/7 estava certo em desconfiar
> que faltava rigor ali, e o referee fechou exatamente esse buraco).

O limitante já publicado (Estágio 6) é, em contraste, **fatorial**:
`D_r(b),C_r(b)` crescem com `D_r/D_{r-1}\approx r`
(`7{,}1\times10^{30}` contra o valor real `11{,}13` em `r=30`). A
folga decompõe-se em dois mecanismos localizados e separadamente
tratáveis: um fator `1/n` descartado no §6 do documento de existência
geral-`K`, corrigível por uma mudança de uma linha usando a própria
hipótese padrão `n≥b{+}r{+}1` do teorema, tornando o limitante
geométrico em vez de fatorial (**Proposição 6, PROVADA e rigorosa**,
taxa medida `≈1{,}24` em `r=45`); e um custo de norma-soma-de-coeficientes
de `Θ((9/8)^r)` (**Lema 7, PROVADO**), não removido.

### Correção pós-adversarial nos termos subordinados

O referee hostil desta frente (agente independente, re-derivação
completa do zero — próprio `ε`-matching, próprio simulador, próprias
identidades binomiais — antes de ler o documento-alvo) confirmou **sem
ressalva** o núcleo inteiro: a EDO de `H_r`, a relação `L_r`, o
Teorema 1, o Teorema 2 (existência de três termos), o Teorema 3, os
Corolários 1a/2a/3a, o Lema 7 e a Proposição 6 — todos re-derivados
independentemente e reproduzidos exatamente (milhares de checagens
exatas, `0` divergências; ver `adversarial/REFEREE_REPORT.md` Partes
1–5). Mas encontrou **dois erros reais nos termos subordinados do
Teorema 4 conforme originalmente publicados** neste documento: o
coeficiente do termo `r^{1/2}` a `b=0` estava com sinal e magnitude
errados (`+\sqrt\pi/128` publicado; correto `-\sqrt\pi/512` — os
próprios números do documento já refutavam o sinal publicado), e o
termo linear a `b≥1` fora tratado como `b`-independente (`-r/12`)
quando na verdade é `-(3b{+}2)r/24`, um erro `Θ(br)`. **A conclusão
`Θ(r^{3/2})` com constante líder `3\sqrt\pi/64` sobrevive intacta e é
agora, graças à forma fechada geral-`b` do próprio referee, PROVADA
sem condição** — o enunciado acima já incorpora as duas correções.
Ambas foram verificadas de forma independente pela sessão
orquestradora (soma vetorizada em ponto flutuante da fórmula do
Teorema 1, `r` até `2\times10^7`) antes da integração. Correções
datadas equivalentes foram registradas no próprio
`error_constant_growth_attempt/ATTEMPT.md`.

### O que isto muda, precisamente

**O item (ii) da lista "o que permanece aberto" do Estágio 6/7 está
FECHADO.** A taxa de crescimento em `r` das constantes de erro tem
agora forma fechada exata a `b=0` e todo `b`, taxa assintótica exata
`Θ(r^{3/2})` com constante líder `b`-independente provada
incondicionalmente, e a origem precisa da folga entre o limitante
publicado (fatorial) e o valor verdadeiro está identificada em dois
mecanismos nomeados, um deles corrigido rigorosamente (Proposição 6).

**O que permanece aberto, sem mudança:** os demais itens do Estágio
6/7 — (i) forma fechada exata todas-as-ordens geral-`K`; (iv) versão
uniforme-em-`c` do Teorema 3; (v) Conjecturas 1–2 — mais, dentro do
escopo desta própria frente: um limitante rigoroso polinomial-em-`r`
(a Proposição 6 chega a geométrico, não polinomial — dois obstáculos
nomeados no próprio documento); se `S_r(b)/D^*_r(b)` é limitado
(caracterizado numericamente como crescente até `r=150`, não provado
limitado); a taxa exata do limitante melhorado `D'_r(b)` (medida
`≈1{,}24` decrescendo, convergência para `9/8` plausível não provada).
**O Teorema 3 (Estágio 6) permanece inteiramente inafetado** — nunca
dependeu desta frente.

**Veredito honesto atualizado (ao fim do Estágio 8):** tudo do Estágio
6/7, mais **a taxa exata de crescimento das constantes de erro
`D_r(b),C_r(b)` agora completamente determinada**: forma fechada em
`b=0` e geral-`b`, `Θ(r^{3/2})` provado incondicionalmente para todo
`b` fixo, com os dois erros do Teorema 4 originalmente publicado
corrigidos por verificação adversarial. Fontes completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/ATTEMPT.md`,
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 9 — 2026-08-23]

**Onda 11, frente (b), `DISC-DEC-047`/`DISC-DEC-048`
(`ALL-ORDERS-CLOSED-FORM-ATTEMPT`).** Alvo: item **(i)** da lista "o
que permanece aberto" do Estágio 6/7/8 — a forma fechada exata,
todas-as-ordens, geral-`K`, para a recursão discreta — nomeada
"separada e mais dura" desde o fechamento do Estágio 6, intocada por
todas as frentes seguintes.

### O que foi provado

Estendendo o `ε`-matching que produziu `F_r,G_r,H_r` (ordens `1`,
`1/n`, `1/n²`) a um índice de ordem **simbólico** `p`, obtém-se a EDO
receptora e a relação-fonte de ordem-`p` geral (não apenas mais um
degrau, mas a família inteira de uma vez). Lendo os multiplicadores
resultantes em `p=0,\ldots,8`, antes de qualquer ajuste, eles se
revelam serem exatamente os **números de Stirling de primeira espécie
sem sinal**, `c(k{+}p{+}1,k{+}1)` — do que seguem, por identidade
clássica de fatorial ascendente, a re-soma exata e finita da série
inteira (a série termina em `p=r`, já que `\deg\Phi^{[p]}_r=r{-}p`):

> **Teorema A (PROVADO, exato, todas-as-ordens, geral-`r`, geral-`b`,
> `n` finito).** Para todo `n`, todo `r,b\ge0` e todo `m` válido
> (`b{+}r{+}1\le m\le n`):
> `\displaystyle g_r(m,b)=\sum_{j=0}^{r}c^{(r)}_j(b)\prod_{i=1}^{j}\Big(\frac mn+\frac in\Big)`,
> `c^{(r)}_j(b)` os coeficientes **já provados** de `F_r` (ordem `1`).
>
> **Teorema B (PROVADO).** `\displaystyle h_r(a,b)=\frac{n{-}a{+}1}n
> g_r(n{-}a{+}1,b{+}1)` (com uma ressalva de domínio no extremo `a=0`,
> tratada explicitamente — ver documento fonte).
>
> **Corolário A1 (a instância-alvo, item (i)).**
> `\displaystyle \psi_n^{(K)}=\frac{\varphi_K}{4^K}\sum_{j=0}^{K}\binom{2K{+}1}{K{-}j}\frac{(n{+}j)!}{n!\,n^{j}}` —
> uma expressão finita, `K{+}1` termos, totalmente explícita, válida
> para todo `n\ge K{+}1`.

Teorema A admite **prova elementar independente** (quatro fatos
algébricos simples, P1–P4, mais indução bem-fundada na própria
recursão discreta), que não usa a maquinaria `ε` em momento algum —
logo as duas derivações (a maquinaria `ε` que *encontrou* o padrão, e
a prova elementar que o *fecha*) confirmam-se mutuamente.

### Verificação adversarial independente

Um referee hostil dedicado rederivou tudo **do zero**, começando pela
prova elementar do Teorema A (nomeada pelo próprio documento como o
lugar mais importante para atacar) antes de ler como o documento a
deriva: mesmo argumento, cada passo confere. Verificou os quatro fatos
simbolicamente — incluindo uma identidade por-termo simultaneamente
simbólica em `r` **e** `j`, estritamente mais forte que a checagem do
próprio documento — e contra um simulador próprio, do zero, das regras
`(a,b,r)` **originais** (não a reescrita do documento): **215.070
checagens exatas, 0 divergências**. Rederivou também a maquinaria `ε`
de ordem-`p` geral, confirmando os sinais (incluindo o sinal que o
próprio autor havia inicialmente errado e depois corrigido), a
identificação de Stirling até `p=8`, e a assimetria de terminação
`g`/`h` (`p=r` vs `p=r{+}1`), cuja causa estrutural o referee derivou
independentemente.

O referee encontrou **um erro real, de natureza negativa**: o
documento alegava que a forma fechada geral-`b` falha para `b\ge1`
("54–56 falhas de 61 pontos fora-da-amostra"), quando na verdade os
números reportados são exatamente os de `b=2` e `b=3` — em `b=1` a
mesma base representa a resposta **exatamente**, e o caso `p=2` já era
**provado** pelo Teorema 3′ do referee da onda 10
(`error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3)
especializado em `b=1`. O documento havia declarado aberto um caso que
seu próprio predecessor citado já fechara. Corrigido: a base funciona
exatamente em `b\in\{0,1\}` (razão estrutural: o prefator de Teorema
3′ colapsa a uma constante exatamente até `b=1`) e é refutada, por
obstrução estrutural (não por tamanho de base insuficiente), a partir
de `b\ge2`, que permanece aberto.

O referee também **promoveu duas alegações** que o documento
deliberadamente deixara conservadoras: executou a rota de prova
nomeada mas não realizada para as constantes agudas `D^{*(p)}_r(0)`
em `p=3,4,5` (via um teorema de estrutura análogo à técnica de
momentos binomiais par/ímpar de Estágio 8), promovendo-as de
NUMERICALLY VERIFIED a **PROVADAS**, com duas novas formas em `p=6,7`;
e provou, em duas linhas a partir desse teorema de estrutura, que o
coeficiente líder `(2p{-}1)!!/(4^pp!)` (antes apenas caracterizado
numericamente) é exato.

> **Veredito: SOUND, com uma correção negativa e duas promoções.**
> "Theorem A survives... The document's central claim is sound, and
> with it Theorem B, Theorem M, and Corollaries A1/A2/A3." Auditoria de
> honestidade específica pelo padrão de falha da onda 10 (condicional
> no scorecard virando incondicional no corpo do texto): **não
> encontrada** — a estrutura condicional é coerente em todo o
> documento.

Ver
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/adversarial/REFEREE_REPORT.md`
para o relatório completo.

### O que isto muda, precisamente

**O item (i) da lista "o que permanece aberto" desde o Estágio 6 está
FECHADO** — a forma fechada exata, todas-as-ordens, geral-`K`, geral-`b`,
geral-`m`, finito-`n`, existe e está provada (Teorema A/B, Corolário
A1). Como corolário imediato, os Teoremas 1–4 e o Corolário 1a–3a de
`k_general_existence_attempt/ATTEMPT.md` e de
`error_constant_growth_attempt/ATTEMPT.md` (Estágios 6–8 inteiros)
tornam-se casos particulares desta forma fechada única — **nenhum
deles é enfraquecido ou substituído**; a nova forma apenas os subsume.
Novas fórmulas exatas `ψ_n^{(6)},ψ_n^{(7)},ψ_n^{(8)}` são produzidas
como subproduto direto.

**O que permanece aberto, sem mudança:** (iv) versão uniforme-em-`c`
do Teorema 3 [Ver Estágio 10 abaixo — este item foi fechado] (onda 11
frente (a) tratou exatamente disto); (v) Conjecturas 1–2 (lei distribucional
completa, `K≥2`); e, dentro do escopo desta própria frente: a forma
fechada geral-`b` das constantes agudas `D^{*(p)}_r(b)` para `b\ge2`
[Ver Estágio 14 abaixo — fechado para `p=1,2,3,4`; `p\ge5`
permanece aberto] (estrutura da obstrução agora identificada, não apenas negativa);
qualquer alegação uniforme-em-`K` (explicitamente não tentada em
nenhum lugar). **O Teorema 3 (Estágio 6) permanece inteiramente
inafetado** — nunca dependeu desta frente.

**Veredito honesto atualizado (ao fim do Estágio 9):** a linha `U_1/2`
tem agora uma forma fechada exata, todas-as-ordens, geral-`K`,
geral-`b`, finito-`n`, para a recursão discreta inteira, da qual todo
resultado anterior desta linha (Teorema 3, Estágios 5–8) é corolário.
Restam abertos apenas: a forma fechada das constantes agudas em
`b\ge2`; uniformidade-em-`c` do Teorema 3 (frente paralela); as
Conjecturas 1–2 da lei distribucional completa. Fontes completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/ATTEMPT.md`,
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 10 — 2026-08-23]

**Onda 11, frente (a), `DISC-DEC-047`/`DISC-DEC-049`
(`UNIFORM-IN-C-TEOREMA-3-ATTEMPT`).** Alvo: item **(iv)** da lista "o
que permanece aberto" desde o Estágio 6/7/8/9 — a versão
localmente-uniforme-em-`c` do Teorema 3, nunca tentada, mais a
pergunta nunca respondida do que acontece quando `c` cresce junto com
`n`.

### O que foi provado

Teorema 3 (Estágio 6) prova `φ(n,c)→φ_∞(c)` para cada `c\ge0`
**fixo**, um `c` de cada vez — nada sobre uniformidade. Este front
fecha a lacuna, e mais:

> **Teorema A (PROVADO, incondicional).** Para todo `C>0` fixo,
> `\displaystyle\sup_{c\in[0,C]}|φ(n,c)-φ_∞(c)|\xrightarrow[n\to\infty]{}0`.
>
> **Teorema C (PROVADO, incondicional).** `\displaystyle\sup_{c\in[0,\infty)}|φ(n,c)-φ_∞(c)|\xrightarrow[n\to\infty]{}0`
> (sob a convenção `q=\min(c/n,1)` de Definição 1) — mais forte do que
> o item pedia: não apenas uniforme em compactos, mas em todo o
> domínio.

Ambos os teoremas descartam inteiramente a maquinaria `F_r/G_r/H_r` —
apoiam-se em apenas dois lemas elementares novos: um acoplamento de
`ξ` que dá `|φ(n,c)-φ(n,c')|\le|c-c'|`, uniforme em `n` (Lema 3.1,
"equi-Lipschitz"), e um limitante de cauda uniforme-em-`n` provado
diretamente na exploração do passeio (Lema 4.1). O argumento
"pontual + equicontínuo ⟹ uniforme em compactos" é padrão; o que
faltava no arquivo era só a equicontinuidade, suprida em uma linha.

Além disso, o perfil de erro de primeira ordem tem forma fechada
exata:

> **Teorema D (PROVADO, incondicional).** Para todo `j\ge0` fixo,
> `n([c^j]φ(n,\cdot)-[c^j]φ_∞)\to e_j`, uma soma finita explícita em
> `c_K` (Estágio 7) e `φ_K` (Wallis). E
> `\displaystyle e(c)=\sum_j e_jc^j=\tfrac12\int_0^1\frac{1-(1+ct^2+c^2t^4)e^{-ct^2}}{t^2}dt`,
> com `e(c)\sim\sqrt{πc}/8` para `c` grande — a constante de erro
> uniforme em `[0,C]` cresce exatamente como `\sqrt C`.

A versão **uniforme** (não apenas coeficiente-a-coeficiente) desse
perfil, `n\sup_{[0,C]}|Δ_n|\to\sup_{[0,C]}|e|`, e um limitante
explícito `\sup_{[0,C]}|Δ_n|\le(a\sqrt C+κ_B)/n` permanecem
condicionais a uma hipótese nomeada — exatamente "a taxa `1/n` do
Estágio 7, uniforme em `K`", que o próprio Estágio 7 explicitamente
não afirma. Esta é a única obstrução nomeada a uma taxa totalmente
explícita.

Sobre `c` crescendo com `n`: em termos **absolutos** nada diverge —
até o sup global tende a `0`. Em termos **relativos** a lei-limite
degrada de forma precisamente localizável: para `c=γn`,
`φ(n,c)/φ_∞(c)\to\sqrt{2/(2-γ)}`, **provado** no extremo `γ=1`
(`φ(n,n)=Q(n)/n` exatamente, função `Q` de Ramanujan) e caracterizado
numericamente para `γ\in(0,1)`. [Ver Estágio 23 abaixo — 2026-08-26:
provado para todo `γ\in(0,1]`, com uniformidade em compactos e o
limite `γ_n\to0`.]

### Verificação adversarial independente

Um referee hostil dedicado atacou os dois insumos analíticos novos
(Lema 3.1, Lema 4.1) e os dois teoremas incondicionais (Teorema A,
Teorema C) com peso máximo, auditando cada uma das seis etapas do
Lema 4.1 separadamente (não apenas o limitante final) — nenhum erro
encontrado em nenhum deles. Confirmou também Teorema D como
"*airtight*" (testado contra uma recursão simbólica que nunca usa a
identidade binomial de apoio, 91/91 coeficientes exatos), e
re-derivou o perfil `e(c)` por uma rota totalmente independente,
reproduzindo a mesma forma fechada, incluindo o cancelamento exato
`1-j(2j-1)=-(2j+1)(j-1)`.

**Um achado substantivo, de natureza incomum: o documento nomeava a
lacuna errada para a razão de Teorema E ser condicional.** O texto
original afirmava, incorretamente, que a Proposição 6 do Estágio 8
"prova" a geometricidade dos limitantes melhorados — na verdade
Estágio 8 prova apenas o limitante, não a geometricidade (sua própria
tabela de status classifica isso como apenas caracterizado
numericamente). O rótulo PROVED-MODULO permanece correto, mas a
lacuna nomeada estava errada: não é a falta de uma constante
geométrica explícita, é a falta de uma prova escrita da
geometricidade *qualitativa*. Mais três pequenas imprecisões de
sumário executivo (qualificadores presentes no corpo do texto que
sumiam no resumo) foram corrigidas, mais uma dúzia de nits cosméticos.
O referee também registrou um fortalecimento não solicitado: a
identidade que explica a constante afiada `a^*` é **exata**
(`φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n`), não apenas aproximada como o
documento original afirmava.

> **Veredito: SPLIT, esmagadoramente positivo.** "The two headline
> unconditional theorems survive a deliberate attempt to break them...
> found **no error of any kind**." Nenhuma das correções toca Lema
> 3.1, Teorema A, Lema 4.1, Corolário 4.2 ou Teorema C.

Ver
`uniform_in_c_attempt/ATTEMPT.md` e
`uniform_in_c_attempt/adversarial/REFEREE_REPORT.md` para os
relatórios completos.

### O que isto muda, precisamente

**O item (iv) da lista "o que permanece aberto" desde o Estágio 6 está
FECHADO** — e de forma mais forte do que pedido: não apenas
uniformidade em compactos, mas em todo `[0,\infty)`. A pergunta
correlata (o que acontece quando `c` cresce com `n`) recebeu resposta
completa: nenhuma divergência absoluta em lugar nenhum, com
degradação relativa precisamente localizada e mecanismo identificado.

**O que permanece aberto, sem mudança:** uma taxa explícita para
Teorema A/C (condicional à hipótese (U'), uniformidade-em-`K` da taxa
do Estágio 7 — nomeada, não provada); a versão uniforme de Teorema E
(gap real, agora corretamente nomeado: geometricidade qualitativa de
`M_K`) [Ver Estágio 11 abaixo — este item foi fechado]; a lei de escala
`γ\in(0,1)` (caracterizada, não provada); (v)
Conjecturas 1–2. **O Teorema 3 (Estágio 6) permanece inteiramente
inafetado** — nunca dependeu desta frente.

**Veredito honesto atualizado (ao fim do Estágio 10):** a linha
`U_1/2` tem agora convergência uniforme incondicional em todo o
domínio de `c` (Teoremas A e C), além da forma fechada
todas-as-ordens geral-`K` do Estágio 9 — os dois itens mais difíceis
da lista original de itens abertos desde o Estágio 6 estão ambos
fechados. Resta, como obstrução central e única nomeada para uma taxa
explícita: uniformidade-em-`K` da taxa `1/n` do Estágio 7. Fontes
completas:
`theorem/uniform_in_c_attempt/ATTEMPT.md`,
`theorem/uniform_in_c_attempt/adversarial/REFEREE_REPORT.md`.

## [Extensão, Estágio 11 — 2026-08-23]

**Onda 12, frente (a), `DISC-DEC-051`/`DISC-DEC-052`
(`MK-QUALITATIVE-GEOMETRICITY-ATTEMPT`).** Alvo: a única obstrução
nomeada restante para tornar Teorema E (Estágio 10) incondicional —
uma prova escrita de que `M_K := sup_{n≥K+1}|n(φ_n^{(K)}-φ_K)|` cresce
no máximo geometricamente em `K` (qualquer taxa `λ` serve, o valor
exato é irrelevante).

### O que foi provado

> **Teorema (crescimento geométrico qualitativo de `M_K`, PROVADO).**
> `M_K \le φ_K(K{+}1)e^{K/2}+K = O(K(\sqrt e)^K)`. Em particular
> `\Sigma_K c^K M_K/K! < \infty` para todo `c\ge0` — exatamente o que
> Teorema E precisa para tomar o limite termo-a-termo por convergência
> dominada.

A prova (Rota A) NÃO segue a rota originalmente esboçada pelo referee
de Estágio 10 (desenrolar a recursão da Proposição 6 de Estágio 8) —
essa rota foi verificada até onde vai (seus passos algébricos (a) e
(b) checam), mas exigiria um limitante geométrico geral-`b` para
`A_r(b),B_r(b)` que não está estabelecido em lugar nenhum do arquivo
(marcado como item aberto separado, NÃO tentado aqui). Em vez disso, a
frente encontrou uma rota mais direta usando um ingrediente que não
existia quando Estágio 8/10 foram escritos: a forma fechada
todas-as-ordens do Estágio 9 (`ψ_n^{(K)}`, Corolário A1, já PROVADA
incondicionalmente). Três passos elementares: (1) `n(ψ_n^{(K)}-φ_K)`
decompõe-se numa soma não-negativa de termos que são, cada um,
não-crescentes em `n` (positividade de polinômios simétricos
elementares), logo o supremo sobre `n` é atingido exatamente em
`n=K+1`; (2) em `n=K+1`, a desigualdade `1+x\le e^x` termo-a-termo dá
um limitante geométrico cru; (3) o Lema A de redução (já PROVADO,
Estágio 3) conecta `ψ_n^{(K)}` a `φ_n^{(K)}`, usando apenas que ambas
as quantidades envolvidas são probabilidades (logo em `[0,1]`, por
definição). Nenhum passo usa `D_r(b)`, `A_r(b)`, `B_r(b)` ou a
Proposição 6.

**Achado colateral, informativo, não parte da prova:** a taxa
verdadeira de `M_K` parece ser `Θ(\sqrt K)`, não geométrica — a mesma
ordem do limite já-provado `Kφ_K/4` (Estágio 6). O limitante cru é
válido mas extremamente frouxo (razão `>10^{19}` já em `K=300`),
espelhando o mesmo padrão que Estágio 8 encontrou para `D_r(b)` vs
`D*_r(b)`. Não provado, não reivindicado.

### Verificação adversarial independente

Um referee hostil dedicado re-derivou cada um dos cinco passos da Rota
A do zero, a partir das afirmações matemáticas apenas (nenhum arquivo
`.py` da frente-alvo foi lido), e checou cada citação contra as
próprias fontes primárias (não contra a transcrição da frente-alvo):
o Corolário A1 reproduz quatro fórmulas fechadas independentemente
derivadas (`ψ_n^{(1)},\dots,ψ_n^{(4)}`, de dois métodos de derivação
diferentes); o argumento de monotonicidade (o passo mais crítico,
atacado com mais força) foi re-derivado do zero e testado
exaustivamente muito além da faixa da própria frente (50.399 + 24.430
pares exatos, 0 violações, argmax correto em 70/70 `K` testados); o
limitante geométrico cru e a identidade da meia-soma binomial
subjacente foram confirmados exatos até `K=400`; a propriedade
`ψ_n^{(K)},ψ_n^{(K),R}\in[0,1]` foi confirmada como genuinamente
definicional na fonte primária do Lema A (não uma suposição não
justificada da frente-alvo); e o diagnóstico de que a Rota B
(Proposição 6) permanece genuinamente aberta (não apenas não
explorada) foi confirmado contra as próprias tabelas de status das
fontes primárias.

> **Veredito: SOUND. "ACCEPT for catalogue."** "No error, gap, or
> unjustified step was found anywhere in Steps 1–5." Único achado: uma
> imprecisão de citação (paráfrase, não erro matemático) na lista de
> fontes lidas da frente-alvo — sem efeito sobre nenhuma alegação.

Ver
`uniform_in_c_attempt/mk_geometricity_attempt/ATTEMPT.md` e
`uniform_in_c_attempt/mk_geometricity_attempt/adversarial/REFEREE_REPORT.md`
para os relatórios completos.

### O que isto muda, precisamente

**Teorema E (Estágio 10, §5.6 de `uniform_in_c_attempt/ATTEMPT.md`)
PERDE o rótulo PROVED-MODULO e torna-se PROVADO, incondicional, em
ambas as versões** (pontual `n\,Δ_n(c)\to e(c)` e uniforme
`n\sup_{[0,C]}|Δ_n|\to\sup_{[0,C]}|e|`). Nenhum resultado anterior é
enfraquecido: Teorema 3 (Estágio 6), a taxa `c_K` (Estágio 7), a forma
fechada de erro (Estágio 8), a forma fechada todas-as-ordens
(Estágio 9), e Teoremas A/C/D (Estágio 10) permanecem exatamente como
provados, usados aqui apenas por citação.

**Isto NÃO fecha a hipótese (U') nem "uma taxa explícita para Teorema
A/C"** — obstrução genuinamente diferente e mais forte, que exige
`|φ_n^{(K)}-φ_K|\le a\sqrt K/n` UNIFORME em `K` (um limitante que NÃO
cresce com `K`), contra a condição aqui provada, que só exige que
`M_K` cresça no máximo geometricamente (um limitante que CRESCE com
`K`, apenas não mais rápido que geométrico) — suficiente para a soma
`\Sigma_K c^K M_K/K!` convergir, insuficiente para um limitante
explícito uniforme-em-`K`. Este item permanece **aberto, sem
mudança**. [Ver Estágio 12 abaixo — este item foi fechado, com
constante explícita não-nítida, `2026-08-23`.]

**O que permanece aberto, sem mudança:** uma taxa explícita para
Teorema A/C (condicional à hipótese (U'), ainda não provada) [Ver
Estágio 12 abaixo — hipótese (U') agora PROVADA, taxa explícita
incondicional obtida]; a lei de
escala `γ\in(0,1)` (caracterizada, não provada); a forma fechada
geral-`b` das constantes agudas em `b\ge2` (Estágio 9); Conjecturas
1–2. **O Teorema 3 (Estágio 6) permanece inteiramente inafetado** —
nunca dependeu desta frente.

**Veredito honesto atualizado (ao fim do Estágio 11):** a linha
`U_1/2` tem agora, além da forma fechada todas-as-ordens (Estágio 9) e
da convergência uniforme incondicional (Estágio 10), o próprio perfil
de erro (Teorema D/E) inteiramente incondicional — não resta mais
nenhuma alegação "PROVED-MODULO" nesta linha. Resta, como obstrução
central e única nomeada para uma taxa explícita uniforme-em-`K`: a
hipótese (U'). Fontes completas:
`uniform_in_c_attempt/mk_geometricity_attempt/ATTEMPT.md`,
`uniform_in_c_attempt/mk_geometricity_attempt/adversarial/REFEREE_REPORT.md`.
[Ver Estágio 12 abaixo — hipótese (U') fechada, `2026-08-23`.]

---

## [Extensão, Estágio 12 — 2026-08-23]

**Onda 13, frente (a), `DISC-DEC-054`/`DISC-DEC-055`
(`U-PRIME-HYPOTHESIS-ATTEMPT`).** Alvo: a única obstrução central
restante nomeada para uma taxa explícita uniforme-em-`K` — a hipótese
(U'), deixada aberta pelo Estágio 11.

### O que foi provado

> **Teorema (Hipótese (U'), PROVADA).** Existe `a<\infty` tal que
> `\displaystyle|φ_n^{(K)}-φ_K| \le \frac{a\sqrt K}n` para **todo**
> `n\ge1` e todo inteiro `0\le K\le n`, com constante explícita
> `a = 1+\sqrt{π/2} = 2,253314\ldots`.

A prova combina a forma fechada todas-as-ordens do Estágio 9
(Corolário A1, `ψ_n^{(K)}=g_K(n,0)`) com uma fórmula-companheira para
`ψ_n^{(K),R}` derivada aqui, pela primeira vez, do Teorema B de
Estágio 9 (`h_r(a,b)` avaliado em `a=0`, dentro do "domain caveat" já
explicitamente sinalizado pela própria fonte primária), via o Lema A
de redução: (1) uma identidade exata decompõe
`T(n,K):=n(φ_n^{(K)}-φ_K)` numa combinação não-negativa de termos
não-crescentes em `n`, provando — para **todo** `K`, não apenas
numericamente até `K=16384` como o Estágio 10 havia deixado — que o
supremo sobre `n` é sempre atingido em `n=K{+}1`; (2) nesse ponto, a
quantidade colapsa, via a identidade exata `φ_n^{(n-1)}=Q(n)/n` já
estabelecida por correção pós-adversarial em Estágio 10, à forma
fechada `M_K = Q(K{+}1)-(K{+}1)φ_K`, ligando `M_K` diretamente à
função `Q` de Ramanujan; (3) dois limitantes-sanduíche elementares
(`φ_K` entre `\sqrt π/(2\sqrt{K{+}1})` e `\sqrt π/(2\sqrt K)`; `Q(n)\le
1{+}\sqrt{πn/2}`) fecham a desigualdade com a constante explícita
acima. A constante **nítida** `a^*=\sqrt π(1/\sqrt2-1/2)=0,3670872\ldots`
**não** é estabelecida — este teorema prova limitação com uma
testemunha explícita, não nitidez — e permanece aberta, com o
ingrediente exato que falta nomeado com precisão (um limitante
*inferior* correspondente para `Q(n)`, simétrico ao limitante superior
usado acima).

### Verificação adversarial independente

Um referee hostil dedicado re-derivou cada teorema/lema do zero a
partir das fontes primárias citadas (nenhum arquivo `.py` da
frente-alvo foi lido), incluindo um motor Markov `(a,b,r)`
inteiramente independente (`mychain.py`) construído apenas a partir
das regras de transição declaradas em `k3_attempt_2/ATTEMPT.md` — não
de nenhuma forma fechada — usado para checar cada passo algébrico
independentemente da álgebra fechada. Escala independente muito além
da própria frente e da sessão orquestradora: Proposição 2.1
re-derivada simbolicamente (`K=1..14`); decomposição exata (Teorema 1)
simbólica até `K=25`, exata até `K=300` (2.408 pares); monotonicidade/
argmax (Teorema 2) em 9.960 pares `(K,n)`; identidade `M_K`
(Teorema 3) exata até `K=1000`; **o Lema 4.1 (sanduíche de `φ_K`),
sinalizado como não verificado à mão pela sessão orquestradora, recebeu
o escrutínio mais intenso** — identidades cúbicas checadas
simbolicamente como polinômios não-reduzidos, monotonicidade exata até
`K=20.000` e via `mpmath` até `K=10^6`; a desigualdade final montada
(Teorema 4) checada com **zero violações** em quatro escalas
independentes, até `K=10^5` e `n` interior até `100K`.

> **Veredito: SOUND. "ACCEPT for catalogue."** Nenhum erro matemático,
> lacuna, uso indevido de citação ou alegação excessiva encontrado em
> lugar algum do documento-alvo. A própria seção de honestidade do
> documento-alvo (constante nítida `a^*` não estabelecida; ingrediente
> exato que falta nomeado) foi checada contra a numérica independente
> do referee e considerada precisa, nem subestimando nem superestimando
> o que foi provado.

Ver
`uniform_in_c_attempt/u_prime_hypothesis_attempt/ATTEMPT.md` e
`uniform_in_c_attempt/u_prime_hypothesis_attempt/adversarial/REFEREE_REPORT.md`
para os relatórios completos.

### O que isto muda, precisamente

**A hipótese (U') PERDE o rótulo "aberta" e torna-se PROVADA**, com
constante explícita `a=1{+}\sqrt{π/2}` (não nítida). Via o Teorema B
de `uniform_in_c_attempt/ATTEMPT.md` §6.2 (já PROVADO ali,
condicionalmente a (U')), isto dá imediatamente uma **taxa explícita,
incondicional**, para Teorema A/C: para `n\ge4`, `0\le c\le n`,

`\displaystyle |Δ_n(c)| \le \big[(1{+}\sqrt{π/2})\sqrt c + 0,2805\big]/n`.

> [Ver Estágio 22 abaixo — 2026-08-25: a mesma montagem, re-executada
> com a constante nítida `a^*` do Estágio 19, dá o **Teorema R**:
> `|Δ_n(c)| \le [a^*\sqrt c + 0{,}2805]/n`, estrito em `(0,n]`, mesma
> constante aditiva (independência estrutural da metade `B_n`).]

Isto fecha "a única obstrução nomeada restante entre Teorema A/C
(provado, incondicional) e uma taxa totalmente explícita", nomeada
pelo Estágio 10 e reafirmada pelo Estágio 11. Nenhum resultado anterior
é enfraquecido: Teorema 3 (Estágio 6), a taxa `c_K` (Estágio 7), a
forma fechada de erro (Estágio 8), a forma fechada todas-as-ordens
(Estágio 9), Teoremas A/C/D/E (Estágios 10–11) permanecem exatamente
como provados, usados aqui apenas por citação. A prova de Estágio 11
(crescimento geométrico qualitativo de `M_K`) permanece
**estritamente mais fraca** que este resultado e não é superada nem
tornada redundante por ele — são obstruções genuinamente diferentes
que este documento manteve deliberadamente distintas em todo o seu
histórico.

**O que permanece aberto, sem mudança:** a constante **nítida**
`a^*=0,3670872\ldots` (este Estágio prova limitação com constante
explícita `\approx6,16\times` mais frouxa, não nitidez); o segundo fato
nomeado em Estágio 10/§6.3 — que o limite `K\to\infty` da razão do
extremo é genuinamente o supremo sobre `K`, não apenas seu limite —
permanece aberto; a lei de escala `γ\in(0,1)` (caracterizada, não
provada); a forma fechada geral-`b` das constantes agudas em `b\ge2`
(Estágio 9); Conjecturas 1–2. O ingrediente exato que fecharia a
nitidez foi nomeado com precisão pela própria frente: um limitante
*inferior* para `Q(n)` da forma `Q(n)\ge\sqrt{πn/2}-C`, simétrico ao
limitante superior usado aqui. [Ver Estágio 13 abaixo — o limitante
inferior de `Q(n)` foi provado e o LIMITE `\lim_K M_K/\sqrt K=a^*` está
agora exato; o SUPREMO `\sup_K M_K/\sqrt K=a^*` continua aberto,
`2026-08-23`.] [Ver Estágio 19 abaixo — o SUPREMO também está agora
PROVADO: `\sup_K M_K/\sqrt K=a^*` exatamente, `2026-08-25`.]

**Veredito honesto atualizado (ao fim do Estágio 12):** a linha `U_1/2`
tem agora uma taxa de convergência **explícita e incondicional** para
Teorema A/C — não resta mais nenhuma obstrução central nomeada entre
"convergência provada" e "taxa explícita provada" nesta linha. Resta,
como refinamento nomeado e não mais central, tornar essa taxa
**nítida** (constante `a^*` em vez de `a\approx6,16a^*`). Fontes
completas:
`uniform_in_c_attempt/u_prime_hypothesis_attempt/ATTEMPT.md`,
`uniform_in_c_attempt/u_prime_hypothesis_attempt/adversarial/REFEREE_REPORT.md`.
[Ver Estágio 13 abaixo — progresso parcial na nitidez, `2026-08-23`.]

---

## [Extensão, Estágio 13 — 2026-08-23]

**Onda 14, frente (a), `DISC-DEC-057`/`DISC-DEC-058`
(`SHARP-CONSTANT-U-PRIME-ATTEMPT`).** Alvo: a constante nítida
`a^*=\sqrt π(1/\sqrt2-1/2)=0,3670872\ldots` deixada aberta pelo
Estágio 12 — o ingrediente exato nomeado ali (um limitante inferior
para a função `Q` de Ramanujan) e um segundo fato separado
(monotonicidade de `M_K/\sqrt K` em `K`, equivalente a `\sup_K=\lim_K`).

### O que foi provado

> **Teorema (limitante inferior de `Q(n)`, PROVADO).**
> `\displaystyle Q(n) \ge \sqrt{\frac{πn}2} - 6` para todo `n\ge1`.

> **Teorema (o limite exato, PROVADO).**
> `\displaystyle \lim_{K\to\infty}\frac{M_K}{\sqrt K} = a^*`.

A prova do primeiro usa a rota elementar já nomeada pela decisão
autorizadora (`-\ln(1{-}x)\le x/(1{-}x)`, o dual logarítmico da
desigualdade `1{-}x\le e^{-x}` já usada pelo Estágio 12), mas com uma
comparação termo-a-termo sem truncamento (evitando um trade-off
desfavorável que uma primeira tentativa em papel encontrou, registrado
e descartado no pré-registro). Combinado com o Teorema 3 e o Lema 4.1
do Estágio 12 (ambos citados, inalterados), o segundo teorema
**eleva** o `\limsup_{K\to\infty}M_K/\sqrt K\le a^*` já implícito na
prova do Estágio 12 a um limite exato — a primeira identificação
exata da constante assintótica líder, não apenas um limitante superior
sobre ela.

**O que NÃO foi fechado:** monotonicidade de `M_K/\sqrt K` em `K`
(equivalente a `\sup_K=\lim_K`) — tentada por duas rotas distintas
(uma recursão exata para `Q(n)`, refutada por contraexemplo explícito
`Q(3)=17/9\ne1{+}\tfrac23Q(2)=2`; e um limitante pontual direto
`M_K\le a^*\sqrt K`, que exigiria limitantes superior de `Q(n)` e
inferior de `φ_K` ambos precisos a `O(1/\sqrt K)` para todo `K` finito
— mais delicado que qualquer ferramenta elementar disponível) —
nenhuma das duas fecha. Evidência numérica exata forte (`K` até
`3000`, estritamente crescente, nunca atinge `a^*`) é relatada
honestamente como heurística, não prova.

### Verificação adversarial independente

Um referee hostil dedicado re-derivou cada passo algébrico do zero —
incluindo os dois passos explicitamente sinalizados como não
verificados à mão (a decomposição de `ε(x)` e o limitante de
`\mathrm{Err}(n)`) — e não encontrou nenhum erro. Foi além do exigido:
derivou independentemente o limite `\mathrm{Err}(n)\to3/2` quando
`n\to\infty` (não presente no documento-alvo), confirmando que a folga
do limitante `\le5` usado é de fator `\approx2`, não arbitrária. A
verificação numérica independente alcançou `n,K` até `10^6` — sem
nenhuma violação em lugar algum, a margem convergindo monotonicamente
ao valor exato `17/3` (Teorema 5) e a razão `M_K/\sqrt K` nunca
atingindo `a^*` em nenhum dos aproximadamente `1.500` valores de `K`
testados até `10^6`.

> **Veredito: SOUND. "ACCEPT for catalogue."** Nenhum erro matemático
> encontrado em lugar algum. Único achado: uma inconsistência interna
> cosmética entre a contagem de pontos numéricos relatada no texto e na
> seção de arquivos do documento-alvo — sem efeito sobre nenhuma
> alegação matemática, confirmado diretamente pelo referee.

Ver
`uniform_in_c_attempt/u_prime_hypothesis_attempt/sharp_constant_attempt/ATTEMPT.md`
e
`uniform_in_c_attempt/u_prime_hypothesis_attempt/sharp_constant_attempt/adversarial/REFEREE_REPORT.md`
para os relatórios completos.

### O que isto muda, precisamente

**O limite `\lim_{K\to\infty}M_K/\sqrt K=a^*` está agora PROVADO,
exatamente** — a primeira confirmação rigorosa de que a constante
numericamente conjecturada `a^*` é genuinamente a constante assintótica
correta, não apenas um limitante superior sobre ela. **Isto NÃO
prova a hipótese (U') com a constante nítida `a^*`** — a constante
explícita provada na hipótese (U') permanece `a=1{+}\sqrt{π/2}\approx
2,2533` (Estágio 12, inalterado), pois o fato que faltava para a
nitidez uniforme-em-`K` (`\sup_K=\lim_K`) continua aberto. Nenhum
resultado anterior é enfraquecido: Teoremas 3/E (Estágios 10–11), a
hipótese (U') com constante não-nítida (Estágio 12), e todos os
resultados anteriores permanecem exatamente como provados.

**O que permanece aberto, sem mudança:** `\sup_K M_K/\sqrt K=a^*`
(equivalente a monotonicidade de `M_K/\sqrt K` em `K`) — o ingrediente
exato que falta agora nomeado com ainda mais precisão: limitantes de
`Q(n)` (superior) e `φ_K` (inferior) ambos precisos a `O(1/\sqrt K)`
para **todo** `K` finito, não apenas assintoticamente. A constante
usada na hipótese (U') como efetivamente provada continua sendo
`a=1{+}\sqrt{π/2}`, não `a^*`.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-068`] O supremo
> está agora PROVADO: `\sup_K M_K/\sqrt K=a^*` exatamente, na
> terceira tentativa (onda 16), via um limitante superior
> não-assintótico de `Q(n)` construído de duas citações clássicas —
> com a precisão de que o diagnóstico acima estava meio certo: só o
> lado `Q(n)` precisava de afiação; o `z_K`-bound do Lema 4.1, usado
> sem modificação, já bastava do outro lado. A hipótese (U') fica com
> a constante nítida `a^*` em todos os casos (caso de contorno `K=n`
> fechado pelo referee da própria frente, verificado pela sessão).
> [Ver Estágio 19 abaixo.] A lei de escala `γ\in(0,1)`
(caracterizada, não provada); Conjecturas 1–2; a forma fechada
geral-`b` das constantes agudas em `b\ge2` (Estágio 9) permanecem
inalterados [Ver Estágio 14 abaixo — fechado para `p=1,2,3,4`;
`p\ge5` permanece aberto].

**Veredito honesto atualizado (ao fim do Estágio 13):** a linha
`U_1/2` tem agora, além da taxa explícita incondicional (Estágio 12),
a identificação exata da constante assintótica líder `a^*` como
verdadeiro valor-limite (não apenas cota superior) — um refinamento
genuíno, mas que ainda não se traduz num limitante uniforme-em-`K` com
essa constante nítida. O único ingrediente nomeado que fecharia esse
último passo é um limitante inferior de `Q(n)` de precisão
`O(1/\sqrt K)` para todo `K`, não apenas assintótico — um alvo
concreto para uma frente futura. Fontes completas:
`uniform_in_c_attempt/u_prime_hypothesis_attempt/sharp_constant_attempt/ATTEMPT.md`,
`uniform_in_c_attempt/u_prime_hypothesis_attempt/sharp_constant_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 14 — 2026-08-23]

**Onda 14, frente (d), `DISC-DEC-057`/`DISC-DEC-059`
(`GENERAL-B-DSTAR-ATTEMPT`).** Alvo: o item deixado nomeadamente
aberto pelo Estágio 9 — a forma fechada geral-`b` das constantes
agudas `D^{*(p)}_r(b)` para `b\ge2` (Corolário A3 de
`all_orders_closed_form_attempt/ATTEMPT.md`, tomado aqui como insumo
fixo, já provado, não re-derivado).

### O que foi provado

Estendendo a rota de colapso de prefator no estilo Teorema 3′ (já
provada para `p=2` pelo referee da onda 10) a `p` simbólico, usando
quatro ingredientes (grau/anulamento de `Q_p(u)`; os momentos centrais
de `\mathrm{Bin}(N,\tfrac12)`; duas identidades novas `I5,I7` via soma
por partes de Abel; e uma família de colapso geral-`k` do prefator):

> **Teorema D1 (PROVADO).** `\displaystyle D^{*(1)}_r(b)` tem forma
> fechada exata para todo `b\ge0`, reduzindo caractere-por-caractere às
> fórmulas já provadas em `b\in\{0,1\}`.

> **`D^{*(2)}_r(b)`, `D^{*(3)}_r(b)`, `D^{*(4)}_r(b)` (PROVADOS, todo
> `b\ge0`).** O caso `p=2` é uma re-derivação independente do já
> provado Teorema 3′ (confere exatamente); `p=3,4` são formas novas.

O mecanismo é integralmente `p`-uniforme (nenhum passo usa fato
específico de `p` além do grau/anulamento de `Q_p`), fechando quatro
valores de `p` simultaneamente com um único método.

### Verificação adversarial independente

Um referee hostil dedicado re-derivou a rota inteira do zero — a partir
apenas do Corolário A3, sem ler nenhum script do próprio documento —
com sua própria tabela de Stirling, sua própria soma-por-partes de
Abel, sua própria extração de momentos centrais via função geradora de
cumulantes, e sua própria montagem final: **165.888 checagens exatas,
0 divergências**, em escala superior à do próprio documento em todos
os quatro valores de `p` (`24` valores distintos de `b\ge2` testados
para `p=3,4`, não apenas o único ponto `b=2` que a sessão orquestradora
já havia sinalizado como fino antes de despachar o referee).

O referee foi além do exigido: o documento-alvo classificava como
**OPEN** (item 11 do seu scorecard) se o padrão de cancelamento de
`I5,I7` generaliza para `I9,I11,\ldots` (i.e., para `p\ge5`). O referee
mostrou que esse cancelamento é, na verdade, uma consequência de uma
linha só de um fato binomial de paridade —
`(w-1)^n-(w+1)^n=-2\sum_{t\text{ ímpar}}\binom nt w^{n-t}`, válido para
**todo** expoente par `n`, não apenas os dois casos `n=4,6` usados pelo
documento — verificada simbolicamente até `n=40` e numericamente (força
bruta, sem recursão) até `k=11`. Isto torna a obstrução nomeada no item
11 **removível por um argumento mecânico**, não uma nova ideia em
aberto — mas o referee **não** executou a montagem completa para
`p\ge5` (nenhum `Q_5,Q_6,\ldots`, nenhum momento `\mu_{10},\mu_{12}`,
nenhuma fórmula `D^{*(p\ge5)}_r(b)` foi produzida), então `p\ge5`
continua honestamente **não fechado**, apenas com seu único obstáculo
nomeado agora identificado como removível.

> **Veredito: SOUND. "ACCEPT."** Nenhum erro encontrado em lugar
> algum — nem nas quatro fórmulas montadas, nem nas cinco instâncias
> concretas impressas, nem na correção de um erro auto-relatado no
> próprio documento (verificado como genuinamente corrigido, sem
> reintrodução silenciosa). O único achado é uma sub-alegação (item 11
> descrito como "OPEN" quando sua obstrução nomeada é removível),
> registrada para benefício de uma frente futura, não uma falha exigindo
> correção.

Ver
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/ATTEMPT.md`
e
`.../general_b_dstar_attempt/adversarial/REFEREE_REPORT.md` para os
relatórios completos.

### O que isto muda, precisamente

**O item nomeado aberto pelo Estágio 9 — forma fechada geral-`b` das
constantes agudas `D^{*(p)}_r(b)` para `b\ge2` — está agora FECHADO
para `p=1,2,3,4`, todo `b\ge0`** (Teorema D1 e as três fórmulas
irmãs). Nenhum resultado anterior é enfraquecido: Corolário A3,
Teorema 3′, e todas as fórmulas de calibração `b\in\{0,1\}` já
provadas permanecem exatamente como estavam, agora casos particulares
das novas formas fechadas.

**O que permanece aberto, sem mudança:** a forma fechada geral-`b`
para `p\ge5` — o único obstáculo nomeado (o padrão de cancelamento de
`I_{2k+1}`) foi identificado pelo referee como mecanicamente removível,
mas a montagem explícita para `p\ge5` não foi executada em lugar
algum, nesta frente ou pelo referee; permanece um alvo concreto,
agora mais barato, para uma frente futura [Ver Estágio 16 abaixo — a
montagem foi executada para `p=1,\ldots,10`]. A soma da faixa (`strip
sum`) continua sendo deixada como soma explícita de `b` termos, por
desenho, não uma limitação. Nenhuma alegação uniforme-em-`K` ou
uniforme-em-`p` é feita.

**Veredito honesto atualizado (ao fim do Estágio 14):** a linha
`U_1/2` tem agora forma fechada geral-`b` provada para as quatro
constantes agudas mais usadas (`p=1,2,3,4`), fechando o item nomeado
pelo Estágio 9 nesse escopo; `p\ge5` permanece aberto, mas com seu
único obstáculo identificado e mostrado removível por um argumento de
uma linha — um alvo concreto e barato para uma frente futura, não mais
uma incógnita estrutural. Fontes completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/ATTEMPT.md`,
`.../general_b_dstar_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 15 — 2026-08-23]

**Onda 14, frente (c), `DISC-DEC-057`/`DISC-DEC-061`
(`CONJECTURE-1-K2-ATTEMPT`).** Alvo: §8 Conjectura 1
(`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`), provada apenas em `K=1` (§5.3) desde a
criação deste documento — o item 5 da lista de gaps do §9.

### O que foi provado

> **Teorema (este documento, PROVADO módulo uma citação clássica).**
> `\displaystyle f_{M_2}(x) = 4x(1-x^2)` em `(0,1)`, exatamente —
> a instância `K=2` da Conjectura 1.

Método: generaliza a computação whole-space do §5.3 (`K=1`) a `K=2`.
Duas fontes de reroteamento `x_1,x_2\sim\mathrm{Unif}(0,1)` i.i.d.
dividem `[0,1]` em duas "massas de região" `(m_1,m_2)` cuja lei
conjunta é **exatamente uniforme** na triângulo `T=\{m_1,m_2>0,
m_1+m_2<1\}` (Lema 1) — provado módulo a propriedade clássica de
amostragem size-biased/residual de `PD(1)` (McCloskey 1965;
Patil–Taillie 1977; Pitman, *Combinatorial Stochastic Processes*,
St-Flour 2002, Cap. 3), a **mesma** citação que a Proposição 2.4 deste
documento já usa sem re-derivação, e adicionalmente apoiada por um
argumento combinatório finito-`n` autocontido. As `9` combinações de
onde os dois destinos `u_1,u_2` pousam colapsam em `4` grupos mutuamente
exclusivos com densidades exatas `f_A(x)=2x^2(1-x)`,
`f_B(x)=f_C(x)=x(1-x^2)`, `f_D(x)=2x(1-x)`, cuja soma simbólica é
exatamente `4x(1-x^2)`. Subprodutos: reproduz `E[M_2]=8/15=\varphi_2`
(já conhecido) e estabelece **novo** `E[M_2^2]=1/3`. A redução `K=1`
do mesmo método reproduz exatamente `f_{M_1}(x)=2x` (§5.3), confirmando
o método geral, não apenas a tabela específica de `K=2`.

**O que NÃO foi fechado:** `K\ge3` — não tentado, sem alegação feita.
A explosão combinatória do número de configurações de destino cresce
com `K`, ecoando exatamente o mesmo diagnóstico que
`k2_open_lemma/ATTEMPT.md` dá para seu próprio problema *diferente*
(a ponte `n\to\infty`) explodir além de `K=2`.

> [Correção pós-adversarial, 2026-08-24 — `DISC-DEC-065`] `K=3`
> **foi** tentado na onda 15 e fechou por completo, inesperadamente —
> a explosão combinatória diagnosticada acima não se materializou.
> [Ver Estágio 17 abaixo para a prova completa e sua verificação
> adversarial.]

### Verificação adversarial independente

A sessão orquestradora re-derivou, do zero, toda a cadeia
simbólica/algébrica (as quatro probabilidades de grupo somando a `1`,
os quatro densidades de grupo via marginalização própria, a soma exata
a `4x(1-x^2)`, os momentos, e a redução `K=1`) antes de despachar um
referee hostil dedicado, que re-derivou o restante do zero: o Lema 1
(via um modelo gerativo genuinamente diferente — simulação de
permutação discreta que não toca a maquinaria contínua `PD(1)`/
stick-breaking, três escalas `n=300,1000,3000`, tendência de
convergência limpa conforme `n\to\infty`); a tabela de mecanismo de `9`
células (`260.000` testes exatos, `100%` de acerto, incluindo casos-
limite de colisão de destino e ponto fixo — o nível mais granular já
testado nesta linha); o enquadramento "mesma citação da Proposição
2.4" (confirmado ser a mesma jogada metodológica já aceita pelo §5.3
deste documento); e re-confirmou a densidade agregada a `n=20.000`
(`2×` a escala da própria frente).

> **Veredito: SOUND WITH NAMED ISSUES (um, menor, não-substantivo) —
> "ACCEPT for catalogue."** Nenhum erro matemático encontrado em lugar
> algum. Único achado: uma rotulagem de citação imprecisa dentro da
> prova do Lema 1 do próprio documento-alvo (uma invocação da mesma
> propriedade subjacente citada como "Fact A, PROVADO" em vez do fato
> clássico direto, exatamente como o parágrafo seguinte do mesmo
> documento já faz corretamente) — sem efeito sobre a validade da prova,
> confirmado independentemente e corrigido via correção datada.

Ver `theorem/conjecture1_k2_attempt/ATTEMPT.md` e
`.../conjecture1_k2_attempt/adversarial/REFEREE_REPORT.md` para os
relatórios completos.

### O que isto muda, precisamente

**Conjectura 1 (§8) está agora PROVADA em `K=2`**, além do `K=1` já
provado desde §5.3 — a primeira instância `K\ge2` da lei distribucional
completa a ser fechada. `K\ge3` permanece exatamente tão aberto quanto
antes; nenhuma tentativa ou alegação é feita para `K\ge3`. Conjectura 2
(§8, a mistura de Poisson sobre a Conjectura 1) permanece CONJECTURA —
herda o fechamento de `K=2` como um componente a mais confirmado da
mistura, mas continua condicional a `K\ge3` para ser totalmente
fechada. Nenhum resultado anterior é enfraquecido: a classificação
`U_{1/2}` no limite `n\to\infty`, todos os Teoremas/Estágios anteriores,
e a própria Conjectura 1 em `K=1` (§5.3) permanecem exatamente como
estavam.

**O que permanece aberto, sem mudança:** Conjectura 1 para `K\ge3`;
Conjectura 2 em geral (herda o gap acima); a forma fechada geral-`b`
das constantes agudas para `p\ge5` (Estágio 14); `\sup_K M_K/\sqrt K
=a^*` (Estágio 13). Nenhuma alegação de progresso em Millennium
Problem; matemática combinatória pura interna a este arquivo.

> [Correção pós-adversarial, 2026-08-24 — `DISC-DEC-065`] Conjectura 1
> em `K=3` não está mais aberta — fechada na onda 15. [Ver Estágio 17
> abaixo.] `K\ge4` permanece aberto, sem nenhuma tentativa registrada.

**Veredito honesto atualizado (ao fim do Estágio 15):** a linha
`U_1/2` tem agora a lei distribucional completa provada em `K=1,2`
(módulo, em ambos os casos, a mesma citação clássica já aceita pela
Proposição 2.4 do próprio documento) — a primeira extensão de
Conjectura 1 além do caso base desde sua formulação. `K\ge3` continua
sem nenhuma tentativa registrada nesta linha; a explosão combinatória
do número de configurações nomeada por esta e por frentes anteriores
como a razão estrutural provável permanece a melhor explicação
disponível para por que o método não se generaliza trivialmente.
Fontes completas: `theorem/conjecture1_k2_attempt/ATTEMPT.md`,
`.../conjecture1_k2_attempt/adversarial/REFEREE_REPORT.md`.

> [Correção pós-adversarial, 2026-08-24 — `DISC-DEC-065`] Este
> "veredito honesto" descrevia o estado ao fim do Estágio 15. `K=3`
> fechou na onda 15 (Estágio 17), inesperadamente. [Ver Estágio 17
> abaixo.]

---

## [Extensão, Estágio 16 — 2026-08-24]

**Onda 15, frente (a), `DISC-DEC-063`
(`GENERAL-P-DSTAR-CLOSURE-ATTEMPT`).** Alvo: item 11 do scorecard de
`general_b_dstar_attempt/ATTEMPT.md` — a forma fechada geral-`p` das
constantes agudas `D^{*(p)}_r(b)`, `p\ge5`, cuja obstrução nomeada
(padrão de cancelamento de `I_{2k+1}`) o referee da onda 14 já havia
mostrado ser mecanicamente removível (Estágio 14), sem executar a
montagem completa.

### O que foi provado

A montagem mecânica foi executada: os quatro ingredientes do
Estágio 14 (grau/anulamento de `Q_p(u)`; momentos centrais de
`\mathrm{Bin}(N,\tfrac12)`; a identidade de paridade binomial já
citada; o colapso geral-`k` do prefator) foram implementados como
algoritmos parametrizados por `p` — não ajustados caso a caso — via
identidades de Newton (`Q_p`) e uma extração por função geradora de
cumulantes (momentos), e rodados para `p=1,\ldots,10` (o dobro do
mínimo `p=5,6` do mandato).

> **Teorema (este documento, PROVADO dado os ingredientes já citados).**
> Para todo `p=1,\ldots,10` e todo `b\ge0`, `D^{*(p)}_r(b)` tem forma
> fechada exata, produzida por um único algoritmo geral-`p`.

`26.710` checagens exatas contra Corolário A3 (tabela de Stirling
própria), `0` divergências; reduz caractere-por-caractere às seis
fórmulas já provadas em `b\in\{0,1\}` e re-deriva de forma
independente as cinco instâncias `b\ge2` que o documento-pai só havia
verificado numericamente. Novas formas fechadas para `p=5,6,7` são
produzidas e impressas.

### Verificação adversarial independente

Um referee hostil dedicado re-verificou cada peça com métodos
deliberadamente diferentes dos do próprio documento (rota de
interpolação de Lagrange para `Q_p` e momentos, em vez de identidades
de Newton/função geradora de cumulantes; tabela de Stirling e
implementação de Corolário A3 próprias), sem ler nenhum script da
própria frente: `18.653` checagens independentes, `0` divergências,
incluindo uma extensão de escala para `p=5,6` até `r=200,b=30`
(igualando a escala máxima do documento-pai, `2,5×` além da escala do
próprio documento desta frente) e re-verificação dedicada dos casos de
contorno do erro auto-capturado da frente (`i=1`, `i=b` na fórmula de
peso da faixa).

O referee foi além do exigido: construiu uma **prova indutiva**
(usando apenas `(E2)` — uma identidade elementar de uma linha — e a
recursão de `S_{2k-1}` já citada do Estágio 14) de que a máquina
`H_k(r,b)` deste documento é correta para **todo** `k`, não apenas os
valores testados numericamente — fechando analiticamente, não apenas
numericamente, a lacuna que o próprio documento nomeou como seu maior
risco (cobertura direta de força bruta parando em `k=7`; a montagem
para `p=9,10` precisa de `k` até `9,10`).

> **Veredito: SOUND. "ACCEPT for catalogue."** Nenhum erro encontrado
> em lugar algum — nem na aritmética, nem na tabela de calibração, nem
> no enquadramento de honestidade. Único achado uma nuance de redação
> não-substantiva (dois limites de `k` diferentes, referindo-se a
> coisas diferentes, cada um individualmente correto), já tornada
> irrelevante pela prova indutiva do próprio referee.

Ver
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/general_p_dstar_closure_attempt/ATTEMPT.md`
e
`.../general_p_dstar_closure_attempt/adversarial/REFEREE_REPORT.md`
para os relatórios completos.

### O que isto muda, precisamente

**O item 11 do scorecard de `general_b_dstar_attempt/ATTEMPT.md` está
agora FECHADO para `p=1,\ldots,10`, todo `b\ge0`** — a forma fechada
geral-`b` das constantes agudas `D^{*(p)}_r(b)`, deixada aberta pelo
Estágio 9 para `b\ge2` e parcialmente fechada pelo Estágio 14 apenas
até `p=4`, agora se estende a dez valores de `p`. Adicionalmente, a
prova indutiva do referee estabelece que a máquina de colapso
`I_{2k+1}` subjacente é correta **para todo `k`**, não apenas os
valores usados até `p=10` — fortalecendo a confiança de que estender
a `p>10` é uma questão puramente computacional (custo de
`sympy.cancel`/interpolação), não uma incerteza matemática residual,
embora nenhuma montagem além de `p=10` tenha sido executada. Nenhum
resultado anterior é enfraquecido: Corolário A3, Teorema 3′, o
Teorema D1 e as fórmulas do Estágio 14 permanecem exatamente como
provados, agora casos particulares do algoritmo geral.

**O que permanece aberto, sem mudança:** `p>10` — nenhuma montagem
explícita foi executada além de `p=10`, apesar da máquina subjacente
estar agora provada correta para todo `k` (a barreira restante é de
custo computacional de interpolação/cancelamento simbólico, não de
correção matemática). A soma da faixa continua sendo deixada como
soma explícita de `b` termos, por desenho. Nenhuma alegação uniforme-
em-`K` ou de uma fórmula elementar única `p`-livre é feita — o próprio
documento nomeia explicitamente que `Q_p(u)` tem grau `2p` genuíno e
não há evidência de forma elementar uniforme em `p`.

**Veredito honesto atualizado (ao fim do Estágio 16):** a linha
`U_1/2` tem agora forma fechada geral-`b` provada para dez valores de
`p` (`1,\ldots,10`), com a maquinaria subjacente (`H_k`) agora provada
correta para todo `k` por indução — fechando o item 11 do Estágio 14
em escopo bem além do mínimo mandatado (`p=5,6`). `p>10` permanece
aberto apenas por não ter sido executado, não por incerteza
matemática.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-070`] A montagem
> foi executada e verificada também para `p=11,\ldots,20` na onda 16.
> [Ver Estágio 21 abaixo.] `p>20` permanece aberto apenas por escopo.

Fontes completas:
`k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/general_p_dstar_closure_attempt/ATTEMPT.md`,
`.../general_p_dstar_closure_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 17 — 2026-08-24]

**Onda 15, frente (b), `DISC-DEC-063`/`DISC-DEC-065`
(`CONJECTURE-1-K3-ATTEMPT`).** Alvo: §8 Conjectura 1
(`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`), provada em `K=1` (§5.3) e `K=2`
(Estágio 15) — este documento tenta `K=3`. Dispatch feito com a
expectativa explícita, compartilhada por duas frentes anteriores
nesta linhagem, de que a explosão combinatória do número de
configurações de destino impediria o fechamento em `K=3`; um
não-fechamento honesto era o resultado esperado e plenamente aceitável.

### O que foi provado

> **Teorema (este documento, PROVADO módulo uma citação clássica).**
> `\displaystyle f_{M_3}(x) = 6x(1-x^2)^2` em `(0,1)`, exatamente —
> a instância `K=3` da Conjectura 1.

Método: generaliza o mesmo método whole-space de `K=1,2` a `K=3`.
Três fontes de reroteamento `x_1,x_2,x_3\sim\mathrm{Unif}(0,1)` i.i.d.
dividem `[0,1]` em três "massas de região" `(m_1,m_2,m_3)` cuja lei
conjunta é **exatamente uniforme** (densidade `3!=6`) no simplex
`\Delta=\{m_1,m_2,m_3>0,\ m_1+m_2+m_3<1\}` (Lema 1, generalizado a
`K=3` via um split de casos em `5` padrões pelo particionamento em
co-blocos de `\{x_1,x_2,x_3\}`), provado módulo a mesma propriedade
clássica de amostragem size-biased/residual de `PD(1)` já usada em
`K=1,2`, aplicada recursivamente (duas vezes, a segunda uma instância
direta da representação GEM(1)/stick-breaking em múltiplos passos, não
uma extrapolação), mais uma peça de maquinaria genuinamente nova —
os "gaps rotulados" seguem `\mathrm{Dirichlet}(1,1,1)`, verificada por
dois argumentos independentes (simetria/exchangeability geral e
mudança-de-variáveis explícita por ordenação cíclica). As `64`
combinações brutas de onde os três destinos `u_1,u_2,u_3` pousam
colapsam, via o fato-chave "nós fora-do-ciclo contribuem massa cíclica
nova exatamente zero, independentemente do alvo," em apenas `7` formas
mutuamente exclusivas (`T0=16, T1a=24, T1b=9, T1c=2, T2a=9, T2b=3,
T3=1`, soma `64`), com probabilidades-alvo exatas `9/20, 1/8, 1/60,
1/8, 1/40, 1/120, 1/4` (soma `1`) e densidades condicionais fechadas
cuja soma simbólica é exatamente `6x(1-x^2)^2`. Subprodutos: novos
momentos `E[M_3]=16/35=\varphi_3`, `E[M_3^2]=1/4`, `E[M_3^3]=16/105`.
A redução `K=2` do mesmo método reproduz exatamente `f_{M_2}(x)=
4x(1-x^2)` (Estágio 15), confirmando o método geral. O documento
autodivulga três bugs autocapturados-e-corrigidos no processo (um bug
de classificação de ciclos, um bug na fórmula de posição discreta, um
miscount na checagem de redução `K=2`) — nenhum sobrevive à versão
final.

**O que NÃO foi fechado:** `K\ge4` — explicitamente não tentado, sem
alegação feita (§7 do documento-alvo). O documento oferece apenas uma
discussão informal, *post hoc*, de por que `K=3` funcionou apesar da
expectativa de explosão (o colapso `64\to7` via "fora-do-ciclo
contribui zero" é mais forte do que a contagem bruta `4^K` sugeria) —
explicitamente não uma prova de que a mesma tratabilidade persiste
além de `K=3`.

### Verificação adversarial independente

A sessão orquestradora re-derivou, do zero, a classificação
`64\to7` e re-derivou simbolicamente duas das sete densidades de forma
(`T3`, `T1c`, incluindo o caso topologicamente novo do 3-ciclo) antes
de despachar um referee hostil dedicado, briefado explicitamente para
caçar ativamente a falha que explicaria a surpresa, não apenas
verificar alguns números. O referee re-derivou do zero: o Lema 1
completo, incluindo a peça genuinamente nova (`\mathrm{Dirichlet}
(1,1,1)` rotulado, verificada por dois métodos independentes) e o uso
duplo da citação recursiva (confirmado ser uma instância legítima da
representação GEM(1) em múltiplos passos); as **sete** densidades de
forma (não apenas as duas pré-checadas) via integração simbólica 3D
exata mais um Monte Carlo contínuo independente de `8.000.000`
amostras com uma terceira implementação de classificação, testando
todas as sete formas fechadas via KS (`p` de `0.17` a `0.84`, nenhuma
rejeição); a checagem de mecanismo discreto, reconstruída inteiramente
do zero (`26.000` testes, `0` divergências, todas as `64` células
brutas atingidas, com `n=30` estressando deliberadamente colisões e
pontos fixos a quase `10\%` cada); e a redução `K=2` (R2, `4.000.000`
amostras, todos os `4` grupos batendo).

> **Veredito: SOUND — "ACCEPT for catalogue."** Nenhum erro
> matemático encontrado em lugar algum. Único achado: uma lacuna de
> exposição menor, não-substantiva — o esboço de prova de "fora-do-
> ciclo contribui zero" no documento-alvo não detalha explicitamente
> um subcaso sutil (um redirecionamento fora-do-ciclo pousando dentro
> de um arco já periódico); o referee verificou à mão que a alegação
> permanece válida mesmo nesse subcaso — não é um erro, é uma nota de
> completude de rigor, sem efeito sobre o veredito. A surpresa se
> resolve exatamente como o próprio documento explica: a explosão
> bruta `4^K` diagnosticada por duas frentes anteriores nunca ocorre
> de fato, porque "fora-do-ciclo contribui zero" colapsa a contagem ao
> número (bem menor, ainda que crescente) de estruturas de ciclo em
> `K` itens rotulados, e esse número menor ainda é tratável em `K=3`.

Ver
`theorem/conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md` e
`.../conjecture1_k3_attempt/adversarial/REFEREE_REPORT.md` para os
relatórios completos.

### O que isto muda, precisamente

**Conjectura 1 (§8) está agora PROVADA em `K=1,2,3`** — um fechamento
inesperado, além da expectativa de dispatch de não-fechamento por
explosão combinatória compartilhada por duas frentes anteriores nesta
linhagem. `K\ge4` permanece exatamente tão aberto quanto `K\ge3`
estava antes deste estágio; nenhuma tentativa ou alegação é feita para
`K\ge4`, e a discussão informal de por que `K=3` funcionou
explicitamente não se estende a uma previsão de tratabilidade além
dele. Conjectura 2 (§8, a mistura de Poisson sobre a Conjectura 1)
permanece CONJECTURA — herda o fechamento de `K=3` como mais um
componente confirmado da mistura, mas continua condicional a `K\ge4`
para ser totalmente fechada. Nenhum resultado anterior é enfraquecido:
a classificação `U_{1/2}` no limite `n\to\infty`, todos os Teoremas/
Estágios anteriores, e a própria Conjectura 1 em `K=1,2` permanecem
exatamente como estavam.

**O que permanece aberto, sem mudança:** Conjectura 1 para `K\ge4`
[Ver Estágio 20 abaixo — `K=4` PROVADO em 2026-08-25; `K\ge5`
permanece aberto]; Conjectura 2 em geral (herda o gap acima); a forma
fechada geral-`b` das constantes agudas para `p>10` (Estágio 16)
[Ver Estágio 21 abaixo — estendida a `p=1,\ldots,20` em 2026-08-25];
`\sup_K M_K/\sqrt K=a^*` (Estágio 13) [Ver Estágio 19 abaixo —
PROVADO em 2026-08-25]; a forma fechada completa do piso `H2` em `b=1`
(onda 14, frente (b), diagnosticada como mesma dificuldade que
Conjectura 1 geral-`K`). Nenhuma alegação de progresso em Millennium
Problem; matemática combinatória pura interna a este arquivo.

**Veredito honesto atualizado (ao fim do Estágio 17):** a linha
`U_1/2` tem agora a lei distribucional completa provada em `K=1,2,3`
(módulo, em todos os casos, a mesma citação clássica já aceita pela
Proposição 2.4 do próprio documento, aplicada recursivamente para
`K=3`) — um fechamento inesperado que contraria o diagnóstico de
explosão combinatória de duas frentes anteriores. `K\ge4` continua
sem nenhuma tentativa registrada nesta linha; a discussão informal
*post hoc* de por que `K=3` funcionou é explicitamente não uma prova
de tratabilidade contínua, e nenhuma extrapolação além de `K=3` é
alegada por nenhum documento desta linhagem. Fontes completas:
`theorem/conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md`,
`.../conjecture1_k3_attempt/adversarial/REFEREE_REPORT.md`.

---

## [Extensão, Estágio 18 — 2026-08-25]

**Onda 16, frente (e), `DISC-DEC-066`/`DISC-DEC-067`
(`CONJECTURE-2-DIRECT-ATTEMPT`).** Alvo: §8 Conjectura 2 (a lei
distribucional incondicional completa, `M(c)\overset{d}{=}
\min(1,\sqrt{E/c})`), por uma rota **direta** — que não passe por
provar a Conjectura 1 caso-a-caso para todo `K` (infactível em
princípio: "todo `K`" não é uma lista finita). Frente despachada como
a de maior risco da onda, com não-fechamento honesto pré-declarado
plenamente aceitável.

### O que aconteceu

> **Não-fechamento honesto, com progresso parcial estrutural provado
> e uma refutação rigorosa de rota.** Nenhuma prova direta, completa
> ou parcial, da Conjectura 2 é alegada.

O que ficou estabelecido, no tier de cada alegação:

**(i) A arquitetura do método dos momentos (PROVADA como
correta-se-completada).** `M(c)\in[0,1]` q.c., logo sua lei é
determinada pela sequência de momentos (problema de momentos de
Hausdorff, determinado em suporte compacto — citação clássica); e
cada momento reduz, pelo mesmo dispositivo Fubini/exchangeability que
o Teorema 1 já usa para a média, a uma probabilidade cíclica conjunta
de `p` pontos que nunca fixa `K`. Se completada para todo `p`, seria
uma prova direta integral. O referee registrou como bônus o momento
geral-`p` da lei conjecturada:
`E[\min(1,\sqrt{E/c})^p]=e^{-c}+\gamma(p/2{+}1,c)/c^{p/2}`.

**(ii) Novos alvos em forma fechada (PROVADOS como computações sobre
a lei conjecturada — alvos, não evidência).**
`E[M(c)^2]=(1-e^{-c})/c` e `E[M_K^2]=1/(K{+}1)` — incondicionais
apenas em `K\le3` (âncoras via as densidades já provadas: `1/2, 1/3,
1/4`, re-verificadas pelo referee); conjecturais no geral, exatamente
como as Conjecturas 1–2. Não constavam em nenhum lugar deste
documento antes.

**(iii) A redução por estrutura de blocos do caso `p=2` (PROVADA,
elementar).** `P(\text{mesmo bloco})=1/2`; densidades condicionais
exatas nos dois casos — cada fato cruzado contra enumeração exata
finita (`n=2,\ldots,7` pela frente; estendida a `n=8` pelo referee,
que ainda a fortaleceu: toda célula das tabelas discretas vale
exatamente `(n-2)!`).

**(iv) O certificado de bloco intacto (PROVADO).** Limite inferior
exato `e^{-ct}` dentro do caso difícil, com verificação de
zero-violações por simulação (frente e referee, seeds distintos).

**(v) Refutação da rota Poissonization-em-`c` (PROVADA, com os dois
reparos do referee incorporados).** Sob o acoplamento natural em que
marcas só são adicionadas conforme `c` cresce, `\{M(c)\}` NÃO é
monótono por trajetória — contraexemplo exato (`n=6`: adicionar um
segundo reroute AUMENTA a contagem cíclica de `3` para `5`, ao fechar
um 2-ciclo novo em território morto) — e o scan exaustivo do referee
(9 subidas / 7 descidas / 14 neutras a partir de UMA mesma
configuração) fecha também a refutação de qualquer função de direção
determinística em `M`. Uma equação-mestra fechando no escalar `M(c)`
está descartada por essa via.

**(vi) A obstrução, localizada com precisão (ABERTA).** O passo
genuinamente difícil — já em `p=2` — é que o dispositivo de exploração
de um ponto (Definição 3) abstrai exatamente a informação de destino
físico que uma exploração *conjunta* de dois pontos precisa; uma
re-derivação a partir da Definição 2 é o sub-problema preciso, bem
posto e não resolvido. O documento nota (como pista, não alegação)
que essa mesma peça nova — uma exploração conjunta não-marginalizada —
é plausivelmente a chave comum tanto para a rota direta da Conjectura
2 quanto para o caso geral-`K` da Conjectura 1.

### Verificação adversarial independente

Referee hostil dedicado, sem ler nenhum script da frente: re-derivou
as duas formas fechadas por duas rotas simbólicas cada; re-enumerou as
checagens discretas do zero até `n=8` (fortalecendo-as); re-verificou
o certificado de bloco intacto com seeds frescos (0 violações em 6.519
trials intactos, `c=1` e `c=4`); verificou o contraexemplo à mão e por
dois algoritmos independentes; reproduziu os padrões exploratórios de
`g(\ell)`/`\rho(\ell)`; e auditou a disciplina de rotulagem
honesta linha a linha.

> **Veredito: SOUND WITH NAMED ISSUES (quatro, todos menores) —
> "ACCEPT for catalogue" no tier reivindicado.** Nenhum erro em
> nenhuma computação exata/PROVED. Os quatro achados — um qualificador
> de condicionalidade ausente nos rótulos de tabela; duas lacunas de
> nível de prova no escopo do §4 (ponte finito→contínuo; ambas as
> direções a partir de um só estado), ambas reparadas pelo próprio
> referee; e uma frase super-assertiva no §6 — foram corrigidos por
> adendos datados no documento-alvo.

Ver `theorem/conjecture2_direct_attempt/ATTEMPT.md` e
`.../conjecture2_direct_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**A Conjectura 2 permanece CONJECTURA — nada muda em seu status.**
O que muda: (a) a rota direta tem agora uma arquitetura precisa e
correta-se-completada (momentos), com o caso `p=2` reduzido à sua
metade fácil e a metade difícil localizada com exatidão; (b) a rota
alternativa mais natural (equação-mestra via Poissonization-em-`c`
no escalar `M(c)`) está **descartada por refutação rigorosa**, não
por impressão; (c) dois alvos de momento em forma fechada estão
registrados para qualquer tentativa futura testar contra; (d) uma
pista estrutural unificadora (a exploração conjunta como chave comum
às duas conjecturas) está nomeada. Nenhum resultado anterior é
tocado.

**O que permanece aberto, sem mudança:** Conjectura 2 em geral
[Ver Estágio 24 abaixo — 2026-08-26: PROVADA como corolário indireto,
não pela rota direta desta frente, que permanece exatamente como
registrado acima]; a exploração conjunta de `p\ge2` pontos (o novo
sub-problema nomeado — permanece seu próprio problema aberto, mesmo
após o fechamento indireto) [Ver Estágio 25 abaixo — 2026-08-26: um
primeiro resultado genuíno nesta linha, o Teorema J de restrição
cíclica uniforme, provado; não fecha os alvos de momento (já fechados
por outra rota no Estágio 24), mas é progresso real na maquinaria de
exploração conjunta em si]; Conjectura 1 para `K\ge4` (sob revisão
adversarial na própria onda 16) [Ver Estágio 24 abaixo — fechada para
todo `K` em 2026-08-26]; `\sup_K M_K/\sqrt K=a^*` (idem); `p>20` de
`D^{*(p)}_r(b)` (idem); o piso `H2` em `b=1` (idem); a lei de escala
`\gamma\in(0,1)` (caracterizada, não provada, sem frente ativa).
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 19 — 2026-08-25]

**Onda 16, frente (b), `DISC-DEC-066`/`DISC-DEC-068`
(`SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT`).** Alvo: o supremo
`\sup_K M_K/\sqrt K = a^*` — o gap mais difícil nomeado pelo Estágio
13, na **terceira tentativa** (duas rotas anteriores documentadas como
falhas: a recursão exata de `Q(n)`, refutada por contraexemplo; o
limitante pontual direto por afiação from-scratch de ambos os lados,
julgado delicado demais).

### O que foi provado

> **Teorema (este documento, PROVADO).** `M_K < a^*\sqrt K`,
> estritamente, para **todo** inteiro `K\ge1`.

> **Corolário (fecha o gap do Estágio 13).**
> `\displaystyle \sup_K \frac{M_K}{\sqrt K} = a^*` **exatamente** —
> e o supremo é aproximado mas nunca atingido em nenhum `K` finito
> (todo passo da cadeia é estrito), confirmando como teorema a
> observação numérica das duas frentes anteriores.

Rota, genuinamente diferente das duas que falharam: duas citações
clássicas reais — o limite de Stirling explícito de Robbins (1955) e
o Teorema 7 de Flajolet–Grabner–Kirschenhofer–Prodinger (1995, "On
Ramanujan's `Q`-function", J. Comput. Appl. Math. 58: `θ(n)=\tfrac13+
\tfrac4{135(n+k(n))}` com `k(n)\in[\tfrac2{21},\tfrac8{45}]` para
TODO `n\ge0`, resolvendo uma conjectura da primeira carta de Ramanujan
a Hardy, 1913) — combinadas com a identidade elementar clássica
`Q(n)=\tfrac{n!e^n}{2n^n}-θ(n)` (eq. (1.4) do próprio FGKP95; ver
correção S-1) para produzir um limitante superior **não-assintótico**
totalmente explícito:
`Q(n) < \sqrt{\pi n/2} - \tfrac13 + \tfrac1{11}\sqrt{\pi/(2n)}`
(Teorema 1). O outro lado precisou de **zero trabalho novo**: o
`z_K`-bound do Lema 4.1, exatamente como já provado, basta —
corrigindo com precisão o diagnóstico da tentativa anterior de que
ambos os lados precisavam de afiação. O passo final numericamente
decisivo (`\mathrm{LHS}(1)<1/3`) é provado por aritmética racional
pura, sem confiança em ponto flutuante.

**Consequência imediata para a hipótese (U'):** o caso genérico
(`1\le K\le n-1`) da hipótese (U') sobe imediatamente para a constante
nítida: `|φ_n^{(K)}-φ_K| < a^*\sqrt K/n`. O caso de contorno `K=n`,
explicitamente NÃO tentado pela frente (que o nomeou como próximo
alvo), foi **fechado pelo próprio referee** (§8 do relatório): a
conversão de índice perde apenas `O(1/\sqrt n)` — não `O(1)` como a
frente diagnosticara — e um argumento de meia página com ferramentas
já aceitas (lado superior `n\ge3` via `3c^2<1`; lado inferior `n\ge67`
via Teorema 5; resto finito `n\le80` verificado exato) fecha
`|Q(n)-nφ_n|<a^*\sqrt n` para todo `n\ge1`. A sessão orquestradora
re-verificou o argumento do referee independentemente (álgebra à mão;
`0` violações em verificação racional certificada, `n=1..300`;
âncoras exatas `1/3` em `n=1` e `13/30` em `n=2`). **Com isso, a
hipótese (U') vale com a constante nítida `a^*` em todos os casos
`0\le K\le n`.** A substituição mecânica de `a=1+\sqrt{\pi/2}` por
`a^*` na taxa explícita do Estágio 12 (`|Δ_n(c)|\le[a\sqrt c+0{,}2805]/n`)
NÃO foi executada nem verificada por ninguém — a montagem do Estágio
12 precisa ser re-percorrida com a nova constante antes de qualquer
taxa nítida ser afirmada; item nomeado como próximo passo trivial-mas-
não-executado. [Ver Estágio 22 abaixo — executado em 25/08/2026, onda
17 frente (b): todos os passos sobrevivem verbatim, constante aditiva
inalterada.]

### Verificação adversarial independente

A sessão orquestradora fez seu próprio spot-check antes do despacho
(identidade final do Lema 1 exata em `n=1..300` — encontrando,
independentemente, o mesmo typo de índice que o referee depois nomeou
como E-2; limites de `θ(n)`; Teorema 1; o passo racional final por
intervalos próprios; `M_K<a^*\sqrt K` com cota racional certificada).
O referee hostil dedicado então: **buscou e leu o PDF primário do
FGKP95** (arquivo do INRIA Algorithms Project), confirmando o Teorema
7 palavra por palavra (enunciado, numeração, "for all integers
`n\ge0`", estrutura da prova `n\ge116` + verificação exaustiva,
detalhes de proveniência); verificou Robbins na forma usada em 2.006
pontos até `n=10^8`; auditou o Lema 1 caractere por caractere
(encontrando E-1/E-2); re-derivou toda a cadeia dos Teoremas 1–2
incluindo a borda `n=1`; re-provou o final racional com inteiros
próprios E re-verificou os inteiros do documento um a um; e empurrou
a verificação exata de `M_K<a^*\sqrt K` a `K=10.000` (3× a
profundidade da frente), zero violações em ~5.000 pontos combinados.

> **Veredito: SOUND WITH NAMED ISSUES — "ACCEPT for catalogue"**, com
> dois erratas obrigatórios e três notas, nenhum invalidando teorema
> algum: **E-1** — a exibição da citação de Robbins omite `(n/e)^n` e
> é falsa como impressa (a forma USADA na prova é a correta); **E-2**
> — dois intermediários impressos da prova do Lema 1 são falsos
> (deslize de índice na substituição `k:=n-j`; a identidade FINAL é
> verdadeira e foi re-provada duas vezes); **S-1** — a identidade é
> clássica (FGKP95 eq. (1.4)), não nova; **S-2** — o diagnóstico do
> caso de contorno estava quantitativamente errado na direção segura,
> e o referee o fechou construtivamente; **N-1** — conflação
> cosmética `v_n`/`z_n`. Todos corrigidos via adendos datados no
> documento-alvo.

Ver `.../sharp_constant_monotonicity_attempt/ATTEMPT.md` e
`.../sharp_constant_monotonicity_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**O gap do Estágio 13 está FECHADO: `\sup_K M_K/\sqrt K=a^*`,
exatamente.** A hipótese (U') vale agora com a constante nítida `a^*`
para todos os `0\le K\le n` (caso genérico pela frente; caso de
contorno pelo referee, verificado pela sessão; `K=0` trivial).
Nenhum resultado anterior é enfraquecido: Estágios 12–13, Lema 4.1,
Teoremas 3/5/6 permanecem exatamente como provados, usados por
citação.

**O que permanece aberto:** a re-execução da montagem do Estágio 12
com `a^*` no lugar de `a` (para uma taxa explícita nítida em `c`) —
não executada [Ver Estágio 22 abaixo — executada e fechada em
25/08/2026]; monotonicidade literal termo-a-termo de `M_K/\sqrt K`
(o documento prova `\sup=\lim`, que era o que se pedia — as duas
formulações não são logicamente idênticas, e a monotonicidade em si
segue apenas numericamente sugerida); Conjecturas 1 (`K\ge4`, sob
revisão na onda 16) e 2; `p>20`; o piso `H2` em `b=1`; a lei de
escala `\gamma\in(0,1)`. Nenhuma alegação de progresso em Millennium
Problem; matemática combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 20 — 2026-08-25]

**Onda 16, frente (a), `DISC-DEC-066`/`DISC-DEC-069`
(`CONJECTURE-1-K4-ATTEMPT`).** Alvo: §8 Conjectura 1 em `K=4`, após
`K=1,2,3` provados (§5.3, Estágios 15 e 17). Dispatch feito com risco
declarado incerto — o próprio documento de `K=3` nomeia a
continuidade da tratabilidade como "pergunta genuinamente nova, não
respondida" — e não-fechamento honesto plenamente aceitável.

### O que foi provado

> **Teorema (este documento, PROVADO módulo uma citação clássica).**
> `\displaystyle f_{M_4}(x) = 8x(1-x^2)^3` em `(0,1)`, exatamente —
> a instância `K=4` da Conjectura 1. **Segundo fechamento inesperado
> consecutivo nesta linha.**

Método: o mesmo whole-space de `K=1,2,3`, com três ingredientes novos
tratados explicitamente: (i) o Lema 1 generaliza via os `Bell(4)=15`
padrões de co-blocos, agrupados em 5 formas por tipo de partição —
cada padrão contribui a constante `\prod_j(b_j-1)!`, e uma observação
nova e elementar (a bijeção clássica partição-com-ordem-cíclica ↔
permutações) força `\sum\prod(b_j-1)!=K!=24` ANTES de qualquer
derivação probabilística; (ii) o fato de espaçamentos rotulados
`n=4` (`\mathrm{Dirichlet}(1,1,1,1)`), provado inline; (iii) a mesma
citação `PD(1)`, aplicada recursivamente até **três** vezes (um peel a
mais que `K=3`). As `5^4=625` configurações brutas de destino colapsam
em **12 tipos de forma** (`\sum_{s\le4}p(s)=12`, previsão
pré-registrada ANTES da enumeração), e o peso fora-de-ciclo
`W_C(Q)=1-Q` é verificado por enumeração simbólica bruta para todo
`n_{\mathrm{off}}\le4` — incluindo `n_{\mathrm{off}}=3`, o caso que
excede o máximo de `K=3` e não podia ser herdado. Soma simbólica
exata: `8x(1-x^2)^3`. Subprodutos: `E[M_4]=128/315=\varphi_4`,
`E[M_4^2]=1/5` (consistente com o `1/(K{+}1)` do Estágio 18),
`E[M_4^3]=128/1155`. Dois bugs auto-capturados divulgados (confusão
de escala residual-vs-absoluta na forma `3+1`, capturada pela checagem
pré-registrada de densidade constante; pitfall de `sympify` com
símbolo fresco no script de comparação da redução `K=3`). A redução
do método geral a `K=3` e `K=2` reproduz os resultados já revisados
grupo a grupo.

### Verificação adversarial independente

A sessão orquestradora re-verificou antes do despacho, com código
próprio: a classificação `625\to12` (contagens por `r_{\mathrm{on}}` e
constância de `N(r,n_{\mathrm{off}})`), `W_C=1-Q` por enumeração
própria até `n_{\mathrm{off}}=3`, a identidade de partições
(`2,6,24`), e as cinco densidades por grupo via marginalização própria
(fórmula integral re-derivada de primeiros princípios), com
probabilidades `1/5,2/5,2/7,1/10,1/70` e soma exata. O referee hostil
— briefado para caçar um possível **erro sistemático herdado por toda
a linhagem** — reconstruiu tudo por rotas ainda diferentes: os 15
padrões do Lema 1 individualmente (mais forte que o agrupamento por
exchangeability do documento); o fato `n=4` por duas rotas; uma
superfície nova de momentos exatos `p=0..8` sobre as 625 configurações
brutas SEM nenhuma maquinaria de colapso (45 momentos por grupo + 9
totais, todos exatos); mecanismo discreto do zero com oráculo
validado (110.000 trials, 0 divergências, todas as 625 células em
todas as escalas, incluindo `n=12` com 43% de colisões); Monte Carlo
contínuo de 8M com KS por grupo E por tipo-de-ciclo (teste que
nenhuma frente havia rodado — a independência de `\sigma` verificada
distribucionalmente); e simulação discreta bruta com ground truth por
pointer-doubling em `n=10000/20000/40000` — a última uma escala nunca
rodada pela frente, e a mais limpa (KS `p=0{,}97`). **O erro
sistemático procurado não existe em nenhuma superfície alcançável.**

> **Veredito: SOUND — "ACCEPT for catalogue."** Nenhum erro
> matemático encontrado em lugar algum. Único achado: uma nota
> cosmética herdada (a exposição comprimida do subcaso
> "redirecionamento dentro de arco periódico", já traçado
> explicitamente na correção pós-adversarial de `K=3`) — tratada por
> adendo datado. A surpresa dupla se dissolve por razão estrutural
> identificada: as três juntas do método (`\prod(b_j-1)!` somando a
> `K!` por bijeção; densidade dependendo só de `r_{\mathrm{on}}`;
> `W=1-Q` via a identidade de florestas ponderadas degenerando em
> `E+Q=1`) não têm conteúdo específico de `K` nos intervalos
> verificados.

Ver `theorem/conjecture1_k2_attempt/conjecture1_k3_attempt/conjecture1_k4_attempt/ATTEMPT.md`
e `.../conjecture1_k4_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**Conjectura 1 (§8) está agora PROVADA em `K=1,2,3,4`.** `K\ge5`
permanece aberto e explicitamente não tentado — mas com uma pista
concreta e bem posta nomeada para uma frente futura: provar a
identidade geral de florestas ponderadas `W(n)=1-Q` para todo `n`
(o que fecharia o único ingrediente genuinamente novo por `K` de uma
vez, em vez de um `K` por vez; o probe do referee registra ainda que
a fórmula geral do documento em `K=5` soma a `10x(1-x^2)^4`, e que
`W=1-Q` já está verificado em `n_{\mathrm{off}}=4` — restando o Lema 1
em `K=5` e `W` em `n_{\mathrm{off}}=5`). Conjectura 2 herda `K=4`
como mais um componente confirmado, permanecendo CONJECTURA. Nenhum
resultado anterior é enfraquecido.

**O que permanece aberto, sem mudança:** Conjectura 1 para `K\ge5`
[Ver Estágio 24 abaixo — fechada para todo `K` em 2026-08-26];
Conjectura 2 em geral [Ver Estágio 24 abaixo — fechada como corolário
em 2026-08-26]; a exploração conjunta de `p\ge2` pontos (Estágio 18);
a re-montagem do Estágio 12 com `a^*` (Estágio 19)
[Ver Estágio 22 abaixo — fechada em 25/08/2026];
`p>20` de `D^{*(p)}_r(b)` [Ver Estágio 21 abaixo]; o piso `H2` em
`b=1` (sob revisão na onda 16); a lei de escala `\gamma\in(0,1)`.
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 21 — 2026-08-25]

**Onda 16, frente (c), `DISC-DEC-066`/`DISC-DEC-070`
(`GENERAL-P-DSTAR-EXTENSION-ATTEMPT`).** Alvo: estender a montagem
geral-`p` de `D^{*(p)}_r(b)` (Estágio 16, `p=1,\ldots,10`) até
`p=20` — frente de execução, risco baixo por desenho, já que a
máquina `H_k(r,b)` fora provada correta para todo `k` pela indução do
referee da onda 15.

### O que foi executado e verificado

> **Resultado: o alvo completo do mandato, `p=11,\ldots,20`, fechado
> — `62.310` checagens exatas contra ground truth independente
> (Corolário A3, tabela de Stirling própria), `0` divergências, a
> `r\le200, b\le30` uniformemente para todos os dez novos `p`** — a
> maior escala já usada nesta linhagem, sem redução conforme `p`
> cresce.

Método idêntico ao Estágio 16 em conteúdo matemático; a única
engenharia nova são extrações mais rápidas (validadas cruzado,
caractere por caractere, contra as rotas lentas originais antes de
qualquer uso) dos mesmos dois objetos geradores: os momentos centrais
via a recorrência clássica de exponenciação de séries de potências
(mesma classe algorítmica das identidades de Newton), e `H_k` via
avaliação-e-interpolação exata. Novas formas fechadas impressas para
todo `p=11,\ldots,20` em `b=0,1` (mais instâncias `b=2,3`),
confirmando a persistência do padrão de denominador `(2r+3)`. Um bug
latente auto-capturado e divulgado (`sp.nsimplify` corrompendo
racionais exatos grandes — herdado de código dormante, nunca
exercitado, do documento-pai; capturado por uma varredura de
calibração falhando ruidosamente; a rota de verificação de produção
nunca o tocou).

### Verificação adversarial independente

A sessão orquestradora verificou antes do despacho, com Corolário A3
próprio: as formas impressas de `p=11` (`b=0,1,2`) em `123` pontos
incluindo a região de anulamento `r<p`. O referee hostil (sem ler
nenhum script da frente): re-derivou a recorrência de momentos e a
checou contra somatório binomial direto para **todo** `l=1..20`
(rota que a frente não usou); construiu uma **terceira rota** para
`H_k` (fatoração fechada `S_{2k-1}=A_k\cdot C(N,m{+}1)` derivada da
recursão aceita, sem interpolação alguma); **provou a cota de grau**
`\deg_r H_{2k-1}=k-1` (coeficiente líder `4^{k-1}(k-1)!`,
independente de `b`) — o único fato que a frente admitia como
empírico — e provou que o self-check da interpolação é determinístico
(um grau sub-estimado é capturado por qualquer ponto held-out;
`36/36` em testes de ajuste deliberadamente errado); replicou o grid
**inteiro** de `62.310` pontos com pipeline próprio sem `sympy` na
varredura, `0` divergências, mais um push de escala a `r=300` em
`p=15,20`; verificou as `26` formas impressas por duas vias; e
confirmou a divulgação do bug caractere por caractere. Total:
`75.899` checagens exatas, `0` divergências.

> **Veredito: SOUND — "ACCEPT for catalogue."** Dois achados menores
> apenas de documentação (uma contagem sub-declarada no tally do
> ground truth; um rótulo de scorecard comprimindo a então-empírica
> cota de grau — agora irrelevante, pois o referee a provou).
> Condições de integração atendidas: a prova da cota de grau entra no
> catálogo como PROVED, citada ao referee.

Ver `.../general_p_dstar_closure_attempt/general_p_dstar_extension_attempt/ATTEMPT.md`
e `.../general_p_dstar_extension_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**`D^{*(p)}_r(b)` está agora executado e verificado para
`p=1,\ldots,20`, todo `b\ge0`** — dobrando o alcance do Estágio 16 —
com a cota de grau `\deg_r H_{2k-1}(r,b)=k-1` agora **PROVADA**
(referee), removendo o último fato empírico da maquinaria. `p>20`
permanece aberto apenas por escopo: os próprios tempos das rotas
rápidas (sub-segundo em `p=20`) sugerem, sem provar, tratabilidade
continuada. Nenhum resultado anterior é enfraquecido.

**O que permanece aberto, sem mudança:** `p>20` (por escopo);
nenhuma fórmula elementar única livre-em-`p` é alegada (grau genuíno
`2p` de `Q_p`); Conjectura 1 `K\ge5`; Conjectura 2; a exploração
conjunta (Estágio 18); a re-montagem nítida do Estágio 12 (Estágio
19) [Ver Estágio 22 abaixo — fechada em 25/08/2026]; o piso `H2` em
`b=1`; `\gamma\in(0,1)`. Nenhuma alegação de
progresso em Millennium Problem; matemática combinatória pura
interna a este arquivo.

---

## [Extensão, Estágio 22 — 2026-08-25]

**Contexto.** O Estágio 19 fechou `\sup_K M_K/\sqrt K = a^*` e elevou a
hipótese (U') à constante nítida `a^*` em todos os casos `0\le K\le n`,
mas deixou explicitamente NÃO executada a substituição mecânica de
`a=1+\sqrt{\pi/2}` por `a^*` na taxa explícita do Estágio 12 — "a
montagem do Estágio 12 precisa ser re-percorrida com a nova constante
antes de qualquer taxa nítida ser afirmada". A onda 17, frente (b)
(`SHARP-RATE-REASSEMBLY-ATTEMPT`, DISC-DEC-072/073) executou exatamente
isso, sob a disciplina integral da linhagem (engine re-derivado da
prosa, nenhum script de frente anterior aberto, aritmética racional
certificada em toda checagem de carga; sem aleatoriedade — seeds
reservados não usados).

**Resultado central.**

> **Teorema R (PROVADO).** Para todo inteiro `n\ge4` e todo real
> `0\le c\le n`:
>
> `\displaystyle \big|φ(n,c)-φ_∞(c)\big| \;\le\; \frac{a^*\sqrt c + κ_B}{n},
> \qquad a^*=\sqrt π\Big(\frac1{\sqrt2}-\frac12\Big)=0{,}36708721\ldots,
> \quad κ_B=\sup_{c\ge0}c^2I_2(c)=0{,}28048017\ldots,`
>
> com desigualdade **estrita** para todo `c\in(0,n]`; forma-sup
> `\sup_{[0,C]}|Δ_n|\le(a^*\sqrt C+κ_B)/n` para `C\le n`; forma decimal
> `|Δ_n(c)| \le [0{,}3670873\sqrt c + 0{,}2805]/n`.

Três fatos estruturais sustentam a substituição, todos verificados
pelo referee contra a prosa-fonte: (i) a constante `a` entrava na prova
antiga em **exatamente um passo** (inserção de (U') na metade `A_n`
antes de Jensen), como caixa-preta sobre todo o suporte binomial
`0\le K\le n` — exatamente o que a (U') nítida do Estágio 19 fornece
(caso genérico via `M_K<a^*\sqrt K`; contorno `K=n` via o §8 do referee
do Estágio 19; `K=0` trivial; o caso `K=n-1` é coberto pelo caso
genérico em `n=K+1`); (ii) a constante aditiva `κ_B` é fabricada
inteiramente na metade `B_n` (mistura Binomial→Poisson), que nunca
referencia (U') nem `a` — logo **κ\* = κ_B, inalterada**, por
independência estrutural, não por coincidência aritmética; (iii) a
estritividade sobrevive inclusive em `c=n`, onde a Binomial degenera na
massa pontual em `K=n` e a (U') nítida é estrita. Novidade adicional: o
primeiro bracket **certificado em aritmética racional pura** para a
constante aditiva, `κ_B\in(0{,}28048,\ 0{,}2805)` (branch-and-bound de
1.525 folhas + cota de cauda gaussiana), elevando o que o referee da
onda 11 (F-9) apontara como avaliação em nível de float; valor de
exibição `0{,}280480169024586` em `c^*=4{,}08675454645254`.

**Nitidez (avaliação honesta, sem teorema de otimalidade).** Ao longo
da linha de contorno `c=n`, `n\,Δ_n(n) = a^*\sqrt n - \tfrac13 + o(1)`
(via as cotas bilaterais de `Q(n)` dos Estágios 13/19 + Corolário 4.2),
logo a razão `LHS/RHS → 1`: `a^*` é a melhor constante multiplicativa
possível para um bound desta forma — o coeficiente de `\sqrt c` melhora
por fator exato `a/a^* = 6{,}1384` sobre o Estágio 12. No interior, o
bound excede o perfil exato `|e(c)|` pelo fator assintótico
`4(\sqrt2-1)=1{,}657` (era ~10,8) — `κ_B` NÃO é alegada ótima.

**Verificação.** Frente: 2.594 células certificadas da desigualdade
final, 0 violações (`n\le1024` interior incluindo `c\in\{n,n-\tfrac14,
n-\tfrac12,n-1\}`; linha `c=n` a `n=30.000`); engine validado contra
enumeração bruta da Definição 4 (19/19) + 18 âncoras; (U') nítida
re-verificada em ~1.490 pontos certificados. Spot-check da sessão antes
do despacho: `κ_B` e argmax reproduzidos em todos os dígitos; 404
células independentes na linha `c=n` via `φ(n,n)=Q(n)/n`, 0 violações;
razões de justeza 0,847/0,949/0,970 reproduzidas; aproximação a
`-1/3` confirmada. Referee hostil dedicado (relatório em
`.../sharp_rate_reassembly_attempt/adversarial/REFEREE_REPORT.md`):
re-derivou o traço da montagem contra a prosa-fonte, re-certificou
`κ_B` com branch-and-bound próprio (mesma contagem de folhas, mesma
folga mínima `1{,}79\cdot10^{-8}`), replicou a desigualdade em 1.060
células certificadas com 0 violações **empurrando a linha de contorno a
`n=50.000`**, e re-derivou do zero a álgebra do caso `K=n` do Estágio
19. **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue**, com
duas questões, nenhuma tocando teorema algum: **R-1** (menor,
obrigatória) — a estatística impressa "pior razão 0,970" não era o
máximo da própria grade da frente; o máximo verdadeiro é ≈0,9904 em
`(30000,30000)` (0,9926 em `(50000,50000)` do referee), erro na direção
segura, corrigido por adendo datado; **O-1** (nit, herdado do Estágio
12) — o domínio impresso do Fact 4.1 diz `n>c` enquanto o uso é em
`0\le c\le n`; a instância `c=n` é verdadeira pela convenção
`q=c/n\wedge1` da Definição 1 e é exatamente o uso já aceito da
Proposição 7.1/Lema 5.1, verificada por força bruta.

### O que isto muda, precisamente

**O item "trivial-mas-não-executado" do Estágio 19 está EXECUTADO e
FECHADO: a taxa explícita incondicional de Teorema A/C vale agora com a
constante nítida.** O Estágio 12 permanece exatamente como provado (o
Teorema R o substitui como melhor taxa disponível, sem invalidá-lo).
Nenhum resultado anterior é enfraquecido.

**O que permanece aberto, sem mudança:** uma constante aditiva de ordem
inferior casada (fechar o gap `κ_B+\tfrac13` no contorno, ou o fator
`4(\sqrt2-1)` no interior — um bound interpolando ao perfil exato
`e(c)`); `n\in\{2,3\}` (herdado, F-13: numérico apenas); monotonicidade
literal termo-a-termo de `M_K/\sqrt K` (herdado do Estágio 19);
Conjecturas 1 (`K\ge5`, sob revisão na onda 17) e 2; a exploração
conjunta (Estágio 18); `p>20`; o piso `H2` em `b=1`; a lei de escala
`\gamma\in(0,1)` (sob revisão na onda 17) [Ver Estágio 23 abaixo —
FECHADA em 2026-08-26]. Nenhuma alegação de
progresso em Millennium Problem; matemática combinatória pura interna
a este arquivo.

---

## [Extensão, Estágio 23 — 2026-08-26]

**Contexto.** Primeiro ataque dedicado ao item aberto desde os
Estágios 10–13: a lei de escala `\gamma\in(0,1)`, para `c=\gamma n`
com `\gamma` fixo, `\varphi(n,\gamma n)/\varphi_\infty(\gamma n) \to
\sqrt{2/(2-\gamma)}` — provada apenas no extremo `\gamma=1`
(`\varphi(n,n)=Q(n)/n` exatamente), caracterizada apenas
numericamente para `\gamma\in(0,1)`, sem frente dedicada até a onda
17 (`GAMMA-SCALING-LAW-ATTEMPT`, DISC-DEC-072).

**Resultado central.**

> **Teorema 2 (PROVADO).** Para todo `\gamma\in(0,1]` fixo,
> `\displaystyle \lim_{n\to\infty}
> \frac{\varphi(n,\gamma n)}{\varphi_\infty(\gamma n)} =
> \sqrt{\frac2{2-\gamma}}`, com taxa explícita `O_\gamma(n^{-1/4})`
> via um sanduíche de dois lados em `n` finito (Teorema 1', abaixo).

**Ambos os alvos-bônus também alcançados**: uniformidade em compactos
`[\gamma_0,1]\subset(0,1]` (Corolário 1); e o limite `\gamma_n\to0`
com `\gamma_n n^{1/3}/\ln n\to\infty` fazendo a razão `\to1` — a lei
degrada continuamente para "sem degradação", exatamente como prediz
`\sqrt{2/(2-\gamma)}\to1` (Corolário 2). O extremo `\gamma=1`
(`\to\sqrt2`) é re-obtido de forma independente (Corolário 3).

O motor da prova **não** é a maquinaria dos Estágios 9/12/22 — a taxa
`|\Delta_n(c)|\le[a\sqrt c+\kappa_B]/n` é, como o próprio despacho
pré-diagnosticou, estruturalmente fraca demais aqui: em `c=\gamma n`
ela dá erro `O(1)` **relativo** contra `\varphi_\infty(\gamma n) =
\Theta(n^{-1/2})`. Em vez disso, o Estágio 23 deriva do zero, direto
da Definição 1, uma **nova fórmula soma-dupla exata em `n` finito**
para `\varphi(n,c)` (Lema 1) — da qual a identidade
`\varphi(n,n)=Q(n)/n` (correção pós-adversarial do Estágio 10) é o
caso particular `q=1` de uma linha — e realiza uma análise de
Laplace/gaussiana dessa fórmula no regime `c=\gamma n`, com todos os
termos de erro explícitos (Lema 2: sanduíche de produto; Lema 3:
decaimento a priori via Chernoff; Lema 4: substituição gaussiana via
o lema de Hoeffding, clássico, citado; Lema 5: comparação
soma-integral). Todos os ingredientes são elementares; as únicas
citações são clássicas (Hoeffding) ou resultados já provados do
próprio arquivo (Teorema 1/Corolário 4.2 para `\varphi_\infty`).

**Bônus além do mandato**: um termo de segunda ordem em forma
fechada, `\sqrt n(\text{razão}-\sqrt{2/(2-\gamma)}) \to C(\gamma) =
-\frac2{3\sqrt\pi}\sqrt\gamma\,\frac{6-8\gamma+3\gamma^2}{(2-\gamma)^2}`,
**PROVADO em `\gamma=1`** (reduz a `-2/(3\sqrt\pi)`, via Robbins 1955
+ FGKP95, já verificados na linhagem do Estágio 19) e
**CONJECTURADO para `\gamma\in(0,1)`** (extrapolação de Richardson
casa com a forma fechada a 7 dígitos significativos em 11 valores de
`\gamma`; a troca de ordem expansão↔soma não foi feita rigorosamente
— rotulado honestamente como não provado, nunca promovido ao
scorecard principal).

**Verificação.** Frente: fórmula do Lema 1 validada 4 formas
independentes (força bruta de `n=3,4,5`; endpoint `q=1` contra `Q(n)/n`
até `n=400`; inversão da identidade de mistura recuperando
`\varphi_n^{(K)}` já provados; roundoff float64 vs. exato); sanduíche
do Teorema 1' certificado em 30/30 pontos de grade; auditorias de
desigualdade com zero violações; grade `\gamma\times n` até `n=2^{18}`
reproduzindo o alvo com precisão crescente. Referee hostil dedicado
(relatório em `.../gamma_scaling_attempt/adversarial/REFEREE_REPORT.md`):
re-derivou o Lema 1 à mão a partir da Definição 1 antes de escrever
qualquer código — confirmação independente, não apenas leitura;
confirmou a identidade algébrica central `(G_n/n)/L_n =
\sqrt{2/(2-\gamma)}` exatamente à mão; reconstruiu todo o motor
numérico do zero (nunca abriu os scripts da frente nem de uma
instância anterior travada do próprio referee) — força bruta exata
em `n=3,4,5` contra o Lema 1 (0 divergências); reproduziu a tabela
`\gamma\times n` impressa dígito a dígito; auditou ~154.000
desigualdades pontuais dos Lemas 2–4 (encontrou e corrigiu um bug de
underflow no próprio script de diagnóstico, disclosurado, 0
violações após a correção); replicou a extrapolação de Richardson do
termo de segunda ordem. Veredito: **SOUND — ACCEPT for catalogue**,
no nível exatamente reivindicado (prova completa do mandato, não
parcial); nenhum erro matemático, uso indevido de citação ou
superalegação encontrado. **Spot-check da sessão** antes de
catalogar: fórmula do Lema 1 confirmada por força bruta própria
(`n=3,4`); identidade algébrica central confirmada simbolicamente;
`\varphi(n,n)=Q(n)/n` confirmada exata `n=1..7`; `C(1)=-2/(3\sqrt\pi)`
exato; a tabela `\gamma\times n=2^{18}` reproduzida a `\sim10^{-11}`
em todos os 6 valores de `\gamma` — após a sessão encontrar e
corrigir um bug de underflow catastrófico no seu **próprio** script
de verificação (`(1-q)^k` subestourando para `0.0` em float64 antes
da recursão binomial alcançar a moda), da mesma classe do bug que o
próprio referee já havia documentado e corrigido em seu `av04`.

### O que isto muda, precisamente

**O item aberto desde os Estágios 10–13 está FECHADO para todo
`\gamma\in(0,1]`, incluindo ambos os alvos-bônus de uniformidade e do
limite `\gamma_n\to0`.** Nenhum resultado anterior é enfraquecido —
os Estágios 9/12/22 permanecem exatamente como provados, apenas não
usados aqui (diagnosticados como estruturalmente insuficientes para
esta pergunta específica, um fato verificado, não presumido).

**O que permanece aberto, com precisão:** uma taxa `n^{-1/2}` e um
termo de segunda ordem **provados** (não apenas conjecturados) para
`\gamma\in(0,1)` — precisaria de uma versão rigorosa em nível de
Edgeworth da expansão do §7.3 [Ver Estágio 26 abaixo — 2026-08-26:
progresso parcial genuíno (Lema E e a metade determinística `D_0(γ)`
agora PROVADOS incondicionalmente para todo `γ`), mas `C(γ)` em si
para `γ\in(0,1)` continua ABERTO — apenas a metade "difícil" resta,
agora precisamente isolada]; a janela intermediária `n^\epsilon \le
c_n \le n^{2/3}/\log` entre o regime `c` fixo do Estágio 10 e o
regime `\gamma_n\ge n^{-1/3}\ln n` do Corolário 2 — nomeada aqui como
o resíduo natural, explicitamente não fechada. Conjectura 1 (`K\ge5`)
e 2 [Ver Estágio 24 abaixo — ambas fechadas em 2026-08-26]; a
exploração conjunta (Estágio 18, permanece aberta em si mesma mesmo
após o fechamento indireto da Conjectura 2); `p>20`; o piso `H2` em
`b=1`; a constante do platô de DISC-DEC-071 (sob revisão na onda 17).
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 24 — 2026-08-26]

**Onda 17, frente (a), `DISC-DEC-072`/`DISC-DEC-075`
(`CONJECTURE-1-K5-GENERAL-ATTEMPT`).** Alvo: §8 Conjectura 1 em
`K=5` (o mandato explícito da frente), mais um objetivo de estica
("stretch goal") declarado no despacho: se possível, um argumento
`K`-uniforme fechando a Conjectura 1 para **todo** `K\ge1` de uma vez,
em vez de mais uma instância pontual.

### O que aconteceu

> **O objetivo de estica foi alcançado.** Todo ingrediente da linha
> `K=1,2,3,4` que antes era provado caso a caso foi generalizado para
> `K` simbólico, e a Conjectura 1 está agora **PROVADA para todo
> `K\ge1`**, condicional à mesma citação clássica única de toda a
> linha. Como corolário imediato (não parte do mandato original, mas
> observado e sinalizado pela própria frente para decisão desta
> sessão), a **Conjectura 2 também está agora PROVADA**, no mesmo
> patamar.

**Teorema (geral-`K`).** Para todo inteiro `K\ge1`,
`f_{M_K}(x)=2Kx(1-x^2)^{K-1}` em `(0,1)` — PROVADO, condicional à
propriedade `PD(1)` de residual/size-biasing (McCloskey 1965;
Patil–Taillie 1977; Pitman 2002 Cap. 3), aplicada recursivamente até
`K-1` vezes para cada `K` fixo — a mesma citação única já usada em
`K=1,2,3,4`, aplicada o número de vezes que a construção exige, nunca
de forma não-limitada ou "no infinito" para um único `K`. Em
particular `f_{M_5}(x)=10x(1-x^2)^4`, a instância explicitamente
mandatada pela onda.

Cada ingrediente per-`K` da linha anterior foi generalizado para `K`
simbólico: o Lema 1a (espaçamentos circulares rotulados) para todo
tamanho de bloco `b`; a "cascata telescópica" (§2.2) para todo padrão
de partição, com um único passo indutivo sobre peels em vez de um
argumento por `K`; a fórmula do mecanismo de destino (§3.1) sem
divisão por casos; e — a peça nomeada como pista pelo próprio
Estágio 20 — a identidade geral de florestas ponderadas
`W(n)=e(e+Q)^{n-1}` provada para **todo** `n` via a bijeção de Prüfer,
fechando de uma vez o único ingrediente que antes exigia um `n` por
`K`. A soma sobre `r` fecha pelo teorema binomial, com `K` simbólico,
reproduzindo exatamente `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`.

**Corolário: Conjectura 2.** `THEOREM.md` §8 Conjectura 2 é, por sua
própria definição, a mistura de Poisson(`c`) da Conjectura 1 sobre
`K`. Combinando o Teorema geral-`K` acima com a citação de Kingman já
usada em §5.1 (condicionar o modelo incondicional em `\mathcal N=K`
reproduz exatamente o modelo `K`-condicional) e aditividade contável:

`P(M(c)\le x) = \sum_{K\ge0} e^{-c}\frac{c^K}{K!}[1-(1-x^2)^K]
 = 1-e^{-c}e^{c(1-x^2)} = 1-e^{-cx^2}`,

com átomo `P(M(c)=1)=e^{-c}` — exatamente
`M(c)\overset{d}{=}\min(1,\sqrt{E/c})`, `E\sim\mathrm{Exp}(1)`, no
mesmo patamar PROVADO-condicional-à-citação do Teorema. Consistência:
`E[M(c)]=\varphi_\infty(c)` reproduz o Teorema 1; e
`E[M(c)^2]=(1-e^{-c})/c`, com `E[M_K^2]=1/(K+1)` para **todo** `K` —
os dois alvos que o Estágio 18 havia registrado e deixado
condicionais/incondicionais apenas em `K\le3` estão agora exatos e
incondicionais para todo `K`. Esta é uma rota **indireta** — através
da Conjectura 1 geral-`K`, não da arquitetura de momentos direta do
Estágio 18, que permanece exatamente como estava (obstrução
localizada, não removida).

Também provados como subprodutos, novos além de `K\le4`:
`E[M_K]=\varphi_K`, `E[M_K^2]=1/(K+1)` para todo `K`; a instância
`E[M_5^3]=256/3003`.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee reforçado
(feito em turno anterior a este, já registrado nas notas internas):
verificação independente das 7 seções de prova do documento,
incluindo reconstrução própria da cascata telescópica para `K=2,3` e
da identidade de florestas para `n=1,\ldots,5` — nenhuma discrepância
encontrada.

Dado o peso do resultado — o maior alegado nesta linha `U_{1/2}` até
agora — a sessão despachou um **referee reforçado**, com briefing
explícito para atacar a passagem do per-`K` para o geral-`K`
(especificamente: a independência do resíduo na cascata telescópica,
citada como o ponto de maior risco de um salto ilegítimo). O referee
reconstruiu do zero, sem abrir nenhum script da frente:

- O Lema 1 geral (a densidade `K!` no simplex `\Delta_K`) foi
  re-derivado à mão, e a "cascata telescópica" foi provada
  **simbolicamente para qualquer sequência de tamanhos de bloco**,
  cobrindo de uma vez todo padrão de todo `K`, não apenas os padrões
  de `K=5`.
- A independência conjunta (não apenas marginal) do resíduo em
  relação a `\ell_1,\ldots,\ell_{j-1}` foi confirmada como definicional
  à representação stick-breaking `GEM(1)`, o mesmo dispositivo já
  aceito em `K=1,2,3,4` — nenhuma falha encontrada no salto per-`K`
  para geral-`K`.
- A identidade `\sum\prod(b_j-1)!=K!` foi re-verificada por enumeração
  direta `K=1,\ldots,9`.
- A fórmula fechada por `r`, re-derivada à mão (deliberadamente
  evitando o padrão `sympy.Sum(...).doit()` em `K` simbólico que havia
  travado uma tentativa anterior de referee); fechamento da soma
  binomial verificado `K=1,\ldots,15`.
- O Lema 3 (identidade de florestas ponderadas, Prüfer) verificado
  como identidade polinomial exata por força bruta `n=1,\ldots,7` — um
  passo além tanto da própria frente (`n=1,\ldots,6`) quanto de uma
  tentativa anterior travada (`n=1,\ldots,7`, confirmando).
- O mecanismo discreto verificado em `K=5` com 300.000 trials, 0
  discrepâncias, cobertura completa das 7.776 células em 3 escalas.
- **Além do escopo da própria frente:** classificação exaustiva fresca
  e MC de receita contínua em `K=6` (117.649 mapas brutos, 30 tipos de
  forma; MC de receita `N=800\text{k}`, KS `p=0{,}55`, casando
  `E[M_6^2]=1/7`).
- Quatro bugs encontrados e corrigidos — todos no **próprio** código
  de verificação do referee (ordem de integração errada; fórmula de
  Dirichlet de referência errada; soma sobre ciclo mal-indexada; erro
  de sinal descartando o termo de massa OUT), todos disclosurados; após
  as correções, as quatro rotas reproduzem exatamente as alegações do
  documento-alvo. Nenhum erro no documento-alvo em si.

> **Veredito: SOUND — ACCEPT for catalogue.** "The general-`K` claim
> survives at its claimed tier: PROVED for every `K\ge1`, modulo the
> single classical PD(1) size-biased/residual citation... Conjecture 2
> (§4.6) also survives at the same tier: it follows as an exact
> corollary of the general-K theorem via the Poisson mixture algebra,
> which I re-derived by hand and confirms exactly." Nenhum novo achado
> além dos três itens já auto-disclosurados pela própria frente em seu
> §6 (artefato `Piecewise` do sympy em um harness de checagem, não em
> nenhuma derivação; dois p-valores isolados abaixo de `0{,}01`
> resolvidos por um follow-up pré-declarado com poder maior; uma frase
> de pré-registro otimista demais sobre cobertura em `n=12`).

Ver `theorem/conjecture1_k2_attempt/conjecture1_k3_attempt/`
`conjecture1_k4_attempt/conjecture1_k5_attempt/ATTEMPT.md` e
`.../conjecture1_k5_attempt/adversarial/REFEREE_REPORT.md`.

### Reconciliação com a frente (c) da mesma onda

A frente (c) (`JOINT-TWO-POINT-EXPLORATION-ATTEMPT`, integrada
separadamente) registrou seus alvos `E[M(c)^2]=(1-e^{-c})/c` e
`E[M_K^2]=1/(K+1)` como **ABERTOS**, com base no estado de
`THEOREM.md` no momento em que essa frente rodou — momento anterior ao
retorno do referee reforçado desta frente. Essa caracterização estava
correta **no momento em que foi escrita**; está agora superada por
este Estágio, que fecha ambos os alvos incondicionalmente para todo
`K`. Isto não invalida o resultado genuíno da frente (c) (o Teorema J
de restrição cíclica uniforme e seu corolário `P(\text{mesmo
ciclo})=P(\text{ciclo diferente})=\frac12 P(\text{ambos cíclicos})`
exatos, em `n,K` finitos) — apenas sua nota de contexto sobre o que
permanecia aberto no momento do despacho, e a própria frente (c) já
havia notado explicitamente (§6.2) que não existe atalho de "split é
50/50" para fechar `E[M_K^2]` sem resolver a Conjectura 1 geral-`K`
em si — exatamente o que esta frente independentemente fechou por
outra rota. Nenhuma tensão real entre os dois resultados; a
sobreposição é apenas cronológica.

### O que isto muda, precisamente

**Conjectura 1 (§8) está agora PROVADA para TODO `K\ge1`.** Nenhum `K`
permanece aberto. **Conjectura 2 (§8) está agora PROVADA**, como
corolário indireto, no mesmo patamar. Ambas condicionais à mesma
citação `PD(1)` única já aceita em toda a linha `K=1,\ldots,4` — nenhum
novo ingrediente de confiança é pedido além do que este arquivo já
aceita desde o Estágio 3. Nenhum resultado anterior é enfraquecido;
os Estágios 3–20 permanecem exatamente como provados, agora como
instâncias `K=1,\ldots,4` de um teorema estritamente mais geral.

**O que permanece aberto, com precisão:** a ponte `n\to\infty` para a
*distribuição* de `M(c)` (distinta da média, já fechada pelo Teorema
1/Estágio 22) — não endereçada aqui, por ser um tipo de alegação
diferente, exatamente como `THEOREM.md` §8 já separa [Ver Estágio 27
abaixo — 2026-08-26: progresso parcial genuíno (a redução a
convergência de CDF ponto-a-ponto em `K` fixo é agora PROVADA
incondicionalmente, junto com o fechamento completo em `K=0,1`), mas a
ponte completa para `K\ge2` continua ABERTA]; a exploração
conjunta de `p\ge2` pontos como maquinário independente (Estágio 18 —
permanece seu próprio problema aberto, mesmo com seus dois alvos de
momento agora fechados por outra rota); `p>20` de `D^{*(p)}_r(b)`
(Estágio 21); o piso `H2` em `b=1` (sob revisão na onda 17); a
constante do platô de DISC-DEC-071 (sob revisão na onda 17). Nenhuma
alegação de progresso em Millennium Problem; matemática combinatória
pura interna a este arquivo.

---

## [Extensão, Estágio 25 — 2026-08-26]

**Onda 17, frente (c), `DISC-DEC-072`/`DISC-DEC-076`
(`JOINT-TWO-POINT-EXPLORATION-ATTEMPT`).** Alvo: a obstrução localizada
pelo Estágio 18 — a lei conjunta da exploração em dois pontos. Alvos
numerados no despacho, em ordem de valor: (1) `E[M(c)^2]=(1-e^{-c})/c`
incondicional; (2) `E[M_K^2]=1/(K+1)` incondicional para todo `K`; (3)
qualquer estrutura rigorosa parcial da lei conjunta de dois pontos.

### O que aconteceu

> **Não-fechamento honesto dos alvos (1) e (2) — que, no momento em que
> esta frente rodou, ainda estavam abertos em `THEOREM.md` — combinado
> com um novo teorema genuíno e completo sobre a estrutura em si (alvo
> 3).** Nenhum atalho de "split é 50/50" para os alvos de momento é
> alegado; a própria frente já havia diagnosticado (§6.2) que fechar
> `E[M_K^2]` exige resolver a Conjectura 1 geral-`K` em si — exatamente
> o que o Estágio 24 fechou, por outra rota, no mesmo dia.

**Teorema J (Teorema da Restrição Cíclica Uniforme, PROVADO).** No
modelo condicional-`K` finito da Definição 4 (`THEOREM.md` §7.2),
condicional ao conjunto cíclico final realizado `C(f)=c` (qualquer
subconjunto com `|c|=m\ge2`), a restrição `f|_c` é **exatamente
uniformemente distribuída** sobre todas as `m!` bijeções de `c` — para
todo `n,K`, não apenas assintoticamente. Prova elementar, bijetiva:
**Lema J1** (invariância por pós-composição — `\kappa\circ f
\overset{d}{=} f` para qualquer bijeção fixa `\kappa`, uma identidade
algébrica pontual mais um argumento de invariância de lei, sem nenhuma
probabilidade condicional envolvida na primeira parte); **Lema J2**
(uma bijeção de troca explícita, para `\rho'=\rho\circ(x\,y)` com
`\kappa:=(\rho(x)\,\rho(y))`, entre `\{C(h)=c,h|_c=\rho\}` e
`\{C(h)=c,h|_c=\rho'\}` — a parte de maior risco: `\kappa` tem suporte
inteiramente contido em `c` por construção, logo nunca alcança nem é
alcançada por estrutura fora de `c`, o que preserva `C(g)=c`
exatamente, verificado por indução completa sobre a cauda da órbita
pré-`c`).

**Corolário (PROVADO).** `P(\text{dois pontos fixos no mesmo ciclo
final}\mid\text{ambos cíclicos}) = 1/2` **exatamente**, para todo
`n\ge2` finito e todo `0\le K\le n` — um fortalecimento estrito do
Lema B1 do Estágio 18 (que só concernia a permutação `\pi` de fundo
incondicional, não o grafo funcional rerouted de fato, condicional a
ambos os pontos sobreviverem).

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: enumeração
exaustiva independente e fresca em `(n,K)\in\{(3,1),(4,1),(4,2),(5,2),
(3,3),(4,4)\}` — confirmando tanto a uniformidade de restrição quanto
o split 50/50 exatos, mais uma re-verificação separada do fato
clássico `P(\text{mesmo ciclo})=1/2`. Zero discrepâncias.

Referee hostil dedicado, sem ler nenhum script da frente: re-derivou
os Lemas J1 e J2 à mão, atacando com peso máximo o passo de maior
risco nomeado no despacho (`|c|=2`; se `\kappa` pode alcançar estrutura
fora de `c`; se a troca pode silenciosamente mudar quais pontos
terminam cíclicos) — nenhuma falha encontrada em nenhum dos três.
Reconstruiu o motor computacional do zero: o fato clássico
`P(\text{mesmo ciclo})=1/2` re-verificado `m=2,\ldots,9` (frente:
até `7`) mais checagem todos-os-pares em `m=4,5,6`; enumeração
exaustiva da Definição 4 em **33 células `(n,K)`** (frente: 21),
incluindo quatro tipos de célula nunca testados pela frente
(`K=0` inteiro; `K=6,7`, incluindo o contorno `K=n=7`) — **33/33
verificações de sanidade de peso, 33/33 do corolário, 33/33 da
uniformidade de restrição do Teorema J, zero violações**; mais uma
re-implementação "ingênua" totalmente independente (sem nenhum atalho
de reponderação) em 12 células, batendo exatamente com o método
otimizado — incluindo confirmar que a coincidência `n=4,K=3` e
`n=4,K=4` ambos `P_{\text{both}}=19/64` é genuína, não um bug.

> **Veredito: SOUND — ACCEPT for catalogue**, no tier reivindicado
> (PROVADO, elementar, autocontido). Nenhum erro matemático encontrado
> no Teorema J, no Corolário, ou nos dois lemas subjacentes. Um achado
> cosmético (framing de um conjunto gerador desnecessário no §2.2, não
> afeta a prova). Disclosure do referee: um quase-incidente de processo
> (execução concorrente duplicada no run exaustivo principal, detectada
> via `ps aux` antes de confiar no log, ambos processos mortos, re-run
> limpo único — nenhum dado corrompido chegou ao relatório final);
> nenhum bug matemático/lógico encontrado no código do próprio referee.

Ver `theorem/conjecture2_direct_attempt/joint_two_point_attempt/ATTEMPT.md`
e `.../joint_two_point_attempt/adversarial/REFEREE_REPORT.md`.

### Reconciliação com a frente (a) da mesma onda

Esta frente registrou os alvos (1)/(2) como abertos com base no estado
de `THEOREM.md` no momento em que rodou — anterior ao retorno do
referee reforçado da frente (a) (Estágio 24, integrado no mesmo dia).
Essa caracterização era precisa **no momento em que foi escrita**; está
agora superada pelo Estágio 24, que fecha ambos os alvos
incondicionalmente para todo `K`, por uma rota inteiramente diferente
(a Conjectura 1 geral-`K`, não a exploração conjunta). Isto não
invalida o resultado desta frente — o Teorema J é uma peça estrutural
genuína e nova, e a própria frente já havia notado (§6.2) que não
existe atalho do split para o alvo de momento, exatamente o que se
confirmou: os dois fechamentos são de fato independentes, não
concorrentes.

### O que isto muda, precisamente

**Um novo teorema exato — Teorema J e seu Corolário — está catalogado,
fortalecendo estritamente o Lema B1 do Estágio 18 para o regime
condicional de fato (não apenas o pano de fundo `\pi`).** Os alvos de
momento (1)/(2) que esta frente mirava permanecem, quanto a esta
frente, não fechados por sua própria rota — mas já fechados pelo
Estágio 24, por outra rota, no mesmo dia. Nenhum resultado anterior é
enfraquecido.

**O que permanece aberto, sem mudança:** a maquinaria de exploração
conjunta de `p\ge2` pontos como ferramenta geral (o Teorema J resolve
apenas a peça condicional "split dado ambos cíclicos", não a lei
conjunta completa); a versão contínua-nativa do Teorema J a partir da
Definição 3 (tentada em §6.3, não completada — mesma obstrução do
Estágio 18 §3.3) [Ver Estágio 28 abaixo — 2026-08-26: progresso parcial
genuíno via transferência (não construção contínua direta), fechando
`K=0,1` incondicionalmente; `K\ge2` continua ABERTO]; `p>20` de
`D^{*(p)}_r(b)`; o piso `H2` em `b=1`
(sob revisão na onda 17); a constante do platô de DISC-DEC-071 (sob
revisão na onda 17). Nenhuma alegação de progresso em Millennium
Problem; matemática combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 26 — 2026-08-26]

**Onda 18, frente (b), `DISC-DEC-078`/`DISC-DEC-079`
(`GAMMA-SECOND-ORDER-ATTEMPT`).** Alvo: o item deixado explicitamente
aberto pelo Estágio 23 — uma prova rigorosa (não apenas uma
extrapolação de Richardson que casa numericamente) do termo de segunda
ordem `C(\gamma)` para `\gamma\in(0,1)`, com `C(1)=-2/(3\sqrt\pi)` já
provado servindo de âncora de contorno.

### O que aconteceu

> **Não-fechamento honesto do mandato central**, combinado com
> progresso parcial genuíno e novo: a decomposição do problema em duas
> metades, uma das quais é agora provada incondicionalmente para todo
> `\gamma`, isolando com precisão onde a dificuldade remanescente vive.

**Lema E (PROVADO).** Equivalência elementar entre a conjectura
`C(\gamma)` e uma afirmação sobre a soma exata
`S_n:=n\varphi(n,\gamma n)=\sum_kA_k` (com `A_k` os termos de
Definição 1/§2 já provados na linhagem): `C(\gamma)` vale se e somente
se `S_n=G_n+D(\gamma)+o(1)` para a constante `D(\gamma)` associada.
Prova por álgebra direta a partir de resultados já citados no arquivo,
sem nenhum ingrediente novo além do que já está aceito.

**Lema D0 (PROVADO, novo, generaliza além de `\gamma=1`).** Separando
`A_k = e^{-s(k)} + [A_k-e^{-s(k)}]` (a "metade determinística" contra
o resíduo), a primeira metade tem forma fechada exata para **todo**
`\gamma\in(0,1]`: `S_n^{(0)}:=\sum_{k=1}^ne^{-s(k)} = G_n + D_0(\gamma)
+ \Theta(n^{-1/2})`, `D_0(\gamma)=(\gamma-1)/(2(2-\gamma))`, via soma
de Poisson / transformação theta de Jacobi — uma ferramenta elementar
nunca antes usada nesta linhagem. **Correção pós-adversarial
(2026-08-26):** o termo de erro originalmente enunciado pela frente,
`O(\sqrt n\,e^{-cn})` (exponencialmente pequeno), estava **errado**; o
referee hostil derivou de forma independente e confirmou
numericamente (mpmath, `n` até 32000) que o erro correto é
`\Theta(n^{-1/2})` — polinomialmente pequeno, com coeficiente líder
explícito `(\gamma^2\sqrt\pi)/(32\beta^{3/2})` — já visível nos
próprios dados numéricos da frente (razão de erros sucessivos
`\to\sqrt{10}` sob `n\mapsto10n`), mas nunca reconciliado com o
enunciado formal do lema. O **valor** de `D_0(\gamma)` não muda; ver
adendo datado em
`.../gamma_second_order_attempt/ATTEMPT.md` §3.

**§4 (heurística, NÃO provada, evidência forte).** Uma segunda derivação
independente, estruturalmente diferente (expansão termo-a-termo de
cumulantes, não "Taylor da razão inteira"), reproduz
`E(\gamma):=D(\gamma)-D_0(\gamma)` **exatamente, simbolicamente** (zero
discrepância, checado por sympy) — a mesma função racional que a onda
17 já havia conjecturado via extrapolação de Richardson. Duas rotas
independentes convergindo para a mesma forma fechada exata é evidência
forte de que a conjectura é verdadeira, mas não constitui prova: a
troca de ordem limite/soma na derivação heurística não foi
justificada rigorosamente.

**§5 (diagnóstico honesto do que falta).** Três lacunas técnicas
nomeadas com precisão para fechar `E(\gamma)` rigorosamente — nenhuma
delas exige uma nova citação externa além do que este arquivo já
aceita — avaliadas pelo referee como precisas, com uma adição
sugerida (não crítica).

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee
(`spotcheck_gamma_second_order.py`): confirmação numérica direta de
`D_0(\gamma)` via soma `mpmath` em vários `\gamma,n`, com a taxa de
convergência correta `O(n^{-1/2})` já visível antes mesmo do referee
apontar o erro no enunciado formal; confirmação simbólica via sympy de
que `D(\gamma)-D_0(\gamma)` (derivado do Lema E) coincide exatamente
com `E_{\text{heurística}}(\gamma)` do §4 (diferença simplifica a
zero); `D(1)=E(1)=-1/3` batendo com a âncora clássica em `\gamma=1`.

Referee hostil dedicado (`.../gamma_second_order_attempt/adversarial/`
`REFEREE_REPORT.md`, 372 linhas): confirmou o Lema E são por duas
rotas algébricas independentes (nenhum erro); re-derivou o valor
fechado de `D_0(\gamma)` por um método distinto do da frente
("completar o quadrado antes da soma de Poisson") — valor confirmado,
mas **encontrou que o termo de erro enunciado no Lema D0 estava
errado** (ver acima); re-confirmou o casamento simbólico do §4 por três
rotas, incluindo pontos `\gamma` irracionais; avaliou o diagnóstico de
lacunas do §5 como preciso, com uma adição sugerida; reproduziu a
numérica do §6 a `\le4{,}2\times10^{-7}`/`\le5\times10^{-11}`.

> **Veredito: SOUND WITH ONE NAMED ISSUE — ACCEPT for catalogue**, no
> tier efetivamente reivindicado (não-fechamento honesto do mandato,
> mais duas peças genuinamente provadas), condicional à correção do
> termo de erro do Lema D0 — aplicada nesta integração (ver adendo
> datado no `ATTEMPT.md` da frente). Nenhum outro erro encontrado;
> Lema E, o casamento simbólico do §4 e a numérica do §6 confirmados
> sem ressalvas.

Ver
`.../gamma_scaling_attempt/gamma_second_order_attempt/ATTEMPT.md` e
`.../gamma_second_order_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**Duas peças novas e genuínas estão catalogadas: o Lema E (equivalência)
e o Lema D0 (metade determinística de `S_n`, forma fechada para todo
`\gamma`, com taxa de erro `\Theta(n^{-1/2})` corrigida).** O mandato
central — `C(\gamma)` provado para `\gamma\in(0,1)` — permanece
**NÃO FECHADO**, mas a dificuldade remanescente está agora precisamente
isolada na "metade difícil" `E(\gamma)`, com duas derivações
independentes (Estágio 19/Robbins-FGKP95 em `\gamma=1`, mais a
heurística de cumulantes do §4 aqui) apontando para a mesma forma
fechada. Nenhum resultado anterior é enfraquecido; a caracterização
"CONJECTURADO para `\gamma\in(0,1)`" do Estágio 23 permanece
tecnicamente correta — apenas mais precisamente diagnosticada agora.

**O que permanece aberto, com precisão:** `C(\gamma)` para
`\gamma\in(0,1)` em si — precisaria de uma das três lacunas técnicas
do §5 (nomeadas com precisão, mesma classe de citação já aceita no
arquivo) [Ver Estágio 30 abaixo — 2026-08-26: a Lacuna 2 está agora
FECHADA rigorosamente (e em forma mais forte que a pedida); restam
as Lacunas 1 e 3, com a Lacuna 1 identificada como a mais dura das
duas]; a janela intermediária do Estágio 23; `p>20` de
`D^{*(p)}_r(b)` (sob revisão na onda 18); a versão contínua-nativa do
Teorema J (sob revisão na onda 18); a ponte distribucional `M_n(c)\to_d
M(c)` (sob revisão na onda 18); o piso `H2` em `b=1`; a constante do
platô de DISC-DEC-071. Nenhuma alegação de progresso em Millennium
Problem; matemática combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 27 — 2026-08-26]

**Onda 18, frente (d), `DISC-DEC-078`/`DISC-DEC-080`
(`DISTRIBUTIONAL-BRIDGE-ATTEMPT`).** Alvo: a ponte `n\to\infty` para a
**distribuição** completa de `M(c)` (`M_n(c)\to_d M(c)`), distinta da
média já fechada pelo Teorema 1/Estágio 22 — questão nomeada como
aberta e de tipo distinto desde o Estágio 6 (§8), nunca atacada
diretamente por nenhuma frente anterior.

### O que aconteceu

> **Não-fechamento honesto do mandato completo** (a ponte de
> distribuição para todo `K`), combinado com o fechamento incondicional
> do caso `K=0,1` e de toda a maquinaria de redução que o generaliza,
> mais um resultado de segundo momento inteiramente novo nesta
> linhagem.

**Proposição D0 (PROVADA).** Identidade exata de mistura de CDFs em
`n` finito: `F_n(x) = \sum_{K=0}^nP(\mathrm{Bin}(n,c/n)=K)\,F_n^{(K)}(x)`
— um upgrade genuíno do Fato 4.1 (que só rastreava médias) para leis
condicionais completas.

**Lema R (PROVADO).** Re-derivação completa, em nível de CDF, do
argumento de mistura de Poisson da Proposição 3 (Scheffé + Chernoff),
reduzindo o alvo `M_n(c)\to_dM(c)` a convergência de CDF em `K` fixo,
para todo `K`.

**`K=0` trivial; `K=1` (Proposição D1, PROVADA, o centro do
resultado).** Forma fechada exata em `n` finito,
`P(M_n^{(1)}\le k/n) = k(k+1)/n^2`, obtida estendendo a divisão de
casos da Proposição 4 (`THEOREM.md`) da média para a lei completa —
com corolários dando taxa uniforme de convergência de CDF `O(1/n)`
(Corolário D1.1) e um segundo momento exato,
`E[(M_n^{(1)})^2]=\tfrac12+\tfrac1{2n^2}`, à taxa `O(n^{-2})` (Corolário
D1.2 — "o primeiro resultado de segundo momento/flutuação nesta
linhagem"), mais convergência de variância (D1.3).

**Lema P2 (PROVADO).** Redução geral-`K` da convergência do segundo
momento a um único escalar `P_{nn}(n,K)`, via identidade exata de
exchangeability — o análogo em dois pontos do Lema de Redução A
geral-`K` de `THEOREM.md`.

`K\ge2` honestamente aberto (tanto a ponte completa de CDF quanto
mesmo apenas `P_{nn}(n,K)\to1/(K+1)`), com diagnóstico preciso: a
maquinaria marginal existente é estruturalmente incapaz de uma
resposta conjunta em dois pontos — a mesma obstrução que os Estágios
18/25 já diagnosticaram para uma quantidade contínua relacionada, mas
distinta (`E[M_K^2]`, fechada por outra rota no Estágio 24).

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee
(`spotcheck_distributional_k1.py`): enumeração exaustiva independente
por força bruta confirmando `P(M_n^{(1)}\le k/n)=k(k+1)/n^2` exatamente
para `n=2,\ldots,6`.

Referee hostil dedicado (`.../distributional_bridge_attempt/adversarial/`
`REFEREE_REPORT.md`, 362 linhas), sem ler nenhum script da frente:
re-derivou a Proposição D0 e, além disso, fechou de forma independente
o único gap implícito do documento — que a lei *completa* de
`M_n^{(K)}` (não apenas a média) independe de qual `K`-subconjunto é
fixado — via um argumento de conjugação explícito (`σ∘f∘σ⁻¹=f'`
identicamente, logo contagem de pontos cíclicos é invariante por
conjugação, não apenas em distribuição); verificou o Lema R
checando explicitamente se alguma propriedade específica de CDF
(monotonicidade etc.) era contrabandeada onde o argumento original de
médias não licenciaria — não encontrou nenhuma; re-derivou a
Proposição D1 do zero, antes de ler a versão do documento, e
confirmou por enumeração exaustiva independente (`n=2,\ldots,9`,
aritmética `Fraction` exata, `0/63` discrepâncias); refez toda a
álgebra dos Corolários D1.1–D1.3 e do Lema P2 à mão, confirmando por
força bruta em 11 células (`K=1,2,3`); avaliou o diagnóstico de
não-fechamento de `K\ge2` como preciso, nem superestimado nem
subestimado; reproduziu as tabelas numéricas da §7 exatamente.

> **Veredito: SOUND — ACCEPT for catalogue**, exatamente no tier
> reivindicado. Nenhum bug encontrado em lugar nenhum da matemática do
> documento; nenhuma superalegação e nenhuma subalegação desnecessária.

Ver `theorem/distributional_bridge_attempt/ATTEMPT.md` e
`.../distributional_bridge_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**Duas peças novas e genuínas estão catalogadas: a Proposição D0
(mistura de CDFs exata) e o fechamento completo `K=0,1` da ponte
distribucional (Proposição D1 e seus três corolários), mais o Lema P2
(redução geral-`K` do segundo momento).** O mandato completo — a ponte
`M_n(c)\to_dM(c)` para todo `K`, e mesmo `P_{nn}(n,K)\to1/(K+1)` para
`K\ge2` — permanece **NÃO FECHADO**, mas agora com a maquinaria de
redução (Lema R, Lema P2) provada incondicionalmente, isolando com
precisão o que falta: apenas o caso `K\ge2` da própria Proposição
D1/análoga. Nenhum resultado anterior é enfraquecido.

**O que permanece aberto, com precisão:** a ponte distribucional
completa e `P_{nn}(n,K)\to1/(K+1)` para `K\ge2` [Ver Estágio 31 abaixo
— 2026-08-26: `K=2` FECHADO (`P_{nn}(n,2)\to1/3`, PROVADO); `K\ge3`
continua ABERTO, agora com obstrução estruturalmente diagnosticada] —
precisaria de uma
generalização da Proposição D1 análoga à obstrução já diagnosticada
para a exploração conjunta (Estágios 18/25); `C(\gamma)` para
`\gamma\in(0,1)` (Estágio 26); `p>20` de `D^{*(p)}_r(b)` (sob revisão
na onda 18); a versão contínua-nativa do Teorema J (sob revisão na
onda 18); o piso `H2` em `b=1`; a constante do platô de DISC-DEC-071.
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 28 — 2026-08-26]

**Onda 18, frente (c), `DISC-DEC-078`/`DISC-DEC-081`
(`JOINT-EXPLORATION-CONTINUUM-ATTEMPT`).** Alvo: completar a versão
contínua-nativa (Definição 3) do Teorema J — tentada em §6.3 do
Estágio 25 e explicitamente não completada ali, mesma obstrução
diagnosticada no Estágio 18 §3.3 (o dispositivo de exploração de um
ponto abstrai exatamente a informação de destino físico que uma
versão contínua do Teorema J precisaria).

### O que aconteceu

> **Não-fechamento honesto do mandato completo** (uma construção
> contínua-nativa direta a partir da Definição 3, para todo `K`),
> combinado com um **bypass genuíno via transferência**: em vez de
> resolver a obstrução de construção contínua, a frente mostrou que ela
> pode ser evitada inteiramente para `K=0,1`, explorando que o
> Corolário do Teorema J (Estágio 25) é uma identidade algébrica exata
> em `n` finito, não apenas assintótica.

**Proposição R (PROVADA, redução elementar).** Como o Corolário do
Teorema J vale exatamente em todo `n` finito, se
`P_n^{(K)}(\text{ambos cíclicos})\to\tau_K` então automaticamente
`P_n^{(K)}(\text{mesmo ciclo})\to\tau_K/2` — contornando inteiramente a
obstrução de construção contínua-nativa, em vez de resolvê-la.

**`K=0` trivial. `K=1` (Proposição K1, PROVADA, nova).** Forma fechada
exata `P_n^{(1)}(\text{0,1 ambos cíclicos}) = (3n^2-n+2)/(6n^2)`,
derivada por uma análise de dois casos (fonte do reroute disjunta
de/coincidente com um ponto de consulta) que generaliza o método da
Proposição 4 de `THEOREM.md` — com um falso começo autodetectado e
disclosurado (a derivação inicial omitiu o caso coincidente, dando o
valor errado `5/9` em vez do correto `13/27` em `n=3`).

**Combinado: novo teorema contínuo POR TRANSFERÊNCIA em `K=0,1`:**
`P(\text{mesmo ciclo final} \mid K \text{ marcas}) = 1/(2(K+1))`.
`K\ge2` honestamente deixado aberto, como um problema mais estreito e
estruturalmente distinto da obstrução original de construção do zero.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee
(`spotcheck_k1_second_moment.py`): enumeração exaustiva independente
por força bruta da Definição 4 em `K=1` para `n=2,\ldots,6`, confirmando
exatamente a fórmula `(3n^2-n+2)/(6n^2)` em todo `n`.

Referee hostil dedicado (`.../joint_exploration_continuum_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script da frente:
re-derivou a Proposição R à mão, confirmando-a genuinamente tão simples
quanto reivindicada, sem caso de borda em `K=0` ou `n` pequeno;
re-derivou do zero a forma fechada `K=1` (reproduzindo
independentemente `V_a(n)=(3n+1)/(6n)` e `V_b(n)=(n+1)/(3n)` de forma
exata), depois cruzou contra enumeração fresca por força bruta
(`n=2,\ldots,7`) — todos os valores batem exatamente, incluindo
sub-casos com `R` mantido fixo; confirmou o falso começo (`5/9` em
`n=3` de fato errado, `13/27` correto); confirmou a taxa
`n(P-\tfrac12)\to-\tfrac16`; verificou de forma independente todos os 8
valores da tabela de spot-check `K=2,3` (`n=3,\ldots,7` para `K=2`,
`n=4,\ldots,6` para `K=3`), incluindo a célula mandatada `n=6,K=2:
44/135`; estressou o diagnóstico de "por que `K\ge2` não fecha" tentando
ele mesmo ajustar a forma fechada `K=2` verdadeira (um ajuste de 4
parâmetros a partir de 4 pontos exatos ainda falha em prever o 5º),
corroborando o diagnóstico de dificuldade da frente.

> **Um erro genuíno, precisamente localizado.** A narrativa causal do
> §3.3 alegava que "o Caso (a) sozinho mostraria comportamento
> `O(1/n^2)`" — **falso**, contradito pela própria fórmula de `V_a(n)`
> do documento, que já tem desvio `\Theta(1/n)` explícito. Os dois
> termos `O(1/n)` (Caso (a): coeficiente `-5/6`; Caso (b)/(c):
> coeficiente `+2/3`) cancelam parcialmente para dar a taxa `-1/6`
> corretamente relatada — não compõem como "base `O(1/n^2)` mais
> perturbação `O(1/n)`". Confinado à prosa explicativa; **não afeta**
> a Proposição K1, a reassemblagem, nem o valor da taxa `-1/6` em si.
> Corrigido por adendo datado em ATTEMPT.md §3.3.

> **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue**, no
> tier reivindicado. Nenhum outro erro encontrado; a honestidade do
> diagnóstico de não-fechamento `K\ge2` (§4/§5) foi verificada como
> precisa, sem contrabando de informação de destino escondida.

Ver
`.../conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/ATTEMPT.md`
e `.../joint_exploration_continuum_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**Um novo teorema contínuo — `P(\text{mesmo ciclo} \mid K \text{
marcas}) = 1/(2(K+1))` — está catalogado para `K=0,1`, obtido por
transferência da identidade exata do Corolário do Teorema J
(Estágio 25), não por construção contínua direta.** A obstrução de
construção contínua-nativa da Definição 3, diagnosticada nos Estágios
18/25, **permanece intocada em si mesma** — esta frente a contornou
para `K=0,1`, não a resolveu. Nenhum resultado anterior é
enfraquecido; a correção do §3.3 afeta apenas a narrativa causal
explicativa desta própria frente, não nenhum resultado catalogado
anteriormente.

**O que permanece aberto, com precisão:** a construção contínua-nativa
direta da Definição 3 em si (a obstrução original dos Estágios 18/25,
intocada); o bypass por transferência para `K\ge2` [Ver Estágio 31
abaixo — 2026-08-26: `K=2` FECHADO via transferência
(`P(\text{mesmo ciclo}\mid K=2)\to1/6`, PROVADO); `K\ge3` continua
ABERTO] (um problema mais
estreito, estruturalmente distinto, honestamente não perseguido além
de `K=1`); `C(\gamma)` para `\gamma\in(0,1)` (Estágio 26); a ponte
distribucional `M_n(c)\to_dM(c)` para `K\ge2` (Estágio 27); `p>20` de
`D^{*(p)}_r(b)` (sob revisão na onda 18) [Ver Estágio 29 abaixo —
2026-08-26: `p=21,\ldots,40` FECHADO em escala completa, mais evidência
exploratória em escala reduzida para `p=41,\ldots,60`; `p>60` continua
aberto apenas por não-executado]; o piso `H2` em `b=1`; a
constante do platô de DISC-DEC-071. Nenhuma alegação de progresso em
Millennium Problem; matemática combinatória pura interna a este
arquivo.

---

## [Extensão, Estágio 29 — 2026-08-26]

**Onda 18, frente (a), `DISC-DEC-078`/`DISC-DEC-082`
(`GENERAL-P-DSTAR-EXTENSION2-ATTEMPT`).** Alvo: estender a montagem em
forma fechada geral-`p` para as constantes de erro exatas
`D^{*(p)}_r(b)` (já provada e executada para `p=1,\ldots,10` na onda 15
e `p=11,\ldots,20` na onda 16, referee-aprovada `DISC-DEC-070`) para
`p>20` — item aberto apenas por não-executado, não por incerteza
matemática, risco baixo.

### O que aconteceu

> **Fechamento completo do alvo, e além dele.** O mandato pedia pelo
> menos `p=21,\ldots,30`; a frente fechou `p=21,\ldots,40` em escala
> completa (a mesma escala-teto `r\le200,b\le30` usada pela onda 16),
> mais uma incursão exploratória honestamente rotulada em escala
> reduzida até `p=60`. Nenhum ingrediente matemático novo é usado ou
> alegado — toda a montagem é entrada já provada, citada das ondas
> 15/16.

**Verificação exaustiva:** `124\,620` checagens exatas contra uma
verdade fundamental independente (Corolário A3, implementação própria
de números de Stirling), `0` divergências, `p=21,\ldots,40`,
`r=0,\ldots,200`, `b=0,\ldots,30` — igualando o teto de escala da onda
16 para um intervalo duas vezes mais largo. Mais uma incursão exaustiva
em escala reduzida até `p=41,\ldots,60` (`13\,420` checagens, `0`
divergências) e um teste de estresse aleatorizado (seed reservada
`20260870000`) alcançando `r` até `400` e `b` até `60` (`400`
checagens, `0` divergências). Total: `138\,040` checagens exaustivas +
`400` aleatorizadas, `0` divergências em lugar nenhum. Novas formas
fechadas, antes desconhecidas, impressas para `p=21,\ldots,40` em
`b=0,1` (limpo sem denominador, justificado por um fato descoberto e
verificado durante a derivação: `Q_p(-1)=0` para todo `p\ge1`).

### Verificação adversarial independente

Referee hostil dedicado (`.../general_p_dstar_extension2_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: reconstruiu cada ingrediente do zero por uma rota
deliberadamente **diferente** da própria frente — `Q_p(u)` via números
de Stirling de segunda espécie + identidade do taco de hóquei (em vez
da rota Bernoulli/Faulhaber da frente), momentos centrais via
recorrência log/exp em série de potências independente, e a máquina
`H_{2k-1}(r,b)` via a recursão `a_k^{(d)}` citada da fatoração/limite
de grau já provados pelo referee da onda 16. **Total: `86\,112`
checagens exatas `Fraction`, `0` divergências**, incluindo uma
varredura exaustiva completa `p=21,\ldots,40`, `r=0,\ldots,150`,
`b=0,\ldots,25` (`78\,520` checagens — grade reduzida frente ao
`r\le200,b\le30` da frente, disclosurado explicitamente como limitação
de desempenho da própria implementação do referee, não uma
discrepância encontrada), mais teste de estresse aleatorizado na seed
reservada do próprio referee (`20260871000`) alcançando `r\le300,
b\le40, p\le60` (`500` checagens, `0` falhas), checagens estruturais
(`Q_p(-1)=0` para `p=1,\ldots,60`; limite de grau até `k=45`; `r<p`
forçado a zero pela fórmula completa) e um spot-check manual da forma
fechada impressa `p=21,b=0` da própria frente contra a verdade
fundamental em 5 valores concretos de `r` (5/5 exatos). Confirmou a
alegação de "nenhum ingrediente matemático novo" como precisa — todo
fato não-trivial usado remonta à onda 15 (`DISC-DEC-063`) ou ao
referee da onda 16 (`DISC-DEC-070`), verificado por comparação direta.
Disclosure do referee: um bug real no próprio código do referee (fator
de 2 faltando na recursão `a_k^{(d)}`), capturado imediatamente pelo
próprio teste de limite de grau falhando com um diagnóstico limpo;
sem impacto em nenhum número final reportado.

> **Veredito: SOUND — ACCEPT for catalogue.** Nenhum erro encontrado em
> lugar nenhum. Ambos os bugs autodisclosurados pela própria frente
> (um off-by-one de Faulhaber; um deslize de indexação em teste
> próprio) foram reproduzidos independentemente a partir de seus
> mecanismos descritos e confirmados matematicamente exatos e
> imateriais.

Ver
`theorem/k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/general_p_dstar_closure_attempt/general_p_dstar_extension_attempt/general_p_dstar_extension2_attempt/ATTEMPT.md`
e `.../general_p_dstar_extension2_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**`D^{*(p)}_r(b)` está agora FECHADO para `p=1,\ldots,40`** (ondas
15/16/18 combinadas), em escala completa `r\le200,b\le30`, com
evidência exploratória adicional em escala reduzida até `p=60`.
Nenhum resultado anterior é enfraquecido; nenhum ingrediente
matemático novo foi introduzido — apenas execução em escala maior da
maquinaria já provada.

**O que permanece aberto, com precisão:** `p>40` em escala completa
(apenas por não-executado, a incursão `p=41,\ldots,60` é exploratória
em escala reduzida, não uma verificação completa) [Ver Estágio 32
abaixo — 2026-08-26: `p=41,\ldots,80` FECHADO em escala completa
`r\le200,b\le30`; `p>80` continua aberto apenas por não-executado]; a
ausência de uma
única fórmula elementar simbólica em `p` livre (`Q_p(u)` tem grau
genuíno `2p`); a soma em faixa `\mathrm{Strip}_p` continua sendo uma
soma explícita de `b` termos, por desenho; `C(\gamma)` para
`\gamma\in(0,1)` (Estágio 26, com a Lacuna 2 agora fechada — Estágio
30); a ponte distribucional `M_n(c)\to_dM(c)`
para `K\ge2` (Estágio 27); a construção contínua-nativa do Teorema J
(Estágio 28); o piso `H2` em `b=1`; a constante do platô de
DISC-DEC-071. Nenhuma alegação de progresso em Millennium Problem;
matemática combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 30 — 2026-08-26]

**Onda 19, frente (b), `DISC-DEC-083`/`DISC-DEC-084`
(`GAMMA-SECOND-ORDER-GAP-CLOSURE-ATTEMPT`).** Alvo: o Estágio 26 §5
nomeou três lacunas técnicas precisas entre a heurística de cumulantes
do §4 e uma prova rigorosa de `C(\gamma)` para `\gamma\in(0,1)`. Esta
frente ataca uma delas.

### O que aconteceu

> **Lacuna 2 ("a correção de flutuação de `M` em `\tau`") está FECHADA,
> rigorosamente, em forma mais forte que a pedida.** A frente anterior
> pediu um limitante `E_M[\tau(M)] = \tau(\gamma k) + O(n^{-3/4})`,
> uniforme para `k\le K\sim\sqrt{n\ln n}`, chamando-o de "computação
> curta e mecânica... não realizada". Esta frente a realiza por
> completo: `\tau(m)` é um **polinômio cúbico exato** em `m` (álgebra
> elementar), então `E_M[\tau(M)]-\tau(\gamma k)` tem valor **exato em
> forma fechada** — sem resto de Taylor, sem aproximação, válido para
> **todo** `1\le k\le n` (não apenas `k\le K`):
> `\Delta\tau(k) = \dfrac{-k^2\gamma(1-\gamma)^2+\tfrac16k\gamma(1-\gamma)(5-4\gamma)}{n^2}`,
> e a soma ponderada que de fato importa para `E(\gamma)`,
> `\Sigma_ke^{-s(k)}|\Delta\tau(k)|`, é provada (via um novo corolário —
> Lema G2 — da identidade de soma de Poisson já PROVADA da frente
> anterior, obtido por diferenciação em `a`) igual a `O(n^{-1/2})\to0`
> — mais forte que o `O(n^{-3/4})` pontual pedido: a ordem pontual real
> é `O(k^2/n^2)`, e a contribuição somada, que é o que de fato importa,
> é `O(n^{-1/2})`.

**Lema G2 (esta frente; PROVADO, corolário elementar da ferramenta de
soma de Poisson do Lema D0).**
`\Sigma_{k=1}^\infty k^2e^{-ak^2} = \tfrac{\sqrt\pi}4a^{-3/2} +
O(a^{-5/2}e^{-\pi^2/a})` quando `a\to0^+`, obtido diferenciando a
identidade de soma de Poisson do Lema D0 em relação a `a` (justificado
por convergência uniforme de ambas as séries em subintervalos compactos
de `a`, confirmado pelo referee via teste-M de Weierstrass).

**O que isto NÃO fecha.** `C(\gamma)` para `\gamma\in(0,1)` permanece
**ABERTO**. A Lacuna 1 (controle de resto de Taylor sobre
`E_M[e^{-\delta(M)-\tau(M)/2}]`, envolvendo a quantidade transcendental
`\delta`, exigindo maquinaria de controle de MGF estilo Hoeffding) está
intocada e é agora, por eliminação e por comparação direta de
dificuldade, o obstáculo dominante remanescente. A Lacuna 3
(uniformidade sobre toda a faixa de truncamento) está **parcialmente**
pré-descarregada — a peça de `\tau` fechada aqui já vale na faixa
completa `1\le k\le n`, mas a contribuição da Lacuna 1 para a Lacuna 3
permanece intocada.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: re-derivação
independente da forma fechada de `\tau(m)` e de `\Delta\tau(k)` via
sympy (identidade geral em `k,n,\gamma` e verificação separada via soma
da pmf Binomial para `k=1,\ldots,6`) — ambas batendo exatamente com o
enunciado da frente; confirmação numérica independente do Lema G2
(mpmath dps=50) em `a\in\{0.1,0.01,0.001\}`, diferença absoluta
`\sim10^{-40}$–$10^{-48}`.

Referee hostil dedicado (`.../gamma_second_order_gap_closure_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: re-derivou `\tau(m)` e `\Delta\tau(k)` à mão antes
de qualquer código; confirmou que a diferenciação da identidade de
Poisson é de fato justificada (teste-M de Weierstrass, convergência
uniforme de ambas as séries); reproduziu a tabela de razões
`W_n/W_{10n}` da frente **dígito a dígito** (`3.154462, 3.149726,
\ldots, 2.258223`); verificou explicitamente se a Lacuna 2, tal como
enunciada pela frente antecessora, exige uniformidade em `\gamma` além
de `k` — concluiu que não, e que a convergência mais lenta em
`\gamma=0.99` (disclosurada honestamente pela própria frente) não é um
defeito, apenas um fato pontual-em-`\gamma`, não um requisito
violado; avaliou a lógica de "pré-descarregamento parcial" da Lacuna 3
como estruturalmente sólida. Disclosure do referee: dois bugs no
próprio código do referee (um símbolo livre não substituído; vazamento
de float ao misturar inteiros Python com expressões sympy), ambos
capturados e corrigidos antes de qualquer conclusão.

> **Veredito: SOUND — ACCEPT for catalogue.** Nenhum erro matemático,
> uso indevido de citação ou superalegação encontrado.

Ver
`.../gamma_second_order_attempt/gamma_second_order_gap_closure_attempt/ATTEMPT.md`
e `.../gamma_second_order_gap_closure_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**A Lacuna 2 do Estágio 26 §5 está catalogada como FECHADA.** O número
de lacunas técnicas nomeadas entre a heurística do §4 e uma prova
completa de `C(\gamma)` cai de três para duas (Lacuna 1, Lacuna 3), com
a Lacuna 3 parcialmente pré-descarregada para a peça fechada aqui, e a
Lacuna 1 identificada — com razão concreta, não apenas por eliminação —
como a mais dura das duas remanescentes. Nenhum resultado anterior é
enfraquecido.

**O que permanece aberto, com precisão:** a Lacuna 1 (controle de resto
de Taylor + MGF estilo Hoeffding sobre a quantidade transcendental
`\delta(M)`) [Ver Estágio 33 abaixo — DATE: 2026-08-26]; a Lacuna 3
restrita à contribuição da Lacuna 1; `C(\gamma)`
para `\gamma\in(0,1)` em si, portanto ainda inteiramente ABERTO; a
janela intermediária do Estágio 23; a exploração conjunta (Estágio 18,
com `K=2` agora fechado — Estágio 31); `p>20` de `D^{*(p)}_r(b)`; a
ponte distribucional `M_n(c)\to_dM(c)`
para `K\ge2` (Estágio 27, com `K=2` agora fechado — Estágio 31); a
construção contínua-nativa do Teorema J
(Estágio 28, com o bypass por transferência em `K=2` agora fechado —
Estágio 31); o piso `H2` em `b=1`; a constante do platô de
DISC-DEC-071. Nenhuma alegação de progresso em Millennium Problem;
matemática combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 31 — 2026-08-26]

**Onda 19, frente (a), `DISC-DEC-083`/`DISC-DEC-086`
(`K2-JOINT-CASE-SPLIT-ATTEMPT`).** Alvo: generalizar o método de
caso-split de Proposição D1 (Estágio 27)/Proposição K1 (Estágio 28) de
`K=1` para `K=2` — a obstrução nomeada, de forma independente, como
bloqueador em QUATRO integrações distintas (o problema geral do
Estágio 18, o `P_{nn}(n,2)` da ponte distribucional do Estágio 27, o
bypass por transferência `K=2` do Estágio 28, e a exploração conjunta
em si), tornando esta a frente de maior valor estratégico da onda 19.

### O que aconteceu

> **`K=2` FECHADO, para o alvo escalar do segundo momento.** A frente
> generalizou o método de caso-split de um ponto para dois pontos
> marcados via duas novas lemas: o **Lema da Estrutura de Lacunas de
> Pontos Marcados** (para `m` pontos marcados numa permutação uniforme,
> a permutação contraída sobre eles é uniforme em `S_m`, e os tamanhos
> das lacunas entre eles são composições uniformes — generaliza o
> Passo 1 da Proposição 4 de `m=1` para `m` geral) e o **Lema da
> Estrutura de Redirecionamento de Duas Fontes** (uma análise completa
> de 9 casos de onde os dois alvos de reroute pousam em relação a dois
> arcos de ciclo).

**Proposição NN2 (PROVADA).** Forma fechada exata:
`P_{nn}(n,2) = \dfrac{10n^2+7n+2}{30n^2} = \dfrac13+\dfrac7{30n}+\dfrac1{15n^2}`,
para todo `n\ge4` — fechando o alvo de segundo momento `K=2` do
Estágio 27 (`E[(M_n^{(2)})^2]\to\tfrac13`).

**Corolário NN2.2 (PROVADO, quase de graça).** Via o Corolário já
PROVADO do Teorema J (Estágio 25, identidade exata em todo `n` finito,
não apenas assintótica): `P(\text{mesmo ciclo final}\mid K=2
\text{ marcas})\to\tfrac16` — estendendo o Teorema por transferência do
Estágio 28 de `K=0,1` para `K=2`, confirmando a hipótese do próprio
despacho de que (i) quase entrega (ii) de graça.

**Lema bônus (PROVADO).** A convenção de `n` finito diferente do
Estágio 28 converge para os mesmos limites; a tabela `K=2` já reportada
pelo Estágio 28 (`49/144, 33/100, 44/135, 143/441`) é reproduzida
exatamente por um script novo, independente.

**`K=3` honestamente diagnosticado como mais duro.** Requer rastrear um
grafo funcional nos próprios arcos (não apenas uma tabela `3\times3`
fixa), agravado pela necessidade de rastrear duas posições de
consulta simultaneamente, diferente do problema marginal `K\ge3`. O
CDF completo em `K=2` (não apenas o segundo momento) e o alvo geral
(iii) permanecem abertos, com ferramentas parciais reutilizáveis
(Lemas 1–2) nomeadas explicitamente.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: enumeração
exaustiva independente por força bruta do próprio Definição 4 em
`K=2` (todas as `n!\cdot n^2` configurações, aritmética exata),
confirmando `P_{nn}(n,2)=(10n^2+7n+2)/(30n^2)` exatamente em
`n=4,5,6,7` — sem nunca ler nenhum script da frente.

Referee hostil dedicado (`.../k2_joint_case_split_attempt/adversarial/`
`REFEREE_REPORT.md`), sem ler nenhum script de nenhuma frente da
linhagem: re-derivou os dois novos lemas do zero, antes de ler a
prova da frente de perto (para evitar ancoragem) — confirmação por
força bruta do Lema 1 (`m=2,3`, `n\le7`, 11/11 células) e do Lema 2
(construindo ambas as topologias de permutação explicitamente,
240/240 células, zero divergências); re-derivou a Proposição NN2
independentemente dos Lemas 1+2 (não a partir da fórmula da frente) —
correspondência exata `n=4,\ldots,12` (9/9); enumeração exaustiva
totalmente independente do modelo completo `K=2` da Definição 4 —
correspondência exata `n=4,\ldots,10` (7/7), incluindo uma execução de
29,4 milhões de configurações em `n=9` e, além do pedido mínimo do
mandato, uma execução de 362.880.000 configurações exatas em `n=10`
(`P_{nn}(10,2)=134/375`, batendo exatamente com a predição
independente da rota Lema 1+2); confirmou
independentemente o Corolário do Teorema J (`P(\text{mesmo}\mid
\text{ambos})=1/2`) em cada `n=4,\ldots,10` dentro de sua própria
enumeração, não por confiança cega; reproduziu por força bruta
independente os 4 valores da tabela do Estágio 28 (o mandato pedia
`\ge2`); construiu explicitamente uma topologia `K=3` e mostrou que a
extensão "plana" ingênua da fórmula `K=2` falha (a probabilidade
depende da divisão individual do comprimento dos arcos, não apenas da
soma) — confirmando concretamente o diagnóstico da própria frente de
que `K=3` precisa de maquinaria genuinamente nova, não uma rendição
prematura. Único achado: uma inconsistência puramente cosmética de
prosa em §3.1 (rótulos de fonte trocados numa observação lateral,
relativa à própria convenção do documento) — verificada por construção
independente que as fórmulas reais estão corretas em ambas as
topologias; nenhuma prova é afetada.

> **Veredito: SOUND — ACCEPT for catalogue.** Nenhum bug encontrado na
> matemática do documento-alvo; nenhum bug encontrado no próprio
> código de verificação do referee.

Ver
`.../conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/k2_joint_case_split_attempt/ATTEMPT.md`
e `.../k2_joint_case_split_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**`P_{nn}(n,2)\to\tfrac13` está agora PROVADO** — fechando `K=2` do
Estágio 27, e, por transferência via o Corolário do Teorema J,
também `K=2` do bypass do Estágio 28
(`P(\text{mesmo ciclo}\mid K=2)\to\tfrac16`). O item nomeado, de forma
independente, como bloqueador em quatro integrações distintas
(Estágios 18, 25, 27, 28) está agora resolvido para `K=2`
especificamente — a maior alavancagem estratégica de uma única frente
nesta onda. `K\ge3` permanece aberto, agora com um diagnóstico
estrutural concreto (não apenas uma afirmação de dificuldade) do
porquê o método de caso-split não se estende diretamente. Nenhum
resultado anterior é enfraquecido.

**O que permanece aberto, com precisão:** `K\ge3` da ponte
distribucional (Estágio 27) e do bypass por transferência (Estágio
28) — diagnóstico estrutural agora disponível, mas nenhuma solução
[Ver Estágio 35 abaixo — DATE: 2026-08-26, K=3 especificamente
fechado];
o CDF completo em `K=2` (não apenas o segundo momento); o problema
geral (iii) da exploração conjunta (Estágio 18); a construção
contínua-nativa direta da Definição 3 em si (intocada); `C(\gamma)`
para `\gamma\in(0,1)` (Estágios 26/30); `p>80` de `D^{*(p)}_r(b)`
(Estágio 32); o
piso `H2` em `b=1`; a constante do platô de DISC-DEC-071. Nenhuma
alegação de progresso em Millennium Problem; matemática combinatória
pura interna a este arquivo.

---

## [Extensão, Estágio 32 — 2026-08-26]

**Onda 19, frente (c), `DISC-DEC-083`/`DISC-DEC-087`
(`GENERAL-P-DSTAR-EXTENSION3-ATTEMPT`).** Alvo: estender a montagem em
forma fechada geral-`p` para as constantes de erro exatas
`D^{*(p)}_r(b)` de `p=1,\ldots,40` (já provada e executada até a onda
18, `DISC-DEC-082`) para `p=41,\ldots,80` — em ESCALA COMPLETA
(`r\le200,b\le30`, mesma escala-teto usada desde a onda 16), tanto
confirmando em escala completa a incursão exploratória em escala
reduzida da onda 18 (`p=41,\ldots,60`) quanto estendendo além dela
(`p=61,\ldots,80`).

### O que aconteceu

> **Mandato completo alcançado em escala completa.** Todos os 40
> novos valores de `p` fechados em `r\le200,b\le30`, sem nenhum
> ingrediente matemático novo — toda a montagem é entrada já provada
> das ondas 15/16/18.

**Verificação exaustiva da própria frente:** `261\,274` checagens
exatas `Fraction`, `0` divergências, incluindo `249\,240` checagens
exaustivas em escala completa (`p=41,\ldots,80`, `r=0,\ldots,200`,
`b=0,\ldots,30`), mais autotestes de ingredientes, checagens de formas
impressas, e um teste de estresse aleatorizado (`400` checagens, seed
`20260884000`, `r\le400,b\le60`). `Q_p(-1)=0` reconfirmado para todo
`p=41,\ldots,80`. Uma reparametrização bivariada `(x,y)` da recursão
`A_k` citada foi necessária por engenharia de escala (o rebuild
ingênuo por `(p,b)` da máquina `H_k` era computacionalmente inviável
nesta escala) — verificada contra três rotas alternativas
independentes.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: computação
independente da soma direta de Corolário A3 (números de Stirling,
implementação própria) em vários `(p,r,b)` com `p` até `80`,
`r=200`, `b=30` — confirmando que a quantidade-alvo é computável na
escala reivindicada, sem nunca ler nenhum script da frente.

Referee hostil dedicado (`.../general_p_dstar_extension3_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: reconstruiu cada ingrediente por rota
deliberadamente diferente (Stirling de segunda espécie + identidade do
taco de hóquei para `Q_p`, em vez de Bernoulli/Faulhaber; soma direta
fechada para `H_{2k-1}` em vez da recursão bivariada da frente).
**Total: `163\,008` checagens exatas `Fraction`, `0` divergências**,
incluindo uma varredura de fronteira batendo exatamente a escala
completa reivindicada em três `p` representativos (`41,60,80`,
`r\le200,b\le30`, incluindo a célula mais extrema `p=80,r=200,b=30`).
Verificou especificamente, por implementação independente da recursão
`A_k` original não-reparametrizada, que a reparametrização bivariada
da frente é matematicamente inerte (mera relabeling), não um atalho
não verificado. Confirmou a alegação de "nenhum ingrediente novo".

> **Um achado nomeado, menor, apenas de narrativa (não matemático).**
> A própria frente disclosurou (§5.1) um erro de raciocínio em seu
> próprio autoteste (assumiu Teorema 3 = `D^{*(1)}_r(0)`, quando na
> verdade é `D^{*(2)}_r(0)`) — o referee confirmou a substância
> matematicamente relevante desta disclosure (`40/40` correspondências
> contra `D^{*(2)}_r(0)`), mas encontrou que o **ponto de início da
> divergência** declarado (`r=12`) está incorreto — a divergência real
> começa em `r=1`, não `r=12` (a contagem total de `39` falhas está
> correta). Sem efeito em nenhuma implementação ou checagem numérica.
> Corrigido por adendo datado em `ATTEMPT.md` §5.1.

> **Veredito: SOUND — ACCEPT for catalogue.**

Ver
`theorem/k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/error_constant_growth_attempt/all_orders_closed_form_attempt/general_b_dstar_attempt/general_p_dstar_closure_attempt/general_p_dstar_extension_attempt/general_p_dstar_extension2_attempt/general_p_dstar_extension3_attempt/ATTEMPT.md`
e `.../general_p_dstar_extension3_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**`D^{*(p)}_r(b)` está agora FECHADO para `p=1,\ldots,80`** (ondas
15/16/18/19 combinadas), em escala completa `r\le200,b\le30`. Nenhum
resultado anterior é enfraquecido; nenhum ingrediente matemático novo.

**O que permanece aberto, com precisão:** `p>80` em escala completa
(apenas por não-executado); a ausência de uma única fórmula elementar
simbólica em `p` livre; `K\ge3` da exploração conjunta (Estágio 31);
`C(\gamma)` para `\gamma\in(0,1)` (Estágios 26/30
[Ver Estágio 33 abaixo — DATE: 2026-08-26]); a ponte
distribucional `M_n(c)\to_dM(c)` para `K\ge2` (Estágios 27/31); a
construção contínua-nativa direta do Teorema J (Estágio 28); o piso
`H2` em `b=1`; a constante do platô de DISC-DEC-071. Nenhuma alegação
de progresso em Millennium Problem; matemática combinatória pura
interna a este arquivo.

---

## [Extensão, Estágio 33 — 2026-08-26]

**Onda 20, frente (a), `DISC-DEC-088`/`DISC-DEC-089`
(`GAMMA-GAP1-MGF-ATTEMPT`).** Alvo: a Lacuna 1 do Estágio 26 §5
(controle de resto de Taylor + MGF estilo Hoeffding sobre a quantidade
transcendental `\delta(M)`), o único obstáculo nomeado remanescente
para `C(\gamma)` para `\gamma\in(0,1)` após o fechamento da Lacuna 2
(Estágio 30).

### O que aconteceu

> **A Lacuna 1 NÃO está fechada.** Isto é um FECHAMENTO PARCIAL
> honesto, de caráter diferente do da Lacuna 2: onde a Lacuna 2 tinha
> resposta exata em forma fechada, a Lacuna 1 não tem — o objeto de
> estudo é genuinamente transcendental. A frente entrega: (i) um novo
> fato algébrico exato — `x(D):=\delta(D)+\tau(M)/2` é um **polinômio
> cúbico exato** em `D:=M-\gamma k`, com coeficientes `c_0,\ldots,c_3`
> em forma fechada (não isolado anteriormente nesta linhagem); (ii) um
> novo **Lema Bulk/Tail** rigoroso, reduzindo a Lacuna 1 a limitar duas
> quantidades escalares determinísticas `g(\Theta_K),g(K)` conforme
> `n\to\infty`, via monotonicidade + a desigualdade de Hoeffding (já
> citação clássica desta linhagem); (iii) assintótica de ordem
> dominante (não uma desigualdade totalmente explícita-em-constante)
> mostrando que o limitante resultante de fato se anula; (iv)
> confirmação numérica direta, via soma exata da pmf Binomial
> (`mpmath` dps=50, sem atalhos), de que a quantidade-alvo literal da
> Lacuna 1 encolhe monotonicamente em `n`, em 6 valores de `\gamma`
> amostrados.

**O que isto NÃO fecha.** `C(\gamma)` para `\gamma\in(0,1)` permanece
**ABERTO**. Falta converter a assintótica de ordem dominante em uma
desigualdade `n\ge n_0(\gamma)` totalmente explícita e uniforme em
`\gamma\in(0,1)` como contínuo (verificado apenas em 6 pontos amostrais
mais os dois limites de contorno), e fixar a constante literal `\kappa_0`
da truncagem `K\sim\sqrt{n\ln n}` citada da onda 17 (uma substituição de
constante, não uma lacuna estrutural). A Lacuna 3 permanece com sua
contribuição da Lacuna 1 intocada, ainda que a forma do Lema Bulk/Tail
já seja uniforme em `k\le K` por construção — tornando visível, mas não
executando, a forma de um futuro fechamento da Lacuna 3.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: re-derivação
simbólica independente (sympy, substituição de `\tau(m)` cúbica exata
com `M=\gamma k+D` e extração de coeficientes via `Poly`) de todos os
quatro coeficientes `c_0,\ldots,c_3` do polinômio cúbico `x(D)`,
confirmando exatidão contra as fórmulas declaradas pela frente, sem
nunca ler nenhum script da frente.

Referee hostil dedicado (`.../gamma_gap1_mgf_attempt/adversarial/`
`REFEREE_REPORT.md`), sem ler nenhum script de nenhuma frente da
linhagem: re-derivou a identidade cúbica de `x(D)` por duas rotas
simbólicas independentes (substituição direta + `Poly`, e montagem à
mão via `\tau,\tau',\tau''` em `m=\gamma k`), confirmando exatidão da
forma "derivative-based"; re-verificou a lógica de prova do Lema
Bulk/Tail passo a passo e a checou numericamente (pmf exata, `mpmath`
dps=50) em pontos amostrais e numa varredura completa `k=1,\ldots,K`;
re-derivou a álgebra da assintótica de ordem dominante do §3.3 de
forma independente, confirmando ajuste numérico do expoente `\lambda`
a `4,3\%$–$5,3\%` do previsto (a frente reporta `\sim6\%`); reconstruiu
a tabela de `W_{\mathrm{bound}}(n,\gamma)$` da §4 do zero (pmf exata,
`mpmath` dps=50), batendo os valores publicados a `<1\%` em todos os 18
pontos testados, com `R_k^{\mathrm{exact}}\le R_k^{\mathrm{Gap1}}` sem
violações.

> **Três achados nomeados, nenhum alterando o veredito de não-fechamento.**
> (1, MODERADO) O Lema Bulk/Tail, tal como usado em §3.3, depende
> implicitamente de `|c_i(k)|` ser não-decrescente em `k` — fato não
> declarado e não literalmente verdadeiro termo-a-termo (o referee
> encontrou `c_1(k)` mudando de sinal para `\gamma` próximo de `1`); a
> checagem mais profunda do referee (os dois fatos que a prova
> realmente precisa, comparando contra os coeficientes de `K`) não
> encontrou nenhuma falha em nenhum caso testado. (2, BAIXO) A "forma
> algébrica fechada" alternativa de `c_0` em §2 carrega um fator
> espúrio extra de `\gamma` em cinco dos seus seis termos — a forma
> "derivative-based", efetivamente usada em toda a numérica da frente,
> permanece exata. (3, BAIXO) A §1 alega que uma checagem de
> equivalência "was checked in Section 2", quando na verdade a §2 não a
> aborda — a própria §5.4 da frente já disclosurava honestamente que
> essa checagem não foi feita, contradizendo a §1. Todos os três
> corrigidos por adendos datados em `ATTEMPT.md`.

> **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

Ver
`.../gamma_second_order_gap_closure_attempt/gamma_gap1_mgf_attempt/ATTEMPT.md`
e `.../gamma_gap1_mgf_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**A Lacuna 1 do Estágio 26 §5 permanece ABERTA**, mas com uma
estratégia de prova concreta, estruturalmente sólida e
numericamente validada — não mais "nenhuma tentativa, dificuldade
transcendental" (avaliação do próprio Estágio 30), mas "estratégia
concreta, rigor parcial forte, forte suporte numérico, não totalmente
montada". `C(\gamma)` para `\gamma\in(0,1)` permanece inteiramente
ABERTO. Nenhum resultado anterior é enfraquecido.

**O que permanece aberto, com precisão:** a Lacuna 1 em si (converter
a assintótica de ordem dominante em desigualdade explícita uniforme em
`\gamma\in(0,1)`, fixar `\kappa_0`); `C(\gamma)` para `\gamma\in(0,1)`;
a Lacuna 3 restrita à contribuição da Lacuna 1; a janela intermediária
do Estágio 23 [Ver Estágio 34 abaixo — DATE: 2026-08-26]; a exploração
conjunta para `K\ge3` (Estágio 31); `p>80`
de `D^{*(p)}_r(b)` (Estágio 32); a ponte distribucional
`M_n(c)\to_dM(c)` para `K\ge2` (Estágios 27/31); a construção
contínua-nativa direta do Teorema J (Estágio 28); o piso `H2` em `b=1`;
a constante do platô de DISC-DEC-071; `H1`/`H2` da lei assintótica do
platô M-CLUST(b) (`PROOF_DEPENDENCY_MAP.md`, nó `PLATRESUM`). Nenhuma
alegação de progresso em Millennium Problem; matemática combinatória
pura interna a este arquivo.

---

## [Extensão, Estágio 34 — 2026-08-26]

**Onda 20, frente (d), `DISC-DEC-088`/`DISC-DEC-090`
(`GAMMA-INTERMEDIATE-WINDOW-ATTEMPT`).** Alvo: a janela intermediária
`n^\epsilon\le c_n\le n^{2/3}/\log n`, entre o regime `c` fixo do
Estágio 10 e o regime `\gamma_n\ge n^{-1/3}\ln n` do Corolário 2
(Estágio 23), nomeada como resíduo aberto desde a onda 17, nunca
atacada por nenhuma frente dedicada até agora.

### O que aconteceu

> **FECHAMENTO COMPLETO da janela nomeada**, por combinação direta e
> elementar de dois resultados JÁ PROVADOS do arquivo — Teorema R
> (Estágio 22) e Corolário 4.2 (Estágio 6) — sem nenhuma maquinaria
> nova. **Teorema W (esta frente, PROVADO).** Para todo inteiro `n\ge4`
> e todo real `1\le c\le n`,
> `|\varphi(n,c)/\varphi_\infty(c)-1|\le B(n,c):=(a^*\sqrt c+\kappa_B)/
> \big(n[(\sqrt\pi/2)c^{-1/2}-e^{-c}/(2c)]\big)`. Consequentemente, para
> todo `\epsilon\in(0,2/3)` fixo e toda sequência `c_n` com
> `n^\epsilon\le c_n\le n^{2/3}/\log n`,
> `\varphi(n,c_n)/\varphi_\infty(c_n)\to1`, com taxa explícita não
> assintótica `O(n^{-1/3}/\log n)` na aresta mais dura (superior) e
> mais rápida em todo o resto da janela.

**Bônus honesto, além do mandato:** o mesmo argumento dá
`B(n,c_n)\to0$` para **qualquer** sequência com `c_n\to\infty` e
`c_n=o(n)` — sem nenhuma restrição de taxa mínima de crescimento de
`c_n` — subsumindo estritamente a metade `\gamma_n\to0` do Corolário 2
(que exigia a hipótese extra `\gamma_n n^{1/3}/\ln n\to\infty`) por um
argumento bem mais curto. **Isto NÃO toca, enfraquece ou reprova** a
metade `\gamma_n\to\gamma^*\in(0,1]` do Corolário 2, que exige a
maquinaria mais fina e dá estritamente mais (o limite não-trivial exato
`\sqrt{2/(2-\gamma^*)}`, taxa `O(n^{-1/4})` provada, termo de segunda
ordem conjecturado) — território genuinamente diferente e mais duro,
não atacado por esta frente.

**Diagnóstico chave.** A frente predecessora (`gamma_scaling_attempt`)
já havia considerado e rejeitado corretamente esta rota via Teorema R —
mas apenas no regime de `\gamma` FIXO `>0` (`c=\gamma n`), onde
`\varphi_\infty(\gamma n)=\Theta(n^{-1/2})` torna o limitante `O(1/n)`
absoluto de Teorema R vazio em termos relativos. Essa diagnose é
correta para `\gamma` fixo `>0` e permanece correta — mas o predecessor
não verificou separadamente se a mesma rota é vazia no regime
`\gamma_n\to0`. Não é: `\varphi_\infty(c_n)` é, ali, maior que
`\Theta(n^{-1/2})` (pois `c_n=o(n)`), tornando a divisão do limitante
absoluto de Teorema R genuinamente evanescente em termos relativos —
exatamente o mecanismo explorado por este resultado.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: (i) confirmação
direta, contra o texto de `THEOREM.md`, de que Teorema R (Estágio 22) e
Corolário 4.2 (Estágio 6) são citados com exatidão pela frente
(constantes, domínios de validade, forma da desigualdade); (ii)
implementação própria e independente (mpmath dps=50) da fórmula
soma-dupla exata de `\varphi(n,c)$` (Lema 1, citado, não re-lido de
nenhum script), confirmando Teorema R (0 violações) e a desigualdade
combinada do Teorema W (0 violações em 15 pontos, `n=4..300`,
`\epsilon\in\{0,1;0,3;0,5\}`) — o processo de checagem numérica em
`n=1000` foi encerrado por lentidão (`O(n^2)` em precisão dps=50) após
já ter acumulado evidência suficiente nos pontos menores.

Referee hostil dedicado (`.../gamma_intermediate_window_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: re-derivou a montagem algébrica do Teorema W à mão
e confirmou computacionalmente; confirmou as duas citações exatas
contra `THEOREM.md`; re-derivou independentemente a não-vacuidade e
disjunção da janela; re-derivou as taxas assintóticas em ambas as
arestas; re-derivou o "bônus" **do zero, algebricamente** (não apenas
re-citando) e o testou numericamente com uma sequência deliberadamente
lenta, `c_n=\log n$` — que falha provadamente a hipótese do Corolário 2
mas satisfaz a hipótese do bônus — confirmando `\to1` exatamente como
alegado; confirmou, por contraste, que para `\gamma` fixo `>0` o
limitante converge a uma constante NÃO-nula (não a zero), validando a
diagnose do predecessor sem disputa; reconstruiu um motor `\varphi(n,c)`
independente do zero e reproduziu os números específicos publicados
pela frente em `n=3000` dígito a dígito.

> **Dois achados nomeados, ambos MENORES e apenas apresentacionais
> (nenhum erro matemático).** (1) A caixa do veredito afirmava
> `\epsilon\in(0,1)`, inconsistente com a própria §0 do documento, que
> deriva corretamente `\epsilon\in(0,2/3)` para não-vacuidade genuína —
> corrigido. (2) Um limiar numérico auxiliar reportado para `\epsilon=0,5`
> (`n\gtrsim10^{12}`) reflete um artefato de grade de teste esparsa; a
> travessia real fica entre `10^7` e `10^8` — corrigido, sem afetar
> nenhum teorema.

> **Veredito: SOUND WITH NAMED ISSUES (ambos menores, apresentacionais)
> — a alegação de FECHAMENTO COMPLETO e a generalização bônus
> permanecem de pé.**

Ver
`.../gamma_scaling_attempt/gamma_intermediate_window_attempt/ATTEMPT.md`
e `.../gamma_intermediate_window_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**A janela intermediária nomeada desde a onda 17 (`n^\epsilon\le c_n\le
n^{2/3}/\log n`) está FECHADA**, por combinação de dois resultados já
provados, sem nenhum ingrediente matemático novo. Como corolário
honesto (bônus, não alvo original), a metade `\gamma_n\to0` do Corolário
2 (Estágio 23) está estritamente fortalecida — a hipótese de taxa
mínima `\gamma_n n^{1/3}/\ln n\to\infty$` deixa de ser necessária para a
conclusão `\to1`; a metade `\gamma_n\to\gamma^*\in(0,1]` do Corolário 2
permanece inteiramente intocada e mais forte onde se aplica. Nenhum
resultado anterior é enfraquecido.

**O que permanece aberto, com precisão:** a Lacuna 1 do Estágio 26/33
(`C(\gamma)` para `\gamma\in(0,1)`, ainda ABERTO); a exploração conjunta
para `K\ge3` (Estágio 31) [Ver Estágio 35 abaixo — DATE: 2026-08-26];
`p>80` de `D^{*(p)}_r(b)` (Estágio 32); a
ponte distribucional `M_n(c)\to_dM(c)` para `K\ge2` (Estágios 27/31); a
construção contínua-nativa direta do Teorema J (Estágio 28); o piso
`H2` em `b=1`; a constante do platô de DISC-DEC-071; `H1`/`H2` da lei
assintótica do platô M-CLUST(b). Nenhuma alegação de progresso em
Millennium Problem; matemática combinatória pura interna a este
arquivo.

---

## [Extensão, Estágio 35 — 2026-08-26]

**Onda 20, frente (b), `DISC-DEC-088`/`DISC-DEC-092`
(`K3-JOINT-STRUCTURAL-ATTEMPT`).** Alvo: tentar `K=3` da exploração
conjunta, generalizando o método de caso-split de K=2 (Estágio 31), que
diagnosticou precisamente que `K=3` exige rastrear um grafo funcional
de reroteamento nos próprios arcos marcados — obstrução genuinamente
mais dura que a tabela plana `3\times3` de `K=2`.

### O que aconteceu

> **`K=3` FECHADO para os alvos escalares de segundo momento/mesmo
> ciclo** — resultado surpreendente e de alto valor: o Estágio 31 havia
> diagnosticado `K=3` como estruturalmente muito mais difícil, e o
> mandato da onda 20 tratava não-fechamento honesto como plenamente
> aceitável. Esta frente fechou completa e corretamente, identificando
> duas simplificações genuínas que respondem diretamente ao diagnóstico
> do Estágio 31, em vez de contorná-lo: (i) **Reindexação por
> Fonte-Governante** (corolário novo do Lema 1 do Estágio 31,
> re-verificado fresco em `m=3`): por exchangeability, a topologia
> `\sigma` se marginaliza inteiramente, tornando o problema tratável;
> (ii) **Lema 4 (Unicidade do Predecessor-de-Ciclo)**: o conjunto
> cíclico de cada arco depende apenas do único predecessor-de-ciclo no
> grafo funcional de 3 nós, sendo qualquer outra fonte incidente
> provadamente inerte — isto colapsa a tabela de 64 células diagnosticada
> pelo Estágio 31 em regras fechadas lineares/bilineares.
>
> **Proposição NN3 (PROVADA, derivação simbólica exata, sympy,
> aritmética `Rational`):**
> `P_{nn}(n,3) = (35n^3+38n^2+23n+6)/(140n^3) = 1/4+19/(70n)+23/(140n^2)+3/(70n^3)`,
> para todo `n\ge6` (na verdade já válida em `n=5`, achado do referee,
> não um defeito). **Corolário NN3.1** (PROVADO): `E[(M_n^{(3)})^2]\to
> 1/4`, fechando o item K=3 de segundo momento nomeado desde o Estágio
> 27/18. **Corolário NN3.2** (PROVADO): `P(\text{mesmo ciclo}\mid K=3)
> \to1/8`, estendendo o teorema de transferência por continuum dos
> Estágios 28/31 (`1/(2(K+1))`) para `K=3`, confirmando o padrão
> `1/2,1/4,1/6,1/8` em `K=0,1,2,3`.

**O que isto NÃO fecha.** A CDF completa de `M_n^{(3)}` (estilo
Proposição D1, não apenas o segundo momento) permanece ABERTA — Lemas
4/5 dão apenas a lei conjunta par-a-par, não a distribuição de contagem
completa. A lei conjunta de dois pontos para `K` geral também permanece
ABERTA — os dois mecanismos novos (reindexação por fonte-governante;
redução por predecessor-de-ciclo) são estruturalmente gerais (nada na
prova do Lema 4 é específico de exatamente 3 fontes), sugerindo — como
uma pista precisamente delimitada, não uma alegação — que possam
generalizar, mas isto não foi tentado.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: implementação
independente e fresca (força bruta exata, `Fraction`, construída
apenas da Definição 4, sem ler nenhum script da frente) do modelo
completo K=3 em `n=6`, confirmando `P_{nn}(6,3)=3/10` exatamente,
batendo com a Proposição NN3.

Referee hostil dedicado (`.../k3_joint_structural_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: re-verificou exaustivamente o Lema 1 em `m=3` e a
Reindexação por Fonte-Governante (`n=4..7`, zero divergências);
verificou o Lema 4 em duas camadas — nível-fonte (exaustivo sobre as
64 funções `dest`, zero exceções em 78 instâncias cíclicas) e
nível-posição (simulação de grafo funcional totalmente independente,
`45\,424` configurações, `29\,280` com aresta extra genuinamente
inerte, zero divergências); re-derivou o Lema 5 simbolicamente por
análise de casos própria e cruzou contra enumeração exata; **atacou a
Proposição NN3 por três rotas independentes**: (a) força bruta crua do
modelo completo da Definição 4, `n=5,\ldots,9`, incluindo uma
enumeração completa em `n=9` (`264\,539\,520` configurações, `~102s`),
`5/5` correspondências exatas; (b) montagem de modelo reduzido própria
(não copiada da frente), `n=5,\ldots,30,40`, `27/27` correspondências;
(c) derivação simbólica tripla-soma totalmente independente,
algebricamente idêntica à forma fechada reivindicada. Re-testou
diretamente com dados brutos frescos (não apenas citação) a alegação
"mesmo ciclo = 1/2" do Teorema J em `K=3` especificamente
(`n=6,7,8`, exatamente `1/2` em todos). Confirmou a honestidade da §8
(CDF completa e lei geral-K corretamente escopadas como abertas).

> **Um achado nomeado, negligível/cosmético (nenhum erro matemático).**
> A prosa da §3.3 chama o índice menor `i` (em `i<i'`, mesmo arco) de
> "o marginal do ponto mais próximo da cauda" — pela própria convenção
> da frente (posição `L_s`, o índice máximo, é a cauda), `i` está na
> verdade MAIS LONGE da cauda, não mais perto. A fórmula em si e seu
> uso permanecem corretos (re-verificados independentemente); apenas o
> rótulo descritivo está invertido — mesma classe de deslize cosmético
> já encontrada pelo referee da frente K=2 predecessora. Corrigido por
> nota datada (não correção) em `ATTEMPT.md` §3.3.

> **Veredito: SOUND — ACCEPT for catalogue**, no tier reivindicado.

Ver
`.../conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/k2_joint_case_split_attempt/k3_joint_structural_attempt/ATTEMPT.md`
e `.../k3_joint_structural_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**`K=3` da exploração conjunta está FECHADO para os alvos escalares de
segundo momento/mesmo ciclo** — resposta direta e não-contornada ao
diagnóstico estrutural do Estágio 31, via dois novos mecanismos
(reindexação por fonte-governante; redução por predecessor-de-ciclo).
O padrão de transferência por continuum `1/(2(K+1))` agora confirmado
em `K=0,1,2,3`. Nenhum resultado anterior é enfraquecido.

**O que permanece aberto, com precisão:** a CDF completa de
`M_n^{(3)}` (Estágio 27's Proposição D1, estilo geral, ainda não
estendida a K=3); a lei conjunta de dois pontos para `K` geral (método
flagrado como plausivelmente generalizável, não tentado); a Lacuna 1
do Estágio 26/33/30 (`C(\gamma)` para `\gamma\in(0,1)`)
[Ver Estágio 36 abaixo — DATE: 2026-08-26]; `p>80` de
`D^{*(p)}_r(b)` (Estágio 32); a construção contínua-nativa direta do
Teorema J (Estágio 28); o piso `H2` em `b=1`; a constante do platô de
DISC-DEC-071; `H1`/`H2` da lei assintótica do platô M-CLUST(b).
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 36 — 2026-08-26]

**Onda 21, frente (a), `DISC-DEC-093`/`DISC-DEC-094`
(`GAMMA-GAP1-CONTINUATION-ATTEMPT`).** Alvo: continuar o fechamento
parcial da Lacuna 1 do Estágio 33, atacando os três itens que aquele
Estágio deixou precisamente nomeados em aberto (converter a
assintótica de ordem dominante numa desigualdade explícita
`n\ge n_0(\gamma)` uniforme em `\gamma`; fixar a constante `\kappa_0`
da truncagem).

### O que aconteceu

> **Achado principal: uma CORREÇÃO a uma afirmação já integrada do
> Estágio 33.** Lendo a prova do Teorema 2 da própria frente da onda
> 17 (`gamma_scaling_attempt/ATTEMPT.md` §5), a truncagem exata é
> `K:=⌈√((4/β)n\ln n)⌉`, `β:=γ(2-γ)/2`, dando
> `\kappa_0(\gamma)=4/\beta=8/(\gamma(2-\gamma))` — uma FUNÇÃO de
> `\gamma`, não a constante ilustrativa `2,25` usada por Estágio 33.
> Consequentemente `\lambda(\gamma)=\kappa_0(\gamma)(3/2-\gamma)=
> 4(3-2\gamma)/(\gamma(2-\gamma))` é contínua mas NÃO LIMITADA em
> `(0,1)` (diverge conforme `\gamma\to0^+`) — refutando diretamente a
> afirmação do predecessor de que `\lambda` era "limitada em `(0,1)`".
> **A substituição corretamente escopada é PROVADA** (álgebra exata,
> não apenas amostragem numérica: `\lambda(\gamma)` é estritamente
> decrescente em `(0,1)`, sem raiz real do numerador de `\lambda'` no
> intervalo): um único `C(\gamma_0)` funciona uniformemente em todo
> compacto `[\gamma_0,1)\subset(0,1)`, `\gamma_0>0` fixo — o mesmo
> padrão "uniforme em compactos" já usado alhures nesta linhagem
> (Corolário 1 da onda 17) — mas nenhum `C` único funciona no intervalo
> aberto `(0,1)` inteiro simultaneamente.
>
> **Segundo achado: uma desigualdade explícita `\forall n\ge n_0(\gamma)`
> foi de fato construída** (o item 1 do Estágio 33), fechando a lacuna
> LÓGICA (assintótica → explícita) — mas não a lacuna PRÁTICA: usando
> constantes elementares deliberadamente cruas (desigualdade
> triangular, `\ln n\le2\sqrt n`), o limiar `n_0(\gamma)` resultante é
> astronomicamente grande (`\sim10^{21}` em `\gamma=0,99` até
> `\sim10^{85}` em `\gamma=0,01`), muitas ordens de magnitude além de
> qualquer `n` numericamente alcançável nesta linhagem. Verificado sem
> oscilação espúria em mais de 60 décadas além de cada `n_0(\gamma)`
> certificado.

**O que isto NÃO fecha.** A Lacuna 1 permanece ABERTA; `C(\gamma)`
para `\gamma\in(0,1)` permanece inteiramente ABERTO. Constantes mais
afiadas (uma técnica de controle de cauda diferente, não-Hoeffding, ou
rastreamento de cancelamento exato em vez de pior-caso) seriam
necessárias para um `n_0(\gamma)` numericamente útil — não tentado
aqui.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: confirmação
direta, lendo `gamma_scaling_attempt/ATTEMPT.md` pessoalmente, de que
a fórmula de truncagem `K:=⌈√((4/β)n\ln n)⌉`, `β:=γ(2-γ)/2` é citada
com exatidão; re-derivação independente da álgebra
`\kappa_0(\gamma)=8/(\gamma(2-\gamma))` e
`\lambda(\gamma)=4(3-2\gamma)/(\gamma(2-\gamma))`, confirmando
`\lambda(1)=4` e a divergência conforme `\gamma\to0`, antes de
despachar o referee.

Referee hostil dedicado (`.../gamma_gap1_continuation_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: leu a fonte primária (`gamma_scaling_attempt/
ATTEMPT.md`) pessoalmente e confirmou a citação exata e o contexto;
re-derivou `\kappa_0(\gamma)` e `\lambda(\gamma)` do zero (sympy,
diferença simbólica exatamente zero); confirmou a monotonicidade
estrita de `\lambda` de duas formas independentes (`sympy.solve` +
varredura numérica de 19.999 pontos); reconstruiu inteiramente da
prosa (sem nunca consultar os scripts da frente) a construção
explícita completa (limitantes de coeficiente, `\hat G(n,\gamma)`,
`K\le K_{\max}`, `W(n,\gamma,C)`, e a tabela `n_0(\gamma)`),
confirmando os 8 valores de `n_1(\gamma)` reportados como inteiros
EXATOS e os 8 valores de `\log_{10}n_0(\gamma)` a `<0,004` de
diferença.

> **Um achado nomeado, BAIXA severidade, puramente narrativo/cosmético
> (não afeta nenhum resultado de carga).** Uma frase descritiva na §4
> afirmava um "fator de folga" `\hat\lambda/\lambda` "entre `3`
> (`\gamma=1`) e `\approx4,67` (`\gamma\to0`)"; o valor correto em
> `\gamma=1` é `6`, não `3` (a razão é crescente em `\gamma`, o oposto
> do que a frase sugeria). O número `3` nunca é usado em nenhuma
> fórmula posterior — `C_0(\gamma)`, `\hat G(n,\gamma)` e toda a
> tabela `n_0(\gamma)` usam `\hat\lambda(\gamma)` diretamente,
> re-verificados corretos pelo referee. Corrigido por adendo datado em
> `ATTEMPT.md`.

> **Veredito: SOUND WITH ONE NAMED ISSUE (BAIXA) — ACCEPT for
> catalogue.** A alegação central de correção — que a afirmação de
> limitação do Estágio 33/predecessor está errada — foi CONFIRMADA
> além de dúvida razoável.

Ver
`.../gamma_gap1_mgf_attempt/gamma_gap1_continuation_attempt/ATTEMPT.md`
e `.../gamma_gap1_continuation_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

**Uma afirmação real do predecessor imediato (Estágio 33's fonte,
`gamma_gap1_mgf_attempt/ATTEMPT.md` §5 item 2) foi corrigida por
adendo datado**: `\lambda(\gamma)` não é limitada em `(0,1)` como
alegado — é não-limitada, com a substituição corretamente escopada
(uniforme em compactos) agora provada rigorosamente. Além disso, o
item 1 do Estágio 33 (desigualdade explícita) está agora tecnicamente
satisfeito, embora não numericamente útil dado o tamanho de
`n_0(\gamma)`. `C(\gamma)` para `\gamma\in(0,1)` permanece inteiramente
ABERTO. Nenhum resultado numérico anterior é enfraquecido — a correção
afeta apenas uma afirmação qualitativa sobre a forma da desigualdade,
não nenhum número catalogado.

**O que permanece aberto, com precisão:** a Lacuna 1 em si (um
`n_0(\gamma)` numericamente útil exigiria constantes mais afiadas ou
uma técnica de controle de cauda diferente [Ver Estágio 37 abaixo —
DATA: 2026-08-27, melhoria parcial via desigualdade de Bernstein]);
`C(\gamma)` para
`\gamma\in(0,1)`; a CDF completa de `M_n^{(3)}` (Estágio 35); a lei
conjunta de dois pontos para `K` geral; `p>80` de `D^{*(p)}_r(b)`
(Estágio 32); a construção contínua-nativa direta do Teorema J
(Estágio 28); o piso `H2` em `b=1`; a constante do platô de
DISC-DEC-071; `H1`/`H2` da lei assintótica do platô M-CLUST(b).
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.

---

## [Extensão, Estágio 37 — 2026-08-27]

**Onda 22, frente (c), `DISC-DEC-096`/`DISC-DEC-098`
(`GAMMA-GAP1-SHARPER-TAIL-ATTEMPT`).** Alvo: exatamente o item nomeado
como o mais difícil do relatório "Mapa da Fronteira" — encontrar uma
técnica de controle de cauda genuinamente mais afiada que Hoeffding
para a desigualdade do Lema Bulk/Tail (Estágio 33/36), visando tornar
`n_0(\gamma)` numericamente útil.

### O que aconteceu

> **Achado principal: melhoria parcial genuína, não fechamento.** A
> frente substitui a desigualdade de Hoeffding (cega à variância) por
> uma desigualdade de Bernstein (sensível à variância), derivada do
> zero e verificada de forma independente contra a cauda Binomial
> EXATA (`mpmath` dps=50, zero violações). Como o denominador de
> Bernstein não cancela a dependência em `k` da mesma forma limpa que
> Hoeffding, a frente constrói um dispositivo de "parâmetro de folga"
> `a>0` que recupera um limitante `k`-uniforme
> `2n^{-C^2/((2+a)\sigma^2)}` para `k\ge k_2(n,\gamma,C,a)=O(\ln n)`.
>
> **Achado-bandeira (álgebra exata, não amostragem numérica):**
> `C0_{\mathrm{Bernstein}}(\gamma,a)^2:=(2+a)\sigma^2(\gamma)
> (\hat\lambda(\gamma)+1/2)` é PROVADO estritamente decrescente e
> LIMITADO em todo o intervalo aberto `(0,1)`, para todo `a>0` fixo —
> ao contrário de `\hat\lambda(\gamma)`/`\lambda(\gamma)` isolado
> (a quantidade da rota Hoeffding, provada NÃO LIMITADA conforme
> `\gamma\to0^+` no Estágio 36) — com
> `\sup_{\gamma\in(0,1)}C0_{\mathrm{Bernstein}}^2=\lim_{\gamma\to0^+}
> =28a+56`, uma forma fechada finita para todo `a>0`. O mecanismo não é
> coincidência: `\hat\lambda(\gamma)\sim28/\gamma` diverge, mas a
> variância verdadeira `\sigma^2(\gamma)=\gamma(1-\gamma)\sim\gamma`
> encolhe exatamente na taxa recíproca, então o produto
> `\sigma^2(\gamma)\hat\lambda(\gamma)\to28` permanece finito. **Um
> único `C` `\gamma`-independente agora basta para todo o intervalo
> aberto `(0,1)` simultaneamente** — não apenas em compactos
> `[\gamma_0,1)` como sob Hoeffding — um bônus genuíno além do pedido
> literal (que era sobre `n_0(\gamma)`, não uniformidade).
>
> **Resultado numérico líquido:** redução genuína em `n_0(\gamma)` em
> 7 dos 8 pontos `\gamma` testados (os mesmos 8 do Estágio 36),
> variando de `0.44`–`3.19` décadas em `\gamma` moderado até **`9.09`
> décadas (fator `\sim10^9`) em `\gamma=0.01`**, crescendo
> sistematicamente conforme `\gamma\to0` ou `\gamma\to1` — exatamente
> onde a construção de Hoeffding era mais fraca. Em `\gamma=0.5`,
> perda negligível de `0.07` décadas (compreendida, estrutural:
> `\sigma^2(1/2)=1/4` é exatamente o pior caso que Hoeffding já
> assume para todo `\gamma`, então uma desigualdade sensível à
> variância não pode superá-la ali). `n_0(\gamma)` permanece
> **astronomicamente grande** (`10^{18}`–`10^{76}` nos pontos
> testados) — a frente não alega o contrário.

**O que isto NÃO fecha.** A Lacuna 1 permanece ABERTA; `C(\gamma)`
para `\gamma\in(0,1)` permanece inteiramente ABERTO. Os limitantes de
coeficiente `|c_i(k)|` e a montagem `\hat G`/`\hat G_\Theta` continuam
INALTERADOS do predecessor — a mesma folga de desigualdade triangular
permanece. O ângulo 2 do mandato (rastreamento de cancelamento exato
nos próprios limitantes de coeficiente) e o ângulo 3 (uma decomposição
fundamentalmente diferente) não foram tentados. O limite ideal
`a\to0^+` (`C0_{\mathrm{Bernstein}}^2\to2\sigma^2(\gamma)
(\hat\lambda(\gamma)+1/2)`, ainda estritamente melhor que Hoeffding
para todo `\gamma\ne1/2`, igual exatamente em `\gamma=1/2`) não foi
perseguido — a frente usou `a=0.05` fixo.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: re-derivação
simbólica independente (`sympy`) de
`C0_{\mathrm{Bernstein}}(\gamma,a)^2` a partir das definições do
predecessor (`\sigma^2(\gamma)=\gamma(1-\gamma)`,
`\beta(\gamma)=\gamma(2-\gamma)/2`,
`\hat\lambda(\gamma):=16(7/4-\gamma)/\beta(\gamma)`), confirmando
independentemente: monotonicidade estritamente decrescente em `(0,1)`
para múltiplos valores de `a` testados (derivada sempre `\le0`, sem
raiz real do numerador em `(0,1)`); limite `28a+56` conforme
`\gamma\to0^+`; limite `0` conforme `\gamma\to1^-`. Verificação
independente adicional de Bernstein contra a cauda Binomial exata
(`mpmath` dps=50, 60 checagens, zero violações) antes de despachar o
referee.

Referee hostil dedicado (`.../gamma_gap1_sharper_tail_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script de nenhuma
frente da linhagem: re-derivou Bernstein do zero e verificou contra a
cauda Binomial exata (352 checagens, zero violações); re-derivou a
construção de parâmetro de folga e `k_2(n,\gamma,C,a)` (à mão e via
`sympy.solve`, correspondência exata); confirmou o achado-bandeira com
uma prova estrutural MAIS FORTE que a da própria frente (mostrando que
o sinal da derivada de `C0_{\mathrm{Bernstein}}^2` é idêntico ao sinal
de `f'(\gamma)` para TODO `a>0` simultaneamente, não apenas em `a`
amostrados) — e provou, como achado extra, uma alegação que a frente
declarou mas não provou (`C0_{\mathrm{Hoeffding}}^2-
C0_{\mathrm{Bernstein}}(\gamma,0^+)^2=(\gamma-1/2)^2(2\hat\lambda(
\gamma)+1)\ge0`, com igualdade sse `\gamma=1/2`); reconstruiu
inteiramente da prosa a montagem completa de `n_0(\gamma)` e reproduziu
a tabela publicada da frente nos 8 pontos `\gamma` (não apenas 2-3), a
`\le0.005`–`0.03` décadas — incluindo um auto-diagnóstico transparente
de um artefato na própria reconstrução do referee (não um erro da
frente) no termo residual de `k` pequeno em `\gamma=0.99`, corrigido e
documentado.

> **Dois achados nomeados, ambos severidade BAIXA.** (1) Um artefato de
> modelagem do próprio processo de reconstrução do referee (não um erro
> da frente) — documentado no relatório do referee, sem necessidade de
> correção na `ATTEMPT.md` da frente. (2) Uma frase em §5 descrevendo os
> ganhos em `\gamma=0.7`/`0.3` como redigida de forma confusa
> ("simétrico por construção" e "não simétrico" na mesma oração) —
> conteúdo numérico correto, apenas clareza de redação. Corrigido por
> nota datada (não correção) na `ATTEMPT.md` da frente.

> **Veredito: SOUND — ACCEPT for catalogue.** Nenhum erro matemático,
> algébrico ou lógico encontrado. O achado-bandeira foi confirmado sem
> qualificação, e fortalecido pela prova estrutural do referee.

Ver
`.../gamma_gap1_continuation_attempt/gamma_gap1_sharper_tail_attempt/ATTEMPT.md`
e
`.../gamma_gap1_sharper_tail_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

Nenhuma fórmula de registro é substituída. `C(\gamma)` para
`\gamma\in(0,1)` permanece inteiramente ABERTO — este Estágio não
fecha a Lacuna 1, apenas demonstra que sua constante-líder pode ser
melhorada substancialmente (até `\sim10^9\times` em `\gamma\to0`) por
uma técnica de cauda mais afiada, e que a uniformidade em todo
`(0,1)` (não apenas compactos) é alcançável por essa mesma rota — um
resultado estrutural genuíno, mesmo sem fechar `C(\gamma)`.

**O que permanece aberto, com precisão:** `C(\gamma)` para
`\gamma\in(0,1)`; um `n_0(\gamma)` numericamente útil (ainda
`10^{18}`–`10^{76}`, mesmo após esta melhoria); o ângulo 2
(rastreamento de cancelamento exato nos limitantes de coeficiente) e o
ângulo 3 (decomposição fundamentalmente diferente) do mandato original,
nenhum tentado; o limite ideal `a\to0^+` não perseguido; a cota de
Chernoff/entropia relativa exata (mais afiada que Bernstein, mas sem
forma algébrica fechada simples) considerada mas não perseguida. Todos
os demais itens em aberto listados no Estágio 36 permanecem
inalterados por este Estágio. Nenhuma alegação de progresso em
Millennium Problem; matemática combinatória pura interna a este
arquivo.


## [Extensão, Estágio 38 — 2026-08-28]

**Onda 21, frente (c), `DISC-DEC-093`/`DISC-DEC-106`
(`GENERAL-K-JOINT-ATTEMPT`, v2).** Alvo: generalizar de `K=3` para `K`
geral o método de caso-split (Reindexação por Fonte-Governante +
Lema 4 do Estágio 35) que fechou `P_{nn}(n,3)`, e determinar até onde a
generalização é prova genuína versus padrão numericamente verificado.
Redespachada do zero após a frente v1 ter estagnado por tempo
indeterminado sem retorno verificável (`DISC-DEC-106`); a v2 reaproveita
o `ATTEMPT.md` já existente e já lido/spot-checado pela sessão
antes da compactação de contexto, despachando apenas um novo referee
hostil sobre ele.

### O que aconteceu

> **Achado principal: fechamento parcial genuíno, com não-fechamento
> precisamente diagnosticado — não uma extrapolação de padrão.**
> Mecanismo 1 (Reindexação por Fonte-Governante) e Mecanismo 2
> (Lema 4, Unicidade do Predecessor de Ciclo) são PROVADOS para `K`
> geral — literalmente a mesma prova de `K=3` com `3` substituído por
> `K`, sem uso do valor específico `3` em nenhum passo lógico
> (exchangeability de `K` variáveis aleatórias simétricas sob
> relabeling, para o Mecanismo 1; um fato padrão sobre grafos
> funcionais em qualquer conjunto finito de nós mais um estado
> absorvente, para o Mecanismo 2). Um novo **Lema 5 análogo para `K`
> geral** é PROVADO — fórmulas fechadas de ponto único/arco-cruzado
> `P_0(s)`, `P_{\mathrm{same}}`, `P_{\mathrm{disjoint}}`, derivadas por
> soma-ciclo/inclusão simbólica completa em `K`. O algoritmo de
> montagem (soma sobre composições de `n-K` em `K+1` partes) é PROVADO
> **correto como algoritmo** para `K` geral (self-consistency-checado
> contra `K=1,2,3` já provados nos Estágios 27/28/35).
>
> **Proposições NN4, NN5, NN6 (novas formas fechadas concretas,
> PROVADAS):**
> `P_{nn}(n,4)=(126n^4+187n^3+177n^2+98n+24)/(630n^4)`, mais NN5 e NN6
> analogamente — todas derivadas por soma simbólica completa em `K`
> (não conjecturadas-e-checadas), cross-checadas por brute force
> verdadeiro até 165M (NN4) e 84,7M (NN5) configurações exaustivas.
>
> **Não-fechamento diagnosticado com precisão (§8), não um fracasso de
> método:** uma única fórmula fechada-em-`K` para `P_{nn}(n,K)`
> permanece ABERTA — a causa identificada é crescimento do número de
> termos na soma simbólica com `K`, não uma barreira estrutural do
> método (que continua válido, apenas cada `K` concreto exige nova
> execução simbólica). Coeficiente de taxa `c_1(K)` reportado como
> dados brutos (§8.3), sem alegação de padrão — a frente cita
> explicitamente seu próprio quase-erro anterior de ajuste de padrão
> prematuro como a razão da cautela aqui. `K\ge7` não tentado, com
> razão concreta declarada (orçamento computacional, não parede
> matemática).

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: brute force
independente do zero
(`/tmp/.../spotcheck_pnn_k4.py`), confirmando `P_{nn}(n=6,K=4)=209/810`
exatamente, coincidindo com a Proposição NN4.

Referee hostil dedicado (`.../general_k_joint_attempt/adversarial/`
`REFEREE_REPORT.md`), sem ler nenhum script deste front ou de qualquer
front irmão/ancestral desta linhagem antes de escrever e rodar seus
próprios: quatro rotas de verificação largamente independentes,
construídas inteiramente do zero a partir apenas da prosa de
`ATTEMPT.md` e das Definições/Estágios anteriores citados —

1. **Brute force verdadeiro** do modelo literal da Definição 4,
   `K=1,\ldots,5`, incluindo os dois maiores casos desta linhagem em
   `K\ge4`: `K=4,n=8` (165.150.720 configurações exatas, confirma
   `P_{nn}(8,4)=25999/107520`) e `K=5,n=7` (84.707.280 configurações
   exatas, confirma `P_{nn}(7,5)=78077/352947`). Zero divergências.
2. **Checagem de fórmula ao nível de nó** do Mecanismo 3, reimplementada
   do zero a partir da prosa apenas, alcançando `K=1,\ldots,7` — um
   valor de `K` além do que a própria frente testou a nível de nó
   (que para em `K=6`). Zero divergências.
3. **Checagem ao nível de posição** da alegação "landing-uniform"
   (§4.1), `K=1,\ldots,4`, contra travessia direta do grafo funcional
   completo. Zero divergências.
4. **Montagem `K`-fold independente**, alcançando `K=6` (onde brute
   force verdadeiro é astronomicamente inviável para ambas as partes) —
   confirmando as Proposições NN1–NN6 a `K+5` ou mais pontos
   independentes por `K` (um polinômio de grau `K` não pode concordar
   com um genuinamente diferente em mais de `K` pontos). **Primeira
   confirmação independente conhecida da Proposição NN6 por qualquer
   rota que não a da própria frente.** Zero divergências.
5. **Corolário do Teorema J** (`P(\mathrm{mesmo\ ciclo}\mid\mathrm{ambos\
   cíclicos})=1/2` exatamente) reconfirmado em dados brutos frescos,
   `K=1,\ldots,4`. Zero divergências.

> **Um achado, severidade BAIXA, precisão de citação apenas.** A
> tabela de self-consistency §5.2 cita a fórmula base `K=1`
> `P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` como "(Estágio 27)" — mas o
> Estágio 27 apenas *enuncia* esta fórmula como padrão
> numericamente-verificado (`n=3,\ldots,9`), explicitamente rotulado lá
> como não-provado para `n` geral; a prova real (uma derivação
> case-split completa) aparece um estágio depois, no Estágio 28, como
> `V_a(n)` — algebricamente idêntico a `\tfrac12+\tfrac1{6n}`. O valor
> em si está correto (reconfirmado pelo próprio brute force do referee
> em `n=3,4,5`) e de fato é provado em algum lugar do arquivo, apenas
> não no local citado. Nenhum outro achado — todas as demais citações,
> fórmulas e alegações verificadas conferem exatamente.

> **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue, no tier
> alegado.** Nenhum erro matemático encontrado. Toda proposição,
> corolário e mecanismo alegado PROVADO foi re-derivado e confirmado
> exatamente por rota independente; todo item alegado ABERTO ou NÃO
> TENTADO é, na inspeção, genuinamente aberto/não tentado — sem
> overclaiming, sem alegação de progresso em Millennium Problem.

Ver
`.../k3_joint_structural_attempt/general_k_joint_attempt/ATTEMPT.md`
e
`.../general_k_joint_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

Nenhuma fórmula de registro anterior é substituída. As Proposições
NN4, NN5, NN6 entram no catálogo como novas fórmulas fechadas
provadas, generalizando o fechamento `K=3` do Estágio 35 para
`K=4,5,6`. O método (Mecanismos 1+2+Lema-5-análogo+montagem) é agora
estabelecido como genuinamente `K`-livre em sua lógica de prova — não
apenas verificado ponto a ponto — o que abre caminho para qualquer `K`
concreto futuro ser fechado por execução do mesmo método, sem
necessidade de reprovar a estrutura geral.

**O que permanece aberto, com precisão:** uma fórmula fechada única
válida para `K` geral (não apenas o algoritmo, que já é geral); um
padrão ou fórmula fechada para o coeficiente de taxa `c_1(K)` (seis
pontos apenas, nenhum padrão evidente por inspeção, tentativa
deliberadamente não feita); `K\ge7` (nenhum polinômio fechado alegado
para nenhum `K\ge7`, apenas o método suportado por checagem
independente ao nível de nó do próprio referee). Correção de citação
de precisão (Estágio 27 → Estágio 28 para a fórmula base `K=1`)
aplicada como nota datada no `ATTEMPT.md` da frente, ver abaixo.
Nenhuma alegação de progresso em Millennium Problem; matemática
combinatória pura interna a este arquivo.


## [Extensão, Estágio 39 — 2026-08-28]

**Onda 22, frente (a), `DISC-DEC-096`/`DISC-DEC-099`
(`PNN-GENERAL-K-EGF-ATTEMPT`).** Alvo: sucessora direta do Estágio 38
(`GENERAL-K-JOINT-ATTEMPT`) — usar a representação
integral/função-geratriz-exponencial para (1) colapsar o integral
duplo de `P_{\mathrm{disjoint}}(s,s')` sinalizado como "a questão
aberta mais concreta" pelo predecessor, (2) empurrar essa mesma ideia
através da soma de composição completa em busca de uma fórmula
fechada única válida para `K` simbólico. Integração ao `THEOREM.md`
estava explicitamente ADIADA desde `DISC-DEC-099` (revisão adversarial
já concluída naquela decisão) até o Estágio 38 ser integrado primeiro,
por ordem de dependência — agora desbloqueada.

### O que aconteceu

> **Achado principal: fechamento completo do item 1 do mandato, mais
> um algoritmo geral-`K` genuinamente mais rápido, mais uma
> obstrução nova e mais precisamente localizada e certificada por
> prova negativa rigorosa — não um fracasso vago de `sympy`.**
>
> **Item 1 (PROVADO, completo):** o integral duplo de
> `P_{\mathrm{disjoint}}(s,s')` colapsa para um **único** integral —
> mais um achado-bônus: `P_{\mathrm{same}}(s,s')` e
> `P_{\mathrm{disjoint}}(s,s')` são IDÊNTICOS como funções algébricas
> de `x_M` (identidade combinatória elementar, prova por contagem
> direta de pares ordenados `(S_1,S_2)` por tamanho do conjunto ativo
> `S=S_1\cup S_2`). Consequência:
> `P_{s,s'}=2x_sx_{s'}\int_0^\infty s\,e^{-s}\prod_{u\in M}(1+x_us)\,ds`
> — um único integral, não a transformada genuinamente bivariada que o
> mandato antecipava poder ser necessária.
>
> **Item 2 (PROVADO, para cada `K` concreto):** a soma de composição
> externa também colapsa via identidade de função-geratriz ordinária,
> `\mu_r(n,K)=\binom{n+r}{K+r}` exatamente, produzindo um algoritmo
> geral-`K` muito mais rápido — reproduz `K=1,\ldots,6` em `\sim1$s`
> (contra `\sim166$s` do predecessor via soma simbólica aninhada) e
> estende a dois resultados genuinamente novos, **`K=7` e `K=8`**,
> cada um reconfirmado independentemente por dois caminhos distintos
> (enumeração direta lenta e simulação Monte Carlo).
>
> **Item 3 (obstrução nova, CERTIFICADA rigorosamente, não apenas
> observada):** o empurrão simbólico-em-`K` foi tentado concretamente
> — cada tipo de momento que `T(L)` precisa foi re-derivado como
> expressão fechada explícita em `(n,K,r)` simultaneamente. O
> obstáculo remanescente é uma única soma finita sobre `r` de `0` a
> `K-1`, com `K` em si o limite superior simbólico. O algoritmo de
> Gosper — o procedimento de decisão real para se um termo
> hipergeométrico tem antidiferença de termo hipergeométrico, não uma
> heurística — retorna `None` nos três tipos de somando distintos, um
> certificado formal de que nenhuma forma fechada elementar existe no
> sentido de razão-de-função-Gama. A soma É expressável, trivialmente,
> como uma função hipergeométrica terminante `\,_3F_1(1-K,n+2,1;K+4;
> -1/n)` (verificada numericamente, correspondência exata) — uma
> "forma fechada envolvendo função especial" legítima, exatamente como
> o mandato antecipava como possível resultado — mas
> `sympy.hyperexpand` não a reduz a nada elementar para `(n,K)`
> simbólicos. Esta é uma obstrução nova, um nível acima da do
> predecessor (que vivia na contagem de termos da soma de subconjunto)
> — aqui vive no próprio passo de soma-em-`r` de um pipeline
> geral-`K`-uniforme e muito mais rápido.
>
> **Bônus (§4):** `c_1(K)` computado em `K=7,8`, estendendo a tabela
> do predecessor, dados brutos apenas, nenhum padrão proposto:
> `c_1(7)=4387/12870\approx0{,}34087`, `c_1(8)=76627/218790\approx
> 0{,}35023`.

**O que isto NÃO fecha.** Nenhuma fórmula elementar única
`P_{nn}(n,K)=F(n,K)` para `K` simbólico — não meramente "não
encontrada", mas certificada não existir na classe elementar/
Gosper-somável para os blocos naturais construídos por esta frente,
no ponto preciso onde a obstrução agora vive (a soma-em-`r` da
maquinaria de soma de composição, de outro modo totalmente uniforme
em `K` e rápida). Nenhuma alegação sobre o padrão de `c_1(K)` em `K`.
Nenhuma alegação sobre `K\ge9`. Nenhuma alegação sobre a CDF completa
de `M_n^{(K)}`, `K\ge2` (pré-existente, intocada por esta frente).

### Verificação adversarial independente

Já concluída e registrada em `DISC-DEC-099` (2026-08-27), antes deste
Estágio — resumo para o registro: **spot-check da sessão** antes do
despacho do referee, verificando independentemente as duas alegações
mais surpreendentes (`P_{\mathrm{same}}\equiv P_{\mathrm{disjoint}}`
via `sympy` do zero; `\mu_r(n,K)=\binom{n+r}{K+r}` via enumeração
direta de composições) — ambas conferem exatamente.

Referee hostil dedicado (`.../pnn_general_k_egf_attempt/adversarial/`
`REFEREE_REPORT.md`), com foco extra no certificado de Gosper por ser
o achado mais consequente, sem ler nenhum script desta frente ou de
qualquer front ancestral/irmão desta linhagem: confirmou `K=7`/`K=8`
via segunda rota de código independente (5/5 correspondências
exatas); re-derivou a decomposição Peça A/B/C/D do zero; re-derivou a
fórmula de momento simbólica em `(n,K,r)` por rota estruturalmente
diferente (função-geratriz-ordinária via polinômios de Euler); rodou
o próprio `gosper_sum`/`gosper_term` (não apenas confiou no relato da
frente) com `K` simbólico E em 13 valores de `K` concretos
(`K=3,\ldots,15`), todos `None`; rodou controles positivos
confirmando que o próprio harness detecta somabilidade quando
presente; leu o código-fonte do `sympy` para confirmar que `None`
aqui é um certificado genuíno de não-existência, não um timeout ou
heurística.

> **Dois achados nomeados, ambos severidade BAIXA, ambos cosméticos.**
> (1) A etiqueta `\,_3F_2` usada em todo o documento está incorreta —
> a lista de parâmetros de fato usada (3 superiores, 1 inferior) é
> uma `\,_3F_1` por contagem direta e pela própria classificação de
> objeto do `sympy`. (2) Um erro de arredondamento de um dígito na
> coluna "ratio to `K-1`" para `K=7` (`1{,}035` impresso, valor exato
> arredonda para `1{,}034`). Nenhum dos dois afeta o valor de nenhuma
> fórmula, o certificado de Gosper, ou o veredito de não-fechamento.
> Ambos corrigidos por adendo datado na `ATTEMPT.md` da frente
> (2026-08-27, sob `DISC-DEC-099`).

> **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue.** Toda
> alegação matemática re-verificada de forma independente confere
> exatamente, incluindo a alegação mais nova e mais consequente da
> frente (o certificado de não-fechamento via Gosper).

Ver
`.../general_k_joint_attempt/pnn_general_k_egf_attempt/ATTEMPT.md`
e
`.../pnn_general_k_egf_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

Nenhuma fórmula de registro anterior é substituída. O integral duplo
de `P_{\mathrm{disjoint}}(s,s')`, sinalizado como a questão aberta
mais concreta ao final do Estágio 38, fecha completamente (item 1,
com o bônus `P_{\mathrm{same}}\equiv P_{\mathrm{disjoint}}`). A
soma de composição colapsa para um algoritmo geral-`K` muito mais
rápido (item 2), produzindo `P_{nn}(n,7)` e `P_{nn}(n,8)` como novos
resultados concretos, ambos verificados independentemente por dois
caminhos. A obstrução restante para uma fórmula fechada única em `K`
(deixada aberta pelo Estágio 38) é agora precisamente relocalizada —
não mais na contagem de termos da soma de subconjunto (já resolvida
por esta frente), mas na própria soma finita sobre `r` de tamanho
`K`, com não-existência de forma fechada elementar CERTIFICADA por
Gosper, não apenas observada.

**O que permanece aberto, com precisão:** uma fórmula fechada
elementar única `P_{nn}(n,K)=F(n,K)` para `K` simbólico — certificada
não existir na classe Gosper-somável para a construção natural desta
frente, mas sem alegação de impossibilidade absoluta (uma
reorganização diferente da mesma combinatória poderia, em princípio,
evitar esta soma-em-`r` específica; nenhuma foi encontrada aqui, nem
alegada como descartada); um padrão ou fórmula fechada para `c_1(K)`;
`K\ge9`; a CDF completa de `M_n^{(K)}`, `K\ge2` (pré-existente,
inalterada por este Estágio). Nenhuma alegação de progresso em
Millennium Problem; matemática combinatória pura interna a este
arquivo.


## [Extensão, Estágio 40 — 2026-08-28]

**Onda 21, frente (b), `DISC-DEC-093`/`DISC-DEC-106`
(`K3-FULL-CDF-ATTEMPT`, v2).** Alvo: estender o fechamento do segundo
momento de `M_n^{(3)}` (Estágio 35, Proposição NN3) para a CDF
completa `P(M_n^{(3)}\le k/n)` em forma fechada, no estilo de
Proposição D1 (Estágio 27, `K=1`). Redespachada do zero após a
frente v1 ter estagnado sem retorno verificável (`DISC-DEC-106`); a
v2 é uma tentativa nova, não uma continuação — a tentativa abandonada
original foi preservada (não deletada) para auditoria.

### O que aconteceu

> **Achado principal: fechamento completo do mandato, excedendo a
> ambição original.** Um novo **Teorema de Decomposição Completa da
> Contagem de Ciclos** (PROVADO) fortalece o Lema 4/5 do Estágio 35 de
> uma afirmação par-a-par para a **lei conjunta completa** da contagem
> `T:=\#\{\text{pontos cíclicos de }f\}` (`M_n^{(3)}=T/n`):
> `T=O+\sum_{s\in S}V_s`, onde `S\subseteq\{0,1,2\}` é o conjunto
> aleatório de fontes cíclicas e, dado `S`, os `V_s` são
> **mutuamente independentes**, `V_s\sim\mathrm{Uniforme}\{1,\ldots,
> L_s\}`. A lei de `S` é dada por quatro fórmulas fechadas novas
> (Proposição S). Disto segue uma CDF condicional fechada dada
> `(L_0,L_1,L_2)`, e — o resultado principal — **Proposição D3**: para
> todo `n\ge3` e todo inteiro `0\le k\le n-1`,
> `P(M_n^{(3)}\le k/n)=k(k+1)[k^4-4k^3-(3n^2-9n-5)k^2+(3n^2-11n-2)k+
> (3n^4-12n^3+12n^2+2n)]/[n^4(n-1)(n-2)]` — uma única fórmula fechada,
> uniforme em `n`, exatamente na ambição de Proposição D1. Provada por
> derivação simbólica completa, sem lacunas, em três regimes
> combinatórios distintos (`0\le k\le n-3`; `k=n-2`; `k=n-1`), cada um
> derivado e verificado independentemente por `sp.summation`.
>
> **Corolários (todos PROVADOS):** `P(M_n^{(3)}=1)=6/n^3`
> (prova direta elementar); recuperação simbólica exata, com **zero
> resto simbólico**, da já-provada média finita-`n` `\varphi_n^{(3)}`
> (Estágio 4); limites de segundo/terceiro momento coincidindo com os
> já-provados valores contínuos `1/4` e `16/105` (Estágio 17/18); um
> limitante de convergência uniforme `O(1/n)`.

**O que isto NÃO fecha.** A CDF completa geral-`K` (`K\ge4`) não foi
tentada por esta frente (fora do escopo do mandato) — permanece
aberta; o método (destinos governantes i.i.d., dicotomia
cíclico/não-cíclico) parece estruturalmente generalizável, mas isto é
uma pista não verificada, não uma alegação. A constante do limitante
de taxa de Corolário D3.5 não é otimizada (`22/n`, com termo
assintótico líder `\approx0{,}712/n` honestamente relatado como não
provado como limitante uniforme).

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: brute force
independente do zero (modelo Definição 4 literal, contagem exata via
`Fraction`), confirmando Proposição D3 exatamente em `n=3,4,5`, todo
`k` — correspondência exata em todos os casos.

Referee hostil dedicado (`.../k3_full_cdf_attempt/adversarial/`
`REFEREE_REPORT.md`), sem ler nenhum script deste front ou de
qualquer front da linhagem: brute force verdadeiro estendido até
`n=9` (superando até o próprio alcance testado pela frente); soma
simbólica independente sobre os `4^3=64` casos brutos confirmando as
quatro fórmulas de Proposição S; montagem de modelo reduzido
independente confirmando o Teorema de Decomposição e a CDF
condicional; re-soma simbólica independente confirmando a recuperação
de média com zero resto; verificação estrutural do particionamento
dos três regimes (sem lacunas nem sobreposições) e dos valores de
fronteira; auditoria completa da cadeia de desigualdades do
Corolário D3.5.

> **Dois achados nomeados.** (1) **BAIXA, informacional:** a fórmula
> da média do Estágio 4 é enunciada em `THEOREM.md` apenas para
> `n\ge4`; o referee constatou que ela (e a Proposição D3) também vale
> exatamente em `n=3` — não é um erro. (2) **MODERADO, sinalizado por
> metadados apenas (sem leitura de conteúdo, por mandato):** o
> diretório da tentativa abandonada continha arquivos cujos nomes
> (`symbolic_D3_derivation.py`, `P_D3_closed_form.txt`) pareciam
> potencialmente contradizer a alegação da §10 de que "nenhuma CDF em
> forma fechada" estava presente ali — sinalizado para a sessão
> orquestradora resolver com acesso de leitura irrestrito.

**Resolução do achado #2 pela sessão orquestradora:** os arquivos
sinalizados contêm **fórmulas de ponto único** `P(T=n{-}2)` e
`P(T=n{-}3)` (não uma CDF em função de `k`, não o estilo Proposição
D1) — confirmando que a §10 original está correta. Verificação
adicional contra brute force fresco (`n=6,7,8`) mostrou que a fórmula
`P(D=2)` da tentativa abandonada está correta, mas a fórmula `P(D=3)`
está **errada** (`19n^2{-}105n{+}160` impresso vs. o valor correto
`19n^2{-}108n{+}160`) — consistente com a tentativa anterior ter sido
corretamente abandonada em meio ao trabalho, não silenciosamente
completa. Nota datada registrada em `k3_full_cdf_attempt/ATTEMPT.md`
§10.

> **Veredito: SOUND WITH NAMED ISSUES — ACCEPT for catalogue.** Nenhum
> erro matemático encontrado em nenhuma parte do documento.

Ver
`.../k3_joint_structural_attempt/k3_full_cdf_attempt/ATTEMPT.md`
e
`.../k3_full_cdf_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

Nenhuma fórmula de registro anterior é substituída. `M_n^{(3)}`'s CDF
completa entra no catálogo como resultado fechado e provado — a
primeira CDF completa fechada nesta linhagem além de `K=0,1`
(Estágio 27). O Teorema de Decomposição Completa da Contagem de
Ciclos é um resultado estrutural novo e genuinamente mais forte que o
Lema 4/5 do Estágio 35 (lei conjunta completa, não apenas par-a-par).

**O que permanece aberto, com precisão:** a CDF completa geral-`K`
(`K\ge4`) — não tentada por esta frente; uma constante mais afiada
para o limitante de convergência uniforme de Corolário D3.5 (o termo
assintótico líder `\approx0{,}712/n` é conhecido mas não provado como
limitante uniforme finito-`n`); todos os demais itens abertos
catalogados nos Estágios 38/39 (a fórmula fechada única em `K` para o
segundo momento, certificada não existir na classe Gosper-somável, é
uma questão distinta desta CDF completa a `K=3` fixo). Nenhuma
alegação de progresso em Millennium Problem; matemática combinatória
pura interna a este arquivo.


## [Extensão, Estágio 41 — 2026-08-28]

**Onda 23, frente (b), `DISC-DEC-110`
(`GENERAL-K-DECOMPOSITION-ATTEMPT`).** Alvo: generalizar o Teorema de
Decomposição Completa da Contagem de Ciclos e a Proposição S do
Estágio 40 (`K=3`) para `K` geral — a pista explicitamente sinalizada
mas não verificada pelo próprio Estágio 40 ("parece estruturalmente
generalizável... mas isto é uma pista não verificada, não uma
alegação"). Diferente dos Estágios 38/39 (que generalizaram uma
quantidade mais fraca — o segundo momento par-a-par `P_nn(n,K)`), esta
frente ataca a lei conjunta *completa* de `T`.

### O que aconteceu

> **Achado principal: fechamento completo do mandato primário, com uma
> unificação genuína como bônus.** A **Proposição S, `K` geral**
> (PROVADA, nova) é uma única fórmula fechada, livre de `K` e livre de
> `|A|`, para a lei inteira de `S`:
> `P(S=A)=|A|!\cdot\prod_{a\in A}p_a\cdot(p_D+\sum_{a\in A}p_a)`, para
> todo `K\ge0` e todo `A\subseteq\{0,\ldots,K-1\}`. Esta única fórmula
> **reproduz exatamente as quatro fórmulas separadas do Estágio 40**
> como casos especiais `|A|=0,1,2,3` — o Estágio 40 nunca percebeu que
> eram uma única fórmula.
>
> **O cerne da prova:** um Lema-Chave novo — para qualquer conjunto
> finito `B` com pesos `p_b` e peso de escape combinado
> `q_B:=1-\sum_{b\in B}p_b`, a probabilidade de que NENHUM nó de `B`
> esteja em um ciclo é exatamente `q_B`, independentemente de como o
> peso de escape se distribui internamente entre os "sabores" de
> escape e independentemente de `|B|` — provado por indução forte em
> `|B|`, via uma identidade algébrica nova
> `(1-P_B)F(B)+G(B)=1`, ela mesma provada via representação de integral
> exponencial e integração por partes. Isto generaliza — e, aplicado a
> `B=\{0,1,2\}`, `A=\emptyset`, reproduz exatamente — o único fato que
> o próprio Estágio 40 provou apenas por "soma simbólica direta sobre
> os 64 casos" (suas próprias palavras), nunca por argumento de mão.
>
> **O Teorema de Decomposição Completa da Contagem de Ciclos, `K`
> geral** (PROVADO): `T=O+\sum_{s\in S}V_s`, `(V_s)_{s\in S}`
> mutuamente independentes dado `S`, `V_s\sim\mathrm{Uniforme}\{1,
> \ldots,L_s\}` — provado para todo `K`, literalmente pelo mesmo
> argumento de `K=3` com `3` substituído por `K`, apoiando-se
> inteiramente em fatos já provados para `K` geral (Lema 4 do
> Estágio 38; o fato "posição-de-aterrissagem-uniforme" de
> `general_k_joint_attempt` §4.1) — confirmando a pista do próprio
> mandato do Estágio 40.

**O que isto NÃO fecha.** Uma única fórmula fechada em `(n,K)` para a
CDF (o análogo geral-`K` da Proposição D3 do Estágio 40) não foi
tentada além de uma pequena demonstração de que a maquinaria
algorítmica funciona — correta e deliberadamente fora do escopo
primário do mandato, espelhando a experiência dos Estágios 38/39 de
que o método generalizar-se de forma limpa não implica que uma fórmula
fechada única em `K` seja fácil de extrair.

### Verificação adversarial independente

**Spot-check da sessão** antes de despachar o referee: verificação
simbólica independente em `K=4` (pesos livres `p_0,\ldots,p_3`,
`p_D=1-\sum p_i`), comparando a Proposição S contra uma enumeração
bruta da tabela de destinos `(K+1)^K` — correspondência exata para
todo subconjunto `A`.

Referee hostil dedicado (`.../general_k_decomposition_attempt/`
`adversarial/REFEREE_REPORT.md`), sem ler nenhum script desta frente
ou de qualquer front da linhagem: re-derivou a identidade algébrica
crucial `(1-P_B)F(B)+G(B)=1` de quatro formas independentes (soma de
subconjunto bruta até `|B|=8`; re-derivação independente da identidade
de log-derivada; duas rotas independentes para o passo de integração
por partes; verificação com pesos racionais aleatórios, incluindo
negativos/`>1`, até `|B|=12`, confirmando ser uma identidade
polinomial pura); percorreu a lógica da indução linha por linha;
testou a forma mais forte do Lema-Chave (independência de múltiplos
"sabores" de escape distinguíveis — algo que os próprios testes do
documento nunca exercitam diretamente) com um modelo bruto
multi-sabor genuinamente diferente, incluindo um controle negativo
deliberado (não-normalizado) que corretamente falhou primeiro; rodou
enumeração simbólica bruta `(K+1)^K` em `K=0,\ldots,5` mais valores
racionais concretos em `K=6,7`; construiu um brute force verdadeiro de
Definição 4 totalmente independente (reconstrução própria de arcos a
partir da estrutura de ciclos de `\pi`) em 11 células `(n,K)` até
`(7,3)` — uma célula além do próprio alcance da frente; verificou a
liberdade-em-`K` do Teorema de Decomposição, incluindo a independência
CONJUNTA completa (não apenas marginal) de `(V_s)`, via um modelo
posição-nível fresco em `K=4,5,6`; confirmou a recuperação exata das
quatro fórmulas do Estágio 40; verificou ambas as citações (Lema 4 do
Estágio 38; fato posição-uniforme de `general_k_joint_attempt` §4.1)
contra seus textos-fonte.

> **Veredito: SOUND — ACCEPT for catalogue.** Nenhum erro matemático
> encontrado em nenhuma parte do documento. Dois achados, ambos BAIXA
> severidade, puramente informacionais (nenhum defeito).

Ver
`.../general_k_joint_attempt/general_k_decomposition_attempt/ATTEMPT.md`
e
`.../general_k_decomposition_attempt/adversarial/REFEREE_REPORT.md`.

### O que isto muda, precisamente

Nenhuma fórmula de registro anterior é substituída. A Proposição S e o
Teorema de Decomposição Completa da Contagem de Ciclos entram no
catálogo como resultados PROVADOS para todo `K`, com provas livres de
`K` — não meramente verificados em muitos `K` concretos. Isto é
estritamente mais forte, no sentido específico que o mandato
perguntou, que os fechamentos geral-`K` do segundo momento dos
Estágios 38/39 (a lei conjunta inteira de `S` e `T`, não apenas um
escalar par-a-par). A Proposição S também revela, como bônus, que as
quatro fórmulas separadas do Estágio 40 eram sempre uma única fórmula.

**O que permanece aberto, com precisão:** uma fórmula fechada única em
`(n,K)` para a CDF não-condicional geral-`K` (o análogo geral do
Estágio 40 §4) — a CDF *condicional* dada `L` é fechada e correta para
qualquer `K` (demonstrado), mas somar isso sobre o simplex de
composição `K`-dimensional em forma algébrica fechada não foi
tentado; nenhum padrão ou fórmula fechada para coeficientes de
taxa/momento como função de `K`; nenhum exame do comportamento
`K\to\infty`. Nenhuma alegação de progresso em Millennium Problem;
matemática combinatória pura interna a este arquivo.
