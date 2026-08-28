# Adversarial referee report: `GENERAL-K-DECOMPOSITION-ATTEMPT` (`DISC-DEC-110`)

**Target document:** `.../general_k_joint_attempt/general_k_decomposition_attempt/ATTEMPT.md`

**Referee discipline followed.** No `.py` file from this front or any front in
its lineage (`general_k_decomposition_attempt`, `general_k_joint_attempt`,
`pnn_general_k_egf_attempt`, `k3_full_cdf_attempt`, `k3_joint_structural_attempt`,
or any other ancestor) was opened, read, or imported at any point. Every
script in this `adversarial/` directory was written from scratch, from
`ATTEMPT.md`'s prose and `THEOREM.md`'s prose only. No edits were made to
`THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `git` command was run. All writes are confined to this
`adversarial/` subdirectory.

**Seed reservation.** `grep -rn "20260924" 05_DISCOVERY_LAB/` was run before
first use (see below) and confirmed the range `20260924001`–`20260924006` is
the only part of the front's own `20260924000`–`20260924999` block already
consumed (by `monte_carlo_bonus.py`); this referee's assigned sub-range
`20260924500`–`20260924799` is untouched. In the event, **no script in this
directory used randomness at all** — every check is exact (symbolic algebra,
exact `Fraction`/`sympy.Rational` brute force, or exhaustive enumeration) —
so the seed range was reserved but not consumed. The confirming grep output:

```
$ grep -rn "20260924" 05_DISCOVERY_LAB/
...general_k_decomposition_attempt/ATTEMPT.md (several lines, this front's own text)
...general_k_decomposition_attempt/monte_carlo_bonus.py:118-119 (seeds 20260924001-20260924006)
...general_k_decomposition_attempt/monte_carlo_bonus.log (same six seeds)
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7329: ... Seeds 20260924000-20260924999.
```

---

## Verdict

> **SOUND — ACCEPT for catalogue.**

No mathematical error was found anywhere in the document. Every claim
labeled PROVED was independently re-derived and/or re-verified by a route
built entirely from scratch; every citation to a prior stage was checked
against that stage's own text and found accurate; the one genuinely
subtle step (the crux algebraic identity `(**)`, and the Key Lemma's
strongest form — independence from the internal split of the escape
weight among multiple flavors) survived the most adversarial stress tests
this referee could construct, including two negative controls that fired
correctly when normalization was deliberately withheld.

---

## What was read (citation-checking pass)

- `ATTEMPT.md` (target document), in full, with close attention to §2.2
  (the bijection-on-A / no-cycle-on-B reduction), §2.3 (the Key Lemma and
  its induction, including identity `(**)` and its exponential-integral
  proof), and §3 (the Decomposition Theorem's K-free proof).
- `THEOREM.md`'s "Estágio 40" entry (the K=3 target this front generalizes)
  and the K=3 front's own `k3_full_cdf_attempt/ATTEMPT.md` §2 (its full
  statement and proof of Proposição S and the Decomposition Theorem at
  K=3, in prose) — confirmed the target document's restatement of
  Estágio 40's four K=3 formulas is verbatim-accurate (see Finding L1).
- `THEOREM.md`'s "Estágio 38" entry — confirmed its own referee's summary
  states Mechanism 2 (Lemma 4, Cycle-Predecessor Uniqueness) is "PROVADO
  para `K` geral — literalmente a mesma prova de `K=3` com `3` substituído
  por `K`, sem uso do valor específico `3` em nenhum passo lógico," exactly
  matching this document's citation of it in §3.1.
- `general_k_joint_attempt/ATTEMPT.md` §4.1 (the "landing-position-uniform"
  fact) — read directly; its stated claim ("conditional on `dest(t)=s`...
  the landing position within `ARC(s)` is uniform on `{1,...,L_s}` —
  regardless of which source `t` this is, which cycle it belongs to, or how
  many other sources also happen to target `ARC(s)`") matches this
  document's citation exactly, and `THEOREM.md`'s Estágio 38 entry records
  that an earlier independent referee already re-verified this same claim
  at the position level for `K=1,...,4` by direct traversal, zero
  discrepancies.

Both citations (Estágio 38's Lemma 4, and `general_k_joint_attempt` §4.1's
landing-uniform fact) check out exactly as represented. No citation issue
found.

---

## Independent verification performed (all scripts/logs in this directory)

### 1. The crux algebraic identity `(1-P_B)F(B)+G(B)=1` — `adv_01_algebraic_identity.py`/`.log`

Four independent routes, all passing:

- **(A)** Direct subset-sum expansion of `F(B)`, `G(B)` from their raw
  definitions, fully free symbolic weights, `m=1..8` — all exact zero
  residual.
- **(B)** Independent re-derivation of the log-derivative identity
  `sum_c p_c^2/(1+p_c*lambda) = (P_B - L(lambda))/lambda` used in the
  document's proof, `m=1..6` — confirmed both algebraically (clearing
  denominators) and by cross-checking `L(lambda)=g'/g` against the direct
  sum `sum_c p_c/(1+p_c*lambda)`.
- **(C)** Independent verification of the integration-by-parts step
  `int_0^inf e^{-lambda}g'(lambda)dlambda = F(B)-1`, via two separate
  routes: genuine `sp.integrate` term-by-term, and an independent
  combinatorial route through the elementary-symmetric-polynomial
  expansion of `g` — both agree with each other and with `F(B)-1`,
  `m=1..6`.
- **(D)** Exact-rational random-weight numeric spot checks of the full
  identity, `m=1..12`, **including negative and >1 weights** (this is a
  pure polynomial identity, not a probability fact — confirmed it holds
  even outside the probability simplex, exactly as claimed).

**This referee's own hand re-derivation** (done before writing any code,
recorded here for the record): re-derived the reduction from the induction
step to identity `(**)`, and re-derived `(**)`'s proof via the exponential
integral independently line by line — the log-derivative identity, the
`sum_j p_j^2 prod_{c!=j}(1+p_c\lambda) = [P_B g(\lambda)-g'(\lambda)]/\lambda`
step, and the integration-by-parts boundary terms (`e^{-\lambda}g(\lambda)\to0`
as `\lambda\to\infty` since `g` is a fixed-degree polynomial;
`e^0 g(0)=1`) all check out independently. No gap found.

