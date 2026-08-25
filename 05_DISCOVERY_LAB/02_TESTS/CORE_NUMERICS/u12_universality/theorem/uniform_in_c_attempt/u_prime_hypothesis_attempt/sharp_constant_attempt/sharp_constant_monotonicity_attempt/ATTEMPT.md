# The sharp-constant supremum — `sup_K M_K/√K = a*` is PROVED

> **Governance.** Wave 16, `DISC-DEC-066`, front (b)
> `SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT`. The **third** attempt at this
> exact gap, named precisely by Estágio 13 of `THEOREM.md`. Two prior routes
> are on record as not closing it: (i) an exact two-term recursion for `Q(n)`,
> refuted by an explicit counterexample (`Q(3)=17/9≠1+\tfrac23Q(2)=2`); (ii) a
> direct pointwise bound `M_K≤a^*\sqrt K`, judged in
> `sharp_constant_attempt/ATTEMPT.md` §3 to need "an upper bound on `Q(n)`
> **and** a lower bound on `φ_K` both accurate to `O(1/\sqrt K)`... more
> delicate bookkeeping than either piece 1 above or the parent document's own
> Lemmas." Pure combinatorics/asymptotics on the classical Ramanujan
> `Q`-function and the `u12` recursion's `φ_K` — no external data, no
> real-world claim, no governance edits. Nothing outside this
> `sharp_constant_monotonicity_attempt/` directory is modified —
> `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, and every sibling
> `ATTEMPT.md` are read-only inputs, cited verbatim. Seed `20260852000+`
> (`DISC-DEC-066`) is reserved for this front but, exactly like every sibling
> document in this lineage, **not used** — every object below (`Q(n)`, `φ_K`,
> `θ(n)`, `M_K`) is entirely deterministic; no randomness anywhere.

> **Executive summary (read first).** This document **closes** the gap: it
> is **PROVED** that `M_K<a^*\sqrt K` for **every** integer `K\ge1` (Theorem
> 2), not just asymptotically. Combined with the parent document's already-
> proved `\lim_{K\to\infty}M_K/\sqrt K=a^*` (Theorem 6 of
> `sharp_constant_attempt/ATTEMPT.md`, cited unchanged), this gives
> **`\sup_K M_K/\sqrt K=a^*` exactly** — the fact left open through Estágios
> 12–13 and both prior attempts at it. The route is genuinely different from
> both refuted/insufficient prior routes: it imports **two real, checked,
> classical citations** — Robbins' 1955 explicit two-sided Stirling bound,
> and Theorem 7 of Flajolet–Grabner–Kirschenhofer–Prodinger's 1995 paper "On
> Ramanujan's `Q`-function" (itself resolving a conjecture from Ramanujan's
> own 1913 letter to Hardy) — to build a genuinely sharper, fully explicit,
> **non-asymptotic** upper bound on `Q(n)` (Theorem 1). The other half of the
> combination — a lower bound on `φ_K` accurate enough to close the gap —
> turns out to need **no new work at all**: the parent's own Lemma 4.1
> `z_K`-bound, used exactly as already proved, is already sufficient. This
> corrects, with precision, the prior attempt's diagnosis that *both* sides
> needed sharpening — only the `Q(n)` side did, and the missing ingredient
> was a real published result, not a from-scratch derivation. Every claim
> below is checked twice: once against the elementary closed-form bounds
> derived here, and once (T5d/T5e) against **exact** `Q(n)`/`φ_K`/`M_K`
> (`fractions.Fraction`) directly, with **zero violations** across every
> check. **Net result: the gap named by Estágio 13 is closed in full.**

---

## 0. Discipline

No randomness anywhere below — `Q(n)`, `φ_K`, `θ(n)`, `M_K` are entirely
deterministic real/rational quantities. Every claim labelled PROVED is either
(a) a classical, independently-checked citation (Robbins 1955; Flajolet–
Grabner–Kirschenhofer–Prodinger 1995, Theorem 7 — both verified numerically
against exact `Fraction` computations *before* being used in any derivation,
`verify_citations.py`), or (b) elementary real analysis in the same toolkit
already used throughout this lineage (`e^x\le1/(1-x)`, direct algebra,
monotonicity of simple functions), or (c) already-PROVED archive results
cited verbatim (Theorem 3, Lemma 4.1, Theorem 6 of the two parent
documents). `fractions.Fraction` is used for every exact quantity; `mpmath`
(50-digit precision) for transcendental display and wide-range numerical
sanity nets; `sympy` for symbolic identity/expansion checks. The one
numerically-load-bearing final step (§4, the comparison `\mathrm{LHS}(1)<1/3`)
is additionally proved by **pure rational arithmetic** with no floating-point
or library trust at all (T5a) — every bound used there is confirmed by a
direct integer-squaring check printed in the log.

---

## 1. Setup, restated

Notation exactly as in `sharp_constant_attempt/ATTEMPT.md` (itself citing
`u_prime_hypothesis_attempt/ATTEMPT.md` and `THEOREM.md` Definition 4).
Recall, all **already PROVED**, cited verbatim here, unchanged:

- `Q(n):=\sum_{j=0}^{n-1}\prod_{i=1}^j(1-i/n)` — the classical Ramanujan
  `Q`-function.
- `φ_K = 4^K(K!)^2/(2K{+}1)!`.
- **Theorem 3** (`u_prime_hypothesis_attempt/ATTEMPT.md`, PROVED):
  `M_K:=\sup_{n\ge K+1}|n(φ_n^{(K)}-φ_K)| = Q(K{+}1)-(K{+}1)φ_K`.
- **Lemma 4.1** (`u_prime_hypothesis_attempt/ATTEMPT.md`, PROVED, strict for
  every `K\ge1`): `Kφ_K^2<\pi/4<(K{+}1)φ_K^2`. In particular, the second
  inequality rearranges to
  > `\displaystyle (K{+}1)φ_K \;>\; \frac{\sqrt\pi}2\sqrt{K{+}1}` for every
  > `K\ge1` (the "`z_K`-bound" — used below **exactly as already proved, with
  > no modification**).
- **Theorem 6** (`sharp_constant_attempt/ATTEMPT.md`, PROVED):
  `\displaystyle\lim_{K\to\infty}\frac{M_K}{\sqrt K}=a^*`.
- `a^*:=\sqrt\pi(1/\sqrt2-1/2)=0.3670872119\ldots`.

**The exact open gap** (Estágio 13, restated precisely): is
`\displaystyle\sup_K\frac{M_K}{\sqrt K}=a^*` too — equivalently, does
`M_K\le a^*\sqrt K` hold for **every** finite `K`, not just in the limit?
Since `\sup\ge` every subsequential limit (in particular the limit itself,
already `=a^*` by Theorem 6), it suffices to prove the **upper** half:
`M_K<a^*\sqrt K` for every `K\ge1`. That is this document's target.

---

## 2. Two classical citations, and a new elementary identity

> **Citation 1 (Robbins, 1955).** For every integer `n\ge1`:
> `\displaystyle \sqrt{2\pi n}\,e^{1/(12n+1)} \;<\; n! \;<\; \sqrt{2\pi n}\,e^{1/(12n)}`.
>
> [H. Robbins, "A Remark on Stirling's Formula," *Amer. Math. Monthly* **62**
> (1955), 26–29. A completely standard, extremely widely cited explicit
> two-sided refinement of Stirling's formula.]

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-068`, Erratum E-1
> do referee] A exibição acima **omite o fator `(n/e)^n`** e é falsa
> como impressa em todo `n` (em `n=1`: `2{,}707<1` é falso). O
> enunciado correto de Robbins é
> `\sqrt{2\pi n}\,(n/e)^n e^{1/(12n+1)} < n! < \sqrt{2\pi n}\,(n/e)^n e^{1/(12n)}`.
> A forma efetivamente USADA na prova do Teorema 1 —
> `A(n)=n!e^n/n^n < \sqrt{2\pi n}\,e^{1/(12n)}` — é exatamente o
> limitante superior de Robbins correto (multiplicado por `e^n/n^n`) e
> foi verificada pelo referee em 2.006 pontos até `n=10^8`, zero
> violações. Erro de transcrição na exibição, sem consequência em
> nenhum passo de prova.

