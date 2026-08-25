# Hostile referee report — `general_p_dstar_extension_attempt/ATTEMPT.md`

> **Scope.** Wave 15/16 follow-on front hostile-referee pass (`DISC-DEC-066`),
> target: the extension of the general-`p` algorithm for `D^{*(p)}_r(b)` from
> `p=1,\dots,10` (wave 15, verdict SOUND) to `p=11,\dots,20`. Pure
> combinatorics on the Tamesis Discovery Lab's internal ensemble — **no
> Millennium Prize claim of any kind is made anywhere in this report**, no
> external data, no holdout, no real-world claim. Everything below was built
> from scratch in this new `adversarial/` subdirectory. **None of the target
> front's own scripts** (`ground_truth.py`, `ingredients_ext.py`,
> `odd_part_ext.py`, `assemble_ext.py`) **were read, imported, or executed**,
> per the task's discipline; the front's `.log` files were read only as
> *claimed outputs to be verified* (the printed closed forms and check
> counts). Accepted inputs, read in full:
> `general_p_dstar_closure_attempt/ATTEMPT.md`, its
> `adversarial/REFEREE_REPORT.md` (in particular its §1c induction
> `H(\mathrm{power},d)=P_b\,S_{\mathrm{power}}(N-d,r-d)` for every
> `(\mathrm{power},d)`), and `THEOREM.md` "Estágio 16". Nothing outside this
> directory was created, modified, or deleted; no git write command was run
> (a read-only `git status` was used once, see §7). Exact arithmetic
> (`fractions.Fraction` / `sympy.Rational`) throughout; **no randomness
> anywhere** — the reserved referee seed range `20260855000+` was confirmed
> present only in the ledger's/queue's own reservation lines
> (`grep -rn "20260855" 05_DISCOVERY_LAB/`) and was not needed.

## Verdict

**SOUND. ACCEPT for catalogue**, as the executed extension of the
already-proved general-`p` closed-form algorithm for `D^{*(p)}_r(b)` to
`p=11,\dots,20`, in exactly the sense the document claims (execution front,
no new mathematics, two mathematically-identical fast ingredient routes).
No mathematical error was found anywhere: not in the two fast-route
re-implementations, not in the assembly, not in any of the 26 printed
closed forms, not in the self-caught-bug disclosure, not in the claimed
structural signature. Two **minor, non-substantive documentation issues**
are named in §6 (a check-count bookkeeping slip in §3's `ground_truth.py`
tally, and a slightly compressed scorecard row) — neither touches any
mathematical claim, and the second is rendered moot by this report.

**75 899 independent exact numeric checks in this report, 0 mismatches**,
plus one new analytic result: a **proof of the interpolation degree bound
`\deg_r H_{2k-1}(r,b)=k-1`** (leading coefficient `4^{k-1}(k-1)!`,
independent of `b`) — the one load-bearing fact the front itself flagged
(§2.2, §6) as "empirically confirmed but not proved here". With that
proved, every ingredient of the extension is now analytically, not merely
numerically, grounded.

This referee's replication reaches the front's full claimed scale
(`r\le200`, `b\le30`, all ten `p`, the identical `62 310`-point grid) with
completely independent machinery, and **pushes past it to `r=300` at
`p=15` and `p=20`** — the scale-push the front's own §6 suggested —
finding no scale-dependent failure of any kind.

---

## 0. Independence of method (summary)

Every ingredient was rebuilt by a route different from BOTH the front's
fast routes AND the closure attempt's slow routes:

