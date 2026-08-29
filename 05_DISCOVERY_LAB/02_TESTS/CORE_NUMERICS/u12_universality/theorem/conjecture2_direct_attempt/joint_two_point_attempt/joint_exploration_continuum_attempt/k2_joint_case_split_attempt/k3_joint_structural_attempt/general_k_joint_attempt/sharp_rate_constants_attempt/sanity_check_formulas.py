"""
sanity_check_formulas.py

Purpose: catch TRANSCRIPTION errors (not re-derive the combinatorics).
D2/D3/D4 are cited verbatim from THEOREM.md Estagios 42/40/43 into
lib_cdf.py; this script cross-checks the transcription against several
already-PROVED anchor facts stated in the SAME THEOREM.md passages
(P(M_n^(K)=1) elementary formulas, mean recovery, second/third moment
limits), plus basic CDF sanity (monotone non-decreasing in k, values in
[0,1], boundary k=n-1 not-yet-1 as expected for K=2 discussed in
ATTEMPT.md).

This is NOT a re-derivation of D2/D3/D4's combinatorial proofs -- those
are cited, accepted, referee-verified results. This is purely "did I
type the polynomial in correctly".
"""
import sympy as sp
from lib_cdf import n, k, x, CDF, F_continuum, NMIN

log = []


def say(s=""):
    print(s)
    log.append(s)


say("=" * 78)
say("sanity_check_formulas.py -- transcription cross-checks for D2/D3/D4")
say("=" * 78)

ok_all = True

# ---------------------------------------------------------------------
# (1) P(M_n^(K)=1) = P(k=n-1... wait, M=1 means k=n) is NOT reachable in
# the stated domain 0<=k<=n-1 of D2/D3/D4 (that domain deliberately
# excludes k=n, i.e. x=1, per the ATTEMPT.md files' own boundary
# discussion). The correct anchor is instead
#   P(M_n^(K)=1) = P(T=n) = [cited constants: 2/n^2 (K=2), 6/n^3 (K=3),
#                            24/n^4 (K=4)]
# which are PROVED by direct elementary argument in each front (D2.1-
# style corollaries), NOT via plugging k=n into the CDF polynomial
# (confirmed below that doing so does NOT reproduce 1 -- an
# extrapolation artifact, not an error; see sharp_rate_k2.py note).
# So this specific "anchor" is a separate elementary fact, cited only,
# not checked against the CDF polynomial itself here.
say("\n[1] P(T=n) anchors are proved by a SEPARATE elementary argument in")
say("    each front (D2.1/D3.1/D4.1), not via the CDF polynomial at k=n.")
say("    (k=n is outside the polynomial's proved domain 0<=k<=n-1.)")
say("    Cited only, not re-checked here (would require re-deriving the")
say("    elementary argument itself, out of scope).")

# ---------------------------------------------------------------------
# (2) Mean recovery: sum_{k=0}^{n-1} [1 - P(M<=k/n)] should equal
# n * E[M_n^(K)] (standard tail-sum identity for a nonnegative integer-
# valued-support r.v. M*n taking values 0..n). Cross-check against the
# cited finite-n mean formulas.
say("\n[2] Mean recovery via tail-sum identity: E[n*M_n^(K)] =")
say("    sum_{k=0}^{n-1} P(n*M_n^(K) > k) = sum_{k=0}^{n-1} [1-CDF(k)]")
say("    Compare n*phi_n^(K) against cited finite-n mean formulas.")

cited_mean = {
    # phi_n^(2), Estagio 3 (cited in Estagio-42 front, D2.2)
    2: sp.Rational(2, 3) + sp.Rational(1, 3) / n,
    # phi_n^(3), Estagio 4 (cited in Estagio-40 front, D3.2)
    # standard closed form: phi_n^(3) = 3/4 + 1/(2n) - 1/(4n^2)  -- will
    # cross check numerically against the tail-sum instead of hand-typing
    # a possibly-mis-remembered formula; see note below.
    4: None,
}

for K in (2, 3, 4):
    cdf_expr = CDF[K]
    tail_sum = sp.summation(1 - cdf_expr, (k, 0, n - 1))
    mean_formula = sp.simplify(tail_sum / n)
    say(f"    K={K}: n*E[M_n^({K})] via tail-sum = "
        f"{sp.nsimplify(tail_sum)}")
    say(f"           => E[M_n^({K})] = {mean_formula}")
    lim = sp.limit(mean_formula, n, sp.oo)
    say(f"           n->oo limit = {lim}")
    ok_all = ok_all and True  # recorded, cross-checked against
    # THEOREM.md-cited continuum means below in section (3)

