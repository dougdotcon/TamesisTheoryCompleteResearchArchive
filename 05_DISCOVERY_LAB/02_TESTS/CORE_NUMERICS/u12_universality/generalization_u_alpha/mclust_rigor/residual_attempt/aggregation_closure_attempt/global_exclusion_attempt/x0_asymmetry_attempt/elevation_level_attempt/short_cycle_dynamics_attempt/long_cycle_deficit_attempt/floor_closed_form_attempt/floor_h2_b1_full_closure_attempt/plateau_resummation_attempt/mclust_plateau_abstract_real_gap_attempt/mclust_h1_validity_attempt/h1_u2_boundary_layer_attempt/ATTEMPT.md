# ATTEMPT — the boundary-layer content of `(U2)`: a uniform-in-`x`
# Poincaré expansion for `W_inf(x)`, including `x=O(eps)`
# (`H1-U2-BOUNDARY-LAYER-ATTEMPT`)

**Wave 27, front (a), `DISC-DEC-127`.** Target: `(U2)` specifically —
`DISC-DEC-088/091` (wave 20) — the uniform-in-`x` Poincaré asymptotic
expansion claimed for `W_inf(x;eps)`, including the boundary-layer scale
`x=O(eps)`. Seven consecutive waves (20–26) attacked the *companion*
condition `(U1)` by five genuinely different technical routes (Watson
concentration/energy estimate, Volterra quasi-nilpotency, translation
structure, Tauberian oscillation) and made real, catalogued progress on
`(U1)` — but, as the orchestrating session's own portfolio audit before
this wave confirmed (`DISC-DEC-127`, grep-verified independently below,
§0), none of those seven fronts made `(U2)` its own dedicated target;
every occurrence of `(U2)` in the record outside its own defining front
is a scoreboard entry ("OPEN, unchanged"), never itself attacked. This
front rotates to that untouched condition.

**This is `M-CLUST(b)` (Tree B of `PROOF_DEPENDENCY_MAP.md`), the `b=1`
floor's abstract `(s,g)` recursive process — pure combinatorial/asymptotic
mathematics about a random-permutation-with-reroutes ensemble. It is a
standalone object, entirely independent of the archive's separate Tree A
(`u1/2` / "Lemma Aberto") line in `THEOREM.md`. Nothing here is, or is
adjacent to, a Millennium Prize Problem, and no such claim appears
anywhere below.**

Reserved seed range for this front: `20260939000-20260939999`. Grep-
confirmed BEFORE any use to appear only in `DECISION_LEDGER.yaml`'s own
reservation line (§0 below), and again at the end (§10, Seeds). **No
randomness was needed anywhere in this front** — every result below is
exact symbolic reasoning (`sympy`) or deterministic arbitrary-precision
series summation (`mpmath`), exactly as every ancestor in this exact
sub-lineage reports.

---

## EXECUTIVE SUMMARY (read first)

**Tier: honest non-closure of `(U2)`, with (a) a new explicit closed-form
outer expansion for `W_inf(x;eps)` itself — never before written down in
this record — derived from already-established results and verified
symbolically end to end; (b) a precise structural diagnosis of the
boundary-layer question, showing it reduces to a *degenerate* matched-
asymptotics problem (no genuinely new "inner" equation with different
functional content) *conditional on* the outer coefficients' own
uniform validity — exactly the unresolved content seven prior waves
could not establish for the closely related condition `(U1)`; and (c) a
genuinely new numerical experiment — the first in this lineage to probe
`x` shrinking *at the same rate as* `eps` (`x=eps u`, `u` fixed, as
`eps->0`), rather than `x` fixed while `eps->0` — showing no sign
whatsoever of non-uniform behavior at the two orders tested, anywhere in
the boundary layer.** `(U2)` is **not closed**.

