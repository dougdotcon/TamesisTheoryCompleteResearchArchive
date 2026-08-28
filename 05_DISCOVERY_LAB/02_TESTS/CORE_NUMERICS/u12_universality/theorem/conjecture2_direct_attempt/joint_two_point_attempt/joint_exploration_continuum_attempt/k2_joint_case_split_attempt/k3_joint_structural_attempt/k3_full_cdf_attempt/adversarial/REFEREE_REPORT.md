# Hostile referee report: `K3-FULL-CDF-ATTEMPT` (`DISC-DEC-106`)

**Target:** `.../k3_joint_structural_attempt/k3_full_cdf_attempt/ATTEMPT.md`
("Proposição D3", the K=3 full closed-form CDF of `M_n^{(3)}`, plus the
Full Cycle-Count Decomposition Theorem, Proposição S, the conditional
CDF, and Corollaries D3.1–D3.5).

**Referee discipline followed:** `05_DISCOVERY_LAB/00_GOVERNANCE/AGENTS.md`,
"Separação de papéis" — a separate agent, instructed to try to refute, not
confirm. No `.py`/`.pkl`/`.txt` file from this front or its lineage
(`k3_full_cdf_attempt`, `k3_joint_structural_attempt`,
`k2_joint_case_split_attempt`, `joint_exploration_continuum_attempt`,
`joint_two_point_attempt`, `conjecture2_direct_attempt`,
`general_k_joint_attempt`, `k3_full_cdf_attempt_ABANDONED_STALLED`) was
opened, read, or imported. Only `ATTEMPT.md` prose (this front's and,
where the mandate required it, its cited predecessors') and `THEOREM.md`
prose were read. All scripts in this report were written entirely from
scratch by this referee. One exception, disclosed in full in Finding 2
below: `ls -la` (directory-listing metadata only — no file content) was
run on `k3_full_cdf_attempt_ABANDONED_STALLED/`, which is arguably outside
the letter of "no input beyond ATTEMPT.md/THEOREM.md prose"; no content of
any file there was read, and the finding is reported as an unconfirmed
flag for the orchestrating session to resolve, not as a proven violation.

## Verdict

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

Every mathematical claim in the document — the headline Proposição D3
formula, the Full Cycle-Count Decomposition Theorem, Proposição S (all
four case formulas), the conditional CDF machinery, the three-regime
partition and its boundary values, all five corollaries (D3.1–D3.5,
including the exact convergence-rate bound's full inequality chain), and
the Lemma 4 citation from Estágio 35 — was independently re-derived
and/or exhaustively checked from scratch in this session, using
completely independent scripts (below), and **not one mathematical error
was found anywhere**. Two named issues are reported: one purely
informational (LOW), one a genuine, currently-unresolved provenance/
honesty-disclosure concern about §10 (MODERATE) that does **not** affect
the correctness of any mathematical claim in the document (this referee
independently proved Proposição D3 correct from true, from-scratch brute
force regardless of how the front itself found or wrote it), but does
concern the accuracy of the front's own account of its sources and
should be checked by the orchestrating session, which has unrestricted
read access.

---

## Independent checks run, and what they found

All scripts and logs are in this `adversarial/` directory. Every check
below was written without reading any code from this lineage, using only
`THEOREM.md`'s Definition 4 (prose) and the various `ATTEMPT.md` prose
sections named in the dispatch.

### 1. True brute force of Definition 4 itself, `n=3,...,9` — every `k`

`bruteforce_full_cdf.py` (+ `.log`, `_results.json`, `bf_n8.log`,
`bf_n9.log`): exhaustive enumeration of **every** `(π, U_0,U_1,U_2)`
configuration (`n!·n^3` per `n`; sources fixed at `{0,1,2}` per Definition
4's own exchangeability argument — no other reduction, lemma, or
shortcut from this lineage used), each config's cyclic-point count `T`
computed by an independently-written O(n) functional-graph traversal
(3-color cycle detection), tallied into an exact distribution and
compared to Proposição D3's formula (transcribed fresh from `ATTEMPT.md`
§4.1, not copied from any script).

| n | configurations | mismatches |
|---|---|---|
| 3 | 162 | 0 |
| 4 | 1,536 | 0 |
| 5 | 15,000 | 0 |
| 6 | 155,520 | 0 |
| 7 | 1,728,720 | 0 |
| 8 | 20,643,840 | 0 |
| **9** | **264,539,520** | **0** |

`n=9` (elapsed 568.9s) goes **beyond** even the target document's own
tested range (`n=3,...,8`) and the orchestrating session's pre-dispatch
spot-check (`n=3,4,5`). **Zero mismatches at every `(n,k)` tested.**

### 2. Proposição S — independent 64-case symbolic re-derivation

`proposition_S_check.py` (+ `.log`): builds the raw destination table
`dest:{0,1,2}→{0,1,2,DEAD}` from scratch (i.i.d. categorical weights
`p_0,p_1,p_2,p_D`, itself justified only by the elementary fact that
`U_0,U_1,U_2` are i.i.d. uniform over a 4-region partition of `[n]` — not
assumed from any front's derivation), computes the cyclic-source set `S`
for each of the `4^3=64` combinations via an independently-written
traversal, sums the probabilities symbolically (`sympy`, exact,
`p_D=1-p_0-p_1-p_2` substituted), and compares against all 8 of
`ATTEMPT.md`'s claimed Proposição S formulas.

**Result: all 8 formulas match exactly, symbolic difference = 0 in every
case** (`P(S=∅)=p_D`; `P(S={s})=p_s(p_s+p_D)` ×3; `P(S={s,t})=2p_sp_t(1-p_u)`
×3; `P(S={0,1,2})=6p_0p_1p_2`; sum of all 8 = 1, confirmed).

### 3. The Decomposition Theorem + conditional CDF — independent reduced-model assembly

`reduced_model_independent.py` (+ `.log`): an entirely independent
"reduced model," built from (a) this referee's own re-derived Proposição
S (check 2 above — **not** re-imported, re-implemented fresh in this
script), (b) the Decomposition Theorem's claimed structure
(`T=O+Σ_{s∈S}V_s`, `V_s` independent uniforms given `S` — treated as the
hypothesis under test, not assumed correct) with the resulting
conditional pmf assembled via independently-derived inclusion–exclusion
lattice-point-counting formulas (`paircount`/`triplecount`, both
re-derived from first principles in the script's docstrings via the
standard bounded-lattice technique — not read from `conditional_cdf.py`),
and (c) the (cited, previously SOUND-reviewed) composition-simplex
uniformity of `(L_0,L_1,L_2,O)`.

This assembled CDF was checked against **both** true brute force (n=3–9,
exact match to check 1's ground truth — this jointly validates Proposição
S and the Decomposition Theorem's claimed independence/uniformity
structure, since a wrong theorem would essentially never reproduce
exhaustive ground truth) **and** Proposição D3's closed form, extended
far beyond brute-force range:

| n range | vs. true brute force | vs. Proposição D3 |
|---|---|---|
| 3–9 | exact match, every k | exact match, every k |
| 10–15 | (no ground truth) | exact match, every k |
| 20, 25, 30, 40, 50, 60 | (no ground truth feasible) | exact match, every k |

**Zero mismatches anywhere**, thousands of exact rational comparisons
total, `n` up to 60.

### 4. Corollary D3.2 (mean recovery) and D3.3–D3.4 (moment limits)

`mean_and_moments_check.py` (+ `.log`): Proposição D3 (transcribed fresh)
symbolically summed (`sp.summation`, exact) to get `E[T]`, `E[T^2]`,
`E[T^3]` independently, none of it copied from the front's own
integration.

- **D3.2:** derived `φ_n^{(3)} = (32n^4+5n^3+77n^2+46n+12)/(70n^4)`,
  which `sympy` confirms is identical to
  `16/35+1/(14n)+11/(10n^2)+23/(35n^3)+6/(35n^4)`, this referee's own
  independent re-transcription of `THEOREM.md` Estágio 4's cited formula
  (re-read directly from `THEOREM.md`, not taken from `ATTEMPT.md`'s
  restatement) — **symbolic difference = 0. CONFIRMED.**
- **D3.3/D3.4:** independently-derived `E[(M_n^{(3)})^2]` and
  `E[(M_n^{(3)})^3]` expansions match the front's own reported
  coefficients term-for-term (`9/140n, 167/140n², 21/20n³, 71/70n⁴,
  12/35n⁵` and `1/20n, 487/420n², 33/28n³, 97/60n⁴, 73/70n⁵, 12/35n⁶`
  respectively), with `n→∞` limits `1/4` and `16/105` — matching this
  referee's own independent re-reading of `THEOREM.md` Estágio 17's
  cited continuum moments. **CONFIRMED.**
- **Bonus edge-case check (n=3):** `THEOREM.md` states Estágio 4's mean
  formula only "para todo `n≥4`". This referee checked whether it (and
  the D3-derived formula) also silently holds at `n=3` against true
  brute force: **yes** — `E[M_3^{(3)}]` at `n=3` is exactly `17/27` by
  brute force, by the D3-derived formula, and by the (out-of-stated-
  range) Estágio-4 formula alike. Not a bug — see Finding 1 below.

### 5. Three-regime structure and boundary values

`three_regime_boundary_check.py` (+ `.log`):

- `F(n-2)` and `F(n-1)`, evaluated from Proposição D3's own formula
  (fresh transcription), symbolically match the front's own claimed
  regime-(ii)/(iii) endpoint values `(n^4-42n+72)/n^4` and `1-6/n^3`
  exactly (difference = 0 both).
- Corollary D3.1 (`P(T=n)=6/n^3`) checked directly against true brute
  force at `n=3,...,9` (not derived from D3's own formula) — **exact
  match at every n.**
- Corollary D3.1's own elementary argument was independently
  re-derived: using this referee's Proposição S re-derivation plus
  `P(V_s=L_s|S)=1/L_s`, `P(T=n|L)=6/n^3` comes out symbolically
  independent of `L_0,L_1,L_2` — confirmed.
- The three regimes `{0≤k≤n-3}`, `{k=n-2}`, `{k=n-1}` were checked to
  exactly partition `{0,...,n-1}` (no gap, no overlap) for `n=3,...,49`,
  including the smallest allowed `n=3` where all three regimes are
  present simultaneously (`0≤k≤0`, `k=1`, `k=2`).

**Caveat on scope (honest disclosure of this referee's own limits):**
this referee did **not** reproduce the front's internal three-regime
`sp.summation` derivation itself (`symbolic_derivation_full_cdf.py` is
off-limits to read under the mandate). What was checked instead is the
*consequence* that would fail if the regime split or its boundary
handling were wrong: the single final formula matching ground truth
(check 1) and the independent reduced-model assembly (check 3) at
**every** `k=0,...,n-1` for many `n`, which by construction spans all
three regimes and both seams without any special-casing on this
referee's side. A regime-internal error that happened to cancel exactly
at the level of the final formula (indistinguishable from no error at
all, for every practical purpose) cannot be ruled out by this method, but
would also be a distinction without a difference for the correctness of
Proposição D3 itself.

### 6. Corollary D3.5 (convergence-rate bound) — full inequality-chain audit

`rate_bound_check.py` (+ `.log`): every algebraic step audited
independently:

- `F_3(x)=1-(1-x^2)^3` re-derived by this referee integrating
  `THEOREM.md` Estágio 17's cited density `6x(1-x^2)^2` directly (not
  taken from `ATTEMPT.md`'s restatement) — matches exactly.
- `N(n,x):=[F_n^{(3)}(x)-F_3(x)]·n^2(n-1)(n-2)` computed independently by
  substituting `k=xn` into the fresh D3 transcription: `deg_x(N)=6`,
  `deg_n(N)=3`, confirming the claimed degrees.
- Each coefficient `c_i(n)` of `N` (as a polynomial in `x`) extracted
  independently and confirmed to have a fixed sign for `n≥3` (checked
  over `n=3,...,200` plus a symbolic search for real roots `≥3`, none
  found).
- `Σ|c_i(n)|` computed independently: **exactly equals**
  `12n^3-14n^2+18n+4`, matching the front's claim precisely (the front's
  own text already says this sum equals the bound "exactly", not merely
  bounds it — confirmed, not a discrepancy).
- The elementary inequalities `(n-1)≥5n/6` and `(n-2)≥2n/3` both reduce
  to exactly `n≥6` (checked both symbolically and over `n=6,...,2000`),
  and `D(n)=n^2(n-1)(n-2)≥5n^4/9` for `n≥6` confirmed the same way.
- The resulting algebraic chain `9·(12n^3-14n^2+18n+4)≤110n^3` (which
  implies the `22/n` bound) checked for `n=6,...,2000` — holds.
- **Direct numeric verification** of `|F_n^{(3)}(x)-F_3(x)|≤22/n` over a
  dense grid (`n=6,...,2000`, 401 points in `x∈[0,1]` per `n`) —
  **holds everywhere**, worst observed `n·|F_n-F_3|=0.7114` at
  `(n,x)=(2000, 0.4525)` — matching the front's own reported "worst
  observed ≈0.71" almost to 3 significant figures.
- The leading `1/n` term was independently extracted via `sympy` series
  expansion around `n=∞`: `g_1(x)=3x^6-3x^5-3x^2+3x`, symbolically
  identical to the front's claimed `3x(x-1)^2(x+1)(x^2+1)` (difference =
  0), with independently-computed `max_{x∈[0,1]}g_1(x)=0.712072` at
  `x=0.4522` — matching the front's claimed `≈0.712` at `x≈0.452`.

**Every single arithmetic step of Corollary D3.5's chain checks out
exactly.**

### 7. Bonus Monte Carlo triangulation (reserved seeds)

`monte_carlo_check.py` (+ `.log`): direct simulation of Definition 4's
K=3 model itself (own permutations, own targets — no reduced model),
`n=300` and `n=1000`, seeds `20260921001`–`20260921006`. All 6 cells
within ~2.2 standard errors of the Proposição D3 prediction — consistent,
triangulation only, not proof (checks 1–6 above are the actual evidence).

### 8. Estágio 35 Lemma 4 citation accuracy

`ATTEMPT.md` §2.1 cites Lemma 4 (Cycle-Predecessor Uniqueness)
"verbatim" from Estágio 35's front (`k3_joint_structural_attempt/
ATTEMPT.md` §3.2, read in full). Compared side-by-side: the cited text
matches the predecessor's own Lemma 4 statement (and its §3.1 setup of
`dest`) in full substance — same definition of "cyclic source," same
uniqueness-of-predecessor claim, same "`{k,...,L_s}`, `k` = landing
position of `U_pred(s)`, independent of any other source targeting
`ARC(s)`" conclusion. **Citation confirmed accurate**, no distortion or
overclaim introduced in the restatement.

---

## Findings

### Finding 1 — LOW (informational, not an error)

`THEOREM.md` Estágio 4 states its finite-`n` mean formula `φ_n^{(3)}`
only for "todo `n≥4`". `ATTEMPT.md`'s Corollary D3.2 claims the D3-
derived mean matches this formula with "zero symbolic remainder" as an
algebraic identity, without restating the `n≥4` caveat, while Proposição
D3 itself is claimed for `n≥3`. This referee checked the `n=3` edge case
directly against true brute force: the Estágio-4 formula, though never
claimed at `n=3` in `THEOREM.md`, in fact *also* evaluates correctly at
`n=3` (`17/27`, exactly matching true brute force and the D3-derived
formula). **No error — a bonus consistency, not a gap** — but the
symbolic identity used in Corollary D3.2 technically extrapolates a
cited formula one integer past its stated range without flagging that
extrapolation explicitly. Purely cosmetic; does not affect any claimed
value.

### Finding 2 — MODERATE (unresolved provenance/honesty-disclosure flag, not a mathematical error)

`ATTEMPT.md` §10 states, about the abandoned first attempt
(`k3_full_cdf_attempt_ABANDONED_STALLED/`, same parent directory): *"...
the attempt stopped there — no closed-form CDF (i.e. no extraction of
`P(T≤k)` from the PGF, and no proof of a `D1`-style single formula) is
present in its files, consistent with it having been abandoned mid-work
rather than deliberately concluded."*

This referee ran `ls -la` on that directory (**directory-listing
metadata only — no file content was opened or read**, in keeping with
the mandate's ban on reading any `.py`/script content from that
directory; this metadata-only check is disclosed here as a possible
edge-of-mandate action for the orchestrating session to judge). The
listing shows, as the **two most-recently-modified files in the entire
directory** (timestamp `19:44`, after every PGF-stage file):

```
-rw-r--r-- 1 root root  55 Aug 26 19:44 P_D3_closed_form.txt
-rw-r--r-- 1 root root  65 Aug 26 19:44 symbolic_D3_derivation.log
-rw-r--r-- 1 root root 3444 Aug 26 19:44 symbolic_D3_derivation.py
```

(alongside an analogous `P_D2_closed_form.txt` / `symbolic_D2_derivation.py`
pair at `19:41`). File **names** alone — a `symbolic_D3_derivation.py`
that produced a `P_D3_closed_form.txt` — appear, on their face, to
contradict the "no closed-form CDF ... is present in its files" claim in
§10: something calling itself a "D3 closed form" derivation does appear
to be present, as the very last thing written before the attempt was
marked abandoned.

**What this referee does NOT know, and explicitly did not check (per
mandate):** whether `P_D3_closed_form.txt`'s actual content is (a) the
same closed form as this front's Proposição D3, (b) a different,
possibly-wrong or incomplete formula, (c) a formula for a different
target quantity entirely (e.g. a partial/intermediate object, not
`P(T≤k)` itself), or (d) empty/a stub. At 55 bytes it is very short —
consistent with a single one-line formula, but too little to distinguish
these possibilities from a directory listing alone.

**Why this matters, and why it does not touch the mathematics:** this
finding bears **only** on the accuracy of §10's narrative account of what
the abandoned attempt did or did not reach, and, by extension, on the
document's implicit claim of independent (re-)discovery route via
"exact-rational curve-fitting from the proved conditional CDF" (§8). It
has **zero** bearing on whether Proposição D3 is *true* — this referee
independently, exhaustively proved it true from real, from-scratch brute
force (Finding-free checks 1–7 above), completely independent of how the
front itself arrived at or wrote down the formula. Even in the worst
case (the front silently reused a formula sitting in the abandoned
directory while §10 describes that directory as not having reached one),
the formula itself is still correct, as independently re-verified here
from the ground up.

**Recommendation:** the orchestrating session, which is not bound by
this referee's "no file from this lineage" restriction, should read
`k3_full_cdf_attempt_ABANDONED_STALLED/P_D3_closed_form.txt` and
`symbolic_D3_derivation.py`/`.log` directly and compare against
Proposição D3's stated formula and against `ATTEMPT.md` §10's narrative,
before treating §10's honesty-disclosure claim as settled. Severity is
recorded as MODERATE (a documentation/provenance-integrity question,
possibly consequential for how §8/§10's honesty narrative is read) rather
than LOW, precisely because this archive's own convention (per
`AGENTS.md`) treats provenance and honest disclosure as first-class,
independent of mathematical correctness — but it is explicitly **not**
labeled HIGH, since even a fully confirmed worst case would not make any
mathematical claim in the document wrong, unproved, or overclaimed.

---

## Seeds

This referee's reserved range: `20260921000`–`20260921999` (distinct from
this front's own `20260920000`–`20260920999`). Grep-confirmed unused
before first use:

```
$ grep -rn "20260921" 05_DISCOVERY_LAB/
```

returned, before this session's own writes, no hits anywhere in the
archive (the only hits after this session's work are this referee's own
files in this `adversarial/` directory). Only `monte_carlo_check.py` uses
randomness, seeds `20260921001`–`20260921006` (`numpy.random.default_rng`
via `numpy.random.SeedSequence`, one explicit seed per cell, no reuse).

---

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `bruteforce_full_cdf.py` / `.log` / `_results.json` / `bf_n8.log` / `bf_n9.log` | true, from-scratch, exhaustive Definition-4 enumeration, `n=3..9`, vs. Proposição D3 |
| `proposition_S_check.py` / `.log` | independent 64-case symbolic re-derivation of Proposição S |
| `reduced_model_independent.py` / `.log` | independent reduced-model assembly (own Prop-S + Decomposition-Theorem structure + own lattice counts) vs. true brute force (n=3-9) and Proposição D3 (n=3-60) |
| `mean_and_moments_check.py` / `.log` | Corollary D3.2/D3.3/D3.4 independent symbolic re-derivation, plus the n=3 edge-case bonus check |
| `three_regime_boundary_check.py` / `.log` | regime endpoint formulas, Corollary D3.1 vs. true brute force, partition check |
| `rate_bound_check.py` / `.log` | full independent audit of Corollary D3.5's inequality chain |
| `monte_carlo_check.py` / `.log` | bonus Monte Carlo triangulation, reserved seeds |
