"""Referee independent Monte Carlo, rebuilt from ATTEMPT.md prose only (no
front script read or reused).  Fresh referee seeds 20260859000 (c=1) and
20260859001 (c=4), from the referee-reserved block 20260859000+ (confirmed
unused across the archive before first use; only reservation lines hit).

Model: THEOREM.md Definition 1.  pi = uniform permutation of [n];
xi_i ~ Bernoulli(c/n) iid; U_i ~ Unif([n]) iid; f(i) = U_i if xi_i else pi(i).
Query points: 0 and 1 (exchangeability).

Per c value:
  [M1] harness sanity: E[fraction cyclic] vs phi_inf(c) (PROVED target) and,
       observationally, E[(fraction cyclic)^2] vs the CONJECTURED (1-e^-c)/c.
  [M2] Lemma B1 sanity: fraction of same-pi-cycle trials ~ 1/2.
  [M3] Lemma B4 inclusion: on same-cycle trials, {no member of the shared
       cycle rerouted} => {both query points cyclic}.  Violations MUST be 0
       (exact logical check, trial by trial).  Also per-bucket empirical
       P(both) >= empirical P(intact).
  [M4] g(ell) buckets vs exp(-c*ell^2) and exp(-2c*ell^2): confirm g matches
       NEITHER (|z|>3 somewhere for each candidate), per ATTEMPT.md 3.5.
  [M5] rho(ell) = (g - m^2)/(m - m^2) with the empirical finite-n marginal m:
       qualitative check that rho is high at small/mid ell and decreases
       toward ell -> 1 (last bucket < first three buckets' max).

Cyclic set computed by pointer doubling (image of f^(2^k), 2^k >= n, is
exactly the cyclic set); cross-validated on the first 50 trials of each run
against an independent in-degree-peeling implementation.
"""
import numpy as np
import math

FAIL = 0


def check(name, ok, detail=""):
    global FAIL
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
    print(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))


def cyclic_mask_doubling(f):
    n = len(f)
    g = f.copy()
    steps = 1
    while steps < n:
        g = g[g]
        steps *= 2
    mask = np.zeros(n, dtype=bool)
    mask[g] = True
    return mask


def cyclic_mask_peel(f):
    n = len(f)
    indeg = np.bincount(f, minlength=n)
    removed = np.zeros(n, dtype=bool)
    stack = list(np.nonzero(indeg == 0)[0])
    while stack:
        v = stack.pop()
        removed[v] = True
        w = f[v]
        indeg[w] -= 1
        if indeg[w] == 0 and not removed[w]:
            stack.append(w)
    return ~removed


def phi_inf(c, npts=200001):
    tt = np.linspace(0, 1, npts)
    return np.trapezoid(np.exp(-c * tt * tt), tt)