1. **The precise target, restated exactly (§1).** `W_inf(x;eps) :=
   \lim_{g\to\infty} W(x,g;eps)` (existence assumed by the companion
   condition `(U1)`, `mclust_h1_validity_attempt/ATTEMPT.md` §2.1,
   quoted verbatim below). `(U2)` claims this admits a genuine Poincaré
   expansion in `eps` as `eps\to0`, **uniformly in `x\in[0,\infty)`,
   including `x=O(eps)`**, with an `x`-independent `O(eps^{N+1})`
   remainder. This front confirms (mandate step: "verify this from the
   precise statement... rather than assuming") that the target genuinely
   *is* a classical matched-asymptotics/boundary-layer statement in the
   textbook sense: `x=O(eps)` is exactly the scale that dominates the
   Watson-type integral `Pi(c)=(1/eps)\int_0^\infty e^{-v/eps}W_inf(v)dv`
   (`STAR`) once `eps` is also sent to `0` — the record's own citation is
   explicit and this front does not need to reinterpret it.

2. **An "outer" expansion already exists in the record — for `F(x)`, not
   yet for `W_inf(x)` itself (§2).** The record's own matched-asymptotics
   derivation (`plateau_resummation_attempt/ATTEMPT.md` §4/§6) already
   gives `F(x;eps):=\lim_{g\to\infty}\Phi(x,g) = \sum_n eps^n\psi_n(x)`,
   `n\le4`, in closed form. This front does **not** re-derive `\psi_n`.
   What it derives, new: using the exact `W=\Psi-eps\Psi_x` identity
   (`KEY`, record) plus the already-stated hypotheses (ii)/(iii) of
   `mclust_h1_validity_attempt/ATTEMPT.md` §2.3 (`\lim_g\Psi=F`,
   `\lim_g\Psi_x=F'`), algebraically:

   ```
   W_inf(x;eps) = F(x;eps) - eps*F'(x;eps)                         (W-F)
   ```

   — new to the record. Substituting the outer series for `F` gives
   `W_inf`'s own outer coefficients, `chi_n(x) := psi_n(x) - psi_{n-1}'(x)`.
   This front proves (§2.2, symbolically, `sympy`, general `x`, machine-
   verified) a clean closed form for `n=1..4`:

   ```
   chi_n(x) = (gamma_n - gamma_{n-1}) * R^{(n-1)}(x)
   chi_1 = R(x),  chi_2 = R'(x),  chi_3 = (3/2) R''(x),  chi_4 = (13/6) R'''(x)
   ```

   using the record's own `gamma_n` sequence (`1,2,7/2,17/3`) and `R^{(n)}`
   closure identity — after also *generalizing* the record's own
   `psi_n(0)=gamma_n R^{(n-1)}(0)` (stated only at `x=0`) to
   `psi_n(x)=gamma_n R^{(n-1)}(x)` for **all** `x`, proved here by direct
   substitution into the record's own `psi_n` ODEs (§2.1). A self-
   consistency check (§2.3) re-derives the record's PUBLISHED 4-term law
   for `Pi(c)` via this `W_inf`+Watson's-lemma route and matches it
   EXACTLY, symbolically, at every one of the 4 known orders — strong
   internal confirmation that no arithmetic slip entered the `(W-F)`
   bookkeeping.

3. **Boundary-layer ("inner") analysis (§3).** Rescaling `x=eps u`
   (`u` fixed) — the variable the Watson integral itself dictates, not
   guessed — and combining `(W-F)` with the record's own exact `(ODE-F)`
   (`F'-xF=-C(x)`, `mclust_h1_validity_attempt` §2.3) gives an EXACT
   algebraic identity, new to the record:

   ```
   W_inf(x;eps) = F(x;eps)*(1 - eps*x) + eps*C(x;eps)              (W-F-C)
   ```

   Because every `chi_n(x)` derived in §2.2 is an ENTIRE function of `x`
   (built from `R` and its derivatives, `R(x)=\sqrt{\pi/2}\,erfcx(x/
   \sqrt2)` being entire), Taylor-re-expanding the outer series at
   `x=eps u` produces a REGULAR double series in `(eps,u)` with **no new
   singular content and no distinct inner functional form** — i.e. this
   specific boundary layer is *degenerate* in the classical taxonomy:
   the "inner solution" is simply the outer series' own Taylor expansion,
   and the matching condition is satisfied automatically, not as a
   nontrivial constraint. This is a genuine, checkable structural finding
   (§3.2), stated with its exact and important caveat: it is
   **conditional** on the outer coefficients' remainder staying uniform
   as `x\to0` — which is not established, is not implied by mere
   entireness, and is exactly a special/limiting case of the SAME
   uniform-rate problem that stopped all seven `(U1)`-attacking waves.
   **This is precisely where the analysis gets stuck (§3.3, §6)**: no
   route in this front, or any ancestor, supplies a uniform-in-`y\to
   \infty` convergence rate for `\Psi(x,g)\to F(x)` from the EXACT PDE
   system — everything downstream (§2, §3, §5) is built on the SAME
   heuristic matched-asymptotics status the rest of `H1` already carries.

4. **Fresh numerical machinery + the boundary-layer experiment (§4-§5).**
   A from-scratch `(P,Q)`-family recursion implementation (§4, no code
   opened from any ancestor front), validated **7/7** against the
   record's own published anchors (`a_2(0),a_3(0),a_4(0),b_2(0),b_1(0)`
   exact, `\Phi(0,0.002)`, and the `c=1000` plateau to `~34` matching
   digits — §4.2), is used for the first numerical test in this lineage
   of `x` shrinking **at the rate of `eps`** (`x=eps\,u`, `u\in\{0,1,2,4\}`
   fixed, `c\in\{1000,4000,16000,64000\}`, an `8\times` range in `eps`) —
   every ancestor grid used `x` FIXED while `eps\to0`. `W_inf(x;c)` is
   computed **directly** from the exact `\Psi` series and its
   `s`-derivative (via `KEY`, not through `(W-F)`'s own hypotheses),
   giving, as a genuine BONUS, the first independent numerical
   confirmation of hypothesis (ii) itself (`\lim_g\Psi=\lim_g\Phi`):
   agreement to `\sim10^{-33}`–`10^{-34}` relative at every one of the 20
   grid points (§5.2) — the ancestor front left this "not independently
   verified numerically beyond a leading-order consistency check."

   **Main result**: `resid5(x;eps):=(W_inf^{numeric}-W_pred^{(4)})/eps^5`
   stays **bounded and converges cleanly** (no blow-up, no divergence,
   monotone approach with the expected `O(eps)` rate) at **every** tested
   point, `u=0,1,2,4` AND a fixed bridge point `x=1` — direct numerical
   evidence FOR uniform validity through order 5, at `x=O(eps)`
   specifically, where no ancestor tested (§5.3). A KNOWN-order sanity
   check (`n=4`, using the already-PROVED `gamma_4=17/3`, not a
   conjecture) confirms the whole machinery reproduces the correct
   `chi_4(x)` with the theoretically-expected `O(eps)` convergence rate,
   uniformly across the boundary layer, BEFORE the order-5 numbers are
   trusted (§5.4). Richardson-extrapolating `resid5` to `eps\to0` at
   every point matches, to `0.02\%`–`0.6\%` (tightest near `x=0`), a
   SPECULATIVE extension of the `n\le4` closed form to `n=5` using the
   record's own **conjectured** (not derived) `gamma_5=209/24` — an
   independent, different-computational-route piece of evidence
   consistent with that conjecture, reported honestly as speculative,
   not as a proof of `gamma_5` (§5.5).

5. **Honest limitations (§6).** `(U2)` is not proved. The chain
   `psi_n\to chi_n\to` "degenerate boundary layer" is built entirely on
   the SAME heuristic (`H1`-status) matched-asymptotics content the rest
   of this sub-lineage already carries — this front does not touch the
   analytic obstruction (a uniform-in-`x`, `y\to\infty` convergence rate
   from the exact PDE system) that stopped all seven prior `(U1)`-
   attacking waves. The numerical evidence is real but structurally blind
   to non-perturbative (trans-series) content, tests only two successive
   orders, and — while it is the first test at `x=O(eps)` in this
   lineage — the tested `(c,u)` grid is still finite. `gamma_5=209/24`
   remains a conjecture; this front's agreement with it is supportive,
   not decisive.

`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, the 4-term asymptotic law, and
every formula of record: **untouched**. No claim of a proof of `H1`,
`(U1)`, `(U2)`, or any part of the 4-term (or any) asymptotic law is made
anywhere below. No `THEOREM.md`, `PROOF_DEPENDENCY_MAP.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, or ancestor front file was
opened for writing. No `adversarial/` subdirectory created; no referee
dispatched. No git command run.

---

## 0. Reading discipline and provenance

Read in full, in prose, before any derivation or code, per the mandate's
strict lineage convention:

- `DECISION_LEDGER.yaml`, the full `DISC-DEC-127` entry (this front's own
  authorization and rationale — the "rotation away from `(U1)`" decision).
- `PROOF_DEPENDENCY_MAP.md` §2 (Tree B), the `PLATRESUM` node's COMPLETE
  addenda history, every dated entry from `DISC-DEC-072/077` (wave 17,
  the original 4-term law) through `DISC-DEC-125` (wave 26, the most
  recent, `(H-osc)` shown logically unnecessary for `(U1)` specifically).
  Every occurrence of `(U2)` in this file was grepped and read in context
  (`DISC-DEC-088/091, 096/100, 110, 113, 115, 118, 122, 125` — 8 addenda
  mention it): in every one of them `(U2)` is listed alongside `(U1)` as
  part of the `H1` scoreboard ("`(U1)`, `(U2)` permanenceem ABERTOS" /
  "OPEN, unchanged") — **never** the front's own dedicated target. This
  independently confirms `DISC-DEC-127`'s own stated rationale for this
  wave's rotation.
- `mclust_h1_validity_attempt/ATTEMPT.md` in full (825 lines) — the
  PRIMARY source for `(U2)`'s exact statement (wave 20, `DISC-DEC-088/
  091`, the front that first reduced `H1` to `(U1)`+`(U2)` via the Watson
  Concentration Lemma). Every quoted formula in this document that is
  attributed to that front is transcribed, not paraphrased from memory —
  the exact hypothesis statements (§2.1 `(U1)`, §2.2 `(U2)`), the exact
  `(E1)/(KEY)/(E2)` system, the exact `(ODE-F)` derivation and its stated
  hypotheses (i)-(iii), and the exact post-adversarial notes (`DISC-DEC-
  091`) narrowing "equivalence" to "sufficiency" for `(U1)`+`(U2)`
  implying `H1`.
- `plateau_resummation_attempt/ATTEMPT.md` in full (961 lines) — the
  PRIMARY source for the established outer expansion `F(x;eps)=\sum
  eps^n\psi_n(x)`, its exact derivation (§4.1–§4.4b) including the closed
  forms `\psi_1=R`, `\psi_2=2xR-2`, `\psi_3(x)` (integral form + `\psi_3(0)`
  closed form), `\psi_4(x)=(17/3)R'''(x)`, the `\gamma_n` recursion and its
  explicit CONJECTURE status past `n=4` (§4.4b: "`gamma_5=209/24` onward
  is a PATTERN CONJECTURE"), and the record's own published `Pi(c)`
  4-term law used as this front's cross-check target (§2.3).
- Skimmed in full where `(U2)` is discussed (confirmed each front's own
  primary technical content is about `(U1)`/`\Phi`, not `(U2)`/`W_inf`'s
  boundary layer, matching `DISC-DEC-127`'s own framing exactly — grep
  counts and representative excerpts recorded in this front's own working
  notes, not reproduced here for brevity): `h1_energy_estimate_attempt/
  ATTEMPT.md` (`(U1)`/`(U2)` mentioned 14×, all scoreboard except one
  passage on approach-rate `x`-dependence noted in §5.3.4 below), `h1_
  volterra_attempt/ATTEMPT.md` (13×, all scoreboard/status), `h1_post_
  correction_attempt/ATTEMPT.md` (11×, scoreboard), `h1_translation_
  structure_attempt/ATTEMPT.md` (9×, scoreboard), `tauberian_oscillation_
  bound_attempt/ATTEMPT.md` (6×, scoreboard), `mclust_h2_validity_
  attempt/ATTEMPT.md` (7×, scoreboard — this front's own `H2` is a
  DIFFERENT, unrelated use of the letter "H2" from the `long_cycle_
  deficit_attempt` lineage's H1/H2 mixture-diagnosis; not to be confused
  with this document's own boundary-layer content). None of the six
  fronts attacked `(U2)` as a dedicated target; this front's reading
  confirms `DISC-DEC-127`'s claim with its own independent grep pass,
  not merely trusting the ledger's summary.

**Seed range grep-confirmed BEFORE any use**: `grep -rn "20260939"
05_DISCOVERY_LAB/` matched only `DECISION_LEDGER.yaml`'s own reservation
line (`DISC-DEC-127`), zero other occurrences — confirmed empty before
this front wrote anything. Re-confirmed at the end (§10).

**No `.py` file from any ancestor front in the `mclust_rigor` lineage was
opened, read, or imported at any point in this front.** Every script in
this directory (`u01`–`u08`) is written fresh from the mathematical
content of the prose cited above; every previously-published number used
as a cross-check (anchors, `Pi(1000)`, `\gamma_n`, `\psi_n(0)`, the
published `(H-osc)`/`(H-ces)` findings) is transcribed as plain text,
never imported as code.

`PROOF_DEPENDENCY_MAP.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `THEOREM.md`, and every ancestor front's own
`ATTEMPT.md`/`.py`/`adversarial/` were read-only references throughout;
nothing outside this front's own new subdirectory
(`.../mclust_h1_validity_attempt/h1_u2_boundary_layer_attempt/`) was
written to.

---

## 1. The precise target, restated exactly

Verbatim, `mclust_h1_validity_attempt/ATTEMPT.md` §2.1–§2.2 (this front's
required reading, transcribed not paraphrased):

> **Hypothesis (U1).** There is a function `W_inf(x)` (for the fixed
> `eps` under consideration) such that: for every `delta>0` there is
> `G(delta)` with `|W(x', g') - W_inf(x')| < delta` for ALL `g' >
> G(delta)` and ALL `x' in [x0, x0+G(delta)]`.
>
> ...
>
> **Hypothesis (U2).** `W_inf(x;eps)`, as a function of `x\ge0` for each
> `eps`, admits a genuine asymptotic (Poincaré) power series in `eps` as
> `eps\to0`, **uniformly for `x` in `[0,\infty)`** (in particular,
> remaining valid down to `x=O(eps)`, the boundary-layer scale that
> dominates the Watson-type integral in `(STAR)` once `eps` is also sent
> to `0`), with a remainder after `N` terms that is `O(eps^{N+1})` with a
> constant independent of `x`.

So: `W_inf(x;eps) := \lim_{g\to\infty} W(x,g;eps)` (existence, locally
uniform in `x`, is exactly what `(U1)` supplies); `W(x,g)` itself is
defined, exactly (`KEY`, record):

```
W(x,g) = Psi(x,g) - eps * Psi_x(x,g)
```

with `\Psi` the mode-`E` component of the exact `(x,y)`-rescaled PDE
system (`x=s\sqrt c`, `y=g\sqrt c`, `eps=1/\sqrt c`, all record notation,
`mclust_h1_validity_attempt` §0). `(U2)`'s target is a genuine
matched-asymptotics/boundary-layer statement in the textbook sense — this
front confirms this from the precise citation above rather than
assuming it, per the mandate: the phrase "the boundary-layer scale that
dominates the Watson-type integral" is the record's own, and is exactly
correct — substituting `v=eps\,u` into `(STAR)`,
`Pi(c)=(1/eps)\int_0^\infty e^{-v/eps}W_inf(v)\,dv = \int_0^\infty
e^{-u}W_inf(eps\,u)\,du`, shows the WHOLE mass of the integral (weight
`e^{-u}`, `O(1)` support in `u`) is contributed by `v=x=eps\,u=O(eps)` —
precisely the classical Watson's-lemma requirement that the integrand's
local Taylor behavior AT the lower endpoint (here rescaled to `u=O(1)`)
be what actually gets extracted, not its behavior at some fixed `x>0`
bounded away from `0`.

---

## 2. Does an "outer" expansion already exist? — Yes, for `F(x)`; this
front derives one, new, for `W_inf(x)` itself

### 2.1 Generalizing `psi_n(0)=gamma_n R^{(n-1)}(0)` to all `x`

The record's own matched-asymptotics derivation
(`plateau_resummation_attempt/ATTEMPT.md` §4) gives, for `F(x;eps):=
\lim_{g\to\infty}\Phi(x,g)` (so `F(0)=Pi(c)`):

```
F(x;eps) = eps*psi1(x) + eps^2*psi2(x) + eps^3*psi3(x) + eps^4*psi4(x) + O(eps^5)
psi1(x) = R(x) := sqrt(pi/2)*erfcx(x/sqrt2),   R' = xR - 1,  R(inf)=0
psi2(x) = 2xR(x) - 2
psi3(x) = -e^{x^2/2} int_x^inf e^{-t^2/2} 7R'(t) dt     [record's stated ODE: psi3'=x*psi3+7R']
psi4(x) = (17/3) R'''(x)                                 [record's stated ODE: psi4'=x*psi4+17R'']
```

with `gamma_n:=\psi_n(0)/R^{(n-1)}(0)` published only AT `x=0`:
`gamma_1,...,gamma_4 = 1, 2, 7/2, 17/3` (record, `plateau_resummation_
attempt` §4.4b, V18).

**This front's first new result**: `psi_n(x)=gamma_n\,R^{(n-1)}(x)` holds
for ALL `x`, not just `x=0` — verified symbolically
(`u01_symbolic_outer_expansion.py`, sympy, general `x`) by direct
substitution into the record's own stated `\psi_n` ODEs, using the
record's own `R^{(n+1)}=xR^{(n)}+nR^{(n-1)}` closure identity (cross-
checked independently against direct repeated differentiation of
`R'=xR-1`, `n=0..5`, all match exactly):

```
n=2: psi_2' - x*psi_2 - 2R          = 0   (candidate 2*R'(x) solves it exactly)
n=3: psi_3' - x*psi_3 - 7R'         = 0   (candidate (7/2)*R''(x) solves it exactly)
n=4: psi_4' - x*psi_4 - 17R''       = 0   (candidate (17/3)*R'''(x) solves it exactly,
                                            MATCHES the record's own already-stated closed form)
```

all three residuals **exactly `0`** symbolically (not a numeric
approximation). Boundedness as `x\to\infty` (needed to select this as the
UNIQUE solution the record intends, among the ODE's two-parameter family
— the homogeneous mode `A\,e^{x^2/2}` diverges for any `A\ne0`, exactly
the mechanism of the record's own `H2`/Growth-Exclusion Lemma,
`mclust_h2_validity_attempt`, cited not re-derived) follows because every
`R^{(k)}(x)` is, by the SAME closure identity, a combination of `R` and
lower derivatives, all sharing `R`'s own bounded/decaying branch (the
record's stated `R(x)\to0`), never the divergent homogeneous mode.
Sanity check at `x=0` reproduces every one of the record's own published
values EXACTLY (`\psi_2(0)=-2`, `\psi_3(0)=(7/2)\sqrt{\pi/2}`,
`\psi_4(0)=-34/3`) — a strong confirmation before building on top of it.

### 2.2 The `(W-F)` relation and `W_inf`'s own outer expansion, `chi_n(x)`

From `KEY` (record, exact) and hypotheses (ii)/(iii) of `mclust_h1_
validity_attempt` §2.3 (`\lim_g\Psi(x,g)=F(x)`, `\lim_g\Psi_x(x,g)=F'(x)`
— quoted, not re-derived, and inherited with their SAME conditional
status), taking `g\to\infty` in `W=\Psi-eps\,\Psi_x` gives, algebraically:

```
W_inf(x;eps) = F(x;eps) - eps*F'(x;eps)                              (W-F)
```

**New to the record** — `W_inf`'s own eps-coefficients had never before
been written down; only its EXISTENCE was hypothesized (`(U1)`) and its
INTEGRAL against the Watson kernel used (`(STAR)`). Substituting the
outer series for `F` and matching powers of `eps`:

```
W_inf(x;eps) = sum_n eps^n [psi_n(x) - psi_{n-1}'(x)]  =:  sum_n eps^n chi_n(x)
```

Computed symbolically (`u01_symbolic_outer_expansion.py`, Part 2), then
CONFIRMED to collapse to the clean closed form (verified exactly,
`sympy`, `n=1..4`):

```
chi_n(x) = (gamma_n - gamma_{n-1}) * R^{(n-1)}(x)      [gamma_0 := 0]
chi_1(x) = R(x)
chi_2(x) = R'(x)              = x*R(x) - 1
chi_3(x) = (3/2) R''(x)        = (3/2)*[R(x) + x*R'(x)]
chi_4(x) = (13/6) R'''(x)
```

### 2.3 Self-consistency check: re-derive the record's own published
4-term law via this route

If `(U2)`'s classical-Watson-lemma machinery is applied TERM BY TERM to
`chi_n(v)=(gamma_n-gamma_{n-1})R^{(n-1)}(v)` (each entire, admitting the
textbook Taylor-at-`0` hypothesis) inside `(STAR)` at `x_0=0`:

```
Pi(c) = (1/eps) int_0^inf e^{-v/eps} W_inf(v;eps) dv
      ~ sum_N eps^N * [ sum_{n=1}^{N} (gamma_n-gamma_{n-1}) * R^{(N-1)}(0) ]     (Watson's lemma,
                                                                                   term by term)
      = sum_N eps^N * gamma_N * R^{(N-1)}(0)                [TELESCOPES EXACTLY,
                                                               sum_{n=1}^N (gamma_n-gamma_{n-1})
                                                               = gamma_N - gamma_0 = gamma_N]
```

— i.e. this front's `W_inf`-based route, recombined through Watson's
lemma, reproduces EXACTLY the record's own `\psi_N(0)=\gamma_N
R^{(N-1)}(0)` rule applied directly to `Pi(c)=F(0;eps)`. Verified
symbolically at `N=1..4` (`u01_symbolic_outer_expansion.py`, Part 3): the
resulting coefficients match the record's published 4-term law

```
Pi(c) = sqrt(pi/(2c)) - 2/c + (7/2)sqrt(pi/2)*c^{-3/2} - (34/3)*c^{-2} + O(c^{-5/2})
```

**digit-for-digit, symbolically** (`sympy.simplify` of the difference
returns exactly `0` at every one of the 4 orders — `u01_symbolic_outer_
expansion.log`). This is a nontrivial internal-consistency check (the two
routes — direct outer expansion of `F`, vs. this front's `W_inf` route —
are the SAME underlying heuristic content organized two different ways,
and MUST agree if no arithmetic slipped into `(W-F)` or the `chi_n`
bookkeeping); it is **not** an independent proof of the 4-term law (it
uses exactly the same heuristic ingredients, only recombined).

---

## 3. Boundary-layer ("inner") analysis at `x = eps*u`

### 3.1 The natural inner variable, derived not guessed

The mandate asks for the natural boundary-layer variable to be DERIVED
from the actual governing equation, not assumed. §1 already answered
this from the Watson integral `(STAR)` itself: substituting `v=eps\,u`
is what makes the kernel `O(1)`-supported in `u`, so `u:=x/eps` is
exactly the variable the equation dictates — matching the classical
matched-asymptotics convention (`x=eps\,u`) named in the mandate.

### 3.2 An exact algebraic identity for `W_inf` at the inner scale

Combining `(W-F)` with the record's OWN exact `(ODE-F)`
(`mclust_h1_validity_attempt` §2.3, conditional on that front's stated
integrability hypotheses (i)-(iii), cited not re-derived):

```
F'(x) - x*F(x) = -C(x),   C(x) := int_0^infty [Phi(x,y') - F(x)] dy'      (ODE-F, record)
```

substituting `F'=xF-C` into `(W-F)` gives, algebraically (new to the
record):

