# The K=3 Open Lemma, attempt 2 — a K-uniform transfer-matrix method

> **Governance.** `DISC-DEC-027`, front (c), `K3-OPEN-LEMMA-ATTEMPT-2`. Pure
> combinatorial mathematics — no external data, no holdout, no real-world claim, no
> governance edits. `THEOREM.md`, `ATTEMPT.md` (wave 5, in the parent directory) and
> `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` are **not** touched by this document —
> everything here lives under this new `k3_attempt_2/` directory. No git commit was
> made. Every claim below is labeled PROVED, NUMERICALLY VERIFIED (exact rational
> arithmetic, not sampling), CONJECTURED, or OPEN, following the same discipline
> `THEOREM.md`/`ATTEMPT.md` use throughout.

> **Task.** `ATTEMPT.md` (wave 5) closed the `K=2` case of `THEOREM.md` §7.4's Open
> Lemma unconditionally, by a hand case-analysis (three cases on where the two
> sources land relative to the reference point's own π-cycle, tied together by an
> elementary "co-cycle lemma" with a `P=1/2` symmetry). It explicitly left `K≥3`
> open, diagnosing *why* the same hand-casework explodes combinatorially with `K`
> (§7.1 there) and naming, as the missing ingredient, a conjectural `K`-source
> generalization of its co-cycle lemma (its "Lemma B′", §7.2). This document was
> asked to try a genuinely different technique — not another round of hand casework —
> and, in particular, to try approach (b) named in the task brief: *a
> generating-function/transfer-matrix approach across all `K` simultaneously instead
> of case-by-case.*

> **Executive summary (read first).** This document finds and executes exactly such
> a technique: instead of a hand case-split on "where do the sources land," the
> discrete exploration walk from wave 5's §2 (Reduction Lemma A) is reformulated as
> an explicit, exact, **`K`-uniform Markov chain** on a 3-integer state `(a,b,r)` —
> the same walk, but tracked by state instead of by enumerated cases — whose exact
> transition probabilities are derived once, for general `K`, from the same
> elementary permutation-exchangeability fact wave 5 already used (§2 below). Solving
> this chain in closed form is then a *mechanical* algorithm (an exact linear
> recursion solved by a standard "falling-factorial/hockey-stick" telescoping
> identity, executed symbolically) — not a new hand argument for each `K`. Result:
> - **The `K=3` case of the Open Lemma is PROVED (§4–§5):**
>   `ψ_n^{(3)} = 16/35 + 12/(35n) + 5/(28n²) + 3/(70n³)` exactly, for every `n≥4`,
>   and by wave 5's Reduction Lemma A this proves `φ_n^{(3)} → φ_3 = 16/35`
>   unconditionally. The full rate is also obtained:
>   `φ_n^{(3)} = 16/35 + 1/(14n) + 11/(10n²) + 23/(35n³) + 6/(35n⁴)`, exactly.
> - **Verified six independent ways** (§6): the method reproduces wave 5's *already
>   proved* `K=1,2` closed forms exactly (§4); the `K=3` closed form matches wave 5's
>   own brute-force log at `n=4..8`; it matches a **fresh** brute-force run at `n=9`
>   (never computed before, genuinely new); it matches an independently-coded direct
>   (non-symbolic) recursion at `n=4..9`; the *full* `φ_n^{(3)}` formula matches a
>   third, independently-coded brute-force enumeration of the raw Definition-4
>   average (not the single-reference-point machinery) at `n=4..7`; **20/20** automated
>   checks pass (`verify_all.py`, `verify_all.log`).
> - **Bonus, general `K` (§7):** the same mechanical method, run one level further,
>   gives `K=4` and `K=5` closed forms too (both verified against fresh brute force),
>   revealing an exact pattern in the leading correction: the coefficient of `1/n` in
>   `ψ_n^{(K)}` equals `Kφ_K/4` for `K=1,2,3,4,5` — five independent exact
>   confirmations of one clean formula. This is reported as a strongly-supported
>   **CONJECTURE for general `K`**, not a proof (§7.3 states precisely what is
>   missing for a general-`K` proof).
> - **What this does *not* close:** a fully general (symbolic-`K`) closed form for
>   `ψ_n^{(K)}`, or a proof of the rate conjecture for every `K` at once. §7.3 states
>   precisely where that would-be proof is blocked and why it is a different, harder
>   problem than "solve one more level of the recursion."

---

## 0. Relationship to wave 5's `ATTEMPT.md` — what is reused, what is new

Reused **verbatim, without re-derivation**, as established, PROVED facts from
`../ATTEMPT.md`:

- **Definition 4 / component quantities** (`../ATTEMPT.md` §2): `ψ_n^{(K)} :=
  P(K{+}1\text{ cyclic})` (generic reference point), `ψ_n^{(K),R} := P(1\text{
  cyclic})` (a rerouted source as reference point).
- **Lemma A (Reduction Lemma, PROVED, every fixed `K≥1`)** (`../ATTEMPT.md` §2):
  `φ_n^{(K)} = (K/n)ψ_n^{(K),R} + (1-K/n)ψ_n^{(K)}` exactly, and consequently
  `ψ_n^{(K)}\to φ_K \Rightarrow φ_n^{(K)}\to φ_K`. This document does not re-prove
  Lemma A — it is cited and used exactly as wave 5 proved it, general in `K` already.
