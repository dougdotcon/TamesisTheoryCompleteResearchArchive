# REFEREE_REPORT — hostile adversarial verification of `k_general_existence_attempt/ATTEMPT.md`

> **Target under review:**
> `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/ATTEMPT.md`
>
> **Claim under review:** that the two-term asymptotic expansion
> `g_r(m,b) = F_r(t,b) + (1/n)G_r(t,b) + O(1/n²)` (`t=m/n`) **exists for every `r`**,
> with an error bound uniform in `m` — including at the recursion's base-case
> boundary — proved by induction on `r` whose inductive step is a discrete-Gronwall
> bound on the exact discrete recursion. If true, this closes the single named
> caveat of `../ATTEMPT.md` §4 and makes the general-`K` rate conjecture and the
> general-`K` Open Lemma bridge unconditional.
>
> **Reading order followed, in full, before forming any opinion:** `../ATTEMPT.md`
> (the parent, §§0–10 including §2.4 and every post-adversarial correction block);
> `../adversarial/REFEREE_REPORT.md` (the prior referee, especially §B.4); then the
> target. Additionally consulted for the *already-established* facts this document is
> permitted to reuse: `../../ATTEMPT.md` §2 (the transition-rule Proposition) and §3
> (the `r=0` closed forms and telescoping algorithm); `THEOREM.md` §7.4 / Estágio 5.
>
> **Discipline followed.** Every one of Part A's six items was worked out by me from
> the transition rules and the stated closed forms, *by hand and in fresh code*,
> **before** reading how the target does it. Not one line of `common.py`,
> `probe_boundary.py`, `probe_uniform.py`, `probe_h_uniform.py`,
> `verify_gronwall_pieces.py`, `markov_direct.py` or `markov_transfer.py` was
> imported, copied or adapted. My simulator is a separately-written memoized
> exact-`Fraction` chain keyed on `(a,b,r)` with its own domain assertions; my closed
> forms are separately transcribed from the stated formulas; my `Δ_r` is extracted by
> my own symbolic substitution. The target's own scripts and logs were read **only
> after** all of my results were in, and are used below solely to check the
> document's *descriptions of its evidence* against its artifacts.

---

## VERDICT (read this first)

# **SOUND — WITH NAMED ISSUES.**

The **Target Theorem is genuinely established.** I attacked every step and could not
break any of them. Specifically:

- The exact residual recursion of §3 is **correct**. I re-derived it independently
  and then verified it as an *exact rational identity* at **477 concrete
  `(r,b,n,m)` points, 0 mismatches**, including at the base case `m=b+r+1` at every
  one of them.
- The base-case mechanism §3 leans on — that `(*)`'s coefficient on the
  out-of-domain `g_r(b+r,b)` is *exactly* `0` at `m=b+r+1` — is a **real, checkable
  algebraic fact about the already-proven wave-6 recursion**, not a new assumption.
  It follows from `m-(1+r+b) = m-1-r-b`, which is `0` at `m=b+r+1`.
- The Taylor device is exact, the coefficient-sum lemma is correctly stated and
  correctly applied (every argument really is in `[0,1]`), the falling-factorial and
  hockey-stick identities are correct, and the "no spurious `log n`" claim is
  **not** overstated — I constructed the crude bound myself and it really does grow
  like `H_n ~ log n`.
- The `h_r` step really is pure substitution with no hidden recursive dependency,
  and I verified its identity exactly at **309 concrete points, 0 mismatches**.
- The induction closes with no circularity: level `r` needs only level `r-1` at `b`
  and `b+1`, and level `0` is exactly zero.
- My **own fresh numerics**, at `(r,b,n,m)` combinations the target never touched
  (`r=6,7,9,10`; `b=2,3,5`; `n` to `10⁶`; exhaustive rather than log-sampled
  `m`-scans), show `n²·R_r` **converging to finite constants everywhere**, with no
  `log n` growth, no boundary blow-up, and **zero violations** of the bound
  `D_r(b)/n²` computed from the document's own constant recursion.

Four issues are named below. **None of them is fatal, and none changes the verdict**,
but two of them must be acted on before cataloguing:

| # | Issue | Severity |
|---|---|---|
| **I-1** | §4's displayed exponent is wrong: it writes `Δ_r = Σ_{j≥2} h^{j-1}p_j` and justifies the key bound with "`h^{j-1} ≤ h²` for `j≥2`", which is **false** (`h ≤ h²` fails for `h<1`). The true fact — which I verified independently, symbolically, for `r=0,…,8` at symbolic `b` — is `Δ_r = Σ_{k=2}^{r} h^k q_k(t,b)`, so the bound `|Δ_r| ≤ A_r(b)h²` **does** hold. §3 states the correct fact ("order `h²` and higher"). | **Load-bearing typo.** The mathematics is right; the written justification of the single most load-bearing bound is not. **Must be corrected.** |
| **I-2** | §6's identity references `R_r(n-a, b+1, n)` at `a = n-b-r-1`, where `n-a = b+r+1` is **outside** `g_r(·,b+1)`'s domain (which needs `m ≥ b+r+2`), so §5's theorem does not cover it. The coefficient multiplying it is **exactly 0** there — the same mechanism §3 uses and explains for `g_r` — so the identity and bound survive intact. §6 never mentions this. | Minor write-up gap; one sentence fixes it. |
| **I-3** | Several of §7's / the Executive Summary's descriptions of the numerical evidence do not match the retained logs (specific `n`-lists absent from `probe_boundary.log`; "the **entire** range of `m` (log-spaced sample …)" is self-contradictory and the script really does sample ~25 points; "`r=1,2,3` at `b=0,1`" when only `r=2` was run at `b=1`; "`r=1,…,5`, `n` up to `1600`, both `g_r` and `h_r`" conflates narrower runs). | Cosmetic overstatement of the evidence surface. I re-ran the exhaustive versions myself; the claims are true, the descriptions are loose. |
| **I-4** | **Downstream, and the one that matters for cataloguing.** The target's §9 says its Theorem "removes the **last named caveat** from `../ATTEMPT.md`'s general-`K` rate-conjecture proof **and from the general-`K` Open Lemma bridge**". That is right for those two. But `../ATTEMPT.md` §5 / Scorecard row 9 also carried the *same* caveat on the claim "`φ_n^{(K)} − φ_K = Θ(1/n)` for every `K ≥ 1`" — **and that claim is FALSE at `K=1`**: `φ_n^{(1)} − φ_1 = 1/(3n²)` exactly. Promoting that row verbatim would turn a false statement from conditional into unconditional. | **Not the target's error** (it is pre-existing in the parent, and the prior referee supplied the counterexample without joining the dots) — but it becomes *more* consequential now. **Must be handled at integration.** |

**Bottom line for the archive:** the general-`K` rate conjecture
`lim n(ψ_n^{(K)} − φ_K) = Kφ_K/4` and the **general-`K` Open Lemma**
`lim φ_n^{(K)} = φ_K` should now be catalogued as **unconditional PROVED, for every
`K`**, once I-1 is corrected. The `Θ(1/n)` claim for `φ_n^{(K)}` must be
re-scoped to `K ≥ 2` (with `K=1` an exact `Θ(1/n²)` exception), and can in fact be
**upgraded** to an exact coefficient for every `K` (§A.7 below).

