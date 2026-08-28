# Adversarial referee report: `K4-FULL-CDF-ATTEMPT` (Proposição D4 and corollaries)

**Target document:** `k4_full_cdf_attempt/ATTEMPT.md`.
**Referee posture:** hostile — the task was to try to refute the claims,
not confirm them. No `.py` file from this front or any ancestor/sibling
front (`k4_full_cdf_attempt`, `general_k_joint_attempt`,
`general_k_decomposition_attempt`, `pnn_general_k_egf_attempt`,
`k3_full_cdf_attempt`, `k3_joint_structural_attempt`,
`k2_full_cdf_attempt`, `k2_joint_case_split_attempt`, or any other) was
read. Every script in this directory was written completely from
scratch, from THEOREM.md's own prose (Definition 4, Estágios 7, 20, 24,
40, 41, 42) and ATTEMPT.md's stated closed-form formulas only.

## Verdict

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

No mathematical error was found anywhere in the document. Proposição D4
(the headline result), all five corollaries (D4.1–D4.5), Proposição S
and the Full Cycle-Count Decomposition Theorem as instantiated at K=4,
the four-regime structure and its exact collapse to one formula, and
every numerical/symbolic claim checked in the document were all
independently re-derived or re-verified from scratch and matched
exactly, with zero discrepancies, across every check attempted —
including several checks that go beyond what the mandate required (n=9
true brute force, one step past even the front's own n=8 reach; the
full finite-n D4.3/D4.4 formulas via an independent identity, not just
their limits; the D4.5 leading-order term and its numeric maximum).
Two findings are named below: one MODERATE (a false "not stated
anywhere" claim about prior art for one specific value, not affecting
the mathematics), and procedural/informational LOW findings.

## Findings

### F1 — MODERATE: Corollary D4.4's "not stated anywhere in THEOREM.md" claim is false for `E[M_4^3]=128/1155`

ATTEMPT.md §6.3 states: *"`128/1155` is **not** separately stated
anywhere in `THEOREM.md` for K=4 — it is derived here directly, by
elementary calculus... from the cited general-K continuum density."*

This is factually incorrect. `THEOREM.md` **Estágio 20**
("Extensão, Estágio 20 — 2026-08-25", the K=4 instance of Conjectura 1,
lines 3608–3647) already states, verbatim, as a byproduct of its own
K=4 continuum-density derivation:

> *"Subprodutos: `E[M_4]=128/315=\varphi_4`, `E[M_4^2]=1/5`
> (consistente com o `1/(K{+}1)` do Estágio 18), `E[M_4^3]=128/1155`."*
> (THEOREM.md, line 3639–3641)

So `E[M_4^3]=128/1155` was already on record for K=4 before this front
existed — the same value ATTEMPT.md's §6.3 claims is newly derived
here and absent from THEOREM.md. The front's own §1.1 reading list
names Estágio 24 (the K=5 front) for the continuum-density citation
but does not list Estágio 20 (the K=4-specific predecessor, in the
very same `conjecture1_k4_attempt` branch) among what was read, which
is presumably how this was missed.

This does **not** affect the mathematical correctness of Corollary
D4.4 or of the front's cross-check logic: I independently re-verified,
by direct elementary integration of the cited Estágio-24 continuum
density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, that `E[M_4^3]=128/1155`
exactly, that `E[M_5^3]=256/3003` exactly (matching Estágio 24's own
stated K=5 instance, `THEOREM.md` line 4083, exactly), and that the
general closed-form `E[M_K^3]=K!\,2^K/\prod_{j=0}^{K-1}(2j+5)` produces
both values correctly (see `adv_symbolic_checks.log`, section (e)). The
cross-check methodology itself (deriving the general-K formula from the
cited density, then checking it reproduces THEOREM.md's own K=5
instance) is sound and the value is right — only the specific
"not stated anywhere" / "derived here" framing for this one number is
inaccurate. Corollary D4.2's own genuinely new content (the `1/n^2`
through `1/n^5` terms of the mean formula) is unaffected by this
finding; nor is the constant-term/leading-rate cross-check for D4.2,
which is correctly cited and verified (see F0 below, no issue).

