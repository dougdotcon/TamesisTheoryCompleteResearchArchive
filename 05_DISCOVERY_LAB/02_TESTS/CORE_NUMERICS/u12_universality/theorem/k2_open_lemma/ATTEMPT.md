# The K≥2 Open Lemma — a bounded attempt via the explicit coupling strategy of THEOREM.md §7.4

> **Governance.** DISC-DEC-022, front (a) (K2-OPEN-LEMMA). Self-contained mathematics,
> no external data, no holdout, no governance edits. `THEOREM.md` (closed/finalized) is
> not touched by this document. Every claim below is labeled PROVED, CONFIRMED BY EXACT
> FIT (not yet re-derived from first principles), NUMERICALLY SUPPORTED ONLY, or OPEN —
> the same discipline `THEOREM.md` itself uses.

> **Executive summary (read first).** §7.4 of `THEOREM.md` sketches, but does not
> execute, a coupling strategy for the Open Lemma (`φ_n^{(K)} → φ_K` as `n→∞`, fixed
> `K≥2`). This document restates that sketch precisely (§1), then executes it via an
> explicit discrete exploration process. The main results:
> - **A general (all `K`) Reduction Lemma, PROVED (§2):** the Open Lemma at any fixed
>   `K` follows from convergence of a strictly simpler "generic-point" quantity
>   `ψ_n^{(K)}`, with the "rerouted-point-itself" contribution killed for free by a
>   `O(K/n)` bound that needs no further work. This is a genuine, general-`K`
>   simplification of the target, not previously stated in `THEOREM.md`.
> - **K=1 executed via this route, PROVED (§3):** `ψ_n^{(1)} = 2/3 + 1/(6n)` exactly,
>   an independent cross-check of Proposition 4 by a different method.
> - **K=2 executed in full, PROVED (§4–§5): the K=2 case of the Open Lemma is closed.**
>   `ψ_n^{(2)} = 8/15 + 4/(15n) + 1/(15n^2)` exactly, derived from an explicit
>   case-by-case combinatorial analysis of the discrete exploration process (not merely
>   fitted), and independently cross-checked against brute-force enumeration. Combined
>   with the Reduction Lemma, this proves `φ_n^{(2)} → φ_2 = 8/15`.
> - **A bonus exact-rate result for K=2 (§6):** `φ_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) +
>   1/(5n^3)` exactly (one input piece confirmed by exact rational fit rather than
>   first-principles derivation — flagged precisely). This **resolves** `THEOREM.md`
>   §9 item 2 for `K=2`: the true rate is `Θ(1/n)`, not `Θ(1/n^2)` — explaining exactly
>   why the `n^2`-rescaled deviation in §7.4's table never levels off.
> - **General `K≥3`: NOT closed.** §7 precisely characterizes *why* the case-analysis
>   method's cost grows combinatorially with `K` (not just "combinatorial explosion" in
>   the abstract — the precise combinatorial objects responsible are named), gives
>   supportive-only numerics at `K=3` (consistent with, not proof of, `ψ_n^{(3)}→φ_3`),
>   and states precisely what additional fact would close the gap for general `K`.
>
> **Net honest verdict:** the coupling strategy of §7.4, once made precise and
> executed, **succeeds completely at K=2** (a strictly stronger result than
> `THEOREM.md` itself proves) but the *same* method's cost genuinely explodes
> combinatorially beyond that, exactly as §7.4 anticipated — this document sharpens
> *why*, rather than resolving it.

---

## 1. The coupling strategy of §7.4, restated precisely

`THEOREM.md` §7.4 sketches (verbatim, condensed): couple the `K` discrete uniform
reroute targets and the discrete cycle structure of `π` with `K` continuum points and
the `PD(1)` cycle partition of `L(c)`'s construction (Definition 3), and bound the
probability that the coupling fails — a "collision" with no continuum counterpart (two
reroute targets colliding, a reroute target landing on another reroute's source, or two
reroute-affected regions overlapping within `O(1/n)` of each other in cycle-position).
Each such collision has probability `O(K^2/n) → 0` for fixed `K`, which is offered as
the heuristic reason the Open Lemma should be true. Two gaps are named as not carried
out: (i) a precise coupling construction, (ii) an argument that, off the collision
event, the discrete cyclic-count functional converges to the continuum one.

**What exactly needs to be coupled to what.** Unpacking this precisely, before
attempting it:

- **The discrete object.** Fix `n`, fix `K` labeled sources `{1,…,K}` ⊂ `[n]` (WLOG, by
  the exchangeability already established in Definition 4 of `THEOREM.md`). `π` is a
  uniform random permutation of `[n]`; `U_1,…,U_K` are i.i.d. uniform on `[n]`,
  independent of `π`; `f(i)=U_i` for `i≤K`, `f(i)=π(i)` otherwise. The question is
  whether a fixed reference point is cyclic under `f`.
- **The continuum object.** Definition 3 of `THEOREM.md`: `K` i.i.d. uniform marks
  `S_1,…,S_K` on `[0,1)`, each with an i.i.d. uniform destination `Θ_j`, plus i.i.d.
  `Exp(1)` clocks `E_0,E_1,…,E_K` driving the arc-head closure-time algorithm. The
  question is whether `x_0` is cyclic.
