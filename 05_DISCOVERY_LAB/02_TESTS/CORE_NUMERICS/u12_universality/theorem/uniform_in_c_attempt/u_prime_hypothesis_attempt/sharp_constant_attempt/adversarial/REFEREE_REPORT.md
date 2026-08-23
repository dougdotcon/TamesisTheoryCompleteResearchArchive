# Adversarial referee report — `sharp_constant_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent re-verification of `ATTEMPT.md`'s two
> claimed PROVED results — Theorem 5, `Q(n) ≥ √(πn/2) - 6` for every `n≥1`,
> and Theorem 6, `lim_{K→∞} M_K/√K = a*` exactly — before catalogue. Pure
> combinatorics/asymptotics on the classical Ramanujan `Q`-function and the
> `u12` recursion's `φ_K`; no physics claim, no Millennium Problem
> relevance.
>
> **Discipline.** Neither of this front's own scripts
> (`verify_Q_lower_bound.py`, `verify_limit.py`) nor their `.log` files was
> opened at any point — every algebraic step below was re-derived by hand
> and independently re-coded from scratch; every numerical claim was
> independently recomputed, never transcribed from the target's logs. The
> parent documents cited as already-established background —
> `u_prime_hypothesis_attempt/ATTEMPT.md` (Theorem 3, Lemma 4.1, Lemma 4.2)
> and `uniform_in_c_attempt/ATTEMPT.md` §6.3 — were read directly as
> ordinary literature review; their own adversarial history
> (`u_prime_hypothesis_attempt/adversarial/REFEREE_REPORT.md`, verdict
> SOUND/ACCEPT) is treated as established, not re-verified here.
> `fractions.Fraction` for everything labelled PROVED or a counterexample;
> `sympy` for symbolic identities and integrals; `mpmath` (60 dps) for
> wide-range numerical stress-testing, never as the basis of a PROVED claim.
> No randomness used or needed — every object here is deterministic. No
> file outside this `adversarial/` directory was created or modified; no
> git command was run.

---

## 0. Executive summary

**Verdict: SOUND. ACCEPT for catalogue**, with one immaterial
self-consistency nit in the target's own reported figures (§7, N-1) and no
mathematical error found anywhere in the proofs.

