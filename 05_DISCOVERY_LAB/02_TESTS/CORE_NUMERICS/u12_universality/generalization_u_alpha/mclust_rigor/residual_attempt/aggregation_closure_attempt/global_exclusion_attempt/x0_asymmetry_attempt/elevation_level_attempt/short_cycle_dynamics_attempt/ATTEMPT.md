# ATTEMPT — short π-cycle dynamics and the residual φ_REDB leaves open

**Wave 12, `DISC-DEC-051`, front (b) `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT`**
(continuation of the `MCLUST-RESIDUAL-RIGOR` line, `DISC-DEC-033`, most
recently `MCLUST-ELEVATION-LEVEL-ATTEMPT`, `DISC-DEC-045`/`050`).

**Scope, fixed by mandate.** Everything in this document and this subfolder
(`short_cycle_dynamics_attempt/`) is new. No file outside it was modified —
not `elevation_level_attempt/ATTEMPT.md`, not its `adversarial/` referee
report, not any ancestor `ATTEMPT.md`, not `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `README*`, or
`PROOF_DEPENDENCY_MAP.md`. Integration is the orchestrating session's
business, not this front's. **No git commit was created.**

**Target, quoted from the mandate.** `adversarial/REFEREE_REPORT.md` §11:

> "I also tested a stronger variant, `φ_REDX`, built from the exact densities
> of §3.2 … It is *not* better … it repairs the worst extreme cell … but
> overshoots two others. My reading is that on a π-cycle shorter than `b` the
> *dynamics* also change (the whole cycle is absorbed into `R` and becomes
> unreachable by normal steps), so substituting corrected mean densities into
> a formula derived for the long-cycle regime is not enough."

**Verdict in one line (details in §10): honest non-closure.** The short-cycle
absorption mechanism the referee named is confirmed exactly, at machine
precision, and turns out to sit inside a *much richer* L-dependent structure
than a two-bucket fix can capture. The pre-registered candidate `φ_REDC`
built from it is refuted — like the referee's own `φ_REDX`, it moves the
wrong way on most cells — but the diagnostic run that refutes it also
uncovers a genuine, previously unreported phenomenon (§6, §8) that sharpens
what "closing this" would actually require.

---

## 0. Discipline

Read in full before deriving anything: `DECISION_LEDGER.yaml` `DISC-DEC-051`;
`PROOF_DEPENDENCY_MAP.md` "Árvore B" (with its dated addenda);
`elevation_level_attempt/ATTEMPT.md` §0–14 (all `[Correção pós-adversarial]`
blockquotes read alongside the original text they correct);
`elevation_level_attempt/adversarial/REFEREE_REPORT.md` §0–12 in full, §0/
§3.2/§5/§11 read line by line as instructed; `generalization_u_alpha/
DERIVATIONS.md` §0–3.6, §6; `mclust_rigor/DERIVATION_MCLUST_FIXED.md` §0–6
(the last two are prose derivation documents needed to pin the mechanism
down precisely — not scripts of the target front or its referee, so reading
them does not violate the independence rule below).

**Independence.** No `.py` file under `elevation_level_attempt/` or
`elevation_level_attempt/adversarial/` was read or imported at any point —
not `elev_formula.py`, `elev_mc.py`, `elev_pool_probe.py`,
`elev_reduction.py`, `elev_validate.py`, nor `ref2_mc.py`, `ref2_walk.py`,
`ref2_reduction.py`, `ref2_formula.py`, `ref2_algebra.py`, or any other
`ref2_*.py`. Every script in this subfolder (`sc_*.py`) is written from
scratch from the mechanism as stated in the prose of the primary sources
above, and imports only one another.

**Seeds** — all fresh (`SeedSequence` ≥ `20260825900`), checked by `grep -r
"20260825" ..` over the whole archive before use (only
`20260825800`–`20260825899`, reserved by the sibling wave-12 front (a), were
already in use; nothing in this front's range was):

| seed | use |
|---|---|
| `SeedSequence(20260825900)` | `sc_engine.py selftest` (T0, §4) |
| `SeedSequence(20260825901)` | T1 diagnostic split, target cell `b=100,c=1000,n=65536`, N=2500 |
| `SeedSequence(20260825902)` | T1 diagnostic split, `b=400,c=100,n=65536`, N=2500 |
| `SeedSequence(20260825903)` | T1 diagnostic split, `b=200,c=150,n=65536`, N=2500 |
| `SeedSequence(20260825910)` | T2, own-engine, `b=50,c=400,n=65536`, N=2000 |
| `SeedSequence(20260825911)` | T2, `b=100,c=400,n=65536`, N=2000 |
| `SeedSequence(20260825912)` | T2, `b=100,c=600,n=65536`, N=2000 |
| `SeedSequence(20260825913)` | T2, `b=200,c=150,n=65536`, N=2000 |
| `SeedSequence(20260825914)` | T2, `b=400,c=100,n=65536`, N=2000 |
| `SeedSequence(20260825915)` | T2, target cell `b=100,c=1000,n=65536`, N=3000 |
| `SeedSequence(20260825999)` | a 100-instance throwaway smoke test of `sc_diagnostic.py`, discarded, not counted in any reported number |

**Order of work.** `DERIVATION_PREREG.md` — the re-derived mechanism, the
exact short-cycle combinatorics, the candidate `φ_REDC`, and the fixed
refutation criteria for T1/T2 — was written and saved **before any
simulation of this front was run** (file mtime `13:35:50`; first simulation
output `sc_engine_selftest.log` at `13:38:34`; `sc_formula_selfcheck.log` at
`13:43:45`; every T1/T2 `.log` later still, through `13:59:06`). No
functional form below was chosen after seeing T1 or T2's numbers.
`DERIVATION_PREREG.md` §2.2 states the candidate's sign was not known in
advance, in writing, before any simulation; §8/§9 report the T1 diagnostic
finding exactly as pre-committed — as a diagnostic, not promoted to a new
fitted formula.

---

## 1. The mechanism, re-derived and reconciled (no `.py` read)

`n` points, `π` uniform. Each point is an i.i.d. seed w.p. `p=c/n`. The run
of seed `s` is the **full `b`-point forward orbit** `{s,π(s),…,π^{b−1}(s)}`
(seed included) — reconciling `elevation_level_attempt/ATTEMPT.md`'s terser
§2 phrasing with `DERIVATION_MCLUST_FIXED.md` §1's explicit statement, via
three internal consistency checks (`ρ=1−(1−c/n)^b`, `I⊆R`, `R^c⊆U_rem`
"always") that hold simultaneously only under this reading — full argument
in `DERIVATION_PREREG.md` §1.1. `R = ∪_s` run`(s)`. Every point of `R` gets
an i.i.d. `Uniform([n])` destination, fixed once; outside `R`, `f=π`.
`φ = E[(1/n)|\{x: x$ cyclic under $f\}|]`.

**Re-derived exact fact** (classical, re-derived independently by
sequential exposure, matching but not copied from referee §3.2): for a
uniform permutation, `P(cycle-length(y)=L)=1/n` for every `L=1,…,n`.
Corollary: `E[\#\{y: L(y)\le K\}] = K` for any `K\le n`.

**The dynamical claim this front targets, checked deterministically before
any statistics** (`sc_engine.py selftest`, parts (c)/(d), §4 below): if the
π-cycle through a seed has length `L≤b`, the seed's `b`-point run covers
**every** point of the cycle. Hence a length-`L≤b` cycle is either (i)
**untouched** by every seed (prob `(1−c/n)^L`) — then `f`≡`π` on it exactly,
it is deterministically a cycle of `f`, and **every point on it is cyclic
with probability exactly 1** — or (ii) **touched** by at least one seed —
then **every** point of the cycle is pulled into `R` (not just the seed),
every run-start test on the cycle fails, and the cycle becomes **permanently
unreachable by any normal π-step, from anywhere**, reachable only via a
reroute destination landing on it directly. This is qualitatively different
from a `L>b` cycle, where a seed's run covers only a proper `b`-point sub-arc
and the rest of the cycle stays walkable — the regime `φ_RED`/`φ_REDB`'s
mean-field reduction is built for.

---

## 2. Candidate `φ_REDC` (pre-registered before any simulation)

`DERIVATION_PREREG.md` §2 derives, with no free parameter:

```
S_untouched(b,c,n) = (1/n) sum_{L=1}^{b} (1-c/n)^L        [exact]
P(x0 in R^c)        = (1/n)[ sum_{L=1}^b (1-c/n)^L + (n-b)(1-c/n)^b ]   [exact]
w_short             = S_untouched / P(x0 in R^c)

phi_cond_C = w_short * 1  +  (1 - w_short) * phi_U(c'')     [c'' = phi_REDB's argument]
phi_REDC   = P(R^c) * phi_cond_C  +  P(R) * eps_REDB(c'')
```

i.e. `φ_REDC` layers two derived corrections on top of `φ_REDB`: (a) the
referee's own exact-density ingredient (`P(x0∈R^c)` in place of the
mean-field `1−ρ`, the same idea behind the referee's own tested-and-rejected
`φ_REDX`) and (b) a mixture that gives the short-untouched population
probability **exactly 1** instead of `φ_U(c'')`. `DERIVATION_PREREG.md` §2.2
states explicitly, before any simulation, that the net sign was not known in
advance — because `φ_U(c'')`'s own implicit handling of short `π''`-cycles
(gradual, since `M-U`'s own blocks are single points) had not been
analytically compared to `M-CLUST(b)`'s (all-or-nothing) handling, only
flagged as a mismatch in kind.

**Sized from the formula alone** (`sc_formula.py`, `sc_formula_selfcheck.log`,
§5 below): at the target cell, `w_short≈0.359%`, and `φ_cond_C` sits **+5.6%
above** `φ_U(c'')` — already the wrong direction relative to the referee's
`z≈−10.86` (measured M-CLUST **below** `φ_U(c'')`). Across the full 6-cell
grid `φ_REDC` sits `+1.6%` to `+6.4%` **above** `φ_REDB`, uniformly the wrong
sign relative to what the residual needs, at every one of the six cells.
**This was written down and reported before any Monte Carlo confirmed it.**

---

## 3. T1 — the diagnostic split (the load-bearing measurement)

`sc_diagnostic.py`, own engine, three cells, N=2500 each. For every instance,
the whole functional graph is built once and the whole cyclic mask computed
once (in-degree peeling); every `R^c` point of that one instance is then a
sample of "x₀", split by whether its own π-cycle length is `≤b` (the
short-untouched bucket, `su`) or `>b` (`long`). No walk is simulated and no
formula enters the measurement side.

**Sanity check, hundreds of thousands of points, zero exceptions:**
`φ(cyclic | short & untouched)` measures **exactly 1.000000 ± 0.000000** in
all three cells (128,504 / 751,282 / 392,960 total short-untouched points
respectively) — the mechanism claim of §1 is not approximately true, it is
exact, and the simulator reproduces it at machine precision.

**The long-cycle population, on its own, deviates sharply from `φ_U(c'')`
— and not in the direction `φ_REDC` assumed:**

| cell (b,c,ρ) | φ(long, x0∈R^c) | φ_U(c'') | dev% | z |
|---|---|---|---|---|
| 100, 1000, 0.785 (target) | 0.054957 ± 0.000611 | 0.059993 | **−8.40%** | −8.25 |
| 400, 100, 0.457 | 0.111104 ± 0.001258 | 0.120185 | **−7.56%** | −7.22 |
| 200, 150, 0.368 | 0.086576 ± 0.000975 | 0.090890 | **−4.75%** | −4.43 |

The long-cycle-only population is **below** `φ_U(c'')` by 4.7–8.4%, highly
significantly. This is the opposite of what mixing in the guaranteed-1
short-untouched bucket needs to explain a net *deficit* — and it is much
larger in magnitude than the aggregate residual (1–3%) this whole lineage
has been chasing. The overall `φ(cyclic|x0∈R^c)` (mixing both buckets) comes
out **less negative** than the long-only figure precisely because the small
(0.36–0.84% weight) guaranteed-1 bucket partially offsets it:

| cell | φ(x0∈R^c, overall) | φ_U(c'') | dev% | z | w_short |
|---|---|---|---|---|---|
| 100, 1000 (target) | 0.058426 ± 0.000606 | 0.059993 | −2.61% | −2.59 | 0.365% |
| 400, 100 | 0.118629 ± 0.001250 | 0.120185 | −1.30% | −1.25 | 0.844% |
| 200, 150 | 0.090049 ± 0.000971 | 0.090890 | −0.93% | −0.87 | 0.379% |

These overall numbers are consistent in sign and rough magnitude with the
referee's own high-precision T3 result (`z≈−10.86`, `dev≈−1.03%` at the
target cell, 300k–400k instances) — my 2000–3000-instance runs are noisier
(as expected) but land in the same place. **The two effects this front
identifies — a genuine, large, negative long-cycle deficit, and a small,
positive, exactly-derived short-cycle boost — are of comparable order and
opposite sign, and they very nearly cancel, which is exactly why `φ_REDB`
(which models neither) has looked "almost right" for five waves.**

