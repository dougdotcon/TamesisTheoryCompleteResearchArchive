# Pre-registration — CONJECTURE-1-K5-GENERAL-ATTEMPT (wave 17, front (a), DISC-DEC-072)

Written and saved **before any script in this directory ran** (timestamp
`2026-08-25T22:00Z`; every script/log in this directory postdates this
file). Target: `THEOREM.md` §8 Conjecture 1 at `K=5`
(`f_{M_5}(x)=10x(1-x^2)^4`), and — stretch goal, only if every step is
genuinely `K`-uniform — the general-`K` case
`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`. Honest non-closure is a pre-declared
acceptable outcome. Seed budget: `20260860000+` (this front), confirmed
unused before first use (`grep -rn "20260860" 05_DISCOVERY_LAB/` returned
only the three reservation lines in `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`). The referee range
`20260861000+` will NOT be used by this front. No script of any prior
front or referee is read or imported — everything is re-derived and
re-implemented from the prose of `THEOREM.md` and the lineage
`ATTEMPT.md`/`REFEREE_REPORT.md` documents only.

## Planned derivation route (registered before computing)

The route is the lineage's whole-space method, with the two per-`K`
ingredients replaced by genuinely `K`-uniform arguments:

1. **Lemma 1, general `K` (uniform simplex law).** Claim to prove:
   `(m_1,…,m_K)` has constant joint density `K!` on
   `Δ_K={m_i>0, Σm_i<1}`. Route: sequential block peeling over the
   co-block set partition; the peel-`j` factor is
   `(b_j−1)!·(1−s_j)^{K−c_j}/(1−s_{j−1})^{K−c_{j−1}}`
   (`s_j`=cumulative block length, `c_j`=cumulative block size), which
   **telescopes** to `∏_j(b_j−1)!` for every pattern; summing over set
   partitions gives `K!` by the partition↔permutation bijection
   (`Σ∏(b_j−1)!=K!`). Sub-ingredient to prove uniformly in block size
   `b`: the labeled circular spacings of `b−1` i.i.d. uniform free
   points plus one anchor on a circle of circumference `ℓ` are jointly
   `ℓ·Dirichlet(1,…,1)` (density `(b−1)!/ℓ^{b−1}`), by the
   per-cyclic-ordering unit-Jacobian change of variables summed over
   `(b−1)!` orderings. The classical citation (size-biased pick of
   `PD(1)` is `Unif(0,1)`; residual after size-biased deletion is fresh
   rescaled `PD(1)`, applied recursively — multi-step GEM(1)) is the
   SAME single citation the whole lineage uses; at `K=5` it is used up
   to **four** peels (one more than `K=4`'s three).

2. **Off-cycle-zero + mechanism formula, `K`-uniform.** Claim: with
   `g:{1..K}→{1..K,OUT}` the region-level redirect map and `C` the set
   of nodes on cycles of `g`, the cyclic mass is exactly
   `M_K = (1−Σ_{i=1}^K m_i) + Σ_{j∈C}(m_j−P_j)`, `P_j` the landing
   offset of the unique on-cycle redirect into region `j`. Route: the
   forward-orbit/node-chain argument (an off-cycle node `k`'s own orbit
   visits regions `k,g(k),g²(k),…` and `g^t(k)≠k` for all `t≥1`, so
   region `k` is never revisited) — this subsumes the "landing inside an
   already-periodic arc" sub-case flagged by the `K=3`/`K=4` referees,
   with no case split at all.

3. **Off-cycle weight, ALL `n` at once (the named candidate route).**
   Claim to prove: `W(n)=e·(e+q_1+…+q_n)^{n−1}` as a polynomial
   identity, where `W(n)` sums, over all maps from `n` off-cycle nodes
   to (regions/OUT) with no cycle inside the off-set, the product of
   target masses (`q_i`=own-region masses, `e`=combined external mass).
   Route: acyclic-map ↔ rooted-forest ↔ tree-rooted-at-external
   bijection + the **Prüfer-sequence** proof of the weighted Cayley
   formula (each vertex `v` appears `deg(v)−1` times in the Prüfer
   code). At `e+Q=1` this degenerates to `W=1−Q` for every `n` —
   `E(E+Q)^{n−1}=E`, exactly the identity Estágio 20 names.

4. **Assembly, general `K`.** For on-cycle set `C`, `|C|=r`,
   `n_off=K−r`: joint density `K!·r!·(1−Q)` in
   `((P_j,D_j:=m_j−P_j)_{j∈C},(m_i)_{i∉C})` after summing over the `r!`
   internal permutations; marginalizing gives (registered prediction)

   `f_r(x) = C(K,r)·x^r·(1−x)^{K−1}·[K−(K−r)(1−x)]`,

   valid for ALL `r=0,…,K` (the `r=0` and `r=K` edge cases included),
   and the binomial-theorem sum

   `Σ_{r=0}^K f_r(x) = 2Kx(1−x^2)^{K−1}` exactly, for every `K≥1`.

## Registered numerical predictions (K=5 unless stated)

- Bell(5)=52 co-block patterns; by integer-partition type
  `5 / 4+1 / 3+2 / 3+1+1 / 2+2+1 / 2+1+1+1 / 1^5`:
  multiplicities `1,5,10,10,15,10,1` (sum 52), constants
  `24,6,2,2,1,1,1`, contributions `24+30+20+20+15+10+1 = 120 = 5!`.
- `Σ_{partitions}∏(b_j−1)! = K!` for `K=1..8`: `1,2,6,24,120,720,5040,40320`.
- Labeled-spacings density constant `(b−1)!/ℓ^{b−1}` for `b=2,3,4,5`
  (and `b=6` as a beyond-target check).
- Destination classification of all `6^5=7776` raw maps: shape-type
  count `Σ_{s=0}^5 p(s)=1+1+2+3+5+7=19`; per-`r_on` raw counts
  `1296,2160,2160,1440,600,120` (sum 7776), via
  `C(5,r)·r!·N(r,5−r)` with `N(r,n)=(r+1)(r+1+n)^{n−1}`;
  `N(r,n_off)` constant across every specific on-set/cycle-type choice.
  Beyond-target check at `K=6`: `7^6=117649` raw maps, `30` shape types.
- Forest identity `W(n)=e(e+Q)^{n−1}` as exact polynomial identity in
  distinct symbolic masses for `n=1..6` (`n=5` is the case `K=5` needs;
  `n=6` beyond target); unit-weight counts `(n+1)^{n−1} = 1,3,16,125,1296,16807`.
- Per-`r` densities at `K=5` (from the registered unified formula):
  `f_0=5x(1−x)^4`, `f_1=5x(1−x)^4(1+4x)`, `f_2=10x^2(1−x)^4(2+3x)`,
  `f_3=10x^3(1−x)^4(3+2x)`, `f_4=5x^4(1−x)^4(4+x)`, `f_5=5x^5(1−x)^4`;
  sum `= 10x(1−x^2)^4 = 10x−40x^3+60x^5−40x^7+10x^9`.
- Per-`r` probabilities: `P(r=0..5) = 1/6, 5/14, 25/84, 5/36, 1/28,
  1/252` (sum `= 252/252 = 1`).
- Moments: `E[M_5]=256/693=φ_5` (must equal the §5.2 Wallis value
  `4^K(K!)^2/(2K+1)!` at `K=5` — independent target), `E[M_5^2]=1/6`
  (consistent with Estágio 18's `1/(K+1)` target), `E[M_5^3]=256/3003`.
- Reduction: the unified `f_r` formula at `K=1,2,3,4` must reproduce the
  already-proved group-by-group densities of §5.3 / Estágio 15 / 17 / 20
  exactly (e.g. `K=4`: `4x(1−x)^3, 4x(1−x)^3(1+3x), 6x^2(1−x)^3(?)…` —
  computed symbolically in the script, compared against the published
  polynomials of the `K=4` document transcribed as sympy expressions
  built with the script's own symbol, never `sympify` from string, per
  the `K=4` document's disclosed pitfall).
- General-`K` sum check: symbolic verification `Σ_r f_r = 2Kx(1−x^2)^{K−1}`
  for `K=1..12`.
- Machinery-free exact check: per-`r` moments `E[M^p·1{r_on=r}]`,
  `p=0..10`, computed over the raw 7776 configurations with
  `fractions.Fraction` (no collapse machinery), must match the exact
  integrals `∫x^p f_r dx` — since `deg f_r ≤ 9`, matching `p=0..9`
  already pins the polynomials uniquely; `p=10` is margin.

## Registered acceptance criteria for the numerical checks

- **Mechanism check (discrete, per-configuration exact match):**
  `M_pred = #{points in source-free π-blocks} + Σ_{i∈cyc(g)}(D_i+1)`,
  `D_i`=discrete distance from `u_i` forward to its region's source.
  Criterion: **0 mismatches** at every scale; report raw-cell coverage
  per scale honestly (7776 cells; full coverage expected at the small-`n`
  scales given the trial counts, not guaranteed at `n=150`).
  Scales/seeds: `n=12`/30000 trials/seed `20260860001`;
  `n=25`/500000/`20260860002`; `n=150`/25000/`20260860003`.
- **Lemma 1 discrete MC:** moments `E[m_i]=1/6`, `E[m_i^2]=1/21`,
  `Cov(m_i,m_j)=−1/252` (all `|z|<3`); KS of `L=Σm_i` vs `t^5`, pooled
  `m_i` vs `Beta(1,5)`, exchangeability — expected small-`n`
  discretization rejection at `n=300` (the lineage's standard signature)
  with clean convergence (no rejection at `α=0.01`) by `n=1000,5000`.
  Seeds `20260860020/021/022`, `n=300/1000/5000`, trials
  `15000/10000/6000`.
- **Raw discrete full-model MC:** KS vs `F(x)=1−(1−x^2)^5`, no rejection
  at `α=0.01` at `n=10000` (4000 trials) and `n=20000` (2000 trials);
  mean consistent with `256/693` (`|z|<3`). Seeds `20260860010/011`.
- **Continuum recipe MC:** `N=2,000,000`, seed `20260860030`; overall KS
  no rejection at `α=0.01`; per-`r_on` group fractions vs the registered
  probabilities (`|z|<3.5` across 6 tests); per-group KS vs the
  registered conditional densities, no rejection at `α=0.01` across 6
  tests.

Any failed criterion, and any bug caught along the way, will be reported
in the open in `ATTEMPT.md`, per the archive's standing discipline.
