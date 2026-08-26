# Adversarial referee report: `K3-JOINT-STRUCTURAL-ATTEMPT` (`DISC-DEC-088`)

**Target:** `.../k2_joint_case_split_attempt/k3_joint_structural_attempt/ATTEMPT.md`
(Wave 20, front (b)). Pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble defined in `THEOREM.md`
Definitions 1–4. **This is not a Millennium Problem and no claim of
that kind appears anywhere in the target document or in this report.**

**Referee discipline.** No `.py` file from this front or any front in
its lineage (`conjecture2_direct_attempt`, `joint_two_point_attempt`,
`joint_exploration_continuum_attempt`, `k2_joint_case_split_attempt`,
`k3_joint_structural_attempt`) was opened, read, or imported. Every
script in this `adversarial/` directory is written fresh from the
mathematical prose of `ATTEMPT.md` and the required `THEOREM.md`
sections (Estágios 18, 25, 27, 28, 31) and the predecessor's
`ATTEMPT.md` (`k2_joint_case_split_attempt/ATTEMPT.md`, read in full).
Reserved seed range for this referee: `20260893000`–`20260893999`
(grep-confirmed clean before first use — only governance reservation
lines in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` predate this report's
own files). No governance file touched, no git command run, no other
front's `adversarial/` subdirectory touched.

---

## Verdict

> **SOUND — ACCEPT for catalogue**, at the tier claimed. Every load-bearing
> mathematical claim in the target document — Lemma 1 at m=3, the
> Governing-Source Reindexing corollary, Lemma 4 (Cycle-Predecessor
> Uniqueness), Lemma 5's closed-form formulas, and Proposition NN3 itself
> (the exact closed form of `P_nn(n,3)`) — was independently rebuilt from
> scratch and found correct, by methods structurally different from (and,
> for Proposition NN3, considerably more extensive than) what the front
> itself reports. No mathematical error was found anywhere in the target
> document. One purely cosmetic wording issue is named below (negligible
> severity, does not affect any proof). No overclaim was found: §8's
> non-closure scoping (full CDF at K=3; general joint two-point law at
> any K) is accurate, and no claim of progress on any Millennium Problem
> appears anywhere.

This is a genuinely surprising, high-value result — Estágio 31 (the K=2
predecessor) diagnosed K=3 as substantially harder than K=2 (a
functional-graph-on-arcs obstruction, not a flat table), and the wave 20
mandate treated honest non-closure at K=3 as fully acceptable. This front
nonetheless closed the scalar second-moment/same-cycle K=3 target
completely and correctly, by identifying two genuine simplifications
(governing-source reindexing collapses topology; cycle-predecessor
uniqueness collapses the 64-cell table to closed-form linear/bilinear
rules) that directly answer Estágio 31's own diagnosis rather than
sidestepping it. Independent re-derivation confirms both simplifications
are real and correctly exploited.

---

## What was independently re-verified, and how

### 1. Lemma 1 at m=3 + Governing-Source Reindexing corollary (§2)

**Script:** `adv_lemma1_m3.py` / `.log`.

Built from scratch: for each permutation of `[n]`, `n=4,...,7`
(exhaustive, all `n!` permutations), computed the contracted permutation
`σ` on marks `{0,1,2}`, the mark-indexed gap vector `(g(0),g(1),g(2),O)`,
the mark-indexed arc lengths `a_m=g(m)+1`, and — independently, not by
citing the front's proof — the **governing-source**-indexed arc lengths
`L_s := a_{σ⁻¹(s)}`.

Checked, exactly (integer counting, no floats):
- `σ` uniform on `S_3` (6 topologies, equal counts) — **holds, all n**.
- `(σ, a\text{-composition})` cells all equal `(n-3)!` (Lemma 1(b)) —
  **holds, all n** (`0` mismatches, `4≤n≤7`).
- `(σ, L\text{-composition})` cells **also** all equal `(n-3)!`, i.e. the
  governing-source-indexed vector is independent of `σ` too — **holds,
  all n**.
- The *distribution* of `(L_0,L_1,L_2,O)` (as a multiset of
  composition→count) is **identical** to that of `(a_0,a_1,a_2,O)` —
  **holds, all n** — this is the corollary's precise content, and it was
  checked cell-by-cell, not just at the level of marginals.

All checks pass at `n=4,5,6,7`, zero mismatches. The corollary is correct.

### 2. Lemma 4 (Cycle-Predecessor Uniqueness, §3.2)

**Scripts:** `adv_lemma4_cycle_predecessor.py` (source-level, all 64
`dest:{0,1,2}→{0,1,2,DEAD}` functions) and `adv_lemma4_position_level.py`
(position-level, full functional-graph simulation).

*Source-level check (64/64 exhaustive):* for every one of the `4^3=64`
destination functions, computed the cyclic subset of `{0,1,2}` (nodes
whose forward `dest`-orbit returns before hitting `DEAD`), and for every
cyclic `s`, counted how many `t∈{0,1,2}` satisfy `dest(t)=s ∧ t` cyclic.
**Result: exactly one such `t`, in every one of the 78 (dest, cyclic-`s`)
instances across all 64 functions — zero exceptions.** Also confirmed the
lemma is non-vacuous: 27 of those 78 instances have a genuine *extra*
incoming edge from a non-cyclic source (the scenario the "inertness"
claim is about).

*Position-level check (the harder, second half of the lemma):* built the
full 3-arc functional graph explicitly at the level of concrete
positions — own construction, not using the cycle-predecessor shortcut
in the construction itself, only in the *prediction* being tested —
determined cyclicity of **every** position by direct forward-graph
traversal, and compared against Lemma 4's closed-form prediction
(`ARC(s)`'s cyclic set `= {k,...,L_s}`, `k` = the unique cycle-predecessor's
landing position, independent of any other incoming edge). Exhaustive
over `L_0,L_1,L_2 ∈ {1,2,3,4}` (including the degenerate `L=(1,1,1)` edge
case with no interior positions at all) and all 64 destination
assignments with all valid landing positions:

**`45,424` (L, dest, pos) configurations checked, `29,280` of them with
a genuine extra inert incoming edge, `0` mismatches.**

Lemma 4 — both the uniqueness half and the harder inertness half — is
correct, confirmed at the position level, not just abstractly.

### 3. Lemma 5's closed-form formulas (§3.3)

**Script:** `adv_lemma5_check.py`.

*Part A, symbolic re-derivation (own case analysis, sympy):* independently
enumerated the 5 cyclic-structure cases that put source `0` on a cycle
(home; 2-cycle via 1; 2-cycle via 2; 3-cycle `0→1→2→0`; 3-cycle
`0→2→1→0`) and summed their probabilities — reproduced
`P(\text{pos }i\text{ cyclic})=i(2L_1L_2+L_1n+L_2n+n^2)/n^3` **exactly**
(`sympy` difference `0`). Independently enumerated the 6 cyclic-structure
cases that put both `0` and `1` on cycles and summed — reproduced
`P(\text{both cyclic})=2ii'(2L_2+n)/n^3` **exactly** (`sympy` difference
`0`). Both formulas match the claim to the term.