### 3.1 A finer diagnostic: binning by π-cycle length

Binning the long (`L>b`) population by `L` (edges `b,2b,5b,20b,∞` — fixed
before looking at any data) reveals the deficit is **not** uniform in `L`,
and the true structure is considerably richer than a two-bucket split:

| cell | L∈(b,2b] | L∈(2b,5b] | L∈(5b,20b] | L∈(20b,∞) |
|---|---|---|---|---|
| 100,1000 | **+267.7% (z=+11.7)**, n=52,943 | −11.0% (z=−1.4), n=160,974 | −23.5% (z=−5.5), n=786,448 | −9.7% (z=−9.4), n=34.1M |
| 400,100 | **+328.2% (z=+28.0)**, n=510,648 | **+71.5% (z=+9.8)**, n=1.69M | −11.9% (z=−3.6), n=8.08M | −14.7% (z=−13.3), n=78.0M |
| 200,150 | **+569.7% (z=+39.0)**, n=318,964 | **+203.4% (z=+18.4)**, n=948,265 | −3.7% (z=−0.9), n=4.75M | −10.7% (z=−9.7), n=97.2M |

(Full tables: `sc_diag_cell0_target.log`, `sc_diag_cell1_b400c100.log`,
`sc_diag_cell2_b200c150.log`.)

