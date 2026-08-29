# REFEREE REPORT — `CU-DIRECT-PROOF-ATTEMPT` (wave 29, front a, `DISC-DEC-134`)

**Hostile independent referee.** Target:
`.../h_ces_direct_attempt/cu_direct_proof_attempt/ATTEMPT.md`. Scope: pure
combinatorial/asymptotic mathematics, `M-CLUST(b)` (Tree B of
`PROOF_DEPENDENCY_MAP.md`, node `PLATRESUM`) — standalone, unrelated to any
Millennium Prize Problem and unrelated to the archive's separate Tree A
(`U_α`/`u1/2`) line. This is the tenth consecutive wave (waves 20–29)
attacking the `H1`/`(U1)`/`(U2)` gap in this exact sub-lineage, and the
first to attack the two named hypotheses `(C')`/`(U)` directly rather than
another convergence architecture.

**Method.** Read in full, in the order specified by the dispatching
mandate, before opening any of the target's own scripts: the immediate
predecessor `h_ces_direct_attempt/ATTEMPT.md` (wave 28, front a) in full,
plus its own `adversarial/REFEREE_REPORT.md`; `h1_translation_structure_
attempt/ATTEMPT.md` (wave 25, grandparent) in full, for the closed-form
kernel `K(y,t)`, the operator definitions `K_B`, `M_y`, `K_A^raw`, and the
formal Mills-ratio asymptotic series this front's Sec 2 replaces with a
rigorous bound; `tauberian_oscillation_bound_attempt/ATTEMPT.md` (wave 26)
in full, especially its Route (a) dead-end (Sec 2) — the "unbounded
coefficient with no cancellation partner" diagnosis this front's Sec 5
explicitly compares itself against; and `PROOF_DEPENDENCY_MAP.md`'s dated
addenda under `DISC-DEC-122`, `DISC-DEC-125`, `DISC-DEC-132` for the
orchestrating session's own precise record of `(B)`, `(C')`, `(U)`. Only
then the target's own `ATTEMPT.md` in full, then its scripts
(`s01`–`s05`, plus `s04b`–`s04d`).

The orchestrating session's own pre-dispatch spot-check (fresh `sympy`,
zero discrepancy) already confirmed: the ODE `w1'=z*w1-2/(1+z²)²`; that
the closed-form integral solves it; the Sec 3.2 coefficient-regrouping
identities; and the Sec 5.1 pointwise derivative-under-the-integral-sign
identity. This report does **not** re-verify those four items — it
targets everything the pre-dispatch spot-check did *not* cover, per the
dispatch mandate's six lettered items (a)–(f), each addressed below with
independent, from-scratch derivation and/or fresh numerical
reproduction — no `.py` file from the target or any ancestor front was
opened before this referee's own independent re-derivation of each item
was complete; the target's own scripts were read only afterward, for
cross-checking arithmetic and provenance. All adversarial scripts in this
directory (`adv01`–`adv05`, plus `adv04b`) were written fresh, importing
nothing from the target or any ancestor front.

---

## VERDICT

# SOUND WITH THREE NAMED ISSUES, ALL LOW SEVERITY (FRAMING/DOCUMENTATION, NO MATHEMATICAL ERROR) — ACCEPT FOR CATALOGUE

