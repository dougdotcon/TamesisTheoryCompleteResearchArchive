# Joint two-point exploration, attempted again — a proved finite-`n` structural theorem, and why the moment targets stay open

> **Governance.** Wave 17, front (c) (`JOINT-TWO-POINT-EXPLORATION-ATTEMPT`),
> authorized by `DISC-DEC-072` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. This front
> continues (does not blindly reuse) a stalled prior instance's work in
> this same directory: `PREREG.md`, `symbolic_checks.py/.log` and
> `finite_n_exact_enum.py/.log` predate this document and were written by
> that earlier, non-terminating attempt. Per the dispatch instructions,
> neither partial script was assumed correct; both were **independently
> redone from scratch** below (`uniform_cyclic_restriction_exact.py`,
> which re-derives and substantially extends `finite_n_exact_enum.py`'s
> checks; `poisson_continuum_same_diff_mc.py`, a fresh MC harness). The
> old `symbolic_checks.py` (an internal-consistency check of the
> conjectured-law target values, not a derivation from first principles)
> was read for orientation but not relied upon; nothing below cites its
> output. `PREREG.md`'s ambitious S1–S7 program (a candidate full
> two-walker derivation) was **not** completed or adopted wholesale — see
> §7 for exactly what survives from it and what does not. Every claim
> below is labeled PROVED, CITED (a named classical fact used without
> re-derivation, same rigor level `THEOREM.md` itself uses), NUMERICALLY
> EXPLORED (exploratory data, never offered as evidence toward a proof of
> Conjecture 1 or 2 themselves), or OPEN. `THEOREM.md` is **not** edited
> by this document, nor is any ledger or governance file. No git command
> was run. Seeds used: `20260864000`, `20260864001` (this front's
> reserved block `20260864000+`, grep-confirmed unused before first use —
> the only prior occurrences of `"20260864"` in the archive were the two
> reservation lines in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` and this
> front's own `PREREG.md`, none of which is a use). The referee range
> `20260865000+` was **not** used. No `adversarial/` subdirectory was
> created and no referee was dispatched, per mandate.

> **Executive summary (read first).** The mandate's primary targets, in
> order of value, were: (1) `E[M(c)^2]=(1-e^{-c})/c` unconditionally; (2)
> `E[M_K^2]=1/(K+1)` for all `K` unconditionally; (3) any rigorous partial
> structure of the two-point joint law. **Targets (1) and (2) are NOT
> closed here** — see §6 for exactly why, and confirmation that
> `THEOREM.md`'s latest state (Estágio 22, 2026-08-25) still lists
> Conjecture 1 (`K\ge5`) and Conjecture 2 as open, with no closure to
> pivot away from. **Target (3) is achieved, with a genuinely new result
> that was not in `THEOREM.md`, in `conjecture2_direct_attempt/ATTEMPT.md`
> (Estágio 18), or in this front's own stalled `PREREG.md`:**
>
> 1. **A new PROVED theorem** — the *Uniform Cyclic Restriction Theorem*
>    (§2): in the finite conditional-`K` model (`THEOREM.md` Definition
>    4), conditional on the realized final cyclic point set `C(f)=c`
>    (any subset with `|c|=m\ge2`), the permutation `f` induces on `c` is
>    **exactly uniformly distributed** over all `m!` bijections of `c` —
>    for *every* `n` and `K`, not just asymptotically. Proved by an
>    elementary, fully explicit bijective/symmetry argument (§2.2), not
>    merely observed numerically.
> 2. **Corollary (§3):** `P(\text{two fixed points same final cycle} \mid
>    \text{both cyclic}) = 1/2` **exactly**, for every finite `n\ge2` and
>    every `0\le K\le n` — a strict strengthening of Estágio 18's Lemma B1
>    (which only concerned the *unconditional, background-only*
>    permutation `\pi`, not the actual rerouted functional graph
>    conditioned on both points surviving).
> 3. **Exhaustive computational confirmation:** zero violations across 21
>    exhaustively-enumerated `(n,K)` pairs, `n=3,\dots,7`, `K=0,\dots,5`
>    (including the `K=n` boundary), independently redone in this session
>    (§4.1).
> 4. **Fresh Monte Carlo evidence (§5)** that the same 50/50 split also
>    holds, empirically, in the large-`n` regime standing in for the
>    continuum `L(c)` — at `c=2` (not used by Estágio 18) and `c=1`
>    (cross-check), both within ~0.2pp of `1/2`.
> 5. **A sharpened diagnosis of the standing obstruction (§6):** the
>    *same/different-cycle split given both-cyclic* piece of the
>    two-point joint law is now closed exactly, at the finite-`n` level.
>    What remains open — precisely localized, narrower than Estágio 18's
>    statement — is the *value* `P(\text{both cyclic})` itself (equivalently
>    `E[M_K^2]`), which requires a genuinely different computation (the
>    actual survival/reroute dynamics), **not** anything the new theorem
>    touches; and separately, whether the finite-`n` theorem transfers to
>    the continuum `L(c)` rigorously (via the pre-existing, independently
>    open `n\to\infty` bridge, `THEOREM.md` §7, or via a genuine
>    continuum-native two-point construction from Definition 3's
>    primitives — attempted briefly here and explicitly not completed,
>    §6.3).
> 6. **One self-caught false start**, reported honestly (§7.1): an
>    initial attempt to prove the theorem via a "freeze everything outside
>    `c`, swap the permutation on `c`" bijection *fails* in general
>    (changing the permutation on `c` can silently break the injectivity
>    constraint used to define the model when reroute-domain points
>    outside `c` collide with the new images) — the fix (post-composition
>    by a fixed bijection, which preserves the *law*, not naive
>    freeze-and-swap, which only preserves *cardinality* under an
>    unjustified assumption) is what §2.2 actually uses.
>
> **Net verdict: honest non-closure of the mandate's primary numbered
> targets, with a new, fully proved, non-trivial piece of exact finite-`n`
> two-point structure — squarely target (3), and a genuine (if partial)
> narrowing of Estágio 18's obstruction.** See §8 for the complete
> scorecard.

---

## 0. What this front inherited, and what it does with it

The directory already contained, from a prior stalled instance of this
same front:

- `PREREG.md` — a pre-registration proposing an ambitious "sequential
  two-walker exploration" derivation (steps S1–S7) aimed directly at the
  mandate's targets (1)/(2), built on Definition 3's `(\Theta,E)`
  hazard-clock primitives extended to two simultaneous reference points.
- `symbolic_checks.py`/`.log` — `sympy` checks that the *numbers*
  appearing in S2–S6 integrate consistently with each other and with the
  conjectured law's known moments. All checks pass, but — as the script's
  own docstring makes clear and as re-read here — **these check internal
  arithmetic consistency of the proposed formulas, not whether the
  underlying probabilistic claims (the actual two-walker exploration
  process, S1 and S3 in particular) are correct constructions from
  Definition 2/3's primitives.** No claim in `symbolic_checks.log` is
  used below as evidence for anything.
- `finite_n_exact_enum.py`/`.log` — exact enumeration for `K=1` (`n=3..7`)
  and `K=2` (`n=3..6`) of `P_both`, `P_same`, `P_diff` for two fixed
  points, finding `P_same=P_diff` exactly at every tested `n`. This *is*
  a genuine, correct, load-bearing data point — but per the mandate's
  explicit instruction not to assume the partial scripts are correct, it
  is **not relied upon**; §4.1 below independently re-derives the same
  fact from scratch, with a different implementation, extended range
  (`K` up to 5, including the `K=n` boundary), and — the actual point of
  this document — an accompanying *proof* of why it is exactly `1/2`,
  which the prior attempt did not have.

**What this front concluded about `PREREG.md`'s S1–S7 program.** Reading
it carefully (§7 below), S1 ("conditional on `x_1` cyclic with closure
mass `t`, the explored region is exactly the cycle of `x_1`, with mass
exactly `t`") is precisely the claim that Estágio 18 identified as the
genuine obstruction — a physical-geometry statement about Definition 2's
literal construction that Definition 3's `(\Theta,E)` proxies are not
obviously entitled to make (Definition 3 is a computational surrogate for
the *marginal* law of one point; asserting that its internal state `T_0`
equals the physical Lebesgue measure of a specific subset of the circle,
without re-deriving this from Definition 2, is exactly the step Estágio
18 could not complete). This document does **not** resolve that step
either — but §2 below finds a genuinely different, self-contained route
into a *piece* of the same target (the same/different-cycle split), that
sidesteps the destination-information obstruction entirely by working in
the finite-`n` combinatorial model directly, where "cyclic set" and "the
permutation induced on it" are unambiguous finite objects requiring no
extension of Definition 3's proxies at all.

---

## 1. Setup

Work throughout (§§2–4) in `THEOREM.md`'s **Definition 4** (the finite
conditional-`K` model): fix `n\ge2` and `0\le K\le n`. Let `\pi` be a
uniform random permutation of `[n]:=\{0,1,\dots,n-1\}`. Let `R\subseteq[n]`,
`|R|=K`, be a uniform random `K`-subset, independent of `\pi`. For
`i\in R` let `U_i` be i.i.d. `\mathrm{Uniform}([n])`, independent of
`(\pi,R)`. Define

`f(i) := U_i` if `i\in R`,  `f(i) := \pi(i)` if `i\notin R`.

A point `i` is **cyclic** iff its forward `f`-orbit returns to `i` in
finitely many steps (automatic, since `[n]` is finite: every forward
orbit eventually repeats, and `i` is cyclic iff the first repeat is `i`
itself). Write `C(f)\subseteq[n]` for the set of cyclic points — a
disjoint union of directed cycles of `f`, i.e. `f` restricted to `C(f)`
is a **bijection** `C(f)\to C(f)` (elementary: a point that eventually
returns to itself under repeated `f`-application, together with every
point on that literal return path, forms a genuine cycle of the
functional graph — standard structure theory of finite functional
graphs, used without further comment throughout `THEOREM.md` itself, e.g.
Estágio 18 Lemma B4).

---

## 2. The Uniform Cyclic Restriction Theorem

> **Theorem J (Uniform Cyclic Restriction; PROVED).** Fix `n,K` with
> `0\le K\le n`, and fix a subset `c\subseteq[n]` with `m:=|c|\ge2` and
> `P(C(f)=c)>0`. Under Definition 4's model, conditional on `\{C(f)=c\}`,
> the restriction `f|_c` (a bijection `c\to c`) is distributed **exactly
> uniformly** over `\mathrm{Sym}(c)` — every one of the `m!` bijections
> equally likely.

### 2.1 Two ingredients

**Lemma J1 (post-composition invariance of `f`'s law; PROVED,
elementary).** For any fixed bijection `\kappa:[n]\to[n]`,
`\kappa\circ f \overset{d}{=} f`.

*Proof.* Define `\pi' := \kappa\circ\pi`, `R':=R`, `U'_i := \kappa(U_i)`
for `i\in R`. Since left-multiplication by a fixed element is a bijection
of any group onto itself, `\pi\mapsto\kappa\pi` is a bijection of
`\mathrm{Sym}(n)` onto itself, so `\pi'\sim\mathrm{Uniform}(\mathrm{Sym}(n))`
exactly (a uniform measure pushed forward by a bijection of the group
onto itself is the same uniform measure). `R'=R` is unchanged. `U'_i =
\kappa(U_i)` is `\mathrm{Uniform}([n])`, since `\kappa` is a bijection of
`[n]` and `U_i\sim\mathrm{Uniform}([n])`; the `U'_i` remain i.i.d. across
`i\in R` (each is a fixed deterministic function of the corresponding
independent `U_i`) and independent of `\pi'` (each `U'_i` is a
deterministic function of `U_i` alone, and `U_i` is independent of `\pi`
by construction, hence of `\pi'=\kappa\pi`, a deterministic function of
`\pi`). So `(\pi',R',\{U'_i\}) \overset{d}{=} (\pi,R,\{U_i\})` — an
**exact distributional identity**, not merely equal marginals: every
independence relationship Definition 4 stipulates for `(\pi,R,\{U_i\})`
is reproduced verbatim for `(\pi',R',\{U'_i\})`, by the argument just
given for each piece separately. Now observe that the map `f'` built
from `(\pi',R',\{U'_i\})` via Definition 4's own recipe satisfies, for
every `i\in[n]`: if `i\in R`, `f'(i)=U'_i=\kappa(U_i)=\kappa(f(i))`; if
`i\notin R`, `f'(i)=\pi'(i)=\kappa(\pi(i))=\kappa(f(i))`. So `f'=\kappa\circ f`
identically (as functions, for every realization). Since
`(\pi',R',U')\overset{d}{=}(\pi,R,U)`, and `f`/`f'` are the *same*
deterministic function of the respective primitive tuples, `f' \overset{d}{=} f`,
i.e. `\kappa\circ f \overset{d}{=} f`. `\square`

**Lemma J2 (the swap bijection; PROVED, elementary).** Fix `c\subseteq[n]`,
`\rho\in\mathrm{Sym}(c)`, and a transposition `(x\,y)` with `x,y\in c`,
`x\ne y`. Let `\kappa := (\rho(x)\ \rho(y))` (the transposition of `[n]`
swapping the two *values* `\rho(x),\rho(y)\in c`, fixing everything
else), and `\rho' := \rho\circ(x\,y)` (so `\rho'(x)=\rho(y)`,
`\rho'(y)=\rho(x)`, `\rho'(z)=\rho(z)` for `z\in c\setminus\{x,y\}`). Then
`h \mapsto \kappa\circ h` is a bijection

`\{h:[n]\to[n] \mid C(h)=c,\ h|_c=\rho\} \ \longrightarrow\ \{h:[n]\to[n] \mid C(h)=c,\ h|_c=\rho'\}`,

with inverse `h'\mapsto\kappa\circ h'` (the same map — `\kappa` is an
involution).

*Proof.* Let `h` satisfy `C(h)=c`, `h|_c=\rho`, and set `g:=\kappa\circ h`.

*Restriction on `c`.* For `z\in c\setminus\{x,y\}`: `h(z)=\rho(z)\notin\{\rho(x),\rho(y)\}`
(injectivity of `\rho`), so `\kappa` fixes it: `g(z)=\rho(z)=\rho'(z)`.
For `z=x`: `g(x)=\kappa(\rho(x))=\rho(y)=\rho'(x)`. For `z=y`:
`g(y)=\kappa(\rho(y))=\rho(x)=\rho'(y)`. So `g|_c=\rho'` exactly, a
bijection `c\to c`.

*Cyclic set unchanged.* For `i\notin c`: if `h(i)\notin c`, then
`\kappa` (supported only on `\{\rho(x),\rho(y)\}\subseteq c`) fixes
`h(i)`, so `g(i)=h(i)`. If `h(i)\in c`, then `g(i)=\kappa(h(i))\in c`
regardless (`\kappa` maps `c\to c`). Either way, whether the *first*
step of `i`'s forward orbit lands inside `c` is unchanged by passing from
`h` to `g` (only *which* point of `c` it lands on can change, via
`\kappa`), and once any orbit is inside `c` it *stays* inside `c`
forever under both `h` and `g` (both restrict to bijections of `c`), so
it can never subsequently revisit `i\notin c`. Hence: `i\notin c` is
non-cyclic for `h` iff its orbit under `h` reaches `c` without first
repeating outside `c` — a property that depends only on the *domain*
restriction `h|_{[n]\setminus c}`, which is **identical** for `g` and `h`
wherever the orbit hasn't yet entered `c` (established above), and is
irrelevant once it has (both trap it in `c` forever). So the set of
non-cyclic points, and hence `C(g)`, equals `C(h)=c` exactly. (This is
the same "tributaries feed in without altering cycle membership"
mechanism Estágio 18's Lemma B4 already uses, now applied to verify that
*relabeling* the surviving cycle's own internal wiring cannot change
*which* points are on it.)

So `g \in \{C(h')=c, h'|_c=\rho'\}`, establishing the map is well-defined
into the claimed codomain. Since `\kappa\circ\kappa=\mathrm{id}`
(transposition is an involution), applying the identical construction to
`g` (using the same transposition `\kappa`, and noting `\kappa\circ\rho'=\rho`
by direct check — swapping back) returns exactly `h`; running the same
argument with roles of `\rho,\rho'` swapped shows `\kappa\circ(-)` maps
`\{C=c,\,\cdot|_c=\rho'\}` into `\{C=c,\,\cdot|_c=\rho\}` too. So
`h\mapsto\kappa h` is a bijection between the two sets, self-inverse.
`\square`

### 2.2 Proof of Theorem J

Fix `c`, `m=|c|\ge2`. Write `A_\rho := \{h : C(h)=c,\ h|_c=\rho\}` for
`\rho\in\mathrm{Sym}(c)`. By Lemma J1 (applied with `\kappa` as in Lemma
J2 — a fixed bijection of `[n]`, so Lemma J1 applies to it directly),
`P(f\in B) = P(\kappa f \in B)` for every measurable `B`; taking
`B:=A_{\rho'}` gives `P(f\in A_{\rho'}) = P(\kappa f\in A_{\rho'}) =
P(f\in\kappa^{-1}(A_{\rho'}))`. By Lemma J2, `\kappa^{-1}(A_{\rho'}) =
A_\rho` exactly (as *sets* of functions, since `\kappa` is a bijection
between them with `\kappa\circ\kappa=\mathrm{id}`). So

`P(f\in A_\rho) = P(f\in A_{\rho'})` for every `\rho\in\mathrm{Sym}(c)` and every `\rho'=\rho\circ(x\,y)`, `x,y\in c`.

Transpositions `(0\,1),(0\,2),\dots` (any generating set of transpositions
of `c`, indexed by a fixed reference element of `c`) generate
`\mathrm{Sym}(c)`, and right-multiplication by generators is *transitive*
on `\mathrm{Sym}(c)` in the sense that every `\rho\in\mathrm{Sym}(c)` is
reachable from any fixed `\rho_0` by a finite chain of such steps. Each
step in the chain preserves `P(A_\cdot)`, so `P(A_\rho)` is the **same
value** for every `\rho\in\mathrm{Sym}(c)`. Since
`\sum_{\rho\in\mathrm{Sym}(c)} P(A_\rho) = P(C(f)=c)`, each individual
`P(A_\rho) = P(C(f)=c)/m!`, i.e.

`P(f|_c=\rho \mid C(f)=c) = 1/m!` for every `\rho\in\mathrm{Sym}(c)`. `\blacksquare`

**Remark (why this is not the same as the classical uniform-random-function
fact).** For a genuinely uniform random function `[n]\to[n]` it is a
textbook fact (Kolchin, *Random Mappings*, 1986) that, conditional on the
cyclic set, the induced permutation is uniform — proved there by a direct
forest-counting argument specific to that model. Definition 4's `f` is
**not** a uniform random function (it is a uniform permutation with only
`K` points independently re-targeted; the un-rerouted `n-K` points are
constrained to be *injective*, not merely "any function"). The proof
above does not invoke or adapt the classical forest-counting argument at
all — it is a self-contained symmetry proof specific to Definition 4's
construction, using only that (i) post-composing the whole map by a fixed
bijection preserves the law (Lemma J1, which holds because "uniform
permutation" and "iid uniform destinations" are each themselves
composition-invariant), and (ii) an explicit local bijection on the event
of interest (Lemma J2). It applies verbatim at `K=0` (pure permutation:
trivially every cycle-restriction is already a specific permutation with
probability 1, and Theorem J correctly degenerates since `\mathrm{Sym}(c)`-uniformity
conditional on `C(\pi)=c` is exactly the classical fact used in Estágio
18's own finite-`n` cross-checks) and at `K=n` (pure i.i.d. uniform
targets: conditional on being a bijection, trivially uniform over
`\mathrm{Sym}(c)`, since every function value is drawn i.i.d.).

---

## 3. Corollary: the exact 50/50 same/different-cycle split

**Classical fact (CITED, re-verified independently below, §4.1).** For a
uniform random permutation of any `m\ge2` labeled elements, and any two
fixed distinct elements `i,j`, `P(i,j\text{ same cycle})=1/2`, for
**every** `m` (not merely as `m\to\infty`).

> **Corollary (PROVED).** Fix `n\ge2`, `0\le K\le n`, and two distinct
> points `i,j\in[n]`. Then, under Definition 4,
>
> `P(i,j\text{ both cyclic, same final cycle}) = P(i,j\text{ both cyclic, different final cycles}) = \tfrac12\,P(i,j\text{ both cyclic})`,
>
> **exactly**, for every `n` and `K` in this range.

*Proof.* Condition on `C(f)=c` for each subset `c\ni i,j` with `|c|\ge2`.
By Theorem J, `f|_c` is a uniform random permutation of `c`; by the
classical fact (with `m=|c|`), `P(i,j\text{ same cycle}\mid C(f)=c)=1/2`
regardless of `m=|c|`. Averaging over the (random) realized `c` — a
mixture of `1/2`'s is `1/2` — gives `P(i,j\text{ same cycle}\mid i,j\text{
both cyclic}) = 1/2` unconditionally on `|c|`, hence the stated identity.
`\square`

This is a genuine strengthening of Estágio 18's **Lemma B1**
(`P(x_1,x_2\text{ same block})=1/2`), which concerned only the
*unconditional background* `\mathrm{PD}(1)`/permutation partition (`K=0`,
or more precisely: same-block-of-`\pi`, ignoring rerouting and ignoring
whether either point survives to be cyclic at all). The Corollary here is
about the **actual final cyclic structure after rerouting**, conditioned
on **both points surviving** — exactly the harder, `K`-coupled object
Estágio 18 flagged (§3.3 of that document) as requiring a genuine joint
two-point construction to access, and reported as not obtained. This
document obtains it, **for the finite-`n` model**, without needing any
extension of Definition 3's primitives at all — see §6.3 for why this
route does not, however, resolve Estágio 18's harder residual question
(the *value* of `P(\text{both cyclic})`).

**A remark on the "easy half" this replaces.** `PREREG.md`'s S2/S3
attempted to derive the same/different split via a two-walker extension
of Definition 3's hazard-clock machinery, reducing it (in the
*continuum*) to `\mathrm{Term1}=\mathrm{Term2}=\int_0^1 t(1-t^2)^K\,dt`.
Independently of whether that continuum route can be completed (open,
§6.3), the **fact being targeted** — same/diff exactly 50/50 given both
cyclic — has an entirely elementary reason at the finite-`n` level (this
section), with no hazard-clock machinery, no `(\Theta,E)` primitives, and
no destination-information obstruction whatsoever. The two routes prove
(candidate proof, resp. proved fact) the same *qualitative* conclusion by
completely different mechanisms; this document endorses only the
finite-`n` one, as proved.

---

## 4. Verification

### 4.1 Exhaustive exact enumeration (fresh, this session)

`uniform_cyclic_restriction_exact.py` enumerates, exhaustively and
exactly (Python arbitrary-precision integers; `fractions.Fraction` used
only for the final display ratios — no floating point anywhere in the
counting), **every** `(\pi,R,\text{destinations})` configuration for a
grid of `(n,K)` pairs, and checks two things per configuration set:

1. For every realized cyclic set `c` with `|c|\ge2`: are all `|c|!`
   bijections of `c` realized, each with **exactly equal** count (Theorem
   J's claim, checked directly, not inferred)?
2. Direct tally of `P_\text{both}`, `P_\text{same}`, `P_\text{diff}` for
   the fixed pair `(0,1)`, cross-checking the Corollary.

A companion routine `classical_same_cycle_half(m)` independently
re-verifies, by its own separate exhaustive enumeration (not reusing the
main routine's code path), the classical fact of §3 for `m=2,\dots,7`.

**Results (zero violations, every one of 21 `(n,K)` cells, plus the
classical-fact table):**

| `m` | `P(1,2\text{ same cycle})`, uniform perm. of `m` |
|---|---|
| 2–7 | `1/2` exactly, all six values |

| `n` | `K` | configs | `P_\text{both}` | `P_\text{same}` | `P_\text{diff}` | ratio | restriction test |
|---|---|---|---|---|---|---|---|
| 3–7 | 1 | 54 – 246,960 | → | `1/2\times` `P_\text{both}` | (same) | `1/2` exact, all 5 `n` | UNIFORM |
| 3–7 | 2 | 162 – 5,186,160 | → | ″ | ″ | `1/2` exact, all 5 `n` | UNIFORM |
| 3–6 | 3 | 162 – 3,110,400 | → | ″ | ″ | `1/2` exact, all 4 `n` | UNIFORM |
| 4–6 | 4 (incl. `K=n=4`) | 6,144 – 13,996,800 | → | ″ | ″ | `1/2` exact, all 3 `n` | UNIFORM |
| 5–6 | 5 (incl. `K=n=5`) | 375,000 – 33,592,320 | → | ″ | ″ | `1/2` exact, both `n` | UNIFORM |

(Full exact fractions, e.g. `n=6,K=4`: `P_\text{both}=1382/6075`,
`P_\text{same}=P_\text{diff}=691/6075`; every single row's ratio column
printed exactly `1/2`, not merely close to it — see
`uniform_cyclic_restriction_exact.log` for the complete table with every
exact fraction. Total enumeration: **21 `(n,K)` cells, 21/21 exact
matches, zero violations** in either the restriction-uniformity check or
the same/diff-exact-half check, spanning `\binom{n}{K}\cdot n! \cdot n^K`
up to `\sim3.4\times10^7` configurations per cell, run time up to 130s
per cell.) The `K=n` boundary cells (`n=K=4,5`) are a genuine edge case
of the theorem's proof (no un-rerouted points at all: `f` is a uniform
i.i.d. map, conditional on being injective/bijective on its domain) and
pass identically, matching the trivial-case check noted in §2.2's
remark.

`E[C/n]` (fraction cyclic) is also tabulated in the log purely as a
harness sanity readout (matches the known monotone-decreasing-in-`K`
pattern with no anomaly); it is not a new claim.

### 4.2 What was and was not re-derived from the prior attempt

The prior attempt's `finite_n_exact_enum.py` covered `K=1` (`n=3..7`)
and `K=2` (`n=3..6`) for `P_\text{both},P_\text{same},P_\text{diff}`
only. This session's script (i) is a fresh, independent implementation
(different cyclic-detection routine, different enumeration loop
structure, additionally tracks the *full* permutation-on-`c` breakdown
rather than only the same/diff binary), (ii) reproduces the same exact
fractions the old script reported for the overlapping `(n,K)` cells
(spot-checked: `n=6,K=2`: old script `P_\text{both}=44/135`, this
session's independent run: **identical** `44/135` — see both logs),
giving genuine independent confirmation rather than mere reuse, and (iii)
extends the range to `K=3,4,5` including both `K=n` boundary cases, which
the old script did not attempt.

---

## 5. Numerically explored: does the split transfer to the continuum-flavored regime?

Theorem J and its Corollary are exact statements about Definition 4 (the
finite conditional-`K` model). Whether they transfer to `L(c)` itself —
i.e. whether `P(\text{same final cycle}\mid \text{both cyclic})=1/2`
holds for the actual Poisson-mixture object of Conjecture 2 — is a
**separate question** (§6.3). `poisson_continuum_same_diff_mc.py` (fresh
this session, seeds `20260864000`, `20260864001`) checks it empirically
in the large-`n` finite-model regime this archive uses throughout as the
standard numerical proxy for `L(c)` (Definition 1, `n` large,
`c`-dependent Bernoulli reroute probability):

| Run | `n` | `c` | trials | seed | `P(\text{both})` empirical | target `(1-e^{-c})/c` | `P(\text{same}\mid\text{both})` | target |
|---|---|---|---|---|---|---|---|---|
| `c=2, n=8000` | 8000 | 2.0 | 100,000 | `20260864000` | `0.42909` | `0.43233` | `0.49852` | `0.5` |
| `c=1, n=6000` (cross-check) | 6000 | 1.0 | 80,000 | `20260864001` | `0.63235` | `0.63212` | `0.50113` | `0.5` |

Both the `P(\text{both})` sanity readout (already a known target,
`c=1` matching Estágio 18's own value to 4 decimals, `c=2` a value not
previously tested in this lineage) and — the actual new check —
`P(\text{same}\mid\text{both})` land within `\sim0.15`–`0.9` percentage
points of the exact-finite-`n` prediction `1/2`, consistent with pure
Monte Carlo noise at these trial counts (a back-of-envelope binomial
standard error on the ratio is `\approx0.2`–`0.3` percentage points here,
matching the observed deviations in scale). **This is exploratory
evidence for transfer, not a proof** — see §6.3 for exactly what a proof
would require.

---

## 6. Relationship to the mandate's primary targets, and the sharpened obstruction

### 6.1 Targets (1)/(2): confirmed still open, not pivoted away from

Per the mandate's instruction, `THEOREM.md` was checked for whether a
newer Estágio already closed Conjecture 1 for general `K` (which would
make target (1) an immediate corollary and require pivoting to target
(3) regardless). **It has not**: `THEOREM.md`'s latest state (Estágio 22,
2026-08-25, the most recent entry in the file) explicitly lists, in its
closing "what remains open" paragraph, `"Conjecturas 1 (K\ge5, sob
revisão na onda 17) e 2; a exploração conjunta (Estágio 18)"` —
Conjecture 1 for `K\ge5` and Conjecture 2 are both still open, and
Estágio 18's joint-exploration obstruction is explicitly still listed as
unresolved. `DECISION_LEDGER.yaml`'s `DISC-DEC-072` entry (this same
wave) confirms only front (b) (`SHARP-RATE-REASSEMBLY-ATTEMPT`, Estágio
22) has been integrated so far — front (a) (`CONJECTURE-1-K5-GENERAL-ATTEMPT`)
has no ledger entry or directory yet, so there is nothing to duplicate or
pivot around. **Targets (1) and (2) are therefore reported here as open**,
exactly the honest-non-closure outcome the mandate pre-declared
acceptable — this document does not manufacture a pivot that isn't
warranted by the record.

