# Hostile Referee Report — EXACT-ALGEBRAIC-CLOSURE-ATTEMPT

**Target:** `.../sharp_rate_constants_attempt/exact_algebraic_closure_attempt/ATTEMPT.md`
(wave 26, front b, `DISC-DEC-123`(b))

**Referee:** dedicated hostile session, no script or intermediate file of
the target front read until after independently reconstructing every
headline claim from `THEOREM.md`'s own D3/D4 formulas.

---

## VERDICT: SOUND WITH NAMED ISSUES — ACCEPT for catalogue integration, with two MODERATE findings that should be patched into the write-up before/at integration

The target's central claim — **full exact closure of the K=3 and K=4
sharp finite-`n` rate constants at `M_3`/`M_4` themselves (not the
predecessor's inflated `C_3=1.0088×M_3`, `C_4=1.0365×M_4`), matching
K=2's tier** — **holds up under independent, from-scratch, hostile
reconstruction.** Every headline number the target reports (`M_3`,
`M_4`, their exact quartic minimal polynomials, the factorizations of
`g_3'`/`g_4'`, all four resultant-elimination thresholds, the
exhaustive-window numbers, the wide-range float-grid results) was
independently reproduced by this referee via genuinely separate
constructions and matches to full displayed precision (20–60 digits
in several cases) in every instance. The core diagnostic claim the
mandate specifically asked for — that the "no clean closed form for
the critical point of `g_4`" framing is imprecise, and that the real
obstruction Estágio 46 hit was the sign-positivity of a correction term
breaking its "sum of sups" method, not a radical-solvability issue — is
independently confirmed to be an accurate reading of the predecessor's
own §7.

Two genuine, but non-corrupting, issues were found, both in the single
section the task flagged as highest-risk (§4.5, the K=4 lower-bound
"wrinkle"). Both are named below (F1, F2) at severity MODERATE. Neither
changes the truth of any proved constant or theorem — this referee
independently closed both gaps and confirms the final claimed results
are correct. A third, LOW-severity wording issue (F3) is also named.

---

## 1. Methodology

Per the mandate: `sharp_rate_constants_attempt/ATTEMPT.md` (predecessor,
in full), `THEOREM.md` Estágios 40 (D3), 43 (D4), 46 (predecessor's
integrated write-up), and `DECISION_LEDGER.yaml`'s `DISC-DEC-123` entry
were read in full **before** opening any of the target's own scripts.
`g_3(x)`, `g_4(x)`, `M_3`, `M_4`, their minimal polynomials, and all
four resultant-elimination constructions (K=3 upper/lower, K=4
upper/lower) were independently rebuilt from `THEOREM.md`'s own D3/D4
formulas — transcribed by hand a second time, never copy-pasted from
the target's files — using `sp.Poly(...).real_roots()` throughout (not
`sp.solve`), before the target's own `k3_exact_closure.py` /
`k4_exact_closure.py` were read at all. Only after this independent
reconstruction already matched the target's headline numbers were the
target's own scripts read, to compare methodology and dig into the
one disclosed wrinkle (§4.5) in more depth than a first pass affords.

---

## 2. Item-by-item results

### Item 1 — Transcription check: PASS, independently confirmed

`n·Δ_n(x)` computed symbolically from THEOREM.md's verbatim D3/D4
formulas and its `n→∞` limit taken directly (`sp.limit` and an
independent series-in-`1/n` cross-check) reproduce, with **zero**
symbolic difference:
```
g_3(x) = 3x^6-3x^5-3x^2+3x = 3x(x-1)^2(x+1)(x^2+1)
g_4(x) = -6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x
```
Script: `adv1_transcription_check.py`/`.log`.

### Item 2 — `M_3`, `M_4` exact values and minimal polynomials: PASS

Independently found via `Poly(g_K'.diff, x).real_roots()`:
- `x_3^*` = unique root of `6t^4+t^3+t^2+t-1` in `(0,1)`, `M_3 =
  g_3(x_3^*) = 0.712071558138027808419103234207...` — matches the
  claimed `0.71207155813802780842...` to all 20+ digits shown.
- `x_4^*` = unique root of `12t^4-2t^3+t^2+2t-1` in `(0,1)`, `M_4 =
  g_4(x_4^*) = 0.708718393409321614178660709132...` — matches
  `0.70871839340932161418...` exactly.

