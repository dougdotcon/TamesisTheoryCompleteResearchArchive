# REFEREE REPORT — `H1-ENERGY-ESTIMATE-ATTEMPT`

**Target document:** `h1_energy_estimate_attempt/ATTEMPT.md` (wave 22, front b,
`DISC-DEC-096`). **Referee status:** independent, hostile/adversarial; no
`.py` file from this front or any front in its lineage
(`mclust_h1_validity_attempt`, `mclust_h2_validity_attempt`,
`mclust_plateau_abstract_real_gap_attempt`, `plateau_resummation_attempt`,
or any further ancestor) was opened, read, or imported at any point. Every
check below was built fresh from the mathematical prose of the target
document and the required-reading ancestors, in the referee's own code
(`v01`–`v05` in this directory), with the referee's own variable names,
own numerical strategy, and own choice of test points (deliberately
different from every point tested by the target or any predecessor).

**Reserved seed range for this referee:** `20260913000-20260913999`
(grep-confirmed to appear only in `DECISION_LEDGER.yaml` and
`TEST_QUEUE.yaml` reservation lines, unused elsewhere). **No randomness was
needed anywhere in this review** — every check is exact symbolic reasoning
(`sympy`) or deterministic arbitrary-precision (`mpmath`, `dps` 30–150)
computation, so the reserved range remains entirely unused, consistent with
every front in this lineage.

---

## VERDICT

# **SOUND — WITH NAMED ISSUES (ACCEPT for catalogue)**

The target's central claims all check out under independent re-derivation:
the new exact identity `(BB-Psi')` is correctly derived from the
Growth-Exclusion Lemma applied to `(E1)`, and is independently corroborated
numerically (fresh series solver, genuinely different numerical route from
the target's own `e02`, agreement to `2.6e-8`–`2.7e-10` at two
independently-chosen `(s,g)` points — see §2 below); the global-in-`x`
oscillation bound `(star-star)` is correctly derived (its key algebraic
identity, `delta_x - (x+y1)*delta = h*Psi(x,y2) - int_{y1}^{y2}Phi`, was
re-derived from scratch and matches exactly) and is confirmed never
violated at every one of the referee's own independently-chosen
`(y1,y2,x)` triples; the Lipschitz-`<=1` chain in §8.2 is algebraically
correct at every step; `R(z)<=1/z` and the shift identity
`R(z)=sqrt(pi/2)*erfcx(z/sqrt2)` both check out symbolically and
numerically. No claim of unconditional closure is made anywhere in the
target, and no Millennium Prize Problem framing appears anywhere (§7 below)
— the "honest non-closure" tier claimed is the correct one.

Three named issues were found, none of which changes the tier or overturns
any load-bearing claim (see §6 for full detail and severity):

- **N1 (MODERATE).** The claimed connection to `plateau_resummation_
  attempt`'s Borel-resummation obstruction (target §6.2, citing that
  document's §2.3) **misidentifies which limit that obstruction concerns**.
  The predecessor's Borel-Laplace attempt resums the `t0` (`=g`, at FIXED
  `c`) series — i.e. it is about the **same** `y->infinity` direction the
  target's own §6.2 is analyzing, not "the `eps->0` limit" as the target
  states. The two obstructions are also mechanistically different kinds of
  failure (super-fast Taylor-coefficient growth defeating classical
  Borel-1 summability of a specific series, vs. the fully generic fact
  that any Watson/Laplace asymptotic expansion of a smooth kernel is blind
  to exponentially-small corrections). The target's framing — "an exact
  structural echo... now identified for the first time in the `y->infinity`
  limit instead" — overstates both the novelty and the depth of the
  analogy, and gets the predecessor's limit wrong.
- **N2 (LOW).** Target §5.1's displayed intermediate formula
  `delta(x) = int_0^inf e^{-u^2/2-u(x+y1)} f(x+u) du` is missing a leading
  minus sign relative to a correct application of the Growth-Exclusion
  Lemma (confirmed by two independent derivations here: the Leibniz-rule
  route and an integrating-factor route). Non-consequential: the very next
  step takes `|delta(x)|`, and `|-Z|=|Z|`, so the final bound `(star-star)`
  is unaffected.
