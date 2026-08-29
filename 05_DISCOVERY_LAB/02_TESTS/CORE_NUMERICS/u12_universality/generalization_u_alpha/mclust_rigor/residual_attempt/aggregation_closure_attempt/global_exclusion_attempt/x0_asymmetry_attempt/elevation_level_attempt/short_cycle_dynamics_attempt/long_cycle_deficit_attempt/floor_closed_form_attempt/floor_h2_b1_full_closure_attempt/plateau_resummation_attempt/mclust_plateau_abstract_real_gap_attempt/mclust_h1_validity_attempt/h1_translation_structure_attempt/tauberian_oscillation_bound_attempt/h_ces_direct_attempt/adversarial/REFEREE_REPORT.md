# REFEREE REPORT — `H-CES-DIRECT-ATTEMPT` (wave 28, front a, `DISC-DEC-131`)

**Hostile independent referee.** Target:
`.../mclust_h1_validity_attempt/h1_translation_structure_attempt/tauberian_oscillation_bound_attempt/h_ces_direct_attempt/ATTEMPT.md`.
Scope: pure combinatorial/asymptotic mathematics, `M-CLUST(b)` (Tree B of
`PROOF_DEPENDENCY_MAP.md`, node `PLATRESUM`) — standalone, unrelated to any
Millennium Prize Problem and unrelated to the archive's separate Tree A
(`U_α`/`u1/2`) line. This is the ninth consecutive wave (waves 20–28)
attacking the same `H1`/`(U1)`/`(U2)` gap in this exact sub-lineage, and the
first to target `(H-ces)` directly.

**Method.** Read in full, in the order specified by the dispatching mandate,
before opening any of the target's own scripts: the immediate predecessor
`tauberian_oscillation_bound_attempt/ATTEMPT.md` (wave 26, front c) in full,
including its `T0`/`T1`/`T2` decomposition, its verbatim statements of
`(C')`, `(U)`, `(B)`, and its dated referee Achado F2 (necessary-and-
sufficient bridge); `h1_translation_structure_attempt/ATTEMPT.md` (wave 25)
in full, including Sec 6.1's self-averaging-identity derivation and Sec 4.4's
"pointwise-in-`f`, not operator-norm" scope note; `PROOF_DEPENDENCY_MAP.md`'s
`PLATRESUM`-node addenda for `DISC-DEC-122` and `DISC-DEC-125`; and only then
the target's own `ATTEMPT.md` in full. The core algebraic machinery — the
`(VOLTERRA-Phi)`-plus-closed-form decomposition into `g_y(x) - J(y)/z +
E_W(y)`, the `J(y)` bound from `(B)` alone, the quotient-rule identity, the
tail integral, the telescoping-sum cross-check, and both Sec 4 worked
examples — was independently re-derived **from scratch, by hand and in fresh
code**, before the target's own `s01`–`s04` scripts were opened. `s01`–`s04`
were read only afterward, for cross-checking arithmetic and for the Sec 8
self-caught-issue spot-check. All adversarial scripts in this directory
(`adv01`–`adv03`) were written fresh, importing nothing from the target or
any ancestor front.

---

## VERDICT

# SOUND WITH ONE COSMETIC ISSUE — ACCEPT FOR CATALOGUE

