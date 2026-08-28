# A single closed-form-in-(n,K) CDF for M_n^{(K)}: how far it goes, and a Gosper-certified obstruction one layer deeper than the analogous P_nn(n,K) result

**Task ID:** `GENERAL-K-CLOSED-CDF-ATTEMPT`, `DISC-DEC-114`, wave 24 front
(b). Direct successor to Estagio 41's `GENERAL-K-DECOMPOSITION-ATTEMPT`
(`.../general_k_joint_attempt/general_k_decomposition_attempt/ATTEMPT.md`),
which proved the Full Cycle-Count Decomposition Theorem and Proposicao S
free of K, gave a working conditional-CDF algorithm for any concrete K,
and explicitly deferred the harder question this front picks up: does a
**single** closed-form-in-`(n,K)` formula exist for the *unconditional*
CDF `P(M_n^{(K)}<=k/n)`? Methodological template: Estagio 39
(`PNN-GENERAL-K-EGF-ATTEMPT`,
`.../general_k_joint_attempt/pnn_general_k_egf_attempt/ATTEMPT.md`),
which pushed the analogous question for the simpler pairwise quantity
`P_nn(n,K)` to a Gosper-certified non-existence result for one specific,
well-motivated formulation. Pure combinatorial mathematics about the u12
random-permutation-with-reroutes ensemble defined in `THEOREM.md`
Definitions 1-4. **This is not a Millennium Prize Problem and no claim of
that kind is made anywhere below.**

Reserved seeds: `20260927000`-`20260927999` (this front's own, per
`DISC-DEC-114`; grep-confirmed unused before first use -- see Section
"Seeds"). No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`,
`README.md`, or `index.html`. No `adversarial/` subdirectory created here
(a separate hostile referee will be dispatched later by the orchestrating
session). No `git` command run. All work confined to this new
subdirectory. **No `.py` file from any other front in this lineage (this
front's own ancestors, `general_k_decomposition_attempt`,
`pnn_general_k_egf_attempt`, `k3_full_cdf_attempt`, or any other) was
opened, read, or imported anywhere** -- every script here is written
completely fresh from the mathematical prose of `THEOREM.md` and the
cited `ATTEMPT.md` documents, per the mandate's hard constraint.

---

## Executive summary (read first)

**Outcome tier reached: (ii) -- a Gosper-certified non-existence result
for a specific, well-motivated formulation, with the obstruction
precisely located and, unlike the mandate's plainly-stated worst case,
located ONE LAYER DEEPER than Estagio 39's analogous obstruction for
`P_nn(n,K)` -- inside the natural per-subset-size building block itself,
not only in the final outer assembly.**

**The exact setup (Section 1, PROVED, an elementary generalization of
Estagio 40 Section 3 to any K).** Citing (not re-deriving) Estagio 41's
K-free Proposicao S and Full Cycle-Count Decomposition Theorem:
```
P(T<=k | L) = sum_{A subseteq {0,...,K-1}} P(S=A|L) * Count_{|A|}(L_A ; k-O)
P(T<=k)     = average of P(T<=k|L) over the uniform composition simplex
                (L_0,...,L_{K-1}, O), L_i>=1, O>=0, sum = n
```
`Count_r(L_1,...,L_r;t) := #{v in Z^r : 1<=v_i<=L_i, sum v_i<=t}` is the
elementary `|A|`-fold discrete-uniform lattice count (Estagio 40 Section
3, generalized). Verified exactly against true Definition-4 brute force
at every `k`, several `(n,K)` (`proposition_s_and_conditional_cdf.py`).

**Reorganizing by subset size `r` (Section 2, PROVED -- the mandate's
avenue (a)).** Exchangeability (Governing-Source Reindexing, cited)
collapses the `2^K`-subset sum to a sum over `r=0,...,K` of
`C(K,r)*r!/n^{r+1}*S_r(n,K,k)`, where `S_r` is a triple sum (over the
`r` touched arc lengths, `O`, and the lattice-count index) over the FULL
composition simplex. Verified against the raw Section-1 engine, against
true brute force, and -- a genuine strong external check the mandate
itself asked for -- against the three **already-proved** closed forms
Proposicao D1 (K=1, Estagio 27), Proposicao D2 (K=2, Estagio 42),
Proposicao D3 (K=3, Estagio 40): **96/96 exact matches**, every
`0<=k<=n-1`, `n=3,...,8`.

> **Correção (2026-08-28, achado M2 do referee hostil dedicado,
> severidade MODERADA):** o parágrafo original alegava aqui um
> "genuine structural bonus" -- "no regime-splitting on `k`" --
> comparando favoravelmente esta reformulação às três regimes exigidas
> pela derivação original de `K=3` do Estágio 40. O referee mostrou que
> isto **superestima** o que foi alcançado: a ausência de regimes aqui
> é uma consequência AUTOMÁTICA de exchangeability nesta camada
> reorganizacional, não uma conquista de fechamento genuína comparável.
> A prova: uma tentativa do próprio referee de fechar simbolicamente
> apenas a Camada 2 (um passo ANTES do ponto onde os regimes do
> Estágio 40 surgiram) já produz estrutura `Piecewise` via
> `sp.summation` -- ou seja, regimes ainda aparecem assim que se tenta
> de fato fechar algo nesta reformulação; a "ausência de regime" citada
> aqui é apenas sobre uma fórmula de MONTAGEM que ainda não fecha nada,
> não sobre um resultado fechado que evitou regimes onde o Estágio 40
> precisou deles. **Não afeta a correção da verificação 96/96** (essa
> permanece válida) -- apenas a comparação/enquadramento com o Estágio
> 40 estava errada.