- **N3 (LOW).** Target §8.2's tightness claim — "essentially TIGHT
  (saturated as `x->0`)" — names the wrong asymptotic regime. The quantity
  actually being bounded, `y*R(x+y)`, is maximized over `x` at `x=0` for
  every fixed `y` (confirmed numerically), but that maximum value is close
  to `1` only when `y` itself is large (`y*R(y)|_{y=1}~=0.656`,
  `y*R(y)|_{y=100}~=0.9999`) — genuine saturation requires `y->infinity`,
  not `x->0` at some arbitrary fixed finite `y`. The stated CONCLUSION
  (Lipschitz constant is exactly `1`, not `<1`, sup approached but not
  attained) is correct; only the specific regime cited for why is
  imprecise.

No arithmetic or algebraic error was found that affects any reported
number, bound, or the front's own stated verdict ("`H1` remains
ABERTO/OPEN"). All five "what remains open" items and all "self-caught
issues" disclosures in the target are consistent with what this review
independently found.

---

## 1. What was read (required reading, in full, per the mandate)

- `PROOF_DEPENDENCY_MAP.md` §2 (Tree B) in full, including every dated
  addendum under `PLATRESUM` (waves 17–21) and the `FLOORH2` node.
- `plateau_resummation_attempt/ATTEMPT.md` in full (§4 matched-asymptotics
  derivation, §4.5 exact `H1`/`H2` statement, §2.3 the Borel-resummation
  obstruction, §7 identification/exclusion attempts, VERDICT UP FRONT).
- `mclust_h1_validity_attempt/ATTEMPT.md` in full (the exact `(E1)`/`(KEY)`/
  `(E2)` system, the Watson-concentration lemma, the precise statements of
  `(U1)`/`(U2)`, the `(ODE-F)` fact, the `(x,c)` uniformity grid of §4).
- `mclust_h2_validity_attempt/ATTEMPT.md` in full (the Growth-Exclusion
  Lemma, §2, and its proof).
- The target document, `h1_energy_estimate_attempt/ATTEMPT.md`, in full,
  in prose, before any derivation or code (per the mandate).

No `.py` file belonging to any of these fronts, or to any further ancestor
(`floor_h2_b1_full_closure_attempt`, `floor_closed_form_attempt`, etc.),
was opened at any point in this review.

---

## 2. Independent re-derivation of `(BB-Psi')` (target §2)

**Symbolic** (`v01_symbolic_checks.py`, Parts A–B; log: `v01_symbolic_
checks.log`):

