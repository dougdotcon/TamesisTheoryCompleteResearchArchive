# The rate coefficient `c_K` is strictly positive for every `K\ge2`: `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)`

> **Governance.** `DISC-DEC-041`, front (b),
> `RATE-COEFFICIENT-POSITIVITY-ATTEMPT`, continuing the
> `K6-OPEN-LEMMA-ATTEMPT` / `K-GENERAL-EXISTENCE-ATTEMPT` lineage. Pure
> combinatorial/analytic mathematics — no external data, no holdout, no
> real-world claim, no governance edits. `../../../../../THEOREM.md`,
> `../../../../ATTEMPT.md` (wave 5), `../../../ATTEMPT.md` (wave 6,
> `k3_attempt_2/`), `../../ATTEMPT.md` (wave 7, `k6_attempt/`), and
> `../ATTEMPT.md` + `../adversarial/REFEREE_REPORT.md` (wave 8) are **not**
> touched — everything here lives under this new
> `rate_coefficient_positivity_attempt/` directory. No git commit was made.
> Every claim below is labeled PROVED, NUMERICALLY VERIFIED (exact rational
> arithmetic, never floating-point sampling), CONJECTURED, or OPEN, following
> the discipline the whole lineage uses.

> **Task.** `THEOREM.md` Estágio 6, item 4, and `DISC-DEC-040/041` name one
> remaining, narrow open item in this line. The exact `1/n` coefficient of
> `\varphi_n^{(K)}-\varphi_K` is now PROVED unconditionally for every `K\ge1`
> to equal
>
> `c_K := K\big[\varphi_K/4 + F_{K-1}(1,1) - \varphi_K\big]`,
>
> with `\varphi_K=4^K(K!)^2/(2K{+}1)!` the Wallis integral and `F_r(t,b)` the
> general-`r` leading-order continuum closed form of `k6_attempt/ATTEMPT.md`
> §2.3. That coefficient is exactly `0` at `K=1` and was **verified, not
> proved**, strictly positive for `2\le K\le12`. Whether `c_K>0` for every
> `K\ge13` — equivalently, whether the rate is exactly `\Theta(1/n)` rather
> than merely the already-proved `O(1/n)` — was left genuinely open. This
> document attempts to settle it.

> **Executive summary (read first).** The attempt succeeds, and the answer is
> much simpler than the problem's statement suggests. The apparently
> two-ingredient expression `c_K` collapses onto a **single** ingredient: the
> Wallis integral itself. Specifically (§2–§3, both PROVED):
>
> `\displaystyle F_{K-1}(1,1)=\frac{(2K{+}1)\varphi_K-1}{2K}`,  hence
> `\displaystyle \boxed{\,c_K=\frac{(K{+}2)\varphi_K-2}{4}\,}`.
>
> So the entire question "`c_K>0`?" is exactly the question
> "**`(K{+}2)\varphi_K>2`?**", with **equality** at `K=1` (which is precisely
> why `c_1=0`, the `K=1` degeneracy the wave-8 referee flagged as issue I-4).
> Because `\varphi_{K+1}/\varphi_K=(2K{+}2)/(2K{+}3)` exactly, the quantity
> `v_K:=(K{+}2)\varphi_K` satisfies
>
> `\displaystyle \frac{v_{K+1}}{v_K}-1=\frac{K}{(K{+}2)(2K{+}3)}>0\quad(K\ge1)`,
>
> so `v_K` is **strictly increasing** from `v_1=2` — giving `v_K>2`, i.e.
> `c_K>0`, for every `K\ge2`. Telescoping that increment gives the sharpest
> form of the result, a representation in which positivity is not an inequality
> to be proved at all but a visible property of the expression (§4.3):
>
> `\displaystyle c_K=\frac14\sum_{j=1}^{K-1}\frac{j\,\varphi_j}{2j+3}`
>
> — a sum of **strictly positive** terms, empty (hence `0`) exactly at `K=1`.
> The result is therefore **PROVED for every `K\ge2`**, not merely extended
> numerically: `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)` for every `K\ge2`, and
> `\Theta(1/n^2)` at `K=1`. Free corollaries (§5): `c_K` is strictly increasing
> in `K`, so `c_K\ge c_2=1/30` for all `K\ge2`; `c_K\to\infty` like
> `\sqrt{\pi K}/8`; and an explicit elementary lower bound
> `c_K\ge\big[(K{+}2)\sqrt{3K{+}1}/(2K{+}1)-2\big]/4` holds for every `K`.
> **What this does *not* do:** it does not touch any of the other named open
> items of the line (§8) — the all-orders general-`K` closed form, the
> uniform-in-`c` Theorem 3, the error-constant growth in `r`, or Conjectures
> 1–2. **And it is not yet catalogued:** by this archive's standing discipline
> a positive result of this weight requires independent adversarial
> reproduction before integration (§9, row 8; §10).

---

## 0. Disciplina — what was read, what is reused, what is new

**Read in full before writing anything here** (in the order mandated by the
brief):

1. `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-041`
   (the mandate and scope for this front).
2. `../../../../../THEOREM.md`, the entire `[Extensão, Estágio 6 — 2026-08-22]`
   section — the authoritative statement of what is now proved unconditionally
   for every `K\ge0`, and of the exact target named in its item 4.
3. `../ATTEMPT.md` (`k_general_existence_attempt/`, wave 8) — the
   discrete-Gronwall existence proof that closed `k6_attempt/ATTEMPT.md` §4's
   regularity caveat, making `F_r`, `G_r` and the general-`K` rate conjecture
   unconditional.