def run(c, n, trials, seed, nbuck=8):
    rng = np.random.default_rng(seed)
    print(f"\n=== referee MC: c={c}, n={n}, trials={trials}, seed={seed} ===")
    fr = np.empty(trials)
    same = np.zeros(trials, dtype=bool)
    intact = np.zeros(trials, dtype=bool)
    both = np.zeros(trials, dtype=bool)
    ell0 = np.empty(trials, dtype=np.int64)   # cycle length of point 0
    cyc0 = np.zeros(trials, dtype=bool)       # point 0 cyclic
    violations = 0
    for tr in range(trials):
        pi = rng.permutation(n)
        xi = rng.random(n) < c / n
        U = rng.integers(0, n, size=n)
        f = np.where(xi, U, pi)
        mask = cyclic_mask_doubling(f)
        if tr < 50:
            assert np.array_equal(mask, cyclic_mask_peel(f)), \
                "cyclic-set algorithms disagree"
        fr[tr] = mask.mean()
        cyc0[tr] = mask[0]
        # walk pi-cycle of 0
        members = [0]
        j = int(pi[0])
        while j != 0:
            members.append(j)
            j = int(pi[j])
        ell0[tr] = len(members)
        if 1 in members:
            same[tr] = True
            mem = np.array(members)
            intact[tr] = not xi[mem].any()
            both[tr] = mask[0] and mask[1]
            if intact[tr] and not both[tr]:
                violations += 1
    mean_fr = fr.mean()
    m2_fr = (fr * fr).mean()
    phi = phi_inf(c)
    tgt2 = (1 - math.exp(-c)) / c
    se_mean = fr.std(ddof=1) / math.sqrt(trials)
    print(f"  E[frac cyclic]   = {mean_fr:.5f}  vs PROVED phi_inf({c})={phi:.5f}"
          f"  (z={(mean_fr - phi) / se_mean:+.2f})")
    se2 = (fr * fr).std(ddof=1) / math.sqrt(trials)
    print(f"  E[frac cyclic^2] = {m2_fr:.5f}  vs conjectured (1-e^-c)/c={tgt2:.5f}"
          f"  (z={(m2_fr - tgt2) / se2:+.2f})  [observational only]")
    check(f"M1 c={c}: mean matches PROVED phi_inf within 4 sigma",
          abs(mean_fr - phi) < 4 * se_mean)
    nsame = int(same.sum())
    check(f"M2 c={c}: same-cycle fraction ~ 1/2",
          abs(nsame / trials - 0.5) < 4 * 0.5 / math.sqrt(trials),
          f"{nsame}/{trials}")
    check(f"M3 c={c}: ZERO intact-but-not-both-cyclic violations "
          f"(intact trials: {int(intact.sum())})", violations == 0,
          f"violations={violations}")

    # buckets over ell/n
    edges = np.linspace(0, 1, nbuck + 1)
    print(f"  bucket  mid   n_same  P(intact)  P(both)  both>=intact"
          f"   g_emp   e^-cl^2  e^-2cl^2   marg_m    rho")
    zA_max = zB_max = 0.0
    rhos = []
    ok_incl = True
    for b in range(nbuck):
        lo, hi = edges[b], edges[b + 1]
        mid = (lo + hi) / 2
        sel = same & (ell0 / n > lo) & (ell0 / n <= hi)
        ns = int(sel.sum())
        selm = (ell0 / n > lo) & (ell0 / n <= hi)   # marginal bucket (all trials)
        nm = int(selm.sum())
        if ns < 30 or nm < 30:
            print(f"  {b:5d}  {mid:.3f}  {ns:6d}  (skipped, too few)")
            rhos.append(np.nan)
            continue
        pi_int = intact[sel].mean()
        pb = both[sel].mean()
        g = pb
        seg = math.sqrt(max(g * (1 - g), 1e-12) / ns)
        gA = math.exp(-c * mid * mid)
        gB = math.exp(-2 * c * mid * mid)
        zA = (g - gA) / seg
        zB = (g - gB) / seg
        zA_max = max(zA_max, abs(zA))
        zB_max = max(zB_max, abs(zB))
        m = cyc0[selm].mean()
        rho = (g - m * m) / (m - m * m) if m * (1 - m) > 0 else np.nan
        rhos.append(rho)
        inc = pb >= pi_int
        ok_incl &= inc
        print(f"  {b:5d}  {mid:.3f}  {ns:6d}   {pi_int:.5f}  {pb:.5f}"
              f"     {str(inc):5s}    {g:.4f}   {gA:.4f}   {gB:.4f}"
              f"   {m:.4f}  {rho:6.3f}")
    check(f"M3 c={c}: per-bucket empirical P(both) >= empirical P(intact)",
          ok_incl)
    check(f"M4 c={c}: g matches NEITHER e^-cl^2 (max|z|={zA_max:.1f}) nor "
          f"e^-2cl^2 (max|z|={zB_max:.1f}) -- both rejected somewhere (|z|>3)",
          zA_max > 3 and zB_max > 3)
    r = np.array(rhos, dtype=float)
    valid = ~np.isnan(r)
    first3 = np.nanmax(r[:3]) if valid[:3].any() else np.nan
    last = r[valid][-1] if valid.any() else np.nan
    check(f"M5 c={c}: rho decreasing pattern (last bucket {last:.3f} < "
          f"max of first three {first3:.3f})", last < first3)
    return


run(c=1.0, n=2000, trials=20000, seed=20260859000)
run(c=4.0, n=2000, trials=20000, seed=20260859001)

print()
print("TOTAL FAILURES:", FAIL)
assert FAIL == 0, "AT LEAST ONE MC CHECK FAILED"
print("ALL REFEREE MC CHECKS PASSED")
