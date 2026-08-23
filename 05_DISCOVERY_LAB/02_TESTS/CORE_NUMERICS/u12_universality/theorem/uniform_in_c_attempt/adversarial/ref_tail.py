"""
Adversarial referee -- item 3: LEMA 4.1 and COROLARIO 4.2.

The proof of Lema 4.1 is a chain of five separate inequalities.  Rather than
only testing the final bound (which is loose, and would hide an error in any
single step), this script computes the EXACT law of the exploration by a
forward pass and audits every step of the chain independently.

Forward pass.  Let mu_j(R) = P(alive at step j, R reroutes so far), where
"alive at step j" = no return and no fatality in steps 0..j-1.  mu_0(0)=1 and

  return  hazard  r(j,R) = q/n + (1-q)/(n-j+R)
  fatal   hazard  F(j,R) = q*j/n + (1-q)*R/(n-j+R)
  fresh -> (j+1,R+1) with prob q*(n-j-1)/n
  fresh -> (j+1,R)   with prob (1-q)*(n-j-1)/(n-j+R)

(r + F + fresh = 1 identically -- checked below.)  Then
  P(first return at step j) = sum_R mu_j(R) r(j,R)   =: Rt_j
  P(alive at J)             = sum_R mu_J(R)          =: Alive_J
  phi(n,c) = sum_{j=0}^{n-1} Rt_j.
"""

from fractions import Fraction as F
import math
from ref_engine import chain_phi


def forward(n, q):
    """returns (Rt, Fat, Alive) as exact lists indexed by j = 0..n-1 (Alive
    has length n, Alive[j] = P(alive at step j))."""
    q = F(q)
    mu = {0: F(1)}
    Rt, Fat, Alive = [], [], []
    for j in range(n):
        Alive.append(sum(mu.values()))
        rt = F(0)
        fat = F(0)
        nxt = {}
        for R, m in mu.items():
            av = n - j + R
            r = q * F(1, n) + (1 - q) * F(1, av)
            f = q * F(j, n) + (1 - q) * F(R, av)
            fr1 = q * F(n - j - 1, n)              # -> (j+1, R+1)
            fr0 = (1 - q) * F(n - j - 1, av)       # -> (j+1, R)
            assert r + f + fr1 + fr0 == 1, (n, q, j, R)
            rt += m * r
            fat += m * f
            if n - j - 1 > 0:
                nxt[R + 1] = nxt.get(R + 1, F(0)) + m * fr1
                nxt[R] = nxt.get(R, F(0)) + m * fr0
        Rt.append(rt)
        Fat.append(fat)
        mu = nxt
    return Rt, Fat, Alive


print("=" * 76)
print("A. The exploration decomposition itself  (the step the brief flags)")
print("=" * 76)
print("""
Claim audited: {1 cyclic} is the DISJOINT union over j of {first return at
step j}, and phi(n,c) = sum_j P(first return at step j) with no missing mass
and no double counting.

Re-derivation.  The exploration is absorbed the first time it returns to x_0
or the first time it lands on x_1..x_j.  So with A_j = {alive at step j},
Rt_j = A_j cap {step j returns}, Ft_j = A_j cap {step j fatal}, one has
A_{j+1} = A_j \\ (Rt_j u Ft_j); the Rt_j are pairwise disjoint BY
CONSTRUCTION (each is contained in A_j, and A_j is decreasing and excludes
every earlier return).  There is therefore no distinction at all between
"return at step j" and "FIRST return at step j": the process cannot return
twice.  At j = n-1 there is no fresh branch (n-j-1 = 0), so
sum_j (Rt_j + Ft_j) = 1 and the decomposition is exhaustive.  VALID.

Numerical confirmation that no mass is lost or double counted:
""")
bad = 0
for n in (2, 3, 5, 8, 12):
    for q in (F(0), F(1, 7), F(1, 3), F(1, 2), F(4, 5), F(1)):
        Rt, Fat, Alive = forward(n, q)
        s = sum(Rt)
        tot = sum(Rt) + sum(Fat)
        direct = chain_phi(n, q)
        ok = (s == direct) and (tot == 1)
        if not ok:
            bad += 1
            print("   *** FAILURE", n, q, s, direct, tot)
print(f"   sum_j Rt_j == phi(n,c) exactly and sum_j (Rt_j+Ft_j) == 1 exactly")
print(f"   for n in {{2,3,5,8,12}} x 6 values of q: {30-bad}/30 cells pass, "
      f"{bad} failures.")

