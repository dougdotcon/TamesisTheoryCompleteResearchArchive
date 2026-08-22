# DERIVATIONS — the U_α family (front C, wave 3)

**Status labels used throughout: DERIVED (probabilistic argument at
research-draft rigor, each step verifiable), HEURISTIC (order-of-
magnitude / annealed argument, labeled), CONJECTURED. Written after
METHODOLOGY_NOTE.md and BEFORE any simulation of this front
(timestamps verifiable). Inherits the exploration process of
`../limit_characterization/DERIVATION.md` §1–2 (adversarially
confirmed), including its honest caveat: the finite-n → continuum
passage is a standard rates-convergence argument controlled
empirically, not formalized at full rigor. Everything below is exact
GIVEN that continuum description, unless labeled otherwise.**

## 0. Inherited setup

Exploration of the f-orbit of a typical point x₀, parametrized by
traversed mass t ∈ [0,1): π-closure into any of the current arc starts
at hazard 1/(1−t) per arc start (uniform among them); x₀ is cyclic iff
the first terminal event is π-closure into x₀ itself. Reroute events
along fresh π-path at rate c per unit mass (for mechanisms marking
each point independently w.p. c/n).

## 1. Master class M-q and master formula [DERIVED]

**Class M-q** (defined at the level of the continuum exploration
process): reroute events at rate c; an event at time s **kills** (jump
into visited mass; terminal, x₀ non-cyclic a.s.) with probability
q(s), and otherwise lands on fresh mass and **starts a new arc**
(adding closure hazard 1/(1−r) for r ∈ [s, t]). q: [0,1) → [0,1]
measurable.

Exactly as in wave 2 §3 (Poisson PGFL, conditioning on reroute times):
the per-event factor is

F(s) = (1−q(s)) · exp(−∫ₛᵗ dr/(1−r)) = (1−q(s)) · (1−t)/(1−s),