4. `../adversarial/REFEREE_REPORT.md` §A.7 (and its issue **I-4**) — where
   `c_K` is derived downstream of the Target Theorem and tabulated for
   `K=1,\dots,12`.
5. `../../ATTEMPT.md` (`k6_attempt/ATTEMPT.md`, wave 7) §2.3 — the symbolic-`r`
   closed form for `F_r(t,b)`, PROVED unconditionally for general `r`; and
   §2.4 (the post-adversarial boundary-condition addendum).
6. `../../../ATTEMPT.md` (`k3_attempt_2/ATTEMPT.md`, wave 6) §1–§3 — the exact
   `(a,b,r)` Markov chain and its transition rules, needed only for the
   independent finite-`n` corroboration of §6.

**Reused verbatim, without re-derivation, as established PROVED facts:**

- **The `1/n`-coefficient formula itself.** That
  `\varphi_n^{(K)}-\varphi_K=c_K/n+O(1/n^2)` with
  `c_K=K[\varphi_K/4+F_{K-1}(1,1)-\varphi_K]` is PROVED unconditionally for
  every `K\ge1` (`THEOREM.md` Estágio 6 items 2–4; derived in
  `../adversarial/REFEREE_REPORT.md` §A.7 from the wave-8 Target Theorem plus
  wave 5's Reduction Lemma A, using `\hat H_{K-1}(0,0)=F_{K-1}(1,1)`). **This
  document does not re-prove it and does not depend on re-proving it.** Its
  entire subject is the sign of the explicit expression `c_K`.
- **The closed form `F_r(t,b)=\sum_{k=0}^r\frac{r!}{(r-k)!}\,
  t^k\big/\prod_{i=1}^{k+1}(r{+}b{+}i)`** (`k6_attempt/ATTEMPT.md` §2.3,
  Theorem, PROVED for general `r`; unconditional since wave 8). Re-transcribed
  from its stated formula, not re-derived.
- **The Wallis-integral mean `\varphi_K=4^K(K!)^2/(2K{+}1)!`**
  (`THEOREM.md` Lemma 2, §5.2, PROVED).
- **The exact `(a,b,r)` transition rules** (`k3_attempt_2/ATTEMPT.md` §2,
  Proposition, PROVED) and **wave 5's Reduction Lemma A**
  `\varphi_n^{(K)}=(K/n)\psi_n^{(K),R}+(1-K/n)\psi_n^{(K)}` (PROVED) — used
  **only** in §6, for an independent corroboration that is explicitly *not*
  part of the proof.

**New in this document:** everything else — Lemma 1 (§2), Theorem A (§3),
Theorem B and its two independent proofs plus the manifestly-positive
representation (§4), the corollaries of §5, and all scripts. Every script was
written from scratch in this directory; nothing is imported from any sibling
directory.

**Arithmetic discipline.** Every claim labeled PROVED or "exact" below rests on
`fractions.Fraction` or `sympy.Symbol`/`sympy.gamma` arithmetic. Floating point
appears nowhere in any claim — only in columns explicitly labeled as decimal
display of a trend.

---

## 1. The target, restated precisely

Fix an integer `K\ge1`. Write

- `\displaystyle \varphi_K:=\frac{4^K(K!)^2}{(2K{+}1)!}` (the Wallis integral;
  equivalently `\varphi_K=\int_0^1(1-x^2)^K\,dx`, see §4.1);
- `\displaystyle F_r(t,b):=\sum_{k=0}^{r}\frac{r!}{(r-k)!}\cdot
  \frac{t^k}{\prod_{i=1}^{k+1}(r{+}b{+}i)}` (`k6_attempt/ATTEMPT.md` §2.3);
- `\displaystyle c_K:=K\Big[\frac{\varphi_K}{4}+F_{K-1}(1,1)-\varphi_K\Big]
   =K\Big[F_{K-1}(1,1)-\tfrac34\varphi_K\Big]`.

**What is already PROVED (upstream, not here).**
`\varphi_n^{(K)}-\varphi_K=\dfrac{c_K}{n}+O\!\big(1/n^2\big)` for every fixed
`K\ge1`.

**What this document must decide.** Whether `c_K>0` for every `K\ge13`
(equivalently, since `2\le K\le12` is already verified, for every `K\ge2`).
A positive answer upgrades the rate from the already-proved `O(1/n)` to exactly
`\Theta(1/n)`, for every `K\ge2`.

> **Note on `K=1`.** `c_1=0` exactly, and independently
> `\varphi_n^{(1)}-\varphi_1=1/(3n^2)` exactly — the degeneracy that the wave-8
> referee raised as issue **I-4**, and the reason the correct statement quantifies
> over `K\ge2`, not `K\ge1`. §4 shows this is not an accident of small `K`: `K=1`
> is exactly the **equality case** of the inequality being proved.

---

## 2. Lemma 1 — `F_{K-1}(1,1)` in closed form

> **Lemma 1 (PROVED).** For every integer `K\ge1`,
> `\displaystyle F_{K-1}(1,1)=\frac{(2K{+}1)\varphi_K-1}{2K}`.

*Proof.* Put `r=K{-}1`, `b=1`, `t=1` in the §2.3 closed form. Then
`r{+}b{+}i=K{+}i`, so
`\prod_{i=1}^{k+1}(r{+}b{+}i)=\prod_{i=1}^{k+1}(K{+}i)=\dfrac{(K{+}k{+}1)!}{K!}`,
and

`\displaystyle F_{K-1}(1,1)=\sum_{k=0}^{K-1}\frac{(K{-}1)!}{(K{-}1{-}k)!}\cdot
\frac{K!}{(K{+}k{+}1)!}
=(K{-}1)!\,K!\sum_{k=0}^{K-1}\frac{1}{(K{-}1{-}k)!\,(K{+}k{+}1)!}`.  (2.1)

Since `(K{-}1{-}k)+(K{+}k{+}1)=2K` for every `k`, multiplying and dividing by
`(2K)!` turns each summand into a binomial coefficient of the *same* row `2K`:

`\displaystyle \frac{(2K)!}{(K{-}1{-}k)!\,(K{+}k{+}1)!}=\binom{2K}{K{+}k{+}1}`,

and as `k` runs over `0,\dots,K{-}1` the index `j:=K{+}k{+}1` runs over
`K{+}1,\dots,2K`. Hence

`\displaystyle F_{K-1}(1,1)=\frac{(K{-}1)!\,K!}{(2K)!}\sum_{j=K+1}^{2K}\binom{2K}{j}`.  (2.2)

The remaining sum is the strict upper tail of a full binomial row. By the row
symmetry `\binom{2K}{j}=\binom{2K}{2K-j}` the strict lower tail
(`j\le K{-}1`) and the strict upper tail (`j\ge K{+}1`) are equal, and by the
binomial theorem the whole row is `2^{2K}=4^K`; therefore

`\displaystyle \sum_{j=K+1}^{2K}\binom{2K}{j}=\frac{4^K-\binom{2K}{K}}{2}`.  (2.3)

Combining (2.2)–(2.3), and using
`\dfrac{(K{-}1)!\,K!}{(2K)!}=\dfrac1K\cdot\dfrac{(K!)^2}{(2K)!}
=\dfrac{1}{K\binom{2K}{K}}`,

`\displaystyle F_{K-1}(1,1)=\frac{1}{2K}\left[\frac{4^K}{\binom{2K}{K}}-1\right]`.  (2.4)

Finally `\varphi_K=\dfrac{4^K(K!)^2}{(2K{+}1)!}
=\dfrac{4^K}{(2K{+}1)\binom{2K}{K}}`, i.e.
`\dfrac{4^K}{\binom{2K}{K}}=(2K{+}1)\varphi_K`. Substituting into (2.4) gives
the claim. `∎`

**Machine confirmation.** Every step is verified with `K` (and, where relevant,
`k`) kept **symbolic** in `sympy`: S1 (the product identity), S2 (the summand),
S3 (the binomial rewrite), S4a/S4b (the two ingredients of (2.3)), S5, P0, P2 —
see `verify_symbolic_K.log`. The assembled identity is additionally confirmed as
an exact rational identity for `K=1,\dots,120` against a *direct* evaluation of
the §2.3 sum, and (2.3) itself for `K=1,\dots,300`
(`verify_ck_closed_form.log`).

> **Remark (worth recording independently of the positivity question).**
> Lemma 1 says that `F_{K-1}(1,1)` — a value of the general-`r` continuum
> function at an *off-diagonal* argument `b=1`, which the source documents
> only ever evaluate as an explicit `K`-term sum — is an elementary rational
> function of the Wallis integral `\varphi_K` alone. `k6_attempt/ATTEMPT.md`
> §2.3 already notes that `F_r(1,0)=\varphi_r`; Lemma 1 is the companion fact
> one rung over in `b`. Nothing upstream needed or noticed it.

---

## 3. Theorem A — the rate coefficient in closed form

> **Theorem A (PROVED).** For every integer `K\ge1`,
> `\displaystyle c_K=\frac{(K{+}2)\varphi_K-2}{4}
> =\frac{(K{+}2)\,4^K(K!)^2}{4\,(2K{+}1)!}-\frac12`.

*Proof.* By Lemma 1,

`\displaystyle c_K=K\Big[F_{K-1}(1,1)-\tfrac34\varphi_K\Big]
=K\cdot\frac{(2K{+}1)\varphi_K-1}{2K}-\frac{3K}{4}\varphi_K
=\frac{(2K{+}1)\varphi_K-1}{2}-\frac{3K}{4}\varphi_K`,

and `\dfrac{2K{+}1}{2}-\dfrac{3K}{4}=\dfrac{4K{+}2-3K}{4}=\dfrac{K{+}2}{4}`,
so `c_K=\dfrac{K{+}2}{4}\varphi_K-\dfrac12`. `∎`

Equivalent forms, all PROVED and all machine-confirmed symbolically (P0, P1, S6):

`\displaystyle c_K=\frac{(K{+}2)\,4^K}{4\,(2K{+}1)\binom{2K}{K}}-\frac12
=\frac{K{+}2}{4}\int_0^1(1-x^2)^K dx-\frac12
=\frac{K{+}2}{4}\prod_{j=1}^{K}\frac{2j}{2j+1}-\frac12`.

**Immediate consequence — the reformulation that solves the problem.**

`\displaystyle c_K>0\iff (K{+}2)\,\varphi_K>2`,  and  `c_K=0\iff(K{+}2)\varphi_K=2`.

Write `v_K:=(K{+}2)\varphi_K`. At `K=1`, `v_1=3\cdot\tfrac23=2` **exactly** —
so `K=1` is the exact equality case, and `c_1=0` is not a coincidence but the
boundary of the inequality. The whole problem is now: *is `v_K>2` for `K\ge2`?*

**Exact values (all computed with `fractions.Fraction`; `K=1..8` reproduce
`../adversarial/REFEREE_REPORT.md` §A.7's table exactly, `K\ge9` extend it):**

| `K` | `\varphi_K` | `F_{K-1}(1,1)` | `v_K=(K{+}2)\varphi_K` | `c_K` | `c_K` (decimal) |
|---|---|---|---|---|---|
| 1 | `2/3` | `1/2` | `2` | `0` | 0.000000000 |
| 2 | `8/15` | `5/12` | `32/15` | `1/30` | 0.033333333 |
| 3 | `16/35` | `11/30` | `16/7` | `1/14` | 0.071428571 |
| 4 | `128/315` | `93/280` | `256/105` | `23/210` | 0.109523810 |
| 5 | `256/693` | `193/630` | `256/99` | `29/198` | 0.146464646 |
| 6 | `1024/3003` | `793/2772` | `8192/3003` | `1093/6006` | 0.181984682 |
| 7 | `2048/6435` | `1619/6006` | `2048/715` | `309/1430` | 0.216083916 |
| 8 | `32768/109395` | `26333/102960` | `65536/21879` | `10889/43758` | 0.248845925 |
| 9 | `65536/230945` | `53381/218790` | `65536/20995` | `11773/41990` | 0.280376280 |
| 10 | `262144/969969` | `43191/184756` | `1048576/323323` | `200965/646646` | 0.310780551 |
| 11 | `524288/2028117` | `436109/1939938` | `524288/156009` | `106135/312018` | 0.340156658 |
| 12 | `4194304/16900975` | `1172755/5408312` | `8388608/2414425` | `1779879/4828850` | 0.368592729 |
| **13** | `8388608/35102025` | `7088533/33801950` | `8388608/2340135` | `1854169/4680270` | 0.396167101 |
| 14 | `33554432/145422675` | `28539857/140408100` | `536870912/145422675` | `123012781/290845350` | 0.422949107 |
| 15 | `67108864/300540195` | `57414019/290845350` | `67108864/17678835` | `15875597/35357670` | 0.449000090 |
| 16 | `2147483648/9917826435` | `1846943453/9617286240` | `4294967296/1101980715` | `1045502933/2203961430` | 0.474374424 |
| 20 | `274877906944/1412926920405` | `240416274739/1378465288200` | `549755813888/128447901855` | `146430005089/256895803710` | 0.569997653 |

(`K=13`, the first value beyond the previously verified range, is highlighted;
`c_{13}=1854169/4680270>0`.)

---

## 4. Theorem B — positivity for every `K\ge2`

### 4.1 The one fact about `\varphi_K` that is needed

> **Fact (PROVED, elementary).** `\varphi_0=1` and
> `\dfrac{\varphi_{K+1}}{\varphi_K}=\dfrac{2K{+}2}{2K{+}3}` for every `K\ge0`;
> equivalently `\varphi_K=\prod_{j=1}^{K}\dfrac{2j}{2j{+}1}`.

*Proof.* Directly from `\varphi_K=4^K(K!)^2/(2K{+}1)!`:

`\displaystyle\frac{\varphi_{K+1}}{\varphi_K}
=\frac{4\,(K{+}1)^2\,(2K{+}1)!}{(2K{+}3)!}
=\frac{4(K{+}1)^2}{(2K{+}2)(2K{+}3)}
=\frac{4(K{+}1)^2}{2(K{+}1)(2K{+}3)}=\frac{2K{+}2}{2K{+}3}`,

and `\varphi_0=4^0(0!)^2/1!=1`. `∎` (Machine-confirmed with `K` symbolic: P3,
P6b; and exactly for `K=0,\dots,300`. This is of course the same recursion as
`\int_0^1(1-x^2)^{K+1}dx=\frac{2K+2}{2K+3}\int_0^1(1-x^2)^Kdx`, which is why
`\varphi_K=\int_0^1(1-x^2)^Kdx` — confirmed by symbolic integration for
`K=0,\dots,12`, P6a. The integral representation is *not* used in the proof;
it is recorded because it makes `\varphi_K>0` self-evident.)

### 4.2 The proof

> **Theorem B (PROVED).** `c_K>0` for **every** integer `K\ge2`, and `c_1=0`.
> Consequently, `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)` for every fixed `K\ge2`.

*Proof.* By Theorem A it suffices to show `v_K:=(K{+}2)\varphi_K>2` for `K\ge2`,
with `v_1=2`.

`v_1=3\varphi_1=3\cdot\tfrac23=2`.

For `K\ge1`, by the Fact of §4.1,

`\displaystyle \frac{v_{K+1}}{v_K}
=\frac{K{+}3}{K{+}2}\cdot\frac{\varphi_{K+1}}{\varphi_K}
=\frac{K{+}3}{K{+}2}\cdot\frac{2K{+}2}{2K{+}3}
=\frac{2(K{+}1)(K{+}3)}{(K{+}2)(2K{+}3)}`.

Both numerator and denominator are positive, and

`2(K{+}1)(K{+}3)-(K{+}2)(2K{+}3)=(2K^2{+}8K{+}6)-(2K^2{+}7K{+}6)=K`,

so

`\displaystyle \frac{v_{K+1}}{v_K}-1=\frac{K}{(K{+}2)(2K{+}3)}>0\qquad(K\ge1)`.  (4.1)

Hence `v_{K+1}>v_K` for every `K\ge1`: the sequence `(v_K)_{K\ge1}` is strictly
increasing. Since `v_1=2`, induction gives `v_K>2` for every `K\ge2`, i.e.
`c_K=(v_K-2)/4>0`. Finally `c_1=(v_1-2)/4=0`.

For the last sentence: the upstream result gives
`\varphi_n^{(K)}-\varphi_K=c_K/n+O(1/n^2)`; with `c_K>0` a fixed positive
constant, `n(\varphi_n^{(K)}-\varphi_K)\to c_K\in(0,\infty)`, which is exactly
`\Theta(1/n)`. `∎`

Note that the proof is *sharp at exactly one point*: the single algebraic
cancellation `2(K{+}1)(K{+}3)-(K{+}2)(2K{+}3)=K` is `0` at `K=0` and positive
for every `K\ge1`, and the anchor `v_1=2` is an exact equality. Nothing about
the argument is asymptotic; no estimate is made anywhere.

**Machine confirmation, `K` symbolic:** P3 (the `\varphi` ratio), P4 (identity
(4.1) itself), P5 (`v_1=2`) — all verified as exact symbolic identities in
`sympy` with `K` a positive-integer `Symbol`, not sampled
(`verify_symbolic_K.log`). Independent exact-rational re-checks of (4.1) for
`K=1,\dots,300`, and of `v_K>2` for `K=2,\dots,300`, in
`verify_ck_closed_form.log`.

### 4.3 The manifestly-positive representation

Telescoping (4.1) gives a form in which positivity requires no argument at all.
From `v_{K+1}-v_K=v_K\cdot\frac{K}{(K+2)(2K+3)}` and `v_K=(K{+}2)\varphi_K`,

`\displaystyle v_{K+1}-v_K=\frac{K\,\varphi_K}{2K{+}3}`,

so summing from `1` to `K{-}1` and using `v_1=2`:

> **Corollary B′ (PROVED).** For every integer `K\ge1`,
> `\displaystyle c_K=\frac14\sum_{j=1}^{K-1}\frac{j\,\varphi_j}{2j+3}
> =\frac14\int_0^1\sum_{j=1}^{K-1}\frac{j}{2j+3}\,(1-x^2)^j\,dx`.

Every summand `j\varphi_j/(2j{+}3)` is strictly positive (`j\ge1`,
`\varphi_j>0`), so `c_K>0` for `K\ge2` is *visible*, and the sum is empty —
hence exactly `0` — at `K=1`. This is the "sum of manifestly non-negative
terms" the brief asked about as route (ii), obtained as a by-product of route
(i) rather than as an alternative to it.

*Example.* `c_4=\frac14\big[\frac{1\cdot(2/3)}{5}+\frac{2\cdot(8/15)}{7}
+\frac{3\cdot(16/35)}{9}\big]=\frac14\big[\frac2{15}+\frac{16}{105}
+\frac{16}{105}\big]=\frac{23}{210}` ✓.

Machine-confirmed: P7a (the increment, `j` symbolic), P7b (the assembled
identity, exact, `K=1,\dots,400`), P7c (term positivity); and independently in
`verify_ck_closed_form.log` for `K=1,\dots,300`.

### 4.4 A second, independent proof

Because the result matters, here is a route that shares no algebra with §4.2
beyond Theorem A. Using `c_K=\frac{(K{+}2)4^K}{4(2K{+}1)\binom{2K}{K}}-\frac12`,
positivity is equivalent to

`\displaystyle \binom{2K}{K}<\frac{4^K(K{+}2)}{2(2K{+}1)}`.  (4.2)

Take the classical bound `\binom{2K}{K}\le 4^K/\sqrt{3K{+}1}` (`K\ge0`), which
we re-prove by the same technique for completeness: with
`a_K:=\binom{2K}{K}\sqrt{3K{+}1}/4^K` one has `a_0=a_1=1` and

`\displaystyle \frac{a_{K+1}}{a_K}=\frac{2K{+}1}{2(K{+}1)}\sqrt{\frac{3K{+}4}{3K{+}1}}`,
with `4(K{+}1)^2(3K{+}1)-(2K{+}1)^2(3K{+}4)=K\ge0`,

so `a_{K+1}\le a_K`, hence `a_K\le1` for all `K\ge0`. It therefore suffices that
`4^K/\sqrt{3K{+}1}<4^K(K{+}2)/(2(2K{+}1))`, i.e. `(4K{+}2)<(K{+}2)\sqrt{3K{+}1}`,
i.e. (squaring, both sides positive)

`(K{+}2)^2(3K{+}1)-(4K{+}2)^2=(3K^3{+}13K^2{+}16K{+}4)-(16K^2{+}16K{+}4)
=3K^3-3K^2=3K^2(K{-}1)>0` for `K\ge2`.

This reproves Theorem B for `K\ge2`, and as a bonus yields the explicit
elementary lower bound of §5.3. Machine-confirmed with `K` symbolic: S11a,
S11b, S11c.

---

## 5. Corollaries (all PROVED)

### 5.1 Monotonicity, and a uniform positive floor

(4.1) gives `v_{K+1}>v_K` for every `K\ge1`, hence `c_{K+1}>c_K`: the rate
coefficient is **strictly increasing** in `K` on `K\ge1`. In particular

`\displaystyle c_K\ge c_2=\frac1{30}\qquad\text{for every }K\ge2`,

a uniform positive floor. (Exactly re-verified for `K=2,\dots,5000`,
`verify_ck_closed_form.log`.)

### 5.2 Growth rate

From Corollary B′ and `\varphi_j\sim\frac12\sqrt{\pi/j}`, the summand is
`\sim\frac14\sqrt{\pi/j}`, and `\sum_{j\le K}j^{-1/2}\sim2\sqrt K`, giving
`c_K\sim\frac{\sqrt{\pi K}}{8}\to\infty`. Equivalently, directly from
Theorem A and the classical Wallis-ratio expansion
`\binom{2K}{K}4^{-K}=(\pi K)^{-1/2}\big(1-\frac1{8K}+\frac1{128K^2}+\cdots\big)`:

`\displaystyle c_K=\frac{\sqrt{\pi K}}{8}-\frac12+\frac{13\sqrt\pi}{64\sqrt K}
+O\!\big(K^{-3/2}\big)`.

Confirmed by `sympy` series (S10a) and numerically: the residual after these
three terms, multiplied by `K^{3/2}`, is flat at `\approx0.1229` across
`K=200,10^3,5\cdot10^3,2\cdot10^4,10^5` — exactly the signature of a genuine
`O(K^{-3/2})` next term (`verify_symbolic_K.log`, S10). So the rate coefficient
does not merely stay positive; it grows without bound, like `\sqrt K`.

### 5.3 An explicit elementary lower bound, valid for every `K`

From §4.4, `\varphi_K=\dfrac{4^K}{(2K{+}1)\binom{2K}{K}}\ge
\dfrac{\sqrt{3K{+}1}}{2K{+}1}`, hence

`\displaystyle c_K\ \ge\ \frac14\left[\frac{(K{+}2)\sqrt{3K{+}1}}{2K{+}1}-2\right]`,

which is strictly positive exactly for `K\ge2` (§4.4). At `K=13` it gives
`c_{13}\ge0.3784\ldots` against the true `0.3961\ldots`; at `K=10^4` it gives
`21.154\ldots` against `21.659\ldots` (S11d). The bound captures the correct
`\sqrt K` growth up to the constant `\sqrt3/8` vs. the true `\sqrt\pi/8`.

---

## 6. Independent corroboration from the finite-`n` side (NUMERICALLY VERIFIED, exact)

The proof above is entirely about the sign of an explicit expression. The one
thing it cannot self-check is whether **this session read the definition of
`c_K` correctly** — i.e. whether the expression proved positive is really the
`1/n` coefficient of `\varphi_n^{(K)}-\varphi_K`. That identification is
upstream (PROVED, adversarially refereed) and is not re-proved here, but it is
worth an independent check that costs little.

`corroborate_finite_n.py` re-implements, from scratch, the **raw** exact
transition rules of `k3_attempt_2/ATTEMPT.md` §2 —

`g(a,b,r)=\frac1m+\frac rm h(a{+}1,b,r{-}1)+\frac{m-1-r-b}{m}g(a{+}1,b,r)`
(`m=n{-}a`), `h(a,b,r)=\frac1n+\frac rn h(a,b{+}1,r{-}1)+
\frac{n-1-a-b-r}{n}g(a,b{+}1,r)`,
`\psi_n^{(K)}=g(0,0,K)`, `\psi_n^{(K),R}=h(0,0,K{-}1)` —

together with wave 5's Reduction Lemma A, as an iterative exact-`Fraction`
evaluation (note `b\le K` always, so the state space is `O(nK^2)`). It never
touches `F_r`, `G_r`, or anything from §§2–5 above.

**Sanity, against already-PROVED closed forms.**

- `\varphi_n^{(3)}` from the raw rules `=16/35+\frac1{14n}+\frac{11}{10n^2}
  +\frac{23}{35n^3}+\frac6{35n^4}` exactly, `n=4,\dots,30` — wave 6's own
  PROVED closed form, reproduced by an independently written implementation.
- `\varphi_n^{(1)}-\varphi_1=1/(3n^2)` exactly, `n=2,\dots,40` — the `K=1`
  degeneracy (issue I-4), reproduced independently.

**The exact `1/n` coefficient, extracted with no extrapolation.** For each `K`,
`\varphi_n^{(K)}` is fitted as an exact polynomial `\sum_{j=0}^{D}\alpha_j n^{-j}`
in `1/n` (exact Gaussian elimination over `Fraction`, `D{+}1` data points), and
the fitted polynomial is then **validated against six further `n` values it never
saw**. It validates in every case, with `D=K{+}1`, so the `\alpha_j` are exact:

| `K` | `D` | `\alpha_0` | `=\varphi_K`? | `\alpha_1` (exact) | `=c_K`? |
|---|---|---|---|---|---|
| 1 | 2 | `2/3` | yes | `0` | yes |
| 2 | 3 | `8/15` | yes | `1/30` | yes |
| 3 | 4 | `16/35` | yes | `1/14` | yes |
| 4 | 5 | `128/315` | yes | `23/210` | yes |
| 5 | 6 | `256/693` | yes | `29/198` | yes |
| 6 | 7 | `1024/3003` | yes | `1093/6006` | yes |
| 7 | 8 | `2048/6435` | yes | `309/1430` | yes |
| 8 | 9 | `32768/109395` | yes | `10889/43758` | yes |
| 9 | 10 | `65536/230945` | yes | `11773/41990` | yes |

Nine exact confirmations, obtained from the raw Definition-4 machinery with no
reference whatsoever to `F_r` or to the continuum limit. Note `K=9`
(`c_9=11773/41990`) lies **beyond** the referee report's printed table and
agrees exactly with Theorem A. This closes the transcription risk.

*(Presented as corroboration of the upstream identification, not as any part of
the proof of Theorem B.)*

---

## 7. What was tried, and the honest record of the route

The brief suggested three routes: (i) get an explicit closed form and prove
positivity by calculus/asymptotics with exact small-`K` computation; (ii) find a
manifestly-positive representation; (iii) failing a proof, extend the verified
range and say so honestly.

What actually happened: route (i)'s **first step alone was decisive**. The
moment `F_{K-1}(1,1)` was written with a common `(2K)!` — which is natural
because `(K{-}1{-}k)+(K{+}k{+}1)=2K` is constant in `k` — the sum became a
binomial-row tail, which is elementary, and the whole expression collapsed onto
`\varphi_K`. No calculus, no asymptotic analysis, and no large-`K` numerical
campaign was needed for the proof (they appear here only as corroboration and
as corollaries). Route (ii) then fell out for free by telescoping (§4.3).
Route (iii) was not needed.

Things attempted that were *not* needed, recorded so a later reader does not
repeat them:

- **Direct symbolic summation of (2.1) by `sympy`.** `sympy` does not close
  `\sum_{k=0}^{K-1}\Gamma(K)\Gamma(K{+}1)/(\Gamma(K{-}k)\Gamma(K{+}k{+}2))` in
  reasonable time (it was left running for minutes without terminating and was
  killed). This is why §2 does the binomial-row step by hand instead; that step
  is two lines and every ingredient of it *is* machine-checked symbolically
  (S4a, S4b). The check was removed from the final script rather than left as a
  hanging call.
- **Richardson extrapolation** on `n(\varphi_n^{(K)}-\varphi_K)` (first
  version of §6). It converges cleanly to `c_K` but only to `\sim10^{-4}` at
  `n=256`, which is corroboration of the weaker, floating-comparison kind. It
  was replaced by the exact polynomial-in-`1/n` fit, which is an exact rational
  identification and strictly stronger. The intermediate result is noted here
  because it is what motivated looking for the exact fit.
- **The `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}` route** (§4.4) was found first and
  kept as a second independent proof, but it is strictly weaker and less
  self-contained than §4.2: it needs a classical inequality (re-proved here,
  but still an extra ingredient) where §4.2 needs only `\varphi_1=2/3` and a
  ratio.

Nothing was found that contradicts, weakens, or is in tension with any prior
result in the lineage.

---

## 8. What this closes, precisely, and what it does not

**Closed.**

- **`THEOREM.md` Estágio 6, item 4's remaining open piece** — the positivity of
  the rate coefficient for `K\ge13` — is settled affirmatively, and in fact for
  all `K\ge2` uniformly, by proof rather than by extended verification. Item
  (iii) of Estágio 6's "what remains genuinely open" list ("*a positividade do
  coeficiente de taxa para `K\ge13`*") is answered.
- Consequently, `\varphi_n^{(K)}-\varphi_K=\Theta(1/n)` **exactly**, for every
  fixed `K\ge2` — not merely `O(1/n)`. Together with the exact
  `\varphi_n^{(1)}-\varphi_1=1/(3n^2)`, the rate of `\varphi_n^{(K)}\to\varphi_K`
  is now completely determined at leading order for **every** `K\ge1`.
- As a side effect, the correct scoping of the wave-8 referee's issue **I-4**
  is now not merely correct-by-inspection but explained: `K=1` is the exact
  equality case of `(K{+}2)\varphi_K\ge2`, so `\Theta(1/n)` fails at `K=1` for
  a structural reason, not by accident.

**Not closed, and untouched by anything here** (verbatim the same list as
`THEOREM.md` Estágio 6, minus item (iii)):

1. The exact, **all-orders**, general-`K` closed form for `\psi_n^{(K)}`
   (`k6_attempt/ATTEMPT.md` §6.2) — separate, harder, not approached.
2. The growth rate in `r` of the error constants `D_r(b),C_r(b)` of
   `../ATTEMPT.md` — named there, not pursued there or here.
3. The **locally-uniform-in-`c`** version of Theorem 3 (`THEOREM.md` §9 item 4)
   — genuinely independent gap, untouched.
4. Conjectures 1–2 (`THEOREM.md` §8, the full distributional law) — untouched.

Also explicitly **not** claimed here: any statement about the `O(1/n^2)`
remainder beyond what is already proved upstream. Theorem B upgrades `O(1/n)`
to `\Theta(1/n)` and nothing more; the second-order coefficient is not
addressed.

**Not yet catalogued.** Per this archive's standing discipline (and
`DISC-DEC-041`'s own `untouched_safeguards`), a positive result of this weight
requires **independent adversarial reproduction** before it may be integrated
into `THEOREM.md` or the governance ledger. This document does not claim
victory in the archive's sense; it reports a proof and flags that the review is
required. Integration is the orchestrating session's job, not this one's. No
file outside this directory was modified, and no git commit was made.

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | **Lemma 1** — `F_{K-1}(1,1)=[(2K{+}1)\varphi_K-1]/(2K)` (§2) | **PROVED**, elementary; every step machine-verified with `K,k` symbolic (`sympy`: S1–S5, P0, P2) and exactly re-checked for `K=1..120` against a direct evaluation of `k6_attempt` §2.3's sum |
| 2 | **Theorem A** — `c_K=[(K{+}2)\varphi_K-2]/4` (§3) | **PROVED**, one line from Lemma 1; symbolic `K` (P1, S6); reproduces `REFEREE_REPORT` §A.7's table for `K=1..8` exactly and extends it |
| 3 | **Theorem B** — `c_K>0` for every `K\ge2`; `c_1=0` (§4.2) | **PROVED**, elementary and non-asymptotic: `v_1=2` and `v_{K+1}/v_K-1=K/((K{+}2)(2K{+}3))>0`. Symbolic-`K` confirmation P3–P5; exact re-check `K=2..5000` |
| 4 | **Corollary B′** — `c_K=\frac14\sum_{j=1}^{K-1}j\varphi_j/(2j{+}3)`, a sum of strictly positive terms (§4.3) | **PROVED** (telescoping (4.1)); symbolic increment P7a, exact assembly `K=1..400` (P7b) |
| 5 | **Second independent proof** via `\binom{2K}{K}\le4^K/\sqrt{3K{+}1}` (§4.4) | **PROVED**, including a re-proof of the classical bound by the same ratio technique (symbolic `K`: S11a–S11c) |
| 6 | Corollaries: `c_K` strictly increasing, `c_K\ge1/30` for `K\ge2`, `c_K\sim\sqrt{\pi K}/8`, explicit lower bound `[(K{+}2)\sqrt{3K{+}1}/(2K{+}1)-2]/4` (§5) | **PROVED** (monotonicity, floor, lower bound); the three-term asymptotic expansion is **PROVED given** the classical Wallis-ratio expansion, and is separately corroborated numerically (flat `K^{3/2}`-scaled residual across `K=200..10^5`) |
| 7 | Independent finite-`n` corroboration: `\alpha_1=c_K` exactly, `K=1..9`, from the raw `(a,b,r)` transition rules via an exact validated polynomial-in-`1/n` fit (§6) | **NUMERICALLY VERIFIED** (exact `Fraction` arithmetic, out-of-sample validated) — presented as a guard against transcription error, **not** as part of the proof |
| 8 | Independent adversarial re-verification of this document | **NOT PERFORMED.** Required by the archive's standing discipline before this result may be catalogued in `THEOREM.md` / the ledger. Flagged, not executed here |
| 9 | The upstream identification `\varphi_n^{(K)}-\varphi_K=c_K/n+O(1/n^2)` | **NOT RE-PROVED HERE** — reused as PROVED (`THEOREM.md` Estágio 6 items 2–4; `REFEREE_REPORT` §A.7), correctly labelled as a dependency, and independently corroborated in §6 |
| 10 | Any of the four remaining open items of §8 | **NOT ADDRESSED** — out of scope, correctly labelled |

**Net honest verdict.** The task's target — decide whether `c_K>0` for every
`K\ge13` — is achieved as a **proof**, not as extended verification: outcome
(a), full closure of the named question. The proof is short, elementary, and
non-asymptotic, and rests on nothing beyond (i) the already-PROVED closed form
for `F_r(t,b)` and (ii) `\varphi_1=2/3` with the Wallis recursion. The one
genuine idea is a change of viewpoint rather than a technique: writing the
`K`-term sum `F_{K-1}(1,1)` over a common `(2K)!` reveals it as half a binomial
row, after which the two-ingredient expression `c_K` collapses to the single
ingredient `\varphi_K` and the question becomes `(K{+}2)\varphi_K>2`, whose
proof is a ratio computation with an exact equality case at `K=1`. The result
**does not** touch the other four open items of the line (§8), and it is
**not** catalogued: scorecard row 8 (independent adversarial reproduction)
remains open and is a precondition for integration.

---

## 10. Files, reproducibility

All scripts are new, written from scratch in this directory; nothing is
imported from any sibling directory. Already-proved closed forms (`F_r(t,b)`,
`\varphi_K`, the `(a,b,r)` transition rules) are re-transcribed from their
stated formulas and labelled as such in the source. Every claim labelled PROVED
or "exact" rests on `fractions.Fraction` or `sympy` symbolic arithmetic; floats
appear only in columns explicitly labelled as decimal display.

- **`verify_ck_closed_form.py` / `.log`** — the exact-rational spine.
  (1) `F_r(t,b)` built **twice independently** — from §2.3's diagonal
  coefficient recursion and from §2.3's closed form — agreeing exactly at 1575
  points (`r=0..24`, `b=0..8`, seven values of `t`), plus `F_r(1,0)=\varphi_r`
  for `r=0..24`. (2) `c_K` by its *definition* reproducing
  `REFEREE_REPORT` §A.7's three columns for `K=1..8`. (2b) the headline
  identities of §§2–4 including the manifestly-positive sum, exact to `K=300`.
  (3)–(5) the equivalent central-binomial forms and the `u_K` ratio identity.
  (6) exact positivity **and** strict monotonicity sweep, `K=2..5000`, plus the
  exact values `c_9..c_{16}` extending A.7's table. 23 checks, 0 failures;
  runtime `\approx26` s.
- **`verify_symbolic_K.py` / `.log`** — `K` kept **symbolic** (`sympy.Symbol`,
  positive integer) through every algebraic step: P0–P7c (the primary
  `\varphi_K` route of §§2–4, including the telescoping increment) and S1–S11d
  (the equivalent central-binomial route of §4.4, the asymptotic expansion of
  §5.2, and the classical-bound re-proof). 29 checks, 0 failures; runtime
  `\approx12` s.
- **`corroborate_finite_n.py` / `.log`** — §6: an independent from-scratch
  iterative exact-`Fraction` implementation of the raw `(a,b,r)` transition
  rules plus Reduction Lemma A; reproduces wave 6's PROVED `\varphi_n^{(3)}`
  closed form (`n=4..30`) and the exact `\varphi_n^{(1)}-\varphi_1=1/(3n^2)`
  (`n=2..40`); then extracts `\alpha_0,\alpha_1` exactly by a validated
  polynomial-in-`1/n` fit, `K=1..9`. 3 checks, 0 failures; runtime `\approx3` s.
- **`PROGRESS.log`** — chronological checkpoint trail kept during this session,
  including the point at which the collapse onto `\varphi_K` was found and the
  two superseded intermediate routes recorded in §7.

To reproduce, from this directory:

```
python3 verify_ck_closed_form.py     #  ~26 s, exact rationals   -> 23 checks OK
python3 verify_symbolic_K.py         #  ~12 s, symbolic K        -> 29 checks OK
python3 corroborate_finite_n.py      #   ~3 s, exact rationals   ->  3 checks OK
```

All three were re-run clean, from scratch, immediately before this document was
finalised: **55 checks, 0 failures, all three exiting `0`.**

Each exits `0` and prints a final `RESULT:` line only if every check passed;
any failure is collected and reported by name and forces a non-zero exit.