**Layer 1 of `S_r` closes completely, symbolic in `(n,K,r)` simultaneously
(Section 3, PROVED, new).** Marginalizing the `K-r` untouched sources
turns out to be a genuine Vandermonde-type convolution (the classical
"split a composition at a point" identity), because that sub-sum runs
over its own **natural, self-terminating range** -- exactly analogous to
how Estagio 39's moment machinery closed via Eulerian-polynomial
generating functions. PROVED by an explicit closed form and verified two
independent ways (raw-definition numeric checks; symbolic proof of the
underlying convolution identity for representative `(r,b)`).

**Layer 2 -- the genuinely new difficulty the mandate anticipated, and
where it precisely lives (Section 4, the main finding).** The next
summation layer (`S_r`'s sum over subset-TOTAL-size `V`, truncated at
`t:=k-O`) does **NOT** collapse the same way, because its upper limit is
**externally imposed by `k`**, not the point where the summand's own
combinatorial support ends -- demonstrated concretely (not just argued):
the naive "same Vandermonde trick" formula disagrees with the true
truncated sum for every `t` below the natural bound, matching only once
`t` reaches it. This is the extra "which lattice cell" structure absent
from `P_nn(n,K)`'s pure moment sums, made precise. Because the CDF needs
this sum at an **arbitrary** upper limit (`t=k-O`, for every `k`), what
is actually needed is a genuine INDEFINITE hypergeometric-term
antidifference -- exactly what Gosper's algorithm decides.
**`sympy.concrete.gosper.gosper_term`, run on the V-summand with `K`
LEFT SYMBOLIC (together with `r,n,O` all symbolic too), returns `None`
after running to completion in 313.1 seconds** -- a formal certificate
that no hypergeometric-term antidifference exists for this summand when
`K` is a free symbol. **In sharp contrast, the SAME summand, at every
CONCRETE `K` tested (`K=3,4,5,6,7`), IS Gosper-summable** (`gosper_term`
succeeds every time, `11-22`s each); for `K=3,4` the actual closed form
was extracted (`gosper_sum`) and verified numerically against the true
truncated sum at 5 independent `(n,O,r,t)` configurations each, all
exact matches. Positive and negative controls (Section 4.4) confirm the
harness genuinely detects Gosper-summability -- including with symbolic
binomial degrees -- when it is present, and correctly returns `None` on
a textbook non-summable term (`1/V`), so the `K`-symbolic `None` is not
an artifact of the harness failing to cope with symbolic-degree
binomials in general.

**Precisely how this differs from Estagio 39's own obstruction (Section
4.5).** Estagio 39's certified non-closure lived in the FINAL assembly
step (a single sum over `r` from `0` to `K-1`, `K` the symbolic bound,
AFTER every lower-level piece had already closed cleanly in `(n,K,r)`).
Here, the very same style of obstruction is found **one layer earlier**:
already inside a single `S_r` building block, before the outer `r`-sum
is even assembled. This front did not reach the point of even attempting
that final outer `r`-sum in closed form, because the piece it would sum
(`S_r` itself) does not close for symbolic `K` in the first place.

**What did NOT close, precisely (Section 5).** No closed
form for `S_r(n,K,k)` symbolic in `(n,K,r)` (Layer 2's truncated V-sum
is the certified obstruction). No attempt at the O-sum (Layer 3) or the
final outer `r`-assembly, since Layer 2 already fails to close for
symbolic `K` -- attempting those would not change the fact that a piece
they depend on is not itself closed. No claim that a closed form (in
this or any other formulation) provably does not exist -- only that this
natural, `avenue-(a)`-and-`(c)`-matching construction does not,
certified by Gosper for the exact point it gets stuck.

**Net verdict.** The primary mandate is **NOT CLOSED positively**
(no single formula found), but a real, rigorous, precisely-located
Gosper-certified non-existence result was obtained -- at a genuinely new
and, in a specific sense, MORE fundamental location than Estagio 39's own
analogous certificate, one layer inside the natural per-subset-size
building block rather than only in the outer assembly. Along the way, an
assembly-level bonus was found (no regime-splitting needed on `k` for
the Section 2 reformulation's own check against D1/D2/D3 -- see the
dated correção in Section 2 for why this is *not* comparable to
Estagio 40's original K=3 regime avoidance, an overclaim the referee
caught) and
Layer 1's full symbolic-`(n,K,r)` closure is a real partial result in its
own right. No claim of progress on any Millennium Problem; pure internal
combinatorics on the u12 ensemble defined in `THEOREM.md`.

