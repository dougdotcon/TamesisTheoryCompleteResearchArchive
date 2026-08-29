# REFEREE REPORT — `H1-TRANSLATION-STRUCTURE-ATTEMPT` (wave 25, front c, `DISC-DEC-118`)

**Hostile independent referee.** Target:
`.../mclust_h1_validity_attempt/h1_translation_structure_attempt/ATTEMPT.md`.
Scope: pure combinatorial/asymptotic mathematics, `M-CLUST(b)` (Tree B of
`PROOF_DEPENDENCY_MAP.md`, node `PLATRESUM`) — standalone, unrelated to any
Millennium Prize Problem and unrelated to the archive's separate Tree A
(`U_alpha`/`u1/2`) line. This is the sixth consecutive wave (waves 20–25)
attacking the same `H1`/`(U1)`/`(U2)` gap in this exact sub-lineage.

**Method.** Every required background document was read in full before any
code was opened: `PROOF_DEPENDENCY_MAP.md`'s `PLATRESUM` node (full addenda
history, with particular attention to `DISC-DEC-088/091`, `DISC-DEC-113`,
`DISC-DEC-115`), and the immediate predecessor's full
`h1_post_correction_attempt/ATTEMPT.md` (the exact source of `K(y,t)`,
`K_A^raw`, `K_B`, `M_y`, `T_w`'s definitions). All four core new claims of
the target (the exponential-conjugation identity, the single-integral
reduction, the closed-form leading asymptotic, and the self-averaging/
Tauberian reformulation) were independently re-derived **by hand and from
scratch**, before any of the target's own `.py` scripts were opened. Only
after completing that independent derivation were the target's own scripts
read, for cross-checking. All adversarial scripts in this directory were
written fresh, without importing or copying code from the target or any
ancestor front.

---

## VERDICT

# SOUND WITH NAMED ISSUES

Two findings, both **LOW** severity, both about the *precision of prose/
framing*, not about mathematical correctness. Every substantive
mathematical claim examined — the exponential-conjugation identity, the
single-integral reduction, the closed-form leading asymptotic (including
the exact numeric coefficients this referee re-derived independently by
hand), and both self-disclosed bugs — was independently re-derived from
scratch and **confirmed correct**. The flagged `y=3000,h=1500` numerical
discrepancy is **conclusively resolved as a quadrature artifact**, not a
failure of the asymptotic (see Sec 3 below) — the true relative error
there is `~3.0e-4`, consistent with the `O(1/y)` prediction, not `99.6%`.
This referee directly reproduced the naive-quadrature failure mode itself
(via plain `scipy.integrate.quad`, no de-stiffening) and traced it to the
inner integral's thin peak being missed by roughly six orders of
magnitude, root-causing the discrepancy rather than merely re-asserting
the asymptotic from a different angle.

`H1`/`(U1)`/`(U2)` remain OPEN, exactly as the target states; nothing in
this report changes that. `phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and
the four-term asymptotic law of record are untouched by both the target and
this review.

---

## 1. Independent re-derivation of the exponential-conjugation identity and
the single-integral reduction (mandate items 1–2)

Working **only** from the predecessor's stated definitions
(`h1_post_correction_attempt/ATTEMPT.md` Sec 0, quoted verbatim):

```
(T_w f)(x) := int_0^infinity e^{-u^2/2-u(x+w)} f(x+u) du
K_A^raw(y,t) := int_t^y e^{-(y-w)/eps} S_{y-w} T_w dw
K_B(h)       := int_0^h e^{-v/eps} S_v dv,   (S_v f)(x):=f(x+v)
M_y          := multiplication-by-[(1-eps(x+y))/eps]
K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)
```

**`K_B` translation-invariance.** Trivial by inspection: `K_B(h)`'s only
free parameters are `h,eps`; substituting `y->y+a,t->t+a` leaves `h=y-t`
unchanged for every shift `a`. Confirmed formally
(`adversarial/adv01_from_scratch_identities.py`, Check 4).

**The exponential-conjugation identity.** Writing out `(T_w f)(x)` and
`e^{wx}*(T_0[e^{-w(.)}f])(x)` and subtracting their integrands:

```
e^{-u^2/2-u(x+w)} f(x+u)  -  e^{wx} * e^{-u^2/2-ux} * [e^{-w(x+u)} f(x+u)]
```

simplifies, by direct algebra (the `e^{wx}` and the `e^{-w(x+u)}`'s `e^{-wx}`
factor cancel `e^{wx}`; the remaining `e^{-wu}` combines with `e^{-uw}` from
the LHS's exponent), to **identically zero for every `u`** — re-derived by
hand and confirmed symbolically (`adv01`, Check 1). This is a **genuine,
exact algebraic consequence of the original `T_w` definition**, not a
silent redefinition: the identity is a trivial rewriting of the same
integral, nothing about `T_w`'s domain, action, or defining formula is
changed. **CONFIRMED.**

**The single-integral reduction.** Using `x':=x+y-w` (the shift `S_{y-w}`
composed before `T_w`), the exponent's `x'+w` simplifies to `x+y`,
independent of `w` (the `DISC-DEC-113` cancellation, re-confirmed
independently, `adv01` Check 2). Substituting `h':=y-w` into the raw
double integral (`dh'=-dw`; `w=t -> h'=h:=y-t`; `w=y -> h'=0`) gives,
**exactly**:

```
K_A^raw(y,t) f(x) = int_0^h e^{-h'/eps} [int_0^infinity e^{-u^2/2-u(x+y)} f(x+h'+u) du] dh'
```

matching the target's claimed formula exactly — re-derived independently
by hand and confirmed symbolically (`adv01`, Check 3), including the
outer-weight and integration-bounds transformation. **CONFIRMED**, a
correct change of variables, not an unjustified substitution.

---

## 2. Independent from-scratch re-derivation of the closed-form leading
asymptotic (mandate item 3, analytic part)

Starting from the single-integral reduction above and using the standard
Laplace/Watson expansion `∫_0^∞ e^{-uz}φ(u)du = φ(0)/z+φ'(0)/z^2+φ''(0)/z^3
+O(1/z^4)` (`z:=x+y`) applied with `φ(u):=e^{-u^2/2}f(x+h'+u)` (giving
`φ(0)=f(x+h')`, `φ'(0)=f'(x+h')`, `φ''(0)=f''(x+h')-f(x+h')`), then
integrating term-by-term against `e^{-h'/eps}dh'` over `[0,h]` and
integrating the `1/z^2` term **by parts** (`u=e^{-h'/eps}`,
`dv=f'(x+h')dh'`):

```
∫_0^h e^{-h'/eps} f'(x+h') dh' = e^{-h/eps}f(x+h) - f(x) + (1/eps)∫_0^h e^{-h'/eps}f(x+h')dh'
```

this referee independently obtained, **by hand, before reading any of the
target's own scripts**:

```
K(y,t) f(x)  =  [f(x) - e^{-h/eps} f(x+h)] / z  +  O(1/z^2),   z:=x+y
```

**exactly matching the target's claimed closed form.** As a further,
sharper cross-check, this referee also independently re-derived the
target's intermediate quantity `c(z):=(1-eps*z)*R(z)/eps` via the
Mills-ratio series `R(z)=1/z-1/z^3+3/z^5-...` (from the ODE `R'=zR-1`),
obtaining by hand `c(z) = -1 + 1/(eps*z) + 1/z^2 + O(1/z^3)` — matching the
target's Sec 4.2 formula **exactly, including the sign and the previously-
disputed `1/z^2` coefficient (`=+1`, not `0`)**. This is strong independent
confirmation that the closed form, and the intermediate algebra it is built
from, are correct — not merely "the right order," but the exact leading
coefficient. **CONFIRMED**, conditional (as the target states) on the
standing hypothesis `(B)` and the new auxiliary regularity hypothesis `(C)`
needed to control the Watson's-lemma remainder.