### 6.2 What Theorem J does and does not contribute toward (1)/(2)

It is worth stating precisely why the Corollary of §3, despite being an
exact statement about the *same joint two-point quantity* Estágio 18's
`\mathrm{Term1}`/`\mathrm{Term2}` decomposition needs, does **not** close
`E[M_K^2]=1/(K+1)`. Writing `P_\text{both} := P(1,2\text{ both cyclic})`
(the finite-`n` analogue of `E[M_K^2]`, up to the standard
`n(n-1)`-vs-`n^2` finite-size correction Definition 4's exchangeability
argument always uses), the Corollary gives

`P(\text{both, same}) = P(\text{both, diff}) = \tfrac12 P_\text{both}`,

an exact statement about the **conditional split**, but it says
**nothing about the value of `P_\text{both}` itself**. Computing
`P_\text{both}` is exactly the harder half of the problem — equivalent
(by a standard exchangeability identity, `P_\text{both} =
E[C(C-1)]/(n(n-1))` with `C:=|C(f)|`) to knowing the **second moment of
the cyclic count**, i.e. it *is* Conjecture 1's density question in
disguise (for `K\ge5`, exactly the still-open case). There is no
shortcut from "the split is 50/50" to "the total is `1/(K+1)`" — these
are logically independent facts about the joint law, and this document
makes only the first one rigorous. This is stated explicitly so the
result is not misread as closing more than it does.