### 2. The induction's base case and logic (walked line by line)

Verified by hand, independently of any script: the base case `|B|=0`
(`R(\emptyset)=1=q_\emptyset` vacuously) is correct; the inductive step's
algebra (isolating the `C=\emptyset` term, substituting the IH
`R(B\setminus C)=1-P_B+P_C` for `C\ne\emptyset` since `|B\setminus
C|<|B|`) reduces exactly to `(**)` as claimed, with no hidden
`K`-dependence anywhere — the argument never references the original
index set `\{0,...,K-1\}`, only that `B` is *some* finite index set,
exactly as the document states. **`adv_07_partition_identity_star.py`/`.log`**
additionally checks the starting identity `(*)` itself — `sum_{C\subseteq
B}|C|!\prod_C p_c\cdot R(B\setminus C)=1` — using a **raw brute-force**
`R` (genuine cycle detection, no closed form assumed anywhere), confirming
both the set-theoretic partition claim and the resulting weighted identity
directly, `|B|=1..4`, all exact. (Two bugs were found and fixed in this
referee's own script during this check — see Self-Caught Bugs below; both
were caught by internal assertions/crashes before any conclusion was drawn.)

### 3. The Key Lemma `R(B)=q_B`, including its strongest (multi-flavor) form — `adv_06_key_lemma_multi_flavor_escape.py`/`.log`