---

## 3. Numerical verification of the closed form, and resolution of the
`y=3000,h=1500` discrepancy (mandate item 3, numerical part)

All numerics below are from `adversarial/adv02_closed_form_mpmath.py`, an
independent, from-scratch `mpmath` implementation (arbitrary-precision
adaptive quadrature, with explicit de-stiffening substitutions — see file
header for why the raw double integral is genuinely stiff at large `z`, and
how this script avoids the stiffness).

**Route 1 — `f≡1`, entirely quadrature-stiffness-free.** For the constant
test function, `K(y,t)[1](x)` reduces to an *exact* closed form in the
special function `R(z)=sqrt(pi/2)*erfcx(z/sqrt2)` (re-derived by hand — see
script header), needing no 2D quadrature at all. Sweeping `z=x+y` from `50`
to `100000`, including **exactly** the flagged point `z=3000` (from
`y=3000,h=1500`): the true relative error of the closed form there is
`3.32e-5` (not `99.6%`), and `rel.err * z` converges cleanly to `eps=0.1`
as `z` grows (matching an independently-derived exact next-order
coefficient) — an entirely independent, stiffness-free confirmation that
the asymptotic is genuinely accurate at this parameter regime.

**Route 2 — general `f`, full de-stiffened double quadrature.** Two test
functions (`f=1/(1+x)`, `f=e^{-x/20}cos(x/10)`) were checked at:

- **(a) fixed `h` (`2` and `20`), growing `y` (`50,500,3000`):** relative
  error shrinks cleanly like `O(1/y)` in every case (e.g. `f=1/(1+x),h=2`:
  `0.0179 -> 0.00181 -> 0.000303` at `y=50,500,3000` — each roughly `10x`
  smaller as `y` grows `10x`, and `rel.err*z` stabilizes near a constant,
  confirming the predicted `O(1/z^2)`-absolute /`O(1/z)`-relative
  structure).
- **(b) proportional growth `h=y/2`** up to `y=3000` (`h=1500`): relative
  errors `0.00900 -> 0.000908 -> 0.000303` (`f=1/(1+x)`) and
  `0.000393 -> 0.0000485 -> 0.0000164` (`f=e^{-x/20}cos(x/10)`) at
  `y=100,1000,3000` — same `O(1/y)` rate, and (as the target's own Sec 5.4
  predicts) the `y=3000` value is **numerically indistinguishable** from
  the fixed-`h` case's value at the same `y` (`0.00030272` both ways for
  `f=1/(1+x)`), confirming the formula's insensitivity to `h` once
  `h/eps` is not small.