### 6.3 The continuum-transfer question, attempted and honestly left open

A natural next question: does Theorem J's *proof technique* (Lemma
J1+J2, working entirely within the finite combinatorial model) adapt
directly to Definition 2/3's continuum construction, bypassing the
finite-`n\to\infty` bridge (`THEOREM.md` §7, a pre-existing, independently
open gap unrelated to this front) entirely? This was considered briefly.

The obstruction is exactly Estágio 18's: Definition 3 represents "`x_0`
cyclic" via an *abstract* hazard-clock race (`(\Theta_j,E_j)` primitives)
that is a **citation-justified** (Proposition 2.4), not first-principles,
stand-in for Definition 2's literal picture. Lemma J1's proof crucially
used that `f` (in the finite model) is a **literal, explicit function**
built from primitives that transform simply under post-composition by a
fixed bijection (`\kappa\circ\pi` is again uniform; `\kappa(U_i)` is
again uniform). Definition 3 has no directly analogous "literal
destination" object to post-compose — its primitives are already an
abstraction of the *marginal* one-point question, and (per Estágio 18
§3.3, restated and not superseded here) it is exactly this abstraction
that discards the destination information a genuine two-point
construction would need. Constructing a literal, two-point-capable
analogue of Definition 3 directly from Definition 2's primitives (real
Poisson marks, real `\mathrm{Unif}(0,1)` destinations, the real
`\mathrm{PD}(1)` cyclic order) — the same "substantial, well-posed, but
not completed" piece of mathematics Estágio 18 named — was not attempted
to completion here either; attempting even a sketch of it exceeded what
could be honestly verified within this front's time budget. **This is
reported as open, not solved by implication from the finite-`n` result**,
consistent with the discipline requested. What *has* changed, precisely,
is: the piece of the two-point joint law that is *reachable without*
that missing construction (the finite-`n` conditional-split fact) is now
closed; the piece that provably *needs* it (the value `P_\text{both}`,
and any literal continuum statement) is unchanged in status from Estágio
18, now with one fewer plausible shortcut around it (§6.2's remark rules
out "derive the split, then bootstrap the value" as a route).

