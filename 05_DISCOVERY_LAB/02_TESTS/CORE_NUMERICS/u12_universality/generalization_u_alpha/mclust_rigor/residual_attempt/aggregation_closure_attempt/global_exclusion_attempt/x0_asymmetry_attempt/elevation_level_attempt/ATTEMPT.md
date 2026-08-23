# ATTEMPT — the level of the closure-hazard elevation, derived

**Wave 10, `DISC-DEC-045`, front (a) `MCLUST-ELEVATION-LEVEL-ATTEMPT`**
(continuation of the `MCLUST-RESIDUAL-RIGOR` line, `DISC-DEC-033`).

**Scope, fixed by mandate.** This document and the files in this subfolder
(`elevation_level_attempt/`) are a NEW annex extending
`x0_asymmetry_attempt/ATTEMPT.md` and `x0_asymmetry_attempt/adversarial/REFEREE_REPORT.md`
without modifying either. No file in `x0_asymmetry_attempt/`,
`x0_asymmetry_attempt/adversarial/`, `global_exclusion_attempt/`,
`aggregation_closure_attempt/`, `residual_attempt/` or `mclust_rigor/` was
touched (only read). `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `README.md`/`README_*.md`, `PROOF_DEPENDENCY_MAP.md`
and `tamesis-cycle-survival/` were not touched — integration is the
orchestrating session's business, not this front's. No git commit was created.
Nothing under `u12_universality/theorem/` was touched. **The classification
M-CLUST(b) ∈ U_{1/2} in the n→∞ limit (∀ fixed b) is not questioned anywhere
below** — everything here is about the *finite-n correction formula*, exactly
as in the four documents this one extends. (Written in English, matching
`DERIVATIONS.md` and the referee report that established the formula of record
this front builds on.)

**Target, quoted from the mandate and from both sources that localised it.**
`x0_asymmetry_attempt/ATTEMPT.md` §5.3 item 3:

> "O excesso lambda_bar/P_lead − 1 é +0,9% a +5,6% e parece crescer com b …
> **Ajustar uma [lei] é exatamente o que o mandato desta linha proíbe apresentar
> como derivação, e não é feito aqui.** Fica registrado como o alvo mais bem
> localizado que esta linha já teve."

and `adversarial/REFEREE_REPORT.md` §5.6 / §10(C):

> "This is the residual, essentially in full, and it lives entirely in `φ_V4` —
> i.e. in the elevation model. … That is where the next front belongs."

---

## 0. Discipline

**Read in full before writing a single line of code:** `DISC-DEC-045`
(`00_GOVERNANCE/DECISION_LEDGER.yaml`, lines 2686–2740);
`residual_attempt/ATTEMPT.md` (§0–9);
`aggregation_closure_attempt/ATTEMPT.md` (§0–10);
`global_exclusion_attempt/ATTEMPT.md` (§0–7);
`x0_asymmetry_attempt/ATTEMPT.md` (§0–9);
`x0_asymmetry_attempt/adversarial/REFEREE_REPORT.md` (§0–10, with §4 and §5.6
read line by line as instructed);
`generalization_u_alpha/DERIVATIONS.md` §0–3.6 and §6;
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` §0–6 (needed because §6 below has to
say precisely which of its two corrections survives this front and which is
re-expressed).

**Implementation.** Every script in this subfolder is written from scratch from
the mechanism as stated in the primary sources. Nothing is imported or copied
from `ualpha_sim.py`, `mclust_validate.py`, `mclust_decompose.py`,
`mclust_walk_diagnostic.py`, `mclust_residual_v3/v4/v5.py`,
`mclust_residual_validate.py`, `mclust_aggregation_validate.py`,
`mclust_global_formula.py`, `mclust_global_validate.py`,
`global_exclusion_walk_measure.py`, `x0_asym_formula.py`,
`x0_asym_candidate.py`, `x0_asym_validate.py`, `x0_asymmetry_walk_measure.py`,
`x0_asym_analysis.py`, or any `ref_*.py` of the `adversarial/` review. The nine
scripts of this front import only one another (`elev_formula.py` and
`elev_mc.py` → `elev_pool_probe.py`, `elev_triage_recorded.py`,
`elev_analysis.py`; `elev_validate.py`, `elev_reduction.py`,
`run_pool_probe.py`, `rebuild_reduction.py` are drivers), which is the practice
all four predecessor documents already record for scripts of one front.

**Seeds** — all fresh, never used anywhere in this lineage (checked against the
list in the mandate and by `grep` over the archive):

| seed | use |
|---|---|
| `SeedSequence(20260823800)` | `elev_mc.py selftest` (§7.0) |
| `SeedSequence(20260823801)` | smoke test of `elev_pool_probe.py` (400 walks, discarded) |
| `SeedSequence(20260823810–817)` | `elev_pool_probe.py`, the eight T1/T2 cells (§7) |
| `SeedSequence(20260823820–843)` | `elev_validate.py`, the 24 fresh-grid cells (§9) |
| `SeedSequence(20260823850–867)` | `elev_reduction.py`, the 18 reduction-test jobs (§8) |

None of `20260822018`, `918302033`, `720330339`, `20260822901–904`,
`20260822910–911`, `20260822941–945`, `20260823700–707` was reused.

**Reuse, explicitly labelled** (formula constants re-transcribed from their
stated closed forms — not code):

* `ρ = 1−(1−c/n)^b`, `ρ_start = (c/n)(1−ρ)` — wave 4 §1, exact.
* `q_CLUST(s) = s/(1−ρ)`, un-clipped — wave 4 §3.
* `P_lead = 1/(1−ρ)` (φ_CAND) and `P_exact = (1−c/n)^{−(b−1)}` (φ_CAND5).
* the closed form `H(t) = 1 − (2/(2−P))(1−t)^P + (P/(2−P))(1−t)²`, and
  `φ_V4`, `T`, `φ_runstart`, `eps_ref`, `φ_EPSR` — `adversarial/REFEREE_REPORT.md`
  §1(i) and §4.1. My re-implementation of `φ_CAND` and `φ_EPSR` reproduces the
  referee's own χ² values on all six recorded grids to 3 significant figures
  (§10), which is the cross-check that the re-transcription is faithful.
* Monte-Carlo means **already recorded** by earlier fronts are used as *cheap
  triage* (§10), always labelled as such. The decision on the candidate (§9) is
  taken with new simulation and new seeds.

**Order of work, which matters for the no-curve-fitting rule.**
`DERIVATION_PREREG.md` — containing the derivation of §2–§5 below, the formula
`φ_RED` with every constant fixed, and the four pre-registered tests with their
refutation criteria — was written and saved **before any simulation of this
front was run** (file mtime, and the `PROGRESS.log` line recording it, precede
every `*.json` and every simulation log in this folder). No functional form
below was chosen because it reduced χ²; §11 states plainly the one place where
prior knowledge of the predecessors' numbers guided *which* mechanism feature I
went looking for.

---

## 1. The state of the line, and the exact object in question

The formula of record (`DISC-DEC-044`) is

```
φ_EPSR  = (1−ρ)·φ_V4 + ρ·eps_ref
eps_ref = (ρ_start/ρ)·φ_runstart + (1 + c·T)/((1−ρ)·n)
φ_V4    = ∫₀¹ P (1−t)^{P−1} e^{−cH(t)} dt ,    P = P_lead = 1/(1−ρ)
```

Two independent measurements (`x0_asymmetry_attempt/ATTEMPT.md` §5.3, by a
Horvitz–Thompson estimator on a walk-level simulator; and
`adversarial/REFEREE_REPORT.md` §5.6, by direct measurement of
`φ(cyclic | x₀ ∉ R)` on the whole functional graph with no walk at all) agree
that the entire residual of `φ_EPSR` lives in `φ_V4`, i.e. in the **elevation
model**, and that the true elevation exceeds `P_lead` by an amount that grows
with `b` and `ρ`.

Every formula this lineage has produced — `φ_NEW`, `φ_CAND`, `φ_CAND5`,
`φ_GLOBAL`, `φ_EPS`, `φ_EPSR` — assumes the elevation is a **constant** `P`,
independent of the traversed mass, and differs only in which constant.
`global_exclusion_attempt/ATTEMPT.md` §2.2 proved it does not depend on *arc
depth*; `x0_asymmetry_attempt/ATTEMPT.md` §4.4 found no dependence on *target
identity*; §4.4 also reported, without pursuing it, "uma leve subida em s alto
presente nas DUAS populações igualmente" — a slight rise at high traversed
mass, present in both target populations equally.

**That remark is the whole answer.** The elevation is not a constant. §2–§4
derive what it is; §7 measures it; the constant-`P` hypothesis is refuted at the
mechanism level by χ² = 2473 against 51 (§7.3).

---

## 2. Where `P` comes from, re-derived: expose `R` first

Generate the mechanism in this order.

1. Reveal the **seed set** `Σ` (i.i.d. marks, independent of `π`).
2. For every seed `s`, reveal `π(s), π²(s), …, π^{b−1}(s)` — `b−1` forward
   `π`-queries, following already-revealed values where blocks overlap. **After
   this step `R` is completely determined** as a subset of `[n]`.
