# ATTEMPT — the abstract-vs-real ~30% gap, and a fifth-term push on the
# plateau resummation (`MCLUST-PLATEAU-ABSTRACT-REAL-GAP-ATTEMPT`)

**Wave 19, front (d), authorized by `DISC-DEC-083` in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`.** Target: the two
items `plateau_resummation_attempt/ATTEMPT.md` (`DISC-DEC-072/077`) left
open that are closest to being reachable without redoing its full
matched-asymptotics machinery: (1) the abstract-vs-real `~30%` gap,
disclosed but explicitly out of scope by every front since
`floor_closed_form_attempt`; (2) a genuinely new structural push on the
plateau constant's closed-form resummation, specifically the
"conjectured, not derived" fifth asymptotic term.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`), the b=1
floor's abstract `(s,g)` recursive process — pure combinatorial/asymptotic
mathematics about a random-permutation-with-reroutes ensemble. It is a
standalone object, entirely independent of the archive's separate Tree A
(u₁/₂ / "Lemma Aberto") line in `THEOREM.md`. Nothing here is, or is
adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

Seeds: this front's reserved range `20260886000-20260886999` was
grep-confirmed unused before first use (`grep -rn "20260886"
05_DISCOVERY_LAB/` matched only the ledger/queue reservation lines). **In
the end no randomness was needed anywhere in this front** — every result
below is either a deterministic recursion/series computation (`mpmath`,
arbitrary precision) or exact symbolic algebra (`sympy`), so the reserved
range remains, like `plateau_resummation_attempt`'s own, entirely unused.
`20260887000+` (reserved for a future referee) was not touched.

---

## EXECUTIVE SUMMARY (read first)

**Objective 1 (abstract-vs-real gap): genuine narrowing of the
characterization, no closure.** Tier: **DIAGNOSIS SHARPENED, not closed.**

- The gap is precisely re-defined and, using the now-EXACT abstract
  plateau constant `Pi(1000) = 0.0377615983402126188...` (previously
  known only to ~2-3 significant figures when the "~30%" figure was first
  quoted) against the record's own already-vetted, referee-confirmed
  real-engine `phi(ell)` bin tables, characterized far more sharply than
  "~30%": a bin-resolved composite table across the WHOLE far tail
  (`t0` from `~0.05` to `~0.94`, using cluster-robust real-engine values
  where the record's own replication showed the naive point-level
  estimate is unreliable) gives a relative gap **`38.8% mean, range
  [35.8%, 43.2%]`** — closer to `~39%` than `~30%`, and (this is the
  substantive new finding) **roughly CONSTANT across the entire `t0`
  range** (Pearson `r=0.33` against `t0`), not concentrated near any one
  regime.
- This flatness is used, together with a structural fact about the
  abstract process read directly off its own governing PDEs (`s+g` is
  exactly CONSERVED while in "mode G" and grows only during "mode E"
  excursions — derived here, not previously stated this way in the
  record), to **argue against** the "s+g<=1 boundary/total-mass
  constraint" hypothesis floor_closed_form_attempt named as one of two
  candidate sources: that mechanism predicts a gap that GROWS toward
  `t0->1` and is small at moderate `t0` (plenty of "room" `1-t0`); the
  observed gap is already `~36%` at `t0~0.05`, essentially as large as at
  `t0~0.94` — inconsistent with that mechanism being the *dominant*
  driver (a modest, unproven residual contribution near `t0->1` is not
  excluded).
- A clean magnitude/scaling argument (`1/n=1.5e-5`, `1/sqrt(n)=0.39%`,
  `sqrt(c/n)=12.4%`, all versus the observed `O(1)` `~39%` gap at
  `n=65536`) similarly **disfavors** the other named hypothesis (a
  finite-`n` effect vanishing as `n->infinity`) taken literally — `n` is
  simply too large for any power-law-in-`1/n` correction to produce an
  `O(1)` gap without an implausibly large, unexplained prefactor.
- **Neither named hypothesis survives as the primary explanation.** No
  replacement is derived; a concrete, well-motivated, NOT-yet-executed
  next step (a discrete finite-pool re-simulation using the real engine's
  own `n`, sketched precisely in §1.5) is named instead of forced through
  under this front's time budget — consistent with the mandate's
  "honest non-closure acceptable" framing.

**Objective 2 (fifth-term push on the plateau resummation): the strongest
numerical evidence yet for the conjectured `d4=209/8`, and a first
meaningfully-constrained read on `d5` — still CONJECTURED, not DERIVED.**
Tier: **STRENGTHENED NUMERICAL CONFIRMATION of an existing conjecture,
via a genuinely independent method; no new derivation, H1/H2 unchanged.**

- A fresh, from-scratch `(P,Q)`-family recursion implementation (read
  from the prose of THREE documents' descriptions of the same technique,
  no `.py` file of any ancestor front opened) reproduces all 6 published
  numeric anchors exactly, then computes `Pi(c)` independently at **11
  values of `c` from `100` to `655360`** — a `6553x` range, *wider* than
  either ancestor front's own `1024x` range, and reaching `c=100`, a
  value **neither ancestor front's own direct-summation method could
  complete** (their own disclosed cost wall stopped at `c=250`,
  expensively, `736s` for 46 digits). This front reaches `c=100` in `113s`
  because it targets ~30 stable digits rather than >=110 — enough to
  resolve `d4`/`d5` by 20+ orders of magnitude of safety margin, at a
  small fraction of the cost.
