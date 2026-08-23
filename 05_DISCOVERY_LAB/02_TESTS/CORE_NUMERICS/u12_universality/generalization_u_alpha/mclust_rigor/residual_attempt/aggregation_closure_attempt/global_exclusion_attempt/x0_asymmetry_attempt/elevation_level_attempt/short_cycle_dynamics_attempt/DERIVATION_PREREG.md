# DERIVATION_PREREG — short-π-cycle dynamics correction to φ_REDB

**Wave 12, `DISC-DEC-051`, front (b) `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT`.**
Written and saved BEFORE any simulation of this front is run (no `.json`,
`.log`, or Monte-Carlo output exists in this subfolder yet — check file
mtimes). Target: the residual the referee's `adversarial/REFEREE_REPORT.md`
§11 left after `φ_REDB` and after the failed naive fix `φ_REDX`, concentrated
in `b=100, c=1000, n=65536` (ρ=0.785, z≈−10 in the formula-free reduction
test).

---

## 1. The mechanism, re-derived from the prose sources (no `.py` read)

Read in full: `DECISION_LEDGER.yaml` `DISC-DEC-051`; `PROOF_DEPENDENCY_MAP.md`
"Árvore B"; `elevation_level_attempt/ATTEMPT.md` (all 14 sections, all dated
correction blockquotes); `elevation_level_attempt/adversarial/REFEREE_REPORT.md`
(all 12 sections); `generalization_u_alpha/DERIVATIONS.md` §0–3.6, §6;
`mclust_rigor/DERIVATION_MCLUST_FIXED.md` §0–6 (the last two are prose
derivation documents, not scripts of the target front or its referee — reading
them is required to pin down the mechanism precisely and is not excluded by
the independence rule, which excludes only `.py` files under
`elevation_level_attempt/` and `elevation_level_attempt/adversarial/`).

**Mechanism, reconciled.** `n` points, `π` a uniform random permutation. Each
point is an i.i.d. seed with probability `p = c/n`. For each seed `s`, the
**run** is the full forward orbit of `b` points `{s, π(s), π²(s), …,
π^{b−1}(s)}` (confirmed against `DERIVATION_MCLUST_FIXED.md` §1, "o bloco de s
é {s, π(s), …, π^{b−1}(s)}", and against the internal consistency of
`elevation_level_attempt/ATTEMPT.md` §2's own `U_rem`/`A_rem` definitions and
the identity `ρ = 1−(1−c/n)^b` it reuses unchanged from wave 4 — a block that
excluded `s` itself would give `ρ = 1−(1−c/n)^{b−1}`, not `1−(1−c/n)^b`; the
reconciliation is spelled out in full in §1.1 below). `R = ∪_s block(s)`.
Every point of `R` — seed or interior/shadowed member, no distinction — is
assigned an i.i.d. `Uniform([n])` destination `f(x)`, drawn once and fixed.
Outside `R`, `f = π`. `φ := E[(1/n)·|{x ∈ [n] : x lies on a cycle of f}|]`.

### 1.1 Reconciling the two block conventions