- **The classical cycle-length fact** (`THEOREM.md` §7.3 Step 1, `../ATTEMPT.md` §3):
  for a uniform random permutation of a finite set of size `N`, any fixed point's
  cycle length is exactly `\mathrm{Unif}\{1,\dots,N\}`, and — the form actually used
  below — the "lazy revelation" fact that images of a uniform random permutation can
  be revealed one query at a time, each new query uniform over not-yet-assigned
  targets, regardless of the (possibly adaptive) order of querying.
- `φ_K = 4^K(K!)^2/(2K{+}1)!` (`THEOREM.md` Lemma 2, §5.2, the Wallis-integral mean).

**New in this document:** everything else. In particular, wave 5's Reduction Lemma A
reduces the Open Lemma to convergence of `ψ_n^{(K)}` alone; wave 5 then computed
`ψ_n^{(K)}` for `K=1,2` by an explicit hand case-analysis specific to those `K`
(three cases at `K=2`, tied together by a hand-proved co-cycle symmetry). **This
document computes `ψ_n^{(K)}` (and `ψ_n^{(K),R}`) by a completely different route: an
exact Markov chain on the exploration walk, general in `K` by construction, solved by
a mechanical algorithm rather than a per-`K` case split.** §1–§3 set this up; §4
executes it at `K=1,2` as a validation (reproducing wave 5's proved formulas exactly,
by a different method); §5 executes it at `K=3` (new); §6 verifies; §7 pushes it to
`K=4,5` as a bonus and states the general-`K` conjecture and its precise obstruction.

---

## 1. Setup: the discrete exploration walk, restated

Model (`THEOREM.md` Definition 1/4, `../ATTEMPT.md` §1–§2, unchanged): fix `n`, fix
`K` labeled sources `{1,\dots,K}\subset[n]` (WLOG by exchangeability). `π` is a
uniform random permutation of `[n]`; `U_1,\dots,U_K` are i.i.d. `\mathrm{Unif}[n]`,
independent of `π` and of each other; `f(i)=U_i` for `i\le K`, `f(i)=π(i)` otherwise.
Fix a reference point `x^*` and ask whether `x^*` is cyclic under `f`.

**The walk.** Trace the forward orbit `y_0=x^*,\,y_1=f(y_0),\,y_2=f(y_1),\dots` At
each step, if the current point `y_t` is **not** a source, the next point is
`π(y_t)` (queried, if not already known, as described in §2); if `y_t` **is** a
source, the next point is its own `U_{y_t}` (independent, uniform on `[n]`, used
exactly once — the moment the walk first reaches that source). `x^*` is cyclic iff
the walk returns to `y_0` before it revisits any other earlier point of the walk (a
revisit of any `y_s`, `s\ge1`, closes a cycle not containing `x^*`, ending the
exploration in failure; reaching `y_0` again ends it in success). This is exactly
`../ATTEMPT.md` §1/§3's walk, restated so it can be tracked by a state instead of
enumerated by hand.

**Two ways a point can enter the "visited" set — the key bookkeeping distinction.**
This is the one idea in this document that wave 5's hand case-analysis did not need
to isolate explicitly (its `K=2` cases folded it into the case structure by hand; at
general `K` it must be tracked explicitly, which is exactly what makes a `K`-uniform
treatment possible):

- A point reached via a **π-query** (`y_t` not a source, `π(y_t)` newly revealed) can
  **never be revisited by a later π-query** — `π` is a bijection, so an already-used
  image can never recur as a later image. Such a point, once passed, permanently
  leaves the pool of possible future π-targets.
- A point reached via a **U-jump landing on fresh territory** (`y_t` a source,
  `U_{y_t}` lands on a point never seen before) is **not** thereby removed from the
  pool of future π-targets — its own `π`-image was never queried (sources' π-images
  are simply never looked at by this walk), so it remains, from π's perspective, an
  "unassigned" point that a **later** π-query could still land on. This is a genuine
  new failure mode with no `K=1` analogue: a π-step colliding with a previously
  U-visited point.

This distinction is exactly what the Markov chain state below tracks.

---

## 2. The Markov chain: state, transitions, and their derivation from first principles

**State**, while at some point `y_t` on the walk, having not yet succeeded or failed:

- `a` := number of π-queries made so far (= number of distinct points reached via a
  π-step, whatever the outcome of each query) — these points are permanently removed
  from the future π-target pool.
- `b` := number of points reached so far via a U-jump onto fresh territory — these
  remain available as future π-targets (the "poisoned" points of §1).
- `r` := number of the `K` sources not yet reached by the walk.

Write `g(a,b,r) := P(x^*\text{ eventually cyclic})` starting from a **non-source**
current point in this state (about to make a π-query), and `h(a,b,r)` for the same
starting from a **source** current point (about to draw its own `U`). By definition,
`ψ_n^{(K)} = g(0,0,K)` (`x^*` starts at a non-source point, nothing visited yet, all
`K` sources unreached) and `ψ_n^{(K),R} = h(0,0,K{-}1)` (`x^*` itself is one of the
`K` sources — the reference point *is* the current point about to draw its own `U`,
with the other `K{-}1` sources unreached).

