# Pre-registration — `sharp_constant_attempt` (wave 14, front (a), `DISC-DEC-057`)

Written before any of the verification runs reported in `ATTEMPT.md` are
executed. A small amount of throwaway float/`mpmath` exploration preceded
this (disclosed here, per the archive's own established practice in the
parent document): (1) computed `Q(n)` exactly for `n` up to `1000` and
observed `sqrt(pi n/2) - Q(n) -> 1/3` (consistent with the classical
Ramanujan-`Q` asymptotic expansion, used only to sanity-check the *sign* and
rough *size* of the constant `C` before committing to a derivation, never as
the basis of any claim below); (2) computed `r_K := M_K/sqrt K` exactly for
`K` up to `400` and observed it strictly increasing, always `< a*`, with gap
`a*-r_K` shrinking roughly like `0.33/sqrt K`; (3) tried a handful of
candidate two-term recursions `Q(n) = f(Q(n-1))` and found none holds exactly
(`Q(3)=17/9 != 1+(2/3)Q(2)=2`), which is why the monotonicity piece is
attempted via analytic bounds below, not exact induction on a recursion.
None of this is used as evidence for any PROVED claim; it only shaped which
routes to attempt.

## Task

Wave 14 front (a), per `00_GOVERNANCE/DECISION_LEDGER.yaml` `DISC-DEC-057`
and the parent `u_prime_hypothesis_attempt/ATTEMPT.md` §7's two named gaps:

1. A lower bound `Q(n) >= sqrt(pi n/2) - C` for explicit `C`, via
   `-ln(1-x) <= x/(1-x)`, combined with Theorem 3 and Lemma 4.1 to try to
   upgrade `limsup_K M_K/sqrt K <= a*` (implicit in the parent's Theorem 4
   proof) to `lim_K M_K/sqrt K = a*` exactly.
2. Monotonicity of `M_K/sqrt K` in `K` (or `limsup = lim`), needed to
   upgrade a limit statement into a supremum-over-all-`K` statement.

## Planned derivation (piece 1), fixed before computation

For `0 <= j <= n-1`, using `-ln(1-i/n) <= (i/n)/(1-i/n) = i/(n-i)` for each
`1<=i<=j<n`, summing, and bounding `1/(n-i) <= 1/(n-j)` for `i<=j`:

`-ln P_j <= sum_{i=1}^j i/(n-i) <= j(j+1)/(2(n-j))`, `P_j := prod_{i=1}^j(1-i/n)`.

So `P_j >= h(j) := exp(-phi(j))`, `phi(j):=j(j+1)/(2(n-j))`, for **every**
`0<=j<=n-1` — no truncation needed (unlike the naive approach of restricting
to `j = O(sqrt n)`, which was tried first on paper and found to force an
unfavorable trade-off between "linearization error" and "Gaussian tail" that
does not close with an `O(1)` constant; abandoned in favor of the
no-truncation route below, which is what is actually attempted).

`h` is strictly decreasing on `[0,n)` (`phi' >0`), so
`Q(n) = sum_{j=0}^{n-1} P_j >= sum_{j=0}^{n-1} h(j) >= int_0^n h(x) dx`.

Write `phi(x) = x^2/(2n) + eps(x)`, `eps(x) = x(n+x^2)/(2n(n-x)) >= 0`. Split
`int_0^n h(x)dx = int_0^n e^{-x^2/2n}dx - int_0^n e^{-x^2/2n}(1-e^{-eps(x)})dx`,
first term `= sqrt(pi n/2) - Tail(n,n)` (Gaussian integral minus its tail
past `x=n`, both classical/standard); bound the second term (`Err(n)`,
nonnegative) by splitting `[0,n/2]` (Taylor-type bound
`eps(x)<=x/n+x^3/n^2` there, integrated against `e^{-x^2/2n}` using
`int_0^infty x e^{-x^2/2n}dx=n`, `int_0^infty x^3 e^{-x^2/2n}dx=2n^2`, giving
`<=3`) and `[n/2,n)` (crude `1-e^{-eps}<=1`, bounded by the Gaussian tail
past `n/2`, `<=2e^{-n/8}`). Standard tail bound throughout:
`int_T^infty e^{-x^2/2n}dx <= (n/T) e^{-T^2/2n}` for `T>0`.