| ingredient | front (fast route) | this referee |
|---|---|---|
| `\mu_{2l}(N)` | power-series-exp recurrence (re-derived here too, §1) | own implementation of the recurrence, **validated against direct binomial summation for every `l=1..20`** (the front's direct-sum check stopped at `l=8`) |
| `H_{2k-1}(r,b)` | evaluate recursion + interpolate (degree `k-1` assumed) | **new closed factorization** `S_{2k-1}(N,m)=A_k(N,m)\binom N{m+1}` → `H_{2k-1}=B_k(2r{+}b{+}1,r)` evaluated directly, no interpolation, no recursion at runtime (§2) |
| `Q_p(u)` | Newton's identities (unchanged from closure) | DP values of `e_p(1..u)` + exact Newton-divided-difference interpolation, with out-of-node extrapolation checks |
| ground truth | own Corollary A3 + Stirling table | **own** Corollary A3, **own** Stirling recurrence, single-common-denominator integer summation |
| final check | `fractions.Fraction` sweep | independent `fractions.Fraction` sweep against the referee's own A3 |

`sp.nsimplify` appears nowhere in this referee's verification call graph
(the sweep code does not even import sympy), by deliberate construction —
see §4.

---

## 1. The fast central-moment route (§2.1 of the target): re-derived, re-implemented, and cross-checked on the orders the front could not

**Re-derivation** (from the same cumulant generating function, one line at
each step): for `X\sim\mathrm{Bin}(N,\tfrac12)` centered,
`M(t)=\cosh(t/2)^N=\exp(N\log\cosh(t/2))`. With
`c(t)=\cosh(t/2)=\sum_j t^{2j}/(4^j(2j)!)`, the log-series recurrence
follows from `c=e^f\Rightarrow c'=f'c\Rightarrow nc_n=\sum_{k=1}^n kf_kc_{n-k}`,
and the exponentiation recurrence from
`g=e^{h}\Rightarrow g'=h'g\Rightarrow mg_m=\sum_{k=1}^m kh_kg_{m-k}` with
`h=Nf`. Both are exactly the classical recurrences the front describes;
`\mu_{2l}(N)=(2l)!\,g_{2l}` is a polynomial in `N` of degree `l`
(confirmed for every `l\le20`, matching the front's log's degree column).

**Independent implementation, independent cross-check**
(`ref_moments.py`): the recurrence route vs **direct binomial summation**
`\mu_{2l}(N)=\sum_k\binom Nk(2k-N)^{2l}/(4^l2^N)` — exact `Fraction`s — for
**every `l=1,\dots,20`** at `N\in\{0..40\}\cup\{101,250,431,631\}`
(`N=431` is the largest `N` in the front's sweep; `N=631` the largest in
this report's scale push): **900 checks, 0 mismatches.**

This closes the one genuine coverage gap in the front's own validation of
this ingredient: the front's direct-summation check stopped at `l=8`, and
its `l=9,10` coverage was fast-vs-slow only, leaving `l=11..20` with no
ingredient-level cross-check other than the end-to-end sweep. Here every
moment order actually consumed by `p=11..20` is checked against the
definition directly. No issue found.

## 2. The fast `H_k` route (§2.2): a third route, and a PROOF of the degree bound

### 2a. A closed factorization of `S_{2k-1}` (new here, from accepted inputs only)

Using only the cited wave-14/15 recursion (accepted input)

`S_{2k-1}(N,m)=(N{-}2m)^{2k-2}(m{+}1)\binom N{m+1}+2N\!\!\sum_{s\ \mathrm{odd},\,1\le s\le2k-3}\!\!\binom{2k-2}{s}S_s(N{-}1,m{-}1)`,

base `S_1(N,m)=(m{+}1)\binom N{m+1}`, define polynomials

`A_1(N,m):=m+1`,
`A_k(N,m):=(m{+}1)\Big[(N{-}2m)^{2k-2}+2\sum_{s\ \mathrm{odd},\,1\le s\le2k-3}\binom{2k-2}{s}A_{(s+1)/2}(N{-}1,m{-}1)\Big]`.

> **Lemma.** `S_{2k-1}(N,m)=A_k(N,m)\binom N{m+1}` for every `k\ge1` and
> every integer `m\ge0` (with the convention `S_s(\cdot,-1)=0`, consistent
> since `(m+1)\mid A_k`).
>
> *Proof.* Induction on `k`. `k=1` is the cited base case. For `k\ge2`,
> apply the recursion; by the induction hypothesis
> `S_s(N{-}1,m{-}1)=A_{(s+1)/2}(N{-}1,m{-}1)\binom{N-1}{m}`; the identity
> `N\binom{N-1}{m}=(m{+}1)\binom N{m+1}` converts the tail into
> `2(m{+}1)\binom N{m+1}\sum_s\binom{2k-2}sA_{(s+1)/2}(N{-}1,m{-}1)`; the
> head is `(N{-}2m)^{2k-2}(m{+}1)\binom N{m+1}`; collecting gives exactly
> `A_k(N,m)\binom N{m+1}`. The `m=0` boundary holds with the empty-sum
> convention. `\blacksquare`

With `(E2)` at `j=0` (accepted; also one elementary line:
`P_b\binom N{r+1}=\frac{r!(r+b)!}{(r+1)!\,(N-r-1)!}=\frac1{r+1}` since
`N-r-1=r+b`), and writing `A_k=(m{+}1)B_k`:

`H_{2k-1}(r,b)=P_b\,S_{2k-1}(N,r)=A_k(N,r)/(r{+}1)=B_k(2r{+}b{+}1,\,r)`

— **manifestly a polynomial in `(r,b)` with integer coefficients.** (This
also re-proves, by an independent route, the polynomiality that the
closure attempt observed via `sympy.cancel` always returning denominator
`1`.)

### 2b. The degree bound, proved

> **Proposition.** For every `k\ge1` and every `b` (symbolic or any fixed
> integer `\ge0`), `\deg_r H_{2k-1}(r,b)=k-1`, with leading coefficient
> `4^{k-1}(k-1)!`, independent of `b`.
>
> *Proof.* For a shift `d\ge0` set `a_k^{(d)}(r):=A_k(N{-}d,\,r{-}d)`,
> `N=2r{+}b{+}1`. Claim: `\deg_r a_k^{(d)}=k` with leading coefficient
> `4^{k-1}(k-1)!` for every `d`. Induction on `k`:
> `a_1^{(d)}=r{-}d{+}1`, degree `1`, lead `1`. For `k\ge2`, the defining
> recursion gives
> `a_k^{(d)}(r)=(r{-}d{+}1)\big[(b{+}1{+}d)^{2k-2}+2\sum_s\binom{2k-2}{s}a_{(s+1)/2}^{(d+1)}(r)\big]`,
> because `(N{-}d)-2(r{-}d)=b{+}1{+}d` is **constant in `r`** — this is the
> decisive structural fact, and it holds at every recursion depth. By the
> induction hypothesis the bracket has degree
> `\max_s\frac{s+1}2=k{-}1`, attained only by the single term `s=2k{-}3`,
> so `\deg a_k^{(d)}=k` and
> `\mathrm{lead}(a_k^{(d)})=2\binom{2k-2}{2k-3}\mathrm{lead}(a_{k-1}^{(d+1)})=4(k{-}1)\cdot4^{k-2}(k{-}2)!=4^{k-1}(k{-}1)!`,
> independent of `d` and of `b`. At `d=0`, `A_k(N,r)=(r{+}1)B_k(N,r)`
> yields `\deg_r H_{2k-1}=\deg_r B_k=k-1` with the same leading
> coefficient. `\blacksquare`

Computationally confirmed (`ref_hk.py`) for `k=1,\dots,20` **with `b`
symbolic**: `(r{+}1)\mid A_k(2r{+}b{+}1,r)`, degree exactly `k-1`, leading
coefficient exactly `4^{k-1}(k-1)!` — all 20 verified, plus the closed
forms `H_1=1` and `H_3=(b{+}1)^2+4r` (matching the closure attempt's
printed `k=2` bracket `-(\beta^2+4r)/8=-H_3/2^3`).

**Consequence for the front's route.** The front's evaluate-then-
interpolate extraction samples the (referee-proved-correct, wave-15 §1c)
recursion at `k` points and fits degree `k-1`. The degree assumption is
now a **theorem**, so the extraction is exact — the front's §6 fourth
bullet and the "empirically confirmed but not proved" caveat of §2.2 are
both discharged analytically.

### 2c. Could a wrong degree guess have passed the self-check? No.

Independently of the proof above: if the degree had been **under**-guessed
by one (fit through `k{-}1` nodes), the discrepancy
`H_{2k-1}-\mathrm{interpolant}` is a degree-`(k{-}1)` polynomial whose
roots are exactly the `k{-}1` nodes (it equals
`4^{k-1}(k{-}1)!\prod_i(r-r_i)`), hence **nonzero at every point off the
nodes** — any single distinct held-out evaluation catches it, with
certainty, not probabilistically. Under-guess by `t`: the discrepancy has
at most `t{-}1` roots off the nodes, so `t` distinct held-out points
suffice deterministically. Over-guess: harmless (interpolating more
points of a lower-degree polynomial returns that polynomial).
Demonstrated numerically (`ref_hk.py`): deliberate under-guessed fits at
`k=5,12,20` disagreed at **12/12** held-out points each, exactly as the
theory requires. The front's self-check design (held-out points at
`\mathrm{offset}+\mathrm{npts}+j+5`, off the nodes by construction) is
therefore a genuine safeguard, not a coincidence-prone one.

### 2d. Direct cross-check of the machine at every `k` used

`H_{2k-1}(r,b)=B_k(2r{+}b{+}1,r)` vs **brute-force**
`P_b\sum_{i=0}^r(N{-}2i)^{2k-1}\binom Ni` (no recursion, no
factorization), `k=1,\dots,20`, `r\in\{0..12,16,20,30,50\}`,
`b\in\{0,1,2,3,5,8,13,30\}`: **2 720 checks, 0 mismatches.** This closes
the ingredient-level coverage gap left by the front (its own brute-force
cross-check stopped at power `21`, i.e. `k=11`; powers `23..39` had no
direct check other than the end-to-end sweep).

## 3. Independent end-to-end verification at (and beyond) the front's full claimed scale

`ref_ground_truth.py`: own Corollary A3 (own unsigned-Stirling recurrence,
single-common-denominator integer summation). Validated against every
PROVED calibration formula used in this lineage's referee tradition —
`p=1,2` at `b=0`; `p=1` at `b=1`; the parent's Theorem D1 instance
`p=1,b=2`; the closure attempt's PROVED `p=4,b=1` row — each at
`r=0..60`, plus the `r<p` vanishing boundary through `p=20` at
`b\in\{0,1,2,7,30\}`: **1 355 checks, 0 fails.**

`ref_assembly_sweep.py`: this referee's own implementation of the accepted
assembly formula, from the referee-built ingredients of §§1–2 (own `Q_p`
by DP + exact interpolation with out-of-node extrapolation asserts; own
`\mu` polynomials; `H` via the `B_k` factorization — no interpolation
anywhere), checked against the referee's own A3:

| stage | grid | checks | fails |
|---|---|---|---|
| calibration gate `p=1..4` | `r\in\{0,1,2,3,7,15,40\}`, `b=0..10` | 308 | 0 |
| **full replication** `p=11..20` | `r=0..200`, `b=0..30` — the front's exact claimed grid, all ten `p`, uniformly | **62 310** | **0** |
| **scale push** `p=15,20` | `r=201..300`, `b=0..30` | 6 200 | 0 |

Total **68 818 checks, 0 fails**, in ~2.5 minutes of referee compute —
independently confirming both the front's headline number (`62 310`
checks at that grid do pass, with completely different code on both sides
of the comparison) and the absence of any scale-dependent failure through
`r=300` (`N=631`) at the largest `p`. The `r<p` boundary region is
included throughout and passes.