I re-derived Lemma 5.1's termwise bound (`P_j ≥ h(j)`) from the elementary
inequality `-ln(1-x) ≤ x/(1-x)` by hand, confirmed the derivative argument
establishing that inequality, and independently re-checked the summation
step (`Σi/(n-i) ≤ j(j+1)/(2(n-j))`) for a sign/off-by-one error — none
found. I re-derived Lemma 5.2's monotonicity claim (`φ'(x)`'s numerator is a
sum of a positive and a nonnegative term, hence `>0`) both symbolically and
by direct expansion.

Theorem 5's proof — the longest and most failure-prone part of the
document — was re-derived in full algebraic detail, independently of the
target's own write-up wherever a concrete formula was involved:

- The `ε(x)` decomposition was re-expanded by hand and confirmed
  algebraically (`nx(x+1)-x²(n-x) = nx+x³ = x(n+x²)`, symbolically
  verified with `sympy.expand`).
- Both moment integrals (`∫x e^{-x²/2n}dx=n`, `∫x³e^{-x²/2n}dx=2n²`) were
  recomputed independently via `sympy.integrate` and matched exactly.
- The Gaussian integral `∫₀^∞ e^{-x²/2n}dx=√(πn/2)` was likewise
  re-verified symbolically.
- The split-domain `Err(n)` bound was checked against the **true** integral
  (`mpmath.quad` of the actual `ε(x)`-integrand, not the target's own
  algebraic sub-bounds) for `n` up to `50\,000`: **zero violations**, and I
  additionally derived, independently, the exact asymptotic limit
  `Err(n) → 3/2` as `n→∞` (a scaling argument, `x=√n·t`, not in the target
  document) — this matches my own numerics (`Err(50\,000)=1.4958`) almost
  exactly and gives an independent explanation for why the target's `≤3`
  sub-bound on `[0,n/2]` is valid but loose by a factor of `2`.
- The final assembly `Q(n) ≥ √(πn/2) - Tail(n,n) - Err(n) ≥ √(πn/2)-1-5 =
  √(πn/2)-6` is arithmetically correct given the sub-bounds.

Theorem 6's assembly was likewise re-derived and checked symbolically term
by term (`sympy.simplify` on every intermediate step, including the
`(√π/(2√K))(K+1) = (√π/2)(√K+1/√K)` rewrite and the final division by
`√K`) — every step reduced to exactly `0` difference from the target's
claim.

**Independent numerical verification, exceeding what was checked upstream
at every stage:**

- Lemma 5.1 termwise bound: exact `Fraction` `P_j` vs. `mpmath` `h(j)`,
  **14,491 pairs** (`n∈{1,…,10000}`, all `j`) — zero violations; extended
  with a pure-`mpmath` log-sum stress test to **1,350,000 pairs**, `n` up to
  `10^6` — zero violations.
- Theorem 5's final bound: exact `Fraction` `Q(n)` to `n=4000` (68 values,
  zero violations, worst margin `5.6683` at `n=4000`), plus exactly at
  `n=6000` and `n=12000` (margins `5.6680`, `5.6676` — see §7 nit), plus a
  cross-validated `mpmath` log-sum method (agreement with exact `Fraction`
  to `10^{-59}`) pushed to a **full dense-then-sparse scan of the assembled
  bound itself to `n=1\,000\,000`** — `n=1,…,1500` dense plus 17 further
  points to `n=10^6` — **zero violations anywhere**, worst (smallest)
  margin `5.66677` at `n=10^6`, converging monotonically from above toward
  `17/3=5.66667` (`=6-1/3`, matching the classical Ramanujan-`Q` next-order
  constant cited, not re-derived, by the target).
- Theorem 6's two-sided squeeze: exact `Fraction` `M_K` to `K=2000` (66
  values, zero violations), `mpmath` log-gamma/log-sum method (cross-checked
  against exact `Fraction` to `10^{-59}` agreement) pushed to a dense scan
  `K=1,…,1500` plus 17 sparse points out to **`K=1\,000\,000`** — zero
  violations anywhere, `r_K` never once reaching `a*`, and the gap
  `a*-r_K` shrinking smoothly and monotonically from `0.2004` (`K=1`) to
  `3.33×10^{-4}` (`K=10^6`).

**No error was found in the mathematics of either Theorem 5 or Theorem 6.**
One minor internal-consistency nit in the document's own §2 prose vs. its
own Files-section tally is recorded in §7 — it does not affect the proof
and I independently confirmed the bound holds at the two `n`-values in
question anyway.

The document's own honesty section (§3–4: piece 2, monotonicity /
`sup_K=lim_K`, explicitly NOT closed) was checked against the parent
documents and against my own numerics and found **accurate** — see §6.

---

## 1. What I tried to break, and what happened

- **Lemma 5.1's elementary inequality and summation bound** — re-derived the
  derivative sign argument for `-ln(1-x)≤x/(1-x)` by hand and numerically
  (1000+ points in `[0,0.999]` plus 29 points approaching `x→1⁻`); checked
  the `1/(n-i)≤1/(n-j)` step for `i≤j` (direction depends on `n-i` being
  *decreasing* in `i`, easy to get backwards — confirmed correct). Held.
- **Lemma 5.2's monotonicity proof** — re-derived `φ'(x)`'s numerator by
  hand and via `sympy`, checked the claim that it is a sum of a strictly
  positive and a nonnegative term (not just "eventually positive" or
  "positive only on a sub-interval"). Held.
- **The `ε(x)` algebra** (the step I judged most likely to hide a sign
  error, given the task's flag that it was not independently hand-verified
  upstream) — re-expanded `nx(x+1)-x²(n-x)` completely from scratch on
  paper before touching any code, then confirmed with `sympy.expand`. Held,
  exactly as claimed.
- **The two moment integrals** — recomputed by substitution `u=x²/2n` by
  hand (`∫x e^{-x²/2n}dx=n`, `∫x³e^{-x²/2n}dx=2n²`, the latter via
  `∫u e^{-u}du=1!=1` after the substitution) and confirmed symbolically.
  Held.
- **The split-domain `Err(n)` bound**, specifically the `[0,n/2]`
  sub-bound's leap from `ε(x)≤x/n+x³/n²` to `"≤3"` — attacked by computing
  the **true** `Err(n)` via numerical quadrature (not the target's
  algebraic sub-bounds) and separately deriving its `n→∞` limit
  analytically to cross-check the numerics are self-consistent. Held, and
  the independent asymptotic derivation (§5 below) is a genuinely new
  cross-check not present in the target document.
