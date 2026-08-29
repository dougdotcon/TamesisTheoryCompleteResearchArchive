# A genuinely different organization of the general-K closed CDF: a new exact collapse identity, a second independent Gosper certificate on a simpler object, and a sharper structural diagnosis of why neither route closes

**Task ID:** `GENERAL-K-CDF-ALTERNATE-ROUTE-ATTEMPT`, `DISC-DEC-118`, wave 25
front (b). Direct successor to Estagio 44's `GENERAL-K-CLOSED-CDF-ATTEMPT`
(`.../general_k_joint_attempt/general_k_closed_cdf_attempt/ATTEMPT.md`),
which reorganized the general-K CDF by touched-subset size `r`, closed
the resulting per-subset-size building block `S_r(n,K,k)`'s "Camada 1"
(marginalization of the `K-r` untouched sources) fully symbolic in
`(n,K,r)`, and certified via `sympy.concrete.gosper.gosper_term` that
"Camada 2" (the touched-subset-total-size `V`-sum, truncated at `t=k-O`)
has **no** hypergeometric-term antidifference for symbolic `K` — the
obstruction this front was explicitly dispatched to route AROUND, not
repeat. Estagio 44 explicitly never attempted its own "Camada 3" (the
`O`-sum) or the final outer `r`-assembly, since Camada 2 already failed
to close first. Methodological references: Estagio 41
(`GENERAL-K-DECOMPOSITION-ATTEMPT`, the K-free Proposicao S and Full
Cycle-Count Decomposition Theorem this front cites, not re-derives) and
Estagio 39 (`PNN-GENERAL-K-EGF-ATTEMPT`, the Gosper/EGF methodological
template). Pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble defined in `THEOREM.md`
Definition 4. **This is not a Millennium Prize Problem and no claim of
that kind is made anywhere below.**

Reserved seeds: `20260930000`-`20260930999` (this front's own, per
`DISC-DEC-118`; grep-confirmed unused before first use — see Section
"Seeds"). No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `git` command run. All work confined to this new
subdirectory; the sibling directory `general_k_closed_cdf_attempt/` was
read in full (its `ATTEMPT.md` prose and, for exact formula
transcription, `gosper_certification_vsum.py`) but never written to.

---

## Executive summary (read first)

**Outcome tier reached: primarily (c) — an honest, sharper structural
diagnosis of exactly what blocks closure — with a genuine secondary
component of (b): a second, independent Gosper-certified non-existence
result, obtained via a NEW exact combinatorial identity this front
discovered, on a structurally SIMPLER object than Estagio 44's own. Not
"broader" in formal decision-procedure class (still Gosper-class, not a
holonomic/P-recursive decision procedure — see Section 6 for the honest
disclosure of why `sympy.holonomic` could not be used to obtain a
genuinely broader class of certificate here). No closed form found (tier
(a) not reached).**