Both claimed minimal quartics (`15552t⁴-3355t³-42192t²+181440t-110592`
for `M_3`; `35831808t⁴-49852544t³-220711113t²+556322688t-274710528`
for `M_4`) were **independently confirmed irreducible over ℚ**
(`factor_list`/`is_irreducible`) and confirmed to vanish exactly at the
independently-computed `M_3`/`M_4` (`simplify` → `0`). As a fully
independent cross-check via a *different* SymPy code path,
`sp.minimal_polynomial(M_3, t)` and `sp.minimal_polynomial(M_4, t)`
were called directly (not via the elimination route at all) and
**reproduce the target's claimed polynomials exactly, coefficient for
coefficient.** Script: `adv2_M3_M4_minpoly.py`/`.log`.

### Item 3 — The core diagnostic claim: CONFIRMED, and the target's re-characterization is accurate

Independent factorization:
```
g_3'(x) = 3(x-1)(6x^4+x^3+x^2+x-1)
g_4'(x) = -4(x-1)^2(x+1)(12x^4-2x^3+x^2+2x-1)
```
Both quartic factors (`6x^4+x^3+x^2+x-1`, `12x^4-2x^3+x^2+2x-1`) are
independently confirmed **irreducible over ℚ**
(`adv2b_quartic_irreducibility.py`/`.log`) — an irreducible quartic is
always Ferrari-radical-solvable (degree ≤4 sits below the Abel–Ruffini
boundary), so there is genuinely no Galois-theoretic obstruction at
`K=3,4`. This referee independently re-read the predecessor's own §7
("What did NOT close, precisely") in full: it explicitly attributes the
non-closure at exactly `M_3`/`M_4` to `B(x)` (K=3) / `B(x),B̄(x)` (K=4)
being sign-*positive* on `[0,1]`, breaking the "sum of sups" pointwise
argument — **never** to any radical-form difficulty. The target's claim
that `THEOREM.md`'s own terse Estágio-46 summary ("no clean closed form
for the critical point of `g_4`") is an imprecise compression of the
predecessor's own more careful §7 diagnosis is **accurate** — this
referee independently verified the exact THEOREM.md sentence in
question and confirms it is a looser paraphrase than what the
predecessor's own document actually argued.

### Item 4 — K=3 resultant elimination: PASS, independently reproduced end-to-end

