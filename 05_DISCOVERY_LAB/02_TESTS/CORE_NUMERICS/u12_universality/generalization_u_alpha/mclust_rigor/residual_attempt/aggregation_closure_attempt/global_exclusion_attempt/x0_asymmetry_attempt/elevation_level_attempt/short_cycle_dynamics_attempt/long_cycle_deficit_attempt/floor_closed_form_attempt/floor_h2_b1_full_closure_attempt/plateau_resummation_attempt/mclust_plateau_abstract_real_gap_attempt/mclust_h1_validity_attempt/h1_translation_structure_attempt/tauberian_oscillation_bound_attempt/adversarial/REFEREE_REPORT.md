# REFEREE REPORT — `TAUBERIAN-OSCILLATION-BOUND-ATTEMPT` (wave 26, front c, `DISC-DEC-123`)

**Hostile independent referee.** Target:
`.../mclust_h1_validity_attempt/h1_translation_structure_attempt/tauberian_oscillation_bound_attempt/ATTEMPT.md`.
Scope: pure combinatorial/asymptotic mathematics, `M-CLUST(b)` (Tree B of
`PROOF_DEPENDENCY_MAP.md`, node `PLATRESUM`) — standalone, unrelated to any
Millennium Prize Problem and unrelated to the archive's separate Tree A
(`U_α`/`u1/2`) line. This is the seventh consecutive wave (waves 20–26)
attacking the same `H1`/`(U1)`/`(U2)` gap in this exact sub-lineage.

