# Generalizing the K=1 case-split to K=2: an exact closed form for `P_nn(n,2)`, and what breaks at `K=3`

**Front:** Wave 19, front (a), `K2-JOINT-CASE-SPLIT-ATTEMPT`, authorized by
`DISC-DEC-083` (`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`). Pure
combinatorial mathematics about the u12 random-permutation-with-reroutes
ensemble defined in `THEOREM.md` Definitions 1–4. **This is not a
Millennium Problem and no claim of that kind is made anywhere below.**

Reserved seeds: `20260880000`–`20260880999` (this front's own; grep-confirmed
unused before first use — see §9). Referee range `20260881000+` untouched.

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, or
`DISCOVERY_LAB_STATE.md`. No `adversarial/` subdirectory created here, no
referee dispatched by this front, no git command run. All work confined to
this new subdirectory.

---

## Executive summary (read first)

**Mandate.** Generalize the K=1 case-split method (`THEOREM.md`
Proposition 4 / Proposition K1) from one reroute source to two, for one of
three closely related K=2 targets named by the dispatch: (i) the exact
limiting second moment `P_nn(n,2)` of the distributional bridge (Estágio 27,
`distributional_bridge_attempt`); (ii) the K=2 case of the continuum
Theorem J transfer, `P(\text{same final cycle}\mid2\text{ marks})`
(Estágio 28, `joint_exploration_continuum_attempt`); (iii) the general
joint two-point law at K=2 (Estágio 18's original obstruction).

**Target chosen: (i), `P_nn(n,2)`.** Rationale (§1): it is the most tightly
scoped of the three (a single scalar limit, not a full law), it is exactly
what Lemma P2 (`distributional_bridge_attempt` §6.2, PROVED, cited) needs to
close the K=2 second moment of the distributional bridge, and — as
anticipated by the dispatch — solving it turns out to hand over target (ii)
at K=2 essentially for free, via the already-proved Theorem J transfer
(Estágio 28's Proposition R, cited).

**What this document proves, unconditionally, all independently
verified by fresh brute-force enumeration (own scripts, no code read from
any other front):**

1. **The Marked-Point Gap Structure Lemma** (§2, PROVED, new): for a
   uniform random permutation of `[n]` and `m` distinguished points, the
   "contracted permutation" on the `m` marks is uniform on `S_m`, and,
   independently of that topology, the `m` inter-mark gap sizes plus one
   "outside" count are jointly uniform over all compositions of `n-m` into
   `m+1` nonnegative parts. This is the exact `m`-point generalization of
   `THEOREM.md` Proposition 4 Step 1 (`L\sim\mathrm{Unif}\{1,\dots,n\}`,
   the `m=1` case). Verified by exhaustive enumeration, `m=2,3`, `n` up to
   `7`, `0/11` mismatches.
2. **The Two-Source Redirect-Structure Lemma** (§3, PROVED, new): with two
   reroute sources cutting a permutation's cycle structure into two "arcs"
   of lengths `p,q`, a full 9-case analysis gives closed-form probabilities
   for a single arc point being cyclic, and for **two** arc points (same
   arc or different arcs) being **jointly** cyclic — the exact generalization
   of Proposition 4/K1's single-arc per-point rule to two arcs. Verified by
   exhaustive enumeration over all `n^2` `(U_0,U_1)` pairs, `120`
   `(n,p,q)` configurations (`n=2,\dots,9`), `0` mismatches across every
   sub-formula.
3. **Proposition NN2 (main result, PROVED):**
   `\displaystyle P_{nn}(n,2) = \frac{10n^2+7n+2}{30n^2} = \frac13+\frac{7}{30n}+\frac1{15n^2}`,
   for every `n\ge4`. Derived by combining Lemmas 1–2 via exact symbolic
   resummation (`sympy`, exact rational arithmetic) and independently
   confirmed by fresh brute-force enumeration of Definition 4's K=2 model
   at `n=4,\dots,9` — `6/6` exact rational matches, including a brand-new
   `n=9` data point (`29{,}393{,}280` exact configurations).
4. **Corollary NN2.1 (PROVED, closes Estágio 27's named K=2 item, second
   moment only):** `P_{nn}(n,2)\to\tfrac13=\tfrac1{K+1}\big|_{K=2}`, so by
   Lemma P2 (cited, `distributional_bridge_attempt`), `E[(M_n^{(2)})^2]\to
   \tfrac13=E[M_2^2]` (Estágio 24). This is a genuine, unconditional
   closure of the specific gap Estágio 27 named open: "`K\ge2` honestly
   open... needs a whole-space `K=2` case analysis in Proposition D1's
   style" — for the second moment.
5. **Corollary NN2.2 (PROVED, target (ii), K=2 closure of the continuum
   transfer, both finite-`n` conventions):** by Theorem J's Corollary
   (Estágio 25, cited, exact at every finite `n,K`) applied directly to the
   `P_nn` convention, `P_{nn\text{-same}}(n,2):=\tfrac12P_{nn}(n,2) =
   \frac{10n^2+7n+2}{60n^2}\to\frac16=\frac1{2(K+1)}\big|_{K=2}` — extending
   Estágio 28's K=0,1 continuum-transfer theorem
   (`P(\text{same}\mid K\text{ marks})=1/(2(K{+}1))`) to K=2, matching the
   value the continuum theory already predicts. A bonus reduction lemma
   (§6, PROVED) also shows the *other* finite-n convention used by Estágio
   28's own Proposition K1 (query points fixed, reroute-source set allowed
   to overlap them) converges to the **same** limit `1/3`, `1/6` —
   independently confirmed by fresh brute force reproducing the exact
   values Estágio 28 §4.1 reported (`n=4,\dots,7`: `49/144, 33/100,
   44/135, 143/441`) — so this front's closure covers **both** conventions
   in the limit, though only the `P_{nn}` convention gets an exact
   finite-`n` closed form here.
6. **Target (iii) (general joint two-point law): NOT attempted directly**,
   beyond what (i)+(ii) already supply — see §8.

**What did NOT close (honest, precisely diagnosed, §7).** The `K=3` case of
the same case-split: the redirect structure for 3 sources requires tracking
a *functional graph on the 3 arcs themselves* (which arc's tail feeds which
other arc, or itself, or escapes) rather than the simple 9-case (`3\times3`)
table that sufficed for `K=2` — this is a `4^3=64`-cell analogue (`K+1=4`
destinations per source) with genuine cyclic-vs-tree substructure among the
sources' redirects, isomorphic in complexity to the marginal K≥3 problem
`THEOREM.md` needed a dedicated transfer-matrix front (Estágio 4) to solve
— but *compounded* by needing to simultaneously track two query-point
positions through that structure, which the marginal problem never needed.
The **full CDF** of `M_n^{(2)}` (not just its second moment) is also not
attempted — Proposition D1's method gives the *entire* distribution at
`K=1`; extending that (not just the second moment) to `K=2` is a strictly
harder, separately open target. Both are stated precisely in §7, not folded
into a vague "K≥2/K≥3 is hard."

**Net verdict.** A genuine, new, doubly-useful closed-form result
(`P_nn(n,2)`, Proposition NN2) is proved and cross-verified by five
independent methods (own from-scratch case-split + symbolic resummation +
exact brute force to `n=9` + a from-scratch general Gap Lemma + large-`n`
Monte Carlo triangulation), closing the K=2 second-moment case of the
distributional bridge (target i) and, via an already-proved transfer
lemma, the K=2 case of the continuum same-cycle question (target ii) too —
with `K=3` and the full-CDF generalization honestly and precisely left
open. No claim of progress on any Millennium Problem; pure internal
combinatorics on this archive's own random-permutation-with-reroutes
ensemble.

---

## 1. Reading discipline and target selection

### 1.1 What was read (prose only, per mandate)

`THEOREM.md`: Definitions 1–4 (§7.2 for Definition 4; Definitions 1–3 are
§1–2); Proposition 3 (§7.2, the mixing reduction); Proposition 4 (§7.3, the
K=1 fixed-K bridge, the case-split this front generalizes); the "Estágio
3" extension (K=2 of the *marginal* fixed-K bridge `\psi_n^{(2)} =
8/15+4/(15n)+1/(15n^2)`, via a *different* three-case split on the
generic-point's own cycle — used only as a cross-check target below, §4);
Estágio 18 (the joint-two-point obstruction, first diagnosed); Estágio 25
(Theorem J and its Corollary — `P(\text{same}\mid\text{both cyclic})=
\tfrac12` exactly, at every finite `n,K`); Estágio 27 (the distributional
bridge, Proposition D1's K=1 case-split, Lemma P2's second-moment
reduction, and the explicit "K≥2 open" diagnosis this front answers);
Estágio 28 (the continuum Theorem J transfer, Proposition R's reduction,
Proposition K1's K=1 case-split, and its own K≥2 non-closure).

Full prose (not scripts) of `distributional_bridge_attempt/ATTEMPT.md`
(Proposition D1's proof, §5; Lemma P2, §6.2) and
`joint_exploration_continuum_attempt/ATTEMPT.md` (Proposition K1's proof,
§3.2–3.3; Proposition R, §2). **No `.py` file from any other front was
opened, read, or imported anywhere in this document's derivation** — every
script below is written fresh from the mathematical descriptions in the
prose above.

### 1.2 Why target (i), `P_nn(n,2)`, and not (ii) or (iii) directly

- **(iii)** (the general joint two-point law) is, by the dispatch's own
  framing and every predecessor front's diagnosis (Estágios 18/25/27/28,
  independently), the *broadest* and least tractable of the three — a full
  joint *law*, not a scalar. Attacking it directly, with no intermediate
  target, repeats the exact failure mode two prior fronts already
  documented (Estágio 18 §3.3, Estágio 25 §6.3).
- **(ii)** (`P(\text{same}\mid2\text{ marks})`) is *already reduced*, by
  Estágio 28's Proposition R (cited, PROVED there), to exactly the scalar
  question `P_n^{(K)}(\text{both cyclic})\to\tau_K` — i.e. (ii) is not an
  independent target once (i) (or its analogue) is settled; it is a
  corollary away.
- **(i)** (`P_nn(n,2)`) is the sharpest well-posed scalar target of the
  three: Lemma P2 (`distributional_bridge_attempt`, PROVED, cited) already
  reduces the *entire* second-moment bridge question to this one number,
  for exactly the reason Estágio 27 names — "the entire existing K≥2
  machinery... is a single-point marginal device by construction... The
  genuinely new combinatorics needed... is exactly what
  [Estágio 18/25] already diagnosed."

This document attacks (i) directly, by extending Proposition 4/K1's
per-point case-split method from one arc to two — and finds, as the
dispatch anticipated, that a genuine K=2 closure of (i) hands over (ii) at
K=2 with no further probabilistic work (§6).

### 1.3 Notation (fixed once, matching Definition 4 and Lemma P2)

Work throughout in `THEOREM.md`'s Definition 4 (finite conditional-K model,
§7.2): `\pi` a uniform random permutation of `[n]=\{0,\dots,n-1\}`, the
`K=2` reroute sources fixed WLOG (Definition 4's own exchangeability
argument) at `\{0,1\}`, targets `U_0,U_1` i.i.d. `\mathrm{Unif}([n])`
independent of `\pi`, `f(i):=U_i` for `i\in\{0,1\}`, `f(i):=\pi(i)`
otherwise. Query points fixed WLOG at `\{n{-}2,n{-}1\}` (distinct from the
sources, requiring `n\ge4` — matching Lemma P2's own stated domain
`n>K+1`). Define

`P_{nn}(n,2) := P(n{-}2,\,n{-}1\text{ both cyclic for }f)`

— **exactly** Lemma P2's `P_{nn}(n,K)` at `K=2` (query points *strictly
disjoint* from the reroute sources, by construction). This is deliberately
distinguished (§6) from the different, but asymptotically-equivalent,
convention Proposition K1 uses (query points fixed, reroute sources a
uniform *unrestricted* `K`-subset that can coincide with a query point) —
conflating the two silently would be an error; §6 makes the relationship
precise and proves both converge to the same limit.

---

## 2. The Marked-Point Gap Structure Lemma (PROVED, new)

This is the tool that replaces `THEOREM.md` Proposition 4 Step 1
(`L\sim\mathrm{Unif}\{1,\dots,n\}`, valid for **one** marked point) once
several points must be tracked jointly.

> **Lemma 1 (Marked-Point Gap Structure).** Fix `m\ge1` distinguished
> points `S=\{s_1,\dots,s_m\}\subset[n]`. For a uniform random permutation
> `\pi` of `[n]`, define the **contracted permutation** `\sigma` on `S`:
> `\sigma(s)` is the first element of `S` encountered following `\pi`
> forward from `s` (i.e. `\sigma(s):=\pi^{k}(s)` for the smallest `k\ge1`
> with `\pi^k(s)\in S`) — well-defined since `\pi` is a permutation of a
> finite set. For each `s\in S` let `g(s)\ge0` be the number of
> **unmarked** points strictly between `s` and `\sigma(s)` (i.e.
> `\pi(s),\pi^2(s),\dots,\pi^{k-1}(s)`, all `\notin S`), and let
> `O := n-m-\sum_{s\in S}g(s)` be the number of points lying in cycles of
> `\pi` that contain **no** point of `S` at all. Then:
>
> (a) `\sigma` is a **uniform random permutation of `S`** (`m!` equally
>     likely outcomes).
>
> (b) `\sigma` and `\big(g(s_1),\dots,g(s_m),O\big)` are **independent**,
>     and the latter is **uniform** over all compositions of `n-m` into
>     `m+1` nonnegative parts (there are `\binom nm` such compositions).

*Proof.* Fix any specific topology `\sigma_0\in\mathrm{Sym}(S)` — say
`\sigma_0` decomposes `S` into cycles of sizes `k_1,\dots,k_t`
(`\sum k_i=m`) in some specific cyclic orders — and any specific gap sizes
`(g_1,\dots,g_m,O)` summing to `n-m` (`g_i:=g(s_i)`, indexed to match
`\sigma_0`'s cyclic order). Count the permutations `\pi` of `[n]` realizing
exactly this `(\sigma_0, g_1,\dots,g_m,O)`: choose which `\sum g_i` of the
`n-m` unmarked points are "inside" (fill the `m` gaps): `\binom{n-m}{\sum
g_i}` ways; arrange them, in order, into the `\sum g_i` gap-slots dictated
by `\sigma_0`'s cyclic structure (concatenating all gaps into one ordered
sequence to be filled, since each gap's slot order is fixed once the
specific points occupying it are chosen): `(\sum g_i)!` ways; arrange the
remaining `n-m-\sum g_i=O` "outside" points into an **arbitrary**
permutation of themselves (they may form any cycle structure at all,
since nothing distinguishes them): `O!` ways. Multiplying,

`\text{Count}(\sigma_0,g_1,\dots,g_m,O) = \binom{n-m}{\textstyle\sum g_i}\cdot\Big(\sum g_i\Big)!\cdot O! = \frac{(n-m)!}{(\sum g_i)!\,O!}\cdot\Big(\sum g_i\Big)!\cdot O! = (n-m)!`,

**independent of `\sigma_0` and of the specific `(g_1,\dots,g_m,O)`** — the
count is the *same* `(n-m)!` for every topology and every composition.
Summing over the `\binom nm` compositions of `n-m` into `m+1` nonnegative
parts, the total count for one fixed topology `\sigma_0` is
`(n-m)!\binom nm = n!/m!`; since `m!` topologies exist and every
permutation of `[n]` realizes exactly one `(\sigma,g_1,\dots,g_m,O)`
triple, the counts sum correctly to `n!` (`m!\times n!/m!=n!`), confirming
no double-counting or omission. Dividing by `n!`: `P(\sigma=\sigma_0,
g_1,\dots,g_m,O) = (n-m)!/n! = 1/[n!/(n-m)!]`, the **same** value for every
`(\sigma_0,g_1,\dots,g_m,O)` pair — proving both (a) (each of the `m!`
topologies has probability `1/m!`) and (b) (uniform over the `\binom nm`
compositions, independent of topology) simultaneously. `\blacksquare`

`m=1` recovers `THEOREM.md` Proposition 4 Step 1 exactly (`\sigma`
trivial; `g(s_1)+O=n-1`, uniform over the `n` compositions, i.e.
`L=g(s_1)+1\sim\mathrm{Unif}\{1,\dots,n\}`).

**Independent verification (exact enumeration, own fresh script,
`gap_lemma_unittest.py`).** Exhaustive enumeration of all `n!`
permutations, `m=2` (`n=2,\dots,7`) and `m=3` (`n=3,\dots,7`): for every
cell, both the topology distribution (uniform on `S_m`) and the gap-
composition distribution (uniform on the `\binom nm` compositions) are
confirmed exactly (`11/11` cells, `0` mismatches — see
`gap_lemma_unittest.log`).

---

## 3. The Two-Source Redirect-Structure Lemma (PROVED, new)

### 3.1 Setup: two sources cut a cycle structure into two arcs

Apply Lemma 1 with `S=\{0,1\}` (`m=2`): `\sigma` is uniform on
`\mathrm{Sym}(\{0,1\})` (two outcomes, each probability `\tfrac12`: `0,1`
share a cycle, or they don't — recovering the classical `P(\text{same
cycle})=\tfrac12` fact, already used throughout this lineage), and,
**independent of that**, `(g(0),g(1),O)` is uniform over compositions of
`n-2` into 3 nonnegative parts.

Define `p:=g(0)+1`, `q:=g(1)+1` (so `p,q\ge1`, `p+q\le n`, `O=n-p-q`). By
Lemma 1(b), **`(p,q)` is uniform over all pairs with `p,q\ge1,\,p+q\le n`**
(there are `\binom n2` such pairs, matching `\binom n2` compositions —
each with probability `1/\binom n2 = 2/[n(n-1)]`), **regardless of whether
`0,1` share a cycle or not** — this is the key simplification: the
redirect combinatorics below depend only on the abstract lengths `p,q`,
not on which of the two topologies produced them, so both cases can be
handled by one unified formula (independently re-derived and confirmed
identical for both topologies by direct counting; see the proof of Lemma
1, which gives `\text{Count}=(n-2)!` for either topology at fixed
`(p,q)`).

Concretely: let `\mathrm{arc}_1 := (e_1,\dots,e_p)` be the points strictly
after `0`, forward along `\pi`, up to and including `1` (`e_p=1`;
`\mathrm{arc}_1` is entirely within `0`'s cycle if `0,1` share one, else
`\mathrm{arc}_1=` all of `1`'s own cycle). Let `\mathrm{arc}_2:=(d_1,
\dots,d_q)` be the points strictly after `1`, forward along `\pi`, up to
and including `0` (`d_q=0`). Only `f(e_p)=f(1)=U_1` and `f(d_q)=f(0)=U_0`
differ from `\pi`; every other arc point's edge is the unaffected `\pi`
edge (`f(e_i)=e_{i+1}` for `i<p`, `f(d_i)=d_{i+1}` for `i<q`). Points
outside `\mathrm{arc}_1\cup\mathrm{arc}_2` are **automatically cyclic**
(their forward `f`-orbit never meets a reroute source — the exact `K=2`
generalization of Proposition 4 Step 2), regardless of `U_0,U_1`.

### 3.2 The 9-case redirect analysis

`U_0,U_1` each independently land in one of 3 places: **home**
(`U_0\in\mathrm{arc}_2`, `U_1\in\mathrm{arc}_1` — i.e. a source's own
tail redirects back into its own arc), **other** (`U_0\in\mathrm{arc}_1`,
`U_1\in\mathrm{arc}_2` — redirects into the *other* arc), or **outside**.
A direct trace of the resulting functional graph (worked from scratch,
not cited from any predecessor script) gives, for the `3\times3=9`
combinations:

| `U_0` \ `U_1` | home (`\in\mathrm{arc}_1`, pos. `k`) | other (`\in\mathrm{arc}_2`, pos. `l`) | outside |
|---|---|---|---|
| **home** (`\in\mathrm{arc}_2`, pos. `m`) | two separate self-cycles: `\{e_k,\dots,e_p\}` and `\{d_m,\dots,d_q\}` | one merged cycle: `\{e_j,\dots,e_p\}\cup\{d_l,\dots,d_q\}` (uses `U_0`'s own position `j\in\mathrm{arc}_1`) | arc1 self-cycle `\{e_k,\dots,e_p\}` only, arc2 dead |
| **other** (`\in\mathrm{arc}_1`, pos. `j`) | (same merged case, listed once) | arc2 self-cycle `\{d_m,\dots,d_q\}` only, arc1 dead | both dead (0 cyclic) |
| **outside** | arc1 self-cycle `\{e_k,\dots,e_p\}` only, arc2 dead | both dead | both dead |

("dead" = that arc's points feed into something and are never cyclic.) The
key derived fact, worked out by tracing each of the 9 cases explicitly
(full case-by-case trace in the proof below): **which points end up
cyclic depends only on `U_1`'s position when `U_1` lands home (`k`), or on
the pair `(j,l)` when both land "other" (the cross/merge case) — never on
`U_0`'s position when `U_0` lands home (`m`) affecting anything about
arc1, and vice versa** — an entry point into an already-self-consistent
arc does not change that arc's own eventual cycle.

> **Lemma 2 (Two-Source Redirect Structure; PROVED).** For arc lengths
> `p,q\ge1` in a universe of `n` points, writing `e_i,d_i` for arc-1/arc-2
> points at position `i` (interior, `1\le i\le p-1` resp. `1\le i\le q-1`):
>
> (R1) `P(e_i\text{ cyclic}) = i(n+q)/n^2`.
>
> (R2) `P(d_i\text{ cyclic}) = i(n+p)/n^2`.
>
> (R3) For `i<i'` both in `\mathrm{arc}_1`: `P(e_i,e_{i'}\text{ both
>      cyclic}) = i(n+q)/n^2` (the *nearer*-to-the-tail point's own
>      marginal — monotone containment, `e_i` cyclic `\Rightarrow` `e_{i'}`
>      cyclic, exactly generalizing Proposition K1's `\{c_j\text{
>      cyclic}\}\subseteq\{c_k\text{ cyclic}\}` fact).
>
> (R4) Symmetrically for two arc-2 points.
>
> (R5) For `i\in\mathrm{arc}_1`, `i'\in\mathrm{arc}_2`:
>      `P(e_i,d_{i'}\text{ both cyclic}) = 2ii'/n^2`.