3. What is left of `π` is a uniform bijection between the un-queried arguments
   and the unused images:
   ```
   A_rem = [n] \ { π^j(s) : s ∈ Σ, 0 ≤ j ≤ b−2 }
   U_rem = [n] \ { π^j(s) : s ∈ Σ, 1 ≤ j ≤ b−1 }
   ```
   (the same sequential-exposure fact `aggregation_closure_attempt/ATTEMPT.md`
   §3.1 uses, applied globally instead of locally).

Two exact densities follow:

> **[Correção pós-adversarial, 2026-08-23.]** (2.1)–(2.2) NÃO são exatas
> como afirmado: assumem que os `b−1` pontos `π^{−1}(y),…,π^{−(b−1)}(y)`
> são distintos, o que falha em ciclos-π de comprimento `<b−1`. O
> referee derivou as densidades verdadeiramente exatas (soma sobre o
> comprimento `L` do ciclo, ponderada por `1/n`) e mostrou que o erro
> relativo é `O(b²c/n²)` — `≤0,06%` na grade padrão (onde é de fato
> desprezível), mas `+0,6%` a `+1,2%` em quatro das seis células
> "extremas" da §9, exatamente as células usadas para argumentar que o
> resíduo não cresce mais com `b`. Confirmado por Monte Carlo a 4,2σ
> contra (2.1) em `b=800,c=100,n=65536`. Ver
> `adversarial/REFEREE_REPORT.md` §3.2.

```
P(y ∈ U_rem)      = P(no seed among π^{−1}(y),…,π^{−(b−1)}(y)) = (1−c/n)^{b−1}
                  = (1−ρ)/(1−c/n)                                          (2.1)
P(y ∈ R ∩ U_rem)  = (c/n)(1−c/n)^{b−1}                                     (2.2)
```

The walk takes a `π`-step only from a point `x ∉ R` (from a point of `R` it
reroutes), and `x ∉ R ⟹ x ∈ A_rem`. Hence **at the first step `π(x)` is
uniform on `U_rem`**, so the per-target density is
`1/|U_rem| = (1−c/n)^{−(b−1)}/n = P_exact/n`.

That is *exactly* the wave-8 lemma — derived there by a different route and
validated at production scale (`aggregation_closure_attempt/ATTEMPT.md` §4.3,
χ² = 1.93 for 4 cells). Reproducing it is the necessary sanity condition before
using this exposure for anything new. Verified independently here
(`elev_mc.py selftest`): `|U_rem|/n` matches `(1−c/n)^{b−1}` to within 1.2 sem
in every cell tested, `π(R^c) ⊂ U_rem` holds identically on 20 instances at
n = 65536, and `π(R^c)` meets `R` only at run starts (wave 4's shadowing lemma,
re-verified).

---

## 3. The piece that was missed: the pool keeps shrinking *inside* `U_rem`

`P_exact` is the elevation **at `t = 0`**. The lineage then froze it.

But the walk consumes images out of `U_rem`, not out of `[n]`:

* every normal `π`-step is taken from a visited point of `R^c` and consumes
  exactly one value of `U_rem` (its image, which is either another `R^c` point
  or a run start — both are in `U_rem`);
* the number of normal steps taken by the time the walk has visited `t·n`
  points is the number of visited `R^c` points, `t_c·n`, and
  `t_c = t − O(c t/n)` (the visited points of `R` are the run starts hit,
  ≈ `c t`, plus the chain points, ≈ `c t ρ/(1−ρ)`).

Therefore, at traversed mass `t`,

```
|U_rem(t)| = n (1−ρ)/(1−c/n) − t_c n ,      hazard per live target = 1/|U_rem(t)|
```

and, **relative to the master formula's own density `1/((1−t)n)`**, the
elevation is

```
       λ(t) = (1−t) / [ (1−ρ)/(1−c/n) − t_c ]   ≈  (1−t)/(1−ρ−t)            (3.1)
```

`λ(0) = P_exact` — the lineage's value — and `λ` **increases with `t`**, because
the pool `(1−ρ)n` is smaller than `n` while the consumption is the same. That is
the whole excess. Its relative growth rate is `d ln λ/dt |₀ = ρ/(1−ρ)` per unit
mass, so the excess grows with `ρ`; and at fixed `ρ` the walk survives to larger
`t` when `c` is smaller, i.e. when `b` is larger at fixed `bc/n` — which is
exactly the "grows roughly with `b`" pattern both predecessor measurements
reported.

**Why four fronts walked past it.** `residual_attempt/ATTEMPT.md` §2.2 *did*
try the subtractive hazard `1/(1−s−ρ)` and discarded it, correctly for what it
tested — but that was §2.2, written **before** §6 of the same document
discovered the `x₀ ∈ R` dilution factor `(1−ρ)`, and the two were never put
together. `global_exclusion_attempt/ATTEMPT.md` §1 then concluded that the
inherited `(1−t)` already *is* the global pool — true for M-U, where the pool is
all of `[n]`, but for M-CLUST(b) the pool is `U_rem`, smaller by `ρ` — and its
§2.2 accordingly looked only for a correction of order `(b−1)/n` (0.1–0.4%, too
small), rather than one of order `ρ·t/(1−ρ)` (2–5%, the right size).
`aggregation_closure_attempt/ATTEMPT.md` derived the correct `t = 0` value and
substituted it as a constant.

---

## 4. The reduction: M-CLUST(b) conditioned on `x₀ ∉ R` **is** M-U

(3.1) is not an isolated patch. Once `R` is exposed the whole conditioned
process collapses onto a smaller M-U.

**Claim.** Conditionally on `x₀ ∉ R`, the exploration of the `f`-orbit of `x₀`
in M-CLUST(b) at `(c, n)` is, in the continuum description this lineage uses,
*the same process* as M-U at

```
        n' = (1−ρ) n ,       c' = c(1−ρ) ,       c'/n' = c/n .              (4.1)
```

Ingredient by ingredient, each checked against what the lineage already proved:

| ingredient | M-CLUST(b) at `(c,n)`, conditioned on `x₀ ∉ R` | M-U at `(c′,n′)` |
|---|---|---|
| world | `R^c`, size `(1−ρ)n` | `[n′]`, size `n′` |
| image pool | `U_rem`, size `n(1−ρ)/(1−c/n)` (2.1) | `[n′]`, size `n′/(1−c′/n′)` |
| pool at mass `u` | `(pool) − u·(world)` | `(pool) − u·(world)` |
| per-target closure hazard | `1/[(1−c/n)^{−1} − u]` per unit collapsed mass | `1/[(1−c′/n′)^{−1} − u]` |
| reroute rate per normal step | `(2.2)/(2.1) = c/n`, constant — this **is** wave 4's "encounter rate `c` per unit mass" | `c′/n′` |
| kill law | chain kills w.p. `t/(1−ρ) = u` | draw kills w.p. `u` |
| surviving reroute | creates exactly one arc start | idem |
| structurally unclosable arc starts | a fresh arc start `D ∉ R` lies outside `U_rem` w.p. `c/n` (it is the successor of a run end) | idem, w.p. `c′/n′` |

Every row matches identically once `c′/n′ = c/n`, i.e. `n′ = (1−ρ)n`,
`c′ = c(1−ρ)`. Hence, in the continuum limit,

```
        φ(cyclic | x₀ ∉ R)  =  φ_U(c(1−ρ))  =  ∫₀¹ e^{−c(1−ρ) u²} du .      (4.2)
```