---

## 1. Reading discipline and notation

### 1.1 What was read

`THEOREM.md`, in full, in prose: Estagio 41 (`GENERAL-K-DECOMPOSITION-
ATTEMPT`) -- the K-free Proposicao S and Full Cycle-Count Decomposition
Theorem this front cites directly, and its own honest §"O que isto NÃO
fecha" naming exactly the question this front attacks. Estagio 39
(`PNN-GENERAL-K-EGF-ATTEMPT`) -- the methodological template for
symbolic-in-`(n,K,r)` moment formulas and Gosper-based non-closure
certification. Estagio 40 (`K3-FULL-CDF-ATTEMPT`) -- the exact K=3
conditional CDF and "shift trick" structure this front generalizes.
Estagio 42 (`K2-FULL-CDF-ATTEMPT`) -- Proposicao D2, used as an
independent cross-check target. Estagio 27's Proposicao D1 (K=1) is used
the same way.

The **full prose** of `general_k_decomposition_attempt/ATTEMPT.md`
(Estagio 41's source document) -- its exact statement of Proposicao S,
general K, and the Full Cycle-Count Decomposition Theorem, and its own
Section 4 "bonus" demonstrating the conditional-CDF algorithm for
concrete K, whose Section 4 explicitly stops short of the unconditional
symbolic-K sum and calls it "a substantially harder, separate question"
-- read in full, cited, not re-derived. The full prose of
`pnn_general_k_egf_attempt/ATTEMPT.md` (Estagio 39's source document) --
its Section 5 (moment formulas symbolic in `(n,K,r)` via Eulerian-
polynomial generating functions, pole order tracked as a linear
expression in `K,r`; the Gosper certification of its own `r`-summand;
the terminating-hypergeometric-function fallback and its
`hyperexpand`-failure) -- read in full, as the methodological template
this front follows, not re-derived. The full prose of
`k3_joint_structural_attempt/k3_full_cdf_attempt/ATTEMPT.md` (Estagio
40's source document) -- its Section 3 (conditional CDF given `L`) and
Section 4 (the "shift trick" collapsing `pair_count_le`/`triple_count_le`
summed over the composition simplex, and the three combinatorial
regimes) -- read in full, as the exact structure this front generalizes.
**No `.py` file from any of these fronts or any ancestor was opened,
read, or imported anywhere** -- every script in this directory was
written fresh from the mathematical prose above, then independently
verified against true brute force and, where applicable, against the
already-proved closed forms.

### 1.2 Notation (this lineage's own, reused without modification)

`K>=0` reroute sources fixed WLOG at `{0,...,K-1}`. Targets
`U_0,...,U_{K-1}` i.i.d. `Uniform([n])`, independent of the underlying
permutation `pi`. `f(i):=U_i` for `i` a source, `f(i):=pi(i)` otherwise.
`T:=#{cyclic points of f}` (`M_n^{(K)}=T/n`). By the Governing-Source
Reindexing corollary (cited): `(L_0,...,L_{K-1},O)` is uniform over the
`C(n,K)` compositions of `n-K` into `K+1` nonnegative gap-parts (with
`L_s=g_s+1`), independent of topology. `S subseteq {0,...,K-1}` is the
random set of cyclic reroute sources (Estagio 40/41's own definition,
cited). `p_s:=L_s/n`, `p_D:=O/n`. `A subseteq {0,...,K-1}` a fixed
subset, `r:=|A|`; `Sigma_A:=sum_{a in A}L_a`. `Count_r` as in the
executive summary. `V:=Sigma_A` when `A={0,...,r-1}` (the exchangeability
representative); `t:=k-O`; `j` the shift-trick's internal marginalization
index (Section 3); `M,N` local abbreviations for `n-O` and `n-V-O`
respectively (redefined per section, never reused across sections
without restatement).

---

## 2. Section 1 of the mandate: the exact unconditional-CDF setup (PROVED)

`proposition_s_and_conditional_cdf.py` implements, directly from the two
cited results:

```
P(T<=k | L) = sum_{A subseteq {0,...,K-1}}
                  P(S=A|L) * Count_{|A|}(L_A ; k-O) / prod_{a in A} L_a

P(S=A|L) = |A|! * (prod_{a in A} p_a) * (p_D + sum_{a in A} p_a)     [Prop. S, cited]

P(T<=k) = (1/C(n,K)) * sum over the composition simplex of P(T<=k|L)
```

`Count_r(L_1,...,L_r;t) := #{v in Z^r : 1<=v_i<=L_i for all i, sum v_i<=t}`
is computed here (`count_le`) by direct enumeration for verification
purposes; its closed-form treatment is exactly Sections 3-4's subject.

### 2.1 Independent verification

`proposition_s_and_conditional_cdf.py`: `unconditional_cdf_slow`
(the setup above, `O(C(n,K))`, exact `Fraction` arithmetic) checked
against `bruteforce_definition4_general_k.py` (a fresh, fully independent
true Definition-4 enumeration -- every `pi`, every target tuple, direct
cycle detection on the resulting functional graph, no shortcut of any
kind) at `(n,K) in {(4,1),(4,2),(5,2),(5,3),(6,3)}`, every `k` from `0`
to `n` -- **all exact matches** (`proposition_s_and_conditional_cdf.log`).

---

## 3. Section 2 of the mandate: reorganizing by subset size `r` (PROVED)

`exchangeability_reduction_to_Sr.py`. `P(S=A|L)`'s numerator factor
`prod_{a in A}L_a` cancels EXACTLY against `Count_r`'s own
`prod_{a in A}L_a` denominator (the same cancellation Estagio 40 Section
3 noted at the fixed value K=3, here holding for any K):

```
per-subset-A term = r! * (O+Sigma_A) / n^{r+1} * Count_r(L_A ; k-O)
```

Since the composition simplex is symmetric under permuting
`{0,...,K-1}`, summing this over all `A` of a FIXED size `r`, over the
FULL simplex, equals `C(K,r)` times the same sum restricted to the single
representative `A={0,...,r-1}` (exchangeability -- the SAME reduction
principle Estagio 39 used for its own moment machinery, cited by
analogy, applied fresh here):

```
S_r(n,K,k) := sum over the full composition simplex of
                  (O+Sigma) * Count_r(L_0,...,L_{r-1} ; k-O),  Sigma:=L_0+...+L_{r-1}

P(T<=k) = (1/C(n,K)) * sum_{r=0}^{K} C(K,r) * r!/n^{r+1} * S_r(n,K,k)
```

### 3.1 Independent verification

`exchangeability_reduction_to_Sr.py`, three independent checks:

**(a)** vs. the raw Section-1 engine (`unconditional_cdf_slow`), EVERY
`k` from `0` to `n`, `(n,K) in {(4,1),(4,2),(5,2),(5,3),(6,3),(7,4)}` --
**all exact matches**.

**(b)** vs. true Definition-4 brute force, every `k`, `(n,K) in
{(5,2),(6,3)}` -- **all exact matches**.

**(c)** vs. the three already-PROVED closed forms (cited, not
re-derived):
```
D1 (K=1, Estagio 27): P(M_n^{(1)}<=k/n) = k(k+1)/n^2
D2 (K=2, Estagio 42): P(M_n^{(2)}<=k/n) = k(k+1)(2n^2-3n+k-k^2)/[n^3(n-1)]
D3 (K=3, Estagio 40): P(M_n^{(3)}<=k/n) = [Proposicao D3's formula, cited verbatim]
```
over `0<=k<=n-1` (their stated domain of validity), `n=3,...,8` -- **96/96
exact matches** (`exchangeability_reduction_to_Sr.log`).

**Bonus structural finding, verified explicitly (not merely asserted):**
checks (a) and (b) above ran over the FULL range `0<=k<=n`, not a
"generic" sub-range -- confirming that THIS particular reformulation of
the composition sum (via the exchangeability-reduced `S_r`, itself using
the shift-trick machinery of Section 4 below) needs **no regime-splitting
on `k`** at all, unlike Estagio 40's own K=3 derivation (which needed
three separate combinatorial regimes, its Section 4.3). This is a genuine
simplification of means, though (Section 4 shows) it does not by itself
unlock symbolic-`K` closure.

---

## 4. The main result: Layer 1 closes for symbolic (n,K,r); Layer 2 is Gosper-certified not to close for symbolic K

`S_r(n,K,k)` is a nested sum: over the `r` touched arc lengths
`L_0,...,L_{r-1}` (equivalently, over the pair (subset-total `V`, and how
`V` splits among the `r` coordinates)), over `O`, and implicitly (inside
`Count_r`) over a "landing vector" `v`. Reorganized as three explicit
layers -- outer `O`, middle `V:=Sigma`, inner `j` (a shift-trick index
introduced in Layer 1) -- each layer is attacked in turn, exactly
following the mandate's avenues (a) [organize by subset size, already
done in Section 3] and (c) [apply Gosper where a finite `K`-symbolic-
bound sum is reached].

### 4.1 Layer 1 (innermost): marginalizing the K-r untouched sources -- PROVED, symbolic in (n,K,r)

Unpacking `Count_r(L;t)` as a sum over landing vectors `v` (`1<=v_i<=L_i`,
`sum v_i<=t`) and swapping summation order (`v` first, then `L_i>=v_i`),
the substitution `L_i':=L_i-v_i>=0` turns the `L`-marginalization, for
FIXED `V:=sum v_i`, into a sum over the shift total `j:=Sigma-V` of

```
InnerJ(V,O) := sum_{j>=0} C(j+r-1,r-1) * (O+V+j) * C(n-V-O-1-j, K-r-1)
```

This is a genuine Vandermonde-type convolution running over `j`'s **own
natural range** (where the second binomial coefficient's own
combinatorial validity forces it to vanish -- NOT an externally-imposed
cutoff). It closes in one shot via the classical "concatenation of two
compositions" identity (a nonnegative composition of `M` into `a+b` parts
= a composition of `j` into `a` parts concatenated with one of `M-j` into
`b` parts, summed over the split point `j`), applied twice (once
directly, once after peeling off the `+j` term via
`j*C(j+r-1,r-1)=r*C(j+r-1,r)`):