`(U)` is **genuinely PROVED**, conditional on `(B)`+`(C'')` — not merely
numerically tested — via a real new technical engine (a fully rigorous,
non-asymptotic integrating-factor comparison lemma for the Mills-ratio
function `R(z)`), independently re-derived from scratch here and confirmed
correct at every step, including an end-to-end numerical test of the full
assembled theorem that this report performed directly against the RAW
kernel operator definitions (not the target's own intermediate formulas).
`(C')` is **genuinely reduced, not proved**, to a single, precisely-named
Volterra-resolvent stability question of the same logical type as
hypothesis `(B)` itself — the new `(DX-K)` identity underlying this
reduction was independently re-derived and verified numerically to ~15
digits, including every correction term computed from its own raw
definition. The Sec 4 sharpness investigation's three numerical claims —
non-adversarial kink shows no degradation, adversarially-aligned kink
shows genuine pointwise `O(1/z²)` degradation, the aggregate quantity
self-heals back to `O(1/z³)` — were independently reproduced with fresh
code to the target's own published precision (`z²|E|→0.2208`,
`z³|E|(z=15000)=3312.42`, `z³|Efull|→0.936`, all matched), and the
pointwise-degradation phenomenon was further confirmed to be robust
across a second, differently-shaped kink function. Three LOW-severity
issues were found (below); none affects any substantive mathematical
claim. `(H-ces)`, `(U1)`, `(U2)`, `H1` correctly remain formally OPEN.

---

## Item (a): Sec 2's sharper upper bound `R(z) ≤ v(z)`, and the Sec 3.2
bracket

