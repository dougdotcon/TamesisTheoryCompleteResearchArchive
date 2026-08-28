# REFEREE REPORT — `MCLUST-H1-VOLTERRA-ATTEMPT`

**Target:** `h1_volterra_attempt/ATTEMPT.md` (Wave 23, front (c), `DISC-DEC-110`).
**Scope:** hostile adversarial review, per mandate. No `.py` file belonging to
this front or any ancestor front was opened, read, or imported at any point;
every check below was coded fresh from the equations quoted in the target's
own prose (Sec 0, Sec 3.1, Sec 4.1).

**VERDICT: NEEDS REVISION.**

Sec 2 (algebra), Sec 3 (Volterra-in-`y` structural reformulation), and Sec
5–6 (the new grid-based Neumann/Picard numerics) are sound and were
independently reproduced. The document's overall bottom line — `H1`,
`(U1)`, `(U2)` remain open, nothing closed — is **not** threatened by
anything found here. But Sec 4's headline result — explicitly named by the
dispatching mandate as "the heart of the claim" — does not survive
scrutiny: the claim that the closed kernel's boundedness "hinges entirely"
on the unbounded multiplication operator `M_y`, and that this "is the
actual content of the obstruction," rests on an unexamined
composition-vs-multiplicativity gap. Direct, independent computation (two
structurally different routes, agreeing to the precision shown) indicates
the actual composed operator the document points to is **uniformly
bounded, not growing in `y` at all** — the opposite of Sec 4.4's central
claim. This is a HIGH-severity finding against the document's own
headline framing of its Part C contribution, not against its overall
non-closure verdict.

---

## 0. Reading discipline (per the mandate)

Read in full before any check: the target `ATTEMPT.md`;
`PROOF_DEPENDENCY_MAP.md`'s complete `PLATRESUM` addendum history (wave 17
through wave 22, i.e. `plateau_resummation_attempt`,
`mclust_plateau_abstract_real_gap_attempt`, `mclust_h1_validity_attempt`,
`mclust_h2_validity_attempt`, `h1_energy_estimate_attempt`) and the
document's own §3 "Regra de uso deste mapa"; the full
`mclust_h1_validity_attempt/ATTEMPT.md` (establishes `(U1)`/`(U2)`
precisely, via the Watson Concentration Lemma); and the full
`h1_energy_estimate_attempt/ATTEMPT.md` (direct predecessor — establishes
`(E1)`, `(KEY)`, `(BB-Psi')`, the named "derivative-loss" obstruction, and
the Lipschitz-`<=1` finding). **No `.py` file from either predecessor, or
this front, was read** — the target's mandate explicitly required
re-deriving/re-coding everything from scratch, which this review followed.

The safety rule in `PROOF_DEPENDENCY_MAP.md` §3 (never cite Tree A as
evidence for Tree B or vice versa) was followed throughout this review;
nothing from the archive's separate `u1/2` line was consulted or cited.

Seed range `20260925000-20260925999` (reserved for this front, per
`DISC-DEC-110`) was grep-confirmed unused elsewhere before this review
began (`grep -rn "20260925" 05_DISCOVERY_LAB/` — appears only in this
front's own reservation line and the ledger/state summary of that same
reservation). **No randomness was needed for any check in this review** —
everything below is exact symbolic reasoning or deterministic
arbitrary-precision (`mpmath`) / deterministic grid (`numpy`) computation.

---

## 1. Findings confirmed sound (no issue)

### C1 — `(NEW-W)` algebra and upstream citation accuracy

`(E1)`, `(KEY)`, `(BB-Psi')` as quoted in the target's Sec 0 were checked
word-for-word against the original text of `h1_energy_estimate_attempt/
ATTEMPT.md` Sec 2.1 — **verbatim matches**, no transcription drift. The
substitution

```
W = Psi - eps*Psi_x = Psi - eps*[(x+y)Psi - I] = (1 - eps*(x+y))*Psi + eps*I
```

is correct, trivial algebra; re-derived by hand independently, no sign
error, no missed term.

### C2 — `(E2')` pulled-out-constant rearrangement (Sec 3.1)

Independently re-derived by direct substitution: since
`(x+v) + (y-v) = x+y` exactly for every `v`, the coefficient
`(1-eps(x+y))` in `(NEW-W)`, evaluated at the shifted point `(x+v,y-v)`,
is genuinely constant in `v` and pulls outside `(E2)`'s convolution
integral without approximation:

```
Phi(x,y) = e^{-y/eps} + (1/eps)*int_0^y e^{-v/eps} * [(1-eps(x+y))Psi(x+v,y-v) + eps*I(x+v,y-v)] dv
         = e^{-y/eps} + [(1-eps(x+y))/eps] * A(x,y) + B(x,y)
```

matches `(E2')` exactly, where `A,B` are as defined in the target. **Not
an approximation — an exact rearrangement**, as claimed.

### C3 — Classical Volterra quasi-nilpotency statement (Sec 3.4)

The statement and simplex-volume proof are the standard textbook fact,
correctly stated: `||K^n|| <= (MT)^n/n!` on a compact triangle
`0<=s<=t<=T` requires only that `M := sup||k(t,s)||` be finite (no
smallness of `M` or `T` needed — factorial beats any fixed exponential).
The document's own `0<=t<=y` convention (Sec 4.1) matches the classical
`s<=t<=T` convention exactly when applied in Sec 4.4 — no domain-labeling
mismatch.

### C4 — Individual bounds on `K_B` and `K_A^raw` (Sec 4.2, 4.3), taken in isolation

Both re-derived step by step from the stated definitions:

- `||K_B(h)|| = ||int_0^h e^{-v/eps} S_v dv|| <= int_0^h e^{-v/eps}*||S_v|| dv = eps(1-e^{-h/eps}) <= eps` — confirmed correct, for every `h>=0`, no domain restriction on `x` needed.
- `||T_w|| <= sup_x R(x+w) = R(w)` (attained at `x=0`, `R` decreasing) — confirmed correct; then `||K_A^raw(y,t)|| <= int_t^y e^{-(y-w)/eps} R(w) dw <= R(t)*eps <= eps*R(0) = eps*sqrt(pi/2)` — confirmed correct, each inequality step checked.

Both bounds are correct **as bounds on the standalone operators**. Their
consequence when *combined* with `M_y` in Sec 4.4 is a separate matter —
see Finding H1 below, which is where the actual problem lives.

The `R(z)` facts (`R(0)=sqrt(pi/2)`, monotone decreasing, `R(z)<=1/z`)
were independently re-confirmed via `mpmath` at `dps=50` (script `r01`),
matching the orchestrating session's own pre-dispatch spot-check.

### C5 — Sec 6 numerics: independently reproduced to 3–4 significant digits

See Section 4 below for the full table. A from-scratch grid Neumann/Picard
solver, built only from the equations in Sec 3–4's prose, reproduces the
Sec 6.2/6.3 successive-difference ratio tables at both `c=100` and
`c=1000` to 3–4 significant digits at every point checked. Strong evidence
this numerical content is genuine and correctly computed.

---

## 2. THE CENTRAL FINDING

### H1 (HIGH) — Sec 4.4's "obstruction isolated to `M_y`" claim does not hold up; direct computation indicates it is false

**What the document claims.** Sec 4.4: "The full kernel's boundedness
therefore hinges entirely on `||M_y||_op = sup_x |1/eps-x-y|`," which is
unbounded as `x->infinity`; restricted to a bounded `x`-strip `[0,L]`, the
document derives `||M_y||_{X_L} <= 1/eps+L+y`, and reads this as growing
linearly in `y` for *any* fixed `L`. Sec 10's scorecard then labels "Full
kernel `K(y,t)` bounded on the UNRESTRICTED `x` domain" as **REFUTED**,
and "That strip-restricted bound stays bounded as `y->infinity`" as
**REFUTED**, attributing both to `M_y`. The VERDICT UP FRONT (item 3) and
Sec 4.6 call this "the actual content of the obstruction," claimed to
independently reproduce, via a completely different method, the same
mechanism the predecessor front found via Lipschitz-contraction analysis.

**The gap.** Nowhere does the document actually bound the *composed*
operator `M_y ∘ K_A^raw(y,t)` — the object that actually appears in the
kernel `K(y,t) = M_y ∘ K_A^raw(y,t) + K_B(y-t)`. It only computes the norm
of `M_y` *in isolation* (as a standalone multiplication operator on `X` or
`X_L`). The inequality `||AB|| <= ||A||*||B||` is one-directional: when
`||A||` is unbounded, it says literally nothing about `||AB||`. Whether
that gap matters is an empirical/analytical question, not something that
can be waved away — so this review computed it directly.

