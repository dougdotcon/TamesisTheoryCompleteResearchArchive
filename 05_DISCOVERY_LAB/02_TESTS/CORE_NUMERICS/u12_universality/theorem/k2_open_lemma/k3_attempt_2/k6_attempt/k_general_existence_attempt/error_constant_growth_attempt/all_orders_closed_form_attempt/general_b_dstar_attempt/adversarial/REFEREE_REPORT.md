# Hostile-referee report on `general_b_dstar_attempt/ATTEMPT.md`

> **Mandate.** Independent adversarial re-verification of the wave-14 front-(d)
> document claiming, for `p=1,2,3,4` at every `b\ge0`, an exact general-`b`
> closed form for the sharp error constants `D^{*(p)}_r(b)` (Corollary A3 of
> `all_orders_closed_form_attempt/ATTEMPT.md`), via a Teorema-3′-style
> prefactor collapse. Everything below was produced inside this `adversarial/`
> directory. **No file outside it was created, modified, or deleted; no git
> commit was made; no governance file was touched.** Pure combinatorics; no
> external data, no physics, no Millennium-Problem relevance.

> **Reuse discipline.** None of the target's own scripts (`ground_truth.py`,
> `ingredients.py`, `assemble.py`) or their `.log` files were opened, imported,
> or trusted as evidence at any point. Every script in this directory is
> written from scratch: its own unsigned-Stirling table (`own_ground_truth.py`),
> its own Abel-summation-by-parts derivation of `I1,I3,I5,I7` — and, crucially,
> of the fully general odd-power identity that subsumes them
> (`abel_identities.py`) — its own re-proof of the general-`k` prefactor
> collapse (`collapse_proposition.py`), its own interpolation of `Q_p(u)`, its
> own cumulant-generating-function derivation of the central moments of
> `Bin(N,1/2)`, and its own end-to-end assembly of `D^{*(p)}_r(b)` for
> `p=1,2,3,4` (`full_rederivation.py`, `assembled.py`). Two documents were read
> as already-established background, per the mandate: `all_orders_closed_form_
> attempt/ATTEMPT.md` §4.3 (Corollary A3, taken as fixed input, never
> re-derived) and `error_constant_growth_attempt/adversarial/REFEREE_REPORT.md`
> §3.3 (Teorema 3′, the already-PROVED `p=2` case) — the latter's formula is
> used **only** as a comparison target (`crosscheck_teorema3prime.py`), never
> transcribed into any derivation step.

> **Exactness policy.** `fractions.Fraction` / `sympy.Rational` throughout. No
> floating point, no randomness, anywhere in this directory.

---

## Executive summary — verdict: **ACCEPT (SOUND)**

**The document's central claim survives.** I rebuilt the entire route —
Steps 1–4 of its §2, independently, from Corollary A3 alone — without reading
a single line of the target's own scripts, and it reproduces the target's
assembled `D^{*(1)}_r(b)`, `D^{*(2)}_r(b)`, `D^{*(3)}_r(b)`, `D^{*(4)}_r(b)`
exactly, at a scale well beyond what the document itself checked: **165 888
exact independent checks in this directory, 0 mismatches**, plus symbolic
(non-numeric, fully general-`r`,`b`) proofs of the general-`k` prefactor
collapse for `k=0..15` and of the general-power parity fact underlying
`I5`/`I7` for exponents up to `40` (i.e. `k` up to `21`). No counterexample was
found anywhere I tried — including several the document did not itself probe
(`b` up to `150` against `r` as small as `0`, `r` up to `800` against small
`b`, and every `r<p` boundary out to `p=8`).

**The two things the document's own §7 flags as most attackable both hold up
under independent re-derivation:**

