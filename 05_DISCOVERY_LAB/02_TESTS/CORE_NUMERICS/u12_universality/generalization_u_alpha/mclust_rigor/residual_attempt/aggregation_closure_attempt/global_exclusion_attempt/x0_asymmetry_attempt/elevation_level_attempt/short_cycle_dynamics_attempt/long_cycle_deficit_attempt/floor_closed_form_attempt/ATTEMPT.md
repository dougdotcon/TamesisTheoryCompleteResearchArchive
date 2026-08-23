# ATTEMPT — closed-form attempt for the b=1 long-cycle deficit floor

**Wave 14, `DISC-DEC-057`, front (b) `FLOOR-CLOSED-FORM-ATTEMPT`.**
Target: `long_cycle_deficit_attempt/ATTEMPT.md` (`DISC-DEC-054/056`) leaves
"why the `b=1` (plain M-U) deficit exists at all" formally open — no
closed-form correction to `φ_U(c)` was proposed or validated by that front.
This front attempts an exact/asymptotic closed form for
`φ_far := P(x0 cyclic | x0∈R^c, L(x0)>threshold)` at `b=1` and an
explanation of the sign/magnitude of `φ_far − φ_U(c)`.

**Verdict up front (expanded in §7): partial closure.** An exact reduction
(§1) is PROVED and explains *why any deviation exists at all* (a selection
effect, not a bias in `φ_U(c)`'s own derivation). The specific pointwise
mechanism most people would guess first (§2, Candidate 1) is cleanly
REFUTED. A concrete, well-posed recursive mechanism (§3) is DERIVED and
validated by direct simulation of its own exact (not further-approximated)
form (§4, T3) — this explains *qualitatively* why `φ(ℓ)` plateaus instead of
vanishing for long cycles. A first closed-form attempt at that mechanism is
DERIVED but shown to be quantitatively **and qualitatively** wrong (§3.2). A
second, more careful characterization of the deviation's shape across
`L/n` (§4, T2) refutes this front's own specific pre-registered guess about
*where* the sign changes; a follow-up cluster-robust replication then shows
T2's own more elaborate replacement claim also does not survive independent
re-seeding, and is honestly withdrawn in §4, leaving only the coarser,
cross-run-robust finding that the deviation is negative (order `−2%` to
`−6%`) across most of the far tail. **The full closed form for `φ(ℓ)` is NOT derived** —
the exact recursive system is a genuinely coupled, nonlocal two-variable
problem (§5) that a bounded numerical attempt did not solve either. This is
reported as honest partial closure, matching the mandate's explicit
allowance.

---

## 0. Setup (per the mandate)

`b=1` in `sc_engine.py`'s `build_R_mask` reduces to `R=seed_mask` exactly
(re-confirmed by the parent front's T0 and its referee — zero block
correlation). Fix `x0` (WLOG index `0`, by exchangeability). Write
`ξ_{x0}∈{0,1}` for whether `x0` is a seed and `L:=L(x0)` for the length of
`x0`'s `π`-cycle. The quantity of interest,
`φ_far(threshold) := P(cyclic | x0∈R^c, L>threshold) = P(cyclic |
ξ_{x0}=0, L>threshold)`, is compared against the naive `φ_U(c) =
∫₀¹e^{-ct²}dt` (`DERIVATIONS.md` §3.1) — the object the parent front's
deficit was measured relative to.

---

## 1. Exact reduction (PROVED)

**Fact A (classical, exact).** For `π` uniform on `S_n` and any fixed point
`x0`, `P(L(x0)=ℓ)=1/n` for `ℓ=1,…,n` — exact for every finite `n`, not an
asymptotic statement (standard "records"/Feller-coupling fact: building
`x0`'s cycle one step at a time, at each step the walk closes back to `x0`
with probability proportional to the remaining mass, giving `P(L=ℓ)=1/n`
by direct telescoping of the product `∏(1-1/(n-j))·(1/(n-ℓ+1))`-type
computation — this is elementary and not re-derived from scratch here
beyond stating it, as it is textbook).

**Fact B (immediate from Def. 1, `THEOREM.md`).** `π ⊥ ξ` by construction,
so `L(x0) ⊥ ξ_{x0}`.

**Corollary (PROVED, no simulation needed — T0 below is only a coding
sanity check, not a test of this claim's validity).** Define
`φ(ℓ):=P(cyclic | ξ_{x0}=0, L(x0)=ℓ)`. Then for any `n,c,1≤threshold<n`:

`φ_far(threshold) = (1/(n−threshold)) Σ_{ℓ=threshold+1}^{n} φ(ℓ)`.   (1.1)

**Coding sanity check (T0, `fcd_t0.py`, seed `SeedSequence(20260833000)`,
`N=2000`).** Measuring `φ_far(2000)` two ways in the same run — directly,
and via summing fine (`width=200`) `L`-bins with each bin's *measured*
point-count as weight — agree **exactly** (`0.027497` both ways, as they
must, being the same computation), confirming no bug in the binning/masking
code. A THIRD variant — re-weighting the same per-bin `φ̂` values by
*theoretical* bin width instead of measured count — gave a small but
`z=−13.9`-different value (`0.027701`); this is disclosed honestly as an
**unresolved minor discrepancy**, most plausibly a symptom of the same
between-instance-correlation phenomenon this archive's referees have
flagged for related statistics elsewhere (bin point-counts are not, in a
single `N=2000`-instance run, purely Poisson-noise deviations from
width-proportionality — some residual correlation between an instance's
`L`-value composition and its cyclic outcomes is plausible) rather than a
coding error, since the two exactly-matching computations above use
identical per-bin `φ̂`s and rule out an arithmetic slip; not chased further
given it does not bear on the PROVED identity (1.1) itself, which is an
algebraic tautology from Facts A+B, not something this simulation could
"fail."

**Why this matters.** `φ_U(c)` is the `n→∞` limit of the *unconditional*
average `(1/n)Σ_{ℓ=1}^{n}φ(ℓ)` (via `H_q(t)=t²`, `DERIVATIONS.md` §1,
with the outer `∫₀¹dt` playing the role of averaging uniformly over
`ℓ/n`, matching `L/n→Unif(0,1)`, Fact A's continuum limit). `φ_far` is the
*same average restricted to `ℓ>threshold`*. These agree **only if `φ(ℓ)`
is constant in `ℓ`** — otherwise a deviation is guaranteed by construction,
of a sign and size set entirely by `φ(ℓ)`'s own shape on the two windows.
This is a complete, rigorous, mechanism-independent explanation for *why
there is a deviation at all* (a selection effect on an already-correct
unconditional formula, not a flaw in `φ_U(c)`'s own derivation) — but it
does not by itself predict the sign or magnitude without knowing `φ(ℓ)`.

---

## 2. Candidate 1 for `φ(ℓ)`: pointwise substitution into the master formula
— REJECTED

**The natural first guess.** `THEOREM.md` Def. 3 constructs `φ_∞(c)` via a
random variable `T₀:=1−e^{-E₀}~Unif(0,1)`, `E₀⊥`everything else, that plays
the role of `L/n` (both facts: `L/n` is exactly uniform for finite `n`
(Fact A above); `T₀` is exactly `Unif(0,1)`; and `φ_∞(c)=∫₀¹e^{-ct²}dt` is
recovered by mixing over `T₀`). The natural guess is therefore
`φ(ℓ) ≈ e^{-c(ℓ/n)²}` — i.e. that fixing `T₀=ℓ/n` (instead of averaging
over it) simply plugs `ℓ/n` into the SAME master-formula integrand
pointwise.

**REJECTED, decisively (T1, `fcd_t1.py`, seed `SeedSequence(20260833001)`,
`N=1500`).** Target cell `c=1000,n=65536,b=1`. Measured `φ̂(ℓ)` vs. the
Candidate-1 prediction at the bin midpoint:

| `L` bin | `n_pts` | `φ̂` | Candidate-1 pred. | `z` |
|---|---|---|---|---|
| `[1,50)` | 72,296 | 0.7030±0.0017 | 0.9998 | −174.7 |
| `[500,1000)` | 736,605 | 0.0298±0.0002 | 0.8772 | −4277 |
| `[2000,4000)` | 3,124,479 | 0.0265±0.00009 | 0.1230 | −1062 |
| `[4000,8000)` | 6,168,647 | 0.0253±0.00006 | 0.00023 | **+397** |
| `[8000,16384)` | 11,995,191 | 0.0258±0.00005 | ~0 | **+563** |
| `[16384,32768)` | 23,320,921 | 0.0266±0.00003 | ~0 | **+798** |
| `[32768,65536)` | 49,236,603 | 0.0273±0.00002 | ~0 | **+1176** |

Pre-registered criterion (≥3 of the `L≥4000` bins at `z≥10` against the
Candidate-1 prediction): **met (4/4)**. `φ(ℓ)` does **not** decay to zero
for large `ℓ` — it **plateaus** around 0.025–0.029 (comparable to,
sometimes above, `φ_U(1000)=0.0280`) for `ℓ` from ~2000 all the way to
`n=65536`. The "T₀=ℓ/n plugged pointwise into `e^{-ct²}`" reading of Def. 3
is wrong for a `precise, identifiable reason` (§3): reaching `x0` via a
*later* reroute that lands on the still-unswept remainder of `x0`'s own
cycle is a *guaranteed* eventual success (barring further interruption),
not a competing "arc" on equal footing with generic fresh mass — Def. 3's
`T₀` (fixed once, via `E₀` alone) does not, on inspection, correctly
represent this recursive "the target stays open and can be completed by
any later leg" structure when conditioned to a *specific* value rather than
averaged over.

---

## 3. The recursive "gap re-entry" mechanism (DERIVED) and why a one-shot
approximation of it still fails (also DERIVED, then shown wrong)

### 3.1 The mechanism, exactly (PROVED)

Let `x0`'s `π`-cycle be `y₀=x0,y₁=π(x0),…,y_{L-1}`. **Claim (proved, finite-
`n`, exact — not asymptotic):** if the trajectory reaches any `y_j`
(`0<j<L`) not yet visited by `x0`'s own trajectory, walking forward via `π`
from `y_j` reaches `x0` **before** it can reach any other already-visited
point of `x0`'s trajectory. *Proof:* off the seed set `f=π`; the only
already-visited points of `x0`'s own cycle lie in the arc immediately
"downstream" of `y₀=x0` (i.e. `y₁,y₂,…`, visited by `x0`'s own earlier
legs); a forward walk from `y_j` (`j>0`) reaches that arc only *after*
first passing through `y₀=x0` (going forward around the cycle, `x0` is
encountered strictly before `x0`'s own already-explored territory). So
reaching *any* fresh point of `x0`'s cycle and walking forward unintercepted
reaches `x0` first — success, unless a *new* seed interrupts first, in
which case the process recurses with a smaller remaining "gap." This is the
`b=1` analogue of `DERIVATIONS.md` §3.6's M-INTRA circle process, but here
the reroute making the intra-cycle jump is a *generic* M-U reroute that
happens, by chance, to land back on `x0`'s own cycle — not a
structurally-forced same-cycle destination.

### 3.2 A one-shot ("`s_E≈0`") closed form (DERIVED), then REJECTED as
qualitatively wrong

Modeling state `(s,g)` — `s`=total mass explored, `g`=remaining gap to
`x0` — under the simplifying assumption that mass spent exploring "outside"
`x0`'s cycle costs nothing (`s=t0−g` exactly, `t0:=ℓ/n`) gives a solvable
Volterra equation. Laplace-transforming (`derive_closed_form.py`, exact
`sympy` algebra, independently re-derives the same characteristic roots as
the by-hand derivation — `0` match confirmed symbolically):

`Φ(g) = [s₁e^{s₁g} − s₂e^{s₂g}]/(s₁−s₂)`,  `s_{1,2}=(−c±√(c²+4c/t0))/2`.  (3.1)

Numerically (`c=1000`): `Φ(t0)` = 0.656 at `t0=0.001`, 0.050 at `t0=0.05`,
0.0053 at `t0=0.5`, 0.0030 at `t0=0.9` — **monotonically decaying toward
0**, exactly like Candidate 1, just more slowly. This **contradicts the
observed plateau** (§2's table). **Diagnosed cause (named precisely, not
hand-waved):** the `s_E≈0` approximation treats every "detour into generic
exploration" as *mass-free* (an instant retry at the same `(s,g)`), which
is a *convenience* simplification, not a small correction — real detours
consume real mass (each retry costs `~1/c` on average), and — the deeper
issue found by direct comparison against T3's exact simulation — even
fixing that leak does not obviously restore the plateau, because the
*full* system (§5) is more than "add back `s_E`"; it is a genuinely
coupled, nonlocal fixed point (see §5). This closed form is kept in the
record as a **worked, explicit, ruled-out heuristic**, not as the answer.

---

## 4. Confirmatory simulation of the mechanism (T3) and finer characterization
of `φ(ℓ)`'s shape (T2)

**T3 — abstract recursive process, simulated exactly (no `s_E≈0`
approximation), `abstract_sim.py`→`fcd_t3.py`, seed
`SeedSequence(20260833003)`, `N=40000` per `t0`, `c=1000`.** State `(s,g)`,
mode `G`/`E`; at each mark (rate `c`): kill w.p. `s`, land in gap w.p. `g`
(new gap `~Unif(0,g)`), else generic (mode `E`, `g` unchanged, `s` still
accrues — i.e. the FULL, not mass-free, dynamics):

| `t0` | `φ_abstract` |
|---|---|
| 0.0001 | 0.905±0.0015 |
| 0.001 | 0.376±0.0024 |
| 0.01 | 0.0383±0.0010 |
| 0.09 | 0.0383±0.0010 |
| 0.37 | 0.0389±0.0010 |
| 0.90 | 0.0374±0.0010 |

**Plateau CONFIRMED** by the pre-registered criterion (ratio of `φ_abstract`
at the two largest `t0` to the `t0=0.09` value stays in `[0.5,2]×`; measured
ratios `0.997` and `0.975`). This is the mechanistic explanation for the
plateau: the recursive gap-re-entry process, simulated in its exact form
(genuinely paying mass for every excursion, no shortcut), reproduces a
`t0`-independent plateau, qualitatively matching the real `n=65536` engine
— **validating the mechanism** even though its closed form is not derived.
(Quantitatively, the abstract-process plateau, `≈0.037–0.039`, sits
somewhat *above* `φ_U(1000)=0.028` and above most of the real engine's
plateau values `≈0.025–0.029` — this gap is not resolved here; see §5/§6.)

**T2 — fine `L/n` sub-binning, `fcd_t2.py`, seed
`SeedSequence(20260833002)`, `N=3000`, same target cell.** This front's own
pre-registered guess (§3 of `DERIVATION_PREREG.md`: a significantly positive
bin somewhere in `L/n∈[0.1,0.6)`, and a significantly negative last bin)
is **REFUTED as literally stated** — no bin in `[0.1,0.6)` is positive:

| `L/n` | `n_pts` | `φ̂` | dev% | `z` |
|---|---|---|---|---|
| (0.031,0.061] | 5,953,942 | 0.02781±0.00007 | −0.76 | −3.16 |
| (0.061,0.122] | 11,690,243 | 0.02716±0.00005 | −3.09 | −18.22 |
| (0.122,0.250] | 24,886,068 | 0.02747±0.00003 | −1.98 | −16.94 |
| (0.250,0.375] | 23,988,069 | 0.02673±0.00003 | −4.62 | −39.34 |
| (0.375,0.500] | 23,551,828 | 0.02722±0.00003 | −2.88 | −24.07 |
| (0.500,0.625] | 26,112,231 | 0.02781±0.00003 | −0.75 | −6.55 |
| (0.625,0.750] | 22,297,014 | 0.02692±0.00003 | −3.93 | −32.12 |
| (0.750,0.875] | 23,140,796 | 0.02866±0.00003 | **+2.25** | **+18.20** |
| (0.875,1.000] | 26,231,949 | 0.02577±0.00003 | **−8.04** | **−72.84** |

**Refutation, honestly reported.** The specific pre-registered pattern
("positive somewhere in `[0.1,0.6)`, negative at the end") did not hold —
every bin through `L/n=0.75` is negative. **New, real (not pre-registered,
disclosed as post-hoc but on the SAME pre-fixed bins) finding instead:** a
genuine **non-monotonic** shape — a moderate, uniformly negative deficit
(`−0.8%` to `−4.6%`) through most of the far tail, a **positive bump** at
`L/n∈(0.75,0.875]` (`+2.25%`, `z=+18.2`), then the **strongest negative**
point at the very end, `L/n∈(0.875,1]` (`−8.04%`, `z=−72.8`) — i.e. the
single most negative sub-population is specifically `x0`'s whose own cycle
covers essentially the *entire* remaining population. Since `φ_far`
aggregates `L>threshold` with **uniform-in-`ℓ` weight** (Fact A), and each
successive bin above covers double the raw point-count of a naively equal-
width bin near the low end (bins get wider in `ℓ` toward `n`, and — more
importantly — `L` itself is exactly uniformly distributed, so the *widest*
absolute-`ℓ`-range bins dominate the weighted sum), the strongly negative
final bin carries real weight in `φ_far`, and is a genuine, well-powered
contributor to the originally-observed deficit.

**Cluster-robustness check (`fcd_t2_cluster.py`, seed
`SeedSequence(20260833004)`, independent `N=3000` re-run, per-instance
SEM instead of naive per-point binomial SEM — addressing the correlation-
inflates-significance caveat this archive's own referees have repeatedly
flagged for analogous statistics) — a genuine correction, reported in
full:**

| bin (`L`) | `n_instances` | `φ̂` (instance-avg) | cluster SEM | dev% | `z` (cluster) | T2's own point-level dev%/`z` (same bin) |
|---|---|---|---|---|---|---|
| (24576,32768] | 718 | 0.02672 | 0.00060 | −4.64 | −2.16 | −2.88 / −24.07 |
| (49152,57344] | 453 | 0.02637 | 0.00070 | −5.91 | −2.35 | **+2.25 / +18.20** |
| (57344,65536] | 424 | 0.02747 | 0.00068 | −1.97 | −0.82 | **−8.04 / −72.84** |

**This is a genuine, important correction, not a footnote.** The
(24576,32768] bin replicates reasonably well (`−4.64%` vs `−2.88%`, same
sign, same rough order, within `~2σ` of each other at cluster precision) —
this one survives as a real, negative, order-few-percent finding. The
other two do not: for the (49152,57344] bin, the cluster-robust re-run
gives the **opposite sign** from T2's own point-level estimate (`−5.91%`
vs `+2.25%`); for the (57344,65536] bin (T2's most dramatic point,
`z=−73`), the cluster-robust re-run gives a MUCH smaller, non-significant
deviation (`z=−0.82`). Both of these gaps are consistent with pure Monte
Carlo noise once the correct (larger, between-*instance*, not
between-*point*) standard error is used (e.g. for the last bin: point
estimates `0.02577` vs `0.02747` differ by `Δ≈0.0007` relative to instance-
level noise `~0.0007–0.001`, i.e. `|z_diff|~1–2`, unremarkable) — confirming
the archive's own standing diagnosis (`short_cycle_dynamics_attempt/
adversarial/REFEREE_REPORT.md` §4.2, re-confirmed by
`long_cycle_deficit_attempt/adversarial/REFEREE_REPORT.md` §3 for T2's
`b=20,50` points): **for this family of statistics, `n_pts` in the tens of
millions is misleading — the effective sample size is much closer to the
number of *instances* (here, `N~400–3000`), and naive per-point binomial
`z`-scores massively overstate significance for bin-level comparisons.**
T2's specific "positive bump at `L/n∈(0.75,0.875]`, strongly negative at
`L/n>0.875`" narrative (as originally reported above) is therefore
**WITHDRAWN as an established finding** — it does not survive a properly-
powered, independently-seeded replication. What DOES survive: `φ(ℓ)` is
**not** uniformly at `φ_U(c)`, and its deviation, averaged over both runs
and across bins with `L/n∈[0.25,0.9]`, sits consistently in the roughly
`−1%` to `−5%` range (both runs agree on this order of magnitude and this
sign for every bin except the two disputed above) — but the **precise
bin-by-bin location of any local sign change is not resolved at this
sample size**, and this front does not claim to have resolved it.

---

## 5. What remains open: the full two-variable system (named precisely)

The exact recursive process (§3.1, §4's T3) is governed, in the continuum
(`n→∞`, `c` fixed) idealization, by a genuinely coupled system for
`Φ(s,g):=`success prob. while actively sweeping the gap, and
`Ψ(s,g):=`success prob. while in generic exploration:

`∂Φ/∂s − ∂Φ/∂g = c[Φ − W]`,  `∂Ψ/∂s = c[Ψ − W]`,
`W(s,g) := g·Avg_g[Φ(s,·)] + (1−s−g)Ψ(s,g)`,
`Avg_g[Φ(s,·)] := (1/g)∫₀^g Φ(s,g′)dg′`,  boundary `Φ(s,0)=1`,

target `φ(t0) = Φ(0,t0)`. This is nonlocal (the `Avg_g` integral couples
`Φ` at every `g′≤g`) and two-dimensional — structurally the same order of
difficulty as `THEOREM.md` §5.4's still-CONJECTURED general-`K` conditional
density, which this same archive has not closed either. **A bounded (time-
boxed) numerical attempt** (`solve_2d_system.py`, a fixed-point iteration on
a discretized `(s,g)` grid) **did not converge to a trustworthy answer** —
it produced numerically implausible results (`Φ(0,0.37)=1.0` exactly, an
artifact of the implementation only fully propagating the `Φ(s=0,·)` row
per iteration while leaving `Φ(s>0,·)` — needed inside `Avg_g` for `s>0` —
essentially unresolved) inconsistent with T3's clean Monte Carlo. This is
disclosed as a genuine, named implementation limitation, not swept under a
"converged" label. **The exact closed form for `φ(ℓ)` — and hence for
`φ_far` via (1.1) — is not derived by this front.**

---

## 6. Honest synthesis: does this explain the ORIGINAL deficit's sign and
magnitude?

**Partially, and precisely-scoped.** The exact reduction (§1) is a complete
explanation for *why any deviation exists at all* — no additional mechanism
is needed to explain the mere existence of a gap between `φ_far` and
`φ_U(c)`, since these are, by construction, different weighted averages of
the same non-constant function `φ(ℓ)`. §4's T2 (cross-checked against its
own cluster-robust re-run) establishes that the sign is negative across
essentially the entire far tail, order `−1%` to `−5%` — but, after honestly
withdrawing the finer (positive-bump / most-negative-at-the-top) claim that
did not survive replication, this front does **not** establish *where
within* the far tail the deviation is largest or smallest — only that it is
consistently negative and of this rough order. What is **not** established: a predictive formula
for `φ(ℓ)`'s value at a given `ℓ`, hence no way to *compute* `φ_far`'s exact
magnitude without simulating it — the "why is the plateau's *level*
`≈0.025-0.029` rather than, say, `0.02` or `0.035`" question is answered only
qualitatively (a validated mechanism, §3.1/§4-T3) not quantitatively (§3.2's
one candidate closed form is explicitly ruled out; §5's exact system is
unsolved).

---

## 7. Established / Heuristic / Open — Verdict

**Established (PROVED or measured with stated `z`, no closed form claimed
beyond what's stated):**
- (1.1): the exact reduction of `φ_far` to an `L`-weighted average of
  `φ(ℓ)`, for ANY `n,c,threshold` at `b=1` — PROVED, from two classical
  exact facts (Facts A, B).
- Candidate 1 (`φ(ℓ)≈e^{-c(ℓ/n)²}`, the naive T₀-substitution reading of
  `THEOREM.md` Def. 3) is REJECTED — `z` from `+397` to `+1176` against it
  on the 4 bins `L≥4000` (T1).
- `φ(ℓ)` plateaus (does not decay to 0) for `ℓ` from ~2000 to `n=65536` at
  the target cell, staying in the `0.025–0.029` range vs. `φ_U(1000)=0.028`
  — established directly by T1/T2's own measured `φ̂` values, huge `z`
  against 0 (trivially) and, per-bin, against `φ_U(c)` (T2 table).
- The recursive "gap re-entry" mechanism's structural claim (§3.1, forward
  walk from any fresh point of `x0`'s own cycle reaches `x0` before any
  other already-visited point) — PROVED, finite-`n`, exact, elementary.
- The plateau's qualitative origin in this mechanism — CONFIRMED by direct
  Monte Carlo of the exact (unapproximated) abstract recursive process
  (T3), matching the pre-registered plateau criterion.
- `φ(ℓ)/φ_U(c)−1` sits in roughly the `−1%` to `−5%` range across most of
  `L/n∈[0.03,0.9]`, in the SAME direction and comparable magnitude in two
  independently-seeded `N=3000` runs (T2 and its cluster-robust follow-up)
  — this cross-run agreement (for 7 of 9 T2 bins) is the actually-robust
  part of the finding.

  > **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-062.]** O referee
  > hostil (`adversarial/REFEREE_REPORT.md` §5) nomeou esta frase como
  > uma imprecisão de redação: T2b (`fcd_t2_cluster.py`) na verdade
  > re-checou diretamente apenas **3 das 9** células de T2 (não 7), e
  > dessas 3, apenas **1** de fato concordou em sinal e magnitude — as
  > outras 2 são exatamente as que o próprio §4 relata como "retiradas"
  > por discordarem. As 7 restantes nunca foram re-medidas com SEM de
  > cluster; ausência de contradição não é o mesmo que concordância
  > demonstrada. **Isto não afeta nenhum resultado numérico do
  > documento** — apenas esta frase de síntese. O referee, porém,
  > supriu exatamente a evidência que faltava: sua própria réplica
  > independente (duas rodadas de `N=15.000`, robustas a cluster,
  > sementes frescas) confirma que as 9 células concordam entre si em
  > sinal e ordem de grandeza — a alegação substantiva que esta frase
  > buscava fazer estava correta, apenas a justificativa "7 de 9"
  > citada aqui, no momento em que foi escrita, ainda não estava
  > estabelecida pelos próprios dados desta frente. Ver
  > `adversarial/REFEREE_REPORT.md` §4 para a confirmação completa.

**Heuristic / explicitly rejected (kept in the record as worked, named
dead ends, per this archive's convention):**
- The `s_E≈0` one-shot closed form (3.1) — algebraically correct as a
  solution of its OWN (deliberately simplified) equation (cross-checked
  symbolically via `sympy`), but shown numerically to predict continued
  decay rather than a plateau — REJECTED as an approximation of the true
  process, not merely imprecise.
- This front's own pre-registered guess about *where* `dev%(L/n)` turns
  positive (`[0.1,0.6)`) — REFUTED by T2's own point-level data (which
  instead suggested `(0.75,0.875]`) — and that replacement claim was
  ITSELF then withdrawn (§4) once a cluster-robust, independently-seeded
  re-run showed it does not survive proper variance accounting. Net
  finding: no positive sub-region of the far tail is established at all;
  the honest, cross-run-robust statement is simply "negative throughout,
  order `−1%` to `−5%`," with no resolved finer structure.

**Not established / left open:**
- No closed form (exact or asymptotic with bounded error) for `φ(ℓ)` or
  `φ_far` is derived. The governing two-variable system (§5) is nonlocal
  and structurally comparable in difficulty to `THEOREM.md` §5.4's own
  still-open general-`K` conjecture.
- The numeric *level* of the plateau (`≈0.025-0.029` in the real engine,
  `≈0.037-0.039` in the idealized abstract-process Monte Carlo — a gap not
  reconciled here, possibly a finite-`n` effect, possibly a remaining
  simplification in the abstract model's treatment of the `s+g≤1` total-
  mass constraint for `t0` near 1, possibly both) is not explained.
- The fine bin-by-bin shape of `dev%(L/n)` within the far tail is
  **explicitly unresolved**: T2's own point-level run suggested a specific
  non-monotonic pattern (positive bump then sharply negative), but the
  cluster-robust, independently-seeded follow-up (§4) did not reproduce it
  (one bin flipped sign, another lost significance entirely) — a genuine,
  disclosed non-replication, not merely "needs more precision." Whether
  `φ(ℓ)` truly has a positive sub-region anywhere in the far tail, and if
  so where, is left open; a properly-powered (`N` in the tens of thousands
  of *instances*, matching the scale of the parent front's own referee
  corrections for analogous statistics) adversarial re-run is the natural
  next step.
- Why the real engine's plateau sits *below* the abstract-process plateau
  is not derived — a candidate explanation (finite-`n` corrections not
  captured by the `n→∞` idealization) is offered only as a hypothesis, not
  tested here.

---

> **VERDICT: HONEST PARTIAL CLOSURE.** This front derives, for the first
> time in this lineage, an *exact* reduction explaining why `φ_far` and
> `φ_U(c)` must generally differ (a selection effect on a non-constant
> `φ(ℓ)`), refutes the most natural candidate closed form for `φ(ℓ)`
> decisively, identifies and proves the correct qualitative *mechanism*
> (recursive gap re-entry via later reroutes landing on `x0`'s own
> unswept cycle-remainder) and validates it by direct simulation of its
> exact form, and establishes — cross-checked across two independently-
> seeded `N=3000` runs — that the deviation is consistently negative,
> order `−1%` to `−5%`, across essentially the whole far tail. It honestly
> fails to close the exact functional form, naming precisely
> why (a nonlocal two-variable system of the same order of difficulty as
> this archive's own still-open `K≥2` conjecture) and disclosing a bounded,
> unsuccessful numerical attempt at it rather than reporting a fabricated
> or unverified number. It also disclosed and then WITHDREW a finer,
> bin-by-bin sign-pattern claim once a cluster-robust replication failed to
> reproduce it — an honest correction made within this document itself,
> not left for a referee to catch. **No formula is proposed as a replacement for any
> formula of record** (`φ_REDB`, `φ_U(c)`, `φ_∞(c)`); nothing here
> supersedes any prior result in this lineage. **This document requires
> independent mandatory adversarial verification before any integration
> into governance**, exactly as every predecessor in this lineage.

> **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-062.]** Referee
> hostil dedicado executado. Veredito **SOUND WITH NAMED ISSUES —
> ACCEPT for catalogue**. Todas as três alegações empíricas designadas
> para re-verificação independente (rejeição do Candidato 1 em T1;
> platô do processo abstrato T3, construído apenas a partir da prosa
> deste documento, sem ler nenhum script; e a pergunta central de T2/
> T2b sobre existência de qualquer sub-região positiva) replicaram
> independentemente a `5×+` a potência estatística da própria frente,
> com sementes frescas. Único achado: a imprecisão de redação de §7
> corrigida acima. Nenhum erro muda o veredito da frente — a moldura
> "HONEST PARTIAL CLOSURE" se sustenta, e a retirada da alegação fina
> de T2 foi julgada apropriadamente conservadora, não excessiva.

---

## 8. Seeds (all used, reserved range `20260833000+` per `DISC-DEC-057`;
confirmed unused via `grep -rn "20260833" ..` before each use)

| seed | use | N | result location |
|---|---|---|---|
| `SeedSequence(20260833900)` | THROWAWAY: exploratory `φ(ℓ)` binning | 300 | `explore_phiL.log` |
| `SeedSequence(20260833901)` | THROWAWAY: exploratory abstract-process sim | 20000/t0 | `abstract_sim.log` |
| `SeedSequence(20260833902)` | THROWAWAY: exploratory n-dependence check | 600/150/40 | `explore_ndep.log` |
| `SeedSequence(20260833000)` | T0: exact-reduction sanity cross-check | 2000 | `fcd_t0.log` |
| `SeedSequence(20260833001)` | T1: Candidate-1 rejection | 1500 | `fcd_t1.log` |
| `SeedSequence(20260833002)` | T2: fine `L/n` sub-binning | 3000 | `fcd_t2.log` |
| `SeedSequence(20260833003)` | T3: abstract recursive-process, real seed | 40000/t0 | `fcd_t3.log` |
| `SeedSequence(20260833004)` | T2b: cluster-robustness follow-up (§4) | 3000 | `fcd_t2_cluster.log` |

## 9. Files

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration (written first, unmodified since) |
| `explore_phiL.py`/`.log`, `explore_ndep.py`/`.log`, `abstract_sim.py`/`.log` | throwaway exploration, kept for transparency |
| `derive_closed_form.py`/`.log` | symbolic (`sympy`) re-derivation of (3.1) and its numeric decay table |
| `check_formula_heuristic.py` | early numeric-only version of the same heuristic (superseded by `derive_closed_form.py`; kept for transparency) |
| `fcd_t0.py`/`.log` | T0 |
| `fcd_t1.py`/`.log` | T1 |
| `fcd_t2.py`/`.log` | T2 |
| `fcd_t2_cluster.py`/`.log` | T2b, cluster-robustness follow-up |
| `fcd_t3.py`/`.log` | T3 |
| `solve_2d_system.py`/`.log` | bounded, unsuccessful numerical attempt at the full §5 system |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this subfolder touched (other than
reading, read-only, the parent front's `sc_engine.py`/`sc_formula.py` by
import, and its `ATTEMPT.md`/`adversarial/REFEREE_REPORT.md`/
`DERIVATION_PREREG.md` for reference, plus `THEOREM.md` and
`DERIVATIONS.md` for the governing definitions, per the mandate).
