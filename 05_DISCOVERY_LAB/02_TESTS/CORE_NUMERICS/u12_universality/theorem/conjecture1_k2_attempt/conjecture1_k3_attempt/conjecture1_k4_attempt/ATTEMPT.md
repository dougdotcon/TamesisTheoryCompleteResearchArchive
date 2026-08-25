# Conjecture 1 at K=4 — extending the K=2/K=3 whole-space method

> **Governance.** This document is a dispatched research front targeting
> `THEOREM.md` §8 Conjecture 1 at `K=4`, produced as a direct extension of
> `conjecture1_k2_attempt/ATTEMPT.md` (`K=2`, PROVED, integrated as
> "Estágio 15") and
> `conjecture1_k2_attempt/conjecture1_k3_attempt/ATTEMPT.md` (`K=3`,
> PROVED, integrated as "Estágio 17"). Pre-registered in
> `DERIVATION_PREREG.md` (this directory) before any script ran. Every
> claim below is labeled PROVED, CITED (a named classical fact used
> without re-derivation, exactly the citation `THEOREM.md`, `K=2`'s, and
> `K=3`'s own Lemma 1 use), NUMERICALLY SUPPORTED, or OPEN. `THEOREM.md`
> (closed/finalized text), `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
> `DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, any README, and
> every sibling attempt's own files are **not** touched by this document —
> integration is the orchestrating session's job, done later, not this
> front's. No `adversarial/` subdirectory is created and no referee is
> dispatched here — that review is separate and still pending. No git
> command was run. Seed budget used: `20260850000+`, confirmed unused
> before first use (`grep -rn "20260850"` across the archive returned only
> the three reservation lines in `DECISION_LEDGER.yaml`,
> `DISCOVERY_LAB_STATE.md`, `TEST_QUEUE.yaml` — see `DERIVATION_PREREG.md`
> §Governance for the exact grep output). **This document requires
> mandatory independent adversarial verification, exactly as every prior
> front in this lineage has received, before any integration into
> `THEOREM.md` or any ledger.** Nothing here is asserted as fact anywhere
> else in the archive until that review completes.

> **Executive summary (read first).** `THEOREM.md` §8 Conjecture 1 states
> `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, proved at `K=1` (§5.3), `K=2`
> (`conjecture1_k2_attempt/ATTEMPT.md`, `f_{M_2}(x)=4x(1-x^2)`), and `K=3`
> (`conjecture1_k3_attempt/ATTEMPT.md`, `f_{M_3}(x)=6x(1-x^2)^2`). The
> `K=3` document's own §7 states, verbatim, that whether the mechanism
> behind its unexpected closure — off-cycle nodes contribute zero new
> cyclic mass regardless of target, collapsing what looks like `4^K`/`5^K`
> raw destination configurations down to a tractable number of shapes —
> continues to work at `K=4` and beyond is "a new, genuinely open question
> this document raises but does not attempt to answer." This document is
> the first attempt to answer that question, dispatched with the explicit
> expectation that an honest non-closure was fully acceptable.
>
> **That expectation was again not borne out. The extension to `K=4`
> closes completely, by the identical method, with every step verified
> both symbolically and numerically.**
>
> > **Theorem (this document, PROVED modulo one classical citation — the
> > same one `K=2`/`K=3`'s own Lemma 1 use).** `f_{M_4}(x) = 8x(1-x^2)^3`
> > on `(0,1)`, exactly — the `K=4` instance of `THEOREM.md` §8
> > Conjecture 1.
>
> **Why the shape-collapse keeps working, precisely identified this time
> (not just observed).** (1) **Lemma 1 generalizes**, via the `Bell(4)=15`
> co-block set-partitions of `{x_1,x_2,x_3,x_4}`, grouped into 5 *shapes*
> by partition-integer-type (`4`; `3+1`; `2+2`; `2+1+1`; `1+1+1+1`) using an
> **exchangeability argument checked concretely** (not merely asserted):
> the "`3+1`" shape is derived via *two independent routes* — anchor inside
> the size-3 block, and anchor as the singleton — and both give the
> identical constant `2`, with the first route's naive attempt containing
> a genuine algebra bug (caught and fixed in the open, see below). Each
> shape's constant contribution is exactly `∏_j(b_j-1)!` (block sizes
> `b_j`), and — a new observation this document adds — summing this over
> all set partitions of `{1,...,K}` is *exactly* `K!` via the classical,
> elementary bijection between (set partition + per-block cyclic order) and
> permutations (each permutation's own disjoint-cycle decomposition *is*
> such a pair). This identity is checked directly for `K=2,3,4` (predicting
> `2,6,24`) *before* any probabilistic derivation is run, and the full
> peeling derivation (up to **three** sequential residual-property
> applications for the `1+1+1+1` pattern, one more than `K=3`'s maximum of
> two) confirms it. (2) **The destination combinatorics — `5^4=625` raw
> configurations — collapse via the identical structural fact `K=2`/`K=3`
> established** (off-cycle nodes contribute zero regardless of target,
> re-verified independently at K=4 in its own right, not merely assumed
> inherited — a from-scratch discrete mechanism check finds **zero
> mismatches across 105,000 trials**, all 625 raw cells hit). Exhaustive
> brute-force classification finds **exactly 12 shape types** — matching a
> prediction (`Σ_{s=0}^{4}p(s)=1+1+2+3+5=12`, the partition function)
> made and pre-registered *before* the enumeration script ran — and
> confirms the deeper structural fact that the raw-config count for a
> given `(r_on, n_off)` pair is identical across every specific subset and
> cycle-type realizing it. (3) **The exact density formula per shape closes
> via a general, `r`-indexed formula re-derived from scratch in this
> document** (not merely copied from `K=3`'s script), whose one open
> ingredient — an "off-cycle weight" `W_C(Q)` — is verified by direct
> brute-force symbolic enumeration (not assumed) to equal `1-Q` for
> **every** off-cycle count needed at `K=4` (`n_off=0,1,2,3,4`), including
> `n_off=3`, which **exceeds `K=3`'s maximum of `n_off=2`** and is
> precisely the case this document could not simply inherit. Summed
> exactly (`sympy`), the 5 shapes give **exactly** `8x(1-x^2)^3`
> (`sympy` confirms the difference is identically `0`). (4) **A reduction
> check** — this document's own general `K`-parametrized method, applied
> with `K=3` instead of `4`, reproduces `K=3`'s already-PROVED, already
> adversarially-reviewed per-shape densities **exactly, group by group**
> (not just in the final sum) — the same kind of check that caught a real
> error in `K=3`'s own reduction to `K=2`; here it passes cleanly, but only
> after a second, unrelated, honestly-reported bug in the *comparison
> script itself* was caught and fixed (see §5). Three independent numerical
> checks — a discrete-permutation check of Lemma 1 (3 scales, the expected
> discretization-bias signature at small `n`, clean convergence by
> `n=1000,5000`), a from-scratch discrete finite-`n` simulation of the full
> model (`n=10000,20000`, KS `p=0.35,0.30`), and a continuum Monte Carlo of
> the derived recipe (`N=2{,}000{,}000`, KS `p=0.65`) — all pass cleanly
> (no `|z|` above `1.9`).
>
> As a byproduct: `E[M_4]=128/315=φ_4` (matches the already-PROVED
> mean-consistency identity, `THEOREM.md` §5.4, and the Wallis-integral
> value `THEOREM.md` §5.2 gives for `K=4`), and new exact moments
> `E[M_4^2]=1/5`, `E[M_4^3]=128/1155`.
>
> **Two real bugs were caught and fixed in the open during this work** —
> reported in full in §2 and §5 below, per this archive's standing
> discipline, not silently patched.

---

## 0. Discipline / provenance

`DERIVATION_PREREG.md` (this directory) was written and saved before any
script ran; every file below postdates it:

```
2026-08-25T17:14Z  DERIVATION_PREREG.md
2026-08-25T17:18Z+ (all scripts/logs below, same session)
```

All arithmetic labeled PROVED is exact (`sympy.Rational`/symbolic
integration and exact brute-force combinatorics — no floating point enters
any derivation step; floating point appears only in the Monte Carlo checks,
exactly as `K=2`/`K=3`'s documents do). Monte Carlo checks use
`numpy.random.SeedSequence`/`default_rng` values starting at `20260850000`
(this front's reserved block, confirmed unused by `grep -rn "20260850"`
across the archive before first use — the only prior hits were the three
reservation lines in `DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`, and
`TEST_QUEUE.yaml`).

## 1. Setup — the continuum whole-space K=4 model

Exactly generalizing `conjecture1_k3_attempt/ATTEMPT.md` §1's `K=3` object
to `K=4`: an independent `PD(1)` cyclic partition of `[0,1]`; four reroute
sources `x_1,x_2,x_3,x_4\sim\mathrm{Unif}(0,1)` i.i.d.; four destinations
`u_1,u_2,u_3,u_4\sim\mathrm{Unif}(0,1)` i.i.d., independent of everything
else. The map: `f(x_i)=u_i` for `i=1,\dots,4`, and `f(y)=` background
cyclic-successor of `y` for every other `y`. Target: the density of
`M_4:=\mathrm{Leb}(\{y:y\text{ cyclic under }f\})`.

**Lemma 0 (locality of cyclic status, K=4; identical argument to `K=2`'s
and `K=3`'s Lemma 0, restated for completeness).** A point `y` is cyclic
under `f` iff its forward `f`-orbit returns to `y` in finitely many steps.
Only `x_1,\dots,x_4`'s own outgoing arrows are modified, so every other
point's own future trajectory is exactly the background one, regardless of
what flows into it. Consequently: (a) a background block containing none
of `x_1,\dots,x_4` is unaffected in full — this is exactly the "OUT" mass
`1-m_1-m_2-m_3-m_4`, always cyclic; (b) within the touched region, whether
a point is cyclic depends only on the forward chain of (background flow,
jump at a source, background flow again, …), and an incoming jump landing
at a point `w` never changes `w`'s own subsequent orbit. This argument is
`K`-independent (it never mentions how many sources there are), so it
carries over verbatim — nothing new is claimed here at `K=4`.

## 2. Step A — the joint law of the four "region masses" (Lemma 1, K=4)

**Definition.** For `i=1,\dots,4`, `m_i :=` Lebesgue measure of points
whose background-forward flow reaches `x_i` before (if ever) reaching the
other three sources.

> **Lemma 1 (Step A, K=4; PROVED given the cited residual property).**
> `(m_1,m_2,m_3,m_4)` has joint density **exactly `24` (constant) on the
> simplex `Δ_4=\{m_1,\dots,m_4>0,\ m_1+m_2+m_3+m_4<1\}`** — i.e. uniform
> on `Δ_4`.

*Proof.* Generalizing `K=3`'s 5-pattern co-block case split to four points
requires the set-partition of `\{x_1,x_2,x_3,x_4\}` by shared
background-block membership — `Bell(4)=15` mutually exclusive co-block
patterns. Rather than deriving all 15 separately (the literal generalization
of `K=3`'s by-hand approach, and exactly the point at which combinatorial
explosion was feared), this document groups them by **partition-integer
type** — 5 shapes: `4` (all four share one block, 1 pattern); `3+1` (three
share, one separate, `\binom43=4` patterns); `2+2` (two disjoint pairs, `3`
patterns); `2+1+1` (one pair, two singles, `\binom42=6` patterns);
`1+1+1+1` (all four separate, `1` pattern) — `1+4+3+6+1=15=Bell(4)` ✓ — and
justifies collapsing each group into one representative computation via an
**exchangeability argument**, checked concretely rather than only asserted
(see below).

**A general structural fact used throughout (new in this document, PROVED
elementarily).** For a co-block set-partition of `\{1,\dots,K\}` into
blocks of sizes `b_1,\dots,b_r`, this document's peeling method (Fact A +
the `PD(1)` residual property, applied recursively, plus the "labeled
circular spacings are Dirichlet" fact within each block) gives that
pattern's contribution to the joint density of `(m_1,\dots,m_K)` as the
**constant** `\prod_j(b_j-1)!` on `Δ_K`. This is not a coincidence:
choosing a set partition together with an independent **cyclic ordering**
within each block (`(b-1)!` distinct cyclic orderings of `b` labeled items)
is *exactly* the standard, elementary bijection between (set partition +
per-block cyclic order) and **permutations** of `\{1,\dots,K\}` (a
permutation's own disjoint-cycle decomposition *is* such a pair, and vice
versa). Hence `\sum_{\text{set partitions}}\prod_j(b_j-1)! = \sum_{\text{permutations}} 1 = K!`
— a pure combinatorial identity (no probability involved), checked by
brute-force enumeration of set partitions for `K=2,3,4` in
`derive_lemma1_k4_symbolic.py` Part 0, predicting totals `2,6,24`
respectively **before** any probabilistic derivation runs — matching
`K=2`/`K=3`'s already-established constants and predicting this document's
own `K=4` target.

**The `n=4` labeled circular spacings fact, proved inline (not merely
cited), generalizing `K=3`'s own `n=3` proof one level further.** Needed
for the "`4`" (AllSame) shape: with `x_1` fixed as anchor and
`Y_2,Y_3,Y_4\sim\mathrm{Unif}(0,\ell_1)` i.i.d. free points, the 4 circular
gaps (each ending at one of the 4 points) are jointly `\ell_1\cdot
\mathrm{Dirichlet}(1,1,1,1)`, density `3!/\ell_1^3` on the 3-simplex.
Proved by direct integration over all `3!=6` cyclic orderings of the three
free points, with explicit `3\times3` Jacobians — `derive_lemma1_k4_symbolic.py`
Part 1 runs the *identical* generic routine at `j=1` (`n=2`, reproducing
`K=2`'s constant `1`), `j=2` (`n=3`, reproducing `K=3`'s constant `2`, as a
self-check), and `j=3` (`n=4`, the new case), confirming all three exactly.

**The 5 shapes, each derived via explicit sequential peeling
(`derive_lemma1_k4_symbolic.py` Part 2):**

| Shape | Representative pattern | Multiplicity | Constant density | Contribution |
|---|---|---|---|---|
| `4` | `\{1,2,3,4\}` all one block | `1` | `6` | `6` |
| `3+1` | `\{1,2,3\}`same, `4`diff | `4` | `2` | `8` |
| `2+2` | `\{1,2\}`+`\{3,4\}` | `3` | `1` | `3` |
| `2+1+1` | `\{1,2\}`same, `3`,`4`diff | `6` | `1` | `6` |
| `1+1+1+1` | all four separate | `1` | `1` | `1` |
| **Total** | | | | **`24`** |

`∎` (Full symbolic derivation, every Jacobian, every peeling step's
probability×density cancellation, and the pattern-probability
self-consistency check `\sum P(\text{shape})=1`, in
`derive_lemma1_k4_symbolic.py`/`.log`, §6.1 below.)

**Honest process note — a real algebra bug, caught and fixed in the
open.** The `3+1` shape was derived via **two independent routes**, to
check the exchangeability claim (that it does not matter whether the
anchor `x_1` is inside the size-3 block or is the singleton) *concretely*
rather than only by symmetry assertion. Route A (anchor inside the
3-block) gave the constant `2` cleanly. Route B (anchor as the singleton,
`\{2,3,4\}` together) was **first** computed using `P(x_3\text{ lands in
}x_2\text{'s block}\mid \ell_1,\ell_2) = \ell_2/(1-\ell_1)` — treating this
as a probability *relative to the rescaled residual*, by (incorrect)
analogy with how Fact A itself is invoked on a rescaled residual. This
produced a joint density of `2/(\ell_1-1)^2` — genuinely `\ell_1`-dependent
(confirmed via `sp.diff(\cdot,\ell_1)\ne0` in the script), **failing** the
required constant-on-`Δ_4` check. Diagnosed: `x_3,x_4` are
`\mathrm{Unif}(0,1)` on the **whole** unit interval, not on the rescaled
residual — their probability of landing in `B_2` (an *absolute* subset of
`[0,1]` of measure `\ell_2`) is simply `\ell_2`, not `\ell_2/(1-\ell_1)`;
the erroneous `/(1-\ell_1)` conflated the residual-*rescaling* used for
peeling `\ell_2`'s own density (via Fact A on the rescaled residual) with
the separate, already-absolute question of whether a point lands in a
fixed-measure subset of `[0,1]`. Fixed: using the correct absolute
probability `\ell_2` gives joint density `2` — an exact match to Route A.
**This is reported here precisely because it is the kind of subtle,
scale-confusion error the `K=3` document's own §7 flagged as the specific
risk that additional residual-peeling depth might introduce at `K=4`** —
and it is exactly what happened, caught by the pre-registered
constant-density check, not silently patched.

**On the citation.** Exactly as `K=2`/`K=3`: `L_1\sim\mathrm{Unif}(0,1)` by
the classical size-biased-sampling fact (McCloskey 1965; Patil–Taillie
1977; Pitman, *Combinatorial Stochastic Processes*, St-Flour 2002, Ch. 3),
and the `PD(1)` residual property, applied recursively — here up to
**three** sequential peels (the `1+1+1+1` pattern: `\ell_1\to\ell_2\to
\ell_3\to\ell_4`), one more than `K=3`'s maximum of two. This is the
*identical* citation, applied one additional time — not a new or weaker
link; iterating a self-similar/recursive classical property is exactly
what the property licenses, the same move `K=3`'s own Lemma 1 already
makes to go from `K=2`'s one peel to two.

## 3. Step B — the destination combinatorics: classification into 12 shape types

With 4 destinations `u_1,\dots,u_4`, each landing in region `1,2,3,4`, or
`\mathrm{OUT}`, there are `5^4=625` raw combinations.

**The structural fact (identical statement to `K=2`/`K=3`, re-verified
independently at K=4, not merely assumed inherited).** Model the redirect
structure as `g:\{1,2,3,4\}\to\{1,2,3,4,\mathrm{OUT}\}`. A point contributes
new cyclic mass **iff** its source index lies on a genuine cycle of `g`;
every node NOT on a cycle contributes exactly zero new cyclic mass,
regardless of where its own redirect lands. The proof of this fact
(Lemma 0(b), a chain from an off-cycle node either drains to OUT or merges
into a cycle's own periodic pattern *without ever returning to its own
starting node*) never referenced `K=3` specifically — it is `K`-independent
— so it is expected, and independently confirmed below (§3.1), to carry
over verbatim.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-069`, nota
> cosmética §9 do referee] O esboço acima herda a exposição
> comprimida de `K=3` para o subcaso mais sutil — um
> redirecionamento fora-de-ciclo pousando *dentro* de um arco já
> periódico. Esse subcaso está traçado explicitamente na correção
> pós-adversarial do documento `K=3`
> (`conjecture1_k3_attempt/ATTEMPT.md`, §3, `DISC-DEC-065`); o
> argumento é `K`-independente e vale aqui verbatim, e a checagem de
> mecanismo de 110.000 trials do referee (incluindo a escala `n=12`
> saturada de colisões/pontos-fixos) o confirma exaustivamente em
> `K=4`. Não é um erro; nota de completude de exposição.

**Exhaustive brute-force classification** (`enumerate_destination_combinatorics_k4.py`,
exact functional-graph cycle detection, not by hand) of all 625 raw
configurations, by `(r_{\text{on}}:=|\text{on-cycle set}|,\ \text{cycle
type of the permutation on that set})`:

| `r_on` | cycle type(s) present | shape types at this `r_on` | raw configs |
|---|---|---|---|
| `0` | (empty) | `1` | `125` |
| `1` | `1` | `1` | `200` |
| `2` | `1{+}1`, `2` | `2` | `180` |
| `3` | `1{+}1{+}1`, `2{+}1`, `3` | `3` | `96` |
| `4` | `1{+}1{+}1{+}1`, `2{+}1{+}1`, `3{+}1`, `2{+}2`, `4` | `5` | `24` |
| **Total** | | **`12`** | **`625`** |

`1+1+2+3+5=12` shape types — **exactly** matching the pre-registered
prediction `\sum_{s=0}^{4}p(s)` (`p(s)`= number of integer partitions of
`s`), made in `DERIVATION_PREREG.md` **before** this script ran, and
exactly generalizing `K=3`'s `\sum_{s=0}^{3}p(s)=7` shapes.

**A further structural fact, checked (not assumed):** for every `(r_on,
n_off)` pair, the raw-config count is **identical** across every specific
choice of on-cycle subset and cycle type realizing that `r_on` — i.e. the
"off-cycle raw count" `N(r_on,n_off)` (`125,50,15,4,1` for
`n_off=4,3,2,1,0` respectively) depends only on `(r_on,n_off)`, never on
*which* labels or *which* permutation. Cross-checked against the coarse
`r_on` totals: `\sum_{r} \binom4r\, r!\, N(r,4{-}r) = 625` exactly.

### 3.1 Discrete mechanism check — per-configuration exact match

Generalizing `K=3`'s own 52,000-trial check (itself generalizing the
`K=2` referee's decisive check), `mechanism_check_k4.py` builds a genuine
uniform random permutation `\pi`, four distinct reroute labels, i.i.d.
uniform destinations (with replacement — collisions and fixed points
allowed), the actual map `f`, and finds the **true** cyclic set by a
from-scratch color-marking orbit trace (ground truth). Independently, it
computes the **predicted** count from this document's own mechanism
(region/distance classification + cycle detection among `\{1,2,3,4\}` +
the `(D_i{+}1)`-points-per-cycle-member formula) and compares exactly.

```
n=25,  trials=80000: mismatches=0/80000  (match rate=1.00000000)
n=150, trials=25000: mismatches=0/25000  (match rate=1.00000000)
TOTAL: 0 mismatches / 105000 trials, ALL 625 raw target-cells hit at BOTH
  scales (including 17798+1008 collision trials, 12861+667 fixed-point
  trials)
```

**Zero mismatches across both scales, every one of the 625 raw cells hit
at both scales, including every collision and fixed-point edge case** —
the mechanism is confirmed to generalize to `K=4` at the same granular,
per-configuration level `K=2`/`K=3` used.

## 4. Step C/D — assembling `f_{M_4}(x)`

Each shape's contribution is derived by exact marginalization (never a
Dirac delta), via a general `r`-indexed formula **re-derived from scratch
in this document** (not merely copied from `K=3`'s script, since `K=4`
needs off-cycle counts up to `n_off=3` — one more than `K=3`'s maximum —
so the pattern found at `K=3` is *checked*, not *assumed*, to persist):

For a fixed on-cycle subset `C` (`|C|=r`), the "discrete choice probability
times position density cancels to `1`" mechanism (re-verified generically
at `K=4`, Part A of `derive_step2_k4_symbolic.py`) means the joint density
of `(m_1,\dots,m_4,\{P_j\}_{j\in C})`, summed over all `r!` internal cycle
permutations on `C`, is the constant `r!\cdot24\cdot W_C(\text{off-masses})`,
where `W_C` — the **off-cycle weight** — is the sum, over every way the
`n_off=4-r` off-cycle nodes can independently target *anything but
themselves* (another region, another off-cycle node, or OUT) *without
forming a new cycle purely among themselves*, of the product of the target
masses. `W_C` is computed by **brute-force symbolic enumeration**
(`derive_step2_k4_symbolic.py` Part B) — not assumed — for every
`n_off\in\{0,1,2,3,4\}` needed:

```
n_off=1: W_C = 1 - m4                    = 1 - Q   (Q = sum of off masses)
n_off=2: W_C = 1 - m3 - m4                = 1 - Q
n_off=3: W_C = 1 - m2 - m3 - m4           = 1 - Q   <-- NEW, exceeds K=3's max n_off=2
n_off=4 (T0, r=0): P_T0 = 1 - m1-m2-m3-m4 = 1 - Q   (cross-checked via a
                                                       literal 625-term
                                                       brute-force sum)
```

**`W_C(Q)=1-Q` for every off-cycle count needed at `K=4`, including
`n_off=3` — the exact extension `K=3` could not by itself confirm.** (An
informal, *not fully proved here*, structural explanation: this matches
the closed form `E\cdot(E+Q)^{n_{\text{off}}-1}` of the classical weighted
generalization of Cayley's formula for labeled forests, with `E:=1-Q`
[the combined "external" weight of on-cycle-plus-OUT] — since `E+Q=1`
identically, this collapses to `E\cdot1^{n_{\text{off}}-1}=E=1-Q`
*independently of `n_off`*. This is offered as a *suggestive*, not
independently re-verified beyond `n_off\le4`, explanation for why the
pattern might continue at `K\ge5` — a lead for a future front, not a claim
made here.)

Given `W_C(Q)=1-Q`, the change of variables `(m_j,P_j)\to(P_j,D_j{:=}m_j{-}P_j)`
for `j\in C` (unit Jacobian, `K=2`'s own "Group A" trick generalized to `r`
variables at once) turns the constant into a joint density of
`(P_1,\dots,P_r,D_1,\dots,D_r,\text{off-masses})` that is *still* the same
constant; marginalizing at fixed `s=\sum P_j`, `t=\sum D_j=`new mass,
`Q=\sum` off-masses gives:

```
f_(r,n_off)(x) = binom(4,r) * 24 * x^r *
    Integral_{Q=0}^{1-x} (1-Q) * Q^(n_off-1)/(n_off-1)! *
                          (1-x-Q)^(r-1)/(r-1)! dQ        (r>=1, n_off>=1)
```

with the `n_off=0` case (`r=4`) collapsing directly (no `Q` integral) and
`r=0` (`T0`) computed via the complement-probability route (as `K=3`'s own
script does), cross-checked against a literal 625-term brute-force sum
over the same raw classification §3 already validated:

```
f_(r=0)(x) [T0] = -4x^4 + 12x^3 - 12x^2 + 4x
f_(r=1)(x)       = -12x^5 + 32x^4 - 24x^3 + 4x
f_(r=2)(x)       = -12x^6 + 24x^5 - 24x^3 + 12x^2
f_(r=3)(x)       = -4x^7 + 24x^5 - 32x^4 + 12x^3
f_(r=4)(x)       = -4x^7 + 12x^6 - 12x^5 + 4x^4
```

**Per-shape probability cross-check.** `P(r_on{=}0,\dots,4) = 1/5,\ 2/5,\
2/7,\ 1/10,\ 1/70` respectively, summing to `1` exactly (`14+28+20+7+1=70`
over `70`) — a stronger check than the final sum alone, since an error
that happened to cancel in the grand total would still be caught here.

**Summing:**

```
f_M4(x) = f_(r=0) + f_(r=1) + f_(r=2) + f_(r=3) + f_(r=4)
        = -8x^7 + 24x^5 - 24x^3 + 8x
```

`8x(1-x^2)^3 = 8x(1-3x^2+3x^4-x^6) = 8x-24x^3+24x^5-8x^7` — **identical**.
`sympy.simplify(f_M4(x) - 8x(1-x^2)^3)` returns exactly `0`.

> **Theorem.** `f_{M_4}(x) = 8x(1-x^2)^3` on `(0,1)` — PROVED, modulo the
> citation of §2 (the `PD(1)` residual/size-biased-sampling property,
> identical in kind and risk level to `K=2`/`K=3`'s own citation, applied
> recursively up to three times, not newly or more riskily).

Cross-checks (all exact, `sympy`): `\int_0^1 f_{M_4}\,dx=1` ✓;
`\int_0^1 x f_{M_4}\,dx = 128/315 = \varphi_4` ✓ (matches the already-PROVED
mean-consistency identity, `THEOREM.md` §5.4, for every `K`, **and**
matches `THEOREM.md` §5.2's Wallis-integral closed form
`4^K(K!)^2/(2K{+}1)!` evaluated at `K=4`: `256\cdot576/362880=128/315`);
new exact moments `E[M_4^2]=1/5`, `E[M_4^3]=128/1155`.

## 5. R2 — the K=3 reduction check (and a second caught error)

Applying this front's *own* general, `r`-indexed shape-derivation method
with **3** total reroute sources instead of 4 (base Lemma-1 density `3!=6`
on the simplex, `W_C(Q)=1-Q` re-derived by brute force for `n_off\in\{1,2\}`
rather than `\{1,2,3\}`) should reproduce
`conjecture1_k3_attempt/ATTEMPT.md`'s already-PROVED, already
adversarially-reviewed `f_{M_3}(x)=6x(1-x^2)^2` — and it does, **group by
group** (`r_on=0,1,2,3`), not merely in the final sum
(`r3_k3_reduction_check.py`):

```
r=0 (T0):           this method = 3x^3-6x^2+3x     established = 3x^3-6x^2+3x     MATCH
r=1 (T1a):           this method = 6x^4-9x^3+3x     established = 6x^4-9x^3+3x     MATCH
r=2 (T1b+T2a):        this method = 3x^5-9x^3+6x^2   established = 3x^5-9x^3+6x^2   MATCH
r=3 (T1c+T2b+T3):     this method = 3x^5-6x^4+3x^3   established = 3x^5-6x^4+3x^3   MATCH
Sum: 6x^5-12x^3+6x = 6x(1-x^2)^2  MATCH
```

**Honest process note — a second real bug, unrelated to the mathematics,
caught and fixed in the open.** The **first** version of the comparison
above built the "established" `K=3` reference densities via
`sp.sympify("3*x**3 - 6*x**2 + 3*x")` — a string literal. `sympify()`
parses a **fresh** `Symbol('x')` from the string, *without* this script's
own `positive=True` assumption on `x` — so the resulting expression's `x`
was a genuinely *different* `sympy` symbol from the `x` used everywhere
else in the script, despite printing identically. `results[0] -
established[0]` could then never cancel (`sympy` correctly refuses to
equate two distinct symbols of the same name but different assumptions),
producing a persistent false "MISMATCH" at `r=0` that **neither**
`sp.simplify()` **nor** `sp.expand()` resolved — both were operating
correctly on what was, to `sympy`, genuinely a difference of two different
variables. Diagnosed via `sp.srepr()` (which showed two distinct
`Symbol('x', ...)` objects with different assumption sets) after the
naive fixes failed to help. Fixed by building every "established" entry as
a direct `sympy` expression using the script's own `x` symbol, with no
`sympify`-from-string anywhere. **This is a real, if elementary, `sympy`
pitfall, reported here exactly because it produced a genuinely misleading
false-negative on a check whose entire purpose was catching real errors —
worth flagging for any future front reusing this pattern.**

## 6. Verification

### 6.1 Symbolic derivation (the proof itself)

`derive_lemma1_k4_symbolic.py`/`.log`: Step A (Lemma 1) — the general
`\prod(b_j{-}1)!`/`K!` identity check (Part 0), the `n=2,3,4` circular
spacings fact proved inline (Part 1), all 5 K=4 shapes via explicit
sequential peeling including the two-route `3+1` cross-check and its
caught bug (Part 2), and the final total/self-consistency check (Part 3).
`enumerate_destination_combinatorics_k4.py`/`.log`: brute-force
classification of all 625 raw destination configurations into 12 shape
types (§3), the `N(r_on,n_off)` constancy check, and the raw-count
cross-check. `derive_step2_k4_symbolic.py`/`.log`: the on-cycle
cancellation re-verification (Part A), the brute-force off-cycle-weight
derivation for every `n_off` needed including the new `n_off=3` case (Part
B), the general formula's assembly for `r=1,\dots,4` (Part C), `T0` via two
independent routes (Part D), the final symbolic sum, the exact match to
`8x(1-x^2)^3`, the moment checks, and the per-shape probability
cross-check. `r3_k3_reduction_check.py`/`.log`: §5, including the caught
`sympify` bug.

### 6.2 R_MC1 — independent discrete-permutation check of Lemma 1

`mc_lemma1_k4_check.py`, seeds `20260850020/021/022`, three scales
(`n=300,1000,5000`; `15000/10000/6000` trials). Generalizing `K=3`'s own
independent Lemma-1 check to four sources — does not touch continuum
`PD(1)`/stick-breaking machinery at all, using the same `region_and_distance`
routine validated by the 105,000-trial exact-match mechanism check of §3.1.

```
n=300:  E[m_i]~0.199-0.202 (|z|<1.9), E[m1^2]=0.0657 (target 1/15=0.0667),
        Cov(m1,m2)=-0.00667 (target -1/150=-0.00667, close MC match)
        KS(L vs 4ell^3): p=0.0016   KS(pooled m_i vs Beta(1,4)): p=0.0000
        Exchangeability KS(m1 vs m2): p=0.25, KS(m1 vs m4): p=0.03
n=1000: KS(L): p=0.08   KS(marginal): p=0.15   Exchangeability: p=0.59,0.99
n=5000: KS(L): p=0.70   KS(marginal): p=0.46   Exchangeability: p=0.45,0.50
```

The small-`n` KS rejection at `n=300` and clean convergence to
non-rejection by `n=1000,5000` is **exactly the expected discretization-
bias signature** of a genuine continuum limit claim — the identical
pattern `K=3`'s own Lemma-1 check exhibited (and `K=3`'s own referee
confirmed and explained) — not evidence against Lemma 1. All moments
match at every scale (`|z|<1.9`); exchangeability never rejected at scale.

### 6.3 R_MC2 — raw discrete finite-n simulation of the full model

`discrete_k4_full_distribution_mc.py`, seeds `20260850010/011`. A
from-scratch simulator reusing **only** the ground-truth orbit tracer
already independently validated in §3.1 (`true_cyclic_count`) — none of
the region/shape/formula machinery. Builds a genuine uniform random
permutation, 4 rerouted labels, i.i.d. uniform destinations, finds the
true cyclic set, repeats:

```
n=10000, trials=4000: KS D=0.01472 p=0.3479  mean(M4/n)=0.402779+/-0.002980
                       vs 128/315=0.406349 (z=-1.20)
n=20000, trials=2000: KS D=0.02175 p=0.2963  mean(M4/n)=0.403062+/-0.004255
                       vs 128/315=0.406349 (z=-0.77)
```

Both scales pass cleanly (no rejection), means consistent with `128/315`.
This is the strongest available independent check — genuinely different
code (discrete combinatorics, not continuum measure theory) converging to
`8x(1-x^2)^3` at large finite `n`, exactly generalizing `K=2`/`K=3`'s own
analogous check.

### 6.4 R_MC3 — Monte Carlo of the derived continuum recipe

`mc_recipe_check_k4.py`, seed `20260850030`, `N=2{,}000{,}000`: draw
`(m_1,m_2,m_3,m_4)` from Lemma 1 (via `\mathrm{Dirichlet}(1,1,1,1,1)`),
draw `u_1,\dots,u_4\sim\mathrm{Unif}(0,1)`, classify, find cycles, compute
`M_4` via the exact continuum formula of §3/§4 (independent
re-implementation, not reusing the symbolic-integration code of §4):

```
KS D=0.00052 p=0.6543   mean=0.406478+/-0.000132 vs 128/315=0.406349 (z=+0.98)
```

Passes cleanly (not rejected); confirmatory of the full recipe's internal
consistency.

### 6.5 Summary table

| Check | What | Result |
|---|---|---|
| §4 | `\int x f_{M_4}=128/315=\varphi_4` | exact, symbolic — matches the already-PROVED `THEOREM.md` §5.4 mean identity and §5.2's Wallis-integral value |
| — | `E[M_4^2]=1/5`, `E[M_4^3]=128/1155` | exact, symbolic (new) |
| §4 | per-shape probability cross-check (5/5) | all match exactly (`1/5,2/5,2/7,1/10,1/70`, sum `1`), independent route |
| §5 (R2) | K=3 reduction reproduces `6x(1-x^2)^2` group-by-group | exact match (after catching and fixing a real, unrelated `sympy`-assumptions bug in the comparison script) |
| §3.1 | discrete mechanism check, 625 cells | **0 mismatches / 105,000 trials**, 2 scales, all 625 cells hit at both |
| R_MC1 | Lemma 1, independent discrete-permutation | 3 scales, convergent KS trend, moments match |
| R_MC2 | raw discrete finite-`n` full-model simulation | KS `p=0.35,0.30`; `n=10000,20000` |
| R_MC3 | MC of the derived recipe | KS `p=0.65`, `z=+0.98` |

Every check passes; no script was selectively rerun. Two real bugs were
caught during this work (§2's residual-vs-absolute-probability scale
confusion in the `3+1` shape's second derivation route; §5's `sympify`
fresh-symbol/assumptions mismatch in a comparison script) — both reported
here in the open, per this archive's standing discipline, rather than
silently corrected.

## 7. Scope, honesty, and what remains open

**What is PROVED here.** `f_{M_4}(x)=8x(1-x^2)^3` on `(0,1)`, exactly —
the `K=4` instance of `THEOREM.md` §8 Conjecture 1 — via a whole-space
computation generalizing `THEOREM.md` §5.3 (`K=1`), `conjecture1_k2_attempt/ATTEMPT.md`
(`K=2`), and `conjecture1_k3_attempt/ATTEMPT.md` (`K=3`)'s method to four
reroute sources. Both major steps close fully: Lemma 1's generalization
(§2) and the destination-combinatorics classification and assembly (§3–§4),
each independently verified numerically as well as symbolically.

**The one non-self-contained input.** Exactly as at `K=2`/`K=3`: Lemma 1
relies on the `PD(1)` residual/size-biased-sampling property (McCloskey
1965; Patil–Taillie 1977), here applied **recursively up to three times**
(one "peel" per additional separate block in the `1+1+1+1` pattern),
rather than `K=3`'s maximum of two. This is not a new or weaker citation —
iterating a self-similar/recursive classical property is exactly what the
property licenses, and is the same move `K=3`'s own Lemma 1 already makes
to extend `K=2`'s single use to two. Anyone auditing `THEOREM.md`'s Stage 1
core, or the already-accepted `K=2`/`K=3` documents, already accepts this
citation at this rigor level; nothing here asks for more trust than that.

**Why the feared explosion again did not materialize, identified
precisely this time.** `K=3`'s own §7 left this as "a new, genuinely open
question... does not attempt to answer." The mechanism identified here:
(a) the number of destination-combinatorics **shape types** grows as
`\sum_{s=0}^K p(s)` (the partition function, summed), not as `4^K`/`5^K` —
`4` at `K=2`, `7` at `K=3`, `12` at `K=4` — because the density formula for
an on-cycle set depends *only* on `r_{\text{on}}=|C|`, never on the
specific cycle decomposition within `C` (the on-cycle discrete-choice ×
position-density cancellation removes all dependence on the specific
permutation, §4 Part A); (b) the one quantity that genuinely needed to be
*checked, not assumed*, at each new `K` — the off-cycle weight `W_C(Q)` —
is verified here, by brute-force symbolic enumeration, to equal `1-Q` for
every `n_off` up to `4`, including `n_off=3` (the case exceeding `K=3`'s
own maximum), and an informal (not independently re-proved beyond
`n_off\le4` here) structural explanation is offered via the classical
weighted-forest identity `E(E{+}Q)^{n-1}=E` (since `E{+}Q=1` always); (c)
Lemma 1's own generalization required one additional recursive peel
(three instead of two) and one additional labeled-spacings case (`n=4`
instead of `n=3`), both handled by the *same* citation/technique, with no
new mathematical machinery — only more bookkeeping, and that bookkeeping
was done by exhaustive brute-force enumeration (§2, §3) rather than by
hand, exactly the discipline `K=3`'s own §3 process note recommends.

**What was NOT attempted.** General `K\ge5`: this document computed `K=4`
specifically, verified extensively, and did **not** attempt `K=5` or
higher. The structural explanation above (shape-type count growing as
`\sum_{s\le K}p(s)`, and the off-cycle weight collapsing to `1-Q` via the
classical weighted-forest identity) is offered as an informal, *post hoc*
account of why `K=4` was tractable — strengthened, relative to `K=3`'s own
analogous (weaker) account, by the fact that the crux new ingredient
(`n_off=3`) *was* checked here, not merely conjectured — but it is still
not a proof that the same mechanism stays manageable for `K=5,6,\dots`.
`\sum_{s\le K}p(s)` itself grows (the partition function `p(s)` grows
sub-exponentially but the *number of raw configurations needing off-cycle-
weight verification* at each new `K` still grows, and the weighted-forest
identity's general-`n` case, though classical, was not independently
re-derived here beyond the specific instances needed). `THEOREM.md` §8
Conjecture 1 for `K\ge5` remains exactly as open as before this document;
no claim is made about it here. A natural, concrete next step for a future
front: verify the weighted-forest identity `W(n)=1-Q` in full generality
(not case-by-case), which would settle the one genuinely open ingredient
for *all* `K` at once, rather than one `K` at a time.

**No claim of progress on any Millennium Problem.** This document is
purely internal combinatorial mathematics on the archive's own
random-permutation-with-reroutes ensemble, exactly as every other document
in this lineage states.

## 8. Scorecard

| Item | Status |
|---|---|
| `f_{M_4}(x) = 8x(1-x^2)^3` | **PROVED** (modulo §2's citation, applied recursively up to three times) |
| `E[M_4] = \varphi_4 = 128/315` | PROVED (matches `THEOREM.md` §5.4's already-proved mean identity, and §5.2's Wallis-integral closed form at `K=4`) |
| `E[M_4^2]=1/5`, `E[M_4^3]=128/1155` | PROVED (new) |
| Step A uniform-simplex law (Lemma 1, K=4) | PROVED modulo the cited `PD(1)` residual property, applied recursively (up to 3 peels) |
| The general `\prod(b_j-1)!` / `K!` set-partition identity | PROVED (elementary combinatorics; new observation, checked for `K=2,3,4`) |
| Destination-combinatorics classification (12 shape types, 625 raw configs) | PROVED (exhaustive brute-force enumeration + exact symbolic densities) |
| Off-cycle weight `W_C(Q)=1-Q` for `n_off=0,1,2,3,4` | PROVED (direct brute-force symbolic enumeration, not assumed) |
| General weighted-forest identity `W(n)=1-Q` for *all* `n` | OPEN (classical fact offered as informal explanation, not independently re-proved here beyond `n\le4`; a concrete, well-scoped item for a future front) |
| Per-shape probability cross-check (5/5) | PROVED (independent route, all match) |
| K=3 reduction check (R2) | PROVED, matches `conjecture1_k3_attempt/ATTEMPT.md` group-by-group (after catching and fixing a real, unrelated `sympy`-assumptions bug) |
| Discrete mechanism check (625 cells, 105,000 trials) | 0 mismatches — strong NUMERICAL/combinatorial confirmation |
| Numerical cross-checks (R_MC1–R_MC3) | 3/3 pass, no selective reruns |
| `K\ge5` | **not attempted**, left exactly as open as before; a concrete lead (the general weighted-forest identity) is offered for a future front |

**This document's net result: `THEOREM.md` §8 Conjecture 1 is (subject to
the mandatory adversarial review below) PROVED at `K=4`**, extending the
now-closed `K=1,2,3` line one step further, and — for the second front in a
row in this exact lineage — contradicting the immediately-preceding
document's own explicit non-attempt/open-question framing for the next
`K`. Ready for the standing adversarial-referee requirement this archive
applies to every positive finding before any catalog update to
`THEOREM.md` itself.

> [Correção pós-adversarial, 2026-08-25 — `DISC-DEC-069`] Revisão
> adversarial concluída: veredito **SOUND — ACCEPT for catalogue.**
> Nenhum erro matemático encontrado em lugar algum. O referee
> reconstruiu tudo do zero por rotas distintas — os 15 padrões do
> Lema 1 individualmente, o fato de espaçamentos `n=4` por duas rotas,
> `W_C=1−Q` por enumeração própria até `n_off=4`, uma superfície nova
> de momentos exatos sobre as 625 configurações brutas SEM a
> maquinaria de colapso, mecanismo discreto do zero (110.000 trials,
> 0 divergências, incluindo escala de estresse `n=12`), Monte Carlo
> contínuo de 8M com testes por tipo-de-ciclo que nenhuma frente
> havia rodado, e simulação discreta bruta em `n=40000` (escala nunca
> rodada pela frente) — descartando explicitamente a hipótese de erro
> sistemático herdado na linhagem. Único achado: a nota cosmética
> tratada no adendo do §3 acima. Integrado como "Estágio 20" em
> `THEOREM.md`. Ver `adversarial/REFEREE_REPORT.md`.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `mechanism_check_k4.py` | `20260850001`, `20260850002` | reserved `20260850000+` |
| `discrete_k4_full_distribution_mc.py` | `20260850010`, `20260850011` | reserved `20260850000+` |
| `mc_lemma1_k4_check.py` | `20260850020`, `20260850021`, `20260850022` | reserved `20260850000+` |
| `mc_recipe_check_k4.py` | `20260850030` | reserved `20260850000+` |

No seed outside this front's own `20260850000+` reservation was used.

## Files table

| File | Role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any script ran |
| `derive_lemma1_k4_symbolic.py` / `.log` | Step A / Lemma 1, K=4 (§2, §6.1) |
| `enumerate_destination_combinatorics_k4.py` / `.log` / `.json` | brute-force 625-config classification into 12 shape types (§3) |
| `mechanism_check_k4.py` / `.log` / `.json` | discrete per-configuration mechanism check (§3.1) |
| `derive_step2_k4_symbolic.py` / `.log` | Step B/C/D assembly, all 5 shape densities, final sum (§4, §6.1) |
| `r3_k3_reduction_check.py` / `.log` | K=3 reduction check, including the caught `sympify` bug (§5) |
| `mc_lemma1_k4_check.py` / `.log` / `.json` | R_MC1 (§6.2) |
| `discrete_k4_full_distribution_mc.py` / `.log` / `.json` | R_MC2 (§6.3) |
| `mc_recipe_check_k4.py` / `.log` / `.json` | R_MC3 (§6.4) |
| `ATTEMPT.md` | this document |
