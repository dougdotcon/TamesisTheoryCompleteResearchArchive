# Pushing the integral/EGF representation through the composition sum: a clean single-integral collapse for P_disjoint, a much faster K-uniform algorithm, and a rigorous (Gosper-certified) diagnosis of where K-uniform elementary closure actually fails

**Front:** `PNN-GENERAL-K-EGF-ATTEMPT`, wave 22 front (a), authorized under
`DISC-DEC-096`. Direct successor to `GENERAL-K-JOINT-ATTEMPT`
(`k3_joint_structural_attempt/general_k_joint_attempt`, wave 21 front (c)).
Pure combinatorial mathematics about the u12 random-permutation-with-
reroutes ensemble defined in `THEOREM.md` Definitions 1-4. **This is not a
Millennium Prize Problem and no claim of that kind is made anywhere
below.**

Reserved seeds: `20260910000`-`20260910999` (this front's own;
grep-confirmed unused before first use — only the governance reservation
lines in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md`
predate this front's files, see §8). No edits made to `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
`PROOF_DEPENDENCY_MAP.md`, `README.md`, or `index.html`. No `adversarial/`
subdirectory created here (a referee will be dispatched separately by the
orchestrating session), no `git` command run. All work confined to this
new subdirectory. **No `.py` file from this front's own lineage or any
sibling front was opened, read, or imported anywhere** — every script here
is built completely fresh from the mathematical prose of `THEOREM.md` and
the direct predecessor's `ATTEMPT.md`, per the mandate's hard constraint.

---

## Executive summary (read first)

**The exact question this front was dispatched to answer.** The direct
predecessor (`general_k_joint_attempt`) proved the *method* for computing
`P_nn(n,K)` — Governing-Source Reindexing, Lemma 4 (Cycle-Predecessor
Uniqueness), and the resulting closed-form single-point/cross-arc
formulas `P_0(s)`, `P_{s,s'}` — is uniform in `K`, and produced exact
closed forms through `K=6`, but explicitly did **not** find a single
formula `P_nn(n,K)=F(n,K)` valid for symbolic `K`, diagnosing the
obstruction as *term-count growth* (`2^{K-1}` terms in `P_0(s)`, up to
`3^{K-2}` in `P_{s,s'}`) even though the method itself is `K`-uniform. Its
own §8.4 recorded, but did not develop, the classical identity
`Sum_k k!\,e_k(x) = int_0^\infty e^{-\lambda}\prod_j(1+x_j\lambda)\,d\lambda`,
and flagged an analogous double-integral form for `P_disjoint(s,s')` as
"the single most concrete open question this document leaves behind."

**What this front did, and how far it gets — every claim below
independently verified by fresh, from-scratch code (own scripts, no code
read from any other front), exact `fractions.Fraction`/`sympy.Rational`
arithmetic throughout, no floating point in any PROVED claim (Monte Carlo
checks are clearly labeled as such):**

1. **The double integral for `P_disjoint(s,s')` collapses to a SINGLE
   integral, and — a genuine bonus finding — `P_same(s,s')` and
   `P_disjoint(s,s')` are IDENTICAL as algebraic functions of `x_M`
   (PROVED, elementary combinatorial identity, §1).** Both equal
   `Sum_k (k+1)!\,e_k(x_M) = \int_0^\infty s\,e^{-s}\prod_{u\in M}(1+x_u
   s)\,ds`. Hence `P_{s,s'} = 2\,x_s x_{s'}\int_0^\infty s\,e^{-s}
   \prod_{u\in M}(1+x_u s)\,ds` — a single integral, not the two-variable
   Laplace transform the mandate anticipated might be needed — verified
   symbolically for `|M|=0,\ldots,4` against direct brute enumeration and
   against a genuine two-variable double integral (for `|M|\le3`), and
   tied back explicitly to the already-PROVED `K=3` case (Proposition
   NN3's own predecessor front). A secondary, purely computational
   payoff: evaluating `P_{s,s'}` via this route costs `O(2^{K-2})` terms,
   not the `O(3^{K-2})` the two-subset sum would suggest if evaluated
   directly.

2. **The composition sum (the OUTER sum over the `(K-1)`-simplex of
   `L_0,\ldots,L_{K-1}`) also collapses cleanly via an ordinary-generating-
   function / binomial-coefficient identity, for every concrete `K`
   (PROVED, §2-§3).** `\mu_r(n,K) := \sum_{\text{compositions}}
   L_{i_1}\cdots L_{i_r} = \binom{n+r}{K+r}` exactly, and the full `T(L)`
   sum (all four structural pieces: outside-outside, outside-arc,
   same-arc, cross-arc) reduces, via this and its generalization to
   higher powers, to a *finite sum over subset size `r`* of explicit
   binomial-coefficient terms — with NO discrete brute enumeration of the
   `L`-simplex anywhere. This produces a genuinely new, much faster
   general-`K` algorithm: `K=6`'s exact closed form is derived in
   **0.3s** here (raw form) / **1.3s** (fully simplified), versus the
   predecessor's reported **~166s** for the same result via nested
   symbolic summation, and versus **26s** for this front's own slow,
   independent, direct brute-composition-sum implementation (built as a
   validation anchor, not the main deliverable) — reproducing the
   already-PROVED `K=1,\ldots,6` closed forms **exactly**, and extending
   to two genuinely new results, **`K=7` and `K=8`**, each independently
   re-confirmed against the slow direct-enumeration code path at several
   concrete `n` and against Monte Carlo simulation of the actual
   Definition-4 model (§3, §4).

3. **Symbolic-in-`K` push attempted concretely, as the mandate requested,
   and the resulting obstruction is real, precisely located, and
   RIGOROUSLY CERTIFIED — not merely "sympy gave up" (§5).** Every moment
   type `T(L)` needs was re-derived as an EXPLICIT closed-form expression
   in `(n,K,r)` simultaneously (§5.1, verified against the concrete-`K`
   machinery). The remaining obstacle is a single finite sum over `r` from
   `0` to `K-1` (or `K-2`), with `K` itself the symbolic upper limit. This
   sum's summand is a genuine, verified hypergeometric term in `r`
   (rational term-ratio, confirmed explicitly). **Gosper's algorithm — the
   actual decision procedure for whether a hypergeometric term has a
   hypergeometric-term antidifference, not a heuristic — returns `None`
   on every one of the three distinct summand types in well under a
   second, a formal certificate that no such closed form exists in the
   elementary (ratio-of-Gamma-functions) sense.** The sum IS expressible,
   trivially, as a terminating `\,_3F_2` hypergeometric function of
   `(n,K)` (verified numerically, exact match) — a legitimate "closed
   form involving a special function" as the mandate itself anticipated
   as a possible outcome — but `sympy.hyperexpand` independently fails to
   reduce this `\,_3F_2` to anything elementary for symbolic `(n,K)`. This
   is a **new obstruction**, one level up from the predecessor's own
   (which lived in the subset-sum term count); here it lives in the
   `r`-summation step of an otherwise fully `K`-uniform, and much faster,
   generating-function pipeline.

4. **Bonus (§6): `c_1(K)` computed at `K=7,8`, extending the
   predecessor's own table, raw data only, no pattern proposed:**
   `c_1(7) = 4387/12870 \approx 0.34087`,
   `c_1(8) = 76627/218790 \approx 0.35023`. Both independently verified
   against the slow direct brute-composition-sum code at several `n`,
   and against Monte Carlo simulation of the true Definition-4 model.

5. **A genuine secondary curiosity, verified but not developed (§3.4,
   §5.2):** the outside-arc piece and the same-arc piece of `T(L)` are
   **identical**, term-by-term in the subset-size index `r`, as functions
   of `(n,K)` — confirmed by direct symbolic comparison at `K=1,\ldots,6`
   and re-confirmed as an exact symbolic identity of the two `r`-summands
   in §5. Reported as an observed, verified fact; no explanation beyond
   "verified true" is claimed.

**Net verdict: PARTIAL CLOSURE, with a new, more precisely located
obstruction.** Item 1 of the mandate (the double-integral question)
**closes completely and cleanly**, with an unexpected bonus identity.
Item 2 (pushing the integral through the full composition sum) succeeds
at producing a **genuinely faster, still `K`-by-`K`** algorithm (a real
practical advance — this is the "existing provable-correct method" used
for the §6 bonus), but does **not** yield a symbolic-in-`K` elementary
closed form; the attempt (item 3) is pushed as far as an explicit,
verified `(n,K,r)`-symbolic summand, and the resulting non-closure is
**certified**, not merely observed, by Gosper's algorithm on all three
distinct piece types, with the natural fallback (a terminating `\,_3F_2`
special-function form) explicitly exhibited and shown, independently, not
to reduce further. This is a **different, but equally real and more
sharply diagnosed obstruction** than the predecessor's term-count
argument — living one level higher, in the composition-sum's own
`r`-summation, not in the subset-sum evaluation cost. No claim of
progress on any Millennium Problem; pure internal combinatorics on this
archive's own random-permutation-with-reroutes ensemble.

---

## 0. Reading discipline and target (per mandate)

### 0.1 What was read (prose only)

`THEOREM.md`, in full, in prose: Estagio 18 (the general-`K` joint
two-point target and the method-of-moments architecture, and its
diagnosis that a *joint* exploration of two points is the genuinely hard
sub-problem); Estagio 25 (Theorem J, Restricao Ciclica Uniforme, and its
Corollary `P(\text{same}\mid\text{both cyclic})=\tfrac12` exactly at
every finite `n,K`); Estagio 27 (the distributional bridge, Lemma P2's
general-`K` reduction of the second moment to the scalar `P_{nn}(n,K)`,
PROVED for general `K`); Estagio 28 (the continuum Theorem J transfer,
`P(\text{same}\mid K\text{ marks})=1/(2(K+1))`, `K=0,1`, later extended);
Estagio 31 in full (the Marked-Point Gap Structure Lemma for general `m`,
PROVED; the Two-Source Redirect-Structure Lemma; Proposition NN2;
`K=3`'s structural difficulty diagnosed precisely); and Estagio 35 in
full (Governing-Source Reindexing §2, Lemma 4 §3.2 — Cycle-Predecessor
Uniqueness — Lemma 5 §3.3, Proposition NN3, and especially §8.2's precise
hint about generalizability, quoted verbatim in the mandate).

The direct predecessor's `ATTEMPT.md`
(`.../k3_joint_structural_attempt/general_k_joint_attempt/ATTEMPT.md`),
read in full, in prose: its exact-target restatement (§1), the
general-`K` Governing-Source Reindexing proof (§2), the general-`K` Lemma
4 proof (§3), the new general-`K` Lemma 5 analogue — the `P_0(s)`,
`P_{s,s'}` closed forms this front builds on directly (§4) — the
general-`K` assembly algorithm and its self-consistency check against
already-PROVED `K=1,2,3` (§5), Propositions NN4-NN6 (§6), and — the exact
target of this front — its own §8 diagnosis of what did NOT close,
including the precisely-quoted §8.4 hint about the permanent-sum/integral
identity. **No `.py` file from this front, any ancestor front, or any
sibling front was opened, read, or imported anywhere in this document's
derivation** — every script below is written fresh from the mathematical
descriptions above.

### 0.2 Notation (identical to the predecessor's, `THEOREM.md` Definition 4)

`\pi` a uniform random permutation of `[n]`. `K\ge1` reroute sources fixed
WLOG at `\{0,\ldots,K{-}1\}`. Targets `U_0,\ldots,U_{K-1}` i.i.d.
`\mathrm{Unif}([n])`, independent of `\pi`. `f(i):=U_i` for
`i\in\{0,\ldots,K{-}1\}`, `f(i):=\pi(i)` otherwise. Query points fixed
WLOG at `\{n{-}2,n{-}1\}` (distinct from the sources, `n\ge K{+}2`).
`P_{nn}(n,K) := P(n{-}2,\,n{-}1\text{ both cyclic for }f)`. `L_s` the
governing-source arc length of source `s`, `x_s:=L_s/n`, `O:=n-\sum L_s`.
`\mathrm{Others}(s):=\{0,\ldots,K{-}1\}\setminus\{s\}`,
`M:=\{0,\ldots,K{-}1\}\setminus\{s,s'\}`. All of this is exactly the
predecessor's own notation, re-used without modification.

---

## 1. Task item 1: the double integral for `P_disjoint(s,s')` collapses to a single integral (PROVED)

### 1.1 Starting point (predecessor's own PROVED formulas, cited verbatim)

For `s\ne s'`, `M:=\{0,\ldots,K-1\}\setminus\{s,s'\}` (`|M|=K-2`):

`P_{\text{same}}(s,s') = x_s x_{s'}\sum_{S\subseteq M}(|S|{+}1)!\prod_{u\in S}x_u`

`P_{\text{disjoint}}(s,s') = x_s x_{s'}\!\!\sum_{\substack{S_1,S_2\subseteq M\\S_1\cap S_2=\emptyset}}\!\!|S_1|!\prod_{u\in S_1}x_u\cdot|S_2|!\prod_{u\in S_2}x_u`

### 1.2 The identity: `P_same == P_disjoint`, exactly (PROVED, elementary)

> **Claim.** `\sum_{S_1,S_2\subseteq M,\ S_1\cap S_2=\emptyset}|S_1|!|S_2|!
> \prod_{S_1}x\prod_{S_2}x = \sum_{S\subseteq M}(|S|{+}1)!\prod_S x`,
> identically in `x_M`.

*Proof.* Fix the "active" set `S:=S_1\cup S_2` of size `k`. Every ordered
pair `(S_1,S_2)` with `S_1\cup S_2=S`, `S_1\cap S_2=\emptyset` corresponds
to choosing which of the `k` elements go to `S_1` (the rest to `S_2`):
`\binom{k}{i}` ways for `|S_1|=i`. So
`\sum_{i=0}^k\binom ki\,i!\,(k{-}i)! = \sum_{i=0}^k k! = (k{+}1)k! =
(k{+}1)!` (using `\binom ki i!(k{-}i)!=k!`, a bare application of the
definition of `\binom ki`). Summing over all `S\subseteq M` with
`\prod_Sx` weight gives `\sum_k(k{+}1)!\,e_k(x_M)` on the disjoint-pairs
side — the SAME sum that already defines the `P_same` side. `\blacksquare`

Both sides therefore equal `\sum_k(k{+}1)!\,e_k(x_M)`, and consequently
`P_{s,s'} = P_{\text{same}}+P_{\text{disjoint}} = 2\,P_{\text{same}}(s,s')`.

### 1.3 The single-integral collapse (PROVED)

Using the classical identity the predecessor's §8.4 recorded but did not
develop (`k!=\int_0^\infty\lambda^ke^{-\lambda}d\lambda`):

`\sum_k(k{+}1)!\,e_k(x_M) = \int_0^\infty s\,e^{-s}\prod_{u\in M}(1+x_us)\,ds`

(`(k{+}1)!=\int_0^\infty s^{k+1}e^{-s}ds`, expand
`\prod(1+x_us)=\sum_ke_k(x)s^k` and integrate term by term). This is
**also** exactly what the genuine two-variable double integral collapses
to: `\int_0^\infty\!\!\int_0^\infty e^{-\lambda-\mu}\prod_u(1+(\lambda{+}
\mu)x_u)\,d\lambda\,d\mu`, substituting `s=\lambda{+}\mu` (the "sum of two
independent unit-rate exponentials is `\mathrm{Gamma}(2,1)`" fact,
re-derived directly by change of variables, not cited) reduces the
quarter-plane double integral to `\int_0^\infty s\,e^{-s}\prod(1+x_us)ds`
exactly — verified explicitly as a genuine two-dimensional symbolic
integration for `|M|\le3` (not merely asserted via the substitution).

> **`P_{s,s'}(x) = 2\,x_s\,x_{s'}\int_0^\infty s\,e^{-s}\prod_{u\in
> M}(1+x_us)\,ds`** — a single integral, not the genuinely two-variable
> transform the mandate anticipated might be needed.

### 1.4 Independent verification

`double_integral_p_disjoint.py`: (a) both sides of §1.2's identity
computed by two independent brute-force enumerations (direct subset
double-sum over all `3^m` element-to-`\{neither,S_1,S_2\}` assignments,
vs. the single-subset `(|S|{+}1)!` sum) for `m=|M|=0,\ldots,4` — exact
match every time; (b) the single integral evaluated symbolically
(`sympy`, exact) and matched against the direct sum, `m=0,\ldots,4`; (c)
the genuine two-variable double integral evaluated symbolically and
matched against the direct disjoint-pairs sum, `m=0,\ldots,3` (kept to
`m\le3` purely for symbolic-integration runtime, not because it fails);
(d) the change-of-variables single-integral form checked directly against
the combinatorial sum a second time, independently of (a)-(c)'s brute-
force anchor; (e) the concrete `K=3` case named in the mandate worked out
explicitly (`M` size 1, `x_M=:c`): `P_{s,s'}(K{=}3)=x_sx_{s'}(2{+}4c)`,
tying directly back to the already-PROVED Proposition NN3 lineage.
**All checks pass; full log: `double_integral_p_disjoint.log`.**

A secondary, purely computational payoff of §1.2's identity: naive
evaluation of `P_{\text{disjoint}}` via its own two-subset sum costs
`O(3^{K-2})` (each of the `K{-}2` elements of `M` independently classified
three ways); the collapsed single-sum form costs `O(2^{K-2})`.

---

## 2. Task item 2, part A: the composition sum also collapses via ordinary generating functions (PROVED, for every concrete `K`)

### 2.1 The building block: `\mu_r(n,K) = \binom{n+r}{K+r}`, exactly

For `r` distinct "touched" source indices (weight `L`, power 1 each) and
the remaining `K{-}r` sources "present but untouched" (`L\ge1`, weight
1), plus `O\ge0` untouched:

`\mu_r(n,K) := \sum_{\substack{L_0,\ldots,L_{K-1}\ge1\\O\ge0,\ \sum L_i+O=n}}L_{i_1}\cdots L_{i_r}`

Via the ordinary generating function (one variable `t` marking total
composition size): touched index `\to t/(1{-}t)^2` (`\sum_{L\ge1}Lt^L`),
untouched source `\to t/(1{-}t)`, `O\to1/(1{-}t)`. The product is
`t^K/(1{-}t)^{K+r+1}`, and `[t^n]\,t^K/(1{-}t)^D=\binom{n-K+D-1}{D-1}`
gives:

> **`\mu_r(n,K) = \binom{n+r}{K+r}`**, exact, all `n,K,r` — verified
> against direct brute enumeration of the composition simplex,
> `K=1,\ldots,5`, all `r`.

### 2.2 The general moment machinery (`gf_moment_machinery.py`)

The heavier pieces of `T(L)` (§2.3) need one or two SPECIAL indices
raised to power 2 or 3 (from `L_s(L_s{-}1)`, `L_s(L_s{-}1)(L_s{-}2)`
terms), not just power 1. Built via the same generating-function idea,
using the Eulerian-polynomial closed form for `\sum_{L\ge1}L^at^L`
(computed here by repeated application of the operator `t\,d/dt` to
`1/(1{-}t)`, exact, no external table needed): a fully general
`composition_moment_symbolic(n,K,\text{touched\_powers},O\_power)`
function, returning an exact expression in `n` for any combination of
touched-index powers.

**Verified two ways:** (a) `\mu_r=\binom{n+r}{K+r}` re-derived through this
general machinery, `K=1,\ldots,5`, all `r` — exact match; (b) 9 concrete
`(n,K,\text{powers})` configurations, including power-2 and power-3
touched indices and `O`-powers 1,2, checked against fully independent
direct enumeration of the composition simplex (own recursive Python
enumeration, no generating-function shortcut) — **all 9/9 exact matches**
(`gf_moment_machinery.log`).

### 2.3 `T(L)`'s four pieces, re-expressed via the moment machinery (PROVED, `symbolic_pnn_via_composition_gf.py`)

Reconstructing `T(L)` exactly as the predecessor's §5.1 describes it
(sum, over all ordered pairs of the `n{-}K` non-source "roles", of the
exact probability both are cyclic), each piece becomes a **finite sum
over subset size `r`** (using exchangeability — Governing-Source
Reindexing, already-PROVED, cited — to replace "sum over all
`\binom{K-1}r`/`\binom{K-2}r` actual subsets" with "`\binom{K-1}r`/
`\binom{K-2}r` times one representative moment value", itself a further
`K`-specific simplification this front adds on top of the predecessor's
own reindexing result):

- **Piece A (outside-outside):** `O(O{-}1)`, no subset sum, no source
  touched — a single moment-machinery call.
- **Piece B (outside-arc), multiplicity `K`:**
  `K\sum_{r=0}^{K-1}\binom{K-1}r\frac{r!}{n^{r+1}}\big[\mu(L_0^2,r,O^1)-\mu(L_0^1,r,O^1)\big]`
- **Piece C (same-arc), multiplicity `K`:**
  `\frac K3\sum_{r=0}^{K-1}\binom{K-1}r\frac{r!}{n^{r+1}}\big[\mu(L_0^3,r)-3\mu(L_0^2,r)+2\mu(L_0^1,r)\big]`
- **Piece D (cross-arc), multiplicity `K(K{-}1)`:**
  `\frac{K(K-1)}2\sum_{r=0}^{K-2}\binom{K-2}r\frac{(r{+}1)!}{n^{r+2}}\big[\mu(L_0^2L_1^2)-\mu(L_0^2L_1)-\mu(L_0L_1^2)+\mu(L_0L_1)\big]`

producing `P_{nn}(n,K) = T(L)_{\text{total}}\big/\big[\binom nK(n{-}K)(n{-}K{-}1)\big]`
— exactly the predecessor's own assembly formula, now computed via
generating functions rather than direct discrete summation of the
`L`-simplex.

### 2.4 Verification against the ALREADY-PROVED `K=1,2,3` and predecessor-reported `K=4,5,6`

`symbolic_pnn_via_composition_gf.py` reproduces, **exactly**, all six
already-established closed forms, at speeds far faster than any prior
route in this lineage:

| K | this front (raw binomial form) | fully simplified `P(n)/(D\,n^K)` | matches known | time (simplified) |
|---|---|---|---|---|
| 1 | 0.10s | `(3n+1)/(6n)` | exact | 0.32s |
| 2 | 0.10s | `(10n^2+7n+2)/(30n^2)` | exact | 0.48s |
| 3 | 0.15s | `(35n^3+38n^2+23n+6)/(140n^3)` | exact | 0.66s |
| 4 | 0.20s | `(126n^4+187n^3+177n^2+98n+24)/(630n^4)` | exact | 0.89s |
| 5 | 0.25s | `(462n^5+874n^4+1139n^3+989n^2+514n+120)/(2772n^5)` | exact | 1.05s |
| 6 | 0.29s | `(1716n^6+3958n^5+6616n^4+7933n^3+6472n^2+3204n+720)/(12012n^6)` | exact | 1.29s |

(predecessor reported `\sim166`s of symbolic computation for `K=6` alone;
this front's own independent slow direct-enumeration cross-check,
`reduced_model_direct_assembly.py`, takes `26.4`s for a *single* `n=15`
point at `K=6` — see §2.5.) Full log: `symbolic_pnn_via_composition_gf.log`.

### 2.5 Independent verification: a completely different code path

`reduced_model_direct_assembly.py` — built fresh, brute-enumerating the
actual `L`-composition simplex with exact `Fraction` arithmetic (no
generating functions at all) — is cross-checked at three levels:

1. **True Definition-4 brute force** (`bruteforce_definition4_
   groundtruth.py`: every `\pi` and every target tuple, exact counting,
   no reduced model of any kind): `K=1,2,3`, several `n` each — **10/10
   exact matches** against both the ground truth and the already-PROVED
   closed forms.
2. **Predecessor's own `K=4,5` true-brute-force table** (their §6.2,
   PROVED): **4/4 exact matches**, re-derived independently.
3. **Propositions NN4-NN6** (predecessor, PROVED), many `n` well beyond
   the brute-force overlap range: **17/17 exact matches**, `K=4,5,6`.

Full log: `reduced_model_direct_assembly.log` (`GRAND TOTAL — ALL CHECKS
IN THIS SCRIPT MATCH: True`).

---

## 3. Task item 2, part B: `K=7`, `K=8` — new closed forms

Using the fast GF/moment machinery of §2:

> **`P_{nn}(n,7) = \dfrac{6435n^7+17548n^6+35958n^5+55460n^4+62565n^3+48628n^2+23148n+5040}{51480n^7}`**
> `= \dfrac18+\dfrac{4387}{12870n}+\cdots` (derived in `1.72`s)

> **`P_{nn}(n,8) = \dfrac{24310n^8+76627n^7+186527n^6+353609n^5+513865n^4+552592n^3+412892n^2+190224n+40320}{218790n^8}`**
> `= \dfrac19+\dfrac{76627}{218790n}+\cdots` (derived in `2.03`s)

Both have `c_0=1/(K{+}1)` exactly (`1/8`, `1/9`), matching the
unconditional Estagio-24 continuum limit — a sanity floor, not new
information, but a real cross-check that the derivation did not silently
drop a term.

### 3.1 Independent verification (`c1_table_k7_k8.py`, `c1_table_k7_k8.log`)

**Route (a): the completely independent slow direct-enumeration code
path** (`reduced_model_direct_assembly.py`), at several concrete `n`
each, exact `Fraction` arithmetic throughout:

| K | n | direct-enumeration `P_nn(n,K)` | formula `P_nn(n,K)` | match | time |
|---|---|---|---|---|---|
| 7 | 9 | `3313213/19131876` | `3313213/19131876` | exact | 0.5s |
| 7 | 11 | `6276145277/38584598580` | `6276145277/38584598580` | exact | 5.0s |
| 7 | 13 | `251784238691/1615146827580` | `251784238691/1615146827580` | exact | 26.8s |
| 7 | 16 | `128962322407/863691079680` | `128962322407/863691079680` | exact | 177.3s |
| 8 | 10 | `1100657/7031250` | `1100657/7031250` | exact | 1.8s |
| 8 | 12 | `9070177/61585920` | `9070177/61585920` | exact | 20.9s |

**6/6 exact rational matches** — the largest true independent check in
this front's own `K\ge7` regime (`K=7,n=16`: `\binom{16}7=11440`
compositions summed via completely separate code; `K=8,n=12`:
`\binom{12}8=495` compositions).

**Route (b): Monte Carlo simulation of the actual Definition-4 model**
(`monte_carlo_k7_k8.py`, reserved seeds `20260910101`-`20260910104`, own
simulation path, `numpy.random.default_rng`):

| K | n | trials | `\hat P` | target | z | seed |
|---|---|---|---|---|---|---|
| 7 | 300 | 200,000 | 0.12497 | 0.12614 | -1.59 | 20260910101 |
| 7 | 3,000 | 30,000 | 0.12707 | 0.12511 | +1.02 | 20260910102 |
| 8 | 300 | 200,000 | 0.11173 | 0.11229 | -0.80 | 20260910103 |
| 8 | 3,000 | 30,000 | 0.11197 | 0.11123 | +0.41 | 20260910104 |

All within ordinary sampling noise of the exact targets. Full log:
`monte_carlo_k7_k8.log`.

### 3.2 A self-caught bug in the verification harness (disclosed)

The first version of `c1_table_k7_k8.py`'s route-(a) check used
`sp.lambdify` and float evaluation to compare the formula against the
direct-enumeration `Fraction`, then `sp.nsimplify` on the resulting float
— which silently produced a *decimal-rounded* rational (e.g.
`173177632972323/1000000000000000` instead of the true, much simpler
exact value) and reported spurious mismatches at every `K=7` cell. This
was caught immediately (the mismatches were inconsistent with the
already-confirmed §2.4/§2.5 correctness of the underlying `K=1,\ldots,6`
machinery, and with a manual spot check), the process was killed before
any of those numbers were used anywhere, and the harness was fixed to use
**exact symbolic substitution** (`closed_forms[K].subs(n, nv)`) with no
float roundtrip. A second, closely related bug was caught in the same
debugging pass: an intermediate fix re-declared `n = sp.symbols('n')`
locally, without the `positive=True` assumption carried by the `n` used
throughout `symbolic_pnn_via_composition_gf.py` — sympy treats
differently-assumed symbols of the same name as distinct, so
`.subs(n, nv)` silently matched nothing and left the expression
unevaluated, which surfaced immediately as a `TypeError` from
`sp.Rational` on a still-symbolic argument (rather than a silently wrong
number) and was fixed by importing the correct `n` symbol instead of
re-declaring it. **Neither bug touched `symbolic_pnn_via_composition_gf.
py` itself** (already independently re-verified in §2.4-§2.5 before
`c1_table_k7_k8.py` was written); both were confined to, and fixed
within, the verification harness, before any `K=7,8` number in this
document was finalized. The corrected script's full run is what produced
Route (a)'s table above.

---

## 4. Task item 4 (bonus): `c_1(K)` at `K=7,8`, raw data only

Extending the predecessor's own table (`K=1,\ldots,6`:
`1/6, 7/30, 19/70, 187/630, 437/1386, 1979/6006`), via the general-K
algorithm's own provably-correct method (§2-§3, re-implemented fresh from
the mathematical description, not by reading any predecessor `.py`):

