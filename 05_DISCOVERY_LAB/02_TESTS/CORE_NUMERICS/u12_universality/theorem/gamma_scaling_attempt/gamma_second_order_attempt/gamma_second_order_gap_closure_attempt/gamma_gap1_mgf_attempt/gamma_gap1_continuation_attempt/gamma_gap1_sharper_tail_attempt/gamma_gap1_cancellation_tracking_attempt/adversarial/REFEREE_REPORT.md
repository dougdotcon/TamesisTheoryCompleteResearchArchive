# REFEREE REPORT — `GAMMA-GAP1-CANCELLATION-TRACKING-ATTEMPT`

**Target:** `.../gamma_gap1_sharper_tail_attempt/gamma_gap1_cancellation_tracking_attempt/ATTEMPT.md`
(Wave 27, front (c), authorized by `DISC-DEC-127`)

**Referee:** hostile, independent adversarial session, dispatched per the
orchestrating session's mandate. Read `THEOREM.md`'s γ-scaling law section
(Estágios 30, 33, 36, 37) and all three immediate-ancestor `ATTEMPT.md`
files in full, in prose, **before** opening any script belonging to the
target front. All core mathematical claims (items 1–9 of the mandate) were
independently re-derived from the raw definitions, from scratch, using
fresh `sympy`/`mpmath`/`scipy` code, before the target's own scripts were
consulted at all. The target's own scripts were read only afterward, for
the narrow governance checks (seed usage, file-scope discipline) that
necessarily require inspecting them.

---

## VERDICT: **SOUND WITH NAMED ISSUES — ACCEPT for catalogue**

Every load-bearing mathematical claim in this front — the cubic
coefficients, the asymmetric-support observation, the exact `λ_tight(γ)`
limits (including the interior-critical-point analysis), the
`λ_tight(γ)<λ(γ)` comparison and its diagnosis, the Bernstein combination
and the exact "14× smaller, uniformly in `a`" flagship result, the
`K_real` tightening, the `n₀(γ)` table, and the self-caught bug — was
independently reproduced, in every case exactly (zero symbolic
difference, or numeric agreement to the reported precision). The one
named issue below is a genuine, moderate-severity **presentational/
arithmetic error in how the flagship improvement range is summarized** in
three prominent places (the up-front VERDICT, §5, and the §11 Scorecard),
which conflates the "vs. Bernstein" and "vs. Hoeffding" comparison
columns of the front's own §9 table. It does **not** affect any proved
result, the `n₀(γ)` table itself (independently verified correct), or the
non-closure conclusion — but it does misstate the size of the headline
"vs. sharper_tail" gain in the places a reader is most likely to see
first, and it appears to have propagated into the orchestrating task's
own framing (see Finding 1). No mathematical, logical, or attribution
error was found anywhere else.

---

## Independent verification, item by item

### 1. The exact cubic coefficients `c₀,c₁,c₂,c₃`

Re-derived `τ(m):=Σ_{i=1}^m((k-i)/n)²` via `sympy.summation` from scratch,
substituted `M=γk+D`, expanded `x(D):=δ(D)+τ(M)/2` (with the cited exact
`δ(D)=D(2k(1-γ)-D-1)/(2n)`), and extracted the quartet of coefficients via
`sympy.Poly`. **Exact zero symbolic difference** against all four
coefficients as transcribed in the target's §2 (both the "derivative-based"
closed form and its listed algebraic-bracket form). Numeric spot check at
`γ=1/2,k=10,n=100` reproduces `c₀=51/4000` exactly.
(`adversarial/adv01_cubic_rederivation.py/.log`)

### 2. The asymmetric support of `D`

