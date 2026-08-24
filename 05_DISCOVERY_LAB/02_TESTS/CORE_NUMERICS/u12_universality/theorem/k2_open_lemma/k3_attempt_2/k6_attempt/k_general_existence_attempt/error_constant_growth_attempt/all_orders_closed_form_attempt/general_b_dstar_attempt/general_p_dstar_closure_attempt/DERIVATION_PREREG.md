# Pre-registration — `GENERAL-P-DSTAR-CLOSURE-ATTEMPT`

Written before any non-throwaway verification run in this directory, per
standing archive discipline. Timestamp: 2026-08-24, wave 15 front (a),
authorized by `DISC-DEC-063`.

## Target

Item 11 of `general_b_dstar_attempt/ATTEMPT.md`'s scorecard: a general-`p`
closed form for the sharp error constants `D^{*(p)}_r(b)` (Corollary A3 of
`all_orders_closed_form_attempt/ATTEMPT.md`), `p\ge5`, every `b\ge0`. Attempt
a genuinely general-`p` symbolic/algorithmic closed form first; fall back to
explicit `p=5,6` (and further, as far as tractable) if a fully general-`p`
route proves unwieldy.

## Method (planned before any code is run)

Reuse, by citation, the four ingredients already established:

1. `Q_p(u)=e_p(1,\dots,u)`, degree `2p`, vanishing for `u<p` — PROVED in
   `general_b_dstar_attempt/ATTEMPT.md` §3.1, general `p`. I will compute
   `Q_p(u)` for arbitrary `p` via Newton's identities from the Faulhaber
   power-sum polynomials `P_1(u),\dots,P_p(u)` — a classical, `p`-general
   algorithm, not case-by-case interpolation — and cross-check the output
   against direct evaluation of `e_p(1,\dots,u)` at many concrete `u`.
2. Central moments `\mu_{2l}(N)` of `\mathrm{Bin}(N,\tfrac12)` via the
   cumulant generating function `N\log\cosh(t/2)`, Taylor-expanded to order
   `2p` — the parent document's own method (§3.2), executed there only to
   `l=4`; I will implement it as a function of `l` (not degree-limited) and
   run it up to whatever `l=p` is needed.
3. The general-`k` odd-power identity (referee's Part 1,
   `general_b_dstar_attempt/adversarial/REFEREE_REPORT.md`, PROVED,
   symbolically verified to exponent `40`, numerically to `k=11`):
   `S_{2k-1}(N,m)=(N-2m)^{2k-2}(m{+}1)\binom N{m+1}+2N\sum_{s\text{ odd},1\le
   s\le2k-3}\binom{2k-2}{s}S_s(N{-}1,m{-}1)`. **Cited as established input,
   not re-derived from scratch** — a quick independent spot check (against
   direct summation) will be run for the specific `k` values actually needed
   here, per the mandate's instruction.
4. The general-`k` prefactor collapse (parent §3.4, PROVED, every `k`):
   `P_b[N]_k(r{-}k{+}1)\binom{N-k}{r-k+1}=[r]_k`. I will use the equivalent
   one-line closed form `P_b\binom{N-j}{r-j+1}=[r]_j/([N]_j(r-j+1))`
   (immediate from `N-r-1=r+b`), derived independently below in
   `odd_part.py` before use, and cross-checked against the collapse
   proposition's own statement.

**Assembly plan.** `N:=2r+b+1`, `\beta:=b+1`, `v:=\alpha-N/2`. Write
`Q_p(-(v+\beta/2))=E_p(v)+O_p(v)` (even/odd split in `v`). Then

`D^{*(p)}_r(b) = \tfrac12\big[\Phi_b(r)M_p(N) - \mathrm{Strip}_p(r,b)\big]
 - \sum_{k=1}^p o_k\,H_k(r,b)/2^{2k-1}`,