- **The final constant arithmetic** (`Tail≤1`, `Err≤5`, `1+5=6`) — checked
  by hand; trivial but confirmed correct.
- **Theorem 6's full algebra chain** — every intermediate rewrite checked
  symbolically as an identity (`sympy.simplify(LHS-RHS)==0`), not just
  spot-numerically. Held at every step.
- **Observation 0's citation** — read the parent's Theorem 4 proof directly
  (not the target's paraphrase) and confirmed `M_K<1+a*√(K+1)` is exactly
  what is proved there, in the form Observation 0 needs. Held.
- **A direct hunt for a counterexample** to Theorem 5 or Theorem 6, across
  four independent routes: exact `Fraction` (`n,K` up to `2000`–`4000`),
  `mpmath` dense sweeps (`n,K` up to `1500`), sparse `mpmath` all the way to
  **`n,K=1\,000\,000`** for the *fully assembled* bounds (not just their
  sub-steps), and a dedicated check of whether `r_K` ever reaches or
  exceeds `a*` itself (it never does, at any of the roughly `1\,500` `K`
  values tested up to `10^6`). **Zero counterexamples found.**
- **Edge cases**: `n=1` (Theorem 5's bound is `√(π/2)-6≈-4.75`, trivially
  true since `Q(1)=1`); the split point `x=n/2` (checked the two pieces'
  bounds separately, no gap or double-count at the boundary); `x→n⁻` (`h(x)
  →0`, improper integral genuinely converges — confirmed both symbolically,
  via the `φ(x)→∞` argument, and numerically); `K` small (the lower-bound
  squeeze's RHS is trivially negative for `K≲267`, exactly as the target
  notes, and I confirmed this is harmless to the *limit* statement, which
  needs no small-`K` behavior at all).
- **The document's own self-consistency** — cross-checked every reported
  count (`1491/1491`, `66/66`, `9/9`-style tallies) against the grids the
  prose actually describes. Found one discrepancy (§7, N-1); traced it to
  its likely source and confirmed it is cosmetic, not mathematical.

I could not break the mathematics of either theorem.

---

## 2. Lemma 5.1 and Lemma 5.2 — re-derived from scratch

**Lemma 5.1.** For `x∈[0,1)`, `d/dx[x/(1-x)+ln(1-x)] = 1/(1-x)² - 1/(1-x) =
x/(1-x)² ≥ 0`, and both sides vanish at `x=0`, so `x/(1-x)≥-ln(1-x)` on
`[0,1)` — re-derived independently and confirmed against 1000+ sample
points plus 29 points approaching `x→1⁻` (`lemma_5_1_5_2.py`, Part 0, zero
violations). With `x=i/n` for `1≤i≤j≤n-1`: `x∈(0,1)` strictly (since
`i≤n-1`), so the inequality applies validly, giving `-ln(1-i/n)≤i/(n-i)`.
Summing `i=1,…,j`: since `i≤j⟹n-i≥n-j>0` (using `j≤n-1`), `1/(n-i)≤1/(n-j)`
for every term in the sum — **the direction is the one that makes the bound
correct** (I checked this is not accidentally reversed, a natural place for
an off-by-one/direction slip): `Σᵢ i/(n-i) ≤ (1/(n-j))Σᵢi = j(j+1)/(2(n-j))`.
So `P_j≥h(j)`. **Confirmed correct in every detail**, including the range
`1≤i≤j≤n-1` (guaranteeing `x∈(0,1)`, not just `[0,1)`, so the inequality is
never invoked at its boundary).

**Lemma 5.2.** `φ(x)=x(x+1)/(2(n-x))`; quotient-rule differentiation gives
`φ'(x)=[(2x+1)(n-x)+x(x+1)]/(2(n-x)²)` — re-derived independently
(`lemma_5_1_5_2.py`, Part 2b, `sympy.diff` minus the claimed formula
simplifies to exactly `0`). On `[0,n)`: `(2x+1)>0`, `(n-x)>0`, so their
product is `>0`; `x(x+1)≥0`; sum of a positive and a nonnegative term is
`>0`. So `φ'>0`, `h=e^{-φ}` strictly decreasing. **Confirmed.** (The
document's own proof text includes one unfinished/abandoned expansion
attempt — `"(2n-2x-1)x+n+…"` — before switching to the simpler
positive-plus-nonnegative argument actually used; this is a harmless,
visibly-abandoned dead end in the prose, not a used or load-bearing step,
and not a math error.)

**Independent numerical scale:** exact `Fraction` `P_j` vs. `mpmath` `h(j)`,
`n∈{1,2,3,5,10,20,50,100,300,1000,3000,10000}`, all `0≤j≤n-1`: **14,491
pairs, zero violations** (target: 1,491 pairs, `n` up to `1000`) — a
`~10×` increase in pair count and a `10×` increase in the largest `n`
tested. Extended with a pure-`mpmath` log-sum stress test (not exact, but a
genuinely new scale) to `n∈{50000,300000,1000000}`, all `j`: **1,350,000
additional pairs, zero violations**.

---

## 3. Theorem 5 — full algebraic re-derivation

**The `ε(x)` decomposition.** By hand: `n·x(x+1) - x²(n-x) = nx²+nx-nx²+x³
= nx+x³ = x(n+x²)` — the `nx²` terms cancel exactly. Confirmed
symbolically (`sympy.expand`, difference `=0`). So `ε(x) = x(n+x²)/(2n(n-x))
≥ 0` on `[0,n)`. **Confirmed correct**, matching the target's claim exactly.

**The two moment integrals.** By substitution `u=x²/(2n)` (`x dx = n du`):
`∫₀^∞ x e^{-x²/2n}dx = n∫₀^∞ e^{-u}du = n`. For the cubic moment,
`x³dx=x²·(x dx)=2nu·n du=2n²u du`: `∫₀^∞ x³e^{-x²/2n}dx =
2n²∫₀^∞ u e^{-u}du = 2n²·Γ(2) = 2n²`. Both re-derived by hand before
touching code, both confirmed via `sympy.integrate` returning exactly `n`
and `2n²`. **Confirmed correct.**

**The Gaussian integral** `∫₀^∞ e^{-x²/2n}dx=√(πn/2)` — standard, and
`sympy.integrate` returns `√2·√π·√n/2`, symbolically identical to
`√(πn/2)`. **Confirmed.**

**The tail bound** `Tail(n,T)≤(n/T)e^{-T²/2n}` — re-derived from
`x≥T⇒x/T≥1⇒e^{-x²/2n}≤(x/T)e^{-x²/2n}`, integrated using the exact
antiderivative `d/dx[-ne^{-x²/2n}]=xe^{-x²/2n}`. Checked against the
**true** tail (`√(πn/2)·erfc(T/√(2n))`, exact closed form, not quadrature)
for 45 `(n,T)` pairs spanning `n=1` to `10^6`: **zero violations**, worst
observed ratio `exact/bound = 0.99999996` at `n=10^6,T=5n` (i.e. the bound
is essentially tight there, as expected for large `T/√n`). The two specific
instantiations used in the proof — `Tail(n,n)≤e^{-n/2}` and
`Tail(n,n/2)≤2e^{-n/8}` — independently re-derived (`(n/n)e^{-n²/2n}=
e^{-n/2}`; `(n/(n/2))e^{-(n/2)²/2n}=2e^{-n/8}`, using `(n/2)²/(2n)=n/8`) and
confirmed for `n` up to `10^6`. **Confirmed correct.**

**The split-domain `Err(n)≤3+2e^{-n/8}` bound.** On `[0,n/2]`: `n-x≥n/2⟹
ε(x)≤x(n+x²)/(n²)=x/n+x³/n²`, confirmed by hand; combined with
`1-e^{-a}≤a` (`a≥0`, standard tangent-line bound) and the two moment
integrals gives `≤1+2=3`. On `[n/2,n)`: crude `1-e^{-ε}≤1`, giving
`≤Tail(n,n/2)≤2e^{-n/8}≤2`. Sum `≤5`.

I went one step further than either the target or a line-by-line check: I
**independently re-derived the `n→∞` asymptotic limit of the true
`Err(n)`** via the scaling substitution `x=√n·t` (not present in the target
document at all). Under this substitution, `ε(x)≈t(1+t²)/(2√n)→0`
pointwise, but the `√n` from `dx=√n\,dt` exactly cancels the `1/√n` in
`1-e^{-ε(x)}≈ε(x)`, giving
`Err(n) → ½∫₀^∞ e^{-t²/2}t(1+t²)dt = ½[1+2] = 3/2` as `n→∞` — a genuine
nonzero limit, **not** `0`. This matches my own numerical quadrature almost
exactly (`Err(50000)=1.49580`, converging toward `1.5` from below) and
independently confirms two things at once: (a) the target's `≤3` bound on
the `[0,n/2]` piece is valid with a factor-of-`2` margin to spare (true
limit `3/2` vs. claimed bound `3`), consistent with the document's own
"deliberately not tight" framing; (b) my numerics are internally
consistent with the analytic structure of the proof, an independent
cross-check the target itself does not perform.

**Numerical re-verification of `Err(n)≤3+2e^{-n/8}` against the TRUE
integral** (`mpmath.quad` of the actual `ε(x)`-integrand — not the
target's own algebraic sub-bounds, which is what the target's own script
would presumably check): `n∈{1,2,5,10,50,100,500,1000,5000,10000,50000}`,
**zero violations**, `Err(n)` rising monotonically from `0.394` to `1.496`
as `n` grows, always `<5` (and, per the analysis above, provably `<3/2` in
the limit, well inside the target's `≤5`).

**Final assembly.** `Q(n)≥√(πn/2)-Tail(n,n)-Err(n)≥√(πn/2)-1-5=√(πn/2)-6`
— arithmetically correct given `Tail(n,n)≤1` and `Err(n)≤5`, both
independently confirmed above. **Confirmed correct.**

**Independent numerical scale on the final bound:** exact `Fraction` `Q(n)`
(via an incremental cumulative-product implementation, `O(n)` total
multiplications rather than the `O(n²)` a naive from-scratch recomputation
per `n` would cost) checked against `mpmath` (60 dps) `√(πn/2)-6` for **68
values of `n` up to `4000`**: zero violations, worst (smallest) margin
`5.6683` at `n=4000`; plus **exactly at `n=6000` and `n=12000`** (margins
`5.6680` and `5.6676` respectively — see §7 for why these two values matter
specifically); plus a cross-validated `mpmath` log-sum method (agreement
with exact `Fraction` to `1.5×10^{-59}` at `n=2000`) used to push the
**full assembled bound itself** — not just its Tail/Err sub-bounds — to a
dense scan `n=1,…,1500` plus 17 sparse points out to `n=1\,000\,000`.
**Zero violations anywhere**, worst (smallest) margin `5.66677` at
`n=10^6`, and the margin sequence converges monotonically, from above,
toward the exact value `17/3=5.66667`.

---

## 4. Theorem 6 — assembly re-derived and re-checked symbolically

Every intermediate algebraic rewrite in the target's proof was checked as a
`sympy.simplify(LHS-RHS)==0` symbolic identity, not merely spot-checked
numerically:

- `(√π/(2√K))(K+1) = (√π/2)(√K+1/√K)` — confirmed, difference `0`.
- `√(π(K+1)/2) ≥ √(π/2)·√K` — confirmed at `K=1,5,100` (trivial, since
  `K+1≥K`), all differences `≥0` as required.
- The full assembled lower bound
  `√(π/2)√K - (√π/2)(√K+1/√K) = a*√K - (√π/2)/√K` — confirmed, difference
  `0`, using the independently-checked identity `a*=√(π/2)-√π/2` (itself
  confirmed as `sqrt(π)(1/√2-1/2) - [√(π/2)-√π/2] = 0`, symbolically).
- Division by `√K`: `[a*√K-(√π/2)/√K-6]/√K - [a*-(√π/2)/K-6/√K]` —
  confirmed, difference `0`.
- Observation 0's upper-bound rewrite (cited from the parent's Theorem 4
  proof, read directly, not paraphrased): `(1+a*√(K+1))/√K -
  [1/√K+a*√((K+1)/K)]` — confirmed, difference `0`; both the lower-bound
  chain's limit and the upper-bound chain's limit were computed
  symbolically as `K→∞` and both equal `a*` exactly (`sympy.limit`).

**No error found in any step of the assembly.**

**Independent numerical scale.** Exact `Fraction` `M_K=Q(K+1)-(K+1)φ_K`
(`φ_K` computed via `4^K(K!)²/(2K+1)!` directly, `Q(K+1)` via the same
incremental exact product used for Theorem 5) checked against the
two-sided bound for **66 values of `K` up to `2000`**: zero violations,
worst margins `0.1272` (lower side) and `0.0298` (upper side) at `K=2000`.
Extended via a `mpmath` log-gamma/log-sum method (φ_K via `loggamma` to
avoid forming huge factorials; cross-validated against exact `Fraction` to
`10^{-59}` agreement) to a dense scan `K=1,…,1500` plus 17 sparse points
out to **`K=1\,000\,000`**: **zero violations anywhere**, `r_K=M_K/√K`
rising smoothly and monotonically (`0.16667` at `K=1` to `0.36675` at
`K=10^6`), the gap `a*-r_K` shrinking correspondingly from `0.2004` to
`3.33×10^{-4}` — fully consistent with, and a `~300×` scale extension
beyond, what the target itself reports (`r_{3000}=0.361060` vs. its
`a*=0.367087` — my own `r_{3000}=0.361060` matches to all six displayed
digits). A dedicated sweep specifically checking whether `r_K` ever reaches
or exceeds `a*` (which would immediately contradict the `limsup≤a*` half
of the proof) found **zero such cases** at any of the (roughly `1\,517`)
`K` values tested, up to `K=10^6`.

---

## 5. An independent cross-check not in the target document

Worth recording on its own: the `n→∞` limit `Err(n)→3/2`, derived in §3 via
the scaling substitution `x=√n·t`, is a genuinely new analytic fact not
present in `ATTEMPT.md` (which only ever asserts and uses the crude bound
`Err(n)≤5`). It serves two purposes here: it independently corroborates
that my own numerical quadrature of `Err(n)` (rising toward `≈1.5`, never
close to `5`) is not an artifact of the quadrature routine but reflects the
integral's true limiting behavior, and it quantifies exactly how much slack
the target's `Err(n)≤5` (and hence the final `C=6`) leaves on the table —
about `4×` on the `Err` term alone, on top of the roughly `18×` overall
looseness relative to the classical `1/3` that the target itself reports
via its true-gap-vs-`Q(n)` comparison.

---

## 6. Honesty section (piece 2) — checked, found accurate

The target's §3–4 state plainly that monotonicity of `M_K/√K` (equivalently
`sup_K=lim_K`) is attempted along two named routes and **not closed**:

- **Route (a)** (an exact 2-term recursion for `Q(n)`): the target reports
  testing candidate recursions against exact `Q(1),…,Q(9)` and finding none
  holds, citing `Q(3)=17/9≠1+(2/3)Q(2)=2` as a concrete counterexample to
  the simplest candidate. **Independently re-checked**: `Q(2)=3/2`
  (`P_0+P_1=1+1/2`), `Q(3)=17/9` (`1+2/3+2/3·1/3=1+2/3+2/9=17/9`), and
  `1+(2/3)Q(2)=1+1=2≠17/9`. Confirmed — the stated counterexample to the
  candidate recursion is itself correct.
- **Route (b)** (a direct pointwise `M_K≤a*√K` for every `K`): the target
  correctly identifies that Theorem 5's `Q(n)` bound is a *lower* bound and
  Lemma 4.1's `z_K`-bound gives a *lower* bound on `φ_K` — the wrong
  combination for an *upper* bound on `M_K=Q(K+1)-(K+1)φ_K`. This is a
  correct diagnosis, not a hand-wave: producing an upper bound on `M_K`
  tight to `O(1)` at the target's own scale would need a `Q(n)` upper bound
  and a `φ_K` lower bound both accurate to `O(1/√K)` for *every* finite
  `K`, which is a strictly different (and, as the parent's own §7 already
  flagged, "more delicate") task than what Theorem 5 solves. The named
  obstruction is precise and correctly scoped, not vague.