*Proof (sketch of the trace; full case enumeration in the executive
summary's table above).* `e_i` (`i<p`) is cyclic iff **either** `U_1`
lands home in `\mathrm{arc}_1` at position `\le i` (probability `i/n`,
regardless of `U_0`: cases "home/home" and "home/other" for `U_0`, and
"outside" — all three give the arc1-self-cycle `\{e_k,\dots,e_p\}`
whenever `U_1=e_k`) **or** the merge case occurs (`U_0` other, at
`j\le i`, **and** `U_1` other, landing in `\mathrm{arc}_2`) — probability
`(i/n)\cdot(q/n)` by independence of `U_0,U_1`. Summing (the two events
are disjoint, since the first requires `U_1\in\mathrm{arc}_1`, the second
`U_1\in\mathrm{arc}_2`): `P(e_i\text{ cyclic}) = i/n + (i/n)(q/n) =
i(n+q)/n^2`. (R2) is symmetric (swap the roles of `U_0/U_1` and
`\mathrm{arc}_1/\mathrm{arc}_2`). For (R3): both events defining
`\{e_i\text{ cyclic}\}` are nested inside the corresponding events for
`e_{i'}` (`i<i'`) — `\{U_1=e_k,k\le i\}\subset\{U_1=e_k,k\le i'\}` and
`\{U_0=e_j,j\le i\}\subset\{U_0=e_j,j\le i'\}` — so `e_i` cyclic implies
`e_{i'}` cyclic, and `P(\text{both}) = P(e_i\text{ cyclic}) = i(n+q)/n^2`.
For (R5): only the two "cross" placements of the merge case
(`(U_0,U_1)=(\text{other at }j\le i,\text{other at }l\le i')`, or the
"two-separate-self-cycles" case `(U_0,U_1)=(\text{home at }m\le i',\text{
home at }k\le i)`) give **both** `e_i` and `d_{i'}` cyclic simultaneously
— every other one of the 9 cases leaves at least one of the two arcs
entirely non-cyclic (verified case-by-case in the table). Each contributes
`(i/n)(i'/n)` (independence of `U_0,U_1`), so `P(\text{both})=
2ii'/n^2`. `\blacksquare`

**Independent verification (exact enumeration over all `n^2` `(U_0,U_1)`
pairs, `redirect_structure_unittest.py`, no permutation/gap machinery
involved — a clean unit test of Lemma 2 alone).** All `120` `(n,p,q)`
configurations with `n=2,\dots,9`, `p,q\ge1,p+q\le n`: **every** instance
of (R1)–(R5) checked by exact `Fraction` equality — `0` mismatches across
every sub-formula and every configuration (`redirect_structure_unittest.log`).

---

## 4. Proposition NN2: the exact closed form (PROVED)

Combining Lemma 1 (`(p,q)` uniform on the `\binom n2` pairs) with Lemma 2
and Lemma 1's own position-placement fact (used a second time, at `m=4`
implicitly: given `(p,q)`, the remaining `n-2` non-source points are
placed into the `p-1` arc-1 slots, `q-1` arc-2 slots, and `O=n-p-q`
outside slots via a **uniform random bijection** — this is exactly the
`\text{Count}=(n-4)!` refinement of Lemma 1's own proof, applied to locate
the two *specific* query points `n{-}2,n{-}1` among the `n-2` non-source
points): for any two **specific**, distinct roles (out of the `n-2`
available), `P(\text{query 1}\to\text{role }R_1,\text{query
2}\to\text{role }R_2) = 1/[(n-2)(n-3)]`, the same for every ordered pair
of distinct roles.