> **Proposition (exact transition rules, PROVED).** For every `n`, `K`, and every
> reachable state `(a,b,r)` with `a+b+r<n`:
>
> **Non-source step** (pool of still-unassigned π-targets has size `m:=n-a`):
> `g(a,b,r) = \dfrac1m + \dfrac{r}{m}\,h(a{+}1,b,r{-}1) + \dfrac{m{-}1{-}r{-}b}{m}\,g(a{+}1,b,r)`.
>
> **Source step** (draws `U` uniform over *all* `n` points, unconstrained by the
> π-pool):
> `h(a,b,r) = \dfrac1n + \dfrac{r}{n}\,h(a,b{+}1,r{-}1) + \dfrac{n{-}1{-}a{-}b{-}r}{n}\,g(a,b{+}1,r)`.

*Proof.* **Non-source step.** By the lazy-revelation fact (§0), `π(y_t)`, queried
for the first time, is uniform over the `n-a` points not yet assigned as some
π-image — call this pool `\mathcal P`, `|\mathcal P|=m=n-a`. `\mathcal P` decomposes
exactly into: `\{y_0\}` (`1` point — landing here is success, since `y_0` has not yet
been used as any π-image, as the walk has not yet succeeded); the `r` not-yet-reached
sources (landing on one is a "continue," moving to a source with one fewer remaining
unreached source, and this π-query — like every π-query — increments `a`, so the new
state is `(a{+}1,b,r{-}1)`, entering `h`); the `b` "poisoned" points reached earlier
via a U-jump (still in `\mathcal P` by §1's observation — landing on one is a
failure, since it revisits an earlier walk point, closing a cycle not containing
`y_0`); and the remaining `m-1-r-b` points, never visited by the walk and not
sources (landing on one is a "continue" at a non-source, state `(a{+}1,b,r)`,
entering `g` again). Dividing each count by `m` gives exactly the stated formula.

