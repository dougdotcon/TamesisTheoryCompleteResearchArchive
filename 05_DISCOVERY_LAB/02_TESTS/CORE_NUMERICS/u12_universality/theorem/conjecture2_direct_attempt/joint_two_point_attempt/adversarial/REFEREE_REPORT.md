# Referee report — Uniform Cyclic Restriction Theorem (Theorem J) and its Corollary

**Target document:** `../ATTEMPT.md` (joint_two_point_attempt front, Wave 17
front (c), `JOINT-TWO-POINT-EXPLORATION-ATTEMPT`).

**Scope of this review.** Exactly the two PROVED claims named in the
dispatch: **Theorem J** (Uniform Cyclic Restriction Theorem, ATTEMPT.md
§2) and its **Corollary** (exact 50/50 same/different-cycle split given
both cyclic, ATTEMPT.md §3), both stated for Definition 4's finite
conditional-`K` model. The document's other content — the open moment
targets `E[M(c)^2]=(1-e^{-c})/c`, `E[M_K^2]=1/(K+1)`, the incomplete §6.3
continuum-native construction, and the disclosed §7.1 false start — is
read for context but is **not** under review here and no verdict is
rendered on it (it is not claimed as proved by the target document
either). THEOREM.md's Definitions 1–4, §5.1, and the newly-appended
Estágio 24 section were read for ambient context as instructed; Estágio
24's closure of Conjectures 1/2 via a *different* route (Definition 3,
continuum) is unrelated to Theorem J's finite-`n` Definition-4 claim and
creates no tension with it (ATTEMPT.md's own §6.2 had already noted no
shortcut exists from the split to the moment value, which is exactly
consistent with Estágio 24 needing a wholly separate argument).

---

## Verdict

> **SOUND. ACCEPT for catalogue at the claimed tier (PROVED, elementary,
> self-contained).**

Theorem J and its Corollary hold exactly, for every `n,K` in Definition
4's model, as claimed. The proof strategy (Lemma J1: post-composition
invariance of `f`'s law under any fixed bijection of `[n]`; Lemma J2: an
explicit involutive swap bijection between the two restriction-events
`{C(h)=c, h|_c=rho}` and `{C(h)=c, h|_c=rho'}`) is correct in every step
I was able to identify, including at the specific stress points named in
the dispatch (the `|c|=2` edge case, whether `kappa` can act on anything
outside `c`, and whether the swap can silently change *which* points end
up cyclic). No counterexample was found, by hand or by exhaustive
computation, in a grid substantially larger than the one the front itself
tested. One cosmetic writing issue is named below; it does not affect
soundness.

---

## 1. Independent hand re-derivation

### 1.1 The model, restated precisely

Definition 4 (`THEOREM.md` §7.2, restated by ATTEMPT.md §1): fix `n>=2`,
`0<=K<=n`. `pi` uniform on `Sym(n)`. `R` a uniform `K`-subset of `[n]`,
independent of `pi`. For `i in R`, `U_i` i.i.d. `Uniform([n])`,
independent of `(pi,R)`. `f(i) := U_i` if `i in R`, else `pi(i)`.

Two structural facts I confirmed independently before touching Theorem J
itself, since the whole argument leans on them:

- **`f` need not be injective.** Unlike `pi`, `f` is a genuine *random
  mapping* (`U_i` can collide with `pi(j)` for `j` not in `R`, or with
  another `U_{i'}`). This matters below because it means `C(f)` (the
  cyclic set) is a proper substructure of `[n]`, not all of `[n]`, in
  general — Theorem J's restriction event `{C(f)=c}` is a genuinely
  nontrivial conditioning, not a relabeling of the whole permutation.