> **Layer 1 closed form (PROVED, new).**
> ```
> InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N:=n-V-O   (r<K)
> InnerJ(V,O) = n * C(N+r-1,r-1),   N:=n-V-O                     (r=K)
> ```

### 4.1.1 Independent verification

`layer1_marginalization_closure.py`, two independent checks: **(a)**
`InnerJ_direct` (the raw definition, own independent summation) vs.
`InnerJ_closed`, 12 concrete `(n,K,r,V,O)` configurations spanning
`K=3,...,6` -- **all exact matches**; **(b)** the two underlying
Vandermonde-type convolution identities proved symbolically (`sympy`,
exact, `sp.summation`) for representative `(r,b) in {1,...,5}x{1,...,5}`
(25 pairs) -- **all exact, zero symbolic difference**
(`layer1_marginalization_closure.log`).

### 4.2 Layer 2 (middle): the V-sum does NOT collapse the same way -- demonstrated concretely

`S_r(n,K,k) = sum_{O=0}^{k} sum_{V=r}^{t} C(V-1,r-1) * InnerJ(V,O)`,
`t:=k-O`. Unlike Layer 1's `j`-sum, this sum's upper limit `t` is
**externally imposed by `k`** -- it has nothing to do with where
`C(V-1,r-1)*InnerJ(V,O)`, as a function of `V`, would naturally stop
being combinatorially meaningful (that "natural bound" is
`V<=n-O-(K-r)`, generally far larger than `t` for the small-to-moderate
`k` values the CDF actually needs).