Every mathematical claim examined — the exact rearrangement of
`(VOLTERRA-Phi)` under the cited closed-form kernel into
`e(y)=g_y(x)-J(y)/z+E_W(y)`; the `|J(y)/z|<=M_Phi*eps/z` bound from `(B)`
alone (both the extremal constant-`Φ` case and the concrete oscillatory
`M_Phi*cos(t)/(1+u)` majorant argument); the elementary fact that
integrating a **pointwise-in-`t`, `t`-independent** remainder bound
`|rho(t)|<=D(x,eps)/z^2` over `t∈[0,y]` gives `|E_W(y)|<=y*D(x,eps)/z^2`
with nothing beyond the triangle inequality for integrals; the assembly of
`(QUANT-E)`; the exact quotient-rule identity
`d/dy[A(y)/(x+y)]=e(y)/(x+y)`; the exact tail-integral formula
`∫_{Y0}^∞ C/(x+y)^2 dy = C/(x+Y0)`; the Cauchy-criterion mechanics; the
independent telescoping-sum cross-check (reconstructed via `sympy Sum` and
confirmed to telescope to the identical `C/(x+Y0)` limit, including the
concrete `x=1,D=2,Y0=1` numeric instance, running sum `0.999023914104`
against predicted total `1.0`, reproduced digit-for-digit); the Sec 3
triangle-inequality rate transfer; and both Sec 4 worked examples (the
positive `e(y)=D/(x+y)` example, confirmed exactly and via independent
`mpmath` re-integration of `h'(y)=D/(x+y)^2` from scratch to <1e-25 absolute
agreement across `Y=2` to `Y=10^7`; and the sharpness
`h(y)=sin(log(log(x+y+3)))` example, confirmed exactly for `h'(y)`, the
`O(1/\log z)` vs `O(1/z)` separation, the divergent `log(log w)` antiderivative,
and the constructive subsequence hitting `-1,0,+1` exactly to `<10^-30`) —
**was independently re-derived or reproduced and confirmed correct**, with
no arithmetic or logical error found anywhere. One LOW-severity, purely
cosmetic finding (below) does not affect any substantive claim.

**The central claim under the sharpest scrutiny — that Sec 2.1's derivation
needs no hypothesis beyond `(B)`, `(C')`, and `(U)` as wave 26 itself already
defined them — survives.** See Finding-free discussion, item (a) below, for
the full independent re-derivation that establishes this.

---

## 1. Item (a): Sec 2.1's bound on `e(y)` — does it smuggle in anything
beyond `(B)`, `(C')`, `(U)`?