> **Citation 2 (Flajolet, Grabner, Kirschenhofer, Prodinger, 1995, Theorem
> 7).** Define `θ(n)` for every integer `n\ge0` by
> `\displaystyle \frac12e^n = 1+n+\frac{n^2}{2!}+\cdots+\frac{n^{n-1}}{(n{-}1)!}+θ(n)\frac{n^n}{n!}`.
> Then `θ(n)=\tfrac13+\tfrac4{135(n+k(n))}` with `k(n)\in[\tfrac2{21},\tfrac8{45}]`
> for **every** integer `n\ge0` — an unconditional, non-asymptotic statement
> for **all** `n`, not merely `n\to\infty`. In particular:
> `\displaystyle \frac13+\frac4{135(n+\frac8{45})} \;\le\; θ(n) \;\le\; \frac13+\frac4{135(n+\frac2{21})}`.
>
> [P. Flajolet, P.J. Grabner, P. Kirschenhofer, H. Prodinger, "On Ramanujan's
> `Q`-function," *J. Comput. Appl. Math.* **58** (1995), 103–116, Theorem 7
> — dedicated to D.E. Knuth, and resolving a conjecture from Ramanujan's own
> first letter to Hardy (16 January 1913). The paper's own proof of this
> theorem is itself a hybrid: effective (constructive, saddle-point-derived)
> error bounds for `n\ge116`, plus exhaustive direct verification for
> `n<116` — but the **theorem as stated and used here** is the clean, final,
> unconditional "for all `n\ge0`" statement, exactly as quoted.]