The document's Key Lemma claims `R(B)=q_B` holds **"regardless of how the
escape weight is internally distributed among the individual escape
flavors."** Proposition S's own application (§2.2) only ever exercises a
single bundled escape (`DEAD` and landing-in-`A`, lumped together), so this
stronger multi-flavor claim is not directly stress-tested by the document's
own raw-enumeration checks. This referee built a genuinely different raw
model — `B` with `E\ge2` separately-named, separately-weighted escape
flavors — and checked `R(B)=q_B:=\sum_j e_j` by raw brute-force cycle
detection, for `(m,E)` up to `(4,2)` and `(3,3)`, **with a deliberate
negative control first** (an unnormalized version, correctly found to
FAIL, confirming the check is sensitive) and then correctly normalized
(the last flavor's weight forced dependent so `\sum p+\sum e=1`) —
**all pass exactly**, including a "different flavor made dependent"
re-split confirming `R(B)` truly depends only on the total `q_B`, not the
internal split. This is a genuine extension of the front's own testing
reach, not a re-run of it.

### 4. Proposition S itself — `adv_02`, `adv_02b`, `adv_03`, `adv_05`

- **`adv_02_proposition_s_raw_enum.py`/`.log`**: raw `(K+1)^K`
  destination-table enumeration, fully free symbolic weights, `K=0..5` —
  matches the document's own claimed fully-symbolic reach, one `K` beyond
  the orchestrating session's own pre-dispatch K=4 spot-check. (A K=6
  fully-symbolic attempt was also made; the naive expand-every-term
  approach did not finish in a 580s budget for 117,649 terms of degree-6
  polynomials and was killed rather than left unbounded — disclosed, not
  hidden; K=6/7 were instead confirmed at concrete rational weights.)
- **`adv_02b_proposition_s_k6_concrete.py`/`.log`**: `K=6,7` at concrete
  generic rational weights, exact `Fraction` arithmetic — matches the
  document's own claimed concrete-weight reach for those `K`, all exact.
