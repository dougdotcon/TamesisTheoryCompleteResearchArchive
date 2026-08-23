# DERIVATION_PREREG — closed-form attempt for the b=1 long-cycle deficit floor

**Wave 14, `DISC-DEC-057`, front (b) `FLOOR-CLOSED-FORM-ATTEMPT`.**
Written and saved BEFORE any real (non-throwaway) simulation of this front is
run — check this file's mtime against the `.log`/`.py` files in this
directory, all later. Target: derive a closed-form (exact or asymptotic) for
`φ_far := P(x0 cyclic | x0∈R^c, L(x0)>threshold)` at `b=1` (plain M-U), and
explain the sign/magnitude of the deficit vs `φ_U(c)` established by
`long_cycle_deficit_attempt/ATTEMPT.md` (`DISC-DEC-054/056`).

Exploratory work (THROWAWAY seeds `20260833900+`, disclosed in full below)
was used to build intuition and find/discard two wrong hypotheses before this
pre-registration — this is normal derivation process, not data-snooping,
since no number from the throwaway runs is reported as a final result below;
this document fixes what WILL be reported, and with what seeds, before any
of those seeds are drawn.

---

## 0. Exact setup (not itself requiring simulation — proved below)

At `b=1`, `sc_engine.build_R_mask` reduces to `R=seed_mask` exactly (T0 of
the parent front, re-confirmed by its referee). Fix `x0` (WLOG `x0=0` by
exchangeability). Let `L := L(x0)` be the length of `x0`'s `π`-cycle.

**Fact A (classical, exact).** For `π` uniform on `S_n` and any fixed point
`x0`, `P(L(x0)=ℓ) = 1/n` for `ℓ=1,…,n` — the cycle length containing a fixed
point of a uniform random permutation is *exactly* uniform on `{1,…,n}` (not
just asymptotically). Standard (e.g. via the "records"/Feller-coupling
construction of a uniform permutation's cycle containing a marked point:
each step "continues" or "closes back to x0" with probability proportional
to remaining mass, giving `P(L=ℓ)` = 1/n by direct product-telescoping).

**Fact B (immediate from Def. 1).** `L(x0) ⊥ ξ_{x0}` (whether `x0` is a
seed), since `π` and the seed indicators `ξ` are independent by construction.

**Corollary (exact reduction, PROVED, no simulation needed).** Define
`φ(ℓ) := P(x0 cyclic | ξ_{x0}=0, L(x0)=ℓ)`. Then for any `1≤threshold<n`:

`φ_far(threshold) = (1/(n−threshold)) · Σ_{ℓ=threshold+1}^{n} φ(ℓ)`.  (0.1)

This holds for every finite `n,c,threshold` — an exact identity, not an
approximation. It immediately explains **why there is any deviation at all**
between `φ_far` and `φ_U(c)`: `φ_U(c)` (via `H_q(t)=t²` in the master-formula
framework, `DERIVATIONS.md` §1) is the `n→∞` limit of the **unconditional**
average `(1/n)Σ_ℓ φ(ℓ)`, achieved by mixing over `L/n → Unif(0,1)`
(`T_0=1−e^{-E_0}~Unif(0,1)` in `THEOREM.md` Def. 3's construction, which we
verify below matches `L/n` in law). Restricting to `ℓ>threshold` is a
**selection effect** on this same mixture: `φ_far` and `φ_U(c)` are the
*same weighted-average machinery* evaluated over two different windows of
`ℓ`, and they agree only if `φ(ℓ)` happens to be constant in `ℓ`. This
Corollary is reported as PROVED (elementary, from Facts A+B); no simulation
is needed to establish it, though T0 below cross-checks it as a sanity check
on the engine.

## 1. Two candidate closed forms for `φ(ℓ)`, and what refutes/supports them
(exploratory finding, stated here for the record — NOT yet confirmed with
real seeds; T1/T2 below are the pre-registered confirmatory tests)