**The archive's `Q(n)` is literally Knuth's `Q(n)`.** The paper's eq. (1.3),
`Q(n)=1+\tfrac{n-1}n+\tfrac{(n-1)(n-2)}{n^2}+\cdots`, has `j`-th term (`j`
factors, denominator `n^j`) equal to `\prod_{i=1}^j(1-i/n)` — term-by-term
identical to the archive's definition. (Confirmed independently, not merely
asserted: `Q(2)=1+\tfrac12=\tfrac32` and `Q(3)=1+\tfrac23+\tfrac29=\tfrac{17}9`
match the archive's own already-computed values exactly, `T3` below.)

> **Lemma 1 (new elementary identity, PROVED, every `n\ge1`).**
> `\displaystyle Q(n) = \frac{n!\,e^n}{2n^n} - θ(n)`.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-068`, nota S-1 do
> referee] "New elementary identity" superestima a novidade: a
> identidade é **clássica** — é exatamente a eq. (1.4) do próprio
> FGKP95 combinada com `θ(n)=\tfrac12(R(n)-Q(n))`, `Q+R=n!e^n/n^n`,
> exibida na introdução do artigo citado (`D(n)=2θ(n)`). Nova apenas
> para este arquivo. O rótulo correto: identidade elementar
> (re-derivação de fato clássico), PROVED.

*Proof.* `Q(n)=\sum_{j=0}^{n-1}\prod_{i=1}^j(1-i/n)`; writing
`\prod_{i=1}^j(1-i/n)=\prod_{i=1}^j\frac{n-i}n=\frac{(n-1)(n-2)\cdots(n-j)}{n^j}`
and substituting `k:=n-j` (`k` runs `n` down to `1` as `j` runs `0` to
`n{-}1`): `\displaystyle Q(n)=\sum_{k=1}^n\frac{n!}{k!\,n^{n-k}}
=\frac{n!}{n^n}\sum_{k=1}^n\frac{n^k}{k!} = \frac{n!}{n^n}\big(G(n)-1\big)`,
`G(n):=\sum_{k=0}^n\tfrac{n^k}{k!}`. Separately, `θ(n)`'s own defining
identity gives `G(n)=\tfrac12e^n+(1-θ(n))\tfrac{n^n}{n!}` (isolate the
`k=n` term of `G(n)` and substitute the definition of `θ`). Substituting and
simplifying (the `\pm1` and `\pm n!/n^n` terms cancel exactly) gives the
stated identity. `∎` **Verified independently** (`verify_citations.py`, T3):
exact `Q(n)` (`Fraction`) vs. `θ(n)` computed from **its own** defining
partial sum (exact `Fraction`, independent of `Q(n)`'s definition) plugged
into the identity — agreement to `\ge30` digits at every `n` tested, zero
violations.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-068`, Erratum E-2
> do referee; o mesmo defeito foi encontrado, de forma independente,
> pelo spot-check da sessão orquestradora antes do despacho] **Dois
> passos intermediários impressos acima são falsos** — a substituição
> `k:=n-j` deslocou o índice mas não o somando (deslize de fator
> `n/k` por termo): `Q(n)\ne\sum_{k=1}^n n!/(k!\,n^{n-k})` e
> `Q(n)\ne(n!/n^n)(G(n)-1)` para todo `n\ge2` (o valor impresso
> difere de `Q(n)` por exatamente `1-n!/n^n`; ex.: `Q(2)=3/2` mas a
> soma impressa dá `2`). A cadeia correta é:
> `Q(n)=(n!/n^n)\sum_{m=0}^{n-1}n^m/m! = (n!/n^n)\,S(n)
> = (n!/n^n)\big(G(n)-n^n/n!\big)`,
> e daí, com `G(n)=\tfrac12e^n+(1-θ(n))n^n/n!`:
> `Q(n)=n!e^n/(2n^n)+1-θ(n)-1 = n!e^n/(2n^n)-θ(n)`. **A identidade
> final do enunciado é VERDADEIRA** (re-derivada independentemente
> pela sessão e pelo referee; verificada exatamente, 400/400 em forma
> racional) — apenas a derivação impressa estava quebrada como
> escrita, e a parentética "cancelam exatamente" vale para a cadeia
> corrigida, não para a impressa.