- **`adv_03_true_bruteforce_def4.py`/`.log`**: a genuinely independent
  **true Definition-4 brute force** — real permutations `\pi`, real target
  tuples `U`, arcs reconstructed directly from `\pi`'s own cycle structure
  (own implementation, not the document's) — run at 11 `(n,K)` cells
  including `(7,3)` (1,728,720 configurations), one cell beyond the
  document's own true-brute-force reach. Confirms, **at the fully
  unconditional level** (i.e. exactly the level the document itself
  disclosed catching a bug at — gap-vector vs. `L`-vector composition
  uniformity): (i) the bookkeeping identity `T=O+\sum_{s\in S}V_s` in
  every single configuration, zero failures; (ii) `P(S=A)` computed two
  fully independent ways (raw enumeration vs. Proposition S averaged over
  the TRUE brute-force arc-length distribution, recomputed from scratch,
  not citing the gap-vector-uniformity fact at all) — exact match on
  every one of the resulting values across all 11 cells.
- **`adv_05_recovers_k3_formulas.py`/`.log`**: confirms Proposition S's
  general-`K` formula, specialized to `K=3`, reproduces Estágio 40's four
  formulas **exactly**, symbolically, for all 8 subsets of `\{0,1,2\}`
  (not just the 4 "shapes"), including an independent re-verification of
  the `p_D+p_s+p_t=1-p_u` normalization step Estágio 40's own proof uses,
  and a global sanity check that all 8 probabilities sum to exactly 1.

### 5. The Full Cycle-Count Decomposition Theorem's K-freeness — `adv_04_decomposition_position_level.py`/`.log`

Built a **fresh position-level reduced model** directly from
`ATTEMPT.md`'s prose description of the arcs (§1.2), with **no reference
anywhere in the construction to "who the cycle predecessor is"** — cyclicity,
`S`, and each `V_s` are read off purely by direct forward simulation of
the resulting functional graph. Ran at `K=4,5,6` (six configurations, up
to `n^K=531{,}441` raw target-configurations per cell), checking, for
**every** raw configuration:

- the bookkeeping identity `T=O+\sum_{s\in S}V_s` — zero failures, and
- the **full joint** empirical distribution of `(V_s)_{s\in S}`, for
  **every** observed value of `S`, against the predicted product of
  independent `Uniform\{1,...,L_s\}` distributions, checked at the level
  of **every cell of the joint product space** (not marginals) — every
  cell hit with exactly equal count, zero discrepancies, at every `K`
  tested including `K=6`.

This directly targets the task's warning that "independence claims are
exactly the kind of thing that looks true marginally but can fail
jointly" — checked at the strongest (full joint) level, and it holds.

---

## Self-caught bugs (in this referee's own scripts — disclosed per lineage convention)

None of these affect the verdict; all were caught by internal consistency
checks (an assertion or a crash) before any conclusion was drawn from the
affected script, and are recorded here in the same spirit the front itself
used for its own disclosed bugs.

1. **`adv_03_true_bruteforce_def4.py` (initial version): arc direction
   reversed.** The first version reconstructed `ARC(s)` by walking
   *forward* via `\pi` from the source (`s,\pi(s),\pi(\pi(s)),...`).
   `ATTEMPT.md` §1.2 states the source occupies the *last* position of its
   arc ("position `L_s` the source itself"), so the arc must be built by
   walking *backward* via `\pi^{-1}`. The forward-direction bug
   misattributed points between arcs and produced 44/384 spurious
   `T\ne O+\sum V_s` "failures" at `(n=4,K=2)` — a bug in this referee's
   script, not evidence against the theorem. Fixed (walk `\pi^{-1}`); all
   384 configurations pass after the fix, and all subsequent cells
   (including the `n^K` up to 1,728,720-configuration cell) pass cleanly.
2. **`adv_04_decomposition_position_level.py` (initial version): duplicate
   `'DEAD'` slots silently collapsed by `itertools.product`/dict keys.**
   Using `O` identical `'DEAD'` entries in the raw target-slot list meant
   distinct raw draws that both happened to land on (possibly different)
   `DEAD` copies were treated as the same dict key, undercounting escape
   probability. Caught by an internal `assert total_configs == n**K`
   firing before any conclusion was drawn. Fixed by tagging each outside
   slot `('DEAD', k)` for distinct `k`, restoring genuine `n^K` raw
   configurations.
3. **`adv_06_key_lemma_multi_flavor_escape.py`: first version omitted
   normalization entirely.** An initial "pure identity, no normalization"
   version of the multi-flavor stress test failed for every `(m,E)`
   tried — this reflects a real mathematical fact (the Key Lemma is a
   statement about a genuine probability distribution, requiring
   `\sum p_b+\sum e_j=1`; without that constraint there is no reason for
   `R(B)` to equal `1-P_B`), not a bug in the theorem — mirroring, and
   independently confirming the necessity of, the front's own disclosed
   normalization caveat for Proposition S/`p_D` (§2.5c), now shown to
   extend correctly to the more general multi-flavor Key Lemma statement.
   The script was corrected to impose true normalization and to include
   the failing unnormalized run as an explicit negative control (see
   check 3 above); no further issue found.
4. **`adv_07_partition_identity_star.py`: two chained bugs in the
   from-scratch `R_raw` helper.** (i) used the outer index set's domain
   instead of the sub-index-set's own domain when recursively computing
   `R(B\setminus C)`, causing a `KeyError` (caught immediately, a crash,
   not a silent wrong answer); (ii) after fixing (i), the bundled `'ESC'`
   outcome for `R(B\setminus C)` initially carried only the *original*
   escape weight `p_D`, omitting the `\sum_{c\in C}p_c` contribution that
   must also count as "escape" from `B\setminus C`'s perspective — fixed
   by passing the correct combined escape weight explicitly. Both fixed
   before drawing any conclusion; the final run (§2 above) passes exactly
   at `|B|=1..4`.

---

## Findings, with severity

**No HIGH-severity findings.** No MODERATE-severity findings against the
document's own mathematical content. Two LOW-severity, purely
informational findings:

**L1 — BAIXA / LOW, informational.** None found in the target document
itself; all citations checked (to Estágio 38's Lemma 4 general-`K` form,
and to `general_k_joint_attempt` §4.1's landing-uniform fact) are
verbatim-accurate against the cited documents' own text, and the
restatement of Estágio 40's four K=3 formulas in §2.4 is exact (confirmed
symbolically, `adv_05`). Recorded here only to note that the citation-checking
pass found nothing to flag — included for completeness of the audit trail,
not as a defect.

**L2 — BAIXA / LOW, scope-labeling only.** The document's own Section 5
already labels the single closed-form-in-`(n,K)` unconditional CDF as
NOT ATTEMPTED (correctly, matching the mandate's own secondary-target
scoping) — this referee did not attempt it either (out of the assigned
adversarial task's scope, which is to break the two headline PROVED
claims, not to close an already-honestly-disclosed open question). No
issue with the document's own honesty here; noted only so the scorecard
below is complete.

No other findings. In particular:

- The crux algebraic identity `(**)` and its exponential-integral proof:
  **no error found**, verified by four independent routes plus an
  independent hand re-derivation.
- The induction's logic (base case, inductive step, the starting partition
  identity `(*)`): **no error found**, including the strongest
  (multi-flavor escape) form of the Key Lemma, which the document's own
  checks do not directly exercise but which this referee's `adv_06` does,
  and which holds.