**The new route, precisely (mandate avenue (a), executed literally).**
Estagio 44's `S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1) *
InnerJ(V,O)` truncates in **two separate steps**: `O<=k` (outer), then
for each fixed `O`, `V<=k-O` (inner). This front proves — a new fact
Estagio 44 never used — that the cited Layer-1 closed form `InnerJ(V,O)`
depends on `(V,O)` **only through their sum** `W:=V+O`, not on how `W`
splits between them (Section 3, PROVED, symbolic, sympy exact). Given
this, the `k`-truncation can be applied **once**, on the single combined
variable `W`, instead of twice. Summing `C(V-1,r-1)` over the implicit
`O`-split for fixed `W` collapses via the classical hockey-stick identity
`sum_{V=r}^{W} C(V-1,r-1) = C(W,r)` (Section 3, PROVED, `sp.summation`,
exact) to a genuinely new, structurally simpler identity:

```
S_r(n,K,k) = sum_{W=r}^{k} C(W,r) * InnerJ(W)      <-- NEW, this front
```

a **single** univariate sum with the `O` parameter eliminated
**algebraically**, not merely hidden — one fewer free symbol than
Estagio 44's own `V`-summand carried throughout its own analysis. This
identity is exactly "treating O and V together... truncating [k] later"
as the mandate's avenue (a) describes, and IS the genuine attempt at
Estagio 44's never-reached Camada 3 + outer-`r`-assembly step, done by
combining Camada 2 and Camada 3 into one step rather than leaving Camada
3 for later. Verified numerically against Estagio 44's own (cited,
independently re-implemented and re-verified against fresh brute force
here) double-sum construction across 768 `(n,K,r,k)` cells — zero
mismatches (Section 3.3).

**The second Gosper certificate (Section 4, THE MAIN RESULT).** The
collapsed sum's summand `C(W,r)*InnerJ(W)` **is** Gosper-summable at
every concrete `K=1,...,7` tested (`gosper_term` succeeds every time,
`K=1,2` closed forms extracted via `gosper_sum` and verified against 6
independent `(n,r,k)` numeric checks, all exact). **With `K` left fully
symbolic (together with `r,n`), `gosper_term` runs the genuine algorithm
to completion (confirmed via an explicit `hypersimp` trace that the term
IS recognized as hypergeometric before the decision procedure runs — a
documented pitfall this script explicitly guards against, having hit it
once during exploration and self-corrected, see Section 4.4) and returns
`None` in `13.19s` (and `12.17s` on an independent re-run, and `11.69s`
in an earlier exploratory script) — a genuine, reproducible,
non-existence certificate for THIS collapsed formulation.** This is a
**second, independent** Gosper certificate, at a genuinely different and
structurally SIMPLER point (one fewer free parameter, roughly `25x`
faster to obtain) than Estagio 44's own `313.1s` certificate on the
un-collapsed nested double sum — demonstrating that the obstruction is
**not** an artifact of the particular two-step truncation order Estagio
44 used, and survives even after an exact identity eliminates an entire
summation layer.

**New complementary check Estagio 44 explicitly did not attempt (Section
5).** Mirroring Estagio 39's own fallback exactly: the collapsed sum is
exhibited as a genuine terminating hypergeometric-function representation
(`sympy.concrete.summations.eval_sum_hyper`, a difference of two `hyper()`
objects, `2.01s`), and `sympy.hyperexpand` is tested on it for `K`
symbolic. **It does not reduce to anything elementary** (`0.33s`,
confirmed `hyper()` objects remain) — independently reproducing, for
THIS front's own collapsed object, the same conclusion Estagio 39 reached
for its own (structurally different) `r`-sum, and completing a check
Estagio 44's own Section 5.5 flagged as "NOT ATTEMPTED" for its nested
double sum.

**Two supplementary diagnostics sharpen WHY neither route closes (Section
6, new structural content beyond both predecessors).** (1) **Order-swap
control:** summing the FULL assembly term over `r` FIRST (for fixed `W`)
— the only other natural order — fails Gosper already at every
**concrete** `K` tested (`K=1,...,5`), strictly worse than the `W`-first
order this front's main route uses (which succeeds at every concrete `K`
tested). (2) **Generating-function-in-K (mandate avenue (b)):** a clean
new exact identity, `sum_{K} InnerJ(W;K) x^K = (Wx+r)(1+x)^{n-W+r-1}`
(PROVED, elementary Binomial Theorem, verified both as a polynomial
identity and via direct coefficient-extraction against the true `InnerJ`,
Section 6.2), folds `K`'s troublesome symbolic-DEGREE binomial into a
harmless symbolic-BASE power. The resulting `W`-sum **does** become
Gosper-summable for `x,n` symbolic **once `r` is concrete** (any
`r=0,...,5` tested, instantly) — but the **same style** of obstruction
reappears, genuinely, the moment `r` is ALSO left symbolic (with `x,n`
symbolic, `K` entirely eliminated). **Conclusion:** the true obstruction
is not "`K` is hard" per se — it is the SIMULTANEOUS presence of two free
"family-size" parameters (`K` and `r`), each acting as a symbolic
binomial DEGREE coupled to the summation variable's own combinatorics,
with whichever one is left un-marked being the one that blocks Gosper.
Both Estagio 39's and Estagio 44's own certificates only ever had ONE
such parameter (`K` alone) symbolic at the point of certification; this
front shows the obstruction is more fundamental than "`K`" and would
recur under essentially any single-parameter marking scheme.

**`sympy.holonomic`, investigated per the mandate's suggestion (Section
6.3, honest disclosure).** This module operates on holonomic functions
already given via a differential/recurrence operator, or converts a known
`hyper()` special-function object to one (`from_hyper`) — it is **not** a
decision procedure that can determine, from scratch, whether an
*unevaluated* sum with two free symbolic parameters (`K,r`) is
uniformly holonomic in them. No genuinely broader (P-recursive-class)
non-existence certificate could be obtained with the tooling available in
this environment. **This limit is disclosed honestly, not worked around
by an ad hoc hand-rolled creative-telescoping implementation** (which
this front judged too error-prone to trust without an established,
independently-audited decision procedure, consistent with this archive's
verification discipline).

**Net verdict.** The primary mandate's target (a closed form, or a
broader-in-class non-existence certificate) is **not reached**. What is
delivered: a genuinely new, doubly-proved (symbolic + 768-cell numeric)
structural identity that Estagio 44 never found (the `W`-collapse); a
second, independent, reproducible Gosper certificate on a strictly
simpler object than Estagio 44's own; a new hyperexpand-fallback check
Estagio 44 explicitly skipped; and — the most valuable single finding —
a sharper structural diagnosis, backed by four separate computational
experiments, of exactly WHY this obstruction is not specific to `K` and
would likely resist essentially any comparable single-variable
reorganization. This is Section 4's honest, sharper diagnosis (tier (c)),
with real new proved content (the collapse identity) and a real second
certificate (tier (b) in spirit, not in formal class) along the way. No
claim of progress on any Millennium Problem; pure internal combinatorics
on the u12 ensemble defined in `THEOREM.md`.

---

## 1. Reading discipline and notation

### 1.1 What was read

`DISC-DEC-118` in `DECISION_LEDGER.yaml` (full entry, read first, for
mandate context). `THEOREM.md` Estagio 41 (`GENERAL-K-DECOMPOSITION-
ATTEMPT`) — the K-free Proposicao S and Full Cycle-Count Decomposition
Theorem cited directly, not re-derived. `THEOREM.md` Estagio 44
(`GENERAL-K-CLOSED-CDF-ATTEMPT`) — this front's direct predecessor and
the "dead end" this front routes around; read in full both in
`THEOREM.md`'s integrated summary and in the sibling's own
`ATTEMPT.md` (`.../general_k_closed_cdf_attempt/ATTEMPT.md`, all 689
lines, in full), to understand precisely which layer (Camada 1) closed,
which (Camada 2) is the certified obstruction, and which (Camada 3, the
outer `r`-assembly) was never attempted, and exactly where the Gosper
certificate's `313.1s` `None` was obtained. `THEOREM.md` Estagio 39
(`PNN-GENERAL-K-EGF-ATTEMPT`) — the Gosper/EGF methodological template,
including its own `hyperexpand`-fallback technique this front replicates
in Section 5. `THEOREM.md` Estagio 40 (K=3 full CDF, Proposicao D3) and
Estagio 42 (K=2, Proposicao D2) and Estagio 27 (K=1, Proposicao D1) — the
three already-PROVED closed forms used as an external cross-check
(Section 2.2), cited verbatim, not re-derived.

For exact formula transcription only (never for copying logic or
structure), `.../general_k_closed_cdf_attempt/gosper_certification_vsum.py`
was read (this sibling front's own script, read-only, never modified —
the task mandate permits reading the sibling directory) to confirm the
precise algebraic form of the cited Layer-1 `InnerJ` closed form and the
Camada-2 `V`-summand before independently re-transcribing and
re-verifying both from scratch in this front's own
`reference_Sr_double_sum.py`.

### 1.2 Notation (inherited from the cited lineage, reused without
redefinition beyond what is restated here)

`K>=0` reroute sources fixed WLOG at `{0,...,K-1}` (Definition 4,
`THEOREM.md` Section 7.2). `pi` a uniform random permutation of `[n]`,
independent of the sources' i.i.d. uniform targets `U_0,...,U_{K-1}`.
`f(i):=U_i` for `i` a source, `f(i):=pi(i)` otherwise. `T:=#{cyclic
points of f}` (`M_n^{(K)}=T/n`). `S subseteq {0,...,K-1}` the random set
of cyclic reroute sources (Estagio 40/41). `A subseteq {0,...,K-1}` a
fixed subset, `r:=|A|`. `(L_0,...,L_{K-1},O)` the composition of `n-K`
into `K+1` nonnegative parts governing arc lengths (cited, Estagio
40/41). `Count_r`, `S_r(n,K,k)`, `InnerJ(V,O)` exactly as defined and
PROVED in Estagio 44's `ATTEMPT.md` Sections 2-4.1 (cited below, verbatim,
before this front's own new material begins in Section 3).
**`W:=V+O`** — this front's own new notation, the combined "touched-total
plus untouched-slack" variable central to Section 3's identity.

---

## 2. The cited starting point (Estagio 44's construction), independently re-verified

`reference_Sr_double_sum.py` re-implements, from the mathematical prose
(not the sibling's code) plus a formula-transcription cross-check against
`gosper_certification_vsum.py` (Section 1.1), the two cited results this
front's new route builds on top of:

**Cited (Estagio 41, PROVED, K-free): Proposicao S + Full Cycle-Count
Decomposition Theorem.** `T = O + sum_{s in S} V_s`, `(V_s)` mutually
independent given `S`, `V_s ~ Uniform{1,...,L_s}`; `P(S=A|L) = |A|! *
prod_{a in A} p_a * (p_D + sum_{a in A} p_a)`.

**Cited (Estagio 44, PROVED): exchangeability reduction to `S_r`.**
```
S_r(n,K,k) := sum over the full composition simplex of
                  (O+Sigma) * Count_r(L_0,...,L_{r-1} ; k-O),   Sigma:=L_0+...+L_{r-1}