## 4. The `nsimplify` disclosure (§2.4): verified on every checkable point

The front's disclosed bug narrative has two independently checkable
claims, and both check out exactly:

1. **The stated true value is true:** this referee's own A3 gives
   `D^{*(3)}_{15}(0)=1143904849/80144052` — precisely the value §2.4
   states (`ref_assembly_sweep.log`).
2. **The corruption is real and exactly as quoted:** in this environment
   (sympy 1.14.0), `sp.nsimplify(Rational(1143904849, 80144052))` returns
   `3\cdot2^{269/341}3^{57/682}5^{290/341}7^{329/682}/4` —
   **character-for-character the spurious expression printed in §2.4**
   (`ref_nsimplify_probe.log`). The bug mechanism (float-based
   algebraic-constant guessing losing precision on a large exact rational)
   is therefore confirmed reproducible, and it is indeed
   `p`-independent/size-triggered as the front says.

The front's further claim that its production
`check_against_ground_truth` never reaches `nsimplify` **cannot be
audited here** (reading the front's code is barred by the task's
discipline). It also does not need to be: every mathematical output the
front claims — the full sweep grid and all 26 printed closed forms — has
been re-derived and re-verified in this report by a pipeline that
provably contains no `nsimplify` (the sweep code never imports sympy at
all). Whatever the front's internal call graph does, its published
results are correct.