---

# PART A — the six items, worked out independently

## A.1 The exact residual recursion (§3)

### A.1.0 My own derivation (done before reading §3's)

From `../../ATTEMPT.md` §2's Proposition, in `(m,b)` coordinates (`m = n-a`):

```
g_r(m,b) = 1/m + (r/m) h_{r-1}(n-m+1,b) + ((m-1-r-b)/m) g_r(m-1,b)
h_r(a,b) = 1/n + (r/n) h_{r-1}(a,b+1) + ((n-1-a-b-r)/n) g_r(n-a,b+1)
```

Multiplying the first by `m` and using `m - (1+r+b) = m-1-r-b`:

```
(*)  m[g_r(m,b) - g_r(m-1,b)] + (1+r+b) g_r(m-1,b)
   = m g_r(m,b) - (m-1-r-b) g_r(m-1,b) = 1 + r h_{r-1}(n-m+1,b)
```

— an exact identity, no approximation. Then with `h := 1/n`, `t := m/n`, `m = t/h`,
`A(x) := F_r(x,b) + h G_r(x,b)`, and `s := (1-t)+h`, substitute
`g_r(m,b) = A(t) + R_r(m)`, `g_r(m-1,b) = A(t-h) + R_r(m-1)`,
`h_{r-1}(n-m+1,b) = Ĥ_{r-1}(s,b) + h K_{r-1}(s,b) + ε^h_{r-1}(n-m+1)`. Collecting:

- **`h⁰`:** `t F_r' + (1+r+b) F_r − 1 − r Ĥ_{r-1}(1-t,b)` — vanishes by **Fact 2**.
- **`h¹`:** `t G_r' − ½ t F_r'' + (1+r+b)(G_r − F_r') − r Ĥ'_{r-1}(1-t,b) − r K_{r-1}(1-t,b)`
  — vanishes by **Fact 3** rearranged.
- **`h^{≥2}`:** everything else `=: Δ_r(t,b,h)`.

giving `0 = Δ_r + m R_r(m) − (m-1-r-b) R_r(m-1) − r ε^h_{r-1}`, i.e.

```
R_r(m,b,n) = ((m-1-r-b)/m) R_r(m-1,b,n) + (1/m)[ r ε^h_{r-1}(n-m+1,b,n) − Δ_r(t,b,h) ]
```

**This is exactly what §3 states, sign for sign.** (Note: `PROGRESS.log`'s
intermediate entry at `19:35Z` records this with a `+Δ_r`; the final ATTEMPT.md has
the correct `−Δ_r`, and my 477 exact identity checks confirm the minus sign.)

### A.1(a) Is the polynomial Taylor expansion *exactly* remainder-free?

**CONFIRMED, and it is not a `O(h^{r+1})` estimate — it is an identity.**
`adv_residual_derivation.py` §(a) takes random rational polynomials of degree
`d = 0,…,8` and computes `p(x-h) − Σ_{j=0}^{d} ((-h)^j/j!) p^{(j)}(x)` symbolically:

```
deg=0..8: remainder with d+1 terms = 0   (with only d terms: nonzero, as expected)
```

Nine degrees, remainder exactly `0` every time; truncating one term earlier leaves a
nonzero remainder, so `d+1` terms is exactly the right count, not an over-count. This
is the structural fact the whole argument rests on and it holds.

### A.1(b) Do the `h⁰` and `h¹` brackets vanish *identically in `t`*?

**CONFIRMED, for symbolic `b`, `r = 0,…,8`.** I built
`(t/h)[A(t)−A(t-h)] + (1+r+b)A(t-h) − 1 − r[Ĥ_{r-1}(1-t+h) + h K_{r-1}(1-t+h)]`
and read off its Laurent coefficients in `h`:

```
r=0: h^(-1): none | h^0 coeff = 0 | h^1 coeff = 0 | h^k (k>=2) present for k in []
r=1: h^(-1): none | h^0 coeff = 0 | h^1 coeff = 0 | h^k (k>=2) present for k in []
r=2: h^(-1): none | h^0 coeff = 0 | h^1 coeff = 0 | h^k (k>=2) present for k in [2]
r=3: ...                                             ... k in [2, 3]
r=4: ...                                             ... k in [2, 3, 4]
r=5: ...                                             ... k in [2, 3, 4, 5]
r=6: ...                                             ... k in [2, 3, 4, 5, 6]
r=7: ...                                             ... k in [2, 3, 4, 5, 6, 7]
r=8: ...                                             ... k in [2, 3, 4, 5, 6, 7, 8]
```

Three things follow, all of them the target's claims and all confirmed:
(i) there is no surviving `h^{-1}` term (the `m = t/h` factor is harmless);
(ii) the `h⁰` and `h¹` brackets are identically `0` **as polynomials in `t`**, hence
at every real `t` including `t = (b+r+1)/n → 0` — so **no separate boundary-layer
treatment is needed**, exactly as §3 argues;
(iii) `Δ_r = Σ_{k=2}^{r} h^k q_k(t,b)` — **`r-1` terms**, starting at `h²`.

I also checked Facts 2 and 3 in the form the parent states them, directly:

```
r=0..8 (symbolic b):  Fact2 LHS-RHS = 0   |   Fact3 LHS-RHS = 0
r=0..12 (b = 0,1,3,7): Fact1 (degrees) all-true | Fact2 all-zero | Fact3 all-zero
```

and — going beyond what the target and the parent do — I extracted the
**coefficient-of-`t^k` form of Fact 3 from the ODE myself** (using
`Ĥ_{r-1}(1-t,b) = t F_{r-1}(t,b+1)` and
`K_{r-1}(1-t,b) = 1 + (r-1)tF_{r-2}(t,b+2) + tG_{r-1}(t,b+1) − (b+r)F_{r-1}(t,b+1)`)
and verified it for **fully symbolic `r,k,b`** using gamma-function closed forms
(`adv_symbolic_r.py`):

```
FACT 2, symbolic r,k,b:  k>=1 case LHS-RHS = 0 ;  k=0 case = 0
FACT 3, symbolic r,k,b:  general k>=1 case LHS-RHS = 0 ;  k=0 boundary case = 0
numeric cross-check: 1200 (r,k,b) triples; Fact2 mismatches=0  Fact3 mismatches=0
```

So Facts 2–3 hold for **general `r`**, not merely the `r` I could expand concretely.
This matters: it is precisely what makes the target's argument a general-`r` proof
rather than a family of case checks.

### A.1(c) Is the contraction coefficient really `(m-1-r-b)/m`, i.e. `g_r`'s own?

**CONFIRMED, trivially and exactly.** The residual terms are
`m[R(m)-R(m-1)] + (1+r+b)R(m-1) = m R(m) − (m−(1+r+b))R(m-1)`
and `m−(1+r+b) = m-1-r-b`. Dividing by `m` gives `(m-1-r-b)/m`, which is verbatim
the "continue at the same `r`" coefficient of the original wave-6 non-source rule.
The residual therefore inherits `g_r`'s own linear operator — which is exactly why
the *same* falling-factorial telescoping that wave 6 used to *solve* the recursion
can be reused here to *bound* it. That structural observation is correct and is the
argument's best idea.

