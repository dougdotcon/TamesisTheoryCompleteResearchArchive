# REFEREE REPORT — `mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md`

**Wave 19, front (d), `MCLUST-PLATEAU-ABSTRACT-REAL-GAP-ATTEMPT`, authorized
by `DISC-DEC-083`. Mandatory independent adversarial verification.**

**Scope.** `M-CLUST(b)`, Tree B of `PROOF_DEPENDENCY_MAP.md`, node under
`FLOORH2`/`PLATRESUM`. Pure combinatorial/asymptotic mathematics about an
abstract random-permutation-with-reroutes ensemble. **This is not a
Millennium Prize Problem, not the Conjecture-1/whole-space (Tree A) line,
not `phi_REDB`, and no claim of progress on a Millennium Problem appears
anywhere in this report.**

Object under review: `ATTEMPT.md` (two objectives — (1) re-characterizing
the abstract-vs-real ~30% gap; (2) a fifth-term push on the plateau
resummation), both explicitly framed by the mandate as honest-non-closure
acceptable.

---

## VERDICT

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue, at the tier claimed
> for both objectives.**
>
> Every central numerical and symbolic claim in the document independently
> reproduces, from a completely fresh implementation (own recursion code,
> own multi-`c` grid at different `(K,dps)` working points, own fitting
> code, own sympy derivation), to the precision the document itself
> claims. No overclaim was found in either objective's headline numbers or
> tier framing. Two moderate/minor named issues are raised below (§4, §6)
> — one a genuine completeness gap in the Sec A.4 magnitude argument
> (does not overturn its conclusion, which is already correctly hedged),
> one a minor bin-mislabeling in Sec A.2's citation of the ancestor's
> cluster-robustness check (does not affect any number used). Neither
> issue changes the document's tier self-assessment.

---

## 0. Method and discipline

Per the mandate: no `.py` file belonging to this front, either ancestor
front (`floor_h2_b1_full_closure_attempt`, `plateau_resummation_attempt`),
their referees, or the grandparent `floor_closed_form_attempt` was opened,
read, or imported at any point — including this front's own `g01`-`g06`,
`h01` scripts. Everything below was rebuilt from the mathematical prose of
`PROOF_DEPENDENCY_MAP.md` Tree B §2 (node `FLOORH2`/`PLATRESUM` and every
dated addendum through `DISC-DEC-077`), the FULL prose of
`floor_h2_b1_full_closure_attempt/ATTEMPT.md` + its
`adversarial/REFEREE_REPORT.md`, the FULL prose of
`plateau_resummation_attempt/ATTEMPT.md` + its
`adversarial/REFEREE_REPORT.md`, the target `ATTEMPT.md` itself, and (for
the real-engine `phi(ell)` tables cited in Objective 1) the relevant
sections of `floor_closed_form_attempt/ATTEMPT.md` (§2, §4) — all prose
only.

`mpmath` (dps up to 260) and `sympy` were used throughout for
arbitrary-precision arithmetic and exact symbolic algebra. Seeds: this
front's reserved range `20260886000-999` and the referee range
`20260887000+` were grep-confirmed to appear only in ledger/queue
reservation lines (`grep -rn "20260887" 05_DISCOVERY_LAB/` — matches only
in the target's own `ATTEMPT.md`, `DECISION_LEDGER.yaml`, and
`TEST_QUEUE.yaml` reservation text). **No randomness was needed anywhere
in this review** — every check is either exact symbolic algebra or
deterministic high-precision series summation — so no seed from either
range was drawn.

Files produced by this review, all in this `adversarial/` subdirectory:

| file | role |
|---|---|
| `ref01_family_series.py`/`.log` | fresh, from-scratch `(P,Q)`-family recursion implementation, re-derived by hand from the PDE prose (§1 below); anchor validation |
| `ref03_plateau_compute.py` | `Pi(c)` computation with 3-way-style error control (multiple `c*t0` targets, last-term/stable-digit diagnostics) |
| `ref04_grid.py`/`.log`, `ref04_grid_results.json` | independent 11-point `Pi(c)` grid, `c=100..655360`, own `(K,dps)` tuning per `c` (§2) |
| `ref05_residual_isolation.py`/`.log` | independent residual-isolation fit for `d4`,`d5` using my own grid (§3) |
| `ref06_symbolic_check.py`/`.log` | independent sympy verification of the `R`/`gamma_n` closure identities (§3.3) |
| `ref07_gap_tables.py`/`.log` | independent recomputation of the T1/T2 gap tables, mean/range/Pearson-`r` (§4) |
| `ref08_scaling_completeness.py`/`.log` | completeness check on the Sec A.4 magnitude argument against additional candidate finite-`n` rates (§4.3) |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was written. No git
command was run.

---

## PART A — Objective 2 (the fifth-term push): checked first, since it is
more independently machine-checkable than Objective 1

### 1. Re-deriving the `(P,Q)`-family recursion (independent, from the PDE)

Working only from the governing PDE system as restated in the target
document's Sec 0 (`dPhi/ds - dPhi/dg = c[Phi-W]`, `dPsi/ds = c[Psi-W]`,
`W = g*Avg_g[Phi] + (1-s-g)*Psi`), I matched powers of `g` by hand
(`Phi = sum a_k(s) g^k`, `Psi = sum b_k(s) g^k`) and re-derived exactly
the stated recursion:

```
a_{k+1}(s) = [a_k'(s) - c*a_k(s) + c*w_k(s)] / (k+1)
b_k'(s) - c*s*b_k(s) = -c*a_{k-1}(s)/k + c*b_{k-1}(s)
w_k(s) = a_{k-1}(s)/k + (1-s)*b_k(s) - b_{k-1}(s)
```

For the family representation `P(s) + Q(s)*erfcx(s*sqrt(c/2))`, I
independently re-derived: (i) the closure identity
`E'(s) = c*s*E(s) - sqrt(2c/pi)` from `erfcx'(z) = 2z*erfcx(z) - 2/sqrt(pi)`
via the chain rule; (ii) the `b`-ODE solve `b' - c*s*b = A + B*E` by
writing `b = U + V*E`, getting `V' = B` (one free constant `kappa`) and
`U' - c*s*U = A + sc*V =: R`, then solving the polynomial `U` by matching
powers of `s` DESCENDING from the top degree of `R` (forcing
`deg(U) = deg(R)-1`), with the leftover low-order relation pinning
`kappa`. **I validated this by hand on a concrete case before trusting
the general implementation**: solving for `b_2` from `a_1=-c`, `b_1=psi1`
by this method reproduces the record's own closed form
`b_2(s) = -c - (c/2)*sqrt(pi c/2)*(1-2s)*erfcx(s*sqrt(c/2))` exactly,
including the sign and value of `kappa`.

**Anchor validation (`ref01_family_series.log`, `K=6`, `dps=50`, `c=1000`),
all 6/6 exact on the first run of the finished implementation:**

| quantity | my value | published anchor | rel. diff |
|---|---|---|---|
| `a2(0)` | `520316.63648803...` | `520316.636488` | `~10^-14` |
| `a3(0)` | `-180730907.62850806...` | `-180730907.6285` | `~10^-14` |
| `a4(0)` | `47146963944.137885...` | `47146963944.14` | `~10^-14` |
| `b2(0)` | `-20816.636488030...` | `-20816.636488` | `~10^-14` |
| `b1(0)` | `39.633272976060110...` | `sqrt(pi*1000/2)` | exact (identical to displayed precision) |
| `Phi(0,0.002)` | `0.158500145747308484...` (at `K=60`, converged) | `0.15850015` | matches to all published digits |

### 2. Independent multi-`c` grid, including `c=100`