```
W_inf(x;eps) = F(x;eps)*(1 - eps*x) + eps*C(x;eps)                    (W-F-C)
```

At `x=eps\,u`:

```
W_inf(eps*u; eps) = F(eps*u;eps)*(1 - eps^2*u) + eps*C(eps*u;eps)
```

This IS the "inner problem" the mandate asks for — but it resolves to an
ALGEBRAIC substitution, not a fresh differential equation to solve at the
rescaled variable. Two observations:

1. **`(1-eps^2 u)`** only departs from `1` at `O(eps^2)` — since `F`
   itself starts at `O(eps)`, this factor only affects `W_inf`'s OWN
   coefficients from order `eps^3` onward, consistent with (not a new
   derivation beyond) the direct `chi_n=\psi_n-\psi_{n-1}'` computation
   of §2.2 — the two routes must, and do, agree order by order (checked
   symbolically as part of §2.2/§2.3; not reproduced as a third
   redundant derivation here).
2. **`C(x;eps)`'s own expansion is NOT independently derived by this
   front beyond the record's own LEADING-order consistency check**
   (`mclust_h1_validity_attempt` §2.3: `C(x)\approx eps\cdot1+O(eps^2)`,
   `x`-independent at leading order) — pushing `(W-F-C)` further would
   need `C(x)`'s `eps^2,eps^3,eps^4` coefficients, which requires
   integrating `\Phi(x,y')-F(x)` over the FULL `y`-dependence (not just
   the plateau), a genuinely separate computational undertaking this
   front did not attempt (named as a concrete open item, §6, §8).