Writing `T(p,q) := \sum_{R_1\ne R_2}(\text{value at }R_1,R_2)` (summed
over all ordered pairs of the `n-2` roles, using Lemma 2's (R1)–(R5) and
the trivial value `1` when a role is "outside"):

`T(p,q) = O(O{-}1) + \frac{O(n{+}q)p(p{-}1)+O(n{+}p)q(q{-}1)}{n^2} + \frac{(n{+}q)p(p{-}1)(p{-}2)+(n{+}p)q(q{-}1)(q{-}2)}{3n^2} + \frac{p(p{-}1)q(q{-}1)}{n^2}`

(`O=n-p-q`; derivation of each term — outside/outside, outside/arc,
same-arc, cross-arc — is direct bookkeeping from Lemma 2, `T(p,q)`'s exact
expansion recorded in `symbolic_sum_pnn2.py`/`.log`), and

`P_{nn}(n,2) = \frac{2}{n(n-1)}\sum_{p=1}^{n-1}\sum_{q=1}^{n-p}\frac{T(p,q)}{(n-2)(n-3)}`.

> **Proposition NN2 (PROVED).** For every `n\ge4`:
> `\displaystyle P_{nn}(n,2) = \frac{10n^2+7n+2}{30n^2} = \frac13+\frac{7}{30n}+\frac1{15n^2}`.

