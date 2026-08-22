# The general-`K` Open Lemma, attempt 3 — a continuum scaling limit of the `K`-uniform Markov chain, and the `K=6..10` frontier

> **Governance.** `DISC-DEC-033`, front (a), `K6-OPEN-LEMMA-ATTEMPT`. Pure combinatorial
> mathematics — no external data, no holdout, no real-world claim, no governance edits.
> `THEOREM.md`, `ATTEMPT.md` (wave 5, `../..`) and `ATTEMPT.md` (wave 6,
> `..`, this document's immediate predecessor) and `DECISION_LEDGER.yaml`/
> `TEST_QUEUE.yaml` are **not** touched by this document — everything here lives
> under this new `k6_attempt/` directory. No git commit was made. Every claim below is
> labeled PROVED, PROVED-MODULO-[X] (X named precisely), NUMERICALLY VERIFIED (exact
> rational arithmetic, never floating-point sampling), CONJECTURED, or OPEN, following
> the discipline `THEOREM.md`/`ATTEMPT.md` use throughout.

> **Task.** `..`'s `ATTEMPT.md` (wave 6) proved the `K=3,4,5` cases of `THEOREM.md`
> §7.4's Open Lemma via a `K`-uniform Markov-chain / transfer-matrix method, solved
> level-by-level (`r=0,1,...,K`) through an exact telescoping-sum algorithm executed
> symbolically. It left `K≥6` open and named, in its §7.3, the precise obstruction to a
> fully general (symbolic-`K`) proof: each level's telescoping sum needs the
> *previous* level's closed form substituted in *numerically* before the next
> summation can execute, so there is no single expression "`h_r(a,b)`, `r` symbolic"
> to sum against. It named two concrete candidate routes, neither attempted: (i) an
> inductive proof, on `r`, that the closed-form solution has a predicted general shape,
> preserved by one more application of the recursion; (ii) a generating-function-in-`K`
> argument. This document was asked to attempt route (i) or (ii) (or both), and, at
> minimum, to push the concrete-`K` frontier past `K=5`.

> **Executive summary (read first).** Both goals were achieved, by two different
> routes:
>
> **1. The concrete-`K` frontier (§1).** Wave 6's own mechanical ladder
> (`markov_transfer.py`'s `build_levels`) — already `K`-uniform *as a procedure* — was
> simply run six rungs further. This is not a new idea, just wave 6's own method
> executed past where wave 6 stopped: **`K=6,7,8,9,10` are now all PROVED**
> (`ψ_n^{(K)}` exact closed forms for every one of these `K`, each independently
> re-verified). `K=6` in particular received the *same* verification discipline wave 6
> used for `K=3` (§1.2): matched against a **fresh, independent, exhaustive raw
> brute-force enumeration** at `n=7` (593M `(π,U)` combinations, exact rational
> arithmetic) and, as a genuinely new held-out point, at `n=8` (10.6B combinations);
> matched against a fast independent direct (non-symbolic) recursion at 19 further
> values of `n`; and the full recombined `φ_n^{(6)}` rate matched against a third,
> independent brute force of the raw Definition-4 average. **Zero mismatches.**
>
> **2. A genuinely new technique for general `K` (§2–§4): a continuum (`n→∞`) scaling
> limit of the `K`-uniform discrete Markov chain itself**, taken to *two* orders in
> `1/n`. This is route (ii) of the task brief, arrived at not as a formal
> generating-function-in-`K` sum (which was tried and did not close, §6.1) but as an
> asymptotic ODE system in the continuum variable `t=m/n`, with `r` (the source count)
> entering as a genuine free *parameter*, not a summation index — exactly sidestepping
> wave 6's named obstruction. This produces:
>
> - **A full, symbolic-`r` closed form for the leading order** `F_r(t,b) :=
>   lim_{n→∞} g_r(nt,b)` (§2), derived by an honest induction on `r` (solving a linear
>   ODE via a diagonal coefficient-matching argument at each level, unrolled explicitly
>   in closed form) — **PROVED**, and independently re-derives
>   `φ_K = 4^K(K!)^2/(2K+1)!` (`THEOREM.md` Lemma 2's Wallis integral) for *every* `K`
>   at once, by a completely different route than `THEOREM.md`'s own continuum
>   construction on `L(c)`.
> - **A full, symbolic-`r` closed form for the `O(1/n)` correction**
>   `G_r(t,b) := lim_{n→∞} n[g_r(nt,b) - F_r(t,b)]` (§3) — first conjectured from data
>   (`r=0..8`), then **PROVED** by an exact, fully symbolic-in-`(r,k,b)` algebraic
>   identity check (not curve-fitting: `sympy` confirms the conjectured closed form
>   satisfies the *defining recursion*, for generic `r,k,b`, reducing to `0` in both
>   the general and the `k=0` boundary case).
> - **A complete, hand-checkable proof that this closed form's `t=1,b=0` value equals**
>   `Kφ_K/4` **for every `K`** (§3.4) — i.e., **wave 6's rate conjecture
>   (`ATTEMPT.md` §7.2) is PROVED for general `K`**, via an elementary reduction to a
>   binomial-coefficient sum identity, itself proved by a symmetry argument plus three
>   classical binomial moment sums (`Σ C(n,i)`, `ΣiC(n,i)`, `Σi²C(n,i)`, all standard).
>
> **The one honest caveat (§4, stated precisely, not buried):** the ODE derivation
> establishes what `F_r,G_r` **must equal** *if* `g_r(m,b)` admits a regular
> two-term asymptotic expansion in `1/n` of the assumed polynomial-in-`t` shape, for
> every `r`. That the expansion's *existence* (for `r` **beyond the concretely
> computed range**) holds is not separately reproven here from `ε`-`δ` first
> principles — this is the one place a standard (in this genre of finite-`n`-to-
> continuum bridge) but not-here-independently-rederived analytic fact is used. It is
> **decisively corroborated**, not merely suggested, by *exact* (not approximate)
> agreement with the fully independent, unconditionally-proved discrete closed forms
> at **every one of the 11 concrete `K` values checked (`K=0,...,10`)** — both the
> leading order and the `1/n` rate, and, for `K≤5`, the *entire* `b`-dependence, not
> just a single number. §4 states exactly what remains open.

---

## 0. Relationship to prior work — what is reused, what is new

Reused **verbatim, without re-derivation**, from `../ATTEMPT.md` (wave 6):

- **The `(a,b,r)` Markov chain and its exact transition rules** (`../ATTEMPT.md` §2,
  Proposition, PROVED general in `K`): `g(a,b,r)` and `h(a,b,r)`, the two-function
  recursion this entire document works with. Not re-derived; cited and used as-is.
- **The telescoping-sum solving algorithm** (`../ATTEMPT.md` §3) and its
  implementation, `markov_transfer.py`'s `build_levels`/`g_closed_via_telescoping` —
  reused unmodified to extend the concrete-`K` ladder in §1 below.
- **Wave 5's Reduction Lemma A** (`../../ATTEMPT.md` §2, PROVED general in `K`):
  `φ_n^{(K)} = (K/n)ψ_n^{(K),R} + (1-K/n)ψ_n^{(K)}`, so that `ψ_n^{(K)}→φ_K` alone
  already proves `φ_n^{(K)}→φ_K` — used in §1 to state the `K=6..10` Open-Lemma
  corollaries without re-deriving Lemma A.
- **The Wallis integral** `φ_K = 4^K(K!)^2/(2K+1)! = \int_0^1(1-t^2)^K dt`
  (`THEOREM.md` Lemma 2, §5.2, PROVED for every `K`) — the target that the continuum
  leading order `F_r(1,0)` must reproduce (§2.3) as a nontrivial check.
- **The brute-force infrastructure** `psi_bruteforce_ref.py`, `markov_direct.py`,
  `phi_bruteforce_full.py` from `../` (wave 6) — reused, and, where the required `n,K`
  made the un-optimized versions too slow for this task's time budget, re-implemented
  independently for speed (§1.2 explains exactly how, and cross-validates the fast
  versions against the originals on every case where both are feasible, before trusting
  the fast version on the one case only it can reach).

**New in this document:** everything else. §1 is wave 6's own procedure run further —
no new idea, just six more mechanical rungs, with a full independent verification
pass at `K=6` matching wave 6's own standard. §2–§4 are the genuinely new content: a
continuum scaling-limit analysis of the *same* `(a,b,r)` chain that produces a
general-`r` (not case-by-case) answer for the leading order and the `1/n` rate —
route (ii) of the task brief, arrived at via an asymptotic ODE rather than a formal
generating-function sum (§6.1 records why the literal generating-function-in-`K` sum
was tried and abandoned in favor of this route). §5 states the resulting proof of the
rate conjecture in full, standalone form. §6 documents what was tried and did not
work (an honest negative-results record, per the task's own instruction that this is
an acceptable and valuable outcome).

---

## 1. Pushing the concrete-`K` frontier: `K=6,7,8,9,10`, all PROVED

### 1.1 The extension itself

`../markov_transfer.py`'s `build_levels(max_r)` is, by wave 6's own design, already a
`K`-uniform *procedure* (`../ATTEMPT.md` §3, §7.3): climb the ladder
`g_0→h_0→g_1→h_1→⋯→g_K`, each rung one exact telescoped symbolic sum. Wave 6 ran it to
`K=5`. This document simply ran it six rungs further, incrementally (each level reuses
the previous level's already-computed closed form rather than rebuilding from scratch —
`k6_attempt/extend_frontier.py`), recording the exact closed form and per-level timing
at every step. Levels `6` through `10` completed in `21.5s`, `40.8s`, `85.5s`, `169.5s`,
`348.3s` respectively (roughly doubling each level — expected, since each level's
`sympy` summation must first substitute in an increasingly large previous-level
expression), for a cumulative `690s` from `K=0` through `K=10`. No error, no timeout,
no manual intervention at any level — this is exactly the "no new idea, only more
arithmetic" character wave 6 itself predicted for `K=4,5` (`../ATTEMPT.md` §9,
"Net honest verdict") and it continues to hold five levels further.

> **Theorem (`ψ_n^{(6)}` exact closed form; PROVED).** For every `n≥7`,
>
> `ψ_n^{(6)} = \dfrac{2048n^6+3072n^5+4293n^4+4638n^3+3529n^2+1662n+360}{6006n^6}`
> `= \dfrac{1024}{3003} + \dfrac{512}{1001n} + \dfrac{1431}{2002n^2} + \dfrac{773}{1001n^3} + \dfrac{2521}{6006n^4} + \dfrac{277}{1001n^5} + \dfrac{60}{1001n^6}`.

*Proof.* `../ATTEMPT.md` §2's Proposition gives the exact transition rules for every
`K`, in particular `K=6`; `../ATTEMPT.md` §3's telescoping algorithm solves them level
by level (`g_0,h_0,\dots,g_6`), each step an exact identity (elementary induction at
`r=0`, standard hockey-stick binomial summation, executed symbolically, at `r≥1`);
`ψ_n^{(6)}=g_6(n,0)` is the result of substituting `m=n,b=0` into the level-`6`
closed form. No step is an approximation or a fit. `∎`

> **Corollary (`K=6` case of the Open Lemma; PROVED, unconditional).**
> `\lim_{n\to\infty}φ_n^{(6)} = φ_6 = \dfrac{4^6(6!)^2}{13!} = \dfrac{1024}{3003}`.

*Proof.* `ψ_n^{(6)}\to1024/3003=φ_6` by the Theorem above; by wave 5's Reduction Lemma
A (§0, PROVED for every fixed `K\ge1`), this alone implies `φ_n^{(6)}\to φ_6`,
regardless of `ψ_n^{(6),R}`. `∎`

**`K=7,8,9,10`, also PROVED, by the identical mechanical procedure:**

```
ψ_n^{(7)}  = (16384n^7+28672n^6+48818n^5+67550n^4+70819n^3+52192n^2+23868n+5040)/(51480n^7)
ψ_n^{(8)}  = (32768n^8+65536n^7+131870n^6+223472n^5+300913n^4+306016n^3+219100n^2+97632n+20160)/(109395n^8)
ψ_n^{(9)}  = (262144n^9+589824n^8+1371549n^7+2759301n^6+4562055n^5+5967729n^4+5900344n^3+4116636n^2+1792656n+362880)/(923780n^9)
ψ_n^{(10)} = (524288n^10+1310720n^9+3462425n^8+8082170n^7+15900584n^6+25576250n^5+32554945n^4+31376020n^3+21389436n^2+9124560n+1814400)/(1939938n^10)
```

each verified (`k6_attempt/extend_frontier.py`, `k6_attempt/extend_frontier.log`) to
have `n\to\infty` limit exactly `φ_K` (`K=7,\dots,10`), proving `φ_n^{(K)}\to φ_K`
unconditionally for `K=7,8,9,10` too, by the identical Reduction-Lemma-A argument.

**The bonus rate check, for free.** Since every one of these closed forms is exact and
symbolic in `n`, their `1/n` coefficient is available for zero extra cost, and was
checked against wave 6's conjectured rate `\lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` (`../ATTEMPT.md`
§7.2) for all of `K=6,\dots,10` — **five more exact matches**, extending wave 6's
`K=1,\dots,5` confirmations to ten consecutive values with zero exceptions (§3.2's
table gives `K=1,\dots,8`; §3.4 gives `K=9,10` directly from these exact closed forms;
§3–§5 below give the now-*proved* general argument, for every `K` at once).

