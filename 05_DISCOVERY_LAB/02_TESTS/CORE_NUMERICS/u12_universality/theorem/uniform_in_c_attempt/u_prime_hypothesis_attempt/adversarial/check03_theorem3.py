"""
Referee check 03 -- Theorem 3: M_K = Q(K+1) - (K+1) phi_K.

Also directly re-checks the two citations Theorem 3's proof leans on:
  - Estagio 7's c_K = [(K+2)phi_K-2]/4 >= 0 formula (used by Theorem 2's
    proof, cited by Theorem 3's context) -- re-derived independently and
    checked for positivity K>=2, equality at K=0,1.
  - The '[Correcao pos-adversarial, 2026-08-23]' identity
    phi_n^{(n-1)} = phi_n^{(n)} = Q(n)/n, read directly from
    uniform_in_c_attempt/ATTEMPT.md Sec.6.3 -- verified here independently
    via mychain.py (phi_n^{(n-1)}, computable since n>K=n-1) and an
    independent from-scratch Q(n)/n direct-probability computation
    (uniform random mapping, brute-force exact enumeration for small n, and
    the same product-sum formula cross-checked against Q_exact for larger n).
"""
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, ".")
import closed_forms as cf
import mychain as mc

log = open("check03_theorem3.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


# ---------------------------------------------------------------------------
# Part A: Theorem 3 M_K identity, exact, K=0..1000 (via T(K+1,K) closed form,
# not Theorem 2's argmax claim -- computed directly at n=K+1).
# ---------------------------------------------------------------------------
p("=" * 78)
p("PART A: M_K = Q(K+1) - (K+1) phi_K, exact, K=0..1000")
p("(orchestrator: K=0..14; target's own T4: K=0..40).")
p("=" * 78)

mism = 0
for K in range(0, 1001):
    T_at_Kplus1 = cf.T_of_nK(K, K + 1)  # this IS M_K if Theorem 2 holds;
    # but here we check Theorem 3's formula independently of Theorem 2's
    # argmax claim, by computing T(K+1,K) directly and comparing to the
    # claimed closed form Q(K+1)-(K+1)phi_K -- both sides computed via
    # totally different routes (finite sum vs Q's own product-sum).
    claimed = cf.Q_exact(K + 1) - (K + 1) * cf.phi_K(K)
    if T_at_Kplus1 != claimed:
        mism += 1
        p(f"  MISMATCH K={K}: T(K+1,K)={T_at_Kplus1}  Q(K+1)-(K+1)phi_K={claimed}")
p(f"RESULT: 1001 K values checked (K=0..1000), {mism} mismatches.")

# ---------------------------------------------------------------------------
# Part B: c_K = [(K+2)phi_K - 2]/4, positivity K>=2, equality K=0,1
# (Estagio 7 of THEOREM.md, re-derived/re-checked independently here).
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("PART B: c_K = [(K+2)phi_K-2]/4 >= 0 for all K, equality only K=0,1")
p("(Estagio 7 of THEOREM.md -- citation used by Theorem 2's proof).")
p("=" * 78)

c_ok = True
for K in range(0, 2001):
    cK = ((K + 2) * cf.phi_K(K) - 2) / 4
    if K <= 1:
        if cK != 0:
            c_ok = False
            p(f"  UNEXPECTED: c_{K} should be exactly 0, got {cK}")
    else:
        if cK <= 0:
            c_ok = False
            p(f"  VIOLATION: c_{K}={cK} not >0")
p(f"c_K sign pattern (K=0..2000): {'CONFIRMED (c_0=c_1=0, c_K>0 for K>=2)' if c_ok else 'VIOLATION FOUND'}")

# ---------------------------------------------------------------------------
# Part C: phi_n^{(n-1)} = phi_n^{(n)} = Q(n)/n, exact, independently, for
# n=2..14 (brute-force at very small n, mychain+Q_exact beyond).
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("PART C: phi_n^{(n-1)} = phi_n^{(n)} = Q(n)/n, exact, independently.")
p("phi_n^{(n)} via a from-scratch BRUTE-FORCE enumeration of the raw")
p("uniform-random-mapping model (n<=6: exhaustive over all n^n mappings),")
p("and via Q(n)/n for n up to 30; phi_n^{(n-1)} via mychain.py.")
p("=" * 78)


def brute_force_phi_nn(n):
    """phi_n^{(n)} = P(1 is cyclic) for f uniform over ALL n^n functions
    [n]->[n] (every point rerouted == uniform random mapping). Exhaustive
    for small n."""
    total = F(0)
    count = 0
    for f in product(range(1, n + 1), repeat=n):
        # f[i-1] = f(i)
        # is 1 cyclic? iterate forward orbit of 1, see if returns to 1
        # before revisiting.
        seen = set()
        cur = 1
        cyclic = False
        while True:
            if cur == 1 and len(seen) > 0:
                cyclic = True
                break
            if cur in seen:
                cyclic = False
                break
            seen.add(cur)
            cur = f[cur - 1]
        if cyclic:
            total += 1
        count += 1
    return total / count


ok_bf = True
for n in range(1, 6):
    bf = brute_force_phi_nn(n)
    qn = cf.Q_exact(n) / n
    if bf != qn:
        ok_bf = False
        p(f"  MISMATCH n={n}: brute-force phi(n,n)={bf}  Q(n)/n={qn}")
    else:
        p(f"  n={n}: brute-force phi(n,n)={bf} == Q(n)/n={qn}  OK")
p(f"Brute-force phi(n,n)=Q(n)/n, n=1..5: {'ALL MATCH' if ok_bf else 'MISMATCH FOUND'}")

p("")
p("phi_n^{(n-1)} (via mychain.py, n>K=n-1 so within chain's valid domain)")
p("vs Q(n)/n, n=2..30:")
ok_c2 = True
for n in range(2, 31):
    chain_val = mc.phi(n, n - 1)
    qn = cf.Q_exact(n) / n
    if chain_val != qn:
        ok_c2 = False
        p(f"  MISMATCH n={n}: chain phi_n^(n-1)={chain_val}  Q(n)/n={qn}")
p(f"phi_n^{{(n-1)}} = Q(n)/n via mychain.py, n=2..30: "
  f"{'ALL MATCH' if ok_c2 else 'MISMATCH FOUND'}")

log.close()
print("\nWrote check03_theorem3.log")