*Derivation.* Exact symbolic double summation in `sympy` (exact `Rational`
arithmetic throughout, no floating point at any stage —
`symbolic_sum_pnn2.py`): `T(p,q)` expanded, summed over `q=1,\dots,n-p`
(closed form in `n,p`), then summed over `p=1,\dots,n-1`, giving
`\sum_{p,q}T(p,q) = \dfrac{10n^5-53n^4+70n^3+5n^2-20n-12}{60n}`; dividing
by `n(n-1)(n-2)(n-3)/2` and simplifying (`sympy.simplify`+`factor`) gives
the stated closed form directly, with no further hand simplification
needed. `\blacksquare`

**Corollary NN2.0 (rate, PROVED, immediate from the closed form).**
`n\big(P_{nn}(n,2)-\tfrac13\big) \to \tfrac7{30}` — an exact `\Theta(1/n)`
rate, the same order (though a different coefficient) as every other
second-moment-type quantity found `\Theta(1/n)` elsewhere in this lineage
(Proposition K1's `K=1` rate `-1/6`; contrast the *marginal*
`\psi_n^{(2)}`'s own `\Theta(1/n)` rate `4/15`, `THEOREM.md` Estágio 3).

### 4.1 Independent verification (exact brute force, `n` up to 9)

Fresh, from-scratch enumeration of the *entire* Definition 4 K=2 model
(`brute_force_k2.py` — every one of the `n!\cdot n^2` `(\pi,U_0,U_1)`
configurations, exact `Fraction` counting, **no code read from any other
front**):

| `n` | configs | `P_{nn}(n,2)` (brute force) | Proposition NN2 predicts | match | `\psi_n^{(2)}` (marginal, brute force) | `THEOREM.md` `8/15+4/(15n)+1/(15n^2)` | match |
|---|---|---|---|---|---|---|---|
| 4 | 384 | `19/48` | `19/48` | ✓ | `29/48` | `29/48` | ✓ |
| 5 | 3,000 | `287/750` | `287/750` | ✓ | `221/375` | `221/375` | ✓ |
| 6 | 25,920 | `101/270` | `101/270` | ✓ | `313/540` | `313/540` | ✓ |
| 7 | 246,960 | `541/1470` | `541/1470` | ✓ | `421/735` | `421/735` | ✓ |
| 8 | 2,580,480 | `349/960` | `349/960` | ✓ | `109/192` | `109/192` | ✓ |
| 9 | 29,393,280 | `175/486` | `175/486` | ✓ | `137/243` | `137/243` | ✓ |

**`6/6` exact rational matches** for `P_{nn}(n,2)` (Proposition NN2), and
`6/6` for the marginal `\psi_n^{(2)}` cross-check against `THEOREM.md`'s
already-proved formula (the latter also validates the brute-force script's
basic correctness, since it independently reproduces a fact proved by a
completely different method — Estágio 3's transfer-matrix machine — in
`THEOREM.md`). `n=9` (`29.4` million exact configurations) is a genuinely
new data point beyond any table in this lineage's K=2 second-moment work
(`brute_force_k2.log`).

### 4.2 Large-`n` Monte Carlo triangulation (bonus, not a substitute for §4.1)

`monte_carlo_k2.py`, reserved seeds `20260880001`–`20260880003`:

| `n` | trials | `\hat P(\text{both})` | s.e. | `z` vs `1/3` | `\hat P(\text{same})` | s.e. | `z` vs `1/6` |
|---|---|---|---|---|---|---|---|
| 200 | 200,000 | 0.33416 | 0.00105 | +0.79 | 0.16860 | 0.00084 | +2.31 |
| 2,000 | 30,000 | 0.33393 | 0.00272 | +0.22 | 0.16527 | 0.00214 | −0.65 |
| 5,000 | 10,000 | 0.32800 | 0.00469 | −1.14 | 0.16460 | 0.00371 | −0.56 |

All within `\approx2.3\sigma` of the exact targets `1/3,1/6` proved above —
consistent, not itself proof (exact brute force + exact symbolic
resummation are the actual evidence; this is triangulation, per lineage
convention).

---

## 5. Corollary NN2.1: closes Estágio 27's K=2 second-moment item (PROVED)

`THEOREM.md` Estágio 27 diagnosed precisely: "`K\ge2` honestly open (both
the full CDF bridge and even just `P_{nn}(n,K)\to1/(K{+}1)`)... needs
either a whole-space K=2 case analysis in Proposition D1's style or a
genuine joint two-point exploration." Proposition NN2 (§4) **is** that
case analysis, and its immediate consequence:

> **Corollary NN2.1 (PROVED).** `P_{nn}(n,2)\to\tfrac13=\tfrac1{K+1}
> \big|_{K=2}`. By Lemma P2 (`distributional_bridge_attempt` §6.2, PROVED,
> cited — `E[(M_n^{(K)})^2]\to\lim_nP_{nn}(n,K)` whenever the latter
> exists, for fixed `K`, since the `P_{nr},P_{rr}`-weighted terms are
> `O(K/n)\to0`), `E[(M_n^{(2)})^2]\to\tfrac13=E[M_2^2]` (the continuum
> value, already PROVED directly on `L(c)` at Estágio 24).

This closes, **at K=2 specifically**, the second-moment half of Estágio
27's named open item. The **full CDF** bridge at K=2 (Proposition D1's
*entire distributional* result, not just its second moment) remains open
— §7 states precisely why this document does not attempt it.

---

## 6. Corollary NN2.2: target (ii), the K=2 continuum transfer (PROVED)

### 6.1 Direct route, via the `P_nn` convention

Theorem J's Corollary (Estágio 25, cited, PROVED there, **exact at every
finite `n,K`**, for *any* fixed distinct `i,j\in[n]` — the proof never
assumes `i,j\notin R`): applied with `i,j=n{-}2,n{-}1` (this document's own
`P_{nn}` query pair, always disjoint from the K=2 reroute sources by
construction),

