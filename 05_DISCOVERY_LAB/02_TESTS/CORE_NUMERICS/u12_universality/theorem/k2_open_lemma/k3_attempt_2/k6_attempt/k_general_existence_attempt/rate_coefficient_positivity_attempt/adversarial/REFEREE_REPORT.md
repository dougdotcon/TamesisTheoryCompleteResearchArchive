# Adversarial referee report — `RATE-COEFFICIENT-POSITIVITY-ATTEMPT`

**Target under review.**
`k_general_existence_attempt/rate_coefficient_positivity_attempt/ATTEMPT.md`
(wave 9, front (b), `DISC-DEC-041`).

**Claim under review.** That the exact `1/n` rate coefficient
`c_K:=K[\varphi_K/4+F_{K-1}(1,1)-\varphi_K]` is strictly positive for every
integer `K\ge2`, via the collapse `c_K=[(K{+}2)\varphi_K-2]/4` and a
monotone-ratio argument on `v_K:=(K{+}2)\varphi_K` anchored at `v_1=2`;
upgrading the already-PROVED `\varphi_n^{(K)}-\varphi_K=O(1/n)` to
`\Theta(1/n)` for every `K\ge2`.

**Date of review:** 2026-08-22. **Mandate:** `DISC-DEC-041`,
`untouched_safeguards` line 2 ("qualquer resultado positivo exige verificação
adversarial obrigatória antes de catalogar").

---

# VERDICT

> ## **SOUND.**
>
> The target theorem is genuinely established. I attacked every step of the
> argument, independently re-derived every load-bearing identity before
> reading how the document derives it, wrote every verification script from
> scratch, and **found no error of any kind in any numbered claim.**
>
> The proof is correct, short, elementary, non-asymptotic, non-circular, and
> its scope is stated accurately throughout. Lemma 1, Theorem A, Theorem B and
> Corollary B′ are all **PROVED** exactly as labelled. The second proof (§4.4)
> is also correct. Every exact rational value printed in the document —
> **all 85 cells of the §3 table (17 rows × 5 entries), checked
> individually** — is right. The document's own honesty labels
> (`PROVED` / `NUMERICALLY VERIFIED` / `NOT PERFORMED`) are accurate, and its
> claims about its own scripts (23 / 29 / 3 checks, 0 failures, ~26 s / ~12 s /
> ~3 s) reproduce exactly on re-run.
>
> I record **four notes (N-1 … N-4)**. **None is an error, none affects any
> numbered claim, and none requires a correction before cataloguing.** They are
> presentational observations only, listed for completeness because this
> lineage's standard is to name everything found.
>
> **Recommendation: CATALOGUE**, with the precise wording given in §F.

Verdict qualifier for the record: this is the first document I have refereed in
this lineage where I found **no issue requiring correction**. That is not
because I looked less hard — I made five independent scripts, five deliberate
break attempts, and three predictions of my own that go beyond anything the
target tested (all three confirmed exactly, §D.4). The result is simply
correct, and it is correct for a structural reason: after the collapse, the
whole question is a two-line statement about the Wallis integral.

---

# A. Method and discipline

Per the dispatch, for each of items 1–7 I derived the result **by hand first**,
then wrote fresh code, and only then opened the target document. Concretely, my
own derivations of Lemma 1, Theorem A, the Wallis ratio, the `=K` cancellation,
`v_1=2`, the telescoping sum, and the `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}`
route were all complete and machine-confirmed **before** the target's
`ATTEMPT.md` was opened. Only the §3/§6 table transcriptions and the §10
script-honesty audit were necessarily done afterwards.

- Nothing was imported or copied from `rate_coefficient_positivity_attempt/`
  or any sibling directory. All five scripts below are mine, written from
  scratch in this `adversarial/` subdirectory.
- All arithmetic is exact: `fractions.Fraction` or `sympy` with `K` a genuine
  `Symbol`. Floating point appears only where explicitly labelled as a decimal
  display of a trend, and in the `mpmath` (60-digit) asymptotic study of
  §C.9(c), where the object of study is itself an asymptotic statement.
- Upstream facts used as given, not re-derived (per the dispatch's
  out-of-scope list): the `F_r(t,b)` closed form (`k6_attempt/ATTEMPT.md`
  §2.3, PROVED), `\varphi_K=4^K(K!)^2/(2K{+}1)!` (`THEOREM.md` §5.2, Lemma 2,
  PROVED), the exact `(a,b,r)` transition rules (`k3_attempt_2/ATTEMPT.md` §2,
  PROVED), wave 5's Reduction Lemma A (PROVED), and the discrete-Gronwall
  existence theorem (`../ATTEMPT.md`, already adversarially refereed).
  I re-transcribed each of these by hand from its stated formula rather than
  copying code.
- No file outside this `adversarial/` directory was created or modified.
  `git status` confirms: only untracked new directories, no tracked file
  touched, no commit made. No model name appears in any file I wrote.

**My scripts** (all in this directory, each with its `.log`):

| script | what it does |
|---|---|
| `ref_01_raw_ck.py` | `c_K` from the RAW definition, exact, `K=1..50` + `K\in\{100,200,500,1000,5000\}`; `F_{K-1}(1,1)` by **four** independent routes; the four quoted table fractions; `F_r(1,0)=\varphi_r` anchor `r=0..40` |
| `ref_02_symbolic.py` | S1–S10: every load-bearing identity with `K` (and `k`) a `sympy.Symbol`; the binomial-row-tail identity exactly for 64 values of `K`; `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}` exactly for 204 values of `K` |
| `ref_03_asymptotics.py` | item 9(c): the `\sqrt{\pi K}/8` asymptotic at 60-digit precision to `K=10^7`; the exact monotone increment `K=1..399` |
| `ref_04_table_and_finite_n.py` | all 85 cells of the §3 table; an **independent from-scratch** implementation of the raw `(a,b,r)` chain + Reduction Lemma A, exact `1/n`-coefficient extraction with out-of-sample validation, `K=1..9` |
| `ref_05_break_attempts.py` | five deliberate attempts to break the result, incl. exhaustive sweeps to `K=3000`, a literal machine induction, and three predictions of my own beyond the target's range |

Totals: **0 discrepancies anywhere**, across every check listed below.

---

# B. My independent derivations, item by item

Each subsection states what I got **before** looking at the target, then the
comparison.

## B.1 (dispatch item 1) Lemma 1 — `F_{K-1}(1,1)` in closed form

Starting from the `k6_attempt` §2.3 formula, re-transcribed by hand:

`\displaystyle F_r(t,b)=\sum_{k=0}^{r}\frac{r!}{(r-k)!}\cdot
\frac{t^k}{\prod_{i=1}^{k+1}(r{+}b{+}i)}`.

Put `r=K{-}1`, `b=1`, `t=1`. Then `r{+}b{+}i=K{+}i`, so
`\prod_{i=1}^{k+1}(K{+}i)=(K{+}k{+}1)!/K!`, and

`\displaystyle F_{K-1}(1,1)=(K{-}1)!\,K!\sum_{k=0}^{K-1}
\frac1{(K{-}1{-}k)!\,(K{+}k{+}1)!}`.

**The "constant in `k`" step, verified exactly (not approximately).**
`(K{-}1{-}k)+(K{+}k{+}1)=2K`: the `k` cancels identically, symbolically
verified in sympy with `k` and `K` both free symbols (S8: the difference
simplifies to `0`). Because the two factorial arguments sum to the *same*
constant `2K` for every `k`, multiplying each summand by `(2K)!/(2K)!` gives
**exactly** — no approximation, no asymptotics — a binomial coefficient of row
`2K`:

`\displaystyle\frac{(2K)!}{(K{-}1{-}k)!\,(K{+}k{+}1)!}=\binom{2K}{K{+}k{+}1}`,

legitimate because `(2K)-(K{+}k{+}1)=K{-}1{-}k`, which is `\ge0` exactly on the
summation range `0\le k\le K{-}1`. As `k` runs `0\to K{-}1`, `j:=K{+}k{+}1`
runs `K{+}1\to2K` — a bijection onto the strict upper tail of the row. Endpoint
check: `k=0\mapsto\binom{2K}{K+1}`, `k=K{-}1\mapsto\binom{2K}{2K}=1`. Both
correct.

**The binomial-row-tail identity, re-derived from scratch.** By the binomial
theorem at `x=1`, `\sum_{j=0}^{2K}\binom{2K}{j}=(1{+}1)^{2K}=4^K`. By row
symmetry `\binom{2K}{j}=\binom{2K}{2K-j}`, the strict lower tail
(`j\le K{-}1`) and the strict upper tail (`j\ge K{+}1`) are term-by-term equal,
so with `S` the common value, `2S+\binom{2K}{K}=4^K`, i.e.

`\displaystyle S=\sum_{j=K+1}^{2K}\binom{2K}{j}=\frac{4^K-\binom{2K}{K}}2`.

Machine-checked exactly (row sum `=4^K`, row symmetry entry by entry, tail
value) for `K\in\{1,\dots,60\}\cup\{100,250,501,1000\}` — **0 failures**.

Hence, using `\dfrac{(K{-}1)!K!}{(2K)!}=\dfrac1{K\binom{2K}{K}}` and
`\varphi_K=\dfrac{4^K}{(2K{+}1)\binom{2K}{K}}` (itself verified exactly for
`K=0..300`):

> **My result:** `\displaystyle F_{K-1}(1,1)
> =\frac1{2K}\left[\frac{4^K}{\binom{2K}{K}}-1\right]
> =\frac{(2K{+}1)\varphi_K-1}{2K}`.

**Comparison: identical to the target's Lemma 1.** The target's proof takes the
same route, and every intermediate line of it — (2.1), (2.2), (2.3), (2.4) —
is correct as printed. Verified additionally with `K` fully symbolic via gamma
functions (S1: `F_{\rm mine}-F_{\rm target}` simplifies to exactly `0`), and by
**four independent numerical routes agreeing exactly for `K=1..50`**:
(a) the §2.3 closed-form sum; (b) the §2.3 *diagonal coefficient recursion*
`c_0^{(r)}(b)=1/(1{+}r{+}b)`, `c_k^{(r)}(b)=\frac r{k+1+r+b}c_{k-1}^{(r-1)}(b{+}1)`
summed at `t=1` (i.e. bypassing the closed form entirely and using only the
recursion it solves); (c) my hand collapse; (d) the target's Lemma 1 statement.

Anchor sanity: my transcription of `F_r(t,b)` reproduces
`F_r(1,0)=\varphi_r` exactly for `r=0..40` (the `k6_attempt` §2.3 table gives
seven of these; I extended to 41), confirming I transcribed the upstream
formula correctly.

**Structural check on why `b=1` is the right argument.** `k6_attempt` §2.2's
algebraic relation is `\hat H_r(s,b)=(1{-}s)F_r(1{-}s,b{+}1)`; at `s=0,b=0`
this gives `\hat H_{K-1}(0,0)=F_{K-1}(1,1)` — exactly the substitution the
wave-8 referee's §A.7 used to obtain `c_K`. The `b=1` is forced, not chosen.

## B.2 (dispatch item 2) Theorem A

By hand, with `\varphi:=\varphi_K`:

`c_K=K[\varphi/4+F_{K-1}(1,1)-\varphi]=K\varphi/4-K\varphi
+\tfrac12[(2K{+}1)\varphi-1]
=\varphi\big[\tfrac K4-K+\tfrac{2K+1}2\big]-\tfrac12`,

and `\tfrac K4-K+\tfrac{2K+1}2=\tfrac{K-4K+4K+2}4=\tfrac{K+2}4`. So

> **My result:** `c_K=\dfrac{(K{+}2)\varphi_K-2}4`.

**Comparison: identical to the target's Theorem A.** The target computes it via
`\frac{2K+1}2-\frac{3K}4=\frac{K+2}4`, which is the same cancellation written
differently and is correct. **No sign error.** Verified symbolically with both
`K` and `\varphi` free symbols: both sides expand to `K\varphi/4+\varphi/2-1/2`,
difference exactly `0` (S2).

## B.3 (dispatch item 3) The Wallis ratio

`\dfrac{\varphi_{K+1}}{\varphi_K}
=\dfrac{4^{K+1}((K{+}1)!)^2}{(2K{+}3)!}\cdot\dfrac{(2K{+}1)!}{4^K(K!)^2}
=\dfrac{4(K{+}1)^2}{(2K{+}2)(2K{+}3)}
=\dfrac{4(K{+}1)^2}{2(K{+}1)(2K{+}3)}=\dfrac{2(K{+}1)}{2K{+}3}
=\dfrac{2K{+}2}{2K{+}3}`.

**Comparison: matches the target's §4.1 Fact exactly**, including the
intermediate lines as printed. Verified with `K` symbolic via gamma functions
(S3: difference exactly `0`), and exactly for `K=0..300`. The equivalent product
form `\varphi_K=\prod_{j=1}^K\frac{2j}{2j+1}` also checks
(`\varphi_0=1`, `\varphi_1=2/3`, `\varphi_2=8/15`, `\varphi_3=16/35`).

## B.4 (dispatch item 4) The load-bearing cancellation, and the anchor

`2(K{+}1)(K{+}3)=2K^2+8K+6`; `(K{+}2)(2K{+}3)=2K^2+7K+6`; difference `=K`.
Verified by symbolic expansion (S4): `\text{LHS}-\text{RHS}-K` expands to
exactly `0`.

`v_1=3\varphi_1`, and `\varphi_1=4^1(1!)^2/3!=4/6=2/3`, so `v_1=3\cdot\frac23=2`
**exactly as a `Fraction`, not numerically close to 2** (S5). Consequently
`c_1=(v_1-2)/4=0` exactly.

**Comparison: both match the target exactly.** This is THE cancellation the
whole positivity argument rests on, and it is right.

## B.5 (dispatch item 5) Is the induction/monotonicity actually valid?

The chain is: `v_{K+1}/v_K-1=K/[(K{+}2)(2K{+}3)]>0` for `K\ge1`, plus `v_1=2`,
gives `v_K>2` for all `K\ge2`. I checked this for an off-by-one at the boundary
and for a hidden positivity assumption:

- **Boundary.** The first application is at `K=1`:
  `v_2/v_1-1=1/(3\cdot5)=1/15>0`, so `v_2=2\cdot\frac{16}{15}=\frac{32}{15}>2`.
  The induction's base case is therefore `K=2`, and `v_2>2` holds. Every
  subsequent step gives `v_{K+1}>v_K>2`. **No off-by-one.** (The document's
  table independently prints `v_2=32/15`, which I confirmed.)
- **Direction of the quantifiers.** The increment identity is claimed for
  `K\ge1` and the conclusion for `K\ge2`. That is exactly right and exactly
  what the document says. At `K=0` the increment is `0` (the cancellation gives
  `K=0`), so `v_0=v_1=2` — the sequence is flat on `\{0,1\}` and strictly
  increasing from `K=1` onward. The document notes this (§4.2's closing
  remark: "is `0` at `K=0` and positive for every `K\ge1`").
- **Hidden sign assumption?** Strictly, "ratio `-1>0` ⟹ `v_{K+1}>v_K`" needs
  `v_K>0`. See N-1 below: it is immediate and is carried by the induction
  itself, so there is no gap — only a one-clause omission.

**Machine induction (B3 of `ref_05`).** To be certain the recursion really
generates `v_K` and the telescoping is not a non sequitur, I started from the
bare anchor `v=\mathrm{Fraction}(2)` and applied *only*
`v\mapsto v\,(1+K/[(K{+}2)(2K{+}3)])`, never touching `\varphi_K` again. The
generated sequence equals `(K{+}2)\varphi_K` exactly for `K=1..1500` and
exceeds `2` for every `K\ge2`. **The induction is valid.**

## B.6 (dispatch item 6) The manifestly-positive telescoping sum

From `v_{K+1}-v_K=v_K\cdot\frac K{(K+2)(2K+3)}` and `v_K=(K{+}2)\varphi_K`:

`\displaystyle v_{K+1}-v_K=\frac{K\varphi_K}{2K{+}3}`,

verified symbolically with `\varphi` and `K` free symbols (S6: difference
exactly `0`). Summing `j=1,\dots,K{-}1` from the anchor `v_1=2`:

> **My result:** `\displaystyle c_K=\frac{v_K-2}4
> =\frac14\sum_{j=1}^{K-1}\frac{j\,\varphi_j}{2j{+}3}`.

**Comparison: identical to the target's Corollary B′.**

**Worked example, both ways.** Theorem A at `K=4`:
`c_4=[6\cdot\frac{128}{315}-2]/4=\frac{23}{210}`. Telescoping sum:
`\frac14[\frac{1\cdot2/3}5+\frac{2\cdot8/15}7+\frac{3\cdot16/35}9]
=\frac14[\frac2{15}+\frac{16}{105}+\frac{16}{105}]
=\frac14\cdot\frac{46}{105}=\frac{23}{210}` ✓ — **matches the target's §4.3
worked example exactly**, including its intermediate fractions.

Both routes agree exactly for `K=1..50` and at `K=100,200,500,1000,5000`
(`ref_01` Parts 2–3), and both agree with the raw definition.

## B.7 (dispatch item 7) The second proof, via `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}`

**Re-proof of the classical bound.** With
`a_K:=\binom{2K}{K}\sqrt{3K{+}1}/4^K`: `a_0=1`, `a_1=2\cdot2/4=1`. Since
`\binom{2K+2}{K+1}/\binom{2K}{K}=\frac{(2K{+}2)(2K{+}1)}{(K{+}1)^2}
=\frac{2(2K{+}1)}{K{+}1}` (verified symbolically, S9),

`\displaystyle\frac{a_{K+1}}{a_K}=\frac{2K{+}1}{2(K{+}1)}
\sqrt{\frac{3K{+}4}{3K{+}1}}`,

which is `\le1` iff `(2K{+}1)^2(3K{+}4)\le4(K{+}1)^2(3K{+}1)`. Expanding:
`4(K{+}1)^2(3K{+}1)=12K^3+28K^2+20K+4` and
`(2K{+}1)^2(3K{+}4)=12K^3+28K^2+19K+4`; **difference `=K\ge0`** (S9,
symbolic). So `a_{K+1}\le a_K` for `K\ge0` (equality only at `K=0`), hence
`a_K\le a_0=1` for all `K\ge0`, i.e. `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}`.

**Independent truth check of the bound itself**, in exact integer arithmetic
(comparing `\binom{2K}{K}^2(3K{+}1)` against `16^K`, avoiding square roots
entirely): holds for every `K\in\{0,\dots,200\}\cup\{500,1000,3000\}`, with
**equality exactly at `K=0` and `K=1`** and strict inequality elsewhere — which
is precisely consistent with `c_0=c_1=0` being the equality cases.

**The final cubic.** `(K{+}2)^2(3K{+}1)=3K^3+13K^2+16K+4`;
`(4K{+}2)^2=16K^2+16K+4`; difference `=3K^3-3K^2=3K^2(K{-}1)`, `>0` exactly for
integers `K\ge2` (S10, symbolic: difference from `3K^2(K{-}1)` expands to `0`).

**Comparison: every line of the target's §4.4 is correct as printed**,
including the intermediate expansions `3K^3{+}13K^2{+}16K{+}4` and
`16K^2{+}16K{+}4`, and the sufficiency reduction
`4^K/\sqrt{3K{+}1}<4^K(K{+}2)/(2(2K{+}1))\iff(4K{+}2)<(K{+}2)\sqrt{3K{+}1}`.
Note the target defines `a_K` as the reciprocal of a natural alternative; I
checked both orientations and both give difference `=K`, consistently.

The §5.3 lower bound `c_K\ge\frac14[(K{+}2)\sqrt{3K{+}1}/(2K{+}1)-2]` follows
correctly, is `0` at `K=0,1` and positive exactly for `K\ge2`, and I confirmed
its two quoted numerical instances: at `K=13` it gives `0.37841\ldots` against
the true `0.39617\ldots`, and at `K=10^4` it gives `21.1542\ldots` against the
true `21.6593\ldots`. Its `\sqrt3/8` vs. `\sqrt\pi/8` growth-constant remark is
also right.

---

# C. Fresh numerics and the specific failure modes probed

## C.1 (dispatch item 8) `c_K` from the RAW definition, exact

`ref_01_raw_ck.py` computes `c_K=K[\varphi_K/4+F_{K-1}(1,1)-\varphi_K]` with
`fractions.Fraction` **from the raw definition**, `F` built from the §2.3
closed-form sum (not from Theorem A's collapse):

- `K=1..50`: RAW `==` Theorem A `==` telescoping sum, **0 mismatches**;
  `c_1=0` exactly; `c_K>0` for every `2\le K\le50`.
- Large-`K` spot checks `K=100,200,500,1000,5000`: RAW `==` Theorem A `==`
  telescoping sum, all `>0`, **0 mismatches**.
- `ref_05` extends: RAW definition `K=1..400` — no counterexample, no mismatch;
  closed form `K=1..3000` — **no counterexample to `c_K>0` (`K\ge2`) and no
  failure of strict monotonicity**.

**Spot-checks of specific fractions quoted in the target's table:**

| `K` | target's value | my exact value from the RAW definition | match |
|---|---|---|---|
| 2 | `1/30` | `1/30` | ✓ |
| 3 | `1/14` | `1/14` | ✓ |
| **6** | `1093/6006` | `1093/6006` | ✓ |
| **9** | `11773/41990` | `11773/41990` | ✓ |

`c_6=1093/6006` is now confirmed by a **sixth** independent route in this
archive (the wave-5 correction's four methods, the wave-8 referee's §A.7, and
this review's raw-definition computation).

**All 85 cells of the §3 table** (`K=1..16` and `K=20`; columns `\varphi_K`,
`F_{K-1}(1,1)`, `v_K`, `c_K`, and the printed 9-decimal display) were
recomputed independently: **0 bad cells** (`ref_04` Part A).

## C.2 (dispatch item 9a) Is a sign assumption smuggled in?

`\varphi_K=4^K(K!)^2/(2K{+}1)!` is manifestly a quotient of positive integers,
so `\varphi_K>0` needs no argument at all; the target additionally records the
integral representation `\varphi_K=\int_0^1(1-x^2)^K dx` in §4.1 explicitly to
make positivity self-evident, while stating that the integral form "is *not*
used in the proof". I checked every step for a place where a sign could be
assumed rather than established:

- §4.2's "Both numerator and denominator are positive" refers to the ratio
  expression `2(K{+}1)(K{+}3)/[(K{+}2)(2K{+}3)]`, and is correct for `K\ge1`.
- The only place positivity of `v_K` itself is needed is the implication
  "ratio `>1\Rightarrow v_{K+1}>v_K`" — see **N-1**; it is immediate and is in
  any case supplied by the induction's own base case `v_1=2>0`.
- Corollary B′'s summands `j\varphi_j/(2j{+}3)` are positive for `j\ge1` by
  inspection.
- §4.4's squaring step "(squaring, both sides positive)" is explicitly
  justified in the text, and both sides genuinely are positive for `K\ge0`.

**No smuggled sign assumption found.**

## C.3 (dispatch item 9b) Is `K=1` the *exact* equality case, symbolically?

Yes. `v_1=3\varphi_1=3\cdot\frac23=2` as an exact `Fraction`; `c_1=0` as an
exact `Fraction`; the sympy check `c_K|_{K=1}` simplifies to exactly `0`. This
is **not** a floating-point coincidence.

I additionally swept **every integer `K\in[0,3000]`** for exact equality
`(K{+}2)\varphi_K=2` using `Fraction` equality: the complete solution set is
`\{0,1\}`. Within the document's declared domain `K\ge1`, `K=1` is therefore
the unique equality case, exactly as claimed. (`K=0` is discussed under **N-3**;
it is harmless, is anticipated by the document's own §4.2 remark, and I verified
that `\varphi_n^{(0)}=1` exactly for `n=2..8` from the raw chain, so the `K=0`
case is entirely degenerate and `c_0=0` is correct there too.)

## C.4 (dispatch item 9c) Does the `\sqrt{\pi K}/8` asymptotic follow?

I derived it independently. Using the exact identity
`\varphi_K=4^K/[(2K{+}1)\binom{2K}{K}]` (verified exactly for `K=0..300`) and
the classical `\binom{2K}{K}4^{-K}=(\pi K)^{-1/2}(1-\frac1{8K}+\frac1{128K^2}
+\cdots)`:

`\varphi_K=\frac{\sqrt{\pi K}}{2K{+}1}\big(1+\frac1{8K}+\frac1{128K^2}+\cdots\big)`,
and `\frac{K+2}{2K+1}=\frac12\big(1+\frac3{2K}-\frac3{4K^2}+\cdots\big)`, so

`(K{+}2)\varphi_K=\frac{\sqrt{\pi K}}2\big(1+\frac{13}{8K}+O(K^{-2})\big)`,
hence

> `\displaystyle c_K=\frac{\sqrt{\pi K}}8-\frac12+\frac{13\sqrt\pi}{64\sqrt K}
> +O(K^{-3/2})`.

**This is exactly the target's §5.2 expansion, including the `13\sqrt\pi/64`
coefficient**, which I derived independently before reading it. Numerical
confirmation at 60-digit precision (`ref_03`): `\sqrt K\,(c_K-\text{lead}+\frac12)`
equals `0.3599068575, 0.3600173996, 0.3600284595, 0.3600295656, 0.3600296762`
at `K=10^3,10^4,10^5,10^6,10^7`, converging to `13\sqrt\pi/64=0.3600296885`
— **agreement to 7 significant figures**. The residual after all three terms,
scaled by `K^{3/2}`, is flat at `-0.12289` across `K=200\ldots10^6`
(the target's script prints `|{\cdot}|`, hence its `\approx0.1229`; same number).

So `c_K\sim\sqrt{\pi K}/8` is **correct at leading order** and the three-term
expansion is right. **No hidden error.** One thing a reader should know (this is
not an error in the document, which states the expansion with its `-1/2` term
explicitly in §5.2): the *ratio* `c_K/(\sqrt{\pi K}/8)` converges only slowly —
`0.79` at `K=100`, `0.930` at `K=10^3`, `0.9993` at `K=10^7` — because the
`-1/2` correction is `O(1)` against an `O(\sqrt K)` leading term. The document's
executive summary phrase "`c_K\to\infty` like `\sqrt{\pi K}/8`" is a correct
statement about growth order and is not affected.

## C.5 The transcription guard — re-done independently (target's §6)

This is the one thing the algebraic proof cannot self-check: is the expression
proved positive really the `1/n` coefficient? I re-implemented the **raw**
`(a,b,r)` transition rules of `k3_attempt_2/ATTEMPT.md` §2 from scratch
(memoized exact `Fraction` recursion, my own code, never touching `F_r`,
`G_r`, or anything in §§2–5 of the target), formed
`\varphi_n^{(K)}=(K/n)h(0,0,K{-}1)+(1-K/n)g(0,0,K)` via Reduction Lemma A,
fitted `\varphi_n^{(K)}` as an exact polynomial in `1/n` of degree `K{+}1` by
exact Gaussian elimination over `Fraction`, and validated each fit **out of
sample on six `n` values the fit never saw**.

- Sanity 1: `\varphi_n^{(3)}=\frac{16}{35}+\frac1{14n}+\frac{11}{10n^2}
  +\frac{23}{35n^3}+\frac6{35n^4}` exactly, `n=4..26` ✓ (wave 6's PROVED
  closed form, reproduced by my independent implementation).
- Sanity 2: `\varphi_n^{(1)}-\varphi_1=1/(3n^2)` exactly, `n=2..40` ✓
  (the `K=1` degeneracy / issue I-4, reproduced independently; I also
  reproduce the wave-8 referee's printed values at `n=3,5,10,20`).
- `K=1..9`: `\alpha_0=\varphi_K` and `\alpha_1=c_K` **exactly**, every fit
  out-of-sample validated. This reproduces the target's §6 table row for row.

**And beyond it — three predictions of my own** (`ref_05` B4). From Theorem A I
predicted, before computing them, that the finite-`n` `1/n` coefficients at
`K=10,11,12` would be `200965/646646`, `106135/312018` and `1779879/4828850`,
and that the degree in `1/n` would be exactly `K{+}1`. **All three confirmed
exactly**, out-of-sample validated, top coefficient nonzero. The target's §6
stops at `K=9`; these are new. The transcription risk is closed.

## C.6 Four genuinely different formulas must agree

`ref_05` B5: the raw definition, the product form
`\frac{K+2}4\prod_{j=1}^K\frac{2j}{2j+1}-\frac12`, the central-binomial form
`\frac{(K+2)4^K}{4(2K+1)\binom{2K}{K}}-\frac12`, the telescoping sum, and
Theorem A all agree **exactly** for `K=1..300`. **0 disagreements.**

---

# D. Audit of the document's own honesty and scope claims (dispatch item 10)

## D.1 Are the PROVED / VERIFIED labels accurate?

| Scorecard row | document's label | my assessment |
|---|---|---|
| 1 Lemma 1 | PROVED | **Confirmed.** Elementary and complete; I re-derived it independently and it is right, including the exact (not approximate) binomial rewrite. |
| 2 Theorem A | PROVED | **Confirmed.** One line, no sign error. |
| 3 Theorem B | PROVED | **Confirmed.** Elementary, non-asymptotic, no off-by-one, valid induction. |
| 4 Corollary B′ | PROVED | **Confirmed**, incl. the `K=4` worked example. |
| 5 Second proof (§4.4) | PROVED | **Confirmed**, incl. the re-proof of the classical bound. See **N-2** on the word "independent". |
| 6 Corollaries (§5) | PROVED; asymptotic "PROVED **given** the classical Wallis-ratio expansion" | **Confirmed, and the conditional wording is exactly right.** The script itself discloses that sympy cannot do gamma-at-infinity and that the classical expansion is fed in. Honest. See **N-4** on the §5 header. |
| 7 Finite-`n` corroboration (§6) | **NUMERICALLY VERIFIED**, explicitly *not* part of the proof | **Confirmed and correctly labelled.** Exact rational, out-of-sample validated. It would have been easy — and wrong — to call this PROVED; the document does not. |
| 8 Adversarial re-verification | **NOT PERFORMED** | **Correct at time of writing. Now performed — this report.** |
| 9 Upstream `1/n` identification | **NOT RE-PROVED HERE**, reused as PROVED | **Correctly labelled as a dependency**, and correctly *not* claimed as this document's work. |
| 10 Other open items | **NOT ADDRESSED** | **Correctly labelled.** §8's list matches `THEOREM.md` Estágio 6's list minus item (iii), as claimed — I checked item by item. |

**I found no instance of PROVED-where-only-VERIFIED, and no instance of the
reverse.** The `NUMERICALLY VERIFIED` label on §6 is, if anything, modest.

## D.2 Is the `K\ge2` scoping consistent everywhere?

I grepped every positivity / `\Theta` statement in the document and checked its
quantifier individually. Every one of them says `K\ge2`:

- Title, executive summary (twice), §1 "What this document must decide",
  §4 header, Theorem B, §8's two bullets, Scorecard row 3, and the net verdict.
- The only `K\ge1` quantifiers are on (a) the increment identity (4.1) — true
  for `K\ge1`; (b) Corollary B′ — true for `K\ge1`, giving `0` at `K=1`;
  (c) strict monotonicity of `c_K` on `K\ge1` — true, since `c_1=0<c_2`;
  (d) Lemma 1 and Theorem A themselves — true for `K\ge1`, since they are
  identities, not inequalities. **Every one of these is correct at `K=1`.**
- `\Theta(1/n)` is always qualified "for every **fixed** `K\ge2`" — no
  uniformity in `K` is claimed anywhere, which is correct, since the
  `O(1/n^2)` remainder's constant depends on `K`.

**No place accidentally implies `K\ge1` positivity.** The `K=1` exclusion is
stated in the title, the executive summary, §1's dedicated note, §3, §4.2,
§4.3 and §8 — seven times, consistently.

## D.3 Do the document's claims about its own scripts hold up?

I re-ran all three target scripts:

| claimed | observed |
|---|---|
| `verify_ck_closed_form.py`: 23 checks, 0 failures, ≈26 s, exit 0 | **23 `[OK]`, 0 failures, 25.6 s, exit 0** |
| `verify_symbolic_K.py`: 29 checks, 0 failures, ≈12 s, exit 0 | **29 `[OK]`, 0 failures, 12.1 s, exit 0** |
| `corroborate_finite_n.py`: 3 checks, 0 failures, ≈3 s, exit 0 | **3 `[OK]`, 0 failures, 2.7 s, exit 0** |
| "55 checks, 0 failures, all three exiting `0`" | **55 checks, 0 failures, all exit 0** |
| "`K` kept **symbolic** (`sympy.Symbol`, positive integer), not sampled" | **True.** `K = sp.symbols('K', positive=True, integer=True)` with gamma-function representations throughout; the identities are `simplify(...)==0` on symbolic expressions, not point samples. |
| "1575 exact agreements (`r=0..24`, `b=0..8`, seven `t`)" | **True** (`25\times9\times7=1575`), and the log says so. |
| ranges "`K=1..120`", "`K=1..300`", "`K=2..5000`" | **All present in the log as claimed.** |

This is a rare case where the retained logs are, if anything, *understated*
relative to what the scripts do. Contrast with issue I-3 of the wave-8 review
(descriptions more optimistic than the logs): **that failure mode does not
occur here.** `PROGRESS.log`'s chronology is also consistent with §7's honest
record, including the two superseded intermediate routes.

## D.4 Is there any circularity?

No. Theorem B's proof consumes exactly: the `F_r(t,b)` closed form (upstream,
PROVED), `\varphi_K=4^K(K!)^2/(2K{+}1)!` (upstream, PROVED), and elementary
algebra. The upstream identification of `c_K` as the rate coefficient is used
only to *interpret* the result, is labelled as a dependency (Scorecard row 9),
and is independently corroborated in §6 — which I re-did myself and extended.
Nothing in §§2–5 is used to establish anything §§2–5 assumes.

---

# E. Named notes (N-1 … N-4)

**None of these is an error. None affects any numbered claim. None blocks
cataloguing.** They are recorded because this lineage's discipline is to name
everything found.

### N-1 (presentational; zero mathematical consequence)

§4.2 argues `\frac{v_{K+1}}{v_K}-1=\frac K{(K{+}2)(2K{+}3)}>0`, "Hence
`v_{K+1}>v_K`". Strictly, passing from a statement about the *ratio* to one
about the *difference* uses `v_K>0`. The document does not write that clause at
the point of use. It is nevertheless not a gap: `v_K=(K{+}2)\varphi_K` with
`\varphi_K=4^K(K!)^2/(2K{+}1)!` a quotient of positive integers, so `v_K>0` by
inspection; §4.1's parenthetical explicitly records that the integral form
"makes `\varphi_K>0` self-evident"; and the induction supplies it anyway, since
it starts from `v_1=2>0` and each multiplicative factor exceeds `1`. **No
correction needed;** at most one could add five words. I verified the induction
as a literal machine induction (§B.5) precisely to rule out any gap here.

### N-2 (terminology)

§4.4 is headed "A second, **independent** proof" and says it "shares no algebra
with §4.2 beyond Theorem A". The *algebra performed* is genuinely different
(`(2K{+}1)^2(3K{+}4)` vs `4(K{+}1)^2(3K{+}1)` against `(K{+}3)(2K{+}2)` vs
`(K{+}2)(2K{+}3)`), so the literal claim is true. But both cancellations reduce
to the same underlying central-binomial/Wallis recursion — `\varphi_{K+1}/
\varphi_K=(2K{+}2)/(2K{+}3)` and `\binom{2K+2}{K+1}/\binom{2K}{K}
=2(2K{+}1)/(K{+}1)` are the same fact wearing different clothes, which is why
**both** cancellations come out to exactly `K`. So §4.4 is best described as a
second *route* through a different intermediate object (a classical inequality
with slack), not a logically independent proof from different mathematical
input. The document's own §7 already says §4.4 "is strictly weaker and less
self-contained than §4.2", which is the honest framing; only the §4.4 heading
is slightly stronger than that. **Both proofs are correct**; the result does not
depend on §4.4 at all.

### N-3 (completeness)

`K=0` is also an exact equality case: `v_0=2\varphi_0=2`, so `c_0=0`. The
document quantifies over `K\ge1` throughout (fixed in §1's first line), so
"`K=1` is the exact equality case" is correct within its stated domain, and
§4.2's closing remark already observes that the cancellation "is `0` at `K=0`".
For the record: the `K=0` case is entirely degenerate — I verified from the raw
chain that `\varphi_n^{(0)}=1` exactly for every `n` tested, so there is no
error term at all there and `c_0=0` is right. A cataloguing note should simply
avoid the phrase "the unique equality case" without the `K\ge1` qualifier.

### N-4 (cosmetic)

The §5 section header reads "Corollaries (all PROVED)", while Scorecard row 6
more carefully says the three-term asymptotic is "PROVED **given** the classical
Wallis-ratio expansion". The Scorecard's wording is the accurate one and is the
one that should govern. Since the Wallis-ratio/Stirling expansion is a standard
classical fact (and I confirmed the resulting expansion numerically to 7
significant figures), this is a wording mismatch of no substance. §5.1 and §5.3
are unconditionally PROVED.

---

# F. Recommendation for cataloguing in `THEOREM.md`

**Recommendation: CATALOGUE this result as PROVED.** It closes, by proof rather
than by extended verification, the item that Estágio 6 named as open. I did not
edit `THEOREM.md`, `DECISION_LEDGER.yaml`, or any governance file — integration
is the orchestrating session's job. Suggested content:

**1. Mark Estágio 6, item 4's remaining piece — and the "what remains open"
list's item (iii) ("*a positividade do coeficiente de taxa para `K\ge13`*") —
as CLOSED**, affirmatively, and in fact for all `K\ge2` uniformly.

**2. The statement to record.** For every fixed integer `K\ge2`,

> `\displaystyle\lim_{n\to\infty}n\big(\varphi_n^{(K)}-\varphi_K\big)
> =c_K=\frac{(K{+}2)\varphi_K-2}4
> =\frac14\sum_{j=1}^{K-1}\frac{j\,\varphi_j}{2j{+}3}\;>\;0`,

hence `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)`, **not merely `O(1/n)`**; while at
`K=1`, `c_1=0` and `\varphi_n^{(1)}-\varphi_1=1/(3n^2)` exactly, so the rate
there is `\Theta(1/n^2)`. Together these determine the leading-order rate for
**every** `K\ge1`.

**3. Wording cautions for whoever writes the entry** (these matter — the wave-8
review's issue I-4 arose from exactly this kind of quantifier slip):

- Never write "`c_K>0` for every `K\ge1`". `K=1` is an **exact equality case**
  (`v_1=3\varphi_1=2` exactly), not an approximation. `K=0` likewise.
- Keep "for every **fixed** `K\ge2`" on the `\Theta(1/n)` statement. No
  uniformity in `K` is proved, and none is claimed by the target.
- The `\Theta(1/n^2)` statement at `K=1` is an upstream fact (wave 5 /
  wave-8 §A.7), not this document's; I re-confirmed it independently
  (`n=2..40`, exact), but it should be attributed upstream.

**4. Worth recording separately: Lemma 1 is a new standalone fact.**
`F_{K-1}(1,1)=[(2K{+}1)\varphi_K-1]/(2K)` is the companion, one rung over in
`b`, to `k6_attempt` §2.3's already-recorded `F_r(1,0)=\varphi_r`. Nothing
upstream needed or noticed it, and it is the entire reason the two-ingredient
expression `c_K` collapses to one ingredient. It deserves a line of its own,
independent of the positivity question.

**5. Also worth a line:** `c_K` is strictly increasing in `K` on `K\ge1`, so
`c_K\ge c_2=1/30` for every `K\ge2` (a uniform positive floor), and
`c_K=\sqrt{\pi K}/8-\frac12+O(K^{-1/2})\to\infty`.

**6. What must NOT change.** The other four open items are untouched and remain
open exactly as Estágio 6 states them: (i) the all-orders general-`K` closed
form; (ii) the growth in `r` of the error constants `D_r(b),C_r(b)`;
(iv) the locally-uniform-in-`c` version of Teorema 3; (v) Conjecturas 1–2.
I verified the target's §8 list against Estágio 6's list item by item: it is
Estágio 6's list minus item (iii), exactly as the document claims. Teorema 3
itself is unaffected (it never depended on this front).

**7. On the notes.** N-1 … N-4 are presentational and require no addendum to
the target document. If the archive's convention is to record referee notes
regardless, a single dated line pointing at this report's §E suffices; unlike
the wave-8 review's I-1, nothing here needs a text correction.

---

# G. Summary of what I checked

| # | Item | Method | Result |
|---|---|---|---|
| 1 | Lemma 1 | hand derivation; 4 independent numeric routes `K=1..50`; symbolic `K` via gamma | **confirmed, 0 discrepancies** |
| 1a | `(K{-}1{-}k)+(K{+}k{+}1)=2K` constant in `k` | symbolic in `k` and `K` | **exact identity, not approximate** |
| 1b | `\sum_{j=K+1}^{2K}\binom{2K}j=(4^K-\binom{2K}K)/2` | re-derived from binomial theorem + row symmetry; exact for 64 values of `K` | **confirmed** |
| 2 | Theorem A `c_K=[(K{+}2)\varphi_K-2]/4` | hand; symbolic in `K` and `\varphi` | **confirmed, no sign error** |
| 3 | `\varphi_{K+1}/\varphi_K=(2K{+}2)/(2K{+}3)` | hand from `4^K(K!)^2/(2K{+}1)!`; symbolic; `K=0..300` | **confirmed** |
| 4 | `2(K{+}1)(K{+}3)-(K{+}2)(2K{+}3)=K`; `v_1=3\varphi_1=2` | symbolic expansion; exact `Fraction` | **confirmed, exact** |
| 5 | Induction validity / off-by-one | boundary trace at `K=1\to2`; literal machine induction `K=1..1500` | **valid, no off-by-one** |
| 6 | Corollary B′ telescoping sum | hand; `c_4=23/210` both ways; `K=1..50` + large `K` | **confirmed, matches worked example** |
| 7 | §4.4 second proof; `\binom{2K}K\le4^K/\sqrt{3K{+}1}`; cubic identity | ratio re-proof; exact integer check for 204 values of `K`; symbolic | **confirmed; equality exactly at `K=0,1`** |
| 8 | RAW-definition numerics `K=1..50`, `K=100..5000`; `K=1..3000` sweep | exact `Fraction` | **positive for all `K\ge2`, `c_1=0`, no counterexample** |
| 8a | Quoted fractions `c_6=1093/6006`, `c_9=11773/41990` | exact, from raw definition | **both confirmed** |
| 8b | All 85 cells of the §3 table | exact recomputation | **0 bad cells** |
| 9a | Hidden sign assumption | step-by-step audit | **none found** |
| 9b | `K=1` equality exact, not float | `Fraction` equality; full sweep `K=0..3000` | **exact; solution set `\{0,1\}`** |
| 9c | `c_K\sim\sqrt{\pi K}/8` and the 3-term expansion | independent derivation; 60-digit `mpmath` to `K=10^7` | **correct, incl. `13\sqrt\pi/64`** |
| 10 | Honesty / scope / label audit | grep of every quantifier; re-run of all 3 scripts; log vs. text | **accurate throughout** |
| — | Transcription guard (§6) re-done | my own raw `(a,b,r)` chain + Reduction Lemma A, exact fit, out-of-sample | **`\alpha_1=c_K` exactly, `K=1..9`** |
| — | **My own predictions beyond the target** | `K=10,11,12` rate coefficients + degree `K{+}1` | **all three confirmed exactly** |

**Total: 0 discrepancies, 0 counterexamples, 0 failed break attempts.**

---

*Reproduce from this directory:*

```
python3 ref_01_raw_ck.py
python3 ref_02_symbolic.py
python3 ref_03_asymptotics.py
python3 ref_04_table_and_finite_n.py
python3 ref_05_break_attempts.py
```

*(`ref_02` ends with a sympy `PoleError` on its final block: sympy 1.14 has no
gamma-at-infinity asymptotic series. That is a library limitation, not a failed
check — every S-check before it passes, and the asymptotic question it was
attempting is settled independently and to higher precision in `ref_03`, whose
result is recorded in §C.4. The `.log` retains the traceback verbatim rather
than hiding it.)*
