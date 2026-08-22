"""
ATTEMPT.md Sec.3.4: verify (a) the classical binomial moment sums used in the proof,
(b) the reduced binomial-sum identity sum_{i=0}^{r-1}(r-i)(r-i+1)C(2r+1,i)=r*2^(2r-1),
and (c) that this identity implies G_r(1,0) = r*phi_r/4 (the rate conjecture) -- all by
exact rational computation, r=1..25 (well beyond the r=0..10 range independently
cross-checked against actual discrete closed forms elsewhere in this document).
"""
import sympy as sp

print("=== Classical binomial moment sums (elementary, standard) ===")
for n in [5, 10, 13]:
    s0 = sum(sp.binomial(n, i) for i in range(n + 1))
    s1 = sum(i * sp.binomial(n, i) for i in range(n + 1))
    s2 = sum(i**2 * sp.binomial(n, i) for i in range(n + 1))
    print(f"n={n}: sum C(n,i)=2^n: {s0==2**n}   sum i*C(n,i)=n*2^(n-1): {s1==n*2**(n-1)}   "
          f"sum i^2*C(n,i)=n(n+1)*2^(n-2): {s2==n*(n+1)*2**(n-2)}")

print()
print("=== Reduced binomial-sum identity: sum_{i=0}^{r-1}(r-i)(r-i+1)C(2r+1,i) = r*2^(2r-1) ===")
allok = True
for r in range(1, 26):
    n = 2 * r + 1
    lhs = sum((r - i) * (r - i + 1) * sp.binomial(n, i) for i in range(0, r))
    rhs = r * 2**(2 * r - 1)
    ok = (lhs == rhs)
    allok = allok and ok
print(f"holds for r=1..25: {allok}")

print()
print("=== G_r(1,0) = r*phi_r/4 (the rate conjecture), via the FULL d_k^{(r)}(0) sum ===")


def d_k_r_0(rr, kk):
    return sp.Rational((kk + 1) * (kk + 2), 2) * sp.factorial(rr) / sp.factorial(rr - kk - 1) * sp.factorial(rr) / sp.factorial(rr + kk + 2)


allok2 = True
for rr in range(1, 26):
    S = sum(d_k_r_0(rr, kk) for kk in range(0, rr))
    phi_r = sp.Rational(4, 1)**rr * sp.factorial(rr)**2 / sp.factorial(2 * rr + 1)
    target = sp.Rational(rr, 4) * phi_r
    ok = (S == target)
    allok2 = allok2 and ok
    if rr <= 10 or not ok:
        print(f"r={rr}: G_r(1,0)={S}  r*phi_r/4={target}  match={ok}")
print(f"holds for r=1..25: {allok2}")