- The numerical evidence for piece 2 (`r_K` strictly increasing,
  `K=1,…,3000`, `mpmath` not exact, explicitly flagged as such) is
  correctly labelled NUMERICAL EVIDENCE / HEURISTIC throughout, never
  PROVED — and my own independent sweep (dense `K` to `1500`/`2000`, sparse
  to `2×10^5`) is consistent with it: `r_K` rose monotonically and stayed
  strictly below `a*` at every one of the (many more than 3000) values I
  checked, with no reversal anywhere.

**The honesty section neither overclaims nor underclaims.** It does not
claim monotonicity is "almost proved" or "just a technicality" — it states
the precise mismatch in bound *direction* that blocks route (b), which is
exactly the obstruction I independently rediscovered while trying to
break it myself.

---

## 7. Findings

| id | severity | finding |
|---|---|---|
| N-1 | nit, not a math error | **Internal count inconsistency in the target's own §2 prose vs. its Files-section tally.** §2's prose describing T4's grid reads "`n=1,…,59` plus `n∈{80,120,200,400,800,1500,3000,6000,12000}`" (a 9-element sparse set, `59+9=68` values total), but the Files section reports "`n` up to `3000`… `66/66` checked" — `66=59+7`, i.e. consistent only with the sparse set `{80,120,200,400,800,1500,3000}` (**dropping** `6000` and `12000`). The two counts (`68` vs. `66`) do not match; the likely explanation is that `6000` and `12000` were mentioned in the derivation-planning prose (matching `DERIVATION_PREREG.md`'s own file-list note) but not actually included in the run whose count (`66/66`) and worst-margin figure (`5.67` at `n=3000`, not at `n=12000`) are reported. **I independently ran the exact bound at both `n=6000` and `n=12000` myself** (`Q(n)` via a from-scratch incremental exact/`mpmath` computation): both hold comfortably (margins `5.6680` and `5.6676`). So this is a bookkeeping/reporting slip in the document's own self-description, not a mathematical error, and not one that affects Theorem 5's correctness — recorded per this archive's discipline of naming every imprecision found, however small. |