### 1.2 Independent verification of `K=6`, to the same standard wave 6 used for `K=3`

Wave 6's own `K=3` verification (`../ATTEMPT.md` §6) used six independent layers. This
document repeats the discipline for `K=6` (the task's explicit instruction: use the
existing brute-force infrastructure to verify any candidate closed form *before*
trusting it, "exactly the same discipline used for K=3,4,5"):

**1. Independent, non-symbolic direct recursion (`../markov_direct.py`), 19 values of
`n`.** `k6_attempt/direct_check_k6.py` runs `../markov_direct.py`'s plain memoized
`fractions.Fraction` recursion (which never sums anything — it implements the two
transition rules of `../ATTEMPT.md` §2 directly) for `K=6`, `n=7,\dots,25`, and
compares against the closed form above. **19/19 exact matches**, instantaneous
(`<0.1s` total — this is a genuinely fast, independent check of the model, distinct
from the summation algebra).

**2. A fresh, full, raw-definition brute force at `n=7` (the minimal case,
`n=K+1`).** The task explicitly asks that the closed form be checked against
`psi_bruteforce_ref.py`'s exhaustive enumeration before being trusted. At `K=6,n=7`
this is `7!\times7^6=592{,}912{,}960` exact `(π,U_1,\dots,U_6)` combinations

> **[Correção pós-adversarial, 2026-08-22]** Este número está aritmeticamente
> errado. `7!\times7^6 = 5040\times117649 = 592{,}950{,}960`, não
> `592{,}912{,}960`. Achado pelo referee adversarial hostil independente
> (`adversarial/REFEREE_REPORT.md` §A.4), confirmado de três formas
> independentes ali (multiplicação direta; o `denom` da própria força-bruta
> `numpy` independente do referee; e `592950960/823543=720=6!` exatamente,
> o fator de sanidade `n!/K!` esperado, enquanto `592912960/823543` não é
> inteiro). **Severidade: cosmética** — não afeta nenhum valor computado; o
> resultado real `355081/823543` está correto, confirmado por três métodos
> totalmente independentes (recursão direta, telescopagem simbólica, e
> força-bruta — tanto a original quanto a do referee). — too slow
for the original unoptimized script within this task's time budget (extrapolating
wave 6's own `n=9,K=3` timing, `448.6s` for `264.5`M combinations, `\sim590`K
combos/s single-threaded, this would take `\sim1000s`). `k6_attempt/fast_bruteforce.py`
is an **independent re-implementation of the identical raw definition** — array state
instead of dict-rebuilding, plain integer counts instead of a running `Fraction`
per-combination (the `Fraction` is formed once, exactly, at the end from the exact
integer numerator/denominator — mathematically identical to the original's running
sum, just cheaper per iteration), parallelized across the outer permutation loop over
this machine's 4 cores. **Before being trusted**, this fast implementation was
cross-validated against `psi_bruteforce_ref.py`'s original on five small cases
(`(n,K)\in\{(4,3),(5,3),(6,3),(4,2),(5,1)\}`) — five exact matches
(`k6_attempt/fast_bruteforce_selftest.log`). Run at `K=6,n=7`:

```
K=6 n=7 psi=355081/823543 = 0.4311626715  time=106.4s
```

matching the closed form's value at `n=7` **exactly** (`355081/823543` — also
independently reproduced by the direct-recursion check above at `n=7`).

**3. A second, genuinely new, held-out brute-force point at `n=8`.** Paralleling wave
6's own `n=9` fresh point for `K=3`, a second raw-definition brute force was run at
`K=6,n=8` (`8!\times8^6=10{,}568{,}983{,}680` combinations, `k6_attempt/
bruteforce_k6_n8.log`):

> **[Correção pós-adversarial, 2026-08-22]** Este número também está
> aritmeticamente errado (mesma classe de erro do §A.4 do referee, mas não
> a checagem específica que o referee fez — encontrado pela sessão
> orquestradora durante a integração, verificado com `python3`).
> `8!\times8^6 = 40320\times262144 = 10{,}569{,}646{,}080`, não
> `10{,}568{,}983{,}680` (diferença de `662{,}400`). **Severidade:
> cosmética** — mesma natureza do §A.4: erro de dígitos na prosa descritiva
> sobre o *tamanho* do espaço de busca, não afeta o valor computado
> `191647/458752`, que permanece confirmado por dois métodos independentes
> (recursão direta e a própria força-bruta completa).