**Two robust, highly significant (z up to +39) findings, both new to this
lineage:**

1. **Cycles of length just above `b` (roughly `b` to `~5b`) show a large,
   positive excess over `φ_U(c'')`** — up to +570% — driven by the *same*
   mechanism as §1's exact result, extended past the `L≤b` cutoff: **any**
   cycle, of **any** length, that happens to be completely untouched by
   every seed is deterministically an `f`-cycle. For `L` a few multiples of
   `b`, `(1−p)^L` is no longer astronomically small (e.g. at the target
   cell, `p=c/n≈0.01526`, so `(1−p)^{150}≈0.10`), so a non-negligible
   fraction of even moderately-long cycles are fully untouched, and this
   pulls the bin average sharply upward. A simple, no-new-parameter,
   two-state approximation — treat every cycle as either "fully untouched
   (prob 1)" or "touched (prob `φ_U(c'')` as before)", the *same* logic as
   `φ_cond_C` but applied to **every** `L`, not only `L≤b` — predicts
   `+159%` for the target cell's `(100,200]` bin (representative `L=150`)
   against the measured `+267.7%`: right sign, right order of magnitude,
   under by a factor ≈1.7 (the `φ_U(c'')` value used for the "touched" state
   is itself too low for a moderately-short *partly*-touched cycle, whose
   surviving connected arc is still far more self-contained than a generic
   long-cycle background — a second-order effect not modeled). **This is
   reported as a qualitative, illustrative cross-check, explicitly not a
   validated closed form** — no new formula is proposed from it, per
   `DERIVATION_PREREG.md` §3's pre-committed handling of a post-hoc finding.