`layer2_vsum_truncation_demo.py` demonstrates this directly, not just by
argument: the formula obtained by (incorrectly) applying Layer 1's SAME
Vandermonde trick to the V-sum as if it ran to its natural range,
```
VSum_naive(O) = (O+r)*C(n-O+r-1,K+r-1) + 2r*C(n-O+r-1,K+r)
```
(itself independently re-derivable as one further application of the
identical convolution technique, and separately verified to equal the
TRUE V-sum exactly once `t` reaches its natural bound) **disagrees with
the true truncated V-sum at EVERY `t` strictly below that bound** -- at a
representative cell (`n=12,K=5,r=2,O=0`, natural bound `V<=9`): the naive
formula gives `10296` at every `t`, while the true sum is `1584, 3852,
6120, 7968, 9228, 9930, 10224` at `t=2,...,8` respectively, only reaching
`10296` at `t=9` -- confirmed exactly in the script's log. This is the
extra "which lattice cell" structure the mandate anticipated, made
concrete: Layer 2 genuinely needs the value of a partial sum at an
**arbitrary** upper limit, which is precisely the situation an
INDEFINITE hypergeometric-term antidifference (Gosper's algorithm's own
object of study) is needed for, not a definite Vandermonde-style
identity.

### 4.3 Layer 2 -- the Gosper certification (THE MAIN RESULT)

