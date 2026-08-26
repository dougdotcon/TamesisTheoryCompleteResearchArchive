# Pushing the case-split method to K=3: an exact closed form for `P_nn(n,3)` via a governing-source reduction and a cycle-predecessor simplification

**Front:** Wave 20, front (b), `K3-JOINT-STRUCTURAL-ATTEMPT`, `DISC-DEC-088`.
Pure combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a
Millennium Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260892000`–`20260892999` (this front's own; grep-confirmed
unused before first use, see §9). No edits made to `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
`PROOF_DEPENDENCY_MAP.md`, `README.md`, or `index.html`. No `adversarial/`
subdirectory created here, no referee dispatched by this front, no git
command run. All work confined to this new subdirectory. **No `.py` file
from any other front (this lineage or any ancestor/sibling) was opened,
read, or imported anywhere** — every script in this directory is written
fresh from the mathematical prose of `THEOREM.md` and the predecessor's
`ATTEMPT.md`, per the mandate's hard constraint.

---

## Executive summary (read first)

**The exact K=3 target, restated precisely.** Estágio 31 (the predecessor
front, `k2_joint_case_split_attempt`) closed `P_nn(n,2)` — the probability
that two specific query points, disjoint from `K` reroute sources, are
*both* cyclic for the rerouted function `f` of Definition 4 — and diagnosed
`K=3` as structurally harder: with 3 reroute sources, the permutation's
cycle structure is cut into 3 arcs, and each of the 3 sources' reroute
targets `U_0,U_1,U_2` independently lands in one of `K{+}1=4` destinations
(its own arc, either of the other two arcs, or outside) — a `4^3=64`-cell
table, but the genuinely new difficulty named was that *which points end up
cyclic now depends on the functional graph of which arc's tail feeds into
which other arc* (a chain can pass through an intermediate arc before
closing), not a flat `3\times3` table as at `K=2`. This front's mandate was
to attempt exactly this: generalize the K=2 case-split (Lemma 1 + Lemma 2 +
Proposition NN2) to `K=3`, i.e. compute `P_{nn}(n,3)` exactly.

**What this document proves, unconditionally, all independently verified
by fresh brute-force enumeration (own scripts, no code read from any other
front) and by two internally-independent implementations of the reduced
model itself:**

1. **A governing-source reindexing corollary of Lemma 1 (§2, PROVED, new,
   elementary).** The predecessor's own Marked-Point Gap Structure Lemma
   (Lemma 1, general `m`, PROVED there, cited by statement and re-verified
   fresh here at `m=3`) gives mark-indexed arc lengths independent of
   topology `\sigma`. This front adds: by exchangeability of the gap
   vector and independence of `\sigma`, the *governing-source*-indexed arc
   lengths `L_s` (the arc whose *tail* is source `s`, i.e. whose
   continuation `U_s` controls) have the **same** uniform-over-compositions
   law, **also independent of `\sigma`** — so topology can be marginalized
   out of the whole `K=3` computation entirely. This is the first new
   simplification, and it is what makes the `4^3=64`-cell table tractable
   at all.
2. **The Three-Source Redirect-Structure Lemma (§3, PROVED, new):** the
   `K{=}3` generalization of the predecessor's Lemma 2. The key new fact
   (Lemma 4, §3.2) resolving the diagnosed difficulty: an arc's own cyclic
   point-set depends **only** on whichever incoming source is part of the
   *actual returning cycle* of the 3-node functional graph on
   `\{0,1,2\}\to\{0,1,2,\mathrm{DEAD}\}` — any *other* source that happens
   to also target that arc (extra in-degree, always possible with 3
   sources and only 2 "other" arcs) is provably irrelevant to that arc's
   cyclic set. This collapses the `64`-case table into closed-form
   **linear** (single-point) and **bilinear** (cross-arc pair) rules in the
   query positions — structurally simpler than the raw case count
   suggested, and is the resolution of Estágio 31's own diagnosis, not a
   side-step of it.
3. **Proposition NN3 (main result, PROVED):**
   `\displaystyle P_{nn}(n,3) = \frac{35n^3+38n^2+23n+6}{140n^3} =
   \frac14+\frac{19}{70n}+\frac{23}{140n^2}+\frac3{70n^3}`, for every
   `n\ge6`. Derived by a **full exact symbolic derivation** (`sympy`, exact
   `Rational` arithmetic throughout, triple closed-form summation over all
   compositions `(L_0,L_1,L_2)`, no floating point at any stage) —
   matching, to the last digit, a numeric closed-form fit independently
   obtained from the same reduced model at 15+ separate values of `n`
   (`n=6,\ldots,25,30`) — and independently confirmed by fresh brute-force
   enumeration of Definition 4's *entire* K=3 model at `n=6,7,8,9`
   (`4/4` exact rational matches, including a brand-new `n=9` data point,
   `264{,}539{,}520` exact configurations, `96` seconds of exhaustive
   computation).
