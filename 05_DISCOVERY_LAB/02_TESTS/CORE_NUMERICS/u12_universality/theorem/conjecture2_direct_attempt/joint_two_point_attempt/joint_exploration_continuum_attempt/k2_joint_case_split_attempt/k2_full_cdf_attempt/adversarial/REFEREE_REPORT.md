# Adversarial referee report: `K2-FULL-CDF-ATTEMPT` (Proposição D2 and its predecessors)

**Target document:** `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/
conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/
k2_joint_case_split_attempt/k2_full_cdf_attempt/ATTEMPT.md`

**Referee posture:** hostile/adversarial, dispatched to try to refute the claims, not confirm
them. Every script in this directory was written **from scratch**, from mathematical prose
only (`THEOREM.md`'s prose, `ATTEMPT.md`'s prose, and the K=2 predecessor's
`k2_joint_case_split_attempt/ATTEMPT.md` prose). **No `.py` file from `k2_full_cdf_attempt`,
`k2_joint_case_split_attempt`, `k3_joint_structural_attempt`, `k3_full_cdf_attempt`,
`general_k_joint_attempt`, or any other ancestor front was opened, read, or imported** at any
point while writing these scripts.

Pure combinatorial mathematics about the u12 random-permutation-with-reroutes ensemble
defined in `THEOREM.md` Definitions 1–4. **This is not a Millennium Problem and no claim of
that kind is made anywhere below.**

---

## Verdict

> **SOUND — ACCEPT for catalogue.**

No mathematical error was found anywhere in `ATTEMPT.md`. Every headline claim (Proposição S,
the Full Cycle-Count Decomposition Theorem, the conditional CDF, Proposição D2 itself, and all
five corollaries D2.1–D2.5) was independently re-derived and/or re-verified by methods
genuinely different from the front's own, and every one of those independent checks matched
exactly, with zero discrepancies. Two informational (BAIXA) findings are named below; neither
affects the validity of any claim.

---

## Reading discipline (§1 of the mandate)

Read in full, this session, before writing any code:

- `ATTEMPT.md` (the target document), in full.
- `THEOREM.md` "Estágio 3" (lines 1401–1487): the cited K=2 marginal-bridge mean formula
  `φ_n^(2) = 8/15 + 1/(30n) + 7/(10n²) + 1/(5n³)`. **Transcription check: accurate** — this is
  exactly what `ATTEMPT.md` §5.2/§1.1 cites.
- `THEOREM.md` "Estágio 15" (lines 2994–3109): the K=2 continuum density
  `f_{M_2}(x) = 4x(1-x²)`, `E[M_2]=8/15`, `E[M_2^2]=1/3`, proved directly on the continuum
  object. **Transcription check: accurate.**
- `THEOREM.md` "Estágio 24" (lines 4018–4199ish): the general-`K` continuum theorem
  `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` and `E[M_K^2]=1/(K+1)` for all `K`, giving `1/3` at `K=2`.
  **Transcription check: accurate.** (Note: the value `8/35` for `E[M_2^3]` does **not** itself
  appear verbatim anywhere in `THEOREM.md` — `ATTEMPT.md` §5.3–5.4 is honest about this,
  stating it is "computed here directly from `f_{M_2}(x)=4x(1-x^2))`," not citing it as a
  pre-established `THEOREM.md` fact. This is correct and not a citation error.)
- `THEOREM.md` "Estágio 27" (lines 4445–4552): Proposição D0, Lemma R, Proposição D1
  (`P(M_n^{(1)}≤k/n)=k(k+1)/n²`), Lemma P2 — the K=1 template `ATTEMPT.md` mirrors.
- `THEOREM.md` "Estágio 40" (lines 6003–6120), in full: the K=3 predecessor (Proposição S with
  the `(1-p_u)` third-source factor, the Full Cycle-Count Decomposition Theorem, Proposição D3,
  its corollaries, its own adversarial verdict). **Cross-check: `ATTEMPT.md`'s claim that its
  own Proposição S is "exactly the K=3 formulas... with `p_u=0`" was independently verified**
  by reading `k3_full_cdf_attempt/ATTEMPT.md`'s own statement of Proposição S
  (`P(S={s,t})=2p_sp_t(1-p_u)`, `P(S={s})=p_s(p_s+p_D)`) — setting `p_u=0` in the pair formula
  gives exactly `2p_0p_1`; the singleton formula has no explicit `p_u` term to begin with
  (already absorbed into `p_D`), so it is unchanged — both consistent with `ATTEMPT.md`'s claim.
