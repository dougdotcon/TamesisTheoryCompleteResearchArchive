# Qualitative geometric growth of `M_K`, proved — Teorema E's named gap closed by a route that bypasses `D_r(b)`/Proposição 6 entirely

> **Governance.** Wave 12, front (a), authorized by `DISC-DEC-051`
> (`MK-QUALITATIVE-GEOMETRICITY-ATTEMPT`). Target: the single obstruction
> named by `uniform_in_c_attempt/adversarial/REFEREE_REPORT.md` §6.2 (F-1) —
> a written-down proof that `|n(φ_n^{(K)}-φ_K)| ≤ M_K` for some
> `M_K = O(λ^K)` (any finite `λ`), which is exactly what `uniform_in_c_attempt/ATTEMPT.md`
> Teorema E (§5.6) needs to drop its `PROVED-MODULO` label. Pure combinatorial
> / asymptotic mathematics — no external data, no holdout, no real-world
> claim, no governance edits. **Nothing outside this directory was modified.**
> No git commit was made. Every claim below is labeled PROVED, NUMERICALLY
> VERIFIED, or (for the one part deliberately not pursued) OPEN.

> **Executive summary (read first).** The attempt **succeeds**, but not via
> the route the referee sketched. The referee's own "Constructive note"
> (§6.2 of `uniform_in_c_attempt/adversarial/REFEREE_REPORT.md`) proposed
> unrolling Estágio 8's Proposição 6 recursion for `C'_r(b)`, using the crude
> bound `F_r(2,0) = O(2^r)` from Lemma 7. That arithmetic **is verified here**
> (§3) and is correct — but carrying it through to `M_K` turns out to require
> a closed-form geometric bound on `A_r(b), B_r(b)` **for general `b`**, which
> is not established anywhere in the archive (the parent document's own
> scorecard lists it as "NOT ATTEMPTED") and was judged, after inspection, to
> be a substantial separate undertaking, not a short unrolling exercise. This
> document instead finds and proves a **different, more direct route** (§2)
> that reaches the same target using an ingredient that did not exist when
> Estágio 8/10 were written: Estágio 9's exact, all-orders, closed-form
> `ψ_n^{(K)}` (Corolário A1, PROVED unconditionally, adversarially verified
> with zero surviving findings against it). That closed form makes `M_K`
> directly computable and boundable by elementary calculus — no `D_r(b)`, no
> `A_r(b)`/`B_r(b)`, no Proposição 6 needed at all:
>
> > **Theorem (qualitative geometric growth of `M_K`, PROVED).**
> > `M_K := \sup_{n\ge K+1}|n(φ_n^{(K)}-φ_K)| \le φ_K(K{+}1)e^{K/2} + K =
> > O(K\cdot(\sqrt e)^K)`. In particular `M_K = O(λ^K)` with `λ=\sqrt e\approx
> > 1.6487` (any larger `λ` also works, and by the referee's own remark
> > (§6.1) the specific value is irrelevant to Teorema E). Consequently
> > `Σ_K c^K M_K/K! < ∞` for **every** `c\ge0`, and **Teorema E's named gap
> > is closed**: the `A_n(c)` half of `nΔ_n(c)` may be taken to the limit
> > term-by-term by dominated convergence.
>
> The proof (§2) is three elementary, fully rigorous steps built on two
> already-PROVED archive facts (Estágio 9's Corolário A1; the Reduction Lemma
> A of Estágio 3) plus two textbook inequalities (`1+x\le e^x`; positivity of
> elementary symmetric polynomials of positive reals). Every step is verified
> independently and exactly in §3–§5 (own scripts, exact `Fraction`/`sympy`
> arithmetic, no code reused from any sibling directory).
>
> **A striking bonus finding (§5, purely informational, not needed for the
> proof):** the true growth of `M_K` looks nothing like geometric —
> numerically it tracks `Θ(\sqrt K)`, the *same order* as the already-PROVED
> `n\to\infty` limit `Kφ_K/4` (Estágio 6). The crude bound above is valid but
> enormously loose (ratio to the true value already `>10^{19}` at `K=300`) —
> the same qualitative pattern Estágio 8 found for `D_r(b)` vs `D^*_r(b)`. If
> `M_K=Θ(\sqrt K)` is ever proved, it would be a *much* stronger closure than
> Teorema E needs; that is explicitly **not attempted or claimed** here.
>
> **This is a positive result and therefore requires the archive's mandatory
> adversarial reproduction before being catalogued.** I do not claim victory
> in the sense of "integrated" — that is not this document's call to make.
> §6 states the scorecard precisely; §7 names exactly what a hostile referee
> should attack first.

---

## 0. Disciplina

**Sources read, in the order the task mandated, before any code was
written** (full detail, not just filenames):

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-051`
   — the exact authorization language for `MK-QUALITATIVE-GEOMETRICITY-ATTEMPT`,
   including the referee's boxed recursion `C'_r(b) ≤ (B_r(b)+A_r(b+1)) +
   2C'_{r-1}(b+1)` quoted verbatim in the ledger entry.