the base (x₀'s own closure clock) contributes (1−t), and

E[S(t)] = (1−t) · exp(−c ∫₀ᵗ (1 − F(s)) ds) = (1−t) e^{−c H_q(t)},

**H_q(t) = t − (1−t) ∫₀ᵗ (1−q(s))/(1−s) ds.**            (1.1)

Substituting into φ = ∫₀¹ E[S(t)] dt/(1−t):

**φ_q(c) = ∫₀¹ exp(−c H_q(t)) dt.**                       (1.2)

Checks: q(s) = s ⇒ H = t − (1−t)t = t² (wave-2 result recovered);
q ≡ 1 ⇒ H = t; q ≡ 0 ⇒ H = t + (1−t)ln(1−t); H_q(0)=0, H_q(1⁻)=1;
H_q is pointwise nondecreasing in q (more killing ⇒ smaller φ). ✓

## 2. Exponent law, floor and ceiling [DERIVED]

Small-t expansion of (1.1) with q(s) = a s^β (1+o(1)), a > 0, β ≥ 0
(and the convention "q ≡ o(s^β) for all β" = the q≡0 boundary):
using 1/(1−s) = 1 + s + O(s²) and Q(t) = ∫₀ᵗ q = a t^{β+1}/(β+1)(1+o(1)),

**H_q(t) = t²/2 + (1−t)Q(t) + t³/6 + … = t²/2 + a t^{β+1}/(β+1) + h.o.**  (2.1)

The **t²/2 term is mechanism-independent**: it is the *crowding* cost
of the arc starts created by surviving reroutes (each survivor is a new
closure target competing with x₀; even a never-killing mechanism pays
it). This is the term the naive heuristic "kill ~ s^β ⇒
exp(−c t^{β+1}/(β+1))" misses.

Laplace/Watson at t = 0⁺ applied to (1.2):

- **β < 1:** H ~ a t^{β+1}/(β+1) ⇒
  φ_q(c) ~ Γ(1 + 1/(β+1)) · [(β+1)/(a c)]^{1/(β+1)}, **α = 1/(β+1) ∈ (1/2, 1]**.
  In particular β = 0 (an atom of kill probability at s = 0⁺):
  φ ~ 1/(a c), **α = 1**.
- **β = 1:** H ~ (1+a) t²/2 ⇒ φ ~ (1/2)√(2π/((1+a)c)), **α = 1/2**;
  a = 1 gives (√π/2) c^{−1/2}, the u12 value. ✓
- **β > 1 (incl. q ≡ 0):** H ~ t²/2 ⇒ φ ~ √(π/(2c)), **α = 1/2**,
  coefficient √(π/2) ≈ 1.2533.

**Exponent law: α = 1/(1 + min(β, 1)).**                   (2.2)

**Floor/ceiling theorem (within class M-q, given the continuum
description):** 0 ≤ q ≤ 1 gives H_{q≡0} ≤ H_q ≤ H_{q≡1} pointwise, so

(1−e^{−c})/c ≤ φ_q(c) ≤ ∫₀¹ e^{−c(t+(1−t)ln(1−t))} dt ~ √(π/(2c)),

hence **α ∈ [1/2, 1] for the entire class**: no single-point
redirection mechanism (rate c, one arc start per surviving event) can
decay slower than c^{−1/2} or faster than c^{−1}. The exponent 1/2 is
the *attainable floor*, protected by two independent quadratic
channels: linear-in-mass kill probability (β = 1) AND arc-start
crowding — either one alone forces t², hence α = 1/2. To leave the
class upward (α = 1) a mechanism needs an ATOM of kill probability at
age 0⁺, i.e. it must be able to hit the *recent past* of the orbit
with probability bounded away from 0 — a structure-aware backtracking
ingredient. α < 1/2 is impossible in the class. Corrections to (2.2)
for a general mechanism require mapping it into M-q (done case by case
in §3; M-INTRA falls OUTSIDE the class and is handled separately).

## 3. Mechanisms

### 3.1 M-U (original) [DERIVED, wave 2]

Uniform destination: kill prob = visited mass ⇒ q(s) = s (a = β = 1).
φ = ∫₀¹ e^{−ct²} dt, tail (√π/2)c^{−1/2}, α = 1/2.

**Exchangeability lemma [DERIVED, elementary]:** if destinations D_i
are i.i.d. across rerouted points, independent of (π, R), drawn from a
FIXED distribution ν on [n] whose definition does not depend on the
labels (ν invariant under relabeling of [n]), then ν is uniform and
the mechanism is *identical in law* to M-U. Hence the whole
structure-blind family collapses to U_{1/2} trivially — deviations
from α = 1/2 require destinations that read the structure (π, R, or
shared randomness across reroutes). (Remark, not pursued: shared
randomness alone can also break it — e.g. all reroutes jumping to one
common uniform point X makes every event after the first a kill,
an α = 1-type mechanism. Stated without derivation; not simulated.)

### 3.2 M-SELF (D_i = i) [DERIVED, two independent routes]

Finite-n route: a rerouted point is a fixed point of f (itself
cyclic); every other point of a cycle containing ≥1 reroute feeds into
that fixed point and is non-cyclic. Cyclic mass = reroute-free cycle
mass + |R|/n → E[Σ L_i e^{−cL_i}] = (1−e^{−c})/c (size-biased PD(1),
wave-2 §5; numerically verified as wave-2 T4 and by the wave-2
adversary). Exploration route: q ≡ 1 ⇒ φ = ∫₀¹e^{−ct}dt = (1−e^{−c})/c. ✓
Tail 1/c, **α = 1** (a = 1, β = 0). Not re-simulated (already verified
via the free-mass component).

### 3.3 M-MIX(p) [DERIVED]

q(s) = p + (1−p)s ⇒ H(t) = p t + (1−p) t², so

**φ_p(c) = ∫₀¹ e^{−c(pt + (1−p)t²)} dt**                  (3.1)

(erf closed form exists by completing the square; quadrature values in
`predictions.json`). Tail: φ ~ 1/(pc), **α = 1 for every p > 0** —
an arbitrarily small atom of backtracking destroys α = 1/2.
Crossover: the α = 1/2 behaviour survives for c ≪ (1−p)/p² and bends
to α = 1 beyond (relevant caution: finite-c slope estimates can
misclassify a crossover mechanism). K=1 exact (size-biased L ~ U(0,1),
independent of the master formula): loss = p·L + (1−p)(L − L²/2) ⇒
φ₁ = 1 − p/2 − (1−p)/3; **p = 1/2: φ₁ = 7/12**. Consistency with
(3.1): −dφ_p/dc|₀ = ∫₀¹(pt+(1−p)t²)dt = p/2 + (1−p)/3 ✓.

### 3.4 M-PREV (D_i = π^{−1}(i)) [DERIVED, two independent routes]

Finite-n route: a single reroute at i creates the 2-cycle
{i, π^{−1}(i)} (f(i) = π^{−1}(i), f(π^{−1}(i)) = π(π^{−1}(i)) = i when
π^{−1}(i) ∉ R); every other point of the cycle feeds into it. Adjacent
rerouted pairs occur at O(c²/n) density (negligible). Cyclic mass =
reroute-free cycles + 2|R∩·|/n → **(1−e^{−c})/c**, same limit as
M-SELF via different geometry. Exploration route: at a rerouted point
w of arc age > 0, the destination π^{−1}(w) is the point visited one
step earlier ⇒ kill w.p. 1 (terminal 2-cycle ∌ x₀ up to O(1/n) —
x₀ ∈ {w, π^{−1}(w)} only if the very first step hit a reroute) ⇒
q ≡ 1 ⇒ (1−e^{−c})/c ✓. **α = 1.** K=1 exact: φ₁ = 1 − E[L] = **1/2**.

### 3.5 M-CLUST(b) (blocks along π, uniform destinations) [DERIVED, draft rigor]

Key observation (*shadowing*): the π-walk can enter the rerouted set R
only at points p ∈ R with π^{−1}(p) ∉ R ("run starts") — interior
block members have rerouted π-predecessors, from which the orbit jumps
away instead of walking on. Run-start density: p is a run start iff
π^{−1}(p) uncovered (no seed among π^{−j}(p), j = 1..b) and p itself a
seed ⇒ ρ = (c/n)(1−c/n)^b. So reroute events occur along the orbit at
rate n·ρ = c(1−c/n)^b → c, with uniform destinations: kill prob t;
a jump landing on a fresh rerouted point re-jumps immediately (chain),
but chains have length 1 a.s. in the limit (P(land in R) = bc/n → 0).
Bookkeeping caveats (draft rigor): observing R reveals fragments of π
along blocks; these involve O(bc) points of mass O(bc/n) → 0 and do
not alter the closure-hazard accounting in the limit. Hence

**φ_CLUST(b),∞(c) = φ_U(c) = ∫₀¹ e^{−ct²} dt, independent of b** —
despite |R| ≈ b·c points (b× the perturbed mass of M-U): the b−1
shadowed members per block are dynamically irrelevant. α = 1/2.
**Finite-n comparison target (declared):** dominant correction is the
rate depression c_eff = c(1−c/n)^b; the chain-kill amplification is
+O(bc/n) with partial cancellation of sign — target
φ_U(c(1−c/n)^b) with declared systematic band 2bc/n (methodology §4).

### 3.6 M-INTRA (destination uniform on own π-cycle)

**Exact, K = 1 [DERIVED]:** reroute at uniform W, its cycle has
size-biased length L, L/n → ℓ ~ U(0,1); destination v uniform on the
cycle; the surviving f-cycle is the forward segment v → W, of length
d+1, d ~ U{0,…,L−1}; all other cycles intact. φ₁ = 1 − E[ℓ] + E[ℓ]/2
= 1 − 1/2 + 1/4 = **3/4**, hence a₁ = 1 − φ₁ = **1/4** in
φ = 1 − a₁c + O(c²) (vs 1/3 for M-U: intra-cycle rerouting is
strictly gentler at first order).

**Tail [HEURISTIC — labeled]:** condition on x₀'s cycle mass ℓ; the
orbit of x₀ never leaves its cycle C (every jump lands in C), so the
dynamics is a circle process: circumference rescaled to 1, rerouted
points ~ Poisson(λ), λ = cℓ; walk from 0; at each rerouted point jump
to a uniform position; landing on visited mass or walking into a
previously created arc start ends the process (x₀ cyclic iff the end
is the walk closing into 0, i.e. a landing in the reroute-free gap
immediately upstream of 0). [Exact description up to here — given the
continuum limit; what follows is an annealed estimate.] After k jumps:
visited mass ≈ k/λ; per-jump termination ≈ k/λ (visited) + k·(1/λ)
(gaps behind the k arc starts); success ≈ 1/λ (x₀'s gap). Summing,

ψ(λ) = P(x₀ cyclic | λ) ≈ (1/λ)∫₀^∞ e^{−k²/λ} dk = √π/(2√λ),

φ_INTRA(c) ≈ ∫₀¹ min(1, ψ(cℓ)) dℓ, tail ∫₀¹ √π/(2√(cℓ)) dℓ =
**√π · c^{−1/2} ≈ 1.772 c^{−1/2}: α = 1/2 [HEURISTIC], coefficient
uncertain to an O(1) factor** (quenched/annealed gap correlations
ignored; the two termination counts above shifted the coefficient from
√(2π) to √π in successive refinements — treated as a class prediction
α = 1/2, coefficient report-only). Note M-INTRA is strongly
structure-AWARE yet lands in U_{1/2}: the kill probability still
vanishes linearly at small age (the freshly walked mass is the only
visited part of the cycle), so no atom at 0⁺ forms — consistent with
§2's criterion.

## 4. Exact K=1 battery (all size-biased, independent of §1) [DERIVED]

| Mechanism | φ₁ exact |
|---|---|
| M-U | 2/3 (wave 2) |
| M-MIX(1/2) | 7/12 |
| M-PREV | 1/2 |
| M-SELF | 1/2 (not simulated; = M-PREV limit value by coincidence of E[L]) |
| M-INTRA | 3/4 |

## 5. Predicted class table (to be tested; status per line)

| Mechanism | φ_∞(c) | tail (c→∞) | α | class | status |
|---|---|---|---|---|---|
| M-U | ∫₀¹e^{−ct²}dt | (√π/2)c^{−1/2} | 1/2 | U_{1/2} | DERIVED+verified (waves 1–2) |
| any exchangeable destination | = M-U | same | 1/2 | U_{1/2} | DERIVED (lemma §3.1) |
| M-CLUST(b) | = M-U, ∀ fixed b | same | 1/2 | U_{1/2} | DERIVED (draft) |
| M-INTRA | no closed form derived | ~√π·c^{−1/2} (coeff. heuristic) | 1/2 | U_{1/2} | K=1 DERIVED; tail HEURISTIC |
| M-MIX(p>0) | ∫₀¹e^{−c(pt+(1−p)t²)}dt | 1/(pc) | 1 | U_1 | DERIVED |
| M-SELF | (1−e^{−c})/c | 1/c | 1 | U_1 | DERIVED (2 routes) |
| M-PREV | (1−e^{−c})/c | 1/c | 1 | U_1 | DERIVED (2 routes) |
| abstract q ~ a·s^β, β∈(0,1) | ∫₀¹e^{−cH_q}dt | ~c^{−1/(1+β)} | 1/(1+β) | U_{1/(1+β)} | DERIVED in M-q; no natural intrinsic realization found |
| any M-q | (1.2) | — | ∈ [1/2, 1] | floor/ceiling | DERIVED (§2) |

## 6. Loose ends, honestly listed

1. Finite-n → continuum passage: same status as wave 2 (empirically
   controlled, not fully rigorous); all "DERIVED" limit claims here
   are conditional on that description, and B1/B2 test them at
   n = 32768 only.
2. The M-q class is defined at exploration level; mapping a concrete
   mechanism into it (identifying its q and checking survivors create
   exactly one closure target) is a per-mechanism argument. M-CLUST's
   mapping is draft-rigor (bookkeeping of π-reveals by R). M-INTRA
   does NOT map into M-q (its jumps stay on one cycle); its tail
   status is heuristic only.
3. Intermediate exponents α ∈ (1/2, 1): realized abstractly by
   q = a·s^β, β ∈ (0,1); we did NOT find a natural intrinsic
   mechanism realizing them. Candidate examined on paper (heavy-tailed
   backward π-jumps) appears to yield α = 1, not intermediate — left
   OPEN, no claim recorded.
4. M-INTRA mean curve at moderate c: no derived form; cells c ∈
   {0.5, 2} are tabulation-only.
5. No novelty claims: classification is internal to this archive;
   priority questions are front A's mandate (DISC-DEC-015).
