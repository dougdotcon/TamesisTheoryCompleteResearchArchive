# REFEREE REPORT — `DIAGONAL-2F0-SUM-ATTEMPT`

**Target:** `.../gamma_c_gamma_construction_attempt/diagonal_2f0_sum_attempt/ATTEMPT.md`
(Wave 29, front (b), authorized by `DISC-DEC-134`)

**Referee:** hostile, independent adversarial session. Read, in full and in
prose, before opening any script belonging to the target, in the order the
target's own §0 specifies: `THEOREM.md`'s Estágio 51 (the predecessor's
integration, its exact framing of the Charlier non-identification and the
"diagonal-parameter sum" diagnosis); `.../gamma_c_gamma_construction_attempt/ATTEMPT.md`
(611 lines, the immediate predecessor, wave 28 front (b)) **in full,
including a direct reading of its own script `01_exact_hypergeometric_structure.py`**
(not just its prose/log) — this last step was treated as mandatory, since
the target's central claim is a correction of that script's own Part C, and
no assessment of "is this a fair reconstruction of the predecessor's bug"
is possible without reading the actual code; `.../gamma_c_gamma_construction_attempt/adversarial/REFEREE_REPORT.md`
(373 lines, the predecessor's own referee); `.../gamma_scaling_attempt/ATTEMPT.md`
(592 lines, the ultimate ancestor, for Lemma 1, Lemma 3, and the original
`A_k`/`P_{k,m}` definitions). Only after all of that was the target's own
`ATTEMPT.md` and its seven scripts (`01`–`07`) read.

This is pure combinatorial/asymptotic mathematics internal to this
archive, about a specific random-permutation-with-reroutes ensemble — no
Millennium Prize Problem, no physics claim, anywhere in this document, its
target, or any of its ancestors.

---

## VERDICT: **SOUND — ACCEPT for catalogue.** The correction to Estágio
## 51's Charlier finding survives hostile scrutiny and should be recorded.

Every load-bearing mathematical claim was independently re-derived —
**not merely re-read** — from primary definitions, using fresh code that
imports nothing from the target, the predecessor, or any ancestor. In
every single case the independent computation reproduces the target's
claim exactly (symbolic zero-difference or exact-rational/high-precision
numeric agreement). The central, highest-stakes claim — that the
predecessor's reported Charlier "non-identification" was the predecessor's
own sign-convention **implementation bug**, not a genuine mathematical
fact — is **confirmed at the strongest possible level this referee could
achieve short of literally re-executing the predecessor's file**: by
transcribing the predecessor's own `Charlier_symbolic` function verbatim
from their script `01` (read directly, per the mandate) and proving
**algebraically** (symbolic zero-difference, `k=0..6`) that it computes
*exactly* the same function as the target's "wrong `+1/a` sign" variant —
not a coincidentally-matching alternative bug, but the literal same
mathematical object. Additionally, this referee found and independently
confirmed a **second, previously-unnoticed error** on the predecessor
side of this dispute: the predecessor's own referee's specific claim that
the Charlier mismatch was "a real, structural mismatch, not a sign flip
away from working" does **not** hold up — it is, in fact, exactly a sign
flip away from working (see finding (A) below).

Two **minor/cosmetic** findings are recorded (neither affects any proved
result or the front's bottom-line verdict): (i) a prose percentage in §4
("≈0.2%") is off by a factor of ≈1.8× from the front's own script `04`
tabulated value (0.11%); (ii) the phrase "neither the predecessor nor
their dedicated referee... caught it" is slightly overstated — the
predecessor's own prose *did* already flag "likely a sign/convention
mismatch" as a suspected cause, though neither party tested or resolved
it. No MODERATE or SEVERE finding was found anywhere in this front —
cleaner, on this metric, than its own immediate predecessor's front (which
had one MODERATE finding, itself correctly caught by that front's referee).

---

## Independent verification, item by item

### (A) The corrected Charlier identity and the predecessor's actual bug (§2) — the central claim

**DLMF convention, re-derived from its primary characterization, not
trusted from the citation.** `C_n(x;a) := {}_2F_0(-n,-x;;-1/a) =
\sum_{j=0}^n\binom nj(-x)_j(-1/a)^j`. This referee independently expanded
this from the raw hypergeometric-series definition (`(a)_j(b)_j/j!\cdot
z^j` summed, `a=-n,b=-x,z=-1/a`) — matching what both the predecessor's
and the target's own scripts cite as "DLMF 18.20.1 / Koekoek–Lesky–
Swarttouw" — a standard, unambiguous convention independent of any
archive script.

**Identity re-verified, extended range.** `A_k(n,γ) = (1-γ)^k\,{}_2F_0(-k,
n-k+1;;w)`, `w=-γ/((1-γ)n)` (the predecessor's own PROVED fact, re-derived
here too from the raw `A_k` sum): symbolic zero difference, `n,γ` free,
`k=0,\ldots,8` (this referee's own range, one `k` beyond both the target's
and the orchestrating session's pre-dispatch check) — **0/9 mismatches**
(`adv01`, CHECK 1). The Charlier identification itself, `A_k(n,γ)=(1-γ)^k
C_k(k-n-1;(1-γ)n/γ)`, independently re-implemented from the DLMF
definition (not copied from the target's `02_charlier_identity_correction.py`):
symbolic zero difference, `k=0,\ldots,8` — **0/9 mismatches** (`adv01`,
CHECK 2). **This is an exact algebraic identity, confirmed independently
at one `k` beyond every prior check in this dispute.**

**Root-causing the predecessor's actual bug, by direct code inspection —
not just residual-matching.** The predecessor's `01_exact_hypergeometric_structure.py`,
Part C, defines:

```python
def Charlier_symbolic(k_val, x_sym, a_sym):
    total = sp.Integer(0)
    poch_negk = sp.Integer(1)      # (-k)_m -- COMPUTED...
    poch_negx = sp.Integer(1)
    fact = sp.Integer(1)
    for m_val in range(0, k_val+1):
        if m_val > 0:
            poch_negk *= (-k_val + (m_val-1))
            poch_negx *= (-x_sym + (m_val-1))
            fact *= m_val
        total += binomial(k_val, m_val) * poch_negx * (-1/a_sym)**m_val
    return sp.expand(total)
```

`poch_negk` (the Pochhammer `(-k)_m`, needed for the correct coefficient
`(-k)_m(-x)_m/m!`) is computed on every iteration **and never used** —
`total` accumulates `binomial(k_val,m_val)` instead. Since the correct
identity is `(-k)_m/m! = (-1)^m\binom km`, using `\binom km` in its place
silently drops a factor of `(-1)^m` from every term with `m` odd. This
referee proved, **by literal transcription of the predecessor's function**
(not a paraphrase — `adv01` CHECK 3 defines `predecessor_charlier_aswritten`
copying the above code's logic exactly, arithmetic operation for arithmetic
operation) that this dropped sign is **algebraically identical**,
term-by-term, to substituting `+1/a` for DLMF's `-1/a` inside the `2F0` —
symbolic zero difference against the target's own "wrong-sign"
reconstruction, `k=0,\ldots,6`, **0/7 mismatches**. This closes the loop
the dispatch mandate asked to close: the target's reconstruction of the
predecessor's bug is **not** a coincidentally-matching alternative
explanation that happens to produce the same `-2γ` number — it is a
byte-for-byte-equivalent-in-effect account of the actual defect in the
actual function the predecessor ran. **Confirmed at the highest evidentiary
standard achievable without executing the original file itself.**

**Residual formulas, hand- and machine-verified beyond the target's own
range.** By hand (this referee, independent of any script): at `k=1`,
`x=-n`, `a=(1-γ)n/γ`; correct `C_1(x;a)=1-x/a=1/(1-γ)`, giving `(1-γ)C_1=1=A_1`
✓. Wrong-sign `C_1^{\text{wrong}}=1+x/a=(1-2γ)/(1-γ)`, giving
`(1-γ)C_1^{\text{wrong}}=1-2γ`, residual `-2γ` against `A_1=1` — **matches
the predecessor's reported number exactly**, derived here independently of
any archive script. Machine-verified, extended to `k=1,2,3,4` (`adv01`,
CHECK 2 second block): `k=1`: `-2γ`; `k=2`: `4γ(γ-1)(n-1)/n`, algebraically
identical to the target's own quoted `4γ(γn-γ-n+1)/n` (verified by hand:
`γn-γ-n+1=(n-1)(γ-1)`); `k=3`,`k=4`: new (uncomputed by either ancestor
front), increasingly complex rational-function residuals, consistent with
the same single sign bug propagating through longer Pochhammer products —
**not** independent evidence of a "genuine structural mismatch" at each
`k` (see next paragraph).

**A finding of this referee's own, beyond the dispatch's checklist: the
predecessor's referee's specific rebuttal does not survive scrutiny.** The
predecessor's `adversarial/REFEREE_REPORT.md` §(g) states the mismatch is
"a real, structural mismatch, **not a sign flip away from working**,"
reasoning from the fact that `k=2,\ldots,6` "leave increasingly complex
nonzero polynomial residuals." This referee's own `k=1,\ldots,4`
computation above shows this reasoning does not hold: a **single**,
consistent sign bug propagating through a Pochhammer product of growing
length is *expected* to produce increasingly complex, `n`-and-`γ`-dependent
residuals at each successive `k` — that pattern is fully consistent with
(not evidence against) exactly the sign-flip explanation the predecessor's
referee dismissed. The predecessor's referee re-read the log but, by their
own account, did not independently re-derive this specific sub-claim — had
they tested the single-sign-flip hypothesis computationally (as this front,
and now this report, both do), it would have resolved cleanly. This is a
genuine, if secondary, error on the predecessor-referee side of this
dispute, uncovered by this review, not merely inherited from the target.

**Nuance on "neither the predecessor nor their referee caught it"
(cosmetic finding).** Re-reading the predecessor's own prose precisely:
`ATTEMPT.md` §2 already says the failure is "likely a sign/convention
mismatch against one of several inequivalent textbook conventions," and
script `01`'s own inline comment says "almost certainly caused by a wrong
sign or off-by-one." The predecessor did **not** have zero suspicion of a
sign issue — they named the right general category. What they did not do
is test any specific alternate sign/convention computationally, or
recognize that their own code did not correctly implement *any* legitimate
textbook variant (the bug is not "convention B instead of convention A" —
it is a dropped alternating sign, not equivalent to any standard reference
convention on its own). The target's phrasing is defensible as "neither
party identified, tested, or fixed the specific defect," but a maximally
fair record should note the predecessor's prose already gestured at the
right diagnosis without running it down. Recommended for the `THEOREM.md`
wording (see "What this changes" below).

### (B) Why the corrected identification still doesn't unlock the diagonal
### sum — the EGF/Cauchy-extraction divergence argument (§2)

Re-derived independently from scratch. The Charlier EGF
`\sum_kC_k(x;a)t^k/k!=e^t(1-t/a)^x` (standard, cross-checked by this
referee against the DLMF-convention series definition at small `k` by
direct Taylor expansion) gives, via Cauchy's coefficient formula,
`C_k(x;a)=\frac{k!}{2\pi i}\oint\frac{e^t(1-t/a)^x}{t^{k+1}}dt`. Substituting
`x_k=k-(n+1)` (linear in `k`, elementary algebra, independently confirmed)
factors `(1-t/a)^{x_k}=(1-t/a)^{-(n+1)}(1-t/a)^k` exactly, turning
`\sum_k(1-γ)^kC_k(x_k;a)` into a contour integral of `\sum_kk!\,z(t)^k`,
`z(t):=(1-γ)(1-t/a)/t`. This referee confirms the underlying fact used
here — that `\sum_{k=0}^\infty k!z^k` has zero radius of convergence for
`z\ne0` and is only Borel-summable — is standard and correctly invoked.
**One clarification this referee adds, not present in the target's own
text**: the *actual* sum in `S_n(γ)` is finite (`k` from `0` to `n`), so
there is no formal convergence failure in the literal object being
computed — the obstruction is that there is no simpler *closed form* for
the **partial** sum `\sum_{k=0}^nk!z^k` either, precisely because it is a
truncation of a divergent asymptotic series with no elementary generating
function of its own (unlike, e.g., a truncated geometric series). The
target's own §6 item 2 already scopes this correctly ("not a proof that no
technique using the Charlier structure could work") — this referee agrees
that is the right, appropriately hedged conclusion, and confirms the
underlying algebra and the standard fact about `\sum k!z^k` are both used
correctly. **SHOWN, not proved-impossible — accurately labeled as such
by the target.**

### (C) The double-sum reformation and the Vandermonde-type sub-identity (§3)

Independently re-derived the swap `S_n'=\sum_m(γ^m/n^m)m!\,T(n,m)` from
Lemma 1's `P_{k,m}=(n-k+1)_m/n^m` (cited, PROVED ancestor fact) by the
substitution `j=k-m`, matching the target's derivation exactly. Verified
on **fresh sample points** disjoint from the target's own script `03`
grid (`n\in\{4,7,10,15\}` vs. target's `\{3,5,8,12\}`; fresh `γ`'s
`\{1/4,3/10,5/9,9/13\}` vs. target's `\{1/3,2/5,1/2,3/7\}`): exact
`Fraction` arithmetic, **0/16 mismatches** (`adv01`, CHECK 5). The
Vandermonde-type convolution `\sum_j\binom{j+m}m\binom{n-j}m=\binom{n+m+1}{2m+1}`
verified for the **extended** range `0\le m\le n\le12` (target checked
`\le8`): **0/91 mismatches** (`adv01`, CHECK 4). Both PROVED claims hold
under independent, extended-range re-derivation.

### (D) The truncation approximation `T(n,m)\to T_\infty(n,m)` (§3)

Re-implemented the coefficient extraction `T_\infty(n,m)=[y^m](1+y)^{n+m+1}/
(y+γ)^{m+1}` via a **different method** than the target's `sympy.series`
(this referee: `mpmath.taylor`, a numerically-evaluated Taylor expansion,
not a symbolic series manipulation). At the target's flagged badly-wrong
point, `n=20,m=6,γ=0.2`: relative error **`8.9799\times10^3`**,
independently matching the target's own claimed `\approx9\times10^3`
essentially exactly, via unrelated machinery (`adv02`). Independently
confirmed the approximation is excellent in the `m\ll n` regime that
actually matters (`n=100,m=3,γ=0.2`: relative error `4.7\times10^{-10}`).
**The badly-wrong-at-large-`m/n` and good-at-`m\ll n` characterization is
accurate and independently reproduced by a structurally different
computation.**

### (E) The swapped-sum's local decay rate `c(γ)=2(1-γ)/γ` (§4, script `07`)

Independently re-derived, by a **different symbolic route** than the
target's script `07` (which computes exact finite sums for `term_0,
term_1` then takes an exact limit; this referee instead used
`sympy.summation` fresh and cross-validated the same exact closed forms,
then additionally hand-derived the asymptotic expansion directly:
`term_0\to1/γ`, `term_1\to1/γ-2(1-γ)/(γ^2n)+O((1-γ)^n)`, giving
`\log(term_0/term_1)\approx2(1-γ)/(γn)` and hence `n\log(term_0/term_1)\to
2(1-γ)/γ` — a fully independent, hand-checkable derivation, not merely a
sympy re-run). **Exact symbolic match, difference simplifies to `0`**
(`adv01`, CHECK 6). Independently refitted the numeric local rate at
`n=6400,m=1` via fresh `mpmath` code (different code path than target's
script `06`): `γ=1/2\to2.000313`, `γ=1/5\to8.005004`, `γ=7/10\to0.857200`
— **matching the target's own reported `2.00031`, `8.00500`, `0.85720` to
every digit shown** (`adv02`). The "not proportional to `β`" ratio numbers
(`5.33` at `γ=0.5`, `1.88` at `γ=0.7`) independently confirmed by direct
hand calculation: `c(0.5)/β(0.5)=2/0.375=5.\overline3`;
`c(0.7)/β(0.7)=0.857143/0.455=1.884`. **PROVED claim confirmed exactly;
numeric corroboration confirmed exactly.**

### (F) The independent numerical cross-check of `T(γ)`/`C(γ)` via the swap route (§5)

Re-implemented `S_n'` via the swap route in fresh `mpmath` code
(different precision, `dps=25` vs. target's `dps=40`) and — deliberately —
a **different Richardson-extrapolation pair**, `n=1000,2000`, instead of
the target's `n=1600,3200`: `C_{\text{extrap}}=-0.325055` vs. the closed
form `C(0.5)=-0.325064`, `|diff|=9\times10^{-6}` (`adv02`) — consistent
with, and corroborating rather than merely repeating, the target's own
`6\times10^{-6}` at a different `n`-pair. This confirms the numerical
phenomenon is robust to the specific extrapolation points chosen, not an
artifact of the target's particular choice.

### Minor/cosmetic findings

1. **§4 prose vs. own script data (cosmetic).** "at `n=800`, `m=60` is
   still at `\approx0.2\%` of the peak value" — this referee's independent
   computation (`adv03`) gives `0.1082\%`, matching the target's **own**
   `04_m_sum_shape_probe.log` tabulated row (`term_m/max=0.0011`) exactly
   — the prose figure is off by a factor of `\approx1.8\times` from the
   front's own underlying data. Does not affect the qualitative claim
   (decay is slow, `m`-range needed grows with `n`), which is correct and
   independently confirmed.
2. See "Nuance on 'neither...caught it'" in (A) above.

No other discrepancy — cosmetic, moderate, or severe — was found anywhere
in the target's mathematical content.

---

## Overclaim/underclaim check on the document as a whole

The up-front VERDICT, §6 ("what remains open"), and §8 (Scorecard) are
mutually consistent and were checked against each other line by line: the
Charlier correction is labeled "PROVED" (correct — it is an exact algebraic
identity, independently reconfirmed here) and the bug-diagnosis is labeled
"STRONGLY EVIDENCED... not itself a new obstruction" (an appropriately
hedged label — "strongly evidenced" rather than "proved," since a literal
line-by-line diff of the predecessor's `.py` file was, per this front's own
mandate, not permitted; this referee's own reading of that file, which
*was* permitted, upgrades this to as-close-to-certain as this dispute can
get without re-executing the predecessor's own script, but the target's own
more cautious label was reasonable given its stated constraints). The EGF
divergence finding is labeled "SHOWN... not a proof no Charlier-based
technique can work" — correct, not overclaimed. The `T_\infty`
approximation is labeled "numerically supported only, not proved" —
correct. The swap-route numerics are labeled "evidence, not proof" —
correct. **No instance of overclaiming was found; the front is, if
anything, conservative** (e.g., it could have stated the bug-diagnosis
more strongly than "strongly evidenced," as this report's own deeper code
inspection now supports, but chose the more cautious label consistent with
not having read the predecessor's `.py` file itself — a self-imposed
discipline this referee verifies was actually honored, see governance
below).

---

## Scope, seed, and governance discipline

- **File-scope discipline.** `git status --porcelain` (read-only) at the
  repository root shows exactly **three** untracked entries in the whole
  repository: two pre-existing, unrelated, already-known stalled
  directories from a completely different sub-lineage (`conjecture2_direct_attempt/...`,
  the same ones the predecessor's own referee already flagged as
  pre-existing and untouched), and the target's own new
  `diagonal_2f0_sum_attempt/` directory. **Zero modified (tracked) files
  anywhere in the entire repository** — confirmed by the complete absence
  of any `M `-prefixed line in `git status --porcelain`'s output.
  `THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
  `TEST_QUEUE.yaml`, every ancestor/predecessor `ATTEMPT.md` and
  `adversarial/` file (including the predecessor's own
  `01_exact_hypergeometric_structure.py`, which this review read but did
  not modify), and every sibling directory are untouched.
- **Seed range.** `grep -rn "20260943" 05_DISCOVERY_LAB/` (run
  independently) finds: the `DECISION_LEDGER.yaml` reservation line itself
  (confirming `20260943000-20260943999` is officially reserved for "frente
  b" of this sub-chain, alongside sibling blocks `20260942000-999` and
  `20260944000-999` for fronts a/c); exactly one coincidental digit
  substring inside an unrelated, pre-existing `COSMOLOGY_WIDE_BINARIES`
  data file (matching the target's own disclosure); and every other match
  confined **exclusively** to files inside the target's own new
  `diagonal_2f0_sum_attempt/` directory (`01_baseline_2f0_identity.py`/`.log`,
  `02_charlier_identity_correction.py`/`.log`, and the target's own
  `ATTEMPT.md` prose) — confirmed via a directory-scoped `grep -rl`, no
  matches anywhere else. The two seeds actually drawn,
  `random.seed(20260943001)` (script `01`) and `random.seed(20260943002)`
  (script `02`), both fall inside the reserved block and are both
  disclosed in the target's own Seeds table — matches exactly.
- **No `git` command** of any kind appears in any of the target's seven
  scripts (checked via `grep -n "subprocess\|os\.system\|git "` across all
  `.py` files — zero matches); no `git` command other than the read-only
  `git status --porcelain` above was run by this referee.
- `DECISION_LEDGER.yaml` was grepped (read-only) and confirms the
  `DISC-DEC-134` seed-reservation context (the three-front block
  authorization) at the cited location.

---

## What this changes, precisely — recommended wording for the record

**The correction to Estágio 51 survives scrutiny and should be recorded.**
Recommended precise wording for the eventual `THEOREM.md` dated addendum
(subject to the orchestrating session's own editorial judgment):

> Estágio 51 reported that an attempted identification of `A_k(n,γ)` with
> the classical Charlier polynomial family "did not check out" under a
> naive parameter match (an exact, nonzero `-2γ` residual at `k=1`), and
> its own referee independently confirmed this as "a genuine,
> honestly-disclosed negative finding," further characterizing it as "a
> real, structural mismatch, not a sign flip away from working."
> **Both characterizations are corrected here.** Using the standard DLMF
> convention `C_n(x;a):={}_2F_0(-n,-x;;-1/a)`, the identity
> `A_k(n,γ)=(1-γ)^k\,C_k(k-n-1;(1-γ)n/γ)` is an EXACT algebraic identity
> (independently confirmed twice, by two separate hostile referee
> sessions, symbolically to `k=8` and numerically to 50+60 exact-`Fraction`
> spot checks). The reported `-2γ` residual, and the analogous
> higher-`k` residuals, are reproduced exactly by a specific, identified
> sign-convention bug in the predecessor's own `01_exact_hypergeometric_structure.py`
> (Part C): the function `Charlier_symbolic` computes the Pochhammer
> `(-k)_m` but never uses it, substituting the unsigned `\binom km` and
> thereby silently dropping the alternating sign required by
> `(-k)_m/m!=(-1)^m\binom km` — an effect algebraically identical,
> term-by-term, to using `+1/a` instead of DLMF's `-1/a`. The predecessor's
> own prose had already suspected "a sign/convention mismatch" in general
> terms but did not test or resolve it; the predecessor's dedicated referee
> reasoned that the increasingly complex residuals at `k=2,\ldots,6` ruled
> out a simple sign flip, but this reasoning does not hold — a single,
> consistent sign bug propagating through Pochhammer products of growing
> length produces exactly this pattern. **This does not change the
> bottom-line status of anything else in Estágio 51**: `C(γ)` remains
> entirely open, Gap 1 and Gap 3 are untouched, and the `n_0(γ)` reduction
> and its honest self-critical framing stand exactly as before — this is a
> narrow, verified correction to one sub-claim's *cause*, not its
> consequence.

**Nothing else in Estágio 51's verdict, or in `THEOREM.md`'s broader
state, requires correction as a result of this front or this review.**

---

## Summary assessment

This front's central, highest-stakes claim — correcting an
already-integrated, already-refereed result — survives the hardest
scrutiny this reviewer could bring to bear: independent re-derivation from
a primary-source characterization of the DLMF convention, extended-range
symbolic and numeric re-verification beyond both the target's and the
orchestrating session's own pre-dispatch checks, and, most importantly, a
literal transcription-and-comparison of the predecessor's own buggy code
against the target's reconstructed "wrong-sign" variant — which are shown
to be the exact same function, not a coincidentally-matching alternative.
A genuine secondary error on the *predecessor-referee* side of this
dispute (their specific "not a sign flip away from working" claim) was
additionally found and confirmed by this review, strengthening rather than
merely accepting the target's correction. The front's other claims —
the EGF/Cauchy-extraction structural obstruction, the double-sum
reformation and its Vandermonde-type sub-identity, the proved local decay
rate `c(γ)=2(1-γ)/γ`, the truncation-error characterization, and the
independent swap-route numerics — all independently reproduce, all are
appropriately (and if anything conservatively) hedged between "PROVED,"
"SHOWN (structural, not a proof of impossibility)," and "numerically
supported, not proved," and none of it is overclaimed. `C(γ)` for
`γ\in(0,1)` remains, correctly and honestly, entirely OPEN.

**Verdict: SOUND — ACCEPT for catalogue.**

---

## Files

| File | Content |
|---|---|
| `REFEREE_REPORT.md` | this document |
| `adv01_symbolic_charlier_and_bug_reconstruction.py`/`.log` | fresh symbolic re-derivation of the `2F0` identity (`k=0..8`), the DLMF Charlier identity (`k=0..8`), the wrong-sign residual formulas (`k=1..4`), a **literal transcription** of the predecessor's own buggy `Charlier_symbolic` function proven algebraically identical to the wrong-sign variant (`k=0..6`), the Vandermonde-type convolution (extended range `0<=m<=n<=12`), the double-sum swap identity on fresh sample points, and an independent symbolic (asymptotic-series-based, not exact-sum-based) re-derivation of `c(γ)=2(1-γ)/γ` |
| `adv02_numeric_crosschecks.py`/`.log` | independent `mpmath` re-implementation (fresh code, different precision and sample points) of: the swap-route Richardson extrapolation for `C(0.5)` at a different `n`-pair; the fitted local decay rate `c(n=6400,γ)` at the target's three sample `γ`; the `T(n,m)` vs `T_\infty(n,m)` truncation error at `n=20,m=6,γ=0.2` via a different extraction method (`mpmath.taylor` vs `sympy.series`) |
| `adv03_prose_number_spotcheck.py`/`.log` | independent check of the `n=800,m=60,\approx0.2\%` prose figure in §4 against fresh computation and against the target's own script `04` log (minor/cosmetic finding) |

No Millennium Problem claims anywhere in the target or this report; pure
combinatorial/asymptotic mathematics internal to this archive. No file
outside this front's own
`diagonal_2f0_sum_attempt/adversarial/` directory was created or modified
by this review — the predecessor's `01_exact_hypergeometric_structure.py`
was read in full, as the dispatch mandate required, but not modified. No
`git` command was run by this referee beyond the read-only
`git status --porcelain` reported above.
