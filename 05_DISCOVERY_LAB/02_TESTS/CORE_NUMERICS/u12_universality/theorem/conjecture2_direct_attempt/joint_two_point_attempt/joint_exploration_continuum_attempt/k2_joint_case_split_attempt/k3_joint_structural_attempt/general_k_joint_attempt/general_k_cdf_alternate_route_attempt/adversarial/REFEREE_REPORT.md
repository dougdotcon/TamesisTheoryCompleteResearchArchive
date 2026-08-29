# Hostile referee report: GENERAL-K-CDF-ALTERNATE-ROUTE-ATTEMPT

**Target:** `.../general_k_joint_attempt/general_k_cdf_alternate_route_attempt/ATTEMPT.md`
(`DISC-DEC-118`, wave 25 front (b)). Pure combinatorial mathematics about
the u12 permutation-with-reroutes ensemble. Not a Millennium Prize
Problem; no such claim appears anywhere in the target document.

**Method.** Read `THEOREM.md` Estagio 44 (the predecessor result),
Estagio 41 (Proposicao S / Decomposition Theorem, cited machinery),
Estagio 39 (Gosper/EGF methodological template), and the sibling front's
full `general_k_closed_cdf_attempt/ATTEMPT.md` before touching any
target script. Every core mathematical claim below was independently
re-derived and re-verified from the mathematical prose alone, using
fresh, from-scratch scripts (never copied from the target's or any
sibling's `.py` files), before the target's own scripts were opened for
cross-checking. Target scripts were opened only after independent
results were in hand, to resolve a genuine notational subtlety (Claim
2) and to check the specific implementation of the `hypersimp` guard
(Claim 4), per the mandate.

## Verdict

**SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**

Every core new claim of the front (the W-collapse identity, the
hockey-stick collapse, the second Gosper certificate, the self-disclosed
`hypersimp` guard, the OGF diagnostic, the honest `sympy.holonomic`
disclosure) was independently reconstructed from scratch and confirmed
correct. One genuine LOW-severity documentation-clarity finding is
raised (a notational subtlety at `r=0` that the target's own code
handles correctly but its prose does not spell out). No error affects
any reported result, timing, or the certificate itself. Scope, seed, and
git discipline all independently confirmed clean.

## What was independently reconstructed and confirmed

### 1. The W-collapse identity (Section 3) — CONFIRMED

Built `InnerJ(V,O)` from scratch directly from the cited Estagio 44
closed form, substituted `O=W-V`, and confirmed symbolically (both
`InnerJ(V,W-V) - InnerJ_W(W)` simplifies to `0` **and** `d/dV[InnerJ(V,W-V)]`
simplifies to `0`) for both the `r<K` and `r=K` cases. Also confirmed
numerically at 20 random `(n,K,r,W)` configurations, each with up to 5
distinct `(V,O)` splits of the same `W`, all giving identical `InnerJ`
values (`adversarial/adv01_w_collapse_identity.py`, Parts 1–1b). The
identity is in fact elementary once seen: the cited closed form's only
dependence on `(V,O)` is through the two combinations `O+V` and
`N=n-V-O`, both of which collapse to functions of `W=V+O` alone by
inspection — the claim is correct, and not difficult to see once stated,
which is itself a mild point in the front's favor (a real, clean,
previously-unused structural fact, exactly as the mandate hoped a
literal "avenue (a)" attempt might surface).

### 2. The hockey-stick collapse and the overall reorganization (Section 3) — CONFIRMED, with one LOW finding

Verified `sp.summation(binomial(V-1,r-1),(V,r,W)) - binomial(W,r))`
simplifies to `0` for generic symbolic `r`, matching the target's own
symbolic check.

**A genuine subtlety was found and resolved.** At `r=0`, the notation
`C(V-1,r-1) = C(V-1,-1)` is convention-dependent. Under the naive/literal
convention that both `sympy.binomial` and `math.comb` actually implement
(`C(n,k)=0` for `k<0`), the symbolic sum's own closed form
`W*C(W-1,r-1)/r` is `0/0` (indeterminate) exactly at `r=0`, and a direct
term-by-term evaluation gives `0` for every `W`, not `C(W,0)=1`. Rebuilding
the ORIGINAL uncollapsed double sum from scratch with this naive
convention and comparing against the collapsed single sum across 810
`(n,K,r,k)` cells (`n∈{6,8,10,12,15}`, `K=1..6`, every `r=0..K`,
`k∈{0,1,2,⌊n/2⌋,n-1,n}`) produced exactly 145 mismatches — **all of them
at `r=0`**, zero elsewhere (`adversarial/adv01_w_collapse_identity.py`
Part 3a).

