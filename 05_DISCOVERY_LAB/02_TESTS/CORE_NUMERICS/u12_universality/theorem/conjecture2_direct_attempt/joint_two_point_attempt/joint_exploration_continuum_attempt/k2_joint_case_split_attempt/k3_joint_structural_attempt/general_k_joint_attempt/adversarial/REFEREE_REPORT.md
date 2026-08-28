# Adversarial referee report: `general_k_joint_attempt` (DISC-DEC-106)

**Front reviewed:** `GENERAL-K-JOINT-ATTEMPT`, `DISC-DEC-093`, wave 21
front (c). Document under review:
`.../k3_joint_structural_attempt/general_k_joint_attempt_ABANDONED_STALLED_REFEREE/ATTEMPT.md`
(directory renamed by the orchestrating session to mark the original
referee dispatch as stalled/abandoned — see dispatch note; this is a
completely fresh, independent review, not a continuation of any prior
referee's work. Its `adversarial/` subdirectory was empty before this
report.)

**Referee:** fresh dispatch, DISC-DEC-106, no prior context on this
front. Per `05_DISCOVERY_LAB/00_GOVERNANCE/AGENTS.md` §"Separação de
papéis": this review's mandate is to try to refute the front's claims,
not confirm them. **No `.py`/`.log` file belonging to this front (or
any ancestor/sibling front in this lineage) was opened, read, or
imported at any point before every script listed below was written and
run.** Everything below was re-derived from scratch from (a) the prose
of `ATTEMPT.md`, (b) `THEOREM.md`'s Estágio 35 (and the earlier stages
it cites), and (c) `THEOREM.md`'s Definition 4 as directly restated in
`ATTEMPT.md` §1.2. Only after all independent results below were in
hand did this report cross-reference a handful of *other* fronts'
`ATTEMPT.md` prose (never `.py`/`.log` files) to check citation
provenance (see the one LOW finding below) — this is explicitly
permitted by the mandate ("only after your own results are in hand you
may cross-check against the front's scripts if useful"), and even that
narrower cross-reference never touched this front's own scripts or
this front's sibling `pnn_general_k_egf_attempt`'s scripts.

---

## Verdict

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue, at the tier
> claimed.** One finding, LOW severity, citation-precision only, not a
> mathematical error and not affecting any numerical or logical claim
> in the document. Every proposition, corollary, and mechanism claimed
> **PROVED** in `ATTEMPT.md` was independently re-derived and confirmed
> exactly by this referee, via four largely disjoint verification
> routes (below) built entirely from scratch. Every item the document
> scopes as **OPEN** or **NOT ATTEMPTED** is, on inspection, genuinely
> open/not attempted — no overclaiming found, no covert progress on a
> Millennium Problem (there is none to be found: this is finite,
> internal combinatorics on the u12 ensemble, and the document says so
> explicitly and repeatedly).

---

## 1. What was independently re-derived, and how

Four verification routes, each built without reading any of this
front's own scripts, targeting different layers of the claim so that a
defect in one layer could not hide behind agreement in another:

### (a) True brute force of the actual Definition-4 model (`01_truth_bruteforce.py`)

Directly simulates the process as literally described in `ATTEMPT.md`
§1.2 (itself a restatement of `THEOREM.md` Definition 4 under WLOG
fixing by exchangeability): a uniform random permutation `π` of `[n]`,
`K` sources fixed at `{0,...,K-1}`, i.i.d. `Uniform([n])` targets
`U_0,...,U_{K-1}`, `f(i):=U_i` for sources and `f(i):=π(i)` otherwise,
query points fixed at `{n-2,n-1}`. Enumerates **every** `n!·n^K`
configuration exactly (`fractions.Fraction`, no shortcuts, no "arc"
abstraction of any kind — literal per-point forward-iteration
cyclicity test) and computes `P_nn(n,K)` as an exact ratio.

Result: **exact match to Propositions NN1–NN5 at every `(K,n)` tested**,
`K=1,\ldots,5`, including the two largest-scale checks in this whole
lineage's `K\ge4` regime: `K=4,n=8` (`165{,}150{,}720` exact
configurations, confirming `P_{nn}(8,4)=25999/107520`, `110`s) and
`K=5,n=7` (`84{,}707{,}280` exact configurations, confirming
`P_{nn}(7,5)=78077/352947`, `56`s). Both of these numbers also happen
to be exactly what `ATTEMPT.md` §6.2's own table reports at the same
cells — an independent implementation landing on the same number to
the last digit of a 6-digit numerator/denominator is not a coincidence.
**Zero mismatches anywhere** (see `01_truth_bruteforce.log`).

