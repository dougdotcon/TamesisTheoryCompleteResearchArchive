# Adversarial referee report — K2-JOINT-CASE-SPLIT-ATTEMPT

**Target document:** `ATTEMPT.md` (this front's parent directory),
`K2-JOINT-CASE-SPLIT-ATTEMPT`, wave 19 front (a), authorized by
`DISC-DEC-083`. Central claim: an exact closed form for `P_nn(n,2)`,
`Lemma P2`'s (`distributional_bridge_attempt`, cited) K=2 "both
non-rerouted query points cyclic" probability:

`P_nn(n,2) = (10n²+7n+2)/(30n²) = 1/3 + 7/(30n) + 1/(15n²)`, `n≥4`,

obtained by generalizing `THEOREM.md` Proposition 4 / `joint_exploration_
continuum_attempt`'s Proposition K1's K=1 case-split method to K=2, via two
new lemmas: a "Marked-Point Gap Structure Lemma" (Lemma 1) and a
"Two-Source Redirect-Structure Lemma" (Lemma 2).

**This is pure internal combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble defined in `THEOREM.md`
Definitions 1–4. It is NOT a Millennium Prize Problem, and no claim of
progress on one is made anywhere in this report.**

---

## Verdict

> **SOUND — ACCEPT for catalogue**, at the tier claimed (PROVED, exact,
> elementary case-split + symbolic resummation, independently cross-checked
> by exhaustive brute force). No mathematical error was found in Lemma 1,
> Lemma 2, Proposition NN2, Corollary NN2.0/NN2.1/NN2.2, Lemma 3, or
> Corollary NN2.3. One minor, purely cosmetic documentation issue is named
> (§5) — it does not touch any proof and required no correction to any
> claimed result. The K=3 non-closure diagnosis is independently
> stress-tested (§6) and found to be a genuine, correctly-identified
> structural escalation, not premature surrender.

Every numerical claim checked below was independently re-derived and/or
re-enumerated from the mathematical descriptions in `THEOREM.md` and the
two named predecessor `ATTEMPT.md` files' **prose only**. **No `.py` file
belonging to this front (its own 7 scripts) or any predecessor front was
opened, read, or imported at any point in this review.** All verification
code below is fresh, written by this referee, and lives in this
`adversarial/` directory (never modifying the target front's own files).

---

## 0. Provenance / anchoring disclosure

Per the review mandate, `THEOREM.md`'s relevant sections, both named
predecessor `ATTEMPT.md` files' prose, and the target `ATTEMPT.md` were
read in full *before* any independent derivation work began (mandate items
1–3 require reading the target document in full before proceeding). This
means the "re-derive before reading the target's own proof closely" step
(mandate item 5) could not be performed in strict textual isolation — the
target's Lemma 1/Lemma 2 statements and Proposition NN2's closed form had
already been read once the independent derivation work started.

To mitigate anchoring risk within that constraint: every re-derivation
below was carried out with **freshly written code implementing the
mathematics from first principles** (own permutation-construction
functions, own case-enumeration logic, own role-assignment bookkeeping),
never by transcribing or lightly editing the target document's stated
formulas into code, and never by reading any of the target's own `.py`
files. Where a check's *purpose* was to catch a missed or double-counted
case, the check was built to enumerate the case space directly (e.g.
`rederive_nn2.py`'s explicit loop over every ordered pair of the `n-2`
non-source roles) rather than to evaluate the target's already-simplified
closed-form expressions. The results (§§2–4 below) constitute a genuine,
independent re-derivation, not a transcription check — but the reader
should weigh the "already read once" caveat honestly, as instructed.

---

## 1. Cycle-detector: unit-tested before any use

`cycle_utils.py`: a from-scratch functional-digraph cyclicity detector
(3-color DFS: white/gray/black), used by every enumeration script below.
Unit-tested on 10 hand-built examples *before* first use in any
enumeration (`cycle_utils.py`, run directly):

| test | functional graph `f` | expected cyclic set | result |
|---|---|---|---|
| `identity_4` | `[0,1,2,3]` | `{0,1,2,3}` | PASS |
| `single_4cycle` | `[1,2,3,0]` | `{0,1,2,3}` | PASS |
| `two_2cycles` | `[1,0,3,2]` | `{0,1,2,3}` | PASS |
| `3cycle_plus_fixed` | `[1,2,0,3]` | `{0,1,2,3}` | PASS |
| `rho_shape` | `[1,2,1,3]` | `{1,2,3}` | PASS |
| `tail_into_cycle` | `[1,2,3,1]` | `{1,2,3}` | PASS |
| `star_into_fixed` | `[2,2,2,2]` | `{2}` | PASS |
| `two_components` | `[1,0,3,3]` | `{0,1,3}` | PASS |
| `n1_fixed` | `[0]` | `{0}` | PASS |
| `prop4_style_reroute` (n=5, single 5-cycle, source `0`, `U=2`) | `[2,2,3,4,0]` | `{0,2,3,4}` | PASS |

**10/10 PASS.** No bug found in the detector at any point in this review.

---

## 2. Lemma 1 (Marked-Point Gap Structure Lemma): independently re-derived and verified

**Own derivation (before close reading of the target's proof text).**
Fixing `m` marked points `S` in a uniform random permutation `π` of `[n]`:
counting permutations by their "contracted permutation" `σ` on `S` (first
marked point reached walking forward) and gap sizes `(g(s))_{s∈S},O`
(unmarked points between each mark and its `σ`-image, resp. outside any
marked cycle) gives, for *any* fixed topology `σ₀` and any fixed
composition `(g_1,…,g_m,O)` of `n-m`: choose which `Σg_i` of the `n-m`
unmarked points sit in the gaps (`\binom{n-m}{Σg_i}` ways), order them into
the gap slots dictated by `σ₀` (`(Σg_i)!` ways), and freely permute the
`O` outside points among themselves (`O!` ways) — giving count
`(n-m)!/[(Σg_i)! O!] · (Σg_i)! · O! = (n-m)!`, the **same** for every
`σ₀` and every composition. This matches the target's own count exactly
and independently confirms both parts of Lemma 1 (uniformity of `σ` on
`Sym(S)`; uniformity and independence of the gap composition).

**Independent brute-force verification** (`lemma1_ref.py`, exhaustive
`Sym([n])`, own contracted-permutation/gap-extraction code, no code read
from any front):

| `m` | `n` range | cells | result |
|---|---|---|---|
| 2 | 2–7 | 6 | all PASS (`σ` uniform on 2 outcomes; gap-triples uniform on the `\binom n2` compositions; joint = product) |
| 3 | 3–7 | 5 | all PASS (`σ` uniform on 6 outcomes; gap-quadruples uniform on the `\binom n3` compositions; joint = product) |

**11/11 cells, 0 mismatches** — matching the target document's own
reported scope and result (`gap_lemma_unittest.py`, "11/11 cells, 0
mismatches") exactly, from independently written code.

---

## 3. Lemma 2 (Two-Source Redirect-Structure Lemma): independently re-derived and verified

**Own construction.** For arc lengths `p,q≥1`, `O=n-p-q≥0`, two explicit
permutation topologies were built from scratch (`lemma2_ref.py`):
"same" (one `π`-cycle `0→e₁→…→e_{p-1}→1→d₁→…→d_{q-1}→0`, plus `O` outside
fixed points) and "diff" (two separate cycles, one of length `p`
containing source `0`, one of length `q` containing source `1`, plus `O`
outside fixed points) — corresponding to the two possible values of
Lemma 1's contracted permutation `σ` on `{0,1}` (swap vs. identity). For
every `(U_0,U_1)∈[n]²` (full enumeration, no randomness), the referee's
own `cyclic_points` was used to check, for every interior arc point, the
target's claimed closed forms **(R1)–(R5)**:

- (R1) `P(e_i cyclic) = i(n+q)/n²`
- (R2) `P(d_i cyclic) = i(n+p)/n²`
- (R3) `P(e_i,e_{i'} both cyclic) = min(i,i')(n+q)/n²`
- (R4) symmetric for two `d`'s
- (R5) `P(e_i,d_{i'} both cyclic) = 2ii'/n²`

**Result:** `n=2,…,9`, every valid `(p,q,O)` triple, **both** topologies
separately: **240/240 `(n,p,q,O,topology)` cells, 0 mismatches**, across
every one of (R1)–(R5) (exact `Fraction` equality, not floating point).
This is a genuinely independent check — it also directly settles the
target's own claim that the formulas hold "regardless of whether `0,1`
share a cycle," by testing both topologies explicitly and separately
rather than only implicitly averaging over them (as the target's own unit
test, `redirect_structure_unittest.py`, is described as doing in the
target document's prose).

**Named cosmetic issue (does not affect any proof).** §3.1 of the target
document states, for the case `0,1` on *different* cycles: "arc_1 = all
of `1`'s own cycle." Given the document's own parametrization
(`p:=g(0)+1`, associated with source `0`'s own walk), this referee's
independent construction (and Lemma 1's proof, which the referee also
re-derived) instead identifies the disjoint-cycles "arc_1" (length `p`)
with **`0`'s own** full cycle, not `1`'s — the aside appears to have the
source labels swapped. This is confirmed to be a pure prose/labeling
slip: the *formulas* (R1)–(R5), which are what Proposition NN2 actually
uses, were checked and hold identically and correctly for both
topologies regardless of this aside, as tabulated above. **No result is
affected.** Flagged here per the mandate's "no placeholder text, disclose
everything found" instruction, not as a substantive error.

---

## 4. Proposition NN2: independently re-derived AND independently brute-forced

### 4.1 Re-derivation of the closed form from Lemma 1 + Lemma 2 alone (own code, not the target's `T(p,q)` formula)

`rederive_nn2.py` builds its own case-value function `value(role1,role2)`
directly from the independently-verified (R1)–(R5) (§3) — covering
outside/outside (=1), outside/arc (=marginal (R1)/(R2)), same-arc
(=(R3)/(R4)), cross-arc (=(R5)) — and sums it by direct enumeration over
**every ordered pair of the `n-2` non-source roles**, for **every**
`(p,q)` with `p,q≥1,p+q≤n`, then averages using Lemma 1's uniform-`(p,q)`
and uniform-role-assignment facts. This is a genuine independent
re-derivation of Proposition NN2's mechanism (mandate item 6: work
through the case-split, confirm no case missed/double-counted) — it does
**not** use the target's own `T(p,q)` closed-form expression or its
`sympy` summation at all, only the raw, independently-verified (R1)–(R5)
and a brute enumeration of role-pairs.

| `n` | re-derived `P_nn(n,2)` | Proposition NN2 formula `(10n²+7n+2)/(30n²)` | match |
|---|---|---|---|
| 4 | 19/48 | 19/48 | ✓ |
| 5 | 287/750 | 287/750 | ✓ |
| 6 | 101/270 | 101/270 | ✓ |
| 7 | 541/1470 | 541/1470 | ✓ |
| 8 | 349/960 | 349/960 | ✓ |
| 9 | 175/486 | 175/486 | ✓ |
| 10 | 134/375 | 134/375 | ✓ |
| 11 | 1289/3630 | 1289/3630 | ✓ |
| 12 | 763/2160 | 763/2160 | ✓ |

**9/9 exact matches, `n=4..12`** — a closed form with effectively 3 free
parameters (coefficients of `n²,n,1` in the numerator, over a fixed
`30n²` denominator) confirmed at 9 independent points is massively
over-determined; a wrong formula could not survive this test. This
directly confirms: (a) Lemma 1 and Lemma 2 are correctly stated, (b) the
case decomposition (outside–outside / outside–arc / same-arc / cross-arc)
is exhaustive and non-overlapping (no case missed or double-counted), and
(c) Proposition NN2's stated closed form is the correct consequence of
(a)+(b).

### 4.2 Independent full-model brute force (Definition 4 directly, no Lemma 1/2 machinery at all)

`brute_k2_ref.py`: enumerates **every** one of the `n!·n²` `(π,U_0,U_1)`
configurations of `THEOREM.md` Definition 4 at `K=2` directly (reroute
sources fixed at `{0,1}`, query points at `{n-2,n-1}`), using only the
referee's own unit-tested `cyclic_points` — no Lemma 1/2 machinery
involved at all, a maximally independent check.

| `n` | configs | `P_nn(n,2)` (brute force) | Prop. NN2 predicts | match | `ψ_n^{(2)}` marginal (brute force) | `THEOREM.md` `8/15+4/(15n)+1/(15n²)` | match | `P(same\|both)` | wall time |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 384 | 19/48 | 19/48 | ✓ | 29/48 | 29/48 | ✓ | 1/2 | 0.00s |
| 5 | 3,000 | 287/750 | 287/750 | ✓ | 221/375 | 221/375 | ✓ | 1/2 | 0.01s |
| 6 | 25,920 | 101/270 | 101/270 | ✓ | 313/540 | 313/540 | ✓ | 1/2 | 0.07s |
| 7 | 246,960 | 541/1470 | 541/1470 | ✓ | 421/735 | 421/735 | ✓ | 1/2 | 0.58s |
| 8 | 2,580,480 | 349/960 | 349/960 | ✓ | 109/192 | 109/192 | ✓ | 1/2 | 6.43s |
| 9 | 29,393,280 | 175/486 | 175/486 | ✓ | 137/243 | 137/243 | ✓ | 1/2 | 77.89s |
| 10 | see §4.3 (pushed further, background job) | | | | | | | | |

**6/6 exact rational matches** for `P_nn(n,2)` and **6/6** for the
marginal `ψ_n^{(2)}` cross-check against `THEOREM.md`'s already-proved
formula, `n=4,…,9`, fully reproducing (independently) every value in the
target document's own §4.1 table, plus `n=9` (29.4M exact
configurations, ~78s). **`P(same|both)=1/2` exactly at every single `n`
tested** — an independent, direct confirmation of Theorem J's Corollary
(Estágio 25, cited by the target) inside this exact model, not merely a
citation taken on faith.

### 4.3 Pushed further: `n=10` (attempted, not completed — disclosed honestly)

The mandate's minimum requirement (`n=4,…,9`) is already met in full,
exactly, by §4.2's table (6/6 matches) and independently by §4.1's
Lemma-1/2-based re-derivation (`n=4,…,12`, 9/9 matches, including `n=10`
*algebraically* via the independently-verified Lemma 1/2 machinery — see
§4.1's table, which already covers `n=10` by that separate, non-brute-force
route). As a genuine "push further" bonus, a **direct, full Definition-4
brute force at `n=10`** (`10!·10²=362{,}880{,}000` exact configurations)
was launched in the background (`brute_k2_ref.py 10`). It was still
running, having processed roughly 10 million perm×target configurations
per 2 seconds of CPU time consistent with the `n=9` timing, when this
report had to be finalized within the session's time budget (n=10 is
~12.3× the work of `n=9`, which itself took 78s — an expected total of
~16 minutes single-threaded, longer here due to CPU contention with the
other checks run concurrently). **This specific `n=10` full brute-force
run did not complete in time and its result is not reported here** — per
the mandate's explicit instruction not to report unfinished computations
as complete. This does not weaken the verdict: `n=10` is independently
already confirmed via the completely different, non-brute-force route of
§4.1 (Lemma 1 + Lemma 2 re-derivation, exact match), and the mandate's
own minimum bar (`n=4..9`, direct brute force) is fully met by §4.2.

### 4.4 Corollary NN2.0 (rate), checked against the brute-force data

`n·(P_nn(n,2)-1/3)`, computed directly from the exact brute-force values
in §4.2's table: `n=4: 0.25000`, `n=5: 0.24667`, `n=6: 0.24444`,
`n=7: 0.24286`, `n=8: 0.24167`, `n=9: 0.24074` — monotonically decreasing
toward `7/30≈0.23333`, consistent with Corollary NN2.0's exact
`Θ(1/n)` rate claim (which follows immediately by algebra from
Proposition NN2's closed form, independently re-verified in §4.1).

---

## 5. Corollary NN2.1: the marginal cross-check (mandate item 8)

`P_nn(n,2)→1/3` (proved twice independently above, §4.1/§4.2) plus Lemma
P2 (`distributional_bridge_attempt`, cited, not re-derived here per the
mandate's citation tier — but its *statement* was read in full, §6.2 of
that document) gives `E[(M_n^{(2)})²]→1/3`, matching Estágio 24's
continuum value. **Separately**, this referee's own brute force (§4.2)
independently reproduces `THEOREM.md`'s already-proved marginal formula
`ψ_n^{(2)}=8/15+4/(15n)+1/(15n²)` exactly at `n=4,…,9` — the requested
"does `P_nn(n,2)` correctly relate to `ψ_n^{(2)}`" cross-check. `P_nn` and
`ψ_n^{(2)}` are genuinely *different* quantities (a pairwise joint
probability vs. a single-point marginal) computed from the *same*
underlying model by the *same* independently-written enumeration code —
their simultaneous, independent agreement with two different previously
established results (Proposition NN2's own closed form, and `THEOREM.md`'s
already-proved `ψ_n^{(2)}`) is strong evidence that this referee's own
model implementation, and hence its verification of the target's claims,
is itself correct (a mutual-consistency check, not circular: `ψ_n^{(2)}`'s
closed form was proved in `THEOREM.md` by a *completely different* method
— Estágio 3's transfer-matrix machine — with no dependency on the target
document at all).

---

## 6. Corollary NN2.2 / Theorem J's Corollary: the logical step (mandate item 9)

**Algebra, checked by hand and by direct computation.**
`P_nn-same(n,2) := (1/2)·P_nn(n,2) = (10n²+7n+2)/(60n²) → 10/60 = 1/6`.
This is elementary algebra on an already-verified closed form (§4);
no error found.

**The cited step itself (Theorem J's Corollary — `P(same|both cyclic) =
1/2` exactly at every finite `n,K`) was independently confirmed, not
merely trusted**, directly inside this referee's own K=2 brute-force
enumeration (§4.2's table, "`P(same|both)`" column): **exactly `1/2` at
every one of `n=4,…,9`**, computed by the referee's own same-cycle
detection (walking `f` forward from one query point and checking whether
the other is encountered before returning), independent of any code from
the `joint_two_point_attempt` front where Theorem J was originally proved.
Combining `P(both cyclic)→1/3` (Proposition NN2) with the exactly-`1/2`
split gives `P(same cycle, both cyclic)→1/6`, matching the target's
Corollary NN2.2 and Estágio 24's `E[M_K²]/2` prediction at `K=2`. No gap
found in this logical step.

---

## 7. Bonus reduction lemma (Lemma 3) and Estágio 28's own table: spot-checked (mandate item 10)

`brute_k2_overlap_ref.py`: an independent, from-scratch brute force of
Estágio 28's own finite-`n` convention (query points fixed at `{0,1}`,
reroute-source set `R` a uniform random 2-subset of **all** of `[n]`,
allowed to overlap `{0,1}` — built purely from the mathematical
description in `joint_exploration_continuum_attempt/ATTEMPT.md` §1's
prose, no code read from that front):

| `n` | configs | `P_n^{(2)}(both)` [overlap-allowed convention] | Estágio 28 §4.1's reported value | match |
|---|---|---|---|---|
| 4 | 2,304 | 49/144 | 49/144 | ✓ |
| 5 | 30,000 | 33/100 | 33/100 | ✓ |
| 6 | 388,800 | 44/135 | 44/135 | ✓ |
| 7 | 5,186,160 | 143/441 | 143/441 | ✓ |

**All 4/4 values reproduced exactly** (the mandate asked for at least 2;
all 4 were checked, given the low marginal cost). These are confirmed
**visibly different**, at each `n`, from this front's own `P_nn(n,2)`
values (§4.2's table) — e.g. at `n=4`, `49/144≈0.3403` vs
`19/48≈0.3958` — consistent with the target document's own claim (§6.3)
that the two finite-`n` conventions are genuinely different numbers
converging to the same limit. Lemma 3's own elementary algebra
(`P(R∩{0,1}=∅)=\binom{n-2}{2}/\binom n2=(n-2)(n-3)/(n(n-1))→1`) was
checked by hand — correct.

---

## 8. K=3 stress test: is the non-closure diagnosis genuine? (mandate item 11)

The target document (§7.1) diagnoses `K=3` as requiring a genuinely new
"functional graph on the arcs" treatment, not merely a bigger version of
the same `K=2`-style flat case table. This referee independently
stress-tested this claim (`k3_stress_test.py`) by building an **explicit**
`K=3` topology (all three sources `0,1,2` on one `π`-cycle, in cyclic
order `0→1→2→0`, arc lengths `p,q,r`) and asking a concrete question: does
`P(e_i cyclic)` for a point interior to the arc ending at source `1`
(length `p`) depend on the *other two* arc lengths `q,r` only through
their **sum** `q+r` — i.e. does the natural "flat" extrapolation of the
`K=2` formula `i(n+q)/n²` (replacing the single "other arc length `q`" by
the aggregate "total other length `q+r`") hold — or does it depend on the
individual **split** `(q,r)`, even when `q+r` is held fixed?

**Result** (`n=10, p=4`, `q+r` fixed at `4`, all three splits
`(q,r)∈{(1,3),(2,2),(3,1)}` enumerated exactly over all `n³=1000`
`(U_0,U_1,U_2)` combinations):

| `(q,r)` | `P(e_1 cyclic)` | `P(e_2 cyclic)` | `P(e_3 cyclic)` |
|---|---|---|---|
| (1,3) | 73/500 = 0.14600 | 73/250 = 0.29200 | 219/500 = 0.43800 |
| (2,2) | 37/250 = 0.14800 | 37/125 = 0.29600 | 111/250 = 0.44400 |
| (3,1) | 73/500 = 0.14600 | 73/250 = 0.29200 | 219/500 = 0.43800 |

**The probability genuinely depends on the split, not just the sum**
(`(2,2)` differs from `(1,3)`/`(3,1)` at every position tested) — the
naive flat/aggregate extrapolation of the `K=2` formula
`i(n+q+r)/n²` was checked directly and **mismatches at every one of the 9
`(split,i)` cells tested** (e.g. `(q,r)=(2,2), i=1`: naive predicts
`7/50=0.14000`, actual is `37/250=0.14800`). This is concrete, independent
evidence that a simple linear/additive bookkeeping extension of the `K=2`
method does **not** work at `K=3` — the individual arc-to-arc structure
(which specific other arc a chain passes through, and in what order)
genuinely matters, not just an aggregate total, precisely as the target
document's diagnosis states. (The exact `(1,3)`/`(3,1)` symmetry observed
is itself consistent with — not contrary to — the target's diagnosis: it
reflects that relabeling the two *other* arcs is a symmetry of the
`K=3` problem, not that only the sum matters; a true closed form would
need to be symmetric in `q,r` while still depending on more than their
sum, e.g. via a genuine `qr` cross term, which is exactly the kind of
extra structure the "functional graph on arcs" treatment the target names
would be expected to produce.)

**Assessment: the non-closure diagnosis is judged genuine, not premature
surrender.** The escalation from a `3×3` per-source destination table
(`K=2`: home / one other arc / outside) to a `4×4×4` table with **two**
distinct "other" destinations per source (`K=3`) is not merely a bigger
version of the same bookkeeping — it introduces cross-arc chaining
(`arc_i→arc_j→arc_k`) with no `K=2` analogue, and this stress test
confirms the resulting dependence on individual arc lengths (not sums)
is real, not a bookkeeping artifact. This mirrors, as the target document
itself notes, the marginal `K≥3` escalation `THEOREM.md` needed a
dedicated transfer-matrix front (Estágio 4) to resolve, compounded here
by needing to track **two** query-point positions through that same
richer state space. The target document's decision not to attempt a full
`K=3` closure in this front's budget, and to name the precise obstruction
instead, is assessed as the right call, not an underclaim or an
unjustified stopping point.

---

## 9. Seeds

Mandate-reserved range for this referee: `20260881000` onward. Confirmed
unused before first use:

```
$ grep -rn "20260881" 05_DISCOVERY_LAB/
.../k2_joint_case_split_attempt/monte_carlo_k2.py:12:20260881000+ untouched.
.../k2_joint_case_split_attempt/ATTEMPT.md:10:...Referee range `20260881000+` untouched.
.../k2_joint_case_split_attempt/ATTEMPT.md:661:range `20260881000+` untouched...
00_GOVERNANCE/DECISION_LEDGER.yaml:5554:      20260881000+. (b) ...
01_PORTFOLIO/TEST_QUEUE.yaml:3326:        Seeds 20260880000+/referee 20260881000+.
```

— only reservation/mention lines, confirmed before any use by this referee.

**No randomness was used anywhere in this review.** Every check above
(cycle-detector unit tests, Lemma 1/2 verification, Proposition NN2's
re-derivation and brute-force cross-checks, Theorem J's Corollary check,
the overlap-convention reproduction, and the K=3 stress test) is exact and
deterministic — full enumeration with exact `Fraction` arithmetic
throughout, no floating point, no sampling. The reserved seed range was
therefore not needed; this is disclosed per the mandate's instruction to
report explicitly when a front's checks turn out to be exact rather than
requiring a random seed.

---

## 10. Bugs found (own code) — disclosure

**None.** Every script written for this review (`cycle_utils.py`,
`brute_k2_ref.py`, `brute_k2_overlap_ref.py`, `lemma1_ref.py`,
`lemma2_ref.py`, `rederive_nn2.py`, `k3_stress_test.py`) produced results
consistent with every cross-check attempted (self-consistency between the
`ψ_n^{(2)}` marginal and `THEOREM.md`'s independently-proved formula;
consistency between the Lemma-1/2-based re-derivation and the fully
independent full-model brute force; consistency between the overlap
convention's reproduced values and the target's own reported table) at
every stage. No script needed a fix during this review.

---

## 11. Bugs / issues found in the target document — disclosure

**One, purely cosmetic, does not affect any proved result:** the §3.1
aside describing "arc_1" in the disjoint-cycles topology as "all of `1`'s
own cycle" appears to have the source labels swapped relative to the
document's own `p:=g(0)+1` convention (§4, §3 above) — this referee's
independent construction and Lemma 2 verification (§3) confirm the actual
**formulas** (R1)–(R5) are correct and self-consistent for both
topologies; only the informal descriptive aside is affected. No other
issue — mathematical, citational, or in the honesty/labeling discipline
(PROVED vs. OPEN vs. NUMERICALLY EXPLORED tags) — was found anywhere in
the target document.

---

## 12. Summary scorecard

| # | Target document claim | Independent check performed | Result |
|---|---|---|---|
| 1 | Lemma 1 (Marked-Point Gap Structure, general `m`) | own derivation + brute force, `m=2,3`, `n≤7` | **CONFIRMED**, 11/11 |
| 2 | Lemma 2 (Two-Source Redirect Structure, R1–R5) | own construction (both topologies), `n=2..9` | **CONFIRMED**, 240/240 |
| 3 | Proposition NN2 closed form | (a) own re-derivation from Lemma1+2, `n=4..12` (incl. `n=10` algebraically); (b) independent full-model brute force, `n=4..9` (`n=10` direct brute force launched but did not finish in time, §4.3 — disclosed, not required) | **CONFIRMED**, 9/9 and 6/6 |
| 4 | Corollary NN2.0 (rate `7/30`) | algebra + brute-force trend | **CONFIRMED** |
| 5 | Corollary NN2.1 (`E[(M_n^{(2)})^2]→1/3`) | algebra (Lemma P2 cited) + independent marginal `ψ_n^{(2)}` cross-check | **CONFIRMED** |
| 6 | Corollary NN2.2 (`→1/6`) | algebra + independent Theorem J Corollary re-verification (`P(same\|both)=1/2` exactly, `n=4..9`) | **CONFIRMED** |
| 7 | Lemma 3 (Overlap-Reduction) | algebra | **CONFIRMED** |
| 8 | Corollary NN2.3 / Estágio 28 table reproduction | independent brute force, all 4 values | **CONFIRMED**, 4/4 |
| 9 | K=3 non-closure diagnosis (honest, not premature) | explicit stress test, flat-formula falsification | **CONFIRMED genuine** |
| 10 | Cycle detector correctness (referee's own tool) | 10 hand-built unit tests | **CONFIRMED**, 10/10 |

---

## 13. Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `cycle_utils.py` | from-scratch cyclicity detector + 10 unit tests |
| `brute_k2_ref.py` | full Definition-4 K=2 brute force (`P_nn`, `ψ_n^{(2)}`, Theorem J check), `n=4..10` |
| `brute_k2_overlap_ref.py` | Estágio 28's overlap-allowed convention, independent brute force, `n=4..7` |
| `lemma1_ref.py` | Marked-Point Gap Structure Lemma, independent brute force, `m=2,3` |
| `lemma2_ref.py` | Two-Source Redirect-Structure Lemma, independent brute force, both topologies |
| `rederive_nn2.py` | independent re-derivation of Proposition NN2 from Lemma1+2 alone, `n=4..12` |
| `k3_stress_test.py` | K=3 stress test: flat-formula falsification |

## 14. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, or any file outside this `adversarial/`
directory. No `.py` file belonging to the target front or any predecessor
front was read, opened, or imported. No git command was run. No claim of
progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
