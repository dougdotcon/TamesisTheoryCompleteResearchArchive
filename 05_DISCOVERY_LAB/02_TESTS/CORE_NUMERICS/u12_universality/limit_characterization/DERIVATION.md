# DERIVATION — the limit function φ_∞(c) of the u12 ensemble

**Status of every claim below: DERIVED (probabilistic argument, each step
verifiable), unless explicitly marked otherwise.** Written before the
numerical runs of this front (see METHODOLOGY_NOTE.md for the
pre-registered validation protocol).

## 0. Setup and notation

Finite model: π a uniform permutation of [n]; independently for each i,
with probability q = c/n set f(i) = U_i (uniform on [n], independent),
else f(i) = π(i). Observable: φ(n,c) = E[#cyclic points of f]/n, where
i is cyclic iff f^t(i) = i for some t ≥ 1. Goal: φ_∞(c) = lim_{n→∞} φ(n,c)
(existence established empirically in wave 1; the derivation below
constructs the limit directly).

By exchangeability, φ(n,c) = P(x₀ cyclic) for a fixed (equivalently,
uniform) point x₀. We compute this probability by revealing the
randomness along the f-orbit of x₀ ("exploration process"), which is
exact at finite n and converges to a clean continuum process.

## 1. The exploration process (exact description, finite n)

Reveal the orbit x₀ → f(x₀) → f²(x₀) → … step by step. At each newly
visited point w:

1. Reveal w's reroute indicator (prob. q): if rerouted, f(w) = uniform
   on [n] ("jump"); else f(w) = π(w).
2. π is revealed lazily: π(w) is uniform on the set of points whose
   π-preimage has not yet been revealed.

Bookkeeping (all verifiable invariants of the orbit):

- The visited set is a single path x₀ → … → w (no repeats until the
  first "terminal event" below, since π-steps can only hit points with
  unrevealed π-preimage, and jumps that hit the path end the exploration
  — see below).
- The path decomposes into **arcs**: maximal runs of π-steps. Arc starts
  are x₀ and every jump destination that landed on fresh territory.
  Points entered *by a π-step* (arc interiors and arc ends) have their
  π-preimage revealed; **arc starts do not** (x₀ was never entered;
  jump destinations were entered by f-jumps, which reveal f, not π).
  Hence the π-preimage-free set = (unvisited points) ∪ (arc starts).
- Rerouted points end their arc; note π at a rerouted point is *never*
  revealed, so rerouted points stay out of the π-image bookkeeping.

Terminal events (after which the orbit is deterministic forever):

- **(A) π-closure:** a π-step from the current point w hits an arc
  start u_i (possible precisely because arc starts are π-preimage-free).
  Then the orbit cycles on u_i → … → w → u_i. The resulting f-cycle
  contains x₀ **iff u_i = x₀** (x₀ is the first point of the path; a
  cycle rooted at any later arc start excludes it).
- **(B) jump into visited territory:** a jump lands on an already
  visited point y. The orbit then cycles on y → … → (jump point) → y.
  This cycle contains x₀ iff y = x₀ exactly — probability 1/n per jump,
  vanishing in the limit.

Non-terminal events: a jump landing on fresh territory starts a new arc
(m → m+1, where m = number of arc starts, m(0) = 1).

**Conclusion (exact):** x₀ is cyclic iff the first terminal event is a
π-closure into x₀ itself, up to an O(1/n) correction from (B) hitting
x₀ exactly and from x₀ itself being rerouted (prob c/n).

## 2. Continuum limit: rates per unit of traversed mass

Let t ∈ [0,1) be the traversed (=visited) fraction of [n]; one step
traverses mass 1/n. With m arc starts and t·n visited points:

- **Reroute hazard:** each fresh point is rerouted w.p. c/n ⇒ rate
  **c dt**. Given a reroute at time t: the jump lands visited w.p. t
  (terminal, non-cyclic a.s.), lands fresh w.p. 1−t (m → m+1).
- **π-closure hazard:** π-step target is uniform over the
  π-preimage-free set, of size n(1−t) + m ≈ n(1−t). Probability of
  hitting a *specific* arc start per step: 1/(n(1−t)) ⇒ rate per unit
  mass **1/(1−t) per arc start**; total closure rate m/(1−t), and the
  hit is uniform among the m arc starts.

So closure-into-x₀ occurs at rate exactly **1/(1−t)**, independent of m:

φ_∞(c) = ∫₀¹ E[S(t)] · dt/(1−t),                    (2.1)

where S(t) = 1{no terminal event before t}. (The m-dependence survives
only inside S(t).)

Sanity check at c = 0: no reroutes, S(t) = survival of the single
closure clock of rate 1/(1−t) ⇒ E[S(t)] = exp(−∫₀ᵗ dr/(1−r)) = 1−t, and
(2.1) gives ∫₀¹ 1 dt = 1 = φ_∞(0). ✓ (Also: the closure time has density
1 on [0,1] — the size-biased cycle length of a uniform permutation is
uniform, the classical result recovered.)

## 3. Solving for E[S(t)] by the Poisson PGFL

Reroute events on [0,t] form a Poisson process of rate c (independent
Bernoulli(c/n) marks on n·t points). Condition on the reroute times
{s_j}. Each reroute independently: kills with prob. s_j (jump lands
visited — terminal, and if this happens S(t) = 0), else survives and
adds one arc start, i.e. adds closure hazard 1/(1−r) for r ∈ [s_j, t].
Given the marked configuration,

S-survival = 1{no killing reroute} · exp(−∫₀ᵗ m_s/(1−s) ds),
   m_s = 1 + #{surviving reroutes ≤ s}.

The base contribution (the "1", x₀'s own arc-start clock) gives
exp(−∫₀ᵗ dr/(1−r)) = (1−t). Each reroute at time s contributes the
independent multiplicative factor

F(s) = (1−s) · exp(−∫ₛᵗ dr/(1−r)) + s · 0
     = (1−s) · (1−t)/(1−s)
     = **(1−t)**   — independent of s.

By the probability generating functional of the Poisson process,

E[S(t)] = (1−t) · exp(−c ∫₀ᵗ (1 − F(s)) ds)
        = (1−t) · exp(−c ∫₀ᵗ t ds)
        = (1−t) · e^{−c t²}.                        (3.1)

The two hazards conspire so that a surviving reroute (prob 1−s) exactly
cancels its own added closure hazard ((1−t)/(1−s)); the net attrition
per reroute is (1−t) regardless of when it occurs. This cancellation is
the entire reason a closed form exists.

## 4. The closed form

Substituting (3.1) into (2.1), the (1−t) factors cancel:

**φ_∞(c) = ∫₀¹ e^{−c t²} dt = (1/2)·√(π/c) · erf(√c).**   (4.1)

Equivalently φ_∞(c) = c^{−1/2} ∫₀^{√c} e^{−u²} du = E[e^{−cU²}],
U ~ Uniform(0,1).

### 4.1 Series (exact, from term-by-term integration; entire function)

φ_∞(c) = Σ_{k≥0} (−c)^k / (k! (2k+1))
       = 1 − c/3 + c²/10 − c³/42 + c⁴/216 − c⁵/1320 + …    (4.2)

(a_k denominator: k!(2k+1); radius of convergence ∞.)

### 4.2 Large-c asymptotics (exact, from the erf expansion)

φ_∞(c) = (√π/2)·c^{−1/2} − e^{−c}·[1/(2c) − 1/(4c²) + 3/(8c³) − …] (4.3)

The tail is a **pure** c^{−1/2} power law with coefficient
A = √π/2 = 0.8862269255, up to exponentially small corrections — sharper
than the wave-1 statement "~c^{−1/2}". (Contrast: the refuted archive
form (1+c)^{−1/2} has tail coefficient 1 and power corrections.)

### 4.3 Conditional-K predictions (exact consequence of (4.1))

Writing e^{−ct²} = e^{−c} e^{c(1−t²)} and expanding the Poisson mixture
φ_∞(c) = Σ_K e^{−c} c^K/K! · φ_K gives

**φ_K = ∫₀¹ (1−t²)^K dt = 4^K (K!)² / (2K+1)!**  (Wallis integrals):
φ₀ = 1, φ₁ = 2/3, φ₂ = 8/15, φ₃ = 16/35, φ₄ = 128/315, φ₅ = 256/693.

These are rigid parameter-free predictions for the limit object
conditioned on exactly K reroutes — tested in run T3.

## 5. Independent low-order verification (separate route, no exploration process)

**Claim: φ₁ = 2/3 exactly** (hence a₁ = φ₀ − φ₁·(coeff) ⇒
dφ/dc|₀ = −φ₀ + φ₁ = −1/3, i.e. a₁ = 1/3 in φ = 1 − a₁c + O(c²)).

Direct computation on the limit object with exactly one reroute: the
reroute sits at a uniform position x; the cycle C containing a uniform
position has size-biased length L ~ Uniform(0,1) (classical: the cycle
of a fixed element of a uniform permutation has length uniform on
{1,…,n}). Destination u uniform on [0,1]:

- If u ∉ C (prob 1−L): C is broken, nothing re-enters it ⇒ cyclic mass
  = 1 − L.
- If u ∈ C (prob L): the jump map has the single cycle {reroute}, and
  the f-cycle is the forward segment from u to x, of length
  d ~ Uniform(0, L) given u ∈ C ⇒ cyclic mass = 1 − L + d.

E[loss] = E[L − 1{u∈C} d] = E[L − L²/2] = 1/2 − 1/6 = **1/3**
⇒ φ₁ = 1 − 1/3 = 2/3. ✓ Matches (4.3)'s Wallis value ∫₀¹(1−t²)dt = 2/3.

This is a genuinely independent check: it uses the wave-1 adversarial
limit-object construction (PD(1) + segments), not the exploration
process; and it refutes (1+c)^{−1/2} analytically at first order
(that form has a₁ = 1/2 ≠ 1/3).

**Also exact (used as simulator component test T4):**
E[reroute-free cycle mass] = E[Σ_i L_i e^{−cL_i}] = E[e^{−cL*}] with L*
the size-biased pick ~ U(0,1) ⇒ **(1 − e^{−c})/c**.

## 6. Loose ends, honestly listed

1. The exploration-process limit (Section 2) is a standard
   rates-convergence argument, not written here at full
   Stein/coupling rigor; the O(1/n) terminal events (B→x₀, x₀ rerouted)
   and the m/n corrections vanish in the limit. Wave-1's finite-n data
   (deviations stable from n = 2·10³ to 6.4·10⁴ and matching the
   continuum object at χ² p = 0.09/0.58) plus this front's T1–T4 tests
   are the empirical control of that step.
2. Everything else — (2.1), (3.1), (4.1)–(4.3), Section 5 — is exact
   given the continuum description, with each step elementary.
3. Classification per the line's discipline: (4.1) with Sections 1–3, 5
   is a **derivation** (category (a): reduced to well-defined
   probabilistic identities), not a fit; its status against the
   pre-registered numerical criteria is reported in RESULTS_SUMMARY.md.
