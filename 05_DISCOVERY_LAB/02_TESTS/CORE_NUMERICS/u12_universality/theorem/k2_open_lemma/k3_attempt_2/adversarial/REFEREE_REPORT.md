# REFEREE_REPORT — hostile adversarial verification of `k3_attempt_2/ATTEMPT.md`

> Independent adversarial referee, target:
> `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/ATTEMPT.md`,
> which claims to prove the `K=3` case of `THEOREM.md` §7.4's Open Lemma
> (`φ_n^{(3)}→φ_3=16/35`) via a new "K-uniform Markov chain / transfer-matrix"
> method, plus bonus `K=4,5` closed forms and a `K≥6`-general rate conjecture.
> Reference material read in full before verification: `THEOREM.md` (§1, §2.4, §7.2–§7.5,
> §9, and the dated Estágio-3 addendum), `../ATTEMPT.md` (wave 5's `K=2` proof this
> document builds on and claims to reproduce), and wave 5's own
> `../adversarial/REFEREE_REPORT.md` (read only for expected format/rigor, per task
> instructions — its subject is a different document). Discipline followed: every
> closed form re-derived or independently re-implemented before being trusted; every
> brute-force number claimed by the front was recomputed by code written from scratch
> for this review; every automated-verification claim ("20/20", "matches
> `n9_check.log`") was re-executed, not read off the log file.

## Verdict (read this first)

**SOUND.** After a genuinely hostile, multi-layer attempt to break it — independent
re-derivation of the transition-rule Proposition from first principles including a
deliberate hunt for missing/double-counted edge cases (self-loops at intermediate
walk positions, the a-vs-b bookkeeping asymmetry between π-reached and U-reached
points), an independent symbolic re-solution of the recursion by a *different*
technique (integrating-factor method vs. the front's hockey-stick telescoping) with
direct substitution-into-the-recursion checks, and fresh, independently-coded
exhaustive brute force at every `K` and every `n` value the task named — **no error
was found anywhere in the `K=3` proof.** The `K=3` case of the Open Lemma
(`φ_n^{(3)}→φ_3=16/35`) is honestly labeled PROVED. `K=4` and `K=5` are also
independently confirmed by fresh brute force (not merely trusted from the document),
though — like the front itself says — these are individual finite computations, not
part of a general-`K` proof. The general-`K` rate pattern (§7.2) is correctly and
consistently labeled CONJECTURED throughout, never slipping into "proved" language
anywhere in the document, including its own Scorecard. No overclaiming was found.

This report also independently *executed* (not merely read) every script the front's
§6 cites as evidence, including the ~7.5-minute uncached `n=9` exhaustive brute force
— see §9 below for the re-run transcript, which reproduces the front's claimed
`3385/6804` exactly, at a comparable wall-clock time (`462.5s` here vs. `448.6s`
claimed), confirming the log was not fabricated or stale.

---

## 1. Model/setup fidelity (`ATTEMPT.md` §1) — **SOUND**

**Check performed.** Read `THEOREM.md` Definition 1 (§1, the `M_n(c)` model) and
Definition 4 (§7.2, the fixed-`K`-conditioned model: `π` uniform random permutation,
`K` rerouted indices a uniform random `K`-subset by exchangeability, independent
`U_1..U_K` i.i.d. uniform, `f(i)=U_i` for rerouted `i`, `f(i)=π(i)` otherwise;
`φ_n^{(K)} := E[\#\text{cyclic}/n \mid K_n=K]`) directly from the source document, not
from a paraphrase. Compared word-for-word against `k3_attempt_2/ATTEMPT.md` §1's
restatement ("`π` a uniform random permutation of `[n]`; `U_1,…,U_K` i.i.d.
`Unif[n]`… `f(i)=U_i` for `i≤K`, `f(i)=π(i)` otherwise") — **identical model**, and
identical to wave 5's own `../ATTEMPT.md` §1's restatement of the same thing (which I
also re-read in full, §3's "discrete exploration process" description). The "walk"
description in `k3_attempt_2/ATTEMPT.md` §1 (forward orbit under `f`, jump via `U` at
a source, success iff return to `y0` before any other revisit) is exactly wave 5's
own walk (`../ATTEMPT.md` §3), merely restated to be tracked by state rather than
enumerated by hand — no drift in the model was found.

**Verdict: SOUND**, no discrepancy from `THEOREM.md`'s Definition 1/4 or from wave
5's own walk description.

---

## 2. The Markov chain transition-rule Proposition (`ATTEMPT.md` §2) — **SOUND**

This is the load-bearing claim, so the most adversarial effort went here: an
independent re-derivation from first principles, followed by a deliberate hunt for
edge-case bugs before trusting the formula, followed by a runtime-asserted partition
check on every state actually visited during the `K=1,2,3` computations.

### 2.1 Independent re-derivation

**Non-source step.** By the lazy-revelation fact (any not-yet-revealed `π`-image is
uniform over the `m=n-a` not-yet-assigned range values, regardless of query order —
standard, and already used identically in `THEOREM.md` §7.3 Step 1 and wave 5's
`../ATTEMPT.md` §3), the pool of `m` possible outcomes decomposes into exactly:
`{y0}` (1, success), the `r` unreached sources (continue to `h`, and this π-query
consumes a range value regardless of outcome, hence `a→a+1`), the `b` "poisoned"
points (still unassigned as range values — see below for why — landing on one closes
a cycle not containing `y0`, failure), and the remaining `m-1-r-b` fresh non-source
points (continue, `g` again). **`1+r+b+(m-1-r-b)=m`, exactly** — the partition is
airtight by construction, not merely checked.

**Source step.** `U` is unconstrained (not a range value being consumed at all), so it
partitions the *full* `n` points: `{y0}` (1, success), the `a+b` already-visited
points other than `y0` (**both kinds** — failure, since `U` has no injectivity
constraint the way `π` does, so it genuinely *can* re-land on an already-`π`-visited
point, which is the new failure mode at `K≥2` that has no `K=1` analogue), the `r`
unreached sources (continue to `h`, and — since this is a U-jump onto a point never
before consumed as a range value — `b→b+1`, not `a→a+1`), and the remaining
`n-1-a-b-r` fresh points (continue to `g`, `b→b+1`). **`1+a+b+r+(n-1-a-b-r)=n`**,
exactly.

### 2.2 Why the a-vs-b asymmetry is *necessary*, not arbitrary (deliberate attempt to
find a bug here)

The one place an error would plausibly hide is: does a point visited via a **π**-step
get excluded from the future π-target pool for the *right structural reason*, and is a
point visited via a **U**-jump *correctly retained* in that pool? I checked this by
injectivity, not by trusting the prose:

- A π-reached point `Q` was revealed as `π(y_s)=Q` for some earlier domain point `y_s`.
  Since `π` is a bijection, **no other** domain point can also map to `Q` — so `Q` is
  permanently and correctly excluded from pool `P` (the not-yet-assigned range
  values). Consuming `Q` this way is exactly what `a` counts.
- A U-reached point `Q'` was never used as anyone's `π`-image — drawing `U` is a
  completely separate random variable from `π`, so `Q'`'s status as a *potential
  future π-target* is untouched. It correctly remains in pool `P`, tracked by `b`.
- **The asymmetric case I specifically hunted for:** when the *source-step* recursion
  hits one of the `r` remaining sources via a U-jump, the target-set-principle
  formula adds `+1` to `b` (not `a`) for that newly-triggered source — because it was
  reached by `U`, not `π`, so (per the point above) it genuinely remains available as
  a *future π-target*, a possible later collision. Symmetrically, when the
  *non-source-step* recursion hits a remaining source via a `π`-query, it adds `+1` to
  `a` (not `b`) — because that query already consumed the source as a range value.
  **These two rules are mirror images of each other, and getting the mirror backwards
  in either direction would be exactly the kind of subtle bug this task asked me to
  hunt for.** I checked both directions by hand against the injectivity argument
  above and found the document's assignment correct in both cases.
- **Self-loop edge case (deliberately hunted for a "point falls into no bucket"
  bug).** Can the *current* position itself be a valid outcome of its own next draw
  (a length-1 self-loop)? For a π-step at a currently-*b*-type position (reached
  earlier via U-jump, hence still in pool `P`): yes, `π(y_t)=y_t` is possible, and it
  is correctly captured inside the stated "`b` poisoned points, landing on one is
  failure" bucket, since `b`'s tally already includes the current position itself
  (bookkeeping tracks *how a point was reached*, not "all points except the current
  one" — the current position is folded into whichever of `a`/`b` produced it, once
  reached, exactly like every other visited point). For a π-step at a currently
  *a*-type position: `π(y_t)=y_t` is *impossible* (would require two domain points
  mapping to `y_t`, violating injectivity) — correctly, such a position is excluded
  from pool `P` (`m=n-a` already reflects this), so no spurious extra outcome is
  possible or missing. For `h(0,0,K-1)` (the very first step of `ψ_n^{(K),R}`, current
  position `=y0` itself): `U=y0` is precisely the "1 point, success" bucket — a
  length-1 self-loop at the reference point itself is *correctly* success (the
  reference point is trivially cyclic). **No missing or double-counted outcome was
  found in any of these cases.**

### 2.3 Independent symbolic + numeric confirmation

- `adv_direct_recursion.py` (this review, written from scratch, not derived from
  `markov_direct.py`) implements exactly the two formulas above with a **runtime
  assertion**, on *every* state actually visited, that the non-source partition sums
  to `m` and the source partition sums to `n` — these assertions never fired across
  the full `K=1,2,3`, `n` up to `8` sweep (`adv_direct_recursion.log`), i.e. the
  partition identity was checked computationally at every reachable state, not just
  algebraically in the abstract.
- The same script's output matches this review's own independent brute force
  (`adv_bruteforce.py`, §5 below) **exactly at all 19 tested `(K,n)` pairs** —
  confirms the *transition rules themselves*, independent of any summation algebra.

**Verdict: SOUND.** No missing case, no double-counted case, no asymmetry bug found
after a deliberate, structured search for exactly this class of error.

---

## 3. The telescoping solution (`ATTEMPT.md` §3) — **SOUND**

**Independent re-derivation, by a *different* method than the front's.**
`markov_transfer.py` solves the first-order linear recursion
`g_r(m)=c_r(m)+w(m)g_r(m-1)` via `sympy.summation` applied directly to the
hockey-stick-identity closed form. This review instead re-derives the *same* closed
form from scratch via the **integrating-factor method** for first-order linear
recurrences (`adv_symbolic_recursion.py`, Part A): with `w(t)=(t-j)/t`,
`j:=r+b+1`, the integrating factor `P(m):=\prod_{t=j+1}^m w(t)` was computed via
`sympy.Product(...).doit()` (a structurally different sympy code path than
`sympy.summation`) and its identity with `1/\binom{m}{j}` was verified symbolically
(`difference == 0`) — this is the one fact the whole telescoping method rests on, and
it was not assumed, it was derived and checked.

**Direct substitution into the ORIGINAL recursion (the strongest form of the check
the task asked for).** Using the re-derived integrating-factor formula, this review
built its own independent `K=3` ladder (`g0,h0,g1,h1,g2,h2,g3`) and then — the core of
this section's check — **substituted every one of the 7 resulting closed forms back
into the original defining recursion equations** (typed fresh from the Proposition's
statement, not imported from `markov_transfer.py`'s internal functions) and confirmed
`sympy.simplify(LHS-RHS) == 0` for **all 7 levels** (`adv_symbolic_recursion.py` Part
B, `adv_symbolic_recursion.log`):

```
g0 recursion (r=0, trivial: no h term): RECURSION HOLDS: True
h0 recursion (r=0): RECURSION HOLDS: True
g1 recursion (r=1): RECURSION HOLDS: True
h1 recursion (r=1): RECURSION HOLDS: True
g2 recursion (r=2): RECURSION HOLDS: True
h2 recursion (r=2): RECURSION HOLDS: True
g3 recursion (r=3): RECURSION HOLDS: True
```

This is exactly the check the task specified: not "does some summation procedure
reproduce the target," but "does the claimed closed-form solution actually satisfy
the defining functional equation," verified symbolically (holds identically in `n`
and `b`, not just at sampled integer values).

**Cross-check against the front's own solver.** The resulting `ψ_n^{(3)}`,
`ψ_n^{(3),R}`, and the Lemma-A-recombined `φ_n^{(3)}` from this review's
independently-derived ladder match `markov_transfer.py`'s own output **symbolically,
exactly** (`adv_symbolic_recursion.py` Part D, difference `==0` in all three cases) —
two structurally different sympy solution paths agreeing exactly is strong evidence
neither has an algebra slip.

**Verdict: SOUND.** Re-derived by a different method, and independently confirmed to
satisfy the defining recursion by direct substitution — not merely re-run.

---

## 4. `K=1,2` reproduction claim (`ATTEMPT.md` §4) — **SOUND**

Recomputed `ψ_n^{(1)}`, `ψ_n^{(1),R}`, `ψ_n^{(2)}`, `ψ_n^{(2),R}` using **this
review's own** independently-derived ladder levels `g1,h0,g2,h1` (the same ladder
built and recursion-verified in §3 above — not a second, separate implementation, but
independent of `markov_transfer.py`'s code) and confirmed symbolic equality
(`adv_k1k2_check.py`/`.log`) to wave 5's already-proved formulas:

```
psi_n^(1)   = (4n+1)/(6n)          == 2/3+1/(6n)                 MATCH
psi_n^(1),R = (n+1)/(2n)           == 1/2+1/(2n)                 MATCH
psi_n^(2)   = (8n^2+4n+1)/(15n^2)  == 8/15+4/(15n)+1/(15n^2)     MATCH
psi_n^(2),R = (5n^2+7n+2)/(12n^2)  == (n+1)(5n+2)/(12n^2)        MATCH
phi_n^(1) via Lemma A = 2/3+1/(3n^2)        == THEOREM.md Prop.4  MATCH
phi_n^(2) via Lemma A = 8/15+1/(30n)+7/(10n^2)+1/(5n^3)  == ../ATTEMPT.md SS6  MATCH
```

Also independently confirmed numerically at `n=2..7` (`K=1`) and `n=3..7` (`K=2`),
both `ψ` and `ψ^R`, via a **completely separately written** brute-force enumeration
(`adv_bruteforce.py`, §5) — 22 exact matches, 0 mismatches
(`adv_bruteforce_results.log`).

**Verdict: SOUND.** Reproduced independently, not merely re-read from the document.

---

## 5. The `K=3` closed form itself (`ATTEMPT.md` §5) — **SOUND**

**Symbolic:** confirmed in §3 above (the K=3 closed form is exactly the output of a
solution independently verified to satisfy the recursion).

**Fresh brute force, written from scratch, not `psi_bruteforce_ref.py`.**
`adv_bruteforce.py` was written for this review with a deliberately different
implementation from the front's scripts: cyclic-point test via a visited-set
early-stop walk (not the front's fixed bounded-loop test), success counted as plain
Python integers rather than accumulating `fractions.Fraction` every iteration
(different performance profile — my `n=8` run took `12.4s` vs. the front's claimed
`36.1s`, consistent with a genuinely different implementation, not a copy). **13 hand
unit tests** on `is_cyclic_from` (identity, cycles, fixed points, self-loops, a
composite `n=4` case with both a cyclic and a non-cyclic tail point) were run and
passed before trusting the function on anything (see the transcript embedded in
§7 below and reproducible via the module).

Task explicitly asked for `n=5,6,7`; this review also ran `n=4` and `n=8` for extra
margin:

| `n` | my brute force | closed form | match |
|---|---|---|---|
| 4 | `71/128` | `71/128` | yes |
| 5 | `1333/2500` | `1333/2500` | yes |
| 6 | `187/360` | `187/360` | yes |
| 7 | `4897/9604` | `4897/9604` | yes |
| 8 | `18023/35840` | `18023/35840` | yes |

All 5 exact. Additionally cross-checked against **this review's own** independently
coded direct memoized recursion (`adv_direct_recursion.py`, §2.3 above), `n=4..8`, all
matching (`adv_direct_recursion.log`).

**Verdict: SOUND**, verified both symbolically (recursion-satisfaction) and
numerically (fresh brute force, own code, own unit-tested cyclic-detector).

---

## 6. `φ_n^{(3)}` recombination via Lemma A (`ATTEMPT.md` §5 bonus) — **SOUND**

**Algebra check.** Lemma A's recombination
(`φ_n^{(3)}=(3/n)ψ_n^{(3),R}+(1-3/n)ψ_n^{(3)}`) was re-executed independently in
`adv_symbolic_recursion.py` Part C from this review's own `ψ_n^{(3)}`/`ψ_n^{(3),R)`
(not the front's), giving `(32n^4+5n^3+77n^2+46n+12)/(70n^4)`, symbolically identical
to `ATTEMPT.md`'s claim (difference `==0`) and to `markov_transfer.py`'s own
recombination (Part D).

**Fresh brute force of the RAW Definition-4 average — the strongest available check,
since it uses neither Lemma A nor the generic/rerouted split at all.** `phi_raw()` in
`adv_bruteforce.py` computes `E[\#\text{cyclic points among ALL }n]/n` directly by
summing cyclicity over every point of every `(π,U_1,U_2,U_3)` configuration — a
different code path from `psi_generic`/`psi_rerouted` entirely. Task asked for "at
least one `n` value"; this review ran **four**:

| `n` | my `phi_raw` (fresh brute force) | closed form | match |
|---|---|---|---|
| 4 | `71/128` | `71/128` | yes |
| 5 | `1628/3125` | `1628/3125` | yes |
| 6 | `181/360` | `181/360` | yes |
| 7 | `41327/84035` | `41327/84035` | yes |

All 4 exact (`adv_bruteforce_results.log`).

**Verdict: SOUND.**

---

## 7. `K=4`, `K=5` bonus claims (`ATTEMPT.md` §7.1) — **independently confirmed, not
just spot-checked**

Task asked for "at minimum" one `K=4` spot-check. This review ran the two the front
itself cites, plus the `K=5` point, all via `adv_bruteforce.py`:

| `K` | `n` | my brute force | closed form | match |
|---|---|---|---|---|
| 4 | 5 | `1569/3125` | `1569/3125` | yes |
| 4 | 6 | `196/405` | `196/405` | yes |
| 5 | 6 | `899/1944` | `899/1944` | yes |

All 3 exact (`adv_bruteforce_results.log`). Note these are individual finite-`n`
confirmations, exactly as the front itself frames them (§7.1: "each individually a
complete derivation" — not a general-`K` proof); this review's confirmation carries
the same scope, deliberately, and does not extend the claim any further than the
front already does.

**Verdict: independently confirmed** at every `(K,n)` pair the front cites for
`K=4,5`.

---

## 8. Overclaim audit (`ATTEMPT.md` §7.2–§7.3, Scorecard §9) — **no overclaiming
found**

Read the Executive summary, §7.2's Observation table, §7.3's obstruction discussion,
and every row of the Scorecard (§9) specifically looking for language that would
treat the general-`K` conjecture as settled, or for a status label inconsistent with
what was actually shown.

- §7.2's Observation is explicitly headed "NUMERICALLY VERIFIED for `K=1,…,5`,
  CONJECTURED for general `K`" and the closing sentence of that section is explicit:
  "it is reported as a **CONJECTURE**, not a theorem: no argument below proves it for
  general `K`, only for the five values actually computed." No slippage into
  "proved" language was found anywhere near this claim, including in the Executive
  summary's bullet on the same result.
- §7.3 names the *precise* missing piece (an induction on `r` through the
  telescoping-sum solution, or a generating-function argument) and explicitly states
  neither was attempted — this is more precise, not less honest, than wave 5's
  analogous §7.1/§7.2 in `../ATTEMPT.md` (which named the obstruction only
  qualitatively, "combinatorial explosion").
- Scorecard row 9 ("General-`K` rate conjecture") is labeled **CONJECTURED**, matching
  the body text exactly; row 10 ("obstruction") is labeled **NAMED PRECISELY**, not
  "resolved"; row 11 (literature search) is labeled **NOT ATTEMPTED**, an honest
  admission of scope not covered, matching §8(c)'s own text.
- The document's framing of what it closes relative to `THEOREM.md` ("residual
  condition is exactly `K≥4`... in the fully-verified sense... or `K≥4`... in the
  'proved individually'... sense") was cross-checked against `THEOREM.md`'s own §9
  master gap list and its dated Estágio-3 addendum (which records `K=2` as PROVADO
  and `K≥3` as still ABERTO, written before this `k3_attempt_2` document existed) —
  consistent; no inflation of what `THEOREM.md` itself currently states as open.
- The governance framing in the document's header (`DISC-DEC-027`, front (c),
  `K3-OPEN-LEMMA-ATTEMPT-2`, no lock, no real data) was checked against
  `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`'s `DISC-DEC-027` entry
  (read-only) — matches exactly, including the explicit prior authorization that
  "failing or remaining open is a complete, honest outcome" for this line of work.

**Verdict: no overclaiming found anywhere in the document.**

---

## 9. Re-executing the front's own verification pipeline (not trusting the logs)

Per the task's explicit instruction, every script `ATTEMPT.md` §6 cites was actually
run by this review, and its output diffed or compared against the checked-in logs —
not read as a claim.

**`markov_transfer.py`**, re-run in full: output is **byte-identical**
(`diff` returns nothing) to the checked-in `markov_transfer.log`
(`adversarial/rerun_markov_transfer.log`).

**`verify_all.py --skip-slow`**, re-run in full: **20/20 PASS, 0 FAIL**, identical to
the checked-in `verify_all.log` (`adversarial/rerun_verify_all_skipslow.log`).

**`verify_all.py` (full, including the ~7.5-minute uncached fresh `n=9` brute force)
— re-run from scratch, not skipped, in the background of this review, actually
waited on to completion:**

```
STEP 3: K=3 closed form vs FRESH brute force at n=9 (beyond wave 5)
brute force n=9: 3385/6804  (462.5s)
PASS: psi_n^(3) at n=9 matches fresh brute force
...
TOTAL: 21 PASS, 0 FAIL
ALL CHECKS PASSED.
```

(`adversarial/rerun_verify_all_full.log`, full transcript.) This independently
reproduces `n9_check.log`'s claimed value (`3385/6804`) at a comparable wall-clock
time (`462.5s` here vs. `448.6s` claimed there — consistent with normal machine-load
variance, not evidence of a stale or fabricated log) — this is a **second, fully
independent** execution of the single most expensive claim in the document (the front
ran this once; this review ran it again, from a cold cache, and got the identical
exact fraction).

**Verdict: every automated-verification claim in `ATTEMPT.md` §6 was reproduced by
actually running the code, including the slow step other reviews might reasonably
have skipped.**

---

## Consolidated scorecard (this review's verdict on every row of `ATTEMPT.md` §9)

| # | Claim | Front's status | Referee verdict |
|---|---|---|---|
| 1 | Exact transition rules, general `K` | PROVED | **SOUND** — independently re-derived from first principles, edge cases (self-loops, a/b asymmetry) hunted for and not found, partition-sum verified by runtime assertion on every reachable state (§2) |
| 2 | `g_0(m,b)=1/(b+1)` general symmetry | PROVED | **SOUND** — re-derived, confirmed as the `r=0` case of the recursion-satisfaction check (§3) |
| 3 | Telescoping algorithm correctness | PROVED in general, executed `r=0..5` | **SOUND** — re-derived by a different method (integrating factor vs. hockey-stick), direct substitution into the recursion confirmed symbolically at every level `r=0..3` (§3) |
| 4 | `ψ_n^{(1)}`, `ψ_n^{(2)}` reproduced | PROVED | **SOUND** — reproduced via an independently-built ladder, symbolic and numeric match (§4) |
| 5 | `ψ_n^{(3)} = 16/35+12/(35n)+5/(28n^2)+3/(70n^3)` | PROVED | **SOUND** — symbolic recursion-satisfaction (§3) + fresh brute force `n=4..8` via from-scratch, unit-tested code (§5) |
| 6 | `K=3` Open Lemma: `φ_n^{(3)}→φ_3` | PROVED | **CONFIRMED PROVED** |
| 7 | `ψ_n^{(3),R}` and full rate `φ_n^{(3)}` | PROVED | **SOUND** — symbolic + fresh raw-definition brute force `n=4..7` (§6) |
| 8 | `ψ_n^{(4)}`, `ψ_n^{(5)}` closed forms | PROVED (individually) | **INDEPENDENTLY CONFIRMED** at every cited `(K,n)` (§7) |
| 9 | General-`K` rate conjecture | CONJECTURED | **Correctly labeled** — no overclaiming found (§8) |
| 10 | Precise obstruction to general-`K` proof | NAMED PRECISELY | **Confirmed accurately named**, not resolved by this review either |
| 11 | Literature search | NOT ATTEMPTED | **Confirmed honestly labeled** — this review did not attempt it either (out of scope for a correctness referee check) |

**No item was downgraded.** No item required a correction in the front's favor either
(unlike wave 5's referee report, which found one genuinely under-claimed item — this
document's own §5 already notes it derives `ψ_n^{(3),R}` from first principles
directly, so there was no analogous "fitted, not derived" item left to promote).

---

## Governance discipline check

- No file under `05_DISCOVERY_LAB/00_GOVERNANCE/` was modified (read-only).
- `THEOREM.md`, `../ATTEMPT.md` (wave 5), `ATTEMPT.md` (this attempt),
  `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml` — none modified.
- No git commit made in this session.
- All artifacts of this review are confined to
  `.../k2_open_lemma/k3_attempt_2/adversarial/`, as instructed.
- No AI-model name appears in any file created by this review.

---

## Files produced by this review

All in
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2/adversarial/`:

- `adv_bruteforce.py` — independent, from-scratch exhaustive enumeration (own
  visited-set cyclic-detector, own unit tests, integer-count accumulation) of
  `ψ_n^{(K)}`, `ψ_n^{(K),R}`, and the raw `φ_n^{(K)}` Definition-4 average.
- `adv_bruteforce_results.py` + `.log` — consolidated run of every fresh brute-force
  check in this review: `K=1` (`n=2..7`, both `ψ`/`ψ^R`), `K=2` (`n=3..7`, both),
  `K=3` `ψ` (`n=4..8`), `K=3` `ψ^R` (`n=4..7`), `K=3` raw `φ` (`n=4..7`), `K=4`
  (`n=5,6`), `K=5` (`n=6`) — **38/38 exact matches, 0 mismatches**.
- `adv_symbolic_recursion.py` + `.log` — independent symbolic re-derivation of the
  telescoping solution via the integrating-factor method (Part A), direct
  substitution of every `K=3` closed form into the original recursion (Part B, all 7
  levels verified), cross-check against `ATTEMPT.md`'s claimed closed forms (Part C)
  and against `markov_transfer.py`'s own output (Part D) — all symbolic differences
  `0`.
- `adv_k1k2_check.py` + `.log` — independent recomputation of `ψ_n^{(1)}`,
  `ψ_n^{(1),R}`, `ψ_n^{(2)}`, `ψ_n^{(2),R}` and their Lemma-A recombinations from this
  review's own ladder, confirmed symbolically identical to wave 5's proved formulas
  and `THEOREM.md`'s Proposition 4.
- `adv_direct_recursion.py` + `.log` — independent, separately-coded memoized
  exact-fraction implementation of the transition rules (different memoization
  strategy from `markov_direct.py`, with a runtime partition-sum assertion on every
  state), checked against `adv_bruteforce.py`, `K=1,2,3`, `n` up to `8` — all match.
- `rerun_markov_transfer.log` — this review's own re-run of `markov_transfer.py`,
  byte-identical to the checked-in log.
- `rerun_verify_all_skipslow.log` — this review's own re-run of
  `verify_all.py --skip-slow`, 20/20 PASS, identical to the checked-in log.
- `rerun_verify_all_full.log` — this review's own re-run of the **full**
  `verify_all.py`, including the ~7.5-minute uncached fresh `n=9` brute force, run to
  completion (not skipped): 21/21 PASS, independently reproducing `3385/6804`.

## Final verdict

**SOUND.** The `K=3` case of the Open Lemma, `φ_n^{(3)}→φ_3=16/35`, survives a
genuinely hostile, structured attempt to break it at every layer named in this
review's brief — model fidelity, the transition-rule Proposition (re-derived from
scratch with a deliberate edge-case hunt), the telescoping solution (re-derived by a
different method, verified by direct substitution into the recursion), the `K=1,2`
reproduction (independently reproduced), the `K=3` closed form (verified symbolically
and by fresh from-scratch brute force), the `φ_n^{(3)}` recombination (verified by an
independent raw-definition brute force that uses neither Lemma A nor the split at
all), and the document's own self-verification pipeline (actually re-executed,
including the slow step, not merely read). `K=4` and `K=5` are **independently
confirmed** at every point the document cites, though — exactly as the document
itself says — this is individual finite-`n` confirmation, not a general-`K` proof;
the general-`K` rate conjecture is honestly and consistently labeled conjectural
throughout, with no overclaiming found anywhere in the document.
