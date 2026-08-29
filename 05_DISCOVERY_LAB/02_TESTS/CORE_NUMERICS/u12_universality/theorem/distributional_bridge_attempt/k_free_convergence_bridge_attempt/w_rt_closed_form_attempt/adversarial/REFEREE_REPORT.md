# Referee report: `W-RT-CLOSED-FORM-ATTEMPT` (wave 27, front (b), `DISC-DEC-127`)

**Target:** `.../distributional_bridge_attempt/k_free_convergence_bridge_attempt/w_rt_closed_form_attempt/ATTEMPT.md`

## VERDICT: SOUND WITH NAMED ISSUES — ACCEPT

The target's central claim — a general closed form `W(r,t)=(t+2r+1)(t+r)!`,
a general closed form for the resulting `K`-symbolic sum `S(K,t)=
Γ(t/2+1)/Γ(K+t/2+1)`, and the consequent proof of Claim B
(`M_K'\overset d=M_K`) for **every** `K\ge1`, upgrading the predecessor's
Main Theorem `sup_x|F_n^{(K)}(x)-F_K(x)|\le8K^2/n` from conditional to
**unconditional** — is **mathematically correct**. I re-derived every
non-trivial step from scratch, independently of both the target's and the
predecessor's code, and found no error that survives to the final result.
I did find one genuine, non-trivial exposition flaw in the target's own
written derivation (Section 3.3), which I traced, diagnosed, and confirmed
does **not** affect the correctness of the conclusion. I also flag one
minor, low-severity process/disclosure point (item 7 below). Nothing found
here changes the verdict on the mathematics: **the escalation to an
unconditional Main Theorem is sound.**

---

## Summary of independent work

I read, in full, before opening any target script: the predecessor's
`ATTEMPT.md` (`k_free_convergence_bridge_attempt/`, wave 26 front (a)),
its `find_W_pattern.py`/`.log` and `verify_MK_moments.py` (for `W(r,t)`'s
exact computational definition), `THEOREM.md` "Estágio 47", and only then
the target's own `ATTEMPT.md` and its five `.py`/`.log` files.

I then wrote five fresh, independent verification scripts
(`adversarial/adv1..adv5_*.py`, logs alongside), none importing any code
from the target or the predecessor, covering the mandate's seven items.
Every script ran clean on its final version; two of my own scripts had
bugs on first draft (documented honestly below and in the scripts'
comments) that I caught, diagnosed, and fixed before drawing any
conclusion from them — none of these bugs were in the target's work.

---

## Item 1 & 2: `W(r,t) = (t+2r+1)(t+r)!` — definition, derivation, numerics

