# Pre-registration: continuum-native Theorem J (`JOINT-EXPLORATION-CONTINUUM-ATTEMPT`)

> Governance: wave 18, front (c), authorized by `DISC-DEC-078` in
> `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Written before
> any non-trivial code runs, per mandate.

## Target

Complete (or honestly fail to complete, with a genuinely new diagnosis)
a **continuum-native** version of Theorem J (Estágio 25: `THEOREM.md`
§7.2's finite conditional-`K` model, Definition 4 — conditional on
`C(f)=c`, `f|_c` uniform over `Sym(c)`; Corollary — the 50/50
same/different-final-cycle split given both cyclic), stated directly in
terms of Definition 3's primitives / `L(c)`, per the mandate's two
acceptable routes: (1) a from-scratch continuum construction, or (2) a
rigorous `n→∞` *transfer* of the already-proved finite theorem — these
are explicitly different questions and I will be clear about which one
I attempt.

## What I already know from required reading (not to be re-litigated,
only cited)

- Estágio 18 §3.3 / Estágio 25 §6.3: the obstruction to route (1) is
  that Definition 3 is a *marginal* single-point abstraction
  (`(Θ_j,E_j)` hazard-clock primitives) that discards the physical
  destination information a genuine simultaneous two-point exploration
  needs. This is not re-attacked head-on here (both fronts tried and
  stalled on exactly this; a third blind attempt at the same
  construction is not "a genuinely new angle").
- Theorem J's Corollary is an **exact algebraic identity at every
  finite `n,K`**: `P_n^{(K)}(\text{same},\text{both}) =
  \tfrac12 P_n^{(K)}(\text{both cyclic})`, not merely an asymptotic
  fact. This is the lever I intend to use.
- Estágio 24 proved the general-`K` cyclic-mass density
  `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` **directly in the continuum model
  `L(c)`** (a whole-space computation on Definition 2/PD(1) primitives,
  *not* via a finite-`n\to\infty` limit), hence
  `E[M_K^2]=1/(K{+}1)` is an already-PROVED continuum fact for every
  `K`, and by the Fubini identity `THEOREM.md` §2.4 already uses,
  `E[M_K^2] = P(x_1,x_2\text{ both cyclic in }L(c)\mid K)` for two
  independent uniform points — i.e. the "hard half" (the total
  both-cyclic probability) of the continuum two-point law is *already
  known exactly*, obtained by a route (whole-space mass distribution)
  that never needed a joint two-point exploration construction at all.

## The angle I intend to attack (new, not a restatement)

**Route 2 (transfer), attempted via a new reduction.** Since Theorem
J's Corollary is an *exact* identity at every finite `n,K`, dividing
through and passing to the limit is legitimate **for free**, with no
new joint-exploration machinery, *provided* the purely scalar quantity
`P_n^{(K)}(\text{both cyclic})` (a second-moment fixed-`K` bridge, the
finite-`n` analogue of the already-known continuum value
`E[M_K^2]=1/(K{+}1)`) converges to it as `n\to\infty`. This is a
**different, narrower, and — I will argue — more tractable open lemma**
than "construct a joint exploration on `L(c)`": it is a marginal-type
(scalar, not joint-dynamics) convergence statement, structurally
parallel to `THEOREM.md` §7.4's *already-solved* first-moment fixed-`K`
bridge (Estágio 3–6), just for the second factorial moment
`E[C(C-1)]/(n(n-1))` instead of the first moment `E[C]/n`.

**Plan:**
1. State this reduction as a precise proposition (mixing-free, an
   exact identity at each `n`, so the only content is the limit
   claim) — analogous in spirit to `THEOREM.md` Proposition 3, but far
   simpler since Theorem J removes the need to separately track "which
   cycle."
2. Attempt to prove the second-moment fixed-`K` bridge directly by
   exact finite-`n` combinatorics, generalizing `THEOREM.md`
   Proposition 4's `K=1` method (which computed the *first*-moment
   fixed-`K=1` bridge exactly, `φ_n^{(1)}=2/3+1/(3n^2)`) to the
   *two-point* joint quantity at `K=0,1`, and see how far a similar
   direct approach reaches for `K\ge2` (expect it to get harder, same
   general reason the marginal case needed the full `g_r(m,b)`
   machinery of Estágio 3–6 to close `K\ge2`, not attempted to
   completion here — that machinery is large and reusing/adapting it
   fully is out of scope for this front's budget; what is in scope is
   getting the *reduction* exactly right, proving `K=0,1` exactly, and
   giving an honest account of what a general-`K` closure would need).
3. Cross-check every exact closed form against fresh exhaustive
   enumeration (small `n`), and check the `n\to\infty` limit and rate
   match the already-proved continuum target `1/(K{+}1)`.
4. If the general-`K` bridge is not closed (expected, given budget), an
   honest diagnosis of exactly what's missing — and, separately, an
   explicit statement of what a *full* continuum-native two-point
   *exploration process* (route 1, not attempted from scratch again
   here) would still be needed for beyond this: namely, anything about
   `L(c)` that is not expressible as a *scalar mixture over `K` of
   already-known whole-space facts* — e.g. the *local/geometric*
   structure of the two-point exploration (where the split happens
   physically on the circle), which Theorem J's route intentionally
   never touches even at finite `n` (the Corollary is a bare
   probability, not a construction).

**What would count as success here.** A rigorous continuum-level
statement `P(x_1,x_2\text{ same final cycle in }L(c)) =
\tfrac12 E[M(c)^2] = \tfrac{1-e^{-c}}{2c}` (mixing the fixed-`K` result
over Poisson(`c`), *if* the fixed-`K` second-moment bridge closes for
every `K`) — obtained by transfer, not by a from-scratch continuum
exploration process. Partial success: the reduction itself (stated and
proved), plus exact closure at `K=0,1`, plus a precise account of what
blocks `K\ge2`.

**What would NOT count, and I will not claim it:** reusing Theorem J's
Corollary to claim anything about the *physical/geometric* two-point
exploration process on `L(c)` itself (e.g. "where" on the circle two
points end up relative to marks) — that remains exactly Estágio 18/25's
open problem, untouched by this route, and I will say so explicitly.

## Numerics discipline

Reserved seed range: `20260874000`–`20260875000` (referee range
`20260875000+` not used, no referee dispatched). Exact finite-`n`
combinatorics use no randomness at all (arbitrary-precision integer /
`fractions.Fraction` enumeration, as `THEOREM.md` Proposition 4 and the
parent `ATTEMPT.md` both do); any Monte Carlo cross-check of the
`n\to\infty` transfer in the large-`n` regime will use seeds from the
reserved block, grep-confirmed unused first.

## Non-negotiables

- No edits to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`.
- No `adversarial/` subdirectory, no referee dispatch.
- No git commands.
- All work confined to this new subdirectory.
- Full, precise PROVED/CITED/OPEN labeling in the final `ATTEMPT.md`,
  with an honest verdict either way.