2. `.../u12_universality/theorem/THEOREM.md`, `[Extensão, Estágio 6]` through
   `[Extensão, Estágio 10]` in full — Teorema 3 (Estágio 6), the exact rate
   `c_K` (Estágio 7), the exact error-constant closed form and Proposição 6
   (Estágio 8), the all-orders closed form and Corolário A1 (Estágio 9), and
   Teoremas A/C/D/E and the precisely-named `M_K` gap (Estágio 10).
3. `.../k_general_existence_attempt/error_constant_growth_attempt/ATTEMPT.md`
   in full (840 lines) — Lemma 7's exact statement/proof (§6.2), Proposição 6's
   exact boxed recursion (§6.1), its "PROVED bound; rate NUMERICALLY
   CHARACTERIZED" status (§6.3 table, scorecard row 15/16), and its own §8.3
   open-items list (item 1: "closed-form for `A_r(b), B_r(b)`" not attempted).
4. `.../error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` — read
   for context on how Proposição 6 itself was verified by the wave-8 referee
   (confirmed the recursion's rigor, not its geometricity).
5. `.../k_general_existence_attempt/ATTEMPT.md` §2–§6 — the exact definitions
   of `A_r(b)` (§4, the Taylor-tail coefficient-sum bound), `B_r(b)` (§6, the
   `h_r`-substitution constant), `D_r(b)` (§5), `C_r(b)` (§6, including the
   original, un-improved recursion `C_r(b)=B_r(b)+rC_{r-1}(b{+}1)+2D_r(b{+}1)`)
   — needed to confirm precisely what Proposição 6 improves and why a
   general-`b` bound on `A_r(b),B_r(b)` is a separate, non-trivial gap (scorecard
   row 7 there: "closed-form … `A_r(b)` … NOT ATTEMPTED").
6. `.../error_constant_growth_attempt/all_orders_closed_form_attempt/` — via
   `THEOREM.md` Estágio 9's summary (the source file itself was not re-read
   line-by-line beyond what Estágio 9 quotes, since Estágio 9's PROVED,
   adversarially-verified Corolário A1 statement is exact and self-contained;
   its **use** here is checked independently in §3/§4 against known target
   values by fresh code, not by re-reading its derivation).
7. `.../uniform_in_c_attempt/ATTEMPT.md` in full (971 lines), especially §5.3
   (`A_n`, the exact rate `c_K` recalled), §5.6 (Teorema E, the `M_K` gap
   stated precisely: `|ψ_n^{(K)}-φ_K-\frac{Kφ_K}{4n}|\le D_K(0)/n^2` plus
   Reduction Lemma A gives `M_K\le\frac{5K}4+D_K(0)`), and its
   `[Correção pós-adversarial, 2026-08-23]` blockquote (the corrected gap
   statement this front directly answers).
8. `.../uniform_in_c_attempt/adversarial/REFEREE_REPORT.md` §6 in full
   (§6.1–§6.5) — the source of the "Constructive note" (§6.2) quoted in the
   ledger; read in full, not just the excerpt, including §6.3's `K=n` nit and
   §6.5's exact (`φ_n^{(n-1)}=φ_n^{(n)}=Q(n)/n`) strengthening (both
   unrelated to this front's target but read for completeness as instructed).
9. `.../k2_open_lemma/k3_attempt_2/ATTEMPT.md` §0/§1 — the exact statement of
   Reduction Lemma A (`φ_n^{(K)}=(K/n)ψ_n^{(K),R}+(1-K/n)ψ_n^{(K)}`) and, most
   importantly for this document, the **definitions**: `ψ_n^{(K)} :=
   P(K{+}1\text{ cyclic})`, `ψ_n^{(K),R} := P(1\text{ cyclic})` — both
   **literally probabilities**, hence in `[0,1]` by definition, not by any
   further argument.