**Direct algebraic check, without the reduction language.** Put the elevated
hazard `1/(A−t)` with `A = 1−ρ`, the reroute rate `c` per unit `t` (wave 4's
value, unchanged), and `q_CLUST(s) = s/(1−ρ)` (wave 4's value, unchanged) into
the master formula. Then `(1−q(s))/(A−s) ≡ 1/A`, so
`H(t) = t − (A−t)·t/A = t²/A`, and

```
φ_cond = ∫₀^A [1/(A−t)]·[(A−t)/A]·e^{−ct²/A} dt  =(t=Au)=  ∫₀¹ e^{−cA u²} du .
```

Both of wave 4's ingredients survive intact; only the *coordinate* changes.

---

## 5. The candidate `φ_RED` (derived, no free parameter)

Using the exact total-probability decomposition
`φ = (1−ρ)·φ(cyclic|x₀∉R) + ρ·eps` and the referee's corrected `eps` channels
(`REFEREE_REPORT.md` §4.1) re-expressed through (4.1) — i.e. with `P → 1`,
`c → c′`, `H(t) → u²`, so that `φ_runstart → T_U(c′)` and
`E[#f-draws] → (1 + c′T_U(c′))/(1−ρ)`:

```
φ_U(c′) = ∫₀¹ e^{−c′u²} du          = (√π/(2√c′)) erf(√c′)
T_U(c′) = ∫₀¹ (1−u) e^{−c′u²} du    = φ_U(c′) − (1−e^{−c′})/(2c′)
eps_RED = (ρ_start/ρ)·T_U(c′) + (1 + c′T_U(c′))/((1−ρ)n)
φ_RED   = (1−ρ)·φ_U(c′) + ρ·eps_RED
        = (1−ρ)[ φ_U(c′) + (c/n)T_U(c′) ] + ρ(1 + c′T_U(c′))/((1−ρ)n)        (5.1)
```

Checks (in `elev_formula.py`, `python3 elev_formula.py`): `ρ→0 ⇒ φ_RED → φ_U(c)`
(diff < 5e-10); `φ_RED − (1−ρ)φ_U(c′)` is *exactly* proportional to `c/n` at
fixed `ρ` (measured 1.122e-2 → 1.120e-3 → 1.120e-4 → 1.120e-5 as `c/n` falls by
factors of 10); `λ(0) = P_exact` to machine precision.

**Both correction factors of `φ_RED` vanish as `n → ∞` at fixed `(b,c)`**
(`ρ → 0`), so `φ_RED → φ_U(c)` and **the U_{1/2} classification is untouched**,
exactly as the lineage frames it.

> **[Correção pós-adversarial, 2026-08-23 — SUPERSEDE ESTA FÓRMULA.]**
> `φ_RED` (5.1) usa `c′=c(1−ρ)` na redução §4, que o referee refutou a
> alta precisão (ver adendo em §8/§12 abaixo). A candidata correta,
> recomendada pelo próprio referee como fórmula de registro em seu
> lugar, troca apenas o argumento de `φ_U`/`T_U`:
> ```
> c'' = c(1-c/n)^(b-1) = c(1-rho)/(1-c/n)     [= c / P_exact, constante da onda 8]
> phi_REDB = (1-rho)[ phi_U(c'') + (c/n)T_U(c'') ] + rho(1 + c''T_U(c'')) / ((1-rho)n)
> ```
> `φ_REDB` reduz o χ² pooled de `φ_RED` (64,9 na grade de 24 células
> desta frente) para **46,0**, e no teste-de-redução sem fórmula do
> referee (§8/§12 abaixo, agora completo em 6 células) reduz o χ² de
> 334,6 (convenção `c′`) para **101,4** (convenção `c''`). Continua
> sendo `O(n→∞)`-equivalente: `φ_REDB → φ_U(c)` do mesmo jeito. Ver
> `adversarial/REFEREE_REPORT.md` §11.

---

## 6. Relation to what the lineage already decided — read this before objecting

### 6.1 `φ_U(c(1−ρ))` is numerically `φ_OLD`. This is not a resurrection of the refuted `c_eff`.

`φ_OLD = φ_U(c(1−c/n)^b) = φ_U(c(1−ρ))` is the wave-3 target of
`DERIVATIONS.md` §3.5, which wave 4 refuted with deviations up to −46 %, and
which `residual_attempt/ATTEMPT.md` §2.2 re-derived and discarded again. The
same number reappears here. The difference is precise and it matters:

* **Wave 3's argument** was that the *reroute rate* is depressed to
  `n·ρ_start = c(1−ρ)` per unit mass, with the closure hazard left at `1/(1−t)`
  and the answer read as the **unconditional** `φ`.
* **Wave 4 refuted exactly that** (their §2, "Erro 1"): the rate conditional on
  the walk is `c/n` per step, i.e. `c` per unit mass, **not** `c(1−ρ)`. That
  refutation stands, and this front uses wave 4's rate, not wave 3's.
* **This front's route** keeps the rate at `c` per unit `t` and instead elevates
  the closure hazard to `1/(1−ρ−t)`. The factor `(1−ρ)` then appears through the
  *change of variable* `u = t/(1−ρ)` — the walk lives on a world of mass
  `(1−ρ)`, so `c` events per unit `t` is `c(1−ρ)` events per unit `u`.
* And the answer is the **conditional** probability, to be multiplied by the
  dilution `(1−ρ)` that wave 7 discovered three waves after §2.2 was written.

So wave 3 wrote down the correctly-rescaled process while believing it was the
unrescaled one, and then compared it to the wrong quantity. `(1−ρ)·φ_OLD` and
`φ_OLD` differ by up to a factor 2.5 on this grid; that missing factor is the
whole of wave 3's −46 %.

### 6.2 What this front does NOT overturn

* wave 4's `q_CLUST(s) = s/(1−ρ)` — used unchanged, and it is what makes
  `(1−q)/(A−s) ≡ 1/A` in §4;
* wave 4's encounter rate `c` per unit mass — used unchanged;
* wave 4's shadowing lemma — used, and re-verified in `elev_mc.py selftest`;
* wave 8's aggregation lemma `P_exact` — reproduced as the `t = 0` value of
  (3.1), and its validation is inherited;
* wave 9's refutation of the `x₀`-asymmetry — untouched; (3.1) assigns the same
  `λ(t)` to `x₀` and to every other arc start, which is what §4.2 of that
  document showed the data require;
* the referee's `eps ≠ 0` and the two-channel structure — used, with the same
  two channels, only re-expressed through (4.1);
* `global_exclusion_attempt`'s finding that the elevation does not depend on arc
  depth — consistent: (3.1) depends on the *global* traversed mass, not on the
  depth of the current arc, which is precisely what their §2.2 argued and their
  §3 measured.

### 6.3 The `O(c/n)` pieces deliberately dropped, sized

The reduction (4.1) is exact row by row **except** in the kill law.

> **[Correção pós-adversarial, 2026-08-23.]** Falso como escrito: a
> linha do "pool de imagem" também é inexata, na mesma ordem `O(c/n)`,
> e não é nomeada em lugar nenhum aqui — o pool de imagem de M-U é
> `n′`, não `n′/(1−c′/n′)` como a tabela da §4 escreve (para `b=1`,
> `U_rem=[n′]` exatamente). Essa contradição entre a linha "mundo" e a
> linha "pool de imagem" da tabela da §4 é resolvida, nesta frente, em
> favor da linha errada — daí a redução (4.1) usar `c′=c(1−ρ)` em vez
> de `c''=c(1−c/n)^{b−1}` (ver correção em §5 acima). Ver
> `adversarial/REFEREE_REPORT.md` §5.1.

An `f`-draw
kills on *any* visited point, and M-CLUST's walk visits points of `R` (the run
starts it hits, and the chain points) that are **not** part of the collapsed
mass. At collapsed mass `u` their count is `c′u/(1−ρ)`, so

```
q(u) = u·(1 + δ(1−u)) ,   δ = c/((1−ρ)n)   [vs the continuum]
                          δ_extra = cρ/((1−ρ)n)  [vs M-U at (c′,n′), which carries its own c/n]
```

and, since `(1−q(s))/(1−s) = 1 − δs` exactly,

```
H_δ(u) = u² + (δ/2)·u²(1−u) ,     φ_RED2 := φ_RED with H_δ in place of u².      (6.1)
```

`δ` is 0.003–0.011 on the standard grid (a −0.06 % to −0.26 % effect on `φ`) but
reaches 0.058–0.071 on the extreme cells added in §9 (a −1.2 % to −1.6 %
effect). `φ_RED2` is **derived, not fitted**, and §9 reports it; but it is a
second-order refinement whose baseline (the continuum M-U's own finite-`n`
error, which `x0_asymmetry_attempt` §5.4 measured only in the `b = 1` control)
is not independently pinned down, so **`φ_RED` (5.1) is the claim of this front
and `φ_RED2` is reported as a quantified, named refinement, not adopted.**

---

## 7. T1/T2 — the elevation measured directly as a function of the traversed mass

### 7.0 The simulator

`elev_pool_probe.py`: my own step-by-step walk simulator (not the `f^(2^k)`
shortcut), `x₀` drawn by rejection from `R^c`, `n = 65536` (32768 for `b = 8`),
**40 000 walks per cell** in 800 instances, 8 cells, seeds 20260823810–817.
Total 57–161 million normal `π`-steps per cell.

At every normal step it records, in bins of the traversed mass `s`:

```
pool     = |U_rem| − (# normal steps taken so far)            [the claim of §3]
w_master = n_test_live / ((1−s)·n)        the density the master formula assigns
w_exact  = n_test_live / pool             the density (3.1) assigns
hit      = 1{ π(x) ∈ Y_test }
```

`Y_test` is an **exogenous** probe set of 1000 points drawn uniformly from
`U_rem \ R` when the instance is built, independent of the walk;
`n_test_live` is how many of them are not yet consumed as an image. Then per bin

```
λ_measured = Σhit / Σw_master     λ_model = Σw_exact / Σw_master     ratio = Σhit / Σw_exact
```

Using an exogenous probe instead of the walk's own arc starts buys ~10² × the
statistics (a walk yields at most one closure into a live arc start, but tens of
probe hits), at the cost of not exercising the survival conditioning; the
live-arc-start estimator is accumulated in parallel as a cross-check (§7.4).
Errors are cluster bootstrap over instances (2000 replicates).

