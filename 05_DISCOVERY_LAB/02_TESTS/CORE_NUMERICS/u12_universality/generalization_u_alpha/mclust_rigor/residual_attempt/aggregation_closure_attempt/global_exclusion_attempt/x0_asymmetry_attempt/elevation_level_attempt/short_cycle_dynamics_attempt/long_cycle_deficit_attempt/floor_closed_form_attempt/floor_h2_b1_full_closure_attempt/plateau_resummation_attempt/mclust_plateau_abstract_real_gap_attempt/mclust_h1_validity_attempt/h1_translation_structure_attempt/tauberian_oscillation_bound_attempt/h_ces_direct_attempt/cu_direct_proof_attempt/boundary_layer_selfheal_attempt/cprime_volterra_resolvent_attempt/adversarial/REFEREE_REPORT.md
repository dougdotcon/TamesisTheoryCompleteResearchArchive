# Hostile Referee Report — `CPRIME-VOLTERRA-RESOLVENT-ATTEMPT` (wave 31, front a, `DISC-DEC-142`)

**Target:** `.../boundary_layer_selfheal_attempt/cprime_volterra_resolvent_attempt/ATTEMPT.md`
(999 lines, scripts `s01`–`s08`). Scope: pure combinatorial/asymptotic
mathematics, `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`, node
`PLATRESUM`) — standalone, unrelated to any Millennium Prize Problem and
unrelated to the archive's separate Tree A (`u1/2`) line. This is wave 31
front (a), the twelfth consecutive wave (20–31) in this sub-lineage, and
the first to attack `(C')` itself as a standalone Volterra-resolvent-
stability claim.

**Method.** Read, in full and in the mandated order, before opening any
target script: `boundary_layer_selfheal_attempt/ATTEMPT.md` (wave 30
front c) and its `adversarial/REFEREE_REPORT.md`; `cu_direct_proof_
attempt/ATTEMPT.md` (wave 29 front a) Sec 5 in full, with extreme care,
and its `adversarial/REFEREE_REPORT.md` item (e); `PROOF_DEPENDENCY_
MAP.md` Tree B in full, including the `DISC-DEC-136`/`140` addenda and
the closing "Leitura" paragraph; `DECISION_LEDGER.yaml`'s `DISC-DEC-142`
and `DISC-DEC-115` entries; `h1_translation_structure_attempt/ATTEMPT.md`
for the original raw operator definitions. Only then the target's own
`ATTEMPT.md` in full, then all eight of its scripts.

Before opening any target script, this referee independently re-derived,
by hand and via fresh code (`sympy`/`mpmath`/`scipy`, never importing or
reading any target `.py` file until each re-derivation was complete), the
crux algebraic step of Theorems A and B (Sec 3.2–3.3) directly from the
raw kernel definitions, the renewal/Malthusian obstruction's generality
(Sec 2.2), and the Sec 5 growth-exponent numerics via a fresh ODE
implementation. All verification scripts and logs are in this directory
(`adv01`–`adv04`).

---

## VERDICT: **SOUND WITH ONE SUBSTANTIVE ERROR (correção) IN THE CENTRAL THEOREM'S ASSEMBLY STEP, propagating into two headline quantitative claims in Sec 5 — plus several low-severity notas. The error is fully diagnosed, its fix is exhibited and independently verified, and — critically — the fix STRENGTHENS rather than weakens the document's own honest negative/diagnostic conclusion (Sec 6). ACCEPT for catalogue only with the correction below applied.**