Using my own implementation, tuned independently (own `(K,dps)` per `c`,
no correspondence to any ancestor script's sizing), I computed `Pi(c)` at
the **same 11 points the target document uses** (`c=100` to `655360`, a
`6553x` range), each with a 3-way approach-error check (`c*t0` in
`{60,80,100}`, agreement between the two largest targets reported as
"stable digits"). Full log: `ref04_grid.log`.

| `c` | my `Pi(c)` (leading digits) | stable digits | matches target's claimed value? |
|---|---|---|---|
| 100 | `0.10883475474933102253...` | 34 | **yes, all 20 quoted digits** |
| 250 | `0.07222263178151416196...` | 34 | **yes, all 21 quoted digits** |
| 640 | `0.04666266520579072643...` | 33 | **yes, all 21 quoted digits** |
| 1000 | `0.03776159834021261882...` | 33 | **yes, all 21 quoted digits** |
| 2560 | `0.02402177558766597640...` | 33 | **yes, all 21 quoted digits** |
| 6400 | `0.01536222721588020350...` | 33 | **yes, all 21 quoted digits** |
| 16000 | `0.00978544240443958604...` | 32 | **yes, all 21 quoted digits** |
| 40960 | `0.00614439327855519180...` | 32 | **yes, all 21 quoted digits** |
| 100000 | `0.00394346489098030786...` | 32 | **yes, all 21 quoted digits** |
| 250000 | `0.00249866318713473057...` | 32 | **yes, all 21 quoted digits** |
| 655360 | `0.00154513120966623087...` | 31 | **yes, all 21 quoted digits** |

**All 11 of the target's grid values reproduce to every digit it quotes**,
from a wholly independent recursion implementation and a differently-sized
`(K,dps)` grid (I used `K=1000,dps=220` at `c=100`, taking 28s, versus the
document's `K=1800,dps=300`, taking 112s — different sizing, same
result). **This independently confirms the specific, checkable claim that
`c=100` is reachable** — a value neither ancestor front's own
direct-summation attempt (`plateau_resummation_attempt` Sec 2.2/§3)
completed (their disclosed cost wall stopped at `c=250`, `736s`, 46
digits; `c=100` never produced output in either ancestor).

**Self-caught issue in this review's own process (disclosed).** My first
attempt at the `c=100` value (targets `{80,100,120}`, `K=1100,dps=220`)
gave only **6** stable digits and a value that DIFFERED starting at the
~7th significant digit from a subsequent, more carefully-sized run — a
pure precision/working-point sizing problem (the `ct0=120` target at
`c=100` needs substantially more working precision than my first guess
supplied, not a bug in the recursion itself: the SAME code, re-run with
`K=1200,dps=260` and again with `K=1000,dps=220` at the gentler target set
`{60,80,100}`, both converge cleanly to 34+ stable digits and agree with
each other and with the target document's claimed 20-digit value). Caught
by this review's own stable-digit diagnostic before any number was
trusted or reported; the final grid in `ref04_grid.log` uses only the
converged, cross-checked sizing.

### 3. Residual isolation: independent fit for `d4`, `d5`

Using **my own** grid (§2 above — no numbers shared with the target
document's grid), and the ALREADY-EXACT closed forms
`d0=1, d1=-2*sqrt(2/pi), d2=7/2, d3=-(34/3)*sqrt(2/pi)` (not re-fitted),
I computed `R4(c) := [y(eps)-d0-d1*eps-d2*eps^2-d3*eps^3]/eps^4` and fit
it against `eps` by several independent methods (`ref05_residual_isolation.log`):

**Sanity check first**: `(y-d0-d1*eps-d2*eps^2)/eps^3` should trend toward
the ALREADY-DERIVED `d3=-9.0426917...` as `eps->0`. It does, monotonically:
`-7.05` (`c=100`) `-> -7.66 -> -8.12 -> ... -> -9.01` (`c=655360`) — a
clean, monotone approach exactly as expected for a genuine `eps`-expansion,
not an artifact.

**`d4`, `d5` fits (all 4 methods matching the target document's own
methods, independently computed):**

| method | my `d4` | my `d5` |
|---|---|---|
| linear fit, all 11 pts | `25.96064733` | `-62.7637776` |
| linear fit, 5 largest-`c` | `26.12096869` | `-79.74300192` |
| **quadratic fit, 7 largest-`c`** | **`26.12464128`** | **`-82.01744048`** |
| quadratic fit, all 11 pts (LSQ) | `26.1119381` | `-79.2774206` |

**Comparison against the target document's own reported values (same
methods): `d4` differs by `4.1e-5`, `d5` by `-4.4e-4`** — essentially
exact agreement given the different `(K,dps)` sizing and independent
implementation. **Comparison against the conjectured values**:
`d4=26.12464128` vs `209/8=26.125` (`-0.0014%`, matching the document's
claimed "~5 significant digits" agreement almost exactly); `d5=-82.01744`
vs `-(1546/15)*sqrt(2/pi)=-82.2353` (`-0.265%`, matching the claimed "~2.6
digits" exactly).

**Assessment of the residual-isolation technique itself.** This is a
sound, well-motivated variance-reduction technique, not merely a
relabeling: removing the exactly-known lower-order terms before fitting
shrinks the dynamic range the fit must resolve (the raw `y(eps)` values
span from `0.868` at `c=100` to `0.998` at `c=655360` — a narrow range
dominated by the `d0=1` term — while `R4(c)` spans `19.95` to `26.02`,
directly exposing the higher-order structure without an ill-conditioned
simultaneous 7-unknown Vandermonde solve). My own results independently
confirm the qualitative pattern the target reports: fits using the
widest-`eps` (smallest-`c`) subsets are visibly worse-conditioned
(linear-all: `-0.63%` off `d4`) than fits restricted to the
narrowest-`eps` (largest-`c`) subsets (quadratic-7: `-0.0014%`) — exactly
the signature of a genuine, convergent asymptotic expansion contaminated
by unresolved higher orders at large `eps`, not overfitting.

### 3.3 Symbolic verification of the `R`/`gamma_n` bookkeeping

Independent sympy derivation (`ref06_symbolic_check.log`), all checks PASS
exactly:

1. **`R'(x) = x*R(x) - 1`** for `R(x)=sqrt(pi/2)*erfcx(x/sqrt(2))`:
   symbolic residual simplifies to exactly `0`.
2. **Closure identity `R^{(n+1)} = x*R^{(n)} + n*R^{(n-1)}`, `n=1..6`**: all
   6 residuals simplify to exactly `0`.
3. **`psi_n(0) = gamma_n * R^{(n-1)}(0)` bookkeeping, `n=1..4`**: using the
   record's own already-established `psi_n(0)` values
   (`sqrt(pi/2), -2, (7/2)sqrt(pi/2), -34/3`), I computed `R^{(n-1)}(0)`
   independently from the closure identity and recovered
   `gamma_n = 1, 2, 7/2, 17/3` exactly — **4/4 match**, confirming
   `gamma_n` is forced by the bookkeeping, not free numerology.
4. **`gamma_5=209/24  <=>  d4=209/8`**: re-deriving the mapping
   `d_n = sqrt(2/pi)*psi_{n+1}(0)` from the stated definitions
   (`y(eps):=Pi(c)*sqrt(2c/pi)`, `Pi(c)=sum_k eps^k*psi_k(0)`), and cross
   checking it reproduces `d0..d3` correctly (it does, exactly, 4/4),
   substituting `gamma_5=209/24` gives `psi5(0) = 209*sqrt(2pi)/16`, hence
   `d4 = sqrt(2/pi)*psi5(0) = 209/8` — **EXACT MATCH**, sympy
   `nsimplify`-confirmed exact rational arithmetic, matching the target's
   claim precisely.

### 3.4 Assessment: Objective 2's tier claim

**Accurate, not overclaimed.** Every headline number (6/6 anchors, all 11
grid points including the `c=100` reachability claim, `d4=26.1246`,
`d5=-82.017`, all 4 symbolic identities) independently reproduces from a
completely fresh implementation. The document correctly and repeatedly
states this is NUMERICAL confirmation, not a derivation of `gamma_5`; H1
(uniform validity of matched asymptotics) and H2 (uniqueness of the
bounded-order solution) are correctly left untouched — nothing in this
review's checks bears on H1/H2 either (my checks confirm the SPECIFIC
numerical claims, exactly as the ancestor referee's own analogous check
did for the `n<=4` law; this is corroborating, not conclusive, evidence
for H1/H2, exactly as both the target document and its ancestor's referee
already frame it). "STRENGTHENED NUMERICAL CONFIRMATION of an existing
conjecture ... no new derivation" is the correct tier label.

---

## PART B — Objective 1 (the abstract-vs-real gap)

### 4. Independent recomputation of the gap tables

Using the SAME `phi_real` values transcribed verbatim from
`floor_closed_form_attempt/ATTEMPT.md` §2 (T1) and §4 (T2 point-level +
cluster-robust re-measurement) — read directly from that document's prose,
not from any script — and the independently-confirmed
`Pi(1000)=0.0377615983402126188243712025905770479904...` (§2 above), I
recomputed every gap%, the composite mean/range/spread, and the Pearson
correlation from scratch (`ref07_gap_tables.log`):

| statistic | target's claim | my recompute |
|---|---|---|
| T1 gaps (6 bins) | `26.72%` to `49.26%` | **identical**, all 6 values match to 2 decimal places |
| T2 composite mean | `38.78%` | **`38.78%`** |
| T2 composite range | `[35.78%, 43.20%]` | **`[35.78%, 43.20%]`** |
| T2 composite spread | `7.41 pp` | `7.415 pp` (rounds to `7.41`/`7.42`, negligible) |
| Pearson `r(gap%,t0)` | `0.331` | `0.3302` |

**Every number in Sec A.2's tables is arithmetically correct and
internally consistent** — no computational error found anywhere in the
gap-table arithmetic.

### 4.1 The mode-`G`/mode-`E` `s+g` structural claim

**Verified as correct, elementary PDE-characteristics reasoning.** The
document's claim: in mode `G`, `dPhi/ds - dPhi/dg = c(Phi-W)` has
characteristic direction `(ds,dg)=(1,-1)`, so along that characteristic
`d(s+g)/dt = 1 + (-1) = 0` — `s+g` is exactly conserved. In mode `E`,
`dPsi/ds = c(Psi-W)` has NO `dg`-dependence at all, so its characteristic
is `(ds,dg)=(1,0)`, giving `d(s+g)/dt = 1` — `s+g` grows at unit rate.
This is a direct, correct reading of the two PDEs stated identically by
every document in this lineage (wave-14 SS5, restated unchanged through
`FLOORH2`/`PLATRESUM`) — I re-derived it independently by inspection of
the characteristic directions and confirm both claims exactly. This part
of the document's argument is sound, not merely plausible.

### 4.2 The argument against the `s+g<=1` boundary hypothesis

**Logically coherent, appropriately hedged, not rigorously conclusive —
exactly as the document itself frames it.** The inference ("boundary
mechanism should predict a `t0`-growing gap; the observed gap is roughly
flat; therefore boundary is not the PRIMARY driver") rests on one
unverified (though reasonable) intermediate assumption: that the
magnitude of any boundary-crossing excess scales with the available
"room" `1-t0`. The document does not prove this scaling relationship from
the PDE system directly — it is a plausibility argument, not a derivation
— and the document says so explicitly ("not decisive," "a modest
additional boundary contribution ... is not excluded"). I find no flaw in
the logic given the stated premise, and no attempt to oversell it beyond
that premise's own honest hedging.

### 4.3 The magnitude argument against a vanishing finite-`n` effect — a
named completeness gap

I recomputed the document's three candidate rates and independently
verified: `1/n=0.0015%`, `1/sqrt(n)=0.39%`, `sqrt(c/n)=12.35%`, all
correctly computed against the observed `~38.8%` gap at `n=65536,
c=1000` (`ref08_scaling_completeness.log`). The document's own conclusions
for these three specific rates are correct: `1/n` and `1/sqrt(n)` are
implausibly small (need `~2500x`-`100000x` prefactors); `sqrt(c/n)` needs
a real, unexplained `~3.1x` prefactor.

**However, the set of three tested rates is not exhaustive, and this
review finds other natural candidates that come markedly closer without
an implausible prefactor:**

| rate | value | prefactor needed to match 38.8% |
|---|---|---|
| `sqrt(c/n)` (document's most generous candidate) | `12.35%` | `~3.14x` |
| `(c/n)^(1/3)` (not tested by the document) | `24.80%` | `~1.56x` |
| `(c/n)^(1/4)` (not tested by the document) | `35.15%` | `~1.10x` |

`(c/n)^{1/4}` in particular comes within `10%` of the observed magnitude
with essentially no unexplained prefactor at all — a candidate rate the
document's own analysis does not consider. **This does not overturn the
document's conclusion**, which is already correctly hedged ("at least not
at any of the natural small-parameter rates checked here") — the document
never claims to have ruled out ALL vanishing-finite-`n` explanations, only
the three it names. But it is a genuine, moderate-severity gap: a reader
could come away believing the vanishing-finite-`n` hypothesis is more
comprehensively disfavored than the document's own evidence actually
supports. **Named as issue N1 below.**

### 4.4 A minor citation-accuracy issue in Sec A.2

The document describes 2 of the 9 T2-composite bins (`t0~0.812`,
`t0~0.938`) as cluster-robust replacements for "the 3 rightmost bins"
where "the record's own replication showed the naive point-level estimate
is unreliable." Checking this against `floor_closed_form_attempt/ATTEMPT.md`
§4's own cluster-robustness table directly: the three bins that document
actually re-measured are `(24576,32768]`, `(49152,57344]`, `(57344,65536]`
in absolute-`L`, which correspond to `L/n` ranges `(0.375,0.5]`,
`(0.75,0.875]`, `(0.875,1.0]` — i.e., **bin positions 5, 8, and 9 of the
9-bin point-level table, not literally the 3 rightmost (which would be
positions 7, 8, 9)**. Bin 5 (`t0~0.438`) is in the middle of the range,
not at the tail. **This is purely a descriptive/citation imprecision, not
a computational error**: the target document correctly kept bin 5's
point-level value (`0.02722`, since it is the one of the three that
"survives" cluster replication per the source's own finding) and correctly
substituted the cluster-robust values only for bins 8 and 9 (the two that
do NOT survive) — every actual number used in the gap table is verbatim
correct, verified in §4 above. Only the prose label "the 3 rightmost
bins" is imprecise; it should read "the 3 bins the ancestor's
cluster-robustness check covered" or similar. **Named as issue N2 below
(minor, wording only, no effect on any reported number).**

### 4.5 Assessment: Objective 1's tier claim

**Accurate.** "DIAGNOSIS SHARPENED, not closed" correctly describes what
was achieved: a precise re-characterization (mean `38.8%`, range,
flatness, all independently confirmed to be arithmetically correct), a
sound (if heuristic) structural argument against one named hypothesis, a
magnitude argument against the other that is correct as far as it goes
but not exhaustive (§4.3), and no replacement mechanism proposed. The
document does not claim more than this anywhere, and the two named issues
above (§4.3, §4.4) are gaps in supporting detail, not overclaims of the
central finding.

---

## 5. Overall honesty-framing audit

| document's claim | this review's finding |
|---|---|
| Objective 1: composite gap `38.8%` mean, `[35.8%,43.2%]` range, `r=0.33` | **CONFIRMED**, exact arithmetic reproduction |
| Objective 1: `s+g` conserved in mode G, grows in mode E | **CONFIRMED**, correct PDE-characteristics reading |
| Objective 1: argument against boundary hypothesis | Logically sound given its stated (hedged, unproven) premise |
| Objective 1: argument against vanishing finite-`n` | Correct for the 3 rates tested; **NOT exhaustive** — named gap, §4.3 |
| Objective 1: "3 rightmost bins" description | **Imprecise** — actually bins 5, 8, 9; no effect on any number, §4.4 |
| Objective 2: 6/6 anchors, 11-point grid incl. `c=100` | **CONFIRMED**, every digit reproduces independently |
| Objective 2: `d4=26.1246`, `d5=-82.017` | **CONFIRMED**, independent method lands within `4e-5`/`4e-4` |
| Objective 2: `gamma_n`/`R` symbolic bookkeeping, `gamma_5<=>d4=209/8` | **CONFIRMED**, exact symbolic match |
| Objective 2: H1/H2 not closed, no new derivation | Accurate; nothing in this review touches H1/H2 either |
| Neither objective touches `phi_REDB` or any formula of record | **CONFIRMED** — nothing in this review's checks, or the document's own claims, proposes any replacement |

---

## 6. Named issues (for governance / future fronts)

- **N1 (moderate, Sec A.4).** The magnitude argument against a vanishing
  finite-`n` effect tests only `1/n`, `1/sqrt(n)`, `sqrt(c/n)`. This
  review finds `(c/n)^{1/3}` and especially `(c/n)^{1/4}` come much closer
  to the observed `~38.8%` gap with unremarkable prefactors (`~1.56x`,
  `~1.10x` respectively) — candidates the document does not consider.
  Recommended correction: note explicitly that the magnitude argument
  disfavors only the specific rates tested, not the broader class of
  vanishing finite-`n` corrections in `c/n` at other powers.
- **N2 (minor, Sec A.2, wording only).** "The 3 rightmost bins" should be
  corrected to accurately describe which 3 bins the ancestor's
  cluster-robustness check covered (positions 5, 8, 9 of the 9-bin table,
  not 7, 8, 9). No numerical value in any table is affected.

Neither issue changes the document's tier self-assessment for either
objective, nor any of its central numerical claims — both issues concern
the completeness/precision of supporting argument or citation, not the
correctness of what is reported as established.

---

## 7. Self-caught issues in this review's own process (disclosed)

- A first attempt at computing `Pi(100)` with an overly ambitious `c*t0`
  target (`120`) at insufficient working precision (`dps=220`) gave only 6
  stable digits and a value that disagreed with a subsequent, correctly-
  sized run starting at the 7th significant digit. Caught by this review's
  own stable-digit diagnostic (comparing the two largest `c*t0` targets)
  before the number was used anywhere; the final grid (`ref04_grid.log`)
  uses only the converged, cross-validated sizing (`c*t0` targets
  `{60,80,100}`, `K=1000,dps=220`), which independently reproduces the
  target document's claimed value to all 20 quoted digits. This was a
  precision-tuning mistake in my own review, not a bug in the recursion
  implementation (the same code, correctly sized, converges cleanly).
- No other bug was found in this review's own code.

---

## 8. Final assessment

Both objectives' claimed tiers — "DIAGNOSIS SHARPENED, not closed" for
Objective 1, "STRENGTHENED NUMERICAL CONFIRMATION of an existing
conjecture ... no new derivation" for Objective 2 — are accurate and
appropriately hedged. Every independently-checkable numerical and symbolic
claim reproduces from a completely fresh implementation sharing no code
with any ancestor front or with this front's own scripts. Two named issues
are raised (§6), both concerning the completeness of supporting arguments
or the precision of a citation, neither touching the correctness of any
number the document reports as established. `phi_REDB`, `phi_U(c)`,
`phi_infinity(c)`, and the four-term asymptotic law of record remain
untouched, as both the document and this review confirm.

**Verdict: SOUND WITH NAMED ISSUES — ACCEPT for catalogue**, with the
recommended (non-mandatory, since neither issue affects a reported number
or the tier verdict) corrections N1/N2 noted for a future revision.

No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, or `DISCOVERY_LAB_STATE.md` file was read for writing,
modified, or touched by this review. No git command was run. Nothing
outside this `adversarial/` subdirectory was written.