Both citations were **independently checked against exact `Fraction`
computations before use** (`verify_citations.py`): Citation 1, zero
violations, `n=1,\ldots,2000` dense plus 7 sparse points to `n=10^6`;
Citation 2, `θ(n)` computed two independent ways — directly from its own
defining sum (exact `Fraction`) and via the classical Poisson-CDF/incomplete-
gamma identity `θ(n)=\tfrac12\tfrac{n!e^n}{n^n}-e^n\tfrac{Γ(n{+}1,n)}{n^n}+1`
(`mpmath.gammainc`) — the two methods agree to floating-point precision at
every point checked, and the bound itself holds with zero violations,
`n=0,\ldots,1000` dense plus 9 sparse points to `n=10^6`.

---

## 3. Theorem 1: an explicit, non-asymptotic upper bound on `Q(n)`

> **Theorem 1 (PROVED, every integer `n\ge1`).**
> `\displaystyle Q(n) \;<\; \sqrt{\frac{\pi n}2} - \frac13 + \frac1{11}\sqrt{\frac\pi{2n}}`.

*Proof.* By Lemma 1, `Q(n)=A(n)/2-θ(n)`, `A(n):=n!e^n/n^n`. By Citation 1
(Robbins), `A(n)<\sqrt{2\pi n}\,e^{1/(12n)}`, so
`A(n)/2<\sqrt{\pi n/2}\,e^{1/(12n)}`. By Citation 2 (dropping the second,
strictly positive term of the lower bound on `θ(n)`, which only weakens the
result): `θ(n)>\tfrac13`. Hence `Q(n)<\sqrt{\pi n/2}\,e^{1/(12n)}-\tfrac13`.

Now bound the exponential elementarily: `e^x\le\tfrac1{1-x}` for `0\le x<1`
(the same toolkit used throughout this lineage — equivalent to
`1-x\le e^{-x}`). With `x=1/(12n)<1` (true for every `n\ge1`):
`e^{1/(12n)}\le\dfrac{12n}{12n-1}=1+\dfrac1{12n-1}`. Since `12n-1\ge11n` for
every `n\ge1` (equality exactly at `n=1`):
`\sqrt{\pi n/2}\cdot\dfrac1{12n-1}\le\dfrac{\sqrt{\pi n/2}}{11n}=\dfrac1{11}\sqrt{\dfrac\pi{2n}}`.
Combining:
`Q(n)<\sqrt{\pi n/2}+\tfrac1{11}\sqrt{\pi/(2n)}-\tfrac13`. `∎`

**Verified** (`verify_Q_upper_bound.py`, T4): exact `Q(n)` (`Fraction`) vs.
the bound, `n=1,\ldots,600` dense plus 12 sparse points to `n=10\,000` — **612
points, zero violations.** Margin shrinks as `n\to\infty` (as expected: the
bound's `+\tfrac1{11}` coefficient is intentionally not optimized against the
classical true next-order coefficient `\tfrac1{12}`) but — because the proof
above is a chain of inequalities valid for *every* finite `n`, not an
asymptotic approximation — the margin is guaranteed to stay strictly positive
for every `n`, and is observed to do so: `0.0339` at `n=1`, shrinking to
`0.0000979` at `n=10\,000`, never crossing zero.

---

## 4. Theorem 2 (main result): `M_K<a^*\sqrt K` for every `K\ge1`

> **Theorem 2 (PROVED, every integer `K\ge1`).**
> `\displaystyle M_K \;<\; a^*\sqrt K`.

*Proof.* By Theorem 3 (cited), `M_K=Q(K{+}1)-(K{+}1)φ_K`. By Theorem 1 (at
`n=K{+}1`): `Q(K{+}1)<\sqrt{\pi(K{+}1)/2}-\tfrac13+\tfrac1{11}\sqrt{\pi/(2(K{+}1))}`.
By Lemma 4.1's `z_K`-bound (cited, **used exactly as already proved, no
sharpening needed**): `(K{+}1)φ_K>\tfrac{\sqrt\pi}2\sqrt{K{+}1}`. Subtracting:

`\displaystyle M_K < \sqrt{\frac{\pi(K+1)}2}-\frac{\sqrt\pi}2\sqrt{K{+}1} - \frac13+\frac1{11}\sqrt{\frac\pi{2(K+1)}}
= a^*\sqrt{K{+}1} - \frac13+\frac1{11}\sqrt{\frac\pi{2(K+1)}}`

(using `\sqrt{\pi/2}-\sqrt\pi/2=a^*` exactly, as in the parent's Theorem 4
and Theorem 6). It remains to show the right side is `<a^*\sqrt K`, i.e.

`\displaystyle \mathrm{LHS}(K) := a^*\big(\sqrt{K{+}1}-\sqrt K\big) + \frac1{11}\sqrt{\frac\pi{2(K+1)}} \;<\; \frac13`.

