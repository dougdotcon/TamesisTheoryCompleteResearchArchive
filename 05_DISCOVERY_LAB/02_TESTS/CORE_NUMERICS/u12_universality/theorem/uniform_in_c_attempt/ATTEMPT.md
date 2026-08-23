# Uniformity in `c` of Teorema 3: the convergence `φ(n,c)→∫₀¹e^{-ct²}dt` is uniform on every compact `[0,C]` — and, in fact, globally on `[0,∞)` — with an exact first-order error profile `e(c)`, and a precisely-located relative breakdown at `c≍n`

> **Governance.** Wave 11, front (a), `UNIFORM-IN-C-TEOREMA-3-ATTEMPT`,
> authorized by `DISC-DEC-047` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Target: item **(iv)**
> of the "o que permanece aberto" list of `THEOREM.md` Estágio 6/7/8 — *"a
> versão localmente-uniforme-em-`c` do Teorema 3 (§9 item 4 original — nunca
> tocada por nada neste estágio, gap genuinamente independente)"* — together
> with the never-attempted question of what happens when `c` grows with `n`.
> Pure combinatorial/asymptotic mathematics: no external data, no holdout, no
> real-world claim, no governance edits. Every claim below is labeled
> **PROVED**, **PROVED-MODULO-[X]** (X named precisely), **NUMERICALLY
> VERIFIED**, **NUMERICALLY CHARACTERIZED**, **CONJECTURED**, or **OPEN**.

