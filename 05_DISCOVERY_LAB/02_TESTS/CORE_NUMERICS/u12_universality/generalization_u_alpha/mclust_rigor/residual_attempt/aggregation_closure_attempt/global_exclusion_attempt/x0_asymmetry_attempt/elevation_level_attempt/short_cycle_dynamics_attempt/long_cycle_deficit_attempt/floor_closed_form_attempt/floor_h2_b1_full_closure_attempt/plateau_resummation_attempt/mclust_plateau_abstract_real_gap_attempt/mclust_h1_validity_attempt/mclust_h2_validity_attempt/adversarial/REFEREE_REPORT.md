# REFEREE REPORT — `mclust_h2_validity_attempt` (`MCLUST-H2-VALIDITY-ATTEMPT`, `DISC-DEC-093`)

**Referee:** independent hostile review, dedicated session. No `.py` file from
`mclust_h2_validity_attempt` or any ancestor front in the `mclust_rigor`
lineage was opened, read, or imported at any point. Every check below was
built fresh from the mathematical prose of `ATTEMPT.md` and the required
reading (`PROOF_DEPENDENCY_MAP.md` §2 Tree B, `mclust_h1_validity_attempt/
ATTEMPT.md`, `plateau_resummation_attempt/ATTEMPT.md`), all read in full.

**Scope reminder.** This is pure combinatorial/asymptotic analysis about the
`M-CLUST(b)` plateau line (Tree B, node `PLATRESUM`) — a standalone
mathematical object internal to this archive. It is **not** a claim about
any Millennium Prize Problem. No such claim was found anywhere in the
target document, and none appears in this report.

---

## VERDICT

**SOUND WITH NAMED ISSUES — ACCEPT for catalogue, at exactly the tier
claimed** ("a reduction of `H2` to a corollary of `H1`'s own open content,
not an unconditional proof").

Every mathematical claim independently checked in this review holds up.
No arithmetic, algebraic, or logical error was found anywhere in the
document's central chain of reasoning (the Growth-Exclusion Lemma, the
moment-integral normalization, the general-`n` telescoping identity, the
`phi_n` formula, or the numerical table). The document's own honesty
sections (§4, §7, §8) accurately state what is and is not established, and
correctly identify that the whole reduction bottoms out in `H1`'s own open
`(U1)+(U2)` Watson-bookkeeping content — it does not overclaim `H2` as
closed anywhere. One additional, previously unnamed hypothesis is
identified below (Issue R1) that the induction (§3.3) implicitly needs but
does not explicitly flag as distinct from the "ordinary smoothness"
caveat it does name; this is a documentation-completeness gap, not a
mathematical error, and does not change the front's own honest verdict of
non-closure.

---

## What was independently re-verified, and how

### 1. The Growth-Exclusion Lemma (§2) — `adv01_growth_exclusion.py`

- **Homogeneous solution.** Verified symbolically (`sympy`, exact) that
  `e^{x^2/2+xy}` solves `u_x = (x+y)u`. PASS.
- **Leibniz-rule particular solution.** Re-derived the Leibniz-rule step
  independently on a concrete `f(t)=t` (full symbolic integral,
  differentiated directly — not just asserted) and then on an abstract
  `f`, confirming `u_p = -e^{x^2/2+xy}\int_x^\infty e^{-(t^2/2+ty)}f(t)dt`
  solves `u_p_x - (x+y)u_p = f(x)` exactly, given only the single Leibniz
  fact `dI/dx = -e^{-(x^2/2+xy)}f(x)`. PASS.
- **Uniqueness / growth divergence.** Verified symbolically, for general
  symbolic `y\ge0` (not just numeric spot values), that
  `\lim_{x\to\infty}e^{x^2/2+xy} = +\infty`. PASS.
- **`y=0,f=-1` special case.** Verified this reduces EXACTLY (symbolic
  zero difference) to `R(x) = \sqrt{\pi/2}\,\mathrm{erfcx}(x/\sqrt2)`, the
  record's own closed form for `psi1`. This confirms the lemma's claimed
  consistency with the record's own §1.1 remark (independently confirmed
  present at line 180 of `plateau_resummation_attempt/ATTEMPT.md`: "The
  polynomial ansatz automatically discards the `e^{c s^2/2}` homogeneous
  branch") is not a fabricated citation — genuinely present, and the
  `x=s\sqrt c` scaling reduction is exact. PASS.