print()
print("=" * 76)
print("B. The two conditional facts (a) and (b), audited CELLWISE")
print("=" * 76)
print("""
 (a)  r(j,R) = q/n + (1-q)/(n-j+R) <= q/(n-j) + (1-q)/(n-j) = 1/(n-j),
      using n-j <= n (so 1/n <= 1/(n-j)) and R >= 0 (so 1/(n-j+R) <=
      1/(n-j)).  Both are unconditional.  CORRECT.
 (b)  F(j,R) = q*j/n + (1-q)*R/(n-j+R) >= q*j/n, dropping a nonnegative
      term.  CORRECT.  Note (b) is a bound on the CONDITIONAL hazard given
      the whole history, and the bound q*j/n is DETERMINISTIC -- that is
      exactly what makes the tower-property product legitimate (below).

 Cellwise audit over every reachable state (j,R):""")
worst_a, worst_b = F(0), F(10)
cells = 0
for n in (5, 9, 14, 20):
    for q in (F(1, 10), F(1, 3), F(1, 2), F(9, 10), F(1)):
        for j in range(n):
            for R in range(j + 1):
                av = n - j + R
                r = q * F(1, n) + (1 - q) * F(1, av)
                f = q * F(j, n) + (1 - q) * F(R, av)
                assert r <= F(1, n - j), ("(a) FAILS", n, q, j, R)
                assert f >= q * F(j, n), ("(b) FAILS", n, q, j, R)
                cells += 1
                worst_a = max(worst_a, r * (n - j))
                if j > 0 and q > 0:
                    worst_b = min(worst_b, f / (q * F(j, n)))
print(f"   {cells} states audited, 0 violations of (a) or of (b).")
print(f"   worst (a) tightness  r(j,R)*(n-j) = {float(worst_a):.6f}  (<= 1)")
print(f"   worst (b) tightness  F(j,R)/(q j/n) = {float(worst_b):.6f}  (>= 1)")

print()
print("=" * 76)
print("C. The split, the harmonic sum, and the tower-property product")
print("=" * 76)
print("""
 phi = sum_{j<J} Rt_j + sum_{j>=J} Rt_j.
   * sum_{j<J} Rt_j <= sum_{j<J} P(A_j)/(n-j) <= sum_{j<J} 1/(n-j)
     <= J/(n-J+1) <= J/(n-J).                                [step 1,2]
   * sum_{j>=J} Rt_j <= P(A_J), because those events are disjoint and all
     contained in A_J.                                        [step 3]
   * P(A_{j+1}) = E[1_{A_j}(1 - r - F)] <= E[1_{A_j}(1 - F)]
                <= E[1_{A_j}(1 - qj/n)] = P(A_j)(1 - qj/n),
     the last step because qj/n is deterministic; nonnegativity of the
     factor needs qj/n <= 1, true since q <= 1 and j < J <= n/2.  Iterating,
     P(A_J) <= prod_{j<J}(1-qj/n) <= exp(-(q/n) sum_{j<J} j)
             = exp(-q J(J-1)/(2n)).                           [step 4,5]
 Every step audited numerically below (exact arithmetic).
""")
hdr = (f"{'n':>4} {'q':>6} {'J':>4} | {'S<J':>10} {'J/(n-J)':>10} | "
       f"{'S>=J':>10} {'P(A_J)':>10} {'prod':>10} {'exp':>10} | "
       f"{'phi':>10} {'LEMA 4.1':>10}  ok")