2. **For `L` genuinely large (the bulk of the `R^c` population by point
   count — 34–97 million of the ≈35–89 million total `R^c` points measured
   per cell), the deficit relative to `φ_U(c'')` settles at a persistent,
   roughly constant `−10%` to `−15%`, not shrinking further as `L` grows
   from `20b` to `n`.** This is a **third, independent finding**, distinct
   from both the short-cycle-absorption mechanism this front targeted and
   the moderate-`L` untouched-cycle excess of item 1: it says `φ_U(c'')`
   itself is biased by an order of magnitude larger than the final aggregate
   residual, *even restricted to the asymptotically-long-cycle population
   the mean-field reduction is supposed to describe best*. This front does
   **not** explain this third effect — it is reported honestly as open
   (§9 item 1).

The one intermediate cell (target only) that breaks the otherwise-monotonic
"large positive near `b`, settling to a constant negative plateau" pattern is
`(500,2000]`, at **−23.5% (z=−5.5)** — *more* negative than either
neighboring bin. This is not explained here either; it is flagged, not
smoothed over.

> **[Correção pós-adversarial, 2026-08-23.]** As estimativas pontuais desta
> seção para os bins `(b,2b]` e `(2b,5b]` (a tabela acima e o item 1 logo
> abaixo) **não são reprodutíveis** sob remedição independente: o referee
> mediu, com duas sementes frescas independentes na célula-alvo,
> `+874,3%` e `+795,8%` (não `+267,7%`) para o bin `(b,2b]` — uma diferença
> consistente de `1,3×`–`3,3×` nas três células testadas, incluindo
> inversão de sinal no bin `(2b,5b]` da célula-alvo. O referee rastreou a
> causa: a subpopulação de ciclos totalmente intocados responde por
> **54,6%** da população condicional-a-`R^c` do bin `(b,2b]` na célula-alvo
> — muito mais que a estimativa não-condicional (`≈11%`) que o modelo de
> dois estados desta seção usa implicitamente, porque condicionar em
> `x0∈R^c` é, por si só, um forte efeito de seleção a favor de ciclos
> intocados (que contribuem *todos* os seus pontos a `R^c`, contra o arco
> residual encolhido de um ciclo tocado). Usando o peso correto (54,6%) no
> mesmo modelo de dois estados desta seção, a previsão sobe para `≈+855%`
> — muito mais perto do que o referee mediu do que da figura original desta
> tabela. **O bin de cauda longa `(20b,∞)` e a forma qualitativa
> (excesso grande perto de `b`, assentando num platô negativo persistente)
> replicam de forma robusta e independente — inclusive mais fortemente no
> pico perto de `b` do que aqui relatado.** A anomalia do bin `(500,2000]`
> mencionada acima também não replicou como característica isolada em três
> remedições independentes do referee (`−9,1%`, `−2,2%`, `−11,8%`,
> nenhuma claramente mais extrema que o platô vizinho) — consistente com
> ruído comum, não um efeito robusto. Nada disto ameaça o veredito desta
> frente: estes números específicos já eram tratados aqui como
> ilustrativos, nunca adotados como fórmula (ver nota logo abaixo). Ver
> `adversarial/REFEREE_REPORT.md` §4.2.