Two **deterministic** audits run on a 1-in-4096 sample of the steps: the image
`π(x)` must lie in `U_rem`, and must not already have been consumed (injectivity).
**`audit_fail = 0` in all eight cells** — 0 failures out of ≈2.2×10⁵ audited
steps drawn from the 9.1×10⁸ normal steps simulated.

**Simulator cross-check.** The walk simulator's own `φ(cyclic | x₀ ∉ R)` agrees
with the referee's graph-level `phi_notR` (an entirely different algorithm — no
walk at all) within 1.7σ in all eight cells.

### 7.1 The elevation is not constant

Two representative cells (full tables in `elev_analysis.log`):

`b = 100, c = 600, ρ = 0.6014`, `P_lead = 2.5086`, 40 000 walks, 57.6 M steps:

| mass bin | hits | λ measured | ± | λ model (3.1) | P_lead | ratio |
|---|---|---|---|---|---|---|
| [0.000,0.005] | 477 423 | 2.4985 | 0.0057 | 2.4951 | 2.5086 | 1.00136 |
| [0.005,0.010] | 438 697 | 2.5058 | 0.0060 | 2.5122 | 2.5086 | 0.99746 |
| [0.010,0.020] | 671 591 | 2.5355 | 0.0060 | 2.5362 | 2.5086 | 0.99974 |
| [0.020,0.035] | 469 865 | 2.5732 | 0.0067 | 2.5721 | 2.5086 | 1.00040 |
| [0.035,0.060] | 118 830 | 2.6067 | 0.0097 | 2.6174 | 2.5086 | 0.99591 |
| [0.060,0.100] | 2 368 | 2.7368 | 0.0496 | 2.6684 | 2.5086 | 1.02566 |
| **aggregate** | | **2.5332** | **0.0052** | **2.5342** | 2.5086 | **0.99959 ± 0.00127** |

`b = 400, c = 100, ρ = 0.4571`, `P_lead = 1.8419`, 159 M steps (abridged — two
of the eight bins omitted for width; the full eight are in `elev_analysis.log`):

| mass bin | hits | λ measured | ± | λ model (3.1) | P_lead | ratio |
|---|---|---|---|---|---|---|
| [0.000,0.005] | 364 288 | 1.8454 | 0.0054 | 1.8481 | 1.8419 | 0.99855 |
| [0.010,0.020] | 686 498 | 1.8706 | 0.0054 | 1.8667 | 1.8419 | 1.00206 |
| [0.035,0.060] | 1 106 989 | 1.9147 | 0.0058 | 1.9101 | 1.8419 | 1.00243 |
| [0.060,0.100] | 802 778 | 1.9452 | 0.0067 | 1.9434 | 1.8419 | 1.00094 |
| [0.100,0.180] | 216 397 | 1.9768 | 0.0093 | 1.9797 | 1.8419 | 0.99852 |
| [0.180,1.000] | 2 818 | 2.0554 | 0.0356 | 2.0400 | 1.8419 | 1.00754 |
| **aggregate** | | **1.8984** | **0.0053** | **1.8975** | 1.8419 | **1.00047 ± 0.00112** |

The measured elevation rises by **11.4 %** across the mass range in this cell
while `P_lead` is flat, and (3.1) tracks it bin by bin with no fitted parameter.

> **[Correção pós-adversarial, 2026-08-23.]** A coluna "λ model (3.1)"
> nas duas tabelas acima está rotulada incorretamente: não é a forma
> fechada (3.1) (que usa o pool médio de ensemble `A·n`), e sim a
> **razão do pool medido passo-a-passo** (`Σw_exact/Σw_master` — o
> mecanismo, não a fórmula). Isso é visível nos próprios números
> impressos: em `b=400,c=100`, o valor da coluna no bin `[0,100,0,180]`
> é 1,9797, enquanto a forma fechada (3.1) nesse bin toma valores
> 2,028–2,254 — uma média ponderada de `λ(t)` não pode cair fora do
> intervalo do próprio bin. O referee mediu a forma fechada (3.1)
> separadamente com seu próprio simulador (9 células, 5,91×10⁸ passos)
> e a **refutou**, χ²=360/67 bins (contra χ²=77,5/67 para o mecanismo
> de pool medido, que se confirma) — o texto da §7.3/§13 abaixo sobre
> "λ(t) consistente com ruído puro" refere-se ao mecanismo, não à
> forma fechada (3.1), que `φ_RED`/`φ_REDB` de fato usam. O efeito é
> pequeno ponderado pela massa (a razão agregada `hits/Σw_cf` do
> referee fica dentro de 0,6% de 1), mas o scorecard da §13
> sobre-afirma o que foi mostrado neste ponto. Ver
> `adversarial/REFEREE_REPORT.md` §4.2.

### 7.2 The derived density reproduces the measured one

Aggregate `ratio = Σhits / Σ(derived density)` — must be 1 if §3 is right:

| b | c | ρ | ratio | ± | z vs 1 |
|---|---|---|---|---|---|
| 8 | 160 | 0.0384 | 1.00166 | 0.00120 | +1.39 |
| 50 | 400 | 0.2637 | 0.99816 | 0.00121 | −1.52 |
| 100 | 150 | 0.2048 | 0.99941 | 0.00122 | −0.48 |
| 100 | 400 | 0.4579 | 0.99941 | 0.00123 | −0.48 |
| 100 | 600 | 0.6014 | 0.99959 | 0.00127 | −0.32 |
| 200 | 150 | 0.3676 | 0.99756 | 0.00118 | −2.06 |
| 300 | 150 | 0.4971 | 1.00314 | 0.00111 | +2.82 |
| 400 | 100 | 0.4571 | 1.00047 | 0.00112 | +0.42 |

**The derived pool law reproduces the measured closure density to 0.3 % or
better everywhere, with a measurement precision of 0.12 %.** Two cells sit at
±2–3σ; the scatter across cells (0.0022) is about 1.8× the quoted sems, the same
under-dispersion `x0_asymmetry_attempt` §6 item 2 already flagged as an open
property of this class of measurement.

### 7.3 The decisive number

χ² of the measured `λ` per mass bin (bins with ≥ 2000 hits) against each
hypothesis, over the eight cells:

| b | c | ρ | bins | λ measured, first → last bin | χ² vs constant `P_lead` | χ² vs λ(t) of (3.1) |
|---|---|---|---|---|---|---|
| 100 | 150 | 0.2048 | 7 | 1.2556 → 1.2916 | 173.2 | 1.6 |
| 100 | 400 | 0.4579 | 6 | 1.8355 → 1.9196 | 187.4 | 2.0 |
| 100 | 600 | 0.6014 | 6 | 2.4985 → 2.7368 | 239.4 | 4.7 |
| 200 | 150 | 0.3676 | 7 | 1.5780 → 1.6643 | 421.3 | 9.7 |
| 300 | 150 | 0.4971 | 7 | 1.9939 → 2.1401 | 650.8 | 6.8 |
| 400 | 100 | 0.4571 | 8 | 1.8454 → 2.0554 | 718.9 | 3.0 |
| 50 | 400 | 0.2637 | 7 | 1.3481 → 1.4133 | 67.1 | 8.5 |
| 8 | 160 | 0.0384 | 8 | 1.0414 → 1.0490 | 15.3 | 14.6 |
| **pooled** | | | **56** | | **2473.4** | **50.9** |

**The constant-elevation ansatz shared by `φ_NEW`, `φ_CAND`, `φ_CAND5`,
`φ_GLOBAL`, `φ_EPS` and `φ_EPSR` is refuted directly at the mechanism level,
χ² = 2473 for 56 degrees of freedom. The derived `λ(t)` is consistent with pure
noise, χ² = 50.9 for 56.** No `φ` and no quadrature enter this comparison.

### 7.4 Cross-check against the predecessors' own estimator

Re-running the same walks through a Horvitz–Thompson estimator on the walk's
**real** live arc starts — the estimator and weighting of
`x0_asymmetry_attempt` §5.3 — reproduces their `λ_bar/P_lead`:

| b, c | this front | `x0_asymmetry_attempt` §5.3 |
|---|---|---|
| 100, 400 | 1.0232 ± 0.0015 | 1.0203 |
| 100, 600 | 1.0193 ± 0.0020 | 1.0256 (run A) / 1.0375 (run R) |
| 200, 150 | 1.0279 ± 0.0014 | 1.0445 |
| 300, 150 | 1.0367 ± 0.0020 | 1.0555 / 1.0345 |
| 400, 100 | 1.0462 ± 0.0019 | 1.0470 / 1.0434 |
| 50, 400 | 0.9911 ± 0.0011 | 1.0094 |

so their measurement is independently replicated (within their own
realisation-to-realisation scatter), and the model's prediction for that same
weighting (1.0175, 1.0222, 1.0287, 1.0441, 1.0510, 1.0073) tracks it. The
live-target ratio is `0.994 ± 0.003` pooled over the eight cells — consistent
with the exogenous probe's `1.000` to within 0.6 %, with a −2.0σ hint that live
arc starts may be very slightly harder to hit than an exogenous set of the same
size. **Not used anywhere; recorded as an open item (§11).**