**The exact cancellation the document's own algebra sets up but never
uses.** Sec 4.1's own derivation gives
`(S_{y-w} T_w f)(x) = int_0^inf e^{-u^2/2-u(x'+w)} f(x'+u) du` with
`x' = x+y-w`. Hence `x'+w = (x+y-w)+w = x+y` — **independent of `w`**.
Writing `z := x+y`, this gives the SHARPER, w-independent bound:

```
|(K_A^raw(y,t) f)(x)|  <=  eps * R(x+y) * ||f||_inf
```

(tighter than the document's own `eps*R(t)`, since `R(x+y)<=R(t)` with
equality only at `x=0`). Then:

```
|(M_y K_A^raw(y,t) f)(x)|  <=  |1-eps(x+y)| * R(x+y) * ||f||_inf  =:  h_eps(x+y) * ||f||_inf
```

**Direct computation** (`mpmath`, `dps` 30–50, script `r01`) shows
`h_eps(z) := |1-eps*z|*R(z)` is **globally bounded by `sqrt(pi/2) ~
1.2533`** — attained at `z=0`, an **eps-independent bound** — decaying to
`0` at `z=1/eps`, then rising back but asymptoting to `eps` (not to
infinity) as `z->infinity`. Because `x>=0` forces `z=x+y>=y`, the operator
norm restricted to the physical domain `x>=0` is `sup_{z>=y} h_eps(z)`,
which is **non-increasing in `y`** past a threshold, not growing (script
`r02`):

| `c` | `eps` | `y` | `sup_x \|M_y K_A^raw(y,0)[1](x)\|` |
|---|---|---|---|
| 100 | 0.1 | 5 | 0.0964 |
| 100 | 0.1 | 20 | 0.0900 |
| 100 | 0.1 | 100 | 0.0944 |
| 100 | 0.1 | 1000 | 0.0991 |
| 1000 | 0.0316 | 10 | 0.0677 |
| 1000 | 0.0316 | 100 | 0.0283 |
| 1000 | 0.0316 | 1000 | 0.0308 |

No growth in `y` at all — the values saturate near a small constant
(consistent with the `h_eps(z)->eps` asymptote). This was cross-checked
**two structurally independent ways**: the closed-form route above
(`r01`, `r02`), and a fully independent **raw double numerical
quadrature** of the literal double-integral definition of `K_A^raw`,
which never invokes the `R(z)` closed form at all (`r03`) — the two agree
to the precision shown (a sign difference only, from `M_y(x)` changing
sign at `x=1/eps-y`, expected and harmless since the operator-norm claim
uses `|.|`).

**What this does and doesn't mean.** The full kernel
`K(y,t) = M_y∘K_A^raw(y,t) + K_B(y-t)` is, per this computation, bounded
by roughly `sqrt(pi/2)+eps` **uniformly in `x,y,t`** — including on the
FULL unrestricted `x`-domain the document claims fails. This directly
contradicts the Sec 10 rows "full kernel bounded on unrestricted domain:
REFUTED" and "strip-restricted bound stays bounded as `y->infinity`:
REFUTED." It does **not**, however, establish `(U1)`/`(U2)` or close
`H1` — boundedness of one kernel piece's operator norm is a much weaker
statement than the uniform-in-`x`, `y->infinity` convergence `(U1)`/`(U2)`
actually require (that needs control of the Neumann series' behavior as
`y->infinity`, not just a bound on `K(y,t)` at each finite `y,t`). The
document's overall "`H1` remains open" verdict is not threatened by this
finding. What IS threatened is the specific claim that Sec 4 "isolates
the exact obstruction to a single operator" and that this "is the actual
content of the obstruction" — that mechanism, as diagnosed, does not
appear to exist.

**A constructive side-effect.** This also answers a question the document
itself leaves open. Sec 11 item 2 calls the gap between the crude Sec 4
bound and the much better-behaved Sec 6 numerics "itself unexplained,"
speculating about unexploited sign/cancellation structure in the iterated
kernel. The explanation is simpler and specific: the Sec 4 bound is not
tight because `||AB||<=||A||*||B||` was applied with `||A||=infinity`,
discarding exactly the `x'+w=x+y` cancellation the document's own Sec 4.1
algebra produces one line earlier but never exploits when bounding.

**Severity: HIGH.** Per this archive's convention ("the headline claim is
wrong, unproved, or overclaimed") and per the dispatching mandate's own
framing of Sec 4 as "the heart of the claim," this is scored HIGH. It does
not collapse the document's overall non-closure verdict, but it does
invalidate the specific new analytic content claimed as Part C's headline
contribution.

