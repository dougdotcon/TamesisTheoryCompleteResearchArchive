"""
ref_stats.py -- referee's own from-scratch statistical machinery, re-derived
from first principles (standard textbook methods), independently of any
front script. Cross-validated against scipy.stats where scipy provides a
standard reference implementation (a legitimate library use, not "trusting
the front's code" -- the front's own p-values are ALSO computed via
scipy.stats.t.sf, so this is a like-for-like check, not a dependency on the
front's methodology).
"""
import numpy as np
from scipy import stats as _scipy_stats


def pearson_r(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xm, ym = x - x.mean(), y - y.mean()
    num = np.sum(xm * ym)
    den = np.sqrt(np.sum(xm ** 2) * np.sum(ym ** 2))
    return num / den


def pearson_r_t_p(x, y, n_perm=200000, perm_seed=None):
    """Pearson r, t-stat, df, two-sided p (parametric, scipy.stats.t.sf), and
    an independent permutation-test p-value (label-shuffle null, no
    distributional assumption) as a from-scratch cross-check."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    r = pearson_r(x, y)
    df = n - 2
    if abs(r) >= 1.0 or df <= 0:
        t = np.inf * np.sign(r)
        p_param = 0.0
    else:
        t = r * np.sqrt(df) / np.sqrt(1 - r ** 2)
        p_param = 2.0 * _scipy_stats.t.sf(abs(t), df)
    p_perm = None
    if n_perm and n >= 4:
        rng = np.random.default_rng(perm_seed)
        cnt = 0
        y_arr = y.copy()
        for _ in range(n_perm):
            rng.shuffle(y_arr)
            r_p = pearson_r(x, y_arr)
            if abs(r_p) >= abs(r) - 1e-12:
                cnt += 1
        p_perm = cnt / n_perm
    return dict(r=r, t=t, df=df, p_param=p_param, p_perm=p_perm, n=n)


def spearman_r(x, y):
    """Spearman rank correlation, from scratch (rank + Pearson on ranks)."""
    def rank(a):
        order = np.argsort(a, kind="mergesort")
        ranks = np.empty(len(a), dtype=float)
        sorted_a = a[order]
        i = 0
        while i < len(a):
            j = i
            while j + 1 < len(a) and sorted_a[j + 1] == sorted_a[i]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            ranks[order[i:j + 1]] = avg_rank
            i = j + 1
        return ranks
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return pearson_r(rank(x), rank(y))


def partial_corr(x, y, z):
    """Partial correlation of x,y controlling for z: r_xy.z =
    (r_xy - r_xz*r_yz) / sqrt((1-r_xz^2)(1-r_yz^2)). Standard first-order
    partial correlation formula."""
    rxy = pearson_r(x, y)
    rxz = pearson_r(x, z)
    ryz = pearson_r(y, z)
    return (rxy - rxz * ryz) / np.sqrt((1 - rxz ** 2) * (1 - ryz ** 2))


def ols(X, y):
    """OLS via numpy.linalg.lstsq; X includes intercept column. Returns
    coefficients, SEs, t, two-sided p (df = n - k)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    beta, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    resid = y - yhat
    df = n - k
    sigma2 = np.sum(resid ** 2) / df
    XtX_inv = np.linalg.pinv(X.T @ X)
    cov_beta = sigma2 * XtX_inv
    se = np.sqrt(np.diag(cov_beta))
    t = beta / se
    p = 2.0 * _scipy_stats.t.sf(np.abs(t), df)
    ss_res = np.sum(resid ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    return dict(beta=beta, se=se, t=t, p=p, df=df, r2=r2, resid=resid)


def bonferroni(p_values, alpha=0.05):
    m = len(p_values)
    alpha_adj = alpha / m
    return dict(alpha_adj=alpha_adj, m=m,
                survives=[p < alpha_adj for p in p_values])


def pairwise_z(v1, sem1, v2, sem2):
    """z-score for the difference between two independent point estimates."""
    diff = v2 - v1
    se = np.sqrt(sem1 ** 2 + sem2 ** 2)
    z = diff / se if se > 0 else np.nan
    return diff, se, z


def subgroup_range_ztest(shares, sems):
    """Range test on a sub-group: range = max-min, z of that (max,min) pair's
    difference via pairwise_z. Also returns which two cells are extremal."""
    shares = np.asarray(shares, dtype=float)
    sems = np.asarray(sems, dtype=float)
    imax = np.argmax(shares)
    imin = np.argmin(shares)
    rng = shares[imax] - shares[imin]
    _, se, z = pairwise_z(shares[imin], sems[imin], shares[imax], sems[imax])
    return dict(range_pp=rng, z=z, imax=imax, imin=imin, se=se)


def cluster_bootstrap_ratio(n_far, cyc_far, B=3000, seed=None):
    """Cluster bootstrap (resample instances with replacement) for the pooled
    ratio estimator R=sum(y)/sum(x). Independent cross-check of the
    delta-method SEM."""
    rng = np.random.default_rng(seed)
    n_far = np.asarray(n_far)
    cyc_far = np.asarray(cyc_far)
    N = len(n_far)
    boots = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, N, size=N)
        xs = n_far[idx].sum()
        ys = cyc_far[idx].sum()
        boots[b] = ys / xs if xs > 0 else np.nan
    return dict(mean=np.nanmean(boots), sem=np.nanstd(boots, ddof=1), boots=boots)