**Candidate 1 (REJECTED by throwaway exploration, seed `20260833900`,
`N=300`, `c=1000,n=65536` — see `explore_phiL.py` in this directory):**
`φ(ℓ) ≈ φ_∞(t0):=e^{-c t0²}` with `t0=ℓ/n`, obtained by literally
substituting `T_0=t0` into the master formula's integrand pointwise (a
plausible-looking but, per the analysis below, over-simplified reading of
`THEOREM.md` Def. 3). This predicts `φ(ℓ)→0` by `ℓ≈4000` (`t0≈0.06`) at the
target cell. The throwaway run instead shows `φ(ℓ)` **plateauing** around
0.023–0.03 for `ℓ` beyond ≈2000, all the way out to `ℓ=n` — flatly
inconsistent with Candidate 1's predicted decay to numerically zero. This
candidate is REJECTED (not merely imprecise); T1 below re-confirms this
rejection with real seeds, adequate power, and a pre-fixed criterion.

**Mechanism identified for the plateau (derivation, not yet a closed
form).** A reroute landing on the still-unswept remainder of `x0`'s own
`π`-cycle (the "gap") is a **guaranteed eventual success** (walking forward
from any point of `x0`'s cycle, via `π`, reaches `x0` before it can reach
any other already-visited point — proved in §2 below) *unless* interrupted
by yet another seed before reaching `x0`, in which case the process
recurses: a new destination (uniform over `[n]`) again has a chance of
re-entering the (now smaller) gap, or landing elsewhere, or killing. This is
a genuinely recursive structure (structurally analogous to the still-open
`K≥2` density problem, `THEOREM.md` §5.4). A "single re-entry, mass-free
generic retry" approximation gives a closed-form ODE solution (§3 below);
throwaway exploration shows this approximation is **not merely imprecise
but qualitatively wrong** (it predicts continued decay to 0 for large
`ℓ/n`, not a plateau) — so a naive one-shot treatment of the recursion is
insufficient; the true mechanism needs the full recursion, which is not
solved in closed form in this document (an honest open item, named
precisely in §5).

**Candidate 2 (exploratory, throwaway seed `20260833901`, abstract
recursive-process simulation, `explore/abstract_sim.py`):** direct Monte
Carlo of the exact (not mass-free-approximated) two-variable recursive
process (state `(s,g)`: `s`=total explored mass, `g`=remaining gap) DOES
reproduce a plateau, qualitatively matching the true engine — validating
the *mechanism* (recursive gap re-entry) even though no closed form for it
is derived. T2 below re-runs this with a real seed for the record.

## 2. Proof of the "guaranteed success" structural fact (used above, PROVED)

Let `x0`'s π-cycle be `y_0=x0, y_1=π(x0), …, y_{L-1}, y_L=y_0`. Suppose the
walk from `x0` (or from any later reroute) reaches some `y_j` (`0<j<L`) that
has never before been visited by `x0`'s trajectory. Since `f=π` off the
seed set, and `y_j` is confirmed fresh (not yet a member of `x0`'s
trajectory), continuing forward from `y_j` via `π` visits `y_{j+1},
y_{j+2},…` in the FIXED cyclic order established by `π` — the *only* way
this forward walk can reach an already-visited point before reaching `x0`
would require passing `x0` (`y_0`) first, since `x0`'s trajectory's
already-visited points (from earlier legs) all lie in the "downstream" arc
`(y_0, y_1, …]` that any forward walk from `y_j` (`j>0`) reaches **only
after** passing through `y_0` (going forward around the cycle, `y_0` is
encountered before any of `x0`'s own trajectory's earlier-visited
territory, because that territory begins immediately after `y_0`). Hence:
reaching any fresh point of `x0`'s own cycle, and walking forward
unintercepted, reaches `x0` **before** it can reach any other
already-visited point — i.e. it is cyclic-for-`x0` unless intercepted by a
NEW seed first. This is an exact (not asymptotic, not mean-field) fact
about the finite-n structure, used as the basis of the recursive mechanism.