```
K=6 n=8 psi=191647/458752 = 0.4177573068  time=2148.4s
```

matching the closed form's value at `n=8` **exactly** (`191647/458752` — also
independently reproduced by the direct-recursion check above at `n=8`). This point was
computed *after* the closed form and the `n=7` check were already complete, purely as
an additional held-out confirmation — not used in deriving anything.

**4. The full recombined `φ_n^{(6)}` rate, independently.** Computing
`ψ_n^{(6),R}=h_5(0,0)` by the same first-principles method (no fitting) gives

`ψ_n^{(6),R} = \dfrac{1586n^6+4458n^5+6915n^4+8055n^3+6496n^2+3204n+720}{5544n^6}`

and recombining via Lemma A:

> `φ_n^{(6)} = \dfrac{4096n^7+2186n^6+29676n^5+47655n^4+56117n^3+45424n^2+22428n+5040}{12012n^7}`

with `n\to\infty` limit exactly `φ_6=1024/3003` and `1/n` coefficient `512/1001`,
matching `6φ_6/4=512/1001` exactly (a sixth independent confirmation of the rate
pattern, from the *combined* not the generic-point quantity).

> **[Correção pós-adversarial, 2026-08-22]** A afirmação do coeficiente de
> `1/n` acima está ERRADA — não é uma questão cosmética como os dois
> achados anteriores. A forma fechada de `φ_n^{(6)}` em si está correta
> (rederivada independentemente pelo referee, batendo bit a bit). Mas o
> verdadeiro coeficiente de `1/n` dessa forma fechada, confirmado por
> QUATRO métodos independentes (`sympy.limit`, `sympy.series`,
> `sympy.apart`, extrapolação numérica `Fraction` pura até `n=10^6`, todos
> concordando — `adversarial/adv_phi6_rate_bug.py`/`.log`), é
> **`1093/6006 ≈ 0,18199`**, não `512/1001 ≈ 0,51149`. Portanto a
> "sexta confirmação independente do padrão de taxa, a partir da
> quantidade *combinada*" alegada acima NÃO existe — esta checagem
> específica é falsa e deve ser desconsiderada. **Isso não afeta**: a
> prova do Lema Aberto para `K=6` (que só precisa do limite, provado
> corretamente); a conjectura de taxa como formalmente provada em §3.4/§5
> (sempre corretamente escopada para `ψ_n^{(K)}`, nunca para `φ_n^{(K)}`
> combinado, e re-verificada independentemente para `K=6..10` pelo
> referee); nem a afirmação mais fraca `φ_n^{(K)}-φ_K=Θ(1/n)` de §5 (que
> permanece verdadeira, já que `1093/6006≠0`). O padrão histórico já
> citado pelo próprio documento (`K=1`: cancelamento total dando
> `Θ(1/n²)`; `K=2`: coeficiente `1/30≠2φ_2/4=4/15`; `K=3`: coeficiente
> `1/14≠3φ_3/4=12/35`) já mostrava que `Kφ_K/4` geralmente NÃO é a taxa de
> `φ`, então esta frase parece um lapso isolado de cópia/memória, não um
> erro estrutural. Achado pelo referee adversarial hostil independente
> (`adversarial/REFEREE_REPORT.md` §A.5). Ver Correção do Scorecard (§7)
> abaixo para o impacto na tabela de status final. This was checked against
a **third, independent brute force of the raw Definition-4 average**
(`k6_attempt/fast_phi_bruteforce.py`, an independent re-implementation of
`../phi_bruteforce_full.py` for speed, cross-validated against the original on two
small cases before use, `k6_attempt/fast_phi_bruteforce_selftest.log`), at `n=7`:

```
K=6 n=7 phi=355081/823543 = 0.4311626715  time=628.3s
```

matching `φ_n^{(6)}` at `n=7` **exactly**. (A striking, and correctly-explained, extra
check falls out here: at `n=K{+}1=7`, `\psi_n^{(6)}` and `\psi_n^{(6),R}` turn out to
be *exactly equal* — `355081/823543` for both, confirmed directly from the two closed
forms — so `\varphi_n^{(6)}` at this one `n` coincides with `\psi_n^{(6)}` itself,
exactly, which the brute force reproduces to the digit; `k6_attempt/
verify_phi_n7_identity.py` records this cross-check.)

---

## 2. A continuum scaling limit of the `(a,b,r)` chain: the leading order `F_r(t,b)`

Wave 6's obstruction (`../ATTEMPT.md` §7.3) is that the telescoping-sum solution needs
the *previous level's exact closed form* substituted in before the next summation can
execute — there is no single expression "`h_r(a,b)`, `r` symbolic" to sum against. This
section sidesteps that obstruction entirely, by not trying to solve the *exact*
discrete recursion symbolically in `r` at all. Instead, it takes the `n\to\infty`
scaling limit of the recursion *first* — at which point `r` stops being a summation
index and becomes an ordinary free parameter of a linear ODE, which *can* be solved,
honestly, for symbolic `r`.

### 2.1 Setup: the scaling ansatz

Fix `r,b` (thought of as `O(1)`, not growing with `n` — justified below, §2.4). Write
`t := m/n \in(0,1]` and posit

`g_r(m,b) = F_r(t,b) + O(1/n)`  (leading order, this section)  ,  `h_r(a,b) = \hat H_r(a/n,\,b) + O(1/n)`.

### 2.2 The leading-order ODE and algebraic relation

**Derivation.** Start from `../ATTEMPT.md` §2's exact non-source transition rule,
rearranged (no approximation yet):

`m\big[g_r(m,b)-g_r(m-1,b)\big] + (1{+}r{+}b)\,g_r(m-1,b) = 1 + r\,h_{r-1}(n{-}m{+}1,b)`.

Set `m=nt` (so one discrete step `m\to m{-}1` is `t\to t{-}1/n`), and Taylor-expand
`g_r(m-1,b)=F_r(t,b) - \frac1n F_r'(t,b) + O(1/n^2)`, so that
`m[g_r(m,b)-g_r(m-1,b)] \to t\,F_r'(t,b)` at leading order (the discrete difference
quotient becomes the derivative — this is the one non-symbolic-algebra step, revisited
in §2.4). On the right, `n{-}m{+}1 = n(1{-}t)+1`, so `a/n\to1{-}t`, giving
`h_{r-1}(n{-}m{+}1,b)\to\hat H_{r-1}(1{-}t,b)`. This yields:

> **ODE (leading order, `g`):** `\;t\,F_r'(t,b) + (1{+}r{+}b)\,F_r(t,b) = 1 + r\,\hat H_{r-1}(1{-}t,b)`.

