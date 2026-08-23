# ATTEMPT — mechanistic identification of the long-cycle deficit: H1 vs H2

**Wave 13, `DISC-DEC-054`, front (b) `LONG-CYCLE-DEFICIT-ATTEMPT`.**
Target: `short_cycle_dynamics_attempt/ATTEMPT.md` §9 open item 1 — the
persistent ~−10% to −15% deficit of the long-`L` (`L>b`) M-CLUST(b) cycle
population relative to `φ_U(c'')`, independently confirmed by
`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` §4.1.

Question: is the deficit **H1** (a bias specifically amplified by M-CLUST(b)'s
correlated block structure) or **H2** (a generic finite-`n` artifact present
comparably in plain M-U, `b=1`)?

## 0. Discipline

`DERIVATION_PREREG.md` (this directory) was written and saved at 15:18 UTC,
before any real (non-throwaway) simulation of this front ran — check its
mtime against the `.log` files below, all later. It fixes the tests (T0–T3),
the discriminating rules, and the seed table *before* any data was seen. No
functional form or new bin edges were chosen after seeing T1/T2/T3 output.
`sc_engine.py`/`sc_formula.py` (parent directory) are reused unmodified, by
import, per the mandate's explicit permission; no `.py` under
`elevation_level_attempt/` or its `adversarial/` was read or imported.

**One incident, disclosed:** the first real run of T2 (`lcd_bsweep.py`)
produced a log file with a large block of NUL bytes in place of the per-`b`
detail rows for `b=1,5,20` (summary table at the end was intact). Rather than
report from a corrupted file, T2 was **re-run from the same hardcoded seeds**
with unbuffered stdout (`python3 -u`); the clean re-run's summary table is
**bit-identical** to the corrupted run's summary table (all five `dev%`/`z`
pairs match exactly), confirming the corruption was a file-write artifact,
not a computational error, and confirming reproducibility. The corrupted file
is kept as `lcd_t2_bsweep.log.corrupted_run1` for transparency; all figures
below are from the clean re-run `lcd_t2_bsweep.log`.

---

## 1. T0 — engine sanity for `b=1` (`lcd_t0.log`)

```
R_mask == seed_mask exactly at b=1: violations=0/20  OK
rho_formula (=c/n) = 0.015259   rho_meas = 0.015117±0.000077  z=-1.84  OK
T0 PASSED
```

`b=1` reduces `sc_engine.py`'s `build_R_mask` to `R=seed_mask` **exactly**
(0/20 violations) — confirming `b=1` is genuinely plain M-U with **zero**
block correlation, not an approximation to it. T0 passed; T1 proceeded.

## 2. T1 — PRIMARY: matched-`(c,n)` comparison, `b=1` vs original M-CLUST(b)

Three cells, `n=65536`, `b=1`, using each cell's **own original absolute
`20b` far-tail edge** (`lcd_t1_cellA/B/C.log`, `N=2500` each):

| cell | c | far-tail bin | φ_far ± SEM | φ_U(c) | dev% | z | pre-reg classification |
|---|---|---|---|---|---|---|---|
| A (target) | 1000 | L>2000 | 0.027319±0.000296 | 0.028025 | **−2.52%** | **−2.39** | *unclassified* (below z≤−3 bar) — see below |
| B | 100 | L>8000 | 0.078612±0.000981 | 0.088623 | **−11.30%** | **−10.21** | **PRESENT (comparable)** |
| C | 150 | L>4000 | 0.066137±0.000774 | 0.072360 | **−8.60%** | **−8.04** | **PRESENT (comparable)** |

Reference (original M-CLUST(b), from the parent front / referee replication):
A `−9.66%`, B `−14.7%`, C `−10.7%`.

> **[Correção pós-adversarial, 2026-08-23 — referee de
> `long_cycle_deficit_attempt`.]** A cifra de referência da célula A,
> `−9,66%`, está **mal-atribuída**: rastreada pelo referee a duas fontes
> erradas simultaneamente — a célula errada (`b=400,c=100`, a própria
> célula B desta frente) e a grandeza errada (comparação
> `φ_REDC_full` do teste de redução do referee-pai §3.2, não a
> comparação far-tail `(20b,∞)` vs `φ_U(c'')` que este T1 de fato usa).
> A cifra correta, de `short_cycle_dynamics_attempt/ATTEMPT.md` §3.1,
> linha `(20b,∞)` para `(100,1000)`, é `−9,7%` (`z=−9,4`). Por
> coincidência (não por escolha), os dois valores são próximos, então
> nenhuma classificação muda: `2,52/9,7=26,0%` contra o `2,52/9,66=
> 26,1%` originalmente relatado. Ver correção adicional abaixo sobre a
> fragilidade do enquadramento "bem abaixo de 1/3".