1. **§3.3, the `I5`/`I7` Abel-summation-by-parts step.** I redid the
   summation by parts from scratch (`S_5(N,m)=\sum(N-2i)^4[A(i)-A(i-1)]`,
   telescoped by hand, not copied) and it produces **exactly** the document's
   printed intermediate polynomial (`y^4-(y+2)^4=-8w^3-8w` in `w`, confirmed
   both by hand and by `sympy.expand`) and exactly the document's final `I5`
   closed form. Same for `I7`. This part of the document is correct as stated.
2. **§3.4, the general-`k` collapse, especially the `r<k` edge case.** Redone
   by hand (the `N-r-1=r+b` step checked as an algebraic identity, not
   assumed) and then checked at `r<k` specifically and exhaustively — `13 325`
   cases, `0` failures, plus the `k\ge N` degenerate case, plus a **symbolic**
   proof for general `r,b` at `k=0,\dots,15` (the document only went to `k=3`
   symbolically). Correct as stated, and more general than claimed.

**One finding worth flagging prominently — not an overclaim, the opposite.**
Item 11 of the scorecard ("General-`p` closure … OPEN — mechanism exhibited at
`k=2,3` only, not proved in general") is not false, but it **understates**
what the document's own machinery already gives. Redoing the `I5`/`I7`
derivation for **general** `k` (not just `k=3,4`) shows the "even-`w`-terms
cancel" step is not a coincidence checked twice — it is a one-line consequence
of the binomial identity `(w-1)^{2n}-(w+1)^{2n}=-2\sum_{t\text{ odd}}\binom{2n}{t}w^{2n-t}`
(only odd powers of `w` ever appear, for **every** even `2n`), which I have
now verified symbolically for exponents up to `40` and numerically (against
brute-force summation, no recursion) for the full recursive `S_{2k-1}` family
up to `k=11` (power `21`), `0` mismatches. Combined with the fact that the
general-`k` collapse (§3.4, item 6) and the central-moment derivation (§3.2,
via a Taylor-series extraction that is not degree-limited) were *already*
general in the document, this means every ingredient needed for a fully
general-`p` closed form is now established — closing item 11 would be a
mechanical (if tedious) write-out, not a new idea. I did **not** carry out
that write-out for `p\ge5` myself (no explicit `Q_5,Q_6,\dots` polynomials or
assembled formulas were produced here), so I am not promoting `p\ge5` to
PROVED — but the document's own "OPEN, not proved for general `k`" is,
strictly, an underclaim, and I record the one-line proof below (Part 1) so a
future front does not have to rediscover it.

**No errors found in the assembled formulas, the four `p=1..4` general-`b`
theorems, or the printed `b=2,3` concrete instances.** The one self-disclosed
error (§4.5) checks out exactly as described: the wrong intermediate formula
does give `-3/40` at `r=1`, the corrected one gives `1/20`, and `1/20` is the
true ground-truth value — the fix was applied correctly, nothing new broke.

---

## Part 1. Re-deriving `I5` and `I7` from scratch — and finding they generalize

### 1.1 The derivation, redone by hand

Following the document's own recipe (§3.3): with `A(i):=(i+1)\binom N{i+1}`,
the identity `A(i)-A(i-1)=(N-2i)\binom Ni` is elementary (telescoping the
definition of `A` against I1). Writing `g(i):=(N-2i)^{2k-2}`, standard
summation by parts gives, for `S_{2k-1}(N,m):=\sum_{i=0}^m(N-2i)^{2k-1}\binom Ni`:

`S_{2k-1}(N,m)=g(m)A(m)-\sum_{i=0}^{m-1}A(i)\big[g(i+1)-g(i)\big]`,
`\;A(-1)=0`.

With `j:=i+1`, `y:=N-2j`, `w:=y+1=N-1-2i`, and `jB_j=N\binom{N-1}{j-1}`
(`B_j:=\binom Nj`), the tail sum becomes `N\sum_{l=0}^{m-1}\binom{M}{l}\,\Delta g`,
`M:=N-1`, `\Delta g=y^{2k-2}-(y+2)^{2k-2}=(w-1)^{2k-2}-(w+1)^{2k-2}`.

**The key fact, general in `k`.** For any exponent `n=2k-2` (even, for
**every** `k\ge1`):

`\displaystyle(w-1)^{n}-(w+1)^{n}=\sum_{t=0}^n\binom nt w^{n-t}\big[(-1)^t-1\big]=-2\sum_{t\text{ odd}}\binom nt w^{n-t}`,

because `(-1)^t-1=0` for every even `t`. **Only odd powers of `w` survive —
for every even `n`, not just `n=4,6`.** This is what the document calls
"checked symbolically … looks mechanical" (§7); it is in fact a one-line
consequence of the binomial theorem, requiring no case-by-case check at all.
Substituting back and reindexing `s:=n-t` (odd, ranging `1,\dots,n-1`):

> **Proposition (general `k`, re-derived, not in the target document).**
> `\displaystyle S_{2k-1}(N,m)=(N-2m)^{2k-2}(m{+}1)\binom N{m+1}+2N\!\!\sum_{s\text{ odd},1\le s\le 2k-3}\!\!\binom{2k-2}{s}\,S_s(N{-}1,m{-}1)`,
> base case `S_1(N,m)=(m+1)\binom N{m+1}`.

At `k=3` this gives `S_5(N,m)=(N-2m)^4(m{+}1)\binom N{m+1}+8N[S_3(N{-}1,m{-}1)+S_1(N{-}1,m{-}1)]`
(coefficients `\binom41=\binom43=4`, `2N\cdot4=8N`) — **character for character
the document's `I5`**. At `k=4`: `\binom61=\binom65=6`, `\binom63=20`, giving
`+N[12S_5+40S_3+12S_1]` — **character for character the document's `I7`**.
Both were also confirmed independently by direct `sympy.expand` on
`y^4-(y+2)^4` and `y^6-(y+2)^6` (`abel_identities.py::symbolic_I5_I7_deltaf`),
matching the document's printed `-8w^3-8w` and `-12w^5-40w^3-12w` exactly.

### 1.2 Verification scale (this directory)

| check | scope | result |
|---|---|---|
| general recursion vs. brute-force direct summation (no recursion) | powers `1,3,\dots,21` (`k` up to `11`), `N\le27`, every `m` | `4774` checks, `0` mismatches |
| document's exact `I5`,`I7` formulas vs. brute force | `N\le45`, every `m` | `2254` checks, `0` mismatches |
| symbolic parity fact `(w-1)^n-(w+1)^n` has zero even-degree coefficients | `n=2,4,\dots,40` (`k` up to `21`) | `20/20`, `0` failures |
| symbolic `\Delta f` expansion vs. document's printed polynomials | `I5`, `I7` | exact match, both |

The document verified `I5` to `N\le39` and `I7` to `N\le34` at the two
concrete instances it needed; this directory verifies the **general-`k`**
statement (of which `I5`,`I7` are two special cases) up to `k=11`, plus a
symbolic proof of the structural step for `k` up to `21`.

---

## Part 2. The general-`k` prefactor collapse (§3.4), re-derived

### 2.1 Re-proof, step by step

`P_b\cdot[N]_k\cdot(r{-}k{+}1)\cdot\binom{N-k}{r-k+1}`. Using `[N]_k(N-k)!=N!`:

`=P_b\cdot N!\cdot(r{-}k{+}1)/[(r{-}k{+}1)!(N{-}k{-}(r{-}k{+}1))!]=r!(r{+}b)!(r{-}k{+}1)/[(r{-}k{+}1)!(N{-}r{-}1)!]`.

`(r{-}k{+}1)/(r{-}k{+}1)!=1/(r{-}k)!`, and the fact that must carry the whole
argument — `N-r-1=r+b` — is a **direct algebraic consequence of `N=2r+b+1`**,
not an assumption: checked as its own identity, `40 401` cases (`r,b\le200`),
`0` failures. That makes `(N{-}r{-}1)!=(r{+}b)!`, cancelling the `(r{+}b)!` in
the numerator and leaving `r!/(r{-}k)!=[r]_k`. `\blacksquare` — same proof as
the document's, independently reconstructed.

### 2.2 The `r<k` edge case, and beyond

With the standard convention `\binom nk=0` for `k<0` or `k>n`, and
`[r]_k=r(r{-}1)\cdots(r{-}k{+}1)` naturally containing a zero factor whenever
`0\le r<k`, both sides vanish for `r<k` **for two independent reasons**
(the explicit `(r-k+1)` factor and/or the binomial convention), not by an
ad hoc convention layered on top. Checked exhaustively, `k\le25`, `b\le40`,
every `r<k`: `13 325` cases, `0` failures. Also checked the further-out
degenerate case `k\ge N` (so `[N]_k` itself contains a zero factor):
`1232` cases, `0` failures.

### 2.3 Scale

| check | document's scale | this directory's scale |
|---|---|---|
| numeric sweep | `k\le6,b\le8,r\le15` | `k\le20,r\le80,b\le40` (`69 741` checks) |
| symbolic, general `r,b` | `k=0,1,2,3` | `k=0,\dots,15` (`16` values, all `0` residual) |
| `r<k` edge case | not isolated | `13 325` dedicated checks, `0` failures |
| `k\ge N` degenerate case | not checked | `1232` checks, `0` failures |

**Verdict: PROVED, confirmed, and pushed well past the document's own scale.**

---

## Part 3. Full independent assembly, `p=1,2,3,4`, general `b`

### 3.1 Independent ground truth

`own_ground_truth.py` implements Corollary A3 from its own unsigned-Stirling
recurrence (`c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k)`), never touching the target's
`ground_truth.py`. Matches every PROVED calibration formula quoted in the
document — `p=1,2` at `b=0`, `p=1,2,3,4` at `b=1` — exactly, `r=0,\dots,199`
(`1240` checks, `0` failures).

### 3.2 Rebuilding Steps 1–4 independently

- **Step 1** (`c_j^{(r)}(b)=P_b\binom N{r-j}`, extension-for-free): re-derived
  and checked against ground truth directly, `p\le6,r\le40,b\le15`
  (`4592` checks); the "added terms vanish" claim checked on its own,
  `p\le10,r\le40` (`1870` checks). All `0` failures.
- **`Q_p(u)`**: interpolated from `2p+1` points of *my own* Stirling table,
  then checked at `25` further out-of-sample points per `p`, `p\le6`
  (`175` checks, `0` failures) — independently reproduces the document's
  degree-`2p` claim and its printed `Q_1,\dots,Q_4`.
- **Central moments `\mu_2,\mu_4,\mu_6,\mu_8`**: re-derived via my own
  cumulant-generating-function extraction (`sympy.series` on
  `\exp(N\log\cosh(t/2))`), verified by direct summation `N\le25`
  (`130` checks, `0` failures) — the polynomials produced are character-for-
  character the document's `\mu_2,\mu_4,\mu_6,\mu_8`.
- **Odd-part collapse** (`Pcollapse(power,r,b):=P_b\cdot S_{power}(N,r)`):
  built purely from the general-`k` recursion of Part 1 plus the general-`k`
  collapse of Part 2, checked against brute force, `power\le13,r\le25,b\le15`
  (`2912` checks, `0` failures), and its `k=1,2,3,4` instances checked to
  match the document's printed intermediate brackets **exactly** (all four,
  symbolically, `sympy.simplify` residual `0`).