---

## 8. T3 — the formula-free reduction test

Because M-U **is** M-CLUST(1), both sides of claim (4.1) can be *measured* with
the same engine and the same estimator. No master formula, no quadrature, no
elevation and no `eps` model enter this test on either side.

`elev_reduction.py`, seeds 20260823850–867, **40 000 instances per job**, six
stress cells × three jobs (the M-CLUST source cell, and M-U at two conventions
for `n′` that differ by `c(1−ρ)` points, i.e. by a relative `c/n`):

| b | c | ρ | M-CLUST `φ(·\|x₀∉R)` measured | M-U at `n′=(1−ρ)n`, **measured** | z | M-U at `n′=(1−ρ)(n+c)`, **measured** | z | continuum `φ_U(c(1−ρ))` | z |
|---|---|---|---|---|---|---|---|---|---|
| 50 | 400 | 0.2637 | 0.051656 ± 0.000133 | 0.051739 | −0.44 | 0.051621 | +0.18 | 0.051640 | +0.12 |
| 100 | 400 | 0.4579 | 0.060273 ± 0.000157 | 0.060001 | +1.23 | 0.060132 | +0.64 | 0.060181 | +0.59 |
| 100 | 600 | 0.6014 | 0.056987 ± 0.000152 | 0.057262 | −1.29 | 0.057293 | −1.43 | 0.057305 | −2.08 |
| 200 | 150 | 0.3676 | 0.091104 ± 0.000237 | 0.091093 | +0.03 | 0.090918 | +0.56 | 0.090995 | +0.46 |
| 300 | 150 | 0.4971 | 0.101880 ± 0.000270 | 0.101881 | −0.00 | 0.101494 | +1.03 | 0.102041 | −0.59 |
| 400 | 100 | 0.4571 | 0.120138 ± 0.000313 | 0.120439 | −0.68 | 0.120005 | +0.30 | 0.120277 | −0.44 |

```
chi2 over 6 cells:   vs measured M-U(n'=(1-rho)n)      = 3.83
                     vs measured M-U(n'=(1-rho)(n+c))  = 3.93
                     vs the continuum phi_U(c(1-rho))  = 5.47      (expected ~6)
```

**The reduction (4.1) is confirmed at the level of the raw simulated quantity,
with no formula on either side, χ² = 3.83 for 6 cells and |z| ≤ 1.29.**

> **[Correção pós-adversarial, 2026-08-23 — SUBSTITUÍDO, não apenas
> refinado.]** Este resultado usava apenas 40.000 instâncias. O
> referee re-rodou o mesmo teste, sem fórmula em nenhum dos lados, a
> 300.000/400.000 instâncias (7,5× a precisão) e a **6 células
> pré-registradas completas** (as duas que faltavam aqui foram
> concluídas na revisão adversarial): a redução exatamente como
> declarada em (4.1) é **refutada**, com discrepância crescendo com
> `ρ` e `c/n` (χ² pooled = 334,6 contra M-U medido; 420,1 contra a
> forma contínua `φ_U(c(1−ρ))`). A convenção corrigida `c''` de §5
> acima (`φ_REDB`) reduz o χ² pooled ~3,3× para **101,4** (contínuo:
> 123,3) e traz cinco das seis células a `|z|≤1,5` — mas a correção
> não é completa: a sexta célula, a mais extrema (`b=100,c=1000,
> ρ=0,785`, o maior `c/n` testado), sozinha fornece **~96%** do χ²
> pooled da forma corrigida, com desvio de 1,2–1,3% (`z≈−10`) — maior
> que a correção `O(c/n)` de ~0,77% que a §5.1 do referee estima para
> essa célula, indicando um resíduo real além da correção de
> parâmetro nas células mais extremas, consistente com o efeito
> `O(b²c/n²)` não-modelado que a correção de §2 acima já assinala.
> Tudo qualitativo em §2–§4 sobrevive à correção; só o argumento de
> `φ_U` muda. Ver `adversarial/REFEREE_REPORT.md` §0, §5.

For
comparison, `φ_V4` — the constant-elevation model of the formula of record —
sits at χ² = 475.6 against the same quantity on this front's 24-cell grid (§9)
and at χ² = 169.4 / 139.5 on the referee's two grids (§10).

The one cell at −2σ against the continuum, `b=100, c=600` (the largest `ρ` and
largest `c/n` of the standard grid), deviates by −0.55 %, against the −0.35 %
that the chain-mass term `δ` of §6.3 predicts — i.e. the residual there is of
the size and sign of the `O(c/n)` piece deliberately dropped, not of the
elevation.

---

## 9. T4 — fresh-seed validation, including six cells beyond anything ever tested

`elev_validate.py`, own engine, seeds 20260823820–843, 20 000 instances per
cell: the lineage's standard 18-cell grid (for direct comparison with six
recorded grids), plus **six cells deliberately outside everything this lineage
has probed** — `ρ` up to 0.841 against a previous maximum of 0.601, `b·c/n` up
to 1.83 against a previous maximum of 0.92, and two cells at `n = 131072`.

**Engine cross-validation first** (mandatory before trusting a new simulator).
My `φ_mc` against four already-recorded grids, cell by cell:

| recorded grid | cells | χ²/dof | \|z\|max | mean z |
|---|---|---|---|---|
| referee A (20260823701) | 18 | 19.3 / 18 | 1.93 | −0.174 |
| referee C (20260823703) | 18 | 18.3 / 18 | 1.94 | −0.046 |
| x0_asymmetry (20260822943) | 18 | 14.9 / 18 | — | −0.518 |
| global_exclusion (20260822911) | 18 | 12.2 / 18 | — | +0.138 |

No systematic offset, no outlier beyond 2σ.

**The conditional half on its own** — the quantity §5.6 of the referee report
localised the residual in, measured here on 24 cells:

```
chi2 (24 cells) on phi(cyclic | x0 not in R):
      phi_V4  (constant elevation P_lead, the formula of record) = 475.60
      phi_U(c(1-rho))  (this front)                              =  88.74
```

**Full φ, standard 18-cell grid and the six extra cells:**

| n | b | c | ρ | bc/n | φ_mc (sem) | φ_CAND dev% (z) | φ_EPSR dev% (z) | **φ_RED dev% (z)** | φ_RED2 dev% (z) |
|---|---|---|---|---|---|---|---|---|---|
| 32768 | 8 | 10 | 0.0024 | 0.002 | 0.279944 (0.001045) | +0.047 (+0.12) | +0.021 (+0.06) | **−0.012 (−0.03)** | −0.007 (−0.02) |
| 32768 | 8 | 40 | 0.0097 | 0.010 | 0.138028 (0.000506) | −0.953 (−2.62) | −1.064 (−2.93) | **−1.125 (−3.10)** | −1.100 (−3.03) |
| 32768 | 8 | 160 | 0.0384 | 0.039 | 0.068857 (0.000251) | +0.343 (+0.94) | −0.143 (−0.39) | **−0.262 (−0.72)** | −0.147 (−0.40) |
| 65536 | 50 | 10 | 0.0076 | 0.008 | 0.278910 (0.001005) | +0.006 (+0.02) | −0.007 (−0.02) | **−0.109 (−0.30)** | −0.107 (−0.30) |
| 65536 | 50 | 50 | 0.0374 | 0.038 | 0.123341 (0.000462) | +0.522 (+1.39) | +0.448 (+1.19) | **+0.234 (+0.62)** | +0.250 (+0.67) |
| 65536 | 50 | 150 | 0.1083 | 0.114 | 0.068806 (0.000253) | +1.059 (+2.85) | +0.810 (+2.19) | **+0.446 (+1.21)** | +0.504 (+1.37) |
| 65536 | 50 | 400 | 0.2637 | 0.305 | 0.038341 (0.000144) | +1.431 (+3.76) | +0.608 (+1.61) | **+0.021 (+0.06)** | +0.215 (+0.57) |
| 65536 | 100 | 10 | 0.0151 | 0.015 | 0.279245 (0.001043) | +0.612 (+1.63) | +0.599 (+1.59) | **+0.393 (+1.05)** | +0.395 (+1.05) |
| 65536 | 100 | 50 | 0.0735 | 0.076 | 0.120783 (0.000449) | +0.547 (+1.46) | +0.470 (+1.26) | **+0.043 (+0.12)** | +0.060 (+0.16) |
| 65536 | 100 | 150 | 0.2048 | 0.229 | 0.064180 (0.000237) | +0.185 (+0.50) | −0.095 (−0.26) | **−0.815 (−2.23)** | −0.751 (−2.05) |
| 65536 | 100 | 400 | 0.4579 | 0.610 | 0.032920 (0.000122) | +2.104 (+5.56) | +0.961 (+2.57) | **−0.220 (−0.60)** | +0.039 (+0.10) |
| 65536 | 100 | 600 | 0.6014 | 0.916 | 0.023201 (0.000085) | +3.082 (+8.12) | +0.718 (+1.94) | **−0.730 (−2.00)** | −0.203 (−0.55) |
| 65536 | 200 | 5 | 0.0151 | 0.015 | 0.392217 (0.001427) | +0.186 (+0.51) | +0.180 (+0.49) | **−0.117 (−0.32)** | −0.116 (−0.32) |
| 65536 | 200 | 20 | 0.0592 | 0.061 | 0.192938 (0.000717) | +0.940 (+2.51) | +0.911 (+2.43) | **+0.350 (+0.94)** | +0.356 (+0.96) |
| 65536 | 200 | 60 | 0.1674 | 0.183 | 0.105143 (0.000392) | +1.656 (+4.37) | +1.550 (+4.09) | **+0.610 (+1.63)** | +0.633 (+1.69) |
| 65536 | 200 | 150 | 0.3676 | 0.458 | 0.057935 (0.000216) | +2.161 (+5.68) | +1.795 (+4.73) | **+0.326 (+0.87)** | +0.407 (+1.09) |
| 65536 | 300 | 150 | 0.4971 | 0.687 | 0.051624 (0.000194) | +2.851 (+7.38) | +2.377 (+6.18) | **+0.151 (+0.40)** | +0.250 (+0.66) |
| 65536 | 400 | 100 | 0.4571 | 0.610 | 0.065915 (0.000245) | +3.402 (+8.86) | +3.108 (+8.12) | **+0.663 (+1.77)** | +0.722 (+1.93) |
| **65536** | **200** | **600** | **0.8411** | **1.831** | 0.015106 (0.000056) | +8.231 (+20.43) | +1.869 (+4.93) | **−1.179 (−3.20)** | +0.064 (+0.17) |
| **65536** | **800** | **100** | **0.7053** | **1.221** | 0.048962 (0.000188) | +7.012 (+17.06) | +6.404 (+15.67) | **+1.217 (+3.13)** | +1.320 (+3.39) |
| **65536** | **100** | **1000** | **0.7851** | **1.526** | 0.013780 (0.000051) | +8.253 (+20.57) | +0.761 (+2.04) | **−1.102 (−3.01)** | +0.497 (+1.33) |
| **65536** | **400** | **300** | **0.8404** | **1.831** | 0.020960 (0.000079) | +7.426 (+18.29) | +4.080 (+10.37) | **−0.467 (−1.24)** | +0.126 (+0.33) |
| **131072** | **200** | **800** | **0.7061** | **1.221** | 0.017229 (0.000064) | +3.215 (+8.34) | +1.044 (+2.77) | **−0.669 (−1.80)** | −0.193 (−0.52) |
| **131072** | **400** | **400** | **0.7055** | **1.221** | 0.024225 (0.000091) | +3.275 (+8.47) | +2.164 (+5.66) | **−0.310 (−0.83)** | −0.079 (−0.21) |