> **Executive summary (read first).**
>
> 1. **The target question is answered affirmatively, and unconditionally.**
>    For every fixed `C>0`, `sup_{c∈[0,C]}|φ(n,c)-φ_∞(c)| → 0` (**Teorema A**,
>    §3). The proof is short and rests on exactly two inputs: Teorema 3 itself
>    (pointwise, already unconditional since Estágio 6), and one new elementary
>    lemma proved here by a one-line coupling — the whole family `{φ(n,·)}_n`
>    is **equi-Lipschitz with constant 1** on `[0,∞)`, uniformly in `n`
>    (**Lema 3.1**). Pointwise + equicontinuous ⟹ locally uniform.
> 2. **It extends past compacts to the entire parameter range** (**Teorema C**,
>    §4): `sup_{c∈[0,∞)}|φ(n,c)-φ_∞(c)| → 0`. The extra input is a second new
>    elementary lemma — a *uniform-in-`n`* tail bound `φ(n,c) ≤ J/(n-J) +
>    e^{-qJ(J-1)/(2n)}` (**Lema 4.1**) proved directly on the orbit
>    exploration, which forces `sup_{c≥C_0}φ(n,c)→0` as `C_0→∞` uniformly in
>    `n`. Neither theorem needs the `F_r,G_r,H_r` machinery at all.
> 3. **The exact first-order error profile is identified in closed form.**
>    `n[φ(n,c)-φ_∞(c)] → e(c)` with
>    `e(c) = ½∫₀¹[1-(1+ct²+c²t⁴)e^{-ct²}]\,dt/t²`, equivalently
>    `e(c)=Σ_{j≥1}(-1)^{j+1}\frac{(j-1)^2}{2(2j-1)\,j!}c^j`, equivalently
>    `¼[c(I_0{-}I_1)+2I_0-2]-\frac{c^2}2I_2`. Two of its three ingredients are
>    already-proved archive facts (`c_K` of Estágio 7; the Wallis `φ_K`); the
>    third is an exact Binomial-vs-Poisson identity proved here. The
>    **coefficient-wise** version (each `c`-Taylor coefficient) is **PROVED**
>    unconditionally (§5.4); the **uniform** version needs one named
>    interchange-of-limits step (§5.6) and is **PROVED-MODULO** that
>    [ver adendo em §5.6 abaixo — este gap foi fechado em 2026-08-23,
>    Teorema E agora incondicional].
>    `e(c) = -c²/12 + c³/15 - …` near `0` and
>    `e(c) = \sqrt{πc}/8 - ½ + O(\sqrt c\,e^{-c})` at large `c` — so the
>    uniform-on-`[0,C]` error constant **grows exactly like `√C`**, answering
>    the brief's "quantify how the bound grows as `C→∞`".
>
>    > **[Correção pós-adversarial, 2026-08-23, F-3/F-4 de
>    > `adversarial/REFEREE_REPORT.md` §8.3/§8.4.]** Duas imprecisões neste
>    > item. **(F-3)** "the uniform version needs..." dá a entender que
>    > apenas a versão *uniforme* de Teorema E é condicional e a versão
>    > *pontual* (`n\,Δ_n(c)\to e(c)` para `c` fixo) já é incondicional. Não
>    > é — Teorema E (§5.6) enuncia AMBAS as afirmações («For every `c\ge0`,
>    > `n\,Δ_n(c)\to e(c)`, **and** `n\sup_{[0,C]}|Δ_n|\to\sup_{[0,C]}|e|`»)
>    > sob o mesmo rótulo PROVED-MODULO — a versão pontual também precisa do
>    > passo de troca de limites de §5.6, já que a soma em `K` cresce com
>    > `n`. Apenas a versão coeficiente-a-coeficiente (Teorema D) é
>    > incondicional. **(F-4)** "grows exactly like `√C`" é uma afirmação
>    > sobre `\sup_{[0,C]}|e|` sozinho (PROVADA, dada a Proposição 5.2) —
>    > mas chamá-la de "*o* error constant" pressupõe que
>    > `\lim n\sup_{[0,C]}|Δ_n|=\sup_{[0,C]}|e|`, que é exatamente Teorema
>    > E, condicional. A linha do Scorecard (item 13) já registra essa
>    > distinção corretamente; este item do sumário executivo não.
> 4. **An explicit bound** `sup_{[0,C]}|Δ_n| ≤ (a\sqrt C+κ_B)/n`, `κ_B =
>    0.2804801690…` computed exactly here, follows from one clean hypothesis
>    (**U'**) `|φ_n^{(K)}-φ_K| ≤ a\sqrt K/n` uniformly in `K≤n` (§6). (U') is
>    **NUMERICALLY VERIFIED** over a wide range with the sharp constant
>    identified as `a^* = \sqrt π(1/\sqrt2-1/2)=0.3670872…`, but is **not
>    proved**: Estágio 6/7 give the `1/n` coefficient `c_K` for each *fixed*
>    `K` with **no uniformity in `K`**, and that is precisely and only what is
>    missing for an explicit rate. This is named as the single remaining
>    obstruction.
> 5. **The `c` growing with `n` question is answered sharply, and the answer
>    is a genuine partial breakdown.** In **absolute** terms nothing breaks —
>    even the global sup tends to `0`, at rate `Θ(n^{-1/2})`
>    **[Correção pós-adversarial, 2026-08-23, F-2: leia-se "at rate
>    `Θ(n^{-1/2})` (numerically characterized)" — a metade `Ω(n^{-1/2})` é
>    essencialmente provada (`sup_{c\ge0}|Δ_n|\ge φ(n,n)=Q(n)/n`, Proposição
>    7.1 mais a assíntota citada de `Q`), mas a metade `O(n^{-1/2})` precisa
>    de `\sup_{[0,n]}|Δ_n|=O(n^{-1/2})`, que só segue de Teorema B sob a
>    hipótese (U'), não provada — ver `adversarial/REFEREE_REPORT.md` §8.2.]**.
>    In **relative**
>    terms the limit law *does* break down, and exactly where one can name:
>    for `c=γn` with `γ∈(0,1]` fixed,
>    `φ(n,c)/φ_∞(c) → \sqrt{2/(2-γ)} > 1`. At the endpoint `γ=1` this is
>    **PROVED** (`φ(n,n)=Q(n)/n` exactly, `Q` Ramanujan's function, ratio
>    `→\sqrt2`); for `γ∈(0,1)` it is **NUMERICALLY CHARACTERIZED** with a
>    derived (non-rigorous) mechanism: the discrete chain's kill hazard is
>    `γ(2-γ)` times the continuum's `γ·2`, i.e. the finite-`n` model behaves
>    like the continuum one at the *renormalized* parameter
>    `c_{\rm eff}=c(1-c/2n)`. The relative error is `≈ c/(4n)`.
> 6. **No error or gap was found in any prior catalogued document.** The
>    engines built here reproduce, independently and exactly,
>    `φ_n^{(1)},φ_n^{(2)}`(table),`φ_n^{(6)}`(closed form, incl. `355081/823543`),
>    and Estágio 7's `c_K`. One *scope note* (not a defect) is flagged in §9.3
>    **[Correção pós-adversarial, 2026-08-23, F-6: leia-se "§8" — §9 é o
>    Scorecard, uma tabela sem subseções; a nota de escopo está em §8,
>    "Prior-document review".]**.
>
> **This is a positive result of real substance and therefore REQUIRES
> INDEPENDENT ADVERSARIAL REVIEW before being catalogued.** Nothing here is
> integrated, promoted, or closed by this document.

---

## 0. Discipline

**Scope.** Exactly two questions, in the brief's priority order: (1) is the
Teorema 3 convergence uniform for `c` in a fixed compact `[0,C]`, with an
explicit bound if possible; (2) what happens as `C→∞` / `c=c(n)→∞` jointly
with `n`. Both a symbolic/by-hand derivation and an independent numerical
corroboration were carried out for every claim.

**What was touched.** Only files inside this directory,
`.../theorem/uniform_in_c_attempt/`, all created by this front. **Nothing
outside it was modified, created, or deleted** — in particular not
`THEOREM.md`, not `DECISION_LEDGER.yaml`, not `TEST_QUEUE.yaml`, not
`DISCOVERY_LAB_STATE.md`, not `PROOF_DEPENDENCY_MAP.md`, not any `README*`,
not `tamesis-cycle-survival/`, and not any sibling `*_attempt/` directory.
Those documents were **read** (extensively) and are cited, never edited. **No
git commit was made.**

**Prior work reused as given, not re-derived.** `THEOREM.md` Definition 1
(`M_n(c)`), Definition 4 (`φ_n^{(K)}`), Fact 4.1 (the exact mixture identity
(7.1)), Lemma 2 (`φ_K=4^K(K!)^2/(2K+1)!=∫₀¹(1-t²)^K dt`), Theorem 1
(`φ_∞(c)=∫₀¹e^{-ct²}dt`), and **Teorema 3** (Estágio 6: for every fixed `c≥0`,
`φ(n,c)→φ_∞(c)`, unconditional). From Estágio 7: `c_K=[(K+2)φ_K-2]/4` as the
exact `1/n` coefficient of `φ_n^{(K)}-φ_K` **for each fixed `K`**. From
Estágio 6/8: the constants `D_r(b)` and their growth (used only to *name* a
gap in §5.6, never to support a claim). No transition rule, ODE, or closed
form of the `F_r/G_r/H_r` ladder is used anywhere in the proofs below.

**Arithmetic discipline.** Everything labeled PROVED or "exactly" uses
`fractions.Fraction` or `sympy.Rational`/`Symbol`. `mpmath` (40 digits) is used
for `φ_∞`, for the `e(c)` quadratures, and for display; `numpy.float64` is used
for the large-`n` sweeps, with a published float64-vs-longdouble-vs-exact audit
(`probe_pointwise.log`, agreement `≤6·10^{-15}` at `n=800`) so that every
displayed `n·Δ_n` figure carries `≥8` correct digits.

**Randomness.** One use only: `mc_check.py`, an independent Monte Carlo of the
**raw** Definition-1 model (uniform permutation + Bernoulli marks + cycle
detection on the functional digraph) used to validate the exact engines against
the model itself rather than against internal consistency. Seed, drawn fresh
for this session with `numpy.random.SeedSequence()`:

```
SeedSequence entropy = 109988594598087819892849058742026646086
```

No other script in this directory uses randomness of any kind.

**Two parameters, never conflated.** `c ≥ 0` is the **continuous** cyclic-return
rate of Definition 1 (`ξ_i ~ Bern(c/n)`); `K` (and its continuum avatar `r`)
is the **discrete** number of reroutes actually realized, the index of
Definition 4's `φ_n^{(K)}` and of the `F_r,G_r,H_r` ladder. The link is the
exact mixture (7.1): `φ(n,c)=E_{K∼\mathrm{Bin}(n,c/n)}[φ_n^{(K)}]`. Uniformity
in `c` is *not* uniformity in `K`; §6 makes their exact relationship the
subject of the one open hypothesis.

---

## 1. The target, restated precisely

Write, throughout,

`Δ_n(c) := φ(n,c) - φ_∞(c)`,  `φ_∞(c)=\int_0^1 e^{-ct^2}dt`,

with `φ(n,c)` as in `THEOREM.md` Definition 1, i.e. `q := c/n` for `c ≤ n`, and
`q := 1` for `c > n` (Definition 1's own stated convention, *"take `q = c/n ∧ 1`
if one insists on `n ≤ c`, immaterial in the limit"* — immaterial for Teorema 3,
but *material* for the global statement of §4, so it is named here explicitly;
see §8 **[Correção pós-adversarial, 2026-08-23, F-6: era "§9.3", referência
quebrada — corrigido para §8, "Prior-document review", onde a nota de fato
está.]**).

> **Question 1.** For fixed `C>0`, is `ω_n(C) := \sup_{c∈[0,C]}|Δ_n(c)| → 0`?
> With an explicit bound? How does the bound grow with `C`?
>
> **Question 2.** What happens for `C→∞`, or `c=c(n)→∞` jointly with `n`?

Teorema 3 gives `Δ_n(c)→0` for each fixed `c`, one `c` at a time, and nothing
more: `THEOREM.md` §7.1 explicitly says the locally-uniform version is *"a
natural strengthening, not attempted here and flagged as its own gap"*.

---

## 2. An independent finite-`n` representation: the `(j,R)` orbit chain

Nothing in this section is needed for the *proofs* of §§3–4 — those are direct
arguments on Definition 1. It is needed for the *numerics*, and it is derived
from scratch so that the numerical corroboration is genuinely independent of
every script in the rest of the archive.

### 2.1 The chain

Fix `n` and `q∈[0,1]`. Under Definition 1, explore the forward orbit of the
marked point `x_0 := 1`, revealing `ξ` and `π` lazily. Suppose the orbit has
reached `x_j`, having visited the `j+1` **distinct** points `x_0,…,x_j` and
completed `j` steps, of which `R` were **reroute** steps (`ξ=1`) and `j-R` were
**permutation** steps (`ξ=0`). Then:

- the revealed part of `π` is a partial injection whose image set is exactly
  `{x_{i+1} : \text{step } i \text{ was a permutation step}}`, of size `j-R`,
  and this set **never contains `x_0`** (every revealed image has index `≥1`);
- hence the still-available `π`-targets number `n-(j-R)`, comprising `x_0`,
  the `R` visited points reached *by a reroute* (`x_i`, `i≥1`, whose
  predecessor step was a reroute), and `n-j-1` fresh points.

Reading off the three outcomes — return to `x_0` (⇒ `1` is cyclic), land on
`x_1,…,x_j` (⇒ the orbit closes a cycle **not** containing `x_0`, so `1` is
never cyclic), or move to a fresh point — gives, conditionally on the entire
history:

| branch | weight | return to `x_0` | fatal | fresh |
|---|---|---|---|---|
| reroute (`U∼\mathrm{Unif}[n]`) | `q` | `1/n` | `j/n` | `(n{-}j{-}1)/n` → `(j{+}1,R{+}1)` |
| permutation (`π(x_j)`) | `1-q` | `1/(n{-}j{+}R)` | `R/(n{-}j{+}R)` | `(n{-}j{-}1)/(n{-}j{+}R)` → `(j{+}1,R)` |

so, with `P(j,R) := P(1 \text{ cyclic} \mid \text{state } (j,R))`,

> **(2.1)** `\displaystyle P(j,R) = q\Big[\tfrac1n+\tfrac{n-j-1}nP(j{+}1,R{+}1)\Big] + (1-q)\Big[\tfrac1{n-j+R}+\tfrac{n-j-1}{n-j+R}P(j{+}1,R)\Big]`,
>
> with terminal value `P(n{-}1,R)=q/n+(1-q)/(R{+}1)`, and `φ(n,c)=P(0,0)`.

`(j,R)` is a sufficient state: the *identities* of the visited points never
matter, only how many are fatal (`j`) and how many remain `π`-available (`R+1`,
one of which is `x_0`).

### 2.2 The conditional-`K` version

Conditioning on `K_n=K` (Definition 4) makes the rerouted set a uniform
`K`-subset of `[n]`, so the branch weight becomes the sampling-without-
replacement probability `(K-R)/(n-j)` instead of `q`; everything else is
unchanged. That gives `φ_n^{(K)}` by the same backward pass.

### 2.3 Validation (`chain_selftest.log`, `mc_check.log`, `chain_multi_selftest.log`)

The two engines were checked against **every** independently-published exact
value in the lineage that they can reach, and against the raw model:

| check | source | result |
|---|---|---|
| `φ_n^{(0)}=1`, `φ_n^{(1)}=2/3+1/(3n²)`, `n=1..12` | `THEOREM.md` Prop. 4 | exact, 12/12 |
| `φ_n^{(2)}`, `n=2..8` (`3/4,17/27,113/192,356/625,151/270,569/1029,281/512`) | `THEOREM.md` §7.4 table | exact, 7/7 |
| `φ_n^{(6)}` closed form, `n=7..11`, incl. `φ_7^{(6)}=355081/823543` | `k6_attempt/ATTEMPT.md` §1.2 | exact, 5/5 |
| mixture identity (7.1), `n=2..7`, 4 values of `c` each | `THEOREM.md` Fact 4.1 | exact, 24/24 **[Correção pós-adversarial, 2026-08-23, F-7: era "28/28" — `n=2..7` são 6 valores × 4 = 24, não 28; o referee confirmou 24/24 exato de forma independente.]** |
| `φ(n,0)=1`; `φ(n,n)=Q(n)/n` (Ramanujan `Q`), `n=1..11` | classical | exact, 11/11 |
| `n(φ_n^{(K)}-φ_K) → c_K`, `K=1,2,3,6,10,20,50` | Estágio 7 Teorema A | converging, 7/7 |
| raw Monte Carlo of Definition 1, `2·10^5` mappings × 13 `(n,c)`/`(n,K)` cells | — | all within sampling error |

No mismatch anywhere. In particular the engines reproduce, from a completely
different derivation, three separate archive results obtained by three
different methods (`K=1` case analysis; `K=2` brute-force enumeration; `K=6`
transfer-matrix telescoping).

---

## 3. Equi-Lipschitz in `c`: the one new analytic input, and Teorema A

### 3.1 The coupling lemma

> **Lema 3.1 (equi-Lipschitz, PROVED).** For all `n≥1` and all `c,c'≥0`,
> `|φ(n,c)-φ(n,c')| ≤ |c-c'|`.

*Proof.* By the convention of §1 it suffices to treat `0≤c<c'≤n`. On one
probability space let `V_1,…,V_n` be i.i.d. `Unif(0,1)`, put `ξ_i:=1\{V_i<c/n\}`
and `ξ'_i:=1\{V_i<c'/n\}`, and use the **same** `π` and the **same**
`U_1,…,U_n` for both. Then `ξ` has the law required by Definition 1 at `c`, and
`ξ'` at `c'`. On the event `E:=\{ξ_i=ξ'_i \ ∀i\}` the two mappings `f` and `f'`
are *identical*, so the indicator `1\{1 \text{ cyclic}\}` agrees. Hence

`|φ(n,c)-φ(n,c')| = |E[1\{1 \text{ cyc for } f\}] - E[1\{1\text{ cyc for }f'\}]| ≤ P(E^c) ≤ \sum_{i=1}^n P(ξ_i≠ξ'_i) = n\cdot\frac{c'-c}n = c'-c`. `∎`

Two remarks. (i) The bound is **uniform in `n`** — that is the entire point.
(ii) It is not pointwise-monotone: adding a reroute can *increase* the cyclic
count (e.g. `n=3`, `π=(1\,2\,3)`, reroute set `\{1\}` with `U_1=1` gives one
cyclic point, while reroute set `\{1,2\}` with `U_1=1,U_2=2` gives two), so no
coupling proof of monotonicity is available and none is used.

### 3.2 The sharp constant (not needed for the proof)

> **Lema 3.2 (derivative identity, PROVED).** For `0<c<n`,
> `\displaystyle \frac{\partial}{\partial c}φ(n,c) = E\big[φ_n^{(J+1)}-φ_n^{(J)}\big]`, `J∼\mathrm{Bin}(n{-}1,c/n)`.

*Proof.* Differentiate (7.1). With `p=c/n`, `\frac{d}{dp}P(\mathrm{Bin}(n,p)=K)
= n[P(\mathrm{Bin}(n{-}1,p)=K{-}1)-P(\mathrm{Bin}(n{-}1,p)=K)]` (from
`K\binom nK=n\binom{n-1}{K-1}` and `(n{-}K)\binom nK=n\binom{n-1}K`, with
`\binom{n-1}{-1}=\binom{n-1}n=0`); multiply by `dp/dc=1/n` and re-index. `∎`

Verified as an **exact symbolic identity** for `n=2,…,8` (`probe_exact.log`,
`LHS−RHS` simplifies to `0` in every case). It gives
`|∂_cφ(n,c)| ≤ \max_{0≤J<n}|φ_n^{(J+1)}-φ_n^{(J)}|`, and exact computation
(`probe_exact.log`, `probe_K.log`) shows that maximum is attained at `J=0` and
equals `φ_n^{(0)}-φ_n^{(1)} = \frac13-\frac1{3n^2}` (`n=2,4,8,16,32,64`:
`1/4, 5/16, 21/64, 85/256, 341/1024, 1365/4096`) — i.e. the **true** Lipschitz
constant is `<1/3`, exactly matching `|φ_∞'(0)|=1/3`. That sharpening is
**NUMERICALLY VERIFIED**, not proved (it needs `K↦φ_n^{(K)}` monotone, §6.3);
only the crude `≤1` of Lema 3.1 is used below, and it is unconditional.

### 3.3 Teorema A

> **Teorema A (locally uniform convergence; PROVED, unconditional).** For every
> fixed `C>0`,
> `\displaystyle ω_n(C)=\sup_{c∈[0,C]}\big|φ(n,c)-φ_∞(c)\big| \xrightarrow[n\to\infty]{} 0`,
> with the explicit finite-`n` inequality, valid for every integer `M≥1`,
>
> `\displaystyle ω_n(C) \le \max_{0\le i\le M}\big|Δ_n(iC/M)\big| \;+\; \frac{4C}{3M}`.

*Proof.* `φ_∞` is Lipschitz with constant `\sup_c|φ_∞'(c)|=\sup_c\int_0^1
t^2e^{-ct^2}dt ≤ \int_0^1t^2dt = 1/3`. With Lema 3.1, `Δ_n` is Lipschitz with
constant `1+\frac13=\frac43`, **uniformly in `n`**. Put `c_i := iC/M`. Every
`c∈[0,C]` lies in some `[c_i,c_{i+1}]`, whence `|Δ_n(c)| ≤ |Δ_n(c_i)| +
\frac43\cdot\frac CM`, giving the displayed inequality. Now fix `ε>0`: choose
`M` with `4C/(3M)<ε/2`; by **Teorema 3** (Estágio 6, unconditional) applied at
each of the finitely many points `c_0,…,c_M`, there is `N` with
`\max_i|Δ_n(c_i)|<ε/2` for all `n≥N`; hence `ω_n(C)<ε` for `n≥N`. `∎`

This is the standard "pointwise + equicontinuous ⟹ uniform on compacts"
argument; the only thing that was missing in the archive was the
equicontinuity, and Lema 3.1 supplies it in one line. Note what is *not*
needed: no `F_r/G_r/H_r`, no error constants, no rate, no monotonicity.

**Answer to Question 1, qualitative part: YES — the finite-`n` error on a fixed
compact is bounded by a function of `n` alone.** The quantitative part (how the
bound grows with `C`, and whether it can be made explicit) is §§5–6.

---

## 4. Beyond compacts: a uniform tail bound, and global uniformity

### 4.1 The tail lemma

> **Lema 4.1 (uniform-in-`n` tail bound; PROVED).** Let `q:=\min(c/n,1)`. For
> every `n≥1`, every `c≥0`, and every integer `1≤J≤n/2`,
>
> `\displaystyle φ(n,c) \;\le\; \frac J{n-J} \;+\; \exp\Big(-\,\frac{q\,J(J-1)}{2n}\Big) \;\le\; \frac{2J}n + \exp\Big(-\frac{qJ(J-1)}{2n}\Big)`.

*Proof.* Run the exploration of §2.1 (only the two conditional facts below are
used; the full chain is not). Conditionally on **any** history, at step `j`:

- **(a)** `P(\text{return to } x_0 \text{ at step } j) = \frac qn +
  \frac{1-q}{n-j+R} \le \frac q{n-j}+\frac{1-q}{n-j} = \frac1{n-j}`,
  using `R≥0` and `n-j≤n`; and `x_0` is always an available `π`-target (§2.1).
- **(b)** `P(\text{fatal at step } j) \ge q\cdot\frac jn`, from the reroute
  branch alone (landing on any of `x_1,…,x_j` permanently excludes `x_0` from
  the orbit's terminal cycle).

The event `\{1\text{ cyclic}\}` is the disjoint union over `j` of "first return
at step `j`". Splitting at `J`,

`φ(n,c) \le \sum_{j<J}P(\text{return at step }j) + P(\text{alive at step }J)`,

where "alive at `J`" means no return and no fatality before step `J`. By (a)
the first sum is `\le\sum_{j<J}\frac1{n-j}\le\frac J{n-J}`. By (b) and the
tower property, `P(\text{alive at }J)\le\prod_{j<J}(1-\frac{qj}n) \le
\exp(-\frac qn\sum_{j<J}j) = \exp(-\frac{qJ(J-1)}{2n})`. `∎`

> **Corolário 4.2 (PROVED).** Let `L≥1` and `C_0 ≥ \max(16L,\,80)`. For every
> `n ≥ C_0`,
> `\displaystyle \sup_{c\ge C_0}φ(n,c) \;\le\; 2\sqrt{\tfrac{2L}{C_0}} + \tfrac4n + e^{-L}`,
> and in particular, taking `L=\log C_0`,
> `\displaystyle \sup_{c\ge C_0}φ(n,c) \;\le\; ω(C_0)+\tfrac4n`, `ω(C_0):=2\sqrt{\tfrac{2\log C_0}{C_0}}+\tfrac1{C_0} \xrightarrow[C_0\to\infty]{}0`.

*Proof.* The right-hand side of Lema 4.1 is non-increasing in `c` (only through
`q=\min(c/n,1)`), so it suffices to evaluate at `c=C_0`, where `q=C_0/n` since
`n≥C_0`. Take `J:=\lceil n\sqrt{2L/C_0}\rceil+1`; then `J-1\ge n\sqrt{2L/C_0}`
and `J\ge J-1`, so `\frac{qJ(J-1)}{2n} \ge \frac{C_0}{n}\cdot
\frac{(n\sqrt{2L/C_0})^2}{2n}=L`. Also `J\le n\sqrt{2L/C_0}+2 \le n/2` because
`C_0\ge16L` gives `\sqrt{2L/C_0}\le\frac1{\sqrt8}=0.3536\le\frac12-\frac2n` for `n\ge C_0\ge80`. Then
`2J/n\le2\sqrt{2L/C_0}+4/n`. `∎`

Numerically controlled in `probe_tail.log`: **zero violations** of Lema 4.1
across `n∈\{50,200,800,3200\}` and `c∈\{5,20,50,200,800,n\}` (the bound is loose
by a factor `2.5`–`4.2`), and the `C_0`-tail values `0.531, 0.259, 0.116,
0.053, 0.025` at `C_0=50,200,10^3,5·10^3,2.5·10^4`, essentially identical at
`n=10^3,10^4,10^5` — i.e. genuinely uniform in `n`, decaying like `C_0^{-1/2}`
up to the log.

### 4.2 Teorema C

> **Teorema C (globally uniform convergence; PROVED, unconditional).**
> `\displaystyle \lim_{n\to\infty}\ \sup_{c\in[0,\infty)}\big|φ(n,c)-φ_∞(c)\big| \;=\; 0`,
> with `φ(n,c)` read under Definition 1's `q=\min(c/n,1)` convention.

*Proof.* Fix `ε>0`. Since `φ_∞(C_0)\le\frac{\sqrtπ}{2\sqrt{C_0}}\to0` and
`ω(C_0)\to0`, choose `C_0\ge80` with `ω(C_0)+φ_∞(C_0)<ε/2`. For `c\ge C_0`,
`|Δ_n(c)|\le φ(n,c)+φ_∞(c)\le ω(C_0)+\frac4n+φ_∞(C_0)` by Corolário 4.2 and
monotonicity of `φ_∞`; so `\sup_{c\ge C_0}|Δ_n|<ε/2+\frac4n`. By **Teorema A**,
`\sup_{[0,C_0]}|Δ_n|<ε/4` for `n` large. Taking `n\ge\max(C_0,16/ε)` and
combining gives `\sup_{c\ge0}|Δ_n|<ε`. `∎`

So the answer to Question 1 is stronger than asked: **uniformity does not fail
anywhere on the parameter range**, compact or not. What *does* happen at large
`c` is not a failure of uniform convergence but a failure of *relative*
accuracy — §7.

---

## 5. The exact first-order error profile `e(c)`

### 5.1 The exact two-part decomposition

From (7.1) and (7.2), with `b_K(c):=P(\mathrm{Bin}(n,c/n)=K)` and
`p_K(c):=P(\mathrm{Poi}(c)=K)`, exactly (no asymptotics):

`\displaystyle Δ_n(c) \;=\; \underbrace{\sum_{K=0}^n b_K(c)\,\big(φ_n^{(K)}-φ_K\big)}_{=:A_n(c)} \;+\; \underbrace{\sum_{K\ge0}\big(b_K(c)-p_K(c)\big)φ_K}_{=:B_n(c)}`.

This is exactly the split `THEOREM.md` §7.2 uses to prove Proposition 3; here
both halves are computed to first order rather than merely shown to vanish.

### 5.2 `B_n` in closed form — an exact integral identity

> **Lema 5.1 (PROVED).** For every `n≥1` and `0\le c\le n`,
> `\displaystyle B_n(c) \;=\; \int_0^1\Big[\Big(1-\frac{ct^2}n\Big)^{\!n} - e^{-ct^2}\Big]\,dt \;\le\; 0`.

*Proof.* `φ_K=\int_0^1(1-t^2)^K dt` (Lemma 2). Exchanging the finite/absolutely
convergent sums with the integral and using the two probability generating
functions at `z=1-t^2`:
`\sum_K b_K z^K = (1-\frac cn(1-z))^n = (1-\frac{ct^2}n)^n` and
`\sum_K p_K z^K = e^{-c(1-z)} = e^{-ct^2}`. The sign follows from `1-u\le e^{-u}`
with `u=ct^2/n`. `∎`

Confirmed to `\le1.6\cdot10^{-17}` against direct summation for
`n\in\{5,10,20\}`, `c\in\{1,3,5\}` (`probe_exact.log`). Its `1/n` expansion,
`(1-x/n)^n = e^{-x}(1-\frac{x^2}{2n}+O(n^{-2}))`, gives

`\displaystyle n\,B_n(c) \longrightarrow -\frac{c^2}2\int_0^1 t^4e^{-ct^2}dt = -\frac{c^2}2 I_2(c)`, `I_k(c):=\int_0^1t^{2k}e^{-ct^2}dt`,

equivalently `-\frac{c^2}2 E_{\mathrm{Poi}(c)}[Δ^2φ_K]` with
`Δ^2φ_K=φ_{K+2}-2φ_{K+1}+φ_K=\int_0^1(1-t^2)^Kt^4dt`.

### 5.3 `A_n`, and the profile

For each *fixed* `K`, Estágio 6/7 give `n(φ_n^{(K)}-φ_K)\to c_K=\frac{(K+2)φ_K-2}4`.
Since `E_{\mathrm{Poi}(c)}[Kφ_K]=\int_0^1 c(1-t^2)e^{-ct^2}dt` and
`E_{\mathrm{Poi}(c)}[φ_K]=φ_∞(c)=I_0(c)`,

`\displaystyle E_{\mathrm{Poi}(c)}[c_K] = \tfrac14\big[c(I_0(c)-I_1(c))+2I_0(c)-2\big]`,

and adding the `B_n` part gives the **error profile**

> **(5.1)** `\displaystyle e(c) \;:=\; \tfrac14\big[c\,(I_0-I_1)+2I_0-2\big] \;-\; \tfrac{c^2}2 I_2`.

### 5.4 The coefficient-wise theorem — fully rigorous

> **Teorema D (PROVED, unconditional given Estágio 6/7).** For every fixed
> integer `j≥0`, writing `[c^j]` for the `j`-th Taylor coefficient at `c=0`
> (`φ(n,\cdot)` is a polynomial of degree `n`, so this is a finite object):
>
> `\displaystyle n\Big([c^j]φ(n,\cdot) - [c^j]φ_∞\Big) \xrightarrow[n\to\infty]{} e_j := \frac{(-1)^j}{j!}\Big[\sum_{K=0}^j(-1)^K\binom jK c_K \;-\; \binom j2\sum_{K=0}^j(-1)^K\binom jKφ_K\Big]`,
>
> and `e_j = [c^j]e(c)` for every `j`.

*Proof.* From (7.1), `[c^j]` picks up only `K\le j`, and
`\binom nK\binom{n-K}{j-K}=\binom nj\binom jK`, so **exactly**

`\displaystyle [c^j]φ(n,\cdot) \;=\; (-1)^j\,\frac{\binom nj}{n^j}\sum_{K=0}^j(-1)^K\binom jK\,φ_n^{(K)}`,

a **finite** sum of `j+1` terms. The same computation on the Poisson mixture
gives `[c^j]φ_∞ = \frac{(-1)^j}{j!}\sum_{K=0}^j(-1)^K\binom jKφ_K`
(`=\frac{(-1)^j}{j!(2j+1)}`). Insert `φ_n^{(K)}=φ_K+\frac{c_K}n+O_K(n^{-2})`
(Estágio 6/7, valid for each of the finitely many fixed `K\le j`) and
`\frac{\binom nj}{n^j}=\frac1{j!}\prod_{i=0}^{j-1}(1-\tfrac in)
=\frac1{j!}\big(1-\frac{\binom j2}n+O(n^{-2})\big)`; collect the `1/n` term. No
interchange of limits occurs anywhere: the sum is finite for each `j`. `∎`

**Both formulas for `e_j` were computed exactly and independently** — the
finite-difference one above from `c_K,φ_K` in `Fraction` arithmetic, the
analytic one from the series of (5.1) in `sympy` — and agree for `j=0,…,8`
(`probe_taylor.log`): `e_0=e_1=0`, `e_2=-1/12`, `e_3=1/15`, `e_4=-3/112`,
`e_5=1/135`, `e_6=-5/3168`, `e_7=1/3640`, `e_8=-7/172800`. The finite-`n` exact
Taylor coefficients converge to them (`j=2`: `-0.0831375` at `n=20` →
`-0.0833331` at `n=640`, target `-1/12=-0.0833333`).

`e_0=e_1=0` is a consistency check with a known archive fact: `THEOREM.md`
Corolário 4.3 proves `a_1(n)=\frac13-\frac1{3n^2}` exactly, i.e. the linear
Taylor coefficient has **no** `1/n` term — precisely `e_1=0`.

### 5.5 Closed form and asymptotics of `e`

> **Proposição 5.2 (PROVED).** For `j≥1`,
> `\displaystyle e_j = (-1)^{j+1}\frac{(j-1)^2}{2\,(2j-1)\,j!}` (and `e_0=0`), whence
>
> `\displaystyle e(c) \;=\; \frac12\int_0^1\frac{1-\big(1+ct^2+c^2t^4\big)e^{-ct^2}}{t^2}\,dt \;=\; \frac{\sqrt c}2\int_0^{\sqrt c}\frac{1-(1+u^2+u^4)e^{-u^2}}{u^2}\,du`.
>
> Consequently `e(c) = -\frac{c^2}{12}+\frac{c^3}{15}-\frac{3c^4}{112}+\cdots`
> near `0`, and
> `\displaystyle e(c) \;=\; \frac{\sqrt{\pi c}}8-\frac12+O\!\big(\sqrt c\,e^{-c}\big)` as `c\to\infty`.

*Proof.* `\frac1{2j-1}=\int_0^1t^{2j-2}dt` turns `\sum_j e_jc^j` into
`\frac12\int_0^1 t^{-2}\sum_{j\ge1}(-1)^{j+1}(j-1)^2\frac{(ct^2)^j}{j!}dt`, and
`\sum_{j\ge0}(j-1)^2\frac{(-x)^j}{j!}=e^{-x}(x^2+x+1)` (from `\sum z^j/j!=e^z`,
`\sum jz^j/j!=ze^z`, `\sum j^2z^j/j!=(z^2+z)e^z` at `z=-x`), so the inner sum is
`1-e^{-x}(1+x+x^2)` with `x=ct^2`. Substituting `u=t\sqrt c` gives the second
form. For the tail, `\int_0^\infty\frac{1-(1+u^2+u^4)e^{-u^2}}{u^2}du =
\int_0^\infty\frac{1-e^{-u^2}}{u^2}du-\int_0^\infty e^{-u^2}du-\int_0^\infty
u^2e^{-u^2}du = \sqrtπ-\frac{\sqrtπ}2-\frac{\sqrtπ}4=\frac{\sqrtπ}4`
(the first by one integration by parts), while
`\int_{\sqrt c}^\infty\frac{1-(1+u^2+u^4)e^{-u^2}}{u^2}du =
\frac1{\sqrt c}-O(e^{-c}\mathrm{poly})`; multiply by `\sqrt c/2`. `∎`

Machine-confirmed (`ecoef2.log`): the three representations of `e(c)` agree to
`\ge16` digits at nine values of `c`; the coefficient closed form matches the
`sympy` series for `j=1,…,11` **symbolically**; `\int_0^\infty\cdots
= 0.44311346272637900682 = \sqrtπ/4` to 20 digits; and `e(c)/\sqrt c` equals
`\sqrtπ/8-\frac1{2\sqrt c}` to 12 digits already at `c=100`.

Useful landmarks (`ecoef.log`): `e<0` on `(0,c_\times)`, `e>0` after, with
`c_\times = 4.83904605495…`; the unique minimum is `e = -0.06696142887…` at
`c=2.283781525…`; `e(c)\sim\sqrt{πc}/8`, `\sqrtπ/8=0.2215567314…`.

### 5.6 The uniform version, and the one named gap

> **Teorema E (PROVED-MODULO-[K-uniform domination]).** For every `c\ge0`,
> `n\,Δ_n(c) \to e(c)`, and `n\,\sup_{[0,C]}|Δ_n| \to \sup_{[0,C]}|e|`.

The `B_n` half is unconditional (Lema 5.1 plus dominated convergence on a
*fixed* `[0,1]` integral). The `A_n` half needs to move the limit inside the
`K`-sum, i.e. a bound `|n(φ_n^{(K)}-φ_K)|\le M_K` with
`\sum_K \frac{c^K}{K!}M_K<\infty` (legitimate since `b_K(c)\le c^K/K!`). The
archive supplies exactly such a bound only through the error constants
`D_r(b)`: `|ψ_n^{(K)}-φ_K-\frac{Kφ_K}{4n}|\le D_K(0)/n^2` (Estágio 6) plus
Reduction Lemma A gives `M_K\le \frac{5K}4+D_K(0)` on the theorem's own
hypothesis `n\ge K+1`. **Any geometric growth `D_K(0)=O(λ^K)` suffices**
(`\sum c^Kλ^K/K!=e^{cλ}<\infty`), and Estágio 8's Proposição 6 does prove the
improved constants `D'_r(b)` are geometric — but Estágio 8 itself labels the
**rate** of that geometric bound NUMERICALLY CHARACTERIZED (`≈1.24` at `r=45`),
with no published closed constant, and the originally-published `D_r(b)` are
factorial, which is *not* enough (`\sum c^K K!/K!` diverges for `c\ge1`). So
Teorema E is **honestly conditional** on a growth statement that the archive
has proved qualitatively but not with an explicit constant.

> **[Correção pós-adversarial, 2026-08-23, F-1 de
> `adversarial/REFEREE_REPORT.md` §6.2.]** O parágrafo acima contém uma
> inconsistência lógica real, apontada pelo referee: se (i) "qualquer
> crescimento geométrico `D_K(0)=O(λ^K)` basta" e (ii) "Estágio 8's
> Proposição 6 **does prove** ... geométricas" são ambas verdadeiras, então
> o valor exato de `λ` é irrelevante e Teorema E seria **incondicional** —
> não "condicional por falta de constante explícita" como (iii) afirma
> logo a seguir. As três afirmações não podem ficar de pé juntas.
> Verificando a fonte citada: a afirmação (ii) está **superestimada**.
> `error_constant_growth_attempt/ATTEMPT.md` §6.1 (a Proposição 6) prova o
> LIMITANTE (a construção `D'_r(b),C'_r(b)` satisfaz o Teorema-Alvo), mas
> não prova a geometricidade — sua própria tabela de status em §6.3
> classifica `D'_r(b),C'_r(b)` como "**PROVED bound; rate NUMERICALLY
> CHARACTERIZED**", e a geometricidade dos insumos `A_r(b),B_r(b)` que a
> sustentariam está listada como apenas "NUMERICALLY CHARACTERIZED,
> mechanism proved". **O rótulo PROVED-MODULO de Teorema E permanece
> correto**, mas a lacuna nomeada está errada: não é "um limitante
> geométrico de constante explícita" que falta, é uma **prova escrita da
> geometricidade qualitativa** de `M_K` — a própria Proposição 6 ainda não
> fornece isso. (O referee registra, sem executar, uma rota plausível para
> fechar essa lacuna a partir de ingredientes já provados do Estágio 8 —
> ver `adversarial/REFEREE_REPORT.md` §6.2, nota construtiva — que, se
> bem-sucedida, tornaria Teorema E incondicional.) Corrigido aqui e no
> Scorecard (item 12) e nas seções §8/§10 abaixo.

> **[Adendo datado, 2026-08-23 — DISC-DEC-052, GAP FECHADO.]** A rota
> construtiva mencionada acima foi tentada (onda 12, frente (a),
> `mk_geometricity_attempt/ATTEMPT.md`) — mas não pela rota Proposição-6
> literalmente sugerida (que exigiria um limitante geométrico geral-`b`
> para `A_r(b),B_r(b)` ainda não estabelecido em nenhum lugar do
> arquivo, e permanece OPEN como questão separada). Uma rota mais direta,
> usando a forma fechada todas-as-ordens do Estágio 9 (`ψ_n^{(K)}`,
> Corolário A1) mais o Lema A de redução, prova
> `M_K \le φ_K(K{+}1)e^{K/2}+K = O(K(\sqrt e)^K)` — geométrico,
> qualquer `λ` serve, exatamente o que falta acima — de forma totalmente
> elementar e incondicional. Verificado adversarialmente, veredito
> **SOUND**, "ACCEPT for catalogue"
> (`mk_geometricity_attempt/adversarial/REFEREE_REPORT.md`). **Teorema E
> PERDE o rótulo PROVED-MODULO e torna-se PROVADO, incondicional, em
> ambas as versões (pontual e uniforme).** Isto NÃO fecha a hipótese
> (U') nem "uma taxa explícita para Teorema A/C" (§6.3 abaixo,
> item 16) — são obstruções genuinamente diferentes: (U') exige
> `|φ_n^{(K)}-φ_K|\le a\sqrt K/n` UNIFORME em `K` (um limitante que NÃO
> cresce com `K`), enquanto o resultado aqui só precisa que `M_K` cresça
> no máximo geometricamente em `K` (um limitante que CRESCE com `K`,
> apenas não mais rápido que geométrico) — uma condição estritamente
> mais fraca, suficiente para a soma `\Sigma_K c^K M_K/K!` convergir mas
> insuficiente para um limitante explícito uniforme-em-`K`. Ver
> `THEOREM.md` "Estágio 11" para o enunciado completo e
> `mk_geometricity_attempt/ATTEMPT.md` para a prova.

It is nevertheless

**NUMERICALLY VERIFIED to high accuracy** (`probe_pointwise.log`,
`probe_uniform.log`): at `c=0.5,1,2,5,10,25,60`, `n\,Δ_n(c)` agrees with `e(c)`
to `4`–`5` significant digits at `n=102400` with clean `1/n` convergence; and

| `C` | `n·\sup_{[0,C]}|Δ_n|`, `n=200` | `800` | `3200` | `12800` | `51200` | `\sup_{[0,C]}|e|` |
|---|---|---|---|---|---|---|
| 1 | 0.035748 | 0.036976 | 0.037282 | 0.037359 | 0.037378 | **0.037384** |
| 2 | 0.062181 | 0.064742 | 0.065380 | 0.065540 | 0.065579 | **0.065593** |
| 5 | 0.063048 | 0.065974 | 0.066714 | 0.066900 | 0.066946 | **0.066961** |
| 10 | 0.225230 | 0.206800 | 0.202261 | 0.201131 | 0.200849 | **0.200755** |
| 25 | 0.688230 | 0.627227 | 0.612604 | 0.608986 | — | **0.607784** |
| 100 | 2.342404 | 1.848715 | 1.747643 | 1.723514 | — | **1.715567** |
| 400 | — | 5.080512 | 4.172816 | — | — | **3.931135** |

with the argmax tracked as well: for `C\le2.284` it sits at `c=C`; at `C=5` it
sits at the **interior** point `c=2.2839`, matching `e`'s minimiser
`2.283781…` to 4 digits; for `C\ge10` it returns to `c=C`. Grid resolution was
controlled (npts `41/161/641` give identical values to 8 digits).

**Consequence — the answer to "how does the bound grow with `C`":**
`\sup_{[0,C]}|e| = |e(2.2838)|=0.066961` for `C\le c_\times`, and `=e(C)\sim
\sqrt{πC}/8` after. **The uniform-on-`[0,C]` error constant grows exactly like
`\sqrt C`** — sublinearly, which is why §4's global statement can hold at all.

---

## 6. An explicit bound, and exactly what is missing

### 6.1 The Poisson-approximation half, done explicitly

> **Lema 6.1 (PROVED, elementary).** For `n\ge4` and `0\le x\le n`,
> `0 \le e^{-x}-(1-x/n)^n \le \frac{x^2}n e^{-x}`.

*Proof.* Left inequality: `1-u\le e^{-u}`. Right: if `x\ge\sqrt n` then
`\frac{x^2}ne^{-x}\ge e^{-x}\ge e^{-x}-(1-x/n)^n`, done. If `x<\sqrt n`, put
`u=x/n<1/\sqrt n`; then `e^{-x}-(1-u)^n = e^{-x}\big(1-e^{-n\sum_{k\ge2}u^k/k}\big)
\le e^{-x}\,n\sum_{k\ge2}\frac{u^k}k \le e^{-x}\frac{nu^2}{2(1-u)} \le e^{-x}nu^2
=\frac{x^2}ne^{-x}`, using `1-e^{-y}\le y` and `1-u\ge1-\frac1{\sqrt n}\ge\frac12`
for `n\ge4`. `∎`

Scanned over `n\in\{4,5,7,10,30,100,1000\}` × 2001 points each: the ratio to the
bound never exceeds `0.564` and the left side is never negative
(`probe_exact.log`). Combining with Lema 5.1,

> **Corolário 6.2 (PROVED).** For `n\ge4` and `0\le c\le n`,
> `\displaystyle |B_n(c)| \le \frac{c^2 I_2(c)}n \le \frac{κ_B}n`, `κ_B := \sup_{c\ge0}c^2I_2(c) = 0.280480169025…` (attained at `c=4.086754546…`).

That half of the error is therefore bounded **uniformly over all `c` at once**,
by an absolute constant over `n`. All the `C`-dependence lives in `A_n`.

### 6.2 The hypothesis that would finish the job

> **Hypothesis (U'_a).** There is `a<∞` with
> `\displaystyle \big|φ_n^{(K)}-φ_K\big| \le \frac{a\sqrt K}{n}` for **all** `0\le K\le n`.

> **Teorema B (PROVED given (U'_a)).** For `n\ge4` and `0\le c\le n`,
> `\displaystyle |Δ_n(c)| \le \frac{a\sqrt c + κ_B}{n}`, hence
> `\displaystyle \sup_{c\in[0,C]}|Δ_n(c)| \le \frac{a\sqrt C+0.2805}{n}`.

*Proof.* `|A_n(c)|\le\frac an E[\sqrt{\mathrm{Bin}(n,c/n)}]\le\frac an
\sqrt{E[\mathrm{Bin}]}=\frac{a\sqrt c}n` (Jensen), plus Corolário 6.2. `∎`

The `\sqrt C` growth of Teorema B matches the *truth* established in §5.5
(`e(C)\sim\sqrt{πC}/8`), so (U') is the right shape of hypothesis, not a lossy
one. Numerically (`probe_uniform.log`), across the entire `(n,C)` scan the ratio
`|Δ_n(c^*)|\big/\big[(\sqrt{c^*}+κ_B)/n\big]` never exceeds **0.2505**, i.e.
Teorema B with `a=1` holds with a factor-4 margin everywhere tested.

### 6.3 Status of (U'), honestly

`probe_K.log` / `probe_K_sharp.log`: for each `K`, `\max_n n|φ_n^{(K)}-φ_K|` is
attained at the **smallest** admissible `n`, namely `n=K+1`, and

| `K` | 8 | 32 | 128 | 512 | 2048 | 8192 | 16384 |
|---|---|---|---|---|---|---|---|
| `n\lvert φ_n^{(K)}-φ_K\rvert/K` (max over `n`) | 0.0953 | 0.0554 | 0.0300 | 0.0156 | — | — | — |
| `n\lvert φ_n^{(K)}-φ_K\rvert/\sqrt K` (max over `n`) | 0.2696 | 0.3135 | 0.3390 | 0.3527 | 0.3598 | 0.3634 | 0.3645 |

The `/K` column decreases (so the cruder `|φ_n^{(K)}-φ_K|\le K/n` holds with a
lot of room); the `/\sqrt K` column increases and is converging, from below, to

`a^* := \sqrtπ\big(\tfrac1{\sqrt2}-\tfrac12\big) = 0.3670872119…`,

which is exactly the value predicted by the two endpoint asymptotics
`φ_{K+1}^{(K)}\sim\sqrt{π/(2(K{+}1))}` (at `n=K{+}1` all but one point is
rerouted, so `f` is a uniform random mapping in all but one coordinate, and the
Ramanujan-`Q` value of Prop. 7.1 applies up to an `O(1/n)` relative correction)
and `φ_K\sim\sqrtπ/(2\sqrt K)` (Wallis/Stirling).

> **[Correção pós-adversarial, 2026-08-23, S-1 de
> `adversarial/REFEREE_REPORT.md` §6.5 — um fortalecimento, não uma
> correção.]** A correção `O(1/n)` acima é desnecessária: a identidade é
> **exata**. `φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n` para todo `n\ge1` — com `K=n-1`
> reroteamentos, o único ponto `x` não-reroteado tem `f(x)=π(x)`, e a lei
> **marginal** de `π(x)` para uma permutação uniforme é `Uniform[n]`,
> independente dos `U_i`; logo `f` é exatamente um mapeamento aleatório
> uniforme, e a Proposição 7.1 se aplica textualmente, sem correção alguma.
> Verificado exatamente (`Fraction`) para `n=2,\ldots,10`: os três valores
> `φ_n^{(n-1)}`, `φ_n^{(n)}` e `Q(n)/n` são idênticos em cada caso — o que
> também explica retroativamente por que `φ_7^{(6)}=355081/823543` (§2.3
> acima) é exatamente o mesmo racional que `φ(7,7)`. Isto torna o mecanismo
> de `a^*` exato no extremo `K=n-1`, em vez de apenas heurístico — mas
> **não** prova (U'), que precisa adicionalmente que o máximo sobre `n` seja
> atingido em `n=K+1`, o que permanece numérico.
Two-point Richardson in `K` (assuming the `O(K^{-1/2})` correction the two
endpoint asymptotics predict) gives `0.366966, 0.367026, 0.367057, 0.367072`
for the consecutive pairs up to `(8192,16384)` — approaching `a^*` monotonically,
the last one within `1.6\cdot10^{-5}` of it (`extrapolate.log`).

> **Status of (U'):** **NUMERICALLY CHARACTERIZED**, sharp constant `a^*`
> identified and mechanistically explained, **not proved**. Proving it is
> exactly the statement "Estágio 7's `1/n` rate is uniform in `K`" — and the
> archive is explicit (Estágio 7, *Cautelas de redação*) that **no uniformity
> in `K` is proved or claimed** there. This is the single obstruction between
> Teorema A/C (soft, unconditional) and a fully explicit rate.

A related, weaker fact also came out **NUMERICALLY VERIFIED** and would give an
independent second proof of §4's tail step: `K\mapstoφ_n^{(K)}` is
non-increasing (exhaustively in `K` for `n=5,12,30,80,200,600` in float, and in
**exact `Fraction` arithmetic for all `K` at `n=2,…,9`**; strict decrease in
every case). Combined with Lema 3.2 this would give `∂_cφ(n,c)\le0`, i.e.
`φ(n,\cdot)` non-increasing, and hence a Pólya-type route to Teorema A. It is
**not used** in any proof above — Lema 3.1 and Lema 4.1 are unconditional and
suffice.

---

## 7. Question 2: `c` growing with `n`

### 7.1 The endpoint `c=n`: exact, and the limit law does break — in ratio

> **Proposição 7.1 (PROVED).** For every `n\ge1`, `φ(n,n) = Q(n)/n` where
> `Q(n)=\sum_{j\ge0}\prod_{i=1}^{j}(1-\tfrac in)` is Ramanujan's `Q`-function.
> Hence, using the classical `Q(n)=\sqrt{πn/2}-\tfrac13+O(n^{-1/2})` (**CITED**:
> Ramanujan; Knuth, *TAOCP* I §1.2.11.3; Flajolet–Odlyzko, *Random mapping
> statistics*, EUROCRYPT'89):
>
> `\displaystyle \sqrt n\,φ(n,n) \to \sqrt{π/2}=1.25331…`, while `\sqrt n\,φ_∞(n)\to\sqrtπ/2=0.88623…`,
>
> so `\displaystyle \frac{φ(n,n)}{φ_∞(n)}\to\sqrt2`, while
> `\displaystyle |φ(n,n)-φ_∞(n)| \sim \frac{a^*}{\sqrt n}\to0`, `a^*=\sqrtπ(\tfrac1{\sqrt2}-\tfrac12)`.

*Proof of the exact identity.* At `c=n`, `q=1`: every point is rerouted, so `f`
is a uniform random mapping `[n]\to[n]`. `P(1\text{ cyclic})=\sum_{j\ge1}
P(\text{orbit } 1\to x_1\to\cdots\to x_{j-1}\to1 \text{ with all distinct}) =
\sum_{j\ge1}\frac1n\prod_{i=1}^{j-1}(1-\tfrac in) = Q(n)/n`. `∎`

Verified exactly (`Fraction`) for `n=1,…,11` in `chain_selftest.log`, and
numerically: `\sqrt n\,φ(n,n)=1.220996, 1.236905, 1.245046, 1.249164` at
`n=100,400,1600,6400` — matching `\sqrt{π/2}-\frac1{3\sqrt n}` to six digits.

This is the sharpest possible statement of the breakdown: **the two functions
stay within `O(n^{-1/2})` of each other (Teorema C), but their ratio converges
to `\sqrt2`, not to `1`.**

### 7.2 The joint regime `c=γn`

The same exploration explains the whole family. With `q=γ` fixed and the orbit
length on the scale `j = x\sqrt n` (so `R\approx γ j`, `n-j+R\approx n`), the
per-step hazards of §4.1 read

`\text{return}: \ \tfrac γn+\tfrac{1-γ}{n-j+R}\approx\tfrac1n`,  
`\text{fatal}: \ γ\tfrac jn + (1-γ)\tfrac Rn \approx \tfrac{γ(2-γ)\,j}{n}`,

giving `φ(n,γn)\approx\frac1n\sum_{J\ge0}e^{-γ(2-γ)J^2/(2n)} \to
\sqrt{\dfracπ{2γ(2-γ)}}\cdot n^{-1/2}`. Equivalently, since the continuum's
fatal hazard is `2c\,t\,dt` (i.e. `γ(2-γ)\to2γ` as `γ\to0`), the finite-`n`
model behaves like the continuum one at the **renormalized parameter**

> **(7.1)** `\displaystyle c_{\rm eff} \;=\; c\Big(1-\frac{c}{2n}\Big)`,  so  `\displaystyle \frac{φ(n,c)}{φ_∞(c)} \;\longrightarrow\; \sqrt{\frac2{2-γ}}`, `γ=c/n`.

Both limits reduce correctly: `γ\to0` gives ratio `1` and
`\sqrt{π/(4γ)}\,n^{-1/2}=φ_∞(c)`; `γ=1` gives `\sqrt{π/2}\,n^{-1/2}` and ratio
`\sqrt2`, reproducing the **proved** Proposição 7.1. Also, expanding (7.1) for
`1\ll c\ll n` gives relative error `\approx γ/4 = c/(4n)`, which independently
reproduces §5's large-`c` profile: `e(c)/φ_∞(c)\approx
\frac{\sqrt{πc}/8}{\sqrtπ/(2\sqrt c)}=\frac c4`, divided by `n`. **Two
unrelated derivations, the same `c/(4n)`.**

`probe_large_c.log`:

| `γ` | `\sqrt n\,φ(n,γn)` at `n=4000` | predicted `\sqrt{π/(2γ(2-γ))}` | ratio `φ/φ_∞` at `n=4000` | predicted `\sqrt{2/(2-γ)}` |
|---|---|---|---|---|
| 0.05 | 4.006055 | 4.013818 | 1.010781 | 1.012739 |
| 0.10 | 2.867677 | 2.875300 | 1.023258 | 1.025978 |
| 0.25 | 1.887647 | 1.894833 | 1.064991 | 1.069045 |
| 0.50 | 1.440789 | 1.447203 | 1.149583 | 1.154701 |
| 0.75 | 1.288754 | 1.294417 | 1.259377 | 1.264911 |
| 1.00 | 1.248070 | 1.253314 | 1.408296 | 1.414214 |

— converging monotonically from below with visible `O(n^{-1/2})` corrections
(the `γ=1` column is the proved case and shows exactly the `-\frac13n^{-1/2}`
of Ramanujan's `Q`).

> **Status:** the `γ=1` endpoint is **PROVED** (Prop. 7.1, modulo one classical
> citation for `Q(n)`'s asymptotics). The `γ\in(0,1)` family (7.1) is
> **NUMERICALLY CHARACTERIZED** with a derived mechanism; making it a theorem
> requires concentration for `R` around `γj` and a Riemann-sum control on
> `\frac1n\sum_J\prod(\cdot)` uniformly in the regime — routine in style, not
> carried out here, and **not claimed**.

### 7.3 Where the global sup sits

`probe_large_c.log`, exhaustive over `c\in[0,n]`:

| `n` | 125 | 250 | 500 | 1000 | 2000 | 4000 |
|---|---|---|---|---|---|---|
| `\sup_{[0,n]}\lvert Δ_n\rvert` | 0.030239 | 0.021909 | 0.015759 | 0.011278 | 0.008043 | 0.005721 |
| argmax `c^*/n` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `\sqrt n\cdot\sup` | 0.338088 | 0.346416 | 0.352386 | 0.356650 | 0.359686 | 0.361843 |

The sup over the natural range is attained at the **right endpoint `c=n`**, and
`\sqrt n\sup_{[0,n]}|Δ_n| \to a^* = 0.3670872…` (two-point Richardson on the
consecutive pairs: `0.366799, 0.366944, 0.367016, 0.367050`, the last within
`3.7\cdot10^{-5}` of `a^*`; `extrapolate.log`) — the
same constant as in §6.3, and for the same reason (both are the `K\approx n`
boundary). Under Definition 1's `q=\min(c/n,1)` convention `φ(n,\cdot)` is
constant beyond `c=n` while `φ_∞\downarrow0`, so the sup over **all** `c\ge0` is
`\lim_{c\to\infty}Δ_n(c)=φ(n,n)=Q(n)/n\sim\sqrt{π/2}\,n^{-1/2}` — still `\to0`,
consistent with Teorema C, at the same `Θ(n^{-1/2})` order.

> **Summary of Question 2.** `\;φ(n,c)` remains well-defined and bounded for all
> `c` at fixed `n` (it is a probability); `φ_∞(c)\to0` and `φ(n,c)` follows it
> down at the same `n^{-1/2}` order, so **no absolute divergence occurs
> anywhere** — the convergence is uniform on `[0,\infty)` (Teorema C), at rate
> `Θ(n^{-1/2})` (numerically characterized). What genuinely fails is the
> **relative** approximation: `φ(n,c)/φ_∞(c) = 1+\frac c{4n}+O((c/n)^2)`, so the
> limit law is relatively accurate exactly when `c=o(n)` and provably fails
> (ratio `\sqrt2`) at `c=n`. There is no regime, within the model's own
> parameter range, where the limit *breaks down in absolute terms*.

---

## 8. What this closes, and what it does not

**Closes (subject to adversarial review).** Item **(iv)** of the "o que
permanece aberto" list of `THEOREM.md` Estágio 6/7/8 — the locally-uniform-in-`c`
version of Teorema 3 — **affirmatively and unconditionally**, and in a stronger
form than the item asks (globally uniform, not merely locally). It also answers
the second half of `DISC-DEC-047`(a)'s brief ("caracterizar o que acontece
quando `c` cresce junto com `n`") with a sharp absolute/relative dichotomy, one
proved endpoint, and a quantified profile.

**Does not close.**

1. **An explicit rate for Teorema A.** Available only modulo (U') (§6.2–6.3).
   The exact obstruction is named: *uniformity in `K` of Estágio 7's `1/n`
   rate*. Nothing in Estágios 5–8 provides it, and Estágio 7 explicitly
   disclaims it.
2. **Teorema E (both the pointwise `n\,Δ_n\to e` and its uniform strengthening)**
   carries the domination gap of §5.6. **[Correção pós-adversarial,
   2026-08-23, F-1: a lacuna não é "um limitante geométrico de constante
   explícita" — Estágio 8 Prop. 6 prova o limitante, não a geometricidade
   qualitativa de `M_K`, que é o que de fato falta; ver a correção completa
   em §5.6 acima.]** **[Adendo datado, 2026-08-23, DISC-DEC-052: este item
   FECHADO — a geometricidade qualitativa de `M_K` foi provada
   (`mk_geometricity_attempt/ATTEMPT.md`, onda 12, SOUND adversarialmente).
   Teorema E é agora incondicional, ambas as versões. Ver o adendo completo
   em §5.6 acima e `THEOREM.md` "Estágio 11".]**
3. **The `γ\in(0,1)` scaling law (7.1)** is characterized, not proved (§7.2).
4. **`\sqrt n\sup_{[0,n]}|Δ_n|\to a^*`** and the `a^*` value: numerics +
   heuristic, not proved.
5. Everything else in the archive's open list — the all-orders general-`K`
   closed form (item (i)) and Conjecturas 1–2 (item (v)) — is untouched here
   and unaffected in either direction.

**Prior-document review.** No error, gap, or overclaim was found in any
catalogued document while working. Every archive value the engines could reach
was reproduced exactly (§2.3), including Estágio 7's `c_K` and the three
independently-derived `φ_n^{(K)}` families. **One scope note, not a defect:**
`THEOREM.md` Definition 1 calls the `n\le c` convention *"immaterial in the
limit"* — true for Teorema 3 and for Teorema A here, but it is **material** for
the global statement of Teorema C (it is what makes `φ(n,\cdot)` constant on
`[n,\infty)`), so Teorema C is stated with that convention named explicitly.
Flagged for the orchestrating session's attention; **this document does not
edit `THEOREM.md`.**

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | The `(j,R)` orbit chain (2.1) computes `φ(n,c)` exactly; its conditional version computes `φ_n^{(K)}` | **PROVED** (§2.1–2.2, derivation from Definition 1) and **NUMERICALLY VERIFIED** against 7 independent archive/classical checks + raw Monte Carlo, zero mismatches |
| 2 | **Lema 3.1**: `\|φ(n,c)-φ(n,c')\|\le\|c-c'\|`, uniformly in `n` | **PROVED**, one-line monotone coupling on Definition 1 |
| 3 | **Lema 3.2**: `∂_cφ(n,c)=E[φ_n^{(J+1)}-φ_n^{(J)}]`, `J\sim\mathrm{Bin}(n{-}1,c/n)` | **PROVED**; additionally verified as an exact `sympy` identity for `n=2,\dots,8` |
| 4 | Sharp Lipschitz constant `= φ_n^{(0)}-φ_n^{(1)} = \frac13-\frac1{3n^2}` | **NUMERICALLY VERIFIED** (exact `Fraction`, `n=2,\dots,64`); needs monotonicity in `K`, not proved |
| 5 | **Teorema A**: `\sup_{[0,C]}\|φ(n,\cdot)-φ_∞\|\to0` for every fixed `C` | **PROVED, unconditional** — Teorema 3 (Estágio 6) + item 2 + grid argument; explicit finite-`n` inequality with `4C/(3M)` given |
| 6 | **Lema 4.1** tail bound and **Corolário 4.2** (`\sup_{c\ge C_0}φ(n,c)\le ω(C_0)+4/n`, uniform in `n\ge C_0`) | **PROVED**, elementary; **NUMERICALLY VERIFIED**, 0 violations in 22 cells, looseness factor 2.5–4.2 |
| 7 | **Teorema C**: `\sup_{c\in[0,\infty)}\|φ(n,c)-φ_∞(c)\|\to0` | **PROVED, unconditional** (under Definition 1's own `q=\min(c/n,1)` convention, named explicitly) |
| 8 | **Lema 5.1**: `B_n(c)=\int_0^1[(1-ct^2/n)^n-e^{-ct^2}]dt \le 0`, exactly | **PROVED**; verified to `1.6\cdot10^{-17}` against direct summation |
| 9 | **Teorema D**: `n([c^j]φ(n,\cdot)-[c^j]φ_∞)\to e_j`, with `e_j` given by a finite `c_K`/`φ_K` alternating sum | **PROVED**, unconditional given Estágio 6/7; no interchange of limits (finite sums) |
| 10 | `e_j=[c^j]e(c)` for `j=0,\dots,8`, both computed exactly and independently | **PROVED** for those `j` by exact symbolic/rational agreement; `e_0=e_1=0` cross-checks `THEOREM.md` Cor. 4.3 |
| 11 | **Proposição 5.2**: `e_j=(-1)^{j+1}\frac{(j-1)^2}{2(2j-1)j!}`; `e(c)=\frac12\int_0^1\frac{1-(1+ct^2+c^2t^4)e^{-ct^2}}{t^2}dt`; `e(c)=\frac{\sqrt{πc}}8-\frac12+O(\sqrt c\,e^{-c})` | **PROVED** (resummation + three Gamma integrals); coefficient identity additionally machine-checked symbolically `j=1,\dots,11`; `\int_0^\infty=\sqrtπ/4` to 20 digits |
| 12 | **Teorema E**: `n\,Δ_n(c)\to e(c)` and `n\sup_{[0,C]}\|Δ_n\|\to\sup_{[0,C]}\|e\|` | **PROVED-MODULO-[an explicit-constant geometric bound on `D_r(b)`]** (§5.6); **NUMERICALLY VERIFIED** to 4–5 digits at `n=10^5`, 7 values of `c` and 7 values of `C`, argmax location included — **[Correção pós-adversarial, 2026-08-23, F-1: o rótulo PROVED-MODULO está correto, mas a lacuna nomeada está errada — não é a constante explícita do limitante geométrico que falta, é a prova escrita da geometricidade *qualitativa* de `M_K` (Estágio 8 Prop. 6 prova apenas o limitante, não a geometricidade). Ver §5.6.]** **[Adendo datado, 2026-08-23, DISC-DEC-052: status atualizado para PROVADO, incondicional — a geometricidade qualitativa de `M_K` foi provada e verificada adversarialmente (`mk_geometricity_attempt/`, onda 12). Ver §5.6.]** |
| 13 | The uniform-on-`[0,C]` error constant grows like `\sqrt C`: `\sup_{[0,C]}\|e\|\sim\sqrt{πC}/8` | **PROVED** given item 11 (a statement about `e` alone); its identification *as* the limiting error constant inherits item 12's status |
| 14 | **Lema 6.1**: `0\le e^{-x}-(1-x/n)^n\le\frac{x^2}ne^{-x}` for `n\ge4`, `0\le x\le n`; `κ_B=\sup c^2I_2(c)=0.280480169025…` | **PROVED**; scanned at `1.4\cdot10^4` points, max ratio `0.564` |
| 15 | **Teorema B**: `(U'_a)\Rightarrow \sup_{[0,C]}\|Δ_n\|\le(a\sqrt C+κ_B)/n` | **PROVED given (U'_a)**; the bound with `a=1` holds with margin `\ge4` everywhere in the numerical scan |
| 16 | **(U')**: `\|φ_n^{(K)}-φ_K\|\le a\sqrt K/n` uniformly in `0\le K\le n`, sharp `a^*=\sqrtπ(1/\sqrt2-1/2)=0.3670872…` | **NUMERICALLY CHARACTERIZED** (`K` to `16384`, max over `n` always at `n=K{+}1`, ratio `\to a^*` from below); **OPEN** as a theorem — it is exactly "Estágio 7's rate, uniformly in `K`", which Estágio 7 explicitly does not claim |
| 17 | `K\mapstoφ_n^{(K)}` is non-increasing | **NUMERICALLY VERIFIED** (exhaustive in `K`; exact `Fraction` for all `K` at `n=2,\dots,9`); not proved, and **not used** in any proof here |
| 18 | **Proposição 7.1**: `φ(n,n)=Q(n)/n` exactly; `φ(n,n)/φ_∞(n)\to\sqrt2`; `\|φ(n,n)-φ_∞(n)\|\sim a^*n^{-1/2}\to0` | **PROVED** (exact identity here; `Q(n)\sim\sqrt{πn/2}` **CITED**, Knuth TAOCP I §1.2.11.3 / Flajolet–Odlyzko) |
| 19 | **(7.1)**: for `c=γn`, `φ(n,c)/φ_∞(c)\to\sqrt{2/(2-γ)}`, i.e. `c_{\rm eff}=c(1-c/2n)`; relative error `\approx c/(4n)` | **NUMERICALLY CHARACTERIZED**, mechanism derived, endpoint `γ=1` proved (item 18), and independently cross-derived from item 11's `e(c)\simeq\sqrt{πc}/8`; **not proved** for `γ\in(0,1)` |
| 20 | `\sup_{[0,n]}\|Δ_n\|` is attained at `c=n` and `\sqrt n\sup\to a^*`; `\sup_{c\ge0}\|Δ_n\|=φ(n,n)=Θ(n^{-1/2})` | **NUMERICALLY CHARACTERIZED** (`n\le4000`, exhaustive sweep); the `\to0` part is item 7 (PROVED) |
| 21 | Independent adversarial re-verification of this document | **NOT PERFORMED** — that is the orchestrating session's job, per the standing discipline of this lineage. **This document must not be catalogued before it happens.** |

---

## 10. Honest verdict

**Outcome: (a) — the target question is fully answered, affirmatively, and
unconditionally.** The convergence of Teorema 3 *is* uniform on every compact
`[0,C]`, and the proof is genuinely short: the only missing ingredient in the
archive was equicontinuity in `c`, and Lema 3.1's monotone coupling supplies it
uniformly in `n` in one line. The result then extends past compacts to the whole
parameter range (Teorema C) via a second elementary lemma proved directly on the
orbit exploration. **Neither theorem uses any part of the `F_r/G_r/H_r`
machinery** — which is worth saying plainly, because the brief anticipated that
the error-constant ladder would be the route, and it turned out not to be the
one that works. (The ladder *is* what gives the exact profile `e(c)`, §5, but
that is the quantitative refinement, not the qualitative theorem.)

Three things stop this from being a clean sweep, and they are stated as such
rather than smoothed over:

- **No explicit rate is proved.** Teorema A gives uniformity with no bound in
  `n`. The explicit bound exists (Teorema B, `\sup_{[0,C]}|Δ_n|\le(a\sqrt
  C+0.2805)/n`) but rests on (U'), which is the statement that Estágio 7's
  `1/n` rate is uniform in `K` — precisely what Estágio 7 declines to claim.
  The numerics for (U') are strong (max over `n` always at `n=K+1`, ratio
  converging to an identified constant `a^*` with an explained mechanism), and
  I record them as evidence, not as proof.
- **Teorema E carries one named interchange-of-limits gap** — real, and not
  papered over, but **[Correção pós-adversarial, 2026-08-23, F-1]** it does
  *not* reduce to an explicit-constant geometric bound on `D_r(b)`: Estágio 8
  Prop. 6 proves the improved constants satisfy the Target Theorem, not that
  they are geometric (its own §6.3 marks the rate NUMERICALLY CHARACTERIZED
  with no geometricity proof supplied). The actual missing ingredient is a
  written proof of *qualitative* geometric growth of `M_K`. Everything I could
  make unconditional there — the coefficient-wise Teorema D, and the exact
  closed forms of `e` — I did.
- **The `γ\in(0,1)` scaling law is not proved**, only characterized, with the
  endpoint `γ=1` proved separately. I have not tried to dress the heuristic up:
  it needs concentration for `R` and a uniform Riemann-sum control that I did
  not carry out.

On the second question the honest answer is more interesting than a yes/no:
**nothing diverges, but the limit law does degrade, and the degradation is
relative rather than absolute, with a clean profile.** `φ(n,c)` stays a
probability, `φ_∞(c)` decays like `c^{-1/2}`, and the finite-`n` object tracks it
down to `0` — the absolute error is `Θ(n^{-1/2})` even at the extreme `c=n`, so
uniform convergence survives everywhere. But the *ratio* tends to
`\sqrt{2/(2-c/n)}`, provably `\sqrt2` at `c=n`, so the limit law is a faithful
*relative* approximation exactly on the range `c=o(n)`. The mechanism is
identified and elementary: in the discrete model the orbit is killed both by a
reroute landing on the visited path *and* by the permutation step landing on a
severed tail, and those two hazards sum to `γ(2-γ)` rather than the continuum's
`2γ` — equivalently, the finite-`n` model is the continuum model at the
renormalized rate `c(1-c/2n)`.

**Independent adversarial review is required before any of this is catalogued.**
The central positive claims (Teorema A, Teorema C, and the closed form of `e`)
are of real substance, and this document integrates, promotes, or closes
nothing. `THEOREM.md`'s open-item list, `TEST_QUEUE.yaml`, the
`DECISION_LEDGER.yaml`, and every sibling document remain exactly as they were.

> **[Adendo pós-adversarial, 2026-08-23 — demais nits de
> `adversarial/REFEREE_REPORT.md` §10, não corrigidos individualmente no
> corpo do texto acima por serem cosméticos e não afetarem nenhuma
> conclusão.]** F-5: "monotone coupling" (Scorecard linha 2, §10) é
> defensável (os *marcadores* `ξ` são acoplados monotonamente) mas lido ao
> lado de §3.1(ii) ("not pointwise-monotone") soa contraditório — deveria
> ler "monotone in the marks". F-8: o contraexemplo de §3.1(ii) mostra que
> a **contagem** de pontos cíclicos não é monótona, não que o evento
> `{1 cíclico}` não é — o referee supre um contraexemplo mais forte que
> mostra a não-monotonicidade do evento em si (mesma conclusão, nada
> depende disso). F-9: "computed exactly" para `κ_B` (Executive Summary
> item 4) deveria ler "computed to high numerical precision" — é um valor
> numérico de alta precisão de um supremo transcendente, não uma forma
> fechada. F-10: os "`C_0`-tail values" de §4.1 são o limitante de Lema 4.1
> otimizado em `J`, não `ω(C_0)` nem o sup verdadeiro — vale uma frase
> esclarecendo. F-11: "uniformly in `n`" (Executive Summary item 2) deveria
> ler "uniformly in `n\ge C_0`" — Corolário 4.2 e Teorema C já dizem isso
> corretamente. F-12: a dominação `M_K\le5K/4+D_K(0)` exige `n\ge K+1`,
> excluindo o termo `K=n` da soma — inofensivo (`\le(c/n)^n\cdot n\to0`),
> mas merece uma cláusula. F-13: o `n\ge4` do Lema 6.1 é artefato da prova
> (de `1-u\ge1/2`); `n=2,3` também valem numericamente. Nenhum destes
> afeta Lema 3.1, Teorema A, Lema 4.1, Corolário 4.2 ou Teorema C.

---

## 11. Files, reproducibility

All scripts are in this directory; all use exact `fractions.Fraction` /
`sympy.Rational` where a claim says "exact", `mpmath` at 40 digits for `φ_∞` and
the `e(c)` quadratures, and `numpy.float64` only for large-`n` sweeps whose
precision is audited in `probe_pointwise.log`.

| file | what it does | runtime |
|---|---|---|
| `chain.py` / `chain_selftest.log` | the two exact engines (§2) + the full validation table of §2.3 | ~30 s |
| `chain_multi.py` / `chain_multi_selftest.log` | engine vectorised over a grid of `c`; untruncated-vs-truncated audit (`0.000e+00`) | ~40 s |
| `mc_check.py` / `mc_check.log` | Monte Carlo of the **raw** Definition-1 model vs the engines (the one use of randomness; seed in §0) | ~20 min |
| `ecoef.py` / `ecoef.log` | `e(c)` from (5.1); its two parts; small-`c` and large-`c` behaviour; minimiser and zero | ~1 min |
| `ecoef2.py` / `ecoef2.log` | the three representations of `e(c)` agree; the exact coefficient closed form `j=1..11`; `\int_0^\infty=\sqrtπ/4` | ~2 min |
| `probe_pointwise.py` / `.log` | float64/longdouble/exact precision audit; `n\,Δ_n(c)\to e(c)` at 7 values of `c`, `n\le102400`; exact `[c^2]` check | ~15 min |
| `probe_uniform.py` / `.log` | the §5.6 table: `n\sup_{[0,C]}|Δ_n|\to\sup_{[0,C]}|e|`, argmax tracking, grid-resolution control, Teorema B margin | ~40 min |
| `probe_tail.py` / `.log` | Lema 4.1 checked against the exact chain (0 violations) and the uniform-in-`n` `C_0`-tail | ~2 min |
| `probe_K.py` / `.log` | Estágio-7 `c_K` reconfirmation; the (U)/(U') scan; monotonicity in `K` incl. exact `n=2..9` | ~5 min |
| `probe_K_sharp.py` / `.log` | (U') pushed to `K=16384`; the sharp constant `a^*` | ~10 min |
| `probe_large_c.py` / `.log` | §7: the `γ` regime, the global sup and its argmax, `φ(n,n)` vs `\sqrt{π/2}` | ~10 min |
| `probe_taylor.py` / `.log` | `e_j` two independent exact ways, `j=0..8`; finite-`n` exact Taylor convergence | ~2 min |
| `probe_exact.py` / `.log` | exact/symbolic checks of Lema 3.2, the sharp Lipschitz constant, Lema 5.1, Lema 6.1, `κ_B`, plus rational anchors for `φ(n,c)` | ~2 min |
| `extrapolate.py` / `.log` | Richardson extrapolation of the two sequences converging to `a^*` (transcribed inputs, nothing recomputed) | instant |

To reproduce, from this directory: `python3 chain.py`, `python3 chain_multi.py`,
`python3 ecoef.py`, `python3 ecoef2.py`, `python3 probe_taylor.py`,
`python3 probe_exact.py`, `python3 probe_tail.py`, `python3 probe_K.py`,
`python3 probe_K_sharp.py`, `python3 probe_pointwise.py`,
`python3 probe_large_c.py`, `python3 probe_uniform.py`, `python3 extrapolate.py`,
and (slow, random)
`python3 mc_check.py`.