- Re-derived the Growth-Exclusion Lemma completely from scratch, via TWO
  independent routes: (i) the Leibniz-rule construction (matching the
  target's own derivation route), checked symbolically for two concrete
  sources `f(t)=1` and `f(t)=t` (residual exactly `0` both times); (ii) an
  independent integrating-factor derivation (`mu(x)=e^{-(x^2/2+xy)}`,
  `d/dx[mu*u]=mu*f`, integrate to `X->infinity`, use boundedness to kill
  the `mu(X)u(X)` term) that does **not** reuse the Leibniz construction at
  all — both routes agree exactly on the Lemma's stated formula, including
  its sign.
- Confirmed the `t=x+u` exponent-simplification algebra used to pass from
  the Lemma's output to `(BB-Psi')` is EXACT: `sympy.simplify` of
  `[x^2/2+xy] - [(x+u)^2/2+(x+u)y] - (-u^2/2-u(x+y))` returns `0`.
- Conclusion: the target's §2.1 derivation of `(BB-Psi')` — apply the
  Growth-Exclusion Lemma to `(E1)` (with `f(x):=-I(x,y_1)`, `y_1` as
  parameter), then substitute `t=x+u` — is **algebraically correct at
  every step**, and the sign bookkeeping in THIS particular application
  (§2.1, unlike §5.1 — see N2) is done correctly (the extra minus sign
  from `f(x)=-I(x,y)` correctly cancels the Lemma's own leading minus,
  giving the stated positive-kernel form).
- The unscaled conversion (target §2.2) was also independently re-derived
  by hand (not scripted, since it is a direct one-line substitution
  `x=s*sqrt(c), y=g*sqrt(c), u=sqrt(c)*v`): confirmed to reproduce the
  target's `(BB-Psi'-unscaled)` exactly.

**Numerical** (`v03_series_solver.py` + `v04_identity_check.py`; logs:
`v03_series_solver.log`, `v04_identity_check.log`):

Built a fresh, from-scratch general-`s` `(P,Q)`-family series solver,
independently re-deriving the descending-recursion/`kappa`-pinning
bounded-branch ODE-solve algorithm by hand from the prose of
`plateau_resummation_attempt/ATTEMPT.md` §1.1 (worked out completely
independently before any code was written — see the module docstring of
`v03_series_solver.py` for the full by-hand derivation, including the
observation, verified in code, that `b_1` itself falls out of the SAME
general ODE-solve routine applied at `k=1` with `a_0=1,b_0=0`, an internal
consistency check "for free" that is not present in the target's own
approach). **Validated 7/7 against the SAME published anchors used across
this entire lineage** at `c=1000,K=220,dps=150`:

| quantity | this review's value | published anchor | reldiff |
|---|---|---|---|
| `a2(0)` | `520316.63648803005507` | `520316.636488030055067` | `5.3e-22` |
| `a3(0)` | `-180730907.62850806677` | `-180730907.628508066766` | `1.2e-21` |
| `a4(0)` | `47146963944.137885921` | `47146963944.1378859211` | `9.0e-22` |
| `b1(0)` | `39.633272976060110133` | `sqrt(pi*1000/2)` (exact) | `0` |
| `b2(0)` | `-20816.636488030055067` | `-20816.6364880300550667` | `1.2e-21` |
| `Phi(0,0.002)` | `0.15850014574730848424` | `0.158500145747308484241` | matches |
| `Phi(0,0.05)` [plateau] | `0.037761598340212618824` | `0.0377615983402126188243712...` | `2.2e-21` |

Then tested `(BB-Psi')` at **two `(s,g)` points chosen independently of
every point tested by the target or any predecessor** (`s=0.03,g=0.07` and
`s=0.15,g=0.06`, at `c=1000`), computing `Psi` two structurally different
ways: (a) directly, from the validated `b_k(s)` series; (b) via the
renewal integral, with the inner integral `J(s',g)=int_0^g Phi(s',g')dg'`
evaluated as a finite sum of the SAME validated `a_k` series and the outer
`v`-integral done by the referee's own `mpmath.quad` (Gauss–Legendre, own
substitution `w=c(s+g)v` rescaling the kernel's decay to `O(1)`, own
breakpoints — a different numerical strategy from the target's own `e02`
quadrature approach). An explicit `K`-vs-`K+40` convergence check is run
before trusting any number (this caught, in the referee's own scratch
work, that `K=220` — sufficient for the `s=0` anchors — was NOT yet
converged at `s=0.03,g=0.07`; `K=260` vs `K=300` agree to 23+ digits and
was used for the final numbers below):

| `s` | `g` | `Psi` (direct series) | `Psi` (renewal integral, own quadrature) | rel. diff |
|---|---|---|---|---|
| 0.03 | 0.07 | `0.0206193210660027783071438427597` | `0.0206193205229798398764582793222` | `2.6e-8` |
| 0.15 | 0.06 | `0.0063256141880134521032211351806` | `0.00632561418628267663255446683879` | `2.7e-10` |

**Two structurally independent computation routes agree to 8–10 digits at
two independently-chosen points.** This is not as sharp as the target's
own 23–37 digit agreement (the target invested far more in `(K,dps)`
calibration and quadrature precision than this review's time budget
allowed), but per the mandate's own relaxed bar ("even a few digits of
agreement... via a genuinely different route... would meaningfully
corroborate the claim") this is a solid, independent corroboration of
`(BB-Psi')` — via a route that is genuinely different from a plain
re-implementation of the target's own described computation (different
quadrature substitution, different breakpoint strategy, different
`(K,dps)` sizing, different test points), not merely a rerun of the same
numbers.

**Finding: `(BB-Psi')` is CORRECT**, both algebraically (symbolic
re-derivation, two independent routes) and numerically (independent series
solver + independent quadrature).

---

