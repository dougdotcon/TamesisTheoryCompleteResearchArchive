# Generalizing the Full Cycle-Count Decomposition Theorem from K=3 to general K

**Task ID:** `GENERAL-K-DECOMPOSITION-ATTEMPT`, `DISC-DEC-110`, wave 23
front (b). Direct successor to Estagio 40's K=3 result
(`k3_joint_structural_attempt/k3_full_cdf_attempt`) and sibling to
`general_k_joint_attempt`/`pnn_general_k_egf_attempt` (which generalized a
different, weaker quantity — the pairwise second moment `P_nn(n,K)` — to
general `K`). Pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble defined in `THEOREM.md`
Definitions 1–4. **This is not a Millennium Prize Problem and no claim of
that kind is made anywhere below.**

Reserved seeds: `20260924000`–`20260924999` (this front's own, per
`DISC-DEC-110`; grep-confirmed unused before first use — see Section 9).
No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created here (a separate
hostile referee will be dispatched later by the orchestrating session), no
`git` command run. All work confined to this new subdirectory. **No `.py`
file from any other front in this lineage (this front's own ancestors,
`k3_full_cdf_attempt`, `general_k_joint_attempt`, `pnn_general_k_egf_attempt`,
or any other) was opened, read, or imported anywhere** — every script here
is written completely fresh from the mathematical prose of `THEOREM.md` and
the cited `ATTEMPT.md` documents, per the mandate's hard constraint.

---

## Executive summary (read first)

**The exact target.** Estagio 40 (K=3) proved the **Full Cycle-Count
Decomposition Theorem**: `T = O + sum_{s in S} V_s`, where `T` is the total
count of cyclic points, `S subseteq {0,1,2}` is the random set of cyclic
reroute sources, and, given `S`, the `V_s` (`s in S`) are **mutually
independent**, `V_s ~ Uniform{1,...,L_s}`. Its own text flagged the method
as "looking structurally generalizable... but this is an unverified hint,
not a claim." This front's mandate: attempt the general-`K` version.

**What closed (PROVED, unconditionally, for every `K` and every subset
`A subseteq {0,...,K-1}`) — the main new mathematical content of this
document:**

1. **Proposition S, general `K` (Section 2, PROVED, new).** A single,
   `K`-free, `|A|`-free closed form for the ENTIRE law of `S`:
   ```
   P(S = A) = |A|! * (prod_{a in A} p_a) * (p_D + sum_{a in A} p_a)
   ```
   for **every** `A subseteq {0,...,K-1}` and **every** `K >= 0`, where
   `p_i := L_i/n`, `p_D := O/n` (`sum_i p_i + p_D = 1`). This one formula
   **exactly reproduces all four of Estagio 40's separate K=3 formulas**
   as the special cases `|A| = 0,1,2,3` (verified symbolically, Section
   2.5) — Estagio 40 had four different-looking closed forms because it
   never noticed they are all one formula. It also recovers the (already
   known, trivial) full-cycle case `P(S = {0,...,K-1}) = K! prod_i p_i`
   for general `K`.
