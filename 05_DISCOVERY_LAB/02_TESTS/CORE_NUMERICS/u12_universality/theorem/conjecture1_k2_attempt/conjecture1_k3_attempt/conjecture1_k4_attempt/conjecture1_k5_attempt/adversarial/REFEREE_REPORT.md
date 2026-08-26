# Adversarial referee report — `conjecture1_k5_attempt/ATTEMPT.md` (REINFORCED review)

> **Mandate.** Wave 17, front (a), `CONJECTURE-1-K5-GENERAL-ATTEMPT`
> (`DISC-DEC-072`). This front claims not only the mandated `K=5` instance
> of `THEOREM.md` §8 Conjecture 1 but a **general-`K` closure** of the whole
> conjecture, plus Conjecture 2 as a corollary — the largest single result
> claimed anywhere in this archive's `U₁/₂` line so far. Explicit brief:
> **hunt for the flaw that would explain the jump** from four separate
> per-`K` closures (`K=1..4`) to one uniform argument covering every `K`.
> Do not accept the surprise; try to break it.

> **Prior stalled attempt.** A different background instance began this same
> review earlier and left four partial scratch files in this directory
> (`ref_symbolic_lemma1.py/.log`, `ref_forest_identity.py/.log`,
> `ref_classify.py/.log`, `ref_assembly_symbolic.py/.log`) with no
> `REFEREE_REPORT.md`. Per the independence discipline, **none of those
> four `.py` files was opened, read, or imported** at any point in this
> review (they are a prior referee's own scripts). Their `.log` files were
> read once, purely as an orientation sanity-check before writing any code
> of my own, and every computation they report was **independently redone
> from scratch** below (fresh code, fresh reasoning) rather than trusted —
> see §0. The stalled attempt's own `ref_assembly_symbolic.log` cuts off
> mid-computation on an unresolved `sympy` hypergeometric expression from a
> symbolic-`K` `Sum(...).doit()` call — this is almost certainly *why* that
> session stalled, and this review deliberately avoids that exact pattern
> (see §4).

---

## Verdict

> **SOUND — ACCEPT for catalogue.**
>
> **The general-`K` claim survives at its claimed tier: PROVED for every
> `K≥1`, modulo the single classical `PD(1)` size-biased/residual citation
> (McCloskey 1965; Patil–Taillie 1977; Pitman 2002 Ch. 3) — the same
> citation the whole `K=1..4` line already uses, here applied recursively
> up to `K-1` times for each fixed `K` (never an unbounded or infinite
> application at any single `K`).**
>
> **Conjecture 2 (§4.6) also survives at the same tier: it follows as an
> exact corollary of the general-`K` theorem via the Poisson mixture
> algebra, which I re-derived by hand and confirms exactly (§8 below); its
> only additional ingredients are `THEOREM.md` §5.1's already-cited
> conditioning fact and countable additivity, neither of which this
> document strains.**
>
> After an intentionally hostile, from-scratch reconstruction of every
> major joint — the residual-independence claim underlying the telescoping
> peel (attacked hardest, per the brief), Lemma 1a for general block size,
> the generic algebraic telescoping (proved once, for *every* pattern of
> *every* `K` at once, not spot-checked at `K=5`), the node-chain mechanism
> argument, the Prüfer/weighted-forest proof of Lemma 3, the coarea/slice
> assembly and its binomial-theorem closure, and the Conjecture-2 mixture —
> **no mathematical error was found anywhere in the document.** Four bugs
> were found and fixed, but all four were in *this review's own* fresh
> verification code (see §0), not in the target document; every one, once
> fixed, reproduced the document's claims exactly. No new issue beyond the
> document's own self-disclosed §6 items is named.

---

## 0. Independence discipline and this review's own bugs (disclosed in the open)

No `.py` file of the front (`derive_lemma1_general_symbolic.py`,
`enumerate_destination_combinatorics_k5.py`, `forest_identity_check.py`,
`derive_assembly_k5_symbolic.py`, `mechanism_check_k5.py`, any `mc_*.py`) or
of the prior stalled referee attempt was read at any point. `grep -rn
"20260861"` was run before any code (`05_DISCOVERY_LAB/00_GOVERNANCE` and the
`u12_universality/theorem` subtree) and found only the ledger/queue
reservation line plus one seed (`20260861040`) already used by the stalled
attempt's own `ref_symbolic_lemma1.py` (identified via `grep`, not by reading
that file) — this review's own seeds start at `20260861100` to avoid
collision (see Seeds table).