Re-derived completely independently (`adv01_core_derivation_from_scratch.py`,
never having opened the target's own `s01`), starting only from the cited
`(VOLTERRA-Phi)` equation and the cited closed-form kernel asymptotic:

- **The relabeling `h:=y-t` inside the closed form, producing `J(y):=
  int_0^y e^{-(y-t)/eps} Phi_t(x+y-t) dt`, is an exact algebraic
  substitution with no hidden approximation** — confirmed symbolically
  (`adv01` Part 1: `e^{-(y-t)/eps}` and `x+y-t` match `e^{-h/eps}`,
  `x+h`|_{h=y-t} identically, residual `0`).
- **`|J(y)/z|<=M_Phi*eps/z` genuinely requires `(B)` alone, nothing more.**
  The extremal case `Phi_t≡M_Phi` gives `J(y)=M_Phi*eps*(1-e^{-y/eps})`
  exactly (symbolic, `adv01` Part 2), confirmed `<=M_Phi*eps` at 5 numeric
  points spanning `y∈[0.001,10^5]`. A **concrete non-constant** example,
  `Phi_t(u):=M_Phi*cos(t)/(1+u)`, was independently constructed (not
  imported from the target, which uses the identical example) and confirmed
  to satisfy the SAME bound via the pointwise absolute-value majorant
  `|cos(t)/(1+u)|<=1` — no Lipschitz/regularity hypothesis enters this piece
  at all, matching the target's claim precisely.
- **The step the mandate specifically flagged for scrutiny — going from a
  POINTWISE-in-`t` remainder bound `|rho(t)|<=D(x,eps)/z^2` to the
  INTEGRATED bound `|E_W(y)|<=y*D(x,eps)/z^2` — is nothing more than the
  triangle inequality for integrals, PROVIDED `D(x,eps)` is `t`-independent**
  (confirmed symbolically, `adv01` Part 3: `int_0^y (D/z^2) dt = y*D/z^2`
  exactly, trivially, since the integrand carries no `t`-dependence once `D`
  is assumed uniform). **This `t`-independence of `D` is EXACTLY what wave
  26 itself already meant by `(C')` (Lipschitz regularity of `Φ_t(·)`
  UNIFORM in `t`) and `(U)` (the `O(1/z^2)` remainder uniform over the FULL
  `h∈[0,y]` range, i.e. over the full `t∈[0,y]` range) — not a stronger or
  differently-shaped requirement.** Cross-checked directly against wave 26's
  own Sec 3.4 `T1` derivation (re-read carefully for this purpose): wave 26's
  `T1` bound, `int_0^{y1}[K(y2,t)-K(y1,t)]Phi_t(x)dt`, **already** applies
  the closed form pointwise-in-`t` across the identical full history
  `t∈[0,y1]` (covering `h/y1` from near `0` to near `1`, the same "distant
  past" regime), and its own stated error term `y1·O(1/z1²)` is **licensed
  by exactly the same `t`-uniform-constant assumption**, which wave 26 names
  `(U)` in that exact spot (its own Sec 3.4: "GIVEN the closed form's
  `O(1/z²)` remainder is uniform over the FULL `t∈[0,y1]` range... this is
  hypothesis `(U)`"). **The target's Sec 2.1 is, if anything, a strictly
  SIMPLER instance of the identical combined `(C')+(U)` usage wave 26's own
  `T1` already required** (a single application of the closed form across
  `t∈[0,y]`, rather than wave 26's paired application at two different `y`
  values followed by a subtraction) — not a silently stronger one. **The
  mandate's concern (b) [that "applied uniformly across the WHOLE family
  `{Φ_t}_{t∈[0,y]}`" might be a strengthened use] does not hold up**: it is
  literally the same family-uniform use wave 26's `T1` piece already made,
  restated here in slightly more explicit prose than wave 26 itself used.
- **`(QUANT-E)`'s assembly is correct arithmetic** (`adv01` Part 4):
  `|e(y)|<=e^{-y/eps}+M_Phi*eps/z+D/z`, and for `y` large enough that
  `e^{-y/eps}<=1/z` (numerically confirmed at `eps=0.1`: already true by
  `y=10`, where `e^{-y/eps}~3.7e-44` against `1/z=0.1`), this collapses to
  `C(x,eps)/z` with `C(x,eps)=1+M_Phi*eps+D(x,eps)`, matching the target
  exactly.

**Conclusion on item (a): no hidden strengthening found. `(C')` and `(U)`
are used in Sec 2.1 in exactly the sense, and to exactly the degree, wave
26's own `T1` piece already established as needed.**

---

## 2. Item (b): Sec 3's "local uniformity in `x`" inheritance

The target explicitly does not re-derive wave 26 Sec 5.2's finding, citing
it instead. Traced through independently: every constant entering
`(QUANT-E)` — `M_Phi` (global, `(B)`, manifestly `x`-independent), the "1"
from the `e^{-y/eps}<=1/z` bound (a bare numeric constant, no `x`-dependence
at all), and `D(x,eps)` — is **the identical `D(x,eps)` quantity that arose
in wave 25's own Watson's-lemma expansion of the closed-form kernel's
remainder** (wave 25 Sec 4.3: `rho(h',z)~f'(x+h')/z^2+O(1/z^3)`), cited
unchanged, not re-derived or re-parametrized by this front. Since this
front's `E_W(y)` is built from the SAME closed-form kernel's remainder,
integrated over the SAME `t∈[0,y]` history wave 26's `T1` already integrated
over, no new source of `x`-dependence is introduced — the target's claim
that "no NEW `x`-uniformity concern is introduced by this front's argument
beyond what wave 26 already named" checks out. The inherited caveat
(spot-checked at `x=0,3` only, not exhaustively proved) is honestly carried
forward, not concealed (Sec 7 item 6 restates it explicitly).

---

## 3. Item (c): Section 5's numerical stress-test — overclaiming check

Read carefully against its own log (`s03_kernel_family_uniformity_
stress_test.log`, values cross-checked: `max|z²·remainder|=0.4225`,
`min=0.0336`, phase-spread `<=0.757` — all match the prose exactly, no
rounding games). The "Scope of this result, stated precisely" paragraph
explicitly states the test is **NOT** on the real, evolving `Φ_t`, and
**NOT** exhaustive over all `(B)+(C')`-admissible families — only a single
rigid, deliberately simple 6-member family. This is honest, appropriately
hedged "support, not proof" language; no overclaiming found. The two
self-caught issues in Sec 8 (a tolerance-scale bug in `s01`'s Check 2, and a
breakpoint-count performance bug in `s03`) were spot-checked directly against
the committed `.py` files and are genuinely present and accurately described
(the "SELF-CAUGHT" markers and the geometric-breakpoint fix are both visible
in `s03`; the relative-tolerance fix is visible in `s01`).

---

## 4. Item (d): does the Cauchy-criterion argument really bypass the
Tauberian apparatus, or smuggle back an equivalent?

**No smuggling found.** The classical Tauberian theorem's actual work is to
license `g(y)->L` from `(1/y)∫_0^y g\,dt->L` PLUS a relative-step
slow-oscillation condition on `g` itself — a genuinely nontrivial converse
("Tauberian") step precisely because a Cesàro-convergent sequence need not
converge itself (wave 26's own `sin(log(1+t))` counter-example is the proof
of exactly this). The target's argument does not attempt any such converse
step on the sequence `Φ_y(x)` at all: it instead directly bounds the
DERIVATIVE of `h(y):=A(y)/(x+y)` — a single, already-well-defined real
function of `y` once `x` is fixed — and invokes the Cauchy criterion for
improper integrals, which needs nothing beyond `h∈C^1` and `h'∈L^1`. This is
elementary one-variable calculus, not a citation-only classical theorem
whose own hypotheses must be checked to "transfer" to a PDE-slice setting —
there is no abstract theorem's proof being re-run here, so the "transfer"
question (wave 26 Sec 5.1) genuinely does not arise. The mandate's concern
that this might "secretly still need something equivalent to what the
Tauberian apparatus provided" does not materialize on inspection: the
Tauberian theorem's distinctive content (converting Cesàro convergence into
ordinary convergence for a MERELY slowly-oscillating `g`) is not used or
needed, because the target's route establishes ordinary convergence of `h`
DIRECTLY (via absolute integrability of `h'`), which is strictly stronger
information than mere Cesàro convergence of `h` would have been. `(OSC-PHI)`
is correctly reported as remaining true and independently interesting, not
invalidated — merely off the critical path for `(U1)` specifically, exactly
as claimed.

---

## 5. Finding

**Finding 1 (LOW, cosmetic — no mathematical error).** Sec 4.2's prose
states the constructive subsequence works "for `k=0,1,2,3`" for each target
`v∈{-1,0,+1}`. Independently reproducing the construction
(`adv03_worked_examples.py`) confirms this holds exactly for `v=±1`, but for
`v=0` with the natural choice `θ_0=asin(0)=0`, `k=0` gives `y_k=e^{e^0}-3-x
= e-3-x <0` for `x>=0` — a **domain violation** (the whole construction is
about `y_k->infinity`, so a negative `y_k` is not a meaningful member of the
intended sequence, even though the trigonometric identity `sin(0)=0` still
holds algebraically at that point). Spot-checked against the target's own
`s02_cauchy_criterion_worked_examples.py`: the same `k=0` term appears there
too (`base_theta=mp.mpf('0')`, `k` looped over `[0,1,2,3]` uniformly across
all three targets, with no domain check on `y_k>=0`), and the script's own
`report(...)` call still passes because it only checks the algebraic
identity `sin(θ_k)=v`, not `y_k>=0`. **This does not affect the substantive
conclusion** — for `v=0`, `k=1,2,3` (and all higher `k`) already supply
infinitely many strictly-increasing, valid `y_k->infinity` hitting `0`
exactly, which is all the non-convergence argument needs; the demonstrated
"more than `10^100`-fold growth between consecutive `k`" claim is unaffected
and independently confirmed. Recommend, for a future front touching this
example again, either starting the `v=0` sequence at `k=1` or using the
supplementary-angle alternative the prose already parenthetically allows
("or the supplementary angle").

**No other issues found.** In particular: the "no new hypothesis introduced"
claim (VERDICT item 1, Sec 6), the "(H-ces) closed conditional on (B),(C'),
(U)" claim, the explicit `O(1/(x+y))` rate claims (Sec 3), and the
"bypasses the Tauberian apparatus entirely" claim (Sec 6) all survive
independent, from-scratch re-derivation.

---

## 6. Scope-discipline confirmation

- `grep -rn "random"` and `grep -rn "np\.random"` over the target's own
  `s01`–`s04` `.py` files: **zero matches** — no randomness used anywhere,
  matching the front's own claim.
- `grep -rn "git"` over the same files: only prose-comment substring hits
  (e.g. "digits" containing no such substring; actual hits were words like
  "legitimate" — no `git` command invoked). No `git` command was found in
  any script, and this referee ran none either.
- Reserved seed range `20260940000-20260940999`: `grep -rn "20260940"
  05_DISCOVERY_LAB/` shows it appearing only in `DECISION_LEDGER.yaml`'s own
  reservation line and the target's own `ATTEMPT.md` prose (both expected,
  neither a use) — genuinely unused.
- The target's own directory contains exactly the 9 files (`ATTEMPT.md` +
  4×`.py`/`.log` pairs) its own Sec 12 file table describes — no more, no
  fewer.