### F2 — LOW, procedural (front's own disclosure, relayed per the mandate)

The orchestrating session reported that the front (K4-FULL-CDF-ATTEMPT)
disclosed running one read-only `git status` command near the end of
its own work, to confirm no tracked files were modified — a technical
breach of its own "no git command of any kind" scope instruction,
though read-only and made no changes. Relayed here as instructed;
cosmetic/procedural, not a mathematical finding.

### F3 — LOW, procedural (this referee's own conduct, self-disclosed)

This referee session's own **very first** tool call included
`git branch --show-current` (bundled with an `ls` of the target
directory), run before recognizing that the "do NOT run any git
command whatsoever, including read-only ones" instruction applied to
this review. It was read-only, made no changes, and no git command was
run at any point afterward. Disclosed here in the same spirit as F2,
holding this session to the same standard it was asked to apply to the
front under review.

### F4 — LOW, informational (notation clarity, no defect)

ATTEMPT.md §1.2 defines `O:=n-L_0-L_1-L_2-L_3` and, in the same
sentence, states `(L_0,\ldots,L_3,O)` is "uniform over the
`\binom n4` compositions of `n-4` into `5` nonnegative parts." Read
naively, these two clauses appear to conflict (if `O=n-\sum L_i`
directly, the parts sum to `n`, not `n-4`). Investigating this by
attempting to independently construct a position-level model of the
arc structure, I initially built `L_s` to mean "predecessor-arc points
of `s`, excluding `s` itself" — under that reading, my model's
empirical `P(S=A)` did **not** match Proposição S's formula in any of
several tested configurations (only `p_D` summed against wrong totals;
sums of the formula over all 16 subsets came out `<1`).