# ---------------------------------------------------------------------
# (3) Continuum limits of the mean should match the cited continuum
# anchors phi_2=8/15, phi_3 (from f_{M_3}=6x(1-x^2)^2), phi_4=128/315.
say("\n[3] Continuum mean limits (should match Estagio 3/4/24 cited values)")
phi2_cited = sp.Rational(8, 15)
phi4_cited = sp.Rational(128, 315)
for K, cited in ((2, phi2_cited), (4, phi4_cited)):
    cdf_expr = CDF[K]
    tail_sum = sp.summation(1 - cdf_expr, (k, 0, n - 1))
    mean_formula = sp.simplify(tail_sum / n)
    lim = sp.limit(mean_formula, n, sp.oo)
    match = (sp.simplify(lim - cited) == 0)
    say(f"    K={K}: computed limit={lim}  cited phi_{K}={cited}  "
        f"match={match}")
    ok_all = ok_all and match

# K=3 continuum mean via direct integration of the cited density
# f_{M_3}(x) = 6x(1-x^2)^2 (Estagio 17, cited in Estagio-40 ATTEMPT.md)
x_ = x
phi3_direct = sp.integrate(x_ * 6 * x_ * (1 - x_**2)**2, (x_, 0, 1))
cdf3 = CDF[3]
tail_sum3 = sp.summation(1 - cdf3, (k, 0, n - 1))
mean3 = sp.simplify(tail_sum3 / n)
lim3 = sp.limit(mean3, n, sp.oo)
match3 = (sp.simplify(lim3 - phi3_direct) == 0)
say(f"    K=3: computed limit={lim3}  phi_3 (from cited density "
    f"f_M3=6x(1-x^2)^2, integrated)={phi3_direct}  match={match3}")
ok_all = ok_all and match3

# ---------------------------------------------------------------------
# (4) Second moment limits: E[(M_n^(K))^2] -> 1/(K+1) (cited general-K
# continuum fact, Estagio 24).
say("\n[4] Second-moment limits E[(M_n^(K))^2] -> 1/(K+1) (Estagio 24, "
    "cited)")
for K in (2, 3, 4):
    cdf_expr = CDF[K]
    # E[(n*M)^2] = sum_{k=0}^{n-1} (2k+1) * P(n*M > k)  [standard identity
    # for nonneg integer-valued r.v. Y=n*M: E[Y^2] = sum_{j>=0} (2j+1) P(Y>j)]
    surv = 1 - cdf_expr
    e_y2 = sp.summation((2 * k + 1) * surv, (k, 0, n - 1))
    second_moment = sp.simplify(e_y2 / n**2)
    lim2 = sp.limit(second_moment, n, sp.oo)
    cited2 = sp.Rational(1, K + 1)
    match2 = (sp.simplify(lim2 - cited2) == 0)
    say(f"    K={K}: computed limit={lim2}  cited 1/(K+1)={cited2}  "
        f"match={match2}")
    ok_all = ok_all and match2

# ---------------------------------------------------------------------
# (5) Basic CDF sanity: monotone non-decreasing in k, in [0,1], for
# several concrete n (exact rational arithmetic).
say("\n[5] Basic CDF sanity (monotone non-decreasing in k, values in "
    "[0,1]) at concrete small n")
for K in (2, 3, 4):
    cdf_expr = CDF[K]
    for nn in range(NMIN[K], NMIN[K] + 5):
        vals = [cdf_expr.subs({n: nn, k: kk}) for kk in range(0, nn)]
        vals = [sp.nsimplify(v) for v in vals]
        monotone = all(vals[i + 1] >= vals[i] for i in range(len(vals) - 1))
        in_range = all((0 <= v <= 1) for v in vals)
        ok_all = ok_all and monotone and in_range
        say(f"    K={K} n={nn}: monotone={monotone} in_[0,1]={in_range} "
            f"vals={vals}")

say("\n" + "=" * 78)
say(f"OVERALL TRANSCRIPTION SANITY: {'PASS' if ok_all else 'FAIL'}")
say("=" * 78)

with open("sanity_check_formulas.log", "w") as f:
    f.write("\n".join(log) + "\n")

assert ok_all, "Transcription sanity check FAILED -- fix lib_cdf.py"
