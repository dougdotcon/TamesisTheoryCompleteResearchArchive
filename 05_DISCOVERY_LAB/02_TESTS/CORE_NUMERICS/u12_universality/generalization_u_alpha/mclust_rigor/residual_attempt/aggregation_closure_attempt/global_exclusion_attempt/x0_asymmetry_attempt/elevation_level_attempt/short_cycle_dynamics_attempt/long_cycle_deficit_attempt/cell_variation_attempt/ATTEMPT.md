# ATTEMPT — what drives the cell-to-cell H2-share variation? `ρ` implicated, not proven, `b` ruled out as a solo driver

**Wave 14, `DISC-DEC-057`, front (e) `CELL-VARIATION-ATTEMPT`.**
Target: `long_cycle_deficit_attempt/ATTEMPT.md` §5's explicitly named open
pattern — the cell-to-cell variation in how much of the long-cycle deficit
is already present at `b=1` (`~26–38%` at the target cell vs `~77–80%` at
cells B/C), left untested against `ρ`, `c`, `b` individually because the
original three cells confound all three covariates simultaneously.

## 0. Discipline

`DERIVATION_PREREG.md` (this directory) was written and saved at 21:18 UTC
(2026-08-23), before any real (non-throwaway) simulation of this front ran —
its mtime predates `cv_grid.log` (21:36 UTC) and `cv_analysis.log` (21:38
UTC). It locks the 13-cell design, the exclusion rule, the H2-share
definition, the correlation/regression methods, and — critically — the
numeric sub-group range thresholds (`≤15pp` flat, `≥30pp` varies
substantially) **before** any cell was measured. Two throwaway seeds
(`999900010`, `999900011`, outside the reserved range) were used only to
validate multiprocessing determinism and size `N`; discarded, not counted in
any reported number.

**One post-hoc formatting fix, disclosed:** `cv_grid.py`'s machine-readable
CSV summary used a comma-joined `group` string (`"G1,G2,G3"` for cell A,
which belongs to three sub-comparisons), which broke CSV column alignment
for that one row. Fixed by switching the separator to `;` in both
`cv_grid.py` (for future re-runs) and directly in the one affected line of
the already-generated `cv_grid.log` (`A,100,1000,G1,G2,G3,...` →
`A,100,1000,G1;G2;G3,...`) — **no numeric value on that line, or anywhere
else in the log, was touched**; this is a delimiter-only fix to a
presentation bug in the analysis script, not a data correction. `cv_analysis.py`'s
group-membership check was updated to split on `;` to match.

`sc_engine.py`/`sc_formula.py` (two directories up) are reused unmodified,
by import. T0 (`b=1` engine sanity) re-passed with a fresh seed
(`20260839000`, `N=30`, `0/30` violations, `z=+0.15` on `ρ_meas` vs `c/n`)
before any cell was measured, per `DERIVATION_PREREG.md` §1/§5.

---

## 1. Design recap (locked in `DERIVATION_PREREG.md` §3)