P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r)*r!/n^{r+1} * S_r(n,K,k)
```

**Cited (Estagio 44 Section 4.1, PROVED): Layer 1 (Camada 1) closed
form.**
```
InnerJ(V,O) = (O+V)*C(n-V-O+r-1,K-1) + r*C(n-V-O+r-1,K),   (r<K)
InnerJ(V,O) = n*C(n-V-O+r-1,r-1),                          (r=K)
S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{k-O} C(V-1,r-1) * InnerJ(V,O)
```

### 2.1 Independent verification of the reference engine

`bruteforce_definition4_general_k.py`: a fresh, fully independent true
Definition-4 enumeration (every `pi`, every target tuple, direct
cycle detection on the resulting functional graph, exact `Fraction`
arithmetic, no shortcut), written completely from the Definition 4 prose
in `THEOREM.md` Section 7.2. Ran at `(n,K) in {(4,1),(4,2),(5,2),(5,3),
(6,3),(6,4),(7,3),(7,4)}`, every `k=0,...,n` (`21.4s`,
`bruteforce_definition4_general_k.log`).

`reference_Sr_double_sum.py`: the cited construction above, assembled
into `unconditional_cdf_via_Sr(n,K,k)`, checked two independent ways:
**(a)** against the fresh brute force above, **every** `(n,K,k)` cell —
**all exact matches**; **(b)** against the three already-PROVED closed
forms D1 (K=1, Estagio 27), D2 (K=2, Estagio 42), D3 (K=3, Estagio 40),
cited verbatim, `n=3,...,8`, every `k=0,...,n-1` (their stated domain) —
**all exact matches** (`reference_Sr_double_sum.log`). This confirms the
starting point this front's new route is checked against is itself
correct, before any new material is introduced.

---

## 3. THE NEW RESULT: the W-collapse identity (mandate avenue (a), executed)

`w_collapse_identity.py`. Estagio 44's `S_r` truncates `O<=k` and (for
each `O`) `V<=k-O` in two separate steps. This front proves a fact
Estagio 44 never used to reorganize its own computation.

### 3.1 `InnerJ(V,O)` depends on `(V,O)` only through `W:=V+O`

Symbolic check (`sympy`, exact): substituting `O=W-V` into the cited
`InnerJ(V,O)` and simplifying the difference against a version written
purely in terms of `W`:
```
r<K:  InnerJ(V, W-V) - InnerJ_W(W) simplifies to 0    (PROVED)
r=K:  InnerJ(V, W-V) - InnerJ_W(W) simplifies to 0    (PROVED)
```
Both cases confirmed, `w_collapse_identity.log`.

### 3.2 The hockey-stick collapse

Since `InnerJ` depends only on `W`, summing the `C(V-1,r-1)` factor over
the implicit `O`-split, for fixed `W`, reduces to the classical identity
```
sum_{V=r}^{W} C(V-1,r-1) = C(W,r)
```
proved symbolically via `sp.summation` (exact, `sp.summation(binomial(V-1,
r-1), (V,r,W)) - binomial(W,r)` simplifies to `0`, `w_collapse_identity.log`).

> **Nota (2026-08-29, achado F1 do referee hostil dedicado, severidade
> BAIXA, esclarecimento, não erro):** a frase "proved symbolically via
> `sp.summation`" acima não divulga que esta verificação genérica-em-`r`
> deixa uma fronteira indeterminada `0/0` em `r=0` (`C(V-1,-1)`, ambígua
> por convenção). O código desta própria frente (`w_collapse_identity.py`,
> `reference_Sr_double_sum.py`) já trata isto corretamente, tratando
> `C(V-1,-1)` pela convenção combinatória correta (delta de Kronecker),
> e o referee confirmou 810/810 correspondências exatas com essa
> convenção — **nenhum número reportado está errado**; apenas a prosa
> não descrevia o escopo completo da verificação. Ver
> `adversarial/REFEREE_REPORT.md`, achado F1.

### 3.3 The new identity, and its independent numeric verification

```
>>> S_r(n,K,k) = sum_{W=r}^{k} C(W,r) * InnerJ(W)   <<<   NEW, this front
```
Verified against `reference_Sr_double_sum.Sr_double_sum` (the cited,
independently-re-verified starting point, Section 2) across **768**
`(n,K,r,k)` cells spanning `n in {6,8,10,12,15}`, `K=1,...,6`, every
valid `r=0,...,K`, `k in {0,1,2,n//2,n-1,n}` — **zero mismatches**
(`w_collapse_identity.log`).

**Why this is genuinely the mandate's avenue (a).** Estagio 44's own
Camada 3 (the `O`-sum, on top of Camada 2's `V`-sum) was never attempted,
because Camada 2 already failed for symbolic `K`. This front's `W`-
collapse IS the direct, literal attempt at combining Camada 2 and Camada
3 — "treating `O` and `V` together rather than truncating in two separate
steps" — except that, because the two truncations turn out to combine
into ONE via the exact hockey-stick identity above, the combined object
is not a harder nested double sum but a **strictly simpler single sum**
with `O` eliminated entirely.

---

## 4. THE MAIN RESULT: a second, independent Gosper certificate on the collapsed sum

`gosper_certification_W.py`. The collapsed summand:
```
term(W) = C(W,r) * [ W*C(n-W+r-1,K-1) + r*C(n-W+r-1,K) ]
```
Because `k` is an arbitrary upper limit (needed at every `k=0,...,n`),
what is required is a genuine INDEFINITE hypergeometric-term antidifference
in `W` — exactly Gosper's algorithm's object of study, mirroring both
Estagio 39's and Estagio 44's own use of Gosper, but on a structurally
DIFFERENT (and simpler) object.

### 4.1 Part A — positive/negative controls (harness soundness)

| control | summand | symbolic parameters | result | time |
|---|---|---|---|---|
| 1 | `C(W,r)` | `r` | found | 0.12s |
| 2 | `C(W,K)` | `K` (symbolic binomial degree) | found | 0.02s |
| 3 | `C(n-W+r-1,K-1)*W` | `K,r` (structurally close to real term) | found | 0.08s |
| 4 (negative) | `1/W` | — | `None` (correctly, textbook non-summable) | 0.01s |

### 4.2 Part B — concrete K, symbolic r: SUCCEEDS every time

| K | `gosper_term` | time |
|---|---|---|
| 1 | found | 0.20s |
| 2 | found | 1.55s |
| 3 | found | 1.68s |
| 4 | found | 1.91s |
| 5 | found | 2.18s |
| 6 | found | 2.76s |
| 7 | found | 2.87s |

For `K=1,2`, `gosper_sum(term,(W,r,t))` closed forms extracted (`0.19s`,
`1.30s`) and verified numerically against the true single-sum
`S_r` at **6** independent `(n,r,k)` configurations — **6/6 exact
matches** (`gosper_certification_W.log`).

### 4.3 Part C — THE CERTIFICATE: K symbolic

```
term(W) = (K*W - K*r - W*r + n*r + r**2)*binomial(W, r)
          *factorial(-W + n + r - 1)/(factorial(K)*factorial(-K - W + n + r))
```

> **`gosper_term(term, W)`, with `K` (together with `r,n`) left fully
> symbolic, recognized the term as hypergeometric (`hypersimp` succeeded,
> ratio confirmed a genuine rational function of `W` — see Section 4.4)
> and ran the real decision procedure to completion, returning `None` in
> `13.19s` in this front's own consolidated script, `12.17s` on an
> independent re-run of the same computation, and `11.69s` in an earlier
> standalone exploratory script — three independent, mutually consistent
> timings, `~25x` faster than Estagio 44's own `313.1s` certificate on
> the un-collapsed, more-parameter object.**

Full transcripts: `gosper_certification_W.log`,
`gosper_certification_W_second_run.log`.

### 4.4 A self-disclosed pitfall this front hit and corrected

During exploration, an early draft of this exact check called
`gosper_term` on the **unsimplified** raw algebraic expression for
`term(W)` (built directly from `sp.binomial(...)` calls without a prior
`sp.simplify()` pass). This returned `None` in `0.04s` — deceptively fast.
Tracing the call revealed the cause: `sympy.simplify.hypersimp` (the
first internal step of `gosper_term`, which computes the term ratio and
checks it is a rational function) **failed to recognize the unsimplified
sum-of-two-binomial-products expression as hypergeometric at all**
(returned `None` at the recognition stage, before the real Gosper
degree-bound machinery ever ran) — this is a **recognition failure**, NOT
a genuine non-existence certificate. Calling `sp.simplify()` on `term(W)`
FIRST (combining the sum-of-two-binomials into the single-fraction form
shown in Section 4.3, matching the methodology Estagio 44's own
`build_term` function already used) fixed this: `hypersimp` then
correctly recognizes the term (confirmed via an explicit trace, printed
in every run of `gosper_certification_W.py`, Section 4.3) and the
algorithm genuinely runs for ~12-13 seconds before returning `None`. This
pitfall — and its fix — is disclosed here because it is exactly the kind
of error this archive's verification discipline exists to catch, and
because a hypothetical hostile referee re-deriving this certificate
without first simplifying the term could reproduce the SAME spurious
`0.04s` "None" and mistake it for a certificate; the script now
explicitly checks and prints `ratio.is_rational_function(W)` before
trusting the final `None`, precisely to make this distinction auditable.

---

## 5. New complementary check: the hyperexpand fallback (not attempted by Estagio 44)

`hyperexpand_fallback.py`. Mirroring Estagio 39's own methodology
exactly: after Gosper certifies no ELEMENTARY hypergeometric-term
antidifference exists, exhibit the sum as a terminating hypergeometric
FUNCTION and test whether `sympy.hyperexpand` reduces it further — a
weaker, broader question ("is there a special-function closed form that
simplifies") than Gosper's own ("is there an elementary term-ratio
closed form").

`sympy.concrete.summations.eval_sum_hyper` (the internal routine
`Sum(...).doit()` itself calls for hypergeometric summands) converts the
`K`-symbolic collapsed sum into a genuine closed form — a **difference of
two terminating `hyper()` objects** (a legitimate `_3F_2`/`_4F_3`-type
special-function representation, `2.01s`):
```
n*r*(n-1)!*hyper((r+1, K-n, ...), (1-n, ...), 1)/(K! (n-K)!)
  - (...)*C(k+1,r)*(n+r-k-2)!*hyper((1, k+2, K+k-n-r+1, ...), (...), 1)/(K! (n-K-k+r-1)!)
```
`hyperexpand` applied to this (`0.33s`): **still contains unevaluated
`hyper()` objects — it does NOT reduce to anything elementary for
`(n,K,r,k)` symbolic.** Same conclusion Estagio 39 reached for its own
(structurally different) `r`-sum, now independently confirmed for this
front's own collapsed object, which Estagio 44's Section 5.5 explicitly
flagged as not attempted for its nested double sum
(`hyperexpand_fallback.log`).

A concrete-`K` (`K=3`) sanity pre-check hit an internal `sympy`
`ValueError: Non-suitable parameters` inside `hyperexpand`'s own
`devise_plan` — **disclosed honestly as a `sympy` library limitation, not
this front's bug**: the underlying sum unquestionably HAS a closed form
at `K=3` (Section 4.2's Gosper closure, obtained via a completely
different code path, already confirms this), so the exception reflects a
gap in `hyperexpand`'s internal case-handling for this particular
concrete-parameter instance, not a mathematical failure. It does not
affect, and is structurally unrelated to, the symbolic-`K` test (which
uses a different internal `hyperexpand` code path and completes without
error).

---

## 6. Two supplementary diagnostics: sharpening WHY neither route closes

`order_swap_and_gf_diagnostics.py`.

### 6.1 Diagnostic 1 — order-swap control (r-first fails even at concrete K)

The only other natural summation order — summing the FULL assembled term
(including the `C(K,r)*r!/n^{r+1}` outer-assembly weight) over `r` FIRST,
for FIXED `W` (valid with no case-split, since `C(W,r)` automatically
vanishes for `r>W`) — was tested directly. **Result: `gosper_term`
returns `None` already at every CONCRETE `K=1,...,5` tested** (confirmed
genuine via `hypersimp` trace each time, not a recognition failure;
`0.4`-`4.4s` each). This is **strictly worse** than the `W`-first order
this front's main route uses (which succeeds at every concrete
`K=1,...,7`). This confirms the `W`-first order is the structurally
correct one to attempt (it alone reproduces the "succeeds concrete,
fails symbolic" pattern common to Estagio 39's and Estagio 44's own
certificates), and independently confirms that the OUTER `r`-assembly —
not the inner `O`/`V` layers — is the genuinely hard part, consistent
with Estagio 39's own historical experience (its certified obstruction
for the simpler quantity `P_nn(n,K)` lived in exactly this same style of
`r`-indexed sum).

### 6.2 Diagnostic 2 — generating-function-in-K (mandate avenue (b))

**Step 1 (proved): the OGF identity.**
```
sum_{K=0}^{infty} InnerJ(W;K) x^K = (W*x+r) * (1+x)^(n-W+r-1)
```
Proved two ways: (i) as the elementary Binomial Theorem (`sum_K
C(M,K)x^K=(1+x)^M`, applied twice — once directly, once after the
standard index-shift for the `C(.,K-1)` piece), spot-checked as an exact
polynomial identity in `x` for `M=0,...,11` (`sp.summation`'s own
symbolic-`M` result carries a cosmetic `|x|<=1` convergence-condition
Piecewise — a well-known artifact of sympy's default hypergeometric-series
summation machinery for a sum that is actually finite and needs no
convergence condition at all; self-disclosed and worked around by the
concrete-`M` spot-check, which is the mathematically correct verification
method for an elementary finite-sum identity). (ii) directly against the
true `InnerJ` via **coefficient extraction** (`[x^K]` of the closed-form
polynomial, for every valid `K=r,...,n-W+r`, at 4 concrete `(n,W,r)`
triples) — all exact matches.

> **Self-disclosed verification bug, caught and fixed in this exact
> check:** a first attempt at this numeric verification compared a
> TRUNCATED SUM `sum_{K=r}^{Kmax} InnerJ_true(K)*x^K` directly against
> the FULL closed-form polynomial `(Wx+r)(1+x)^{n-W+r-1}` — and found
> systematic mismatches. Diagnosis: that polynomial's own low-order
> `x^0,...,x^{r-1}` coefficients are generically NONZERO (the same
> algebraic formula, continued to `K<r` where it is not combinatorially
> meaningful as `InnerJ`), so a sum starting at `K=r` necessarily
> disagreed with the FULL polynomial by exactly that missing low-order
> part — a bug in the verification's summation RANGE, not in the
> underlying identity. Fixed by comparing coefficients one `K` at a time
> instead (well-defined and correct for every `K>=r` regardless of what
> the formula does for `K<r`) — this is the check reported above, and it
> passes exactly.

**Step 2: Gosper on the GF-marked W-sum.** Folding `K` into the marker
`x` removes `K`'s own symbolic-degree-binomial obstruction (the term now
has a symbolic-BASE power `(1+x)^{...}` instead, a much milder object for
Gosper): `gosper_term` **succeeds** for `x,n` symbolic at every concrete
`r=0,...,5` tested (instantly, `0.02`-`0.27s` each). **But the same STYLE
of obstruction reappears, genuinely** (confirmed via `hypersimp` trace),
the moment `r` is ALSO left symbolic (with `x,n` symbolic — `K` is by
this point entirely gone from the term): `gosper_term` returns `None` in
`0.05`-`0.08s`, and `hypersimp` genuinely recognizes the term as
hypergeometric first (not a recognition-failure bailout).