**Reuse policy.** Every script in this directory (`verify_corollary_a1.py`,
`verify_monotonicity.py`, `compute_MK.py`, `explore_true_rate.py`,
`route_b_arithmetic.py`) was written from scratch. Corolário A1's closed
form is re-transcribed from its stated formula (`THEOREM.md` Estágio 9) and
used as the starting object of §2's derivation — this is the one "reuse" in
the sense every predecessor document in this lineage reuses already-PROVED
formulas; it is not re-derived here, but it **is** independently checked
against five other already-PROVED, independently-derived closed forms
(`ψ_n^{(1)},\dots,ψ_n^{(4)}` exactly, `ψ_n^{(5)}`'s `1/n^2` coefficient) in
§3, by fresh `sympy` code. The five target closed forms themselves were
transcribed only as **targets to reproduce**, exactly the convention used by
every predecessor in this lineage.

**Exactness policy.** `fractions.Fraction` / `sympy.Rational` /
`sympy.Symbol` throughout for every claim labeled PROVED, "exact", or
"identity". Floating point / `mpmath` (60–80 dps) appears only in: (a)
display columns; (b) `explore_true_rate.py`, which is explicitly
**informational context, not part of the proof** (flagged as such in the
file header and throughout); (c) `compute_MK.py`'s bound-vs-value comparison
table, where the crude bound `φ_K(K{+}1)e^{K/2}` is irrational and evaluated
at 60 dps, cross-checked against a second, independent `mpmath`-only
recomputation of `M_K^ψ` itself (not just the bound) — 0 relative
discrepancy `>3\times10^{-61}` at `K=50,150,300` (§4).

**Timestamps.** `DERIVATION_PREREG.md` was written and saved at
`2026-08-23T13:19:42Z`, **before** any script existed or any numeric value
was computed (`ls -la --time-style=full-iso` confirms every `.py`/`.log`
file in this directory postdates it).

**No randomness.** No Monte Carlo or randomized simulation was used or
needed — every check below is exact combinatorial/symbolic arithmetic or
deterministic high-precision evaluation. The wave-12 seed range
(`numpy.random.SeedSequence` from `20260825800`) was reserved by governance
but **no seed was drawn**, since nothing here is randomized. (Seed table:
none.)

---

## 1. The target, restated precisely

`uniform_in_c_attempt/ATTEMPT.md` §5.6, Teorema E:

> For every `c\ge0`, `nΔ_n(c)\to e(c)`, and `n\sup_{[0,C]}|Δ_n|\to
> \sup_{[0,C]}|e|`.

Status: `PROVED-MODULO-[K\text{-uniform domination}]`. The `A_n(c)` half of
`nΔ_n(c)=nA_n(c)+nB_n(c)` is `Σ_{K=0}^n b_K(c)\cdot n(φ_n^{(K)}-φ_K)`, a sum
whose term count grows with `n`; moving `n\to\infty` inside it legitimately
requires — this was independently reconfirmed correct by the wave-11 referee,
`adversarial/REFEREE_REPORT.md` §6.1, "yes, Teorema E really does need what
the document says it needs" — a bound

`|n(φ_n^{(K)}-φ_K)| \le M_K` for every valid `n`, with `Σ_K c^K M_K/K! <
∞`  (using `b_K(c)\le c^K/K!`, already proved).

Since `Σ_K c^Kλ^K/K! = e^{cλ}<∞` for **any** finite `λ`, this reduces to:
does `M_K = O(λ^K)` hold for some finite `λ`? (The value of `λ` is
irrelevant — the referee's own point, §6.2.) This is the sole target of this
document.

**Precise definition used throughout.**
`\displaystyle M_K := \sup_{n\ge K+1}\big|n\big(φ_n^{(K)}-φ_K\big)\big|`
(the domain `n\ge K+1` is the natural one — it is the domain on which
`ψ_n^{(K)}`, and hence, via Reduction Lemma A, `φ_n^{(K)}`, is defined by the
closed forms this document uses; the excluded case `K=n` is handled
separately and is harmless, exactly as the referee's F-12 nit already notes,
§6.3 of `adversarial/REFEREE_REPORT.md`: `b_n(c)\cdot n|φ_n^{(n)}-φ_n|\le
(c/n)^n\cdot n\to0` super-exponentially, so it contributes `0` to the
relevant limit regardless of what `M_n` itself does).

---

## 2. The proof (Route A)

### 2.1 Step 1 — the exact closed form, restated

Estágio 9's Corolário A1 (`THEOREM.md`, PROVED unconditionally, all `n\ge
K{+}1`, adversarially verified with **215,070** exact checks and zero
surviving findings against the theorem itself):

`\displaystyle ψ_n^{(K)} = \frac{φ_K}{4^K}\sum_{j=0}^{K}\binom{2K{+}1}{K{-}j}\,\frac{(n{+}j)!}{n!\,n^j}`.

Write `g(j;n):=\prod_{i=1}^j\big(1+\tfrac in\big)=(n{+}j)!/(n!\,n^j)`
(empty product `=1` at `j=0`). Since
`\sum_{j=0}^K\binom{2K+1}{K-j}=\sum_{i=0}^K\binom{2K+1}i=2^{2K}` (the classical
odd-`N` half-sum identity, re-derived and checked in §5 of
`route_b_arithmetic.py` below), `ψ_n^{(K)}\to φ_K` as `n\to\infty` is
recovered as the `g\to1` limit, consistently.

`\displaystyle n\big(ψ_n^{(K)}-φ_K\big) = \frac{φ_K}{4^K}\sum_{j=0}^K\binom{2K{+}1}{K{-}j}\,f_j(n)`,  `\quad f_j(n):=n\big[g(j;n)-1\big]`.

### 2.2 Step 2 — `f_j(n)` is exactly a positive combination of powers of `1/n`, hence nonincreasing; sup at `n=K+1`

Expand `g(j;n)=\prod_{i=1}^j(1+i/n)=\sum_{k=0}^je_k(1,\dots,j)\,n^{-k}`, `e_k`
the `k`-th elementary symmetric polynomial of `\{1,\dots,j\}` (`e_0=1`).
Every `e_k(1,\dots,j)>0` for `1\le k\le j` (elementary symmetric polynomials
of positive reals are sums of positive products). Hence

`\displaystyle f_j(n) = \sum_{k=1}^j \frac{e_k(1,\dots,j)}{n^{k-1}} = e_1(j) + \frac{e_2(j)}n + \frac{e_3(j)}{n^2}+\cdots`

is a sum of `e_1(j)\ge0` (constant in `n`) plus **strictly positive**,
**strictly decreasing** functions of `n` (for `j\ge2`; `f_0\equiv0`,
`f_1\equiv1` constant). So `f_j(n)` is nonincreasing in `n` for every `j`,
strictly decreasing for `j\ge2`. Since `n(ψ_n^{(K)}-φ_K)` is a
**nonnegative-weighted sum** (`\binom{2K+1}{K-j}\ge0`) of the `f_j(n)`, each
individually maximized at the **same** point — the smallest valid `n`,
namely `n=K{+}1` — the whole sum is too:

`\displaystyle M_K^ψ := \sup_{n\ge K+1} n\big(ψ_n^{(K)}-φ_K\big) = (K{+}1)\big(ψ_{K+1}^{(K)}-φ_K\big)`,

attained exactly at `n=K{+}1`, and `n(ψ_n^{(K)}-φ_K)\ge0` always (so `M_K^ψ`
really is the sup of the absolute value too). This is a **fully rigorous,
closed-form** version of the phenomenon `error_constant_growth_attempt/ATTEMPT.md`
§5.3 could only verify numerically for its (different, second-order) quantity
`S_r(b)` ("attained at the minimal state `n=m=b{+}r{+}1`") — here it is a
three-line algebraic consequence of positivity of elementary symmetric
polynomials, for the specific first-order quantity `n(ψ_n^{(K)}-φ_K)` needed.

### 2.3 Step 3 — the crude geometric bound

At `n=K{+}1`, for `0\le j\le K`: `1+i/n\le e^{i/n}` (`1+x\le e^x`), so
`g(j;K{+}1)\le\exp\big(\sum_{i=1}^ji/(K{+}1)\big)=\exp\big(\tfrac{j(j+1)}{2(K+1)}\big)
\le\exp(K/2)` (using `j(j{+}1)\le K(K{+}1)` for `j\le K`). Hence
`f_j(K{+}1)=(K{+}1)[g(j;K{+}1)-1]\le(K{+}1)e^{K/2}`, and, using
`\sum_j\binom{2K+1}{K-j}=2^{2K}` again:

`\displaystyle M_K^ψ = \frac{φ_K}{4^K}\sum_j\binom{2K{+}1}{K{-}j}f_j(K{+}1) \le \frac{φ_K}{4^K}\cdot(K{+}1)e^{K/2}\cdot2^{2K} = φ_K\,(K{+}1)\,e^{K/2}`.

`φ_K\le1` for every `K\ge0` (Wallis mean), so `M_K^ψ\le(K{+}1)e^{K/2}` —
geometric, `λ=\sqrt e`.

### 2.4 Step 4 — from `ψ_n^{(K)}` to `φ_n^{(K)}`: the Reduction Lemma A

Reduction Lemma A (`k2_open_lemma/k3_attempt_2/ATTEMPT.md` §0/§2, PROVED,
`K` general): `φ_n^{(K)}=(K/n)ψ_n^{(K),R}+(1-K/n)ψ_n^{(K)}` exactly. Algebra
(subtract `φ_K`, multiply by `n`):

`\displaystyle n\big(φ_n^{(K)}-φ_K\big) = n\big(ψ_n^{(K)}-φ_K\big) + K\big[ψ_n^{(K),R}-ψ_n^{(K)}\big]`.

Both `ψ_n^{(K)}:=P(K{+}1\text{ cyclic})` and `ψ_n^{(K),R}:=P(1\text{
cyclic})` are **literally probabilities** by their own definition
(`k3_attempt_2/ATTEMPT.md` §0), hence both in `[0,1]`, hence
`|ψ_n^{(K),R}-ψ_n^{(K)}|\le1`. So:

`\displaystyle M_K = \sup_n|n(φ_n^{(K)}-φ_K)| \le M_K^ψ + K \le φ_K(K{+}1)e^{K/2}+K`.

### 2.5 Conclusion

`\displaystyle M_K \le φ_K(K{+}1)e^{K/2}+K = O\big(K\cdot(\sqrt e)^K\big)`,
i.e. `M_K=O(λ^K)` for `λ=\sqrt e\approx1.6487` (any larger `λ` too). Hence
`Σ_Kc^KM_K/K!\le\sum_Kc^K[(K{+}1)e^{K/2}+K]/K!<\infty` for **every**
`c\ge0` — Teorema E's named hypothesis, closed, unconditionally, without
reference to `D_r(b)`, `A_r(b)`, `B_r(b)`, or Proposição 6 at all.

---

## 3. Independent verification, exact

### 3.1 Corolário A1 vs five independently-PROVED closed forms (R1)

`verify_corollary_a1.py` (fresh `sympy`, symbolic in `n`) checks Corolário
A1's formula against the wave-5/6 hand-derived `ψ_n^{(1)},ψ_n^{(2)}`, the
`k3_attempt_2` Markov-chain-derived `ψ_n^{(3)},ψ_n^{(4)}`, and `ψ_n^{(5)}`'s
`1/n^2` Taylor coefficient — **all five match exactly** (`sympy.simplify` of
the difference `=0`), plus the `n\to\infty` limit reproduces `φ_K` exactly
for `K=0,\dots,8`, plus `ψ_n^{(0)}\equiv1` identically.
(`verify_corollary_a1.log`.)

### 3.2 The elementary-symmetric-function monotonicity claim (R2)

`verify_monotonicity.py`, three parts, all exact:

- (a)/(b) the identity `f_j(n)=\sum_ke_k(1,\dots,j)n^{-(k-1)}` and positivity
  of every `e_k(1,\dots,j)` — checked symbolically (`sympy`) for `j=0,\dots,14`,
  all match, all positive;
- (c) `f_j(n)` nonincreasing in `n` — exhaustive exact (`Fraction`) grid,
  `j=0,\dots,60`, `n=j{+}1,\dots,j{+}300`: **18,299 consecutive pairs
  checked, 0 violations**;
- (d) `n(ψ_n^{(K)}-φ_K)` nonincreasing in `n`, nonnegative, argmax at
  `n=K{+}1` — exhaustive exact grid, `K=1,\dots,40`, `n=K{+}1,\dots,K{+}200`:
  **7,960 consecutive pairs, 0 violations; 0 negative values across the
  entire grid; argmax at `n=K{+}1` in all 40 of 40 cases**.

(`verify_monotonicity.log`.)

### 3.3 `M_K^ψ` exactly, and the crude bound (R3)

`compute_MK.py` computes `M_K^ψ=(K{+}1)(ψ_{K+1}^{(K)}-φ_K)` **exactly**
(`Fraction`) for `K=1,\dots,300`, and checks `M_K^ψ\le φ_K(K{+}1)e^{K/2}`
(the latter evaluated at 60 `mpmath` dps from the exact `φ_K`): **0
violations across all 300 values of `K`.** Independent cross-check: a
second, wholly separate `mpmath`-only recomputation (not reusing the exact
`Fraction` code path) of `M_K^ψ` at `K=50,150,300` agrees with the exact
value to relative error `\le3\times10^{-61}`. (`compute_MK.log`.)

### 3.4 Route B's arithmetic, verified independently (R-B, as the task required)

`route_b_arithmetic.py` independently checks the referee's cited arithmetic
(ledger `DISC-DEC-051`, "the crude bound `Σ_{i≤r}C(2r+1,i)≤2^{2r+1}` already
yields `F_r(2,0)≤2φ_r·2^r=O(2^r)`"):

- the exact half-sum identity `\sum_{i=0}^rC(2r{+}1,i)=2^{2r}` (**not** just
  `\le2^{2r+1}`) — verified exactly for `r=0,\dots,59`, plus a one-line
  symmetry proof recorded (binomial theorem at `x=1`, then the fixed-point-free
  involution `i\mapsto2r{+}1{-}i` on `\{0,\dots,2r{+}1\}` splits the sum into
  two equal halves since `2r{+}1` is odd);
- this gives a **sharper** crude bound than the ledger's own,
  `F_r(2,0)\le φ_r\cdot2^r` (not `2φ_r\cdot2^r`) — both bounds verified
  exactly, `r=0,\dots,40`, **0 violations**;
- as expected for a deliberately crude bound, it is far from tight: the ratio
  `F_r(2,0)/(φ_r2^r)\to0` (the true rate is `\Theta((9/8)^r)`, base `9/8<2`)
  — consistent with, not contradicting, everything already on record in
  `error_constant_growth_attempt/ATTEMPT.md` §6.2.

(`route_b_arithmetic.log`.) **This is as far as Route B was carried** — see
§4 for why steps (b)/(c) (unrolling Proposição 6 with general-`b` bounds on
`A_r(b),B_r(b)`) were not attempted, now that Route A has closed the target
on its own.

---

## 4. Route B (the referee's sketch): what was checked, what was not, and why

The referee's "Constructive note" sketch has three pieces (§6.2 of
`uniform_in_c_attempt/adversarial/REFEREE_REPORT.md`, quoted in the ledger):
(a) `F_r(2,0)=O(2^r)` from Lemma 7 — **verified above, §3.4, and correct**;
(b) unroll Proposição 6's recursion,
`C'_r(b)\le(B_r(b)+A_r(b{+}1))+2C'_{r-1}(b{+}1)` — **verified algebraically**
below; (c) connect the result to the actual `M_K` — **not carried through**,
for the reason given.

**Step (b), the algebra.** Proposição 6's boxed recursion
(`error_constant_growth_attempt/ATTEMPT.md` §6.1) is
`D'_r(b):=[rC'_{r-1}(b)+A_r(b)]/(r{+}b{+}1)`,
`C'_r(b):=B_r(b)+\frac r{b+r+1}C'_{r-1}(b{+}1)+D'_r(b{+}1)`. Substituting
`D'_r(b{+}1)=[rC'_{r-1}(b{+}1)+A_r(b{+}1)]/(r{+}b{+}2)` into the second line:

`C'_r(b) = B_r(b) + \frac{A_r(b{+}1)}{r{+}b{+}2} + C'_{r-1}(b{+}1)\Big[\frac r{b{+}r{+}1}+\frac r{r{+}b{+}2}\Big]`.

Since `b\ge0\Rightarrow r/(b{+}r{+}1)<1` and `r/(r{+}b{+}2)<1`, dropping the
denominator on the `A_r(b{+}1)` term (`\le A_r(b{+}1)`) gives exactly the
ledger's quoted `C'_r(b)\le(B_r(b){+}A_r(b{+}1))+2C'_{r-1}(b{+}1)`. **This
algebra checks out** — it is a correct, one-line consequence of the boxed
recursion, exactly as the referee describes.

**Step (c), why it was not carried through.** Unrolling `C'_K(0)` down to
the base case `C'_0=0` forces `r+b=K` invariant at every level (`r=K{-}j`,
`b=j`, `j=0,\dots,K{-}1`), so a bound on `C'_K(0)` of the referee's sketched
form needs `\max_{r+b=K}A_r(b)` and `\max_{r+b=K}B_r(b)` — i.e. **general-`b`**
bounds on `A_r(b), B_r(b)`, not just the `b=0` case Lemma 7 addresses via
`F_r(2,0)`. `A_r(b)` is the coefficient-sum norm of a Taylor-tail polynomial
built from **derivatives** of `F_r(\cdot,b), G_r(\cdot,b), \hat H_{r-1}(\cdot,b),
K_{r-1}(\cdot,b)` (`k_general_existence_attempt/ATTEMPT.md` §4); `B_r(b)` is
similarly built (§6 there). Neither has a published closed form for general
`b` anywhere in the archive — `error_constant_growth_attempt/ATTEMPT.md`'s
own scorecard row 7 lists "Closed-form expressions for `D_r(b),C_r(b),A_r(b)`
for general `r`" as **NOT ATTEMPTED**, and this document's own reading found
no route to a coefficient-sum-norm bound on the relevant *derivative*
polynomials that is both (i) rigorous (not just numerically observed, as
`F_r(2,0)`'s asymptotic rate itself is only "NUMERICALLY CHARACTERIZED,
mechanism proved" per that document's own §6.3 status table) and (ii) valid
uniformly as `b` ranges over `0,\dots,K{-}1` while `r` ranges over
`K,\dots,1`. A naive derivative-norm bound (`\|p^{(k)}\|\le[d!/(d{-}k)!]\|p\|`
for a degree-`d` polynomial `p`) reintroduces a **factorial-in-`r`** factor —
exactly the kind of looseness Proposição 6 was designed to remove — so it
cannot be used without a sharper, Lemma-7-style sign-alignment argument for
the *derivative* polynomials specifically, which was not found. **This is
reported as OPEN, not refuted** — the sketch's algebra (steps a, b) is
correct as far as it goes; whether a genuinely general-`b` geometric bound on
`A_r(b),B_r(b)` exists is a separate, unresolved question that this document
does not need to answer, because Route A closes the actual target
independently. No further time was spent on it once Route A's proof (§2) was
complete and verified (§3), per the pre-registered plan (`DERIVATION_PREREG.md`
§2, "Route B will be reported as far as it goes; if Route A succeeds, Route B
is not required to close").

---

## 5. Bonus finding (informational, not part of the proof): the true rate looks like `Θ(√K)`, not geometric at all

`explore_true_rate.py` (`mpmath`, 80 dps) tracks `M_K^ψ/\sqrt K` and
`M_K^ψ/(Kφ_K/4)` (the ratio to the already-PROVED `n\to\infty` limit,
Estágio 6) for `K` up to `3000`:

| `K` | `M_K^ψ` | `M_K^ψ/\sqrt K` | `Kφ_K/4` | `M_K^ψ/(Kφ_K/4)` |
|---|---|---|---|---|
| 10 | 0.8795 | 0.2781 | 0.6757 | 1.302 |
| 100 | 3.3549 | 0.3355 | 2.2073 | 1.520 |
| 1000 | 11.2806 | 0.3567 | 7.0036 | 1.611 |
| 3000 | 19.7761 | 0.3611 | 12.1336 | 1.630 |

Both ratios are slowly converging (to constants somewhere near `0.37`–`0.4`
and `1.7`–`1.8` respectively, on this trend), consistent with `M_K^ψ=\Theta(\sqrt
K)` — the **same order** as the leading-order limit `Kφ_K/4\sim\sqrt{\pi
K}/4` itself, meaning the "excess" the supremum-over-`n` adds beyond the
`n\to\infty` limit is only a **bounded multiplicative factor**, not a new
growth order. (An initial attempt to extend this table to `K=10^4,3\times10^4`
was abandoned — see `explore_true_rate.py`'s header comment — as the naive
per-`K` recomputation of multi-thousand-digit binomial coefficients from
scratch made it too slow to finish in reasonable wall-clock time; this is a
performance limitation of the exploratory script, not a mathematical
obstruction, and does not affect the trend already visible in `K\le3000`.)

**This is emphatically not proved here and is not needed** — §2's proof only
needs *some* geometric bound, which is established unconditionally. It is
recorded because, exactly as `error_constant_growth_attempt/ATTEMPT.md` did
for `D_r(b)` vs `D^*_r(b)`, honesty about how loose a crude-but-sufficient
bound is seems valuable context for whoever picks this up next, and because
if `M_K=\Theta(\sqrt K)` (or even just `M_K=O(\text{poly}(K))`) is ever
proved, it would make the domination argument for Teorema E far more
comfortable than merely "geometric" — but that is a strictly harder,
separate claim, explicitly not attempted or claimed here.

---

## 6. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Corolário A1's closed form reproduces `ψ_n^{(1)},\dots,ψ_n^{(4)}` exactly, `ψ_n^{(5)}`'s `1/n^2` coefficient, the `n\to\infty\to φ_K` limit `K=0..8`, and `ψ_n^{(0)}\equiv1` | **PROVED** (exact `sympy` symbolic-in-`n` match, §3.1, `verify_corollary_a1.log`) |
| 2 | `f_j(n)=\sum_ke_k(1,\dots,j)n^{-(k-1)}`, every `e_k(1,\dots,j)>0` | **PROVED**, elementary (positivity of elementary symmetric polynomials of positive reals); symbolically re-confirmed `j=0..14` (§3.2) |
| 3 | `f_j(n)` nonincreasing in `n`; `n(ψ_n^{(K)}-φ_K)` nonincreasing in `n`, `\ge0`, sup at `n=K{+}1` | **PROVED**, algebraic consequence of claim 2; exhaustively confirmed exact, 0 violations over 18,299 + 7,960 checked pairs, argmax correct in 40/40 tested `K` (§3.2) |
| 4 | `M_K^ψ:=(K{+}1)(ψ_{K+1}^{(K)}-φ_K)\le φ_K(K{+}1)e^{K/2}` | **PROVED**, elementary (`1+x\le e^x` termwise + the exact half-sum identity `\sum_i\binom{2K+1}i=2^{2K}`); confirmed exact for `K=1..300`, 0 violations (§3.3) |
| 5 | `n(φ_n^{(K)}-φ_K)=n(ψ_n^{(K)}-φ_K)+K[ψ_n^{(K),R}-ψ_n^{(K)}]`, and `|ψ_n^{(K),R}-ψ_n^{(K)}|\le1` | **PROVED** — pure algebra on the already-PROVED Reduction Lemma A, plus `ψ_n^{(K)},ψ_n^{(K),R}\in[0,1]` **by their own definition** as probabilities (§2.4) |
| 6 | **`M_K\le φ_K(K{+}1)e^{K/2}+K = O(K(\sqrt e)^K)` — qualitative geometric growth of `M_K`** | **PROVED**, given claims 1–5 (§2.5) |
| 7 | `Σ_Kc^KM_K/K!<\infty` for every `c\ge0` — Teorema E's named domination hypothesis | **PROVED**, immediate corollary of claim 6 |
| 8 | Route B step (a): `F_r(2,0)\le φ_r2^r` (sharper than the ledger's `2φ_r2^r`, both valid), and the exact half-sum identity underlying it | **PROVED**, exact, `r=0..59`/`r=0..40` (§3.4) |
| 9 | Route B step (b): the unrolled inequality `C'_r(b)\le(B_r(b)+A_r(b{+}1))+2C'_{r-1}(b{+}1)` follows algebraically from Proposição 6's boxed recursion | **PROVED**, one-line algebra (§4) |
| 10 | Route B step (c): a general-`b` geometric bound on `A_r(b),B_r(b)`, needed to finish Route B | **OPEN** — not established anywhere in the archive; not attempted further here since Route A (claim 6) closes the actual target independently (§4) |
| 11 | (Informational) `M_K^ψ=\Theta(\sqrt K)$, same order as the `n\to\infty` limit `Kφ_K/4` | **NUMERICALLY CHARACTERIZED** only, `K\le3000`, not proved, not needed, not claimed as a result (§5) |
| 12 | Independent adversarial re-verification of this document | **NOT PERFORMED** — required before any integration (see below) |

**Net honest verdict.** The single named obstruction to Teorema E — a
written-down proof of qualitative geometric growth of `M_K` — is **answered
in the affirmative**, unconditionally, `M_K=O(K(\sqrt e)^K)`, via a route
(Estágio 9's exact closed form + Reduction Lemma A + two elementary
inequalities) that is independent of, and does not require closing, the
referee's originally-sketched Proposição-6 route, which was found (§4) to
require an unestablished general-`b` bound on `A_r(b),B_r(b)` and was
correspondingly not pursued to completion. Nothing here weakens any existing
result: Teorema 3 (Estágio 6), the rate `c_K` (Estágio 7), the error-constant
growth rate `D^*_r(b)=\Theta(r^{3/2})` (Estágio 8), the all-orders closed
form (Estágio 9), and Teoremas A/C/D of Estágio 10 are all untouched and
unused beyond citation.

**This is a positive result and is therefore not catalogued by this
document: it requires the archive's mandatory hostile-referee pass first.**
A referee should attack, in order of importance: (i) §2.2's monotonicity
argument and its use to locate the supremum exactly at `n=K{+}1` — the
single most load-bearing step, verified here only by elementary algebra plus
an exhaustive-but-finite grid (§3.2), not by a from-scratch independent
re-derivation; (ii) whether `ψ_n^{(K)},ψ_n^{(K),R}\in[0,1]$ really needs
nothing beyond their stated definitions as probabilities (§2.4) — this
document treats it as definitional and does not re-derive it; (iii) Route
B's diagnosis (§4) that a general-`b` bound on `A_r(b),B_r(b)` is genuinely
missing, not merely unexploited — a referee with more appetite for that
route than this document had might find it closes after all, which would be
a welcome independent confirmation, not a contradiction, of this document's
Route A result.

---

## 7. Scope discipline

No file outside `theorem/uniform_in_c_attempt/mk_geometricity_attempt/` was
created, modified, or deleted. In particular `THEOREM.md`,
`error_constant_growth_attempt/ATTEMPT.md`, `uniform_in_c_attempt/ATTEMPT.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`,
`README*.md`, `PROOF_DEPENDENCY_MAP.md`, and every predecessor
`ATTEMPT.md`/`REFEREE_REPORT.md` in this lineage are untouched. No git
command was run.

---

## 8. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any computation | — |
| `verify_corollary_a1.py` / `.log` | §3.1: Corolário A1 vs 5 independently-PROVED targets, symbolic | ~5 s |
| `verify_monotonicity.py` / `.log` | §3.2: elementary-symmetric-function identity/positivity, exhaustive exact monotonicity + argmax grid | ~15 s |
| `compute_MK.py` / `.log` | §3.3: `M_K^ψ` exact, `K=1..300`, crude bound check, independent `mpmath` cross-check | ~20 s |
| `route_b_arithmetic.py` / `.log` | §3.4/§4: Route B step (a) verified independently, half-sum identity | ~1 s |
| `explore_true_rate.py` / `.log` | §5: informational-only true-rate exploration, `K` up to 3000 | ~30 s |

Reproduce in this order: `python3 verify_corollary_a1.py`;
`python3 verify_monotonicity.py`; `python3 compute_MK.py`;
`python3 route_b_arithmetic.py`; `python3 explore_true_rate.py`.