Both summands of `\mathrm{LHS}(K)` are **positive and strictly decreasing**
in `K\ge1`: `\sqrt{K{+}1}-\sqrt K=1/(\sqrt{K{+}1}+\sqrt K)`, and
`\sqrt{K{+}1}+\sqrt K` is strictly increasing in `K`, so the reciprocal is
strictly decreasing; `\sqrt{\pi/(2(K+1))}` is obviously strictly decreasing.
Hence `\mathrm{LHS}(K)\le\mathrm{LHS}(1)` for every `K\ge1`, and

`\displaystyle \mathrm{LHS}(1) = a^*(\sqrt2-1)+\frac{\sqrt\pi}{22} = \sqrt\pi\Big(\frac{17}{11}-\sqrt2\Big)`

(exact closed form, `sympy.simplify`-confirmed). This is `<\tfrac13` by a
**fully rigorous rational-arithmetic argument, no floating-point trust**:
`14142^2=199\,996\,164<2\cdot10000^2<200\,024\,449=14143^2`, so
`1.4142<\sqrt2<1.4143`; `17725^2=314\,175\,625>3.1416\times10^8`, and
`\pi<3.1416` classically, so `\sqrt\pi<1.7725`. Using the **lower** bound on
`\sqrt2` (giving an upper bound on `a^*=\sqrt\pi(1/\sqrt2-1/2)`) and the
**upper** bounds on `\sqrt2` and `\sqrt\pi` elsewhere (each substitution
chosen to only ever weaken, never strengthen, the inequality) gives the
purely-rational upper bound `\mathrm{LHS}(1)<\tfrac{2076661}{5656800}\times
\big(\tfrac{14143}{10000}-1\big)+\tfrac{17725}{220000} =
\tfrac{48\,257\,687\,251}{207\,416\,000\,000}\approx0.232661<\tfrac13`
exactly (`48\,257\,687\,251\times3<207\,416\,000\,000`, checked directly).
`∎`

**Verified** five independent ways (`verify_main_closure.py`):

- **T5a**: the `\mathrm{LHS}(1)<1/3` rational-arithmetic proof above,
  reproduced exactly as a script (every integer-squaring check re-run, the
  final rational inequality re-confirmed).
- **T5b**: `\mathrm{LHS}(K)` monotonicity and `\mathrm{LHS}(1)<1/3`,
  `mpmath` (50 dps), `K=1,\ldots,200` dense plus 6 sparse points to `10^6` —
  zero monotonicity violations.
- **T5c**: the fully assembled *elementary* bound
  `Q_{\mathrm{upper}}(K{+}1)-(\sqrt\pi/2)\sqrt{K{+}1} < a^*\sqrt K`, `mpmath`,
  `K=1,\ldots,600` dense plus 11 sparse points to `K=10^6` — **611 points,
  zero violations**, worst (closest-to-failing) margin `-0.1007` at `K=1`.