A completely fresh `F_1:=∂_xN(n,x)`, `F_2:=m·D(n)-n·N(n,x)`,
`R:=Res_x(F_1,F_2)`, eliminated against the independently-derived `M_3`
minimal quartic, gives an `S(n)` of degree 148 (the target's own
construction, using an unreduced `D(n)`, gets degree 236 — a different
but equivalent construction, confirming the result is not an artifact
of one particular clearing-of-denominators convention). **Largest real
root: `2.166862253906554925165270`**, matching the target's claimed
`2.1668622539065549252...` to all digits shown. Independently
confirmed: `h(n,1) = 6/((n-1)(n-2))` exactly; boundary crossing
`n_0=4.4455253252736719460` (target: `4.4456...`); `h(5,1)=1/2`;
lower-bound "touches-zero" locus largest real root
`5.9681846046308027719` (target: `5.9682...`); direct per-`n` values
`a(6)=0.45208772547323901782` and `min_x h(5,x)=-0.0088960114122526977709`,
**both matching the target's cited values to every digit shown.**
Additionally verified (new check, beyond the task's explicit list): the
double root responsible for the `n=5.968` threshold sits at
`x≈0.85425...` — genuinely **inside** `[0,1]`, so K=3's lower bound has
no analogue of the K=4 out-of-domain-branch wrinkle (see Item 6).
Scripts: `adv3_k3_upper_resultant.py`, `adv4_k3_boundary_and_lower.py`,
`adv13...` (inline, folded into this report; see §4 below).

### Item 5 — K=4 upper bound + degree-444 diagnosis: PASS, independently reproduced

Fresh construction (again with a differently-reduced `D(n)`, giving
`S(n)` of degree 324 rather than the target's 444 — same phenomenon as
K=3): `factor_list` independently isolates **the exact same structure**
the target reports — `n^100·(6n²-11n+6)^4·B(n)` with `B` an
**irreducible degree-216 factor** (the target's own construction gets
`n^220` instead of `n^100`, purely from the different `D(n)` convention;
the `(6n²-11n+6)^4` factor and `B`'s degree, 216, match **exactly**).
`B.real_roots()` (6.6–7.7s across two independent runs) finds 12 real
roots, **largest `3.2243805173995860158...`**, matching the target's
claim to every digit. Scripts: `adv5_k4_setup.py`,
`adv6_k4_upper_resultant.py`, `adv6b_k4_upper_Broots.py`.

### Item 6 — THE K=4 lower-bound wrinkle: the mathematical CONTENT and the PATCH are both independently confirmed correct; TWO named issues found in the surrounding narrative/exposition

This was treated as the highest-priority check. Independent, from-scratch
reconstruction (`adv8_k4_lower_wrinkle_resultant.py`):
- `M_4`'s minimal quartic has two real roots, `M_4≈0.70872` and
  `-2.897959841839993074210129`; `minpoly(-M_4)` therefore has real
  roots `-M_4` and `+2.897959841839993074210129` — matches the target's
  cited `+2.8979...` exactly.
- `S_2(n)`'s genuine (multiplicity-free, `n≠0`) factor has degree 220
  (exact match) with **largest real root
  `64.768366227610798420`** (exact match, all digits).
- **Independent exhaustive re-check, `n=6..64`, fresh implementation**
  (`adv7_k4_exhaustive_window_6to64.py`, exact `Poly.real_roots()`
  arithmetic, no reuse of the target's code): **zero violations**,
  worst combined margin `0.0341346693581287858686718687045` at `n=64`
  — matches the target's reported `(0.0341346693581287858686718686958,
  64, 0.6745837240511928283099888, -0.0001007277580519251592757674)`
  tuple to essentially full precision (my computation and theirs agree
  on `hi`, `lo`, and the margin at `n=64` to 25+ digits).

**Named Finding F1 (MODERATE) — the target's causal explanation of the
`n≈64.77` spurious threshold is factually wrong, though the conclusion
and patch remain valid.** The target's `k4_exact_closure.py` (Step 6
comment) and `ATTEMPT.md` §4.5 both state: *"this root does NOT
correspond to an x in [0,1] (it is the OTHER real root of -M4's
minimal quartic, +2.8979..., achieved at x=-0.957, outside [0,1])."*
This referee computed, at **60-digit precision** (`n` taken as the
exact `CRootOf` object, not a truncated decimal, `adv10_branch_check_60dps.py`),
all five real critical points of `h(n,·)` at `n=n_spurious`:

| `x` (critical point) | `h(n,x)` | in `[0,1]`? |
|---|---|---|
| `-0.9569809504181047722...` | `-0.7087183934093216141786607091323450...` | **No** |
| `-0.5830846969276822414...` | `-2.7977569479485247252...` | No |
| `0.3621654212943609862...` | `0.6749943301118803172...` | Yes |
| `0.9838850172211264294...` | `-0.0000313509469880973...` | Yes |
| `0.9894855584264469824...` | `-0.0000286014379908394...` | Yes |

The value at `x≈-0.957` is `-0.70871839340932161417866070913...` —
**this is `-M_4` itself** (matches the independently-computed `-M_4 =
-0.708718393409321614178660709132...` to 30+ significant digits), **not**
`+2.898`. No critical point at this `n` gives anything close to `+2.898`.
The correct, simpler diagnosis is: `h(n,x)`, viewed over *all* real `x`
(not just `[0,1]`), has several critical branches; one of them, sitting
outside `[0,1]`, happens to sweep through `-M_4` exactly at this `n` —
there is no need to invoke "the other conjugate" at all. This does
**not** undermine the mathematical validity of the elimination step or
the exhaustive patch (both independently re-verified correct above) —
it is purely an error in the target's own explanatory narrative of
*why* the spurious threshold appears, worth correcting in the write-up.

**Named Finding F2 (MODERATE) — the written proof does not spell out
the closing argument for integer `n≥65`; a careful reconstruction shows
it does close, but the target's own document leaves the final link
implicit.** Step 6 rigorously shows "no real `x` at all (unrestricted)
achieves `h=-M_4`" only for real `n>64.768...`. The exhaustive patch
(Step 7) covers integers `6..64`. For integers `n≥65`, the target's
document asserts the bound directly from Step 6 alone, but Step 6's
conclusion ("no real `x`, of any kind, anywhere") does not by itself
pin the **sign** of `min_x h(n,x) - (-M_4)` for that unbounded tail — a
continuous function that never *equals* a level can still fail to stay
on one side of it, in general, without an anchor point plus an
Intermediate Value Theorem argument (which the target explicitly gives
for the **upper** bound, via `a(6)`, but not for this lower-bound tail).
This referee reconstructed the missing argument rigorously:
1. Independently confirmed `g_4(x)≥0` on `[0,1]` (its only real roots on
   `[0,1]` are the endpoints, each with multiplicity ≥1 — `real_roots`
   gives `[-1,-1,0,1,1,1]`, no interior roots), which anchors the
   `n→∞` behavior of `h(n,x)→g_4(x)` (a consequence of the `deg_n N =
   deg_n D - 1` fact already used in both scripts' own Step 1).
2. Directly, exactly verified `n=65, 70, 100, 1000` all satisfy
   `min_x h(n,x) > -M_4` with large margins (`adv12_ivt_anchor_gap_check.py`):
   e.g. `min_x h(65,x) = -0.00009601 > -M_4 = -0.70872`.
3. Most importantly: the branch table above already shows that **at
   `n=n_spurious` itself**, restricted to `x∈[0,1]`, the minimum is
   `≈-0.0000314` (nowhere near `-M_4`) — so the single point where
   Step 6's unrestricted-`x` argument is silent (`n=64.768...` exactly)
   is *not* actually a place where the `[0,1]`-restricted minimum comes
   anywhere close to `-M_4` either, closing the continuity argument with
   no remaining gap.

**The final theorem is correct and this referee has independently
verified it holds for `n≥65` too** — but the target's own `ATTEMPT.md`
and scripts do not include this closing step, so as *literally written*
the proof has a narrow, unaddressed logical link for the unbounded tail
`n≥65`. This should be patched (one more anchor computation, e.g. at
`n=65` or `n=1000`, plus a one-line continuity remark, suffices) before
the "EXACT, fully closed" framing is taken at face value for that
specific sub-case.

**Named Finding F3 (LOW) — imprecise "worst margin" labeling.** §4.5's
text attributes the `0.0341` figure to "confirms zero violations of
`h_4(n,x)≥−M_4`... worst margin `0.0341` (at `n=64`)" — but by the
target's own code, `margin := min(M_4-h_max, h_min-(-M_4))`, and at
`n=64` this minimum is realized by the **upper**-bound side
(`M_4-h_max=0.0341`); the lower-bound-specific margin at `n=64` is
actually a comfortable `0.7086`. No effect on correctness — the check
itself correctly verifies both sides — but the prose could mislead a
reader into thinking the *lower* bound is the tight one at `n=64`, when
it is in fact the upper bound that is tight there (a fact already
correctly reported elsewhere in §4.3–4.4).

**Answering the task's explicit question — could the same
"wrong-branch" issue be silently present elsewhere, uncaught?** No.
This referee checked all four resultant-elimination-style constructions
in the document:
- K=3 upper (§3.3): threshold `2.17`, far below the domain start
  (`n≥5`) and below the boundary threshold (`4.45`) that actually
  drives the domain — even if inflated by a spurious-conjugate branch,
  it cannot matter.
- K=3 lower ("touches-zero", §3.4): **structurally immune** — this
  construction targets `m=0` (no external algebraic conjugate to
  confuse with), and this referee additionally verified the double root
  responsible for its `n=5.968` threshold sits at `x≈0.854∈[0,1]`,
  genuinely in-domain, not a spurious branch.
- K=4 upper (§4.3): threshold `3.22`, below the domain start (`n≥6`) —
  harmless even if not perfectly tight.
- K=4 lower (§4.5): the one case where the spurious branch actually
  mattered (threshold inflated past the domain start) — correctly
  caught, and correctly patched (Findings F1/F2 concern the
  *explanation* and *exposition completeness*, not the patch's
  validity, which is independently confirmed).

### Item 7 — Wide-range numeric cross-check: PASS

Fresh, non-symbolic float-grid check (`adv11_float_grid_crosscheck.py`),
`n` from the respective domain start up to `10^5` (integer plus
geometric spacing, `4001`-point `x`-grid): **zero violations** for both
`K=3` (`n≥5`) and `K=4` (`n≥6`); worst ratio `|h|/M_K` approaches `1`
from below as `n→10^5`, exactly as the exact theorems predict
(`0.99998` for K=3, `0.99997` for K=4). The target's own
`independent_numeric_crosscheck.py`/`.log` (read and checked) is
internally consistent with this and correctly labels the below-domain
excursions (`n<n_min`) as expected, not violations.

### Item 8 — Timing/factorization diagnosis (§5.1): directionally confirmed

The **factorization structure** underlying this diagnosis (spurious
`n^k` from clearing denominators at `n=0`, a real-root-free quadratic
factor, and one genuinely irreducible high-degree factor carrying all
the real roots) was independently reproduced exactly (Item 5). The
specific **relative-timing** claim (`count_roots(inf=...)` far slower
than full `real_roots()` on the same polynomial) was spot-checked
(not exhaustively reproduced — the target's own reported times run to
115–590s per attempt, too long to fully replicate here): on the
independently-computed degree-216 `B(n)`, `real_roots()` completed in
`6.55s` while `count_roots(inf=6)` **did not finish within a 30s
bound** (`timeout` killed it, exit 124) — qualitatively consistent
with, though not a full reproduction of, the target's claim. This is a
secondary methodological aside in the target's own document, not
load-bearing for any proved result.

---

## 3. Governance / scope-discipline checks

- **Seed range** `20260934000`–`20260934999`: grep-confirmed unused
  anywhere in `05_DISCOVERY_LAB/` except the reservation notice itself
  and the target's own self-quoted grep output in `ATTEMPT.md`.
- **No randomness used:** grep for `random`/`seed`/`Random` in all
  three of the target's scripts finds nothing except the target's own
  prose disclaimer in `independent_numeric_crosscheck.py`'s docstring.
- **No file outside the target's own directory modified:** all files
  inside `sharp_rate_constants_attempt/` (the predecessor's own
  scripts/logs, e.g. `k2_sharp_rate.py`, `k3_exact_sup_table.txt`, ...)
  carry mtimes from `01:4x`–`02:1x`, well before the target front's own
  work began (`03:3x`+); the predecessor's own `ATTEMPT.md` is untouched
  (mtime `02:30`, before the target front started). **Note:**
  `THEOREM.md`, `DECISION_LEDGER.yaml`, `PROOF_DEPENDENCY_MAP.md`, and
  `DISCOVERY_LAB_STATE.md` were observed with very recent mtimes during
  this review; a content check traced this to the concurrent, unrelated
  **sibling** front of the same wave (wave 26, front (a),
  `K-FREE-CONVERGENCE-BRIDGE-ATTEMPT`, integrated as `THEOREM.md`
  Estágio 47 / `DECISION_LEDGER.yaml` `DISC-DEC-124` while this review
  was in progress) — entirely orthogonal to K=3/K=4 sharp-rate content,
  and **not** attributable to this target front. No new
  `DECISION_LEDGER.yaml` entry touches `DISC-DEC-123`(b)'s own mandate
  text.
- **No `git` command was run** by this referee at any point (per
  instruction); the above checks used only `stat`/`grep`/content
  inspection.

---

## 4. File manifest (this referee's own work)

| File | Role |
|---|---|
| `adv1_transcription_check.py`/`.log` | Item 1: `g_3`,`g_4` re-derived from THEOREM.md's D3/D4, `n→∞` limit two ways |
| `adv2_M3_M4_minpoly.py`/`.log` | Item 2: `M_3`,`M_4` via `real_roots`, minimal-polynomial cross-check via independent `sp.minimal_polynomial` route |
| `adv2b_quartic_irreducibility.py`/`.log` | Item 3: irreducibility of the two `x`-quartics in `g_3'`,`g_4'` |
| `adv3_k3_upper_resultant.py`/`.log` | Item 4: fresh K=3 upper-bound resultant elimination |
| `adv4_k3_boundary_and_lower.py`/`.log` | Item 4: K=3 boundary formula, threshold, touches-zero locus, per-`n` spot checks |
| `adv5_k4_setup.py`/`.log` | Item 5 setup: K=4 `N(n,x)`,`D(n)`, boundary, `M_4` |
| `adv6_k4_upper_resultant.py`/`.log` | Item 5: fresh K=4 upper-bound resultant + `factor_list` |
| `adv6b_k4_upper_Broots.py`/`.log` | Item 5: `B(n)` real roots (largest `3.2244`) |
| `adv7_k4_exhaustive_window_6to64.py`/`.log` | Item 6: fresh exhaustive `n=6..64` check |
| `adv8_k4_lower_wrinkle_resultant.py`/`.log` | Item 6: fresh `S_2(n)` construction, conjugate-root identification |
| `adv9_branch_check_40dps.py`/`.log` | Item 6: first-pass numeric branch check (40 digits) |
| `adv10_branch_check_60dps.py`/`.log` | Item 6: definitive 60-digit branch check underlying Finding F1 |
| `adv11_float_grid_crosscheck.py`/`.log` | Item 7: wide-range float-grid cross-check |
| `adv12_ivt_anchor_gap_check.py`/`.log` | Finding F2: `n=65,70,100,1000` exact checks + independent `g_4(x)≥0` re-derivation, closing the K=4 lower-bound tail argument |
| `adv13_k3_touches_zero_branch.py`/`.log` | Item 4 extra check: confirms K=3's touches-zero double root (`x≈0.854`) is genuinely inside `[0,1]`, unlike K=4's lower-bound wrinkle |
| `adv14_timing_spotcheck.py`/`.log`, `adv14b_countroots_spotcheck.py`/`.log` | Item 8: `real_roots()` (6.55s) vs `count_roots(inf=6)` (>30s, timed out) on the same degree-216 polynomial |

**Dependency note:** `adv6b`, `adv8`, `adv9`, `adv10`, `adv12`, `adv13`,
`adv14`/`adv14b` load pickled intermediates (`k4_Nx_Dn.pkl`,
`k4_R_upper.pkl`, `k4_S_upper.pkl`) that were written to this referee's
session scratchpad by `adv5`/`adv6` and are **not** included here
(scratch artifacts, not part of the permanent record) — each script is
nonetheless a faithful, complete record of what was run, and its exact
output is preserved verbatim in the accompanying `.log`; regenerating
the pickles requires re-running `adv5`→`adv6` first (`adv13` instead
rebuilds `N(n,x)`,`D(n)` directly from THEOREM.md's D3 formula inline,
so it has no pickle dependency).

---

## 5. Summary

| # | Item | Result |
|---|---|---|
| 1 | Transcription (`g_3`,`g_4`) | **PASS**, exact match |
| 2 | `M_3`,`M_4` + minimal polynomials | **PASS**, exact match, cross-confirmed via independent SymPy route |
| 3 | Quartic-factorization / no-Galois-obstruction diagnosis | **CONFIRMED ACCURATE** |
| 4 | K=3 resultant elimination (upper+lower) | **PASS**, exact match to all digits shown |
| 5 | K=4 upper bound + degree-444 factorization diagnosis | **PASS**, exact match to all digits shown |
| 6 | K=4 lower-bound wrinkle (patch) | **PASS** — patch is correct and independently reproduced |
| 6′ | K=4 lower-bound wrinkle (causal narrative) | **F1 (MODERATE)** — wrong conjugate attributed |
| 6″ | K=4 lower-bound wrinkle (proof completeness, `n≥65`) | **F2 (MODERATE)** — closing argument not spelled out; independently supplied here, theorem confirmed true |
| 6‴ | "Worst margin" labeling | **F3 (LOW)** — cosmetic |
| 7 | Wide-range numeric cross-check | **PASS**, zero violations |
| 8 | Timing/factorization diagnosis | **Structure confirmed; timing claim directionally corroborated, not exhaustively reproduced** |
| — | Governance/scope discipline | **CLEAN** (unrelated sibling-front activity explained) |

**Bottom line:** the target's central claim is true and the proofs are
sound. Two MODERATE findings concern the exposition of the single
disclosed "wrinkle" the target itself flagged as the trickiest part of
this front's work — exactly where a hostile referee should look
hardest — and this referee's hardest look confirms the underlying
mathematics survives, while identifying two concrete write-up fixes
(correct the `+2.898`-vs-`-M_4` attribution; add an explicit anchor
point for `n≥65`, e.g. reuse the `n=65` or `n=1000` computation given
here) that should be made before this front's result is presented as a
fully self-contained, gap-free "EXACT" closure.