**Method.** Read in full before opening any code: `PROOF_DEPENDENCY_MAP.md`'s
`PLATRESUM` node (full addenda history, `DISC-DEC-088/091` through
`DISC-DEC-122`); the predecessor's full
`h1_translation_structure_attempt/ATTEMPT.md` and its
`adversarial/REFEREE_REPORT.md` (including Finding 1's corrected framing);
`h1_energy_estimate_attempt/ATTEMPT.md` in full. All core claims — the
route-(a) dead-end mechanism, the entire `T0`/`T1`/`T2` decomposition and
each piece's bound, the kernel-uniformity numerics, and the `sin(log(1+t))`
counter-example — were independently re-derived **by hand and from scratch**
before the target's own `.py` scripts were opened. Only afterward were
`s01`–`s04` read, for cross-checking. All adversarial scripts here were
written fresh, without importing or copying code from the target or any
ancestor front.

---

## VERDICT

# SOUND WITH NAMED ISSUES

Every mathematical derivation examined — the `W=ε[M_yΨ+I]` identity, the
entire `T0`/`T1`/`T2` split and each sub-bound (`A_t`, `B_t`, the error
term), the closed-form-vs-crude-bound comparison for `T2`, the
Watson's-lemma IBP identity, and the `sin(log(1+t))` counter-example
(boundedness, exact relative-step oscillation bound, exact Cesàro-mean
closed form, and non-convergence) — was independently re-derived from
scratch and **confirmed correct**, with no arithmetic or logical error
found anywhere. All numerical claims checked (the predecessor
cross-validation point, the full `s02b` transition sweep, the `s02c`
`x=3` spot-check, and the counter-example's Cesàro mean up to `Y=10^8`)
were independently reproduced via a fresh `mpmath` implementation and
**matched the target's reported values to the digits given** in every
case. Two findings, both about *framing/emphasis*, neither a
mathematical error, one of them (Finding 2) genuinely worth the front's
attention going forward:

- **Finding 1 (LOW).** Sec 2.2's characterization of the
  `(M_{y2}-M_{y1})·Ψ(x,y1)` term as "fine" could mislead a reader — it is
  `O(δ·y1)` in absolute magnitude, exactly the same order as the
  `M_{y2}·Δ_Ψ(x)` term explicitly named "the wall," not a vanishing
  quantity. Does not affect the correctness of the "dead end" conclusion.
- **Finding 2 (MODERATE, constructive).** The document's own sharp new
  finding (Sec 6: the classical theorem needs `(H-ces)` as a third,
  separate hypothesis) has a sharper corollary the document does not
  quite state: **given the already-proved self-averaging bridge, `(H-ces)`
  alone is both necessary AND sufficient for `(U1)`, via elementary
  triangle-inequality reasoning — making the classical Tauberian
  theorem's oscillation hypothesis `(H-osc)`, and hence `(OSC-PHI)` itself
  (this front's central technical result, Sec 3–4), logically
  UNNECESSARY as a stepping stone toward closing `(U1)` via this specific
  bridge.** This reinforces, rather than contradicts, the document's own
  Sec 9 recommendation ("attack `(H-ces)` directly... rather than
  revisiting `(H-osc)`") — it supplies the precise logical reason for
  that recommendation. See Sec 4 below.

`H1`/`(U1)`/`(U2)` remain OPEN, exactly as the target states. **Confirmed
explicitly, as the mandate's "extreme caution" clause requires: nowhere
in this document is `(U1)` claimed to be closed** — the hedging is
consistent and accurate throughout (VERDICT UP FRONT item 5, Sec 6.3,
Sec 7 item 1, Sec 8's scorecard, Sec 9, Sec 12's final bullet). `φ_REDB`,
`Φ_U(c)`, `Φ_infinity(c)`, and the four-term asymptotic law of record are
untouched by both the target and this review.

---

## 1. Route (a) — independent re-derivation (mandate item 1)

Working only from the cited definitions ((E1), (KEY), (E2), `M_y`), this
referee independently derived, by hand, `W = Ψ - ε[(x+y)Ψ-I] = ε[M_yΨ+I]`
— confirmed symbolically, `adv01_from_scratch_identities.py` Check 1.
Splitting `M_{y2}Ψ(x,y2)-M_{y1}Ψ(x,y1) = M_{y2}Δ_Ψ(x)+(M_{y2}-M_{y1})Ψ(x,y1)`
(Checks 2–3) is exact algebra; `M_{y2}-M_{y1}=-(y2-y1)` confirmed exactly.

**The core diagnosis is correct.** `M_{y2}=1/ε-z2→-∞` as `y2→∞` while
`(⋆⋆)` bounds `|Δ_Ψ(x)|` only by `O(Δ/y1)=O(δ)` — this referee confirms
the product `M_{y2}·Δ_Ψ(x)` is genuinely `O(δ·y2)`, growing (not
vanishing) as `y1→∞` at fixed `δ`, and that there is no cancellation
partner analogous to `K_B` **visible within the (KEY)/(E2) identity
taken as an opaque, scalar bound** — i.e. treating `(⋆⋆)` as a black-box
sup-norm bound genuinely discards the fine structure (the `K_A^raw`/`K_B`
cancellation only becomes visible after unpacking `Ψ` via `(BB-Psi')`,
which is essentially route (b)'s own machinery, not route (a)'s). The
direct-route argument (Sec 2.3, `Δ_W=Δ_Ψ-ε·d/dx[Δ_Ψ]`, a genuine
derivative-loss issue since `(⋆⋆)` bounds a sup norm, not an
`x`-derivative) is standard and correct.

**Finding 1 (LOW, imprecise framing).** Re-examining Sec 2.2's own
numbers: `(M_{y2}-M_{y1})Ψ(x,y1) = -Δ·Ψ(x,y1)`, bounded by
`Δ·M_Ψ = δ·y1·M_Ψ` — **the same order, `O(δ·y1)`, as the term explicitly
called "the wall."** Calling this piece "fine ... poses no obstruction"
(ATTEMPT.md Sec 2.2) is true only in the sense that it is an *exact,
lossless* computation (no crude/lossy inequality applied beyond simple
boundedness), as opposed to the wall term, which combines an *unbounded*
coefficient with a bound (`(⋆⋆)`) independently known to be loose by
`10²`–`10³` (`h1_energy_estimate_attempt` Sec 5.2). The target's own
`s04` script says this more carefully than the prose in ATTEMPT.md
("fine, O(delta*y1), i.e. O(delta) after normalizing by z~y1 in a LATER
step") — but that normalization step never actually occurs anywhere in
the document (route (a) is abandoned before any such step), so as
written, a reader could come away thinking route (a)'s single genuine
obstruction is confined to the `M_{y2}Δ_Ψ` term while the rest of the
crude decomposition is already small — it is not; the *entire* crude
sum is `O(δ·y1)`, and the correct point is narrower: only the wall term
combines unboundedness with independently-known slack, so only it is a
plausible *entry point* for a sharper technique. **Does not change the
correctness of "route (a) is a dead end."**

---

## 2. Route (b) — independent re-derivation of `(OSC-PHI)` (mandate item 2)

The entire `T0`/`T1`/`T2` split was independently re-derived from
`(VOLTERRA-Phi)` by hand, confirmed to be an *exact* rearrangement (no
approximation) — splitting `∫_0^{y2}` at `y1` gives exactly the three
terms claimed, matching the target's Sec 3.1 verbatim.

- **`T0`**: trivial, `|T0|≤e^{-y1/ε}`. Confirmed.
- **`T2` (mandate's specific check: does the closed form genuinely beat
  the crude bound?).** Independently confirmed: crude operator-norm
  bound gives `|T2|≤Δ(√(π/2)+ε)M_Φ`, which for `Δ=δy1` is `O(δ·y1)` —
  genuinely useless (grows without bound at fixed `δ`). Using the
  closed-form kernel instead: `|T2|≤2ΔM_Φ/z2+ΔO(1/z2²)`, and since
  `(Δ/z2)/(Δ/z2²)=z2→∞` (independently confirmed,
  `adv01_from_scratch_identities.py` Check 5), the `O(Δ/z2)` term
  dominates; with `z2~y1(1+δ)` this gives `|T2|=O(δ)`, **uniformly in
  `y1`** — confirmed exactly as claimed, a genuine improvement.
- **`T1`'s bulk term `A_t` (mandate's specific check: is
  `|∫A_t dt|=O(δ)` correctly derived?).** Independently confirmed:
  `1/z2-1/z1=-Δ/(z1z2)` exactly (Check 4); `A_t` has this constant
  coefficient times `Φ_t(x)`, so `∫_0^{y1}A_t dt=-Δ/(z1z2)·A(y1)`, and
  `|A(y1)|≤y1M_Φ` gives `|∫A_t dt|≤M_Φ·(y1/z1)·(Δ/z2)≤M_Φ·Δ/z2=O(δ)`
  (using `y1/z1≤1` exactly for `x≥0`). **Correctly derived.**
- **`T1`'s localized term `B_t` (mandate's specific check: does it
  really need no smoothness assumption?).** Independently confirmed:
  bounding `|∫_0^{y1}e^{-h1/ε}Φ_{y1-h1}(x+h1)dh1|≤M_Φ·ε·(1-e^{-y1/ε})≤M_Φε`
  uses **only** the standing boundedness hypothesis `(B)` — no Lipschitz
  or closed-form-remainder assumption enters this specific sub-bound at
  all (it never invokes the closed form for `K` on this piece), so the
  claim is correct: `B_t`'s bound genuinely sidesteps the `(U)`-hypothesis
  concern that the *rest* of `T1` needs. Total `O(ε/y1)`, no
  `δ`-dependence. **Correctly derived.**
- **Error term and assembly**: `y1·O(1/z1²)=O(1/y1)` given uniformity of
  the closed form's remainder over the full `t∈[0,y1]` range (hypothesis
  `(U)`) — correctly identified as needing the "distant past" (`h1→y1`,
  i.e. `t→0`) regime no ancestor front tested. `|Φ_{y2}(x)-Φ_{y1}(x)|
  ≤C1δ+C2/y1` follows exactly as claimed, and is genuinely the
  relative-step form the classical Tauberian theorem needs.

**Independent re-derivation of the full `T0`/`T1`/`T2` chain: no gap,
no error found anywhere.** See `adv01_from_scratch_identities.py`.

---

## 3. Numerical verification of hypothesis `(U)` (mandate item 3)

A fresh, independent `mpmath` implementation of the raw kernel
definitions (`K_A^raw` via the single-integral reduction, `K_B`, `M_y`)
was built from scratch, with the same de-stiffening idea the lineage's
discipline requires (substitution `u=v/z` for the inner integral;
explicit breakpoints at multiples of `ε` for the outer integral) —
independently coded, not copied from the target's `s02`/`s02b`/`s02c`.

**Sanity check** (`adv02_kernel_uniformity_mpmath.py` Part 1): reproduced
the predecessor's published Sec 5.4 value
(`x=0,ε=0.1,f=1/(1+x),h=y/2,y=10`): this referee's implementation gives
`z·K(y,t)f(0)=0.915633339397...`, agreeing with the published
`0.9156333394` to `2.1×10⁻¹²` — the *identical* agreement figure the
target itself reports for the same cross-check.

**`s02b` regime reproduced** (Part 2, `ε=5,z=1000,x=0,f=1/(1+x)`, `h/y`
from `0.0002` to `0.99`): this referee's independent values —
`-0.1536, -0.1596, +0.3098, +0.4487, +0.4894, +0.4929` (stabilizing) —
**match the target's reported table digit-for-digit**
(`-0.154, -0.160, +0.310, +0.449, +0.489, +0.493`), with `max|z²err|`
converging to `0.4929` (target: `0.493`). No divergence anywhere,
including deep into the previously-untested `h/y→1` regime.

**`s02c` spot-check reproduced** (Part 3, `adv02b_xnonzero_spotcheck.py`,
`x=3,ε=0.1,z∈{200,1000}`, ratios `{0.1,0.5,0.9}`): this referee obtains
`z²·err=-0.0392` at `z=200` and `-0.0383` at `z=1000`, constant across
all three ratios at each `z` — matching the target's claimed `-0.039`
and `-0.038` essentially exactly.

**Conclusion: hypothesis `(U)`'s numerical support is independently
confirmed**, via a structurally different implementation, in exactly the
previously-untested regime the mandate asked to stress-test.

---

## 4. The `sin(log(1+t))` counter-example (mandate item 4) — the most
consequential claim, verified with special care

All four sub-checks independently re-derived from scratch
(`adv03_cesaro_counterexample.py`), **before** reading the target's
`s03_cesaro_gap_counterexample.py`:

**(a) Boundedness**: trivial, `|g(t)|≤1`.

**(b) The exact relative-step oscillation condition.** This referee
derived a **sharper, fully rigorous, non-asymptotic** version of the
target's claim: via `|sin A-sin B|≤|A-B|`,
`|g(s)-g(y)|≤log(1+(s-y)/(1+y))≤log(1+δ)≤δ` for **every** `y≥0` and
**every** `δ∈[0,1)` with `0≤s-y≤δy` — not merely a first-order Taylor
approximation (which is all the target's own derivation uses, backed by
spot numerical checks). This confirms, by a strictly stronger route, that
the target's claim ("bounded by 1 in absolute value for ALL `y≥0`") is
correct, and that `g` genuinely satisfies the theorem's **exact**
relative-step definition (`Y=0` suffices — even stronger than "eventually
true" — not a weaker or different condition). Numerically spot-checked
against exact `g` at `y∈{0,1,10,10³,10⁷}`, `δ∈{0.5,0.1,0.01,0.001}`: the
elementary bound holds in every case (worst observed ratio
`|g(s)-g(y)|/δ≈0.916<1`).

**(c)+(d) The exact Cesàro-mean closed form**, independently re-derived
via `t=e^u-1`: `sympy` gives
`∫sin(u)e^u du=-√2·e^u·cos(u+π/4)/2` — algebraically identical to
`(sin u-cos u)e^u/2` — and the definite integral
`∫_0^Y g(t)dt=-√2(Y+1)cos(log(Y+1)+π/4)/2+1/2` **matches the target's
stated closed form exactly** (symbolic difference `0`), confirmed by
direct differentiation (`d/dY[∫_0^Y g\,dt]-g(Y)≡0`, exact).
**Independent numerical quadrature** (not the closed form, not the
target's own numbers) of `∫_0^Y g(t)dt` at `Y=10,10²,...,10⁸` matches the
closed-form value to `<10⁻¹⁰` at every point, and reproduces the target's
own spot values almost exactly: at `Y=10⁷`, this referee gets
`g=-0.3987`, Cesàro mean `=0.2592` (target: `-0.399`, `0.259`); at
`Y=10⁸`, `g=-0.4158`, Cesàro mean `=-0.6626` (target: `-0.416`,
`-0.663`). **No trend toward convergence across 8 orders of magnitude in
`Y`** — both `g` and its Cesàro mean keep oscillating with amplitude
`√2/2≈0.707`, exactly as claimed. The self-caught harness bug (Sec 6.2,
comparing against the bare integration-variable symbol rather than `g`
evaluated at `Y`) was independently located in `s03`
(lines 98–105) and matches the document's description exactly — a
genuine harness bug, correctly diagnosed and fixed, not tainting the
underlying mathematics.

**(d) Is this really a "new finding," or an obvious/already-understood
requirement?** Independent judgment, as requested: **the underlying
mathematical fact is textbook-standard** — every Tauberian theorem, by
definition, upgrades a *weaker* summability notion (here, Cesàro-`(C,1)`)
to ordinary convergence given a regularity condition; the weaker
notion's convergence is *always* an explicit, foundational hypothesis
(see e.g. Hardy, *Divergent Series*, or any standard treatment of Abelian
vs. Tauberian theorems) — this is not a novel discovery in the wider
mathematical literature. **However, it genuinely was NOT stated
explicitly anywhere in this archive's own record before this front.**
Checked directly against the predecessor's own Sec 6.3 (quoted in full
above): its two named ingredients are (1) an oscillation bound on `Φ`
and (2) verification that *the classical theorem's proof* (not its
Cesàro-convergence hypothesis specifically) transfers to a PDE-slice
setting — nowhere does it, or `DISC-DEC-122`'s summary of it, flag
`(H-ces)` as a separate, unestablished requirement, even after the
referee's Finding 1 (which corrected the *logical framing* of the
self-averaging identity's relationship to `(U1)`, without going the one
further step of explicitly naming `(H-ces)` as a third theorem
hypothesis). So: **elementary in the wider literature, genuinely new
to this archive's own written record** — a fair, honestly-scoped
characterization of "genuinely new reduction beyond what `DISC-DEC-122`
already named," satisfying the wave-26 checkpoint's explicit bar.

---

## 5. Does a sharper conclusion follow? (constructive finding, beyond the mandate)

Independent analysis, not requested by name in the mandate but a direct
consequence of verifying mandate item 4 carefully: the self-averaging
identity `Φ_y(x)-A(y)/(x+y)→0` is proved **unconditionally** (given `(B)`,
`(C)`, and `t`-uniformity of the error term) — it does **not** need
`(H-osc)`/`(OSC-PHI)` in its own derivation (predecessor, Sec 6.1,
re-confirmed here by inspection). Given this bridge, the elementary fact
"two sequences differing by `o(1)` converge to the same limit iff either
one does" (already invoked by the predecessor's own referee, Finding 1)
means: **if `(H-ces)` — Cesàro convergence of `A(y)/(x+y)` — is
established by ANY means, `(U1)` follows immediately by the triangle
inequality, with no need for `(H-osc)`, `(OSC-PHI)`, or the classical
Tauberian theorem's machinery at all.** Conversely, the same
`sin(log(1+t))` counter-example that defeats `(H-osc)⇒`convergence
(Sec 6.2 Part 3) *also* shows `(H-bdd)+(H-osc)` gives **no leverage**
toward establishing `(H-ces)` itself (the counter-example's own Cesàro
mean also fails to converge) — so `(OSC-PHI)`, though a correctly-derived
new fact about `Φ`, offers no logical stepping-stone toward `(H-ces)`
either. Consistent with this: the document's own **one candidate future
route for `(H-ces)`** (Sec 7 item 2, bounding
`d/dy[A(y)/(x+y)]` via the self-averaging identity) does **not** use
`(OSC-PHI)` at all. Sec 9's recommendation ("attack `(H-ces)` directly...
rather than revisiting `(H-osc)`") is therefore not just good practical
advice but the logically forced conclusion — a sharper statement the
document could have made explicitly. This does **not** undermine
`(OSC-PHI)`'s correctness as an independent fact about `Φ`, nor the
value of Sec 6's `(H-ces)` finding; it tempers how much *practical*
credit should attach to Sec 3–4 (the front's largest technical
investment) toward the specific goal of closing `(U1)`.

---

## 6. Sections 5 and the mandate's remaining items

**Sec 5.1** (abstract-function transfer at fixed `x`): correct and
unremarkable — once `x` is fixed, `g(y):=Φ_y(x)` is literally an
abstract bounded function of `y`, and the classical theorem's proof
(about such functions) has no PDE-specific obstruction to invoking, once
`(OSC-PHI)` and `(H-ces)` are both in hand. **Confirmed.**

**Sec 5.2** (`x`-uniformity, bound gets better not worse as `x` grows):
independently re-traced through the `T0`/`T1`/`T2` derivation — every
bound obtained is `O(1/z1)` or `O(1/z2)`-type with `z1=x+y1≥y1`,
`z2=x+y2≥y2` for `x≥0`, so every term is automatically non-increasing in
`x`, **given** `(C')` and `(U)` hold uniformly in `x` (correctly flagged
as the residual caveat, spot-checked only at `x=0,3`). **Confirmed,
reasoning sound.**

**Mandate item 6 (self-caught bug disclosure)**: independently located
in `s03_cesaro_gap_counterexample.py` lines 98–105 — the description in
ATTEMPT.md Sec 6.2 and Sec 12 matches the actual code and comment
exactly; a genuine harness bug (comparing against the free symbol `t`
rather than `g.subs(t,Y)`), correctly diagnosed, fixed, and disclosed.
Does not taint the mathematical result (confirmed independently above,
Sec 4).

**Scope/seed/governance discipline** (`adv04_scope_seed_discipline.sh`/
`.log`): the reserved range `20260935000-20260935999` appears in the
archive only in the target's own prose and `DECISION_LEDGER.yaml`'s
`DISC-DEC-123` reservation line — no `random`/`seed`/`SeedSequence`
usage in any of the target's scripts, no `git` command anywhere. No
sibling front directory (`h1_volterra_attempt`, `h1_post_correction_
attempt`, `h1_energy_estimate_attempt`, `mclust_h2_validity_attempt`, or
the parent `h1_translation_structure_attempt` itself) shows a file
touched during or after this front's own work window (03:08–03:29 on
2026-08-29). `THEOREM.md`, `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.
md`, and `PROOF_DEPENDENCY_MAP.md` all predate that window at the time
of this front's work. **One nuance actively checked and resolved**:
during this review, `DECISION_LEDGER.yaml` and `THEOREM.md` acquired
*later* mtimes (03:52) — traced to a **newly-added, unrelated ledger
entry, `DISC-DEC-124`** ("Onda 26 frente (a) K-FREE-CONVERGENCE-BRIDGE-
ATTEMPT integrada..." — Tree A content, a different wave-26 front
entirely), confirming this is the orchestrating session integrating a
**sibling** wave-26 front concurrently, not an action by the reviewed
front (c) or by this review. `PROOF_DEPENDENCY_MAP.md` (the Tree B
document actually governing `M-CLUST(b)`) still does not mention
`TAUBERIAN-OSCILLATION-BOUND-ATTEMPT` anywhere, confirming no premature
integration of the reviewed front has occurred. `DISC-DEC-123`'s ledger
entry (front c) matches the target's stated mandate verbatim in
substance, including the explicit checkpoint clause. **All scope/seed/
governance discipline confirmed clean.**