### H2 (HIGH, downstream of H1) — Sec 4.6's "two independent routes converge on the identical obstruction" overclaims

Sec 4.6 and the VERDICT UP FRONT (item 3) present the predecessor's
Lipschitz-`<=1` finding and this front's `M_y` finding as two
structurally different methods "independently arriv[ing] at the identical
underlying mechanism," explicitly calling this convergence itself a
meaningful finding — evidence the obstruction is a genuine feature of the
system, not an artifact of one technique. Since Finding H1 shows this
front's own route does not actually establish an obstruction (the
composed operator it points to is, per direct computation, bounded), there
is no second, independent confirmation here — the predecessor's
Lipschitz-`<=1` result (itself already reviewed by a prior referee and
found essentially sound, modulo the already-corrected N3 note) stands
alone, not doubly confirmed by an independent method as claimed.

---

## 3. Secondary findings

### M1 (LOW) — "`S_v` is an isometry" is imprecise terminology

Sec 4.2 calls the shift operator `S_v` an isometry with `||S_v||=1`. The
operator-norm claim (`sup_{||f||<=1} ||S_v f|| = 1`) is correct and is all
the subsequent `||K_B(h)||<=eps` bound needs. But `S_v` is not literally
an isometry: take `f` supported entirely on `[0,v)` — then
`(S_v f)(x) = f(x+v) \equiv 0` for all `x>=0`, while `||f||=1`. `S_v` is a
norm-1, non-expansive operator, not a norm-preserving one for every `f`.
Does not affect the correctness of any bound used downstream (only
`||S_v||<=1` is ever needed). Cosmetic/terminology only.

### M2 (LOW, scope note — not a document defect) — Sec 5.2 published anchors not independently re-derived this pass

Given the effort budget, priority went to Sec 4's operator bounds
(explicitly named by the mandate as the heart of the claim) and Sec 6's
genuinely new numerics, both independently verified. The `(P,Q)`-family
anchors at `c=1000` (Sec 5.2) were not re-derived from scratch a sixth
time in this review — they are the same anchors already independently
reproduced, digit-for-digit, by at least four prior referees documented in
`PROOF_DEPENDENCY_MAP.md`'s `PLATRESUM` addenda (waves 17, 19, 20, 22).
This is a scope choice on this referee's part, not a finding against the
document.

---

## 4. Independent computation log

All scripts in this directory were written fresh from the equations
quoted in `ATTEMPT.md`'s own prose. **No `.py` file belonging to this
front or any ancestor front was read at any point**, per the mandate.