- No `adversarial/` directory existed prior to this referee's dispatch (this
  referee created it).
- A repository-wide `find -newermt` sweep around the front's working window
  was run as a sanity check; it is **inconclusive** by itself (the entire
  checked-out working tree shares similar filesystem timestamps from
  checkout, unrelated to this front's actual edits, and this referee did not
  run `git` to get an authoritative diff, per its own instructions) — but
  content inspection (the file-count match above, and this front's own
  detailed, itemized Sec 13 scope-discipline confirmation, consistent with
  every ancestor front's identical convention in this sub-lineage) gives no
  reason to doubt the front's own scope claims.

---

## 7. Overall assessment

This front makes a genuine, correct, and useful contribution: a simpler
argument than the classical-Tauberian route this sub-lineage had been
building since wave 25, closing `(H-ces)` — and hence, via wave 26's
already-recorded necessary-and-sufficient bridge, `(U1)` itself — under
**exactly** the same two open hypotheses, `(C')` and `(U)`, with no
enlargement of what they need to supply. `H1`/`(U1)`/`(U2)` correctly remain
formally OPEN, since `(C')` and `(U)` are not independently proved for the
real `Φ` — the document is scrupulously careful never to claim otherwise,
and this referee's independent re-derivation confirms that care is
warranted and honored throughout. The document's own recommendation (Sec
10 — a ninth/tenth wave should attack `(C')`/`(U)` directly, or pivot to a
real-`Φ` numerical solver) is sound and requires no revision.

**`H1`, `(U1)`, `(U2)` remain ABERTO/OPEN.** `φ_REDB`, `Φ_U(c)`,
`Φ_infinity(c)`, and the four-term asymptotic law of record are untouched.

---

## 8. Files in this directory

| file | role |
|---|---|
| `adv01_core_derivation_from_scratch.py`/`.log` | independent, from-scratch re-derivation of Sec 2.1's decomposition and `(QUANT-E)` bound, targeting item (a) of the dispatch mandate specifically |
| `adv02_quotient_tail_cauchy_telescoping.py`/`.log` | independent verification of the quotient-rule identity, tail-integral formula, Cauchy-criterion mechanics, the telescoping-sum cross-check, and the Sec 3 rate-transfer triangle inequality |
| `adv03_worked_examples.py`/`.log` | independent reproduction of both Sec 4 worked examples (positive `D/(x+y)` example and the `sin(log(log(x+y+3)))` sharpness/non-convergence example), including the Finding 1 domain-check |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was created or modified by
this referee. No `git` command was run by this referee.