Trivially confirmed: `M∼Bin(k,γ)` satisfies `M∈[0,k]` exactly by
definition, hence `D=M-γk∈[-γk,(1-γ)k]` exactly. Grepped all three
ancestor `ATTEMPT.md` files for any acknowledgment of this asymmetry: the
grandparent (`gamma_gap1_mgf_attempt`) does cite `M∈[0,k]` but only to
derive the **crude, symmetric** conclusion `|D|≤k≤K` ("Tail. `|D|\le
k\le K` always (`M\in[0,k]`)"); neither the continuation nor the
sharper_tail front mentions the asymmetric interval at all. The target's
claim that this is a genuinely new observation, not used by any ancestor,
is **confirmed**.

### 3. `λ_tight(γ)`: the two support-endpoint limits

Independently built `x_K(D)` from the coefficients above with `k=K`,
`K:=√((4/β)n\ln n)`, and attempted `sympy.limit()` at the two support
endpoints. As the task anticipated, the naive call **fails** exactly on
the documented sympy Gruntz-algorithm sign-ambiguity limitation
(`Result depends on the sign of sign((gamma - 1)**2)` at `D_max`;
`sign(-4*gamma**2+12*gamma-8)` at `D_min`). Rather than falling back to
numerics only, I found that applying `.factor()` to the pre-limit
expression before calling `sp.limit()` resolves the ambiguity completely,
yielding a **full symbolic proof for generic positive `γ`** (no upper
bound `γ<1` even required):

```
lim_{n→∞} x_K((1-γ)K)/ln(n) = 4(1-γ)²/(γ(2-γ))      [exact, symbolic]
lim_{n→∞} x_K(-γK)/ln(n)    = -4                      [exact, symbolic, γ-independent]
```

Both match the target's claims with **exact zero symbolic difference**.
This is independently cross-checked at extreme precision (mpmath dps=80,
using the *true integer ceiling* `K:=⌈√((4/β)n\ln n)⌉`, not the idealized
real-valued surrogate) at `n` up to `10²⁰⁰`, across 5 `γ` values
(`0.01,0.1,0.5,0.9,0.99`): agreement to within `10⁻²¹`–`10⁻⁸¹` absolute
difference at every point. (`adversarial/adv02_lambda_tight_limits.py/.log`,
`adv03_numeric_crosscheck.py/.log`)

**Interior critical point.** Solved `x_K'(D)=c₁+2c₂D+3c₃D²=0` exactly via
`sympy.solve` (quadratic formula), with `k` replaced by a symbolic `K`.
One root matches the target's claimed closed form
`D*=-Kγ+K+n-√(36n²+3)/6-1/2` with **exact zero difference**; direct
substitution confirms `x_K'(D*)=0` exactly (an independent check, not
relying on `solve`'s own correctness). The other root is
`D*+√(36n²+3)/3`, confirmed `O(n)` (dominated by `2n`, since
`K=o(n)`) — the "asymptotically irrelevant" root. The series expansion
`√(36n²+3)/6 = n+1/(24n)+O(n⁻³)` is confirmed exactly, giving
`D*-D_max = -1/2-1/(24n)+O(n⁻²)`, i.e. exactly `-1/2+O(1/n)` as claimed.
(`adversarial/adv04_critical_points.py/.log`)

### 4. `λ_tight(γ)` vs. `λ(γ)`, and why `λ(γ)` is loose

Proved `λ_tight(γ)<λ(γ)` for **every** `γ∈(0,1)` by full symbolic algebra
(not sampling): on `[γ*,1)`, `λ(γ)-4 = 4(1-γ)(3-γ)/(-γ(γ-2))`, manifestly
positive there (both bracketed factors positive, denominator negative);
on `(0,γ*)`, `λ(γ)-λ_tight(γ) = 4(2-γ²)/(γ(2-γ))`, manifestly positive on
`(0,1)`. Ratio checks: `γ=1/2`: `λ/λ_tight=2.6667` (target: `2.67×`);
`γ=0.01`: `λ/λ_tight=3.0405` (target: `3.04×`) — **exact match**.

I then independently re-derived **why** `λ(γ)` is loose: computed the
leading order of `|c₁(K)|K+|c₂(K)|K²` (confirming, via random sign probes
across 30 `γ∈(0,1)`, that `c₁(K)>0` and `c₂(K)<0` throughout, so
`|c₂(K)|=-c₂(K)`), and found `lim_{n→∞}(|c₁(K)|K+|c₂(K)|K²)/\ln n` equals
`4(3-2γ)/(γ(2-γ))` with **exact zero symbolic difference** from Estágio
36's own `λ(γ)`. This independently confirms the target's diagnosis:
`λ(γ)` is exactly the triangle-inequality-summed bound at the *symmetric*
point `D=K`, not the exact signed evaluation at the true endpoints — the
predecessors' own "true leading constant" still carried the same class of
slack this front removes. (`adversarial/adv05_lambda_comparison.py/.log`)

### 5. Combination with Bernstein: the 14× flagship result

Re-derived Estágio 37's own `C0_Bernstein(γ,a)²` structure from its
prose-cited `σ²(γ)=γ(1-γ)`, `λ̂(γ):=16(7/4-γ)/β(γ)` — matches
`sup_{γ→0+}=28a+56` exactly. Combining with `λ_tight(γ)` in place of
`λ̂(γ)`:

- On `[γ*,1)`: `C0_tight²=9/2·(2+a)γ(1-γ)`, vertex at `γ=1/2`, value
  `9a/8+9/4` — matches exactly.
- On `(0,γ*)`: `lim_{γ→0+}C0_tight²=2a+4` — matches exactly, exact
  `sympy.limit`.
- `sup=max(9a/8+9/4,2a+4)=2a+4` for every `a>0` (since
  `(2a+4)-(9a/8+9/4)=7a/8+7/4>0` for all `a>-2`) — confirmed.
- **`28a+56=14·(2a+4)` is an exact algebraic identity for every `a`**
  (not just a numeric check at `a=0.05`) — confirmed via
  `sympy.simplify((28a+56)-14(2a+4))=0`.

All confirmed with **exact zero symbolic difference**.
(`adversarial/adv06_bernstein_combination.py/.log`)

### 6. The disclosed non-fully-symbolic piece (monotonicity on `(0,γ*)`)

This was the item flagged for the most scrutiny. The target confirms
monotone decrease of `C0_tight_Bernstein(γ,a)²` on `(0,γ*)` only by dense
sign-sampling (400 points × 5 values of `a`), disclosing honestly that
`sympy` could not simplify the derivative's real root outside `(0,γ*)`
to closed form.

**Key structural fact the target did not exploit, which I found and
verified:** `C0_tight_Bernstein(γ,a)² = (2+a)·h(γ)` where
`h(γ):=σ²(γ)(λ_tight(γ)+1/2)` **does not depend on `a` at all**. Since
`2+a>0` for every `a>0`, the *sign* of the `γ`-derivative — hence
monotonicity — is governed entirely by `h'(γ)`, identically across all
`a>0` simultaneously. This means the target's own "sample 5 values of
`a`" check was testing something that is mathematically guaranteed not
to vary with `a` — not a flaw, but an opportunity for a stronger, simpler
proof.

I computed `h'(γ)`'s numerator explicitly: a **cubic** polynomial,
`14γ³-63γ²+84γ-36`. Using `sympy.real_roots` (Sturm-sequence-based exact
root isolation, which does **not** require expressing roots in closed
radical form), this cubic has **exactly one real root**, `≈2.5305`,
**strictly outside** `(0,γ*)≈(0,0.2929)` (indeed outside `(0,1)`
entirely) — confirming the "root sympy could not simplify" the target
refers to is real but irrelevant to the interval in question. Combined
with the sign at one interior sample point (`h'(0.1)<0`) and continuity
on the root-free interval, **this constitutes a full, rigorous, exact
closed-form proof of strict monotonicity on `(0,γ*)`, for every `a>0`
simultaneously** — an upgrade from the target's own dense-sampling
disclosure to a genuine symbolic proof, achievable with the tools already
in front of them.

As additional, independent belt-and-suspenders confidence (per the task's
own suggestion), I ran: (i) a 2,000,000-point dense grid scan of `h(γ)`
on `(0,γ*)` — **zero** locally-increasing steps found; (ii) a
`scipy.optimize.minimize_scalar` search from 50 restart seeds for any
interior local maximum of `h` — the found maximum sits at the `γ→0`
boundary (`h≈2`, matching the exact limit `2` from item 5's `2a+4=(2+a)·2`
factorization), not in the interior. **No counterexample exists; the
disclosed limitation was honest, appropriately flagged, and posed no real
risk to the flagship result** — if anything, it was more conservative
than necessary. (`adversarial/adv07_monotonicity_deepdive.py/.log`)

### 7–9. `K_real`, `k`-uniformity, and the `n₀(γ)` table

Built a **complete, independent, from-scratch re-implementation** of the
full `W_tight(n,γ,C,a)` assembly (bulk + Bernstein-tail + small-`k`
residual, `K_real`, exact-cubic-max helper, log-domain bisection),
constructed purely from the formulas quoted in the target's own §1–§9
prose — not from its scripts.

- **`K_real` validity**: confirmed `K_real=√(4n\ln n/β)+1 ≥` the true
  integer ceiling `K` at every tested `(γ,n)` (5 `γ`, `n` up to `10⁶⁰`);
  `K_max/K_real→2.0000` exactly, as claimed.
- **`k`-uniformity**: 60 spot checks (5 `γ`, 2 `n`-scales up to `10³⁰`, 6
  `k`-fractions from `0.001K` to `0.999K`) — **zero violations** of
  `H_k≤H_{K_real}`.
- **`n₀(γ)` recomputation**: bisected `n₀(γ)` independently at **5** of
  the 8 sample points (`γ=0.99,0.9,0.5,0.1,0.01`, more than the requested
  2–3), using the target's own reported `C(γ)` values. **My independently
  bisected `log₁₀n₀` matched the target's published table to within
  `0.001`–`0.009` decades at every point** — e.g. `γ=0.5`: mine `35.492`
  vs. target's `35.49`; `γ=0.01`: mine `61.173` vs. target's `61.17`. The
  underlying `C0_tight²` values (hence `C(γ)`) also matched, confirming
  the reported "best margin" values (`1.010`–`1.050`) are consistent.
  (`adversarial/adv08_full_assembly.py/.log`)
- **Independent brute-force grid-scan cross-check** of the exact-cubic-max
  method itself (mirroring, but built independently of, the target's own
  §3/script 08 check): 15 `(γ,n)` triples, 20,000-point grids, **zero
  mismatches** (grid value never exceeds the closed-form value); worst
  relative gap `6.088×10⁻¹⁰` — matching the target's own reported
  `~6×10⁻¹⁰` almost exactly. (`adversarial/adv10_bruteforce_gridscan.py/.log`)

### 8 (continued). The self-caught bug (§8)

Directly reproduced both the buggy and fixed versions of the small-`k`
residual term in my own independent assembly. Using `H_K` (astronomically
large, `k=K`-scale) instead of `H_{k₂}` (the true, much smaller
`k=O(\ln n)`-scale) in the residual, at the target's own working point
(`γ=0.5,C=1.595,a=0.05`), produces `log W` that **grows monotonically**
from `115.0` at `n=10¹⁰` to `675.4` at `n=10⁷⁰` — never crossing zero,
exactly matching the target's own description of the caught bug ("showed
`log W` growing, not shrinking, with `n`, up to `n=10⁴⁴` with no sign of a
crossing"). The fixed version (`H_{k₂}` at its own natural scale) decays
cleanly, crossing zero near the reported `n₀`. This **directly and
independently confirms the bug's diagnosis and the fix are both
accurate**. A no-spurious-oscillation scan (22 decades, my own assembly)
at `γ=0.5` and `γ=0.01` found **zero** local increases beyond `n₀`, in
agreement with the target's own claim.
(`adversarial/adv09_bug_and_oscillation.py/.log`)

### Honest non-closure framing

Read the document in full for overclaiming. Every prose section, the
executive VERDICT, §10, and the §11 Scorecard consistently and
repeatedly state Gap 1 is **not closed**, `C(γ)` for `γ∈(0,1)` remains
**fully OPEN**, and `n₀(γ)` (`10¹⁵·⁴`–`10⁶¹·²`) is explicitly described as
"astronomically large... vastly beyond any numerically reachable `n`...
this front does not claim a numerically useful bound." This framing is
accurate and consistent throughout; no instance of overclaiming was
found.

### Scope, seed, and governance discipline

- **Seed range** `20260938000–20260938999`: `grep -rn "20260938"
  05_DISCOVERY_LAB/` (run independently by this referee) finds only the
  ledger's own reservation line — confirmed **unused**, matching the
  front's own before/after disclosure.
- **`random`/`seed` usage**: `grep -rn "random\.\|seed("` across the
  target's 8 scripts finds exactly one use, `random.seed(1)` in script
  `01`, for a disclosed 40-point deterministic sanity spot-check — matches
  the front's own characterization exactly (not a draw from the reserved
  block).
- **File-scope discipline**: `git status --porcelain` shows the target's
  own new directory as the only relevant untracked addition; `grep` for
  any modified (non-`??`) entries across the whole repository returns
  **empty** — confirming no existing tracked file (`THEOREM.md`,
  `PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`,
  `DISCOVERY_LAB_STATE.md`, or any ancestor/sibling `ATTEMPT.md`) was
  modified.
- **No git commands** were run by the target front (consistent with the
  absence of any staged/committed changes); this referee's own git
  commands were read-only (`status` only).
- The target's own directory listing (`01`–`08` `.py`/`.log` pairs plus
  `ATTEMPT.md`, no pre-existing `adversarial/`) exactly matches its §11
  Files table.