Resolving this: the convention actually used throughout §4.1's
building blocks (`S1`, `PS`, `TS`, `QS`, and the "`\binom{m-1}3`
compositions of `m` into 4 **positive** parts" language), and required
by D4.1's own boundary reasoning ("`V_s=L_s`... landing at position 1
of its own arc"), is that **`L_s` includes the source point `s`
itself** — so `L_s\ge1` always, `V_s=1` corresponds to a direct
self-loop landing (`U_s=s`), and `O=n-\sum L_s` (as literally written)
is exactly correct with no missing `-4` term. The "compositions of
`n-4`" clause refers to a separately-shifted, nonnegative
`L_i':=L_i-1`, used only to justify the `\binom n4` count in that one
sentence — a valid but momentarily confusing double use of "`L_s`" for
two related-but-different quantities within one paragraph. Once
corrected, an independently-built position-level model (constructing
explicit permutations realizing chosen `(L_0,\ldots,L_3,O)`
compositions, including many deliberately-degenerate cases with
several `L_i=0`, and brute-forcing over all `n^4` target-tuples) matched
Proposição S **exactly** in every one of 14 tested configurations, and
also confirmed the Decomposition Theorem's `V_s | S` mutual
independence and uniformity exactly (see Checks §2 below). No
mathematical defect — a one-sentence clarification in §1.2 that `L_s`
includes the source point would preempt this kind of misreading.

No other issues — LOW, MODERATE, or HIGH — were found anywhere in the
document, including in the parts of the mandate given special
scrutiny (the D4.2 mean formula's citation match, the D4.4 K=5
cross-check, the four-regime partition and collapse, the D4.5 rate-bound
chain).

## Independent checks run (all from scratch; scripts and full logs in this directory)

### 1. Headline Proposição D4 — true brute force of Definition 4, n=4..9

`adv_bruteforce_k4.py` / `adv_bruteforce_k4.log`. Built directly from
`THEOREM.md`'s own Definition 4 text (lines 859–872): π uniform random
permutation of `[n]`; sources `{0,1,2,3}`; `U_0,\ldots,U_3` i.i.d.
`Uniform([n])`; `f(i):=U_i` on sources, `\pi(i)` otherwise;
`T:=`#cyclic points of `f`. Two independent enumeration routes:

- **Route A (literal):** all `n!` permutations × all `n^4` target-tuples
  — exactly the raw sample space (`n!\cdot n^4`) the front itself
  reports. Run and cross-checked at `n=4,5`.
- **Route B (reduced, proved equivalent):** since `\pi(0..3)` is
  discarded, the law of `T` depends only on `\pi` restricted to
  `\{4,\ldots,n-1\}`, which — a uniform random permutation's restriction
  to any fixed domain subset is uniform over injections — is uniform
  over all `P(n,n-4)` injective maps into `[n]`. This gives the
  **identical** `T`-distribution using `24\times` fewer raw
  configurations. Verified identical to Route A exactly (every `T`
  value, `n=4,5`) before being trusted alone at larger `n`.

Results, all exact `Fraction` arithmetic, zero mismatches at every `k`:

| n | configs enumerated (Route B) | wall time | vs Proposição D4 |
|---|---|---|---|
| 4 | 256 | <0.1s | exact match, every k |
| 5 | 3,125 | <0.1s | exact match, every k |
| 6 | 38,880 | <0.1s | exact match, every k |
| 7 | 504,210 | 0.3s | exact match, every k |
| 8 | 6,881,280 | 5.5s | exact match, every k |
| 9 | 99,202,320 | 93.8s | exact match, every k |

n=9 goes one full step beyond even the front's own reach (n=8). This is
the single strongest check in this report: it validates Proposição D4's
final closed form directly against the literal model definition,
independent of every intermediate derivation step.

### 2. Proposição S and the Decomposition Theorem at K=4 — position-level, from scratch

`adv_propS_position_model.py` / `.log`: explicit permutations
constructed to realize chosen `(L_0,L_1,L_2,L_3,O)` arc-length
compositions (predecessor-arc-including-source convention, see F4),
brute-forced over all `n^4` target-tuples, exact `Fraction` empirical
`P(S=A)` compared against Proposição S's closed form for **all 16**
subsets `A\subseteq\{0,1,2,3\}`, across 14 configurations spanning
`n=8` to `n=12` — including 8 deliberately-degenerate boundary cases
(one, two, three, or all four `L_i=0`), and two different topologies
for the O-region (a single O-cycle vs. `O` isolated fixed points, to
probe the "independent of topology" claim). **All 14 cases matched
exactly on every one of the 16 subsets**, and the 16 probabilities
summed to exactly 1 in every case.

`adv_decomposition_Vs_check.py` / `.log`: using the same construction,
the joint empirical law of `(V_s)_{s\in S}` (computed directly as the
count of cyclic points landing within each source's own arc) was
checked against the Decomposition Theorem's claim — mutual independence
given `S`, each `V_s\sim\mathrm{Uniform}\{1,\ldots,L_s\}` — across 3
configurations (36 distinct nonempty `S` cells total). **Every cell
matched**: uniform support with no gaps, exactly the claimed
probability on every joint outcome.

### 3. Regime partition, boundary continuity, monotonicity, range

`adv_symbolic_checks.py` / `.log`, section (c). The four regimes
(`0\le k\le n-4`; `k=n-3`; `k=n-2`; `k=n-1`) partition `\{0,\ldots,n-1\}`
with no gap or overlap by direct arithmetic inspection (four
consecutive integer ranges). The three boundary-value formulas quoted
verbatim in §4.2's transcript (`F(n-3)`, `F(n-2)`, `F(n-1)`) were
independently substituted into the single stated Proposição D4 formula
and found to match **exactly** (`sp.simplify` difference `=0` in all
three cases) — confirming the claimed "collapse to one formula" is
exact, not approximate. `F(0)=0` confirmed exactly (the `k(k+1)`
factor). A monotonicity + `[0,1]`-range scan across `n=4,\ldots,40`,
every `k`, using exact `Fraction` arithmetic, found zero violations.

### 4. Corollary D4.1

`1-F(n-1)` computed independently from the stated Proposição D4 formula
equals `24/n^4` exactly (symbolic, all `n`) — matches D4.1 and is
independently confirmed by the brute-force table above at `k=n-1` for
every tested `n`.

### 5. Corollary D4.2 — independent mean-formula re-derivation, and the φ_4/c_4 citation check

`adv_symbolic_checks.py`, section (d). `\varphi_n^{(4)} := 1 -
\frac1n\sum_{k=0}^{n-1}F(k)` computed independently via `sp.summation`
directly on the stated Proposição D4 formula: result matches the
claimed `128/315+23/(210n)+482/(315n^2)+99/(70n^3)+7/(9n^4)+4/(21n^5)`
**exactly** (symbolic difference `0`).

**Citation check (task-mandated, done by reading `THEOREM.md`
directly, not trusting the front's transcription):**
- `\varphi_4=128/315`: confirmed at `THEOREM.md` line 3639 (Estágio
  20, K=4 continuum-density front) and again at line 4082 (Estágio 24,
  general-K front, "`E[M_K]=\varphi_K`... para todo `K`"). Matches
  exactly.
- `c_4=23/210`: confirmed at `THEOREM.md` line 2065 (Estágio 7,
  "a soma telescópica reproduzindo o exemplo trabalhado
  `c_4=23/210`"). Matches exactly.

Both citations are accurate. (See F1 above for the one citation
inaccuracy found, which concerns a different value, `E[M_4^3]`, not
`\varphi_4` or `c_4`.)

### 6. Corollaries D4.3–D4.4 — independent moment re-derivation and K=5 cross-check

`adv_symbolic_checks.py`, sections (e) and (bonus). Two independent
checks:

- **Continuum limits**, by direct elementary integration of the cited
  density `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` (Estágio 24): `E[M_4^2]=1/5`
  and `E[M_4^3]=128/1155` both confirmed exactly; `E[M_5^3]=256/3003`
  confirmed exactly, matching `THEOREM.md`'s own stated K=5 instance
  (line 4083) exactly — the general formula
  `E[M_K^3]=K!\,2^K/\prod_{j=0}^{K-1}(2j+5)` was independently derived
  and confirmed correct at both `K=4,5`. The cross-check logic itself
  (derive the general-K formula, verify it reproduces the cited K=5
  instance) is sound. (Only the "not stated anywhere for K=4" framing
  is wrong — F1 above.)
- **Full finite-n formulas**, via a genuinely different identity from
  the one used for D4.2 (`E[T^p]=\sum_{t=0}^{n-1}[(t+1)^p-t^p](1-F(t))`,
  the Abel/survival-function summation, vs. D4.2's direct
  `1-\frac1n\sum F(k)`): both `E[(M_n^{(4)})^2]` and
  `E[(M_n^{(4)})^3]` reproduced **exactly**, matching every claimed
  coefficient in D4.3 and D4.4, including all the `1/n^2,\ldots,1/n^7`
  terms (not just the limits) — this goes beyond what the task
  required and adds a second, independent confirmation route.

### 7. Corollary D4.5 — rate-bound arithmetic chain

`adv_symbolic_checks.py`, section (f). `F_n^{(4)}(x)-F_4(x)` computed
independently via `sp.cancel` after substituting `k=xn` into the
Proposição D4 formula; denominator confirmed to match the claimed
`n^3(n-1)(n-2)(n-3)` exactly. Re-deriving the bound from scratch using
the front's own stated method (bound each `x`-coefficient of the
numerator, viewed as a polynomial in `n`, by the sum of its own
coefficients' absolute values, using `|x|\le1`; then use
`n^3(n-1)(n-2)(n-3)\ge n^6/8` for `n\ge6`, independently verified by
direct factoring: `n^3(n-1)(n-2)(n-3)-n^6/8 =
n^3(7n^3-48n^2+88n-48)/8`, nonnegative for `n\ge6`): this reproduces
**exactly** `7248/n` — not merely an upper bound on the claimed
constant, but the identical constant. A dense numeric scan (`n=6`
through `10{,}000`, `x`-grid step `0.001`) found zero bound
violations, worst observed ratio `|gap|/(7248/n)\approx0.000098`
(the bound is loose, as disclosed). The leading-order term
`g_1(x)=-6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x` was also independently
re-derived (`\lim_{n\to\infty}n\cdot(F_n^{(4)}(x)-F_4(x))`) and matches
the document's stated `g_1(x)` exactly; its numeric maximum on
`[0,1]` was found at `x=0.3699`, value `0.708718` — matching the
document's disclosed (honestly, as *not* proved uniform) `\approx0.7087`
at `x\approx0.3699` exactly.

### 8. Bonus Monte Carlo triangulation, reserved seeds

`adv_mc_bonus.py` / `.log`: fully independent direct simulation of
Definition 4 itself (own `numpy` permutation + own i.i.d. targets, not
the decomposition/reduced model, not any code from the front), at the
same 6 `(n,k)` cells the front itself reports, using seeds
`20260926501`–`20260926506`. All 6 cells landed within `2.1\sigma` of
the exact Proposição D4 prediction — consistent, as expected.

## Seed reservation

Task-mandated sub-range: `20260926500`–`20260926799` (a sub-range of
this front's own reserved `20260926000`–`20260926999` block).
Confirmed unused before use:

```
$ grep -rn "20260926" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7510:      20260926000-20260926999.
05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md:15:antes da correção. Seeds `20260926000-20260928999`, um bloco por
```
— only the governance reservation line and one `DISCOVERY_LAB_STATE.md`
mention of the wider block range (not individual seeds), plus this
front's own files (outside the scope of this grep, run against
`05_DISCOVERY_LAB/` broadly) — no other prior use of any seed in the
task-mandated sub-range found. Seeds actually used:
`20260926501`–`20260926506` (six Monte Carlo cells in
`adv_mc_bonus.py`), all within the reserved sub-range.

## Files in this directory

| file | contents |
|---|---|
| `adv_bruteforce_k4.py` / `.log` | true brute force of Definition 4, n=4..9, vs Proposição D4 |
| `adv_propS_position_model.py` / `.log` | position-level, from-scratch verification of Proposição S at K=4, 14 configurations incl. boundary cases |
| `adv_decomposition_Vs_check.py` / `.log` | verification of the Decomposition Theorem's `V_s\vert S` independence + uniformity |
| `adv_symbolic_checks.py` / `.log` | all symbolic checks: regime boundaries/collapse/monotonicity, D4.2 mean re-derivation + φ_4/c_4 citation check, D4.3/D4.4 moment re-derivation + K=5 cross-check, D4.5 rate-bound re-derivation + leading term |
| `adv_mc_bonus.py` / `.log` | bonus Monte Carlo triangulation, reserved seeds |
| `REFEREE_REPORT.md` | this document |

## Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html`, or the front's own `ATTEMPT.md`. All writes confined to
this `adversarial/` subdirectory. No `.py` file from this front or any
ancestor/sibling front was read, opened, or imported — every script
here was written fresh from `THEOREM.md`'s prose and `ATTEMPT.md`'s
stated formulas only. One git-command deviation self-disclosed (F3
above). All randomized checks used only seeds
`20260926501`–`20260926506`, within the task-mandated reserved
sub-range.