### (b) Node-level closed-form check for Mechanism 3 (`02_node_level_formula_check.py`)

Independently re-implements the "destination graph" abstraction
described in `ATTEMPT.md` §3–4 (K source-nodes plus an absorbing DEAD
state) **from the prose only**, and exhaustively enumerates all
`(K+1)^K` destination functions, weighting each by its exact
probability and determining cyclicity by direct forward-traversal
(own code, not the front's shortcut formulas). This is compared,
exactly (`Fraction`), against the claimed closed forms
`P_0(s) = x_s\sum_S|S|!\prod x_u` and
`P_{s,s'}=P_{\text{same}}+P_{\text{disjoint}}` (§4.2–4.3).

Result: **exact match at every one of 26 randomly-sampled `(K,n,L,O)`
configurations spanning `K=1,\ldots,7`** — one `K` value beyond what
`ATTEMPT.md` itself tested at node level (its own Lemma 4/5 node-level
checks stop at `K=6`; this referee's check reached `K=7`, still exact).
Zero mismatches (`02_node_level_formula_check.log`).

### (c) Position-level check of the "landing-uniform" claim (`03_position_level_check.py`)

Independently builds the actual position-by-position functional graph
(not the node abstraction) for concrete small arc-length vectors,
`K=1,\ldots,4`, and verifies **every** single-point and cross-arc
prediction (`P(\text{pos }i\text{ cyclic})=(i/L_s)P_0(s)`, and the
bilinear cross-arc analogue) against direct traversal of the full
`n^K`-configuration space. This is the layer that specifically tests
§4.1's claim that landing position is uniform and independent of cycle
structure — the load-bearing simplification that keeps the whole
derivation tractable in general `K`.

Result: **exact match, every position, every pair, every configuration
tested** (`03_position_level_check.log`).

### (d) Independent K-fold assembly, reaching K=6 (`04_independent_assembly.py`)

Built on top of (b) and (c)'s already-verified ingredients (own
re-implementation, not copied from any front's assembly script), this
enumerates every composition `(L_0,\ldots,L_{K-1},O)` of `n-K` into
`K+1` parts exactly (there are `\binom nK` of them — Lemma 1's cited
count, confirmed structurally by assertion in the code), assembles
`T(L)` from the position-level formulas, and averages to get
`P_{nn}(n,K)` for concrete `(n,K)`.

**This is the route that reaches the one place true brute force cannot
(`K=6`, where `n!\cdot n^6` at the minimum valid `n=8` is astronomically
large — `ATTEMPT.md` §6.2 itself disclosed this and did not attempt
it, honestly).** Compared against Propositions NN1–NN6:

| K | n values checked | points | polynomial degree | result |
|---|---|---|---|---|
| 1 | 3–14 | 12 | 1 | all match |
| 2 | 4–14 | 11 | 2 | all match |
| 3 | 5–15 | 11 | 3 | all match |
| 4 | 6–16 | 11 | 4 | all match |
| 5 | 7–17 | 11 | 5 | all match |
| 6 | 8–16 (interactively; 8–14 in the archived log for wall-time) | 9 (7 archived) | 6 | all match |

A degree-`K` rational-function numerator cannot agree with a genuinely
different one at more than `K` points — every row above checks at
`K+5` or more independent points, so this is not a coincidental match
at a handful of cherry-picked `n`. **Zero mismatches**
(`04_independent_assembly.log`; the K=6 wide-range run's console output
is reproduced verbatim in this report's §2 below since the archived
log uses a trimmed range for wall-time reasons).

### (e) Theorem J Corollary spot-check (`05_same_cycle_check.py`)

Re-tests, on fresh raw brute-force data (extending script (a)), the
claim underlying Corollaries NN4.2/NN5.2/NN6.2 — "`P(\text{same
cycle}\mid\text{both cyclic})=1/2` exactly, at every finite `n,K`."

Result: **exactly `1/2` at every one of 7 tested `(K,n)` cells,
`K=1,\ldots,4`** (`05_same_cycle_check.log`).

---

## 2. K=6 wide-range assembly run (interactive, not in the archived log)

The archived `04_independent_assembly.log` trims the `K=6` range to
`n=8..14` (7 points, the minimum needed to pin a degree-6 numerator) to
keep the default run's wall-time bounded. Interactively, this referee
also ran `n=8..16` (9 points) before trimming the script for the
archive copy; the full session transcript:

```
K=6 n=8  time=0.04s match=True
K=6 n=9  time=0.15s match=True
K=6 n=10 time=0.49s match=True
K=6 n=11 time=1.29s match=True
K=6 n=12 time=2.98s match=True
K=6 n=13 time=6.40s match=True
K=6 n=14 time=12.15s match=True
K=6 n=15 time=22.05s match=True
K=6 n=16 time=38.09s match=True
ALL OK
```

**This is, to this referee's knowledge, the first independent
confirmation of Proposition NN6 by any route other than the front's
own — since true brute force is infeasible for K=6 for both parties,
this K-fold-assembly route (built from independently-verified
node/position-level ingredients) is the strongest verification
available for that Proposition, and it holds up.**

---

## 3. Rigor of the K=3 → general-K generalization: what is proof, what is verified pattern, what is honestly open

Per the mandate's item 2, an explicit breakdown:

- **Mechanism 1 (Governing-Source Reindexing) and Mechanism 2 (Lemma 4,
  Cycle-Predecessor Uniqueness):** claimed "PROVED for general K,
  literally the same proof as K=3 with 3 replaced by K." This referee
  agrees this is a genuine proof, not a verified-pattern claim: the
  cited argument (exchangeability of K symmetric random variables under
  relabeling, for Mechanism 1; a standard fact about functional graphs
  on any finite node set plus one absorbing sink, for Mechanism 2)
  never uses the number 3 or any specific K in its logic — this
  referee's own reading of the argument concurs it is K-free. The
  document's own verification of these two mechanisms is exhaustive
  enumeration at concrete `K` (up to 5–6), which is appropriately
  labeled a **sanity check of a general proof**, not offered as the
  proof itself — correctly scoped.

- **Mechanism 3 (the Lemma 5 analogue, §4):** this is the document's
  own "genuinely new" claim, and this referee's independent route (b)
  above — a from-scratch re-implementation of the underlying
  destination-graph model, not a transcription of the front's cycle-sum
  formula — reaches the same closed form exactly at every tested `K`
  up to 7. That the derivation route in `ATTEMPT.md` (an explicit
  cycle-sum / inclusion argument) and this referee's route (direct
  enumeration + traversal) are structurally different and agree exactly
  is strong evidence the claimed formula is a real identity, not an
  artifact of one particular way of counting.

- **The assembly algorithm (§5):** proved correct **as an algorithm**
  for general `K` (a program, given any `K`, produces the exact closed
  form) — not reduced to a single closed-form-in-`K` expression. The
  document is explicit and correct about this distinction throughout
  (§8.1's "headline non-closure"); this referee's route (d) confirms
  the algorithm's *output* is correct at `K=1,\ldots,6` by an
  independent assembly, which is exactly the right level at which to
  test an "algorithm, not formula" claim.

- **Propositions NN4, NN5, NN6 (concrete new closed forms):** genuinely
  PROVED, not merely conjectured-and-checked — the document derives
  them by full symbolic K-fold summation (their own route) and this
  referee confirms them by a structurally different route (own
  destination-graph + composition-sum implementation) at many points
  each, plus true brute force for NN4 (three n values, up to 165M
  configs) and NN5 (one n value, 84.7M configs). NN6 has no true brute
  force from either party (correctly disclosed as infeasible by the
  front) but is confirmed by this referee's independent assembly route
  at 9 values of `n`.

- **What the document correctly leaves open, verified as genuinely
  open, not just labeled so:** a single closed-form-in-`K` formula for
  `P_{nn}(n,K)` (§8.1–8.2); a closed form or even a conjectured pattern
  for the rate coefficient `c_1(K)` (§8.3 — this referee re-derived the
  six `c_1(K)` values from the confirmed closed forms by elementary
  fraction simplification and confirms they match the table exactly,
  but agrees six points is thin evidence and no pattern is evident by
  inspection — the document's restraint here, explicitly citing its own
  earlier disclosed near-miss with premature pattern-fitting as the
  reason for caution, is the correct call); `K=7` and beyond (no
  closed-form polynomial claimed anywhere for `K=7` — confirmed by
  grep, only the *method* is asserted general there, and this referee's
  own node-level check (b) independently supports that the *method*
  specifically continues to hold at K=7, without extending this to any
  claim about a K=7 polynomial, matching the document's own scoping
  exactly).

**Overall: this is a real proof of a genuine generalization for the
two flagged mechanisms and the new Lemma-5-analogue, plus a real
algorithm (proved correct in general, executed concretely through
K=6), with an honestly-scoped, correctly-diagnosed non-closure at the
single hardest remaining step (a free-K formula) — not a
pattern-matched extrapolation dressed up as a proof.**

---

## 4. One finding: LOW severity, citation-precision only

**§5.2's self-consistency table cites the `K=1` baseline
`P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` as "(Estágio 27)."** This referee
traced the actual provenance across the lineage (only after all
independent numerical work above was complete):

- `THEOREM.md` Estágio 27 (`distributional_bridge_attempt`) does
  contain this exact formula, at its own §7.1(c) — but there it is
  explicitly labeled **"exact-verified pattern (`n=3,\ldots,9`,
  rational arithmetic), not proved for general `n` in this document"**
  (`distributional_bridge_attempt/ATTEMPT.md` line 740's own scorecard
  wording).
- The actual **proof** of this formula (a full case-split derivation,
  not a numeric pattern) appears one stage later, in Estágio 28
  (`joint_exploration_continuum_attempt/ATTEMPT.md` §3.2), as `V_a(n)`
  — the Case-(a)-conditional probability (reroute source disjoint from
  the two query points), which is *exactly* the quantity `P_{nn}(n,1)`
  denotes under this whole sub-lineage's fixed-disjoint-sources
  convention (confirmed: `V_a(n)=(3n+1)/(6n)`, algebraically identical
  to `1/2+1/(6n)`).
- The direct predecessor two stages up, `k2_joint_case_split_attempt`,
  is scrupulously careful about this: it cites **both** sources jointly
  when making the same point ("`P_{nn}(n,1)=\tfrac12+\tfrac1{6n}` ...
  `distributional_bridge_attempt` §7.1(c) vs `joint_exploration_
  continuum_attempt` §3.2" — line 565–568 of its `ATTEMPT.md`), and
  elsewhere is explicit that `P_{nn}` (the fixed-disjoint-sources
  convention this whole lineage uses) is a genuinely different
  finite-`n` quantity from Estágio 28's own overlap-allowed
  `P_n^{(K)}(\text{both})` convention — a distinction this referee
  independently confirms is real and correctly maintained throughout
  `general_k_joint_attempt/ATTEMPT.md` (its own model, §1.2, is
  unambiguously the fixed-disjoint convention, matching `P_{nn}`, not
  Estágio 28's `P_n^{(K)}`).

**Net effect: `general_k_joint_attempt`'s citation "(Estágio 27)" for
the K=1 row names the stage that first *states* the formula (as a
numerically-verified pattern) rather than the stage that first *proves*
it (Estágio 28, `V_a(n)`) — a citation-precision slip, not a
mathematical error.** The value itself is correct (independently
reconfirmed by this referee's own true brute force at `n=3,4,5` — see
`01_truth_bruteforce.log`) and is, in fact, proven somewhere in the
archive (just not at the cited location). This is the same class of
minor, narrative-only slip this lineage's referees have repeatedly
flagged as LOW severity without affecting any verdict (e.g. Estágio
32's divergence-onset-point mislabel, Estágio 35's own predecessor's
"closer to the tail" inversion) — named here in that same spirit, for
a dated addendum, not as grounds to weaken the verdict.

**No other citation, formula, or claim in `ATTEMPT.md` was found to
have any defect** — every other cross-reference checked against
`THEOREM.md` (Estágio 18's item (iii), Estágio 24's `E[M_K^2]=1/(K+1)`
for all K, Estágio 27's Lemma P2 general-K second-moment reduction,
Estágio 31's Proposition NN2, Estágio 35's Proposition NN3 and its own
referee report) matches exactly.

---

## 5. Honest-scoping and Millennium Problem check

- Every claim in `ATTEMPT.md` is labeled PROVED / OPEN / NOT ATTEMPTED
  at the point of use (confirmed by direct reading, cross-checked
  against §11's scorecard — all 12 rows match their in-body labels).
- No item claimed PROVED in this document was found by this referee to
  be merely a checked-and-extrapolated pattern; conversely, no item
  scoped OPEN or NOT ATTEMPTED was found to actually be closed by the
  document's own machinery (in particular, this referee explicitly
  checked that no `K=7` closed-form polynomial is claimed anywhere —
  grep-confirmed, §8.5 is honest about this being a compute-budget
  choice, not a mathematical wall, and the method-level K=7 check this
  referee performed independently supports that framing without
  crossing into an unearned K=7 *result* claim).
- "No claim of progress on any Millennium Problem" appears repeatedly
  (title, executive summary, §8.6, §12) and is accurate: this document
  is entirely internal, finite combinatorics on the u12
  random-permutation-with-reroutes ensemble defined in `THEOREM.md`
  Definitions 1–4. Nothing in the mathematical content touches, even
  indirectly, any Millennium Problem.
- Seed range: the front's own reserved range `20260904000`-`20260904999`
  (used only for §6.4's bonus Monte Carlo triangulation, sub-seeds
  `20260904001`-`20260904006`) is confirmed via a fresh `grep` by this
  referee to be unused elsewhere in the archive before this front's
  files, exactly as `ATTEMPT.md` §9 claims. (Informational per this
  review's own mandate — not a finding either way.)

---

## 6. Scope discipline (this referee)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, or `ATTEMPT.md`
itself. No `git` command run. All independent verification code written
fresh in this referee's own scratch directory first, then copied
verbatim into this `adversarial/` directory alongside its run logs;
`ATTEMPT.md`'s own scripts were never opened.

## 7. Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `01_truth_bruteforce.py` / `.log` | true, from-scratch brute force of the full Definition-4 model; confirms Propositions NN1–NN5 exactly, `K=1..5` |
| `02_node_level_formula_check.py` / `.log` | independent destination-graph re-implementation confirming the Lemma-5-analogue node-level formulas, `K=1..7` |
| `03_position_level_check.py` / `.log` | independent position-level functional-graph check confirming the landing-uniform / linear-in-position claim, `K=1..4` |
| `04_independent_assembly.py` / `.log` | independent K-fold composition-sum assembly, confirming Propositions NN1–NN6 (including K=6, unreachable by true brute force) at many `n` each |
| `05_same_cycle_check.py` / `.log` | independent confirmation of the Theorem J Corollary (`P(\text{same}\mid\text{both cyclic})=1/2` exactly) underlying Corollaries NNK.2 |