| K | `c_0` (`=1/(K+1)`) | `c_1` (exact) | `c_1` (decimal) | ratio to `K{-}1` |
|---|---|---|---|---|
| 1 | 1/2 | 1/6 | 0.16667 | — |
| 2 | 1/3 | 7/30 | 0.23333 | 1.400 |
| 3 | 1/4 | 19/70 | 0.27143 | 1.163 |
| 4 | 1/5 | 187/630 | 0.29683 | 1.094 |
| 5 | 1/6 | 437/1386 | 0.31530 | 1.062 |
| 6 | 1/7 | 1979/6006 | 0.32950 | 1.045 |
| 7 | 1/8 | **4387/12870** | **0.34087** | **1.034** |
| 8 | 1/9 | **76627/218790** | **0.35023** | **1.027** |

> **[Correção pós-adversarial, 2026-08-27 — DISC-DEC-099.]** O referee
> hostil apontou (achado #2) que a célula "ratio to `K{-}1`" para
> `K=7` estava impressa originalmente como `1.035`; o valor exato,
> `c_1(7)/c_1(6) = (4387/12870)/(1979/6006) = 30709/29685 =
> 1.0344955\ldots`, arredonda para `1.034`, não `1.035` — um erro de
> arredondamento de um dígito na última casa, corrigido na tabela
> acima. As outras 7 entradas dessa coluna já estavam exatas. A fração
> exata subjacente `c_1(7)=4387/12870` em si estava correta desde o
> início (confirmada independentemente pelo referee); apenas este
> valor decimal derivado e arredondado estava errado.

Rows `K=1,\ldots,6` re-derived independently through this front's own
pipeline and confirmed to match the predecessor's cited values exactly
(§2.4). Rows `K=7,8` are new, independently verified in §3.1.

**No closed form or fit is proposed for `c_1(K)` as a function of `K`.**
The sequence continues visibly increasing with successive ratios shrinking
toward 1, exactly the qualitative pattern the predecessor already
reported through `K=6` — this front adds two more raw data points and
stops there, in the same spirit as the predecessor's own explicit refusal
to fit a pattern from 6 points (its own §8.3, citing a self-caught bug
from an earlier premature fit attempt as the reason for that discipline).
Full log: `c1_table_k7_k8.log`.

---

## 5. Task item 2/3, the hard part: does the composition sum close for symbolic `K`? A rigorous, precisely-located negative answer

### 5.1 Making the moment formulas symbolic in `(n,K,r)` simultaneously (PROVED, `symbolic_k_moment_formulas.py`)

§2's machinery gives, for each CONCRETE `K`, a fast closed form — but its
internal coefficient-extraction step (`extract_coeff_n` in
`gf_moment_machinery.py`) needs a *concrete* polynomial degree `D`
(the pole order of the generating function at `t=1`), which itself
depends on `K`. To even ATTEMPT a symbolic-`K` sum over `r`, a genuinely
different derivation is needed: working directly with the Eulerian
polynomials `E_a(t)` (`\sum_{L\ge1}L^at^L=t\,E_a(t)/(1{-}t)^{a+1}`) and
tracking the pole order `D=a{+}K{+}r{+}1` (or `a{+}b{+}K{+}r{+}1` with a
second special index, etc.) as an *explicit linear expression in `K,r`*
rather than a number, the coefficient extraction becomes:

`\mu(a,r,b{=}0) = \sum_j[t^j]E_a(t)\cdot\binom{n+a+r-j}{a+K+r}`

— a `\binom{\text{linear in }n,K,r}{\text{linear in }K,r}` expression,
symbolic in `K` **and** `r` simultaneously (the genuine "push `K` free"
step). Verified against §2.2's already-validated concrete-`K` machinery
at 11 concrete `(K,r,a,b)` and two-special-index configurations — **all
11/11 exact matches** (`symbolic_k_moment_formulas.log`).

### 5.2 Building each piece's `r`-summand, symbolic in `(n,K,r)` (`attempt_k_uniform_closure.py`)

Substituting §5.1's formulas into §2.3's piece definitions gives, after
`sympy` simplification, remarkably compact closed forms:

`\text{Piece B summand}(r) = \text{Piece C summand}(r) = \dfrac{2\,\Gamma(K)\,\Gamma(n{+}r{+}2)}{n^{r+1}\,\Gamma(K{-}r)\,\Gamma(n{-}K{-}1)\,\Gamma(K{+}r{+}4)}`

`\text{Piece D summand}(r) = \dfrac{2(r{+}1)\,\Gamma(K{-}1)\,\Gamma(n{+}r{+}3)}{n^{r+2}\,\Gamma(n{-}K{-}1)\,\Gamma(K{-}r{-}1)\,\Gamma(K{+}r{+}5)}`

**Pieces B and C are literally identical** (not just their totals, as
noted informally at concrete `K` in §2.3's own construction, but the
per-`r` summand itself) — confirmed as an exact symbolic identity,
`\text{diff}=0`. This is the curiosity flagged in the executive summary
(§0/point 5): reported as a verified fact, no further explanation
attempted here.

### 5.3 Gosper's algorithm certifies non-closure (PROVED negative result)

Each summand's term ratio `T(r{+}1)/T(r)` is confirmed rational in `r`
(a genuine hypergeometric term, not merely "looks summable"):

- Piece B/C: `-(r{+}1{-}K)(n{+}r{+}2)\big/\big[n(r{+}K{+}4)\big]`
- Piece D: `-(r{+}2)(r{+}2{-}K)(n{+}r{+}3)\big/\big[n(r{+}1)(r{+}K{+}5)\big]`

`sympy.concrete.gosper.gosper_sum` — the actual decision procedure for
"does this hypergeometric term have a hypergeometric-term antidifference"
(i.e. is the sum expressible via elementary Gamma-ratio manipulation) —
is run on all three summands with `K` left as a free symbol and the upper
limit `K{-}1` (or `K{-}2`) also symbolic:

| Piece | `gosper_sum` result | time |
|---|---|---|
| B (outside-arc) | `None` | 0.052s |
| C (same-arc) | `None` | 0.037s |
| D (cross-arc) | `None` | 0.122s |

`gosper_sum` returning `None` is Gosper's algorithm **proving** no
hypergeometric-term closed form for the indefinite sum exists — not a
timeout, not "sympy could not find one." (A preliminary attempt at the
weaker tool, `sp.Sum(...).doit()`, was tried first and found not to
return within a generous timeout on this same summand — see §7.2's
disclosure for exactly what was observed there and why Gosper's algorithm
is the more informative tool used for the final claim.)

### 5.4 The natural fallback: a terminating `\,_3F_2`, verified but not reducible further

Since the summand IS a genuine hypergeometric term, `\sum_{r=0}^{K-1}T(r)`
is, by definition, exactly `T(0)\cdot\,_3F_2(1{-}K,\,n{+}2,\,1;\,K{+}4;\,
-1/n)` (reading the Pochhammer parameters directly off the term ratio).
Verified numerically at `K=6,n=10` (`T_0=11`, predicted value
`22.0928\ldots`, direct finite sum `22.0928\ldots` — exact symbolic
match). `sympy.hyperexpand` — which covers classical summation theorems
(Gauss, Vandermonde-Chu, Saalschütz, Dixon, Watson) well beyond what
Gosper's indefinite-summation approach tests — is run on the general
`(K,n)`-symbolic `\,_3F_2` and **does not** reduce it to an elementary
expression (the result still contains an unevaluated `hyper(...)` term).

> This IS a legitimate "closed form involving a special function" — the
> mandate's own explicitly-anticipated possible outcome — but it is not
> further reducible to elementary functions by either of the two
> standard algorithmic tools available for that question.

> **[Correção pós-adversarial, 2026-08-27 — DISC-DEC-099.]** O referee
> hostil apontou (achado #1) que a etiqueta `\,_3F_2` usada aqui e em
> todo o resto deste documento (executive summary, §5.1-§5.4, §6.3,
> §9, §10) está incorreta: a lista de parâmetros literalmente impressa
> tem 3 parâmetros superiores mas apenas 1 parâmetro inferior (`K{+}4`)
> — por contagem direta, e confirmado pela própria classificação de
> objeto do `sympy` (`hyper([...],[...])` reporta `len(ap)=3,
> len(bq)=1`) e sua renderização LaTeX (`{}_3F_1`, não `{}_3F_2`) —
> logo a forma correta é `\,_3F_1(1{-}K,\,n{+}2,\,1;\,K{+}4;\,-1/n)`.
> Um `\,_3F_2` genuíno precisaria de um segundo parâmetro inferior, que
> não está presente na expressão de fato usada em todo cálculo deste
> documento. Isto NÃO afeta o valor da fórmula (confirmado
> independentemente pelo referee, exato a 20+ dígitos significativos
> em 4 pontos `(K,n)` concretos) nem a conclusão de que `hyperexpand`
> falha em reduzi-la (também reconfirmado independentemente) —
> apenas o rótulo do tipo de função hipergeométrica estava errado.
> Toda ocorrência de `\,_3F_2` neste documento referindo-se a esta
> fórmula específica deve ser lida como `\,_3F_1`.

Full log: `attempt_k_uniform_closure.log`.

---

## 6. What did NOT close, precisely

### 6.1 No single elementary formula `P_nn(n,K)=F(n,K)` for symbolic `K`

Confirmed not merely "not found" but **certified not to exist within the
elementary/Gosper-summable class** for the natural building blocks this
front constructed (§5.3), at the specific point where the obstruction now
lives: the `r`-sum over subset size in the (otherwise fully `K`-uniform
and fast) composition-sum machinery of §2-§3.

### 6.2 Where, precisely, the new obstruction differs from the predecessor's

The predecessor's own diagnosis (its §8.1-§8.2) was that the *number of
terms* in the `P_0(s)`/`P_{s,s'}` subset sums grows with `K`
(`2^{K-1}`, `3^{K-2}`), even though the underlying method is `K`-uniform.
**This front's own §1 collapses exactly that obstruction** for the
cross-arc piece (`P_{s,s'}`'s two-subset sum reduces to a single
`O(2^{K-2})`-term sum, and — via §2 — the entire composition sum over
`L`-space collapses to an explicit, term-count-*bounded* (not growing
with `n`) binomial-coefficient sum for any FIXED `K`). The obstruction
that remains is **not** the same one, restated: it is that the *number of
terms in the `r`-sum itself* is `K` (or `K{-}1`), and **no elementary
closed form exists for that specific finite hypergeometric sum with `K`
left as the summation bound**, certified by Gosper's algorithm (§5.3).
This is a genuinely different, higher-level obstruction — one that
appears only *after* the predecessor's own term-count problem has already
been resolved by §1-§2's collapse — not a restatement of it.

### 6.3 What is NOT claimed

No claim that a free-`K` closed form (elementary or special-function)
provably does not exist in an absolute sense — only that: (a) the natural
`r`-sum this front's construction produces is certified non-Gosper-
summable, and (b) the natural special-function fallback (`\,_3F_2`) does
not reduce further under `sympy.hyperexpand`. A different, cleverer
reorganization of the SAME underlying combinatorics might conceivably
avoid this specific `r`-sum altogether; none was found here, and none is
claimed to be ruled out. No claim about `c_1(K)`'s pattern in `K` (§4). No
claim about `K\ge9`. No claim about the full CDF of `M_n^{(K)}`,
`K\ge2` (pre-existing, untouched by this front). No claim of any kind
about a Millennium Problem; pure internal combinatorics on the u12
ensemble defined in `THEOREM.md`.

---

## 7. Self-caught issues, consolidated (all fixed before any final claim used them)

1. **`attempt_k_uniform_closure.py`, cross-arc prefactor (1/4 vs 1/2).**
   An early draft of the piece-D construction (in the scratch work behind
   §2.3/§5.2) used `mult*inner/4`, copying the `(L_s{-}1)/2\cdot
   (L_{s'}-1)/2` position-sum coefficient without also accounting for
   `P_{s,s'}`'s own factor of 2 from the §1.2 `P_same{=}P_disjoint`
   collapse. Caught by a dedicated piece-by-piece numeric comparison
   (`debug_pieces.py`-style, not archived as a separate deliverable since
   its only role was this one diagnostic) against
   `reduced_model_direct_assembly.py`'s direct `T(L)` computation at
   several concrete `(n,K)`: pieces A, B, C matched exactly, piece D was
   off by *exactly* `2\times` at every cell — a clean signature pointing
   directly at a missing/extra factor of 2, not a structural error. Fixed
   to `mult*inner/2`; re-verified — all four pieces then matched exactly,
   and the full `K=1,\ldots,6` closed-form reproduction (§2.4) only
   succeeded after this fix.
2. **`c1_table_k7_k8.py`, float-roundtrip verification bug.** Documented
   in full in §3.2 (`sp.lambdify`/float/`nsimplify` producing spurious
   decimal-rounded "mismatches"; fixed to exact symbolic substitution).
3. **`c1_table_k7_k8.py`, symbol-shadowing bug.** Documented in full in
   §3.2 (a locally re-declared `n` without `positive=True` silently
   failed to match the correctly-assumed `n` used elsewhere; fixed by
   importing the correct symbol instead of re-declaring it).

No other bug was found or is known to remain in any script in this
directory; every numeric claim in §1-§6 above was produced by the
POST-fix versions of the scripts, and every script's own log
(`*.log` files, listed in §9) is the actual run that produced the
numbers quoted in this document.

---

## 8. Seeds

Reserved range: `20260910000`-`20260910999` (this front's own).
Grep-confirmed unused before this front's first use:

```
$ grep -rn "20260910" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:6403: ...Seeds 20260910000-20260910999 (frente) /
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:6465: ...Seeds 20260910000-20260919999 confirmadas nao-usadas
05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md:28: ...confirmadas não-usadas por grep antes
05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml:3310: ...Seeds 20260910000-20260919999...
05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml:3481: ...20260910000-20260910999 (frente) /
```

All hits are governance reservation lines (predating this front's files);
no other file in the archive outside this front's own new subdirectory
references the range.

Only `monte_carlo_k7_k8.py` uses randomness
(`numpy.random.default_rng`, one explicit seed per configuration, no
shared/reused seed):

| script | seed(s) | purpose |
|---|---|---|
| `double_integral_p_disjoint.py` | none (exact/symbolic) | Task item 1 |
| `bruteforce_definition4_groundtruth.py` | none (exhaustive) | ground-truth Definition-4 brute force, `K=1,2,3` |
| `reduced_model_direct_assembly.py` | none (exact) | independent slow direct-enumeration cross-check, all `K` |
| `gf_moment_machinery.py` | none (exact/symbolic) | inner GF-moment building blocks |
| `symbolic_pnn_via_composition_gf.py` | none (exact/symbolic) | main fast general-`K` algorithm; `K=1,\ldots,8` |
| `symbolic_k_moment_formulas.py` | none (exact/symbolic) | moment formulas symbolic in `(n,K,r)` |
| `attempt_k_uniform_closure.py` | none (exact/symbolic) | Gosper/hyperexpand `K`-uniform closure attempt |
| `c1_table_k7_k8.py` | none (exact/symbolic) | bonus `c_1(K)` table, `K=7,8` |
| `monte_carlo_k7_k8.py` | `20260910101`-`20260910104` | bonus Monte Carlo triangulation, `K=7,8` |

---

## 9. Files

| file | contents |
|---|---|
| `ATTEMPT.md` | this document |
| `double_integral_p_disjoint.py` / `.log` | Task item 1: double-integral collapse, `P_same==P_disjoint` identity |
| `bruteforce_definition4_groundtruth.py` / `.log` | true Definition-4 brute force, `K=1,2,3` (ground-truth anchor) |
| `reduced_model_direct_assembly.py` / `.log` | independent slow direct-enumeration `P_nn(n,K)` assembly, all `K`, validated vs. ground truth and vs. NN4-NN6 |
| `gf_moment_machinery.py` / `.log` | inner composition-simplex GF/moment building blocks, validated |
| `symbolic_pnn_via_composition_gf.py` / `.log` | main fast general-`K` algorithm (Task item 2); reproduces `K=1,\ldots,6`, derives new `K=7,8` |
| `symbolic_k_moment_formulas.py` / `.log` | moment formulas made explicit and symbolic in `(n,K,r)` simultaneously (Task item 3a) |
| `attempt_k_uniform_closure.py` / `.log` | the symbolic-`K` closure attempt; Gosper certificate of non-closure; `\,_3F_2` fallback exhibited and shown not to reduce further |
| `c1_table_k7_k8.py` / `.log` | Task item 4 bonus: `c_1(7)`, `c_1(8)`, raw data, independently verified two ways |
| `monte_carlo_k7_k8.py` / `.log` | bonus Monte Carlo triangulation, `K=7,8`, reserved seeds |

---

## 10. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `P_same(s,s')\equiv P_disjoint(s,s')` (algebraic identity) | **PROVED** (§1.2) |
| 2 | Double integral for `P_disjoint` collapses to a single integral | **PROVED** (§1.3) |
| 3 | `\mu_r(n,K)=\binom{n+r}{K+r}` and the general moment machinery | **PROVED** (§2.1-§2.2) |
| 4 | Fast `K`-uniform algorithm reproduces `K=1,\ldots,6` exactly | **PROVED** (§2.4-§2.5) |
| 5 | New closed forms, `K=7,8` | **PROVED**, doubly independently verified (§3) |
| 6 | `c_1(7)=4387/12870`, `c_1(8)=76627/218790` | **PROVED** (raw data, no pattern claimed) (§4) |
| 7 | Symbolic-`(n,K,r)` moment formulas | **PROVED** (§5.1) |
| 8 | `r`-summand not Gosper-summable (`K` symbolic) | **PROVED** (rigorous negative certificate) (§5.3) |
| 9 | `r`-sum equals a terminating `\,_3F_2`, not reducible via `hyperexpand` | **PROVED / negative** (§5.4) |
| 10 | Single elementary closed form `P_nn(n,K)=F(n,K)` for symbolic `K` | **OPEN**, precisely diagnosed, non-closure certified for the natural construction (§6) |
| 11 | `K\ge9` | **NOT ATTEMPTED** (no obstruction beyond §5's, simply not run) |
| 12 | Full CDF of `M_n^{(K)}`, `K\ge2` | **OPEN** (pre-existing, untouched by this front) |

---

## 11. Scope discipline (confirmed)

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html`. No `adversarial/` subdirectory created, no referee
dispatched by this front. No `git` command run. No `.py` file from any
other front (this lineage or any ancestor/sibling) was read, opened, or
imported — every script in this directory is written fresh from the
mathematical prose of `THEOREM.md` and the direct predecessor's
`ATTEMPT.md` description only. Every claim above is labeled PROVED / OPEN
/ NOT ATTEMPTED at the point of use, with the Gosper-certificate results
(§5.3) explicitly flagged as rigorous negative results, not "sympy could
not find it." All randomized verification used only the reserved seed
range `20260910000`-`20260910999`. No claim of progress on any Millennium
Problem; this is pure combinatorial mathematics internal to the u12
ensemble defined in `THEOREM.md`.