- **Step 2/3 isolation** (substitution + even/odd split + reflection,
  *excluding* the odd-part collapse machinery): reconstructed
  `\sum_{\alpha=0}^rQ_p(r-\alpha)\binom N\alpha` from
  `\tfrac12(\text{FullEvenSum}-\text{StripEvenSum})+\text{OddSumRaw(direct)}`
  and checked it equals the direct sum exactly, `p=1..4,r\le30,b\le15`
  (`1984` checks, `0` failures) — isolates and confirms Steps 2–3 independent
  of whether Step 4's recursion is right.

### 3.3 The full assembled `D^{*(p)}_r(b)`, `p=1,2,3,4`, vs. ground truth

| `p` | scope | checks | failures |
|---|---|---|---|
| 1 | `r\le150,b\le25` | 3926 | 0 |
| 2 | `r\le150,b\le25` | 3926 | 0 |
| 3 | `r\le150,b\le25` | 3926 | 0 |
| 4 | `r\le150,b\le25` | 3926 | 0 |

**Total: 15 704 checks, 0 failures** — matching or exceeding the mandate's
target scale (`b` to 20–30, `r` to 100–200) for **all four** `p`, not just
`p=3,4`'s single spot-checked `b=2` point the orchestrating session had
already flagged as thin: this directory checks `b=2,3,4,\dots,25` for
`p=3,4`, i.e. **24 distinct `b\ge2` values**, each over `r=0,\dots,150`.