---

## 7. Explicit confirmation on the mandate's "extreme caution" clause

Read in full: the document does **not** anywhere claim `(U1)` is closed.
VERDICT UP FRONT item 5 states plainly "`(U1)`/`(U2)` do NOT close";
Sec 6.3 states the same for the specific reduction found here; Sec 7
item 1 restates it; the Sec 8 scorecard marks `(U1)`, `(U2)`, `H1` all
`OPEN (unchanged)`; Sec 9's recommendation is framed around *future*
work, not a claim of present success; Sec 12's final bullet explicitly
addresses the mandate's caution and is accurate. **The honest
non-closure framing is consistent, accurate, and neither overstated nor
understated anywhere in this document.**

---

## 8. Files in this directory

| file | role |
|---|---|
| `adv01_from_scratch_identities.py`/`.log` | independent symbolic re-derivation (sympy) of the `W=ε[M_yΨ+I]` identity, the `M_{y2}-M_{y1}` algebra, the `T1`/`T2` elementary identities (`1/z2-1/z1=-Δ/(z1z2)`, the `O(1/z)`-dominates-`O(1/z²)` ratio check), the single-integral reduction of `K_A^raw` re-derived independently from the raw `(w,u)` definitions, and the Watson's-lemma IBP identity confirmed on a concrete test function (Sec 1–2 above) |
| `adv02_kernel_uniformity_mpmath.py`/`.log` | independent from-scratch `mpmath` re-implementation of the raw kernel (`K_A^raw`, `K_B`, `M_y`), de-stiffened via `u=v/z`; reproduces the predecessor's published Sec 5.4 cross-check (agreement `2.1e-12`) and the target's `s02b` combined transition+large-`h` sweep (`ε=5,z=1000`), matching the reported table digit-for-digit (Sec 3 above) |
| `adv02b_xnonzero_spotcheck.py`/`.log` | independent reproduction of the `s02c` `x=3` spot-check, matching the target's reported `z²·err` values (Sec 3 above) |
| `adv03_cesaro_counterexample.py`/`.log` | independent symbolic (sympy) and numerical (mpmath, direct quadrature to `Y=10⁸`) verification of the `sin(log(1+t))` counter-example, including a sharper, fully rigorous (non-Taylor-approximate) relative-step oscillation bound derived independently (Sec 4 above) |
| `adv04_scope_seed_discipline.sh`/`.log` | scope/seed/governance-file discipline audit, including the `DISC-DEC-124`-traced clarification (Sec 6 above) |
| `REFEREE_REPORT.md` | this document |

No file outside this `adversarial/` subdirectory was modified. No `git`
command was run. No claim of progress on any Millennium Prize Problem
appears anywhere in this report — `M-CLUST(b)` is a standalone
combinatorial/asymptotic object, as stated throughout the target and its
required reading.
