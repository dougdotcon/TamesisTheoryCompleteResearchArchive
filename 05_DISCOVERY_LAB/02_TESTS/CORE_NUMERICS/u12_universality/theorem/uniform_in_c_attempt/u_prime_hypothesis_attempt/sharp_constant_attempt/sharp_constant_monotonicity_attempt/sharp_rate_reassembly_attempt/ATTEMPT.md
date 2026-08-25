# The sharp explicit rate — the Estágio 12 assembly re-executed with `a*`: every step survives verbatim, and `κ* = κ_B` unchanged

> **Governance.** Wave 17, front (b), `SHARP-RATE-REASSEMBLY-ATTEMPT`,
> `DISC-DEC-072`. Target: the "mechanical but unexecuted" item named by
> Estágio 19 of `THEOREM.md` — re-run the Estágio 12 assembly of the
> explicit unconditional convergence rate with the SHARP constant `a*`
> in place of `a = 1+\sqrt{π/2}`, recomputing the additive constant
> honestly. Pure combinatorics/asymptotics internal to this archive; no
> external data, no real-world claim, no governance edits, no git commit.
> Nothing outside this `sharp_rate_reassembly_attempt/` directory was
> created or modified; every input document was read-only, prose only —
> **no prior front's `.py` script was opened**; every formula used below
> was re-derived/re-implemented fresh from the prose statements of the
> cited documents. Seed `20260862000+` is reserved for this front
> (`DISC-DEC-072`; grep-confirmed to appear only in ledger/queue
> reservations before use) but — exactly as in every sibling document of
> this lineage — **not used**: every object below is deterministic, and
> every load-bearing check is exact rational (`fractions.Fraction`) or
> certified-bracket arithmetic. No Millennium Problem claim anywhere.