Assembling gives an explicit `C` (target: single-digit, not optimized —
the classical true constant is `1/3`, elementary bounds here are expected to
be considerably looser, which is acceptable per the task).

**Success criterion, fixed in advance:** any finite explicit `C` making
`Q(n) >= sqrt(pi n/2) - C` PROVED for all `n>=1` suffices to upgrade the
`limsup` in the parent's Theorem 4 argument to an exact `lim`, because the
`C`-dependence washes out under `/sqrt K` as `K->infinity`. Precision of `C`
is not the target; correctness is.

## Planned derivation (piece 2), fixed before computation

Attempt, in order, stopping at the first that closes or exhausting the
list honestly:

(a) Look for an exact 2-term recursion for `Q(n)` enabling induction on
`r_K` — **the throwaway probe above already found none of the simplest
candidate forms holds**, so this is not expected to close but is recorded
as attempted.
(b) Attempt a *direct* pointwise bound `M_K <= a* sqrt K` for **every** `K`
(not just asymptotically), which would give `sup_K r_K <= a*` and, combined
with piece 1's `lim_K r_K = a*`, immediately give `sup_K r_K = a*` exactly
(since `sup >= lim` always) — a strictly weaker requirement than literal
monotonicity, and the route actually preferred if it closes. This needs a
lower bound on `Q(n)` and an upper bound on `(K+1)phi_K` **both** tight
enough, for every finite `K`, that their difference (not just their
leading `sqrt K` asymptotics) stays `<= a* sqrt K` — expected to require
next-order (`O(1)`, signed) terms in both expansions, not just the
leading-order elementary bounds of piece 1 / the parent's Lemma 4.1.
(c) If (a)-(b) do not close with full rigor in reasonable effort, report
the exact-arithmetic numerical evidence (strict monotonicity of `r_K`
observed up to `K` in the several-hundreds, gap shrinking like
`~0.33/sqrt K`, consistent with — but not proof of — the classical
next-order Ramanujan-`Q` asymptotic term `-1/3`) as NUMERICALLY VERIFIED /
HEURISTIC, not PROVED, exactly as the parent document did for this same
fact, and stop rather than force a proof.

## Discipline

- All claims labelled PROVED below use elementary real-analysis inequalities
  (`-ln(1-x)<=x/(1-x)`, `1-e^{-a}<=a`, `x/(n-i)` term comparisons, standard
  Gaussian-tail bounds, direct algebra) verified by hand and cross-checked
  by `sympy`/exact rational arithmetic (`fractions.Fraction`) where the
  quantity is rational (`Q(n)`, `phi_K`, `M_K`, the `r_K` monotonicity scan)
  and by `mpmath` (30-50 digit precision) only for the transcendental
  quantities (`sqrt(pi n/2)`, `a*`) and for wide-range sanity nets, never as
  the basis of a PROVED claim.
- No randomness needed (the object is entirely deterministic); per
  `DISC-DEC-057`, seed `20260831000+` is reserved for this front but is
  **not used**, exactly as the parent document used none — noted here so a
  referee does not need to ask.
- Full non-closure of piece 2 is an acceptable, pre-registered possible
  outcome, per the task's explicit instruction; it will be reported as such,
  not forced.

## Files planned

- `verify_Q_lower_bound.py` / `.log` — exact + `mpmath` verification of the
  piece-1 chain: `P_j>=h(j)` termwise (exact `Fraction` vs `mpmath` `h`),
  `Err(n)<=3+2e^{-n/8}` and `Tail(n,n)<=e^{-n/2}` numerically (integration),
  and the final `Q(n)>=sqrt(pi n/2)-C` over a wide grid.
- `verify_limit.py` / `.log` — exact verification that the assembled
  two-sided bound on `r_K=M_K/sqrt K` holds and that it forces
  `r_K -> a*`, plus the raw `r_K` monotonicity scan (piece 2, numerical
  evidence only) up to `K` in the low thousands, `Fraction`-exact.
