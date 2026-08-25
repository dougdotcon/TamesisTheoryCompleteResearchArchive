# Conjecture 1 at K=5 — and, via a K-uniform argument, at every K

> **Governance.** Wave 17, front (a) (`CONJECTURE-1-K5-GENERAL-ATTEMPT`),
> authorized by `DISC-DEC-072` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Pre-registered in
> `DERIVATION_PREREG.md` (this directory) before any script ran. Every
> claim below is labeled PROVED, CITED (a named classical fact used
> without re-derivation — the *same* single citation `THEOREM.md` and the
> `K=2,3,4` lineage documents use), NUMERICALLY SUPPORTED, or OPEN.
> `THEOREM.md` (closed/finalized text), all ledgers, all governance files,
> and every sibling attempt's files are **not** touched by this document —
> integration is the orchestrating session's job. No `adversarial/`
> subdirectory is created and no referee is dispatched here — that review
> is separate and still pending. No git command was run. Seed budget used:
> `20260860000+`, confirmed unused before first use
> (`grep -rn "20260860" 05_DISCOVERY_LAB/` returned only the three
> reservation lines in `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
> `DISCOVERY_LAB_STATE.md`). The referee range `20260861000+` was NOT
> used. **No script of any prior front or referee was read or imported at
> any point** — every derivation and every line of code here is fresh,
> built from the prose of `THEOREM.md` and the lineage
> `ATTEMPT.md`/`REFEREE_REPORT.md` documents only. **This document
> requires mandatory independent adversarial verification before any
> integration into `THEOREM.md` or any ledger.** Nothing here is asserted
> as fact anywhere else in the archive until that review completes.

> **Executive summary (read first).** `THEOREM.md` §8 Conjecture 1 states
> `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`; proved at `K=1` (§5.3), `K=2` (Estágio
> 15), `K=3` (Estágio 17), `K=4` (Estágio 20). The `K=4` document and its
> referee named one concrete candidate route for `K\ge5`: prove the
> weighted-forest identity `E(E+Q)^{n-1}=E` for all `n`, closing the one
> genuinely per-`K` ingredient all at once. This front was dispatched to
> attack `K=5`, with general `K` as a stretch goal contingent on every
> step being genuinely `K`-uniform, and honest non-closure fully
> acceptable.
>
> **Both targets close.**
>
> > **Theorem (this document, PROVED modulo one classical citation — the
> > same single `PD(1)` size-biased/residual citation the `K=1..4` line
> > uses).** For **every** integer `K\ge1`,
> > `f_{M_K}(x) = 2Kx(1-x^2)^{K-1}` on `(0,1)`, exactly.
> > In particular `f_{M_5}(x)=10x(1-x^2)^4` — the `K=5` instance — and
> > `THEOREM.md` §8 **Conjecture 1 is closed for all `K`**, not one `K`
> > at a time.
>
> The three joints that were previously verified per-`K` are here proved
> uniformly in `K`:
> **(1) Lemma 1 (uniform simplex law), general `K`.** The joint law of
> the region masses `(m_1,\dots,m_K)` is exactly uniform with density
> `K!` on `\Delta_K=\{m_i>0,\ \sum m_i<1\}`. Two new general proofs
> replace per-`K` case work: (a) the *labeled circular spacings* fact is
> proved for every block size `b` at once (each of the `(b-1)!` cyclic
> orderings contributes a unit-Jacobian cell mapping onto the full gap
> simplex — §2.1); (b) the sequential block-peeling factor
> `(b_j{-}1)!\,(1-s_j)^{K-c_j}/(1-s_{j-1})^{K-c_{j-1}}` **telescopes**
> over the blocks of any co-block pattern, so every pattern contributes
> the constant `\prod_j(b_j{-}1)!` with no case analysis (§2.2); summing
> over patterns gives `K!` by the partition↔permutation bijection already
> proved at `K=4` (§2.3). The classical citation is used once per peel —
> up to four peels at `K=5`, and `R-1\le K-1` peels in general, which is
> literally the multi-step GEM(1)/stick-breaking representation, exactly
> as the `K=3`/`K=4` referees verified for two and three peels.
> **(2) The mechanism formula, general `K`.** `M_K = (1-\sum_i m_i) +
> \sum_{j\in C}(m_j-P_j)` where `C` is the set of nodes on cycles of the
> region-level redirect map `g` — proved by a *node-chain* argument
> (§3.1) that is one paragraph, `K`-independent, and **subsumes with no
> case split** the "redirect landing inside an already-periodic arc"
> sub-case that the `K=3` and `K=4` referees had to trace by hand.
> **(3) The off-cycle weight `W=1-Q`, ALL `n` at once (the named
> candidate route — closed).** The weighted-forest identity
> `W(n)=e\,(e+q_1+\cdots+q_n)^{n-1}` is **proved for every `n`** by the
> Prüfer-sequence bijection (§3.2); at `e+Q=1` it degenerates to
> `W=e=1-Q` — precisely `E(E+Q)^{n-1}=E`. This was the single ingredient
> `K=4` verified only case-by-case (`n_{\mathrm{off}}\le4`); it is now a
> theorem for all `n`, so nothing per-`K` remains anywhere in the chain.
> **(4) Assembly in closed form, general `K`.** The per-`r` density
> collapses to the two-term closed form
> `f_r(x)=\binom{K}{r}x^r(1-x)^{K-1}\,[K-(K{-}r)(1-x)]` (valid for all
> `r=0..K` including both edge cases), and the sum over `r` closes by
> the binomial theorem: `\sum_r f_r = 2Kx(1-x^2)^{K-1}` (§4.3) — a
> five-line computation, uniform in `K`.
>
> Verification at `K=5` (all fresh code, fresh seeds `20260860000+`):
> exhaustive classification of all `6^5=7776` raw destination
> configurations (19 shape types, matching the pre-registered
> `\sum_{s\le5}p(s)`); the forest identity verified as an exact
> polynomial identity for `n=1..6`; a **machinery-free exact-`Fraction`
> moment surface** over the raw 7776 configurations (66 per-`r` moments
> `p=0..10`, all matching the derived polynomials exactly — since
> `\deg f_r\le9`, this pins every coefficient with margin); a discrete
> per-configuration mechanism check (**0 mismatches in 555,000 trials**,
> all 7776 raw cells hit at the main scale, collisions/fixed points
> saturated at `n=12`); a discrete-permutation Lemma-1 MC at 3 scales; a
> raw discrete full-model simulation at `n=10000, 20000`; and a 2M-sample
> continuum recipe MC with per-group KS (6/6 pass). Reduction checks: the
> general formula at `K=1,2,3,4` reproduces every published, already
> adversarially-reviewed group density **group by group**, and the
> general-`K` sum is verified symbolically for `K=1..12`.
>
> Byproducts: new exact moments `E[M_5]=256/693=\varphi_5` (= the §5.2
> Wallis value), `E[M_5^2]=1/6`, `E[M_5^3]=256/3003`; and, for all `K`,
> `E[M_K^2]=1/(K+1)` — closing the moment target Estágio 18 could anchor
> only at `K\le4`. A short corollary (§4.6, flagged for the orchestrator)
> records that **Conjecture 2 follows** from the general-`K` theorem by
> the Poisson mixture already definitional in `THEOREM.md` §5.1.
>
> Two process items are disclosed in the open (§6): a sympy `Piecewise`
> artifact in one *check harness* (not in any derivation), and two stray
> sub-`0.01` p-values among the 12 statistics of the Lemma-1 MC, resolved
> as chance by a pre-declared higher-power follow-up on fresh seeds (the
> original run is reported as-is, not rerun).

---

## 0. Discipline / provenance

`DERIVATION_PREREG.md` (this directory) was written and saved before any
script ran:

```
2026-08-25T22:00Z  DERIVATION_PREREG.md
2026-08-25T22:0xZ+ (all scripts/logs below, same session, in the order
                    listed in the files table)
```

All arithmetic labeled PROVED is exact (`sympy` symbolic integration and
`fractions.Fraction` combinatorics — no floating point enters any
derivation step; floats appear only in the Monte Carlo checks, exactly as
the `K=2,3,4` documents do). Monte Carlo checks use
`numpy.random.SeedSequence` values `20260860001–20260860030` (all listed
in the seeds table), from this front's reserved block, confirmed unused
before first use.

## 1. Setup — the continuum whole-space K-conditional model, and Lemma 0

Exactly generalizing the `K=2,3,4` lineage's object to arbitrary `K`: an
independent `PD(1)` cyclic partition of `[0,1]` (`THEOREM.md` Definition
2(i)); `K` reroute sources `x_1,\dots,x_K\sim\mathrm{Unif}(0,1)` i.i.d.;
`K` destinations `u_1,\dots,u_K\sim\mathrm{Unif}(0,1)` i.i.d., independent
of everything else. The map: `f(x_i)=u_i` for each `i`, and `f(y)=`
background cyclic-successor of `y` for every other `y`. Target: the
density of `M_K:=\mathrm{Leb}(\{y:y\text{ cyclic under }f\})`. This is
the same whole-space redescription of `L(c)` conditional on exactly `K`
reroutes that `THEOREM.md` §5.3 uses at `K=1` and the lineage uses at
`K=2,3,4`; its identification with §5.1's conditional model carries the
same already-accepted status (Proposition 2.4's citation) as everywhere
else in this line — nothing new is asked here.

**Lemma 0 (locality of cyclic status; identical to the lineage's, stated
`K`-free).** A point `y` is cyclic under `f` iff its forward `f`-orbit
returns to `y` in finitely many steps. Only the sources' outgoing arrows
are modified, so every other point's own future trajectory is exactly the
background one, regardless of what flows *into* it. Consequently (a) a
background block containing no source is unaffected in full (its points
are cyclic exactly as before — this is the "OUT" mass `1-\sum_i m_i`),
and (b) within the touched region, whether a point is cyclic depends only
on its own forward chain (background flow, jump at a source, background
flow, …); an incoming jump landing at a point `w` never changes `w`'s own
subsequent orbit. The argument never mentions `K`.

**Regions.** For `i=1..K`, region `i` (`m_i` := its Lebesgue measure) is
the set of points whose background flow reaches `x_i` before (if ever)
reaching any other source. Within a block containing `b\ge1` sources, the
regions are the `b` arcs ending (in flow direction) at the respective
sources; a block containing exactly one source is that source's region in
full. Regions partition the union of touched blocks.

## 2. Step A — Lemma 1 for every K

> **Lemma 1 (general `K`; PROVED given the cited residual property).**
> `(m_1,\dots,m_K)` has joint density **exactly `K!` (constant)** on
> `\Delta_K=\{m_1,\dots,m_K>0,\ \sum_i m_i<1\}`.

The proof has three parts, each uniform in `K`.

### 2.1 Labeled circular spacings, every block size at once (PROVED)

> **Lemma 1a.** Fix `\ell>0`. On a circle of circumference `\ell`, fix an
> anchor point and place `b-1` i.i.d. `\mathrm{Unif}` free points. Label
> each of the `b` circular gaps by the point at its forward (flow-wise)
> end. Then the labeled gap vector `(G_1,\dots,G_b)` is distributed as
> `\ell\cdot\mathrm{Dirichlet}(1,\dots,1)`; equivalently, any `b-1` of the
> labeled gaps have joint density `(b-1)!/\ell^{\,b-1}` on
> `\{g_i>0,\ \sum g_i<\ell\}`.

*Proof.* Put the anchor at coordinate `0` (the block's cyclic coordinate
is defined up to rotation, and gaps depend only on relative positions).
The free points `(Y_2,\dots,Y_b)` have joint density `1/\ell^{\,b-1}` on
`(0,\ell)^{b-1}`. Partition the domain (up to a null set) into the
`(b-1)!` open cells given by the orderings of the free points. On the
cell with cyclic order `0\to Y_{i_1}\to\cdots\to Y_{i_{b-1}}\to 0` (flow
direction), the labeled gaps are `G_{i_1}=Y_{i_1}`,
`G_{i_k}=Y_{i_k}-Y_{i_{k-1}}` (`k\ge2`), and the anchor's gap
`\ell-Y_{i_{b-1}}` (dependent). The map
`(Y_{i_1},\dots,Y_{i_{b-1}})\mapsto(G_{i_1},\dots,G_{i_{b-1}})` is
triangular with unit Jacobian, and it is a bijection from the ordering
cell onto the **full** open simplex `\{g>0,\sum g<\ell\}` (invert by
partial sums; the ordering constraints are exactly positivity of the
gaps). So each ordering cell contributes density `1/\ell^{\,b-1}` on the
full simplex; summing the `(b-1)!` cells gives `(b-1)!/\ell^{\,b-1}`. `∎`

(The `b=2,3,4` instances are the facts the `K=2,3,4` documents proved
one at a time; `b` is now a free parameter. Verified symbolically for
`b=2..6`, all orderings unimodular — `derive_lemma1_general_symbolic.py`
Part 1.)

### 2.2 The telescoping peel (PROVED modulo the citation)

Condition on the co-block pattern `\pi` (the set partition of
`\{1..K\}` by shared background-block membership; `\mathrm{Bell}(K)`
mutually exclusive events). Order `\pi`'s blocks `B^{(1)},\dots,B^{(R)}`
by their minimal source index; write `b_j=|B^{(j)}|`,
`c_j=b_1+\cdots+b_j`, `\ell_j` for block `j`'s length,
`s_j=\ell_1+\cdots+\ell_j` (`s_0=c_0=0`). Peel the blocks in order. At
peel `j`, conditionally on peels `1..j-1`:

- **(residual state)** the un-placed sources (`K-c_{j-1}` of them) are
  i.i.d. uniform on the residual set (measure `1-s_{j-1}`) — immediate,
  since they are i.i.d. `\mathrm{Unif}(0,1)` conditioned to avoid the
  removed blocks — and the residual partition, rescaled by
  `1/(1-s_{j-1})`, is a fresh `PD(1)` partition independent of everything
  revealed. **CITED:** for `j=1` this is just the setup; for `j\ge2` it
  is the classical size-biased-deletion/residual property of
  `PD(1)`/`GEM(1)` (McCloskey 1965; Patil–Taillie 1977; Pitman,
  *Combinatorial Stochastic Processes*, St-Flour 2002, Ch. 3), applied
  `j-1` times — the multi-step stick-breaking representation. This is
  the **identical** citation `K=2` used once, `K=3` twice, `K=4` three
  times; at `K=5` the deepest pattern (`1^5`) uses it four times, and in
  general `R-1\le K-1` times — iterating a self-similar property finitely
  often, exactly what both prior referees confirmed the citation
  licenses.
- **(anchor)** the anchor `a_j` (least un-placed index) is a uniform
  point on the residual, so its block is a size-biased pick from the
  rescaled fresh `PD(1)`: the rescaled length is `\mathrm{Unif}(0,1)`
  (same citation), i.e. `\ell_j` has conditional density
  `1/(1-s_{j-1})` on `(0,\,1-s_{j-1})`.
- **(membership)** each of the other `K-c_{j-1}-1` un-placed sources
  independently lands in `B^{(j)}` with probability
  `\ell_j/(1-s_{j-1})`; the pattern requires exactly the `b_j-1`
  designated members to land inside and the remaining `K-c_j` to stay
  outside — probability
  `[\ell_j/(1-s_{j-1})]^{\,b_j-1}\,[(1-s_j)/(1-s_{j-1})]^{\,K-c_j}`.
- **(gaps)** given membership, the `b_j-1` members are i.i.d. uniform
  within `B^{(j)}`; by Lemma 1a the labeled gaps — which are exactly
  `(m_i)_{i\in B^{(j)}}`, summing to `\ell_j` — have conditional density
  `(b_j-1)!/\ell_j^{\,b_j-1}` (with respect to any `b_j-1` of them).

Multiplying the four factors, the `\ell_j`-powers cancel and peel `j`
contributes

`(b_j-1)!\ \cdot\ \dfrac{(1-s_j)^{K-c_j}}{(1-s_{j-1})^{K-c_{j-1}}}`

(exponent bookkeeping: `1+(b_j-1)+(K-c_j)=K-c_{j-1}`). The product over
`j=1..R` **telescopes**: the numerator of the last peel is
`(1-s_R)^{K-c_R}=(1-s_R)^0=1` and the first denominator is `1`, leaving
exactly `\prod_j(b_j-1)!` — a constant, for **every** pattern, with no
per-pattern case analysis. The change of variables from
`(\ell_1..\ell_R,\ \text{gaps dropping one per block})` to
`(m_1,\dots,m_K)` is triangular with unit Jacobian (block sums recover
the `\ell_j`), and the support is all of `\Delta_K` (any `m\in\Delta_K`
is consistent with any pattern by setting `\ell_j=\sum_{i\in B^{(j)}}m_i`).
So pattern `\pi` contributes the constant density `\prod_j(b_j-1)!` on
`\Delta_K`. (All `2+5+15+52` patterns for `K=2..5` verified to telescope
symbolically — `derive_lemma1_general_symbolic.py` Part 2.)

### 2.3 Summing the patterns (PROVED)

`\sum_{\text{set partitions of }\{1..K\}}\ \prod_j(b_j-1)! = K!` — the
elementary bijection (a permutation's disjoint-cycle decomposition *is* a
set partition equipped with one of the `(b-1)!` cyclic orders per block),
first recorded in this lineage by the `K=4` document, here used for
general `K`; verified by enumeration for `K=1..8`
(`1,2,6,24,120,720,5040,40320`). Since the pattern events are disjoint
and exhaustive, `(m_1..m_K)` has density `K!` on `\Delta_K`. `∎` (Lemma 1)

At `K=5`: `\mathrm{Bell}(5)=52` patterns in 7 integer-partition shapes
with multiplicities `1,5,10,10,15,10,1` and constants
`24,6,2,2,1,1,1`, contributions `24+30+20+20+15+10+1=120=5!` — the
pre-registered table, confirmed.

## 3. Step B — the destination mechanism for every K

Each destination `u_i` lands in region `g(i)\in\{1..K\}` (probability
`m_{g(i)}` given the masses, landing offset uniform within the region) or
in OUT (`g(i)=\mathrm{OUT}`, probability `1-\sum m`), independently
across `i`. Let `C` be the set of nodes on cycles of
`g:\{1..K\}\to\{1..K\}\cup\{\mathrm{OUT}\}` (equivalently: `g|_C` is a
permutation of `C` and no cycle of `g` meets the complement — a cycle
through a `C`-node stays in `C` since `g` maps `C` into `C`). Write
`r=|C|`, `n_{\mathrm{off}}=K-r`, `Q=\sum_{i\notin C}m_i`.

### 3.1 The mechanism formula (PROVED, K-uniform, no case split)

> **Lemma 2.** Almost surely, the cyclic set of `f` is the union of (i)
> all untouched blocks and (ii) for each `j\in C`, the arc of region `j`
> from the landing point of the unique on-cycle redirect into region `j`
> forward to `x_j`. Hence
> `M_K = (1-\textstyle\sum_i m_i) + \sum_{j\in C}(m_j-P_j)
>      = 1 - Q - \sum_{j\in C}P_j`,
> `P_j\in(0,m_j)` the landing offset (from the region's start).

*Proof.* (i) is Lemma 0(a). For the rest, note first that within a
region the background flow is strictly forward (an arc ending at its
source), so an orbit that leaves a region can revisit it only by some
*jump* landing there — and by Lemma 0(b) the only jumps on `y`'s own
orbit are those the orbit itself takes at sources.

**Off-cycle regions contribute zero.** Let `k\notin C` and
`y\in\text{region }k`. `y`'s orbit flows to `x_k`, jumps to `u_k` (in
region `g(k)`, or OUT), and thereafter visits regions
`g(k),g^2(k),g^3(k),\dots` in order: landing in region `g^t(k)`, flowing
forward to `x_{g^t(k)}`, jumping again. If some `g^t(k)=\mathrm{OUT}`,
the orbit enters a source-free block and stays on its background cycle
forever (that block contains no source, so no further jumps ever occur)
— it never returns to region `k`. Otherwise the node sequence
`k,g(k),g^2(k),\dots` lives in the finite set `\{1..K\}`, so it is
eventually periodic, and its periodic part is a cycle of `g` — a subset
of `C`. Since `k\notin C`, `g^t(k)\neq k` for every `t\ge1`. Either way
the orbit never re-enters region `k` after leaving it, hence never
returns to `y`: no point of region `k` is cyclic. (Note this argument
needs no case split on *where* off-cycle redirects land — in particular
the "redirect landing inside an already-periodic arc" sub-case that the
`K=3`/`K=4` referees traced by hand never arises: incoming jumps are
simply not part of `y`'s own orbit.)

**On-cycle regions contribute exactly their tail arcs.** Let `j\in C`
with `g`-cycle `j\to g(j)\to\cdots\to j`, and let `i` be `j`'s cycle
predecessor (`g(i)=j`), so `u_i` lands in region `j` at offset `P_j`.
For `y` at offset `\rho` in region `j`: the orbit flows to `x_j`, then
traverses the cycle (landing at the fixed offsets `P_{g(j)}`, etc.), and
re-enters region `j` precisely via `u_i` at offset `P_j`, then flows
forward to `x_j` — and repeats, forever, with the same landing offsets.
If `\rho\ge P_j` the orbit's re-entry at `P_j` flows forward *through*
`y`: `y` is periodic. If `\rho<P_j` the orbit re-enters only at
`P_j>\rho` and moves forward, never reaching `y` again: `y` is not
cyclic. So region `j`'s cyclic part is the arc `[P_j,m_j]`, mass
`m_j-P_j`. Boundary coincidences (`\rho=P_j`, landings exactly on
sources, destination collisions) have probability zero. `∎`

Verified at the most granular level available: a from-scratch discrete
per-configuration check (`mechanism_check_k5.py`, §5.2) — ground-truth
orbit tracing vs. the discrete counterpart of this formula
(`M_{\text{pred}}=\#\mathrm{OUT}+\sum_{i\in\mathrm{cyc}(g)}(D_i{+}1)`)
— found **0 mismatches in 555,000 trials** across `n=12,25,150`, with
all `7776` raw cells hit at the main scale and collisions/fixed points
saturated at `n=12` (62% / 35% of trials).

### 3.2 The off-cycle weight for every n: the weighted-forest identity (PROVED)

Conditional on the masses, the probability that the off-cycle part of
`g` equals a specific assignment (each off node targeting a region or
OUT, forming no cycle inside the off-set — self-loops included) is the
product of the target masses. The total off-cycle weight is therefore

`W(n) := \sum_{\substack{h:[n]\to[n]\cup\{\mathrm{ext}\}\\ \text{no cycle inside }[n]}}\ \prod_{i=1}^{n} w(h(i))`,

with `n=n_{\mathrm{off}}`, `w(i)=q_i` (the `i`-th off region's mass) and
`w(\mathrm{ext})=e` (the combined external mass: OUT plus all on-cycle
regions — the sum over *which* external target factorizes, since the
no-internal-cycle constraint does not involve external edges).

> **Lemma 3 (weighted rooted forests, all `n`).** As an identity of
> polynomials in commuting indeterminates `e,q_1,\dots,q_n`:
> `W(n) = e\,(e+q_1+\cdots+q_n)^{\,n-1}` for every `n\ge1`.
> Consequently, at `e = 1-Q` with `Q=q_1+\cdots+q_n` (so `e+Q=1`):
> `W(n) = 1-Q` for every `n` — the identity `E(E+Q)^{n-1}=E` named by
> Estágio 20 as the candidate route, now proved in general.

*Proof.* A map `h` with no internal cycle is exactly a parent-pointer
description of a tree on the vertex set `V=\{0,1,\dots,n\}` rooted at
`0:=\mathrm{ext}` (every forward path leaves `[n]`, so the functional
graph is a forest of trees hanging on `0`). Its weight is
`\prod_{i\ge1} w(h(i)) = \prod_{v\in V} w_v^{\,c(v)}`, `c(v)` the number
of children of `v`. Rooted-at-`0` trees on `V` are in bijection with
unrooted labeled trees on `V` (`n+1` vertices), and for a tree `T`:
`c(v)=\deg_T(v)-1` for `v\neq0`, `c(0)=\deg_T(0)`, so the weight equals
`w_0\prod_{v\in V}w_v^{\deg_T(v)-1}`. The Prüfer bijection maps labeled
trees on `n+1\ge2` vertices bijectively onto sequences in `V^{\,n-1}` in
which each vertex `v` appears exactly `\deg_T(v)-1` times. Hence
`\sum_T \prod_v w_v^{\deg_T(v)-1} = \sum_{\text{sequences}}\prod w =
(\sum_{v} w_v)^{\,n-1}`, and `W(n)=w_0(\sum w)^{n-1}
= e(e+q_1+\cdots+q_n)^{n-1}`. (`n=1`: the single tree has weight `e`,
and `(\cdot)^0=1` — consistent.) `∎`

Verified brute-force as an exact polynomial identity in distinct
symbolic masses for `n=1..6` (`forest_identity_check.py`; the `n=5` case
is the one `K=5` needs; acyclic-map counts `(n{+}1)^{n-1} =
1,3,16,125,1296,16807` also match, extending the `K=4` referee's
`1,3,16,125` sequence two steps).

The `r=0` boundary case is the same statement with **all** `K` nodes
off-cycle: `P(\text{no cycle at all}\mid m)=W(K)=1-\sum_i m_i`.

## 4. Step C/D — assembly for every K

### 4.1 The joint density for fixed (C, σ)

Fix an on-cycle set `C` (`|C|=r\ge1`) and a permutation `\sigma` of `C`
(the on-cycle part of `g`; any of the `r!` permutations of `C` can occur,
each the union of its cycles). Conditional on the masses:

- each `i\in C` must land in region `\sigma(i)`; the probability of
  landing there *at offset* `P_{\sigma(i)}\in\mathrm dp` is exactly
  `\mathrm dp` (probability `m_{\sigma(i)}` times conditional offset
  density `1/m_{\sigma(i)}` — the same exact cancellation the lineage
  relies on, valid verbatim for every `K`); since `\sigma` is a
  bijection, each on-cycle region `j\in C` receives exactly one landing,
  with offset `P_j` of joint density `\prod_{j\in C}\mathbf1\{0<P_j<m_j\}`;
- the off-cycle part contributes the weight `W(n_{\mathrm{off}})=1-Q`
  (Lemma 3), and off-cycle landing offsets do not enter `M_K` (Lemma 2),
  so they are integrated out.

With Lemma 1's density `K!` for the masses, the joint density of
`\big((m_j,P_j)_{j\in C},(m_i)_{i\notin C}\big)` on the event
`\{\text{on-cycle part}=(C,\sigma)\}` is `K!\,(1-Q)` on
`\{0<P_j<m_j,\ m\in\Delta_K\}` — **independent of `\sigma`**, which is
the general-`K` form of the "depends only on `r_{\mathrm{on}}`" fact.
Summing over the `r!` permutations multiplies by `r!`; the `\binom{K}{r}`
choices of `C` contribute equally (the density `K!` is symmetric), giving
the factor `\binom{K}{r}` at the end.

### 4.2 Marginalizing to the per-r density

Change variables `D_j:=m_j-P_j` (unit Jacobian): the density is still
`K!\,r!\,(1-Q)` in `\big((P_j)_{j\in C},(D_j)_{j\in C},(m_i)_{i\notin C}\big)`
on `\{$all positive$,\ \sum P+\sum D+Q<1\}`, and
`M_K = 1-Q-\sum_{j\in C}P_j` (Lemma 2). Fix `x`; for fixed `Q`, the
constraint `M_K=x` fixes `s:=\sum P_j = 1-x-Q` (`|\mathrm ds/\mathrm dx|=1`),
the `P`-slice has surface measure `s^{r-1}/(r-1)!`, the off-slice
`Q^{\,n_{\mathrm{off}}-1}/(n_{\mathrm{off}}-1)!`, and the free `D`-vector
ranges over `\{\sum D< x\}`, volume `x^r/r!`. Hence for `1\le r\le K-1`:

`f_r(x) = \binom{K}{r} K!\ x^r \displaystyle\int_0^{1-x}
  (1-Q)\ \frac{Q^{\,n_{\mathrm{off}}-1}}{(n_{\mathrm{off}}-1)!}\
  \frac{(1-x-Q)^{r-1}}{(r-1)!}\ \mathrm dQ`,

with the edge cases `r=K` (no `Q`-integral: `f_K=K x^K(1-x)^{K-1}`) and
`r=0` (`M=1-Q` with weight `1-Q`: `f_0=Kx(1-x)^{K-1}`). Substituting
`Q=(1-x)v` and using Beta integrals
(`B(n,r)/((n{-}1)!(r{-}1)!)=1/(K{-}1)!`,
`B(n{+}1,r)/((n{-}1)!(r{-}1)!)=n/K!`):

> **Unified per-`r` closed form (all `r=0..K`, edge cases included):**
> `f_r(x) = \binom{K}{r}\ x^r (1-x)^{K-1}\ \big[K-(K{-}r)(1-x)\big]`.

(Check: `r=0` gives `Kx(1-x)^{K-1}` ✓; `r=K` gives `Kx^K(1-x)^{K-1}` ✓.)

### 4.3 The sum over r: the binomial theorem closes the conjecture

`\sum_{r=0}^{K} f_r(x)
 = (1-x)^{K-1}\Big[K\sum_r\binom{K}{r}x^r
   \;-\;(1-x)\sum_r (K{-}r)\binom{K}{r}x^r\Big]
 = (1-x)^{K-1}\big[K(1+x)^K - (1-x)\,K(1+x)^{K-1}\big]`

using `\sum_r\binom{K}{r}x^r=(1+x)^K` and
`\sum_r (K{-}r)\binom{K}{r}x^r = K\sum_r\binom{K-1}{r}x^r
= K(1+x)^{K-1}`. Factoring `K(1+x)^{K-1}(1-x)^{K-1}`:

`\sum_{r} f_r(x) = K(1-x^2)^{K-1}\big[(1+x)-(1-x)\big]
                = 2Kx(1-x^2)^{K-1}.`

> **Theorem.** For every integer `K\ge1`,
> `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` on `(0,1)` — PROVED, modulo the citation
> of §2.2 (the `PD(1)` size-biased/residual property, applied recursively
> up to `K-1` times — the identical single citation of the whole
> `K=1..4` line, used the number of times the construction calls for).
> In particular `f_{M_5}(x)=10x(1-x^2)^4`.

### 4.4 The K=5 instance, explicitly

`f_0=5x(1-x)^4`, `f_1=5x(1-x)^4(1+4x)`, `f_2=10x^2(1-x)^4(2+3x)`,
`f_3=10x^3(1-x)^4(3+2x)`, `f_4=5x^4(1-x)^4(4+x)`, `f_5=5x^5(1-x)^4`;
group probabilities `1/6,\ 5/14,\ 25/84,\ 5/36,\ 1/28,\ 1/252` (sum
`252/252=1`); sum `=10x-40x^3+60x^5-40x^7+10x^9=10x(1-x^2)^4` — all
verified symbolically (`derive_assembly_k5_symbolic.py`) and, coefficient
by coefficient, by the machinery-free exact route of §5.3.

### 4.5 Moments (all exact; new)

`\int_0^1 f_{M_K}=1`; `E[M_K]=K\,B(3/2,K)=\varphi_K` (the §5.2 Wallis
integral — at `K=5`: `256/693`); `E[M_K^2]=K\,B(2,K)=1/(K+1)` — proving,
for **all** `K`, the moment target Estágio 18 recorded with anchors only
at `K\le4`; at `K=5` additionally `E[M_5^3]=256/3003`.

### 4.6 Corollary: Conjecture 2 follows (flagged for the orchestrator)

`THEOREM.md` §8 Conjecture 2 is, by its own statement, the
`\mathrm{Poisson}(c)`-mixture of Conjecture 1 over `K`, and §5.1 already
records (with its Kingman citation) that conditioning the unconditional
model on `\mathcal N=K` yields exactly the `K`-conditional model. Given
the Theorem above, for `x\in(0,1)`:

`P(M(c)\le x) = \sum_{K\ge0} e^{-c}\frac{c^K}{K!}\big[1-(1-x^2)^K\big]
 = 1-e^{-c}e^{c(1-x^2)} = 1-e^{-cx^2}`,

with the atom `P(M(c)=1)=e^{-c}` (the `K=0` term; `M_K<1` a.s. for
`K\ge1` since `f_{M_K}` is a proper density). This is exactly
`M(c)\overset{d}{=}\min(1,\sqrt{E/c})`, `E\sim\mathrm{Exp}(1)` —
**Conjecture 2**, at the same PROVED-modulo-citation tier as the Theorem
(the only extra ingredients are §5.1's already-cited conditioning fact
and countable additivity). Consistency: `E[M(c)]=\int_0^1e^{-cx^2}dx
=\varphi_\infty(c)` reproduces Theorem 1, and
`E[M(c)^2]=\sum_K e^{-c}c^K/K!\cdot\frac1{K+1}=(1-e^{-c})/c` — Estágio
18's second-moment target, now exact. Estágio 18's *direct* route
remains failed as recorded; this closure is indirect, through the now
general-`K` Conjecture 1. Recorded here as a corollary; whether and how
to catalogue it is the orchestrating session's decision after
adversarial review.

## 5. Verification

### 5.1 Symbolic derivation scripts (the proof's computations)

`derive_lemma1_general_symbolic.py`/`.log`: Part 0 — the
`\sum\prod(b_j-1)!=K!` identity, `K=1..8`; Part 1 — Lemma 1a by direct
change of variables, all orderings unimodular, `b=2..6`; Part 2 — the
telescoping peel product for **every** set partition at `K=2..5`
(`2+5+15+52` patterns), each simplifying to `\prod(b_j-1)!`; Part 3 —
pattern probabilities sum to 1, plus two direct `K=5` integral
spot-checks. **All pass.**

`enumerate_destination_combinatorics_k5.py`/`.log`/`.json`: exhaustive
classification of all `6^5=7776` raw maps — per-`r` counts
`1296,2160,2160,1440,600,120` (pre-registered), `19` shape types
(`=\sum_{s\le5}p(s)`, pre-registered), `N(r,n_{\mathrm{off}})` constant
across every specific on-set/`\sigma` choice and equal to the
labeled-forest count `(r{+}1)(r{+}1{+}n_{\mathrm{off}})^{n_{\mathrm{off}}-1}`,
cross-footing to `6^5`; the same at `K=6` (`7^6=117649` maps, `30`
types) as a beyond-target uniformity check. **All pass.**

`forest_identity_check.py`/`.log`: Lemma 3 verified as an exact
polynomial identity (own `Fraction`/dict polynomial engine, no floats)
for `n=1..6`, plus unit-weight counts and exact rational evaluations at
`e=1-Q`. **All pass.**

`derive_assembly_k5_symbolic.py`/`.log`: the §4.2 integral route vs. the
unified closed form (all six `r`), the symbolic sum `=10x(1-x^2)^4`, the
probabilities/moments (including the independent Wallis target), the
reduction checks (§7 below), the general-`K` sum for `K=1..12`, and the
two binomial identities of §4.3 with symbolic `K`. **All pass** (after
one disclosed check-harness fix — §6, item 1).

### 5.2 Discrete mechanism check and Monte Carlo

`mechanism_check_k5.py`/`.log`/`.json` (seeds `20260860001/002/003`):

```
n= 12, trials= 30000: mismatches=0, cells hit=6995/7776, collisions=18582, fixed-points=10492
n= 25, trials=500000: mismatches=0, cells hit=7776/7776, collisions=173168, fixed-points=92383
n=150, trials= 25000: mismatches=0, cells hit=6742/7776, collisions=1553,  fixed-points=802
TOTAL: 0 mismatches / 555,000 trials
```

Full 7776-cell coverage at the main scale (`n=25`), as pre-registered;
the `n=12` and `n=150` scales cannot cover all cells at their trial
counts (30000, 25000 < 4×7776) and are reported honestly as partial —
their role is edge-case saturation (`n=12`: 62% collision, 35%
fixed-point trials) and large-`n` confirmation respectively.

`mc_lemma1_k5_check.py`/`.log`/`.json` (seeds `20260860020/021/022`):

```
n=300:  worst moment |z|=1.84; KS(L) p=0.0000, KS(pooled) p=0.0000 [expected small-n signature]
        exchangeability p=0.82/0.35
n=1000: worst moment |z|=2.15; KS(L) p=0.29, KS(pooled) p=0.026
        exchangeability p=0.0039/0.023   <-- flagged, see §6 item 2
n=5000: worst moment |z|=1.57; KS(L) p=0.0085, KS(pooled) p=0.054
        exchangeability p=0.24/0.60      <-- KS(L) flagged, see §6 item 2
```

`mc_lemma1_k5_followup.py`/`.log`/`.json` (pre-declared follow-up, fresh
seeds `20260860023/024`, higher power): exchangeability KS(m1,m2) at
`n=1000`, 40000 trials: `p=0.92`; KS(L) at `n=5000`, 20000 trials:
`D=0.0045, p=0.82`. Both flags resolve as chance (§6 item 2).

`discrete_k5_full_distribution_mc.py`/`.log`/`.json` (seeds
`20260860010/011`) — raw finite-`n` model, none of the machinery:

```
n=10000, trials=4000: KS D=0.01448 p=0.3682  mean=0.367612±0.002690 vs 256/693 (z=-0.67)
n=20000, trials=2000: KS D=0.02997 p=0.0539  mean=0.362605±0.003910 vs 256/693 (z=-1.74)
```

Both pass the registered criteria (no rejection at `\alpha=0.01`,
`|z|<3`); the `n=20000` `p=0.054` is unremarkable but reported.

`mc_recipe_check_k5.py`/`.log`/`.json` (seed `20260860030`,
`N=2{,}000{,}000`, vectorized, independent re-implementation):

```
overall: KS D=0.00071 p=0.2695  mean=0.369271±0.000123 (z=-1.12)
group fractions r=0..5: z = +0.92, +1.17, -0.48, -1.14, -1.06, -1.49
per-group KS vs conditional f_r: p = 0.53, 0.91, 0.96, 0.33, 0.087, 0.95
```

All 6 group fractions and all 6 per-group KS pass.

### 5.3 The machinery-free exact route (raw-7776 moment surface)

`raw7776_exact_moments_k5.py`/`.log`/`.json`: for **each** of the 7776
raw configurations separately, `E[M^p\,\mathbf1\{\text{config}\}]` is
computed exactly (`fractions.Fraction`, no floats) from only the
primitive facts (Lemma 1's density, independent uniform destinations,
Lemma 2's formula) — with **no** collapse machinery: no forest identity,
no `W=1-Q`, no `\sigma`-independence, no per-`r` integral formula. The
inner `P`-integrations produce terms `c\,(1-\sum_{i\in T}m_i)^q` with
`T` between the off-set and its union with `C`; each term is integrated
in closed form by the two-stage Dirichlet reduction

`\int_{\Delta_K}\prod_i m_i^{e_i}\,\big(1-\sum_{i\in T}m_i\big)^{q}\,dm
 = \frac{\prod_i e_i!\ \cdot\ (q+E_U+|U|)!}{(E_U+|U|)!\ \cdot\ (\sum_i e_i+K+q)!}`

(`U` = complement of `T` in the `K` mass indices, `E_U=\sum_{i\in U}e_i`;
derived by integrating the `U`-variables first over their sub-simplex,
then the `T`-variables as a standard Dirichlet integral; OUT-factors
`(1-\sum_{\text{all}}m)^a` are expanded multinomially first). Result:
**all 66 per-`r` moments (`r=0..5`, `p=0..10`) and all 11 totals match
the exact integrals of the derived polynomials, as exact fractions** —
including `P(r)=1/6,5/14,25/84,5/36,1/28,1/252`, `E[M_5]=256/693`,
`E[M_5^2]=1/6`, `E[M_5^3]=256/3003`. Since `\deg f_r\le9`, agreement at
`p=0..9` alone determines each polynomial uniquely; every load-bearing
coefficient is thus confirmed by two genuinely independent exact routes.

### 5.4 Summary table

| Check | What | Result |
|---|---|---|
| §5.1 | Lemma 1a (`b=2..6`), telescoping (74 patterns, `K=2..5`), `\sum\prod(b_j{-}1)!=K!` (`K=1..8`) | all exact, PASS |
| §5.1 | 7776→19 classification + forest counts (+ `K=6`: 117649→30) | all exact, PASS |
| §5.1 | Lemma 3 polynomial identity `n=1..6` | exact, PASS |
| §5.1 | integral route = unified `f_r`; sum `=10x(1-x^2)^4`; general-`K` sum `K=1..12` | exact, PASS |
| §5.3 | machinery-free raw-7776 exact moments, 66+11 values | all exact matches |
| §5.2 | discrete mechanism, 3 scales | **0 mismatches / 555,000**; 7776/7776 cells at `n=25` |
| §5.2 | Lemma 1 discrete MC, 3 scales + follow-up | moments pass; 2 stray p-values resolved as chance (§6) |
| §5.2 | raw discrete full model `n=10^4,2\cdot10^4` | KS `p=0.37, 0.054`; `z=-0.67,-1.74` |
| §5.2 | continuum recipe MC 2M, per-group | overall `p=0.27`; groups 6/6 pass |
| §7 | reductions `K=1..4` group-by-group | exact match to all published groups |

No script was selectively rerun; every log corresponds to a single run
of its script (the one edit made after a run — the §6 item-1 harness fix
in `derive_assembly_k5_symbolic.py` — is disclosed below, and the script
was rerun in full afterwards, both results reported).

## 6. Self-caught issues (disclosed in the open)

1. **sympy `Piecewise` artifact in a check harness (not in any
   derivation).** The first run of `derive_assembly_k5_symbolic.py`
   Part E reported FAIL on the two *symbolic-`K`* binomial-identity
   checks. Diagnosis: `sympy.Sum(...).doit()` returns the closed form
   wrapped in `Piecewise(..., x<=1, ...)` (an artifact of its
   hypergeometric summation machinery; the sums are finite polynomials,
   so the identities hold for all `x`), and `simplify` cannot cancel a
   guarded branch against an unguarded target. Fix: extract the `x\le1`
   branch (our domain is `x\in(0,1)`) and compare; both identities then
   verify, and the second is additionally re-derived from the first two
   (`K\,s_1-s_2`). The identities themselves are the binomial theorem —
   the §4.3 proof never depended on sympy — and the general-`K` sum was
   independently verified exactly for `K=1..12` in the same run that
   first FAILed, so no mathematical content was ever at risk.
   **Log-preservation note (disclosed):** the rerun wrote to the same
   log filename, overwriting the failing first run's log — an oversight
   against best practice (the `K=2` front preserved its buggy first log
   under a separate name). The failing run's two FAIL lines were,
   verbatim, `FAIL Sum C(K,r) x^r = (1+x)^K (symbolic K)` and
   `FAIL Sum (K-r) C(K,r) x^r = K(1+x)^(K-1) (symbolic K)`, with every
   other line of that run PASS, identical to the preserved second log;
   the sympy output that caused them is reproducible in one line —
   `sympy.Sum(sympy.binomial(K,r)*x**r,(r,0,K)).doit()` returns
   `Piecewise(((x+1)**K, x <= 1), ...)`. The fix is visible in the
   script (`branch_at_x_le_1`).
2. **Two stray sub-`0.01` p-values in the Lemma-1 MC.** Among the 12
   statistics of `mc_lemma1_k5_check.py`: exchangeability KS(m1,m2) at
   `n=1000` gave `p=0.0039`, and KS(L) at `n=5000` gave `p=0.0085` —
   nominally below the registered `\alpha=0.01` for `n\ge1000`.
   Assessment before any further computation: (i) exchangeability of
   `(m_1,\dots,m_5)` holds *exactly* at every finite `n` by construction
   symmetry, so a genuine rejection could only indicate a code bug;
   moreover `ks_2samp`'s nominal p assumes independent samples, while
   `m_1,m_2` from the same trial are negatively correlated; (ii) a real
   discretization bias in `L` would have shown a *larger* deviation at
   `n=1000` (5× the bias), where `p=0.29`. Per the no-selective-rerun
   discipline the original results stand as reported; a pre-declared
   follow-up on **fresh** seeds at higher power
   (`mc_lemma1_k5_followup.py`: `n=1000`×40000 trials, `n=5000`×20000)
   gave `p=0.92` and `p=0.82` respectively — both flags resolve as
   chance, consistent with 12 partially-dependent tests.
3. **Pre-registration wording on `n=12` cell coverage.** The prereg said
   "full coverage expected at the small-`n` scales"; at `n=12` (30,000
   trials over 7776 cells) coverage was 6995/7776 — arithmetically
   unattainable in full at that trial count, an over-optimistic wording
   rather than a failed criterion (the registered *criterion* was zero
   mismatches plus honest coverage reporting; the scale that was sized
   for full coverage, `n=25`×500,000, achieved 7776/7776). Noted for the
   record.

## 7. Reductions to K=1,2,3,4 (exact, group by group)

The unified formula of §4.2, evaluated at `K=1,2,3,4`, reproduces
**exactly** every published, already adversarially-reviewed group
density of the lineage (`derive_assembly_k5_symbolic.py` Part D; all
reference polynomials transcribed from the lineage documents' prose and
built directly on the script's own symbol — never `sympify` from string,
per the `K=4` document's disclosed pitfall):

- `K=1`: `f_0=x`, `f_1=x` — `THEOREM.md` §5.3's two branches; sum `2x`.
- `K=2`: `f_0=2x(1-x)` (=group D), `f_1=2x(1-x^2)` (=B+C),
  `f_2=2x^2(1-x)` (=A); sum `4x(1-x^2)`.
- `K=3`: `3x{-}6x^2{+}3x^3`, `3x{-}9x^3{+}6x^4`, `6x^2{-}9x^3{+}3x^5`,
  `3x^3{-}6x^4{+}3x^5` — the `K=3` groups as tabulated in the reviewed
  lineage; sum `6x(1-x^2)^2`.
- `K=4`: all five `r`-groups of the `K=4` document's §4, verbatim; sum
  `8x(1-x^2)^3`.

## 8. Scope, honesty, and what remains open

**What is PROVED here.** `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` for **every**
`K\ge1` — the whole of `THEOREM.md` §8 Conjecture 1 — modulo exactly one
classical citation (below). Every previously per-`K` ingredient is now a
general theorem: Lemma 1a for every block size (§2.1), the telescoping
peel for every pattern (§2.2), the mechanism formula with no case split
(§3.1), the weighted-forest identity for every `n` (§3.2 — the route
Estágio 20 named), the two-term closed form and binomial-theorem sum
(§4.2–4.3). The `K=5` instance is additionally verified numerically at
the full pre-registered battery. As a corollary (§4.6), Conjecture 2
follows at the same tier; its cataloguing is left to the orchestrating
session.

**The one non-self-contained input.** Exactly as at `K=1,2,3,4`: the
`PD(1)` size-biased/residual property (McCloskey 1965; Patil–Taillie
1977; Pitman 2002 Ch. 3), applied recursively — up to `R-1\le K-1` peels
for the all-singletons pattern (four at `K=5`). Iterating the
self-similar residual property finitely many times is the multi-step
GEM(1)/stick-breaking representation — the same single citation, used
the number of times the construction calls for, as both prior referees
explicitly verified for two and three peels. The identification of the
whole-space model with §5.1's conditional model likewise carries the
same already-accepted status (Proposition 2.4's citation) as everywhere
in this line. Anyone auditing `THEOREM.md`'s Stage 1 core, or the
accepted `K=2,3,4` documents, already accepts these; nothing here asks
for more trust than that.

**On the honesty of the "general K" claim.** The mandate required not
claiming general `K` unless every step is genuinely `K`-uniform. The
audit of each step: Lemma 0 — never mentions `K`. Lemma 1a — proved for
symbolic `b`. §2.2 — a single induction over peels with an explicit
telescoping factor; the only `K`-dependence is the exponent bookkeeping
`1+(b_j-1)+(K-c_j)=K-c_{j-1}`, an identity. §2.3 — a bijection, proved
for symbolic `K`. Lemma 2 — a node-chain argument on a finite functional
graph, no `K`-specific enumeration. Lemma 3 — Prüfer, symbolic `n`.
§4.1–4.3 — exact cancellations, Beta integrals, and the binomial
theorem, all with symbolic `K`/`r`. No step enumerates cases whose
number grows with `K`; the `K=5`-specific enumerations in §5 are
*verification*, not proof. The numerical support is strongest at `K\le5`
(exhaustive) with uniformity spot-checks at `K=6` (classification,
forest identity) and `K\le12` (symbolic sum); the proof itself does not
lean on any of them.

**What remains open (unchanged by this document).** The `n\to\infty`
bridge for the *distribution* (as opposed to the mean, which is Theorem
3's line) is a different kind of statement and is not addressed here —
same separation `THEOREM.md` §8 itself draws. The other open items of
the wave-17 dispatch (sharp rate re-assembly, joint two-point
exploration as an *independent* route, plateau resummation, `\gamma`
scaling law) are untouched; note the two-point front's target
`E[M_K^2]=1/(K+1)` is now proved unconditionally as a byproduct (§4.5),
though the *joint exploration machinery* it was chartered to build
remains its own open problem. **No claim of progress on any Millennium
Problem** — this is pure combinatorial mathematics internal to this
archive's random-permutation-with-reroutes ensemble.

## 9. Scorecard

| Item | Status |
|---|---|
| `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` for **every** `K\ge1` | **PROVED** (modulo §2.2's citation, applied recursively ≤`K-1` times) |
| `f_{M_5}(x)=10x(1-x^2)^4` (the mandated instance) | **PROVED** (same status; exhaustively verified numerically) |
| Lemma 1 general-`K` (density `K!` on `\Delta_K`) | PROVED modulo the citation; telescoping proof, no per-`K` cases |
| Lemma 1a (labeled spacings, every `b`) | PROVED (unit-Jacobian ordering cells; verified `b=2..6`) |
| `\sum\prod(b_j-1)!=K!` | PROVED (bijection; verified `K=1..8`) |
| Mechanism formula `M=1-Q-\sum_{C}P_j` (Lemma 2) | PROVED, `K`-uniform, subsumes the referees' sub-case; 0/555,000 discrete mismatches |
| Weighted-forest identity `W(n)=e(e+Q)^{n-1}`, all `n` (Lemma 3) | **PROVED** (Prüfer) — the Estágio-20 candidate route, closed; verified `n=1..6` |
| Unified per-`r` closed form + binomial sum (§4.2–4.3) | PROVED (symbolic `K`); verified `K=1..12` |
| `E[M_K]=\varphi_K`, `E[M_K^2]=1/(K+1)` (all `K`); `E[M_5^3]=256/3003` | PROVED (new beyond `K\le4`) |
| Conjecture 2 (`M(c)\overset{d}{=}\min(1,\sqrt{E/c})`) | **Corollary** of the Theorem + §5.1's cited conditioning (§4.6); cataloguing left to orchestrator |
| Reductions to `K=1,2,3,4`, group by group | PROVED, exact match to all published groups |
| Machinery-free exact raw-7776 surface (66+11 moments) | all exact matches (second independent route for every coefficient) |
| Numerical battery (mechanism, 3 MCs + follow-up) | all registered criteria pass; 2 stray p-values resolved as chance (§6) |
| `n\to\infty` distributional bridge | not addressed (different kind of statement, per `THEOREM.md` §8) |

**This document's net result: `THEOREM.md` §8 Conjecture 1 is (subject
to the mandatory adversarial review) PROVED for all `K`** — closing the
`K=5` mandate and the stretch goal in one `K`-uniform argument, with
Conjecture 2 following as a corollary — ready for the standing
adversarial-referee requirement this archive applies to every positive
finding before any catalogue update to `THEOREM.md`.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `mechanism_check_k5.py` | `20260860001`, `20260860002`, `20260860003` | reserved `20260860000+` |
| `discrete_k5_full_distribution_mc.py` | `20260860010`, `20260860011` | reserved `20260860000+` |
| `mc_lemma1_k5_check.py` | `20260860020`, `20260860021`, `20260860022` | reserved `20260860000+` |
| `mc_lemma1_k5_followup.py` | `20260860023`, `20260860024` | reserved `20260860000+` |
| `mc_recipe_check_k5.py` | `20260860030` | reserved `20260860000+` |

No seed outside this front's reservation was used; the referee range
`20260861000+` is untouched.

## Files table

| File | Role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any script ran |
| `derive_lemma1_general_symbolic.py` / `.log` | Lemma 1a (`b=2..6`), telescoping peels (all patterns `K=2..5`), partition identity (`K=1..8`) (§2, §5.1) |
| `enumerate_destination_combinatorics_k5.py` / `.log` / `.json` | 7776→19 classification, forest counts, `K=6` check (§5.1) |
| `forest_identity_check.py` / `.log` | Lemma 3 exact polynomial identity, `n=1..6` (§3.2, §5.1) |
| `derive_assembly_k5_symbolic.py` / `.log` | integral route, unified form, sum, moments, reductions, general-`K` sum (§4, §5.1, §7) |
| `raw7776_exact_moments_k5.py` / `.log` / `.json` | machinery-free exact `Fraction` moment surface (§5.3) |
| `mechanism_check_k5.py` / `.log` / `mechanism_check_k5_results.json` | discrete per-configuration mechanism check (§3.1, §5.2) |
| `mc_lemma1_k5_check.py` / `.log` / `.json` | Lemma 1 discrete-permutation MC (§5.2) |
| `mc_lemma1_k5_followup.py` / `.log` / `.json` | pre-declared higher-power follow-up on the two flagged statistics (§6) |
| `discrete_k5_full_distribution_mc.py` / `.log` / `.json` | raw discrete full-model MC (§5.2) |
| `mc_recipe_check_k5.py` / `.log` / `.json` | continuum recipe MC, per-group KS (§5.2) |
| `ATTEMPT.md` | this document |