---

## 7. What survives from `PREREG.md`'s S1–S7, and what does not

For completeness, since this front inherited that document:

- **S1** (continuum, "explored region = cycle of `x_1`, mass exactly `t`")
  — **not proved here**, and identified above (§0) as exactly Estágio
  18's obstruction restated; not adopted.
- **S2/S3** (continuum `\mathrm{Term1}=\mathrm{Term2}=\int t(1-t^2)^K dt`,
  via a two-walker hazard-clock extension) — **not attempted**; superseded
  in *conclusion* (same/diff 50/50) by this document's finite-`n` Theorem
  J route, which reaches the analogous fact by a completely different,
  fully elementary mechanism requiring none of Definition 3's machinery.
  Whether S2/S3's specific continuum mechanism is itself correct remains
  open and untested by this document either way.
- **S4** (`E[M_K^2]=1/(K+1)`, `E[M(c)^2]=(1-e^{-c})/c`) — mandate targets
  (1)/(2); **not closed**, per §6.1.
- **S5/S6** (general-`p` moment identity, `p`-point extension) — **not
  attempted** in this document; out of scope for the mandate's `p=2`
  focus, and would inherit whatever status S1–S3 end up having.
- **S7** (the refuted per-mark-independence shortcut, `E[A^2]=49/180\ne1/3`
  at `K=2`) — a self-contained negative finding from the stalled
  attempt's own paper work, verified internally by its `symbolic_checks.py`
  (arithmetic only, no probabilistic construction at stake) — **not
  re-verified independently by this document** (out of scope: it plays no
  role in what this document proves or claims), but nothing here
  contradicts it either.