`P_{nn\text{-same}}(n,2) := P_n^{(2)}(n{-}2,n{-}1\text{ both cyclic, same final cycle}) = \tfrac12 P_{nn}(n,2) = \frac{10n^2+7n+2}{60n^2}`,

**exactly**, for every `n\ge4` — no new probability needed beyond
Proposition NN2 and the cited Corollary. Hence:

> **Corollary NN2.2 (PROVED).**
> `\displaystyle P_{nn\text{-same}}(n,2) \to \frac16 = \frac1{2(K{+}1)}\Big|_{K=2}`.

This is exactly Estágio 28's target quantity, extended from `K=0,1` (where
Estágio 28 proved `1/2,1/4`) to `K=2` (`1/6`) — matching the value
`E[M_K^2]/2` the continuum theory already predicts for every `K`
(Estágio 24 + the Fubini device `THEOREM.md` §2.4 / Estágio 28 §1).

### 6.2 The other convention: a bonus reduction lemma (PROVED) closes it too

Estágio 28's own Proposition K1 uses a **different** finite-`n` proxy:
query points fixed at `\{0,1\}`, but the K=2 reroute-source set `R` a
uniform random 2-subset of **all** of `[n]` (allowed to intersect
`\{0,1\}`) — call this quantity `P_n^{(2)}(\text{both})` (Estágio 28's own
notation). This is *not* the same finite-`n` number as `P_{nn}(n,2)`
(confirmed by fresh brute force below, §6.3), but it converges to the
*same* limit, by a one-line reduction in the exact style of `THEOREM.md`
Estágio 3's Reduction Lemma A / Lemma P2:

> **Lemma 3 (Overlap-Reduction; PROVED, elementary).** For fixed `K`, as
> `n\to\infty`: `P(R\cap\{0,1\}=\emptyset) = \binom{n-2}{K}/\binom
> nK\to1`, so `P_n^{(K)}(\text{both}) = P(R\cap\{0,1\}{=}\emptyset)\cdot
> P_{nn}(n,K) + \big(1-P(R\cap\{0,1\}{=}\emptyset)\big)\cdot(\text{a
> quantity bounded in }[0,1]) \to \lim_n P_{nn}(n,K)`, whenever the latter
> limit exists.