---

## 4. T0 — mechanism self-consistency

`sc_engine.py selftest` (`sc_engine_selftest.log`):

```
(a) rho_measured vs 1-(1-c/n)^b, 30 instances/cell, 8 cells: all |z|<1.7  OK
(b) R^c subseteq U_rem -- always: 40 instances, 0 violations  OK
(c) untouched cycle length<=b is exactly a cycle of f: 2389 short-cycle
    points examined, 0 violations  OK
(d) touched short (L<=b) cycle has zero run starts: 38 touched short cycles
    examined, 0 violations  OK
(e) cyclic_mask_peeling vs brute-force orbit-following: 200 random small
    functional graphs, 0 mismatches  OK
ALL SELFTESTS PASSED
```

A batched (vectorized-across-instances) peeling variant was also written
(`sc_batch.py`) and cross-checked against the per-instance peeling above (0
mismatches on 40 instances) — but rejected for production use: M-CLUST(b)'s
functional graph can carry very long tails (a long, mostly-untouched π-cycle
cut open by a single seed anywhere on it forms a tail of length up to
`O(n)`), and round-synchronized batched peeling pays one round per tail
*layer* across the *whole* batch, which is slower in wall-clock terms than
per-instance deque-based peeling despite doing the same total `O(n)` work.
Kept in the subfolder for the record; not used for any reported number.

---

## 5. Formula self-checks

`sc_formula.py` (`sc_formula_selfcheck.log`): `φ_REDB → φ_U(c)` and
`φ_REDC → φ_U(c)` as `n→∞` at fixed `(b,c)`, both differences shrinking by
almost exactly 16× per doubling of `n` (i.e. `O(1/n)`), from `2^16` through
`2^28`; the exact identity `P(R^c)+P(R)=1` holds to `<1e-12`; `φ_REDC` stays
in `(0,1)` and moves uniformly **above** `φ_REDB` (`+1.6%` to `+6.4%`) on all
six grid cells.

---

## 6. T2/T3 — formula-free measurement on the 6-cell grid

`sc_reduction.py`, own engine, one instance-batch per cell (N=2000, target
cell N=3000), no formula on the measurement side. `φ(cyclic|x0∈R^c)` and
full `φ` measured directly; scored against `φ_U(c')` (superseded), `φ_U(c'')`
(`φ_REDB`'s conditional / `φ_REDB` full), and `φ_cond_C`/`φ_REDC` (this
front).

| cell (b,c,ρ) | φ_Rc measured | φ_REDB dev% (z) | φ_REDC dev% (z) | φ full measured | φ_REDB full dev% (z) | φ_REDC full dev% (z) |
|---|---|---|---|---|---|---|
| 50, 400, 0.264 | 0.051474±0.000606 | −0.02% (−0.01) | −1.63% (−1.41) | 0.038214±0.000450 | −0.01% (−0.00) | −1.62% (−1.40) |
| 100, 400, 0.457 | 0.059409±0.000683 | −0.98% (−0.86) | **−4.13% (−3.75)** | 0.032658±0.000377 | −0.72% (−0.62) | **−3.89% (−3.50)** |
| 100, 600, 0.601 | 0.058779±0.000675 | **+3.05% (+2.57)** | −1.03% (−0.90) | 0.024019±0.000276 | **+3.23% (+2.72)** | −0.85% (−0.75) |
| 200, 150, 0.368 | 0.088372±0.001047 | **−2.77% (−2.41)** | **−6.39% (−5.76)** | 0.056134±0.000670 | **−2.68% (−2.31)** | **−6.37% (−5.70)** |
| 400, 100, 0.457 | 0.118285±0.001357 | −1.58% (−1.40) | **−7.28% (−6.84)** | 0.064716±0.000760 | −1.09% (−0.94) | **−7.01% (−6.42)** |
| **100, 1000, 0.785 (target)** | 0.059011±0.000571 | **−1.64% (−1.72)** | **−6.88% (−7.64)** | 0.013624±0.000131 | **−1.55% (−1.63)** | **−6.63% (−7.37)** |
| **pooled χ² (6 cells)** | | **18.1** | **155.0** | | **16.7** | **143.1** |