---

## Findings

### Finding 1 (MODERATE severity) — Headline "decades saved vs. Bernstein" figure is misstated in three places

The front's own §9 table (line-for-line) gives, for the "decades saved
vs. Bernstein" column: `2.30, 14.55, 14.12, 14.86, 16.21, 15.34, 15.00,
14.62` (at `γ=0.99,0.9,0.7,0.5,0.3,0.1,0.05,0.01` respectively) —
independently recomputed from the same table's own `log₁₀n₀` and "OLD
Bernstein" columns and confirmed correct by direct subtraction at every
row. The correct range for this specific comparison is therefore **`2.30`
to `16.21` decades**, with the maximum at **`γ=0.3`** (not `γ=0.01`) —
and this is exactly what §9's own prose paragraph immediately following
the table states correctly ("`10²·³×` up to `10¹⁶·²×`... relative to the
sharper_tail front's own... Bernstein table").

However, **three other places in the same document misstate this range**:

1. **The up-front VERDICT** (the section a reader sees first) states:
   *"ranging from 2.30 decades (γ=0.99...) up to 23.71 decades (a factor
   of `~10²³·⁷`) at `γ=0.01`, compared against the sharper_tail front's
   own best (Bernstein-only) table."* The figure `23.71` is actually the
   `γ=0.01` value of the **Hoeffding** comparison column (correctly used
   in the very next clause, "against the original Hoeffding-based
   (continuation) table the range is 5.37 to 23.71 decades") — it has
   been duplicated into the Bernstein-comparison sentence in error.
2. **§5** ("Why the improvement is not uniform"), discussing the
   mechanism, states: *"this is why γ=0.99 shows the smallest gain (2.30
   decades) and γ=0.01 the largest (23.71 decades)"* — same conflation,
   in a sentence that is specifically about the `λ̂/λ_tight` (i.e.
   Bernstein-route) mechanism.
3. **The §11 Scorecard** states: *"Net improvement: `2.30`–`14.86` decades
   vs. sharper_tail's Bernstein table..."* — here the *maximum* is
   understated (`14.86` is the `γ=0.5` value; the table's actual maximum
   for this column is `16.21` at `γ=0.3`, and three other points —
   `γ=0.3,0.1,0.05` — all exceed `14.86` too).

So the same "vs. Bernstein" range is reported **three different, mutually
inconsistent ways** across one document: `2.30`–`23.71` (VERDICT, §5),
`2.30`–`14.86` (Scorecard), and the correct `2.30`–`16.21` (§9 prose,
matching the table). This is a real, reproducible arithmetic/transcription
error, not a matter of interpretation — verified independently in
`adversarial` by direct subtraction of the table's own published columns
(no re-derivation of `n₀` needed to catch it, only arithmetic on numbers
already in the document). It does **not** affect the underlying `n₀(γ)`
table (independently re-verified correct in item 9 above), the flagship
`14×`/`sup=2a+4` result (independently verified exact), or the paper's
non-closure conclusion. It **does** matter because it inflates the
headline "vs. Bernstein" improvement claim by roughly `7.5` decades (a
spurious extra factor of `~10^7.5`) in the two most prominent summary
locations, and — notably — **the orchestrating session's own task prompt
for this review repeats the erroneous `2.30`–`14.86` figure** (from the
Scorecard) verbatim, showing the error had already begun to propagate
before this referee's check. **Recommendation:** a future pass should
correct the VERDICT and §5 sentences to read "`2.30` to `16.21` decades
(`γ=0.3`) vs. Bernstein; `5.37` to `23.71` decades (`γ=0.01`) vs.
Hoeffding" and correct the Scorecard's "`2.30`–`14.86`" to "`2.30`–
`16.21`". Per this referee's mandate, this document is **not** modified
here — the finding is recorded for the orchestrating session or a future
front to act on.

No other findings. No mathematical, logical, citation, or attribution
error was found in any of the nine core claims, the self-caught-bug
disclosure, the honesty of the non-closure framing, or the governance/
scope discipline.

---

## Summary assessment

This is a genuinely substantial result on a line that had been dormant
for five waves. The central new idea — that `D`'s true, asymmetric
support (`M∈[0,k]` forces `D∈[-γk,(1-γ)k]`, not the symmetric `|D|≤k`
every ancestor used) lets the Bulk/Tail Lemma's coefficient bound be
computed *exactly* (endpoint-or-critical-point of a cubic) rather than
triangle-inequality-summed — is correct, is a real advance over even
Estágio 36's own "true leading constant" `λ(γ)` (itself shown, both by
the target and independently confirmed here, to still carry the same
class of slack), and produces an exact, clean closed form
(`λ_tight(γ)=max(4,4(1-γ)²/(γ(2-γ)))`) with a strikingly simple
`M→0`-side universal constant (`=4` for every `γ`). Combined with
Estágio 37's Bernstein-with-slack technique, the resulting `14×`-smaller
(uniformly in `a`) supremum is an exact algebraic identity, not a
numerical coincidence at one sample `a`. The one disclosed non-fully-
symbolic piece (monotonicity of `C0_tight_Bernstein²` on `(0,γ*)`) turned
out, on independent investigation, to admit a full closed-form proof via
an `a`-independence factorization the target did not notice — a genuine
opportunity for strengthening, not a weakness that was missed carelessly,
since the target's own dense-sampling check already correctly found no
counterexample. The self-caught bug (§8) is accurately described and
correctly fixed, independently reproduced here. The non-closure framing
is honest and consistent throughout. The one real issue (Finding 1) is a
headline-arithmetic slip that inflates a summary number in prominent
locations without touching any actual proof, computation, or the paper's
own honest bottom line.

**Verdict: SOUND WITH NAMED ISSUES — ACCEPT for catalogue.**