- A different fitting method — **residual isolation**: using the
  ALREADY-EXACT closed forms of `d0..d3` (not re-fitting them) to isolate
  `R4(c) := [y(eps)-d0-d1*eps-d2*eps^2-d3*eps^3]/eps^4 -> d4`, then fitting
  `R4` itself against `eps` — is much better-conditioned than the
  ancestor front's blind simultaneous degree-6/7 fit of all coefficients.
  Result (quadratic fit, 7 largest-`c` points): **`d4 = 26.1246`, vs the
  conjectured `209/8 = 26.125` — agreement to `~5` significant digits**
  (up from the ancestor front's own `~2.6` digits, its own fit not even
  trusting itself past `~0` digits by its own stability diagnostic), and
  **`d5 = -82.017`, vs the conjectured `-82.235` — agreement to `~2.6`
  digits** (up from "not meaningfully constrained").
- An independent SYMBOLIC (sympy) check confirms the `gamma_n`/`R^(n-1)(0)`
  bookkeeping identity is exactly self-consistent for `n=1..4` (re-derived
  from scratch here, not merely re-quoted) and that the conjectured
  `gamma_5=209/24` is arithmetically equivalent to `d4=209/8` — a
  structural sanity check, not a derivation of `gamma_5` itself (which
  needs the un-redone 5th-order boundary-layer step; explicitly out of
  this front's scope, same as the ancestor front's own honest limit).
- **H1 (uniform validity of the matched-asymptotics decomposition) and H2
  (uniqueness of the bounded-order solution) are NOT closed here** — no
  attempt was made to justify them directly from the exact PDE system
  (that is a different, much larger undertaking than this front's budget
  allows, as both ancestor documents already note). What changes is
  purely the numerical confidence in the SPECIFIC conjectured `n=5`
  coefficients, via a route (residual isolation + a wider, independently
  computed `c`-grid) that shares no machinery with either the original
  matched-asymptotics derivation or the ancestor front's own polynomial
  fit.

`phi_REDB`, `phi_U(c)`, `phi_infinity(c)`, and every formula of record:
**untouched.** No claim of a closed form for `Pi(c)` at finite `c` is
made anywhere below. No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, or `TEST_QUEUE.yaml` file was modified (or, per
the mandate, even opened for writing) by this front. No `adversarial/`
subdirectory was created and no referee dispatched by this front itself.

---

## 0. Reading discipline and provenance (per the mandate)