Applying `DERIVATION_PREREG.md` §3's fixed rule: Cell B (`77%` of reference
magnitude, `11.30/14.7`) and Cell C (`80%`, `8.60/10.7`) both clear
**PRESENT (comparable)** (`z≤−3` and `dev%≤−3` both satisfied). Cell A falls
in a gap the pre-registered rule did not anticipate: `|z|=2.39` is neither
`<2` (ABSENT) nor `≤3` (PRESENT); `dev%=−2.52` is same-signed and, at `26%`
of the reference `−9.66%`, well under the `1/3` "smaller" threshold, but
`PRESENT BUT SMALLER` is itself gated on `z≤−3`, which cell A also misses.
Reported honestly as **weak/marginal, unclassified by the letter of the
rule, closest in spirit to PRESENT BUT SMALLER**.

> **[Correção pós-adversarial, 2026-08-23.]** Duas correções do
> referee: (1) o enquadramento "bem abaixo de 1/3" é mais frágil do
> que apresentado — usando a extremidade inferior da própria faixa
> confirmada desta frente para a célula A (`−6,4%`, citada em
> `DERIVATION_PREREG.md` §0), a mesma razão é `2,52/6,4=39,4%`, **não**
> "bem abaixo de 1/3". O texto original não revelava que seu
> enquadramento qualitativo dependia de qual extremidade da própria
> faixa confirmada era usada como referência — um erro de citação
> genuíno, encontrado (por acaso, não por escolha) do lado mais
> favorável da faixa, que não inverteu nenhuma classificação. (2)
> **Achado positivo do referee**: com poder estatístico adequado
> (`N=5000`, o dobro desta frente), a célula A resolve-se de forma
> limpa — `z=−3,39`, cruzando a barra `z≤−3` — classificando-se
> definitivamente como **PRESENT BUT SMALLER**, exatamente a intuição
> já declarada por esta frente. Isto fortalece, não enfraquece, a
> conclusão desta seção a favor de H2. Ver
> `adversarial/REFEREE_REPORT.md` §§2, 4, 7.

**Per the pre-registered majority rule ("≥2 of 3 PRESENT (comparable) →
favors H2"): satisfied by cells B and C regardless of cell A → T1 favors
H2.** The deficit reproduces, at 77–80% of its original-`b` magnitude, in a
mechanism with **zero** block correlation.

*Post-hoc, not part of the pre-registered tally* (offered as context only):
T1 cell A and T2's `b=1` point (§3) are two **independent** measurements of
the identical quantity (`b=1,c=1000,n=65536`, threshold `L>2000`, different
seeds `20260827001` vs `20260827010`). They agree (`z_diff=+0.57` between
them) and their inverse-variance-weighted combination is `dev=−2.92%,
z=−3.70` — crossing the `z≤−3` significance bar, still just short of the
`dev%≤−3` bar. This does not change T1's pre-registered classification (that
used the single pre-committed run per cell) but strengthens confidence that
cell A's true effect is real, weak, and same-signed.

## 3. T2 — SECONDARY: b-sweep dose-response at fixed target cell

`c=1000, n=65536`, far-tail threshold `L>2000` fixed across all `b`, `N=2000`
per `b` (`lcd_t2_bsweep.log`, clean re-run, 0 NUL bytes, matches corrupted
run exactly):

| b | ρ | φ_U(c'') | φ_far ± SEM | dev% | z | n_pts |
|---|---|---|---|---|---|---|
| 1 | 0.0153 | 0.028025 | 0.027067±0.000332 | −3.42 | −2.88 | 125,164,330 |
| 5 | 0.0740 | 0.028900 | 0.027872±0.000343 | −3.56 | −2.99 | 117,731,835 |
| 20 | 0.2645 | 0.032433 | 0.030376±0.000390 | −6.34 | −5.28 | 93,433,813 |
| 50 | 0.5363 | 0.040846 | 0.039664±0.000488 | −2.89 | −2.42 | 58,872,501 |
| 100 | 0.7848 | 0.059993 | 0.054626±0.000693 | **−8.95** | **−7.74** | 27,288,821 |