**Source step.** `U_{y_t}` is a fresh i.i.d. `\mathrm{Unif}[n]` variable, entirely
unconstrained by anything revealed so far (it is not a π-image at all, and is
independent of every other source's own `U` and of `π`). It is uniform over all `n`
points of `[n]`, which decompose into: `\{y_0\}` (`1` point, success); the `a+b`
already-visited points other than `y_0` (`a` reached via π, `b` reached via earlier
U-jumps — landing on **either** kind is a failure, by the same revisit argument as
above, since `U` has no injectivity constraint the way π does: unlike a π-query, a
U-jump genuinely can land on an already-π-visited point, this being exactly the
"collision" wave 5's §7.4/§1 coupling sketch names); the `r` not-yet-reached sources
(continue, to `h(a,b{+}1,r{-}1)` — this step does **not** touch `a`, since it is not
a π-query, but the point reached, being freshly visited via a U-jump, adds `1` to
`b`); and the remaining `n-1-a-b-r` points (continue, to `g(a,b{+}1,r)`). Dividing by
`n` gives the stated formula. `∎`

**Base cases.** `g(a,b,r)` and `h(a,b,r)` are always well-defined probabilities in
`[0,1]`, and the recursion terminates because `a+b` strictly increases with every
non-terminal step and is bounded by `n`; formally, the closed-form solution below
(§3) is derived with the convention `g(b{+}r,b,r):=0`, i.e. the value "just before"
the state where the "continue at the same `r`" coefficient `(m{-}1{-}r{-}b)/m`
vanishes — this is not an extra assumption, it is exactly what the recursion's own
coefficient forces (§3 checks this is consistent, not merely assumed).

**Independent sanity check of the model itself (not just its closed-form solution).**
`markov_direct.py` implements exactly the two formulas above as a plain memoized
exact-fraction recursion (`fractions.Fraction`, no symbolic algebra, no summation
identity) for concrete integer `n`, and checks `g(0,0,K)` against
`psi_bruteforce_ref.py`'s **exhaustive enumeration of the raw definition** (all `n!
\times n^K` `(π,U)` tuples). This matches exactly for `K=1` (`n=2..8`), `K=2`
(`n=3..8`), and `K=3` (`n=4..9`) — see `verify_all.log` STEP 4 and `n9_check.log`.
Since this check never invokes the telescoping-sum solution of §3 at all, it is
independent evidence that the *transition rules themselves* (not merely their
downstream algebra) are exactly right.

---

## 3. Solving the recursion: an exact, mechanical algorithm (general in `K`)

**The dependency structure.** Fix `K`. To compute `ψ_n^{(K)}=g(0,0,K)`, unwind the
transition rules: `g` at "level" `r` needs `h` at level `r{-}1` (same `b`); `h` at
level `r` needs `g` and `h` at level `r` and `r{-}1` respectively, both evaluated at
`b{+}1`. So the computation only ever needs `g_r,h_r` — the functions `g(\cdot,\cdot,r)`
and `h(\cdot,\cdot,r)`, for **one value of `r` at a time** — as functions of the two
remaining variables `(a,b)` (equivalently `(m,b)` with `m=n-a`), **not restricted to
one fixed `b`**: `g_0`, then `h_0`, then `g_1`, then `h_1`, …, up to `g_K` — a
strictly increasing ladder of `2K{+}1` closed forms, each built from the previous
one, with no case-split on `K` anywhere in the *procedure* (only the *number of
rungs climbed* depends on `K`).

**Level `0` (no sources left) — closed form independent of `n,a`.** With `r=0`, the
non-source recursion becomes `g_0(m,b) = \frac1m + \frac{m-1-b}{m}g_0(m{-}1,b)`
(fixed `b`, no `h` term). Solving (elementary induction, or telescoping — verified
below): **`g_0(m,b) = \dfrac{1}{b+1}`, for every `m\ge b{+}1`, independent of `m`
(hence of `n,a`) entirely.** *Proof by induction on `m`, base `m=b{+}1`:
`g_0(b{+}1,b)=\frac1{b+1}+0` (the "continue" coefficient vanishes there), matching
`1/(b{+}1)`. Step: if `g_0(m{-}1,b)=1/(b{+}1)`, then `g_0(m,b) = \frac1m +
\frac{m-1-b}{m}\cdot\frac1{b+1} = \frac1m\big[1+\frac{m-1-b}{b+1}\big] =
\frac1m\cdot\frac{m}{b+1}=\frac1{b+1}`.* `∎` This already reproduces, as the special
case `b=1`, wave 5's **co-cycle Lemma B** (`../ATTEMPT.md` §4.1, `P=1/2`
independent of `m`) — here obtained as one instance of a fact true for *every* `b`,
not a standalone lemma needing its own proof: `g_0(m,1)=1/2` for every `m\ge2`. (This
is the precise sense in which this document answers part of the task's question (a) —
*is there a more general symmetry, of which `K=2`'s `P=1/2` is one instance?* — Yes:
`g_0(m,b)=1/(b{+}1)`, exactly, for every `b`, is that general fact; §7.3 discusses why
it alone is not enough to close general `K`.)

**Level `r\ge1` — telescoping.** With `b` fixed, `g_r(m,b)` solves
`g_r(m) = \frac1m + \frac{r}{m}h_{r-1}(n{-}m{+}1,b) + \frac{m-1-r-b}{m}g_r(m{-}1)`,
a first-order linear recursion in `m` with forcing term `c_r(m) := \frac1m +
\frac{r}{m}h_{r-1}(n{-}m{+}1,b)`. Writing `j:=r{+}b{+}1` (the value of `m` at which
the "continue" coefficient vanishes, i.e. the base case), the standard
falling-factorial telescoping identity gives the closed-form solution

`g_r(m,b) = \dfrac{\sum_{k=j}^{m} c_r(k)\binom{k}{j}}{\binom{m}{j}}`,

which is summed in closed form via `\sum_k \binom{k}{j}=\binom{m{+}1}{j{+}1}`
(hockey-stick) after rewriting `c_r(k)`'s `1/k` term via `\frac1k\binom kj =
\frac1j\binom{k-1}{j-1}` (a standard identity) — see `markov_transfer.py`'s
`g_closed_via_telescoping`, which performs exactly this and lets `sympy` complete the
sum (`sympy.summation`, exact, symbolic in `n` and in `b`) rather than doing the
binomial bookkeeping by hand at each `r` (safer against algebra slips; every output
is checked against known/brute-force values below). `h_r(a,b)` is then **immediate
algebra**, not a further summation: `h_r(a,b) = \frac1n + \frac rn h_{r-1}(a,b{+}1) +
\frac{n-1-a-b-r}{n}g_r(a,b{+}1)`, plugging in the just-derived `g_r` (at `b{+}1`) and
the previous level's `h_{r-1}` (at `b{+}1`).

**This is the `K`-uniform algorithm**: climb the ladder `g_0\to h_0\to g_1\to h_1\to
\cdots\to g_K`, each rung an exact, mechanical step (one closed-form telescoped sum,
one algebraic substitution), with **no per-`K` case analysis** — the same two-line
procedure produces the `K=1`, `K=2`, `K=3`, `K=4`, `K=5` closed forms below, differing
only in how many times it is iterated. This is exactly the "transfer-matrix approach
across all `K` simultaneously" the task brief asked to try (its option (b)): the
"transfer matrix" is the `(g_r,h_r)` pair viewed as a linear operator advancing the
walk by one step, and "simultaneously" means the *procedure* is `K`-independent even
though each individual output is computed one `K` at a time.

---

## 4. Validation at `K=1,2`: the method reproduces wave 5's proved theorems exactly

Running the ladder to `r=1` and `r=2` and evaluating at `(a,b)=(0,0)`:

> `ψ_n^{(1)} = \dfrac{4n+1}{6n} = \dfrac23+\dfrac1{6n}`
> — **identical** to `../ATTEMPT.md` §3's independently, hand-derived formula.
>
> `ψ_n^{(2)} = \dfrac{8n^2+4n+1}{15n^2} = \dfrac{8}{15}+\dfrac{4}{15n}+\dfrac1{15n^2}`
> — **identical** to `../ATTEMPT.md` §4.4's formula, itself a PROVED theorem (closing
> `THEOREM.md`'s Open Lemma at `K=2`, verified by an independent adversarial referee,
> `DISC-DEC-022`).

Both matches are **exact** (`sympy` symbolic difference `=0`, `verify_all.log` STEP
1), not merely numerically close. Since `../ATTEMPT.md`'s `K=1,2` closed forms were
derived by a completely different method (hand case-analysis on where the sources
land relative to `x^*`'s own `π`-cycle, §3–§4 there) and independently proved
correct (Proposition 4 of `THEOREM.md` for `K=1`, adversarial referee for `K=2`),
this is strong evidence that the Markov-chain reformulation and its telescoping
solution (§2–§3 here) are themselves correct — a new method reproducing two
already-proved theorems exactly is the best available check on the method, prior to
trusting it on the genuinely new `K=3` case.

---

## 5. The `K=3` result

Running the ladder one rung further, to `r=3`:

> **Theorem (`ψ_n^{(3)}` exact closed form; PROVED).** For every `n\ge4`,
>
> `ψ_n^{(3)} = \dfrac{64n^3+48n^2+25n+6}{140n^3} = \dfrac{16}{35}+\dfrac{12}{35n}+\dfrac5{28n^2}+\dfrac3{70n^3}`.

*Proof.* §2's Proposition gives the exact transition rules for every `K`, in
particular `K=3`; §3's telescoping algorithm solves them level by level
(`g_0,h_0,g_1,h_1,g_2,h_2,g_3`), each step an exact identity (elementary induction at
`r=0`, standard hockey-stick binomial summation — executed symbolically, `sympy` —
at `r\ge1`); `ψ_n^{(3)}=g_3(n,0)` is the result of substituting `m=n,b=0` into the
level-`3` closed form. Every step of this chain is an *equality*, not an
approximation or a fit — there is no free parameter anywhere in the derivation (contrast
this with `../ATTEMPT.md` §6's `ψ_n^{(2),R}`, which that document obtained by exact
rational **interpolation** and flagged "CONFIRMED BY EXACT FIT, not derived from
first principles" — nothing in *this* document's `K=3` derivation is a fit; see §6.5
below for the analogous `ψ_n^{(3),R}` quantity, which *this* document derives from
first principles too, by the same route). `∎`

> **Corollary (`K=3` case of the Open Lemma; PROVED, unconditional).**
> `\displaystyle\lim_{n\to\infty}φ_n^{(3)} = φ_3 = \dfrac{4^3(3!)^2}{7!}=\dfrac{16}{35}`.

*Proof.* `ψ_n^{(3)}\to16/35=φ_3` by the Theorem above; by wave 5's Reduction Lemma A
(`../ATTEMPT.md` §2, PROVED for every fixed `K\ge1`, cited verbatim in §0), this
alone implies `φ_n^{(3)}\to φ_3`, regardless of the behaviour of `ψ_n^{(3),R}`. `∎`

**What this establishes relative to `THEOREM.md`/`../ATTEMPT.md`.** `THEOREM.md`
§7.4's Open Lemma is left open for every `K\ge2`; `../ATTEMPT.md` closes `K=2`
unconditionally and states `K\ge3` as open, diagnosing precisely why its method does
not extend (§7 there). This document closes `K=3` — the very case wave 5 named as
the sharpened open problem — **unconditionally**, by a method wave 5 did not use and
that was explicitly requested by this task's brief. `THEOREM.md`'s Proposição
Condicional 5 (§7.5, the general `n\to\infty` bridge, conditional on the Open Lemma
for every `K\ge2`) is therefore now unconditional at `K=0,1,2,3`; the residual
condition, after this document, is exactly `K\ge4`.

**The full rate, as a bonus (paralleling `../ATTEMPT.md` §6's `K=2` bonus result).**
Computing `ψ_n^{(3),R} = h_2(0,0)` (the reference point is itself one of the three
sources) by the *same* first-principles method — no fitting — gives

`ψ_n^{(3),R} = \dfrac{22n^3+39n^2+23n+6}{60n^3} = \dfrac{11}{30}+\dfrac{13}{20n}+\dfrac{23}{60n^2}+\dfrac1{10n^3}`,

and recombining via Lemma A (`φ_n^{(3)} = \frac3n ψ_n^{(3),R}+(1-\frac3n)ψ_n^{(3)}`):

> **`φ_n^{(3)} = \dfrac{32n^4+5n^3+77n^2+46n+12}{70n^4} = \dfrac{16}{35}+\dfrac1{14n}+\dfrac{11}{10n^2}+\dfrac{23}{35n^3}+\dfrac6{35n^4}`**,
> exactly, for every `n\ge4` — **PROVED**, not fit (both `ψ_n^{(3)}` and
> `ψ_n^{(3),R}` are first-principles outputs of the same §2–§3 algorithm).

**The rate.** `φ_n^{(3)}-φ_3 = \frac1{14n}+\frac{11}{10n^2}+\frac{23}{35n^3}+\frac6{35n^4}`
is `\Theta(1/n)` (leading coefficient `1/14`), matching the pattern `../ATTEMPT.md`
§6 already found at `K=2` (`\Theta(1/n)`, not the naively-expected `\Theta(1/n^2)` of
`K=1`) — see §7.4 for the general-`K` version of this observation.

---

## 6. Verification (before trusting the closed form, per the task's own instruction)

The task brief asked explicitly that any candidate closed form be checked against
`psi_k3_exploration.py`'s brute-force values *before* being trusted, "exactly like
wave 5's practice." This was done, in six independent layers (`verify_all.py`
automates 1–2, 4–6; `n9_check.log` documents 3 in full):

1. **Reproduction of already-proved theorems (§4).** The method reproduces
   `../ATTEMPT.md`'s proved `K=1,2` closed forms exactly, by a different derivation.
2. **Wave 5's own `K=3` brute-force log.** `ψ_n^{(3)}` matches
   `../psi_k3_exploration.log` exactly at `n=4,5,6,7,8` (`71/128`, `1333/2500`,
   `187/360`, `4897/9604`, `18023/35840`) — every value wave 5 had already computed
   and left unexplained.
3. **A fresh, held-out brute-force point at `n=9`** (never computed in wave 5, which
   explicitly stopped at `n=8`, "n=9 was not attempted"). This document's closed
   form was derived and cross-checked against `n=4..8` *first*; `n=9` was then
   computed independently via exhaustive enumeration (`9!\times9^3=264{,}539{,}520`
   exact-rational combinations, `448.6`s, `psi_bruteforce_ref.py`) as a genuine
   out-of-sample check, not used in the derivation. Result: `3385/6804`, matching the
   closed form exactly (`n9_check.log`).
4. **An independently-coded direct recursion** (`markov_direct.py`, plain memoized
   `fractions.Fraction` arithmetic implementing §2's transition rules directly, no
   symbolic summation) matches both the closed form *and* brute force exactly at
   `K=1,2,3` for every tested `n` (`n=2..8`, `3..8`, `4..9` respectively) — this
   checks the *model* (§2), independently of whether §3's summation algebra is
   correct.
5. **A third, independently-coded brute force of the *full* Definition-4 average**
   (`phi_bruteforce_full.py` — computes `φ_n^{(K)}` directly by counting cyclic
   points over *all* `n` positions, not via the single-reference-point machinery
   `psi_bruteforce_ref.py`/`markov_direct.py` share) confirms the *recombined*
   `φ_n^{(3)}` formula (§5's bonus result) exactly at `n=4,5,6,7`
   (`71/128,1628/3125,181/360,41327/84035`) — the strongest available check, since it
   validates the Lemma-A recombination against a computation that never uses Lemma A
   or the generic/rerouted split at all.
6. **`verify_all.py`**: `20/20` automated checks pass (`verify_all.log`); the one
   slow step (fresh `n=9` brute force, `\sim7.5` min) is documented separately in
   `n9_check.log` rather than re-run by default.

No numerical evidence anywhere in this document is treated as a substitute for the
derivation of §2–§3 (which is a proof, not a fit); the brute-force checks are exactly
what the task asked for — confirmation *before trusting*, not a replacement for
derivation.

---

## 7. Bonus: `K=4`, `K=5`, and a general-`K` rate conjecture

Since §3's algorithm is mechanical and `K`-uniform, it costs nothing conceptually to
climb further. This was not required by the task (`K=3` was the target), but was run
as a natural stress-test of the method and produced a genuine bonus finding.

### 7.1 `K=4`, `K=5`: further exact closed forms, both verified

> `ψ_n^{(4)} = \dfrac{128n^4+128n^3+103n^2+52n+12}{315n^4} = \dfrac{128}{315}+\dfrac{128}{315n}+\dfrac{103}{315n^2}+\dfrac{52}{315n^3}+\dfrac4{105n^4}`
>
> `ψ_n^{(5)} = \dfrac{1024n^5+1280n^4+1405n^3+1105n^2+538n+120}{2772n^5}`

Both checked against fresh brute force (not previously computed anywhere in this
archive): `ψ_n^{(4)}` at `n=5` (`1569/3125`) and `n=6` (`196/405`); `ψ_n^{(5)}` at
`n=6` (`899/1944`) — all exact matches (`verify_all.log` STEP 6). `φ_4=128/315`,
`φ_5=256/693` (Wallis-integral means, `THEOREM.md` §5.2), both reproduced exactly as
the `n\to\infty` limit of the corresponding closed form.

### 7.2 An exact pattern in the leading correction

> **Observation (NUMERICALLY VERIFIED for `K=1,\dots,5`, CONJECTURED for general
> `K`).** `\displaystyle\lim_{n\to\infty} n\big(ψ_n^{(K)}-φ_K\big) = \dfrac{K}{4}φ_K`.

| `K` | `φ_K` | coefficient of `1/n` in `ψ_n^{(K)}` | `Kφ_K/4` | match |
|---|---|---|---|---|
| 1 | `2/3` | `1/6` | `1/6` | exact |
| 2 | `8/15` | `4/15` | `4/15` | exact |
| 3 | `16/35` | `12/35` | `12/35` | exact |
| 4 | `128/315` | `128/315` | `128/315` | exact |
| 5 | `256/693` | `320/693` | `320/693` | exact |

Five consecutive, independently-derived exact matches (each `ψ_n^{(K)}` is itself a
full first-principles closed form, not a fit — the *pattern* across them is what is
conjectural, not any individual entry) make this an unlikely coincidence, but it is
reported as a **CONJECTURE**, not a theorem: no argument below proves it for general
`K`, only for the five values actually computed.

### 7.3 Why this document does not attempt a general-`K` proof, precisely

The obstruction is different in kind from wave 5's `../ATTEMPT.md` §7.1 obstruction
(combinatorial explosion in the number of *hand cases*). Here the *procedure* is
already `K`-uniform (§3) — the obstruction is instead that **the procedure has not
been solved "in `r`."** Concretely: `g_r(m,b)` was computed, symbolically, for
`r=0,1,2,3,4,5` **one integer at a time** — each level's telescoping sum needs the
*previous* level's closed form substituted in as an explicit rational function of
`(n,a,b)` before `sympy` can execute the next `\sum_k(\cdot)\binom kj` (§3). Making
`r` itself a free symbolic variable inside that sum (i.e., summing with a *symbolic*
number of "levels already climbed" baked into the forcing term `c_r(k)`) is a
qualitatively different — and harder — problem: the forcing term `c_r(k)` is itself
only known as a closed form *after* solving level `r{-}1`, so there is no
single expression "`h_r(a,b)`, `r` symbolic" to sum against; what would be needed is
either (i) an inductive proof, on `r`, that the closed form has a specific
**predicted general shape** (e.g., a rational function of `n` with numerator/
denominator degree growing linearly in `r`, plausible from the `r=0..5` data but not
derived here) *and* that this shape is preserved by one more application of §2's
recursion — an induction this document did not attempt to carry out symbolically —
or (ii) an entirely different, generating-function-in-`K` argument (e.g. summing
`\sum_K x^K/K!\cdot ψ_n^{(K)}` and finding a closed-form ODE/PDE governing it in
`n`), not attempted here. **This is the precise, sharpened obstruction**: not "more
hand cases," as in wave 5, but "an induction on `r` through the telescoping-sum
solution, or a generating-function argument, neither of which has been carried out."
Either route is a plausible, concrete next step (unlike wave 5's `K\ge3` obstruction,
which had no similarly concrete candidate route named) — but it is a different,
harder task than the one this document completed (`K=3`, exactly, plus `K=4,5` as
confirmatory extensions of the same finite computation).

### 7.4 The general-`K` rate, restated precisely

If the §7.2 conjecture holds for every `K`, then combined with wave 5's Lemma A
(which shows the `ψ_n^{(K),R}` contribution to `φ_n^{(K)}` is `O(K/n)`, i.e. the same
order, so it does *not* automatically wash out the way it did at `K=1` — recall
`../ATTEMPT.md` §3's exact `\Theta(1/n)\to\Theta(1/n^2)` cancellation was a `K=1`-only
special feature, not a general pattern, exactly as `../ATTEMPT.md` §6 already
concluded from `K=2` alone and this document's `K=3` full-rate result, §5, confirms
again) this would give `φ_n^{(K)} = φ_K + \Theta(1/n)` for every `K\ge2` — resolving
`THEOREM.md` §9 item 2 ("whether `φ_n^{(K)}-φ_K` is `Θ(1/n^2)`, `Θ(\log n/n^2)`, or
something else... is left fully open") for every `K` at once, **conditionally on the
§7.2 conjecture**. This document does not claim this resolution as proved beyond
`K=3` (§5's own unconditional result).

---

## 8. Answering the task's three named approaches directly

- **(a) A more general symmetry, of which `K=2`'s `P=1/2` is one instance?** **Yes,
  found**: `g_0(m,b)=1/(b{+}1)`, exact and independent of `m` (hence of `n`) for
  every `b\ge0` (§3) — wave 5's Lemma B is the `b=1` case. This is a genuine,
  general-`K`-relevant symmetry (it governs the "no sources left" tail of the walk at
  *every* `K`), but by itself it only handles the `r=0` rung of the ladder; closing
  `K=3` needed climbing three more rungs (`h_0,g_1,h_1,g_2,h_2,g_3`), each an exact
  but `b`-dependent (not merely `m`-independent) computation — so the search for "the
  symmetry" was productive but the symmetry alone was not the whole answer; the
  telescoping algorithm of §3 was the piece that actually closes each level.
- **(b) A generating-function/transfer-matrix approach across all `K`
  simultaneously?** **Yes, this is what §2–§3 execute** — a `K`-uniform state machine
  and a mechanical, `K`-independent solving *procedure*, demonstrated concretely
  through `K=5`. It falls short of a single closed-form-in-`K` (§7.3), which would
  need the recursion solved symbolically "in `r`" as well — not attempted.
- **(c) An existing published combinatorial identity (random mapping / functional
  graph literature)?** **Not pursued in this document** (`THEOREM.md` §5.5 already
  cites Hansen–Jaworski 2014 for a *different but related* microscopic model's
  `K`-conditional density; this document's problem — exact finite-`n` `ψ_n^{(K)}`,
  not the `n\to\infty` density — was not checked against Hansen–Jaworski or other
  named literature beyond what `THEOREM.md`/`../ATTEMPT.md` had already located; a
  literature match for the *exact rational sequence* `ψ_n^{(K)}` or the general-`K`
  closed form, if one exists, was not searched for here and remains a candidate next
  step, not attempted for lack of time within this task's scope).

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Exact transition rules for the `(a,b,r)` Markov chain, general `K` | **PROVED** (§2), verified independently against brute force via `markov_direct.py` at `K=1,2,3` |
| 2 | `g_0(m,b)=1/(b{+}1)` (general-`b` symmetry generalizing wave 5's co-cycle Lemma B) | **PROVED** (§3), elementary induction |
| 3 | Telescoping algorithm correctly solves the recursion at each level | **PROVED in general** (§3, standard hockey-stick identity); **executed and verified** at `r=0..5` |
| 4 | `ψ_n^{(1)}`, `ψ_n^{(2)}` reproduced exactly by this method | **PROVED**, matches `../ATTEMPT.md`'s independently-proved theorems exactly (§4) |
| 5 | **`ψ_n^{(3)} = 16/35+12/(35n)+5/(28n^2)+3/(70n^3)`** | **PROVED** (§5), matches wave 5's brute force `n=4..8`, fresh brute force `n=9`, and independent direct recursion `n=4..9` |
| 6 | **`K=3` case of the Open Lemma**: `φ_n^{(3)}\to φ_3` | **PROVED** (§5) — closes an item `../ATTEMPT.md` lists as open, unconditionally |
| 7 | `ψ_n^{(3),R}` and the full rate `φ_n^{(3)}=16/35+1/(14n)+11/(10n^2)+23/(35n^3)+6/(35n^4)` | **PROVED** (§5), first-principles (not fit), matches independent full-definition brute force `n=4..7` |
| 8 | `ψ_n^{(4)}`, `ψ_n^{(5)}` closed forms | **PROVED** (§7.1), each individually a complete derivation, verified against fresh brute force |
| 9 | General-`K` rate conjecture, `\lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` | **CONJECTURED** (§7.2) — verified exactly for `K=1..5`, not proved for general `K` |
| 10 | Precise obstruction to a general-`K` (symbolic-`r`) closed form | **NAMED PRECISELY** (§7.3) — an induction-on-`r` or generating-function argument, neither attempted |
| 11 | Literature search for a matching published identity | **NOT ATTEMPTED** (§8(c)) |

**Net honest verdict.** The task's central ask — prove or precisely narrow the `K=3`
case of the Open Lemma via a genuinely different technique from wave 5's — is
**fully achieved**: `K=3` is now **PROVED**, unconditionally, exactly like `K=0,1,2`
before it, by a method (`K`-uniform transfer matrix, §2–§3) that is qualitatively
different from wave 5's hand case-analysis and that generalizes mechanically (§7,
`K=4,5` as free bonus data). What remains open is now `K\ge6` in the fully-verified
sense, or `K\ge4` in the "proved, individually, one `K` at a time, at whatever
computational cost the reader is willing to spend" sense (since the method never
required a *new idea* between `K=3` and `K=5` — only more arithmetic) — a
meaningfully narrower and more precisely characterized open problem than "`K\ge3`,
combinatorial explosion, no known route" (`../ATTEMPT.md` §7.4's own summary). The
one thing this document does **not** claim is a proof of the general-`K` case in one
shot; §7.3 states exactly what such a proof would additionally require.

---

## 10. Files, reproducibility

All scripts use exact rational arithmetic (`fractions.Fraction` or `sympy.Rational`)
throughout — no floating point enters any PROVED claim above; floats appear only for
human-readable display. Every brute-force run enumerates **all** `n!\times n^K`
`(π,U_1,\dots,U_K)` combinations exhaustively — not sampled.

- `markov_transfer.py` — the core §2–§3 machinery: exact transition rules, the
  telescoping-sum solver (`g_closed_via_telescoping`), and `psi_closed_form(K)`,
  `psi_rerouted_closed_form(K)`, `phi_closed_form(K)` for any `K`. Run directly
  (`python3 markov_transfer.py`) to print `K=0..5` closed forms, limits, and the
  §7.2 rate-coefficient check; output saved in `markov_transfer.log`.
- `psi_bruteforce_ref.py` — self-contained copy of wave 5's exhaustive
  brute-force enumeration logic (`../psi_bruteforce.py`, unmodified in content, just
  relocated so this directory is self-contained).
- `markov_direct.py` — independent, non-symbolic (plain memoized `Fraction`
  recursion) check of the §2 transition rules against `psi_bruteforce_ref.py`,
  `K=1,2,3`.
- `phi_bruteforce_full.py` — independent brute force of the *full* `φ_n^{(K)}`
  Definition-4 average (not the single-point machinery), used to check §5's
  recombined `φ_n^{(3)}` formula.
- `verify_all.py` — consolidated pipeline running all of the above and reporting
  PASS/FAIL for every check in §6; output in `verify_all.log` (`--skip-slow` flag
  used there to omit the `\sim7.5`-minute fresh `n=9` brute force, separately
  documented, with full output, in `n9_check.log`).

To reproduce everything from scratch: `python3 markov_transfer.py` (closed forms,
seconds); `python3 markov_direct.py` (direct-recursion cross-check, seconds);
`python3 verify_all.py --skip-slow` (fast checks, seconds); `python3 verify_all.py`
(same, plus the slow fresh `n=9` brute force, `\sim7.5` min); `python3
phi_bruteforce_full.py 3 7` (independent `φ_n^{(3)}` brute force, `\sim10`s total).