**Definition transcription.** I independently re-implemented `W(r,t)`'s
exact monomial-expansion definition from `find_W_pattern.py`'s prose (two
separate fresh code paths: a `sympy.Poly`-based route and a
stars-and-bars/`Fraction` route — `adv1_W_fresh_definition.py`). Both
reproduce the predecessor's `find_W_pattern.log` values exactly (`t=1..4,
r=0..7`) and match the closed form on **110** cells (`r=0..10, t=1..10`),
extending well past the predecessor's own `t=1,2`-only closed forms and
past the target's own `99`-cell check. All match exactly.

**Independent re-derivation (not pattern-matching).** I derived the
closed form by hand from the raw definition (all-diagonal Prop-S monomial
+ `r` doubled-at-`b` monomials, multiplied against the conditional-moment
multinomial expansion, summed over compositions), confirming:

- Per-composition contribution of the all-diagonal term:
  `r!·t!·(k_D+1)`.
- Per-composition contribution of the doubled-at-`b` term:
  `r!·t!·(k_b+2)`.
- Summing over all `N=C(t+r,r)` compositions, using the standard
  "average slot value" symmetry fact `Σk_D=Σk_b=tN/(r+1)`, telescopes
  cleanly to `W(r,t) = r!·t!·N·(t+2r+1) = (t+r)!·(t+2r+1)` (since
  `r!·t!·N = r!·t!·(t+r)!/(t!r!) = (t+r)!`).

This confirms `W(r,t)=(t+2r+1)(t+r)!` **matches my own from-scratch
derivation exactly**, and (mechanically) reduces correctly to the
predecessor's `t=1,2` formulas. `adv2_derivation_check.py` checks every
sub-step symbolically and against direct per-composition evaluation
(`r=3,t=4`, all compositions, exact match).

**Named issue (exposition, not correctness) — Section 3.3 of the
target's `ATTEMPT.md`.** The target's own displayed derivation states
that "the combined coefficient times `∏(exps[i]!)` collapses to exactly
`t!·(k_D+1)`" (correct, as an isolated per-composition claim, if read as
excluding Prop S's own `r!` prefactor), but the very next displayed line —
"Summing over all `N` compositions... `W(r,t) = r!\big[(tN/(r+1)+N) +
r(tN/(r+1)+2N)\big]`" — **silently drops the `t!` factor** that the
preceding paragraph just established. I checked this literally
(`adv2_derivation_check.py`, Part 3): the bracket formula **as written**
disagrees with the true `W(r,t)` at every tested `t\ge2` (`48/56` mismatched
cells; the `t=1` cells can't distinguish the bug since `1!=1`). The very
next line of the target's own box then reinserts an unexplained `·t!`
factor ("`r!\cdot\frac{(t+r)!}{t!\,r!}\cdot t!\cdot(t+2r+1)`") to land on
the correct final boxed answer. So the target's Section 3.3, **read
literally as a derivation**, has an internal inconsistency — a factor of
`t!` is dropped then silently reinstated with no algebraic justification
shown for either move. This is a genuine gap in the *written exposition*
of "derived, not pattern-matched" — a careful reader following the display
formulas literally cannot get from one line to the next.

**This does not affect Result 1's correctness.** The final boxed formula
`(t+2r+1)(t+r)!` is right, confirmed three independent ways: (a) my own
corrected from-scratch re-derivation with the `t!` factor tracked
correctly throughout (`adv2`), (b) 110 fresh numeric cells (`adv1`), and
(c) the target's own 99+32 numeric cells. I recommend the orchestrating
session ask a future pass to patch Section 3.3's displayed intermediate
line to include the `t!` factor explicitly (or state clearly that "N"
there is being used loosely) — a documentation fix, not a mathematical
one.

---

## Item 3: the self-disclosed Gosper false lead (Section 5.4)

Independently reproduced, via completely fresh code
(`adv3_gosper_reproduction.py`, different variable-construction order and
helper structure from the target's `symbolic_K_sum_attempt.py`):

- **Mandate's literal Step 2** (`sympy.summation`/`gosper_sum` on `S(K,t)`
  directly, symbolic `K`): closes for even `t` (`t=2,4,6,8` →
  `1/Γ(K+2)`, `2/Γ(K+3)`, etc.), returns `None` (certified non-existence
  of a hypergeometric antidifference) for odd `t` and for symbolic `t`.
  Matches the target's Section 5.1 table exactly.
- **The three-way Gosper-differencing discrepancy**: independently
  reproduced exactly — `Form 1` (raw `sp.binomial`, no pre-simplify) →
  `None`; `Form 2` (same expression, `sp.simplify()` first) → `0`; `Form
  3` (explicit factorial-ratio binomial) → `None`. I added a fourth form
  (`sp.expand()` instead of `sp.simplify()`) as an extra check: also
  `None`. **Confirmed: this is a genuine, reproducible `sympy`/Gosper
  subtlety** (how `simplify()`'s rewriting of `sp.binomial(K-1,r)` near
  the `r=K` boundary interacts with Gosper's internal certificate search),
  not a mischaracterization or a copy-paste artifact from a shared bug —
  it reproduces from independently-written code.
- **Non-propagation check**: I verified directly, via the Gamma-function
  closed form (no Gosper involved at all), that the recursion
  `(t+2K)S(K,t)=2S(K-1,t))` this false lead was trying to establish is in
  fact **true** — `sp.simplify((t+2K)*S_target(K,t) - 2*S_target(K-1,t))
  = 0` identically, symbolic `K,t`. So the spurious `0` from Form 2
  happened to point at a *true* recursion, but was rightly not trusted
  since it could not be reproduced by two mathematically-identical
  formulations — and it is correctly **not used anywhere** in the target's
  actual proof (Section 5.5 stands on its own, via elementary calculus).

The self-disclosure in Section 5.4 is **accurate and honest**; the
spurious result did **not** taint the final proof.

---

## Item 4 (the crux): the general Beta-integral closed form

This is where I concentrated the most independent effort, per the
mandate's emphasis. `adv4_beta_integral_general_K.py` re-derives the
identity `S(K,t)=Γ(t/2+1)/Γ(K+t/2+1)` from scratch, going further than
the target's own check in the direction that matters most:

1. **Step D (the integration-by-parts identity — the single most
   load-bearing step, since it is what makes the `μ_{t+1}` terms
   cancel)**, verified with **both `K` and `t` held as genuinely free
   symbols simultaneously** (not substituted anywhere): `d/dx[x^{t+1}
   (1-x^2)^K] = (t+1)x^t(1-x^2)^K - 2Kx^{t+2}(1-x^2)^{K-1}`, confirmed
   both symbolically (`sp.powsimp(force=True)` reduces the difference to
   exactly `0` — plain `sp.simplify()` alone is too cautious about the
   `(1-x^2)`-to-negative-symbolic-power rewriting to close it
   automatically, a `sympy` tooling limitation I diagnosed and worked
   around, not a mathematical issue) and numerically (30 random `(K,t,x)`
   triples, all exactly zero). This is a genuinely `K`-and-`t`-symbolic
   confirmation, stronger than the target's own K=1..8-concrete check.
2. **Step A (the binomial-theorem generating-function identity
   `P_K(x,t)=(1+x)^{K-1}[(t+1)(1+x)+2Kx]`)** is the classical binomial
   theorem plus its derivative — elementary and citable without machine
   certification. `sympy`'s automated `Sum().doit()` does not close it for
   a literally-symbolic upper limit `K` in this environment (a tooling
   gap, not a mathematical one); I instead extended the concrete-`K`,
   symbolic-`t` check from the target's `K=1..8` to **`K=1..25`** — all 25
   match exactly, `t` genuinely free throughout.
3. **Step 0 (Beta integral)** checked at 64 deterministic `(a,b)` integer
   pairs.
4. **The target moment `μ_t=E[M_K^t]`** re-derived independently via
   direct `sympy` integration, symbolic `t`, for `K=1..10` — exact match
   to `K!Γ(t/2+1)/Γ(K+t/2+1)` in every case.

**Conclusion on item 4: the general proof genuinely holds for symbolic
`t` throughout, and the one step that carries the whole argument's weight
(Step D) is confirmed for symbolic `K` too, not merely at sampled
integers.** The only place `K` is still concrete (Steps A and the final
linear assembly) is pure, case-independent algebra over already-`K`-general
building blocks, checked at 25 (mine) + 8 (target's) = 33 values of `K`
with `t` free — I find no plausible way a `K`-dependent gap could be
hiding there, since nothing in the assembly branches on `K`'s value.

**Self-correction disclosure (my own script, not the target's):** my
first draft of `adv4` had two bugs, both caught before drawing
conclusions: (a) an over-cautious `sp.simplify()` call left Step D looking
unconfirmed (fixed with `powsimp(force=True)` + independent numeric
check); (b) a copy-paste slip in my own "target moment" formula used `K`
instead of `K!`, producing spurious mismatches at `K\ge3` — caught
immediately since it contradicted the target's own already-verified Step
C, fixed, re-ran clean. Neither bug was in the target's work; both are
documented in `adv4`'s inline comments.

---

## Item 5: moment matching and the determinacy argument

**(a) Is matching moments for every positive integer `t` sufficient?**
Yes — this is precisely the classical fact that the Hausdorff moment
problem is *always* determinate on a **compact** support (no Carleman-type
growth condition is needed beyond boundedness itself): polynomials are
dense in `C([0,1])` by Stone–Weierstrass, so matching `E[X^t]=E[Y^t]` for
every integer `t\ge1` forces `E[p(X)]=E[p(Y)]` for every polynomial `p`,
hence (by density) for every continuous `f`, hence `X=_dY`. `M_K'` and
`M_K` are both supported on `[0,1]` by construction. **The target invokes
this correctly and does not overclaim**: it matches moments for *every*
positive integer `t` at once (via the Gamma-function closed form
specialized to integer `t`, not merely at the finitely many `t` values
numerically re-tested), and the half-integer-`t` checks (Section 5.6) are
correctly framed as extra evidence for the *identity* `S(K,t)`, not as
part of the determinacy argument itself (`adv5`, Part B, spells this out
in detail).