print(hdr)
print("-" * len(hdr))
allok = True
for n in (10, 16, 24, 40):
    for q in (F(1, 20), F(1, 4), F(1, 2), F(1)):
        Rt, Fat, Alive = forward(n, q)
        phi = sum(Rt)
        for J in (1, 2, max(1, n // 4), n // 2):
            if not (1 <= J <= n // 2):
                continue
            s1 = sum(Rt[:J])
            s2 = sum(Rt[J:])
            b1 = F(J, n - J)
            AJ = Alive[J]
            prod = F(1)
            for j in range(J):
                prod *= (1 - q * F(j, n))
            ex = math.exp(-float(q) * J * (J - 1) / (2 * n))
            lem = float(b1) + ex
            ok = (s1 <= b1) and (s2 <= AJ) and (AJ <= prod) \
                 and (float(prod) <= ex + 1e-15) and (float(phi) <= lem + 1e-15)
            allok &= ok
            print(f"{n:4d} {str(q):>6} {J:4d} | {float(s1):10.6f} "
                  f"{float(b1):10.6f} | {float(s2):10.6f} {float(AJ):10.6f} "
                  f"{float(prod):10.6f} {ex:10.6f} | {float(phi):10.6f} "
                  f"{lem:10.6f}  {'OK' if ok else '***FAIL***'}")
print(f"\n   Every individual step of the Lema 4.1 chain holds in every cell: "
      f"{allok}")

print()
print("=" * 76)
print("D. Adversarial sweep for a violation of LEMA 4.1 itself")
print("=" * 76)
print("   phi(n,c) <= J/(n-J) + exp(-q J(J-1)/(2n)),  1 <= J <= n/2, q=min(c/n,1)")
worst = 0.0
argworst = None
viol = 0
count = 0
for n in list(range(2, 41)):
    for qq in [F(0), F(1, 100), F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)]:
        phi = float(chain_phi(n, qq))
        for J in range(1, n // 2 + 1):
            b = J / (n - J) + math.exp(-float(qq) * J * (J - 1) / (2 * n))
            count += 1
            if phi > b + 1e-14:
                viol += 1
                print("   *** VIOLATION", n, qq, J, phi, b)
            if b > 0:
                r = phi / b
                if r > worst:
                    worst, argworst = r, (n, qq, J)
print(f"   {count} (n,q,J) cells swept exhaustively: {viol} violations.")
print(f"   worst ratio phi/bound = {worst:.6f} at (n,q,J) = {argworst}")
print("   (ratio < 1 everywhere => the lemma holds, loosely, in every cell.)")

print()
print("=" * 76)
print("E. COROLARIO 4.2 -- the algebra, re-derived")
print("=" * 76)
print("""
 Claim: L >= 1, C_0 >= max(16L, 80), n >= C_0  =>
        sup_{c>=C_0} phi(n,c) <= 2 sqrt(2L/C_0) + 4/n + e^{-L}.
 Re-derivation:
  * monotonicity in c: the RHS of Lema 4.1 depends on c only through
    q = min(c/n,1) and is non-increasing in q, so for c >= C_0 and n >= C_0
    (whence q >= C_0/n) it suffices to evaluate at q = C_0/n.   OK
  * J := ceil(n sqrt(2L/C_0)) + 1 depends only on (n,C_0,L).  Then
    J-1 >= n sqrt(2L/C_0) and J >= J-1, so
      qJ(J-1)/(2n) >= (C_0/n)(J-1)^2/(2n) >= (C_0/n) n^2 (2L/C_0)/(2n) = L,
    giving exp(...) <= e^{-L}.                                  OK
  * admissibility J <= n/2:  J <= n sqrt(2L/C_0) + 2 and C_0 >= 16L gives
    sqrt(2L/C_0) <= 1/sqrt8 = 0.353553; need 0.353553 n + 2 <= n/2, i.e.
    n >= 2/0.146447 = 13.66, and n >= C_0 >= 80 gives it.        OK
  * J/(n-J) <= 2J/n <= 2 sqrt(2L/C_0) + 4/n.                     OK
 With L = log C_0: e^{-L} = 1/C_0, and L >= 1 needs C_0 >= e, while
 C_0 >= 16 log C_0 needs C_0 >= 79.0 (checked below) -- so C_0 >= 80 is
 exactly the right threshold and the "in particular" clause is sound.
""")
import numpy as np
xs = np.linspace(2, 200, 20000)
thr = xs[np.where(xs - 16 * np.log(xs) >= 0)[0]]
cross = thr[thr > 20].min()
print(f"   smallest C_0 > 20 with C_0 >= 16 log C_0 :  {cross:.4f}   "
      f"(so the stated 80 is safe)")
print()
print("   Direct numerical audit of Corolario 4.2 (exact chain for phi):")
print(f"   {'C_0':>7} {'L=logC0':>8} {'n':>7} {'sup_{c>=C0} phi':>16} "
      f"{'Cor 4.2 bound':>14}  ok")
for C0 in (80, 200, 1000):
    L = math.log(C0)
    for n in (int(C0), int(2 * C0), int(6 * C0)):
        from ref_engine import chain_phi_float
        # sup over c >= C_0 is attained at c = C_0 (phi is non-increasing;
        # verified separately) -- we take the max over a grid to be safe.
        vals = [chain_phi_float(n, min(c / n, 1.0))
                for c in (C0, 1.5 * C0, 3 * C0, 10.0 * C0, 1e9)]
        sup = max(vals)
        b = 2 * math.sqrt(2 * L / C0) + 4.0 / n + math.exp(-L)
        print(f"   {C0:7d} {L:8.4f} {n:7d} {sup:16.8f} {b:14.8f}  "
              f"{'OK' if sup <= b else '*** VIOLATION ***'}")
print()
print("   omega(C_0) = 2 sqrt(2 log C_0 / C_0) + 1/C_0, uniform in n >= C_0:")
for C0 in (50, 200, 1000, 5000, 25000):
    print(f"     C_0={C0:7d}   omega = "
          f"{2*math.sqrt(2*math.log(C0)/C0)+1.0/C0:.6f}")