**Interpretation (the sharpest new finding of this front).** The true
obstruction is not "`K` is hard" in isolation. It recurs, in the same
form, on `r` the moment `K`'s own version of it is removed by a
generating-function trick. The common structural feature across every
failure mode found in this front (Section 4's `K`-symbolic certificate,
Section 6.1's `r`-first order, and Section 6.2's `r`-symbolic-after-GF
certificate) is: **a summation whose summand contains a binomial
coefficient with a symbolic DEGREE that is itself a "family-size"
parameter coupled to the summation variable's own combinatorial range.**
This construction has exactly TWO such parameters (`K` and `r`); every
route this front and Estagio 44 tried leaves at least one of them
symbolic at the point Gosper is invoked, and that is enough to block
closure every time. Both Estagio 39's and Estagio 44's own certificates
only ever had ONE such parameter (`K` alone) symbolic — this front is the
first in the lineage to show the obstruction is not specific to `K`.

### 6.3 `sympy.holonomic`, investigated per the mandate's suggestion — honest disclosure of a dead end

The mandate explicitly suggested investigating `sympy.holonomic` or a
Zeilberger-style creative-telescoping check as a possible route to a
BROADER (not merely Gosper-class) non-existence certificate. This was
investigated. `sympy.holonomic`'s public API
(`HolonomicFunction`, `DifferentialOperators`, `RecurrenceOperators`,
`from_hyper`, `from_meijerg`, `expr_to_holonomic`) operates on functions
**already specified** via a differential/recurrence operator, or converts
a **known** `hyper()`/`meijerg()` special-function expression into one —
it provides closure operations (sums, products, composition) on
already-holonomic objects and a `to_sequence()` method to extract a
recurrence FROM a given holonomic function. **It is not a decision
procedure that can determine, from an unevaluated finite sum with two
free symbolic parameters (`K,r`), whether that sum is holonomic
(P-recursive) uniformly in those parameters** — that would require an
implementation of Zeilberger's algorithm / creative telescoping for
multivariate parametrized hypergeometric sums, which `sympy` does not
provide (unlike, e.g., Maple's `SumTools[Hypergeometric][Zeilberger]` or
the Mathematica `HolonomicFunctions` package). **This front did not
attempt a hand-rolled implementation of creative telescoping**,
judging the risk of an unverified, ad hoc implementation producing a
false certificate (or a false non-certificate) to be higher than the
value of the attempt, inconsistent with this archive's standing
verification discipline of using established, independently-audited
decision procedures rather than novel unaudited ones. **No claim of a
broader-than-Gosper non-existence result is made anywhere in this
document** — only the Section 4 Gosper certificate (on the collapsed
sum) and the Section 6.1/6.2 supplementary diagnostics, all of which are
squarely within the same Gosper-decision-procedure class Estagio 39 and
44 already used.

