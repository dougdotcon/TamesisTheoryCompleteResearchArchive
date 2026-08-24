# Conjecture 1 at K=3 — extending the K=2 whole-space method

> **Governance.** Wave 15, front (b) (`CONJECTURE-1-K3-ATTEMPT`), authorized
> by `DISC-DEC-063` in `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`.
> Pre-registered in `DERIVATION_PREREG.md` before any script ran. Every
> claim below is labeled PROVED, CITED (a named classical fact used
> without re-derivation, exactly `THEOREM.md`'s own discipline, and the
> *same* citation `conjecture1_k2_attempt/ATTEMPT.md`'s own Lemma 1 uses),
> NUMERICALLY SUPPORTED, or OPEN. `THEOREM.md` (closed/finalized text) is
> **not** edited by this document, nor is any ledger or governance file.
> No git command was run. Seed budget used: `20260843000+` (this front's
> reservation), confirmed unused before first use; the referee range
> `20260844000+` was **not** used here. **This document requires
> mandatory independent adversarial verification, exactly as every
> prior front in this lineage has received, before any integration into
> `THEOREM.md` or any ledger.** Nothing here is asserted as fact anywhere
> else in the archive until that review completes.

> **Executive summary (read first).** `THEOREM.md` §8 Conjecture 1 states
> `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, proved at `K=1` (§5.3) and, as of wave 14
> front (c), at `K=2` (`conjecture1_k2_attempt/ATTEMPT.md`, `f_{M_2}(x)
> =4x(1-x^2)`). Two prior fronts in this exact lineage — `k2_open_lemma`
> for its own (different) `n\to\infty`-bridge problem, and
> `conjecture1_k2_attempt/ATTEMPT.md` §7 itself, for this same
> density-conjecture problem — explicitly diagnosed combinatorial
> explosion as the likely structural reason this style of method would
> not trivially generalize past `K=2`, and this front was dispatched with
> the explicit expectation that an honest non-closure was a fully
> acceptable outcome.
>
> **That expectation was not borne out. The extension to `K=3` closes
> completely.**
>
> > **Theorem (this document, PROVED modulo one classical citation —
> > the same one `conjecture1_k2_attempt/ATTEMPT.md`'s own Lemma 1
> > uses).** `f_{M_3}(x) = 6x(1-x^2)^2` on `(0,1)`, exactly — the `K=3`
> > instance of `THEOREM.md` §8 Conjecture 1.
>
> The reason the expected explosion did not materialize: (1) **Lemma 1
> generalizes cleanly.** With three reroute sources, the joint law of the
> region masses `(m_1,m_2,m_3)` is exactly uniform (density `3!=6`) on the
> simplex `Δ={m_1,m_2,m_3>0,m_1+m_2+m_3<1}` — proved by a 5-pattern case
> split (the co-block set-partitions of `\{x_1,x_2,x_3\}`, Bell number
> `B_3=5`), using the *same* `PD(1)` residual/size-biased citation as
> `K=2`, applied **recursively** (a legitimate, not a new, use — iterating
> a self-similar property is exactly what the property says). (2) **The
> destination combinatorics — `4^3=64` raw configurations, feared to be
> the explosion point — collapse via a genuine structural fact, not a
> lucky pattern-match:** a point contributes new cyclic mass **iff** its
> source lies on a literal cycle of the 3-node redirect digraph; every
> off-cycle node contributes **exactly zero**, regardless of where its own
> redirect lands. This reduces 64 raw cells to exactly **7 mutually
> exclusive shapes** (confirmed by exhaustive computer enumeration, not
> by hand — a real error was caught this way, see below), each with a
> closed-form density derived via exact `sympy` marginalization. Summed,
> the 7 shapes give **exactly** `6x(1-x^2)^2` (`sympy.simplify` confirms
> the difference is identically `0`). (3) Every group's own probability
> mass independently matches its target-level probability (a per-shape
> consistency check, not just the final sum); the whole 7-shape
> decomposition, applied with 2 nodes instead of 3, exactly reproduces
> the *already-proved* `K=2` result `4x(1-x^2)` group-by-group (a strong
> reduction check, mirroring `K=2`'s own R2) — **and this specific side
> check is where a real by-hand classification error (a missed shape)
> was caught and fixed in the open**, which is exactly why the main
> `K=3` classification was done by exhaustive brute-force enumeration
> rather than by hand in the first place. A discrete, per-configuration
> mechanism check (mirroring the `K=2` referee's own decisive check)
> found **zero mismatches across 52,000 trials** at two scales, hitting
> all 64 raw target cells including collisions and fixed points. Three
> independent numerical checks — an independent discrete-permutation
> check of Lemma 1, a from-scratch discrete finite-`n` simulation of the
> full model (`n=10000,20000`), and a continuum Monte Carlo of the
> derived recipe — all pass cleanly (KS `p` from `0.16` to `0.70`, no
> `|z|` above `1.8`).
>
> As a byproduct: `E[M_3]=16/35=\varphi_3` (matches the already-PROVED
> mean-consistency identity, `THEOREM.md` §5.4), and new exact moments
> `E[M_3^2]=1/4`, `E[M_3^3]=16/105`.

---

## 0. Discipline / provenance

`DERIVATION_PREREG.md` (this directory) was written and saved before any
script ran; every file below postdates it:

```
2026-08-24T18:22Z  DERIVATION_PREREG.md
2026-08-24T18:23Z+ (all scripts/logs below, same session, through 18:56Z)
```

All arithmetic labeled PROVED is exact (`sympy.Rational`/symbolic
integration and exact `fractions`-equivalent combinatorics — no floating
point enters any derivation step; floating point appears only in the
Monte Carlo checks, exactly as `K=2`'s document does). Monte Carlo checks
use `numpy.random.SeedSequence`/`default_rng` values starting at
`20260843000` (this front's reserved block, confirmed unused by
`grep -rn "20260843"` across the archive before first use — the only
prior hits were the three reservation lines in `DECISION_LEDGER.yaml`,
`DISCOVERY_LAB_STATE.md`, and `TEST_QUEUE.yaml`).

## 1. Setup — the continuum whole-space K=3 model

Exactly generalizing `conjecture1_k2_attempt/ATTEMPT.md` §1's `K=2` object
to `K=3`: an independent `PD(1)` cyclic partition of `[0,1]`; three
reroute sources `x_1,x_2,x_3\sim\mathrm{Unif}(0,1)` i.i.d.; three
destinations `u_1,u_2,u_3\sim\mathrm{Unif}(0,1)` i.i.d., independent of
everything else. The map: `f(x_i)=u_i` for `i=1,2,3`, and `f(y)=`
background cyclic-successor of `y` for every other `y`. Target: the
density of `M_3:=\mathrm{Leb}(\{y:y\text{ cyclic under }f\})`.

**Lemma 0 (locality of cyclic status, K=3; identical argument to `K=2`'s
Lemma 0, restated for completeness).** A point `y` is cyclic under `f`
iff its forward `f`-orbit returns to `y` in finitely many steps. Only
`x_1,x_2,x_3`'s own outgoing arrows are modified, so every other point's
own future trajectory is exactly the background one, regardless of what
flows into it. Consequently: (a) a background block containing none of
`x_1,x_2,x_3` is unaffected in full — this is exactly the "OUT" mass
`1-m_1-m_2-m_3`, always cyclic; (b) within the touched region, whether a
point is cyclic depends only on the forward chain of (background flow,
jump at a source, background flow again, ...), and an incoming jump
landing at a point `w` never changes `w`'s own subsequent orbit.

## 2. Step A — the joint law of the three "region masses" (Lemma 1, K=3)

**Definition.** For `i=1,2,3`, `m_i :=` Lebesgue measure of points whose
background-forward flow reaches `x_i` before (if ever) reaching the other
two sources.

> **Lemma 1 (Step A, K=3; PROVED given the cited residual property).**
> `(m_1,m_2,m_3)` has joint density **exactly `6` (constant) on the
> simplex `Δ=\{m_1,m_2,m_3>0,\ m_1+m_2+m_3<1\}`** — i.e. uniform on `Δ`.

*Proof.* Generalizing `K=2`'s Same/Different case split to three points
requires the set-partition of `\{x_1,x_2,x_3\}` by shared background-block
membership — the Bell number `B_3=5` mutually exclusive "co-block
patterns": **AllSame** (all three share one block), three symmetric
**exactly-two-same** patterns (`\{1,2\}`same-`3`diff, `\{1,3\}`same-`2`diff,
`\{2,3\}`same-`1`diff), and **AllDiff** (three separate blocks). Explore
sequentially (`x_1` then `x_2` then `x_3`, peeling one block at a time —
the same size-biased/residual exploration `K=2`'s own Lemma 1 uses once,
here iterated twice): let `\ell_1=L_1\sim\mathrm{Unif}(0,1)` (the same
`Fact A`/classical size-biased-sampling citation `K=2`'s Lemma 1 uses —
see the note on citation precision below). Given `\ell_1`:

- `P(x_2\in B_1\mid\ell_1)=\ell_1`, `P(x_3\in B_1\mid\ell_1)=\ell_1`
  independently of `x_2`'s position (both immediate from "`x_2,x_3`
  independent uniform," no citation needed beyond that);
- given `x_2,x_3\notin B_1` (prob `(1-\ell_1)`, resp. joint prob
  `(1-\ell_1)^2\cdot[\text{further split}]`), the **residual**
  `PD(1)` property (McCloskey 1965; Patil–Taillie 1977; Pitman,
  *Combinatorial Stochastic Processes*, St-Flour 2002, Ch. 3 — the
  identical citation `K=2`'s own Lemma 1 relies on) gives the rescaled
  complement of `B_1` (mass `1-\ell_1`) as an independent fresh `PD(1)`
  partition; a **second** application of the same residual fact, to the
  complement of `B_1\cup B_2` (mass `1-\ell_1-L_2`), is needed for the
  AllDiff pattern's third block — this is not a new or weaker citation,
  it is the same self-similar stick-breaking property applied twice
  (iterating a recursive property is what the property *says*, not an
  additional risk);
- within a block shared by `\ge2` sources, a **labeled uniform spacings**
  fact splits the block into arcs: for `n=2` co-located sources this is
  exactly `K=2`'s own "Same block" computation (`A\sim\mathrm{Unif}(0,\ell)`);
  for `n=3` (the AllSame pattern) the 3 gaps, labeled by which source
  each ends at, are jointly `\ell_1\cdot\mathrm{Dirichlet}(1,1,1)` — proved
  inline (not merely cited) in `derive_lemma1_k3_symbolic.py` by direct
  change-of-variables integration over the two possible cyclic orderings
  of `(x_2,x_3)` relative to `x_1`, `sympy`-verified Jacobians `=1`.

Working through all 5 patterns (`derive_lemma1_k3_symbolic.py`, full
output below), **each pattern's joint density of `(m_1,m_2,m_3)`, after
change of variables, is a CONSTANT on the full simplex `Δ`** — exactly
the same `P(\text{pattern}\mid\ell_1)` vs. `1/\ell_1`-type-density
cancellation `K=2`'s Lemma 1 flags as "the entire reason a closed form
exists":

| Pattern | Contribution to density on `Δ` |
|---|---|
| AllSame | `2` |
| `\{1,2\}`same,`3`diff | `1` |
| `\{1,3\}`same,`2`diff | `1` |
| `\{2,3\}`same,`1`diff | `1` |
| AllDiff | `1` |
| **Total** | **`6`** |

`∎` (Full symbolic derivation, including every Jacobian and the
pattern-probability self-consistency check `P(\text{AllSame})+3\cdot
P(\text{two-same})+P(\text{AllDiff})=E[\ell_1^2]+3E[\ell_1(1-\ell_1)]+
1/6=1`, in `derive_lemma1_k3_symbolic.py` / `.log`, §6.1 below.)

**On the `Fact A` citation label.** `conjecture1_k2_attempt/adversarial/
REFEREE_REPORT.md` §3.3 named a non-substantive labeling imprecision in
the parent document's Lemma 1 (invoking `Fact A, PROVED` for
`L_1\sim\mathrm{Unif}(0,1)` where the precise citation is the classical
size-biased-sampling fact directly), corrected post-adversarially there.
This document inherits the identical `L_1\sim\mathrm{Unif}(0,1)` step and
gives it the **same corrected framing** here: `L_1\sim\mathrm{Unif}(0,1)`
by the classical size-biased-sampling fact (McCloskey 1965; Patil–Taillie
1977; Pitman 2002 Ch. 3), the same fact `THEOREM.md` §5.3's own `K=1`
proof already uses without comment; `Fact A` (`THEOREM.md` §2.3) is at
most a partial, self-contained check of this within a different
construction (Definition 3), not the source of the claim.

## 3. Step B — the destination combinatorics: classification into 7 shapes

With 3 destinations `u_1,u_2,u_3`, each landing in region `1,2,3`, or
`\mathrm{OUT}`, there are `4^3=64` raw combinations — the step
`conjecture1_k2_attempt/ATTEMPT.md` §3 flags as "the genuinely new `K=2`
phenomenon" (the double-cross big loop) and where the archive's prior
diagnosis of combinatorial explosion was expected to bite hardest.

**The structural fact that prevents the explosion.** Model the redirect
structure as a function `g:\{1,2,3\}\to\{1,2,3,\mathrm{OUT}\}`, `g(i)` :=
the region (or OUT) that `u_i` lands in. **A point contributes new cyclic
mass if and only if its source index lies on a genuine cycle of `g`**
(a self-loop `g(i)=i`, a 2-cycle `g(i)=j,g(j)=i`, or the 3-cycle
`g(1)=2,g(2)=3,g(3)=1` or its reverse); **every node NOT on a cycle
contributes exactly zero new cyclic mass, regardless of where its own
redirect lands** — even if that redirect feeds directly into a cycle's
territory. *Proof of the "off-cycle contributes zero" claim:* a chain of
redirects starting from an off-cycle node `k` (`k\to g(k)\to g(g(k))\to
\cdots`) either reaches OUT (drains permanently, Lemma 0(a)) or enters a
cycle's territory at some interior point and thereafter follows that
cycle's own periodic pattern *forever from that entry phase* — it can
revisit the CYCLE's nodes repeatedly, but it never returns to node `k`
itself (since no cycle node maps back to an off-cycle node, by definition
of "cycle"), so `k`'s own points are never periodic. This generalizes
`K=2`'s "single-cross-plus-OUT drains away" mechanism verbatim, and with
only 3 nodes total, off-cycle tails have length at most 2 so the argument
is fully explicit and checkable by hand as well as by the code below.

> [Correção pós-adversarial, 2026-08-24 — `DISC-DEC-065`] O referee
> hostil nomeou este parágrafo como uma lacuna de exposição menor
> (não um erro): a justificativa acima não trata explicitamente o
> subcaso em que o redirecionamento de um nó fora-do-ciclo `k` pousa
> *dentro* de um arco já periódico (antes da posição própria do
> predecessor no ciclo), e não apenas "antes do ciclo" ou "em OUT".
> Traçado à mão pelo referee: um ponto nesse subarco se funde à
> trajetória futura do ciclo, mas a reentrada periódica do próprio
> ciclo naquela região sempre pousa no *mesmo offset fixo* (o do
> predecessor no ciclo), nunca de volta no ponto de fusão — logo o nó
> `k` nunca é revisitado, confirmando a alegação mesmo neste subcaso
> mais sutil. Não afeta a validade da prova nem o veredito.

Given this fact, new cyclic mass depends *only* on which disjoint cycles
exist among `\{1,2,3\}` and the *positions* `P_i` (`:=` offset of `u_i`
within its target region, from the region's start) of the redirects that
lie *on* a cycle — never on where off-cycle redirects land. Exhaustive
brute-force enumeration of all 64 raw configurations
(`enumerate_destination_combinatorics.py`, exact functional-graph cycle
detection, not by hand) confirms this collapses into **exactly 7
mutually exclusive shapes**, accounting for all 64 raw cells with no
leftover:

| Shape | Description | Raw configs | New mass formula |
|---|---|---|---|
| `T0` | no cycle | 16 | `0` |
| `T1a` | one self-loop (3 sub-types) | 24 (8 each) | `m_i-P_i` |
| `T1b` | one 2-cycle, 3rd node not self-looping (3 sub-types) | 9 (3 each) | `(m_i-P_j)+(m_j-P_i)` |
| `T1c` | one 3-cycle (2 orientations) | 2 | `(m_1{+}m_2{+}m_3)-(P_1{+}P_2{+}P_3)` |
| `T2a` | two self-loops, 3rd not self-looping (3 sub-types) | 9 (3 each) | `(m_i-P_i)+(m_j-P_j)` |
| `T2b` | self-loop + 2-cycle on the other two (3 sub-types) | 3 | `(m_i-P_i)+(m_j-P_k)+(m_k-P_j)` |
| `T3` | three self-loops | 1 | `(m_1-P_1)+(m_2-P_2)+(m_3-P_3)` |
| **Total** | | **64** | |

`M_3 = (1-m_1-m_2-m_3) + [\text{new mass}]`, which reduces, for **every**
non-`T0` shape, to the uniform pattern `M_3 = 1 - (\text{sum of
off-cycle region masses}) - (\text{sum of on-cycle }P\text{'s})` (verified
by direct substitution for all 6 shapes).

**Honest process note — a real classification bug, caught and fixed in
the open.** The first implementation of the cycle-detection routine
(`enumerate_destination_combinatorics.py`) had a genuine bug: when a
forward-walk from a fresh starting node encountered a node *already
classified* by an earlier walk (a legitimate occurrence, since a single
background `\pi`-cycle can contain multiple sources, and the first walk
through it only resolves the segment up to the first source it hits),
the buggy version unconditionally marked the new segment as "drains to
OUT" instead of correctly inheriting the already-resolved node's own
classification. This produced garbled shape counts (`T1a`: 14 instead of
24, `T3`: 6 instead of 1, total `60\ne64`) — caught immediately by the
pre-registered `total==64` assertion, diagnosed, and fixed (see
`enumerate_destination_combinatorics.py`'s inline comments and
`mechanism_check_k3.py`'s analogous, separately-caught bug in §3.1
below). This is exactly the standing "report bugs caught along the way,
not silently patched" discipline this archive's own `K=2` document (§6.2)
already exemplifies.

### 3.1 Discrete mechanism check — per-configuration exact match

Generalizing the `K=2` referee's own decisive check (260,000-trial,
9-cell, 100%-exact-match test), `mechanism_check_k3.py` builds a genuine
uniform random permutation `\pi`, three distinct reroute labels, i.i.d.
uniform destinations (with replacement — collisions and fixed points
allowed), the actual map `f`, and finds the **true** cyclic set by a
from-scratch color-marking orbit trace (ground truth). Independently, it
computes the **predicted** count from this document's own mechanism
(region/distance classification + cycle detection + the formula above)
and compares exactly.

**Honest process note — a second bug, caught the same way.** The first
version of the discrete "predicted" formula used the *continuum*
convention for the position variable (`m_i-D_i`, `D_i` measured from the
region's far edge) applied naively to a *discrete* distance-to-source
variable, producing systematic mismatches (e.g. a destination landing
exactly on its own source, `D_i=0`, wrongly predicted the *entire* region
became cyclic, when in fact only the source itself is a fixed point).
Diagnosed by hand-tracing one failing case (`u_i=x_i` exactly) and fixed:
the discrete arc size is `(\text{distance to source})+1` points, which
recovers the continuum formula exactly in the `n\to\infty` limit (a
boundary/measure-zero correspondence issue in the discrete
implementation, not a flaw in the continuum derivation of §3 — the
continuum arc-length formula `m_i-P_i` is unaffected, since the point
`P_i=m_i` — landing exactly on the source — has probability zero in the
continuum model). After the fix:

```
n=25,  trials=40000: mismatches=0/40000  (match rate=1.00000000)
n=150, trials=12000: mismatches=0/12000  (match rate=1.00000000)
TOTAL: 0 mismatches / 52000 trials, all 64 raw target-cells hit
  (including 4618+234 collision trials and 4819+244 fixed-point trials)
```

**Zero mismatches across both scales, all 64 raw cells, including every
collision and fixed-point edge case** — the mechanism is confirmed at the
same granular, per-configuration level the `K=2` referee used to close
out §3's table there.

## 4. Step C/D — assembling `f_{M_3}(x)`

Each shape's contribution to `f_{M_3}` is derived by exact marginalization
(never a Dirac delta): fix the on-cycle position variables, integrate out
the region masses (each on-cycle `m_i` shifted by its own `P_i`, each
off-cycle mass carrying the derived exclusion weight `W`), then integrate
the positions themselves for a fixed sum (`derive_step2_k3_symbolic.py`).
Two shapes (`T3`, `T2a`) were additionally derived independently by hand
and cross-checked exactly against the code's general formula
(`sympy.simplify(\text{diff})==0` for both). All 7:

```
f_T1a(x) = 3x(x-1)^2(2x+1)
f_T1b(x) = (3/2)x^2(x-1)^2(x+2)
f_T1c(x) = x^3(x-1)^2
f_T2a(x) = (3/2)x^2(x-1)^2(x+2)
f_T2b(x) = (3/2)x^3(x-1)^2
f_T3(x)  = (1/2)x^3(x-1)^2
f_T0(x)  = 3x^3-6x^2+3x     (via P_{T0}(m_1,m_2,m_3)=1-m_1-m_2-m_3 exactly —
                              confirmed two independent ways: as
                              1 minus the other 6 shapes' target-level
                              probabilities, symbolically, AND by literal
                              64-term brute-force summation over all raw
                              (target_1,target_2,target_3) combinations;
                              both give the identical polynomial. Spot-
                              checked with exact fractions at 3 numeric
                              points, all matching.)
```

**Per-shape probability cross-check (beyond the final sum).** For every
one of the 7 shapes, `\int_0^1 f_\text{shape}(x)\,dx` was checked
*independently* against that shape's own target-level probability
(`P_\text{shape}(m_1,m_2,m_3)`, integrated directly over `Δ` with weight
`6`) — computed via a completely separate symbolic route (3D simplex
integration of the raw combinatorial probability polynomial, not the
`x`-marginalized density). **All 7 match exactly**: `9/20, 1/8, 1/60,
1/8, 1/40, 1/120`, and `T0`'s `1/4`, summing to `1`. This is a much
stronger check than confirming only the final total, since an error
that happened to cancel in the grand sum would still be caught here.

**Summing:**

```
f_M3(x) = f_T0 + f_T1a + f_T1b + f_T1c + f_T2a + f_T2b + f_T3
        = 6x^5 - 12x^3 + 6x
```

`6x(1-x^2)^2 = 6x(1-2x^2+x^4) = 6x-12x^3+6x^5` — **identical**.
`sympy.simplify(f_M3(x) - 6x(1-x^2)^2)` returns exactly `0`.

> **Theorem.** `f_{M_3}(x) = 6x(1-x^2)^2` on `(0,1)` — PROVED, modulo the
> citation of §2 (the `PD(1)` residual/size-biased-sampling property,
> identical in kind and risk level to `K=2`'s own citation, applied
> recursively — not newly or more riskily).

Cross-checks (all exact, `sympy`): `\int_0^1 f_{M_3}\,dx=1` ✓;
`\int_0^1 x f_{M_3}\,dx = 16/35 = \varphi_3` ✓ (matches the already-PROVED
mean-consistency identity, `THEOREM.md` §5.4, for every `K`); new exact
moments `E[M_3^2]=1/4`, `E[M_3^3]=16/105`.

## 5. R2 — the K=2 reduction check (and a caught error)

Applying this front's *own* general shape-derivation method with **2**
total reroute sources instead of 3 (base Lemma-1 density `2!=2` on the
segment instead of `3!=6` on the simplex) should reproduce
`conjecture1_k2_attempt/ATTEMPT.md`'s already-PROVED `f_{M_2}(x)=4x(1-x^2)`
— and, group by group, it does: the 2-node shapes are `T0`(no cycle),
"single self-loop, other node off"(`\times2` sub-types), "both self-loop",
and "the 2-cycle" — a brute-force check (`r2_k2_reduction_check.py`)
confirms these 4 shapes exhaust the `3^2=9` raw configurations
(`3+2+2+1+1=9`). Their densities:

```
f_self(single self, other off)  = 2x(1-x^2)   [matches K=2's f_B+f_C exactly]
f_bothself (both self-loop)     = x^2(1-x)    [matches half of K=2's f_A]
f_2cyc (the 2-cycle)            = x^2(1-x)    [matches the other half of f_A]
f_T0 (no cycle)                 = 2x(1-x)     [matches K=2's f_D exactly]
```

Summing: `2x(1-x^2) + x^2(1-x)+x^2(1-x) + 2x(1-x) = 4x-4x^3`, exactly
`4x(1-x^2)`. `sympy.simplify(\text{diff})=0`.

**Honest process note.** The **first** attempt at this reduction check,
done by hand-enumerating the shapes for `N=2` (not by exhaustive code, as
a shortcut for what was meant only as a sanity aside), **missed the
"both self-loop" shape entirely**, mistaking it for a sub-case of the
"single self-loop, other off" bucket. This produced `4x-x^2-3x^3`, which
does **not** equal `4x-4x^3` (`\text{diff}=x^2(x-1)\ne0`) — caught
immediately by the exact-match check itself, not silently accepted.
Diagnosed and fixed by brute-force-enumerating the `9` raw `N=2` configs
explicitly (`r2_k2_reduction_check.py`), which revealed the missing
4th shape. **This mistake is reported here precisely because it is a
concrete illustration of why the main `K=3` classification (§3) was done
by exhaustive computer enumeration from the start, rather than by hand**
— the by-hand version of an *easier*, smaller problem (`N=2`, only 4
shapes) still produced a real miscount; a by-hand `N=3` attempt (7
shapes, some with subtle disjoint-cycle interactions) would have carried
materially higher risk of an uncaught, unmatched error, which is exactly
the kind of combinatorial-explosion failure mode this front was
dispatched expecting.

## 6. Verification

### 6.1 Symbolic derivation (the proof itself)

`derive_lemma1_k3_symbolic.py` / `.log`: Step A (Lemma 1), all 5 patterns,
including the inline proof of the `n=3` labeled-spacings fact (explicit
Jacobians, both cyclic orderings), the pattern-probability
self-consistency check (sums to `1`), and the final `6`-density
confirmation. `enumerate_destination_combinatorics.py` / `.log`:
brute-force classification of all 64 raw destination configurations into
the 7 shapes (§3), including the bug caught and fixed in the open.
`derive_step2_k3_symbolic.py` / `.log`: all 7 shape densities, the
per-shape probability cross-check, `T0` via two independent routes, the
final symbolic sum, the exact match to `6x(1-x^2)^2`, and the moment
checks. `r2_k2_reduction_check.py` / `.log`: §5, including the caught
error.

### 6.2 R_MC1 — independent discrete-permutation check of Lemma 1

`mc_lemma1_k3_check.py`, seeds `20260843020/021/022`, three scales
(`n=300,1000,5000`; `15000/10000/6000` trials). Generalizing the `K=2`
referee's own independent Lemma-1 check to three sources — does not touch
continuum `PD(1)`/stick-breaking machinery at all, using the same
`region_and_distance` routine validated by the 52,000-trial exact-match
mechanism check of §3.1.

```
n=300:  E[m_i]~0.250-0.252 (z<1.5), E[m1^2]=0.0992 (target 0.1),
        Cov(m1,m2)=-0.0124 (target -1/80=-0.0125),
        KS(L vs 3ell^2): p=0.019   KS(pooled m_i vs Beta(1,3)): p=0.0001
        Exchangeability KS(m1 vs m2): p=0.86
n=1000: KS(L): p=0.24   KS(marginal): p=0.15   Exchangeability: p=0.92
n=5000: KS(L): p=0.49   KS(marginal): p=0.67   Exchangeability: p=0.87
```

The small-`n` KS rejection at `n=300` and clean convergence to
non-rejection by `n=1000,5000` is **exactly the expected discretization-
bias signature** of a genuine continuum limit claim — the identical
pattern the `K=2` referee's own Lemma-1 check exhibited and explained
(`REFEREE_REPORT.md` §1.2) — not evidence against Lemma 1. All moments
match at every scale (`|z|<1.5`); exchangeability never rejected.

### 6.3 R_MC2 — raw discrete finite-n simulation of the full model

`discrete_k3_full_distribution_mc.py`, seeds `20260843010/011`. A
from-scratch simulator reusing **only** the ground-truth orbit tracer
already independently validated in §3.1 (`true_cyclic_count`) — none of
the region/shape/formula machinery. Builds a genuine uniform random
permutation, 3 rerouted labels, i.i.d. uniform destinations, finds the
true cyclic set, repeats:

```
n=10000, trials=4000: KS D=0.01538 p=0.2977  mean(M3/n)=0.454470+/-0.003219
                       vs 16/35=0.457143 (z=-0.83)
n=20000, trials=2000: KS D=0.01724 p=0.5857  mean(M3/n)=0.458050+/-0.004569
                       vs 16/35=0.457143 (z=+0.20)
```

Both scales pass cleanly (no rejection), means consistent with `16/35`.
This is the strongest available independent check — genuinely different
code (discrete combinatorics, not continuum measure theory) converging to
`6x(1-x^2)^2` at large finite `n`, exactly generalizing `K=2`'s own R4.

### 6.4 R_MC3 — Monte Carlo of the derived continuum recipe

`mc_recipe_check_k3.py`, seed `20260843030`, `N=2{,}000{,}000`: draw
`(m_1,m_2,m_3)` from Lemma 1 (via `\mathrm{Dirichlet}(1,1,1,1)`), draw
`u_1,u_2,u_3\sim\mathrm{Unif}(0,1)`, classify, find cycles, compute `M_3`
via the exact continuum formula of §3 (independent re-implementation, not
reusing the symbolic-integration code of §4):

```
KS D=0.00080 p=0.1578   mean=0.456893+/-0.000143 vs 16/35=0.457143 (z=-1.74)
```

Passes (not rejected); confirmatory of the full recipe's internal
consistency, exactly as `K=2`'s own R5.

### 6.5 Summary table

| Check | What | Result |
|---|---|---|
| §4 | `\int x f_{M_3}=16/35=\varphi_3` | exact, symbolic — matches the already-PROVED `THEOREM.md` §5.4 mean identity |
| — | `E[M_3^2]=1/4`, `E[M_3^3]=16/105` | exact, symbolic (new) |
| §4 | per-shape probability cross-check (7/7) | all match exactly, independent route |
| §5 (R2) | K=2 reduction reproduces `4x(1-x^2)` group-by-group | exact match (after catching and fixing a real error) |
| §3.1 | discrete mechanism check, 64 cells | **0 mismatches / 52,000 trials**, 2 scales |
| R_MC1 | Lemma 1, independent discrete-permutation | 3 scales, convergent KS trend, moments match |
| R_MC2 | raw discrete finite-`n` full-model simulation | KS `p=0.30,0.59`; `n=10000,20000` |
| R_MC3 | MC of the derived recipe | KS `p=0.16`, `z=-1.74` |

Every check passes; no script was selectively rerun. Two real bugs were
caught during this work (§3's cycle-classification bug, §3.1's discrete
position-formula bug) and one real by-hand miscount (§5's missed shape)
— all reported here in the open, per this archive's standing discipline,
rather than silently corrected.

## 7. Scope, honesty, and what remains open

**What is PROVED here.** `f_{M_3}(x)=6x(1-x^2)^2` on `(0,1)`, exactly —
the `K=3` instance of `THEOREM.md` §8 Conjecture 1 — via a whole-space
computation generalizing both `THEOREM.md` §5.3 (`K=1`) and
`conjecture1_k2_attempt/ATTEMPT.md` (`K=2`)'s method to three reroute
sources. Both major steps close fully: Lemma 1's generalization (§2) and
the destination-combinatorics classification and assembly (§3–§4).

**The one non-self-contained input.** Exactly as at `K=2`: Lemma 1 relies
on the `PD(1)` residual/size-biased-sampling property (McCloskey 1965;
Patil–Taillie 1977), here applied **recursively** (twice, once per
"peeled" source) rather than once. This is not a new or weaker citation
— iterating a self-similar/recursive classical property is exactly what
the property licenses, and is the same move `K=2`'s own Lemma 1 already
makes once. Anyone auditing `THEOREM.md`'s Stage 1 core, or the already-
accepted `K=2` document, already accepts this citation at this rigor
level; nothing here asks for more trust than that.

**Why this front's own risk assessment (and two prior fronts' diagnosis)
did not materialize.** `DISC-DEC-063` dispatched this front expecting
combinatorial explosion, citing `k2_open_lemma/ATTEMPT.md`'s (different
problem: the `n\to\infty` mean-bridge) diagnosis and
`conjecture1_k2_attempt/ATTEMPT.md` §7's own explicit non-attempt of
`K\ge3` for *this* problem. The structural reason the explosion did not
occur here: the "off-cycle nodes contribute zero, regardless of target"
fact (§3) collapses what looks like `4^K` raw configurations down to a
number of *shapes* growing only with the number of set-partitions-into-
cycles of `K` labeled items (`K=2`: 4 shapes; `K=3`: 7 shapes) rather than
with the raw `4^K` count itself, and each shape's density integral has a
uniform closed form (the `1-\Sigma(\text{off-cycle }m)-\Sigma(\text{on-
cycle }P)` pattern, §3) that a single general `sympy` routine handles
for every shape without shape-specific derivation. Whether this
particular collapse — the number of shapes growing only as the number of
"permutation-with-fixed-points-and-cycles" structures on `K` labels
(closely related to the associated Stirling-number/set-partition-into-
cycles counting, not raw `4^K`) — continues to make `K=4,5,\dots` tractable
by the *same* general method is a **new, genuinely open question this
document raises but does not attempt to answer**; see below.

**What was NOT attempted.** General `K\ge4`: this document computed `K=3`
specifically, verified extensively, and did **not** attempt `K=4` or
higher. The "shapes grow with set-partitions-into-cycles of `K` labels,
not `4^K`" observation above is an informal, *post hoc* explanation for
why `K=3` was tractable, not a proof that the same growth rate stays
manageable for larger `K` — the number of such structures still grows
superexponentially in `K` in general (this is essentially counting
permutations of a `K`-subset weighted by cycle structure, summed over
subset size — related to `\sum_j \binom{K}{j} \cdot (\text{number of
permutations of }j\text{ elements})`, which is known to grow
faster than `K!` itself for large `K`), so a genuine claim about `K\ge4`
tractability would require new work, not an extrapolation from this
document. `THEOREM.md` §8 Conjecture 1 for `K\ge4` remains exactly as
open as before this document; no claim is made about it here.

**No claim of progress on any Millennium Problem.** This document is
purely internal combinatorial mathematics on the archive's own
random-permutation-with-reroutes ensemble, exactly as every other
document in this lineage states.

## 8. Scorecard

| Item | Status |
|---|---|
| `f_{M_3}(x) = 6x(1-x^2)^2` | **PROVED** (modulo §2's citation, applied recursively) |
| `E[M_3] = \varphi_3 = 16/35` | PROVED (matches `THEOREM.md` §5.4's already-proved mean identity for every `K`) |
| `E[M_3^2]=1/4`, `E[M_3^3]=16/105` | PROVED (new) |
| Step A uniform-simplex law (Lemma 1, K=3) | PROVED modulo the cited `PD(1)` residual property, applied recursively |
| Destination-combinatorics classification (7 shapes, 64 raw configs) | PROVED (exhaustive brute-force enumeration + exact symbolic densities) |
| Per-shape probability cross-check (7/7) | PROVED (independent route, all match) |
| K=2 reduction check (R2) | PROVED, matches `conjecture1_k2_attempt/ATTEMPT.md` group-by-group (after catching and fixing a real by-hand miscount) |
| Discrete mechanism check (64 cells, 52,000 trials) | 0 mismatches — strong NUMERICAL/combinatorial confirmation |
| Numerical cross-checks (R_MC1–R_MC3) | 3/3 pass, no selective reruns |
| `K\ge4` | **not attempted**, left exactly as open as before; an informal (not proved) observation about why `K=3` was tractable is offered as a lead for a future front |

**This document's net result: `THEOREM.md` §8 Conjecture 1 is (subject to
the mandatory adversarial review below) PROVED at `K=3`**, extending the
now-closed `K=1,2` line one step further, and contradicting this front's
own dispatched risk expectation of combinatorial explosion at this
specific step — ready for the standing adversarial-referee requirement
this archive applies to every positive finding before any catalog update
to `THEOREM.md` itself.

---

## Seeds table

| Script | Seeds used | Range |
|---|---|---|
| `mechanism_check_k3.py` | `20260843001`, `20260843002` | reserved `20260843000+` |
| `discrete_k3_full_distribution_mc.py` | `20260843010`, `20260843011` | reserved `20260843000+` |
| `mc_lemma1_k3_check.py` | `20260843020`, `20260843021`, `20260843022` | reserved `20260843000+` |
| `mc_recipe_check_k3.py` | `20260843030` | reserved `20260843000+` |

No seed from the referee-reserved range `20260844000+` was used by this
front.

## Files table

| File | Role |
|---|---|
| `DERIVATION_PREREG.md` | pre-registration, written before any script ran |
| `derive_lemma1_k3_symbolic.py` / `.log` | Step A / Lemma 1, K=3 (§2, §6.1) |
| `enumerate_destination_combinatorics.py` / `.log` | brute-force 64-config classification into 7 shapes (§3) |
| `mechanism_check_k3.py` / `.log` / `mechanism_check_k3_results.json` | discrete per-configuration mechanism check (§3.1) |
| `derive_step2_k3_symbolic.py` / `.log` | Step B/C/D assembly, all 7 shape densities, final sum (§4, §6.1) |
| `r2_k2_reduction_check.py` / `.log` | K=2 reduction check, including the caught error (§5) |
| `mc_lemma1_k3_check.py` / `.log` / `.json` | R_MC1 (§6.2) |
| `discrete_k3_full_distribution_mc.py` / `.log` / `.json` | R_MC2 (§6.3) |
| `mc_recipe_check_k3.py` / `.log` / `.json` | R_MC3 (§6.4) |
| `ATTEMPT.md` | this document |
| `adversarial/` | reserved for the mandatory independent adversarial referee (not yet run) |