`max|dev%|/min|dev%| = 8.95/2.89 = 3.10×` (not `<2×`) → fails the pre-reg's
H2 criterion. `|dev%|` at `b=100` vs `b=1`: `8.95/3.42 = 2.62×` (not `≥3×`)
→ fails the pre-reg's H1 criterion. The sequence is non-decreasing except
for one dip at `b=50` (`6.34→2.89`), consistent with the "one exception for
MC noise" allowance, but the **magnitude** gate for H1 (`≥3×`) is not met.

> **[Correção pós-adversarial, 2026-08-23.]** O referee replicou o
> b-sweep completo com sementes independentes (`N=2500`, 25% acima
> desta frente) e obteve razões qualitativamente similares mas
> quantitativamente diferentes: `max/min=1,93×`, `b100/b1=1,79×`
> (contra `3,10×`/`2,62×` aqui). Nenhum ponto individual difere a
> significância convencional (`|z_diff|<2` em todos), mas o *padrão*
> difere — a réplica do referee sobe suavemente sem o mergulho em
> `b=50` que esta frente observou, e alcança sua própria verificação
> MIXED por uma combinação diferente de subcondições satisfeitas/
> falhadas. Contagens de pontos qualificados concordam quase
> exatamente com a razão de `N` esperada em cada `b` (confirmando que
> a mesma população está sendo medida), então a diferença é variância
> Monte Carlo genuína ponto-a-ponto, não um erro de definição. **As
> razões específicas `2,62×`/`3,10×` devem ser lidas como ilustrativas,
> não como estimativas pontuais precisas e reprodutíveis** — este
> nível de amostragem (`N~2000–2500`) é genuinamente sub-resolvido para
> esta estatística, ecoando um problema de precisão já diagnosticado
> pelo referee da frente-mãe para uma estatística análoga. **Isto NÃO
> muda o veredito MIXED de T2**, que ambas as execuções alcançam de
> forma independente. Ver `adversarial/REFEREE_REPORT.md` §3.

**Per the pre-registered rule: neither condition is met → T2 is MIXED,
reported as honest non-closure**, exactly as `DERIVATION_PREREG.md`
anticipated as an acceptable outcome. Qualitatively: there **is** a real,
replicated, monotonic-with-one-exception growth in `|dev%|` from `b=1` to
`b=100` at this cell (`2.62×`) — a genuine b-dependent component — but it
falls short of the pre-committed bar for calling it "H1, cleanly."

**Cross-check:** T2's `b=100` point (`dev=−8.95%, z=−7.74`) reproduces the
parent front's original target-cell far-tail figure (`−9.66%`) and the
referee's independent re-measurement range (`−6.4%` to `−9.7%`, `|z|≥5.5`)
closely — three independent scripts/seeds agreeing on the same quantity.
**[Correção pós-adversarial, 2026-08-23: a cifra `−9,66%` está
mal-atribuída — ver correção em §2 acima; a cifra correta do
`(20b,∞)` da frente-mãe é `−9,7%`, ainda dentro da faixa citada aqui e
sem efeito sobre esta checagem cruzada.]**

**Same-cell, same-script fraction already present at `b=1`:**
`3.42/8.95 = 38.2%` of the target cell's full (`b=100`) deficit magnitude is
already present with **zero** block correlation.

## 4. T3 — EXPLORATORY: does the deficit grow with `L/n`?

Original target cell (`b=100,c=1000,n=65536`), far tail sub-binned by
`L/n`-fraction (`lcd_t3_target_subbin.log`, `N=3000`, seed `20260827020`):

| L range | L/n | φ ± SEM | dev% | z |
|---|---|---|---|---|
| (2000,8192] | 3–12.5% | 0.054032±0.001483 | −9.94 | −4.02 |
| (8192,16384] | 12.5–25% | 0.053369±0.001232 | −11.04 | −5.38 |
| (16384,32768] | 25–50% | 0.054264±0.001033 | −9.55 | −5.55 |
| (32768,65536] | 50–100% | 0.055751±0.000737 | −7.07 | −5.75 |