```
chi2, standard 18-cell grid : CAND =  324.66   EPSR =  181.50   RED =  30.20   RED2 = 26.97
chi2, all 24 cells          : CAND = 1931.87   EPSR =  602.62   RED =  64.79   RED2 = 40.71
formula BELOW the MC mean   : CAND = 23/24     EPSR = 20/24     RED = 11/24    RED2 = 15/24
```

One cell deserves a note before anyone else finds it: `b=8, c=40` sits at
−1.13 % (−3.10σ) for `φ_RED`, and at −0.95 % / −1.06 % for `φ_CAND` / `φ_EPSR` —
all three agree there, because `ρ = 0.0097` makes them numerically the same
formula, so it is not an elevation effect. The referee's two grids give −0.23 %
and +0.05 % for the same cell and formula; this is a fluctuation of my
realisation, and it is the largest |z| `φ_RED` shows anywhere on the standard
grid.

`eps` on the same fresh grid: χ² (24 cells) = **97.6** for `eps_ref` (the formula
of record) against **57.2** for `eps_RED` — the same two channels, only with
`φ_runstart → T_U(c′)` and `cT → c′T_U(c′)` under the reduction.

---

## 10. All seven grids pooled

`φ_CAND` and `φ_EPSR` are re-implemented here from their stated closed forms;
they reproduce the referee's own χ² values on every recorded grid to three
significant figures (335.56 / 183.56 on grid A, 298.80 / 152.57 on grid C,
121.78 / 71.40, 80.06 / 43.58, 73.63 / 46.52, 81.60 / 49.58), which is the check
that the re-transcription is faithful.

Six of the seven grids below are **cheap triage on already-recorded Monte-Carlo
means** (labelled as such, no new seed); the seventh is this front's own fresh
grid of §9.

| grid | cells | χ² CAND | χ² EPSR | **χ² RED** | χ² RED2 | below-MC CAND / EPSR / RED |
|---|---|---|---|---|---|---|
| residual_attempt (720330339) | 18 | 81.60 | 49.58 | **15.14** | 15.33 | 15/18, 14/18, 11/18 |
| aggregation_closure (20260822904) | 18 | 73.63 | 46.52 | **21.59** | 20.57 | 16/18, 16/18, 10/18 |
| global_exclusion (20260822911) | 18 | 80.06 | 43.58 | **11.05** | 12.27 | 12/18, 12/18, 8/18 |
| x0_asymmetry (20260822943) | 18 | 121.78 | 71.40 | **14.79** | 17.47 | 18/18, 17/18, 15/18 |
| referee grid A (20260823701) | 18 | 335.56 | 183.56 | **33.13** | 32.83 | 16/18, 15/18, 10/18 |
| referee grid C (20260823703) | 18 | 298.80 | 152.57 | **22.85** | 20.93 | 15/18, 14/18, 10/18 |
| **this front, fresh (20260823820–843)** | 24 | 1931.87 | 602.62 | **64.79** | 40.71 | 23/24, 20/24, 11/24 |
| **POOLED** | **132** | **2923.29** | **1149.82** | **183.33** | 160.10 | **115/132, 108/132, 75/132** |
| pooled, standard grids only | 126 | 1316.08 | 728.70 | **148.74** | 146.36 | — |

| | median \|dev%\| | max \|dev%\| |
|---|---|---|
| φ_CAND | 1.060 | 8.253 |
| φ_EPSR | 0.781 | 6.404 |
| **φ_RED** | **0.456** | **2.168** |
| φ_RED2 | 0.451 | 2.186 |

Two things matter more than the χ² number itself.

1. **The residual no longer grows with `b` or `ρ`.** For `φ_EPSR` the deviation
   climbs monotonically into the corner of the grid (+6.4 % at `b=800`, +4.1 % at
   `ρ=0.84`); for `φ_RED` the six extreme cells give −1.18, +1.22, −1.10, −0.47,
   −0.67, −0.31 %, i.e. the same size as the ordinary cells and of both signs.
2. **The sign bias is gone.** `adversarial/REFEREE_REPORT.md` §5.8 warns
   explicitly that "`φ_CAND` is below the Monte-Carlo mean in 16–18 of 18 cells
   on every grid tested. Any strictly positive additive correction of roughly
   the right size would therefore reduce χ². **The χ² reduction alone is weak
   evidence for the specific functional form.**" Pooled over 132 cells from
   seven independent seeds, `φ_CAND` is below the mean in 115/132
   (p ≈ 1e-17) and `φ_EPSR` in 108/132 (p ≈ 1e-13), while `φ_RED` is below in
   **75/132**, which is 1.5σ from the 66 expected of an unbiased formula. That
   caveat is met, not side-stepped — and it is met by a formula that was fixed
   in writing before any of these numbers were computed.

---

## 11. Honesty — what is established, what is heuristic, what is open

**Established (derived from the mechanism first, then measured, with fresh
seeds, at production scale):**

1. **The closure-hazard elevation is not a constant.** χ² of the measured
   elevation per mass bin, pooled over 56 bins in 8 cells: **2473.4** against the
   constant `P_lead` that every formula of this lineage uses, **50.9** against
   the derived `λ(t)`. This is a mechanism-level measurement: no `φ`, no
   quadrature, no fitted parameter.
2. **The reason is the pool.** The walk's `π`-images are drawn from `U_rem`
   (density `(1−c/n)^{b−1}`), not from `[n]`, and the walk consumes out of
   `U_rem` at the same rate at which it consumes mass — so the elevation grows
   from `P_exact` at `t = 0` to `(1−t)/(1−ρ−t)`. The derived density reproduces
   the measured closure rate to ≤ 0.3 % in eight cells (measurement precision
   0.12 %), with **zero failures** of two deterministic audits sampled 1-in-4096
   along the 9.1×10⁸ normal steps simulated.
3. **The reduction.** Conditioned on `x₀ ∉ R`, M-CLUST(b) at `(c,n)` is M-U at
   `(c(1−ρ), (1−ρ)n)`. Tested with no formula on either side: χ² = 3.83 for 6
   cells.
4. **In the master formula this gives `φ_RED`**, which pooled over seven
   independent grids and 132 cells reduces χ² from 1149.8 (the formula of
   record) to 183.3 with the sign bias removed, and whose residual no longer
   grows with `b` or `ρ` — including in six cells at `ρ` up to 0.841 and
   `b·c/n` up to 1.83, far outside anything this lineage had tested.