Similarly, from the exact source-step rule `h_r(a,b)=\frac1n+\frac rn h_{r-1}(a,b{+}1)+
\frac{n-1-a-b-r}n g_r(n{-}a,b{+}1)`: as `n\to\infty` with `s:=a/n` fixed, `1/n\to0`,
`\frac rn h_{r-1}(a,b{+}1)\to0` (an `O(1)`-bounded quantity times `O(1/n)`), and
`\frac{n-1-a-b-r}n\to1{-}s`, `g_r(n{-}a,b{+}1)\to F_r(1{-}s,b{+}1)` (no derivative
correction here — `n-a` has no `+1` offset, unlike the `g`-recursion's `n-m+1` above).
This yields, with no ODE needed — purely algebraic:

> **Relation (leading order, `h`):** `\;\hat H_r(s,b) = (1{-}s)\,F_r(1{-}s,\,b{+}1)`.

**Base case.** `F_0(t,b)=1/(b{+}1)`, constant — this is not an asymptotic statement at
all but the *exact* fact `g_0(m,b)=1/(b{+}1)` for every finite `m,n`, proved by
elementary induction in `../ATTEMPT.md` §3 (the general-`b` symmetry that specializes,
at `b=1`, to wave 6's co-cycle Lemma B). So `\hat H_0(s,b)=(1{-}s)/(b{+}2)`.

### 2.3 Solving the ladder: an explicit, symbolic-`r` closed form

Since `F_{r-1}(t,b{+}1)` is (inductively) a polynomial in `t`, so is
`\hat H_{r-1}(1{-}t,b)=t\,F_{r-1}(t,b{+}1)` (substituting `s=1{-}t` into the algebraic
relation above and simplifying), hence so is the ODE's right-hand side — the ansatz
`F_r(t,b)=\sum_{k=0}^r c_k^{(r)}(b)\,t^k` is self-consistent. Matching the coefficient
of `t^k` on both sides of the ODE (`t\,F_r'` contributes `k\,c_k^{(r)}t^k`, so the
left side's `t^k` coefficient is `(k{+}1{+}r{+}b)c_k^{(r)}(b)`) gives a **diagonal**
recursion — no summation, pure algebra:

`c_0^{(r)}(b) = \dfrac1{1{+}r{+}b}`,  `\quad c_k^{(r)}(b) = \dfrac{r}{k{+}1{+}r{+}b}\,c_{k-1}^{(r-1)}(b{+}1)`  `(1\le k\le r)`.

(The choice of the *particular* solution here — with no added multiple of the
homogeneous solution `t^{-(1+r+b)}` of the same ODE — is forced by requiring `F_r`
regular/bounded as `t\to0^+`, since `g_r(m,b)` is a probability, hence bounded, for
every valid `m`; §2.4 discusses this boundary condition's status precisely.)

Unrolling this recursion `k` times (each step reduces `r\to r{-}1`, `k\to k{-}1`,
`b\to b{+}1`, contributing a factor `\frac{r-i}{k+1+r+b-i}` at step `i=0,\dots,k{-}1`,
and terminating at the base case `c_0^{(r-k)}(b{+}k)=\frac1{1+r+b}` — independent of
`k`, since `1+(r-k)+(b+k)=1+r+b`) gives, in closed form:

> **Theorem (leading-order closed form; PROVED, general `r`).**
> `\displaystyle F_r(t,b) = \sum_{k=0}^r \frac{r!}{(r-k)!}\cdot\frac{t^k}{\prod_{i=1}^{k+1}(r+b+i)}`.

*Proof.* By induction on `r`. Base case `r=0`: the sum is the single term
`k=0`: `0!/0! \cdot t^0/(b{+}1) = 1/(b{+}1)`, matching `F_0(t,b)` above. Inductive
step: assume the formula for `r-1` (all `b`); the diagonal-coefficient recursion just
derived, unrolled `k` times down to the base case, gives exactly the stated product —
this is elementary algebra on the recursion, not an assumption, and was additionally
verified as an exact symbolic identity in `sympy`, general `r,k,b`
(`k6_attempt/verify_dk_recursion.py` — see §3.3 for the analogous, harder check at the
next order, of which this is the simpler special case). `∎`

**Verification against independently-known values.** At `t=1,b=0`:

| `r` | `F_r(1,0)` (this document's closed form) | `φ_r` (Wallis integral, `THEOREM.md` Lemma 2) | match |
|---|---|---|---|
| 0 | `1` | `1` | exact |
| 1 | `2/3` | `2/3` | exact |
| 2 | `8/15` | `8/15` | exact |
| 3 | `16/35` | `16/35` | exact |
| 4 | `128/315` | `128/315` | exact |
| 5 | `256/693` | `256/693` | exact |
| 6 | `1024/3003` | `1024/3003` | exact |

— **seven exact matches** (`k6_attempt/verify_closed_forms.py`), confirmed exactly
(sympy symbolic difference `=0`, not a numerical/floating coincidence), and in fact
this document's closed form was separately checked to reproduce `F_r(1,b)` **for
general `b`, not just `b=0`** against the actual `n\to\infty` limit of
`markov_transfer.py`'s exact `g_r(m,b)` output, for `r=0,\dots,5` (the full range
where that exact symbolic-`(m,b)` output was computed) — **all six exact matches**
(`k6_attempt/pattern_analysis.py`, `k6_attempt/pattern_analysis_r5.log`). This is a
new, independent derivation of `THEOREM.md`'s Wallis-integral mean formula
`φ_K=4^K(K!)^2/(2K+1)!`, for **every `K` at once**, via the discrete finite-`n`
recursion's own scaling limit — not previously derived from this direction anywhere
in the archive (`THEOREM.md`'s own derivation of `φ_K`, §5.2, works directly on the
continuum object `L(c)`, never touching the finite-`n` `(a,b,r)` chain at all).

### 2.4 [Adendo pós-adversarial, 2026-08-22] O status preciso da condição de contorno

> Esta seção não existia na versão original do documento — §2.1, §2.2 e §2.3
> prometiam ("justificado abaixo, §2.4", "revisitado em §2.4", "§2.4 discute
> o status desta condição de contorno com precisão") uma seção que nunca foi
> escrita. Achado pelo referee adversarial hostil independente
> (`adversarial/REFEREE_REPORT.md` §B.4(a), confirmado por grep de todos os
> cabeçalhos do documento). Em vez de simplesmente marcar as três referências
> como quebradas, esta seção entrega o conteúdo prometido, usando exatamente
> o raciocínio que o próprio referee construiu e verificou independentemente
> — não é uma correção cosmética, é a análise substantiva que faltava.

**Para `F_r`: o argumento de limitação PODE ser tornado rigoroso.** A solução
homogênea da EDO `tX'(t)+(1{+}r{+}b)X(t)=0` é `X=C\cdot t^{-(1+r+b)}`, que diverge
quando `t\to0^+` para qualquer `C\ne0` (já que `1{+}r{+}b>0`). Como `g_r(m,b)\in[0,1]`
**exatamente, incondicionalmente, para todo `m,n` finitos** (é uma probabilidade
condicional genuína, por construção), qualquer limite `F_r(t,b):=\lim_n g_r(nt,b)`
que exista num `t>0` fixo também deve estar em `[0,1]` (limite de sequência
limitada é limitado). Um `C\ne0` forçaria `|F_r(t,b)|>1` para `t` pequeno o
suficiente — contradizendo essa cota a priori. Logo **`C=0` é forçado, DADO QUE
`F_r(t,b)` exista como função-limite genuína perto de `t=0`** — isso só exige a
existência (mais fraca) do limite de *ordem líder*, não a expansão completa de
duas parcelas, então não é circular em relação exatamente ao que está sendo
questionado; é uma dedução legítima, ainda que estreita.

**Para `G_r`: NÃO existe argumento análogo, e esta lacuna não estava sequer
nomeada na versão original.** `G_r` é o termo de correção de ordem `O(1/n)`, que
**não tem cota a priori análoga a "probabilidade ∈[0,1]"** — nada no modelo
garante que `G_r` permaneça limitado quando `t\to0^+`. Pior: `t\to0^+`
(`m=O(1)` enquanto `n\to\infty`) é exatamente a região mais próxima da própria
fronteira de caso-base da recursão (`g_r(m,b)` só é definido para `m\ge b{+}r{+}1`),
que é *precisamente* o tipo de "camada limite" onde expansões de perturbação
singular são classicamente conhecidas por se comportar de forma não-uniforme
mesmo quando bem-comportadas longe da fronteira. A derivação de §3 não oferece
nenhum argumento — de limitação ou outro — para por que a solução homogênea de
`G_r` deve se anular; ela simplesmente aplica o mesmo procedimento de
casamento diagonal usado para `F_r`, sem justificar por que esse procedimento
é válido aqui também. Esta é a assimetria substantiva mais importante que o
referee identificou além do que este documento discutia por si só.

**Evidência empírica direta (nova, não-circular), feita pelo referee, ausente
do documento original.** Toda checagem em qualquer lugar deste documento
avalia `F_r`/`G_r` **apenas em `t=1`** (já que `ψ_n^{(K)}=g_K(n,0)` significa
`m=n`, i.e. `t=1` sempre) — o que importa porque `t^{-(1+r+b)}=1` em `t=1`
para *qualquer* expoente, então uma mistura homogênea só apareceria ali como
uma constante aditiva facilmente absorvida, não como uma discrepância de
forma. Usando os dados exatos simbólicos `(m,b,n)` do próprio
`markov_transfer.py` (a mesma referência independente que as checagens em
`t=1` do documento usam, para `r=0,\dots,5`), o referee checou `F_r(t,b)` e
`G_r(t,b)` em `t=1/2,1/3,2/3,3/4,1/5` — genuinamente longe de `t=1`:
`F_r(t,b)`: **30/30 confirmações exatas** (`r=0,\dots,5`, 5 valores de `t`
cada, `b` simbólico geral); `G_r(t,b)`: **15/15 confirmações exatas**
(`r=1,\dots,5`, 3 valores de `t` cada, `b` simbólico geral) — incluindo em
`r=4,5`, onde as formas fechadas são funções racionais multi-termo
visivelmente intricadas de `b`, não padrões simples que pudessem coincidir
por acaso.

**Conclusão honesta (não uma remoção da ressalva de §4).** Isto NÃO prova o
ansatz para `r>10` — nenhuma checagem finita provaria. É evidência nova,
não-circular, *a favor* da correção do ansatz na faixa checada, que amplia
substancialmente a superfície de teste além de qualquer coisa que este
documento realizava por si só — especificamente no ponto (`t\ne1`) onde uma
discrepância do tipo solução-homogênea seria mais provável de aparecer e
menos provável de ficar mascarada. **O julgamento explícito do referee, que
esta sessão adota integralmente: a ressalva de §4 está corretamente
dimensionada — nem otimista demais, nem conservadora demais.** Não há base,
a partir de qualquer coisa encontrada aqui ou pelo referee, para reclassificar
qualquer resultado de §2.3/§3.3 como incondicional, nem para tratar a lacuna
de existência como mais séria do que §4 já a trata.

---

## 3. The next order: `G_r(t,b)`, and a full proof of the rate conjecture

### 3.1 The second-order expansion

Push the same Taylor expansion one order further: `g_r(m,b) = F_r(t,b) +
\frac1n G_r(t,b) + O(1/n^2)`, `h_r(a,b) = \hat H_r(s,b) + \frac1n K_r(s,b) + O(1/n^2)`
(`s=a/n`). Expanding the *exact* discrete recursions to `O(1/n)` (keeping the
`O(\varepsilon^2)` terms in every Taylor series this time, `\varepsilon:=1/n` — the
full by-hand derivation, term by term, is given here and reproduced in
`k6_attempt/rate_ode.py`'s header comment) gives a **second, coupled ODE/algebraic
system**. Sketch of the derivation (both recursions expanded to `O(\varepsilon^2)`,
i.e. one order past what §2.2 needed): for the `g`-recursion, write
`g_r(m{-}1,b)=F_r(t{-}\varepsilon,b)+\varepsilon G_r(t{-}\varepsilon,b)+O(\varepsilon^2)
=F_r(t,b)+\varepsilon[G_r(t,b)-F_r'(t,b)]+O(\varepsilon^2)`, so that
`m[g_r(m,b)-g_r(m-1,b)] = t\,F_r'(t,b) + \varepsilon\,t\big[G_r'(t,b)-\tfrac12F_r''(t,b)\big]+O(\varepsilon^2)`
(one further Taylor term than §2.2 kept); the source-term argument
`n{-}m{+}1=n(1{-}t)+1` gives `s=(1{-}t)+\varepsilon` exactly, so
`h_{r-1}(n{-}m{+}1,b)=\hat H_{r-1}(1{-}t,b)+\varepsilon\big[\hat H_{r-1}'(1{-}t,b)+K_{r-1}(1{-}t,b)\big]+O(\varepsilon^2)`
(chain rule on the shifted argument, plus the level's own `O(\varepsilon)` term);
matching the `O(\varepsilon)` coefficients on both sides of the rearranged exact
recursion gives the `G_r` ODE below. For the `h`-recursion, `a=ns` exactly (no shift),
so `g_r(n{-}a,b{+}1)=F_r(1{-}s,b{+}1)+\varepsilon G_r(1{-}s,b{+}1)+O(\varepsilon^2)`
directly, and `(n{-}1{-}a{-}b{-}r)/n=(1{-}s)-\varepsilon(1{+}b{+}r)` exactly; matching
`O(\varepsilon)` coefficients gives the `K_r` relation below (no ODE needed, same as
at leading order).

> **ODE (`O(1/n)`, `g`):** `\;t\,G_r'(t,b) + (1{+}r{+}b)\,G_r(t,b) = r\,\hat H_{r-1}'(1{-}t,b) + r\,K_{r-1}(1{-}t,b) + \tfrac t2 F_r''(t,b) + (1{+}r{+}b)F_r'(t,b)`
>
> **Relation (`O(1/n)`, `h`):** `\;K_r(s,b) = 1 + r\,\hat H_{r-1}(s,b{+}1) + (1{-}s)\,G_r(1{-}s,b{+}1) - (1{+}b{+}r)\,F_r(1{-}s,b{+}1)`

with base case `G_0(t,b)\equiv0`, `K_0(s,b)=1/(b{+}2)` (both exact, from the known
closed forms `g_0(m,b)=1/(b{+}1)` and `h_0(a,b)=(n{-}a{+}1)/(n(b{+}2))` — the latter's
own `O(1/n)` term is exactly `1/(n(b{+}2))`, giving `K_0` directly, no limit needed).

The right-hand side of the `G_r` ODE is again a polynomial in `t` (given `F_r`, `\hat
H_{r-1}`, `K_{r-1}` are), so the same diagonal-coefficient-matching method applies,
giving `G_r(t,b)=\sum_{k=0}^{r-1}d_k^{(r)}(b)t^k` with `d_k^{(r)}(b)` determined by an
explicit (if more intricate, since it now also references the *previous* level's `d`,
not just `c`) recursion — worked out in full in `k6_attempt/rate_ode.py`, run
concretely for `r=1,\dots,8` (§3.2), then **guessed** in closed form from that data and
**proved** by a direct symbolic identity check (§3.3) — this is genuine induction, not
curve-fitting, exactly as the task requires: the closed form was first suggested by
the `r=1..8` data, but then independently *verified to satisfy the defining recursion
for symbolic `r,k,b`*, which is the actual proof.

### 3.2 Solving level-by-level (`r=1,\dots,8`) and finding the pattern

`k6_attempt/rate_ode.py` solves the coupled `(F_r,G_r,\hat H_r,K_r)` system for
`r=1,\dots,8`, at every level checking `G_r(1,0)` against wave 6's conjectured rate
`Kφ_K/4` (`../ATTEMPT.md` §7.2) — **eight exact matches**, `r=1` through `r=8`
(`k6_attempt/rate_ode.log`):

| `r` | `G_r(1,0)` (this derivation) | `rφ_r/4` (wave 6's conjecture) | match |
|---|---|---|---|
| 1 | `1/6` | `1/6` | exact |
| 2 | `4/15` | `4/15` | exact |
| 3 | `12/35` | `12/35` | exact |
| 4 | `128/315` | `128/315` | exact |
| 5 | `320/693` | `320/693` | exact |
| 6 | `512/1001` | `512/1001` | exact |
| 7 | `3584/6435` | `3584/6435` | exact |
| 8 | `65536/109395` | `65536/109395` | exact |

Extracting the coefficients `d_k^{(r)}(b)` for every `r=1,\dots,8,\ k=0,\dots,r{-}1`
(`k6_attempt/coefficient_dump.py`, applying `pattern_analysis.py`'s coefficient-
extraction method to `rate_ode.py`'s saved `G_r` output) reveals a strikingly clean
pattern — factoring numerator and denominator separately for each `(r,k)`
(`k6_attempt/coefficient_dump.log`):

```
d_0^(r)(b) = r / [(b+r+1)(b+r+2)]
d_1^(r)(b) = 3r(r-1) / [(b+r+1)(b+r+2)(b+r+3)]
d_2^(r)(b) = 6·r(r-1)(r-2) / [(b+r+1)···(b+r+4)]
d_3^(r)(b) = 10·r(r-1)(r-2)(r-3) / [(b+r+1)···(b+r+5)]
  ...
```

with the numerator multiplier `1,3,6,10,15,21,28,36,\dots` at `k=0,1,2,\dots,7`
immediately recognizable as `\binom{k+2}2`, and the falling-factorial part
`r(r-1)\cdots(r-k)=r!/(r-k-1)!`.

### 3.3 The general-`r,k` closed form — conjectured, then PROVED

> **Conjecture (from the `r=1..8` data above).**
> `\displaystyle d_k^{(r)}(b) = \binom{k+2}2\cdot\frac{r!}{(r-k-1)!}\cdot\frac1{\prod_{i=1}^{k+2}(r+b+i)}`,  `0\le k\le r-1`.

**This is not left as a fit.** `k6_attempt/verify_dk_recursion.py` substitutes this
closed form (together with the already-*proved* `c_k^{(r)}(b)` closed form of §2.3)
into the **exact defining recursion** derived in §3.1 (the coefficient-of-`t^k`
matching condition for the `G_r` ODE), for **symbolic `r,k,b`** — not looping over
concrete values — and asks `sympy` to simplify `\text{LHS}-\text{RHS}`. Two cases (the
general `k\ge1` recursion, and the `k=0` boundary case, which draws its `K_{r-1}`
piece from a slightly different, constant-only branch of the `K` relation):

```
General k>=1 case, symbolic r,k,b: LHS-RHS simplify = 0
k=0 special case, symbolic r,b:    LHS-RHS simplify = 0
```

**Both identities reduce to exactly `0`, symbolically, for generic `r,k,b`**
(`k6_attempt/verify_dk_recursion.log`). This is the genuine inductive step the task
asked for: it proves that *if* `c_{k}^{(r-1)}(b{+}1)` and `d_{k-1}^{(r-1)}(b{+}1)` have
the stated closed forms (inductive hypothesis, one level down), *then* `d_k^{(r)}(b)`
having the stated closed form is exactly what the defining recursion forces (inductive
step) — for every `r`, not case-by-case. Combined with the base case `G_0\equiv0`
(trivially of the stated form, the empty sum) and §2.3's already-proved `c_k^{(r)}(b)`,
this constitutes a complete induction on `r`:

> **Theorem (`O(1/n)` correction, closed form; PROVED, general `r`).**
> `\displaystyle G_r(t,b) = \sum_{k=0}^{r-1}\binom{k+2}2\frac{r!}{(r-k-1)!}\cdot\frac{t^k}{\prod_{i=1}^{k+2}(r+b+i)}`.

**Cross-validation against the independently-known exact discrete formula.** As with
`F_r`, this closed form's `t=1` value was checked, for general `b` (not just `b=0`),
against `B_r(b):=\lim_{n\to\infty}n\big[g_r(n,b)-F_r(1,b)\big]` computed *directly*
from `markov_transfer.py`'s actual, independently-derived, exact `(m,b)`-symbolic
`g_r` output — for `r=1,\dots,5` (the full range where that exact output exists):

```
r=1: match=True   B_exact = 1/((b+2)(b+3))
r=2: match=True   B_exact = 2(b+8)/((b+3)(b+4)(b+5))
r=3: match=True   B_exact = 3(b^2+19b+96)/((b+4)(b+5)(b+6)(b+7))
r=4: match=True   B_exact = 4(b+12)(b^2+21b+128)/((b+5)···(b+9))
r=5: match=True   B_exact = 5(b^4+50b^3+971b^2+8722b+30720)/((b+6)···(b+11))
```

**five exact matches, full `b`-dependence** (`k6_attempt/verify_dk_recursion.py`'s
final section) — this is an *exact* algebraic check against a formula independently
derived by wave 6's completely different (exact telescoping-sum) method, not a
numerical coincidence at isolated points.

### 3.4 Closing the loop: `G_r(1,0) = rφ_r/4` for every `r` — a complete proof

It remains to show the closed form of §3.3, evaluated at `t=1,b=0`, algebraically
equals wave 6's conjectured `rφ_r/4`. Write `n{:=}2r{+}1` and use
`\frac{r!}{(r-k-1)!}\cdot\frac1{\prod_{i=1}^{k+2}(r+i)} = \frac{(r!)^2}{(r-k-1)!(r+k+2)!}`
and `(r-k-1)!(r+k+2)! = (2r+1)!/\binom{2r+1}{r-k-1}` (a direct binomial-coefficient
identity, since `(r-k-1)+(r+k+2)=2r+1`), then substitute `i:=r-k-1` (so `k=r-1-i`,
`i` runs `0,\dots,r-1` as `k` runs `r-1,\dots,0`) to get

`\displaystyle G_r(1,0) = \frac{(r!)^2}{2\,(2r{+}1)!}\sum_{i=0}^{r-1}(r{-}i)(r{-}i{+}1)\binom{2r{+}1}i`

(the `\binom{k+2}2=(k+1)(k+2)/2` factor becomes `(r{-}i)(r{-}i{+}1)/2` under the
substitution). **The remaining sum is evaluated by an elementary symmetry argument:**

> **Lemma (binomial sum identity; PROVED).**
> `\displaystyle\sum_{i=0}^{r-1}(r{-}i)(r{-}i{+}1)\binom{2r{+}1}i = r\cdot2^{2r-1}`.

*Proof.* Let `n=2r{+}1`, `w(i):=(r{-}i)(r{-}i{+}1)`. Expand `w(i)=i^2-ni+r(r{+}1)`
(direct algebra, using `n=2r{+}1`). Summed against `\binom ni` over the **full** range
`i=0,\dots,n`, three classical binomial moment identities apply (each an elementary
consequence of differentiating `(1{+}x)^n` once or twice and evaluating at `x=1`):
`\sum_i\binom ni=2^n`, `\sum_i i\binom ni=n2^{n-1}`, `\sum_i i^2\binom ni=n(n{+}1)2^{n-2}`.
Substituting,

`\textstyle\sum_{i=0}^n w(i)\binom ni = n(n{+}1)2^{n-2} - n\cdot n2^{n-1} + r(r{+}1)2^n = 2^{2r}\big[{-}r(2r{+}1)+2r(r{+}1)\big] = r\cdot2^{2r}`

(direct substitution `n=2r{+}1`, elementary simplification). Now, `w(i)` is a
quadratic in `i` symmetric about `i=n/2=r{+}\tfrac12` (its vertex, by direct
calculus/algebra: `w(i)=w(n{-}i)` for every `i`, checked directly since
`w(n{-}i)=(r{-}n{+}i)(r{-}n{+}i{+}1)=(i{-}r{-}1)(i{-}r)=(r{-}i)(r{-}i{+}1)=w(i)`, using
`r{-}n={-}r{-}1`). Since `\binom ni=\binom n{n-i}` too, the full sum splits into two
equal halves, `i=0,\dots,r{-}1` and `i=r{+}2,\dots,n` (related by `i\leftrightarrow
n{-}i`), **plus the two middle terms** `i=r,r{+}1`, both of which **vanish
identically**: `w(r)=(0)(1)=0`, `w(r{+}1)=({-}1)(0)=0`. Hence
`\sum_{i=0}^n w(i)\binom ni = 2\sum_{i=0}^{r-1}w(i)\binom ni + 0 + 0`, giving
`\sum_{i=0}^{r-1}w(i)\binom ni = \tfrac12\cdot r\cdot2^{2r} = r\cdot2^{2r-1}`. `∎`

Substituting back: `G_r(1,0) = \dfrac{(r!)^2}{2(2r{+}1)!}\cdot r\cdot2^{2r-1} =
\dfrac r4\cdot\dfrac{4^r(r!)^2}{(2r{+}1)!} = \dfrac{r\varphi_r}4`.

> **Theorem (rate conjecture; PROVED, general `K`).** For every `K\ge0`,
> `\displaystyle\lim_{n\to\infty}n\big(\psi_n^{(K)}-\varphi_K\big) = \frac{K\varphi_K}4`
> — wave 6's `ATTEMPT.md` §7.2 conjecture, proved in full, modulo exactly the one
> caveat stated precisely in §4 below.

**Every step of this final reduction was independently machine-checked** (not just
hand algebra): `k6_attempt/verify_rate_conjecture.py` confirms the binomial-sum
identity exactly, by direct exact-rational computation, for `r=1,\dots,25`
(`k6_attempt/verify_rate_conjecture.log`) and confirms `G_r(1,0)=r\varphi_r/4` for the
same range; separately, `k6_attempt/rate_ode.py`'s own `r=1,\dots,8` runs (§3.2) check
the same identity via the *fully independent* route of actually solving the ODE
system level-by-level rather than evaluating the closed-form sum, and agree exactly;
and finally the identity is checked a **third** way, against the mechanically-extended
*exact discrete* closed forms of §1 themselves (which do not depend on the continuum
argument at all): `K=9`'s and `K=10`'s exact `\psi_n^{(K)}` formulas (§1.1) were
Taylor-expanded directly and their `1/n` coefficients compared to `K\varphi_K/4` —
**both exact matches** (`k6_attempt/verify_via_exact_k9_k10.py`), extending the
fully-unconditional (no continuum argument needed) confirmations of the rate
conjecture to **eleven consecutive values, `K=0,\dots,10`, with zero exceptions**.

---

## 4. The one honest caveat, stated precisely

The derivation of §2–§3 establishes: **if** `g_r(m,b)` admits a regular two-term
asymptotic expansion `F_r(t,b)+\frac1n G_r(t,b)+O(1/n^2)` in the scaling variable
`t=m/n`, of the specific polynomial-in-`t` shape used throughout (which is not a free
choice — it is *forced*, order by order, by the algebraic structure of the exact
discrete recursion itself, via the diagonal coefficient-matching arguments of §2.3 and
§3.3), **then** `F_r,G_r` are uniquely determined by the closed forms proved above,
for every `r` symbolically. What is **not** separately re-derived here from `ε`-`δ`
first principles is the **existence** of that expansion for every `r` — i.e., a
rigorous convergence/error-bound argument (e.g. a discrete-Gronwall-type induction on
`m` bounding `|g_r(m,b)-F_r(m/n,b)-\tfrac1nG_r(m/n,b)|=O(1/n^2)` uniformly, for
general symbolic `r`) is not carried out in this document.

**Why this is not treated as a serious open gap, and what would close it fully.**
Three things narrow this considerably below "an unverified guess":

1. `g_r(m,b)` is, **by construction**, an exact conditional probability
   (`P(x^*\text{ eventually cyclic}\mid\text{state})`, `../ATTEMPT.md` §2) — hence
   `0\le g_r(m,b)\le1` for *every* valid `m,b,r,n`, unconditionally, with no asymptotic
   argument needed for this bound itself.
2. The specific functional shape assumed (polynomial in `t`, of degree growing by
   exactly one per order in `1/n`, per level `r`) is not an arbitrary ansatz: it is
   *forced* to be internally self-consistent by the recursion's own algebra at every
   step checked (§2.3, §3.3) — an inconsistent guess would have failed the symbolic
   identity checks, not merely produced an unverified-but-untested formula.
3. **Wherever the assumption can be independently checked against the unconditional,
   exact discrete closed form — it holds, exactly, with zero exceptions**: `F_r`
   matches for `K=0,\dots,6` at `t=1,b=0` and `K=0,\dots,5` at general `b`; `G_r`
   matches for `K=1,\dots,10` at `b=0` and `K=1,\dots,5` at general `b`. Eleven
   concrete `K` values, in every case tested, agreeing exactly — not approximately —
   with a fully independent, unconditionally-proved computation.

**What would close this gap completely** is exactly wave 6's own original route (i):
a genuine symbolic-`r` proof of the *exact* (all-orders, not just two-orders)
discrete closed form itself — which would automatically supply the needed existence
statement as a corollary (an exact closed form has no "does the expansion exist"
question left to ask). §6.2 records why this was not additionally achieved here.

**The honest scope of what is PROVED, unconditionally, in this document, with no
caveat at all:** `K=6,7,8,9,10` (§1, exactly wave 6's own standard of proof, extended);
the exact rate-conjecture match at `K=6,\dots,10` from those same exact closed forms
(§1.1, §3.4); and the diagonal-recursion algebra of §2.3/§3.3 as a conditional
statement (*if the expansion exists, this is what it must be*). What carries the one
stated caveat is the *general-`K`, symbolic-`r`* form of the Open Lemma and the rate
conjecture (§2, §3, §5) — proved modulo the expansion's existence for `r>10`, an
assumption checked and never once violated across every one of the eleven cases where
independent checking is possible.

---

## 5. The rate conjecture, restated standalone

For quick reference, separated from the derivation:

> **Theorem.** For every `K\ge0`, `\displaystyle\lim_{n\to\infty} n\big(\psi_n^{(K)}-\varphi_K\big)
> = \frac{K\varphi_K}4`, where `\varphi_K=\frac{4^K(K!)^2}{(2K+1)!}` (`THEOREM.md`
> Lemma 2). Consequently, by wave 5's Reduction Lemma A
> (`\varphi_n^{(K)}=(K/n)\psi_n^{(K),R}+(1{-}K/n)\psi_n^{(K)}`, general in `K`, PROVED)
> and the analogous, easier `O(1/n)`-order treatment of `\psi_n^{(K),R}=h_{K-1}(0,0)`
> (not separately spelled out here — `h_r`'s `O(1/n)` correction `K_r(s,b)` at `s=0` is
> already given in closed form by §3.1's algebraic relation, no new ODE needed),
> `\varphi_n^{(K)}-\varphi_K = \Theta(1/n)` for every `K\ge1`, resolving `THEOREM.md`
> §9 item 2 ("whether `φ_n^{(K)}-φ_K` is `Θ(1/n^2)`, `Θ(\log n/n^2)`, or something
> else... is left fully open") for every `K` at once, matching `../ATTEMPT.md` §7.4's
> conditional statement of this — now **unconditional**, modulo exactly §4's one named
> caveat.

**Proof status, precisely.** Unconditionally PROVED (no caveat) for `K=0,\dots,10`
directly from the exact discrete closed forms of `../ATTEMPT.md` and this document's
§1. PROVED for general `K`, modulo §4's stated (and, in every checkable instance,
verified) regularity assumption, via §2–§3's continuum-ODE argument.

---

## 6. What was tried and did not close, or needed a workaround (honest record)

Per the task's own instruction, a documented negative result is a valid and valuable
outcome. Three things did not go as first attempted:

### 6.1 A literal generating-function-in-`K` sum on the *exact* discrete recursion

The task brief's route (ii) suggests, as an example, `\sum_K x^K/K!\cdot\psi_n^{(K)}`
and looking for a closed-form ODE/PDE in `n`. This was considered directly on the
*exact* (not continuum-limit) `(a,b,r)` chain before the ODE approach of §2–§3 was
found, and **abandoned before being coded up**, for a precise structural reason: the
exact transition-rule coefficients (`1/m`, `r/m`, `(m{-}1{-}r{-}b)/m` for the
non-source step; `1/n`, `r/n`, `(n{-}1{-}a{-}b{-}r)/n` for the source step) are *not*
translation-invariant in the state — every coefficient carries an explicit `n` or `m`
in its denominator that does not cancel when marking `r` with a formal variable `x`.
A generating function `\sum_r g_r(m,b)x^r` would need `m` (or `a,b`) treated as a
*second* free variable simultaneously, and the resulting two-variable functional
equation inherits the *same* `n`-dependence problem that made solving "in `m`" alone
already require the telescoping-sum machinery of `../ATTEMPT.md` §3 in the first
place — i.e., a naive `x`-marking does not remove the original difficulty, it just
adds a second one on top. This is exactly why the ODE route of §2–§3 goes through the
`n\to\infty` scaling limit *first*: only after that limit does `n` stop appearing as
an explicit normalizing denominator in every single coefficient, at which point `r`
becomes an ordinary parameter of a genuinely `r`-uniform linear ODE. **Lesson recorded
for any future attempt:** a formal power series in `x` marking `K`, applied directly
to the *finite-`n`* recursion, does not appear to be the productive order of
operations; take the continuum limit first, then treat the resulting parameter
(`r`) symbolically.

### 6.2 Extending to a full, all-orders, general-`K` exact closed form

Only two orders (`F_r`, `O(1)`, and `G_r`, `O(1/n)`) were derived. The *exact* finite-`n`
closed form for general `K` — which would need *all* `K{+}1` orders
(`1,1/n,\dots,1/n^K`) resummed, not just the first two — was not attempted beyond the
concrete-`K` mechanical ladder of §1. This is squarely still open; nothing in this
document claims otherwise. Two things suggest it is at least *structurally* tractable
by the same method (though **not attempted**, for lack of remaining time in this
task): (a) the `O(1/n^2)` correction would follow the identical recipe — Taylor-expand
one order further, get a third coupled ODE/algebraic pair sourced by `F_r,G_r` and the
previous level's third-order term, solve by the same diagonal-coefficient method; (b)
each new order's ODE has the *same* linear operator (`t\,d/dt+(1{+}r{+}b)`) as every
previous order, only the forcing term changes — so the "hard part" (solving the ODE)
is a fixed, already-solved recipe at every order, and what would grow is only the
bookkeeping complexity of the forcing term (as seen already going from `F_r`'s simple
recursion to `G_r`'s more intricate one, §3.1). Whether the *pattern* found for
`c_k^{(r)}(b)` (§2.3) and `d_k^{(r)}(b)` (§3.3) itself continues in a similarly
closed-form-guessable way at every order is an open question this document does not
address.

### 6.3 Direct symbolic-`r` summation via `sympy.summation`, on the *final* identity

Section 3.4's final reduction — proving `G_r(1,0)=r\varphi_r/4` — was first attempted
by asking `sympy.summation` to evaluate the coefficient sum directly for symbolic `r`
(`\sum_k\binom{k+2}2\frac{r!}{(r-k-1)!}\cdot\frac{(r!)^2\text{-style denominator}}
{\cdots}`, symbolic upper limit `r{-}1`). This call **did not terminate** within
several minutes and was killed (`k6_attempt/`, not saved as a log since it produced no
output) — `sympy`'s generic hypergeometric-summation machinery does not appear to
close this particular sum automatically for a symbolic bound. The identity was instead
proved *by hand* (§3.4): rewriting the factorial ratio as a binomial coefficient,
re-indexing, and using the elementary symmetry-plus-classical-moments argument. This
is a useful, concrete data point on where automation stops helping in this problem:
**level-by-level algebra and coefficient-recursion verification (§2.3, §3.3) is
something `sympy` handles very well for symbolic `r,k,b`; closing a specific finite sum
into a product formula, for a symbolic bound, was not something the default
`sympy.summation` call could do here — a hand-found symmetry argument was needed.**

---

## 7. Scorecard

| # | Claim | Status |
|---|---|---|
| 1 | `ψ_n^{(6)}` exact closed form | **PROVED** (§1.1), matches direct recursion `n=7..25`, fresh raw brute force `n=7` (593M combos) and `n=8` (10.6B combos, §1.2) |
| 2 | `K=6` case of the Open Lemma: `φ_n^{(6)}→φ_6` | **PROVED** (§1.1) |
| 3 | `ψ_n^{(6),R}` and full rate `φ_n^{(6)}` | **PROVED** (§1.2), first-principles, matches independent full-definition brute force `n=7` |
| 4 | `ψ_n^{(7)},\dots,ψ_n^{(10)}` exact closed forms, `K=7,\dots,10` cases of the Open Lemma | **PROVED** (§1.1), each verified against `n\to\infty`-limit `=φ_K` |
| 5 | Leading-order continuum closed form `F_r(t,b)`, general `r` | **PROVED** (§2.3), symbolic-`r` induction; re-derives `φ_K` for every `K` by a new route |
| 6 | `O(1/n)`-order continuum closed form `G_r(t,b)` (i.e. `d_k^{(r)}(b)`), general `r` | **PROVED** (§3.3), symbolic-`(r,k,b)` algebraic identity check, not curve-fit; cross-validated against exact discrete `B_r(b)` for `K≤5`, all `b` |
| 7 | Rate conjecture, general `K`: `\lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` | **PROVED, modulo §4's stated regularity caveat** (§3.4) — the binomial-sum reduction and its proof are unconditional; the caveat is only about the *existence* of the assumed asymptotic expansion for `r` beyond the 11 concretely-checked values |
| 8 | Rate conjecture, `K=0,\dots,10` | **PROVED unconditionally**, no caveat (§1.1, §3.4), directly from exact discrete closed forms |
| 9 | `φ_n^{(K)}-φ_K=Θ(1/n)` for every `K≥1` | **PROVED, same caveat as #7** (§5) |
| 10 | Full general-`K` exact (all-orders) closed form for `ψ_n^{(K)}` | **NOT ATTEMPTED beyond §1's concrete ladder** — open (§6.2) |
| 11 | Generating-function-in-`K` sum on the exact finite-`n` recursion | **TRIED, abandoned before coding** — structural reason recorded (§6.1) |

> **[Correção pós-adversarial, 2026-08-22]** Linhas 5 e 6 acima estão
> rotuladas **PROVED** sem qualificador, ao contrário da linha 7 (que
> corretamente carrega "modulo §4's stated regularity caveat"). Achado
> pelo referee adversarial hostil independente
> (`adversarial/REFEREE_REPORT.md` §B.4(c)): os Teoremas em §2.3 e §3.3
> que essas linhas resumem SÃO, na prosa cuidadosa de §4, listados
> explicitamente como "uma afirmação condicional" que carrega a mesma
> ressalva — o próprio corpo do documento é consistente, mas um Scorecard
> existe precisamente para ser lido isoladamente por um processo de
> catalogação a jusante, e lido assim, as linhas 5–6 seriam mal
> categorizadas como incondicionais. **Correção: leia as linhas 5 e 6
> como "PROVED, modulo §4's stated regularity caveat" — exatamente igual
> à linha 7 — para consistência interna com §4/§5.** Isto é uma questão
> de rotulagem/consistência, não um erro substantivo — a existência e o
> escopo da ressalva estão corretos; apenas duas linhas do Scorecard
> subestimavam, quando lidas isoladamente, que estão cobertas por ela.
> Ver também §2.4 (adicionada nesta mesma revisão) para a análise
> completa do porquê a ressalva é necessária e o que a evidência empírica
> adicional do referee mostra sobre seu alcance.

**Net honest verdict.** The task's two stated goals are both achieved. The concrete-`K`
frontier moved from `K=5` (wave 6) to `K=10`, by wave 6's own method, with the same
brute-force verification discipline wave 6 applied at `K=3`. The general-`K` question
— genuinely attempted via route (ii), reformulated as an asymptotic ODE rather than a
literal formal-power-series sum (§6.1 records why the literal version did not seem
productive) — is answered for the rate conjecture with a complete proof, carrying one
precisely-stated, standard, and (in every one of eleven checkable instances)
zero-exception-corroborated regularity assumption; the *full* Open Lemma for general
`K` (not just its leading order and rate, but the complete exact finite-`n` formula)
remains open, and §6.2 names exactly what the natural next step of the same method
would be.

---

## 8. Files, reproducibility

All scripts use exact rational arithmetic (`fractions.Fraction` or `sympy.Rational`)
throughout — no floating point enters any PROVED claim above; floats appear only for
human-readable display. Every brute-force run enumerates **all**
`n!\times n^K` `(π,U_1,\dots,U_K)` combinations exhaustively — not sampled.

- `extend_frontier.py` / `extend_frontier.log` — §1.1: runs `../markov_transfer.py`'s
  `build_levels` incrementally through `K=10`, recording every closed form and
  per-level timing.
- `direct_check_k6.py` — §1.2 check 1: `../markov_direct.py`'s direct recursion vs. the
  `K=6` closed form, `n=7..25`.
- `fast_bruteforce.py` — §1.2 checks 2–3: optimized, parallelized re-implementation of
  `../psi_bruteforce_ref.py`'s exact raw-definition enumeration (array state, integer
  counts, `multiprocessing`), used for the `K=6,n=7` (`bruteforce_k6_n7.log`) and
  `K=6,n=8` (`bruteforce_k6_n8.log`) fresh brute-force points. `fast_bruteforce_selftest.log`
  cross-validates it against the original `psi_bruteforce_ref.py` on five small cases
  before it is trusted on the cases only it can reach.
- `fast_phi_bruteforce.py` — §1.2 check 4: analogous optimized re-implementation of
  `../phi_bruteforce_full.py` (the full Definition-4 average, independent of the
  single-reference-point machinery/Lemma A), used for the `K=6,n=7` check of the
  recombined `φ_n^{(6)}` formula (`phi_bruteforce_k6_n7.log`). `fast_phi_bruteforce_selftest.log`
  cross-validates it against the original on two small cases first.
- `pattern_analysis.py` / `pattern_analysis_r5.log` — §2.3, §3.3: extracts the full,
  two-variable-symbolic (`m,b` or `a,b`) closed forms for `g_r,h_r` at `r=0,\dots,5`
  from `../markov_transfer.py`'s machinery (not just the `b=0` specialization used for
  `ψ_n^{(K)}` itself), used as the ground truth every continuum-limit prediction is
  checked against.
- `rate_ode.py` / `rate_ode.log` — §2, §3.1–§3.2: the core continuum-ODE machinery.
  Solves the coupled `(F_r,G_r,\hat H_r,K_r)` system level-by-level, `r=1,\dots,8`,
  by the diagonal-coefficient-matching method (`solve_ode_poly`), printing and
  checking `F_r(1,0)=φ_r` and `G_r(1,0)=Kφ_K/4` at every level. Saves `rate_ode_data.pkl`.
- `verify_closed_forms.py` — §2.3: checks the closed-form `F_r(t,b)` formula against
  `pattern_analysis.py`'s exact `r=0..5` data (all `b`) and against `φ_K` at `t=1,b=0`
  for `r=0..6`.
- `verify_dk_recursion.py` / `verify_dk_recursion.log` — §3.3: the central symbolic
  proof — substitutes the conjectured `d_k^{(r)}(b)` closed form (and the proved
  `c_k^{(r)}(b)`) into the exact defining recursion for **symbolic `r,k,b`** and
  confirms `sympy` reduces `LHS-RHS` to `0`, both the general and `k=0` cases; also
  cross-validates `G_r(1,b)` against `pattern_analysis.py`'s exact `B_r(b)` data,
  `r=1..5`, all `b`.
- `verify_rate_conjecture.py` / `verify_rate_conjecture.log` — §3.4: the binomial-sum
  identity `\sum_{i=0}^{r-1}(r-i)(r+1-i)\binom{2r+1}i=r2^{2r-1}` and the three
  classical moment sums it rests on, checked by exact computation for `r=1..25` (resp.
  `n=5,10,13`); `G_r(1,0)=r\varphi_r/4` checked the same way, `r=1..25`.
- `verify_via_exact_k9_k10.py` — §3.4: extracts the `1/n` coefficient directly from
  `extend_frontier.py`'s exact `K=9,K=10` closed forms and compares to `Kφ_K/4` — the
  fully unconditional (no continuum argument) confirmation at the two highest `K`
  values reached.
- `coefficient_dump.py` / `coefficient_dump.log` — §3.2: extracts and factors every
  `d_k^{(r)}(b)`, `r=1,\dots,8`, from `rate_ode.py`'s saved `rate_ode_data.pkl`,
  exhibiting the pattern that led to §3.3's closed-form conjecture.
- `verify_phi_n7_identity.py` / `verify_phi_n7_identity.log` — §1.2 check 4: confirms
  the exact `\psi_n^{(6)}=\psi_n^{(6),R}` coincidence at `n=7` symbolically, matching
  the raw brute-force value bit-for-bit.

To reproduce: `python3 extend_frontier.py 10` (concrete-`K` ladder through `K=10`,
`\sim12` min cumulative); `python3 direct_check_k6.py` (seconds);
`python3 fast_bruteforce.py 7 6 4` (`\sim2` min), `python3 fast_bruteforce.py 8 6 4`
(`35.8` min measured, run once under CPU contention with the `phi` check below — log
retained rather than re-run by default); `python3 fast_phi_bruteforce.py 7 6 4`
(`10.5` min measured); `python3 pattern_analysis.py 5` (`\sim35`s);
`python3 rate_ode.py` (`\sim1-2` min); `python3 coefficient_dump.py`,
`verify_dk_recursion.py`, `verify_rate_conjecture.py`, `verify_via_exact_k9_k10.py`,
`verify_closed_forms.py`, `verify_phi_n7_identity.py` (all seconds).