**Interpretation, all 6 cells.** `φ_REDB` already does well at low `ρ`
(`b=50,c=400`, `z≈0`); its worst cells here are `b=100,c=600` (+3.05%,
`z=+2.57`) and `b=200,c=150` (−2.77%, `z=−2.41`), with the target cell
(`b=100,c=1000,ρ=0.785`) at −1.55% full / `z=−1.63` — smaller in magnitude
than the referee's own high-precision figure (`dev≈−1.03%` to `−1.3%`,
`z≈−10.86` at 300k–400k instances) but consistent in sign and rough size at
this front's much lower instance count (N=3000 here vs. their N=300k+ — the
factor-of-~6 gap in `|z|` is exactly what the `~10×` smaller sample predicts
for a fixed underlying effect size).

`φ_REDC` **helps** exactly the one cell (`b=100,c=600`) where `φ_REDB`
already overshoots, dragging it from `z=+2.72` to `z=−0.75` — but it
**hurts every other cell**, including the target cell itself, which moves
from `z=−1.64` (already a real but modest residual) to `z=−7.39` — a
dramatically *worse* fit than `φ_REDB`. Pooled over all 6 cells, χ² rises
from 16.7 (`φ_REDB`, full φ) to 143.1 (`φ_REDC`) — an **8.6× degradation**,
not an improvement (conditional-`φ_Rc` scoring: 18.1 → 155.0, 8.6× as well).
This is the referee's own `φ_REDX` failure pattern reproduced independently,
on a different candidate, more starkly: **`φ_REDX` "repaired the worst cell
but overshot two others"; `φ_REDC` repairs one cell and overshoots all five
others, including the one it was built to fix.**

---

## 7. Refutation, exactly per the pre-registered criterion

`DERIVATION_PREREG.md` §3, T2 criterion: *"this front's correction is judged
a SUCCESS only if it reduces |z| on the target cell (100,1000,65536) by at
least 30% without increasing |z| on any of the other 5 cells beyond
max(2×its φ_REDB |z|, 2.5)."*

**On the target cell itself, `φ_REDC` moves the wrong way**: `|z|` (full φ)
goes from `1.64` (`φ_REDB`) to `7.39` (`φ_REDC`) — a **4.5× increase**, not
the required 30% decrease. The primary success condition fails outright, on
the one cell this front exists to fix. It also independently fails the
"don't damage the other five" condition: `b=100,c=400` goes from `|z|=0.62`
to `3.51` (exceeds `max(1.25,2.5)=2.5`), `b=200,c=150` from `2.31` to `5.70`
(exceeds `max(4.62,2.5)`... within bound numerically but the direction is a
2.5× worsening of an already-real residual), and `b=400,c=100` from `0.94`
to `6.42` (exceeds `max(1.89,2.5)=2.5`). **`φ_REDC` is refuted on both
pre-registered conditions independently, and on the target cell it was
built for.**

---

## 8. What this front establishes, and what it does not

**Established, mechanism-level, at machine precision:**
The referee's diagnosis is exactly right, and stronger than stated: any
π-cycle — not only those of length `≤b` — that is completely untouched by
every seed is **deterministically** an `f`-cycle. For `L≤b` this is the only
way `x₀` can be in `R^c` at all (§1); for `L` up to a few multiples of `b`
it remains a *non-negligible* probability event that materially lifts the
bin average (§3.1); it decays to irrelevance only once `L≫1/p=n/c`.

**Established, at the level of clear, high-|z| Monte Carlo evidence:**
The long-cycle population (`L>b`) deviates from `φ_U(c'')` by 4.7–8.4%
(three cells, |z| 4.4–8.3) — much larger than the 1–3% aggregate residual —
and this deviation is *itself* non-monotonic in `L`: strongly positive just
above `b`, settling to a persistent ≈−10% to −15% plateau for asymptotically
long cycles. **The small aggregate residual this whole lineage has chased
since wave 7 is the near-cancellation of two much larger, opposite-signed
effects, neither of which any formula in this lineage — including this
front's own `φ_REDC` — currently models.**