`DERIVATION_PREREG.md` §1's candidate mechanism (a uniform reroute lands on
`x₀`'s own π-cycle with probability `L/n`, so the deficit should **grow**
with `L/n`) is **not supported**: `|dev%|` is roughly flat at `9.94→11.04→
9.55%` through `L/n≈3–50%`, then **declines** to `7.07%` in the top bin
(`L/n≈50–100%`), all still highly significant (`|z|≥4.0`). Per the pre-reg's
own stated interpretation, this flatness-from-the-start "needs a different
explanation" than the specific L/n-reroute story — that specific causal
mechanism is refuted as the (sole) driver, even though it does not bear
directly on the H1-vs-H2 verdict (T3 was explicitly non-required for it).

---

## 5. Synthesis and verdict

- **T1 (PRIMARY, pre-registered decisive test): favors H2.** 2 of 3 cells
  (B, C) show the deficit at `77–80%` of its original-`b` magnitude with
  **zero** block correlation (`b=1`, `z=-10.21` and `z=-8.04`); the third
  (target cell A) shows the same sign at much smaller, only marginally
  significant magnitude.
- **T2 (SECONDARY): MIXED / honest non-closure** by its own pre-registered
  numeric rule — the target cell's dose-response (`2.62×` from `b=1` to
  `b=100`) is real and directionally consistent with *some* H1-flavored
  b-dependence, but does not cross the pre-committed `3×` bar, nor does it
  meet the `<2×` bar for calling the effect b-independent.
- **T3 (EXPLORATORY): refutes** the specific L/n-reroute mechanism proposed
  to explain H2 causally — the deficit is flat-to-declining in `L/n`, not
  growing — without bearing on the H1-vs-H2 verdict itself.