`PREREG.md`'s own T1–T5 test plan is superseded by the test plan actually
executed here (§4–§5); T2's exact-enumeration item is the one piece that
was carried out in spirit (independently redone and substantially
extended, §4.1), the rest (T1's symbolic checks of S2–S7's *arithmetic*,
T3's general-`K` KS tests, T5's kernel bin-checks) were not pursued, as
they are downstream of S1–S3 and S5–S7, none of which this document
relies on or completes.

### 7.1 Self-caught issue: the naive "freeze-and-swap" bijection fails

Before arriving at Lemma J1/J2's post-composition argument (§2.1), this
session's first attempt at Theorem J tried a simpler-looking bijection:
fix `h` with `C(h)=c`, `h|_c=\rho`; define `h'` by leaving `h`
**completely unchanged outside domain `c`**, and replacing `h|_c=\rho`
with `h|_c=\rho'` directly (no relabeling of outside-domain images at
all). This *does* correctly preserve `C(h')=c` (the same "tributaries
don't affect cycle membership" argument used in the final Lemma J2
proof, §2.1). But it does **not**, in general, preserve membership in the
underlying sample space: if some domain point `y\in c\setminus R` (a
non-rerouted, hence `\pi`-image-constrained point of `c`) has its image
changed from `\rho(y)` to `\rho'(y)`, and some domain point `i\notin c`
(with `i\notin R` also) happens to satisfy `h(i)=\rho'(y)` already, the
new function `h'` has **two** domain points (`y` and `i`, both outside
`R`) mapping to the same target `\rho'(y)` — impossible for any
`h'`-arising-from-a-genuine-permutation `\pi'` (permutations are
injective everywhere, in particular on `[n]\setminus R`). This is a real
failure mode, not a hypothetical one: it means the naive bijection's
image can contain "configurations" that are not realizable under
Definition 4's model at all, so counting/measure arguments built on it
are unsound. The count-preservation this naive map *would* give, if it
worked, matches Theorem J's conclusion — which is presumably why the
stalled prior attempt's `finite_n_exact_enum.py` found the right
*numbers* — but the mechanism needed independent repair. Lemma J1's fix
(post-compose the *entire* map by a fixed bijection `\kappa`, rather than
freezing the outside and locally swapping) sidesteps this exactly: `\kappa`
is applied to literally every domain point's *output*, both inside and
outside `c`, so it can never create two domain points colliding on a
target that weren't already going to collide under the identical
transformation applied to `h` itself — injectivity of `h` on
`[n]\setminus R` is preserved because `\kappa` is injective and
post-composition of an injective map with an injective map is injective,
full stop, with no case analysis needed. This was caught by direct
inspection (attempting to write the "freeze-and-swap" argument down
rigorously as this document, and finding no way to rule out the collision
case) before any script was written to test it — no script output was
affected; this is purely a self-caught proof-attempt correction, recorded
per the archive's disclosure discipline.