- **The coupling that would need to be built.** A joint probability space carrying both
  `(π, U_1,…,U_K)` (for every `n`, coupled coherently as `n→∞`) *and* `(S_1,…,S_K,
  Θ_1,…,Θ_K, E_0,…,E_K)`, such that: (a) the marginals are correct at every `n` and in
  the limit; (b) outside an event `Bad_n` with `P(Bad_n)→0`, the discrete cyclic
  indicator and the continuum cyclic indicator (Definition 3's algorithm) are computed
  by *structurally the same steps*, so that they agree, or at least that the discrete
  indicator converges to the correct value conditionally on `Bad_n^c`.
- **The "collision" error term, made concrete.** The natural discrete analogue of
  Definition 3's exploration is a **forward walk** from the reference point under `f`
  (§2 below spells this out in full). The walk proceeds along `π` until it strikes one
  of the `K` sources, then "jumps" via that source's reroute target, and so on. A
  "collision" in the sense of the sketch is precisely: a reroute target landing on an
  *already-visited* point of this walk (closing a cycle that does not contain the
  reference point — a discrete phenomenon with no direct single-point-in-continuum
  analogue, since Definition 3's algorithm never "revisits" a point in the same sense).
  The sketch's `O(K^2/n)` heuristic is the right order of magnitude for a *single*
  collision (a specific reroute target landing among a set of `O(n)` — really
  `O(1)`-per-mark, `O(K)` total — already-visited points, out of `n` choices), but does
  **not** by itself say anything about what happens on the complementary
  (non-collision) event, which is exactly gap (ii) above and is where the real content
  of a proof has to live.
- **Why this would give convergence, if executed.** If (i)+(ii) were both carried out
  rigorously, one would get `P(discrete cyclic) = P(continuum cyclic) + O(P(Bad_n)) =
  φ_K + o(1)`, i.e. exactly the Open Lemma, possibly with an explicit rate if
  `P(Bad_n)` is bounded quantitatively (the sketch's heuristic suggests `O(K^2/n)`, but
  §4–§6 below show this guess is **not** the true rate even at `K=2` — see the honest
  discussion in §6).

This document does **not** build the joint space described above — that remains
undone, exactly as `THEOREM.md` states. Instead, §2–§5 take a related but more direct
route: work entirely on the **discrete side**, using the *exact* classical combinatorics
of uniform random permutations (the same "lazily revealed" / Feller-coupling
machinery `THEOREM.md` Proposition 2.4 cites for the continuum side) to compute the
discrete quantities *exactly*, and check their limit against `φ_K` (already computed on
the continuum side by Lemma 2 — no re-derivation of the continuum object is needed).
This sidesteps building the joint continuum/discrete coupling explicitly, at the cost
of not producing a *uniform-in-K* argument — which is exactly why it closes `K=1,2` but
not general `K` (§7 explains precisely where the case-count explodes).

---

## 2. A reduction lemma: the generic-point quantity suffices (PROVED, all `K`)

Definition 4 of `THEOREM.md` defines `φ_n^{(K)} := E[\#\text{cyclic}(f)]/n`, conditioned
on the rerouted sources being exactly `{1,…,K}` (WLOG by exchangeability, as already
noted there) — this is an average **over all `n` points**, including the `K` rerouted
sources themselves. Split this average into the two kinds of points:

> **Definition (component quantities).**
> `ψ_n^{(K)}   := P(K{+}1 \text{ is cyclic under } f)` — the probability that a fixed
> point *not* among the `K` rerouted sources is cyclic (the "generic-point" quantity);
> `ψ_n^{(K),R} := P(1 \text{ is cyclic under } f)` — the probability that a fixed
> point *among* the `K` rerouted sources is cyclic (well-defined for `n>K`).

> **Lemma A (Reduction Lemma, PROVED, every fixed `K≥1`).**
> `φ_n^{(K)} = \dfrac{K}{n}\,ψ_n^{(K),R} + \Big(1-\dfrac{K}{n}\Big)\,ψ_n^{(K)}`
> exactly, for every `n>K`. Consequently: **if `ψ_n^{(K)} → φ_K` as `n→∞`, then
> `φ_n^{(K)} → φ_K` as `n→∞`** — i.e. the Open Lemma at that `K` holds — *regardless of
> the behaviour of `ψ_n^{(K),R}`* (only its boundedness in `[0,1]`, trivial since it is
> a probability, is used).

*Proof.* By definition, `φ_n^{(K)} = (1/n) Σ_{i=1}^n P(i \text{ cyclic})`. Split the sum
into `i∈\{1,…,K\}` and `i∈\{K{+}1,…,n\}`.

**Symmetry within each block.** Fix any transposition `σ` of two indices `i,i'` both in
`{1,…,K}` (respectively both in `{K{+}1,…,n}`). Relabel: `π' := σ∘π∘σ^{-1}` (uniform,
since `π` is uniform and conjugation by a fixed permutation preserves uniformity);
`U'_j := U_{σ^{-1}(j)}` for `j≤K` (exchangeable, since the `U_j` are i.i.d. — swapping
two of them, or leaving them alone if `σ` acts outside `\{1,…,K\}`, does not change
their joint law). A direct check shows `f' := σ∘f∘σ^{-1}` exactly (both sides agree at
every argument: for `j≤K`, `f'(j)=U'_j=U_{σ^{-1}(j)}=f(σ^{-1}(j))=σ^{-1}(f(σ^{-1}(j)))`
composed correctly with `σ`; for `j>K`, `f'(j)=π'(j)=σ(π(σ^{-1}(j)))=σ(f(σ^{-1}(j)))`
since `σ^{-1}(j)>K` too when `σ` acts within `\{1,…,K\}` or within `\{K{+}1,…,n\}` only
— the two blocks are never mixed by such a `σ`). Since `(π',U') \overset{d}{=} (π,U)`,
`f' \overset{d}{=} f`. And relabeling preserves cyclicity structurally: `i` is cyclic
under `f'` iff `σ^{-1}(i)` is cyclic under `f`. Hence `P(i \text{ cyclic under } f) =
P(i \text{ cyclic under } f') = P(σ^{-1}(i) \text{ cyclic under } f)`, i.e.
`P(i \text{ cyclic})` is the same for every `i` in the same block. Call the common
values `ψ_n^{(K),R}` (block `\{1,…,K\}`) and `ψ_n^{(K)}` (block `\{K{+}1,…,n\}`) — these
are exactly the Definition above, with `i=1` and `i=K{+}1` as canonical representatives.

**Assembling.** `φ_n^{(K)} = (1/n)\big[K\cdot ψ_n^{(K),R} + (n-K)\cdot ψ_n^{(K)}\big] =
(K/n)\,ψ_n^{(K),R} + (1-K/n)\,ψ_n^{(K)}`, exactly, for every `n>K`.

**The limit.** `ψ_n^{(K),R}\in[0,1]` (a probability) and `K/n\to0` as `n\to\infty` (`K`
fixed), so `\big|(K/n)ψ_n^{(K),R}\big|\le K/n\to0`. If `ψ_n^{(K)}\to φ_K`, then
`(1-K/n)ψ_n^{(K)}\to 1\cdot φ_K=φ_K` (product of a sequence `\to1` and a sequence
`\toφ_K`). Summing, `φ_n^{(K)}\to 0+φ_K=φ_K`. `∎`

**What this buys, and what it does not.** Lemma A is a genuine, fully general (every
fixed `K≥1`, no restriction to `K=1,2`), unconditional simplification of the Open
Lemma's target: it removes the "rerouted point's own fate" entirely from consideration
— a real reduction in scope, since (as §4–§6 show concretely) `ψ_n^{(K),R}` is itself a
nontrivial quantity with its own combinatorics, but the Lemma proves that quantity is
*irrelevant to the limit*, at every `K`, for free. What it does **not** do is prove
`ψ_n^{(K)}\to φ_K` for any particular `K` — that remains exactly as hard as the original
problem, just posed on a strictly smaller, cleaner object. §3–§5 prove it at `K=1,2`.
§7 discusses precisely why the same route does not close at general `K`.

*(Sanity check on the mechanism: Lemma A explains, in passing, an odd numerical feature
that would otherwise look mysterious. `ψ_n^{(K)}` and `ψ_n^{(K),R}` individually
converge to `φ_K` and to some other limit respectively — see §6 — at rate `O(1/n)` each;
yet Proposition 4 of `THEOREM.md` proves `φ_n^{(1)}=2/3+1/(3n^2)`, rate `O(1/n^2)`. §3
computes `ψ_n^{(1)},ψ_n^{(1),R}` explicitly and shows the two `O(1/n)` terms cancel
*exactly* in the weighted sum `(K/n)ψ^R+(1-K/n)ψ` that Lemma A specifies — a genuine,
checkable cancellation, not a coincidence of rounding.)*

---

## 3. Executing the discrete exploration method at K=1 (validation, PROVED, cross-checks Prop. 4 independently)

The route below is deliberately **not** Proposition 4's route (which directly averages
`E[\#\text{cyclic}]` over all points at once). Instead it computes `ψ_n^{(1)}` (generic
point `2`, source `1`) directly, as a rehearsal for the `K=2` case analysis of §4, and
as an independent cross-check on Proposition 4 via Lemma A.

**The discrete exploration process.** Fix source `\{1\}`, generic reference point
`x^*=2` (so `n\ge2`). Trace the forward orbit of `x^*` under `f`: `y_0=x^*`,
`y_{t+1}=f(y_t)`. Since `x^*` is not special, the walk follows `π` — tracing `x^*`'s own
`π`-cycle `C_0` — until (if ever) it strikes the source `1`, at which point it "jumps"
to the independent, uniform reroute target `U_1` instead of continuing along `π`. `x^*`
is cyclic iff this walk returns to `y_0=x^*` before revisiting any other earlier point
of the walk.

**The one classical fact this rests on (cited, standard, already used verbatim in
`THEOREM.md`'s Proposition 4 Step 1).** For a uniform random permutation of `[n]` and
any fixed point, its cycle length `L` is **exactly** `\mathrm{Unif}\{1,…,n\}` — the
finite-`n` exact analogue of Fact A (§2.3 of `THEOREM.md`). Given `L=\ell`, the other
`\ell-1` cycle-mates are a uniform `(\ell-1)`-subset of the other `n-1` points, in a
uniform cyclic order — this is the same classical fact `THEOREM.md` §7.3's Step 1 uses.

**Case split, given `L=\ell` (`x^*`'s cycle length).**

- **Source `1` not on `C_0`** (probability `1-(\ell-1)/(n-1)`): the walk never touches
  `1` at all, so `f` agrees with `π` on `x^*`'s entire forward orbit — `x^*` is cyclic
  with probability `1`, unconditionally.
- **Source `1` on `C_0`, at position `d\in\{1,…,\ell-1\}`** (uniform given presence,
  probability `(\ell-1)/(n-1)` of presence): write `C_0 = (c_0{=}x^*, c_1,…,c_{\ell-1})`,
  `c_d=1`. Reroute target `U_1`, uniform on `[n]`, determines the outcome:
  `U_1=x^*` (success, prob. `1/n`); `U_1\in\{c_1,…,c_{d-1}\}` or `U_1=1` (immediate
  failure — closes a sub-cycle not containing `x^*`, total prob. `d/n`);
  `U_1\in\{c_{d+1},…,c_{\ell-1}\}` (success — the untouched tail of `C_0` after
  position `d` leads straight back to `c_0=x^*` via `π`, unaffected by the reroute,
  prob. `(\ell-1-d)/n`). Any other outcome is impossible here since only one source
  exists. Hence `P(\text{success}\mid \ell,d) = \dfrac{1+(\ell-1-d)}{n} =
  \dfrac{\ell-d}{n}`.

**Assembling (independently verified against exhaustive brute-force enumeration,
`n=2,…,9`, exact rational arithmetic — `psi_bruteforce.py K=1 ref=generic`,
`psi_k1_generic.log`, this directory).**

`ψ_n^{(1)} = \dfrac1n\sum_{\ell=1}^n\Big[1-\dfrac{\ell-1}{n-1}\Big(1-\dfrac{\ell}{2n}\Big)\Big]`

(using `\mathbb E_d[\ell-d]=\ell/2` for `d\sim\mathrm{Unif}\{1,…,\ell-1\}`), which
simplifies by elementary power-sum identities (`\sum\ell=n(n{+}1)/2`,
`\sum\ell^2=n(n{+}1)(2n{+}1)/6`) to the **exact closed form**

> `ψ_n^{(1)} = \dfrac{4n+1}{6n} = \dfrac23+\dfrac1{6n}`, for every `n\ge2`.

This matches brute force exactly for `n=2,…,9` (e.g. `n=2:\,3/4`; `n=9:\,37/54`). Since
`2/3=φ_1` (Lemma 2, `THEOREM.md` §5.2), **`ψ_n^{(1)}\to φ_1`, so Lemma A re-proves the
`K=1` Open Lemma** — independently of Proposition 4's direct route.

**The companion quantity, `ψ_n^{(1),R}`, and the exact cancellation.** The same style
of argument (walk starting *at* the source itself: `y_0=1`, `f(1)=U_1` immediately, no
initial `π`-traversal) gives, by an entirely analogous but shorter case split
(`U_1=1`: self-loop, success; `U_1=x^*` type points on a freshly-explored cycle
containing `1`: use the same `L\sim\mathrm{Unif}\{1,…,n\}` fact applied to `U_1`'s own
cycle) the exact closed form

> `ψ_n^{(1),R} = \dfrac{n+1}{2n} = \dfrac12+\dfrac1{2n}`, for every `n\ge2`,

verified exactly against brute force for `n=2,…,9` (`psi_k1_rerouted.log`). Both
`ψ_n^{(1)}` and `ψ_n^{(1),R}` converge at rate exactly `Θ(1/n)` — yet recombining via
Lemma A's exact identity,

`φ_n^{(1)} = \dfrac1n\Big(\dfrac12+\dfrac1{2n}\Big)+\Big(1-\dfrac1n\Big)\Big(\dfrac23+\dfrac1{6n}\Big) = \dfrac{2n^2+1}{3n^2} = \dfrac23+\dfrac1{3n^2}`,

**exactly Proposition 4's formula**, `O(1/n^2)`. Expanding `φ_n^{(1)}-φ_1` to order
`1/n` from the recombination above: the `1/n`-coefficient is
`\big(\tfrac12-\tfrac23\big) + \tfrac16 = -\tfrac16+\tfrac16 = 0` exactly — the first
term coming from `(1/n)ψ_n^{(1),R}`'s leading constant `1/2` measured against `φ_1=2/3`,
the second from `ψ_n^{(1)}`'s own `1/(6n)` term (carried at weight `\approx1`). **This
is a real, checkable cancellation, not a coincidence** — it is the reason Proposition
4's `O(1/n^2)` rate is *not* the "generic" rate one would naively expect from a
single-reroute perturbation (which is `O(1/n)`, as `ψ_n^{(1)}` itself shows); the
`O(1/n^2)` rate is a special feature of *averaging over all `n` points including the
rerouted one*, not of the underlying single-point convergence, which is genuinely
`O(1/n)`. This observation turns out to matter again at `K=2` (§6).

---

## 4. Executing the method at K=2 (PROVED)

This is the genuinely new case: two sources, `\{1,2\}`, generic reference point
`x^*=3` (so `n\ge3`). The walk from §3 generalizes, but a source's reroute can now
itself land on the *other* source, or on a point whose own `π`-cycle (in fresh,
unexplored territory) happens to contain the other source — the "combinatorial
explosion" §7.4 warns about. The two facts below tame it completely for `K=2`.

### 4.1 Two supporting facts

> **Fact C (cycle-revelation independence; standard, cited).** If a cycle `C` of a
> uniform random permutation of a finite set `S` has been fully revealed (occupying a
> known subset of `S`), the restriction of the permutation to `S\setminus C` is itself
> a uniform random permutation of `S\setminus C`, independent of `C`'s internal
> structure. *(Immediate from the sequential/"lazily revealed" construction of a
> uniform permutation — the same device `THEOREM.md` Definition 2.4 cites, and
> `DERIVATION.md` §1 uses, as "`π` revealed lazily": once a full cycle's images are
> pinned down, the remaining unassigned domain/range pairs are, by exchangeability, a
> uniform bijection on what remains.)*

> **Lemma B (co-cycle lemma; PROVED here, elementary, apparently not stated as such in
> `THEOREM.md`).** For a uniform random permutation of any finite set of size `m\ge2`,
> two fixed distinct elements lie on the same cycle with probability **exactly `1/2`**
> — independent of `m`.
>
> *Proof.* Let `w,z` be the two elements. By the cycle-length fact (§3), `w`'s cycle
> length `L_w\sim\mathrm{Unif}\{1,…,m\}`, and given `L_w=\lambda`, `z` is among `w`'s
> `\lambda-1` cycle-mates with probability `(\lambda-1)/(m-1)`. Hence `P(\text{same
> cycle}) = \mathbb E_\lambda\big[(\lambda-1)/(m-1)\big] =
> \big(\mathbb E[\lambda]-1\big)/(m-1) = \big((m{+}1)/2-1\big)/(m-1) = \tfrac12`. `∎`

Lemma B is the load-bearing fact that keeps `K=2` tractable: whenever the walk escapes
`x^*`'s own cycle `C_0` into completely fresh territory (via a reroute landing on a
point never seen before), the chance that the *other*, still-untriggered source
happens to sit on that fresh point's cycle is *exactly* `1/2`, **regardless of how much
of `[n]` has already been explored** (by Fact C, the fresh territory is itself a
uniform permutation on whatever remains, of whatever size — Lemma B's `m`-independence
is what makes this usable without tracking exploration size explicitly).

### 4.2 The target-set principle

Tracing through every branch of the walk (both sources on `C_0`, in either order; one
on `C_0` and one off, reached directly or via a fresh excursion aided by Lemma B; etc.
— the full enumeration is mechanical and is exactly what `psi_k2_case_formula.py`
implements and cross-checks) yields one clean, recurring structural fact:

> **Whatever path the walk takes to eventually trigger the *last* remaining source's
> reroute, the set of "winning" landing points for that final reroute is always exactly
> `\{x^*\}\,\cup\,\{\text{the still-untouched tail of }C_0\text{ strictly after the
> position of the last source that lay on }C_0\}`** — a set whose size depends only on
> `C_0`'s length `\ell` and the position of the rightmost `C_0`-resident source, **not**
> on which detour (direct, or via one or more fresh excursions) was taken to reach it.

This is what makes an exact finite-`n` formula possible at all: every intermediate
"failure" branch (landing on already-visited territory, self-loops, exhausting all
sources without ever finding a way back to `C_0`) is a **dead end** that contributes
`0` to the success probability and can be discarded without being individually
integrated into a rate — only the *final* live reroute's landing distribution matters,
and it is always the same simple set.

### 4.3 The three cases

Given `x^*`'s cycle length `L=\ell` (`P(L{=}\ell)=1/n` exactly, §3):

- **(a) Neither source on `C_0`.** Probability `(n-\ell)(n-\ell-1)/[(n-1)(n-2)]`. Neither
  source is ever reached by the walk — success with probability `1`.

- **(b) Exactly one source on `C_0`, at position `d\in\{1,…,\ell-1\}` (the other lies
  entirely off `C_0`, unrestricted).** Probability, given `\ell`,
  `2\cdot(\ell-1)(n-\ell)/[(n-1)(n-2)]` (factor `2` for "source 1 on / 2 off" or the
  symmetric reverse). Working through the sub-branches (direct win/loss on `C_0`
  itself; the on-`C_0` source's reroute landing exactly on the off-`C_0` source
  [triggering it immediately]; landing on fresh territory, where Lemma B applies) gives

  `P_b(\ell,d) = \dfrac{(\ell-d)(3n-\ell+1)}{2n^2}`.

- **(c) Both sources on `C_0`, at positions `p<q` in `\{1,…,\ell-1\}`.** Probability,
  given `\ell`, `(\ell-1)(\ell-2)/[(n-1)(n-2)]`. Here, critically, a reroute escaping to
  fresh territory can **never** find the other source (it already sits on `C_0`, fully
  accounted for), so every fresh excursion is a guaranteed dead end — only paths that
  stay on or return to `C_0` matter. This gives the cleaner

  `P_c(\ell,p,q) = \dfrac{(\ell-q)(n+q-p)}{n^2}`.

**Every one of these formulas, and the case weights above them, is independently
verified** — not merely the final summed answer — by `psi_k2_case_formula.py`, which
implements exactly the (a)/(b)/(c) split above (including the inner averages over `d`,
and over pairs `p<q`) and is checked to agree with exhaustive brute-force enumeration
(`psi_bruteforce.py`) *exactly*, term by term, for `n=3,…,8`
(`psi_k2_case_formula.log` vs. `psi_k2_generic.log`, this directory). This is a
stronger check than matching the final closed form alone: it confirms the *case
analysis itself* — not just its consequence — is correct.

### 4.4 The closed form

Summing case (a)+(b)+(c) over `L=1,…,n` (symbolic summation, `derive_closed_forms.py`,
using `sympy`'s exact `Sum`/`simplify`, no floating point anywhere):

> **`ψ_n^{(2)} = \dfrac{8n^2+4n+1}{15n^2} = \dfrac{8}{15}+\dfrac{4}{15n}+\dfrac1{15n^2}`,
> for every `n\ge3`.**

Verified exactly against brute-force enumeration for `n=3,…,8`
(`derive_closed_forms.log`, Step 1 — all 6 values match bit-for-bit as exact
fractions). Since `8/15=φ_2` (Lemma 2, `THEOREM.md` §5.2), `ψ_n^{(2)}\to φ_2` — and by
Lemma A (§2), **this proves `φ_n^{(2)}\to φ_2`.**

---

## 5. Closing the K=2 case of the Open Lemma

> **Theorem (Open Lemma at K=2; PROVED).** `\displaystyle\lim_{n\to\infty}φ_n^{(2)} =
> φ_2 = \dfrac{4^2(2!)^2}{5!} = \dfrac{8}{15}`.

*Proof.* By Lemma A (§2, `K=2`), `φ_n^{(2)}\to φ_2` follows from `ψ_n^{(2)}\to φ_2`,
which is §4.4's closed form (`8/15+4/(15n)+1/(15n^2)\to8/15`). `∎`

**What this establishes relative to `THEOREM.md`.** `THEOREM.md` §7.4 leaves the Open
Lemma at `K=2` explicitly unresolved ("neither proved nor disproved"), backed only by
exact enumeration to `n=8` showing monotone numerical convergence with an unclear rate
(§7.4's table). This document **proves** the `K=2` case unconditionally, via an
independent method (the discrete exploration/case-analysis route of §4, not the direct
whole-average combinatorics of `k2_exact_exploration.py`, which the task brief noted
had already been tried and had not revealed a clean rate — that attempt computed
`φ_n^{(2)}` directly by brute force, without the generic-point reduction of Lemma A,
and so could not separate the `Θ(1/n)` and cancelling-`Θ(1/n)` components found here).
The corresponding entry in `THEOREM.md`'s Proposição Condicional 5 (§7.5) — "conditional
on the Open Lemma holding for every `K\ge2`" — is therefore now **unconditional at
`K=0,1,2`**; the residual condition is exactly `K\ge3` (§7 below).

*(This document does not edit `THEOREM.md` itself — per the task brief, that document
is closed/finalized. The status update above is a claim about what this document
establishes, for a future integration step to act on if the user chooses.)*

---

## 6. Bonus: the exact rate for φ_n^{(2)} — resolving `THEOREM.md` §9 item 2 at K=2

§4–§5 prove `φ_n^{(2)}\to φ_2`. A sharper question, left explicitly open in
`THEOREM.md` §9 item 2 ("Whether `φ_n^{(K)}-φ_K` is `Θ(1/n^2)`, `Θ(\log n/n^2)`, or
something else for `K\ge2` is left fully open"), is: at what *rate*? This section
answers it exactly for `K=2`, with one piece of honesty about method flagged
precisely.

**The missing piece: `ψ_n^{(2),R}`.** Lemma A's identity needs `ψ_n^{(2),R}` (the
"rerouted point's own fate") to recover `φ_n^{(2)}` itself (not just its limit, for
which boundedness sufficed). Unlike `ψ_n^{(2)}` (§4, derived from first principles via
the case analysis), **`ψ_n^{(2),R}` is *not* independently re-derived here** — it is
obtained by exact rational interpolation: brute-force values at `n=6,7,8`
(`psi_k2_rerouted.log`) are fit to the 3-parameter family `(An^2{+}Bn{+}C)/(15n^2)`
(the same denominator structure as `ψ_n^{(2)}`, a reasonable but *unproven* ansatz),
giving `A{=}25/4,B{=}35/4,C{=}5/2`, i.e.

> `ψ_n^{(2),R} = \dfrac{(5n+2)(n+1)}{12n^2} = \dfrac{5}{12}+\dfrac{7}{12n}+\dfrac1{6n^2}`
> — **CONFIRMED BY EXACT FIT, not derived from first principles.**

The fit is checked against **three further, independent** data points (`n=3,4,5`,
*not* used in the fit) and matches exactly in every case (`derive_closed_forms.log`,
Step 2) — six exact rational matches from a three-parameter family is very strong
evidence, but it is evidence of a different kind than §4's case-by-case derivation,
and is labeled accordingly. *(A first-principles derivation of `ψ_n^{(2),R}` would
follow the same walk method with the walk starting **at** a source, `y_0=1`,
`f(1)=U_1` immediately — structurally similar to §4 but not carried out symbolically
here; flagged as a natural, likely-tractable follow-up, not attempted further under
this task's time budget.)*

**Recombining.** Substituting both closed forms into Lemma A's identity
(`derive_closed_forms.py`, Step 3):

> `φ_n^{(2)} = \dfrac{16n^3+n^2+21n+6}{30n^3} = \dfrac{8}{15}+\dfrac1{30n}+\dfrac{7}{10n^2}+\dfrac1{5n^3}`.

This is checked **exactly against every value in `THEOREM.md` §7.4's own table**,
`n=2,…,8` — including `n=2`, formally outside this derivation's stated range `n>K=2`,
which also matches exactly (`derive_closed_forms.log`, Step 3, 7/7 exact matches).

**The resolution.** `\displaystyle φ_n^{(2)}-φ_2 = \dfrac1{30n}+\dfrac{7}{10n^2}+\dfrac1{5n^3}`
— **the true rate is `Θ(1/n)`** (leading coefficient `1/30`), not `Θ(1/n^2)`. This
explains precisely the puzzling numerical behaviour `THEOREM.md` §7.4 reports and
flags without resolving: the table's rescaled quantity `n^2\cdot(φ_n^{(2)}-φ_2)`
increases steadily over `n=2,…,8` (`0.867\to0.992`, "no sign of leveling off") — of
course it does not level off, because the true leading term is order `1/n`, so
`n^2\cdot(φ_n^{(2)}-φ_2)\approx n/30\to\infty`. And `n\cdot(φ_n^{(2)}-φ_2) =
1/30+7/(10n)+1/(5n^2)\to1/30\approx0.0333` — a small constant approached only slowly,
which is also why the naive `n\cdot\text{dev}` sequence (`0.433,0.289,…,0.124` at
`n=2,…,8`) looks like it might be heading to `0` rather than to `1/30`: at `n=8` the
`7/(10n)` correction term (`\approx0.0875`) still dominates the limiting `1/30`
(`\approx0.0333`) by nearly `3\times` — the asymptotic regime has not yet set in at the
`n\le8` range `THEOREM.md`'s own exact enumeration reached. **This is a genuine,
non-obvious clarification of an explicitly flagged open item**, obtained only because
Lemma A's decomposition separates the `Θ(1/n)` generic-point behaviour (§4) from a
*different* `Θ(1/n)` rerouted-point behaviour (this section) whose leading terms very
nearly, but not exactly, cancel — leaving a genuine but small residual `Θ(1/n)`, not
the naively-expected `Θ(1/n^2)` of `K=1`, nor an un-cancelling `Θ(1/n)` of the same
size as either individual piece.

---

## 7. What happens at general K — precisely characterizing the obstruction, and the sharpened open problem

### 7.1 Why the K=2 method's cost grows combinatorially with K — made precise

`THEOREM.md` §7.4 already flags "a combinatorial explosion" for `K\ge2` in general. This
document's method makes the *source* of that explosion completely explicit, which is
itself a sharpening of the open problem beyond what §7.4 states: it is not merely that
"more marks interact," but a **specific, enumerable set of combinatorial objects** that
must each be classified as a win or loss, and whose count grows with `K`:

1. **Which subset `J\subseteq\{1,…,K\}` of sources lies on `x^*`'s own cycle `C_0`.**
   `2^K` subsets. (At `K=2`: the three nontrivial cases (a)/(b)/(c) of §4.3, collapsing
   `\{1,2\}\text{ off}`, exactly one on, both on — already `3` non-symmetric cases from
   `4` subsets, by the `\{1\}`/`\{2\}` symmetry.)
2. **Given `J`, the relative order of `J`'s positions along `C_0`.** `|J|!` orderings.
   (At `K=2`, `|J|=2` gave the `p<q` split inside case (c); already needed the *joint*
   quantity `(\ell-q)(n+q-p)`, not a function of `q` alone — the gap `q-p` genuinely
   enters, which is why the formula does not simplify to something depending only on
   the *last* position.)
3. **For each source in `\{1,…,K\}\setminus J`, *whether and how* it eventually gets
   triggered** — directly (a still-live reroute lands exactly on it), or via a chain of
   one or more fresh excursions, each requiring Lemma B (or its natural but unproven
   `K`-source generalization — see §7.2) to decide whether the *next* untriggered
   source lies on the newly-explored fresh cycle. At `K=2` there is only one such
   source to chase, hence only one Lemma-B application per branch. At general `K`, a
   chain of fresh excursions can encounter the *remaining* off-`C_0` sources in **any
   order**, each such order potentially requiring a distinct sub-computation (does the
   walk find source `i` before source `j`, and does landing "between" two of them on a
   shared fresh cycle behave like the on-`C_0` "between" case of §4.3(c), or
   differently, since a fresh cycle has no analogue of "the tail leads to `x^*`"
   unless `x^*`'s own cycle is what gets re-entered?).

Combining (1)–(3), the number of structurally distinct branches needing their own
success-probability computation is **super-exponential in `K`** in the worst case (a
weak but honest upper bound: at most `\sum_{|J|=0}^K \binom{K}{|J|}|J|!\cdot
(K-|J|)!` `\le K!\cdot 2^K`-order objects, from choosing `J`, ordering it, and ordering
the triggering sequence of the rest) — even though, as §4.2's target-set principle
shows, *many* of these branches collapse onto the same simple final answer once reached
(only the position of the rightmost `C_0`-resident source, and the pairwise gaps
between all `C_0`-resident sources, end up mattering — not the full path). It is
exactly this collapse, not case-avoidance, that made `K=2` tractable by hand; whether an
analogous collapse exists for **every** `K` (reducing the *effective* case count from
super-exponential to something polynomial in `K`) is precisely the open combinatorial
question this document could not resolve.

### 7.2 The additional fact that would be needed

Sharpening `THEOREM.md`'s task-brief request for "what additional fact would close the
gap": the natural generalization of Lemma B needed is:

> **Conjectural Lemma B′ (K-source co-cycle structure; NOT proved here).** For a
> uniform random permutation of `[n]` and any `K` fixed distinct points, there is a
> closed-form (or at least `n`-uniformly-bounded-error) description of the **joint**
> law of (i) which subsets of the `K` points share a cycle, (ii) their relative cyclic
> positions, that is *tractable enough* to be summed against the target-set principle
> of §4.2, generalized to: "the win set for the final live reroute in a chain
> triggered by sources at `C_0`-positions `d_1<\cdots<d_j` (the on-`C_0` ones) is
> `\{x^*\}\cup\{\text{tail of }C_0\text{ after }d_j\}`, reached with a probability that
> is a *rational function of `n` and the gaps `d_i-d_{i-1}`, uniformly in `K`*."
>
> Lemma B is exactly the `K=2`, "one source already fixed off `C_0`" instance of this;
> what is missing for general `K` is the *joint* multi-point version — not a new kind
> of mathematics, but a genuinely bigger classical-combinatorics computation (the
> "records"/Feller-coupling literature `THEOREM.md` Proposition 2.4 already cites,
> e.g. Arratia–Barbour–Tavaré 2003, almost certainly contains the needed joint law in
> some form for the *continuum* limit directly — reducing this whole document's
> discrete-side approach to a special case — but locating and adapting the exact
> finite-`n` statement needed here was not attempted under this task's scope).

A second, independent route that was considered but not pursued: attempt the *actual*
coupling of §1 (build the joint discrete/continuum probability space explicitly,
bound `P(Bad_n)`) rather than working purely on the discrete side as §2–§6 do. This
would need, at minimum, an explicit, quantitative version of Proposition 2.4 (currently
CITED, not derived, in `THEOREM.md`) — i.e. an explicit rate for the Feller-coupling
convergence of the `K`-mark structure, not just its existence. This is very plausibly
available in the literature (Feller-coupling rates are classical) but was not looked up
or verified here, so it is named as a candidate fact, not claimed as available.

### 7.3 Numerical evidence at K=3 (supportive only — NOT a proof, NOT even a rate estimate)

Exhaustive brute-force enumeration of `ψ_n^{(3)}` (three sources, generic reference
point `4`), `n=4,…,8` (`psi_k3_exploration.py`, `psi_k3_exploration.log`, exact rational
arithmetic; `n=8` took `36s`, cost grows like `n!\cdot n^3`, `n=9` was not attempted):

| `n` | `ψ_n^{(3)}` | `n\cdot(ψ_n^{(3)}-φ_3)` |
|---|---|---|
| 4 | `71/128 \approx 0.5547` | `0.390` |
| 5 | `1333/2500\approx0.5332` | `0.380` |
| 6 | `187/360\approx0.5194` | `0.374` |
| 7 | `4897/9604\approx0.5099` | `0.369` |
| 8 | `18023/35840\approx0.5029` | `0.366` |

(`φ_3=4^3(3!)^2/7!=16/35\approx0.4571`, Lemma 2.) `ψ_n^{(3)}` is monotonically
decreasing toward `φ_3`, and `n\cdot(ψ_n^{(3)}-φ_3)` is decreasing slowly and appears to
be levelling off (`0.390\to0.366` over `n=4,…,8`, the decrements shrinking each step:
`0.010,0.006,0.005,0.004`), **consistent with** — but, on `5` data points at small `n`,
nowhere near sufficient to establish — a continuation of the `Θ(1/n)` pattern found
(and *proved*) at `K=1,2`. §6's lesson (that a clean-looking `Θ(1/n)`-vs-`Θ(1/n^2)`
call from finite-`n` numerics alone can be **actively misleading** — recall
`THEOREM.md`'s own `K=2` table, which showed `n^2\cdot\text{dev}` still visibly
*increasing* at `n=8` while the true underlying rate was in fact `Θ(1/n)`, not
`Θ(1/n^2)` nor unboundedly growing — is a direct reason **not** to treat this `K=3`
table as informative about the rate, only about the qualitative direction (decreasing,
plausibly toward `φ_3`). No closed form for `ψ_n^{(3)}` is offered; deriving one by the
case-analysis method of §4 was assessed (§7.1) to require handling `\binom{3}{2}{+}
\binom{3}{1}{+}\binom{3}{0}` on-`C_0` subset cases, `2`-source Lemma-B-type multi-hop
chains for the "one on `C_0`, two off" case, and a genuinely new "two sources chase
each other through fresh territory" sub-case with no `K=2` analogue — assessed as
substantially more work than this task's bounded scope, not as impossible.

### 7.4 Honest bottom line on general K

**Open, precisely.** The Open Lemma for `K\ge3` is neither proved nor disproved by this
document. What this document adds beyond `THEOREM.md` §7.4's own honest statement:
(i) a fully general (`K`-uniform) reduction (Lemma A) that removes the "rerouted point's
own fate" from the problem for *every* `K`, for free; (ii) a concrete, executable method
(the walk/target-set/Lemma-B machinery) that **provably closes `K=1,2`** and whose exact
combinatorial growth with `K` is now named precisely (§7.1) rather than gestured at;
(iii) a named, specific missing fact (Conjectural Lemma B′, §7.2) whose resolution would
plausibly close the general case via this document's route, and a named alternative
route (an explicit-rate Proposition 2.4) that was not attempted; (iv) supportive-only
`K=3` numerics, explicitly *not* used to guess a rate, per the lesson of §6.

---

## 8. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Lemma A (Reduction Lemma): `ψ_n^{(K)}\to φ_K \Rightarrow φ_n^{(K)}\to φ_K`, every fixed `K\ge1` | **PROVED** (§2), fully general in `K`, no citations beyond elementary limit algebra |
| 2 | `ψ_n^{(1)} = 2/3+1/(6n)` exactly | **PROVED** (§3), verified vs. brute force `n=2..9` |
| 3 | `ψ_n^{(1),R} = 1/2+1/(2n)` exactly | **PROVED** (§3), verified vs. brute force `n=2..9` |
| 4 | `K=1` Open Lemma, via Lemma A + #2 | **PROVED**, independent cross-check of `THEOREM.md` Prop. 4 |
| 5 | Lemma B (co-cycle lemma, `P=1/2`) | **PROVED** (§4.1), elementary |
| 6 | `ψ_n^{(2)} = 8/15+4/(15n)+1/(15n^2)` exactly | **PROVED** (§4), case analysis verified vs. brute force `n=3..8`, *and* case formulas independently cross-checked (not just final answer) |
| 7 | **`K=2` Open Lemma**: `φ_n^{(2)}\to φ_2` | **PROVED** (§5) — closes an item `THEOREM.md` §9 lists as open |
| 8 | `ψ_n^{(2),R} = (5n+2)(n+1)/(12n^2)` exactly | **CONFIRMED BY EXACT FIT** (§6): 3-parameter fit matching 6/6 independent brute-force points exactly; not derived from first principles here |
| 9 | `φ_n^{(2)} = 8/15+1/(30n)+7/(10n^2)+1/(5n^3)` exactly | **PROVED modulo #8's status** (§6): exact given #6+#8; matches `THEOREM.md`'s own table 7/7 including `n=2` |
| 10 | True rate of `φ_n^{(2)}-φ_2` is `Θ(1/n)`, not `Θ(1/n^2)` | **RESOLVED for K=2** (§6) — answers `THEOREM.md` §9 item 2 at `K=2` specifically |
| 11 | General-`K` combinatorial cost characterization (§7.1) | **ARGUED**, not formally proved as a lower bound — an honest accounting of the method's branching, not a hardness theorem |
| 12 | Conjectural Lemma B′ (§7.2) — the named missing fact for general `K` | **STATED, NOT PROVED** — this is the sharpened open problem |
| 13 | `ψ_n^{(3)}` numerically consistent with `\to φ_3` at rate plausibly `Θ(1/n)` | **NUMERICALLY SUPPORTED ONLY** (§7.3), `n\le8`, explicitly not a rate claim |
| 14 | Open Lemma for `K\ge3` | **OPEN** — not advanced to a proof by this document |

**One line on faithfulness to the task's coupling sketch.** §1 restates §7.4's sketch
precisely; §2–§6 do **not** execute that exact joint-space coupling (the "build both
`(π,U)` and `(S,Θ,E)` on one space" construction) — they execute an equivalent but more
direct discrete-side computation that achieves the same conclusion at `K=1,2` without
needing to construct the joint space explicitly. This is disclosed, not hidden: §7.2
names the joint-coupling route as a genuine alternative not pursued, and is honest that
this document's actual method, while inspired by and validating the sketch's heuristic
(`O(K^2/n)`-type collision events do appear, informally, as the "off-`C_0`, landing on
already-visited territory" branches of §4.3), is not literally "the coupling of §7.4,
executed" — it is a different, self-contained route to the same target, whose relation
to the sketch is exactly as described in §1's closing paragraph.

---

## 9. Files, reproducibility

All scripts use exact rational arithmetic (`fractions.Fraction` or `sympy.Rational`) —
no floating point enters any PROVED claim above; floats appear only for human-readable
display. Every brute-force run enumerates **all** `n!\times n^K` `(π,U_1,…,U_K)`
combinations exhaustively — not sampled.

- `psi_bruteforce.py` — exhaustive enumeration of `ψ_n^{(K)}` and `ψ_n^{(K),R}` for any
  `K`; `psi_k1_generic.log`, `psi_k1_rerouted.log`, `psi_k2_generic.log`,
  `psi_k2_rerouted.log` are its outputs for `K=1,2`, `n` up to `8` or `9`.
- `psi_k2_case_formula.py` — evaluates §4.3's case-(a)/(b)/(c) formulas directly (not
  the summed closed form), cross-checking the *case analysis itself* against brute
  force; `psi_k2_case_formula.log` is its output, `n=3,…,8`.
- `derive_closed_forms.py` — the full symbolic pipeline: (1) sums the case formulas in
  closed form via `sympy` and checks against brute force; (2) fits `ψ_n^{(2),R}` by
  exact rational interpolation and checks the fit against held-out brute-force points;
  (3) recombines via Lemma A and checks against every value in `THEOREM.md` §7.4's own
  table. `derive_closed_forms.log` is its full output.
- `psi_k3_exploration.py` — secondary, exploratory brute force for `K=3` (§7.3);
  `psi_k3_exploration.log` is its output, `n=4,…,8`.

To reproduce everything from scratch: `python3 psi_bruteforce.py 1 9 generic`,
`... 1 9 rerouted`, `... 2 8 generic`, `... 2 8 rerouted`; `python3
psi_k2_case_formula.py 8`; `python3 derive_closed_forms.py`; `python3
psi_k3_exploration.py 8`. All run in well under `2` minutes total except the `K=2`,
`n=8` brute-force runs (`~5s` each) and the `K=3`, `n=8` run (`~36s`).
