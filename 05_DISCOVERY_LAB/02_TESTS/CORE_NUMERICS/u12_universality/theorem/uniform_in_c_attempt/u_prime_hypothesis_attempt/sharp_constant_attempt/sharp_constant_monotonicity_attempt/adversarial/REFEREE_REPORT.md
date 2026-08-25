# Adversarial referee report — `sharp_constant_monotonicity_attempt/ATTEMPT.md`

> **Mandate.** Hostile, independent re-verification of the target's claimed
> full closure of the hardest named gap in this line (Estágio 13 of
> `THEOREM.md`): Theorem 2, `M_K < a*√K` for every `K≥1`, hence (with the
> parent's Theorem 6) `sup_K M_K/√K = a*` exactly. Third attempt at this
> exact gap, and the wave's only front resting on **two external literature
> citations** — so the citations were treated as the single highest-priority
> attack surface, per the mandate. Pure combinatorics/asymptotics; no
> physics claim, no Millennium Problem relevance anywhere.
>
> **Discipline.** None of this front's own scripts or logs
> (`verify_citations.py`, `verify_Q_upper_bound.py`, `verify_main_closure.py`,
> or their `.log` files) was opened at any point — everything below was
> rebuilt from the ATTEMPT.md prose alone. The parent documents
> (`u_prime_hypothesis_attempt/ATTEMPT.md`, `sharp_constant_attempt/ATTEMPT.md`)
> and their adversarial reports (both verdict SOUND/ACCEPT) were read as
> ordinary literature; their results (Theorem 3, Lemma 4.1, Theorem 5,
> Theorem 6) are treated as established inputs, quoted-accuracy-checked but
> not re-proved. **Both external citations were verified against the primary
> source**: the FGKP95 paper itself was retrieved (via the INRIA Algorithms
> Project archive, `FlGrKiPr95.pdf`) and its text extracted and read
> directly. Exact `fractions.Fraction`/integer arithmetic for every verdict
> labelled *certified* (including certified rational square-root brackets
> built from `isqrt` and the classical decimal digits of `π`, cross-checked
> against `mpmath` at 60 dps); `mpmath` (60–95 dps) only for margin displays
> and wide-range stress nets; `sympy` for symbolic identities. Reserved
> referee seed range `20260853000+` confirmed **unused** by grep
> (`DECISION_LEDGER.yaml`/`TEST_QUEUE.yaml` reservations only), and this
> review uses no randomness either — every object is deterministic. No file
> outside this `adversarial/` directory was created or modified; the only
> git command run was a read-only `git status`.

---

## 0. Executive summary

**Verdict: SOUND WITH NAMED ISSUES. ACCEPT for catalogue**, with two
mandatory errata (E-1, E-2) and two scope-accuracy notes (S-1, S-2), none of
which invalidates any theorem. **The mathematics of the main chain — Lemma
1's stated identity, Theorem 1, Theorem 2, and the Corollary
`sup_K M_K/√K = a*` — is correct.** I re-derived every step from scratch,
verified both citations against the true classical statements (FGKP95
against the actual paper), and re-verified everything numerically with
certified rational arithmetic at ranges meeting or exceeding the target's,
with **zero violations anywhere**. The gap named by Estágio 13 is genuinely
closed.

The named issues, in decreasing order of weight:

- **E-1 (erratum, mis-printed citation display).** Citation 1's displayed
  formula, `√(2πn)·e^{1/(12n+1)} < n! < √(2πn)·e^{1/(12n)}`, **omits the
  factor `(n/e)^n`** and is false as printed at every `n` (at `n=1`:
  `2.707 < 1` is false; for `n≥3` the printed "bounds" are astronomically
  below `n!`). The form actually *used* in Theorem 1's proof —
  `A(n) = n!e^n/n^n < √(2πn)·e^{1/(12n)}` — **is** the correct Robbins
  bound (verified here, 2,006 values of `n` to `10^8`, zero violations,
  both sides strict). The error is a transcription slip in the display,
  not a citation misuse: **no proof step relies on the false display.**
- **E-2 (erratum, broken printed intermediates in Lemma 1's proof).** Two
  displayed intermediate equations in Lemma 1's proof are **false**:
  `Q(n) = Σ_{k=1}^n n!/(k!·n^{n−k})` and the equivalent
  `Q(n) = (n!/n^n)(G(n)−1)`. Checked with exact Fractions: the printed
  value differs from `Q(n)` by exactly `1 − n!/n^n ≠ 0` for every `n≥2`
  (e.g. `Q(2)=3/2` but the printed sum gives `2`; `Q(3)=17/9` vs `8/3`).
  The `k := n−j` substitution shifted the summation index but not the
  summand (a per-term factor-`n/k` slip); the correct sum is
  `Q(n) = (n!/n^n)·Σ_{m=0}^{n−1} n^m/m!` — which is, verbatim, **eq. (1.4)
  of the cited FGKP95 paper itself**. The claimed cancellation ("the ±1 and
  ±n!/n^n terms cancel exactly") does not follow from the printed chain
  (it leaves the residue `1 − n!/n^n`); it does follow from the corrected
  chain. **The final identity `Q(n) = n!e^n/(2n^n) − θ(n)` is TRUE** —
  re-derived independently here (two-line derivation, §4), verified exactly
  in rational form (400/400) and to ≥50 digits in transcendental form. So
  the *result* stands; the *printed proof* does not, as written.
- **S-1 (novelty overstatement, minor).** Lemma 1 is presented as "a new
  elementary identity". It is classical — it is exactly FGKP95's own
  (1.4) combined with the identity `θ(n) = ½(R(n)−Q(n))`,
  `Q(n)+R(n) = n!e^n/n^n`, displayed in the cited paper's introduction
  (their `D(n) = 2θ(n)`). New to this archive, yes; new, no.
- **S-2 (scope mis-diagnosis in §6, in the safe direction).** §6's stated
  reason why the `K=n` boundary case does not immediately upgrade — "the
  index mismatch … reintroduces exactly the kind of **O(1)-losing**
  conversion step" — is quantitatively wrong: converting the `z`-bound
  exactly and using `1/√(1+x) ≥ 1−x/2` loses only `≤ (√π/4)/√n = O(1/√n)`.
  In fact the boundary case **closes with the sharp constant right now**
  using only tools already accepted by the archive (demonstrated in §8:
  a half-page argument for `n≥3`/`n≥67` plus certified exact checks for
  the finitely many small `n`). This is an under-claim, not an over-claim
  — the "open" §6 target is markedly more tractable than described.

Everything else held under attack: the FGKP95 Theorem 7 statement is
quoted **exactly right** (verified against the paper: statement, theorem
number, "for all integers n ≥ 0", `k(n) ∈ [2/21, 8/45]`, the proof's
`n ≥ 116`-plus-exhaustive-verification structure, the 16 January 1913
letter, the Knuth dedication, journal/volume/pages); every step of Theorem
1's chain is valid for every `n≥1` including the `n=1` equality edge; the
`√(π/2) − √π/2 = a*` identity, the `LHS(K)` monotonicity, and the
rational-arithmetic endgame are all correct (the document's own integers
were re-verified one by one, and the `LHS(1) < 1/3` step was additionally
re-proved with the referee's **own, different** integer-squaring bounds);
all three cited archive inputs are quoted accurately; and the exact
`Fraction` `M_K < a*√K` check was pushed, certified-rationally, to
`K = 10,000` (target: 3,000) with zero violations.

---

## 1. What I tried to break, and what happened

- **Citation 1 as printed** — checked the displayed inequality literally,
  exact `n!` vs `mpmath` bounds, `n=1..10`: **false at every `n`** (E-1).
  Then checked the form the proof actually uses (the correct Robbins
  statement) at 2,006 points to `n=10^8`: zero violations; smallest margins
  `6.9e-19` (lower) and `2.8e-27` (upper) at `n=10^8`, both positive. The
  proof survives; the display does not.
- **Citation 2 from every available angle** — (i) primary source: fetched
  and read FGKP95 itself; Theorem 7 says precisely what the target says it
  says, including the "for all integers n ≥ 0" clause the proof needs, and
  the paper's proof structure matches the target's bracketed description
  (effective bounds for `n ≥ 116` — the paper's own `n₀=n₂=116`, `n₁=24` —
  plus "calculate k(n) for n ≤ 115 by computer"). (ii) Internal
  consistency: `k(0)=8/45 ⟺ θ(0)=1/2` (exact, since `1/3 + 4/(135·8/45)
  = 1/2`) — confirmed to all digits; `k(∞)=2/21 ⟺` second-order
  coefficient `−4·(2/21)/135 = −8/2835` in `θ(n) ~ 1/3 + 4/(135n) −
  8/(2835n²)` — confirmed numerically (`(θ(n)−1/3−4/135n)·n² →
  −0.0028219 = −8/2835`), and the same expansion appears in FGKP95's own
  `D₁₀(n)` display (`D(n)=2θ(n)`: `2/3 + 8/135n − 16/2835n² − 32/8505n³…`).
  (iii) High-precision numerics: `θ(n)` computed **two independent ways**
  (its own defining sum with exact-rational partial sums; the
  incomplete-gamma/Poisson-CDF route — whose identity
  `θ(n) = ½·n!e^n/n^n − e^nΓ(n+1,n)/n^n + 1` I re-derived and confirmed),
  agreeing to `<10^{-74}` everywhere tested; the two-sided FGKP bound
  checked at 747 values, dense `n=0..600` + strided to `2000` + sparse to
  `10^6`: **zero violations**, `k(n)` always in `[2/21, 8/45]`, strictly
  decreasing, equality only at `n=0` (where the document's `≤` is exactly
  right). **The citation is correct and correctly used.**
- **Lemma 1, character by character** — every displayed equation of the
  printed proof checked separately at small `n` with exact arithmetic. Two
  of the five displays are false (E-2, table in §4); the other three,
  including the final identity, are true. The final identity was
  independently re-derived (§4) and verified exactly.
- **Theorem 1's chain** — every step re-derived, domains and strictness
  audited including `n=1` (where `12n−1 = 11n` holds with equality, as the
  document says); the two algebraic rewrites confirmed symbolically
  (`sympy`, exact zero). Certified-rational verification `Q(n) < RHS`
  (exact `Fraction` `Q(n)` vs a rational lower bound on the RHS, no float
  in any verdict): 809 points, dense `n=1..800` + sparse to `n=12,000` —
  **zero violations** (target's exact range: 600 dense/10,000 sparse).
  Margin at `n=1`: `0.0339185` (doc: `0.0339`); at `n=10^4`: `9.79066e-5`
  (doc: `0.0000979` — matches to the digit). Deep `mpmath` scan to
  `n=10^6`: margin decays exactly like the predicted `(1/132)√(π/(2n))`
  (the un-optimized `1/11` vs the classical `1/12`), always positive.
- **Theorem 2's assembly** — subtraction step audited for direction and
  strictness (upper bound minus lower bound, both strict: correct); the
  identity `√(π/2) − √π/2 = a*` and the closed form
  `LHS(1) = √π(17/11 − √2)` confirmed symbolically (exact zeros); `LHS(K)`
  monotonicity re-derived (sum of two strictly decreasing positive terms)
  and stress-checked (`K=1..2000` + sparse to `10^6`, zero violations,
  always `< 1/3`).
- **The rational endgame** — re-proved `LHS(1) < 1/3` with **my own**
  bounds (`√2 > 1.41421356` via `141421356² < 2·10^{16}`;
  `√π < 1.7724539` via `17724539²·10² > 31415926535897933`, using the
  classical digits of `π` cross-checked against `mpmath`), yielding
  `LHS(1) < 639701140399069/2750000000000000 ≈ 0.2326186 < 1/3` by pure
  integer comparison. Separately, the **document's own** chain was
  re-verified integer by integer: all six squaring claims, the reduction
  `(17725/10^4)(10^4/14142 − 1/2) = 2076661/5656800`, the certified fact
  that this really is `≥ a*`, the exact sum
  `= 48257687251/207416000000`, and `3·48257687251 < 207416000000` — all
  **true**, every substitution direction sound (lower bound on `√2` where
  an upper bound on `a*` is needed; upper bounds elsewhere).
- **The main claim at scale** — exact `Fraction`
  `M_K = Q(K+1) − (K+1)φ_K` vs a certified rational **lower** bound on
  `a*√K`: 1,010 points, dense `K=1..1000` + sparse to `K=10,000` — **zero
  violations**; `M_1 = 1/6` exactly (doc's `r_1=0.16667` confirmed);
  margin `0.200421` at `K=1` (doc: `0.2004`) rising toward `1/3`
  (consistent with `a*−r_K ~ 1/(3√K)`); `r_{10000} = 0.363772 < a*`.
  Plus the assembled elementary bound (T5c analog), certified rational,
  606 points to `K=10^5`, zero violations, worst gap `0.100715` at `K=1`
  (doc: `0.1007`); plus the T5e analog isolating the `z_K` citation from
  Theorem 1 (exact `Q(K+1)` + cited `z`-bound only), 407 points to
  `K=3000`, zero violations.
- **The cited archive inputs** — Theorem 3, Lemma 4.1 (+ the `z_K`
  rearrangement, which I re-derived: `(K+1)φ_K² > π/4` ⟹ multiply by
  `(K+1)`, take positive roots ⟹ `(K+1)φ_K > (√π/2)√(K+1)`), Theorem 6,
  the `a*` value, the two prior failed routes and the §3 quotation, and
  the Estágio 13 framing in `THEOREM.md` — all checked against the source
  documents directly: **quoted accurately** (one cosmetic conflation in
  §6's parenthetical about the parent's boundary case, N-1 below).
- **The §6 scope claims** — the generic-case upgrade really is immediate
  (parent's Theorem 2 gives `n|φ_n^{(K)}−φ_K| = T(n,K) ≤ T(K+1,K) = M_K`,
  then Theorem 2 here); the boundary-case difficulty description does not
  survive scrutiny (S-2, §8): I closed the boundary case myself with
  archive-accepted tools, so the "O(1)-losing conversion" diagnosis is
  disproved constructively.

I could not break any theorem. I could — and did — break two printed
displays (E-1, E-2), neither of which is load-bearing once corrected.

---

## 2. Citation 1 (Robbins 1955) — the finding, precisely

The true statement (Robbins, *Amer. Math. Monthly* **62** (1955) 26–29 —
reference details correct) is

`√(2πn)·(n/e)^n·e^{1/(12n+1)} < n! < √(2πn)·(n/e)^n·e^{1/(12n)}`, strict, every `n≥1`.

The target's Citation-1 display drops `(n/e)^n`. As printed it is false at
every `n` (demonstrated exactly in `referee_citations_lemma1.log`, section
R'). However, Theorem 1's proof never invokes the printed display: it
invokes `A(n) := n!e^n/n^n < √(2πn)e^{1/(12n)}`, which is precisely the
correct Robbins upper bound after multiplying through by `e^n/n^n`. The
correct statement was verified here at 2,006 points (`n=1..2000` dense,
sparse to `10^8` — beyond the target's `10^6`), zero violations, both
inequalities strict, with margins matching the classical
`d(n) − 1/(12n+1) ≈ 1/(144n²)`, `1/(12n) − d(n) ≈ 1/(360n³)` behavior. So:
**a real transcription error in the document's most prominent display, with
no mathematical consequence** — but it must be corrected, because a reader
checking "the citation as stated" (as this mandate does) finds a false
statement, and the target's own claim that the citation was "verified
numerically … zero violations" can only refer to the corrected form.

## 3. Citation 2 (FGKP95, Theorem 7) — verified against the paper itself

Retrieved `FlGrKiPr95.pdf` from the INRIA Algorithms Project archive and
read the text. Confirmed, against the target's quotation:

- **Theorem number and statement**: it is Theorem 7; "With the quantity
  θ(n) being defined by `½eⁿ = 1 + n/1! + n²/2! + … + θ(n)·nⁿ/n!`, one
  has, **for all integers n ≥ 0**, `θ = 1/3 + 4/(135(n+k))`, where
  `k = k(n)` lies between [2/21 and 8/45]." Identical in substance to the
  target's Citation 2, including the unconditional "for all n ≥ 0" that
  the target correctly emphasizes (the OCR mangles the two fractions in
  the theorem display itself, but they are unambiguous from the paper's
  (1.2), the Watson quotation, Fig. 2's caption "the first 120 values of
  k(n) … all lie inside the interval", and the proof's two displayed
  inequalities with `8/45` and `+2/21`).
- **The derived two-sided bound** the target uses
  (`1/3 + 4/(135(n+8/45)) ≤ θ(n) ≤ 1/3 + 4/(135(n+2/21))`) is the correct
  monotone rearrangement, with equality on the lower side exactly at
  `n=0` (`θ(0)=1/2`, `k(0)=8/45` — stated in the paper: "θ(0) = ½ …
  k(0) = 8/45"). The step Theorem 1 actually consumes, `θ(n) > 1/3`
  strictly, follows a fortiori.
- **Proof structure**: the paper fixes `K=10` in its saddle-point
  decomposition, obtains effective bounds valid for `n ≥ n₀ = 116`
  (`n₁ = 24`, `n₂ = 116`), and finishes by "calculat[ing] k(n) for
  n ≤ 115 by computer" — matching the target's bracketed description
  ("effective … error bounds for n≥116, plus exhaustive direct
  verification for n<116") exactly.
- **Provenance details**: J. Comput. Appl. Math. **58** (1995) 103–116;
  dedicated to D.E. Knuth; the strong assertion is from Ramanujan's first
  letter to Hardy "dated 16 January 1913" (paper, p. 104). All as the
  target states.
- **Definitional match**: the paper's (1.3) is
  `Q(n) = 1 + (n−1)/n + (n−1)(n−2)/n² + …` — term-by-term the archive's
  `Σ_j Π_{i=1}^j (1−i/n)`; anchor values `Q(2)=3/2`, `Q(3)=17/9`
  re-verified exactly.

Independent numerics (two methods, exact-rational partial sums and
incomplete-gamma, agreement `<10^{-74}`): the two-sided bound holds at all
747 tested `n` from 0 to `10^6`, `k(n)` decreasing from `8/45` (attained,
`n=0`) through `0.148098` (`n=1`) toward `2/21` (`k(10^6) − 2/21 =
7.256e-8`), and the second-order-coefficient consistency check converges
to `−8/2835`. **Citation 2 is correct, correctly stated, and correctly
used.** Residual risk: none identified — this is a primary-source
confirmation, not a memory-based one.

## 4. Lemma 1 — result true, printed proof broken

**Referee derivation (independent).** The `j`-th term of `Q(n)` is
`(n−1)(n−2)…(n−j)/n^j = (n−1)!/((n−1−j)!·n^j)`; substituting
`m := n−1−j` gives

`Q(n) = ((n−1)!/n^{n−1})·Σ_{m=0}^{n−1} n^m/m! = (n!/n^n)·S(n)`, `S(n) := Σ_{m=0}^{n−1} n^m/m!`

(the last equality because `n! = n·(n−1)!`, `n^n = n·n^{n−1}`). This is
FGKP95's own eq. (1.4). The θ-definition says exactly
`S(n) = e^n/2 − θ(n)·n^n/n!`; substituting,
`Q(n) = n!e^n/(2n^n) − θ(n)`. Done — no `G(n)`, no cancellation
bookkeeping needed. **The stated identity is true** (and classical: the
paper writes it as `θ(n) = ½(R(n)−Q(n))` with `Q+R = n!e^n/n^n` — S-1).

**The printed proof, display by display** (exact-`Fraction` audit,
`referee_citations_lemma1.log`, L3):

| displayed equation | verdict |
|---|---|
| `Π(1−i/n) = (n−1)(n−2)…(n−j)/n^j` | **correct** |
| `Q(n) = Σ_{k=1}^n n!/(k!·n^{n−k})` | **FALSE** for every `n≥2` (per-term factor `n/k` slip: the `k:=n−j` substitution shifted the index but not the summand; the true summand is `n!/((k−1)!·n^{n−k+1})`) |
| `= (n!/n^n)(G(n)−1)`, `G(n)=Σ_{k=0}^n n^k/k!` | **FALSE** for every `n≥2` (equivalent to the previous; should be `(n!/n^n)(G(n) − n^n/n!)`) |
| `G(n) = ½e^n + (1−θ(n))·n^n/n!` | **correct** |
| `Q(n) = n!e^n/(2n^n) − θ(n)` (final) | **correct** (verified exactly, 400/400 rational form; ≥50 digits transcendental form) |

Following the printed chain literally yields
`Q(n) = n!e^n/(2n^n) − θ(n) + (1 − n!/n^n)` — off by `1 − n!/n^n ≠ 0` for
`n≥2` (e.g. printed sum `= 2` vs `Q(2)=3/2`; `8/3` vs `Q(3)=17/9`; the
difference matches `1 − n!/n^n` exactly at every `n` tested, 12/12). The
parenthetical "the ±1 and ±n!/n^n terms cancel exactly" is therefore false
of the printed chain and true of the corrected one. **Load-bearing?** The
*result* is load-bearing and true; the *printed derivation* is broken but
correctable by a one-line fix (replace `G(n)−1` by `G(n) − n^n/n!`, i.e.
`Σ_{k=1}^n n^k/k!` by `Σ_{m=0}^{n−1} n^m/m!`). The target's own T3
verification (and mine) checks the final identity, which is why the
numerics passed while the printed algebra is wrong — exactly the failure
mode a referee is for. Classified as an erratum (E-2), not an
invalidation, because the corrected proof is immediate and the identity is
independently established (twice over: my derivation, and the cited
paper's own introduction).

## 5. Theorem 1 — confirmed, with certified rational arithmetic

Chain audit (details in `referee_theorem1.log`): Lemma 1 (as re-proved) +
Robbins upper bound (correct form, strict) + `θ(n) > 1/3` (strict, from
FGKP's lower bound, valid at every `n≥0`) gives
`Q(n) < √(πn/2)·e^{1/(12n)} − 1/3`. Then `e^x ≤ 1/(1−x)` on `[0,1)`
(equivalent to `1−x ≤ e^{−x}`; here `x = 1/(12n) ≤ 1/12`, safely inside
the domain), `12n/(12n−1) = 1 + 1/(12n−1)` (identity, sympy-zero),
`12n−1 ≥ 11n ⟺ n ≥ 1` with equality exactly at `n=1`, and
`√(πn/2)/(11n) = (1/11)√(π/(2n))` (identity, sympy-zero). Every step valid
for every `n≥1`; strictness carried by Robbins and `θ>1/3`. The `n=1` edge
holds with margin `0.0339185` (`Q(1)=1` vs certified rational lower bound
`1.033918…` of the RHS).

Certified-rational verification (no floating point in any verdict): 809
points, zero violations, to `n=12,000` exact. Deep scan to `n=10^6`
(mpmath, `Q(n)` summed from its own product definition with a certified
truncation tail `<10^{-44}`): margins positive everywhere and tracking
`(1/132)√(π/(2n))` — the document's "margin shrinks but is guaranteed
positive" narrative is exactly right, and its two reported margins
(`0.0339` at `n=1`, `0.0000979` at `n=10^4`) reproduce to all displayed
digits.

## 6. Theorem 2 and the Corollary — confirmed

Assembly audit (details in `referee_theorem2.log`): Theorem 3 (cited
equality) + Theorem 1 at `n=K+1` (strict upper) + Lemma 4.1's `z_K`-bound
(strict lower, rearrangement re-derived) ⟹
`M_K < a*√(K+1) − 1/3 + (1/11)√(π/(2(K+1)))` — the `√(π(K+1)/2) −
(√π/2)√(K+1) = a*√(K+1)` collapse confirmed symbolically, as is the
reduction of the remaining goal to `LHS(K) < 1/3` and the closed form
`LHS(1) = √π(17/11 − √2)`. Monotonicity of `LHS(K)`: re-derived (both
summands positive, strictly decreasing — the `1/(√(K+1)+√K)` rewrite is
correct) and scanned (`K` to `10^6`, zero violations).

The rational endgame was proved twice: once with the referee's own
integers (§1; final integer comparison
`3·639701140399069 < 2.75·10^{15}`, giving `LHS(1) < 0.2326186`), and once
by re-verifying the document's own chain integer-by-integer (all
verdicts true; its bound `0.2326614` is slightly looser than mine but
comfortably `< 1/3`; every substitution direction — lower bound on `√2`
inside `a*`, upper bounds elsewhere — is the correct, weakening one). True
value `LHS(1) = 0.2326186…`, so the safety margin to `1/3` is ≈ `0.1007`,
matching the document's T5c worst margin.

Main exact verification: `M_K < a*√K` **certified rationally** at 1,010
points, dense `K=1..1000` + sparse to `K=10,000` — three-plus times the
target's exact depth — zero violations, `M_1 = 1/6` exactly, margins
rising from `0.200421` (`K=1`) toward `1/3` exactly as the limit theory
predicts (`a*√K − M_K → 1/3` since `a* − r_K ~ 1/(3√K)`), with
`r_K < a*` always. The Corollary's logic (`sup ≤ a*` from Theorem 2;
`sup ≥ lim = a*` from cited Theorem 6; strictness at every finite `K` from
the strict steps) is airtight; the "approached but never attained" remark
is consistent with every numeric here and upstream.

## 7. The cited archive inputs — quoted accurately

Checked against the parent documents read directly:

- **Theorem 3** (`u_prime_hypothesis_attempt`, §5):
  `M_K := sup_{n≥K+1}|n(φ_n^{(K)}−φ_K)| = Q(K+1) − (K+1)φ_K` — quoted
  verbatim, used as an equality (correct).
- **Lemma 4.1** (same document, §6): `Kφ_K² < π/4 < (K+1)φ_K²`, strict for
  `K≥1` — quoted verbatim; the target's `z_K` rearrangement
  `(K+1)φ_K > (√π/2)√(K+1)` re-derived and confirmed as the parent's own
  Theorem 4 usage.
- **Theorem 6** (`sharp_constant_attempt`, §2): `lim_{K→∞} M_K/√K = a*` —
  quoted verbatim; its adversarial report (SOUND/ACCEPT) covers it.
- **The §3 quotation** in the target's governance block (the prior
  route-(b) diagnosis) is a fair ellipsized quotation of
  `sharp_constant_attempt` §3/§4, and the recursion counterexample
  `Q(3) = 17/9 ≠ 1 + (2/3)Q(2) = 2` re-verified exactly.
- **Estágio 13** of `THEOREM.md` names exactly this gap
  (`sup_K M_K/√K = a*`, equivalent to fact (ii)/monotonicity), as the
  target's framing claims; the ledger reserves seeds
  `20260852000+`/referee `20260853000+` for this front, matching the
  target's Seeds section (and neither range is used — no randomness
  exists in either document or in this review).
- The target's §5 correction of the prior diagnosis ("only the `Q(n)`
  side needed sharpening") is accurate: my T5e-analog run (§1) confirms
  the unmodified `z_K`-bound suffices at every tested `K`, and the
  `LHS(K)` analysis shows why (the `z`-route loses only `O(1/√K)` against
  the available `1/3` slack).

## 8. The §6 scope claims — one confirmed, one disproved constructively

**Generic case: confirmed immediate.** Parent's Theorem 2 gives
`T(n,K) ≥ 0` nonincreasing in `n`, so
`n|φ_n^{(K)}−φ_K| = T(n,K) ≤ T(K+1,K) = M_K < a*√K` for every `n ≥ K+1`,
`K ≥ 1` — the claimed upgrade `|φ_n^{(K)}−φ_K| < a*√K/n` follows with no
additional work, exactly as stated (Scorecard #9 is accurate).

**Boundary case `K=n`: the difficulty is misdescribed (S-2).** The
target's stated obstruction — the `(n+1)φ_n`-vs-`nφ_n` index mismatch
"reintroduc[ing] exactly the kind of O(1)-losing conversion step" — is
quantitatively wrong. Demonstration (`referee_boundary_case_probe.log`,
all finite checks certified rational):

- The exact conversion `nφ_n = (n+1)φ_n · n/(n+1) > (√π/2)·n/√(n+1)`
  combined with the elementary `1/√(1+x) ≥ 1−x/2` (proved:
  `(1−x/2)²(1+x) − 1 = x²(x−3)/4 ≤ 0` on `[0,3]`) gives
  `nφ_n > (√π/2)(√n − 1/(2√n))` — a loss of at most `(√π/4)/√n =
  O(1/√n)`, not `O(1)`. (The parent's `n/√(n+1) ≥ √n−1` was `O(1)`-lossy,
  but nothing forces that choice.)
- **Upper side, `n ≥ 3`:** with Theorem 1,
  `Q(n) − nφ_n < a*√n − 1/3 + c/√n`, `c := (1/11)√(π/2) + √π/4`; certified
  `3c² < 1`, so `c/√n ≤ c/√3 < 1/3` for every `n ≥ 3`.
- **Lower side, `n ≥ 67`:** with the `v`-bound and the archive's accepted
  Theorem 5 (`Q(n) ≥ √(πn/2) − 6`),
  `nφ_n − Q(n) < 6 − a*√n ≤ a*√n` once `a*√n ≥ 3`; certified
  `a*_lo·√67_lo = 3.0047 > 3`.
- **Finite remainder:** `|Q(n) − nφ_n| < a*√n` verified exactly
  (certified rational) for all `n = 1..80` — zero violations
  (`n=1`: `1/3 < a*`; `n=2`: `13/30 < a*√2`).

Together with the generic case and the trivial `K=0`, this closes the
**full** sharp-constant upgrade of (U') — `|φ_n^{(K)}−φ_K| ≤ a*√K/n` for
all `0 ≤ K ≤ n` — using only results the archive has already accepted
plus a half-page of elementary work. To be precise about what this means
for the target document: its §6 is *honest* (it claims only non-attempt,
and the official (U') constant indeed remains `1+√(π/2)` until the
boundary case is separately catalogued), and the error is in the safe,
under-claiming direction; but the catalogue entry for "what remains open"
should record that the named next target is essentially already within
reach — indeed closed above, subject to this report's own adversarial
standing — rather than "likely tractable". Scorecard #10's "NOT attempted,
named precisely" is accurate as to fact, inaccurate as to the diagnosis
that accompanies it.

## 9. Findings

| id | severity | finding |
|---|---|---|
| E-1 | erratum (must fix; no mathematical consequence) | Citation 1's display omits `(n/e)^n` and is false as printed at every `n`; the form used in Theorem 1's proof is the correct Robbins bound. §2 above. |
| E-2 | erratum (must fix; result unaffected, printed proof invalid as written) | Two of Lemma 1's displayed intermediates are false (`Σ_{k=1}^n n!/(k!n^{n−k})` and `(n!/n^n)(G(n)−1)`; off by exactly `1 − n!/n^n`); the final identity is true and independently re-proved. §4 above. |
| S-1 | minor (novelty framing) | Lemma 1 is classical — FGKP95's own (1.4) + `θ = ½(R−Q)`; "new elementary identity" overstates novelty (it is new only to this archive). |
| S-2 | minor-to-moderate (scope accuracy, safe direction) | §6's "O(1)-losing conversion" diagnosis of the `K=n` boundary case is quantitatively wrong (`O(1/√n)` actual); the boundary case closes with the sharp constant using already-accepted archive tools (demonstrated, §8). Affects cataloguing of the named next target, not any theorem in this document. |
| N-1 | nit | §6's parenthetical describing the parent's boundary case pairs the conversion inequality `n/√(n+1) ≥ √n−1` with "its `v_n`-bound"; in the parent's Theorem 4 that inequality accompanies the `z_n`-bound (upper side), while the `v_n`-bound serves the lower side. Cosmetic conflation. |

**No error was found in the statements or validity of Lemma 1 (as a
result), Theorem 1, Theorem 2, or the Corollary; no citation is misused;
every numerical claim checked reproduces.**

---

## 10. Scorecard

| # | Target claim | Target status | **Referee verdict, independent scale** |
|---|---|---|---|
| 1 | Lemma 1 identity | PROVED | **Statement CONFIRMED** (exact 400/400 + ≥50-digit transcendental + primary-source classical); **printed proof REFUTED as written** (E-2), corrected chain supplied |
| 2 | Citation 1 (Robbins) correctly stated and applicable | PROVED | **Applicable-as-used CONFIRMED** (2,006 points to `n=10^8`, strict, zero violations); **displayed statement FALSE as printed** (E-1) |
| 3 | Citation 2 (FGKP95 Thm 7) correctly stated and applicable | PROVED | **CONFIRMED against the primary source** (paper fetched and read; statement, numbering, `n≥0` clause, proof structure all match) + two independent numeric routes, 747 `n` to `10^6`, zero violations, endpoints `k(0)=8/45` (equality) and `k(∞)=2/21` (coefficient `−8/2835`) both confirmed |
| 4 | Theorem 1 | PROVED | **CONFIRMED** — chain re-derived incl. `n=1` edge; certified-rational, 809 points to `n=12,000`; mpmath to `10^6`; doc's margins reproduced to displayed digits |
| 5 | Theorem 2 (main) | PROVED | **CONFIRMED** — assembly symbolic-zero-checked; rational endgame proved with referee's own integers AND the doc's integers re-verified; certified exact `M_K` check, 1,010 points to `K=10,000` (doc: 3,000), zero violations |
| 6 | Corollary `sup_K M_K/√K = a*` | PROVED | **CONFIRMED** (logic + strictness audit; `r_K < a*` at every tested `K`) |
| 7–8 | Prior routes refuted/superseded | recorded | **CONFIRMED** (recursion counterexample re-verified; supersession framing accurate) |
| 9 | (U') generic case upgraded to `a*` | PROVED | **CONFIRMED immediate** from parent's Theorem 2 + this Theorem 2 |
| 10 | (U') boundary case: not attempted, named as next target | NOT attempted | **Non-attempt accurately reported; accompanying difficulty diagnosis REFUTED** (S-2) — referee closed the boundary case with archive-accepted tools (§8) |
| 11 | Official (U') constant unchanged | unchanged | **CONFIRMED** (and correctly so, pending separate cataloguing of the boundary case) |
| 12 | `sup=lim` vs literal monotonicity distinction | stated | **CONFIRMED accurate** (the document proves `sup=lim` only, and says so) |

---

## 11. Final verdict

**SOUND WITH NAMED ISSUES. ACCEPT for catalogue**, with errata E-1 and E-2
required (a corrected Robbins display; a corrected pair of intermediates
in Lemma 1's proof — both one-line fixes whose corrected forms are given
in this report), and notes S-1/S-2/N-1 recorded. The headline result —
`M_K < a*√K` for every `K ≥ 1`, hence `sup_K M_K/√K = a*` exactly, the gap
named by Estágio 13 — **is correct and is genuinely closed**: every
inequality in the chain was re-derived independently, both external
citations were verified (one against the primary source retrieved during
this review), and every claim was re-checked with certified rational
arithmetic at or beyond the target's own scale with zero violations. The
two errata are textual defects in precisely the places this review was
directed to attack hardest — a mis-transcribed citation display and a
broken printed derivation — and it is fair to record plainly that the
document's own printed proof of Lemma 1 is not a proof as written; but the
underlying statements are true, classical, and doubly re-established here,
so they do not reduce the mathematical standing of Theorems 1–2 or the
Corollary. The §6 assessment of what remains open should be revised when
catalogued: the `K=n` boundary case of the sharp-constant upgrade of (U')
is not merely "likely tractable" — it follows now, by the short argument
in §8 of this report, from results the archive has already accepted.

---

## 12. Files in this directory

| file | what it does |
|---|---|
| `referee_citations_lemma1.py` / `.log` | Part 1 — Robbins correct-form verification (2,006 points to `n=10^8`) and printed-display refutation; FGKP95 Theorem 7 two-method θ verification (747 points to `10^6`), `k(n)` interval/monotonicity/endpoints, `−8/2835` coefficient consistency; Lemma 1 exact re-derivation (400/400), ≥50-digit transcendental check, and the exact-Fraction refutation table for the printed intermediates |
| `referee_theorem1.py` / `.log` | Part 2 — Theorem 1 chain audit (domains, strictness, `n=1` edge, sympy identities) + certified-rational verification (809 points to `n=12,000`, no float in verdicts) + deep margin scan to `n=10^6` |
| `referee_theorem2.py` / `.log` | Part 3 — Theorem 2 assembly (symbolic zeros), `LHS(K)` monotonicity, referee's own rational proof of `LHS(1)<1/3`, the document's rational chain re-verified integer-by-integer, certified elementary-bound check (606 points to `K=10^5`), certified exact `M_K<a*√K` (1,010 points to `K=10,000`), T5e-analog isolation check (407 points) |
| `referee_boundary_case_probe.py` / `.log` | Part 4 — §6 scope audit: the `O(1/√n)` conversion-loss demonstration, and the referee's closure of the `K=n` boundary case (`n≥3` / `n≥67` arguments certified; `n=1..80` exact certified checks) |
| `REFEREE_REPORT.md` | this report |

Reproduce in order: `python3 referee_citations_lemma1.py`;
`referee_theorem1.py`; `referee_theorem2.py`;
`referee_boundary_case_probe.py`. All scripts are self-contained
(stdlib `fractions`/`math` + `sympy` + `mpmath`), deterministic (no
randomness, reserved seed range untouched), and were written without
reading any `.py` or `.log` file from the target front's directory. Total
runtime ≈ 8 s.
