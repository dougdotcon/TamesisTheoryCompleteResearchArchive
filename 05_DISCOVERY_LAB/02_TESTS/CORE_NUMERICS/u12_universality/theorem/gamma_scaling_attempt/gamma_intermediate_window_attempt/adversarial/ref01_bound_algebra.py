"""
Referee script 01 -- independent re-derivation and stress-test of
Theorem W (the combined bound) claimed in
gamma_intermediate_window_attempt/ATTEMPT.md.

Built entirely from the PROSE of THEOREM.md (Estagio 22's Teorema R,
Estagio 6's Corolario 4.2) and the prose of the target ATTEMPT.md.
No .py file of this front or any front in its lineage was opened.

Checks performed:
  (1) a* recomputed to 50 digits from its closed form.
  (2) L(c) := (sqrt(pi)/2) c^{-1/2} - e^{-c}/(2c)  (Corolario 4.2's
      lower bound on phi_infty(c)) -- find crossover to positivity by
      bisection, independently.
  (3) Confirm L(c) > 0 for all c >= 1 (the front's "safe" threshold).
  (4) B(n,c) := (a* sqrt(c) + kappa_B) / (n * L(c))  -- Theorem W's
      claimed bound on |phi/phi_infty - 1|.  Evaluate at the window's
      two edges for a large range of n, check monotone decay to 0,
      and check the claimed leading asymptotic orders:
        upper edge c = n^(2/3)/log(n):  B ~ (2 a*/sqrt(pi)) n^{-1/3}/log n
        lower edge c = n^eps:            B ~ (2 a*/sqrt(pi)) n^{eps-1}
  (5) Window non-emptiness / disjointness-from-Corolario-2 checks,
      independently re-derived.
  (6) Flag the eps-range inconsistency between the VERDICT box
      (eps in (0,1)) and Section 0's own derivation (eps in (0,2/3)).
"""
import mpmath as mp

mp.mp.dps = 50

# ---------------------------------------------------------------
# (1) a* recomputation
# ---------------------------------------------------------------
a_star = mp.sqrt(mp.pi) * (1/mp.sqrt(2) - mp.mpf(1)/2)
print("=== (1) a* recomputation ===")
print("a* =", mp.nstr(a_star, 40))
claimed = mp.mpf('0.36708721186')
print("ATTEMPT.md claims a* = 0.36708721186...  matches to shown digits:",
      abs(a_star - claimed) < mp.mpf('1e-11'))
print()

# kappa_B: cited, NOT re-derived (branch-and-bound not repeated here,
# per the hard constraint against opening any lineage .py; we use the
# THEOREM.md-cited bracket verbatim as an input, exactly as the front
# itself does).
kappa_B_lo = mp.mpf('0.28048')
kappa_B_hi = mp.mpf('0.2805')
kappa_B = kappa_B_hi   # conservative (largest) choice, as the front uses
print("kappa_B bracket (cited from THEOREM.md Estagio 22):",
      kappa_B_lo, "<", "kappa_B", "<", kappa_B_hi)
print("Using kappa_B =", kappa_B, "(conservative upper end, matches ATTEMPT.md's",
      "'kappa_B<0.2805' usage)")
print()

# ---------------------------------------------------------------
# (2)+(3) L(c) crossover to positivity
# ---------------------------------------------------------------
def L(c):
    c = mp.mpf(c)
    return (mp.sqrt(mp.pi)/2) * c**mp.mpf('-0.5') - mp.e**(-c) / (2*c)

print("=== (2) L(c) crossover to positivity, independent bisection ===")
lo, hi = mp.mpf('0.001'), mp.mpf('2.0')
assert L(lo) < 0 and L(hi) > 0
for _ in range(200):
    mid = (lo+hi)/2
    if L(mid) < 0:
        lo = mid
    else:
        hi = mid
crossover = (lo+hi)/2
print("crossover c* (independent bisection) =", mp.nstr(crossover, 15))
print("ATTEMPT.md claims c*=0.2094 -- match:",
      abs(crossover - mp.mpf('0.2094')) < mp.mpf('0.0001'))
print()