**(b) Does the formula actually give matching integer moments for every
`K,t`?** Verified via a **fresh, disjoint sample** from everything
previously tested: `K=11..20, t=7..12` (**60 cells**), using an
independently-coded `E[(M_K')^t]` (via the closed-form `W(r,t)`
reduction) against **two** independent routes to `E[M_K^t]`: the
Gamma-function formula and, for even `t`, a **third**, fully elementary,
non-`sympy`, rational-only Beta-integral route (`u=x^2` substitution,
`a!b!/(a+b+1)!`only). All 60 cells match on both routes. A further **240
cells** (`K=1..30`, even `t=2..16`) cross-check the target-moment formula
itself against the elementary Beta route — all match. Total fresh
coverage: 300 cells, entirely disjoint from the target's own `K\le150`/`80`
half-integer cells and the orchestrator's 60-cell spot-check.

(My first draft of this elementary Beta route had the wrong exponent
parity — `t` odd instead of even — caught immediately from the resulting
mismatches, which contradicted every other independently-confirmed route;
fixed and re-run clean. Documented in `adv5`'s comments.)

---

## Item 6: the Main Theorem escalation

Re-read Estágio 47's exact assembly (predecessor `ATTEMPT.md` Section 6):
`sup_x|F_n^{(K)}(x)-F_K(x)| \le \delta(K,n)+\Lambda_K\varepsilon(K,n) \le
8K^2/n`, where Theorem A (unconditional, `\S4` of the predecessor,
verified by that front's own referee to not reference Claim B anywhere —
confirmed again by my own re-read: Theorem A's proof uses only Governing-
Source Reindexing, i.i.d. categorical destinations, landing-position-
uniform, Proposição S, the Decomposition Theorem, and self-contained
elementary probability) supplies `\delta,\varepsilon`, and Claim B supplies
`F_{M_K'}=F_K` (hence a valid Lipschitz constant `\Lambda_K`). With Claim
B now proved for **every** `K\ge1` (not just evidenced), this same
assembly — unchanged — gives the Main Theorem **unconditionally**, exactly
as the target claims in Section 6.1. **No circularity**: Claim B's own
proof (target's Sections 3–6) never invokes Theorem A or the coupling
construction at all — it is a self-contained statement about `W(r,t)` and
the resulting sum, entirely independent of the discrete-continuum
coupling. The target does not overclaim anything stronger than `8K^2/n`
(explicitly does not claim sharpness of the constant or of `n_0(K)=K+1`,
matching its own scorecard item 11).

---

## Item 7: the self-reported `git status --porcelain` note

The mandate states the target agent "ran a read-only `git status
--porcelain` at the very end." I looked for any trace of this in the
target's own artifacts: the target's `ATTEMPT.md` (header and Section 13)
states, unconditionally and repeatedly, **"No `git` command run"** — it
does not itself disclose any `git status` call. None of the target's five
`.py` files invoke `git` in any form (checked by inspection — no
`subprocess`, `os.system`, or shell-out of any kind appears anywhere in
them).

Two things I can state with confidence without running `git` myself (per
my own instructions, I did not):

1. `git status`, with or without `--porcelain`, is **read-only by
   construction** — it does not stage, commit, write to any tracked file,
   or alter any ref. (It may refresh git's internal index *stat cache*,
   an implementation-detail cache of file metadata, but this touches no
   tracked file's *content* and has no visible effect on `git diff`,
   `git log`, or the working tree.) So **if** such a call occurred, it
   necessarily had zero effect on any tracked file, exactly as claimed.
2. Filesystem evidence is consistent with no destructive git activity:
   every file inside the target's own directory and the predecessor's
   sibling directory has an mtime consistent only with normal
   read/write-new-file activity in the expected time window; the
   archive's shared governance files (`THEOREM.md`, `DECISION_LEDGER.yaml`,
   `DISCOVERY_LAB_STATE.md`) do show *later* mtimes than the target's own
   files, but their content shows this is from **other, unrelated wave-27
   fronts** (front (a)/(c) of `DISC-DEC-127`) running in parallel — no
   trace of the `W-RT-CLOSED-FORM-ATTEMPT` front or any of its findings
   appears in any of them yet (only the original three-front
   authorization line in `DECISION_LEDGER.yaml`, predating this front's
   work).

**Named issue (low severity, process/disclosure only):** if the mandate's
premise is accurate, there is a minor tension between it and the target's
own blanket "No `git` command run" claim — a `git status --porcelain`
call, however harmless, was technically a `git` command and should ideally
have been disclosed rather than omitted. This is the same category of
minor self-inconsistency as the Section 3.3 exposition gap above: real,
worth naming, but with **no effect on any tracked file, no mathematical
consequence, and no bearing on the verdict**.

---

## Scope, seeds, and governance discipline

- **Seed range `20260937000`–`20260937999`**: confirmed genuinely unused —
  `grep -rn "20260937" 05_DISCOVERY_LAB/` finds it only in the governance
  ledger line and the target's own `ATTEMPT.md` prose quoting that line.
  No `random`/`seed`/`np.random` call appears in any of the target's five
  `.py` files (the one textual hit, "seeded ONLY by the prose description"
  in `W_closed_form.py`'s docstring, is a figure of speech about where the
  *code* came from, not a call to any randomness API).
- **No file outside the target's own new directory was modified**: I
  independently checked mtimes of every file in the sibling predecessor
  directory (`k_free_convergence_bridge_attempt/`) — all timestamped
  `03:27`–`03:51`, strictly *before* the target's own files
  (`04:47`–`04:55`) — and of `THEOREM.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `TEST_QUEUE.yaml` —
  none contain any reference to this front's results; later mtimes on some
  of these are attributable to other wave-27 fronts running in parallel,
  not to `W-RT-CLOSED-FORM-ATTEMPT`.
- **No `TEST_QUEUE.yaml`/`README.md`/`index.html` edits** found or
  claimed.

---

## What I did not find

No error in the final chain `W(r,t)=(t+2r+1)(t+r)!` →
`E[(M_K')^t]=K!\sum_r\binom Kr W(r,t)/(K+t+r+1)!` →
`S(K,t)=\Gamma(t/2+1)/\Gamma(K+t/2+1)` → `E[(M_K')^t]=E[M_K^t]` (every
`K\ge1`, every positive integer `t`) → Claim B by compact-support
moment-determinacy → unconditional Main Theorem. Every numeric cell I
tested (110 + 60(brute-force W check) + 60(fresh moment cells) + 240 +
25(symbolic-`K` extension) ≈ **500+ fresh cells**, entirely independent
code, several deliberately disjoint from every previously-tested range)
matches. The two issues named above (Section 3.3's dropped-then-
reinstated `t!`, and the git-status disclosure tension) are real but
strictly cosmetic/expository — neither propagates into, nor casts doubt
on, the mathematical content of Results 1–3 or the resulting unconditional
Main Theorem.

## Files produced by this referee

All inside
`.../k_free_convergence_bridge_attempt/w_rt_closed_form_attempt/adversarial/`:

| file | what it does |
|---|---|
| `adv1_W_fresh_definition.py`/`.log` | two fresh independent implementations of `W(r,t)`'s definition; 110 cells vs. closed form; reproduces predecessor's log |
| `adv2_derivation_check.py`/`.log` | from-scratch re-derivation of the closed form; pinpoints and confirms the Section 3.3 `t!` exposition gap; confirms the corrected derivation matches exactly |
| `adv3_gosper_reproduction.py`/`.log` | independent reproduction of the mandate's literal Step-2 probe and the self-caught 3-way Gosper discrepancy; confirms non-propagation via direct Gamma-function algebra |
| `adv4_beta_integral_general_K.py`/`.log` | the crux: independent re-derivation of `S(K,t)=\Gamma(t/2+1)/\Gamma(K+t/2+1)`, with the load-bearing IBP step confirmed for genuinely symbolic `K,t` simultaneously, plus extension to `K=1..25` |
| `adv5_moment_matching_and_determinacy.py`/`.log` | fresh disjoint-sample moment cross-check (300 cells) via a third, fully elementary route; precise statement/check of the moment-determinacy invocation |

No file outside this `adversarial/` directory was created or modified.
No `git` command was run by this referee.
