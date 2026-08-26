"""
Referee script 02 -- independent, from-scratch finite-n engine for
phi(n,c), built ONLY from the prose formula (Lemma 1, as quoted and
cited in gamma_intermediate_window_attempt/ATTEMPT.md, itself citing
gamma_scaling_attempt/ATTEMPT.md Section 1):

   phi(n, qn) = (1/n) sum_{k=1}^n A_k(n,q)
   A_k(n,q)   = sum_{m=0}^k C(k,m) q^m (1-q)^{k-m} P_{k,m}
   P_{k,m}    = prod_{i=1}^m (1 - (k-i)/n)      (empty product = 1)

No .py file of this front or any front in its lineage was opened.
mpmath dps=50 throughout.  O(n^2) total work per (n,q) evaluation via
incremental recurrences (binomial pmf ratio; partial product), a
performance detail only.

Checks:
 (a) sanity phi(n,0) = 1 exactly, several n.
 (b) Teorema R pointwise re-check: |phi(n,c)-phi_infty(c)| <=
     (a* sqrt(c) + kappa_B)/n  at a grid of (n, c=n^alpha) points,
     including points beyond the window's own 2/3 cutoff as a stress
     test.
 (c) Ratio phi(n,c)/phi_infty(c) -> 1 trend as n grows, at fixed alpha
     (window-representative and beyond).
 (d) The "bonus" claim: ratio -> 1 for c_n -> infinity, c_n = o(n),
     with NO rate restriction -- test with a genuinely slow-growing
     sequence c_n = log(n) (much slower than any n^alpha), which is
     NOT covered by Corolario 2's hypothesis (log n grows far slower
     than n^{1/3}... in fact log(n) / n^{1/3} -> 0, so Corolario 2's
     hypothesis gamma_n n^{1/3}/ln n -> infinity FAILS for c_n=log n
     since gamma_n = log(n)/n and gamma_n n^{1/3}/ln n = n^{1/3}/n ->0)
     -- exactly the kind of sequence the bonus claims to newly cover.
"""
import mpmath as mp

mp.mp.dps = 50

a_star = mp.sqrt(mp.pi) * (1/mp.sqrt(2) - mp.mpf(1)/2)
kappa_B = mp.mpf('0.2805')   # cited upper end of THEOREM.md's certified bracket

def phi_infty(c):
    c = mp.mpf(c)
    # Theorem 1 closed form: phi_infty(c) = (sqrt(pi)/2) c^{-1/2} erf(sqrt(c))
    return (mp.sqrt(mp.pi)/2) * c**mp.mpf('-0.5') * mp.erf(mp.sqrt(c))

def phi_finite(n, c):
    """Exact finite-n formula (Lemma 1), O(n^2) via incremental recurrences."""
    n = int(n)
    q = mp.mpf(c)/n
    if q > 1:
        q = mp.mpf(1)
    total = mp.mpf(0)
    for k in range(1, n+1):
        # incremental over m = 0..k
        # binomial pmf term: b(m) = C(k,m) q^m (1-q)^(k-m)
        # P_{k,m} = prod_{i=1}^m (1 - (k-i)/n)
        if q == 0:
            A_k = mp.mpf(1)  # only m=0 term survives, P_{k,0}=1
            total += A_k
            continue
        if q == 1:
            # only m=k term survives
            P = mp.mpf(1)
            for i in range(1, k+1):
                P *= (1 - mp.mpf(k-i)/n)
            total += P
            continue
        b = (1-q)**k          # m=0 term
        P = mp.mpf(1)          # P_{k,0}
        A_k = b * P
        for m in range(1, k+1):
            b = b * (k-m+1) * q / (m*(1-q))
            P = P * (1 - mp.mpf(k-m)/n)
            A_k += b * P
        total += A_k
    return total / n

print("=== (a) Sanity: phi(n,0) = 1 exactly ===")
for n in [1, 5, 20, 100]:
    val = phi_finite(n, 0)
    print(f"n={n}: phi(n,0) = {mp.nstr(val, 20)}  ==1 exactly: {val == 1}")
print()

print("=== (b) Teorema R pointwise re-check ===")
print("|phi(n,c) - phi_infty(c)| <= (a* sqrt(c) + kappa_B)/n  ?")
violations = 0
tested = 0
rows = []
for n in [30, 100, 300, 1000]:
    for alpha in [mp.mpf('0.15'), mp.mpf('0.35'), mp.mpf('0.55'), mp.mpf('0.65')]:
        c = mp.mpf(n)**alpha
        phi_n = phi_finite(n, c)
        phi_i = phi_infty(c)
        lhs = abs(phi_n - phi_i)
        rhs = (a_star*mp.sqrt(c) + kappa_B)/n
        ok = lhs <= rhs
        tested += 1
        if not ok:
            violations += 1
        rows.append((n, float(alpha), float(c), mp.nstr(lhs,10), mp.nstr(rhs,10), ok))
for r in rows:
    print(f"n={r[0]:5d} alpha={r[1]:.2f} c={r[2]:10.4f}  |phi-phi_inf|={r[3]:>14}  "
          f"bound={r[4]:>14}  OK={r[5]}")
print(f"\nTotal tested={tested}, violations={violations}")
print()

print("=== (c) Ratio phi(n,c)/phi_infty(c) -> 1 trend (window-representative alpha) ===")
for alpha in [mp.mpf('0.15'), mp.mpf('0.35'), mp.mpf('0.55')]:
    print(f"-- alpha={alpha} --")
    for n in [30, 100, 300, 1000, 2000]:
        c = mp.mpf(n)**alpha
        phi_n = phi_finite(n, c)
        phi_i = phi_infty(c)
        ratio = phi_n/phi_i
        print(f"   n={n:5d}  c={mp.nstr(c,8):>12}  ratio={mp.nstr(ratio,10)}")
    print()

print("=== (d) Bonus claim stress test: c_n = log(n) (NOT covered by Corolario 2) ===")
print("Corolario 2 needs gamma_n n^(1/3)/ln n -> infinity;")
print("for c_n=log(n): gamma_n = log(n)/n, so gamma_n n^(1/3)/ln n = n^(1/3)/n = n^(-2/3) -> 0.")
print("Corolario 2's hypothesis genuinely FAILS here -- this sequence is only reachable")
print("by the bonus claim (c_n -> infinity, c_n = o(n), no rate restriction).")
for n in [30, 100, 300, 1000, 3000]:
    c = mp.log(mp.mpf(n))
    phi_n = phi_finite(n, c)
    phi_i = phi_infty(c)
    ratio = phi_n/phi_i
    B_bound = (a_star*mp.sqrt(c)+kappa_B)/(n * ((mp.sqrt(mp.pi)/2)*c**mp.mpf('-0.5') - mp.e**(-c)/(2*c)))
    print(f"n={n:5d}  c=log(n)={mp.nstr(c,8):>10}  ratio={mp.nstr(ratio,10)}  "
          f"|ratio-1|={mp.nstr(abs(ratio-1),8)}  TheoremW_bound={mp.nstr(B_bound,8)}  "
          f"within_bound={abs(ratio-1)<=B_bound}")
