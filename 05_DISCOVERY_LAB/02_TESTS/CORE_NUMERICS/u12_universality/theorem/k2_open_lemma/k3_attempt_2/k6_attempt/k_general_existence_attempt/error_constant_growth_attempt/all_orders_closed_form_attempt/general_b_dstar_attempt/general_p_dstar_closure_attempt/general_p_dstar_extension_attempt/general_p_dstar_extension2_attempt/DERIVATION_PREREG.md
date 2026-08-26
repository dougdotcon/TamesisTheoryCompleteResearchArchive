# Pre-registration: `D^{*(p)}_r(b)` general-`p` closure, `p>20`

> Wave 18, front (a), `GENERAL-P-DSTAR-EXTENSION2-ATTEMPT`, authorized by
> `DISC-DEC-078`. Written **before** any non-throwaway verification run,
> per this archive's standing pre-registration discipline (mirrors
> `general_p_dstar_closure_attempt/DERIVATION_PREREG.md` and
> `general_p_dstar_extension_attempt/DERIVATION_PREREG.md`, both read for
> structure only — not their content, since neither addresses `p>20`).

## 1. What is being computed

The same target as every predecessor in this lineage: the sharp error
constants `D^{*(p)}_r(b)` in the closed-form family

`D^{*(p)}_r(b) = Phi^{[p]}_r(1,b) = sum_{j=p}^{r} c_j^{(r)}(b) * c(j+1, j+1-p)`,

(Corollary A3 of `all_orders_closed_form_attempt/ATTEMPT.md`, PROVED,
cited, not re-derived), via the general-`p` assembly algorithm proved and
executed for `p=1..10` (`general_p_dstar_closure_attempt`, wave 15) and
`p=11..20` (`general_p_dstar_extension_attempt`, wave 16, referee-approved
`DISC-DEC-070`). This front extends the **same, unchanged** algorithm to
`p=21` and beyond, as far as computationally reasonable.

Nothing in the mathematical content changes. This is an execution front,
not a new-theory front — exactly the classification the wave-16 front
carried and the ledger's dispatch text for this front confirms ("item
aberto apenas por não-executado, risco baixo").

## 2. What is cited as fixed, already-PROVED input (not re-derived)

- Corollary A3 itself.
- `Q_p(u)`'s degree/vanishing and its Newton's-identity computation
  method (closure attempt §2.1/§3.1, wave 15).
- The cumulant-generating-function definition of `mu_{2l}(N)` and the
  power-series-exponentiation recurrence extracting it (closure attempt
  §2.2; extension attempt §2.1, wave 16).
- `(E1)`: `Phi_b(r) = P_b * 2^N` (closure attempt §3, `(E1)`).
- `(E2)`: `P_b * C(N-j, r-j+1) = [r]_j / ([N]_j * (r-j+1))` (closure
  attempt §2.3, PROVED, elementary).
- The referee's (wave-15 referee, `general_p_dstar_closure_attempt`'s
  `adversarial/REFEREE_REPORT.md`) general-`k` odd-power identity and its
  inductive proof that `H(power,depth)` — as literally defined by the
  `(E2)`-based recursion — equals `P_b * S_power(N-d, r-d)` for **every**
  `(power, d)`, not just values checked numerically. This is the
  load-bearing fact behind this front's low-risk classification.
- The wave-16 referee's **additional, stronger** result (this front's
  direct predecessor's own referee,
  `general_p_dstar_extension_attempt/adversarial/REFEREE_REPORT.md` §2a-2b):
  a closed factorization `S_{2k-1}(N,m) = A_k(N,m) * C(N,m+1)` (with
  `(m+1) | A_k`), proved by induction on `k` from the same cited
  recursion, and the **proved** degree bound
  `deg_r H_{2k-1}(r,b) = k-1` with leading coefficient `4^{k-1}(k-1)!`,
  independent of `b`, verified there symbolically (`b` symbolic) for
  `k=1..20`. This upgrades the degree bound this front's `H_k`
  interpolation route will rely on from "empirically confirmed" (wave 16's
  own status) to fully PROVED — a strictly stronger starting point than
  either predecessor had.
- The assembly formula itself (closure attempt §2, reproduced verbatim by
  the extension attempt §1, reused verbatim again here):

  `N := 2r+b+1`, `beta := b+1`,

  `D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)] - sum_{k=1}^{p} o_k * H_{2k-1}(r,b) / 2^{2k-1}`,

  with `Q_p(-(v+beta/2)) = E_p(v) + O_p(v)`, `e_{2l}`, `o_k` its
  coefficients, `M_p(N) := sum_l e_{2l} mu_{2l}(N)`,
  `Strip_p(r,b) := sum_{i=1}^{b} E_p(i-beta/2) w_i(r,b)`,
  `w_i(r,b) := r!(r+b)! / [(r+i)!(r+b+1-i)!]`,
  `H_{2k-1}(r,b) := P_b * S_{2k-1}(N,r)`.

None of the above will be re-derived from scratch; each will be re-coded
fresh (own scripts, no import of any predecessor `.py` file — the task
mandate forbids reading predecessor scripts at all, so this is also a
hard constraint, not just a style choice) and spot-checked for internal
consistency, per this lineage's standing convention.

## 3. Target scale

Fixed floor, matching or exceeding the wave-16 predecessor:

- **`p = 21, ..., 30`** (ten new values, doubling this document's own
  minimum ambition relative to the ledger's floor language "aim for at
  least p=21..30, more if computationally tractable").
- If timing allows (checked empirically before committing, exactly as the
  wave-16 front's own §0 exploratory-timing discipline), push further,
  **`p = 31, ..., 40`**, as a stretch target — reported honestly either
  way, not forced.
- **`r = 0, ..., 200`, `b = 0, ..., 30`** per `p` value, matching the
  wave-16 predecessor's own scale (the largest reached anywhere in this
  lineage) — attempted uniformly, not shrunk with growing `p`, unless
  timing data collected in §0-style exploration shows this is genuinely
  infeasible, in which case any reduction will be reported explicitly and
  its cause named (cf. wave-15's honest scale note for `p>=5`).

## 4. Method

Reuse, unchanged in mathematical content, the wave-16 predecessor's own
innovation: **fast ingredient extraction** for the two components whose
naive (`sympy`-generic) implementation does not scale —

- central moments `mu_{2l}(N)` via the power-series-exponentiation
  recurrence on `log cosh(t/2)` (classical, `Fraction`-exact, no `sympy`
  in the hot path);
- `H_{2k-1}(r,b)` via the **proved** closed factorization
  `S_{2k-1} = A_k * C(N,m+1)` (wave-16 referee's own new result, cited
  above) — a rational-function-of-`r,b` recursion for `A_k` alone, one
  level cheaper than either predecessor's own route (the closure attempt
  used raw `sympy.cancel`; the extension attempt used evaluate-then-
  interpolate; this front can use the referee's own proved factorization
  directly if it is fast enough, falling back to evaluate-then-interpolate
  — now backed by a **proved**, not merely empirical, degree bound — if
  the factorization route itself is slower in practice).

Every ingredient will be **cross-validated** against at least one
independent implementation route before being trusted for the main sweep,
exactly as both predecessors did (own from-scratch ground truth via
Corollary A3's Stirling-number recurrence; brute-force direct summation
of `S_{2k-1}` for small `k`; reduction to previously-PROVED calibration
formulas at `b=0,1` and the printed `b=2,3` instances from earlier
fronts).

## 5. Verification criteria

A `(p,r,b)` triple counts as **verified** iff the assembled closed-form
value equals the independent Corollary A3 ground-truth value **exactly**
(exact rational arithmetic throughout — `fractions.Fraction` and/or
`sympy.Rational`, no floating point in any non-throwaway check).

**Success tiers, declared in advance:**

- **Full success:** `p=21,...,30` (floor) closed and verified at
  `r<=200, b<=30` uniformly, `0` mismatches against ground truth, with
  every ingredient independently cross-validated per §4, matching or
  exceeding predecessor scale.
- **Stretch success:** the above, extended further to `p=31,...,40` or
  beyond, reported with the same rigor, only if timing genuinely permits
  without cutting corners on verification scale or exactness.
- **Partial/honest non-closure:** if any `p` in the target range fails to
  close at full scale (a genuine mismatch, not a timeout), it will be
  reported precisely — which `(p,r,b)` triples fail, and whether the
  failure traces to a bug (to be found and fixed if possible) or a
  genuine mathematical obstruction (not expected, given the wave-15
  induction and wave-16 degree-bound proof already establish the
  underlying machine is correct for every `k` — but this front will not
  assume that guarantees success at execution time; every claim is
  checked, not presumed). Given the governance dispatch's own low-risk
  classification and the fact that the underlying `H_k` machine is proved
  correct for *every* `k` (not just `k<=20`), a mismatch would be a
  genuine surprise and will be investigated exhaustively before any
  "OPEN" label is applied.

## 6. Randomness / seeds

This entire lineage (closure attempt, extension attempt) used **no
randomness** — every check is exact symbolic/rational algebra or an
exhaustive finite sweep. The same is expected here. **If** any randomized
check turns out to be useful (e.g. randomized spot-checks over a larger
`(r,b)` grid than exhaustive sweep affords, for extra assurance at the
stretch-target `p` values), it will use Python's `numpy.random.SeedSequence`
or `random.Random` seeded from the reserved range
**`20260870000-20260870999`** (front (a)'s reservation under
`DISC-DEC-078`; confirmed unused elsewhere in the archive by
`grep -rn "20260870" 05_DISCOVERY_LAB/` returning only the ledger's and
`DISCOVERY_LAB_STATE.md`'s own reservation lines, checked immediately
before this document was written). The referee range `20260871000+` will
not be touched by this front.

## 7. Honesty commitments

- Every claim will be labelled PROVED / CITED / NUMERICALLY VERIFIED /
  OPEN, per archive convention.
- Any self-caught bug will be disclosed in full, in the same style as the
  two predecessor fronts' own disclosures (`w_i` off-by-one, wave 15;
  `nsimplify` corruption, wave 16) — including exactly how it was caught,
  what it affected, and confirmation the fix does not silently mask a
  deeper issue.
- No `adversarial/` subdirectory will be created and no referee will be
  dispatched by this front — that is explicitly out of scope, reserved
  for the orchestrating session, per the task mandate.
- `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, and
  `DISCOVERY_LAB_STATE.md` will not be edited by this front.
- If `p=21..30` at the target scale turns out to be genuinely
  intractable in the time available, this will be reported as a scale
  limitation (naming the actual bottleneck, with timing data), not
  disguised as a mathematical obstruction, and the highest `p` actually
  reached at full verification scale will be stated precisely as the
  front's real result.
