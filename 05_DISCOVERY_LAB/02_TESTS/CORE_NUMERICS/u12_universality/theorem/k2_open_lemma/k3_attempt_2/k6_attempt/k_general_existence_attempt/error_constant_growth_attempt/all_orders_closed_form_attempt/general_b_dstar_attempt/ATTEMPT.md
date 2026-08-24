# The general-`b` closed form for `D^{*(p)}_r(b)`: the prefactor-collapse route, carried through for `p=1,2,3,4`

> **Governance.** Wave 14, front (d), authorized by `DISC-DEC-057` item (d)
> (`GENERAL-B-DSTAR-ATTEMPT`). Target: the general-`b` closed form for the sharp
> error constants `D^{*(p)}_r(b)`, `b\ge2`, left OPEN by
> `all_orders_closed_form_attempt/ATTEMPT.md` §6.3 items 3–4 (as corrected
> post-adversarially, 2026-08-23). Pure combinatorics — no external data, no
> holdout, no real-world claim, no governance edits. **Nothing outside this
> directory was created, modified or deleted.** No git commit was made. Every
> claim below is labeled PROVED, NUMERICALLY VERIFIED, or OPEN.

> **Executive summary (read first).**
>
> 1. **The recommended route closes, for `p=1,2,3,4`, at every `b\ge0`.** The
>    mandate named the exact obstruction (`\Phi_b(r)` stops being polynomial in
>    `r` at `b\ge2`) and the exact recommended route (a Teorema-3′-style
>    prefactor collapse). Carrying that route through explicitly gives an exact,
>    closed-form expression for `D^{*(p)}_r(b)` at every `b\ge0`, for
>    `p=1,2,3,4` — not just `p=1` as the mandate's "at least" asked for.
> 2. **The mechanism generalises the referee's own `p=2` result (Teorema 3′,
>    wave 10) to a `p`-uniform machine.** The key structural facts, each PROVED
>    and each *independent of `p`*: (i) the polynomial `Q_p(u):=c(u{+}1,u{+}1{-}p)`
>    that carries all the `p`-dependence vanishes for `u<p`, so a truncated sum can
>    always be extended to a full half-range "for free"; (ii) under
>    `v:=\alpha-N/2`, the "distance from center" variable `u=r-\alpha` becomes
>    `-(v+\beta/2)`, `\beta:=b{+}1`, **for every `p`**; (iii) the resulting
>    even/odd split of `Q_p` in `v` turns the sum into (a full symmetric moment
>    sum) minus (an explicit `b`-term strip), via the same reflection
>    `\alpha\mapsto N-\alpha` the referee used; (iv) a **general-`k`** prefactor
>    collapse, proved here in one line for every `k` (not fitted case by case),
>    `P_b\cdot[N]_k\cdot(r{-}k{+}1)\cdot\binom{N-k}{r-k+1}=[r]_k`, turns every
>    partial odd-moment sum into an explicit polynomial in `r,b`.
> 3. **Two new exact combinatorial identities were needed and derived**: `I5`
>    and `I7`, the quintic and septic analogues of the referee's `I1,I3`
>    (`\sum_{i=0}^m(N{-}2i)^{5}\binom Ni` and the `^7` version), each proved by
>    the same Abel-summation-by-parts technique the referee used to get `I3`
>    from `I1`, and each verified exhaustively (`N\le39`/`N\le34`, every `m`,
>    `0` mismatches).
> 4. **The resulting closed forms reduce to every already-PROVED calibration
>    formula character-for-character**: `D^{*(p)}_r(0)` for `p=1,2` and
>    `D^{*(p)}_r(1)` for `p=1,2,3,4` — including the `p=2,b=1` case, itself a
>    PROVED specialisation of Teorema 3′ — all checked as exact `Fraction`
>    identities for `r=0,\dots,200`, not merely spot-checked.
> 5. **New, previously-unknown closed forms are produced for `b\ge2`.** E.g.
>    `\displaystyle D^{*(1)}_r(2)=\frac{(r{+}2)(r{+}3)}{2(2r{+}3)}\varphi_r-\frac{r{+}2}{2(r{+}1)}`
>    — and this is the answer to the open question named by the mandate: the
>    coefficient of `\varphi_r` is genuinely a **rational function of `r`**, not
>    a polynomial, confirming exactly why the `\{r^q\varphi_r\}\cup\{r^q\}`
>    polynomial basis was structurally doomed at `b\ge2`.
> 6. **What is not closed for general `p`:** the identities `I_{2k+1}`
>    needed for `p\ge5` (`I9,I11,\dots`) are not derived (the recursive
>    mechanism that produced `I5,I7` from `I1,I3` is exhibited and looks
>    mechanical, but is verified only at the two instances used, not proved for
>    general `k`). This is named precisely in §7.

---

## 0. Disciplina

**Sources read, in the order the task mandated, before any derivation:**

1. `00_GOVERNANCE/DECISION_LEDGER.yaml`, entry `DISC-DEC-057` (mandate and scope
   for wave 14 front (d)).