- **`C(f)` is always closed under `f`, and `f|_{C(f)}` is a bijection
  `C(f)->C(f)`.** This is the standard finite-functional-graph fact
  ATTEMPT.md §1 cites without further proof (also used, unattributed to
  any external source, throughout `THEOREM.md` itself, e.g. its own
  Estágio 18 Lemma B4). I re-derived it directly: every forward orbit in
  a finite functional graph is eventually periodic (pigeonhole on `[n]`
  finite); a point is cyclic iff it lies on the eventual period; the set
  of all such points is, by definition, invariant under one more
  application of `f`, and `f` restricted to it is injective (if
  `f(i)=f(j)` for two distinct cyclic `i,j`, tracing both orbits forward
  from their respective returns to themselves forces `i=j`) and
  surjective onto itself (every cyclic point is reached by its own
  predecessor on its cycle) — hence a bijection. No issue.

### 1.2 Lemma J1 (post-composition invariance) — re-derived, VALID

**Claim.** For any fixed bijection `kappa:[n]->[n]`, `kappa o f =d f`.

**My independent check.** Write `f = F(pi,R,U)` for the fixed
deterministic map `F` given by Definition 4's recipe. Two things need
to hold, and I checked each on its own terms rather than accepting the
document's assertion:

1. **A pointwise (not just distributional) algebraic identity:**
   `kappa o F(pi,R,U) = F(kappa o pi, R, kappa(U))` for *every* fixed
   `(pi,R,U)`, where `kappa(U)` denotes applying `kappa` to each
   `U_i, i in R`. Check: for `i in R`, LHS `= kappa(U_i)`; RHS
   `= (kappa(U))_i = kappa(U_i)`. For `i not in R`, LHS
   `= kappa(pi(i))`; RHS `= (kappa o pi)(i) = kappa(pi(i))`. Equal
   termwise. This is a *pure algebra* fact about the recipe `F`, true
   for literally every realization, no probability involved yet.
2. **`(kappa o pi, R, kappa(U)) =d (pi, R, U)` exactly** (full joint
   law, not just marginals). `kappa o pi`: left-multiplication by a
   fixed group element is a bijection of `Sym(n)` onto itself, so
   pushing the uniform measure on `Sym(n)` forward by it gives the
   uniform measure back — `kappa o pi ~ Uniform(Sym(n))` exactly. `R` is
   untouched. `kappa(U_i)` is `Uniform([n])` (pushforward of a uniform
   distribution on a finite set by a bijection of that set is again
   uniform) and the `kappa(U_i)`, `i in R`, remain mutually independent
   (each a fixed deterministic function of a *distinct* independent
   `U_i`) and independent of `kappa o pi` (each `kappa(U_i)` is a
   function of `U_i` alone, and `U_i` was independent of `pi` by
   construction, hence of any function of `pi`). I did not find any
   independence relationship among the primitives that this
   substitution disturbs.

Combining 1 and 2: `f' := kappa o f` satisfies `f' = F(kappa o pi, R,
kappa(U))` (identity 1, valid pathwise) and the input triple on the
right has the same law as `(pi,R,U)` (fact 2), so applying the same
fixed function `F` to equal-in-law inputs gives `f' =d f` — i.e.
`kappa o f =d f`. **Confirmed correct**, with no gap.

### 1.3 Lemma J2 (the swap bijection) — re-derived, VALID, including the two named stress points

**Claim.** Fix `c`, `rho in Sym(c)`, a transposition `(x y)` with
`x,y in c`. Let `kappa := (rho(x) rho(y))` (transposition of `[n]`
swapping the two *values*), `rho' := rho o (x y)`. Then `h -> kappa o h`
bijects `{C(h)=c, h|_c=rho}` onto `{C(h)=c, h|_c=rho'}`, self-inverse.

**My independent check, done before reading the document's own proof
closely, then compared against it.** Two things must be shown for a
fixed `h` in the domain set: (a) `g := kappa o h` has `g|_c = rho'`; (b)
`C(g) = c`.

**(a)** is pure pointwise algebra given `h|_c = rho`, `kappa`'s support
`{rho(x),rho(y)}`: for `z in c \ {x,y}`, `h(z)=rho(z)`, and `rho(z) not
in {rho(x),rho(y)}` by injectivity of `rho` (since `z != x,y`), so
`kappa` fixes it and `g(z)=rho(z)=rho'(z)`; at `z=x`,
`g(x)=kappa(rho(x))=rho(y)=rho'(x)`; at `z=y`, symmetric. Direct
computation, no issue.