Independently re-derived from scratch (`adv01_sharper_bound_and_bracket.py`,
never having opened the target's own `s01b`), via the identical
integrating-factor technique applied to a fresh comparison function
`w4(z):=v(z)-R(z)`, `v(z):=(z²+2)/(z(z²+3))`.

**This report's derivation is, in one respect, STRICTLY MORE RIGOROUS than
the target's own `s01b`**: the target's `s01b` Part 1 checks the sign of
the ODE's forcing term at only 8 sampled `z` values. This report instead
computes the forcing term (`z·v(z)-1-v'(z)`) in **exact closed form** and
finds it equals `6/(z²(z²+3)²)` identically — a manifestly positive
rational function for *every* `z>0` at once, not a sampled claim. This
proves `R(z)≤v(z)` for all `z>0` unconditionally, confirming the target's
sharper bound holds with no gap in the argument.

The two-sided bracket needed in Sec 3.2, `1/(1+z²) ≤ 1-z²σ(z) ≤ 3/(z²+3)`,
is then confirmed to follow *exactly* (symbolic algebra, zero residual)
from combining the `G1` lower bound (`R≥z/(1+z²)`) with this sharper
upper bound — and to hold numerically across a 13-point grid spanning
`z∈[10⁻³,10⁵]`, zero violations. **Confirmed in full.**

---

## Item (b): Sec 3.3's residual bound — genuinely two independent routes,
or does it just look that way?

Independently re-derived `ρ(h',z) = ∫₀^∞ f'(x+h'+u)·Q_u(z)du` via
integration by parts on the original `ρ` definition
(`adv02_rho_and_E_routes.py`, Part 1) — confirmed exactly via the same
exponent-identity technique as `s01`.

**The two bounding routes ARE genuinely, mathematically independent
techniques**, verified here in detail: Route B (the one actually derived
in the target's own `s03` code, via the pointwise majorization
`R(u+z)≤1/z`) and Route A (asserted in `s02`'s summary print statement and
used in `s03`'s Part 3, via `R''(z)`) use *opposite directions* of the
`G1` bracket. This report independently derives Route A's underlying
claim from scratch, via a double-integral swap distinct from Route B's
argument, and finds it is not merely a bound but an **exact identity**:
`∫₀^∞ u·Q_u(z) du = R''(z)/2` — confirmed to full `mpmath` precision. So
the two routes are real, independent mathematics, and their coincidence
in the *final numeric formula* `L2/(z(1+z²))` is a genuine (not
accidental) consequence of `R''(z)` and `σ(z)` being algebraically linked
(`R''(z) = [1-σ(z)(1+z²)]/z`, verified here), while remaining genuinely
distinct quantities.

**Finding 1 (LOW, documentation gap, not a mathematical error).** Route
A's core identity (`∫u·Q_u(z)du = R''(z)/2`) — which this report has now
independently derived and confirmed true — is **never actually derived
anywhere in the target's own committed scripts** (`s01`, `s02`, `s03`).
It appears only as a bare, undecorated formula in `s02` Part 4's summary
print statement and is reused in `s03` Part 3's `bound_route_A` function
with no derivation shown. Only Route B is genuinely derived, step by
step, in code. The "TWO independent bounding routes, cross-checked"
framing (ATTEMPT.md Sec 3.3) is therefore mathematically accurate but
somewhat overstates what the committed artifact trail itself demonstrates
— Route A's derivation exists only in this referee's own reconstruction,
not in the target's own scripts.

---

## Item (c): Sec 3.4's final assembled theorem

Rather than re-trace the coefficient algebra symbolically (the
regrouping identities were already confirmed with zero discrepancy by
the orchestrating session's pre-dispatch spot-check), this report performs
a **decisive, independent, end-to-end NUMERICAL test**
(`adv03_full_assembly_check.py`): computing `K(y,t)f(x)` **directly from
the RAW operator definitions** (`K_B`, `K_A^raw`'s single-integral
reduction, `M_y` — cited record facts, not the target's own derived
intermediate quantities) for a concrete `C^∞` test function with
independently-measured `M_Φ` and `L2`, and checking the claimed
`D(x,ε)/z²` bound directly.

**Result: all 17 tested `(x,ε,h,z)` combinations — `x∈{0,0.02,1}`,
`ε∈{0.05,0.1,0.5}`, `h∈[0.1,2.0]`, `z∈[5,500]`, including `h` close to
`ε` and small `x` — satisfy the bound**, with comfortable (not
razor-thin, not absurdly loose) margins, `actual/bound` ratios typically
`0.02`–`0.17`. This confirms the full chain of inequalities from Sec 3.2
+ Sec 3.3 genuinely composes to the claimed bound, with correct handling
of the `(1-εz)/ε` prefactor (an algebraic re-check of this specific step
also confirms: `|1-εz|≤1+εz` triangle-inequality, then
`(1+εz)·L2/(z(1+z²)) = L2/(z(1+z²))+εL2/(1+z²) ≤ L2(1+ε)/z²` for `z≥1`,
matching Sec 3.4 exactly). **Confirmed in full.**

---

## Item (d): Sec 4's sharpness investigation — the most delicate part

Independently reproduced the target's own three numerical experiments
with fresh code (`adv04_sharpness_reproduction.py`), using the target's
exact `a0=0.1`, `ε=0.5` parameters to check the SPECIFIC published
numbers:

- **Adversarially-aligned pointwise `E(h',z)` (s04c reproduction):**
  `z²|E| → 0.22082783...` (published: `0.2208`), `z³|E|` at `z=15000`
  `= 3312.4175...` (published: `3312.42`) — **matched to full precision.**
- **Aggregate `Efull` self-healing (s04d reproduction):** `z³|Efull| →
  0.9362995...` (published: `0.936`) — **matched to full precision.**

These are genuine, correctly-computed findings, not errors or artifacts.

**Robustness beyond the one tested function** (`adv04b_fresh_kink_
robustness.py`): a fresh, DIFFERENTLY-SHAPED kink (a one-sided ramp
`0.6·max(0,a-b0)` rather than the target's two-sided `0.3|a-a0|`, same
derivative-jump magnitude, different location `b0=0.25`, different
`ε=0.3`, nonzero `x=0.05`) was tested with the same adversarial-alignment
protocol. The **pointwise degradation phenomenon reproduces robustly**:
`z²|E|` converges cleanly to `≈0.2206` (essentially the same magnitude as
the target's `0.2208`, consistent with the matched jump size) as `z`
sweeps `20→15000` — confirming this is not an artifact of the one
specific function tested. The **aggregate self-healing test on this
second function was less decisive**: `z³|Efull|` did not diverge, but
climbed slowly and had not clearly plateaued by `z=500`
(`0.0586→0.0511→0.1137→0.1358→0.1444`, decelerating: ratio `1.19` from
`z=80→200`, `1.06` from `z=200→500`) — consistent with, but not as clean
a confirmation of, self-healing as the exact reproduction on the target's
own function. This is reported honestly here as suggestive-but-not-fully-
resolved for the second function, rather than overstated in either
direction; a longer sweep (`z>500`) would be needed to settle it, and was
not attempted given the diminishing marginal value against time invested.

**Assessment of Sec 4.3's "boundary-layer self-healing" framing**: this
is a fair, honest characterization of a genuinely open, delicate
phenomenon. The target does not claim it is general (Sec 4.4: "confirmed
for exactly ONE concrete adversarial test function... no claim is made
that it holds for every possible Lipschitz-only `f`") and does not claim
it resolves whether `(C')` alone suffices for the full `(U)`. This
referee's independent numbers (exact reproduction plus a second, honestly
partial, test) support treating this exactly as the target does: real,
interesting, precisely characterized, genuinely open.

---

## Item (e): Sec 5's Volterra-resolvent reduction

**Full `(DX-K)` identity, independently verified** (not just the
pointwise derivative-under-the-integral identity already spot-checked by
the orchestrating session): `adv05_dxk_identity_and_gronwall.py` Part A
computes *every* term — the LHS via finite difference on the full raw
double integral, and the RHS's three pieces (`K(y,t)[f']`, `K_A^raw(y,t)f`,
and, crucially, `N(y,t)f(x)` computed **directly from its own raw
double-integral definition**, not inferred from a residual) — and finds
the identity holds to `~10⁻¹⁵` (limited by the finite-difference step, as
expected) across 4 fresh `(x,ε,h,z)` cases. This is a stronger, more
direct test than the target's own `s05` Part 3, which only checks that
`dKdx-K[f']` is `O(1/z)`, not that it equals the negative of the full
correction term to high precision.

The `O(1/z)` bounds on `K_A^raw` and `M_y·N(y,t)f(x)` were re-traced
algebraically and confirmed to use **only `(B)`+`(C')`** (specifically:
the `N`-piece bound needs only `(B)`; the `K_A^raw`-piece's `ρ`-integral
sub-bound needs `(C')`'s Lipschitz constant `L1` for `f` itself, not any
`C''`-type bound on `f'`) — exactly as claimed, no silent strengthening.

**Finding 2 (LOW, conceptual imprecision, not a computational error).**
`√(π/2)≈1.2533` is correctly stated. But the claim that Gronwall's bound
"EXPONENTIATES ... because `√(π/2)≈1.2533>1`" is not quite the right
diagnosis: standard Gronwall applied to a Volterra memory-integral
inequality `u(y)≤a+∫₀^y C·u(t)dt` with a *constant* kernel bound `C`
gives `u(y)≤a·e^{Cy}`, which diverges as `y→∞` for **any** fixed `C>0` —
including `C<1` — not only for `C` exceeding `1` (confirmed here
numerically for `C=0.3`, `0.9`, `1.2533`, all three diverge). The `>1`
threshold is not actually significant for this type of estimate (unlike,
say, a discrete contraction-mapping iteration where `<1` vs `>1` would
matter). This is consistent with the lineage's own already-recorded fact
(`DISC-DEC-115`) that the Picard/Neumann series in fact converges at each
fixed `y` via *factorial* suppression from the iterated-integral simplex
volume, not because the crude kernel bound is `<1`. The target's
**substantive conclusion — naive Gronwall on the crude constant operator
norm fails to give a useful `y`-uniform bound — remains correct**; only
the specific stated reason is imprecise.

**Finding 3 (LOW, apt-but-overstated comparison).** Is this "the
identical failure mode as wave 26's route (a)"? Re-reading wave 26's own
Sec 2.2 closely for this comparison: that failure was an *individually
unbounded* coefficient (`M_{y2}~-z2→-∞`) multiplying a term bounded only
by `O(Δ/y1)`, with no cancellation partner — a direct algebraic
divergence of one specific product term. The target's Gronwall failure
here is a *different* mechanism: a classical differential-inequality
argument applied to a **bounded** (though `>1`) constant kernel bound
over a domain of *growing length*, yielding an exponentially-growing a
priori estimate via general Gronwall theory. Both are genuine instances
of "a naive/crude bound fails for a `y→∞` argument in this system, a
sharper structural argument is needed instead" — a fair higher-level
analogy — but the precise mechanisms differ (unbounded-coefficient-with-
no-cancellation-partner vs. constant-bound-exponentiates-via-Gronwall-
over-a-growing-domain), so "identical failure mode" somewhat overstates
the parallel. Neither finding affects the substance of Sec 5.3's honest
conclusion: the naive route fails, and `(C')` remains a genuine
reduction, not a proof.

---

## Item (f): is the overall verdict honestly and precisely stated?

**Yes.** Every substantive claim independently checked above survives:
`(U)` is genuinely proved conditional on `(B)`+`(C'')` (Sec 3, confirmed
via full independent re-derivation plus an end-to-end numerical test
against raw kernel definitions); `(C')` is genuinely reduced, not proved
(Sec 5, confirmed via full independent verification of `(DX-K)` and its
`O(1/z)` correction bound); the Sec 4 sharpness investigation's three
seemingly-in-tension claims are all independently confirmed, and the
"open, not resolved either way" framing for whether `(C')` alone suffices
for the aggregate `(U)` is honest, not hedging toward an overclaim. The
document states plainly and repeatedly, in the VERDICT UP FRONT and
throughout Secs 3–5, 8–9, that `(H-ces)`/`(U1)`/`(U2)`/`H1` remain
formally OPEN because `(C')` is unproved and even `(U)`'s proof is
conditional on the new `(C'')`. No `THEOREM.md`-tier claim of closure
appears anywhere. This is a genuinely careful, non-overclaiming document.

---

## Scope-discipline / governance confirmation

- `grep -rn "random"` over the target's own `s01`–`s05` (and `s04b`–`s04d`)
  `.py` files: **zero matches** — no randomness used anywhere, matching
  the front's own claim.
- `grep -rn "\bgit\b"` over the same files: **zero matches** — no `git`
  command invoked by any script; this referee ran none either.
- Reserved seed range `20260942000-20260942999`: `grep -rn "20260942"
  05_DISCOVERY_LAB/` shows it appearing only in `DECISION_LEDGER.yaml`'s
  own `DISC-DEC-134` reservation line, the target's own `ATTEMPT.md`
  prose (both expected, neither a use), and one passing mention in a
  *sibling* wave-29-front's own referee report (`gamma_c_gamma_
  construction_attempt/diagonal_2f0_sum_attempt/adversarial/
  REFEREE_REPORT.md`, listing sibling seed blocks `20260942`/`43`/`44`
  reserved for wave 29 fronts a/b/c side by side — a documentation
  reference, not a use) — genuinely unused.
- The target's own directory contains exactly the files its own Sec 12
  file table describes (`ATTEMPT.md` + `s01`/`s01b`/`s02`/`s03`/`s04`/
  `s04b`/`s04c`/`s04d`/`s05`, each with a matching `.log`) — no more, no
  fewer, before this referee's `adversarial/` subdirectory was added.
- A repository-wide `find -newermt` sweep in the target's own working
  window (2026-08-29 07:55–08:05) found files modified outside the
  target's own directory, but every one belongs to the *other two*,
  clearly-separate wave-29 fronts (`diagonal_2f0_sum_attempt` = front b,
  `k5_exact_closure_attempt` = front c, both under the unrelated Tree A
  `gamma`/algebraic-closure sub-lineage) running in parallel per
  `DISC-DEC-134`'s own three-front mandate, plus `THEOREM.md`/
  `DECISION_LEDGER.yaml`/`DISCOVERY_LAB_STATE.md` edits traced to
  `DISC-DEC-135` (front b's *own*, already-completed integration —
  confirmed by reading that ledger entry directly; it is about
  `DIAGONAL-2F0-SUM-ATTEMPT`, not about this target). No `DISC-DEC-13x`
  ledger entry exists yet for this target front (`cu_direct_proof_
  attempt`/`H-CES-DIRECT-ATTEMPT`'s successor is not yet integrated,
  consistent with its own claim that no `THEOREM.md`/`PROOF_DEPENDENCY_
  MAP.md`/`DECISION_LEDGER.yaml` file was opened for writing by this
  front). No evidence this target front itself touched anything outside
  its own `cu_direct_proof_attempt/` directory.
- No `adversarial/` directory existed prior to this referee's dispatch
  (this referee created it).

---

## Overall assessment

This front makes a genuine, substantial, correct contribution: the first
rigorous (non-asymptotic-series) proof of `(U)` in this ten-wave
sub-lineage, via a real new technical engine (the Gordon-type Mills-ratio
double inequality), conditional on a mild, precisely-named, honestly-
flagged strengthening `(C'')` of the standing `(C')`; and a genuine,
precise reduction (not a proof) of `(C')` itself to a Volterra-resolvent
stability question of the same difficulty class as hypothesis `(B)`,
which no front across all 29 waves of this lineage has ever attempted.
The Sec 4 sharpness investigation is a genuinely delicate, honestly
double-sided piece of work — this referee's independent reproduction
confirms both the pointwise degradation and the aggregate self-healing
findings are real and correctly computed, not artifacts, and confirms
the front's own "left OPEN, not resolved either way" framing for the
deeper question is the right level of caution. Three LOW-severity
findings (a documentation gap in Route A's derivation trail; an imprecise
"`>1`" diagnosis for why Gronwall fails; an overstated comparison to wave
26's route (a) failure mode) are disclosed above — none affects any
substantive claim, and all are of the same character and severity as
findings already logged repeatedly by prior referees in this exact
sub-lineage.

**`(H-ces)`, `(U1)`, `(U2)`, `H1` remain ABERTO/OPEN.** `φ_REDB`,
`Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of record are
untouched.

---

## Files in this directory

| file | role |
|---|---|
| `adv01_sharper_bound_and_bracket.py`/`.log` | independent, from-scratch re-derivation of the sharper Mills-ratio upper bound `R(z)≤v(z)` (with an EXACT, not spot-checked, sign proof of the ODE forcing term) and the Sec 3.2 two-sided bracket — item (a) |
| `adv02_rho_and_E_routes.py`/`.log` | independent re-derivation of `ρ(h',z)`'s IBP representation, and an examination of whether the "two independent bounding routes" for `E(h',z)` are genuinely independent (yes) and fully derived in the target's own scripts (Route A is not) — item (b) |
| `adv03_full_assembly_check.py`/`.log` | decisive end-to-end numerical test of the Sec 3.4 assembled theorem, computing `K(y,t)f(x)` directly from raw operator definitions across 17 `(x,ε,h,z)` combinations — item (c) |
| `adv04_sharpness_reproduction.py`/`.log` | independent, fresh-code reproduction of the target's own `s04c`/`s04d` experiments and specific published numbers — item (d), part 1 |
| `adv04b_fresh_kink_robustness.py`/`.log` | robustness test of the Sec 4 phenomena with a fresh, differently-shaped kink function and parameters — item (d), part 2 |
| `adv05_dxk_identity_and_gronwall.py`/`.log` | full independent verification of the `(DX-K)` identity (every term from its own raw definition) and an examination of the Gronwall/wave-26-comparison claims in Sec 5.3 — item (e) |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was created or modified
by this referee. No `git` command was run by this referee.