- **(c) THE EXACT FLAGGED POINT, `y=3000,h=1500,eps=0.1,x=0`,** run at
  **three independent working precisions** (`dps=20,30,40`) to confirm
  convergence: for `f=1/(1+x)`, all three give `K_exact=
  0.000333232426679...` to full agreement (`dps=20` vs `dps=40` differ by
  `6.6e-23`), giving **relative error `3.03e-4`** against the closed-form
  prediction — small, `O(1/y)`-consistent, and **numerically identical**
  to the value independently computed via a completely different `mpmath`
  method by the target's own `s07_uniformity_in_h_check.py`
  (`rel.err=0.0003027`, read from that script's own log) — two
  independently-written `mpmath` implementations (this referee's
  de-stiffened-substitution route, and the target's own direct
  nested-quadrature route with `U_CUTOFF=15`) agree to 4 significant
  figures. `f=e^{-x/20}cos(x/10)` gives an even smaller relative error,
  `1.64e-5` (`dps=20` vs `dps=40` differ by `1.3e-22`, again fully
  converged).

**Root-causing the flagged `99.6%` scipy result (Part 3 of `adv02`).**
This referee additionally reproduced, in plain `float64` via
`scipy.integrate.quad` with **default tolerances and no de-stiffening
substitution or explicit breakpoints** — i.e. exactly the kind of "quick,
naive" computation the mandate describes — the same double integral at the
flagged point. The result is a **direct, dramatic reproduction of the root
cause**: naive `scipy.integrate.quad(integrand, 0, np.inf)` on the inner
`u`-integral, called at each outer-quadrature node with no hint of where
the mass lies, returns `A_naive = 4.70e-11` — versus the correct,
de-stiffened value `A = 3.05e-5` from this same script's Part 2 (Sec 3
above) — **off by roughly six orders of magnitude**, because scipy's
default node placement over the semi-infinite interval never samples
close enough to `u≈1/z≈3.3e-4` to detect the genuine spike there, and (since
both its low- and high-order estimates agree on the — wrongly sampled —
near-zero result) its own convergence check is satisfied without any
warning. This propagates to `M_y*A_naive ≈ -1.41e-7` (versus the correct
`M_y*A ≈ -0.0912`), so the naive computation adds an essentially-unchanged
`K_B≈0.0916` to a near-zero `M_y*A`, producing `K_naive(y,t)f(0) ≈ 0.0916`
— **a relative error of `27369%`** against the closed-form prediction
(`2.74e4`, i.e. off by roughly `1000x` in absolute terms), even more
extreme than the mandate's originally-flagged `99.6%`, but the **exact same
qualitative failure mode**: `K(y,t)f(x)` is a **near-total cancellation**
between `M_y*A` and `K_B(h)f(x)`, both individually `O(1)` in magnitude
(`M_y*A≈-0.091`, `K_B≈+0.092` at the correct, de-stiffened values), whose
**sum** is `O(1/z)≈3.3e-4` — three orders of magnitude smaller than either
piece. Any quadrature routine that even partially mishandles the inner
integral's thin peak corrupts the `O(1)` piece `M_y*A`, and after the
near-total cancellation that corruption survives as an `O(1)`-sized
**absolute** error in the final `O(1/z)` result — i.e. an apparent
`~100%`-or-worse *relative* error in `K(y,t)` itself, matching (and here,
exceeding) the originally-flagged symptom. Full printed values in
`adversarial/adv02_closed_form_mpmath.log` (Part 3).

**CONCLUSION on the flagged discrepancy: definitively a numerical
quadrature artifact of the original quick scipy check, not a real failure
of the closed-form asymptotic.** The asymptotic's true behavior at
`y=3000,h=1500` is unremarkable — a modest, `O(1/y)`-consistent relative
error around `3e-4`, confirmed by three independent routes (this referee's
`f=1` exact route, this referee's de-stiffened general-`f` `mpmath` route,
and the target's own independently-coded `mpmath` route in `s07`).

---

## 4. The self-averaging / Tauberian reformulation (mandate item 4)

The derivation in the target's Sec 6.1 was independently re-checked
step-by-step. Substituting the closed form (with `z=x+y` **fixed**
throughout the `t`-integration, since `z` does not depend on `t` — only
`h=y-t` does) into the exact `(VOLTERRA-Phi)` equation and integrating over
`t∈[0,y]`:

```
Phi_y(x) = g_y(x) + (1/z)A(y) - (1/z)[bounded term <= eps*sup|Phi|] + y*O(1/z^2)
A(y) := int_0^y Phi_t(x) dt
```

Since `g_y(x)=e^{-y/eps}->0`, the bounded term divided by `z` `->0`, and
(**given** the flagged uniformity-in-`t` assumption, item 4 of the target's
own Sec 7) `y*O(1/z^2) ~ O(1/y) -> 0`, this gives `Phi_y(x) - A(y)/z -> 0`
— the self-averaging identity, correctly and rigorously derived from the
stated hypotheses.

**One LOW-severity finding on this derivation's framing** (Finding 1
below): the identity `Phi_y(x)-A(y)/z->0` is derived here **unconditionally**
(given `(B),(C)`, and `t`-uniformity) — it does **not** itself depend on
whether `(U1)` (i.e. `Phi_t(x)` actually converging) holds or not. The
document's own Sec 6.2 correctly recognizes the easy, classical direction
("if `Phi_t(x)->L(x)`, Cesàro convergence of the running average follows
automatically") and correctly identifies the missing Tauberian direction —
but its boldface Sec 6.1 claim, and the scorecard/executive-summary
repetitions of it, that "`(U1)` **is equivalent to** [the self-averaging
identity]" is imprecise if read literally: a statement cannot be
"equivalent to" another statement that has *already* been established as
unconditionally true while itself remaining an open question. The
technically precise statement — fully consistent with, and immediately
recoverable from, the document's own Sec 6.2/6.3 discussion — is that
`(U1)` is equivalent to **the Cesàro-type running average `A(y)/(x+y)`
itself converging** (a standard real-analysis fact once the *unconditional*
self-averaging bridge is in hand: two sequences differing by `o(1)`
converge to the same limit iff either one does), with the self-averaging
identity serving as the (correctly, rigorously proved) bridge to that
restatement, not as the thing itself that is "equivalent to" `(U1)`. See
Finding 1.