## 5. The printed closed forms (§3.3 and `assemble_ext.log`): all 26, two ways

**Numerically** (`ref_printed_forms.py`): every printed form in
`assemble_ext.log` — all twenty `(p,b)` with `p=11..20`, `b\in\{0,1\}`,
and all six `(p,b)` with `p\in\{11,15,20\}`, `b\in\{2,3\}` — parsed
directly from the log (no hand transcription), evaluated with exact
`\varphi_r=4^r(r!)^2/(2r{+}1)!`, and compared to the referee's own A3 at
`r=0..60` and `r\in\{150,200,300\}`: **26/26 forms, 1 664 checks, 0
mismatches.** (This goes beyond the orchestrating session's `p=11`,
`r\le40` verification: different `p` values, the log's forms rather than
only the ATTEMPT's, and `r` up to `300`.)

**Symbolically** (`ref_symbolic_forms.py`): each of the 26 forms was
**reconstructed from scratch** — `\varphi_r`-coefficient as
`M_p(N)\prod_{j=1}^b\frac{2r+2j}{2r+j+1}` (using `(E1)`, itself
re-verified numerically here: 441 checks, `r,b\le20`, 0 fails), remainder
as `-\tfrac12\sum_iE_p(i{-}\beta/2)w_i-\sum_ko_kH_{2k-1}/2^{2k-1}` with
`w_i` from the factorial definition and `H` from the referee's `B_k`
factorization — and compared to the parsed log form as rational functions
(`sympy.cancel` of the difference): **26/26 exact matches.**

**Transcription integrity:** the ATTEMPT's hand-typeset `p=11` block
(`b=0,1,2`, six display formulas) matches the log's machine-printed
forms in its complete ordered integer sequence (136 tokens vs 136,
identical) — no hand-copy slip.

**Structural signature (§3.3's claim), confirmed and explained:** for all
twenty `b\in\{0,1\}` forms the remainder is a genuine polynomial and the
`\varphi_r`-coefficient's denominator is a pure integer (no `(2r{+}3)`);
for all six `b\in\{2,3\}` forms the `\varphi_r`-coefficient's denominator
is exactly `\mathrm{const}\cdot(2r{+}3)` and the remainder denominator is
exactly `\mathrm{const}\cdot(r{+}1)` at `b=2`,
`\mathrm{const}\cdot(r{+}1)(r{+}2)` at `b=3`. The `(2r{+}3)` is exactly
what `(E1)`'s product forces: in
`\prod_{j=1}^b\frac{2r+2j}{2r+j+1}`, odd-`j` denominators are even and
cancel; the first surviving odd factor is `j=2`'s `(2r{+}3)`. (A
referee's note, outside the front's claimed scope: at `b\ge4` the same
mechanism would generically contribute `(2r{+}5)` as well — the front
claims the `(2r{+}3)` pattern only for the `b=2,3` instances it printed,
so no overclaim is involved.)

## 6. Honesty / overclaim review — two minor named issues

The document's framing was read hostilely against its own logs, the
closure attempt, its referee report, and `THEOREM.md`. The
executive-summary numbers, the §3.2 sweep table (row-for-row equal to
`assemble_ext.log`, including check counts and times), the §2.1/§2.2/§2.3
cross-validation counts (`10/10`, `72`, `4/4`, `50/50`, `847`, `225`,
`880`), the timing narrative (§0 vs the logs' timing columns), the "not
claimed" items (§5), and the seed-discipline statements all reconcile
exactly. The `62\,310=10\times201\times31` arithmetic is exact, and the
"same scale for all ten `p`" claim is true (and now independently
replicated). Two minor issues, neither mathematical:

1. **`ground_truth.py` check-count bookkeeping (§3).** The ATTEMPT states
   "`1044+120=1164` checks (see `ground_truth.log`)". The log lists
   *four* check groups: `p=1,b=0` (`r=0..59`), `p=2,b=0` (`r=0..59`) —
   together the `120` — the `r<p` vanishing sweep (`1044`), **and a
   `b=1` calibration line ("p=1,4 b=1 vs PROVED formulas: r=0..79")
   whose checks (at least 160) are omitted from the stated total.** An
   *under*count of its own verification work, so it weakens nothing —
   but the printed total does not reconcile with the document's own log,
   which is exactly the kind of slip a catalogue entry should not
   propagate. Recommended fix: one line in any future integration note.
2. **Scorecard row 2 wording.** "Fast `H_k(r,b)` route … **PROVED given
   the wave-15 referee's `H` induction (cited)**" compresses away the
   fact — stated candidly in §2.2 and §6 of the same document — that the
   route's correctness also needs the interpolation degree bound, which
   was only *empirically* confirmed by the front. The self-check makes a
   wrong degree loudly detectable (§2c above), so the compression is not
   an error in substance, and it is **now moot**: §2b of this report
   proves the degree bound, making the row's "PROVED" accurate
   retroactively (given this report as an additional citation).

Nothing else: the `p>20` frontier discussion (§5) is properly hedged
("suggests, but does not prove"); the distinction between the front's
own verification depth and cited prior depth is drawn correctly
throughout; the self-caught-bug disclosure is complete and, on every
checkable point, verbatim-accurate (§4).

## 7. Discipline notes

- A read-only `git status` (no other git command) was run once, to
  confirm this review's footprint. The working tree contains
  **pre-existing** modifications unrelated to this lineage (one modified
  `ATTEMPT.md` under `conjecture2_direct_attempt/` and several untracked
  `adversarial/` directories of other fronts); none were touched by this
  review. This review created exactly one directory — this one — and
  nothing else.
- `ref_A_cache.pkl` is a regenerable cache of the `A_k` polynomials
  (delete it to force the ~80 s sympy rebuild in `ref_hk.build_A_polys`);
  it exists only to keep re-runs fast and contains no independent claim.
- No `sp.nsimplify`, no floating point, no randomness anywhere in this
  suite; the one *probe* of `nsimplify` (§4) exists precisely to
  reproduce the front's disclosed bug, not to compute anything.

## 8. Summary of this report's checks

| # | Check | Method | Checks | Mismatches |
|---|---|---|---|---|
| 1 | `\mu_{2l}(N)` recurrence (re-derived) vs direct binomial summation, **`l=1..20`**, `N\le631` | own implementation, own derivation | 900 | 0 |
| 2 | `H_{2k-1}` via new `A_k` factorization vs brute-force `P_b S_{2k-1}`, **`k=1..20`**, `r\le50`, `b\le30` | third route, no recursion at runtime | 2 720 | 0 |
| 3 | `\deg_r H_{2k-1}=k{-}1`, lead `4^{k-1}(k{-}1)!`, `b` **symbolic**, `k=1..20` | proof (§2b) + symbolic confirmation | 20 symbolic | 0 |
| 4 | wrong-degree-guess stress test (`k=5,12,20`) | deliberate under-fit vs held-out points | 36 | 0 passes-wrongly (all 36 caught, as theory demands) |
| 5 | own-A3 ground-truth self-checks (5 PROVED formulas + vanishing to `p=20`) | own Stirling table | 1 355 | 0 |
| 6 | calibration gate `p=1..4` (assembly vs A3) | independent end-to-end assembly | 308 | 0 |
| 7 | **full replication `p=11..20`, `r=0..200`, `b=0..30`** | independent end-to-end assembly vs own A3 | **62 310** | **0** |
| 8 | **scale push `p=15,20`, `r=201..300`, `b=0..30`** | same | 6 200 | 0 |
| 9 | all 26 printed closed forms vs own A3, `r=0..60,150,200,300` | parsed from log, exact `\varphi_r` | 1 664 | 0 |
| 10 | all 26 printed forms vs from-scratch symbolic reconstruction; denominator signatures | sympy `cancel` of differences | 26 symbolic | 0 |
| 11 | `(E1)` re-verification, `r,b\le20` | direct factorial arithmetic | 441 | 0 |
| 12 | §2.4 true value + `nsimplify` corruption reproduction | own A3 + direct probe | 1 (+verbatim repro) | 0 |
| 13 | ATTEMPT `p=11` typeset block vs log | ordered integer-sequence comparison | 136 tokens | 0 |

**Total: 75 899 exact numeric checks, 0 mismatches**, plus the degree-bound
proof (§2b), the factorization lemma (§2a), and the self-check
deterministic-detection argument (§2c).

## 9. Net verdict

**SOUND. ACCEPT for catalogue.** The extension front's central claim — the
already-proved general-`p` algorithm, executed for `p=11,\dots,20` via two
mathematically-identical fast ingredient routes, verified at `r\le200`,
`b\le30` uniformly with `0` mismatches, producing 26 new printed closed
forms with the established structural signature — survives a fully
independent, methodologically disjoint re-verification at the same scale
and beyond it (`r=300`), with every attack surface the front's own §6
named now closed: the moment route checked against the definition on
every order used (`l\le20`); the `H_k` machine checked by a third route on
every `k` used and its degree bound **proved**, not assumed; the
interpolation self-check shown to be deterministically sound; the
`nsimplify` disclosure verified verbatim where checkable and made
irrelevant to the results by full independent re-derivation; the printed
forms confirmed numerically and symbolically, all 26. The two named
issues (§6) are documentation-level only; naming them in any integration
note is sufficient. `p>20` remains correctly OPEN and unclaimed by either
document.

**Conditions for integration into `THEOREM.md`:** none beyond standing
conventions, with the suggestion that the integration entry (a) cite this
report's §2a–2b so the `H_k` degree bound enters the catalogue as PROVED
rather than empirical, and (b) correct the `ground_truth.py` check-count
tally per §6 item 1.

## 10. Files, reproducibility

| file | contents | runtime |
|---|---|---|
| `ref_moments.py` / `.log` | own moment recurrence + direct-summation cross-check, `l=1..20` | <1 s |
| `ref_hk.py` / `.log` | `A_k` factorization build, brute-force cross-check `k=1..20`, symbolic degree/lead checks (`b` symbolic), wrong-degree stress test | ~85 s |
| `ref_ground_truth.py` / `.log` | own Stirling table + Corollary A3 + self-checks | ~3 s |
| `ref_assembly_sweep.py` / `.log` | independent end-to-end assembly; calibration; full `p=11..20` replication; `r=300` scale push | ~3 min (+~80 s `A_k` cache build on first run) |
| `ref_printed_forms.py` / `.log` | all 26 log-printed forms vs own A3; ATTEMPT-vs-log token comparison | ~2 min |
| `ref_symbolic_forms.py` / `.log` | `(E1)` re-check; from-scratch symbolic reconstruction of all 26 forms; denominator signatures | ~4 min |
| `ref_nsimplify_probe.log` | §4's verbatim reproduction of the disclosed corruption | <1 s |
| `ref_A_cache.pkl` | regenerable cache of `A_k` polynomials (see §7) | — |
| `REFEREE_REPORT.md` | this report | — |

Reproduce in order: `python3 ref_moments.py`; `python3 ref_hk.py`;
`python3 ref_ground_truth.py`; `python3 ref_assembly_sweep.py`;
`python3 ref_printed_forms.py`; `python3 ref_symbolic_forms.py`.
Total well under 15 minutes. All self-contained; no imports from, and no
reads of, the target front's scripts.