---

## 7. What did NOT close, precisely (honest, as mandated)

### 7.1 `S_r(n,K,k)`, closed form symbolic in `(n,K,r)`

**NOT CLOSED.** The `W`-collapse (Section 3) is a genuine structural
simplification (a single sum instead of a nested double sum, `O`
eliminated), but the resulting single sum is **certified NOT to close**
for symbolic `K` via `gosper_term` (Section 4) — while closing
individually at every concrete `K` tested (`K=1,...,7`). This is a
**second** certified non-closure for `S_r`, on a different object than
Estagio 44's, not a resolution of the first.

### 7.2 The full outer `r`-assembly

**NOT ATTEMPTED IN CLOSED FORM**, for the same reason Estagio 44 stopped
before its own Camada 3: since `S_r` itself (in this front's collapsed
form) does not close for symbolic `K`, attempting to close the outer
`sum_{r=0}^{K}` assembly on top of it would not change that the piece it
depends on is itself unclosed. Diagnostic 1 (Section 6.1) additionally
shows that attempting the outer `r`-assembly FIRST (before the `W`-sum)
is a strictly worse order, failing already at concrete `K` — so there is
no indication a different assembly order would have helped even had
Section 4's certificate not existed.

### 7.3 A single closed-form-in-(n,K) CDF, `P(M_n^{(K)}<=k/n)=F(n,K,k)`