## 3. Independent re-derivation of the oscillation bound (target §5)

**Symbolic** (`v01_symbolic_checks.py` Part C; log as above):

Re-derived the key identity from scratch, using abstract `sympy.Function`
objects `Psi(x,y)`, `I(x,y)` satisfying `(E1)` at `y=y1` and `y=y2`
independently (NOT copying the target's own presentation — built the
identity fresh from `(E1)` applied twice and the definition
`delta:=Psi(x,y2)-Psi(x,y1)`):

```
delta_x(x) - (x+y1)*delta(x)  =  h*Psi(x,y2) - [I(x,y2)-I(x,y1)]
```

`sympy.expand` of [own re-derivation] `-` [target's claimed RHS,
`(x+y1)*delta + h*Psi(x,y2) - (I(x,y2)-I(x,y1))`] returns exactly `0` —
**the target's Sec5.1 identity is EXACTLY correct**, confirmed by an
independent re-derivation, not merely re-transcribed.

Applying the Growth-Exclusion Lemma to this identity (parameter `y1`) and
bounding `|f(x+u)|<=h*K` gives `|delta(x)|<=h*K*R(x+y1)<=h*K*R(y1)<=hK/y1`
exactly as the target states — **except** for a sign discrepancy in the
target's own displayed intermediate formula (see N2, §6 below): applying
the Lemma correctly (confirmed via TWO independent routes, matching Part A
above) gives `delta(x) = -int_0^inf e^{-u^2/2-u(x+y1)} f(x+u) du`, with a
leading minus sign the target's Sec5.1 formula omits. This does not affect
the final bound, since the next step takes `|delta(x)|`.

