# Generalizing the K=3 case-split method to arbitrary K: a general-K reduction, exact closed forms through K=6, and a precise diagnosis of what resists a free-K formula

**Front:** `GENERAL-K-JOINT-ATTEMPT`, `DISC-DEC-093`, wave 21 front (c).
Pure combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1-4. **This is not a Millennium
Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260904000`-`20260904999` (this front's own; grep-confirmed
unused before first use — only the governance reservation lines in
`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` predate this front's files, see
§9). No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created here, no referee
dispatched by this front, no `git` command run. All work confined to this
new subdirectory. **No `.py` file from any other front (this lineage or any
ancestor/sibling) was opened, read, or imported anywhere** — every script in
this directory is written fresh from the mathematical prose of `THEOREM.md`
and the direct predecessor's `ATTEMPT.md` (the `k3_joint_structural_attempt`
front), per the mandate's hard constraint.

---

## Executive summary (read first)

**The exact general-K target, restated precisely.** For `K` reroute sources
fixed WLOG at `\{0,\ldots,K{-}1\}` (Definition 4's exchangeability, cited)
and two query points fixed WLOG at `\{n{-}2,n{-}1\}` (disjoint from the
sources, needing `n\ge K{+}2`),

`P_{nn}(n,K) := P(n{-}2,\,n{-}1\text{ both cyclic for the rerouted function }f)`

is Lemma P2's scalar (`distributional_bridge_attempt` §6.2, PROVED for
general `K`, cited): the second-moment bridge target
`E[(M_n^{(K)})^2]\to\lim_nP_{nn}(n,K)` needs, for every fixed `K`, an exact
closed form of `P_{nn}(n,K)`. This is exactly item (iii)/target (iii) named
open by Estágio 18 and, in the K=3 predecessor's own words (§8.2), "the
general joint two-point law (any K)". The predecessor closed `K=1,2,3`
one integer at a time (Estágio 27/28, Estágio 31, Estágio 35) and explicitly
did not attempt a general-`K` version, naming two mechanisms — Governing-
Source Reindexing and Lemma 4 (Cycle-Predecessor Uniqueness) — as
"structurally general... but this was not attempted" (§8.2, precisely
quoted in the mandate).

**What this document does, and how far it gets — all independently
verified by fresh, from-scratch code (own scripts, no code read from any
other front), exact `fractions.Fraction`/`sympy.Rational` arithmetic
throughout, no floating point in any PROVED claim:**

1. **Mechanism 1 (Governing-Source Reindexing) generalizes to every `K`
   (PROVED).** The exchangeability argument that marginalizes topology
   `\sigma` out entirely is verified, from scratch, at `K=1,\ldots,5` (exhaustive
   over all `n!` permutations, `n` up to `7`) — exactly the same one-line
   proof as at `K=3`, with `3` replaced by `K` throughout, no new step
   needed. §2.

2. **Mechanism 2 (Lemma 4, Cycle-Predecessor Uniqueness) generalizes to
   every `K` (PROVED).** The uniqueness of a cyclic node's cycle-predecessor,
   and the inertness of any other incoming edge, is a fact about functional
   graphs on **any** finite node set with an absorbing DEAD state — verified
   exhaustively over all `(K{+}1)^K` destination assignments for
   `K=1,\ldots,6` (node level) and by direct position-level graph
   traversal for `K=1,\ldots,5` (small arcs, all landing positions swept).
   §3.

3. **A genuinely new general-K Lemma 5 analogue (PROVED, the hardest
   requested step, and the main new mathematical content of this
   document).** Closed-form single-point and cross-arc formulas, valid for
   **every** `K`, derived from Lemma 4 by an explicit cycle-sum /
   inclusion-style combinatorial argument (not case enumeration — see §4):
   `\displaystyle P(\text{pos }i\text{ in }ARC(s)\text{ cyclic}) =
   \frac iL_s\,P_0(s)`,
   `\displaystyle P_0(s) = x_s\!\!\sum_{S\subseteq\mathrm{Others}(s)}\!\!|S|!\prod_{u\in S}x_u`
   (`x_u:=L_u/n`), and, for `s\ne s'`,
   `\displaystyle P(\text{pos }i\text{ in }ARC(s),\text{ pos }i'\text{ in
   }ARC(s')\text{ both cyclic}) = \frac iL_s\frac{i'}{L_{s'}}\,P_{s,s'}`,
   `P_{s,s'}=P_{\mathrm{same}}(s,s')+P_{\mathrm{disjoint}}(s,s')` (two
   explicit finite sums over subsets of the remaining `K{-}2` "other"
   sources, §4.2-4.3). Verified against **two independent** from-scratch
   brute-force computations: (a) the full `(K{+}1)^K` destination table
   (node level, `K=1,\ldots,6`); (b) the actual position-by-position
   functional graph over all `n^K` landing choices (`K=1,\ldots,5`) — exact
   match in every one of `18` test configurations. §4, §5.