### 3.4 Document's printed concrete formulas

The five explicit closed forms printed in §4.1–§4.3
(`D^{*(1)}_r(2),D^{*(1)}_r(3),D^{*(2)}_r(2),D^{*(2)}_r(3),D^{*(3)}_r(2)`) were
transcribed exactly and checked against ground truth, `r=0,\dots,300`:
**1505 checks, 0 failures.** Theorem D1 (§4.1's boxed general-`b` formula for
`p=1`) checked directly, `r\le149,b\le29`: **4500 checks, 0 failures.**

### 3.5 Edge-case / counterexample hunt

| probe | scope | result |
|---|---|---|
| `r<p` (empty Corollary-A3 sum ⇒ must be `0`) | ground truth: `p\le8`; assembled: `p\le4`; `b\le15` | `896` checks, `0` failures, `0` nonzero |
| `r=p` (first nonzero term) | `p\le4,b\le15` | `144` checks, `0` failures |
| `b=0` boundary | `p\le4,r\le200` | `804` checks, `0` failures |
| large `r` (`r=300,500,800`), small-to-mid `b` | `p\le4,b\in\{0,1,2,5,10,20,40\}` | `84` checks, `0` failures |
| `b\gg r` (e.g. `r=0..4`, `b` up to `150`) | `p\le4` | included in the `144`-case ad hoc sweep, `0` failures |
| `r\gg b` (e.g. `r` up to `200`, `b\in\{0,1\}`) | `p\le4` | `0` failures |

