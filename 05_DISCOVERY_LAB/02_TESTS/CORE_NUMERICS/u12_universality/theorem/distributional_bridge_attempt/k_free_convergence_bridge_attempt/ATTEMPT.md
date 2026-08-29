# A K-free convergence-rate coupling for `F_n^{(K)}(x) -> F_K(x)`

**Front:** wave 26, front (a), `K-FREE-CONVERGENCE-BRIDGE-ATTEMPT`, authorized
by `DISC-DEC-123` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`).
Pure combinatorial mathematics about the u12 random-permutation-with-
reroutes ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a
Millennium Prize Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260933000`–`20260933999` (this front's own, per
`DISC-DEC-123`). Grep-confirmed unused before first use and re-confirmed at
the end — see Section 11. No edits made to `THEOREM.md`,
`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
`TEST_QUEUE.yaml`, `README.md`, or `index.html`. No `adversarial/`
subdirectory created here (a hostile referee is dispatched separately by the
orchestrating session). No `git` command run. Every `.py` file in this
directory was written completely fresh for this front — no script from any
ancestor or sibling front was opened, read, or imported.

---

## Executive summary (read first)

**The precise target (mandate, `DISC-DEC-123` frente (a)).** Lema R
(PROVED, `distributional_bridge_attempt/ATTEMPT.md` §3) reduces the full
distributional bridge `M_n(c)\to_d M(c)` to fixed-`K` CDF convergence
`F_n^{(K)}(x)\to F_K(x)` for every `K`. That convergence is established in
the archive so far only pointwise/case-by-case, via four increasingly
elaborate closed-form CDF derivations at `K=0,1` (Estágio 27), `K=2`
(Estágio 42), `K=3` (Estágio 40) and `K=4` (Estágio 43). This front's
mandate: attempt a single `K`-free argument giving an **explicit rate**
`\sup_x|F_n^{(K)}(x)-F_K(x)|\le h(K)/n`, built on the `K`-free machinery of
Estágio 41 (Proposição S general-`K`, the Full Cycle-Count Decomposition
Theorem `T=O+\sum_{s\in S}V_s`) — **not** by finding a fifth closed form.

**What this front does.** It builds an explicit continuum random variable
`M_K'` — the literal `n\to\infty` continuum limit of the Estágio-41
decomposition machinery itself (Dirichlet(1,…,1) arc-length simplex,
Proposição S applied with continuum weights, uniform within-arc landing
positions) — and constructs, from scratch, an explicit **coupling** between
the discrete `M_n^{(K)}` and `M_K'` on a common probability space, using
**only** already-PROVED `K`-free facts (Governing-Source Reindexing, the
i.i.d.-categorical-destinations fact, the landing-position-uniform fact,
Proposição S, the Decomposition Theorem — none re-derived) plus new,
elementary, `K`-free probability of this front's own (an exact
ceiling-discretization coupling, no concentration inequality of any kind).

**What closed (PROVED, unconditionally, `K`-free).**

> **Theorem A.** For every `K\ge0`, `n\ge K+1`, there is an explicit coupling
> of `M_n^{(K)}` and `M_K'` on a common probability space such that, off an
> event of probability at most `\delta(K,n):=(3K^2-K)/(2n)`,
> `|M_n^{(K)}-M_K'|\le\varepsilon(K,n):=(2K+1)/n` **deterministically**
> (Section 4). Consequently
> `\sup_x|F_n^{(K)}(x)-F_{M_K'}(x)|\le\delta(K,n)+\Lambda\cdot\varepsilon(K,n)`
> for any Lipschitz constant `\Lambda` of `F_{M_K'}`.

This is the piece of the mandate that closes completely and unconditionally
— a genuine `K`-free, explicit-rate coupling bound built directly from the
Estágio 41 machinery, exactly the kind of argument the mandate asked for.

**What did NOT close (honest, precisely diagnosed).** Theorem A bounds
`M_n^{(K)}` against **`M_K'`**, this front's own construction — not
directly against the archive's already-proved target `M_K` (density
`2Kx(1-x^2)^{K-1}`, Estágio 24). Closing the loop requires:

> **Claim B.** `M_K' \overset{d}{=} M_K`, i.e. `F_{M_K'}(x)=F_K(x)=1-(1-x^2)^K`.

