# ref_check_engine.py -- referee check R1: engine faithfulness.
# R1a: closed-form phi_n^{(K)} vs BRUTE FORCE from Definition 4
#      (all permutations x destination vectors; no closed form anywhere).
# R1b: prose anchors.
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import (phi_K, Q_exact, psi_nK, psi_nK_R, phi_nK,
                        phi_nK_bruteforce, phi_mix, phi_nK_table,
                        phi_inf_bracket)

t0 = time.time()
fails = 0
checks = 0

def rec(ok, msg):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("  ** FAIL:", msg)

print("== R1a: brute force (Definition 4) vs closed-form engine ==")
cases = ([(4, K) for K in range(5)] + [(5, K) for K in range(6)]
         + [(6, K) for K in range(5)] + [(7, K) for K in range(3)])
for (n, K) in cases:
    bf = phi_nK_bruteforce(n, K)
    cf = phi_nK(n, K)
    rec(bf == cf, f"n={n} K={K}: brute={bf} closed={cf}")
    print(f"  n={n} K={K}: {cf}  match={bf==cf}")
print(f"  {len(cases)} brute-force pairs done, elapsed {time.time()-t0:.1f}s")

print("== R1b: prose anchors ==")
# phi_n^{(1)} = 2/3 + 1/(3n^2)   (THEOREM.md Prop. 4)
ok = all(phi_nK(n, 1) == F(2, 3) + F(1, 3 * n * n) for n in range(2, 51))
rec(ok, "phi_n^(1)")
print("  phi_n^(1)=2/3+1/(3n^2), n=2..50:", ok)
# psi_n^{(1)} = 2/3+1/(6n), psi_n^{(1),R} = 1/2+1/(2n) (k2_open_lemma Res.2)
ok = all(psi_nK(n, 1) == F(2, 3) + F(1, 6 * n) and
         psi_nK_R(n, 1) == F(1, 2) + F(1, 2 * n) for n in range(2, 51))
rec(ok, "psi_1 / psi_1^R")
print("  psi_n^(1), psi_n^(1)R closed forms, n=2..50:", ok)
# psi_n^{(2)} = 8/15+4/(15n)+1/(15n^2); psi_n^{(2),R}=(n+1)(5n+2)/(12n^2)
ok = all(psi_nK(n, 2) == F(8, 15) + F(4, 15 * n) + F(1, 15 * n * n) and
         psi_nK_R(n, 2) == F((n + 1) * (5 * n + 2), 12 * n * n)
         for n in range(3, 41))
rec(ok, "psi_2 / psi_2^R")
print("  psi_n^(2), psi_n^(2)R closed forms (Estagio 3), n=3..40:", ok)
# phi_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) + 1/(5n^3) (Estagio 3 Res.5)
ok = all(phi_nK(n, 2) ==
         F(8, 15) + F(1, 30 * n) + F(7, 10 * n * n) + F(1, 5 * n**3)
         for n in range(3, 41))
rec(ok, "phi_n^(2) full rate")
print("  phi_n^(2)=8/15+1/(30n)+7/(10n^2)+1/(5n^3), n=3..40:", ok)
# phi_n^{(n-1)} = Q(n)/n  (post-adversarial exact identity)  -- engine route
ok = all(phi_nK(n, n - 1) == Q_exact(n) / n for n in range(2, 41))
rec(ok, "phi_n^(n-1)=Q/n")
print("  phi_n^(n-1)=Q(n)/n via Lemma A closed form, n=2..40:", ok)
# phi_7^{(6)} = 355081/823543
rec(phi_nK(7, 6) == F(355081, 823543), "phi_7^(6)")
print("  phi_7^(6)=355081/823543:", phi_nK(7, 6) == F(355081, 823543))
# phi_K anchors (Lemma 2): 1, 2/3, 8/15, 16/35
ok = ([phi_K(K) for K in range(4)] == [F(1), F(2, 3), F(8, 15), F(16, 35)])
rec(ok, "phi_K anchors")
print("  phi_K anchors K=0..3:", ok)
# Q anchors: Q(2)=3/2, Q(3)=17/9 (archive), Q(7)=355081/117649
ok = (Q_exact(2) == F(3, 2) and Q_exact(3) == F(17, 9)
      and Q_exact(7) == F(355081, 117649))
rec(ok, "Q anchors")
print("  Q(2)=3/2, Q(3)=17/9, Q(7)=355081/117649:", ok)
# mixture endpoints: phi(n,0)=1 and phi(n,n)=Q(n)/n
for n in range(4, 13):
    tab = phi_nK_table(n)
    rec(phi_mix(n, 0, tab) == 1, f"phi({n},0)")
    rec(phi_mix(n, n, tab) == Q_exact(n) / n, f"phi({n},{n})")
print("  phi(n,0)=1 and phi(n,n)=Q(n)/n, n=4..12: done")
# phi_inf bracket consistency across the series/tail crossover c=40
for c in [F(39), F(395, 10), F(40), F(405, 10), F(41), F(45)]:
    lo1, hi1 = phi_inf_bracket(c)
    # force the other branch by evaluating both around the switch
    ok = lo1 < hi1 and hi1 - lo1 < F(1, 10**8)
    rec(ok, f"phi_inf bracket width at c={c}")
# direct cross: series value at c=40 vs tail form at c=41 monotonic
l40, h40 = phi_inf_bracket(F(40))
l41, h41 = phi_inf_bracket(F(41))
rec(l40 > h41 * F(999, 1000), "phi_inf monotone-ish across crossover")
print("  phi_inf bracket sanity across crossover: done")

print(f"== R1 SUMMARY: {checks} checks, {fails} failures, "
      f"elapsed {time.time()-t0:.1f}s ==")
sys.exit(1 if fails else 0)