print("=== (3) L(c) > 0 for all c >= 1 ===")
worst = None
for cc in [mp.mpf(x)/100 for x in range(100, 100000, 137)]:
    val = L(cc)
    if worst is None or val < worst[1]:
        worst = (cc, val)
print("min L(c) sampled over c in [1, 1000]:", worst, " (should be well above 0)")
print("L(1) exactly:", mp.nstr(L(1), 20))
print()

# ---------------------------------------------------------------
# (4) B(n,c) evaluation and asymptotics
# ---------------------------------------------------------------
def B(n, c):
    n = mp.mpf(n); c = mp.mpf(c)
    return (a_star*mp.sqrt(c) + kappa_B) / (n * L(c))

print("=== (4a) Upper edge c_n = n^(2/3)/log(n): decay and leading order ===")
leading_const = 2*a_star/mp.sqrt(mp.pi)
print("leading constant (2 a*/sqrt(pi)) =", mp.nstr(leading_const, 15))
prev = None
ns = [10, 100, 1000, 10**4, 10**6, 10**9, 10**12, 10**20, 10**50, 10**100,
      10**200, 10**300]
for n in ns:
    n_mp = mp.mpf(n)
    c_n = n_mp**mp.mpf('2')/mp.mpf(3) / mp.log(n_mp)
    # NB: n^(2/3) via mpower
    c_n = n_mp**(mp.mpf(2)/3) / mp.log(n_mp)
    b = B(n_mp, c_n)
    leading = leading_const * n_mp**(mp.mpf(-1)/3) / mp.log(n_mp)
    ratio = b/leading
    decreasing = (prev is None) or (b < prev)
    print(f"n=10^{float(mp.log10(n_mp)):.0f}  c_n={mp.nstr(c_n,6):>14}  B={mp.nstr(b,10):>14}"
          f"  B/leading={mp.nstr(ratio,10)}  decreasing_so_far={decreasing}")
    prev = b
print()

print("=== (4b) Lower edge c_n = n^eps for eps in {0.1,0.3,0.5}: decay rate O(n^(eps-1)) ===")
for eps in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5')]:
    print(f"-- eps={eps} --")
    prevb = None
    for n in [10**2, 10**4, 10**8, 10**16, 10**32, 10**64]:
        n_mp = mp.mpf(n)
        c_n = n_mp**eps
        b = B(n_mp, c_n)
        leading = leading_const * n_mp**(eps-1)
        ratio = b/leading
        print(f"   n=10^{float(mp.log10(n_mp)):.0f}  c_n={mp.nstr(c_n,8):>10}  B={mp.nstr(b,10)}"
              f"  B/leading={mp.nstr(ratio,8)}")
    print()

# ---------------------------------------------------------------
# (5) Window non-emptiness for various eps, and disjointness check
# ---------------------------------------------------------------
print("=== (5) Window non-emptiness: n^eps <= n^(2/3)/log(n) ? ===")
for eps in [mp.mpf(x) for x in ['0.1','0.3','0.5','0.6','0.65','0.6667','0.7','0.9']]:
    # find smallest n (power of 10) where window nonempty
    found = None
    n = mp.mpf(10)
    for _ in range(400):
        lhs = n**eps
        rhs = n**(mp.mpf(2)/3)/mp.log(n)
        if lhs <= rhs:
            found = n
            break
        n *= 10
    print(f"eps={float(eps):<8} first nonempty at n~10^{float(mp.log10(found)):.0f}" if found
          else f"eps={float(eps):<8} NOT nonempty up to n=10^400")
print()

print("=== (5b) Disjointness from Corolario 2's threshold order n^(2/3) log n ===")
for n in [mp.mpf(x) for x in [3, mp.e, 10, 100, 10**6]]:
    upper_edge = n**(mp.mpf(2)/3)/mp.log(n) if n>1 else None
    threshold = n**(mp.mpf(2)/3)*mp.log(n) if n>1 else None
    if n>1:
        print(f"n={mp.nstr(n,6)}: window upper edge={mp.nstr(upper_edge,8)}  "
              f"Corolario-2 threshold order={mp.nstr(threshold,8)}  "
              f"upper_edge < threshold: {upper_edge < threshold}")
print("(at n=e both sides equal log(n)=1: 1/1 vs 1*1 -- boundary case, ATTEMPT.md claims 'n>e')")