| file | role |
|---|---|
| `r01_operator_norm_cancellation.py`/`.log` | Closed-form derivation of `h_eps(z) = \|1-eps*z\|*R(z)`; confirms `R(0)=sqrt(pi/2)` two ways (closed form + direct integral), then scans `h_eps` over four `eps` values, finding the global max at `z=0` in every case (Finding H1) |
| `r02_sup_over_x_vs_y.py`/`.log` | `sup_{x>=0} \|M_y K_A^raw(y,0)[1](x)\|` as a direct function of `y`, at `eps=0.1` and `eps=0.0316`, `y` from `0.001` to `1000` — confirms no growth in `y`, contrary to Sec 4.4 |
| `r03_raw_double_quadrature_crosscheck.py`/`.log` | Fully independent re-check of `r01`/`r02` via raw `mpmath.quad` double integration of the literal definitions, never invoking the `R(z)` closed form — magnitudes match to the precision shown |
| `r04_independent_neumann_iteration.py`/`.log` | From-scratch grid Picard/Neumann solver for the closed system `(E2')+(NEW-W)+(BB-Psi')+I`, coded from Sec 3–4 prose only, `numpy` float64, trapezoidal quadrature |
| `r05_finer_grid_c100_and_c1000.py`/`.log` | Runs `r04` at `h=0.1` (matching the target's own grid spacing) at `c=100` and `c=1000`; reproduces the Sec 6.2/6.3 successive-difference ratio tables |

### Sec 6.2/6.3 reproduction table (c=100 and c=1000)

| `c` | `y` | source | successive-difference ratios (n=1…5) |
|---|---|---|---|
| 100 | 0.5 | `ATTEMPT.md` Sec 6.2 | 0.207, 0.076, 0.044, 0.031, 0.025 |
| 100 | 0.5 | this review (`r05`) | 0.2067, 0.0760, 0.0442, 0.0314, 0.0247 |
| 100 | 1.0 | `ATTEMPT.md` Sec 6.2 | 0.552, 0.197, 0.105, 0.068, 0.049 |
| 100 | 1.0 | this review (`r05`) | 0.5516, 0.1970, 0.1052, 0.0678, 0.0490 |
| 100 | 2.0 | `ATTEMPT.md` Sec 6.2 | 1.124, 0.432, 0.238, 0.154, 0.109 |
| 100 | 2.0 | this review (`r05`) | 1.1244, 0.4323, 0.2379, 0.1536, 0.1089 |
| 1000 | 1.0 | `ATTEMPT.md` Sec 6.3 | 1.112, 0.447, 0.258, 0.175, 0.130 |
| 1000 | 1.0 | this review (`r05`) | 1.1125, 0.4468, 0.2580, 0.1749, 0.1301 |

Agreement to 3–4 significant digits at every tested point, both `c`
values, using an independently-written grid solver at the same grid
spacing (`h=0.1`) the target used. Strong evidence the Sec 5–6 numerical
content is genuine and correctly computed, not fabricated or
cherry-picked.

---

## 5. Sec 10 scorecard rows affected by Finding H1

| claim (as labeled in `ATTEMPT.md` Sec 10) | this review's finding |
|---|---|
| "Full kernel `K(y,t)` bounded on the UNRESTRICTED `x` domain" — **REFUTED** | **contradicted** — per this review's computation, appears bounded (`<= sqrt(pi/2)+eps`) |
| "Strip-restricted bound stays bounded as `y->infinity`" — **REFUTED** (grows linearly) | **contradicted** — per this review's computation, does not grow; saturates or decreases |
| `\|\|K_B(h)\|\| <= eps` unconditionally — **PROVED** | confirmed correct |
| `\|\|K_A^raw(y,t)\|\| <= eps*sqrt(pi/2)` unconditionally — **PROVED** | confirmed correct, as a standalone bound |
| Classical Volterra quasi-nilpotency, stated/re-derived — **PROVED** | confirmed correct |
| Discretized Neumann/Picard fixed point converges (Richardson `O(h^2)`) — **PROVED numerically** | not independently re-run (out of scope this pass) |
| Actual Neumann series converges at every tested finite `y` — **CONFIRMED numerically** | independently reproduced (Section 4 above) |

---

## 6. Overall verdict

**NEEDS REVISION.** Not a rejection of the front's contribution as a
whole — a correction to its Sec 4 claim specifically. Sec 2 (algebra),
Sec 3 (Volterra-in-`y` structure), and Sec 5–6 (numerics) are sound and
independently reproducible; the document's overall bottom line —
`(U1)`/`(U2)`/`H1` remain open, nothing closed, `phi_REDB` and every
formula of record untouched — is not threatened by anything found in this
review. But Sec 4's headline result, explicitly named by the dispatching
mandate as the heart of this front's claim, does not survive scrutiny:
the claimed "obstruction isolated to a single multiplication operator" is
not established by the document's own derivation, and direct, independent
computation via two structurally different routes (agreeing to the
precision shown) indicates the composed operator the document actually
points to is uniformly bounded, not growing in `y`. This affects the
VERDICT UP FRONT item 3, Sec 4.4, Sec 4.6's "two routes converge" framing,
and the two "REFUTED" rows of the Sec 10 scorecard identified in Section 5
above.

**Recommendation for integration** (for the orchestrating session, which
owns all ledger/map edits): the Sec 4 diagnosis should be corrected via a
dated addendum — ideally replaced with the sharper, more favorable bound
this review derives (`||M_y ∘ K_A^raw(y,t)|| <= sqrt(pi/2)` uniformly,
hence `||K(y,t)|| <= sqrt(pi/2)+eps` uniformly in `x,y,t`, including on
the unrestricted `x`-domain) — before this front is integrated at the
tier it currently claims for its Part C contribution. Nothing else in the
document requires revision; the non-closure verdict for `H1` and the Sec
5–6 numerical content can be integrated as claimed.

`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the four-term asymptotic
law of record are unaffected by any finding in this review.

---

## 7. Scope discipline

No edits made to `THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`,
`index.html`, or the target's own `ATTEMPT.md`. No `git` command of any
kind run. All writes confined to this `adversarial/` subdirectory. Per
`PROOF_DEPENDENCY_MAP.md` §3, no result from Tree A (`u1/2`) is cited
anywhere above, even in hedged language, and no finding in this review is
intended as evidence for anything in Tree A.