**(b), the highest-risk step, re-derived independently rather than
trusted.** Key structural observation, which I verified is exactly what
makes the argument work and is *not* an accident of the specific
construction: `kappa`'s support is `{rho(x),rho(y)} subseteq c`, i.e.
**`kappa` acts as the identity everywhere outside `c`, and maps `c` into
`c`** (this directly answers the dispatch's specific concern — `kappa`
never touches structure outside `c` at all, by construction, so there is
no way for the swap to reach outside `c` and disturb anything there).
Consequences I checked directly:

- For `i not in c`: if `h(i) not in c`, `kappa` fixes it (its support is
  inside `c`), so `g(i)=h(i)`. If `h(i) in c`, then `g(i)=kappa(h(i))`,
  which is again in `c` regardless of which element of `{rho(x),rho(y)}`
  it happens to be (since `kappa` maps `c` to `c`).
- Once an orbit enters `c` (under `h` or under `g`), it never leaves,
  under either map, because both `h|_c=rho` and `g|_c=rho'` are
  bijections `c->c` — this is where the "`f` restricted to `C(f)` is a
  bijection onto itself" fact from §1.1 is used, correctly, on the
  hypothesis side (`C(h)=c` given) and is separately *re-established* on
  the conclusion side (`g|_c=rho'` is shown to be a bijection `c->c` in
  part (a), so `C(g)` inherits the same trapping property automatically
  once we know `c subseteq C(g)`).

I then did the full induction the document's proof only sketches
("tributaries feed in without altering cycle membership"), rather than
taking that phrase on faith:

- **`c subseteq C(g)`:** `g|_c = rho'` is a bijection `c -> c` (shown in
  (a)), hence every `z in c` lies on a genuine cycle of `g` restricted to
  `c` (a permutation of a finite set), so every `z in c` is cyclic for
  `g`. Direct.
- **`C(g) subseteq c`, i.e. no `i not in c` is cyclic for `g`.** Fix
  `i not in c`. Since `C(h)=c` exactly, `i` is not cyclic for `h`; and
  since every forward orbit is eventually periodic on the finite set
  `[n]`, and the *only* cyclic points of `h` are in `c`, `i`'s forward
  `h`-orbit must eventually reach `c` (it cannot cycle forever while
  staying outside `c`, since that would produce a cycle disjoint from
  `c`, contradicting `C(h)=c`). Let `t>=1` be minimal with
  `h^t(i) in c`, and write the pre-entry tail
  `i_0=i, i_1=h(i_0), ..., i_{t-1}=h^{t-1}(i)` (all `not in c` by
  minimality of `t`) followed by `i_t=h^t(i) in c`. **This tail is
  pairwise distinct**, in particular `i_s != i_0` for `1<=s<=t-1`: if it
  ever repeated before reaching `c` it would create a cycle of `h`
  entirely outside `c`, again contradicting `C(h)=c`. Now, for
  `0<=s<=t-2`, `h(i_s)=i_{s+1} not in c`, so (by the bullet point above)
  `g(i_s)=h(i_s)=i_{s+1}` — i.e. **the tail is literally identical for
  `g` and `h`, step for step, up to and including `i_{t-1}`.** At the
  final step, `g(i_{t-1}) = kappa(h(i_{t-1})) = kappa(i_t) in c` (some
  point of `c`, possibly `i_t` itself, possibly its `kappa`-partner —
  either way, in `c`). So `g^t(i) in c`, and thereafter (by the
  trapping property of `g|_c`) `g^s(i) in c` for all `s>=t`, hence
  `g^s(i) != i` for `s>=t` (as `i not in c`). For `1<=s<=t-1`,
  `g^s(i)=i_s != i_0=i` by the pairwise-distinctness just established
  (which transfers to `g` because the tail is identical). So `g^s(i)!=i`
  for **every** `s>=1`: `i` is not cyclic for `g`. Since `i not in c` was
  arbitrary, `C(g) subseteq c`.