**Heuristic / derived at leading order, labelled (not proved):**

1. The exposure of §2 is at the same research-draft rigor as everything else in
   this lineage. The non-trivial step is not "π restricted to `A_rem → U_rem` is
   a uniform bijection" (standard) but "given the walk's entire history —
   including the conditioning on not having closed yet — `π(x)` is uniform on
   `U_rem` minus what the walk has consumed". That step is **measured** (§7),
   not proved. The martingale/optional-stopping justification for the
   Horvitz–Thompson estimator is the one `x0_asymmetry_attempt` §2.2 already
   used.
2. Events of probability `O(b²/n)` (a short `π`-cycle crossing a window) are
   neglected throughout, as in `aggregation_closure_attempt` §3.1.
3. `§6.3`'s `δ` term is derived but **not** adopted; `φ_RED2` quantifies it.
   It is a real effect (`−0.06 %` to `−1.6 %` across the grid) and it improves
   the extreme cells markedly (χ² 64.8 → 40.7 on the 24-cell grid) while being
   neutral on the standard grid (148.7 → 146.4 over 126 cells). I do not adopt
   it because its baseline — the continuum M-U's own finite-`n` error at the
   *reduced* parameters `(c′, n′)` — is not independently pinned down here;
   `x0_asymmetry_attempt` §5.4 measured that error only in the `b = 1` control.
4. The `eps` channels are the referee's, re-expressed; their leading-order
   status is unchanged.

**Open (named, not pursued):**

1. **A real residual remains**: χ²/dof ≈ 1.4 pooled (183.3 / 132), 1.18 on the
   standard grids alone (148.7 / 126), against ~1.0 for pure noise. Median
   deviation 0.46 %, maximum 2.17 %. Its size matches the `O(c/n)` pieces named
   in §6.3, and it does not grow with `b` or `ρ`, but it is not zero and I have
   not derived it.
2. The live-arc-start estimator gives `Σhits/Σ(derived density) = 0.994 ± 0.003`
   pooled over the eight probe cells, against `1.000 ± 0.0012` for the exogenous
   probe — a −2.0σ hint that the walk's own arc starts are marginally harder to
   hit than an exogenous set of the same size. This is exactly the exogeneity
   question `aggregation_closure_attempt` §7.1 raised. Not used anywhere; would
   need ~4× the walks to settle.
3. The realisation-to-realisation scatter of these HT ratios is ≈1.8× the
   cluster-bootstrap sem, the same under-dispersion `x0_asymmetry_attempt` §6
   item 2 flagged. Not investigated.
4. `x0_asymmetry_attempt` §5.5's unmodelled terminal channel (a normal `π`-step
   landing on a visited point of `R` that is not an arc start, 0.15–0.70 % of
   terminal events) is present in my walk simulator but is still not represented
   in the master formula.
5. **The Poissonisation/independence approximation of the master formula itself**
   remains untouched, as in every predecessor. But this front *narrows* it
   rather than leaving it where it was: by (4.1), whatever that error is for
   M-CLUST(b) conditioned on `x₀ ∉ R`, it is M-U's own error at `(c′, n′)` — a
   quantity `x0_asymmetry_attempt` §5.4 measured directly (O(1/n), ≈0.02 % at
   `n = 65536`; +0.071 % at `n = 16384`, which brackets the smallest `n′` on
   this grid). That is the same order as the residual left in item 1.

**One point of intellectual honesty about how the derivation was found.** I read
both predecessor localisations before deriving anything, so I knew the residual
grows with `b` and `ρ` and lives in the elevation. That knowledge told me *which
mechanism feature to look for*; it did not supply the answer, and no functional
form was chosen because it reduced χ². `DERIVATION_PREREG.md` — with the
derivation, the formula, all constants and the four refutation criteria — was
written and saved before a single simulation of this front was run. In the
referee's own classification (§5.7 of the report) this is measurement-guided
model *selection*, not parameter fitting; and here it is weaker than that, since
what guided me was a qualitative statement ("grows with b and ρ") rather than
any number.

---

## 12. Verdict

> **POSITIVE RESULT — the target of `DISC-DEC-045` front (a) is closed, and it
> did not have a closed form because it was not a constant.**
>
> The excess of the true per-target closure elevation over `P_lead = 1/(1−ρ)`,
> named by `x0_asymmetry_attempt/ATTEMPT.md` §5.3 and by
> `adversarial/REFEREE_REPORT.md` §5.6 as the entire remaining residual of the
> formula of record, is **not a larger constant**. It is the growth of a
> `t`-dependent elevation that every formula in this lineage — `φ_NEW`,
> `φ_CAND`, `φ_CAND5`, `φ_GLOBAL`, `φ_EPS`, `φ_EPSR` — has been evaluating at
> `t = 0`. The mechanism is that the walk draws its `π`-images from `U_rem`
> (mass `(1−ρ)/(1−c/n)`), not from `[n]`, while consuming from it at the same
> rate at which it consumes mass:
> ```
> λ(t) = (1−t) / [ (1−ρ)/(1−c/n) − t_c ] ,     λ(0) = P_exact = (1−c/n)^{−(b−1)}.
> ```
> Measured directly at the mechanism level, over 56 mass bins in 8 cells and
> 9.1×10⁸ walk steps: **χ² = 2473 against a constant elevation, χ² = 50.9 against
> the derived λ(t)** (56 expected). The constant-elevation ansatz is refuted, and
> the derived law is at noise level.
>
> With that elevation the master formula collapses: **conditioned on `x₀ ∉ R`,
> M-CLUST(b) at `(c,n)` is exactly M-U at `(c(1−ρ), (1−ρ)n)`** — wave 4's
> encounter rate `c` and wave 4's `q_CLUST(s)=s/(1−ρ)` both survive untouched,
> only the mass coordinate changes. Tested with **no formula on either side**
> (M-U simulated at the matched parameters): χ² = 3.83 for 6 cells.
> Hence `φ(cyclic | x₀ ∉ R) = φ_U(c(1−ρ))`, and, with the referee's two `eps`
> channels re-expressed through the same reduction,
> ```
> φ_RED = (1−ρ)[ φ_U(c′) + (c/n)·T_U(c′) ] + ρ(1 + c′T_U(c′))/((1−ρ)n),   c′ = c(1−ρ).
> ```
> Pooled over **seven independent grids and 132 cells** (six recorded as cheap
> triage, one fresh with seeds 20260823820–843): χ² falls from **1149.8**
> (`φ_EPSR`, the formula of record) to **183.3**; the median absolute deviation
> falls from 0.78 % to 0.46 % and the maximum from 6.40 % to 2.17 %; and — the
> point the referee's §5.8 insisted on — the systematic sign bias disappears,
> 108/132 cells below the Monte-Carlo mean becoming 75/132, 1.5σ from unbiased.
> On six cells deliberately placed beyond anything this lineage has ever tested
> (`ρ` to 0.841, `b·c/n` to 1.83), `φ_CAND` is off by +7 % to +8 % and `φ_EPSR`
> by +0.8 % to +6.4 %, while `φ_RED` is off by −1.2 % to +1.2 %.
>
> A real residual remains — χ²/dof ≈ 1.2–1.4, median 0.46 % — but it no longer
> grows with `b` or `ρ`, it is of the size of the `O(c/n)` terms this document
> derives and names (§6.3), and one of those terms, written down explicitly as
> `φ_RED2`, accounts for most of it in the extreme cells (χ² 64.8 → 40.7 on the
> 24-cell fresh grid) without being adopted.
>
> `φ_U(c(1−ρ))` is numerically the wave-3 `φ_OLD`. That is **not** a
> rehabilitation of the refuted `c_eff`: wave 4's refutation of the *rate
> depression* stands and is used here; the same number reappears through a
> different route (an elevated hazard plus a change of variable), it is the
> **conditional** probability rather than the unconditional one, and the missing
> factor `(1−ρ)` — discovered three waves later — is the whole of wave 3's
> −46 % (§6.1).
>
> **This is a positive claim about the formula of record. Per this line's
> standing discipline it requires independent adversarial verification before
> any cataloguing. This front does NOT declare `φ_RED` integrated and does NOT
> declare `φ_EPSR` superseded.**
>
> The classification **M-CLUST(b) ∈ U_{1/2} in the n→∞ limit (∀ fixed b) is
> completely untouched** by everything above: `ρ → 0` at fixed `(b,c)`, so
> `c′ → c`, `(1−ρ) → 1`, and `φ_RED → φ_U(c)` — the same limit the lineage has
> always had. Every term of `φ_RED` that differs from `φ_U(c)` vanishes as
> `n → ∞`.