Read in full, prose only, before any derivation:
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/PROOF_DEPENDENCY_MAP.md`
(specifically Tree B §2, node `FLOORH2` and its child `PLATRESUM`, and
every dated addendum through `DISC-DEC-077`); the FULL prose (not code) of
`.../floor_h2_b1_full_closure_attempt/ATTEMPT.md` and its
`adversarial/REFEREE_REPORT.md`; `.../plateau_resummation_attempt/ATTEMPT.md`
and its `adversarial/REFEREE_REPORT.md`; and, since the precise definition
of the "abstract-vs-real gap" this front was asked to characterize is
first stated there (not in either of the two documents named above, which
only *cite* it as already-disclosed and out of scope), the relevant
sections (`§0`-`§2`, `§4`, `§6`) of the grandparent
`.../long_cycle_deficit_attempt/floor_closed_form_attempt/ATTEMPT.md` —
also prose only. **No `.py` file belonging to ANY front in this lineage
was opened, read, or imported at any point.** Every script in this
directory (`g01`-`g06`, `h01`) was written fresh from the mathematical
content of the prose cited above; where a script's output is compared
against a previously-published number, that number is transcribed as
plain text into the script (see e.g. `g02_validate_anchors.py`'s literal
anchor constants), never imported as code.

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory
(`plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/`)
was written to. No git command was run.

**The established inputs this front works from** (all PROVED/DERIVED and
referee-confirmed, restated here only for self-containedness — not
re-derived except where explicitly marked "re-derived" below):

```
Phi(s,g) = sum_k a_k(s) g^k,  Psi(s,g) = sum_k b_k(s) g^k,  a_0=1, b_0=0
a_{k+1}(s) = [a_k'(s) - c*a_k(s) + c*w_k(s)] / (k+1)
b_k'(s) - c*s*b_k(s) = -c*a_{k-1}(s)/k + c*b_{k-1}(s)          (bounded branch)
w_k(s) = a_{k-1}(s)/k + (1-s)*b_k(s) - b_{k-1}(s)
a_1(s) = -c,  b_1(s) = psi1(s) = sqrt(pi*c/2)*erfcx(s*sqrt(c/2))
every a_k, b_k in F = {P(s) + Q(s)*erfcx(s*sqrt(c/2))}, P,Q polynomials
Phi(0,t0) = sum_k a_k(0) t0^k converges for ALL t0 (entire-function-like)
Pi(c) := lim_{t0->inf} Phi(0,t0);  Pi(1000) = 0.0377615983402126188243712025905770479904...

Four-term asymptotic law (DERIVED heuristic n<=4, CONFIRMED numerically):
  y(eps) := Pi(c)*sqrt(2c/pi) = d0 + d1*eps + d2*eps^2 + d3*eps^3 + O(eps^4)
  d0=1, d1=-2*sqrt(2/pi), d2=7/2, d3=-(34/3)*sqrt(2/pi),  eps:=1/sqrt(c)
  psi_n(0) = gamma_n * R^{(n-1)}(0),  gamma_n = 1,2,7/2,17/3,209/24(conj.),...
  R(x)=sqrt(pi/2)*erfcx(x/sqrt2),  R'=xR-1,  R^{(n+1)}=x R^{(n)} + n R^{(n-1)}
  conjectured, UNPROVEN: gamma_5=209/24  <=>  d4=209/8=26.125,
                          d5 = -(1546/15)*sqrt(2/pi) = -82.2353...
```

**Governing PDE system of record** (wave-14, restated by every descendant
document identically):

```
dPhi/ds - dPhi/dg = c[Phi - W],     dPsi/ds = c[Psi - W]
W(s,g) = g*Avg_g[Phi(s,.)] + (1-s-g)*Psi(s,g)
Avg_g[Phi] := (1/g) int_0^g Phi(s,g') dg'
boundary: Phi(s,0) = 1;   target: Phi(0,t0)
```

**Where the "abstract-vs-real gap" is first named and precisely defined**
(`floor_closed_form_attempt/ATTEMPT.md` §4, §6 — quoted/paraphrased
faithfully, this is not this front's own construction): the "real engine"
side is `phi(ell) := P(cyclic | x0 not seed, L(x0)=ell)`, measured by
DIRECT simulation of the actual, finite `n=65536, c=1000` M-CLUST(1)
engine, in two already-vetted tables (T1, absolute-`ell` bins, §2; T2,
relative-`L/n` bins spanning the whole far tail, §4, plus a
cluster-robust re-measurement of the 3 bins the ancestor's
cluster-robustness check covered — positions 5, 8, and 9 of the 9-bin
point-level table, not literally the 3 rightmost (which would be
positions 7, 8, 9); see the dated correction below — after the front's
own replication showed the naive point-level SEM understates the true
uncertainty there).

> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-085.]** O referee
> hostil (`adversarial/REFEREE_REPORT.md`, N2) apontou que a descrição
> acima ("its 3 rightmost bins") é imprecisa: checando diretamente
> contra a tabela de robustez-de-cluster de
> `floor_closed_form_attempt/ATTEMPT.md` §4, os três bins que de fato
> receberam a re-medição robusta são as posições 5, 8 e 9 da tabela de
> 9 bins em nível de ponto (não literalmente os 3 mais à direita, que
> seriam as posições 7, 8, 9) — o bin 5 (`t0~0{,}438`) fica no meio da
> faixa, não na cauda. Isto é **puramente uma imprecisão descritiva de
> citação, não um erro computacional**: o documento manteve
> corretamente o valor em nível de ponto do bin 5 (`0{,}02722`, já que
> é o único dos três que "sobrevive" à replicação por cluster segundo o
> próprio achado da fonte) e substituiu corretamente pelos valores
> robustos por cluster apenas nos bins 8 e 9 (os dois que NÃO
> sobrevivem) — todo número efetivamente usado na tabela do gap está
> correto, já verificado independentemente pelo referee. Apenas o rótulo
> "3 bins mais à direita" precisava de correção; corrigido acima e em
> §A.3 abaixo para "os 3 bins que a checagem de robustez-de-cluster da
> frente ancestral cobriu". Nenhum valor numérico é afetado.

The "abstract" side is `Phi(0,t0)` of the idealized
`(s,g)` recursive process at the same `c=1000`, with `t0` identified with
`L/n` — originally measured only by Monte Carlo of the abstract process
(`~0.037-0.039`, 2-3 significant figures) against a real-engine range
`~0.025-0.029`, "not reconciled" and named informally as "~30%" larger.
Two candidate explanations were offered, EXPLICITLY as untested
hypotheses, not findings: "(H-finite-n) possibly a finite-`n` effect not
captured by the `n->infinity` idealization", and "(H-boundary) possibly a
remaining simplification in the abstract model's treatment of the
`s+g<=1` total-mass constraint for `t0` near 1".

---

## PART A — Objective 1: characterizing the abstract-vs-real gap

### A.1 Precise re-definition using the now-exact abstract constant

At the time the "~30%" figure was first quoted, the abstract side was
known only to `~0.037-0.039` (Monte Carlo, `N=40,000`). Two subsequent
fronts (`floor_h2_b1_full_closure_attempt` + its referee, `DISC-DEC-071`;
`plateau_resummation_attempt` + its referee, `DISC-DEC-077`) pinned this
down to an exact, many-times-cross-validated 121-digit value via the
`(P,Q)`-family closed-form series — re-verified fresh by this front's own
independent implementation (`g01`/`g02`, §B.1 below; all 6 published
anchors match to 12-14 significant digits, the residual being pure
`mpmath` roundoff at the working precision used):

```
Pi(1000) = Phi(0, t0>=0.02) = 0.0377615983402126188243712025905770479904...
```

This alone lets the gap be computed EXACTLY on the abstract side, for the
first time — all remaining uncertainty is now entirely on the real-engine
(Monte Carlo) side, which the record already quantifies with proper SEMs.

### A.2 Bin-resolved gap tables (`h01_gap_characterization.py`, deterministic,
cites the record's own already-published, referee-confirmed real-engine
numbers verbatim as data — no re-simulation)

**Table T1** (absolute-`ell` bins, `floor_closed_form_attempt` §2,
`gap% := (Pi_abstract - phi_real)/phi_real * 100`):

| `ell` bin | `t0`≈mid/n | `phi_real` | gap% |
|---|---|---|---|
| `[500,1000)` | 0.011 | 0.0298 | 26.72% |
| `[2000,4000)` | 0.046 | 0.0265 | 42.50% |
| `[4000,8000)` | 0.092 | 0.0253 | **49.26%** |
| `[8000,16384)` | 0.186 | 0.0258 | 46.36% |
| `[16384,32768)` | 0.375 | 0.0266 | 41.96% |
| `[32768,65536)` | 0.750 | 0.0273 | 38.32% |

**Table T2 composite** (relative-`L/n` bins spanning the WHOLE far tail,
`floor_closed_form_attempt` §4; point-level values used except the 3
rightmost bins, where the cluster-robust re-measurement replaces the
point-level estimate — per the front's OWN finding that 2 of those 3
point-level bins do not survive a properly-powered, cluster-robust
replication):

| `L/n` bin (mid) | `phi_real` | gap% |
|---|---|---|
| 0.046 | 0.02781 | 35.78% |
| 0.091 | 0.02716 | 39.03% |
| 0.186 | 0.02747 | 37.46% |
| 0.312 | 0.02673 | 41.27% |
| 0.438 | 0.02722 | 38.73% |
| 0.562 | 0.02781 | 35.78% |
| 0.688 | 0.02692 | 40.27% |
| 0.812 | 0.02637 (cluster) | 43.20% |
| 0.938 | 0.02747 (cluster) | 37.46% |

**mean gap = 38.78%, range [35.78%, 43.20%], spread = 7.41 percentage
points, Pearson `r(gap%, t0) = 0.331` (n=9, weak).**

**Reading this honestly.** The two tables broadly agree on ORDER OF
MAGNITUDE (`~30-50%`, not `~30%` on the nose, and never close to `0`
anywhere) but disagree on fine SHAPE: T1 shows a pronounced mid-range
"hump" (peak `49.3%` at `t0~0.09`, lower at both the small-`t0` end
`26.7%` and the large-`t0` end `38.3%`); the T2 composite is much flatter
(`35.8%` to `43.2%`, weak positive trend). **This discrepancy is disclosed
honestly, not resolved**: T1 was not cluster-corrected in the record (only
T2's bins 5, 8, and 9 — the ones the ancestor's own cluster-robustness
check covered, not literally the 3 rightmost — received that treatment;
see the dated correction in §A.2 above), so T1's shape may itself
partly be the same kind of correlated-bin-noise artifact the record's own
referees have repeatedly flagged for this statistic family elsewhere
(`short_cycle_dynamics_attempt/adversarial/REFEREE_REPORT.md` §4.2, and
`long_cycle_deficit_attempt/floor_closed_form_attempt/ATTEMPT.md`'s own
T2 cluster-robustness finding, cited above). **What survives across both
tables, robustly:** the gap is a genuine `O(1)` effect (`25%` to `50%`
depending on bin and correction), present at EVERY `t0` tested from
`~0.01` to `~0.94`, never vanishing or trending toward zero anywhere in
the tested range.

### A.3 A structural argument against the boundary/`s+g<=1` hypothesis
(this front's own reasoning, from the governing PDEs already cited above)

Reading the two PDEs' characteristic structure directly: `dPhi/ds -
dPhi/dg = c(Phi-W)` has characteristic direction `(ds,dg)=(1,-1)` — i.e.
in "mode G" (the `Phi`-branch, actively sweeping the identified gap), `s`
and `g` move in lockstep, so **`s+g` is exactly CONSERVED between marks
while in mode G**. `dPsi/ds = c(Psi-W)` has NO `dPsi/dg` term at all —
i.e. in "mode E" (the `Psi`-branch, generic exploration outside the
identified gap, matching `floor_closed_form_attempt`'s own T3 process
description: "generic (mode E, g unchanged, s still accrues)"), **`g` is
frozen and `s` alone grows, so `s+g` INCREASES strictly during every mode-E
excursion.** Since the idealized process never caps `s+g` at `1` (the
`(1-s-g)*Psi` term in `W` would need to be replaced by something bounded
below at `0` to enforce this, which the abstract model as stated does
not do), any trajectory that spends enough mass in mode E can push `s+g`
past the real engine's hard physical ceiling of `1` — this IS the
mechanism `floor_closed_form_attempt` gestured at with "(H-boundary)".

**But this mechanism predicts a `t0`-DEPENDENT gap**: at small-to-moderate
`t0` there is abundant room (`1-t0` close to `1`) before `s+g` could ever
approach the physical ceiling, so any boundary-driven excess should be
small there and grow specifically as `t0->1` (where `1-t0` is small). The
T2 composite table (§A.2) does **not** show this pattern: the gap at
`t0~0.046` (`35.78%`) is already nearly as large as at `t0~0.938`
(`37.46%`), and the single largest value in the whole table
(`43.20%`) occurs at `t0~0.812`, not at the extreme tail. The weak overall
correlation (`r=0.33`) is consistent with, at most, a MODEST additional
boundary contribution superposed on a much larger, roughly `t0`-independent
base gap — **not** with the boundary mechanism being the *primary* driver
of the ~39% figure. This is a genuine (if not decisive — the T1/T2 shape
disagreement of §A.2 leaves real residual uncertainty) narrowing: it
redirects attention away from "boundary depletion near `t0=1`" as the main
story and toward something present already at moderate `t0`.

### A.4 A magnitude argument against a vanishing finite-`n` hypothesis

Taken literally, "(H-finite-n): a finite-`n` effect not captured by the
`n->infinity` idealization" means a correction that VANISHES as
`n->infinity` at fixed `c`. At the record's own target cell, `n=65536` is
enormous relative to `c=1000`:

```
1/n            = 1.53e-5   (0.0015%)
1/sqrt(n)      = 3.91e-3   (0.39%)
c/n            = 0.0153    (1.53%)
sqrt(c/n)      = 0.1235    (12.35%)
observed gap   ~ 38.8%     (O(1))
```

Any correction that is `O(1/n)` or `O(1/sqrt(n))` is many orders of
magnitude too small to produce an `O(1)` `~39%` effect at this `n` — such
a hypothesis would need an implausibly large (`~2500x` to `~100000x`)
unexplained multiplicative prefactor. Even `O(sqrt(c/n))`, the most
generous natural small parameter available, would need a prefactor
`~3.1x` (`38.8/12.35`) to close the gap alone — not impossible, but a
real, unexplained factor that the "vanishing finite-`n` effect" framing
does not supply or motivate. **Read plainly: whatever the gap's source
is, it is NOT primarily a correction that shrinks as `n` grows** (at
least not at any of the natural small-parameter rates checked here) —
either it is a genuine `O(1)` STRUCTURAL difference between the abstract
idealization and the real engine (e.g. a different effective normalization
of "rate `c`", or a systematic difference in how mode-E's implicit
"infinite generic reservoir" assumption behaves even far from any hard
boundary), or it involves a specific, currently unidentified large
prefactor on an otherwise-small finite-size parameter. This front does
not have the evidence to distinguish these further.

> **[Correção pós-adversarial, 2026-08-26 — DISC-DEC-085.]** O referee
> hostil (`adversarial/REFEREE_REPORT.md`, N1) apontou que o argumento
> de magnitude acima testa apenas três taxas candidatas
> (`1/n`, `1/\sqrt n`, `\sqrt{c/n}`) e não é exaustivo: o referee
> encontrou que `(c/n)^{1/3}` e, especialmente, `(c/n)^{1/4}` chegam
> muito mais perto do gap observado (`~38{,}8\%`) com prefatores
> multiplicativos pequenos e nada implausíveis (`\sim1{,}56\times` e
> `\sim1{,}10\times`, respectivamente) — candidatos que este parágrafo
> não considerou. Isto **não** derruba a conclusão do documento, que já
> era honestamente restrita ("pelo menos não nas taxas de parâmetro
> pequeno naturais testadas aqui"): a hipótese (H-finite-n) permanece
> desfavorecida nas três taxas efetivamente testadas. Mas o argumento
> de magnitude deve ser lido como desfavorecendo apenas essas taxas
> específicas, não a classe mais ampla de correções finite-`n`
> evanescentes em `c/n` a outras potências — em particular,
> `(c/n)^{1/4}` permanece uma explicação candidata não descartada por
> este front.

### A.5 A concrete, well-defined, NOT-yet-executed next step (named, not
executed, per this front's time budget and the mandate's anti-stall
instruction)

The most direct way to test (H-finite-n) properly (rather than by the
magnitude argument of §A.4 alone) is a **discrete, finite-pool
re-simulation of the SAME `(s,g)` process**, using the real engine's own
`n=65536` as an explicit, finite total item count rather than the
idealization's implicit infinite reservoir: `n` discrete "slots"
representing the population outside `x0`; step through them one at a
time (`ds=1/n` each); at each slot, independently w.p. `c/n`, a "mark"
(reroute) triggers there (giving `Binomial(n,c/n) -> Poisson(c)` marks in
the `n->infinity` limit, matching the abstract idealization exactly in
that limit); crucially, cap `s+g` at `n` (physically: once every
non-`x0`-cycle item is exhausted, mode E can no longer draw a "fresh"
target). Comparing this discrete process's own plateau (as a function of
initial `g0=t0*n`) against BOTH the exact abstract value `0.0377616` and
the real engine's own `phi(ell)` would directly test whether finite-pool
discretization by itself accounts for any of the ~39% gap, and by how
much, without needing to replicate the real engine's full permutation
machinery (which is a substantially higher-risk undertaking this front
judged disproportionate to attempt from scratch, with no reference
implementation to cross-check against, within this mandate's budget).
**This was sketched but NOT implemented or run** — named here as the
single most concrete, actionable next step for a future front, per this
lineage's convention of disclosing a real next avenue rather than forcing
a rushed, unverified execution of it.

### A.6 Honest verdict, Objective 1

**Tier: diagnosis sharpened, not closed.** The gap is now characterized
to real precision (composite mean `38.8%`, range `[35.8%,43.2%]`, roughly
`t0`-independent) rather than the informal "~30%" — this directly answers
the mandate's option (c) ("characterize it more precisely"). Neither
named hypothesis is confirmed; both are genuinely weakened as PRIMARY
explanations by concrete, checkable arguments (§A.3 structural, §A.4
magnitude) — this is a real, if partial, contribution to option (b)
("diagnose its source") by elimination, not by a positive identification.
No corrected or refined abstract construction is proposed (option (a) is
NOT achieved) — the evidence gathered here narrows where the true source
must lie (a genuine `O(1)` structural difference, likely present already
at moderate `t0`, not concentrated at a boundary and not a vanishing
finite-size correction) without identifying it.

---

## PART B — Objective 2: pushing the plateau resummation toward `n=5`

### B.1 Fresh `(P,Q)`-family implementation and anchor validation

`g01_family_series.py` implements the recursion and the `b`-ODE
"descending coefficient matching, leftover `j=0` relation pins `kappa`"
technique exactly as described in BOTH ancestor documents' prose (§0
above), entirely fresh (no `.py` file opened). `g02_validate_anchors.py`
validates it against all 6 published numeric anchors (`c=1000`) BEFORE
using it for anything else:

| quantity | this front's value | published anchor | rel. diff |
|---|---|---|---|
| `a2(0)` | 520316.63648803... | 520316.636488 | 5.8e-14 |
| `a3(0)` | -180730907.6285080... | -180730907.6285 | 4.5e-14 |
| `a4(0)` | 47146963944.137885... | 47146963944.14 | 4.5e-14 |
| `b2(0)` | -20816.63648803... | -20816.636488 | 1.4e-12 |
| `b1(0)` | 39.63327297606011... | `sqrt(pi*1000/2)` | 0 (exact) |
| `Phi(0,0.002)` | 0.15850014574730848 | 0.15850015 | 2.7e-8 |

**6/6 PASS** (`g02_validate_anchors.log`).

### B.2 A wider, independently-computed `c`-grid, at deliberately reduced
(but ample) precision

`g03_timing_probe.py` establishes that this front's precision NEEDS are
far below the ancestor fronts' `>=110`-digit target: since `d0..d3` are
already exact and `d4/d5` only need to be resolved to a handful of
digits, `~28-32` stable digits (three-way error control: `S(c*t0=60,
80, 100)`, matching the record's own methodology recalibrated to a
smaller target) is already `20+` orders of magnitude more precision than
needed, and is dramatically cheaper: `c=1000` in `6.3s` (`K=500,dps=100`)
vs. the ancestor front's `163.5s` for `110+` digits. This lets
`g04_compute_grid.py` reach **`c=100`** (`K=1800,dps=300`, `112.3s`) — a
value **neither ancestor front's own cost-wall-limited method could
complete** (their disclosed failed attempts stopped at `c=250`, `736s`,
`46` digits; `c=100,40,10,1` never produced output at all in either
front). Full 11-point grid (`c=100` to `655360`, a `6553x` range):

| `c` | `Pi(c)` (20 sig. figs) | time | cross-check vs. record |
|---|---|---|---|
| 100 | 0.10883475474933102253 | 112.3s | (no published reference at this `c`) |
| 250 | 0.072222631781514161964 | 18.4s | reldiff `1.9e-43` |
| 640 | 0.046662665205790726432 | 6.4s | reldiff `4.8e-40` |
| 1000 | 0.037761598340212618824 | 6.3s | reldiff `5.6e-40` |
| 2560 | 0.024021775587665976409 | 6.4s | reldiff `3.2e-39` |
| 6400 | 0.015362227215880203506 | 6.5s | (no published reference) |
| 16000 | 0.0097854424044395860488 | 6.6s | (no published reference) |
| 40960 | 0.0061443932785551918066 | 6.3s | reldiff `6.0e-39` |
| 100000 | 0.0039434648909803078682 | 6.5s | (no published reference) |
| 250000 | 0.0024986631871347305795 | 6.5s | (no published reference) |
| 655360 | 0.0015451312096662308760 | 6.3s | reldiff `9.7e-39` |

(full 40-digit values, approach-error diagnostics: `g04_grid_results.json`,
`g04_compute_grid.log`.) Every value cross-checked against the record
(`c=250,640,1000,2560,40960,655360`) matches to roundoff (`<1e-38`
relative) — a strong, independent, THIRD confirmation (after the front
and its referee) of the record's own numbers, at 5 new `c` values never
computed by either ancestor front (`100, 6400, 16000, 100000, 250000`).

### B.3 Residual isolation: a better-conditioned route to `d4`, `d5`

`g05_residual_isolation.py`. Using `d0=1, d1=-2*sqrt(2/pi), d2=7/2,
d3=-(34/3)*sqrt(2/pi)` **as exact closed forms, not re-fitted**, define
`R4(c) := [y(eps)-d0-d1*eps-d2*eps^2-d3*eps^3]/eps^4`
(`y(eps):=Pi(c)*sqrt(2c/pi)`, `eps:=1/sqrt(c)`); `R4(c) -> d4` as
`c->infty`, with `R4(c) = d4 + d5*eps + O(eps^2)`. This is much
better-conditioned than fitting `d0..d6` simultaneously from a
Vandermonde solve (the ancestor front's own method, which by its own
diagnostic does not even trust its `d4` to any digit): it isolates only
the two genuinely unknown quantities.

| method | `d4` | vs. `209/8=26.125` | `d5` | vs. conj. `-82.235` |
|---|---|---|---|---|
| linear fit, all 11 pts | 25.9606 | `-0.63%` | -62.76 | `-23.7%` |
| linear fit, 5 largest-`c` | 26.1210 | **`-0.015%`** | -79.74 | `-3.03%` |
| linear fit, 4 smallest-`c` | 25.4640 | `-2.53%` | -55.65 | (not informative) |
| **quadratic fit, 7 largest-`c`** | **26.1246** | **`-0.0014%`** | **-82.017** | **`-0.26%`** |

(`g05_residual_isolation.log`, `g05_residual_results.json`.) **The
quadratic fit's `d4` agrees with the conjectured `209/8` to `~5`
significant digits** (vs. the ancestor front's own `~2.6` digits, itself
flagged by its own cross-subset stability check as "the fit does not even
trust its own `d4`"), and **`d5` agrees with the conjectured value to
`~2.6` digits** (vs. "not meaningfully constrained" — the ancestor's own
`d5` estimate, `-79.02`, was `3.9%` off; this front's `-82.02` is `0.26%`
off, a `>10x` tighter constraint). The pattern across subsets (worse for
the widest-`eps` subsets, best for the narrowest) is exactly what a
genuine `eps`-expansion, contaminated by unresolved higher-order terms at
large `eps`, should produce — not an artifact of overfitting (the
7-largest-`c` quadratic fit uses 7 data points for 3 unknowns, not a
saturated fit).

**Honest labeling.** This is a NUMERICAL result, via a genuinely
independent method (own recursion implementation, own wider `c`-grid,
own residual-isolation fitting technique — sharing no code or fitting
machinery with either the original matched-asymptotics derivation or the
ancestor front's own polynomial fit). It **confirms more strongly** that
the conjectured `d4=209/8, d5=-(1546/15)sqrt(2/pi)` are numerically very
likely correct. **It does NOT derive `gamma_5` or `d4`/`d5`** — it is not
a proof, and does not touch H1/H2 (§B.5).

### B.4 Independent symbolic structural check (`g06_gamma_structure_check.py`)

A from-scratch `sympy` re-derivation, independent of both ancestor
documents' own machinery: `R'(x)=x*R(x)-1` verified symbolically (exact
simplification to `0`); the closure identity `R^{(n+1)}=x*R^{(n)}+n*R^{(n-1)}`
verified for `n=1..6` (all exact `0` residuals); `R^{(k)}(0)` computed for
`k=0..6` (`sqrt(pi/2), -1, sqrt(pi/2), -2, (3/2)sqrt(2pi), -8, ...`); and
the ALREADY-ESTABLISHED `gamma_1..gamma_4` (`1, 2, 7/2, 17/3`) re-derived
independently from `psi_1(0)..psi_4(0)` (taken as given, machine-verified
elsewhere in the record) divided by the corresponding `R^{(n-1)}(0)` —
**exact match, 4/4**, confirming `gamma_n` is not free numerology fit to
4 numbers but is forced, self-consistently, once `psi_n(0)` is known.
Applying the SAME bookkeeping to the conjectured `gamma_5=209/24` gives
`predicted d4 = 209/8` **exactly** (sympy `nsimplify`, exact rational
arithmetic) — confirming the record's own bookkeeping is internally
consistent (this was implicit in the ancestor document but not
independently re-verified before). **This does not derive `gamma_5`**
(that requires redoing the 5th-order boundary-layer step, `h_5`, which
neither this front nor the ancestor front's referee attempted — the
referee explicitly estimated `3-4` hours even for a PARTIAL check of one
lower order) — it only confirms the identity is arithmetically sound,
which is what makes §B.3's numerical confirmation meaningful evidence
FOR the conjecture rather than a comparison against an arbitrarily
chosen number.

### B.5 H1/H2 status (unchanged; explicit discussion, not closure)

**Not closed.** H1 (uniform validity of the outer/inner matched-asymptotics
decomposition) and H2 (uniqueness of the bounded-order solution) remain
exactly as the ancestor front and its referee left them: genuinely open,
with the referee's own named structural concern (`Phi(0,.)` being
order-2-entire, a growth class where non-perturbative trans-series content
is common and would not contradict any finite number of confirmed
power-series coefficients) unaddressed by anything in this front. **What
this front's §B.3 result DOES provide**: one more data point in the same
spirit as the referee's own §4 argument (if H1/H2 were silently corrupting
the specific `n<=4`/`n=5` coefficients, an INDEPENDENT numerical route
sharing no machinery with the derivation would be unlikely to keep
matching to increasing precision as more, wider-ranging data is added) —
this is corroborating, not conclusive, evidence, exactly as the referee's
own analogous check was. **No claim of rigor is made for H1/H2 anywhere
in this document.**