No counterexample found anywhere. I specifically tried the cases the document
itself did not report checking (`b` up to `150`, `r=0`; `r` up to `800`) and
they all hold.

---

## Part 4. Cross-check against the already-PROVED `p=2` result (Teorema 3′)

`error_constant_growth_attempt/adversarial/REFEREE_REPORT.md` §3.3's Teorema
3′ was transcribed exactly (formula only, never its derivation) and checked
two ways: against my own Corollary-A3 ground truth, and against this front's
independently-assembled `p=2` formula. `r\le100,b\le20`: **2121 pairs, 0
mismatches either way** — confirming §4.2's claim that this front
"independently re-derives" the already-PROVED Teorema 3′, and additionally
confirming Teorema 3′ itself still matches Corollary A3 (a re-check of a
previously-PROVED result, not required by the mandate but cheap and useful).

---

## Part 5. The self-disclosed error (§4.5)

Reconstructed both the wrong and the corrected formula exactly as the
document describes: coefficient of `\varphi_r` unchanged
(`(r{+}2)(r{+}3)/(2(2r{+}3))`), wrong remainder `-(3r{+}4)/(4(r{+}1))`, correct
remainder `-(r{+}2)/(2(r{+}1))`. At `r=1`: wrong total `=-3/40`, correct total
`=1/20`. Ground truth (`own_ground_truth.py::D_star(1,1,2)`) `=1/20` exactly.
**The document's account is accurate, and the fix was applied correctly** —
nothing was silently reintroduced while "correcting" the disclosed slip
(consistent with the `p=1,b=2` line in Part 3.3's 3926-check sweep, which
passes for every `r`, not just `r=1`).