---

## 8. Scope, honesty, scorecard

**PROVED in this document.** Lemma J1 (post-composition invariance of
`f`'s law, Definition 4); Lemma J2 (explicit swap bijection on the
cyclic-restriction event); Theorem J (Uniform Cyclic Restriction: `f|_c`
exactly uniform over `\mathrm{Sym}(c)` given `C(f)=c`, all `n,K`); its
Corollary (exact 50/50 same/different-cycle split given both cyclic, all
`n,K`) — all elementary, self-contained, and independently
cross-checked against exhaustive exact enumeration with zero deviations
across 21 `(n,K)` cells.

**NUMERICALLY EXPLORED, not proved.** Transfer of the 50/50 split to the
large-`n` continuum-flavored regime at `c=1,2` (fresh MC, within noise of
`1/2` in both runs).

**NOT achieved / still OPEN.** The mandate's primary targets: (1)
`E[M(c)^2]=(1-e^{-c})/c` unconditionally; (2) `E[M_K^2]=1/(K+1)` for all
`K` unconditionally. Neither is touched by Theorem J, which is
orthogonal (the conditional split, not the total probability) — see
§6.2 for the precise logical reason a shortcut does not exist. Also open,
unchanged from Estágio 18: the genuine continuum two-point exploration
construction from Definition 2/3's primitives (§6.3); `PREREG.md`'s S1–S3
continuum mechanism, neither confirmed nor refuted by this document.