2. `all_orders_closed_form_attempt/ATTEMPT.md` in full — §1 (definitions of
   `g_r,h_r`, `(\ast)`, `(\ast\ast)`), §3 (Theorem M, the Stirling-number
   multiplier `M_p(k)=c(k{+}p{+}1,k{+}1)`), §4 (Theorem A, the exact all-orders
   closed form, and Corollary A3, `D^{*(p)}_r(b):=\Phi^{[p]}_r(1,b)=\sum_{j=p}^r
   c_j^{(r)}(b)c(j{+}1,j{+}1{-}p)`), and §6.3 items 3–4 in full, including the
   `[Correção pós-adversarial, 2026-08-23]` block naming the exact obstruction
   (`\Phi_b(r)` collapses to a constant only at `b\in\{0,1\}`) and the exact
   recommended route (a Teorema-3′-style prefactor collapse, not a naive
   basis fit).
3. `error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3 (Theorem
   3′, the referee's own exact general-`b` closed form for the `p=2` case)
   read in full, including its proof: the two boundary identities `I1,I3`
   (§3.1), the even/odd split and Wallis-type moment computation (§3.2 of the
   parent, reused via §3.0's half-sum), and the reflection argument that turns
   a truncated half-range sum into a full symmetric sum minus a `b`-term strip
   (§3.3).

**Reuse policy (same convention as every predecessor in this lineage).** Every
script in this directory is written from scratch. **Used as fixed, already-PROVED
input, never re-derived:** the definition `D^{*(p)}_r(b)=\Phi^{[p]}_r(1,b)=
\sum_{j=p}^r c_j^{(r)}(b)c(j{+}1,j{+}1{-}p)` (Corollary A3 of the target document;
`ground_truth.py` implements exactly this formula, with its own from-scratch
unsigned-Stirling table, and is the sole ground truth every derived formula here
is checked against). **Used only as calibration targets, never as derivation
input:** the four `b=1` formulas quoted in the task, the two `b=0` formulas
`\tfrac r4\varphi_r` and Estágio 8's Teorema 3, and the referee's Teorema 3′
statement (its formula is not transcribed into any derivation step here; instead
an independent derivation is carried out from Corollary A3 alone, and the two are
compared only via numerical/algebraic agreement — see §5 and §6.2).

**Exactness policy.** `fractions.Fraction` / `sympy.Rational` / `sympy.Symbol`
throughout every script. No floating point anywhere in this directory. Every claim
labelled PROVED rests on an explicit algebraic identity (stated and, where
non-trivial, proved in §3–§4 below), independently corroborated by exhaustive
exact numerical sweeps.

**No randomness.** Every verification here is an exhaustive sweep over a stated
finite integer range; nothing is randomised. The reserved seed range
`20260837000+` (front (d) of `DISC-DEC-057`) was therefore not used. Confirmed
unused elsewhere in the archive before `DERIVATION_PREREG.md` was written
(`grep -rn "20260837" 05_DISCOVERY_LAB/` — the only hit is the ledger's own
reservation line for this wave).

**Pre-registration.** `DERIVATION_PREREG.md` in this directory was written and
committed to before any non-throwaway verification run in this directory (it
names the route, the concrete deliverable, and the honesty criteria in advance).
A handful of hand-algebra sanity checks were run off-repository beforehand
purely to catch arithmetic slips (one such slip *was* caught this way — see
§4.5) before committing to the plan; none of their output is cited as evidence
anywhere in this document. Every number below is reproduced by the scripts in
this directory, logged in `*.log` files alongside them.

---

## 1. The target, restated precisely

Fix `p\ge0`. Recall (already PROVED, `all_orders_closed_form_attempt/ATTEMPT.md`
§4.3, Corollary A3):

`\displaystyle D^{*(p)}_r(b):=\lim_{n\to\infty}\max_m n^p\big|R^{(p)}_r(m,b,n)\big|
=\Phi^{[p]}_r(1,b)=\sum_{j=p}^{r}c_j^{(r)}(b)\cdot c(j{+}1,\,j{+}1{-}p)`,

`\displaystyle c_j^{(r)}(b):=\frac{r!}{(r-j)!\prod_{i=1}^{j+1}(r+b+i)}`, `c(N,M)`
the unsigned Stirling numbers of the first kind. This is a finite, exact,
computable quantity for every `r,b,p\ge0` — the open question is not whether it
exists but whether it has a **closed form** in `r` for fixed `b,p`, valid for
**every** `b`, not just `b\in\{0,1\}`.

**Known calibration.** `D^{*(p)}_r(0)` PROVED for `p=0,1,2` (`\varphi_r`,
`\tfrac r4\varphi_r`, Estágio 8 Teorema 3). `D^{*(p)}_r(1)`, PROVED for `p=2`
(Teorema 3′ specialised at `b=1`), NUMERICALLY VERIFIED to `r=400` for
`p=1,3,4`:

`D^{*(1)}_r(1)=\tfrac{r+1}4\varphi_r-\tfrac14`,
`\;D^{*(2)}_r(1)=\tfrac{(r+1)(3r+8)}{32}\varphi_r-\tfrac{5r+6}{24}`,
`\;D^{*(3)}_r(1)=\tfrac{(r+1)(5r^2+39r+32)}{128}\varphi_r-\tfrac{(r+1)(7r+12)}{48}`,
`\;D^{*(4)}_r(1)=\tfrac{(r+1)(105r^3+1765r^2+3314r+1536)}{6144}\varphi_r-\tfrac{45r^3+229r^2+306r+120}{480}`.

**The named obstruction.** The referee's Teorema 3′ prefactor
`\Phi_b(r):=2\varphi_r\prod_{j=1}^b\frac{2r+2j}{2r+j+1}` collapses to `2\varphi_r`
exactly at `b\in\{0,1\}` (the `j=1` factor `(2r+2)/(2r+2)=1` identically) and is a
genuine rational — not polynomial — function of `r` times `\varphi_r` for
`b\ge2`. This is *why* the `\{r^q\varphi_r\}\cup\{r^q\}` basis is refuted for
`b\ge2`: no finite-degree polynomial-times-`\varphi_r` basis can represent a
`\varphi_r`-coefficient that is a genuine rational function of `r`.

---

## 2. The route, in outline

`N:=2r+b+1`, `\beta:=b+1`, `P_b:=r!(r+b)!/N!` (so `c_j^{(r)}(b)=P_b\binom N{r-j}`,
an elementary rewrite already used by the referee, §3.0).

**Step 1 (extend the sum for free).** `Q_p(u):=c(u{+}1,u{+}1{-}p)=e_p(1,\dots,u)`
(elementary symmetric polynomial of degree `p` in `1,\dots,u`) vanishes for
`u<p` — fewer than `p` distinct factors available. Hence

`\displaystyle D^{*(p)}_r(b)=P_b\sum_{\alpha=0}^{r}Q_p(r-\alpha)\binom N\alpha`,

the sum extended from `\alpha\le r-p` to `\alpha\le r` for free, since the added
terms (`\alpha=r-p+1,\dots,r`, i.e. `u=p-1,\dots,0`) vanish identically. This is
`p`-uniform: it holds for **every** `p`, generalising the referee's ad-hoc
observation (specific to `p=2`, their §3.0: *"the range extends to `i\le r` free
of charge (`w` has the factors `u` and `u{-}1`, vanishing at `i=r` and
`i=r{-}1`)"*) to a structural fact about `Q_p` for arbitrary `p`.

**Step 2 (the `p`-uniform substitution).** Put `v:=\alpha-N/2`. Then
`u:=r-\alpha=-(v+\beta/2)`, independent of `p`. Since `Q_p` has degree `2p` in
`u` (classical: `e_p(1,\dots,u)` is a polynomial in `u` of degree `2p`, via
Newton's identities and the Faulhaber power-sum polynomials), `Q_p(r-\alpha)`
becomes a degree-`2p` polynomial in `v`, coefficients depending on `b` (via
`\beta`) but **not on `r`**. Split into even part `E_p(v)` and odd part `O_p(v)`.

**Step 3 (even part: full symmetric sum minus a `b`-strip).** The reflection
`\alpha\mapsto N-\alpha` maps `\{r{+}b{+}1,\dots,N\}` onto `\{0,\dots,r\}` and
fixes the `b`-term strip `\{r{+}1,\dots,r{+}b\}` setwise. Since `E_p` is even and
`\binom N\alpha=\binom N{N-\alpha}`,

`\displaystyle \sum_{\alpha=0}^r E_p\binom N\alpha
=\tfrac12\Big[\sum_{\alpha=0}^N E_p\binom N\alpha-\sum_{\alpha=r+1}^{r+b}E_p\binom N\alpha\Big]`.

The first (full) sum is `2^N` times a polynomial in `N` built from the central
moments `\mu_{2l}(N)` of `\mathrm{Bin}(N,\tfrac12)`; `P_b\cdot2^N=\Phi_b(r)`
exactly (the referee's own named object). The second (strip) sum is a genuine
finite sum of `b` explicit terms — this is the honest, irreducible source of the
non-polynomiality at `b\ge2`.

**Step 4 (odd part: partial-sum identities, collapsed to explicit polynomials).**
`P_b\sum_{\alpha=0}^r v^{2k-1}\binom N\alpha` reduces to `P_b` times
`S_{2k-1}(N,r):=\sum_{\alpha=0}^r(N-2\alpha)^{2k-1}\binom N\alpha` (referee's
`I1,I3` at `k=1,2`; `I5,I7` new here, at `k=3,4`), each of which collapses to an
explicit polynomial in `r,b` via a general-`k` prefactor-collapse identity
proved in §3.4.

---

## 3. The four ingredients, proved

(Full code and logs: `ingredients.py` / `ingredients.log`.)

### 3.1 `Q_p(u)`, degree `2p`, vanishing below `p`

Classical fact, stated for completeness: `e_p(1,\dots,u)` is a polynomial in `u`
of degree `2p`. *Proof sketch.* `\prod_{k=1}^u(1{+}kx)=\sum_p e_p(1,\dots,u)x^p`;
taking `\log` and differentiating gives the power sums
`P_m(u):=\sum_{k=1}^u k^m`, each a polynomial in `u` of degree `m{+}1`
(Faulhaber); Newton's identities express `e_p` as a universal (`u`-independent)
polynomial in `P_1,\dots,P_p`, and the top-degree term (`P_1^p/p!`, degree `2p`)
dominates. `\square` Given the a-priori degree bound, `Q_p` is *determined* by
`2p{+}1` exact values, computed here from the same from-scratch unsigned-Stirling
table `ground_truth.py` uses (not from any formula transcribed from a
predecessor). `Q_poly(p)` interpolates on `u=0,\dots,2p` and is then checked
against `15` further out-of-sample points, all exact:

`Q_0(u)=1`, `\;Q_1(u)=\tfrac{u^2+u}2`,
`\;Q_2(u)=\tfrac{u^4}8+\tfrac{u^3}{12}-\tfrac{u^2}8-\tfrac u{12}`,
`\;Q_3(u)=\tfrac{u^6}{48}-\tfrac{u^5}{48}-\tfrac{u^4}{16}+\tfrac{u^3}{48}+\tfrac{u^2}{24}`,
`\;Q_4(u)=\tfrac{u^8}{384}-\tfrac{u^7}{96}-\tfrac{u^6}{576}+\tfrac{u^5}{30}-\tfrac{5u^4}{1152}-\tfrac{u^3}{32}+\tfrac{u^2}{288}+\tfrac u{120}`.

(`Q_1,Q_2` match the referee's `c(N,N{-}1)=\binom N2`,
`c(N,N{-}2)=\tfrac{3N-1}4\binom N3` exactly once `N=u{+}1` is substituted — an
independent cross-check, since these were derived here by interpolation, not by
transcribing the referee's formulas.)

### 3.2 Central moments of `\mathrm{Bin}(N,\tfrac12)`, orders `2,4,6,8`

`\mu_{2l}(N):=2^{-N}\sum_{\alpha=0}^N(\alpha-N/2)^{2l}\binom N\alpha`. Classical:
the centered sum of `N` iid `\mathrm{Bernoulli}(\tfrac12)` has cumulant
generating function `K(t)=N\log\cosh(t/2)`; expanding
`M(t)=e^{K(t)}=\sum\mu_k(N)t^k/k!` as a power series (here done by `sympy`,
`ingredients.py:_derive_moment_formulas`, not by hand) gives

`\mu_2(N)=\tfrac N4`, `\;\mu_4(N)=\tfrac{N(3N-2)}{16}`,
`\;\mu_6(N)=\tfrac{N(15N^2-30N+16)}{64}`,
`\;\mu_8(N)=\tfrac{105N^4}{256}-\tfrac{105N^3}{64}+\tfrac{147N^2}{64}-\tfrac{17N}{16}`.

(`\mu_2,\mu_4` match the referee's §3.2 exactly, `\mu_2=N/4`,
`\mu_4=N(3N{-}2)/16` — an independent re-derivation via a different method
[cumulant generating function vs. their direct combinatorial argument], not a
transcription.) Each verified exhaustively by direct summation, `N\le20`, `0`
mismatches.

### 3.3 Two new identities: `I5` and `I7`

`I1` (`S_1(N,m)=(m{+}1)\binom N{m+1}`) is the direct telescope
`(N{-}2i)\binom Ni=A(i)-A(i-1)`, `A(i):=(i{+}1)\binom N{i+1}` (using
`(i{+}1)\binom N{i+1}=(N-i)\binom Ni`). `I3` (referee, PROVED) follows by Abel
summation of `(N{-}2i)^2` against this same `A(i)`.

**`I5` (NEW).** Abel-summing `(N{-}2i)^4` against `A(i)`:
`\displaystyle S_5(N,m)=(N{-}2m)^4(m{+}1)\binom N{m+1}-\sum_{i=0}^{m-1}A(i)\,\Delta f(i)`,
`f(i):=(N{-}2i)^4`. With `j:=i{+}1`, `y:=N{-}2j`, `\Delta f(j{-}1)=y^4-(y{+}2)^4`,
and `jB_j=N\binom{N-1}{j-1}` (`B_j:=\binom Nj`), substituting `l:=j{-}1`,
`M:=N{-}1`, `w:=M{-}2l` gives `y=w{-}1`. Expanding
`y^4-(y+2)^4=-(8y^3{+}24y^2{+}32y{+}16)` in `w{-}1` and collecting by degree, the
**even-degree-in-`w` terms cancel exactly** (`w^4,w^2,w^0` coefficients: `0,0,0`
— checked symbolically, `verify_S7_collapse`-style, and in `ingredients.py`'s
by-hand derivation comment), leaving only

`\displaystyle S_5(N,m)=(N{-}2m)^4(m{+}1)\binom N{m+1}+8N\big[S_3(N{-}1,m{-}1)+S_1(N{-}1,m{-}1)\big]`.

**`I7` (NEW).** The same technique one level deeper, Abel-summing
`(N{-}2i)^6`: the sextic `\Delta f` again collapses onto only the odd-`w` terms
(`w^5,w^3,w^1` survive with coefficients `12,40,12`; `w^4,w^2,w^0` cancel):

`\displaystyle S_7(N,m)=(N{-}2m)^6(m{+}1)\binom N{m+1}+N\big[12S_5(N{-}1,m{-}1)+40S_3(N{-}1,m{-}1)+12S_1(N{-}1,m{-}1)\big]`.

Both proved by this construction (not merely fitted) and verified exhaustively
against direct summation: `I5` at every `(N,m)`, `N\le39` (`820` pairs); `I7` at
every `(N,m)`, `N\le34` (`630` pairs); `0` mismatches, both (`ingredients.log`).

### 3.4 The general-`k` prefactor-collapse family (closes Step 4 for every `k`)

> **Proposition (general `k`, PROVED).**
> `\displaystyle P_b\cdot[N]_k\cdot(r{-}k{+}1)\cdot\binom{N-k}{r-k+1}=[r]_k`
> for every `k\ge0`, where `[x]_k:=x(x{-}1)\cdots(x{-}k{+}1)` and both sides are
> `0` by convention when `r<k`.

*Proof.* `[N]_k\cdot(N{-}k)!=N!` exactly, so

`\displaystyle P_b[N]_k(r{-}k{+}1)\binom{N-k}{r-k+1}
=\frac{r!(r{+}b)!}{N!}\cdot N!\cdot\frac{r{-}k{+}1}{(r{-}k{+}1)!(N{-}r{-}1)!}
=\frac{r!(r{+}b)!(r{-}k{+}1)}{(r{-}k{+}1)!(N{-}r{-}1)!}`.

`(r{-}k{+}1)/(r{-}k{+}1)!=1/(r{-}k)!` (`r\ge k`), and `N{-}r{-}1=r{+}b` exactly
(from `N=2r{+}b{+}1`), so `(N{-}r{-}1)!=(r{+}b)!`, which cancels the `(r{+}b)!`
standing in the numerator, leaving `r!/(r{-}k)!=[r]_k`. `\blacksquare`

This is a **one-line** general proof, not a case-by-case fit — it subsumes the
referee's own two named collapses as special cases: `k=0` is
`P_b(r{+}1)\binom N{r+1}=1`, exactly their stated identity; and their
`P_b\binom{N-1}r=\tfrac1N` is, up to multiplying both sides by `N` and then by
`r`, the same content as the `k=1` instance
`P_b\cdot N\cdot r\cdot\binom{N-1}r=r=[r]_1` used below (not a verbatim quote —
the referee state it in the `1/N` form, this document uses the rescaled form
that composes directly with the rest of §4). Verified numerically for
`k=0,\dots,6`, `b\le8,r\le15`
(`0` mismatches) and **symbolically**, general `r,b`, for `k=0,1,2,3`
(`sympy.simplify`, `0` residual in every case) — `ingredients.py`,
`verify_collapse_symbolic` / `verify_collapse_general_k`.

Applying this at `k=1,2,3` gives the odd-partial-sum closed forms actually used
in §4 (writing `P_b\cdot(\cdot)` throughout, `\beta=b{+}1`):

`P_b\sum_{\alpha=0}^r v\,\binom N\alpha=-\tfrac12`,
`\qquad P_b\sum_{\alpha=0}^r v^3\binom N\alpha=-\tfrac18(\beta^2{+}4r)`,

`P_b\sum_{\alpha=0}^r v^5\binom N\alpha
=-\tfrac1{32}\big[\beta^4+8r\big((\beta{+}1)^2{+}1\big)+32r(r{-}1)\big]`,

`P_b\sum_{\alpha=0}^r v^7\binom N\alpha
=-\tfrac1{128}\Big[\beta^6+r\big(12(\beta{+}1)^4{+}40(\beta{+}1)^2{+}12\big)
+r(r{-}1)\big(96(\beta{+}2)^2{+}256\big)+384\,r(r{-}1)(r{-}2)\Big]`

(each obtained by substituting the explicit `I5`/`I7` closed forms into the
`k=1,2,3` collapse identity above; each an explicit **polynomial** in `r`, no
binomial coefficients remaining).

---

## 4. The assembled closed forms

(Full code: `assemble.py`; logs: `assemble.log`.)

### 4.1 `p=1` (the mandated target)

`E_1(v)=\tfrac{v^2}2+\tfrac{\beta^2-2\beta}8`, `O_1(v)=\tfrac{b}2v`
(`Q_1(u)=\tfrac{u^2+u}2` under `u=-(v+\beta/2)`). Assembling via §2–§3:

> **Theorem D1 (PROVED, every `b\ge0`).**
> `\displaystyle D^{*(1)}_r(b)=\frac{\Phi_b(r)}{16}\big[2r+b(b{+}1)\big]
> -\frac b4-\frac12\sum_{j=1}^{b}E_1\!\Big(j-\frac\beta2\Big)\,w_j(r,b)`,
> `\qquad w_j(r,b):=\dfrac{r!(r{+}b)!}{(r{+}j)!(r{+}b{+}1{-}j)!}`.

At `b=0` the strip is empty: `D^{*(1)}_r(0)=\tfrac{2\varphi_r}{16}\cdot2r=\tfrac
r4\varphi_r` — the PROVED formula, exactly. At `b=1`: `\Phi_1(r)=2\varphi_r`
(the `j=1` factor collapses to `1`), `\beta=2`, and the single strip term
`E_1(0)=0` vanishes, giving `D^{*(1)}_r(1)=\tfrac{2\varphi_r}{16}(2r{+}2)-\tfrac14
=\tfrac{r+1}4\varphi_r-\tfrac14` — **the PROVED calibration formula, character
for character**.

**Concrete new instances, `b=2,3`** (strip now genuinely non-trivial):

`\displaystyle D^{*(1)}_r(2)=\frac{(r{+}2)(r{+}3)}{2(2r{+}3)}\,\varphi_r-\frac{r{+}2}{2(r{+}1)}`,

`\displaystyle D^{*(1)}_r(3)=\frac{(r{+}3)(r{+}6)}{2(2r{+}3)}\,\varphi_r-\frac{3r^2+17r+24}{4(r+1)(r+2)}`.

These are the answer to the question the mandate posed: the `\varphi_r`
coefficient is manifestly a **rational function of `r`** (denominator `2r{+}3`,
not a constant), confirming precisely why no finite polynomial-times-`\varphi_r`
basis could ever represent `D^{*(1)}_r(b)` at `b\ge2` — not "basis too small",
structurally impossible for *any* finite polynomial basis of that shape.

### 4.2 `p=2` (independent re-derivation, cross-checked against Teorema 3′)

`Q_2(u)=\tfrac{u^4}8+\tfrac{u^3}{12}-\tfrac{u^2}8-\tfrac u{12}` gives
`E_2,O_2` with both `\mu_2,\mu_4` and `I1,I3` needed. The assembled formula (full
expression: `assemble.py::D_formula(2,r,b)`) reduces to `\tfrac{r(3r+1)}{32}
\varphi_r-\tfrac r{12}` at `b=0` and to
`\tfrac{(r+1)(3r+8)}{32}\varphi_r-\tfrac{5r+6}{24}` at `b=1` — both PROVED
formulas, exactly. At `b=2,3`:

`\displaystyle D^{*(2)}_r(2)=\frac{3r^3+33r^2+94r+80}{16(2r+3)}\,\varphi_r
-\frac{2r^2+9r+10}{6(r+1)}`,

`\displaystyle D^{*(2)}_r(3)=\frac{3r^3+58r^2+265r+354}{16(2r+3)}\,\varphi_r
-\frac{(r+3)(11r^2+75r+118)}{24(r+1)(r+2)}`.

This is derived here from Corollary A3 **alone**, via §2–§3, with no formula
transcribed from the referee's Teorema 3′ at any step — and it matches
`D^{*(2)}_r(b)` (ground truth) exactly for `b\le10,r\le60` (`671` exact checks,
`0` failures). Since Teorema 3′ is itself PROVED and is exactly `D^{*(2)}_r(b)`,
this is an **independent re-derivation of an already-PROVED theorem**, via a
cleaner, `p`-uniform route — strong end-to-end validation that §2–§3's general
method is correct, not merely that it happens to fit `p=1`.

### 4.3 `p=3,4` (new, general `b`)

Needing `\mu_6` and `I5` (`p=3`), then `\mu_8` and `I7` (`p=4`) as well —
everything derived in §3. `D^{*(3)}_r(b)` reduces to `\tfrac{5r^3+9r^2+2r}{128}
\varphi_r-\tfrac{r^2}{12}` at `b=0` (matching the referee's structure-theorem
result, §11 of that report's scorecard) and to the PROVED `D^{*(3)}_r(1)` at
`b=1`, character for character. `D^{*(4)}_r(b)` likewise reduces correctly at
`b=0,1`. New instance:

`\displaystyle D^{*(3)}_r(2)=\frac{5r^4+104r^3+501r^2+914r+576}{64(2r+3)}\,\varphi_r
-\frac{5r^3+39r^2+94r+72}{24(r+1)}`.

### 4.4 Verification summary

| check | scope | result |
|---|---|---|
| `Q_p(u)` interpolation + out-of-sample | `p=0..4`, `15` extra pts each | `0` failures |
| central moments `\mu_2,\mu_4,\mu_6,\mu_8` | `N\le20` | `0` failures |
| `I1,I3` re-derived | `N\le60`, all `m` | `0` failures |
| `I5` (NEW) | `N\le39`, all `m` (`820` pairs) | `0` failures |
| `I7` (NEW) | `N\le34`, all `m` (`630` pairs) | `0` failures |
| collapse family, numeric | `k\le6`, `b\le8`, `r\le15` | `0` failures |
| collapse family, symbolic (general `r,b`) | `k=0,1,2,3` | `0` residual |
| `D^{*(p)}_r(1)`, `p=1,2,3,4` vs the PROVED calibration formulas | `r=0..200` each | `0` failures (character-for-character) |
| `D^{*(p)}_r(0)`, `p=1,2` vs the PROVED formulas | `r=0..200` | `0` failures |
| `D^{*(1)}_r(b)` vs ground truth (Corollary A3) | `b\le20,r\le150` | **3171** checks, `0` failures |
| `D^{*(2)}_r(b)` vs ground truth | `b\le10,r\le60` | **671** checks, `0` failures |
| `D^{*(3)}_r(b)` vs ground truth | `b\le10,r\le60` | **671** checks, `0` failures |
| `D^{*(4)}_r(b)` vs ground truth | `b\le10,r\le60` | **671** checks, `0` failures |

**Total: `5184` exact exhaustive equality checks against ground truth (Corollary
A3) across `p=1,2,3,4`, plus `1206` character-for-character calibration checks
against the PROVED `b=0,1` formulas, plus `6324` exact checks at the
ingredient level (`Q_p` out-of-sample points, central moments, `I1,I3,I5,I7`,
the collapse family) — `12714` exact checks in all, `0` mismatches anywhere.**

### 4.5 A self-caught error, disclosed

The first hand-algebra pass at `D^{*(1)}_r(2)` (done off-repository, before the
scripts here existed) produced `-(3r{+}4)/(4(r{+}1))` for the non-`\varphi_r`
remainder — **wrong**. It was caught immediately because it failed the `r=1`
exact check against ground truth (`1/20` predicted `-3/40`). The bug was in the
strip-sum arithmetic (`\Sigma(j^2{-}j\beta)w_j` mis-summed by hand); recomputing
that one intermediate quantity with `sympy` instead of by hand gave the correct
`-\ (r{+}2)/(2(r{+}1))`, which is what appears in §4.1. This is recorded here
per the archive's convention of disclosing self-caught errors (cf. the target
document's own §6.4 sign-error disclosure), and is why **every** intermediate
piece used in the final assembly (§3.1–§3.4) was independently verified
exhaustively before being composed, rather than trusted from a single hand
derivation.

---

## 5. What this resolves, precisely

The mandate's exact recommended route — a Teorema-3′-style prefactor collapse —
closes for `p=1` (the "at least" target), and the mechanism used to close it
turned out to be entirely `p`-uniform (Steps 1–4 of §2 use no `p`-specific fact
except the degree and vanishing of `Q_p`), so it closes for `p=2,3,4` as well
with no change of method, only two new lower-level identities (`I5,I7`). This is
strictly more than "a rigorous partial result for one specific `p`" — the task's
"very good" tier — for four values of `p` simultaneously, all reducing correctly
to the known `b\in\{0,1\}` calibration.

**Item 3 of the target document's §6.3 is now resolved** for `p=1,2,3,4`: the
`\{r^q\varphi_r\}\cup\{r^q\}` basis is not merely "refuted, route named" but
**replaced** by an exact closed form of the correct, non-polynomial shape
(`\varphi_r` times a rational function of `r`, plus an explicit finite `b`-term
correction), matching precisely what §6.3's post-adversarial correction
predicted the right answer should look like.

---

## 6. What this does **not** do

1. **It does not close general `p`.** `I5,I7` are proved for the specific
   instances needed (`p=3,4`); the pattern that produced them (Abel summation
   against `A(i)`, with the "offset" terms cancelling to leave only odd-`w`
   contributions) is exhibited twice and looks mechanical, but the general-`k`
   statement "`I_{2k+1}` reduces to `I_{2k-1},I_{2k-3},\dots,I_1` at
   `(N{-}1,m{-}1)` with all even-`w` terms cancelling" is **not proved for
   general `k`** here — only observed at `k=2,3`. This is the one piece of the
   route that is not yet `p`-uniform in the way §3.4's collapse family is.
2. **The strip sum is not further reduced.** `\sum_{j=1}^b E_p(j{-}\beta/2)w_j`
   is left as an explicit `b`-term sum. `sympy`'s automatic hypergeometric
   summation was tried (`/tmp` exploration, not in this directory, per §0's
   disclosure policy — the attempt itself is reported honestly here) and did
   not return an elementary closed form; a numerically-observed pattern (the
   strip's denominator appears to be `(r{+}1)(r{+}2)\cdots(r{+}\lceil b/2\rceil)`
   for the `p=1` case, checked for `b\le8`) is noted but **not promoted** — it
   is an unproved empirical observation, not a claim. This is fine: an explicit
   finite sum of `b` closed-form terms **is** a closed form in every sense that
   matters (`O(b)` exact rational operations, no limit, no truncation error),
   and matches exactly the shape of the referee's own Teorema 3′, which also
   leaves its strip term as an explicit sum.
3. **It does not re-derive Corollary A3 or Theorem A/M.** Those are taken as
   fixed, already-PROVED input, exactly per this archive's standing convention
   for this lineage (§0).
4. **No independent adversarial re-verification of this document has been
   performed.** Per the archive's standing discipline, a positive result
   requires a hostile-referee pass before integration into `THEOREM.md`. §7
   names what a referee should attack first.
5. **It does not change the status of anything already catalogued.** Teorema 3,
   Teorema 3′, and every PROVED calibration formula quoted here are reproduced
   exactly, not superseded or weakened.

---

## 7. What a hostile referee should attack first

- **§3.3, the `I5`/`I7` derivation.** This is the one genuinely new piece of
  combinatorics. A referee should re-derive the Abel-summation-by-parts step
  independently (starting from `S_5(N,m)=\sum(N{-}2i)^4[A(i){-}A(i{-}1)]`) and
  check, by hand or symbolically, that the even-degree-in-`w` terms really do
  cancel — this is the crux of why `I5,I7` collapse onto `S_1,S_3,\dots` at
  `(N{-}1,m{-}1)` rather than needing a new family of "partial unweighted
  binomial sum" terms (which have no closed form).
- **§3.4, the general-`k` collapse proof.** Short and elementary (one line of
  factorial cancellation), easy to re-check independently; if it is right, it
  is right for every `k`, so the referee should look hardest at the edge case
  `r<k` (where both sides are asserted to vanish "by convention") rather than
  the generic case.
- **Whether the `I5,I7` cancellation pattern (§6 item 1) actually generalises
  to `I9,I11,\dots`.** This is the one open item with genuine mathematical
  content left unresolved — if a referee (or a future front) proves it in
  general, §2's route closes for **every** `p`, not just `p\le4`.

---

## 8. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `Q_p(u)=e_p(1,\dots,u)` vanishes for `u<p`, degree `2p` | **PROVED** (classical + exact interpolation, `p=0..4`, `15` out-of-sample checks each) |
| 2 | The `p`-uniform substitution `u=-(v+\beta/2)` | **PROVED** (direct algebra from `N=2r+b+1`) |
| 3 | Even/odd split + reflection collapse (Step 3) | **PROVED**, general `p` (elementary symmetry argument, `E_p` even reflects, `O_p` odd anti-reflects) |
| 4 | `I1,I3` | **PROVED** (referee, wave 10; re-derived independently here as a sanity check) |
| 5 | `I5,I7` (NEW) | **PROVED** for these two specific instances (Abel summation by parts, §3.3), exhaustively verified (`N\le39`/`34`, all `m`, `0` failures) |
| 6 | General-`k` collapse `P_b[N]_k(r{-}k{+}1)\binom{N-k}{r-k+1}=[r]_k` | **PROVED**, every `k` (one-line factorial cancellation, §3.4), verified numerically `k\le6` and symbolically `k\le3` |
| 7 | Central moments `\mu_2,\mu_4,\mu_6,\mu_8` of `\mathrm{Bin}(N,\tfrac12)` | **PROVED** (cumulant generating function, classical), verified `N\le20` |
| 8 | `D^{*(1)}_r(b)`, every `b\ge0` (Theorem D1) | **PROVED** — reduces to PROVED `b=0,1` formulas character-for-character; `3171` exact checks vs ground truth, `0` failures |
| 9 | `D^{*(2)}_r(b)`, every `b\ge0` | **PROVED** — independently re-derives Teorema 3′ (already PROVED); reduces to PROVED `b=0,1` formulas; `671` exact checks, `0` failures |
| 10 | `D^{*(3)}_r(b)`, `D^{*(4)}_r(b)`, every `b\ge0` | **PROVED** given claims 1–7 (mechanical composition); reduce to PROVED `b=1` formulas; `671`+`671` exact checks, `0` failures each |
| 11 | General-`p` closure (`I_{2k+1}` for arbitrary `k`) | **OPEN** — mechanism exhibited at `k=2,3` only, not proved in general (§6 item 1, §7) |

> **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-059.]** The hostile
> referee (`adversarial/REFEREE_REPORT.md` Part 1, Part 6) found this
> "OPEN, not proved in general" framing to be an **underclaim**: the
> even-`w`-term cancellation behind `I5,I7` is a one-line consequence of
> the binomial parity identity `(w-1)^n-(w+1)^n=-2\sum_{t\text{ odd}}
> \binom nt w^{n-t}`, holding for **every** even exponent `n`, verified
> symbolically to `n=40` and numerically (brute force) through `k=11`.
> The named obstruction is therefore **removable by a mechanical
> argument**, not an open mathematical question. The referee explicitly
> did **not** carry out the full `p\ge5` assembly (no `Q_5,Q_6,\ldots`,
> no `\mu_{10},\mu_{12},\ldots`, no assembled `D^{*(p\ge5)}_r(b)`), so
> `p\ge5` remains honestly **not proved** — only its single named
> obstacle is now known to be removable. See `THEOREM.md` "Estágio 14."

> **[Correção pós-adversarial, 2026-08-24 — DISC-DEC-064.]** Wave 15
> front (a) (`general_p_dstar_closure_attempt/ATTEMPT.md`) executed the
> full assembly for `p=1,\ldots,10`: `26,710` exact checks, `0`
> mismatches, reducing character-for-character to every PROVED
> `b\in\{0,1\}` formula and independently re-deriving the five `b\ge2`
> instances this document only numerically verified. Its hostile
> referee went further and proved, by induction (using only `(E2)` and
> the `S_{2k-1}` recursion cited above), that the general-`k` machine
> is correct for **every** `k`, not merely the values checked — closing
> the underlying mechanism analytically, not just numerically. `p>10`
> remains open, but only as an unexecuted computation, not a
> mathematical uncertainty. See `THEOREM.md` "Estágio 16."
| 12 | The strip sum reduces to a single closed-form (non-summed) expression for general `b` | **OPEN** — left as an explicit `b`-term sum by design; an unpromoted empirical pattern is noted but not claimed (§6 item 2) |
| 13 | Independent adversarial re-verification | **NOT PERFORMED** — required before integration (§7) |

> **[Correção pós-adversarial, 2026-08-23 — DISC-DEC-059.]** Performed.
> Verdict SOUND / ACCEPT, 165,888 independent exact checks, 0
> mismatches, no error found anywhere; see the row-11 correction above
> and `THEOREM.md` "Estágio 14." Integrated into `THEOREM.md`.

**Net honest verdict.** The mandate's route — a Teorema-3′-style prefactor
collapse — was carried through explicitly and closes for `p=1,2,3,4` at every
`b\ge0`, reducing character-for-character to every PROVED calibration formula
available (`b=0`: `p=1,2`; `b=1`: `p=1,2,3,4`), independently re-deriving the
already-PROVED Teorema 3′ along the way as a strong end-to-end check, and
producing genuinely new closed forms at `b\ge2` (§4.1–§4.3) whose non-polynomial
shape is the precise, now fully mechanised, explanation for why the earlier
polynomial-basis fit was structurally doomed. The one substantive item left open
is whether the same machine closes for **every** `p` at once (item 11) — the
evidence (`k=2,3` both work by the identical mechanism) is suggestive but not a
proof, and is named exactly, not glossed over.

---

## 9. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any real verification run here | — |
| `ground_truth.py` / `.log` | `D^{*(p)}_r(b)` via Corollary A3, own Stirling table; smoke test vs. every PROVED calibration formula | <0.1 s |
| `ingredients.py` / `.log` | §3: `Q_p(u)` (interpolation+extension), central moments, `I1,I3,I5,I7`, the general-`k` collapse family (numeric + symbolic) | ~1.5 s |
| `assemble.py` / `.log` | §4: the assembled `D^{*(p)}_r(b)` for `p=1,2,3,4`; hard-requirement calibration checks (`r=0..200`); the big exhaustive sweeps vs. ground truth; the `b=2,3` printed instances | ~7 s |
| `ATTEMPT.md` | this document | — |

Reproduce in this order: `python3 ground_truth.py`; `python3 ingredients.py`;
`python3 assemble.py`. All three run in well under a minute combined.