---

## Part 6. Item 11 of the scorecard — accurately characterized?

**Not an overclaim.** The document never states or implies that `I9,I11,\dots`
have been derived, and correctly restricts every PROVED label to `p\le4`.

**A mild underclaim, documented above (Part 1).** The "mechanism … looks
mechanical, but is not proved for general `k`" framing (§7) undersells the
document's own result: the cancellation is not merely observed at two
instances, it follows in one line from a binomial-theorem parity fact that
holds for every even exponent. I record this because a future front closing
`p\ge5` should not have to rediscover it — but I emphasize this directory did
**not** carry the full `p\ge5` assembly through (no `Q_5,Q_6,\dots`, no
`\mu_{10},\mu_{12},\dots`, no assembled formula for `p\ge5` was produced), so
"general-`p` closure" itself remains, honestly, not fully executed — only the
one identified obstruction (item 11) is now known to be removable.

---

## Scorecard (this referee's)

| # | Claim | Document's label | This referee's independent check | Verdict |
|---|---|---|---|---|
| 1 | `c_j^{(r)}(b)=P_b\binom N{r-j}`, extension-for-free (Step 1) | PROVED | re-derived + `6462` checks, `0` fail | **CONFIRMED** |
| 2 | `Q_p(u)` degree `2p`, vanishes `u<p` | PROVED | own interpolation, `175` out-of-sample checks | **CONFIRMED** |
| 3 | Substitution `u=-(v+\beta/2)`, even/odd split + reflection (Steps 2–3) | PROVED | isolated reconstruction, `1984` checks, `0` fail | **CONFIRMED** |
| 4 | `I1,I3` | PROVED (referee, wave 10) | reproduced as `k=1,2` case of the general recursion | **CONFIRMED** |
| 5 | `I5,I7` (NEW) | PROVED (2 instances) | re-derived by hand + `sympy`; **also generalized to all `k`, `k\le11` verified** | **CONFIRMED, and strengthened** |
| 6 | General-`k` collapse | PROVED, every `k` | re-proved; `r<k` and `k\ge N` edge cases isolated, `14 557` dedicated checks | **CONFIRMED** |
| 7 | Central moments `\mu_2,\mu_4,\mu_6,\mu_8` | PROVED | own cumulant-generating-fn derivation, `130` checks | **CONFIRMED** |
| 8 | `D^{*(1)}_r(b)`, every `b\ge0` (Thm D1) | PROVED | full independent assembly, `3926`+`4500` checks | **CONFIRMED** |
| 9 | `D^{*(2)}_r(b)`, every `b\ge0` | PROVED | full assembly + cross-check vs. Teorema 3′, `3926`+`2121` checks | **CONFIRMED** |
| 10 | `D^{*(3)}_r(b)`, `D^{*(4)}_r(b)`, every `b\ge0` | PROVED | full assembly, `24` distinct `b\ge2` values each, `3926`+`3926` checks | **CONFIRMED (gap from single-`b=2` spot check closed)** |
| 11 | General-`p` closure `I_{2k+1}` | OPEN | the specific named obstruction is **removable** by a one-line parity argument (Part 1); full `p\ge5` assembly not attempted here | **UNDERCLAIMED — obstruction resolved, `p\ge5` still not executed** |
| 12 | Strip sum left as explicit `b`-term sum | OPEN (by design) | not attacked further (mandate did not ask); no closed form found or claimed | **ACCURATELY LABELLED** |
| 13 | Self-disclosed error (§4.5) | disclosed, corrected | wrong/right values reconstructed exactly, correction verified sound | **CONFIRMED** |