*Proof.* Total probability, exactly as Lemma P2's own proof splits
`E[C^2]` by pair type; `P(R\cap\{0,1\}=\emptyset)=\binom{n-2}K/\binom
nK\to1` for fixed `K` (elementary, e.g. `\binom{n-2}2/\binom n2 =
(n-2)(n-3)/[n(n-1)]\to1` at `K=2`), and the complementary weight is
bounded by a probability (`\in[0,1]`) times a probability (`\in[0,1]`), so
its contribution `\to0`. `\blacksquare`

Applied at `K=2` with Proposition NN2 (`\lim_n P_{nn}(n,2)=1/3`
PROVED, §4):

> **Corollary NN2.3 (PROVED).** `P_n^{(2)}(\text{both})\to\tfrac13` (in
> Estágio 28's own, overlap-allowed convention) — closing, at the level of
> the *limit* (not the exact rate/closed form), the item Estágio 28 §4
> left as "NUMERICALLY EXPLORED... not proof": `\tau_K=1/(K{+}1)` for
> `K\ge2`, at `K=2` specifically. Combined with Estágio 28's own
> Proposition R (cited): `P_n^{(2)}(\text{same})\to\tfrac16` in **that**
> convention too.

So both finite-`n` conventions used across this lineage for the K=2
same-cycle question converge to the identical continuum value `1/6` — this
document proves it for `P_{nn}` directly (exact closed form, §4) and for
Estágio 28's own convention via Lemma 3 (limit only, no closed form
attempted there).

### 6.3 Verification that the two conventions really are different numbers