> **VERDICT (read first).** **The re-assembly CLOSES, in full.** The
> final theorem (Teorema R, §4) is:
>
> `\displaystyle |φ(n,c) - φ_∞(c)| \;\le\; \frac{a^*\sqrt c + κ_B}{n}`
> for every integer `n\ge4` and every real `0\le c\le n`, with
> `a^* = \sqrt π\big(\tfrac1{\sqrt2}-\tfrac12\big) = 0.3670872119\ldots`
> and `κ^* = κ_B := \sup_{c\ge0} c^2 I_2(c) = 0.280480169\ldots \in
> (0.28048,\,0.2805)` — **strict** (`<`) for every `0<c\le n`. In
> decimal form: `|Δ_n(c)| \le [\,0.3670873\sqrt c + 0.2805\,]/n`.
>
> 1. **Every step of the Estágio 12 assembly goes through verbatim with
>    `a^*`.** The old proof of Teorema B
>    (`uniform_in_c_attempt/ATTEMPT.md` §6.2) uses the hypothesis
>    `(U'_a)` strictly as a black box — the numerical value of `a`
>    enters exactly once, as a multiplicative constant pulled out of the
>    `A_n`-half by Jensen; no other step interacts with it. Substituting
>    the sharp `(U')` (now PROVED with `a^*` for **all** `0\le K\le n`,
>    Estágio 19 + its referee's boundary-case closure, session-verified)
>    changes nothing else. No repaired step, no non-closure.
> 2. **The additive constant does NOT change: `κ^* = κ_B`.** Traced to
>    its source (§5), the `0.2805` of Estágio 12 is a decimal upper
>    bound for `κ_B=\sup_{c\ge0}c^2I_2(c)`, which comes **entirely from
>    the `B_n` (Binomial→Poisson mixture) half** of the exact split
>    `Δ_n=A_n+B_n` — a half in which neither `(U')` nor any constant
>    `a` ever appears. The honest recomputation is therefore a proof of
>    *independence*, not a new value — plus, new here, the first
>    **certified** rational bracket `κ_B\in(0.28048, 0.2805)` (pure
>    rational branch-and-bound, no floating-point trust; §5.2),
>    upgrading what Estágio 12's own referee had flagged (F-9) as a
>    float-level evaluation of a transcendental sup.
> 3. **Domain unchanged, made fully explicit:** `n\ge4`, `0\le c\le n`
>    (and `C\le n` in the sup-over-`[0,C]` corollary — implicit in
>    Estágio 12's wording, explicit here). `n\ge4` is a proof artifact
>    of Lema 6.1 exactly as before (wave-11 referee note F-13).
> 4. **Validation:** 2 594 certified cells of the final inequality
>    (exact rational `φ(n,c)`, certified rational brackets of `φ_∞`,
>    conservative rational RHS), `n` from 4 to 1024 on interior grids
>    and to 30 000 on the boundary line `c=n`, including `c` at and near
>    `n` — **zero violations**; the assembled bound's two halves
>    verified separately; the fresh engine validated against brute-force
>    enumeration from Definition 4 plus archive anchors (37/37 exact);
>    sharp `(U')` independently re-verified at ~1 490 certified points.
>    Worst observed `LHS/RHS = 0.970` at `(n,c)=(3000,3000)` — the
>    bound is **asymptotically tight along `c=n`** (§6), so `a^*` is
>    genuinely the best possible multiplicative constant in this shape
>    of bound. One self-caught bug in this front's own checking code
>    disclosed (§8); it affected only a diagnostic, never the theorem.

---

## 0. Discipline

- **Read (prose only):** `THEOREM.md` (Estágios 11, 12, 13, 19 and the
  sections they reference: §§3–5, §7); `uniform_in_c_attempt/ATTEMPT.md`
  (§5, §6, §7.1) and its `adversarial/REFEREE_REPORT.md` (§4);
  `u_prime_hypothesis_attempt/ATTEMPT.md` (all) and its referee report;
  `sharp_constant_attempt/ATTEMPT.md` and its referee report;
  `sharp_constant_monotonicity_attempt/ATTEMPT.md` **with all dated
  addenda** and its `adversarial/REFEREE_REPORT.md` (esp. §8, the
  boundary-case closure, and §9 findings E-1/E-2/S-1/S-2/N-1).
- **Not read:** any `.py` file of any prior front. The exact engine used
  here (`engine.py`) was written from scratch from the prose closed
  forms, then validated against brute-force enumeration built directly
  from `THEOREM.md` Definition 4 (§7, T1).
- **Arithmetic:** every certified claim uses `fractions.Fraction` (with
  integer-squaring square-root brackets and the classical rational
  brackets `π\in(3.14159265358979,\,3.14159265358980)`,
  `e>2.718281` — CITED). `mpmath` (30–50 dps) appears only in display
  rows explicitly labeled non-load-bearing.
- **No randomness anywhere.** Seed table: §10.

Notation as in the parent lineage: `φ(n,c)` (Definition 1 with
`q=c/n\le1`), `φ_n^{(K)}` (Definition 4), `φ_K=4^K(K!)^2/(2K+1)!`,
`φ_∞(c)=\int_0^1e^{-ct^2}dt`, `Δ_n(c):=φ(n,c)-φ_∞(c)`,
`I_k(c):=\int_0^1t^{2k}e^{-ct^2}dt`, `Q(n)` Ramanujan's function,
`a^*=\sqrt π(1/\sqrt2-1/2)`, `a=1+\sqrt{π/2}`.

---

## 1. The ingredients, with provenance

Every ingredient below is an already-catalogued PROVED result, used by
citation; nothing in this document re-proves them, and nothing new is
assumed.

| # | Ingredient | Statement | Proved by |
|---|---|---|---|
| I1 | Mixture identity (7.1) | `φ(n,c)=\sum_{K=0}^n\binom nK(\tfrac cn)^K(1-\tfrac cn)^{n-K}φ_n^{(K)}`, exact, `0\le c\le n` | `THEOREM.md` Fact 4.1 (Stage 2) |
| I2 | Poisson mixture (7.2) | `φ_∞(c)=\sum_{K\ge0}e^{-c}\tfrac{c^K}{K!}φ_K`, exact | `THEOREM.md` §5.2 / Fact 4.1 |
| I3 | Exact split | `Δ_n(c)=A_n(c)+B_n(c)` with `A_n=\sum_{K=0}^n b_K(φ_n^{(K)}-φ_K)`, `B_n=\sum_{K\ge0}(b_K-p_K)φ_K` (`b_K` Binomial(`n,c/n`), `p_K` Poisson(`c`) masses) | `THEOREM.md` §7.2 Prop. 3; `uniform_in_c_attempt` §5.1 |
| I4 | **Sharp (U')** | `\lvertφ_n^{(K)}-φ_K\rvert\le a^*\sqrt K/n` for **all** `0\le K\le n`, all `n\ge1`; strict for `K\ge1` | Estágio 19: generic `1\le K\le n{-}1` via `M_K<a^*\sqrt K` (monotonicity-attempt Th. 2) + argmax-at-`n{=}K{+}1` (u_prime Th. 2); boundary `K=n` via the Estágio 19 referee's §8 closure (session-verified); `K=0` trivial (`φ_n^{(0)}=φ_0=1`) |
| I5 | `B_n` integral form | `B_n(c)=\int_0^1[(1-\tfrac{ct^2}n)^n-e^{-ct^2}]dt\le0`, `n\ge1`, `0\le c\le n` | `uniform_in_c_attempt` Lema 5.1 |
| I6 | Poisson-approx. bound | `0\le e^{-x}-(1-x/n)^n\le\tfrac{x^2}ne^{-x}` for `n\ge4`, `0\le x\le n` | `uniform_in_c_attempt` Lema 6.1 |
| I7 | `B_n` uniform bound | `\lvert B_n(c)\rvert\le c^2I_2(c)/n\le κ_B/n`, `n\ge4`, `0\le c\le n`, `κ_B=\sup_{c\ge0}c^2I_2(c)` | `uniform_in_c_attempt` Corolário 6.2 |
| I8 | Boundary anchor | `φ(n,n)=φ_n^{(n)}=φ_n^{(n-1)}=Q(n)/n` exactly | `uniform_in_c_attempt` Prop. 7.1 + post-adversarial exact identity |
| I9 | `φ_∞` tail bracket | `φ_∞(c)=\tfrac{\sqrt π}{2\sqrt c}-R(c)`, `0<R(c)<\tfrac{e^{-c}}{2c}` | `THEOREM.md` Corolário 4.2 (used only in verification) |

All of I1–I3, I5–I7 were confirmed SOUND by the wave-11 adversarial
referee (`uniform_in_c_attempt/adversarial/REFEREE_REPORT.md` §4); I4 by
the Estágio 12/13/19 referees (three independent SOUND verdicts, the
`K=n` case closed constructively by the Estágio 19 referee itself and
re-verified by the orchestrating session, per the dated addendum in
`sharp_constant_monotonicity_attempt/ATTEMPT.md` §6).

---

## 2. The Estágio 12 assembly, traced step by step

Estágio 12's explicit rate is `uniform_in_c_attempt/ATTEMPT.md` §6.2
**Teorema B** applied with the then-new hypothesis `(U'_a)` at
`a=1+\sqrt{π/2}`. Its complete proof, unwound to primitive steps:

- **(S1)** *Split.* `Δ_n(c)=A_n(c)+B_n(c)` exactly (I1–I3). — Uses no
  constant; **no interaction with `a`.**
- **(S2)** *A-half, triangle.* `|A_n(c)|\le\sum_{K=0}^n b_K(c)\,
  \lvertφ_n^{(K)}-φ_K\rvert`. — No interaction with `a`.
- **(S3)** *A-half, insert `(U'_a)`.* `\le\frac an\sum_K b_K\sqrt K =
  \frac an\,E\big[\sqrt{\mathrm{Bin}(n,c/n)}\big]`. — **The single
  point where the value of `a` enters**, and it enters as a
  multiplicative constant applied uniformly to every term `0\le K\le n`
  of the Binomial support. All that is required of the hypothesis is
  that it hold *for every `K` in `\{0,\dots,n\}`* with one constant.
- **(S4)** *A-half, Jensen.* `E[\sqrt{\mathrm{Bin}}]\le
  \sqrt{E[\mathrm{Bin}]}=\sqrt{n\cdot c/n}=\sqrt c` (concavity of
  `\sqrt\cdot`), so `|A_n(c)|\le a\sqrt c/n`. — No interaction with `a`.
- **(S5)** *B-half.* `|B_n(c)|\le c^2I_2(c)/n\le κ_B/n` for `n\ge4`,
  `0\le c\le n` (I5–I7: `x=ct^2\in[0,c]\subseteq[0,n]` inside the
  integral, then Lema 6.1, then the sup over `c`). — Contains **no
  reference to `(U')`, to `A_n`, or to any constant `a` whatsoever.**
- **(S6)** *Combine.* Triangle inequality; then, `a\sqrt c+κ_B` being
  nondecreasing in `c`, `\sup_{[0,C]}|Δ_n|\le(a\sqrt C+κ_B)/n` for
  `C\le n`. — No interaction with `a` beyond carrying it.

**Conclusion of the trace.** The constant `a` appears in exactly one
step (S3), as a black-box multiplicative constant; the additive constant
`κ_B` (rounded up to `0.2805` for display) is produced exclusively by
(S5). Replacing `a` by any constant for which `(U')` holds on the full
range `0\le K\le n` — in particular `a^*`, per §3 — is a verbatim
substitution. **No step needs repair; nothing fails to close.**

---

## 3. The sharp `(U')` input, restated precisely

> **Fact (sharp `(U')`; PROVED, Estágio 19 — cited, not re-proved
> here).** For every integer `n\ge1` and every integer `0\le K\le n`:
> `\displaystyle \big|φ_n^{(K)}-φ_K\big| \;\le\; \frac{a^*\sqrt K}{n}`,
> with strict inequality for every `K\ge1` (and equality `0=0` at
> `K=0`).

Provenance, case by case, as catalogued in `THEOREM.md` Estágio 19:

- **`1\le K\le n-1`:** `n|φ_n^{(K)}-φ_K| = T(n,K) \le T(K{+}1,K) = M_K`
  (u_prime Theorem 2: `T(n,K)\ge0` and nonincreasing in `n`), and
  `M_K<a^*\sqrt K` strictly for every `K\ge1`
  (`sharp_constant_monotonicity_attempt` Theorem 2, via the
  FGKP95/Robbins non-asymptotic `Q(n)` upper bound and Lemma 4.1's
  `z_K`-bound).
- **`K=n`:** `n|φ_n^{(n)}-φ_n| = |Q(n)-nφ_n| < a^*\sqrt n` for every
  `n\ge1` (Estágio 19 referee report §8: upper side `n\ge3` via
  `3c^2<1` with `c=\tfrac1{11}\sqrt{π/2}+\sqrt π/4`; lower side
  `n\ge67` via Theorem 5 `Q(n)\ge\sqrt{πn/2}-6`; finite remainder
  `n\le80` verified in certified rational arithmetic; independently
  re-verified by the orchestrating session, `0` violations `n=1..300`,
  exact anchors `1/3` at `n=1` and `13/30` at `n=2`).
- **`K=0`:** `φ_n^{(0)}=1=φ_0` (no reroutes ⇒ uniform permutation ⇒
  every point cyclic), difference `0`.

The three cases exactly cover the support `\{0,1,\dots,n\}` of
`\mathrm{Bin}(n,c/n)` — which is exactly what step (S3) consumes.
Independent numerical re-verification of this input at ~1 490 certified
points (including `K` to `5000` exact and the `K=n` boundary to
`n=30\,000`): §7, T2 — zero violations.

---

## 4. Teorema R: the sharp explicit unconditional rate

> **Teorema R (PROVED).** For every integer `n\ge4` and every real
> `0\le c\le n`:
>
> `\displaystyle \big|φ(n,c)-φ_∞(c)\big| \;\le\; \frac{a^*\sqrt c + κ_B}{n},
> \qquad a^*=\sqrt π\Big(\frac1{\sqrt2}-\frac12\Big)=0.36708721\ldots,
> \quad κ_B=\sup_{c\ge0}c^2I_2(c)=0.28048017\ldots,`
>
> with **strict** inequality for every `c\in(0,n]` (at `c=0` the left
> side is `0`). Consequently, for every `0\le C\le n`:
> `\displaystyle \sup_{c\in[0,C]}\big|Δ_n(c)\big| \le \frac{a^*\sqrt C+κ_B}{n}`,
> and in decimal form (valid since `a^*<0.3670873`, `κ_B<0.2805`):
> `\displaystyle |Δ_n(c)| \;\le\; \frac{0.3670873\,\sqrt c + 0.2805}{n}.`

*Proof.* By I1–I3 (exact identities, `0\le c\le n`),
`Δ_n(c)=A_n(c)+B_n(c)`.

**A-half.** By the triangle inequality and the sharp `(U')` (§3),
applied to every `K` in the Binomial support,

`\displaystyle |A_n(c)| \le \sum_{K=0}^n b_K(c)\,\big|φ_n^{(K)}-φ_K\big|
\le \frac{a^*}n\sum_{K=0}^n b_K(c)\sqrt K
= \frac{a^*}n\,E\big[\sqrt{\mathrm{Bin}(n,c/n)}\big]
\le \frac{a^*}n\sqrt{E[\mathrm{Bin}(n,c/n)]} = \frac{a^*\sqrt c}{n},`

the last inequality by Jensen (concavity of `\sqrt\cdot`), and
`E[\mathrm{Bin}(n,c/n)]=c` exactly. For `c\in(0,n]` the middle
inequality is strict: some `K\ge1` has `b_K(c)>0`, and for every such
`K` the sharp `(U')` is strict (§3).

**B-half.** By I5, `B_n(c)=\int_0^1[(1-\tfrac{ct^2}n)^n-e^{-ct^2}]dt`;
by I6 with `x=ct^2\in[0,c]\subseteq[0,n]` (here `c\le n` and `n\ge4`
are used, and only here),
`|B_n(c)|\le\int_0^1\tfrac{c^2t^4}ne^{-ct^2}dt=\tfrac{c^2I_2(c)}n
\le\tfrac{κ_B}n` (I7).

**Combine.** `|Δ_n(c)|\le|A_n(c)|+|B_n(c)|<\tfrac{a^*\sqrt c}n+
\tfrac{κ_B}n` for `c\in(0,n]`; at `c=0`, `Δ_n(0)=1-1=0`. The
sup-over-`[0,C]` form follows because `a^*\sqrt c+κ_B` is nondecreasing
in `c` and the pointwise bound applies on all of `[0,C]\subseteq[0,n]`.
The decimal form follows from the certified brackets
`a^*<0.3670873` (§7 constants) and `κ_B<0.2805` (§5.2). `∎`

**What changed relative to Estágio 12, exhaustively:** (i) `a\mapsto
a^*` (factor `a/a^*=6.1384` improvement in the `\sqrt c` term); (ii)
strictness for `c>0` is now available (Estágio 12's `(U')` was stated
with `\le`; Estágio 19's is strict for `K\ge1`); (iii) the restriction
`C\le n` in the sup form, implicit in Estágio 12's "`n\ge4`,
`0\le c\le n`" preamble, is stated explicitly. **Nothing else changed;
in particular the domain `n\ge4`, `0\le c\le n` is exactly the old one**
(`n\ge4` being Lema 6.1's proof artifact — wave-11 referee note F-13
records that `n=2,3` also hold numerically, unproved, unchanged here).

---

## 5. The additive constant `κ^*`, honestly recomputed

### 5.1 Where `0.2805` comes from, and why it does not change

Tracing (S5): the additive constant is
`κ_B := \sup_{c\ge0} c^2I_2(c)`, `I_2(c)=\int_0^1t^4e^{-ct^2}dt`,
attained at `c=4.0867545\ldots` — a quantity manufactured entirely
inside the `B_n` (Binomial-vs-Poisson mixture) half of the split. The
constant `a` of `(U')` never appears in I5, I6, or I7; conversely `κ_B`
never appears in the `A_n` half. The two halves are added once, at the
very end (S6). Therefore the re-assembly with `a^*` leaves the additive
constant **exactly as it was**:

> `κ^* = κ_B = 0.280480169\ldots` — **unchanged.** The `0.2805` of
> Estágio 12 was, and remains, a decimal rounding-up of `κ_B`.

This is the honest recomputation the mandate asked for: the answer is a
*structural independence proof* (the constant lives in the half of the
assembly that has no `a` in it), not a coincidence of arithmetic. Had
the old assembly mixed the two halves before bounding (e.g. bounded
`|A_n|+|B_n|` jointly), the additive constant could have interacted
with `a`; it does not — the split (S1) is exact and the halves are
bounded separately.

### 5.2 Certified value (new here)

Estágio 12 reported `κ_B=0.280480169025` from a numerical sup
(`14\,000`-point scan); its wave-11 referee reproduced
`0.280480169024586` and noted (finding F-9) that "computed exactly" was
loose wording for a float-level evaluation of a transcendental sup.
This document supplies the missing certification
(`verify_kappa_star.py`, pure rational arithmetic, no float trust):

- **`κ_B < 0.2805` (the bound Teorema R's decimal form uses).**
  *Tail:* `c^2I_2(c)\le c^2\int_0^∞t^4e^{-ct^2}dt=\tfrac38\sqrt{π/c}`
  (Gaussian moment, by differentiating
  `\int_0^∞e^{-at^2}dt=\tfrac12\sqrt{π/a}` twice in `a`), decreasing in
  `c`, and at `c=5.62`: `\tfrac38\,\mathrm{hi}(\sqrt π)/
  \mathrm{lo}(\sqrt{5.62})\le0.2803742<0.2805` in certified rationals.
  *Head `[0,5.62]`:* branch-and-bound with the certified interval bound
  `\sup_{[c_1,c_2]}c^2I_2(c)\le c_2^2\,I_2^{\mathrm{hi}}(c_1)` (valid
  since `I_2` is decreasing in `c`), `I_2` evaluated by its exact
  alternating series `\sum_k(-c)^k/(k!(2k+5))` with rational bracketing
  of the remainder by the first omitted term: **1 525 certified leaves,
  3 049 interval evaluations, 0 failures**; tightest leaf clearance
  `1.8\cdot10^{-8}` at `c\approx4.107`.
- **`κ_B > 0.28048`:** single certified evaluation at
  `c_0=4.086754546`: `c_0^2I_2(c_0)\in(0.280480169024,
  0.280480169025)\ni` — in particular `>0.28048`.
- Display (non-load-bearing, `mpmath` 50 dps, closed form
  `c^2I_2(c)=\tfrac1{\sqrt c}\big[\tfrac{3\sqrt π}8\mathrm{erf}(\sqrt c)
  -e^{-c}(\tfrac{3\sqrt c}4+\tfrac{c^{3/2}}2)\big]` cross-checked
  against direct quadrature): `κ_B=0.280480169024586` at
  `c^*=4.08675454645254` — matching the wave-11 referee's value to all
  printed digits and Estágio 12's to its printed precision.

So `κ_B\in(0.28048,\,0.2805)` is now a certified statement, and every
numerical verification in §7 uses the conservative rational
`κ_{\mathrm{lo}}=0.28048` on the right-hand side (a *smaller* RHS than
the theorem's, so every PASS certifies the theorem's inequality).

---

## 6. How sharp is the sharp rate? (honest assessment)

- **The multiplicative constant `a^*` cannot be improved** in a bound
  of the shape `(a\sqrt c+κ)/n` valid on all of `0\le c\le n`: along
  the boundary line `c=n`, `n\,Δ_n(n) = Q(n)-nφ_∞(n)
  = a^*\sqrt n - \tfrac13 + O(1/\sqrt n)` (Estágio 13/19's two-sided
  `Q(n)` bounds plus Corolário 4.2), so
  `n|Δ_n(n)|/(a^*\sqrt n+κ_B)\to1`. The certified checks reproduce
  this: `LHS/RHS = 0.847` at `n=100`, `0.949` at `n=1000`, `0.970` at
  `n=3000` (T4/T5) — approaching `1` from below, never crossing it.
- **The additive constant is NOT claimed optimal.** On the interior
  (fixed `c`, `n\to\infty`) the truth is `n|Δ_n(c)|\to|e(c)|`
  (Teorema E, Estágios 10–11), and the sharp bound overshoots `|e(c)|`
  by the asymptotic factor `a^*\big/(\sqrt π/8)=4(\sqrt2-1)=1.6569`
  at large `c` (vs. `10.8` for the old bound), and by more at small
  `c` — the price of a bound that must also survive `c\asymp n`, where
  `|e(c)|` is no longer the truth. Both facts are displayed honestly in
  the T5 table (§7).
- **Improvement over Estágio 12:** the `\sqrt c` coefficient shrinks by
  the exact factor `a/a^* = (1+\sqrt{π/2})/(\sqrt{π/2}-\sqrt π/2)
  = 6.1384`; the full bound by a factor between `3.47` (`c=0.5`) and
  `5.90`+ (`c\to\infty`) on tested cells.

---

## 7. Validation (test log — all deterministic, no seeds)

Certified = exact `Fraction` arithmetic end-to-end, with all
transcendental quantities replaced by rational brackets rounded in the
conservative direction (LHS up, RHS down), so a PASS is a machine proof
of the inequality at that cell.

| Test | Script / log | What | Scale | Result |
|---|---|---|---|---|
| T1a | `verify_engine_anchors.py` / `.log` | fresh closed-form engine (`ψ`, `ψ^R`, Lema-A reduction — re-typed from prose) vs **brute-force enumeration from Definition 4** (all `π\in S_n`, all destination vectors; no closed form anywhere) | `n=4,5` all `K`; `n=6`, `K\le4`; `n=7`, `K\le2` — 19 pairs, exact | **19/19 exact** |
| T1b–d | same | prose anchors: `φ_n^{(1)}=\tfrac23+\tfrac1{3n^2}` and `ψ_n^{(1),R}=\tfrac12+\tfrac1{2n}` (`n\le50`), `φ_n^{(n-1)}=Q(n)/n` (`n\le40`, engine vs independent `Q` code), `φ_7^{(6)}=355081/823543`, `φ_K` anchors, mixture endpoints `φ(n,0)=1`, `φ(n,n)=Q(n)/n` (`n\le12`), `φ_∞` bracket consistency across the series/tail crossover | 18 checks | **18/18** |
| T2a | `verify_sharp_uprime.py` / `.log` | `M_K` identity cross-check: engine `T(K{+}1,K)` vs `Q(K{+}1)-(K{+}1)φ_K` | `K=1..200`, exact | **200/200 exact** |
| T2b | same | `0\le M_K<a^*\sqrt K` certified (`a^*_{\mathrm{lo}}`, `\sqrt{\phantom{K}}_{\mathrm{lo}}`) | `K=1..800` dense + sparse to `5000` (807 pts) | **0 violations**; max certified ratio `0.9873` at `K=5000` |
| T2c | same | interior `n`: `0\le T(n,K)\le M_K<a^*\sqrt K` + monotonicity in `n` | 72 cells, exact | **0 violations** |
| T2d | same | boundary `K=n`: `\lvert Q(n)-nφ_n\rvert<a^*\sqrt n` | `n=1..400` dense + exact to `2000` (406 pts) + certified-truncated `Q` at `n=5000,10^4,3\cdot10^4`; referee anchors `1/3`, `13/30` reproduced exactly | **0 violations** |
| T3 | `verify_kappa_star.py` / `.log` | `κ_B<0.2805` (branch-and-bound + tail, pure rational) and `κ_B>0.28048` (certified witness); mpmath display value | 3 049 interval evals + 1 witness | **CERTIFIED**, `κ_B\in(0.28048,0.2805)`; display `0.280480169024586` @ `4.08675454645254` |
| T4a | `verify_final_rate.py` / `.log` | **the final inequality**, certified: exact `φ(n,c)` (mixture I1 over the engine's `φ_n^{(K)}` table) vs `φ_∞` bracket vs `(a^*_{\mathrm{lo}}\sqrt c_{\mathrm{lo}}+0.28048)/n` | `n\in\{4..24,28,32,40,48,56,64,80,96,112,128,160,192,224,256,320,384,448,512\}` × ~52 `c`-values spanning `[0,n]` incl. `c=n,\,n-\tfrac14,\,n-\tfrac12,\,n-1`; `n=1024` × 12 | **0 violations** |
| T4b | same | the two halves separately: `\lvert A_n\rvert\le a^*\sqrt c/n` (exact `A_n`), `\lvert B_n\rvert\le c^2I_2(c)/n` (bracketed), and the exact Lema 5.1 identity `\sum_Kb_Kφ_K=\sum_k\binom nk(-c/n)^k/(2k{+}1)` | `n\in\{8,32,128\}` × 12 `c` = 36 cells × 3 checks | **0 violations** |
| T4c | same | boundary line `c=n` via `φ(n,n)=Q(n)/n`: exact `n=4..600` + `700,800,1000,1500,2000,3000`; certified-truncated `Q` at `n=5000,10^4,3\cdot10^4` | 606 cells | **0 violations** |
| — | T4 total | certified cells of the final inequality | **2 594** | **0 violations**; max `LHS/RHS=0.9700` at `(3000,3000)` |
| T5 | `compare_bounds.py` / `.log` | comparison table `n\lvertΔ_n\rvert` vs sharp vs old bound (`n\in\{16,64,256\}`, exact-driven), `n\to\infty` reference `\lvert e(c)\rvert`, boundary-tightness column | display | old/sharp ratio `3.47\to5.90`; `\mathrm{ratio}\to1` along `c=n` |

Excerpt of the T5 comparison (true values exact-rational; bounds
displayed to 6 d.p.):

| `n` | `c` | `n\lvertΔ_n(c)\rvert` | sharp `a^*\sqrt c+κ_B` | old `a\sqrt c+κ_B` | old/sharp |
|---|---|---|---|---|---|
| 256 | 1 | 0.036106 | 0.647567 | 2.533794 | 3.91 |
| 256 | 10 | 0.219808 | 1.441312 | 7.406085 | 5.14 |
| 256 | 100 | 2.181324 | 3.951352 | 22.813622 | 5.77 |
| 256 | 256 | 5.546475 | 6.153876 | 36.333506 | 5.90 |
| 3000 | 3000 | 19.774758 | 20.386675 | — | (ratio `0.970`) |

---

## 8. Self-caught issues (disclosed)

1. **`I_2` bracket returned a vacuous lower bound for `c>60` (checking
   code only).** First run of T4b flagged 7 "B-half violations" at
   `n=128`, `c\ge64` — not violations of anything: my `I2_bracket`
   switched to the tail *upper* bound at `c>60` and returned `0` as the
   lower end, so the diagnostic `\lvert B_n\rvert\le c^2
   I_2^{\mathrm{lo}}(c)/n` compared against `0`. Fixed by extending the
   exact alternating-series bracket to `c\le200` (`engine.py`); re-run
   clean. The final-inequality check (T4a/T4c) never used `I_2` and was
   unaffected — it showed 0 violations in both runs.
2. No other issue was caught. The first (pre-fix) T4 log also printed a
   summary line conflating the T4b diagnostic failure count with
   "violations of the final inequality"; the archived
   `verify_final_rate.log` is from the corrected, expanded run.

---

## 9. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Every step of the Estágio 12 assembly survives verbatim under `a\mapsto a^*`; the value of `a` enters the proof at exactly one step (S3) | **PROVED** (trace, §2; the one consumed property is `(U')` on `0\le K\le n`, supplied sharp by Estágio 19) |
| 2 | `κ^*=κ_B` — the additive constant is unchanged, by structural independence of the `B_n` half from `(U')`/`a` | **PROVED** (§5.1) |
| 3 | `κ_B\in(0.28048,\,0.2805)` | **PROVED, certified rational arithmetic** (§5.2, T3 — new; upgrades wave-11 F-9's float-level value) |
| 4 | **Teorema R**: `\lvertφ(n,c)-φ_∞(c)\rvert\le(a^*\sqrt c+κ_B)/n` for `n\ge4`, `0\le c\le n`, strict on `(0,n]`; sup form for `C\le n`; decimal form `[0.3670873\sqrt c+0.2805]/n` | **PROVED** (§4) |
| 5 | Final inequality verified, certified, at scale | **0 violations / 2 594 cells**, `n\le1024` interior, `n\le30\,000` boundary, `c` through `c=n` (T4) |
| 6 | Sharp `(U')` input independently re-verified | **0 violations / ~1 490 certified points** incl. `K=5000`, boundary `n=3\cdot10^4` (T2) |
| 7 | Fresh engine faithful to Definition 4 | **19/19 brute-force matches + 18/18 anchors** (T1) |
| 8 | `a^*` is optimal as the multiplicative constant in this bound shape (ratio `\to1` along `c=n`) | **NUMERICALLY CHARACTERIZED** + asymptotic argument (§6); the limit statement itself follows from Estágio 13/19's proved asymptotics, but no formal "optimality theorem" is claimed here |
| 9 | `κ_B` optimal as additive constant | **NOT claimed** (§6) |
| 10 | Domain extension to `n=2,3` | **NOT claimed** (inherited F-13 status: numerical only, unchanged) |

**Established (this document):** claims 1–5 above.
**Cited (already PROVED elsewhere, unchanged):** I1–I9 (§1), sharp
`(U')` (§3).
**Heuristic / not claimed:** claims 8–10's non-claimed parts.
**Open (named, for the catalogue):** a matching *lower*-order additive
constant (closing the gap `κ_B+\tfrac13` along `c=n`, or `4(\sqrt2-1)`
vs `1` in the interior) — i.e. a rate bound interpolating to the exact
profile `e(c)`; literal term-by-term monotonicity of `M_K/\sqrt K`
(inherited from Estágio 19, unchanged); `n\in\{2,3\}`.

---

## 10. Seeds

No randomness is used anywhere in this document — every object
(`φ_n^{(K)}`, `φ(n,c)`, `φ_K`, `φ_∞` brackets, `Q(n)`, `I_2`, `κ_B`)
is deterministic, and every load-bearing check is exact/certified.
Seed `20260862000+` is reserved for this front per `DISC-DEC-072`
(grep-confirmed before use to appear only in the ledger/queue
reservations) and **not used**, exactly as in every sibling document of
this lineage.

| seed | used for |
|---|---|
| `20260862000+` (reserved, `DISC-DEC-072`) | N/A — no randomness anywhere in this document |

---

## 11. Files, reproducibility

| file | role |
|---|---|
| `engine.py` | fresh exact/certified toolkit: closed-form `φ_n^{(K)}` (re-typed from prose of Estágio 9's Corolário A1 + Proposição 2.1 + Lema A), exact `Q(n)` + certified truncated bracket, mixture `φ(n,c)`, certified brackets for `\sqrt{\phantom c}`, `π`, `a^*`, `φ_∞(c)`, `I_2(c)`, brute-force enumerator from Definition 4 |
| `verify_engine_anchors.py` / `.log` | T1 (engine vs brute force + archive anchors), 37/37 |
| `verify_sharp_uprime.py` / `.log` | T2 (sharp `(U')` re-verification: identity, binding case, interior `n`, `K=n` boundary), 0 violations |
| `verify_kappa_star.py` / `.log` | T3 (`κ_B\in(0.28048,0.2805)` certified; branch-and-bound 3 049 evals; mpmath display value) |
| `verify_final_rate.py` / `.log` | T4 (**the final inequality**, 2 594 certified cells, 0 violations; per-half checks; Lema 5.1 identity; boundary line to `n=3\cdot10^4`) |
| `compare_bounds.py` / `.log` | T5 (sharp vs old vs true comparison table; `e(c)` reference; boundary-tightness column) |

Run order: `verify_engine_anchors.py`, `verify_sharp_uprime.py`,
`verify_kappa_star.py`, `verify_final_rate.py`, `compare_bounds.py`
(each independent; stdlib + `mpmath` only; `mpmath` never load-bearing).
Total runtime ≈ 4½ minutes, dominated by the `n=1024` exact mixture.

---

## Verdict

**The named "mechanical but unexecuted" item is now EXECUTED and
CLOSED.** The Estágio 12 assembly re-runs with the sharp constant
without a single step needing repair — the constant `a` was consumed at
exactly one point, as a black box, and Estágio 19's sharp `(U')` slots
in verbatim over the full range `0\le K\le n` that the Binomial mixture
requires. The additive constant is honestly recomputed and found
**unchanged** (`κ^*=κ_B`), for a structural reason (it lives entirely
in the mixture half of the assembly, which never references `(U')`),
and is now, for the first time, certified to `(0.28048,\,0.2805)` by
pure rational arithmetic. The resulting Teorema R —
`|φ(n,c)-φ_∞(c)|\le[a^*\sqrt c+κ_B]/n` for `n\ge4`, `0\le c\le n`,
strict on `(0,n]` — is verified with zero violations on 2 594 certified
cells reaching `n=1024` in the interior and `n=30\,000` on the boundary
line `c=n`, where the bound is observed (and asymptotically expected)
to be tight to within `3\%` — confirming that `a^*` is not just sharp
in `(U')` but the best possible multiplicative constant for this bound
shape. This is a positive result and, per this archive's discipline,
**requires independent adversarial review before being catalogued**;
nothing is integrated, promoted, or closed into `THEOREM.md` by this
document itself.