This is **not a bug in the target's result**. Inspecting the target's own
`reference_Sr_double_sum.py` (line 64) and `w_collapse_identity.py` shows
both correctly special-case `C(V-1,r-1)` at `r=0` to its actual
combinatorial meaning — "the number of compositions of `V` into 0
positive parts," i.e. the Kronecker delta `[V=0]`, not a literal binomial
value (`math.comb` cannot even accept a negative second argument, so this
special-casing was a forced, deliberate, and correct choice, not an
oversight). Re-running the same 810-cell comparison with this correct
convention gives **0/810 mismatches** (`adv01...` Part 3b), confirming the
target's claimed "768/768 exact matches, every valid `r=0,...,K`" is
genuine.

**LOW severity finding (F1):** the ATTEMPT.md prose (Section 3.2) states
the hockey-stick identity and its "proved symbolically via `sp.summation`"
verification without noting that this generic-`r` symbolic verification
does not, by itself, cover the `r=0` boundary (the sum's own symbolic
closed form is indeterminate there), and that a literal re-implementation
of `C(V-1,r-1)` via a direct binomial-function call would silently give
the wrong answer at `r=0`. The target's own code handles this correctly,
but a future front citing this identity from the prose alone, without
inspecting the code, could reintroduce the r=0 bug. Purely a documentation
gap; no computed result in the document is affected.

### 3. The second Gosper certificate (Section 4, THE MAIN RESULT) — CONFIRMED

Built `term(W) = C(W,r)*InnerJ(W)` from scratch from the cited `InnerJ`
formula. `gosper_term` on the raw, unsimplified term returned a spurious
fast `None` in `0.040s` (reproducing the self-disclosed pitfall, Claim 4
below). After `sp.simplify()`, `hypersimp` genuinely recognized the term
as hypergeometric (`ratio.is_rational_function(W) = True`), with a ratio
expression that is **character-for-character identical** to the one
printed in the target's own `gosper_certification_W.log`. Concrete
positive controls `K=1,...,7` all succeeded (`FOUND`, `0.17s`–`2.0s`,
matching the target's Part B table in magnitude). The symbolic-`K`
certificate: `gosper_term(term, W)` with `K` (and `r,n`) fully symbolic
ran to completion and returned `None` in **11.19s** and, on a second
independent build/run, **12.40s** — closely matching the target's own
three independently-timed runs (`13.19s`/`12.17s`/`11.69s`), and
confirming the claimed ~25x speedup over Estagio 44's `313.1s` certificate
on the un-collapsed object (`adversarial/adv02_gosper_certificate.py`).

### 4. The `hypersimp` self-disclosed pitfall and its guard — CONFIRMED real and correctly placed

Independently reproduced the exact pitfall: calling `gosper_term` on the
raw, unsimplified `term(W)` gives a deceptively fast `None` (`0.04s`) that
is a recognition failure, not a certificate. Read the target's own
`gosper_certification_W.py` (`part_c_symbolic_K_certificate`, lines
124–154): it calls `hypersimp(term, W)` and checks
`ratio.is_rational_function(W)` **before** calling `gosper_term` and
**before** declaring `is_certificate = (res is None) and (ratio is not
None) and is_rational` — the guard is real, in the right place (prior to
trusting `None`), and its trace output is printed in every run, exactly
as the prose in Section 4.4 describes. Not merely claimed in prose.

### 5. The OGF/generating-function diagnostic (Section 6) — CONFIRMED, honestly scoped

Derived the OGF identity `sum_K InnerJ(W;K) x^K = (Wx+r)(1+x)^{n-W+r-1}`
from scratch via two applications of the elementary Binomial Theorem
(trivial algebra, confirmed `=0` exactly) and independently via
coefficient extraction against a from-scratch `InnerJ` at several
`(n,W,r)` triples — all exact. Independently reproduced Diagnostic 1 (the
r-first summation order fails Gosper already at concrete `K=1`, genuinely
— `hypersimp` recognized the term first) and Diagnostic 2 (the GF-marked,
`K`-eliminated `W`-sum is Gosper-summable at concrete `r=0,2` but
genuinely fails, hypersimp-confirmed, once `r` is also left symbolic).
Also independently reproduced Section 5's hyperexpand fallback: a direct
`eval_sum_hyper` call without the target's `W=r+i` reindex returns `None`
in `0.04s` (no closed form reachable that way), but with the reindex —
confirmed to be a legitimate, purely notational index shift, and
reproducing the target's own printed `term(i)` verbatim — `eval_sum_hyper`
produces a genuine `hyper()`-containing closed form in `2.34s` (target:
`2.01s`), and `hyperexpand` fails to reduce it further in `0.35s` (target:
`0.33s`) (`adversarial/adv03_ogf_and_diagnostics.py`,
`adv04_hyperexpand_fallback.py`).

**Honesty of scoping, confirmed.** The document explicitly and
repeatedly disclaims obtaining a broader-than-Gosper certificate anywhere
(Executive Summary, Section 6.3, Section 7.4, Scorecard item 15) — grepped
the full document for "holonomic"/"broader"/"Zeilberger" and found no
instance where these words are used to claim more than was earned.
Independently inspected `sympy.holonomic`'s actual public API
(`HolonomicFunction`, `DifferentialOperator(s)`, `RecurrenceOperator(s)`,
`from_hyper`, `from_meijerg`, `expr_to_holonomic`) and confirmed it does
indeed require an already-given operator or special-function expression —
it is not a decision procedure for an unevaluated sum with two free
symbolic parameters, exactly as Section 6.3 states.

### 6. Scope and seed discipline — CONFIRMED clean

- No `git` command in any of the 7 target `.py` files or in ATTEMPT.md
  prose (the 3 "git" mentions in the prose are all disclosure statements,
  "No `git` command run").
- Sibling directory `general_k_closed_cdf_attempt/` has zero files with an
  mtime at or after the target directory's own earliest file mtime —
  confirms nothing in the sibling was touched during or after this
  front's work.
- `THEOREM.md`, `index.html`, `README.md`, `PROOF_DEPENDENCY_MAP.md`: no
  mention of this front's task ID or directory name (no self-integration).
  `DECISION_LEDGER.yaml` mentions `DISC-DEC-118` only as the pre-existing
  wave-25 dispatch record (predates this front's own work; `DISCOVERY_LAB_STATE.md`
  likewise only carries the dispatch-time listing, not a front-authored edit).
- Seed range `20260930000-20260930999`: exactly one occurrence of this
  range outside the target directory in the whole `05_DISCOVERY_LAB/`
  tree — the `DECISION_LEDGER.yaml` reservation line itself (split across
  two lines by YAML wrapping). The 8 seeds actually used
  (`20260930001`–`20260930008`) are exactly as printed in the ATTEMPT.md
  Monte Carlo table, all within the reserved block, none reused, none
  colliding with the sibling front's own `20260927xxx` block.

(`adversarial/adv05_scope_seed_git_audit.py`)

### General failure modes checked

- **Fabrication:** none found. Every number this referee attempted to
  reproduce independently (Gosper timings, `hypersimp` ratios, OGF
  identity, hyperexpand results, term formulas) matched the target's
  reported values closely, including character-for-character matches on
  two symbolic expressions (the `hypersimp` ratio in Section 4.3, the
  reindexed `term(i)` in Section 5).
- **Executive summary vs. body consistency:** read the full document;
  found no contradiction between the executive summary's claims and the
  detailed derivations.
- **Overclaim of a broader decision-procedure class:** none found (see
  item 5 above).
- **Silent reuse of Estagio 44's own numbers presented as independently
  obtained:** none found. Every citation of Estagio 44's own results
  (the `313.1s` certificate, the `InnerJ` formula, the exchangeability
  reduction) is explicitly and correctly attributed throughout, and the
  front's own new numeric work (`bruteforce_definition4_general_k.py`,
  `reference_Sr_double_sum.py`) is a fresh, independent re-implementation,
  not a copy.