`brute_force_k2_overlap.py` (fresh, own script), Estágio 28's own
convention, `n=4,\dots,7`: **`49/144, 33/100, 44/135, 143/441`** — these
are **exactly** the four values Estágio 28 §4.1 itself reports (an
independent reproduction, from a from-scratch script, of a table this
front did not read the code for), and they are visibly **different** from
this front's own `P_{nn}(n,2)` at the same `n` (`19/48, 287/750, 101/270,
541/1470` — e.g. at `n=4`: `49/144\approx0.340` vs `19/48\approx0.396`).
Both series are heading toward the same `1/3\approx0.333` (Lemma 3), just
along different finite-`n` paths — exactly the same qualitative pattern
already on record for `K=1` in this lineage (`P_{nn}(n,1)=\tfrac12+
\tfrac1{6n}` vs Proposition K1's `\tfrac12-\tfrac1{6n}+\tfrac1{3n^2}`, both
`\to\tfrac12`, `distributional_bridge_attempt` §7.1(c) vs
`joint_exploration_continuum_attempt` §3.2).

---

## 7. What did NOT close, precisely (honest, as mandated)

### 7.1 `K=3`: where the case-split genuinely gets harder

For `K=2`, the redirect structure needed only a `3\times3` table (each of
`U_0,U_1` lands home/other/outside), because with exactly 2 arcs, "other"
has a unique meaning (the *one* other arc). For `K=3` sources, three arcs
`\mathrm{arc}_1,\mathrm{arc}_2,\mathrm{arc}_3` exist, and each of `U_0,U_1,
U_2` independently lands in **one of `K{+}1=4` destinations** (its own
arc, either of the *other two* arcs, or outside) — a `4\times4\times4=64`-
cell table, but the genuine new difficulty is not the cell count: it is
that **which points end up cyclic now depends on the *global* structure of
which arc's tail feeds into which other arc**, i.e. on the induced
functional graph on the 3 arcs themselves (`\{1,2,3\}\to\{1,2,3,\text{
DEAD}\}`, where arc `i`'s image is "home"=`i`, "other"=the specific other
arc its tail landed in, or DEAD=outside). Cyclic points now correspond to
**cycles of this 3-node functional graph** (a source can chain through
*two* other arcs before closing, not just one directly), and the
`K=2` case's clean fact "an arc's own eventual cycle doesn't depend on
where an incoming chain entered it" needs to be re-derived for chains that
pass through an intermediate arc first. This is genuinely the same order
of combinatorial growth `THEOREM.md` already met at the *marginal* level
(Estágio 3's manual K=2 case analysis giving way to Estágio 4's uniform-in-
K transfer-matrix method for `K\ge3`) — but **compounded**, since a
transfer-matrix-style solution here would need to track *two* query-point
positions through the same state space, not zero (the marginal problem
never needed to track any query point at all, only whether the *reference*
point itself survives). **No attempt at `K=3` was made in this document**
beyond this diagnosis; a genuine next step would be adapting Estágio 4's
uniform-in-K machinery (`(a,b,r)`-state Markov chain) to carry two
additional state variables for the two query points' cyclic status —
concretely named, not attempted here for lack of budget.

### 7.2 The full CDF at K=2 (Proposition D1's whole-distribution generalization)

Proposition NN2 gives only the **second moment** contribution
(`P(\text{two specific points both cyclic})`), not the full law of
`T=\#\{\text{cyclic points}\}`. Proposition D1 (`distributional_bridge_
attempt`, K=1) got the *entire* CDF `P(T\le k)` in closed form by tracking
a *single* arc's within-arc case split directly on the count `T`, not just
pairwise. Generalizing that (rather than the pairwise `P_{nn}` machinery
built here) to K=2 would need the *whole* joint distribution of which
`\mathrm{arc}_1\cup\mathrm{arc}_2` positions are cyclic (as a random
**subset**, not just two fixed points' joint indicator) — a strictly
harder target this document does not attempt. Lemma 2 (§3) is a genuine
step toward it (it already gives the *pairwise* joint law for **any** two
positions, same arc or different), but assembling a full count
distribution from pairwise data requires the entire correlation structure
(all `\binom{p+q}{2}` pairs simultaneously, or an inclusion–exclusion /
generating-function argument over subsets) — not carried out here.

### 7.3 Target (iii): the general joint two-point law at K=2

Not attacked directly. Lemma 2 (§3) *is* genuinely progress toward it — it
gives the exact joint cyclicity law of **any** two points relative to the
two-source redirect structure, which is a real piece of "the general joint
two-point law" — but a full closure of (iii) would need this combined with
the *general* (not just K=2) marked-point machinery of Lemma 1 at
arbitrary `K`, plus the K≥3 redirect-structure generalization named as
open in §7.1. This document reports Lemma 1 and Lemma 2 as reusable,
K-general (Lemma 1) or K=2-specific (Lemma 2) building blocks for a future
attempt at (iii), not as a solution to it.

### 7.4 What is explicitly NOT claimed

No claim that Proposition NN2 extends past K=2. No claim about the rate of
convergence of Estágio 28's own overlap-allowed convention (only the limit,
via Lemma 3). No claim about any moment beyond the second. No claim of any
kind about a Millennium Problem.

---

## 8. Relationship among the three original targets, as actually found

The dispatch's own hypothesis — "a full solution to the K=2 case-split for
(i) likely yields or nearly yields (ii) as well" — is **confirmed exactly**
here (§6): once Proposition NN2 (i) is proved, (ii) follows from a single
already-proved citation (Theorem J's Corollary) with no new probability.
Target (iii) is *not* subsumed — Lemma 2 is real partial progress toward
it (the exact pairwise law for K=2), but the *general* joint two-point law
(any K, or even just "the whole distribution," not a single pair) remains
a strictly larger problem than (i)+(ii) together, as diagnosed precisely
in §7.2–7.3.

---

## 9. Seeds

Reserved range: `20260880000`–`20260880999` (this front's own; referee
range `20260881000+` untouched). Grep-confirmed unused before first use:

```
$ grep -rn "20260880" 05_DISCOVERY_LAB/
```

returned only the governance reservation lines (`DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`) before this front's own files existed. Only
`monte_carlo_k2.py` uses randomness (Python's `random.Random`, seeded
explicitly per cell, no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `gap_lemma_unittest.py` | none (exhaustive) | Lemma 1 verification |
| `redirect_structure_unittest.py` | none (exhaustive) | Lemma 2 verification |
| `symbolic_sum_pnn2.py` | none (symbolic) | Proposition NN2 derivation |
| `brute_force_k2.py` | none (exhaustive) | Proposition NN2 cross-check, `n=4..9` |
| `brute_force_k1_check.py` | none (exhaustive) | disambiguates `P_nn` vs overlap-allowed conventions at K=1 |
| `brute_force_k2_overlap.py` | none (exhaustive) | §6.3, reproduces Estágio 28's own K=2 table independently |
| `monte_carlo_k2.py` | `20260880001`, `20260880002`, `20260880003` | §4.2 large-`n` triangulation |

---

## 10. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `gap_lemma_unittest.py` / `.log` | Lemma 1, exhaustive verification, `m=2,3`, `n` up to 7 |
| `redirect_structure_unittest.py` / `.log` | Lemma 2, exhaustive verification over all `n^2` `(U_0,U_1)` pairs, `120` `(n,p,q)` configurations |
| `symbolic_sum_pnn2.py` / `.log` | Proposition NN2's exact symbolic derivation (`sympy`), numeric table `n=4..11` |
| `brute_force_k2.py` / `.log` | fresh exhaustive Definition-4 K=2 enumeration, `P_nn(n,2)` and marginal `\psi_n^{(2)}` cross-check, `n=4..9` |
| `brute_force_k1_check.py` / `.log` | K=1 disambiguation of the two finite-`n` conventions (`P_nn` vs overlap-allowed) |
| `brute_force_k2_overlap.py` / `.log` | independent reproduction of Estágio 28's own K=2 convention/table, `n=4..7` |
| `monte_carlo_k2.py` / `.log` / `_results.json` | large-`n` Monte Carlo triangulation, reserved seeds |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Lemma 1 (Marked-Point Gap Structure, general `m`) | **PROVED** |
| 2 | Lemma 2 (Two-Source Redirect Structure, (R1)–(R5)) | **PROVED** |
| 3 | Proposition NN2 (`P_{nn}(n,2)=(10n^2+7n+2)/(30n^2)`) | **PROVED** |
| 4 | Corollary NN2.0 (rate `\Theta(1/n)`, coefficient `7/30`) | **PROVED** |
| 5 | Corollary NN2.1 (`E[(M_n^{(2)})^2]\to1/3`, closes Estágio 27's K=2 2nd-moment item) | **PROVED** |
| 6 | Corollary NN2.2 (`P_{nn\text{-same}}(n,2)\to1/6`, target (ii) at K=2) | **PROVED** |
| 7 | Lemma 3 (Overlap-Reduction, general K) | **PROVED** |
| 8 | Corollary NN2.3 (Estágio 28's own convention also `\to1/3,1/6` at K=2) | **PROVED** (limit only, not rate) |
| 9 | Full CDF of `M_n^{(2)}` (Proposition D1-style, K=2) | **OPEN** (precisely scoped, §7.2) |
| 10 | K=3 redirect structure / case-split | **OPEN** (precisely diagnosed, §7.1) |
| 11 | Target (iii), general joint two-point law | **OPEN** (partial tools supplied — Lemma 1, Lemma 2 — not a solution) |
| 12 | Rate/closed form of Estágio 28's overlap-allowed convention at K=2 | **OPEN** (not attempted; only its limit is proved, via item 7-8) |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
or `DISCOVERY_LAB_STATE.md`. No `adversarial/` subdirectory created, no
referee dispatched by this front. No git command run. No `.py` file from
any other front was read, opened, or imported — every script in this
directory is written fresh from the mathematical prose of `THEOREM.md` and
the two named predecessor `ATTEMPT.md` files' descriptions only. Every
claim above is labeled PROVED / OPEN at the point of use; no claim is left
as an unlabeled assertion. No claim of progress on any Millennium Problem;
this is pure combinatorial mathematics internal to the u12 ensemble
defined in `THEOREM.md`.
