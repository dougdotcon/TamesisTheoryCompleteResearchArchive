# THEOREM — the u12 limit law φ_∞(c): rigorous core and the n→∞ bridge

> **[Atualização 2026-08-22 — ver "Extensão, Estágio 3" ao final do
> documento]** O sumário original abaixo (fechado ao fim da Etapa 2)
> descreve o caso `K=2` como parte do Lema Aberto não-provado. Isso
> **não é mais exato**: o Estágio 3 (onda 5, `DISC-DEC-022`) prova o
> caso `K=2` incondicionalmente, verificado por referee adversarial
> independente sem nenhum erro encontrado. O texto abaixo é preservado
> intacto como registro histórico da Etapa 2; o estado atual e correto
> do documento está na seção de extensão ao final.

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
   only at `K=1` (§5.3).
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

**Veredito honesto atualizado do documento inteiro:** Teorema 1 +
corolários (Estágio 1); Lema 2 (Estágio 1); Proposição 3 (Estágio 2);
Proposição 4 = ponte exata K=0,1 (Estágio 2); **ponte exata K=2,
incluindo taxa completa (Estágio 3, novo) — agora PROVADA, não mais
listada como faltante**. Resta como PROPOSIÇÃO CONDICIONAL apenas a
ponte geral para `K≥3` (Lema Aberto, agora estritamente mais estreito
do que "K≥2"). Conjecturas 1–2 (§8) inalteradas. Fontes completas:
`../k2_open_lemma/ATTEMPT.md`, `../k2_open_lemma/adversarial/REFEREE_REPORT.md`.