### 3.3 Structural finding: this boundary layer is *degenerate*
(conditional) — and precisely where that conditionality bites

Every `chi_n(x)` derived in §2.2 (equivalently, via `(W-F-C)`, every
`\psi_n(x)`, `R^{(k)}(x)`) is an **entire function of `x`**
(`erfcx(z)=e^{z^2}erfc(z)` is entire; polynomials times an entire
function are entire). Consequently, Taylor-re-expanding `chi_n(eps\,u)`
about `u=0` — i.e. `\chi_n(x)=\chi_n(0)+eps\,u\,\chi_n'(0)+O(eps^2)` — and
resubstituting into the (already known, `eps`-power) outer series
produces a REGULAR double series in `(eps,u)` with no new singular terms
at ANY finite order: the naive substitution `x\to eps\,u` into the SAME
outer formula, term by term, is well-defined and consistent, with no
obstruction, through every order this front computed (`n\le4` proved,
`n=5` numerically supported, §5).

**This is the precise, checkable content of "the boundary layer is
degenerate" here**: unlike a classical singular-perturbation boundary
layer (e.g. a viscous shock profile, where the inner solution has a
GENUINELY different functional form — `\tanh`, not a Taylor truncation of
the outer solution — and the matching condition is a real, nontrivial
constraint that PICKS OUT free constants), this system's candidate
"inner solution" is *literally* the outer series' own Taylor re-
expansion. The matching condition (inner's `u\to\infty` limit equals
outer's `x\to0^+` limit) is therefore satisfied **automatically, by
construction**, not as an independent check — there is no free constant
left to pin, and no separate inner boundary-value problem to solve.

**The exact and important caveat, stated as precisely as this front can
make it — this is where the analysis genuinely gets stuck:**

This finding is **conditional** on the outer coefficients' `eps`-series
remainder staying UNIFORM as `x\to0` — entireness of `\chi_n(x)`
guarantees each TRUNCATED partial sum is well-defined at `x=O(eps)`, but
says **nothing** about whether the `O(eps^{N+1})` remainder after `N`
terms stays bounded by a CONSTANT INDEPENDENT of `x` as `x\to0` at the
SAME rate as `eps\to0` — which is exactly `(U2)`'s own literal content,
restated, not resolved. Establishing that antecedent would require an a
priori bound on the EXACT (not asymptotically-expanded) system — e.g. a
maximum-principle/energy-estimate argument controlling how fast
`\Psi(x,g)\to F(x)` as `g\to\infty`, UNIFORMLY in `x` including as
`x\to0` — and this is **not a new, easier problem**: it is a special/
limiting case of the SAME uniform-rate estimate that seven consecutive
waves (`DISC-DEC-096,110,113,115,118,122,125`) attempted for `(U1)` by
five different techniques and did not close:

- **energy estimate/contraction** (`DISC-DEC-096/100`): got a global
  oscillation bound but the contraction constant is `\le1`, not `<1` —
  not a contraction; Watson/Laplace expansion of the identity recovers
  only algebraic, not the needed exponential, content in `y`.
- **Volterra quasi-nilpotency** (`DISC-DEC-113/115`): after a real,
  adversarially-caught correction, PROVES Neumann-series convergence
  locally uniformly in `y` on every COMPACT `[0,Y]` — but not a rate
  uniform as `Y\to\infty`, which is exactly what would be needed here.
- **translation structure** (`DISC-DEC-118/122`): finds a clean closed-
  form leading asymptotic for the FULL kernel `K(y,t)\sim1/(x+y)`, and
  reduces `(U1)` to Cesàro-`(C,1)` convergence of a running average — but
  that reduction is about the `y\to\infty` behavior of `\Phi`, a
  DIFFERENT (if related) object from the `x\to0` behavior `(U2)` needs.
- **Tauberian oscillation** (`DISC-DEC-125`): shows `(H\text{-}osc)` is
  achievable but that `(H\text{-}ces)` — Cesàro convergence of the mean
  itself — remains open and is NOT implied by the oscillation bound,
  via an explicit non-convergent counterexample.

None of these four routes, even where successful, supplies what `(U2)`'s
`x\to0` boundary layer needs: a bound UNIFORM IN `x` (not just in `y`) on
how the exact system's remainder behaves. This front does not find a
fifth route either — the numerical evidence of §5 is real and positive,
but it is evidence, not the missing uniform-rate estimate.

---

## 4. Numerical machinery: a fresh general-`s` `(P,Q)`-family
implementation

### 4.1 Implementation (`u02_family_series.py`)

Independently re-derived (worked through by hand before any code was
written) from the record's own recursion (`mclust_h1_validity_attempt`
§0, quoted in full there):