## 3. The single-re-entry ("s_E≈0") closed-form candidate — DERIVED, then
shown wrong in a NAMED way

Modeling `(s,g)` with `s=t0−g` exactly (i.e. neglecting mass consumed by
"elsewhere" excursions before they resolve into kill/gap-hit/retry) gives,
via a Laplace-transform solution of the resulting Volterra equation:

`Φ(g) = [s₁e^{s₁g} − s₂e^{s₂g}]/(s₁−s₂)`,  `s_{1,2}=(−c±√(c²+4c/t0))/2`  (3.1)

with `φ_far`'s candidate pointwise value `Φ(t0)`. Full derivation in
`derive_closed_form.py` (symbolic, sympy, exact). This is reported as a
**named, explicit HEURISTIC** — throwaway exploration (§1) shows it predicts
continued decay toward 0 for large `t0`, not the observed plateau, so it is
**not** claimed as the answer; it is kept in the write-up as a worked
example of why the naive one-shot treatment fails (the "stay in generic
exploration costs no mass" assumption turns out to matter qualitatively,
not just quantitatively).

## 4. Planned CONFIRMATORY tests (fresh seeds, fixed criteria, run AFTER this
file is saved)

**T0 — sanity check of the exact reduction (0.1).** At the target cell
(`c=1000,n=65536,b=1`), measure `φ_far(threshold=2000)` two independent
ways in the SAME run: (a) directly (condition on `L>2000`), and (b) via
fine `L`-binning + the weighted average (0.1). **Criterion:** the two must
agree to within `2×`SEM of their difference (near-tautological, but confirms
no bug in the binning code). `N=2000` instances, all `n` points used per
instance (exchangeability).

**T1 — re-confirm rejection of Candidate 1 (`φ(ℓ)≈e^{-c(ℓ/n)²}`), with real
seed and enough power.** Same cell, sub-bin edges `[1,50,200,500,1000,2000,
4000,8000,16384,32768,65536]` (as in the throwaway explore run, but now with
`N=1500` and a real seed). **Criterion:** REJECTED if, for at least 3 of the
bins with `ℓ≥4000`, the measured `φ̂(bin)` exceeds the Candidate-1 point
prediction (evaluated at the bin midpoint) by `≥10σ` (using the bin's own
SEM) — a very conservative bar given the throwaway run already showed
Candidate 1 predicting numerically 0 against measured values around 0.025.

**T2 — characterize `dev%(ℓ/n)` non-monotonicity across the WHOLE range
(new, not just re-confirming a throwaway finding — this is the primary new
empirical contribution of this front).** Same cell (`c=1000,n=65536,b=1`),
finer bins covering `ℓ/n` from ~0.03 to 1: edges
`[2000,4000,8000,16384,24576,32768,40960,49152,57344,65536]`. `N=3000`
instances. **Report:** `dev%(bin):=100(φ̂(bin)/φ_U(c)−1)` and its `z`-score
per bin (using the bin's own binomial SEM against `φ_U(c)`, exact `φ_U`
computed via `scipy.integrate.quad` cross-check). **Pre-registered claim
being tested:** dev% is significantly POSITIVE for at least one bin with
`ℓ/n∈[0.1,0.6]` (`z≥+3`) AND significantly NEGATIVE for the last bin
(`ℓ/n∈(0.875,1]`, `z≤−3`) — i.e. a genuine sign change across the far tail,
not a uniformly negative deficit. If this pattern does NOT hold (e.g. dev%
is uniformly negative, or uniformly positive, or not significant anywhere),
that is reported as a refutation of the "sign-change" finding, honestly.

**T3 — abstract recursive-process mechanism validation, real seed.** Same
as the throwaway `abstract_sim.py` run, `c=1000`, 12 values of `t0` spanning
`1e-4` to `0.9`, `N=40000` per `t0`. **Report:** whether `φ_abstract(t0)`
plateaus (criterion: ratio of `φ_abstract` at the two largest `t0` values to
the value at `t0=0.09` stays within `[0.5,2]×`, i.e. does not continue
decaying by an order of magnitude, unlike Candidate 1) — a qualitative,
pre-registered check of the plateau claim using the fully-general (not
mass-free-approximated) abstract simulation.