where `\Phi_b(r):=P_b2^N` (already-established identity, spot-checked
here), `M_p(N):=\sum_l e_{2l}\mu_{2l}(N)` (`e_{2l}`= coefficient of `v^{2l}`
in `E_p`), `\mathrm{Strip}_p(r,b):=\sum_{i=1}^b E_p(i-\beta/2)w_i(r,b)`,
`w_i(r,b):=r!(r{+}b)!/[(r{+}i)!(r{+}b{+}1{-}i)!]` (elementary, re-derived
independently below, matches parent's Step 3 with `E_1\to E_p`), `o_k`=
coefficient of `v^{2k-1}` in `O_p`, and `H_k(r,b):=P_b\,S_{2k-1}(N,r)`
computed via a depth-tracking unrolling of ingredient 3 combined with
ingredient 4 (§ above) — an explicit, terminating, `k`-general algorithm,
implemented once and run for whatever `k\le p` is needed.

This is `p`-uniform in every step except the raw computation of `Q_p` and
`\mu_{2l}` themselves, which have no simpler form independent of `p` (this
is inherent — `Q_p` has genuine degree `2p`) but are computed by a single
`p`-general algorithm (Newton's identities / cumulant-series extraction),
not fitted per `p`. This is the same standard of "closed form" already used
in this archive for the general-`k` collapse and the referee's general-`k`
odd-power identity: a formula parameterized by an integer index, given by an
explicit terminating procedure proved correct for every value of the index,
not a single index-free algebraic expression.

## Success criteria (stated in advance)

- **Strong target (attempted first):** a `p`-general algorithm, proved
  correct for every `p` from the four cited ingredients plus the two
  elementary identities re-derived here (`\Phi_b(r)=P_b2^N`,
  `P_b\binom{N-j}{r-j+1}=[r]_j/([N]_j(r-j+1))`), that produces the exact
  closed form for any given `p`, verified against an independently
  implemented Corollary-A3 ground truth (own Stirling table, not imported
  from any predecessor script) at `p` up to at least `8`, `r` up to `150`,
  `b` up to `20`.
- **Fallback (if the general algorithm cannot be validated at scale, or
  numerical issues arise for large `p`):** explicit closed forms for
  `p=5,6` only, at the same verification scale as the parent document.
- **Honesty commitment:** if the general algorithm's correctness proof has
  a gap (e.g. an ingredient turns out not to be as general as claimed), this
  will be reported precisely, the claim demoted to whatever scope is
  actually justified, and the gap named exactly — no reformulation of the
  target to manufacture an apparent closure.

## Ground truth

`ground_truth.py`, written from scratch in this directory (own
unsigned-Stirling recurrence `c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k)`), implementing
Corollary A3 directly: `D^{*(p)}_r(b)=\sum_{j=p}^r c_j^{(r)}(b)c(j{+}1,j{+}1-p)`,
`c_j^{(r)}(b):=r!/[(r-j)!\prod_{i=1}^{j+1}(r+b+i)]`. Not imported from the
parent document's or the referee's `ground_truth.py`/`own_ground_truth.py`
(read only for understanding, per task instructions).

## Exactness policy

`sympy.Rational` / `fractions.Fraction` / `sympy.Symbol` throughout. No
floating point anywhere in this directory's non-throwaway code.

## Randomness / seeds

This entire derivation is exact symbolic algebra plus exhaustive finite
sweeps — **no randomness is needed or used**. The reserved seed range
`20260841000+` (`DISC-DEC-063`, front (a)) is therefore not used. Confirmed
unused elsewhere in the archive before this file was written
(`grep -rn "20260841" 05_DISCOVERY_LAB/` returned no hits other than the
ledger's own reservation line for this wave — checked directly).

## Files planned

- `DERIVATION_PREREG.md` — this file.
- `ground_truth.py` / `.log` — independent Corollary A3 implementation.
- `ingredients.py` / `.log` — `Q_p(u)` (Newton's identities, general `p`),
  central moments `\mu_{2l}(N)` (cumulant series, general `l`), sanity checks
  against the parent's printed `Q_1..Q_4`, `\mu_2,\mu_4,\mu_6,\mu_8`, and an
  independent spot-check of the referee's general-`k` odd-power identity for
  the `k` values used here.
- `odd_part.py` / `.log` — the `H_k(r,b)` machine (§ above), the two
  elementary identities (`\Phi_b(r)=P_b2^N`, the `j`-collapse), verified
  against brute-force `S_{2k-1}` summation and against the parent's printed
  `k=1,2,3,4` brackets.
- `assemble.py` / `.log` — full assembly `D^{*(p)}_r(b)` for general `p`
  (function of `p`), run for `p=1,\dots,8` (or as far as tractable), checked
  against `ground_truth.py` at scale; explicit printed formulas for
  `p=5,6,7`.
- `ATTEMPT.md` — final report, this front's deliverable.

No file outside this directory will be created, modified, or deleted. No
git operation will be performed. `THEOREM.md` and the decision ledger will
not be touched.