Combining, `C(g)=c` exactly. **This closes the highest-risk step
completely** — I found no gap, and in particular no way for `kappa`
(whose support is confined to `c` by construction) to change which
points end up cyclic, matching what the dispatch flagged as the thing to
scrutinize hardest.

**The `|c|=2` edge case, checked explicitly.** With `m=|c|=2`,
`x,y` are forced to be `c`'s only two elements, `rho` is one of the two
elements of `Sym({x,y})`, and `rho'` is the other. `kappa=(rho(x)
rho(y))` is always a genuine transposition of two *distinct* elements of
`[n]` (since `rho` is injective, `x!=y => rho(x)!=rho(y)`), so `kappa`
never degenerates to the identity, and the argument above goes through
verbatim with no special-casing needed. I also checked this case
concretely by hand at `n=2,K=0` (`c=[n]={0,1}`): both permutations of
`[2]` — identity (two fixed points, i.e. `C(pi)={0,1}` realized as two
separate 1-cycles) and the transposition (a single 2-cycle) — satisfy
`C(pi)=c`, each with probability `1/2`, matching Theorem J's `1/2!=1/2`
prediction exactly; this is confirmed again, mechanically, in the
exhaustive run below.

**Involutivity / surjectivity onto the claimed codomain.** `kappa` is a
transposition, `kappa o kappa = id`. Applying the identical argument to
`g` (same `kappa`; note `kappa o rho' = rho` by direct check — the same
swap undoes itself) returns `h` exactly, and the roles of `rho,rho'` are
symmetric in the construction (nothing above privileged which was
"first"), so the map is a bijection both ways, not just an injection one
way. Confirmed.

**Conclusion of my own re-derivation:** Lemma J1 and Lemma J2 are both
correct as stated, with no residual issue at the specific stress points
named in the dispatch (the `|c|=2` case; `kappa` acting on anything
outside `c`; the swap silently changing which points are cyclic). The
assembly in ATTEMPT.md §2.2 (using Lemma J1 with `kappa` from Lemma J2 to
get `P(f in A_rho)=P(f in A_{rho'})`, then chaining over a generating set
of transpositions of `Sym(c)` to get all `P(A_rho)` equal, hence each
`=P(C(f)=c)/m!`) is standard and correct given the two lemmas; I checked
the specific algebraic step
`P(f in A_{rho'}) = P(kappa f in A_{rho'}) = P(f in kappa^{-1}(A_{rho'}))
= P(f in A_rho)` line by line and found no gap (the middle equality is a
plain preimage identity for the deterministic map `h -> kappa o h`; the
last equality is exactly Lemma J2's bijection statement, using that
`kappa` is an involution so `kappa^{-1}(A_{rho'})=A_rho` as *sets of
functions*).

### 1.4 The Corollary — re-derived, VALID

`P(i,j \text{ same cycle} \mid C(f)=c) = 1/2` for every realized `c` with
`i,j in c`, `|c|>=2`, by Theorem J (uniform restriction) plus the
classical fact (independently re-verified below, not merely cited). This
holds for *every* such `c` regardless of `|c|`, so averaging over the
random realized `c` (a mixture of `1/2`'s) gives `1/2` unconditionally —
this is the correct and only nontrivial step, and it is trivial once
Theorem J is granted. No issue found.

### 1.5 One cosmetic issue (does not affect soundness)

ATTEMPT.md §2.2 writes "transpositions `(0 1),(0 2),...` (any generating
set... indexed by a fixed reference element)" as if invoking a
*specific* minimal generating set, then separately invokes "any
`rho in Sym(c)` is reachable from any fixed `rho_0` by a finite chain of
such steps" — but Lemma J2 itself is proved for an *arbitrary*
transposition `(x y)` of `c`, not merely the reference-indexed
generating set. The chain argument therefore works using *any*
sequence of transpositions decomposing `rho` (not only the named
generating set), which is in fact the easier and more standard fact.
This is purely an expository imprecision — naming a specific generating
set that is then not actually needed, rather than just invoking "every
permutation is a product of transpositions" directly — and does not
weaken the proof; I note it only because the dispatch asked for
cosmetic issues to be named, not inflated.