**The Tauberian missing ingredient** (Sec 6.3) is honestly and specifically
named: an oscillation bound on `Phi` itself (not `Psi`, for which
`(star-star)` already exists, correctly cited from
`h1_energy_estimate_attempt` and re-confirmed against that document's own
text) of the *relative*-step form the classical continuous-Cesàro
Tauberian theorem needs, plus formal verification the classical theorem's
hypotheses transfer to this two-variable-PDE setting. Both are correctly
and specifically flagged as **not attempted**, not silently assumed or
hand-waved. **No overclaim of closure anywhere** — Sec 7 item 1 states
plainly "`(U1)`/`(U2)`/`H1` are not closed," consistent throughout the
scorecard and executive summary.

---

## 5. The two self-disclosed bugs (mandate item 5)

Both independently reconstructed from the mathematical description alone
(`adversarial/adv03_selfcaught_bugs_reconstruction.py`), without taking the
target's account on faith:

**Bug 1 (Sec 4.2, `s02`):** the described wrong claim (`c(z)~-1-1/(eps*z)`,
sign flipped, and `1/z^2` term wrongly claimed to vanish) was reconstructed
and checked against the independently-confirmed correct series
`c(z)=-1+1/(eps*z)+1/z^2+...`: the wrong claim's sign is indeed wrong, and
its "`1/z^2` vanishes" claim is indeed false (`zm2=1≠0`) — **genuine, real
error, correctly diagnosed, correctly fixed**. One documentation-precision
note: the executive summary states both bugs were "caught by the front's
OWN symbolic verification scripts failing their own assertions," but
Sec 4.2's own detailed account says this bug was **prose-only** — the
`sympy` computation was correct throughout, and the error was caught by
noticing the commentary contradicted the script's own already-correct
printed output, with the corroborating `assert` statements **added after**
the fix (not the mechanism that caught it). This is a minor inaccuracy in
how the executive summary characterizes Bug 1's catch mechanism
specifically (Bug 2's catch mechanism, below, genuinely does match the
"assert failure" description). See Finding 2.

**Bug 2 (Sec 4.3, `s05`):** the described wrong scaling
(`(1-eps*z)/eps ~ -1/(eps*delta)`, an extra spurious `1/eps` factor,
`delta:=1/z`) was reconstructed and checked: using the wrong scaling, the
`K_B(h)f(x)`-proportional coefficient does **not** cancel — it evaluates to
`(eps-1)/eps^2 = 1/eps - 1/eps^2`, exactly matching the target's own
description ("manifestly nonzero and dimensionally inconsistent") — while
the corrected scaling gives an **exact** `0`, matching both the target's
own final result and this referee's independent by-hand derivation (Sec 2
above) via the `B0/eps - B1` integration-by-parts route. **Genuine, real
error, correctly diagnosed via a genuine assert failure (matching the
described catch mechanism), correctly fixed.**