**Refuted:** the pre-registered candidate `φ_REDC`, which assumed the
long-cycle population is well-described by `φ_U(c'')` and only needed a
short-cycle correction on top. It is not: `φ_U(c'')` is *not* a good
long-cycle-only value (§3), so adding a purely-positive correction to it
overshoots, exactly like the referee's `φ_REDX` — confirmed on 6/6 grid
cells directly (§6), refuted by its own pre-registered criterion (§7).

**Not attempted:** deriving closed forms for either of the two newly-isolated
effects (the moderate-`L` untouched-cycle excess, the persistent long-`L`
plateau). Both would need genuinely new derivations — the first requires
integrating the untouched-cycle probability against a *properly-modeled*
touched-cycle conditional (not `φ_U(c'')`, which this front's own diagnostic
shows is not that conditional even at the asymptotic end); the second
requires understanding why the master formula's own mean-field construction
is biased by ~10% for a population it is nominally built for, which is a
question about the master formula itself, not about `M-CLUST(b)`'s
seed/run mechanism — out of this front's scope and budget.

---

## 9. Honesty — established / heuristic / open

**Established (derived from the mechanism, verified deterministically and
statistically, fresh seeds, own engine):**
1. Full-`b`-point-run reconciliation of the mechanism (§1, `DERIVATION_PREREG.md`
   §1.1) — internally consistent, reproduces `ρ=1−(1−c/n)^b` to `|z|<1.7`
   over 8 cells.
2. Untouched π-cycle (any length) ⟹ deterministic `f`-cycle: exact identity,
   confirmed on >1.2M short-cycle points combined across 3 cells with **zero**
   exceptions.
3. Touched short (`L≤b`) cycle ⟹ zero run starts anywhere on it, permanently
   unreachable by normal steps: confirmed deterministically on every touched
   short cycle examined (0 violations).
4. The long-cycle (`L>b`) population deviates from `φ_U(c'')` by 4.7–8.4%,
   |z| 4.4–8.3, three cells (§3).
5. The deviation is non-monotonic in `L`: large positive near `b`, negative
   plateau for large `L` (§3.1), |z| up to 39 in the most significant bins.
   **[Correção pós-adversarial, 2026-08-23: a forma qualitativa é
   CONFIRMADA, de forma ainda mais forte no pico perto de `b` do que
   relatado aqui — mas as estimativas pontuais especificas dos bins
   `(b,2b]`/`(2b,5b]` desta tabela não são reprodutíveis (o referee mediu
   valores ~2-3× maiores). Ver adendo completo em §3.1 acima.]**

**Heuristic / illustrative, explicitly not adopted as a formula:**
1. The "untouched-vs-`φ_U(c'')`" two-state approximation, extended past
   `L≤b`, predicts the right sign and order of magnitude for the
   moderate-`L` excess but undershoots by roughly 1.7× (§3.1 item 1). Not a
   candidate formula; reported only as supporting evidence for the
   mechanism. **[Correção pós-adversarial, 2026-08-23: o referee mostrou
   que o modelo de dois estados, com o peso condicional-a-`R^c` correto
   (54,6%, não ~11%), na verdade prevê `≈+855%` — muito mais perto do
   que o referee mediu (+796% a +874%) do que da figura original desta
   seção. O modelo não estava "quase certo, subestimando por 1,7×"; a
   estimativa original de "1,7×" comparava contra o número medido errado.
   Ver §3.1 acima.]**

**Refuted:**
1. `φ_REDC` (§2, §6, §7) — the pre-registered candidate. Helps one of six
   cells measured, hurts the other five (including the target cell it was
   built for), refuted by its own pre-registered criterion.