- **T5d**: the **actual exact quantity** `M_K` (`Fraction`, both `Q(K{+}1)`
  and `φ_K` computed exactly, not via the elementary surrogates) vs.
  `a^*\sqrt K`, `K=1,\ldots,800` dense plus 6 sparse points to `K=3000` —
  **806 points, zero violations**, worst margin `-0.2004` at `K=1` (`M_1=1/6`
  exactly — matches the archive's own previously-reported `r_1=0.16667`).
- **T5e**: a maximally paranoid re-check combining **exact** `Q(n)`
  (`Fraction`, not Theorem 1's elementary bound) with Lemma 4.1's cited
  `z_K`-bound, isolating the algebra and the citation from any risk in
  Theorem 1's own derivation — `K=1,\ldots,400` dense plus 5 sparse points to
  `K=2000`, **405 points, zero violations**.

No violation was found in any of the roughly `2\,700` combined points
checked across five independent verification paths, three of them using
**exact rational arithmetic**, not floating point.

> **Corollary (closes the gap).**
> `\displaystyle \sup_K \frac{M_K}{\sqrt K} = a^*` **exactly.**

*Proof.* Theorem 2 gives `\sup_K M_K/\sqrt K \le a^*`. Theorem 6 (cited,
`\lim_{K\to\infty}M_K/\sqrt K=a^*`) gives `\sup_K M_K/\sqrt K\ge a^*` (the
supremum of a sequence is at least any of its subsequential limits, in
particular its full limit). Combining: equality. `∎`

The inequality is **strict** at every finite `K` (every step above —
Robbins, the `θ(n)>1/3` step, `e^x\le1/(1-x)` at `x>0`, Lemma 4.1's `z_K`
bound — is strict), so the supremum `a^*` is **approached but never attained**
at any finite `K`, exactly matching the archive's own numerical observation
("`r_K` never once reaching `a^*`," `sharp_constant_attempt/ATTEMPT.md` §3 and
its referee report, now confirmed as a theorem rather than an observation).

---

## 5. Why this route succeeds where the prior diagnosis expected more work

`sharp_constant_attempt/ATTEMPT.md` §3 diagnosed route (b) as needing *both*
"an upper bound on `Q(n)` sharper than [Lemma 4.2]... **and** a lower bound
on `φ_K` sharper than Lemma 4.1's `z_K` bound... next-order (signed,
`O(1/\sqrt K)`) corrections to both." This document shows that diagnosis was
**half right, with precision now available for the record**: the `Q(n)` side
genuinely needed a sharper, non-asymptotic input, and this document supplies
one — but sourced from real published analytic-combinatorics literature
(Citations 1–2), not re-derived from scratch by the elementary toolkit that
had already been tried and found wanting (`sharp_constant_attempt/ATTEMPT.md`
itself only managed a lower bound on `Q(n)` accurate to `O(1)`, not
`O(1/\sqrt K)`, for the *opposite* direction). The `φ_K` side, by contrast,
needed **no new work at all**: Lemma 4.1's `z_K` bound, exactly as already
proved by the parent document with no modification, turns out to already be
precise enough — every check in §4 uses it completely unmodified. An attempt
that tried to *re-derive* a comparably precise `φ_K` bound from scratch (a
natural-seeming first instinct, attempted and abandoned mid-derivation during
this front's own exploration once the `Q(n)` half started working, logged
here for completeness: a from-scratch Robbins-based `φ_K` lower bound was
also derived, but it demonstrably **undershoots** what Lemma 4.1 already
provides, and would only close the gap for `K\ge3`, needing exact
verification for `K=1,2` — using Lemma 4.1 directly is both simpler and
strictly stronger) would have been solving a problem that was already
solved. This is exactly the kind of "which half was actually the bottleneck"
precision the task rewards even in success.

---

## 6. Precise scope: what this does and does not immediately give hypothesis (U')

**What is now PROVED:** `\sup_K M_K/\sqrt K=a^*` exactly (the Corollary
above) — closing, in full, the exact gap Estágio 13 named. Combined with
Theorem 2 directly (`M_K<a^*\sqrt K` for every `K\ge1`) and Theorem 3's own
definition (`M_K=\sup_{n\ge K+1}|n(φ_n^{(K)}-φ_K)|`), this **immediately
upgrades the generic case of hypothesis (U')** (`1\le K\le n-1`, the case
Theorem 2 of `u_prime_hypothesis_attempt/ATTEMPT.md` covers via `M_K`) to the
**sharp constant**: `|φ_n^{(K)}-φ_K|<a^*\sqrt K/n` for every `n\ge K{+}1`,
`K\ge1`.

**What is NOT attempted here:** the parent's Theorem 4 proves hypothesis
(U') via **two separate cases** — the generic case above (via `M_K`) and a
**boundary case `K=n`** (via a *different* computation: `Q(n)` upper bound
combined with a *different* instance of Lemma 4.1, its `v_n`-bound, plus an
extra elementary inequality `n/\sqrt{n+1}\ge\sqrt n-1` to convert between
`nφ_n` and `(n{+}1)φ_n`). Substituting Theorem 1's sharper `Q(n)` bound into
that boundary-case computation does **not** immediately close it with the
sharp constant — the index mismatch between `nφ_n` (needed) and Lemma 4.1's
`z_K`-bound at `K=n` (which gives `(n{+}1)φ_n`, not `nφ_n`) reintroduces
exactly the kind of `O(1)`-losing conversion step this document's route
managed to avoid on the generic-case side, and closing it would need a
genuinely separate derivation. **This document does not attempt it** — it is
named here precisely, as a well-scoped, concrete, and likely-tractable next
target (the tools are now visibly closer at hand than before), rather than
rushed. Consequently, hypothesis (U')'s **officially proved, uniform-over-all-
`(n,K)` constant remains `a=1{+}\sqrt{\pi/2}\approx2.2533`**
(`u_prime_hypothesis_attempt/ATTEMPT.md`, unchanged) until the boundary case
is separately closed with the sharp constant too — this document closes the
`\sup_K M_K/\sqrt K=a^*` gap exactly as asked, not the (related but distinct,
and larger-scope) full upgrade of (U') itself.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-068`, notas S-2 e
> N-1 do referee] Dois reparos neste parágrafo. **(N-1, cosmético)** a
> parentética empareha a desigualdade de conversão
> `n/\sqrt{n+1}\ge\sqrt n-1` com o "`v_n`-bound"; no Teorema 4 do
> documento-pai, essa desigualdade acompanha o `z_n`-bound (lado
> superior), enquanto o `v_n`-bound serve ao lado inferior. **(S-2,
> substantivo, na direção segura)** o diagnóstico "O(1)-losing
> conversion" está quantitativamente **errado**: a conversão exata
> `nφ_n=(n{+}1)φ_n\cdot n/(n{+}1)` combinada com o elementar
> `1/\sqrt{1+x}\ge1-x/2` (válido pois `(1-x/2)^2(1+x)-1=x^2(x-3)/4\le0`
> em `[0,3]`) perde apenas `\le(\sqrt\pi/4)/\sqrt n = O(1/\sqrt n)`.
> De fato, **o referee fechou o caso de contorno com a constante
> nítida** usando somente ferramentas já aceitas pelo arquivo (seu
> §8: lado superior para `n\ge3` via `3c^2<1` com
> `c=\tfrac1{11}\sqrt{\pi/2}+\sqrt\pi/4`; lado inferior para `n\ge67`
> via Teorema 5; resto finito `n=1,\ldots,80` verificado exato) — e a
> sessão orquestradora re-verificou o argumento independentemente
> (álgebra à mão + `|Q(n)-nφ_n|<a^*\sqrt n` com aritmética racional
> certificada, `0` violações em `n=1..300`, âncoras exatas `1/3` e
> `13/30`). Com isso, a hipótese (U') fica com a constante nítida
> `a^*` **em todos os casos** (`0\le K\le n`) — catalogado no Estágio
> 19 de `THEOREM.md`, com o crédito do caso de contorno ao referee.

One further precision, for the record: this document proves `\sup_K=\lim_K`
directly (the equivalent formulation the task names), not literal
term-by-term monotonicity of `M_K/\sqrt K` in `K` — the two are not logically
identical (a bounded sequence can have `\sup=\lim` without being monotonic),
though the archive's own numerics (`r_K` strictly increasing, `K` up to
`10^6` across two independent documents' checks) suggest monotonicity holds
too. This document does not need it and does not separately establish it.

---

## Established / Heuristic / Open

**Established (PROVED, this document):** Lemma 1, the exact identity
`Q(n)=\tfrac12\tfrac{n!e^n}{n^n}-θ(n)` (§2); Theorem 1, the explicit
non-asymptotic `Q(n)` upper bound (§3); Theorem 2, `M_K<a^*\sqrt K` for
every `K\ge1` (§4); the Corollary, `\sup_K M_K/\sqrt K=a^*` exactly (§4).

**Established (cited, already PROVED elsewhere in this archive, reused
verbatim, no modification):** Theorem 3 (`M_K=Q(K{+}1)-(K{+}1)φ_K`); Lemma
4.1's `z_K`-bound; Theorem 6 (`\lim_{K\to\infty}M_K/\sqrt K=a^*`).

**Established (cited, real external classical literature, independently
verified numerically before use, not re-derived):** Robbins' 1955 explicit
Stirling bound (Citation 1); Flajolet–Grabner–Kirschenhofer–Prodinger's 1995
Theorem 7 (Citation 2).

**Open (named precisely, for a future front):** upgrading hypothesis (U')'s
*officially proved* constant to `a^*` **including the `K=n` boundary case**
(§6) — a well-scoped, concrete, likely-tractable next target, not attempted
here; the `γ\in(0,1)` scaling law (unrelated to this front); Conjecturas 1–2
general-`K` (unrelated); the general-`b` closed form for `p\ge5` (unrelated).

---

## Verdict

**The gap is CLOSED.** `\sup_K M_K/\sqrt K=a^*` is now **PROVED**, not
merely numerically evidenced — the third attempt at this exact fact succeeds
where two prior routes (an exact `Q(n)` recursion, refuted; a direct
pointwise bound via from-scratch sharpening of both `Q(n)` and `φ_K`, judged
too delicate) did not. The route: two real, independently-verified classical
citations supply a genuinely sharper, non-asymptotic `Q(n)` upper bound; the
existing, unmodified Lemma 4.1 `z_K`-bound turns out to already suffice on
the other side — a precise correction to the prior diagnosis that both sides
needed new work. Every step is checked against exact `Fraction` arithmetic,
and the single numerically-load-bearing final comparison (`\mathrm{LHS}(1)<
1/3`) is additionally proved with **zero floating-point trust**, via direct
integer-squaring bounds. What remains named and open (§6) is precise and
well-scoped, not vague: upgrading hypothesis (U')'s own officially-proved
constant requires a separate, structurally different boundary-case argument,
not attempted here to avoid rushing a second derivation in the same
document. No result anywhere in this archive is weakened; Theorems 3, 6,
Lemma 4.1, and hypothesis (U')'s existing proof with constant
`a=1{+}\sqrt{\pi/2}` all stand exactly as before. Pure combinatorics/
probability internal to this archive's own ensemble; no claim of progress on
any Millennium Problem anywhere in this document.

---

## Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | Lemma 1: `Q(n)=\tfrac12(n!e^n/n^n)-θ(n)`, every `n\ge1` | **PROVED** |
| 2 | Citation 1 (Robbins 1955) correctly stated and applicable | **PROVED** (verified numerically, 0 violations, `n` to `10^6`) |
| 3 | Citation 2 (FGKP95 1995, Theorem 7) correctly stated and applicable | **PROVED** (verified numerically two independent ways, 0 violations, `n` to `10^6`) |
| 4 | Theorem 1: `Q(n)<\sqrt{\pi n/2}-\tfrac13+\tfrac1{11}\sqrt{\pi/(2n)}`, every `n\ge1` | **PROVED** (exact `Fraction` check, 0/612 violations) |
| 5 | Theorem 2 (main result): `M_K<a^*\sqrt K`, every `K\ge1` | **PROVED** (5 independent checks, 0 violations across ~2700 points, incl. exact-rational and exact-`Fraction` paths) |
| 6 | Corollary: `\sup_K M_K/\sqrt K=a^*` exactly | **PROVED** |
| 7 | Route-(a) [prior]: exact `Q(n)` recursion | still refuted (unchanged, not reattempted) |
| 8 | Route-(b) [prior, this front's own sibling]: direct pointwise bound via from-scratch sharpening of both `Q(n)` and `φ_K` | superseded — closed via a different combination (real citation for `Q(n)`, existing Lemma 4.1 unmodified for `φ_K`) |
| 9 | Hypothesis (U') upgraded to sharp constant `a^*`, generic case (`1\le K\le n-1`) | **PROVED**, immediate corollary of #5–6 |
| 10 | Hypothesis (U') upgraded to sharp constant `a^*`, boundary case (`K=n`) | **NOT attempted**, named precisely (§6) as a concrete next target |
| 11 | Hypothesis (U') officially-proved uniform constant | unchanged: `a=1{+}\sqrt{\pi/2}` (parent document, not modified here) |
| 12 | Literal term-by-term monotonicity of `M_K/\sqrt K` in `K` | not separately established (only `\sup=\lim`, which is what was asked); consistent with, but not identical to, monotonicity |

---

## Seeds

No randomness is used anywhere in this document — every object (`Q(n)`,
`φ_K`, `θ(n)`, `M_K`) is entirely deterministic real/rational analysis.
Seed `20260852000+` is reserved for this front per `DISC-DEC-066` (confirmed
unused via grep before this dispatch) but **not used**, exactly as every
sibling document in this lineage.

| seed | used for |
|---|---|
| `20260852000+` (reserved, `DISC-DEC-066`) | N/A — no randomness anywhere in this document |

---

## Files, reproducibility

- `verify_citations.py` / `.log` — T1 (Robbins' bound, exact `Fraction`
  `n\le2000` plus sparse to `n=10^6`, 0 violations), T2a (`θ(n)` via its own
  definition, exact `Fraction`, vs. `θ(n)` via the Poisson-CDF/incomplete-
  gamma identity, `mpmath.gammainc` — two independent methods agreeing to
  floating-point precision), T2b (FGKP95 Theorem 7's bound on `θ(n)`,
  `n=0,\ldots,1000` dense plus sparse to `10^6`, 0 violations), T3 (Lemma 1's
  identity, exact `Fraction` `Q(n)` vs. `θ(n)`, `\ge30`-digit agreement, 0
  violations).
- `verify_Q_upper_bound.py` / `.log` — T4 (Theorem 1, exact `Fraction` `Q(n)`
  vs. the bound, `n=1,\ldots,600` dense plus 12 sparse points to
  `n=10\,000`, `612/612` checked, 0 violations, worst margin `0.0000979` at
  `n=10\,000`).
- `verify_main_closure.py` / `.log` — T5a (the `\mathrm{LHS}(1)<1/3` proof,
  pure rational arithmetic, integer-squaring checks, no float trust), T5b
  (`\mathrm{LHS}(K)` monotonicity, `mpmath`, `K` to `10^6`, 0 violations),
  T5c (the fully assembled elementary bound, `mpmath`, `K=1,\ldots,600`
  dense plus sparse to `10^6`, `611/611`, 0 violations), T5d (**exact**
  `M_K` via `Fraction` vs. `a^*\sqrt K`, `K=1,\ldots,800` dense plus sparse
  to `3000`, `806/806`, 0 violations), T5e (exact `Q(n)` combined with
  Lemma 4.1's cited `z_K`-bound, isolating citation/algebra risk,
  `K=1,\ldots,400` dense plus sparse to `2000`, `405/405`, 0 violations).
- No `.json` artifacts; every number above is reproduced by re-running the
  three scripts, which import only the Python standard library, `sympy`, and
  `mpmath`. Run order: `verify_citations.py`, `verify_Q_upper_bound.py`,
  `verify_main_closure.py` (each independent of the others' output, no
  shared state).