Neither bug is fabricated post-hoc, and neither survives into the final
published closed form, which this referee independently confirmed is
correct both analytically (Sec 2 above) and numerically (Sec 3 above).

---

## 6. Hypotheses `(B)` and `(C)` (mandate item 6)

Hypothesis `(B)` ("`Phi, Psi` bounded") is quoted verbatim, identically, in
both the predecessor's (`h1_post_correction_attempt`) and the target's
Sec 0, and matches the wording in `PROOF_DEPENDENCY_MAP.md`'s
`DISC-DEC-096/100` addendum ("hipótese de limitação padrão `(B)` já usada
em toda a linhagem") — **correctly cited from its actual source, not
altered.**

Hypothesis `(C)` ("an auxiliary Lipschitz-type regularity hypothesis...on
the function `K(y,t)` acts on") is explicitly introduced as **NEW** by this
front (Sec 4.4: "an auxiliary hypothesis `(C)`, beyond the standing `(B)`")
and explicitly, honestly disclosed as **not independently proved** for the
actual `Phi`/`Psi` of the system (Sec 7 item 3: "assumed, consistent with
how `(B)` itself is a standing, not independently proved, hypothesis
throughout this entire lineage"). **No silent upgrade to "already proved
elsewhere"** — this is exactly the honest disclosure the mandate asks to
confirm. **CONFIRMED correctly and honestly handled.**

---

## 7. Scope and seed discipline

`adversarial/adv04_scope_seed_discipline.sh` (full output in
`adv04_scope_seed_discipline.log`) confirms:

- **No sibling directory modified.** `h1_volterra_attempt/`,
  `h1_post_correction_attempt/`, `h1_energy_estimate_attempt/`, and
  `mclust_h2_validity_attempt/` show **no files with a 2026-08-29 (or
  later) mtime** — clean.
- **No `git` command** appears in any of the target's own `.py` scripts.
- **The reserved seed range `20260931000-20260931999`** appears in the
  archive **only** in `DECISION_LEDGER.yaml`'s own `DISC-DEC-118`
  reservation line, the target's own self-referential prose (Sec 0, Sec 9),
  and one unrelated front's own audit log quoting the full seed-block list
  for its own documentation purposes — **never as an actual random-seed
  call**. No `seed`/`SeedSequence`/`random` usage anywhere in the target's
  scripts, consistent with the claim that no randomness was needed.
- **`THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`** do show
  2026-08-29 mtimes, but these are attributable to the **wave-25
  orchestration and other, already-integrated wave-25 fronts** (confirmed:
  `DECISION_LEDGER.yaml`'s `DISC-DEC-118` entry itself, which *authorizes*
  this wave, and `DISC-DEC-119`'s already-integrated addendum in
  `PROOF_DEPENDENCY_MAP.md` for a *different* wave-25 front), **not** to
  `h1_translation_structure_attempt` — `PROOF_DEPENDENCY_MAP.md` does
  **not yet** mention `H1-TRANSLATION-STRUCTURE-ATTEMPT` anywhere,
  confirming no premature integration of this front's own results has
  occurred.
- `DISC-DEC-118`'s mandate text in `DECISION_LEDGER.yaml` (front c) matches
  the target's own stated mandate verbatim in substance (the translation-
  invariance-failure angle, as the candidate source of the exponential
  content).

---

## 8. Findings

**Finding 1 (LOW).** The claim "`(U1)` is equivalent...to the
self-averaging identity" (Sec 6.1, repeated in the executive summary item 4
and the Sec 8 scorecard) is imprecise if read literally: the self-averaging
identity `Phi_y(x)-A(y)/(x+y)->0` is derived **unconditionally** (given
`(B)`, `(C)`, and `t`-uniformity of the error term) — it does not itself
depend on `(U1)` holding, so it cannot be "equivalent to" an open question
in the strict logical sense. The technically correct statement, fully
consistent with and easily recoverable from the document's own honest
Sec 6.2/6.3 discussion, is that `(U1)` is equivalent to the Cesàro running
average `A(y)/(x+y)` itself converging, with the (unconditionally proved)
self-averaging identity serving as the bridge to that restatement. This
does **not** affect the substantive content, the Tauberian-gap diagnosis,
or the non-closure verdict — Sec 7 item 1 already states plainly that
`(U1)` is not closed and the self-averaging identity is "not a proof of
it." Fix: rephrase the Sec 6.1 boldface claim (and its two echoes) to say
`(U1)` is equivalent to Cesàro-mean convergence of `Phi_t(x)`, with the
self-averaging identity as the proved bridge — not to say `(U1)` is
"equivalent to" the self-averaging identity itself.

**Finding 2 (LOW).** The executive summary states both self-caught bugs
were "caught by the front's OWN symbolic verification scripts failing
their own assertions." This is accurate for Bug 2 (`s05`, Sec 4.3) but not
for Bug 1 (`s02`, Sec 4.2), whose own detailed account correctly says it
was a prose-only error, caught by noticing the commentary contradicted the
script's own already-correct printed series output — the corroborating
assertions were added *after* the fix, as a hardening measure, not as the
original catch mechanism. Purely a documentation-precision point; the
underlying mathematics of both bugs, their diagnoses, and their fixes are
all independently confirmed correct (Sec 5 above). Fix: qualify the
executive summary's claim to note Bug 1 was prose-only / caught by
cross-reading rather than by an assertion failure.

No other findings. In particular: no fabricated results; no inconsistency
between the executive summary and the detailed derivation beyond Finding 1;
no unearned claim of closure anywhere (`H1`/`(U1)`/`(U2)` are stated as OPEN
consistently in the executive summary, Sec 6.2, Sec 6.3, Sec 7, and the
scorecard); the operator-norm-vs-pointwise-in-`f` scope clarification
(Sec 4.4) is correct and does not contradict `DISC-DEC-113/115`; the
"genuine exponential content" discussion (Sec 6.4) is honestly and
correctly labeled a plausibility synthesis, not a proof.

---

## 9. Files in this directory

| file | role |
|---|---|
| `adv01_from_scratch_identities.py`/`.log` | independent symbolic re-derivation (sympy) of the exponential-conjugation identity, the `x'+w=x+y` cancellation, the single-integral reduction of `K_A^raw`, and `K_B`'s trivial translation-invariance — written entirely from the predecessor's stated definitions, before opening any target script (Sec 1 above) |
| `adv02_closed_form_mpmath.py`/`.log` | independent from-scratch `mpmath` numerical verification of the closed-form leading asymptotic: an `f≡1` quadrature-free exact route, a de-stiffened general-`f` double-quadrature route (fixed-`h`/growing-`y`, proportional `h=y/2`, and the exact flagged `y=3000,h=1500` point at three working precisions), and an explicit reproduction + root-cause of the flagged scipy discrepancy via naive float64 `scipy.integrate.quad` (Sec 3 above) |
| `adv03_selfcaught_bugs_reconstruction.py`/`.log` | independent symbolic reconstruction of both self-disclosed bugs' wrong versions, confirming each genuinely produces the described incorrect/inconsistent result, and that the corrected versions match this referee's own independent derivation (Sec 5 above) |
| `adv04_scope_seed_discipline.sh`/`.log` | scope/seed/governance-file discipline audit (Sec 7 above) |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was modified. No `git`
command was run. No claim of progress on any Millennium Prize Problem
appears anywhere in this report — `M-CLUST(b)` is a standalone
combinatorial/asymptotic object, as stated throughout the target and its
required reading.
