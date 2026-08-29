# Hostile Referee Report — `BOUNDARY-LAYER-SELFHEAL-ATTEMPT` (wave 30, front c, `DISC-DEC-138`)

**Note on provenance.** This report is the verbatim final report returned
by the dedicated hostile-referee session dispatched for this front. That
session's own verification scripts were written and run in its working
scratchpad (outside this repository, per the orchestrating session's
dispatch instructions, which — unlike the parallel wave 30 front (a)
dispatch — did not request an `adversarial/` subdirectory be populated
inside the archive) and are not available to commit alongside this
report; their names and what each checked are listed in the "Files
referenced" section below, exactly as the referee reported them, but only
this report text itself is preserved in the archive. This gap is
disclosed honestly rather than silently omitted or backfilled with
fabricated scripts.

---

## VERDICT: **SOUND WITH ISSUES — all low severity (documentation/coverage framing only, zero mathematical error found)**

**The central claim is genuine and independently verified: `(U)` is proved conditional on `(B)`+`(C')` alone, with `(C'')` needed nowhere.** This is a real strengthening of the wave-29 predecessor's theorem, not a restatement, and it correctly resolves the predecessor's honestly-left-open "boundary-layer self-healing" question in the positive direction.

---

## Why I believe the escalation is genuinely sound (in my own words)