4. **Corollary NN3.1 (PROVED, closes Estágio 27's named K=3 item, second
   moment):** `P_{nn}(n,3)\to\tfrac14=\tfrac1{K+1}\big|_{K=3}`, so by Lemma
   P2 (`distributional_bridge_attempt` §6.2, PROVED for **general** `K`,
   cited), `E[(M_n^{(3)})^2]\to\tfrac14=E[M_3^2]` (Estágio 18, an
   incondicional anchor there for `K\le3`).
5. **Corollary NN3.2 (PROVED, K=3 closure of the continuum transfer):** by
   Theorem J's Corollary (Estágio 25, cited, PROVED there, exact at every
   finite `n,K`), `P_{nn\text{-same}}(n,3):=\tfrac12P_{nn}(n,3) =
   \frac{35n^3+38n^2+23n+6}{280n^3}\to\frac18=\frac1{2(K{+}1)}\Big|_{K=3}`
   — extending Estágio 28's `K=0,1` and Estágio 31's `K=2` continuum
   same-cycle transfer theorem `P(\text{same}\mid K\text{ marks})=
   1/(2(K{+}1))` to `K=3`.
6. **The full CDF at K=3, and target (iii) (the general joint two-point
   law): NOT attempted**, precisely as at K=2 — see §8. A large-`n` Monte
   Carlo triangulation (own reserved seeds) is reported as a bonus, not a
   substitute for the exact results above.

**Net verdict.** `K=3` of the case-split method is **closed for the
scalar second-moment / same-cycle targets** — the exact analogue of what
the predecessor closed at `K=2` — by a genuinely new mechanism (governing-
source reindexing + cycle-predecessor reduction) that directly resolves
the structural obstruction Estágio 31 diagnosed (the 3-arc functional
graph), rather than working around it. The **full CDF** at K=3 and the
**general** joint two-point law (any `K`) remain honestly open, precisely
scoped in §8 — full closure of those was never in scope for a single
front, and is not claimed. No claim of progress on any Millennium
Problem; pure internal combinatorics on this archive's own
random-permutation-with-reroutes ensemble.

---

## 1. Reading discipline and target

### 1.1 What was read (prose only, per mandate)

`THEOREM.md`: Estágio 18 (the joint-two-point obstruction, K≤3
method-of-moments anchor `E[M_K^2]=1/(K{+}1)` for `K\le3`); Estágio 25
(Theorem J, Restrição Cíclica Uniforme, and its Corollary
`P(\text{same}\mid\text{both cyclic})=\tfrac12` exactly at every finite
`n,K`); Estágio 27 (the distributional bridge: Proposition D0, Lemma R,
Proposition D1 at K=1, Lemma P2's general-K second-moment reduction to
`P_{nn}(n,K)`, and the explicit "K≥2 open" diagnosis); Estágio 28 (the
continuum Theorem J transfer: Proposition R's reduction,
`P(\text{same}\mid K\text{ marks})=1/(2(K{+}1))` proved at `K=0,1`); and
Estágio 31 in full (the Marked-Point Gap Structure Lemma, the Two-Source
Redirect-Structure Lemma, Proposition NN2, Corollary NN2.2, and — the
target of this front — the precise diagnosis of why `K=3` is structurally
harder: the functional-graph-on-arcs obstruction named in the executive
summary above).

Full prose (not scripts) of the predecessor's own `ATTEMPT.md`
(`k2_joint_case_split_attempt`), in full, as required by the mandate: its
notation (§1.3), Lemma 1 statement and proof (§2), Lemma 2 statement and
proof (§3), Proposition NN2's derivation (§4), Corollaries NN2.1–NN2.3
(§5–6), and, most importantly, its own §7.1 diagnosis of `K=3` — the exact
passage this front's mandate targets. **No `.py` file from this front, any
ancestor front, or any sibling front was opened, read, or imported
anywhere in this document's derivation** — every script below is written
fresh from the mathematical descriptions above.

### 1.2 Notation (extending the predecessor's, `THEOREM.md` Definition 4)

