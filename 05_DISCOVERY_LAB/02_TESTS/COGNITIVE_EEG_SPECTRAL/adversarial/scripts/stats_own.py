"""Independent implementations of Welch's t-test and Mann-Whitney U,
written from the standard formulas (not calling scipy.stats.ttest_ind /
mannwhitneyu for the reported numbers, though cross-validated against
them separately)."""
import numpy as np
import math


def welch_ttest(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n1, n2 = len(a), len(b)
    m1, m2 = a.mean(), b.mean()
    v1, v2 = a.var(ddof=1), b.var(ddof=1)
    se2 = v1 / n1 + v2 / n2
    se = math.sqrt(se2)
    t = (m1 - m2) / se
    df = se2 ** 2 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
    p = 2.0 * (1.0 - student_t_cdf(abs(t), df))
    sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)
    d = (m1 - m2) / math.sqrt(sp2)
    return {
        "n1": n1, "n2": n2, "mean1": m1, "mean2": m2, "sd1": math.sqrt(v1), "sd2": math.sqrt(v2),
        "t": t, "df": df, "p_two_tailed": p, "cohens_d": d,
    }


def student_t_cdf(x, df):
    # CDF of Student's t via regularized incomplete beta function (mpmath-free, using
    # scipy.special.betainc for numerical robustness of the incomplete beta -- this is
    # a standard special-function evaluation, not a statistical-test judgment call).
    from scipy.special import betainc
    if x <= 0:
        # CDF(x) = 0.5 * betainc(df/2, 0.5, df/(df+x^2)) for x<0 ... use symmetry
        xx = df / (df + x * x)
        ib = betainc(df / 2.0, 0.5, xx)
        return 0.5 * ib
    else:
        xx = df / (df + x * x)
        ib = betainc(df / 2.0, 0.5, xx)
        return 1.0 - 0.5 * ib


def mann_whitney_u(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    n1, n2 = len(a), len(b)
    combined = np.concatenate([a, b])
    order = np.argsort(combined, kind="mergesort")
    ranks = np.empty(len(combined), dtype=np.float64)
    sorted_vals = combined[order]
    # average ranks for ties
    i = 0
    rank = 1
    while i < len(sorted_vals):
        j = i
        while j + 1 < len(sorted_vals) and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        avg_rank = (rank + (rank + (j - i))) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        rank += (j - i + 1)
        i = j + 1

    R1 = ranks[:n1].sum()
    U1 = R1 - n1 * (n1 + 1) / 2.0
    U2 = n1 * n2 - U1

    # normal approximation with tie correction
    # tie correction term
    vals, counts = np.unique(combined, return_counts=True)
    tie_term = np.sum(counts ** 3 - counts) / ((n1 + n2) * (n1 + n2 - 1))
    mu_U = n1 * n2 / 2.0
    sigma2_U = (n1 * n2 / 12.0) * ((n1 + n2 + 1) - tie_term / (n1 + n2))
    sigma_U = math.sqrt(sigma2_U)

    U = min(U1, U2)
    # continuity correction
    z = (U - mu_U) / sigma_U
    # two-sided p using normal approx of |U1 - mu| with continuity correction
    Ustat = U1
    if Ustat > mu_U:
        z_cc = (Ustat - 0.5 - mu_U) / sigma_U
    else:
        z_cc = (Ustat + 0.5 - mu_U) / sigma_U
    from scipy.special import erf
    p = 2.0 * (1.0 - 0.5 * (1 + erf(abs(z_cc) / math.sqrt(2))))
    p = min(p, 1.0)
    return {"U1": U1, "U2": U2, "n1": n1, "n2": n2, "z": z_cc, "p_two_tailed": p}