The crux is Sec 3.2's claim that `|Γ_u(h)-Γ(h)| ≤ 3·L1·u` needs only `(C')` (Lipschitz `f`), not `(C'')` (Lipschitz `f'`). I traced why this works and it is not a trick: the predecessor's route bounds the *pointwise* quantity `E(h',z) = ∫[f'(h'+u)-f'(h')]Q_u(z)du`, which is a genuine difference of two values of the *derivative*, and there is no way to control that without extra regularity on `f'` itself (Sec 4.2's adversarial-kink test in the predecessor honestly demonstrates this is a real, non-artifactual obstruction at the pointwise level). This front avoids that trap entirely by never forming a pointwise derivative-difference: it first converts `Γ_u(h)` and `Γ(h)` — each an integral *of* `f'` — into pure differences of `f`-*values* via the elementary FTC/IBP identity (Sec 2.1, valid for any Lipschitz/AC `f`, since Lipschitz functions satisfy the exact, not merely a.e., fundamental theorem of calculus). Only *then* does it subtract, giving `Γ_u(h)-Γ(h)` as three plain `f`-value differences, each between points at distance exactly `u` — bounded directly by `(C')`'s Lipschitz constant with no reference to `f'`'s fine structure at all. This is the mathematically correct reason the escalation is legitimate, not merely a numerically-observed coincidence: differentiating and then comparing loses information that integrating (via FTC) and then comparing does not. I re-derived every step of this by hand and it is exact.

## Independent verification performed

- **Sec 2.1 identity**, **Sec 3.2 core lemma** (algebra), **Sec 3.3 assembly** (`R''(z)=(1+z²)R(z)-z`, `∫u·Q_u(z)du=R''(z)/2` via Tonelli, `R''(z)≤2/z³` via two independent routes), and **Sec 3.4's final `D(x,eps)`** — all re-derived by hand from scratch; every one matches the document exactly, including the specific extra `1/eps` factor in the new `L1`-term (see Nota 3 below for why it's there and legitimate).
- **Sec 3.2's bound**, adversarially stress-tested with my own fresh code: a random search over 60 trials of 1–12-kink Lipschitz-1 functions with random weights/signs, sweeping `h,u,eps,x` into degenerate corners (`h→0`, `u→0`, `u` large) — zero violations, worst observed ratio `0.096` (comfortably below 1).
- **Sec 3.4's full theorem**, tested end-to-end against the RAW kernel operators (`K_A^raw`, `K_B`, `M_y`, not the front's own intermediate `ρ`/`E_full` formulas — the same rigor level as the predecessor's referee's `adv03`), on a genuinely non-`C¹` (kinked) globally-bounded Lipschitz test function, across `x∈{0,0.3,2.0}`, `eps∈{0.1,0.5,1.0}`, `z` from `3` to `302`, **including `h=y` (t=0)** — the maximal-`h` case the front's own numerics never probe (see Nota 2). Zero violations; ratios `0.0012`–`0.2`. (My first two attempts at this had a genuine bug of my own — a missing `e^{-h''/eps}` weight in the outer integral — caught and fixed before trusting the result; worth flagging since it shows how easy this exact class of mistake is to make, which is also why I checked the front's own code line-by-line rather than trusting prose alone.)
- **Sec 4 numerics**, reproduced with completely fresh, independently-written code: F1 (predecessor's single kink) matches to 4 significant figures (`z³|E_full|→0.9363` at `z=500`, vs. published `0.936`/referee's `0.9362995`). The **F3-style 8-kink geometrically-accumulating cluster pushed to `z=2500`** — the specific stress test flagged as highest-risk — reproduces to `z³|E_full|=1.5296` against the front's own `1.5310`, a `~0.1%` agreement, both comfortably inside the proved bound of `3.0`.
- **Self-caught issues** (Sec 5): both verified as genuinely present and correctly fixed in the committed code, not merely narrated — `s01_new_identities_symbolic.py` Part 2 does build the product rule by hand (`dexpo_du*R(u+z)+expo*Rprime_at_uz`) exactly as described, and `s03`'s dynamic per-evaluation kink-breakpoint design is genuinely present and matches the narrative.
- **Scope/governance**: `git status` confirms `boundary_layer_selfheal_attempt/` is the only new, untracked directory (sibling wave-30 fronts a/b are separately untracked and unrelated); no `adversarial/` subdirectory was created by this front; no `git`/`random` calls in any of its scripts; `DECISION_LEDGER.yaml` has no entry past `DISC-DEC-138`, consistent with "not yet integrated." Seed block `20260947000-20260947999` (`grep -rn "20260947" 05_DISCOVERY_LAB/`) appears only in `DECISION_LEDGER.yaml`'s own reservation line and this front's own prose — no collision. `PROOF_DEPENDENCY_MAP.md`'s cited `DISC-DEC-136` addendum text matches what this front quotes. `H1`/`(U1)`/`(U2)`/`(C')` are correctly and repeatedly stated as still OPEN; the front does not overclaim and does not re-attack `(C')` itself, honoring its narrow mandate.

## Issues found (all "nota" — clarifications, no correction needed)

1. **Nota — VERDICT item 1 / Scorecard row 2** ("`int u·Q_u(z)du=R''(z)/2`... matches a claim the predecessor's referee made but never itself derived in committed code"). This is ambiguously worded: the predecessor's referee's *own* script, `cu_direct_proof_attempt/adversarial/adv02_rho_and_E_routes.py` Part 2, **does** contain a full, numerically-verified derivation of this identity (confirmed to `<1e-30` relative error). The true state (per `DISC-DEC-136`'s own Finding 1, which this sentence is paraphrasing) is that the identity was never derived in the **predecessor front's own** `s01`–`s03` scripts — it was derived only in the referee's separate `adv02.py`. As written, a future reader could conclude it was never derived in any committed code anywhere in the lineage, which is false. A one-clause fix (e.g., "...never derived in the predecessor front's own `s01`–`s03`, only in the referee's `adv02.py`") would remove the ambiguity.

2. **Nota — Sec 4 / `s03`'s `H_CAP=15*eps` design**. The front's own decisive numerics (F1/F2/F3) fix the outer `h`-integration cutoff at a constant multiple of `eps`, independent of `y`/`z`, so they never numerically probe `h` close to `y` (the theorem's own claimed full range, `h∈[0,y]`) — even at the `z=2500` stress test, the tested `h` never exceeds `7.5`. This is disclosed as a deliberate numerical-efficiency choice with a correct analytic justification (the core lemma bound doesn't depend on `h`), so it isn't a hidden gap in the *proof* — but it does mean Sec 4's own numerics don't directly stress-test the full-`h` regime the theorem claims. I closed this gap independently (see above): the raw-kernel end-to-end check at `h=y` shows the bound holds there too, with comfortable margin.

3. **Nota — Sec 3.4's `D(x,eps)`**. The new `L1`-term (`3·L1·(1+eps)/eps`) carries an extra `1/eps` factor that the predecessor's structurally-parallel `L2`-term (`L2·(1+eps)`) lacked. I confirmed this is algebraically correct, not an error — the `eps`/`1/eps` cancellation that gave the predecessor's cleaner form happens, in this front's route, already *inside* the Sec 3.2 core-lemma bound (third term: `(1/eps)·L1·u·eps = L1·u`), so it isn't available a second time at the final assembly step. It doesn't affect the theorem's validity or its overall `O(1/eps)` order (the cited, unchanged `D1` piece already dominates that order), but it does mean this front's new bound is not uniformly tighter than the predecessor's old one in every `(L1,L2,eps)` regime (e.g., for `eps→0` with `L1≈L2`, the new residual term is asymptotically worse by a factor `~1/eps`). Not mentioned in the document; worth a one-line note since a future reader combining the two fronts' results (e.g., taking the sharper of the two bounds when both hypotheses happen to hold) should know this.

No issue rises to "correção" — I found no algebraic error, no unjustified inequality step, no numerical claim that failed to reproduce, and no case (including ones the front's own numerics don't cover) where the bound actually fails.

## Files referenced

- `05_DISCOVERY_LAB/.../cu_direct_proof_attempt/boundary_layer_selfheal_attempt/ATTEMPT.md` (document under review)
- `05_DISCOVERY_LAB/.../cu_direct_proof_attempt/boundary_layer_selfheal_attempt/s01_new_identities_symbolic.py`, `s02_Rpp_bound_numeric.py`, `s03_Efull_bound_stress_test.py`, `s04_core_lemma_direct_check.py`, `s05_assembly_arithmetic_symbolic.py` (and matching `.log`s)
- `05_DISCOVERY_LAB/.../cu_direct_proof_attempt/ATTEMPT.md` (predecessor) and `.../cu_direct_proof_attempt/adversarial/REFEREE_REPORT.md` (+ `adv02_rho_and_E_routes.py`)
- `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml` (`DISC-DEC-134`, `-136`, `-138`)
- `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/PROOF_DEPENDENCY_MAP.md`
- The referee's own scratch verification scripts (not part of the archive — see provenance note above): `ref02_adversarial_core_lemma_search.py`, `ref06_fixed_final.py`, `ref07_efull_reproduction.py`

No Millennium Problem claims anywhere in the target or this report; pure
mathematical analysis internal to this archive.