Every derivation in this report was built from the *prose* of `ATTEMPT.md`,
`DERIVATION_PREREG.md`, `THEOREM.md` §5.1/§5.3/§8/Estágios 15/17/20, and the
`K=2,3,4` lineage `ATTEMPT.md`/`REFEREE_REPORT.md` prose — all read in full
before any code was written.

**Four bugs were caught in this review's own fresh code while building the
checks below — all disclosed here, all in this reviewer's code, none in the
target document:**

1. `ref2_symbolic_core.py` Part 1 (moment cross-check of Lemma 1a): a wrong
   nested-integration order (integrating the ordering-chain variables from
   outermost to innermost instead of innermost to outermost) initially left
   un-integrated symbols in the result. Fixed by reversing the loop order.
2. Same script, same Part: after fixing (1), the *reference* Dirichlet
   second-moment formula I compared against was itself wrong (used
   `2/(b+1)!` instead of the correct `2(b-1)!/(b+1)! = 2/(b(b+1))` for
   `E[X_i^2]` under `Dirichlet(1,...,1)` with `b` parts). Fixed; both bugs
   were in the comparison scaffolding, not the underlying nested-integral
   computation, which was correct throughout.
3. `ref2_mechanism_mc.py`: the predicted-mass formula summed `D_i+1` over
   every `i` whose *target* region `g(i)` was on-cycle, instead of over
   every `i` that was *itself* on-cycle (`i∈cyc(g)`, as the document's own
   prose states). Since an off-cycle node can legitimately target an
   on-cycle region, this double/mis-attributed mass and produced
   mismatches on ~30% of trials in a smoke test. Fixed by conditioning on
   `on_cycle[i]` (the summation index), not `on_cycle[g[i]]` (its target) —
   traced by hand against one concrete failing trial (§ below) before the
   fix, confirming the corrected formula reproduces ground truth exactly.
4. `ref2_recipe_mc.py`: an initial sign error dropped the `1 - Σm_i`
   (OUT-mass) term from the Lemma-2 formula entirely (`M = 1 - Q_off -
   OUT - ΣP` instead of the correct `M = OUT + Σ_{on-cycle}(m_j-P_j)`),
   giving a mean of `~0.20` against a target of `0.369`. Fixed by rebuilding
   the formula directly from the document's own stated form,
   `M=(1-Σm_i)+Σ_{j∈C}(m_j-P_j)`.

All four are ordinary implementation bugs of the kind any fresh
re-implementation risks, caught by the same discipline this whole lineage
uses (pre-declared acceptance criteria catching wrong numbers immediately);
none survive into any result below.

---

## 1. Lemma 1 general-`K` — the residual-independence claim, attacked hardest (per the brief)

This is the crux joint named in the dispatch as the single most likely place
for "a subtle conditional-independence error" to hide, so it gets the most
scrutiny, done by hand *before* any code was written (the derivation below is
mine, built independently of the document's own §2.2 exposition, then
cross-checked against it only after being derived).

**Re-derivation.** Peel co-blocks in a fixed order (any order determined
solely by the pattern `π`, e.g. "least unplaced index" — this is a
deterministic function of `π`, revealed no new randomness). At peel `j`,
given peels `1..j-1` (revealing block memberships **and** lengths
`ℓ_1,...,ℓ_{j-1}`):

- The **anchor** `a_j` is one specific *not-yet-conditioned-on* source
  (its identity is fixed by `π`, but its *position* has not yet been used
  for any conditioning). Since all `K` sources are i.i.d. `Unif(0,1)`
  independent of the whole `PD(1)` partition, `a_j`'s position, conditioned
  only on "avoids `B_1∪...∪B_{j-1}`" (a measurable event about *position*,
  not about the fine structure of the residual), is `Unif` on the residual
  set **and independent of the residual partition's own realization** —
  this needs no citation beyond "conditioning an independent uniform mark
  on a measurable landing set gives a uniform mark on that set, regardless
  of what structure lives on that set."