*Part B, exact enumeration cross-check:* for 5 diverse concrete `(L_0,
L_1,L_2,n)` configurations (including the `L=(1,1,1)` edge case with no
interior positions), enumerated **all** `n^3` `(U_0,U_1,U_2)` choices as
concrete abstract slots, built the position-level functional graph
directly, and compared exact `Fraction` counts against both Lemma 5's
claimed formulas and the same-arc monotone-nesting claim (`i<i'` in the
same arc ⟹ `P(\text{both cyclic})=P(i\text{ cyclic})`, the smaller/harder
index's own marginal). **Zero mismatches across every sub-formula, every
configuration.**

*Minor wording note (cosmetic, see "Issues found" below):* the target's
own prose calls the smaller index `i` (in `i<i'`) "the nearer-to-tail
point's own marginal" — given the document's own convention that position
`L_s` (the maximum index) is the tail, `i<i'` makes `i` the point
*farther* from the tail, not nearer. The formula and its use are
unaffected (verified independently above); only the descriptive label is
inverted.

### 4. Proposition NN3 — the main result (§4)

This was treated as the single most important, most checkable claim, and
was attacked by **three independent routes**, one of them considerably
beyond what the mandate required.

**(a) TRUE raw brute force of Definition 4's full K=3 model — no reduced
model, no arc shortcut of any kind.** `adv_raw_brute_k3.py`: literally
iterates every permutation of `[n]` (`itertools.permutations`) and every
`(U_0,U_1,U_2)∈[n]^3`, builds `f`, and checks cyclicity of `n-2,n-1` by
direct forward simulation. Exact integer counting, `Fraction` only at the
end.

| `n` | configs (`n!·n^3`) | brute force `P_nn(n,3)` | closed form | match | elapsed |
|---|---|---|---|---|---|
| 5 | 15,000 | `389/1250` | `389/1250` | ✓ | 0.01s |
| 6 | 155,520 | `3/10` | `3/10` | ✓ | 0.05s |
| 7 | 1,728,720 | `7017/24010` | `7017/24010` | ✓ | 0.61s |
| 8 | 20,643,840 | `10271/35840` | `10271/35840` | ✓ | 7.6s |
| 9 | 264,539,520 | `4801/17010` | `4801/17010` | ✓ | 102.4s |

**`5/5` exact matches**, including a full raw enumeration at `n=9`
(264,539,520 literal configurations, ~102s) — this is the same scale the
front itself reports for its own independent brute force, reproduced here
completely independently (own code, own approach, no reduced-model
shortcut at all). A bonus `n=5` point (outside the front's own
`n≥6` domain) was also checked and matches — see "domain note" below.

**(b) Reduced-model assembly, built independently from Lemma 1 + Lemma 5
(both already independently re-verified above), NOT copied from the
front's `assemble_pnn3.py`.** `adv_reduced_model_assembly.py`: own
`T(L_0,L_1,L_2)` formula (OO / O–arc / same-arc / cross-arc terms, built
from first principles using the independently-derived Lemma 5 formulas),
summed exactly (`Fraction`) over every composition, for `n=5,...,30,40`.
**All `27/27` match the closed form exactly.**

**(c) Full independent symbolic (sympy) triple-sum derivation**, own code,
own case analysis (not the front's `symbolic_derivation_k3.py`).
`adv_symbolic_derivation.py`: built `T(L_0,L_1,L_2,n)` symbolically from
the independently re-derived Lemma 5 formulas, summed in closed form over
`L_2`, then `L_1`, then `L_0` (`sp.summation`, exact rationals throughout),
divided by `\binom n3\cdot(n-3)(n-4)`, and simplified. **The result is
algebraically identical to the claimed closed form** —
`sp.simplify(derived - claimed) == 0`. This is a genuine, independent,
from-scratch algebraic proof of Proposition NN3, not merely a numerical
match at finitely many `n`.

**Conclusion: Proposition NN3, `P_nn(n,3)=(35n^3+38n^2+23n+6)/(140n^3)`,
is correct**, confirmed by three independent and mutually corroborating
routes, including a full raw enumeration at `n=9` matching the front's
own reported scale.

**Domain note (not an issue, minor positive finding).** The target
restricts to `n≥6` "for a safety margin matching the predecessor's own
convention." Independent check at `n=5` (the natural minimum — sources
`{0,1,2}` and query points `{n-2,n-1}={3,4}` are disjoint at `n=5` but
collide at `n=4`, where `n-2=2` coincides with a reroute source) shows the
formula **already holds exactly at `n=5`** (`389/1250`, both by raw brute
force and by the reduced model). The front is not overclaiming — if
anything it is slightly conservative — so this is not a defect, just a
note that the true domain is `n≥5`.

### 5. Corollary NN3.1 (`E[(M_n^{(3)})^2]→1/4`)

Algebra check: `(35n^3+38n^2+23n+6)/(140n^3) → 35/140 = 1/4` as `n→∞` —
correct. `1/4 = 1/(K+1)|_{K=3}` — correct. Citation check: `THEOREM.md`
Estágio 18 does state `E[M_K^2]=1/(K+1)` as an **unconditional** anchor
for `K≤3` (verified by reading Estágio 18 in full — see paragraph (ii)
there, citing the already-proved conditional densities `1/2,1/3,1/4`).
Estágio 27's Lemma P2 is confirmed, by reading Estágio 27 in full, to be
stated and proved for **general** `K` (not just `K≤2`), so its
application here at `K=3` is a legitimate citation, not a scope
violation. Corollary NN3.1 is correct as stated.

### 6. Corollary NN3.2 (`P_nn\text{-same}(n,3)→1/8`)

Algebra check: `\tfrac12\cdot\tfrac{35n^3+38n^2+23n+6}{140n^3} =
\tfrac{35n^3+38n^2+23n+6}{280n^3} → 35/280 = 1/8` — correct.
`1/8=1/(2(K+1))|_{K=3}` — correct.

The load-bearing citation here — Theorem J's Corollary (Estágio 25):
`P(\text{same cycle}\mid\text{both cyclic})=1/2` **exactly at every
finite `n,K`**, including `K=3` — was not just read and cited on trust
but **independently re-tested with fresh raw data**. `adv_same_cycle_
check.py`: same raw, full Definition-4-K=3 brute force as above, but also
tracking whether `n-2,n-1` land in the same final cycle when both are
cyclic:

| `n` | `P(\text{both cyclic})` | `P(\text{both, same cycle})` | ratio |
|---|---|---|---|
| 6 | `3/10` | `3/20` | `1/2` |
| 7 | `7017/24010` | `7017/48020` | `1/2` |
| 8 | `10271/35840` | `10271/71680` | `1/2` |

**Exactly `1/2` at every `n` tested** — direct confirmation, at `K=3`
specifically, of the exact-`1/2` claim underlying Corollary NN3.2, not
just trust in the Estágio 25 citation. Corollary NN3.2 is correct.

### 7. §8 (what did NOT close) — honesty check

Read in full and checked against the actual content of §§2–6. §8.1
correctly scopes the full CDF of `M_n^{(3)}` (not just the second moment)
as open — Lemma 4/5 give pairwise joint law only, not the whole-count
distribution, and the document says so plainly. §8.2 correctly scopes the
general-`K` joint two-point law as open, explicitly labeling the
generalizability of the method as "a genuine, precisely-scoped hint, not
a claim" — this is accurate; nothing in §§2–3's proofs was found, on
independent reconstruction, to secretly rely on `K=3` being special in a
way that would make the hint false, but the document correctly does not
claim the generalization is done. §8.3 correctly disclaims any moment
beyond the second, any rate for the overlap-allowed convention, and any
Millennium Problem connection. No overclaim found in §8, and no
overclaim found in the executive summary either — "closed for the scalar
second-moment / same-cycle targets" is precisely the tier actually
proved, not overstated to "K=3 solved" in general.

### 8. Overall claim discipline

Grepped the target document for scope-related language; every PROVED
claim in the scorecard (§11) was independently checked above and holds;
every OPEN item is genuinely open (not silently answered elsewhere in
the document). No claim of progress on any Millennium Problem appears
anywhere in `ATTEMPT.md`; none appears in this report.

### 9. Supplementary Monte Carlo triangulation (bonus, own seeds)

`adv_monte_carlo.py`, reserved seeds `20260893001`–`20260893003`, direct
simulation of Definition 4's K=3 model (own `numpy` RNG, own code):

| `n` | trials | `P̂(\text{both})` | `z` vs `1/4` | `P̂(\text{same})` | `z` vs `1/8` |
|---|---|---|---|---|---|
| 200 | 200,000 | 0.25005 | +0.05 | 0.12487 | −0.17 |
| 2,000 | 30,000 | 0.25397 | +1.58 | 0.12827 | +1.69 |
| 5,000 | 10,000 | 0.24610 | −0.91 | 0.12150 | −1.07 |

All within `≈1.7σ` of the exact targets — consistent, supplementary only
(the exact proofs above are the actual evidence).

---

## Issues found

| # | Issue | Severity | Detail |
|---|---|---|---|
| 1 | Inverted "nearer-to-tail" label in §3.3's same-arc formula description | **Negligible / cosmetic** | The document's own §3.1 convention makes position `L_s` (the max index) the tail; for `i<i'` in the same arc, `i` (the smaller index) is the one whose marginal governs `P(\text{both cyclic})`, and `i` is *farther* from the tail, not nearer. The formula itself, and its use throughout §4's assembly, are correct (independently re-verified above, both symbolically and by exact enumeration) — only the descriptive phrase is inverted. This is the same class of purely-cosmetic prose slip the predecessor's own referee found in the K=2 front (a swapped source label in a side remark, "não afeta a prova") — a recurring minor authorial habit in this lineage, not a mathematical defect. |

No other issues — of any severity — were found. In particular: no error in Lemma 1's re-verification, no error in Lemma 4 (either half), no error in Lemma 5, no error in Proposition NN3 or its three independent re-derivations, no error in Corollaries NN3.1/NN3.2's algebra or citations, no scope overreach in §8, no Millennium Problem claim anywhere, and no seed-range or governance-file violation (all reserved-range and no-edit constraints independently checked — see the seed-collision grep this referee ran, reproduced above).

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `adv_lemma1_m3.py` / `.log` | Lemma 1 at m=3 + Governing-Source Reindexing corollary, exhaustive `n=4..7` |
| `adv_lemma4_cycle_predecessor.py` / `.log` | Lemma 4 uniqueness half, exhaustive over all 64 `dest` functions |
| `adv_lemma4_position_level.py` / `.log` | Lemma 4 inertness half, position-level, 45,424 configurations |
| `adv_lemma5_check.py` / `.log` | Lemma 5, symbolic re-derivation + exact enumeration cross-check, 5 configs |
| `adv_raw_brute_k3.py` / `.log` | TRUE raw brute force of Definition 4's full K=3 model, `n=5..9` |
| `adv_reduced_model_assembly.py` / `.log` | independently-built reduced-model assembly, `n=5..30,40` |
| `adv_symbolic_derivation.py` / `.log` | full independent symbolic (sympy) triple-sum re-derivation of Proposition NN3 |
| `adv_same_cycle_check.py` / `.log` | direct raw confirmation of the exact-1/2 same-cycle split at K=3, `n=6,7,8` |
| `adv_monte_carlo.py` / `.log` | supplementary Monte Carlo triangulation, own reserved seeds |

---

## Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No file outside this `adversarial/` subdirectory was
created or modified. No git command run. No `.py` file from this front
or any front in its lineage was read, opened, or imported — every script
in this directory is written fresh from the mathematical prose of
`THEOREM.md` and the target/predecessor `ATTEMPT.md` files only. All
randomized verification used only this referee's own reserved seed range
`20260893000`–`20260893999` (grep-confirmed clean before first use). No
claim of progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