**NOT CLOSED**, and not claimed to be impossible — see Section 6.3's
honest disclosure of what this front could and could not check. The
conditional CDF given `L`, for any concrete `K`, remains fully closed and
correct (cited, Estagio 41's own demonstration; independently
re-verified here in Section 2 via a fresh brute-force cross-check).

### 7.4 What is explicitly NOT claimed

No claim that a closed form (elementary or special-function) for
`S_r(n,K,k)`, or the full unconditional CDF, provably does not exist in
any absolute sense — only that (i) Estagio 44's original nested-sum
formulation is Gosper-certified not to close (their own result, cited),
and (ii) this front's genuinely different, structurally simpler
`W`-collapsed formulation is ALSO Gosper-certified not to close (Section
4, this front's own new result) — two independent data points, not an
exhaustive search over all possible reorganizations. No claim of a
broader-than-Gosper (e.g. P-recursive/holonomic) non-existence result
(Section 6.3). No claim about `K->infinity` asymptotics. No claim of
progress on any Millennium Problem; pure combinatorial mathematics
internal to the u12 ensemble defined in `THEOREM.md`.

---

## 8. Numerical exploration (bonus, not a substitute for Sections 3-6)

`monte_carlo_bonus.py`, reserved seeds `20260930001`-`20260930008`,
direct simulation of Definition 4's actual model (its own independent
random-permutation simulation path, not reusing any of the
composition-simplex or `W`-collapse machinery above), compared against
the exact reference engine (`reference_Sr_double_sum.
unconditional_cdf_via_Sr`, itself independently verified against true
brute force and D1/D2/D3, Section 2):