## Findings summary

| # | Finding | Severity | Affects any reported result? |
|---|---|---|---|
| F1 | ATTEMPT.md Section 3.2's hockey-stick "proved symbolically via `sp.summation`" claim does not disclose that this generic-`r` verification leaves an indeterminate `0/0` boundary at `r=0`, requiring the Kronecker-delta convention the target's own code correctly (and necessarily) uses but does not document in prose. | LOW (documentation clarity only) | No — independently confirmed the target's own code and numeric results are correct at `r=0`; only the prose's self-description of "proved symbolically" is incomplete about scope. |

No MODERATE or HIGH severity findings. No claimed result (the W-collapse
identity, the hockey-stick collapse, the second Gosper certificate, the
`hypersimp` guard, the OGF diagnostic, the honest holonomic disclaimer)
was found to be wrong, overstated, or unsupported. The front's honest
non-closure — with genuine new content (a new structural identity, a
second independent and markedly faster certificate, a new hyperexpand
check, and a sharper structural diagnosis of the obstruction) — is
treated, per this archive's standing discipline, as a fully legitimate
outcome, not penalized for failing to find a positive closure.

## Files in this directory

| file | contents |
|---|---|
| `REFEREE_REPORT.md` | this report |
| `adv01_w_collapse_identity.py` / `.log` | independent, from-scratch verification of the W-collapse identity and the hockey-stick collapse, including discovery and resolution of the `r=0` boundary subtlety (Finding F1) |
| `adv02_gosper_certificate.py` / `.log` | independent, from-scratch reproduction of the second Gosper certificate (raw-term pitfall, `hypersimp` guard, concrete K=1-7 positive controls, symbolic-K `None` certificate) |
| `adv03_ogf_and_diagnostics.py` / `.log` | independent verification of the OGF identity, Diagnostic 1 (r-first order), Diagnostic 2 (GF-marked term), and a `sympy.holonomic` API sanity check |
| `adv04_hyperexpand_fallback.py` / `.log` | independent reproduction of the Section 5 hyperexpand fallback, including the negative control (direct call without reindexing) |
| `adv05_scope_seed_git_audit.py` / `.log` | scope, seed, and git-command discipline audit (read-only; no git commands invoked) |

No file outside this `adversarial/` subdirectory was modified by this
referee. No `git` command was run by this referee at any point.