### 1.6 Assessment of the disclosed §7.1 false start

Not under review as a claim (it is explicitly disclosed as a rejected
attempt, not something the document relies on), but I checked it for
internal consistency since a referee should not wave through a
self-report uncritically. The failure mode described — freezing `h`
outside `c` and only swapping `h|_c` from `rho` to `rho'` can make two
distinct non-rerouted domain points (one inside `c`, one outside) map to
the same image, which is impossible under any actual `pi in Sym(n)`
restricted to `[n]\R` (injective there) — is a genuine, correctly
diagnosed failure mode, consistent with my own understanding of the
model (§1.1 above: only `pi`'s restriction to `[n]\R` is a
*permutation-derived* injection; nothing about that restriction is
preserved by an arbitrary local relabeling of `c`'s images alone). The
diagnosis is accurate and the fix genuinely addresses it (post-composing
the *entire* map by `kappa`, which is injective, preserves injectivity
of the composite on `[n]\R` automatically, with no case analysis). No
issue with this disclosure.

---

## 2. Independent computational verification

All code in this directory (`adversarial/`) was written from scratch,
from the prose of Definition 4 and Theorem J/Corollary alone. **No
script from `joint_two_point_attempt/` (`finite_n_exact_enum.py`,
`uniform_cyclic_restriction_exact.py`, `symbolic_checks.py`,
`poisson_continuum_same_diff_mc.py`) was opened, read, or imported at any
point**, per mandate. Where a specific numeric value happened to
coincide with a value quoted in ATTEMPT.md's prose (e.g. `n=6,K=2`,
`P_both=44/135`), that is noted below as an independent confirmation —
comparing two independently-computed final numbers is not code reuse.

### 2.1 Classical fact `P(i,j\text{ same cycle})=1/2` (`classical_same_cycle_check.py`)

Exhaustive enumeration of all `m!` permutations of `range(m)` via
`itertools.permutations`, a from-scratch cycle-labeling routine, exact
`Fraction` arithmetic. Extended one step past the front's own range
(`m=2..7`) to **`m=2..9`**, plus an extra independent cross-check that
the `1/2` fact holds for *every* pair `(i,j)`, not only `(0,1)`, at
`m=4,5,6`.

**Result: exactly `1/2` at every `m=2,...,9`, and for every pair at
`m=4,5,6` (`C(4,2)=6`, `C(5,2)=10`, `C(6,2)=15` pairs checked, all
exact). Zero violations.** See `classical_same_cycle_check.log`.

### 2.2 Definition 4 exhaustive enumeration (`def4_exhaustive_check.py`)

**Method.** Rather than looping over all `n!` permutations directly (of
which only the restriction `pi|_{[n]\R}` matters for `f`), the
enumeration loops over: all `C(n,K)` choices of `R`; all injections
`sigma: [n]\R -> [n]` (via `itertools.permutations(range(n), n-K)`,
which enumerates exactly the injections, in bijection with ordered
tuples of distinct images); all `n^K` tuples of destinations `U` for
`R`'s elements — and weights each resulting configuration by the exact
integer `K!` (the number of permutations `pi in Sym(n)` extending a
given injection `pi|_{[n]\R}=sigma`, a standard "injections extend to
bijections" count). This is an **exact reweighting**, verified (not
merely asserted) by an internal sanity check computed independently
inside the same script: the total weighted count is checked, for every
single cell, to equal `n! * C(n,K) * n^K` exactly (the true size of the
`(pi,R,U)` sample space) — this passed at all 33 cells run (see below),
which is itself a nontrivial check that the reweighting device has no
off-by-one or double-counting bug.