Claim B is **PROVED exactly at `K=1`** (Section 5.1: `M_K'` reduces, term
for term, to `THEOREM.md` §5.3's independently-proved `K=1` construction).
For `K\ge2` it is **not proved** in this document. It is, however,
**exact-verified** — zero discrepancies, exact rational arithmetic, two
fully independent computational routes — for **every one of 35 cells**
(`K=1,\ldots,7`, moments `t=1,\ldots,5`, Section 5.2), and further supported
by Kolmogorov–Smirnov tests against the exact target CDF at `K` up to `20`
(Section 5.4) and by a genuine (if incomplete) piece of structural progress
toward a general proof — an exact closed form found and verified for the
key combinatorial weight `W(r,t)` at `t=1,2` (Section 5.3). Section 7 gives
the precise diagnosis of exactly what resists closure.

**Net verdict.** Substantial, genuinely `K`-free partial closure: an
unconditional, explicit-rate coupling theorem (Theorem A) reducing the
mandate's target to a single, precisely-isolated, exceptionally
well-evidenced (but not fully proved) distributional identity (Claim B).
Combining the two (Section 6) gives the mandate's exact requested form,
**conditional on Claim B**:

> **Main Theorem (conditional on Claim B).** For every `K\ge1`, `n\ge K+1`:
> `\sup_x|F_n^{(K)}(x)-F_K(x)| \le 8K^2/n`.

No claim of progress on any Millennium Problem; pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.

---

## 1. Reading discipline and provenance

**Read in full before any derivation.** `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`
entry `DISC-DEC-123` (the full three-front wave-26 authorization, including
what was rejected as redundant — the direct Conjecture-2 route, already
closed indirectly since Estágio 24; and a third Gosper-style certificate for
the general-`K` closed CDF, already twice independently certified
non-summable, Estágios 44/45). `THEOREM.md` §7 in full (the fixed-`K` bridge
machinery, the "Open Lemma" §7.4, Proposição Condicional 5 promoted to
Teorema 3 by Estágio 6 — the analogous **mean**-bridge closure, read for
context and as a consistency cross-check target, not reused as a proof
technique here since it goes through a different, EDO/Gronwall-based route
unrelated to the arc-decomposition machinery this front needs). `THEOREM.md`
§8 (Conjectures 1–2, and their promotion to PROVED at Estágio 24 — the
already-established target density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, all
`K\ge1`, and `F_K(x)=1-(1-x^2)^K`). `THEOREM.md` Estágio 27 in full (Lema R's
first statement and the `K=0,1` closure) and its own
`distributional_bridge_attempt/ATTEMPT.md` in full (exact definitions of
`M_n^{(K)}`, `F_n^{(K)}(x)`, `M(c)`, Lema R's precise statement and proof,
Proposition D0/D1, the Portmanteau reduction of §1). `THEOREM.md` Estágios
40, 42, 43 (the individual `K=2,3,4` closed-form CDF closures — read to
confirm this front does **not** replicate or extend that case-by-case
route). `THEOREM.md` Estágio 41 (the K-free announcement) **and, in full,
the standalone front it summarizes**,
`.../conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/k2_joint_case_split_attempt/k3_joint_structural_attempt/general_k_joint_attempt/general_k_decomposition_attempt/ATTEMPT.md`
— the exact technical template for this front: Proposição S's precise
statement and proof (the Key Lemma, strong induction on `|B|`, the
`(1-P_B)F(B)+G(B)=1` identity via exponential-integral representation), and
the Full Cycle-Count Decomposition Theorem's precise statement and proof for
general `K`. `THEOREM.md` §2 (Definition 3, the explicit hazard-clock
continuum construction) and §5 (Lemma 2, the `K=1` density proof, §5.3) were
also read in full — Definition 3 turns out to compute only the
single-point marginal `P(x_0\text{ cyclic})`, not the full spatial law
needed here (this is made precise in Section 3 below), but §5.3's `K=1`
construction is the exact object this front's `M_K'` is checked against at
`K=1` (Section 5.1).

**What is cited, not re-derived, and used as a black box throughout:**
Governing-Source Reindexing (Estágio 35 `K=3`/ Estágio 38 general-`K`: the
gap vector `(g_0,\ldots,g_{K-1},O)` is uniform over compositions of `n-K`
into `K+1` nonnegative parts, independent of topology); the i.i.d.
categorical-destinations fact (`dest(0),\ldots,dest(K-1)` i.i.d. categorical
on `\{0,\ldots,K-1,\mathrm{DEAD}\}` with weights `p_i:=L_i/n`,
`p_D:=O/n` — Estágio 40 §2.1, re-verified `K`-free by Estágio 41's referee);
the landing-position-uniform fact (`general_k_joint_attempt` §4.1: given
`\mathrm{dest}(s)=t`, the within-arc landing position is uniform on
`\{1,\ldots,L_t\}`, independent across sources); Proposição S general-`K`
(Estágio 41, PROVED); the Full Cycle-Count Decomposition Theorem general-`K`
(Estágio 41, PROVED: `T=O+\sum_{s\in S}V_s`, `(V_s)_{s\in S}` mutually
independent given `S`, `V_s\sim\mathrm{Uniform}\{1,\ldots,L_s\}`); Conjecture
1 general-`K` (Estágio 24, PROVED unconditionally for every `K\ge1`,
`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`); Lema R (this document's `THEOREM.md`
Estágio 27 lineage, `distributional_bridge_attempt/ATTEMPT.md` §3, PROVED).
Two classical, standard, low-risk facts used without re-derivation: the
joint density of order statistics of i.i.d. `\mathrm{Uniform}(0,1)`
variables (hence that their spacings are `\mathrm{Dirichlet}(1,\ldots,1)`
— any probability text's treatment of the Dirichlet distribution); and the
elementary "continuification of a discrete uniform" identity
`U=\lceil n\eta\rceil` for `U\sim\mathrm{Unif}\{1,\ldots,n\}`,
`\eta\sim\mathrm{Unif}(0,1)` a specific coupling of the two (used, not
re-derived, though re-verified for this front's own purposes in Section
4.2). **Nothing** from `k2_open_lemma`, `k3_full_cdf_attempt`,
`sharp_rate_constants_attempt`, or any `K`-fixed closed-form-CDF front is
used or replicated — this front is deliberately orthogonal to that route,
per the mandate.

---

## 2. Setup, restated precisely

Fix `K\ge0`. Under `THEOREM.md` Definition 4, sources fixed WLOG at
`\{0,\ldots,K-1\}\subset\{0,\ldots,n-1\}`, `M_n^{(K)}:=T/n`,
`T:=\#\{\text{cyclic points of }f\}`, `F_n^{(K)}(x):=P(M_n^{(K)}\le x)`. The
target: `F_K(x):=1-(1-x^2)^K` for `x\in[0,1)`, `F_K(x)=1` for `x\ge1`
(`F_0\equiv\mathbf1\{x\ge1\}`; `K=0` needs no argument at all —
`M_n^{(0)}\equiv1\equiv M_0`, exactly, every `n`, already noted in
`distributional_bridge_attempt/ATTEMPT.md` §4). **Every claim below with
`K` unqualified means "for every `K\ge1`."**

By the Governing-Source Reindexing fact, on `\{n>K\}`, `L_s:=g_s+1`
(`s=0,\ldots,K-1`, `L_s\ge1` the length of `\mathrm{ARC}(s)`) and `O` (points
on no marked arc) satisfy `\sum_s L_s+O=n`, and `(L_0,\ldots,L_{K-1},O)` is
uniform over compositions of `n-K` into `K+1` nonnegative parts — equivalently
(a standard bijection, re-derived in Section 4.2 for this front's own use),
the sorted set of `K` "divider" positions `\{L_0, L_0+L_1,\ldots,
\sum_{i<K}L_i\}\subset\{1,\ldots,n\}` is a uniform random `K`-subset.

---

## 3. The continuum object `M_K'`

`M_K'` is the literal `n\to\infty` continuum limit of the Estágio-41
decomposition machinery, built from the same three ingredients with
continuum inputs:

1. **Arc-length simplex.** `(p_0,\ldots,p_{K-1},p_D)\sim\mathrm{Dirichlet}
   (1,\ldots,1)` (`K+1` ones) — the standard continuum limit of a uniform
   composition, realized concretely (Section 4.1) as the spacings of `K`
   i.i.d. `\mathrm{Uniform}(0,1)` order statistics.
2. **The set `S`.** Proposição S (Estágio 41) is proved for **any**
   normalized weight vector — its proof (the Key Lemma, strong induction on
   `|B|` via the algebraic identity `(1-P_B)F(B)+G(B)=1`) is verified in
   `general_k_decomposition_attempt/ATTEMPT.md` §2.5 even against negative
   and `>1` rational weights, i.e. it is a **pure algebraic identity**, not
   one relying on discreteness or on `p_i` being a ratio `L_i/n`. So
   Proposição S applies **verbatim, with no new argument**, to the
   continuum weights `(p_0,\ldots,p_{K-1},p_D)` of item 1: `S\subseteq
   \{0,\ldots,K-1\}` is the random set with `P(S=A\mid p) = |A|!\,\prod_{a\in
   A}p_a\,(p_D+\sum_{a\in A}p_a)`, realized concretely (Section 4.1) via the
   same "categorical destination, chase for cycles" construction as the
   discrete model, now on continuum weights.
3. **Within-arc positions.** Given `s\in S`, `V_s'\sim\mathrm{Uniform}(0,p_s)`,
   mutually independent given `S` — the continuum limit of `V_s/n` given
   `V_s\sim\mathrm{Uniform}\{1,\ldots,L_s\}`, licensed by the same
   landing-position-uniform fact used discretely (Section 4.1 makes this
   concrete without extra randomness).

`\boxed{M_K' := p_D + \sum_{s\in S}V_s'}` — a well-defined random variable
regardless of whether it equals `M_K` in law; Claim B (Section 5) is exactly
the question of whether it does.

---

## 4. Theorem A: the coupling (PROVED, unconditional, `K`-free)

### 4.1 Shared primitives, and both constructions from them

Let `\xi_0,\ldots,\xi_{K-1}` and `\eta_0,\ldots,\eta_{K-1}` be `2K` i.i.d.
`\mathrm{Uniform}(0,1)` random variables (the `\xi`'s drive the arc
structure, the `\eta`'s the destinations — **no further randomness is
needed**: the same `\eta_j` that decides *which* arc source `j`'s target
lands in also gives, via its position inside that arc's sub-interval, the
within-arc landing position, discretely and continuously at once).

**Discrete side.** `D_i:=\lceil n\xi_i\rceil\in\{1,\ldots,n\}`
(`i=0,\ldots,K-1`). Call `\mathrm{NoColl}` the event that `D_0,\ldots,
D_{K-1}` are pairwise distinct.

> **Fact 1 (elementary, PROVED).** Conditional on `\mathrm{NoColl}`,
> `\{D_0,\ldots,D_{K-1}\}` is exactly a uniform random `K`-subset of
> `\{1,\ldots,n\}`; and `P(\mathrm{NoColl}^c)\le K(K-1)/(2n)`.

*Proof.* Unconditionally `(D_0,\ldots,D_{K-1})` is i.i.d.
`\mathrm{Unif}\{1,\ldots,n\}` (each `D_i=\lceil n\xi_i\rceil` takes each
value `1,\ldots,n` with probability exactly `1/n`, independently), i.e.
uniform over the `n^K` equally-likely tuples. `\mathrm{NoColl}` is the
sub-event of the `K!\binom nK` all-distinct tuples, each still equally
likely (a subset of equally-likely outcomes, each with the same
probability `n^{-K}`), so conditional on `\mathrm{NoColl}`,
`(D_0,\ldots,D_{K-1})` is uniform over ordered `K`-tuples of distinct
values, i.e. `\{D_0,\ldots,D_{K-1}\}` is a uniform `K`-subset. For the
probability bound: for `i\ne j`, `P(D_i=D_j)=\sum_{k=1}^n(1/n)^2=1/n`
(both `\lceil n\xi_i\rceil` and `\lceil n\xi_j\rceil` land in interval `k`
with probability `1/n`, independently); union bound over the
`\binom K2` pairs. `\square`

By Fact 1 and the Governing-Source Reindexing fact (§2), on `\mathrm{NoColl}`
the sorted values `D_{(1)}<\cdots<D_{(K)}` **exactly** realize a valid
instance of Definition 4's gap-vector law: set `\mathrm{cumL}(0):=0`,
`\mathrm{cumL}(t):=D_{(t)}` (`t=1,\ldots,K`), `L_{t-1}:=\mathrm{cumL}(t)-
\mathrm{cumL}(t-1)` (`t=1,\ldots,K`, `0`-indexed as `L_0,\ldots,L_{K-1}`),
`O:=n-D_{(K)}`.

For `j=0,\ldots,K-1`, `\mathrm{dest}(j):=t` if `\eta_j\in(\mathrm{cumL}(t)/n,
\mathrm{cumL}(t+1)/n]` (`t=0,\ldots,K-1`), `\mathrm{dest}(j):=\mathrm{DEAD}`
if `\eta_j\in(\mathrm{cumL}(K)/n,1]`. This is exactly a realization of the
already-cited i.i.d.-categorical-destinations fact (weights `L_t/n`, `O/n`),
by the standard continuification identity `U=\lceil n\eta\rceil` for
`U\sim\mathrm{Unif}\{1,\ldots,n\}` applied region-by-region (§1's citation).
`S:=` the union of cycles of the functional graph on `\{0,\ldots,K-1\}`
induced by `\mathrm{dest}` (absorbing at `\mathrm{DEAD}`). For `t\in S`, let
`j=\mathrm{pred}(t)` be the unique source with `\mathrm{dest}(j)=t`
(existence/uniqueness: already-cited Lemma 4, Estágio 35/38); the within-arc
landing position, in `\{1,\ldots,L_t\}`, is `k_t:=\lceil n\eta_j-
\mathrm{cumL}(t)\rceil`, and `V_t:=L_t-k_t+1`. By the Decomposition Theorem
(cited): `T=O+\sum_{t\in S}V_t`, `M_n^{(K)}=T/n`.

**Continuum side, from the *same* `(\xi,\eta)`.** Let `\xi_{(1)}<\cdots<
\xi_{(K)}` be the order statistics of `\xi_0,\ldots,\xi_{K-1}`,
`\mathrm{cumQ}(0):=0`, `\mathrm{cumQ}(t):=\xi_{(t)}` (`t=1,\ldots,K`),
`q_{t-1}:=\mathrm{cumQ}(t)-\mathrm{cumQ}(t-1)`, `q_D:=1-\mathrm{cumQ}(K)` —
by the standard order-statistics-spacings fact (§1, cited), `(q_0,\ldots,
q_{K-1},q_D)\sim\mathrm{Dirichlet}(1,\ldots,1)` exactly. `\mathrm{dest}^\infty
(j):=t` if `\eta_j\in(\mathrm{cumQ}(t),\mathrm{cumQ}(t+1)]`, or `\mathrm{DEAD}`
if `\eta_j\in(\mathrm{cumQ}(K),1]` — by Proposição S's algebraic universality
(§3, item 2), this is exactly a realization of `S^\infty\sim` Proposição
S`(q)`. `V_t':=\mathrm{cumQ}(t+1)-\eta_j` for `t\in S^\infty`,
`j=\mathrm{pred}^\infty(t)` (the unique source with `\mathrm{dest}^\infty
(j)=t`) — this is exactly `\mathrm{Uniform}(0,q_t)` given `S^\infty` (§3,
item 3: `\eta_j`, conditioned on landing in the sub-interval
`(\mathrm{cumQ}(t),\mathrm{cumQ}(t+1)]` of length `q_t`, is uniform on it, so
`\mathrm{cumQ}(t+1)-\eta_j` is uniform on `(0,q_t)`; independence across
`t\in S^\infty` since the underlying `\eta_j`'s are independent and distinct
`t`'s have distinct predecessors, Lemma 4 again). `M_K':=q_D+\sum_{t\in
S^\infty}V_t'`, exactly matching Section 3's construction.

### 4.2 The pointwise bound

> **Lemma (sorting is `1`-Lipschitz in `\ell^\infty` under matched indices;
> elementary, PROVED).** If `a_i,b_i\in\mathbb R` (`i=1,\ldots,K`) satisfy
> `|a_i-b_i|\le\eta` for every `i`, then `|a_{(j)}-b_{(j)}|\le\eta` for the
> sorted sequences, every `j`.

*Proof.* `N_a(t):=\#\{i:a_i\le t\}`, similarly `N_b`. `a_i\le b_i+\eta`
`\Rightarrow` `\{i:b_i\le t-\eta\}\subseteq\{i:a_i\le t\}` `\Rightarrow`
`N_a(t)\ge N_b(t-\eta)`. `a_{(j)}=\inf\{t:N_a(t)\ge j\}\le\inf\{t:N_b(t-\eta)
\ge j\}=\eta+b_{(j)}`. Symmetric argument gives `b_{(j)}\le a_{(j)}+\eta`.
`\square`

Since `|D_i/n-\xi_i|\le1/n` deterministically for every `i`
(`\lceil n\xi_i\rceil/n-\xi_i\in[0,1/n)`), the Lemma gives, for every
`t=0,\ldots,K`: `|D_{(t)}/n-\xi_{(t)}|\le1/n`, i.e.
`|\mathrm{cumL}(t)/n-\mathrm{cumQ}(t)|\le1/n`. **This bound does not
accumulate over `t`** — it is the direct order-statistic bound, not a sum of
`t` individual gap errors.

**Divider-boundary mismatch.** `\mathrm{dest}(j)\ne\mathrm{dest}^\infty(j)`
only if `\eta_j` lands in the "mismatch zone" around one of the `K` internal
thresholds `t=1,\ldots,K` (the zone around threshold `t` has length
`|\mathrm{cumL}(t)/n-\mathrm{cumQ}(t)|\le1/n`); total zone length `\le K/n`.
So, for fixed `j`, on `\mathrm{NoColl}`:
`P(\mathrm{dest}(j)\ne\mathrm{dest}^\infty(j)\mid\xi)\le K/n` deterministically
(the bound holds for **every** realization of `\xi` satisfying
`\mathrm{NoColl}`, not merely on average — `\eta_j` is independent of `\xi`).
Union bound over `j=0,\ldots,K-1`:

`P(\exists j:\mathrm{dest}(j)\ne\mathrm{dest}^\infty(j)\mid\mathrm{NoColl})\le
K\cdot K/n = K^2/n`.

**The good event.** `G:=\mathrm{NoColl}\cap\{\mathrm{dest}(j)=
\mathrm{dest}^\infty(j)\ \forall j\}`. By Fact 1 and the mismatch bound,
`P(G^c)\le K(K-1)/(2n)+K^2/n = (3K^2-K)/(2n) =: \delta(K,n)`.

On `G`: `\mathrm{dest}=\mathrm{dest}^\infty` as functions on
`\{0,\ldots,K-1\}`, so their iteration sequences from every starting point
coincide identically — **`S=S^\infty` exactly** (a direct fact about
iterating an identical function, no further argument needed). For `t\in S`,
with `j=\mathrm{pred}(t)=\mathrm{pred}^\infty(t)` (same `j`, since `S=S^\infty`
and predecessors are determined by `\mathrm{dest}=\mathrm{dest}^\infty`):

`V_t/n-V_t' = \big[(\mathrm{cumL}(t+1)/n-\eta_j)+\delta_1\big] -
\big[\mathrm{cumQ}(t+1)-\eta_j\big]`, `\delta_1\in(0,1/n]`

(the identity `V_t=(\mathrm{cumL}(t+1)-n\eta_j)+\delta`, `\delta\in(0,1]` —
direct algebra from `k_t=\lceil n\eta_j-\mathrm{cumL}(t)\rceil`, verified in
`coupling_bound_check.py`'s assertions), so
`|V_t/n-V_t'|\le|\mathrm{cumL}(t+1)/n-\mathrm{cumQ}(t+1)|+1/n\le1/n+1/n=2/n`.
Also `|O/n-q_D| = |\mathrm{cumL}(K)/n... | = |D_{(K)}/n-\xi_{(K)}|\le1/n`
(no accumulation, same direct order-statistic bound). Hence, on `G`:

`|M_n^{(K)}-M_K'| = \Big|(O/n-q_D)+\sum_{t\in S}(V_t/n-V_t')\Big| \le
1/n + |S|\cdot 2/n \le 1/n+K\cdot2/n = (2K+1)/n =: \varepsilon(K,n)`.

### 4.3 Assembling Theorem A

For any `x`: `F_n^{(K)}(x)=P(M_n^{(K)}\le x) \le P(M_K'\le
x+\varepsilon(K,n), G)+P(G^c) \le F_{M_K'}(x+\varepsilon(K,n))+\delta(K,n)`;
symmetrically `F_n^{(K)}(x)\ge F_{M_K'}(x-\varepsilon(K,n))-\delta(K,n)`. If
`F_{M_K'}` is `\Lambda`-Lipschitz, `|F_{M_K'}(x\pm\varepsilon)-F_{M_K'}(x)|
\le\Lambda\varepsilon(K,n)`, giving Theorem A as stated in the executive
summary. `\blacksquare`

**What Theorem A does and does not use.** Every ingredient is either (i) a
fact already PROVED `K`-free in the archive and cited verbatim
(Governing-Source Reindexing, categorical destinations, landing-position-
uniform, Proposição S, the Decomposition Theorem, Lemma 4), (ii) a standard,
completely elementary classical fact (order-statistic spacings are
Dirichlet, discrete-uniform continuification), or (iii) new, fully
self-contained, elementary probability proved from scratch above (Fact 1,
the sorting lemma, the mismatch-zone bound). **No concentration inequality
of any kind is used** — every bound is either exact/deterministic (the
ceiling-rounding bounds) or an exact combinatorial probability (Fact 1's
`1/n` per-pair collision probability), which is what keeps the whole
argument `K`-free with a clean **polynomial**, not exponential-in-`K`,
constant — avoiding the `2^K`-blowup that a naive per-subset union bound
over Proposição S's `2^K` terms would have produced (this is exactly the
kind of obstruction the mandate flagged as a risk; it is avoided here by
coupling the primitive `\mathrm{dest}`-vector directly, never summing over
subsets `A` at all).

### 4.4 Independent numerical verification of Theorem A

**`construction_crosscheck.py`** (this directory): before trusting the
`(\xi,\eta)`-coupling of §4.1 at all, this script checks that the
**discrete** reduced-model recipe of §2 (gap-vector via a uniform
`K`-subset, i.i.d. categorical destinations, landing-position-uniform,
Decomposition Theorem — sampled *directly*, not via `\xi,\eta`) reproduces
the exact `T`-distribution of a **fresh, independent, literal brute-force
implementation of Definition 4** (real permutations, real reroute targets,
`true_definition4_bruteforce.py`, this directory, exhaustive for
`n\le6`). Result (`n,K\in\{(4,1),(5,1),(4,2),(5,2),(6,2),(5,3),(6,3)\}`,
`400{,}000` trials each, reserved seeds `20260933100`–`20260933106`): every
mean matches to within Monte Carlo noise (max deviation `0.0007`) and every
per-value pmf discrepancy is `\le0.0015`, consistent with sampling noise at
this trial count (`\mathrm{SE}\approx0.0008`). As a bonus, the exact `E[T]/n`
values from `true_definition4_bruteforce.py` reproduce `THEOREM.md` §7.3–7.4's
own reported table exactly (`n=4,K=1`: `11/16`; `n=5,K=1`: `17/25`;
`n=4,K=2`: `113/192`; `n=5,K=2`: `356/625`; `n=6,K=2`: `151/270` — all exact
rational matches), an unplanned independent re-confirmation of that table.

**`xi_construction_meancheck.py`**: specifically checks the `\lceil
n\xi_i\rceil`-based divider construction of §4.1 (not just the abstract
reduced model) reproduces the correct mean, conditioning on `\mathrm{NoColl}`
(reserved seeds `20260933150`–`20260933152`, `300{,}000` trials each,
`n,K\in\{(6,2),(5,1),(5,3)\}`): MC means `0.559546/0.680816/0.522263` vs
exact `0.559259/0.680000/0.520960` — all within Monte Carlo noise, even at
these small `n` where `\mathrm{NoColl}` fails on a sizeable fraction of
trials (as low as `48\%` kept at `n=5,K=3`), confirming conditioning on
`\mathrm{NoColl}` does not introduce a hidden bias.

**`coupling_bound_check.py`** (the main check, this directory): implements
§4.1's **full joint** construction exactly as specified (both sides from the
same `\xi,\eta`) and empirically checks all three quantitative claims of
Theorem A's proof, at `(K,n)\in\{(2,50),(2,500),(4,50),(4,500),(6,50),
(6,500),(8,200)\}`, `60{,}000` trials each (reserved seeds
`20260933200`–`20260933206`):

| `K` | `n` | `P(\mathrm{coll})` MC | bound | `P(\mathrm{mismatch}\mid\mathrm{NoColl})` MC | bound | `\max\lvert M_n^{(K)}-M_K'\rvert` on `G` | bound `\varepsilon(K,n)` |
|---|---|---|---|---|---|---|---|
| 2 | 50 | 0.02000 | 0.02000 | 0.03935 | 0.08000 | 0.058912 | 0.100000 |
| 2 | 500 | 0.00192 | 0.00200 | 0.00414 | 0.00800 | 0.005889 | 0.010000 |
| 4 | 50 | 0.11355 | 0.12000 | 0.14870 | 0.32000 | 0.114361 | 0.180000 |
| 4 | 500 | 0.01198 | 0.01200 | 0.01557 | 0.03200 | 0.012004 | 0.018000 |
| 6 | 50 | 0.26558 | 0.30000 | 0.30630 | 0.72000 | 0.145268 | 0.260000 |
| 6 | 500 | 0.02848 | 0.03000 | 0.03515 | 0.07200 | 0.014865 | 0.026000 |
| 8 | 200 | 0.13112 | 0.14000 | 0.14649 | 0.32000 | 0.041237 | 0.085000 |

**Every one of the `420{,}000` trials across all seven configurations
respects `|M_n^{(K)}-M_K'|\le\varepsilon(K,n)` on the good event `G` — zero
violations** (the "max" column is always `<` the bound column), a hard
per-trial check, not a statistical average — strong evidence against an
off-by-one or sign error anywhere in §4.1–4.2's chain of inequalities. The
collision and mismatch rates track their analytic bounds closely (the
collision bound is essentially tight; the mismatch bound has more slack,
consistent with it being a cruder union bound). The resulting empirical
`\sup_x|F_n^{(K)}(x)-F_{M_K'}(x)|` (estimated on a `199`-point grid, from the
same trials) is, in every row, far below the (deliberately loose, worst-case)
analytic bound `\delta(K,n)+\Lambda_K\varepsilon(K,n)` (full log:
`coupling_bound_check.log`).

---

## 5. Claim B: `M_K' \overset{d}{=} M_K`

### 5.1 `K=1`: PROVED exactly

At `K=1`: `(p_0,p_D)\sim\mathrm{Dirichlet}(1,1)`, i.e. `p_0\sim
\mathrm{Uniform}(0,1)` — write `L:=p_0`. Proposição S at `K=1`:
`P(S=\{0\})=1!\cdot p_0\cdot(p_D+p_0)=p_0\cdot1=L` (using
`p_D+p_0=1`), `P(S=\emptyset)=p_D=1-L`. Given `S=\{0\}`, `V_0'\sim
\mathrm{Uniform}(0,L)`; `M_1'=p_D+V_0'=(1-L)+V_0'`. Given `S=\emptyset`,
`M_1'=p_D=1-L`. This is **term for term** `THEOREM.md` §5.3's already-proved
`K=1` construction: `L\sim\mathrm{Unif}(0,1)` the struck-cycle length,
`u\notin C` (probability `1-L`) `\Rightarrow M_1=1-L`; `u\in C` (probability
`L`) `\Rightarrow M_1=1-L+D`, `D\mid(L,u\in C)\sim\mathrm{Uniform}(0,L)` —
identical distributional recipe, `P(u\in C)=L` matching `P(S=\{0\})=L`
exactly. Hence `M_1'\overset d=M_1`, i.e. Claim B at `K=1` is **PROVED**,
not merely numerically supported — it reduces directly to a result already
established elsewhere in this archive by an independent method.

### 5.2 Exact moment verification, `K=1,\ldots,7`

`verify_MK_moments.py` (this directory) computes `E[(M_K')^t]` **exactly**
(Python `Fraction` arithmetic throughout, no floating point, no randomness)
via: (a) expanding Proposição S`(A;p)` into monomials in
`p_0,\ldots,p_{K-1},p_D` for every subset `A`; (b) expanding
`E[(p_D+\sum_{a\in A}V_a')^t\mid p,A]` into monomials via the multinomial
theorem, using `E[(V_a')^k\mid p_a]=p_a^k/(k+1)`; (c) integrating each
resulting monomial **exactly** against the `\mathrm{Dirichlet}(1,\ldots,1)`
density via the closed-form Dirichlet-moment formula
`E[\prod_ip_i^{k_i}]=K!\prod_i(k_i!)/(K+\sum_ik_i)!` (a standard, elementary
fact about the flat distribution on the simplex — cross-checked
independently by Monte Carlo inside the script itself, `K=3`, three
exponent patterns, all within `0.0005` of the exact value). The target
`E[M_K^t]` is computed by a **fully independent route** — direct `sympy`
exact symbolic integration of `x^t\cdot2Kx(1-x^2)^{K-1}` over `[0,1]`, using
only the already-cited density formula, no reference to Proposição S or the
decomposition machinery at all.

| `K` | `t` | `E[(M_K')^t]` | `E[M_K^t]` (target) | match |
|---|---|---|---|---|
| 1 | 1 | `2/3` | `2/3` | exact |
| 1 | 2 | `1/2` | `1/2` | exact |
| 1 | 3–5 | `2/5, 1/3, 2/7` | same | exact |
| 2 | 1–5 | `8/15, 1/3, 8/35, 1/6, 8/63` | same | exact |
| 3 | 1–5 | `16/35, 1/4, 16/105, 1/10, 16/231` | same | exact |
| 4 | 1–5 | `128/315, 1/5, 128/1155, 1/15, 128/3003` | same | exact |
| 5 | 1–5 | `256/693, 1/6, 256/3003, 1/21, 256/9009` | same | exact |
| 6 | 1–5 | (5 values) | same | exact |
| 7 | 1–5 | (5 values) | same | exact |

**All 35 cells (`K=1,\ldots,7`, `t=1,\ldots,5`) match exactly — zero
discrepancies, exact rational equality, not a floating-point tolerance**
(full transcript `verify_MK_moments.log`). Since `M_K` and `M_K'` are both
supported on `[0,1]` (a compact interval, where the moment problem is
determinate), matching five moments for seven consecutive `K` values is
substantial — though explicitly **not** a proof that all moments match, nor
that they match for `K>7` — evidence.

### 5.3 Partial structural progress toward a general proof

Reorganizing the exact computation of §5.2 by grouping the `2^K` subsets `A`
by size `r:=|A|` (Proposição S and the Dirichlet-moment formula both depend
on `A` only through `r`, by exchangeability) gives, for a purely
combinatorial quantity `W(r,t)` (independent of `K`, defined precisely in
`find_W_pattern.py`, this directory — the Proposição-S-weighted `t`-th
moment contribution from a size-`r` subset, before any `K`-dependent
Dirichlet normalization):

`E[(M_K')^t] = K!\displaystyle\sum_{r=0}^K\binom Kr\frac{W(r,t)}{(K+t+r+1)!}`

(cross-checked against §5.2's direct computation: exact match, `15/15`
cells, `K=1,\ldots,5`, `t=1,\ldots,3` — `find_W_pattern.py`'s own
independent-route check). Computing `W(r,t)` for `r=0,\ldots,8` and pattern-
matching the resulting integer sequences (`find_W_pattern.log`) gives two
**exact, verified** closed forms:

`W(r,1) = 2\,r!\,(r+1)^2`, `\qquad W(r,2) = r!\,(r+1)(r+2)(2r+3)`

(verified against all `9` computed values each, `r=0,\ldots,8`, exact
rational equality). If a closed form `W(r,t)` were found for **every** `t`
and the resulting sum over `r` (with `K` symbolic) were summable in closed
form — e.g. via `\texttt{sympy.summation}` on the binomial-weighted sum
above, which requires `W(r,t)` as an explicit function of `r`, not merely a
table — this would upgrade Claim B to a genuine `K`-free proof, mirroring
exactly how Estágio 41 upgraded Estágio 40's four separate `K=3` formulas
into one `K`-free Proposição S. **This was not completed**: `W(r,t)` for
`t\ge3` was computed (`find_W_pattern.log` tabulates `t=1,\ldots,4`) but no
closed form was found or guessed for `t\ge3` in the time available, and even
with `W(r,t)` in closed form, `\texttt{sympy}`'s ability to evaluate the
resulting binomial sum in closed form for symbolic `K` was not tested. This
is reported as a **precisely located, partially-executed, unfinished**
route — not a vague "this seems hard."

### 5.4 Extended numerical support, `K` up to `20`

`MK_prime_KS_test.py` (this directory) simulates `M_K'` **directly** from
its own defining construction (§3/§4.1's continuum side, no reference to
`M_n^{(K)}` or the discrete model at all) and runs a one-sample
Kolmogorov–Smirnov test against `F_K(x)=1-(1-x^2)^K`, `40{,}000` trials per
`K`, reserved seeds `20260933300`–`20260933309`:

| `K` | `D_{KS}` | `p`-value | mean(`M_K'`) | target `\varphi_K` |
|---|---|---|---|---|
| 2 | 0.00567 | 0.152 | 0.531379 | 0.533333 |
| 3 | 0.00277 | 0.918 | 0.456967 | 0.457143 |
| 4 | 0.00257 | 0.954 | 0.406428 | 0.406349 |
| 5 | 0.00515 | 0.239 | 0.368943 | 0.369408 |
| 6 | 0.00399 | 0.547 | 0.340276 | 0.340992 |
| 8 | 0.00632 | 0.082 | 0.298310 | 0.299538 |
| 10 | 0.00428 | 0.455 | 0.270512 | 0.270260 |
| 12 | 0.00307 | 0.845 | 0.248673 | 0.248169 |
| 15 | 0.00763 | 0.019 | 0.224455 | 0.223294 |
| 20 | 0.00273 | 0.926 | 0.194685 | 0.194545 |

No systematic rejection pattern across `10` independent tests (one
`p=0.019` at `K=15` is unremarkable at this sample size with no
multiple-testing correction applied — a `\approx1`-in-`10` chance event
under the null, exactly what one such low value among ten independent tests
would suggest, not evidence against Claim B). Means track `\varphi_K`
closely throughout. This extends Claim B's empirical support well past the
exact-symbolic reach of §5.2.

### 5.5 Honest status of Claim B

**PROVED** at `K=1` (§5.1, an exact structural match to an independently-
proved result elsewhere in this archive). **NOT PROVED** for `K\ge2`. The
evidence for `K\ge2` is, in order of strength: (i) exact rational moment
matching, `35/35` cells, `K=1,\ldots,7`, `t=1,\ldots,5`, zero discrepancies,
two fully independent computational routes (§5.2); (ii) a genuine
(incomplete) reduction to a single combinatorial-sequence question `W(r,t)`,
with exact closed forms already found and verified at `t=1,2` (§5.3); (iii)
Kolmogorov–Smirnov tests, `K` up to `20`, no rejection pattern (§5.4). No
claim stronger than this is made anywhere in this document.

---

## 6. Main Theorem (conditional on Claim B)

Combining Theorem A (§4.3) with Claim B (`F_{M_K'}=F_K`, hence any Lipschitz
constant of `F_K` is usable in Theorem A's bound):

> **Lemma (Lipschitz bound for `F_K`, PROVED, elementary, `K`-free).** For
> `K\ge1`, `f_K(x)=2Kx(1-x^2)^{K-1}` attains its maximum on `[0,1]` at
> `x^*=1/\sqrt{2K-1}`, with `\Lambda_K:=\max_xf_K(x) =
> \frac{2K}{\sqrt{2K-1}}\Big(\frac{2K-2}{2K-1}\Big)^{K-1} \le 2\sqrt K`.

*Proof.* `\frac{d}{dx}\big[x(1-x^2)^{K-1}\big] = (1-x^2)^{K-2}\big[1-x^2(2K-1)
\big]`, zero exactly at `x^*=1/\sqrt{2K-1}\in(0,1)` for `K\ge1` (a maximum:
the bracket is positive for `x<x^*`, negative for `x>x^*`). Substituting,
`\Lambda_K = \frac{2K}{\sqrt{2K-1}}\big(\frac{2K-2}{2K-1}\big)^{K-1}`; since
`\big(\frac{2K-2}{2K-1}\big)^{K-1}\le1` and `2K-1\ge K` for `K\ge1`,
`\Lambda_K\le 2K/\sqrt K=2\sqrt K`. `\square` (Independently re-verified,
both the exact formula and the `\le2\sqrt K` bound, against direct
numerical maximization of `f_K` on a fine grid for `K\in\{1,2,3,5,10\}` —
`0` discrepancies beyond the grid's own resolution — and symbolically via
`sympy` for `K\in\{1,2,3,5,10,20,50\}`, all consistent.)

> **Main Theorem (CONDITIONAL on Claim B).** For every `K\ge1`, `n\ge K+1`:
> `\displaystyle\sup_x|F_n^{(K)}(x)-F_K(x)| \le \delta(K,n)+\Lambda_K\,
> \varepsilon(K,n) \le 8K^2/n`.

*Proof of the final inequality.* `\delta(K,n)+\Lambda_K\varepsilon(K,n) \le
\frac{3K^2-K}{2n} + 2\sqrt K\cdot\frac{2K+1}n = \frac1n\Big[\frac{3K^2-K}2
+4K^{1.5}+2\sqrt K\Big]`. For `K\ge1`: `K^{1.5}\le K^2` and `\sqrt K\le K^2`,
so the bracket is `\le\frac{3K^2}2+4K^2+2K^2 = 7.5K^2 \le 8K^2`. `\square`

This is the mandate's requested form exactly: `h(K)=8K^2`, an explicit
polynomial, `n_0(K)=K+1` (the bound is a valid inequality there; it becomes
numerically informative, i.e. `<1`, once `n>8K^2`, but validity does not
require this). At `K=0` the statement is trivial and exact
(`M_n^{(0)}\equiv1\equiv M_0`, §2), so the theorem holds unconditionally at
`K=0` and conditionally-on-Claim-B for every `K\ge1`.

---

## 7. What did NOT close, precisely

**The single missing piece is Claim B for `K\ge2`** (§5.5) — nothing else.
Precisely:

1. **Theorem A itself is unconditional** and does not depend on Claim B in
   any way; it is a complete, `K`-free, explicit-rate coupling result on
   its own terms, regardless of whether Claim B holds.
2. **Where a `K`-free proof of Claim B would need to go, precisely
   diagnosed:** the reduction of §5.3 shows Claim B for all `K,t`
   simultaneously is *equivalent* to finding a closed form for the purely
   combinatorial sequence `W(r,t)` (defined with no reference to `K` or
   Dirichlet integrals at all — a finite sum of products of factorials and
   small integers, computable for any `r,t` in closed form from Proposição
   S's own two-term monomial expansion) valid for **every** `t`, plus
   verifying that the resulting `K`-symbolic sum
   `\sum_{r=0}^K\binom Kr W(r,t)/(K+t+r+1)!` is summable in closed form.
   Exact closed forms for `W(r,1)` and `W(r,2)` were found (§5.3); the
   obstruction is **not** a structural barrier of the kind Estágios 44/45
   certified for the general-`K` closed CDF (no Gosper-non-summability
   argument was attempted here, and none is claimed) — it is simply that
   the pattern-matching-then-generalizing process was not carried past
   `t=2`, and the resulting `K`-symbolic sum was never attempted in
   `\texttt{sympy}`. This is a genuinely *unfinished*, not *obstructed*,
   route, and is flagged as such rather than being dressed up as a deeper
   difficulty.
3. **A direct, from-scratch, general-`K` distributional proof of Claim B**
   (e.g. matching `M_K'`'s Laplace transform, `E[e^{-\theta(1-M_K')}]`, to
   the known Laplace transform of `\max(U_1,\ldots,U_K)` for `K` i.i.d.
   `\mathrm{Uniform}(0,1)` — using the identity, re-derived independently in
   this document's own reasoning (not present anywhere else in the archive
   under this name) that `1-M_K\overset d=\max(U_1,\ldots,U_K)`, equivalently
   `M_K\overset d=\sqrt{\min(U_1,\ldots,U_K)}`

   > **Correção (2026-08-29, achado do referee hostil dedicado, severidade
   > BAIXA, dentro de uma rota já rotulada "attempted and abandoned" —
   > nenhum resultado provado ou evidenciado é afetado):** as duas formas
   > acima NÃO são equivalentes, e a primeira é falsa. `M_K\overset
   > d=\sqrt{\min(U_1,\ldots,U_K)}` está correta (`P(\sqrt{\min}\le
   > x)=P(\min\le x^2)=1-(1-x^2)^K=F_K(x)`, batendo exatamente). Mas
   > `1-M_K\overset d=\max(U_1,\ldots,U_K)` é falsa: calculando diretamente,
   > `P(1-M_K\le x)=1-F_K(1-x)=(2x-x^2)^K=x^K(2-x)^K`, que não é `x^K` (a
   > CDF de `\max(U_i)`), exceto trivialmente. A identidade correta,
   > equivalente a `M_K\overset d=\sqrt{\min(U_i)}` por substituição direta
   > (`\min(U_i)=M_K^2`), é `1-M_K^2\overset d=\max(U_1,\ldots,U_K)` (ambos
   > têm CDF `x^K` em `[0,1]`) — confirmado pelo referee analiticamente e
   > por Monte Carlo, e reconfirmado pela sessão orquestradora de forma
   > independente. Este erro está inteiramente dentro de uma rota que este
   > próprio item já rotula como "attempted and abandoned" por um motivo
   > distinto (o desacoplamento de `X_i/\Sigma` do normalizador `\Sigma`) —
   > não afeta o Teorema A (Seção 4, provado incondicionalmente) nem a
   > Reivindicação B (Seção 5, evidenciada mas não provada para `K\ge2`).
   > Fonte: `adversarial/REFEREE_REPORT.md`.

   was set up algebraically (the Laplace transform of `M_K'` reduces, via Proposição S's normalization
   `p_D+\sum_{a\in A}p_a=1-P_{A^c}`, to
   `\varphi_p(\theta)=\sum_A|A|!\,\theta^{-|A|}\prod_{a\in A}(1-e^{-\theta
   p_a})\cdot(1-P_{A^c})e^{-\theta P_{A^c}}`) but averaging this over the
   Dirichlet simplex in closed form, via the `K+1`-i.i.d.-`\mathrm{Exp}(1)`
   representation of the Dirichlet distribution, was **attempted and
   abandoned**: the ratio `X_i/\Sigma` appearing inside the non-polynomial
   function `1-e^{-\theta p_a}` does not obviously decouple from the shared
   normalizer `\Sigma=\sum X_i+X_D`, unlike the *polynomial* case the Key
   Lemma's own exponential-integral trick (§2.3 of `general_k_decomposition_
   attempt/ATTEMPT.md`) was built for. This is reported honestly as a route
   tried and not completed, distinct from item 2's route (which *was*
   pushed to a partial, verified result).
4. **A locally-uniform-in-`c`** version, or any statement about `n_0(K)`
   sharper than `K+1` (the threshold for validity, as opposed to
   usefulness) — not attempted, out of scope for this mandate.
5. **Whether `h(K)=8K^2` is close to sharp** — not examined; the
   union-bound-heavy construction of §4.2 (in particular the `K^2/n`
   mismatch-zone bound, itself already a factor-`K` improvement over a naive
   per-subset argument, §4.3) very likely leaves room for a better constant
   or exponent via a tighter (e.g. maximal-coupling rather than shared-`\eta`
   comonotone) construction — not pursued, flagged as a natural follow-up,
   not attempted here.

---

## 8. Self-caught issues (disclosed per archive convention)

1. **An early, cruder version of the mismatch-zone bound (§4.2) gave
   `O(K^3/n)`, not `O(K^2/n)`.** The first draft of the argument bounded
   `|\mathrm{cumL}(t)/n-\mathrm{cumQ}(t)|` by *accumulating* individual
   per-gap errors, `\sum_{i<t}|p_i-q_i|\le t\cdot(2/n)`, giving a threshold
   error of `O(K/n)` (not `O(1/n)`) and, after unioning over `K` thresholds
   and `K` sources, an overall `\delta(K,n)=O(K^3/n)`. Caught by noticing
   `\mathrm{cumL}(t)` and `\mathrm{cumQ}(t)` are **not** re-summed gap
   totals but literally the `t`-th sorted divider/order-statistic
   themselves, to which the sorting Lemma (§4.2) applies *directly*, giving
   the much sharper `O(1/n)` bound with no accumulation at all — this is
   what produced the final `\delta(K,n)=O(K^2/n)`, `\varepsilon(K,n)=O(K/n)`
   pair, and hence the clean `h(K)=8K^2` (rather than a much worse
   `O(K^{4.5})`-type bound the cruder version would have produced after
   folding in `\Lambda_K=O(\sqrt K)`). No downstream numbers in this
   document were computed with the cruder bound; it is recorded here only
   because the archive's convention is to disclose self-caught errors in
   the working, not just the final numbers.
2. **First version of `construction_crosscheck.py`'s cycle-finding routine
   was checked for a subtle correctness question, not a bug**: does
   re-traversing a functional-graph trajectory that passes through nodes
   already resolved by an earlier `start` value (without a *global*
   visited-set, only a per-path one) ever mis-classify a node? Traced
   through by hand (§ inline comment in the script) — no bug found, the
   redundant re-traversal always correctly re-detects the same cycle (sets
   are idempotent under redundant insertion) — but flagged and resolved
   explicitly before trusting the script's output, per this archive's
   self-check discipline.
3. **No bug found in the core exact-arithmetic pipeline**
   (`verify_MK_moments.py`, `find_W_pattern.py`): the Dirichlet-moment
   formula was cross-checked against direct Monte Carlo simulation inside
   the script itself (three exponent patterns, `K=3`) before being trusted
   for the exact computation, and the two independent routes to
   `E[(M_K')^t]` (direct subset-enumeration vs. the `r`-grouped `W(r,t)`
   reformulation) were cross-checked against each other (`15/15` exact
   matches) before either was used to claim anything.

---

## 9. Numerical verification summary

All scripts in this directory, written fresh for this front (no import from
any other front's `.py` files).

| script | type | what it checks |
|---|---|---|
| `true_definition4_bruteforce.py` | exact enumeration, no randomness | ground-truth `T`-distribution of literal Definition 4, small `n,K` |
| `construction_crosscheck.py` | Monte Carlo, reserved seeds | the discrete reduced-model recipe (§2) vs. true brute force |
| `xi_construction_meancheck.py` | Monte Carlo, reserved seeds | the `\lceil n\xi_i\rceil`-based construction (§4.1) vs. exact means |
| `coupling_bound_check.py` | Monte Carlo, reserved seeds | Theorem A's three quantitative claims, directly, per-trial |
| `verify_MK_moments.py` | exact (`Fraction`), no randomness | Claim B via `35` exact moment matches, `K=1..7`, `t=1..5` |
| `find_W_pattern.py` | exact (`Fraction`+`sympy`), no randomness | the `W(r,t)` reduction and its `t=1,2` closed forms (§5.3) |
| `MK_prime_KS_test.py` | Monte Carlo, reserved seeds | Claim B via KS tests, `K` up to `20` |

---

## 10. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Construction of `M_K'` (§3) | well-defined (not itself a claim requiring proof) |
| 2 | Fact 1 (`\mathrm{NoColl}` ⟹ uniform `K`-subset; `P(\mathrm{NoColl}^c)\le K(K-1)/(2n)`) | **PROVED** |
| 3 | Sorting-is-`1`-Lipschitz lemma | **PROVED** (elementary, standard) |
| 4 | Mismatch-zone bound `P(G^c)\le(3K^2-K)/(2n)` | **PROVED** |
| 5 | Pointwise bound `|M_n^{(K)}-M_K'|\le(2K+1)/n` on `G` | **PROVED** |
| 6 | **Theorem A** (coupling CDF bound, `M_n^{(K)}` vs `M_K'`) | **PROVED**, unconditional, `K`-free |
| 7 | Theorem A, numerical verification | zero violations, `420{,}000` trials (§4.4) |
| 8 | Claim B at `K=1` | **PROVED** (exact match to `THEOREM.md` §5.3) |
| 9 | Claim B, exact moments `K=1..7`, `t=1..5` | **PROVED per cell** (`35/35` exact matches); general-`K,t` **NOT PROVED** |
| 10 | `W(r,1)=2r!(r+1)^2`, `W(r,2)=r!(r+1)(r+2)(2r+3)` | **PROVED** (verified against `9` values each, exact) |
| 11 | `W(r,t)` general closed form; the resulting `K`-symbolic sum | **NOT ATTEMPTED / NOT FOUND** for `t\ge3` |
| 12 | Claim B, `K\ge2` general | **NOT PROVED**; strong numerical/exact-moment/KS support |
| 13 | Lipschitz bound `\Lambda_K\le2\sqrt K` for `F_K` | **PROVED**, elementary |
| 14 | **Main Theorem** `\sup_x|F_n^{(K)}-F_K|\le8K^2/n` | **PROVED, conditional on Claim B** (items 8–12) |
| 15 | Sharpness of `h(K)=8K^2` | **NOT EXAMINED** |

---

## 11. Seeds

Reserved range: `20260933000`–`20260933999` (`DISC-DEC-123`, frente (a)).

**Grep-confirmation before first use** (run before any file in this
directory was written):
```
$ grep -rn "20260933" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8049:      Seed reservado: 20260933000-20260933999.
```
Only the governance reservation line — the range was genuinely unused.

**Grep-confirmation after all work** (run after every file in this
directory was created):
```
$ grep -rn "20260933" 05_DISCOVERY_LAB/ | grep -v "/k_free_convergence_bridge_attempt/"
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8049:      Seed reservado: 20260933000-20260933999.
```
Still only the governance line outside this front's own directory — no
collision with any other front, before or after.

**Seed allocation, no seed reused across scripts or cells:**

| script | seeds | cells |
|---|---|---|
| `verify_MK_moments.py` | `20260933050` (Dirichlet-formula MC self-check only; main pipeline is exact/deterministic) | `1` |
| `construction_crosscheck.py` | `20260933100`–`20260933106` | `7` `(n,K)` cells |
| `xi_construction_meancheck.py` | `20260933150`–`20260933152` | `3` `(n,K)` cells |
| `coupling_bound_check.py` | `20260933200`–`20260933206` | `7` `(K,n)` cells |
| `MK_prime_KS_test.py` | `20260933300`–`20260933309` | `10` `K` cells |
| `true_definition4_bruteforce.py`, `find_W_pattern.py` | none (exact/exhaustive) | — |

---

## 12. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `true_definition4_bruteforce.py` / `.log` | fresh, exact, from-scratch brute force of literal Definition 4 |
| `construction_crosscheck.py` / `.log` | discrete reduced-model recipe vs. true brute force |
| `xi_construction_meancheck.py` / `.log` | `\lceil n\xi\rceil`-based divider construction vs. exact means |
| `coupling_bound_check.py` / `.log` | main empirical verification of Theorem A |
| `verify_MK_moments.py` / `.log` | exact moment verification of Claim B, `K=1..7`, `t=1..5` |
| `find_W_pattern.py` / `.log` | the `W(r,t)` reduction, cross-check, and `t=1,2` closed forms |
| `MK_prime_KS_test.py` / `.log` | KS tests of Claim B, `K` up to `20` |

---

## 13. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml`,
`README.md`, or `index.html`. No `adversarial/` subdirectory created, no
referee dispatched by this front. No `git` command run. No `.py` file from
any other front (this lineage or any ancestor/sibling) was read, opened, or
imported — every script in this directory was written fresh from
`THEOREM.md` and the cited `ATTEMPT.md` documents' mathematical prose only.
Every claim above is labeled PROVED / CONDITIONAL / NOT PROVED / NOT
ATTEMPTED at the point of use; the one genuinely open piece (Claim B,
`K\ge2`) is isolated as precisely as this front could manage, with the
partial `W(r,t)` progress reported honestly as unfinished rather than
either overclaimed as a proof or dismissed as a dead end. No claim of
progress on any Millennium Problem anywhere in this document; this is pure
combinatorial mathematics internal to the u12 ensemble defined in
`THEOREM.md`.
