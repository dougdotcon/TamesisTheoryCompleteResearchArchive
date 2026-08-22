"""
Referee check #5: independent exact enumeration for K=2 (Definition 4, two
fixed rerouted indices 1,2), fresh implementation, cross-checking the table
in THEOREM.md S7.4 (n=2..4 spot check; n=5 if time allows) against
phi_n^(2) claimed there: n=2: 3/4, n=3: 17/27, n=4: 113/192.
"""
import itertools
from fractions import Fraction

def num_cyclic(f, n):
    cnt = 0
    for x in range(n):
        cur = f[x]
        steps = 1
        found = False
        while steps <= n:
            if cur == x:
                found = True
                break
            cur = f[cur]
            steps += 1
        if found:
            cnt += 1
    return cnt

def exact_phi_K2(n):
    total = Fraction(0)
    count = 0
    for perm in itertools.permutations(range(n)):
        pi = list(perm)
        for U1 in range(n):
            for U2 in range(n):
                f = list(pi)
                f[0] = U1
                f[1] = U2
                c = num_cyclic(f, n)
                total += Fraction(c, n)
                count += 1
    return total / count

if __name__ == "__main__":
    claimed = {2: Fraction(3,4), 3: Fraction(17,27), 4: Fraction(113,192)}
    for n in [2, 3, 4]:
        phi = exact_phi_K2(n)
        print(f"n={n}: my_exact={phi} = {float(phi):.6f}   claimed_in_THEOREM.md={claimed[n]} = {float(claimed[n]):.6f}   match={phi==claimed[n]}")