> **[Correção pós-adversarial, 2026-08-23 — leia antes de citar este
> veredito.]** A verificação adversarial mandatória (agora completa,
> incluindo as duas células que faltavam neste veredito original) muda
> materialmente a conclusão sobre a redução e a fórmula candidata:
>
> 1. **O mecanismo da elevação (a descoberta central desta frente) foi
>    CONFIRMADO independentemente**, e de forma mais forte: o referee
>    reproduziu a refutação da elevação constante com seu próprio
>    simulador (χ²=1925/67 bins) e confirmou o mecanismo "hazard =
>    1/(pool)" a ≈0,2% por célula, com zero falhas de auditoria em
>    5,91×10⁸ passos. **Esta parte do veredito permanece de pé, e é a
>    evidência mais decisiva de toda a frente.**
> 2. **A redução exatamente como declarada (`c′=c(1−ρ)`, χ²=3,83/6
>    células) foi REFUTADA** por um re-teste a 7,5× a precisão (χ²
>    pooled = 334,6 em 6 células completas). O erro está nos
>    parâmetros da redução (`c′,n′` subestimam o mundo e o pool em
>    `≈c(1−ρ)` pontos), não no mecanismo.
> 3. **A fórmula correta a catalogar é `φ_REDB` (correção em §5
>    acima), não `φ_RED`.** `φ_REDB` usa `c''=c(1−c/n)^(b−1)` em vez
>    de `c′=c(1−ρ)` e reduz o χ² pooled do teste de redução de 334,6
>    para 101,4 (5 de 6 células a `|z|≤1,5`).
> 4. **Mesmo `φ_REDB` não fecha o resíduo completamente**: a célula
>    mais extrema testada (`b=100,c=1000,ρ=0,785`) sozinha fornece
>    ~96% do χ² pooled restante de `φ_REDB`, com desvio de 1,2–1,3%
>    (`z≈−10`) — maior que a correção `O(c/n)` esperada, indicando um
>    resíduo real e ainda não modelado nos parâmetros mais extremos.
>    Isto não é varrido para debaixo do tapete: fica registrado como
>    item aberto, não como fechamento completo.
> 5. A classificação `U_{1/2}` no limite `n→∞`, e o veredito de que
>    isto é uma melhoria real (não uma reabilitação do `c_eff` da onda
>    3, §6.1), permanecem corretos e inafetados por esta correção.
>
> Ver `adversarial/REFEREE_REPORT.md` §0 (VERDICT) e §5 (T3 completo,
> 6 células) para a fonte completa desta correção.

---

## 13. Scorecard

| item | status | evidence |
|---|---|---|
| Mandated target: closed form for the elevation excess | **FOUND — it is not a constant** | `λ(t) = (1−t)/[(1−ρ)/(1−c/n) − t_c]`, derived §3, pre-registered before any simulation |
| Is the elevation constant in `t`? | **NO — refuted** | χ² 2473.4 vs 50.9 over 56 mass bins, 8 cells (§7.3) |
| Derived density reproduces the measured one | **YES** | ratio 0.998–1.003 in 8 cells, sem 0.0012 (§7.2); 0 audit failures in 9×10⁸ steps |
| Reduction M-CLUST(b)\|x₀∉R ≡ M-U(c(1−ρ),(1−ρ)n) | **CONFIRMED, formula-free** | χ² = 3.83 / 6 cells, both sides measured (§8) |
| `φ_RED` improves on `φ_EPSR` | **YES, fresh seeds + 6 recorded grids** | χ² 1149.8 → 183.3 over 132 cells, 7 seeds (§10) |
| Residual still grows with `b`/`ρ`? | **NO** | extreme cells (ρ≤0.841, bc/n≤1.83): −1.18 % … +1.22 %, both signs (§9) |
| Systematic sign bias (referee §5.8 caveat) | **REMOVED** | 108/132 → 75/132 below the MC mean (§10) |
| `φ_RED` closes the residual completely | **no** | χ²/dof ≈ 1.2–1.4; median dev 0.46 %, max 2.17 % (§10, §11) |
| `O(c/n)` pieces dropped | **derived and sized, not adopted** | §6.3; `φ_RED2` χ² 64.8 → 40.7 on the 24-cell grid (§9) |
| Wave 4's `q_CLUST(s)=s/(1−ρ)` and rate `c` | **used unchanged, not contradicted** | §4, §6.2 |
| Wave 8's `P_exact` | **reproduced as `λ(0)`** | §2, machine precision (§ selftest) |
| Wave 9's x₀-asymmetry refutation | **untouched, consistent** | §6.2 |
| Own engine cross-validated | **yes** | χ²/dof 19.3/18, 18.3/18, 14.9/18, 12.2/18 vs 4 recorded grids (§9) |
| Own walk simulator cross-validated | **yes** | `φ(·\|x₀∉R)` within 1.7σ of the referee's graph method in 8/8 cells (§7.0) |
| `x0_asymmetry` §5.3's `λ_bar` independently replicated | **yes** | §7.4 |
| U_{1/2} classification affected | **no** | `φ_RED → φ_U(c)` as `ρ → 0` (§5, §12) |
| Curve-fitting to `φ_mc` | **none** | `DERIVATION_PREREG.md` predates every simulation of this front; no free parameter anywhere |
| Files outside this subfolder modified | **none** | `git status`: only `elevation_level_attempt/` (untracked) |
| Git commit created | **none** | — |
| Adversarial verification | **REQUIRED, not done here** | §12 |

> **[Correção pós-adversarial, 2026-08-23 — linhas substituídas, não a
> tabela original acima.]** A verificação adversarial mandatória
> (completa, adversarial/REFEREE_REPORT.md) revisa três linhas desta
> tabela:
>
> | item | status corrigido | evidência |
> |---|---|---|
> | Reduction M-CLUST(b)\|x₀∉R ≡ M-U(c(1−ρ),(1−ρ)n) (como declarado) | **REFUTADO** a 7,5× a precisão, 6/6 células completas | χ² pooled = 334,6 vs M-U medido (referee §5.2) |
> | Reduction, convenção corrigida `c''=c(1−c/n)^(b−1)` (`φ_REDB`) | **muito melhor, não perfeito** | χ² pooled 334,6→101,4; 5/6 células `\|z\|≤1,5`; 1 célula extrema (`b=100,c=1000`) fornece ~96% do χ² restante, `z≈−10` |
> | `φ_RED` (5.1) como fórmula candidata a catalogar | **SUPERSEDIDA por `φ_REDB`** (mesma forma, argumento corrigido) | ver §5 acima e `adversarial/REFEREE_REPORT.md` §11 |
>
> Todas as demais linhas da tabela original permanecem válidas como
> escritas — em particular as duas primeiras (mecanismo não-constante,
> densidade derivada reproduz a medida) são as mais fortemente
> confirmadas de toda a frente, com re-derivação independente completa
> pelo referee.

---

## 14. Files (all in this subfolder, `elevation_level_attempt/`)

| file | role |
|---|---|
| `ATTEMPT.md` | this document |
| `DERIVATION_PREREG.md` | **the derivation, the candidate `φ_RED` and the four refutation criteria, written and saved BEFORE any simulation of this front.** The audit trail for the no-curve-fitting rule |
| `PROGRESS.log` | timestamped checkpoints (not the report) |
| `elev_formula.py` / `elev_formula_selftest.log` | own closed forms: `H` (referee §1(i), reuse), `φ_V4`, `φ_CAND`, `φ_EPSR`, and this front's `λ(t)`, `φ_U(c′)`, `T_U(c′)`, `eps_RED`, `φ_RED`. `python3 elev_formula.py` runs the self-checks |
| `elev_mc.py` / `elev_mc_selftest.log` | own M-CLUST(b) engine (three independent constructions of `R` and of the cyclic set, checked against brute force). `python3 elev_mc.py selftest` |
| `elev_pool_probe.py` + `pool_probe_b*_c*.json` + `parts/pool_probe_*.log` | **§7, T1/T2** — own step-by-step walk simulator with the exogenous pool probe, 8 cells, seeds 20260823810–817, 40 000 walks per cell. **This is the result that refutes the constant-elevation ansatz at the mechanism level** |
| `run_pool_probe.py` | driver for the above |
| `elev_reduction.py` / `rebuild_reduction.py` / `elev_reduction_results.json` / `parts/red_*` | **§8, T3** — the formula-free reduction test, seeds 20260823850–867, 40 000 instances per job. `rebuild_reduction.py` reassembles the part files (four jobs were OOM-killed on the first launch and re-run with the same seeds after `elev_mc.py`'s bootstrap was chunked) |
| `elev_validate.py` / `elev_validate.log` / `elev_validate_results.json` / `parts/val_*` | **§9, T4** — fresh 18-cell grid + 6 cells beyond anything tested, seeds 20260823820–843. **This is the result that decides whether `φ_RED` beats `φ_EPSR`** |
| `elev_triage_recorded.py` / `elev_triage_recorded.log` | **§10** — cheap triage on six already-recorded grids (labelled reuse, no new seed); also the check that my `φ_CAND`/`φ_EPSR` reproduce the referee's χ² |
| `elev_analysis.py` / `elev_analysis.log` | deterministic analysis of everything above (T1/T2, T3, T4, engine cross-validation, the sized `O(c/n)` terms and `φ_RED2`) |
| `elev_pooled.log` | the seven-grid pooled χ², sign test and deviation summary of §10 |