### A.1(d) Is the zero coefficient at `m=b+r+1` a real fact about the *already-proven* recursion?

**CONFIRMED — it is an algebraic fact about wave-6's own rule, not a smuggled
assumption.** In the original (not rearranged) form the coefficient of
`g_r(m-1,b)` is literally `(m-1-r-b)/m`, and at `m = b+r+1` that is
`0/(b+r+1) = 0`. In the rearranged `(*)`, `g_r(m-1,b)` appears twice, with
coefficients `−m` and `+(1+r+b)`, whose sum is `−(m-1-r-b) = 0` at `m=b+r+1`.
Wave 6's `../../ATTEMPT.md` §2 "Base cases" paragraph already records the same
observation ("the value 'just before' the state where the coefficient
`(m-1-r-b)/m` vanishes — this is not an extra assumption").

I then checked the consequence the target actually needs, namely that at `m=b+r+1`
the residual recursion reduces to `R_r(j) = β(j)` with **no reference at all** to the
undefined `R_r(j-1)`. Because the ansatz `A(x)` is a polynomial defined at every real
`x`, the identity `mA(t) − (m-1-r-b)A(t-h) − 1 − r[Ĥ_{r-1}(s)+hK_{r-1}(s)] = Δ_r`
holds at `t = j/n` too, and there the second term is `0·A(t-h) = 0`. So
`j·A(t₀) + j R(j) − 1 − r[…] − rε^h_{r-1} = 0`, i.e. `R(j) = (1/j)[rε^h_{r-1} − Δ_r(t₀)]`.
**Verified numerically at the base case in every one of the 477 checks below.**

### A.1(e) The decisive check: the residual recursion as an exact rational identity

`adv_endtoend.py` STEP 2 computes `R_r(m,b,n)` from my own chain and my own closed
forms, computes `Δ_r` from my own symbolic substitution, and checks the recursion
holds **exactly** (Fractions, no floats), for every valid `m` from `b+r+1` to `n`:

```
r=1 b=0 (n=9,13,20,27) ... r=6 b=0 (n=9,13,20,27), also (2,3),(3,2),(4,1)
TOTAL: 477 exact identity checks, 0 mismatches
```

**§3 is correct.**

---

## A.2 The Taylor-tail bound (§4)

### The lemma itself

**Correct, and correctly hypothesised.** `|p(x)| ≤ Σ|a_k|` on `x∈[0,1]`: 12 000
random exact-rational samples, **0 violations**; and the hypothesis really is needed
— `p(x)=1+x` has `‖p‖=2` but `p(1.5)=2.5`. The derivative version
`|p^{(j)}(x)| ≤ d!‖p‖` on `[0,1]`: **0 violations** over 300 random polynomials × all
`j ≤ d` × 12 sample points.

### Is it applied only where `x∈[0,1]`? (the task's specific question)

**Yes, everywhere.** I enumerated the arguments:

| argument | range | in `[0,1]`? |
|---|---|---|
| `t = m/n`, `b+r+1 ≤ m ≤ n` | `(0,1]` | yes |
| `1-t` (the Taylor **centre** of `Ĥ_{r-1}`, `K_{r-1}`) | `[0,1)` | yes |
| `s = a/n`, `0 ≤ a ≤ n-b-r-1` | `[0,1)` | yes |
| `1-s = (n-a)/n` | `(0,1]` | yes |

On the task's specific worry about `s = 1-t+h`: `s = (n-m+1)/n ≤ 1` iff `m ≥ 1`, and
`m ≥ b+r+1 ≥ 1`, so `s ∈ (0,1]` — it never exceeds `1` and never goes negative.
Moreover it is *not* where the bound is applied: the tail polynomials in `Δ_r` are
the Taylor coefficients **at the centre `1-t`**, so the lemma is only ever used at
`1-t ∈ [0,1)`. **No misapplication.**

### **ISSUE I-1 — the exponent in §4 is wrong as written**

§4 writes

> `Δ_r(t,b,h) = Σ_{j≥2} h^{j-1}·p_j(t,b)` … `|Δ_r| ≤ Σ_{j=2}^{r} h^{j-1}‖p_j‖ ≤ h²(Σ_{j=2}^r ‖p_j‖) =: A_r(b)h²`
> (used `h^{j-1} ≤ h²` for `j≥2`, `h∈(0,1]`, true once `n≥1`)

`h^{j-1} ≤ h²` for `j ≥ 2` is **false at `j = 2`**: it reads `h ≤ h²`, which for
`h = 1/n ∈ (0,1)` is backwards. Taken literally, §4's argument yields only
`|Δ_r| ≤ A_r(b)·h`, which would degrade the final theorem from `O(1/n²)` to
`O(1/n)` — i.e. it would *not* establish the two-term expansion at all, only the
leading order. So this is not a harmless slip in a decorative sentence; it is in the
written justification of the single most load-bearing inequality in the document.

**But the underlying fact is true**, and I verified it independently (A.1(b) above):
the actual expansion is `Δ_r = Σ_{k=2}^{r} h^k q_k(t,b)`, from which
`|Δ_r| ≤ h²Σ_{k=2}^r‖q_k‖ =: A_r(b)h²` follows immediately. The index count in §4
("`≤ r-1` explicit polynomials", "`j = 2,…,r`") already matches the *correct* `h^k`
indexing, and §3's prose ("collects every exact Taylor term of order `h²` and
higher") states the correct fact. So this is an exponent typo (`h^{j-1}` for `h^j`)
that propagated into the justification line.

**Verdict on I-1: cosmetic in mathematical consequence, NOT cosmetic in status.**
A referee reading §4 alone cannot verify the bound. **It must be corrected** before
the document is catalogued as a proof. I am deliberately not downgrading it to
"typo, ignore": the archive's discipline is that a proof must be checkable as
written.

### Are the `Δ_r` coefficients `n`-free? (a check the document does not make)

They must be, or `A_r(b)` would not be a constant. **Confirmed:** every coefficient
of `Δ_r` is a rational function of `r,b` only — `n` enters solely through the
explicit powers of `h`. Example output for symbolic `b`:

```
r=2:  h^2 coefficient q_2(t,b) = 8/((b+3)(b+4)(b+5))                       [t-free]
r=3:  h^2 coefficient q_2(t,b) = 12(2b+11t+14)/((b+4)(b+5)(b+6)(b+7))
      h^3 coefficient q_3(t,b) = -90/((b+4)(b+5)(b+6)(b+7))
at b=0, r=2:  q_2 = 2/15
```

That last number is worth pausing on. Combined with my own computation
`ε^h_1(a,b,n) = 2/((b+3)(b+4)n²)` (independent of `a`), it gives
`β(m) = 1/(5mn²)` and hence, through the telescoping of §5,
`R_2(m,0,n) = 1/(15n²)` — **exactly the number the target found numerically at the
base case, but derived analytically here, and valid at every `m`, not just the base
case.** See A.6(d). That is a strong, non-trivial confirmation that the derivation is
not missing a term.

---

## A.3 The discrete-Gronwall telescoping (§5)

### The falling-factorial identity, re-derived from scratch

```
∏_{i=k+1}^{m}(i-j) = (m-j)!/(k-j)! ,   ∏_{i=k+1}^{m} i = m!/k!
⇒ ∏_{i=k+1}^{m}(i-j)/i = (m-j)!k!/((k-j)!m!)
C(k,j)/C(m,j) = [k!/(j!(k-j)!)]·[j!(m-j)!/m!] = k!(m-j)!/((k-j)!m!)      ✔ equal
```

Symbolic difference (gamma form) simplifies to `0`; numerically, **4 764 concrete
`(j,k,m)` triples (`j=1..8`, `k=j..29`, `m=k..39`), 0 mismatches**.

### The summation, re-derived from scratch

`(1/k)C(k,j) = (k-1)!/(j!(k-j)!) = (1/j)C(k-1,j-1)` — symbolic simplify `0`;
**429 `(j,k)` pairs, 0 mismatches**. Hockey stick
`Σ_{l=j-1}^{m-1} C(l,j-1) = C(m,j)` — **0 mismatches**. Composite
`Σ_{k=j}^{m}(1/k)C(k,j) = C(m,j)/j` — **429 `(j,m)` pairs, 0 mismatches**.

Hence `|R_r(m)| ≤ (E_r(b)/(n²C(m,j)))·(C(m,j)/j) = E_r(b)/(j n²)` with `j = r+b+1`,
**with `m` cancelling completely** — the claimed uniformity. Note also
`α(i) = (i-j)/i ≥ 0` for all `i ≥ j`, which is what licenses `|∏α| = ∏α` in the
triangle inequality; that holds since the unrolling only ever uses `i ≥ j+1`.

### Is the "no `log n`" claim overstated? (the task's specific question)

**No — the claim is accurate.** I built the crude bound myself (`∏α(i) ≤ 1`, i.e.
`|R(m)| ≤ (E/n²)·Σ_{k=j}^{m}1/k = (E/n²)(H_m − H_{j-1})`) and compared:

```
  j    m=n   crude factor (H_m-H_(j-1))   exact factor 1/j   crude/exact
  1     10                     2.928968           1.000000        2.929
  1  10000                     9.787606           1.000000        9.788
  1 100000                    12.090146           1.000000       12.090
  3 100000                    10.590146           0.333333       31.770
  6 100000                     9.806813           0.166667       58.841
(check: H_100000 = 12.09015,  ln(100000)+gamma = 12.09014)
```

The crude factor is `H_n ~ log n + γ`; the exact factor is the constant `1/j`. So a
naive discrete-Gronwall write-up genuinely would carry a `log n`, and the exact
telescoping genuinely removes it. **The document is not inflating what it did.**
The numerics also independently corroborate this: `n²|R_r|` is flat/converging in
`n`, not creeping upward (§A.6).

---

## A.4 The `h_r` step (§6): is it really "pure substitution, no Gronwall"?

### My own derivation

`h_r(a,b) = h + rh·h_{r-1}(a,b+1) + [(1-s) − (1+b+r)h]·g_r(n-a,b+1)` with
`s = a/n`, `1-s = (n-a)/n` (**no shift** — the same `s`, so no Taylor expansion is
needed at all here; the target is right about that). Substituting the level-`(r-1)`
`h`-expansion and the just-proved level-`r` `g`-expansion and collecting:

- `h⁰`: `(1-s)F_r(1-s,b+1) = Ĥ_r(s,b)` — by **definition**;
- `h¹`: `1 + rĤ_{r-1}(s,b+1) + (1-s)G_r(1-s,b+1) − (1+b+r)F_r(1-s,b+1) = K_r(s,b)` — by **definition**;
- remainder:
  `ε^h_r = h²[rK_{r-1}(s,b+1) − (1+b+r)G_r(1-s,b+1)] + rh·ε^h_{r-1}(a,b+1) + [(1-s)−(1+b+r)h]·R_r(n-a,b+1)`.

**Identical to §6, term for term.** So yes: one algebraic step, triangle inequality,
done — `h_r`'s rule is not a chain in `a`, so no telescoping is possible or needed.

### Is there a hidden recursive dependency? (the task's specific question)

**No.** `h_r(a,b)` depends on `h_{r-1}(a,b+1)` (level `r-1`, handled by the inductive
hypothesis) and on `g_r(n-a,b+1)` (level `r`, but at `b+1`, and *already bounded* by
§5 which itself needs only level `r-1`). There is no `h_r → h_r` or `h_r → g_{r+1}`
edge. I verified the identity **exactly** over the whole `a`-range including `a=0`:

```
r=1..5, b=0,1,2, n=11,18,25:  TOTAL 309 exact identity checks, 0 mismatches
```

### **ISSUE I-2 — one unremarked out-of-domain reference**

At the maximal valid `a = n-b-r-1`, §6's formula references
`R_r(n-a, b+1, n) = R_r(b+r+1, b+1, n)`, but `g_r(·,b+1)`'s domain requires
`m ≥ (b+1)+r+1 = b+r+2`. So that value does not exist and is **not** covered by §5.

I checked what saves it:

```
r=2 b=0 n=15: a_max=12, coefficient (1-s)-(1+b+r)/n = 0 ; referenced m'=3 < domain min 4  -> OUT OF DOMAIN
r=3 b=1 n=20: a_max=15, coefficient = 0 ; m'=5 < 6   -> OUT OF DOMAIN
r=4 b=0 n=18: a_max=13, coefficient = 0 ; m'=5 < 6   -> OUT OF DOMAIN
r=5 b=2 n=22: a_max=14, coefficient = 0 ; m'=8 < 9   -> OUT OF DOMAIN
```

`(1-s) − (1+b+r)/n = (n-a-1-b-r)/n = 0` there, exactly. So the term is `0·(anything)`
and both the identity and the bound `≤ 2D_r(b+1)/n²` survive — this is the *same*
zero-coefficient mechanism §3 uses for `g_r` and explains at length. **§6 simply
never says so.** One sentence fixes it. Severity: minor write-up gap, no
mathematical consequence.

---

## A.5 The induction closure (§7)

### Base case `r = 0`, re-derived from the lineage's own facts

From the transition rule at `r=0`: `g_0(m,b) = 1/m + ((m-1-b)/m)g_0(m-1,b)`, and by
induction from `g_0(b+1,b) = 1/(b+1)` (the continue-coefficient is `0` there):
`g_0(m,b) = (1/m)[1 + (m-1-b)/(b+1)] = 1/(b+1)`. And `F_0(t,b) = c_0^{(0)}(b) = 1/(b+1)`,
`G_0 ≡ 0` (empty sum). So **`R_0 ≡ 0`, exactly.**

For `h`: `h_0(a,b) = 1/n + ((n-1-a-b)/n)·(1/(b+2)) = (n-a+1)/(n(b+2))`. And
`Ĥ_0(s,b) = (1-s)F_0(1-s,b+1) = (n-a)/(n(b+2))`, `K_0(s,b) = 1/(b+2)` (which I
confirmed also drops out of the *general* `K_r` formula: `1 − (1+b)/(b+2) = 1/(b+2)`).
Then `Ĥ_0 + K_0/n = (n-a)/(n(b+2)) + 1/(n(b+2)) = (n-a+1)/(n(b+2)) = h_0`. So
**`ε^h_0 ≡ 0`, exactly.** `D_0(b) = C_0(b) = 0`. ✔ Matches §7.

### Bookkeeping / circularity audit

```
D_r(b) = [ r·C_{r-1}(b) + A_r(b) ] / (r+b+1)                 <- needs level r-1 at b
C_r(b) =  B_r(b) + r·C_{r-1}(b+1) + 2·D_r(b+1)               <- needs level r-1 at b+1
                                        └─ D_r(b+1) needs C_{r-1}(b+1)
```

Level `r` at `b` needs **only** level `r-1` at `b` and `b+1`, plus `A_r(b)`,
`A_r(b+1)`, `B_r(b)` — all computed from already-known closed forms. **Nothing at
level `r` depends on `D_r(b)` or `C_r(b)` themselves, and nothing depends on a level
`> r`.** Reaching level `r` at `b=0` needs level `0` at `b = 0,…,r`, which is
`0`. **No circularity.** The `b`-index drifts upward but is always finite.

### The audit made concrete: I built the constants myself and tested the bound

Using **my own** `A_r(b)` (from my own `Δ_r`) and the document's own recursion:

```
   r  b           A_r(b)           D_r(b)           C_r(b)
   1  0         0.000000         0.000000         0.500000
   2  0         0.133333         0.377778         2.233333
   3  0         0.464286         1.791071         9.019714
   4  0         1.076190         7.431010        39.764374
   5  0         2.075036        33.482818       202.485138
   6  0         3.594572       174.072200      1200.680035
```

Then, over the **full** `m`-range and the **full** `a`-range, at several `n`:

```
|R_r(m,b,n)| <= D_r(b)/n^2 :
  r=1 b=0: D=0.000000  max n^2|R| observed=0.000000  violations=0  OK
  r=2 b=0: D=0.377778  max=0.066667  violations=0  OK
  r=2 b=2: D=0.140952  max=0.019048  violations=0  OK
  r=3 b=0: D=1.791071  max=0.182143  violations=0  OK
  r=3 b=1: D=1.087000  max=0.098214  violations=0  OK
  r=3 b=5: D=0.303012  max=0.017929  violations=0  OK
  r=4 b=0: D=7.431010  max=0.341005  violations=0  OK
  r=4 b=3: D=2.376231  max=0.078114  violations=0  OK
  r=5 b=0: D=33.482818 max=0.541446  violations=0  OK
  r=6 b=0: D=174.072200 max=0.783381 violations=0  OK

|eps^h_r(a,b,n)| <= C_r(b)/n^2 :
  r=1 b=0: C=0.500000   max=0.166667  violations=0  OK
  r=2 b=0: C=2.233333   max=0.391667  violations=0  OK
  r=2 b=2: C=1.406746   max=0.163690  violations=0  OK
  r=3 b=0: C=9.019714   max=0.669048  violations=0  OK
  r=3 b=1: C=6.955026   max=0.426257  violations=0  OK
  r=4 b=0: C=39.764374  max=0.997266  violations=0  OK
  r=5 b=0: C=202.485138 max=1.376849  violations=0  OK
```

**Zero violations.** Note `A_1(b) = 0 ⇒ D_1(b) = 0`, so the proof makes the sharp
prediction `R_1 ≡ 0` — not merely bounded — which the data confirms exactly (A.6(d)).
Note also that `D_r(b)` is very loose at larger `r` (`174` vs an observed `0.78` at
`r=6`); the document is honest that it makes no claim about the growth rate of the
constants (§8 item 1), and I confirm none is established.

---

## A.6 Fresh, independent numerics — my own simulator, my own probe points

**My simulator.** A separately-written memoized exact-`Fraction` recursion over
`(a,b,r)` implementing wave 6's two transition rules directly, with explicit domain
assertions (`a+b+r < n`). Validation *against facts proved elsewhere in the lineage,
not against this document*:

```
K=1, n=2..7:  chain == (4n+1)/(6n)                            [wave 5, PROVED]  6/6
K=2, n=3..8:  chain == (8n^2+4n+1)/(15n^2)                    [wave 5, PROVED]  6/6
K=6, n=7,8,9,12,17,25: chain == parent's PROVED psi_n^(6)     6/6 exact
   incl. n=7 -> 355081/823543  (the value confirmed by exhaustive brute force
   in the prior referee round, 592,950,960 combinations)
```

My closed forms independently reproduce `F_r(1,0) = φ_r` and `G_r(1,0) = rφ_r/4` for
`r = 0,…,8`. So the model and the closed forms in my code are the right ones.

### (a) The base-case boundary at `r = 6` and `r = 7` (and `9`, `10`), `b = 0` and `b = 2`

The target checked the exact-value pattern only at `r = 1` (exactly `0`) and `r = 2`
(exactly `1/(15n²)`). I checked whether that pattern "continues sensibly or breaks".
It does **not** continue as an exact closed value — and it should not, and the
theory says so: exact values occur only when `Δ_r` and `ε^h_{r-1}` are constant,
which happens only at `r = 1, 2`. At `r ≥ 3`, `n²R` at the base case is
`n`-dependent but **converges**:

```
 r  b     n   m       R_r(m,b,n) (exact)        n^2 * R
 1  0   2..66  2                     0        +0.0000000000   -> CONSTANT = 0
 2  0   3..69  3          1/135 … 1/71415      +0.0666666667   -> CONSTANT = 1/15
 6  0     7   7     6041621/353299947          +0.8379266159
 6  0    81   7  18821610107/848135898052443   +0.1455999966   (not constant)
 7  0     8   8     3070751/173015040          +1.1359016187
 7  0    84   8  14940092459/703298659295232   +0.1498897957   (not constant)
 6  2 / 7  2 : same picture, decreasing, not constant
```

Pushing `n` far higher (the base-case computation collapses to a short explicit path,
so `n = 10⁶` is cheap and *exact*):

```
  r=6  b=0, m=7 :  n=100 0.140212  n=10^3 ~0.1215  n=10^4 0.1192454  n=10^5 0.1190674  n=10^6 0.1190496
  r=7  b=2, m=10:  n=100 0.079319                  n=10^4 0.0637785  n=10^5 0.0636506  n=10^6 0.0636378
  r=9  b=0, m=10:  n=100 0.148718                  n=10^4 0.1094321  n=10^5 0.1091250  n=10^6 0.1090943
  r=10 b=3, m=14:  n=100 0.077930                  n=10^4 0.0537735  n=10^5 0.0535916  n=10^6 0.0535734
```

Successive changes shrink by a factor of ~10 per decade of `n` — i.e. `n²R = c + O(1/n)`,
exactly what `R = c/n² + O(1/n³)` predicts. **Bounded, convergent, no `log n`, no
break in the pattern.** These are `r = 6,7,9,10` — well beyond the target's `r ≤ 5`
and beyond the parent's 11 concretely-checked `K` values only in the sense that they
are new probe points; note `r = 9, 10` are inside the parent's ladder but were never
probed this way.

### (b) A genuinely large `b`: `r = 3, b = 5`

```
  n=  20:  max_m n^2|R_3(m,5,n)| = 0.01782828  at m=20 (t=1.000)
  n=  40:  max_m n^2|R_3(m,5,n)| = 0.01775253  at m=40
  n=  80:  max_m n^2|R_3(m,5,n)| = 0.01771465  at m=80
  n= 160:  max_m n^2|R_3(m,5,n)| = 0.01769571  at m=160
```

Monotonically converging, bound `D_3(5) = 0.303` never approached. The target's
numerics were essentially `b ∈ {0,1}`; large `b` behaves identically.

### (c) `n²R_r` at fixed `t`, growing `n`, at combinations the target never tested

```
r=4, b=3, t=1  : 0.0767992 0.0761495 0.0758266 0.0756657 0.0755853   (n=24..384)
r=4, b=3, t=1/2: 0.0532407 0.0527225 0.0524654 0.0523373 0.0522734
r=6, b=0, t=1  : 0.7480017 0.7311308 0.7228933 0.7188232 0.7168002
r=3, b=5, t=1/4: 0.0135732 0.0135417 0.0135259 0.0135180            (n=48..384)
r=5, b=2, t=2/3: 0.1373346 0.1352452 0.1342164 0.1337059 0.1334517
```

Ratios to the previous `n` are `0.9915, 0.9958, 0.9979, 0.9989` — halving the gap
each time `n` doubles. That is `c + O(1/n)`, i.e. **bounded, converging, no `log n`
and no growth**, at five `(r,b,t)` combinations none of which the target tested.

### (c′) The genuine boundary layer: `m` fixed and small, `n → 5·10⁵`

This is the sharpest version of the prior referee's §B.4(b) worry: if `G_r` carried a
homogeneous admixture `C·t^{-(1+r+b)}`, then at fixed `m` we would see
`n²R ~ n²·(1/n)·(m/n)^{-(1+r+b)} ~ n^{r+b}` — a blow-up by `~5^{r+b}` per column
below. Observed:

```
r=3 b=0 m= 4 : n=200 +0.101786  n=10^3 +0.100357  n=5·10^3 +0.100071  n=5·10^4 +0.100007  n=5·10^5 +0.100001
r=3 b=0 m=12 : n=200 +0.104929  n=10^3 +0.100986  n=5·10^3 +0.100197  n=5·10^4 +0.100020  n=5·10^5 +0.100002
r=4 b=1 m= 6 : n=200 +0.074317  n=10^3 +0.072001  n=5·10^3 +0.071543  n=5·10^4 +0.071440  n=5·10^5 +0.0714297
r=4 b=1 m=18 : n=200 +0.079767  n=10^3 +0.073057  n=5·10^3 +0.071753  n=5·10^4 +0.071461  n=5·10^5 +0.0714318
r=6 b=0 m= 7 : n=200 +0.129273  n=10^3 +0.121037  n=5·10^3 +0.119443  n=5·10^4 +0.119087  n=5·10^5 +0.1190516
r=6 b=0 m=21 : n=200 +0.150065  n=10^3 +0.124799  n=5·10^3 +0.120180  n=5·10^4 +0.119161  n=5·10^5 +0.1190589
```

Every column converges to the *same* constant independent of `m`
(`1/10`, `1/14`, `≈0.11905`). **No blow-up of any kind.** For `r=6,b=0` a homogeneous
admixture would have inflated these numbers by `~5⁷ ≈ 78 000` per column; they move
by `<0.01`. This is the single strongest piece of evidence that the polynomial `G_r`
is the whole `O(1/n)` correction, uniformly to the boundary.

### (d) Two sharp predictions of the argument that the document never states

Deriving `Δ_r` and `ε^h_{r-1}` myself lets me make predictions the target does not
make, and then test them — a stronger test than agreeing with its numbers:

- **P1:** since `deg F_1 ≤ 1`, `deg G_1 ≤ 0`, `deg Ĥ_0 ≤ 1`, `deg K_0 ≤ 0`,
  `Δ_1 ≡ 0`; and `ε^h_0 ≡ 0`; so `R_1(m,b,n) = 0` **exactly for every `m,b,n`**, not
  just at the base case. → **485 exact evaluations, 0 nonzero residuals. CONFIRMED.**
- **P2:** `Δ_2(t,0,h) = (2/15)h²` (`t`-free) and `ε^h_1(a,b,n) = 2/((b+3)(b+4)n²)`
  (`a`-free), so `β(k) = 1/(5kn²)` and the telescoping collapses to
  `R_2(m,0,n) = 1/(15n²)` **for every `m`**, not just the base case the target
  probed. → **220 exact evaluations, 0 deviations. CONFIRMED.** The `ε^h_1`
  prediction: **0 deviations** over `n=6,11,20,33`, `b=0..3`, all `a`.

The target reported `1/(15n²)` as an empirical curiosity at one point. It is in fact
a theorem of its own argument, valid on the whole domain — and it drops out of my
independent hand-derivation of `Δ_2` (`q_2 = (1+r+b)F_2''/2 − (1+r+b)G_2' − (r/2)Ĥ_1''
− rK_1' = 3/10 · … = 2/15`). Recovering the document's observed constant from a
from-scratch symbolic expansion is about as good a cross-check as this kind of
argument admits.

### (e) Exhaustive `m`-scans (the target's scan is log-sampled; mine is not)

`probe_uniform.py` samples ~25 log-spaced `m` per `n`, though §7 calls it "the
entire range". I scanned **every** `m`:

```
r=3 b=0 n=200: ALL 197 m scanned; max 0.17878571 at m=200 (t=1.0000); max over m<n = 0.17839286
r=3 b=0 n=400: ALL 397 m scanned; max 0.17867857 at m=400;             max over m<n = 0.17848214
r=2 b=1 n=200: ALL 197 m scanned; max 0.03333333 at m=4 (t=0.0200);    max over m<n = 0.03333333
r=5 b=0 n=120: ALL 115 m scanned; max 0.51018967 at m=120;             max over m<n = 0.50528043
r=4 b=1 n=150: ALL 145 m scanned; max 0.18709079 at m=150;             max over m<n = 0.18613788
r=4 b=3 / r=5 b=1 / r=6 b=0, n=64,128,256: max always at m=n
```

**No interior spike anywhere.** The worst case is essentially always `t=1` — i.e. at
`ψ_n^{(K)}` itself — which is the *opposite* of a boundary-layer failure. The
log-sampling did not hide anything.

### (f) `h_r` at its own boundary, at `r=4,5` (target checked `r≤3`, `b=0`)

```
r=4 b=0: n=20 0.96908730  n=40 0.94856994  n=80 0.93850639   (worst at a=0)
r=4 b=2: n=20 0.43774495  n=40 0.42976720  n=80 0.42584610   (worst at a=0)
r=5 b=0: n=20 1.32294282  n=40 1.28435883  n=80 1.26564011   (worst at a=0)
```

Worst case at `a=0` as the target reports for lower `r`; converging, bounded, well
under `C_4(0)=39.8`, `C_5(0)=202.5`.

---

## A.7 (beyond the brief) What the theorem actually licenses downstream — and a pre-existing error it exposes

If the Target Theorem holds, then with Reduction Lemma A
(`φ_n^{(K)} = (K/n)ψ_n^{(K),R} + (1-K/n)ψ_n^{(K)}`, wave 5, PROVED) and
`ψ_n^{(K,R)} = h_{K-1}(0,0)`, one gets for **every** `K` the exact `1/n` coefficient
of `φ_n^{(K)}`:

```
φ_n^(K) − φ_K = K[ φ_K/4 + F_{K-1}(1,1) − φ_K ]/n + O(1/n²)
```

(using `Ĥ_{K-1}(0,0) = F_{K-1}(1,1)`). I computed it:

```
    K     phi_K   F_(K-1)(1,1)   predicted 1/n coeff
    1       2/3            1/2                    0    <-- EXACTLY ZERO
    2      8/15           5/12                 1/30
    3     16/35          11/30                 1/14
    4   128/315         93/280               23/210
    5   256/693        193/630               29/198
    6  1024/3003       793/2772           1093/6006
    7  2048/6435       1619/6006            309/1430
    8 32768/109395  26333/102960         10889/43758
   ... through K=12, all strictly positive
```

**Three independent confirmations of this formula:** `1/30` at `K=2` is wave 5's
own number; `1/14` at `K=3` is wave 6's own number; and **`1093/6006` at `K=6` is
exactly the value the prior referee computed by four independent methods when
correcting the parent's §1.2 bug.** Getting all three out of a formula derived from
the Target Theorem is meaningful evidence that the theorem is doing real work.

### **ISSUE I-4 — the `Θ(1/n)` claim is false at `K=1`, and this now matters**

`../ATTEMPT.md` §5 and its Scorecard row 9 assert
`φ_n^{(K)} − φ_K = Θ(1/n)` **for every `K ≥ 1`**, carrying "the same caveat as #7".
The `K=1` coefficient above is exactly `0`, and directly from my chain:

```
n=3:  phi_n^(1) = 19/27   , phi_n^(1)-2/3 = 1/27   , n^2*(…) = 1/3
n=5:  phi_n^(1) = 17/25   , phi_n^(1)-2/3 = 1/75   , n^2*(…) = 1/3
n=10: phi_n^(1) = 67/100  , phi_n^(1)-2/3 = 1/300  , n^2*(…) = 1/3
n=20: phi_n^(1) = 267/400 , phi_n^(1)-2/3 = 1/1200 , n^2*(…) = 1/3
n=40: phi_n^(1) = 1067/1600, phi_n^(1)-2/3= 1/4800 , n^2*(…) = 1/3
```

`φ_n^{(1)} − φ_1 = 1/(3n²)` exactly — **`Θ(1/n²)`, not `Θ(1/n)`.** Wave 5 already
recorded this cancellation, and the prior referee quoted it (in §A.5, for a different
purpose) without noticing it contradicts the parent's §5 quantifier.

This is **not the target document's error.** But the target's §9 says its Theorem
"removes the last named caveat" from the parent's general-`K` results, and that row
carried exactly that caveat. Promoting it verbatim would convert a *false*
conditional statement into a *false unconditional* one — a strictly worse outcome for
the archive. **The orchestrating session must re-scope it at integration.**

---

# Assessment of the target's own honesty and scorecard

I checked each Scorecard row against what I verified:

| Row | Target's status | My assessment |
|---|---|---|
| 1 — exact residual recursion (§3) | PROVED | **Confirmed.** 477 exact identity checks, 0 mismatches; base case genuinely subsumed. |
| 2 — `Δ_r = O(h²)` uniformly, constant `A_r(b)` (§4) | PROVED | **Confirmed as a fact** (I verified `Δ_r = Σ_{k=2}^r h^k q_k` for `r=0..8`, symbolic `b`), **but the written proof of it contains I-1 and does not currently establish it as printed.** Fix required. |
| 3 — Gronwall closure, no `log n` (§5) | PROVED | **Confirmed**, identities re-derived and checked symbolically + on thousands of concrete cases; the `log n` claim is not overstated. |
| 4 — `h_r` closure (§6) | PROVED | **Confirmed**, 309 exact checks; one unremarked out-of-domain point (I-2), harmless. |
| 5 — Existence Theorem, general `r` (§7) | PROVED | **Confirmed**, subject to I-1's correction. No circularity; base case exact. |
| 6 — numerical corroboration | NUMERICALLY VERIFIED | **Confirmed and extended far beyond what was run** — but the *descriptions* of the runs overstate them (I-3). |
| 7 — closed forms for `D_r,C_r,A_r` | NOT ATTEMPTED | **Correctly labelled**, and correctly identified as not needed for existence: for each fixed `(r,b)`, `A_r(b)` is a finite sum of coefficient-norms of an explicit finite polynomial. Its *finiteness* is fully rigorous for general `r` given Facts 1–3. |
| 8 — all-orders closed form | NOT ADDRESSED | **Correctly labelled.** Genuinely separate and genuinely still open. |
| 9 — independent adversarial review | NOT PERFORMED | **Now performed — this report.** |

The document's §8 accounting is unusually good. In particular §8's answer to the
prior referee's `F_r`/`G_r` boundedness asymmetry is *logically correct and worth
recording*: it does not find an a-priori bound for `G_r`; it makes one unnecessary by
directly certifying the specific polynomial candidate against the true recursion at
the boundary itself. Note the argument is in fact stronger than §8 claims: **if the
polynomial two-term expansion holds uniformly to `O(1/n²)`, then no homogeneous
admixture is possible at all**, since the `O(1/n)` correction of a convergent
expansion is unique. So the prior referee's §B.4(b) concern is genuinely *closed*,
not merely side-stepped.

I found **no** overclaim in §8's list of what remains open, and **no** attempt to
present the numerics as the proof.

---

# FINAL JUDGMENT

## Is the Target Theorem established?

**Yes.** Modulo the correction of I-1 (a one-character exponent fix in §4 whose
underlying fact I verified independently), the argument of §§2–7 is a complete,
non-circular, first-principles proof that for every `r ≥ 0` and `b ≥ 0` there are
finite constants `D_r(b), C_r(b)` with
`|g_r(m,b) − F_r(m/n,b) − G_r(m/n,b)/n| ≤ D_r(b)/n²` for **every** valid `m`, and
`|h_r(a,b) − Ĥ_r(a/n,b) − K_r(a/n,b)/n| ≤ C_r(b)/n²` for **every** valid `a`.

The proof's dependencies are exactly: (i) wave-6's transition rules (PROVED,
referee-verified upstream; my independent implementation reproduces wave 5's and
wave 6's PROVED closed forms including the brute-force-confirmed `355081/823543`);
(ii) Facts 1–3, which are algebraic identities about *explicit polynomials* and which
I verified for **fully symbolic `r,k,b`**; (iii) Fact 4, definitions. Nothing
asymptotic is assumed anywhere. The one genuine cleverness — that the base case is
subsumed because the contraction coefficient is exactly zero there — is a real,
checkable property of the already-proven recursion.

## How should the archive describe the results now?

**1. `k6_attempt/ATTEMPT.md` §4's caveat is CLOSED.** It should no longer be carried.
Scorecard rows 5, 6 and 7 of that document — the general-`r` closed forms `F_r`,
`G_r`, and the general-`K` rate conjecture — become **PROVED, unconditional**. (This
supersedes the prior referee's recommendation, which was correct *at the time*, that
rows 5–6 be annotated "modulo §4's caveat".)

**2. The general-`K` Open Lemma bridge becomes UNCONDITIONAL.** `ψ_n^{(K)} = g_K(n,0)`
is the `t=1` instance of the Target Theorem, so `ψ_n^{(K)} → F_K(1,0) = φ_K` for every
`K`; with Reduction Lemma A (PROVED, wave 5), `φ_n^{(K)} → φ_K` for every fixed `K`.
`THEOREM.md` §7.4's Open Lemma is therefore **PROVED for every `K`**, not just
`K = 0,…,10`, and `THEOREM.md`'s "Proposição Condicional 5" loses its dependence on
the Open Lemma as an unproved hypothesis. *This is the major upgrade, and I judge it
earned.*

**3. The general-`K` rate becomes UNCONDITIONAL:**
`lim n(ψ_n^{(K)} − φ_K) = Kφ_K/4` for every `K ≥ 0`.

**4. But `φ_n^{(K)} − φ_K = Θ(1/n)` must NOT be promoted as written.** It is false at
`K = 1` (`= 1/(3n²)` exactly). Re-scope to `K ≥ 2`, or — better, since the Target
Theorem now licenses it — state the *stronger* result: for every `K ≥ 1`,
`φ_n^{(K)} − φ_K = K[φ_K/4 + F_{K-1}(1,1) − φ_K]/n + O(1/n²)`, a coefficient that is
`0` at `K=1` and strictly positive for `2 ≤ K ≤ 12` (verified; `1/30`, `1/14`,
`23/210`, …, `1093/6006` at `K=6`).

**5. Prerequisites before cataloguing:** I-1 corrected in `k_general_existence_attempt/ATTEMPT.md`
§4 (mandatory — the printed proof of the key bound is currently invalid as written);
I-2 noted in §6 (one sentence); I-3's evidence descriptions in §7/Executive Summary
brought into line with the retained logs; I-4 handled wherever the parent's `Θ(1/n)`
row is carried forward.

**6. What remains genuinely open** (and the archive should keep saying so):
the *exact, all-orders* closed form for `ψ_n^{(K)}` at general `K`
(`../ATTEMPT.md` §6.2); the growth rate in `r` of the error constants `D_r(b), C_r(b)`
(the recursion produces constants that are visibly very loose — `174` at `r=6` where
the truth is `0.78`); and closed forms for `A_r(b), B_r(b)`. None of these is needed
for anything catalogued above.

---

# Scope of this review, stated honestly

- I did **not** re-derive wave 6's transition-rule Proposition, wave 5's Reduction
  Lemma A, or the parent's discovery of `F_r`/`G_r` from the combinatorial model —
  the brief scopes those out as already referee-verified. I did confirm that my
  independently-written chain reproduces wave 5's PROVED `ψ_n^{(1)}, ψ_n^{(2)}` and
  the parent's PROVED `ψ_n^{(6)}` (including `n=7,8`, the brute-force-confirmed
  points) exactly, which is a meaningful check that the model in my code is the
  right one.
- I did **not** re-run the parent's `K = 7,…,10` ladder; the prior referee did.
- Facts 2 and 3 for general symbolic `r` I *did* verify myself, from a coefficient
  recursion I extracted from the ODE independently rather than transcribing.
- All numerics are exact `fractions.Fraction` / `sympy.Rational`; floats appear only
  in printed convergence displays.

---

# Files produced by this review

All in
`.../k3_attempt_2/k6_attempt/k_general_existence_attempt/adversarial/`:

- `adv_core.py` / `.log` — my independent exact-`Fraction` `(a,b,r)` chain and my
  independent transcription of `F_r, G_r, Ĥ_r, K_r`; smoke tests against `φ_r`,
  `rφ_r/4`, `K_0 = 1/(b+2)` and wave 5's PROVED `ψ_n^{(1)}, ψ_n^{(2)}`.
- `adv_residual_derivation.py` / `.log` — Part A items 1(a)–(d): exact polynomial
  Taylor; my own substitution of the ansatz into `(*)` with the `h`-coefficient
  breakdown for `r=0..8`, symbolic `b`; Facts 2/3 as stated; the base-case zero
  coefficient; explicit `Δ_2`, `Δ_3`.
- `adv_gronwall_identities.py` / `.log` — Part A items 2 and 3: the coefficient-sum
  lemma (and the necessity of `x∈[0,1]`, and where it is applied); the
  falling-factorial identity (symbolic + 4 764 triples); `(1/k)C(k,j)=(1/j)C(k-1,j-1)`,
  hockey stick, and the composite sum (symbolic + 429 pairs each); the
  independently-constructed crude bound and its `log n` growth.
- `adv_symbolic_r.py` / `.log` — Facts 2 and 3 for **symbolic `r,k,b`** via
  gamma-function closed forms, from a coefficient recursion I extracted myself; plus
  the two sharp predictions P1 (`R_1 ≡ 0`) and P2 (`R_2(m,0,n) = 1/(15n²)` for every
  `m`) and their exact confirmation.
- `adv_endtoend.py` / `.log` — the decisive check: 477 exact verifications of §3's
  residual recursion, 309 of §6's identity, and construction of `A_r(b), B_r(b),
  D_r(b), C_r(b)` by the document's own recursion followed by a full-domain test of
  the claimed bounds (0 violations).
- `adv_numerics.py` / `.log` — fresh numerics at probe points the target never used:
  base case at `r=6,7`, `b=0,2`; `r=3,b=5`; fixed-`t` scaling at five untested
  `(r,b,t)`; whole-range scans; `h_r` at `r=4,5`.
- `adv_boundary_layer.py` / `.log` — Facts 1–3 at concrete `b` up to `r=12`; base
  case to `n = 10⁶`; the fixed-small-`m`, `n → 5·10⁵` boundary-layer stress test;
  larger-`n` whole-range scans.
- `adv_final_sweep.py` / `.log` — exhaustive (every `m`) scans at `n` up to 400; the
  §6 out-of-domain point and its zero coefficient; my chain vs the parent's PROVED
  `ψ_n^{(6)}`.
- `adv_downstream_consequences.py` / `.log` — the general-`K` `φ`-rate coefficient
  and the `K=1` counterexample to the parent's `Θ(1/n)` claim.

To reproduce: each script runs standalone with `python3 <script>.py`.
`adv_residual_derivation.py` takes ~15 min (symbolic `b` up to `r=8`);
`adv_endtoend.py` and `adv_boundary_layer.py` a few minutes each; the rest seconds.

---

# Governance discipline check

- `THEOREM.md`, `DECISION_LEDGER.yaml`, `CLAIM_LEDGER.yaml`, `TEST_QUEUE.yaml`,
  `DISCOVERY_LAB_STATE.md`, `README.md`/`README_*.md` — **none modified**, read-only.
- The target document (`k_general_existence_attempt/ATTEMPT.md`) and every file in
  `k6_attempt/` and its other subdirectories — **none modified**, read-only.
- Nothing under `generalization_u_alpha/` was read or touched.
- All artifacts of this review confined to
  `.../k6_attempt/k_general_existence_attempt/adversarial/`.
- No git commit made. No AI model name appears in any file created by this review.