`\pi` a uniform random permutation of `[n]`. `K=3` reroute sources fixed
WLOG at `\{0,1,2\}` (Definition 4's exchangeability argument, cited).
Targets `U_0,U_1,U_2` i.i.d. `\mathrm{Unif}([n])`, independent of `\pi`.
`f(i):=U_i` for `i\in\{0,1,2\}`, `f(i):=\pi(i)` otherwise. Query points
fixed WLOG at `\{n{-}2,n{-}1\}` (distinct from the sources, requiring
`n\ge5` arithmetically; this document verifies at `n\ge6` for a safety
margin matching the predecessor's own convention). Define

`P_{nn}(n,3) := P(n{-}2,\,n{-}1\text{ both cyclic for }f)`

— exactly Lemma P2's `P_{nn}(n,K)` at `K=3`, and exactly the predecessor's
own `P_{nn}` convention (query points strictly disjoint from the reroute
sources), so that Lemma P2 (cited, general-`K`, PROVED) applies directly
without any further reduction lemma needed.

---

## 2. The governing-source reindexing corollary of Lemma 1 (PROVED, new)

### 2.1 Lemma 1, cited (predecessor, general `m`, PROVED)

> **Lemma 1 (Marked-Point Gap Structure, predecessor `ATTEMPT.md` §2,
> PROVED for general `m`, cited here at `m=3`).** For a uniform random
> permutation `\pi` of `[n]` and `m=3` marks `\{0,1,2\}`: the contracted
> permutation `\sigma` on `\{0,1,2\}` (`\sigma(s)` := first mark hit
> forward along `\pi` from `s`) is uniform on `S_3` (`6` equally likely
> topologies), and, **independently** of `\sigma`, the gap vector
> `(g(0),g(1),g(2),O)` — `g(m)` the number of unmarked points strictly
> between mark `m` and `\sigma(m)`, `O=n-3-\sum g(m)` the count of points
> in `\pi`-cycles touching no mark — is **uniform** over all compositions
> of `n-3` into `4` nonnegative parts (`\binom n3` of them).

Re-verified fresh, independently, at `m=3` (own script, no code read from
the predecessor): `gap_lemma_m3_unittest.py`, exhaustive enumeration of all
`n!` permutations, `n=4,\ldots,7`. Checks (a) `\sigma` uniform on `S_3`
(`6` topologies, equal counts); (b) `(g(0),g(1),g(2),O)` uniform over
`\binom n3` compositions, each cell exactly `6\cdot(n{-}3)!` (marginalizing
the `6` topologies, each contributing `(n{-}3)!` — Lemma 1's own proof
mechanism, re-derived and confirmed); (c) joint independence of `\sigma`
and the gap vector (every `(\sigma,\text{gap})` cell exactly `(n{-}3)!`).
**All checks pass, `n=4,5,6,7`, zero mismatches**
(`gap_lemma_m3_unittest.log`).

### 2.2 The new corollary: topology marginalizes out entirely (PROVED, elementary)

Write `a_m := g(m)+1` (mark-indexed arc length, including the tail
`\sigma(m)`). Define the **governing-source**-indexed arc length
`L_s := a_{\sigma^{-1}(s)}` — `ARC(s)` is, by definition, the arc whose
*tail* is source `s`, so `ARC(s)`'s continuation is controlled by `U_s`
(exactly the role `p,q` play in the predecessor's K=2 §3.1, made explicit
and generalized to 3 sources here).

> **Lemma (Governing-Source Reindexing, PROVED, new).** `(L_0,L_1,L_2,O)`
> is uniform over the **same** `\binom n3` compositions of `n-3` into 4
> nonnegative parts as `(a_0,a_1,a_2,O)`, and **independent of `\sigma`**.

*Proof.* `(a_0,a_1,a_2)` are exchangeable given `O`: the uniform-over-
compositions law is, by construction, invariant under permuting which of
the 3 "gap" coordinates is which (all three obey the identical constraint
`\ge1`, and the composition-counting argument in Lemma 1's own proof never
distinguishes them), so `(a_{\tau(0)},a_{\tau(1)},a_{\tau(2)})\overset d=
(a_0,a_1,a_2)` for any permutation `\tau` of `\{0,1,2\}`. Since
`L_s=a_{\sigma^{-1}(s)}`, and `\sigma` is independent of `(a_0,a_1,a_2,O)`
(Lemma 1), conditioning on `\sigma=\sigma_0` for any fixed `\sigma_0` gives
`(L_0,L_1,L_2)\mid\sigma{=}\sigma_0 \overset d= (a_0,a_1,a_2)` by
exchangeability — the **same** distribution for every `\sigma_0` — hence
unconditionally `(L_0,L_1,L_2,O)\overset d=(a_0,a_1,a_2,O)`, independent of
`\sigma`. `\blacksquare`

**Independent verification**: the same `gap_lemma_m3_unittest.py` computes
`L_s := g(\sigma^{-1}(s))+1` directly from the enumeration (not via the
proof above) and confirms its distribution, cell-by-cell, exactly equals
the mark-indexed gap distribution — `ok_governing_source_reindex_matches:
True` at every `n=4,\ldots,7` tested.

**Consequence.** Topology `\sigma` never needs to be tracked again: `ARC(s)`
has length `L_s`, `(L_0,L_1,L_2,O)` uniform over compositions of `n-3`,
independent of anything else — exactly mirroring the predecessor's own K=2
observation ("regardless of topology") but now derived as an explicit,
separately-stated corollary rather than left implicit, because at `K=3`
topology genuinely has 6 (not 2) values and the reduction is no longer a
one-line symmetry.

---

## 3. The Three-Source Redirect-Structure Lemma (PROVED, new)

### 3.1 Setup: three governing-source arcs, tails are the sources themselves

`ARC(s)` (`s=0,1,2`) has `L_s` total positions: `1,\ldots,L_s-1` interior
(non-source), `L_s` = source `s` itself (the tail). Interior edges are
un-rerouted `\pi`-edges (deterministic succession `i\to i{+}1`). Points
outside all three arcs (the `O=n-\sum L_s` "outside" points) are
**automatically cyclic** — their forward `f`-orbit never meets a reroute
source, exactly the K=1/K=2 fact, now with `O=n-L_0-L_1-L_2`. Query points,
disjoint from sources by construction, occupy interior positions
`1,\ldots,L_s-1` of some arc, or are outside.

Each source `t\in\{0,1,2\}` sends `U_t` to one of `n` equally likely slots:
`\mathrm{dest}(t)=t` ("home", lands in its own governed arc, `L_t` slots),
`\mathrm{dest}(t)=s\ne t` ("other", lands in `ARC(s)`, `L_s` slots), or
`\mathrm{dest}(t)=\mathrm{DEAD}` (lands outside, `O` slots) — `4` choices
per source, `4^3=64` total combinations, matching Estágio 31's own naming
of this exact obstruction ("um `4\times4\times4=64`-cell").

### 3.2 The cycle-predecessor reduction (Lemma 4, PROVED, new — this is the resolution of Estágio 31's diagnosis)

Fix a destination assignment `\mathrm{dest}:\{0,1,2\}\to\{0,1,2,\mathrm
{DEAD}\}` (one of the 64). Say source `s` is **cyclic** iff iterating
`\mathrm{dest}` from `s` returns to `s` before hitting `\mathrm{DEAD}`
(i.e. `s` lies on a fixed point, 2-cycle, or 3-cycle of `\mathrm{dest}`
restricted to `\{0,1,2\}`).

> **Lemma 4 (Cycle-Predecessor Uniqueness, PROVED).** If `s` is cyclic,
> there is a **unique** `t\in\{0,1,2\}` with `\mathrm{dest}(t)=s` **and**
> `t` itself cyclic — call it `\mathrm{pred}(s)` (possibly `t=s`, the
> "home" case). Moreover, `ARC(s)`'s cyclic point-set is **exactly**
> `\{k,\ldots,L_s\}`, where `k` is the position where
> `U_{\mathrm{pred}(s)}` actually landed within `ARC(s)` — **independent
> of any other source that may also target `ARC(s)`** (with `K{=}3` there
> is exactly one other candidate per arc besides its cycle-predecessor,
> and it is provably inert for this purpose).

*Proof.* Uniqueness of `\mathrm{pred}(s)`: since `\mathrm{dest}` has
out-degree exactly 1 per node, the sub-relation "`t\to\mathrm{dest}(t)`
restricted to cyclic nodes" is itself a permutation of the cyclic subset
(every cyclic node has exactly one cyclic predecessor and one cyclic
successor within its own cycle) — a standard functional-graph fact,
verified computationally without exception across all `64` cases
(`redirect_core_k3.py`'s `analyze_dest`, which asserts
`len(candidates)==1` at every cyclic `s` and never raised across the full
enumeration used throughout this document). For the second claim: a
non-cycle-forming incoming edge into `ARC(s)` (from some `t'\ne
\mathrm{pred}(s)` with `\mathrm{dest}(t')=s`, `t'` itself *not* cyclic)
lands at some position `k'`; the point at `k'` still has its own,
unaffected forward edge to `k'{+}1` (interior positions' edges never
depend on incoming edges — only on their own position, which is fixed by
the arc's linear structure) — so `t'`'s edge does not alter `ARC(s)`'s
*own* forward flow at all, only adds an extra (irrelevant, for cyclicity
purposes) predecessor to the functional graph at position `k'`. Hence the
cyclic set of `ARC(s)` is governed *solely* by the one incoming edge that
is part of the actual returning cycle. `\blacksquare`

**Independent verification, two layers:**

1. *(64-case correctness, no crash across the full state space.)*
   `redirect_core_k3.py` implements `analyze_dest` exactly as above and is
   called, across this document's entire derivation, at every one of the
   `64` combinations for dozens of `(n,L)` configurations — the internal
   `assert len(candidates)==1` never fails.
2. *(Position-level ground truth, fully independent implementation.)*
   `redirect_direct_check_k3.py` — built with **no reference to** the
   cycle-predecessor shortcut at all — literally enumerates all `n^3`
   `(U_0,U_1,U_2)` slot choices at the level of concrete abstract
   positions, constructs the resulting functional graph by hand
   position-by-position, and determines query-point cyclicity by direct
   graph traversal. Cross-checked against `redirect_core_k3.py`'s
   64-case-shortcut answer at `5` configurations, `6` query-pair types
   each (`n=10,L=(3,2,2)`; **all 6/6 exact matches**), then at `5`
   further configurations including edge cases (`L=(1,1,1)`, no interior
   positions at all) with up to `12` query pairs each — **all matches, no
   discrepancy found anywhere.**

### 3.3 Closed-form single-point and cross-arc formulas (PROVED, symbolic)

Because exactly one source is "constrained" (its landing position must be
`\le` the query position) in the single-point case, and exactly two
*distinct* sources are constrained in the cross-arc joint case (never the
same source twice, since `\mathrm{dest}` is single-valued and `s_1\ne
s_2`), every one of the `64` terms is **linear** in the query position(s)
— summed exactly, symbolically, in `sympy` (`symbolic_redirect_k3.py`):

> **Lemma 5 (PROVED, symbolic, `n,L_0,L_1,L_2` as `sympy` symbols,
> `sp.Rational` throughout — the K=3 analogue of the predecessor's
> Lemma 2 (R1)–(R5)).**
> `\displaystyle P(\text{pos. }i\text{ in }ARC(0)\text{ cyclic}) =
> \frac{i\,(2L_1L_2+L_1n+L_2n+n^2)}{n^3}`
> (symmetric under `0\leftrightarrow1\leftrightarrow2`, i.e. independent
> of `ARC(0)`'s **own** length `L_0` — exactly the same qualitative fact
> as the predecessor's (R1)/(R2), now with two "other" arcs contributing
> `2L_1L_2/n^3` in place of one).
>
> `\displaystyle P(\text{pos. }i\in ARC(0),\ i'\in ARC(1)\text{ both
> cyclic}) = \frac{2\,i\,i'\,(2L_2+n)}{n^3}`
> (symmetric under permuting the arc-pair label; depends only on the
> **third**, uninvolved arc's length `L_2` and `n` — exactly the K=2
> analogue `2ii'/n^2`, now with a `(2L_2+n)/n` correction factor coming
> from the extra possible "chain-through-the-third-arc" 3-cycle case that
> did not exist at `K=2`).
>
> Same-arc pairs (`i<i'`, same `ARC(s)`): `P(\text{both cyclic}) =
> P(\text{pos. }i\text{ cyclic})` — the nearer-to-tail point's own
> marginal
> **[Nota pós-adversarial, 2026-08-26 — DISC-DEC-092, sem correção — o
> referee hostil não encontrou nenhum erro matemático nesta frente.] O
> referee observou que este rótulo está invertido: pela própria
> convenção da §3.1 deste documento, a posição `L_s` (o índice máximo)
> é a cauda; para `i<i'` no mesmo arco, `i` (o índice menor, cujo
> marginal governa `P(\text{both cyclic})`) está MAIS LONGE da cauda,
> não mais perto. A fórmula em si e seu uso ao longo da montagem da §4
> estão corretos (re-verificados independentemente pelo referee, tanto
> simbolicamente quanto por enumeração exata) — apenas a frase
> descritiva está invertida. Classificado pelo referee como achado de
> severidade negligível/cosmética, do mesmo tipo de deslize de prosa já
> encontrado (e igualmente sem efeito em nenhuma prova) pelo referee da
> frente K=2 predecessora.]**, exactly generalizing the predecessor's (R3). **Verified
> computationally without exception**, `redirect_core_k3.py`, across `5`
> `(n,L)` configurations spanning `n=9,\ldots,15`, every interior
> `(k,k')` pair (`redirect_verify_same_arc` check, all match).

Each of these four formulas is independently cross-checked at concrete
`(n,L,i,i')` against the exhaustive-enumeration reduced model
(`redirect_core_k3.py`'s own numeric `Fraction` computation) — exact
agreement in all spot checks reported in §5.

---

## 4. Proposition NN3: the exact closed form (PROVED)

### 4.1 Assembly (the K=3 analogue of the predecessor's §4)

`T(L_0,L_1,L_2) :=` sum, over all ordered pairs of **distinct** "roles"
among the `n-3` non-source slots, of `P(\text{both roles cyclic})` — same
definition as the predecessor's `T(p,q)`, generalized to 4 role-types
(outside, and interior of each of 3 arcs). Using Lemma 5 (§3.3) for every
sub-term (OO, O–arc both orders, same-arc both orders via the monotone
fact, cross-arc both orders), `T(L_0,L_1,L_2)` is summed in closed form —
`assemble_pnn3.py`'s symbolic derivation (`symbolic_redirect_k3.py` +
exact `sympy.summation` over the interior-position ranges of each arc, no
approximation).

`\displaystyle P_{nn}(n,3) = \frac{1}{\binom n3}\sum_{\substack{L_0,L_1,L_2\ge1\\L_0+L_1+L_2\le n}}\frac{T(L_0,L_1,L_2)}{(n-3)(n-4)}`

— exactly the predecessor's own K=2 assembly formula (their §4), with
`\binom n2\to\binom n3` (Lemma 1 at `m=3`) and `(n{-}2)(n{-}3)\to(n{-}3)
(n{-}4)` (one more non-source slot to place the second query point among).

### 4.2 Full exact symbolic derivation (PROVED, no floating point)

`T(L_0,L_1,L_2)` was expanded fully symbolically (`sympy.expand`, exact
rationals), then the triple sum over the composition region was carried
out **symbolically, in closed form**, one variable at a time
(`sp.summation`, `L_2` first, then `L_1`, then `L_0`, each producing an
explicit polynomial-over-`n^k` intermediate — full expressions archived in
`symbolic_derivation_k3.py`'s run log):

> **Proposition NN3 (PROVED).** For every `n\ge6`:
> `\displaystyle P_{nn}(n,3) = \frac{35n^3+38n^2+23n+6}{140n^3} =
> \frac14+\frac{19}{70n}+\frac{23}{140n^2}+\frac3{70n^3}`.

*Derivation.* `symbolic_derivation_k3.py`: `T(L_0,L_1,L_2)` built exactly
as in §4.1 from the closed forms of §3.3 (via `symbolic_redirect_k3.py`);
summed exactly over `L_2=1,\ldots,n{-}L_0{-}L_1`, then `L_1=1,\ldots,
n{-}L_0{-}1`, then `L_0=1,\ldots,n{-}2`; divided by
`\binom n3\cdot(n{-}3)(n{-}4)`; simplified (`sp.simplify`+`sp.factor`) —
the stated closed form emerges directly, with **zero** residual terms and
**zero** hand simplification. `\blacksquare`

**Corollary NN3.0 (rate, PROVED, immediate).** `n(P_{nn}(n,3)-\tfrac14)\to
\tfrac{19}{70}` — an exact `\Theta(1/n)` rate, continuing the pattern
already on record: K=1 rate `\tfrac16` (`P_{nn}(n,1)=\tfrac12+\tfrac1{6n}`,
Estágio 27), K=2 rate `\tfrac7{30}` (Proposition NN2), K=3 rate
`\tfrac{19}{70}` here.

### 4.3 Independent verification (exact brute force, `n=6,\ldots,9`)

Fresh, from-scratch, full enumeration of the *entire* Definition 4 K=3
model (`brute_force_k3.py` — every one of the `n!\cdot n^3`
`(\pi,U_0,U_1,U_2)` configurations, exact `Fraction` counting, **no code
read from any other front, no reduced-model shortcut of any kind used**):

| `n` | configs (`n!\cdot n^3`) | `P_{nn}(n,3)` (brute force) | Proposition NN3 predicts | match | elapsed |
|---|---|---|---|---|---|
| 6 | 155,520 | `3/10` | `3/10` | ✓ | 0.05s |
| 7 | 1,728,720 | `7017/24010` | `7017/24010` | ✓ | 0.6s |
| 8 | 20,643,840 | `10271/35840` | `10271/35840` | ✓ | 6.8s |
| 9 | 264,539,520 | `4801/17010` | `4801/17010` | ✓ | 96.5s |

**`4/4` exact rational matches.** `n=9` (`264.5` million exact
configurations, exhaustive, no sampling) is the largest ground-truth check
in this front's own computation, and the first true full-brute-force
verification of any K=3 joint-two-point quantity anywhere in this lineage
(`brute_force_k3.log`).

### 4.4 Independent verification (reduced model, `n=6,\ldots,30`)

The reduced model (§2–3, `assemble_pnn3.py`) — which does **not** rely on
Proposition NN3's own closed form, only on the case-split machinery of
§2–3 — was run independently at `n=6,\ldots,25` (every value) and
`n=30,40` (spot checks beyond the fitting range used to first notice the
closed form): **every single value matches Proposition NN3's closed form
exactly**, `20/20` for the full `n=6,\ldots,25` range plus both the `n=30`
and `n=40` spot checks (full timings in `assemble_pnn3.log`; `n=40` alone
takes several minutes, reflecting the reduced model's polynomial — not
exponential — growth, still dramatically faster than true brute force
would be at that `n`). This closes the loop: (a)
the reduced model matches TRUE brute force at `n=6,\ldots,9` (§4.3); (b)
the reduced model matches the fully independent symbolic derivation
(§4.2) at every `n` tested, `n=6,\ldots,30`; (c) the symbolic derivation
was obtained by a *closed-form, exact* triple summation, not curve-fitting
— the numeric fit (over `n=6,\ldots,9`, degree-`\le3` polynomial
hypothesis in `n^3\cdot P_{nn}(n,3)`) was used only to **notice** the
pattern before the symbolic derivation confirmed it exactly, and is
reported for narrative honesty in §4.5, not as the proof itself.

### 4.5 How the closed form was found (narrative honesty)

Before attempting the full symbolic triple sum, this front first computed
`P_{nn}(n,3)` numerically (exact `Fraction`, reduced model) at
`n=6,\ldots,15`, noticed the values were consistent with `n^3P_{nn}(n,3)`
being a degree-`\le3` polynomial in `n`, fit that polynomial exactly from
4 points (`n=6,\ldots,9`, `sympy.interpolate`, exact rationals), and
verified it against the **remaining** `6` already-computed points
(`n=10,\ldots,15`) — `6/6` exact matches, a very strong signal before any
symbolic derivation was attempted. The subsequent full symbolic triple sum
(§4.2) then **independently reproduced the identical polynomial** by a
completely different route (case-by-case exact algebra, not
interpolation) — this is the actual proof; the numeric fit was the
heuristic that motivated attempting it.

---

## 5. Corollary NN3.1: closes Estágio 27's/18's K=3 second-moment item (PROVED)

`THEOREM.md` Estágio 27 (Lemma P2, cited, PROVED for general `K`) reduces
`E[(M_n^{(K)})^2]\to\lim_nP_{nn}(n,K)`, whenever the limit exists, for any
fixed `K` (the `P_{nr},P_{rr}`-weighted terms are `O(K/n)\to0`). Estágio 18
already established `E[M_K^2]=1/(K{+}1)` unconditionally for `K\le3` (the
continuum anchor, via the already-proved conditional densities `1/2,1/3,
1/4`).

> **Corollary NN3.1 (PROVED).** `P_{nn}(n,3)\to\tfrac14=\tfrac1{K+1}
> \big|_{K=3}`, so `E[(M_n^{(3)})^2]\to\tfrac14=E[M_3^2]` — the K=3
> instance of the distributional bridge's second-moment convergence,
> matching the *already-proved* continuum value exactly.

---

## 6. Corollary NN3.2: K=3 closure of the continuum same-cycle transfer (PROVED)

Theorem J's Corollary (Estágio 25, cited, PROVED there, exact at every
finite `n,K`, for any fixed distinct `i,j\in[n]`, proof never assumes
`i,j\notin R`): applied with `i,j=n{-}2,n{-}1` (this document's own
`P_{nn}` query pair, always disjoint from the K=3 reroute sources by
construction),

`P_{nn\text{-same}}(n,3) := P_n^{(3)}(n{-}2,n{-}1\text{ both cyclic, same
final cycle}) = \tfrac12P_{nn}(n,3) = \frac{35n^3+38n^2+23n+6}{280n^3}`,

exactly, for every `n\ge6` — no new probability needed beyond Proposition
NN3 and the cited Corollary. Hence:

> **Corollary NN3.2 (PROVED).**
> `\displaystyle P_{nn\text{-same}}(n,3) \to \frac18 = \frac1{2(K{+}1)}
> \Big|_{K=3}`.

This extends Estágio 28's `K=0,1` (`1/2,1/4`) and Estágio 31's `K=2`
(`1/6`) continuum same-cycle transfer theorem to `K=3` (`1/8`) — the
pattern `1/(2(K{+}1))` now confirmed exactly at `K=0,1,2,3`.

---

## 7. Large-`n` Monte Carlo triangulation (bonus, not a substitute for §4)

`monte_carlo_k3.py`, reserved seeds `20260892001`–`20260892003`, direct
simulation of Definition 4's K=3 model (own random permutations and
targets, **not** the reduced model — an independent simulation path):

| `n` | trials | `\hat P(\text{both cyclic})` | s.e. | `z` vs `1/4` | `\hat P(\text{same cycle})` | s.e. | `z` vs `1/8` |
|---|---|---|---|---|---|---|---|
| 200 | 200,000 | 0.25132 | 0.00097 | +1.36 | 0.12538 | 0.00074 | +0.52 |
| 2,000 | 30,000 | 0.25580 | 0.00252 | +2.30 | 0.12883 | 0.00193 | +1.98 |
| 5,000 | 10,000 | 0.25380 | 0.00435 | +0.87 | 0.12680 | 0.00333 | +0.54 |

All triangulation cells land within a few standard errors of the exact
targets `1/4,1/8` proved in §4–6 — consistent, not itself proof (the exact
brute force of §4.3 and the exact symbolic derivation of §4.2 are the
actual evidence; this is triangulation only, per lineage convention).

---

## 8. What did NOT close, precisely (honest, as mandated)

### 8.1 The full CDF at K=3 (Proposition D1's whole-distribution generalization)

Proposition NN3 gives only the **second moment** contribution (`P(\text{two
specific points both cyclic})`), not the full law of
`T=\#\{\text{cyclic points}\}` among the 3 arcs. Proposition D1
(`distributional_bridge_attempt`, K=1) obtained the *entire* CDF in closed
form by tracking a single arc's case split directly on the count, not just
pairwise. Lemma 4/Lemma 5 here (§3) are genuine tools toward a K=3 version
(they give the exact pairwise joint law for *any* two positions across the
3-arc structure, and the cycle-predecessor reduction that makes the 64-case
table tractable at all), but assembling a *full* count distribution needs
the entire correlation structure (all `\binom{L_0+L_1+L_2}2` pairs
simultaneously, or an inclusion–exclusion/generating-function argument
over subsets of a 3-arc structure) — not attempted here, precisely because
it is a strictly harder, separately well-posed target, exactly as the
predecessor scoped it at K=2.

### 8.2 Target (iii): the general joint two-point law (any K)

Not attacked directly. The governing-source reindexing (§2) and the
cycle-predecessor reduction (§3, Lemma 4) are **general mechanisms** — they
were stated and proved for `K=3` here, but nothing in the *proof* of
Lemma 4 is specific to exactly 3 sources; it is a fact about functional
graphs on any finite node set with an absorbing DEAD state. This suggests
(a genuine, precisely-scoped hint, **not** a claim) that the same two-step
reduction (marginalize topology via exchangeability; reduce a `(K{+}1)^K`-
cell destination table to per-arc linear/bilinear rules via the unique-
cycle-predecessor fact) might generalize to arbitrary `K`. This document
does **not** attempt that generalization — deriving the general-`K`
closed-form single-point/cross-arc rules (Lemma 5's K=3 instance) and the
resulting `K`-fold symbolic composition sum is a substantially larger
undertaking than the K=3 instance solved here, and is reported only as a
named, well-posed direction for a future front, not as progress on it.

### 8.3 What is explicitly NOT claimed

No claim that Proposition NN3 extends past K=3 as stated (only the
*method* is flagged, in §8.2, as plausibly generalizable — untested). No
claim about any moment beyond the second. No claim about the rate of
convergence of any alternative finite-`n` convention (e.g. Estágio 28's own
overlap-allowed convention, analogous to the predecessor's Lemma 3 at
K=2) — not attempted at K=3 here, though the same one-line
Overlap-Reduction argument (predecessor's Lemma 3, general-`K`, PROVED,
cited) already guarantees it converges to the same limit `1/4,1/8` without
any further work needed, since Lemma 3 was stated and proved for general
`K` there. No claim of any kind about a Millennium Problem.

---

## 9. Seeds

Reserved range: `20260892000`–`20260892999` (this front's own). Grep-
confirmed unused before this front's first use (only governance
reservation lines in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` predate this
front's own files):

```
$ grep -rn "20260892" 05_DISCOVERY_LAB/
```

Only `monte_carlo_k3.py` uses randomness (`numpy.random.default_rng` seeded
via `numpy.random.SeedSequence`, explicitly per cell, no shared/reused
seed):

| script | seed(s) | purpose |
|---|---|---|
| `brute_force_k3.py` | none (exhaustive) | ground truth, `n=6..9` |
| `gap_lemma_m3_unittest.py` | none (exhaustive) | Lemma 1 at m=3 + reindexing corollary |
| `redirect_core_k3.py` | none (exact enumeration over 64 cases) | reduced model core |
| `redirect_direct_check_k3.py` | none (exhaustive) | independent position-level cross-check |
| `symbolic_redirect_k3.py` | none (symbolic) | closed-form P_single/P_joint |
| `assemble_pnn3.py` | none (exact) | T(L) assembly, numeric P_nn(n,3) |
| `symbolic_derivation_k3.py` | none (symbolic) | full closed-form Proposition NN3 derivation |
| `monte_carlo_k3.py` | `20260892001`, `20260892002`, `20260892003` | §7 large-n triangulation |

---

## 10. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `brute_force_k3.py` / `.log` | true ground-truth exhaustive Definition-4 K=3 enumeration, `n=6..9` |
| `gap_lemma_m3_unittest.py` | fresh Lemma 1 (m=3) + governing-source reindexing corollary verification |
| `redirect_core_k3.py` | Three-Source Redirect-Structure reduced model (numeric, exact `Fraction`) |
| `redirect_direct_check_k3.py` | independent position-level cross-check of the 64-case reduction |
| `symbolic_redirect_k3.py` | symbolic closed forms for P_single, P_joint (Lemma 5) |
| `assemble_pnn3.py` | numeric assembly of `T(L)` and `P_nn(n,3)`, `n=6..30` |
| `symbolic_derivation_k3.py` | full symbolic triple-sum derivation of Proposition NN3 |
| `monte_carlo_k3.py` / `.log` | large-n Monte Carlo triangulation, reserved seeds |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Lemma 1 at m=3 (cited, re-verified fresh) | **PROVED** (cited + re-verified) |
| 2 | Governing-Source Reindexing corollary (topology marginalizes out) | **PROVED** (new) |
| 3 | Lemma 4 (Cycle-Predecessor Uniqueness — resolves Estágio 31's obstruction) | **PROVED** (new) |
| 4 | Lemma 5 (closed-form single-point / cross-arc rules) | **PROVED** (new, symbolic) |
| 5 | Proposition NN3 (`P_{nn}(n,3)=(35n^3+38n^2+23n+6)/(140n^3)`) | **PROVED** |
| 6 | Corollary NN3.0 (rate `\Theta(1/n)`, coefficient `19/70`) | **PROVED** |
| 7 | Corollary NN3.1 (`E[(M_n^{(3)})^2]\to1/4`, closes Estágio 27/18's K=3 2nd-moment item) | **PROVED** |
| 8 | Corollary NN3.2 (`P_{nn\text{-same}}(n,3)\to1/8`, K=3 continuum transfer) | **PROVED** |
| 9 | Full CDF of `M_n^{(3)}` (Proposition D1-style, K=3) | **OPEN** (precisely scoped, §8.1) |
| 10 | Target (iii), general joint two-point law (any K) | **OPEN** (method flagged as plausibly generalizable, §8.2 — not attempted) |
| 11 | Rate/closed form of the overlap-allowed convention at K=3 | **OPEN** (limit only, via cited general-K Lemma 3; rate not attempted) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No git command run. No `.py` file from any other
front (this lineage or any ancestor/sibling) was read, opened, or
imported — every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the predecessor's `ATTEMPT.md`
description only. Every claim above is labeled PROVED / OPEN at the point
of use; no claim is left as an unlabeled assertion. All randomized
verification used only the reserved seed range `20260892000`–
`20260892999`. No claim of progress on any Millennium Problem; this is
pure combinatorial mathematics internal to the u12 ensemble defined in
`THEOREM.md`.