- **Numerical illustration, independently reconstructed.** A DIFFERENT
  `x`-grid (`0,5,9,11,13,14,16` vs. the front's `0,8,10,12,15`) and a
  DIFFERENT admixture size (`1e-25` vs. the front's `1e-30`) both confirm
  the same qualitative blow-up (relative contamination growing from
  `~1e-26` at `x=0` to `~1e31` at `x=16`). PASS — the qualitative claim is
  not an artifact of the front's specific choice of grid/admixture size.
- **Genuinely separate from `H1`'s own Watson-concentration lemma?**
  Confirmed. `H1`'s lemma (`mclust_h1_validity_attempt` §2.1) is a
  real-analysis convergence statement about the exact renewal integral
  `(E2)` — it shows `\lim_{y\to\infty}\Phi(x_0,y)` exists and equals a
  specific convolution, under a local-uniformity hypothesis `(U1)` on `W`.
  The target's Growth-Exclusion Lemma is an entirely different kind of
  fact — an elementary linear-ODE existence/uniqueness result via
  variation of parameters, with no dependence on any `g\to\infty` limit or
  on `(U1)`. These do not overlap or repackage one another; the target's
  own §0 characterization of this distinction is accurate.

### 2. The moment-integral normalization (§3.1, S2 crux) — `adv02_moment_integral.py`

Independently re-derived, via the standard `v=\epsilon u` substitution and
the Gamma-function moment formula (not copied from the target), that
`\int_0^\infty e^{-v/\epsilon}v^m\,dv = \epsilon^{m+1}\,m!` for general
symbolic `m`, hence
`(1/\epsilon)\int_0^\infty e^{-v/\epsilon}\,v^m/m!\,dv = \epsilon^m` exactly,
with **no leftover `1/m!`**. Verified both by direct exact symbolic
integration at `m=0..8` and by the general-`m` Gamma-function argument.
This is exactly the crux the front says it self-caught (S2): an early
draft carried a spurious extra `1/m!` by forgetting the moment integral's
own `m!` exactly cancels the Taylor `1/m!`. **PASS — S2's disclosed
near-miss and its resolution are both confirmed correct**, independently.

### 3. The general telescoping identity (§3.2) — `adv03_telescoping_identity.py`

**By-hand re-derivation (independent of the document, done from the
prose recursion only).** Given `omega_k := \psi_k - \psi_{k-1}'` and
`\phi_n := \sum_{m=0}^{n-1}(d/dx-d/dy)^m[\omega_{n-m}]`, with
`\psi_1,\dots,\psi_{n-1}` known `y`-independent:

- For `m\ge1`, `\omega_{n-m}` (index `\le n-1`) is `y`-independent, so
  `(d/dx-d/dy)^m` collapses to the pure `d^m/dx^m` term (every binomial
  term containing `d/dy` annihilates a `y`-independent function). This
  gives `\phi_n = \omega_n(x,y) + \sum_{m=1}^{n-1}\omega_{n-m}^{(m)}(x)`.
- Substituting `\omega_j = \psi_j - \psi_{j-1}'` and re-indexing
  `j=n-m` in the remaining sum: `\sum_{j=1}^{n-1}\psi_j^{(n-j)} -
  \sum_{j=1}^{n-1}\psi_{j-1}^{(n-j+1)}`. Re-indexing the second sum by
  `i=j-1` (dropping the `i=0` term since `\psi_0=0`) gives
  `\sum_{i=1}^{n-2}\psi_i^{(n-i)}`, which cancels term-by-term against all
  but the last (`j=n-1`) term of the first sum, leaving exactly
  `\psi_{n-1}'(x)`.
- Hence `\phi_n = [\psi_n(x,y)-\psi_{n-1}'(x)] + \psi_{n-1}'(x) =
  \psi_n(x,y)` exactly, so `f_n=\psi_n-\phi_n=0`.

This by-hand re-derivation reproduces the document's §3.2 proof
**exactly**, step for step, with no gap found — the re-indexing and
cancellation argument is airtight for arbitrary `n\ge2` (and trivially
`n=1`, where the sum is empty and `\phi_1=\omega_1=\psi_1`).

**Independent symbolic verification, own script.** Built entirely fresh
(own variable names, own loop/binomial-expansion structure, representing
`\psi_1,\dots,\psi_{n-1}` as genuinely `y`-independent `Function(x)`
objects and `\psi_n` as a bivariate `Function(x,y)`) — checked
`f_n \equiv 0` at **`n=2,3,4,5,6,7`** (the task specifically asked for
`n=4,5`, extended here through `n=7`), all PASS. Full intermediate
`\omega_k` and `\phi_n` builds printed and audited for `n=4,5`. This
matches, but does not merely repeat, the orchestrating session's own
`n=2,3` spot-check and the front's own `n=2..9` claim; the independent
construction here reaches `n=7` cleanly and would extend further with no
qualitative change.

### 4. The `phi_n` formula and Watson-operator generalization (§3.1) — `adv04_phin_formula_derivation.py`

Re-derived, from the stated inputs `\Phi\sim\sum_m \epsilon^m(d/dx-d/dy)^m
W` and `W=\Psi-\epsilon\Psi_x` combined with `\Psi=\sum_n\epsilon^n\psi_n`,
that the `\epsilon^n` coefficient of `W` is exactly `\omega_n=\psi_n-
\psi_{n-1}'` (with `\omega_0=0` since `\psi_0:=\psi_{-1}:=0`), and that the
`\epsilon^n` coefficient of the double sum `\sum_m\epsilon^m(d/dx-d/dy)^m
W` is exactly `\sum_{m=0}^{n-1}(d/dx-d/dy)^m[\omega_{n-m}]` (the `m=n` term
vanishes since `\omega_0=0`), matching the document's formula exactly, at
`n=1..6`, with `\psi_k` left as fully general bivariate functions (not
assumed `y`-independent — this checks the operator algebra itself,
independent of any inductive hypothesis).

**Self-caught issue in this referee's own script, disclosed for
transparency.** An initial version of this extraction (using SymPy's
`.coeff(eps, k)` on an un-expanded `Mul(const, Add(...))` expression
produced by the binomial-expansion helper) silently returned WRONG,
`eps`-contaminated results at `n\ge3` — a `sympy` API pitfall (`.coeff()`
requires the expression pre-expanded to bucket correctly by power), not a
flaw in the target's mathematics. Caught by inspecting the raw output
(residual `eps^1..eps^6` terms in an expression that should have been
`eps`-free), diagnosed via an isolated minimal reproduction, and fixed by
adding `sp.expand()` before every `.coeff()` call; a permanent self-test
assertion was added to the script confirming the fix. After the fix, all
`n=1..6` cases match exactly. This mirrors — appropriately, given this
review's own adversarial mandate — the disclosure discipline the target
document itself uses for its self-caught S1/S2/S3 issues.

### 5. Numerical work (§5) — `adv05_numerics.py`

- **`R(x)\le1/x` bound.** Independently re-derived from scratch (`t/x\ge1`
  for `t\ge x>0` implies `e^{-t^2/2}\le(t/x)e^{-t^2/2}`; integrate and use
  `\int_x^\infty t e^{-t^2/2}dt=e^{-x^2/2}` exactly). Verified numerically
  at 11 test points including the two physical-edge values
  `x=\sqrt{1000}=31.62` and `x=\sqrt{8000}=89.44`, using `mpmath`'s
  built-in `erfc` (a DIFFERENT numerical route than the front's own
  quadrature-plus-substitution fix for S1) — all PASS, `R(x)\le1/x` holds
  throughout with no violation.
- **Physical-edge spot check.** Independently implemented `R` (via
  `mpmath.erfc`, not quadrature), `R',R'',R'''` (via the elementary
  derivative-closure recursion, re-derived directly from `R'=xR-1`), and
  `psi3` via the Growth-Exclusion Lemma's own bounded-branch formula
  applied to `f(t)=7R'(t)`, using the numerically-safe substituted
  integral `t=x+u` (independently re-derived, mirroring the fix the front
  names for its own self-caught S1 pitfall, not copied from it).
  `psi4=(17/3)R'''`. Sanity-checked all four at `x=0` against the record's
  own closed forms (agreement to `\ge30` digits). Then spot-checked at
  `x=\sqrt c` for **`c=1000,4000,8000`** (3 of the front's 6 tested
  values, as requested): **all 12 values (3 `c`-values × 4 profiles)
  matched ATTEMPT.md's §5.2 table to within the precision the front
  itself printed** (relative differences `1e-6` to `1e-9`, consistent
  with the fewer significant digits printed in the table). Monotone
  decrease in magnitude across the 3 tested `c`-values confirmed for all
  four profiles, independently. PASS.

### 6. Honesty check (§4, §7, §8)

Read against the actual content of §2/§3: the document's own framing is
accurate. It correctly states that (a) the Growth-Exclusion Lemma is
unconditional and general; (b) the telescoping identity is a purely
algebraic fact about the Watson-operator bookkeeping, but that bookkeeping
itself is exactly `H1`'s own named open content (`(U1)+(U2)` of
`mclust_h1_validity_attempt`); (c) `H2` is therefore reduced to a
corollary of `H1`, not proved unconditionally; (d) ordinary smoothness
(`\Psi_{xy}=\Psi_{yx}`) is a named, unverified standing assumption; and
(e) no counterexample search was performed. All of this checks out against
the actual mathematical content — no overclaiming was found. Cross-checked
against `PROOF_DEPENDENCY_MAP.md`'s own wave-20/21 addenda (`DISC-DEC-088/
091/093` context) — no unresolved contradiction with the ledger's own
characterization of `H1` as open and `H2` as (this front's finding)
reduced-not-closed.

### 7. Millennium Prize Problem claim check

None found anywhere in `ATTEMPT.md`. The document explicitly and
repeatedly disclaims any such association (opening paragraph, §0). This
review makes no such claim either.

---

## Named issues

### Issue R1 — implicit boundedness hypothesis on `chi_n` in the induction step (§3.3)

**Severity: MINOR / documentation-completeness (not a mathematical
error).**

The induction (§3.3) concludes `chi_n := \partial_y\psi_n \equiv 0` by
invoking "the Growth-Exclusion Lemma's HOMOGENEOUS case (§2, `f=0`: the
unique bounded solution of `u_x=(x+y)u` is `u=0`)". But the lemma's
uniqueness argument only forces the constant `C(y)` to `0` for the
*specific solution instance under examination*, given that instance is
already known to be **bounded as `x\to\infty`**. The document does not
explicitly state, as a separately named hypothesis, that `chi_n`
itself — as opposed to `psi_n` — is a priori known to be bounded as
`x\to\infty` before the lemma can be invoked to conclude `chi_n=0` rather
than merely `chi_n\in\{0,\ \text{unbounded}\}`.

This is very plausibly already covered by the document's own broader
disclosure that the whole induction depends on the same order-by-order
Watson/Taylor bookkeeping validity that is `H1`'s own open content
(§4, item 3) — if `\psi_n(x,y)` is only well-defined at all via a
bookkeeping scheme in which every order's field (and its `y`-derivatives)
inherits the same boundedness class, this extra hypothesis is subsumed
rather than independent. It is, however, logically distinct from the
"ordinary smoothness" caveat the document DOES name explicitly (§4 item 2,
`\Psi_{xy}=\Psi_{yx}` mixed-partial commutativity) — boundedness-of-a-
parameter-derivative is not implied by mixed-partial commutativity alone.
Recommended fix (editorial, not mathematical): a one-sentence addition to
§3.1 or §3.3 naming "`chi_n` inherits the same bounded-as-`x\to\infty`
selection as `\psi_n` itself" as an explicit, separately-flagged standing
assumption, alongside the existing smoothness caveat.

**Impact on verdict: none.** This does not identify an error in any
computation, formula, or numerical claim, and does not change the
document's own (already conservative) non-closure verdict — if anything
it very slightly sharpens, rather than weakens, the honest accounting
already given in §4/§8.

No other issues — mathematical, numerical, or rhetorical — were found.

---

## Files produced by this review

All in this directory (`adversarial/`):

| file | role |
|---|---|
| `adv01_growth_exclusion.py`/`.log` | independent re-derivation of the Growth-Exclusion Lemma (homogeneous solution, Leibniz particular solution for concrete and abstract `f`, uniqueness/growth-divergence, `y=0,f=-1` reduction to `R(x)`, independent numerical blow-up illustration) |
| `adv02_moment_integral.py`/`.log` | independent re-derivation of the moment-integral normalization (S2 crux): `(1/eps)\int_0^\infty e^{-v/eps}v^m/m!\,dv=eps^m` exactly, `m=0..8` symbolic + general-`m` Gamma-function argument |
| `adv03_telescoping_identity.py`/`.log` | independent by-hand re-derivation (in this report) plus fresh symbolic script verifying `f_n=0` at `n=2..7` |
| `adv04_phin_formula_derivation.py`/`.log` | independent re-derivation of the `phi_n` formula from the stated Watson-operator/`(KEY)` inputs, `n=1..6`; includes disclosure of a self-caught script bug (SymPy `.coeff()` extraction pitfall), fixed and self-tested |
| `adv05_numerics.py`/`.log` | independent proof and numerical check of `R(x)\le1/x`; independent implementation and physical-edge spot check of `psi1..psi4` at `c=1000,4000,8000` against ATTEMPT.md §5.2's table |
| `REFEREE_REPORT.md` | this document |

No governance file (`PROOF_DEPENDENCY_MAP.md`, `THEOREM.md`,
`DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`) was
opened for writing. No file outside this `adversarial/` subdirectory was
modified. No git command was run.