Theorems A and B (Sec 3.2–3.3), the renewal/Malthusian obstruction (Sec
2), the qualitative finding that the integrated kernel mass is uniformly
bounded (Sec 4), the general shape of Sec 5's diagnosis, and the overall
honest, non-overclaiming framing (VERDICT UP FRONT, Sec 6, Sec 8, Sec 9)
are all **independently confirmed sound**. But the Sec 3.4 COROLLARY
(the "(SHARP)" bound, the document's own central new deliverable) contains
a genuine coefficient error — traced to the exact moment the document's
own self-correction narrative (Sec 3.4's blockquote, Sec 7 Issue 3)
believed it was *fixing* a bug, when in fact it was introducing one. This
error is small in absolute magnitude (violations of a fraction of a
percent in the parameter regime this referee could search) but it is a
real, reproducible, non-degenerate violation of a claim stated as
"UNCONDITIONAL," and it propagates directly into Sec 5's two headline
numbers: the claimed growth-exponent formula and the claimed "sharp
qualitative transition at `eps=1`" are **both wrong as literally stated**.
The corrected versions are derived and numerically confirmed below.

---

## 1. Theorems A and B (Sec 3.2–3.3): independently CONFIRMED CORRECT

This referee re-derived, from scratch, directly from the raw operator
definitions (`h1_translation_structure_attempt`'s `K_A^raw`, `K_B`,
`T_w`, `M_y`), never having opened the target's `s01`/`s03`/`s04`:

- The single-integral reduction `K_A^raw(y,t)f(x) = int D_KAraw(s)f(x+s)ds`,
  `D_KAraw(s) := int_0^{min(h,s)} e^{-v/eps}e^{-(s-v)^2/2-(s-v)z}dv`.
- The substitution `u:=s-v` giving, for `s<=h`: `D_KAraw(s) =
  e^{-s/eps}*int_0^s e^{-u^2/2-uw}du`, `w:=z-1/eps`; for `s>h`:
  `D_KAraw(s) = e^{-s/eps}*int_{s-h}^s e^{-u^2/2-uw}du`.
- `M_y = -w` exactly (elementary algebra, re-confirmed).
- `D(s) = e^{-s/eps}[1-w*int_0^s e^{-u^2/2-uw}du]` on `[0,h]`.

**`adv01_theorem_AB_density_derivation.py`/`.log`** confirms every one of
these closed forms against the RAW double-integral definition numerically
(`mpmath`, `dps=40`) to 20–40 significant digits at 30 `(eps,z,h,s)`
combinations (the sympy symbolic route times out on this Gaussian-linear-
exponent integral, so this referee used high-precision numerical
confirmation instead, which is fully decisive here). It further confirms:

- **Theorem A** (`D(s)>=0` on `[0,h]`): the argument that `int_0^s
  e^{-u^2/2-uw}du` is nondecreasing in `s`, bounded by `R(w)`, and that
  `(G2)` applied to `w` in place of `z` — valid because the `z>1/eps`
  branch (the only branch where this positivity argument is invoked)
  guarantees `w=z-1/eps>0` by construction, exactly matching `(G2)`'s own
  domain of validity (`z>0`) — gives `w*R(w)=1-sigma(w)<=1`, hence
  `D(s)>=0`. **This substitution of `w` for `(G2)`'s `z` is legitimate and
  correctly scoped; no domain violation.** Confirmed both by hand and
  numerically (`adv01` Part B: `D(s)>=0` at every tested point).
- **Theorem B** (negative lobe, `s>h`): the closed form `D(s)=-w*e^{-s/eps}*
  int_{s-h}^s e^{-u^2/2-uw}du` and the bound `int_h^inf|D(s)|ds<=eps*e^{-h/eps}`
  (via `int_{s-h}^s(...)<=R(w)` and `w*R(w)<=1` again) are both confirmed
  exactly, including the full derivation chain the task specifically
  flagged as unchecked by the session's own pre-dispatch spot-check
  (which covered only the tail-integral piece `int_h^inf e^{-s/eps}ds`,
  not the `w*R(w)<=1` step folded into the bound).

**Theorems A and B, exactly as stated, are correct.** The error found
below is entirely in how Sec 3.4 *assembles* them.

---

## 2. THE CENTRAL FINDING: Sec 3.4's (SHARP) formula has the wrong coefficient

### 2.1 The exact identity this referee used to find it

Since `D(s)>=0` on `[0,h]` and `D(s)<=0` for `s>h`:

```
K(y,t)[1](x) = int_0^inf D(s)ds = int_0^h D(s)ds - int_h^inf|D(s)|ds
=> int_0^h D(s)ds = K(y,t)[1](x) + int_h^inf|D(s)|ds              (EXACT)

||K(y,t)|| = int_0^h D(s)ds + int_h^inf|D(s)|ds
           = K(y,t)[1](x) + 2 * int_h^inf|D(s)|ds                  (EXACT)
```

This is elementary bookkeeping (the "negative-lobe mass" enters `||K(y,t)||`
**twice** — once implicitly, via the fact that it drags `int_0^h D(s)ds`
itself above `K(y,t)[1](x)`, and once explicitly, as the added `|.|` term
— since `||K(y,t)||` sums the *unsigned* mass on both sides while
`K(y,t)[1](x)` sums the *signed* mass). Using Theorem B's bound
(`int_h^inf|D(s)|ds<=eps*e^{-h/eps}`), the CORRECT bound this identity
licenses is:

```
||K(y,t)||  <=  K(y,t)[1](x)  +  2*eps*e^{-h/eps}          [coefficient 2]
```

**not** coefficient 1, as the target's `(SHARP)` states (Sec 3.4, `s04`
Part 4). The target's own `s04` script (lines 37–48) makes the error
explicit in its own inline comment: *"NOTE the coefficient on the second
term is eps, not 2\*eps as an earlier draft of this reasoning stated
informally — ||K(y,t)|| itself is int|D|=positive_lobe+|negative_lobe|,
i.e. ONE copy of the negative lobe magnitude added to the positive lobe,
not two."* This reasoning silently conflates `int_0^h D(s)ds`
("`positive_lobe`") with `K(y,t)[1](x)` — but these are **different
quantities**, differing by exactly `int_h^inf|D(s)|ds` (the EXACT
identity above). The target's own **Sec 7 Issue 3** and the **Sec 3.4
blockquote** narrate this exact moment as a self-caught fix ("the correct
coefficient is `eps`, not `2*eps`... caught and corrected"); in fact the
originally-discarded `2*eps` estimate was, in the specific sense made
precise above, closer to the truth, and the "fix" introduced the bug.

### 2.2 Numerically confirmed violation, at `dps=50` (not a quadrature artifact)

**`adv02_sharp_corollary_coefficient_bug.py`/`.log`**, at `eps=0.2,
z=8.0, h=0.8` (so `w=z-1/eps=3.0`, comfortably inside the `z>1/eps`
regime the theorem is stated for):

```
TRUE ||K(y,t)|| (unified |D(s)| integral, dps=50) = 0.127602755766681910...
target's (SHARP), coefficient 1                    = 0.127473966390056526...
                                    VIOLATION: excess = 1.288e-4 (relative 0.101%)
```

confirmed via **two independent computation routes within `adv02`** — a
single unified `int_0^inf|D(s)|ds` quadrature, and the component sum
`int_0^h D ds + int_h^inf|D|ds` — agreeing to `<1e-25`, ruling out
numerical noise. The corrected coefficient-2 formula (`0.131137...`) IS a
valid bound at this point, as it must be (an unconditional algebraic
consequence of Theorem B alone). A broader sweep (`mpmath`, `dps=30`, 48
`(eps,w,h/eps)` triples, plus a faster `scipy` double-precision search of
336+ points and a local optimizer) finds violations concentrated in a
band roughly `h/eps in [2,6]`, `w in [1,10]` (moderate lag, moderate
excess over `1/eps`) — with the worst violation found by direct search
around **0.5% relative** (`adv02` Step 4, plus this referee's separate
exploratory `scipy` search reaching a ratio of `TRUE/SHARP~1.005`
before the search boundary was reached; a fully rigorous supremum was
not established, but is not needed to demonstrate the formula is false
as an unconditional bound).

### 2.3 Why the target's own `s08` numerics never caught this

`s08_positivity_and_bound_numeric.py`'s Check C (the ONLY place the
target numerically tests the full `(SHARP)` formula) always sets `h:=z`
(the `t=0, x=0` "maximal-`h`" case), giving `h/eps` in the range `20`–`120`
for its tested `(eps,z)` pairs — so `e^{-h/eps}` is astronomically small
(`~1e-15` to `~0`) in every one of `s08`'s Check C tests, making the
tail-term coefficient (1 vs 2) numerically invisible there. The document's
own claim (Sec 3.4) that `s08` confirms the formula "to quadrature
precision (relative differences `<1e-8`... as small as `1e-25`)" is
**accurate only in this specific tested regime** (`h=z`, large `h/eps`)
and does not generalize to the moderate-`h/eps` regime where the true
coefficient error is visible. This is a genuine gap in test coverage, not
merely an unlucky miss — the one test designed to stress-test the full
`(SHARP)` formula happened to be structurally incapable of detecting a
bug that lives specifically in the tail term's relative weight.

**Severity: correção.** This is a real mathematical error in the
document's central new theorem, independently verified via an exact
identity plus a numerically-confirmed counter-example at 50-digit
precision. It is fixable by a one-word change (coefficient `eps` →
`2*eps` in `(SHARP)`), which this referee has verified is unconditionally
valid (an exact consequence of Theorem A+B alone, needing no further
search).

---

## 3. Downstream impact on Sec 4 and Sec 5

### 3.1 Sec 4 (integrated kernel mass): qualitative conclusion SURVIVES, constant is wrong

Re-integrating the corrected per-`h` bound (`A(z)(1-e^{-h/eps}) +
2*eps*e^{-h/eps}`, `A(z):=R(z)+eps*sigma(z)`) over `h in [0,y]`
(symbolically re-derived, `sympy`, residual 0 — see inline verification
in this report's construction) gives:

```
int_0^y ||K(y,t)|| dt  <=  1 + eps/z + 2*eps^2      [was: 1+eps/z+eps^2]
```

**The QUALITATIVE claim of Sec 4 — the integrated kernel mass is
UNIFORMLY BOUNDED in `y` — is UNAFFECTED and remains correct**; only the
specific additive constant (`2*eps^2`, not `eps^2`) needs correcting.
This is a correção of degree, not of kind: the "how close to closing
`(**)`" discussion (falls short by `eps/z+eps^2`) should read
`eps/z+2*eps^2` — an even LARGER shortfall than reported, i.e. the
document's own "not there yet, falls short by a precisely quantified
margin" framing remains honest and, if anything, was slightly too
optimistic about the margin.

### 3.2 Sec 5 (ODE reformulation, growth exponent, `eps=1` transition): TWO HEADLINE NUMBERS ARE WRONG

Sec 5.1 builds the majorant ODE directly from the flawed `(SHARP)`
decomposition: `A(z) + B(z)e^{-h/eps}`, `B(z):=eps-A(z)`. The corrected
version, following directly from §2 above, is `B_corrected(z) :=
2*eps-A(z)`.

**`adv03_reproduce_target_and_show_downstream_impact.py`/`.log`**:

- **Part 1** independently reproduces the target's own (flawed-`B`) `s07`
  numbers with completely fresh code (a from-scratch ODE derivation,
  `scipy.special.erfcx`-based `R(z)` rather than `mpmath`, `scipy`'s
  `Radau` integrator): `eps=0.3,0.5,0.7` give fitted exponents
  `0.09890, 0.33333, 0.96075` against the target's own published
  `eps^2/(1-eps^2)` heuristic — **matches to the same 4–5 significant
  figures the target itself reports.** This confirms `s07`'s own
  computation is internally correct and its self-caught resolution-bug
  fix (Sec 7 Issue 2, `s05`/`s06` → `s07`) is genuine and adequate —
  **the bug is entirely upstream, in which `B(z)` was fed to a
  correctly-implemented ODE, not in the ODE machinery itself.**

- **Part 2** re-solves the SAME ODE system with `B_corrected(z):=2*eps-A(z)`
  and finds the fitted growth exponent now matches, to 4–5 significant
  figures, a DIFFERENT closed form — `2*eps^2/(1-2*eps^2)` — obtained by
  re-running the target's own Sec 5.3 quasi-steady-state argument with
  `B_corrected` in place of `B`:

  | `eps` | fitted (corrected ODE) | `2eps^2/(1-2eps^2)` |
  |---|---|---|
  | 0.3 | 0.21951 | 0.21951 |
  | 0.5 | 0.99997 | 1.00000 |
  | 0.6 | 2.57103 | 2.57143 |
  | 0.65 | 5.44811 | 5.45161 |
  | 0.68 | 12.25966 | 12.29787 |
  | 0.70 | 46.90666 | 49.00000 |
  | 0.705 | 123.77469 | 167.06723 |
  | ≥0.71 | non-finite (explosive) | — |

  and the ODE integration becomes **non-finite (explosive growth) once
  `eps` exceeds `~0.707`** — matching `1/sqrt(2)=0.70711` almost exactly,
  not the target's claimed `eps=1` transition. This is the corrected
  version of the same quasi-steady-state mechanism the target itself
  identifies (`B(z)-1/eps` changing sign): with `B_corrected(z)->2*eps`
  as `z->infty` (instead of `->eps`), the sign change occurs at
  `2*eps=1/eps`, i.e. `eps=1/sqrt(2)`, not at `eps=eps` i.e. `eps=1`.

**Severity: correção.** Both of Sec 5's headline quantitative findings —
the growth-exponent formula `eps^2/(1-eps^2)` and the "sharp qualitative
transition at `eps=1`" — are **incorrect as literally stated.** The
corrected versions (`2*eps^2/(1-2*eps^2)`, transition at `eps=1/sqrt(2)`)
are derived here via the identical method the target itself uses (its own
Sec 5.3 argument, applied to the corrected coefficient) and independently
confirmed numerically to essentially the same precision the target
reports for its own (flawed) numbers.

### 3.3 Crucially: the correction STRENGTHENS, not weakens, the document's own conclusion

The corrected exponent `2*eps^2/(1-2*eps^2)` is **strictly larger** than
the target's claimed `eps^2/(1-eps^2)` for every `eps` in `(0,1/sqrt(2))`,
and the corrected transition to explosive growth occurs at a **smaller**
`eps` (`0.707` vs `1`). **The TRUE majorant obstruction, correctly
computed, is worse (grows faster, explodes sooner) than what the document
reports.** Sec 6's qualitative conclusion — "no operator-norm/majorant-
based argument on `K(y,t)`, however sharp, can establish the reduction's
needed uniform stability" — is therefore **not undermined by this error;
if anything it is more strongly supported** by the corrected analysis.
This is a fortunate but not automatic consequence, and it should not be
read as diminishing the severity of the underlying algebra error, which
does need correcting in the archived record.

---

## 4. Other items checked

### 4.1 The renewal/Malthusian obstruction's generality (Sec 2.2) — NOTA

**`adv04_renewal_generality_and_misc_checks.py`/`.log`** Part 1 confirms
`s_+(c,eps)=(sqrt(1+4c eps)-1)/(2eps)>0` for every `c,eps>0` and that it
exactly solves `k_hat(s)=1` — a correctly, fully general elementary fact
**for the specific parametric family `k(h)=c(1-e^{-h/eps})`** the target
computes with. The document's "Conclusion" paragraph broadens this to
"ANY norm-envelope argument... by a function of the lag `h` alone that
does not decay... is doomed" — a claim not literally proved for arbitrary
saturating shapes, only for this one family (which is, admittedly, the
natural one here, since it exactly matches `||K_B(h)||`). A spot-check on
one alternative saturating shape (`adv04` Part 2, an algebraic rather
than exponential approach to saturation) shows continued apparent
exponential-type growth, supporting the broader claim's plausibility, but
this is not a proof. **Severity: nota** — the specific proved result and
its use in the paper are correct; only the generalized restatement in the
"Conclusion" paragraph slightly overreaches its own proof.

### 4.2 Sec 6's "however sharp" language — NOTA

The document's overall conclusion (VERDICT item 4, Sec 6 item 4) that "no
operator-norm/majorant-based argument... however sharp, can establish"
the needed stability is, strictly, demonstrated only for the specific
majorant constructions this front tried (the crude constant, and its own
— now corrected — sharp bound), not for literally every conceivable
norm-based construction (e.g. a majorant built from the numerically-exact
`||K(y,t)||`, never attempted here or by this referee). The document
elsewhere appropriately hedges this as "this front concludes" (VERDICT
item 4) and as a diagnosis rather than a proof (Sec 8 item 1), so the
overreach is confined to a few strongly-worded sentences rather than a
misrepresentation of what was shown. **Severity: nota.**

### 4.3 Sup-over-`x` — NOTA (a slight understatement, not an error)

`adv04` Part 3 confirms `A(z)` is monotonically decreasing in `z`, so
`x=0` (not the target's fixed `x=1`) is the worst case for a given `y`.
The document's Sec 8 item 7 already discloses this honestly as "not
independently verified across `x`." This referee's own check (the
earlier `ref04` exploration, reproduced in spirit by `adv04` Part 3)
found the fitted growth EXPONENT is identical across `x=0,1,5` (only the
prefactor/magnitude changes), corroborating the document's own claim that
this omission is unlikely to change the qualitative picture. **Severity:
nota**, and if anything the document's "uniform in `y`" framing (Sec 4)
could have honestly claimed "uniform in `y` AND `x`" — a small
understatement, not an overclaim.

### 4.4 "More than two orders of magnitude sharper" claim (`eps=0.5, z=60`) — CONFIRMED ACCURATE

`adv04` Part 4 independently confirms `TRUE ||K(y,t)|| = 0.016801` vs
`crude sqrt(pi/2)+eps = 1.753314`, a `104.36x` sharpening factor — this
specific claim is accurate, since the cited regime (`h=z=60`, `x=0,t=0`)
has `h/eps=120`, far outside the moderate-`h/eps` band where §2's
coefficient bug is visible.

### 4.5 Self-caught issues (Sec 7) — accurately described, with one exception

- **Issue 1** (`s02`, Laplace-transform slip): confirmed genuine and
  accurately described — `s02`'s committed script derives `k_hat(s)`
  correctly via two independent routes from the start, consistent with
  the narrated catch-and-fix.
- **Issue 2** (`s05`/`s06` resolution bug, fixed via `s07`'s ODE
  reformulation): **confirmed genuine and the fix is adequate** — `adv03`
  Part 1 independently reproduces `s07`'s own numbers with completely
  fresh code, confirming the ODE machinery itself is correct (the
  remaining bug, §2 above, is entirely upstream of `s07`, in what `B(z)`
  value `s07` was given, not in how `s07` solves the ODE). Confirmed:
  `s05`/`s06`'s discredited numbers do not appear as cited facts anywhere
  in the main text (`grep`-confirmed only `s07`'s numbers are used in
  Sec 5.2's table).
- **Issue 3** (the "`2*eps` vs `eps`" bookkeeping slip, Sec 3.4/Sec 7):
  **this is the self-caught-issue entry that, on independent
  verification, describes the WRONG resolution** — see §2 above. The
  document accurately narrates that a `2*eps`-based estimate was
  discarded in favor of an `eps`-based one, but the direction of the
  correction was backwards: the coefficient-1 (`eps`) formula is not a
  valid unconditional bound, while a coefficient-2 (`2*eps`) formula is.
  This is not a "self-caught issue" in the sense the document intends
  (an error found and correctly fixed before assertion) — it is the
  error itself, self-narrated as if it were a fix.
- **Issue 4** (`s07`'s cross-check tolerance relaxation): not
  independently re-examined in depth by this referee; the disclosed
  justification (Richardson-style extrapolation argument, visible in
  the committed script) is plausible and not load-bearing for any of
  this report's findings.

---

## 5. Scope, governance, and seeds — CONFIRMED

- `grep -rn "random\|seed"` over the target's own `s01`–`s08`: matches
  only in comments explicitly stating the ABSENCE of randomness — no
  actual RNG usage anywhere.
- `grep -rn "20260948"` over `05_DISCOVERY_LAB/`: appears only in
  `DECISION_LEDGER.yaml`'s own `DISC-DEC-142` reservation line — the
  reserved block `20260948000-20260948999` is genuinely unused.
- No `git`/`subprocess`/`os.system` calls in any target script.
- `cprime_volterra_resolvent_attempt/` is the only new directory, nested
  correctly inside `boundary_layer_selfheal_attempt/`; no `adversarial/`
  directory was created by the target itself (this referee created the
  one now containing this report); no ancestor files were modified.
- `grep -rniE "tree a|u_alpha|u1/2|lema aberto|millennium"` over the
  target's own `ATTEMPT.md`: matches occur ONLY inside the standard
  Tree-A-independence disclaimer boilerplate (repeated near the top and
  in the Sec 13 scope-discipline confirmation) — no substantive
  cross-reference to Tree A content anywhere, confirming the document's
  own claim that `M-CLUST(b)` is treated as entirely independent.

---

## 6. What this referee independently confirms sound, in its own words

**Theorem A and Theorem B are genuinely new, correct, and non-trivial.**
The crux insight — that swapping the raw `K_A^raw` double integral's
order of integration and substituting `u=s-v` exposes an EXACT,
closed-form density `D(s)` whose sign structure can be read off directly
from the already-proven Mills-ratio bracket `(G2)` applied to the shifted
variable `w=z-1/eps` — is correct, and the resulting positivity-on-`[0,h]`
/ exponentially-small-negative-lobe-beyond-`h` structure is a genuinely
new fact about this kernel that no prior front in twelve waves identified.
This referee re-derived it independently from the raw definitions (never
having opened the target's own scripts) and confirms it to 20–40
significant digits at every tested point.

**The qualitative finding that the integrated kernel mass is uniformly
bounded in `y` (Sec 4) is real and, once the coefficient in §2 is fixed,
correctly established** — a genuine qualitative surprise relative to
every prior naive estimate in this sub-lineage (all of which diverge).

**The renewal/Malthusian obstruction (Sec 2) is a genuine, correct,
general refinement of the predecessor's crude case-specific Gronwall
finding** — for the specific saturating family that matches `||K_B(h)||`
exactly, exponential blow-up of the majorant is unconditional for every
positive saturation level, proved via an exact, elementary Laplace-
transform argument this referee re-derived independently and confirms.

**The Sec 5 diagnosis's qualitative shape (polynomial growth, not
exponential; a sharp transition to faster growth at some threshold
`eps`) is real and correctly identified as a phenomenon** — only the
specific exponent formula and the specific threshold value are wrong, as
detailed in §3.2 above; the corrected versions follow the identical
method the document itself uses.

**Sec 6's overall diagnostic conclusion — that norm/majorant-based
techniques on `K(y,t)` cannot close this reduction, and that a genuinely
different technique exploiting `Phi_t`'s own self-consistency is needed
— survives this review, and if anything is more strongly supported by
the corrected analysis than by the document's own (too-optimistic, due
to the coefficient bug) numbers.**

The document's overall honesty discipline — clearly separating what is
proved from what remains open, disclosing self-caught issues rather than
silently fixing them, not claiming `(C')`/`(B)` are closed anywhere — is
genuine and consistent with this sub-lineage's established convention.
The one place this discipline broke down is exactly the place a subtle
bookkeeping error is hardest to catch: a self-correction that was
believed, and narrated, to be a fix, when independent verification shows
it introduced the bug it thought it was preventing.

---

## 7. Recommended corrections for integration

1. **Sec 3.4, `(SHARP)`**: change `+ eps*e^{-h/eps}` to `+ 2*eps*e^{-h/eps}`.
   Remove or correct the inline blockquote and Sec 7 Issue 3's narrative
   (the "`2*eps` vs `eps`" self-correction was backwards).
2. **Sec 4**: change `<= 1 + eps/z + eps^2` to `<= 1 + eps/z + 2*eps^2`
   throughout; the qualitative conclusion (uniformly bounded) is
   unaffected.
3. **Sec 5.1**: change `B(z):=eps-A(z)` to `B(z):=2*eps-A(z)`.
4. **Sec 5.2's table and Sec 5.3's formula**: replace `eps^2/(1-eps^2)`
   with `2*eps^2/(1-2*eps^2)`, and re-run `s07` with the corrected `B(z)`
   to regenerate the numeric table (this referee's `adv03` provides
   independently-confirmed replacement numbers, matching to 4–5
   significant figures, that can be cross-checked against a corrected
   `s07` re-run).
5. **Sec 5.3**: replace "a sharp qualitative transition at `eps=1`" with
   "at `eps=1/sqrt(2)`" throughout, including the VERDICT UP FRONT and
   Sec 9 scorecard language.
6. **Sec 9 Scorecard**: the row "Sharp bound on `||K(y,t)||` (`SHARP`)...
   PROVED (new, unconditional, central result)" should read "PROVED with
   corrected coefficient (see referee correction)"; the growth-exponent
   and transition rows likewise need the corrected formulas.
7. A one-line addendum noting that the correction **strengthens** Sec 6's
   qualitative conclusion is recommended, so a future reader does not
   mistake this correction for evidence against the document's central
   honest finding.

None of these corrections revive `(C')`, `(B)`, `(H-ces)`, `(U1)`, `(U2)`,
or `H1` from OPEN status — all remain exactly as the document states.
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are untouched by this report.

---

## Files in this directory

| file | role |
|---|---|
| `adv01_theorem_AB_density_derivation.py`/`.log` | independent re-derivation of Theorems A/B from the raw operator definitions — CONFIRMS both correct |
| `adv02_sharp_corollary_coefficient_bug.py`/`.log` | THE central finding: exact identity `\|\|K\|\|=K[1]+2\*tail`, confirmed to 50 digits; demonstrates the target's coefficient-1 `(SHARP)` formula is violated at `eps=0.2,z=8,h=0.8` (and nearby points); confirms the corrected coefficient-2 formula |
| `adv03_reproduce_target_and_show_downstream_impact.py`/`.log` | fresh independent reproduction of the target's own (flawed) Sec 5.2 numbers (confirms `s07`'s ODE machinery itself is sound); re-solves with the corrected `B(z)`, finding a different exponent formula and transition point |
| `adv04_renewal_generality_and_misc_checks.py`/`.log` | renewal-obstruction generality nota; sup-over-`x` nota; independent confirmation of the ">100x sharper" headline numerical claim |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was created or modified
by this referee. No `git` command was run. No claim of progress on any
Millennium Prize Problem appears anywhere in this report; pure
mathematical analysis internal to this archive.