Two independent checks per cell, both from a from-scratch `O(n)`
path-marking cyclic-point/cycle-id algorithm (not the front's):

(a) **Restriction-uniformity** (Theorem J): for every realized `c` with
`|c|>=2`, are all `m!` bijections of `Sym(c)` realized with **exactly**
equal weighted count?
(b) **Same/diff split** (Corollary): exact weighted tally of
`P_both, P_same, P_diff` for the fixed pair `(0,1)`.

**Coverage, deliberately going beyond the front's own grid
(`n=3..7, K=1..5` per its own §4.1 table — which has no `K=0` row, see
below — self-reported by ATTEMPT.md §4.1 as 21 cells total):**

| `K` | `n` range tested here | vs. front |
|---|---|---|
| 0 | 2–8 | **new** — front's own Sec 4.1 table has no `K=0` row at all |
| 1 | 3–8 | front: 3–7; extended by one |
| 2 | 3–7 | reproduces front's range in full, independently |
| 3 | 3–7 | front: 3–6; extended by one |
| 4 | 4–7 | front: 4–6 (incl. `K=n=4`); extended by one |
| 5 | 5–7 | front: 5–6 (incl. `K=n=5`); extended by one |
| 6 | 6–7 | **new K value entirely**, including the `K=n=6` boundary |
| 7 | 7 | **new**, the `K=n=7` boundary |

**33 `(n,K)` cells total** (vs. the front's 21), including four cells
never tested by the front at all (all `K=0` rows, and the entire `K=6,7`
lines), and one-step extensions in `n` for every other `K` the front
tested.

**Result (full log: `def4_exhaustive_check.log`): all 33 `(n,K)` cells
listed in the table above passed on all three axes:**

```
Cells run: 33
Weight-sanity checks passed: 33/33
Corollary (same=diff=half) checks passed: 33/33
Theorem J restriction-uniformity checks passed: 33/33

OVERALL RESULT: ZERO VIOLATIONS across all cells.
```

This includes the new `K=0` line (`n=2..8`, 7 cells, not tested by the
front at all), the new `K=6` line (`n=6,7`, including the `K=n=6`
boundary), the new `K=7` cell (`n=7`, the `K=n=7` boundary — one step
past the front's highest-tested boundary `K=n=5`), and one-step
`n`-extensions for `K=1,2,3,4,5` beyond the front's own range. Every
single realized cyclic set `c` across all 33 checked cells (aggregate:
well over a thousand distinct `c`'s, see the per-cell "`c`'s checked"
counts in the log, e.g. 247 distinct realized `c`'s at `n=8,K=1` alone)
had **all** `|c|!` bijections realized with **exactly** equal weighted
count — no exceptions.

Independent cross-check against a number quoted in ATTEMPT.md's own
prose (§4.2, not code): at `n=6,K=2` this script independently computed
`P_both = 44/135` — **identical** to the value ATTEMPT.md quotes as
having been cross-checked against the (unread, per mandate) prior
script. This is a genuine independent confirmation from a completely
separate implementation.

### 2.3 Redundant naive cross-check of the enumeration method itself (`def4_naive_crosscheck.py`)

`def4_exhaustive_check.py`'s main efficiency device — enumerating
injections `[n]\R -> [n]` weighted by `K!` instead of looping over all
`n!` permutations directly — is itself a place a subtle bug could hide
(an off-by-one in the weight, or a mis-indexed `R`/`D` correspondence,
could silently distort every ratio while still passing the internal
`weight_ok` total-count sanity check, if the distortion happened to
preserve the total but not the per-configuration correctness). To rule
this out, `def4_naive_crosscheck.py` re-implements the **exact same
computation with zero shortcuts**: it loops over literally all `n!`
permutations via `itertools.permutations(range(n))` directly, all
`C(n,K)` subsets, and all `n^K` destination tuples, with no reweighting
at all — structurally the simplest, most obviously-correct (if slowest)
possible implementation. Run at 12 small-to-medium cells including both
members of the suspicious coincidence noted during review (`n=4,K=3` and
`n=4,K=4` both independently returned `P_both=19/64` in the main run —
flagged as worth double-checking rather than dismissed as an obvious
coincidence, since a systematic weighting bug could in principle produce
matching-but-wrong numbers across adjacent `K`).

**Result: every single value (`P_both`, `P_same`, `P_diff`) from the
naive method matches the optimized method's output exactly, at all 12
cross-checked cells — including confirming `n=4,K=3` and `n=4,K=4`
genuinely both equal `19/64` (a real coincidence of the small-`n=4`
sample space, not a bug in either implementation).** See
`def4_naive_crosscheck.log`. This gives full confidence that the
injection-weighting speedup used for the larger cells in §2.2 is exact,
not merely internally self-consistent.

---

## 3. Referee-side bugs and false starts (full disclosure)

Per this archive's disclosure culture, every mistake made while
producing this report is recorded here, not hidden, regardless of
whether it affected the final numbers.

1. **Duplicate concurrent process on the main exhaustive run (caught,
   fixed, re-run clean).** The first launch attempt used a manual
   `nohup ... &` inside a single Bash call meant to background the job;
   the shell wrapper reported "Exit code 1" and the immediate `tail`
   failed to find the log file, which looked like a failed launch — but
   the `nohup`'d process had in fact started successfully and kept
   running undetected. A second, correct launch (via the tool's
   `run_in_background` mechanism) was then started on the **same**
   output file with a truncating `>` redirect, so for a window of time
   **two independent instances of `def4_exhaustive_check.py` were
   simultaneously appending/truncating the same log file**, which could
   have silently corrupted or interleaved the results (or truncated
   away already-computed cells) without raising any error. This was
   caught by checking `ps aux` before trusting the log, both processes
   were killed (`kill -9`), the log file was deleted, and the run was
   restarted as a single clean process, confirmed via `ps aux` to be the
   only instance before letting it run to completion. **No corrupted or
   duplicated data ever made it into the final `def4_exhaustive_check.log`**
   used for this report — the file analyzed above is from the single
   clean re-run — but the near-miss is disclosed since it could easily
   have produced silently-wrong numbers if not caught.
2. **No arithmetic, logic, or mathematical bugs were found** in either
   of my own scripts (`classical_same_cycle_check.py`,
   `def4_exhaustive_check.py`, `def4_naive_crosscheck.py`) after the
   process issue above was resolved — the three-way agreement between
   (a) the optimized enumeration's internal weight-sanity check passing
   at every cell, (b) the fully independent naive brute-force
   cross-check matching the optimized method exactly at all 12 tested
   cells, and (c) one value (`n=6,K=2`, `P_both=44/135`) matching a
   number independently quoted in ATTEMPT.md's own prose, gives strong
   triangulated confidence that no silent counting bug survived into the
   results reported in §2.

---

## 4. Scorecard

| Item | Status |
|---|---|
| Lemma J1 (post-composition invariance), re-derived independently | **VALID** |
| Lemma J2 (swap bijection), re-derived independently, incl. `\|c\|=2` and "does `kappa` reach outside `c`" stress points | **VALID** |
| Theorem J (uniform restriction over `Sym(c)`, all `n,K`) | **VALID** |
| Corollary (exact 50/50 split given both cyclic, all `n,K`) | **VALID** |
| Classical fact `P(\text{same cycle})=1/2`, independent re-derivation, `m=2..9` (+ all-pairs cross-check `m=4,5,6`) | **CONFIRMED, zero violations** |
| Exhaustive Definition-4 enumeration, 33 `(n,K)` cells (vs. front's 21), incl. cells the front never tested (`K=0`, `K=6`, `K=7`) | **CONFIRMED, zero violations** — 33/33 weight-sanity, 33/33 corollary, 33/33 Theorem J restriction-uniformity |
| Redundant naive (no-shortcut) cross-check of the enumeration method, 12 cells | **CONFIRMED exact match**, incl. the `n=4,K=3`/`K=4` coincidence |
| Cosmetic issue: §2.2's "reference-indexed generating set" framing is unused overhead, not a gap | named, does not affect soundness |
| §7.1's self-disclosed false start | independently checked, diagnosis and fix both accurate |
| Referee-side bugs | one process-management near-miss (duplicate concurrent run), caught before any bad data was used; no math/logic bugs found — see §3 |

**Net verdict: SOUND. ACCEPT for catalogue** as Theorem J / Corollary,
PROVED, elementary, self-contained, at the tier ATTEMPT.md claims. No
mathematical error found in the target document's Theorem J, its
Corollary, or the two lemmas underlying them.