- The **residual partition** (rescaled by `1/(1-s_{j-1})`) being a *fresh*
  `PD(1)`, **independent of `ℓ_1,...,ℓ_{j-1}` jointly** (not merely of the
  qualitative pattern revealed so far) is exactly the classical multi-step
  GEM(1)/stick-breaking representation: `ℓ_j = V_j·∏_{i<j}(1-V_i)` with
  `V_1,V_2,...` i.i.d. `Unif(0,1)`, so the residual after `j-1` peels is by
  construction independent of `V_1,...,V_{j-1}` — and hence of
  `ℓ_1,...,ℓ_{j-1}`, which are deterministic functions of those `V`'s. This
  is the textbook property the citation names (McCloskey 1965;
  Patil–Taillie 1977; Pitman 2002 Ch. 3, GEM(1) as iterated size-biased
  deletion) — no extrapolation is needed to get *joint*, not merely
  *marginal*, independence from `ℓ_1,...,ℓ_{j-1}`: it is definitional to
  the stick-breaking construction.
- Given the residual partition (independent of history) and `a_j` uniform
  on it (independent of history and of the residual partition), `a_j`'s
  block is a genuine size-biased pick from a fresh `PD(1)`, so `ℓ_j/(1-s_{j-1})
  ~Unif(0,1)` **independent of `ℓ_1,...,ℓ_{j-1}`** — this is precisely `V_j`.
- The other `K-c_{j-1}-1` unplaced sources are i.i.d. `Unif` on the *whole*
  `[0,1]`, conditioned to avoid `B_1..B_{j-1}` — so, independently of
  everything peeled so far, each lands in the (now-known-size) block `B_j`
  with the **absolute** probability `ℓ_j/(1-s_{j-1})` — not a rescaled or
  doubly-conditioned probability. (This absolute-vs-rescaled distinction is
  exactly the point the `K=4` document's own Route-B bug tripped over —
  see §7 below; the general-`K` document's §2.2 states the absolute form
  correctly throughout, and I independently re-derive it the same way.)