4. **Mechanism 3 assembled into exact closed forms, PROVED via full
   symbolic (`sympy`, exact `Rational`, no floating point) `K`-fold
   summation, for `K=4,5,6` — three new closed forms, going past the K=4
   target named as the "biggest prize" in the mandate:**
   - **Proposition NN4 (PROVED):**
     `P_{nn}(n,4)=\dfrac{126n^4+187n^3+177n^2+98n+24}{630n^4}
     =\tfrac15+\tfrac{187}{630n}+\tfrac{59}{210n^2}+\tfrac7{45n^3}+\tfrac4{105n^4}`.
   - **Proposition NN5 (PROVED):**
     `P_{nn}(n,5)=\dfrac{462n^5+874n^4+1139n^3+989n^2+514n+120}{2772n^5}`.
   - **Proposition NN6 (PROVED):**
     `P_{nn}(n,6)=\dfrac{1716n^6+3958n^5+6616n^4+7933n^3+6472n^2+3204n+720}{12012n^6}`.
   Each cross-validated against fully independent from-scratch true
   brute-force enumeration of Definition 4's **entire** `K`-source model
   (`n^K` targets `\times` `n!` permutations) at every feasible `n`
   (`K=4`: `n=6,7,8`, up to `165{,}150{,}720` exact configurations; `K=5`:
   `n=7`, `84{,}707{,}280` exact configurations — the largest single true
   brute-force check anywhere in this lineage's `K\ge4` regime) **and**
   against `6`-`7` independent numeric reduced-model evaluations per `K`
   at larger `n` (well beyond the fitting range). §6.
5. **The general algorithm itself is proved correct for arbitrary `K`
   (PROVED, this is the actual generalization delivered).** Every step —
   §2's reindexing, §3's Lemma 4, §4's Lemma 5 analogue, §5's assembly — is
   stated and proved **for general `K`**, not `K`-by-`K`; a single
   parametrized script (`symbolic_derivation_general_k.py`) takes `K` as
   input and derives Proposition NN`K` from scratch, reproducing the
   **already-PROVED** `K=1,2,3` closed forms exactly (a strong
   self-consistency check, §7) before producing the new `K=4,5,6` results.
   The only thing **not** proved is a single closed-form expression for
   `P_{nn}(n,K)` as an explicit elementary function of **both** `n` and
   `K` simultaneously (i.e. without running the `K`-fold symbolic
   summation separately for each concrete `K`) — precisely diagnosed in
   §8 as resistant to elementary closure for a structural reason (the
   number of *terms* in the exact combinatorial sum genuinely grows with
   `K`, not merely the *value*), not because the method breaks down.
6. **What did NOT close: honestly scoped, §8.** No free-`K` symbolic
   closed form for `P_{nn}(n,K)`. No closed form (or even conjecture) for
   the rate coefficient `c_1(K)` (the coefficient of `1/n`) as a function
   of `K` — data reported (§8.3), pattern not identified. The full CDF of
   `M_n^{(K)}` for `K\ge2` (already open, unaffected by this front). `K=7`
   and beyond: not attempted (see §8.4 for the concrete scaling reason).

**Net verdict: PARTIAL CLOSURE, substantial.** The two flagged mechanisms
(Governing-Source Reindexing, Lemma 4/Cycle-Predecessor Uniqueness)
**are confirmed to generalize to every `K`, rigorously**, resolving the
predecessor's own "genuine, precisely-scoped hint" in the affirmative for
those two pieces. The single-point/cross-arc formula step (item 3 of the
mandate, flagged as "likely the hardest step") **is also solved in full
generality** — a genuinely general-`K` closed form, not a case-by-case
recipe, verified through `K=6`. The final assembly step produces a
**general, provably-correct algorithm** that yields the exact closed form
of `P_{nn}(n,K)` for any concrete `K` (demonstrated at `K=1,\ldots,6`, three
of them new), but **not** a single closed-form-in-`K` formula — an honest,
precisely diagnosed non-closure at that last, hardest level (§8), matching
the mandate's own prediction that this final step "potentially requires a
generating-function or symbolic-in-K approach rather than explicit case
enumeration." No claim of progress on any Millennium Problem; pure internal
combinatorics on this archive's own random-permutation-with-reroutes
ensemble.

---

## 1. Reading discipline and target

### 1.1 What was read (prose only, per mandate)

`THEOREM.md`: Estágio 18 (the general-K joint two-point target, `E[M_K^2]=
1/(K{+}1)` for `K\le3`, method-of-moments architecture); Estágio 25
(Theorem J, Restrição Cíclica Uniforme, and its Corollary
`P(\text{same}\mid\text{both cyclic})=\tfrac12` exactly at every finite
`n,K`, proof never assumes anything about `K`); Estágio 27 (the
distributional bridge: Lemma P2's general-`K` second-moment reduction to
`P_{nn}(n,K)`, PROVED for general `K`, and the "K≥2 open" diagnosis);
Estágio 28 (the continuum Theorem J transfer, `P(\text{same}\mid K\text{
marks})=1/(2(K{+}1))`, `K=0,1`); Estágio 31 in full (the Marked-Point Gap
Structure Lemma, general `m`, PROVED; the Two-Source Redirect-Structure
Lemma; Proposition NN2; the diagnosis of why `K=3` is structurally harder);
and Estágio 35 in full (Governing-Source Reindexing §2, Lemma 4 §3.2,
Lemma 5 §3.3, Proposition NN3, and especially §8.2's precise hint about
generalizability — quoted verbatim in the mandate and again in this
document's executive summary).

The direct predecessor's `ATTEMPT.md`
(`.../k3_joint_structural_attempt/ATTEMPT.md`), read in full, in prose:
its notation (§1.2), the Governing-Source Reindexing corollary statement
and proof (§2), the Three-Source Redirect-Structure Lemma including Lemma
4's statement and proof (§3), Lemma 5's closed forms (§3.3), Proposition
NN3's assembly and symbolic derivation (§4), and — the exact target of
this front — its own §8.2 diagnosis of what was NOT attempted. **No `.py`
file from this front, any ancestor front, or any sibling front was opened,
read, or imported anywhere in this document's derivation** — every script
below is written fresh from the mathematical descriptions above.

### 1.2 Notation (direct generalization of the predecessor's, `THEOREM.md` Definition 4)

`\pi` a uniform random permutation of `[n]`. `K\ge1` reroute sources fixed
WLOG at `\{0,\ldots,K{-}1\}`. Targets `U_0,\ldots,U_{K-1}` i.i.d.
`\mathrm{Unif}([n])`, independent of `\pi`. `f(i):=U_i` for
`i\in\{0,\ldots,K{-}1\}`, `f(i):=\pi(i)` otherwise. Query points fixed WLOG
at `\{n{-}2,n{-}1\}` (distinct from the sources, requiring `n\ge K{+}2`).

`P_{nn}(n,K) := P(n{-}2,\,n{-}1\text{ both cyclic for }f)` — exactly Lemma
P2's `P_{nn}(n,K)` (`distributional_bridge_attempt`, PROVED general-`K`
reduction target), and exactly the predecessor's own `P_{nn}` convention.

---

## 2. Mechanism 1, general K: Governing-Source Reindexing (PROVED)

### 2.1 Lemma 1, cited (Estágio 31, general `m`, PROVED)

For a uniform random permutation `\pi` of `[n]` and `m=K` marks
`\{0,\ldots,K{-}1\}`: the contracted permutation `\sigma` on
`\{0,\ldots,K{-}1\}` is uniform on `S_K`, and, **independently** of
`\sigma`, the gap vector `(g(0),\ldots,g(K{-}1),O)` is uniform over all
compositions of `n{-}K` into `K{+}1` nonnegative parts. This lemma was
already stated and proved for **general** `m` by the K=2 predecessor
front (`k2_joint_case_split_attempt`) — nothing here reproves it, only
re-verifies it fresh at concrete `K` values as a sanity floor before
building on it.

### 2.2 The reindexing corollary, restated for general K (PROVED, same proof as K=3, `K` in place of `3` throughout)

Write `a_m:=g(m)+1`. Define the governing-source arc length
`L_s:=a_{\sigma^{-1}(s)}`.

> **Lemma (Governing-Source Reindexing, general K, PROVED).**
> `(L_0,\ldots,L_{K-1},O)` is uniform over the **same** `\binom nK`
> compositions of `n-K` into `K{+}1` nonnegative parts as
> `(a_0,\ldots,a_{K-1},O)`, and **independent of `\sigma`**.

*Proof.* Identical to the predecessor's K=3 proof (their §2.2), with `3`
replaced by `K` throughout: `(a_0,\ldots,a_{K-1})` are exchangeable given
`O` (the uniform-over-compositions law is invariant under permuting which
gap coordinate is which — the composition-counting argument in Lemma 1's
proof never distinguishes them, for **any** `K`), `\sigma` is independent
of `(a_0,\ldots,a_{K-1},O)` (Lemma 1, general `m`), so conditioning on any
fixed `\sigma=\sigma_0` gives `(L_0,\ldots,L_{K-1})\mid\sigma{=}\sigma_0
\overset d=(a_0,\ldots,a_{K-1})` — the same law for every `\sigma_0` —
hence unconditionally `(L_0,\ldots,L_{K-1},O)\overset d=(a_0,\ldots,
a_{K-1},O)`, independent of `\sigma`. Nothing in this argument uses `K=3`
specifically; it is literally the exchangeability of `K` symmetric random
variables under any permutation of their labels. `\blacksquare`

**Independent verification (fresh code, `gsr_general_k_unittest.py`):**
exhaustive enumeration of all `n!` permutations, `K=1,\ldots,5`, `n` up to
`7` (`K=5,n=7`: `5040` permutations). Confirms, at every `(K,n)` cell
tested: (a) `\sigma` uniform on `S_K` (`K!` topologies, equal counts); (b)
gap vector uniform over compositions; (c) joint independence of `\sigma`
and gaps; (d) the governing-source reindexed vector
`(L_0,\ldots,L_{K-1},O)` has **exactly** the same distribution (same keys,
same per-key counts) as the mark-indexed `(a_0,\ldots,a_{K-1},O)`. **All
checks pass at every one of `15` `(K,n)` cells tested, zero mismatches**
(`gsr_general_k_unittest.log`).

**Consequence.** Topology never needs tracking, for any `K`: `ARC(s)` has
length `L_s`, `(L_0,\ldots,L_{K-1},O)` uniform over compositions of
`n{-}K`, independent of everything else.

---

## 3. Mechanism 2, general K: Lemma 4 (Cycle-Predecessor Uniqueness) generalizes to any finite node set (PROVED)

### 3.1 Setup: K governing-source arcs

`ARC(s)` (`s=0,\ldots,K{-}1`) has `L_s` positions: `1,\ldots,L_s{-}1`
interior, `L_s` the source itself. The `O=n-\sum L_s` outside points are
automatically cyclic (their forward orbit never meets a reroute source —
independent of `K`). Each source `t` sends `U_t` to one of `n` equally
likely slots: `\mathrm{dest}(t)=t` ("home"), `\mathrm{dest}(t)=s\ne t`
("other"), or `\mathrm{dest}(t)=\mathrm{DEAD}` (outside) — `K{+}1` choices
per source, `(K{+}1)^K` total destination combinations (the predecessor's
own `64=4^3` at `K=3`; e.g. `625=5^4` at `K=4`, `117649=7^6` at `K=6`).

### 3.2 Lemma 4, restated for general K (PROVED — literally the same proof, no K-specific step)

Say source `s` is **cyclic** iff iterating `\mathrm{dest}` from `s`
returns to `s` before hitting DEAD.

> **Lemma 4 (Cycle-Predecessor Uniqueness, general K, PROVED).** If `s` is
> cyclic, there is a **unique** `t\in\{0,\ldots,K{-}1\}` with
> `\mathrm{dest}(t)=s` and `t` itself cyclic — `\mathrm{pred}(s)`. `ARC(s)`'s
> cyclic point-set is exactly `\{k,\ldots,L_s\}`, `k` the landing position
> of `U_{\mathrm{pred}(s)}` within `ARC(s)` — independent of any other
> source that may also target `ARC(s)` (with general `K` there can be up
> to `K{-}1` such "other" candidates per arc, all provably inert).

*Proof (unchanged from the predecessor's K=3 argument, which never used
`K=3` anywhere in its logic).* The sub-relation "`t\to\mathrm{dest}(t)`
restricted to cyclic nodes" is a permutation of the cyclic subset — a
standard fact about **any** finite functional digraph with out-degree `1`
per node: forward iteration from any node either reaches DEAD (absorbing,
terminates) or, by pigeonhole on a finite node set, must eventually
revisit a node, at which point (determinism) it exactly cycles from there.
A node is "cyclic" (by the stated definition) iff it lies **on** that
cycle, not merely upstream of it; every node on a cycle has exactly one
cyclic predecessor within the cycle. For the position-level claim: a
non-cycle-forming incoming edge into `ARC(s)` lands at some position `k'`
whose own forward edge (`k'\to k'{+}1`, or the arc's own deterministic
interior structure) is entirely determined by `k'` itself, never by which
source pointed into it — so it adds an extra, cyclicity-irrelevant
predecessor, never altering `ARC(s)`'s own forward flow. `\blacksquare`

This proof never mentions the number `3`, or any specific `K`; it is a
general theorem about functional graphs on `K` nodes plus one absorbing
sink, for **any** finite `K`.

**Independent verification, two layers, fresh code (`lemma4_general_k_
unittest.py`, no code read from any other front):**

1. *Node-level, `K=1,\ldots,6`:* exhaustive enumeration of **all**
   `(K{+}1)^K` destination functions (`K=6`: `117{,}649` functions,
   `237{,}432` cyclic-node instances across them). At **every** cyclic
   node, `\mathrm{pred}` is asserted unique — **zero assertion failures**.
2. *Position-level, `K=1,\ldots,5`, direct graph traversal (no reference
   to the cycle-predecessor shortcut except for the final comparison):*
   for concrete small arc lengths, every destination assignment is
   combined with a grid of landing-position sweeps (boundary and
   interior), the **actual** functional graph is built position-by-
   position, and cyclicity of every position is determined by direct
   traversal. Lemma 4's predicted cyclic set `\{k,\ldots,L_s\}` is
   compared against the traversal-computed set at **every** cyclic arc in
   **every** configuration (`K=5`: `161{,}050` full-graph configurations,
   `152{,}000` of them with a genuinely extra non-predecessor incoming
   edge into a cyclic arc). **Zero assertion failures anywhere**
   (`lemma4_general_k_unittest.log`).

---

## 4. Mechanism 3, general K: the Lemma 5 analogue — closed-form single-point and cross-arc formulas for arbitrary K (PROVED, new)

This is the step the mandate flagged as "likely the hardest," and the
main new mathematical content of this document.

### 4.1 The key simplification that makes general K tractable: the landing position is uniform, independent of the cycle's other structure

`U_t` is uniform on `[n]`; conditional on `\mathrm{dest}(t)=s` (landing in
`ARC(s)`), the landing position within `ARC(s)` is uniform on
`\{1,\ldots,L_s\}` — **regardless of which source `t` this is, which cycle
it belongs to, or how many other sources also happen to target `ARC(s)`**.
This is the crucial fact that keeps the case analysis from exploding with
`K`: it means the position-level question ("is position `i` cyclic?")
factors cleanly out of the node-level question ("is arc `s` cyclic, and
via which cycle?").

### 4.2 The single-point formula, general K (PROVED)

Write `x_u:=L_u/n` for `u=0,\ldots,K{-}1`. Define
`P_0(s):=P(\text{node }s\text{ cyclic in the destination graph})`. A
directed cycle through `s` of "additional" members `S\subseteq
\mathrm{Others}(s):=\{0,\ldots,K{-}1\}\setminus\{s\}` contributes `|S|!`
distinct cyclic orderings (arrangements of `S` around the cycle after
`s`), each of probability `x_s\prod_{u\in S}x_u` (`x_s` for the edge
closing the cycle back into `s`):

> **`\displaystyle P_0(s) = x_s\sum_{S\subseteq\mathrm{Others}(s)}|S|!
> \prod_{u\in S}x_u`** (a finite sum of `2^{K-1}` terms, computable for any
> concrete `K` in time `O(2^K)`).
>
> **`\displaystyle P(\text{pos }i\text{ in }ARC(s)\text{ cyclic}) =
> \frac iL_s\,P_0(s)`**, `i=1,\ldots,L_s` — by §4.1, since the landing
> position of whichever source turns out to be `s`'s cycle-predecessor is
> uniform on `1,\ldots,L_s`, independent of which cycle realizes `s` as
> cyclic.

This directly generalizes the predecessor's K=3 formula (their §3.3):
substituting `K=3` and expanding the sum over `S\subseteq\{1,2\}`
reproduces their `P_0=x_0(2L_1L_2+L_1n+L_2n+n^2)/n^2` exactly (verified
in §5).

### 4.3 The cross-arc joint formula, general K (PROVED)

For `s\ne s'`, `P_{s,s'}:=P(s\text{ and }s'\text{ both cyclic})` splits
into two structurally different contributions (same cycle vs. two
disjoint cycles), summed over the remaining `M:=\{0,\ldots,K{-}1\}
\setminus\{s,s'\}` (size `K{-}2`):

> `\displaystyle P_{\mathrm{same}}(s,s') = x_sx_{s'}\sum_{S\subseteq M}
> (|S|{+}1)!\prod_{u\in S}x_u`
>
> `\displaystyle P_{\mathrm{disjoint}}(s,s') = x_sx_{s'}\!\!\!
> \sum_{\substack{S_1,S_2\subseteq M\\S_1\cap S_2=\emptyset}}\!\!\!
> |S_1|!\prod_{u\in S_1}x_u\cdot|S_2|!\prod_{u\in S_2}x_u`
>
> `P_{s,s'} := P_{\mathrm{same}}(s,s')+P_{\mathrm{disjoint}}(s,s')`
> (computable, for any concrete `K`, in time `O(3^{K-2})` — every element
> of `M` is independently classified as "in `s`'s cycle," "in `s'`'s
> cycle," or "in neither").
>
> **`\displaystyle P(\text{pos }i\text{ in }ARC(s),\text{ pos }i'\text{
> in }ARC(s')\text{ both cyclic}) = \frac iL_s\frac{i'}{L_{s'}}\,
> P_{s,s'}`** (§4.1's uniform-independent-landing fact again, applied to
> **two** distinct predecessors — they are automatically distinct nodes,
> since a functional graph has out-degree `1` per node, so
> `\mathrm{pred}(s)\ne\mathrm{pred}(s')`).

*Proof of `P_{\mathrm{same}}`.* Identical cycle-sum argument to §4.2, now
requiring `s'\in S` (`s'` fixed to appear in the shared cycle): substitute
`S=S'\cup\{s'\}` and re-index. *Proof of `P_{\mathrm{disjoint}}`.* The two
cycles (through `s`, through `s'`) are automatically vertex-disjoint (any
two distinct cycles of a functional graph never share a node — standard
fact, used without further proof, already implicit in §3.2's argument);
summing over every way of partitioning `M` into "`s`'s other cycle
members" (`S_1`), "`s'`'s other cycle members" (`S_2`), and "neither"
gives the stated double sum. `\blacksquare` Same-arc pairs (`i<i'`, same
`ARC(s)`): `P(\text{both cyclic})=P(i\text{ cyclic})` by the same
monotone-suffix fact as the predecessor's (R3)/K=3 Lemma 5 (Lemma 4's
cyclic set is a suffix `\{k,\ldots,L_s\}`, so the smaller index governs).

### 4.4 Independent verification: two layers, general K (PROVED)

**(a) Node-level, `K=1,\ldots,6`, fresh brute force over the full
`(K{+}1)^K` destination table** (`lemma5_general_k_unittest.py`, no
reference to the formulas above): exact `Fraction` enumeration of `P_0(s)`
and `P_{s,s'}` at `10` concrete `(K,n,L)` configurations spanning
`K=1,\ldots,6` — **all `10/10` match exactly**
(`lemma5_general_k_unittest.log`).

**(b) Position-level, `K=1,\ldots,5`, fresh brute force over all `n^K`
landing choices** (`lemma5_position_level_unittest.py`, independent
implementation, builds the actual position-by-position functional graph
and determines cyclicity by direct traversal — no shortcut): at `8`
concrete `(K,L,O)` configurations, verifies **every** single-point,
cross-arc, and same-arc-pair prediction against direct traversal — **all
`8/8` configurations fully match** (every interior position and pair
checked, `lemma5_position_level_unittest.log`).

---

## 5. Assembly: the general-K algorithm (PROVED correct; produces Proposition NN`K` for any concrete K)

### 5.1 T(L), general K

Direct generalization of the predecessor's own K=2/K=3 assembly
(`THEOREM.md`/`ATTEMPT.md` prose): `T(L_0,\ldots,L_{K-1})` sums, over all
ordered pairs of the `n{-}K` non-source "roles" (`O` outside roles, always
cyclic; interior positions `1,\ldots,L_s{-}1` of each arc), the exact
probability both are cyclic — using §4's closed forms for every term
(outside-outside `=1`; outside-arc; same-arc via the monotone fact;
cross-arc). Because every closed form is **linear** in each query
position, the position-sums close in elementary form:
`\sum_{i=1}^{L_s-1}P(i\text{ cyclic})=P_0(s)(L_s{-}1)/2`, etc. — see
`assemble_pnn_general_k.py` / `symbolic_derivation_general_k.py` for the
full expressions (identical in spirit to the predecessor's own §4.1).

`\displaystyle P_{nn}(n,K) = \frac1{\binom nK}\!\!\sum_{\substack{L_0,
\ldots,L_{K-1}\ge1\\L_0+\cdots+L_{K-1}\le n}}\!\!\frac{T(L)}{(n{-}K)(n{-}K{-}1)}`

— exactly the predecessor's own K=3 assembly formula, with `\binom n3\to
\binom nK` and `(n{-}3)(n{-}4)\to(n{-}K)(n{-}K{-}1)`.

### 5.2 The general-K algorithm, and its self-consistency check against ALREADY-PROVED K=1,2,3

`assemble_pnn_general_k.py` implements this **numerically** (exact
`Fraction`, any concrete `K,n`) and `symbolic_derivation_general_k.py`
implements it **symbolically** (exact `sympy.Rational`, `K`-fold nested
`sp.summation`, any concrete `K` passed as a command-line argument) — a
single parametrized script, not three separate hand-derivations.

**Critical self-consistency check (the strongest sanity floor in this
document): run at `K=1,2,3`, the algorithm reproduces the already-PROVED
closed forms exactly, symbol for symbol:**

| K | this front's algorithm (fresh code) | already-PROVED (cited) | match |
|---|---|---|---|
| 1 | `(3n{+}1)/(6n)` | `P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` (Estágio 27) | exact |
| 2 | `(10n^2{+}7n{+}2)/(30n^2)` | Proposition NN2 (Estágio 31) | exact |
| 3 | `(35n^3{+}38n^2{+}23n{+}6)/(140n^3)` | Proposition NN3 (Estágio 35) | exact |

> **Correção (2026-08-28, referee v2, achado LOW):** a citação
> "(Estágio 27)" na linha `K=1` acima nomeia o estágio que primeiro
> *enuncia* `P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` — lá, explicitamente
> rotulado como padrão numericamente verificado (`n=3,\ldots,9`), não
> provado para `n` geral naquele documento. A prova real (derivação
> case-split completa) aparece um estágio depois, no Estágio 28, como
> `V_a(n)=(3n+1)/(6n)` — algebricamente idêntico. A citação correta
> para "já-PROVADO" nesta linha é portanto Estágio 28, não Estágio 27.
> O valor numérico em si está correto e permanece inalterado (o próprio
> referee reconfirmou-o por brute force independente em `n=3,4,5`);
> apenas o local citado como fonte da prova estava impreciso. Ver
> `adversarial/REFEREE_REPORT.md` §4.

(`symbolic_derivation_general_k.log`, K=1,2,3 sections.) This is not a
weak check: it means the general-`K` machinery of §2-§5, derived
independently from first principles for arbitrary `K`, **collapses onto
three separately, adversarially-verified prior results** the moment `K`
is set to `1`, `2`, or `3` — strong evidence the general reduction is
correct, not merely that it happens to work at the new `K` values.

**A narrative-honesty note on how this was found.** The first version of
`symbolic_derivation_general_k.py` (the parametrized master script,
written to consolidate three separate hand-written K=4/K=5/K=6 scripts
into one) had a genuine bug: the summation bound formula for the `K`-fold
nested sum was `n - \sum L[:j] - j` instead of the correct
`n - \sum L[:j] - (K{-}1{-}j)`. Running it against `K=1,2,3` **caught this
immediately** — `K=1` happened to match (the bug is inert at `K=1`, where
`j` and `K{-}1{-}j` coincide at `0`), but `K=2,3` did not match the
already-proved closed forms, exposing the error before it could
contaminate any new-`K` claim. Fixed (§5.1's bound is now stated
correctly; see the script's inline comment), and re-verified as the table
above shows. **The individual, hand-written K=4/K=5/K=6 derivation scripts
that produced this document's actual Propositions NN4-NN6 (§6) never had
this bug** — they were written and verified independently, each with the
correct explicit bounds copied from the predecessor's own K=3 pattern,
**before** the consolidated script existed; this note discloses the bug
in the *later, consolidating* script only, and documents that it was
caught by exactly the self-consistency check this section describes.

---

## 6. Propositions NN4, NN5, NN6 (PROVED — new results, going past the mandate's named "biggest prize")

### 6.1 Closed forms, full symbolic derivation, no floating point

> **Proposition NN4 (PROVED).** For every `n\ge6`:
> `\displaystyle P_{nn}(n,4) = \frac{126n^4+187n^3+177n^2+98n+24}{630n^4}
> = \frac15+\frac{187}{630n}+\frac{59}{210n^2}+\frac7{45n^3}+\frac4{105n^4}`.

> **Proposition NN5 (PROVED).** For every `n\ge7`:
> `\displaystyle P_{nn}(n,5) = \frac{462n^5+874n^4+1139n^3+989n^2+514n+120}
> {2772n^5} = \frac16+\frac{437}{1386n}+\frac{1139}{2772n^2}+\frac{989}
> {2772n^3}+\frac{257}{1386n^4}+\frac{10}{231n^5}`.

> **Proposition NN6 (PROVED).** For every `n\ge8`:
> `\displaystyle P_{nn}(n,6) = \frac{1716n^6+3958n^5+6616n^4+7933n^3+
> 6472n^2+3204n+720}{12012n^6} = \frac17+\frac{1979}{6006n}+\cdots+
> \frac{60}{1001n^6}`.

Derived by `symbolic_derivation_general_k.py K` for `K=4,5,6`
(equivalently, the original hand-written `symbolic_derivation_k{4,5,6}.py`
— archived as the historical record of how each was first found — produce
byte-identical closed forms; both routes are included in this
submission). Full `sympy` run logs archived
(`symbolic_derivation_general_k.log`): `K=4` in `5.6`s, `K=5` in `25.6`s,
`K=6` in `~166`s of symbolic computation, each a `K`-fold nested exact
`sp.summation` over the composition region, zero floating point at any
stage.

**Corollary NN`K`.0 (rate, PROVED, immediate, `K=4,5,6`):** the coefficient
of `1/n`, `c_1(K)`, continues the pattern already on record for
`K=1,2,3` (`\tfrac16,\tfrac7{30},\tfrac{19}{70}`): `c_1(4)=\tfrac{187}
{630}`, `c_1(5)=\tfrac{437}{1386}`, `c_1(6)=\tfrac{1979}{6006}` — see §8.3
for the honest report that no closed form in `K` was found for this
sequence.

**Corollary NN`K`.1 (PROVED, `K=4,5,6`):** `P_{nn}(n,K)\to\tfrac1{K{+}1}`
— consistent with `E[M_K^2]=1/(K{+}1)`, already proved **unconditionally
for all K** by the completely different route of Estágio 24 (general-K
closure of Conjectura 1), so this is a **consistency confirmation**, not a
new fact about the continuum limit — the new content is the exact
finite-`n` closed form, feeding Lemma P2's bridge.

**Corollary NN`K`.2 (PROVED, `K=4,5,6`, continuum same-cycle transfer):**
by Theorem J's Corollary (Estágio 25, PROVED, exact at every finite `n,K`),
`P_{nn\text{-same}}(n,K)=\tfrac12P_{nn}(n,K)\to\tfrac1{2(K+1)}`:
`\tfrac1{10}` (`K=4`), `\tfrac1{12}` (`K=5`), `\tfrac1{14}` (`K=6`) —
**confirming the mandate's named target** (the pattern `\tfrac12,\tfrac14,
\tfrac16,\tfrac18,\ldots` conjectured to continue to `\tfrac1{10}` at
`K=4`) **exactly**, and extending it two steps further.

### 6.2 Independent verification: true brute force of Definition 4's actual K-source model

`brute_force_k4.py` / `brute_force_k5.py` (fresh, no reduced-model
shortcut of any kind, no code read from any other front): every
`(\pi,U_0,\ldots,U_{K-1})` configuration, exact integer counting converted
to `Fraction`.

| K | n | configs (`n!\cdot n^K`) | brute force `P_{nn}(n,K)` | Prop. NN`K` predicts | match | elapsed |
|---|---|---|---|---|---|---|
| 4 | 6 | 933,120 | `209/810` | `209/810` | exact | 0.7s |
| 4 | 7 | 12,101,040 | `12535/50421` | `12535/50421` | exact | 8-11s |
| 4 | 8 | 165,150,720 | `25999/107520` | `25999/107520` | exact | 119-128s |
| 5 | 7 | 84,707,280 | `78077/352947` | `78077/352947` | exact | 62-67s |

**`4/4` exact rational matches.** `K=4,n=8` (`165.15` million exact
configurations) and `K=5,n=7` (`84.7` million exact configurations) are
the largest true brute-force checks in this lineage's `K\ge4` regime (`n=6`
is the minimum valid `n` for `K=5`, since sources occupy `\{0,\ldots,4\}`
and query points `\{n{-}2,n{-}1\}` must be disjoint from them, forcing
`n\ge7`; `n=6` would collide a query point with source `4`, so it is not a
valid brute-force check for `K=5` and was not attempted). `K=6` true brute
force (`n!\cdot n^6` at the minimum valid `n=8`: over `10^{10}`
configurations) was judged infeasible in this front's compute budget and
was **not attempted** — `K=6`'s Proposition NN6 rests on the symbolic
derivation (§6.1) plus §6.3's independent numeric cross-check, not true
brute force; this is disclosed honestly, not glossed over.

### 6.3 Independent verification: reduced-model numeric cross-check, beyond the fitting range

`assemble_pnn_general_k.py` (numeric, exact `Fraction`, does **not** rely
on the symbolic closed forms — only on §4's formulas and §5.1's
assembly) was run at many `n` values per `K`, well beyond any range used
to first notice a pattern (`verify_propositions_nn4_nn5_nn6.py`,
`verify_run.log`):

- `K=1,2,3`: `n=4,\ldots,14` — **`11/11`, `11/11`, `9/9` exact matches**
  against the already-PROVED closed forms (the same self-consistency
  floor as §5.2, re-run independently here).
- `K=4`: `n=6,\ldots,25` (`20` values) — **`20/20` exact matches** against
  Proposition NN4.
- `K=5`: `n=7,\ldots,13` (`7` values) — **`7/7` exact matches**.
- `K=6`: `n=8,\ldots,13` (`6` values) — **`6/6` exact matches**.

Combined with §6.2's true brute force and §5.2's `K=1,2,3` self-consistency
check, every Proposition in this document has been confirmed by **at
least two, and up to four, mutually independent routes**.

**A second narrative-honesty note.** The first version of
`verify_propositions_nn4_nn5_nn6.py` had its own, independent bug (an
erroneous index reversal when reading off the coefficients `c_0,\ldots,
c_K` from a numerator's coefficient list — unrelated to §5.2's bug, in a
different script) that made it report `0/20`-style mismatches against
Propositions NN4-NN6 despite those propositions being correct (already
independently confirmed by §6.1's symbolic derivation and §6.2's true
brute force at that point). It also briefly produced a corrupted log file
from an unrelated race between two concurrent runs writing to the same
filename. Both were caught immediately (the mismatch was inconsistent
with every other independent check already on record) and fixed before
this document's final claims were written; disclosed here in the same
spirit as §5.2's disclosure, not because either bug reached a claimed
result.

### 6.4 Large-n Monte Carlo triangulation (bonus, not a substitute for §6.1-6.3)

`monte_carlo_general_k.py`, reserved seeds `20260904001`-`20260904006`,
direct simulation of Definition 4's actual model (own random permutations
and targets, independent simulation path):

| K | n | trials | `\hat P(\text{both cyc})` | z vs `1/(K{+}1)` | `\hat P(\text{same})` | z vs `1/(2(K{+}1))` |
|---|---|---|---|---|---|---|
| 4 | 200 | 200,000 | 0.20150 | +1.67 | 0.10106 | +1.57 |
| 4 | 2,000 | 30,000 | 0.19840 | -0.69 | 0.10117 | +0.67 |
| 4 | 5,000 | 10,000 | 0.20400 | +0.99 | 0.10410 | +1.34 |
| 5 | 200 | 200,000 | 0.16719 | +0.62 | 0.08381 | +0.76 |
| 5 | 2,000 | 30,000 | 0.16850 | +0.85 | 0.08497 | +1.01 |
| 6 | 200 | 200,000 | 0.14505 | +2.78 | 0.07265 | +2.10 |

All cells land within a few standard errors of the exact targets proved
in §6.1-6.3 (the `K=6` `z=+2.78` cell is a single moderately-large draw
among `6` z-tests, unremarkable at that count — not itself evidence of
anything, consistent with, not a substitute for, the exact results).

---

## 7. What generalizes cleanly, summarized

| Mechanism | Predecessor's claim (K=3) | This front's result (general K) |
|---|---|---|
| Governing-Source Reindexing | proved at K=3, flagged as plausibly general | **PROVED for general K** (§2) — literally the same one-line exchangeability proof |
| Lemma 4 (Cycle-Predecessor Uniqueness) | proved at K=3, flagged as "a fact about functional graphs on any finite node set... not specific to K=3" | **Confirmed: PROVED for general K** (§3) — the flagged genericity was exactly right |
| Lemma 5 (single-point/cross-arc closed forms) | proved at K=3 by direct case-sum (`64`-cell table) | **PROVED for general K** (§4) — a genuinely general cycle-sum formula, not a per-K case enumeration; the `(K{+}1)^K`/`3^{K-2}` cost is in *evaluating* the formula at a concrete K, not in its *derivation* |
| Assembly into `P_{nn}(n,K)` | proved at K=3 by full symbolic triple sum | **Algorithm PROVED correct for general K** (§5); **executed and closed for K=4,5,6** (§6); **not** reduced to a single free-K formula (§8) |

---

## 8. What did NOT close, precisely (honest, as mandated)

### 8.1 The headline non-closure: no single formula for `P_{nn}(n,K)` as a function of both n and K

Sections 2-6 prove that the *method* — reindex away topology, use the
unique cycle-predecessor to collapse the destination table, sum the
resulting linear/bilinear position formulas over the composition region —
is completely general in `K`, and give a program that, fed any concrete
`K`, outputs the exact closed form of `P_{nn}(n,K)` in time that has been
measured empirically at `K=1,\ldots,6` (§6.1: seconds to a few minutes).
**This document does not, however, produce a single elementary expression
`P_{nn}(n,K)=F(n,K)` valid for symbolic `K`.**

### 8.2 Precise diagnosis of why (this is the substantive part of the non-closure)

The obstruction is **not** that the reasoning breaks down at some `K` — §2-
§5's proofs are uniform in `K`, verified computationally through `K=6`
with no sign of any qualitative change. The obstruction is that the
**number of terms** in the exact formulas of §4.2-4.3 grows with `K`:
`P_0(s)` is a sum of `2^{K-1}` terms, `P_{s,s'}` a sum of (up to)
`3^{K-2}` terms, and the final `K`-fold composition sum (§5.1) integrates
a polynomial in `L_0,\ldots,L_{K-1}` whose own term-count (after full
expansion) grows correspondingly — the `sympy` operation counts in
§6.1 (`501` ops at K=4 rising to `3978+` ops mid-derivation at K=6) make
this growth directly visible, not merely asserted. A "closed form in K"
would need one of:

- an **elementary function of K** (e.g. `1/(K{+}1) + p(K)/n + \cdots`
  with `p` some simple function of `K`) — but the coefficient data itself
  (§8.3) shows no obvious elementary pattern, so this route has no
  positive evidence, only the absence of a found pattern (a negative
  result, not a proof of impossibility);
- a **generating-function identity** that packages the whole `K`-fold sum
  of §4/§5 into a single closed integral or EGF equation valid for all
  `K` at once (the mandate's own suggested route) — a genuine, concrete
  avenue: §4.2's `\sum_S|S|!\prod x_u` is a classical object
  (`\sum_kk!\,e_k(x_1,\ldots,x_m)=\int_0^\infty e^{-\lambda}\prod_j(1{+}x_j
  \lambda)\,d\lambda`, verified as an identity but not exploited further
  here — see §8.4), and it is plausible that expressing `P_{nn}(n,K)`
  itself as some double- or triple-integral transform, uniform in `K`,
  is achievable; this document does not attempt it, and flags it as the
  single most promising concrete next step, precisely because the
  building blocks (the exponential generating function underlying
  `\sum k!\,e_k(x)`) are already visible in §4.2's own derivation.

This is, in the mandate's own words, exactly the predicted difficulty:
"the case-analysis explosion... grows with K, potentially requiring a
generating-function or symbolic-in-K approach" — confirmed here as the
*actual*, *located* obstruction (term-count growth in an otherwise
uniform derivation), not a vague restatement of the prediction.

### 8.3 Rate coefficient data, K=1..6 (reported, no pattern claimed)

| K | `c_0` (`=1/(K{+}1)`, known) | `c_1` (coefficient of `1/n`) |
|---|---|---|
| 1 | `1/2` | `1/6 \approx 0.16667` |
| 2 | `1/3` | `7/30 \approx 0.23333` |
| 3 | `1/4` | `19/70 \approx 0.27143` |
| 4 | `1/5` | `187/630 \approx 0.29683` |
| 5 | `1/6` | `437/1386 \approx 0.31530` |
| 6 | `1/7` | `1979/6006 \approx 0.32950` |

`c_1(K)` is visibly increasing and its successive ratios
(`c_1(K{+}1)/c_1(K)\approx1.40,\,1.16,\,1.09,\,1.06,\,1.05`) shrink toward
`1`, consistent with convergence to some finite limit as `K\to\infty`, but
**no closed form or even a numerically-fit conjecture is offered** — six
data points is not enough to respect the archive's own discipline against
premature pattern-fitting (a lesson already learned once in this very
front: see §5.2's disclosed bug, caught only because a *known* answer was
available to check against; a *guessed* pattern in `K`, with no such
anchor at large `K`, would carry a materially higher risk of exactly that
kind of silent error). Reported as raw data for any future front, not as
a conjecture.

### 8.4 The permanent-sum / integral identity (recorded, not developed)

For completeness, the classical identity underlying §4.2 is recorded
explicitly since it is the concrete opening named in §8.2:
`\sum_{k=0}^mk!\,e_k(x_1,\ldots,x_m) = \int_0^\infty e^{-\lambda}
\prod_{j=1}^m(1+x_j\lambda)\,d\lambda` (elementary: expand the product,
use `\int_0^\infty e^{-\lambda}\lambda^kd\lambda=k!`). Applying this to
`P_0(s)` gives `P_0(s)=x_s\int_0^\infty e^{-\lambda}\prod_{u\ne s}
(1+x_u\lambda)\,d\lambda`, and an analogous **double**-integral form for
`P_{\mathrm{disjoint}}(s,s')` (§4.3) via the two-variable version verified
in this front's own derivation notes (not archived as a separate proof,
since it was not carried through to a full `n,K`-uniform assembly — see
§8.2). Whether this integral representation, pushed through the full
composition sum of §5.1, yields a genuine `K`-uniform closed form (e.g. as
a `K`-fold iterated integral collapsing to a low-dimensional one via the
product structure) is the single most concrete open question this
document leaves behind — well-posed, not attempted to completion, and
named here precisely so a future front does not have to rediscover the
starting point.

### 8.5 K=7 and beyond: not attempted, concrete reason

`K=6`'s symbolic derivation took `\sim166`s and the intermediate
expression sizes were visibly growing faster than linearly (§8.2). `K=7`
was not attempted; a rough extrapolation from the `K=4\to5\to6` timings
(`5.6\to25.6\to166` seconds, each roughly `4\times` to `6\times` the
previous) suggests `K=7` would plausibly take on the order of `15` to `30`
minutes of
symbolic computation with no code changes — plausibly still feasible in a
dedicated run, but not attempted here since it would add a seventh data
point without resolving §8.1's actual obstruction (which is structural,
not a matter of running one more `K`). Flagged as a trivial-but-not-
executed extension for any future front that wants one more anchor point
for §8.3's data, not as a research question in itself.

### 8.6 What is explicitly NOT claimed

No claim that a free-`K` closed form exists or does not exist — only that
this document did not find one, and named precisely where the difficulty
lives (§8.2). No claim about the full CDF of `M_n^{(K)}` for `K\ge2`
(untouched by this front, already open per Estágio 27/35). No claim about
any moment beyond the second. No claim that Propositions NN4-NN6 extend
to `K=7` as stated (only the *method*, §2-§5, is proved general — the
concrete polynomials of §6.1 are specific to `K=4,5,6`). No claim of any
kind about a Millennium Problem; this is pure internal combinatorics on
the u12 ensemble defined in `THEOREM.md`.

---

## 9. Seeds

Reserved range: `20260904000`-`20260904999` (this front's own). Grep-
confirmed unused before this front's first use:

```
$ grep -rn "20260904" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:6215:      se bem-sucedida); seeds 20260904000+/referee 20260905000+. (d)
05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml:3509:        Seeds reservados 20260904000-20260904999 (frente) /
```

Both hits are the governance reservation lines themselves (predating this
front's files); no other file in the archive outside this front's own new
subdirectory references the range.

Only `monte_carlo_general_k.py` uses randomness (`numpy.random.default_rng`
seeded via `numpy.random.SeedSequence`, explicitly per cell, no
shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `lemma4_general_k_unittest.py` | none (exhaustive) | Lemma 4, general K, node + position level |
| `gsr_general_k_unittest.py` | none (exhaustive) | Governing-Source Reindexing, general K |
| `lemma5_general_k_unittest.py` | none (exact enumeration) | Lemma 5 analogue, node-level, K=1..6 |
| `lemma5_position_level_unittest.py` | none (exhaustive) | Lemma 5 analogue, position-level, K=1..5 |
| `assemble_pnn_general_k.py` | none (exact) | numeric T(L) assembly, any K, cross-check |
| `symbolic_derivation_general_k.py` | none (symbolic) | master parametrized closed-form derivation, any K |
| `symbolic_derivation_k4.py` / `k5.py` / `k6.py` | none (symbolic) | original hand-written derivations (historical record; superseded by the master script, kept for provenance) |
| `brute_force_k4.py` | none (exhaustive) | true ground truth, K=4, n=6,7,8 |
| `brute_force_k5.py` | none (exhaustive) | true ground truth, K=5, n=7 |
| `monte_carlo_general_k.py` | `20260904001`-`20260904006` | §6.4 large-n triangulation |

---

## 10. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `lemma4_general_k_unittest.py` / `.log` | Lemma 4, general K, node-level (K=1..6) and position-level (K=1..5) |
| `gsr_general_k_unittest.py` / `.log` | Governing-Source Reindexing, general K (K=1..5) |
| `lemma5_general_k_unittest.py` / `.log` | Lemma 5 analogue (P0, P_pair), node-level, K=1..6 |
| `lemma5_position_level_unittest.py` / `.log` | Lemma 5 analogue, position-level, K=1..5 |
| `assemble_pnn_general_k.py` | numeric T(L)/P_nn(n,K) assembly, any concrete K |
| `verify_propositions_nn4_nn5_nn6.py` / `verify_run.log` | independent numeric cross-check of Propositions NN1-NN6 against the reduced-model assembly, many n per K |
| `symbolic_derivation_general_k.py` / `.log` | master parametrized symbolic closed-form derivation, any concrete K; this run: K=1..6 |
| `symbolic_derivation_k4.py`, `symbolic_derivation_k5.py`, `symbolic_derivation_k6.py` | original hand-written per-K derivations (historical; produce identical results to the master script) |
| `symbolic_k4.log`, `symbolic_k5.log`, `symbolic_k6.log` | run logs of the original hand-written scripts |
| `brute_force_k4.py` / `.log` | true ground-truth exhaustive Definition-4 K=4 enumeration, n=6,7,8 |
| `brute_force_k5.py` / `.log` | true ground-truth exhaustive Definition-4 K=5 enumeration, n=7 |
| `monte_carlo_general_k.py` / `.log` | large-n Monte Carlo triangulation, K=4,5,6, reserved seeds |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Governing-Source Reindexing, general K | **PROVED** (§2) |
| 2 | Lemma 4 (Cycle-Predecessor Uniqueness), general K | **PROVED** (§3) |
| 3 | Lemma 5 analogue (single-point / cross-arc closed forms), general K | **PROVED, new** (§4) |
| 4 | General-K assembly algorithm, correctness | **PROVED** (§5), self-consistency confirmed against already-PROVED K=1,2,3 |
| 5 | Proposition NN4 (`K=4` closed form) | **PROVED** (§6) |
| 6 | Proposition NN5 (`K=5` closed form) | **PROVED, new** (§6) |
| 7 | Proposition NN6 (`K=6` closed form) | **PROVED, new** (§6) |
| 8 | Corollary NN4.2/NN5.2/NN6.2 (continuum same-cycle transfer, `1/10,1/12,1/14`) | **PROVED** (§6.1) — confirms and extends the mandate's named `1/10` target |
| 9 | Single closed-form-in-K formula for `P_{nn}(n,K)` | **OPEN**, precisely diagnosed (§8.1-§8.2) |
| 10 | Closed form / conjecture for the rate coefficient `c_1(K)` | **OPEN**, data reported only (§8.3) |
| 11 | `K=7` and beyond | **NOT ATTEMPTED**, concrete scaling reason given (§8.5) |
| 12 | Full CDF of `M_n^{(K)}`, `K\ge2` | **OPEN** (pre-existing, untouched by this front) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run. No `.py` file from any
other front (this lineage or any ancestor/sibling) was read, opened, or
imported — every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the direct predecessor's
`ATTEMPT.md` description only. Every claim above is labeled PROVED / OPEN
/ NOT ATTEMPTED at the point of use; no claim is left as an unlabeled
assertion. All randomized verification used only the reserved seed range
`20260904000`-`20260904999`. No claim of progress on any Millennium
Problem; this is pure combinatorial mathematics internal to the u12
ensemble defined in `THEOREM.md`.