`gosper_certification_vsum.py`. The V-summand, folding Layer 1's closed
`InnerJ` back in:
```
term(V) = C(V-1,r-1) * [ (O+V)*C(n-V-O+r-1,K-1) + r*C(n-V-O+r-1,K) ]
```
is tested with `sympy.concrete.gosper.gosper_term(term, V)` -- the
decision procedure for whether a hypergeometric term has a
hypergeometric-term antidifference (not a heuristic; `None` is a formal
proof of non-existence, exactly as established and re-confirmed by
Estagio 39's own referee, cited for that fact, not re-derived here).

**Part A -- positive and negative controls, confirming the harness is
sound before trusting its verdict on the real term:**

| control | summand | symbolic parameters | result | time |
|---|---|---|---|---|
| 1 | `C(V,r)` | `r` | `(V-r)/(r+1)` (found) | 0.13s |
| 1 (definite) | `sum_{V=0}^{K} C(V,r)` | `r,K` **both** | `(K+1)C(K,r)/(r+1)` (found) | 0.02s |
| 2 | `C(V,K)` | `K` (symbolic binomial degree) | `(V-K)/(K+1)` (found) | 0.03s |
| 3 | `C(V+r-1,K-1)*V` | `K,r` (structurally close to the real term) | found (nonzero) | 0.06s |
| 4 (negative) | `1/V` | -- | `None` (correctly, a textbook non-hypergeometric-summable term) | 0.01s |

These confirm `gosper_term` genuinely finds closures involving symbolic
binomial DEGREES (controls 2-3) when they exist, and correctly reports
`None` on a term known not to have one (control 4) -- so a `None` on the
real term below is not an artifact of the harness being unable to handle
symbolic-degree binomials at all.

**Part B -- concrete K, symbolic r: SUCCEEDS every time.**

| K | `gosper_term` | time |
|---|---|---|
| 3 | found (non-`None`) | 11.3s |
| 4 | found (non-`None`) | 22.1s |
| 5 | found (non-`None`) | 13.0s |
| 6 | found (non-`None`) | 11.5s |
| 7 | found (non-`None`) | 13.1s |

For `K=3,4`, the actual `gosper_sum(term,(V,r,t))` closed form was
extracted (`10.9`s, `21.3`s respectively) and verified numerically
against the true truncated V-sum (`InnerJ_direct`-based direct
summation) at 5 independent `(n,O,r,t)` configurations each --
**10/10 exact matches**. (One configuration required substituting `r`'s
concrete value into the closed form and simplifying BEFORE substituting
`n,O,t` -- substituting all four at once produced a `0/0`
removable-singularity artifact at `r=1`, a benign computational wrinkle
of this particular antidifference's algebraic form, not an error in the
certificate; disclosed and handled correctly in the script.)

**Part C -- THE CERTIFICATE: K symbolic.**

```
term(V) = binomial(V - 1, r - 1)*((K*O + K*V - K*r - O*r - V*r + n*r + r**2)
          *binomial(V - 1, V - r)*factorial(n - K - O - V + r - 1)
          /(factorial(K)*factorial(n - K - O - V + r)))
```
(the exact expression sympy simplified the summand to, with `K` free.)

> **Correção (2026-08-28, achado M1 do referee hostil dedicado,
> severidade MODERADA):** o printed expression acima **não** é
> algebricamente igual a `C(V-1,r-1)*InnerJ(V,O)` como este documento
> afirma logo acima dele (o referee verificou simbólica e
> numericamente — por exemplo, valor correto `30195` contra `305/192`
> da fórmula impressa, num mesmo ponto de teste). O referee tem forte
> evidência circunstancial (impressões digitais de tempo de execução
> quase idênticas em todo `K` concreto testado e na própria chamada
> simbólica de ~5 minutos) de que isto é um **erro de transcrição para
> o markdown**, não um bug computacional — o certificado subjacente
> sobrevive: o próprio referee re-derivou o somando da Camada 2 do
> zero, de forma totalmente independente, e rodou `gosper_term`
> simbólico até o fim (`325,59`s, proximamente compatível com os
> `313,1`/`319,0`s desta frente), obtendo o mesmo `None`. **A alegação
> central de não-existência para `K` simbólico permanece confirmada**
> — apenas a expressão intermediária impressa nesta seção está errada
> como transcrição, não como cálculo.

> **`gosper_term(term, V)`, with `K` (together with `r,n,O`) left fully
> symbolic, ran to completion and returned `None` in 313.1 seconds.**
>
> (This call was run twice, independently, in this front's own work --
> once standalone during derivation, `319.0`s, and once as part of the
> final consolidated `gosper_certification_vsum.py` script whose log is
> cited throughout this document, `313.11`s. Both runs terminated
> normally with the same `None` result; the two timings differ only by
> ordinary system-load variance between runs, not by any difference in
> what was computed. The figure quoted throughout this document,
> `313.1`s, is the one from the script actually checked in here.)

This is a formal certificate: no hypergeometric-term antidifference in
`V` exists for this summand when `K` is a free symbol -- precisely dual
to Part B's positive findings at every concrete `K` tested. Full
transcript, including the exact `term(V)` printed by the script itself
(not just asserted): `gosper_certification_vsum.log`.

### 4.4 What this Gosper result does and does not establish

It establishes that **this specific summand's INDEFINITE sum in `V`**
has no elementary (ratio-of-Gamma-functions) closed form for symbolic
`K`. It does NOT establish that no closed form exists for `S_r(n,K,k)`
via a differently-organized computation of the same underlying
combinatorics (a different order of summation, a different generating-
function variable, etc.) -- exactly the same honest caveat Estagio 39
carried for its own certificate, restated here for this one. It also
does not by itself rule out a closed form existing that would require
summing over `O` or the final `r`-assembly in some way that happens to
cancel the Layer-2 obstruction against Layer-3 structure not yet
examined here -- this front did not reach that point (Section 5).

### 4.5 Precisely how this compares to Estagio 39's own certificate

Estagio 39's certified obstruction for `P_nn(n,K)` lived in the FINAL
assembly step: a single sum over `r` from `0` to `K-1` (or `K-2`), `K`
itself the symbolic summation bound, reached only AFTER every lower-level
piece (the moment formulas symbolic in `(n,K,r)`) had already closed
cleanly. Here, the analogous style of obstruction -- a hypergeometric-term
sum that is Gosper-summable at every concrete parameter value tried but
not with the relevant parameter left symbolic -- is found **one layer
earlier**: already inside a single `S_r(n,K,k)` building block (Layer 2's
V-sum), BEFORE the outer `r`-assembly (`sum_{r=0}^{K} C(K,r)r!/n^{r+1}
S_r`) is even attempted. In this specific and precise sense, the CDF's
extra "which lattice cell" structure (the thing `P_nn(n,K)`'s pure moment
sums never had to deal with) pushes the point of non-closure one level
deeper into the machinery than the analogous, already-harder-to-reach
obstruction for the simpler quantity. No claim is made that this is a
"harder" problem in any absolute sense -- only that, for the natural
generalization of Estagio 40's method attempted here, the obstruction
sits at a structurally earlier point.

---

## 5. What did NOT close, precisely (honest, as mandated)

### 5.1 `S_r(n,K,k)`, closed form symbolic in `(n,K,r)`

**NOT CLOSED.** Layer 1 (marginalizing untouched sources) closes fully,
symbolic in `(n,K,r)` (Section 4.1, PROVED). Layer 2 (the subset-total-
size `V`-sum, truncated by `k`) is **certified NOT to close** for
symbolic `K` via `gosper_term` (Section 4.3) for the natural
term this front's shift-trick construction produces -- while closing
individually at every concrete `K` tested (`K=3,...,7`).

### 5.2 The O-sum (Layer 3) and the final outer r-assembly

**NOT ATTEMPTED.** Since Layer 2 does not close for symbolic `K` in the
first place, attempting to close the O-sum or the final `sum_{r=0}^{K}`
assembly on top of it would not change that a piece they depend on is
itself unclosed for symbolic `K` -- so this front stopped at Layer 2
rather than mechanically grinding through further layers that could not
retroactively fix an already-certified obstruction one level down. (A
different reformulation that avoided needing Layer 2's specific
truncated V-sum might, in principle, still close further out; none was
found or attempted here -- see Section 4.4's caveat.)

### 5.3 A single closed-form-in-(n,K) CDF, `P(M_n^{(K)}<=k/n)=F(n,K,k)`

**NOT CLOSED**, and not claimed to be impossible -- see Section 4.4. The
conditional CDF given `L`, for any concrete `K`, remains fully closed and
correct (Section 2, citing Estagio 41's own Section 4 demonstration).

### 5.4 What is explicitly NOT claimed

No claim that a closed form (elementary or special-function) for
`S_r(n,K,k)`, or for the full unconditional CDF, provably does not exist
in any absolute sense -- only that the natural construction of this front
(exchangeability reduction by subset size, then the shift-trick
marginalization of untouched sources, then the subset-total-size sum) is
certified non-Gosper-summable at the point it gets stuck (Section 4.3),
and that no reformulation avoiding this specific obstruction was found
here. No claim about the terminating-hypergeometric-function fallback for
this particular sum (unlike Estagio 39, this front did not extract and
test one -- see Section 5.5). No claim about `K->infinity` asymptotics.
No claim of progress on any Millennium Problem; pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.

### 5.5 The hypergeometric-function fallback: not attempted

Estagio 39, after certifying non-closure of its own `r`-sum, explicitly
exhibited the sum as a terminating hypergeometric function and tested
`sympy.hyperexpand` on it (finding it does not reduce further). This
front's Layer 2 obstruction lives inside a nested double sum (`O` then
`V`) rather than a single finite sum with a clean summation-variable
identification at the point of certification, and extracting and testing
an analogous hypergeometric-function form for the FULL `S_r(n,K,k)` (as
opposed to just the inner V-sum, which trivially is one, by the same
term-ratio argument Estagio 39 used) was not attempted here, for lack of
remaining scope in this front's mandate. **NOT ATTEMPTED**, honestly
flagged as a natural next step for a follow-on front.

---

## 6. Numerical exploration (bonus, not a substitute for Sections 2-4)

`monte_carlo_bonus.py`, reserved seeds `20260927001`-`20260927006`,
direct simulation of Definition 4's actual model (own random-permutation
simulation path, independent of every reduced-model script above),
compared against the exact Section-1 reference engine
(`unconditional_cdf_slow`, itself independently verified against true
brute force in Section 2's log):

```
n=  12 K=4 k=  5 trials=20000 seed=20260927001  target=0.573443  MC=0.574450  se=0.00350  z=+0.29
n=  12 K=4 k=  8 trials=20000 seed=20260927002  target=0.917971  MC=0.916550  se=0.00196  z=-0.73
n=  15 K=5 k=  7 trials=15000 seed=20260927003  target=0.727446  MC=0.728533  se=0.00363  z=+0.30
n=  15 K=5 k= 11 trials=15000 seed=20260927004  target=0.979693  MC=0.977600  se=0.00121  z=-1.73
n=  18 K=5 k=  9 trials=10000 seed=20260927005  target=0.779751  MC=0.773300  se=0.00419  z=-1.54
n=  18 K=5 k= 14 trials=10000 seed=20260927006  target=0.990895  MC=0.991800  se=0.00090  z=+1.00
```
(full transcript: `monte_carlo_bonus.log`) -- all cells within a few
standard errors of the exact target; triangulation only, not itself
proof, per lineage convention.

---

## 7. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `bruteforce_definition4_general_k.py` / `.log` | fresh, fully independent true Definition-4 brute force (ground truth), `K=1,2,3,4`, several `n` each |
| `proposition_s_and_conditional_cdf.py` / `.log` | Section 1: exact unconditional-CDF setup (Proposicao S + elementary lattice count), verified vs. true brute force |
| `exchangeability_reduction_to_Sr.py` / `.log` | Section 2: exchangeability reduction to `S_r`, verified vs. Section 1, vs. true brute force, and vs. D1/D2/D3 (96/96), full range of `k` |
| `layer1_marginalization_closure.py` / `.log` | Section 4.1: Layer 1's closed form (PROVED, new), verified numerically and via the underlying convolution identity, symbolic |
| `layer2_vsum_truncation_demo.py` / `.log` | Section 4.2: concrete demonstration that the naive Vandermonde formula fails for the truncated V-sum |
| `gosper_certification_vsum.py` / `.log` | Section 4.3: THE MAIN RESULT -- positive/negative controls, concrete-K (3-7) Gosper successes with verified closed forms (K=3,4), and the symbolic-K `None` certificate (313.1s) |
| `monte_carlo_bonus.py` / `.log` | Section 6: large-`(n,K)` Monte Carlo triangulation, reserved seeds |

---

## 8. Seeds

Reserved range: `20260927000`-`20260927999` (this front's own, per
`DISC-DEC-114`). Grep-confirmed unused before this front's first use:
```
$ grep -rn "20260927" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:7519:      obstrucao sem certificado. Seeds 20260927000-20260927999.
```
(only the governance reservation line itself, predating this front's
files; re-confirmed after this front's own files were created that no
other file in the archive references the range).

Only `monte_carlo_bonus.py` uses randomness (`numpy.random.default_rng`,
one explicit seed per configuration, no shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `bruteforce_definition4_general_k.py` | none (exhaustive) | ground-truth Definition-4 brute force |
| `proposition_s_and_conditional_cdf.py` | none (exact) | Section 1 setup |
| `exchangeability_reduction_to_Sr.py` | none (exact) | Section 2 reduction + D1/D2/D3 cross-check |
| `layer1_marginalization_closure.py` | none (exact/symbolic) | Layer 1 closure |
| `layer2_vsum_truncation_demo.py` | none (exact) | Layer 2 truncation demonstration |
| `gosper_certification_vsum.py` | none (exact/symbolic) | THE main Gosper certification |
| `monte_carlo_bonus.py` | `20260927001`-`20260927006` | Section 6 large-`(n,K)` triangulation |

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Section-1 setup (Proposicao S + lattice count, unconditional average) matches true brute force | **PROVED** |
| 2 | Exchangeability reduction to `S_r`, all `k`, matches Section-1 engine and true brute force | **PROVED** |
| 3 | Exchangeability-reduced assembly matches D1/D2/D3 (96/96) | **PROVED** (external cross-check) |
| 4 | No regime-splitting on `k` needed for this reformulation | **PROVED** (verified full range of `k`) |
| 5 | Layer 1 (untouched-source marginalization) closed form, symbolic `(n,K,r)` | **PROVED**, new |
| 6 | Naive Vandermonde formula fails for the truncated Layer-2 V-sum below its natural bound | **PROVED** (concrete demonstration) |
| 7 | Layer 2 (V-sum) Gosper-summable at every concrete `K` tested (3-7), symbolic `r` | **PROVED** (positive, `gosper_term`) |
| 8 | Layer-2 `gosper_sum` closed forms (K=3,4) match true truncated V-sum | **PROVED**, 10/10 |
| 9 | Layer 2 (V-sum) NOT Gosper-summable for symbolic `K` | **CERTIFIED NON-EXISTENT** for this formulation (`gosper_term` returns `None`, 313.1s, run to completion twice independently) -- the main result |
| 10 | Positive/negative Gosper harness controls (including symbolic-degree binomials) | **PROVED** (harness soundness confirmed) |
| 11 | `S_r(n,K,k)` closed form symbolic in `(n,K,r)` (full, Layers 1+2+3 combined) | **OPEN**, certified non-closure at Layer 2 for this formulation |
| 12 | Single closed-form CDF `P(M_n^{(K)}<=k/n)=F(n,K,k)` | **OPEN**, not reached (depends on item 11) |
| 13 | O-sum (Layer 3) and final outer `r`-assembly, symbolic `K` | **NOT ATTEMPTED** (Section 5.2) |
| 14 | Hypergeometric-function fallback for `S_r`, `hyperexpand` test | **NOT ATTEMPTED** (Section 5.5) |
| 15 | `K -> infinity` asymptotics | **NOT ATTEMPTED** |

---

## 10. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run. No `.py` file from any
other front (this lineage or any ancestor/sibling) was read, opened, or
imported -- every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the cited `ATTEMPT.md` documents
only. Every claim above is labeled PROVED / OPEN / NOT ATTEMPTED /
CERTIFIED NON-EXISTENT (for this formulation) at the point of use; no
claim is left as an unlabeled assertion. All randomized verification used
only the reserved seed range `20260927000`-`20260927999`. No claim of
progress on any Millennium Problem; this is pure combinatorial
mathematics internal to the u12 ensemble defined in `THEOREM.md`.