**Exponent bookkeeping and telescoping.** Multiplying the four factors per
peel (anchor density, membership, non-membership, Lemma-1a gap density)
gives peel-`j`'s contribution `(b_j-1)!·(1-s_j)^{K-c_j}/(1-s_{j-1})^{K-c_{j-1}}`
— I re-derived this by hand from the bullets above (not copied from the
document) and it matches exactly. The product over `j=1..R` telescopes
because the exponent on `R_{j-1}` appearing as peel `j`'s denominator is
*identical* to the exponent on `R_{j-1}` appearing as peel `(j-1)`'s
numerator — a purely algebraic fact, verified symbolically for **generic**
block-size sequences `(b_1,...,b_r)` (not just `K=5`'s 52 patterns) in
`ref2_symbolic_core.py` Part 3, which therefore certifies the telescoping
for *every* co-block pattern of *every* `K` at once, since the derivation
above never referenced which specific labels occupy which block (only block
*sizes*, by exchangeability of the i.i.d. sources).

**Conclusion.** I find no flaw in the residual-independence claim, including
in its strongest form (independence from the full *sequence* of revealed
lengths, not just the pattern) — it is a correct, if carefully-stated,
unpacking of the standard GEM(1) stick-breaking representation with `K`
i.i.d. uniform marks attached, applied recursively a finite (`≤K-1`) number
of times for each fixed `K`. This is the same conclusion both the `K=3` and
`K=4` referees reached for their own (weaker, `≤2` and `≤3` peels)
instances, now confirmed to extend cleanly to the general recursive case.

**Numerical/symbolic checks (all fresh):**

| Check | Script | Result |
|---|---|---|
| Lemma 1a, general `b=2..6`, unit-Jacobian ordering-cell derivation | `ref2_symbolic_core.py` Part 1 | PASS (all `(b-1)!` cells unimodular) |
| Lemma 1a moment cross-route (`b=2,3,4`, independent Bayes-style nested integration vs Dirichlet formula) | same, Part 1 | PASS (after fixing this review's own 2 bugs, §0) |
| `Σ_{partitions}∏(b_j-1)!=K!` bijection, `K=1..9` | same, Part 2 | PASS (exhaustive enumeration of set partitions) |
| Generic algebraic telescoping (covers every pattern of every `K`) | same, Part 3 | PASS |
| `K=5` all-same (`b=5`) pattern, literal peel-product evaluation | same, Part 4 | PASS (density `=24`, `ℓ_1`-independent) |
| `K=5` all-different (`1^5`, 4 recursive peels) pattern | same, Part 4 | PASS |
| Lemma 1 discrete-permutation MC, `K=5`, 3 scales, own independent `region_sizes` routine (distinct from the mechanism-check's `region_assign`) | `ref2_lemma1_mc.py` | see §6 below |

## 2. Lemma 1a — labeled circular spacings, general `b`

Re-proved independently for `b=2..6` via the identical geometric idea stated
in `ATTEMPT.md` §2.1 (anchor at `0`, `(b-1)!` ordering cells, each a
unit-Jacobian bijection onto the full open simplex) but implemented from
scratch with `sympy`'s own `Matrix.jacobian`, not the document's code
(`ref2_symbolic_core.py` Part 1). All Jacobians confirmed `=1` for every
ordering, `b=2..6`. Cross-checked by an independently-derived exact
second-moment formula for the labeled-gap law (`E[G_i^2]=2L^2/(b(b+1))`,
matching `Beta(1,b-1)` scaled by `L`) via direct nested integration over the
free points — a genuinely different route from the ordering-cell bijection,
confirmed to agree for `b=2,3,4`.

I also checked the labeling direction (arcs *ending at* each source, flow
direction) is used consistently between Lemma 1a's own statement and §1's
region definition ("the `b` arcs ending (in flow direction) at the
respective sources") — the two match verbatim; no orientation mismatch
found.

## 3. §2.2/§2.3 — the telescoping peel and the partition→permutation sum

Covered above (§1) for the residual-independence content. The partition↔
(set-partition + per-block cyclic order)↔permutation bijection giving
`Σ∏(b_j-1)!=K!` was independently re-verified by direct enumeration of all
set partitions (not by trusting the bijection abstractly) for `K=1..9`
(`ref2_symbolic_core.py` Part 2) — `1,2,6,24,120,720,5040,40320,362880`, all
exact matches to `K!`. At `K=5`: the pre-registered per-shape breakdown
(`24+30+20+20+15+10+1=120`, multiplicities `1,5,10,10,15,10,1` by partition
type) is consistent with my own enumeration (52 set partitions of `{1..5}`,
grouped by block-size multiset, exactly matches the stated table).

## 4. Assembly of the closed form — hand re-derivation avoiding the sympy trap that stalled the prior attempt

I re-derived the per-`r` closed form **by hand**, independently of the
document's own §4.2 exposition, via the substitution `Q=(1-x)v` in the
`Q`-integral and the two Beta-function evaluations `B(n,r)` and
`B(n+1,r)` (algebra reproduced in full in this report's companion script's
docstring and comments). The result:

```
f_r(x) = C(K,r) x^r (1-x)^{K-1} [K - (K-r)(1-x)]
```

matches `ATTEMPT.md`'s unified closed form **exactly**. I verified this
hand derivation exactly (`sympy.Rational`, no floats) for every `K=1..8,
r=0..K` (`ref2_symbolic_core.py` Part 6) by directly integrating the
`Q`-integral for `1≤r≤K-1` and checking the `r=0,K` edge cases separately —
**deliberately avoiding `sympy.Sum(...).doit()` over a symbolic `K`**, which
is exactly the operation whose `Piecewise`/hypergeometric output the target
document's own §6 item 1 self-diagnoses as a check-harness artifact, and
which is *also*, on inspection of its `.log` file only, where the prior
stalled referee attempt's own `ref_assembly_symbolic.py` appears to have
hung (its log cuts off mid "PART 2: symbolic-(K,r) Beta route" with an
unresolved `hyper(...)` expression and no PASS/FAIL line — consistent with a
slow/hanging `sympy.simplify` on a hypergeometric term, though I did not run
that script myself to confirm, per the independence discipline). This
review's Part 6/7 gets the same mathematical content (closed form valid for
symbolic `K`, binomial sum closes for every `K`) by evaluating at **concrete
integer `K` up to 15** plus a hand proof (not `sympy`) that the underlying
identity is just the ordinary binomial theorem — which cannot stall, and
does not need to: the binomial-theorem step
(`Σ(K-r)C(K,r)x^r=K(1+x)^{K-1}` via `C(K,r)(K-r)=K·C(K-1,r)`) is elementary
and requires no symbolic-`K` machinery to trust.

**Binomial-theorem closure**, `Σ_r f_r(x) = 2Kx(1-x^2)^{K-1}`: verified
exactly for `K=1..15` (`ref2_symbolic_core.py` Part 7). **Reductions to
`K=1,2,3,4`**: the unified formula evaluated at those `K` reproduces every
published, already-adversarially-reviewed group polynomial from the lineage
**exactly**, built on this script's own `sympy` symbol (never
`sympify`-from-string, avoiding the `K=4` document's own disclosed pitfall)
— `ref2_symbolic_core.py` Part 8. The `K=5` explicit instance (§4.4 of
`ATTEMPT.md`) matches exactly, all six groups.

**Exact probabilities and moments**, `K=5` and `K=6` (a `K` the front itself
never symbolically assembled a full closed form for, though it did classify
and forest-check `K=6`): computed exactly via `sympy.Rational` integration
of this review's own independently-derived `f_r` (Part 9). `K=5`:
`P(r=0..5)=1/6,5/14,25/84,5/36,1/28,1/252` (exact match to `ATTEMPT.md`'s
registered table), `E[M_5]=256/693`, `E[M_5^2]=1/6`, `E[M_5^3]=256/3003` —
all exact matches. `K=6`: `E[M_6^2]=1/7` (matching the general
`E[M_K^2]=1/(K+1)` claim at a `K` beyond the front's own exhaustive range).

## 5. Lemma 2 (mechanism formula) and Lemma 3 (weighted-forest identity)

**Lemma 2.** The node-chain argument was re-read and re-derived by hand.
Its key improvement over the `K=3`/`K=4` lineage's own exposition — working
at the *node* level ("does the sequence `k,g(k),g²(k),...` ever return to
`k`?") rather than the *arc/point* level — genuinely does subsume the
"redirect landing inside an already-periodic arc" sub-case those referees
had to trace by hand: an off-cycle node's own forward node-sequence either
hits OUT (drains forever) or becomes eventually periodic with its periodic
part necessarily a cycle of `g` not containing `k` (since `k∉C`), so
`g^t(k)≠k` for all `t≥1` regardless of *where within a cycle's territory*
the chain merges — the point-level sub-case simply never has to be
mentioned. I confirm this is a genuine simplification, not merely a
relabeling of the old argument, and that it is correct. **On-cycle regions**
contribute exactly their tail arc `[P_j,m_j]` by the standard
"periodic-re-entry-lands-at-a-fixed-offset" argument, unchanged in substance
from `K=2..4`.

**Lemma 3 (Prüfer/weighted-forest identity), `W(n)=e(e+Q)^{n-1}`.** Re-proved
by hand: acyclic maps `[n]→[n]∪{ext}` biject with labeled trees on `n+1`
vertices rooted at `ext`; a map's weight is `w_0·∏_v w_v^{deg_T(v)-1}`; the
Prüfer bijection turns the sum over trees into `(Σw_v)^{n-1}`, giving
`W(n)=w_0(Σw)^{n-1}`. Independently verified as an **exact polynomial
identity** — not a numeric spot-check — by literal brute-force enumeration
of **every** acyclic map for `n=1..7` (`8^7≈2.1M` maps at `n=7`, using an
`O(n)`-per-map pointer-chasing cyclic-detector, not `sympy`, to stay fast
and avoid any stall risk) against an exact multinomial-coefficient
expansion of `e(e+Q)^{n-1}`, both built as exact-integer monomial→count
dictionaries (`ref2_symbolic_core.py` Part 5). All 7 values of `n` match
exactly, including `n=7` — one step beyond both the front's own range
(`n=1..6`) and the stalled prior attempt's own range (`n=1..7`, matching).

## 6. Discrete mechanism check — from-scratch orbit tracer, `K=5`

Built entirely independently (`ref2_mechanism_mc.py`): a genuine uniform
random permutation of `[n]`, 5 distinct source labels, i.i.d.
with-replacement destinations (collisions/fixed points allowed), a generic
functional-graph cyclic-node oracle (no knowledge of the `K=5` mechanism —
it would find the true cyclic set of *any* finite function), and an
independently-implemented `region_assign`/predicted-mass routine built from
the document's prose description of `M_pred = #OUT + Σ_{i∈cyc(g)}(D_i+1)`.

```
n= 25  trials=200000  seed=20260861100: mismatches=0  cells_hit=7776/7776
n=150  trials= 60000  seed=20260861101: mismatches=0  cells_hit=7776/7776
n= 12  trials= 40000  seed=20260861102: mismatches=0  cells_hit=7776/7776
TOTAL: 0 mismatches / 300,000 trials, full 7776/7776 cell coverage at EVERY scale
wall time: 31.1s
```

This exceeds the brief's target (`≥200k` trials, all 7776 cells if
feasible) — every one of the three scales independently achieves full raw
cell coverage (the front's own check achieved full coverage only at its
`n=25` scale), and includes an `n=12` collision/fixed-point-saturated scale
(62% collision trials, 35% fixed-point trials) as an edge-case stress test.
**Zero mismatches.**

## 7. `K=6` beyond-target verification (the general-`K` claim tested at a `K` never exhaustively covered by the front)

**Fresh exhaustive classification**, `7^6=117649` raw maps
(`ref2_classify.py`): per-`r` raw counts `16807,28812,30870,23520,12600,
4320,720` (sum `117649`), **30** shape types (`=Σ_{s≤6}p(s)`), `N(r,n_off)`
values `16807,4802,1029,196,35,6,1` — all exactly matching the
labeled-forest count `(r+1)(r+1+n_off)^{n_off-1}`, and cross-footing
exactly to `117649`. (`K=5`'s own classification, `6^5=7776`, was also
independently reproduced in the same script: per-`r` counts
`1296,2160,2160,1440,600,120`, **19** shape types, `N` values
`1296,432,108,24,5,1` — exact matches to `ATTEMPT.md`'s pre-registered
table.)

**Fresh continuum recipe MC**, `K=6` against `12x(1-x^2)^5` — a check the
front itself never ran (it only symbolically classified and forest-checked
`K=6`, never a recipe MC there) — plus `K=5` against `10x(1-x^2)^4`
(`ref2_recipe_mc.py`, `N=1.5M` for `K=5`, `N=800k` for `K=6`, own
independently-implemented on-cycle detector, distinct from both
`ref2_mechanism_mc.py` and `ref2_classify.py`):

```
K=5 (N=1,500,000, seed=20260861120):
  overall KS D=0.00087 p=0.2098   mean=0.369251+/-0.000142 vs 0.369408 (z=-1.11)
  6/6 group fractions |z|<1.3;  6/6 per-group KS pass (worst p=0.030, unremarkable across 12 tests)

K=6 (N=800,000, seed=20260861121, BEYOND the front's own recipe-MC scope):
  overall KS D=0.00089 p=0.5504   mean=0.341035+/-0.000182 vs 0.340992 (z=+0.24)
  7/7 group fractions |z|<2.2;  7/7 per-group KS pass
```

The general-`K` claim survives a genuine test at `K=6`, a value the front
never recipe-MC-verified at all.

**Sub-shape (`σ`) independence — a clean structural argument, not just a
statistical test.** §4.1's claim that the joint density for fixed `(C,σ)`
is independent of the specific permutation `σ` is, on inspection, not
merely a numerically-confirmed coincidence: for each `i∈C`, the event
"`u_i` lands in region `σ(i)`" has probability exactly `m_{σ(i)}`, and
since `σ` is a bijection of `C` onto itself, `∏_{i∈C} m_{σ(i)} = ∏_{j∈C}
m_j` **identically**, regardless of which specific permutation `σ` is. The
`σ`-independence is therefore immediate from the bijection property alone,
before any integration — a strengthening worth recording, not a new risk.

## 8. Conjecture 2 corollary (§4.6) — audited at the same tier

Re-derived the mixture algebra by hand: for `x∈(0,1)`,

```
P(M(c)≤x) = Σ_{K≥0} e^{-c} c^K/K! · [1-(1-x²)^K]
          = 1 - e^{-c} Σ_K [c(1-x²)]^K/K!
          = 1 - e^{-c} e^{c(1-x²)} = 1 - e^{-cx²}
```

exactly reproducing `M(c)≟min(1,√(E/c))`. The `K=0` term contributes `0`
automatically (`1-(1-x²)^0=0`), correctly leaving the atom `P(M(c)=1)=e^{-c}`
outside this sum, not double-counted. Interchange of `Σ_K` and evaluation is
justified by absolute/dominated convergence exactly as `THEOREM.md` §5.2's
own analogous interchange (bound `c^K/K!·|1-x²|^K ≤ c^K/K!`, summable). The
two consistency checks `E[M(c)]=∫e^{-cx²}dx` (Theorem 1) and
`E[M(c)^2]=(1-e^{-c})/c` (Estágio 18's target) both follow immediately and
were independently re-verified as elementary Poisson-sum identities. §5.1's
citation (conditioning `Poisson(c)` on its count `K` gives `K` i.i.d.
uniform marks) is a standard, already-accepted fact in `THEOREM.md` itself
and is used here exactly as stated, not stretched. **Conjecture 2 survives
at the same "PROVED modulo the one citation" tier as Conjecture 1.**

## 9. Citation audit

The recursive use of the `PD(1)` size-biased/residual property — up to
`R-1≤K-1` times for a fixed `K` (four peels at `K=5`, unboundedly many as
`K→∞` but always *finitely* many for any *fixed* `K`) — is, as argued in §1,
literally the standard multi-step GEM(1) stick-breaking representation, not
an extrapolation invented for this document. Both the `K=3` and `K=4`
referees independently reached the identical conclusion for their own
(smaller) recursion depths; this review reaches the same conclusion for the
general, `K`-parametrized recursion depth. No other citation is used beyond
this one and `THEOREM.md` §5.1's already-accepted conditioning fact (used
only in the Conjecture-2 corollary, §8 above). No uncited fact was found
anywhere in the chain.

## 10. Process audit

`DERIVATION_PREREG.md` (timestamp `2026-08-25T22:00Z`) predates every script
listed in the front's own directory (file mtimes `22:01`–`22:13`) and
`ATTEMPT.md` itself (`22:20`), consistent with the front's provenance claim.
The planned route in the prereg (telescoping peel, node-chain mechanism,
Prüfer/weighted-forest route, unified `f_r`, general-`K` binomial sum) is
exactly what `ATTEMPT.md` executed — no undisclosed pivot. The front's own
declared seeds (`20260860001–20260860030`, confirmed via `grep` restricted
to its own directory) match its seeds table exactly; no seed from the
referee-reserved range `20260861000+` appears anywhere in the front's own
files. The three self-disclosed issues in `ATTEMPT.md` §6 (a `sympy`
`Piecewise`/hypergeometric check-harness artifact — the same failure mode
this review deliberately routed around, §4 above; two stray sub-0.01
`p`-values in the Lemma-1 MC, resolved by a pre-declared fresh-seed
follow-up; an over-optimistic prereg wording on `n=12` cell coverage) are
all accurately described, non-substantive, and correctly resolved — nothing
further to add.

## 11. Named issues

**None beyond the document's own three self-disclosed, already-resolved
items (§6 of `ATTEMPT.md`, audited and confirmed accurate in §10 above).**
No new mathematical, expository, or process issue was found in this review
that the document does not already disclose. In particular, the specific
sub-case flagged by the `K=3`/`K=4` referees ("redirect landing inside an
already-periodic arc") is not merely re-asserted but genuinely eliminated
by the node-level phrasing of Lemma 2 (§5 above) — this is a strict
improvement over the prior lineage's exposition, not a carried-over gap.

## 12. What this review did not attempt

`K≥7` was not exhaustively classified or recipe-MC'd (the brief's "moderate
but real" scale directive was interpreted as `K≤6`, already one `K` beyond
the front's own exhaustive range); the algebraic/Lemma-3 argument is
`K`-free and was checked to `n=7` (§5), so nothing about the proof itself
depends on extending the numerics further. The `n→∞` distributional bridge
(a different kind of open problem, per `THEOREM.md` §8's own framing) was
not addressed, exactly as the target document itself does not address it.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `ref2_symbolic_core.py` | none (exact/symbolic throughout) | — |
| `ref2_classify.py` | none (exact enumeration throughout) | — |
| `ref2_mechanism_mc.py` | `20260861100`, `20260861101`, `20260861102` | referee-reserved `20260861000+` |
| `ref2_lemma1_mc.py` | `20260861110`, `20260861111`, `20260861112` | referee-reserved `20260861000+` |
| `ref2_recipe_mc.py` | `20260861120`, `20260861121` | referee-reserved `20260861000+` |

`grep -rn "20260861"` (governance dir + the `u12_universality/theorem`
subtree) before any code confirmed only: the ledger reservation line, and
seed `20260861040` already used by the stalled prior attempt's own
`ref_symbolic_lemma1.py` (found via `grep`, that file itself never read).
This review's own seeds (`...100` onward) do not collide with it. No front
seed (`20260860xxx`) was used by this review.

## Files table

| File | Role |
|---|---|
| `ref2_symbolic_core.py` / `.log` | Lemma 1a (general `b`), the `Σ∏(b_j-1)!=K!` bijection, generic algebraic telescoping (every pattern/every `K`), 2 literal `K=5` peel instantiations, Lemma 3 exact brute-force `n=1..7`, per-`r` closed-form hand re-derivation `K=1..8`, binomial-sum closure `K=1..15`, `K=1..4` reductions, exact `K=5`/`K=6` probabilities & moments (82 checks, all PASS) |
| `ref2_classify.py` / `.log` | fresh exhaustive classification, `K=5` (`6^5=7776`) and `K=6` (`7^6=117649`), all counts/shape-types/forest-cross-checks (all PASS) |
| `ref2_mechanism_mc.py` / `.log` | from-scratch discrete per-configuration mechanism check, `K=5`, 3 scales, 300,000 trials, 0 mismatches, 7776/7776 cells at every scale |
| `ref2_lemma1_mc.py` / `.log` | independent discrete-permutation Lemma-1 MC, `K=5`, 3 scales, own `region_sizes` routine |
| `ref2_recipe_mc.py` / `.log` | independent continuum recipe MC, `K=5` (1.5M) and `K=6` (800k, beyond the front's own scope), overall + per-group KS |
| `REFEREE_REPORT.md` | this report |
| *(pre-existing, from the stalled prior attempt — not read as `.py`, not relied upon)* `ref_symbolic_lemma1.py/.log`, `ref_forest_identity.py/.log`, `ref_classify.py/.log`, `ref_assembly_symbolic.py/.log` | left in place per instructions; their `.log`s were read only as an orientation sanity-check (§0), every computation independently redone above |

---

**Summary.** `THEOREM.md` §8 Conjecture 1 is **PROVED for every `K≥1`**
(`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`), modulo the single classical `PD(1)`
size-biased/residual citation the whole `K=1..4` line already relies on,
here applied recursively a finite number of times per fixed `K` — the
residual-independence claim underlying this, attacked hardest per the
dispatch brief, holds up as a correct instance of the standard GEM(1)
stick-breaking representation. Conjecture 2 follows as an exact corollary
at the same tier. No mathematical error was found anywhere in the document
after a from-scratch reconstruction of every joint, including a genuine
test at `K=6` (classification, forest identity, and — beyond the front's
own scope — a continuum recipe Monte Carlo) that the front itself never
exhaustively ran. **ACCEPT for catalogue** into `THEOREM.md`.