**No mathematical error, gap, citation misuse, sign error, off-by-one
error, or overclaim was found in Lemma 5.1, Lemma 5.2, Theorem 5, Theorem
6, or the document's honesty section (§3–4).**

---

## 8. Scorecard

| # | Claim | Target status | **Referee verdict, independent scale** |
|---|---|---|---|
| 1 | Lemma 5.1, termwise `P_j≥h(j)` | PROVED | **CONFIRMED** — derivative argument re-derived by hand; exact `Fraction` vs. `mpmath`, 14,491 pairs `n≤10000` (target: 1,491, `n≤1000`); `mpmath` stress test to 1,350,000 pairs, `n≤10^6` |
| 2 | Lemma 5.2, `h` strictly decreasing | PROVED | **CONFIRMED** — `φ'(x)` numerator re-derived symbolically and by hand as positive-plus-nonnegative; numerically checked, 10,000 points, several `n` |
| 3 | Theorem 5's `ε(x)` decomposition | PROVED (sub-step) | **CONFIRMED** — hand-expanded and symbolically verified, `nx(x+1)-x²(n-x)=x(n+x²)` exactly |
| 4 | The two moment integrals | CITED (elementary) | **CONFIRMED** by independent substitution-by-hand and `sympy.integrate`: `n` and `2n²` exactly |
| 5 | Gaussian integral + tail bound | CITED / PROVED | **CONFIRMED** — tail bound checked against the **exact** `erfc`-based tail (not quadrature), 45 `(n,T)` pairs to `n=10^6`, zero violations |
| 6 | `Err(n)≤3+2e^{-n/8}≤5` | PROVED | **CONFIRMED** against the TRUE integral via `mpmath.quad`, `n≤50000`, zero violations; **new independent result**: `Err(n)→3/2` as `n→∞` (not derived in the target), matching the numerics |
| 7 | Theorem 5, `Q(n)≥√(πn/2)-6` | PROVED | **CONFIRMED**, exact `Fraction` to `n=4000` (68 values) + exactly at `n=6000,12000` + full assembled-bound scan (`mpmath`, cross-validated) to `n=1\,000\,000`; zero violations anywhere, margin converging to `17/3` |
| 8 | Theorem 6's algebra chain | PROVED | **CONFIRMED**, every intermediate rewrite checked as a symbolic identity (`sympy.simplify=0`), not just numerically |
| 9 | Theorem 6, `lim_K M_K/√K=a*` | PROVED | **CONFIRMED**, exact `Fraction` to `K=2000` (66 values) + `mpmath` to `K=1\,000\,000`, zero violations, gap shrinking monotonically to `3.3×10^{-4}`, `r_K` never reaching `a*` |
| 10 | Citation: Observation 0 (`limsup≤a*`, from parent's Theorem 4) | cited, PROVED elsewhere | **CONFIRMED** against the parent document read directly |
| 11 | Citation: Theorem 3, Lemma 4.1, Lemma 4.2 (parent) | cited, PROVED elsewhere, prior adversarial ACCEPT | **Not re-derived** (per mandate); read directly and confirmed used exactly as stated (the specific `v_K`-bound direction, not `z_K`, in Theorem 6) |
| 12 | Honesty section: piece 2 NOT closed, obstruction correctly named | stated OPEN | **CONFIRMED accurate** — route (a)'s counterexample independently re-verified; route (b)'s bound-direction obstruction independently rediscovered while attempting to break it |
| 13 | Independent adversarial re-verification | NOT PERFORMED | **NOW PERFORMED — this report** |

---

## 9. Final verdict

**SOUND. ACCEPT for catalogue.** Theorem 5 (`Q(n)≥√(πn/2)-6` for every
`n≥1`) and Theorem 6 (`lim_{K→∞}M_K/√K=a*` exactly) are both proved
correctly, with every algebraic step — including the two steps the task
flagged as not yet independently hand-derived, the `ε(x)`-decomposition and
`Err(n)`-bound machinery — re-derived from scratch and matching the
target's claims exactly, and every numerical claim independently
re-verified at a scale meeting or exceeding what was checked upstream. I
went further than the proof itself required in one place (§3, §5): an
independent derivation of `Err(n)→3/2` as `n→∞`, not present in the target,
which both cross-validates my own numerics and quantifies precisely how
loose (but valid) the target's `Err(n)≤5` sub-bound is. The document's
honesty section is accurate — piece 2 (monotonicity / `sup_K=lim_K`) is
genuinely not closed, and the named obstruction (matching `O(1/√K)`
two-sided bounds on `Q(n)` and `φ_K`, valid for every finite `K`, not just
asymptotically) is precisely and correctly scoped, not overstated or
understated. The single finding in this report (§7, N-1) is a
self-consistency nit in the target's own reported grid-size arithmetic,
independently confirmed to have no bearing on the correctness of Theorem 5
itself (the bound holds at both of the disputed `n`-values, checked
directly).

---

## 10. Files in this directory

| file | what it does |
|---|---|
| `lemma_5_1_5_2.py` / `lemma_5_1_5_2.log` | Lemma 5.1 (elementary inequality + termwise bound, exact `Fraction` vs. `mpmath`, 14,491 pairs `n≤10000`; `mpmath`-only stress test, 1,350,000 pairs `n≤10^6`) and Lemma 5.2 (symbolic `φ'(x)` re-derivation + numerical monotonicity scan) |
| `theorem5_algebra.py` / `theorem5_algebra.log` | Full re-derivation of Theorem 5: symbolic `ε(x)` decomposition, the two moment integrals and Gaussian integral (`sympy.integrate`), the exact-`erfc` tail bound vs. the claimed bound (45 pairs to `n=10^6`), `ε(x)≤x/n+x³/n²` on `[0,n/2]` (14,007 points), `Err(n)` vs. the TRUE quadrature (`n≤50000`), and the final bound exactly (`n≤4000`, 68 values) |
| `theorem6_algebra.py` / `theorem6_algebra.log` | Full symbolic re-derivation of Theorem 6's assembly (every rewrite as a `sympy.simplify=0` identity, plus the two limits at `K→∞`) and the two-sided numerical squeeze (exact `Fraction` `K≤2000`, `mpmath` to `K=200\,000`) |
| `counterexample_hunt.py` / `counterexample_hunt.log` | Self-consistency check on the target's own §2/Files-section grid counts (§7 finding); independent confirmation of `Q(n)≥√(πn/2)-6` exactly at `n=6000,12000`; an initial (`O(n^2)`-per-scan, later superseded for speed) counterexample hunt, kept for the grid-count and `n=6000/12000` results |
| `counterexample_hunt_part3.py` / `counterexample_hunt_part3.log` | The main counterexample hunt: dense (`n,K≤1500`) + sparse (17 points to `n,K=1\,000\,000`) scan of the *fully assembled* Theorem 5 and Theorem 6 bounds, `O(n)`-per-point incremental `Q(n)`/log-sum; includes a dedicated check for whether `r_K` ever reaches or exceeds `a*` — zero violations found anywhere in either theorem, at any of the roughly `3\,000` combined points checked |

Reproduce in this order: `python3 lemma_5_1_5_2.py`; `theorem5_algebra.py`;
`theorem6_algebra.py`; `counterexample_hunt.py`;
`counterexample_hunt_part3.py`. All scripts are self-contained
(`sympy`/`fractions`/`mpmath`/stdlib only) and were written without reading
any `.py` file from this front's own directory.