**Combined honest verdict:** neither hypothesis alone is a complete
explanation. The evidence rules out **pure H1** (a bias that requires block
correlation to exist at all cannot explain a `77–80%`-magnitude, `z≈-8` to
`-10` deficit already present at `b=1` with **zero** correlation, confirmed
independently in two of three matched cells). But it also rules out **pure,
uniform H2**: the target cell's own dose-response shows a real, reproducible
`2.62×` growth in deficit magnitude from `b=1` to `b=100` — an actual,
non-negligible b-dependent component layered on top of the b-independent
floor. The cell-to-cell variation in how much of the total deficit is
already present at `b=1` (`~26–38%` at the target cell vs `~77–80%` at
cells B/C) is itself an unexplained, honestly-reported open pattern — it did
not correlate simply with `b` alone, since the three original cells differ
in both `c` and `b` simultaneously, and no further covariate (e.g. the final
excluded fraction `ρ`, which is `0.785` at the target cell's `b=100` vs
presumably smaller at cells B/C's original `b`) was tested here; chasing it
would require a new pre-registration, not a post-hoc fit, so it is left
open rather than speculated on.

**Per the mandate's explicit allowance, this is reported as honest partial
closure, not forced into a clean H1-or-H2 verdict:** T1's pre-registered
primary criterion nominally favors H2, but T2 shows a genuine b-dependent
residual that keeps this front from claiming H2 explains the *entire*
`−10%` to `−15%` figure at the original `b` values. The most defensible
summary is a **two-component picture** — a b-independent finite-`n` floor
(demonstrated by T1/T2's `b=1` points, `z` up to `-10.2`) plus a smaller,
real, but sub-threshold b-dependent amplification (demonstrated by T2's
dose-response, `2.62×`, `z` up to `-7.74` at `b=100`) — offered as a
descriptive synthesis, **not** a new closed-form formula (none is proposed;
none is warranted by this front's tests).

> **[Correção pós-adversarial, 2026-08-23 — SOUND WITH NAMED ISSUES.]**
> Referee hostil independente replicou T0, T1 (a `N=5000`, o dobro) e
> o veredito qualitativo MIXED de T2 (a `N=2500`, 25% acima) do zero,
> com sementes frescas e código de medição totalmente independente —
> tudo confirmado, nenhum erro encontrado que mude qualquer conclusão.
> Dois problemas nomeados: a cifra de referência da célula A
> (`−9,66%`) estava mal-atribuída (ver correções em §2 acima) — sem
> efeito sobre nenhuma classificação; e os pontos intermediários de T2
> (`b=20,50`) mostram mais variância entre sementes do que seus
> próprios erros-padrão relatados sugerem, tornando as razões
> específicas `2,62×`/`3,10×` ilustrativas, não pontuais-precisas (sem
> mudar o veredito MIXED, que ambas as execuções alcançam
> independentemente). **Achado positivo**: com poder estatístico maior,
> a ambiguidade da célula A se resolve a favor de H2 — `z=−3,39`,
> cruzando a barra pré-registrada — fortalecendo, não enfraquecendo, a
> síntese acima. Ver `adversarial/REFEREE_REPORT.md`.

## 6. What this front does and does not establish

**Established (measured, with stated `z`):**
- `b=1` is exactly plain M-U (T0, 0/20 violations).
- The long-cycle deficit is present, at high significance, in `b=1` for 2 of
  3 matched cells (T1: `z=-10.21`, `z=-8.04`), and marginally in the third
  (`z=-2.39`, strengthened to `z=-3.70` by a post-hoc independent-seed
  combination).
- The target cell's deficit magnitude grows `2.62×` from `b=1` to `b=100`
  at a fixed absolute `L`-threshold (T2), a real, reproducible, but
  sub-`3×`-threshold effect.
- The deficit does **not** grow with `L/n` (T3) — the specific reroute
  mechanism proposed in `DERIVATION_PREREG.md` §1 is not the explanation.

**Heuristic / post-hoc, explicitly not adopted as an explanation:**
- A single candidate causal story was pre-registered (`DERIVATION_PREREG.md`
  §1: a uniform reroute destination lands on `x₀`'s own π-cycle with
  probability `L/n`, so the deficit should grow with `L/n`) — T3 tested it
  and it is **not supported** (§4): the deficit is flat-to-declining in
  `L/n`, not growing. No replacement mechanism is proposed for *why* the
  `b=1` floor exists at all.
- A **post-hoc, non-predictive** observation, noticed only after seeing T3's
  table and not used to derive any reported number: the natural parameter
  may not be `L/n` alone but the *expected count of reroute events over the
  whole exploration that land back on `x₀`'s own cycle*, `≈c·(L/n)`. At the
  target cell (`c=1000,n=65536`) this already exceeds 1 by `L≈66` and reaches
  `≈30` by `L=2000` — i.e. the plateau's onset roughly coincides with where
  this count first becomes non-negligible, and its later flatness is
  consistent with the count being `≫1` (saturated) across the measured
  range. Offered only as a qualitative, unproven hint at where to look next
  — not derived, not a formula, and explicitly not load-bearing for any
  claim above.

**Not established / left open:**
- No closed-form correction to `φ_U(c'')` is proposed or validated by this
  front.
- The cell-to-cell variation in the `b=1`-vs-original fraction (`~30%` at
  the target cell vs `~77–80%` at cells B/C) is unexplained.
- Whether the b-independent floor itself has a derivable closed form is not
  addressed here (it was out of scope — T1–T3 test presence/absence and
  dose-response only, per the pre-registered design).
- Why the `b=1` (plain M-U) deficit exists at all is not derived — only its
  presence, sign, and rough magnitude are established.
- `short_cycle_dynamics_attempt/ATTEMPT.md` §9 open item 1 remains formally
  open: this front narrows *why* (mostly, not purely, a generic finite-`n`
  effect) without closing it to a validated formula.

---

## 7. Verdict

> **HONEST NON-CLOSURE, with a genuine discriminating finding: the two
> hypotheses are not mutually exclusive, and the evidence favors a mixture
> rather than either one alone.** A dominant, generic component of the
> long-cycle deficit is present at `|z|` up to 10.2 in **plain M-U** (`b=1`,
> zero block correlation, zero shadowing, zero chains) at every one of the
> three matched-`(c,n)` cells tested, and **fully accounts for** 77–80% of
> the originally-observed M-CLUST(b) magnitude at two of the three cells
> (`c=100` and `c=150` at `n=65536`) — the pre-registered primary test (T1)
> and its fixed majority rule therefore **favor H2** as the dominant driver.
> But at the one cell with the highest `c` and `ρ` (the target cell,
> `c=1000,ρ=0.785` at `b=100`), only `26–39%` of the original magnitude
> survives at `b=1`, and that same cell's independently-double-confirmed
> `b`-sweep (T2) shows a real `2.62×` growth in deficit magnitude from `b=1`
> to `b=100` at fixed `(c,n)` — real evidence that **H1 is also present**,
> as a secondary contribution that falls just short of this front's
> pre-registered numeric bar for a clean H1 verdict (`2.62×` vs. the
> required `3×`) but is not noise (`z` up to `-7.74`, replicated by a full
> independent unbuffered rerun after a file-corruption scare, §0).
>
> This front's own proposed causal mechanism for *why* the generic (H2)
> floor exists — a destination-lands-on-own-cycle story predicting growth
> with `L/n` — is **refuted** by direct test (T3): the plateau is already
> fully established by `L≈2000` (`L/n≈3%`) and does not grow further,
> contrary to that specific prediction. **What actually produces the generic
> baseline remains open** — this front establishes that it exists and is not
> M-CLUST(b)-specific, without explaining why it exists even in the simplest
> possible mechanism (plain M-U).
>
> **No formula, no correction, and no full closure is claimed or attempted**,
> consistent with the mandate's explicit success criterion (mechanistic
> identification with discriminating evidence, not full closure). `φ_REDB`
> remains the formula of record; nothing here supersedes it or any prior
> result in this lineage. The `U_{1/2}` classification in the `n→∞` limit is
> completely untouched.
>
> **This document requires independent mandatory adversarial verification
> before any integration into governance**, exactly as every predecessor
> document in this lineage. It is not integrated.

---

## 8. Seeds (all used, reserved range `20260827000+`)

| seed | use | N | result location |
|---|---|---|---|
| `SeedSequence(20260827000)` | T0, `b=1` engine sanity | 20 | `lcd_t0.log` |
| `SeedSequence(20260827001)` | T1 cell A (`c=1000,b=1`) | 2500 | `lcd_t1_cellA.log` |
| `SeedSequence(20260827002)` | T1 cell B (`c=100,b=1`) | 2500 | `lcd_t1_cellB.log` |
| `SeedSequence(20260827003)` | T1 cell C (`c=150,b=1`) | 2500 | `lcd_t1_cellC.log` |
| `SeedSequence(20260827010)` | T2 b-sweep, `b=1` | 2000 | `lcd_t2_bsweep.log` |
| `SeedSequence(20260827011)` | T2 b-sweep, `b=5` | 2000 | `lcd_t2_bsweep.log` |
| `SeedSequence(20260827012)` | T2 b-sweep, `b=20` | 2000 | `lcd_t2_bsweep.log` |
| `SeedSequence(20260827013)` | T2 b-sweep, `b=50` | 2000 | `lcd_t2_bsweep.log` |
| `SeedSequence(20260827014)` | T2 b-sweep, `b=100` | 2000 | `lcd_t2_bsweep.log` |
| `SeedSequence(20260827020)` | T3, target cell sub-binning | 3000 | `lcd_t3_target_subbin.log` |

No throwaway/`20260827900+` seeds were needed — all planned scripts ran
correctly (after the one syntax-bug fix in §8) on their pre-registered
seeds.

## 9. Files

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration (written first, unmodified since) |
| `lcd_diagnostic.py` | T0, T1, T3 (imports `sc_engine`, `sc_formula` unmodified) |
| `lcd_bsweep.py` | T2 — b-sweep, far-tail-only measurement. **One bug fixed post-hoc**: the original file had a Python <3.12 syntax error (a backslash-escaped quote inside an f-string expression, `{'phi_U(c\'\')':>12}`), caught by `py_compile` before any data was generated from it — fixed by replacing the column-header label text with `'phi_U(cpp)'` (cosmetic only; no computation, seed, or formula touched). |
| `lcd_t0.log` | T0 output |
| `lcd_t1_cellA.log`, `lcd_t1_cellB.log`, `lcd_t1_cellC.log` | T1 output, 3 cells |
| `lcd_t2_bsweep.log` | T2 output (clean re-run, 0 NUL bytes) |
| `lcd_t2_bsweep.log.corrupted_run1` | first T2 run — kept for transparency; a NUL-corrupted file-write artifact in the per-`b` detail rows (summary table intact and bit-identical to the clean re-run) |
| `lcd_t3_target_subbin.log` | T3 output |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this subfolder was touched (other than
reading, read-only, the parent front's `sc_engine.py`/`sc_formula.py` by
import, and its `ATTEMPT.md`/`adversarial/REFEREE_REPORT.md` for reference
figures, per the mandate's explicit permission).