**Confirmed, not pivoted from unnecessarily.** `THEOREM.md`'s latest
state (Estágio 22) does not close Conjecture 1 for general `K`; front (a)
of this same wave has no integrated result yet to duplicate or build on.

| Item | Status |
|---|---|
| `E[M(c)^2]=(1-e^{-c})/c` (target 1) | **OPEN** (unchanged) |
| `E[M_K^2]=1/(K+1)` for all `K` (target 2) | **OPEN** (unchanged) |
| Theorem J: Uniform Cyclic Restriction, all `n,K` (target 3) | **PROVED** (new) |
| Corollary: exact 50/50 same/diff split given both cyclic, all `n,K` | **PROVED** (new) |
| Exhaustive exact-enumeration cross-check, 21 `(n,K)` cells | 21/21, zero violations |
| Classical fact `P(\text{same cycle})=1/2`, uniform perm., independent re-derivation | confirmed, `m=2..7` |
| Continuum-regime transfer of the 50/50 split (fresh MC, `c=1,2`) | NUMERICALLY EXPLORED, within noise of `1/2` |
| Continuum-native (Definition 2/3) proof of Theorem J's analogue | attempted briefly, **not completed** — same obstruction as Estágio 18 §3.3 |
| Self-caught proof-attempt error ("freeze-and-swap") | caught before any script ran; repaired via Lemma J1/J2; disclosed §7.1 |
| `PREREG.md` S1–S7 program | not completed; not adopted wholesale; disposition of each item recorded §7 |