```
Phi(s,g)=sum_k a_k(s) g^k,  Psi(s,g)=sum_k b_k(s) g^k,  a_0=1, b_0=0
a_{k+1}=[a_k' - c a_k + c w_k]/(k+1)
b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}      (bounded branch)
w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
a_1=-c, b_1=sqrt(pi c/2)*erfcx(s sqrt(c/2))
every a_k,b_k in F = {P(s)+Q(s) erfcx(s sqrt(c/2))}, P,Q polynomials
```

Every `a_k,b_k` is stored as a `(P,Q)` coefficient-list pair. The family
is closed under `d/ds` via `E'=c\,s\,E-sc` (`sc:=\sqrt{2c/\pi}`):
`(P+QE)'=(P'-sc\,Q)+(Q'+cs\,Q)E` — implemented directly (`fam_deriv`),
needing no solve. The `b_k` ODE (`b_k'-cs\,b_k=A+B\,E`) is solved for
`b_k=U+V\,E` by: `V=\int B+\kappa` (`\kappa` free); `U'-cs\,U=A+sc\,V=:
\tilde R` solved by a DESCENDING polynomial recursion on `\tilde R`'s
coefficients (worked out from scratch in the module docstring: matching
`s^j` coefficients of `U'-cs\,U=\tilde R` gives `(j{+}1)u_{j+1}-c\,
u_{j-1}=r_j`; the two TOP coefficients of `U` follow directly from the
top two `j`, then descend by steps of `2` using only already-known
values; the LEFTOVER `j=0` relation `u_1=r_0` — unused by the descending
chain, which never touches `r_0` — PINS `\kappa=(u_1-A_0)/sc`, matching
the record's own prose description of this method).

### 4.2 Validation (`u03_validate_anchors.py`/`.log`)

**7/7 PASS** against the record's own published anchors at `c=1000`:

| quantity | this front's value (leading digits) | published anchor | reldiff | verdict |
|---|---|---|---|---|
| `a_2(0)` | `520316.636488030...` | `520316.636488` | `5.8e-14` | PASS |
| `a_3(0)` | `-180730907.628508...` | `-180730907.6285` | `4.5e-14` | PASS |
| `a_4(0)` | `47146963944.1379...` | `47146963944.14` | `4.5e-14` | PASS |
| `b_2(0)` | `-20816.6364880301...` | `-20816.636488` | `1.4e-12` | PASS |
| `b_1(0)` | `39.6332729760601...` | `\sqrt{\pi c/2}` | `0` (exact) | PASS |
| `\Phi(0,0.002)` | `0.15850014574730...` | `0.15850015` | `2.7e-8` | PASS |
| `\Phi(0,t_0\!\ge\!\text{plateau})` | `0.0377615983402126188243712...` | `0.0377615983402126188243712025905770...` | matches to `\sim34` digits | PASS |

(the last row: this front's own `K=400,\text{dps}=250`, `c\,t_0\in
\{60,80\}` run, independently converged — two-`t_0` self-consistency
`\sim9\times10^{-26}` relative — reproduces the RECORD'S OWN
independently-published `Pi(1000)` to `\sim34` matching decimal digits
before the two values diverge, comfortably beyond this front's own
`\sim25`-digit internal precision claim).

Every single `b_k` ODE-solve, at every `k` up to the largest `K` used
anywhere in this front, is ALSO validated directly (residual of the
solved `(U,V)` plugged back into the ODE, at 4 sample `s` points, via an
INDEPENDENT code path — `fam_deriv`, not the descending-recursion algebra
itself) before being trusted — this is how the one genuine bug this front
introduced (§7, S1) was caught immediately, before any new result was
computed from it.

---

## 5. The boundary-layer experiment

### 5.1 Setup (`u06_boundary_layer_experiment.py`)

`c\in\{1000,4000,16000,64000\}` (an `8\times` range in `eps=1/\sqrt c`,
from `0.0316` to `0.00395`); at each `c`, `K=400,\text{dps}=250`
(empirically sized, `u04`/`u05` probes — see §7, S3 for the disclosed
mis-step in first choosing this sizing), verified via the SAME two-`t_0`
convergence check this lineage uses throughout (`c\,t_0\in\{60,80\}`;
`\sim24`–`27` stable digits at every one of the 20 grid points, well past
what this front needs to see an `O(eps^5)` effect against an `O(eps^4)`
term — §5.2 table). Test points: a fixed bridge `x=1` (continuity with
`mclust_h1_validity_attempt`'s own, different, `x`-FIXED grid), and — the
genuinely new content — `x=eps\,u` for `u\in\{0,1,2,4\}`, i.e. `s=u/c`:
`x` **shrinking at the rate of `eps`**, which NO ancestor grid tested
(`mclust_h1_validity_attempt`'s own grid was `x\in\{0,0.5,1,2,4,6,8\}`,
independent of `eps`, confirmed by re-reading that front's prose, §0).

At each point, computed DIRECTLY (not via `(W-F)`'s hypotheses):

```
Psi_plateau(s;c)  := sum_k b_k(s) t0^k          (two-t0 checked)
Psi_x_plateau(s;c):= (1/sqrt(c)) * sum_k [b_k'(s)] t0^k    (fam_deriv on every b_k; two-t0 checked)
W_inf_numeric(x;c):= Psi_plateau - eps*Psi_x_plateau                       (KEY, exact)
```

plus, as an independent cross-check, `F_{plateau}(s;c):=\sum_k a_k(s)
t_0^k` (same two-`t_0` check).

### 5.2 Bonus finding: numerical confirmation of hypothesis (ii)

`mclust_h1_validity_attempt` §2.3 states hypothesis (ii)
(`\lim_g\Psi(x,g)=F(x)`) but discloses it "not independently verified
numerically beyond a leading-order consistency check." This front's
`Psi_plateau` and `F_{plateau}` are computed from entirely SEPARATE
series (`b_k` vs. `a_k`) — their agreement is a genuine, independent
numerical test, not a tautology:

| `c` | point | `\lvert\Psi_{plateau}-F_{plateau}\rvert/\lvert F_{plateau}\rvert` |
|---|---|---|
| 1000 | `x=1` (bridge) | `4.5\times10^{-34}` |
| 1000 | `u=0` | `1.9\times10^{-34}` |
| 4000 | `u=0` | `4.3\times10^{-34}` |
| 16000 | `u=0` | `1.1\times10^{-33}` |
| 64000 | `u=0` | `2.6\times10^{-33}` |

(full 20-point table: `u06_boundary_layer_experiment.log`). Hypothesis
(ii) holds to `\sim33`–`34` decimal digits at every tested point — the
first independent numerical confirmation of this specific hypothesis
beyond the leading-order check the record left it at.

### 5.3 Main result: `resid5` stays bounded through the boundary layer

```
resid5(x;eps) := (W_inf_numeric(x;c) - W_pred4(x;eps)) / eps^5
W_pred4(x;eps) := eps*R(x) + eps^2*R'(x) + eps^3*(3/2)*R''(x) + eps^4*(13/6)*R'''(x)   (chi_1..chi_4, §2.2)
```

| `c` | eps | `x=1` (bridge) | `u=0` | `u=1` | `u=2` | `u=4` |
|---|---|---|---|---|---|---|
| 1000 | `3.162\times10^{-2}` | `1.5773` | `10.476` | `9.802` | `9.176` | `8.053` |
| 4000 | `1.581\times10^{-2}` | `1.6332` | `10.933` | `10.574` | `10.228` | `9.572` |
| 16000 | `7.906\times10^{-3}` | `1.6628` | `11.179` | `10.993` | `10.811` | `10.456` |
| 64000 | `3.953\times10^{-3}` | `1.6780` | `11.306` | `11.212` | `11.118` | `10.933` |

(full precision, `u06_boundary_layer_experiment.log`.) **At every one of
the 5 columns, `resid5` stays `O(1)` — bounded, not diverging — and
converges MONOTONICALLY as `eps\to0`, with increments shrinking by a
factor `\approx0.5`–`0.59` at each `c\times4` step, consistent with an
`O(eps)` next-order correction (i.e. `resid5(eps)=L(x)+A(x)\,eps+
O(eps^2)`) — exactly the qualitative signature a genuinely valid,
uniform asymptotic expansion should show, and the qualitative OPPOSITE of
what a non-uniformity (error blowing up as `x\to0` faster than `eps\to0`)
would look like.** This holds identically at `u=0,1,2,4` — i.e.
**genuinely inside the boundary layer, `x=O(eps)`, shrinking with
`eps`** — not merely at fixed `x`. No sign of breakdown was found
anywhere in this grid.

### 5.4 Sanity check at the KNOWN order (`n=4`, before trusting `n=5`)

Before treating any order-5 extrapolation as meaningful, this front
checks `resid4(x;eps):=(W_inf_numeric-W_pred3)/eps^4 \to chi_4(x)=(13/6)
R'''(x)` — a **non-speculative** prediction, using the already-PROVED
`\gamma_4=17/3` (§2.1), not a conjecture (`u08_order4_sanity_check.py`):

| `c` | eps | reldiff at `x=1` | reldiff at `u=0` | reldiff at `u=4` |
|---|---|---|---|---|
| 1000 | `3.162\times10^{-2}` | `-6.10\%` | `-7.64\%` | `-7.43\%` |
| 4000 | `1.581\times10^{-2}` | `-3.16\%` | `-3.99\%` | `-3.93\%` |
| 16000 | `7.906\times10^{-3}` | `-1.61\%` | `-2.04\%` | `-2.02\%` |
| 64000 | `3.953\times10^{-3}` | `-0.81\%` | `-1.03\%` | `-1.03\%` |

The relative discrepancy **halves at every step** (ratio `0.505`–`0.518`
at every column, converging cleanly toward the theoretically-expected
`1/2` as `c\times4\Rightarrow eps\times1/2`), confirming `resid4\to
chi_4(x)` with exactly the expected `O(eps)` rate, UNIFORMLY across the
whole tested boundary layer — direct evidence this front's machinery is
computing `W_inf` correctly (a KNOWN quantity is reproduced correctly)
before the order-5 numbers (§5.5, built on a CONJECTURE) are given any
weight.

### 5.5 Richardson extrapolation and a speculative order-5 comparison

Two-point Richardson extrapolation (`L=2\,v(eps_{\min})-v(2\,eps_{\min})`,
exact since the `c`-ladder gives `eps` ratio exactly `2`; cross-checked
against the alternate pair from `c=1000,4000` — differences shrink toward
`0` as `u` decreases, consistent with genuine `O(eps)` convergence, not
noise) of `resid5` to `eps\to0`, compared against the SPECULATIVE
extension `chi_5(x):=(\gamma_5-\gamma_4)R''''(x)` using the record's own
**conjectured** (`plateau_resummation_attempt` §4.4b: "a PATTERN
CONJECTURE", not derived) `\gamma_5=209/24`:

| point | `x_{pred}` used | extrapolated `L` | `chi_5(x_{pred})` (speculative) | relative diff |
|---|---|---|---|---|
| `x=1` (bridge) | `1` | `1.693274485...` | `1.693586082...` | `-0.0184\%` |
| `u=0` | `0` | `11.433314606...` | `11.436491503...` | `-0.0278\%` |
| `u=1` | `0` | `11.430109750...` | `11.436491503...` | `-0.0558\%` |
| `u=2` | `0` | `11.425241279...` | `11.436491503...` | `-0.0984\%` |
| `u=4` | `0` | `11.410713604...` | `11.436491503...` | `-0.2254\%` |

(`x_{pred}=0` for every `u`-row: since `x=eps\,u\to0` as `eps\to0` for
ANY fixed `u`, the correct extrapolation TARGET is `\chi_5(0)`
regardless of `u` — `u` affects only the sub-leading approach, exactly
as observed: agreement is tightest at `u=0` and degrades smoothly as `u`
grows, the expected pattern, not an anomaly.)

**Reading this honestly**: this is real, independent, fresh evidence —
via a COMPLETELY different computational route (`\Psi/b_k` series and the
`KEY` identity, never touching the `\Phi/a_k` series or the ancestor
fronts' own residual-isolation fit that produced their own `d_4,d_5`
estimates) — CONSISTENT WITH the record's `\gamma_5=209/24` conjecture,
strengthening it modestly. It is **not** an independent derivation of
`\gamma_5` (this front's own prediction formula takes `\gamma_5` as an
INPUT, not something derived here from the boundary-layer machinery
carried to a genuine 5th order — that derivation, following the exact
pattern of the record's own `V15`–`V17` groups, was not attempted, named
as a concrete next step, §8).

---

## 6. Honest final verdict

**`(U2)` is NOT closed.** What this front contributes:

1. A precise confirmation (§1) that `(U2)`'s target is genuinely a
   classical boundary-layer/matched-asymptotics statement in the
   textbook sense, derived directly from the Watson integral `(STAR)`,
   not assumed.
2. A genuinely new closed-form outer expansion for `W_inf(x;eps)` itself
   (§2), `chi_n(x)=(gamma_n-gamma_{n-1})R^{(n-1)}(x)`, `n=1..4`, PROVED
   symbolically from already-established record content (the `(W-F)`
   relation, the record's own `psi_n` ODEs generalized to all `x`), and
   independently self-consistency-checked by re-deriving the record's
   published 4-term law exactly through this route.
3. A precise structural diagnosis (§3) that this specific boundary layer
   is *degenerate* — no genuinely new inner equation/functional form is
   needed, matching is automatic — **conditional** on the outer
   coefficients' remainder staying uniform as `x\to0`, which is NOT
   established here and is shown (§3.3) to be a special case of the SAME
   uniform-rate obstruction that stopped all seven prior `(U1)`-attacking
   waves by five different techniques.
4. A fresh, independently-validated numerical machinery (§4) and the
   first experiment in this lineage to test `x` shrinking AT THE SAME
   RATE as `eps` (§5) — showing NO sign of non-uniform behavior anywhere
   tested, at two successive orders, plus a bonus independent numerical
   confirmation of hypothesis (ii) and speculative-but-consistent support
   for the record's own conjectured `\gamma_5`.

**This is real, positive, checkable progress — but it is evidence, not
proof.** The single largest remaining gap is exactly the one that has
resisted seven prior waves: a rigorous, `x`-uniform (as `y\to\infty`)
convergence-rate estimate for `\Psi(x,g)\to F(x)` from the EXACT PDE
system. Nothing in this front supplies that estimate; everything here is
built on top of the SAME heuristic matched-asymptotics status the rest of
`H1` already carries, made more explicit and tested more widely, not made
rigorous.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)`, and the 4-term asymptotic law
of record are all untouched and unaffected by anything in this document.

---

## 7. Self-caught issues (disclosed, per this lineage's convention)

**S1 (this front's own catch, the most consequential — a genuine
algebra bug in this front's OWN validation code, caught immediately by
its own discipline before propagating).** The first draft of
`validate_b_ode` computed `b' - c\,b` (a plain scalar multiple of `b`)
instead of the correct `b' - c\,s\,b` (multiply by the POLYNOMIAL `c\,s`,
requiring a shift-and-scale, not a constant scale) — i.e. used
`fam_scale(b,-c)` where `fam_mul_cs(b,-c)` (a new helper, not yet
written) was needed. **Caught**: running the validation on the `k=1`
BASE CASE (`b_1`, given directly in closed form, before ANY of the
recursion's own machinery had a chance to introduce a genuine error)
immediately failed with a residual of `39633.27...` — an unmistakably
`O(1)`-scale (not rounding-scale) discrepancy, flagged before a single
new coefficient was trusted. Fixed by adding `fam_mul_cs` and correcting
`validate_b_ode`; re-run passed cleanly on the base case and every
subsequent `k`. This is a bug in this front's OWN validation harness, not
in `solve_b_ode`/`solve_polynomial_ode` themselves (which correctly used
the polynomial-shift operation throughout) — but it means the FIRST
attempted validation run would have silently reported a false negative
had this front not re-derived and re-checked the failure's magnitude
before assuming the CORE algorithm was wrong.

**S2 (this front's own finding, a calibration/tuning issue, not a
mathematical bug).** The initial validation tolerance for the per-`k`
ODE-residual sanity check was set as a fixed fraction of the working
`dps` (e.g. `10^{-(dps-10)}`, then `-20`, then `-30`) — each of these,
in turn, spuriously failed at successively larger `k` as the recursion's
own coefficient magnitudes grew (the SAME well-documented "order-2
entire" cancellation content this lineage has repeatedly hit elsewhere)
and ate into the fixed `dps` budget: e.g. at `dps=90`, relative residual
was `\sim1.9\times10^{-60}` at `k=85` but `\sim2.8\times10^{-20}` at
`k=195` — genuine, EXPECTED precision decay, not an algorithm error
(confirmed by the fact the SAME formula, already validated correct
against 5 published anchors at low `k`, is applied identically at every
`k`). Resolved by using a FIXED, generous relative tolerance (`10^{-8}`)
— far below any real `O(1)`-scale bug's signature (as S1's `\sim4\times
10^4` showed) but comfortably above ordinary rounding/magnitude-growth
noise at the `(K,\text{dps})` sizes this front actually uses.

**S3 (this front's own finding, a methodology mis-step, corrected before
any new result depended on it).** The FIRST attempt at the plateau
computation matched the ANCESTOR fronts' own DEEP precision target,
`c\,t_0\in\{230,260\}` (aimed, by those fronts, at `\ge110` STABLE
digits) — at `K=800,\text{dps}=550`, this gave essentially **zero**
converged digits (`reldiff(lo,hi)\approx0.9999...`, i.e. `\sim100\%`
relative disagreement between the two `t_0` checks): those ancestor
fronts report needing `K\sim2000` at `c=1000` for that specific target,
far beyond what this front had tried. **Caught** by the same two-`t_0`
convergence discipline this lineage uses throughout, BEFORE trusting any
number from that run. This front does not need `\ge110` digits — only
enough to see an `O(eps^5)` effect clearly against the `O(eps^4)` term
(`\sim20$–$25` digits comfortably suffices) — so `c\,t_0\in\{60,80\}` was
used instead (approach error `\sim e^{-60}\sim10^{-26}`, already more
than sufficient), converging cleanly at a MUCH smaller `K=400,
\text{dps}=250` (verified, `u04`/`u05` probe scripts, `\sim24$–$27`
stable digits at every point in the main grid, §5.1). No number from the
failed `c\,t_0=230/260`, `K=800` attempt is used anywhere in this
document.

---

## 8. What remains open

1. **`(U2)` itself is not proved.** The single largest gap: a rigorous,
   `x`-uniform convergence-rate estimate for `\Psi(x,g)\to F(x)` as
   `g\to\infty`, from the EXACT PDE system — not attempted here, and (§3.3)
   shown to be a special/limiting case of the SAME obstruction that
   stopped seven prior `(U1)`-attacking waves by five distinct techniques.
2. **`C(x;eps)`'s own `eps`-expansion is known only at leading order**
   (record: `C(x)\approx eps+O(eps^2)`, `x`-independent). Computing its
   `eps^2,eps^3,eps^4` coefficients — which would need integrating
   `\Phi(x,y')-F(x)` over the full `y`-range, not just the plateau — is a
   concrete, well-defined, not-yet-executed next step that would make the
   `(W-F-C)` route (§3.2) fully independent of the direct `chi_n=
   \psi_n-\psi_{n-1}'` route, rather than merely consistent with it.
3. **`\gamma_5=209/24` remains a conjecture.** This front's §5.5 finding
   is supportive (agreement to `0.02\%$–$0.6\%` from a genuinely
   independent computational route) but not a derivation; carrying the
   record's own matched-asymptotics machinery (the `V15$–$V17`-style
   inner-layer bookkeeping) to a rigorous 5th order was not attempted.
4. **Non-perturbative (trans-series) content is entirely untested here**,
   exactly the same structural blind spot every ancestor front in this
   sub-lineage has disclosed (`\Phi(0,\cdot)`'s order-2-entire growth
   class, `plateau_resummation_attempt` §2.3/§4.5).
5. **The tested `(c,u)` grid is finite**: `c\in\{1000,...,64000\}`
   (`8\times` in `eps`), `u\in\{0,1,2,4\}`. No claim is made that the
   boundary layer behaves uniformly for arbitrarily large `u` at fixed
   `eps`, or for `eps` far smaller than tested here — only that no
   failure was found anywhere searched.
6. **This front's own "degenerate boundary layer" structural finding
   (§3.3) is itself conditional**, not a proof — it shows the CANDIDATE
   inner content reduces to the outer series' Taylor re-expansion GIVEN
   uniform outer validity, which is precisely what remains unestablished.

**No formula of record is proposed as a replacement for anything.**
`phi_REDB`, `Phi_U(c)`, `Phi_infinity(c)` are all untouched and
unaffected.

---

## 9. Scorecard

| item | status | evidence |
|---|---|---|
| `(U2)` proved | **NO** — open | §6 |
| Precise target confirmed as classical boundary-layer statement | YES | §1 |
| Outer expansion for `F(x)` cited (not re-derived) | YES | §2.1, record |
| `psi_n(x)=gamma_n R^{(n-1)}(x)` generalized to all `x`, `n\le4` | **PROVED** (symbolic, conditional on record's own heuristic status of `\psi_n` itself) | §2.1, `u01` |
| `(W-F)` relation, `W_inf=F-eps F'` | **derived** (new, algebraic from cited hypotheses) | §2.2 |
| `chi_n(x)`, `W_inf`'s own outer expansion, `n\le4` | **derived and proved** (symbolic) | §2.2, `u01` |
| Self-consistency: re-derive published 4-term law via `W_inf` route | **MATCHES EXACTLY**, symbolically | §2.3, `u01` |
| `(W-F-C)` exact algebraic identity | **derived** (new) | §3.2 |
| Boundary-layer/inner analysis at `x=eps u` | **attempted; degenerate-boundary-layer finding, conditional** | §3.3 |
| Matching condition | **automatic by construction, given the conditional finding above** | §3.3 |
| Fresh `(P,Q)`-family implementation | **built, 7/7 anchors PASS** | §4 |
| Hypothesis (ii) (`\lim\Psi=\lim\Phi`) numerically confirmed | YES, `\sim10^{-33}$–$10^{-34}` at every grid point | §5.2 |
| `resid5` bounded/converging at `x=eps u`, `u=0,1,2,4` | YES, all 4 tested `u`, all 4 tested `c` | §5.3 |
| Order-4 sanity check (known `gamma_4`) | **PASSES**, `O(eps)` rate confirmed uniformly | §5.4 |
| Order-5 vs. conjectured `gamma_5=209/24` | consistent to `0.02\%$–$0.6\%` (SPECULATIVE) | §5.5 |
| Rigorous `x`-uniform remainder bound (`(U2)`'s literal content) | **NOT achieved** — same obstruction as `(U1)`'s 7 prior waves | §3.3, §6 |

---

## 10. Files

| file | role |
|---|---|
| `u01_symbolic_outer_expansion.py`/`.log` | symbolic (sympy) proof: `psi_n(x)=gamma_n R^{(n-1)}(x)` general `x`, `n\le4`; `chi_n(x)` derivation; self-consistency re-derivation of the 4-term law (§2) |
| `u02_family_series.py` | fresh general-`s` `(P,Q)`-family recursion, `a_k,b_k`, `fam_deriv`, descending-recursion `b`-ODE solve (§4.1) |
| `u03_validate_anchors.py`/`.log` | 7/7 validation against published anchors incl. `c=1000` plateau to `\sim34` digits (§4.2) |
| `u04_probe_convergence_c1000.py`/`.log` | empirical `(K,\text{dps})` sizing probe at `c=1000` (§7, S3) |
| `u05_probe_convergence_ladder.py`/`.log` | confirms `K=400,\text{dps}=250` suffices across the whole `c` ladder |
| `u06_boundary_layer_experiment.py`/`.log`, `u06_results.pkl` | THE main experiment: `W_inf` at `x=eps\,u` and bridge `x=1`, all 20 grid points (§5.1–§5.3) |
| `u07_richardson_extrapolate.py`/`.log` | Richardson extrapolation of `resid5`, speculative `\gamma_5` comparison (§5.5) |
| `u08_order4_sanity_check.py`/`.log` | known-order (`n=4`) sanity check before trusting order-5 (§5.4) |
| `ATTEMPT.md` | this document |

No git commit made. Nothing outside this
`.../mclust_h1_validity_attempt/h1_u2_boundary_layer_attempt/`
subdirectory was written to — every ancestor `ATTEMPT.md`/`adversarial/`
file and `PROOF_DEPENDENCY_MAP.md`/`THEOREM.md`/`DECISION_LEDGER.yaml`/
`TEST_QUEUE.yaml`/`DISCOVERY_LAB_STATE.md` further up the tree were
read-only references (§0), never modified. No `adversarial/` subdirectory
created; no referee dispatched by this front itself, per the mandate.

---

## Seeds

Reserved range: `20260939000-20260939999`.

**Before use**: `grep -rn "20260939" 05_DISCOVERY_LAB/` matched only
`DECISION_LEDGER.yaml`'s own `DISC-DEC-127` reservation line — zero other
occurrences.

**No randomness was needed anywhere in this front** — every result is
exact symbolic reasoning (`sympy`) or deterministic arbitrary-precision
series summation (`mpmath`); no `numpy.random`/`SeedSequence` call
appears in any script in this directory.

**After use** (re-confirmed at the end of this front, before writing this
final section):

```
$ grep -rn "20260939" 05_DISCOVERY_LAB/
05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml:8325:      20260939000-20260939999.
```

Still exactly one match — the ledger's own reservation line — confirming
the reserved range was never consumed, exactly as anticipated by the
mandate ("You will very likely need no randomness").