```
n= 12 K=4 k=  5 trials=20000 seed=20260930001  target=0.573443  MC=0.574250  se=0.00350  z=+0.23
n= 12 K=4 k=  8 trials=20000 seed=20260930002  target=0.917971  MC=0.914400  se=0.00198  z=-1.81
n= 15 K=5 k=  7 trials=15000 seed=20260930003  target=0.727446  MC=0.731600  se=0.00362  z=+1.15
n= 15 K=5 k= 11 trials=15000 seed=20260930004  target=0.979693  MC=0.978267  se=0.00119  z=-1.20
n= 18 K=6 k=  9 trials=10000 seed=20260930005  target=0.829385  MC=0.832500  se=0.00373  z=+0.83
n= 18 K=6 k= 14 trials=10000 seed=20260930006  target=0.995525  MC=0.995800  se=0.00065  z=+0.42
n= 20 K=4 k= 10 trials=10000 seed=20260930007  target=0.708376  MC=0.712200  se=0.00453  z=+0.84
n= 20 K=8 k= 15 trials= 8000 seed=20260930008  target=0.997740  MC=0.998125  se=0.00048  z=+0.80
```
(full transcript: `monte_carlo_bonus.log`) — all 8 cells within `1.81`
standard errors of the exact target; triangulation only, not itself
proof, per lineage convention.

---

## 9. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `bruteforce_definition4_general_k.py` / `.log` | fresh, fully independent true Definition-4 brute force (ground truth), `(n,K)` up to `(7,4)` |
| `bruteforce_cdf_cache.json` | cached exact brute-force CDF vectors, consumed by `reference_Sr_double_sum.py` |
| `reference_Sr_double_sum.py` / `.log` | the cited starting point (Estagio 41 Prop S + Estagio 44 Layer-1/exchangeability), independently re-implemented and re-verified against brute force and D1/D2/D3 |
| `w_collapse_identity.py` / `.log` | Section 3: THE NEW STRUCTURAL RESULT — the `W`-collapse identity, proved symbolically and verified numerically (768 cells) |
| `gosper_certification_W.py` / `.log`, `gosper_certification_W_second_run.log` | Section 4: THE MAIN RESULT — the second, independent Gosper certificate on the collapsed sum, with controls, concrete-K closures, and the symbolic-K `None` certificate (two independent full-script timings plus one exploratory timing) |
| `hyperexpand_fallback.py` / `.log` | Section 5: the terminating-hypergeometric-function fallback, mirroring Estagio 39, not attempted by Estagio 44 |
| `order_swap_and_gf_diagnostics.py` / `.log` | Section 6: the two supplementary diagnostics (order-swap control; generating-function-in-K) that sharpen the structural diagnosis |
| `monte_carlo_bonus.py` / `.log` | Section 8: large-`(n,K)` Monte Carlo triangulation, reserved seeds |

