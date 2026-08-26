# Hostile referee report — `JOINT-EXPLORATION-CONTINUUM-ATTEMPT`

> Target: `.../joint_exploration_continuum_attempt/ATTEMPT.md`.
> Method: read `THEOREM.md` Definitions 1–4 (§2, §7.2), Proposition 4's
> full proof (§7.3), Estágio 24 (`f_{M_K}`/`E[M_K^2]=1/(K+1)`, all `K`),
> and Estágio 25 (Theorem J and its Corollary, PROVED exactly at every
> finite `n,K`), plus `.../joint_two_point_attempt/ATTEMPT.md` §1–§3
> (prose, Theorem J's finite-model proof). **No `.py` script from this
> front, the parent `joint_two_point_attempt/` front (including its
> `adversarial/`), or any other prior front was opened, per mandate.**
> Every closed form and every numeric claim below was re-derived by
> hand from the target document's *prose* first, then cross-checked
> against a from-scratch exhaustive brute-force enumeration of
> `THEOREM.md`'s Definition 4, written independently in this
> `adversarial/` directory. Seeds: none needed — every check in this
> report is exact/deterministic (no Monte Carlo was run; the reserved
> range `20260875000+` was not touched).

## Verdict

> **SOUND WITH NAMED ISSUES — ACCEPT for catalogue**, at the tier
> actually claimed: **Proposition R (PROVED)**; **the `K=0,1` closed
> forms and their `n→∞` transfer (PROVED)**; **`K≥2` honest
> non-closure (correctly diagnosed, if anything mildly conservative)**.
> One genuine, precisely-locatable **mathematical error** was found —
> confined to the *explanatory/causal narrative* of §3.3 (not to any
> closed form, theorem statement, or numeric result) — and one
> **framing note** on what "PROVED... by transfer" is actually resting
> on is recorded for full transparency. Neither downgrades any of the
> document's PROVED-labeled results; both are named precisely below,
> per the archive's disclosure convention.

---

## 1. What was independently rebuilt

`bruteforce_definition4.py` (this directory) enumerates, exhaustively
and exactly (`fractions.Fraction`, arbitrary-precision Python ints, no
floating point anywhere), **every** `(π, R, {U_i})` triple of
`THEOREM.md`'s Definition 4, for a grid of `(n,K)` pairs, using a
linear-time functional-graph decomposition (own implementation, not
adapted from any existing script) to determine, for each configuration,
whether points `0,1` are cyclic and — if so — whether they land in the
*same* directed cycle of `f`. All `n!·C(n,K)·n^K` configurations are
enumerated with equal weight, which is exactly Definition 4's law
(`π` uniform, `R` a uniform `K`-subset, `U_i` i.i.d. uniform,
mutually independent). Total wall time for the full run: 21.2s.

`rate_decomposition_check.py` and `k2_fit_extrapolation_check.py`
perform exact symbolic algebra (`sympy`, exact rationals) on closed
forms — no enumeration, no randomness.

All three scripts' full output is captured in matching `.log` files in
this directory; `bruteforce_definition4_results.json` holds the raw
numeric results.

---

## 2. Proposition R (the reduction)

**Re-derived by hand, independently of the document's proof.** The
claim is: if `P_n^{(K)}(both)→τ_K`, then `P_n^{(K)}(same)→τ_K/2`,
because `P_n^{(K)}(same) = ½P_n^{(K)}(both)` holds as an **exact**
identity at every finite `n,K` (Theorem J's Corollary, cited from
Estágio 25, itself PROVED there and independently re-verified by a
hostile referee per that stage's log — I re-read that referee's
verdict directly in `THEOREM.md`, not merely the front's own claim).

**Subtlety check requested by the mandate.** Does "both cyclic" or
"Theorem J's Corollary" break down at `K=0` or small `n`? Working
through it: Theorem J conditions on `C(f)=c` with `|c|=m≥2`; the
Corollary's proof conditions on `C(f)=c` for `c∋i,j`. Since `i≠j` and
both are required to be in `c`, `|c|≥2` is **automatic** whenever the
conditioning event is non-empty — there is no edge case where the
`|c|≥2` restriction excludes part of the "both cyclic" event. At `K=0`,
`f=π` and `C(π)=[n]` always (every point of a permutation is cyclic),
so the Corollary degenerates to the classical `P(i,j\text{ same
cycle})=1/2` fact for a uniform permutation of `[n]`, `n≥2` — no
special-casing needed. I also checked that the identity is stated and
used **unconditionally** (`P(\text{same},\text{both})=\tfrac12
P(\text{both})`, not `P(\text{same}\mid\text{both})=\tfrac12`), so it
holds trivially even in a hypothetical `P(\text{both})=0` case (both
sides are `0`) — no division-by-zero risk anywhere in the proof chain.

**Own brute-force confirmation.** `bruteforce_definition4.py` §1 and §4
independently re-verify `P_n^{(K)}(same)=P_n^{(K)}(diff)=\tfrac12
P_n^{(K)}(both)` **exactly** at `K=0` (`n=2..5`), `K=1` (`n=2..7`),
`K=2` (`n=3..7`), and `K=3` (`n=4..6`) — 20/20 exact matches, using a
cycle-membership check built entirely independently of the target
document's or parent front's code.

**Conclusion: Proposition R is correctly stated and correctly proved.**
It is genuinely as simple as the document says — dividing an exact
algebraic identity by 2 and taking a limit — with no hidden edge case.

---

## 3. The `K=1` closed form — from-scratch re-derivation

I re-derived the entire case analysis independently before reading the
document's algebra as anything more than a target to check against
(the mandate's "primary verification tool" instruction was followed:
brute force first, then compare).

**Setup, re-derived.** `R={r}`, `r` uniform on `[n]`. Two cases:
`r∉{0,1}` (prob. `(n-2)/n`) and `r∈\{0,1\}` (prob. `2/n`).

**Case (a), `r∉\{0,1\}`.** Let `L=ℓ` be the length of `π`'s cycle
containing `r` (classical fact, `L~Unif\{1,\dots,n\}`, re-derived from
Proposition 4 Step 1's argument, which does not depend on which point
is fixed). Labeling the cycle `c_0=r,c_1,\dots,c_{ℓ-1}` in forward
`π`-order, I re-derived Proposition 4 Step 3's case split into a
**per-point rule**: `c_0` cyclic `⟺ U∈C` (prob. `ℓ/n`); `c_k` cyclic
(`k≥1`) `⟺ U∈\{c_1,\dots,c_k\}` (prob. `k/n`) — confirmed this gives a
**nested** family of events, so for two points at offsets `j,k≥1`,
"both cyclic" `⟺` the *nearer* one is cyclic, probability
`\min(j,k)/n`. I independently confirmed the standard fact
`E[\min(j,k)]=(m+1)/3` for two distinct uniform draws without
replacement from `\{1,\dots,m\}` (checked at `m=2,3` by hand), giving
conditional-both-cyclic probability `ℓ/(3n)` given both offsets are in
`C`. For "exactly one in `C\{r\}`" (hypergeometric, re-derived: `P=
2(ℓ-1)(n-ℓ)/[(n-1)(n-2)]`), the in-`C` point at offset
`d\sim\text{Unif}\{1,\dots,ℓ-1\}` (`E[d]=ℓ/2`) gives conditional value
`ℓ/(2n)`; "neither in `C`" gives `1` (untouched points always cyclic,
Prop. 4 Step 2's argument). Assembling and averaging over
`L\sim\text{Unif}\{1,\dots,n\}` reproduces exactly
`V_a(n)=(3n+1)/(6n)`.

**Case (b)/(c), `r=0` (or symmetrically `r=1`).** Same per-point rule
applied starting at the reroute source itself; if the other query point
is outside `r`'s cycle, `r` itself is cyclic iff `U∈C` (prob. `ℓ/n`);
if it's inside at offset `d`, both cyclic iff that offset point is
cyclic (prob. `d/n`, and this *implies* `r` is cyclic too, by the
nesting property). Averaging reproduces `V_b(n)=(n+1)/(3n)`.

**Reassembly:** `(n-2)/n·V_a(n) + 2/n·V_b(n) = (3n^2-n+2)/(6n^2)`.

**My hand-derivation independently arrives at exactly the same formulas
the document reports** — this is a genuine from-scratch reproduction,
not merely an algebra check.

### Brute-force cross-checks (all exact, all pass)

| Check | Result |
|---|---|
| `V_a(n)` vs. brute (R fixed at a 3rd point), `n=3..6` | **4/4 exact matches** |
| `V_b(n)` vs. brute (R fixed at `r=0`), `n=3..6` | **4/4 exact matches** |
| `V_b(n)` symmetric check (R fixed at `r=1`), `n=3..6` | **4/4 exact matches** |
| Full closed form `(3n²-n+2)/(6n²)` vs. brute (R averaged), `n=2..7` | **6/6 exact matches** |
| My independent reassembly `(n-2)/n·V_a+2/n·V_b` vs. document's closed form | **algebraically identical**, all `n` |

**False-start reproduction (mandate step 4's explicit sanity check).**
`V_a(3) = 5/9`, confirmed exactly (both by the closed form and by
brute force with `R` fixed at a third point). This *is* the disclosed
false-start value. The true, correctly-assembled value at `n=3` is
`13/27`, confirmed exactly by full brute force (`R` averaged over all
3 choices) — `5/9 ≠ 13/27`. **The document's self-disclosure is
accurate**: the false start really is wrong, by exactly the amount
and for exactly the reason claimed (an entirely omitted `O(1/n)`-weight
case, not an arithmetic slip).

**Verdict: Proposition K1 (the `K=1` closed form) is correct, and its
derivation is sound.** This is the strongest, best-supported claim in
the document.

---

## 4. Rate claim `n(P_n^{(1)}(\text{both})-\tfrac12)\to-\tfrac16`

Trivial algebra, checked symbolically: `(3n^2-n+2)/(6n^2) = \tfrac12 -
\tfrac1{6n}+\tfrac1{3n^2}`, so `n(P-\tfrac12) = -\tfrac16+\tfrac1{3n}
\to-\tfrac16`. Confirmed exactly at `n=10,100,1000,10^6` in
`bruteforce_definition4.py` §5. **Correct, not botched.**

---

## 5. A genuine error, precisely located: the §3.3 causal narrative

The document's §3.3 attributes the entire `Θ(1/n)` rate (as opposed to
the marginal bridge's `Θ(1/n²)`) to Case (b)/(c) alone, stating:

> "...shifts the conditional value from `V_a(n)→1/2` to `V_b(n)→1/3`
> — an `O(1)` jump — which is exactly enough to produce an `O(1/n)`
> contribution to the overall average... **dominating whatever
> `O(1/n²)` behavior Case (a) alone would have shown**."

**This specific claim is false**, and directly contradicted by the
document's *own* formula for `V_a(n)`. I checked it two ways:

1. **Directly:** `V_a(n) = (3n+1)/(6n) = \tfrac12 + \tfrac1{6n}` —
   `V_a(n)` itself has an *explicit, exact* `Θ(1/n)` deviation from
   `1/2` (coefficient `1/6`), not `Θ(1/n²)`.
2. **Via the weighted decomposition** (`rate_decomposition_check.py`):
   `(n-2)/n·V_a(n) = \tfrac12 - \tfrac5{6n} - \tfrac1{3n^2}` — Case
   (a)'s own *weighted contribution* to the final average has an
   `O(1/n)` coefficient of `-5/6`, and Case (b)/(c)'s weighted
   contribution `2/n·V_b(n) = \tfrac1{2n}\cdot\dots` has coefficient
   `+2/3`. The two `O(1/n)` terms **partially cancel**
   (`-5/6+2/3=-1/6`) to give the document's correctly-reported overall
   `-1/6` — they do not compose as "an `O(1/n²)` baseline plus an
   `O(1/n)` perturbation." Both cases individually contribute at
   `O(1/n)`; neither is negligible.

**Why this matters, and why it doesn't.** It matters because it is a
concrete, checkable, *false* quantitative claim in the document's own
explanatory prose — the kind of error the archive's disclosure culture
exists to catch. It doesn't undermine any PROVED result: Proposition
K1's closed form, the reassembly, and the `-1/6` rate value are all
independently confirmed correct (§3–4 above); only the *mechanistic
explanation* of "why" the rate is `Θ(1/n)` and not `Θ(1/n²)` is wrong.
The likely correct diagnosis (not claimed as proved here, offered only
as an observation): the slower rate is a joint-two-point positional
effect present *already within Case (a)* (via the `E[\min(j,k)]/n`
term, which has no analogue in the one-point marginal problem, where
there is no second point to be positioned relative to the first) — not
something attributable to the reroute-source–query-point collision
alone. If anything, this makes the document's closing conjecture ("a
general-`K` second-moment bridge should be expected to converge at
`Θ(1/n)`, not faster, for every `K`") *more* robust than its own
argument shows, since an `O(1/n)` source of error is present even
without any query-point collision — but the document should not claim
this without further work, and neither do I.

**This is disclosed here as a real error requiring correction if this
document is catalogued** — a one-sentence fix to §3.3 replacing the
"Case (a) alone would show `O(1/n²)`" claim with the correct
decomposition would resolve it without touching any other claim.

---

## 6. `K=2, K=3` spot-checks against the document's own table

Per mandate step 7 ("at least one"), I checked **all five** `K=2`
table entries (`n=3..7`) and **all three** `K=3` table entries
(`n=4..6`) by independent brute force — `8/8 exact matches`, including
the specifically-requested `n=6,K=2: 44/135`:

| `n` | `K` | Document | Brute force | Match |
|---|---|---|---|---|
| 3 | 2 | `10/27` | `10/27` | ✓ |
| 4 | 2 | `49/144` | `49/144` | ✓ |
| 5 | 2 | `33/100` | `33/100` | ✓ |
| 6 | 2 | `44/135` | `44/135` | ✓ |
| 7 | 2 | `143/441` | `143/441` | ✓ |
| 4 | 3 | `19/64` | `19/64` | ✓ |
| 5 | 3 | `3383/12500` | `3383/12500` | ✓ |
| 6 | 3 | `233/900` | `233/900` | ✓ |

Theorem J's Corollary (`P(same)=P(diff)=P(both)/2` exactly) was
re-confirmed at every one of these `(n,K)` pairs as a byproduct.

**Assessment of §4's "why `K≥2` isn't closed" diagnosis.** I stress-
tested this by attempting to *find* the true `K=2` closed form myself
via rational-function extrapolation (`k2_fit_extrapolation_check.py`):
a 3-parameter ansatz fit from 3 points fails to predict `n=6,7` (as
the document reports), and — going one step further than the document
did — a *richer* 4-parameter fit using 4 exact points **also** fails
to predict the 5th. This corroborates, and if anything strengthens,
§4's claim that the true `K=2` joint closed form needs materially more
structure than a small polynomial-in-`1/n` ansatz recovers from a
handful of data points. Comparing against `THEOREM.md`'s own account
of what the *marginal* `K=2` bridge required (Estágio 3: a genuine
dedicated front, three cases on whether the reroute source lands on
the reference point's own cycle, `ψ_n^{(2)}` needing terms through
`1/n³`) — the joint two-point quantity studied here needs to track
*all of that* plus the *relative position* of a second query point,
so §4's comparison ("the same order of combinatorial complexity...
applies here too, now to a joint quantity") is accurate, and if
anything conservative rather than an overstatement.

**Verdict: §4's diagnosis is honest and not overstated.**

---

## 7. §5's honesty, and the "transfer, not construction" claim

**No overclaiming of the Estágio 18/25 obstruction found.** §5's
bullets correctly state that (a) no two-point-capable extension of
Definition 3 is supplied, (b) nothing about the physical/geometric
structure of the split is established, (c) the general-`K` bridge is
new and not a renamed obstruction, and (d) `τ_K=1/(K+1)` is unproved
for `K≥2`. All four checked against the document's actual content and
found accurate.

**On whether "transfer, not construction" secretly smuggles in
destination information.** I looked hard for this, since it's the
kind of subtle circularity the mandate specifically flagged as a risk.
Working through the logical chain: (i) the continuum target `E[M_1^2]
=1/2` comes from Estágio 24's density formula `f_{M_K}(x)`, an
**entirely separate** derivation (general-`K` Conjecture 1, no
two-point construction anywhere in it); (ii) the finite-model value
`τ_1=1/2` comes from Proposition K1, a **purely combinatorial**
computation on Definition 4 that never touches Definition 3's
`(Θ,E)` continuum primitives at all; (iii) Proposition R's reduction
(`P_n(\text{same})=\tfrac12P_n(\text{both})`) is pure finite-`n`
algebra needing zero continuum input. No step imports, assumes, or
needs the missing destination-information machinery. **I find no
circularity.**

**A framing note, offered for transparency rather than as a defect.**
The document's "PROVED... continuum theorem" label for item 4
(`P(\text{same}\mid K)=1/(2(K+1))` for `K=0,1`) rests on the *same*
methodology `THEOREM.md` itself uses throughout to certify a "fixed-`K`
bridge, PROVED" (e.g. Proposition 4: derive an exact finite-`n` closed
form, take its elementary `n→∞` limit, and check the limit against an
independently-computed continuum target) — not on a general
coupling/convergence-in-law theorem connecting Definition 4's *joint*
law to Definition 2/3's continuum joint law. Under that established
archive convention this is legitimate and is not a new kind of leap:
the "both cyclic" aggregate is cross-checked against Estágio 24's
independently-derived target (a real, non-trivial confirmation), and
the finer "same final cycle" split then transfers *for free*, at zero
extra cost, purely because Theorem J's Corollary ties it to the
aggregate by an *exact* (not asymptotic) identity at every finite `n`
— so no *separate* joint-convergence argument is actually needed for
that second step, precisely as §2 claims. I record this note only so
a future reader knows exactly what kind of "PROVED" is being invoked
(archive-precedent-consistent value-matching, not a from-scratch
coupling theorem) — it does not change the verdict.

---

## 8. Bugs made in this referee's own work

None found in the final scripts. Process note for full disclosure: the
initial draft of `bruteforce_definition4.py` used 1-indexed labels
`{1,2}` for the query points inconsistently with a 0-indexed `range(n)`
loop in one early sketch (caught and fixed before the first run — no
run with the bug ever produced a logged number, so no retraction is
needed). No other errors encountered.

---

## 9. Scorecard

| Item | Referee verdict |
|---|---|
| Proposition R | **SOUND** — re-derived and confirmed, no edge-case issue at `K=0` or small `n` |
| `K=0` trivial closure | **SOUND** — confirmed exactly |
| `K=1` closed form `(3n²-n+2)/(6n²)` | **SOUND** — independently re-derived from scratch, matches brute force `n=2..7` |
| `V_a(n)`, `V_b(n)` sub-case formulas | **SOUND** — independently re-derived, matches brute force `n=3..6`, both `r=0` and `r=1` |
| False-start value `5/9` at `n=3` | **CONFIRMED**, exactly as disclosed |
| Rate `n(P-\tfrac12)\to-\tfrac16` | **SOUND** — algebra correct |
| §3.3 causal explanation ("Case (a) alone would show `O(1/n²)`") | **ERROR** — false, contradicted by `V_a(n)`'s own formula; does not affect any PROVED result; needs a one-sentence correction |
| `K=0,1` continuum transfer (`P(\text{same}\mid K)=1/2,1/4`) | **SOUND**, consistent with archive's own bridge-proof convention (framing note recorded, not a defect) |
| `K≥2` non-closure diagnosis (§4) | **SOUND** — honest, not overstated (stress-tested and corroborated, if anything conservative) |
| `K=2,3` table values | **8/8 independently confirmed exactly**, including the mandated `n=6,K=2: 44/135` |
| §5 "what is not established" | **HONEST**, no overclaiming found; "transfer not construction" holds up, no smuggled destination information |

**Net assessment.** This is a genuinely careful, well-organized piece
of work whose central claims (Proposition R, the `K=1` closed form,
the `K=0,1` transfer, and the honest `K≥2` non-closure) all survive
independent, from-scratch adversarial re-derivation and brute-force
cross-checking without a single numeric discrepancy. One real error
was found and is named precisely (§3.3's causal narrative) — it is
confined to an explanatory aside and does not touch any of the
document's PROVED-labeled results. **ACCEPT for catalogue** at the
tier claimed, contingent on a correction to §3.3's explanatory
sentence.