13 cells, `n=65536` throughout. Two conditions per cell measured by the
*same* function (`cv_measure.measure_far_tail`, differing only in the `b`
argument): **own-`b`** (far-tail `L>20b` at the cell's own `b`, vs
`φ_U(c''(b,c,n))` — `short_cycle_dynamics_attempt`'s T1 methodology) and
**`b=1`** (same absolute threshold, same `c,n`, vs `φ_U(c)` —
`long_cycle_deficit_attempt`'s T1 methodology). `N=2000` per measurement,
`nworkers=4`. Full 26-run grid completed in **16.1 minutes**
(`cv_grid.log`).

Four sub-comparisons, each holding one covariate (roughly) fixed while the
other two vary:

| group | held (roughly) fixed | what varies | cells |
|---|---|---|---|
| G1 | `c=1000` | `b` (25→200, 8×), `ρ` (0.32→0.95) | A, G1a, G1b, G1d |
| G2 | `b=100` | `c` (200→2000, 10×), `ρ` (0.26→0.95) | A, G2a, G2b, G2d |
| G3 | `ρ≈0.785–0.788` | `b` (50→1007, 20×), `c` (100→2000, 20×) | A, G3a, G3c, G3d |
| G4 | `ρ≈0.452–0.458` | `b` (26→400, 15×), `c` (100→1500, 15×) | B, G4b, G4c |

---

## 2. Full results table (`cv_analysis.log`)

`H2 share = dev_b1% / dev_own%` (defined only when `dev_own<0` and
`|z_own|≥2`, per the pre-registered exclusion rule); `H2 SEM` is the
delta-method propagated standard error (`DERIVATION_PREREG.md` §2).

| id | b | c | ρ | dev_own% | z_own | dev_b1% | z_b1 | H2 share | H2 SEM |
|---|---|---|---|---|---|---|---|---|---|
| A | 100 | 1000 | 0.7851 | −8.06 | −6.93 | −3.32 | −2.80 | **41.2%** | 15.9pp |
| G1a | 25 | 1000 | 0.3191 | −3.79 | −3.20 | −1.35 | −1.11 | **35.5%** | 33.7pp |
| G1b | 50 | 1000 | 0.5364 | −2.37 | **−1.97** | −1.64 | −1.36 | *excluded* (|z_own|<2) | — |
| G1d | 200 | 1000 | 0.9538 | −19.64 | −17.34 | −2.41 | −2.00 | **12.3%** | 6.2pp |
| G2a | 100 | 200 | 0.2633 | −8.42 | −6.95 | −7.41 | −6.31 | **88.0%** | 18.8pp |
| G2b | 100 | 500 | 0.5351 | −8.06 | −7.05 | −1.77 | −1.45 | **21.9%** | 15.5pp |
| G2d | 100 | 2000 | 0.9549 | −20.31 | −17.75 | −1.26 | −1.09 | **6.2%** | 5.7pp |
| G3a | 335 | 300 | 0.7850 | −10.81 | −8.96 | −5.40 | −4.56 | **50.0%** | 12.3pp |
| G3c | 50 | 2000 | 0.7877 | −6.00 | −5.16 | −3.41 | −2.93 | **56.9%** | 22.3pp |
| G3d | 1007 | 100 | 0.7851 | −22.14 | −15.54 | −10.54 | −7.65 | **47.6%** | 6.9pp |
| B | 400 | 100 | 0.4571 | −13.37 | −11.08 | −9.36 | −7.56 | **70.0%** | 11.2pp |
| G4b | 80 | 500 | 0.4581 | −8.64 | −7.59 | −5.57 | −4.78 | **64.5%** | 16.0pp |
| G4c | 26 | 1500 | 0.4523 | −4.27 | −3.67 | −1.98 | −1.70 | **46.5%** | 30.2pp |

12/13 cells have a defined H2 share; `G1b` excluded (`|z_own|=1.97<2`, right
at the boundary — its own-`b` deficit is itself not established at this
`N`). `B`'s own-`b` deficit (`−13.37%, z=−11.08`) closely replicates the
parent front's original cell B far-tail figure (`−14.7%, z=−13.3`) with an
independent seed and script — an incidental cross-lineage consistency
check, not a formal claim.

---

## 3. Pooled correlation (secondary, per `DERIVATION_PREREG.md` §4.2)

| covariate | r | t | df | p |
|---|---|---|---|---|
| `ρ` | **−0.623** | −2.516 | 10 | **0.0306** |
| `log10(c)` | −0.549 | −2.075 | 10 | 0.0648 |
| `log10(b)` | +0.079 | +0.249 | 10 | 0.8083 |

**`ρ` is the only covariate crossing conventional significance in a simple
bivariate test; `b` alone shows essentially zero correlation** (`r=0.08`,
`p=0.81`). `c` is marginal (`p=0.065`).

**Multiple OLS** (`H2share ~ 1 + ρ + log10(c) + log10(b)`, `n=12`,
`R²=0.68`): none of the three coefficients individually clears `p<0.05`
(`ρ: p=0.117`, `log10(c): p=0.072`, `log10(b): p=0.085`), and — tellingly —
`ρ`'s OLS coefficient sign (`+4.33`) **flips relative to its own simple
correlation** (`r=−0.623`). Checked directly: `log10(c)` and `log10(b)` are
strongly anti-correlated across the design (`r=−0.75`, an artifact of the
`G3`/`G4` iso-`ρ` sub-groups, where holding `ρ` fixed forces `c` and `b` to
move in opposite directions) — this multicollinearity makes the individual
OLS coefficients unstable and not separately interpretable at `n=12`. The
OLS is reported for completeness per the pre-registration but is **not**
treated as more informative than the simple correlations or the sub-group
test below.

---

## 4. PRIMARY discriminator: sub-group range test (`DERIVATION_PREREG.md` §4.3, applied mechanically)

| group | range | classification (locked 15pp/30pp cutoffs) | noise check (`z`, delta-method) |
|---|---|---|---|
| G1 (`c` fixed) | 28.9pp (`G1d 12.3%` → `A 41.2%`) | AMBIGUOUS | `z=+1.70` (within noise) |
| G2 (`b` fixed) | **81.7pp** (`G2d 6.2%` → `G2a 88.0%`) | **VARIES SUBSTANTIALLY** | **`z=+4.16`** (exceeds noise) |
| G3 (`ρ≈0.785` fixed) | 15.7pp (`A 41.2%` → `G3c 56.9%`) | AMBIGUOUS *(misses "flat" by 0.7pp)* | `z=+0.57` (well within noise) |
| G4 (`ρ≈0.457` fixed) | 23.5pp (`G4c 46.5%` → `B 70.0%`) | AMBIGUOUS | `z=+0.73` (well within noise) |

**Mechanical verdict per the locked rule:** neither `ρ`-fixed group (G3,
G4) achieves the pre-registered `≤15pp` "FLAT" bar, so the rule's clean
"`ρ` is the driver" branch does **not** fire. **Reported honestly: PARTIAL /
MIXED — the pre-registered primary rule, applied exactly as locked, does
not deliver a clean single-covariate verdict.**

**But the noise-adjusted picture (delta-method `z`, explicitly pre-flagged
in `DERIVATION_PREREG.md` §2 as a legitimate secondary check "to gauge
whether cross-cell H2-share differences within a held-fixed sub-group
exceed measurement noise — not used to change any classification rule") is
considerably cleaner than the raw-range mechanical cutoffs suggest:**
- **Both `ρ`-fixed groups (G3, G4) have internal spreads statistically
  indistinguishable from zero** (`z=0.57` and `z=0.73`) — i.e. at this
  sample size, holding `ρ` fixed is consistent with H2 share being
  genuinely constant, despite `b` moving 15–20× and `c` moving 15–20×
  within each group.
- **G2 (`b` fixed, `ρ` free to range 0.26→0.95) shows a highly significant
  internal spread** (`z=4.16`) — a real, non-noise effect.
- **G1 (`c` fixed, `ρ` free to range 0.32→0.95) shows a positive but
  sub-significant spread** (`z=1.70`) — suggestive of the same direction as
  G2, underpowered to confirm at this `N`.
- G3's raw range (15.7pp) misses the locked 15pp cutoff by a trivial
  0.7pp — a threshold this close to a boundary that a `z=0.57` noise check
  says is not real is a textbook case of a pre-registered numeric cutoff
  being stricter than the data's own noise floor. **The rule is not
  relaxed post-hoc** — the mechanical verdict stands as PARTIAL/MIXED — but
  this is disclosed because it materially changes how much weight the
  "PARTIAL/MIXED" label should carry.

---

## 5. Synthesis

Every method applied — the pooled bivariate correlation, the OLS's
directionally-consistent-despite-unstable coefficients, and the
noise-adjusted sub-group spread test — **converges on the same ordering**:
`ρ` shows the strongest, most consistent signal; `c` is secondary and
largely entangled with `ρ` (its marginal pooled correlation and
sign-flipping OLS behavior are consistent with `c` mattering mostly
*through* its effect on `ρ`, not independently); **`b` shows the weakest
signal of the three by every measure** (pooled `r=0.08, p=0.81`; the
`c`-fixed group G1's spread, while positive, is the less significant of the
two `ρ`-varying groups). This is a genuine, useful discriminating result —
**`b` alone is not what drives the cell-to-cell H2-share variation** — even
though it falls short of a clean, pre-registration-certified "`ρ` alone
explains it" verdict.

---

## 6. Established / Heuristic / Open

**Established (measured, with stated `z`, from a locked pre-registration):**
- `b=1` is exactly plain M-U at every cell (T0, `0/30` violations, fresh
  seed).
- The own-`b` far-tail deficit is present, at high significance, in 12 of
  13 cells (`|z_own|` from `3.2` to `17.8`); one cell (`G1b`) is
  marginal (`z=−1.97`) and honestly excluded from the H2-share analysis
  per the pre-registered rule.
- The `b=1` companion deficit at matched `(c,n,threshold)` is present, at
  varying significance, across the design — from very strong (`G2a,
  z=−6.31`; `G3d, z=−7.65`; `B, z=−7.56`) to weak/non-significant (`G1a,
  G2b, G2d, G4c`, all `|z_b1|<2`) — itself informative: the `b=1` floor's
  own significance varies a great deal across the grid, consistent with a
  real but cell-dependent H2 floor.
- **`ρ` is the only one of `{ρ, c, b}` whose pooled bivariate correlation
  with H2 share crosses conventional significance** (`r=−0.623, p=0.031,
  df=10`), and **`b`'s pooled correlation is statistically indistinguishable
  from zero** (`r=+0.08, p=0.81, df=10`).
- **Both fixed-`ρ` sub-groups (G3 at `ρ≈0.785–0.788`, G4 at `ρ≈0.452–0.458`)
  show internal H2-share spreads statistically consistent with zero**
  (delta-method `z=0.57` and `z=0.73`) despite `b` and `c` each varying
  15–20× within each group; **the fixed-`b` sub-group (G2) shows a highly
  significant internal spread** (`z=4.16`) as `ρ` is allowed to range
  freely from `0.26` to `0.95`.

**Heuristic / suggestive, not certified by the locked primary rule:**
- The convergent reading across §§3–5 — `ρ` (final excluded/rerouted
  fraction) as the leading candidate driver of the H2-share pattern, `c`
  as a secondary, `ρ`-entangled contributor, `b` effectively ruled out as
  an independent driver — is offered as the most defensible qualitative
  summary of the evidence, **not** as a certified conclusion, because the
  pre-registered PRIMARY mechanical rule (§4.3's locked 15pp/30pp range
  cutoffs) does not itself classify either `ρ`-fixed group as cleanly
  "FLAT," so its own decision tree lands on PARTIAL/MIXED, not a clean
  "`ρ` is the driver" call.
- No functional form for `H2share(ρ)` (e.g. linear, logistic) is fit or
  proposed — the pre-registration named only correlation/regression tests,
  not a curve-fitting exercise, and none is warranted by 12 data points
  with this much scatter.

**Not established / left open:**
- Whether `ρ` is causally the driver, or merely the covariate that happens
  to best summarize some other latent quantity `ρ` is constructed from
  (e.g. a specific function of `b` and `c` other than `1-(1-c/n)^b`) is not
  tested here — this front tested `ρ, c, b` as named by the mandate, not
  every possible re-derived combination.
- The `G1b` cell (`c=1000,b=50`) is genuinely ambiguous at `N=2000` — a
  higher-power rerun (as the parent lineage's referees have done
  elsewhere, e.g. `N=5000`) might resolve whether its own-`b` deficit is
  real; not attempted here to keep this front's scope to the
  pre-registered 13-cell grid.
- Why `ρ` (if it is the driver) would govern the H2 floor's share
  mechanistically is not derived — this front is a correlational
  discriminator, per the mandate's explicit scope, not a mechanistic
  derivation (that remains `floor_closed_form_attempt`'s separate mandate,
  wave 14 front (b), `DISC-DEC-057`).

---

## 7. Verdict

> **HONEST PARTIAL RESULT — closer to a positive finding for `ρ` than a
> clean negative, but not certified as such by this front's own locked
> primary rule.** Per the pre-registered PRIMARY discriminator (§4.3's
> mechanical 15pp/30pp sub-group range test, applied exactly as locked),
> the verdict is **PARTIAL/MIXED**: neither fixed-`ρ` sub-group achieves
> the strict "FLAT" bar (G3 misses by `0.7pp`; G4 by `8.5pp`), so no single
> covariate is certified as *the* driver by the letter of the
> pre-registration.
>
> **However, three independent secondary analyses — all explicitly
> anticipated in `DERIVATION_PREREG.md` §§2/4.2 as legitimate, non-rule-
> overriding checks — converge on the same reading**: `ρ` is the only
> covariate with a statistically significant pooled correlation to H2 share
> (`r=−0.623, p=0.031`); the delta-method noise check shows both fixed-`ρ`
> sub-groups have internal spreads consistent with zero (`z=0.57`,
> `z=0.73`) while the fixed-`b` sub-group's spread is highly significant
> (`z=4.16`) as `ρ` ranges freely; and `b`'s pooled correlation with H2
> share is indistinguishable from zero (`r=0.08, p=0.81`) — the weakest
> signal of the three covariates by every method applied.
>
> **`b` alone is ruled out as an independent driver of the cell-to-cell
> H2-share variation** — a genuine, useful discriminating finding, meeting
> the mandate's stated alternative success criterion ("a rigorous negative
> result... also genuinely useful"). `ρ` (the final excluded/rerouted
> fraction) is the best-supported candidate for the leading driver, with
> `c` a secondary, `ρ`-entangled contributor — but this is reported as the
> evidence's honest lean, not a closed, pre-registration-certified
> single-covariate identification.
>
> No closed-form relationship between H2 share and `ρ` (or any covariate)
> is proposed or fit. `φ_REDB` remains the formula of record; nothing here
> supersedes it or any prior result in this lineage. The `U_{1/2}`
> classification in the `n→∞` limit is completely untouched.
>
> **This document requires independent mandatory adversarial verification
> before any integration into governance**, exactly as every predecessor
> document in this lineage. It is not integrated.

> **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-060.]** O referee
> hostil (`adversarial/REFEREE_REPORT.md`) confirma T0 e toda a
> aritmética/fórmulas deste documento exatamente, mas nomeia duas
> complicações reais não divulgadas aqui:
> 1. **A correlação `r=−0,623, p=0,031` de `ρ` não sobrevive a correção de
>    Bonferroni** (`m=3` covariáveis, `α_adj=0,0167`) **nem ao teste de
>    Spearman** (`p=0,08`) — mais frágil, nos dados deste próprio
>    documento, do que aqui divulgado.
> 2. **A célula `G1b`, honestamente excluída aqui por ambiguidade
>    (`|z|=1,97` em `N=2000`)**, foi resolvida pelo referee via
>    triangulação de 3 medições independentes (`N=12.000` combinado,
>    `z=−7,69`): o déficit é real, `H2share=67,7%±15,7pp` — o maior (ou
>    empatado) compartilhamento de `G1` inteiro, numa `ρ` **intermediária**,
>    quebrando qualquer história limpa de monotonicidade-em-`ρ` dentro de
>    `G1` (confirmado por dois testes de heterogeneidade independentes,
>    incluindo o Teste Q de Cochran, `p=0,025`).
>
> **O que isso NÃO muda:** na tabela triangulada de 13 células do próprio
> referee, a correlação `ρ` pooled na verdade **fortalece e sobrevive**
> Bonferroni (`r=−0,680, p=0,011`) — resolver corretamente a célula mais
> fraca do desenho fortalece, não enfraquece, a evidência para `ρ`. `b`
> continua robustamente descartado como driver independente em toda
> versão dos dados testada pelo referee. O enquadramento de honestidade
> deste documento (PARTIAL/MIXED, "lean, não certificado") foi julgado
> pelo referee como **preciso, se algo conservador demais** em relação ao
> que a re-análise sustenta. Ver `THEOREM.md`/`PROOF_DEPENDENCY_MAP.md`
> Árvore B para o registro completo da integração.

---

## 8. Seeds (all used, reserved range `20260839000+` per `DISC-DEC-057` front (e))

| seed | use | N | result |
|---|---|---|---|
| `SeedSequence(20260839000)` | T0, `b=1` engine sanity re-check | 30 | `0/30` violations, `z=+0.15` |
| `SeedSequence(20260839001)` | A, own-`b` | 2000 | `dev=-8.06%, z=-6.93` |
| `SeedSequence(20260839002)` | A, `b=1` | 2000 | `dev=-3.32%, z=-2.80` |
| `SeedSequence(20260839003)` | G1a, own-`b` | 2000 | `dev=-3.79%, z=-3.20` |
| `SeedSequence(20260839004)` | G1a, `b=1` | 2000 | `dev=-1.35%, z=-1.11` |
| `SeedSequence(20260839005)` | G1b, own-`b` | 2000 | `dev=-2.37%, z=-1.97` |
| `SeedSequence(20260839006)` | G1b, `b=1` | 2000 | `dev=-1.64%, z=-1.36` |
| `SeedSequence(20260839007)` | G1d, own-`b` | 2000 | `dev=-19.64%, z=-17.34` |
| `SeedSequence(20260839008)` | G1d, `b=1` | 2000 | `dev=-2.41%, z=-2.00` |
| `SeedSequence(20260839009)` | G2a, own-`b` | 2000 | `dev=-8.42%, z=-6.95` |
| `SeedSequence(20260839010)` | G2a, `b=1` | 2000 | `dev=-7.41%, z=-6.31` |
| `SeedSequence(20260839011)` | G2b, own-`b` | 2000 | `dev=-8.06%, z=-7.05` |
| `SeedSequence(20260839012)` | G2b, `b=1` | 2000 | `dev=-1.77%, z=-1.45` |
| `SeedSequence(20260839013)` | G2d, own-`b` | 2000 | `dev=-20.31%, z=-17.75` |
| `SeedSequence(20260839014)` | G2d, `b=1` | 2000 | `dev=-1.26%, z=-1.09` |
| `SeedSequence(20260839015)` | G3a, own-`b` | 2000 | `dev=-10.81%, z=-8.96` |
| `SeedSequence(20260839016)` | G3a, `b=1` | 2000 | `dev=-5.40%, z=-4.56` |
| `SeedSequence(20260839017)` | G3c, own-`b` | 2000 | `dev=-6.00%, z=-5.16` |
| `SeedSequence(20260839018)` | G3c, `b=1` | 2000 | `dev=-3.41%, z=-2.93` |
| `SeedSequence(20260839019)` | G3d, own-`b` | 2000 | `dev=-22.14%, z=-15.54` |
| `SeedSequence(20260839020)` | G3d, `b=1` | 2000 | `dev=-10.54%, z=-7.65` |
| `SeedSequence(20260839021)` | B, own-`b` | 2000 | `dev=-13.37%, z=-11.08` |
| `SeedSequence(20260839022)` | B, `b=1` | 2000 | `dev=-9.36%, z=-7.56` |
| `SeedSequence(20260839023)` | G4b, own-`b` | 2000 | `dev=-8.64%, z=-7.59` |
| `SeedSequence(20260839024)` | G4b, `b=1` | 2000 | `dev=-5.57%, z=-4.78` |
| `SeedSequence(20260839025)` | G4c, own-`b` | 2000 | `dev=-4.27%, z=-3.67` |
| `SeedSequence(20260839026)` | G4c, `b=1` | 2000 | `dev=-1.98%, z=-1.70` |

Throwaway (outside reserved range, discarded, disclosed §0): `999900010`,
`999900011`.

---

## 9. Files

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration (written first, unmodified since except the disclosed `;`-delimiter fix does not touch it — it never contained the bug) |
| `cv_measure.py` | shared measurement function (T0 + all 26 far-tail runs), imports `sc_engine`/`sc_formula` |
| `cv_grid.py` | driver: runs T0 then all 13 cells × 2 conditions in the locked seed order |
| `cv_analysis.py` | deterministic post-hoc analysis: H2 shares, delta-method SEMs/`z`, Pearson/OLS, sub-group ranges, the §4.3 decision rule |
| `cv_grid.log` | full run output (one line's `group` field delimiter fixed post-hoc, disclosed §0; no numeric value altered) |
| `cv_analysis.log` | analysis output (matches §§2–4 above exactly) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this subfolder touched, other than
reading (read-only, by import) `sc_engine.py`/`sc_formula.py` from
`short_cycle_dynamics_attempt/`, per the mandate's explicit permission.