`elevation_level_attempt/ATTEMPT.md` §2 writes the run as "reveal `π(s),
π²(s), …, π^{b−1}(s)`" (b−1 forward queries, not literally listing `s`), and
defines `A_rem = [n]\{π^j(s): 0≤j≤b−2}`, `U_rem = [n]\{π^j(s): 1≤j≤b−1}`. Read
literally as "`R` = the images set `{π^j(s): 1≤j≤b−1}`" this would make
`U_rem ≡ R^c` identically, which cannot be squared with the referee's own
audited fact `R^c ⊆ U_rem` (§3.1 of the referee report, "always", 0
violations) unless the inclusion is generically strict — and it is: `R` (the
set the *walk* excludes) must additionally contain the seed `s` itself,
because the seed set `Σ` is revealed in step 1 before any forward query and a
seed can never be treated as an ordinary walkable point once marked (this is
also the only reading under which `I ⊆ R` — `I = A_rem`'s excluded set,
`{π^j(s): 0≤j≤b−2}`, which literally contains `s` at `j=0` — holds, as the
referee's §3.1 uses it). So `R = {s} ∪ {π^j(s): 1≤j≤b−1} = block(s)`, the full
`b`-point run, matching `DERIVATION_MCLUST_FIXED.md` exactly; `ATTEMPT.md`'s
phrasing is shorthand that omits the (already-marked) seed from the list of
*new* forward queries, not a different mechanism. This reading is checked
against **three independent internal facts** of the two primary documents
(the `ρ = 1−(1−c/n)^b` identity, `I ⊆ R`, and `R^c ⊆ U_rem` "always"), all of
which are satisfied simultaneously only under this reading, and it is verified
again below by direct simulation (`sc_engine.py selftest`) before anything
else is trusted.

### 1.2 Exact facts about cycle length (re-derived, not copied)

For a uniform random permutation of `[n]`, the cycle through a fixed point has
length `L` with `P(L=ℓ) = 1/n` for every `ℓ = 1,…,n` — **exactly** (this is the
classical fact the referee's §3.2 already cites and I re-derive independently
in §2 below by the standard argument: label the cycle containing a fixed
point `y` by revealing `π(y), π²(y), …` one step at a time; at each step the
"close now" probability is `1/(remaining unrevealed points)`, and integrating
that hazard over the `n` equally-likely stopping positions gives the uniform
law — this is the same sequential-exposure technique the whole lineage already
relies on for `R`'s own densities). A corollary used heavily below: the
**expected number of points lying on cycles of length ≤ K** is exactly `K`,
for any `1 ≤ K ≤ n` (sum `Σ_{L=1}^{K} L·P(a given cycle has length L)`, or
more directly `Σ_{L=1}^K n·P(y on an L-cycle)/n = Σ_{L=1}^K 1 = K`, since there
are `n/L · (1/n) = 1/L`-weighted... — cleanest form: `E[#{y: L(y)≤K}] =
Σ_y P(L(y)≤K) = n·(K/n) = K`).

### 1.3 The dynamical fact this front targets

**Claim, mechanism-level, to be checked deterministically before any Monte
Carlo (§4 below).** If the π-cycle through a seed `s` has length `L ≤ b`, the
run `block(s) = {s,π(s),…,π^{b−1}(s)}` — a set of `b` terms taken mod `L` —
covers **every** point of the cycle, `s` included (since `π^L(s)=s` and
`L≤b−1` puts the index `L` inside the query range, or `L=b` exactly covers all
`b=L` points with no repeats). Hence:

* **If a length-`L≤b` cycle is untouched by every seed** (probability
  `(1−c/n)^L`, since the `L` points' seed-marks are i.i.d. Bernoulli(p),
  independent of `π`): **no point of it is ever in `R`**, `f` restricted to it
  equals `π` restricted to it, and it is **exactly** and **deterministically**
  a cycle of `f`. Every point on it is cyclic with probability **exactly 1** —
  not via any exploration process, not via `φ_U` of anything.
* **If a length-`L≤b` cycle carries at least one seed** (probability
  `1−(1−c/n)^L`), **every** point of it — including points that are not
  themselves the seed — is pulled into `R`, because the seed's `b`-point run
  already covers the whole cycle. **Every run-start test fails on this
  cycle**: a run start is `p∈R` with `π^{-1}(p)∉R`, and on a fully-absorbed
  short cycle `π^{-1}(p)` is always another point of the same (fully absorbed)
  cycle, hence always in `R`. **The cycle is permanently unreachable by any
  normal π-step, from anywhere** — it can only be entered by a reroute
  destination `D(·)` landing on it directly (probability `L/n` per reroute
  event), exactly as the mandate's Background section states.

This is qualitatively different from a cycle of length `L > b`: there, a
seed's run covers only `b` of the `L` points (a proper sub-arc), the rest of
the cycle remains walkable, and only isolated sparse blocks are excluded —
the regime the existing `φ_RED`/`φ_REDB` mean-field reduction (`ATTEMPT.md`
§4) is built for. `φ_U(c'')`, the piece of `φ_REDB` that stands in for
`φ(cyclic | x₀∈R^c)`, is **itself** `M-CLUST(1)`'s value — i.e. it is the
answer for a mechanism whose *own* short cycles (`b=1`) are **not**
all-or-nothing: a seed elsewhere on a short `π''`-cycle of the *reduced* M-U
process does not swallow the whole cycle (blocks are single points), so a
generic point on a short `π''`-cycle in M-U still undergoes genuine,
gradual exploration and is cyclic with probability strictly less than 1 in
general. Substituting `φ_U(c'')` for M-CLUST(b)'s conditional therefore
imports **M-U's own (gradual) short-cycle handling** in place of
**M-CLUST(b)'s (all-or-nothing) short-cycle handling** — a mismatch specific
to short cycles, invisible to any correction that only touches mean
densities (which is exactly why the referee's `φ_REDX`, built from exact
mean densities alone, "repairs the worst extreme cell but overshoots two
others" — §11 of the referee report — and why the referee explicitly named
this as the missing ingredient).

---

## 2. Candidate correction — `φ_REDC`

### 2.1 The exact short-cycle partition of `x₀ ∈ R^c`

Define, exactly (both from §1.2/§1.3, no approximation):

```
S_untouched(b,c,n) = (1/n) Σ_{L=1}^{b} (1−c/n)^L          [prob mass: x0 on an
                                                             untouched cycle
                                                             length ≤ b]
P(x0 ∈ R^c)        = (1/n) [ Σ_{L=1}^{b}(1−c/n)^L + (n−b)(1−c/n)^b ]
                                                            [exact aggregate,
                                                             re-derived §3.2-
                                                             style, independent
                                                             re-derivation in
                                                             §2 of sc_formula.py
                                                             self-check]
w_short(b,c,n)     = S_untouched / P(x0∈R^c)               [conditional weight
                                                             of the short-
                                                             untouched bucket
                                                             inside R^c]
```

`(1−p)^b = 1−ρ` exactly, so `P(x0∈R^c) → (1−ρ)` recovers the aggregate used
throughout the lineage as `b,c/n → 0` (the `S_untouched` term is
`O(b·p) = O(bc/n) → 0` relative to it).

### 2.2 The candidate formula

```
φ_cond,C := w_short · 1  +  (1 − w_short) · φ_U(c'')          (2.1)

φ_REDC := (1 − P(x0∈R^c)) · [ ... same eps machinery as φ_REDB, ρ→P(x0∈R^c)-
          exact-density substituted per referee §3.2 ...]
        + P(x0∈R^c) · φ_cond,C                                 (2.2)
```

i.e. `φ_REDC` takes `φ_REDB` (which already carries the referee's `c''`
correction) and (a) replaces the mean-density `ρ`/`1−ρ` prefactors by the
*exact* combinatorial `P(x0∈R^c)` wherever they gate the conditional-vs-`eps`
split (the referee's own tested-and-separately-insufficient `φ_REDX`
ingredient), **and** (b) replaces the flat `φ_U(c'')` conditional by the
mixture (2.1) that gives probability-1 weight to the short-untouched bucket.
Both pieces are derived, not fitted; neither has a free parameter. The
`eps` channel (`x₀∈R`) is left as `φ_REDB`'s, unmodified — §2.3 names this as
a known, deliberately-not-modeled gap.

**Sized in advance, before simulating anything** (`sc_formula.py`, run below):
at `b=100,c=1000,n=65536` (the target cell), `w_short ≈ 0.0036` (0.36%
of the `R^c` population). This is *small*; the correction (2.1) alone shifts
`φ_cond,C` **upward** relative to `φ_U(c'')` by roughly `w_short·(1−φ_U(c''))
≈ 0.0034` in absolute terms — on the order of the discrepancy's *size* but the
**opposite sign** from what the referee's z=−10.86 needs (measured M-CLUST is
*below* `φ_U(c'')`, not above). This is flagged explicitly, in writing, before
any simulation: **I do not know, going in, whether (2.1)–(2.2) will reduce or
increase the residual on the target cell.** The hand-derivation above gives a
mechanistically well-motivated correction but not a confident sign prediction,
because `φ_U(c'')`'s own implicit handling of short cycles (as an M-U
process) is not analytically decomposed here — only measured, in §3 below.

### 2.3 What is NOT modeled here (named in advance)

* The `eps` channel (`x₀∈R`) is not re-derived for short-cycle absorption.
  Short-absorbed-cycle mass is `≈0.075%` of `n` at the target cell (`sc_formula.py`
  §3), i.e. `≈0.10%` of `R` itself — smaller than the `R^c`-side effect, and not
  pursued given the effort budget of this front.
* Any effect of reroute chains landing preferentially on short absorbed
  cycles (vs. "normal" block interiors) during the *long-cycle* exploration is
  not modeled; §1.3 argues informally that `f`'s rule is identical
  (`Uniform([n])`) regardless of why a point is in `R`, so this is not
  expected to matter, but it is not proved.
* Possible early self-closure of a *spawned arc* that happens to land inside
  a short untouched cycle (an arc that would close on itself after `L≤b`
  steps rather than persisting as competing hazard to `t=1`) is discussed
  qualitatively in the derivation notes but **not** incorporated into (2.1)–
  (2.2) — it requires re-deriving the master formula's arc-competition term,
  which is out of scope for this front's budget. Named as an open item.

---

## 3. Planned tests, IN ORDER, with refutation criteria fixed now

**T0 — mechanism self-consistency (deterministic + MC, must pass before
anything else is trusted).** `sc_engine.py selftest`: (a) `ρ_measured` vs
`1−(1−c/n)^b` on ≥8 cells; (b) `R^c ⊆ U_rem` — 0 violations required, checked
on every simulated instance; (c) a fully-untouched cycle of length `≤ b` is
**always** exactly a cycle of `f` — checked deterministically on every
instance that contains one; (d) a fully-touched cycle of length `≤ b` has
**zero** run starts on it — checked deterministically. **Refutation: any
violation of (b)/(c)/(d) invalidates the mechanism re-derivation and this
front stops to fix it before proceeding.**

**T1 — the diagnostic split (the load-bearing empirical measurement).**
Directly measure, on the target cell (`b=100,c=1000,n=65536`) and 2–3
comparison cells, `φ(cyclic | x₀∈R^c, x₀ on an untouched cycle length≤b)`
(must measure `1.000` to within Monte-Carlo error — a hard sanity check, not
a free result) and `φ(cyclic | x₀∈R^c, x₀ on a long cycle or a touched-but-
not-absorbing-x₀ scenario)` **separately**, compared to `φ_U(c'')`. This is
run and reported **regardless of what it shows** — including if it refutes
§2's sign guess — because the pre-registered purpose of T1 is to determine
the sign and magnitude of the long-cycle-population's own deviation from
`φ_U(c'')`, which (2.1)–(2.2) does not model and cannot get right by
construction if `φ_long ≠ φ_U(c'')`.

**T2 — formula-free reduction test, own engine, 6-cell grid.** The referee's
own pre-registered 6 cells (`b,c,n`): `(50,400,65536)`, `(100,400,65536)`,
`(100,600,65536)`, `(200,150,65536)`, `(400,100,65536)`,
`(100,1000,65536)` — the last being the target cell. For each: measure
`φ(cyclic|x₀∉R)` directly by simulation (own engine, no formula), and score
it against `φ_U(c')` (superseded), `φ_U(c'')` (`φ_REDB`'s value), and
`φ_cond,C` (2.1) (this front's candidate). **Refutation criterion, fixed now:
this front's correction is judged a SUCCESS only if it reduces |z| (or |dev%|)
on the target cell `(100,1000,65536)` relative to `φ_U(c'')` by at least 30%
**without** increasing |z| on any of the other 5 cells beyond
max(2×its φ_REDB |z|, 2.5)** — i.e. it must not reproduce the referee's
`φ_REDX` failure mode (fixed the worst cell, broke two others). If T1 shows
the long-cycle population itself deviates from `φ_U(c'')` by a comparable or
larger amount than the short-cycle mixture correction, that is reported as
the dominant, NOT-modeled effect, and (2.1)–(2.2) is reported as insufficient
by construction — an honest non-closure, not silently patched by fitting a
further term to T2's own numbers.

**T3 — full `φ` on the 6-cell grid** (not just the conditional), using the
`eps` channel unmodified from `φ_REDB`, to see whether the conditional-side
correction (whatever its sign) is large enough to matter once diluted by
`ρ·eps`.

**No functional form is chosen or adjusted after T1/T2 are run.** If (2.1)–
(2.2) is refuted by T1/T2, this document is not rewritten to fit a new
formula to the same numbers; instead, whatever T1 reveals about the sign and
size of the long-cycle-only deviation is reported as a diagnostic finding
(honest non-closure), per the mandate's explicit instruction that this is an
acceptable and valuable outcome.

---

## 4. Seeds (fresh, `SeedSequence` from 20260825900 upward, none reused
anywhere in the archive — checked by `grep -r "202608" ..` over the archive
before assignment)

| seed | use |
|---|---|
| `SeedSequence(20260825900)` | `sc_engine.py selftest` (T0) |
| `SeedSequence(20260825901–908)` | T1 diagnostic split, up to 8 cells |
| `SeedSequence(20260825910–915)` | T2 reduction test, 6 cells |
| `SeedSequence(20260825920–925)` | T3 full-φ test, same 6 cells |
| `SeedSequence(20260825930+)` | any follow-up/exploratory runs, labeled
  post-hoc if used |

---

## 5. Files planned

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | this document |
| `sc_engine.py` | own M-CLUST(b) engine: π, Σ, R (full b-point run, §1.1),
  `f`, cycle detection (in-degree peeling), π-cycle-length utility. Written
  from scratch from the prose mechanism above; does not import any `.py`
  under `elevation_level_attempt/` or its `adversarial/` |
| `sc_formula.py` | `φ_U`, `T_U`, `H`, exact short-cycle combinatorics (§2.1),
  `φ_REDB` (reused/re-transcribed, labeled), `φ_REDC` (this front's candidate,
  §2.2) |
| `sc_diagnostic.py` | T1 |
| `sc_reduction.py` | T2 |
| `sc_full.py` | T3 |
| `ATTEMPT.md` | the write-up |

No git commit. Nothing outside this subfolder is touched.