### B.6 Honest verdict, Objective 2

**Tier: strengthened numerical confirmation of an existing conjecture,
via an independent method — not a derivation, not a closed form, H1/H2
unchanged.** The mandate's three sub-options for Objective 2 are addressed
as follows: (i) closing H1 or H2 rigorously — **NOT attempted** (judged,
consistently with the referee's own explicit time estimate, disproportionate
to this front's budget); (ii) a new structural insight toward a resummation
ansatz — **NOT achieved** (no new resummation idea is proposed; the Borel
and PSLQ routes remain exhausted exactly as the ancestor front left them,
neither revisited here); (iii) deriving the conjectured fifth term rigorously
— **NOT achieved as a derivation**, but **substantially strengthened as a
numerical confirmation** (`d4` to `~5` digits, `d5` to `~2.6` digits, both
via an independent method and a wider, independently-computed `c`-grid
reaching `c=100`, previously unreachable). This is a real, checkable,
disclosed increment — not a closure of anything the mandate asked to be
closed.

---

## Verification summary (test log)

All work in this front is either exact symbolic algebra (deterministic,
no seeds) or exact-precision numerical series summation (deterministic
given `(K,dps)`, no seeds) — **no randomness was needed anywhere**, so
the reserved seed range `20260886000-999` was confirmed unused both
before this front began and remains unused at the end.

| ID | script | purpose | result |
|---|---|---|---|
| V1 | `g01_family_series.py` | fresh `(P,Q)`-family recursion implementation | smoke test matches all quoted anchors |
| V2 | `g02_validate_anchors.py` | validates V1 against 6 published numeric anchors BEFORE any downstream use | **6/6 PASS** |
| V3 | `g03_timing_probe.py` | finds an efficient `(K,dps)` working point; 3-way approach-error control at `c=1000,640,655360,250` | converges to `>=28` stable digits matching the record at every tested `c`, far cheaper than the record's own `>=110`-digit target |
| V4 | `g04_compute_grid.py` | computes `Pi(c)` independently at 11 values of `c`, `100..655360` (`6553x` range) | 6/6 cross-checked values match the record to `<1e-38` relative; 5 new `c` values with no prior published reference computed for the first time |
| V5 | `g05_residual_isolation.py` | isolates `d4`,`d5` via residual subtraction of the EXACT `d0..d3`, three independent fits (all-11, 5-largest-`c`, 4-smallest-`c`) plus a 7-point quadratic fit | `d4=26.1246` (vs `209/8`, `~5` digits), `d5=-82.017` (vs conjectured, `~2.6` digits) |
| V6 | `g06_gamma_structure_check.py` | independent sympy re-derivation of the `R`/`gamma_n` closure identity, `n=1..6` | all identities exact; `gamma_1..4` independently re-derived and matched; `gamma_5=209/24 <=> d4=209/8` confirmed arithmetically |
| V7 | `h01_gap_characterization.py` | bin-resolved abstract-vs-real gap tables (T1, T2 point-level, T2 cluster-robust, composite), magnitude/scaling argument | composite mean gap `38.78%`, range `[35.78%,43.20%]`, `r=0.33` vs `t0`; `1/n`,`1/sqrt(n)` two-to-five orders of magnitude too small to explain an `O(1)` gap |

**Self-caught issue (disclosed, per this lineage's convention).** The
first draft of `g01_family_series.py`'s `solve_b_ode` descending-recursion
loop contained a dead/incomplete code fragment (an early, incorrect
list-indexed attempt, left un-deleted while a correct dict-indexed version
was written immediately below it) — caught while WRITING the script,
before it was ever executed, and removed via `Edit` before the first test
run. No incorrect number was ever produced or reported from the buggy
fragment (it was replaced before `g01_family_series.py` was run for the
first time); disclosed here anyway, per the archive's standing "disclose
even a caught-before-running issue" convention, and because the
anchor-validation discipline of §B.1 is precisely the check that would
have caught it had it survived.

---

## What remains open (honest, precise)

**Objective 1:**
1. The gap's exact source is **not identified**. Two named hypotheses are
   both weakened as PRIMARY explanations (§A.3, §A.4) but neither is
   replaced by a positive mechanism.
2. The T1-vs-T2-composite shape disagreement (§A.2) is a genuine,
   disclosed, UNRESOLVED tension in the record's own existing real-engine
   data — a properly-powered, uniformly cluster-robust re-measurement of
   `phi(ell)` across the whole `t0` range (benchmarked against the newly
   EXACT abstract constant, not the old 2-sig-fig value) is a concrete,
   checkable next step this front did not execute.
3. The discrete finite-pool toy model of §A.5 is sketched precisely but
   **not implemented or run** — the single most concrete, actionable next
   avenue this front identifies, deliberately not forced through under
   this front's time budget (per the mandate's anti-stall instruction).
4. A full replication of the real `n=65536` discrete permutation engine
   (as opposed to the toy finite-pool abstraction of §A.5) was judged too
   high-risk to attempt from scratch, with no reference implementation to
   cross-check against, within this front's scope — named as an even
   larger, separate undertaking.

**Objective 2:**
1. `gamma_5` (and the fifth asymptotic term `d4`) remains a **CONJECTURE**,
   not a derivation — this front's contribution is a substantially
   strengthened, independently-obtained NUMERICAL confirmation (`~5`
   digits for `d4`, `~2.6` for `d5`), not a proof. Deriving `gamma_5`
   rigorously requires carrying the boundary-layer expansion one further
   order (mechanical in principle per the record, not executed by either
   this front or its ancestor).
2. `gamma_n` for `n>=6` is entirely untouched.
3. H1 and H2 remain open exactly as before — no attempt was made here to
   justify the matched-asymptotics framework directly from the exact PDE
   system, and the referee's own named structural concern (order-2-entire
   growth, possible trans-series content) is neither confirmed nor
   excluded by anything in this front.