**Total independent verification in this directory: 165 888 exact numeric
checks (`fractions.Fraction`/exact integer arithmetic, `0` mismatches),
plus symbolic (`sympy`, general `r,b`) proofs of the collapse identity for
`k=0,\dots,15` and of the parity fact underlying `I5`/`I7` for exponents up
to `40`.**

---

## What I tried to break, and whether I succeeded

- Tried to break `I5`/`I7` by re-deriving the Abel summation independently
  rather than trusting "checked symbolically" — it held, and generalizes.
- Tried to break the general-`k` collapse at its flagged weak point (`r<k`)
  with a dedicated, isolated, exhaustive sweep — held, `13 325`/`13 325`.
- Tried degenerate regimes the document did not report checking: `k\ge N`,
  `b\gg r` (`b` up to `150` against `r=0`), `r\gg b` (`r` up to `800`) — all
  held.
- Tried to catch a silently-reintroduced error in the §4.5 "fix" — did not
  find one; the corrected formula passes the full `3926`-check `p=1` sweep.
- Tried to find a case where this front's independently-assembled `p=2`
  formula disagrees with the already-PROVED Teorema 3′ — none found,
  `2121`/`2121`.
- Tried to find an overclaim in item 11 — found the opposite (an
  underclaim), and verified the removal of the named obstruction myself
  rather than taking the document's "not proved for general `k`" at face
  value.

**I did not succeed in breaking any claim in this document.**

---

## Final verdict

> **ACCEPT — SOUND.** The general-`b` closed forms for `D^{*(p)}_r(b)`,
> `p=1,2,3,4`, every `b\ge0`, are correct. Every load-bearing step (Steps 1–4
> of §2, the `I1,I3,I5,I7` identities, the general-`k` collapse, the four
> assembled theorems, the five printed concrete `b\ge2` instances, and the
> self-disclosed §4.5 correction) was independently re-derived from scratch
> and/or checked at a scale exceeding the document's own, with `0`
> mismatches anywhere. The one issue found is not an error but an
> **underclaim**: item 11 ("general-`p` closure … OPEN") undersells a result
> that follows in one line from the document's own machinery (Part 1, Part
> 6) — this is recorded for the benefit of a future front, not as a defect
> requiring correction before cataloguing. No governance edits, no changes to
> `THEOREM.md`, and no claim beyond `p=1,2,3,4` are made by this report.

---

## Files in this directory

| file | contents |
|---|---|
| `own_ground_truth.py` | independent unsigned-Stirling table + Corollary A3, checked against every PROVED `b=0,1` calibration formula |
| `abel_identities.py` | from-scratch Abel-summation-by-parts re-derivation of `I1,I3,I5,I7`, generalized to arbitrary `k`; symbolic parity proof |
| `collapse_proposition.py` | re-proof of the general-`k` prefactor collapse (§3.4), incl. `r<k` and `k\ge N` edge cases, symbolic general-`r,b` proof |
| `full_rederivation.py` | Step-1 rewrite check, `Q_p(u)` interpolation, central moments (own cumulant-gen-fn derivation), odd-part `Pcollapse` machinery |
| `assembled.py` | full independent assembly of `D^{*(p)}_r(b)`, `p=1,2,3,4`, checked against ground truth at scale |
| `edge_and_document_formulas.py` | document's printed `b=2,3` instances + Theorem D1, plus edge-case/counterexample hunt |
| `crosscheck_teorema3prime.py` | Teorema 3′ (background, already-PROVED `p=2`) vs. own ground truth and vs. this front's assembled `p=2` |
| `step2_3_isolation.py` | isolates Steps 2–3 (substitution + even/odd split + reflection) from Step 4 (odd-part collapse) |
| `*.log` | captured stdout of each script, this run |

Reproduce: `python3 own_ground_truth.py && python3 abel_identities.py &&
python3 collapse_proposition.py && python3 full_rederivation.py &&
python3 assembled.py && python3 edge_and_document_formulas.py &&
python3 crosscheck_teorema3prime.py && python3 step2_3_isolation.py`. Total
runtime well under two minutes.