The chain `R(z)<=1/z` was re-proved from scratch (own proof, matching the
lineage's own cited fact): for `t>=z>0`, `e^{-t^2/2}<=(t/z)e^{-t^2/2}`, so
`int_z^inf e^{-t^2/2}dt <= (1/z)int_z^inf t e^{-t^2/2}dt = e^{-z^2/2}/z`,
giving `R(z)=e^{z^2/2}int_z^inf e^{-t^2/2}dt <= 1/z`. Confirmed
numerically at 8 values of `z` from `0.1` to `50` (`v02_numeric_checks.py`,
Part F2) — holds with strictly positive margin at every tested `z`.

**Numerical** (`v05_oscillation_bound_check.py`; log:
`v05_oscillation_bound_check.log`):

Using the same validated series solver, tested the bound at THREE
`(g1,g2,x)` triples chosen independently of the target's own grid
(`c=1000` rather than the target's `c=100`; `g1,g2 in
{0.02,0.035,0.045,0.055,0.06}` rather than the target's `{0.06,0.10,0.18,
0.30}`), with an explicit `K`-convergence check at every triple before
trusting any number. **The bound was never violated at any tested point**:

| `g1` | `g2` | `sup_s |Delta Psi|` | bound `h*K*R(y1)` | ratio |
|---|---|---|---|---|
| 0.02 | 0.035 | `3.42e-11` | `0.0289` | `1.18e-9` |
| 0.02 | 0.06 | `3.42e-11` | `0.0771` | `4.44e-10` |
| 0.045 | 0.055 | `8.41e-17` | `0.0127` | `6.60e-15` |

(The ratios here are far looser than the target's own `~1e-3`–`1e-4`
because these `g`-values are all already deep in the `c=1000` plateau
regime — `Phi(0,g>=0.02)` has essentially converged to its plateau — so
`|Delta Psi|` is extremely small at every tested point; this is a
consequence of this review's own choice of test region, not evidence
against the target's own tighter numbers, which were measured closer to
the transition region at a smaller `c`.)

**Finding: the oscillation bound `(star-star)` is CORRECT**, both
algebraically (own re-derivation of the key identity matches exactly) and
numerically (never violated, own test points).

---

## 4. Lipschitz-chain re-derivation (target §8.2)

Re-derived every step of `|DeltaPsi(x,y)| <= y*||DeltaPhi|| * R(x+y) <=
(y/(x+y))*||DeltaPhi|| <= ||DeltaPhi||` independently
(`v01_symbolic_checks.py` Part F):

1. `|DeltaI(x,y)|<=y*||DeltaPhi||` — elementary (`|int_0^y g|<=y*sup|g|`).
2. `|DeltaPsi(x,y)|<=y*||DeltaPhi||*R(x+y)` — triangle inequality applied
   to `(BB-Psi')`, plus step 1.
3. `y*R(x+y)<=y/(x+y)` — direct substitution of `R(z)<=1/z` (proved §3).
4. `y/(x+y)<=1` for `x>=0` — trivial.

**All four steps confirmed correct.** The claimed Lipschitz constant `<=1`
for the `Phi -> Psi` sub-map is therefore correct.

**Tightness investigation** (`v02_numeric_checks.py` Part G — own
addition, not requested verbatim by the target but directly relevant to
scrutinizing the target's own tightness claim): computed `y*R(x+y)`
(the actual bounded quantity, before the further `R(z)<=1/z` relaxation)
over a grid of `(x,y)`. Found:

- `y*R(x+y)` is strictly DECREASING in `x` for every fixed `y` (confirmed
  at `y=1` and `y=100`), so its supremum over `x` is attained at `x=0` —
  but that supremum value, `y*R(y)`, is close to `1` ONLY for large `y`
  (`y*R(y)|_{y=1}=0.6557`, `y*R(y)|_{y=10}=0.9903`,
  `y*R(y)|_{y=100}=0.99990`, `->1` as `y->infinity`).
- At `y=1` fixed, `y*R(x+y)` ranges from `0.3046` (`x=2`) to `0.6557`
  (`x=0`) — nowhere close to `1`, even in the limit `x->0`.
- At `y=100` fixed, `y*R(x+y)` is already `>0.98` for every tested `x`,
  including `x=2`.

This confirms the true saturation mechanism is `y->infinity` (with `x`
fixed at whatever value maximizes the bound for that `y`, e.g. `x=0`), not
`x->0` at an arbitrary fixed finite `y` as the target's parenthetical
states — see **N3** below. The target's overall CONCLUSION (constant is
exactly `1`, not `<1`, no strict contraction by this bounding route) is
unaffected and independently confirmed correct.

---

## 5. Scrutiny of §6 (the two diagnoses) and §7 (Borel connection)

### 5.1 §6.1 (linear-in-h degradation / telescoping divergence)

Judged **sound and precisely stated**. The claim is narrowly scoped
("this crude bound... is too weak by itself to conclude convergence, let
alone a rate" — not "this proves `Psi` fails to converge"), and the
arithmetic (`sum 1/y` diverges, harmonic-series-like) is elementary and
correct. No issue found.

### 5.2 §6.2 (Watson/Laplace-in-`1/y` blindness to exponential content)

Judged **sound**. Independently confirmed the underlying fact that `R(z)`
has a pure Poincaré (power-series-in-`1/z`) asymptotic expansion with NO
additional exponentially-small-in-`z` correction on the positive real
axis: this is a standard property of the Mills-ratio/`erfcx` asymptotic
series (generated by repeated integration by parts of `int_z^inf
e^{-t^2/2}dt`, which produces only further power-law remainders at every
order, never an exponential one, on the real line). A convolution against
a kernel with this property can only produce algebraic-in-`1/y` content
from the LEADING two-term truncation `I(x+u,y)~=y*F(x+u)+C(x+u)` used in
the target's argument — the target's conclusion (this expansion route
cannot see the numerically-observed exponential approach rate) is correct.
One minor observation (not counted as a formal issue): the true mechanism
is arguably better described as "the two-term truncation of `I` in `y`
already discards `I`'s own exponentially-small-in-`y` remainder before any
kernel convolution happens" rather than purely "the kernel's own expansion
has no exponential term" — both facts are true and related, but the
former is the more complete explanation of where the blindness enters.
This does not affect the target's conclusion.

### 5.3 §7.3 (claimed distinction from `mclust_h1_validity_attempt`'s own grid)

Judged **real and correctly characterized**. Independently re-read
`mclust_h1_validity_attempt/ATTEMPT.md` §4: that front's `(x,c)` grid
computes `F(x;c)` at `t0` large enough to have already converged to the
`g->infinity` plateau (confirmed via its own "two-`t0` cross-check... must
agree to `>=15` digits" convergence discipline) and tests the
`eps->0`-uniformity, IN `x`, of that ALREADY-CONVERGED profile against the
derived `psi_n(x)` — i.e. `(U2)`-type content. The target's new §7
experiment instead measures the RATE at which `Phi(x,g)` approaches that
same plateau AS `g` INCREASES — i.e. `(U1)`-type content (local uniformity
of the `g->infinity` convergence itself). These are genuinely different
questions about the same system; the target's §7.3 characterization of
this distinction is accurate, not overstated.

### 5.4 §6.2's claimed connection to `plateau_resummation_attempt`'s Borel obstruction — **Issue N1**

See VERDICT above for the full statement. In detail: `plateau_resummation_
attempt/ATTEMPT.md` §2.3 states, verbatim, "Since the direct-cost wall is
the order-2 content, the natural move is Borel: `B(u) = sum a_k(0)
u^k/k!` and `Phi(0,t0) = (1/t0) int_0^inf e^{-u/t0} B(u) du`" — this is a
Borel-Laplace resummation of the SERIES IN `t0` (the record's own
unscaled `g`-variable, at `s=0`, at whatever `c` is fixed), attempted as a
computational trick to evaluate the ALREADY-CONVERGENT `g`-series more
cheaply than direct summation (which suffers a severe cancellation "cost
wall" at small `c`, per that document's own §2.2). This document contains
NO textual connection between this Borel attempt and `eps` anywhere
(confirmed by an explicit grep of the whole `ATTEMPT.md` for any co-
occurrence of "eps" and "Borel" — zero matches). Since `t0=g` and
`y=g*sqrt(c)`, `t0->infinity` at fixed `c` is exactly `y->infinity` at
fixed `eps` — the SAME limit direction the target's own §6.2 is analyzing,
not a different one. The target's characterization ("the SAME obstruction
`plateau_resummation_attempt` already found for Borel resummation in the
`eps->0` limit... now identified for the FIRST time in the `y->infinity`
limit instead") is therefore factually imprecise about which limit the
cited predecessor result concerns, and the depth of the claimed analogy is
separately overstated: the predecessor's obstruction is a genuinely
non-generic failure (the Borel transform of a specific, unusually-
fast-growing coefficient sequence — order-2/3 growth — makes classical
Borel-1 summation numerically useless for THAT series), whereas the
target's own §6.2 point is the fully generic, textbook fact that ANY
Watson/Laplace asymptotic expansion of a smooth, non-oscillatory kernel is
blind to exponentially-small corrections (true of essentially any such
expansion, not a specific discovery unique to this system). Calling this
"an exact structural echo, one level removed" of the specific predecessor
finding overstates both the novelty of the observation and the tightness
of the parallel. **Severity: MODERATE** — this is one of the document's
five headline claims (VERDICT UP FRONT item 3, and §6.2/§10 item 1), and
the mischaracterization is clear-cut once the cited source is re-read, but
it does not affect any numerical result, any other derivation, or the
front's own overall (correct) non-closure verdict.

---

## 6. Named issues (severity-rated summary)

| # | Location | Description | Severity | Affects any reported number/verdict? |
|---|---|---|---|---|
| N1 | §6.2 (citing `plateau_resummation_attempt` §2.3) | Misidentifies the predecessor's Borel-resummation obstruction as being about "the `eps->0` limit" when it is actually about the SAME `y->infinity` (`t0->infinity` at fixed `c`) direction the target itself is analyzing; also overstates the depth of the mechanistic analogy (specific coefficient-growth failure vs. generic Watson-expansion blindness) | **MODERATE** | No — does not change any number, bound, or the non-closure verdict |
| N2 | §5.1, displayed formula for `delta(x)` | Missing leading minus sign relative to a correct application of the Growth-Exclusion Lemma (confirmed via two independent re-derivations) | **LOW** | No — the very next step takes `|delta(x)|`, so the sign is immaterial to `(star-star)` |
| N3 | §8.2, "essentially TIGHT (saturated as `x->0`)" | Names the wrong asymptotic regime for where the Lipschitz bound saturates toward `1`; true regime is `y->infinity`, confirmed numerically (`y*R(y)` at `y=1` is `0.656`, far from `1`; at `y=100` it is `0.9999`) | **LOW** | No — the stated conclusion (constant `<=1`, not `<1`, sup approached not attained) is correct either way |

No HIGH-severity issue was found. No error was found in: the 7/7 published
anchor reproduction claims, the `(BB-Psi')` derivation itself, the
oscillation-bound derivation itself, the Lipschitz-chain derivation
itself, the §8.3 "obvious fixes fail" qualitative conclusions (the
"growing weight" sub-argument's specific displayed factor `y(1+y)R(x+y)`
was checked against an independently-derived weighted bound using the
same weight and found to differ in form — the referee's own derivation
gives a factor `~(1+y)*ln(1+y)` rather than `~y(1+y)` — but BOTH forms are
unbounded as `y->infinity`, so the qualitative conclusion, "this fix also
fails", is correct under either derivation; this discrepancy is noted here
for completeness but is not counted as a formal issue, since it does not
change any conclusion and the section is explicitly a brief, exploratory
dismissal of an "obvious fix", not a load-bearing proof step), the self-
caught-issues disclosures (S1–S3), or the "what remains open" list.

---

## 7. Millennium Prize Problem discipline

Checked explicitly, per the mandate. The target document states, at its
own opening ("This is `M-CLUST(b)`... a standalone object, entirely
independent of the archive's separate Tree A (`u1/2` / "Lemma Aberto")
line in `THEOREM.md`. Nothing here is, or is adjacent to, a Millennium
Prize Problem, and no such claim appears anywhere below") and this review
confirms: no such claim, framing, or adjacency appears anywhere in the
document. Consistent with every other front in this lineage.

---

## 8. Overall assessment

The target document's self-assessed tier — "honest non-closure of
`(U1)`/`(U2)`, with a genuinely new exact identity..., a new rigorously-
proved but structurally loose oscillation bound, a precise diagnosis of
exactly two distinct reasons this style of argument does not close the
gap, and a new numerical experiment... offering suggestive — not decisive
— support" — is **accurate and independently confirmed** by this review,
with the three named issues above being genuine but non-load-bearing
imprecisions (one moderate mischaracterization of a cited predecessor
result, two low-severity sign/regime slips that do not propagate to any
final claim). The document does not overclaim: every numerical result is
honestly hedged, every heuristic gap is named precisely, and the
document's own "what remains open" (§10) is, on independent review,
neither too pessimistic nor too optimistic about what was actually
achieved.

**`H1` (via `(U1)`+`(U2)`) remains open.** This front's contribution — a
new exact identity, a new global oscillation bound, and two precise
(now independently re-verified) diagnoses of why this route does not
close the gap — is genuine, correctly derived, and honestly reported.

---

## 9. Files in this directory

| file | role |
|---|---|
| `v01_symbolic_checks.py`/`.log` | sympy re-derivation of the Growth-Exclusion Lemma (2 independent routes), the `(BB-Psi')` exponent algebra, the oscillation-bound ODE identity (own re-derivation), the sign-consistency check (N2), the shift identity, and the Lipschitz-chain (§2–§4, §6 above) |
| `v02_numeric_checks.py`/`.log` | mpmath high-precision check of the shift identity, `R(z)<=1/z`, and the tightness-regime investigation (N3) (§4 above) |
| `v03_series_solver.py`/`.log` | fresh, from-scratch general-`s` `(P,Q)`-family series solver, independently re-deriving the descending-recursion/`kappa`-pinning bounded-branch algorithm by hand; validated 7/7 against published anchors (§2 above) |
| `v04_identity_check.py`/`.log` | numerical spot-check of `(BB-Psi')` at 2 independently-chosen `(s,g)` points via a genuinely different quadrature route (§2 above) |
| `v05_oscillation_bound_check.py`/`.log` | numerical sanity check of the oscillation bound at 3 independently-chosen `(g1,g2,x)` triples (§3 above) |
| `REFEREE_REPORT.md` | this document |

No `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, or
`index.html` was opened for writing. No `git` command was run. All writes
were confined to this `adversarial/` subdirectory.
