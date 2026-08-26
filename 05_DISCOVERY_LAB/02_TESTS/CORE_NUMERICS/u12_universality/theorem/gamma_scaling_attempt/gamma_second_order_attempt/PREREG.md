# PREREG — `GAMMA-SECOND-ORDER-ATTEMPT` (wave 18, front (b), `DISC-DEC-078`)

**Target.** Prove rigorously, for `γ∈(0,1)`, the second-order constant

`√n·(φ(n,γn)/φ_∞(γn) − √(2/(2−γ))) → C(γ) = −(2/(3√π))√γ(6−8γ+3γ²)/(2−γ)²`

left as CONJECTURED (not proved) by the wave-17 front's Estágio 23
§7.3, whose own derivation is an admittedly non-rigorous
Taylor-expansion-then-sum heuristic.

## Intended approach

1. **Reformulate.** Using the wave-17 front's own exact machinery
   (Lemma 1: `nφ(n,γn)=S_n:=Σ_{k=1}^n A_k`, `A_k=E_{M∼Bin(k,γ)}[P_{k,M}]`;
   `φ_∞(γn)=L_n−R`, `R` exponentially small; `(G_n/n)/L_n=√(2/(2−γ))`
   exactly), show `C(γ)` is **equivalent** to a clean deterministic
   statement about `S_n` alone: `S_n = G_n + D(γ) + o(1)` for an
   explicit `D(γ)`, with `D(γ)=−(1/3)(6−8γ+3γ²)/(2−γ)²` (this reduces
   correctly to the archive's own `Q(n)=√(πn/2)−1/3+O(n^{-1/2})` at
   `γ=1`, giving `D(1)=−1/3`, a first consistency check computable by
   hand before any code is run).
2. **Split** `S_n = Σ_k e^{-s(k)} + Σ_k[A_k−e^{-s(k)}]` (`s(k)` exactly
   as defined in the wave-17 front, §2), and attempt to control each
   piece to `O(1)` (i.e. relative order `n^{-1/2}`) separately:
   - The first piece is a **purely deterministic** Gaussian-type sum
     with no residual randomness (`M` has been replaced by its mean).
     Working hypothesis: this piece is tractable by classical,
     fully-elementary tools already one tier below anything cited in
     the wave-17 front — specifically Poisson summation / the Jacobi
     theta transformation, which gives an *exact*, exponentially-precise
     evaluation of `Σ_{k≥1}e^{-ak²}`. If this hypothesis holds, this
     piece closes with a **PROVED** closed form `D_0(γ)`.
   - The second piece carries all the leftover randomness (the
     Binomial fluctuation of `M` around `γk`) and is expected to be the
     hard part — a generalization of exactly the mechanism behind the
     archive's own `Q(n)=√(πn/2)−1/3+...` (Robbins 1955 + FGKP95),
     which is itself a nontrivial, dedicated, non-elementary classical
     result (not reproved from scratch anywhere in this archive, only
     cited). Working hypothesis: this piece will **not** close
     rigorously within this front's scope, because (a) it needs an
     Edgeworth-level (not just CLT/Hoeffding-level) expansion of a
     Binomial average, uniform as `k→∞`, which is a strictly sharper
     tool than anything this archive currently cites, and (b) even
     granting such a tool, the interchange of the `k`-sum and the
     `n→∞` limit needs a non-asymptotic (FGKP95-style) bound, not a
     formal term-by-term Taylor argument, exactly the gap the wave-17
     front already disclosed for the *whole* conjecture and that this
     decomposition is designed to localize to *only* this one piece.
3. **Numerically test** the decomposition itself (does
   `D(γ)=D_0(γ)+E(γ)` actually hold, with `D_0` from step 2's closed
   form and `E:=lim_n Σ[A_k−e^{-s(k)}]` estimated by high-precision
   direct summation + Richardson extrapolation) — an independent check
   of the wave-17 front's conjectured `C(γ)`, via a genuinely different
   route (a structural split) rather than a repeat of their direct
   `√n(R_n−target)` extrapolation.
4. **Attempt** a second-order (Edgeworth) heuristic re-derivation of
   `E(γ)` via moments of `M∼Bin(k,γ)` (mirroring, independently, the
   kind of computation the wave-17 front sketched for the whole
   quantity) to see whether a closed form for `E(γ)` falls out that
   matches the numerics, while being explicit and honest that this
   step, like theirs, will not be rigorous (interchange of expansion
   and summation, uniform error control) unless a specific rigor gap
   can be closed along the way.

## Honest-non-closure criteria (declared in advance)

This attempt will be written up as an **honest non-closure** (not a
full proof) if, after the above, the "hard part" (`E(γ)` / the
Edgeworth piece) is not rigorously closed — this is considered the
**a priori likely outcome** given (a) the wave-17 front already
disclosed the identical obstruction for the undecomposed quantity, and
(b) `E(1)` is *itself* the content of a dedicated 1995 journal paper
(FGKP95) generalizing Ramanujan, not a from-scratch derivation anywhere
in this archive — reproving *and generalizing* a result of that
caliber from scratch is not a realistic bar for a single front. In
that case the deliverable is: (i) the `D_0(γ)` piece PROVED in closed
form (real, if partial, progress — strictly more than the wave-17
front closed, since they left the *entire* second-order term
unproved), (ii) `E(γ)` pinned down numerically to good precision and
shown consistent with the wave-17 front's conjectured `D(γ)−D_0(γ)`,
(iii) a precise statement of exactly which classical tool is missing
and why the `γ=1` proof technique (Robbins+FGKP95, which is a
*deterministic*-product argument, no Binomial averaging) does not
survive the introduction of the `M∼Bin(k,γ)` average for `γ<1`, named
at the level of specificity of the archive's own reference
non-closures (e.g. Estágio 18 of `THEOREM.md`).

Success (full proof of `C(γ)` on `(0,1)`) would instead require finding
and correctly applying/citing an Edgeworth-type expansion theorem for
`E_{M∼Bin(k,γ)}[h(M)]` (`h` the relevant exponential functional),
uniform in `k→∞`, with a non-asymptotic error bound sufficient to
justify the `k`-sum/`n→∞` interchange — this will be attempted but is
not expected to close within scope.

## Seeds

Reserved block: `20260872000–20260873000` (this front only; referee
range `20260873000+` not used, no referee dispatched per mandate).
Only used for an independent direct Monte-Carlo simulation of
Definition 1 as a sanity check on `A_k`/`S_n` at moderate `n` — every
other numerical check in this front is exact/deterministic (Fraction
or mpmath arithmetic), consuming no randomness.

## Discipline

No `.py` script of any prior front (wave 17 front (e) or its referee)
will be opened, read, or imported. Every evaluator is written fresh
from the mathematical description in `ATTEMPT.md`'s and
`REFEREE_REPORT.md`'s prose. `THEOREM.md` and `DECISION_LEDGER.yaml`
are read-only. No `adversarial/` subdirectory, no referee dispatch, no
git commits.
