"""
Referee (adversarial) independent numerical fit of the claimed asymptotic
law (ATTEMPT.md Sec 4.4b/Sec 5) against THIS REFEREE'S OWN Pi(c) data
(ref03_plateau_compute.py outputs), plus independent 2-term/3-term family
exclusion tests (Sec 7.3). Uses none of the front's own fit code.

Reads ref03_result_c*.json (this referee's own computed values) for
c in {640, 1000, 2560, 163840, 655360}.
"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp

mp.mp.dps = 130

HERE = os.path.dirname(os.path.abspath(__file__))


def load_data():
    data = {}
    for fn in glob.glob(os.path.join(HERE, "ref03_result_c*.json")):
        with open(fn) as f:
            r = json.load(f)
        data[r["c"]] = mp.mpf(r["S290"])
    return data


def main():
    data = load_data()
    cs_sorted = sorted(data.keys())
    print("Loaded c values:", cs_sorted)
    eps = {c: 1 / mp.sqrt(c) for c in data}
    y = {c: data[c] * mp.sqrt(2 * c / mp.pi) for c in data}
    for c in cs_sorted:
        print(f"  c={c}: eps={mp.nstr(eps[c],10)}  y={mp.nstr(y[c],25)}")

    # exact NxN Vandermonde fit using ALL points
    N = len(cs_sorted)
    A = mp.matrix(N, N)
    bvec = mp.matrix(N, 1)
    for i, c in enumerate(cs_sorted):
        e = eps[c]
        for j in range(N):
            A[i, j] = e ** j
        bvec[i, 0] = y[c]
    sol = mp.lu_solve(A, bvec)
    print(f"\n=== {N}-point exact fit (all referee-computed points) ===")
    for j in range(N):
        print(f"  d{j} (fit) = {mp.nstr(sol[j], 22)}")

    d_pred = [mp.mpf(1), -2 * mp.sqrt(mp.mpf(2) / mp.pi), mp.mpf('3.5'),
              -(mp.mpf(34) / 3) * mp.sqrt(mp.mpf(2) / mp.pi)]
    labels = ['d0', 'd1', 'd2', 'd3']
    print("\n  coeff | predicted | fit | fit-pred | rel")
    for j in range(min(4, N)):
        diff = sol[j] - d_pred[j]
        rel = diff / d_pred[j] if d_pred[j] != 0 else mp.nan
        print(f"  {labels[j]}: pred={mp.nstr(d_pred[j],18)}  fit={mp.nstr(sol[j],18)}  "
              f"diff={mp.nstr(diff,6)}  rel={mp.nstr(rel,4)}")
    if N >= 5:
        d4_conj = mp.mpf(209) / 8
        print(f"  d4: conjectured={mp.nstr(d4_conj,10)}  fit={mp.nstr(sol[4],10)}  "
              f"diff={mp.nstr(sol[4]-d4_conj,6)}")

    # 4-point subset dropping c=2560 (if present) for stability check
    if 2560 in data:
        cs2 = [c for c in cs_sorted if c != 2560]
        N2 = len(cs2)
        A2 = mp.matrix(N2, N2); b2 = mp.matrix(N2, 1)
        for i, c in enumerate(cs2):
            e = eps[c]
            for j in range(N2):
                A2[i, j] = e ** j
            b2[i, 0] = y[c]
        sol2 = mp.lu_solve(A2, b2)
        print("\n=== 4-point subset fit (drop c=2560), stability check ===")
        for j in range(N2):
            print(f"  d{j} = {mp.nstr(sol2[j], 18)}")

    # 2-term and 3-term family exclusion tests (independent of the above fit)
    def fit_and_test(fit_cs, test_c, nterms):
        Af = mp.matrix(nterms, nterms)
        bf = mp.matrix(nterms, 1)
        for i, c in enumerate(fit_cs):
            for j in range(nterms):
                Af[i, j] = mp.mpf(c) ** (-(j + 1) / mp.mpf(2))
            bf[i, 0] = data[c]
        solf = mp.lu_solve(Af, bf)
        pred = sum(solf[j] * mp.mpf(test_c) ** (-(j + 1) / mp.mpf(2)) for j in range(nterms))
        actual = data[test_c]
        return solf, pred, actual, abs(pred - actual) / abs(actual)

    print("\n=== 2-term family a/sqrt(c)+b/c: fit on 640,1000, test at 655360 ===")
    solf, pred, actual, relerr = fit_and_test([640, 1000], 655360, 2)
    print("  coeffs:", [mp.nstr(x, 8) for x in solf])
    print(f"  pred={mp.nstr(pred,18)}  actual={mp.nstr(actual,18)}  relerr={mp.nstr(relerr,6)}")

    print("\n=== 3-term family a/sqrt(c)+b/c+g/c^1.5: fit on 640,1000,2560, test at 163840 ===")
    solf, pred, actual, relerr = fit_and_test([640, 1000, 2560], 163840, 3)
    print("  coeffs:", [mp.nstr(x, 8) for x in solf])
    print(f"  pred={mp.nstr(pred,18)}  actual={mp.nstr(actual,18)}  relerr={mp.nstr(relerr,6)}")


if __name__ == "__main__":
    main()