**No functional form or bin edges are chosen after seeing T0–T3 output.**
If T2's specific sign-change pattern is not confirmed, that is reported
honestly as non-closure on the finer characterization (while T0/T1's
findings — the exact reduction identity and Candidate 1's rejection — stand
on their own regardless of T2's outcome).

## 5. Honest scope statement (fixed now)

This front's SUCCESS CRITERION, per the mandate, allows "a partial/heuristic
derivation with clearly labeled status if a full derivation isn't
reachable." Given the difficulty already encountered (the exact recursive
`(s,g)` system is a genuinely coupled, nonlocal 2-variable problem —
`∂Φ/∂s−∂Φ/∂g = c[Φ−W]`, `∂Ψ/∂s=c[Ψ−W]`, `W(s,g)=g·Avg_g[Φ(s,·)]+(1−s−g)Ψ`,
with `Avg_g[Φ(s,·)]:=(1/g)∫₀^gΦ(s,g')dg'` — structurally resembling the
archive's own still-CONJECTURED `K≥2` density, `THEOREM.md` §5.4), this
front's PRE-COMMITTED plan is: derive & report the exact reduction (0.1) as
PROVED; run T0–T3 as designed; and if the full `(s,g)` system remains
unsolved after a bounded further effort (attempted in `solve_2d_system.py`,
result reported either way), report that as a named, precise open item —
NOT force a wrong or unverified closed form into the record. This is
pre-committed now, before seeing T0–T3's results.

---

## 6. Seeds (reserved range `20260833000+` per `DISC-DEC-057`; confirmed
unused elsewhere by `grep -rn "20260833" ..` over the whole archive before
this file was saved — only this ledger's own reservation line matched)

| seed | use | N |
|---|---|---|
| `SeedSequence(20260833900)` | THROWAWAY: exploratory `φ(ℓ)` binning, motivated §1 Candidate 1 rejection (not a reported final number) | 300 |
| `SeedSequence(20260833901)` | THROWAWAY: exploratory abstract-process sim, motivated §1 Candidate 2 | 20000/t0 |
| `SeedSequence(20260833902)` | THROWAWAY: exploratory n-dependence check (3 values of n) | 600/150/40 |
| `SeedSequence(20260833000)` | T0: exact-reduction sanity cross-check | 2000 |
| `SeedSequence(20260833001)` | T1: Candidate-1 rejection, real seed | 1500 |
| `SeedSequence(20260833002)` | T2: fine `ℓ/n` sub-binning, sign-change characterization | 3000 |
| `SeedSequence(20260833003)` | T3: abstract recursive-process, real seed | 40000/t0 |

No `20260834000+` (referee-reserved range) used by this front.

---

## 7. Files planned

| file | role |
|---|---|
| `DERIVATION_PREREG.md` | this document |
| `explore_phiL.py`, `explore_ndep.py`, `abstract_sim.py` | throwaway exploration (kept for transparency; copied into this directory from the session scratchpad) |
| `derive_closed_form.py` | symbolic (sympy, exact) derivation of (3.1) |
| `fcd_t0.py`/`.log`, `fcd_t1.py`/`.log`, `fcd_t2.py`/`.log`, `fcd_t3.py`/`.log` | T0–T3 confirmatory runs |
| `solve_2d_system.py`/`.log` | bounded attempt at the full `(s,g)` system; result reported either way |
| `ATTEMPT.md` | the write-up |

No git commit made by this front. Nothing outside this subfolder is touched
(other than reading, read-only, the parent front's `sc_engine.py`/
`sc_formula.py` by import, and its `ATTEMPT.md`/`adversarial/
REFEREE_REPORT.md`, `DERIVATION_PREREG.md` for reference, per the mandate's
explicit permission).
