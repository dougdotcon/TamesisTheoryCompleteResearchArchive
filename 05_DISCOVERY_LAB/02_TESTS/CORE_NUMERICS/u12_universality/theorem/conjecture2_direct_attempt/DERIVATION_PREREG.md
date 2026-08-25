# Pre-registration — CONJECTURE-2-DIRECT-ATTEMPT

Written and saved before any script in this directory ran. Timestamp:
2026-08-25T17:32Z.

## Governance

Wave 16, front (e), authorized by `DISC-DEC-066` in
`05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`. Seed budget
reserved for this front: `20260858000+` (confirmed unused by
`grep -rn "20260858"` across the archive before first use — the only
prior hits were the two reservation lines in `DECISION_LEDGER.yaml` and
`TEST_QUEUE.yaml`). Referee-reserved range `20260859000+` will **not**
be used by this front.

## What this front will attempt

`THEOREM.md` §8 Conjecture 2: `M(c) \overset{d}{=} \min(1,\sqrt{E/c})`,
the Poisson(c)-mixture of Conjecture 1 over `K`. The task is to attempt
a **direct** proof — one that does not go through proving Conjecture 1
case-by-case for every `K` (infeasible, since `K=1,2,3` are proved but
no case-by-case route can ever reach "every `K`").

Three structural routes will be attempted, in this order:

1. **Moment method via `p`-point joint exploration.** Generalize
   Theorem 1's own device (`E[M(c)] = \int_0^1 P(x\text{ cyclic})\,dx`,
   via Fubini, computed by a *single-point* exploration that never
   fixes `K`) to `E[M(c)^p] = \int_{[0,1]^p} P(x_1,\dots,x_p\text{ all
   cyclic})\,dx_1\cdots dx_p`. Since `M(c)\in[0,1]` is bounded, the
   moment problem is determinate (Hausdorff), so if all moments could
   be computed this way and shown to match `\min(1,\sqrt{E/c})`'s
   moments, that would be a genuine, fully `K`-free proof. Attempt at
   minimum the `p=2` (second moment / variance) case, structurally.
2. **Is `\{M(c)\}_{c\ge0}` Markov in `c`** under the natural
   Poissonization coupling (realize all `c` simultaneously via a single
   rate-1 marked process on `[0,1)\times[0,\infty)`, `c` = "time")? If
   so, a master/generator equation for the *marginal* law of `M(c)`
   might close directly. Attempted as a genuine yes/no structural
   question, with a concrete example if the answer is no.
3. If both fail to close, name **precisely** why, distinguishing the
   obstruction(s) found from the already-known K-by-K combinatorial
   explosion that blocks Conjecture 1.

## Discipline

Every claim below will be labeled PROVED, CITED, NUMERICALLY EXPLORED
(honest exploratory numerics informing an open sub-problem — not
offered as evidence toward a proof), or OPEN. Numerical checks against
the *already-established* KS/mean evidence for Conjecture 2 (§8 of
`THEOREM.md`) will not be presented as new evidence toward Conjecture 2
itself; any numerics here either (a) validate a *new* construction or
identity introduced in this document, or (b) are explicitly flagged as
exploratory data informing a stated open sub-problem. An honest
non-closure — a precise structural explanation of the obstruction — is
stated in advance as a fully acceptable outcome, per `DISC-DEC-066`(e)'s
own dispatch language. No file outside this directory will be modified.
No `adversarial/` subdirectory will be created by this front.

## Anticipated seed usage

`20260858000+`, incrementing per distinct numerical check, allocated in
the order the checks are written (recorded exactly, with no
after-the-fact reordering, in the Seeds table of `ATTEMPT.md`).