4. No new resummation ansatz or generating-function idea is proposed — the
   Borel and PSLQ exclusion results of the ancestor front stand entirely
   unrevisited.
5. The `c<100` range remains inaccessible (this front's own cost-wall
   probe was not pushed below `c=100`; no attempt was made at `c=40,10,1`,
   which the ancestor front's own attempts at higher target precision
   failed to complete).

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `phi_U(c)`, `phi_infinity(c)`, and the four-term asymptotic
law of record are all untouched and unaffected by anything in this
document.

---

## Files

| file | role |
|---|---|
| `g01_family_series.py` | fresh `(P,Q)`-family recursion implementation (§B.1) |
| `g02_validate_anchors.py`/`.log` | validation against 6 published anchors (§B.1) |
| `g03_timing_probe.py`/`.log` | efficient `(K,dps)` working-point search, 3-way error control (§B.2) |
| `g04_compute_grid.py`/`.log`, `g04_grid_results.json` | 11-point independent `Pi(c)` grid, `c=100..655360` (§B.2) |
| `g05_residual_isolation.py`/`.log`, `g05_residual_results.json` | residual-isolation fits for `d4`,`d5` (§B.3) |
| `g06_gamma_structure_check.py`/`.log` | independent sympy `gamma_n`/`R` structural check (§B.4) |
| `h01_gap_characterization.py`/`.log` | bin-resolved abstract-vs-real gap tables + magnitude argument (Part A) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/`
subdirectory was written to — every ancestor `ATTEMPT.md`/`adversarial/`
file and `PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (§0), never modified. No `adversarial/` subdirectory
created; no referee dispatched by this front itself, per the mandate.