**Open, named, not pursued (this front's honest non-closure):**
1. **Why does the long-cycle population settle at a persistent ~−10% to
   −15% deficit relative to `φ_U(c'')`, not shrinking as `L→n`?** This is
   larger than any effect this lineage has previously isolated for this
   quantity and is not explained by the short-cycle mechanism this front
   targeted. It may indicate a bias in the master formula's mean-field
   construction itself (Poissonization/independence approximation,
   `DERIVATIONS.md` §6 item 1) that happens to be *specific to M-CLUST(b)'s*
   correlated block structure rather than a generic finite-`n` artifact —
   this front does not distinguish between those possibilities.
2. **A closed form for the moderate-`L` (`b` to `~10b`) excess** — sketched
   qualitatively (§3.1 item 1) but not derived to the precision needed to
   improve on `φ_REDB`.
3. **The `(500,2000]` non-monotonic dip** at the target cell (§3.1) is
   unexplained. **[Correção pós-adversarial, 2026-08-23: o referee
   remediu esta região três vezes de forma independente (−9,1%, −2,2%,
   −11,8%) e não encontrou nenhuma delas mais extrema que o platô
   vizinho — consistente com ruído comum, não uma característica robusta
   isolada. Ver §3.1 acima.]**
4. The `eps` channel (`x₀∈R`) was left entirely unmodified from `φ_REDB`
   throughout — its own short-cycle-absorption sensitivity (a small
   population, §2.1 of `DERIVATION_PREREG.md`) was not investigated.
5. Whether a correction exists that reduces the target cell's residual
   *without* worsening the other five remains **genuinely open** after this
   front. The two effects isolated here (§3, §3.1) are large enough that a
   correct treatment of both together might close it — but building that
   treatment is future work, not something this front's budget reached.

---

## 10. Verdict

> **HONEST NON-CLOSURE, with a genuine mechanism-level advance.** This front
> confirms, at machine precision and far more strongly than the referee's own
> diagnosis required, that untouched π-cycles of **any** length are
> deterministically closed under `f` — not only the `L≤b` cycles the
> referee's remark named. It shows this fact, extended past `L≤b`, produces
> a large, highly significant (|z| up to 39) positive excess over `φ_U(c'')`
> for cycles a few multiples of `b` long — a phenomenon not previously
> reported anywhere in this lineage. It also shows, independently, that the
> long-cycle population (`L>b`) as a whole sits 4.7–8.4% below `φ_U(c'')`,
> settling to a persistent ~10–15% deficit for asymptotically long cycles —
> an effect an order of magnitude larger than the aggregate residual this
> lineage has chased since wave 7, currently unexplained by any formula in
> this lineage.
>
> **The pre-registered candidate `φ_REDC`, built from the exact
> short-cycle-absorption fact alone, is REFUTED.** It assumed the long-cycle
> population is adequately described by `φ_U(c'')`, which §3 shows is false;
> adding a purely-positive correction on top of an already-too-high baseline
> overshoots, on 5 of 6 grid cells measured, pooled χ² rising 8.6× (§6)
> (helping only the one cell where `φ_REDB` itself already overshoots, and
> by coincidence, not by design). This reproduces — independently, on a
> different candidate, with a different (and sharper) mechanistic diagnosis
> — exactly the failure mode the referee's own `φ_REDX` showed in
> `adversarial/REFEREE_REPORT.md` §11.
>
> **`φ_REDB` remains the formula of record.** This front does not propose a
> replacement. The referee's diagnosis — "the DINAMICA changes on short
> cycles, not just the densities" — is correct as far as it goes, but this
> front's own diagnostic shows the required fix is not "add a short-cycle
> term to `φ_U(c'')`"; it is "replace `φ_U(c'')` itself, for the long-cycle
> conditional, with something that is not yet derived," a strictly harder
> problem than the one this front set out to solve.
>
> The `U_{1/2}` classification in the `n→∞` limit is completely untouched:
> nothing above questions it, and `φ_REDC → φ_U(c)` exactly as `φ_REDB`
> does, by the same `ρ→0` argument (§5).
>
> **This document requires independent mandatory adversarial verification
> before any integration into governance**, exactly as every predecessor
> document in this lineage. It is not integrated, and `φ_REDB` is not
> declared superseded.

---

## 11. Files

| file | role |
|---|---|
| `ATTEMPT.md` | this document |
| `DERIVATION_PREREG.md` | pre-registration, written and saved before any simulation |
| `sc_engine.py` / `sc_engine_selftest.log` | own M-CLUST(b) engine + selftest (T0, §4) |
| `sc_batch.py` / `sc_batch_selftest.log` | a rejected batched-peeling optimization, kept for the record (correctness cross-checked, 0/40 mismatches, but round-count blew up on the long tails specific to this mechanism — §4) |
| `sc_formula.py` / `sc_formula_selfcheck.log` | closed forms: `φ_U`, `T_U`, `φ_REDB` (reused/re-transcribed), the exact short-cycle combinatorics, `φ_cond_C`, `φ_REDC` (§5) |
| `sc_diagnostic.py` / `sc_diag_cell*.log` | T1, the cycle-length-conditioned split (§3) |
| `sc_reduction.py` / `sc_red_cell*.log` | T2/T3, formula-free measurement on the 6-cell grid (§6) |