- Proposition S: **no error found**, confirmed by raw symbolic enumeration
  (`K=0..7`, split fully-symbolic `K\le5` / concrete-rational `K=6,7`) and
  by true, from-scratch Definition-4 brute force at the fully unconditional
  level (11 `(n,K)` cells, up to 1,728,720 exact configurations,
  reaching one cell — `(n=7,K=3)` — beyond the document's own true-brute-force
  reach).
- The Full Cycle-Count Decomposition Theorem's K-freeness, including the
  **joint** (not merely marginal) independence of `(V_s)_{s\in S}` given
  `S`: **no error found**, confirmed by a from-scratch position-level
  model built with no reference to "predecessor" anywhere in its
  construction, at `K=4,5,6`, checked at the level of every cell of the
  joint product space.
- The recovery of Estágio 40's four K=3 formulas as one unified formula:
  **exact match confirmed**, all 8 subsets, symbolically.

---

## Files in this directory

| file | what it checks |
|---|---|
| `adv_01_algebraic_identity.py`/`.log` | crux identity `(1-P_B)F(B)+G(B)=1`, four independent routes, `m=1..12` |
| `adv_02_proposition_s_raw_enum.py`/`.log` | Proposition S vs raw `(K+1)^K` table, fully symbolic, `K=0..5` |
| `adv_02b_proposition_s_k6_concrete.py`/`.log` | Proposition S vs raw `(K+1)^K` table, concrete rational weights, `K=6,7` |
| `adv_03_true_bruteforce_def4.py`/`.log` | true Definition-4 brute force (own arc reconstruction), 11 `(n,K)` cells up to `(7,3)`, unconditional `P(S=A)` two independent ways |
| `adv_04_decomposition_position_level.py`/`.log` | fresh position-level model, no reference to "predecessor," bookkeeping + full joint independence of `(V_s)`, `K=4,5,6` |
| `adv_05_recovers_k3_formulas.py`/`.log` | exact symbolic recovery of Estágio 40's four K=3 formulas from Proposition S (general K) |
| `adv_06_key_lemma_multi_flavor_escape.py`/`.log` | Key Lemma's multi-flavor-escape claim, with a deliberate unnormalized negative control |
| `adv_07_partition_identity_star.py`/`.log` | the induction's starting identity `(*)` itself, via raw brute-force `R`, `\|B\|=1..4` |
| `REFEREE_REPORT.md` | this report |

## Seeds

Reserved sub-range `20260924500`–`20260924799` (confirmed unused by the
grep above); not consumed — every check in this directory is exact
(symbolic/exhaustive/exact-rational), no randomness was needed.
