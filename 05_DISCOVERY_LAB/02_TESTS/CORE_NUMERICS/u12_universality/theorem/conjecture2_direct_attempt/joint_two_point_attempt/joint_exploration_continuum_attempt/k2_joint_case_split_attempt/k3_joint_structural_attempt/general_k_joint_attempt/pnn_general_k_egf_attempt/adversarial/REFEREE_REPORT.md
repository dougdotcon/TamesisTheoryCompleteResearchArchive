# Adversarial referee report: `PNN-GENERAL-K-EGF-ATTEMPT`

**Target document:** `.../general_k_joint_attempt/pnn_general_k_egf_attempt/ATTEMPT.md`
(wave 22 front (a), `DISC-DEC-096`).

**Referee discipline followed:** every check below was built completely
fresh, from the mathematical prose of `THEOREM.md` (Estágio 18, 25, 27,
28, 31, 35, read in full) and the direct predecessor's `ATTEMPT.md`
(`general_k_joint_attempt`, read in full — §4, §5, §6, §8 especially), and
from the TARGET document's own prose. **No `.py` file was opened, read, or
imported from the target front or from any front in its lineage**
(`general_k_joint_attempt`, `k3_joint_structural_attempt`,
`k2_joint_case_split_attempt`, `joint_exploration_continuum_attempt`,
`joint_two_point_attempt`, `conjecture2_direct_attempt`, or any other
ancestor). Every script in this directory is my own from-scratch
implementation, with its own variable names and structure. `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
`PROOF_DEPENDENCY_MAP.md`, `README.md`, `index.html` were not touched; no
`git` command was run. No randomness was needed anywhere in this review
(every check is exact/symbolic/exhaustive), so the reserved referee seed
range `20260911000`-`20260911999` (grep-confirmed unused before this
front's own use, and still unused after this review — only the governance
reservation lines in `DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` mention it)
was not needed.

Per the mandate, the two claims already independently verified by the
orchestrating session before dispatch — (a) the `P_same ≡ P_disjoint`
identity, (b) `mu_r(n,K) = C(n+r,K+r)` — were **not** re-verified from
scratch as the primary focus, though (b) is in fact re-derived here anyway,
by a structurally different method (Eulerian-polynomial OGF route,
`02_moment_formula_independent.py`), fully symbolically in `(n,K,r)`
simultaneously, as a byproduct of building the machinery needed for the
higher-priority checks — and it matches exactly. Effort was concentrated,
as instructed, on the K=7/K=8 closed forms, the Piece B/C/D decomposition
and its symbolic-`(n,K,r)` generalization, and especially the Gosper
certificate (§5.3), the front's headline claim.

---

## VERDICT: **SOUND WITH NAMED ISSUES (two, both LOW severity, both
cosmetic)**

Every mathematical claim I attempted to independently re-verify —
including the front's most novel and most consequential claim, the
Gosper-certified non-closure result (§5.3) — checks out exactly. The two
issues found are a type-label slip (the §5.4 fallback is called "₃F₂" but
is, by direct parameter count and by `sympy`'s own object classification,
a ₃F₁) and a one-digit rounding slip in a decimal display column (§4's
table). Neither affects the substance, correctness, or honesty of any
PROVED claim in the document.

---

## What I independently re-verified, and how

### 1. K=7 and K=8 closed forms (target §3) — CONFIRMED, 5/5 exact matches, via a fully independent code path

`01_reduced_model_independent.py` builds the "reduced model" `T(L)`
composition-sum route to `P_nn(n,K)` completely from scratch: it
implements Lemma 5's PROVED `P0(s)`, `P_same(s,s')`, `P_disjoint(s,s')`
formulas (cited from `THEOREM.md` Estágio 35 / the predecessor's §4)
literally — including a genuine, un-collapsed `3^{|M|}`-term brute
enumeration of `P_disjoint`'s double subset sum, **deliberately not using
the target's own `P_same ≡ P_disjoint` bonus identity (claim 1)** so that
this check is independent of that identity too — and assembles `T(L)` by
literally looping over every ordered pair of the `n-K` non-source "roles"
(exactly the predecessor's own §5.1 description of `T(L)`, not the
target's own algebraic Piece-A/B/C/D collapse).

- **Self-consistency floor:** reproduces, exactly, the already-PROVED
  closed forms at `K=1,…,6` (`Estágio 27`/Proposition NN2/NN3, and the
  predecessor's own true-brute-force-anchored NN4/NN5/NN6), 16/16 exact
  `Fraction` matches, 0.35s total.
- **K=7, K=8 (the new claims):** exact match against the target's own
  quoted closed forms at **5 concrete `n` values**: `K=7,n=9,11,13` and
  `K=8,n=10,12` — every one an exact rational equality, no floating
  point anywhere. (`K=7,n=13` and `K=8,n=12` are the two largest of the
  target's own reference points; both confirmed.)

`03_piece_bcd_independent.py` then independently re-derives the SAME
`P_nn(n,K)` values for `K=7,8` a **second, structurally unrelated way** —
via the Piece A/B/C/D moment-machinery route (see item 2 below) — and gets
`diff == 0` symbolically against the target's polynomials for both `K=7`
and `K=8`. Two independent code paths inside this review, built by two
different methods, both agree with the target's claims.

### 2. Piece A/B/C/D decomposition (target §2.3) — CONFIRMED exactly, symbol for symbol

`03_piece_bcd_independent.py` re-derives, purely by hand from Lemma 5's
`P0(s)`/`P_pair(s,s')` formulas plus elementary position-sum combinatorics
(`Σi`, and `Σ_{i≠i'} min(i,i')` over `{1,…,m}`, both derived from scratch
in the file's own docstring, not copied from anywhere), the Piece
B/outside-arc, Piece C/same-arc, and Piece D/cross-arc formulas. The
resulting expressions match the target's own §2.3 formulas **exactly**
(same binomial coefficients, same `r!`/`(r+1)!` factors, same `1/n^{r+1}`,
`1/n^{r+2}` powers, same external multiplicities `K`, `K/3`, `K(K-1)/2`).
Total `P_nn(n,K)` assembled this way reproduces Proposition NN3 (`K=3`)
and NN4 (`K=4`) exactly (`diff == 0`, symbolic), and — as noted above —
also reproduces the new `K=7,8` closed forms exactly.

### 3. Symbolic-`(n,K,r)` moment formula (target §5.1) — CONFIRMED, 372/372 brute-force matches plus a full symbolic re-derivation

`02_moment_formula_independent.py` builds the moment machinery from
scratch via the Eulerian-polynomial/OGF approach described in prose
(repeated application of the operator `t·d/dt` to `t/(1−t)`, exactly as
both the predecessor's §8.4 and the target's §5.1 describe it): derives
`A_a(t) = t·E_a(t)/(1−t)^{a+1}` for the needed powers, and extracts
`[t^n]` of the resulting generating function as an explicit binomial
coefficient with linear-in-`(n,K,r)` arguments — genuinely symbolic in `K`
**and** `r` simultaneously, not `K`-by-`K`.

- Checked against **372** concrete `(specials, r, b, K, n)` configurations
  (one- and two-special-index cases, `a∈{1,2,3}`, `b∈{0,1,2}`,
  `K=4,…,7`) by direct brute-force composition-simplex enumeration:
  **372/372 exact integer matches**.
- Re-derives `μ_r(n,K) = C(n+r,K+r)` with `n, K, r` **all left as free
  sympy symbols** (not substituted until after the derivation): the
  formula collapses to `binomial(n+r, K+r)` identically, `diff == 0`. This
  independently reconfirms, by a structurally different method, what the
  orchestrator's own composition-simplex-enumeration spot-check already
  established.

`04_symbolic_summand_gamma_form.py` uses this machinery to build the
Piece B/C and Piece D **r-summands** fully symbolically in `(n,K,r)`, then
compares them directly against the target's own quoted Gamma-function
formulas (§5.2), copied verbatim from the prose. One bookkeeping subtlety
had to be resolved by trial: the target's §2.3 groups each piece's
coefficient as an *external multiplicity* (plain `K` for Piece B, `K/3`
for Piece C, `K(K-1)/2` for Piece D); its §5.2 "summand(r)" turns out to
mean the per-`r` term with only the *integer* part of that multiplicity
(`K`, or `K(K-1)`) stripped out — the fractional part (`1/3`, `1/2`) stays
inside the summand. Once resolved this way (documented in the script), the
match is exact:

- `sympy.simplify` and `sympy.gammasimp` both give **literal `0`** for
  `(my Piece B summand) − (target's quoted formula)`, same for Piece C and
  Piece D, fully symbolically in `(n,K,r)`.
- **135/135** concrete numeric `(K,r,n)` substitutions (`K=3,…,8`) also
  match exactly.
- The secondary curiosity (target's claim 5, §3.4/§5.2: Piece B's summand
  ≡ Piece C's summand, term-by-term in `r`) is independently reconfirmed:
  my own from-scratch derivations of the two summands are symbolically
  identical (`diff == 0`), not merely numerically close.

### 4. The Gosper certificate (target §5.3) — the headline claim — CONFIRMED, and independently stress-tested well beyond what the target itself reports

This was treated as the most important check, per the mandate's own
emphasis. `05_gosper_certificate_independent.py`:

1. **Term ratios.** Computed `T(r+1)/T(r)` directly from my own
   independently-derived (and, per item 3 above, already-confirmed
   identical to the target's) Piece B/C and Piece D summands. Both
   simplify to rational functions of `r` (confirmed via
   `is_rational_function(r)`), and match the target's own quoted ratios
   exactly (`diff == 0`).

2. **What would a `None` actually mean here?** I read `sympy`'s own
   installed `sympy/concrete/gosper.py` source directly (not a front's
   code — the library's own source). It shows `gosper_term`/`gosper_sum`
   can return `None` for **two structurally different reasons**: (a)
   `hypersimp(f, n)` returns `None`, meaning `f` is not even recognized
   as a hypergeometric term at all (term ratio not rational) — a strictly
   *weaker* failure mode that would **not** license "rigorous certificate"
   language; or (b) `hypersimp` succeeds, but no polynomial solution of
   the algorithm's own completely-computed degree bound exists — the
   in-source comment literally reads `"'f(n)' is *not* Gosper-summable"`.
   Branch (b) is the genuine content of Gosper's theorem
   (Petkovšek–Wilf–Zeilberger, *A=B*, cited in `sympy`'s own docstring):
   given a confirmed hypergeometric term, Gosper's algorithm is a
   **complete decision procedure** for whether a hypergeometric-term
   antidifference exists — not a heuristic, not "gave up". I ran
   `hypersimp` on both summands directly (K, n symbolic): **both are
   recognized as genuine hypergeometric terms**, ruling out branch (a).
   Any subsequent `None` is therefore, by the algorithm's own proven
   completeness, branch (b) — a genuine non-existence result.
3. **Ran `gosper_term`/`gosper_sum` myself**, K symbolic, on my own
   summand formulas: **`None`** for both Piece B/C and Piece D, in well
   under a second each — matching the target's own reported result (and
   my own independently-derived formulas, not theirs, are what was fed
   in).
4. **Triangulation**, not done by the target: ran `gosper_sum` at **13
   concrete integer `K` values (`K=3,…,15`)**, `n` left symbolic, `r`
   bound `0..K-1`/`0..K-2` — **`None` at every single one**, for both
   pieces. If the symbolic-`K` `None` were an artifact of `sympy`
   mishandling a symbolic *parameter* (as opposed to a genuine fact about
   the summation), we would expect at least some concrete `K` to succeed;
   none did.
5. **Positive controls**, also not done by the target: confirmed this
   exact harness genuinely detects summability when it is present — a
   plain polynomial (`Σ(r+1) = K(K+1)/2`), a telescoping term
   (`Σ1/((r+1)(r+2)) = K/(K+1)`), and `sympy`'s own `gosper.py` docstring
   example with a Gamma/factorial-heavy summand and a **symbolic** bound
   variable (structurally the same setup as our `K`-symbolic runs) all
   correctly return closed forms. This rules out a trivially-broken
   harness that just always returns `None`.
6. **The ₃F₂/hyperexpand fallback (§5.4).** Verified the exact closed-form
   VALUE of `Σ_{r=0}^{K-1} T(r)` against the target's quoted
   hypergeometric parameter list at 4 concrete `(K,n)` pairs — exact match
   to 20+ significant figures every time. Ran `sympy.hyperexpand` on the
   symbolic-`(K,n)` version myself: it still contains an unevaluated
   `hyper(...)` term, confirming the target's claim that it does not
   reduce further.

**Conclusion on §5.3/§5.4:** the front's characterization — "Gosper's
algorithm returning `None` … is Gosper's algorithm PROVING no
hypergeometric-term closed form for the indefinite sum exists — not a
timeout, not 'sympy could not find one'" — is **accurate**, and is now
backed by more independent evidence than the target itself presents
(the `hypersimp` branch check, the 13-point concrete-`K` triangulation,
and the positive controls are all new checks added by this review, not
reproductions of anything in the target document). The front's own §6.3
hedge ("no claim that a free-`K` closed form provably does not exist in an
absolute sense … a different, cleverer reorganization … might conceivably
avoid this specific `r`-sum … none is claimed to be ruled out") is exactly
the right level of caution for what Gosper's algorithm can and cannot
establish, and I found nothing in it that overclaims.

### 5. Millennium Prize Problem discipline

Confirmed absent throughout: the front matter, §0, and §11 all carry the
standard disclaimer, and no claim of progress toward any Millennium
Problem appears anywhere in the document. This is pure internal
combinatorics on the u12 ensemble.

### 6. General arithmetic spot-checks (§3, §4)

`06_arithmetic_spotchecks.py`: `c_0(K) = 1/(K+1)` confirmed exactly for
`K=7,8` by reading it off the quoted polynomials' leading coefficients;
`c_1(K)` (the `1/n` coefficient) confirmed to match the quoted `4387/12870`
and `76627/218790` exactly; all 8 decimal values in the §4 table confirmed
to 5 decimal places; 7 of 8 "ratio to `K−1`" column entries confirmed
exactly — see Named Issues below for the one that is not.

---

## Named issues

**Issue 1 (LOW, cosmetic/notational — §5.4).** The target labels the
terminating hypergeometric fallback "`₃F₂(1−K, n+2, 1; K+4; −1/n)`". The
parameter list as literally printed has **3 upper parameters and only 1
lower parameter** (`K+4`) — by direct count, and confirmed by `sympy`'s
own object classification (`hyper([...],[...])` reports `len(ap)=3,
len(bq)=1`) and its own LaTeX rendering (`{}_{3}F_{1}`, not `{}_3F_2`),
this is a **₃F₁**, not a ₃F₂. A genuine ₃F₂ needs a second lower
parameter, which is not present in what is printed. This does **not**
affect the correctness of the formula's *value* — independently confirmed
exact at 4 concrete `(K,n)` points, matching to 20+ significant figures —
nor does it affect the (independently reconfirmed) claim that
`hyperexpand` fails to reduce it further; it is a type-label slip only.
Likely explanation: an extra "1" parameter is a standard device for
absorbing/cancelling the implicit `1/r!` built into the generic `pFq`
series definition when the natural term ratio has no explicit `(r+1)`
factor of its own (exactly the situation here) — but this changes only
the parameter *count* on the "1" side, not automatically both the numerator
and denominator, so the "F2" half of the label does not follow from that
device and appears to be a simple mislabel.

**Issue 2 (LOW, cosmetic — §4 table).** The "ratio to `K−1`" column for
`K=7` is printed as `1.035`. The exact value,
`c_1(7)/c_1(6) = (4387/12870)/(1979/6006) = 30709/29685 = 1.0344955...`,
rounds to `1.034`, not `1.035` — a one-digit-in-the-last-place rounding
slip. All 7 other entries in that column (`K=2,…,6,8`) are exact. The
underlying exact fraction `c_1(7) = 4387/12870` itself is correct
(independently confirmed above); only this one derived, rounded display
value is off by `0.001`.

Neither issue touches any PROVED claim, the Gosper certificate, the K=7/K=8
closed forms, or the Piece B/C/D decomposition.

---

## What was not (and did not need to be) re-verified here

Per the mandate, the `P_same ≡ P_disjoint` identity (claim 1) and
`μ_r(n,K) = C(n+r,K+r)` (part of claim 2/7) had already been independently
verified by the orchestrating session before dispatch; this review's
`02_moment_formula_independent.py` reconfirms the latter anyway, by a
different method, as a natural byproduct. The double-integral collapse of
§1.3 (an elementary calculus consequence of claim 1, `k! = ∫λ^k e^{-λ}dλ`)
was not separately re-derived — it follows immediately from the
already-twice-verified claim 1, and was not flagged as a priority item in
the mandate. The front's own internal performance/timing claims (e.g. "0.3s
vs 166s") were not re-timed, since doing so would require reading the
front's own `.py` files, which is barred by the hard constraint; these
claims do not affect mathematical correctness in any case.

---

## Files in this directory

| file | what it independently checks |
|---|---|
| `01_reduced_model_independent.py` / `.log` | from-scratch `T(L)` reduced-model enumeration (raw, un-collapsed Lemma 5 formulas); self-consistency at K=1–6; K=7/K=8 exact match at 5 concrete `n` |
| `02_moment_formula_independent.py` / `.log` | Eulerian-polynomial/OGF moment machinery, symbolic in `(n,K,r)`; 372 brute-force cross-checks; symbolic re-derivation of `μ_r(n,K)=C(n+r,K+r)` |
| `03_piece_bcd_independent.py` / `.log` | Piece A/B/C/D re-derived from first principles; matches NN3/NN4 and (second, independent code path) the new K=7/K=8 closed forms |
| `04_symbolic_summand_gamma_form.py` / `.log` | symbolic Piece B/C/D r-summands in Gamma-function form; exact match (symbolic + 135 numeric points) to target's §5.2 formulas; B≡C re-confirmed |
| `05_gosper_certificate_independent.py` / `.log` | the headline check: term ratios, `hypersimp` branch determination, `gosper_term`/`gosper_sum` (K symbolic + 13 concrete K), positive controls, ₃F₂/hyperexpand fallback verification and the 3F1-vs-3F2 finding |
| `06_arithmetic_spotchecks.py` / `.log` | `c_0`, `c_1` and the §4 table's decimal/ratio arithmetic |