**This document's net result: honest non-closure of the mandate's primary
numbered targets, with a new, fully elementary, fully proved exact
finite-`n` theorem about the joint two-point law — the genuinely
unclaimed target the mandate names as acceptable in its own right — plus
an explicit, sharpened statement of exactly what remains open and why the
new theorem cannot be leveraged past that boundary.** No Millennium
Problem claim of any kind; pure internal combinatorics on the archive's
own random-permutation-with-reroutes ensemble.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `uniform_cyclic_restriction_exact.py` | none (exact deterministic enumeration) | n/a |
| `poisson_continuum_same_diff_mc.py`, run 1 (`c=2,n=8000`) | `20260864000` | reserved `20260864000+` |
| `poisson_continuum_same_diff_mc.py`, run 2 (`c=1,n=6000`, cross-check) | `20260864001` | reserved `20260864000+` |

Grep-confirmed before first use: the only prior occurrences of
`"20260864"` anywhere in the archive were the two reservation lines
(`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`) and this front's own
`PREREG.md` (pre-registration, not a use). No seed from the
referee-reserved range `20260865000+` was used. `uniform_test.py`, an
early scratch pilot for §2's theorem written to the session scratchpad
directory (not this archive) before being finalized here as
`uniform_cyclic_restriction_exact.py`, used no randomness either
(deterministic enumeration) and is not part of the archive.

## Files table

| File | Role |
|---|---|
| `PREREG.md` | inherited pre-registration from the stalled prior instance of this front (see §0, §7 for disposition) |
| `symbolic_checks.py` / `.log` | inherited; read for orientation only, not relied upon (see §0) |
| `finite_n_exact_enum.py` / `.log` | inherited; independently reproduced and extended by `uniform_cyclic_restriction_exact.py`, not itself relied upon (see §4.2) |
| `uniform_cyclic_restriction_exact.py` / `.log` | **this session, fresh** — §2/§3/§4.1: exhaustive exact verification of Theorem J and its Corollary, 21 `(n,K)` cells, plus the independent classical-fact re-derivation |
| `poisson_continuum_same_diff_mc.py` / `.log` / `_results.json` | **this session, fresh** — §5: fresh MC check of continuum-regime transfer, `c=1,2`, seeds `20260864000/1` |
| `ATTEMPT.md` | this document |
