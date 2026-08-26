"""
Referee script 04 -- direct digit-for-digit cross-check of two specific
numeric values quoted in gamma_intermediate_window_attempt/ATTEMPT.md
Section 2 (script 02's described output): the ratio phi(n,c)/phi_infty(c)
at n=3000 for alpha=0.15 (claimed 0.9999642) and alpha=0.65 (claimed
1.0130), using an entirely independent from-scratch implementation of
the exact finite-n double-sum formula (Lemma 1) built from the prose.

No .py file of this front or any front in its lineage was opened.
"""
import mpmath as mp

mp.mp.dps = 50

def phi_infty(c):
    c = mp.mpf(c)
    return (mp.sqrt(mp.pi)/2) * c**mp.mpf('-0.5') * mp.erf(mp.sqrt(c))

def phi_finite(n, c):
    n = int(n)
    q = mp.mpf(c)/n
    if q > 1:
        q = mp.mpf(1)
    total = mp.mpf(0)
    for k in range(1, n+1):
        if q == 0:
            total += 1
            continue
        b = (1-q)**k
        P = mp.mpf(1)
        A_k = b*P
        for m in range(1, k+1):
            b = b*(k-m+1)*q/(m*(1-q))
            P = P*(1 - mp.mpf(k-m)/n)
            A_k += b*P
        total += A_k
    return total/n

print("Cross-checking ATTEMPT.md Section 2's claimed ratio values at n=3000:")
print("  claimed: alpha=0.15 -> ratio ~ 0.9999642")
print("  claimed: alpha=0.65 -> ratio ~ 1.0130")
print()
for alpha, n in [(mp.mpf('0.15'), 3000), (mp.mpf('0.65'), 3000)]:
    c = mp.mpf(n)**alpha
    phi_n = phi_finite(n, c)
    phi_i = phi_infty(c)
    ratio = phi_n/phi_i
    print(f"alpha={alpha} n={n} c={mp.nstr(c,8)} ratio(independent)={mp.nstr(ratio,10)}")
