# Pre-registration — `GENERAL-P-DSTAR-EXTENSION-ATTEMPT`

Written before any non-throwaway verification run in this directory, per
standing archive discipline. Timestamp: 2026-08-25, wave 15/16 follow-on
front, dispatched as an execution-only extension of
`general_p_dstar_closure_attempt/ATTEMPT.md` (target: item 11 of
`general_b_dstar_attempt/ATTEMPT.md`'s scorecard, already closed for
`p=1,...,10` and, by the closure attempt's referee, proved correct for
**every** `k` in the underlying `H_k(r,b)` machine by induction).

## Target

Run the same, already-validated general-`p` algorithm for `D^{*(p)}_r(b)`
further: `p=11,...,20` if computationally tractable. **No new mathematics.**
Every ingredient (`Q_p` via Newton's identities; central moments via the
cumulant-generating-function Taylor extraction; the `H_k(r,b)` machine via
`(E1)`/`(E2)` and the cited `S_{2k-1}` recursion) is reused exactly as
established and adversarially confirmed in `general_p_dstar_closure_attempt/`.

## Method (planned before any code is run)

Read `general_p_dstar_closure_attempt/ATTEMPT.md` and its
`adversarial/REFEREE_REPORT.md` in full first (done). Reuse their route
verbatim. Before committing to a verification scale for `p=11,...,20`,
**time the closure attempt's own implementation** (`ingredients.py`'s
`central_moment`, `odd_part.py`'s `H_reduced_at_b`) at the powers this
extension will need, to find the actual computational frontier honestly,
rather than assuming `p=20` is free just because the referee proved the
underlying machine correct for all `k`.

**Planned honesty checkpoint:** if the closure attempt's own symbolic
routes (`sympy.series`+`exp` for moments, `sympy.cancel` for `H_k`) turn
out to scale too poorly to reach `p=20` in reasonable time, this document
will not silently stop at whatever `p` those routes happen to reach.
Instead, before declaring a frontier, it will check whether a
**mathematically-identical, faster extraction of the same two objects**
(central moments via the classical power-series-exponentiation recurrence
for `exp(N f(t))`, i.e. `m g_m = sum_k k h_k g_{m-k}` — the same textbook
algorithm class as Newton's identities already used for `Q_p`; `H_k(r,b)`
via evaluation of the *same* `H(power,depth)` recursion at concrete,
sufficiently-large integer `r` followed by exact Lagrange interpolation,
mirroring the closure attempt's own `H_reduced_at_b` performance variant
and the referee's own Lagrange-interpolation cross-check route for `Q_p`
and the moments) closes the gap — **and if so, will use it, cross-validated
character-for-character against the original (slow) symbolic route at
every order where the slow route is still tractable, before relying on it
at any new order.** This is a performance-engineering choice about *how*
to extract Taylor/interpolation data from the *same* generating functions
and the *same* recursion — not a new derivation, not a new ingredient, and
not a relaxation of exactness (both routes use only exact `Fraction`/
`sympy.Rational` arithmetic, zero floating point).

**Exploratory timing (already run, informing the plan below, in
`/tmp/.../scratchpad/`, not part of this directory's non-throwaway record):**
the closure attempt's own `central_moment` (sympy cumulant-GF series) costs
grow from `12.1s` (`l=10`, i.e. `mu_20`, needed for `p=10`) to `45s`
(`l=11`) to `158s` (`l=12`) — clearly too slow to reach `l=20` (`p=20`) in
reasonable time. The closure attempt's own `H_reduced_at_b` (`sympy.cancel`)
costs grow from `4.5s` (`power=19`, `k=10`, needed for `p=10`) to `50s`
(`power=21`) to `99s` (`power=25`) to `171s` (`power=27`) — also clearly
too slow to reach `power=39` (`k=20`, needed for `p=20`). The fast
power-series-exponentiation recurrence for moments and the fast
evaluate-then-interpolate route for `H_k` were built and cross-validated
against these slow routes (character-for-character, `l=1..10` for moments,
`power=1..19` at four `b` values for `H_k`, `0` mismatches in every case)
**before** being adopted for production use in this directory.

## Success criteria (stated in advance)

- **Strong target:** `p=11,...,20`, general-`p` algorithm (same as the
  closure attempt's), each verified exactly against an independent
  Corollary-A3 ground truth at whatever `(r,b)` scale is computationally
  reasonable given the genuinely higher polynomial degree (expected to
  shrink monotonically as `p` grows, exactly as it did `p=1\to10` in the
  closure attempt).
- **Honest fallback:** if a genuine computational wall is hit before
  `p=20` (not expected, given the timing above, but not ruled out — e.g.
  ground-truth Stirling-number computation itself, or `sympy.factor` for
  presentation, could still be a bottleneck independent of the two
  ingredients timed above), stop there and report exactly why, with timing
  evidence, distinguishing this explicitly from any mathematical doubt
  (there is none — the referee's induction already covers every `k`).

## Ground truth

Own from-scratch Corollary A3 implementation (`ground_truth.py`), same
recurrence as the closure attempt's own (`c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k)`),
written fresh in this directory, not imported.

## Exactness policy

`sympy.Rational` / `fractions.Fraction` throughout. No floating point
anywhere in this directory's non-throwaway code.

## Randomness / seeds

No randomness needed anywhere in this front (exact symbolic algebra and
exhaustive finite sweeps only). Reserved seed range `20260854000+` per the
task's dispatch instructions; confirmed unused elsewhere in the archive
before this file was written (`grep -rn "20260854" 05_DISCOVERY_LAB/`
returns only the ledger's/queue's own reservation lines for this front).
Not expected to be needed, exactly as in the closure attempt.

## Files planned

- `DERIVATION_PREREG.md` — this file.
- `ground_truth.py` / `.log` — independent Corollary A3 implementation.
- `ingredients_ext.py` / `.log` — `Q_p(u)` (Newton's identities, unchanged
  from the closure attempt, already fast to `p=20`), central moments
  `\mu_{2l}(N)` via the fast power-series-exponentiation route,
  cross-validated character-for-character against the closure attempt's
  slow `sympy` cumulant-GF route (`l=1..10`) and against direct binomial
  summation, before use at `l=11..20`.
- `odd_part_ext.py` / `.log` — the `H_k(r,b)` machine via the *same*
  `H(power,depth)` recursion and `(E1)`/`(E2)`, extracted via
  evaluate-then-interpolate, cross-validated character-for-character
  against the closure attempt's slow `sympy.cancel` route at every power
  where the slow route is tractable, before use at higher `k`.
- `assemble_ext.py` / `.log` — full assembly for `p=11,...,20` (or as far
  as tractable), checked against `ground_truth.py` at scale; explicit
  printed closed forms for representative new `p`.
- `ATTEMPT.md` — final report, this front's deliverable.

No file outside this directory will be created, modified, or deleted. No
git operation will be performed. `THEOREM.md`, the decision ledger, and
every sibling attempt's files will not be touched. No `adversarial/`
subdirectory will be created here — referee dispatch is out of scope for
this front, per the task's instructions.