- `k2_joint_case_split_attempt/ATTEMPT.md`, in full (prose only): Lemma 1 (Marked-Point Gap
  Structure Lemma, general `m`, cited by `ATTEMPT.md` for its `m=2` instance), Lemma 2, and the
  document's own honest §7.2 diagnosis naming the full CDF as the strictly-harder unattempted
  target this front closes. **Cross-check: `ATTEMPT.md`'s restatement of the arc/notation
  matches** (its `ARC(0)`/`ARC(1)`, ending at the respective source, is the predecessor's
  `arc_2`/`arc_1` under a renaming — same underlying object, no discrepancy).

## Seed range

Grep-confirmed, before using any seed: `grep -rEn "\b20260923[0-9]{3}\b" 05_DISCOVERY_LAB/`
returns only (a) the governance reservation lines in `DECISION_LEDGER.yaml` and
`DISCOVERY_LAB_STATE.md`, and (b) `k2_full_cdf_attempt`'s own files, which already use only
`20260923001`–`20260923003`. My assigned sub-range `20260923500`–`20260923799` is confirmed
**unused** anywhere in the archive. Two seeds from it were used, each for an independent
randomized self-test (not for anything load-bearing to the verdict):

| script | seed | purpose |
|---|---|---|
| `position_level_reference.py` | `20260923501` | random cross-check of the closed-form `paircount()` against its slow `O(A)`-loop reference, 20,000 cases |
| `mean_and_moments_check.py` | `20260923502` | numeric sanity scan of Corollary D2.5's bound over a dense `(n,x)` grid |

---

## Independent checks performed, and results

### (a) True brute force of Definition 4 itself — pushed to `n=10`

`true_bruteforce.py`: written directly from `THEOREM.md`/`ATTEMPT.md`'s statement of
Definition 4 (uniform `π`, `U_0,U_1` i.i.d. `Unif([n])`, `f(0)=U_0, f(1)=U_1`, `f(i)=π(i)`
otherwise, `T`=# cyclic points of the functional graph `f`), using a from-scratch 3-color
cycle detector — no arc/decomposition machinery of any kind, genuinely the rawest possible
check. Enumerates **every** `(π,U_0,U_1)` triple exactly (`n!·n²` of them), exact integer
counts, then compares `P(T≤k)` against Proposição D2's formula as a `Fraction`.

Result: **`n=2` through `n=10`, every `k`, exact match, zero mismatches** — `54` total
rational comparisons (one per `k=0..n-1` at each `n`, `35` for `n=2..8` + `9` at `n=9` + `10`
at `n=10`), drawn from `8+54+384+3000+25920+246960+2580480+29393280+362880000` exhaustively
enumerated configurations respectively. This matches the front's own reach (`n=10`, with a
comparable wall time of ≈11 minutes for the `n=10` run) and confirms every single value the
front reports in its own §6.1–6.2 table, independently.

Logs: `bruteforce_n2to8.log`, `bruteforce_n9.log`, `bruteforce_n10.log`.
Script: `true_bruteforce.py`.

A hand-derivation sanity check (not scripted) was also done for `n=2`: since both points are
reroute sources, `π` is entirely irrelevant and `f=(U_0,U_1)` directly; the four `(U_0,U_1)`
combinations give `T∈{1,2,2,1}`, reproducing the script's raw counts `[0,4,4]` exactly under the
`n!=2`-fold multiplicity from `π` — confirms the cycle-detector's correctness on the base case
independently of the script itself.

### (b) Proposição S and the Full Cycle-Count Decomposition Theorem — re-derived from raw first principles