2. **The Full Cycle-Count Decomposition Theorem, general `K` (Section 3,
   PROVED).** `T = O + sum_{s in S} V_s`, `(V_s)_{s in S}` mutually
   independent given `S`, `V_s ~ Uniform{1,...,L_s}` — proved to hold for
   **every** `K`, by literally the same argument as K=3 with `3` replaced
   by `K` throughout (confirming the mandate's own hint), building on
   Lemma 4's already-PROVED general-`K` form (Estagio 38, cited) and the
   already-PROVED general-`K` "landing-position-uniform-and-independent"
   fact (`general_k_joint_attempt` Section 4.1, cited).

**The crux, and what made it close.** Proposition S's proof reduces to one
key lemma: for a subset `B` of "the rest," with weights `p_b` (`b in B`)
and combined "escape" weight `q_B := 1 - sum_{b in B} p_b`, **the
probability that NO node of B lies on a cycle equals exactly `q_B`,
regardless of how the escape weight is internally distributed among the
individual escape flavors, and regardless of `|B|`.** This is proved here
by strong induction on `|B|`, via a self-similar recursive partition
identity plus a genuinely new algebraic identity
`(1 - P_B) F(B) + G(B) = 1` (`F, G` explicit subset sums), itself proved
via an exponential-integral representation and integration by parts
(Section 2.3) — a complete, `K`-free, `|B|`-free derivation, not a
verified-pattern claim.

**What did NOT close (honestly scoped, Section 5).** A single
closed-form-in-`(n,K)` CDF `P(M_n^{(K)} <= k/n)` — the direct `K`-general
analogue of Estagio 40's Proposicao D3 — was **not attempted** beyond a
small demonstration that the algorithmic machinery works (Section 4,
explicitly labeled secondary/bonus, per the mandate's own scoping); this
mirrors the general-`K` second-moment fronts' own experience (Estagio
38/39) that the *method* generalizing cleanly does not imply a single
symbolic-in-`K` closed form falls out easily, and no attempt is made here
to close that harder, separate question.

**Net verdict.** The **primary mandate is CLOSED**: both Proposition S and
the Full Cycle-Count Decomposition Theorem generalize to every `K`, with
genuine `K`-free proofs (not merely verified at many concrete `K`), making
this front's headline result *strictly stronger* than the general-`K`
second-moment closures of Estagio 38/39 in the specific sense the mandate
asked about (the entire joint law of `S` and `T`, not just a pairwise
scalar). The secondary target (a single symbolic CDF formula) remains
open, correctly out of primary scope. No claim of progress on any
Millennium Problem; pure internal combinatorics on the u12 ensemble
defined in `THEOREM.md`.

---

## 1. Reading discipline and notation

### 1.1 What was read

`THEOREM.md` Estagio 40 **in full** (the primary generalization target):
Section 2 (the Full Cycle-Count Decomposition Theorem and its proof),
Section 2.2 (Proposicao S's K=3 proof — the i.i.d.-destinations
observation, the full-cycle case, and the case-enumeration for
`|A|=1,2`). Estagio 35 **in full** (Lemma 4, Cycle-Predecessor Uniqueness,
K=3) and Estagio 38 **in full** (its already-PROVED general-`K` form,
"literally the same proof as K=3 with 3 replaced by K, never uses the
specific value 3 in any logical step" — cited verbatim, not re-derived).

The K=3 full-CDF front's own `ATTEMPT.md`
(`.../k3_joint_structural_attempt/k3_full_cdf_attempt/ATTEMPT.md`), read
**in full**, in prose, as the structural/style template for this document
(its Section 2's exact statement and proof of the Decomposition Theorem
and Proposicao S are the direct generalization target; its overall
document structure — executive summary, notation, numbered proof
sections, independent-verification subsections, honest non-closure
section, files/seeds/scorecard tables, scope discipline — is reproduced
here). **No `.py` file from this front was read**, per the mandate.

The general-`K` second-moment fronts' `ATTEMPT.md` files, read in full,
for their K-general notation conventions (reused, not reinvented):
`.../k3_joint_structural_attempt/general_k_joint_attempt/ATTEMPT.md`
(sources `{0,...,K-1}`, targets `U_0,...,U_{K-1}`, `x_s := L_s/n`,
`Others(s)`, the Governing-Source Reindexing citation, the "`(K+1)^K` raw
destination table" verification style) and
`.../general_k_joint_attempt/pnn_general_k_egf_attempt/ATTEMPT.md` (the
`sum_k k! e_k(x)` exponential-integral identity, which this front
independently re-derives and extends in Section 2.3 — no code from either
front was read, only their prose notation and the cited identity's
statement, re-proved here from scratch). **No `.py` file from either
front was read**, per the mandate.

### 1.2 Notation (this lineage's own, reused without modification)

`K >= 0` reroute sources fixed WLOG at `{0,...,K-1}`. Targets
`U_0,...,U_{K-1}` i.i.d. `Uniform([n])`, independent of the underlying
permutation `pi`. `f(i) := U_i` for `i in {0,...,K-1}`, `f(i) := pi(i)`
otherwise. `T := #{cyclic points of f}` (so `M_n^{(K)} = T/n`). By the
Governing-Source Reindexing corollary (Estagio 35 K=3 / Estagio 38
general-`K`, **cited, not re-derived**): the gap vector
`(g_0,...,g_{K-1}, O)` is uniform over compositions of `n-K` into `K+1`
nonnegative parts, independent of topology; `L_s := g_s + 1` is the length
of the arc governed by source `s` (`ARC(s)` has `L_s` positions,
`1,...,L_s-1` interior, position `L_s` the source itself); `O` is the
count of points on no marked arc; `n = O + sum_s L_s`. `x_s := L_s/n =:
p_s`, `p_D := O/n` (both names used interchangeably below, matching the
two cited fronts' own differing conventions: `p_i` as in Estagio 40's own
K=3 notation, `x_s` as in `general_k_joint_attempt`'s).

`S subseteq {0,...,K-1}` is the (random) set of **cyclic sources**
(Estagio 40/Estagio 35's own definition, cited): source `s` is cyclic iff
iterating `dest` from `s` (the categorical destination of `U_s` among
`{0,...,K-1,DEAD}`) returns to `s` before hitting `DEAD`.

---

## 2. Proposition S, general K (PROVED, new — the main result)

### 2.1 Setup: i.i.d. categorical destinations (cited, already K-free)

Estagio 40 Section 2.2 observed, for K=3, that `dest(0),...,dest(K-1)` are
**i.i.d.** categorical on `{0,...,K-1,DEAD}` with weights
`(p_0,...,p_{K-1},p_D)` — `dest(s)=t` has probability `p_t` for **every**
`s`, since it depends only on which region `U_s` lands in. Nothing in this
observation is specific to `K=3`; it holds verbatim for every `K`, and is
cited here as such (re-verified as part of the raw enumeration checks of
Section 2.5).

### 2.2 The reduction: S=A splits into an independent bijection-on-A event and a no-cycle-on-the-rest event

Fix `A subseteq {0,...,K-1}`, `|A|=m`, and write `B := {0,...,K-1} \ A`.

> **Claim.** `S = A` holds if and only if (i) `dest` restricted to `A` is a
> bijection `A -> A`, **and** (ii) no node of `B` is cyclic, where "cyclic"
> for `B` treats landing anywhere in `A` as equivalent to landing in
> `DEAD` (both are absorbing from `B`'s perspective).

*Proof.* If `dest|_A` is a bijection, every node of `A` lies on a cycle
entirely within `A` (a permutation decomposes into cycles covering its
whole domain) — so `A subseteq S`. Any trajectory from a node `b in B`
that ever enters `A` stays in `A` forever (since `A` is `dest`-closed on
itself), so it can never return to `b` — `b` is not cyclic whenever its
trajectory enters `A`. Hence `b in B` is cyclic if and only if its
trajectory, treating entry into `A` as equivalent to `DEAD`, forms a cycle
entirely within `B`. This is exactly "no node of `B` is cyclic" in the
stated sense. Conversely, if (i) and (ii) both hold, every node of `A` is
cyclic (by (i)) and no node of `B` is cyclic (by (ii)), so `S = A`
exactly. `∎`

Since `{dest(a) : a in A}` and `{dest(b) : b in B}` are independent
(disjoint sub-collections of the mutually independent family
`{dest(i)}_i`), events (i) and (ii) are **independent**:
```
P(S = A) = P(dest|_A is a bijection A->A) * R(B)
```
where `R(B) := P(no node of B is cyclic, treating escape into A as
equivalent to DEAD)`.

`P(dest|_A bijection) = m! * prod_{a in A} p_a`: summing the product
`prod_{a in A} p_sigma(a)` over the `m!` permutations `sigma` of `A` gives
`prod_{a in A} p_a` for **every** `sigma` (it is the same set of `m`
factors, just relabeled), so the sum over all `m!` permutations is
`m! * prod_{a in A} p_a`. This step is a one-line, fully `K`-free,
`|A|`-free fact (Estagio 40's own K=3 full-cycle case, `6 p_0 p_1 p_2`, is
exactly this at `m=3`).

### 2.3 The crux: R(B) = q_B for every B (PROVED, new — the hard part)

> **Key Lemma.** For any finite index set `B`, any weights `p_b >= 0`
> (`b in B`), and combined escape weight `q_B := 1 - sum_{b in B} p_b`
> (`p_b` and `q_B` here need only be understood as the raw normalized
> categorical weights of a `dest`-type random function `B -> B ∪
> {ESCAPE}`, `ESCAPE` possibly itself a bundle of several distinguishable
> targets, e.g. `DEAD` **and** every `a in A`, as in Section 2.2):
> `R(B) = q_B`.

This directly generalizes (and, applied with `B = {0,1,2}`, `A = empty`,
exactly reproduces) the one fact Estagio 40 itself proved only by "a
direct symbolic sum over all 64 cases" (its own words, Section 2.2) rather
than a hand argument — `P(S=empty) = p_D`. Here it is proved in general.

*Proof, by strong induction on `|B|`.*

**Base case `|B|=0`:** `R(empty) = 1 = q_empty` trivially (no node, vacuous
truth, and `q_empty = 1 - 0 = 1`).

**Self-similar recursive partition.** For `C subseteq B`, the *same*
argument as Section 2.2 (with `B` in the role of "the whole universe" and
`C` in the role of "A") gives:
```
P(S ∩ B = C) = |C|! * prod_{c in C} p_c * R(B \ C)
```
(independence of `dest|_C` and `dest|_{B\C}`, plus the bijection-on-C
fact — this argument never referenced the *original* full index set
`{0,...,K-1}`, only that `B` is *some* finite index set with i.i.d.
weighted destinations, so it applies recursively to `B` itself with no new
argument needed). Since `{S ∩ B = C : C subseteq B}` partitions the whole
probability space:
```
sum_{C subseteq B} |C|! prod_{c in C} p_c * R(B\C) = 1.      (*)
```

**Inductive step.** Assume `R(B') = 1 - P_{B'}` (`P_{B'} := sum_{b in B'}
p_b`) for every `B'` with `|B'| < |B| =: m`. Separate the `C=empty` term of
(*) (which is exactly `R(B)`, the unknown) from the rest, and substitute
the inductive hypothesis `R(B\C) = 1 - P_B + P_C` (valid since `B\C ⊊ B`
for `C != empty`):
```
R(B) = 1 - sum_{C != empty} |C|! prod_C p_c * (1 - P_B + P_C)
     = 1 - (1-P_B)(F(B)-1) - G(B)
```
where `F(B) := sum_{C subseteq B} |C|! prod_{c in C} p_c` and
`G(B) := sum_{C subseteq B} |C|! prod_{c in C} p_c * P_C` (`P_C := sum_{c
in C} p_c`; both sums include the `C=empty` term, which contributes `1`
to `F` and `0` to `G`). Algebra reduces "R(B) = 1 - P_B" (the desired
conclusion) to exactly the identity:
```
(1 - P_B) F(B) + G(B) = 1.                                    (**)
```

**Proof of (**).** Using the exponential-integral identity `k! =
int_0^infty lambda^k e^{-lambda} d(lambda)`, define `g(lambda) :=
prod_{c in B} (1 + p_c lambda)`, so `F(B) = int_0^infty e^{-lambda}
g(lambda) d(lambda)` (expand `g` as `sum_k e_k(p) lambda^k`, `e_k` the
elementary symmetric polynomial, and integrate term-by-term).
Differentiating `log g`: `g'(lambda)/g(lambda) = sum_c p_c/(1+p_c
lambda) =: L(lambda)`. A direct algebraic identity gives
`sum_c p_c^2/(1+p_c lambda) = [P_B - L(lambda)]/lambda`, hence
`g(lambda) * sum_c p_c^2 prod_{c' != c}(1+p_{c'} lambda)/g(lambda) =
[P_B g(lambda) - g'(lambda)]/lambda`. Since `G(B) = sum_{j in B} p_j^2
int_0^infty lambda e^{-lambda} prod_{c != j}(1+p_c lambda) d(lambda)`
(expand the definition of `G`, isolating each `j in C`), substituting the
identity above and integrating term-by-term gives
```
G(B) = int_0^infty e^{-lambda} [P_B g(lambda) - g'(lambda)] d(lambda)
     = P_B F(B) - int_0^infty e^{-lambda} g'(lambda) d(lambda).
```
Integration by parts on the last integral (`u=e^{-lambda}`, `dv=g'
d(lambda)`, boundary terms vanish since `e^{-lambda}` decays faster than
any polynomial, and `g(0)=1`): `int_0^infty e^{-lambda} g'(lambda)
d(lambda) = -g(0) + int_0^infty e^{-lambda} g(lambda) d(lambda) = F(B) -
1`. So `G(B) = P_B F(B) - (F(B)-1) = 1 - (1-P_B)F(B)`, which is exactly
(**). `∎`

This closes the induction: `R(B) = 1 - P_B = q_B` for every finite `B`
and every choice of weights, with **no reference to `K`, `|A|`, or which
specific escape flavors make up `q_B`** — a genuinely general, `K`-free
proof, not a pattern verified at finitely many sizes.

### 2.4 Assembly: Proposition S, general K

Combining Sections 2.2–2.3, with `B := {0,...,K-1}\A` and
`q_B = 1 - sum_{b in B} p_b = p_D + sum_{a in A} p_a` (since `sum_i p_i +
p_D = 1`):

> **Proposition S (general K, PROVED, new).** For every `K >= 0` and every
> `A subseteq {0,...,K-1}` (`m := |A|`):
> ```
> P(S = A) = m! * (prod_{a in A} p_a) * (p_D + sum_{a in A} p_a).
> ```

**Recovers Estagio 40's four K=3 formulas exactly, as one unified
expression:**
- `m=0`: `P(S=empty) = 0! * 1 * p_D = p_D`. ✓ matches.
- `m=1`, `A={s}`: `1! * p_s * (p_D + p_s) = p_s(p_s+p_D)`. ✓ matches.
- `m=2`, `A={s,t}`, third index `u`: `2! p_s p_t (p_D+p_s+p_t)`; since
  `p_D+p_s+p_t = 1-p_u`, this is `2 p_s p_t (1-p_u)`. ✓ matches.
- `m=3`, `A={0,1,2}`: `3! p_0p_1p_2 * (p_D+p_0+p_1+p_2) = 6p_0p_1p_2 * 1 =
  6p_0p_1p_2` (using `p_D+p_0+p_1+p_2=1`). ✓ matches.

Estagio 40 presented these as four separately-derived formulas (three by
direct case counting, the fourth — `P(S=empty)=p_D` — only by raw
64-case symbolic summation, its own words). Proposition S shows they were
always one formula; this is a genuine simplification and unification, not
merely a generalization.

### 2.5 Independent verification

**(a) Algebraic identity `(**)`** (`algebraic_identity_check.py`): the
identity `(1-P_B)F(B)+G(B)=1` is verified two independent ways — (i)
direct subset-sum expansion of `F`, `G` from their raw definitions, fully
symbolic in free `p_1,...,p_m` (no normalization assumed — this is a
*pure algebraic* identity, true for **any** values, not just probability
weights), `m=1,...,9`, **all exact matches**; (ii) an independent
recomputation of `G(B)` via `sp.integrate` (genuine symbolic integration,
not the hand-derived shortcut), `m=1,...,4`, cross-checked against (i) —
**all exact matches**.

**(b) `R(B) = q_B`, raw definition** (`no_cycle_probability_general_m.py`):
verified by brute enumeration of all `(m+1)^m` raw destination functions
with direct cycle detection (no formula, no shortcut) — fully symbolic
(free `p_0,...,p_{m-1}`) for `m=0,...,5` (`(m+1)^m` up to `7776` raw
cases), and with concrete generic rational weights for `m=6,7` (up to
`2,097,152` raw cases) — **all exact matches, zero discrepancies**.

**(c) Proposition S itself, raw `(K+1)^K` enumeration**
(`proposition_s_general_k.py`): every subset `A` checked against the raw
`(K+1)^K` destination table (cycle detection by direct forward
simulation, no shortcut), fully symbolic (free `p_0,...,p_{K-1}`, with
`p_D` **substituted as the dependent quantity `1-sum(p_i)`** — see the
important normalization note below) for `K=0,...,5` (up to `7776` raw
cases), and with concrete generic rational weights for `K=6,7` (up to
`2,097,152` raw cases) — **all exact matches**.

> **A normalization subtlety, caught and documented (not silently
> avoided).** An early version of this check left `p_D` as a genuinely
> independent free symbol (not substituted as `1-sum(p_i)`) when comparing
> the raw enumeration to the closed form, and found **nonzero mismatches**
> for `K>=3` (visible in this script's own git-history / superseded
> intermediate log, reproduced deliberately as a **negative control** —
> `check_symbolic_unnormalized_counterexample`, run at `K=3`, prints an
> explicit nonzero polynomial). This is expected, not a bug in the
> theorem: `R(B)=q_B` (Section 2.3) is a fact about **normalized**
> categorical weights (`P_B + q_B = 1` is used essentially in the
> induction's base relation `(*)`, which is a probability partition). Once
> `p_D` is correctly substituted as the dependent quantity `1-sum(p_i)`
> throughout (matching how the raw `(K+1)^K` enumeration's weights are
> actually a valid probability distribution), all checks pass exactly.
> This distinction is verified explicitly, not glossed over.

**(d) True Definition-4 brute force, unconditional**
(`true_bruteforce_definition4_general_k.py` +
`unconditional_prop_s_vs_bruteforce.py`): a **fully independent, from
scratch** implementation of Definition 4's literal model — genuine random
permutations `pi` of `[n]` (all `n!`), genuine target tuples
`U_0,...,U_{K-1}` (all `n^K`), with arcs `ARC(0),...,ARC(K-1)` and `O`
reconstructed directly from `pi`'s cycle structure (own code, splitting
each `pi`-cycle at its source boundaries — no arc/reduced-model formula
assumed as an input) — run at `(n,K) in
{(4,1),(5,1),(4,2),(5,2),(6,2),(4,3),(5,3),(6,3),(5,4),(6,4)}` (up to
`933,120` exact configurations). Confirms, **for every single
configuration**, the deterministic bookkeeping identity `T = O + sum_{s
in S} V_s` (zero failures across all configurations at every cell), and
gives the exact empirical marginal `P(S=A)` at each `(n,K)`. Averaging
Proposition S over the (correctly, **gap-vector**, not `L`-vector
directly) uniform composition distribution — `unconditional_prop_s_vs_
bruteforce.py`, a genuine, independent, exact rational average over every
composition — reproduces **every one of the 30 empirical `P(S=A)` values**
above exactly (zero discrepancies).

> **A second bug, caught and fixed (disclosed).** An early version of this
> unconditional check treated `(L_0,...,L_{K-1},O)` itself as uniform over
> compositions of `n-K`, rather than the **gap vector** `(g_0,...,g_{K-1},
> O)` (with `L_s = g_s+1`) — producing systematic mismatches (e.g.
> predicting `P(S=A)=0` for `|A|=3` at `n=6,K=4`, which is obviously wrong
> since `L_s>=1` always). Fixed by correctly citing the Governing-Source
> Reindexing statement (Section 1.2) — the composition is of the *gaps*,
> not the arc lengths directly. After the fix, all 30 values match
> exactly; see the script's own log for the full before/after record.

**(e) Monte Carlo, larger `(n,K)`** (`monte_carlo_bonus.py`, Section 6):
triangulation only, consistent with the exact results (see Section 6 for
the full disclosure of a sampling bug caught and fixed there too).

---

## 3. The Full Cycle-Count Decomposition Theorem, general K (PROVED)

### 3.1 Statement and proof

> **Theorem (Full Cycle-Count Decomposition, general K, PROVED).** For
> every `K >= 0`: `T = O + sum_{s in S} V_s`, where, given `S`, `V_s := L_s
> - k_s + 1` (`k_s` the landing position of `U_{pred(s)}` within `ARC(s)`,
> `pred` as in Lemma 4) for `s in S`, and the `(V_s)_{s in S}` are
> **mutually independent**, `V_s ~ Uniform{1,...,L_s}`.

*Proof (literally the same argument as Estagio 40's K=3 proof, `3`
replaced by `K` throughout — verified below to use no K-specific step).*
If `s` is cyclic, Lemma 4 (Cycle-Predecessor Uniqueness, **already PROVED
for general `K`**, Estagio 38, cited verbatim — "a fact about functional
graphs on any finite node set with an absorbing DEAD state," never using
`K=3`) gives a unique cycle-predecessor `pred(s)`, and `ARC(s)`'s cyclic
point-set is exactly `{k_s,...,L_s}`. If `s` is not cyclic, the same
argument used to prove Lemma 4 (a returning cycle through any position of
`ARC(s)` would force `s` itself onto the cycle) shows `ARC(s)` contributes
zero cyclic points. Combined with the `O` outside points (always cyclic,
independent of `K`), `T = O + sum_{s in S} V_s` follows by direct
counting.

`V_s` is uniform on `{1,...,L_s}` because `k_s` is the landing position,
**within `ARC(s)`**, of `U_{pred(s)}` — and a coordinate uniform on `[n]`,
conditioned on which of the `K+1` fixed regions it lands in, is uniform
**within** that region, independent of which region it was (a standard
fact about uniform random variables — already established as the
"landing-position-uniform" fact in `general_k_joint_attempt` Section 4.1,
verified there for `K=1,...,6` and stated as fully general in its own
proof; **cited, not re-derived**, since it is already on record as
`K`-free). For `s != s'` both in `S`: `pred(s) != pred(s')` (distinct
cyclic nodes have distinct cyclic predecessors — `pred` is the inverse of
`dest` restricted to the cyclic subset, a bijection there, by Lemma 4's
own proof, itself already `K`-free per Estagio 38), so `V_s, V_{s'}` are
determined by the landing positions of **two different** `U_t`'s, hence
independent (the `U_t` are i.i.d.). `∎`

**Every step above is either (a) a direct restatement of an
already-PROVED-general-`K` fact (Lemma 4, Estagio 38; the
landing-position-uniform fact, `general_k_joint_attempt` Section 4.1), or
(b) an elementary counting/independence argument that never references the
number `3` or any other specific value of `K`.** This is a genuine
generalization, not a re-verification at finitely many `K` — confirming
the mandate's own hint in the affirmative, exactly as Estagio 38 already
confirmed it for Mechanisms 1–2.

### 3.2 Independent verification

**Position-level, fresh reduced model, no reference to Lemma 4's
conclusion** (`decomposition_theorem_position_level.py`): builds an
explicit position-level functional graph directly from the prose
description of Definition 4 plus the (cited) Governing-Source Reindexing
fact — `ARC(t)` positions `1,...,L_t`, deterministic successor `i ->
i+1` within an arc, source `t`'s own successor determined by its raw
target choice (region + within-region position, enumerated exactly, `n^K`
raw configurations per cell) — and determines cyclicity by **direct
forward simulation**, with **no reference to "who the cycle predecessor
is"** anywhere in the construction (that fact, if true, must emerge from
the simulation, not be assumed by it). At `11` concrete `(K, L, O)`
configurations spanning `K=1,...,5` (up to `3125` raw target-configs per
cell): (i) the bookkeeping identity `T = O + sum V_s` holds in every
single configuration; (ii) for **every** observed value of `S`, the
**joint** empirical distribution of `(V_s)_{s in S}` matches the predicted
product of independent `Uniform{1,...,L_s}` distributions **exactly**
(every cell of the product space hit with equal count) — **zero
discrepancies**.

**True Definition-4 brute force** (`true_bruteforce_definition4_general_
k.py`, Section 2.5(d)): the bookkeeping identity `T=O+sum_{s in S}V_s` is
also confirmed, per-configuration, against a fully independent
implementation built directly from genuine random permutations (arcs
reconstructed from `pi`'s actual cycle structure, not assumed) —
`933,120` configurations at the largest cell (`n=6,K=4`), zero failures.

**Bonus: the algorithmic route to a general-K conditional CDF**
(`conditional_cdf_general_k_demo.py`, Section 4): Proposition S plus the
Decomposition Theorem together give an explicit algorithm for `P(T<=k |
L)` for any concrete `K`, verified exactly against the same from-scratch
position-level ground truth at `K=2,3,4` — see Section 4 for the precise,
deliberately limited, scope of this demonstration.

**Monte Carlo, larger `(n,K)`:** Section 6.

---

## 4. Implications for a K-general CDF machinery (bonus, secondary per the mandate)

The mandate designates a single closed-form-in-`(n,K)` CDF (the direct
analogue of Estagio 40's Proposicao D3) as a **secondary** target, to be
attempted only "if [the primary target] closes easily and you have
significant time left" — and explicitly instructs **not** to attempt the
full symbolic-in-`K` derivation as the main content of this front. Since
the primary target (Sections 2–3) closed with a complete `K`-free proof,
this section records, as a **bonus**, exactly how far the resulting
machinery goes and precisely where it stops — matching, not exceeding, the
mandate's scoping.

**What follows immediately from Sections 2–3, for any concrete `K`.**
Exactly as at K=3 (Estagio 40 Section 3), conditional on `(L_0,...,
L_{K-1})`:
```
P(T<=k | L) = sum_{A subseteq {0,...,K-1}} P(S=A|L) * P(O + sum_{s in A} V_s <= k)
```
where the inner probability is an elementary `|A|`-fold discrete-uniform
lattice-point count (a direct generalization of Estagio 40's `pair_count_
le`/`triple_count_le`). `conditional_cdf_general_k_demo.py` implements
this **directly** (small-`L` exhaustive lattice counting, not a scalable
closed form) and verifies it **exactly** against the same
position-level ground truth used in Section 3.2, at `4` concrete
`(K,L,O)` configurations spanning `K=2,3,4` (every `k` from `0` to `n`
checked) — **all exact matches**. This confirms, concretely (not just "in
principle"), that Proposition S + the Decomposition Theorem give a valid
algorithmic route to the conditional CDF for any `K`.

**What is explicitly NOT attempted here, and why (matching the mandate's
own scope discipline).** Turning this into a single **closed-form-in-
`(n,K)`** unconditional CDF — summing the conditional CDF over the entire
`K`-dimensional composition simplex in closed algebraic form, the way
Estagio 40 Section 4 did for the fixed value `K=3` (three combinatorial
regimes, each a `K`-fold nested `sp.summation`) — is a **substantially
harder, separate question**, for reasons directly analogous to (though not
identical to) what Estagio 38/39 already found for the much simpler
pairwise quantity `P_nn(n,K)`: even after Proposition S collapsed to one
clean formula (unlike `P_nn(n,K)`'s persistently-growing term count), the
outer sum over `2^K` subsets `A`, each contributing an `|A|`-fold lattice
count over the composition simplex, is a symbolic-in-`K` combinatorial
object of a kind this front did not attempt to push through Gosper-style
or generating-function machinery (the tool that let Estagio 39 precisely
locate, and formally certify, exactly where the analogous obstruction for
`P_nn(n,K)` lives). **No claim is made here about whether such a
closed form exists or does not** — only that it was not attempted beyond
the small demonstration above, consistent with the mandate's explicit
instruction to treat this as secondary and not force it.

---

## 5. What did NOT close, precisely (honest, as mandated)

### 5.1 The single symbolic-in-(n,K) CDF formula

Not attempted beyond Section 4's small demonstration. **OPEN**, precisely
scoped: the *conditional* CDF given `L` is fully closed-form and correct
for any `K` (Section 4); the *unconditional*, closed-form-in-`(n,K)`
version (Estagio 40 Proposicao D3's general-`K` analogue) requires summing
that conditional formula over the entire `K`-dimensional composition
simplex in closed algebraic form, which was not attempted.

### 5.2 A closed form or pattern for any rate/moment coefficient in K

No attempt was made here to derive `E[M_n^{(K)}]`, `E[(M_n^{(K)})^2]`, or
any convergence-rate coefficient as an explicit function of `K` from the
Decomposition Theorem (this is a **different** question from the
already-cited, already-closed `E[M_K^2]=1/(K+1)` continuum limit — Estagio
24 — and from the `P_nn(n,K)` rate coefficients `c_1(K)` reported, without
a pattern claim, by Estagio 38/39). Out of scope for this front's mandate,
not attempted.

### 5.3 K -> infinity behavior of any quantity here

Not examined. No claim of any kind about limiting behavior as `K ->
infinity` (this front only established results uniform **in** `K`, i.e.
holding for every fixed `K`, not a limit theorem).

### 5.4 What is explicitly NOT claimed

No claim that the closed-form-in-`(n,K)` CDF (Section 5.1) exists or does
not exist — only that it was not attempted, correctly matching the
mandate's own scoping of it as secondary. No claim about any moment or
rate coefficient's dependence on `K` (Section 5.2). No claim about
`K -> infinity` asymptotics (Section 5.3). No claim of progress on any
Millennium Problem; this is pure combinatorial mathematics internal to
the u12 ensemble defined in `THEOREM.md`.

---

## 6. Numerical exploration (bonus, not a substitute for Sections 2–4)

`monte_carlo_bonus.py`, reserved seeds `20260924001`–`20260924006`, direct
simulation of Definition 4's actual model at larger `(n,K)` than exact
brute force reaches (own random-permutation simulation path, independent
of the position-level reduced model):

```
n= 50 K=3: trials= 20000 seed=20260924001  empirical E[T]=22.9457  Prop-S-based-predicted E[T]=22.9482  diff=-0.0025
n=200 K=3: trials=  8000 seed=20260924002  empirical E[T]=92.1171  Prop-S-based-predicted E[T]=91.6132  diff=+0.5039
n= 50 K=5: trials= 20000 seed=20260924003  empirical E[T]=18.5909  Prop-S-based-predicted E[T]=18.6444  diff=-0.0534
n=200 K=5: trials=  8000 seed=20260924004  empirical E[T]=74.1817  Prop-S-based-predicted E[T]=74.0520  diff=+0.1297
n=100 K=6: trials= 10000 seed=20260924005  empirical E[T]=34.6088  Prop-S-based-predicted E[T]=34.3014  diff=+0.3074
n=300 K=4: trials=  6000 seed=20260924006  empirical E[T]=122.4865 Prop-S-based-predicted E[T]=121.8704 diff=+0.6161
```
(full transcript: `monte_carlo_bonus.log`) — all cells land within a
fraction of a standard error of the exact predictions; triangulation only,
not itself proof, per lineage convention.

> **A bug caught and fixed here too (disclosed).** An early version of
> this script sampled the governing-source gap vector via
> `rng.multinomial(n-K, uniform probs)`, which is **not** the uniform
> distribution over compositions (it is a genuinely different,
> concentration-biased distribution) — producing large, clearly
> non-noise discrepancies (e.g. `n=200,K=3`: empirical `E[T]=92.1` vs.
> predicted `81.0`, an order of magnitude beyond plausible Monte Carlo
> noise at `8000` trials). Fixed by implementing a correct
> stars-and-bars uniform-composition sampler
> (`sample_uniform_composition`, choosing `K` distinct divider positions
> uniformly without replacement) — after the fix, all six cells above
> match to well within sampling noise, as shown.

---

## 7. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `algebraic_identity_check.py` / `.log` | the crux algebraic identity `(1-P_B)F(B)+G(B)=1` (Section 2.3), verified two independent ways |
| `no_cycle_probability_general_m.py` / `.log` | `R(B)=q_B`, verified by raw `(m+1)^m` enumeration (Section 2.3/2.5b) |
| `proposition_s_general_k.py` / `.log` | Proposition S, verified against raw `(K+1)^K` enumeration, `K=0..7`, plus the negative-control demonstration of why normalization is essential (Section 2.5c) |
| `true_bruteforce_definition4_general_k.py` / `.log` | fresh, fully independent true brute force of Definition 4's literal model (own arc reconstruction), confirming the bookkeeping identity and giving exact empirical `P(S=A)` (Section 2.5d, 3.2) |
| `unconditional_prop_s_vs_bruteforce.py` / `.log` | Proposition S averaged over the true (gap-vector) composition distribution, matched exactly against the true-brute-force empirical values (Section 2.5d) |
| `decomposition_theorem_position_level.py` / `.log` | fresh position-level reduced model verifying the Decomposition Theorem's bookkeeping identity and joint independence/uniformity claims, `K=1..5` (Section 3.2) |
| `conditional_cdf_general_k_demo.py` / `.log` | bonus: demonstrates the algorithmic route to a general-K conditional CDF (Section 4) |
| `monte_carlo_bonus.py` / `.log` | large-`(n,K)` Monte Carlo triangulation, reserved seeds (Section 6) |

---

## 8. Seeds

Reserved range: `20260924000`–`20260924999` (this front's own, per
`DISC-DEC-110`). Grep-confirmed unused before this front's first use:
```
$ grep -rn "20260924" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7329:      atual desta linha. Seeds 20260924000-20260924999.
```
(re-confirmed after this front's own files were created: only the
governance reservation line and this front's own files reference the
range — no other file in the archive does).

Only `monte_carlo_bonus.py` uses randomness (`numpy.random.default_rng`,
one explicit seed per configuration, no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `algebraic_identity_check.py` | none (symbolic/exact) | crux algebraic identity |
| `no_cycle_probability_general_m.py` | none (symbolic/exact enumeration) | `R(B)=q_B` |
| `proposition_s_general_k.py` | none (symbolic/exact enumeration) | Proposition S |
| `true_bruteforce_definition4_general_k.py` | none (exhaustive) | true Definition-4 ground truth |
| `unconditional_prop_s_vs_bruteforce.py` | none (exact) | unconditional Proposition S check |
| `decomposition_theorem_position_level.py` | none (exact enumeration) | Decomposition Theorem, position level |
| `conditional_cdf_general_k_demo.py` | none (exact enumeration) | bonus CDF-machinery demonstration |
| `monte_carlo_bonus.py` | `20260924001`–`20260924006` | Section 6 large-`(n,K)` triangulation |

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Key Lemma: `R(B)=q_B` for every finite `B`, any weights | **PROVED** (Section 2.3, new) |
| 2 | Proposition S, general `K`: `P(S=A)=|A|!prod_A p_a(p_D+sum_A p_a)` | **PROVED** (Section 2.4, new, main result) |
| 3 | Proposition S recovers Estagio 40's four K=3 formulas as one | **PROVED** (Section 2.4) |
| 4 | Full Cycle-Count Decomposition Theorem, general `K` | **PROVED** (Section 3, main result) |
| 5 | Algorithmic route to the general-K conditional CDF | **PROVED** as a working algorithm for any concrete `K` (Section 4), verified `K=2,3,4` |
| 6 | Single closed-form-in-`(n,K)` unconditional CDF | **NOT ATTEMPTED** beyond Section 4's demo, correctly out of primary scope (Section 5.1) |
| 7 | Rate/moment coefficient patterns in `K` | **NOT ATTEMPTED** (Section 5.2) |
| 8 | `K -> infinity` asymptotics | **NOT ATTEMPTED** (Section 5.3) |

---

## 10. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run. No `.py` file from any
other front (this lineage or any ancestor/sibling) was read, opened, or
imported — every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the cited `ATTEMPT.md` documents
only. Every claim above is labeled PROVED / OPEN / NOT ATTEMPTED at the
point of use; no claim is left as an unlabeled assertion, and every bug
caught during this front's own work (Sections 2.5, 6) is disclosed rather
than silently corrected. All randomized verification used only the
reserved seed range `20260924000`–`20260924999`. No claim of progress on
any Millennium Problem; this is pure combinatorial mathematics internal to
the u12 ensemble defined in `THEOREM.md`.