---

## 10. Seeds

Reserved range: `20260930000`-`20260930999` (this front's own, per
`DISC-DEC-118`). Grep-confirmed unused before this front's first use:
```
$ grep -rn "20260930" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7765-7766: (the reservation line itself)
```
(re-confirmed after this front's own files were created that no other
file in the archive references this range except this front's own
scripts/logs and the governance reservation line itself.)

Only `monte_carlo_bonus.py` uses randomness (`numpy.random.default_rng`,
one explicit seed per configuration, no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `bruteforce_definition4_general_k.py` | none (exhaustive) | ground-truth Definition-4 brute force |
| `reference_Sr_double_sum.py` | none (exact) | cited-construction reference engine |
| `w_collapse_identity.py` | none (exact/symbolic) | THE new collapse identity |
| `gosper_certification_W.py` | none (exact/symbolic) | THE main Gosper certification |
| `hyperexpand_fallback.py` | none (exact/symbolic) | hyperexpand fallback check |
| `order_swap_and_gf_diagnostics.py` | none (exact/symbolic) | supplementary diagnostics |
| `monte_carlo_bonus.py` | `20260930001`-`20260930008` | Section 8 large-`(n,K)` triangulation |

---

## 11. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Reference engine (cited Prop S + Layer-1 + exchangeability reduction) matches fresh brute force and D1/D2/D3 | **PROVED** (independent re-verification of the cited starting point) |
| 2 | `InnerJ(V,O)` depends on `(V,O)` only through `W=V+O` | **PROVED**, new, symbolic exact |
| 3 | Hockey-stick collapse `sum_{V=r}^{W} C(V-1,r-1) = C(W,r)` | **PROVED**, symbolic exact |
| 4 | `S_r(n,K,k) = sum_{W=r}^{k} C(W,r)*InnerJ(W)` (the W-collapse identity) | **PROVED**, new, verified 768/768 numeric cells |
| 5 | Collapsed W-sum Gosper-summable at every concrete K=1..7, symbolic r | **PROVED** (positive, `gosper_term`) |
| 6 | K=1,2 `gosper_sum` closed forms match true collapsed sum | **PROVED**, 6/6 |
| 7 | Collapsed W-sum NOT Gosper-summable for symbolic K | **CERTIFIED NON-EXISTENT** for this (new) formulation — second, independent certificate, `~12-13s`, `~25x` faster than Estagio 44's `313.1s` on the un-collapsed object |
| 8 | Positive/negative Gosper harness controls | **PROVED** (harness soundness confirmed) |
| 9 | Terminating hypergeometric-function representation exists for the collapsed sum, K symbolic | **PROVED** (`eval_sum_hyper` succeeds) |
| 10 | `hyperexpand` reduces that representation to elementary form | **DISPROVED** (does not reduce, matching Estagio 39's own analogous finding) |
| 11 | r-first summation order (fixed W) is Gosper-summable at concrete K | **DISPROVED** — fails already at concrete K=1..5, strictly worse than W-first |
| 12 | OGF identity `sum_K InnerJ(W;K)x^K = (Wx+r)(1+x)^{n-W+r-1}` | **PROVED**, new, elementary + numeric (coefficient extraction) |
| 13 | GF-marked (K eliminated) W-sum Gosper-summable, r concrete | **PROVED** (positive, r=0..5) |
| 14 | GF-marked W-sum Gosper-summable, r ALSO symbolic | **CERTIFIED NON-EXISTENT** — obstruction moves from K to r, sharper diagnosis |
| 15 | `sympy.holonomic` provides a decision procedure for broader-than-Gosper certification of an unevaluated symbolic-parameter sum | **INVESTIGATED, FOUND INAPPLICABLE** (honest disclosure, no broader certificate claimed) |
| 16 | Single closed-form CDF `P(M_n^{(K)}<=k/n)=F(n,K,k)` | **OPEN**, not reached by either route tried in this front |
| 17 | Full outer r-assembly, symbolic K | **NOT ATTEMPTED** (Section 7.2 — depends on item 7, and Diagnostic 1 shows the alternate order is worse) |
| 18 | `K -> infinity` asymptotics | **NOT ATTEMPTED** |

---

## 12. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `git` command run. The sibling directory
`general_k_closed_cdf_attempt/` was read (its `ATTEMPT.md` in full, and
`gosper_certification_vsum.py` for exact formula transcription only) but
never written to — every script in THIS directory implements its own
independent logic, verified from scratch against fresh brute force and
against the cited-and-reproduced reference engine, not copied from the
sibling's code. All work confined to this new subdirectory. Two
self-disclosed bugs in this front's own exploratory/verification process
are documented in place at the point they occurred (Section 4.4: an
unsimplified-term `hypersimp` recognition-failure that produced a
spurious fast `None`, caught and fixed before being reported as a
result; Section 6.2: a summation-range bug in an OGF-identity numeric
check, caught and fixed via coefficient extraction instead). Every claim
above is labeled PROVED / DISPROVED / CERTIFIED NON-EXISTENT / OPEN /
NOT ATTEMPTED / INVESTIGATED-FOUND-INAPPLICABLE at the point of use; no
claim is left as an unlabeled assertion. All randomized verification used
only the reserved seed range `20260930000`-`20260930999`. No claim of
progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