**Proposição S:** `prop_s_symbolic.py` independently re-derives the raw 9-case
`(dest(0),dest(1))∈{0,1,D}²` functional-graph trace from scratch (its own `cyclic_explicit`
routine, not copied from `ATTEMPT.md`'s own case listing), aggregates by resulting `S`, and
symbolically confirms, via `sympy`, all four closed forms
(`P(S=∅)=p_D`, `P(S={0})=p_0(p_0+p_D)`, `P(S={1})=p_1(p_1+p_D)`, `P(S={0,1})=2p_0p_1`) with
**zero symbolic discrepancy**, plus confirms the four probabilities sum to `1`.
Log: `prop_s_symbolic.log`.

**Decomposition Theorem / conditional CDF:** `position_level_reference.py` builds an
independent **position-level reduced model** directly from the arc-tail mechanics described in
`ATTEMPT.md` §1.2/§2 (positions `e_1..e_{L0}` of `ARC(0)`, `d_1..d_{L1}` of `ARC(1)`, default
`π`-successor edges within each arc, tail edges redirected by `U_0,U_1`'s landing class), using
its own from-scratch cycle detector on this small functional graph — **not** using the "`V_s`
uniform, mutually independent" claim as an input anywhere; that claim is exactly what this
model tests. This was:
1. Spot-checked against the paircount-based conditional-CDF formula transcribed from
   `ATTEMPT.md` §3, at 8 `(n,L0,L1)` configurations, every `k` — **70/70 exact matches**.
2. Averaged over the whole `(L0,L1)` composition simplex (raw, no shortcuts) and compared
   against Proposição D2's closed form directly, `n=2..25,28,30`, every `k`, **with the
   `k=n-1` boundary explicitly checked and reported separately at every `n`** — **382/382
   exact matches, zero mismatches, boundary included every time.**
3. A second, faster layer (`large_n_check_via_validated_formula`) sums the same
   already-validated conditional-CDF formula (validated against the raw model in step 1)
   directly over the simplex using an independently-derived **closed-form** `paircount` (whose
   correctness was itself cross-checked against 20,000 random cases against the slow `O(A)`
   loop version — `self_test_paircount()`), reaching much larger `n` — `n=40,60,80,100,130,160,
   200`, every `k`, **388/388 exact matches.**

Total for this layer: **840 exact rational comparisons, zero mismatches.**
Log: `position_level_reference.log`. Script: `position_level_reference.py`.

**Full symbolic re-derivation of D2 itself**, via a genuinely different route than the front's
own "shift trick" (`s:=v+w` substitution): `symbolic_D2_rederivation.py` derives `PairAgg(m,t)`
by directly swapping the order of the raw `(L0,v,w)` triple sum (no substitution trick), derives
`S1(t,m,O,n)` by directly splitting the sum at `L0=t`, confirms both against `ATTEMPT.md`'s own
transcribed closed forms (**zero symbolic diff**) and against direct `O(m)` numeric
recomputation (**654 numeric comparisons, zero mismatches**), then assembles and sums
`Contribution(O)` over `O=0..k` to re-derive regime (i)'s closed form **from scratch**,
confirming it equals **both** `ATTEMPT.md`'s own transcribed regime-(i) formula and the
Proposição D2 headline formula, with **zero symbolic difference**.
Log: `symbolic_D2_rederivation.log`.

### (c) The "single regime, no boundary case" claim at `k=n-1`

Verified two independent ways:

1. **Symbolically, from scratch** (`symbolic_D2_rederivation.py` Step 5): regime (ii)
   (`k=n-1`, `O` summed `0..n-2`) was derived **independently of regime (i)'s already-derived
   formula** — i.e. not by substituting `k=n-1` into the regime-(i) result, but by re-running
   the entire `Contribution(O)`-summation machinery with `k` fixed to `n-1` from the start.
   Result: `F_regime_ii = 1 - 2/n²`, matching `ATTEMPT.md`'s claimed `(n²-2)/n²` exactly
   (`diff=0`), **and** matching `F_regime_i(k=n-1)` exactly (`diff=0`) — confirming the
   single-formula claim genuinely, not just by algebraic coincidence of one substitution.
2. **Numerically, at every `n` checked** (`position_level_reference.py`'s `large_n_check`):
   the boundary value `k=n-1` is checked and reported explicitly and separately at every one of
   `n=2..25,28,30` — all match, including `n=2`'s single-composition edge case.
3. **By true brute force**, `k=n-1` is included in every one of the `n=2..10` full checks in
   (a) above — all match.

### (d) Mean recovery, Corollary D2.2 — "zero symbolic remainder"

`mean_and_moments_check.py`: independently integrates Proposição D2 via the standard identity
`φ_n^{(2)} = 1 - (1/n)·Σ_{k=0}^{n-1} F(k)`, and compares the result against `φ_n^{(2)} = 8/15 +
1/(30n) + 7/(10n²) + 1/(5n³)` **transcribed from `THEOREM.md` Estágio 3, independently re-read
in this session** (not from `ATTEMPT.md`'s own transcription of it). **Result: `diff=0`,
confirming zero symbolic remainder exactly as claimed.**

As a bonus, this same script independently re-derives the **exact finite-`n`** second- and
third-moment formulas (not just their `n→∞` limits) directly from Proposição D2:

```
E[(M_n^(2))^2] = 1/3 + 1/(30n) + 13/(15n^2) + 11/(30n^3) + 1/(5n^4)
E[(M_n^(2))^3] = 8/35 + 1/(35n) + 101/(105n^2) + 97/(210n^3) + 23/(70n^4) + 1/(35n^5)
```

These match `ATTEMPT.md`'s own §5.3–5.4 formulas **term for term, exactly** — a stronger,
independent confirmation than just the `n→∞` limits the mandate asked for. The `n→∞` limits
(`1/3`, `8/35`) were confirmed via `sympy.limit`, and `E[M_2^3]=8/35` was independently
re-integrated from `THEOREM.md` Estágio 15's density `f_{M_2}(x)=4x(1-x^2)` (not from
`ATTEMPT.md`'s own arithmetic), matching exactly.
Log: `mean_and_moments_check.log`.

### (e) Corollary D2.5's convergence-rate inequality chain

`mean_and_moments_check.py` (same script, second half): independently substitutes `k=xn` into
Proposição D2, `sp.cancel`s against the independently-integrated continuum CDF
`F_2(x)=1-(1-x²)²`, and reproduces `ATTEMPT.md`'s claimed numerator/denominator
`N(n,x)=-nx^4-nx^2+2nx+x^2-3x`, `n(n-1)` exactly (`diff=0` both). The bound `|N(n,x)|≤4n+4` on
`[0,1]` was checked **not just via the coefficient-sum heuristic `ATTEMPT.md` uses**, but via
**exact calculus** (critical points of each `n`-power's coefficient polynomial in `x`, found via
`sp.diff`/`sp.solve`): `max|coeff_{n^1}(x)|` and `max|coeff_{n^0}(x)|` on `[0,1]` both confirmed
`≤4` exactly. The arithmetic chain `n(n-1)≥n²/2` (for `n≥2`) and `8/n²≤4/n` (for `n≥2`,
equality exactly at `n=2`) were both checked directly (not just asserted), confirming the final
bound `|F_n(x)-F_2(x)|≤12/n` is valid, with the `n=2` step tight (not slack). A dense numeric
scan (`n=2..50`, 200-point grid, seed `20260923502`) found **worst observed ratio
`|gap|/(12/n) ≈ 0.1667`** — matching the front's own reported `≈0.167` almost exactly, an
independent confirmation of that number too, and confirming no violation anywhere on the scan.
Log: `mean_and_moments_check.log`.

---

## Findings

### BAIXA (informational, no effect on validity) — 2 findings

**F1.** `ATTEMPT.md`'s §5.3–5.4 phrase "matches the already-proved continuum values `1/3` and
`8/35`" could be misread as claiming `8/35` itself is a pre-existing `THEOREM.md` fact (like
`1/3` genuinely is, via Estágio 24's `E[M_K^2]=1/(K+1)`). It is not — `8/35` does not appear
anywhere in `THEOREM.md`. The document is, on close reading, honest about this ("computed here
directly from `f_{M_2}(x)=4x(1-x^2)`, Estágio 15/24, cited"), so this is a labeling-clarity
observation, not a citation error: the *density* `f_{M_2}` is the cited fact, `8/35` is this
document's own elementary integral of it. No correction needed to the math; a reader skimming
only the Executive Summary bullet (item 5) rather than §5.3–5.4's fuller sentence could get the
wrong impression of what's cited versus computed here.

**F2.** The comparison claim in §6.1 ("`n=9` already exceeds the K=3 front's own brute-force
reach (`n=8` there)") was independently spot-checked by reading `k3_full_cdf_attempt/
ATTEMPT.md`'s own file table, which does list `true_bruteforce_full_cdf_k3.py` as reaching only
`n=3..8` — confirming the comparison is accurate. Flagged here only as a due-diligence note
(this is a cross-front comparison claim, not a mathematical claim about the u12 ensemble
itself), not as an error.

No MODERADA or ALTA findings.

---

## What this report does not (re-)verify

- The Monte Carlo bonus (§6.4 of `ATTEMPT.md`) was not independently re-run — it is explicitly
  disclosed there as "triangulation only, not proof," consistent with lineage convention, and
  is not part of the mandate's five targeted checks (a)–(e).
- Corollary D2.5's *sharper* asymptotic constant `≈0.7107/n` (the `g_1(x)=x(2-x-x^3)`
  leading-order term) was algebraically confirmed to match the coefficient-of-`1/n` term derived
  independently in `mean_and_moments_check.py` (`coeff_n1(x) = -x^4-x^2+2x`, which factors to
  exactly `x(2-x-x^3)`), but its claimed numeric maximum `≈0.7107` was not separately
  re-optimized — `ATTEMPT.md` itself discloses this constant is *not* proved as a uniform
  finite-`n` bound, only the cruder `12/n` is, and that cruder bound is what this report fully
  verified in (e) above.
- Predecessor citations (`k2_joint_case_split_attempt`'s Lemma 1/Lemma 2, `THEOREM.md`
  Estágios 3/15/24/27/40) were read in full and cross-checked for transcription accuracy
  (all accurate, see "Reading discipline" above) but their own internal proofs were not
  re-derived here — they are out of scope for this front's mandate and were independently
  reviewed by their own dedicated referees already on record in `THEOREM.md`.

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `true_bruteforce.py` | fresh, independent, fully-exhaustive Definition-4 K=2 ground truth, `n=2..10`, exact `Fraction` arithmetic, from-scratch cycle detector |
| `bruteforce_n2to8.log` / `bruteforce_n9.log` / `bruteforce_n10.log` | raw transcripts, checks (a) |
| `prop_s_symbolic.py` / `.log` | independent raw 9-case symbolic re-derivation of Proposição S, check (b) |
| `position_level_reference.py` / `.log` | independent from-scratch position-level reduced model (Decomposition Theorem / conditional CDF), simplex-averaged reference engine to `n=200`, checks (b)/(c) |
| `symbolic_D2_rederivation.py` / `.log` | independent full symbolic re-derivation of Proposição D2 via a different summation order than the front's own "shift trick," plus the independent from-scratch regime-(ii)/boundary derivation, checks (b)/(c) |
| `mean_and_moments_check.py` / `.log` | independent mean recovery (D2.2), exact finite-`n` 2nd/3rd moment re-derivation (D2.3/D2.4), and full rate-bound inequality-chain verification (D2.5), checks (d)/(e) |

## Seeds used (sub-range of this front's own reservation, confirmed unused before use)

Reserved sub-range: `20260923500`–`20260923799`.

| script | seed | purpose |
|---|---|---|
| `position_level_reference.py` | `20260923501` | random cross-check, closed-form `paircount()` vs. slow loop, 20,000 cases |
| `mean_and_moments_check.py` | `20260923502` | numeric sanity scan of Corollary D2.5's bound |

---

## Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, `index.html`, or the front's
own `ATTEMPT.md`. No `git` command run. All work confined to this `adversarial/` subdirectory.
No `.py` file from any front in this lineage (`k2_full_cdf_attempt`, `k2_joint_case_split_
attempt`, `k3_joint_structural_attempt`, `k3_full_cdf_attempt`, `general_k_joint_attempt`, or
any other ancestor) was read, opened, or imported — every script here is written fresh from
mathematical prose only. No claim of progress on any Millennium Problem; pure internal
combinatorics on this archive's own random-permutation-with-reroutes ensemble.
